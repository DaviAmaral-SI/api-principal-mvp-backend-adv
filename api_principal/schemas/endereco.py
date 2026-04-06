from pydantic import BaseModel
from typing import Optional, List
from models.endereco import Endereco
from enum import Enum

class EstadoEnum(str, Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"

class EnderecoSchema(BaseModel):
    """Define como um novo endereço deve ser enviado"""
    cep: str = "01001000"

class EnderecoViewSchema(BaseModel):
    """Define como um endereço será retornado"""
    id: int = 1
    cep: str = "01001000"
    logradouro: str = "Praça da Sé"
    bairro: str = "Sé"
    cidade: str = "São Paulo"
    estado: str = "SP"
    latitude: float = -23.55
    longitude: float = -46.63

class ListagemEnderecosSchema(BaseModel):
    """Define como uma lista de endereços será retornada"""
    enderecos: List[EnderecoViewSchema]

class EnderecoBuscaPorIDSchema(BaseModel):
    id: int = 1

class EnderecoBuscaPorEstadoSchema(BaseModel):
    estado: EstadoEnum = EstadoEnum.AC

class EnderecoDelSchema(BaseModel):
    message: str
    id: int

class EnderecoUpdateSchema(BaseModel):
    id: int
    cep: str

class DistanciaSchema(BaseModel):
    id1: int
    id2: int

def apresenta_enderecos(enderecos):
    result = []
    for e in enderecos:
        result.append({
            "id": e.id,
            "cep": e.cep,
            "logradouro": e.logradouro,
            "bairro": e.bairro,
            "cidade": e.cidade,
            "estado": e.estado,
            "latitude": e.latitude,
            "longitude": e.longitude
        })
    return {"enderecos": result}

def apresenta_endereco(endereco):
    return {
        "id": endereco.id,
        "cep": endereco.cep,
        "logradouro": endereco.logradouro,
        "bairro": endereco.bairro,
        "cidade": endereco.cidade,
        "estado": endereco.estado,
        "latitude": endereco.latitude,
        "longitude": endereco.longitude
    }