# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:46:00 2025

@author: mano

This file contains all the functions from the INE as they are, but instead
of returning the result from the input, they build the corresponding url.

They are all described here: https://www.ine.es/dyngs/DAB/index.htm?cid=1100

All params are assumed to be known, so this functions have minimum docs.
"""

from . import INE_Filtering as filtering
from . import INE_URL_Treatment as INEURL
from .Models import FunctionInputsModels as FIM
from pydantic import validate_call
import warnings


@validate_call
def datos_tabla(tab_id: int | str,
                detail_level: int = 0,
                tipology: str = '',
                count: int | None = None,
                list_of_dates=None,
                metadata_filtering=dict()
                ):
    """Function DATOS_TABLA from INE. Returns the URL to make the request."""
    Inputs = FIM.InputParams(
        tab_id=tab_id,
        detail_level=detail_level,
        tipology=tipology,
    )

    filter_params = filtering.metadata_and_date_filtering(
        var_value_dict=metadata_filtering,
        format_='series',
        list_of_dates=list_of_dates,
        count=count
    )

    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen('DATOS_TABLA', Inputs.tab_id, **query)
    return URL


@validate_call
def datos_serie(serie_id: int | str,
                detail_level: int = 0,
                tipology: str = '',
                count: int | None = None,
                list_of_dates=None
                ):
    """Function DATOS_SERIE from INE. Returns the URL to make the request."""
    Inputs = FIM.InputParams(
        serie_id=serie_id,
        detail_level=detail_level,
        tipology=tipology,
    )

    filter_params = filtering.date_count_selection_params_builder(
        list_of_dates=list_of_dates,
        count=count
    )

    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen('DATOS_SERIE', Inputs.serie_id, **query)
    return URL


@validate_call
def datos_metadataoperacion(op_id: int | str,
                            detail_level: int = 0,
                            tipology: str = '',
                            count: int | None = None,
                            list_of_dates=None,
                            metadata_filtering=dict()
                            ):
    """
    Function DATOS_METADATAOPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        op_id=op_id,
        detail_level=detail_level,
        tipology=tipology,
    )

    filter_params = filtering.metadata_and_date_filtering(
        var_value_dict=metadata_filtering,
        format_='metadata',
        list_of_dates=list_of_dates,
        count=count
    )

    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen('DATOS_METADATAOPERACION', Inputs.op_id, **query)
    return URL


@validate_call
def operaciones_disponibles(detail_level: int = 0,
                            geographical_level: int | None = None,
                            page: int = 1,
                            tipology: str = ''
                            ):
    """
    Function OPERACIONES_DISPONIBLES from INE.

    Returns the URL to make the request.

    page>1 doesn't returns anything. No more than 500 Operaciones.
    """
    Inputs = FIM.InputParams(
        detail_level=detail_level,
        geographical_level=geographical_level,
    )

    filter_params = filtering.date_count_selection_params_builder(
        page=page
    )

    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen('OPERACIONES_DISPONIBLES', **query)
    return URL


@validate_call
def operaciones(detail_level: int = 0,
                page: int = 1,
                tipology: str = ''
                ):
    """
    Function OPERACIONES from INE.

    Returns the URL to make the request.

    page>1 doesn't returns anything. No more than 500 Operaciones.

    Not in the official documentation, adds some Operations.
    """
    Inputs = FIM.InputParams(
        detail_level=detail_level,
    )

    filter_params = filtering.date_count_selection_params_builder(
        page=page
    )

    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen('OPERACIONES', **query)
    return URL


@validate_call
def operacion(op_id: int | str,
              detail_level: int = 0,
              tipology: str = ''
              ):
    """Function OPERACION from INE. Returns the URL to make the request."""
    Inputs = FIM.InputParams(
        op_id=op_id,
        detail_level=detail_level,
    )
    URL = INEURL.url_gen('OPERACION', Inputs.op_id, **Inputs.get_params())
    return URL


@validate_call
def variables(page: int = 1):
    """Function VARIABLES from INE. Returns the URL to make the request."""
    filter_params = filtering.date_count_selection_params_builder(
        page=page
    )
    URL = INEURL.url_gen('VARIABLES', **filter_params)
    return URL


@validate_call
def variable(var_id: int | str):
    """
    Function VARIABLE from INE. Returns the URL to make the request.

    Not documented in the official page.
    """
    Inputs = FIM.InputParams(
        var_id=var_id,
    )
    URL = INEURL.url_gen('VARIABLE', Inputs.var_id)
    return URL


@validate_call
def variables_operacion(op_id: int | str,
                        page: int = 1
                        ):
    """
    Function VARIABLES_OPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        op_id=op_id
    )

    filter_params = filtering.date_count_selection_params_builder(
        page=page
    )
    URL = INEURL.url_gen('VARIABLES_OPERACION', Inputs.op_id, **filter_params)
    return URL


@validate_call
def valores_variable(var_id: int | str,
                     detail_level: int = 0,
                     classification_id: int | None = None
                     ):
    """
    Function VALORES_VARIABLE from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        var_id=var_id,
        detail_level=detail_level,
        classification_id=classification_id
    )

    if classification_id is not None:
        warnings.war('Classification_id is kept because it is shown in the official documentation, but it seems deprecated and using this will probably raise an error.')

    URL = INEURL.url_gen(
        'VALORES_VARIABLE',
        Inputs.var_id,
        **Inputs.get_params(add_clasif=True)
    )
    return URL


@validate_call
def valores_variableoperacion(var_id: int | str,
                              op_id: int | str,
                              detail_level: int = 0
                              ):
    """
    Function VALORES_VARIABLEOPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        var_id=var_id,
        op_id=op_id,
        detail_level=detail_level
    )
    URL = INEURL.url_gen(
        'VALORES_VARIABLEOPERACION',
        Inputs.var_id,
        Inputs.op_id,
        **Inputs.get_params()
    )
    return URL


@validate_call
def tablas_operacion(op_id: int | str,
                     detail_level: int = 0,
                     geographical_level: int | None = None,
                     tipology: str = ''
                     ):
    """
    Function TABLAS_OPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        op_id=op_id,
        detail_level=detail_level,
        geographical_level=geographical_level,
        tipology=tipology
    )
    URL = INEURL.url_gen(
        'TABLAS_OPERACION',
        Inputs.op_id,
        **Inputs.get_params()
    )
    return URL


@validate_call
def grupos_tabla(tab_id: int | str):
    """
    Function GRUPOS_TABLA from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        tab_id=tab_id,
    )
    URL = INEURL.url_gen(
        'GRUPOS_TABLA',
        Inputs.tab_id,
    )
    return URL


@validate_call
def valores_grupostabla(tab_id: int | str,
                        group_id: int | str,
                        detail_level: int = 0
                        ):
    """
    Function VALORES_GRUPOSTABLA from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        tab_id=tab_id,
        group_id=group_id,
        detail_level=detail_level
    )
    URL = INEURL.url_gen(
        'VALORES_GRUPOSTABLA',
        Inputs.tab_id,
        Inputs.group_id,
        **Inputs.get_params()
    )
    return URL


@validate_call
def serie(serie_id: int | str,
          detail_level: int = 0,
          tipology: str = ''
          ):
    """
    Function SERIE from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        serie_id=serie_id,
        tipology=tipology,
        detail_level=detail_level
    )
    URL = INEURL.url_gen(
        'SERIE',
        Inputs.serie_id,
        **Inputs.get_params()
    )
    return URL


@validate_call
def series_operacion(op_id: int | str,
                     detail_level: int = 0,
                     tipology: str = '',
                     page: int = 1
                     ):
    """
    Function SERIES_OPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        op_id=op_id,
        tipology=tipology,
        detail_level=detail_level
    )

    filter_params = filtering.date_count_selection_params_builder(
        page=page
    )
    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen(
        'SERIES_OPERACION',
        Inputs.op_id,
        **query
    )
    return URL


@validate_call
def valores_serie(serie_id: int | str,
                  detail_level: int = 0
                  ):
    """
    Function VALORES_SERIE from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        serie_id=serie_id,
        detail_level=detail_level
    )
    URL = INEURL.url_gen(
        'VALORES_SERIE',
        Inputs.serie_id,
        **Inputs.get_params()
    )
    return URL


@validate_call
def series_tabla(tab_id: int | str,
                 detail_level: int = 0,
                 tipology: str = '',
                 metadata_filtering=dict()
                 ):
    """
    Function SERIES_TABLA from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        tab_id=tab_id,
        detail_level=detail_level,
        tipology=tipology
    )
    filter_params = filtering.metadata_param_filtering_builder(
        var_value_dict=metadata_filtering,
        format_='series'
    )
    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen(
        'SERIES_TABLA',
        Inputs.tab_id,
        **query
    )
    return URL


@validate_call
def serie_metadataoperacion(op_id: int | str,
                            detail_level: int = 0,
                            tipology: str = '',
                            metadata_filtering=dict()
                            ):
    """
    Function SERIE_METADATAOPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        op_id=op_id,
        detail_level=detail_level,
        tipology=tipology
    )
    filter_params = filtering.metadata_param_filtering_builder(
        var_value_dict=metadata_filtering,
        format_='metadata'
    )
    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen(
        'SERIE_METADATAOPERACION',
        Inputs.op_id,
        **query
    )
    return URL


@validate_call
def periodicidades():
    """
    Function PERIODICIDADES from INE.

    Returns the URL to make the request.
    """
    URL = INEURL.url_gen('PERIODICIDADES')
    return URL


@validate_call
def periodicidad(periodicity_id: int | str):
    """
    Function PERIODICIDAD from INE.

    Returns the URL to make the request.

    Not in the official documentation.
    """
    Inputs = FIM.InputParams(periodicity_id=periodicity_id)
    URL = INEURL.url_gen('PERIODICIDAD', Inputs.periodicity_id)
    return URL


@validate_call
def publicaciones(detail_level: int = 0,
                  tipology: str = ''
                  ):
    """
    Function PUBLICACIONES from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        detail_level=detail_level,
        tipology=tipology
    )
    URL = INEURL.url_gen('PUBLICACIONES', **Inputs.get_params())
    return URL


@validate_call
def publicaciones_operacion(op_id: int | str,
                            detail_level: int = 0,
                            tipology: str = ''
                            ):
    """
    Function PUBLICACIONES_OPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        op_id=op_id,
        detail_level=detail_level,
        tipology=tipology
    )
    URL = INEURL.url_gen('PUBLICACIONES_OPERACION',
                         Inputs.op_id,
                         **Inputs.get_params())
    return URL


@validate_call
def publicacionfecha_publicacion(publication_id: int | str,
                                 detail_level: int = 0,
                                 tipology: str = ''
                                 ):
    """
    Function PUBLICACIONFECHA_PUBLICACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        publication_id=publication_id,
        detail_level=detail_level,
        tipology=tipology
    )
    URL = INEURL.url_gen('PUBLICACIONFECHA_PUBLICACION',
                         Inputs.publication_id,
                         **Inputs.get_params())
    return URL


@validate_call
def clasificaciones():
    """
    Function CLASIFICACIONES from INE.

    Returns the URL to make the request.
    """
    URL = INEURL.url_gen('CLASIFICACIONES')
    return URL


@validate_call
def clasificaciones_operacion(op_id: int | str):
    """
    Function CLASIFICACIONES_OPERACION from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        op_id=op_id
    )
    URL = INEURL.url_gen('CLASIFICACIONES_OPERACION',
                         Inputs.op_id
                         )
    return URL


@validate_call
def valores_hijos(var_id: int | str,
                  val_id: int | str,
                  detail_level: int = 0
                  ):
    """
    Function VALORES_HIJOS from INE.

    Returns the URL to make the request.
    """
    Inputs = FIM.InputParams(
        var_id=var_id,
        val_id=val_id,
        detail_level=detail_level
    )
    URL = INEURL.url_gen('VALORES_HIJOS',
                         Inputs.var_id,
                         Inputs.val_id,
                         **Inputs.get_params()
                         )
    return URL


@validate_call
def unidades():
    """
    Function UNIDADES from INE.

    Returns the URL to make the request.

    Not in the official documentation.
    """
    URL = INEURL.url_gen('UNIDADES')
    return URL


@validate_call
def unidad(unit_id: int | str):
    """
    Function UNIDAD from INE.

    Returns the URL to make the request.

    Not in the official documentation.
    """
    Inputs = FIM.InputParams(
        unit_id=unit_id
    )
    URL = INEURL.url_gen('UNIDAD', Inputs.unit_id)
    return URL


@validate_call
def escalas(tipology: str = ''):
    """
    Function ESCALAS from INE.

    Returns the URL to make the request.

    Not in the official documentation.
    """
    URL = INEURL.url_gen('ESCALAS')
    return URL


@validate_call
def escala(scale_id: int | str, tipology: str = ''):
    """
    Function ESCALA from INE.

    Returns the URL to make the request.

    Not in the official documentation.
    """
    Inputs = FIM.InputParams(
        scale_id=scale_id
    )
    URL = INEURL.url_gen('ESCALA', Inputs.scale_id)
    return URL


@validate_call
def periodo(period_id: int | str):
    """
    Function PERIODO from INE.

    Returns the URL to make the request.

    Not in the official documentation.
    """
    Inputs = FIM.InputParams(
        period_id=period_id
    )
    URL = INEURL.url_gen('PERIODO', Inputs.period_id)
    return URL
