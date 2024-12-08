
# Здесь мы определим схему задачи так, чтобы она имела следующие атрибуты:
# id — идентификатор задачи (который будет целочисленным типом)
# content — фактическое содержимое объекта задачи «Сделать» (например, «Мыть посуду»)
# is_done — который имеет тип boolean и сообщает, помечена ли данная задача как завершенная или нет. По умолчанию он также должен быть установлен в False.

# Вот как будет выглядеть схема задач в Strawberry:
import strawberry
from typing import Optional

# Schema:


@strawberry.type
class Task:
    id: int
    content: str
    is_done: bool = False


# =============================

# Input Schema:


@strawberry.input
class UpdateTaskInput:
    content: Optional[str] = None
    is_done: Optional[bool] = None


@strawberry.input
class PaginationInput:
    offset: int
    limit: int