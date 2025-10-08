# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 18:46:00 2025

@author: mano

This file contains 4 classes, all of them act as bridge with the INE API,
all of them return the results from the INE API.
"""

from .urlrequestsmangement.src import RequestsManagement as ReqMan
from . import INE_functions as functions
from .Models import INEModels as models
import json


def reemplazar_none_a_null(obj_og: dict):
    """
    Transform None from INE to 'null' string.

    Responses from INE API, may return values that are null. This is
    transformed to None when parsed to Python. In this cases, they will
    be transformed back to 'null' as string, since None is used as missing
    fields and we can't check what fields may be missing and when.
    """
    obj = dict(obj_og)
    for k, v in obj.items():
        if isinstance(v, dict):
            obj[k] = reemplazar_none_a_null(v)
        else:
            if v is None:
                obj[k] = 'null'
    return obj


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
    result = await RM.async_request('GET', url)
    content_str = await result.content.read()
    if mode == 'raw':
        return content_str
    elif mode in ['py', 'pydantic']:
        return json_string_to_python(content_str)
    return None


class Base():
    """Base init for both classes."""

    def __init__(self,
                 mode='raw',
                 sleep_time: int | float = 0.4,
                 print_url: bool = False):
        """
        Init of class.

        Mode: Literal['raw', 'py', 'pydantic']    default: raw

            raw: returns the result straight from INE API, without checking, and as string.
            py: returns the result as python dict or list, without checking.
            pydantic: returns the result as pydantic object and checks the results are correctly formatted according to models.

        sleep_time: is the sleep time after each request. default: 0.4s

        print_url: is the option to set if you want to print URLs after each
        request.
        """
        if mode not in ['raw', 'py', 'pydantic']:
            raise ValueError(
                "mode can't be different from raw, py or pydantic."
            )
        self.mode = mode

        self._RM = ReqMan.RequestsManager(
            sleep_time=sleep_time,
            print_url=print_url
        )
        return None

    def close_all_sessions(self):
        """Closes all requests sessions."""
        self._RM.close_all_sessions()
        return None


class INEAPIClientSync(Base):
    """
    Wrapper for INE API, makes requests using sync requests package.

    All methods make the request and retreive the results.
    """

    def __get_data(self, url):
        """Just to simplify the usage of function."""
        return get_data_process_sync(self._RM, url, self.mode)

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
                                    page: int = 1,
                                    tipology: str = ''
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
                        page: int = 1,
                        tipology: str = ''
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
                      detail_level: int = 0,
                      tipology: str = ''
                      ):
        """Process for OPERACION. Returns content."""
        url = functions.operacion(op_id,
                                  detail_level=detail_level)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyOperacion(**data)
        return data

    def get_variables(self,
                      page: int = 1):
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
                                page: int = 1):
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
                             page: int = 1
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

    def get_escalas(self, tipology: str = ''):
        """Process for ESCALAS. Returns content."""
        url = functions.escalas(tipology=tipology)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyEscalaList(items=data)
        return data

    def get_escala(self,
                   scale_id: int | str,
                   tipology: str = ''):
        """Process for ESCALA. Returns content."""
        url = functions.escala(scale_id, tipology=tipology)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyEscala(**data)
        return data

    def get_periodo(self,
                    period_id: int | str):
        """Process for PERIODO. Returns content."""
        url = functions.periodo(period_id)
        data = self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPeriodo(**data)
        return data


class INEAPIClientAsync(Base):
    """
    Wrapper for INE API, makes requests using sync requests package.

    All methods make the request and retreive the results.
    """

    async def __get_data(self, url):
        """Just to simplify the usage of function."""
        return await get_data_process_async(self._RM, url, self.mode)

    async def get_datos_tabla(self,
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
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyDatosSerieList(items=data)
        return data

    async def get_datos_serie(self,
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
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyDatosSerie(**data)
        return data

    async def get_datos_metadataoperacion(self,
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
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyDatosSerieList(items=data)
        return data

    async def get_operaciones_disponibles(self,
                                          detail_level: int = 0,
                                          geographical_level: int | None = None,
                                          page: int = 1,
                                          tipology: str = ''
                                          ):
        """Process for OPERACIONES_DISPONIBLES. Returns content."""
        url = functions.operaciones_disponibles(
            detail_level=detail_level,
            geographical_level=geographical_level,
            page=page)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyOperacionList(items=data)
        return data

    async def get_operaciones(self,
                              detail_level: int = 0,
                              page: int = 1,
                              tipology: str = ''
                              ):
        """Process for OPERACIONES. Returns content."""
        url = functions.operaciones(detail_level=detail_level,
                                    page=page)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyOperacionList(items=data)
        return data

    async def get_operacion(self,
                            op_id: int | str,
                            detail_level: int = 0,
                            tipology: str = ''
                            ):
        """Process for OPERACION. Returns content."""
        url = functions.operacion(op_id,
                                  detail_level=detail_level)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyOperacion(**data)
        return data

    async def get_variables(self,
                            page: int = 1):
        """Process for VARIABLES. Returns content."""
        url = functions.variables(page=page)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyVariableList(items=data)
        return data

    async def get_variable(self,
                           var_id: int | str):
        """Process for VARIABLE. Returns content."""
        url = functions.variable(var_id)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyVariable(**data)
        return data

    async def get_variables_operacion(self,
                                      op_id: int | str,
                                      page: int = 1):
        """Process for VARIABLES_OPERACION. Returns content."""
        url = functions.variables_operacion(op_id,
                                            page=page)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyVariableList(items=data)
        return data

    async def get_valores_variable(self,
                                   var_id: int | str,
                                   detail_level: int = 0,
                                   classification_id: int | None = None):
        """Process for VALORES_VARIABLE. Returns content."""
        url = functions.valores_variable(
            var_id,
            detail_level=detail_level,
            classification_id=classification_id)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    async def get_valores_variableoperacion(self,
                                            var_id: int | str,
                                            op_id: int | str,
                                            detail_level: int = 0):
        """Process for VALORES_VARIABLEOPERACION. Returns content."""
        url = functions.valores_variableoperacion(
            var_id,
            op_id,
            detail_level=detail_level)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    async def get_tablas_operacion(self,
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
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyTablaList(items=data)
        return data

    async def get_grupos_tabla(self,
                               tab_id: int | str):
        """Process for GRUPOS_TABLA. Returns content."""
        url = functions.grupos_tabla(tab_id)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyGrupoTablaList(items=data)
        return data

    async def get_valores_grupostabla(self,
                                      tab_id: int | str,
                                      group_id: int | str,
                                      detail_level: int = 0):
        """Process for VALORES_GRUPOSTABLA. Returns content."""
        url = functions.valores_grupostabla(tab_id,
                                            group_id,
                                            detail_level=detail_level)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    async def get_serie(self,
                        serie_id: int | str,
                        detail_level: int = 0,
                        tipology: str = ''):
        """Process for SERIE. Returns content."""
        url = functions.serie(serie_id,
                              detail_level=detail_level,
                              tipology=tipology)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerie(**data)
        return data

    async def get_series_operacion(self,
                                   op_id: int | str,
                                   detail_level: int = 0,
                                   tipology: str = '',
                                   page: int = 1
                                   ):
        """Process for SERIES_OPERACION. Returns content."""
        url = functions.series_operacion(op_id,
                                         detail_level=detail_level,
                                         tipology=tipology,
                                         page=page)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerieList(items=data)
        return data

    async def get_valores_serie(self,
                                serie_id: int | str,
                                detail_level: int = 0
                                ):
        """Process for VALORES_SERIE. Returns content."""
        url = functions.valores_serie(serie_id,
                                      detail_level=detail_level)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    async def get_series_tabla(self,
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
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerieList(items=data)
        return data

    async def get_serie_metadataoperacion(self,
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
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pySerieList(items=data)
        return data

    async def get_periodicidades(self):
        """Process for PERIODICIDADES. Returns content."""
        url = functions.periodicidades()
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPeriodicidadList(items=data)
        return data

    async def get_periodicidad(self,
                               periodicity_id: int | str):
        """Process for PERIODICIDAD. Returns content."""
        url = functions.periodicidad(periodicity_id)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPeriodicidad(**data)
        return data

    async def get_publicaciones(self,
                                detail_level: int = 0,
                                tipology: str = ''):
        """Process for PUBLICACIONES. Returns content."""
        url = functions.publicaciones(detail_level=detail_level,
                                      tipology=tipology)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPublicacionList(items=data)
        return data

    async def get_publicaciones_operacion(self,
                                          op_id: int | str,
                                          detail_level: int = 0,
                                          tipology: str = ''):
        """Process for PUBLICACIONES_OPERACION. Returns content."""
        url = functions.publicaciones_operacion(op_id,
                                                detail_level=detail_level,
                                                tipology=tipology)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPublicacionList(items=data)
        return data

    async def get_publicacionfecha_publicacion(self,
                                               publication_id: int | str,
                                               detail_level: int = 0,
                                               tipology: str = ''
                                               ):
        """Process for PUBLICACIONFECHA_PUBLICACION. Returns content."""
        url = functions.publicacionfecha_publicacion(publication_id,
                                                     detail_level=detail_level,
                                                     tipology=tipology)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyFechaPublicacionList(items=data)
        return data

    async def get_clasificaciones(self):
        """Process for CLASIFICACIONES. Returns content."""
        url = functions.clasificaciones()
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyClasificacionList(items=data)
        return data

    async def get_clasificaciones_operacion(self,
                                            op_id: int | str):
        """Process for CLASIFICACIONES_OPERACION. Returns content."""
        url = functions.clasificaciones_operacion(op_id)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyClasificacionList(items=data)
        return data

    async def get_valores_hijos(self,
                                var_id: int | str,
                                val_id: int | str,
                                detail_level: int = 0):
        """Process for VALORES_HIJOS. Returns content."""
        url = functions.valores_hijos(var_id,
                                      val_id,
                                      detail_level=detail_level)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyValorList(items=data)
        return data

    async def get_unidades(self):
        """Process for UNIDADES. Returns content."""
        url = functions.unidades()
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyUnidadList(items=data)
        return data

    async def get_unidad(self,
                         unit_id: int | str):
        """Process for UNIDAD. Returns content."""
        url = functions.unidad(unit_id)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyUnidad(**data)
        return data

    async def get_escalas(self, tipology: str = ''):
        """Process for ESCALAS. Returns content."""
        url = functions.escalas(tipology=tipology)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyEscalaList(items=data)
        return data

    async def get_escala(self,
                         scale_id: int | str,
                         tipology: str = ''):
        """Process for ESCALA. Returns content."""
        url = functions.escala(scale_id, tipology=tipology)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyEscala(**data)
        return data

    async def get_periodo(self,
                          period_id: int | str):
        """Process for PERIODO. Returns content."""
        url = functions.periodo(period_id)
        data = await self.__get_data(url)
        if self.mode == 'pydantic':
            return models.pyPeriodo(**data)
        return data


class EasyINEAPIClientSync(INEAPIClientSync):
    """Same class as INEAPI but with additional methods for easier usage."""

    def get_operations_(self,
                        op_id: int | str | None = None,
                        detail_level: int = 0,
                        geographical_level: int | None = None,
                        extra_op: bool = False,
                        page: int = 1,
                        tipology: str = ''):
        """
        Returns the data of all operations, or the specified one.

        if extra_op param is set, performs the requests that returns some
        additional operaciones.

        If you specify the op_id it will return the specified operation.
        """
        if op_id is None:
            if extra_op:
                return self.get_operaciones(detail_level=detail_level,
                                            page=page,
                                            tipology=tipology)
            return self.get_operaciones_disponibles(
                detail_level=detail_level,
                geographical_level=geographical_level,
                page=page,
                tipology=tipology
            )
        else:
            return self.get_operacion(op_id,
                                      detail_level=detail_level,
                                      tipology=tipology)

    def get_variables_(self,
                       op_id: int | str | None = None,
                       var_id: int | str | None = None,
                       page: int = 1):
        """
        Returns the available variables.

        If the operation is specified, it returns the variables asociated with
        that operation.

        If a variable is specified, it returns the data for such variable.

        If no param is specified it returns all the available variables.
        """
        if var_id is None:
            if op_id is None:
                return self.get_variables(page=page)
            else:
                return self.get_variables_operacion(op_id, page=page)
        else:
            return self.get_variable(var_id)

    def get_values_(self,
                    var_id: int | str | None = None,
                    classification_id: int | str | None = None,
                    op_id: int | str | None = None,
                    val_id: int | str | None = None,
                    serie_id: int | str | None = None,
                    tab_id: int | str | None = None,
                    group_id: int | str | None = None,
                    detail_level: int = 0):
        """
        Returns the available values for the specified inputs.

            If var_id is provided.
                It returns the values for such variable.
                    Additionaly, it can be filtered with the classification_id.
            If var_id and val_id is provided.
                It returns the sons values for such value.
            If var_id and val_id is provided.
                It returns the values for such operation.
            If serie_id is provided.
                It returns the values asociated with such serie. The metadata.
            If tab_id and group_id is provided.
                It returns the values for such group of tables.

        All returns are Valor Objects.
        """
        if var_id is not None:
            if val_id is not None:
                return self.get_valores_hijos(var_id,
                                              val_id,
                                              detail_level=detail_level)
            if op_id is None:
                return self.get_valores_variable(
                    var_id,
                    detail_level=detail_level,
                    classification_id=classification_id)
            else:
                return self.get_valores_variableoperacion(
                    var_id,
                    op_id,
                    detail_level=detail_level)
        elif serie_id is not None:
            return self.get_valores_serie(serie_id, detail_level=detail_level)
        elif tab_id is not None and group_id is not None:
            return self.get_valores_grupostabla(tab_id,
                                                group_id,
                                                detail_level=detail_level)
        else:
            raise ValueError(
                'One input must be provided, var_id, or serie_id or'
                + ' tab_id and group_id.'
            )

    def get_tables_(self,
                    op_id: int | str | None = None,
                    tab_id: int | str | None = None,
                    detail_level: int = 0,
                    geographical_level: int | None = None,
                    tipology: str = ''):
        """
        Returns the tables or group tables.

            If op_id is provided.
                It returns the tables asociated with such operation.
        """
        if op_id is not None:
            return self.get_tablas_operacion(
                op_id,
                detail_level=detail_level,
                geographical_level=geographical_level,
                tipology=tipology)
        elif tab_id is not None:
            return self.get_grupos_tabla(tab_id)
        else:
            raise ValueError('Wether op_id or tab_id must be provided.')

    def get_series_(self,
                    serie_id: int | str | None = None,
                    op_id: int | str | None = None,
                    tab_id: int | str | None = None,
                    detail_level: int = 0,
                    tipology: str = '',
                    page: int = 1,
                    metadata_filtering=dict()
                    ):
        """
        Returns the available information for the series.

            If serie_id is provided.
                It returns the information for such serie.
            If op_id is provided.
                It returns all the series for such operation and such filters.
            If tab_id is provided.
                It returns all the series for such table and such filters.
        """
        if serie_id is not None:
            return self.get_serie(serie_id,
                                  detail_level=detail_level,
                                  tipology=tipology)
        elif op_id is not None:
            empty_filters = not bool(metadata_filtering)
            if empty_filters:
                return self.get_series_operacion(op_id,
                                                 detail_level=detail_level,
                                                 tipology=tipology,
                                                 page=page)
            else:
                return self.get_serie_metadataoperacion(
                    op_id,
                    detail_level=detail_level,
                    tipology=tipology,
                    metadata_filtering=metadata_filtering)
        elif tab_id is not None:
            return self.get_series_tabla(tab_id,
                                         detail_level=detail_level,
                                         tipology=tipology,
                                         metadata_filtering=metadata_filtering)
        else:
            raise ValueError(
                'Wether serie_id, or op_id, or tab_id must be passed.'
            )

    def get_publications_(self,
                          op_id: int | str | None = None,
                          publication_id: int | str | None = None,
                          detail_level: int = 0,
                          tipology: str = ''):
        """
        Returns the available publications.

        If no input is provided returns the available publications.

        If one operation is provided it returns the available publications
        related to such operation.

        If some publication is provided then it returns the publication dates
        for such publication.
        """
        if op_id is not None:
            return self.get_publicaciones_operacion(op_id,
                                                    detail_level=detail_level,
                                                    tipology=tipology)
        elif publication_id is not None:
            return self.get_publicacionfecha_publicacion(
                publication_id,
                detail_level=detail_level,
                tipology=tipology)
        else:
            return self.get_publicaciones(detail_level=detail_level,
                                          tipology=tipology)

    def get_data_(self,
                  serie_id: int | str | None = None,
                  tab_id: int | str | None = None,
                  op_id: int | str | None = None,
                  detail_level: int = 0,
                  tipology: str = '',
                  count: int | None = None,
                  list_of_dates=None,
                  metadata_filtering=dict()):
        """
        Returns the published data from series.

        if serie is provided it returns the data for such serie.
        if table, it returns all the series and their data of such table
            can provide metadata filtering.
        if operation, metadata_filtering must be provided and returns all the
        data of series that belong to such operation and such
        metadata filtering.
        """
        if serie_id is not None:
            return self.get_datos_serie(serie_id,
                                        detail_level=detail_level,
                                        tipology=tipology,
                                        count=count,
                                        list_of_dates=list_of_dates)
        elif tab_id is not None:
            return self.get_datos_tabla(tab_id,
                                        detail_level=detail_level,
                                        tipology=tipology,
                                        count=count,
                                        list_of_dates=list_of_dates,
                                        metadata_filtering=metadata_filtering)
        elif op_id is not None:
            return self.get_datos_metadataoperacion(
                op_id,
                detail_level=detail_level,
                tipology=tipology,
                count=count,
                list_of_dates=list_of_dates,
                metadata_filtering=metadata_filtering)
        else:
            raise ValueError(
                'Wether serie_id or tab_id or op_id must be passed.'
            )

    def get_units_(self,
                  unit_id: int | str | None = None):
        """Returns all the units or the data of the specified unit."""
        if unit_id is None:
            return self.get_unidades()
        else:
            return self.get_unidad(unit_id)

    def get_scales_(self,
                   scale_id: int | str | None = None,
                   tipology: str = ''):
        """Return all the scales or the data of the specified scale."""
        if scale_id is None:
            return self.get_escalas(tipology=tipology)
        else:
            return self.get_escala(scale_id, tipology=tipology)

    def get_periods_(self,
                    period_id: int | str):
        """Returns the data of the specified period. Same as get_periodo()."""
        return self.get_periodo(period_id)


    def get_periodicities_(self,
                          periodicity_id: int | str | None = None):
        """
        Returns the peridocities.

        If no periodicity is specified it returns all of them.

        If it is specified it returns the data for the specified one.
        """
        if periodicity_id is None:
            return self.get_periodicidades()
        else:
            return self.get_periodicidad(periodicity_id)

    def get_classifications_(self,
                            op_id: int | str | None = None):
        """
        Returns classifications.

        Related to operation if op_id is provided.

        All otherwise.
        """
        if op_id is None:
            return self.get_clasificaciones()
        else:
            return self.get_clasificaciones_operacion(op_id)


class EasyINEAPIClientAsync(INEAPIClientAsync):
    """Same class as INEAPI but with additional methods for easier usage."""

    async def get_operations_(self,
                              op_id: int | str | None = None,
                              detail_level: int = 0,
                              geographical_level: int | None = None,
                              extra_op: bool = False,
                              page: int = 1,
                              tipology: str = ''):
        """
        Returns the data of all operations, or the specified one.

        if extra_op param is set, performs the requests that returns some
        additional operaciones.

        If you specify the op_id it will return the specified operation.
        """
        if op_id is None:
            if extra_op:
                return await self.get_operaciones(detail_level=detail_level,
                                                  page=page,
                                                  tipology=tipology)
            return await self.get_operaciones_disponibles(
                detail_level=detail_level,
                geographical_level=geographical_level,
                page=page,
                tipology=tipology
            )
        else:
            return await self.get_operacion(op_id,
                                            detail_level=detail_level,
                                            tipology=tipology)

    async def get_variables_(self,
                             op_id: int | str | None = None,
                             var_id: int | str | None = None,
                             page: int = 1):
        """
        Returns the available variables.

        If the operation is specified, it returns the variables asociated with
        that operation.

        If a variable is specified, it returns the data for such variable.

        If no param is specified it returns all the available variables.
        """
        if var_id is None:
            if op_id is None:
                return await self.get_variables(page=page)
            else:
                return await self.get_variables_operacion(op_id, page=page)
        else:
            return await self.get_variable(var_id)

    async def get_values_(self,
                          var_id: int | str | None = None,
                          classification_id: int | str | None = None,
                          op_id: int | str | None = None,
                          val_id: int | str | None = None,
                          serie_id: int | str | None = None,
                          tab_id: int | str | None = None,
                          group_id: int | str | None = None,
                          detail_level: int = 0):
        """
        Returns the available values for the specified inputs.

            If var_id is provided.
                It returns the values for such variable.
                    Additionaly, it can be filtered with the classification_id.
            If var_id and val_id is provided.
                It returns the sons values for such value.
            If var_id and val_id is provided.
                It returns the values for such operation.
            If serie_id is provided.
                It returns the values asociated with such serie. The metadata.
            If tab_id and group_id is provided.
                It returns the values for such group of tables.

        All returns are Valor Objects.
        """
        if var_id is not None:
            if val_id is not None:
                return await self.get_valores_hijos(var_id,
                                                    val_id,
                                                    detail_level=detail_level)
            if op_id is None:
                return await self.get_valores_variable(
                    var_id,
                    detail_level=detail_level,
                    classification_id=classification_id)
            else:
                return await self.get_valores_variableoperacion(
                    var_id,
                    op_id,
                    detail_level=detail_level)
        elif serie_id is not None:
            return await self.get_valores_serie(serie_id,
                                                detail_level=detail_level)
        elif tab_id is not None and group_id is not None:
            return await self.get_valores_grupostabla(tab_id,
                                                      group_id,
                                                      detail_level=detail_level)
        else:
            raise ValueError(
                'One input must be provided, var_id, or serie_id or'
                + ' tab_id and group_id.'
            )

    async def get_tables_(self,
                          op_id: int | str | None = None,
                          tab_id: int | str | None = None,
                          detail_level: int = 0,
                          geographical_level: int | None = None,
                          tipology: str = ''):
        """
        Returns the tables or group tables.

            If op_id is provided.
                It returns the tables asociated with such operation.
        """
        if op_id is not None:
            return await self.get_tablas_operacion(
                op_id,
                detail_level=detail_level,
                geographical_level=geographical_level,
                tipology=tipology)
        elif tab_id is not None:
            return await self.get_grupos_tabla(tab_id)
        else:
            raise ValueError('Wether op_id or tab_id must be provided.')

    async def get_series_(self,
                          serie_id: int | str | None = None,
                          op_id: int | str | None = None,
                          tab_id: int | str | None = None,
                          detail_level: int = 0,
                          tipology: str = '',
                          page: int = 1,
                          metadata_filtering=dict()
                          ):
        """
        Returns the available information for the series.

            If serie_id is provided.
                It returns the information for such serie.
            If op_id is provided.
                It returns all the series for such operation and such filters.
            If tab_id is provided.
                It returns all the series for such table and such filters.
        """
        if serie_id is not None:
            return await self.get_serie(serie_id,
                                        detail_level=detail_level,
                                        tipology=tipology)
        elif op_id is not None:
            empty_filters = not bool(metadata_filtering)
            if empty_filters:
                return await self.get_series_operacion(op_id,
                                                       detail_level=detail_level,
                                                       tipology=tipology,
                                                       page=page)
            else:
                return await self.get_serie_metadataoperacion(
                    op_id,
                    detail_level=detail_level,
                    tipology=tipology,
                    metadata_filtering=metadata_filtering)
        elif tab_id is not None:
            return await self.get_series_tabla(tab_id,
                                               detail_level=detail_level,
                                               tipology=tipology,
                                               metadata_filtering=metadata_filtering)
        else:
            raise ValueError(
                'Wether serie_id, or op_id, or tab_id must be passed.'
            )

    async def get_publications_(self,
                                op_id: int | str | None = None,
                                publication_id: int | str | None = None,
                                detail_level: int = 0,
                                tipology: str = ''):
        """
        Returns the available publications.

        If no input is provided returns the available publications.

        If one operation is provided it returns the available publications
        related to such operation.

        If some publication is provided then it returns the publication dates
        for such publication.
        """
        if op_id is not None:
            return await self.get_publicaciones_operacion(
                op_id,
                detail_level=detail_level,
                tipology=tipology)
        elif publication_id is not None:
            return await self.get_publicacionfecha_publicacion(
                publication_id,
                detail_level=detail_level,
                tipology=tipology)
        else:
            return await self.get_publicaciones(detail_level=detail_level,
                                                tipology=tipology)

    async def get_data_(self,
                        serie_id: int | str | None = None,
                        tab_id: int | str | None = None,
                        op_id: int | str | None = None,
                        detail_level: int = 0,
                        tipology: str = '',
                        count: int | None = None,
                        list_of_dates=None,
                        metadata_filtering=dict()):
        """
        Returns the published data from series.

        if serie is provided it returns the data for such serie.
        if table, it returns all the series and their data of such table
            can provide metadata filtering.
        if operation, metadata_filtering must be provided and returns all the
        data of series that belong to such operation and such
        metadata filtering.
        """
        if serie_id is not None:
            return await self.get_datos_serie(serie_id,
                                              detail_level=detail_level,
                                              tipology=tipology,
                                              count=count,
                                              list_of_dates=list_of_dates)
        elif tab_id is not None:
            return await self.get_datos_tabla(
                tab_id,
                detail_level=detail_level,
                tipology=tipology,
                count=count,
                list_of_dates=list_of_dates,
                metadata_filtering=metadata_filtering)
        elif op_id is not None:
            return await self.get_datos_metadataoperacion(
                op_id,
                detail_level=detail_level,
                tipology=tipology,
                count=count,
                list_of_dates=list_of_dates,
                metadata_filtering=metadata_filtering)
        else:
            raise ValueError(
                'Wether serie_id or tab_id or op_id must be passed.'
            )

    async def get_units_(self,
                         unit_id: int | str | None = None):
        """Returns all the units or the data of the specified unit."""
        if unit_id is None:
            return await self.get_unidades()
        else:
            return await self.get_unidad(unit_id)

    async def get_scales_(self,
                          scale_id: int | str | None = None,
                          tipology: str = ''):
        """Return all the scales or the data of the specified scale."""
        if scale_id is None:
            return await self.get_escalas(tipology=tipology)
        else:
            return await self.get_escala(scale_id, tipology=tipology)

    async def get_periods_(self,
                           period_id: int | str | None):
        """Returns the data of the specified period. Same as get_periodo()."""
        return await self.get_periodo(period_id)

    async def get_periodicities_(self,
                                 periodicity_id: int | str | None = None):
        """
        Returns the peridocities.

        If no periodicity is specified it returns all of them.

        If it is specified it returns the data for the specified one.
        """
        if periodicity_id is None:
            return await self.get_periodicidades()
        else:
            return await self.get_periodicidad(periodicity_id)

    async def get_classifications_(self,
                                   op_id: int | str | None = None):
        """
        Returns classifications.

        Related to operation if op_id is provided.

        All otherwise.
        """
        if op_id is None:
            return await self.get_clasificaciones()
        else:
            return await self.get_clasificaciones_operacion(op_id)



