-- Tabela para indicadores diários (SELIC e Dólar)

CREATE TABLE IF NOT EXISTS tb_indicadores_diarios (
    data DATE PRIMARY KEY,
    selic REAL,
    dolar_venda REAL
);

-- 2.  Tabela para Indicadores mensais do SGS (IPCA e IGP-M)
CREATE TABLE IF NOT EXISTS tb_indicadores_mensais (
    data DATE PRIMARY KEY,
    ipca REAL,
    igpm REAL
);

-- 3 Tabela para o IPCA Detalhado do IBGE (sidra)
CREATE TABLE IF NOT EXISTS tb_ipca_ibge(
    data DATE PRIMARY KEY,
    variacao_mensal REAL
);
