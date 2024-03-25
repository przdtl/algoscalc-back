from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Calculations(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=255), nullable=False, unique=True)
    description = Column(Text, nullable=False, default='')

    parameters = relationship("Parameters", back_populates='calculation')
    output = relationship("Outputs", back_populates='calculation')

    def __str__(self):
        return self.title


class Parameters(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True)
    calculation_id = Column(ForeignKey('calculations.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)
    title = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=False, default='')
    data_type = Column(String(length=255), nullable=False)
    data_shape = Column(String(length=255), nullable=False)
    default_value = Column(Integer, nullable=False)

    calculation = relationship("Calculations", back_populates='parameters')

    def __str__(self):
        return f'{self.name}, {self.title}, {self.data_type}, {self.data_shape}, {self.default_value}'


class Outputs(Base):
    __tablename__ = "outputs"

    id = Column(Integer, primary_key=True)
    calculation_id = Column(ForeignKey('calculations.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)
    title = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=False, default='')
    data_type = Column(String(length=255), nullable=False)
    data_shape = Column(String(length=255), nullable=False)
    default_value = Column(Integer, nullable=False)

    calculation = relationship("Calculations", back_populates='output')

    def __str__(self):
        return f'{self.name}, {self.title}, {self.data_type}, {self.data_shape}, {self.default_value}'
