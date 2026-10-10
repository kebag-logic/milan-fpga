#!/usr/bin/env python3
"""census_yosys_log.py - the census's own elaboration of the tracked datapath, with Yosys's log kept.

census_elab.run() passes ``-q`` to Yosys, so its warnings are not seen. This
probe runs the census's elaborate() unchanged except that the datapath's Yosys
call is given ``-l <log>`` (``-q`` still silences the terminal, the log file
keeps every message), then prints every WARNING line and a summary of the
instance cells whose port connections Yosys resized. Nothing in the checkout
is written.

Usage: census_yosys_log.py <checkout> <log-path>
"""
import re
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    repo, log = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    sys.path.insert(0, str(repo / "sw/mailbox"))
    import census_elab as ce

    real = ce.run

    def run(argv, cwd, what):
        if argv and argv[0] == ce.tool("yosys") and "-p" in argv and "hierarchy -check" in argv[-1]:
            argv = [argv[0], "-l", str(log), *argv[1:]]
        return real(argv, cwd, what)

    ce.run = run
    net = ce.elaborate({})
    text = log.read_text(encoding="utf-8", errors="replace")
    warns = [ln for ln in text.splitlines() if ln.startswith("Warning:")]
    print(f"cells={len(net.cells)} named-nets={len(net.names) - len(net.hidden)} warnings={len(warns)}")
    kinds = Counter(re.sub(r"\d+", "N", w)[:110] for w in warns)
    for k, n in kinds.most_common(40):
        print(f"{n:6d}  {k}")
    resized = [w for w in warns if "esiz" in w or "width" in w.lower()]
    print(f"resize/width warnings: {len(resized)}")
    for w in resized[:60]:
        print("   ", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
