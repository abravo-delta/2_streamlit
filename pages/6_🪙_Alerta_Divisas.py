import streamlit as st
import time
from datetime import timedelta,datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import win32com.client
import pythoncom
from pages.auxiliares import *

funcion = "Envía correo electronico con el valor de la divisa del día siguiente, en cuanto sale del Banco Central."
inputs = "* **Destinatarios**: Correos electronicos de los destinatarios del aviso."

# Configuración de la página
config_page("Alerta de Divisas", "🪙", funcion, inputs)

# Fecha
fecha = traer_fecha()
mañana = fecha + timedelta(days=1)

# Campo de entrada para el correo electrónico del destinatario
destinatarios_usuales = "malarcon@deltasf.cl; abadilla@deltasf.cl; jariasf@deltasf.cl; abravo@deltasf.cl"
destinatario = st.text_input("Destinatarios", destinatarios_usuales)

# Funciones

def hora_actual_formato_mmhh():
    ahora = datetime.now()
    return ahora.strftime("%H:%M")

def seleccionar_fecha(mañana):
    action = ActionChains(driver)
    driver.find_element(By.ID,"_calendarioButton").click()
    time.sleep(1)
    calendario = driver.find_element(By.ID,"_calendarioContainer")
    dias = calendario.find_elements(By.CLASS_NAME, "calendarDay")
    for dia in dias:
        if dia.text.isdigit() and int(dia.text) == mañana.day:
            time.sleep(1)
            try:
                action.move_to_element(dia).click().perform()
            except:
                driver.execute_script("arguments[0].click();", dia)
            break

# 2. Revisar el valor del dolar y enviar alerta
def revisar_paridad(divisa):
    mensaje = st.empty()
    while True:
        driver.refresh()
        if divisa == "dolar":
            valor = driver.find_element(By.ID,"lblValor1_3").text
        elif divisa == "euro":
            valor = driver.find_element(By.ID,"lblValor1_5").text
        if  valor != "ND":
            correo_alerta(divisa, valor)
            driver.close()
            break
        else:
            time.sleep(20)
            minutuo = hora_actual_formato_mmhh()
            mensaje.write(f"Consultado {divisa}... {minutuo}")
        
# 3. Detalle de correo alerta
def correo_alerta(divisa, valor):
    pythoncom.CoInitialize()  # Inicializar COM
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = destinatario
        mail.Subject = divisa
        mail.Body = f"El valor del {divisa} es {valor}"
        mail.Send()
    finally:
        pythoncom.CoUninitialize()  # Desinicializar COM

# Inicio de proceso de extracción de datos del Banco Central
def extraer_bco_central(divisa):
    global driver
    banco_central_url="https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx"
    driver = webdriver.Edge() 
    driver.get(banco_central_url)
    seleccionar_fecha(mañana)
    revisar_paridad(divisa)
    
# Funcion ejecutable

tab1, tab2 = st.tabs(["💵 Dolar", "💶 Euro"])
# 1. Selecccion de fecha en calendario de Banco Central

with tab1:
    if st.button("Consultar dólar"):
        extraer_bco_central("dolar")
        st.success("Consulta realizada con éxito")

with tab2:
    if st.button("Consultar euro"):
        extraer_bco_central("euro")
        st.success("Consulta realizada con éxito")
