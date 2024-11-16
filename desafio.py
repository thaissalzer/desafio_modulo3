# Compilado

import requests
import pandas as pd
import streamlit as st

#identificando as mulheres

url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F'
resposta = requests.get(url).json()
dfMulheres = pd.DataFrame(resposta['dados'])
dfMulheres['sexo'] = 'F'
dfMulheres.head()

#identificando os homens

url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M'
resposta = requests.get(url).json()
dfHomens = pd.DataFrame(resposta['dados'])
dfHomens['sexo'] = 'M'
dfHomens.head()

#unindo os dataframes
df = pd.concat([dfMulheres, dfHomens])

#Filtrando df por sexo
#inserindo um selectbox
opcao = st.selectbox(
    'Qual o sexo?',
     df['sexo'].unique())

dfFiltrado = df[df['sexo'] == opcao]
st.title('Deputados do sexo ' + opcao)

#ocorrencias totais
#procurando no chat GPT: Como calcular a quantidade de deputados por estado?
ocorrencias = dfFiltrado['siglaUf'].value_counts()
dfEstados = pd.DataFrame({
    'siglaUf': ocorrencias.index,
    'quantidade': ocorrencias.values}
    )

# Total geral 
total_deputados= len(df)
#total de homens
totalHomens = dfHomens['id'].count()
st.metric('Total de Homens', totalHomens)
st.metric(f' {(totalHomens/total_deputados)*100}% dos deputados são homens')


#total de mulheres
totalMulheres = dfMulheres['id'].count()
st.metric('Total de Mulheres', totalMulheres)
st.metric(f' {(totalMulheres/total_deputados)*100}% dos deputados são mulheres')


st.write('Total de deputadas do sexo ' + opcao)
st.bar_chart(dfEstados, x = 'siglaUf', y = 'quantidade', x_label='Siglas dos estados', y_label='Quantidade de deputados')

st.dataframe(dfFiltrado)
