import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime, timedelta
import numpy as np
from tab4 import extraer_bco_central

hoy = datetime.today()
fecha = st.sidebar.date_input('Fecha', value=hoy)
fecha = datetime.combine(fecha, datetime.min.time())
st.session_state['fecha'] = fecha
st.sidebar.title("Menú")
st.sidebar.page_link("pages/tab1.py", label= ":moneybag: Dividendos")
st.sidebar.page_link("pages/tab2.py", label= ":repeat: Traspasos internos")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣", disabled=True)
# st.page_link("http://www.google.com", label="Google", icon="🌎")

#print(pythoncom.__file__)
st.title("Robot Amanda y Max")
st.write("Robot que pretende ayudar a Amanda en automatizaciones")

tab3, tab4, tab5, tab6 = st.tabs([":1234: Renta Fija", ":dollar: Paridades", ":page_facing_up: MBI", ":chart_with_upwards_trend: Cuotas Propias"])

with tab3:
    st.write("")

with tab4:
    st.write("")
    if st.button('Extraer y enviar el dolar del banco central'):
        extraer_bco_central()
