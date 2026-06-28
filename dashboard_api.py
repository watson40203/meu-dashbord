"""
dashboard_api.py — Tokens e funções de busca do RD Station
Só muda quando as APIs mudam. NÃO contém HTML.
"""
"""
Dashboard Unificado - RD Station
Design: Apple Liquid Glass (tema claro, azul)
"""

import requests
import json
import base64
import os
from datetime import datetime

LOGO_PATH = "logoapp.jpeg"

def carregar_logo_base64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

TOKEN_CRM = "681cb285978e2f00145fb15d"
CLIENT_ID_MKT      = "29720919-7b18-4e7b-8110-a333e8daad15"
CLIENT_SECRET_MKT  = "67ef94d961d44decbdb33423df2e46af"
REFRESH_TOKEN_MKT  = "8EEc9Y1JDmnTJ8VYSgIIJAuHzfFH4rTtw5tOBxMI9xs"
TOKEN_PUBLICO_MKT  = "b502ad2ceb5e524a93c7e094cc79ef68"
TOKEN_PRIVADO_MKT  = "e07842e6443360d1def8ad5e1cf263c2"
TOKEN_CONVERSAS = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbXBsb3llZSI6IjY4NmQ2ZGQ5NWM4YzA3MDAxMzFiZGVjYyIsImNvbXBhbnkiOiI2NzYxN2VmYWUzNzE1MDc1ZDI5ODhmOGUiLCJpYXQiOjE3NTQ5MjYzMDR9.Al9dIbdGhSeJ86znoIXBOcyt6U7ahVrkGM2xY1MRowU"
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


