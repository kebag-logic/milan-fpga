#!/usr/bin/env bash
# Every round 6 to 8 reviewer probe, each from its manifest-checked copy and unchanged, at the head clone.
# Arguments and name lists are round 9's, recovered from its receipts (probes/names/). One log and rc each.
# usage: r678_probes.sh <section>
set -u
S=$VALIDATION_STORAGE/833-a726j
H=$S/wt-head
N=$S/probes/names
P=$S/probes
out=$MANAGEMENT/2026-09-23/833-a726j/receipts/final
mkdir -p "$out" "$S/gtrees" "$S/probe-scratch"
export TMPDIR=$S/tmp
grep SigIgn /proc/self/status > "$out/r678-$1.sigign"
run() {  # name, command...
  local name=$1; shift
  cat /proc/loadavg > "$out/$name.load"
  (cd "$H" && "$@") > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
  cat /proc/loadavg >> "$out/$name.load"
  echo "$name rc $(cat "$out/$name.rc"): $(tail -n 1 "$out/$name.log" | cut -c1-220)"
}
case $1 in
r8)
  run r8-mutants python3 -B "$P/833-r763-8/r8_mutants.py" "$H" 6
  run r8-feasibility python3 -I "$P/833-r763-8/r8_feasibility.py" "$H" "$S/probe-scratch/r8f"
  run r763-8-classify python3 -I "$P/833-r763-8/probe_all_listings.py" "$H" --classify
  run r763-8-probe-table python3 -I "$P/833-r763-8/probe_table.py" "$H"
  run r763-8-byte-mapping python3 -I "$P/833-r763-8/probe_byte_mapping.py" "$H" "$P/833-r763-7/scripts/r7_mutants.py" \
      "$P/833-r764-7/scripts/rv7_mutants.py"
  run r764-8-probes python3 -I "$P/833-r764-8/probes/r764_8_probes.py" "$H" "$S/probe-scratch/r764-8"
  run r764-8-live-probes python3 -I "$P/833-r764-8/probes/r764_8_live_probes.py" "$H" "$S/probe-scratch/r764-8-live"
  run r764-8-live-feasibility python3 -I "$P/833-r764-8/probes/r764_8_live_feasibility.py" "$H" \
      "$S/probe-scratch/r764-8-lf"
  run r764-8-rename-check python3 -I "$P/833-r764-8/probes/r764_8_rename_check.py" "$H" \
      "$P/833-r764-7/scripts/rv7_mutants.py" "$P/833-r763-7/scripts/r7_mutants.py" ;;
alllistings)
  run r763-8-mutants-all-listings bash "$P/833-r763-8/probe_mutants_all_listings.sh" "$H" "$P/833-r763-8" \
      $(cat "$N/all-listings.txt") ;;
r7)
  mkdir -p "$P/833-r764-7/scratch"
  run r7-mutants python3 "$P/833-r763-7/scripts/r7_mutants.py" "$H" 6
  run rv7-mutants python3 "$P/833-r764-7/scripts/rv7_mutants.py" "$H" 6
  run row-mutants python3 "$P/833-r764-7/scripts/row_mutants.py" "$H" 6 ;;
whole)
  run rv7-mutants-whole env RV7_WHOLE=1 python3 "$P/833-r764-7/scripts/rv7_mutants.py" "$H" 6 ;;
matrix6)
  rm -rf "$S/r763-6-trees"; mkdir -p "$S/r763-6-trees"
  for n in $(cat "$N/r763-6-matrix.txt"); do
    python3 -I "$P/833-r763-6/probes/mktree.py" "$H/scripts" "$S/r763-6-trees/$n" "$n" >> "$out/r763-6-mktree.log" 2>&1
  done
  run r763-6-matrix python3 -I "$P/833-r763-6/probes/matrix.py" "$H/scripts" "$S/r763-6-trees" 6 \
      $(cat "$N/r763-6-matrix.txt") ;;
grace)
  rm -rf "$S/gtrees"; mkdir -p "$S/gtrees"
  slow=$(sed 's/-0\.[0-9]*$//' "$N/slow.txt" | sort -u)
  run grace-trees python3 "$P/833-r763-7/scripts/grace_trees.py" "$H" "$S/gtrees" \
      $(cat "$N/grace-trees.txt") $(echo "$slow" | grep -vx none)
  mkdir -p "$P/833-r763-7/scratch"
  run pin-feasibility-r763-7 bash "$P/833-r763-7/scripts/pin_feasibility.sh" "$P/833-r763-7" "$S/gtrees" $(cat "$N/pin.txt")
  run pin-feasibility-row2-r763-7 bash "$P/833-r763-7/scripts/pin_feasibility_row2.sh" "$P/833-r763-7" "$S/gtrees" \
      $(cat "$N/pin2.txt")
  run rv7-pin-feasibility python3 -I "$P/833-r764-7/scripts/rv7_pin_feasibility.py" "$H" "$S/probe-scratch/rv7pf"
  run stated-seconds-check python3 "$P/833-r764-7/scripts/stated_seconds_check.py" "$H" owner_stated_seconds \
      $(cat "$N/ssc.txt")
  run grace-resume-head python3 -I "$P/833-r763-6/probes/grace_resume_probe.py" "$H/scripts" 5
  for n in $(cat "$N/grace2.txt"); do
    tree=$S/gtrees/$n/scripts; [ "$n" = none ] && tree=$H/scripts
    run "grace2-$n" python3 -I "$P/833-r763-7/scripts/grace_resume_probe2.py" "$tree" 3
  done ;;
slow)
  mkdir -p "$out/slow-census"
  while read -r spec; do
    n=${spec%-0.*}; d=${spec##*-}; tree=$S/gtrees/$n/scripts; [ "$n" = none ] && tree=$H/scripts
    (cd "$H" && python3 -I "$P/833-r763-6/probes/slow_census.py" "$tree" owner_shell_window "$d") \
      > "$out/slow-census/slow-$spec.log" 2>&1
    echo $? > "$out/slow-census/slow-$spec.rc"
    echo "slow $spec rc $(cat "$out/slow-census/slow-$spec.rc"): $(tail -n 1 "$out/slow-census/slow-$spec.log" | cut -c1-150)"
  done < "$N/slow.txt" ;;
slowshell)
  mkdir -p "$P/833-r764-6/scratch"
  run slow-shell-window python3 "$P/833-r764-6/scripts/slow_shell_window.py" campaign "$H" 8 4 0.15,0.3,0.5
  run sigcont-pending python3 -I "$P/833-r764-6/scripts/sigcont_pending.py" ;;
hup)
  run hupign-head python3 -I "$P/833-r763-6/probes/hup_ignored.py" python3 -B scripts/test_suite_cancellation.py \
      --mutants none --matrix --jobs 6 ;;
repeat)
  for c in owner_report owner_late_cancel owner_late_exit owner_reused_identity; do
    run "stress-$c" python3 -I "$P/833-r763-6/probes/repeat.py" "$H/scripts" "$H" "$c" 64 8
  done
  run repeat-controls bash "$P/833-r764-6/scripts/repeat_controls.sh" "$H" 8 owner_report:64 owner_reused_identity:64 \
      owner_shell_window:24 ;;
tables)
  run table-r763-7 python3 -I "$P/833-r763-7/scripts/table_check.py" "$H"
  run table-r764-7 python3 -I "$P/833-r764-7/scripts/table_vs_mutants.py" "$H"
  run table-r764-6 python3 -I "$P/833-r764-6/scripts/table_vs_mutants.py" "$H"
  run table-r763-6 python3 -I "$P/833-r763-6/probes/table_vs_mutants.py" "$H" ;;
esac
