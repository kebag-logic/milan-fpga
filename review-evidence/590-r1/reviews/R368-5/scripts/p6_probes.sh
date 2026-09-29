#!/usr/bin/env bash
# P6: disposable fault probes on the two fixture commits, run inside a scratch
# clone of the exact head (never the review clone). Each probe mutates one
# file, runs the 1x1 shipping builds without mutants, records the verdict and
# restores the file with git checkout. Usage: p6_probes.sh <scratch clone> <out dir>
set -u
C=$1; OUT=$2; PY=${PY:-python3}
cd "$C/tb/verilator/nvm_cosim"
probe() {  # name, file, python-expression transforming s
  local name=$1 file=$2 expr=$3
  "$PY" - "$file" "$expr" <<'PYEOF'
import sys
p, expr = sys.argv[1], sys.argv[2]
s = open(p).read(); t = eval(expr)
assert t != s, "mutation anchor not found"
open(p, "w").write(t)
PYEOF
  "$PY" -B run_cases.py --shapes 1x1 --jobs 8 --pool 8 --skip-mutants > "$OUT/probe-$name.log" 2>&1
  echo "probe $name rc=$?" | tee -a "$OUT/probe-$name.log"
  git -C "$C" checkout -q -- "tb/verilator/nvm_cosim/$file"
}
# A: nvm_boot() must re-arm nvm_started after the modelled restart; forcing it
#    back to 0 after nvm_boot() must fail W1 (the only restart that re-attaches)
probe A_restart_not_rearmed run_cases.py \
  's.replace("\"\\tset_idle_hook(0);\\n\\tnvm_boot();\\n}\\n\")", "\"\\tset_idle_hook(0);\\n\\tnvm_boot();\\n\\tnvm_started = 0;\\n}\\n\")")'
# B: dropping nvm_started from WRITER_STATICS must be refused (the round-4 bank failure)
probe B_statics_without_started run_cases.py 's.replace("{\"nvm_started\": \"0\", ", "{")'
# C: dropping the cosim host's patch-0006 marker stub must fail the host link on that symbol
probe C_host_without_marker cosim_host.c \
  's.replace("/* The host replaces the BIOS, including its patch-0006 link marker. */\nvoid bios_dispatch_hook_required(void)\n{\n}\n", "")'
git -C "$C" status --porcelain
