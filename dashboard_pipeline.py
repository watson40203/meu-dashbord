#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard de Pipeline e Previsibilidade (IM Incorporadora)
Segundo dashboard, separado do principal. Usa os dados do RD Station CRM.
Gera o arquivo: dashboard_pipeline.html
"""

import json
import os
import calendar
from datetime import datetime
from collections import defaultdict

# ─────────────────────────────────────────────────────────────────────────────
# EQUIPE E METAS (fixas — edite aqui se um dia precisar mudar)
# Os nomes batem por aproximação com o "responsável" da negociação no RD,
# então não precisa ser o nome completo exato.
# ─────────────────────────────────────────────────────────────────────────────

EQUIPE = {
    "Corretor":                 ["joão vasconcelos", "jonathan vitorino"],
    "Coordenadora de Plataforma": ["giovana", "jéssica cararo"],
    "SDR":                      ["dirlei", "nicolas", "lucas", "adriano"],
}

NOMES_DISPLAY = {
    "joão vasconcelos": "João Vasconcelos",
    "jonathan vitorino": "Jonathan Vitorino",
    "giovana": "Giovana",
    "jéssica cararo": "Jéssica Cararo",
    "dirlei": "Dirlei",
    "nicolas": "Nicolas",
    "lucas": "Lucas",
    "adriano": "Adriano",
}

META_VGV_PESSOA   = 800000.0    # meta de VGV por corretor/coordenadora
META_ENT_PESSOA   = 100000.0    # meta de entrada por corretor/coordenadora
META_REUNIOES_SDR = 30          # meta de reuniões realizadas por SDR
META_MACRO_VGV    = 3200000.0   # meta macro de VGV (mês) — meta da equipe
META_MACRO_ENT    = 300000.0    # meta macro de entrada (mês) — meta da equipe

# Números de marketing/conversas exibidos no dashboard KPIs (index.html).
# Por enquanto são fixos. Para deixar ao vivo, ligue-os ao dashboard_api.py
# (buscar_marketing / buscar_conversas) e atualize estes valores.
LEADS_MARKETING   = 4125
LEADS_CRM         = 6300

# Template do dashboard KPIs (precisa estar no repo, ao lado deste arquivo)
KPIS_TEMPLATE     = "index_template.html"
KPIS_OUTPUT       = "index.html"

CICLO_VENDA_PADRAO = 60         # dias (usado enquanto não há negócios novos suficientes)

# Ordem do funil (palavras-chave). "Reunião realizada" conta a partir de ETAPA_REUNIAO.
FUNIL_ORDEM   = ["lead", "contato", "agendamento", "atendimento", "proposta", "negocia", "fecha", "ganho"]
ETAPA_REUNIAO = "atendimento"

CONFIG_FILE = "config_pipeline.json"

DEFAULT_PESOS = {
    "lead": 5, "contato": 10, "agendamento": 20, "atendimento": 35,
    "visita": 35, "proposta": 45, "negocia": 55, "fecha": 100, "ganho": 100,
}
DIAS_PARADO = 14


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG (config_pipeline.json) — só o que muda no dia a dia:
#   - realizado_entrada: entrada realizada por mês (entrada não existe no RD)
#   - transicao: no mês de transição, só contam os negócios listados
#   - pesos / ciclo_venda_dias / dias_parado: ajustes finos
# ─────────────────────────────────────────────────────────────────────────────

def carregar_config():
    cfg = {
        "pesos": dict(DEFAULT_PESOS),
        "dias_parado": DIAS_PARADO,
        "ciclo_venda_dias": CICLO_VENDA_PADRAO,
        "realizado_entrada": {},
        "transicao": {},
    }
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                if isinstance(data.get("pesos"), dict) and data["pesos"]:
                    cfg["pesos"] = {str(k).lower(): float(v) for k, v in data["pesos"].items()}
                if data.get("dias_parado"):
                    cfg["dias_parado"] = int(data["dias_parado"])
                if data.get("ciclo_venda_dias"):
                    cfg["ciclo_venda_dias"] = int(data["ciclo_venda_dias"])
                if isinstance(data.get("realizado_entrada"), dict):
                    cfg["realizado_entrada"] = {str(k): float(v) for k, v in data["realizado_entrada"].items()}
                if isinstance(data.get("transicao"), dict):
                    cfg["transicao"] = data["transicao"]
            print(f"Config carregada de {CONFIG_FILE}")
    except Exception as e:
        print(f"Config: usando padrão ({e})")
    return cfg


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE CLASSIFICAÇÃO
# ─────────────────────────────────────────────────────────────────────────────

def peso_da_etapa(stage, pesos):
    s = (stage or "").lower()
    for kw, w in pesos.items():
        if kw in s:
            return w
    return 50


def classificar(stage):
    s = (stage or "").lower()
    if "perdid" in s or "perda" in s:
        return "perdido"
    if "fecha" in s or "ganho" in s or "ganha" in s:
        return "ganho"
    return "aberto"


def rank_etapa(stage):
    s = (stage or "").lower()
    if "perdid" in s or "perda" in s:
        return -1
    melhor = 0
    for i, kw in enumerate(FUNIL_ORDEM):
        if kw in s:
            melhor = i
    return melhor


RANK_REUNIAO = FUNIL_ORDEM.index(ETAPA_REUNIAO)


def teve_reuniao(stage):
    return rank_etapa(stage) >= RANK_REUNIAO


def membro_de(nome_resp):
    """Retorna a chave do membro da equipe (ou None) batendo por aproximação."""
    n = (nome_resp or "").lower()
    for papel, nomes in EQUIPE.items():
        for kw in nomes:
            if kw in n:
                return kw, papel
    return None, None


# ─────────────────────────────────────────────────────────────────────────────
# BUSCA NO RD STATION CRM
# ─────────────────────────────────────────────────────────────────────────────

def buscar_crm():
    import requests
    token = os.environ.get("TOKEN_CRM", "")
    if not token:
        print("AVISO: TOKEN_CRM nao configurado — dashboard sai vazio.")
        return []

    todas = []
    pagina = 1
    MAX_PAGINAS = 200
    print("Buscando negocios no RD Station CRM...", flush=True)
    while pagina <= MAX_PAGINAS:
        url = f"https://crm.rdstation.com/api/v1/deals?token={token}&limit=200&page={pagina}"
        try:
            r = requests.get(url, timeout=30)
            if r.status_code != 200:
                print(f"Erro pagina {pagina}: HTTP {r.status_code}", flush=True)
                break
            negs = r.json().get("deals", [])
            if not negs:
                break
            todas.extend(negs)
            print(f"Pagina {pagina}: {len(negs)} negocios (total {len(todas)})", flush=True)
            if len(negs) < 200:
                break
            pagina += 1
        except Exception as e:
            print(f"Erro CRM pagina {pagina}: {e}", flush=True)
            break
    print(f"Busca finalizada: {len(todas)} negocios.", flush=True)

    deals = []
    for n in todas:
        try:
            stage = (n.get("deal_stage") or {}).get("name", "Sem etapa")
            try:
                valor = float(n.get("amount_total") or 0)
            except Exception:
                valor = 0.0
            criado = str(n.get("created_at") or "")[:10]
            fechado = n.get("closed_at")
            fechado = str(fechado)[:10] if fechado else None
            atualizado = n.get("updated_at")
            atualizado = str(atualizado)[:10] if atualizado else None
            motivo = ""
            for campo in ("deal_lost_reason", "loss_reason", "lost_reason"):
                lr = n.get(campo)
                if isinstance(lr, dict) and lr.get("name"):
                    motivo = lr["name"]; break
                if isinstance(lr, str) and lr:
                    motivo = lr; break
            user = n.get("user") or {}
            resp = user.get("name", "Sem responsável") if isinstance(user, dict) else "Sem responsável"
            deals.append({
                "nome": n.get("name", "") or "",
                "stage": stage,
                "value": valor,
                "created_at": criado,
                "closed_at": fechado,
                "updated_at": atualizado,
                "loss_reason": motivo,
                "user": resp or "Sem responsável",
            })
        except Exception as e:
            print(f"Erro processando negocio: {e}")
    return deals


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE FORMATAÇÃO
# ─────────────────────────────────────────────────────────────────────────────

def R(v):
    try:
        s = f"{float(v):,.2f}"
    except Exception:
        s = "0,00"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")


def R0(v):
    try:
        return "R$ " + f"{round(float(v)):,}".replace(",", ".")
    except Exception:
        return "R$ 0"


def cor_pct(p):
    if p >= 100:
        return "var(--green)"
    if p >= 50:
        return "var(--yellow)"
    return "var(--red)"


def dias_desde(data_str):
    if not data_str:
        return None
    try:
        d = datetime.strptime(data_str, "%Y-%m-%d").date()
        return (datetime.now().date() - d).days
    except Exception:
        return None


MESES_PT = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f5f5f7;--card:#fff;--t:#1d1d1f;--t2:#6e6e73;--t3:#aeaeb2;--bd:#e3e3e6;
  --bl:#0071e3;--gr:#28cd41;--rd:#ff3b30;--or:#ff9500;--yellow:#ffcc00;--pu:#5e5ce6;
  --green:#28cd41;--red:#ff3b30;
}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--t);-webkit-font-smoothing:antialiased;padding:24px 16px 60px}
.wrap{max-width:1180px;margin:0 auto}
.top{display:flex;align-items:center;gap:14px;margin-bottom:6px}
.logo{width:34px;height:34px;border-radius:8px;background:var(--bl);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px}
h1{font-size:26px;font-weight:700;letter-spacing:-.02em}
.sub{color:var(--t2);font-size:13px;margin-bottom:28px}
.sec{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--t3);margin:34px 0 14px}
.grid{display:grid;gap:14px}
.g4{grid-template-columns:repeat(4,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
@media(max-width:900px){.g4,.g3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.g4,.g3,.g2{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:18px}
.k-lbl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--t3);margin-bottom:8px}
.k-val{font-size:25px;font-weight:700;letter-spacing:-.02em;line-height:1.1}
.k-sub{font-size:12px;color:var(--t2);margin-top:6px}
.hero{background:var(--bl);color:#fff;border:none}
.hero .k-lbl{color:rgba(255,255,255,.7)}
.hero .k-sub{color:rgba(255,255,255,.85)}
.bar{height:9px;background:#ededf0;border-radius:5px;overflow:hidden;margin:10px 0 6px}
.bar.dark{background:rgba(255,255,255,.25)}
.bar>div{height:100%;border-radius:5px;transition:width .4s}
.dual .row{display:flex;justify-content:space-between;align-items:baseline;font-size:13px;margin-top:4px}
.dual .row b{font-size:18px;font-weight:700}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--bd);border-radius:14px;overflow:hidden}
th,td{text-align:left;padding:12px 16px;font-size:13.5px;border-bottom:1px solid var(--bd)}
th{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--t3);background:#fafafc}
tr:last-child td{border-bottom:none}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.role{font-size:11px;color:var(--t2)}
.minibar{height:7px;background:#ededf0;border-radius:4px;overflow:hidden;min-width:90px}
.minibar>div{height:100%}
.empty{color:var(--t3);font-size:14px;padding:16px;background:var(--card);border:1px dashed var(--bd);border-radius:14px}
.note{font-size:12px;color:var(--t2);margin:6px 0 0}
.foot{margin-top:40px;font-size:11px;color:var(--t3);text-align:center}
"""


def barra(pct, cor=None):
    cor = cor or cor_pct(pct)
    return f'<div class="minibar"><div style="width:{min(pct,100):.0f}%;background:{cor}"></div></div>'


# ─────────────────────────────────────────────────────────────────────────────
# GERADOR DO index.html (DASHBOARD KPIs — design novo, tema claro)
# Injeta os dados ao vivo no template index_template.html.
# ─────────────────────────────────────────────────────────────────────────────

# Estoque (apurado das planilhas de vendas — número de unidades e valor das disponíveis).
# Atualize quando lançar/vender unidades. Valor = soma das unidades DISPONÍVEIS.
ESTOQUE = {
    "total": 200,
    "disponivelQtd": 44,
    "disponivelValor": 46976275.59,
    "porEmpreendimento": [
        {"nome": "Laguna Sky Garden",    "total": 75, "disp": 15, "valor": 26099057.15},
        {"nome": "Sintropia Sky Garden", "total": 97, "disp": 29, "valor": 20877218.44},
        {"nome": "Residencial Girassol", "total": 20, "disp": 0,  "valor": 0.0},
        {"nome": "Residencial Lótus",    "total": 8,  "disp": 0,  "valor": 0.0},
    ],
}

# Marketing/Conversas — fixos por enquanto. Para deixar ao vivo, passe os
# resultados de buscar_marketing()/buscar_conversas() do dashboard_api.py.
CONVERSAS_TOTAL = 6681

# Conversões e previsibilidade (vêm do dashboard de marketing/funil — edite ou ligue ao vivo)
CONVERSOES = {
    "leadAgend": 0.5, "agendVenda": 34.4, "leadVenda": 0.17,
    "agendamentos": 32, "vendas": 11,
}
PREVISIBILIDADE = {"leadsPorVenda": 609, "vendasMes": 0.9, "receitaMes": 952508}


def gerar_index_kpis(hoje, vgv_mes, ent_mes, pipe_total, pipe_pond,
                     abertos, ganhos, perdidos, n_ganho, n_perda, win_rate,
                     ciclo_medio, corretores, etapas_ord, motivos_ord,
                     campanhas=None, atendentes=None):
    """Monta o DADOS e grava o index.html a partir do index_template.html."""
    import json

    if not os.path.exists(KPIS_TEMPLATE):
        print(f"AVISO: {KPIS_TEMPLATE} não encontrado — index.html não gerado.")
        return None

    # Ticket médio = receita fechada total / nº de ganhos
    total_ganho = sum(d.get("value", 0) for d in ganhos)
    ticket = (total_ganho / n_ganho) if n_ganho else 0.0

    # Corretores (ordenado por VGV no mês)
    corretores_fmt = []
    for kw, m in corretores:
        corretores_fmt.append({
            "nome": m.get("nome", ""), "cargo": m.get("papel", ""),
            "vgv": round(m.get("vgv_mes", 0), 2), "meta": round(META_VGV_PESSOA, 2),
            "previsao": round(m.get("pipe_pond", 0), 2),
        })
    corretores_fmt.sort(key=lambda c: c["vgv"], reverse=True)

    # Etapas do pipeline ponderado
    etapas_fmt = [{
        "nome": etapa, "peso": round(v["peso"]), "qtd": v["n"],
        "bruto": round(v["valor"], 2), "pond": round(v["pond"], 2),
    } for etapa, v in etapas_ord]

    # Motivos de perda
    tot_perda = sum(v["n"] for _, v in motivos_ord) or 1
    motivos_fmt = [{
        "motivo": motivo, "qtd": v["n"],
        "pct": round(v["n"] / tot_perda * 100), "valor": round(v["valor"], 2),
    } for motivo, v in motivos_ord[:12]]

    # Pipeline executivo (qtd por etapa + fechamento)
    pipeline_exec = [{"nome": e["nome"], "qtd": e["qtd"]} for e in etapas_fmt]
    pipeline_exec.append({"nome": "Fechamento", "qtd": n_ganho})

    carimbo = hoje.strftime("%d/%m/%Y às %H:%M")
    dados = {
        "buscadoEm": carimbo, "atualizadoEm": carimbo,
        "dataFiltro": hoje.strftime("%d/%m/%Y"),

        "metaVGV": round(META_MACRO_VGV, 2), "metaEntrada": round(META_MACRO_ENT, 2),
        "realizadoVGV": round(vgv_mes, 2), "realizadoEntrada": round(ent_mes, 2),

        "receitaFechada": round(vgv_mes, 2),
        "pipelineAtivo": round(pipe_total, 2),
        "previsaoPonderada": round(pipe_pond, 2),
        "negociacoesAtivas": len(abertos),
        "leadsMarketing": LEADS_MARKETING, "leadsCRM": LEADS_CRM,
        "conversasTotal": CONVERSAS_TOTAL,
        "ticketMedio": round(ticket, 2),

        "winRate": round(win_rate, 2), "ganhos": n_ganho, "perdidos": n_perda,
        "cicloDias": ciclo_medio,

        "conversoes": CONVERSOES,
        "previsibilidade": PREVISIBILIDADE,
        "pipelineExecutivo": pipeline_exec,

        "estoque": ESTOQUE,
        "corretores": corretores_fmt,
        "etapas": etapas_fmt,
        "motivos": motivos_fmt,
        "campanhas": campanhas or [],
        "atendentes": atendentes or [],
    }

    template = open(KPIS_TEMPLATE, encoding="utf-8").read()
    if "__DADOS_JSON__" not in template:
        print("AVISO: index_template.html sem o marcador __DADOS_JSON__.")
        return None

    html = template.replace("__DADOS_JSON__", json.dumps(dados, ensure_ascii=False))
    with open(KPIS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {KPIS_OUTPUT} gerado com dados ao vivo do RD ({len(html)} bytes)")
    return KPIS_OUTPUT


# ─────────────────────────────────────────────────────────────────────────────
# GERADOR DO HTML
# ─────────────────────────────────────────────────────────────────────────────

def gerar_dashboard(deals, cfg):
    pesos = cfg["pesos"]
    limite_parado = cfg["dias_parado"]
    realizado_entrada = cfg.get("realizado_entrada", {})
    transicao = cfg.get("transicao", {}) or {}

    hoje = datetime.now()
    mes_tag = hoje.strftime("%Y-%m")
    dias_no_mes = calendar.monthrange(hoje.year, hoje.month)[1]
    dia_atual = hoje.day

    abertos = [d for d in deals if classificar(d["stage"]) == "aberto"]
    ganhos = [d for d in deals if classificar(d["stage"]) == "ganho"]
    perdidos = [d for d in deals if classificar(d["stage"]) == "perdido"]

    # Regra de transição: no mês configurado, só contam os negócios listados.
    em_transicao = transicao.get("mes") == mes_tag
    nomes_ok = [str(x).lower() for x in transicao.get("negocios_que_contam", [])]

    def conta_no_mes(d):
        if not (d["closed_at"] or "").startswith(mes_tag):
            return False
        if em_transicao:
            nome = (d.get("nome") or "").lower()
            return any(kw in nome for kw in nomes_ok)
        return True

    ganhos_mes = [d for d in ganhos if conta_no_mes(d)]

    # ── Pipeline ponderado por etapa ──────────────────────────────────────
    pipe_total = sum(d["value"] for d in abertos)
    por_etapa = defaultdict(lambda: {"valor": 0.0, "pond": 0.0, "n": 0, "peso": 0})
    for d in abertos:
        w = peso_da_etapa(d["stage"], pesos)
        por_etapa[d["stage"]]["valor"] += d["value"]
        por_etapa[d["stage"]]["pond"] += d["value"] * w / 100.0
        por_etapa[d["stage"]]["n"] += 1
        por_etapa[d["stage"]]["peso"] = w
    pipe_pond = sum(v["pond"] for v in por_etapa.values())
    etapas_ord = sorted(por_etapa.items(), key=lambda kv: kv[1]["peso"])

    # ── Win / Loss ────────────────────────────────────────────────────────
    n_ganho, n_perda = len(ganhos), len(perdidos)
    win_rate = (n_ganho / (n_ganho + n_perda) * 100) if (n_ganho + n_perda) else 0

    # ── Ciclo de venda ────────────────────────────────────────────────────
    # Só conta como ciclo "real" negócio criado E fechado depois do mês de
    # transição (datas confiáveis). Senão, usa o valor informado.
    corte = None
    if transicao.get("mes"):
        try:
            y, m = transicao["mes"].split("-")[:2]
            corte = datetime(int(y), int(m), 28).strftime("%Y-%m-%d")
        except Exception:
            corte = None
    ciclos = []
    for d in ganhos:
        if d["created_at"] and d["closed_at"]:
            if corte and (d["created_at"] <= corte or d["closed_at"] <= corte):
                continue
            try:
                c = datetime.strptime(d["created_at"], "%Y-%m-%d").date()
                f = datetime.strptime(d["closed_at"], "%Y-%m-%d").date()
                if (f - c).days >= 0:
                    ciclos.append((f - c).days)
            except Exception:
                pass
    if len(ciclos) >= 5:
        ciclo_medio = round(sum(ciclos) / len(ciclos)); ciclo_fonte = "calculado"
    else:
        ciclo_medio = cfg.get("ciclo_venda_dias", CICLO_VENDA_PADRAO); ciclo_fonte = "informado"

    # ── Pacing macro (VGV + entrada) ──────────────────────────────────────
    vgv_mes = sum(d["value"] for d in ganhos_mes)
    ent_mes = float(realizado_entrada.get(mes_tag, 0))
    pct_vgv = (vgv_mes / META_MACRO_VGV * 100) if META_MACRO_VGV else 0
    pct_ent = (ent_mes / META_MACRO_ENT * 100) if META_MACRO_ENT else 0
    pct_tempo = dia_atual / dias_no_mes * 100

    # ── Equipe: metas por pessoa ──────────────────────────────────────────
    membros = {}
    for papel, nomes in EQUIPE.items():
        for kw in nomes:
            membros[kw] = {"papel": papel, "nome": NOMES_DISPLAY.get(kw, kw.title()),
                           "vgv_mes": 0.0, "pipe_pond": 0.0, "reunioes": 0}
    for d in deals:
        kw, papel = membro_de(d["user"])
        if not kw:
            continue
        cl = classificar(d["stage"])
        if cl == "aberto":
            membros[kw]["pipe_pond"] += d["value"] * peso_da_etapa(d["stage"], pesos) / 100.0
        if cl == "ganho" and conta_no_mes(d):
            membros[kw]["vgv_mes"] += d["value"]
        # Reuniões do mês: negócio criado neste mês que chegou ao atendimento.
        # No mês de transição (cadastro em massa) não conta — começa limpo no mês seguinte.
        if (teve_reuniao(d["stage"]) and not em_transicao
                and (d["created_at"] or "").startswith(mes_tag)):
            membros[kw]["reunioes"] += 1

    corretores = [(kw, m) for kw, m in membros.items() if m["papel"] != "SDR"]
    sdrs = [(kw, m) for kw, m in membros.items() if m["papel"] == "SDR"]

    # ── Motivos de perda ──────────────────────────────────────────────────
    motivos = defaultdict(lambda: {"n": 0, "valor": 0.0})
    for d in perdidos:
        m = d["loss_reason"] or "Não informado"
        motivos[m]["n"] += 1
        motivos[m]["valor"] += d["value"]
    motivos_ord = sorted(motivos.items(), key=lambda kv: kv[1]["n"], reverse=True)

    # ── Negócios parados ──────────────────────────────────────────────────
    parados = []
    for d in abertos:
        dd = dias_desde(d["updated_at"] or d["created_at"])
        if dd is not None and dd > limite_parado:
            parados.append({**d, "dias": dd})
    parados.sort(key=lambda d: d["value"], reverse=True)
    valor_parado = sum(d["value"] for d in parados)

    # ═══════════════════════ MONTAGEM DO HTML ═════════════════════════════
    agora = hoje.strftime("%d/%m/%Y às %H:%M")
    nome_mes = MESES_PT[hoje.month - 1]

    cobertura = (pipe_pond / META_MACRO_VGV * 100) if META_MACRO_VGV else 0
    cor_v, cor_e = cor_pct(pct_vgv), cor_pct(pct_ent)

    topo = f"""
      <div class="card hero">
        <div class="k-lbl">Previsão de fechamento (pipeline ponderado)</div>
        <div class="k-val">{R(pipe_pond)}</div>
        <div class="bar dark"><div style="width:{min(cobertura,100):.0f}%;background:#fff"></div></div>
        <div class="k-sub">{cobertura:.0f}% da meta macro ({R0(META_MACRO_VGV)}) — de {R(pipe_total)} em aberto</div>
      </div>
      <div class="card">
        <div class="k-lbl">Win Rate</div>
        <div class="k-val" style="color:{cor_pct(win_rate)}">{win_rate:.0f}%</div>
        <div class="k-sub">{n_ganho} ganhos / {n_perda} perdidos</div>
      </div>
      <div class="card">
        <div class="k-lbl">Ciclo de venda médio</div>
        <div class="k-val">{ciclo_medio} dias</div>
        <div class="k-sub">{"informado" if ciclo_fonte == "informado" else f"calculado ({len(ciclos)} negócios novos)"}</div>
      </div>
      <div class="card">
        <div class="k-lbl">Negócios em aberto</div>
        <div class="k-val">{len(abertos)}</div>
        <div class="k-sub">{R(pipe_total)} na esteira</div>
      </div>
    """

    pacing = f"""
      <div class="card dual">
        <div class="k-lbl">Ritmo de {nome_mes} — dia {dia_atual} de {dias_no_mes} ({pct_tempo:.0f}% do mês)</div>
        <div class="row"><span>VGV realizado</span><b style="color:{cor_v}">{R(vgv_mes)}</b></div>
        <div class="bar"><div style="width:{min(pct_vgv,100):.1f}%;background:{cor_v}"></div></div>
        <div class="row"><span class="k-sub" style="margin:0">{pct_vgv:.0f}% da meta de {R0(META_MACRO_VGV)}</span></div>
        <div class="row" style="margin-top:14px"><span>Entrada realizada</span><b style="color:{cor_e}">{R(ent_mes)}</b></div>
        <div class="bar"><div style="width:{min(pct_ent,100):.1f}%;background:{cor_e}"></div></div>
        <div class="row"><span class="k-sub" style="margin:0">{pct_ent:.0f}% da meta de {R0(META_MACRO_ENT)}</span></div>
      </div>
    """

    # Tabela: pipeline ponderado por etapa
    if etapas_ord:
        linhas = ""
        max_pond = max((v["pond"] for _, v in etapas_ord), default=1) or 1
        for etapa, v in etapas_ord:
            linhas += f"""<tr>
              <td><strong>{etapa}</strong></td><td class="num">{v['peso']:.0f}%</td>
              <td class="num">{v['n']}</td><td class="num">{R(v['valor'])}</td>
              <td class="num" style="font-weight:700">{R(v['pond'])}</td>
              <td style="width:150px">{barra(v['pond']/max_pond*100,'var(--bl)')}</td>
            </tr>"""
        tab_etapas = f"""<table><thead><tr><th>Etapa</th><th class="num">Peso</th><th class="num">Qtd</th>
          <th class="num">Valor bruto</th><th class="num">Ponderado</th><th>Peso visual</th></tr></thead>
          <tbody>{linhas}</tbody></table>
          <p class="note">Ponderado = valor do negócio × probabilidade da etapa. Ajuste os pesos no config_pipeline.json.</p>"""
    else:
        tab_etapas = '<div class="empty">Nenhum negócio em aberto no momento.</div>'

    # Tabela: corretores e coordenadoras (meta VGV)
    linhas = ""
    for kw, m in sorted(corretores, key=lambda x: x[1]["vgv_mes"], reverse=True):
        pct = (m["vgv_mes"] / META_VGV_PESSOA * 100) if META_VGV_PESSOA else 0
        linhas += f"""<tr>
          <td><strong>{m['nome']}</strong><div class="role">{m['papel']}</div></td>
          <td class="num">{R(m['vgv_mes'])}</td>
          <td class="num">{R0(META_VGV_PESSOA)}</td>
          <td class="num" style="color:{cor_pct(pct)};font-weight:700">{pct:.0f}%</td>
          <td style="width:140px">{barra(pct)}</td>
          <td class="num">{R(m['pipe_pond'])}</td>
        </tr>"""
    tab_corretores = f"""<table><thead><tr><th>Corretor / Coordenadora</th>
      <th class="num">VGV no mês</th><th class="num">Meta</th><th class="num">%</th>
      <th>Progresso</th><th class="num">Previsão (pipeline)</th></tr></thead>
      <tbody>{linhas}</tbody></table>
      <p class="note">VGV no mês = vendas ganhas neste mês. Previsão = pipeline ponderado em aberto da pessoa.</p>"""

    # Tabela: SDRs (meta reuniões)
    linhas = ""
    for kw, m in sorted(sdrs, key=lambda x: x[1]["reunioes"], reverse=True):
        pct = (m["reunioes"] / META_REUNIOES_SDR * 100) if META_REUNIOES_SDR else 0
        linhas += f"""<tr>
          <td><strong>{m['nome']}</strong></td>
          <td class="num">{m['reunioes']}</td>
          <td class="num">{META_REUNIOES_SDR}</td>
          <td class="num" style="color:{cor_pct(pct)};font-weight:700">{pct:.0f}%</td>
          <td style="width:160px">{barra(pct)}</td>
        </tr>"""
    tab_sdrs = f"""<table><thead><tr><th>SDR</th><th class="num">Reuniões realizadas</th>
      <th class="num">Meta</th><th class="num">%</th><th>Progresso</th></tr></thead>
      <tbody>{linhas}</tbody></table>
      <p class="note">Reuniões realizadas no mês = negócios criados neste mês que chegaram à etapa de atendimento (ou além) com o SDR como responsável.</p>"""

    # Tabela: motivos de perda
    if motivos_ord:
        linhas = ""
        tot = sum(m["n"] for _, m in motivos_ord) or 1
        for motivo, m in motivos_ord[:12]:
            linhas += f"""<tr><td>{motivo}</td><td class="num">{m['n']}</td>
              <td class="num">{m['n']/tot*100:.0f}%</td><td class="num">{R(m['valor'])}</td></tr>"""
        tab_perda = f"""<table><thead><tr><th>Motivo da perda</th><th class="num">Qtd</th>
          <th class="num">%</th><th class="num">Valor perdido</th></tr></thead><tbody>{linhas}</tbody></table>
          <p class="note">Aparecem apenas se o motivo for preenchido no RD Station.</p>"""
    else:
        tab_perda = '<div class="empty">Nenhuma perda registrada (ou sem motivo preenchido).</div>'

    # Tabela: negócios parados
    if parados:
        linhas = ""
        for d in parados[:25]:
            cor_d = "var(--rd)" if d["dias"] > 30 else "var(--or)"
            linhas += f"""<tr><td>{d['stage']}</td><td>{d['user']}</td>
              <td class="num">{R(d['value'])}</td>
              <td class="num"><span style="color:{cor_d};font-weight:700">{d['dias']} dias</span></td></tr>"""
        extra = f'<p class="note">Mostrando os 25 maiores de {len(parados)} negócios parados ({R(valor_parado)} no total).</p>' if len(parados) > 25 else ""
        tab_parados = f"""<table><thead><tr><th>Etapa</th><th>Responsável</th>
          <th class="num">Valor</th><th class="num">Parado há</th></tr></thead><tbody>{linhas}</tbody></table>{extra}"""
    else:
        tab_parados = f'<div class="empty">Nenhum negócio parado há mais de {limite_parado} dias.</div>'

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pipeline & Previsibilidade — IM Incorporadora</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="top"><div class="logo">IM</div><h1>Pipeline & Previsibilidade</h1></div>
  <div class="sub">Dados do RD Station CRM — atualizado em {agora}</div>

  <div class="sec">Visão geral</div>
  <div class="grid g4">{topo}</div>

  <div class="sec">Ritmo do mês (pacing)</div>
  <div class="grid">{pacing}</div>

  <div class="sec">Pipeline ponderado por etapa</div>
  {tab_etapas}

  <div class="sec">Metas por corretor e coordenadora</div>
  {tab_corretores}

  <div class="sec">Reuniões por SDR</div>
  {tab_sdrs}

  <div class="grid g2" style="margin-top:8px">
    <div><div class="sec" style="margin-top:18px">Motivos de perda</div>{tab_perda}</div>
    <div><div class="sec" style="margin-top:18px">Negócios em aberto</div>
      <div class="card"><div class="k-lbl">Total na esteira</div>
        <div class="k-val">{R(pipe_total)}</div>
        <div class="k-sub">{len(abertos)} negócios · {R(valor_parado)} parados</div></div></div>
  </div>

  <div class="sec">Negócios parados (sem movimentação há +{limite_parado} dias)</div>
  {tab_parados}

  <div class="foot">Dashboard de pipeline · gerado automaticamente · IM Incorporadora</div>
</div>
</body>
</html>"""

    with open("dashboard_pipeline.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: dashboard_pipeline.html gerado ({len(html)} bytes)")

    # ── Dashboard KPIs (index.html — design novo, publicado no GitHub Pages) ──
    gerar_index_kpis(
        hoje=hoje,
        vgv_mes=vgv_mes,
        ent_mes=ent_mes,
        pipe_total=pipe_total,
        pipe_pond=pipe_pond,
        abertos=abertos,
        ganhos=ganhos,
        perdidos=perdidos,
        n_ganho=n_ganho,
        n_perda=n_perda,
        win_rate=win_rate,
        ciclo_medio=ciclo_medio,
        corretores=corretores,
        etapas_ord=etapas_ord,
        motivos_ord=motivos_ord,
        # Para deixar marketing/conversas ao vivo, passe aqui os resultados
        # de buscar_marketing()["campanhas"] e buscar_conversas_employees():
        campanhas=None,
        atendentes=None,
    )

    return html


if __name__ == "__main__":
    cfg = carregar_config()
    deals = buscar_crm()
    print(f"Total de negocios: {len(deals)}")
    gerar_dashboard(deals, cfg)
    print("Concluido!")
