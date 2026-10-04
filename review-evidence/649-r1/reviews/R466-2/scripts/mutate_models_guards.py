#!/usr/bin/env python3
"""R466-2 probe: disable each guard path of syn/resmap/resmap_models.py in a disposable copy and record
whether `--selftest` still passes; then, on the published summary, delete one point's guard record (and
plant a hard error on another) and require the unmodified models CLI to refuse naming the point.
Usage: mutate_models_guards.py <repo> <scratch dir> <round-2 inputs dir (summary.json decompressed)>"""
import copy, json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
repo, scratch, inputs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
MUTANTS = {
    "missing-record-reads-clean": ("    if guards is None:\n        raise GuardError", "    if guards is None:\n        return []\n        raise GuardError"),
    "hard-error-reads-clean": ("    if guards.get(\"errors\") or (guards.get(\"rc\") and not guards.get(\"refusals\")):", "    if False:"),
    "stream-exclusion-off": ("        if point.get(\"patch\") or point[\"name\"] not in summary or refusals(summary, point[\"name\"]):",
                             "        if point.get(\"patch\") or point[\"name\"] not in summary:"),
    "processor-exclusion-off": ("        if point[\"top\"] != \"KL_pp_shadow\" or point[\"name\"] not in summary or refusals(summary, point[\"name\"]):",
                                "        if point[\"top\"] != \"KL_pp_shadow\" or point[\"name\"] not in summary:"),
    "calibration-exclusion-off": ("        if name not in summary or \"opt\" not in data or refusals(summary, name):",
                                  "        if name not in summary or \"opt\" not in data:"),
    "tdm-exclusion-off": ("        if point[\"name\"] in summary and not refusals(summary, point[\"name\"]):",
                          "        if point[\"name\"] in summary:"),
    "build-upfront-check-off": ("    if unusable:\n        raise GuardError", "    if False:\n        raise GuardError"),
    "rank-check-off": ("    if rank < design.shape[1]:", "    if False:"),
}


def run(item):
    name, (old, new) = item
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    (tree / "syn").mkdir(parents=True)
    for d in ("resmap", "ooc"):
        shutil.copytree(repo / "syn" / d, tree / "syn" / d, ignore=shutil.ignore_patterns("__pycache__"))
    target = tree / "syn/resmap/resmap_models.py"
    text = target.read_text()
    if text.count(old) != 1:
        shutil.rmtree(tree)
        return name, "ABSENT", None, f"site occurs {text.count(old)} times"
    target.write_text(text.replace(old, new))
    proc = subprocess.run([sys.executable, str(target), "--selftest"], capture_output=True, text=True)
    out = (proc.stdout + proc.stderr).strip().splitlines()
    shutil.rmtree(tree)
    first = next((l for l in out if l.startswith("SELF-TEST FAILED")), out[-1] if out else "")
    return name, "SURVIVED" if proc.returncode == 0 else "KILLED", proc.returncode, first[:160]


with ThreadPoolExecutor(8) as pool:
    for name, verdict, rc, detail in pool.map(run, MUTANTS.items()):
        print(f"mutant {name:28s} {verdict:8s} rc={rc} {detail}")

summary = json.loads((inputs / "work/summary.json").read_text())
for label, damage in (("adp-if-1 guard record deleted (a reference point in no fit)", lambda s: s["adp-if-1"].pop("guards")),
                      ("no-crf guard record deleted (a marginal-only point)", lambda s: s["no-crf"].pop("guards")),
                      ("pp-si5 lint hard error planted", lambda s: s["pp-si5"]["guards"].update(errors=["%Error: x.sv:1"]))):
    work = scratch / "guard-work"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(inputs / "work", work)
    broken = copy.deepcopy(summary)
    damage(broken)
    (work / "summary.json").write_text(json.dumps(broken))
    proc = subprocess.run([sys.executable, str(repo / "syn/resmap/resmap_models.py"), "--work", str(work), "--map",
                           str(inputs / "map"), "--out", str(scratch / "guard-out")], capture_output=True, text=True)
    print(f"unmodified models CLI, {label}: rc {proc.returncode}: {(proc.stdout + proc.stderr).strip()[:200]}")
    shutil.rmtree(work)
