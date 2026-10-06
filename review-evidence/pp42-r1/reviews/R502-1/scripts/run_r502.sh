#!/usr/bin/env bash
# The R502-1 review runs for processor PR #164 (issue #42), as executed.
# Usage: CLONE=<processor clone at 72facc6d> PACKET=<output dir> V=<Verilator 5.050> run_r502.sh
# Disposable trees go to $PACKET/scratch; receipts to $PACKET/receipts. Nothing is
# written in $CLONE. The four campaigns ran concurrently (each with its own log and rc).
set -u
HEAD_SHA=72facc6d48807808e4d97a454a0ecceb2769ac9e
BASE_SHA=e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8
S=$PACKET/scratch; R=$PACKET/receipts; mkdir -p "$S" "$R"

export_tree() {  # export_tree SHA DIR: an archive of the commit, then build parallelism -j 0 -> -j 4
  mkdir -p "$2" && git -C "$CLONE" archive "$1" | tar -x -C "$2"
  sed -i 's/--build -j 0/--build -j 4/' "$2/tb/pp_top/Makefile"   # parallelism only (12 GB unit cap)
}
for t in head mut probe; do export_tree $HEAD_SHA "$S/$t"; done
export_tree $BASE_SHA "$S/base"

# static: every arm of the drivers that build tb/pp_top still plants
python3 "$PACKET/scripts/plant_check.py" "$S/base" > "$R/plant_check_base.log" 2>&1; echo "base rc=$?" > "$R/plant_check_base.rc"
python3 "$PACKET/scripts/plant_check.py" "$S/head" > "$R/plant_check_head.log" 2>&1; echo "head rc=$?" > "$R/plant_check_head.rc"

# section DN alone at head
(cd "$S/head/tb/pp_top" && make gsi-build VERILATOR="$V" > "$R/gsi_build_head.log" 2>&1 \
  && ./obj_dir/Vpp_top_sim --domain-notify-only > "$R/dn_only_head.log" 2>&1; echo "rc=$?" > "$R/dn_only_head.rc")

# concurrent campaigns
(cd "$S/head/tb/pp_top" && make run VERILATOR="$V" > "$R/pp_top_full_head.log" 2>&1; echo $? > "$R/pp_top_full_head.rc") &
(cd "$S/base/tb/pp_top" && make run VERILATOR="$V" > "$R/pp_top_full_base.log" 2>&1; echo $? > "$R/pp_top_full_base.rc") &
(cd "$S/mut" && python3 tb/pp_top/notify_mutants.py --output "$S/mut_out" --verilator "$V" --jobs 3 \
   > "$R/notify_mutants_head.log" 2>&1; echo $? > "$R/notify_mutants_head.rc") &
(python3 "$PACKET/scripts/r502_probes.py" "$S/probe" "$S/probe_out" --jobs 2 --verilator "$V" \
   > "$R/r502_probes.log" 2>&1; echo $? > "$R/r502_probes.rc") &
wait
cp "$S/mut_out/results.json" "$R/notify_mutants_head_results.json"
cp "$S/probe_out/results.json" "$R/r502_probes_results.json"
for t in base head; do
  grep -E "^FAIL|^  \[i\]|checks, [0-9]+ failures|checks: |^Ran |^OK" "$R/pp_top_full_$t.log" > "$S/graded_$t.txt"
done
diff "$S/graded_base.txt" "$S/graded_head.txt" > "$R/pp_top_graded_base_vs_head.diff"

# documentation gates (need a git checkout), at base and head
for t in head base; do
  sha=$([ $t = head ] && echo $HEAD_SHA || echo $BASE_SHA)
  git clone -q --no-checkout "$CLONE" "$S/gates_$t" && git -C "$S/gates_$t" checkout -q --detach $sha
  (cd "$S/gates_$t" && make -k links matrix modmatrix params ids figures stale > "$R/docs_gates_$t.log" 2>&1; echo $? > "$R/docs_gates_$t.rc")
done

# timing-statement probe: a head copy with receipts/probe_timing_statements.patch applied (prints only)
mkdir -p "$S/instr" && git -C "$CLONE" archive $HEAD_SHA | tar -x -C "$S/instr"
sed -i 's/--build -j 0/--build -j 4/' "$S/instr/tb/pp_top/Makefile"
(cd "$S/instr/tb/pp_top" && patch -p0 notify_phases.hpp < "$R/probe_timing_statements.patch" \
  && make gsi-build VERILATOR="$V" >/dev/null 2>&1 && ./obj_dir/Vpp_top_sim --domain-notify-only > "$R/probe_timing_statements.log" 2>&1)
