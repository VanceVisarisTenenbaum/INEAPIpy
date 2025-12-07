# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:55:13 2025

@author: mano

This file contains the functions needed for creating the filtering params
for INE API.
"""

import datetime as dt
from .Models import FunctionInputsModels as FIM


def metadata_param_filtering_builder(var_value_dict: dict | None = None,
                                     format_: str = 'series'):
    """
    Transforms the input dictionary into a dictionary valid for the API.

    This function receives a dictionary of shape
        variable_id : [value_id,...]
        publicacion: publication_id

    and will return a dictionary of the shape:
        tv1:"variable_id:value_id_1"
        tv2:"variable_id:value_id_2"

    or of the shape:
        g1:"variable_id:value_id_1"
        g2:"variable_id:value_id_2"

    depending on format param

    If format is series it will be the first option.
    If it is metadata it will return the second option.

    If there is a key named "periodicidad" and a value that is not a list
    it will be the second and will add the next:
        p:periodicity_id

    If periodicidad is not in keys and the value of some keys is not a list
    they will be skipped

    If empty it will return empty dict.
    """
    if var_value_dict is None:
        return dict()
    if not isinstance(var_value_dict, dict):
        return dict()

    # Pydantic checks
    Inputs = FIM.FilteringInputs(
        var_value_dict=var_value_dict,
        format_=format_)

    var_value_dict = Inputs.var_value_dict.root  # root attribute needed.
    format_ = Inputs.format_

    if format_ == 'metadata':
        key_base = 'g'
    elif format_ == 'series':
        key_base = 'tv'

    params_dict = dict()
    counter = 1
    # Loop the input dict and transform it and save it to params_dict
    for i, (k, v) in enumerate(var_value_dict.items()):
        # k is a variable Id or publicacion
        # v is a list of value_id or id of publicacion
        # The only special case is publicacion.
        if k == 'periodicidad':
            if format_ == 'series':
                raise ValueError(
                    "periodicidad can't be a key if format_ is series"
                )
            params_dict['p'] = str(v)  # To str in case it is an int.
            continue
        else:
            # In any other case, the value is a list.
            for val in v:
                params_dict[f'{key_base}{counter}'] = f'{k}:{val}'
                counter += 1
            if len(v) == 0:
                params_dict[f'{key_base}{counter}'] = f'{k}:'
                counter += 1

    return params_dict


def date_count_selection_params_builder(list_of_dates: list | None = None,
                                        count: int | None = None,
                                        page: int = 1
                                        ):
    """
    Builds filtering params valid for the INE API.

    Takes the input of dates or count and builds a dictionary valid
    for the filtering params of the INE API.

    The resulting dict will be
    {
         'date1': 'YYYYmmdd'
         'date2': 'YYYYmmdd:',
         'date3': ':YYYYmmdd',
         'date4': 'YYYYmmdd:YYYYmmdd',
    }

    or

    {
         'nult': count
    }

    depending on inputs.

    Parameters
    ----------
    list_of_dates : List, optional
        List of dates to filter. The default is None.
    count : int, optional
        N first elements to retreive from. The default is None.

    Raises
    ------
    ValueError
        DESCRIPTION.
    TypeError
        DESCRIPTION.

    Returns
    -------
    params_dict : TYPE
        DESCRIPTION.

    """
    if list_of_dates is None and count is None and page is None:
        raise ValueError(
            'At least one must be provided, count or dates or page.'
        )
    # pydantic checks. This raises error if input isn't correctly shaped.
    Inputs = FIM.FilteringInputs(
        list_of_dates=list_of_dates, count=count,
        page=page
    )

    list_of_dates = Inputs.list_of_dates  # Values are transformed by pydantic.
    count = Inputs.count
    page = Inputs.page

    params_dict = dict()  # To store the data.
    if list_of_dates is not None:
        # Recorremos la lista
        for i, date in enumerate(list_of_dates):
            # date is a datetime or an ordered tuple of datetimes
            if isinstance(date, FIM.customDate):
                v = date.date_val.strftime('%Y%m%d')
                # v is the value we will set for the dict.
            elif isinstance(date, FIM.customDateRange):
                start = date.start_date
                end = date.end_date
                if start is None:
                    start_date = ''
                else:
                    start_date = start.strftime('%Y%m%d')
                if end is None:
                    end_date = ''
                else:
                    end_date = end.strftime('%Y%m%d')

                v = f'{start_date}:{end_date}'

            key = f'date{i}'
            params_dict[key] = v
    elif count is not None:
        params_dict['nult'] = count
    elif page != 1:
        params_dict['page'] = page

    return params_dict


def metadata_and_date_filtering(var_value_dict: dict | None = None,
                                format_: str = 'series',
                                list_of_dates: list | None = None,
                                count: int | None = None):
    """Runs both previous functions and concats both dict."""
    newdict = dict()
    newdict.update(
        metadata_param_filtering_builder(
            var_value_dict=var_value_dict,
            format_=format_
        )
    )
    newdict.update(
        date_count_selection_params_builder(
            list_of_dates=list_of_dates,
            count=count
        )
    )
    return newdict
