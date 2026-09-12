from sqlalchemy.orm import DeclarativeBase

class Base (DeclarativeBase):
    """Registry for all models. All models inherit from this class. Inheriting is what makes a class a table."""
    pass