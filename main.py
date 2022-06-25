#!/usr/bin/env python3

import os, sys

from lib.TestPool import TestPool
import numpy as np
import scipy.stats

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

    tests = sorted(tp.names.keys())

    backends = list(tp.groups.keys())
    backends.remove("matcha")
    backends.insert(0, "matcha")

    for test in tests:
        matcha_data = tp.groups["matcha"][test]

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
                    format(m, ".8f").ljust(13), " ", 
                    format(sd, ".8f").ljust(13), " ",
                    end=" "
                    )
            if backend != "matcha":
                statistic, pvalue = scipy.stats.ttest_ind(data, matcha_data, equal_var=False)
                stars = ""
                if pvalue < .001: stars = "***"
                elif pvalue < .01: stars = "**"
                elif pvalue < .05: stars = "*"
                print(stars)
            else:
                print()

        print()

if __name__ == "__main__":
    main(sys.argv)
