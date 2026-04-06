from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from datetime import datetime
from typing import Union

from models import Base

class Endereco(Base):

    __tablename__ = 'enderecos'
    __table_args__ = (UniqueConstraint("cep", name="unique_cep"),)

    id = Column(Integer, primary_key=True)

    cep = Column(String(8))
    logradouro = Column(String(200))
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(2))

    latitude = Column(Float)
    longitude = Column(Float)

    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, cep, logradouro, bairro, cidade, estado,
                 latitude, longitude,
                 data_insercao: Union[DateTime, None] = None):

        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.latitude = latitude
        self.longitude = longitude

        if data_insercao:
            self.data_insercao = data_insercao

    def to_dict(self):
        return {
            "id": self.id,
            "cep": self.cep,
            "logradouro": self.logradouro,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "data_insercao": self.data_insercao
        }

    def __repr__(self):
        return f"Endereco(id={self.id}, cep='{self.cep}', cidade='{self.cidade}', estado='{self.estado}')"
    