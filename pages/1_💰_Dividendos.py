import streamlit as st
import pandas as pd
from datetime import timedelta
from pages.auxiliares import *

funcion =  '''Visibiliza los dividendos y repartos de capital de acciones nacionales y fondos mutuos nacionales presentes en cartera dentro del mes vigente.''' 

inputs = '''1. **Cartola de Dividendos**: Abrir el boletín bursatil del último día habil disponible en la [Bolsa de Santiago](https://www.bolsadesantiago.com/estadisticas_boletinbursatil). Ir a la sección "Noticias Bursátiles", subsección "Resumenes" y descargar el "Resumen de Dividendos, Repartos de Capital y Emisiones de Acciones y Cuotas". Luego subirlo.  
2. **Reportes de Carteras Vigentes Resumidas**: Abrir GPI y descargar las Carteras Vigentes Resumidas de Cada Fondo que tenga Fondos Mutuos Nacionales o Acciones nacionales. Luego, subirlas todas juntas. 
'''

# Configuración de la página
config_page("Dividendos", "💰", funcion, inputs)

# Variables
fecha = traer_fecha()
mes = fecha + timedelta(days=90)
ayer = fecha - timedelta(days=1)

# Funciones 

# Leer hojas de dividendos
def dividendos():
    div_xlsx = st.file_uploader("Suba la cartola de dividendos", 
                                type=["xlsx"], 
                                key = "file1")
    if div_xlsx:
        div_acc_int_df = cartola_dividendos(div_xlsx, "Dividendos acciones nacionales", 10)
        div_cfi_int_df = cartola_dividendos(div_xlsx, "Dividendos CFI nacionales" , 10)
        rep_cfi_cfi_df = cartola_dividendos(div_xlsx, "Repartos CFI-CFM" , 9)
        div_acc_ext_df = cartola_dividendos(div_xlsx, "Dividendos emisores extranjeros" , 10)
        dividendos_df = pd.concat([div_acc_int_df,
                                   div_cfi_int_df,
                                   rep_cfi_cfi_df,
                                   div_acc_ext_df])
        dividendos_df = dividendos_df.sort_values(by='Límite (1)')
        return dividendos_df

# Leer hoja de cartola de dividendos
def cartola_dividendos(div_xlsx, hoja, column1):
    df = pd.read_excel(div_xlsx, sheet_name=hoja)
    columnas = df.iloc[column1, :].values
    df = df.iloc[column1+1:, :]
    df.columns = columnas
    try:
        df = df.rename(columns={'Pesos': 'Nemotécnico', 
                                'Mercado': 'Tipo Instrumento', 
                                'Ex Date (1)': 'Límite (1)'})
    except:
        pass
    df = limpieza_cartola(df)
    return df

# Ajustar cartola de dividendos
def limpieza_cartola(df):
    limite_no_nulo = pd.notnull(df['Límite (1)']) & (df['Límite (1)'] != "-") & (df['Límite (1)'] != "None")
    pago_no_nulo = pd.notnull(df['Pago']) & (df['Pago'] != "-") & (df['Pago'] != "None")    
    df = df[limite_no_nulo & pago_no_nulo]
    limite_nuevo = (df['Límite (1)'] >= ayer) | (df['Pago'] >= ayer)
    limite_cerca = (df['Límite (1)'] <= mes) | (df['Pago'] <= mes)
    df = df[limite_nuevo & limite_cerca]

    df = df[['Nemotécnico', 
             'Tipo Instrumento', 
             'Moneda', 
             'Por Acción / cuota', 
             'Límite (1)', 
             'Pago']]

    df[['Límite (1)', 'Pago']] = df[['Límite (1)', 'Pago']].apply(lambda col: pd.to_datetime(col).dt.strftime('%d-%m-%Y'))
    return df

# Leer carteras
def carteras():
    dataframes = []
    uploaded_files = st.file_uploader("Suba las carteras vigentes resumidas", type=["xlsx"], key = "cvr", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_excel(uploaded_file, sheet_name="CARTERARES")
            df = df.iloc[3:, 1:3]
            df.columns = ['Fondo', 'Nemotécnico']
            dataframes.append(df)
        return pd.concat(dataframes, ignore_index=True)

# Layout
col1, col2 = st.columns(2)
with col1:
    dividendos_df = dividendos()
with col2:
    carteras_df = carteras()

if carteras_df is not None and dividendos_df is not None:
    dividendos_df = pd.merge(carteras_df, dividendos_df, on='Nemotécnico', how='inner')
    dividendos_df['Límite (1)'] = pd.to_datetime(dividendos_df['Límite (1)'])
    dividendos_df = dividendos_df.sort_values('Límite (1)')
    dividendos_df['Límite (1)'] = dividendos_df['Límite (1)'].dt.strftime('%d-%m-%Y')
    st.dataframe(dividendos_df)