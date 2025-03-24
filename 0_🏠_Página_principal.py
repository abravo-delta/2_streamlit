import streamlit as st
import pandas as pd
from datetime import datetime
import os

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

# Función para cargar datos
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=['Checklist', 'Tarea', 'Subtarea'])

# Función para guardar datos
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Cargar datos
pendientes_path = 'pendientes.csv'
dia_a_dia_path = 'dia_a_dia.csv'

if 'pendientes' not in st.session_state:
    st.session_state['pendientes'] = load_data(pendientes_path)
    if st.session_state['pendientes'].empty:
        st.session_state['pendientes'] = pd.DataFrame({
            'Checklist': [False],
            'Tarea': [''],
            'Subtarea': ['']
        })

if 'dia_a_dia' not in st.session_state:
    st.session_state['dia_a_dia'] = load_data(dia_a_dia_path)
    if st.session_state['dia_a_dia'].empty:
        st.session_state['dia_a_dia'] = pd.DataFrame({
            'Checklist': [False],
            'Tarea': [''],
            'Subtarea': ['']
        })

# Checklist
col1, col2 = st.columns(2)
with col1:
    st.header("Tareas generales")
    st.session_state['pendientes'] = st.data_editor(st.session_state['pendientes'], key="editor1", num_rows="dynamic")
with col2:
    st.header("Tareas diarias")
    st.session_state['dia_a_dia'] = st.data_editor(st.session_state['dia_a_dia'], key="editor2", num_rows="dynamic")

# Guardar datos al cerrar la aplicación
if st.button('Guardar cambios'):
    save_data(st.session_state['pendientes'], pendientes_path)
    save_data(st.session_state['dia_a_dia'], dia_a_dia_path)
    st.success('Datos guardados correctamente')