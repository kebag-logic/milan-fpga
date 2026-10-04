#!/usr/bin/env python3
"""R466 probe: (1) the committed resmap_models code excludes a point whose guard
record lists a refusal, (2) a point with NO guard record is treated exactly like a
guard-clean one (fail-open), and (3) removing the exclusion from the code is not
caught by resmap_models --selftest. Usage: guard_exclusion_probe.py <repo> <work> <scratch>"""
import copy, json, shutil, subprocess, sys
from pathlib import Path
repo, work, scratch = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(repo / "syn/resmap"))
import resmap_models as RM, yosys_sweep as YS
plan = YS.load_plan(YS.PLAN)
summary = json.loads((work / "summary.json").read_text())
key = "N_SPORT_IN_P+N_SPORT_OUT_P+N_STREAM_IN_P+N_STREAM_OUT_P"
def pts(s):
    return [r["point"] for r in RM.parameter_models(plan, s)[key]["data"]]
print("no guard records at all:", pts(summary), "-> unchecked points fitted")
refused = copy.deepcopy(summary)
refused["pp-si9"]["guards"] = {"rc": 0, "refusals": ["planted refusal"], "errors": []}
print("pp-si9 planted refused:", pts(refused))
clean = copy.deepcopy(summary)
for p in clean.values():
    p["guards"] = {"rc": 0, "refusals": [], "errors": []}
print("all guard-clean:", pts(clean), "(identical to the no-record case)")
# mutant: drop the refusal exclusion; does the models self-test notice?
tree = scratch / "models-mutant"
if tree.exists():
    shutil.rmtree(tree)
(tree / "syn").mkdir(parents=True)
shutil.copytree(repo / "syn/resmap", tree / "syn/resmap")
shutil.copytree(repo / "syn/ooc", tree / "syn/ooc")
target = tree / "syn/resmap/resmap_models.py"
text = target.read_text()
old = ' or refusals(summary, point["name"]):\n            continue\n        changes'
assert text.count(old) == 1
text = text.replace(old, ':\n            continue\n        changes')
old2 = 'point["name"] not in summary or refusals(summary, point["name"]):'
assert text.count(old2) == 1
text = text.replace(old2, 'point["name"] not in summary:')
target.write_text(text)
run = subprocess.run([sys.executable, str(target), "--selftest"], capture_output=True, text=True)
print("mutant without guard exclusion: models self-test rc", run.returncode, run.stdout.strip().splitlines()[-1])
shutil.rmtree(tree)
