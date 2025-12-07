# INEAPIpy

Este paquete de Python actua como Wrapper de la [API del INE](https://www.ine.es/dyngs/DAB/index.htm?cid=1099), permitiendo realizar peticiones utilizando una interfaz de Python.

## Instalación

```py
pip install ineapipy
```

## Guía de inicio

```py
from INEAPIpy import Wrapper as W

INE = W.INEAPIClientSync()

# Primera función de https://ine.es/dyngs/DAB/index.htm?cid=1100
# Y primer ejemplo
print(INE.get_datos_tabla(50902))
```

## Anotación

Existe un paquete con la misma funcionalidad aunque organizado y estructurado de otra manera. Sin embargo, este paquete fue desarrollado de forma independiente y no existe ninguna relación entre los dos desarrolladores.

Dicho paquete es [ineapy](https://github.com/Angel-RC/ineapy)

También existe el paquete [inejsonstat](https://github.com/Mlgpigeon/inejsonstat) con la misma funcionalidad, pero la última actualización fue hace 3 años.


## Documentación

Toda la documentación se encuentra en este enlace.

https://github.com/VanceVisarisTenenbaum/INEAPIpy/tree/main/INEAPIpy/Documentation

Los diagramas o archivos .mmd son diagramas de mermaid y es recomendable utilizar la [app oficial](https://mermaid.live/) para visualizarlos de la mejor manera posible.

Los diagrams muestran un diagrama por defecto antes de cargar el real, tarda unos 15 segundos en cargar el real.

* [Referencia API Python](https://github.com/VanceVisarisTenenbaum/INEAPIpy/blob/main/INEAPIpy/Documentation/INEAPIpy_Docs.md).
    * [Diagrama API Python](https://mermaid.live/view?gist=https://gist.github.com/VanceVisarisTenenbaum/5b2890f4ccc5517ba9289c5c271af1fa)(Tarda unos 15 segundos en cargar el real).
* [Referencia API INE](https://github.com/VanceVisarisTenenbaum/INEAPIpy/blob/main/INEAPIpy/Documentation/INEAPI_Docs.md).
    * [Diagrama Modelos y Relaciones](https://mermaid.live/view?gist=https://gist.github.com/VanceVisarisTenenbaum/ccafa1dfdc5541dc9e343d81e10b3a76)(Tarda unos 15 segundos en cargar el real).


