import benchmark


def test_backend(backend, group):
    print(group)

    def binary_op(op, a, b):
        ta = backend.ones(a)
        tb = backend.ones(b)
        tc = op(ta, tb)

    def unary_op(op, a):
        ta = backend.ones(a)
        tc = op(ta)

    def binary_op_tiny(op):
        binary_op(op, [1, 1], [1, 1])

    def unary_op_tiny(op):
        unary_op(op, [1, 1])

    def binary_op_small(op):
        binary_op(op, [7, 7], [7, 7])

    def binary_op_small_scalar(op):
        binary_op(op, [7, 7], [])

    def binary_op_small_broadcast(op):
        binary_op(op, [7, 7], [7, 1])

    def unary_op_small(op):
        unary_op(op, [7, 7])

    def binary_op_big(op):
        binary_op(op, [1000, 1000], [1000, 1000])

    def binary_op_big_scalar(op):
        binary_op(op, [1000, 1000], [])

    def binary_op_big_broadcast(op):
        binary_op(op, [1000, 1000], [1000, 1])

    def unary_op_big(op):
        unary_op(op, [1000, 1000])

    def binary_op_huge(op):
        binary_op(op, [10000, 10000], [10000, 10000])

    def binary_op_huge_scalar(op):
        binary_op(op, [10000, 10000], [])

    def binary_op_huge_broadcast(op):
        binary_op(op, [10000, 10000], [10000, 1])

    def unary_op_huge(op):
        unary_op(op, [10000, 10000])

    def binary_op_scale(op, scale):
        binary_op(op, [scale], [scale])

    def unary_op_scale(op, scale):
        unary_op(op, [scale])

    def binary_op_scale_square(op, scale):
        binary_op(op, [scale, scale], [scale, scale])

    bm = benchmark.Benchmark(group, "/home/patz/benchmark/data/")

    bm.linspace(
            lambda s: binary_op_scale(backend.add, s),
            1, 5_000_000, 100, 10, "add"
            )

    bm.linspace(
            lambda s: binary_op_scale_square(backend.dot, s),
            1, 3_000, 100, 10, "dot"
            )

    bm.linspace(
            lambda s: unary_op_scale(backend.exp, s),
            1, 5_000_000, 100, 10, "exp"
            )

    return

    print("  add")
    bm.run(lambda: binary_op_tiny(backend.add), 300, "add_tiny")
    bm.run(lambda: binary_op_small(backend.add), 100, "add_small")
    bm.run(lambda: binary_op_small_scalar(backend.add), 100, "add_small_scalar")
    bm.run(lambda: binary_op_small_broadcast(backend.add), 100, "add_small_broadcast")
    bm.run(lambda: binary_op_big(backend.add), 100, "add_big")
    bm.run(lambda: binary_op_big_scalar(backend.add), 100, "add_big_scalar")
    bm.run(lambda: binary_op_big_broadcast(backend.add), 100, "add_big_broadcast")
    bm.run(lambda: binary_op_huge(backend.add), 20, "add_huge")
    bm.run(lambda: binary_op_huge_scalar(backend.add), 20, "add_huge_scalar")
    bm.run(lambda: binary_op_huge_broadcast(backend.add), 20, "add_huge_broadcast")

    print("  dot")
    bm.run(lambda: binary_op_tiny(backend.dot), 300, "dot_tiny")
    bm.run(lambda: binary_op_small(backend.dot), 100, "dot_small")
    bm.run(lambda: binary_op_big(backend.dot), 100, "dot_big")

    print("  exp")
    bm.run(lambda: unary_op_tiny(backend.exp), 300, "exp_tiny")
    bm.run(lambda: unary_op_small(backend.exp), 100, "exp_small")
    bm.run(lambda: unary_op_big(backend.exp), 100, "exp_big")
    bm.run(lambda: unary_op_huge(backend.exp), 20, "exp_huge")

if __name__ == "__main__":
    import numpy as np
    import tensorflow.experimental.numpy as tf

    test_backend(np, "numpy")
    test_backend(tf, "tensorflow")
