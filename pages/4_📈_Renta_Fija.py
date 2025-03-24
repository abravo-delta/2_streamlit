import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generación de archivo de Renta Fija", page_icon="📈", layout="wide")
st.markdown("# Generación de archivo de Renta Fija")
st.sidebar.header("Generación de archivo de Renta Fija")

st.header("Generación de archivo para valorizar Renta Fija Nacional")
fecha = st.session_state.get('fecha', 'no se encuentra')

col1, col2 = st.columns(2)

with col1:
    input = st.file_uploader("Suba el Archivo para valorizar cartera de Renta Fija Nacional Nevasa", type=["xlsx"], key = "rfn_nev")
    if input:
        input_df=pd.read_excel(input, sheet_name="SVC")
    
    rnf = st.file_uploader("Suba el reporte de cartera de Renta Fija Nacional", type=["xlsx"], key = "car_rfn")
    if rnf:
        rnf_df = pd.read_excel(rnf, sheet_name="CARTERARES")
        rnf_df = rnf_df.iloc[3:, [0, 1, 2, 22]]
        rnf_df.columns = ['Rut_fondo', 'Fondo', 'NEMO', 'Subclase']
        rnf_df['primera_letra'] = rnf_df['NEMO'].apply(lambda x: x[0])
        rnf_df['Subclase'] = rnf_df.apply(lambda row: "error" if row['primera_letra'] != "B" and row['Subclase'] == "BONO - Bono" else row['Subclase'], axis=1)
        valores_unicos = rnf_df['Subclase'].unique()
        opciones = list(valores_unicos)
        seleccionadas = st.multiselect('Selecciona opciones:', opciones)
        subclases = pd.DataFrame(seleccionadas, columns=['Subclase'])        

    if 'rnf_df' in locals() and 'input_df' in locals():
        merge1 = pd.merge(rnf_df, subclases, on='Subclase', how='inner')
        merge2 = pd.merge(input_df, merge1, on='NEMO', how='inner')
        merge2 = merge2.drop_duplicates()
        merge2 = merge2.iloc[:, 0:2]
    else:
        pass

with col2:
    if 'merge2' in locals():
        st.dataframe(merge2) 

        # Descargar en formato xls nombre Archivo Para Valorizar Cartera RENTA FIJA NACIONAL NEVASA (Risk America) dd-mm-yyyy.
        file_path = "Archivo Para Valorizar Cartera RENTA FIJA NACIONAL NEVASA (Risk America) " + fecha.strftime('%d-%m-%Y') + ".xlsx"
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            merge2.to_excel(writer, index=False)
        with open(file_path, "rb") as f:
            st.download_button("Descargar archivo", f, file_name=file_path)
    else:
        pass



