#!/usr/bin/env bash
# Run gate 1b (sw/builder/test_firmware_compiler.py) once with the pinned RV32
# SDK mapped and once with every cross compiler hidden, in parallel, from a
# given checkout. Usage: run_gate1b_pair.sh <checkout> <sdk-dir> <out-dir> <prefix>
set -u
checkout=$1
sdk=$2
out=$3
prefix=$4
verilator_bin=${VERILATOR_BIN_DIR:-}
if [ -n "$verilator_bin" ]; then
  PATH="$verilator_bin:$PATH"
  export PATH
fi
mkdir -p "$out"
cd "$checkout" || exit 2
echo "checkout: $(git rev-parse HEAD 2>/dev/null || echo no-git)" > "$out/$prefix-env.txt"
echo "verilator: $(command -v verilator) $(verilator --version 2>&1)" >> "$out/$prefix-env.txt"
start=$(date +%s)
(
  python3 -B sw/builder/test_firmware_compiler.py --sdk-destination "$sdk" \
    --audit "$out/$prefix-sdk.audit.jsonl" > "$out/$prefix-sdk.log" 2>&1
  echo "exit=$?" >> "$out/$prefix-sdk.log"
) &
(
  python3 -B sw/builder/test_firmware_compiler.py --absent \
    --audit "$out/$prefix-absent.audit.jsonl" > "$out/$prefix-absent.log" 2>&1
  echo "exit=$?" >> "$out/$prefix-absent.log"
) &
wait
echo "elapsed $(( $(date +%s) - start ))s" >> "$out/$prefix-env.txt"
tail -n 3 "$out/$prefix-sdk.log" "$out/$prefix-absent.log"
cat "$out/$prefix-env.txt"
