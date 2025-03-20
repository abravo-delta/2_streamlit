import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Robot procesos diarios", page_icon="🏠", layout="wide")
st.markdown("# Robot procesos diarios")
st.sidebar.header("Robot procesos diarios")

# Fecha
hoy = datetime.today()
fecha = st.sidebar.date_input('Fecha', value=hoy)
fecha = datetime.combine(fecha, datetime.min.time())
st.session_state['fecha'] = fecha

# Bienvenida
st.write("Bienvenido al robot de procesos diarios de Amanda.")
st.write("Este robot tiene el objetivo de ayudar en las tareas básicas del equipo de operaciones. ¡Diviertete!")

# Checklist
col1, col2 = st.columns(2)
with col1:
    st.header("Tareas generales")
    pendientes = pd.DataFrame({
        'checklist': [False],
        'Tarea': [''],
        'Subtarea': ['']
    })
    st.data_editor(pendientes, key="editor1", num_rows="dynamic")
with col2:
    st.header("Tareas diarias")
    dia_a_dia = pd.DataFrame({
        'checklist': [False],
        'Tarea': [''],
        'Subtarea': ['']
    })
    st.data_editor(dia_a_dia, key="editor2", num_rows="dynamic")