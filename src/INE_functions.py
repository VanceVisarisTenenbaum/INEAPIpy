# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:46:00 2025

@author: mano
"""

"""
This file contains all the functions from the INE as they are, but instead
of returning the result from the input, they build the corresponding url.

They are all described here: https://www.ine.es/dyngs/DAB/index.htm?cid=1100
"""

import INE_Filtering as filtering


def datos_tabla(tab_id,
                detail_level=0,
                tipology='',
                count=None,
                list_of_dates=None,
                metadata_filtering=dict()
                ):
    """
    Function from INE.

    Parameters
    ----------
    tab_id : TYPE
        DESCRIPTION.
    detail_level : TYPE, optional
        DESCRIPTION. The default is 0.
    tipology : TYPE, optional
        DESCRIPTION. The default is ''.
    count : TYPE, optional
        DESCRIPTION. The default is None.
    list_of_dates : TYPE, optional
        DESCRIPTION. The default is None.
    metadata_filtering : TYPE, optional
        DESCRIPTION. The default is dict().

    Returns
    -------
    URL : yarl.URL
        Built URL.

    """

    return URL