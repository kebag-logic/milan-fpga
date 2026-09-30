#!/usr/bin/env python3
"""Rerun both round-1 reviewers' gate-1b probes, with their own scripts, on
fresh scratch copies of the committed tree.

usage: rerun_reviewer_probes.py <repo> <scratch> <receipts> <python>

<repo> is the lane worktree at the committed head (only its tracked files are
copied); <scratch> a disposable directory; <receipts> where each probe's log
goes; <python> the interpreter the builder bank runs under.

The one adaptation: R413's plants.py reads the head's firmware bytes from its
review clone, which does not exist on this host, so a copy of it reads them
from a pristine copy of this head's firmware instead (the firmware is
unchanged since 597dba85; the script checks that). Nothing else in either
reviewer's scripts is changed.
"""
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

repo, scratch, receipts, python = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                   Path(sys.argv[3]).resolve(), sys.argv[4])
R412 = Path("$REVIEWS/70L2-r412-1-packet/scripts")
R413 = Path("$REVIEWS/70L2-r413-1-packet/probes")
FW = "sw/firmware/milan_baremetal/milan_baremetal.c"
receipts.mkdir(parents=True, exist_ok=True)
scratch.mkdir(parents=True, exist_ok=True)


def git(*args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True).stdout


head = git("rev-parse", "HEAD").decode().strip()
firmware = git("show", f"HEAD:{FW}")
assert firmware == git("show", f"597dba8593553ad85b1e94936b016907c4d2003a:{FW}"), \
    "the firmware changed since the reviewed head"
pristine = scratch / "pristine-milan_baremetal.c"
pristine.write_bytes(firmware)
plants = scratch / "r413-plants.py"
text = (R413 / "plants.py").read_text()
clone = "$REVIEWS/r413-1-70L2/sw/firmware/milan_baremetal/milan_baremetal.c"
assert text.count(clone) == 1
plants.write_text(text.replace(clone, str(pristine)))


def fresh(name):
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    files = git("ls-files", "-z", "--recurse-submodules")
    subprocess.run(["rsync", "-a", "--from0", "--files-from=-", f"{repo}/", f"{tree}/"],
                   input=files, check=True)
    return tree


def run(log, argv, env=None, cwd=None):
    with (receipts / log).open("w") as stream:
        stream.write(f"# head {head}\n# argv {' '.join(argv)}\n# env {env or {}}\n")
        stream.flush()
        rc = subprocess.run(argv, cwd=cwd or scratch, stdout=stream, stderr=subprocess.STDOUT,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", **(env or {})}).returncode
        stream.write(f"# rc {rc}\n")
    last = [line for line in (receipts / log).read_text().splitlines()
            if "R413 PROBE" in line or "R412 " in line or "GATE" in line][-3:]
    print(f"{log}: rc={rc} :: {' | '.join(item[:260] for item in last)}", flush=True)
    return rc


# R413: plants.py through run_gate1b.py, stopped after the shipping-firmware verdict.
for plant in ("none", "plain_write", "splice_write", "paste_write", "alias_write"):
    tree = fresh(f"r413-{plant}")
    subprocess.run([sys.executable, str(R413 / "instrument_builder.py"),
                    str(tree / "sw/builder/test_builder.py")], check=True, capture_output=True)
    subprocess.run([sys.executable, str(plants), str(tree), plant], check=True, capture_output=True)
    run(f"r413_gate1b_{plant}.log", [python, "-u", str(R413 / "run_gate1b.py"), str(tree)],
        {"R413_STOP_AFTER_BASELINE": "1"})
    if plant == "none":
        run("r413_gate1b_none_forget.log", [python, "-u", str(R413 / "run_gate1b.py"), str(tree)],
            {"R413_STOP_AFTER_BASELINE": "1", "R413_FORCE_FORGET": "1"})

# R412: plant.py, early_stop.py and run_gate1b.py (early and complete).
for probe in ("base", "m_macro_set", "m_macro_addr", "m_ctrl_direct"):
    tree = fresh(f"r412-{probe}")
    subprocess.run([sys.executable, str(R412 / "early_stop.py"), str(tree)], check=True,
                   capture_output=True)
    if probe != "base":
        subprocess.run([sys.executable, str(R412 / "plant.py"), str(tree), probe], check=True,
                       capture_output=True)
    asm = scratch / f"r412-{probe}.s"
    run(f"r412_gate1b_early_{probe}.log", [python, "-u", str(R412 / "run_gate1b.py"), str(tree)],
        {"R412_EARLY": "1", "R412_ASM_OUT": str(asm)}, cwd=tree)
    if asm.exists():
        digest = hashlib.sha256(asm.read_bytes()).hexdigest()
        print(f"  census assembly {asm.name}: {asm.stat().st_size} B sha256 {digest}")
for probe in ("m_macro_set", "m_macro_addr"):
    tree = fresh(f"r412-full-{probe}")
    subprocess.run([sys.executable, str(R412 / "plant.py"), str(tree), probe], check=True,
                   capture_output=True)
    run(f"r412_gate1b_full_{probe}.log", [python, "-u", str(R412 / "run_gate1b.py"), str(tree)],
        cwd=tree)
print("REVIEWER PROBES DONE at", head)
