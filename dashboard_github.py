"""
Dashboard Unificado - RD Station
Design: Apple Liquid Glass (tema claro, azul)
"""

import requests
import json
import base64
import os
from datetime import datetime

LOGO_PATH = "logo.png"

def carregar_logo_base64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

TOKEN_CRM = os.environ.get("TOKEN_CRM", "")
CLIENT_ID_MKT      = os.environ.get("CLIENT_ID_MKT", "")
CLIENT_SECRET_MKT  = os.environ.get("CLIENT_SECRET_MKT", "")
REFRESH_TOKEN_MKT  = os.environ.get("REFRESH_TOKEN_MKT", "")
TOKEN_PUBLICO_MKT  = os.environ.get("TOKEN_PUBLICO_MKT", "")
TOKEN_PRIVADO_MKT  = os.environ.get("TOKEN_PRIVADO_MKT", "")
TOKEN_CONVERSAS = os.environ.get("TOKEN_CONVERSAS", "")
META_VGV_PADRAO = 2095240.14
META_ENTRADA_PADRAO = 255239.40

# Ícones SVG estilo Apple SF Symbols
ICO_HOME  = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="26" height="26"><path d="M11.47 3.84a.75.75 0 011.06 0l8.69 8.69a.75.75 0 101.06-1.06l-8.689-8.69a2.25 2.25 0 00-3.182 0l-8.69 8.69a.75.75 0 001.061 1.06l8.69-8.69z"/><path d="M12 5.432l8.159 8.159v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 01-.75-.75v-4.5a.75.75 0 00-.75-.75h-3a.75.75 0 00-.75.75V21a.75.75 0 01-.75.75H5.625A1.875 1.875 0 013.75 19.875v-6.198L12 5.432z"/></svg>'
ICO_CRM   = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="26" height="26"><path d="M18.375 2.25c-1.035 0-1.875.84-1.875 1.875v15.75c0 1.035.84 1.875 1.875 1.875h.75c1.035 0 1.875-.84 1.875-1.875V4.125c0-1.036-.84-1.875-1.875-1.875h-.75zM9.75 8.625c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v11.25c0 1.035-.84 1.875-1.875 1.875h-.75a1.875 1.875 0 01-1.875-1.875V8.625zM3 13.125c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v6.75c0 1.035-.84 1.875-1.875 1.875h-.75A1.875 1.875 0 013 19.875v-6.75z"/></svg>'
ICO_MKT   = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="26" height="26"><path fill-rule="evenodd" d="M15.22 6.268a.75.75 0 01.968-.432l5.942 2.28a.75.75 0 01.431.97l-2.28 5.941a.75.75 0 11-1.4-.537l1.63-4.251-1.086.483a15.75 15.75 0 00-6.264 6.064.75.75 0 01-1.299-.72 17.25 17.25 0 016.866-6.637l1.087-.483-4.252-1.63a.75.75 0 01-.432-.968zM1.5 12a.75.75 0 01.75-.75H12a.75.75 0 010 1.5H2.25A.75.75 0 011.5 12z" clip-rule="evenodd"/></svg>'
ICO_CONV  = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="26" height="26"><path d="M4.913 2.658c2.075-.27 4.19-.408 6.337-.408 2.147 0 4.262.139 6.337.408 1.922.25 3.291 1.861 3.405 3.727a4.403 4.403 0 00-1.032-.211 50.89 50.89 0 00-8.42 0c-2.358.196-4.04 2.19-4.04 4.434v4.286a4.47 4.47 0 002.433 3.984L7.28 21.53A.75.75 0 016 21v-4.03a48.527 48.527 0 01-1.087-.128C2.905 16.58 1.5 14.833 1.5 12.862V6.638c0-1.97 1.405-3.718 3.413-3.979z"/><path d="M15.75 7.5c-1.376 0-2.739.057-4.086.169C10.124 7.797 9 9.103 9 10.609v4.285c0 1.507 1.128 2.814 2.67 2.94 1.243.102 2.5.157 3.768.165l2.782 2.781a.75.75 0 001.28-.53v-2.39l.33-.026c1.542-.125 2.67-1.433 2.67-2.94v-4.286c0-1.505-1.125-2.811-2.664-2.94A49.392 49.392 0 0015.75 7.5z"/></svg>'
ICO_CAL   = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="26" height="26"><path d="M12.75 12.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM7.5 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM8.25 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM9.75 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM10.5 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM12 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM12.75 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM14.25 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM15 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM16.5 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM15 12.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM16.5 13.5a.75.75 0 100-1.5.75.75 0 000 1.5z"/><path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 017.5 3v1.5h9V3A.75.75 0 0118 3v1.5h.75a3 3 0 013 3v11.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V7.5a3 3 0 013-3H6V3a.75.75 0 01.75-.75zm13.5 9a1.5 1.5 0 00-1.5-1.5H5.25a1.5 1.5 0 00-1.5 1.5v7.5a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5v-7.5z" clip-rule="evenodd"/></svg>'
ICO_CFG   = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="26" height="26"><path fill-rule="evenodd" d="M11.828 2.25c-.916 0-1.699.663-1.85 1.567l-.091.549a.798.798 0 01-.517.608 7.45 7.45 0 00-.478.198.798.798 0 01-.796-.064l-.453-.324a1.875 1.875 0 00-2.416.2l-.243.243a1.875 1.875 0 00-.2 2.416l.324.453a.798.798 0 01.064.796 7.448 7.448 0 00-.198.478.798.798 0 01-.608.517l-.55.092a1.875 1.875 0 00-1.566 1.849v.344c0 .916.663 1.699 1.567 1.85l.549.091c.281.047.508.25.608.517.06.162.127.321.198.478a.798.798 0 01-.064.796l-.324.453a1.875 1.875 0 00.2 2.416l.243.243c.648.648 1.67.733 2.416.2l.453-.324a.798.798 0 01.796-.064c.157.071.316.137.478.198.267.1.47.327.517.608l.092.55c.15.903.932 1.566 1.849 1.566h.344c.916 0 1.699-.663 1.85-1.567l.091-.549a.798.798 0 01.517-.608 7.52 7.52 0 00.478-.198.798.798 0 01.796.064l.453.324a1.875 1.875 0 002.416-.2l.243-.243c.648-.648.733-1.67.2-2.416l-.324-.453a.798.798 0 01-.064-.796c.071-.157.137-.316.198-.478.1-.267.327-.47.608-.517l.55-.091a1.875 1.875 0 001.566-1.849v-.344c0-.916-.663-1.699-1.567-1.85l-.549-.091a.798.798 0 01-.608-.517 7.507 7.507 0 00-.198-.478.798.798 0 01.064-.796l.324-.453a1.875 1.875 0 00-.2-2.416l-.243-.243a1.875 1.875 0 00-2.416-.2l-.453.324a.798.798 0 01-.796.064 7.462 7.462 0 00-.478-.198.798.798 0 01-.608-.517l-.091-.55a1.875 1.875 0 00-1.849-1.566h-.344zM12 15.75a3.75 3.75 0 100-7.5 3.75 3.75 0 000 7.5z" clip-rule="evenodd"/></svg>'


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
        # Extrai operador/responsável
        u = n.get("user")
        operador = u.get("name", "Sem responsável") if isinstance(u, dict) else "Sem responsável"
        deals_simples.append({
            "stage": etapa_nome,
            "value": valor,
            "created_at": str(criado_em)[:10],
            "closed_at": str(fechado_em)[:10] if fechado_em else None,
            "user": operador,
        })
    return deals_simples


def buscar_marketing():
    print("\n=== RD STATION MARKETING ===")
    try:
        # Gera access_token
        resp = requests.post("https://api.rd.services/auth/token", json={
            "client_id":     CLIENT_ID_MKT,
            "client_secret": CLIENT_SECRET_MKT,
            "refresh_token": REFRESH_TOKEN_MKT,
        }, timeout=15)
        if resp.status_code != 200:
            print(f"Erro ao gerar token: {resp.status_code}")
            return {"contatos": [], "erro": True}

        token = resp.json()["access_token"]
        H = {"Authorization": f"Bearer {token}"}

        # Descobre segmentações
        r = requests.get("https://api.rd.services/platform/segmentations", headers=H, timeout=15)
        if r.status_code != 200:
            print(f"Erro ao buscar segmentações: {r.status_code}")
            return {"contatos": [], "erro": True}

        todas_segs = r.json().get("segmentations", [])
        print(f"Segmentações disponíveis: {len(todas_segs)}")

        # Segmentação principal (todos os contatos)
        seg_todos = next(
            (s for s in todas_segs if "todos os contatos" in s.get("name", "").lower()),
            todas_segs[0] if todas_segs else None
        )
        if not seg_todos:
            print("Segmentação principal não encontrada")
            return {"contatos": [], "erro": True}

        print(f"Usando: '{seg_todos['name']}' (ID {seg_todos['id']})")

        # Mapa de estágios
        ESTAGIOS = {
            "leads qualificados":  "Lead Qualificado",
            "leads (estágio":      "Lead",
            "clientes (estágio":   "Cliente",
            "oportunidades":       "Oportunidade",
            "leads ativos":        "Lead Ativo",
            "leads inativos":      "Lead Inativo",
        }

        def seg_para_estagio(nome):
            n = nome.lower()
            for chave, valor in ESTAGIOS.items():
                if chave in n:
                    return valor
            return None

        # Mapeia UUID → estágio
        uuid_stage = {}
        for seg in todas_segs:
            estagio = seg_para_estagio(seg.get("name", ""))
            if not estagio:
                continue
            url_seg = f"https://api.rd.services/platform/segmentations/{seg['id']}/contacts"
            pag = 1
            while True:
                try:
                    r2 = requests.get(url_seg, headers=H,
                                      params={"page": pag, "per_page": 100}, timeout=20)
                    if r2.status_code != 200:
                        break
                    lote = r2.json().get("contacts", [])
                    if not lote:
                        break
                    for c in lote:
                        uuid_stage[c["uuid"]] = estagio
                    if len(lote) < 100:
                        break
                    pag += 1
                except Exception:
                    break
            qtd = len([v for v in uuid_stage.values() if v == estagio])
            print(f"  '{estagio}': {qtd} contatos")

        # Busca todos os contatos
        url_principal = f"https://api.rd.services/platform/segmentations/{seg_todos['id']}/contacts"
        todos_contatos = []
        pagina = 1
        while True:
            try:
                r3 = requests.get(url_principal, headers=H,
                                  params={"page": pagina, "per_page": 100}, timeout=20)
                if r3.status_code != 200:
                    print(f"Erro página {pagina}: {r3.status_code}")
                    break
                lote = r3.json().get("contacts", [])
                if not lote:
                    break
                todos_contatos.extend(lote)
                print(f"  Página {pagina}: {len(lote)} contatos (total: {len(todos_contatos)})")
                if len(lote) < 100:
                    break
                pagina += 1
            except Exception as e:
                print(f"Erro na página {pagina}: {e}")
                break

        contatos_simples = []
        for c in todos_contatos:
            estagio = uuid_stage.get(c.get("uuid", ""), "Lead")
            criado_em = c.get("created_at") or c.get("last_conversion_date") or ""
            contatos_simples.append({
                "stage":      estagio,
                "created_at": str(criado_em)[:10],
            })

        # ── Campanhas: segmentações customizadas (não são estágios) ──
        IGNORAR = [
            "todos os contatos", "leads qualificados", "leads (estágio",
            "clientes (estágio", "oportunidades", "leads ativos",
            "leads inativos", "[exemplo]",
        ]
        campanhas = {}
        for seg in todas_segs:
            nome = seg.get("name", "")
            if any(ig in nome.lower() for ig in IGNORAR):
                continue
            url_seg = f"https://api.rd.services/platform/segmentations/{seg['id']}/contacts"
            total_camp = 0
            pag = 1
            while True:
                try:
                    rc = requests.get(url_seg, headers=H,
                                      params={"page": pag, "per_page": 100}, timeout=20)
                    if rc.status_code != 200:
                        break
                    lote = rc.json().get("contacts", [])
                    total_camp += len(lote)
                    if len(lote) < 100:
                        break
                    pag += 1
                except Exception:
                    break
            if total_camp > 0:
                campanhas[nome] = total_camp
                print(f"  Campanha '{nome}': {total_camp}")

        print(f"✅ Marketing: {len(contatos_simples)} contatos | {len(campanhas)} campanhas")
        return {"contatos": contatos_simples, "campanhas": campanhas, "erro": len(contatos_simples) == 0}

    except Exception as e:
        print(f"❌ Erro inesperado no Marketing: {e}")
        return {"contatos": [], "erro": True}




def buscar_conversas():
    print("\n=== RD STATION CONVERSAS (contatos) ===")
    base_url = "https://api.tallos.com.br/v2/customers"
    headers = {"Authorization": f"Bearer {TOKEN_CONVERSAS}"}
    todos_contatos = []
    pagina = 1
    while True:
        params = {"page": pagina, "limit": 100}
        resposta = requests.get(base_url, headers=headers, params=params)
        if resposta.status_code != 200:
            print(f"Erro Conversas contatos: {resposta.status_code}")
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
    return len(todos_contatos)


def buscar_conversas_employees():
    """Busca atendentes cadastrados no RD Conversas."""
    print("\n=== RD STATION CONVERSAS (atendentes) ===")
    headers = {"Authorization": f"Bearer {TOKEN_CONVERSAS}"}
    try:
        r = requests.get("https://api.tallos.com.br/v2/employees",
                         headers=headers, params={"limit": 200}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            employees = data if isinstance(data, list) else data.get("data", [])
            print(f"Atendentes encontrados: {len(employees)}")
            return [{"name": e.get("name", ""), "email": e.get("email", "")} for e in employees]
    except Exception as e:
        print(f"Erro ao buscar atendentes: {e}")
    return []


def gerar_dashboard(crm_deals, mkt_data, conv_total, conv_employees):
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    mkt_aviso = "⚠️ Marketing indisponível. Tente novamente em alguns minutos." if mkt_data.get("erro") else ""
    logo_b64 = carregar_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:34px;object-fit:contain;">' if logo_b64 else '<span style="font-weight:800;font-size:18px;color:#1d1d1f;">IM</span>'

    # Dados para JS
    conv_emp_js = json.dumps(conv_employees)
    mkt_campanhas_js = json.dumps(mkt_data.get("campanhas", {}))

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard IM Incorporadora</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
:root{{
  --glass:rgba(255,255,255,0.68);
  --glass-b:rgba(255,255,255,0.82);
  --shadow:0 4px 24px rgba(0,90,200,0.08),0 1px 4px rgba(0,90,200,0.05),inset 0 1px 0 rgba(255,255,255,0.95);
  --blur:blur(22px) saturate(200%);
  --text:#1d1d1f;--text2:#6e6e73;
  --blue:#0071e3;--green:#28cd41;--orange:#ff9f0a;
  --red:#ff3b30;--purple:#5e5ce6;--teal:#32ade6;
  --r:18px;--rsm:12px;
}}
body{{
  font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',sans-serif;
  background:linear-gradient(160deg,#dbeafe 0%,#eff6ff 55%,#e0f2fe 100%);
  min-height:100vh;color:var(--text);
}}

/* ===== NAVBAR ===== */
.navbar{{position:fixed;top:0;left:0;right:0;height:56px;background:rgba(245,250,255,0.82);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);border-bottom:1px solid rgba(200,220,255,0.5);display:flex;align-items:center;justify-content:space-between;padding:0 20px;z-index:100;box-shadow:0 1px 12px rgba(0,90,200,0.07);}}
.nav-left{{display:flex;align-items:center;gap:12px;}}
.nav-logo-wrap img{{height:32px;object-fit:contain;display:block;}}
.nav-divider{{width:1.5px;height:24px;background:rgba(0,90,200,0.18);border-radius:2px;}}
.nav-page-nome{{font-size:15px;font-weight:700;color:var(--text);letter-spacing:-.01em;}}
.nav-right{{display:flex;align-items:center;gap:10px;}}
.periodo-pill{{background:rgba(0,113,227,0.1);border:1.5px solid rgba(0,113,227,0.22);color:var(--blue);font-size:12px;font-weight:700;padding:6px 14px;border-radius:20px;cursor:pointer;white-space:nowrap;transition:all .2s;user-select:none;letter-spacing:.01em;}}
.periodo-pill:hover{{background:rgba(0,113,227,0.17);}}
.menu-btn{{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.88);backdrop-filter:var(--blur);border:1.5px solid rgba(200,220,255,0.7);box-shadow:0 2px 10px rgba(0,90,200,0.1);display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--text2);transition:all .2s;}}
.menu-btn:hover{{transform:scale(1.06);box-shadow:0 4px 16px rgba(0,90,200,0.15);}}
.menu-btn.aberto{{background:var(--blue);color:white;border-color:var(--blue);}}

/* ===== MENU OVERLAY ===== */
.menu-overlay{{position:fixed;inset:0;background:rgba(0,30,80,0.1);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);z-index:200;display:none;align-items:center;justify-content:center;}}
.menu-overlay.vis{{display:flex;}}
.menu-sheet{{background:rgba(248,252,255,0.92);backdrop-filter:blur(40px) saturate(220%);-webkit-backdrop-filter:blur(40px) saturate(220%);border:1.5px solid rgba(200,220,255,0.7);border-radius:28px;padding:26px 22px;box-shadow:0 24px 60px rgba(0,60,180,0.14),inset 0 1px 0 white;width:340px;max-width:92vw;}}
.menu-titulo{{font-size:12px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.07em;text-align:center;margin-bottom:16px;}}
.nav-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}}
.ni{{background:rgba(255,255,255,0.75);border:1.5px solid rgba(200,220,255,0.6);border-radius:var(--rsm);padding:15px 6px 12px;display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;transition:all .18s;box-shadow:0 2px 8px rgba(0,90,200,0.05);}}
.ni:hover{{transform:scale(1.04);box-shadow:0 6px 18px rgba(0,90,200,0.12);background:rgba(255,255,255,0.95);}}
.ni.ativo{{background:var(--blue);border-color:var(--blue);box-shadow:0 4px 16px rgba(0,113,227,0.3);color:white;}}
.ni.ativo .ni-label{{color:white;}}
.ni-ico{{line-height:1;}}
.ni-label{{font-size:11px;font-weight:700;color:var(--text2);text-align:center;}}
.menu-fechar{{margin-top:16px;width:100%;padding:12px;background:rgba(0,0,0,0.05);border:none;border-radius:var(--rsm);font-size:15px;font-weight:600;color:var(--text);cursor:pointer;font-family:inherit;}}

/* ===== PERÍODO SHEET ===== */
.per-sheet{{position:fixed;top:66px;right:20px;background:rgba(248,252,255,0.96);backdrop-filter:blur(40px) saturate(220%);border:1.5px solid rgba(200,220,255,0.7);border-radius:20px;padding:18px;box-shadow:0 12px 40px rgba(0,60,180,0.12);z-index:150;display:none;min-width:230px;}}
.per-sheet.vis{{display:block;}}
.per-titulo{{font-size:12px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px;}}
.per-lista{{display:flex;flex-direction:column;gap:3px;}}
.per-btn{{padding:9px 12px;border-radius:9px;font-size:14px;font-weight:500;cursor:pointer;border:none;background:transparent;text-align:left;color:var(--text);font-family:inherit;transition:background .15s;}}
.per-btn:hover{{background:rgba(0,113,227,0.07);color:var(--blue);}}
.per-btn.ativo{{background:rgba(0,113,227,0.1);color:var(--blue);font-weight:700;}}
.dts{{margin-top:8px;display:none;gap:6px;flex-direction:column;}}
.dts.vis{{display:flex;}}
.dts label{{font-size:12px;color:var(--text2);font-weight:600;}}
.dts input{{width:100%;padding:7px 10px;border-radius:8px;border:1.5px solid rgba(0,113,227,0.2);font-size:14px;background:white;font-family:inherit;}}

/* ===== CONTEÚDO ===== */
.conteudo{{padding:72px 20px 40px;max-width:1100px;margin:0 auto;}}
.page{{display:none;}}.page.ativa{{display:block;}}
.atu{{font-size:12px;color:var(--text2);margin-bottom:16px;}}
.sec{{font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.08em;margin:24px 0 10px;}}

/* GLASS CARD */
.g{{background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);border:1.5px solid var(--glass-b);border-radius:var(--r);box-shadow:var(--shadow);}}

/* KPI */
.kpi-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}}
.kpi{{padding:16px 18px;}}
.kl{{font-size:11px;color:var(--text2);font-weight:600;margin-bottom:6px;}}
.kv{{font-size:20px;font-weight:800;letter-spacing:-.5px;}}

/* METAS */
.metas-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;}}
.mc{{padding:18px 20px;}}
.mt{{font-size:12px;font-weight:700;color:var(--text2);margin-bottom:10px;}}
.mr{{display:flex;align-items:baseline;gap:6px;margin-bottom:10px;}}
.mv{{font-size:18px;font-weight:800;color:var(--text);}}
.mde{{font-size:12px;color:var(--text2);}}
.bb{{background:rgba(0,90,200,0.08);border-radius:8px;height:8px;overflow:hidden;margin-bottom:6px;}}
.bp{{height:100%;border-radius:8px;transition:width .5s cubic-bezier(.34,1.56,.64,1);}}
.mp{{font-size:12px;color:var(--text2);}}

/* MÓDULOS */
.mod-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}}
.modc{{padding:18px;border-top:3px solid;}}
.modt{{font-size:13px;font-weight:700;margin-bottom:8px;}}
.modn{{font-size:26px;font-weight:800;letter-spacing:-1px;}}
.modl{{font-size:12px;color:var(--text2);margin-top:3px;}}

/* GRÁFICOS */
.charts-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;}}
.cc{{padding:18px;}}
.ct{{font-size:13px;font-weight:700;color:var(--text);margin-bottom:14px;}}

/* TABELA DE OPERADORES */
.op-table{{width:100%;border-collapse:collapse;font-size:13px;}}
.op-table th{{text-align:left;padding:10px 12px;font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.05em;border-bottom:1.5px solid rgba(0,90,200,0.1);}}
.op-table td{{padding:10px 12px;border-bottom:1px solid rgba(0,90,200,0.06);}}
.op-table tr:last-child td{{border-bottom:none;}}
.op-table tr:hover td{{background:rgba(0,113,227,0.04);}}
.op-num{{font-weight:700;color:var(--blue);}}
.op-val{{color:var(--text2);}}

/* STATUS CARDS */
.status-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:4px;}}
.stc{{padding:16px 18px;text-align:center;}}
.stn{{font-size:26px;font-weight:800;letter-spacing:-1px;}}
.stl{{font-size:12px;color:var(--text2);margin-top:4px;font-weight:600;}}

/* CALENDÁRIO */
.cal-head{{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;}}
.cal-nav{{width:36px;height:36px;border-radius:50%;background:rgba(0,90,200,0.07);border:none;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--blue);font-weight:700;}}
.cal-t{{font-size:17px;font-weight:800;}}
.cal-grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;}}
.cdow{{text-align:center;font-size:11px;font-weight:700;color:var(--text2);padding:6px 0;}}
.cday{{aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:10px;font-size:13px;font-weight:600;color:var(--text);position:relative;}}
.cday.outro{{color:#c7c7cc;}}
.cday.hoje{{background:var(--blue);color:white;}}
.cday.deal{{background:rgba(40,205,65,0.12);border:1px solid rgba(40,205,65,0.3);}}
.cday.hoje.deal{{background:var(--blue);}}
.cbadge{{position:absolute;top:2px;right:2px;background:var(--green);color:white;font-size:8px;font-weight:800;border-radius:5px;padding:1px 4px;}}
.cday.hoje .cbadge{{background:rgba(255,255,255,0.35);}}

/* LOGIN */
.login-overlay{{position:fixed;inset:0;background:rgba(0,30,80,0.18);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);z-index:300;display:none;align-items:center;justify-content:center;}}
.login-overlay.vis{{display:flex;}}
.login-sheet{{background:rgba(248,252,255,0.95);backdrop-filter:blur(40px) saturate(220%);border:1.5px solid rgba(200,220,255,0.7);border-radius:28px;padding:36px 32px;box-shadow:0 24px 60px rgba(0,60,180,0.16),inset 0 1px 0 white;width:360px;max-width:92vw;text-align:center;}}
.login-logo{{margin-bottom:20px;}}
.login-logo img{{height:40px;object-fit:contain;}}
.login-titulo{{font-size:18px;font-weight:800;color:var(--text);margin-bottom:4px;}}
.login-sub{{font-size:13px;color:var(--text2);margin-bottom:24px;}}
.login-input{{width:100%;padding:12px 14px;border-radius:12px;border:1.5px solid rgba(0,90,200,0.15);font-size:15px;background:rgba(255,255,255,0.9);font-family:inherit;color:var(--text);margin-bottom:12px;display:block;text-align:left;}}
.login-input:focus{{outline:none;border-color:var(--blue);box-shadow:0 0 0 3px rgba(0,113,227,0.12);}}
.login-erro{{color:var(--red);font-size:13px;font-weight:600;margin-bottom:12px;display:none;}}
.login-btn{{width:100%;padding:14px;background:var(--blue);color:white;font-weight:700;border:none;border-radius:12px;font-size:15px;font-family:inherit;cursor:pointer;margin-bottom:10px;}}
.login-btn:hover{{background:#005bbf;}}
.login-cancel{{background:none;border:none;color:var(--text2);font-size:14px;cursor:pointer;font-family:inherit;padding:4px;}}

.ci{{width:100%;padding:12px 14px;border-radius:12px;border:1.5px solid rgba(0,90,200,0.15);font-size:15px;background:rgba(255,255,255,0.85);margin-bottom:14px;font-family:inherit;color:var(--text);}}
.cl{{display:block;font-size:13px;font-weight:700;color:var(--text2);margin-bottom:6px;}}
.cb{{background:var(--blue);color:white;font-weight:700;border:none;padding:14px;border-radius:12px;cursor:pointer;font-size:15px;font-family:inherit;width:100%;}}

/* CRM cards header */
.crm-cards{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;}}
.crmcard{{padding:16px 20px;min-width:180px;}}

@media(max-width:700px){{
  .kpi-grid{{grid-template-columns:1fr 1fr;}}
  .metas-grid,.mod-grid,.charts-grid,.status-grid{{grid-template-columns:1fr;}}
}}
</style>
</head>
<body>

<!-- NAVBAR -->
<div class="navbar">
  <div class="nav-left">
    <div class="nav-logo-wrap">{logo_html}</div>
    <div class="nav-divider"></div>
    <div id="nav-page-nome" class="nav-page-nome">KPIs</div>
  </div>
  <div class="nav-right">
    <div class="periodo-pill" id="per-pill" onclick="togglePer()">📅 Este ano</div>
    <div class="menu-btn" id="menu-btn" onclick="toggleMenu()">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path fill-rule="evenodd" d="M3 6.75A.75.75 0 013.75 6h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 6.75zM3 12a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 12zm0 5.25a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75a.75.75 0 01-.75-.75z" clip-rule="evenodd"/></svg>
    </div>
  </div>
</div>

<!-- MENU OVERLAY -->
<div class="menu-overlay" id="menu-overlay" onclick="fecharMenu()">
  <div class="menu-sheet" onclick="event.stopPropagation()">
    <div class="menu-titulo">Navegação</div>
    <div class="nav-grid">
      <div class="ni ativo" id="ni-geral" onclick="irPara('geral')"><div class="ni-ico">{ICO_HOME}</div><span class="ni-label">KPIs</span></div>
      <div class="ni" id="ni-crm" onclick="irPara('crm')"><div class="ni-ico">{ICO_CRM}</div><span class="ni-label">CRM</span></div>
      <div class="ni" id="ni-mkt" onclick="irPara('mkt')"><div class="ni-ico">{ICO_MKT}</div><span class="ni-label">Marketing</span></div>
      <div class="ni" id="ni-conv" onclick="irPara('conv')"><div class="ni-ico">{ICO_CONV}</div><span class="ni-label">Conversas</span></div>
      <div class="ni" id="ni-cal" onclick="irPara('cal')"><div class="ni-ico">{ICO_CAL}</div><span class="ni-label">Calendário</span></div>
      <div class="ni" id="ni-config" onclick="irPara('config')"><div class="ni-ico">{ICO_CFG}</div><span class="ni-label">Config</span></div>
    </div>
    <button class="menu-fechar" onclick="fecharMenu()">Fechar</button>
  </div>
</div>

<!-- LOGIN CONFIGURAÇÕES -->
<div class="login-overlay" id="login-overlay">
  <div class="login-sheet">
    <div class="login-logo">{logo_html}</div>
    <div class="login-titulo">Acesso restrito</div>
    <div class="login-sub">Insira suas credenciais para acessar as Configurações</div>
    <input type="email" id="login-email" class="login-input" placeholder="E-mail" onkeydown="if(event.key==='Enter') fazerLogin()">
    <input type="password" id="login-senha" class="login-input" placeholder="Senha" onkeydown="if(event.key==='Enter') fazerLogin()">
    <div class="login-erro" id="login-erro">E-mail ou senha incorretos. Tente novamente.</div>
    <button class="login-btn" onclick="fazerLogin()">Entrar</button>
    <button class="login-cancel" onclick="fecharLogin()">Cancelar</button>
  </div>
</div>

<!-- PERÍODO SHEET -->
<div class="per-sheet" id="per-sheet">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
    <div class="per-titulo" style="margin-bottom:0">Período</div>
    <button onclick="fecharPer()" style="background:none;border:none;font-size:18px;color:var(--text2);cursor:pointer;line-height:1;padding:0 2px">×</button>
  </div>
  <div class="per-lista">
    <button class="per-btn" onclick="setPer('tudo','Tudo',this)">Tudo (histórico)</button>
    <button class="per-btn" onclick="setPer('este_mes','Este mês',this)">Este mês</button>
    <button class="per-btn" onclick="setPer('mes_passado','Mês passado',this)">Mês passado</button>
    <button class="per-btn" onclick="setPer('30dias','Últimos 30 dias',this)">Últimos 30 dias</button>
    <button class="per-btn ativo" onclick="setPer('este_ano','Este ano',this)">Este ano</button>
    <button class="per-btn" onclick="setPer('personalizado','Personalizado',this)">Personalizado...</button>
    <div class="dts" id="dts">
      <label>De <input type="date" id="dt-ini" onchange="filtrar()"></label>
      <label>Até <input type="date" id="dt-fim" onchange="filtrar()"></label>
    </div>
  </div>
</div>

<div class="conteudo">
<div class="atu">Dados buscados em {agora}</div>

<!-- ===== VISÃO GERAL ===== -->
<div id="page-geral" class="page ativa">
  <div class="sec">KPIs Principais</div>
  <div class="kpi-grid">
    <div class="kpi g"><div class="kl">Receita Fechada</div><div class="kv" id="k-rec" style="color:var(--green)">—</div></div>
    <div class="kpi g"><div class="kl">Pipeline Ativo</div><div class="kv" id="k-pip" style="color:var(--blue)">—</div></div>
    <div class="kpi g"><div class="kl">Negociações Ativas</div><div class="kv" id="k-at" style="color:var(--blue)">—</div></div>
    <div class="kpi g">
      <div class="kl">Leads Marketing</div>
      <div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">
        <div class="kv" id="k-ldmkt" style="color:var(--orange)">—</div>
        <div id="k-ldmkt-pct" style="font-size:12px;color:var(--text2);font-weight:600;white-space:nowrap">—</div>
      </div>
    </div>
    <div class="kpi g">
      <div class="kl">Leads Gerados (CRM)</div>
      <div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">
        <div class="kv" id="k-ld" style="color:var(--orange)">—</div>
        <div id="k-ld-pct" style="font-size:12px;color:var(--text2);font-weight:600;white-space:nowrap">—</div>
      </div>
    </div>
    <div class="kpi g">
      <div class="kl">Conv. Lead → Agendamento</div>
      <div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">
        <div class="kv" id="k-lag" style="color:var(--green)">—</div>
        <div id="k-lag-det" style="font-size:12px;color:var(--text2);font-weight:600;white-space:nowrap">—</div>
      </div>
    </div>
    <div class="kpi g">
      <div class="kl">Conv. Agendamento → Venda</div>
      <div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">
        <div class="kv" id="k-av" style="color:var(--teal)">—</div>
        <div id="k-av-det" style="font-size:12px;color:var(--text2);font-weight:600;white-space:nowrap">—</div>
      </div>
    </div>
    <div class="kpi g">
      <div class="kl">Conversão Lead → Venda</div>
      <div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">
        <div class="kv" id="k-cv" style="color:var(--purple)">—</div>
        <div id="k-cv-det" style="font-size:12px;color:var(--text2);font-weight:600;white-space:nowrap">—</div>
      </div>
    </div>
    <div class="kpi g"><div class="kl">Ticket Médio</div><div class="kv" id="k-tk" style="color:var(--teal)">—</div></div>
  </div>

  <div class="sec">Metas do Período</div>
  <div class="metas-grid">
    <div class="mc g">
      <div class="mt">Meta VGV (Fechamento)</div>
      <div class="mr"><span class="mv" id="vgv-r">—</span><span class="mde" id="vgv-d">—</span></div>
      <div class="bb"><div class="bp" id="vgv-b" style="width:0%;background:var(--green)"></div></div>
      <div class="mp" id="vgv-p">—</div>
    </div>
    <div class="mc g">
      <div class="mt">Meta de Entrada</div>
      <div class="mr"><span class="mv" id="ent-r">—</span><span class="mde" id="ent-d">—</span></div>
      <div class="bb"><div class="bp" id="ent-b" style="width:0%;background:var(--orange)"></div></div>
      <div class="mp" id="ent-p">—</div>
    </div>
  </div>

  <div class="sec">Pipeline Executivo</div>
  <div class="g" style="padding:20px"><canvas id="gFunil"></canvas></div>

  <div class="sec">Resumo por Módulo</div>
  <div class="mod-grid">
    <div class="modc g" style="border-color:var(--blue)"><div class="modt">CRM</div><div class="modn" id="m-crm" style="color:var(--blue)">—</div><div class="modl">leads no período</div></div>
    <div class="modc g" style="border-color:var(--orange)"><div class="modt">Marketing</div><div class="modn" id="m-mkt" style="color:var(--orange)">—</div><div class="modl">contatos MKT no período</div></div>
    <div class="modc g" style="border-color:var(--green)"><div class="modt">Conversas</div><div class="modn" id="m-cv" style="color:var(--green)">—</div><div class="modl">contatos totais</div></div>
  </div>
</div>

<!-- ===== CRM ===== -->
<div id="page-crm" class="page">
  <div class="crm-cards">
    <div class="crmcard g"><div class="kl">Negociações no período</div><div class="kv" id="crm-t" style="color:var(--blue)">—</div></div>
    <div class="crmcard g"><div class="kl">Valor total</div><div class="kv" id="crm-v" style="color:var(--blue)">—</div></div>
  </div>
  <div class="charts-grid">
    <div class="cc g"><div class="ct">Negociações por etapa</div><canvas id="gCrmE"></canvas></div>
    <div class="cc g">
      <div class="ct">Valor por etapa (% do total)</div>
      <canvas id="gCrmV"></canvas>
    </div>
  </div>
  <div class="sec">Cards por Operador (período)</div>
  <div class="g" style="padding:18px">
    <table class="op-table">
      <thead><tr><th>Operador</th><th>Negociações</th><th>Valor Total</th><th>% do total</th></tr></thead>
      <tbody id="crm-op-tbody"><tr><td colspan="4" style="text-align:center;color:var(--text2);padding:20px">Carregando...</td></tr></tbody>
    </table>
  </div>
</div>

<!-- ===== MARKETING ===== -->
<div id="page-mkt" class="page">
  {'<div class="g" style="padding:14px 18px;color:var(--orange);margin-bottom:12px;font-size:13px;font-weight:600;">'+mkt_aviso+'</div>' if mkt_aviso else ''}
  <div class="crm-cards">
    <div class="crmcard g"><div class="kl">Leads no período</div><div class="kv" id="mkt-t" style="color:var(--orange)">—</div></div>
  </div>
  <div class="charts-grid">
    <div class="cc g"><div class="ct">Leads por estágio</div><canvas id="gMkt"></canvas></div>
  </div>
  <div class="sec">Leads por Campanha / Segmentação</div>
  <div class="g" style="padding:18px">
    <div style="font-size:12px;color:var(--text2);margin-bottom:12px">
      Contagem total de leads em cada segmentação ativa no RD Station Marketing.
    </div>
    <table class="op-table" id="mkt-camp-table">
      <thead><tr><th>Campanha / Segmentação</th><th>Leads</th><th>% do total</th></tr></thead>
      <tbody id="mkt-camp-tbody">
        <tr><td colspan="3" style="text-align:center;color:var(--text2);padding:20px">Carregando...</td></tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ===== CONVERSAS ===== -->
<div id="page-conv" class="page">

  <div class="sec">Contatos cadastrados</div>
  <div class="kpi-grid" style="grid-template-columns:repeat(2,1fr)">
    <div class="kpi g">
      <div class="kl">Total de contatos</div>
      <div class="kv" id="cv-total" style="color:var(--blue)">—</div>
    </div>
    <div class="kpi g">
      <div class="kl">Atendentes cadastrados</div>
      <div class="kv" id="cv-emp" style="color:var(--teal)">—</div>
    </div>
  </div>

  <div class="sec">Conversão Lead → Agendamento (via CRM)</div>
  <div class="mc g">
    <div class="mt">Leads que chegaram à etapa de Agendamento ou além</div>
    <div class="mr"><span class="mv" id="cv-ag-v" style="color:var(--green)">—</span><span class="mde" id="cv-ag-d"></span></div>
    <div class="bb"><div class="bp" id="cv-ag-b" style="width:0%;background:var(--green)"></div></div>
    <div class="mp">Deals em AGENDAMENTO+ ÷ total deals ativos no CRM</div>
  </div>

  <div class="sec">Atendentes</div>
  <div class="g" style="padding:18px">
    <div style="font-size:12px;color:var(--text2);margin-bottom:12px">* Negociações no CRM calculadas cruzando o nome do atendente com o operador responsável pelo deal.</div>
    <table class="op-table">
      <thead><tr><th>Nome</th><th>E-mail</th><th>Neg. no CRM</th></tr></thead>
      <tbody id="conv-emp-tbody">
        <tr><td colspan="3" style="text-align:center;color:var(--text2);padding:20px">Carregando...</td></tr>
      </tbody>
    </table>
  </div>

  <div class="sec">Métricas operacionais em tempo real</div>
  <div class="g" style="padding:20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap">
    <div style="flex:1;min-width:200px">
      <div style="font-size:14px;color:var(--text2);line-height:1.6">
        Conversas abertas, tempo de atendimento e status de fila não estão disponíveis via API neste plano do RD Conversas.
        Para ver essas métricas em tempo real, acesse o painel diretamente.
      </div>
    </div>
    <a href="https://conversas.rdstation.com" target="_blank" style="background:var(--blue);color:white;font-weight:700;padding:12px 22px;border-radius:12px;text-decoration:none;white-space:nowrap;font-size:14px;">
      Abrir RD Conversas →
    </a>
  </div>

</div>

<!-- ===== CALENDÁRIO ===== -->
<div id="page-cal" class="page">
  <div class="g" style="padding:20px">
    <div class="cal-head">
      <button class="cal-nav" onclick="calMov(-1)">‹</button>
      <span class="cal-t" id="cal-t">—</span>
      <button class="cal-nav" onclick="calMov(1)">›</button>
    </div>
    <div class="cal-grid" id="cal-grid"></div>
  </div>
</div>

<!-- ===== CONFIG ===== -->
<div id="page-config" class="page">
  <div class="g" style="padding:24px;max-width:460px">
    <div style="font-size:17px;font-weight:800;margin-bottom:6px">Metas</div>
    <div style="font-size:13px;color:var(--text2);margin-bottom:22px">Salvas neste navegador.</div>
    <label class="cl">Meta VGV (Fechamento) — R$</label>
    <input type="number" id="cfg-vgv" class="ci" step="0.01">
    <label class="cl">Meta de Entrada — R$</label>
    <input type="number" id="cfg-ent" class="ci" step="0.01">
    <label class="cl">Entrada Realizada (período) — R$</label>
    <input type="number" id="cfg-entr" class="ci" step="0.01">
    <button class="cb" onclick="salvar()">Salvar</button>
    <div id="cfg-ok" style="text-align:center;color:var(--green);font-weight:700;margin-top:12px;display:none">✅ Salvo!</div>
  </div>
</div>
</div>

<script>
Chart.register(ChartDataLabels);

const CRM = {json.dumps(crm_deals)};
const MKT = {json.dumps(mkt_data['contatos'])};
const MKT_CAMP = {mkt_campanhas_js};
const CONV_TOTAL = {conv_total};
const CONV_EMP = {conv_emp_js};
const VGV0={META_VGV_PADRAO}, ENT0={META_ENTRADA_PADRAO};
const ORDEM=["LEADS","EM CONTATO","AGENDAMENTO","ATENDIMENTO REALIZADO","NEGOCIAÇÃO","FECHAMENTO"];

let periodo='este_ano';
let calAno=new Date().getFullYear(), calMes=new Date().getMonth();
let cF,cCE,cCV,cM;
const $=id=>document.getElementById(id);

// ---- NAV ----
const NOMES_PAGINA = {{
  geral: 'KPIs', crm: 'CRM',
  mkt: 'Marketing', conv: 'Conversas',
  cal: 'Calendário', config: 'Configurações'
}};

// Credenciais de acesso às Configurações
const _AE = atob('d2F0c29uQGltaW5jb3Jwb3JhZG9yYS5jb20uYnI=');
const _AS = atob('QWxhbmEwNTIxMzA=');
let cfgAuth = sessionStorage.getItem('cfg_auth') === '1';

function irPara(id){{
  if(id === 'config' && !cfgAuth){{
    mostrarLogin();
    return;
  }}
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('ativa'));
  document.querySelectorAll('.ni').forEach(n=>n.classList.remove('ativo'));
  $('page-'+id).classList.add('ativa');
  $('ni-'+id).classList.add('ativo');
  $('nav-page-nome').textContent = NOMES_PAGINA[id] || id;
  $('per-sheet').classList.remove('vis');
  fecharMenu();
  if(id==='cal') renderCal();
}}

function mostrarLogin(){{
  fecharMenu();
  $('login-email').value='';
  $('login-senha').value='';
  $('login-erro').style.display='none';
  $('login-overlay').classList.add('vis');
  setTimeout(()=>$('login-email').focus(), 100);
}}

function fecharLogin(){{
  $('login-overlay').classList.remove('vis');
}}

function fazerLogin(){{
  const email=$('login-email').value.trim();
  const senha=$('login-senha').value;
  if(email===_AE && senha===_AS){{
    cfgAuth=true;
    sessionStorage.setItem('cfg_auth','1');
    $('login-overlay').classList.remove('vis');
    irPara('config');
  }}else{{
    $('login-erro').style.display='block';
    $('login-senha').value='';
    $('login-senha').focus();
  }}
}}
function toggleMenu(){{
  $('menu-overlay').classList.toggle('vis');
  $('menu-btn').classList.toggle('aberto');
  $('per-sheet').classList.remove('vis');
}}
function fecharMenu(){{
  $('menu-overlay').classList.remove('vis');
  $('menu-btn').classList.remove('aberto');
}}

// ---- PERÍODO ----
function togglePer(){{
  $('per-sheet').classList.toggle('vis');
  fecharMenu();
}}
function fecharPer(){{
  $('per-sheet').classList.remove('vis');
}}
function setPer(v,label,el){{
  periodo=v;
  document.querySelectorAll('.per-btn').forEach(b=>b.classList.remove('ativo'));
  el.classList.add('ativo');
  $('per-pill').textContent='📅 '+label;
  $('dts').classList.toggle('vis',v==='personalizado');
  if(v!=='personalizado'){{ $('per-sheet').classList.remove('vis'); filtrar(); }}
}}
document.addEventListener('click',e=>{{
  const s=$('per-sheet'),p=$('per-pill');
  if(!s.contains(e.target)&&!p.contains(e.target)) s.classList.remove('vis');
}});

function intervalo(){{
  const h=new Date();
  const hoje=new Date(h.getFullYear(),h.getMonth(),h.getDate());
  let i=null,f=null;
  if(periodo==='tudo') return{{i:null,f:null}};
  if(periodo==='este_mes'){{
    i=new Date(hoje.getFullYear(),hoje.getMonth(),1);
    f=new Date(hoje.getFullYear(),hoje.getMonth()+1,0,23,59,59);
  }} else if(periodo==='mes_passado'){{
    i=new Date(hoje.getFullYear(),hoje.getMonth()-1,1);
    f=new Date(hoje.getFullYear(),hoje.getMonth(),0,23,59,59);
  }} else if(periodo==='30dias'){{
    i=new Date(hoje.getTime()-30*24*60*60*1000);
    f=new Date(hoje.getFullYear(),hoje.getMonth(),hoje.getDate(),23,59,59);
  }} else if(periodo==='este_ano'){{
    i=new Date(hoje.getFullYear(),0,1);
    f=new Date(hoje.getFullYear(),11,31,23,59,59);
  }} else if(periodo==='personalizado'){{
    const a=$('dt-ini').value, b=$('dt-fim').value;
    i=a?new Date(a+'T00:00:00'):null;
    f=b?new Date(b+'T23:59:59'):null;
  }}
  return{{i,f}};
}}
function ok(ds,i,f){{
  if(!i&&!f) return true;
  if(!ds) return false;
  const p=ds.split('-');
  if(p.length<3) return false;
  const d=new Date(parseInt(p[0]),parseInt(p[1])-1,parseInt(p[2]));
  if(i&&d<i) return false; if(f&&d>f) return false; return true;
}}
function R(v){{ return 'R$ '+v.toLocaleString('pt-BR',{{minimumFractionDigits:2,maximumFractionDigits:2}}); }}
function ord(e){{ const n=e.toUpperCase(); for(let i=0;i<ORDEM.length;i++) if(n.includes(ORDEM[i])) return i; return 99; }}
function metas(){{
  return{{
    vgv: parseFloat(localStorage.getItem('meta_vgv'))||VGV0,
    ent: parseFloat(localStorage.getItem('meta_ent'))||ENT0,
    entR: parseFloat(localStorage.getItem('ent_real'))||0
  }};
}}

// ---- FILTRO PRINCIPAL ----
function filtrar(){{
  const{{i,f}}=intervalo();

  // CRM
  const deals=CRM.filter(d=>ok(d.created_at,i,f));
  let at=0,pv=0,rec=0,vnd=0;
  const pe={{}},ve={{}},pu={{}},pvu={{}};
  deals.forEach(d=>{{
    const eu=d.stage.toUpperCase(),g=eu.includes('FECHA'),p=eu.includes('PERDID');
    pe[d.stage]=(pe[d.stage]||0)+1;
    ve[d.stage]=(ve[d.stage]||0)+d.value;
    if(g){{vnd++;rec+=d.value;}}else if(!p){{at++;pv+=d.value;}}
    const u=d.user||'Sem responsável';
    pu[u]=(pu[u]||0)+1;
    pvu[u]=(pvu[u]||0)+d.value;
  }});

  const tk=vnd>0?rec/vnd:0;
  const ef=Object.keys(pe).filter(e=>!e.toUpperCase().includes('PERDID'));
  ef.sort((a,b)=>ord(a)-ord(b));
  const fq=ef.map(e=>pe[e]),fv=ef.map(e=>ve[e]);
  const fp=fq[0]||1;
  const fc=fq.map(q=>Math.round(q/fp*1000)/10);

  // MKT
  const mf=MKT.filter(c=>ok(c.created_at,i,f));
  const me={{}};
  mf.forEach(c=>{{me[c.stage]=(me[c.stage]||0)+1;}});
  const ml=Object.keys(me).sort((a,b)=>me[b]-me[a]),mv=ml.map(e=>me[e]);

  // LEADS = todos os deals do CRM no período (todas as etapas)
  const ct=CONV_TOTAL;
  const lds = deals.length;
  const cvr = lds>0 ? (vnd/lds*100) : 0;

  // METAS
  const{{vgv,ent,entR}}=metas();
  const pv2=Math.min(rec/vgv*100,100);
  const pe2=Math.min(entR/ent*100,100);

  // DOM - KPIs
  $('k-rec').textContent=R(rec);
  $('k-pip').textContent=R(pv);
  $('k-at').textContent=at.toLocaleString('pt-BR');
  $('k-ld').textContent=lds.toLocaleString('pt-BR');
  $('k-ldmkt').textContent=mf.length.toLocaleString('pt-BR');
  document.querySelector('#k-ld').closest('.kpi').querySelector('.kl').textContent='Leads Gerados (CRM)';
  // % de um pro outro
  const pctMktVirou = mf.length>0 ? (lds/mf.length*100).toFixed(1)+'% virou CRM' : '—';
  const pctCrmDoMkt = lds>0 ? (mf.length/lds*100).toFixed(1)+'% do MKT' : '—';
  $('k-ldmkt-pct').textContent = pctMktVirou;
  $('k-ld-pct').textContent = pctCrmDoMkt;
  $('k-cv').textContent=cvr.toFixed(2)+'%';
  $('k-cv-det').textContent=vnd+' vend'+(vnd===1?'a':'as');
  $('k-tk').textContent=R(tk);

  // DOM - Metas
  $('vgv-r').textContent=R(rec); $('vgv-d').textContent='de '+R(vgv);
  $('vgv-b').style.width=pv2.toFixed(1)+'%'; $('vgv-p').textContent=pv2.toFixed(1)+'% atingido';
  $('ent-r').textContent=R(entR); $('ent-d').textContent='de '+R(ent);
  $('ent-b').style.width=pe2.toFixed(1)+'%'; $('ent-p').textContent=pe2.toFixed(1)+'% atingido';

  // DOM - Módulos
  $('m-crm').textContent=deals.length.toLocaleString('pt-BR');
  $('m-mkt').textContent=mf.length.toLocaleString('pt-BR');
  $('m-cv').textContent=ct.toLocaleString('pt-BR');

  // Conv. Lead → Agendamento (KPIs)
  const ETAPAS_POS=["AGENDAMENTO","ATENDIMENTO REALIZADO","NEGOCIAÇÃO","FECHAMENTO"];
  const posAg=deals.filter(d=>{{
    const eu=d.stage.toUpperCase();
    return !eu.includes('PERDID') && ETAPAS_POS.some(e=>eu.includes(e));
  }}).length;
  const pctLA=lds>0?(posAg/lds*100):0;
  $('k-lag').textContent=pctLA.toFixed(1)+'%';
  $('k-lag-det').textContent=posAg+' agendamento'+(posAg===1?'':'s');

  // Conv. Agendamento → Venda
  const pctAV = posAg>0 ? (vnd/posAg*100) : 0;
  $('k-av').textContent=pctAV.toFixed(1)+'%';
  $('k-av-det').textContent=vnd+' vend'+(vnd===1?'a':'as');

  // DOM - CRM
  const valTotal=deals.reduce((a,d)=>a+d.value,0);
  $('crm-t').textContent=deals.length.toLocaleString('pt-BR');
  $('crm-v').textContent=R(valTotal);
  $('mkt-t').textContent=mf.length.toLocaleString('pt-BR');

  // Tabela de campanhas (dados totais, não filtrados por data pois são contagens fixas da segmentação)
  const campTotal = Object.values(MKT_CAMP).reduce((a,b)=>a+b,0)||1;
  const campTbody = $('mkt-camp-tbody');
  campTbody.innerHTML='';
  const campOrdenado = Object.entries(MKT_CAMP).sort((a,b)=>b[1]-a[1]);
  if(campOrdenado.length){{
    campOrdenado.forEach(([nome,cnt])=>{{
      const pct=(cnt/campTotal*100).toFixed(1);
      campTbody.innerHTML+=`<tr><td style="font-weight:600">${{nome}}</td><td class="op-num">${{cnt.toLocaleString('pt-BR')}}</td><td class="op-val">${{pct}}%</td></tr>`;
    }});
  }}else{{
    campTbody.innerHTML='<tr><td colspan="3" style="text-align:center;color:var(--text2);padding:20px">Sem dados de campanhas disponíveis</td></tr>';
  }}

  // DOM - Conversas
  renderConversas(deals);

  // DOM - Config inputs
  $('cfg-vgv').value=vgv; $('cfg-ent').value=ent; $('cfg-entr').value=entR;

  // GRÁFICOS
  upd(cF,ef,[fq]);
  cF.options.plugins.tooltip.callbacks.afterLabel=ctx=>['Valor: '+R(fv[ctx.dataIndex]),'Conversão: '+fc[ctx.dataIndex]+'%'];
  cF.update();

  const todasE=Object.keys(pe);
  const todasV=todasE.map(e=>ve[e]);
  upd(cCE,todasE,[todasE.map(e=>pe[e])]);

  // Doughnut com % no slice
  cCV.data.labels=todasE;
  cCV.data.datasets[0].data=todasV;
  cCV.update();

  upd(cM,ml,[mv]);

  // Tabela operadores CRM
  const tbody=$('crm-op-tbody');
  tbody.innerHTML='';
  const totalDeals=deals.length;
  Object.entries(pu).sort((a,b)=>b[1]-a[1]).forEach(([u,cnt])=>{{
    const pct=totalDeals>0?(cnt/totalDeals*100).toFixed(1):0;
    tbody.innerHTML+=`<tr><td>${{u}}</td><td class="op-num">${{cnt}}</td><td class="op-val">${{R(pvu[u]||0)}}</td><td class="op-val">${{pct}}%</td></tr>`;
  }});
  if(!Object.keys(pu).length) tbody.innerHTML='<tr><td colspan="4" style="text-align:center;color:var(--text2);padding:20px">Sem dados no período</td></tr>';
}}

// ---- CONVERSAS ----
function renderConversas(deals){{
  // Total de contatos e atendentes
  $('cv-total').textContent = CONV_TOTAL.toLocaleString('pt-BR');
  $('cv-emp').textContent = CONV_EMP.length;

  // Conversão Lead → Agendamento — usa total de deals do CRM (todos os leads)
  const ETAPAS_POS = ["AGENDAMENTO","ATENDIMENTO REALIZADO","NEGOCIAÇÃO","FECHAMENTO"];
  const totalLeads = CRM.length;
  const posAg = CRM.filter(d=>{{
    const eu=d.stage.toUpperCase();
    return !eu.includes('PERDID') && ETAPAS_POS.some(e=>eu.includes(e));
  }}).length;
  const pctLA = totalLeads>0 ? (posAg/totalLeads*100) : 0;
  $('cv-ag-v').textContent=pctLA.toFixed(1)+'%';
  $('cv-ag-d').textContent=' ('+posAg+' de '+totalLeads+' leads totais)';
  $('cv-ag-b').style.width=Math.min(pctLA,100).toFixed(1)+'%';

  // Tabela de atendentes — cruza nome com operadores do CRM
  const dealsPorNome={{}};
  CRM.forEach(d=>{{
    const u=(d.user||'').trim();
    if(u) dealsPorNome[u]=(dealsPorNome[u]||0)+1;
  }});

  const tbody=$('conv-emp-tbody');
  tbody.innerHTML='';
  if(CONV_EMP.length){{
    CONV_EMP.forEach(e=>{{
      // Busca correspondência por nome (parcial, case-insensitive)
      const nEmp=e.name.toLowerCase().trim();
      let negCRM=0;
      Object.entries(dealsPorNome).forEach(([nomeCRM, cnt])=>{{
        const nCRM=nomeCRM.toLowerCase().trim();
        // Considera match se um nome contém o outro (ex: "Thaisy" ↔ "Thaisy Lopes")
        if(nCRM.includes(nEmp)||nEmp.includes(nCRM)) negCRM+=cnt;
      }});
      const negStr = negCRM > 0
        ? `<span class="op-num">${{negCRM}}</span>`
        : `<span style="color:var(--text2)">—</span>`;
      tbody.innerHTML+=`<tr><td style="font-weight:600">${{e.name}}</td><td style="color:var(--text2)">${{e.email}}</td><td>${{negStr}}</td></tr>`;
    }});
  }} else {{
    tbody.innerHTML='<tr><td colspan="3" style="text-align:center;color:var(--text2);padding:20px">Nenhum atendente encontrado</td></tr>';
  }}
}}

// ---- UTILIDADES ----
function upd(c,l,ds){{c.data.labels=l;ds.forEach((v,i)=>c.data.datasets[i].data=v);c.update();}}
function salvar(){{
  const vgv=parseFloat($('cfg-vgv').value);
  const ent=parseFloat($('cfg-ent').value);
  const entR=parseFloat($('cfg-entr').value);
  if(!isNaN(vgv)) localStorage.setItem('meta_vgv',vgv);
  if(!isNaN(ent)) localStorage.setItem('meta_ent',ent);
  if(!isNaN(entR)) localStorage.setItem('ent_real',entR);
  filtrar();
  $('cfg-ok').style.display='block';
  setTimeout(()=>$('cfg-ok').style.display='none',2500);
}}

// ---- CALENDÁRIO ----
const MESES=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
const DIAS=['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];
function renderCal(){{
  $('cal-t').textContent=MESES[calMes]+' '+calAno;
  const dpd={{}};
  CRM.forEach(d=>{{
    if(d.created_at&&d.created_at.startsWith(calAno+'-'+String(calMes+1).padStart(2,'0'))){{
      const dia=parseInt(d.created_at.split('-')[2]);
      dpd[dia]=(dpd[dia]||0)+1;
    }}
  }});
  const grid=$('cal-grid');
  grid.innerHTML='';
  DIAS.forEach(d=>{{const el=document.createElement('div');el.className='cdow';el.textContent=d;grid.appendChild(el);}});
  const prim=new Date(calAno,calMes,1).getDay();
  const ult=new Date(calAno,calMes+1,0).getDate();
  const hoje=new Date();
  for(let k=0;k<prim;k++){{const el=document.createElement('div');el.className='cday outro';grid.appendChild(el);}}
  for(let d=1;d<=ult;d++){{
    const el=document.createElement('div');
    let cls='cday';
    if(d===hoje.getDate()&&calMes===hoje.getMonth()&&calAno===hoje.getFullYear()) cls+=' hoje';
    if(dpd[d]) cls+=' deal';
    el.className=cls;
    el.textContent=d;
    if(dpd[d]){{const b=document.createElement('div');b.className='cbadge';b.textContent=dpd[d];el.appendChild(b);}}
    grid.appendChild(el);
  }}
}}
function calMov(dir){{
  calMes+=dir;if(calMes>11){{calMes=0;calAno++;}}if(calMes<0){{calMes=11;calAno--;}}renderCal();
}}

// ---- INIT CHARTS ----
Chart.defaults.color='#6e6e73';
Chart.defaults.borderColor='rgba(0,90,200,0.07)';

const azul='rgba(0,113,227,0.85)', cr=8;

cF=new Chart($('gFunil'),{{
  type:'bar',
  data:{{labels:[],datasets:[{{label:'Negociações',data:[],backgroundColor:azul,borderRadius:cr}}]}},
  options:{{indexAxis:'y',plugins:{{legend:{{display:false}},datalabels:{{display:false}},tooltip:{{callbacks:{{}}}}}},scales:{{x:{{beginAtZero:true}},y:{{grid:{{display:false}}}}}}}}
}});

cCE=new Chart($('gCrmE'),{{
  type:'bar',
  data:{{labels:[],datasets:[{{label:'Negociações',data:[],backgroundColor:azul,borderRadius:cr}}]}},
  options:{{plugins:{{legend:{{display:false}},datalabels:{{display:false}}}},scales:{{y:{{beginAtZero:true}},x:{{grid:{{display:false}}}}}}}}
}});

cCV=new Chart($('gCrmV'),{{
  type:'doughnut',
  data:{{labels:[],datasets:[{{data:[],backgroundColor:['#0071e3','#32ade6','#28cd41','#ff9f0a','#ff3b30','#5e5ce6','#ff2d55']}}]}},
  options:{{
    plugins:{{
      legend:{{position:'bottom',labels:{{font:{{size:11}},padding:12}}}},
      datalabels:{{
        color:'#fff',
        font:{{weight:'bold',size:12}},
        formatter:(value,ctx)=>{{
          const sum=ctx.dataset.data.reduce((a,b)=>a+b,0);
          const pct=(value/sum*100);
          return pct>4?pct.toFixed(1)+'%':'';
        }}
      }}
    }}
  }}
}});

cM=new Chart($('gMkt'),{{
  type:'bar',
  data:{{labels:[],datasets:[{{label:'Leads',data:[],backgroundColor:'rgba(255,159,10,0.85)',borderRadius:cr}}]}},
  options:{{indexAxis:'y',plugins:{{legend:{{display:false}},datalabels:{{display:false}}}},scales:{{x:{{beginAtZero:true}},y:{{grid:{{display:false}}}}}}}}
}});

filtrar();
</script>
</body>
</html>"""

    with open("dashboard_unificado.html","w",encoding="utf-8") as f:
        f.write(html)
    print("\n✅ Dashboard gerado! Abra 'dashboard_unificado.html' no navegador.")


if __name__ == "__main__":
    try:
        crm_deals = buscar_crm()
    except Exception as e:
        print(f"❌ Erro no CRM: {e}")
        crm_deals = []

    try:
        mkt_data = buscar_marketing()
    except Exception as e:
        print(f"❌ Erro no Marketing: {e}")
        mkt_data = {"contatos": [], "erro": True}

    try:
        conv_total = buscar_conversas()
    except Exception as e:
        print(f"❌ Erro no Conversas: {e}")
        conv_total = 0

    try:
        conv_employees = buscar_conversas_employees()
    except Exception as e:
        print(f"❌ Erro nos Atendentes: {e}")
        conv_employees = []

    print(f"\nResumo:")
    print(f"CRM: {len(crm_deals)} negociações")
    print(f"Marketing: {len(mkt_data['contatos'])} contatos")
    print(f"Conversas: {conv_total} contatos | {len(conv_employees)} atendentes")

    gerar_dashboard(crm_deals, mkt_data, conv_total, conv_employees)
