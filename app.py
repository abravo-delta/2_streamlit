import streamlit as st
from tab4 import extraer_bco_central
import pandas as pd
import openpyxl
from datetime import datetime
import numpy as np

print(pythoncom.__file__)
st.title("Robot Amanda y Max")
st.write("Robot que pretende ayudar a Amanda en automatizaciones")

tab1, tab2, tab3, tab4 = st.tabs([":moneybag: Dividendos", ":repeat: Traspasos internos", ":1234: Renta Fija", ":dollar: Paridades"])

with tab1:
    menu = st.selectbox("",["Dividendos nacionales", "Dividendos internacionales"])

with tab2:
    archivo = st.file_uploader("Sube un archivo Excel", type=["xlsx"])
    if archivo:
        df = pd.read_excel(archivo, sheet_name="Hoja1")
        
        # Edición general
        df = df.iloc[1:-4,1:]
        df['Cuenta'] = df['Cuenta'].apply(lambda x: x[:-3] + '-' + x[-3:])
        df['Fecha Operacion'] = datetime.today().strftime('%d/%m/%Y')
        df['Fecha liquidacion'] = datetime.today().strftime('%d/%m/%Y')

        # Mostrar
        st.write("Archivo inicial")
        st.dataframe(df)

        def separar_traspasos(i, j):
            df_x = df[df.iloc[:, i].notna()].drop(df.columns[j], axis=1)
            df_x.columns.values[3] = "Cantidad" 
            df_x['Monto'] = df_x['Monto'].round(0)
            df_x['P*Q'] = df_x['Cantidad'] * df_x['Precio']
            df_x['P*Q'] = df_x['P*Q'].apply(lambda x:round(x,0))
            df_x['Dif'] = df_x['Monto'] - df_x['P*Q']
            df_x['Dif'] = df_x['Dif'].abs()        
            return df_x
        
        # Ejecutar 
        df_egreso = separar_traspasos(3, 4)
        df_ingreso = separar_traspasos(4, 3)

        col1, col2 = st.columns(2)

        if sum(df_egreso['Dif']) != 0 and sum(df_ingreso['Dif']) != 0:
            st.write("Revisar Montos")
        # Errores
        with col1:
            if sum(df_ingreso['Cantidad']) != sum(df_egreso['Cantidad']):
                st.write("Alerta: Diferencia de cantidades")
            else:
                st.write("Ingresos")
                df_in = st.dataframe(df_ingreso)
        with col2: 
            if sum(df_ingreso['Monto']) != sum(df_egreso['Monto']):
                st.write("Alerta: Diferencia de monto")
            else: 
                st.write("Egresos")
                df_eg = st.dataframe(df_egreso)

        df_ingreso = df_ingreso.drop(columns=['P*Q','Dif'])
        df_egreso = df_egreso.drop(columns=['P*Q','Dif'])

        # Generar el archivo Excel automáticamente
        file_path = "Ingresos.xlsx"
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df_ingreso.to_excel(writer, index=False)
        file_path = "Egresos.xlsx"
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df_egreso.to_excel(writer, index=False)

        # Mostrar el botón de descarga directamente
        with col1:
            with open(file_path, "rb") as f:
                st.download_button("Descargar Ingresos", f, file_name="Ingresos.xlsx")
        with col2:
            with open(file_path, "rb") as f:
                st.download_button("Descargar Egresos", f, file_name="Egresos.xlsx")

with tab3:
    st.write("")

with tab4:
    st.write("")
    if st.button('Extraer y enviar el dolar del banco central'):
        extraer_bco_central()
