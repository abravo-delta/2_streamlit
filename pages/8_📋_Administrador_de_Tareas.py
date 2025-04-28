import pandas as pd
import streamlit as st
from pages.auxiliares import *
import os

funcion = ""

inputs = ''''''

tareas_csv = "tareas.csv"

if os.path.exists(tareas_csv):
    df = pd.read_csv(tareas_csv)
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  
else:
    df = pd.DataFrame(columns=["Tarea", "Cliente", "Encargado", "Fecha", "Estado"])

# Configuración de la página
config_page("Administrador de Tareas", "📋", funcion, inputs)

clientes_list = ["Nevasa", "Prudential", "Otros"]
encargados_list = ["Alfredo", "Amanda", "Betania", "Gabriel", "José", "María José", "Maximiliano", "Tamara"]
estados_list = ["Pendiente", "En Proceso", "Finalizado"]

with st.expander("➕ Nueva tarea"):
    col1, col2 = st.columns(2)
    with col1:
        tarea = st.text_input("Tarea", " ")
        clientes =  st.selectbox("Cliente", clientes_list)
        encargados = st.multiselect("Encargado", encargados_list)
    with col2:
        fecha = st.date_input("Fecha", pd.to_datetime("today"))
        estado = st.selectbox("Estado", estados_list)
        if st.button("Agregar tarea"):
            new_row = pd.DataFrame([{"Tarea": tarea, 
                                     "Cliente": clientes,
                                     "Encargado": encargados,
                                     "Fecha": fecha,
                                     "Estado": estado}])
            df = pd.concat([df, new_row], ignore_index=True)  # Usar pd.concat en lugar de append
            df.to_csv(tareas_csv, index=False)
            st.success("Tarea agregada exitosamente!")

query = st.text_input("Filtro")

if query:
    mask = df.applymap(lambda x: query in str(x).lower()).any(axis=1)
    df = df[mask]

st.data_editor(df, 
               column_config={
                   "Tarea": st.column_config.TextColumn(),
                   "Cliente": st.column_config.SelectboxColumn(
                          options= clientes_list),
                   "Encargado": st.column_config.ListColumn(),
                   "Fecha": st.column_config.DateColumn(),
                   "Estado": st.column_config.SelectboxColumn(options=estados_list)
               },
               use_container_width=True)


