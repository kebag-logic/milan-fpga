#!/usr/bin/env python3
"""Does the PR body's 'How to reproduce' command reach validate_shipping_image, from both emitters?

usage: cli_reach_probe.py <pristine-tree> <work-dir>
1. Runs the PR #612 body reproduction command verbatim (bash heredoc) at the pristine tree root.
2. In a copy, instruments validate_shipping_image to log its immediate caller's function name,
   reruns the same command, and counts calls per caller.
3. In a copy, forces validate_shipping_image to raise a sentinel refusal on every call; the
   reproduction command must then fail (it must not pass without reaching the check).
"""
import collections, shutil, subprocess, sys
from pathlib import Path

REPRO = '''python3 - <<'PYTHON'
import sys
sys.path.insert(0, "sw/builder")
from test_builder import test_shipping_image_contract, test_soc_shipping_image_contract
test_shipping_image_contract()
test_soc_shipping_image_contract()
PYTHON
'''
C = "sw/builder/aem_image_checks.py"
DEF = "def validate_shipping_image(blob: bytes) -> None:\n"

def run(tree, env=None):
    r = subprocess.run(["bash", "-c", REPRO], cwd=tree, capture_output=True, text=True, timeout=1200, env=env)
    return r.returncode, r.stdout, r.stderr

def variant(pristine, work, name, body):
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    subprocess.run(["cp", "-al", str(pristine), str(tree)], check=True)
    target = tree / C
    text = target.read_text()
    assert text.count(DEF) == 1
    target.unlink()
    target.write_text(text.replace(DEF, DEF + body, 1))
    return tree

pristine, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
rc, out, err = run(pristine)
print(f"1 verbatim repro at head: rc={rc}; gate 36b lines={out.count('[gate 36b]')}; "
      f"SoC identity lines={out.count('SoC/builder images identical')}; stderr tail={err.strip()[-200:]!r}")
log = work / "calls.log"
if log.exists():
    log.unlink()
tree = variant(pristine, work, "instrumented",
    f"    import sys as _s\n    with open({str(log)!r}, 'a') as _f:\n        _f.write(_s._getframe(1).f_code.co_name + '\\n')\n")
rc, out, _ = run(tree)
calls = collections.Counter(log.read_text().split()) if log.exists() else {}
print(f"2 instrumented repro: rc={rc}; checker calls by immediate caller: {dict(calls)}")
tree2 = variant(pristine, work, "forced",
    "    raise ImageCheckError('L6_ORDER: forced sentinel refusal')\n")
rc, out, err = run(tree2)
last = [l for l in (out + err).splitlines() if l.strip()][-1:] 
print(f"3 forced-refusal repro: rc={rc} (must be nonzero); last line {last}")
for t in (tree, tree2):
    shutil.rmtree(t)
