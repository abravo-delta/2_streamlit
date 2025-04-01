import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
from pages.auxiliares import *

# Configuración de la página
config_page("Welcome", "🏠")

col1, col2 = st.columns([4,1])

# Fecha
with col2:
    hoy = datetime.today()
    fecha = st.date_input('Fecha', value=hoy)
    fecha = datetime.combine(fecha, datetime.min.time())
    st.session_state['fecha'] = fecha

directory = "pages"
files = os.listdir(directory)
df = pd.DataFrame(files, columns=['file_name'])
df['section_name'] = df['file_name'].str.replace("_", " ", regex=False)
df['section_name'] = df['section_name'].str.replace(".py", "", regex=False)
df['section_name'] = df['section_name'].apply(lambda x: " ".join(x.split()[1:]))

try:
    df = df[~df['section_name'].isin(["", "auxiliares", "init", "pycache"])]
except ValueError:
    pass

# Extraer la variable `funcion` de cada archivo
def extract_function_value_safely(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'^funcion\s*=\s*(.+)', line)
                if match:
                    value = match.group(1)
                    return eval(value, {}, {})  # Solo evaluamos esa línea
        return 'funcion not found'
    except Exception as e:
        return f'Error: {e}'
 
# Aplicar a cada archivo en el df
df['funcion'] = df['file_name'].apply(lambda fn: extract_function_value_safely(os.path.join('pages', fn)))


# Descripción
with col1:
    st.markdown("## ¡Hola!")
    st.markdown(f'''
                Te damos la bienvenida a la página web de apoyo en los procesos diarios del area de Operaciones de Delta, Servicios Financieros.  
                El sitio tiene secciones que te permitirán realizar distintas tareas de forma rápida, intuitiva y sencilla,  
                Ahora mismo te encuentras en la sección :blue-background[Página principal]. Pero tenemos otras {len(files)} secciones que puedes explorar:
                ''')
    for _, row in df.iterrows():
        section = row['section_name']
        funcion = row['funcion']
        file_name = row['file_name']
        # Mostrar en un expander
        with st.expander(section):
            st.write(funcion)
            directorio = "pages/" + file_name
            st.page_link(directorio, label = "🔗 Ir al sitio")

# Puntuación
with col2:
    st.text("¿Qué te pareció la página?")
    sentiment_mapping = ["uno", "dos", "tres", "cuatro", "cinco"]
    selected = st.feedback("stars")