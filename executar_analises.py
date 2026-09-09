import os
import sqlite3
import pandas as pd 
from scripts.gerar_graficos import (
    gerar_grafico_01,
    gerar_grafico_02,
    gerar_grafico_03,
    gerar_grafico_04,
    gerar_grafico_05,
    gerar_todos_graficos,
)


DB_PATH = 'banco_indicadores.db'

ANALISES = {
    '1': (
        '01_selic_cambio_mensal.sql', 
        'Média Mensal SELIC e Dólar',
        gerar_grafico_01
    ),
    '2': (
        '02_periodo_alta_juros_cambio.sql',
        'Comportamento do Dólar por Cenário de Juros',
        gerar_grafico_02
    ),
    '3': (
        '03_ipca_selic_defasagem.sql',
        'Comparativo entre o IPCA (SGS) e a Variação Mensal do IPCA (IBGE)',
        gerar_grafico_03
    ),
    '4': (
        '04_juros_real_media_movel.sql',
        'Média Móvel de 7 e 30 dias para a Selic e Dólar (Suavização de Tendência)',
        gerar_grafico_04
    ),
    '5': (
        '05_igpm_cambio_vs_ipca_cambio.sql',
        'Comparação entre IGP-M (sensível ao câmbio) e IPCA no mesmo período',
        gerar_grafico_05
    )
}


def executar_sql(arquivo_sql: str, titulo: str, funcao_grafico=None):
    caminho_completo = os.path.join('sql', arquivo_sql)

    if not os.path.exists(caminho_completo):
        print(f'\n❌ Arquivo {caminho_completo} não encontrado!')
        return
    
    conexao = sqlite3.connect(DB_PATH)

    with open(caminho_completo, 'r', encoding='utf-8') as f:
        query = f.read()
    
    print(f"\n{'=' * 60}")
    print(f'📊 {titulo.upper()}')
    print(f'📄 Arquivo: {arquivo_sql}')
    print(f'{"=" * 60}\n')

    df = pd.read_sql_query(query, conexao)

    conexao.close()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.head(20))

    colunas_numericas = df.select_dtypes(include=['float64', 'int64'])

    if colunas_numericas.shape[1] >= 2:
        matriz_corr = colunas_numericas.corr()
        print('')
        print(f"\n{'=' * 60}")
        print("📈 MATRIZ DE CORRELAÇÃO ESTATÍSTICA (Pearson):")
        print(matriz_corr.round(4))
        print("\n" + "-" * 50)

    print(f'\n Total de registros retornados: {len(df)}\n')

    if funcao_grafico:
        print("🖼️ Gerando e atualizando gráfico da análise...")
        funcao_grafico()


def menu():
    while True:
        print('=' * 60)
        print(' 📊 PAINEL DE ANÁLISES MACROECONÔMICAS E GRÁFICOS (SQL)')
        print('=' * 60)
        for chave, (_, titulo, _) in ANALISES.items():
            print(f'[{chave}] {titulo}')
        print('[6] 🎨 Gerar e Exportar TODOS os Gráficos (.png)')
        print('[0] Sair')
        print('=' * 60)
        opcao = input('Digite o número da análise desejada: ').strip()
        if opcao == '0':
            print('\n Saindo do painel... Até mais!')
            break
        elif opcao == '6':
            gerar_todos_graficos()
            input('\nPressione ENTER para voltar ao menu principal...')
        elif opcao in ANALISES:
            arquivo, titulo, funcao_grafico = ANALISES[opcao]
            executar_sql(arquivo, titulo, funcao_grafico)
            input('\nPressione ENTER para voltar ao menu principal...')
        else:
            print('\n Opção inválida! Tente novamente.\n')


if __name__ == '__main__':
    menu()
