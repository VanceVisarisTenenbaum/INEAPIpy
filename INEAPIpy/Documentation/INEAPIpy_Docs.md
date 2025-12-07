# INEAPIpy

Este paquete de Python actúa como Wrapper para la API del INE. Este proporciona funciones para realizar peticiones y obtener los resultados del INE.


## Inputs

Antes de definir las funciones, es necesario conocer los inputs que los conforman.

* Indetificadores de Objetos
    * ```op_id```: Identificador de **Operación**.
    * ```var_id```: Identificador de **Variable**.
    * ```val_id```: Identificador de **Valor**.
    * ```tab_id```: Identificador de **Tabla**.
    * ```group_id```: Identificador de **Grupo de Tablas**.
    * ```serie_id```: Identificador de **Serie**.
    * ```unit_id```: Identificador de **Unidad**.
    * ```scale_id```: Identificador de **Escala**.
    * ```period_id```: Identificador de **Periodo**.
    * ```periodicity_id```: Identificador de **Periodicidad**.
    * ```classification_id```: Identificador de **Clasificación**.
    * ```publication_id```: Identificador de **Publicación**.
* Parámetros de configuración de respuesta:
    * ```detail_level```: Nivel de detalle.
    * ```tipology```: Tipo o mode de representación de respuesta.
* Parámetros de filtrado:
    * ```geographical_level```: Selección de datos geográficos.
    * ```metadata_filtering```: Parámetros de filtrado por pares variable-valor.
    * ```list_of_dates```: Lista de fechas a filtrar.
    * ```count```: Número de resultados a mostrar (Datos).
    * ```page```: Página de resultados (Metadatos).

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


### ```metadata_filtering``` Input.

Para el filtrado mediante pares variable valor se utiliza este input ***metadata_filtering***. Este input se construye con la siguiente estructura:
```
{
    var_id_1: [val_id_1, ..., val_id_i],
    var_id_2: [val_id_1, ..., val_id_j],

    var_id_n: [val_id_1, ..., val_id_k],
    periodicidad: periodicity_id
}
```

Dónde, ```var_id``` representa la variable y ```val_id``` el valor asociado a dicha variable. Mientra que ```pub_id``` es el identificador de publicación. Todos son opcionales, aunque depende de la petición del INE. Ejemplo:

```
# Supón que hacemos la consulta https://servicios.ine.es/wstempus/js/ES/SERIE_METADATAOPERACION/IPC?g1=115:29&g2=3:84&g3=762:&p=1&det=2&tip=A

# En este caso, metadata_filtering sería:

metadata_filtering = {
    115: [29],
    3: [84],
    762: [],
    "publicacion": 1
}
```

### ```list_of_dates``` Input

Este filtro se utiliza en la selección de datos y permite seleccionar fechas concretas, y/o rangos de fechas. El input se construye de la siguiente manera:

```
[date, (date, None), (None, date), (date, date)]
```

Dónde ***date*** se construye con el siguiente formato: "YYYY-MM-DD" y un valor solo representa una fecha única, y el rango se construye con una tupla de dos ***fechas*** o una ***fecha*** y un ***None***, siendo el ***None*** la carencia de límite. Ejemplos:

```
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

### Wrapper

Este paquete proporciona cuatro clases para realizar las peticiones al INE. Las dos primeras proprocionan exactamente los mismos métodos, sin embargo, el primero es Síncrono y el segundo Asíncrono. Las dos clases siguientes extienden la funcionalidad de las dos primeras proporcionando varios métodos adicionales para realizar las mismas peticiones de la primera clase, pero utilizando una estructura diferente.

Todas las clases utilizan un objeto RequestManager, que se encarga de realizar las peticiones sin necesidad de iniciar tu propia instancia de Sesión y la cierra si tras cierto tiempo no se realizan peticiones.

Si no quieres que existan estos procesos, puedes usar el módulo INE_functions, cuyas funciones sólo devuelven las urls.


#### ```INEAPIClientSync```, ```INEAPIClientAsync```

> Wrapper de la api del INE, realiza las peticiones de manera sincrona o asincrona según la clase elegida.

Todos los métodos devuelven los resultados del INE y se pueden visualizar mejor en el [diagrama](https://mermaid.live/view?gist=https://gist.github.com/VanceVisarisTenenbaum/5b2890f4ccc5517ba9289c5c271af1fa)

##### __init__(mode, RM, sleep_time, print_url)

> Init of class.

* ```Mode```: Literal['raw', 'py', 'pydantic'] el modo de la clase.
    * ```raw```: Devuelve los resultados como un string directamente de la API del INE.
    * ```py```: Devuelve los resultados como un diccionario o como una lista.
    * ```pydantic```: Devuelve los resultados como un objeto de pydantic y comprueba que son correctos.
* ```RM```: Instancia de RequestsManagement.RequestManager en caso de ya tener una. Si no sabes lo que es es un objeto para manejar sesiones de forma automática del submodulo. Se inicia solo si no lo especifícas.
* ```sleep_time```: Cuanto tiempo debe esperar entre peticiones.
* ```print_url```: Establece esta opción como True si quieres imprimir la url después de cada petición.

##### Métodos de las clases.

* ```close_all_sessions()```: Cierra todas las sesiones del gestor de peticiones. Se cierra sola después de cierto tiempo, o cuando se cierra el kernel de Python.
* ```__get_data(url)```: Simplifica el proceso de obtener los datos.

Todos los métodos siguientes siguen la conveción ***get_NombreFuncionIneEnMinusculas*** y obtienen los resultados especificados en su [documentación](https://ine.es/dyngs/DAB/index.htm?cid=1100).

* ```get_datos_tabla(tab_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```get_datos_serie(serie_id, detail_level, tipology, count, list_of_dates)```
* ```get_datos_metadataoperacion(op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```get_operaciones_disponibles(detail_level, geographical_level, page, tipology)```
* ```get_operaciones(detail_level, page, tipology)```
* ```get_operacion(op_id, detail_level, tipology)```
* ```get_variables(page)```
* ```get_variable(var_id)```
* ```get_variables_operacion(op_id, page)```
* ```get_valores_variable(var_id, detail_level, classification_id)```
* ```get_valores_variableoperacion(var_id, op_id, detail_level)```
* ```get_tablas_operacion(op_id, detail_level, geographical_level, tipology)```
* ```get_grupos_tabla(tab_id)```
* ```get_valores_grupostabla(tab_id, group_id, detail_level)```
* ```get_serie(serie_id, detail_level, tipology)```
* ```get_series_operacion(op_id, detail_level, tipology, page)```
* ```get_valores_serie(serie_id, detail_level)```
* ```get_series_tabla(tab_id, detail_level, tipology, metadata_filtering)```
* ```get_serie_metadataoperacion(op_id, detail_level, tipology, metadata_filtering)```
* ```get_periodicidades()```
* ```get_periodicidad(periodicity_id)```
* ```get_publicaciones(detail_level, tipology)```
* ```get_publicaciones_operacion(op_id, detail_level, tipology)```
* ```get_publicacionfecha_publicacion(publication_id, detail_level, tipology)```
* ```get_clasificaciones()```
* ```get_clasificaciones_operacion(op_id)```
* ```get_valores_hijos(var_id, val_id, detail_level)```
* ```get_unidades()```
* ```get_unidad(unit_id)```
* ```get_escalas(tipology)```
* ```get_escala(scale_id, tipology)```
* ```get_periodo(period_id)```


#### ```EasyINEAPIClientSync```, ```EasyINEAPIClientAsync```

Es la misma clase que las anteriores, pero añade varios métodos que simplifican las peticiones. Todos los resultados se pueden ver de manera visual en el [diagrama](https://mermaid.live/view?gist=https://gist.github.com/VanceVisarisTenenbaum/5b2890f4ccc5517ba9289c5c271af1fa).

##### Métodos adicionales.

* ```get_operations_(op_id, detail_level, geographical_level, extra_op, page, tipology)```: Devuelve los datos de todas las operaciones o las especificadas.
    * Si ```extra_op=True```, realiza una petición que devuelve algunas operaciones extra.
    * Si se especifica ```op_id```, devuelve la operación especificada.
* ```get_variables_(op_id, var_id, page)```: Devuelve las variables disponibles.
    * Si se especifica ```op_id```, devuelve las variables asociadas a dicha operación.
    * Si se especifica ```var_id```, devuelve dicha variable.
    * Si no se especifica ningún parámetro, devuelve todas las variables disponibles.
* ```get_values_(var_id, classification_id, op_id, val_id, serie_id, tab_id, group_id, detail_level)```: Devuelve los valores asociados según las inputs.
    * Si se especifiva ```var_id```, devuelve los valores asociados a dicha variable.
        * Se puede filtrar además especificando ```classification_id```.
    * Si se especifica ```var_id``` y ```op_id```, devuelve los valores asociados a dicha variable y dicha operación.
    * Si se especifica ```var_id``` y ```val_id```, devuelve los valores hijos dicho valor.
    * Si se especifica ```serie_id```, devuelve los valores asociados a dicha serie.
    * Si se especifica ```tab_id``` y ```group_id```, devuelve los valores asociados a dicho grupo de tablas.
* ```get_tables_(op_id, tab_id, detail_level, geographical_level, tipology)```: Devuelve las tablas, grupos de tabla o valores según el input.
    * Si se especifica ```op_id```, devuelve las tablas asociadas a dicha operación.
    * Si se especifica ```tab_id```, devuelve los grupos de tabla disponibles para dicha tabla.
* ```get_series_(serie_id, op_id, tab_id, detail_level, tipology, page, metadata_filtering)```: Devuelve la información disponible de las series.
    * Si se especifica ```serie_id```, devuelve los datos de dicha serie.
    * Si se especifica ```op_id```, devuelve las series asociadas a dicha operación.
        * Se puede filtrar utilizando ```metadata_filtering```.
    * Si se especifica ```tab_id```, devuelve las series asociadas s dicha tabla.
        * Se puede filtrar utilizando ```metadata_filtering```.
* ```get_publications_(op_id, publication_id, detail_level, tipology)```: Devuelve las publicaciones disponibles.
    * Si no se especifica ningún input, devuelve todas las publicaciones.
    * Si se especifica ```op_id```, devuelve las publicacionesa asociadas a dicha operación.
    * Si se especifica ```publication_id```, devuelve las fechas de publicación asociadas a dicha publicación.
* ```get_data_(serie_id, tab_id, op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```: Devuelve los datos de las series.
    * Si se especifica ```serie_id```, devuelve los datos asociados a dicha serie.
    * Si se especifica ```tab_id```, devuelve todas las series con sus datos asociados a dicha tabla. Se puede aplicar ```metadata_filtering```
    * Si se especifica ```op_id```, se tiene que especificar ```metadata_filtering``` y devuelve todas las series con sus datos asociados a dicha operación y dichos filtros.
* ```get_units_(unit_id)```: Devuelve las unidades.
    * Si se especifica ```unit_id```, devuelve dicha unidad.
    * Si no se especifica nada, devuelve todas las unidades.
* ```get_scales_(scale_id, tipology)```: Devuelve las escalas.
    * Si se especifica ```scale_id```, devuelve dicha escala.
    * Si no se especifica nada, devuelve todas las escalas.
* ```get_periods_(period_id)```: Devuelve el periodo especificado.
* ```get_periodicities_(periodicity_id)```: Devuelve las periodicidades.
    * Si no se especifica la periodicidad, devuelve todas las periodicidades.
    * Si se especifica ```periodicity_id```, devuelve la periodicidad especificada.
* ```get_classifications_(op_id)```: Devuelve las clasificaciones.
    * Si no se especifica nada, devuelve todas las clasificaciones.
    * Si se especifica ```op_id```, devuelve las clasificaciones asociadas a dicha operación.


### INE_functions

Este módulo contiene las mismas funciones que el INE adaptadas a este paquete y en minúsculas. Todas estas funciones devuelven la URL necesaria para hacer la petición.

* ```datos_tabla(tab_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```datos_serie(serie_id, detail_level, tipology, count, list_of_dates)```
* ```datos_metadataoperacion(op_id, detail_level, tipology, count, list_of_dates, metadata_filtering)```
* ```operaciones_disponibles(detail_level, geographical_level, page, tipology)```: No hay más de 500 operaciones asi que page>1 no devuelve nada.
* ```operaciones(detail_level, page, tipology)```: Añade algunas operaciones. No está en la documentación oficial.
* ```operacion(op_id, detail_level, tipology)```
* ```variables(page)```
* ```variable(var_id)```: No está documentada oficialmente.
* ```variables_operacion(op_id, page)```
* ```valores_variable(var_id, detail_level, classification_id)```
* ```valores_variableoperacion(var_id, op_id, detail_level)```
* ```tablas_operacion(op_id, detail_level, geographical_level, tipology)```
* ```grupos_tabla(tab_id)```
* ```valores_grupostabla(tab_id, group_id, detail_level)```
* ```serie(serie_id, detail_level, tipology)```
* ```series_operacion(op_id, detail_level, tipology, page)```
* ```valores_serie(serie_id, detail_level)```
* ```series_tabla(tab_id, detail_level, tipology, metadata_filtering)```
* ```serie_metadataoperacion(op_id, detail_level, tipology, metadata_filtering)```
* ```periodicidades()```
* ```periodicidad(periodicity_id)```: No está documentada oficialmente.
* ```publicaciones(detail_level, tipology)```
* ```publicaciones_operacion(op_id, detail_level, tipology)```
* ```publicacionfecha_publicacion(publication_id, detail_level, tipology)```
* ```clasificaciones()```
* ```clasificaciones_operacion(op_id)```
* ```valores_hijos(var_id, val_id, detail_level)```
* ```unidades()```: No está documentada oficialmente.
* ```unidad(unit_id)```: No está documentada oficialmente.
* ```escalas(tipology)```: No está documentada oficialmente.
* ```escala(scale_id, tipology)```: No está documentada oficialmente.
* ```periodo(period_id)```: No está documentada oficialmente.
