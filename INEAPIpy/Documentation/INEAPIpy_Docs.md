# INEAPIpy

Este paquete de Python actúa como Wrapper para la API del INE. Este proporciona funciones para realizar peticiones y obtener los resultados del INE.


## Inputs

Antes de definir las funciones, es necesario conocer los inputs que los conforman.

* Indetificadores de Objetos
    * ```py op_id```: Identificador de **Operación**.
    * ```py var_id```: Identificador de **Variable**.
    * ```py val_id```: Identificador de **Valor**.
    * ```py tab_id```: Identificador de **Tabla**.
    * ```py group_id```: Identificador de **Grupo de Tablas**.
    * ```py serie_id```: Identificador de **Serie**.
    * ```py unit_id```: Identificador de **Unidad**.
    * ```py scale_id```: Identificador de **Escala**.
    * ```py period_id```: Identificador de **Periodo**.
    * ```py periodicity_id```: Identificador de **Periodicidad**.
    * ```py classification_id```: Identificador de **Clasificación**.
    * ```py publication_id```: Identificador de **Publicación**.
* Parámetros de configuración de respuesta:
    * ```py detail_level```: Nivel de detalle.
    * ```py tipology```: Tipo o mode de representación de respuesta.
* Parámetros de filtrado:
    * ```py geographical_level```: Selección de datos geográficos.
    * ```py metadata_filtering```: Parámetros de filtrado por pares variable-valor.
    * ```py list_of_dates```: Lista de fechas a filtrar.
    * ```py count```: Número de resultados a mostrar (Datos).
    * ```py page```: Página de resultados (Metadatos).
    
En la siguiente tabla se encuentran los valores que pueden tomar los inputs y sus valores por defecto.

| Input                                | Tipos válidos                                                | Valores por defecto        |
|--------------------------------------|--------------------------------------------------------------|----------------------------|
| Identificadores (op_id, var_id, ...) | int, str, None                                               | None si no es obligatorio. |
| detail_level                         | int >= 0                                                     | 0                          |
| tipology                             | '', 'A', 'M', 'AM'                                           | ''                         |
| geographical_level                   | int >= 0, None                                               | None                       |
| metadata_filtering                   | Dict[int \| str, List[int \| str] \| int \| str] \| None     | EmptyDict                  |
| list_of_dates                        | List[str \| List[str \| None] \| Tuple[str \| None]] \| None | None                       |
| count                                | int > 0 \| None                                              | None                       |
| page                                 | int > 0 \| None                                              | None                       |


### ```py metadata_filtering``` Input.

Para el filtrado mediante pares variable valor se utiliza este input ***metadata_filtering***. Este input se construye con la siguiente estructura:
```py
{
    var_id_1: [val_id_1, ..., val_id_i],
    var_id_2: [val_id_1, ..., val_id_j],
    
    var_id_n: [val_id_1, ..., val_id_k],
    publicacion: pub_id
}
```

Dónde, ```py var_id``` representa la variable y ```py val_id``` el valor asociado a dicha variable. Mientra que ```py pub_id``` es el identificador de publicación. Todos son opcionales, aunque depende de la petición del INE. Ejemplo:

```py
# Supón que hacemos la consulta https://servicios.ine.es/wstempus/js/ES/SERIE_METADATAOPERACION/IPC?g1=115:29&g2=3:84&g3=762:&p=1&det=2&tip=A

# En este caso, metadata_filtering sería:

metadata_filtering = {
    115: [29],
    3: [84],
    762: [],
    "publicacion": 1
}
```

### ```py list_of_dates``` Input

Este filtro se utiliza en la selección de datos y permite seleccionar fechas concretas, y/o rangos de fechas. El input se construye de la siguiente manera:

```py
[date, (date, None), (None, date), (date, date)]
```

Dónde ***date*** se construye con el siguiente formato: "YYYY-MM-DD" y un valor solo representa una fecha única, y el rango se construye con una tupla de dos ***fechas*** o una ***fecha*** y un ***None***, siendo el ***None*** la carencia de límite. Ejemplos:

```py
# petición a https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/50902?date=20240101:20241231&date=20230101&date=20250101:

# En este caso, list of dates sería:

list_of_dates = [('2024-01-01', '2024-12-31'), '2023-01-01', ('2025-01-01', None)]
```


## Contenido

El paquete proporciona los siguientes módulos:

* Bridge
* INE_functions
* INE_filtering (No es necesario usarlo)
* INE_URL_Treatment (No es necesario usarlo)

### Bridge

Este paquete proporciona cuatro clases para realizar las peticiones al INE. Las dos primeras proprocionan exactamente los mismos métodos, sin embargo, el primero es Síncrono y el segundo Asíncrono. Las dos clases siguientes extienden la funcionalidad de las dos primeras proporcionando varios métodos adicionales para realizar las mismas peticiones de la primera clase, pero utilizando una estructura diferente.
    
Todas las clases utilizan un objeto RequestManager, que se encarga de realizar las peticiones sin necesidad de iniciar tu propia instancia de Sesión y la cierra si tras cierto tiempo no se realizan peticiones.
    
Si no quieres que existan estos procesos, puedes usar el módulo INE_functions, cuyas funciones sólo devuelven las urls.


#### ```py INEAPIClientSync```, ```py INEAPIClientAsync```

> Wrapper de la api del INE, realiza las peticiones de manera sincrona o asincrona según la clase elegida.

Todos los métodos devuelven los resultados del INE y se pueden visualizar mejor en el [diagrama](https://mermaid.live/view?gist=https://gist.github.com/VanceVisarisTenenbaum/5b2890f4ccc5517ba9289c5c271af1fa)

##### __init__(mode, RM, sleep_time, print_url)

> Init of class.

* ```py Mode```: Literal['raw', 'py', 'pydantic'] el modo de la clase.
    * ```py raw```: Devuelve los resultados como un string directamente de la API del INE.
    * ```py py```: Devuelve los resultados como un diccionario o como una lista.
    * ```py pydantic```: Devuelve los resultados como un objeto de pydantic y comprueba que son correctos.
* ```py RM```: Instancia de RequestsManagement.RequestManager en caso de ya tener una. Si no sabes lo que es es un objeto para manejar sesiones de forma automática del submodulo. Se inicia solo si no lo especifícas.
* ```py sleep_time```: Cuanto tiempo debe esperar entre peticiones.
* ```py print_url```: Establece esta opción como True si quieres imprimir la url después de cada petición.

##### Métodos de las clases.

* ```py close_all_sessions()```: Cierra todas las sesiones del gestor de peticiones. Se cierra sola después de cierto tiempo, o cuando se cierra el kernel de Python.
* ```py __get_data(url)```: Simplifica el proceso de obtener los datos.

Todos los métodos siguientes siguen la conveción ***get_NombreFuncionIneEnMinusculas*** y obtienen los resultados especificados en su [documentación](https://ine.es/dyngs/DAB/index.htm?cid=1100).

* ```py get_datos_tabla(tab_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```py get_datos_serie(serie_id, detail_level, tipology, count, list_of_dates)```
* ```py get_datos_metadataoperacion(op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```py get_operaciones_disponibles(detail_level, geographical_level, page, tipology)```
* ```py get_operaciones(detail_level, page, tipology)```
* ```py get_operacion(op_id, detail_level, tipology)```
* ```py get_variables(page)```
* ```py get_variable(var_id)```
* ```py get_variables_operacion(op_id, page)```
* ```py get_valores_variable(var_id, detail_level, classification_id)```
* ```py get_valores_variableoperacion(var_id, op_id, detail_level)```
* ```py get_tablas_operacion(op_id, detail_level, geographical_level, tipology)```
* ```py get_grupos_tabla(tab_id)```
* ```py get_valores_grupostabla(tab_id, group_id, detail_level)```
* ```py get_serie(serie_id, detail_level, tipology)```
* ```py get_series_operacion(op_id, detail_level, tipology, page)```
* ```py get_valores_serie(serie_id, detail_level)```
* ```py get_series_tabla(tab_id, detail_level, tipology, metadata_filtering)```
* ```py get_serie_metadataoperacion(op_id, detail_level, tipology, metadata_filtering)```
* ```py get_periodicidades()```
* ```py get_periodicidad(periodicity_id)```
* ```py get_publicaciones(detail_level, tipology)```
* ```py get_publicaciones_operacion(op_id, detail_level, tipology)```
* ```py get_publicacionfecha_publicacion(publication_id, detail_level, tipology)```
* ```py get_clasificaciones()```
* ```py get_clasificaciones_operacion(op_id)```
* ```py get_valores_hijos(var_id, val_id, detail_level)```
* ```py get_unidades()```
* ```py get_unidad(unit_id)```
* ```py get_escalas(tipology)```
* ```py get_escala(scale_id, tipology)```
* ```py get_periodo(period_id)```


#### ```py EasyINEAPIClientSync```, ```py EasyINEAPIClientAsync```

Es la misma clase que las anteriores, pero añade varios métodos que simplifican las peticiones. Todos los resultados se pueden ver de manera visual en el [diagrama](https://mermaid.live/view?gist=https://gist.github.com/VanceVisarisTenenbaum/5b2890f4ccc5517ba9289c5c271af1fa).

##### Métodos adicionales.

* ```py get_operations_(op_id, detail_level, geographical_level, extra_op, page, tipology)```: Devuelve los datos de todas las operaciones o las especificadas.
    * Si ```py extra_op=True```, realiza una petición que devuelve algunas operaciones extra.
    * Si se especifica ```py op_id```, devuelve la operación especificada.
* ```py get_variables_(op_id, var_id, page)```: Devuelve las variables disponibles.
    * Si se especifica ```py op_id```, devuelve las variables asociadas a dicha operación.
    * Si se especifica ```py var_id```, devuelve dicha variable.
    * Si no se especifica ningún parámetro, devuelve todas las variables disponibles.
* ```py get_values_(var_id, classification_id, op_id, val_id, detail_level)```: Devuelve los valores asociados a la variable especificada.
    * ```py var_id``` es un parámetro obligatorio.
    * Si se especifica ```py classification_id```, devuelve los valores asociados a dicha variable y dicha operación.
    * Si se especifica ```py op_id```, devuelve los valores asociados a dicha variable y dicha operación.
    * Si se especifica ```py val_id```, devuelve los valores hijos dicho valor.
* ```py get_tables_(op_id, tab_id, group_id, detail_level, geographical_level, tipology)```: Devuelve las tablas, grupos de tabla o valores según el input.
    * Si se especifica ```py op_id```, devuelve las tablas asociadas a dicha operación.
    * Si se especifica ```py tab_id```, devuelve los grupos de tabla disponibles para dicha tabla.
    * Si se especifica ```py tab_id``` y ```py group_id```, devuelve los valores disponibles para dicho grupo.
* ```py get_series_(serie_id, op_id, tab_id, serie_data, operation_data, detail_level, tipology, page, metadata_filtering)```: Devuelve la información disponible de las series.
    * La función tiene varios modos, y creo que dividirla en dos hubiese sido más difícil de interpretar.
    * Si se especifica ```py serie_id```:
        * Si ```py serie_data=metadata``` devuelve los datos de dicha serie.
        * Si ```py serie_data=values``` devuelve los valores de dicha serie.
    * Si se especifica ```py op_id```:
        * Si ```py operation_data=series``` devuelve las series asociadas a dicha operación.
        * Si ```py operation_data=metadata``` devuelve las series asociadas a dicha operación filtradas con ```py metadata_filtering```.
* ```py get_publications_(op_id, publication_id, detail_level, tipology)```: Devuelve las publicaciones disponibles.
    * Si no se especifica ningún input, devuelve todas las publicaciones.
    * Si se especifica ```py op_id```, devuelve las publicacionesa asociadas a dicha operación.
    * Si se especifica ```py publication_id```, devuelve las fechas de publicación asociadas a dicha publicación.
* ```py get_data_(serie_id, tab_id, op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```: Devuelve los datos de las series.
    * Si se especifica ```py serie_id```, devuelve los datos asociados a dicha serie.
    * Si se especifica ```py tab_id```, devuelve todas las series con sus datos asociados a dicha tabla. Se puede aplicar ```py metadata_filtering```
    * Si se especifica ```py op_id```, se tiene que especificar ```py metadata_filtering``` y devuelve todas las series con sus datos asociados a dicha operación y dichos filtros.
* ```py get_units_(unit_id)```: Devuelve las unidades.
    * Si se especifica ```py unit_id```, devuelve dicha unidad.
    * Si no se especifica nada, devuelve todas las unidades.
* ```py get_scales_(scale_id, tipology)```: Devuelve las escalas.
    * Si se especifica ```py scale_id```, devuelve dicha escala.
    * Si no se especifica nada, devuelve todas las escalas.
* ```py get_periods_(period_id)```: Devuelve el periodo especificado.
* ```py get_periodicities_(periodicity_id)```: Devuelve las periodicidades.
    * Si no se especifica la periodicidad, devuelve todas las periodicidades.
    * Si se especifica ```py periodicity_id```, devuelve la periodicidad especificada.
* ```py get_classifications_(op_id)```: Devuelve las clasificaciones.
    * Si no se especifica nada, devuelve todas las clasificaciones.
    * Si se especifica ```py op_id```, devuelve las clasificaciones asociadas a dicha operación.


### INE_functions

Este módulo contiene las mismas funciones que el INE adaptadas a este paquete y en minúsculas. Todas estas funciones devuelven la URL necesaria para hacer la petición.

* ```py datos_tabla(tab_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```py datos_serie(serie_id, detail_level, tipology, count, list_of_dates)``` 
* ```py datos_metadataoperacion(op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```py operaciones_disponibles(detail_level, geographical_level, page, tipology)```: No hay más de 500 operaciones asi que page>1 no devuelve nada.
* ```py operaciones(detail_level, page, tipology)```: Añade algunas operaciones. No está en la documentación oficial.
* ```py operacion(op_id, detail_level, tipology)```
* ```py variables(page)```
* ```py variable(var_id)```: No está documentada oficialmente.
* ```py variables_operacion(op_id, page)```
* ```py valores_variable(var_id, detail_level, classification_id)```
* ```py valores_variableoperacion(var_id, op_id, detail_level)```
* ```py tablas_operacion(op_id, detail_level, geographical_level, tipology)```
* ```py grupos_tabla(tab_id)```
* ```py valores_grupostabla(tab_id, group_id, detail_level)```
* ```py serie(serie_id, detail_level, tipology)```
* ```py series_operacion(op_id, detail_level, tipology, page)```
* ```py valores_serie(serie_id, detail_level)```
* ```py series_tabla(tab_id, detail_level, tipology, metadata_filtering)```
* ```py serie_metadataoperacion(op_id, detail_level, tipology, metadata_filtering)```
* ```py periodicidades()```
* ```py periodicidad(periodicity_id)```: No está documentada oficialmente.
* ```py publicaciones(detail_level, tipology)```
* ```py publicaciones_operacion(op_id, detail_level, tipology)```
* ```py publicacionfecha_publicacion(publication_id, detail_level, tipology)```
* ```py clasificaciones()```
* ```py clasificaciones_operacion(op_id)```
* ```py valores_hijos(var_id, val_id, detail_level)```
* ```py unidades()```: No está documentada oficialmente.
* ```py unidad(unit_id)```: No está documentada oficialmente.
* ```py escalas(tipology)```: No está documentada oficialmente.
* ```py escala(scale_id, tipology)```: No está documentada oficialmente.
* ```py periodo(period_id)```: No está documentada oficialmente.
