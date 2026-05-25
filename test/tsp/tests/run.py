from .. import ClassicGA, Path, Graph
from .configue import GRAPH_FILENAME, OUTPUT_FILENAME, DEFAULT_N

import os

def run(test_number=1):
    testDir = os.altsep.join([os.curdir, 'test', 'tsp', 'tests', f"test{test_number}"])
    graph_filename = os.altsep.join([testDir, GRAPH_FILENAME])
    output_filename = os.altsep.join([testDir, OUTPUT_FILENAME])
    isFirstTime = os.path.exists(testDir)

    if isFirstTime:
        graph = Graph.load(graph_filename)
    else:
        os.mkdir(testDir)
        graph = Graph.random(vertex_count=DEFAULT_N)
        graph.save(graph_filename)

    solver = ClassicGA(500, mutation_rate=.95)
    fitness = lambda path: -graph.pathWeight(path.body)
    solver.setFitness(fitness)
    solver.setGenerator(lambda : Path.randomize(DEFAULT_N))
    solver.evolve(1000, verbose=True)
    path = solver.bestEntity
    assert isinstance(path, Path)

    if isFirstTime:
        opt_path = Path.load(output_filename)
        opt_val = fitness(opt_path)
        if opt_val < solver.bestFitness:
            print(f"Лучшее решение побито. Было {opt_val}")
            path.save(output_filename)
        else:
            print(f"Лучшее решение {opt_val} НЕ побито.")
    else:
        path.save(output_filename)
