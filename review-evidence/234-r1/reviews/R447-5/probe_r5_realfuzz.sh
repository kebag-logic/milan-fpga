#!/usr/bin/env bash
# Run the surviving reviewer mutants of probe_r5_namekill.py under --fuzz on A's real route (6 manifest entries,
# the committed baseline), which the shipped gates do not run, to see whether real data would reach them.
# Usage: probe_r5_realfuzz.sh <repo checkout> <A route dir> <scratch dir> <cases>
set -u
repo=$1 route=$2 scratch=$3 cases=$4
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$scratch"; mkdir -p "$scratch"
python3 - "$repo" "$scratch" "$here/probe_r5_namekill.py" <<'PY'
import sys, shutil, runpy
from pathlib import Path
repo, scratch, probe = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
mutants = runpy.run_path(probe)["MUTANTS"]
wanted = ["reject: walk visits only the first item of a list", "reject: scope class matched on the last two keys",
          "accept: NAME drops the colon", "accept: NAME capped at 64"]
for name in ["control"] + wanted:
    folder = scratch / "".join(ch if ch.isalnum() else "_" for ch in name)
    folder.mkdir()
    for module in ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py",
                   "pp_resource_baseline.json"):
        shutil.copy(repo / "syn/ooc" / module, folder / module)
    if name != "control":
        old, new = mutants[name]
        text = (folder / "pp_resource_gate.py").read_text()
        assert text.count(old) == 1, name
        (folder / "pp_resource_gate.py").write_text(text.replace(old, new))
    print(folder.name)
PY
for folder in "$scratch"/*/; do
  ( cd "$folder" && python3 -B pp_resource_gate.py --fuzz "$cases" --seed 234 check "$route" --endpoint route-1x1 \
      --baseline pp_resource_baseline.json --budget "$repo/docs/design/AREA_BUDGET.md" > run.log 2>&1; echo $? > run.rc ) &
done
wait
for folder in "$scratch"/*/; do
  printf '%s rc=%s :: %s\n' "$(basename "$folder")" "$(cat "$folder/run.rc")" "$(grep 'cases at seed' "$folder/run.log")"
  grep 'FAILURE' "$folder/run.log" | head -2 | cut -c1-240 | sed 's/^/    /'
done
