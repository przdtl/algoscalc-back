from typing import Optional

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter, HTTPException, Depends

from src import TIME_OVER_MSG
from src.core.schemas.algorithms import (FibonacciOutputVariables, FibonacciInputVariables, MatrixSubOutputVariables,
                                         MatrixSubInputVariables, FibonacciListInputVariables,
                                         FibonacciListOutputVariables, QuadraticEquationInputVariables,
                                         QuadraticEquationOutputVariables, SubstringInStringInputVariables,
                                         SubstringInStringOutputVariables, PerfectNumbersInputVariables,
                                         PerfectNumbersOutputVariables, FuelConsumptionInputVariables,
                                         FuelConsumptionOutputVariables)
from src.database import async_session_maker, get_async_session
from src.core.schemas.calculations import (ReadCalculation, ReadAlgorithms, ReadAlgorithm, ReadOutput, ReadParameters)
from src.config import settings

from src.core.algorithm_collection import ALGORITHM_NOT_EXISTS_TEMPL
from src.api_models import (AlgorithmTitle, Algorithms, DataDefinition,
                            AlgorithmDefinition, AnswerAlgorithmDefinition, Parameters, AnswerOutputs, Outputs, Data)
from src.errors import ErrorMessages
from src.models import Calculations, Parameters as ParametersModel, Outputs as OutputsModel
from src.algorithms_manager import algorithms_manager

router = APIRouter()


@router.get(
    '/new',
    response_model=Page[ReadCalculation],
    tags=['new'],
)
async def get_algorithms(db: Session = Depends(get_async_session), name: Optional[str] = None):
    return await paginate(db,
                          select(Calculations.title, Calculations.name).filter(
                              Calculations.name.like(f'%{name if name else ""}%')),
                          transformer=lambda x: [ReadCalculation(title=row[0], name=row[1]) for row in x]
                          )


@router.get(
    '/new/{algorithm_name}',
    response_model=ReadAlgorithm,
    tags=['new'],
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
                        default_value=row.default_value
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
                        default_value=row.default_value
                    )
                )
        result = ReadAlgorithm(parameters=parameters_rows, outputs=outputs_rows, description=algorithm.description,
                               name=algorithm.name, title=algorithm.title)
        return result


@router.post(
    '/new/fibonacci',
    tags=['algorithms'],
    response_model=FibonacciOutputVariables,
)
async def get_fibonacci_result(parameters: FibonacciInputVariables):
    return await algorithms_manager.fibonacci_result(**parameters.__dict__)


@router.post(
    '/new/perfect_numbers',
    tags=['algorithms'],
    response_model=PerfectNumbersOutputVariables,
)
async def get_perfect_numbers_result(parameters: PerfectNumbersInputVariables):
    return await algorithms_manager.perfect_numbers_result(**parameters.__dict__)


@router.post(
    '/new/matrix_sub',
    tags=['algorithms'],
    response_model=MatrixSubOutputVariables,
)
async def get_matrix_sub_result(parameters: MatrixSubInputVariables):
    return await algorithms_manager.matrix_sub_result(**parameters.__dict__)


@router.post(
    '/new/fibonacci_list',
    tags=['algorithms'],
    response_model=FibonacciListOutputVariables,
)
async def get_fibonacci_list_result(parameters: FibonacciListInputVariables):
    return await algorithms_manager.fibonacci_list_result(**parameters.__dict__)


@router.post(
    '/new/fuel_consumption',
    tags=['algorithms'],
    response_model=FuelConsumptionOutputVariables,
)
async def get_fuel_consumption_result(parameters: FuelConsumptionInputVariables):
    return await algorithms_manager.fuel_consumption_result(**parameters.__dict__)


@router.post(
    '/new/quadratic_equation',
    tags=['algorithms'],
    response_model=QuadraticEquationOutputVariables,
)
async def get_quadratic_equation_result(parameters: QuadraticEquationInputVariables):
    return await algorithms_manager.quadratic_equation_result(**parameters.__dict__)


@router.post(
    '/new/substring_in_a_string',
    tags=['algorithms'],
    response_model=SubstringInStringOutputVariables,
)
async def get_substring_in_a_string_result(parameters: SubstringInStringInputVariables):
    return await algorithms_manager.substring_in_a_string_result(**parameters.__dict__)


# --------------------------------------------------------------------------- LEGACY CODE


@router.get(
    "/legacy_alg",
    tags=['legacy'],
)
async def legacy_get_algorithms() -> Algorithms:
    """Возвращает список имеющихся алгоритмов.

    :return: список имеющихся алгоритмов.
    :rtype: Algorithms
    """
    settings.logger.info('Request received')
    res = Algorithms(algorithms=[])
    for name, title in settings.algorithms.get_name_title_dict().items():
        res.algorithms.append(AlgorithmTitle(name=name, title=title))
    return res


@router.get(
    '/legacy_alg/{algorithm_name}',
    tags=['legacy'],
)
async def legacy_get_specific_algorithm(algorithm_name: str) -> AnswerAlgorithmDefinition:
    """Возвращает описание выбранного алгоритма.

    :param algorithm_name: имя алгоритма;
    :type algorithm_name: str
    :return: Описание алгоритма.
    :rtype: AnswerAlgorithmDefinition
    """
    settings.logger.info(f'Request received. algorithm_name: {algorithm_name}')
    answer = AnswerAlgorithmDefinition()
    if not settings.algorithms.has_algorithm(algorithm_name):
        settings.logger.warning(ALGORITHM_NOT_EXISTS_TEMPL.format(algorithm_name))
        answer.errors = ALGORITHM_NOT_EXISTS_TEMPL.format(algorithm_name)
        return answer
    try:
        alg = settings.algorithms.get_algorithm(algorithm_name)
        params = []
        outputs = []
        for param in alg.parameters:
            params.append(
                DataDefinition(name=param.name, title=param.title,
                               description=param.description,
                               data_type=str(param.data_type),
                               data_shape=str(param.data_shape),
                               default_value=param.default_value))
        for output in alg.outputs:
            outputs.append(
                DataDefinition(name=output.name, title=output.title,
                               description=output.description,
                               data_type=str(output.data_type),
                               data_shape=str(output.data_shape),
                               default_value=output.default_value))
        alg_def = AlgorithmDefinition(name=alg.name, title=alg.title,
                                      description=alg.description,
                                      parameters=params, outputs=outputs)
        answer.result = alg_def
    except Exception as error:
        settings.logger.warning(str(error))
        answer.errors = str(error)
    return answer


@router.post(
    '/legacy_alg/{algorithm_name}',
    tags=['legacy'],
)
async def legacy_get_algorithm_result(algorithm_name: str, parameters: Parameters) -> AnswerOutputs:
    """Возвращает результат выполнения выбранного алгоритма.

    :param algorithm_name: имя алгоритма;
    :type algorithm_name: str
    :param parameters: значения входных данных для выполнения алгоритма.
    :type parameters: Parameters
    :return: результат выполнения выбранного алгоритма
    :rtype: AnswerOutputs
    """
    settings.logger.info(f'Request received. algorithm_name: {algorithm_name}, '
                         f'parameters: {parameters}')
    answer = AnswerOutputs()
    if not settings.algorithms.has_algorithm(algorithm_name):
        settings.logger.warning(ALGORITHM_NOT_EXISTS_TEMPL.format(algorithm_name))
        answer.errors = ALGORITHM_NOT_EXISTS_TEMPL.format(algorithm_name)
        return answer
    params = parameters.get_params_to_execute()
    try:
        results = settings.algorithms.get_algorithm_result(algorithm_name, params)
        outputs = []
        for name, value in results.items():
            outputs.append(Data(name=name, value=value))
        answer.result = Outputs(outputs=outputs)
    except TimeoutError:
        settings.logger.warning(TIME_OVER_MSG)
        answer.errors = TIME_OVER_MSG
    except Exception as error:
        settings.logger.warning(str(error))
        answer.errors = str(error)
    return answer
