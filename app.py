import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime, timedelta
import numpy as np
from tab1 import tab1 as t1
from tab2 import tab2 as t2
from tab4 import extraer_bco_central

#print(pythoncom.__file__)
st.title("Robot Amanda y Max")
st.write("Robot que pretende ayudar a Amanda en automatizaciones")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([":moneybag: Dividendos", ":repeat: Traspasos internos", ":1234: Renta Fija", ":dollar: Paridades", ":page_facing_up: MBI", ":chart_with_upwards_trend: Cuotas Propias"])

with tab1:
    t1() 

with tab2:
    t2()

with tab3:
    st.write("")

with tab4:
    st.write("")
    if st.button('Extraer y enviar el dolar del banco central'):
        extraer_bco_central()
