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

import INE_Filtering as filtering
import INE_URL_Treatment as INEURL
import Models.FunctionInputsModels as FIM


def datos_tabla(tab_id: int | str,
                detail_level=0,
                tipology='',
                count=None,
                list_of_dates=None,
                metadata_filtering=dict()
                ):
    """Function DATOS_TABLA from INE. Returns the URL to make the request."""
    Inputs = FIM.InputParams(
        tab_id=tab_id,
        detail_level=detail_level,
        tipology=tipology,
    )

    filter_params = filtering.date_count_selection_params_builder(
        var_value_dict=metadata_filtering,
        format_='series',
        list_of_dates=list_of_dates,
        count=count
    )

    query = Inputs.join_filtering_params(filter_params)
    URL = INEURL.url_gen('DATOS_TABLA', Inputs.tab_id, **query)
    return URL


def datos_serie(serie_id: int | str,
                detail_level=0,
                tipology='',
                count=None,
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


def datos_metadataoperacion(op_id: int | str,
                            detail_level=0,
                            tipology='',
                            count=None,
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
    URL = INEURL.url_gen('DATOS_METADATAOPERACION', Inputs.serie_id, **query)
    return URL


def operaciones_disponibles(detail_level: int | None = 0,
                            geographical_level: int | None = None,
                            page: int | None = None
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


def operaciones(detail_level: int | None = 0,
                page: int | None = None
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


def operacion(op_id: int | str,
              detail_level: int | None = 0,
              ):
    """Function OPERACION from INE. Returns the URL to make the request."""
    Inputs = FIM.InputParams(
        op_id=op_id,
        detail_level=detail_level,
    )
    query = Inputs.get_params()
    URL = INEURL.url_gen('OPERACION', Inputs.op_id, **query)
    return URL


def variables(page: int | None = None):
    """Function VARIABLES from INE. Returns the URL to make the request."""
    filter_params = filtering.date_count_selection_params_builder(
        page=page
    )
    URL = INEURL.url_gen('VARIABLES', **filter_params)
    return URL


def variable(var_id: int | str):
    """
    Function VARIABLES from INE. Returns the URL to make the request.

    Not documented in the official page.
    """
    Inputs = FIM.InputParams(
        var_id=var_id,
    )
    URL = INEURL.url_gen('OPERACION', Inputs.var_id)
    return URL


def variables_operacion(op_id: int | str,
                        page: int | None = None
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
    URL = INEURL.url_gen('OPERACION', Inputs.op_id, **filter_params)
    return URL


