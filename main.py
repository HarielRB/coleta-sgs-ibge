from scripts.database import inicializar_banco, salvar_dados
from scripts.coleta_dados_bacen import (
    coletar_dados_diarios,
    coletar_dados_mensais,
    coletar_ipca_ibge,
)


def executar_pipeline():
    print("=" * 50)
    print("🚀 INICIANDO PIPELINE DE EXTRAÇÃO E CARGA (ETL)")
    print("=" * 50)

    # 1. Inicializar o banco de dados e criar tabelas
    print("\n1️⃣  Inicializando Banco de Dados SQLite...")
    inicializar_banco()

    # 2. Coletar dados diários (SELIC e Dólar) e salvar
    print("\n2️⃣  Coletando dados diários do Banco Central (SGS)...")
    df_diario = coletar_dados_diarios(inicio="2020-01-01")
    salvar_dados(df_diario, "tb_indicadores_diarios")

    # 3. Coletar dados mensais (IPCA e IGP-M do SGS) e salvar
    print("\n3️⃣  Coletando dados mensais do Banco Central (SGS)...")
    df_mensal = coletar_dados_mensais(inicio="2020-01-01")
    salvar_dados(df_mensal, "tb_indicadores_mensais")

    # 4. Coletar dados do IPCA IBGE (Sidra) e salvar
    print("\n4️⃣  Coletando IPCA detalhado do IBGE (Sidra)...")
    df_ipca_ibge = coletar_ipca_ibge()
    salvar_dados(df_ipca_ibge, "tb_ipca_ibge")

    print("\n" + "=" * 50)
    print(" PIPELINE FINALIZADO COM SUCESSO!")
    print("=" * 50)


if __name__ == "__main__":
    executar_pipeline()