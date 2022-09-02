import numpy as np

class Test:
    """single benchmark test wrapper"""

    def __init__(self, file):
        self.name = ".".join(file.split("/")[-1].split(".")[:-1])
        tokens = self.name.split(" ")
        self.engine = tokens[1]
        self.operation = tokens[2]
        self.generator = tokens[3]
        self.data = np.loadtxt(file)

