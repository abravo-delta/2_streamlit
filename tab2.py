archivo = st.file_uploader("Sube un archivo Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo, sheet_name="Hoja1")
    
    # Edición
    df = df.iloc[1:-4,1:]
    df['Cuenta'] = df['Cuenta'].apply(lambda x: x[:-3] + '-' + x[-3:])
    df['Fecha Operacion'] = datetime.today().strftime('%d/%m/%Y')
    df['Fecha liquidacion'] = datetime.today().strftime('%d/%m/%Y')
    
    # Función tratamiento egreso/ingreso
    def separar_traspasos(i, j, df):
        df_x = df[df.iloc[:, i].notna()]
        df_x = df_x.drop(df_egreso.columns[j], axis=1)
        df_x = df_x.columns.values[3] = "Cantidad" 
        df_x['Monto'] = df_x['Monto'].apply(lambda x:round(x,0))
        df_x['Monto2'] = df_x['Cuotas'] * df_x['Precio']
        df_x['Monto2'] = df_x['Monto2'].apply(lambda x:round(x,0))
        df_x['Dif'] = df_x['Monto'] - df_x['Monto2']
        df_x['Dif'] = df_x['Dif'].abs()        

    # Ejecutar 

    df_egreso = separar_traspasos(3, 4, df)
    df_ingreso = separar_traspasos(4, 3, df)
    

    if sum(df_egreso['Dif']) != 0 and sum(df_ingreso['Dif']) != 0:
        st.write("Revisar montos")
    if sum(df_ingreso['Cantidad']) != sum(df_egreso['Cantidad']):
        st.write("Alerta: Diferencia de cuotas")
    else:
        st.write("Ingresos")
        df_in = st.dataframe(df_ingreso)

    if sum(df_ingreso['Monto']) != sum(df_egreso['Monto']):
        st.write("Alerta: Diferencia de monto")
    else: 
        st.write("Egresos")
        df_eg = st.dataframe(df_egreso)

    df_ingreso = df_ingreso.drop(columns=['Monto2','Dif'])
    df_egreso = df_egreso.drop(columns=['Monto2','Dif'])

    # Botón para descargar el archivo modificado
    if st.button("Descargar Ingresos"):
        with pd.ExcelWriter("Ingresos.xlsx", engine="openpyxl") as writer:
            df_ingreso.to_excel(writer, index=False)
        
        with open("Ingresos.xlsx", "rb") as f:
            st.download_button("Descargar Ingresos", f, file_name=("Ingresos.xlsx"))

    # Botón para descargar el archivo modificado
    if st.button("Descargar Egresos"):
        with pd.ExcelWriter("Egresos.xlsx", engine="openpyxl") as writer:
            df_egreso.to_excel(writer, index=False)
        
        with open("Egresos.xlsx", "rb") as f:
            st.download_button("Descargar Egresos", f, file_name=("Egresos.xlsx"))
