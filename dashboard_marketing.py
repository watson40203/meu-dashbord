"""
Dashboard Unificado - RD Station (CRM + Marketing + Conversas)
-------------------------------------------------------------------
Busca os dados das 3 plataformas e gera UM dashboard web com:
- Filtro de periodo GLOBAL (afeta todas as abas)
- Visao Geral (KPIs + Metas + Pipeline Executivo)
- Abas detalhadas: CRM, Marketing, Conversas
- Aba de Configuracoes (metas editaveis, salvas no navegador)

COMO USAR:
1. Confira se os tokens abaixo estao corretos
2. Rode: python3 dashboard_unificado.py
3. Abra "dashboard_unificado.html" (duplo clique)
"""

import requests
import json
import base64
import os
from datetime import datetime

LOGO_PATH = "logo.png"


def carregar_logo_base64():
    """Carrega a logo da empresa em base64, se o arquivo existir na mesma pasta."""
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None


# ===================================================
# CONFIGURACAO
# ===================================================
TOKEN_CRM = os.environ.get("TOKEN_CRM", "")

CLIENT_ID_MKT = os.environ.get("CLIENT_ID_MKT", "")
CLIENT_SECRET_MKT = os.environ.get("CLIENT_SECRET_MKT", "")
REFRESH_TOKEN_MKT = os.environ.get("REFRESH_TOKEN_MKT", "")

TOKEN_CONVERSAS = os.environ.get("TOKEN_CONVERSAS", "")

META_VGV_PADRAO = 2095240.14
META_ENTRADA_PADRAO = 255239.40


# ===================================================
# RD CRM - retorna lista BRUTA de negociacoes
# ===================================================
def buscar_crm():
    print("\n=== RD STATION CRM ===")
    todas_negociacoes = []
    pagina = 1
    base_url = "https://crm.rdstation.com/api/v1/deals"

    while True:
        params = {"token": TOKEN_CRM, "page": pagina, "limit": 200}
        resposta = requests.get(base_url, params=params)
        if resposta.status_code != 200:
            print(f"Erro CRM: {resposta.status_code}")
            break
        dados = resposta.json()
        negociacoes = dados.get("deals", [])
        if not negociacoes:
            break
        todas_negociacoes.extend(negociacoes)
        print(f"Pagina {pagina}: {len(negociacoes)} negociacoes")
        if len(negociacoes) < 200:
            break
        pagina += 1

    deals_simples = []
    for n in todas_negociacoes:
        etapa_nome = n.get("deal_stage", {}).get("name", "Sem etapa")
        valor = n.get("amount_total") or 0
        criado_em = n.get("created_at") or ""
        fechado_em = n.get("closed_at") or ""
        deals_simples.append({
            "stage": etapa_nome,
            "value": valor,
            "created_at": str(criado_em)[:10],
            "closed_at": str(fechado_em)[:10] if fechado_em else None,
        })

    return deals_simples


# ===================================================
# RD MARKETING - retorna lista BRUTA de contatos
# ===================================================
def buscar_marketing():
    print("\n=== RD STATION MARKETING ===")
    auth_url = "https://api.rd.services/auth/token"
    payload = {
        "client_id": CLIENT_ID_MKT,
        "client_secret": CLIENT_SECRET_MKT,
        "refresh_token": REFRESH_TOKEN_MKT
    }
    resposta = requests.post(auth_url, json=payload)
    if resposta.status_code != 200:
        print("Erro ao gerar access_token do Marketing:", resposta.status_code)
        return {"contatos": [], "erro": True}

    access_token = resposta.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    contacts_url = "https://api.rd.services/platform/contacts"

    todos_contatos = []
    pagina = 1

    while True:
        params = {"page[number]": pagina, "page[size]": 125}
        resposta = requests.get(contacts_url, headers=headers, params=params)
        if resposta.status_code != 200:
            print(f"Erro Marketing: {resposta.status_code}")
            break
        dados = resposta.json()
        contatos = dados.get("data", [])
        if not contatos:
            break
        todos_contatos.extend(contatos)
        print(f"Pagina {pagina}: {len(contatos)} contatos")
        if len(contatos) < 125:
            break
        pagina += 1

    contatos_simples = []
    for c in todos_contatos:
        estagio = c.get("lifecycle_stage", "Sem estagio") or "Sem estagio"
        criado_em = c.get("created_at") or ""
        contatos_simples.append({
            "stage": estagio,
            "created_at": str(criado_em)[:10],
        })

    return {"contatos": contatos_simples, "erro": len(todos_contatos) == 0}


# ===================================================
# RD CONVERSAS - retorna lista BRUTA de contatos
# ===================================================
def buscar_conversas():
    print("\n=== RD STATION CONVERSAS ===")
    base_url = "https://api.tallos.com.br/v2/customers"
    headers = {"Authorization": f"Bearer {TOKEN_CONVERSAS}"}

    todos_contatos = []
    pagina = 1

    while True:
        params = {"page": pagina, "limit": 100}
        resposta = requests.get(base_url, headers=headers, params=params)
        if resposta.status_code != 200:
            print(f"Erro Conversas: {resposta.status_code}")
            break
        dados = resposta.json()
        contatos = dados.get("data", dados) if isinstance(dados, dict) else dados
        if not contatos:
            break
        todos_contatos.extend(contatos)
        print(f"Pagina {pagina}: {len(contatos)} contatos")
        if len(contatos) < 100:
            break
        pagina += 1

    contatos_simples = []
    tem_data = False
    for c in todos_contatos:
        criado_em = c.get("created_at") or c.get("createdAt") or c.get("registered_at") or ""
        if criado_em:
            tem_data = True
        contatos_simples.append({
            "created_at": str(criado_em)[:10] if criado_em else None,
        })

    return {"contatos": contatos_simples, "tem_data": tem_data}


# ===================================================
# GERAR O DASHBOARD HTML
# ===================================================
def gerar_dashboard(crm_deals, mkt_data, conv_data):
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    mkt_aviso = "<p style='color:#fb923c'>⚠️ Não foi possível buscar os dados agora (instabilidade no servidor do RD Station). Rode o script de novo mais tarde.</p>" if mkt_data.get("erro") else ""
    conv_aviso = "" if conv_data.get("tem_data") else "<p style='color:#94a3b8; font-size:13px;'>⚠️ O filtro de período ainda não funciona para Conversas (a API não retornou um campo de data identificável). O total mostrado é sempre geral.</p>"

    logo_b64 = carregar_logo_base64()
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Logo">'
    else:
        logo_html = '<span class="navbar-logo-texto">🧭 RD Dashboard</span>'

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Dashboard RD Station - Visão Geral</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
    * {{ box-sizing: border-box; }}
    body {{ font-family: -apple-system, Arial, sans-serif; background: #0f1729; color: #e2e8f0; margin: 0; padding: 0; }}
    .conteudo {{ padding: 24px 40px; }}

    .navbar {{ display: flex; align-items: center; justify-content: space-between; background: #161f30; border-bottom: 1px solid #2a3650; padding: 10px 28px; position: relative; }}
    .navbar-logo img {{ height: 34px; display: block; }}
    .navbar-logo-texto {{ font-weight: 700; font-size: 16px; color: #e2e8f0; }}
    .navbar-icones {{ display: flex; align-items: center; gap: 6px; }}
    .navbar-icone {{ width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; border-radius: 10px; font-size: 19px; cursor: pointer; color: #94a3b8; position: relative; }}
    .navbar-icone:hover {{ background: #1e293b; }}
    .navbar-icone.ativo {{ background: #1e293b; color: #38bdf8; }}
    .navbar-icone .tooltip {{ position: absolute; top: 50px; left: 50%; transform: translateX(-50%); background: #0f1729; border: 1px solid #2a3650; color: #e2e8f0; font-size: 11px; padding: 4px 9px; border-radius: 6px; white-space: nowrap; opacity: 0; pointer-events: none; transition: opacity 0.15s; z-index: 20; }}
    .navbar-icone:hover .tooltip {{ opacity: 1; }}

    .painel-periodo {{ position: absolute; top: 56px; right: 28px; background: #161f30; border: 1px solid #2a3650; border-radius: 12px; padding: 16px 18px; display: none; gap: 10px; align-items: center; flex-wrap: wrap; z-index: 30; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }}
    .painel-periodo.aberto {{ display: flex; }}
    .painel-periodo label {{ font-size: 13px; color: #94a3b8; }}
    .painel-periodo select, .painel-periodo input[type="date"] {{ background: #0f1729; border: 1px solid #2a3650; color: #e2e8f0; padding: 8px 12px; border-radius: 8px; font-size: 13px; }}
    #datas-personalizadas {{ display: none; gap: 10px; align-items: center; }}

    .atualizado {{ color: #94a3b8; font-size: 13px; margin: 16px 0 20px 0; }}

    .pagina {{ display: none; }}
    .pagina.ativa {{ display: block; }}

    .cards {{ display: flex; gap: 20px; margin-bottom: 35px; flex-wrap: wrap; }}
    .card {{ background: linear-gradient(135deg, #1e293b, #161f30); border-radius: 14px; padding: 22px 28px; min-width: 200px; border: 1px solid #2a3650; }}
    .card .numero {{ font-size: 30px; font-weight: 700; }}
    .card .label {{ color: #94a3b8; font-size: 13px; margin-top: 6px; }}

    .cards-geral {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 10px; }}
    .card-geral {{ background: linear-gradient(135deg, #1e293b, #161f30); border-radius: 14px; padding: 26px 28px; border: 1px solid #2a3650; border-top: 4px solid; }}
    .card-geral-titulo {{ font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 14px; }}
    .card-geral .numero {{ font-size: 30px; font-weight: 700; }}
    .card-geral .label {{ color: #94a3b8; font-size: 13px; margin-top: 4px; }}
    @media (max-width: 900px) {{ .cards-geral {{ grid-template-columns: 1fr; }} }}

    .titulo-secao {{ font-size: 15px; color: #cbd5e1; margin: 30px 0 14px 0; text-transform: uppercase; letter-spacing: 0.05em; }}
    .kpis-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
    .kpi-card {{ background: #161f30; border: 1px solid #2a3650; border-radius: 12px; padding: 18px 20px; }}
    .kpi-label {{ color: #94a3b8; font-size: 12px; margin-bottom: 8px; }}
    .kpi-valor {{ font-size: 22px; font-weight: 700; }}
    @media (max-width: 900px) {{ .kpis-grid {{ grid-template-columns: 1fr; }} }}

    .metas-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .meta-card {{ background: #161f30; border: 1px solid #2a3650; border-radius: 12px; padding: 20px 22px; }}
    .meta-titulo {{ font-size: 13px; color: #cbd5e1; margin-bottom: 10px; font-weight: 600; }}
    .meta-valores {{ display: flex; align-items: baseline; gap: 8px; margin-bottom: 10px; }}
    .meta-realizado {{ font-size: 22px; font-weight: 700; color: #e2e8f0; }}
    .meta-de {{ font-size: 13px; color: #94a3b8; }}
    .barra-fundo {{ background: #2a3650; border-radius: 8px; height: 10px; overflow: hidden; margin-bottom: 8px; }}
    .barra-progresso {{ height: 100%; border-radius: 8px; transition: width 0.3s; }}
    .meta-percentual {{ font-size: 12px; color: #94a3b8; }}
    @media (max-width: 900px) {{ .metas-grid {{ grid-template-columns: 1fr; }} }}

    .graficos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    .painel {{ background: #161f30; border: 1px solid #2a3650; border-radius: 14px; padding: 24px; }}
    .painel h2 {{ font-size: 16px; margin-top: 0; margin-bottom: 16px; color: #cbd5e1; }}
    @media (max-width: 900px) {{ .graficos {{ grid-template-columns: 1fr; }} }}

    .config-input {{ width:100%; padding:10px 12px; border-radius:8px; border:1px solid #2a3650; background:#0f1729; color:#e2e8f0; margin-bottom:18px; font-size:15px; }}
    .config-label {{ display:block; font-size:13px; color:#cbd5e1; margin-bottom:6px; }}
    .config-botao {{ background:#38bdf8; color:#0f1729; font-weight:700; border:none; padding:12px 24px; border-radius:8px; cursor:pointer; font-size:14px; }}
</style>
</head>
<body>

<div class="navbar">
    <div class="navbar-logo">
        {logo_html}
    </div>
    <div class="navbar-icones">
        <div class="navbar-icone ativo" onclick="mudarAba('geral', this)">🧭<span class="tooltip">Visão Geral</span></div>
        <div class="navbar-icone" onclick="mudarAba('crm', this)">📊<span class="tooltip">CRM</span></div>
        <div class="navbar-icone" onclick="mudarAba('mkt', this)">📈<span class="tooltip">Marketing</span></div>
        <div class="navbar-icone" onclick="mudarAba('conv', this)">💬<span class="tooltip">Conversas</span></div>
        <div class="navbar-icone" onclick="togglePainelPeriodo()">📅<span class="tooltip">Período</span></div>
        <div class="navbar-icone" onclick="mudarAba('config', this)">⚙️<span class="tooltip">Configurações</span></div>
    </div>

    <div class="painel-periodo" id="painel-periodo">
        <label>Período:</label>
        <select id="select-periodo" onchange="mudarPeriodo()">
            <option value="tudo">Tudo (histórico completo)</option>
            <option value="este_mes">Este mês</option>
            <option value="mes_passado">Mês passado</option>
            <option value="30dias">Últimos 30 dias</option>
            <option value="este_ano">Este ano</option>
            <option value="personalizado">Personalizado...</option>
        </select>
        <div id="datas-personalizadas">
            <label>De</label>
            <input type="date" id="data-inicio" onchange="aplicarFiltro()">
            <label>até</label>
            <input type="date" id="data-fim" onchange="aplicarFiltro()">
        </div>
    </div>
</div>

<div class="conteudo">
<div class="atualizado">Dados buscados em {agora}</div>

<!-- ===================== VISAO GERAL ===================== -->
<div id="pagina-geral" class="pagina ativa">
    <h2 class="titulo-secao">KPIs Principais (no período)</h2>
    <div class="kpis-grid">
        <div class="kpi-card"><div class="kpi-label">Receita Fechada</div><div class="kpi-valor" id="kpi-receita-fechada" style="color:#34d399">—</div></div>
        <div class="kpi-card"><div class="kpi-label">Pipeline Total (ativo, no período)</div><div class="kpi-valor" id="kpi-pipeline" style="color:#38bdf8">—</div></div>
        <div class="kpi-card"><div class="kpi-label">Negociações Ativas</div><div class="kpi-valor" id="kpi-ativas" style="color:#38bdf8">—</div></div>
        <div class="kpi-card"><div class="kpi-label">Leads Gerados</div><div class="kpi-valor" id="kpi-leads" style="color:#fb923c">—</div></div>
        <div class="kpi-card"><div class="kpi-label">Conversão Geral (Lead → Venda)</div><div class="kpi-valor" id="kpi-conversao" style="color:#a78bfa">—</div></div>
        <div class="kpi-card"><div class="kpi-label">Ticket Médio</div><div class="kpi-valor" id="kpi-ticket" style="color:#facc15">—</div></div>
    </div>

    <h2 class="titulo-secao">Metas do Período</h2>
    <div class="metas-grid">
        <div class="meta-card">
            <div class="meta-titulo">Meta de Fechamento (VGV)</div>
            <div class="meta-valores">
                <span class="meta-realizado" id="vgv-realizado">—</span>
                <span class="meta-de" id="vgv-de">—</span>
            </div>
            <div class="barra-fundo"><div class="barra-progresso" id="vgv-barra" style="width:0%; background:#34d399;"></div></div>
            <div class="meta-percentual" id="vgv-percentual">—</div>
        </div>
        <div class="meta-card">
            <div class="meta-titulo">Meta de Entrada</div>
            <div class="meta-valores">
                <span class="meta-realizado" id="entrada-realizado">—</span>
                <span class="meta-de" id="entrada-de">—</span>
            </div>
            <div class="barra-fundo"><div class="barra-progresso" id="entrada-barra" style="width:0%; background:#facc15;"></div></div>
            <div class="meta-percentual" id="entrada-percentual">—</div>
        </div>
    </div>

    <h2 class="titulo-secao">Pipeline Executivo (no período)</h2>
    <div class="painel">
        <canvas id="graficoFunil"></canvas>
    </div>

    <h2 class="titulo-secao">Resumo por módulo (no período)</h2>
    <div class="cards-geral">
        <div class="card-geral" style="border-color:#38bdf8">
            <div class="card-geral-titulo">📊 CRM</div>
            <div class="numero" id="resumo-crm-total" style="color:#38bdf8">—</div>
            <div class="label">Negociações no período</div>
        </div>
        <div class="card-geral" style="border-color:#fb923c">
            <div class="card-geral-titulo">📈 Marketing</div>
            <div class="numero" id="resumo-mkt-total" style="color:#fb923c">—</div>
            <div class="label">Contatos / Leads no período</div>
        </div>
        <div class="card-geral" style="border-color:#34d399">
            <div class="card-geral-titulo">💬 Conversas</div>
            <div class="numero" id="resumo-conv-total" style="color:#34d399">—</div>
            <div class="label">Contatos totais</div>
        </div>
    </div>
</div>

<!-- ===================== CRM ===================== -->
<div id="pagina-crm" class="pagina">
    <div class="cards">
        <div class="card"><div class="numero" id="crm-total" style="color:#38bdf8">—</div><div class="label">Negociações no período</div></div>
        <div class="card"><div class="numero" id="crm-valor" style="color:#38bdf8">—</div><div class="label">Valor total no período</div></div>
    </div>
    <div class="graficos">
        <div class="painel"><h2>Negociações por etapa</h2><canvas id="graficoCrmEtapas"></canvas></div>
        <div class="painel"><h2>Valor (R$) por etapa</h2><canvas id="graficoCrmValor"></canvas></div>
    </div>
</div>

<!-- ===================== MARKETING ===================== -->
<div id="pagina-mkt" class="pagina">
    {mkt_aviso}
    <div class="cards">
        <div class="card"><div class="numero" id="mkt-total" style="color:#fb923c">—</div><div class="label">Contatos / Leads no período</div></div>
    </div>
    <div class="graficos">
        <div class="painel"><h2>Contatos por estágio do ciclo de vida</h2><canvas id="graficoMktEstagio"></canvas></div>
    </div>
</div>

<!-- ===================== CONVERSAS ===================== -->
<div id="pagina-conv" class="pagina">
    {conv_aviso}
    <div class="cards">
        <div class="card"><div class="numero" id="conv-total" style="color:#34d399">—</div><div class="label">Contatos</div></div>
    </div>
</div>

<!-- ===================== CONFIGURACOES ===================== -->
<div id="pagina-config" class="pagina">
    <div class="painel" style="max-width: 500px;">
        <h2>Metas (editáveis)</h2>
        <p style="color:#94a3b8; font-size: 13px; margin-bottom: 20px;">
            Os valores ficam guardados neste navegador e continuam aqui mesmo depois de rodar o script de novo.
        </p>

        <label class="config-label">Meta de Fechamento (VGV) — R$</label>
        <input type="number" id="input-meta-vgv" step="0.01" class="config-input">

        <label class="config-label">Meta de Entrada — R$</label>
        <input type="number" id="input-meta-entrada" step="0.01" class="config-input">

        <label class="config-label">Entrada Realizada (no período) — R$</label>
        <input type="number" id="input-entrada-realizado" step="0.01" class="config-input">

        <button onclick="salvarConfiguracoes()" class="config-botao">Salvar</button>
        <span id="confirmacao-salvar" style="margin-left:14px; color:#34d399; font-size:13px; display:none;">✅ Salvo!</span>
    </div>
</div>

<script>
// ===================== DADOS BRUTOS (vindos do Python) =====================
const CRM_DEALS = {json.dumps(crm_deals)};
const MKT_CONTATOS = {json.dumps(mkt_data['contatos'])};
const CONV_CONTATOS = {json.dumps(conv_data['contatos'])};

const META_VGV_PADRAO = {META_VGV_PADRAO};
const META_ENTRADA_PADRAO = {META_ENTRADA_PADRAO};

const ORDEM_PRIORIDADE = ["LEADS", "EM CONTATO", "AGENDAMENTO", "ATENDIMENTO REALIZADO", "NEGOCIAÇÃO", "FECHAMENTO"];

let chartFunil, chartCrmEtapas, chartCrmValor, chartMktEstagio;

// ===================== NAVEGACAO DE ABAS =====================
function mudarAba(id, elemento) {{
    document.querySelectorAll('.pagina').forEach(p => p.classList.remove('ativa'));
    document.querySelectorAll('.navbar-icone').forEach(a => a.classList.remove('ativo'));
    document.getElementById('pagina-' + id).classList.add('ativa');
    elemento.classList.add('ativo');
    document.getElementById('painel-periodo').classList.remove('aberto');
}}

function togglePainelPeriodo() {{
    document.getElementById('painel-periodo').classList.toggle('aberto');
}}

document.addEventListener('click', function(event) {{
    const painel = document.getElementById('painel-periodo');
    const dentro = painel.contains(event.target);
    const noIconeCalendario = event.target.closest('.navbar-icone') && event.target.closest('.navbar-icone').textContent.includes('📅');
    if (!dentro && !noIconeCalendario) {{
        painel.classList.remove('aberto');
    }}
}});

// ===================== FILTRO DE PERIODO =====================
function mudarPeriodo() {{
    const valor = document.getElementById('select-periodo').value;
    document.getElementById('datas-personalizadas').style.display = (valor === 'personalizado') ? 'flex' : 'none';
    if (valor !== 'personalizado') {{
        aplicarFiltro();
    }}
}}

function calcularIntervalo() {{
    const preset = document.getElementById('select-periodo').value;
    const hoje = new Date();
    let inicio = null, fim = null;

    if (preset === 'tudo') {{
        return {{ inicio: null, fim: null }};
    }} else if (preset === 'este_mes') {{
        inicio = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
        fim = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0);
    }} else if (preset === 'mes_passado') {{
        inicio = new Date(hoje.getFullYear(), hoje.getMonth() - 1, 1);
        fim = new Date(hoje.getFullYear(), hoje.getMonth(), 0);
    }} else if (preset === '30dias') {{
        fim = hoje;
        inicio = new Date();
        inicio.setDate(hoje.getDate() - 30);
    }} else if (preset === 'este_ano') {{
        inicio = new Date(hoje.getFullYear(), 0, 1);
        fim = new Date(hoje.getFullYear(), 11, 31);
    }} else if (preset === 'personalizado') {{
        const di = document.getElementById('data-inicio').value;
        const dfi = document.getElementById('data-fim').value;
        inicio = di ? new Date(di) : null;
        fim = dfi ? new Date(dfi) : null;
    }}

    return {{ inicio, fim }};
}}

function dataDentroDoIntervalo(dataStr, inicio, fim) {{
    if (!dataStr) return false;
    if (!inicio && !fim) return true;
    const d = new Date(dataStr);
    if (inicio && d < inicio) return false;
    if (fim && d > fim) return false;
    return true;
}}

function formatarReal(valor) {{
    return 'R$ ' + valor.toLocaleString('pt-BR', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
}}

function chaveOrdenacao(etapa) {{
    const nome = etapa.toUpperCase();
    for (let i = 0; i < ORDEM_PRIORIDADE.length; i++) {{
        if (nome.includes(ORDEM_PRIORIDADE[i])) return i;
    }}
    return ORDEM_PRIORIDADE.length + 1;
}}

function obterMetasSalvas() {{
    const vgv = parseFloat(localStorage.getItem('meta_vgv')) || META_VGV_PADRAO;
    const entrada = parseFloat(localStorage.getItem('meta_entrada')) || META_ENTRADA_PADRAO;
    const entradaRealizado = parseFloat(localStorage.getItem('entrada_realizado')) || 0;
    return {{ vgv, entrada, entradaRealizado }};
}}

function salvarConfiguracoes() {{
    const vgv = parseFloat(document.getElementById('input-meta-vgv').value);
    const entrada = parseFloat(document.getElementById('input-meta-entrada').value);
    const entradaRealizado = parseFloat(document.getElementById('input-entrada-realizado').value);

    if (!isNaN(vgv)) localStorage.setItem('meta_vgv', vgv);
    if (!isNaN(entrada)) localStorage.setItem('meta_entrada', entrada);
    if (!isNaN(entradaRealizado)) localStorage.setItem('entrada_realizado', entradaRealizado);

    aplicarFiltro();

    const confirmacao = document.getElementById('confirmacao-salvar');
    confirmacao.style.display = 'inline';
    setTimeout(() => {{ confirmacao.style.display = 'none'; }}, 2500);
}}

// ===================== FUNCAO PRINCIPAL: recalcula tudo =====================
function aplicarFiltro() {{
    const {{ inicio, fim }} = calcularIntervalo();

    // ---------- CRM ----------
    const dealsFiltrados = CRM_DEALS.filter(d => dataDentroDoIntervalo(d.created_at, inicio, fim));

    let negociacoesAtivas = 0, pipelineAtivoValor = 0, receitaFechada = 0, vendasQtd = 0;
    const porEtapa = {{}};
    const valorPorEtapa = {{}};

    dealsFiltrados.forEach(d => {{
        const etapaUpper = d.stage.toUpperCase();
        const ganha = etapaUpper.includes('FECHA');
        const perdida = etapaUpper.includes('PERDID');

        porEtapa[d.stage] = (porEtapa[d.stage] || 0) + 1;
        valorPorEtapa[d.stage] = (valorPorEtapa[d.stage] || 0) + d.value;

        if (ganha) {{
            vendasQtd++;
            receitaFechada += d.value;
        }} else if (!perdida) {{
            negociacoesAtivas++;
            pipelineAtivoValor += d.value;
        }}
    }});

    const ticketMedio = vendasQtd > 0 ? (receitaFechada / vendasQtd) : 0;

    const etapasFunil = Object.keys(porEtapa).filter(e => !e.toUpperCase().includes('PERDID'));
    etapasFunil.sort((a, b) => chaveOrdenacao(a) - chaveOrdenacao(b));
    const funilQtd = etapasFunil.map(e => porEtapa[e]);
    const funilValor = etapasFunil.map(e => valorPorEtapa[e]);
    const primeiraQtd = funilQtd.length > 0 ? funilQtd[0] : 1;
    const funilConversao = funilQtd.map(q => primeiraQtd ? Math.round((q / primeiraQtd) * 1000) / 10 : 0);

    // ---------- MARKETING ----------
    const mktFiltrados = MKT_CONTATOS.filter(c => dataDentroDoIntervalo(c.created_at, inicio, fim));
    const mktPorEstagio = {{}};
    mktFiltrados.forEach(c => {{ mktPorEstagio[c.stage] = (mktPorEstagio[c.stage] || 0) + 1; }});
    const mktEstagioLabels = Object.keys(mktPorEstagio).sort((a,b) => mktPorEstagio[b]-mktPorEstagio[a]);
    const mktEstagioValores = mktEstagioLabels.map(e => mktPorEstagio[e]);

    // ---------- CONVERSAS ----------
    // Se nao ha campo de data confiavel, mostra sempre o total geral
    const temDataConv = CONV_CONTATOS.some(c => c.created_at);
    const convTotal = temDataConv
        ? CONV_CONTATOS.filter(c => dataDentroDoIntervalo(c.created_at, inicio, fim)).length
        : CONV_CONTATOS.length;

    const leadsGerados = mktFiltrados.length + convTotal;
    const conversaoGeral = leadsGerados > 0 ? (vendasQtd / leadsGerados * 100) : 0;

    // ---------- METAS ----------
    const {{ vgv, entrada, entradaRealizado }} = obterMetasSalvas();
    const percentualVgv = Math.min((receitaFechada / vgv) * 100, 100);
    const percentualEntrada = Math.min((entradaRealizado / entrada) * 100, 100);

    // ===================== ATUALIZAR TELA =====================
    document.getElementById('kpi-receita-fechada').textContent = formatarReal(receitaFechada);
    document.getElementById('kpi-pipeline').textContent = formatarReal(pipelineAtivoValor);
    document.getElementById('kpi-ativas').textContent = negociacoesAtivas.toLocaleString('pt-BR');
    document.getElementById('kpi-leads').textContent = leadsGerados.toLocaleString('pt-BR');
    document.getElementById('kpi-conversao').textContent = conversaoGeral.toFixed(2) + '%';
    document.getElementById('kpi-ticket').textContent = formatarReal(ticketMedio);

    document.getElementById('vgv-realizado').textContent = formatarReal(receitaFechada);
    document.getElementById('vgv-de').textContent = 'de ' + formatarReal(vgv);
    document.getElementById('vgv-barra').style.width = percentualVgv.toFixed(1) + '%';
    document.getElementById('vgv-percentual').textContent = percentualVgv.toFixed(1) + '% da meta atingida';

    document.getElementById('entrada-realizado').textContent = formatarReal(entradaRealizado);
    document.getElementById('entrada-de').textContent = 'de ' + formatarReal(entrada);
    document.getElementById('entrada-barra').style.width = percentualEntrada.toFixed(1) + '%';
    document.getElementById('entrada-percentual').textContent = percentualEntrada.toFixed(1) + '% da meta atingida';

    document.getElementById('resumo-crm-total').textContent = dealsFiltrados.length.toLocaleString('pt-BR');
    document.getElementById('resumo-mkt-total').textContent = mktFiltrados.length.toLocaleString('pt-BR');
    document.getElementById('resumo-conv-total').textContent = convTotal.toLocaleString('pt-BR');

    const valorTotalPeriodo = dealsFiltrados.reduce((acc, d) => acc + d.value, 0);
    document.getElementById('crm-total').textContent = dealsFiltrados.length.toLocaleString('pt-BR');
    document.getElementById('crm-valor').textContent = formatarReal(valorTotalPeriodo);

    document.getElementById('mkt-total').textContent = mktFiltrados.length.toLocaleString('pt-BR');
    document.getElementById('conv-total').textContent = convTotal.toLocaleString('pt-BR');

    document.getElementById('input-meta-vgv').value = vgv;
    document.getElementById('input-meta-entrada').value = entrada;
    document.getElementById('input-entrada-realizado').value = entradaRealizado;

    // ===================== GRAFICOS =====================
    const todasEtapasCrm = Object.keys(porEtapa);
    const todosValoresCrm = todasEtapasCrm.map(e => porEtapa[e]);
    const todosValoresRCrm = todasEtapasCrm.map(e => valorPorEtapa[e]);

    atualizarGrafico(chartFunil, etapasFunil, [funilQtd]);
    atualizarGrafico(chartCrmEtapas, todasEtapasCrm, [todosValoresCrm]);
    atualizarGrafico(chartCrmValor, todasEtapasCrm, [todosValoresRCrm]);
    atualizarGrafico(chartMktEstagio, mktEstagioLabels, [mktEstagioValores]);

    chartFunil.options.plugins.tooltip.callbacks.afterLabel = function(context) {{
        const i = context.dataIndex;
        return ['Valor: ' + formatarReal(funilValor[i]), 'Conversão desde o início: ' + funilConversao[i] + '%'];
    }};
    chartFunil.update();
}}

function atualizarGrafico(chart, labels, datasetsValores) {{
    chart.data.labels = labels;
    datasetsValores.forEach((valores, i) => {{ chart.data.datasets[i].data = valores; }});
    chart.update();
}}

// ===================== INICIALIZACAO DOS GRAFICOS =====================
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#2a3650';

chartFunil = new Chart(document.getElementById('graficoFunil'), {{
    type: 'bar',
    data: {{ labels: [], datasets: [{{ label: 'Negociações', data: [], backgroundColor: '#38bdf8' }}] }},
    options: {{
        indexAxis: 'y',
        plugins: {{ legend: {{ display: false }}, tooltip: {{ callbacks: {{}} }} }},
        scales: {{ x: {{ beginAtZero: true }} }}
    }}
}});

chartCrmEtapas = new Chart(document.getElementById('graficoCrmEtapas'), {{
    type: 'bar',
    data: {{ labels: [], datasets: [{{ label: 'Negociações', data: [], backgroundColor: '#38bdf8' }}] }},
    options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
}});

chartCrmValor = new Chart(document.getElementById('graficoCrmValor'), {{
    type: 'doughnut',
    data: {{ labels: [], datasets: [{{ data: [], backgroundColor: ['#38bdf8', '#818cf8', '#f472b6', '#fb923c', '#34d399', '#facc15', '#a78bfa'] }}] }},
    options: {{ plugins: {{ legend: {{ position: 'bottom' }} }} }}
}});

chartMktEstagio = new Chart(document.getElementById('graficoMktEstagio'), {{
    type: 'bar',
    data: {{ labels: [], datasets: [{{ label: 'Contatos', data: [], backgroundColor: '#fb923c' }}] }},
    options: {{ indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
}});

// Primeira renderizacao: periodo "tudo"
aplicarFiltro();
</script>

</div>
</body>
</html>
"""

    with open("dashboard_unificado.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("\n✅ Dashboard unificado gerado! Abra 'dashboard_unificado.html' no navegador.")


if __name__ == "__main__":
    crm_deals = buscar_crm()
    mkt_data = buscar_marketing()
    conv_data = buscar_conversas()

    print(f"\nResumo:")
    print(f"CRM: {len(crm_deals)} negociações")
    print(f"Marketing: {len(mkt_data['contatos'])} contatos")
    print(f"Conversas: {len(conv_data['contatos'])} contatos")

    gerar_dashboard(crm_deals, mkt_data, conv_data)
