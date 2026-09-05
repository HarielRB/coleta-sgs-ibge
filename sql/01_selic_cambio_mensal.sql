SELECT
    strftime('%Y-%m', data) AS mes,
    ROUND(AVG(selic), 2) AS selic_media,
    ROUND(AVG(dolar_venda), 2) AS dolar_medio,
    ROUND(MAX(dolar_venda), 4) AS dolar_maximo,
    ROUND(MIN(dolar_venda), 4) AS dolar_minimo
FROM tb_indicadores_diarios
GROUP BY strftime('%Y-%m', data)
ORDER BY mes DESC