"""Scratch: record every configuration ctrl_boundary explores for each unit of the checkout.
usage: configs.py <repo> <work>"""
import sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402
import fw_rv32  # noqa: E402

seen = []
real = cb.explore


def recording(argv, unit, universe, w, standins=None):
    result = real(argv, unit, universe, w, standins)
    side = "rv32" if any("riscv32" in a for a in argv[:1]) else ("c++" if argv[0] == "g++" else "host")
    seen.append((side, unit, result))
    return result


cb.explore = recording
findings = cb.judge(cb.Trees(cb.CTRL, cb.STACK), fw_rv32.compiler(), work)
print(f"findings: {len(findings)}")
total = 0
for side, unit, result in sorted(seen, key=lambda r: (r[0], str(r[1]))):
    rel = unit.relative_to(repo).as_posix() if unit.is_relative_to(repo) else unit.name
    labels = sorted({s.label or "(default)" for s in result})
    total += len(result)
    print(f"{side:5} {rel}: {len(result)} preprocessing(s); configurations: {'; '.join(labels)}")
print(f"total preprocessings: {total}")
