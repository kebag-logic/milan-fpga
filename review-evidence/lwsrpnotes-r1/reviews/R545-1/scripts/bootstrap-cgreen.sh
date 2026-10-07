#!/usr/bin/env bash
set -euo pipefail
packet=$(cd -- "$(dirname -- "$0")/.." && pwd)
scratch="$packet/scratch"
curl --fail --location --retry 2 https://api.github.com/repos/cgreen-devs/cgreen/tarball/1.7.0 -o "$scratch/cgreen-1.7.0.tar.gz"
sha256sum "$scratch/cgreen-1.7.0.tar.gz"
mkdir "$scratch/cgreen-source"
tar -xzf "$scratch/cgreen-1.7.0.tar.gz" --strip-components=1 -C "$scratch/cgreen-source"
cmake -S "$scratch/cgreen-source" -B "$scratch/cgreen-build" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$scratch/cgreen-prefix" -DWITH_CXX=OFF
make -C "$scratch/cgreen-build" -j16
make -C "$scratch/cgreen-build" install
