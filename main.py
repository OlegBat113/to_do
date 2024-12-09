# https://thepythoncode.com/article/build-a-graphql-api-with-fastapi-strawberry-and-postgres-python


from fastapi import FastAPI

# This is the GraphQL route handler from the package we created

from graphql_server import graphql_app
# Создание сервера GraphQL

app = FastAPI()

# создайте новый маршрут FastAPI /graphql и установите graphql_app в качестве обработчика маршрута.
app.include_router(graphql_app, prefix='/graphql')
