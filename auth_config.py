"""
auth_config.py — Credenciais e controle de acesso
--------------------------------------------------
Edite este arquivo para:
  • Mudar a senha do admin
  • Pré-aprovar usuários da equipe (sem precisar aprovar pelo painel)

NUNCA compartilhe este arquivo com pessoas externas.
"""

# ── ADMINISTRADOR ─────────────────────────────────────────────────────────────
ADMIN_EMAIL    = "watson@imincorporadora.com.br"
ADMIN_NOME     = "Watson Slonski"
ADMIN_PASSWORD = "Alana052130"   # ← mude aqui para trocar a senha

# ── USUÁRIOS PRÉ-APROVADOS ────────────────────────────────────────────────────
# Estes usuários podem criar conta e entrar SEM precisar de aprovação manual.
# Adicione o e-mail de cada membro da equipe que terá acesso ao dashboard.
USUARIOS_PRE_APROVADOS = [
    "thaisy@imincorporadora.com.br",
    "carlos@imincorporadora.com.br",
    "ana@imincorporadora.com.br",
    "pedro@imincorporadora.com.br",
    # Adicione mais e-mails aqui, um por linha
]
