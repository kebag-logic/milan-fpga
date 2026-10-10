#!/bin/sh
# Usage: suite43.sh <clone> <make-binary-dir> <scratchdir> <verilator> <jobs>
# Full maap suite (`make` = harness run + mutation campaign) with the given GNU make
# first on PATH and an inherited MAKEFLAGS=w, the hosted shape; build trees in scratch.
set -u
C=$1; MB=$2; S=$3; V=$4; J=$5
export PATH="$MB:$PATH"; mkdir -p "$S/tmp"; rm -rf "$S/obj_unit"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1) at $(command -v make) verilator=$($V --version)"
cd / && env MAKEFLAGS=w TMPDIR="$S/tmp" VERILATOR="$V" VERILATOR_JOBS="$J" \
  make -s -C "$C/tb/verilator/maap" all MDIR="$S/obj_unit"
