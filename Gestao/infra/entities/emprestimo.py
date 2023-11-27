from __future__ import annotations
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from infra.config.base import Base


class Emprestimo(Base):
    __tablename__ = 'emprestimos'

    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionarios.id"), primary_key=True)
    uniforme_id: Mapped[int] = mapped_column(ForeignKey("uniformes.id"), primary_key=True)
    data_emprestimo: Mapped[datetime] = mapped_column(nullable=False)
    data_devolucao: Mapped[datetime] = mapped_column(nullable=True)
    funcionario = relationship("Funcionario", back_populates="emprestimo")
    uniforme = relationship("Uniforme", back_populates="emprestimo")

