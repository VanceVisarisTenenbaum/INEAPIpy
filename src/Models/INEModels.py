# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 18:40:32 2025

@author: mano

This file contains all the models that the INE API returns.

They all start as py to avoid matching names with INE API outputs keys.

INE API has the option for tip=A, refering to amigable (friendly), it only
changes foreign keys for tempus3 names, the output will change as specified:
    FK_"something" --> T3_"something"
    FK or foreign key refers to the Id while
    T3 refers to Cod_IOE.
This means that if you see T3 or FK, they represent the same, but with
different names.
"""

import typing as ty
import pydantic as p


class pyReferencia(p.BaseModel):
    """
    Class model for Referencia from INE.

    Referencia only appears when asking from Operacion, and it is related
    only to Operacion.
    """

    Id: int
    Titulo: str
    Url: str


class pyOperacion(p.BaseModel):
    """Class model for Operacion from INE."""

    Id: int
    Cod_IOE: str
    Nombre: str
    Codigo: str
    Url: str | None = None  # Not all operations have this param.
    Referencia: ty.List[pyReferencia] | None = None
    # Not all operations contain this param, and appear only if det>0.


class pyVariable(p.BaseMode):
    """Class model for Variable from INE."""

    Id: int
    Nombre: str
    Codigo: str


def check_if_all_are_None(
        *options,
        name=''):
    """
    Checks if all options are None.

    Raises ValueError if all are.

    name optional param is simply a name to print when the error si raised.
    For simplification on debugging.

    Parameters
    ----------
    *options : Any
        Options to check.
    name : str, optional
        String to print when raising the error. The default is ''.

    Raises
    ------
    ValueError
        Error meaning that all options where None.

    Returns
    -------
    None.

    """
    checks = [v is None for v in options]
    if all(checks):
        raise ValueError(f'All values are None.\n---Debug message: {name}')
    return None


class pyValorBase(p.BaseModel):
    """Base because it doesn't have the JerarquiaPadres Keyword."""

    Id: int
    FK_Variable: int | None = None  # Only if det = 0
    T3_Variable: str | None = None  # Only if tip = A, shouldn't appear
    Variable: pyVariable | None  # Only if det>0
    """
    Valor has associated a Variable, this is represented in these params.

    These three are optional, but one of them must input.
    """
    Nombre: str
    Codigo: str
    Nota: str | None = None  # Doesn't appears always.

    @p.model_validator('after')
    def checks(self):
        """
        Checks if FK, T3, or Variable are all None.

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_Variable,
            self.T3_Variable,
            self.Variable,
            name='pyValorBase'
        )

        return self


class pyValor(pyValorBase):
    """Extends pyValorBase by adding JerarquiaPadres."""

    FK_JerarquiaPadres: ty.List[int] | None = None  # Only if det = 0
    T3_JerarquiaPadres: ty.List[str] | None = None  # Only if tip = A,
    # shouldn't appear
    # Not all Valor has this key.
    JerarquiaPadres: ty.List[pyValorBase] | None = None
    """No need to check if one of both happens since they may not appear."""


class pyPeriodicidad(p.BaseModel):
    """Class model for Periodicidad from INE."""

    Id: int
    Nombre: str
    Codigo: str


class pyPeriodo(p.BaseModel):
    """Class model fof Periodo from INE."""

    Id: int
    Valor: int  # This Valor has nothing to do with pyValor.
    FK_Periodicidad: int | None = None
    T3_Periodicidad: str | None = None
    Periodicidad: pyPeriodicidad | None
    Dia_inicio: str
    Mes_inicio: str
    Codigo: str
    Nombre: str
    Nombre_largo: str

    @p.model_validator('after')
    def checks(self):
        """
        Checks if FK, T3, or Periodicidad are all None.

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_Periodicidad,
            self.T3_Periodicidad,
            self.Periodicidad,
            name='pyPeriodo'
        )

        return self


class pyPublicacionFechaActa(p.BaseModel):
    """Class model for PubFechaAct from INE."""

    Id: int
    Nombre: str
    Fecha: str | int
    FK_Periodo: int | None = None
    T3_Periodo: str | None = None
    Periodo: pyPeriodo | None = None
    Anyo: int

    @p.model_validator('after')
    def checks(self):
        """
        Checks if FK, T3, or Periodo are all None.

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_Periodo,
            self.T3_Periodo,
            self.Periodo,
            name='pyPublicacionFechaActa'
        )

        return self


class pyPublicacion(p.BaseModel):
    """Class model for Publicacion from INE."""

    Id: int
    Nombre: str
    FK_Periodicidad: int | None = None
    T3_Periodicidad: str | None = None
    Periodicidad: pyPeriodicidad | None = None
    FK_PubFechaAct: int | None = None
    T3_PubFechaAct: str | None = None
    PubFechaAct: pyPublicacionFechaActa | None = None
    Operacion: ty.List[pyOperacion] | None = None

    @p.model_validator('after')
    def checks(self):
        """
        Checks None for both Periodicidad and PubFechaAct

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_Periodicidad,
            self.T3_Periodicidad,
            self.Periodicidad,
            name='pyPublicacion -- Periodicidad'
        )
        check_if_all_are_None(
            self.FK_PubFechaAct,
            self.T3_PubFechaAct,
            self.PubFechaAct,
            name='pyPublicacion -- PubFechaAct'
        )

        return self


class pyClasificacion(p.BaseModel):
    """Class model for Clasificacion from INE."""

    Id: int
    Nombre: str
    Fecha: str  # COMPROBAR POR QUE PONE DATE EN MMD


class pyUnidad(p.BaseModel):
    """Class model for Unidad from INE."""

    Id: int
    Nombre: str
    Codigo: str
    Abrev: str


class pyEscala(p.BaseModel):
    """Class model for Escala from INE."""

    Id: int
    Nombre: str
    Codigo: str
    Abrev: str
    Factor: float  # COMPROBAR POR QUE PONE FLOAT(STR) EN MMD


class pyTipoDato(p.BaseModel):
    """Class model for TipoDato."""

    Id: int
    Nombre: str
    Codigo: str


class pyDato(p.BaseModel):
    """Class model for Dato from INE."""

    Fecha: str  # COMPROBAR PORQUE PONE DATE EN MMD
    FK_TipoDato: int | None = None
    T3_TipoDato: str | None = None
    TipoDato: pyTipoDato | None = None
    FK_Periodo: int | None = None
    T3_Periodo: str | None = None
    Periodo: pyPeriodo | None = None
    Anyo: int
    Valor: float
    Secreto: bool

    @p.model_validator('after')
    def checks(self):
        """
        Checks if all None for TipoDato and Periodo.

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_TipoDato,
            self.T3_TipoDato,
            self.TipoDato,
            name='pyDato -- TipoDato'
        )
        check_if_all_are_None(
            self.FK_Periodo,
            self.T3_Periodo,
            self.Periodo,
            name='pyDato -- Periodo'
        )

        return self


class pyNota(p.BaseModel):
    """Class model for Nota from INE."""

    texto: str
    Fk_TipoNota: int  # Yes this one is Fk, not FK.
    Nombre_TipoNota: str | None  # Only appears if det>0
    textoTipo: str | None  # Appears but it can be null.


class pyDatosSerie(p.BaseModel):
    """
    Class model for Data from INE.

    Similar to Serie (defined a bit later), but missing some metadata.
    It is defined this way for simplicity. MMD Diagram is cleaner than text
    definition.
    """

    COD: str
    Nombre: str
    FK_Unidad: int | None = None
    T3_Unidad: str | None = None
    Unidad: pyUnidad | None = None
    Notas: ty.List[pyNota] | None = None
    MetaData: ty.List(pyValor) | None = None
    Data: ty.List(pyDato) | None = None

    @p.model_validator('after')
    def checks(self):
        """
        Checks if FK, T3, or Unidad are all None.

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_Unidad,
            self.T3_Unidad,
            self.Unidad,
            name='pyDatosSerie'
        )

        return self


class pySerie(p.BaseModel):
    """Class model for Serie from INE."""

    Id: int
    COD: str
    FK_Operacion: int | None = None
    T3_Operacion: str | None = None
    Operacion: pyOperacion | None = None
    Nombre: str
    Decimales: int
    FK_Periodicidad: int | None = None
    T3_Periodicidad: str | None = None
    Periodicidad: pyPeriodicidad | None = None
    FK_Publicacion: int | None = None
    T3_Publicacion: str | None = None
    Publicacion: pyPublicacion | None = None
    FK_Clasificacion: int | None = None
    T3_Clasificacion: str | None = None
    Clasificacion: pyClasificacion | None = None
    FK_Escala: int | None = None
    T3_Escala: str | None = None
    Escala: pyEscala | None = None
    FK_Unidad: int | None = None
    T3_Unidad: str | None = None
    Unidad: pyUnidad | None = None
    MetaData: ty.List[pyValor] | None = None
    # Only if tip = M
    DatosSerie: pyDatosSerie | None = None

    @p.model_validator('after')
    def checks(self):
        """
        Checks if all None for next attributes.

            Operacion
            Periodicidad
            Publicacion
            Clasificacion
            Escala
            Unidad

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_Operacion,
            self.T3_Operacion,
            self.Operacion,
            name='pySerie -- Operacion'
        )
        check_if_all_are_None(
            self.FK_Periodicidad,
            self.T3_Periodicidad,
            self.Periodicidad,
            name='pySerie -- Periodicidad'
        )
        check_if_all_are_None(
            self.FK_Publicacion,
            self.T3_Publicacion,
            self.Publicacion,
            name='pySerie -- Publicacion'
        )
        check_if_all_are_None(
            self.FK_Clasificacion,
            self.T3_Clasificacion,
            self.Clasificacion,
            name='pySerie -- Clasificacion'
        )
        check_if_all_are_None(
            self.FK_Escala,
            self.T3_Escala,
            self.Escala,
            name='pySerie -- Escala'
        )
        check_if_all_are_None(
            self.FK_Unidad,
            self.T3_Unidad,
            self.Unidad,
            name='pySerie -- Unidad'
        )

        return self


class pyGrupoTabla(p.BaseModel):
    """Class model for GrupoTabla from INE."""

    Id: int
    Nombre: str


class pyTabla(p.BaseModel):
    """Class model for Tabla from INE."""

    Id: int
    Nombre: str
    Codigo: str
    FK_Periodicidad: int | None = None
    T3_Periodicidad: str | None = None
    Periodicidad: pyPeriodicidad | None = None
    FK_Publicacion: int | None = None
    T3_Publicacion: str | None = None
    Publicacion: pyPublicacion | None = None
    FK_Periodo_ini: int | None = None
    T3_Periodo_ini: str | None = None
    Periodo_ini: pyPeriodo | None = None
    Anyo_Periodo_ini: str
    FechaRef_fin: int | str
    Ultima_Modificacion: int | str
    GruposTabla: ty.List[pyGrupoTabla] | None = None
    Series: ty.List[pySerie] | None = None

    @p.model_validator('after')
    def checks(self):
        """
        Checks if all None for next attributes.

            Periodicidad
            Publicacion
            Periodo_ini

        Returns
        -------
        self
        """
        check_if_all_are_None(
            self.FK_Periodicidad,
            self.T3_Periodicidad,
            self.Periodicidad,
            name='pyTabla -- Periodicidad'
        )
        check_if_all_are_None(
            self.FK_Publicacion,
            self.T3_Publicacion,
            self.Publicacion,
            name='pyTabla -- Publicacion'
        )
        check_if_all_are_None(
            self.FK_Periodo_ini,
            self.T3_Periodo_ini,
            self.Periodo_ini,
            name='pyTabla -- Periodo_ini'
        )

        return self
