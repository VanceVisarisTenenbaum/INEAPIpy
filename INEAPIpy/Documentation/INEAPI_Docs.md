# INE API

El [servicio web del INE](https://www.ine.es/dyngs/DAB/index.htm?cid=1099) permite obtener los datos publicos de la misma utilizando su sistema a través de peticiones URL.

El formato de los datos recibidos dependerá de la URL solicitada, pero para este wrapper escrito en Python solo se utiliza la API JSON, es decir, que todos los valores recibidos serán en formato JSON.

Para más infromación consulte la [página oficial](https://www.ine.es/dyngs/DAB/index.htm?cid=1099).

## Referencia API

Tal y como se describe en la [referencia](https://www.ine.es/dyngs/DAB/index.htm?cid=1100) para hacer peticiones es necesario construir la url que realice la petición. Esta url es siempre de la forma:

https://servicios.ine.es/wstempus/js/{idioma}/{función}/{input}\[?parámetros\]

Donde:
* idioma: Es el idioma (EN o ES) de la API. Como no he visto diferencias en los resultados que he probado, solo se usará el idoma español.
* funcion: Es una de las funciones proporcionadas en la API del INE.
* input: Es el input de dicha funcion.
* parámetros: Son los parametros de los resultados, serián equivalentes a los kwargs en Python.

Como no se describen en la documentación oficial, vamos a describir primero qué son los inputs y parametros y qué opciones hay.

### Inputs

Los Inputs son los parámetros obligatorios de las funciones (en Python, los args), y son siempre algún identificador de alguno de los objetos que definen la base de datos.

En la documentacion se describen únicamente los siguientes:
* Variables.
* Valores.
* Series.
* Tablas.

Sin embargo, hay que añadir los siguientes.
* Operaciones.
* Clasificaciones.
* Unidades.
* Escalas.
* Publicaciones.
* Periodos.
* Periodicidades.

En [INEAPIDiagram.mmd] se encuentra el diagrama mermaid que muestra todos los campos y las relaciones entre estos. Para visualizarlo junto con los atributos que los definen es necesario utilizar la app web [mermaid](https://mermaid.live/edit#pako:eNq1WGtv2zYU_SsEgQAxYGd2m9iNMAwo8hjStUnRtfswCBBoiU6ISKRH0kUzI_99l9SLpinZTjN_CMiro8tzX4dC1jgVGcURHo1GMddM5zRCN7dX6JJoMieKxtw-SXOi1CUj95IUMUfwsxZ0t6SSpEzwdWk1v5ssQozr1nAhsuTm7ipCSsvWeiuKuaSeEaDsXnjGL3RBJeUpI0mEPjKlj1vLoIQ9u6Q-U8nAT8oykvXx2o9BwLXo8_oXyYX0bC4jiMHdtiBIb8I4WP34P1EVfhDMVjCq0pjkRPbEtppf0_SBvE_1wVmzL1rgLxv2Kl9NzKJ99J4_Cce1TyVn6c7GClLZK9dN39Yd1RgGjqc2IcZRuwswbjuyj_BXple5X7BvMu8qyVcyz8n_kwEnxWVw9W67eNB7HfVLjLVGbDcEJCVZMB7oi2-5ZgVJPgGvRXVuAPW7XC2Fskmo62RN1uIU6k9gATNSQewupAt2MvtHVzJwTcFTvXyJXt0KTTzTB-gu-c-Kkc8kk1RVTC2hMNPy9FdWL5uZXqW-u_QcuoPSrHeQuKQpFDc3YR6ugnv05QUE07QNgDb2LexKpcQ2Trlwmo9XDMqFK7SamIsvUB4bF9FC2Rwmxx9WSqOFkCazkuknpB-Ihj9MIUmXUGLKtULEeWcQOZtAcTaieKkAZ0SHfJuD1z3gUpuWwuAgL_XyJTruXIGLXBDtTmkqqQbsXIg8JHbVqa_c9GYaHZea_tD-wF4_JuZwgzy-fhwiLjS6_mMQPLtBej6sX_Osi0db_HXfwAUj7OxYQ6RWE7MeHNLM9SPDzFfT_Tu8bu6uvi4p_3xRba8B7ntXgssxP3xySKqbbj2GR4OfIdHeTwcRqXwcHX2hOdEgAKo0NJKLYjyJMRqNfoMVh1X7wbELuXmVVfO7gTKrbTV2Png60KIB1iK9dbh3Z3RBrU__A8umcQ-iHTj_6uhzJ7ogJoa2piWq3QdyDVNWouq092Ng2QewQ7XF2UtqGLSdpw6cn6cwLHDJhoHubRtGuCLmIn5tIf5Nue3IS9TRUftKx4GAuRBFAbJFMytsc6o1leg7U0OkGE8pYhqBvOkHihQpKCIKqZZDxwG8orsTZPR5B9kmqNfgupWGzWs9CNljGixrPMT38OWPIy1XdIgLKgtittiqXoyBVkFjHMEyI_IxxjF_hneWhP8tRFG_JsXq_gFHC5Ir2K2W5oOk-idDYwWNy6i8ECuucfRmYn3gaI1_4OhscjJ9NzudTc9Pz2ezt2dnQ_yEo8np-OTNeDoZj8-ns8n56fTt8xD_a08dn7ybnT3_BwVCAGc)

En este caso, además, hay que clarificar que Identificador hace tanto referencia al Id, un número, como el COD, un código. Es decir, que estos objetos se pueden identificar usando tanto un número como un código. Algo que se verán en algunos ejemplos más adelante y explica por que en las funciones de este paquete se especifican que los tipos pueden ser tanto int como str.

### Parámetros

Los parámetros son aquellos inputs que afectan únicamente a la forma y/o cantidad de datos que se devolverán en la petición. Los parámetros los podemos clasificar según si afectan a la forma de los resultados de las peticiones y las que afectan a la cantidad de datos recibidos.

#### Detalle

* det: Se puede definir como el nivel de detalle de las respuestas. Es decir, si los atributos de las respuestas se muestran únicamente como identificadores o con la información completa.
* tip: Se puede definir como el modo en el que se muestran las respuestas. Los valores posibles son:
    * '': Vacío, no altera los resultados.
    * A: Amigable, elimina los Ids (el identificador de número) y/o los sustituye por los COD (el identificador de código)
    * M: Metadata, añade el atributo metadata a los resultados.
    * AM: Combinación de los dos anteriores.

Para clarificar estas definiciones se tienen los siguientes ejemplos.

##### Nivel de detalle

Los siguientes ejemplos son los resultados de las siguientes peticiones. De este modo poder comparar el efecto del nivel de detalle.

URL Base: https://servicios.ine.es/wstempus/js/ES/SERIE/IPC251852
* Petición: Sin det, equivalente a det=0

```json
{
  "Id": 251852,
  "COD": "IPC251852",
  "FK_Operacion": 25,
  "Nombre": "Total Nacional. Índice general. Índice. ",
  "Decimales": 3,
  "FK_Periodicidad": 1,
  "FK_Publicacion": 8,
  "FK_Clasificacion": 90,
  "FK_Escala": 1,
  "FK_Unidad": 133
}
```

* Petición: det = 1

En este segundo caso se puede comprobar que desaparecen los FK del primer nivel y se transforman en la informacioń completa del objeto, sin embargo, no ocurre con el segundo nivel.
```json
{
  "Id": 251852,
  "COD": "IPC251852",
  "Operacion": {
    "Id": 25,
    "Cod_IOE": "30138",
    "Nombre": "Índice de Precios de Consumo (IPC)",
    "Codigo": "IPC"
  },
  "Nombre": "Total Nacional. Índice general. Índice. ",
  "Decimales": 3,
  "Periodicidad": {
    "Id": 1,
    "Nombre": "Mensual",
    "Codigo": "M"
  },
  "Publicacion": {
    "Id": 8,
    "Nombre": "Índice de Precios de Consumo",
    "FK_Periodicidad": 1,
    "FK_PubFechaAct": 11430
  },
  "Clasificacion": {
    "Id": 90,
    "Nombre": "Base 2021 (IPC)",
    "Fecha": 1643583600000
  },
  "Escala": {
    "Id": 1,
    "Nombre": " ",
    "Factor": "1E0",
    "Codigo": null,
    "Abrev": null
  },
  "Unidad": {
    "Id": 133,
    "Nombre": "Índice",
    "Codigo": null,
    "Abrev": null
  }
}
```

* Petición: det = 2

Si bien es dificil ver, en este caso, ha ocurrido en el segundo nivel de profundidad, lo mismo que ocurrioń anteriormente en el primer nivel.
```json
{
  "Id": 251852,
  "COD": "IPC251852",
  "Operacion": {
    "Id": 25,
    "Cod_IOE": "30138",
    "Nombre": "Índice de Precios de Consumo (IPC)",
    "Codigo": "IPC",
    "Referencia": [
      {
        "Id": 65,
        "Titulo": "Índice de precios de consumo (IPC)",
        "Url": "/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736176802&idp=1254735976607"
      }
    ]
  },
  "Nombre": "Total Nacional. Índice general. Índice. ",
  "Decimales": 3,
  "Periodicidad": {
    "Id": 1,
    "Nombre": "Mensual",
    "Codigo": "M"
  },
  "Publicacion": {
    "Id": 8,
    "Nombre": "Índice de Precios de Consumo",
    "Periodicidad": {
      "Id": 1,
      "Nombre": "Mensual",
      "Codigo": "M"
    },
    "Operacion": [
      {
        "Id": 25,
        "Cod_IOE": "30138",
        "Nombre": "Índice de Precios de Consumo (IPC)",
        "Codigo": "IPC"
      }
    ],
    "PubFechaAct": {
      "Id": 11430,
      "Nombre": "Índice de Precios de Consumo Junio 2025",
      "Fecha": 1752562800000,
      "FK_Periodo": 6,
      "Anyo": 2025
    }
  },
  "Clasificacion": {
    "Id": 90,
    "Nombre": "Base 2021 (IPC)",
    "Fecha": 1643583600000
  },
  "Escala": {
    "Id": 1,
    "Nombre": " ",
    "Factor": "1E0",
    "Codigo": null,
    "Abrev": null
  },
  "Unidad": {
    "Id": 133,
    "Nombre": "Índice",
    "Codigo": null,
    "Abrev": null
  }
}
```

El patrón sigue.

##### Tipología o modo

Para la petición anterior. Recordemos el valor sin utilizar ningún parámetro.

URL Base: https://servicios.ine.es/wstempus/js/ES/SERIE/IPC251852
* Petición: Sin tip, equivalente a tip=''
```json
{
  "Id": 251852,
  "COD": "IPC251852",
  "FK_Operacion": 25,
  "Nombre": "Total Nacional. Índice general. Índice. ",
  "Decimales": 3,
  "FK_Periodicidad": 1,
  "FK_Publicacion": 8,
  "FK_Clasificacion": 90,
  "FK_Escala": 1,
  "FK_Unidad": 133
}
```

* Petición: tip=A

En este caso, los FK se han sustituido por T3 y los valores que se indican son los nombres de los objetos que estén indicando. Ademas se observa que el Id ha desaparecido. El mismo patroń ocurre para el resto de niveles.
```json
{
  "COD": "IPC251852",
  "T3_Operacion": "Índice de Precios de Consumo (IPC)",
  "Nombre": "Total Nacional. Índice general. Índice. ",
  "Decimales": 3,
  "T3_Periodicidad": "Mensual",
  "T3_Publicacion": "Índice de Precios de Consumo",
  "T3_Clasificacion": "Base 2021 (IPC)",
  "T3_Escala": " ",
  "T3_Unidad": "Índice"
}
```

* Petición: tip=M

En este caso, no se han sustituido los FK por T3, pero se ha añadido el atributo o clave MetaData, qué en este caso, son una lista de valores.
```json
{
  "Id": 251852,
  "COD": "IPC251852",
  "FK_Operacion": 25,
  "Nombre": "Total Nacional. Índice general. Índice. ",
  "Decimales": 3,
  "FK_Periodicidad": 1,
  "FK_Publicacion": 8,
  "FK_Clasificacion": 90,
  "FK_Escala": 1,
  "FK_Unidad": 133,
  "MetaData": [
    {
      "Id": 16473,
      "FK_Variable": 349,
      "Nombre": "Total Nacional",
      "Codigo": "00"
    },
    {
      "Id": 304092,
      "FK_Variable": 762,
      "Nombre": "Índice general",
      "Codigo": "00"
    },
    {
      "Id": 83,
      "FK_Variable": 3,
      "Nombre": "Índice",
      "Codigo": ""
    }
  ]
}
```

Para el caso AM es una combinación de ambos, por lo que se puede intuir el resultado.

#### Cantidad

* geo: Obtiene resultados en funcion del ámbito geografico. Los valores posibles son:
    * 0: Resultados nacionales.
    * 1: Resultados por comunidades autónomas, provincias, municipios y otras desagregaciones.
* page: La página de los resultados. En caso de que la petición devuelva más de 500 resultados, la página indica el chunk de la petición.
* nult: La cantidad de resultados, similar a page, sin embargo se utiliza cuando lo que se solicitan son datos en vez de metadatos.
* date: La fecha o rango de fechas de la petición. Afecta a los datos solicitados y no a los metadatos.
* clasif: Obtiene los resultados para una determinada clasificación.
* tv: Se utiliza para filtrar por pares variable valor.
* g: Igual que tv.
* p: Se utiliza para filtrar una publicación.


No es necesario clarificar con ejemplos estos casos ya que solamente afecta a la cantidad de resultados que se ven.

En el paquete de python se utilizan nombres ligeramente distintos, en la siguiente tabla se tienen las relaciones de nombres entre la API del INE y este paquete de Python.

| Nombre Oficial | Nombre Paquete                                | Valores posibles          |
|----------------|-----------------------------------------------|---------------------------|
| det            | detail_level                                  | int >= 0 (mostly 0, 1, 2) |
| tip            | tipology                                      | '', 'A', 'M', 'AM'        |
| geo            | geographical_level                            | None, 0, 1                |
| tv             | metadata_filtering (a dictionary)             |                           |
| g              | metadata_filtering (a dictionary)             |                           |
| p              | metadata_filtering (a dictionary)             |                           |
| page           | page                                          | int > 0                   |
| nult           | count                                         | int > 0                   |
| date           | list_of_date (a list of dates or date ranges) |                           |

### Lista de funciones

Ya están en la página oficial de referencia, sin embargo existen algunas más no indicadas en la documentación. La lista completa es la siguiente:

* OPERACIONES_DISPONIBLES
* OPERACION
* VARIABLES
* VARIABLES_OPERACION
* VALORES_VARIABLES
* VALORES_VARIABLEOPERACION
* VALORES_HIJOS
* TABLAS_OPERACION
* GRUPOS_TABLA
* VALORES_GRUPOSTABLA
* SERIE
* SERIES_OPERACION
* VALORES_SERIE
* SERIES_TABLA
* SERIE_METADATAOPERACION
* PUBLICACIONES
* PUBLICACIONES_OPERACION
* PUBLICACIONFECHA_PUBLICACION
* DATOS_SERIE
* DATOS_TABLA
* DATOS_METADATAOPERACION
* UNIDAD
* UNIDADES
* ESCALA
* ESCALAS
* PERIODO
* PERIODICIDAD
* PERIODICIDADES
* OPERACIONES
* CLASIFICACIONES
* VARIABLE
