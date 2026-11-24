#!/usr/bin/env python3
"""Disposable mutants of tb/verilator/milan_dp/twin_mrp.py for the round-2 delta.

usage: python3 -I -B r2_mutants.py <repo> <scratch>

Each mutant is one exact text substitution (it must match once) in a copy of twin_mrp.py under <scratch>;
the copy runs `--selftest` with the repo's milan_dp directory on PYTHONPATH for twin_decode. A mutant is
CAUGHT when the self-test exits non-zero; the line printed and the failed names are recorded. The control
(no substitution) must exit 0. The repository is never written.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    "control": None,
    # the delta's subject: the sLA's rLA! must reach the Registrar at txLAF!
    "txlaf-registrar-kept": ('part.registrar["rLA!"].get(registrar, registrar))))', "registrar)))"),
    "txlaf-registrar-to-mt": ('part.registrar["rLA!"].get(registrar, registrar))))',
                              '"MT" if registrar == "IN" else registrar)))'),
    "txlaf-applicant-kept": ("(TXLAF.get(applicant, applicant), part", "(applicant, part"),
    "txlaf-outcome-dropped": ("    if leave_all and full:\n", "    if False:\n"),
    "rjoinin-not-registering": ('"rJoinIn!": {"LV": "IN", "MT": "IN"},', '"rJoinIn!": {},'),
    # the census: a check that is not counted, or none counted, must not print OK with a false count
    "census-not-counted": ("        executed.append(name)\n", ""),
    "census-zero-checks": ("    executed = [] if ran is None else ran\n",
                           "    executed = [] if ran is None else ran\n    ran = executed = []\n"),
}


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    src = (repo / "tb/verilator/milan_dp/twin_mrp.py").read_text()
    env = {**os.environ, "PYTHONPATH": str(repo / "tb/verilator/milan_dp"), "PYTHONDONTWRITEBYTECODE": "1"}
    caught = escaped = 0
    for name, sub in MUTANTS.items():
        text = src
        if sub is not None:
            if src.count(sub[0]) != 1:
                print(f"{name}: SUBSTITUTION MATCHES {src.count(sub[0])} TIMES")
                return 2
            text = src.replace(sub[0], sub[1])
        out = scratch / name
        out.mkdir(parents=True, exist_ok=True)
        (out / "twin_mrp.py").write_text(text)
        run = subprocess.run([sys.executable, "-B", str(out / "twin_mrp.py"), "--selftest"], env=env,
                             capture_output=True, text=True, check=False)
        line = (run.stdout.strip().splitlines() or [run.stderr.strip().splitlines()[-1]])[-1]
        if name == "control":
            verdict = "PASS" if run.returncode == 0 else "CONTROL FAILED"
        elif run.returncode != 0:
            verdict, caught = "CAUGHT", caught + 1
        else:
            verdict, escaped = "ESCAPED", escaped + 1
        print(f"{name}: rc {run.returncode} {verdict} | {line}")
    print(f"summary: {caught} caught, {escaped} escaped of {len(MUTANTS) - 1}")
    return 0 if escaped == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
