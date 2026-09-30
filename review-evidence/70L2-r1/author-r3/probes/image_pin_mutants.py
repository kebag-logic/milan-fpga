#!/usr/bin/env python3
"""Gate mutants of the round-3 linked-image census (verdict_image_pins()).

usage: image_pin_mutants.py <scratch-tree> <work-dir>

<scratch-tree> is an export of the head under test (never the lane). For each mutant this
copies the tree's sw/builder/test_builder.py into <work-dir>/<name>/ as a hard-linked tree
whose test_builder.py is a fresh file, applies one edit (each asserted to match once),
instruments it with instrument_verdict_controls_r3.py, and runs the gate's verdict-pin
controls with --require-rv32. A mutant is KILLED when the gate refuses (rc != 0); the
refusal's first line is printed. M0 is the identity and must pass.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
PY = "$WORKSPACE_HOME/litex-milan/venv/bin/python"
RUN = "$REVIEWS/70L2-r413-2-packet/probes/run_gate1b.py"

MUTANTS = {
    "M0 identity": [],
    "G0 verdict_image_pins() breaks nothing (early diagnostics alone)": [
        ("        named = [symbol for symbol in image[\"symbols\"]\n",
         "        return [], []\n        named = [symbol for symbol in image[\"symbols\"]\n")],
    "G1 one-name pin dropped": [
        ("        if others:\n", "        if False:\n")],
    "G2 escape pin dropped": [
        ("        if escapes:\n", "        if False:\n")],
    "G3 locality pin dropped": [
        ("        if not verdict[\"local\"]:\n", "        if False:\n")],
    "G4 AUIPC pin dropped": [
        ("        elif image[\"bare_auipc\"]:\n", "        elif False:\n")],
    "G5 store pin: the image's in-place stores not read": [
        ("        if stores != [\"milan_init()\"] or \\\n", "        if False or \\\n")],
    "G6 store pin: the resolver's by-address stores not read": [
        ("                writes != [(\"milan_init\", Rv32Tag(\"call:load_aem_image\"))]:\n",
         "                False:\n")],
}

work.mkdir(parents=True, exist_ok=True)
source = (tree / "sw/builder/test_builder.py").read_text()
results = []
for name, edits in MUTANTS.items():
    slug = name.split()[0]
    copy = work / slug
    if copy.exists():
        shutil.rmtree(copy)
    subprocess.run(["cp", "-al", str(tree), str(copy)], check=True)
    target = copy / "sw/builder/test_builder.py"
    target.unlink()  # break the hard link before writing
    text = source
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    target.write_text(text)
    subprocess.run([sys.executable, str(HERE / "instrument_verdict_controls_r3.py"), str(target)],
                   check=True, capture_output=True)
    env = dict(os.environ, A457_STOP_AFTER_VERDICT_CONTROLS="1", PYTHONDONTWRITEBYTECODE="1")
    got = subprocess.run([PY, RUN, str(copy)], capture_output=True, text=True, env=env)
    lines = got.stdout.splitlines()
    verdict = next((line for line in lines if line.startswith("GATE REFUSED")), None)
    summary = next((line for line in lines if line.startswith("A457 PROBE")), "")
    status = "KILLED" if got.returncode else "passes"
    results.append((name, status))
    print(f"=== {name}: {status} (rc={got.returncode})")
    print("   ", (verdict or summary)[:900])
    shutil.rmtree(copy)
print()
for name, status in results:
    print(f"{status:7s} {name}")
identity_ok = results[0][1] == "passes"
all_killed = all(status == "KILLED" for _name, status in results[1:])
print("MUTANTS", "OK" if identity_ok and all_killed else "NOT OK")
sys.exit(0 if identity_ok and all_killed else 1)
