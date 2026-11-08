#!/usr/bin/env bash
# Build and run milan_dp's crflic leg in a disposable clone, optionally with a
# harness edit applied to sim_crf_licence.cpp (exact fragment, must occur once).
# usage: probe_onevec.sh <clone> <name> <outdir> [<fragment> <replacement>]
set -u
clone=$1 name=$2 out=$3; frag=${4-}; repl=${5-}
V=${VERILATOR_BIN:?set VERILATOR_BIN to the pinned Verilator 5.050 wrapper}
mkdir -p "$out"
cd "$clone/tb/verilator/milan_dp" || exit 9
if [ -n "$frag" ]; then
  python3 -I - "$frag" "$repl" <<'PY' || { echo 8 > "$out/$name.rc"; exit 8; }
import sys
f = "sim_crf_licence.cpp"; s = open(f).read(); a, b = sys.argv[1], sys.argv[2]
n = s.count(a)
if n != 1: sys.exit(f"fragment count {n}")
open(f, "w").write(s.replace(a, b)); print("edited", f)
PY
fi
{ echo "clone_head $(git -C "$clone" rev-parse HEAD)"; echo "pp $(git -C "$clone/protocol-processor" rev-parse HEAD)";
  git -C "$clone" diff --stat; date -Is; } > "$out/$name.meta"
make -s VERILATOR="$V" crflic CRFLIC_MDIR=obj_r789_$name > "$out/$name.log" 2>&1
echo $? > "$out/$name.rc"; date -Is >> "$out/$name.meta"
