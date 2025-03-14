from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime ,timedelta
import time
import win32com.client
import pythoncom

pythoncom.CoInitialize()

#Comit nuevo


# Funciones
def consultar_paridades(mañana):
    driver.find_element(By.ID,"_calendarioButton").click()
    time.sleep(1)
    calendario = driver.find_element(By.ID,"_calendarioContainer")
    dias = calendario.find_elements(By.TAG_NAME,"td")
    for x in dias:
        if str(mañana.day) == x.text:
            x.click()
            break

def revisar_dolar():
    regla = True
    while regla:
        driver.refresh()
        d = driver.find_element(By.ID,"lblValor1_3").text
        if  d != "ND":
            correo_alerta(f"El valor del dolar es {d}")
            regla = False
        else:
            time.sleep(20)
            print("consultado")
        
def correo_alerta(texto):
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    mail.To = "jariasf@deltasf.cl;malarcon@deltasf.cl"
    mail.Subject = "Dolar"
    mail.Body = texto
    mail.Send()
    pass


# Calcular el próximo día hábil
def siguiente_dia_habil(fecha):
    fecha += timedelta(days=1)  # Avanzar un día
    while fecha.weekday() >= 5:  # 5 = Sábado, 6 = Domingo
        fecha += timedelta(days=1)  # Seguir avanzando si es fin de semana
    return fecha

def extraer_bco_central():
    global driver
    banco_central_url="https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx"
    hoy = datetime.today()
    mañana = siguiente_dia_habil(hoy)
    driver = webdriver.Edge() 
    driver.get(banco_central_url)

    consultar_paridades(mañana)
    revisar_dolar()

pythoncom.CoUninitialize()
