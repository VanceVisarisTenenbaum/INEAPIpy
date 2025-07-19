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
    Referencia: p.List[pyReferencia] | None = None
    # Not all operations contain this param, and appear only if det>0.


class pyVariable(p.BaseMode):
    """Class model for Variable from INE."""

    Id: int
    Nombre: str
    Codigo: str


class pyValorBase(p.BaseModel):
    """Base because it doesn't have the JerarquiaPadres Keyword."""

    Id: int
    FK_Variable: int | None = None  # Only if det = 0
    T3_Variable: str | None = None  # Only if tip = A, shouldn't appear
    Variable: pyVariable | None  # Only if det>0
    """
    Valor has associated a Variable, this is represented in these params.

    Both are optional, but one of them must input.

    COMPROBAR PYDANTIC QUE OCURRE ALGUNO DE LOS INPUTS VARIABLE O FK_VARIABLE.
    """
    Nombre: str
    Codigo: str
    Nota: str | None = None  # Doesn't appears always.


class pyValor(p.BaseModel, pyValorBase):
    """Extends pyValorBase by adding JerarquiaPadres."""

    FK_JerarquiaPadres: p.List[int] | None = None  # Only if det = 0
    T3_JerarquiaPadres: p.List[str] | None = None  # Only if tip = A,
    # shouldn't appear
    # Not all Valor has this key.
    JerarquiaPadres: p.List[pyValorBase] | None = None
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
    # COMPROBAR SI OCURRE UNO U OTRO
    Dia_inicio: str
    Mes_inicio: str
    Codigo: str
    Nombre: str
    Nombre_largo: str


class pyPublicacionFechaActa(p.BaseModel):
    """Class model for PubFechaAct from INE."""

    Id: int
    Nombre: str
    Fecha: str | int
    FK_Periodo: int | None = None
    T3_Periodo: str | None = None
    Periodo: pyPeriodo | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    Anyo: int


class pyPublicacion(p.BaseModel):
    """Class model for Publicacion from INE."""

    Id: int
    Nombre: str
    FK_Periodicidad: int | None = None
    T3_Periodicidad: str | None = None
    Periodicidad: pyPeriodicidad | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_PubFechaAct: int | None = None
    T3_PubFechaAct: str | None = None
    PubFechaAct: pyPublicacionFechaActa | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    Operacion: p.List[pyOperacion] | None = None


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
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_Periodo: int | None = None
    T3_Periodo: str | None = None
    Periodo: pyPeriodo | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    Anyo: int
    Valor: float
    Secreto: bool


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
    # COMPROBAR SI OCURRE UNO U OTRO
    Notas: p.List[pyNota] | None = None
    MetaData: p.List(pyValor) | None = None
    Data: p.List(pyDato) | None = None


class pySerie(p.BaseModel):
    """Class model for Serie from INE."""

    Id: int
    COD: str
    FK_Operacion: int | None = None
    T3_Operacion: str | None = None
    Operacion: pyOperacion | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    Nombre: str
    Decimales: int
    FK_Periodicidad: int | None = None
    T3_Periodicidad: str | None = None
    Periodicidad: pyPeriodicidad | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_Publicacion: int | None = None
    T3_Publicacion: str | None = None
    Publicacion: pyPublicacion | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_Clasificacion: int | None = None
    T3_Clasificacion: str | None = None
    Clasificacion: pyClasificacion | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_Escala: int | None = None
    T3_Escala: str | None = None
    Escala: pyEscala | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_Unidad: int | None = None
    T3_Unidad: str | None = None
    Unidad: pyUnidad | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    MetaData: p.List[pyValor] | None = None
    # Only if tip = M
    DatosSerie: pyDatosSerie | None = None


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
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_Publicacion: int | None = None
    T3_Publicacion: str | None = None
    Publicacion: pyPublicacion | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    FK_Periodo_ini: int | None = None
    T3_Periodo_ini: str | None = None
    Periodo_ini: pyPeriodo | None = None
    # COMPROBAR SI OCURRE UNO U OTRO
    Anyo_Periodo_ini: str
    FechaRef_fin: int | str
    Ultima_Modificacion: int | str
    GruposTabla: p.List[pyGrupoTabla] | None = None
    Series: p.List[pySerie] | None = None
