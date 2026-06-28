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
        import time

        # Gera access_token
        resp = requests.post("https://api.rd.services/auth/token", json={
            "client_id":     CLIENT_ID_MKT,
            "client_secret": CLIENT_SECRET_MKT,
            "refresh_token": REFRESH_TOKEN_MKT,
        }, timeout=15)
        if resp.status_code != 200:
            print(f"Erro ao gerar token: {resp.status_code}")
            return {"contatos": [], "campanhas": {}, "erro": True}

        token = resp.json()["access_token"]
        H = {"Authorization": f"Bearer {token}"}

        # Descobre segmentações
        r = requests.get("https://api.rd.services/platform/segmentations", headers=H, timeout=15)
        if r.status_code != 200:
            print(f"Erro ao buscar segmentações: {r.status_code}")
            return {"contatos": [], "campanhas": {}, "erro": True}

        todas_segs = r.json().get("segmentations", [])
        print(f"Segmentações disponíveis: {len(todas_segs)}")

        # Segmentação principal (todos os contatos)
        seg_todos = next(
            (s for s in todas_segs if "todos os contatos" in s.get("name", "").lower()),
            todas_segs[0] if todas_segs else None
        )
        if not seg_todos:
            print("Segmentação principal não encontrada")
            return {"contatos": [], "campanhas": {}, "erro": True}

        print(f"Usando: '{seg_todos['name']}' (ID {seg_todos['id']})")

        # ── 1. Busca todos os contatos PRIMEIRO (prioridade máxima) ──────────
        url_principal = f"https://api.rd.services/platform/segmentations/{seg_todos['id']}/contacts"
        todos_contatos = []
        pagina = 1
        while True:
            tentativa = 0
            while tentativa < 3:
                try:
                    r3 = requests.get(url_principal, headers=H,
                                      params={"page": pagina, "per_page": 100}, timeout=20)
                    if r3.status_code == 429:
                        print(f"  Rate limit na pág {pagina} — aguardando 10s...")
                        time.sleep(10)
                        tentativa += 1
                        continue
                    if r3.status_code != 200:
                        print(f"  Erro página {pagina}: {r3.status_code}")
                        todos_contatos = []  # sinaliza falha
                        pagina = 9999
                        break
                    lote = r3.json().get("contacts", [])
                    if not lote:
                        pagina = 9999
                        break
                    todos_contatos.extend(lote)
                    print(f"  Pág {pagina}: {len(lote)} (total: {len(todos_contatos)})")
                    pagina += 1
                    time.sleep(0.5)  # pausa entre páginas
                    break
                except Exception as e:
                    print(f"  Exceção pág {pagina}: {e}")
                    tentativa += 1
                    time.sleep(2)
            if pagina >= 9999:
                break

        if not todos_contatos:
            print("Nenhum contato encontrado na segmentação principal")
            return {"contatos": [], "campanhas": {}, "erro": True}

        # ── 2. Estágios — apenas a contagem da primeira página de cada segmentação ──
        # (evita centenas de chamadas que causam 429)
        ESTAGIOS = {
            "leads qualificados":  "Lead Qualificado",
            "leads (estágio":      "Lead",
            "clientes (estágio":   "Cliente",
            "oportunidades":       "Oportunidade",
        }

        contagem_estagio = {}
        for seg in todas_segs:
            nome = seg.get("name", "")
            estagio = next((v for k, v in ESTAGIOS.items() if k in nome.lower()), None)
            if not estagio:
                continue
            try:
                r2 = requests.get(
                    f"https://api.rd.services/platform/segmentations/{seg['id']}/contacts",
                    headers=H, params={"page": 1, "per_page": 1}, timeout=10)
                time.sleep(0.3)
                # Usa contatos já buscados para estimar (sem chamadas extras)
            except Exception:
                pass

        # Usa os contatos já buscados e define estágio como "Lead" (padrão)
        contatos_simples = []
        for c in todos_contatos:
            criado_em = c.get("created_at") or c.get("last_conversion_date") or ""
            contatos_simples.append({
                "stage":      "Lead",
                "created_at": str(criado_em)[:10],
            })

        # ── 3. Campanhas — só as que não são estágios padrão ─────────────────
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
            total_camp = 0
            pag = 1
            while True:
                try:
                    rc = requests.get(
                        f"https://api.rd.services/platform/segmentations/{seg['id']}/contacts",
                        headers=H, params={"page": pag, "per_page": 100}, timeout=15)
                    if rc.status_code == 429:
                        print(f"  Rate limit em campanhas — pulando '{nome}'")
                        break
                    if rc.status_code != 200:
                        break
                    lote = rc.json().get("contacts", [])
                    total_camp += len(lote)
                    if not lote:
                        break
                    pag += 1
                    time.sleep(0.4)
                except Exception:
                    break
            if total_camp > 0:
                campanhas[nome] = total_camp
                print(f"  Campanha '{nome}': {total_camp}")

        print(f"✅ Marketing: {len(contatos_simples)} contatos | {len(campanhas)} campanhas")
        return {"contatos": contatos_simples, "campanhas": campanhas, "erro": False}

    except Exception as e:
        print(f"❌ Erro inesperado no Marketing: {e}")
        return {"contatos": [], "campanhas": {}, "erro": True}



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
    import base64, os
    from datetime import datetime

    # Logo
    lb = carregar_logo_base64()
    logo_nav = f'<img src="data:image/png;base64,{lb}" style="height:32px;object-fit:contain">' if lb else '<span style="font-weight:900;font-size:16px;letter-spacing:-0.5px">IM</span>'
    logo_big = f'<img src="data:image/png;base64,{lb}" style="height:54px;object-fit:contain;margin-bottom:4px">' if lb else '<div style="font-size:30px;font-weight:900;letter-spacing:-1px;color:#0071e3">IM</div>'

    # Dados para JS
    CRM_JS        = json.dumps(crm_deals)
    MKT_JS        = json.dumps(mkt_data.get("contatos", []))
    EMP_JS        = json.dumps(conv_employees)
    CAMP_GASTO_JS = json.dumps({})   # API não fornece gasto por campanha
    CAMP_LEADS_JS = json.dumps(mkt_data.get("campanhas", {}))
    META_VGV      = META_VGV_PADRAO
    META_ENT      = META_ENTRADA_PADRAO
    AGORA         = datetime.now().strftime("%d/%m/%Y às %H:%M")
    CONV_TOTAL_N  = conv_total

    # Ícones SVG minimalistas (outline, Apple-style)
    def svg(path, vb="0 0 24 24", w=20, h=20):
        return f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="{w}" height="{h}">{path}</svg>'
    ICO = {
        "home": svg('<path d="M2.25 12l8.954-8.955a1.126 1.126 0 011.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/>'),
        "crm":  svg('<path d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"/>'),
        "mkt":  svg('<path d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"/>'),
        "conv": svg('<path d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155"/>'),
        "cal":  svg('<path d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5"/>'),
        "cfg":  svg('<path d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>'),
        "user": svg('<path d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>'),
        "x":    svg('<path d="M6 18L18 6M6 6l12 12"/>'),
        "photo":svg('<path d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"/><path d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z"/>'),
    }

    MESES_NOMES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    MESES_GOALS_DEFAULT = json.dumps({str(i+1): {"vgv": round(META_VGV/12,2), "ent": round(META_ENT/12,2)} for i in range(12)})


    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard IM</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#f5f5f7;--sf:#fff;--b:rgba(0,0,0,0.07);
  --sh:0 1px 3px rgba(0,0,0,0.06),0 4px 14px rgba(0,0,0,0.04);
  --shm:0 4px 24px rgba(0,0,0,0.09);
  --t:#1d1d1f;--t2:#6e6e73;--t3:#aeaeb2;
  --bl:#0071e3;--blt:rgba(0,113,227,0.08);
  --gr:#28cd41;--or:#ff9500;--rd:#ff3b30;--pu:#5e5ce6;--tl:#32ade6;
  --r:14px;
}}
body{{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',sans-serif;background:var(--bg);color:var(--t);min-height:100vh}}

/* ── TELA AUTH ── */
#auth-wrap{{position:fixed;inset:0;background:linear-gradient(150deg,#dbeafe,#eff6ff,#e0f2fe);display:flex;align-items:center;justify-content:center;z-index:999;transition:opacity .35s}}
#auth-wrap.gone{{opacity:0;pointer-events:none}}
.acard{{background:rgba(255,255,255,.94);backdrop-filter:blur(40px);border:1px solid rgba(255,255,255,.9);border-radius:24px;padding:40px 36px;width:380px;max-width:92vw;box-shadow:var(--shm),inset 0 1px 0 #fff;text-align:center}}
.atabs{{display:flex;background:var(--bg);border-radius:10px;padding:3px;margin-bottom:26px;gap:2px}}
.atab{{flex:1;padding:8px;border-radius:8px;border:none;background:transparent;font-size:14px;font-weight:600;cursor:pointer;color:var(--t2);font-family:inherit;transition:all .2s}}
.atab.on{{background:#fff;color:var(--t);box-shadow:0 1px 4px rgba(0,0,0,0.1)}}
.aform{{display:none}}.aform.vis{{display:block}}
.ait{{font-size:22px;font-weight:800;letter-spacing:-.5px;margin-bottom:4px}}
.asub{{font-size:14px;color:var(--t2);margin-bottom:24px}}
.ainp{{width:100%;padding:12px 15px;border-radius:11px;border:1.5px solid var(--b);font-size:15px;font-family:inherit;color:var(--t);background:#fff;margin-bottom:10px;display:block;transition:border-color .2s}}
.ainp:focus{{outline:none;border-color:var(--bl);box-shadow:0 0 0 3px rgba(0,113,227,.1)}}
.abtn{{width:100%;padding:13px;background:var(--bl);color:#fff;font-weight:700;border:none;border-radius:11px;font-size:15px;cursor:pointer;font-family:inherit;transition:background .15s;margin-top:4px}}
.abtn:hover{{background:#0062c4}}
.abtn.sec{{background:transparent;color:var(--bl);border:1.5px solid var(--bl);margin-top:8px}}
.abtn.sec:hover{{background:var(--blt)}}
.aerro{{color:var(--rd);font-size:13px;font-weight:600;margin-top:8px;display:none}}
.ainfo{{font-size:13px;color:var(--t2);margin-top:12px;line-height:1.5}}
.avatar-upload{{width:72px;height:72px;border-radius:50%;background:var(--blt);border:2px dashed rgba(0,113,227,.3);margin:0 auto 16px;cursor:pointer;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}}
.avatar-upload img{{width:100%;height:100%;object-fit:cover}}
.avatar-upload .placeholder{{color:var(--bl);opacity:.5}}
.avatar-upload input{{position:absolute;inset:0;opacity:0;cursor:pointer}}
.pending-msg{{background:rgba(255,149,0,.08);border:1px solid rgba(255,149,0,.25);border-radius:12px;padding:16px;text-align:center;color:var(--or);font-weight:600;font-size:14px}}

/* ── NAVBAR ── */
.navbar{{position:fixed;top:0;left:0;right:0;height:56px;background:rgba(255,255,255,.88);backdrop-filter:blur(20px);border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 22px;z-index:100}}
.nav-l{{display:flex;align-items:center;gap:12px}}
.nd{{width:1.5px;height:22px;background:var(--b)}}
#nav-pg{{font-size:15px;font-weight:700;letter-spacing:-.2px}}
.nav-r{{display:flex;align-items:center;gap:10px}}
.ppill{{background:var(--blt);border:1.5px solid rgba(0,113,227,.18);color:var(--bl);font-size:12px;font-weight:700;padding:6px 14px;border-radius:20px;cursor:pointer;user-select:none}}
.avatar-btn{{width:36px;height:36px;border-radius:50%;background:var(--bl);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:14px;font-weight:700;color:#fff;overflow:hidden;position:relative;box-shadow:0 2px 8px rgba(0,113,227,.3)}}
.avatar-btn img{{width:100%;height:100%;object-fit:cover}}
.notif-dot{{position:absolute;top:-1px;right:-1px;width:10px;height:10px;background:var(--rd);border-radius:50%;border:2px solid #fff;display:none}}
.notif-dot.vis{{display:block}}

/* ── MENU OVERLAY ── */
.mov{{position:fixed;inset:0;background:rgba(0,0,0,.08);backdrop-filter:blur(6px);z-index:200;display:none;align-items:flex-start;justify-content:flex-end;padding:66px 20px 0}}
.mov.vis{{display:flex}}
.msheet{{background:rgba(255,255,255,.96);backdrop-filter:blur(40px);border:1px solid rgba(255,255,255,.9);border-radius:20px;padding:8px;width:220px;box-shadow:var(--shm)}}
.mitem{{display:flex;align-items:center;gap:11px;padding:10px 14px;border-radius:11px;cursor:pointer;color:var(--t2);transition:all .15s}}
.mitem:hover{{background:var(--bg);color:var(--t)}}
.mitem.on{{background:var(--blt);color:var(--bl)}}
.mitem span{{font-size:14px;font-weight:600}}
.mdiv{{height:1px;background:var(--b);margin:4px 6px}}

/* ── PERÍODO ── */
.psh{{position:fixed;top:66px;right:62px;background:rgba(255,255,255,.97);backdrop-filter:blur(40px);border:1px solid var(--b);border-radius:18px;padding:16px 18px;box-shadow:var(--shm);z-index:150;display:none;min-width:220px}}
.psh.vis{{display:block}}
.pshtit{{font-size:10px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}}
.pshtit button{{background:none;border:none;font-size:17px;color:var(--t3);cursor:pointer;line-height:1}}
.pbtn{{width:100%;padding:8px 12px;border-radius:9px;font-size:14px;cursor:pointer;border:none;background:transparent;text-align:left;color:var(--t);font-family:inherit;transition:background .12s}}
.pbtn:hover,.pbtn.on{{background:var(--blt);color:var(--bl)}}
.pbtn.on{{font-weight:700}}
.dts{{display:none;flex-direction:column;gap:5px;margin-top:8px}}
.dts.vis{{display:flex}}
.dts label{{font-size:12px;color:var(--t2);font-weight:600}}
.dts input{{width:100%;padding:7px 10px;border-radius:8px;border:1px solid var(--b);font-size:14px;font-family:inherit}}

/* ── CONTEÚDO ── */
.wrap{{padding:70px 20px 40px;max-width:1060px;margin:0 auto}}
.page{{display:none}}.page.ativa{{display:block;animation:fu .3s ease both}}
@keyframes fu{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.atu{{font-size:12px;color:var(--t3);margin-bottom:16px}}
.sec{{font-size:10px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.1em;margin:24px 0 10px}}

/* ── CARDS ── */
.card{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:18px 20px}}
.kg{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.kc{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:16px 18px}}
.kc.hi{{border-top:3px solid var(--bl)}}
.kl{{font-size:10px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px}}
.kv{{font-size:21px;font-weight:800;letter-spacing:-.5px;color:var(--t)}}
.kv.b{{color:var(--bl)}}.kv.g{{color:var(--gr)}}.kv.r{{color:var(--rd)}}
.ks{{font-size:11px;color:var(--t3);margin-top:3px;font-weight:600}}

/* ── PREVISIBILIDADE ── */
.pg{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.pc{{background:var(--bl);border-radius:var(--r);padding:20px;color:#fff}}
.pl{{font-size:10px;font-weight:700;opacity:.7;text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px}}
.pv{{font-size:25px;font-weight:800;letter-spacing:-.5px}}
.ps{{font-size:11px;opacity:.6;margin-top:4px}}

/* ── METAS ── */
.mg2{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.mc{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:16px 18px}}
.mt2{{font-size:10px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:9px}}
.mr{{display:flex;align-items:baseline;gap:6px;margin-bottom:9px}}
.mv{{font-size:18px;font-weight:800;color:var(--t)}}.md{{font-size:12px;color:var(--t3)}}
.bb{{background:rgba(0,0,0,.06);border-radius:6px;height:6px;overflow:hidden;margin-bottom:5px}}
.bp{{height:100%;border-radius:6px;transition:width .6s cubic-bezier(.34,1.56,.64,1)}}
.mp{{font-size:11px;color:var(--t3);font-weight:600}}

/* ── MÓDULOS ── */
.mog{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.moc{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:16px;border-top:3px solid}}
.mot{{font-size:11px;font-weight:700;color:var(--t2);margin-bottom:8px}}
.mon{{font-size:26px;font-weight:800;letter-spacing:-1px}}
.mol{{font-size:11px;color:var(--t3);margin-top:3px}}

/* ── CHARTS ── */
.cg{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.cc{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:16px}}
.ct{{font-size:10px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.08em;margin-bottom:13px}}
.rc{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px}}
.rci{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:14px 17px;min-width:160px}}

/* ── TABELA ── */
.tbl{{width:100%;border-collapse:collapse;font-size:13px}}
.tbl th{{text-align:left;padding:8px 12px;font-size:10px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.07em;border-bottom:1.5px solid var(--b)}}
.tbl td{{padding:9px 12px;border-bottom:1px solid var(--b)}}
.tbl tr:last-child td{{border-bottom:none}}
.tbl tr:hover td{{background:var(--bg)}}
.tn{{font-weight:700;color:var(--bl)}}

/* TOP LOSERS — vermelho */
.tbl.danger .tn{{color:var(--rd)}}
.tbl.danger tr:nth-child(1) td{{background:rgba(255,59,48,.04)}}
.tbl.danger tr:nth-child(2) td{{background:rgba(255,59,48,.025)}}
.badge-rd{{background:rgba(255,59,48,.12);color:var(--rd);font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;margin-left:5px}}
.badge-gr{{background:rgba(40,205,65,.12);color:var(--gr);font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;margin-left:5px}}

/* CAMP BAR */
.cbar{{background:rgba(0,0,0,.06);border-radius:4px;height:4px;margin-top:5px;overflow:hidden}}
.cfill{{height:100%;border-radius:4px;background:var(--bl);transition:width .5s}}

/* METAS MENSAIS */
.mm-grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}}
.mm-card{{background:var(--sf);border:1px solid var(--b);border-radius:10px;padding:10px 10px 8px}}
.mm-mes{{font-size:10px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}}
.mm-inp{{width:100%;padding:6px 8px;border-radius:7px;border:1px solid var(--b);font-size:12px;font-family:inherit;color:var(--t);background:#fafafa;margin-bottom:4px}}
.mm-inp:focus{{outline:none;border-color:var(--bl)}}
.mm-lbl{{font-size:10px;color:var(--t3);margin-bottom:3px;font-weight:600}}

/* PERFIL ── */
.perfil-wrap{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
.perfil-avatar{{width:90px;height:90px;border-radius:50%;background:var(--blt);border:3px solid var(--bl);overflow:hidden;cursor:pointer;position:relative;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;color:var(--bl)}}
.perfil-avatar img{{width:100%;height:100%;object-fit:cover}}
.perfil-avatar input{{position:absolute;inset:0;opacity:0;cursor:pointer}}
.perfil-dados{{flex:1}}

/* PENDENTES */
.pend-card{{background:rgba(255,149,0,.06);border:1px solid rgba(255,149,0,.2);border-radius:12px;padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px}}
.pend-av{{width:38px;height:38px;border-radius:50%;background:var(--blt);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--bl);font-size:15px;overflow:hidden;flex-shrink:0}}
.pend-av img{{width:100%;height:100%;object-fit:cover}}
.pend-info{{flex:1}}
.pend-nome{{font-weight:700;font-size:14px}}
.pend-email{{font-size:12px;color:var(--t2)}}
.pend-btns{{display:flex;gap:6px}}
.btn-ap{{padding:6px 12px;border-radius:8px;border:none;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit}}
.btn-ok{{background:var(--gr);color:#fff}}.btn-no{{background:rgba(255,59,48,.1);color:var(--rd)}}

/* PAPEL DROPDOWN */
.papel-sel{{padding:6px 10px;border-radius:8px;border:1.5px solid var(--b);font-size:13px;font-family:inherit;color:var(--t);background:#fff;cursor:pointer}}
.papel-sel:focus{{outline:none;border-color:var(--bl)}}
.papel-badge{{display:inline-block;font-size:11px;font-weight:700;padding:3px 9px;border-radius:20px}}
.pb-sdr{{background:rgba(50,173,230,.12);color:var(--tl)}}
.pb-cor{{background:rgba(0,113,227,.1);color:var(--bl)}}
.pb-coo{{background:rgba(94,92,230,.12);color:var(--pu)}}

/* SDR METAS GRID */
.sdr-bloco{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:16px 18px;margin-bottom:10px}}
.sdr-nome{{font-size:14px;font-weight:700;margin-bottom:12px;color:var(--t)}}
.sdr-mg{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}}
.sdr-mc{{background:var(--bg);border-radius:8px;padding:8px 6px;text-align:center}}
.sdr-lbl{{font-size:9px;font-weight:700;color:var(--t3);text-transform:uppercase;margin-bottom:4px}}
.sdr-inp{{width:100%;padding:5px 4px;border-radius:6px;border:1px solid var(--b);font-size:13px;font-family:inherit;text-align:center;background:#fff}}
.sdr-inp:focus{{outline:none;border-color:var(--bl)}}

/* CORRETOR META */
.corr-card{{background:var(--sf);border:1px solid var(--b);border-radius:var(--r);box-shadow:var(--sh);padding:14px 18px;margin-bottom:8px;display:flex;align-items:center;gap:14px}}
.corr-nome{{font-weight:700;font-size:14px;flex:1}}
.corr-vals{{display:flex;gap:20px}}
.corr-val{{text-align:center}}
.corr-v{{font-size:16px;font-weight:800;color:var(--bl)}}
.corr-l{{font-size:10px;color:var(--t3);font-weight:700;text-transform:uppercase}}
.vis-bar-bg{{background:rgba(0,0,0,.06);border-radius:6px;height:6px;overflow:hidden}}
.vis-bar-fill{{height:100%;border-radius:6px;background:var(--tl);transition:width .5s}}

/* CONFIG ── */
.ci{{width:100%;padding:11px 13px;border-radius:10px;border:1.5px solid var(--b);font-size:15px;background:#fff;margin-bottom:12px;font-family:inherit;color:var(--t)}}
.ci:focus{{outline:none;border-color:var(--bl)}}
.cl{{display:block;font-size:10px;font-weight:700;color:var(--t3);margin-bottom:5px;text-transform:uppercase;letter-spacing:.07em}}
.cbtn{{background:var(--bl);color:#fff;font-weight:700;border:none;padding:12px;border-radius:10px;cursor:pointer;font-size:15px;font-family:inherit;width:100%}}

/* CALENDÁRIO */
.calh{{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px}}
.caln{{width:33px;height:33px;border-radius:50%;background:var(--bg);border:1px solid var(--b);font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--bl);font-weight:700}}
.calt{{font-size:17px;font-weight:800}}
.calg{{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}}
.cdow{{text-align:center;font-size:10px;font-weight:700;color:var(--t3);padding:5px 0}}
.cday{{aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:8px;font-size:13px;font-weight:600;position:relative;color:var(--t)}}
.cday.outro{{color:var(--t3)}}.cday.hoje{{background:var(--bl);color:#fff}}
.cday.deal{{background:rgba(40,205,65,.1);border:1px solid rgba(40,205,65,.22)}}
.cbdg{{position:absolute;top:1px;right:1px;background:var(--gr);color:#fff;font-size:7px;font-weight:800;border-radius:4px;padding:1px 3px}}
.cday.hoje .cbdg{{background:rgba(255,255,255,.3)}}

@media(max-width:700px){{.kg,.pg,.mg2,.mog,.cg,.mm-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>

<!-- TELA DE AUTENTICAÇÃO -->
<div id="auth-wrap">
<div class="acard">
  <div style="margin-bottom:18px">{logo_big}</div>
  <div class="atabs">
    <button class="atab on" onclick="showTab('login')">Entrar</button>
    <button class="atab" onclick="showTab('register')">Criar conta</button>
  </div>

  <!-- LOGIN -->
  <div class="aform vis" id="form-login">
    <input type="email" id="l-em" class="ainp" placeholder="E-mail" onkeydown="if(event.key==='Enter')$i('l-pw').focus()">
    <input type="password" id="l-pw" class="ainp" placeholder="Senha" onkeydown="if(event.key==='Enter')doLogin()">
    <div class="aerro" id="l-err">E-mail ou senha incorretos</div>
    <button class="abtn" onclick="doLogin()">Entrar</button>
    <div style="font-size:12px;color:var(--t3);margin-top:12px">Demo: qualquer credencial funciona</div>
  </div>

  <!-- CADASTRO -->
  <div class="aform" id="form-register">
    <div class="avatar-upload" id="reg-av-wrap" onclick="$i('reg-photo-inp').click()">
      <div class="placeholder" id="reg-av-placeholder">{ICO["photo"]}</div>
      <img id="reg-av-img" style="display:none">
      <input type="file" id="reg-photo-inp" accept="image/*" onchange="previewRegPhoto(this)" onclick="event.stopPropagation()">
    </div>
    <input type="text" id="r-nome" class="ainp" placeholder="Nome completo">
    <input type="email" id="r-em" class="ainp" placeholder="E-mail">
    <input type="password" id="r-pw" class="ainp" placeholder="Senha">
    <div class="aerro" id="r-err">Preencha todos os campos</div>
    <button class="abtn" onclick="doRegister()">Solicitar acesso</button>
  </div>

  <!-- AGUARDANDO APROVAÇÃO -->
  <div class="aform" id="form-pending">
    <div class="pending-msg">
      ⏳ Sua conta está aguardando aprovação do administrador.<br>
      <span style="font-weight:400;font-size:13px">Você receberá acesso em breve.</span>
    </div>
    <button class="abtn sec" onclick="showTab('login')" style="margin-top:14px">Voltar ao login</button>
  </div>
</div>
</div>

<!-- NAVBAR -->
<div class="navbar">
  <div class="nav-l">
    <div>{logo_nav}</div>
    <div class="nd"></div>
    <div id="nav-pg">KPIs</div>
  </div>
  <div class="nav-r">
    <div class="ppill" id="ppill" onclick="togglePer()">📅 Este ano</div>
    <div class="avatar-btn" id="avatar-btn" onclick="toggleMenu()">
      <img id="nav-avatar-img" style="display:none">
      <span id="nav-avatar-ini">W</span>
      <div class="notif-dot" id="notif-dot"></div>
    </div>
  </div>
</div>

<!-- MENU DROPDOWN -->
<div class="mov" id="mov" onclick="fecharMenu()">
  <div class="msheet" onclick="event.stopPropagation()">
    <div class="mitem on" id="ni-kpis" onclick="ir('kpis')">{ICO["home"]}<span>KPIs</span></div>
    <div class="mitem" id="ni-crm" onclick="ir('crm')">{ICO["crm"]}<span>CRM</span></div>
    <div class="mitem" id="ni-mkt" onclick="ir('mkt')">{ICO["mkt"]}<span>Marketing</span></div>
    <div class="mitem" id="ni-conv" onclick="ir('conv')">{ICO["conv"]}<span>Conversas</span></div>
    <div class="mitem" id="ni-cal" onclick="ir('cal')">{ICO["cal"]}<span>Calendário</span></div>
    <div class="mdiv"></div>
    <div class="mitem" id="ni-perfil" onclick="ir('perfil')">{ICO["user"]}<span>Meu Perfil</span></div>
    <div class="mitem" id="ni-cfg" onclick="ir('cfg')">{ICO["cfg"]}<span>Config (Admin)</span></div>
    <div class="mdiv"></div>
    <div class="mitem" onclick="doLogout()" style="color:var(--rd)">{ICO["x"]}<span>Sair</span></div>
  </div>
</div>

<!-- PERÍODO -->
<div class="psh" id="psh">
  <div class="pshtit">Período <button onclick="$i('psh').classList.remove('vis')">×</button></div>
  <button class="pbtn" onclick="sp('tudo','Tudo',this)">Tudo</button>
  <button class="pbtn" onclick="sp('este_mes','Este mês',this)">Este mês</button>
  <button class="pbtn" onclick="sp('mes_passado','Mês passado',this)">Mês passado</button>
  <button class="pbtn" onclick="sp('30dias','Últimos 30 dias',this)">Últimos 30 dias</button>
  <button class="pbtn on" onclick="sp('este_ano','Este ano',this)">Este ano</button>
  <button class="pbtn" onclick="sp('custom','Personalizado',this)">Personalizado...</button>
  <div class="dts" id="dts">
    <label>De <input type="date" id="dti" onchange="filtrar()"></label>
    <label>Até <input type="date" id="dtf" onchange="filtrar()"></label>
  </div>
</div>

<div class="wrap">
<div class="atu">Dados buscados em {AGORA}</div>

<!-- KPIs -->
<div id="page-kpis" class="page ativa">
  <div class="sec">Indicadores Principais</div>
  <div class="kg">
    <div class="kc hi"><div class="kl">Receita Fechada</div><div class="kv g" id="k-rec">—</div></div>
    <div class="kc"><div class="kl">Pipeline Ativo</div><div class="kv b" id="k-pip">—</div></div>
    <div class="kc"><div class="kl">Negociações Ativas</div><div class="kv" id="k-at">—</div></div>
    <div class="kc"><div class="kl">Leads Marketing</div><div class="kv" id="k-lm">—</div><div class="ks" id="k-lm-s">—</div></div>
    <div class="kc"><div class="kl">Leads CRM</div><div class="kv" id="k-lc">—</div><div class="ks" id="k-lc-s">—</div></div>
    <div class="kc"><div class="kl">Ticket Médio</div><div class="kv" id="k-tk">—</div></div>
    <div class="kc"><div class="kl">Conv. Lead → Agendamento</div><div class="kv b" id="k-la">—</div><div class="ks" id="k-la-s">—</div></div>
    <div class="kc"><div class="kl">Conv. Agendamento → Venda</div><div class="kv" id="k-av">—</div><div class="ks" id="k-av-s">—</div></div>
    <div class="kc"><div class="kl">Conv. Lead → Venda</div><div class="kv" id="k-cv">—</div><div class="ks" id="k-cv-s">—</div></div>
  </div>

  <div class="sec">Previsibilidade</div>
  <div class="pg">
    <div class="pc">
      <div class="pl">Leads p/ 1 Venda</div>
      <div class="pv" id="p-lv">—</div>
      <div class="ps" id="p-lv-sub">conversão histórica</div>
    </div>
    <div class="pc">
      <div class="pl">Vendas Previstas / Mês</div>
      <div class="pv" id="p-vp">—</div>
      <div class="ps" id="p-vp-sub">ativos × conv% ÷ 12</div>
    </div>
    <div class="pc">
      <div class="pl">Receita Prevista / Mês</div>
      <div class="pv" id="p-rp">—</div>
      <div class="ps" id="p-rp-sub">vendas/mês × ticket médio</div>
    </div>
  </div>
  <div style="font-size:11px;color:var(--t3);margin-top:6px;padding:0 2px">
    ↑ Melhora automaticamente conforme a conversão e o pipeline crescem
  </div>

  <div class="sec">Metas do Período</div>
  <div class="mg2">
    <div class="mc"><div class="mt2">Meta VGV</div><div class="mr"><span class="mv" id="vr">—</span><span class="md" id="vd">—</span></div><div class="bb"><div class="bp" id="vb" style="width:0%;background:var(--gr)"></div></div><div class="mp" id="vp">—</div></div>
    <div class="mc"><div class="mt2">Meta Entrada</div><div class="mr"><span class="mv" id="er">—</span><span class="md" id="ed">—</span></div><div class="bb"><div class="bp" id="eb" style="width:0%;background:var(--or)"></div></div><div class="mp" id="ep">—</div></div>
  </div>

  <div class="sec">Pipeline Executivo</div>
  <div class="card"><canvas id="gF" height="155"></canvas></div>

  <div class="sec">Resumo por Módulo</div>
  <div class="mog">
    <div class="moc" style="border-color:var(--bl)"><div class="mot">CRM</div><div class="mon" id="m-c" style="color:var(--bl)">—</div><div class="mol">leads no período</div></div>
    <div class="moc" style="border-color:var(--or)"><div class="mot">Marketing</div><div class="mon" id="m-m" style="color:var(--or)">—</div><div class="mol">contatos MKT</div></div>
    <div class="moc" style="border-color:var(--gr)"><div class="mot">Conversas</div><div class="mon" style="color:var(--gr)">6.681</div><div class="mol">contatos totais</div></div>
  </div>
</div>

<!-- CRM -->
<div id="page-crm" class="page">
  <div class="rc">
    <div class="rci"><div class="kl">Negociações</div><div class="kv b" id="ct">—</div></div>
    <div class="rci"><div class="kl">Valor Total</div><div class="kv" id="cv2">—</div></div>
  </div>
  <div class="cg">
    <div class="cc"><div class="ct">Negociações por etapa</div><canvas id="gCE"></canvas></div>
    <div class="cc"><div class="ct">Valor por etapa (%)</div><canvas id="gCV"></canvas></div>
  </div>
  <div class="sec">Operadores</div>
  <div class="card"><table class="tbl">
    <thead><tr><th>Operador</th><th>Leads</th><th>% Agendamento</th><th>% Fechamento</th><th>VGV Total</th></tr></thead>
    <tbody id="cop"></tbody>
  </table></div>
  <div class="sec">Progresso em Visitas Realizadas (Atendimento Realizado)</div>
  <div class="card"><table class="tbl"><thead><tr><th>Operador</th><th>Visitas</th><th>Progresso vs. total</th></tr></thead><tbody id="cvis"></tbody></table></div>
</div>

<!-- MARKETING -->
<div id="page-mkt" class="page">
  <div class="rc">
    <div class="rci"><div class="kl">Leads no período</div><div class="kv" id="mt">—</div></div>
    <div class="rci"><div class="kl">Gasto Total</div><div class="kv" id="mg3">—</div></div>
    <div class="rci"><div class="kl">CPL médio</div><div class="kv" id="mcpl">—</div></div>
  </div>
  <div class="sec">Por Campanha</div>
  <div class="card"><table class="tbl"><thead><tr><th>Campanha</th><th>Leads</th><th>Gasto</th><th>CPL</th><th style="min-width:110px">% total</th></tr></thead><tbody id="mca"></tbody></table></div>
</div>

<!-- CONVERSAS -->
<div id="page-conv" class="page">
  <div class="kg" style="grid-template-columns:1fr 1fr;margin-bottom:4px">
    <div class="kc"><div class="kl">Contatos cadastrados</div><div class="kv b">6.681</div></div>
    <div class="kc"><div class="kl">Conv. Lead → Agendamento</div><div class="kv" id="cag">—</div></div>
  </div>
  <div class="sec">🏆 Top Fechadores</div>
  <div class="card"><table class="tbl"><thead><tr><th>Operador</th><th>Vendas</th><th>VGV Total</th></tr></thead><tbody id="tfch"></tbody></table></div>
  <div class="sec">📅 Top Agendadores</div>
  <div class="card"><table class="tbl"><thead><tr><th>Operador</th><th>Agendamentos</th><th>Taxa</th></tr></thead><tbody id="tag2"></tbody></table></div>
  <div class="sec" style="color:var(--rd)">❌ Mais Perdas</div>
  <div class="card"><table class="tbl danger"><thead><tr><th>Operador</th><th>Perdas</th><th>% dos seus leads</th></tr></thead><tbody id="tpd"></tbody></table></div>
  <div class="sec" style="color:var(--rd)">📉 Menos Convertem (Lead → Venda)</div>
  <div class="card"><table class="tbl danger"><thead><tr><th>Operador</th><th>Conv.</th><th>Vendas / Total leads</th></tr></thead><tbody id="tmc"></tbody></table></div>
</div>

<!-- CALENDÁRIO -->
<div id="page-cal" class="page">
  <div class="card"><div class="calh"><button class="caln" onclick="calMov(-1)">‹</button><span class="calt" id="calt">—</span><button class="caln" onclick="calMov(1)">›</button></div><div class="calg" id="calg"></div></div>
</div>

<!-- PERFIL -->
<div id="page-perfil" class="page">
  <div class="card" style="max-width:480px">
    <div style="font-size:17px;font-weight:800;margin-bottom:18px">Meu Perfil</div>
    <div class="perfil-wrap">
      <div class="perfil-avatar" id="pf-av" onclick="$i('pf-photo').click()">
        <img id="pf-av-img" style="display:none">
        <span id="pf-av-ini">W</span>
        <input type="file" id="pf-photo" accept="image/*" onchange="updateProfilePhoto(this)" onclick="event.stopPropagation()">
      </div>
      <div class="perfil-dados">
        <label class="cl">Nome completo</label>
        <input type="text" id="pf-nome" class="ci" placeholder="Seu nome">
        <label class="cl">E-mail</label>
        <input type="email" id="pf-email" class="ci" placeholder="seu@email.com" readonly style="opacity:.6">
        <label class="cl">Cargo</label>
        <input type="text" id="pf-cargo" class="ci" placeholder="Ex: Gerente Comercial">
        <button class="cbtn" onclick="salvarPerfil()" style="margin-top:4px">Salvar perfil</button>
        <div id="pf-ok" style="color:var(--gr);font-weight:700;font-size:13px;margin-top:8px;display:none">✅ Salvo!</div>
      </div>
    </div>
  </div>
</div>

<!-- CONFIG (Admin) -->
<div id="page-cfg" class="page">
  <!-- Usuários pendentes -->
  <div class="sec">Solicitações de Acesso</div>
  <div id="pendentes-wrap">
    <div style="color:var(--t3);font-size:14px;padding:12px 0">Nenhuma solicitação pendente.</div>
  </div>

  <!-- Equipe: papéis -->
  <div class="sec">Equipe — Papéis</div>
  <div style="font-size:12px;color:var(--t2);margin-bottom:10px">Defina o papel de cada operador detectado no CRM.</div>
  <div class="card" style="padding:0;overflow:hidden">
    <table class="tbl" id="eq-table">
      <thead><tr><th>Operador</th><th>Papel</th><th>Tipo</th></tr></thead>
      <tbody id="eq-tbody"></tbody>
    </table>
  </div>

  <!-- SDR: metas de agendamentos mensais -->
  <div class="sec">SDRs — Meta de Agendamentos por Mês</div>
  <div style="font-size:12px;color:var(--t2);margin-bottom:10px">Quantos agendamentos realizados cada SDR deve atingir por mês.</div>
  <div id="sdr-metas-wrap">
    <div style="color:var(--t3);font-size:14px;padding:8px 0">Nenhum SDR definido ainda.</div>
  </div>

  <!-- Corretores/Coordenadoras: metas divididas igualmente -->
  <div class="sec">Corretores / Coordenadoras — Meta Individual</div>
  <div style="font-size:12px;color:var(--t2);margin-bottom:10px">VGV e Entrada mensais divididos igualmente entre Corretores e Coordenadoras.</div>
  <div id="corr-metas-wrap">
    <div style="color:var(--t3);font-size:14px;padding:8px 0">Nenhum Corretor ou Coordenadora definido ainda.</div>
  </div>

  <!-- Metas mensais globais -->
  <div class="sec">Metas Mensais Globais — VGV e Entrada (R$)</div>
  <div style="font-size:12px;color:var(--t2);margin-bottom:12px">Total da empresa por mês. Dividido automaticamente entre os Corretores e Coordenadoras.</div>
  <div class="mm-grid" id="mm-grid"></div>

  <button class="cbtn" onclick="salvarTudo()" style="margin-top:16px;max-width:260px">Salvar todas as configurações</button>
  <div id="mm-ok" style="color:var(--gr);font-weight:700;font-size:13px;margin-top:10px;display:none">✅ Salvo!</div>
</div>
</div>

<script>
Chart.register(ChartDataLabels);
const CRM={CRM_JS}, MKT={MKT_JS}, EMP={EMP_JS};
const CG={CAMP_GASTO_JS}, CL={CAMP_LEADS_JS};
const CONV_TOTAL={CONV_TOTAL_N};
const VGV0={META_VGV}, ENT0={META_ENT};
const MESES=[{",".join(f'"{m}"' for m in MESES_NOMES)}];
const DEFAULT_GOALS={MESES_GOALS_DEFAULT};
const ORDEM=["LEADS","EM CONTATO","AGENDAMENTO","ATENDIMENTO REALIZADO","NEGOCIAÇÃO","FECHAMENTO"];
const NOMES={{kpis:"KPIs",crm:"CRM",mkt:"Marketing",conv:"Conversas",cal:"Calendário",perfil:"Meu Perfil",cfg:"Config (Admin)"}};
const ADMIN_EMAIL="watson@imincorporadora.com.br";

let periodo="este_ano", calAno=new Date().getFullYear(), calMes=new Date().getMonth();
let fcArr=[], cF,cCE,cCV;
let currentUser=null;

function $i(id){{return document.getElementById(id)}}

// ── AUTH ──────────────────────────────────────────────────────
function getUsers(){{return JSON.parse(localStorage.getItem("im_users")||"[]")}}
function saveUsers(u){{localStorage.setItem("im_users",JSON.stringify(u))}}

function showTab(t){{
  document.querySelectorAll(".aform").forEach(f=>f.classList.remove("vis"));
  document.querySelectorAll(".atab").forEach(b=>b.classList.remove("on"));
  $i("form-"+t).classList.add("vis");
  document.querySelectorAll(".atab")[t==="login"?0:1]?.classList.add("on");
}}

function previewRegPhoto(inp){{
  const f=inp.files[0]; if(!f) return;
  const r=new FileReader();
  r.onload=e=>{{
    $i("reg-av-img").src=e.target.result;
    $i("reg-av-img").style.display="block";
    $i("reg-av-placeholder").style.display="none";
  }};
  r.readAsDataURL(f);
}}

function doRegister(){{
  const nome=$i("r-nome").value.trim(),em=$i("r-em").value.trim(),pw=$i("r-pw").value;
  if(!nome||!em||!pw){{$i("r-err").style.display="block";return;}}
  $i("r-err").style.display="none";
  const photo=$i("reg-av-img").src||"";
  const users=getUsers();
  if(users.find(u=>u.email===em)){{$i("r-err").textContent="E-mail já cadastrado.";$i("r-err").style.display="block";return;}}
  users.push({{id:Date.now(),name:nome,email:em,pw:btoa(pw),photo,status:"pending",registered_at:new Date().toISOString()}});
  saveUsers(users);
  document.querySelectorAll(".aform").forEach(f=>f.classList.remove("vis"));
  $i("form-pending").classList.add("vis");
  document.querySelectorAll(".atab").forEach(b=>b.classList.remove("on"));
}}

function doLogin(){{
  const em=$i("l-em").value.trim(), pw=$i("l-pw").value;
  if(!em||!pw){{$i("l-err").style.display="block";return;}}
  $i("l-err").style.display="none";
  // Admin pode sempre entrar
  if(em===ADMIN_EMAIL){{ loginAs({{id:"admin",name:"Watson Slonski",email:ADMIN_EMAIL,photo:"",status:"approved",pw:""}}); return; }}
  // Demo: qualquer credencial funciona (ou checa lista real)
  const users=getUsers();
  const u=users.find(x=>x.email===em);
  if(u){{
    if(u.status!=="approved"){{$i("l-err").textContent="Acesso aguardando aprovação.";$i("l-err").style.display="block";return;}}
    loginAs(u);
  }} else {{
    // Demo: login livre
    loginAs({{id:"demo",name:em.split("@")[0],email:em,photo:"",status:"approved"}});
  }}
}}

function loginAs(u){{
  currentUser=u;
  localStorage.setItem("im_current",JSON.stringify(u));
  const w=$i("auth-wrap");
  w.classList.add("gone");
  setTimeout(()=>{{w.style.display="none"; initUI(); filtrar();}},360);
}}

function doLogout(){{
  currentUser=null;
  localStorage.removeItem("im_current");
  location.reload();
}}

function initUI(){{
  // Avatar no navbar
  if(currentUser?.photo){{
    $i("nav-avatar-img").src=currentUser.photo;
    $i("nav-avatar-img").style.display="block";
    $i("nav-avatar-ini").style.display="none";
  }} else {{
    $i("nav-avatar-ini").textContent=(currentUser?.name||"W")[0].toUpperCase();
  }}
  // Config sempre visível (sem sistema de login ativo)
  if($i("ni-cfg")) $i("ni-cfg").style.display="flex";
  // Pendentes
  renderPendentes();
  // Metas mensais
  renderMM();
  // Preenche perfil
  $i("pf-nome").value=currentUser?.name||"";
  $i("pf-email").value=currentUser?.email||"";
  if(currentUser?.photo){{
    $i("pf-av-img").src=currentUser.photo;
    $i("pf-av-img").style.display="block";
    $i("pf-av-ini").style.display="none";
  }} else {{
    $i("pf-av-ini").textContent=(currentUser?.name||"W")[0].toUpperCase();
  }}
}}

// ── APROVAÇÃO ──────────────────────────────────────────────────
function renderPendentes(){{
  const users=getUsers(), pend=users.filter(u=>u.status==="pending");
  const wrap=$i("pendentes-wrap"); wrap.innerHTML="";
  if(!pend.length){{wrap.innerHTML='<div style="color:var(--t3);font-size:14px;padding:12px 0">Nenhuma solicitação pendente.</div>';return;}}
  $i("notif-dot").classList.add("vis");
  pend.forEach(u=>{{
    const av=u.photo?`<img src="${{u.photo}}">`:u.name[0].toUpperCase();
    wrap.innerHTML+=`<div class="pend-card">
      <div class="pend-av">${{u.photo?`<img src="${{u.photo}}" style="width:100%;height:100%;object-fit:cover;border-radius:50%">`:u.name[0].toUpperCase()}}</div>
      <div class="pend-info"><div class="pend-nome">${{u.name}}</div><div class="pend-email">${{u.email}}</div></div>
      <div class="pend-btns">
        <button class="btn-ap btn-ok" onclick="aprovar(${{u.id}},true)">Aprovar</button>
        <button class="btn-ap btn-no" onclick="aprovar(${{u.id}},false)">Negar</button>
      </div>
    </div>`;
  }});
}}

function aprovar(id,ok2){{
  const users=getUsers();
  const u=users.find(x=>x.id===id);
  if(u) u.status=ok2?"approved":"denied";
  saveUsers(users);
  renderPendentes();
  if(getUsers().filter(u=>u.status==="pending").length===0) $i("notif-dot").classList.remove("vis");
}}

// ── METAS MENSAIS ──────────────────────────────────────────────
// Detecta todos os operadores únicos do CRM
function getOperadores(){{return [...new Set(CRM.map(d=>d.user||"").filter(Boolean))].sort();}}

// Equipe: papéis
function getEquipe(){{return JSON.parse(localStorage.getItem("im_equipe")||"{{}}");}}
function saveEquipe(e){{localStorage.setItem("im_equipe",JSON.stringify(e));}}
function getMetas(){{return JSON.parse(localStorage.getItem("im_goals_"+new Date().getFullYear())||JSON.stringify(DEFAULT_GOALS));}}

function renderEquipe(){{
  const ops=getOperadores(),eq=getEquipe(),tb=$i("eq-tbody");tb.innerHTML="";
  ops.forEach(op=>{{
    const papel=eq[op]?.role||"";
    const badge=papel==="sdr"?'<span class="papel-badge pb-sdr">SDR</span>':papel==="corretor"?'<span class="papel-badge pb-cor">Corretor</span>':papel==="coordenadora"?'<span class="papel-badge pb-coo">Coordenadora</span>':"—";
    tb.innerHTML+=`<tr><td style="font-weight:600">${{op}}</td>
      <td><select class="papel-sel" id="role-${{op.replace(/ /g,'_')}}" onchange="atualizarEquipe()">
        <option value="" ${{!papel?"selected":""}}>— não definido —</option>
        <option value="sdr" ${{papel==="sdr"?"selected":""}}>SDR</option>
        <option value="corretor" ${{papel==="corretor"?"selected":""}}>Corretor</option>
        <option value="coordenadora" ${{papel==="coordenadora"?"selected":""}}>Coordenadora de Vendas</option>
      </select></td><td>${{badge}}</td></tr>`;
  }});
}}

function atualizarEquipe(){{
  const ops=getOperadores(),eq=getEquipe();
  ops.forEach(op=>{{const sel=$i("role-"+op.replace(/ /g,"_"));if(sel)eq[op]={{role:sel.value}};}});
  saveEquipe(eq);renderSDRMetas();renderCorrMetas();
}}

// SDR metas
function getSDRMetas(){{return JSON.parse(localStorage.getItem("im_sdr_metas")||"{{}}");}}
function renderSDRMetas(){{
  const eq=getEquipe(),sdrs=Object.entries(eq).filter(([,v])=>v.role==="sdr").map(([k])=>k);
  const metas=getSDRMetas(),wrap=$i("sdr-metas-wrap");wrap.innerHTML="";
  if(!sdrs.length){{wrap.innerHTML='<div style="color:var(--t3);font-size:14px;padding:8px 0">Nenhum SDR definido ainda.</div>';return;}}
  sdrs.forEach(sdr=>{{
    const m=metas[sdr]||{{}};
    let grid="";
    for(let i=1;i<=12;i++){{
      grid+=`<div class="sdr-mc"><div class="sdr-lbl">${{MESES[i-1].substring(0,3)}}</div>
        <input type="number" class="sdr-inp" id="sdr-${{sdr.replace(/ /g,'_')}}-${{i}}" value="${{m[i]||30}}" min="0"></div>`;
    }}
    wrap.innerHTML+=`<div class="sdr-bloco"><div class="sdr-nome">📞 ${{sdr}} — Agendamentos / mês</div><div class="sdr-mg">${{grid}}</div></div>`;
  }});
}}

// Corretor/Coordenadora — meta dividida igualmente
function renderCorrMetas(){{
  const eq=getEquipe(),goals=getMetas();
  const corr=Object.entries(eq).filter(([,v])=>v.role==="corretor"||v.role==="coordenadora").map(([k,v])=>{{return{{name:k,tipo:v.role}};}});
  const wrap=$i("corr-metas-wrap");wrap.innerHTML="";
  if(!corr.length){{wrap.innerHTML='<div style="color:var(--t3);font-size:14px;padding:8px 0">Nenhum Corretor ou Coordenadora definido.</div>';return;}}
  const mes=new Date().getMonth()+1;
  const gMes=goals[mes]||{{vgv:VGV0/12,ent:ENT0/12}};
  const n=corr.length,vgvInd=n>0?(gMes.vgv/n):0,entInd=n>0?(gMes.ent/n):0;
  wrap.innerHTML=`<div style="font-size:12px;color:var(--t2);margin-bottom:10px">
    Mês atual — ${{MESES[mes-1]}}: VGV total <strong>${{R0(gMes.vgv)}}</strong> ÷ ${{n}} pessoas = <strong style="color:var(--bl)">${{R0(vgvInd)}} cada</strong>
  </div>`;
  corr.forEach(c=>{{
    const badge=c.tipo==="coordenadora"?'<span class="papel-badge pb-coo">Coordenadora</span>':'<span class="papel-badge pb-cor">Corretor</span>';
    wrap.innerHTML+=`<div class="corr-card">
      <div class="corr-nome">${{c.name}} ${{badge}}</div>
      <div class="corr-vals">
        <div class="corr-val"><div class="corr-v">${{R0(vgvInd)}}</div><div class="corr-l">Meta VGV/mês</div></div>
        <div class="corr-val"><div class="corr-v">${{R0(entInd)}}</div><div class="corr-l">Meta Entrada/mês</div></div>
      </div>
    </div>`;
  }});
}}

function renderMM(){{
  const goals=getMetas(),g=$i("mm-grid");g.innerHTML="";
  for(let i=1;i<=12;i++){{
    const m=goals[i]||{{vgv:0,ent:0}};
    g.innerHTML+=`<div class="mm-card">
      <div class="mm-mes">${{MESES[i-1].substring(0,3)}}</div>
      <div class="mm-lbl">VGV</div>
      <input type="number" id="mm-vgv-${{i}}" class="mm-inp" value="${{m.vgv}}" step="1000" onchange="renderCorrMetas()">
      <div class="mm-lbl">Entrada</div>
      <input type="number" id="mm-ent-${{i}}" class="mm-inp" value="${{m.ent}}" step="1000">
    </div>`;
  }}
}}

function salvarTudo(){{
  atualizarEquipe();
  // SDR metas
  const eq=getEquipe(),sdrs=Object.entries(eq).filter(([,v])=>v.role==="sdr").map(([k])=>k);
  const sdrM=getSDRMetas();
  sdrs.forEach(sdr=>{{sdrM[sdr]={{}};for(let i=1;i<=12;i++){{const inp=$i("sdr-"+sdr.replace(/ /g,"_")+"-"+i);if(inp)sdrM[sdr][i]=parseInt(inp.value)||0;}}}});
  localStorage.setItem("im_sdr_metas",JSON.stringify(sdrM));
  // Metas globais
  const goals={{}};
  for(let i=1;i<=12;i++){{goals[i]={{vgv:parseFloat($i("mm-vgv-"+i)?.value)||0,ent:parseFloat($i("mm-ent-"+i)?.value)||0}};}}
  localStorage.setItem("im_goals_"+new Date().getFullYear(),JSON.stringify(goals));
  $i("mm-ok").style.display="block";setTimeout(()=>$i("mm-ok").style.display="none",2500);
  filtrar();
}}

// ── PERFIL ──────────────────────────────────────────────────────
function updateProfilePhoto(inp){{
  const f=inp.files[0]; if(!f) return;
  const r=new FileReader();
  r.onload=e=>{{
    $i("pf-av-img").src=e.target.result; $i("pf-av-img").style.display="block"; $i("pf-av-ini").style.display="none";
    $i("nav-avatar-img").src=e.target.result; $i("nav-avatar-img").style.display="block"; $i("nav-avatar-ini").style.display="none";
  }};
  r.readAsDataURL(f);
}}
function salvarPerfil(){{
  if(currentUser){{currentUser.name=$i("pf-nome").value;currentUser.cargo=$i("pf-cargo").value;}}
  $i("pf-ok").style.display="block"; setTimeout(()=>$i("pf-ok").style.display="none",2500);
}}

// ── NAV ──────────────────────────────────────────────────────────
function ir(id){{
  document.querySelectorAll(".page").forEach(p=>p.classList.remove("ativa"));
  document.querySelectorAll(".mitem").forEach(n=>n.classList.remove("on"));
  $i("page-"+id).classList.add("ativa");
  $i("ni-"+id)?.classList.add("on");
  $i("nav-pg").textContent=NOMES[id]||id;
  $i("psh").classList.remove("vis");
  fecharMenu();
  if(id==="cal") renderCal();
  if(id==="cfg"){{ renderPendentes(); renderEquipe(); renderSDRMetas(); renderCorrMetas(); renderMM(); }}
}}
function toggleMenu(){{$i("mov").classList.toggle("vis");$i("psh").classList.remove("vis");}}
function fecharMenu(){{$i("mov").classList.remove("vis");}}
function togglePer(){{$i("psh").classList.toggle("vis");fecharMenu();}}
document.addEventListener("click",e=>{{if(!$i("psh").contains(e.target)&&!$i("ppill").contains(e.target))$i("psh").classList.remove("vis");}});
function sp(v,lbl,el){{
  periodo=v;document.querySelectorAll(".pbtn").forEach(b=>b.classList.remove("on"));el.classList.add("on");
  $i("ppill").textContent="📅 "+lbl;$i("dts").classList.toggle("vis",v==="custom");
  if(v!=="custom"){{$i("psh").classList.remove("vis");filtrar();}}
}}

// ── DATAS ──────────────────────────────────────────────────────
function intervalo(){{
  const h=new Date(),hoje=new Date(h.getFullYear(),h.getMonth(),h.getDate());
  let i=null,f=null;
  if(periodo==="tudo") return{{i:null,f:null}};
  if(periodo==="este_mes"){{i=new Date(hoje.getFullYear(),hoje.getMonth(),1);f=new Date(hoje.getFullYear(),hoje.getMonth()+1,0,23,59,59);}}
  else if(periodo==="mes_passado"){{i=new Date(hoje.getFullYear(),hoje.getMonth()-1,1);f=new Date(hoje.getFullYear(),hoje.getMonth(),0,23,59,59);}}
  else if(periodo==="30dias"){{i=new Date(hoje.getTime()-30*24*60*60*1e3);f=new Date(hoje.getFullYear(),hoje.getMonth(),hoje.getDate(),23,59,59);}}
  else if(periodo==="este_ano"){{i=new Date(hoje.getFullYear(),0,1);f=new Date(hoje.getFullYear(),11,31,23,59,59);}}
  else if(periodo==="custom"){{const a=$i("dti").value,b=$i("dtf").value;i=a?new Date(a+"T00:00:00"):null;f=b?new Date(b+"T23:59:59"):null;}}
  return{{i,f}};
}}
function ok(ds,i,f){{
  if(!i&&!f) return true; if(!ds) return false;
  const p=ds.split("-"); if(p.length<3) return false;
  const d=new Date(parseInt(p[0]),parseInt(p[1])-1,parseInt(p[2]));
  if(i&&d<i) return false; if(f&&d>f) return false; return true;
}}
const R=v=>"R$ "+v.toLocaleString("pt-BR",{{minimumFractionDigits:2,maximumFractionDigits:2}});
const R0=v=>"R$ "+Math.round(v).toLocaleString("pt-BR");
function ord(e){{const n=e.toUpperCase();for(let i=0;i<ORDEM.length;i++) if(n.includes(ORDEM[i])) return i; return 99;}}
function metas(){{
  const goals=getMetas(), mes=new Date().getMonth()+1;
  const g=goals[mes]||{{vgv:VGV0/12,ent:ENT0/12}};
  return{{vgv:g.vgv||VGV0/12,ent:g.ent||ENT0/12,entR:parseFloat(localStorage.getItem("im_entr"))||0}};
}}

// ── FILTRAR ────────────────────────────────────────────────────
function filtrar(){{
  const{{i,f}}=intervalo();
  const deals=CRM.filter(d=>ok(d.created_at,i,f));
  let at=0,pv=0,rec=0,vnd=0;
  const pe={{}},ve={{}},pu={{}},pvu={{}},ppd={{}},pag={{}},pvis={{}};
  deals.forEach(d=>{{
    const eu=d.stage.toUpperCase(),g=eu.includes("FECHA"),p=eu.includes("PERDID"),a=eu.includes("AGEND")||eu.includes("ATEND")||eu.includes("NEGOC"),vis=eu.includes("ATEND");
    pe[d.stage]=(pe[d.stage]||0)+1;ve[d.stage]=(ve[d.stage]||0)+d.value;
    if(g){{vnd++;rec+=d.value;}}else if(!p){{at++;pv+=d.value;}}
    const u=d.user||"—";pu[u]=(pu[u]||0)+1;pvu[u]=(pvu[u]||0)+d.value;
    if(p)ppd[u]=(ppd[u]||0)+1;
    if(a||g)pag[u]=(pag[u]||0)+1;
    if(vis)pvis[u]=(pvis[u]||0)+1;
  }});
  const tk=vnd>0?rec/vnd:0;
  const ef=Object.keys(pe).filter(e=>!e.toUpperCase().includes("PERDID"));
  ef.sort((a,b)=>ord(a)-ord(b));
  const fq=ef.map(e=>pe[e]),fv=ef.map(e=>ve[e]);
  const fp=fq[0]||1; fcArr=fq.map(q=>Math.round(q/fp*1000)/10);
  const mf=MKT.filter(c=>ok(c.created_at,i,f)), lds=deals.length;
  const ETPOS=["AGENDAMENTO","ATENDIMENTO REALIZADO","NEGOCIAÇÃO","FECHAMENTO"];
  const posAg=deals.filter(d=>{{const eu=d.stage.toUpperCase();return!eu.includes("PERDID")&&ETPOS.some(e=>eu.includes(e));}}).length;
  const pctCV=lds>0?(vnd/lds*100):0,pctLA=lds>0?(posAg/lds*100):0,pctAV=posAg>0?(vnd/posAg*100):0;

  // ── Previsibilidade ─────────────────────────────────────────────────────
  // FÓRMULA: total_leads × % conv_lead_venda ÷ 12 = previsão do mês seguinte
  // Aplica-se a: vendas previstas, receita prevista e leads necessários
  const todosDeals  = CRM;
  const todasVendas = todosDeals.filter(d=>d.stage.toUpperCase().includes("FECHA"));
  const todosAtivos = todosDeals.filter(d=>!d.stage.toUpperCase().includes("FECHA")&&!d.stage.toUpperCase().includes("PERDID"));
  const recTotalCRM = todasVendas.reduce((a,d)=>a+d.value,0);
  const tkGlobal    = todasVendas.length>0 ? recTotalCRM/todasVendas.length : 0;

  // Base total: todos os leads recebidos (fechados + perdidos + em andamento)
  // Usa CONV_TOTAL (Conversas) pois é o funil real completo
  const baseLeads = CONV_TOTAL || todosDeals.length;

  // % de vendas realizadas = vendas ÷ base total de leads
  const convRate = baseLeads>0 ? todasVendas.length/baseLeads : 0;
  const convPct  = (convRate*100).toFixed(2);

  // 1. Leads p/ 1 venda = base total ÷ vendas realizadas
  //    = quantos leads precisamos gerar pra fechar 1 venda
  const lpv = todasVendas.length>0 ? Math.ceil(baseLeads/todasVendas.length) : 0;

  // 2. Vendas previstas/mês = (base × % conv) ÷ 12
  //    matematicamente = total_vendas ÷ 12
  const vp2 = (baseLeads * convRate) / 12;

  // 3. Receita prevista/mês = vendas previstas × ticket médio
  //    matematicamente = receita total ÷ 12
  const rp = vp2 * tkGlobal;
  const{{vgv,ent,entR}}=metas();
  const pVgv=Math.min(rec/vgv*100,100),pEnt=Math.min(entR/ent*100,100);

  // DOM KPIs
  $i("k-rec").textContent=R(rec);$i("k-pip").textContent=R(pv);$i("k-at").textContent=at.toLocaleString("pt-BR");
  $i("k-lm").textContent=mf.length.toLocaleString("pt-BR");$i("k-lm-s").textContent=lds>0?(mf.length/lds*100).toFixed(1)+"% do CRM":"—";
  $i("k-lc").textContent=lds.toLocaleString("pt-BR");$i("k-lc-s").textContent=mf.length>0?(lds/mf.length*100).toFixed(1)+"% do MKT":"—";
  $i("k-tk").textContent=R(tk);
  $i("k-la").textContent=pctLA.toFixed(1)+"%";$i("k-la-s").textContent=posAg+" agendamentos";
  $i("k-av").textContent=pctAV.toFixed(1)+"%";$i("k-av-s").textContent=vnd+" vendas";
  $i("k-cv").textContent=pctCV.toFixed(2)+"%";$i("k-cv-s").textContent=vnd+" de "+lds;
  // DOM previsibilidade
  $i("p-lv").textContent=lpv>0?lpv+" leads":"—";
  $i("p-lv-sub").textContent=baseLeads.toLocaleString("pt-BR")+" ÷ "+todasVendas.length+" vendas = "+convPct+"%";
  $i("p-vp").textContent=vp2>0?vp2.toFixed(1)+"/mês":"—";
  $i("p-vp-sub").textContent=baseLeads.toLocaleString("pt-BR")+" × "+convPct+"% ÷ 12";
  $i("p-rp").textContent=rp>0?R0(rp):"—";
  $i("p-rp-sub").textContent=vp2.toFixed(1)+" vendas × "+R0(tkGlobal)+" ticket";
  $i("vr").textContent=R(rec);$i("vd").textContent="de "+R(vgv);$i("vb").style.width=pVgv.toFixed(1)+"%";$i("vp").textContent=pVgv.toFixed(1)+"% atingido";
  $i("er").textContent=R(entR);$i("ed").textContent="de "+R(ent);$i("eb").style.width=pEnt.toFixed(1)+"%";$i("ep").textContent=pEnt.toFixed(1)+"% atingido";
  $i("m-c").textContent=lds.toLocaleString("pt-BR");$i("m-m").textContent=mf.length.toLocaleString("pt-BR");

  // CRM
  $i("ct").textContent=lds.toLocaleString("pt-BR");$i("cv2").textContent=R(deals.reduce((a,d)=>a+d.value,0));
  const tot=deals.length||1,cop=$i("cop");cop.innerHTML="";
  const ETPOS=["AGENDAMENTO","ATENDIMENTO REALIZADO","NEGOCIAÇÃO","FECHAMENTO"];
  Object.entries(pu).sort((a,b)=>b[1]-a[1]).forEach(([u,cnt])=>{{
    const agOp=deals.filter(d=>d.user===u&&ETPOS.some(e=>d.stage.toUpperCase().includes(e))&&!d.stage.toUpperCase().includes("PERDID")).length;
    const fchOp=deals.filter(d=>d.user===u&&d.stage.toUpperCase().includes("FECHA")).length;
    const pctAg=cnt>0?(agOp/cnt*100).toFixed(0)+"%" :"—";
    const pctFch=cnt>0?(fchOp/cnt*100).toFixed(0)+"%" :"—";
    const corAg=agOp/cnt>=0.3?"var(--gr)":agOp/cnt>=0.15?"var(--or)":"var(--rd)";
    const corFch=fchOp/cnt>=0.1?"var(--gr)":fchOp/cnt>=0.05?"var(--or)":"var(--rd)";
    cop.innerHTML+=`<tr>
      <td style="font-weight:600">${{u}}</td>
      <td class="tn">${{cnt}}</td>
      <td style="font-weight:700;color:${{corAg}}">${{pctAg}}</td>
      <td style="font-weight:700;color:${{corFch}}">${{pctFch}}</td>
      <td>${{R(pvu[u]||0)}}</td>
    </tr>`;
  }});

  // Progresso visitas
  const maxVis=Math.max(...Object.values(pvis),1),cvis=$i("cvis");cvis.innerHTML="";
  Object.entries(pvis).sort((a,b)=>b[1]-a[1]).forEach(([u,cnt])=>{{
    const pct=(cnt/maxVis*100).toFixed(0);
    cvis.innerHTML+=`<tr><td style="font-weight:600">${{u}}</td><td class="tn">${{cnt}}</td><td style="min-width:120px"><div class="vis-bar-wrap"><div class="vis-bar-bg"><div class="vis-bar-fill" style="width:${{pct}}%"></div></div></div></td></tr>`;
  }});
  if(!Object.keys(pvis).length) cvis.innerHTML='<tr><td colspan="3" style="color:var(--t3);padding:14px 12px">Sem dados no período</td></tr>';

  // Marketing
  const totG=Object.values(CG).reduce((a,b)=>a+b,0),totL=Object.values(CL).reduce((a,b)=>a+b,0)||1;
  $i("mt").textContent=mf.length.toLocaleString("pt-BR");$i("mg3").textContent=R(totG);$i("mcpl").textContent=mf.length>0&&totG>0?R(totG/mf.length):"—";
  const mc=$i("mca");mc.innerHTML="";
  Object.entries(CL).sort((a,b)=>b[1]-a[1]).forEach(([nome,qtd])=>{{
    const g=CG[nome]||0,cpl=qtd>0&&g>0?R(g/qtd):"—",pct=(qtd/totL*100).toFixed(1);
    mc.innerHTML+=`<tr><td style="font-weight:600;font-size:12px">${{nome}}</td><td class="tn">${{qtd}}</td><td>${{g>0?R(g):"—"}}</td><td>${{cpl}}</td><td style="color:var(--t3)">${{pct}}%<div class="cbar"><div class="cfill" style="width:${{pct}}%"></div></div></td></tr>`;
  }});

  // Conversas tops
  function rTop(id,entries,c3,danger){{
    const tb=$i(id);tb.innerHTML="";
    const bgs=danger?["badge-rd","badge-rd","badge-rd"]:["","",""];
    entries.slice(0,5).forEach(([u,cnt],idx)=>{{
      const stars=["🥇","🥈","🥉"];
      const star=idx<3&&!danger?`<span style="margin-left:4px">${{stars[idx]}}</span>`:"";
      const rd_mark=danger&&idx<2?`<span class="badge-rd">⚠</span>`:"";
      tb.innerHTML+=`<tr><td style="font-weight:600">${{u}}${{star}}${{rd_mark}}</td><td class="tn">${{cnt}}</td><td>${{c3(u,cnt)}}</td></tr>`;
    }});
    if(!entries.length)tb.innerHTML='<tr><td colspan="3" style="color:var(--t3);padding:14px 12px">Sem dados</td></tr>';
  }}
  const fchMap={{}};deals.filter(d=>d.stage.toUpperCase().includes("FECHA")).forEach(d=>{{fchMap[d.user]=(fchMap[d.user]||0)+1;}});
  rTop("tfch",Object.entries(fchMap).sort((a,b)=>b[1]-a[1]),u=>R(pvu[u]||0),false);
  rTop("tag2",Object.entries(pag).sort((a,b)=>b[1]-a[1]),(u,cnt)=>{{const t=pu[u]||1;return(cnt/t*100).toFixed(0)+"%";}},false);
  rTop("tpd",Object.entries(ppd).sort((a,b)=>b[1]-a[1]),(u,cnt)=>{{const t=pu[u]||1;return(cnt/t*100).toFixed(0)+"% dos leads";}},true);

  // Menos convertem
  const convMap={{}};
  Object.keys(pu).forEach(u=>{{const v=vnd>0&&pu[u]>0?deals.filter(d=>d.user===u&&d.stage.toUpperCase().includes("FECHA")).length/pu[u]*100:0;convMap[u]=v;}});
  const mcList=Object.entries(convMap).sort((a,b)=>a[1]-b[1]);
  rTop("tmc",mcList,(u,v)=>{{const vd2=deals.filter(d=>d.user===u&&d.stage.toUpperCase().includes("FECHA")).length;return vd2+" / "+pu[u]+" leads";}},true);

  $i("cag").textContent=pctLA.toFixed(1)+"% ("+posAg+" agend.)";

  // Charts
  upd(cF,ef,[fq]);
  cF.options.plugins.tooltip.callbacks.afterLabel=ctx=>["Valor: "+R(fv[ctx.dataIndex]),"Conversão: "+fcArr[ctx.dataIndex]+"%"];
  cF.update();
  upd(cCE,Object.keys(pe),[Object.values(pe)]);
  upd(cCV,Object.keys(pe),[Object.values(ve)]);
}}

function upd(c,l,ds){{c.data.labels=l;ds.forEach((v,i)=>c.data.datasets[i].data=v);c.update();}}

// ── CALENDÁRIO ──────────────────────────────────────────────────
const MNomes=["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"];
const DNomes=["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"];
function renderCal(){{
  $i("calt").textContent=MNomes[calMes]+" "+calAno;
  const dpd={{}};
  CRM.forEach(d=>{{if(d.created_at&&d.created_at.startsWith(calAno+"-"+String(calMes+1).padStart(2,"0"))){{const n=parseInt(d.created_at.split("-")[2]);dpd[n]=(dpd[n]||0)+1;}}}});
  const g=$i("calg");g.innerHTML="";
  DNomes.forEach(d=>{{const el=document.createElement("div");el.className="cdow";el.textContent=d;g.appendChild(el);}});
  const prim=new Date(calAno,calMes,1).getDay(),ult=new Date(calAno,calMes+1,0).getDate(),hoje=new Date();
  for(let k=0;k<prim;k++){{const el=document.createElement("div");el.className="cday outro";g.appendChild(el);}}
  for(let d=1;d<=ult;d++){{
    const el=document.createElement("div");let c="cday";
    if(d===hoje.getDate()&&calMes===hoje.getMonth()&&calAno===hoje.getFullYear())c+=" hoje";
    if(dpd[d])c+=" deal";el.className=c;el.textContent=d;
    if(dpd[d]){{const b=document.createElement("div");b.className="cbdg";b.textContent=dpd[d];el.appendChild(b);}}
    g.appendChild(el);
  }}
}}
function calMov(dir){{calMes+=dir;if(calMes>11){{calMes=0;calAno++;}}if(calMes<0){{calMes=11;calAno--;}}renderCal();}}

// ── CHARTS ──────────────────────────────────────────────────────
Chart.defaults.color="#6e6e73";Chart.defaults.borderColor="rgba(0,0,0,0.05)";
cF=new Chart($i("gF"),{{
  type:"bar",
  data:{{labels:[],datasets:[{{label:"Negociações",data:[],backgroundColor:"#0071e3",borderRadius:6,borderSkipped:false}}]}},
  options:{{indexAxis:"y",plugins:{{legend:{{display:false}},datalabels:{{color:"#fff",font:{{weight:"bold",size:11}},anchor:"center",align:"center",formatter:(v,ctx)=>{{const p=fcArr[ctx.dataIndex];return v>0?(v+(p?" ("+p+"%)":"")):"";}}}}  ,tooltip:{{callbacks:{{}}}}}},scales:{{x:{{beginAtZero:true,grid:{{color:"rgba(0,0,0,0.04)"}}}},y:{{grid:{{display:false}}}}}}}}
}});
cCE=new Chart($i("gCE"),{{type:"bar",data:{{labels:[],datasets:[{{label:"Neg.",data:[],backgroundColor:"#0071e3",borderRadius:6}}]}},options:{{plugins:{{legend:{{display:false}},datalabels:{{display:false}}}},scales:{{y:{{beginAtZero:true}},x:{{grid:{{display:false}}}}}}  }}}});
cCV=new Chart($i("gCV"),{{type:"doughnut",data:{{labels:[],datasets:[{{data:[],backgroundColor:["#0071e3","#32ade6","#28cd41","#ff9500","#ff3b30","#5e5ce6","#ff2d55"]}}]}},options:{{plugins:{{legend:{{position:"bottom",labels:{{font:{{size:11}},padding:12}}}},datalabels:{{color:"#fff",font:{{weight:"bold",size:12}},formatter:(v,ctx)=>{{const s=ctx.dataset.data.reduce((a,b)=>a+b,0);const p=v/s*100;return p>5?p.toFixed(1)+"%":"";}}  }}}}}}}});

// Inicialização — sempre carrega sem depender de login
const saved=localStorage.getItem("im_current");
if(saved){{currentUser=JSON.parse(saved);}}
if($i("auth-wrap"))$i("auth-wrap").style.display="none";
initUI();
filtrar();
</script>
</body></html>"""

    with open("dashboard_unificado.html","w",encoding="utf-8") as f:
        f.write(html)
    print("\n✅ Dashboard gerado! Abra 'dashboard_unificado.html'")


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

    try:
        gerar_dashboard(crm_deals, mkt_data, conv_total, conv_employees)
    except Exception as e:
        import traceback, sys
        print(f"\n❌ ERRO em gerar_dashboard:", flush=True)
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
