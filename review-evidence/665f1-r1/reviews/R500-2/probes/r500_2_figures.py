#!/usr/bin/env python3
"""R500-2: re-measure the module page's model-time figures at the head
("The service bound": the longest call in the bound run, 168 us on the model
port and 210 us on LiteSPI at 1x1 and 8x8; a dead master's calls 164 us).
Run from the head's checkout root:

    python3 /path/to/r500_2_figures.py <scratch-dir>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))

import test_ctrl_nvm as gate                             # noqa: E402
from nvm_bench import shape_inputs                       # noqa: E402


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    for stem in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
        inputs = shape_inputs(ROOT / f"configs/{stem}.yaml", work / stem / "inputs")
        b = gate.bench_for(inputs, work / stem)
        g = b.file("g.bin", b.assemble(b.frames, 5))
        for port in ((), ("--litespi",)):
            r = b.run(*port, "--slot-b", g, "--boot", "--times", "3000:1000", "--set-pattern", "1",
                      "--until-idle")
            print(f"FIGURE {stem} {'litespi' if port else 'model'} bound run: ok={r.s['ok']} "
                  f"max_call_us={r.s['max_call_us']} step_max={r.s['step_max']} "
                  f"step_bound={r.s['step_bound']}", flush=True)
        rid = max(b.frames)
        plen = len(b.frames[rid]) - 8
        new = bytes((rid * 13 + j * 11 + 29) & 0xFF for j in range(plen)).hex()
        r = b.run("--litespi", "--slot-b", g, "--boot", "--protect-auth", "--set", f"{rid}:{new}",
                  "--until-phase", "4", "--ls-stall", "tx:99999:0:0", "--run-ms", "10000")
        print(f"FIGURE {stem} litespi dead master: failed={r.s['failed']} "
              f"max_call_us={r.s['max_call_us']} calls={r.s['calls']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
