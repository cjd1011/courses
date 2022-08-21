#!/usr/bin/env python
# coding: utf-8

# In[ ]:

### INSTALAMOS LAS LIBRERIAS NECESARIAS

import pandas as pd
import streamlit as st
import plotly.express as px
#from PIL import Image

st.set_page_config(page_title="Encuesta Oficial EPS") # Nombre para configurar la pagina web
st.header('Resultados Encuestas Nacionales EPS Colombia 2022') #Va a ser el titulo de la pagina
st.subheader('Cómo perciben los ciudadanos el servicio de las EPS en Colombia?') #Subtitulo

excel_file = 'ENCUESTA EPS.xlsx' #Nombre archivo a importar  'xlsx' hace referencia a excel

sheet_name = 'BD' #la hoja de excel que voy a importar

df = pd.read_excel(excel_file, #importo el archivo excel
                   sheet_name = sheet_name, #le digo cual hoja necesito
                   usecols = 'A:D', #aqui traigo las columnas que quiero usar
                   header =3) #desde que fila debe empezar a tomarme la informacion *Empieza a contar desde 0*

df_personas = df.groupby(['EPS'], as_index = False)['EDAD PERSONA ENCUESTADA'].count() #hago un tipo de TABLA DINAMICA para agrupar los datos de una mejor manera, lo que hago aqui es que por cada EPS, me cuente la cantidad de personas encuestadas***

df_personas2 = df_personas #la guardo en otro dataframe (NO ES NECESARIO)

st.dataframe(df) #de esta forma nos va a mostrar el dataframe en Streamlit
st.write(df_personas2) #este nos sirve cuando no tenemos dataframe sino object****

#Crear un grafico de torta (pie chart)

pie_chart = px.pie(df_personas2, #tomo el dataframe2
                   title = 'Total No. of Participants', #El titulo
                   values = 'EDAD PERSONA ENCUESTADA',##columna
                   names = 'EPS') ## para verlo por EPS --> Colores

st.plotly_chart(pie_chart) # de esta forma se va a mostrar el dataframe en Streamlit


#Crear una lista con los parametros de una columna

ciudad = df['CIUDAD'].unique().tolist() # se crea una lista unica de la columna CIUDAD
calificacion = df['CALIFICACION'].unique().tolist() # se crea una lista unica de la columna CALIFICACION
edad = df['EDAD PERSONA ENCUESTADA'].unique().tolist() # se crea una lista unica de la columna EDAD PERSONA ENCUESTADA

#Crear un slider de edad

edad_selector = st.slider('Edad persona encuestada:',
                          min_value = min(edad), #el valor minimo va a ser el valor mas pequeño que encuentre dentro de la columna EDAD PERSONA ENCUESTADA
                          max_value = max(edad),#el valor maximo va a ser el valor mas grande que encuentre dentro de la columna EDAD PERSONA ENCUESTADA
                          value = (min(edad),max(edad))) #que tome desde el minimo, hasta el maximo


#crear multiselectores

ciudad_selector = st.multiselect('Ciudad:',
                                 ciudad,
                                 default = ciudad)

calificacion_selector = st.multiselect('Calificacion:',
                                       calificacion,
                                       default = calificacion)


                                       
#Ahora necesito que esos selectores y slider me filtren la informacion

mask = (df['EDAD PERSONA ENCUESTADA'].between(*edad_selector))&(df['CIUDAD'].isin(ciudad_selector))&(df['CALIFICACION'].isin(calificacion_selector))

numero_resultados = df[mask].shape[0] ##number of availables rows
st.markdown(f'*Resultados Disponibles:{numero_resultados}*') ## sale como un titulo que dice cuantos resultados tiene para ese filtro

#una nueva agrupacion

df_agrupado = df[mask].groupby(by=['CALIFICACION']).count()[['EDAD PERSONA ENCUESTADA']] #que me agrupe por CALIFICACION y me cuente por los datos de  EDAD PERSONA ENCUESTADA
df_agrupado =df_agrupado.rename(columns={'EDAD PERSONA ENCUESTADA': 'Votos'})
df_agrupado =df_agrupado.reset_index()

#Crear un gráfico de barras

bar_chart = px.bar(df_agrupado, 
                   x='CALIFICACION',
                   y='Votos',
                   text ='Votos',
                   color_discrete_sequence = ['#f5b632']*len(df_agrupado),
                   template = 'plotly_white')

st.plotly_chart(bar_chart) #mostrar el grafico de barras en streamlit





