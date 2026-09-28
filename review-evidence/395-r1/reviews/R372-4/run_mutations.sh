#!/usr/bin/env bash
# R372-4 disposable mutation campaign on exported copies of the merge head.
# Usage: run_mutations.sh <repo-clone> <litex-python> <packet-dir>
# Each mutant is a fresh `git archive` of 895be307 under <packet>/scratch/mut/<id>,
# with the initialized submodules symlinked read-only.  The clone is not modified.
set -u
REPO=$1; LPY=$2; PKT=$3
HEAD=895be30712acf8dd80956a5b954690859b080d87
OUT=$PKT/receipts/mutations; mkdir -p "$OUT"; rm -rf "$PKT/scratch/mut"; mkdir -p "$PKT/scratch/mut"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0

mk() {  # id -> fresh copy path
  local d=$PKT/scratch/mut/$1; mkdir -p "$d"
  git -C "$REPO" archive "$HEAD" | tar -x -C "$d"
  for s in protocol-processor gptp-processor; do rmdir "$d/$s" 2>/dev/null; ln -s "$REPO/$s" "$d/$s"; done
  echo "$d"
}
sub() {  # file old new  (exact literal, must match once)
  python3 - "$@" <<'EOF'
import sys; p,o,n=sys.argv[1:4]; s=open(p).read(); assert s.count(o)==1,(p,o,s.count(o)); open(p,'w').write(s.replace(o,n))
EOF
}
run() {  # id expect(0|nonzero) cmd...  (cwd = copy)
  local id=$1 want=$2; shift 2; local d=$PKT/scratch/mut/${id%%-*}
  ( cd "$d" && timeout --foreground 900 "$@" ) > "$OUT/$id.log" 2>&1; local rc=$?
  local verdict=UNEXPECTED
  if [ "$want" = 0 ] && [ $rc = 0 ]; then verdict=expected; fi
  if [ "$want" = nonzero ] && [ $rc != 0 ]; then verdict=expected; fi
  echo "$id rc=$rc want=$want $verdict"
}

TG=(python3 -B sw/builder/test_timing_grade.py "$LPY")
CC=("$LPY" -B sw/builder/test_clock_contract.py --soc)
PR=("$LPY" -B "$PKT/probe_composition.py" .)

d=$(mk C0); :                                           # unmodified control
d=$(mk M1); sub "$d/sw/litex/timing_grade.tcl" 'report_timing_summary -delay_type min_max -report_unconstrained \
                    -max_paths 5 -file ${stem}_timing.rpt' 'report_timing_summary -delay_type max -report_unconstrained \
                    -max_paths 5 -file ${stem}_timing.rpt'
d=$(mk M2); sub "$d/sw/litex/milan_soc.py" 'S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))' 'S7PLL(speedgrade=-2)'
d=$(mk M3); sub "$d/sw/litex/platforms/alinx_ax7101.py" '"kl_timing_grade_reports {build_name}_signoff",' ''
d=$(mk M4); sub "$d/sw/litex/milan_soc.py" '    if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:' '    if False:'
d=$(mk M5); sub "$d/tb/verilator/nvm_capture_cpu/recipe.py" 'CPU_HZ = 50_000_000' 'CPU_HZ = 40_000_000'
d=$(mk M6); sub "$d/sw/litex/platforms/ax7101_timing.py" '"junction_max_c": 85,' '"junction_max_c": 100,'

pids=()
{ run C0-timing-grade 0 "${TG[@]}"; run C0-clock-contract-soc 0 "${CC[@]}"; run C0-probe 0 "${PR[@]}"; } > "$OUT/_C0.txt" & pids+=($!)
run M1-timing-grade nonzero "${TG[@]}" > "$OUT/_M1.txt" & pids+=($!)
{ run M2-timing-grade nonzero "${TG[@]}"; run M2-probe nonzero "${PR[@]}"; } > "$OUT/_M2.txt" & pids+=($!)
{ run M3-timing-grade nonzero "${TG[@]}"; run M3-probe nonzero "${PR[@]}"; } > "$OUT/_M3.txt" & pids+=($!)
{ run M4-clock-contract-soc nonzero "${CC[@]}"; run M4-probe nonzero "${PR[@]}"; } > "$OUT/_M4.txt" & pids+=($!)
{ run M5-probe nonzero "${PR[@]}"; run M5-timing-grade 0 "${TG[@]}"; } > "$OUT/_M5.txt" & pids+=($!)
run M6-timing-grade nonzero "${TG[@]}" > "$OUT/_M6.txt" & pids+=($!)
for p in "${pids[@]}"; do wait "$p"; done
cat "$OUT"/_C0.txt "$OUT"/_M*.txt | tee "$OUT/SUMMARY.txt"
rm -f "$OUT"/_*.txt
grep -c UNEXPECTED "$OUT/SUMMARY.txt" | sed 's/^/unexpected=/' | tee -a "$OUT/SUMMARY.txt"
