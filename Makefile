.PHONY: build clean collect_cpp collect_py dump collect

build: 
	@mkdir -p build && cd build && cmake .. && cmake --build .

clean:
	@if [ -d build ]; then rm -rf build; fi
	@if [ -d data ]; then rm -rf data; fi
	@if [ -d out ]; then rm -rf out; fi
	@if [ -L out ]; then rm out; fi

collect: collect_cpp collect_py

collect_cpp: build
	@mkdir -p data/ops
	@./build/matcha-benchmark data/ops

collect_py:
	@mkdir -p data/ops
	@python3 src/collect_py/main.py data/ops

dump:
	@mkdir -p out && python3 src/dump/main.py data/ops out
