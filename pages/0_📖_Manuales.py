import streamlit as st
from pages.auxiliares import *

funcion = "Notas sobre cómo realizar los principales procesos diarios del área de operaciones"

inputs = ''''''

# Configuración de la página
config_page("Manuales", "📖", funcion, inputs)

tab1, tab2 = st.tabs(["Nevasa", "Prudential"])

columnas = ['Secciones', 'Subsecciones']
nvs = [
    ['Valores Cuota', 'FMN: Fondos Mutuos Nacionales'],
    ['Dividendos', 'Dividendos Nacionales'],
    ['Dividendos', 'Dividendos Internacionales'],
    ['Traspasos Internos', 'Traspasos'],
    ['Nuevo Instrumento', 'Ingreso de Bonos'],
    ['Nuevo Instrumento', 'Ingreso de Grupo Económico'],
    ['Operaciones', 'Bonos'],
    ['Operaciones', 'Pagarés Descontables del Banco Central (PDBC)'],
    ['Operaciones', 'Depositos en Pesos'],
    ['Operaciones', 'Depositos en UF'],
    ['Operaciones', 'Cuotas Propias'],
    ['Operaciones', 'Pacto de Retrocompra'],
    ['Operaciones', 'Simultáneas'],
    ['Operaciones', 'Acciones'],
    ['Movimientos de Caja', 'Transferencias'],
    ['Movimientos de Caja', 'Pago de Remuneraciones del fondo'],
    ['Movimientos de Caja', 'Pago de Gastos del fondo'],
    ['Movimientos de Caja', 'Comisiones'],
    ['Precios Públicos en Risk América', 'Renta Fija Internacional'],
    ['Precios Públicos en Risk América', 'Renta Variable Internacional'],
    ['Precios Públicos en Risk América', 'RFN: Renta Fija Nacional'],
    ['Precios Públicos en Risk América', 'RVN: Renta Variable Nacional'],
    ['Precios Públicos en Risk América', 'INT: Internacional'],
    ['Divisas', 'Dólar Observado'],
    ['Divisas', 'IPC'],
    ['Cierre de fondo', 'Devengo'],
    ['Cierre de fondo', 'Vencimientos'],
    ['Cierre de fondo', 'Cortes de cupón'],
    ['Cierre de fondo', 'Cierre'],
    ['Cierre de fondo', 'Revisión del cierre'],
    ['Reportes', 'Reportes de Ahorro'],
    ['Reportes', 'Reportes de Otros Fondos'],
    ['Cuadratura de Cajas', 'Cajas Nacionales'],
    ['Cuadratura de Cajas', 'Cajas Internnacionales'],
    ['Cuadratura de Carteras', 'Carteras Nacionales'],
    ['Cuadratura de Carteras', 'Carteras Internacionales']    
]

df_nvs = pd.DataFrame(nvs, columns=columnas)

secciones_nvs = df_nvs['Secciones'].unique().tolist()

def opciones(secciones):
    options = st.selectbox("Categoría de Proceso", secciones)
    for seccion in secciones:
        if options == seccion:
            expansor_sec(seccion)
            break

def expansor_sec(seccion):
    subsecciones = df_nvs[df_nvs['Secciones'] == seccion]['Subsecciones'].tolist()
    for subseccion in subsecciones:
        expansor_sub(subseccion)

def expansor_sub(subseccion):
    with st.expander(subseccion):
        try:
            directorio = "Manual/"+subseccion+".md"
            with open(directorio, "r", encoding="utf-8") as file:
                md_subseccion = file.read()
                st.markdown(md_subseccion, unsafe_allow_html=True)
        except FileNotFoundError:
            st.write("Aún no tenemos manual para este proceso.")
with tab1:
    opciones(secciones_nvs)
with tab2:
    st.write("")