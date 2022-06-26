#!/usr/bin/env python3

import os, sys

from lib.TestPool import TestPool
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def main(argv):
    data_dir = "."
    if len(argv) == 2:
        data_dir = argv[1]
    elif len(sys.argv) > 2:
        print("expected at most one argument", file=sys.stderr)
        exit(1)

    if not os.path.isdir(data_dir):
        print("not a directory:", data_dir, file=sys.stderr)
        exit(1)

    tp = TestPool(data_dir)

    #table(tp, set(tp.names.keys()).difference(["add"]))
    space(tp, ["add", "dot", "exp"])

def table(tp, tests):
    tests = sorted(tests)

    backends = list(tp.groups.keys())
    backends.remove("matcha")
    backends.insert(0, "matcha")

    for test in tests:
        if test in tp.groups["matcha"]:
            matcha_data = tp.groups["matcha"][test]
        else:
            matcha_data = None

        print("#", 
                test.rjust(20), " ", 
                "mean (ms)".ljust(13), " ", 
                "SD (ms)".ljust(13), " ",
                "t-test"
                )

        for backend in backends:
            if backend not in tp.names[test]: continue
            data = tp.names[test][backend]
            m = np.mean(data) * 1000
            sd = np.std(data, ddof=1) * 1000
            print(" ",
                    backend.rjust(20), " ", 
                    format(m, ".8g").ljust(13), " ", 
                    format(sd, ".8g").ljust(13), " ",
                    end=" "
                    )
            if matcha_data is not None and backend != "matcha":
                statistic, pvalue = scipy.stats.ttest_ind(data, matcha_data, equal_var=False)
                stars = ""
                if pvalue < .001: stars = "***"
                elif pvalue < .01: stars = "**"
                elif pvalue < .05: stars = "*"
                print(stars)
            else:
                print()

        print()


def space(tp, tests):
    for test in tests:
        #fig,ax = plt.subplots()
        backends = tp.names[test]
        xlim = [0, 0]
        ylim = [0, 0]
        for backend in backends:
            data = backends[backend]
            x = data[:, 0]
            y = data[:, 1]
            xlim[0] = min(xlim[0], np.min(x))
            xlim[1] = max(xlim[1], np.max(x))
            ylim[1] = max(ylim[1], np.quantile(y, .95))

            plt.scatter(x, y, label=backend, marker="+")

        plt.legend(loc="upper left")
        plt.xlim(xlim)
        plt.ylim(ylim)

        plt.title(test)
        plt.xlabel("scale")
        plt.ylabel("time [s]")

        plt.show()



if __name__ == "__main__":
    main(sys.argv)
