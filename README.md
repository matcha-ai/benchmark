# Matcha benchmark generator

## Requirements

- Matcha headers and compiled binaries
- Numpy, TensorFlow
- Matplotlib, Scipy

## Usage

To build the C++ benchmarking program (into `build/`):

```sh
make build
```

To run C++ benchmarking, python benchmarking, or both
(collected data will be stored in `data/`):

```sh
make collect_cpp
make collect_py
make collect
```

To generate final figures and text files from collected `data/` into `out/`:

```sh
make dump
```

To clean everything:

```sh
make clean
```
