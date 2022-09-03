import numpy as np

def run(tests):
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

