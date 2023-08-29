import os
import logging
from fastapi import HTTPException


def load_env():
    dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../.env.config')
    if os.path.exists(dotenv_path):
        from dotenv import load_dotenv
        load_dotenv(dotenv_path)


def get_logger():
    return logging.getLogger('app_logger')


logger = get_logger()


def HTTP_ERROR(code: int = 400, message: str = 'Something was wrong!', headers=None):
    raise HTTPException(status_code=code, detail=message, headers=headers)
