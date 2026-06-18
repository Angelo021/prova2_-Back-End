import os 
from typing import Generator, List

from fastapi import Depends, FastAPI, HTTPException, status 
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/produtos_db",
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()
app = FastAPI(title="API de Produtos", version= "1.0.0")

class ProdutoDB(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, index= True)
    preco = Column(Float, nullable= False)
    estoque = Column(Integer, nullable= False, default= 0)
    ativo = Column(Boolean, nullable= False, default= True)

class ProdutoBase(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    preco: float = Field(gt=0)
    estoque: int = Field(default=0, ge= 0)
    ativo: bool = Field(default=True)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoRead(ProdutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

def get_db() -> Generator[Session, None, None]:
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/produtos", response_model=List[ProdutoRead])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).order_by(ProdutoDB.id).all()


@app.post("/produtos", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(
        nome=produto.nome.strip(),
        preco=produto.preco,
        estoque=produto.estoque,
        ativo=produto.ativo,
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.get("/produtos/{produto_id}", response_model=ProdutoRead)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return None
