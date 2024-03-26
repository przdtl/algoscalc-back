from typing import Union, Optional

from pydantic import BaseModel


# INPUT SCHEMAS
class FibonacciInputVariables(BaseModel):
    n: int


class FibonacciListInputVariables(BaseModel):
    n: int


class MatrixSubInputVariables(BaseModel):
    n: list[list[float]]
    m: list[list[float]]


class QuadraticEquationInputVariables(BaseModel):
    a: float
    b: float
    c: float


class SubstringInStringInputVariables(BaseModel):
    text: str
    findtext: str


class PerfectNumbersInputVariables(BaseModel):
    numbers: list[int]


class FuelConsumptionInputVariables(BaseModel):
    distance: float
    mean_consumption: float
    price: float
    need_round: bool


# OUTPUT SCHEMAS


class FibonacciOutputVariables(BaseModel):
    result: int


class FibonacciListOutputVariables(BaseModel):
    result: list[int]


class MatrixSubOutputVariables(BaseModel):
    result: list[list[float]]


class QuadraticEquationOutputVariables(BaseModel):
    roots: str


class SubstringInStringOutputVariables(BaseModel):
    num_count: int


class PerfectNumbersOutputVariables(BaseModel):
    has_perfect: bool
    perfect_numbers: list[int]


class FuelConsumptionOutputVariables(BaseModel):
    volume: float
    cost: float
