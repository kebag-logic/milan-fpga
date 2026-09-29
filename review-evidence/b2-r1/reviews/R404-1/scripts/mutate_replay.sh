#!/bin/sh
# Mutation probe: plant one wrong value per mutant in a scratch copy of the two
# findings pages (or a scratch copy of one packet record) and show replay_b2.py
# rejects each, while the unmutated copy passes.
# Usage: mutate_replay.sh <repo clone> <packet author dir> <scratch dir>
set -u
REPO=$1; PKT=$2; S=$3
HERE=$(cd "$(dirname "$0")" && pwd)
P608=docs/findings/608_75_WITHDRAWAL_AND_RESTART.md
P606=docs/findings/606_FIRST_BIND_MEASUREMENT.md
fresh() {
  rm -rf "$S/m" && mkdir -p "$S/m/docs/findings" &&
  cp "$REPO/$P608" "$REPO/$P606" "$S/m/docs/findings/"
}
run() {  # name, packet dir
  python3 -I -B "$HERE/replay_b2.py" "$2" "$S/m" > "$S/$1.out" 2>&1
  rc=$?
  echo "$1 rc=$rc $(grep -c . "$S/$1.out") lines; $(grep -m1 '^FAILS' "$S/$1.out"); first: $(grep -m1 '^FAIL ' "$S/$1.out")"
}
fresh; run control "$PKT"
fresh; sed -i 's/^| 44 | 0.008967 | IN (observed) | -0.183 | 5 | +1 \/ +1 | no | 0.139247 |/| 44 | 0.008967 | IN (observed) | -0.183 | 5 | +1 \/ +1 | no | 0.039247 |/' "$S/m/$P608"; run m1_restart_c44 "$PKT"
fresh; sed -i 's/^| 22 | 0.010791 | LV |/| 22 | 0.010791 | IN (inferred) |/' "$S/m/$P608"; run m2_class_c22 "$PKT"
fresh; sed -i 's/^| 7 | 0.008820 | IN (inferred) |/| 7 | 0.008820 | IN (observed) |/' "$S/m/$P608"; run m3_class_c7 "$PKT"
fresh; sed -i 's/^| 3 | 36.9 | 17.341 | 1 \/ 0 |/| 3 | 36.9 | 17.341 | 1 \/ 1 |/' "$S/m/$P606"; run m4_prebind_decl_b3 "$PKT"
fresh; sed -i 's/^| 5 | 36.9 | 17.334 | 2 \/ 0 | SUCCESS | 0.000337 (JoinMt) | 0.057989, Listener New | 0.057989 | 0.059352 |/| 5 | 36.9 | 17.334 | 2 \/ 0 | SUCCESS | 0.000337 (JoinMt) | 0.057989, Listener New | 0.057989 | 1.059352 |/' "$S/m/$P606"; run m5_firstpdu_b5 "$PKT"
fresh; sed -i 's/^| 12 | 0.013235 | IN (observed) | -0.553 | 7 | +1 \/ +1 |/| 12 | 0.013235 | IN (observed) | -0.553 | 7 | +0 \/ +1 |/' "$S/m/$P608"; run m6_counter_c12 "$PKT"
# Packet-side mutant: move cycle 22's own LeaveAll after the bridge Lv by 5 ms.
fresh; rm -rf "$S/pk" && cp -r "$PKT" "$S/pk"
python3 -I - "$S/pk/cycles/cycle-022/msrp.tsv" <<'EOF'
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")
out = []
for ln in lines:
    f = ln.split("\t")
    if len(f) > 3 and f[1] == "DUT" and f[3] == "LeaveAll" and abs(float(f[0]) - 3.059247408) < 1e-6:
        f[0] = "%.9f" % (float(f[0]) + 0.006)
    out.append("\t".join(f))
open(p, "w").write("\n".join(out))
EOF
run m7_pkt_c22_own_leaveall_late "$S/pk"
