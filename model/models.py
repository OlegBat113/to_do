from sqlalchemy import Column, String, Integer, Boolean

from .database import Base

 # класс Task наследует класс Base от database.py.
# эта модель Task имеет следующие атрибуты:
class Task(Base):
	# Мы также даем ему переменную "dunder" (двойное подчеркивание) __tablename__, которую SQLAlchemy будет использовать для ссылки на таблицу SQL, на которую сопоставляется эта модель.
	__tablename__ = "tasks"
	
	#  мы передаем им экземпляры класса Column, который SQLAlchemy будет использовать для ссылки на каждый столбец SQL-таблицы, с которой он сопоставлен. 
	id = Column(Integer, primary_key=True)
	content = Column(String)
	is_done = Column(Boolean, default=False)

    # Когда вы вызываете repr() для экземпляра Task, SQLAlchemy автоматически формирует и возвращает текстовое представление этого экземпляра, включая его атрибуты.
	def __repr__(self):
		return f'Task(id={self.id}, content={self.content}, is_done={self.is_done})'

