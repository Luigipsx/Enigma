from getpass import getpass
from sqlalchemy import select
from .database import criar_sessao
from .models import Enigma, Tentativa


def ler_inteiro(mensagem, minimo=None):
    """Lê um número inteiro sem deixar o programa quebrar."""
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue

            return valor

        except ValueError:
            print("Digite apenas um número inteiro.")


def inserir_enigma(session):
    print("\n--- Novo Enigma ---")

    titulo = input("Título: ").strip()

    if not titulo:
        print("O título não pode ficar vazio.")
        return

    descricao = input("Descrição: ").strip()

    if not descricao:
        print("A descrição não pode ficar vazia.")
        return

    resposta = input("Resposta: ").strip()

    if not resposta:
        print("A resposta não pode ficar vazia.")
        return

    limite = ler_inteiro(
        "Limite de tentativas: ",
        minimo=1
    )

    enigma = Enigma(
        titulo=titulo,
        descricao=descricao,
        resposta=resposta,
        limite_tentativas=limite,
        resolvido=False
    )

    try:
        session.add(enigma)
        session.commit()
        print("\nEnigma cadastrado com sucesso!")

    except Exception as erro:
        session.rollback()
        print(f"\nErro ao cadastrar enigma: {erro}")


def listar_enigmas(session, mostrar_resposta=False):
    print("\n--- Enigmas ---")

    enigmas = session.scalars(
        select(Enigma).order_by(Enigma.id)
    ).all()

    if not enigmas:
        print("Nenhum enigma cadastrado.")
        return False

    for enigma in enigmas:
        print(
            f"\nID: {enigma.id}"
            f"\nTítulo: {enigma.titulo}"
            f"\nDescrição: {enigma.descricao}"
            f"\nLimite de tentativas: {enigma.limite_tentativas}"
            f"\nResolvido: {'Sim' if enigma.resolvido else 'Não'}"
        )

        # A resposta só é mostrada quando for realmente necessário.
        if mostrar_resposta:
            print(f"Resposta: {enigma.resposta}")

    return True


def excluir_enigma(session):
    print("\n--- Excluir Enigma ---")

    if not listar_enigmas(session):
        return

    id_enigma = ler_inteiro("\nID do enigma que deseja excluir: ", minimo=1)

    enigma = session.get(Enigma, id_enigma)

    if enigma is None:
        print("Enigma não encontrado.")
        return

    confirmacao = input(
        f"Tem certeza que deseja excluir '{enigma.titulo}'? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    try:
        session.delete(enigma)
        session.commit()

        print("Enigma excluído com sucesso!")

    except Exception as erro:
        session.rollback()
        print(f"Erro ao excluir enigma: {erro}")


def inserir_tentativa(session):
    print("\n--- Nova Tentativa ---")

    if not listar_enigmas(session):
        return

    enigma_id = ler_inteiro(
        "\nID do enigma: ",
        minimo=1
    )

    enigma = session.get(Enigma, enigma_id)

    if enigma is None:
        print("Enigma não encontrado.")
        return

    # Atualiza a lista de tentativas do enigma.
    tentativas = session.scalars(
        select(Tentativa)
        .where(Tentativa.enigma_id == enigma.id)
        .order_by(Tentativa.numero_tentativa)
    ).all()

    numero = len(tentativas) + 1

    if numero > enigma.limite_tentativas:
        print(
            f"\nLimite de {enigma.limite_tentativas} "
            "tentativas já foi atingido."
        )
        return

    print(
        f"\nTentativa {numero} de "
        f"{enigma.limite_tentativas}"
    )

    # getpass evita que a resposta digitada fique visível no terminal.
    resposta_informada = getpass(
        "Digite sua resposta: "
    ).strip()

    if not resposta_informada:
        print("A resposta não pode ficar vazia.")
        return

    acertou = (
        resposta_informada.casefold()
        == enigma.resposta.strip().casefold()
    )

    resultado = "acertou" if acertou else "errou"

    tentativa = Tentativa(
        enigma_id=enigma.id,
        resposta_informada=resposta_informada,
        numero_tentativa=numero,
        resultado=resultado
    )

    if acertou:
        enigma.resolvido = True

    try:
        session.add(tentativa)
        session.commit()

        print("\n=================================")
        print(f"Resultado: {resultado.upper()}")
        print("=================================")

        if acertou:
            print("Parabéns! Você resolveu o enigma.")
        else:
            tentativas_restantes = (
                enigma.limite_tentativas - numero
            )

            if tentativas_restantes > 0:
                print(
                    f"Você ainda possui "
                    f"{tentativas_restantes} tentativa(s)."
                )
            else:
                print("Você atingiu o limite de tentativas.")

    except Exception as erro:
        session.rollback()
        print(f"\nErro ao registrar tentativa: {erro}")


def listar_tentativas(session):
    print("\n--- Tentativas ---")

    tentativas = session.scalars(
        select(Tentativa).order_by(Tentativa.id)
    ).all()

    if not tentativas:
        print("Nenhuma tentativa cadastrada.")
        return False

    for tentativa in tentativas:
        print(
            f"\nID: {tentativa.id}"
            f"\nEnigma ID: {tentativa.enigma_id}"
            f"\nResposta informada: {tentativa.resposta_informada}"
            f"\nNúmero da tentativa: {tentativa.numero_tentativa}"
            f"\nResultado: {tentativa.resultado}"
        )

    return True


def excluir_tentativa(session):
    print("\n--- Excluir Tentativa ---")

    if not listar_tentativas(session):
        return

    id_tentativa = ler_inteiro(
        "\nID da tentativa que deseja excluir: ",
        minimo=1
    )

    tentativa = session.get(Tentativa, id_tentativa)

    if tentativa is None:
        print("Tentativa não encontrada.")
        return

    confirmacao = input(
        "Tem certeza que deseja excluir esta tentativa? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    try:
        session.delete(tentativa)
        session.commit()

        print("Tentativa excluída com sucesso!")

    except Exception as erro:
        session.rollback()
        print(f"Erro ao excluir tentativa: {erro}")


def alterar_banco(session, tipo_banco):
    print("\n--- Alterar Banco de Dados ---")
    print("1 - SQLite")
    print("2 - MySQL")
    print("0 - Cancelar")

    opcao = input("\nEscolha: ").strip()

    if opcao == "0":
        return session, tipo_banco

    if opcao == "1":
        novo_banco = "sqlite"

    elif opcao == "2":
        novo_banco = "mysql"

    else:
        print("Opção inválida.")
        return session, tipo_banco

    if novo_banco == tipo_banco:
        print(f"Você já está conectado ao {tipo_banco.upper()}.")
        return session, tipo_banco

    nova_session = None

    try:
        nova_session = criar_sessao(novo_banco)
        session.close()

        print(
            f"\nConectado ao {novo_banco.upper()} "
            "com sucesso!"
        )

        return nova_session, novo_banco

    except Exception as erro:
        if nova_session is not None:
            nova_session.close()

        print(f"\nNão foi possível conectar ao {novo_banco.upper()}.")
        print(f"Erro: {erro}")

        return session, tipo_banco


def menu():
    tipo_banco = "sqlite"

    try:
        session = criar_sessao(tipo_banco)
    except Exception as erro:
        print(f"Erro ao iniciar o banco SQLite: {erro}")
        return

    while True:
        print("\n=================================")
        print("       SISTEMA DE ENIGMAS")
        print("=================================")
        print(f"Banco atual: {tipo_banco.upper()}")
        print()
        print("1 - Inserir enigma")
        print("2 - Listar enigmas")
        print("3 - Excluir enigma")
        print("4 - Inserir tentativa")
        print("5 - Listar tentativas")
        print("6 - Excluir tentativa")
        print("7 - Alterar banco de dados")
        print("0 - Sair")

        opcao = input("\nEscolha: ").strip()

        try:
            if opcao == "1":
                inserir_enigma(session)

            elif opcao == "2":
                listar_enigmas(session)

            elif opcao == "3":
                excluir_enigma(session)

            elif opcao == "4":
                inserir_tentativa(session)

            elif opcao == "5":
                listar_tentativas(session)

            elif opcao == "6":
                excluir_tentativa(session)

            elif opcao == "7":
                session, tipo_banco = alterar_banco(
                    session,
                    tipo_banco
                )

            elif opcao == "0":
                session.close()
                print("\nPrograma encerrado.")
                break

            else:
                print("Opção inválida. Escolha uma opção do menu.")

        except Exception as erro:
            session.rollback()
            print(f"\nOcorreu um erro: {erro}")


if __name__ == "__main__":
    menu()
