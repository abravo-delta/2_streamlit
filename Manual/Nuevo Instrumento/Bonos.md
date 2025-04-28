1. Identifique el nemotécnico del bono que desea ingresar. 
2. Busque el bono por nemotécnico en [Risk América](https://apps.riskamerica.com/) > Instrumentos RF. En esta página recopilará la información a rellenar en GPI.  
3. En la sección Tabla de desarrollo de Risk América seleccione *Tabla (xlsx)*. Esto descargará la tabla de desarrollo del instrumento. Realice las siguientes modificaciones sobre este archivo:
   1. Modifique el formato de la columna B (Fecha), para que siga el siguiente formato *dd-mm-yyyy*, conocido como *fecha corta*
   2. Elimine la primera fila con datos, es decir, en la que N° sea 0.
4. Ingrese a GPI Escritorio > AGF > Back Office > Mantención > Instrumentos > Instrumentos.
5. Seleccione un instrumento con nombre similar al que se ingresará y copielo. En la pestaña desplegable ingrese el nombre del nuevo instrumento. 
6. En la sección Instrumentos:
   1. Rellene los siguientes campos según la información de Risk América:
      | GPI | Risk América Sección | Risk América |
      |---|---|---|
      | Moneda Instrumento | Información | Moneda |
      | Tasa Efectiva | Emisión | TERA |
      | Tasa Emisión | Emisión | Tasa de emisión |
      | Fecha Emisión | Emisión | Fecha de emisión |
      | Periodo Cupones | Emisión | Periodicidad |
      | Fecha Vencimiento | Emisión | Fecha de Vencimiento |
      | Corte Mínimo Papel | Emisión | Corte mínimo |
      | Base Interés | Emisión | Base TIR |
      | Base Fecha | Emisión | Base TIR |
      | Monto Emisión | Emisión | Monto Emitido |
      | Número Cupones | Emisión | Número de Cupones |
    2. Presione el botón Cupones y en la ventana desplegable pegue la tabla de desarrollo previamente descargada, presionando el botón Pegar. 
7. En la sección de Atributos confirme la siguiente información:
   1. Clase Activo: *Renta Fija Nacional*.
   2. Sub Clase Activo: *Bono*.
   3. Mercado: *Local*.
   4. Moneda: Misma que moneda de instrumento en la sección Instrumento.
   5. Sector económico: *Bancos* u *Otros* según corresponda.
   6. País: *Chile*.
   7. Emisor: Nombre del emisor.
   8. Grupo económico: Grupo Empresarial del emisor disponible al presionar el nombre del emisor en RA.
   9. Tipo Instrumento CMF: Tipo en RA, sección información.
   10. Clasificación Riesgo CMF: Última clasificación de riesgo del emisor disponible al presionar el nombre del emisor en RA.
   11. País Emisor CMF: *CL*.
   12. Rut Emisor CMF: RUT del emisor disponible al presionar el nombre del emisor en RA.