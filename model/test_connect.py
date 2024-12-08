import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base        <--- не используется
from  sqlalchemy.orm import declarative_base
from decouple import config


# Рекомендуется использовать переменные окружения через config

dialect = 'postgresql'
user = 'postgres'
password = 'Adelante'
host = 'localhost'
port = '5432'
database = 'todo'

# psycog2 - заменил на psycopg (pip instal psycopg) - после этого заработало


with open("data.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

engine = create_engine(f"{dialect}+psycopg://{data['user']}:{data['password']}@{data['host']}/{data['database']}",
    echo=True,  # Включаем SQL логирование для отладки
    pool_size=5,  # Устанавливаем размер пула соединений
    max_overflow=10  # Максимальное количество дополнительных соединений
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()

# Функция для получения сессии БД
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

'''

Основные изменения и рекомендации:

1. Удалил неиспользуемый импорт `psycopg2`
2. Добавил настройку через переменные окружения с возможностью установки значения по умолчанию
3. Добавил дополнительные параметры для `create_engine`:
   - `echo=True` для отладки SQL запросов
   - Настройки пула соединений
4. Переименовал `DBSession` в более стандартное `SessionLocal`
5. Добавил вспомогательную функцию `get_db()` для безопасной работы с сессиями

Для использования этого кода вам нужно создать файл `.env` в корне проекта и добавить в него:
    DATABASE_URL=postgresql+psycopg2://postgresql:Adelante@localhost/todo

Это сделает ваше приложение более безопасным и гибким в настройке.
'''


from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Создаем класс для доступа к таблице Users
# Используем базовый класс Base
class Users(Base):
    __tablename__ = "users"
    nrec = Column(Integer, primary_key=True)
    name2 = Column(String)

session = SessionLocal()
# Вставка данных
aaa1 = Users(name2="aaa1")
session.add(aaa1)
bbb1 = Users(name2="bbb1")
session.add(bbb1)
ccc1 = Users(name2="ccc1")
session.add(ccc1)
#session.add_all([aaa1, bbb1,ccc1])

# Подтверждение транзакции
session.commit()


# Обновление данных
aaa1.name = "ddd1"
session.commit()
session.close()

# Запрос данных
recs = session.query(Users).all()

for rec in recs:
    print(f"rec.nrec = {rec.nrec}, rec.name2 = {rec.name2}")




