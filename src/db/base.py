# src/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    All database models will inherit from this class.
    It automatically manages table registration.
    """
    pass
