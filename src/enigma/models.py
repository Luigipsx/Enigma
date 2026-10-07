from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Enigma(Base):
    __tablename__ = "enigmas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    resposta: Mapped[str] = mapped_column(String(150), nullable=False)
    limite_tentativas: Mapped[int] = mapped_column(Integer, nullable=False)
    resolvido: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    tentativas: Mapped[list["Tentativa"]] = relationship(
        back_populates="enigma",
        cascade="all, delete-orphan"
    )


class Tentativa(Base):
    __tablename__ = "tentativas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enigma_id: Mapped[int] = mapped_column(
        ForeignKey("enigmas.id"),
        nullable=False
    )
    resposta_informada: Mapped[str] = mapped_column(String(150), nullable=False)
    numero_tentativa: Mapped[int] = mapped_column(Integer, nullable=False)
    resultado: Mapped[str] = mapped_column(String(10), nullable=False)

    enigma: Mapped["Enigma"] = relationship(back_populates="tentativas")
