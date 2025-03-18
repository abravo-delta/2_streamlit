import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime, timedelta
import numpy as np
import tabula


# Configuración de la página
st.set_page_config(page_title="Aplicación Mandi y Maxi", layout="wide")

st.title("Robot procesos diarios")

# Fecha
hoy = datetime.today()
fecha = st.sidebar.date_input('Fecha', value=hoy)
fecha = datetime.combine(fecha, datetime.min.time())
st.session_state['fecha'] = fecha

# Menú
st.sidebar.title("Menú")
option = st.sidebar.selectbox("Selecciona una página:", ["Home", "Dividendos", "Traspasos", "Valorización", "Divisas", "MBI"])

if option == "Home":
    st.write("Bienvenido al robot de procesos diarios de Amanda.")
    st.write("Este robot tiene el objetivo de ayudar en las tareas básicas del equipo de operaciones. ¡Diviertete!")
    
elif option == "Dividendos":
    st.header(":moneybag: Dividendos")
    col1, col2 = st.columns(2)
    
    with col1:
        div_xlsx = st.file_uploader("Suba la cartola de dividendos", type=["xlsx"], key = "file1")
        if div_xlsx:
                
            fecha = st.session_state.get('fecha', 'no se encuentra')
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
 
    with col2:
        
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
        carteras_df = carteras()

    if carteras_df is not None and dividendos_df is not None:
        dividendos_df = pd.merge(carteras_df, dividendos_df, on='Nemotécnico', how='inner')
        st.dataframe(dividendos_df)

elif option == "Traspasos":
    st.header("Traspasos internos")
    fecha = st.session_state.get('fecha', 'no se encuentra')
    archivo = st.file_uploader("Suba los traspasos internos", type=["xlsx"], key = "file2")
    if archivo:
        df = pd.read_excel(archivo, sheet_name="Hoja1")
        
        # Edición general
        df = df.iloc[1:-4,1:]
        df['Cuenta'] = df['Cuenta'].apply(lambda x: x[:-3] + '-' + x[-3:])
        df['Fecha Operacion'] = fecha.strftime('%d/%m/%Y')
        df['Fecha liquidacion'] = fecha.strftime('%d/%m/%Y')

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

elif option == "Valorización":
    st.header("Generación de archivo para valorizar Renta Fija Nacional")
    fecha = st.session_state.get('fecha', 'no se encuentra')

    col1, col2 = st.columns(2)
    
    with col1:
        input = st.file_uploader("Suba el Archivo para valorizar cartera de Renta Fija Nacional Nevasa", type=["xlsx"], key = "rfn_nev")
        if input:
            input_df=pd.read_excel(input, sheet_name="SVC")
        
        rnf = st.file_uploader("Suba el reporte de cartera de Renta Fija Nacional", type=["xlsx"], key = "car_rfn")
        if rnf:
            rnf_df = pd.read_excel(rnf, sheet_name="CARTERARES")
            rnf_df = rnf_df.iloc[3:, [0, 1, 2, 22]]
            rnf_df.columns = ['Rut_fondo', 'Fondo', 'NEMO', 'Subclase']
            rnf_df['primera_letra'] = rnf_df['NEMO'].apply(lambda x: x[0])
            rnf_df['Subclase'] = rnf_df.apply(lambda row: "error" if row['primera_letra'] != "B" and row['Subclase'] == "BONO - Bono" else row['Subclase'], axis=1)
            valores_unicos = rnf_df['Subclase'].unique()
            opciones = list(valores_unicos)
            seleccionadas = st.multiselect('Selecciona opciones:', opciones)
            subclases = pd.DataFrame(seleccionadas, columns=['Subclase'])        

        if 'rnf_df' in locals() and 'input_df' in locals():
            merge1 = pd.merge(rnf_df, subclases, on='Subclase', how='inner')
            merge2 = pd.merge(input_df, merge1, on='NEMO', how='inner')
            merge2 = merge2.drop_duplicates()
            merge2 = merge2.iloc[:, 0:2]
        else:
            pass

    with col2:
        if 'merge2' in locals():
            st.dataframe(merge2)
            # Descargar en formato xls nombre Archivo Para Valorizar Cartera RENTA FIJA NACIONAL NEVASA (Risk America) dd-mm-yyyy_INPUT_OUT.
            file_path = "Archivo Para Valorizar Cartera RENTA FIJA NACIONAL NEVASA (Risk America) " + fecha.strftime('%d-%m-%Y') + "_INPUT_OUT.xlsx"
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                merge2.to_excel(writer, index=False)
            with open(file_path, "rb") as f:
                st.download_button("Descargar archivo", f, file_name=file_path)
        else:
            pass

elif option == "Divisas":
    pass
    #tab4.show()

elif option == "MBI":
    pass