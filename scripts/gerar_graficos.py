import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Configuração de estilo visual refinado para gráficos financeiros/macroeconômicos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

DB_PATH = 'banco_indicadores.db'
OUTPUT_DIR = 'images'


def garantir_diretorio(diretorio=OUTPUT_DIR):
    """Garante a existência da pasta de saída das imagens."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)


def carregar_dados_sql(arquivo_sql):
    """Lê e executa a query SQL retornando um DataFrame Pandas."""
    caminho_sql = os.path.join('sql', arquivo_sql)
    if not os.path.exists(caminho_sql):
        raise FileNotFoundError(f"Arquivo SQL não encontrado: {caminho_sql}")
    
    with open(caminho_sql, 'r', encoding='utf-8') as f:
        query = f.read()
        
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)
    return df


def gerar_grafico_01():
    """Gráfico 1: Média Mensal SELIC vs. Dólar (USD/BRL)"""
    df = carregar_dados_sql('01_selic_cambio_mensal.sql')
    if df.empty:
        print("⚠️ Dados da query 01 vazios.")
        return

    df['mes_dt'] = pd.to_datetime(df['mes'] + '-01')
    df = df.sort_values('mes_dt')

    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)

    # Eixo 1: SELIC (% a.a.)
    color1 = '#1f77b4' # Azul elegante
    ax1.set_xlabel('Período (Mês/Ano)', fontsize=11, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Taxa Selic Média (% a.a.)', color=color1, fontsize=11, fontweight='bold')
    line1 = ax1.plot(df['mes_dt'], df['selic_media'], color=color1, linewidth=2.5, marker='o', markersize=4, label='Selic Média (% a.a.)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Eixo 2: Dólar (R$)
    ax2 = ax1.twinx()
    color2 = '#2ca02c' # Verde câmbio
    ax2.set_ylabel('Dólar Médio (R$ / USD)', color=color2, fontsize=11, fontweight='bold')
    line2 = ax2.plot(df['mes_dt'], df['dolar_medio'], color=color2, linewidth=2.5, linestyle='-', marker='s', markersize=4, label='Dólar Médio (R$)')
    ax2.fill_between(df['mes_dt'], df['dolar_minimo'], df['dolar_maximo'], color=color2, alpha=0.12, label='Amplitude Dólar (Mín - Máx)')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.grid(False)

    # Formatação de datas no eixo X
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    # Título e Legenda Unificada
    plt.title('Evolução da Taxa SELIC e da Cotação do Dólar (USD/BRL) - Média Mensal', fontsize=14, fontweight='bold', pad=15)
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

    fig.tight_layout()
    caminho_saida = os.path.join(OUTPUT_DIR, '01_selic_cambio_mensal.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"✅ Gráfico 01 salvo em: {caminho_saida}")


def gerar_grafico_02():
    """Gráfico 2: Comportamento do Dólar por Cenário de Juros (Juros Altos vs Juros Baixos)"""
    df = carregar_dados_sql('02_periodo_alta_juros_cambio.sql')
    if df.empty:
        print("⚠️ Dados da query 02 vazios.")
        return

    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

    # Preparar dados para agrupamento em barras
    cenarios = df['cenario_juros'].tolist()
    dolar_medio = df['dolar_medio'].tolist()
    dolar_min = df['dolar_minimo'].tolist()
    dolar_max = df['dolar_maximo'].tolist()
    selic_media = df['selic_media_cenario'].tolist()

    x = range(len(cenarios))
    width = 0.25

    rects1 = ax.bar([i - width for i in x], dolar_min, width, label='Dólar Mínimo', color='#91bfdb')
    rects2 = ax.bar([i for i in x], dolar_medio, width, label='Dólar Médio', color='#4575b4')
    rects3 = ax.bar([i + width for i in x], dolar_max, width, label='Dólar Máximo', color='#d73027')

    ax.set_ylabel('Cotação Dólar (R$ / USD)', fontsize=11, fontweight='bold')
    ax.set_title('Comportamento do Dólar por Cenário de Taxa SELIC\n(Comparação com a Média Histórica de Juros)', fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c}\n(Selic Média: {s:.2f}% a.a.)" for c, s in zip(cenarios, selic_media)], fontsize=10, fontweight='bold')
    ax.legend(loc='upper right', frameon=True)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    # Rotular barras com os valores exatos
    def rotular_barras(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'R$ {height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    rotular_barras(rects1)
    rotular_barras(rects2)
    rotular_barras(rects3)

    fig.tight_layout()
    caminho_saida = os.path.join(OUTPUT_DIR, '02_periodo_alta_juros_cambio.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"✅ Gráfico 02 salvo em: {caminho_saida}")


def gerar_grafico_03():
    """Gráfico 3: Comparativo entre IPCA (SGS), IPCA (IBGE) e IGP-M"""
    df = carregar_dados_sql('03_ipca_selic_defasagem.sql')
    if df.empty:
        print("⚠️ Dados da query 03 vazios.")
        return

    df['data_dt'] = pd.to_datetime(df['data'])
    df = df.sort_values('data_dt')

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    ax.plot(df['data_dt'], df['ipca_sgs'], label='IPCA (SGS/BACEN)', color='#e41a1c', linewidth=2, linestyle='-')
    ax.plot(df['data_dt'], df['ipca_ibge'], label='IPCA (SIDRA/IBGE)', color='#377eb8', linewidth=2, linestyle='--')
    ax.plot(df['data_dt'], df['igpm'], label='IGP-M (FGV)', color='#ff7f00', linewidth=2, linestyle=':')

    ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
    ax.set_xlabel('Período (Mês/Ano)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('Variação Mensal (%)', fontsize=11, fontweight='bold')
    ax.set_title('Comparativo de Índices de Inflação Mensal: IPCA (SGS) vs. IPCA (IBGE) vs. IGP-M', fontsize=13, fontweight='bold', pad=15)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    ax.grid(True, linestyle='--', alpha=0.5)

    fig.tight_layout()
    caminho_saida = os.path.join(OUTPUT_DIR, '03_ipca_selic_defasagem.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"✅ Gráfico 03 salvo em: {caminho_saida}")


def gerar_grafico_04():
    """Gráfico 4: Suavização de Tendência - Média Móvel de 7 dias (Selic) e 30 dias (Dólar)"""
    df = carregar_dados_sql('04_juros_real_media_movel.sql')
    if df.empty:
        print("⚠️ Dados da query 04 vazios.")
        return

    df['data_dt'] = pd.to_datetime(df['data'])
    df = df.sort_values('data_dt')

    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)

    # Eixo 1: SELIC
    color1 = '#2b5c8f'
    ax1.set_xlabel('Data', fontsize=11, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Taxa Selic (% a.a.)', color=color1, fontsize=11, fontweight='bold')
    line1 = ax1.plot(df['data_dt'], df['selic_mm7d'], color=color1, linewidth=2, label='Selic (Média Móvel 7d)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Eixo 2: Dólar
    ax2 = ax1.twinx()
    color2 = '#27ae60'
    ax2.set_ylabel('Dólar Venda (R$ / USD)', color=color2, fontsize=11, fontweight='bold')
    line2 = ax2.plot(df['data_dt'], df['dolar_mm30d'], color=color2, linewidth=2, linestyle='-', label='Dólar (Média Móvel 30d)')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.grid(False)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    plt.xticks(rotation=45)

    plt.title('Tendência de Curto e Médio Prazo: Selic MM(7d) vs. Dólar MM(30d)', fontsize=13, fontweight='bold', pad=15)
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

    fig.tight_layout()
    caminho_saida = os.path.join(OUTPUT_DIR, '04_juros_real_media_movel.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"✅ Gráfico 04 salvo em: {caminho_saida}")


def gerar_grafico_05():
    """Gráfico 5: Sensibilidade de Preços ao Câmbio - IGP-M vs IPCA vs Dólar Médio"""
    df = carregar_dados_sql('05_igpm_cambio_vs_ipca_cambio.sql')
    if df.empty:
        print("⚠️ Dados da query 05 vazios.")
        return

    df['data_dt'] = pd.to_datetime(df['data'])
    df = df.sort_values('data_dt')

    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)

    # Eixo 1: IGP-M e IPCA (% mensal)
    ax1.set_xlabel('Período (Mês/Ano)', fontsize=11, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Variação Mensal de Preços (%)', fontsize=11, fontweight='bold')
    line1 = ax1.plot(df['data_dt'], df['igpm'], color='#e67e22', linewidth=2.2, label='IGP-M (Sensível a Commodities/Câmbio)')
    line2 = ax1.plot(df['data_dt'], df['ipca'], color='#c0392b', linewidth=2.2, linestyle='--', label='IPCA (Inflação Oficial ao Consumidor)')
    ax1.axhline(0, color='black', linewidth=0.8, linestyle=':')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Eixo 2: Dólar Média Mensal
    ax2 = ax1.twinx()
    color_dol = '#2980b9'
    ax2.set_ylabel('Dólar Médio no Mês (R$)', color=color_dol, fontsize=11, fontweight='bold')
    line3 = ax2.plot(df['data_dt'], df['dolar_medio_mes'], color=color_dol, linewidth=1.8, linestyle='-.', label='Dólar Médio Mensal (R$)')
    ax2.tick_params(axis='y', labelcolor=color_dol)
    ax2.grid(False)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    plt.title('Sensibilidade ao Câmbio: Transmissão do Dólar no IGP-M vs. IPCA', fontsize=13, fontweight='bold', pad=15)

    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

    fig.tight_layout()
    caminho_saida = os.path.join(OUTPUT_DIR, '05_igpm_cambio_vs_ipca_cambio.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"✅ Gráfico 05 salvo em: {caminho_saida}")


def gerar_todos_graficos():
    """Gera sequencialmente os 5 gráficos da análise e salva na pasta images/."""
    garantir_diretorio()
    print("\n" + "=" * 60)
    print("🎨 INICIANDO A GERAÇÃO E EXPORTAÇÃO DOS GRÁFICOS...")
    print("=" * 60 + "\n")
    gerar_grafico_01()
    gerar_grafico_02()
    gerar_grafico_03()
    gerar_grafico_04()
    gerar_grafico_05()
    print("\n" + "=" * 60)
    print("🎉 TODOS OS GRÁFICOS FORAM GERADOS E EXPORTADOS COM SUCESSO!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    gerar_todos_graficos()
