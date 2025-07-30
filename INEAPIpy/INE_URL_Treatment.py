# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 19:16:02 2025

@author: mano

This file contains all the functions necesary to build a url valid for INE API.

The only useful function is url_gen, which treats positional args as a list
of path elements of a url and kwargs as parameters for the url.
"""

import yarl
from .Models import URLModels as URLModels


def url_gen(function, *inputs, **kwargs):
    """
    Generates a url valid for INE API.

    Takes a INE function, the inputs for such function, and the query params
    required for filtering and selecting outputs.

    for example
        function = 'SERIES_OPERACION'
        inputs = 25
        page=1
        det=2
        tip=A

        would return
            https://servicios.ine.es/wstempus/js/ES/SERIES_OPERACION/25?page=1&det=2&tip=A

    Parameters
    ----------
    function : str
        function from INE API.
    *inputs : str | int
        Inputs for function.
    **kwargs : int | str
        Query params for INE API URL

    Returns
    -------
    str
        Generated URL valid for INE API.

    """
    Inputs = URLModels.InputModel(
        function=function,
        path=inputs,
        query=kwargs
    )
    url = yarl.URL.build(
        scheme='https',
        host='servicios.ine.es'
    )
    url = url.joinpath(Inputs.path)
    url = url.with_query(Inputs.query)
    final_url = str(url)
    # Pydantic check and transformation
    Output = URLModels.URLModel(url=final_url)
    return Output.url
