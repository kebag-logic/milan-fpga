#!/usr/bin/env bash
# plants.sh <head> <scratch dir> <receipts dir>: stale-page mutants for the two freshness gates, on a
# disposable clean clone, each restored before the next. Records each gate's rc and last lines.
set -u
H=$1; D=$2; R=$3; T=$(dirname "$0")
PY=$VALIDATION_STORAGE/797-a711g/gates/venv/bin/python3  # carries the pinned wavedrom the register gate needs
mkdir -p "$R"
bash "$T/clone_at.sh" "$H" "$D" || exit 2
cd "$D" || exit 2
plant() {  # plant <name> <expected rc> <gate command...>; the mutation is already applied
  n=$1; want=$2; shift 2
  "$@" > "$R/$n.log" 2>&1; rc=$?
  echo "$rc" > "$R/$n.rc"
  git diff --stat > "$R/$n.mutation.txt"
  git checkout -q -- . ; git clean -qfd
  printf '%s want=%s got=%s %s\n' "$n" "$want" "$rc" "$([ "$rc" = "$want" ] && echo OK || echo MISMATCH)" >> "$R/SUMMARY.txt"
}
: > "$R/SUMMARY.txt"
inv="python3 scripts/docs_inventory.py --check"
# P0 control: the head as committed.
plant p0_control 0 $inv
# P1: the pre-change audit page (round-7 head) against the new data file: stale.
git show 1de759d3:docs/DOCUMENTATION_AUDIT.md > docs/DOCUMENTATION_AUDIT.md
plant p1_old_audit_page 1 $inv
# P2: the round-7 data file (all 65 entries) against the new page: stale.
git show 1de759d3:scripts/docs_inventory.json > scripts/docs_inventory.json
plant p2_old_data_file 1 $inv
# P3: one removed entry (D0-018, the "on page" one) restored alone: stale.
python3 -I - <<'PY'
import json, subprocess
old = json.loads(subprocess.run(["git", "show", "1de759d3:scripts/docs_inventory.json"], capture_output=True, text=True, check=True).stdout)
new = json.load(open("scripts/docs_inventory.json", encoding="utf-8"))
ids = [f["id"] for f in old["findings"]]
entry = next(f for f in old["findings"] if f["id"] == "D0-018")
pos = ids.index("D0-018")
keep = [f for f in old["findings"][:pos] if f["id"] in {g["id"] for g in new["findings"]}]
new["findings"].insert(len(keep), entry)
open("scripts/docs_inventory.json", "w", encoding="utf-8").write(json.dumps(new, indent=1, ensure_ascii=False) + "\n")
PY
plant p3_restore_D0-018 1 $inv
# P4: a kept entry (D0-040) dropped from the data file: its five rows vanish, so the page is stale.
python3 -I - <<'PY'
import json
d = json.load(open("scripts/docs_inventory.json", encoding="utf-8"))
d["findings"] = [f for f in d["findings"] if f["id"] != "D0-040"]
open("scripts/docs_inventory.json", "w", encoding="utf-8").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
PY
plant p4_drop_kept_D0-040 1 $inv
# P5: the committed audit marks REGISTER_MAP_CLASSES.md current while its Findings table lists D0-040.
sed -i 's#| stale | 1 finding(s): D0-040 |#| current | no recorded contradiction |#' docs/DOCUMENTATION_AUDIT.md
plant p5_classes_marked_current 1 $inv
# P6: the register reference page edited by hand (one register name in a heading): stale.
python3 -I - <<'PY'
p = "docs/reference/REGISTER_MAP.md"
s = open(p, encoding="utf-8").read()
assert "ETH_GUARD" in s
open(p, "w", encoding="utf-8").write(s.replace("ETH_GUARD", "ETH_GAURD", 1))
PY
plant p6_regmap_hand_edit 1 "$PY" scripts/gen_register_reference.py --check
# P7: control for the register gate.
plant p7_regmap_control 0 "$PY" scripts/gen_register_reference.py --check
test -z "$(git status --porcelain)" && echo clean > "$R/final_restore.txt" || git status --porcelain > "$R/final_restore.txt"
