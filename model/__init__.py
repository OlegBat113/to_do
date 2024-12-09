# Мы помещаем эту функциональность в __init__.py файл пакета модели, так как мы хотим, чтобы она вступала в силу каждый раз, 
# когда мы импортируем пакет модели (или что-либо, что мы импортируем из моделей).

from . import models, database

# Will create the Table/s if they don't exist yet
models.Base.metadata.create_all(bind=database.engine) 
