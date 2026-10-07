#!/usr/bin/env bash
# Usage: run-probe-rla.sh SNAPSHOT_WITH_BUILD OUTDIR
set -u
snap=$1; out=$2; here=$(cd "$(dirname "$0")" && pwd); mkdir -p "$out"
cc -std=c11 -Wall -I"$snap/src/include" "$here/probe-cross-type-rla.c" -L"$snap/build" -lshlan -Wl,-rpath,"$snap/build" -o "$out/probe-rla" && "$out/probe-rla"
