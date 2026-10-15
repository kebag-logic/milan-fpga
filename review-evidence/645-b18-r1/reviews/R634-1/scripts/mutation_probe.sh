#!/usr/bin/env bash
# Disposable fault probes on a copy of the B18 packet: plant SLIP_LB changes in c10's raw counter log (and the
# end baseline, so the cumulative-counter join stays consistent), rerun the packet's own summary tool and this
# review's independent recompute, and print the grade each reports.
# usage: mutation_probe.sh <scratch_dir_with_rerun> <review_scripts_dir>
set -u
S=$1; SC=$2
cd "$S" || exit 2
mutate() { # name dups_value from_s [to_s]
  local name=$1 val=$2 from=$3
  rm -rf "mut-$name"; cp -a rerun "mut-$name"
  python3 -I - "mut-$name/b18" "$val" "$from" <<'PY'
import json, sys, re
from pathlib import Path
root, val, frm = Path(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
ev = [json.loads(l) for l in open(root / "cycles/c10/events.jsonl")]
bt = [e for e in ev if e["kind"] == "bind-time"][0]["t_bind_local"]
p = root / "cycles/c10/poll.jsonl"
out = []
for l in open(p):
    d = json.loads(l)
    if d["t0"] - bt >= frm:
        d["words"]["0x8d4"] = f"{val:08x}"
    out.append(json.dumps(d))
p.write_text("\n".join(out) + "\n")
e = root / "restore/dut-end.txt"
t = e.read_text()
le = " ".join(f"{b:02x}" for b in val.to_bytes(4, "little"))
t = re.sub(r"^(0x900008d4\s+)00 00 00 00", lambda m: m.group(1) + le, t, flags=re.M)
e.write_text(t)
PY
  (cd "mut-$name" && python3 -I summ_b18.py b18 b17 > run.out 2>&1; echo "summ_rc=$?" >> run.out)
  python3 -I - "mut-$name" <<'PY'
import json, sys
from pathlib import Path
d = json.load(open(Path(sys.argv[1]) / "b18/summary/cycles.json"))
L = d["lane"]
c10 = [c for c in d["cycles"] if c["cycle"] == "c10"][0]
print(sys.argv[1], "held", L["held"], "residual_743", L["residual_743"], "class_c", L["class_c"], "other", L["other"],
      "failed_checks", L["failed_checks"], "c10 grade", c10["grade"], "slip_grades", c10["slip_grades"])
PY
  tail -1 "mut-$name/run.out"
  python3 -I "$SC/recompute_b18.py" "mut-$name/b18" | grep -E '"c10"|LANE' | sed 's/.*"slip_lb": \(\[[^]]*\]\).*/c10 recompute slip_lb \1/'
}
# +2 dups first seen by the poll after t=3.5 s, so its interval (about 3.03 to 3.61 s) holds c10's first burst at 3.26 s: B17's class (c) shape
mutate plus2_burst 2 3.5
# +1 dup first seen by the poll after t=0.3 s, so its interval (about 0.01 to 0.59 s) holds c10's first PDU at 0.190 s and ends before the first burst: the #743 residual shape
mutate plus1_firstpdu 1 0.3
# +1 dup late in the hold: neither shape
mutate plus1_late 1 20.0
