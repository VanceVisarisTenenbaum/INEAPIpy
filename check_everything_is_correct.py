# -*- coding: utf-8 -*-

import INEAPIpy.Bridge as Bridge

INE = Bridge.EasyINEAPIClientSync(mode='pydantic')


"""
This file is here just to run every possible option and check everything is
working as intended.

Not many checks needed, since pydantic already does the checks.
If pydantic fails there is something wrong.
"""


# Ops
print('Operaciones')
INE.get_operations_(detail_level=2, extra_op=True, page=1)
INE.get_operations_(geographical_level=0)
INE.get_operations_(geographical_level=1)

INE.get_operations_(25)
INE.get_operations_('IPC')

# Vars
print('Variables')
INE.get_variables_(page=2)
INE.get_variables_(25)
INE.get_variables_(None, 115)

print('Valores')
INE.get_values_(115)
INE.get_values_(19, 107)
INE.get_values_(762, None, 25)
INE.get_values_(70, val_id=8997)


#INE.close_all_sessions()