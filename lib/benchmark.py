import time
import os
import numpy as np

class Benchmark:
    def __init__(self, group, target = "."):
        self._target = target
        self._group = group

        if not self._target: self._target += "."
        if self._target[-1] != "/": self._target += "/"

        if not os.path.isdir(target):
            raise NotADirectoryError

        self._dir = self._target + self._group
        if self._dir[-1] != "/": self._dir += "/"
        os.makedirs(self._dir, exist_ok=True)


    def run(self, function, n, name):
        with open(self._dir + name + ".txt", "w") as file:
            for _ in range(n):
                begin = time.time()
                function()
                end = time.time()
                duration = end - begin
                print(duration, file=file)

    def space(self, function, space, n, name):
        with open(self._dir + name + ".txt", "w") as file:
            for _ in range(n):
                for scale in space:
                    print(scale)
                    begin = time.time()
                    function(int(scale))
                    end = time.time()
                    duration = end - begin
                    print(scale, '\t', duration, file=file)

    def linspace(self, function, low, high, points, n, name):
        space = np.linspace(low, high, points).astype(int)
        self.space(function, space, n, name)

    def geomspace(self, function, low, high, points, n, name):
        space = np.geomspace(low, high, points).astype(int)
        self.space(function, space, n, name)
