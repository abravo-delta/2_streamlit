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
    # Borra columnas innecesarias
    df_x = df[df.iloc[:, i].notna()].drop(df.columns[j], axis=1)
    # Renombra cantidad
    df_x.columns.values[3] = "Cantidad" 
    # Redondea el monto
    df_x['Monto'] = df_x['Monto'].round(0)
    df_x = crear_variables_validacion(df_x)
    return df_x

def crear_variables_validacion(df_x):
    df_x['P*Q'] = df_x['Cantidad'] * df_x['Precio']
    df_x['P*Q'] = df_x['P*Q'].apply(lambda x:round(x,0))
    df_x['Dif'] = df_x['Monto'] - df_x['P*Q']
    df_x['Dif'] = df_x['Dif'].abs()        
    return df_x

def validar(df, tipo):
    sum_q = df.groupby("Nemotecnico")["Cantidad"].sum().reset_index()
    sum_q = sum_q.rename(columns={"Cantidad": f"Cantidad {tipo}"})

    prom_p = df.groupby("Nemotecnico")["Precio"].mean().reset_index()
    prom_p = prom_p.rename(columns={"Precio": f"Precio {tipo}"})

    sum_monto = df.groupby("Nemotecnico")["Monto"].sum().reset_index()
    sum_monto = sum_monto.rename(columns={"Monto": f"Monto {tipo}"})

    # Unir todo por "Nemotecnico"
    df_final = sum_q.merge(prom_p, on="Nemotecnico").merge(sum_monto, on="Nemotecnico")

    return df_final


def leer_traspasos(archivo):
    df = pd.read_excel(archivo, sheet_name="Hoja1")
    # Definir area de tabla
    cuenta = df.iloc[:, 1].count()
    df = df.iloc[1:cuenta+1,1:]
    # Modificar rut:
    df['Cuenta'] = df['Cuenta'].apply(lambda x: x[:-3] + '-' + x[-3:])
    # Ajustar fechas
    df['Fecha Operacion'] = fecha.strftime('%d/%m/%Y')
    df['Fecha liquidacion'] = fecha.strftime('%d/%m/%Y')
    # Separar base en ingresos y egresos. 
    df_ingreso = separar_traspasos(4, 3, df)
    df_egreso = separar_traspasos(3, 4, df)
    validador_ing = validar(df_ingreso, "Ingreso")
    validador_egr = validar(df_egreso, "Egreso")
    validador = validador_ing.merge(validador_egr, on="Nemotecnico")

    return df_ingreso, df_egreso, validador

# Layout
archivo = st.file_uploader("Suba los traspasos internos", type=["xlsx"], key = "file2")
if archivo:
    df_ingreso, df_egreso, res_traspasos = leer_traspasos(archivo)

    for i in range(len(res_traspasos)):
        if res_traspasos["Cantidad Ingreso"][i] == res_traspasos["Cantidad Egreso"][i] and res_traspasos["Precio Ingreso"][i] == res_traspasos["Precio Egreso"][i] and res_traspasos["Monto Ingreso"][i] == res_traspasos["Monto Egreso"][i]:
            col1, col2 = st.columns([3, 8])

            with col1:
                st.success('Sin Diferencias', icon="✅")
            with col2:
                filtro = res_traspasos[['Nemotecnico' ,'Cantidad Ingreso', 'Precio Ingreso', 'Monto Ingreso']]
                filtro = filtro.rename(columns={"Cantidad Ingreso":"Cantidad", "Precio Ingreso":"Precio", "Monto Ingreso":"Monto"})
                filtro = filtro[filtro['Nemotecnico'] == res_traspasos["Nemotecnico"][i]]
                st.dataframe(filtro)
        else:
            col1, col2 = st.columns([3, 8])    
            with col1:
                st.error('Diferencias', icon="🚨")
            with col2:
                res_filtrado = res_traspasos[res_traspasos["Monto Ingreso"] != res_traspasos["Monto Egreso"]]
                st.dataframe(res_filtrado)
    
    # Descarga
    col1, col2 = st.columns(2)

    with col1:
        df_ingreso = df_ingreso.drop(columns=['P*Q','Dif'])
        file_path = "Ingresos.xlsx"
        boton_descarga_xlsx(df_ingreso, "Ingresos", nombre_hoja="Sheet1")

    with col2:
        df_egreso = df_egreso.drop(columns=['P*Q','Dif'])
        file_path = "Egresos.xlsx"
        boton_descarga_xlsx(df_egreso, "Egreso", nombre_hoja="Sheet1")
