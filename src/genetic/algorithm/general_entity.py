from abc import ABC, abstractmethod
import random, json
from .entity import Entity

class GeneralizedEntityBase(ABC):
    @abstractmethod
    def getCode(self) -> list:
        '''Возвращает код -- геном сущности -- список однородных элементов.'''
        ...
    @abstractmethod
    def setCode(self, code: list):
        '''Переопределяяет сущность, меняя код.'''
        ...
    @abstractmethod
    def getEntity(self, code: list):
        '''Из кода получает сущность.'''
        ...
    @abstractmethod
    def getRandomGen(self):
        '''Возвращает случайный корректный ген.'''
        ...


class GeneralizedEntity(Entity, GeneralizedEntityBase):
    def __init__(self, coding_size: int) -> None:
        super().__init__()
        assert coding_size > 1, "Для корректного скрещивания необходимо хотя бы два элемента"
        self.N = coding_size

    def mutate(self, mutation_rate: float = 0.1):
        code = []
        for gen in self.getCode():
            if random.random() < mutation_rate:
                gen = self.getRandomGen()
            code.append(gen)
        self.setCode(code)

    def crossover1p(self, other: 'GeneralizedEntity'):
        code1 = self.getCode()
        code2 = other.getCode()
        x = random.randint(1, self.N)
        newCode1 = code1[:x] + code2[x:]
        newCode2 = code2[:x] + code1[x:]
        self.setCode(newCode1)
        other.setCode(newCode2)

    def save(self, filepath: str) -> None:
        with open(filepath, mode='w') as file:
            json.dump(self.getCode(), file)

    @classmethod
    def load(cls, filepath: str) -> 'GeneralizedEntity':
        code = None
        with open(filepath) as file:
            code = json.load(file)
        obj = cls(len(code))
        obj.setCode(code)
        return obj