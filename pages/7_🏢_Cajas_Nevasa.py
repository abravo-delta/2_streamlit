import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time 
from pages.auxiliares import *

funcion = "Extrae el valor de las cajas a la fecha desde la página web de Nevasa, tanto en dólares como en pesos."

inputs = '''1. **Sitio Web Nevasa**: Ingresar el link del sitio Web de Nevasa, sección de Inicio de Sesión.  
2. **Rut**: Ingrese el Rut del Inicio de Sesión de Nevasa.  
3. **Contraseña**: Ingrese la contraseña del sitio.  
4. **Fondos**: Seleccione los fondos de los que se desea extraer las cajas.  
'''

# Configuración de la página
config_page("Cajas Nevasa", "🏢", funcion, inputs)

# Ver esto en dos columnas
col1, col2 = st.columns(2)

with col1:
    link_nevasa = st.text_input("Sitio Web Nevasa", "https://clientes.nevasa.cl/usuario/inicio-sesion/")
    rut_usuario = st.text_input("Rut", "11111111-1")
    contrasena = st.text_input("Contraseña", type="password")

# 1 Funciones:
def ingresar_usuario(rut , clave):
    rut_input = pagina.find_element(By.NAME, "rut")
    rut_input.clear()
    rut_input.send_keys(rut)
    password_input = WebDriverWait(pagina, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.clear()
    password_input.send_keys(clave)
    login_button = WebDriverWait(pagina, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-iniciar-sesion"))
    )
    login_button.click()

def seleccionar_fondo(rut_fondo):
    cliquear(pagina.find_elements(By.TAG_NAME,"span"),rut_fondo)
    cliquear(pagina.find_elements(By.TAG_NAME,"button"),"Continuar")

def cliquear(lista,p):
    for x in lista:
        if x.text == p:
            elemento = x
            break
    try:
        time.sleep(1)
        pagina.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", elemento)
        elemento.click()
    except:
        print(f"Elemento No encontrado")

def aux_extraer_caja(pagina):
    contenido = pagina.find_element(By.ID, "mainContent_cl")
    wait = WebDriverWait(contenido, 10)
    time.sleep(2)
    web = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe"))) 
    pagina.switch_to.frame(web)
    wait = WebDriverWait(pagina, 5)
    
def extraer_caja(pagina):
    element2 = wait.until(EC.presence_of_element_located((By.ID, "dataGridColumn1"))) 
    element2 = pagina.find_elements(By.ID,"dataGridColumn1")[2]
    time.sleep(3)    
    span_element = element2.find_element(By.TAG_NAME, "span")
    span_text = span_element.text
    return(span_text)

def seleccionar_caja_usd(pagina):
    combo_box = pagina.find_element(By.CLASS_NAME, "ComboBoxTextInput")
    combo_box.click()
    time.sleep(1)  # Espera a que cargue la lista
    usd_option = pagina.find_element(By.XPATH, '//span[@class="StringItemRenderer" and text()="USD"]')
    usd_option.click()
    return pagina

# Ejecución
with col1:
    options = st.multiselect("Seleccione los fondos a extraer cajas", ["Ahorro", "Parque Matucana", "Deuda Privada", "Patrimonio Inmobiliario", "Inmobiliaria VII", "Inmobiliaria VIII", "Chile Axion", "Student Living", "Vision", "Proteccion", "Pre-Ipo Opportunities MVP"])

Fondo=pd.DataFrame(columns = ["Rut","Nombre Cliente","Caja CLP","Caja USD"])
for x in options:
    if x == "Ahorro":
        Fondo.loc[len(Fondo)] = ["76.081.068-1", "Ahorro", 0, 0]
    elif x == "Parque Matucana":
        Fondo.loc[len(Fondo)] = ["76.860.618-8", "Parque Matucana", 0, 0]
    elif x == "Deuda Privada":
        Fondo.loc[len(Fondo)] = ["76.996.925-K", "Deuda Privada", 0, 0]
    elif x == "Patrimonio Inmobiliario":
        Fondo.loc[len(Fondo)] = ["77.076.929-9", "Patrimonio Inmobiliario", 0, 0]
    elif x == "Inmobiliaria VII":
        Fondo.loc[len(Fondo)] = ["77.223.242-K", "Inmobiliaria VII", 0, 0]
    elif x == "Inmobiliaria VIII":
        Fondo.loc[len(Fondo)] = ["76.632.763-K", "Inmobiliaria VIII", 0, 0]
    elif x == "Chile Axion":
        Fondo.loc[len(Fondo)] = ["77.542.715-9", "Chile Axion", 0, 0]
    elif x == "Student Living":
        Fondo.loc[len(Fondo)] = ["76.562.651-K", "Student Living", 0, 0]
    elif x == "Vision":
        Fondo.loc[len(Fondo)] = ["76.080.991-8", "Vision", 0, 0]
    elif x == "Proteccion":
        Fondo.loc[len(Fondo)] = ["77.542.714-0", "Proteccion", 0, 0]
    elif x == "Pre-Ipo Opportunities MVP":
        Fondo.loc[len(Fondo)] = ["76.825.263-7", "Pre-Ipo Opportunities MVP", 0, 0]

with col1:
    if st.button("Extraer cajas"):
        for x,y in Fondo.iterrows():
            ## Abrir edge
            pagina = webdriver.Edge()
            pagina.maximize_window()
            
            ## Entrar a Nevasa
            pagina.get(link_nevasa)
            ingresar_usuario(rut_usuario, contrasena)
            
            wait = WebDriverWait(pagina, 10)  # Esperar hasta 10 segundos
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'custom-control'))) 
            ## Seleccionar fondo
            seleccionar_fondo(y.Rut)

            element = wait.until(EC.presence_of_element_located((By.ID, 'mainContent_cl')))  # Espera hasta que el elemento esté presente
            
            aux_extraer_caja(pagina)
            # Extraer caja en clp
            caja_clp = extraer_caja(pagina)
            Fondo.iloc[x,2] = float(caja_clp.replace('.', '').replace(',', '.'))
            # Extraer caja en usd
            seleccionar_caja_usd(pagina)
            time.sleep(3)
            caja_usd = extraer_caja(pagina)
            Fondo.iloc[x,3] = float(caja_usd.replace('.', '').replace(',', '.'))
            pagina.quit()
        with col2:
            st.header("Cajas")
            st.dataframe(Fondo)