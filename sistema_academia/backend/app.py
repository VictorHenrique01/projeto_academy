from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import crud
from entidades import Aluno, Instrutor, Plano, Equipamento, Turma, Treino
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Criação do banco de dados
Base.metadata.create_all(bind=engine)
# Inicialização do FastAPI
app = FastAPI(title="Sistema de Gerenciamento de Academia", version="1.0.0")
# Middleware CORS
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
# Modelo Pydantic
class AlunoCreate(BaseModel):
   nome: str
   idade: int
   plano_id: int

class PlanoUpdate(BaseModel):
    novo_plano_id: int
# Dependência do banco
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()
# Endpoint para cadastrar aluno
@app.post("/alunos/", status_code=201)
def cadastrar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
   crud.cadastrar_aluno(db, aluno.nome, aluno.idade, aluno.plano_id)
   return {"mensagem": "Aluno cadastrado com sucesso!"}

# Endpoint para consultar aluno pelo nome
@app.get("/alunos", response_description="Consultar um aluno pelo nome")
def consultar_aluno(nome: str, db: Session = Depends(get_db)):
    aluno = crud.consultar_aluno_por_nome(db, nome)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    return aluno

# Endpoints para Treino

@app.get("/treinos/{nome_treino}", response_description="Consultar treinos por tipo")
def consultar_tipo_treino(nome_treino: str, db: Session = Depends(get_db)):
   crud.consultar_tipo_treino(db, nome_treino)
   return {"mensagem": "Consulta de treino concluída"}

# Endpoints para Equipamentos
@app.post("/equipamentos/", response_description="Cadastrar um equipamento")
def cadastrar_equipamento(nome: str, quantidade: int, manutencao: str, db: Session = Depends(get_db)):
   crud.cadastrar_equipamento(db, nome, quantidade, manutencao)
   return {"mensagem": "Equipamento cadastrado com sucesso!"}

@app.get("/equipamentos/{nome_equipamento}", response_description="Consultar equipamento")
def consultar_equipamento(nome_equipamento: str, db: Session = Depends(get_db)):
    # Chama o método do CRUD para consultar o equipamento
    equipamento = crud.consultar_equipamento(db, nome_equipamento)
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado.")
    return equipamento

@app.delete("/equipamentos/{equipamento_id}", response_description="Excluir equipamento")
def excluir_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
   crud.excluir_equipamento(db, equipamento_id)
   return {"mensagem": "Equipamento excluído com sucesso!"}



@app.get("/instrutores/{periodo}", response_description="Consultar disponibilidade de instrutores")
def consultar_disponibilidade_instrutor(periodo: str, db: Session = Depends(get_db)):
   crud.consultar_disponibilidade_instrutor(db, periodo)
   return {"mensagem": "Consulta de instrutores concluída"}

# Endpoints para Planos
@app.post("/planos/", response_description="Cadastrar um plano")
def cadastrar_plano(tipo: str, preco: int, db: Session = Depends(get_db)):
   crud.cadastrar_plano(db, tipo, preco)
   return {"mensagem": "Plano cadastrado com sucesso!"}

@app.put("/planos/{plano_id}", response_description="Editar um plano")
def editar_plano(plano_id: int, tipo: str = None, preco: int = None, db: Session = Depends(get_db)):
   crud.editar_plano(db, plano_id, tipo, preco)
   return {"mensagem": "Plano atualizado com sucesso!"}

@app.delete("/planos/{plano_id}", response_description="Excluir um plano")
def excluir_plano(plano_id: int, db: Session = Depends(get_db)):
   crud.excluir_plano(db, plano_id)
   return {"mensagem": "Plano excluído com sucesso!"}

@app.get("/planos", response_description="Consultar todos os planos disponíveis")
def consultar_todos_planos(db: Session = Depends(get_db)):
    # Chama o método do CRUD para consultar todos os planos
    planos = crud.consultar_todos_planos(db)
    if not planos:
        raise HTTPException(status_code=404, detail="Nenhum plano encontrado.")
    
    # Retorna a lista de planos
    return planos


@app.put("/alunos/{aluno_id}/trocar-plano")
def trocar_plano_aluno(aluno_id: int, plano: PlanoUpdate, db: Session = Depends(get_db)):
    print(f"Recebendo requisição para trocar plano do aluno {aluno_id} para {plano.novo_plano_id}")  # Depuração

    try:
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado.")

        novo_plano = db.query(Plano).filter(Plano.id == plano.novo_plano_id).first()
        if not novo_plano:
            raise HTTPException(status_code=404, detail="Novo plano não encontrado.")

        aluno.plano_id = plano.novo_plano_id
        db.commit()
        db.refresh(aluno)

        return {"mensagem": f"Plano do aluno {aluno_id} alterado para {novo_plano.tipo} com sucesso!"}

    except Exception as e:
        print(f"Erro ao trocar plano do aluno: {e}")  # Depuração
        raise HTTPException(status_code=500, detail=f"Erro ao trocar plano do aluno: {e}")

    
# Endpoints para Turmas

@app.get("/turmas/{turma_id}", response_description="Consultar uma turma")
def consultar_turma(turma_id: int, db: Session = Depends(get_db)):
   crud.consultar_turma(db, turma_id)
   return {"mensagem": "Consulta de turma concluída"}


class TurmaCreate(BaseModel):
    nome: str
    horario: str
    instrutor_id: int

@app.post("/turmas/", response_description="Criar uma turma")
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    crud.criar_turma(db, turma.nome, turma.horario, turma.instrutor_id)
    return {"mensagem": "Turma criada com sucesso!"}

class InstrutorCreate(BaseModel):
    nome: str
    especialidade: str
    horario_trabalho: str

@app.post("/instrutores/", response_description="Cadastrar um instrutor")
def cadastrar_instrutor(instrutor: InstrutorCreate, db: Session = Depends(get_db)):
    crud.cadastrar_instrutor(db, instrutor.nome, instrutor.especialidade, instrutor.horario_trabalho)
    return {"mensagem": "Instrutor cadastrado com sucesso!"}
