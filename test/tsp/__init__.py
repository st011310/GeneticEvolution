from .tests.run import run as testRun

def run():
    try:
        for i in range(3):
            testRun(i)
    except Exception as e:
        print(f"Тест {i}")
        raise e
