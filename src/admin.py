from sqladmin import ModelView

from src.models import Calculations, Outputs, Parameters


class CalculationsAdmin(ModelView, model=Calculations):
    column_list = [c.name for c in Calculations.__table__.c] + [Calculations.parameters, Calculations.outputs]


class ParametersAdmin(ModelView, model=Parameters):
    column_list = [c.name for c in Parameters.__table__.c] + [Parameters.calculation]


class OutputAdmin(ModelView, model=Outputs):
    column_list = [c.name for c in Outputs.__table__.c] + [Parameters.calculation]
