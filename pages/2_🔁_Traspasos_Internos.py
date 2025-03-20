import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Traspasos internos", page_icon="🔁", layout="wide")
st.markdown("# Traspasos internos")
st.sidebar.header("Traspasos internos")

# Variables
fecha = st.session_state.get('fecha', 'no se encuentra')

# Funciones
def leer_traspasos(archivo):
    df = pd.read_excel(archivo, sheet_name="Hoja1")
    
    df = df.iloc[1:-4,1:]
    df['Cuenta'] = df['Cuenta'].apply(lambda x: x[:-3] + '-' + x[-3:])
    df['Fecha Operacion'] = fecha.strftime('%d/%m/%Y')
    df['Fecha liquidacion'] = fecha.strftime('%d/%m/%Y')

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
                df_ingreso = df_ingreso.drop(columns=['P*Q','Dif'])

    # Descarga
    col1, col2 = st.columns(2)
    file_path = "Ingresos.xlsx"
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df_ingreso.to_excel(writer, index=False)
    with open(file_path, "rb") as f:
        with col1:
            st.download_button("Descargar Ingresos", f, file_name="Ingresos.xlsx")                

    df_egreso = df_egreso.drop(columns=['P*Q','Dif'])
    file_path = "Egresos.xlsx"
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df_egreso.to_excel(writer, index=False)
    with open(file_path, "rb") as f:
        with col2:
            st.download_button("Descargar Egresos", f, file_name="Egresos.xlsx")