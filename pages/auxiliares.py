from datetime import datetime ,timedelta
import streamlit as st
from io import BytesIO
import pandas as pd

# Configuración de botón de ayuda
def help (funcion, inputs):
    st.markdown("##### Función")
    st.markdown(funcion)
    if inputs != "":
        st.markdown("##### Inputs")
        st.markdown(inputs)

# Configuración de las páginas con streamlit
def config_page(titulo, icono, funcion="", inputs=""):
    st.set_page_config(page_title=titulo, 
                       page_icon=icono, 
                       layout="wide",
                       initial_sidebar_state="expanded")
    st.sidebar.header(titulo)
    st.title(titulo)
    if funcion != "" or inputs !="":
        with st.expander("❔ Ayuda"):
            help(funcion, inputs)
#    with st.sidebar:
#        st.logo("/ISOTIPO.png", size="large")

# Extraer fecha de calendario de página principal
def traer_fecha():
    fecha = st.session_state.get('fecha', datetime.now())
    return fecha

# Botón generico de descarga de excel
def boton_descarga_xlsx(df, nombre, nombre_hoja="Sheet1"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=nombre_hoja)
    output.seek(0)
    st.download_button(
        label="Descargar "+nombre,
        data=output,
        file_name= nombre+".xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
    )
