from typing import Optional

from pydantic import BaseModel


class ReadCalculation(BaseModel):
    name: str
    title: str


class ReadParameters(BaseModel):
    title: str
    description: str
    name: str
    data_type: str
    data_shape: str


class ReadOutput(BaseModel):
    title: str
    description: str
    name: str
    data_type: str
    data_shape: str


class ReadAlgorithm(ReadCalculation):
    description: str
    parameters: list[ReadParameters]
    outputs: list[ReadOutput]
