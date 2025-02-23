# main.py
from sqlalchemy.orm import Session
from database import SessionLocal  # Importa a função de sessão
import crud


def main():
    db = SessionLocal()  # Cria uma sessão para o banco de dados
    
    while True:
        print("\n|------------------------- ⚒ Bem-vindo ao Sistema de Gerenciamento de Academia ⚒ -------------------------|\n")
        print("0. Para sair do sistema")
        print("1. Cadastrar Aluno(a)")
        print("2. Editar Dados do Aluno(a)")
        print("3. Criar treino para aluno(a)")
        print("4. Cadastrar Instrutor(a)")
        print("5. Verificar disponibilidade do(a) instrutor(a)")
        print("6. Cadastrar Plano")
        print("7. Editar Plano")
        print("8. Excluir plano")
        print("9. Cadastrar equipamento")
        print("10. Verificar disponibilidade do equipamento")
        print("11. Criar turma")
        print("12. Consultar turma")
        print("13. Consultar Aluno(a)")
        print("14. Consultar tipo de treino")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Nome do Aluno: ")
            idade = int(input("Idade do Aluno: "))
            plano_id = int(input("ID do Plano: "))
            crud.cadastrar_aluno(db, nome, idade, plano_id)

        elif escolha == "2":
            aluno_id = int(input("ID do Aluno: "))
            nome = input("Novo Nome do Aluno (ou Enter para manter): ")
            idade = input("Nova Idade do Aluno (ou Enter para manter): ")
            plano_id = input("Novo ID do Plano (ou Enter para manter): ")
            crud.editar_aluno(db, aluno_id, nome if nome else None, int(idade) if idade else None, int(plano_id) if plano_id else None)

        elif escolha == "3":
               print("Escolha o tipo de treino: \n")

               tipos_treino = {  
                    
                   "1": "Membros Inferiores",
                   "2": "Membros Superiores",
                   "3": "Costas e Bíceps",
                   "4": "Peito e Tríceps",
                   "5": "Quadríceps",
                   "6": "Pernas Completo",
                   "7": "Ombros e Abdômen",
                   "8": "Corpo Inteiro (Full Body)",
                   "9": "Cardio",
                   "10": "Flexibilidade"

                }

               for chave, valor in tipos_treino.items():
                   print(f"{chave}. {valor}")

               tipo_escolha = input("Digite o número do tipo de treino desejado: ")
               tipo = tipos_treino.get(tipo_escolha, "Outro")

               crud.mostrar_equipamentos_sugeridos(tipo)
            
               aluno_id = int(input("\nID do(a) Aluno(a): "))
               instrutor_id = int(input("ID do(a) Instrutor(a): "))
               crud.criar_treino(db, tipo, aluno_id, instrutor_id)


        elif escolha == "4":
            nome = input("Nome do(a) Instrutor(a): ")
            especialidade = input("Especialidade do instrutor(a): ")
            horario_trabalho = input("Trabalha em qual período? | Digite uma das opções abaixo:\nManhã, Tarde ou Noite? ")
            crud.cadastrar_instrutor(db, nome, especialidade, horario_trabalho)

        elif escolha == "5":
            periodo = input("Qual período deseja verificar a disponibilidade dos instrutores? (Manhã, Tarde ou Noite): ").capitalize()
            crud.consultar_disponibilidade_instrutor(db, periodo)

        elif escolha == "6":
            tipo = input("Digite o tipo de plano desejado conforme as opções abaixo:\nMensal, Trimestral, Semestral ou Anual? ")
            preco = int(input("Preço do Plano: "))
            crud.cadastrar_plano(db, tipo, preco)

        elif escolha == "7":
            plano_id = int(input("ID do Plano: "))
            tipo = input("Novo tipo do Plano (ou Enter para manter): ")
            preco = input("Novo preço do Plano (ou Enter para manter): ")
            crud.editar_plano(db, plano_id, tipo if tipo else None, int(preco) if preco else None)

        elif escolha == "8":
            plano_id = int(input("ID do Plano para excluir: "))
            crud.excluir_plano(db, plano_id)

        elif escolha == "9":
            nome = input("Nome do equipamento: ")   
            quantidade = int(input("Quantidade desse equipamento: "))  
            manutencao = input("Data da última manutenção feita no equipamento: ") 
            crud.cadastrar_equipamento(db, nome, quantidade, manutencao)  

        elif escolha == "10":
            nome_equipamento = input("Nome do Equipamento para verificar disponibilidade: ")
            crud.consultar_equipamento(db, nome_equipamento)


        elif escolha == "11":
            nome = input("Nome da Turma conforme a sua especialidade: ")
            horario = input("Horário da aula: ")
            instrutor_id = int(input("ID do instrutor: "))
            crud.criar_turma(db, nome, horario, instrutor_id)

        elif escolha == "12":
            turma_id = int(input("ID da turma específica que deseja consultar: "))
            crud.consultar_turma(db, turma_id)

        elif escolha == "13":
            aluno_id = int(input("ID do aluno para consulta: "))
            crud.consultar_aluno(db, aluno_id)
        
        elif escolha == "14":
            nome_treino = input("Qual treino deseja consultar? (Insira o nome do tipo de treino criado): ")
            crud.consultar_tipo_treino(db, nome_treino)

        elif escolha == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    db.close()  # Fecha a sessão ao sair

if __name__ == "__main__":
    main()
