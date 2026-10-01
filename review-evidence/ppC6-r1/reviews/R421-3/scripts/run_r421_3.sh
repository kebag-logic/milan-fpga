#!/bin/sh
# R421-3 reproduction: every probe runs on a disposable `git archive` export
# under $WORK; the reviewed clone is only read.
# Usage: run_r421_3.sh CLONE WORK PIN_VERILATOR OUT
set -eu
CLONE=$1; WORK=$2; PIN=$3; OUT=$4
HERE=$(cd "$(dirname "$0")" && pwd)
HEAD=9624ef4c452d708de68a901d5e645bdfa1f5d6f5; R2=88e0bf82888d6ad83b500425a786814da467610b
export PIN_VERILATOR="$PIN"
VW="$HERE/verilator-j8.sh"
exp() { rm -rf "$WORK/$2"; mkdir -p "$WORK/$2"; git -C "$CLONE" archive "$1" | tar -x -C "$WORK/$2"; }
mkdir -p "$OUT"
# 1. section ID at the head
exp $HEAD head; (cd "$WORK/head/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null && ./obj_idn/Vpp_top_idn) > "$OUT/head_pp_top_identify.log" 2>&1 || true
# 2. the head's tests on round 2's RTL (the failing arm)
exp $HEAD fail_r2; exp $R2 r2; rm -rf "$WORK/fail_r2/hdl"; cp -a "$WORK/r2/hdl" "$WORK/fail_r2/hdl"
(cd "$WORK/fail_r2/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null && ./obj_idn/Vpp_top_idn) > "$OUT/failarm_head_tests_r2_rtl.log" 2>&1 || true
# 3. round-2 reviewer arms at the head and on round 2's RTL
exp $HEAD arms; python3 "$HERE/r421_arms.py" "$WORK/arms"
(cd "$WORK/arms/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null && ./obj_idn/Vpp_top_idn) > "$OUT/r421_2_arms_at_head.log" 2>&1 || true
rm -rf "$WORK/arms_r2"; cp -a "$WORK/arms" "$WORK/arms_r2"; rm -rf "$WORK/arms_r2/hdl" "$WORK/arms_r2/tb/pp_top"/obj_*; cp -a "$WORK/r2/hdl" "$WORK/arms_r2/hdl"
(cd "$WORK/arms_r2/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null && ./obj_idn/Vpp_top_idn) > "$OUT/r421_2_arms_on_r2_rtl.log" 2>&1 || true
# 4. seeded random-press probe, 16 campaigns, at the head and on round 2's RTL
exp $HEAD rnd; python3 "$HERE/r421_3_random.py" "$WORK/rnd"
(cd "$WORK/rnd/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null)
"$HERE/run_random.sh" "$WORK/rnd/tb/pp_top/obj_idn/Vpp_top_idn" "$OUT/random" 200
exp $HEAD rnd_r2; rm -rf "$WORK/rnd_r2/hdl"; cp -a "$WORK/r2/hdl" "$WORK/rnd_r2/hdl"; python3 "$HERE/r421_3_random.py" "$WORK/rnd_r2"
(cd "$WORK/rnd_r2/tb/pp_top" && make identify-build VERILATOR="$VW" >/dev/null)
"$HERE/run_random.sh" "$WORK/rnd_r2/tb/pp_top/obj_idn/Vpp_top_idn" "$OUT/random_on_r2_rtl" 200
# 5. reviewer latch mutants (section ID + random probe), 8 workers x 1 job
VJOBS=1 TMPDIR="$WORK" python3 "$HERE/r421_3_probes.py" --root "$WORK/rnd" --output "$OUT/latch_probes" --verilator "$VW" --jobs 8 > "$OUT/latch_probes.stdout"
# 6. the lane's 40 controls
exp $HEAD camp; (cd "$WORK/camp" && VJOBS=1 TMPDIR="$WORK" python3 tb/pp_top/notify_mutants.py --output "$OUT/notify_mutants" --verilator "$VW" --jobs 8 > "$OUT/notify_mutants.stdout" 2>&1) || true
# 7. tb/aecp_notify (both builds) and the full-timebase phase sweep
(cd "$WORK/head/tb/aecp_notify" && make run VERILATOR="$VW") > "$OUT/head_aecp_notify_run.log" 2>&1 || true
exp $HEAD ft; "$HERE/r421_3_ft_sweep.sh" "$WORK/ft" "$VW" "$WORK/ft_sweep.txt"; cp "$WORK/ft_sweep.txt" "$OUT/ft_phase_sweep_head.txt"
# 8. the full tb/pp_top suite, lint, docs gates, matrix
(cd "$WORK/head/tb/pp_top" && make VERILATOR="$VW") > "$OUT/head_pp_top_full.log" 2>&1 || true
mkdir -p "$WORK/bin"; ln -sf "$VW" "$WORK/bin/verilator"
(cd "$WORK/head" && PATH="$WORK/bin:$PATH" ./scripts/lint_hdl.sh) > "$OUT/lint_hdl_head.log" 2>&1 || true
exp $HEAD docs; (cd "$WORK/docs" && make check) > "$OUT/make_check_head.log" 2>&1 || true
(cd "$WORK/docs" && python3 scripts/gen_matrix.py --check) > "$OUT/gen_matrix_check_head.log" 2>&1 || true
