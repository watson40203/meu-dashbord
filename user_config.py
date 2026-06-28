"""
user_config.py — Equipe, papéis e metas mensais padrão
-------------------------------------------------------
Edite este arquivo para:
  • Definir o papel de cada operador (SDR / Corretor / Coordenadora)
  • Configurar metas mensais de VGV e Entrada
  • Configurar meta de agendamentos por SDR

Os valores aqui são os PADRÕES ao abrir o dashboard pela primeira vez.
Após salvar pelo painel de Config, os valores ficam salvos no navegador.
"""

# ── PAPÉIS DA EQUIPE ─────────────────────────────────────────────────────────
# Valores válidos: "sdr" | "corretor" | "coordenadora" | ""
EQUIPE = {
    "Watson Slonski":  "coordenadora",
    "Thaisy Lopes":    "sdr",
    "Carlos Pereira":  "corretor",
    "Ana Beatriz":     "sdr",
    "Pedro Henrique":  "corretor",
    # Adicione / edite conforme sua equipe real
}

# ── METAS MENSAIS DE AGENDAMENTO POR SDR ────────────────────────────────────
# Quantos agendamentos realizados cada SDR deve atingir por mês
# Formato: { "Nome do SDR": [jan, fev, mar, abr, mai, jun, jul, ago, set, out, nov, dez] }
METAS_SDR = {
    "Thaisy Lopes": [30, 28, 30, 30, 30, 28, 30, 30, 30, 30, 28, 30],
    "Ana Beatriz":  [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25],
}

# ── METAS MENSAIS — VGV E ENTRADA (R$) ──────────────────────────────────────
# Meta global da empresa por mês (dividida igualmente entre corretores)
# Formato: { mês: {"vgv": valor, "ent": valor} }
METAS_MENSAIS = {
    1:  {"vgv": 174_603.35, "ent": 21_278.28},   # Janeiro
    2:  {"vgv": 174_603.35, "ent": 21_278.28},   # Fevereiro
    3:  {"vgv": 174_603.35, "ent": 21_278.28},   # Março
    4:  {"vgv": 174_603.35, "ent": 21_278.28},   # Abril
    5:  {"vgv": 174_603.35, "ent": 21_278.28},   # Maio
    6:  {"vgv": 174_603.35, "ent": 21_278.28},   # Junho
    7:  {"vgv": 174_603.35, "ent": 21_278.28},   # Julho
    8:  {"vgv": 174_603.35, "ent": 21_278.28},   # Agosto
    9:  {"vgv": 174_603.35, "ent": 21_278.28},   # Setembro
    10: {"vgv": 174_603.35, "ent": 21_278.28},   # Outubro
    11: {"vgv": 174_603.35, "ent": 21_278.28},   # Novembro
    12: {"vgv": 174_603.35, "ent": 21_278.28},   # Dezembro
    # Totais anuais: VGV = R$ 2.095.240,14 | Entrada = R$ 255.239,40
}
