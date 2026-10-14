import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

load_dotenv()


def criar_engine(tipo_banco: str):
    if tipo_banco == "sqlite":
        return create_engine(
            "sqlite:///enigmas.db",
            echo=False
        )

    if tipo_banco == "mysql":
        usuario = os.getenv("MYSQL_USER")
        senha = os.getenv("MYSQL_PASSWORD")
        banco = os.getenv("MYSQL_DATABASE")
        servidor = os.getenv("MYSQL_HOST")
        porta = os.getenv("MYSQL_PORT", "3306")

        if not all([usuario, banco, servidor]):
            raise ValueError(
                "As configurações do MySQL não foram encontradas no .env."
            )

        url = (
            f"mysql+pymysql://{usuario}:{senha}"
            f"@{servidor}:{porta}/{banco}"
        )

        return create_engine(url, echo=False)

    raise ValueError("Banco de dados inválido.")


def criar_sessao(tipo_banco: str):
    engine = criar_engine(tipo_banco)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    return Session()
