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
import INE_functions as f


def get_data_process_sync(RM,
                          url: str,
                          mode: str):
    """
    Get the data from INE URL.

    Must pass the request manager instance to make the request.

    Returns the data in the specified format by mode.

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
    content = RM.sync_request('GET', url)
    return content

class INEAPIClientSync():
    """
    Wrapper for INE API, makes requests using sync requests package.

    All methods make the request and retreive the results.
    """

    def __init__(self, mode='raw'):
        """
        Init of class.

        Mode: Literal['raw', 'py', 'pydantic']

            raw: returns the result straight from INE API, without checking.
            py: returns the result as python dict
            pydantic: returns the result as python dict and checks everything
                is correct using pydantic.
        """
        if mode not in ['raw', 'py', 'pydantic']:
            raise ValueError(
                "mode can't be different from raw, py or pydantic."
            )
        self.mode = mode
        return None

    def get_datos_tabla(self,
                        tab_id: int | str,
                        detail_level: int = 0,
                        tipology: str = '',
                        count: int | None = None,
                        list_of_dates=None,
                        metadata_filtering=dict()
                        ):
        return None
