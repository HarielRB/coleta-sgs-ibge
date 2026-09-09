-- Análise 03: Comparativo entre o IPCA (SGS) e a Variação Mensal do IPCA (IBGE)
SELECT 
    m.data,
    m.ipca AS ipca_sgs,
    i.variacao_mensal AS ipca_ibge,
    m.igpm
FROM tb_indicadores_mensais m
INNER JOIN tb_ipca_ibge i ON strftime('%Y-%m', m.data) = strftime('%Y-%m', i.data)
ORDER BY m.data DESC;