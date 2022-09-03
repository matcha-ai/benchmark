import matplotlib.pyplot as plt
import numpy as np

def get_color(engine):
    """every framework has its brand color"""

    return {
        "matcha": "#71c837",
        "tensorflow": "#ff7400",
        "numpy": "#4dabcf",
    }[engine]

def run(tests, out_dir):
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
