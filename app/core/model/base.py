from sqlalchemy.orm import Mapped,mapped_column,declared_attr,DeclarativeBase
from sqlalchemy import UUID as UUID_SA
from utils import camel_case_to_snake_case
from sqlalchemy import MetaData
from core.config import settings
import uuid

class Base(DeclarativeBase):
    __abstract__=True

    @declared_attr.directive
    def __tablename__(cls) ->str:
        return camel_case_to_snake_case(cls.__name__)

    id: Mapped[uuid] = mapped_column(
        UUID_SA(as_uuid=True),
        primary_key = True,
        default=uuid.uuid4
    )
