# Теперь, когда у нас есть схема задач и сопоставители шаблонов, мы можем приступить к определению наиболее важных схем в нашем API GraphQL, схем запросов и мутаций.

# Эти два типа схем являются особыми, поскольку именно их Strawberry будет использовать для обработки запросов и мутаций. Как правило, эти специальные схемы всегда называются так — Query and Mutation.

# В нашем проекте мы хотим, чтобы схема запроса имела следующие атрибуты данных в соответствии с нашими требованиями к CRUD-операциям:

# - задачи: Список[схемы. Task] - Список задач
# - Задача: (Схемы. Задача | None) - Один объект Задачи (или Нет, если идентификатор, переданный запросу, не соответствует ни одной Задаче)
# Обратите внимание, как типы этих двух атрибутов совпадают с типами возвращаемых значений двух методов сопоставителя запросов: get_tasks: -> List[schemas. Task] и get_task: -> (схемы. Задача | Нет). Это связано с тем, что мы подключим эти резолверы к этим атрибутам данных Query позже. Для этих атрибутов мы будем использовать возвращаемое значение методов резолвера. Это также то, что я имел в виду, когда говорил «резолверы обрабатывают получение данных по запросам».

# То же самое относится и к схеме Mutation:
# - add_task: схема. Задача — добавляет новую задачу в список дел и возвращает вновь добавленную задачу.
# - update_task: (схема. Задача | None) - Обновляет определенный объект задачи и возвращает обновленную задачу или null, если задачи с заданным идентификатором не существует.
# - delete_task — Удаляет задачу с заданным идентификатором и возвращает null независимо от того, была ли операция успешной или нет. Кроме того, вам не нужно комментировать это.

# Мы определим эти два параметра непосредственно в файле __init__.py graphql_package:

from strawberry.fastapi import GraphQLRouter

import strawberry
from strawberry.fastapi import GraphQLRouter

from .schemas import Task
from .resolvers import QueryResolver, MutationResolver

from typing import List


@strawberry.type
class Query:
    tasks: List[Task] = strawberry.field(resolver=QueryResolver.get_tasks)
    task: (Task | None) = strawberry.field(resolver=QueryResolver.get_task)


@strawberry.type
class Mutation:
    add_task: Task = strawberry.field(resolver=MutationResolver.add_task)
    update_task: (Task | None) = strawberry.field(
        resolver=MutationResolver.update_task)
    delete_task = strawberry.field(resolver=MutationResolver.delete_task)


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema) 