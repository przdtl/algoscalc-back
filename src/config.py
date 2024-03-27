import json
import os

import logging.config
from pydantic_settings import BaseSettings, SettingsConfigDict

from src import LOG_CONFIG_FILE_PATH, APP_CONFIG_FILE_PATH, PATH_CONFIG, ALGORITHM_CONFIG, IS_TEST_APP, EXECUTE_TIMEOUT
from src.core.algorithm_collection import AlgorithmCollection


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    def __init__(self):
        super().__init__()
        self.__logger_init()
        self.__init_config()
        # self.__init_algorithm_collection()

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def __logger_init(self):
        if os.path.exists('../' + LOG_CONFIG_FILE_PATH):
            os.chdir('..')
        with open(LOG_CONFIG_FILE_PATH, 'r') as log_conf_file:
            log_config = json.load(log_conf_file)
        file_path = None
        try:
            file_path = log_config["handlers"]["file_handler"]["filename"]
        except KeyError:
            pass
        if file_path:
            folder = os.path.split(file_path)[0]
            if not os.path.isdir(folder):
                os.mkdir(folder)
        logging.config.dictConfig(log_config)
        logger = logging.getLogger(__name__)
        logger.info('Start app')
        self.__logger = logger
        self.__logger_config = log_config

    def __init_config(self):
        with open(APP_CONFIG_FILE_PATH, 'r') as conf_file:
            config = json.load(conf_file)
        path_config = config[PATH_CONFIG]
        algorithm_config = config[ALGORITHM_CONFIG]
        if bool(os.environ.get(IS_TEST_APP)):
            algorithm_config[EXECUTE_TIMEOUT] = 0
        self.__path_config = path_config
        self.__algorithm_config = algorithm_config
        self.__web_config = config['web_config']

    def __init_algorithm_collection(self):
        self.__algorithms = AlgorithmCollection(self.__path_config, self.__algorithm_config, self.__logger_config)

    @property
    def logger(self):
        return self.__logger

    @property
    def algorithm_config(self):
        return self.__algorithm_config

    @property
    def path_config(self):
        return self.__path_config

    @property
    def web_config(self):
        return self.__web_config

    @property
    def algorithms(self):
        return self.__algorithms

    @property
    def redis_url(self):
        return 'redis://redis_db:6379/0'

    # model_config = SettingsConfigDict(
    #     # `.env.prod` takes priority over `.env`
    #     env_file=('.env.prod', '.env'),
    #     env_file_encoding='utf-8'
    # )
    class Config:
        env_file = ".env"
        extra = "allow"  # this allows all the other env vars


settings = Settings()
