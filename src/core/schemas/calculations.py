from typing import Optional

from pydantic import BaseModel


class ReadCalculation(BaseModel):
    name: str
    title: str


class ReadAlgorithms(BaseModel):
    algorithms: list[ReadCalculation]


class ReadParameters(BaseModel):
    title: str
    description: str
    name: str
    data_type: str
    data_shape: str
    default_value: int


class ReadOutput(BaseModel):
    title: str
    description: str
    name: str
    data_type: str
    data_shape: str
    default_value: int


class ReadAlgorithm(ReadCalculation):
    description: str
    parameters: list[ReadParameters]
    outputs: list[ReadOutput]
