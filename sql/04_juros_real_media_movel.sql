-- Análise 04: Média Móvel de 7 e 30 dias para a Selic e Dólar (Suavização de Tendência)
SELECT 
    data,
    selic,
    ROUND(AVG(selic) OVER (ORDER BY data ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS selic_mm7d,
    dolar_venda,
    ROUND(AVG(dolar_venda) OVER (ORDER BY data ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 4) AS dolar_mm30d
FROM tb_indicadores_diarios
ORDER BY data DESC;