import streamlit as st
import pandas as pd
from pages.auxiliares import config_page
from pages.auxiliares import *

funcion =  '''Compara ingresos y egresos entregados por el cliente, y genera archivos de descarga para GPI.''' 

inputs = '''* **Traspasos internos**: Excel recibido por correo con nombre Traspasos internos de cuotas en GPI. 
'''

# Configuración de la página
config_page("Traspasos internos", "🔁", funcion, inputs)

# Variables
fecha = traer_fecha()

# Funciones
def separar_traspasos(i, j, df):
    df_x = df[df.iloc[:, i].notna()].drop(df.columns[j], axis=1)
    df_x.columns.values[3] = "Cantidad" 
    df_x['Monto'] = df_x['Monto'].round(0)
    df_x['P*Q'] = df_x['Cantidad'] * df_x['Precio']
    df_x['P*Q'] = df_x['P*Q'].apply(lambda x:round(x,0))
    df_x['Dif'] = df_x['Monto'] - df_x['P*Q']
    df_x['Dif'] = df_x['Dif'].abs()        
    return df_x

def leer_traspasos(archivo):
    df = pd.read_excel(archivo, sheet_name="Hoja1")
    
    df = df.iloc[1:-4,1:]
    df['Cuenta'] = df['Cuenta'].apply(lambda x: x[:-3] + '-' + x[-3:])
    df['Fecha Operacion'] = fecha.strftime('%d/%m/%Y')
    df['Fecha liquidacion'] = fecha.strftime('%d/%m/%Y')

    df_egreso = separar_traspasos(3, 4, df)
    df_ingreso = separar_traspasos(4, 3, df)

    # Crear variables por nemo
    sum_q_ing = df_ingreso.groupby("Nemotecnico")["Cantidad"].sum().reset_index()
    sum_q_egr = df_egreso.groupby("Nemotecnico")["Cantidad"].sum().reset_index()
    prom_p_ing = df_ingreso.groupby("Nemotecnico")["Precio"].mean().reset_index()
    prom_p_egr = df_egreso.groupby("Nemotecnico")["Precio"].mean().reset_index()
    sum_monto_ing = df_ingreso.groupby("Nemotecnico")["Monto"].sum().reset_index()
    sum_monto_egr = df_egreso.groupby("Nemotecnico")["Monto"].sum().reset_index()

    # Juntar df
    res_traspasos = sum_q_ing.merge(sum_q_egr, on="Nemotecnico").merge(prom_p_ing, on="Nemotecnico").merge(prom_p_egr, on="Nemotecnico").merge(sum_monto_ing, on="Nemotecnico").merge(sum_monto_egr, on="Nemotecnico")
    res_traspasos = res_traspasos.rename(columns={"Cantidad_x":"Cantidad Ingreso", "Cantidad_y":"Cantidad Egreso", "Precio_x":"Precio Ingreso", "Precio_y":"Precio Egreso", "Monto_x":"Monto Ingreso", "Monto_y":"Monto Egreso"})

    return df_ingreso, df_egreso, res_traspasos

# Layout
archivo = st.file_uploader("Suba los traspasos internos", type=["xlsx"], key = "file2")
if archivo:
    df_ingreso, df_egreso, res_traspasos = leer_traspasos(archivo)

    for i in range(len(res_traspasos)):
        if res_traspasos["Cantidad Ingreso"][i] == res_traspasos["Cantidad Egreso"][i] and res_traspasos["Precio Ingreso"][i] == res_traspasos["Precio Egreso"][i] and res_traspasos["Monto Ingreso"][i] == res_traspasos["Monto Egreso"][i]:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(
                    """
                    <div style="background-color:#4CAF50; padding:1px; text-align:center; width:100%;">
                        <h4 style="color:white;">No hay diferencias</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                filtro = res_traspasos[['Nemotecnico' ,'Cantidad Ingreso', 'Precio Ingreso', 'Monto Ingreso']]
                filtro = filtro.rename(columns={"Cantidad Ingreso":"Cantidad", "Precio Ingreso":"Precio", "Monto Ingreso":"Monto"})
                filtro = filtro[filtro['Nemotecnico'] == res_traspasos["Nemotecnico"][i]]
                st.dataframe(filtro)
        else:
            col1, col2 = st.columns([1, 3])    
            with col1:
                st.markdown(
                    """
                    <div style="background-color:#E64C4C; padding:1px; text-align:center; width:100%;">
                        <h4 style="color:white;">Hay diferencias</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                st.dataframe(res_traspasos)
    
    # Descarga
    col1, col2 = st.columns(2)

    df_ingreso = df_ingreso.drop(columns=['P*Q','Dif'])
    file_path = "Ingresos.xlsx"
    boton_descarga_xlsx(df_ingreso, "Ingresos", nombre_hoja="Sheet1")

    df_egreso = df_egreso.drop(columns=['P*Q','Dif'])
    file_path = "Egresos.xlsx"
    boton_descarga_xlsx(df_egreso, "Egreso", nombre_hoja="Sheet1")
