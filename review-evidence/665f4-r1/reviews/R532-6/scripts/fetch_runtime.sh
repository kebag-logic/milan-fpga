#!/bin/bash
# Fetch the size fixture's external runtime sources (LiteX at the repository pin; picolibc and compiler-rt from LiteX's data packages).
set -e; cd "$1"
git clone -q https://github.com/enjoy-digital/litex.git litex && git -C litex checkout -q a1e1c3652ec2f1346ebaea7663d2867f393ae2c4
git clone -q --depth 1 --recurse-submodules --shallow-submodules https://github.com/litex-hub/pythondata-software-picolibc.git picolibc
git clone -q --depth 1 https://github.com/litex-hub/pythondata-software-compiler_rt.git compiler_rt
for d in litex picolibc compiler_rt; do echo "$d $(git -C $d rev-parse HEAD)"; done
git -C picolibc submodule status
