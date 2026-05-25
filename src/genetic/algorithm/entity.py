from abc import ABC, abstractmethod

class Entity(ABC):
    """Абстрактный класс для вычислительных моделей"""

    @abstractmethod
    def randomize(*args, **kwargs) -> 'Entity':
        """Случайная инициализация модели"""
        pass

    @abstractmethod
    def mutate(self, mutation_rate: float = 0.1):
        """Мутация модели (изменение правил)"""
        pass

    @abstractmethod
    def crossover(self, other: 'Entity'):
        """Кроссинговер, немного смешивает две модели"""
        pass

    @abstractmethod
    def reproduction(self, other: 'Entity') -> 'Entity':
        """Скрещивание с другой моделью, возвращает нового потомка"""
        pass

    @abstractmethod
    def save(self, filepath: str) -> None:
        """Сохраняет в JSON файл."""

    @abstractmethod
    def load(cls, filepath: str) -> 'Entity':
        """Загружает из JSON файла"""


if __name__ == "__main__":
    pass