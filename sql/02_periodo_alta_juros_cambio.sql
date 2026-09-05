-- Análise 02: Comportamento do Dólar em cenários de Juros Altos vs Juros Baixos
WITH media_historica AS (
    -- Calcula a média geral da SELIC em todo o período coletado
    SELECT AVG(selic) AS selic_media_geral 
    FROM tb_indicadores_diarios
),
classificacao_diaria AS (
    -- Classifica cada dia de acordo com a taxa SELIC comparada à média
    SELECT 
        data,
        selic,
        dolar_venda,
        CASE 
            WHEN selic >= (SELECT selic_media_geral FROM media_historica) THEN 'Juros Altos'
            ELSE 'Juros Baixos'
        END AS cenario_juros
    FROM tb_indicadores_diarios
)
-- Agrupa por cenário para comparar o Dólar médio em cada ambiente de juros
SELECT 
    cenario_juros,
    COUNT(*) AS total_dias,
    ROUND(AVG(selic), 2) AS selic_media_cenario,
    ROUND(AVG(dolar_venda), 4) AS dolar_medio,
    ROUND(MAX(dolar_venda), 4) AS dolar_maximo,
    ROUND(MIN(dolar_venda), 4) AS dolar_minimo
FROM classificacao_diaria
GROUP BY cenario_juros
ORDER BY dolar_medio DESC;