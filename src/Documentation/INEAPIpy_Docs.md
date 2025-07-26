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

