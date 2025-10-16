import pandas as pd 
import os
import sys
import streamlit as st
# Carregar Data set #
NOME_ARQUIVO = 'Animation_Movies.csv'
df = None
try:
    df = pd.read_csv(NOME_ARQUIVO)
    st.title("🎬 Análise de Mercado de Filmes de Animação") # <--- Título Principal
    st.success(f"Dataset de Animações carregado com sucesso! Total de linhas: {len(df)}")
except FileNotFoundError:
    st.error(f"ERRO: Arquivo '{NOME_ARQUIVO}' não encontrado. Verifique o nome e a localização.")
    sys.exit()
    # pré- processamento dos dados e limpeza do dataset #
# 1. Converter Colunas Essenciais para Numérico
# Esta linha estava na Limpeza Original (Linha 15, em uma versão anterior)
df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce') 
df['budget'] = pd.to_numeric(df['budget'], errors='coerce') 
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce') # Adicionado para o KPI 3

# 2. Remover Linhas Nulas em Colunas Chave (Criação do df_limpo)
# Usando as colunas essenciais para o KPI 1 e 2.
df_limpo = df.dropna(subset=['vote_average', 'genres', 'runtime', 'budget']) 
st.subheader("--- Informações Cruciais de Limpeza ---")
st.markdown(f"**Total de Filmes Carregados:** {len(df)}")
st.markdown(f"**Filmes Usados na Análise (sem Nulos):** {len(df_limpo)}")
# Análise - KPI-1#
st.header("1. KPI: Nichos de Qualidade (Alta Nota / Baixa Oferta)")
analise_kpi_1 = df_limpo.groupby('genres').agg(
    Media_Avaliacao=('vote_average', 'mean'),
    Total_Lancamentos=('genres', 'count')
).reset_index()

# Corrigindo a métrica para ser Inversa (Nota / Lançamentos)
analise_kpi_1['Prioridade'] = analise_kpi_1['Media_Avaliacao'] / analise_kpi_1['Total_Lancamentos']
top_prioridade = analise_kpi_1.sort_values(by='Prioridade', ascending=False).head(10)

st.dataframe(top_prioridade, use_container_width=True) # Exibição da Tabela no Streamlit
# Análise - KPI-2#
# Quais são os tipos de animação mais longos e mais caros?#
st.header("2. KPI: Complexidade de Produção (Mais Longos e Mais Caros)")

df_kpi_2 = df_limpo.dropna(subset=['runtime', 'budget'])

analise_kpi_2 = df_kpi_2.groupby('genres').agg(
    Media_Duracao=('runtime', 'mean'),
    Media_Orcamento=('budget', 'mean'),
    Total_Lancamentos=('genres', 'count')
).reset_index()

# Métrica de Complexidade: Duracao * Orcamento
analise_kpi_2['Complexidade'] = analise_kpi_2['Media_Duracao'] * analise_kpi_2['Media_Orcamento']

top_complexidade = analise_kpi_2.sort_values(by='Complexidade', ascending=False).head(10)

st.dataframe(top_complexidade, use_container_width=True)
# Análise - KPI-3#
# Quais são os tipos de animação com maior retorno sobre investimento (ROI)?#
st.header("3. KPI: Top Filmes por Retorno de Qualidade (ROI * Nota)")

df_kpi_3 = df.dropna(subset=['vote_average', 'budget', 'revenue'])
df_kpi_3 = df_kpi_3[(df_kpi_3['budget'] > 0) & (df_kpi_3['revenue'] > 0)]

# Métrica: Taxa de Lucro * Qualidade
df_kpi_3['Retorno_Qualidade'] = (
    (df_kpi_3['revenue'] - df_kpi_3['budget']) / df_kpi_3['budget']
) * df_kpi_3['vote_average']

top_retorno = df_kpi_3.sort_values(by='Retorno_Qualidade', ascending=False).head(10)

st.dataframe(top_retorno[['title', 'vote_average', 'budget', 'revenue', 'Retorno_Qualidade']], use_container_width=True)
# FASE FINAL: SALVAMENTO DOS DADOS CHAVE# 
st.success("Análise concluída. O Dashboard exibe os 3 KPIs principais.")

# Salvamento dos dados chave (se ainda for necessário)
# top_prioridade.to_csv('relatorio_kpi_1_prioridade.csv', index=False)
# top_retorno.to_csv('relatorio_kpi_3_retorno.csv', index=False)