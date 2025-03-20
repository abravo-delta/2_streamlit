import streamlit as st
import pandas as pd
import pdfplumber
from io import BytesIO
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Cuotas Propias", page_icon="🏦", layout="wide")
st.markdown("# Cuotas Propias")
st.sidebar.header("Cuotas Propias")

# Funciones
def leer_factura(factura):
    df = pd.DataFrame(factura)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df = df[:-1]
    df['COMPRA'] = df['COMPRA'].apply(lambda x: int(x.replace('.', '')) if x != '' else np.nan)
    df['VENTA'] = df['VENTA'].apply(lambda x: int(x.replace('.', '')) if x != '' else np.nan)
    df['OPERACION'] = df.apply(lambda x: 'Compra' if x['COMPRA'] != 0 and pd.notnull(x['COMPRA']) else 'Venta', axis=1)
    df['Cuenta'] = "76081068-1/0"
    df['Nemotecnico'] = df['DOCUMENTO'].apply(lambda x: x.split()[0] if pd.notnull(x) else None)
    df['Tipo Precio'] = "L"
    df['Cantidad'] = df['CANTIDAD']
    df['PRECIO'] = df['PRECIO'].apply(lambda x: float(x.replace('.', '').replace(',', '.')) if x != '' else np.nan)
    df['Precio'] = df['PRECIO']
    df['Fecha Operacion'] = df['DOCUMENTO'].apply(lambda x: x.split()[-1] if pd.notnull(x) else None)
    df['Fecha liquidacion'] = df['DOCUMENTO'].apply(lambda x: x.split()[-1] if pd.notnull(x) else None)
    df['Monto'] = df['COMPRA'] + df['VENTA']
    name = df['OPERACION'].iloc[0] 
    df = df[['Cuenta', 'Nemotecnico', 'Tipo Precio', 'Cantidad', 'Precio', 'Fecha Operacion', 'Fecha liquidacion', 'Monto']]
    # IDENDIFICAR VALOR EN OPERACION, primera fila, llamarlo name
    return df, name

# Layout
uploaded_file = st.file_uploader("Entregue el reporte", type="pdf")
if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        table = pdf.pages[0].extract_table()
        if table:
            df, name = leer_factura(table)
            st.header(name+" de Cuotas Propias")
            st.dataframe(df)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)
            st.download_button(
                label="Descargar archivo",
                data=output,
                file_name=name+".xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
