# -*- coding: utf-8 -*-

import INEAPIpy.Bridge as Bridge
import time
import asyncio

INES = Bridge.EasyINEAPIClientSync(mode='pydantic', print_url=True, sleep_time=1)
INEA = Bridge.EasyINEAPIClientAsync(mode='pydantic', print_url=True, sleep_time=1)

"""
This file is here just to run every possible option and check everything is
working as intended.

Not many checks needed, since pydantic already does the checks.
If pydantic fails there is something wrong.
"""


def tests_Sync(INE):
    """All tests."""

    # Ops
    print('Operaciones')
    start = time.time()
    INE.get_operations_(detail_level=2, extra_op=True, page=1)
    INE.get_operations_(geographical_level=0)
    INE.get_operations_(geographical_level=1)

    INE.get_operations_(25)
    INE.get_operations_('IPC')
    end = time.time()
    print(f'Elapsed time: {end - start}')
    # Vars
    print('Variables')
    start = time.time()
    INE.get_variables_(page=2)
    INE.get_variables_(25)
    INE.get_variables_(None, 115)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Valores')
    start = time.time()
    INE.get_values_(115, detail_level=2)
    # INE.get_values_(19, 107)  # Funciona bie, silenciado por tardar demasiado.
    INE.get_values_(762, None, 25)
    INE.get_values_(70, val_id=8997)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Tablas')
    start = time.time()
    INE.get_tables_('IPC')
    INE.get_tables_(tab_id=50913)
    INE.get_tables_(tab_id=50913, group_id=110924, detail_level=2)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Series')
    start = time.time()
    INE.get_series_('IPC251852', detail_level=2, tipology='AM', serie_data='metadata')
    INE.get_series_('IPC251852', detail_level=2, tipology='AM', serie_data='values')
    INE.get_series_(op_id=25, detail_level=2, page=2, operation_data='series')
    INE.get_series_(op_id=25, detail_level=2, page=2, operation_data='metadata',
                    metadata_filtering={
                        115: [29],
                        3: [84],
                        'publicacion': 1
                    })
    INE.get_series_(tab_id=50913)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Publicaciones')
    INE.get_publications_(detail_level=2, tipology='AM')
    INE.get_publications_('IPC')
    INE.get_publications_(publication_id=8, detail_level=2)


    print('UNIDADES')
    INE.get_units_()
    INE.get_units_(11)

    print('Periodos')
    INE.get_periods_(8)

    print('Periodicidades')
    INE.get_periodicities_()
    INE.get_periodicities_(12)

    print('Clasificaciones')
    INE.get_classifications_()

    print('Datos')
    start = time.time()
    INE.get_data_('IPC251856', detail_level=2, tipology='M', count=20)
    INE.get_data_('IPC251856', detail_level=2, tipology='M',
                  list_of_dates=[('2023-01-01', '2023-12-31')])
    INE.get_data_(tab_id=50902, detail_level=2)
    INE.get_data_(op_id='IPC', count=1,
                  metadata_filtering={
                      115: [29],
                      3: [84],
                      762: [],
                      'publicacion': 1
                  },
                  detail_level=2)
    end = time.time()
    print(f'Elapsed time: {end - start}')
    INE.close_all_sessions()

    return None


async def tests_Async(INE):
    """All tests."""

    # Ops
    print('Operaciones')
    start = time.time()
    await INE.get_operations_(detail_level=2, extra_op=True, page=1)
    await INE.get_operations_(geographical_level=0)
    await INE.get_operations_(geographical_level=1)

    await INE.get_operations_(25)
    await INE.get_operations_('IPC')
    end = time.time()
    print(f'Elapsed time: {end - start}')
    # Vars
    print('Variables')
    start = time.time()
    await INE.get_variables_(page=2)
    await INE.get_variables_(25)
    await INE.get_variables_(None, 115)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Valores')
    start = time.time()
    await INE.get_values_(115, detail_level=2)
    # INE.get_values_(19, 107)  # Funciona bie, silenciado por tardar demasiado.
    await INE.get_values_(762, None, 25)
    await INE.get_values_(70, val_id=8997)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Tablas')
    start = time.time()
    await INE.get_tables_('IPC')
    await INE.get_tables_(tab_id=50913)
    await INE.get_tables_(tab_id=50913, group_id=110924, detail_level=2)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Series')
    start = time.time()
    await INE.get_series_('IPC251852', detail_level=2, tipology='AM', serie_data='metadata')
    await INE.get_series_('IPC251852', detail_level=2, tipology='AM', serie_data='values')
    await INE.get_series_(op_id=25, detail_level=2, page=2, operation_data='series')
    await INE.get_series_(op_id=25, detail_level=2, page=2, operation_data='metadata',
                    metadata_filtering={
                        115: [29],
                        3: [84],
                        'publicacion': 1
                    })
    await INE.get_series_(tab_id=50913)
    end = time.time()
    print(f'Elapsed time: {end - start}')

    print('Publicaciones')
    await INE.get_publications_(detail_level=2, tipology='AM')
    await INE.get_publications_('IPC')
    await INE.get_publications_(publication_id=8, detail_level=2)


    print('UNIDADES')
    await INE.get_units_()
    await INE.get_units_(11)

    print('Periodos')
    await INE.get_periods_(8)

    print('Periodicidades')
    await INE.get_periodicities_()
    await INE.get_periodicities_(12)

    print('Clasificaciones')
    await INE.get_classifications_()

    print('Datos')
    start = time.time()
    await INE.get_data_('IPC251856', detail_level=2, tipology='M', count=20)
    await INE.get_data_('IPC251856', detail_level=2, tipology='M',
                  list_of_dates=[('2023-01-01', '2023-12-31')])
    await INE.get_data_(tab_id=50902, detail_level=2)
    await INE.get_data_(op_id='IPC', count=1,
                  metadata_filtering={
                      115: [29],
                      3: [84],
                      762: [],
                      'publicacion': 1
                  },
                  detail_level=2)
    end = time.time()
    print(f'Elapsed time: {end - start}')
    INE.close_all_sessions()

    return None


print('Startin Sync tests.')
tests_Sync(INES)

print('Startin Async tests.')
asyncio.create_task(tests_Async(INEA))
