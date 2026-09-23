#!/usr/bin/env bash
# R227-4: run actual gate 1b through the head's own harness in one disposable
# tree copy. Usage: run_gate.sh <packet> <tree name> <absent|mapped>
# The scoped Verilator 5.050 wrapper is first on PATH; mapped mode maps only
# the absolute selector's argv[0] to the scratch SDK, which the harness
# itself verifies before use.
set -uo pipefail
packet=$1
name=$2
mode=$3
tree="$packet/scratch/gate/$name"
out="$packet/receipts/gate"
mkdir -p "$out"
export PATH="$PINNED_TOOL_BIN:$PATH"
log="$out/$name.$mode.log"
audit="$packet/scratch/audit/$name.$mode.jsonl"
mkdir -p "$packet/scratch/audit"
if [ "$mode" = mapped ]; then
    set -- --sdk-destination "$packet/scratch/sdk"
else
    set -- --absent
fi
start=$(date +%s)
{
    echo "verilator: $(command -v verilator) :: $(verilator --version)"
    echo "tree: $name mode: $mode"
    echo "test_builder.py sha256: $(sha256sum < "$tree/sw/builder/test_builder.py" | cut -d' ' -f1)"
    (cd "$tree" && python3 -B -u sw/builder/test_firmware_compiler.py "$@" --audit "$audit")
    status=$?
    echo "EXIT $status after $(( $(date +%s) - start ))s"
} > "$log" 2>&1
tail -n 1 "$log" | sed "s#^#$name.$mode #"
