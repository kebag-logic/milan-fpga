#!/usr/bin/env python3
"""Reviewer receipt R391-3 item 4: for each nvm_cosim variant, the B1-B4 record
0x20/0x21 port operations (op 1 = WRITE, 2 = ERASE; their end cycle at the
suite's 1 MHz clock, i.e. microseconds) and the status observations at each
snapshot (pend, alarm, backed, stale, the binding manager's dirty sinks).
Usage: cosim_b_timeline.py <cosim scratch dir> <variant> ...
"""
import json
import sys
from pathlib import Path

CASES = ("B1_erase_error_full_span", "B2_erase_error_partial_span",
         "B3_erase_error_no_byte", "B4_write_error_after_erase")


def main() -> int:
    root = Path(sys.argv[1])
    for var in sys.argv[2:]:
        runs = root / f"parent-{var}" / "tb/verilator/nvm_cosim/runs/contract-1x1"
        for case in CASES:
            log = runs / case / "stdout.log"
            if not log.exists():
                print(f"{var} {case}: no run")
                continue
            ops, obs = [], []
            for line in log.read_text().splitlines():
                if line.startswith("EVT "):
                    e = json.loads(line[4:])
                    if e.get("k") == "op" and e.get("op") in (1, 2) and e.get("rid") in (32, 33):
                        ops.append(f"{'W' if e['op'] == 1 else 'E'}{e['rid']:02x}@{e['end']}:{e['res']}")
                elif line.startswith("OBS "):
                    o = json.loads(line[4:])
                    obs.append(f"{o['tag']}@{o['ms']}ms pend {o['pend']} alarm {o['alarm']} "
                               f"backed {o['backed']} stale {o['stale']} mgr_dirty {o['mgr_dirty']}")
            print(f"{var} {case}:\n  ops  " + " ".join(ops) + "\n  obs  " + "; ".join(obs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
