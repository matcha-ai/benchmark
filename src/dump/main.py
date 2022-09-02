#!/usr/bin/env python3

import os, sys
import numpy as np
from Test import Test
#import scipy.stats
import matplotlib.pyplot as plt

def get_color(engine):
    """every framework has its brand color"""

    return {
        "matcha": "#71c837",
        "tensorflow": "#ff7400",
        "numpy": "#4dabcf",
    }[engine]

def make_data(tests):
    """extract quantitative data from the tests"""

    data = {}
    for test in tests:
        x = test.data[:, 0]
        y = test.data[:, 1]

        deg = 3
        coef = np.ndarray([deg + 1])
        regression = np.polynomial.Polynomial(coef)
        regression = regression.fit(x, y, deg)

        temp = y[x.argsort()]
        n = np.sum(x == x[0])
        mrsd = 0
        for i in range(0, len(temp), n):
            temp2 = y[i:i+n]
            mrsd += np.std(temp2) / np.mean(temp2)

        mrsd /= (len(temp) / n)

        data[test.engine] = [mrsd, *regression.coef]

    return data

def make_plot(tests, out_dir):
    """generate a single plot from the tests"""

    name = f"{tests[0].operation} {tests[0].generator}"
    filename = f"{tests[0].operation}-{tests[0].generator}.jpeg"
    path = f"{out_dir}/media/{filename}"
    return filename

    xlim = [0, 0]
    ylim = [0, 0]
    plt.figure(figsize=(8,4))


    for test in tests:
        x = test.data[:, 0]
        y = test.data[:, 1]
        engine = test.engine
        color = get_color(engine)
        plt.scatter(x, y, label=engine, marker="+", color=color)
        xlim[0] = min(xlim[0], np.min(x))
        xlim[1] = max(xlim[1], np.max(x))
        ylim[1] = max(ylim[1], np.quantile(y, .95))


    plt.legend(loc="upper left")
    plt.xlim(xlim)
    plt.ylim(ylim)

    #plt.title(name)
    plt.xlabel("scale")
    plt.ylabel("time [s]")

    plt.savefig(path)
    plt.clf()
    plt.close()
    return filename

def dump_op(op, tests, file, out_dir):
    media = f"{out_dir}/media"
    os.makedirs(media, exist_ok=True)
    by_generator = {}
    for test in tests:
        if test.generator not in by_generator: 
            by_generator[test.generator] = []
        by_generator[test.generator] += [test]

    print(f"## {op}", file=file)
    print(file=file)

    #print(op)
    #print(sorted(by_generator))

    for gen in sorted(by_generator):
        tests = sorted(by_generator[gen], key=lambda test: test.engine)
        #print([test.engine for test in tests])
        data = make_data(tests)
        plot = make_plot(tests, out_dir)

        print(f"#### {gen}", file=file)


        print(file=file)

        print("|Engine|Mean Relative SD|Constant overhead|Linear coef|Quadratic coef|Cubic coef|", file=file)
        print("|------|----------------|-----------------|-----------|--------------|----------|", file=file)

        for engine in data:
            mrsd = data[engine][0]
            buff1 = f"{mrsd * 100:.1f}%"
            if mrsd < .3:
                buff1 = f"_{buff1}_"
            if mrsd > .6:
                buff1 = f"**{buff1}**"


            coefs = data[engine][1:]
            buff2 = []
            for coef in coefs:
                s = f"{coef:0.3e}"
                if coef == min(coefs):
                    buff2.append(f"_{s}_")
                elif coef == max(coefs):
                    buff2.append(f"**{s}**")
                else:
                    buff2.append(s)

            print(f"|{engine}|{buff1}|" + "|".join(buff2) + "|", file=file)

        print(file=file)
        print(f"![img](media/{plot})", file=file)

    print(file=file)

def main(argv):
    data_dir = argv[1]
    out_dir = argv[2]

    tests = [Test(f"{data_dir}/{file}") for file in os.listdir(data_dir)]

    by_op = {}
    for test in tests:
        if test.operation not in by_op: by_op[test.operation] = []
        by_op[test.operation] += [test]

    with open(f"{out_dir}/ops.md", "w") as file:
        print("""# Operation benchmarks

This section documents the performance of Matcha operations
in comparison with other popular computing libraries,
sorted by operation type. The operations
have been tested on broad linear spaces of input scales fed into
the following input generators:

- `matrix_rect(scale)` - generates `Float[scale, max(scale / 2, 1)]` inputs
- `matrix_square(scale)` - generates `Float[scale, scale]` inputs
- `vector(scale)` - generates `Float[scale]` inputs

Note that input generation was performed always before the benchmarking
itself to avoid errors caused by the potential generation overhead.

For numeric relationships, the data have been fitted by the polynomial 
regression of degree 3:

$ y = a_0 + a_1 x + a_2 x^2 + a_3 x^3 $

The Mean Relative Standard Deviation reports the mean of the following value
calculated per $ \\vec{b} $ vector of time datapoints with the same `scale`:

$ \\textrm{rsd} = \\frac{\sqrt{ \\textrm{var} ( \\vec{b} )} }{ \\textrm{mean} ( \\vec{b} ) } $

This file and all shown benchmarks have been generated automatically.

""", file=file)


        for op in sorted(by_op):
            dump_op(op, by_op[op], file, out_dir)


if __name__ == "__main__":
    main(sys.argv)
