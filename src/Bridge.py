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


class INEAPIClientSync():
    """Wrapper for INE API, makes requests using sync requests package."""

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