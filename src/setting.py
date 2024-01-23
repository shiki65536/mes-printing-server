from enum import StrEnum
from typing import Annotated

from pydantic import (
    AnyUrl,
    NewPath,
    DirectoryPath,
    UrlConstraints,
    PositiveFloat,
    PositiveInt,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

OpcuaUrl = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["opc.tcp"])]


class LoggingLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AppSettings(BaseSettings):
    database_url: AnyUrl
    opcua_server_url: OpcuaUrl
    upload_path: NewPath | DirectoryPath
    printer_worker_interval: PositiveFloat = 1
    mock_printer_interval: PositiveFloat = 2
    mock_printer_job_time: PositiveInt = 30
    mock_printer_target_bed_temperature: PositiveInt = 100
    mock_printer_target_bed_nozzle: PositiveInt = 120
    logging_level: LoggingLevel = LoggingLevel.INFO


class EnvAppSettings(AppSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


def display():
    s = EnvAppSettings()
    s.upload_path.mkdir(exist_ok=True)
    print(s.model_dump_json(indent=4))
