import datetime
from bcb import sgs
import pandas as pd
import sidrapy

SERIESDIARIAS = {
    'selic': 432,
    'dolar_venda': 1
}

SERIESMENSAIS = {
    'ipca': 433,
    'igpm': 189
}

def coletar_dados_diarios(inicio = '2020-01-01'):
    fim = datetime.date.today().strftime('%Y-%m-%d')
    df = sgs.get(SERIESDIARIAS, start=inicio, end=fim, timeout=120)
    df = df.dropna(subset = ['dolar_venda'])
    return df


def coletar_dados_mensais(inicio = '2020-01-01'):
    fim = datetime.date.today().strftime('%Y-%m-%d')
    df = sgs.get(SERIESMENSAIS, start=inicio, end=fim, timeout=120)
    return df


def coletar_ipca_ibge():
    ipca_indice = sidrapy.get_table(table_code = '1737', 
                                territorial_level = '1',
                                ibge_territorial_code = 'all',
                                variable = '63',
                                period='all')

    ipca_indice_clean = ipca_indice.iloc[1:][['D2C', 'V']].copy()
    ipca_indice_clean.columns = ['data', 'variacao_mensal']
    ipca_indice_clean['variacao_mensal'] = pd.to_numeric(
        ipca_indice_clean['variacao_mensal'],
        errors='coerce'
    )
    ipca_indice_clean['data'] = pd.to_datetime(ipca_indice_clean['data'], format='%Y%m', errors='coerce')
    ipca_indice_clean.set_index('data', inplace=True)

    return ipca_indice_clean
