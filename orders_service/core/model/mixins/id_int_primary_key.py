import uuid
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUID_PG


class IdPrKey:
    id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
