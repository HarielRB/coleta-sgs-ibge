import sqlite3
import pandas as pd 


DBPATH = 'banco_indicadores.db'

def inicializar_banco():
    #1. criar a conexao com o sqlite
    conexao = sqlite3.connect(DBPATH)

    #2. invocar o script de criação do banco:
    with open('sql/00_criacao_do_banco.sql', 'r', encoding='utf-8') as f:
        script_sql = f.read()

    #3. executar o script sql:
    cursor = conexao.cursor()
    cursor.executescript(script_sql)

    #4. saval e fecha a conexao:

    conexao.commit()
    conexao.close()

    print('Banco de dados criado e inicializado com sucesso!')


def salvar_dados(df: pd.DataFrame, nome_tabela: str):
    
    conexao = sqlite3.connect(DBPATH)

    # Garante que o indice do DataFrame no Pandas seja chamado 'data' para coincidir com a chave primaria no SQL
    df.index.name = 'data'

    df.to_sql(nome_tabela, conexao, if_exists='append', index=True)

    conexao.close()

    print(f'Dados salvos na tabela {nome_tabela} com sucesso!')