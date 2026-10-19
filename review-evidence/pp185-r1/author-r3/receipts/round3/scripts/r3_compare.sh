#!/usr/bin/env bash
# round 3: regenerate the failure-set comparisons with mutants and baselines apart, from
# the existing campaign records (no campaign re-run), into the output receipts/round3
S=$VALIDATION_STORAGE/pp185-a647; O=$MANAGEMENT/2026-09-23/pp185-a647/receipts
R3="$O/round3"; P="$S/scripts"
declare -A SET=([round2/base]="$S/r2/rec/base/campaigns/out" [round2/head]="$S/r2/rec/head/campaigns/out"
                [round2/head-final2]="$S/r2/rec/head-final2/campaigns/out"
                [r1c/base]="$S/r1c/base/campaigns/out" [r1c/head]="$S/r1c/head/campaigns/out"
                [r1b/head]="$S/r1b/head-campaigns/out")
mkdir -p "$R3/compare/round2" "$R3/compare/r1c" "$R3/records" "$R3/selftest" "$R3/scripts"
cp "$P/r3_failsets.py" "$P/r3_failsets_selftest.py" "$P/r3_plant.py" "$P/r3_compare.sh" \
   "$P/r3_reconcile.py" "$R3/scripts/"

# inputs: every results.json and aecp_dispatch log the comparisons read, hashed
: > "$R3/inputs.sha256"
for label in round2/base round2/head round2/head-final2 r1c/base r1c/head r1b/head; do
  for c in notify aecp_dispatch d3 acmp name_state; do
    d="${SET[$label]}/$c"; [ -f "$d/results.json" ] || continue
    for f in "$d/results.json" $([ "$c" = aecp_dispatch ] && ls "$d"/*.log); do
      echo "$(sha256sum < "$f" | cut -d' ' -f1)  $(stat -c %s "$f")  $label/$c/$(basename "$f")" >> "$R3/inputs.sha256"
    done
  done
done
# published copies: every input that round 2 copied or listed must match it byte for byte
python3 -I - "$R3/inputs.sha256" "$O" > "$R3/inputs-check.txt" <<'EOF'
import hashlib, sys
from pathlib import Path
listing, root = Path(sys.argv[1]), Path(sys.argv[2])
over = {l.split(None, 2)[2]: l.split()[0] for l in (root / "OVER-200KB.sha256").read_text().splitlines() if l.strip()}
bad = 0
for line in listing.read_text().splitlines():
    digest, size, label = line.split(None, 2)
    rnd, side, c, name = label.split("/")
    pub = f"{rnd}/{side}/campaigns/out/{c}/{name}"
    if (root / pub).is_file():
        got, where = hashlib.sha256((root / pub).read_bytes()).hexdigest(), "copied"
    elif pub in over:
        got, where = over[pub], "OVER-200KB.sha256"
    else:
        continue
    ok = got == digest
    bad += not ok
    print(f"{'MATCH' if ok else 'MISMATCH'} {label} = receipts/{pub} ({where})")
print(f"{bad} mismatches")
sys.exit(1 if bad else 0)
EOF
echo $? > "$R3/inputs-check.rc"

# small copies of the records not already in receipts (results.json under 200 KB) and
# each aecp_dispatch record set's FAIL: lines, so every count here can be replayed
for label in round2/base round2/head round2/head-final2 r1c/base r1c/head r1b/head; do
  for c in notify aecp_dispatch d3 acmp name_state; do
    f="${SET[$label]}/$c/results.json"; [ -f "$f" ] || continue
    dest="$R3/records/$label/$c"
    if [ ! -f "$O/$label/campaigns/out/$c/results.json" ] && [ "$(stat -c %s "$f")" -lt 204800 ]; then
      mkdir -p "$dest"; cp "$f" "$dest/results.json"
    fi
    if [ "$c" = aecp_dispatch ]; then
      mkdir -p "$dest"
      for l in "${SET[$label]}/$c"/*.log; do echo "== $(basename "$l")"; grep '^FAIL:' "$l"; done > "$dest/fail-lines.txt"
    fi
  done
done

# the comparisons
run() { # run <out-stem> <campaign> <base-label> <head-label>
  python3 -I "$P/r3_failsets.py" "$2" "${SET[$3]}/$2" "${SET[$4]}/$2" --json "$1.json" > "$1.txt" 2>&1
  echo $? > "$1.rc"
  sed -i "1a records: base $3, head $4" "$1.txt"
}
for c in notify aecp_dispatch d3 acmp name_state; do
  run "$R3/compare/round2/$c-base-vs-head" $c round2/base round2/head
done
run "$R3/compare/round2/notify-base-vs-head-final2" notify round2/base round2/head-final2
run "$R3/compare/round2/notify-head-vs-head-final2" notify round2/head round2/head-final2
for c in notify aecp_dispatch d3 acmp name_state; do
  run "$R3/compare/r1c/$c-base-vs-head" $c r1c/base r1c/head
done
for c in notify aecp_dispatch d3 acmp; do
  run "$R3/compare/r1c/$c-r1b-head-vs-r1c-head" $c r1b/head r1c/head
done

# the script's own check and its planted mutants
python3 -I "$P/r3_failsets_selftest.py" "$P/r3_failsets.py" "$P/r1c_failsets.py" > "$R3/selftest/golden.log" 2>&1
echo $? > "$R3/selftest/golden.rc"
rm -rf "$S/r3/mut"
python3 -I "$P/r3_plant.py" "$P/r3_failsets.py" "$S/r3/mut" > "$R3/selftest/plant.log" 2>&1
echo $? > "$R3/selftest/plant.rc"
for m in "$S/r3/mut"/*.py; do
  n=$(basename "$m" .py)
  python3 -I "$P/r3_failsets_selftest.py" "$m" > "$R3/selftest/mutant-$n.log" 2>&1
  echo $? > "$R3/selftest/mutant-$n.rc"
done
echo done
