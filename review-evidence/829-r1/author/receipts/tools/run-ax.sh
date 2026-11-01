#!/usr/bin/env bash
# run-ax.sh <tree> <tag>: the AX7101 1x1 shipping route by docs/testing/PP_SHADOW_BASELINE_RECIPE.md, judged against route-1x1; rc in a file.
set -u
tree=$1 tag=$2
S=$VALIDATION_STORAGE/829-a725b
W=$S/ax/$tag
rcf=$S/rc/ax-$tag.rc
finish() { echo "$1" > "$rcf"; echo "== END-OF-RUN tag=$tag rc=$1 $(date -Iseconds) $2"; exit "$1"; }
mkdir -p "$W" "$S/rc"
cd "$tree" || finish 3 "no tree"
echo "== START tag=$tag head=$(git rev-parse HEAD) $(date -Iseconds)"
[ -z "$(git status --short)" ] || finish 4 "dirty tree"
source $WORKSPACE_HOME/Xilinx2/2026.1/Vivado/settings64.sh
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$PATH PYTHONHASHSEED=0 TMPDIR=$S/tmp
export REPO=$tree WORK=$W LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml --write-rtl > "$W/writertl.log" 2>&1 || finish 5 "write-rtl"
git status --short > "$W/moved.txt"
(cd sw/litex && TAG=$tag ./build.sh ax7101 --dry-run) > "$W/ax7101-dry-run.log" 2>&1 || finish 6 "dry-run"
grep -q REFUSED "$W/ax7101-dry-run.log" && finish 8 "dry run previews a refusal"
python3 - <<'PY' || finish 7 "elaboration"
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
lines = [l for l in (work / "ax7101-dry-run.log").read_text().splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
(work / "ax7101-argv.json").write_text(json.dumps(argv, indent=2))
with (work / "ax7101-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis > "$W/baseline-prep.log" 2>&1 || finish 9 "pp_baseline"
(cd "$W/ax7101/gateware" && vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > "$W/vivado.stdout" 2>&1)
v=$?
echo "== vivado rc=$v $(date -Iseconds)"
python3 syn/ooc/pp_resource_gate.py check "$W/ax7101/gateware" --endpoint route-1x1 --shipping-selection > "$W/gate.log" 2>&1
g=$?
echo "== gate rc=$g $(date -Iseconds)"
xargs -r git checkout -- < <(awk '{print $2}' "$W/moved.txt")
finish $(( v != 0 ? v : g )) "vivado=$v gate=$g"
