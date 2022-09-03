import numpy as np
import scipy.stats
from Test import Test

def init(out_dir: str):
    with open(f"{out_dir}/hypotheses.md", "w") as file:
        print("# Hypothesis testing Matcha vs. TensorFlow", file=file)
        print("""
The following table contains hypothesis tests for specific scales (column "Scale")
extracted from the generated linear space benchmarks (column "Benchmark").
To verify whether the time means are significantly different, the two-sample
independent t-test was used.
        """, file=file)
        print(f"|Benchmark|Scale|Mean Matcha|Mean TensorFlow|SD Matcha|SD TensorFlow|T-test p-value|", file=file)
        print(f"|---------|-----|-----------|---------------|---------|-------------|--------------|", file=file)

def run(tests: list[Test], out_dir: str, hypotheses: int = 5) -> str:

    # extract benchmark metadata - steps, begin, end, n
    x_temp = tests[0].data[:,0]
    n = np.sum(x_temp == x_temp[0])  # get per-step sampling
    steps = len(x_temp) // n
    begin = x_temp[0]
    end = x_temp[steps - 1]

    lsp = np.linspace(begin, end, steps).astype(np.int32)

    # generate hypotheses for x in:
    xs = lsp[:: len(lsp) // hypotheses]

    for x in xs:
        buff = {}
        for test in tests:
            if test.engine.lower() not in ["matcha", "tensorflow"]:
                continue

            ys = test.data[test.data[:,0] == x][:, 1]
            buff[test.engine] = ys


        if min(len(buff["matcha"]), len(buff["tensorflow"])) == 0:
            continue

        t, p = scipy.stats.ttest_ind(buff["matcha"], buff["tensorflow"])
        m_m, sd_m = np.mean(buff["matcha"]), np.std(buff["matcha"], ddof=1)
        m_tf, sd_tf = np.mean(buff["tensorflow"]), np.std(buff["tensorflow"], ddof=1)
        bm = f"{tests[0].operation} {tests[0].generator}"
        scale = x
        ps = f"{p:.3f}"
        if p < 1e-3:
            ps = f"**{ps}**"

        with open(f"{out_dir}/hypotheses.md", "a") as file:
            print(f"|{bm}|{x}|{m_m:.3e}|{m_tf:.3e}|{sd_m:.3e}|{sd_tf:.3e}|{ps}|", file=file)

