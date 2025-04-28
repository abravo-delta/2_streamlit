1. Ingrese a GPI Escritorio > AGF > Back Office > **Operaciones** > **Renta Fija** > Mercado Nacional > Ingreso/Retiro **IIF**
2. Ingrese la siguiente Información:
   1. Intermediación financiera.
   2. Operación.
   3. Compra.
   4. Nombre del cliente.
   5. Concepto Operación: Simultánea.
3. Rellene los datos necesarios para la valorización basándose en:
   1. Si la simultánea es de MBI, complete la siguiente información con la tabla "Detalle Operaciones Vigentes Simultáneas" de la Cartola envíada al correo¹.
      1. Emisor: *MBI*
      2. Moneda Depósito: *CLP*
      3. Sub-Clase Instrumento: *Simultánea*
      4. T+: 0
      5. Monto Operación: Monto a $t_0$
      6. Tasa: Tasa
      7. Fecha de Vencimiento: Fecha $t_1$
      8. Nom. Rescate/Final: Monto a $t_1$
   2. Si la simultánea es de CRM, complete la siguiente información con la órden envíada al correo $^1$:
      1. Emisor: *NEVASA S.A., CORREDORES DE BOLSA*
      2. Moneda Depósito: *CLP*
      3. Sub-Clase Instrumento: *Simultánea*
      4. T+: Liquidación
      5. Monto Operación: Monto contado
      6. Tasa: Diferencial de Precio
      7. Plazo: Plazo
      8. Fecha de Vencimiento: Fecha Vencimiento
      9. Nom. Rescate/Final: Monto Compromiso
   3.  Cambie el nemotécnico a uno con el siguiente formato: "SMT_T1_T0_TASA_INSTRUMENTO", donde
       - T1: fecha de vencimiento en formato *ddmmyyyy*
       - TO: fecha de emisión en formato *ddmmyyyy*
4. Revise si está todo correcto. En caso de que lo esté baje la operación y guardela$^2$.

$^1$ Si no recibió la información necesaria al correo, no dude en solicitarla al cliente.

$^2$ Muchas veces la valorización de GPI no es exacta a la del cliente, considere aceptable una diferencia de $2.000, y siempre iguale el monto al entregado por el cliente. 

$^3$ Muchas veces las simultáneas tienen comisión. Revise la sección correspondiente sobre cómo ingresarlas a GPI, [Manuales](http://localhost:8501/Manuales) > Movimientos de Caja > Comisiones por Simultáneas.