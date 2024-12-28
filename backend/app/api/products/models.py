from sqlalchemy.orm import Mapped, mapped_column

from app.api.core.db import Base


class DBProduct(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

