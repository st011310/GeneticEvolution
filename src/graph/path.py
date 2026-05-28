from src.genetic.algorithm.entity import Entity
from src.genetic.algorithm.general_entity import GeneralizedEntity

import random

class Path(GeneralizedEntity):
    def __init__(self, length: int, body = None) -> None:
        n_vertex = length - 1
        self.n_vertex = n_vertex
        if body is None:
            body = list(range(n_vertex)) + [0]
        assert len(body) == n_vertex + 1, body
        self.body = body
        super().__init__(n_vertex)
    def getCode(self) -> list:
        return self.body
    def getEntity(self, code: list):
        return Path(len(code), code)
    def setCode(self, code: list):
        assert code[0] == code[-1] == 0
        self.body = code
        self.n_vertex = len(code) - 1
    @classmethod
    def randomize(cls, K, *args, **kwargs) -> 'Path':
        body = [0] + random.sample(range(1, K), K-1) + [0]
        return Path(len(body), body)
    def crossover(self, other: 'Path'):
        x = random.randint(1, self.n_vertex - 1)
        def completePath(begin: list[int], path: list[int]):
            return begin + [v for v in path if v not in begin] + [0]
        other.body, self.body = (
            completePath(other.body[:x], self.body),
            completePath(self.body[:x], other.body)
        )

    def mutate(self, mutation_rate: float = 0.1):
        if random.random() < mutation_rate:
            self.body = [0] + random.sample(self.body[1:-1], self.n_vertex-1) + [0]

    def getRandomGen(self):
        return NotImplemented
    def reproduction(self, other: Entity) -> Entity:
        return NotImplemented