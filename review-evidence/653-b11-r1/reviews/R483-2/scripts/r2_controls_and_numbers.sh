#!/usr/bin/env bash
# (a) Planted controls for r2_recompute.py: each mutated input must make it fail.
# (b) Numeric tokens of the page and README row at round 1 vs round 2.
# Usage: r2_controls_and_numbers.sh <repo> <author-dir> <scratch-dir>
set -uo pipefail
repo=${1:?repo}; author=${2:?author dir}; scratch=${3:?scratch}
here=$(cd "$(dirname "$0")" && pwd)
page=docs/findings/653_DISCONNECT_ORDER_BENCH.md
r1=6f76d612a3191b77ac8a1fe2b9c66da42aeb405a
r2=6b83de0009673ce2c438985a0f9720f079a3715d
mkdir -p "$scratch/ctl"
git -C "$repo" show "$r2:$page" > "$scratch/ctl/page.md"

run() { python3 "$here/r2_recompute.py" "$1" "$2" > "$scratch/ctl/$3.out" 2>&1; echo $?; }

echo "== (a) planted controls"
echo "clean: rc $(run "$author" "$scratch/ctl/page.md" clean) (expect 0)"

sed 's/its response 1,637.3 µs after it/its response 1,629.8 µs after it/' "$scratch/ctl/page.md" > "$scratch/ctl/page-m1.md"
echo "M1 page response interval replaced by the command's: rc $(run "$author" "$scratch/ctl/page-m1.md" m1) (expect 1); failed: $(grep '^FAIL' "$scratch/ctl/m1.out" | cut -c6- | tr '\n' ';')"

rm -rf "$scratch/ctl/author-m2"; mkdir -p "$scratch/ctl/author-m2"; cp -r "$author/summary" "$author/runs" "$scratch/ctl/author-m2/"
python3 - "$scratch/ctl/author-m2/runs/s1/s1-probe.jsonl" <<'EOF'
import json, sys
p = sys.argv[1]; out = []; done = False
for ln in open(p):
    d = json.loads(ln)
    if not done and d.get("ev") == "si_counters" and d["counters"]["ML"] == 1 and d["counters"]["MU"] == 0:
        d["counters"]["ML"] = 2; done = True
    out.append(json.dumps(d, separators=(",", ":")))
open(p, "w").write("\n".join(out) + "\n")
EOF
echo "M2 one library update planted as 2/0: rc $(run "$scratch/ctl/author-m2" "$scratch/ctl/page.md" m2) (expect 1); failed: $(grep '^FAIL' "$scratch/ctl/m2.out" | cut -c6- | tr '\n' ';')"

rm -rf "$scratch/ctl/author-m3"; mkdir -p "$scratch/ctl/author-m3"; cp -r "$author/summary" "$author/runs" "$scratch/ctl/author-m3/"
python3 - "$scratch/ctl/author-m3/runs/s1/s1-probe.jsonl" <<'EOF'
import json, sys
# Plant a 1/0 counters update inside R01's NotConnected window.
p = sys.argv[1]; rows = [json.loads(l) for l in open(p)]; cyc = None; out = []
for d in rows:
    if d.get("ev") == "cycle_begin":
        cyc = d["tag"]
    out.append(d)
    if cyc == "R01" and d.get("ev") == "si_connection" and d.get("state") == "NotConnected":
        out.append({"t": d["t"] + 10000, "ev": "si_counters", "who": "dut", "idx": 1,
                    "counters": {"ML": 1, "MU": 0, "SI": 0}, "lib_conn": "NotConnected",
                    "compat_names": "IEEE17221|Milan", "n_events": 0})
open(p, "w").write("\n".join(json.dumps(d, separators=(",", ":")) for d in out) + "\n")
EOF
echo "M3 an update planted inside the R01 window: rc $(run "$scratch/ctl/author-m3" "$scratch/ctl/page.md" m3) (expect 1); failed: $(grep '^FAIL' "$scratch/ctl/m3.out" | cut -c6- | tr '\n' ';')"

echo "== (b) numeric tokens, round 1 vs round 2"
for f in "$page" docs/findings/README.md; do
  git -C "$repo" show "$r1:$f" | grep -oE '[0-9][0-9.,/x-]*[0-9]|[0-9]' | sort > "$scratch/ctl/n1"
  git -C "$repo" show "$r2:$f" | grep -oE '[0-9][0-9.,/x-]*[0-9]|[0-9]' | sort > "$scratch/ctl/n2"
  echo "-- $f: tokens removed (multiset): $(comm -23 "$scratch/ctl/n1" "$scratch/ctl/n2" | tr '\n' ' ')"
  echo "-- $f: tokens added (multiset): $(comm -13 "$scratch/ctl/n1" "$scratch/ctl/n2" | tr '\n' ' ')"
done
echo "-- page sections outside the round-2 hunks: per-cycle table rows and hash table rows identical?"
for pat in '^\| (C0|A[0-9]{2}|R0[12]) ' '^\| `b11-a535-' '^\| (Probe|Session|Lane grader|Provided decoder|The header)'; do
  a=$(git -C "$repo" show "$r1:$page" | grep -E "$pat" | sha256sum | cut -c1-16)
  b=$(git -C "$repo" show "$r2:$page" | grep -E "$pat" | sha256sum | cut -c1-16)
  n=$(git -C "$repo" show "$r2:$page" | grep -cE "$pat")
  echo "   rows /$pat/: $n rows, r1 $a r2 $b $([ "$a" = "$b" ] && echo IDENTICAL || echo DIFFERENT)"
done
