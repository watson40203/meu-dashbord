"""
Dashboard Web - RD Station Marketing
---------------------------------------
Este script busca as conversoes (leads) do RD Station Marketing
e gera uma pagina web (HTML) com graficos.

COMO USAR:
1. Coloque o seu TOKEN PUBLICO do RD Marketing na linha TOKEN_PUBLICO abaixo
2. Rode este arquivo: python3 dashboard_marketing.py
3. Um arquivo "dashboard_marketing.html" sera criado na mesma pasta
4. Abra esse arquivo dando duplo clique nele

OBS: Se aparecer erro 401 ou 403, me avise - pode ser que essa conta
precise de outro tipo de autenticacao (OAuth) e vamos ajustar juntos.
"""

import requests
import json
from collections import Counter
from datetime import datetime

# ===================================================
# CONFIGURACAO - coloque seu token publico aqui
# ===================================================
TOKEN_PUBLICO = "b502ad2ceb5e524a93c7e094cc79ef68"

BASE_URL = "https://www.rdstation.com.br/api/1.3/conversions"


def buscar_conversoes():
    """Busca as conversoes (leads convertidos) do RD Station Marketing."""
    todas_conversoes = []
    pagina = 1

    while True:
        params = {
            "api_key": TOKEN_PUBLICO,
            "page": pagina
        }

        resposta = requests.get(BASE_URL, params=params)

        if resposta.status_code != 200:
            print(f"Erro ao buscar dados: {resposta.status_code}")
            print(resposta.text)
            break

        dados = resposta.json()
        conversoes = dados.get("conversions", []) if isinstance(dados, dict) else dados

        if not conversoes:
            break

        todas_conversoes.extend(conversoes)
        print(f"Pagina {pagina}: {len(conversoes)} conversoes encontradas")

        if len(conversoes) < 20:  # essa API geralmente pagina de 20 em 20
            break

        pagina += 1

        if pagina > 200:  # seguranca para nao rodar infinito
            break

    return todas_conversoes


def processar_dados(conversoes):
    """Calcula estatisticas das conversoes."""

    total = len(conversoes)
    por_origem = Counter()
    por_mes = Counter()

    for conv in conversoes:
        origem = conv.get("source", conv.get("identificador", "Sem origem"))
        por_origem[str(origem)] += 1

        data = conv.get("created_at") or conv.get("conversion_date") or ""
        if data:
            mes = str(data)[:7]
            por_mes[mes] += 1

    meses_ordenados = sorted(por_mes.keys())

    return {
        "total": total,
        "por_origem": dict(por_origem.most_common(10)),
        "meses_labels": meses_ordenados,
        "meses_valores": [por_mes[m] for m in meses_ordenados],
    }


def gerar_dashboard_html(dados):
    origem_labels = list(dados["por_origem"].keys())
    origem_valores = list(dados["por_origem"].values())
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Dashboard RD Station Marketing</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
    * {{ box-sizing: border-box; }}
    body {{ font-family: -apple-system, Arial, sans-serif; background: #0f1729; color: #e2e8f0; margin: 0; padding: 30px 40px; }}
    h1 {{ font-size: 26px; margin-bottom: 4px; }}
    .atualizado {{ color: #94a3b8; font-size: 13px; margin-bottom: 30px; }}
    .cards {{ display: flex; gap: 20px; margin-bottom: 35px; flex-wrap: wrap; }}
    .card {{ background: linear-gradient(135deg, #1e293b, #161f30); border-radius: 14px; padding: 22px 28px; min-width: 200px; border: 1px solid #2a3650; }}
    .card .numero {{ font-size: 30px; font-weight: 700; color: #fb923c; }}
    .card .label {{ color: #94a3b8; font-size: 13px; margin-top: 6px; }}
    .graficos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    .painel {{ background: #161f30; border: 1px solid #2a3650; border-radius: 14px; padding: 24px; }}
    .painel h2 {{ font-size: 16px; margin-top: 0; margin-bottom: 16px; color: #cbd5e1; }}
    @media (max-width: 900px) {{ .graficos {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>

<h1>📈 Dashboard RD Station Marketing</h1>
<div class="atualizado">Atualizado em {agora}</div>

<div class="cards">
    <div class="card">
        <div class="numero">{dados['total']:,}</div>
        <div class="label">Conversões (leads) totais</div>
    </div>
</div>

<div class="graficos">
    <div class="painel">
        <h2>Conversões por origem</h2>
        <canvas id="graficoOrigem"></canvas>
    </div>
    <div class="painel">
        <h2>Conversões por mês</h2>
        <canvas id="graficoMeses"></canvas>
    </div>
</div>

<script>
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#2a3650';

new Chart(document.getElementById('graficoOrigem'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps(origem_labels)},
        datasets: [{{ label: 'Conversões', data: {json.dumps(origem_valores)}, backgroundColor: '#fb923c' }}]
    }},
    options: {{ indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
}});

new Chart(document.getElementById('graficoMeses'), {{
    type: 'line',
    data: {{
        labels: {json.dumps(dados['meses_labels'])},
        datasets: [{{
            label: 'Conversões',
            data: {json.dumps(dados['meses_valores'])},
            borderColor: '#fb923c',
            backgroundColor: 'rgba(251,146,60,0.15)',
            fill: true,
            tension: 0.3
        }}]
    }},
    options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
}});
</script>

</body>
</html>
"""

    with open("dashboard_marketing.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("\n✅ Dashboard gerado! Abra o arquivo 'dashboard_marketing.html' no navegador.")


if __name__ == "__main__":
    print("Buscando conversoes no RD Station Marketing...")
    conversoes = buscar_conversoes()
    print(f"\nTotal encontrado: {len(conversoes)} conversoes")
    dados = processar_dados(conversoes)
    gerar_dashboard_html(dados)
