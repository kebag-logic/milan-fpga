#!/bin/sh
# R421-4: re-run R421-3's probes at the round-4b head on disposable
# `git archive` exports under $WORK; the reviewed clone is only read.
# The round-2-RTL control runs of round 3 are not repeated: round 2's hdl/
# cannot be paired with this head's merged engine and top. The reviewer
# latch mutants (step 3) are the at-head controls for the probes' teeth.
# Usage: run_r421_4_probes.sh CLONE WORK PIN_VERILATOR OUT STEP
set -eu
CLONE=$1; WORK=$2; PIN=$3; OUT=$4; STEP=$5
HERE=$(cd "$(dirname "$0")" && pwd)
HEAD=95a78c099ee5aa914521975355adc1dfef99d01c
export PIN_VERILATOR="$PIN"
VW="$HERE/verilator-j8.sh"
exp() { rm -rf "$WORK/$2"; mkdir -p "$WORK/$2"; git -C "$CLONE" archive "$1" | tar -x -C "$WORK/$2"; }
mkdir -p "$OUT"
case $STEP in
arms)  # R421-2's arms (eof-beat stalls, gap presses) at the head
  exp $HEAD arms; python3 "$HERE/r421_arms.py" "$WORK/arms"
  (cd "$WORK/arms/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null && ./obj_idn/Vpp_top_idn) > "$OUT/r421_2_arms_at_head.log" 2>&1 || true ;;
random)  # R421-3's seeded random-press probe, 16 campaigns of 200 steps
  exp $HEAD rnd; python3 "$HERE/r421_3_random.py" "$WORK/rnd"
  (cd "$WORK/rnd/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null)
  # run from the bench directory: the model $readmem-loads ucode.hex and ltn_rom.hex from its cwd
  (cd "$WORK/rnd/tb/pp_top" && "$HERE/run_random.sh" ./obj_idn/Vpp_top_idn "$OUT/random" 200) ;;
latch)  # R421-3's latch mutants through the lane's own driver (needs step random's tree)
  VJOBS=1 TMPDIR="$WORK" python3 "$HERE/r421_3_probes.py" --root "$WORK/rnd" --output "$OUT/latch_probes" --verilator "$VW" --jobs 8 > "$OUT/latch_probes.stdout" ;;
ft)  # tb/aecp_notify section FT departure-phase sweep at the full timebase
  exp $HEAD ft; "$HERE/r421_3_ft_sweep.sh" "$WORK/ft" "$VW" "$WORK/ft_sweep.txt"; cp "$WORK/ft_sweep.txt" "$OUT/ft_phase_sweep_head.txt" ;;
esac
