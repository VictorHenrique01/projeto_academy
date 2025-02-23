from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    plano_id = Column(Integer, ForeignKey('planos.id'))

    plano = relationship("Plano", back_populates="alunos")
    treinos = relationship("Treino", back_populates="aluno")

# Entidade Instrutor
class Instrutor(Base):
    __tablename__ = 'instrutores'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String)
    horario_trabalho = Column(String)

    # Relacionamento com Turma (um instrutor pode ter várias turmas)
    turmas = relationship("Turma", back_populates="instrutor")
    treinos = relationship("Treino", back_populates="instrutor")

# Entidade Plano
class Plano(Base):
    __tablename__ = 'planos'

    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)  # Ex.: Mensal, Trimestral, Anual
    preco = Column(Integer)

    # Relacionamento com Aluno (um plano pode ter vários alunos)
    alunos = relationship("Aluno", back_populates="plano")

# Entidade Equipamento
class Equipamento(Base):
    __tablename__ = 'equipamentos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer)
    manutencao = Column(String)  # Ex.: Data de última manutenção

# Entidade Turma
class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)  # Nome da aula
    horario = Column(String, nullable=False)  # Horário da aula
    instrutor_id = Column(Integer, ForeignKey('instrutores.id'))

    # Relacionamento com Instrutor (uma turma tem um instrutor responsável)
    instrutor = relationship("Instrutor", back_populates="turmas")

class Treino(Base):
   __tablename__ = 'treinos'
   id = Column(Integer, primary_key=True)
   tipo = Column(String, nullable=False)  # Ex.: Membros Inferiores, Membros Superiores, 
   aluno_id = Column(Integer, ForeignKey('alunos.id'))
   instrutor_id = Column(Integer, ForeignKey('instrutores.id'))
   
   aluno = relationship("Aluno", back_populates="treinos")
   instrutor = relationship("Instrutor", back_populates="treinos")
