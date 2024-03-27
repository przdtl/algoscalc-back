from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from src.schemas.algorithms import (FibonacciOutputVariables, MatrixSubOutputVariables,
                                    FibonacciListOutputVariables,
                                    QuadraticEquationOutputVariables,
                                    SubstringInStringOutputVariables,
                                    PerfectNumbersOutputVariables,
                                    FuelConsumptionOutputVariables, SimplexMethodOutputVariables)

from src.algorithms.fibonacci.function import fibonacci
from src.algorithms.fibonacci_list.function import fibonacci as fibonacci_list
from src.algorithms.fuel_consumption.function import main as fuel_consumption
from src.algorithms.matrix_sub.function import main as matrix_sub
from src.algorithms.perfect_numbers.function import main as perfect_numbers
from src.algorithms.quadratic_equation.function import main as quadratic_equation
from src.algorithms.substring_in_a_string.function import main as substring_in_a_string
from src.algorithms.simplex_method.function import main as simplex_method

from src.database import async_session_maker
from src.errors import ErrorMessages
from src.models import Calculations


class AlgorithmsManager:

    @classmethod
    async def fibonacci_result(cls, **parameters) -> FibonacciOutputVariables:
        await cls.__is_algorithm_exist('fibonacci')
        n = parameters.get('n')
        res = fibonacci(n)
        return FibonacciOutputVariables(result=res)

    @classmethod
    async def fibonacci_list_result(cls, **parameters) -> FibonacciListOutputVariables:
        await cls.__is_algorithm_exist('fibonacci_list')
        n = parameters.get('n')
        res = fibonacci_list(n)
        return FibonacciListOutputVariables(result=res)

    @classmethod
    async def perfect_numbers_result(cls, **parameters) -> PerfectNumbersOutputVariables:
        await cls.__is_algorithm_exist('perfect_numbers')
        numbers = parameters.get('numbers')
        try:
            result = perfect_numbers(numbers)
            result = PerfectNumbersOutputVariables(**result)
            return result
        except ValueError as e:
            exception_message = str(e)
            if exception_message == 'Список чисел пуст':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.THE_LIST_OF_NUMBERS_IS_EMPTY,
                )
            if exception_message == 'Список чисел содержит отрицательное значение':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.THE_LIST_OF_NUMBERS_CONTAINS_NEGATIVE_VALUE,
                )

    @classmethod
    async def matrix_sub_result(cls, **parameters) -> MatrixSubOutputVariables:
        await cls.__is_algorithm_exist('matrix_sub')
        n = parameters.get('n')
        m = parameters.get('m')
        try:
            result = matrix_sub(n, m)
            result = MatrixSubOutputVariables(**result)
            return result
        except ValueError as e:
            exception_message = str(e)
            if exception_message == 'Длины матриц не совпадают!':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.THE_LENGTHS_OF_THE_MATRICES_DO_NOT_MATCH,
                )
            if 'Введено неверное количество столбцов для' in exception_message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.INCORRECT_NUMBER_OF_MATRIX_COLUMNS,
                )
            if 'Не введено значение в матрице' in exception_message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.NO_VALUE_ENTERED_IN_THE_MATRIX,
                )

    @classmethod
    async def fuel_consumption_result(cls, **parameters) -> FuelConsumptionOutputVariables:
        await cls.__is_algorithm_exist('fuel_consumption')
        distance = parameters.get('distance')
        mean_consumption = parameters.get('mean_consumption')
        price = parameters.get('price')
        need_round = parameters.get('need_round')
        try:
            result = fuel_consumption(distance, mean_consumption, price, need_round)
            result = FuelConsumptionOutputVariables(**result)
            return result
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.THE_PARAMETER_VALUE_IS_LESS_THAN_ZERO,
            )

    @classmethod
    async def quadratic_equation_result(cls, **parameters) -> QuadraticEquationOutputVariables:
        await cls.__is_algorithm_exist('quadratic_equation')
        a = parameters.get('a')
        b = parameters.get('b')
        c = parameters.get('c')
        try:
            result = quadratic_equation(a, b, c)
            result = QuadraticEquationOutputVariables(**result)
            return result
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.THE_COEFFICIENTS_MUST_BE_NUMBERS,
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.THE_COEFFICIENT_FOR_X2_CANNOT_BE_EQUAL_TO_0,
            )

    @classmethod
    async def substring_in_a_string_result(cls, **parameters) -> SubstringInStringOutputVariables:
        await cls.__is_algorithm_exist('substring_in_a_string')
        text = parameters.get('text')
        findtext = parameters.get('findtext')
        result = substring_in_a_string(text, findtext)
        result = SubstringInStringOutputVariables(**result)
        return result

    @classmethod
    async def simplex_method_result(cls, **parameters) -> SimplexMethodOutputVariables:
        await cls.__is_algorithm_exist('simplex_method')
        tableau = parameters.get('tableau')
        basic_var = parameters.get('basic_var')
        try:
            result = simplex_method(tableau, basic_var)
            result = SimplexMethodOutputVariables(**result)
            return result
        except ValueError as e:
            exception_message = str(e)
            if exception_message == 'Эта таблица бесконечна':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.THIS_TABLE_IS_ENDLESS,
                )
            if exception_message == 'Решения нет':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.THERE_IS_NO_SOLUTION,
                )
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.INCORRECT_INPUT_DATA,
            )

    @classmethod
    async def __is_algorithm_exist(cls, name):
        async with async_session_maker() as session:
            query = select(Calculations.id).filter_by(name=name)
            fibonacci_calc = await session.execute(query)
            fibonacci_calc = fibonacci_calc.all()
            if not fibonacci_calc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ErrorMessages.GET_ALGORITHM_ALGORITHM_NOT_EXISTS
                )


algorithms_manager = AlgorithmsManager()
