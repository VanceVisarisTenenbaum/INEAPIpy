# -*- coding: utf-8 -*-

import INEAPIpy.Bridge as Bridge

INE = Bridge.EasyINEAPIClientSync(mode='pydantic')


"""
This file is here just to run every possible option and check everything is
working as intended.
"""


INE.get_operations_()