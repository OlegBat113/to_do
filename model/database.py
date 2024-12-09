import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base        <--- не используется
from  sqlalchemy.orm import declarative_base

from decouple import config

# import psycopg2       не нужно импортировать, т.к. он встроен в SQLAlchemy

# Рекомендуется использовать переменные окружения через config

# psycog2 - заменил на psycopg (pip instal psycopg) - после этого заработало

with open("model/data.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

try:
    engine = create_engine(f"postgresql+psycopg://{data['user']}:{data['password']}@{data['host']}/{data['database']}",
        echo=True,  # Включаем SQL логирование для отладки
        pool_size=5,  # Устанавливаем размер пула соединений
        max_overflow=10  # Максимальное количество дополнительных соединений
    )
    print(f"PostgreSQL: Соединение с БД на {data['host']} созданно успешно !")
except Exception as e:
    print(f"Error: Ошибка создания базы данных: {e}")

# Создаем фабрику сессий
DBSession  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()

