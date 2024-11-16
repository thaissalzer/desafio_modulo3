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
st.write(f' {(totalHomens/total_deputados)*100:.2f}% dos deputados são homens')


#total de mulheres
totalMulheres = dfMulheres['id'].count()
st.metric('Total de Mulheres', totalMulheres)
st.write(f' {(totalMulheres/total_deputados)*100:.2f}% dos deputados são mulheres')


st.write('Total de deputadas do sexo ' + opcao)
st.bar_chart(dfEstados, x = 'siglaUf', y = 'quantidade', x_label='Siglas dos estados', y_label='Quantidade de deputados')

st.dataframe(dfFiltrado)

# Calculando a porcentagem de mulheres por estado
total_estado = df['siglaUf'].value_counts()
mulheres_por_estado = dfMulheres['siglaUf'].value_counts()
percentual_mulheres = (mulheres_por_estado / total_estado * 100).dropna()

# Criando um dataframe para o gráfico
dfPercentualMulheres = pd.DataFrame({
    'Estado': percentual_mulheres.index,
    'Percentual de Mulheres (%)': percentual_mulheres.values
})

# Exibindo o gráfico de barras com o percentual de mulheres por estado
st.subheader('Percentual de Mulheres por Estado')
st.bar_chart(dfPercentualMulheres, x='Estado', y='Percentual de Mulheres (%)', x_label='Estados', y_label='Percentual (%)')
