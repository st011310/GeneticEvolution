from .graph import Graph

def testPathWeight():
    g = Graph([
        [0, 1, 2, 3],
        [3, 0, 1, 2],
        [2, 3, 0, 1],
        [1, 2, 3, 0],
    ])
    assert g.pathWeight([0, 1, 2, 3, 0]) == 4, g.pathWeight([0, 1, 2, 3, 0])


def run():
    testPathWeight()
