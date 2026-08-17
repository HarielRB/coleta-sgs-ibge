from pandas.io.formats.style_render import Subset
from pandas._libs import ops_dispatch
from httpx._transports import default
import pandas as pd
# pyrefly: ignore [missing-import]
from bcb import sgs
import datetime
# pyrefly: ignore [missing-import]
import sidrapy

#Séries necessárias
# 432 = Taxa Selic
# 1   = Taxa de câmbio do Dólar comercial (venda)
# 11 = Selic Efetiva
# 12 = Taxa de câmbio do Euro comercial (venda)
# 433= IPCA
# 33659 = Inflação ao consumidor (IPCA) acumulada nos últimos 12 meses
# 189 = IGP-M

#data inicio

inicio = '2026-05-01'
fim = datetime.date.today().strftime('%Y-%m-%d')

#df = sgs.get([432, 1, 11, 12, 3659, 33659, 433, 189], start=inicio)

SERIESDIARIAS = {
    'SELIC':432,
    'Dolar Venda':1
    }

SERIESMENSAIS = {
    'IPCA':433,
    'IGP-M':189
}

df_series_diarias = sgs.get(SERIESDIARIAS, start=inicio, end=fim, timeout=120)
df_series_diarias = df_series_diarias.dropna(subset = ['Dolar Venda'])


df_series_mensais = sgs.get(SERIESMENSAIS, start=inicio, end=fim, timeout=120)

ipca_indice = sidrapy.get_table(table_code = '1737', 
                                territorial_level = '1',
                                ibge_territorial_code = 'all',
                                variable = '2266',
                                period='all')

ipca_indice_clean = ipca_indice.iloc[1:][['D2C', 'V']].copy()
ipca_indice_clean.columns = ['Periodo', 'Valor']
ipca_indice_clean['Valor'] = pd.to_numeric(
    ipca_indice_clean['Valor'],
    errors='coerce'
    )
ipca_indice_clean['Periodo'] = pd.to_datetime(ipca_indice_clean['Periodo'], format='%Y%m', errors='coerce')

print('-=-=Séries Diárias=-=-')
print(df_series_diarias.tail(15))

print('-=-=Séries Mensais=-=-')
print(df_series_mensais.tail(15))

print('-=-=IPCA=-=-')
print(ipca_indice_clean.tail(15))
