#!/bin/bash
set -e
cd /w
gcc --version | head -1; cmake --version | head -1; dpkg -l libgtest-dev | tail -1
cmake -S . -B /b -DTSN_COVERAGE=ON -DCMAKE_BUILD_TYPE=Debug
cmake --build /b -j16
ctest --test-dir /b --output-on-failure -j16
python3 scripts/coverage.py /b --write
cat tests/coverage.ratchet
