#!/usr/bin/env python3
"""Reviewer drift probes for scripts/ci_tool_inventory.py (run with -I).

Usage: inventory_probes.py <checkout> <pristine-tree> <scratch-dir>
For each planted installation form, copy the pristine tree, plant the form,
then run the deriver in --check and --write modes.  An outcome is:
  REFUSED  - --write refused (rc 2): the form cannot be dropped silently
  LISTED   - --write succeeded and the planted tool appears in the tools list
  SILENT   - --write succeeded and the planted tool is absent (drop)
"""
import json, shutil, subprocess, sys
from pathlib import Path

checkout, pristine, scratch = map(Path, sys.argv[1:4])
DERIVE = checkout / "scripts/ci_tool_inventory.py"
WF = ".github/workflows/docs.yml"


def step(tree, text):
    path = tree / WF
    source = path.read_text()
    marker = "    steps:\n"
    i = source.index(marker) + len(marker)
    block = "".join("      " + line + "\n" for line in text.splitlines())
    path.write_text(source[:i] + block + source[i:])


def job(tree, text):
    path = tree / WF
    source = path.read_text()
    marker = "jobs:\n"
    i = source.index(marker) + len(marker)
    path.write_text(source[:i] + "".join("  " + l + "\n" for l in text.splitlines()) + source[i:])


PROBES = {
    "control-apt": (lambda t: step(t, "- name: planted\n  run: sudo apt-get install -y plantedtool"), "plantedtool"),
    "dpkg-i": (lambda t: step(t, "- name: planted\n  run: sudo dpkg -i /tmp/plantedtool.deb"), "plantedtool"),
    "npx": (lambda t: step(t, "- name: planted\n  run: npx --yes plantedtool@1.2.3 --version"), "plantedtool"),
    "go-install": (lambda t: step(t, "- name: planted\n  run: go install example.com/plantedtool@v1.0.0"), "plantedtool"),
    "snap": (lambda t: step(t, "- name: planted\n  run: sudo snap install plantedtool"), "plantedtool"),
    "uv-tool": (lambda t: step(t, "- name: planted\n  run: uv tool install plantedtool"), "plantedtool"),
    "docker-run": (lambda t: step(t, "- name: planted\n  run: docker run --rm example/plantedtool:1 --version"), "plantedtool"),
    "git-fetch": (lambda t: step(t, "- name: planted\n  run: git -C /tmp/x fetch https://github.com/example/plantedtool v1"), "plantedtool"),
    "python-urllib": (lambda t: ((t / "scripts/planted_fetch.py").write_text(
        "import urllib.request\nurllib.request.urlretrieve('https://example.com/plantedtool-1.0.tgz', '/tmp/p.tgz')\n"),
        step(t, "- name: planted\n  run: python3 scripts/planted_fetch.py")), "plantedtool"),
    "job-container": (lambda t: job(t, "planted:\n  runs-on: ubuntu-24.04\n  container: example/plantedtool:1\n  steps:\n    - run: echo ok"), "plantedtool"),
    "job-services": (lambda t: job(t, "planted:\n  runs-on: ubuntu-24.04\n  services:\n    db:\n      image: example/plantedtool:1\n  steps:\n    - run: echo ok"), "plantedtool"),
    "unused-inventory-entry": (None, None),
}

results = {}
for name, (plant, needle) in PROBES.items():
    tree = scratch / ("probe-" + name)
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(pristine, tree, symlinks=True)
    if plant is None:
        inv = tree / "ci/image/tool-inventory.json"
        data = json.loads(inv.read_text())
        data["tools"].append({"tool": "plantedtool", "kind": "apt", "pin": None, "installed_by": []})
        inv.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")
        check = subprocess.run([sys.executable, "-I", str(DERIVE), "--root", str(tree), "--check"],
                               capture_output=True, text=True)
        results[name] = {"check_rc": check.returncode, "check_err": check.stderr.strip()[:200],
                         "outcome": "DETECTED" if check.returncode else "SILENT"}
        continue
    plant(tree)
    check = subprocess.run([sys.executable, "-I", str(DERIVE), "--root", str(tree), "--check"],
                           capture_output=True, text=True)
    write = subprocess.run([sys.executable, "-I", str(DERIVE), "--root", str(tree), "--write"],
                           capture_output=True, text=True)
    listed = False
    if write.returncode == 0:
        tools = json.loads((tree / "ci/image/tool-inventory.json").read_text())["tools"]
        listed = any(needle in json.dumps(row) for row in tools)
    outcome = "REFUSED" if write.returncode else ("LISTED" if listed else "SILENT")
    results[name] = {"check_rc": check.returncode, "write_rc": write.returncode,
                     "write_err": write.stderr.strip()[:200], "outcome": outcome}
    shutil.rmtree(tree)
print(json.dumps(results, indent=1))
