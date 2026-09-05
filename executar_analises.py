import os
import sqlite3
import pandas as pd 


DB_PATH = 'banco_indicadores.db'

ANALISES = {
    '1': (
        '01_selic_cambio_mensal.sql', 
        'Media Mensal SELIC e Dólar'),
    '2': (
        '02_periodo_alta_juros_cambio.sql',
        'Comportamento do Dólar por Cenário de Juros',
    )

}


def executar_sql(arquivo_sql : str, titulo: str):
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


def menu():
    while True:
        print('=' * 50)
        print(' 📊 PAINEL DE ANÁLISES MACROECONÔMICAS (SQL)')
        print('=' * 50)
        for chave, (_, titulo) in ANALISES.items():
            print(f'[{chave}] {titulo}')
        print('[0] Sair')
        print('=' * 50)
        opcao = input('Digite o número da análise desejada: ').strip()
        if opcao == '0':
            print('\n Saindo do painel... Até mais!')
            break
        elif opcao in ANALISES:
            arquivo, titulo = ANALISES[opcao]
            executar_sql(arquivo, titulo)
            input('\nPressione ENTER para voltar ao menu principal...')
        else:
            print('\n Opção inválida! Tente novamente.\n')


if __name__ == '__main__':
    menu()

