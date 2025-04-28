
# DJ 1829
*Manual para la confección de la Delcaración Jurada 1829, sobre contratos de derivados.*

## 1. Alcances
Este documento tiene el propósito de ser una guía para la creación de la Declaración Jurada 1829 a partir del compilado de operaciones de derivados de la institución declarante. No obstante, es importante comprender que está basado únicamente en un caso que posee ciertas particularidades:

### 1.1 Caso Base
EL caso base de este manual, es la Declaración Jurada 1829 de Vantrust Capital Corredores de Bolsa S.A. del año 2025, sobre los contratos de derivados del 2024. El cliente solo operó derivados del tipo forward de divisas. De modo que las especificaciones de este manual solo se basan en este caso.

### 1.2 Formato Thompson
Este documento no describ todo el proceso de la generación de la Declaración Jurada 1829, sino que abarca hasta la generación de los inputs para el aplicativo Thompson. 

## 2. Creación de la Declaración Jurada

### 2.1 Campos sobre Contraparte

#### 2.1.1 Rut contraparte
Corresponde al Rut en formato *12345678-9*. En caso de no existir, por contraparte extranjera, se mantendría vacío.  
$$ \text{RUT CONTRAPARTE} = 
\begin{cases} 
    \text{Vacía} &\text{Si no existe Rut}\\
    \text{Rut} &\text{Si existe Rut}\\
\end{cases} $$
>💡 **Vantrust Capital CDB, 2025**
Todas las operaciones tenían un Rut.

#### 2.1.2 TAX ID de la Contraparte
En caso de una contraparte extrangera (sin Rut) el TAX ID corresponde al código de identificación tributaria de la contraparte en el país de origen. 
$$ \text{TAX ID DE LA CONTRAPARTE} = 
\begin{cases}
    \text{Código de id tributaria del país} &\text{Si no existe Rut}\\
    \text{Vacía} &\text{Si existe Rut}
\end{cases}
$$
>💡 **Vantrust Capital CDB, 2025**
Ninguna contraparte tenía información en este campo, dado que todas tenían Rut chileno.

#### 2.1.3 Código País Contraparte
Corresponde al Código ISO 3166-1 alfa-2 de países o, lo que es igual al del [Anexo de Declaraciones Juradas del SII](#31-código-país-contraparte).
>💡 **Vantrust Capital CDB, 2025**
Solo CL, dado que las contrapartes eran chilenas. 

#### 2.1.4 Tipo de Relación con Contraparte
$$\text{TIPO DE RELACIÓN CON LA CONTRAPARTE}=
\begin{cases}
    1 &\text{De propiedad}\\
    2 &\text{Dirección o Administración}\\
    3 &\text{Otros}\\
    4 &\text{Contraparte en Paraíso Tributario}\\
    99 &\text{Sin relación}
\end{cases}$$
>💡 **Vantrust Capital CDB, 2025**
>La mayoría fueron 99, excepto 5 casos:
>* 1:  76885293-6
>* 2: 76285610-7, 76011977-6, 76130407-0 y 7717445-1
>Ver [Anexo de contrapartes]()

#### 2.1.5 Modalidad de Contratación
$$\text{MODALIDAD DE CONTRATACIÓN}=
\begin{cases}
    1 &\text{En bolsa nacional}\\
    2 &\text{En bolsa extranjera}\\
    3 &\text{Contrato por agente}\\
    4 &\text{Fuera de bolsa}\\
    5 &\text{Confirmación fuera de bolsa}\\
    6 &\text{Otros}
\end{cases}
$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo solo tuvo valor 4.

### 2.2 Campos sobre Acuerdo Marco
Estos campos solo se rellenan si la operación forma parte de un Contrato Marco, es decir, un contrato que englobe a más de una operación.

#### 2.2.1 Tipo
$$\text{TIPO} = 
\begin{cases} 
    1 &\text{Mercado Local}\\ 
    2 &\text{Mercado Internacional}\\
    3 &\text{Otros}
\end{cases}
$$

#### 2.2.2 Número
Número interno asociado al contrato Marco. Solo puede ser númerico de máx 10 carácteres.

#### 2.2.3 Fecha de Suscripción
Fecha de suscripción del contrato marco. Debe estar en el formato fecha corta de excel: dd-mm-yyyy.

### 2.3 Campos sobre contrato o confirmación
Los siguientes campos son sobre los detalles de las operaciones de derivados. 

#### 2.3.1 Número / Identificador
Número identificador único que converse con:
1. Declaración Jurada 1820. 
2. Número de contrato del periodo anterior.  
Debe tener máximo 10 carácteres. 

#### 2.3.2 Fecha de Suscripción_1
Fecha se suscripción, modificación o cesión de un contrato según corresponda. Debe estar en el formato fecha corta de excel: dd-mm-yyyy.

#### 2.3.3 Contrato vencido en el ejercicio
$$\text{CONTRATO VENCIDO EN EL EJERCICIO} = 
\begin{cases}
    1 &\text{Contrato vencido o liquidado}\\
    2 &\text{Contrato Vigente}    
\end{cases}$$

#### 2.3.4 Estado del contrato / confirmación
$$\text{ESTADO DEL CONTRATO/CONFIRMACIÓN} =  
\begin{cases}
    \text{Vacía} &\text{Operación Vencida}\\
    1 &\text{Operación Vigente y Contrato Suscrito}\\
    2 &\text{Operación Vigente y Contrato Modificado}\\
    3 &\text{Operación Vigente y Contrato del ejercicio anterior}\\
    4 &\text{Operación Vigente y Contrato Cedido}
\end{cases}$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo solo tuvo valor 1 o vacío.

#### 2.3.5 Tipo de Contrato
$$\text{TIPO DE CONTRATO}=
\begin{cases}
    1 &\text{Forward}\\
    2 &\text{Futuro}\\
    3 &\text{Swap}\\
    4 &\text{Cross Currency Swap}\\
    5 &\text{Credit Default Swap}\\
    6 &\text{Option Call Americana}\\
    7 &\text{Option Put Americana}\\
    8 &\text{Option Call Europea}\\
    9 &\text{Option Put Europea}\\
    10 &\text{Option Call Asiática}\\
    11 &\text{Option Put Asiática}\\
    12 &\text{Otros derivados incluidos en el N° 2 del artículo 2°, de la Ley 20.544, de 2011}\\
    13 &\text{Otros derivados incluidos en el N° 3 del artículo 2°, de la Ley 20.544, de 2011}\\
    14 &\text{Otros}
\end{cases}$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo solo tuvo valor 1, por forwards.

#### 2.3.6 Nombre del Instrumento
$$\text{NOMBRE DE INSTRUMENTO} =
\begin{cases}
    \text{Instrumento} &\text{Si TIPO DE CONTRATO ≥ 12, 13 o 14}\\
    \text{Vacío} &\text{Si TIPO DE CONTRATO <12}
\end{cases}$$
Reglas de formato:
1. Sin carácteres especiales, símbolos, acentos, letra "ñ". 
2. Sin descripción. 
3. Máximo 20 carácteres. 
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.

#### 2.3.7 Modalidad de Cumplimiento
$$\text{MODALIDAD DE CUMPLIMIENTO}= 
\begin{cases}
    1 &\text{Si es por Compensación}\\
    2 &\text{Si es por Entrega Física}
\end{cases}$$

#### 2.3.8 Posición del Declarante
$$\text{POSICIÓN DEL DECLARANTE}=
\begin{cases}
    \text{Vacía} &\text{Si es Swap}\\
    1 &\text{Si no es Swap y es Venta}\\
    2 &\text{Si no es Swap y es Compra}
\end{cases}$$

### 2.4 Campos sobre el primer activo subyacente

#### 2.4.1 Tipo 
Código del tipo de activo subyacente
$$\text{TIPO}=
\begin{cases}
    1 &\text{Si Moneda}\\
    2 &\text{Si Tasa de Interés}\\
    3 &\text{Si Producto Básico o commodity}\\
    4 &\text{Si UF}\\
    5 &\text{Si Acciones}\\
    6 &\text{Si Índice Bursatil}\\
    7 &\text{Si Otros}
\end{cases}$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo siempre fue 1, dado que solo tenían operaciones Forward de Divisas.

#### 2.4.2 Código
Código del activo subyacente:
$$\text{Si TIPO} = 1 → \text{CODIGO} = \text{ISO3 de Monedas}$$ 
$$\text{Si TIPO} = 2 → \text{CODIGO} = 
\begin{cases}
    1 &\text{Si Tasa Fija}\\ 
    2 &\text{Si Tasa Variable}
\end{cases}
$$
$$\text{Si TIPO} = 3 → \text{CODIGO} = 
\begin{cases}
    1 &\text{Cobre}\\
    2 &\text{Oro}\\
    3 &\text{Plata}\\
    4 &\text{Zinc}\\
    5 &\text{Plomo}\\
    6 &\text{Aluminio}\\
    7 &\text{Níquel}\\
    8 &\text{Petróleo}\\
    9 &\text{Gas Propano}\\
    10 &\text{Jet Fuel 54}\\
    11 &\text{Heating Oil}\\
    12 &\text{Oil Wti}\\
    13 &\text{Fuel Oil 3.5}\\
    14 &\text{Otros}
\end{cases}
$$
$$\text{Si TIPO} \neq \{1,2,3\} → \text{CODIGO = Vacía}$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo fue "CNY", "USD" y "EUR".

#### 2.4.3 Otros (especificación)
$$ \text{Si TIPO} = 2 \text{ y CODIGO} =2 → \text{OTROS (ESPECIFICACIÓN)} =
\begin{cases}
    1 &\text{Euribor 1 mes}\\
    2 &\text{Euribor 3 meses}\\
    3 &\text{Euribor 6 meses}\\
    4 &\text{Euribor 12 meses}\\
    5 &\text{Libor dólar canadiense 3  meses}\\
    6 &\text{Libor dólar canadiense 6 meses}\\
    7 &\text{Libor dólar canadiense 12 meses}\\
    8 &\text{Libor euro 1 mes}\\
    9 &\text{Libor euro 3 meses}\\
    10 &\text{Libor euro 6 meses}\\
    11 &\text{Libor euro 12 meses}\\
    12 &\text{Libor libra esterlina 1 mes}\\
    13 &\text{Libor libra esterlina 3 meses}\\
    14 &\text{Libor libra esterlina 6 meses}\\
    15 &\text{Libor libra esterlina 12 meses}\\
    16 &\text{Libor usd 1 mes}\\
    17 &\text{Libor usd 2 meses}\\
    18 &\text{Libor usd 3 meses}\\
    19 &\text{Libor usd 4 meses}\\
    20 &\text{Libor usd 6 meses}\\
    21 &\text{Libor usd 12 meses}\\
    22 &\text{Libor yen 1 mes}\\
    23 &\text{Libor yen 3 meses}\\
    24 &\text{Libor yen 6 meses}\\
    25 &\text{Libor yen 12 meses}\\
    26 &\text{Libor franco suizo 1 mes}\\
    27 &\text{Libor franco suizo 3 meses}\\
    28 &\text{Libor franco suizo 6 meses}\\
    29 &\text{Libor franco suizo 12 meses}\\
    30 &\text{Pibor (paris interbank offered rate)}\\
    31 &\text{Prime usa}\\
    32 &\text{Short term prime rate, yen}\\
    33 &\text{Tab uf 3 meses}\\
    34 &\text{Tab uf 6 meses}\\
    35 &\text{Tab uf 12 meses}\\
    36 &\text{Tab nominal 1 mes}\\
    37 &\text{Tab nominal 3 meses}\\
    39 &\text{Tab nominal 12 meses}\\
    40 &\text{Otras}    
\end{cases}
$$
$$\text{Si TIPO =  7} → \text{OTROS (ESPECIFICACIÓN)} = \text{Nombre de activo subyacente con máximo 3 carácteres}$$
$$\text{Si TIPO} \neq \{7,2\} → \text{OTROS (ESPECIFICACIÓN)} = \text{Vacía}$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo vacío

#### 2.4.4 Tasa fija / Spread %
Tasa con máximo 3 enteros y 4 decimales en los siguientes casos:

$$\text{TASA FIJA / SPREAD \%} = 
\begin{cases}
    \text{Tasa fija} &\text{Si la hay}\\
    \text{Spread} &\text{Si la tasa es Variable}\\
    \text{Vacía} &\text{Si no hay tasa}
\end{cases}
$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.

### 2.5 Campos sobre el segundo activo subyacente
Solo para Swaps, con los mismos códigos que la sección anterior.
>💡 **Vantrust Capital CDB, 2025**
>Todos estos campos estuvieron vacíos

#### 2.5.1 Tipo_1 
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.
#### 2.5.2 Código_2
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.
#### 2.5.3 Otros (especificación)_3
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.
#### 2.5.4 Tasa fija / Spread %_4
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.

### 2.6 Campos sobre el Precio futuro contratado (futuros, forwards y opciones)
Solo en caso de que los derivados operados NO sean Swaps. 

#### 2.6.1 Código de Precio
$$\text{CÓDIGO DE PRECIO} = 
\begin{cases}
    1 &\text{Valor Monetario}\\
    2 &\text{Tasa (\%)}
\end{cases}
$$
>💡 **Vantrust Capital CDB, 2025**
>Este campo siempre corresponde a 1 debido a que las operaciones eran forwards de divisas.

#### 2.6.2 Precio
$$\text{PRECIO} =
\begin{cases}
    \text{Precio acordado en el contrato de confirmación} &\text{si CÓDIGO DE PRECIO} = 1\\
    \text{Vacía} &\text{si CÓDIGO DE PRECIO} = 2\\
\end{cases}
$$
Formato: máximo 15 carácteres.
>💡 **Vantrust Capital CDB, 2025**
>Este campo estuvo relleno con el Precio al Cliente, correspondiente del valor pactado de la divisa.

#### 2.6.3 Moneda
$$\text{MONEDA} =
\begin{cases}
    \text{ISO 3 de Monedas} &\text{si CÓDIGO DE PRECIO} = 1\\
    \text{Vacía} &\text{si CÓDIGO DE PRECIO} = 2\\
\end{cases}
$$

> 💡**Vantrust Capital CDB, 2025**
>Este campo fue "CLP". 

### 2.7 Campos sobre el nocional

#### 2.7.1 Unidad
$$ \text{UNIDAD} =
\begin{cases}
    1 &\text{Pesos Chilenos}\\
    2 &\text{US Dólares}\\
    3 &\text{Unidad de Fomento}\\
    4 &\text{Libras esterlinas}\\
    5 &\text{Euros}\\
    6 &\text{Yenes}\\
    7 &\text{Libras}\\
    8 &\text{Toneladas}\\
    9 &\text{Onzas}\\
    10 &\text{Barriles}\\
    11 &\text{Galón Americano}\\
    12 &\text{Galón Inglés}\\
    13 &\text{Otros}    
\end{cases}
$$
> 💡**Vantrust Capital CDB, 2025**
>Este campo fue 1.

#### 2.7.2 Monto/cantidad contratado o nocional
Nocional o cantidad. Con máximo 13 enteros y 2 decimales.

#### 2.7.3 Segunda unidad (Sólo Swap)
Mismas reglas que el campo Unidad, y solo rellenable para los Swaps.
> 💡**Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.

#### 2.7.4 Segundo monto nocional (Sólo Swap)
Mismas reglas que el campo Monto/cantidad contratado o nocional, y solo rellenable para los Swaps.
> 💡**Vantrust Capital CDB, 2025**
>Este campo estuvo vacío.

### 2.8 Campos sobre fechas claves
#### 2.8.1 Fecha de Vencimiento
Fecha de vencimiento o último corte de cupón en caso de swaps en formato de fecha corta de excel: dd-mm-yyyy. 

#### 2.8.2 Fecha de liquidación o de ejercicio de opción
Fecha de liquidación o último corte de cupón en caso de swaps en formato de fecha corta de excel: dd-mm-yyyy. 
> 💡**Vantrust Capital CDB, 2025**
>Fecha de liquidación si se tiene, sino, de vencimiento.

### 2.9 Campos sobre el precio subyacente
Sobre el precio al cierre del ejercicio o liquidación del contrato. 

#### 2.9.1 Código de precio2
$$
\text{CÓDIGO DE PRECIO2}
 = \begin{cases}
    1 &\text{Si el Precio es Valor Monetario}\\
    2 &\text{Si el Precio es una Tasa (\%)}
 \end{cases}$$
> 💡**Vantrust Capital CDB, 2025**
>Siempre tomó valor 1. 

#### 2.9.2 Precio_1

$$\text{PRECIO\_1} = \begin{cases}
    \text{Precio de Vencimiento} &\text{Si es Valor Monetario y la Operación está Vencida}\\
    \text{Precio de moneda al fin del ejercicio} &\text{Si es Valor Monetario y la Operación está Vigente}\\
    \text{Tasa de mercado con 4 decimales} &\text{Si es Tasa}
\end{cases}$$
> 💡**Vantrust Capital CDB, 2025**
>Siempre tomó el valor de la moneda, ya sea al vencimiento o al fin del ejercicio, según corresponde. 

### 2.10 Campos sobre valorización

#### 2.10.1 Valor justo del contrato / confirmación

$$\text{VALOR JUSTO DEL CONTRATO / CONFIRMACIÓN} = \begin{cases}
    \text{Valor Justo a liquidación} &\text{Si liquidó}\\
    \text{Valor justo a fin del ejercicio} &\text{Si está vigente}
\end{cases}$$
Puede ser con signo ("-") y debe estar en pesos chilenos.
> 💡**Vantrust Capital CDB, 2025**
> Se calculó como la diferencia de precios por el nocional:
>$$\text({PRECIO\_1} - \text{PRECIO})*\text{MONTO/CANTIDAD CONTRATADO O NOCIONAL}$$

#### 2.10.2 Resultado del ejercicio $
Efecto en el estado de resultados positivo  o negativo (con signo menos) del derivado en pesos chilenos. 
> 💡**Vantrust Capital CDB, 2025**
> Si el contrato se encontraba vencido correspondió al Margen en moneda de transacción. En caso de estar vigente, se mantuvo el Valor Justo. 
> $$\begin{cases}  
    \text{Margen moneda transacción} &\text{Si está vencido}\\
    \text{Valor Justo} &\text{Si está vigente}
\end{cases}$$

#### 2.10.3 Cuenta contable asociada al resultado del ejercicio 
Código de cuenta contable asociada a lo informado en la columna “Resultado del ejercicio”. Máximo 15 carácteres. 
> 💡**Vantrust Capital CDB, 2025**
Se utilizaron los mismos códigos que en la versión anterior. 

#### 2.10.4 Efecto en Patrimonio $
La pérdida (con signo negativo) o ganancia acumulada que haya sido reconocida directamente en el patrimonio neto, en pesos chilenos. 
Máximo 15 carácteres y puede ser con signo ("-"). 

> 💡**Vantrust Capital CDB, 2025**
> Se calculó como la diferencia entre el resultado del ejercicio y el valor justo. 
$$\text{Resultado del ejercicio} - \text{Valor Justo}$$

#### 2.10.5 Cuenta contable asociada al efecto en Patrimonio
Código de la cuenta contable asociada a lo informado en la columna “Efecto en Patrimonio (en pesos)”. 
Máximo 15 carácteres. 
> 💡**Vantrust Capital CDB, 2025**
Se utilizaron los mismos códigos que en la versión anterior. 

### 2.11 Otros campos
> 💡**Vantrust Capital CDB, 2025**
Estos campos estában vacíos.

#### 2.11.1 Comisión pactada $
Monto en CLP de ingresos o desembolsos (con signo negativo) por concepto de comisiones. En caso de no haber, se deja vacío.

#### 2.11.2 Prima total $
Monto en pesos chilenos de la prima cobrada o pagada (con signo negativo). Solo para opciones.

#### 2.11.3 Inversión Inicial $
Valor total pagado (negativo) o recibido  por la suscripción del contrato (análogo a la prima para el caso de la opción), en pesos chilenos. En el caso de contratos de opciones, este campo deberá quedar en blanco.

#### 2.11.4 Otros gastos asociados al contrato $
Otros gastos incurridos durante el ejercicio en pesos chilenos. 

#### 2.11.5 Otros ingresos asociados al contrato $
Otros ingresos obtenidos durante el ejercicio en pesos chilenos.

#### 2.11.6 Montos pagados o adeudados $
Montos pagados o adeudados al exterior, producto de contratos de derivados celebrados con domiciliadas o residentes en el extranjero, en pesos chilenos.

#### 2.11.7 Modalidad de pago
Forma de pago acordada del campo anterior.
$$\text{MODALIDAD DE PAGO}= \begin{cases}
    1 &\text{En dinero}\\
    2 &\text{En acciones}\\
    3 &\text{En derechos sociales}\\
    4 &\text{En otras especies}
\end{cases}$$

#### 2.11.8 Saldo de garantías al cierre (contratos futuros) $
Para futuros, saldo de garantías vigentes y no utilizada o restituida en pesos. Puede tener signo menos.

## 3 Anexos
### 3.1. Código País Contraparte 
| PAÍS | CÓDIGO |
|---|---|
| Afganistán | AF |
| Albania | AL |
| Alemania | DE |
| Andorra | AD |
| Angola | AO |
| Anguila | AI |
| Antártida | AQ |
| Antigua y   Barbuda | AG |
| Arabia Saudita | SA |
| Argelia | DZ |
| Argentina | AR |
| Armenia | AM |
| Aruba | AW |
| Australia | AU |
| Austria | AT |
| Azerbaiyán | AZ |
| Bahamas | BS |
| Bahrein | BH |
| Bangladesh | BD |
| Barbados | BB |
| Bélgica | BE |
| Belice | BZ |
| Benín | BJ |
| Bermudas | BM |
| Bielorrusia | BY |
| Bolivia | BO |
| Bonaire, San   Eustaquio y Saba | BQ |
| Bosnia y   Herzegovina | BA |
| Botswana | BW |
| Brasil | BR |
| Brunéi   Darussalam | BN |
| Bulgaria | BG |
| Burkina Faso | BF |
| Burundi | BI |
| Bután | BT |
| Cabo Verde | CV |
| Camboya | KH |
| Camerún | CM |
| Canadá | CA |
| Chad | TD |
| Chile | CL |
| China | CN |
| Chipre | CY |
| Ciudad del   Vaticano | VA |
| Colombia | CO |
| Comoras | KM |
| Congo | CG |
| Corea del   Norte | KP |
| Corea del Sur | KR |
| Costa de   Marfil | CI |
| Costa Rica | CR |
| Croacia | HR |
| Cuba | CU |
| Curazao | CW |
| Dinamarca | DK |
| Dominica | DM |
| Ecuador | EC |
| Egipto | EG |
| El Salvador | SV |
| Emiratos   Árabes Unidos | AE |
| Eritrea | ER |
| Eslovaquia | SK |
| Eslovenia | SI |
| España | ES |
| Estados Unidos | US |
| Estonia | EE |
| Etiopía | ET |
| Federación   Rusa (Rusia) | RU |
| Filipinas | PH |
| Finlandia | FI |
| Fiyi | FJ |
| Francia | FR |
| Gabón | GA |
| Gambia | GM |
| Georgia | GE |
| Ghana | GH |
| Gibraltar | GI |
| Granada | GD |
| Grecia | GR |
| Groenlandia | GL |
| Guadalupe   (Francia) | GP |
| Guam (EE.UU.) | GU |
| Guatemala | GT |
| Guayana   Francesa | GF |
| Guernsey | GG |
| Guinea | GN |
| Guinea Bissau | GW |
| Guinea Ecuatorial | GQ |
| Guyana | GY |
| Haití | HT |
| Holanda | NL |
| Honduras | HN |
| Hong Kong | HK |
| Hungría | HU |
| India | IN |
| Indonesia | ID |
| Irán | IR |
| Iraq | IQ |
| Irlanda | IE |
| Isla Bouvet | BV |
| Isla de Man | IM |
| Isla de   Navidad | CX |
| Isla de San   Martín (parte francesa) | MF |
| Isla de San   Martín (parte holandesa) | SX |
| Isla Georgia del Sur e Islas Sandwich del Sur | GS |
| Isla Norfolk | NF |
| Isla Pitcairn | PN |
| Islandia | IS |
| Islas Åland | AX |
| Islas Caimán | KY |
| Islas Cocos | CC |
| Islas Cook | CK |
| Islas Falkland   (Malvinas) | FK |
| Islas Faroe | FO |
| Islas Heard y   McDonald | HM |
| Islas Marianas   del Norte | MP |
| Islas Marshall | MH |
| Islas Menores de Estados Unidos de Ultramar | UM |
| Islas Salomón | SB |
| Islas Svalbard   y Jan Mayen | SJ |
| Islas Turcas y Caicos | TC |
| Islas Vírgenes Americanas | VI |
| Islas   Vírgenes Británicas | VG |
| Islas Wallis y Futuna | WF |
| Israel | IL |
| Italia | IT |
| Jamaica | JM |
| Japón | JP |
| Jersey | JE |
| Jordania | JO |
| Kazajistán | KZ |
| Kenia | KE |
| Kirguistán | KG |
| Kiribati | KI |
| Kuwait | KW |
| Laos | LA |
| Lesoto | LS |
| Letonia | LV |
| Líbano | LB |
| Liberia | LR |
| Libia | LY |
| Liechtenstein | LI |
| Lituania | LT |
| Luxemburgo | LU |
| Macao | MO |
| Macedonia | MK |
| Madagascar | MG |
| Malasia | MY |
| Malawi | MW |
| Maldivas | MV |
| Malí | ML |
| Malta | MT |
| Marruecos | MA |
| Martinica | MQ |
| Mauricio | MU |
| Mauritania | MR |
| Mayotte | YT |
| México | MX |
| Micronesia | FM |
| Moldavia | MD |
| Mónaco | MC |
| Mongolia | MN |
| Montenegro | ME |
| Montserrat | MS |
| Mozambique | MZ |
| Myanmar   (Birmania) | MM |
| Namibia | NA |
| Nauru | NR |
| Nepal | NP |
| Nicaragua | NI |
| Níger | NE |
| Nigeria | NG |
| Niue | NU |
| Noruega | NO |
| Nueva   Caledonia (Francia) | NC |
| Nueva Zelanda | NZ |
| Omán | OM |
| Pakistán | PK |
| Palaos | PW |
| Palestina | PS |
| Panamá | PA |
| Papúa Nueva   Guinea | PG |
| Paraguay | PY |
| Perú | PE |
| Polinesia   (Francia) | PF |
| Polonia (std   LE) | PL |
| Qatar | QA |
| Reino Unido | GB |
| República   Centro Africana | CF |
| República   Checa | CZ |
| República   Democrática del Congo | CD |
| República   Dominicana | DO |
| Reunión   (Francia) | RE |
| Ruanda | RW |
| Rumania | RO |
| Sahara   Occidental | EH |
| Samoa | WS |
| Samoa   Americana | AS |
| San Bartolomé | BL |
| San Cristóbal   y Nieves | KN |
| San Marino | SM |
| San Pedro y   Miguelón | PM |
| San Vicente y   las Granadinas | VC |
| Santa Elena, Ascensión y   Tristán de Acuña | SH |
| Santa Lucía | LC |
| Santo Tomé y   Príncipe | ST |
| Senegal | SN |
| Serbia | RS |
| Seychelles | SC |
| Sierra Leona | SL |
| Singapur | SG |
| Siria | SY |
| Somalia | SO |
| Sri Lanka | LK |
| Suazilandia | SZ |
| Sudáfrica | ZA |
| Sudán | SD |
| Sudán del Sur | SS |
| Suecia | SE |
| Suiza | CH |
| Surinam | SR |
| Tailandia | TH |
| Taiwán | TW |
| Tanzania | TZ |
| Tayikistán | TJ |
| Territorio   Británico del Océano Índico | IO |
| Territorios   Australes Franceses | TF |
| Timor Oriental | TL |
| Togo | TG |
| Tokelau | TK |
| Tonga | TO |
| Trinidad y   Tobago | TT |
| Túnez | TN |
| Turkmenistán | TM |
| Turquía | TR |
| Tuvalu | TV |
| Ucrania | UA |
| Uganda | UG |
| Uruguay | UY |
| Uzbekistán | UZ |
| Vanuatu | VU |
| Venezuela | VE |
| Vietnam | VN |
| Yemen | YE |
| Yibouti | DJ |
| Zambia | ZM |
| Zimbabwe | ZW |
| Rentas fuente   extranjeta | RFE    |