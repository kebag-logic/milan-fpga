#!/bin/sh
# Campaign 4: the resmap `shapes` step on the tracked plan at the head, and on
# three planted plans, each in its own work directory, all concurrently, from
# one disposable tree copy (`shapes` exports HEAD; the copy is never edited).
# Usage: c4_shapes.sh <head tree> <receipt dir> <work root>
H=$1; R=$2; W=$3; mkdir -p "$R"; rm -rf "$W"; mkdir -p "$W"
cd "$H" || exit 9
python3 - "$W" <<'EOF'
import json, sys, pathlib
w = pathlib.Path(sys.argv[1])
base = json.load(open("syn/resmap/sweep_plan.json"))
def save(name, edit):
    p = json.loads(json.dumps(base)); edit(p["variants"])
    (w / f"plan-{name}.json").write_text(json.dumps(p, indent=1))
# both expected refusals pinned on a cause their line does not carry
save("foreign", lambda v: [v[n].update(cause="the board section names no part")
                           for n in ("rm_ax7101_8x8_tdm8", "rm_ax7101_8x8_tdm8_2ch")])
# one expected refusal left unmarked: an unexpected refusal
save("unmarked", lambda v: [v["rm_ax7101_8x8_tdm8_2ch"].pop(k) for k in ("expect", "cause")])
# a building variant marked as an expected refusal
save("2x2refused", lambda v: v["rm_ax7101_2x2_tdm8"].update(expect="refused", cause="writable names"))
# a cause that is a true substring of the line but not the writable-name text: must still pass
save("othertext", lambda v: [v[n].update(cause="NAME records")
                             for n in ("rm_ax7101_8x8_tdm8", "rm_ax7101_8x8_tdm8_2ch")])
EOF
go() { # id plan
  python3 syn/resmap/yosys_sweep.py --plan "$2" --work "$W/$1" shapes > "$R/c4_$1.log" 2>&1
  echo $? > "$R/c4_$1.rc"; cp "$W/$1/shapes/outcomes.json" "$R/c4_$1_outcomes.json" 2>/dev/null
}
go tracked syn/resmap/sweep_plan.json &
for p in foreign unmarked 2x2refused othertext; do cp "$W/plan-$p.json" "$R/c4_plan-$p.json"; go "$p" "$W/plan-$p.json" & done
wait
git status --porcelain > "$R/c4_status_after.txt"
echo done > "$R/c4.done"
