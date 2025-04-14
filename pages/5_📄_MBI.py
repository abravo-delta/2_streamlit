import streamlit as st
import pdfplumber
import re
import fitz  # PyMuPDF
import pandas as pd
from pages.auxiliares import *

funcion = "Extrae las simultáneas de la cartola de MBI"
inputs = "Última y penúltima cartola de MBI"

# Configuración de la página
config_page("Cartola MBI", "📄", funcion, inputs)


# Variables
fecha = traer_fecha()
fecha = pd.to_datetime(fecha).strftime('%d-%m-%Y')
words_pages = []

def separate_columns(text):
    transactions = re.split(r'(?<=\d)\s+(?=[A-Z]{2,})', text.strip())
    separated_transactions = [re.split(r'\s+', transaction) for transaction in transactions]
    return separated_transactions

def format_date(date):
    if pd.isna(date):  # Verifica si el valor es NaN o None
        return ""
    return date.replace('-', '')

def extract_text(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page_text = pdf_document[page_num].get_text()
        words = page_text.split()[:]
        words_pages.append(' '.join(words))
    return words_pages

def leer_cartola(pdf_file, page):
    with pdfplumber.open(pdf_file) as pdf:
        if not page>len(pdf.pages):
            table = pdf.pages[page].extract_table()
            if table:
                data = "\n".join([" ".join(str(cell) if cell is not None else "" for cell in row) for row in table])
                transactions = re.split(r'\s+(?=[A-Z]{2,})', data.strip())
                transactions = [str(item).replace('+', '') for item in transactions]
                transactions = [str(item).replace('ORO', '') for item in transactions]
                transactions = [str(item).replace('BLANCO', 'ORO-BLANCO') for item in transactions]
                separated_columns = [re.split(r'\s+', transaction) for transaction in transactions]
                df = pd.DataFrame(separated_columns)
                df = df.iloc[:, :17]

                expected_columns = ['Instrumento', 
                            'Cantidad', 
                            'Plazo', 
                            'Tasa', 
                            'Borrar1', 
                            'Fecha_0', 
                            'Borrar2', 
                            'Monto_0', 
                            'Borrar3', 
                            'Borrar4', 
                            'Borrar5',
                            'Borrar6',
                            'Borrar7',
                            'Borrar8',
                            'Fecha_1',
                            'Borrar9',
                            'Monto_1']
                
                # Recortar o rellenar columnas según sea necesario
                if len(df.columns) > len(expected_columns):
                    df = df.iloc[:, :len(expected_columns)]
                elif len(df.columns) < len(expected_columns):
                    for i in range(len(df.columns), len(expected_columns)):
                        df[i] = None

                df.columns = expected_columns

                df = df.loc[:, ~df.columns.str.startswith('Borrar')]
                df = df[(df['Instrumento'] != 'Detalle') & (df['Instrumento'] != '')]
                df['Plazo'] = df['Plazo'].str.replace(' días', '').str.replace('días', '')
                df['Tasa'] = df['Tasa'].str.replace('%Compra', '')
                # Asegurarse de que las columnas Fecha_1 y Fecha_0 no tengan valores None
                df['Fecha_1'] = df['Fecha_1'].fillna("")
                df['Fecha_0'] = df['Fecha_0'].fillna("")
                df['Nemo'] = "SIM_" + df['Fecha_1'].apply(format_date) + "_" + df['Fecha_0'].apply(format_date) + "_" + df['Tasa'] + "_" + df['Instrumento']
                return df

def leer_caja(cartola_caja):
    st.write(cartola_caja)

def cartola_resumen(j):
    cartola_pdf = st.file_uploader("Suba la cartola de MBI de T" + str(j), type=["pdf"], key="mbi_"+str(j))
    if cartola_pdf:
        words_cart = extract_text(cartola_pdf)
        indices = []
        for i, words1 in enumerate(words_cart):
            if "Detalle Operaciones Vigentes Simultáneas" in words1:
                indices.append(i)
            else:
                pass
        tab = pd.concat([leer_cartola(cartola_pdf, x) for x in indices])
        tab['T'] = "T" + str(j)
        return tab


def caja():
    cartola_caja = st.file_uploader("Suba la cartola de MBI de T1", type=["pdf"], key="caja_1")
    if cartola_caja:
        with pdfplumber.open(cartola_caja) as pdf:
            indices = []
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if "Movimientos de caja CLP" in text:
                    indices.append(i)
            
            all_data = []
            for indice in indices:
                table = pdf.pages[indice].extract_text()
                if table:
                    texto = all_data.extend(table)
        
                    inicio_palabra_clave = "Saldo inicial del periodo 0"
                    fin_palabra_clave = "Saldo Final del Periodo"
    
                    inicio_indice = table.find(inicio_palabra_clave)
                    fin_indice = table.find(fin_palabra_clave)
    
                    if inicio_indice != -1 and fin_indice != -1:
                        texto_limpio = table[inicio_indice + len(inicio_palabra_clave):fin_indice]
            
                        texto_limpio = texto_limpio.replace('VENCIMIENTO DE OPERACIÓN A PLAZO DE VENTA', 'Vencimiento')
                        texto_limpio = texto_limpio.replace('CARGO POR DEPOSITO EN CTA CTE CLIENTE', 'TRANSFERENCIA A_CHILE')
                        texto_limpio = texto_limpio.replace('ANTICIPO SIMULTANEA VENTA PLAZO SIMULTÁNEA', 'Venta')
                        texto_limpio = texto_limpio.replace('ORO BLANCO', 'ORO-BLANCO')


                    # Split the text into lines
                    lines = texto_limpio.split('\n')

                    # Initialize an empty list to store the rows
                    rows = []

                    # Iterate over the lines and extract the data
                    for line in lines:
                        row = line.split(' ')
                        rows.append(row)

                    # Create a DataFrame from the rows
                    df = pd.DataFrame(rows)

                    columnas = ['Borrar1', 
                                'Borrar2', 
                                'Movimiento', 
                                'Instrumento', 
                                'Borrar3', 
                                'Fecha', 
                                'Cargo',
                                'Abono',
                                'Saldo']
                    df.columns = columnas
                    df = df.dropna()
                    df = df.loc[:, ~df.columns.str.startswith('Borrar')]
                    df = df[df['Fecha'] == fecha]
                    # Display the DataFrame
                    print(df)
                    st.dataframe(df)
                                                            
def highlight_row(row):
    if row['Operacion'] == 'Vencimiento':
        return ['background-color: #e8dff5'] * len(row)
    elif row['Operacion'] == 'Venta':
        return ['background-color: #daeaf6'] * len(row)
    elif row['Operacion'] == 'Compra':
        return ['background-color: #fce1e4'] * len(row)
    else:
        return [''] * len(row)

col1, col2 = st.columns(2)

with col1:
    cartola_t0 = cartola_resumen(0)
with col2:
    cartola_t1 = cartola_resumen(1)

try:
    dos_cartolas = pd.concat([cartola_t0, cartola_t1])
    dos_cartolas['indiceaux'] = dos_cartolas['Nemo'] + dos_cartolas['Cantidad']
    dos_cartolas['operation_maintained'] = dos_cartolas.groupby('indiceaux')['T'].transform(lambda x: set(x) == {'T0', 'T1'})
    dos_cartolas = dos_cartolas[dos_cartolas['operation_maintained'] != True]

    # Crear la columna 'Operacion' basada en las condiciones
    dos_cartolas['Operacion'] = dos_cartolas.apply(lambda row: "Vencimiento" if row['Fecha_1'] == fecha else ("Venta" if row['T'] == "T0" else ("Compra" if row['T'] == "T1" else "")), axis=1)

    dos_cartolas = dos_cartolas[['Operacion', 'Nemo', 'Instrumento', 'Plazo', 'Tasa', 
                                'Fecha_0', 'Fecha_1', 
                                'Monto_0', 'Monto_1']]

    # Aplicar estilo al DataFrame
    dos_cartolas.reset_index(drop=True, inplace=True)
    styled_df = dos_cartolas.style.apply(highlight_row, axis=1)

    # Mostrar el DataFrame en Streamlit
    st.dataframe(styled_df, hide_index=True)

except:
    pass

caja()
