#!/bin/bash
set -euo pipefail
packet=$(cd "$(dirname "$0")/.." && pwd)
work="$packet/scratch"
curl -fL --retry 2 https://ftp.gnu.org/gnu/make/make-4.3.tar.gz -o "$work/make-4.3.tar.gz"
sha256sum "$work/make-4.3.tar.gz"
tar -xzf "$work/make-4.3.tar.gz" -C "$work"
cd "$work/make-4.3"
./configure --prefix="$work/make43"
make -j16
make -j16 install
"$work/make43/bin/make" --version
