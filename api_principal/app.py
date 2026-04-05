from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from models import Session, Endereco
from schemas import *

import requests

info = Info(title="API de CEP", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

tag_home = Tag(name="Home", description="Rota inicial da API")
tag_endereco = Tag(name="Endereço", description="Operações relacionadas a endereços")

# ROTAS
@app.get("/", tags=[tag_home])
def home():
    """Rota inicial da API."""
    return redirect("/openapi")


@app.post('/endereco', tags=[tag_endereco],
          responses={"200": EnderecoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_endereco(form: EnderecoSchema):
    cep = form.cep

    try:
        # ViaCEP
        viacep = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()

        if "erro" in viacep:
            return {"message": "CEP inválido"}, 400

        cidade = viacep.get("localidade")
        estado = viacep.get("uf")
        logradouro = viacep.get("logradouro")
        bairro = viacep.get("bairro")

        # Nominatim (CORRIGIDO)
        headers = {"User-Agent": "api-cep-projeto"}
        geo = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": f"{cidade}, {estado}, Brazil",
                "format": "json"
            },
            headers=headers
        ).json()

        if not geo:
            return {"message": "Erro ao buscar coordenadas"}, 400

        lat = float(geo[0]["lat"])
        lon = float(geo[0]["lon"])

        endereco = Endereco(
            cep=cep,
            logradouro=logradouro,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            latitude=lat,
            longitude=lon
        )

        session = Session()
        session.add(endereco)
        session.commit()

        return {"msg": "Endereço salvo"}
    
    except Exception as e:
        print("ERRO REAL:", e)
        return {"message": str(e)}, 500


@app.get('/enderecos', tags=[tag_endereco],
         responses={"200": ListagemEnderecosSchema})
def get_enderecos():
    """Lista todos os endereços cadastrados"""
    
    session = Session()
    enderecos = session.query(Endereco).all()

    if not enderecos:
        return {"enderecos": []}, 200

    return apresenta_enderecos(enderecos), 200


@app.get('/endereco', tags=[tag_endereco],
         responses={"200": EnderecoViewSchema, "404": ErrorSchema})
def get_endereco(query: EnderecoBuscaPorIDSchema):
    """Busca um endereço pelo ID"""
    
    endereco_id = query.id

    session = Session()
    endereco = session.query(Endereco).filter(Endereco.id == endereco_id).first()

    if not endereco:
        return {"message": "Endereço não encontrado"}, 404

    return apresenta_endereco(endereco), 200,


@app.get('/enderecos/busca', tags=[tag_endereco])
def busca_endereco(query: EnderecoBuscaPorEstadoSchema):
    """Busca endereços pelo Estado"""

    estado = query.estado

    session = Session()

    enderecos = session.query(Endereco)\
        .filter(Endereco.estado == estado)\
        .all()

    if not enderecos:
        return {"message": "Endereço(s) não encontrado(s)"}, 200

    return apresenta_enderecos(enderecos), 200


@app.delete('/endereco', tags=[tag_endereco],
            responses={"200": EnderecoDelSchema, "404": ErrorSchema})
def delete_endereco(query: EnderecoBuscaPorIDSchema):
    """Deleta um endereço a partir do ID"""

    endereco_id = query.id

    session = Session()

    # busca o endereço
    endereco = session.query(Endereco).filter(Endereco.id == endereco_id).first()

    if not endereco:
        return {"message": "Endereço não encontrado"}, 404

    # remove
    session.delete(endereco)
    session.commit()

    return {"message": "Endereço removido", "id": endereco_id}, 200


@app.put('/endereco', tags=[tag_endereco],
         responses={"200": EnderecoViewSchema, "404": ErrorSchema})
def update_endereco(form: EnderecoUpdateSchema):
    """Atualiza um endereço com base no novo CEP"""

    try:
        session = Session()

        endereco = session.query(Endereco).filter(Endereco.id == form.id).first()

        if not endereco:
            return {"message": "Endereço não encontrado"}, 404

        novo_cep = form.cep

        # ViaCEP
        viacep = requests.get(f"https://viacep.com.br/ws/{novo_cep}/json/").json()

        if "erro" in viacep:
            return {"message": "CEP inválido"}, 400

        cidade = viacep.get("localidade")
        estado = viacep.get("uf")
        logradouro = viacep.get("logradouro")
        bairro = viacep.get("bairro")

        # Nominatim
        headers = {"User-Agent": "api-cep-projeto"}
        geo = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": f"{cidade}, {estado}, Brazil",
                "format": "json"
            },
            headers=headers
        ).json()

        if not geo:
            return {"message": "Erro ao buscar coordenadas"}, 400

        lat = float(geo[0]["lat"])
        lon = float(geo[0]["lon"])

        # Atualiza os dados
        endereco.cep = novo_cep
        endereco.logradouro = logradouro
        endereco.bairro = bairro
        endereco.cidade = cidade
        endereco.estado = estado
        endereco.latitude = lat
        endereco.longitude = lon

        session.commit()

        return apresenta_endereco(endereco), 200

    except Exception as e:
        print("ERRO:", e)
        return {"message": str(e)}, 500
    


@app.get('/distancia')
def calcular_distancia_enderecos(query: DistanciaSchema):
    session = Session()

    e1 = session.query(Endereco).filter(Endereco.id == query.id1).first()
    e2 = session.query(Endereco).filter(Endereco.id == query.id2).first()

    if not e1 or not e2:
        return {"message": "Endereço não encontrado"}, 404

    response = requests.get(
        "http://secundaria:5001/distancia",
        params={
            "lat1": e1.latitude,
            "lon1": e1.longitude,
            "lat2": e2.latitude,
            "lon2": e2.longitude
        }
    ).json()

    return response
