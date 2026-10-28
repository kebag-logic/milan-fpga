#!/bin/bash
# build the parent CI-pinned tsn-gen field oracle (rtl.yml TSN_GEN_REV) under $1
set -euo pipefail
d="$1"; rev=deca300c9eb4863fa13383b45ba6cb6fd0828671
[ -d "$d/.git" ] || git clone -q --filter=blob:none https://github.com/kebag-logic/tsn-gen.git "$d"
git -C "$d" checkout -q "$rev"
git -C "$d" submodule update --init --depth 1 --recursive external/rapidyaml
cmake -S "$d" -B "$d/build" -DCMAKE_BUILD_TYPE=Release -DENABLE_PARSER_TESTS=OFF
cmake --build "$d/build" --target packet_gen --parallel 4
test -x "$d/build/traffic-gen/packet_gen"
git -C "$d" rev-parse HEAD
