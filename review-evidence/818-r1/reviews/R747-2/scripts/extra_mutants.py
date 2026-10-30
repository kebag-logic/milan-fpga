#!/usr/bin/env python3
"""Reviewer-written mutants of the round-2 delta, each applied alone to a disposable copy of the gate modules.

usage: extra_mutants.py <tree-at-head> <scratch> <out-tsv>
Each row: name, self-test rc, the last error line (the arm or refusal that killed it), or SURVIVED.
"""
import concurrent.futures, re, shutil, subprocess, sys
from pathlib import Path

tree, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
ooc = tree / "syn/ooc"
FILES = ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py",
         "pp_resource_gate_set_selftest.py", "pp_placement.py", "pp_placement_selftest.py")
MUT = {
    "Y1 warning suppressed beside a WHS floor miss only": (
        "        if before - after > tolerance:\n",
        '        if before - after > tolerance and not (missed and figure == "WHS_ns"):\n'),
    "Y2 warning suppressed beside a WNS floor miss only": (
        "        if before - after > tolerance:\n",
        '        if before - after > tolerance and not (missed and figure == "WNS_ns"):\n'),
    "Y3 warning printed for any floor miss": (
        "        if before - after > tolerance:\n", "        if before - after > tolerance or missed:\n"),
    "Y4 warning before the regression": (
        '        return "; ".join(notes) or "ok", not missed\n',
        '        return "; ".join(reversed(notes)) or "ok", not missed\n'),
    "Y5 summary line omits the figure warned beside a floor miss": (
        'warned += [figure] if "WARNING: fell" in verdict else []',
        'warned += [figure] if "WARNING: fell" in verdict and "REGRESSION" not in verdict else []'),
    "Y6 corner guard one-way for WHS only": (
        "        if worst != figures[figure]:\n",
        '        if (worst != figures[figure]) if figure == "WNS_ns" else (worst < figures[figure]):\n'),
    "Y7 corner guard one-way for WNS only": (
        "        if worst != figures[figure]:\n",
        '        if (worst < figures[figure]) if figure == "WNS_ns" else (worst != figures[figure]):\n'),
    "Y8 floor miss passes when a fall is also warned": (
        '        return "; ".join(notes) or "ok", not missed\n',
        '        return "; ".join(notes) or "ok", not missed or len(notes) > 1\n'),
}


def run(item):
    name, (old, new) = item
    folder = scratch / re.sub(r"[^A-Za-z0-9_.-]", "_", name)
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for f in FILES:
        shutil.copy2(ooc / f, folder / f)
    src = (folder / "pp_resource_gate.py").read_text()
    if src.count(old) != 1:
        return f"{name}\tNOT-UNIQUE({src.count(old)})\t"
    (folder / "pp_resource_gate.py").write_text(src.replace(old, new))
    r = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                       capture_output=True, text=True, timeout=900)
    lines = (r.stdout + r.stderr).strip().splitlines()
    errs = [l for l in lines if l.startswith("AssertionError") or "Error:" in l or "Refusal:" in l]
    shutil.rmtree(folder)
    return f"{name}\trc={r.returncode}\t{'SURVIVED' if r.returncode == 0 else (errs[-1] if errs else lines[-1])[:300]}"


with concurrent.futures.ThreadPoolExecutor(8) as pool:
    rows = list(pool.map(run, MUT.items()))
out.write_text("\n".join(rows) + "\n")
print("\n".join(rows))
