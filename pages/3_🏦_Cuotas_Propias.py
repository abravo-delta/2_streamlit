import streamlit as st
import pandas as pd
import pdfplumber
import numpy as np
from pages.auxiliares import *
from random import *

funcion =  '''Entrega archivo de compra o venta de cuotas propias para GPI según su prefactura.''' 

inputs = '''Prefactura de compra y venta de cuotas propias disponible en el sitio web del cliente. 
'''

# Configuración de la página
config_page("Cuotas Propias", "🏦", funcion, inputs)

# Funciones
def leer_factura(factura):
    df = pd.DataFrame(factura)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df = df[:-1]
    df[['COMPRA', 'VENTA']] = df[['COMPRA', 'VENTA']].replace('', np.nan).applymap(lambda x: int(x.replace('.', '')) if pd.notna(x) else np.nan)
    df['OPERACION'] = df.apply(lambda x: 'Compra' if x['COMPRA'] != 0 and pd.notnull(x['COMPRA']) else 'Venta', axis=1)
    df['Cuenta'] = "76081068-1/0"
    df['Nemotecnico'] = df['DOCUMENTO'].apply(lambda x: x.split()[0] if pd.notnull(x) else None)
    df['Tipo Precio'] = "L"
    df['Cantidad'] = df['CANTIDAD']
    df['PRECIO'] = df['PRECIO'].apply(lambda x: float(x.replace('.', '').replace(',', '.')) if x != '' else np.nan)
    df['Precio'] = df['PRECIO']
    df[['Fecha Operacion', 'Fecha liquidacion']] = df['DOCUMENTO'].dropna().str.split().apply(lambda x: pd.Series([x[-1], x[-1]])).values
    df['Monto'] = df['COMPRA'] + df['VENTA']
    name = df['OPERACION'].iloc[0] 
    df = df[['Cuenta', 'Nemotecnico', 'Tipo Precio', 'Cantidad', 'Precio', 'Fecha Operacion', 'Fecha liquidacion', 'Monto']]
    return df, name

# Layout
uploaded_files = st.file_uploader("Entregue el reporte", type="pdf", accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        with pdfplumber.open(uploaded_file) as pdf:
            table = pdf.pages[0].extract_table()
            if table:
                df, name = leer_factura(table)
                st.header(name+" de Cuotas Propias")
                st.dataframe(df)
                boton_descarga_xlsx(df, name, nombre_hoja="Sheet1")