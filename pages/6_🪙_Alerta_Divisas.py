import streamlit as st
import time
from datetime import datetime ,timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import win32com.client
import pythoncom

# Configuración de la página
st.set_page_config(page_title="Alerta de Divisas", page_icon="🪙", layout="wide")
st.markdown("# Alerta de Divisas")
st.sidebar.header("Alerta de Divisas")


# Fecha
fecha = st.session_state.get('fecha', datetime.now())
mañana = fecha + timedelta(days=1)

# Campo de entrada para el correo electrónico del destinatario
destinatario = st.text_input("Correo electrónico del destinatario", "malarcon@deltasf.cl; abadilla@deltasf.cl; jariasf@deltasf.cl; abravo@deltasf.cl")

# Funciones

# 1. Selecccion de fecha en calendario de Banco Central
def consultar_paridades(mañana):
    action = ActionChains(driver)
    driver.find_element(By.ID,"_calendarioButton").click()
    time.sleep(1)
    calendario = driver.find_element(By.ID,"_calendarioContainer")
    dias = calendario.find_elements(By.CLASS_NAME, "calendarDay")
    for dia in dias:
        print(f"Revisando día: {dia.text}")  # Mensaje de depuración
        if dia.text.isdigit() and int(dia.text) == mañana.day:
            print(f"Seleccionando día: {dia.text}")  # Mensaje de depuración
            time.sleep(1)
            try:
                action.move_to_element(dia).click().perform()
            except:
                driver.execute_script("arguments[0].click();", dia)
            break

# 2. Revisar el valor del dolar y enviar alerta
def revisar_dolar():
    while True:
        driver.refresh()
        valor_dolar = driver.find_element(By.ID,"lblValor1_3").text
        if  valor_dolar != "ND":
            correo_alerta(f"El valor del dolar es {valor_dolar}")
            break
        else:
            time.sleep(20)
            st.write("Consultado...")
        
# 3. Detalle de correo alerta
def correo_alerta(texto):
    print("Correo enviado"  )
    pythoncom.CoInitialize()  # Inicializar COM
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = destinatario
        mail.Subject = "Dólar"
        mail.Body = texto
        mail.Send()
    finally:
        pythoncom.CoUninitialize()  # Desinicializar COM

# Inicio de proceso de extracción de datos del Banco Central
def extraer_bco_central():
    global driver
    banco_central_url="https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx"
    driver = webdriver.Edge() 
    driver.get(banco_central_url)
    consultar_paridades(mañana)
    revisar_dolar()

# Funcion ejecutable
if st.button("Consultar dólar"):
    extraer_bco_central()
    st.success("Consulta realizada con éxito")