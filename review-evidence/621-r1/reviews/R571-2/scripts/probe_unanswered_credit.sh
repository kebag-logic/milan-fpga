#!/bin/sh
# Usage: probe_unanswered_credit.sh <repo-root> <scratch-dir> <receipt-dir>
# Negative-path probe for the crossing-exchange liveness credit.
#  nocease        : donor generator with the Milan 4.2.6.2.5 cease rule removed
#                   from the 1 s timer program (the ROM has no free words; this
#                   only makes room, and the step regression has one responder)
#  credit_on_step : nocease plus liveness credit (S_PDGOT) for a request that
#                   overlapped a PHC step (S_PDSTEP), whether or not its
#                   exchange ever completed
#  variant        : scratch copy of the step regression in which the peer also
#                   ignores the crossing request (silence starts at the probe)
# Runs: {nocease, credit_on_step} x {real, variant} harness, and clean x variant.
set -u
root=$1; scratch=$2; out=$3
gen="$root/gptp-processor/hdl/ucode/gen_gptp_ucode.py"
mkdir -p "$scratch/unans"
python3 -I - "$gen" "$scratch/unans" <<'PYEOF'
import sys
from pathlib import Path
src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])
old = '    _tmr_cease_rule(p)\n'
assert src.count(old) == 1, src.count(old)
credit = ('    p.emit("RDST", rd=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n'
          '    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=0)\n'
          '    p.emit("BRS", cnd=BRS_Z, label="r571_skip")\n'
          '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n'
          '    p.label("r571_skip")\n')
(out / 'gen_nocease.py').write_text(src.replace(old, ''))
(out / 'gen_credit_on_step.py').write_text(src.replace(old, credit))
PYEOF
fake="$scratch/unans/root"
rm -rf "$fake"; mkdir -p "$fake/tb/verilator/gptp_plane"
ln -s "$root/hdl" "$fake/hdl"; ln -s "$root/gptp-processor" "$fake/gptp-processor"
ln -s "$root/tb/common" "$fake/tb/common"
cp "$root/tb/verilator/gptp_plane/phc_step.py" "$root/tb/verilator/gptp_plane/gptp_plane_wrap.sv" \
   "$fake/tb/verilator/gptp_plane/"
python3 -I - "$root/tb/verilator/gptp_plane/sim_phc_step.cpp" "$fake/tb/verilator/gptp_plane/sim_phc_step.cpp" <<'PYEOF'
import sys
from pathlib import Path
src = Path(sys.argv[1]).read_text()
old = 'if (silent_after_probe_ && seq != probe_seq_) { ++unanswered_; return; }'
assert src.count(old) == 1
Path(sys.argv[2]).write_text(src.replace(old, 'if (silent_after_probe_) { ++unanswered_; return; }'))
PYEOF
for g in nocease credit_on_step; do
  ( python3 "$root/tb/verilator/gptp_plane/phc_step.py" --generator "$scratch/unans/gen_$g.py" \
      --work "$scratch/unans/${g}_real" > "$out/unans_${g}_real.log" 2>&1
    echo $? > "$out/unans_${g}_real.rc" ) &
  ( python3 "$fake/tb/verilator/gptp_plane/phc_step.py" --generator "$scratch/unans/gen_$g.py" \
      --work "$scratch/unans/${g}_variant" > "$out/unans_${g}_variant.log" 2>&1
    echo $? > "$out/unans_${g}_variant.rc" ) &
done
( python3 "$fake/tb/verilator/gptp_plane/phc_step.py" --generator "$gen" \
    --work "$scratch/unans/clean_variant" > "$out/unans_clean_variant.log" 2>&1
  echo $? > "$out/unans_clean_variant.rc" ) &
wait
for run in nocease_real credit_on_step_real clean_variant nocease_variant credit_on_step_variant; do
  echo "== $run rc=$(cat "$out/unans_$run.rc")"
  grep -E 'ARM liveness|\[FAIL\]|RESULT|checks:' "$scratch/unans/$run/clean/run.log"
done
