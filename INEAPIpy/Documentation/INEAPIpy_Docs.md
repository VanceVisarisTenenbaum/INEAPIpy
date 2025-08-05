# INEAPIpy

Este paquete de Python actúa como Wrapper para la API del INE. Este proporciona funciones para realizar peticiones y obtener los resultados del INE.


## Inputs

Antes de definir las funciones, es necesario conocer los inputs que los conforman.

* Indetificadores de Objetos
    * op_id: Identificador de **Operación**.
    * var_id: Identificador de **Variable**.
    * val_id: Identificador de **Valor**.
    * tab_id: Identificador de **Tabla**.
    * group_id: Identificador de **Grupo de Tablas**.
    * serie_id: Identificador de **Serie**.
    * unit_id: Identificador de **Unidad**.
    * scale_id: Identificador de **Escala**.
    * period_id: Identificador de **Periodo**.
    * periodicity_id: Identificador de **Periodicidad**.
    * classification_id: Identificador de **Clasificación**.
    * publication_id: Identificador de **Publicación**.
* Parámetros de configuración de respuesta:
    * detail_level: Nivel de detalle.
    * tipology: Tipo o mode de representación de respuesta.
* Parámetros de filtrado:
    * geographical_level: Selección de datos geográficos.
    * metadata_filtering: Parámetros de filtrado por pares variable-valor.
    * list_of_dates: Lista de fechas a filtrar.
    * count: Número de resultados a mostrar (Datos).
    * page: Página de resultados (Metadatos).
    
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


### metadata_filtering Input.

Para el filtrado mediante pares variable valor se utiliza este input ***metadata_filtering***. Este input se construye con la siguiente estructura:
```py
{
    var_id_1: [val_id_1, ..., val_id_i],
    var_id_2: [val_id_1, ..., val_id_j],
    
    var_id_n: [val_id_1, ..., val_id_k],
    publicacion: pub_id
}
```

Dónde, var_id representa la variable y val_id el valor asociado a dicha variable. Mientra que pub_id es el identificador de publicación. Todos son opcionales, aunque depende de la petición del INE. Ejemplo:

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

### list_of_dates Input

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
<details>
    <summary>Bridge Module</summary>
    
    Este paquete proporciona cuatro clases para realizar las peticiones al INE. Las dos primeras proprocionan exactamente los mismos métodos, sin embargo, el primero es Síncrono y el segundo Asíncrono. Las dos clases siguientes extienden la funcionalidad de las dos primeras proporcionando varios métodos adicionales para realizar las mismas peticiones de la primera clase, pero utilizando una estructura diferente.
    
    Todas las clases utilizan un objeto RequestManager, que se encarga de realizar las peticiones sin necesidad de iniciar tu propia instancia de Sesión y la cierra si tras cierto tiempo no se realizan peticiones.
    
    Si no quieres que existan estos procesos, puedes usar el módulo INE_functions, cuyas funciones sólo devuelven las urls.
    
    
</details>


#### INEAPIClientSync, INEAPIClientAsync

> Wrapper for INE API, makes requests using sync requests package.

All methods make the request and retreive the results.

##### __init__(mode, RM, sleep_time, print_url)

> Init of class.

Mode: Literal['raw', 'py', 'pydantic']

    raw: returns the result straight from INE API, without checking.
    py: returns the result as python dict
    pydantic: returns the result as pydantic object.

RM: RequestsManagement.RequestManager instance if you already have one.

sleep_time: is the sleep time after each request.

print_url: is the option to set if you want to print URLs after each
request.

##### close_all_sessions()

> Closes all requests sessions.

##### __get_data(url)

> Just to simplify the usage of function.

##### get_datos_tabla(tab_id, detail_level, tipology, count, list_of_dates, metadata_filtering)

> Process for DATOS_TABLA. Returns content.

##### get_datos_serie(serie_id, detail_level, tipology, count, list_of_dates)

> Process for DATOS_SERIE. Returns content.

##### get_datos_metadataoperacion(op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)

> Process for DATOS_METADATAOPERACION. Returns content.

##### get_operaciones_disponibles(detail_level, geographical_level, page, tipology)

> Process for OPERACIONES_DISPONIBLES. Returns content.

##### get_operaciones(detail_level, page, tipology)

> Process for OPERACIONES. Returns content.

##### get_operacion(op_id, detail_level, tipology)

> Process for OPERACION. Returns content.

##### get_variables(page)

> Process for VARIABLES. Returns content.

##### get_variable(var_id)

> Process for VARIABLE. Returns content.

##### get_variables_operacion(op_id, page)

> Process for VARIABLES_OPERACION. Returns content.

##### get_valores_variable(var_id, detail_level, classification_id)

> Process for VALORES_VARIABLE. Returns content.

##### get_valores_variableoperacion(var_id, op_id, detail_level)

> Process for VALORES_VARIABLEOPERACION. Returns content.

##### get_tablas_operacion(op_id, detail_level, geographical_level, tipology)

> Process for TABLAS_OPERACION. Returns content.

##### get_grupos_tabla(tab_id)

> Process for GRUPOS_TABLA. Returns content.

##### get_valores_grupostabla(tab_id, group_id, detail_level)

> Process for VALORES_GRUPOSTABLA. Returns content.

##### get_serie(serie_id, detail_level, tipology)

> Process for SERIE. Returns content.

##### get_series_operacion(op_id, detail_level, tipology, page)

> Process for SERIES_OPERACION. Returns content.

##### get_valores_serie(serie_id, detail_level)

> Process for VALORES_SERIE. Returns content.

##### get_series_tabla(tab_id, detail_level, tipology, metadata_filtering)

> Process for SERIES_TABLA. Returns content.

##### get_serie_metadataoperacion(op_id, detail_level, tipology, metadata_filtering)

> Process for SERIE_METADATAOPERACION. Returns content.

##### get_periodicidades()

> Process for PERIODICIDADES. Returns content.

##### get_periodicidad(periodicity_id)

> Process for PERIODICIDAD. Returns content.

##### get_publicaciones(detail_level, tipology)

> Process for PUBLICACIONES. Returns content.

##### get_publicaciones_operacion(op_id, detail_level, tipology)

> Process for PUBLICACIONES_OPERACION. Returns content.

##### get_publicacionfecha_publicacion(publication_id, detail_level, tipology)

> Process for PUBLICACIONFECHA_PUBLICACION. Returns content.

##### get_clasificaciones()

> Process for CLASIFICACIONES. Returns content.

##### get_clasificaciones_operacion(op_id)

> Process for CLASIFICACIONES_OPERACION. Returns content.

##### get_valores_hijos(var_id, val_id, detail_level)

> Process for VALORES_HIJOS. Returns content.

##### get_unidades()

> Process for UNIDADES. Returns content.

##### get_unidad(unit_id)

> Process for UNIDAD. Returns content.

##### get_escalas(tipology)

> Process for ESCALAS. Returns content.

##### get_escala(scale_id, tipology)

> Process for ESCALA. Returns content.

##### get_periodo(period_id)

> Process for PERIODO. Returns content.


#### EasyINEAPIClientSync, EasyINEAPIClientAsync

> Same class as INEAPI but with additional methods for easier usage.

##### get_operations_(op_id, detail_level, geographical_level, extra_op, page, tipology)

> Returns the data of all operations, or the specified one.

if extra_op param is set, performs the requests that returns some
additional operaciones.

If you specify the op_id it will return the specified operation.

##### get_variables_(op_id, var_id, page)

> Returns the available variables.

If the operation is specified, it returns the variables asociated with
that operation.

If a variable is specified, it returns the data for such variable.

If no param is specified it returns all the available variables.

##### get_values_(var_id, classification_id, op_id, val_id, detail_level)

> Returns the available values for the specified variable.

The variable must be specified.

Additionally one may want the values for a specific variable and
a specific operation, this can be achieved by providing the op_id param

If you just want to get the sons of a specific value from a specific
variable you must specify the val_id. In this case,
the op_id is ignored.

Getting the values return a list of dictionaries. The shape of it
depends on the detail_level

##### get_tables_(op_id, tab_id, group_id, detail_level, geographical_level, tipology)

> Returns different data depending on input options.

If operation is provided it returns the available tables for that
operation. The resulting data will depend on the params provided.

If only the table is provided it will return the available groups for
such table.

If table and group is provided it will return the available values
for such group.

##### get_series_(serie_id, op_id, tab_id, serie_data, operation_data, detail_level, tipology, page, metadata_filtering)

> Returns the available information for the series.

This function is a little more complex than the previous one, but
splitting this function in two may reduce readability.

serie_id param must be a serie of which you want the data from,
you may ask metadata or values for the serie specifying
the serie_data param

op_id is the operation of which you want the data from,
you may ask for series or metadata by specifying the
operation_data param

tab_id is the table of which you want the data from, this param will
return only the series inside the specified table.

##### get_publications_(op_id, publication_id, detail_level, tipology)

> Returns the available publications.

If no input is provided returns the available publications.

If one operation is provided it returns the available publications
related to such operation.

If some publication is provided then it returns the publication dates
for such publication.

##### get_data_(serie_id, tab_id, op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)

> Returns the published data from series.

if serie is provided it returns the data for such serie.
if table, it returns all the series and their data of such table
    can provide metadata filtering.
if operation, metadata_filtering must be provided and returns all the
data of series that belong to such operation and such
metadata filtering.

##### get_units_(unit_id)

> Returns all the units or the data of the specified unit.

##### get_scales_(scale_id, tipology)

> Return all the scales or the data of the specified scale.

##### get_periods_(period_id)

> Returns the data of the specified period. Same as get_periodo().

##### get_periodicities_(periodicity_id)

> Returns the peridocities.

If no periodicity is specified it returns all of them.

If it is specified it returns the data for the specified one.

##### get_classifications_(op_id)

> Returns classifications.

Related to operation if op_id is provided.

All otherwise.


### INE_functions
<details>
    <summary>INE_functions Module</summary>
    
    Este módulo contiene las mismas funciones que el INE adaptadas a este paquete y en minúsculas. Todas estas funciones devuelven la URL necesaria para hacer la petición.
    
</details>

### def datos_tabla(tab_id, detail_level, tipology, count, list_of_dates, metadata_filtering)

> Function DATOS_TABLA from INE. Returns the URL to make the request.


### def datos_serie(serie_id, detail_level, tipology, count, list_of_dates)

> Function DATOS_SERIE from INE. Returns the URL to make the request.


### def datos_metadataoperacion(op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)

> Function DATOS_METADATAOPERACION from INE.

Returns the URL to make the request.


### def operaciones_disponibles(detail_level, geographical_level, page, tipology)

> Function OPERACIONES_DISPONIBLES from INE.

Returns the URL to make the request.

page>1 doesn't returns anything. No more than 500 Operaciones.


### def operaciones(detail_level, page, tipology)

> Function OPERACIONES from INE.

Returns the URL to make the request.

page>1 doesn't returns anything. No more than 500 Operaciones.

Not in the official documentation, adds some Operations.


### def operacion(op_id, detail_level, tipology)

> Function OPERACION from INE. Returns the URL to make the request.


### def variables(page)

> Function VARIABLES from INE. Returns the URL to make the request.


### def variable(var_id)

> Function VARIABLE from INE. Returns the URL to make the request.

Not documented in the official page.


### def variables_operacion(op_id, page)

> Function VARIABLES_OPERACION from INE.

Returns the URL to make the request.


### def valores_variable(var_id, detail_level, classification_id)

> Function VALORES_VARIABLE from INE.

Returns the URL to make the request.


### def valores_variableoperacion(var_id, op_id, detail_level)

> Function VALORES_VARIABLEOPERACION from INE.

Returns the URL to make the request.


### def tablas_operacion(op_id, detail_level, geographical_level, tipology)

> Function TABLAS_OPERACION from INE.

Returns the URL to make the request.


### def grupos_tabla(tab_id)

> Function GRUPOS_TABLA from INE.

Returns the URL to make the request.


### def valores_grupostabla(tab_id, group_id, detail_level)

> Function VALORES_GRUPOSTABLA from INE.

Returns the URL to make the request.


### def serie(serie_id, detail_level, tipology)

> Function SERIE from INE.

Returns the URL to make the request.


### def series_operacion(op_id, detail_level, tipology, page)

> Function SERIES_OPERACION from INE.

Returns the URL to make the request.


### def valores_serie(serie_id, detail_level)

> Function VALORES_SERIE from INE.

Returns the URL to make the request.


### def series_tabla(tab_id, detail_level, tipology, metadata_filtering)

> Function SERIES_TABLA from INE.

Returns the URL to make the request.


### def serie_metadataoperacion(op_id, detail_level, tipology, metadata_filtering)

> Function SERIE_METADATAOPERACION from INE.

Returns the URL to make the request.


### def periodicidades()

> Function PERIODICIDADES from INE.

Returns the URL to make the request.


### def periodicidad(periodicity_id)

> Function PERIODICIDAD from INE.

Returns the URL to make the request.

Not in the official documentation.


### def publicaciones(detail_level, tipology)

> Function PUBLICACIONES from INE.

Returns the URL to make the request.


### def publicaciones_operacion(op_id, detail_level, tipology)

> Function PUBLICACIONES_OPERACION from INE.

Returns the URL to make the request.


### def publicacionfecha_publicacion(publication_id, detail_level, tipology)

> Function PUBLICACIONFECHA_PUBLICACION from INE.

Returns the URL to make the request.


### def clasificaciones()

> Function CLASIFICACIONES from INE.

Returns the URL to make the request.


### def clasificaciones_operacion(op_id)

> Function CLASIFICACIONES_OPERACION from INE.

Returns the URL to make the request.


### def valores_hijos(var_id, val_id, detail_level)

> Function VALORES_HIJOS from INE.

Returns the URL to make the request.


### def unidades()

> Function UNIDADES from INE.

Returns the URL to make the request.

Not in the official documentation.


### def unidad(unit_id)

> Function UNIDAD from INE.

Returns the URL to make the request.

Not in the official documentation.


### def escalas(tipology)

> Function ESCALAS from INE.

Returns the URL to make the request.

Not in the official documentation.


### def escala(scale_id, tipology)

> Function ESCALA from INE.

Returns the URL to make the request.

Not in the official documentation.


### def periodo(period_id)

> Function PERIODO from INE.

Returns the URL to make the request.

Not in the official documentation.
