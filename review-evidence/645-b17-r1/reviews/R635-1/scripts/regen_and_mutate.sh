#!/usr/bin/env bash
# R635-1: re-run the published B17 grading/summary tools on a scratch copy of the published packet and compare their
# outputs with the published summaries; then run the published controls and five grader mutations.
# usage: regen_and_mutate.sh <author_dir> <scratch_dir> <receipt_dir>   (needs python3 with numpy; offline)
set -u
A=$1; S=$2; R=$3
rm -rf "$S/regen" "$S/mut"; mkdir -p "$S/regen/pk/summary" "$S/regen/tools" "$S/mut"
cp -r "$A/cycles" "$S/regen/pk/"; cp "$A"/summary/c??.json "$S/regen/pk/summary/"
cp "$A/tools/summ_b17.py" "$A/tools/ana_b17.py" "$S/regen/tools/"
( cd "$S/regen" && python3 -I tools/summ_b17.py "$S/regen/pk" > summ.out; echo "summ_b17 rc=$?" )
for f in cycles.json table.md counter-logs.sha256; do cmp -s "$S/regen/pk/summary/$f" "$A/summary/$f" && echo "$f byte-identical" || echo "$f DIFFERS"; done
for c in 01 02 03 04 05 06 07 08 09 10; do ( cd "$S/regen" && python3 -I tools/ana_b17.py cycle pk/cycles/c$c - pk/ana-c$c.json >/dev/null ) || echo "ana c$c failed"; done
python3 -I - "$S/regen/pk" <<'PY'
import json, sys
P = sys.argv[1]; bad = 0
for c in range(1, 11):
    a = json.load(open(f"{P}/ana-c{c:02d}.json"))["poll"]; b = json.load(open(f"{P}/summary/c{c:02d}.json"))["poll"]
    for s in b["slips"]:
        s.pop("tap_lateness_max_us", None); s.pop("tap_pdus_in_interval", None)
    bad += a != b
print("poll sections differing from the published grades:", bad)
PY
T="$S/regen/tools/ana_b17.py"
( cd "$S" && python3 -I "$T" control "$R/rerun-controls.json" | sed 's/^/controls: /' )
sed 's/cls = "b" if (s_pred <= w_total and right_dir and periodic) else "c"/cls = "c"/' "$T" > "$S/mut/m1.py"
sed 's/delta = round(rates\["peer-aaf"\]\["rate_ppm"\] - rates\["dut-aaf"\]\["rate_ppm"\], 4)/delta = round(rates["dut-aaf"]["rate_ppm"] - rates["peer-aaf"]["rate_ppm"], 4)/' "$T" > "$S/mut/m2.py"
sed 's/                    lo, hi = rel(pt0), rel(r\["t1"\])/                    lo, hi = rel(r["t0"]), rel(r["t1"])/' "$T" > "$S/mut/m3.py"
sed 's/                periodic = n_expected <= 2.0/                periodic = True/' "$T" > "$S/mut/m4.py"
sed 's/LATE_US = 10.0/LATE_US = 40.0/' "$T" > "$S/mut/m5.py"
for m in 1 2 3 4 5; do cmp -s "$T" "$S/mut/m$m.py" && echo "m$m NOT APPLIED"; ( cd "$S" && python3 -I "mut/m$m.py" control "$R/mutation-m$m.json" > "mut/m$m.log" 2>&1; echo "m$m rc=$? $(tail -1 mut/m$m.log)" ); done
