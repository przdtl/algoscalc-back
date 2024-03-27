from typing import Optional

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter, HTTPException, Depends

from src.schemas.algorithms import (FibonacciOutputVariables, FibonacciInputVariables, MatrixSubOutputVariables,
                                    MatrixSubInputVariables, FibonacciListInputVariables,
                                    FibonacciListOutputVariables, QuadraticEquationInputVariables,
                                    QuadraticEquationOutputVariables, SubstringInStringInputVariables,
                                    SubstringInStringOutputVariables, PerfectNumbersInputVariables,
                                    PerfectNumbersOutputVariables, FuelConsumptionInputVariables,
                                    FuelConsumptionOutputVariables, SimplexMethodOutputVariables,
                                    SimplexMethodInputVariables)
from src.database import async_session_maker, get_async_session
from src.schemas.calculations import (ReadCalculation, ReadAlgorithm, ReadOutput, ReadParameters)

from src.errors import ErrorMessages
from src.models import Calculations, Parameters as ParametersModel, Outputs as OutputsModel
from src.algorithms_manager import algorithms_manager

router = APIRouter()


@router.get(
    '/',
    response_model=Page[ReadCalculation],
    tags=['db_algorithm'],
)
async def get_algorithms(db: Session = Depends(get_async_session), name: Optional[str] = None):
    return await paginate(db,
                          select(Calculations.title, Calculations.name).filter(
                              Calculations.name.like(f'%{name if name else ""}%')),
                          transformer=lambda x: [ReadCalculation(title=row[0], name=row[1]) for row in x]
                          )


@router.get(
    '/{algorithm_name}',
    response_model=ReadAlgorithm,
    tags=['db_algorithm'],
)
async def get_specific_algorithm(algorithm_name: str):
    async with async_session_maker() as session:
        stmt = select(Calculations).filter_by(name=algorithm_name)
        res = await session.execute(stmt)
        algorithm = res.scalar()

        if not algorithm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessages.GET_ALGORITHM_ALGORITHM_NOT_EXISTS
            )

        parameters_stmt = select(ParametersModel).join(ParametersModel.calculation).filter(
            Calculations.id == algorithm.id)
        outputs_stmt = select(OutputsModel).join(OutputsModel.calculation).filter(Calculations.id == algorithm.id)

        parameters = await session.execute(parameters_stmt)
        outputs = await session.execute(outputs_stmt)

        parameters = parameters.all()
        outputs = outputs.all()

        parameters_rows = []
        for parameter in parameters:
            for row in parameter:
                parameters_rows.append(
                    ReadParameters(
                        title=row.title,
                        description=row.description,
                        name=row.name,
                        data_type=row.data_type,
                        data_shape=row.data_shape,
                    )
                )
        outputs_rows = []
        for output in outputs:
            for row in output:
                outputs_rows.append(
                    ReadOutput(
                        title=row.title,
                        description=row.description,
                        name=row.name,
                        data_type=row.data_type,
                        data_shape=row.data_shape,
                    )
                )
        result = ReadAlgorithm(parameters=parameters_rows, outputs=outputs_rows, description=algorithm.description,
                               name=algorithm.name, title=algorithm.title)
        return result


@router.post(
    '/fibonacci',
    tags=['algorithms'],
    response_model=FibonacciOutputVariables,
)
async def get_fibonacci_result(parameters: FibonacciInputVariables):
    return await algorithms_manager.fibonacci_result(**parameters.__dict__)


@router.post(
    '/perfect_numbers',
    tags=['algorithms'],
    response_model=PerfectNumbersOutputVariables,
)
async def get_perfect_numbers_result(parameters: PerfectNumbersInputVariables):
    return await algorithms_manager.perfect_numbers_result(**parameters.__dict__)


@router.post(
    '/matrix_sub',
    tags=['algorithms'],
    response_model=MatrixSubOutputVariables,
)
async def get_matrix_sub_result(parameters: MatrixSubInputVariables):
    return await algorithms_manager.matrix_sub_result(**parameters.__dict__)


@router.post(
    '/fibonacci_list',
    tags=['algorithms'],
    response_model=FibonacciListOutputVariables,
)
async def get_fibonacci_list_result(parameters: FibonacciListInputVariables):
    return await algorithms_manager.fibonacci_list_result(**parameters.__dict__)


@router.post(
    '/fuel_consumption',
    tags=['algorithms'],
    response_model=FuelConsumptionOutputVariables,
)
async def get_fuel_consumption_result(parameters: FuelConsumptionInputVariables):
    return await algorithms_manager.fuel_consumption_result(**parameters.__dict__)


@router.post(
    '/quadratic_equation',
    tags=['algorithms'],
    response_model=QuadraticEquationOutputVariables,
)
async def get_quadratic_equation_result(parameters: QuadraticEquationInputVariables):
    return await algorithms_manager.quadratic_equation_result(**parameters.__dict__)


@router.post(
    '/substring_in_a_string',
    tags=['algorithms'],
    response_model=SubstringInStringOutputVariables,
)
async def get_substring_in_a_string_result(parameters: SubstringInStringInputVariables):
    return await algorithms_manager.substring_in_a_string_result(**parameters.__dict__)


@router.post(
    '/simplex_method',
    tags=['algorithms'],
    response_model=SimplexMethodOutputVariables,
)
async def get_substring_in_a_string_result(parameters: SimplexMethodInputVariables):
    return await algorithms_manager.simplex_method_result(**parameters.__dict__)
