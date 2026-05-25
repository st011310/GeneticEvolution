import random
import json
import math
from copy import deepcopy
from typing import Callable
from .entity import Entity

class ClassicGA:
    def __init__(self, population_size: int,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7):
        """
        Классический генетический алгоритм.
        --
        population_size : размер популяции
        fitness_func : функция оценки приспособленности, принимает модель и возвращает float
        mutation_rate : вероятность мутации особи
        crossover_rate : вероятность скрещивания
        elitism : сохранять ли лучшую особь в следующее поколение
        """
        self.population_size = population_size
        self.fitness: Callable[[Entity], float] | None
        self.generator: Callable[[], Entity] | None
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population: list[tuple[Entity, float]] = []
        self.bestEntity: Entity | None = None
        self.bestFitness = 0

    def isBest(self, entity: Entity, fitness_rate: float):
        if self.bestEntity is None:
            self.bestEntity = entity
            self.bestFitness = fitness_rate
            return True
        if self.bestFitness < fitness_rate:
            self.bestEntity = entity
            self.bestFitness = fitness_rate
            return True
        return False

    def addEntity(self, entity: Entity, fitness_rate: float | None = None):
        if fitness_rate is None:
            fitness_rate = self.evaluate(entity)
        pair = (entity, fitness_rate)
        self.isBest(*pair)
        self.population.append(pair)

    def setPopulation(self, population: list[Entity]):
        for entity in population:
            self.addEntity(entity)
        self.sortPopulation()

    def deleteEntity(self, entityId: int):
        del self.population[entityId]

    def deleteEntities(self, entityIds: list[int]):
        self.population = [
            ind for i, ind in enumerate(self.population)
            if i not in entityIds
        ]

    def selectRandom(self):
        fitnesses = [fitness for entity, fitness in self.population]
        minFitness = fitnesses[-1]
        fitnessCount = len(fitnesses)
        totalSum = sum(fitnesses) - minFitness * fitnessCount
        if totalSum == 0:
            if fitnessCount == 1:
                return 0
            return random.randint(0, fitnessCount - 1)
        score = random.random()
        for i, fitness in enumerate(fitnesses):
            score -= (fitness - minFitness) / totalSum
            if score <= 0:
                return i
        return 0

    def setGenerator(self, generator: Callable):
        self.generator = generator

    def setFitness(self, fitness: Callable):
        self.fitness = fitness

    def initializePopulation(self,
                             generator: Callable | None = None,
                             count: int | None = None,
                             rewrite = True):
        """Создаёт начальную случайную популяцию"""
        if count is None:
            count = self.population_size - len(self.population)
        if generator is None:
            assert self.generator is not None, "generator is not defined"
            generator = self.generator
        if rewrite: self.population = []
        for _ in range(count):
            self.addEntity(generator())
        self.sortPopulation()

    def entityIterator(self):
        for entity, _ in self.population:
            yield entity

    def sortPopulation(self):
        self.population.sort(key=lambda ind: ind[1], reverse=True)

    def evaluate(self, individual: Entity, fitness: Callable | None  = None) -> float:
        """Вычисляет приспособленность особи"""
        if fitness is None:
            assert self.fitness is not None, "fitness is not defined"
            fitness = self.fitness
        return fitness(individual)

    def crossover(self, i: int, j: int):
        p1 = deepcopy(self.population[i][0])
        p2 = deepcopy(self.population[j][0])
        if random.random() < self.crossover_rate:
            p1.crossover(p2)
        p1.mutate(self.mutation_rate)
        p2.mutate(self.mutation_rate)
        return p1, p2

    def reproduction(self):
        N = len(self.population)
        new_population = []
        for _ in range(self.population_size // 2):
            for entity in self.crossover(self.selectRandom(), self.selectRandom()):
                new_population.append(entity)
        self.setPopulation(new_population)

    def selection(self, limit: int | None = None):
        if limit is None:
            limit = self.population_size
        self.population = self.population[:limit]

    def evolve(self, generations: int, verbose: bool = False) -> Entity:
        """Запуск эволюции на указанное количество поколений"""
        self.initializePopulation(self.generator)

        for gen in range(generations):
            self.reproduction()
            self.selection()

            # Статистика поколения
            if verbose:
                avg_fitness = sum(self.evaluate(ind) for ind, _ in self.population) / self.population_size
                max_fitness = max(self.evaluate(ind) for ind, _ in self.population)
                print(f"Поколение {gen+1}: средняя приспособленность = {avg_fitness:.4f}, лучшая = {max_fitness:.4f}")
        assert self.bestEntity, "Best entity don't found"
        return self.bestEntity
