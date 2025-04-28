1. Descargue la Pre-Factura disponible en [CRM](https://clientes.nevasa.cl/usuario/inicio-sesion/).
2. Ingrese a la sección [Cuotas Propias](http://localhost:8501/Cuotas_Propias), donde:
   1. Suba el archivo descargado. 
   2. Descargue la compra o venta presionando el respectivo botón. 
3. Ingrese a GPI Escritorio > AGF > Back Office > **Operaciones** > **Carga Masiva Operaciones**. y seleccione:
   1. Familia: Fondo Mutuo
   2. Tipo Operación:
      1. Compra o Venta, según corresponda
      2. Compra o Venta Cuotas Propias, según corresponda
      3. FFMM_NAC
      4. SI Mueve Cartera
      5. SI Mueve Caja
   3. Archivo Operaciones: Archivo descargado desde [Cuotas Propias](http://localhost:8501/Cuotas_Propias).
4. Ingrese a GPI Escritorio > Partícipe > Back Office > **Operaciones** > **Carga Masiva Operaciones**. y seleccione:
   1. Familia: Fondo Mutuo
   2. Tipo Operación:
      1. Ingreso o Egreso, según corresponda ¹
      2. Traspaso Ingreso/Egreso Cuotas Propias, según corresponda
      3. FFMM_NAC
      4. SI Mueve Cartera
      5. NO Mueve Caja
   3. Archivo Operaciones: Archivo descargado desde [Cuotas Propias](http://localhost:8501/Cuotas_Propias).

¹ Si es una compra de cuotas propias, en partícipe se selecciona un egreso. Si es una venta, se selecciona ingreso. 
