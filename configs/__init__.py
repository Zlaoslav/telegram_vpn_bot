import json
import os
from services.hlpr_logging import logger
from .advanced_settings import *


settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
try:
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)

    for key, value in settings.items():
        globals()[key] = value
except FileNotFoundError:
    logger.critical(f"Файл {settings_path} не найден. Убедитесь, что он существует и находится в правильной директории.")
    pass
except json.JSONDecodeError:
    logger.critical(f"Ошибка при загрузке {settings_path}: неверный формат JSON.")