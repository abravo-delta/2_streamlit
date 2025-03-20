import streamlit as st
import pandas as pd
from datetime import timedelta

# Configuración de la página
st.set_page_config(page_title="Dividendos", page_icon="💰", layout="wide")
st.markdown("# Dividendos")
st.sidebar.header("Dividendos")

# Variables
fecha = st.session_state.get('fecha', 'no se encuentra')
mes = fecha + timedelta(days=30)
ayer = fecha - timedelta(days=1)

# Funciones 
# Leer cartola de dividendos por hoja
def cartola_dividendos(div_xlsx, hoja, column1):
    df = pd.read_excel(div_xlsx, sheet_name=hoja)
    columnas = df.iloc[column1, :].values
    df = df.iloc[column1+1:, :]
    df.columns = columnas
    try:
        df = df.rename(columns={'Pesos': 'Nemotécnico'})
        df = df.rename(columns={'Mercado': 'Tipo Instrumento'})
        df = df.rename(columns={'Ex Date (1)': 'Límite (1)'})
    except:
        pass
    df = df[(pd.notnull(df['Límite (1)']))&(df['Límite (1)'] != "-")&(df['Límite (1)'] != "None")]
    df = df[(pd.notnull(df["Pago"]))&(df["Pago"] != "-")&(df["Pago"] != "None")]
    df = df[(df['Límite (1)'] >= ayer)&(df["Pago"] <= mes)]
    df = df[['Nemotécnico', 'Tipo Instrumento', 'Moneda', 'Por Acción / cuota', 'Límite (1)', 'Pago']]
    df['Límite (1)'] = pd.to_datetime(df['Límite (1)'])
    df['Pago'] = pd.to_datetime(df['Pago'])
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

# Leer dividendos
def dividendos():
    div_xlsx = st.file_uploader("Suba la cartola de dividendos", type=["xlsx"], key = "file1")
    if div_xlsx:
        div_acc_int_df = cartola_dividendos(div_xlsx, "Dividendos acciones nacionales", 10)
        div_cfi_int_df = cartola_dividendos(div_xlsx, "Dividendos CFI nacionales" , 10)
        rep_cfi_cfi_df = cartola_dividendos(div_xlsx, "Repartos CFI-CFM" , 9)
        div_acc_ext_df = cartola_dividendos(div_xlsx, "Dividendos emisores extranjeros" , 10)
        dividendos_df = pd.concat([div_acc_int_df,div_cfi_int_df,rep_cfi_cfi_df,div_acc_ext_df])
        dividendos_df['Límite (1)'] = dividendos_df['Límite (1)'].dt.strftime('%d-%m-%Y')
        dividendos_df['Pago'] = dividendos_df['Pago'].dt.strftime('%d-%m-%Y')
        dividendos_df = dividendos_df.sort_values(by='Límite (1)')
        return dividendos_df

# Layout
col1, col2 = st.columns(2)
with col1:
    dividendos_df = dividendos()
with col2:
    carteras_df = carteras()

if carteras_df is not None and dividendos_df is not None:
    dividendos_df = pd.merge(carteras_df, dividendos_df, on='Nemotécnico', how='inner')
    st.dataframe(dividendos_df)