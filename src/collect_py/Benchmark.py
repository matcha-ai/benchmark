import numpy as np
import time

class Generator:
    """named generator wrapper
    """

    def __init__(self, name, internal):
        self.name = name
        self.internal = internal

class Payload:
    """named payload wrapper
    """

    def __init__(self, name, internal):
        self.name = name
        self.internal = internal

class Benchmark:
    """benchmark family wrapper
    """

    def __init__(self, out_dir, engine):
        self.out_dir = out_dir
        self.engine = engine

    def linspace(self, space: list, n: int, payload: Payload, generator: Generator):
        """benchmark payload on pre-generated inputs from a linear space of scales
        """

        name = f"linspace {self.engine} {payload.name} {generator.name}"
        with open(f"{self.out_dir}/{name}.txt", "w") as file:
            for i in range(n):
                for j in space:
                    scale = int(j)
                    inputs = generator.internal(scale)

                    time0 = time.time()
                    payload.internal(inputs)
                    time1 = time.time()

                    duration = time1 - time0
                    seconds = duration
                    print(scale, "\t", seconds, file=file)
                    print(scale, "\t", seconds)
