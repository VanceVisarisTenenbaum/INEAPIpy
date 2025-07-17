# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 18:14:21 2025

@author: mano
"""

import pydantic as p

class InputParams(p.BaseModel):
    detail_level: int | None = None
    tipology: Literal[]
