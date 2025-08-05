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
    
    <details>
        <summary>INEAPIClientSync, INEAPIClientAsync</summary>
        <details>
            <summary>close_all_sessions</summary>
            
            Este método permite cerrar todas las sesiones del Gestor de Sesiones. En otras palabras, permite terminar las conexiones a la API.
        </details>
        <details>
            <summary>get_datos_tabla</summary>
            <ul>
                <li>tab_id: Obligatorio</li>
                <li>detail_level</li>
                <li>tipology</li>
                <li>count</li>
                <li>list_of_dates</li>
                <li>metadata_filtering</li>
            </ul>
        </details>
        <details>
            <summary>get_datos_serie</summary>
            <ul>
                <li>tab_id: Obligatorio</li>
                <li>detail_level</li>
                <li>tipology</li>
                <li>count</li>
                <li>list_of_dates</li>
                <li>metadata_filtering</li>
            </ul>
        </details>
    </details>
    <details>
        <summary>EasyINEAPIClientSync, EasyINEAPIClientAsync</summary>
    </details>
</details>


### INE_functions
<details>
    <summary>INE_functions Module</summary>
    
</details>
