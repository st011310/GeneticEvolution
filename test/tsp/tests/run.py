from src.graph import Path, Graph
from src.genetic.algorithm import ClassicGA
from .config import GRAPH_FILENAME, OUTPUT_FILENAME, DEFAULT_N

import os

def solve(graph: Graph, **kwargs):
    N = graph.getVertexNum()
    solver = ClassicGA(**kwargs)
    fitness = lambda path: -graph.pathWeight(path.body)
    solver.setFitness(fitness)
    solver.setGenerator(lambda : Path.randomize(N))
    solver.evolve(**kwargs)
    return solver

def run(test_number=1):
    testDir = os.altsep.join([os.curdir, 'test', 'tsp', 'tests', f"test{test_number}"])
    graph_filename = os.altsep.join([testDir, GRAPH_FILENAME])
    output_filename = os.altsep.join([testDir, OUTPUT_FILENAME])
    isFirstTime = os.path.exists(testDir)

    N = DEFAULT_N
    if isFirstTime:
        graph = Graph.load(graph_filename)
        N = graph.getVertexNum()
    else:
        os.mkdir(testDir)
        graph = Graph.random(vertex_count=N)
        graph.save(graph_filename)
    solver = solve(graph, population_size = 500, mutation_rate=.95, verbose = True)
    path = solver.bestEntity
    assert isinstance(path, Path)

    if os.path.exists(output_filename):
        opt_path = Path.load(output_filename)
        assert solver.fitness
        opt_val = solver.fitness(opt_path)
        if opt_val < solver.bestFitness:
            print(f"Лучшее решение побито. Было {opt_val}")
            path.save(output_filename)
        else:
            print(f"Лучшее решение {opt_val} НЕ побито.")
    else:
        path.save(output_filename)
