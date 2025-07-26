# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 18:46:00 2025

@author: mano

This file contains 4 classes, all of them act as bridge with the INE API,
all of them return the results from the INE API.
"""

import os
import sys

RMPath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), './urlrequestsmanagement/src')
)

if RMPath not in sys.path:
    sys.path.insert(0, RMPath)

import RequestsManagement as ReqMan
import INE_functions as functions
import Models.INEModels as models
import json


def json_string_to_python(string: str):
    """
    Process the string to a python dict.

    Raises ValueError if it is an invalid JSON.

    Parameters
    ----------
    string : str
        JSON.

    Raises
    ------
    ValueError
        JSON was invalid.

    Returns
    -------
    data : dict
        JSON as dict.

    """
    string = string.decode('utf-8')
    try:
        data = json.loads(string)
    except json.JSONDecodeError:
        try:
            data = json.loads(string + ']')
            # This is here because sometimes the API returns a list with
            # a missing ] at the end.
        except json.JSONDecodeError:
            raise ValueError(f'Your input {string} is an invalid JSON.')
    return data

def get_data_process_sync(RM,
                          url: str,
                          mode: str):
    """
    Get the data from INE URL.

    Must pass the request manager instance to make the request.

    If mode is raw, it returns the result as string.
    If mode is py or pydantic it returns a python dictionary.

    Parameters
    ----------
    RM : RequestsManagement.RequestsManager
        Request Manager instance.
    url : str
        url to get the data from.
    mode : Literal[raw, py, pydantic]
        Mode to get the results.

    Returns
    -------
    content : str | dict
        Content from request.
    """
    content_str = RM.sync_request('GET', url).content
    if mode == 'raw':
        return content_str
    elif mode in ['py', 'pydantic']:
        return json_string_to_python(content_str)
    return None


async def get_data_process_async(RM,
                                 url: str,
                                 mode: str):
    """
    Get the data from INE URL.

    Must pass the request manager instance to make the request.

    If mode is raw, it returns the result as string.
    If mode is py or pydantic it returns a python dictionary.

    Parameters
    ----------
    RM : RequestsManagement.RequestsManager
        Request Manager instance.
    url : str
        url to get the data from.
    mode : Literal[raw, py, pydantic]
        Mode to get the results.

    Returns
    -------
    content : str | dict
        Content from request.
    """
    content_str = await RM.async_request('GET', url).content
    if mode == 'raw':
        return content_str
    elif mode in ['py', 'pydantic']:
        return json_string_to_python(content_str)
    return None


class INEAPIClientSync():
    """
    Wrapper for INE API, makes requests using sync requests package.

    All methods make the request and retreive the results.
    """

    def __init__(self, mode='raw', RM=None):
        """
        Init of class.

        Mode: Literal['raw', 'py', 'pydantic']

            raw: returns the result straight from INE API, without checking.
            py: returns the result as python dict
            pydantic: returns the result as pydantic object.

        RM: RequestsManagement.RequestManager instance if you already have one.
        """
        if mode not in ['raw', 'py', 'pydantic']:
            raise ValueError(
                "mode can't be different from raw, py or pydantic."
            )
        self.mode = mode
        if RM is None:
            self.__RM = ReqMan.RequestsManager()
        return None

    def __get_data(self, url):
        """Just to simplify the usage of function."""
        return get_data_process_sync(self.__RM, url, self.mode)

    def get_datos_tabla(self,
                        tab_id: int | str,
                        detail_level: int = 0,
                        tipology: str = '',
                        count: int | None = None,
                        list_of_dates=None,
                        metadata_filtering=dict()
                        ):
        """Process for DATOS_TABLA. Returns content."""
        url = functions.datos_tabla(tab_id,
                                    detail_level=detail_level,
                                    tipology=tipology,
                                    count=count,
                                    list_of_dates=list_of_dates,
                                    metadata_filtering=metadata_filtering)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyDatosSerieList(items=data)
        return data

    def get_datos_serie(self,
                        serie_id: int | str,
                        detail_level: int = 0,
                        tipology: str = '',
                        count: int | None = None,
                        list_of_dates=None
                        ):
        """Process for DATOS_SERIE. Returns content."""
        url = functions.datos_serie(serie_id,
                                    detail_level=detail_level,
                                    tipology=tipology,
                                    count=count,
                                    list_of_dates=list_of_dates)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyDatosSerie(**data)
        return data

    def get_datos_metadataoperacion(self,
                                    op_id: int | str,
                                    detail_level: int = 0,
                                    tipology: str = '',
                                    count: int | None = None,
                                    list_of_dates=None,
                                    metadata_filtering=dict()
                                    ):
        """Process for DATOS_METADATAOPERACION. Returns content."""
        url = functions.datos_metadataoperacion(
            op_id,
            detail_level=detail_level,
            tipology=tipology,
            count=count,
            list_of_dates=list_of_dates,
            metadata_filtering=metadata_filtering)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyDatosSerieList(items=data)
        return data

    def get_operaciones_disponibles(self,
                                    detail_level: int = 0,
                                    geographical_level: int | None = None,
                                    page: int | None = None
                                    ):
        """Process for OPERACIONES_DISPONIBLES. Returns content."""
        url = functions.operaciones_disponibles(
            detail_level=detail_level,
            geographical_level=geographical_level,
            page=page)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyOperacionList(items=data)
        return data

    def get_operaciones(self,
                        detail_level: int = 0,
                        page: int | None = None
                        ):
        """Process for OPERACIONES. Returns content."""
        url = functions.operaciones(detail_level=detail_level,
                                    page=page)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyOperacionList(items=data)
        return data

    def get_operacion(self,
                      op_id: int | str,
                      detail_level: int = 0
                      ):
        """Process for OPERACION. Returns content."""
        url = functions.operacion(op_id,
                                  detail_level=detail_level)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyOperacion(**data)
        return data

    def get_variables(self,
                      page: int | None = None):
        """Process for VARIABLES. Returns content."""
        url = functions.variables(page=page)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyVariableList(items=data)
        return data

    def get_variable(self,
                     var_id: int | str):
        """Process for VARIABLE. Returns content."""
        url = functions.variable(var_id)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyVariable(**data)
        return data

    def get_variables_operacion(self,
                                op_id: int | str,
                                page: int | None = None):
        """Process for VARIABLES_OPERACION. Returns content."""
        url = functions.variables_operacion(op_id,
                                            page=page)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyVariableList(items=data)
        return data

    def get_valores_variable(self,
                             var_id: int | str,
                             detail_level: int = 0,
                             classification_id: int | None = None):
        """Process for VALORES_VARIABLE. Returns content."""
        url = functions.valores_variable(
            var_id,
            detail_level=detail_level,
            classification_id=classification_id)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    def get_valores_variableoperacion(self,
                                      var_id: int | str,
                                      op_id: int | str,
                                      detail_level: int = 0):
        """Process for VALORES_VARIABLEOPERACION. Returns content."""
        url = functions.valores_variableoperacion(
            var_id,
            op_id,
            detail_level=detail_level)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    def get_tablas_operacion(self,
                             op_id: int | str,
                             detail_level: int = 0,
                             geographical_level: int | None = None,
                             tipology: str = ''):
        """Process for TABLAS_OPERACION. Returns content."""
        url = functions.tablas_operacion(
            op_id,
            detail_level=detail_level,
            geographical_level=geographical_level,
            tipology=tipology)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyTablaList(items=data)
        return data

    def get_grupos_tabla(self,
                         tab_id: int | str):
        """Process for GRUPOS_TABLA. Returns content."""
        url = functions.grupos_tabla(tab_id)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyGrupoTablaList(items=data)
        return data

    def get_valores_grupostabla(self,
                                tab_id: int | str,
                                group_id: int | str,
                                detail_level: int = 0):
        """Process for VALORES_GRUPOSTABLA. Returns content."""
        url = functions.valores_grupostabla(tab_id,
                                            group_id,
                                            detail_level=detail_level)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    def get_serie(self,
                  serie_id: int | str,
                  detail_level: int = 0,
                  tipology: str = ''):
        """Process for SERIE. Returns content."""
        url = functions.serie(serie_id,
                              detail_level=detail_level,
                              tipology=tipology)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerie(**data)
        return data

    def get_series_operacion(self,
                             op_id: int | str,
                             detail_level: int = 0,
                             tipology: str = '',
                             page: int | None = None
                             ):
        """Process for SERIES_OPERACION. Returns content."""
        url = functions.series_operacion(op_id,
                                         detail_level=detail_level,
                                         tipology=tipology,
                                         page=page)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerieList(items=data)
        return data

    def get_valores_serie(self,
                          serie_id: int | str,
                          detail_level: int = 0
                          ):
        """Process for VALORES_SERIE. Returns content."""
        url = functions.valores_serie(serie_id,
                                      detail_level=detail_level)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    def get_series_tabla(self,
                         tab_id: int | str,
                         detail_level: int = 0,
                         tipology: str = '',
                         metadata_filtering=dict()
                         ):
        """Process for SERIES_TABLA. Returns content."""
        url = functions.series_tabla(tab_id,
                                     detail_level=detail_level,
                                     tipology=tipology,
                                     metadata_filtering=metadata_filtering
                                     )
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerieList(items=data)
        return data

    def get_serie_metadataoperacion(self,
                                    op_id: int | str,
                                    detail_level: int = 0,
                                    tipology: str = '',
                                    metadata_filtering=dict()
                                    ):
        """Process for SERIE_METADATAOPERACION. Returns content."""
        url = functions.serie_metadataoperacion(
            op_id,
            detail_level=detail_level,
            tipology=tipology,
            metadata_filtering=metadata_filtering)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerieList(items=data)
        return data

    def get_periodicidades(self):
        """Process for PERIODICIDADES. Returns content."""
        url = functions.periodicidades()
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPeriodicidadList(items=data)
        return data

    def get_periodicidad(self,
                         periodicity_id: int | str):
        """Process for PERIODICIDAD. Returns content."""
        url = functions.periodicidad(periodicity_id)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPeriodicidad(**data)
        return data

    def get_publicaciones(self,
                          detail_level: int = 0,
                          tipology: str = ''):
        """Process for PUBLICACIONES. Returns content."""
        url = functions.publicaciones(detail_level=detail_level,
                                      tipology=tipology)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPublicacionList(items=data)
        return data

    def get_publicaciones_operacion(self,
                                    op_id: int | str,
                                    detail_level: int = 0,
                                    tipology: str = ''):
        """Process for PUBLICACIONES_OPERACION. Returns content."""
        url = functions.publicaciones_operacion(op_id,
                                                detail_level=detail_level,
                                                tipology=tipology)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPublicacionList(items=data)
        return data

    def get_publicacionfecha_publicacion(self,
                                         publication_id: int | str,
                                         detail_level: int = 0,
                                         tipology: str = ''
                                         ):
        """Process for PUBLICACIONFECHA_PUBLICACION. Returns content."""
        url = functions.publicacionfecha_publicacion(publication_id,
                                                     detail_level=detail_level,
                                                     tipology=tipology)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyFechaPublicacionList(items=data)
        return data

    def get_clasificaciones(self):
        """Process for CLASIFICACIONES. Returns content."""
        url = functions.clasificaciones()
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyClasificacionList(items=data)
        return data

    def get_clasificaciones_operacion(self,
                                      op_id: int | str):
        """Process for CLASIFICACIONES_OPERACION. Returns content."""
        url = functions.clasificaciones_operacion(op_id)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyClasificacionList(items=data)
        return data

    def get_valores_hijos(self,
                          var_id: int | str,
                          val_id: int | str,
                          detail_level: int = 0):
        """Process for VALORES_HIJOS. Returns content."""
        url = functions.valores_hijos(var_id,
                                      val_id,
                                      detail_level=detail_level)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    def get_unidades(self):
        """Process for UNIDADES. Returns content."""
        url = functions.unidades()
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyUnidadList(items=data)
        return data

    def get_unidad(self,
                   unit_id: int | str):
        """Process for UNIDAD. Returns content."""
        url = functions.unidad(unit_id)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyUnidad(**data)
        return data

    def get_escalas(self):
        """Process for ESCALAS. Returns content."""
        url = functions.escalas()
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyEscalaList(items=data)
        return data

    def get_escala(self,
                   scale_id: int | str):
        """Process for ESCALA. Returns content."""
        url = functions.escala()
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyEscala(**data)
        return data

    def get_periodo(self,
                    period_id: int | str):
        """Process for PERIODO. Returns content."""
        url = functions.periodo()
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPeriodo(**data)
        return data