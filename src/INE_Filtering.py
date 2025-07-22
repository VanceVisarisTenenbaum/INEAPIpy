# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:55:13 2025

@author: mano
"""


"""
This file contains the functions needed for creating the filtering params
for INE API.
"""

import datetime as dt

def metadata_param_filtering_builder(self,
                                     var_value_dict=None,
                                     format_='series'):
    """
    Transforms the input dictionary into a dictionary valid for the API.

    This function receives a dictionary of shape
        variable_id : [value_id,...]

    and will return a dictionary of the shape:
        tv1:"variable_id:value_id_1"
        tv2:"variable_id:value_id_2"

    or of the shape:
        g1:"variable_id:value_id_1"
        g2:"variable_id:value_id_2"

    depending on format param

    If format is series it will be the first option.
    If it is metadata it will return the second option.

    If there is a key named "publicacion" and a value that is not a list
    it will be the second and will add the next:
        p:publication_id

    If publication is not in keys and the value of some keys is not a list
    they will be skipped

    If empty it will return empty dict.
    """
    if var_value_dict is None:
        return dict()
    if not isinstance(var_value_dict, dict):
        return dict()

    if format_ == 'series':
        key_base = 'tv'
    elif format_ == 'metadata':
        key_base = 'g'
    else:
        raise ValueError(
            'format_ param can only be "series" or "metadata".'
        )

    params_dict = dict()
    counter = 1
    # Loop the input dict and transform it and save it to params_dict
    for i, (k, v) in enumerate(var_value_dict.items()):
        # The only special case is publicacion.
        if k == 'publicacion':
            if type(v) not in [int, str]:
                raise ValueError(
                    'The input for publicacion must be an '
                    + 'integer or a string.'
                )
            params_dict['p'] = str(v)  # To str in case it is an int.
            continue
        else:
            if isinstance(v, list):
                for val in v:
                    params_dict[f'{key_base}{counter}'] = f'{k}:{val}'
                    counter += 1
            else:
                raise ValueError(
                    f'Your metadata input for key {k} was {v},'
                    + ' it must be a list.'
                )

    return params_dict

def date_count_selection_params_builder(self,
                                        list_of_dates=None,
                                        count=None):
    """
    Builds filtering params valid for the INE API

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
    if list_of_dates is None and count is None:
        raise ValueError('At least count or date range must be provided.')

    params_dict = dict()
    if list_of_dates is not None:
        if not isinstance(list_of_dates, list):
            raise TypeError('list of dates must be a list.')
        # Recorremos la lista
        for i, date in enumerate(list_of_dates):
            """
            each value in the list must be
                datetime
                str: %Y-%m-%d
                tuple: 2 elements of datetime, str or None
                    (date,None)
                    (None,date)
                    (date,date)
                    this indicates a range instead of particular dates.
            """

            if type(date) not in [str, dt.datetime, tuple]:
                raise TypeError(
                    'Dates must be a string, a datetime or a tuple.'
                )

            if isinstance(date, str):
                # if input is a string we just transform it to datetime
                try:
                    v = dt.datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('datetime string must match %Y-%m-%v')
            elif isinstance(date, tuple):
                # if tuple we transform to string "start_date:end_date"
                if len(date) != 2:
                    raise ValueError(
                        'tuple of dates must be of two dates.'
                        + ' In case you dont want one you can set None'
                    )
                start_date = date[0]
                end_date = date[1]

                if start_date is None and end_date is None:
                    raise ValueError(
                        'At least one value must be provided.'
                    )

                if start_date is None:
                    start_date = ''
                if end_date is None:
                    end_date = ''

                if type(start_date) not in [str, dt.datetime]:
                    raise TypeError(
                        'start date must be a string or a datetime.'
                    )
                if type(end_date) not in [str, dt.datetime]:
                    raise TypeError(
                        'end date must be a string or a datetime.'
                    )

                if start_date != '' and isinstance(start_date, str):
                    try:
                        start_date = dt.datetime.strptime(date[0],
                                                          '%Y-%m-%d')
                    except ValueError:
                        raise ValueError(
                            'start date datetime string must match'
                            + ' %Y-%m-%v'
                        )

                if end_date != '' and isinstance(end_date, str):
                    try:
                        end_date = dt.datetime.strptime(date[1],
                                                        '%Y-%m-%d')
                    except ValueError:
                        raise ValueError(
                            'end date datetime string must match %Y-%m-%v'
                        )

                if isinstance(start_date, dt.datetime):
                    start_date = start_date.strftime('%Y-%m-%d')
                if isinstance(end_date, dt.datetime):
                    end_date = end_date.strftime('%Y-%m-%d')

                v = f'{start_date}:{end_date}'
            elif isinstance(date, dt.datetime):
                v = date
            else:
                raise ValueError('This should not happen.')

            key = f'date{i}'
            params_dict[key] = v
    elif count is not None:
        if isinstance(count, int):
            raise TypeError('count param must be an integer.')
        params_dict['nult'] = count

    return params_dict

