import csv
from .generator import generateIntMatrix

class Graph:
    def __init__(self, body: list[list[int]]) -> None:
        self.body = body
        self.vertex_count = len(body)
        for row in self.body:
            assert len(row) == self.vertex_count, "Входная матрица не прямоугольная."
    def getVertexNum(self):
        return self.vertex_count
    def V(self):
        return range(self.vertex_count)
    def E(self):
        for u in self.V():
            for v in self.V():
                if u != v:
                    yield (u, v, self.body[u][v])

    def getWeight(self, u, v):
        assert u < self.vertex_count, u
        assert v < self.vertex_count, v
        return self.body[u][v]

    def pathWeight(self, path: list):
        w = 0
        for i in range(1, len(path)):
            u, v = path[i-1], path[i]
            w += self.getWeight(u, v)
        return w

    def save(self, filename):
        with open(filename, mode="w") as file:
            csv.writer(file, strict=True, lineterminator="\n").writerows(self.body)

    @classmethod
    def load(cls, filename):
        with open(filename, mode="r") as file:
            body = [list(map(int, row)) for row in csv.reader(file, strict=True)]
        return cls(body)

    @classmethod
    def random(cls, vertex_count: int):
        return cls(generateIntMatrix(vertex_count, vertex_count))
