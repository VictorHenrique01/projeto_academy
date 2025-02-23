# crud.py
from sqlalchemy.orm import Session
from entidades import Aluno, Instrutor, Plano, Equipamento, Turma, Treino

# CRUD para Aluno
def cadastrar_aluno(db: Session, nome: str, idade: int, plano_id: int):
    try:
        aluno = Aluno(nome=nome, idade=idade, plano_id=plano_id)
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        print("Aluno cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar aluno: {e}")


def consultar_aluno_por_nome(db: Session, nome: str):
    try:
        aluno = db.query(Aluno).filter(Aluno.nome.ilike(f"%{nome}%")).first()
        if aluno:
            print(f"Aluno ID: {aluno.id}\n Nome: {aluno.nome}\n Idade: {aluno.idade}\n Plano ID: {aluno.plano_id}")
            return aluno
        else:
            print("Aluno não encontrado.")
            return None
    except Exception as e:
        print(f"Erro ao consultar aluno: {e}")
        return None

# Editar Dados do Aluno
def editar_aluno(db: Session, aluno_id: int, nome: str = None, idade: int = None, plano_id: int = None):
    try:
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if aluno:
            if nome:
                aluno.nome = nome
            if idade:
                aluno.idade = idade
            if plano_id:
                aluno.plano_id = plano_id
            db.commit()
            db.refresh(aluno)
            print("Dados do aluno atualizados com sucesso!")
        else:
            print("Aluno não encontrado.")
    except Exception as e:
        print(f"Erro ao editar aluno: {e}")

def criar_treino(db: Session, tipo: str, aluno_id: int, instrutor_id: int):
   try:
       treino = Treino(tipo=tipo, aluno_id=aluno_id, instrutor_id=instrutor_id)
       db.add(treino)
       db.commit()
       print("Treino criado com sucesso!")
   except Exception as e:
       db.rollback()
       print(f"Erro ao criar treino: {e}")

#----------------------------------------------------------------------------------------------------
#Criei uma lista de equipamentos necessárioss para cd tipo de treino que o usuário escolher lá no term

def mostrar_equipamentos_sugeridos(tipo):
   equipamentos_por_treino = {
       "Membros Inferiores": ["Leg Press", "Cadeira Extensora", "Cadeira Flexora"],
       "Membros Superiores": ["Supino", "Pulley", "Máquina de Peito"],
       "Costas e Bíceps": ["Remada Baixa", "Halteres", "Pulley"],
       "Peito e Tríceps": ["Supino", "Polia", "Barras"],
       "Quadríceps": ["Cadeira Extensora", "Barra Guiada Smith", "Halteres", "Bancos para Musculação"],
       "Pernas Completo": ["Leg Press", "Cadeira Flexora", "Cadeira Abdutora"],
       "Ombros e Abdômen": ["Abdominal Máquina", "Halteres", "Máquina Ombro"],
       "Corpo Inteiro (Full Body)": ["Anilhas", "Halteres", "Mesa Posterior", "Leg Press 45 graus", "Bancos para Musculação"],
       "Cardio": ["Esteira", "Bicicleta Ergométrica"],
       "Flexibilidade": ["Colchonetes para Alongamento", "Bola de Pilates", "Elásticos de Resistência"]
   }
   equipamentos = equipamentos_por_treino.get(tipo, [])
   if equipamentos:
       print("-------------------------------------------------------------------------")
       print(f"Equipamentos sugeridos para treino de {tipo}:")
       for equipamento in equipamentos:
           print(f"- {equipamento}")
   else:
       print("Nenhum equipamento sugerido para este tipo de treino.")

# Cadastrar Instrutor
def cadastrar_instrutor(db: Session, nome: str, especialidade: str, horario_trabalho: str):
    try:
        instrutor = Instrutor(nome=nome, especialidade = especialidade, horario_trabalho=horario_trabalho)
        db.add(instrutor)
        db.commit()
        db.refresh(instrutor)
        print("Instrutor cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar instrutor: {e}")


def consultar_disponibilidade_instrutor(db: Session, periodo: str):
    try:
        instrutores = db.query(Instrutor).filter(Instrutor.horario_trabalho == periodo).all()
        if instrutores:
            print(f"Instrutores(as) disponíveis no período {periodo}:")
            for instrutor in instrutores:
                print(f"- {instrutor.nome} (Especialidade: {instrutor.especialidade} | ID do instrutor(a): {instrutor.id})")
        else:
            print(f"Nenhum(a) instrutor(a) disponível no período {periodo}.")
    except Exception as e:
        print(f"Erro ao consultar disponibilidade de instrutores(as): {e}")
        

def cadastrar_plano(db: Session, tipo: str, preco: int):
    try:
        plano = Plano(tipo=tipo, preco=preco)
        db.add(plano)
        db.commit()
        db.refresh(plano)
        print("Plano cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar plano: {e}")

def editar_plano(db: Session, plano_id: int, tipo: str = None, preco: int = None):
    try:
        plano = db.query(Plano).filter(Plano.id == plano_id).first()
        if plano:
            if tipo:
                plano.tipo = tipo
            if preco:
                plano.preco = preco
            db.commit()
            db.refresh(plano)
            print("Plano atualizado com sucesso!")
        else:
            print("Plano não encontrado.")
    except Exception as e:
        print(f"Erro ao editar plano: {e}")

def excluir_plano(db: Session, plano_id: int):
    try:
        plano = db.query(Plano).filter(Plano.id == plano_id).first()
        if plano:
            db.delete(plano)
            db.commit()
            print("Plano excluído com sucesso!")
        else:
            print("Plano não encontrado.")
    except Exception as e:
        print(f"Erro ao excluir plano: {e}")

def consultar_todos_planos(db: Session):
    try:
        planos = db.query(Plano).all()  # Recupera todos os planos
        return planos  # Retorna a lista de planos
    except Exception as e:
        print(f"Erro ao consultar planos: {e}")
        return None


def trocar_plano_aluno(db: Session, aluno_id: int, novo_plano_id: int):
    try:
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()  # Procurar o aluno pelo ID
        if aluno:
            novo_plano = db.query(Plano).filter(Plano.id == novo_plano_id).first()  # Procurar o novo plano pelo ID
            if novo_plano:
                aluno.plano_id = novo_plano_id  # Atualiza o plano do aluno
                db.commit()
                db.refresh(aluno)  # Atualiza o objeto aluno
                print(f"Plano do aluno {aluno.nome} alterado para {novo_plano.tipo} com sucesso!")
            else:
                print("Novo plano não encontrado.")
        else:
            print("Aluno não encontrado.")
    except Exception as e:
        print(f"Erro ao trocar plano do aluno: {e}")


# Reservar Aula Coletiva (Associação entre Aluno e Turma)
def criar_turma(db: Session, nome: str, horario: str, instrutor_id: int):
    try:
        turma = Turma(nome=nome, horario=horario, instrutor_id=instrutor_id)
        db.add(turma)
        db.commit()
        db.refresh(turma)
        print("Turma criada com sucesso!")
    except Exception as e:
        print(f"Erro ao criar turma: {e}")

# Controle de Equipamentos 
def cadastrar_equipamento(db: Session, nome: str, quantidade: int, manutencao: str):
    try:
        equipamento = Equipamento(nome=nome, quantidade=quantidade, manutencao=manutencao)
        db.add(equipamento)
        db.commit()
        print("Equipamento cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar equipamento: {e}")

def consultar_equipamento(db: Session, nome_equipamento: str):
    try:
        equipamento = db.query(Equipamento).filter(Equipamento.nome == nome_equipamento).first()
        if equipamento:
            return {
                "nome": equipamento.nome,
                "quantidade": equipamento.quantidade,
                "manutencao": equipamento.manutencao
            }
        return None
    except Exception as e:
        print(f"Erro ao consultar equipamento: {e}")
        return None


def excluir_equipamento(db: Session, equipamento_id: int):
    try:
        equipamento = db.query(Equipamento).filter(Equipamento.id == equipamento_id).first()
        if equipamento:
            db.delete(equipamento)
            db.commit()
            print("Equipamento excluído com sucesso!")
        else:
            print("Equipamento não encontrado.")
    except Exception as e:
        print(f"Erro ao excluir equipamento: {e}")

# Consulta de turm pelo id
def consultar_turma(db: Session, turma_id: int):
   try:
       turma = db.query(Turma).filter(Turma.id == turma_id).first()
       if turma:
           print(f"Turma ID: {turma.id}\n Nome: {turma.nome}\n Horário: {turma.horario}\n Instrutor ID: {turma.instrutor_id}")
       else:
           print("Turma não encontrada.")
   except Exception as e:
       print(f"Erro ao consultar turma: {e}")


def consultar_tipo_treino(db: Session, nome_treino: str):
    try:
        treinos = db.query(Treino).filter(Treino.tipo == nome_treino).all()
        if treinos:
            print(f" Tipo de treino: {nome_treino}")
            for treino in treinos:
                print(f"* {treino.tipo} -- Para ID Aluno: {treino.aluno_id} | Criado por ID Instrutor: {treino.instrutor_id}")
        else:
            print(f"Nenhum treino existente na academia para o membro do corpo: {nome_treino}.")
    except Exception as e:
        print(f"Erro ao consultar tipo de treino: {e}")
