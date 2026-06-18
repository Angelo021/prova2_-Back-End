# API de Produtos

Este projeto implementa uma API REST com FastAPI, SQLAlchemy e PostgreSQL, além de uma suíte de testes automatizados com Pytest.

## 1. Subir o banco de teste com Docker

Antes de executar os testes, suba o banco de dados exclusivo para testes:

```bash
docker-compose up -d dbtest
```

Se quiser verificar se o container está saudável, execute:

```bash
docker ps
```

ou:

```bash
docker-compose ps
```

## 2. Comando exato para executar os testes

Para rodar toda a suíte de testes, use:

```bash
pytest
```

Se quiser rodar com cobertura:

```bash
pytest --cov=main --cov-report=term-missing
```

## 3. Saída esperada do pytest

Exemplo de saída esperada ao executar `pytest`:

```txt
============================= test session starts =============================
collected 11 items

tests/test_produtos.py ...........

============================== 11 passed in 1.23s =============================
```

## 4. Isolamento entre testes

O isolamento é garantido pela fixture `client` definida em `conftest.py`.

Ela funciona assim:
- cria as tabelas com `Base.metadata.create_all()` antes do teste;
- substitui a dependência `get_db` com `app.dependency_overrides`;
- usa `TestClient` para executar as requisições;
- remove as tabelas com `Base.metadata.drop_all()` no teardown.

Isso faz com que cada teste execute em um banco limpo, sem depender de dados deixados por testes anteriores.

## Endpoints da API

- `GET /produtos`
- `POST /produtos`
- `GET /produtos/{id}`
- `DELETE /produtos/{id}`