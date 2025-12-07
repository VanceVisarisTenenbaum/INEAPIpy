# Notas para el diseño de la página

En este archivo se encuentran una serie de apuntes que buscan preparar con cierta antelacioń el diseño de la aplicación web.

## ¿Cuál es el objetivo de la app?

El objetivo de la app es permitir el uso de la API del INE.

Dado que la API del INE, tiene como objetivo final, proporcionar acceso a un conjunto de series temporales. Entonces, el objetivo final de esta app es el de permitir de forma cómoda la visualización de dichas series temporales.

### ¿Qué resuelve la app?

Por un lado, una forma visual de utilizar las funciones de la API del INE sin necesidad de conocer la API y facilitando la visualización de todos los datos y por otro lado, permitir mostrar varias series temporales de manera sencilla.

## ¿Qué se puede cargar con antelación?

Con esta pregunta buscamos minimizar el uso de la API de INE, cargando en memoria lo que sea posible, para leer directamente de la memoria y evitar utilizar la API del INE.

Se pueden obtener todos los valores posibles de lo siguiente:

* ```Operaciones```.
* ```Variables```, se ***descarta*** por tener demasiados valores posibles.
* ```Publicaciones```.
* ```Unidades```.
* ```Escalas```.
* ```Clasificaciones```.

## ¿Qué función cumple cada objeto de la API del INE dentro del objetivo de la app?

En términos de objetos del INE, el objetivo final es el de obtener una o varias series temporales (y sus datos). Es decir, el objeto final es una ```Serie```.

Según el objetivo, podemos clasificar los objetos en las siguientes categorías:

* **Requerido**. Es decir, necesario para obtener al menos una ```Serie```.
* **Filtro**. Es decir, actúa como filtro para reducir el número de ```Series``` que se pueden obtener.
* **Alternativa**. Es decir, que es requerida para obtener la serie, pero deja de ser obligatoria si se proporciona otro u otros objetos.
* **Propiedad**. Es decir, es actúa como pieza informativa sobre otro objeto.
* **Serie**. Una serie, haciendo referencia tanto a sus propiedades como sus datos.

Los diferentes objetos y sus clasificaciones son:

* ```Operación```: Requerido.
    * Sólo con la operación ya se pueden obtener las series, pero es muy recomendable utilizar filtros por qué se obtienen demasiadas series.
* ```Tabla```: Alternativa.
    * Sólo con esto ya se pueden obtener series.
* ```Variable```: Filtro.
* ```Valor```: Filtro.
    * Este actúa tanto como filtro de series en conjunto con la ```Variable```, pero es necesario tener en cuenta que los valores se obtienen a partir de la variable.
* ```Serie```: Serie.
* ```Publicación```: Filtro y Propiedad.
* ```Fecha Publicación```: Propiedad.
* ```Unidad```: Propiedad.
* ```Escala```: Propiedad.
* ```Periodo```: Propiedad.
* ```Periodicidad```: Propiedad.
* ```Clasificación```: Filtro y Propiedad.
    * No actúa directamente como filtro de ```Series``` pero si como filtro de ```Valores```.
* ```GrupoTablas```: Propiedad.


## ¿Cuáles son las dependencias y propiedades de los objetos de INE?

Al formular esta pregunta buscamos, por un lado, saber las relaciones entre las distintas entidades del INE y ver qué objetos se repiten y cuántas veces, de este modo, poder optimizar la información que se visualiza en la app y en qué orden se van a mostrar. Por un lado, podemos recurrir al [diagrama de la documentación](https://mermaid.live/view?gist=https://gist.github.com/VanceVisarisTenenbaum/ccafa1dfdc5541dc9e343d81e10b3a76) o bien al [diagram simplificado](INSERTAR ENLACE CUANDO ESTÉ) que responde a esta pregunta. En cualquier caso, se tiene en forma de texto los objetos de los que depende para su obtención y los objetos que tiene como propiedad:

* ```Operación```:
    * Dependencias:
    * Propiedades:
* ```Tabla```:
    * Dependencias:
        * ```Operación```
    * Propiedades:
        * ```Periodo```
        * ```Periodicidad```
        * ```Publicación```
        * ```GrupoTablas```
* ```Variable```:
    * Dependencias:
        * ```Operación```: Opcional, pero muy recomendable.
    * Propiedades:
* ```Valor```:
    * Dependencias:
        * ```Variable```
    * Propiedades:
        * ```Valor```
* ```Serie```:
    * Dependencias:
        * ```Operación```: No recomendable usar solo esto.
            * ```Variable```
                * ```Valor```
        * ```Tabla```
    * Propiedades:
        * ```Clasificación```
        * ```Periodicidad```
        * ```Publicación```
        * ```Unidad```
        * ```Escala```
* ```Publicación```:
    * Dependencias:
        * ```Operación```
    * Propiedades:
* ```Fecha Publicación```:
    * Dependencias:
        * ```Publicación```
    * Propiedades:
* ```Unidad```:
    * Dependencias:
    * Propiedades:
* ```Escala```:
    * Dependencias:
    * Propiedades:
* ```Periodo```:
    * Dependencias:
    * Propiedades:
* ```Periodicidad```:
    * Dependencias:
    * Propiedades:
* ```Clasificación```:
    * Dependencias:
        * ```Operación```
    * Propiedades:
* ```GrupoTablas```:
    * Dependencias:
        * ```Tabla```
    * Propiedades:

    
Con el objetivo de evitar redondancia en la información que se muestra, analizamos qué se repite:

* ```Operación``` es una dependencia común a cinco objetos ```Serie```, ```Tabla```, ```Clasificación```, ```Publicación``` y ```Variable```.
* ```Publicación``` y ```Periodicidad``` es una propiedad común a ```Tabla``` y ```Serie```.
* ```Periodicidad``` es además común también a ```Publicación``` y ```Periodo```.

Teniendo esto en cuenta, es necesario responder a las siguientes preguntas.
* ¿Las ```Publicaciones``` y ```Periodicidades``` asociadas a una tabla son las mismas que las asociadas a la ```Serie```? Sí, por que realmente, las ```Series``` están contenidas en una ```Tabla```.


## ¿Cómo afecta que los valores tengan valores hijos a la obtención de Series?

El objetivo de esta pregunta radica en comprender cómo funciona el filtrado mediante variable-valor, ya que algunos pares excluyen a los otros.

Antes que nada, es necesario comprender qué son las variables y los valores. Según la [documentación](https://www.ine.es/dyngs/DAB/index.htm?cid=1105):

* Una variable es una característica que puede fluctuar y cuya variación es susceptible de adoptar diferentes valores.
* Los valores son los estados que puede presentar una variable determinada. Por ejemplo, la variable Provincias contiene los valores: Áraba/Álava, Albacete...

Con esta definición y el ejemplo dado, no es necesaria más explicación. Pero si es necesario aclarar qué son los valores hijos. Algunas variables se organizan en forma de árbol, como es el caso de las variables, Comunidad Autónoma y Provincia, Provincia es "hija" de Comunidad Autónoma, por lo que los valores hijos hacen referencia a los valores que derivan de dicho valor. Por ejemplo, un valor de la variable Comunidad Autónoma sería Andalucía, por lo que los hijos de Andalucía serán, Granada, Málaga, etc.

Si bien en este caso de ejemplo, la jerarquía parece estar relacionada a través de la variable, la relación padre-hijo no siempre ocurre, por ejemplo, los valores padre de Andalucía sería Total nacional o total capitales de provincia.

Para responder a esta pregunta entonces es necesario comprender como funciona el filtrado variable-valor en la API del INE, necesitamos entender si añadir varias ```Variables``` y/o ```Valores``` implican un filtrado excluyente (AND) o inclusivo (OR), es decir, si al utilizar la ```Variable``` Comunidad Autónoma y los ```Valores``` Andalucía y Baleares, implica un filtrado OR o AND, es decir, si busca ```Series``` que cumplan ambas condiciones a la vez, o si cumplen al menos una de las dos. Y hay que realizar la misma comprobación al utilizar más de una ```Variable```.

* ¿Para una única ```Variable``` y varios ```Valores```, el filtrado de ```Series``` es OR o AND?
    * Respuesta: AND
    * Prueba: El [primer caso](https://servicios.ine.es/wstempus/js/ES/SERIE_METADATAOPERACION/132?det=0&tip=&g1=70%3A9002&g2=70%3A9002) devuelve resultados y el [segundo caso](https://servicios.ine.es/wstempus/js/ES/SERIE_METADATAOPERACION/132?det=0&tip=&g1=70%3A9002&g2=70%3A8995) no.
* ¿Para varias ```Variables``` no relacionadas, el filtrado de ```Series``` es OR o AND?
    * Respuesta: AND
    * Prueba: El número de resultados para [este caso](https://servicios.ine.es/wstempus/js/ES/SERIE_METADATAOPERACION/132?det=0&tip=&g1=70%3A9002&g2=94%3A9834) es menor que el anterior.
* ¿Para varias ```Variables``` relacionadas a través de los ```Valores```, el filtrado de ```Series``` es OR o AND?
    * Respuesta: AND
    * Prueba: [Este caso](https://servicios.ine.es/wstempus/js/ES/SERIE_METADATAOPERACION/132?det=0&tip=&g1=70%3A9002&g2=349%3A16473) no devuelve resultados.
    
Habría que comprobarlo pero asumimos que es lo mismo para el caso en el que se filtra mediante ```Tabla``` y pares ```Variable-Valor```.


## ¿Cómo diseñaremos el flujo de uso de la app?

El flujo de uso será el siguiente:

1. Se selecciona la ```Operación```.
    * Opcionalmente se selecciona la ```Clasificación```.
    * Opcionalmente se selecciona la ```Publicación```.
2. Se selecciona la ```Tabla```. O se selecciona los pares ```Variable-Valor```.
    * O ambos. Pero al menos uno de los dos que sea obligatorio.
3. Se seleccionan las ```Series```.

Se debe mostrar toda la información disponible:

* ```Operaciones```.
    * **Formato**: ID - Nombre
    * Información adicional:
        * URL
    * ```Clasificaciones``` disponibles.
        **Formato**: Nombre
        Información adicional:
            * Fecha.
    * ```Publicaciones``` disponibles.
        * **Formato**: Fecha - Nombre
        * Información adicional:
            * ```Periodicidad```.
                **Formato**: Nombre
    * **Nota**: Las operaciones se dividen en dos grupos territoriales según la [documentación](https://www.ine.es/dyngs/DAB/index.htm?cid=1100). Igual conviene hacer esta separación en la app.
* ```Tabla```.
    * **Formato**: ID - Nombre
    * Información adicional:
        * ```Periodicidad```
        * ```Periodo_ini```
        * ```GrupoTabla```
            * **Formato**: Nombre
* ```Serie```.
    * **Formato**: ID - Nombre
    * Información adicional:
        * ```Escala```
        * ```Unidad```
        * ```Publicación```
        * ```Clasificación```
        * Notas: Se obtiene a partir de DatosSerie.

        
## Ideas de características

* Se pueden elegir varias operaciones.
* Se pueden generar varias gráficas.
* Se puede elegir en qué gráfica se van a representar los datos.
    * Se puede elegir el eje.

## Ideas de diseño.

* La selección de operación se divide en dos grupos según el marco geográfico.
* Junto a la selección de operación, opcionalmente se selecciona:
    * La clasificación.
    * La publicación.
* Opcionalmente se selecciona la tabla.
* Opcionalmente se seleccionan los pares variable-valor.
* Se seleccionan las series.
    * Las series se agrupan según la publicación o según la clasificación.
    * Se selecciona en qué gráfica y eje se representan.
* Se muestran las gráficas.






