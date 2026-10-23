"""Configuração dos testes: usa um banco SEPARADO e recria os dados antes de cada teste.

Antes de rodar:  createdb artconnect_teste
Rodar:           pytest  (dentro da pasta artconnect)
"""
import os
import sys

PASTA_APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PASTA_APP)
os.chdir(PASTA_APP)

# o banco de teste é apagado e recriado a cada teste: nunca aponte para o banco real
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/artconnect_teste"
)

import pytest

import app as aplicacao
import db
import popular_banco


@pytest.fixture
def cliente():
    popular_banco.popular()
    aplicacao.app.config["TESTING"] = True
    return aplicacao.app.test_client()


def entrar(cliente, username):
    return cliente.post("/login", data={"username": username, "password": popular_banco.SENHA_PADRAO})


def buscar(sql, parametros=()):
    return db.buscar_um(sql, parametros)
