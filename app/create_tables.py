"""
Скрипт для создания всех таблиц в базе данных.
Запускать отдельно для инициализации структуры БД.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models  # ensure models are imported so tables are registered
from app.database import Base, engine

if __name__ == "__main__":
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы.")
