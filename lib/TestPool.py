import os
import numpy as np


class TestPool:
    def __init__(self, data_dir):
        if not data_dir: data_dir = "."
        if data_dir[-1] != "/": data_dir += "/"

        groups = os.listdir(data_dir)
        self.groups = {}

        for group in groups:
            tests = {}
            files = os.listdir(data_dir + group)
            group_dir = data_dir + group
            if group_dir[-1] != "/": group_dir += "/"
            for file in files:
                name = os.path.splitext(os.path.basename(file))[0]
                data = np.loadtxt(group_dir + file)
                tests[name] = data
            self.groups[group] = tests

        self.names = {}
        for group in self.groups:
            temp = self.groups[group]
            for name in temp:
                if name in self.names:
                    self.names[name][group] = temp[name]
                else:
                    self.names[name] = {group: temp[name]}

