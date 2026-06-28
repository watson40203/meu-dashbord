"""
dashboard_main.py — Orquestrador: chama APIs e gera o HTML
Raramente muda. Roda com: python3 dashboard_main.py
"""
from dashboard_api import (
    buscar_crm, buscar_marketing,
    buscar_conversas, buscar_conversas_employees
)
from dashboard_html import gerar_dashboard

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
