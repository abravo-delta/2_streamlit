import streamlit as st
import pandas as pd
from pages.auxiliares import *

funcion =  '''Genera archivo para ingresar a Risk America con nemotécnicos y cantidad de cada instrumento en cartera.''' 

inputs = '''1. **Interfaz salida Risk America**: Abrir GPI, dirigirse al menú de Interfaz de salida Risk America y descargar el archivo de Renta Fija Nacional. Luego subirlo.  
2. **Reporte de Cartera Vigente Resumida de Renta Fija**: Abrir GPI, dirigirse al menú de Reportes, seleccionar Cartera Vigente Resumida. Filtrar exclusivamente las operaciones de Renta Fija Nacional. Luego subirlo.  
3. **Instrumentos**: seleccionar instrumentos de Renta Fija Nacional con precios públicos, dígase. Bonos, Depósitos y Pagarés Descontables del Banco Central (PDBC).  
'''

# Configuración de la página
config_page("Generación de archivo para Risk America", "📈", funcion, inputs)

fecha = traer_fecha()

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
        seleccionadas = st.multiselect('Selecciona instrumentos:', opciones)
        subclases = pd.DataFrame(seleccionadas, columns=['Subclase'])        

    if 'rnf_df' in locals() and 'input_df' in locals():
        merge1 = pd.merge(rnf_df, subclases, on='Subclase', how='inner')
        merge2 = pd.merge(input_df, merge1, on='NEMO', how='inner')
        merge2 = merge2.drop_duplicates(subset=["NEMO", "CANTIDAD"])
        merge2 = merge2.iloc[:, 0:2]
    else:
        pass

with col2:
    if 'merge2' in locals():
        st.dataframe(merge2)
        boton_descarga_xlsx(merge2, "Archivo Para Valorizar Cartera RENTA FIJA NACIONAL NEVASA (Risk America) " + fecha.strftime('%d-%m-%Y'), nombre_hoja="Sheet1")
    else:
        pass