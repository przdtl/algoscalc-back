"""Реализация API для онлайн-калькулятора с использованием фреймворка FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from src import ALGORITHMS_ENDPOINT
from src.routers.algorithm import router as algorithm_router
from src.admin import CalculationsAdmin, ParametersAdmin, OutputAdmin
from src.database import engine
from src.config import settings

app = FastAPI()

# Добавление заголовков к HTTP ответам
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.web_config['cors']['origins'],
    allow_credentials=settings.web_config['cors']['credentials'],
    allow_methods=settings.web_config['cors']['methods'],
    allow_headers=settings.web_config['cors']['headers']
)

admin = Admin(app, engine)
admin.add_view(CalculationsAdmin)
admin.add_view(ParametersAdmin)
admin.add_view(OutputAdmin)

app.include_router(
    algorithm_router,
    prefix=ALGORITHMS_ENDPOINT,
    tags=['algooscalc'],
)
