-- Análise 05: Comparação entre IGP-M (sensível ao câmbio) e IPCA no mesmo período
SELECT 
    m.data,
    m.igpm,
    m.ipca,
    ROUND(AVG(d.dolar_venda), 4) AS dolar_medio_mes
FROM tb_indicadores_mensais m
LEFT JOIN tb_indicadores_diarios d ON strftime('%Y-%m', m.data) = strftime('%Y-%m', d.data)
GROUP BY m.data, m.igpm, m.ipca
ORDER BY m.data DESC;