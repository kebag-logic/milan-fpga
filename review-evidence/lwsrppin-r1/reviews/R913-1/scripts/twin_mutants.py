#!/usr/bin/env python3
"""Plant faults in a copy of the twin's Applicant grade and require `twin_mrp.py --selftest` to name each one.

Usage: twin_mutants.py <parent-root> <scratch-dir>
Each mutant is one exact text substitution in tb/verilator/milan_dp/twin_mrp.py, applied to a copy under
<scratch-dir>/mutroot/tb/verilator/<name>/ (twin_decode.py finds sw/firmware/ctrl/test two levels up, which is a
symlink to the parent's). A mutant is CAUGHT when the self-test exits non-zero; ESCAPED otherwise. The control is
the unmutated copy, which must pass.
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    # the old model: the Applicant also takes the sLA's rLA!, after its txLA!
    "rla-after-txla": ("    outcomes = transmit(leave_all, config, part)\n",
                       "    outcomes = transmit(leave_all, config, part)\n"
                       "    if leave_all:\n"
                       "        outcomes = [(s, step('rLA!', m, part)) for s, m in outcomes]\n"),
    # the old model's other order: rLA! before txLA!
    "rla-before-txla": ("    outcomes = transmit(leave_all, config, part)\n",
                        "    outcomes = transmit(True, step('rLA!', config, part), part) if leave_all else "
                        "transmit(False, config, part)\n"),
    # txLAF! allowed in any LeaveAll frame, full or not
    "txlaf-unconditional": ("    if leave_all and full:\n", "    if leave_all:\n"),
    # txLAF! leaves QA where it is (Table 10-3 says VP)
    "txlaf-qa-stays": ('TXLAF = _row("LO VP VN VN VP VP LO LO LO VP VP -")',
                       'TXLAF = _row("LO VP VN VN VP -  LO LO LO VP VP -")'),
    # txLA! from QA is optional ([sJ]) rather than sJ
    "txla-qa-bracketed": ('TXLA = (_row("[s] s  sN sN sJ sJ   [s] [s] [s] sJ sJ [s]"),',
                          'TXLA = (_row("[s] s  sN sN sJ [sJ] [s] [s] [s] sJ sJ [s]"),'),
    # the room counts a 1514-octet frame rather than 1500 octets of MRPDU
    "room-1514": ("MRPDU_ROOM = 1500\n", "MRPDU_ROOM = 1514\n"),
    # the smallest vector forgets its VectorHeader
    "vector-no-header": ("    return 2 + WIDTH[application][kind] + 1 +", "    return WIDTH[application][kind] + 1 +"),
    # the MVRP walk forgets the PDU's closing EndMark
    "mvrp-no-final-endmark": ("    return offset + 2 - s.at\n", "    return offset - s.at\n"),
    # the Registrar takes no rLA! after txLAF! (Table 10-4 has no txLAF! row; the sLA's rLA! still reaches it)
    "txlaf-registrar-kept": ('part.registrar["rLA!"].get(registrar, registrar))))',
                             'registrar)))'),
}


def run(root: Path, scratch: Path) -> int:
    src = root / "tb/verilator/milan_dp"
    mutroot = scratch / "mutroot"
    (mutroot / "tb/verilator").mkdir(parents=True, exist_ok=True)
    link = mutroot / "sw"
    if not link.exists():
        link.symlink_to(root / "sw")
    escaped = 0
    for name, (old, new) in [("control", ("", "")), *MUTANTS.items()]:
        where = mutroot / "tb/verilator" / name
        where.mkdir(exist_ok=True)
        for py in src.glob("*.py"):
            shutil.copy2(py, where / py.name)
        target = where / "twin_mrp.py"
        text = target.read_text(encoding="utf-8")
        if old:
            if text.count(old) != 1:
                print(f"{name}: SUBSTITUTION NOT UNIQUE ({text.count(old)})")
                escaped += 1
                continue
            target.write_text(text.replace(old, new), encoding="utf-8")
        res = subprocess.run([sys.executable, "-B", "-E", "-s", "twin_mrp.py", "--selftest"], cwd=where,
                             capture_output=True, text=True, check=False)
        out = (res.stdout + res.stderr).strip().splitlines()
        last = out[-1] if out else ""
        if name == "control":
            verdict = "PASS" if res.returncode == 0 else "CONTROL FAILED"
            escaped += res.returncode != 0
        else:
            verdict = "CAUGHT" if res.returncode != 0 else "ESCAPED"
            escaped += res.returncode == 0
        print(f"{name}: {verdict} rc={res.returncode}: {last}")
    print(f"twin_mutants: {len(MUTANTS)} mutants, {escaped} escaped or failed")
    return 1 if escaped else 0


if __name__ == "__main__":
    sys.exit(run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()))
