# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 18:14:21 2025

@author: mano
"""

import pydantic as p


class InputParams(p.BaseModel):
    """Class model to check valid function inputs."""

    # API Information Config
    detail_level: p.NonNegativeInt = 0  # Int>=0
    # In practice, detail_level shouldnt be greater than 3, but it may work.
    tipology: p.Literal['', 'A', 'M', 'AM'] = ''
    geographical_level: p.NonNegativeInt = 0  # Int>=0

    # API variables options.
    op_id: int | None = None  # Operation Id
    var_id: int | None = None  # Variable Id
    val_id: int | None = None  # Value Id
    tab_id: int | None = None  # Table Id
    group_id: int | None = None  # Table Group Id
    serie_id: int | None = None  # Serie Id

    """
    There is no need for any additional check since this model is used to
    check that the inputs were correct.
    """
