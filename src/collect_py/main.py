#!/usr/bin/env python3

import os
import sys
from Benchmark import *
import numpy as np
import tensorflow as tf

from types import ModuleType


def test_engine(name: str, engine: ModuleType, out_dir: str):
    # create benchmark family
    bm = Benchmark(out_dir, name)

    # create generators
    vector = Generator("vector", 
            lambda a: engine.ones([a], dtype="float64"))
    matrix_square = Generator("matrix_square", 
            lambda a: engine.ones([a, a], dtype="float64"))
    matrix_rect = Generator("matrix_rect", 
            lambda a: engine.ones([a, max([a//2, 1])], dtype="float64"))

    # create payloads
    add = Payload("add", lambda x: engine.add(x, x))
    multiply = Payload("multiply", lambda x: engine.multiply(x, x))
    divide = Payload("divide", lambda x: engine.divide(x, x))
    exp = Payload("exp", lambda x: engine.exp(x))
    transpose = Payload("transpose", lambda x: engine.transpose(x))
    matmul = Payload("matmul", lambda x: engine.matmul(x, x))
    mmax = Payload("max", lambda x: engine.max(x, axis=-1))
    ssum = Payload("sum", lambda x: engine.sum(x, axis=-1))
    relu = Payload("relu", lambda x: tf.nn.relu(x))
    softmax = Payload("softmax", lambda x: tf.nn.softmax(x))
    tanh = Payload("tanh", lambda x: engine.tanh(x))

    n1 = 16
    lsp = np.linspace(5, 500, 100)
    lsp2 = np.linspace(5, 100_000, 100)

    # run benchmarks
    bm.linspace(lsp, n1, add, matrix_square)
    bm.linspace(lsp, n1, add, matrix_rect)
    bm.linspace(lsp2, n1, add, vector)

    bm.linspace(lsp, n1, multiply, matrix_square)
    bm.linspace(lsp, n1, multiply, matrix_rect)
    bm.linspace(lsp2, n1, multiply, vector)

    bm.linspace(lsp, n1, divide, matrix_square)
    bm.linspace(lsp, n1, divide, matrix_rect)
    bm.linspace(lsp2, n1, divide, vector)

    bm.linspace(lsp, n1, exp, matrix_square)
    bm.linspace(lsp, n1, exp, matrix_rect)
    bm.linspace(lsp2, n1, exp, vector)

    bm.linspace(lsp, n1, transpose, matrix_square)
    bm.linspace(lsp, n1, transpose, matrix_rect)

    bm.linspace(lsp, n1, matmul, matrix_square)

    bm.linspace(lsp, n1, mmax, matrix_square)
    bm.linspace(lsp, n1, mmax, matrix_rect)
    bm.linspace(lsp2, n1, mmax, vector)

    bm.linspace(lsp, n1, ssum, matrix_square)
    bm.linspace(lsp, n1, ssum, matrix_rect)
    bm.linspace(lsp2, n1, ssum, vector)

    bm.linspace(lsp, n1, tanh, matrix_square)
    bm.linspace(lsp, n1, tanh, matrix_rect)
    bm.linspace(lsp2, n1, tanh, vector)

    if engine != np:
        # numpy is not a deep learning library
        bm.linspace(lsp, n1, relu, matrix_square)
        bm.linspace(lsp, n1, relu, matrix_rect)
        bm.linspace(lsp2, n1, relu, vector)
        bm.linspace(lsp, n1, softmax, matrix_square)
        bm.linspace(lsp, n1, softmax, matrix_rect)
        bm.linspace(lsp2, n1, softmax, vector)


def main(argv: list[str]):
    out_dir = argv[1]

    import numpy as np
    test_engine("numpy", np, out_dir)
    import tensorflow.experimental.numpy as tnp
    test_engine("tensorflow", tnp, out_dir)


if __name__ == "__main__":
    main(sys.argv)
