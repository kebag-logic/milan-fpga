#!/usr/bin/env bash
# R399-2 focused reproduction (portable). Args: <processor clone at 412efeb7> <packet dir>
# Requires a Verilator 5.050 on PATH (the CI pin). At most 8 parallel jobs.
# Every build and probe runs in a git-archive copy under <packet>/scratch; the
# clone is never written.
set -euo pipefail
HEAD=412efeb750e358a65b04bae1cbb3086134d15b7e
CLONE=$1; PKT=$2; T=$PKT/scratch/tree; S=$PKT/scripts
mkdir -p "$T" "$PKT/receipts/suites" "$PKT/receipts/mutants-full" "$PKT/receipts/probe-armrace" "$PKT/scratch/tmp"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$T"
# 1. four focused suites at the exact head
printf '%s\n' srp_top srp_stream_fsms srp_encoder pp_top |
  xargs -P4 -I{} sh -c "make -C $T/tb/{} > $PKT/receipts/suites/{}.log 2>&1; echo {} rc=\$?"
# 2. static gates
(cd "$T" && ./scripts/lint_hdl.sh > "$PKT/receipts/lint_hdl.log" 2>&1 && make check > "$PKT/receipts/make_check.log" 2>&1 \
  && python3 scripts/gen_matrix.py --check > "$PKT/receipts/gen_matrix.log" 2>&1)
git -C "$CLONE" diff --check c951a9ff0cb5851fb159d33e966e5a2a9a188fe3 "$HEAD"
# 3. the full srp_top mutant campaign in 8 chunks (coverage union computed from the outputs)
cd "$T/tb/srp_top"
python3 -c "
import importlib.util
s=importlib.util.spec_from_file_location('m','mutants.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
l=list(dict.fromkeys(x[0] for x in m.MUTANTS));print('\n'.join(','.join(l[i::8]) for i in range(8)))" |
  nl -nln | TMPDIR=$PKT/scratch/tmp xargs -P8 -L1 sh -c "python3 mutants.py --output $PKT/receipts/mutants-full/c\$0 --only \$1 > $PKT/receipts/mutants-full/c\$0.out 2>&1; echo chunk \$0 rc=\$?"
# 4. round-1 probes, unmodified
cd "$PKT/scratch"
printf '%s\n' 0 2 3 4 8 16 | xargs -P6 -I{} sh -c "DELAYS={} python3 $S/probe_arm_race.py $T $PKT/scratch/probe-armrace-{}"
cp "$PKT"/scratch/probe-armrace-*/armrace-*.log "$PKT/receipts/probe-armrace/"
python3 "$S/probe_licence.py" "$T" "$PKT/scratch/probe-licence"
# 5. round-2 guard probes: wrap sweep, arm delay 16, dropped re-arm (jobs file), then the
#    deadline exactly at the 32-bit wrap for P8/M10/P6, then extra guard mutants on the full suite
"$S/run_guard_sweep.sh" "$T" "$PKT/scratch/pg" "$S/guard_jobs.txt"
N=$(( 4294967296 - 14097 ))
for g in armdelay peer restart; do for m in - unsigned-compare; do echo "$g $m"; done; done |
  xargs -P6 -L1 bash -c 'mm=$2; nm=$2; [ "$mm" = "-" ] && mm="" && nm=head; NOW0='$N' ARM=0 MUT=$mm DROP=0 GROUP=$1 \
    python3 '$S'/probe_guard.py '$T' '$PKT'/scratch/pgw "w14097-$1-$nm" >/dev/null 2>&1 || true' _
printf '%s\n' unsigned-compare age-le-zero cross-deadline mvrp-no-deadline |
  xargs -P4 -I{} bash -c 'NOW0=0 ARM=0 MUT={} DROP=0 GROUP= python3 '$S'/probe_guard.py '$T' '$PKT'/scratch/pgm suite-{} >/dev/null 2>&1 || true'
