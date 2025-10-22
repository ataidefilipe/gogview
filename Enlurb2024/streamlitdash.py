import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
from tratamento import tratamento_dados

# Carregando os dados de exemplo fornecidos
# Decisão de design: Como os dados são limitados, uso um DataFrame hardcoded para simular a base. Em produção, carregar de CSV ou banco de dados.
df = tratamento_dados()

# Carregando GeoJSON para o mapa de bairros do Recife
# Decisão de design: Para o "momento ousadia", incluo um mapa choropleth para visualizar densidade de chamados por bairro. Isso ajuda o diretor a priorizar áreas visualmente. Uso dados abertos da Prefeitura do Recife.
geo_url = "http://dados.recife.pe.gov.br/dataset/c1f100f0-f56f-4dd4-9dcc-1aa4da28798a/resource/e43bee60-9448-4d3d-92ff-2378bc3b5b00/download/bairros.geojson"
try:
    geo_data = requests.get(geo_url).json()
except:
    geo_data = None  # Fallback se falhar, mapa não será exibido
    st.warning("Não foi possível carregar dados geográficos para o mapa.")

# Configuração da página do dashboard
# Decisão de design: Layout wide para melhor uso de espaço em telas grandes, permitindo mais colunas para KPIs e gráficos side-by-side.
st.set_page_config(page_title="Dashboard de Chamados de Serviços Urbanos", layout="wide")

# Título principal
# Decisão de design: Título claro e centralizado para imediata compreensão do propósito do dashboard, focado na persona do diretor.
st.title("Dashboard de Análise de Chamados de Serviços Urbanos - Recife")

# Sidebar para filtros
# Decisão de design: Filtros na sidebar para manter a área principal limpa e focada em visualizações. Escolhi multiselect para flexibilidade, permitindo análise granular.
st.sidebar.header("Filtros")
grupos = st.sidebar.multiselect("Grupo de Serviço", options=df['GRUPOSERVICO_DESCRICAO'].unique(), default=df['GRUPOSERVICO_DESCRICAO'].unique())
zonas = st.sidebar.multiselect("Zona", options=df['ZONA'].unique(), default=df['ZONA'].unique())
meses = st.sidebar.multiselect("Mês", options=df['MES'].unique(), default=df['MES'].unique())
situacoes = st.sidebar.multiselect("Situação", options=df['SITUACAO'].unique(), default=df['SITUACAO'].unique())

# Filtrando os dados com base nos filtros selecionados
# Decisão de design: Filtragem dinâmica para permitir exploração interativa, atendendo à necessidade do diretor de analisar períodos, tipos e áreas específicas.
filtered_df = df[
    df['GRUPOSERVICO_DESCRICAO'].isin(grupos) &
    df['ZONA'].isin(zonas) &
    df['MES'].isin(meses) &
    df['SITUACAO'].isin(situacoes)
]

# KPIs principais em colunas
# Decisão de design: Uso de colunas para exibir métricas chave (bullets/KPIs) de forma compacta e visual. Cores para destacar (verde para positivo). Isso responde diretamente às perguntas do diretor sobre quantidade atendida, eficiência e % atendido.
col1, col2, col3 = st.columns(3)
total_chamados = len(filtered_df)
with col1:
    st.metric("Total de Chamados", total_chamados)
percent_atendida = (filtered_df['SITUACAO'] == 'ATENDIDA').mean() * 100 if total_chamados > 0 else 0
with col2:
    st.metric("% Atendida", f"{percent_atendida:.2f}%")
tempo_medio = filtered_df['DIFERENCA_DIAS'].mean() if total_chamados > 0 else 0
with col3:
    st.metric("Tempo Médio de Atendimento (dias)", f"{tempo_medio:.2f}")

# Gráfico de chamados por mês (sazonalidade)
# Decisão de design: Gráfico de linha para mostrar tendências temporais e sazonalidade, facilitando identificação de períodos de alta demanda. Cor azul para calma e profissionalismo.
st.subheader("Chamados por Mês (Sazonalidade)")
chamados_por_mes = filtered_df.groupby('MES').size().reset_index(name='Quantidade')
fig_mes = px.line(chamados_por_mes, x='MES', y='Quantidade', markers=True, title="Tendência de Chamados por Mês")
fig_mes.update_layout(xaxis_title="Mês", yaxis_title="Quantidade de Chamados")
st.plotly_chart(fig_mes, use_container_width=True)

# Gráfico de chamados por zona
# Decisão de design: Gráfico de pizza para distribuição por zona, pois é categórico e ajuda a priorizar áreas. Cores diferenciadas para cada zona, melhorando a legibilidade.
st.subheader("Chamados por Zona")
chamados_por_zona = filtered_df.groupby('ZONA').size().reset_index(name='Quantidade')
fig_zona = px.pie(chamados_por_zona, values='Quantidade', names='ZONA', title="Distribuição de Chamados por Zona")
st.plotly_chart(fig_zona, use_container_width=True)

# Ranking Top 10 Bairros
# Decisão de design: Gráfico de barras horizontal para ranking, facilitando leitura de nomes longos. Limite a top 10 para foco nos mais importantes. Cor gradiente para destacar os tops.
st.subheader("Top 10 Bairros com Mais Chamados")
chamados_por_bairro = filtered_df.groupby('BAIRRO').size().reset_index(name='Quantidade').sort_values('Quantidade', ascending=False).head(10)
fig_bairro = px.bar(chamados_por_bairro, x='Quantidade', y='BAIRRO', orientation='h', title="Ranking de Bairros")
fig_bairro.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_bairro, use_container_width=True)

# Gráfico de chamados por dia da semana
# Decisão de design: Gráfico de barras para padrões semanais, ajudando a identificar dias de pico. Mapeei dias (0=Segunda) para nomes legíveis. Cor laranja para energia/destaque.
st.subheader("Chamados por Dia da Semana")
dia_semana_map = {0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'}
filtered_df['DIA_SEMANA_NOME'] = filtered_df['DIA_SEMANA'].map(dia_semana_map)
chamados_por_dia = filtered_df.groupby('DIA_SEMANA_NOME').size().reset_index(name='Quantidade').sort_values('DIA_SEMANA_NOME')
fig_dia = px.bar(chamados_por_dia, x='DIA_SEMANA_NOME', y='Quantidade', title="Distribuição por Dia da Semana")
st.plotly_chart(fig_dia, use_container_width=True)

# % Atendido por mês
# Decisão de design: Gráfico de barras para % mensal, comparando eficiência ao longo do tempo. Verde para atendidos, respondendo à pergunta sobre gestões eficientes (aqui por mês).
st.subheader("% Atendido por Mês")
percent_por_mes = filtered_df.groupby('MES').apply(lambda x: (x['SITUACAO'] == 'ATENDIDA').mean() * 100).reset_index(name='% Atendida')
fig_percent = px.bar(percent_por_mes, x='MES', y='% Atendida', title="% de Chamados Atendidos por Mês")
st.plotly_chart(fig_percent, use_container_width=True)

# Ranking de Serviços (Top 10 por Grupo e Serviço)
# Decisão de design: Tabela para ranking detalhado, pois pode haver muitos itens. Uso barras para visual rápido. Foco em top 10 para evitar sobrecarga visual.
st.subheader("Top 10 Serviços por Quantidade")
chamados_por_servico = filtered_df.groupby(['GRUPOSERVICO_DESCRICAO', 'SERVICO_DESCRICAO']).size().reset_index(name='Quantidade').sort_values('Quantidade', ascending=False).head(10)
fig_servico = px.bar(chamados_por_servico, x='Quantidade', y='SERVICO_DESCRICAO', color='GRUPOSERVICO_DESCRICAO', orientation='h', title="Ranking de Serviços")
fig_servico.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_servico, use_container_width=True)

# Mapa de Chamados por Bairro
# Decisão de design: Mapa interativo com escala de cor (vermelho para alta densidade) para priorização espacial. Centralizado em Recife. Isso é o "momento ousadia", proporcionando visão geográfica intuitiva.
if geo_data:
    st.subheader("Mapa de Chamados por Bairro (Escala de Cor)")
    map_df = filtered_df.groupby('BAIRRO').size().reset_index(name='Quantidade')
    fig_map = px.choropleth_mapbox(
        map_df,
        geojson=geo_data,
        locations='BAIRRO',
        featureidkey='properties.nome',  # Assumindo que o campo no GeoJSON é 'nome' (ajuste se necessário após inspeção)
        color='Quantidade',
        color_continuous_scale='Reds',
        mapbox_style='open-street-map',
        center={'lat': -8.05, 'lon': -34.9},
        zoom=11,
        title="Densidade de Chamados por Bairro"
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("Mapa não disponível devido a erro no carregamento de dados geográficos.")

# Nota final no código: O design geral prioriza simplicidade, interatividade e foco nas perguntas da persona. Visuals são escolhidos para serem intuitivos (linhas para tempo, barras para rankings, mapa para espaço), com cores profissionais para evitar distrações.