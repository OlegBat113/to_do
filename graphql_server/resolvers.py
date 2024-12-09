# мы хотим охватить следующие операции CRUD (создание, чтение, обновление, удаление) в наших резолверах:

# - Создать: Добавить новую задачу
# - Прочитайте:
# - Получите все задачи в списке дел
# - Получить одну задачу (по ее id)
# - Обновление: обновление задачи из списка дел
# - Удалить: удаление определенной задачи из списка дел

# Мы сгруппируем наши методы резолвера в два класса:

# Класс QueryResolver - его методы будут обрабатывать операции READ или извлечение данных из базы данных.
# Класс MutationResolver - его методы будут обрабатывать операции WRITE или создавать, обновлять и удалять.

# Мы определим каждый резолвер как статический метод в этих двух классах:

from strawberry import ID

from . import schemas

from model import models
from model.database import DBSession 

from typing import List

class QueryResolver:

    # У нас есть необязательный аргумент для пагинации, который по умолчанию равен None.
    #  Если запрос не включает параметры для пагинации,
    #  этот метод вернет все данные в таблице tasks в базе данных.
    #  В противном случае он обратится к базе данных с параметрами пагинации и вернет полученный запрос.
    @staticmethod
    def get_tasks(pagination: (schemas.PaginationInput | None) = None) -> List[schemas.Task]:
        
        # Сопоставитель get_tasks использует экземпляр Session (сохраненный в переменной db) из DBSession,
        #  который мы определили ранее на нашем уровне данных.
        #  Этот экземпляр Session мы используем для подключения к базе данных и запроса к ней.
        db = DBSession()

        # Обратите внимание, что запрос к базе данных упакован в блок try, в котором мы указали db.close() в блоке finally,
        #  так что что бы ни произошло во время сеанса подключения к базе данных (скажем, произошла ошибка),  мы закрываем соединение с базой данных.
        #  Это важно для обеспечения безопасности, особенно в производственной среде, так как вы не хотите,
        #  чтобы открытая сессия в вашей базе данных просто лежала без внимания,
        #  так как она может быть потенциально украдена злоумышленниками и получить контроль над вашей базой данных.
        try:
            # модель Task из нашего слоя данных используется методом query() для нацеливания на нужную нам таблицу базы данных (tasks). 
            query = db.query(models.Task)

            if pagination is not None:
                # нам все еще нужен еще один компонент: определение схемы входных данных пагинации,
                #  которые представляют собой объект с атрибутами offset и limit.
                query = query\
                    .offset(pagination.offset)\
                    .limit(pagination.limit)

            tasks = query.all()
        finally:
            db.close()
        return tasks

    # Преобразователь get_task() похож на преобразователь get_tasks() в том,
    #  как мы структурируем наш код (с блоком try и переменной db, хранящей экземпляр Session).
    #  Только здесь преобразователь get_task() возвращает только один объект Task вместо списка.
    @staticmethod
    def get_task(task_id: ID) -> (schemas.Task | None):
        db = DBSession()
        try:
            # Мы также запрашиваем базу данных, но фильтруем результат по совпадающему идентификатору, переданному клиентом.
            #  Если параметр id совпадает с записью в таблице задач из базы данных,
            #  он вернет соответствующий объект Task,  в противном случае он вернет None (или null).
            task = db.query(models.Task).filter(
                models.Task.id == task_id).first()
        finally:
            db.close()
        return task


# нам нужно подключить преобразователи мутаций нашего API GraphQL к уровню данных.
class MutationResolver:
    @staticmethod
    def add_task(task_content: str) -> schemas.Task:
        db = DBSession()

        try:
            # Для этого преобразователя требуется один параметр, task_content (который относится к содержанию задачи в задаче, например «мыть посуду»).
            #  Мы требуем только содержимое задачи от клиента, так как атрибут id будет автоматически сгенерирован SQLAlchemy (так как мы указали его в качестве первичного ключа),
            #  в то время как мы хотим, чтобы is_done всегда по умолчанию имел значение False.
            new_task = models.Task(content=task_content)

            # Мы добавляем новую запись в таблицу tasks в базе данных,
            #  после чего сразу же отправляем изменения в базу данных (commit) и получаем измененную запись из базы данных (refresh).
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
        finally:
            db.close()
        return new_task


    #
    @staticmethod
    def update_task(task_id: ID, task: schemas.UpdateTaskInput) -> (schemas.Task | None):
        db = DBSession()
        try:
            modified_task = db.query(models.Task).filter(
                models.Task.id == task_id).first()
            modified_task.content = task.content if task.content is not None else modified_task.content
            modified_task.is_done = task.is_done if task.is_done is not None else modified_task.is_done
            db.commit()
            db.refresh(modified_task)
        finally:
            db.close()
        return modified_task


    # Во-первых, структура кода такая же, как и у блока try.
    #  Мы также используем экземпляр Session, хранящийся в db, для запроса базы данных.
    #  И, как и преобразователи get_task() и update_task(), мы запрашиваем в базе данных определенный объект задачи.
    #  Но в отличие от преобразователя update_task(), он удаляет соответствующий объект задачи (или ничего не удаляет, если совпадения нет).
    #  Независимо от того, совпадет он и удалит объект задачи или нет, он вернет None (или null), что является обычной практикой при создании API GraphQL.
    @staticmethod
    def delete_task(task_id: ID) -> None:
        db = DBSession()
        try:
            deleted_task = db.query(models.Task).filter(
                models.Task.id == task_id).first()
            db.delete(deleted_task)
            db.commit()
        finally:
            db.close()
