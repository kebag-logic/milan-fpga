#!/usr/bin/env bash
# R399-1 focused reproduction (portable). Args: <processor clone at 81b8d6d7> <packet dir>
# Requires a Verilator 5.050 on PATH (the CI pin). At most 8 parallel jobs.
set -euo pipefail
CLONE=$1; PKT=$2; T=$PKT/scratch/tree
mkdir -p "$T" "$PKT/receipts/suites" "$PKT/receipts/mutants-full" "$PKT/scratch/tmp"
git -C "$CLONE" archive 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b | tar -x -C "$T"
# 1. four focused suites at the exact head
printf '%s\n' srp_top srp_stream_fsms srp_encoder pp_top |
  xargs -P4 -I{} sh -c "make -C $T/tb/{} > $PKT/receipts/suites/{}.log 2>&1; echo {} rc=\$?"
# 2. static gates
(cd "$T" && ./scripts/lint_hdl.sh && make check && python3 scripts/gen_matrix.py --check)
# 3. the full srp_top mutant campaign, 72 arms in 8 chunks (coverage union computed from the outputs)
cd "$T/tb/srp_top"
python3 -c "
import importlib.util
s=importlib.util.spec_from_file_location('m','mutants.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
l=list(dict.fromkeys(x[0] for x in m.MUTANTS));print('\n'.join(','.join(l[i::8]) for i in range(8)))" |
  nl -nln | TMPDIR=$PKT/scratch/tmp xargs -P8 -L1 sh -c "python3 mutants.py --output $PKT/receipts/mutants-full/c\$0 --only \$1 > $PKT/receipts/mutants-full/c\$0.out 2>&1; echo chunk \$0 rc=\$?"
# 4. disposable probes (scratch copies only; no source edits)
cd "$PKT/scratch"
for d in 0 2 3 4 8 16; do DELAYS=$d python3 "$PKT/scripts/probe_arm_race.py" "$T" "$PKT/scratch/probe-armrace-$d"; done
python3 "$PKT/scripts/probe_licence.py" "$T" "$PKT/scratch/probe-licence"
