# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 18:14:21 2025

@author: mano
"""

import typing as ty
import pydantic as p
import datetime as dt


class InputParams(p.BaseModel):
    """Class model to check valid function inputs."""

    # API Information Config
    detail_level: p.NonNegativeInt = 0  # Int>=0
    # In practice, detail_level shouldnt be greater than 3, but it may work.
    tipology: ty.Literal['', 'A', 'M', 'AM'] = ''
    geographical_level: p.NonNegativeInt | None = None  # Int>=0 or None

    # API variables options.
    op_id: int | str | None = None  # Operation Id
    var_id: int | str | None = None  # Variable Id
    val_id: int | str | None = None  # Value Id
    tab_id: int | str | None = None  # Table Id
    group_id: int | str | None = None  # Table Group Id
    serie_id: int | str | None = None  # Serie Id
    unit_id: int | str | None = None  # Unit Id
    scale_id: int | str | None = None  # Scale Id
    period_id: int | str | None = None  # Period Id
    periodicity_id: int | str | None = None  # Periodicity Id
    classification_id: int | str | None = None  # Classification Id
    publication_id: int | str | None = None  # Publication Id

    """
    There is no need for any additional check since this model is used to
    check that the inputs were correct.
    """

    @p.model_validator(mode='after')
    def __build_params(self):
        """
        Builds API Information Config inputs as a dict.

        The resulting Dict is valid to use as URL query.
        """
        self.__params = dict()
        # We skip the defaults since there is no need to provide them in the
        # url
        if self.detail_level != 0:
            self.__params['det'] = self.detail_level
        if self.tipology != '':
            self.__params['tip'] = self.tipology
        if self.geographical_level is not None:
            self.__params['geo'] = self.geographical_level
        return self

    def get_params(self, add_clasif=False):
        """
        Returns API Information Config params as a dict if necessary.

        If add_clasif param is true, adds the classification_id as a param
        to the dictionary if it is not None.
        """
        if add_clasif:
            if self.classification_id is not None:
                self.__params['clasif'] = self.classification_id
        return self.__params

    def join_filtering_params(self, filtering_params, add_clasif=False):
        """
        Returns API Config params plus the filtering params from input.

        Doesn't alter the input params.
        """
        newdict = dict(self.get_params(add_clasif))  # Dict to make a copy.
        newdict.update(dict(filtering_params))
        return newdict


class VarValueDictModel(p.RootModel):
    """Class model to check proper shape of input dict for metadata filters."""

    root: ty.Dict[int | str, ty.List[int | str] | str | int]
    # I doubt there is any negative Id, but we don't know.
    """
    This accepts any dict with values as int or str at any point.
    but we want that only the key publicacion has that type.
    """

    @p.model_validator(mode='after')
    def __publication_check(self):
        """
        Raises error if it finds any key other than periodicidad isn't a list.

        Any key value must be a list.
        Only key publicacion can have a value that is a str or int.
        """
        for k, v in self.root.items():
            if k == 'periodicidad':
                if isinstance(v, list):
                    raise TypeError(
                        'Value for periodicidad must be an int or str.'
                    )
            else:
                if not isinstance(v, list):
                    raise TypeError(
                        'Values of dict must be a list except for periodicidad.'
                    )
        return self


class customDate(p.BaseModel):
    """Class model for dates. This exist just to perform the date checks."""

    date_val: dt.datetime | str | None

    @p.field_validator('date_val', mode='after')
    @classmethod
    def date_transform(cls, val):
        """
        Takes a value and transform it to a datetime is possible.

        Parameters
        ----------
        val : datetime or str of shape %Y-%m-%d
            Value to transform to datetime.

        Returns
        -------
        new_val : datetime.datetime
            Input value transformed as datetime.

        """
        if val is None:
            return val
        elif isinstance(val, dt.datetime):
            return val
        elif isinstance(val, str):
            # datetime already raises ValueError if it doesn't have the proper
            # format %Y-%m-%d
            return dt.datetime.strptime(val, '%Y-%m-%d')
        # else shouldn't happen cause this validation occurs after the
        # pydantic validation, which forces the val to be str or datetime.


class customDateRange(p.BaseModel):
    """Class model to handle date ranges formats."""
    start_date: customDate = None
    end_date: customDate = None

    @p.model_validator(mode='after')
    def __reorder_date_range(self):
        """Orders ascendingly the date range if needed."""
        # First we extract the datetimes from customDate
        self.start_date = self.start_date.date_val
        self.end_date = self.end_date.date_val

        if self.start_date is not None and self.end_date is not None:

            first_date = min(self.start_date, self.end_date)
            second_date = max(self.start_date, self.end_date)
            if first_date == second_date:
                raise ValueError("Both dates can't be the same.")
            self.start_date = first_date
            self.end_date = second_date
        return self


class ListOfDates(p.BaseModel):
    """
    Class model to transform possible date formats.

    This class takes as input a list of dates or date ranges that may come
    with different formats.

    These formats are the next (also explained in the INE filtering module):
        each value in the list must be
            datetime
            str: %Y-%m-%d
            tuple: 2 elements of datetime, str or None
                (date,None) from date until today.
                (None,date) from any time until date.
                (date,date) from first date until second date (chrono order).
                this indicates a range instead of particular dates.
    """


class FilteringInputs(p.BaseModel):
    """Class model to check valid filtering function inputs."""

    # Metadata filtering.
    # Metadata filtering inputs are a dictionary and string specifying the
    # shape of the output.
    """
    Already specified in the respective function.

    var_value_dict is a dict of shape
    {
         variable_id_1: [value_id_1_1, value_id_2_1, ..., value_id_m_1],
         variable_id_2: [value_id_1_2, value_id_2_2, ..., value_id_m_2],
         .
         .
         .
         variable_id_n: [value_id_1_n, value_id_2_n, ..., value_id_m_n],
         # With the additional possible key.
         publicacion:publication_id
     }

    """
    var_value_dict: VarValueDictModel | None = None
    format_: ty.Literal['series', 'metadata'] = 'series'
    # Data quantity filtering.
    """
    These formats are the next (also explained in the INE filtering module):
        each value in the list must be
            datetime
            str: %Y-%m-%d
            tuple: 2 elements of datetime, str or None
                (date,None) from date until today.
                (None,date) from any time until date.
                (date,date) from first date until second date (chrono order).
                this indicates a range instead of particular dates.
    """
    list_of_dates: ty.List[str | ty.List[str | None] | ty.Tuple[str | None]] | None = None
    count: p.PositiveInt | None = None

    page: p.PositiveInt = 1

    @p.field_validator('list_of_dates', mode='after')
    @classmethod
    def __correct_list_of_dates(cls, list_):
        """Transforms the list of dates to valid dates."""
        if list_ is None:
            return list_
        corrected_list = list()
        for d in list_:
            if isinstance(d, str):
                corrected_list.append(customDate(date_val=d))
            elif isinstance(d, list) or isinstance(d, tuple):
                corrected_list.append(customDateRange(
                    start_date=customDate(date_val=d[0]),
                    end_date=customDate(date_val=d[1])
                ))
        return corrected_list