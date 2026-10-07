#!/usr/bin/env python3
"""Reviewer mutants on the round-2 delta of sw/litex/milan_soc.py.

Usage: mutants.py SRC_TREE WORK_DIR PYTHON JOBS
Each mutant gets a hard-linked copy of SRC_TREE (including .git, which the
recipe queries for submodule sources) whose milan_soc.py is replaced
by a NEW file (unlink first, so the shared inode is never written). The tree's
own unmodified sw/builder/test_soc_options.py (refusal bank, no --netlists) then
runs against it. A mutant is KILLED when the bank exits non-zero. The anchor
must occur exactly once or the mutant is reported INVALID.
"""
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SRC, WORK, PY, JOBS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
REL = "sw/litex/milan_soc.py"

MUTANTS = {
    "M01 CLI parser returns float": [("        return Decimal(token)\n", "        return float(token)\n")],
    "M02 CLI parser converts via float": [("        return Decimal(token)\n", "        return Decimal(float(token))\n")],
    "M03 validator converts via float": [("        size = Decimal(l2_bytes)\n", "        size = Decimal(float(l2_bytes))\n")],
    "M04 drop negative check": [("not size.is_finite() or size < 0 or", "not size.is_finite() or")],
    "M05 drop whole-number check": [(" or size != size.to_integral_value():", ":")],
    "M06 drop finiteness check": [("if not size.is_finite() or size < 0", "if size < 0")],
    "M07 unknown CPU check only None": [('    if cpu not in ("vexiiriscv", "naxriscv"):', "    if cpu is None:")],
    "M08 unknown CPU check case-folds": [('    if cpu not in ("vexiiriscv", "naxriscv"):',
                                          '    if str(cpu).lower() not in ("vexiiriscv", "naxriscv"):')],
    "M09 CLI refusal raises instead of exit 2": [("    except ValueError as exc:\n        ap.error(str(exc))\n",
                                                   "    except ValueError as exc:\n        raise\n")],
    "M10 invalid token silently omitted": [('        raise argparse.ArgumentTypeError(\n'
                                            '            "--l2-bytes must be a finite, non-negative whole number of bytes") from exc',
                                            "        return None")],
    "M11 Nax zero refusal skips Decimal": [('    if cpu == "naxriscv" and l2_bytes == 0:',
                                            '    if cpu == "naxriscv" and l2_bytes == 0 and not isinstance(l2_bytes, Decimal):')],
    "M12 parser type is bare Decimal": [("default=None, type=_parse_l2_bytes,", "default=None, type=Decimal,")],
    "M13 negative zero refused": [("not size.is_finite() or size < 0 or", "not size.is_finite() or size.is_signed() or")],
    "M14 validation after CPU check order swap (null)": [],
}


def run(name, muts):
    tag = name.split()[0]
    tree = WORK / tag
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(SRC, tree, copy_function=os.link, symlinks=True)
    target = tree / REL
    text = target.read_text()
    for old, new in muts:
        if text.count(old) != 1:
            return name, {"status": "INVALID", "anchor": old, "count": text.count(old)}
        text = text.replace(old, new)
    target.unlink()
    target.write_text(text)
    proc = subprocess.run([PY, "-B", str(tree / "sw/builder/test_soc_options.py")], cwd=tree,
                          capture_output=True, text=True, timeout=1800,
                          env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0",
                               "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(WORK / "tmp"),
                               "HOME": os.environ["HOME"]})
    (WORK / f"{tag}.log").write_text(proc.stdout + proc.stderr)
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
    if not muts:
        status = "NULL-PASS" if proc.returncode == 0 else "NULL-FAIL"
    else:
        status = "KILLED" if proc.returncode != 0 else "SURVIVED"
    shutil.rmtree(tree)
    return name, {"status": status, "rc": proc.returncode, "tail": tail}


(WORK / "tmp").mkdir(parents=True, exist_ok=True)
results = {}
with cf.ThreadPoolExecutor(JOBS) as pool:
    for name, res in pool.map(lambda kv: run(*kv), MUTANTS.items()):
        results[name] = res
        print(name, res["status"], res.get("rc"), flush=True)
(WORK / "mutation-results.json").write_text(json.dumps(results, indent=1) + "\n")
bad = [n for n, r in results.items() if r["status"] in ("INVALID", "NULL-FAIL")]
print("invalid/null failures:", bad)
sys.exit(1 if bad else 0)
