#!/usr/bin/env bash
# R272-5: re-run every probe of R272 rounds one to four UNCHANGED (the probe
# drivers, case files and patches are byte-copies under scripts/r1..r4), at
# the head and, where the earlier round did, at the base, in both compiler
# modes. Only the orchestration differs from the round-one runners: compiler
# runs go one at a time (each may spawn 8 compiler threads), absent runs at
# most 4 at once, so no more than 8 jobs run in parallel.
# Usage: rerun_earlier.sh <packet> <head-tree> <base-tree> <sdk-dir>
set -u
packet=$1 head=$2 base=$3 sdk=$4
s="$packet/scripts"
out="$packet/receipts/rerun"
mkdir -p "$out/probes" "$out/accepted" "$out/disconnect" "$out/reader" "$out/cpp"
export PATH="${R272_VERILATOR_BIN:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin}:$PATH"
probe() {  # outfile-stem tree cases [args...]
  local stem=$1 tree=$2 cases=$3; shift 3
  python3 -B "$s/r1/probe_gate1b.py" --tree "$tree" --cases "$cases" \
    --out "$stem.json" "$@" > "$stem.log" 2>&1
  echo "exit=$?" >> "$stem.log"
}
# 1. the round-one to round-four probe pairs (cases_r1..r4), head and base
for r in r1 r2 r3 r4; do
  probe "$out/probes/$r-head-absent" "$head" "$s/r1/cases_$r.py" --absent &
  probe "$out/probes/$r-base-absent" "$base" "$s/r1/cases_$r.py" --absent &
done
wait
for r in r1 r2 r3 r4; do
  probe "$out/probes/$r-head-sdk" "$head" "$s/r1/cases_$r.py" --sdk "$sdk"
  probe "$out/probes/$r-base-sdk" "$base" "$s/r1/cases_$r.py" --sdk "$sdk"
done
# 2. the accepted-case cross-check (round one), and the resolver-off control
dump="$packet/scratch/retired_rule_cases.json"
R272_ACCEPTED_DUMP="$packet/scratch/retired_rule_cases-absent.json" \
  probe "$out/accepted/head-absent" "$head" "$s/r1/cases_accepted.py" --absent
R272_ACCEPTED_DUMP=$dump \
  probe "$out/accepted/head-sdk" "$head" "$s/r1/cases_accepted.py" --sdk "$sdk"
cmp "$dump" "$packet/scratch/retired_rule_cases-absent.json" \
  > "$out/accepted/dumps-cmp.txt" 2>&1; echo "cmp exit=$?" >> "$out/accepted/dumps-cmp.txt"
probe "$out/accepted/resolver-off-sdk" "$head" "$s/r1/cases_r1.py" --sdk "$sdk" \
  --patch "$s/r1/patches/disconnect-resolver-function.json"
R272_ACCEPTED_DUMP=$dump \
  probe "$out/accepted/base-absent" "$base" "$s/r1/cases_accepted.py" --absent
R272_ACCEPTED_DUMP=$dump \
  probe "$out/accepted/base-sdk" "$base" "$s/r1/cases_accepted.py" --sdk "$sdk"
# 3. the round-one disconnect matrix
p="$s/r1/patches"
dis() { local tag=$1; shift
  probe "$out/disconnect/$tag" "$head" "$s/r1/cases_disconnect.py" --anchor mutations "$@"; }
dis connected-absent --absent &
dis sel-absent --absent --patch "$p/disconnect-sel.json" --patch "$p/skip-accepted-loops.json" &
wait
dis connected-sdk --sdk "$sdk"
dis sel-sdk --sdk "$sdk" --patch "$p/disconnect-sel.json" --patch "$p/skip-accepted-loops.json"
dis e-sdk --sdk "$sdk" --patch "$p/disconnect-e.json"
dis h-sdk --sdk "$sdk" --patch "$p/disconnect-h.json"
dis res-sdk --sdk "$sdk" --patch "$p/disconnect-res.json"
dis eres-sdk --sdk "$sdk" --patch "$p/disconnect-e.json" --patch "$p/disconnect-res.json"
python3 -B "$s/r1/tabulate_disconnect.py" "$out/disconnect" > "$out/disconnect/TABLE.txt" 2>&1
# 4. the pinned-GCC directive spellings (rounds one and two)
bash "$s/r1/cpp_directive_check.sh" "$sdk" "$out/cpp" > "$out/cpp/run.log" 2>&1
echo "exit=$?" >> "$out/cpp/run.log"
python3 -B "$s/r2/gcc_spellings.py" "$sdk/bin/riscv32-linux-gcc" "$packet/scratch/gcc-spellings" \
  > "$out/cpp/gcc-spellings.log" 2>&1
echo "exit=$?" >> "$out/cpp/gcc-spellings.log"
# 5. the reader-level probes (rounds three and four) against the pinned GCC
python3 -B "$s/r3/reader_vs_gcc.py" "$head" "$sdk/bin/riscv32-linux-gcc" \
  "$s/r3/dollar_skipped.c" "$s/r4/mid.c" "$s/r4/comb.c" "$s/r4/sup2.c" "$s/r4/eacute.c" \
  > "$out/reader/reader_vs_gcc.txt" 2>&1
echo "exit=$?" >> "$out/reader/reader_vs_gcc.txt"
# 6. the round-two split-digraph probe, through the whole gate, both modes
#    (path-only copies: REPO points at this head; logic byte-identical)
for sp in control_hash formfeed plain_digraph split_digraph; do
  python3 -B "$s/r5/r272-2_probe_split_digraph_run_sdk_r5.py" "$sdk" "$sp" \
    > "$out/reader/split-digraph-$sp-sdk.txt" 2>&1
  echo "exit=$?" >> "$out/reader/split-digraph-$sp-sdk.txt"
  python3 -B "$s/r5/r272-2_probe_split_digraph_run_absent_r5.py" "$sdk" "$sp" \
    > "$out/reader/split-digraph-$sp-absent.txt" 2>&1
  echo "exit=$?" >> "$out/reader/split-digraph-$sp-absent.txt"
done
for f in "$out"/probes/*.log "$out"/accepted/*.log "$out"/disconnect/*.log; do
  echo "== ${f#$out/}: $(grep -c '^ACCEPTED' "$f") accepted, $(grep -c '^REFUSED' "$f") refused ($(grep -c 'pin_ok=True' "$f") on pin); $(tail -n 1 "$f")"
done
cat "$out/disconnect/TABLE.txt"
tail -n 2 "$out"/reader/*.txt
