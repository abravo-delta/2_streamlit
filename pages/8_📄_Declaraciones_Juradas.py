import streamlit as st
import pandas as pd
from datetime import timedelta
from pages.auxiliares import *

funcion =  '''Manual y ejecutor de Declaraciones Juradas para el SII.''' 

inputs = '''Depende de cada declaración jurada.
'''

# Configuración de la página
config_page("Declaraciones Juradas", "📄", funcion, inputs)

# Anexos: 
dj1929_manual = {
    "i": ["0", "1", 
          "2_1", "2_2", "2_3", "2_4", "2_5", "2_6", 
          "2_7", "2_8", "2_9", "2_10", "2_11"],
    "título": [" ",
               " 1 Alcances", 
               " 2.1 Campos sobre Contraparte", 
               " 2.2 Campos sobre Acuerdo Marco",
               " 2.3 Campos sobre contrato o confirmación",
               " 2.4 Campos sobre el primer activo subyacente",
               " 2.5 Campos sobre el segundo activo subyacente",
               " 2.6 Campos sobre el Precio futuro contratado (futuros, forwards y opciones)",
               " 2.7 Campos sobre el Nocional",
               " 2.8 Campos sobre fechas claves",
               " 2.9 Campos sobre el precio subyacente",
               " 2.10 Campos sobre valorización",
               " 2.11 Otros campos"]
}

DJ1929, DJ1870, ANEXOS = st.tabs(["1929", "1870", "Anexos"])

with DJ1929:
    st.write("## Manual de Declaración Jurada 1929")
    seleccion = st.selectbox(
        "Selecciona una sección del manual:",
        options=dj1929_manual["título"]
    )
    indice = dj1929_manual["título"].index(seleccion)
    i = dj1929_manual["i"][indice]
    try:
        directorio = f"DJ/DJ1829_{i}.md"
        with open(directorio, "r", encoding="utf-8") as file:
            md_subseccion = file.read()
            st.markdown(md_subseccion, unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.write("Aún no tenemos manual para este proceso.")

with DJ1870:
    pass

with ANEXOS:
    CodigoPais =  st.text_input("Buscar Código de País:", )
    if CodigoPais:
        pais_DF = pd.read_csv("DJ/Cod_paises.csv")
        pais_mask = pais_DF.apply(lambda row: row.astype(str).str.contains(CodigoPais, case=False, na=False)).any(axis=1)
        filtered_pais = pais_DF[pais_mask]
        st.dataframe(filtered_pais, use_container_width=True)

    CodigoMoneda =  st.text_input("Buscar Código de País o Moneda:", )
    if CodigoMoneda:
        moneda_DF = pd.read_csv("DJ/Cod_moneda.csv")
        moneda_mask = moneda_DF.apply(lambda row: row.astype(str).str.contains(CodigoMoneda, case=False, na=False)).any(axis=1)
        filtered_moneda = moneda_DF[moneda_mask]
        st.dataframe(filtered_moneda, use_container_width=True)
    
    CodigoCurvas =  st.text_input("Buscar Código de Curva de tasa de interés:", )
    if CodigoCurvas:
        curva_DF = pd.read_csv("DJ/Cod_curvas.csv")
        curva_mask = curva_DF.apply(lambda row: row.astype(str).str.contains(CodigoCurvas, case=False, na=False)).any(axis=1)
        filtered_curva = curva_DF[curva_mask]
        st.dataframe(filtered_curva, use_container_width=True)