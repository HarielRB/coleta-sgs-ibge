# Análise de Indicadores Econômicos Brasileiros (Selic, Câmbio, IPCA e IGP-M)

## 📌 Contexto

Breve parágrafo explicando o cenário: por que analisar a relação entre juros, câmbio e inflação no Brasil é relevante (ex: contexto macroeconômico recente, decisões do Copom, etc). 2-4 frases, sem enrolação.

## ❓ Perguntas de negócio

Este projeto busca responder:

1. Como o dólar (USD/BRL) variou de acordo com a taxa Selic ao longo do tempo?
2. Qual o impacto do IPCA sobre as decisões de Selic?
3. O IGP-M reage de forma mais sensível ao câmbio do que o IPCA?

## 🗂️ Fonte de dados

- **Origem:** API SGS (Sistema Gerenciador de Séries Temporais) do Banco Central do Brasil
- **Séries utilizadas:**

| Indicador | Código SGS |
|---|---|
| Selic | 432 |
| Câmbio USD/BRL | 1 |
| IPCA | 433 |
| IGP-M | 189 |

- **Período analisado:** [preencher, ex: jan/2015 a jul/2026]

## 🛠️ Metodologia

Breve descrição do processo: coleta via API → armazenamento em PostgreSQL → consultas SQL → visualização dos resultados. Mencione as principais técnicas usadas nas queries (CTEs, window functions, funções de correlação) sem entrar em código aqui — o código fica nos arquivos `.sql`.

## 🔍 Principais análises

### 1. Selic x Câmbio

Breve explicação (2-3 frases) do que a query `01_selic_cambio_mensal.sql` mostra e o raciocínio por trás dela.

*(inserir imagem do gráfico aqui)*

**Insight:** [preencher com a conclusão real encontrada nos dados]

---

### 2. Ciclos de alta de juros x comportamento do câmbio

Explicação da CTE que identifica períodos de alta da Selic (query `02_periodos_alta_juros_cambio.sql`) e o que se observou no câmbio nesses períodos.

*(inserir imagem do gráfico aqui)*

**Insight:** [preencher]

---

### 3. IPCA x Selic (com defasagem)

Explicação da lógica de `LAG()` usada em `03_ipca_selic_defasagem.sql` — por que faz sentido testar defasagem entre inflação e resposta de juros.

*(inserir imagem do gráfico aqui)*

**Insight:** [preencher]

---

### 4. Juro real (Selic - IPCA acumulado 12m)

Explicação da média móvel usada em `04_juro_real_media_movel.sql`.

*(inserir imagem do gráfico aqui)*

**Insight:** [preencher]

---

### 5. IGP-M x Câmbio (comparado ao IPCA x Câmbio)

Explicação da comparação de correlação entre os dois índices de preço e o câmbio.

*(inserir imagem do gráfico aqui)*

**Insight:** [preencher — ex: se o IGP-M realmente mostrou correlação mais forte com o câmbio do que o IPCA, e por quê isso faz sentido dado sua composição]

## ✅ Conclusão

Parágrafo final amarrando as descobertas: o que os dados confirmaram (ou não) das teorias macroeconômicas testadas, e qual seria o próximo passo se o projeto continuasse (ex: incluir mais indicadores, testar outros períodos, comparar com outros países).

## 🧰 Tecnologias utilizadas

- PostgreSQL
- Python (coleta de dados via API)
- [biblioteca de visualização usada, ex: Matplotlib/Seaborn]

## 📁 Estrutura do repositório

```
├── README.md
├── /sql
│   ├── 01_selic_cambio_mensal.sql
│   ├── 02_periodos_alta_juros_cambio.sql
│   ├── 03_ipca_selic_defasagem.sql
│   ├── 04_juro_real_media_movel.sql
│   └── 05_igpm_cambio_vs_ipca_cambio.sql
├── /scripts
│   └── coleta_dados_bacen.py
└── /images
    └── (gráficos gerados)
```

## 👤 Autor

[Seu nome] — [link LinkedIn] — [link GitHub]