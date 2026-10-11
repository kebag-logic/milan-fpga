#!/usr/bin/env bash
# Scratch: one command in the Ubuntu 24.04 image with cmake and clang added (CPython 3.12.3, gcc 13.3, static
# GoogleTest 1.14.0, clang 18, cmake 3.28), the pinned RV32 SDK and the pinned Verilator mounted, on given CPUs.
# usage: inbox6.sh <cpus> <working directory> <command...>
set -euo pipefail
cpus=$1; workdir=$2
shift 2
scratch=$VALIDATION_STORAGE/697c-a583
V=$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff
exec podman run --rm --network=none --userns=keep-id --user "$(id -u):$(id -g)" \
  -e HOME="$scratch/tmpdir" -e TMPDIR="$scratch/tmpdir" -e PYTHONDONTWRITEBYTECODE=1 \
  -e MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc \
  -e VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator \
  -v "$scratch":"$scratch" -v $VALIDATION_TOOLS:$VALIDATION_TOOLS:ro -v "$V":"$V":ro \
  -w "$workdir" localhost/697c-r6-ci:latest taskset -c "$cpus" "$@"
