from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

#def tab1(fecha):
div_xlsx = st.file_uploader("Suba la cartola de dividendos", type=["xlsx"], key = "file1")
if div_xlsx:
        
    fecha = st.session_state.get['fecha', 'no se encuentra']
    mes = fecha + timedelta(days=30)

    def cartola_dividendos(hoja, column1):
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
        df = df[(df['Límite (1)'] >= fecha)&(df["Pago"] <= mes)]
        df = df[['Nemotécnico', 'Tipo Instrumento', 'Moneda', 'Por Acción / cuota', 'Límite (1)', 'Pago']]
        df['Límite (1)'] = pd.to_datetime(df['Límite (1)'])
        df['Pago'] = pd.to_datetime(df['Pago'])
        return df

    div_acc_int_df = cartola_dividendos("Dividendos acciones nacionales", 10)
    div_cfi_int_df = cartola_dividendos("Dividendos CFI nacionales" , 10)
    rep_cfi_cfi_df = cartola_dividendos("Repartos CFI-CFM" , 9)
    div_acc_ext_df = cartola_dividendos("Dividendos emisores extranjeros" , 10)

    dividendos_df = pd.concat([div_acc_int_df,div_cfi_int_df,rep_cfi_cfi_df,div_acc_ext_df])
    dividendos_df['Límite (1)'] = dividendos_df['Límite (1)'].dt.strftime('%d-%m-%Y')
    dividendos_df['Pago'] = dividendos_df['Pago'].dt.strftime('%d-%m-%Y')
    dividendos_df = dividendos_df.sort_values(by='Límite (1)')

    if dividendos_df.empty:
        st.write("")
    else:
        st.dataframe(dividendos_df)
