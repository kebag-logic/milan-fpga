#!/usr/bin/env python3
"""Re-run round-1 planted forms at the head under review.

Usage: prior_probes.py <checkout> <pristine-tree> <scratch-dir>
Part 1: inventory forms from R638-1-F3 and R639-1-F2 (outcome REFUSED / LISTED / SILENT on --write).
Part 2: lock mutations from R639-1-F3 against build.py --check-lock (expect rc 2).
"""
import json, shutil, subprocess, sys
from pathlib import Path

checkout, pristine, scratch = map(Path, sys.argv[1:4])
WF = ".github/workflows/docs.yml"
DERIVE = checkout / "scripts/ci_tool_inventory.py"


def fresh(name):
    tree = scratch / ("prior-" + name)
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(pristine, tree, symlinks=True)
    return tree


def add_step(tree, text):
    path = tree / WF
    s = path.read_text()
    i = s.index("    steps:\n") + len("    steps:\n")
    path.write_text(s[:i] + "".join("      " + l + "\n" for l in text.splitlines()) + s[i:])


def script_step(tree, body):
    (tree / "scripts/planted_boot.py").write_text("import os, subprocess\n" + body)
    add_step(tree, "- name: planted\n  run: python3 scripts/planted_boot.py")


def makefile(tree, recipe):
    path = tree / "tb/verilator/planted/Makefile"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("all:\n\t" + recipe + "\n")


FORMS = {
    "R638-1-F3 setup-java": lambda t: add_step(t, "- uses: actions/setup-java@v4\n  with:\n    java-version: '21'\n    distribution: temurin"),
    "R638-1-F3 pipx": lambda t: add_step(t, "- name: planted\n  run: pipx install plantedtool==1.0"),
    "R638-1-F3 Makefile pip": lambda t: makefile(t, "pip install plantedtool==1.0"),
    "R638-1-F3 shell=True string": lambda t: script_step(t, "subprocess.run('pip install plantedtool==1.0', shell=True)\n"),
    "R638-1-F3 os.system": lambda t: script_step(t, "os.system('apt-get install -y plantedtool')\n"),
    "R639-1-F2 command variable": lambda t: script_step(t, "cmd = ['pip', 'install', 'plantedtool==1.0']\nsubprocess.run(cmd, check=True)\n"),
    "R639-1-F2 shell string python -m pip": lambda t: script_step(t, "subprocess.run('python3 -m pip install plantedtool==1.0', shell=True, check=True)\n"),
}
out = {"inventory": {}, "lock": {}}
for name, plant in FORMS.items():
    tree = fresh("inv")
    plant(tree)
    w = subprocess.run([sys.executable, "-I", str(DERIVE), "--root", str(tree), "--write"], capture_output=True, text=True)
    listed = w.returncode == 0 and "plantedtool" in json.dumps(json.loads((tree / "ci/image/tool-inventory.json").read_text())["tools"])
    out["inventory"][name] = {"write_rc": w.returncode, "err": w.stderr.strip()[:160],
                              "outcome": "REFUSED" if w.returncode else ("LISTED" if listed else "SILENT")}
    shutil.rmtree(tree)

# Part 2: lock mutations, run against a copy of the checkout's ci/image so the real lock is never edited.
MUT = {
    "empty layers": lambda d: d.__setitem__("layers", []),
    "invalid layer tool version": lambda d: d["layers"][4]["tools"][0].__setitem__("version", "v9.999"),
    "all-zero image digest": lambda d: d.__setitem__("image_digest", "sha256:" + "0" * 64),
    "different platform": lambda d: d.__setitem__("platform", "linux/arm64"),
    "ubuntu:latest base": lambda d: d.__setitem__("base", "ubuntu:latest"),
    "clean (control)": lambda d: None,
}
work = scratch / "prior-lockwork"
work.mkdir(exist_ok=True)
for name, mutate in MUT.items():
    tree = fresh("lock")
    # build.py and image_lock.py resolve the repository from their own location, so run the copy.
    lock = tree / "ci/image/image.lock.json"
    data = json.loads(lock.read_text())
    mutate(data)
    lock.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")
    r = subprocess.run([sys.executable, str(tree / "ci/image/build.py"), "--work", str(work), "--check-lock"],
                       capture_output=True, text=True)
    out["lock"][name] = {"rc": r.returncode, "msg": (r.stderr or r.stdout).strip()[:160]}
    shutil.rmtree(tree)
print(json.dumps(out, indent=1))
