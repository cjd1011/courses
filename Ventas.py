#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#pip install openpyxl
import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit

#Streamlit run Ventas.py

st.set_page_config(page_title = 'Reporte de Ventas', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = 'moneybag:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

st.title(':clipboard: Reporte de Ventas') #Titulo del Dash
st.subheader('Compañía TECH SAS')
st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown
                   
archivo_excel = 'Reporte de Ventas.xlsx' 
hoja_excel = 'BASE DE DATOS' 

df = pd.read_excel(archivo_excel,
                   sheet_name = hoja_excel,
                   usecols = 'A:P')
                   #header = 0

#st.dataframe(df) 

st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
vendedor = st.sidebar.multiselect(
    "Seleccione el Vendedor:",
    options = df['Vendedor'].unique(),
    default = df['Vendedor'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

status_factura = st.sidebar.multiselect(
    "Factura Pagada (?):",
    options = df['Pagada'].unique(),
    default = df['Pagada'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

ciudad = st.sidebar.multiselect(
    "Seleccione Ciudad:",
    options = df['Ciudad'].unique(),
    default = df['Ciudad'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

industria = st.sidebar.multiselect(
    "Seleccione Industria:",
    options = df['Industria'].unique(),
    default = df['Industria'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

cliente = st.sidebar.multiselect(
    "Seleccione Cliente:",
    options = df['Cliente'].unique(),
    default = df['Cliente'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

plazo = st.sidebar.multiselect(
    "Seleccione plazo:",
    options = df['Términos'].unique(),
    default = df['Términos'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)



###Aqui es donde pasa la MAGIA. conectar los selectores con la base de datos


df_seleccion = df.query("Vendedor == @vendedor  & Ciudad == @ciudad & Pagada ==@status_factura & Industria ==@industria & Cliente ==@cliente & Términos ==@plazo " ) #el primer city es la columna y el segundo es el selector



total_ventas = int(df_seleccion['Valor'].sum())

total_facturas = int(df_seleccion['Valor'].count())

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Ventas Totales:")
    st.subheader(f"US $ {total_ventas:,}")

with right_column:
    st.subheader('Facturas:')
    st.subheader(f" {total_facturas}")
            
 
st.markdown("---") 

st.dataframe(df_seleccion) 

ventas_por_cliente = (df_seleccion.groupby(by=['Cliente']).sum()[['Valor']].sort_values(by='Valor'))

#Guardar el gráfico de barras en la siguiente variable

fig_ventas_cliente = px.bar(
    ventas_por_cliente,
    x = 'Valor',
    y=ventas_por_cliente.index, #se pone el index porque esta como index esa columna dentro del df nuevo que creamos que esta agrupado
    orientation= "h", #horizontal bar chart
    title = "<b>Ventas por Cliente</b>", #con las b lo que hago es ponerlo en bold
    color_discrete_sequence = ["#f5b932"] * len(ventas_por_cliente),
    template='plotly_white',

)

fig_ventas_cliente.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid = False))
    
)

ventas_por_vendedor = (
    df_seleccion.groupby(by=['Vendedor']).sum()[['Valor']].sort_values(by='Valor')
)



#Crear la gráfica de barras para los vendedores
fig_ventas_por_vendedor = px.bar(
    ventas_por_vendedor,
    x=ventas_por_vendedor.index,
    y='Valor',
    title = '<b>Ventas por Vendedor</b>',
    color_discrete_sequence = ["#F5B932"]*len(ventas_por_vendedor),
    template = 'plotly_white',
)

fig_ventas_por_vendedor.update_layout(
    xaxis=dict(tickmode='linear'), # se asegura que todos los ejes de X se muestren
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False)),
   
)    

## QUIERO PONER LAS DOS GRAFICAS A CADA LADO, UNA AL LADO DE LA OTRA

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_ventas_por_vendedor, use_container_width = True) #esta va al lado izquierdo
right_column.plotly_chart(fig_ventas_cliente, use_container_width = True)


# Hide Streamlit Style

hide_st_style = """
            <style>
   
            footer {visibility: hidden;}
           
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html= True)
