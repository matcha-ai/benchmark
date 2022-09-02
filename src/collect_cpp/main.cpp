#include <iostream>
#include <matcha>
#include "Benchmark.h"

int main(int argc, const char** argv) {
  // create benchmark family
  Benchmark bm(argv[1], "matcha");

  // declare generators
  Generator vector("vector",
                   [](size_t a) { return matcha::ones(a); });
  Generator matrix_square("matrix_square",
                          [](size_t a) { return matcha::ones(a, a); });
  Generator matrix_rect("matrix_rect",
                          [](size_t a) { return matcha::ones(a, (int) fmax(1, a / 2)); });

  // declare payloads
  Payload add("add",
              [](const tensor& x) { return x + x; });
  Payload multiply("multiply",
              [](const tensor& x) { return x * x; });
  Payload divide("divide",
                   [](const tensor& x) { return x / x; });
  Payload exp("exp",
              [](const tensor& x) { return matcha::exp(x); });
  Payload transpose("transpose",
              [](const tensor& x) { return matcha::transpose(x); });
  Payload matmul("matmul",
              [](const tensor& x) { return matcha::matmul(x, x); });
  Payload max("max",
                 [](const tensor& x) { return matcha::max(x, -1); });
  Payload sum("sum",
              [](const tensor& x) { return matcha::sum(x, -1); });
  Payload relu("relu",
              [](const tensor& x) { return matcha::nn::softmax(x); });
  Payload softmax("softmax",
               [](const tensor& x) { return matcha::nn::softmax(x); });
  Payload tanh("tanh",
                  [](const tensor& x) { return matcha::tanh(x); });

  int n1 = 16;
  std::tuple lsp1 = {5, 500, 100};
  std::tuple lsp2 = {1, 100'000, 100};


  // run benchmarks
  bm.linspace(lsp1, n1, matrix_square, add);
  bm.linspace(lsp1, n1, matrix_rect, add);
  bm.linspace(lsp2, n1, vector, add);

  bm.linspace(lsp1, n1, matrix_square, multiply);
  bm.linspace(lsp1, n1, matrix_rect, multiply);
  bm.linspace(lsp2, n1, vector, multiply);

  bm.linspace(lsp1, n1, matrix_square, divide);
  bm.linspace(lsp1, n1, matrix_rect, divide);
  bm.linspace(lsp2, n1, vector, divide);

  bm.linspace(lsp1, n1, matrix_square, exp);
  bm.linspace(lsp1, n1, matrix_rect, exp);
  bm.linspace(lsp2, n1, vector, exp);

  bm.linspace(lsp1, n1, matrix_square, transpose);
  bm.linspace(lsp1, n1, matrix_rect, transpose);

  bm.linspace(lsp1, n1, matrix_square, matmul);

  bm.linspace(lsp1, n1, matrix_rect, max);
  bm.linspace(lsp1, n1, matrix_square, max);
  bm.linspace(lsp2, n1, vector, max);

  bm.linspace(lsp1, n1, matrix_rect, sum);
  bm.linspace(lsp1, n1, matrix_square, sum);
  bm.linspace(lsp2, n1, vector, sum);

  bm.linspace(lsp1, n1, matrix_square, relu);
  bm.linspace(lsp1, n1, matrix_rect, relu);
  bm.linspace(lsp2, n1, vector, relu);

  bm.linspace(lsp1, n1, matrix_square, softmax);
  bm.linspace(lsp1, n1, matrix_rect, softmax);
  bm.linspace(lsp2, n1, vector, softmax);

  bm.linspace(lsp1, n1, matrix_square, tanh);
  bm.linspace(lsp1, n1, matrix_rect, tanh);
  bm.linspace(lsp2, n1, vector, tanh);
  return 0;
}
