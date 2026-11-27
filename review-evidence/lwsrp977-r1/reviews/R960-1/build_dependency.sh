#!/usr/bin/env bash
set -euo pipefail
packet=$(cd "$(dirname "$0")" && pwd)
scratch="$packet/scratch"
if ! test -d "$scratch/cgreen/.git"; then
    git init "$scratch/cgreen"
    git -C "$scratch/cgreen" remote add origin https://github.com/cgreen-devs/cgreen.git
    git -C "$scratch/cgreen" fetch --depth 1 origin 25137a17132ed7d7e5fd7bb9a6129aec34b49107
    git -C "$scratch/cgreen" checkout --detach FETCH_HEAD
fi
test "$(git -C "$scratch/cgreen" rev-parse HEAD)" = 25137a17132ed7d7e5fd7bb9a6129aec34b49107
cmake -S "$scratch/cgreen" -B "$scratch/cgreen-build" -DCMAKE_BUILD_TYPE=Release -DCGREEN_WITH_UNIT_TESTS=OFF -DCGREEN_WITH_STATIC_LIBRARY=OFF -DCMAKE_INSTALL_PREFIX="$scratch/cgreen-prefix"
make -C "$scratch/cgreen-build" -j16
cmake --install "$scratch/cgreen-build"
