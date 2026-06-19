import pytest


def test_listar_produtos_vazio(client):
    resposta = client.get("/produtos")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_criar_produto_persiste_no_banco(client):
    resposta = client.post(
        "/produtos",
        json={"nome": "Mouse", "preco": 99.9, "estoque": 5, "ativo": True},
    )
    assert resposta.status_code == 201
    body = resposta.json()
    assert body["id"] > 0
    assert body["nome"] == "Mouse"


def test_criar_produto_aparece_na_listagem(client):
    client.post(
        "/produtos",
        json={"nome": "Monitor", "preco": 899.9, "estoque": 2, "ativo": True},
    )
    resposta = client.get("/produtos")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["nome"] == "Monitor"


def test_buscar_produto_por_id_sucesso(produto_existente, client):
    resposta = client.get(f"/produtos/{produto_existente['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == produto_existente["id"]


def test_buscar_produto_inexistente_retorna_404(client):
    resposta = client.get("/produtos/99999")
    assert resposta.status_code == 404


def test_deletar_produto_retorna_204(produto_existente, client):
    resposta = client.delete(f"/produtos/{produto_existente['id']}")
    assert resposta.status_code == 204


def test_deletar_produto_e_confirmar_remocao(produto_existente, client):
    resposta_delete = client.delete(f"/produtos/{produto_existente['id']}")
    assert resposta_delete.status_code == 204
    resposta_get = client.get(f"/produtos/{produto_existente['id']}")
    assert resposta_get.status_code == 404


def test_deletar_produto_inexistente_retorna_404(client):
    resposta = client.delete("/produtos/99999")
    assert resposta.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco": 10.0, "estoque": 1, "ativo": True},
        {"nome": "Produto", "preco": 0, "estoque": 1, "ativo": True},
        {"nome": "Produto", "preco": -10, "estoque": 1, "ativo": True},
        {"nome": "Produto", "preco": 10.0, "estoque": -1, "ativo": True},
    ],
)
def test_payloads_invalidos_retorna_422(client, payload):
    resposta = client.post("/produtos", json=payload)
    assert resposta.status_code == 422


def test_estoque_default_zero(client):
    resposta = client.post(
        "/produtos",
        json={"nome": "Webcam", "preco": 150.0, "ativo": True},
    )
    assert resposta.status_code == 201
    assert resposta.json()["estoque"] == 0


def test_ativo_default_true(client):
    resposta = client.post(
        "/produtos",
        json={"nome": "Headset", "preco": 200.0},
    )
    assert resposta.status_code == 201
    assert resposta.json()["ativo"] is True


def test_isolamento_entre_testes(client):
    resposta = client.get("/produtos")
    assert resposta.status_code == 200
    assert resposta.json() == []