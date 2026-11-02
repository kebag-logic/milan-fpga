#!/bin/sh
# Run the register-reference gates and the read-table sweep at the checkout's head.
# Usage: run_gates.sh CLONE PACKET PYTHON  (PYTHON: an interpreter with wavedrom 2.0.3.post3 and its six dependency)
set -u
C=$1; P=$2; PY=$3
R=$P/receipts; mkdir -p "$R" "$P/scratch/sweep-head"
export PATH="$P/bin:$PATH"
cd "$C" || exit 2
git rev-parse HEAD > "$R/head.txt"
verilator --version > "$R/verilator_version.txt" 2>&1
run() { name=$1; shift; "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
run gen_check    "$PY" scripts/gen_register_reference.py --check &
run gen_selftest "$PY" scripts/gen_register_reference.py --selftest &
run memmap_check "$PY" docs/diagrams/memory_map.gen.py --check &
run doc_style    "$PY" scripts/check_doc_style.py &
run sweep_head   "$PY" scripts/register_read_sweep.py --work "$P/scratch/sweep-head" &
wait
for f in "$R"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
