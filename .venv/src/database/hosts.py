from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Base, Mapped, relationship, mapped_column

class Host(Base):
    __tablename__ = "Host"
    
    hostname : Mapped[String] = mapped_column(String(120), primary_key=True)
    port : Mapped[Integer] = mapped_column(Integer)