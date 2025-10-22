import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def tratamento_dados():
    #Carga dos dados
    df = pd.read_csv('Enlurb2024\\156_2024.csv', sep=';', encoding='latin-1')

    #Converter colunas
    df['DATA_DEMANDA'] = pd.to_datetime(df['DATA_DEMANDA'], format='%Y-%m-%d')
    df['DATA_ULT_SITUACAO'] = pd.to_datetime(df['DATA_ULT_SITUACAO'], format='%Y-%m-%d')

    #Criando novas colunas
    df['DIFERENCA_DIAS'] = (df['DATA_ULT_SITUACAO'] - df['DATA_DEMANDA']).dt.days #capturar tempo de execução
    df['MES'] = df['DATA_DEMANDA'].dt.month
    df['DIA'] = df['DATA_DEMANDA'].dt.day
    df['ANO'] = df['DATA_DEMANDA'].dt.year
    df['DIA_SEMANA'] = df['DATA_DEMANDA'].dt.dayofweek

    #Retirando colunas desnecessarias
    df = df.drop(columns=["GRUPOSERVICO_CODIGO", "SERVICO_CODIGO","LOGRADOURO","NUMERO", "latitude", "longitude"])

    #Converter RPA pra string
    df['RPA'] = df['RPA'].astype(str)

    #Carregar zonas
    mapeamento_zonas = {
        '1': 'Centro',
        '2': 'Norte',
        '3': 'Norte',
        '4': 'Oeste',
        '5': 'Sul',
        '6': 'Sul'
    }

    #mapear zonas
    df['ZONA'] = df['RPA'].map(mapeamento_zonas)
    df['ZONA'] = df['ZONA'].fillna('Não Informado')

    #Retirar valores onde o ano é diferente de 2024
    df = df[df['ANO']==2024]

    #Filtrar DRENAGEM, ILUMINACAO PUBLICA, LIMPEZA URBANA, ARBORIZACAO
    df = df[df['GRUPOSERVICO_DESCRICAO'].isin(['DRENAGEM', 'ILUMINAÇÃO PÚBLICA', 'LIMPEZA URBANA', 'ARBORIZAÇÃO'])]

    df['SITUACAO'].unique()

    return df
