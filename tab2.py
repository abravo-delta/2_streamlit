import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

def tab2():
    archivo = st.file_uploader("Suba los traspasos internos", type=["xlsx"], key = "file2")
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

        with col1:
            st.write("Ingresos")
            df_in = st.dataframe(df_ingreso)
            df_ingreso = df_ingreso.drop(columns=['P*Q','Dif'])
            file_path = "Ingresos.xlsx"
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                df_ingreso.to_excel(writer, index=False)
            with open(file_path, "rb") as f:
                st.download_button("Descargar Ingresos", f, file_name="Ingresos.xlsx")                

        with col2:
            st.write("Egresos")
            df_eg = st.dataframe(df_egreso)
            df_egreso = df_egreso.drop(columns=['P*Q','Dif'])
            file_path = "Egresos.xlsx"
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                df_egreso.to_excel(writer, index=False)
            with open(file_path, "rb") as f:
                st.download_button("Descargar Egresos", f, file_name="Egresos.xlsx")
