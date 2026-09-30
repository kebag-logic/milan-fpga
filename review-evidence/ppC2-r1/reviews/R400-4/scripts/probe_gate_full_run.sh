#!/usr/bin/env bash
# Disposable probe: plant C3's gate-enable-dropped patch in a git-archive export of
# <repo>@<rev> and run pp_top's full default run; print its FAIL lines and tallies.
# usage: probe_gate_full_run.sh <repo> <rev> <scratch-dir>   (Verilator capped by PATH wrapper)
set -uo pipefail
R=${1:?repo}; REV=${2:?rev}; P=${3:?scratch}/probe-gate
rm -rf "$P"; mkdir -p "$P"
git -C "$R" archive "$REV" | tar -x -C "$P"
cd "$P" && git apply --check tb/adp_engine/mutations/gate-enable-dropped.patch \
  && git apply tb/adp_engine/mutations/gate-enable-dropped.patch || exit 3
make -C tb/pp_top run > "$P.log" 2>&1; rc=$?
echo "rc=$rc"; grep '^FAIL' "$P.log"; grep -E 'checks, [0-9]+ failures' "$P.log" | tail -4
