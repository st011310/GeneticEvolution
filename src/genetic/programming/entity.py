from abc import abstractmethod
from src.genetic.algorithm.entity import Entity

class ComputableEntity(Entity):
    """Абстрактный класс для вычислительных моделей"""
    @abstractmethod
    def run(cls, input: str) -> str:
        """Запускает вычисления"""
        pass

if __name__ == "__main__":
    pass