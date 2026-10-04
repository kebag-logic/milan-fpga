#!/usr/bin/env python3
"""Reviewer fault probes for KL_crf_rx's #653 unbind arm, graded by the crf_rx unit suite.

Usage: crf_probes.py TREE OUTDIR [N ...]
TREE is a disposable checkout at the head under review; each probe writes a
mutated copy of KL_crf_rx.sv under OUTDIR, copies tb/verilator/crf_rx to a
sibling directory (same depth, so the Makefile's relative RTL_DIR holds),
builds the unit target against the mutant and records which checks fail.
A probe is CAUGHT when the unit run reports failures and every expected
check id appears on a [FAIL] line. Nothing in TREE's tracked files is edited.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ARM = ("      if (w_bind_fall_w && locked_o) begin\n"
       "        locked_o       <= 1'b0;\n"
       "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n"
       "        dirty_p_o      <= 1'b1;\n"
       "      end\n")
TOUT = ("        if (locked_o) begin\n"
        "          locked_o       <= 1'b0;\n"
        "          cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n")

PROBES = [
    ("P1 arm deleted (dev behaviour)", ARM, "",
     ["[UNB-a1]", "[UNB-a2]", "[5t-g3b]"]),
    ("P2 arm without the locked_o guard (an unlocked input's unbind counts)",
     "      if (w_bind_fall_w && locked_o) begin\n",
     "      if (w_bind_fall_w) begin\n", ["[UNB-c1]"]),
    ("P3 arm arms no Table 5.22 pulse",
     ARM, ARM.replace("        dirty_p_o      <= 1'b1;\n", ""), ["[UNB-a5]"]),
    ("P4 arm keeps the lock (timeout recounts)",
     ARM, ARM.replace("        locked_o       <= 1'b0;\n", ""), ["[UNB-a1]", "[UNB-b1]"]),
    ("P5 arm counts two unlocks",
     ARM, ARM.replace("cnt_unlocked_o + 32'd1", "cnt_unlocked_o + 32'd2"), ["[UNB-a2]"]),
    ("P6 arm also counts STREAM_INTERRUPTED",
     ARM, ARM.replace("      end\n", "        cnt_intr_o <= cnt_intr_o + 32'd1;\n      end\n"),
     ["[UNB-a6]"]),
    ("P7 timeout counts without the lock guard (double count after unbind)",
     TOUT, TOUT.replace("        if (locked_o) begin\n", "        if (1'b1) begin\n"),
     ["[UNB-b1]"]),
    ("P8 arm placed after the bind-rise wipe (ordering; expected equivalent)",
     None, None, []),
]


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    picks = [int(a) for a in sys.argv[3:]] or list(range(1, len(PROBES) + 1))
    rtl = (tree / "hdl/ieee1722/crf/KL_crf_rx.sv").read_text()
    out.mkdir(parents=True, exist_ok=True)
    rc = 0
    for n in picks:
        name, pat, rep, expect = PROBES[n - 1]
        if pat is None:
            # move the arm below the bind-rise block (just before "    end\n  end : engine")
            if rtl.count(ARM) != 1:
                print(f"[ERR] {name}: arm pattern count {rtl.count(ARM)}"); rc = 1; continue
            body = rtl.replace(ARM, "")
            anchor = "        dirty_p_o <= 1'b1;\n      end\n    end\n  end : engine"
            if body.count(anchor) != 1:
                print(f"[ERR] {name}: anchor count {body.count(anchor)}"); rc = 1; continue
            mut = body.replace(anchor, "        dirty_p_o <= 1'b1;\n      end\n" + ARM +
                               "    end\n  end : engine")
        else:
            if rtl.count(pat) != 1:
                print(f"[ERR] {name}: pattern count {rtl.count(pat)}"); rc = 1; continue
            mut = rtl.replace(pat, rep)
        src = out / f"KL_crf_rx_P{n}.sv"
        src.write_text(mut)
        tb = tree / f"tb/verilator/crf_rx_P{n}"
        if not tb.exists():
            shutil.copytree(tree / "tb/verilator/crf_rx", tb,
                            ignore=shutil.ignore_patterns("obj_*"))
        r = subprocess.run(["make", "-s", "unit", f"RX_RTL={src}"], cwd=tb,
                           capture_output=True, text=True, check=False)
        log = r.stdout + r.stderr
        (out / f"P{n}.log").write_text(log)
        tally = re.findall(r"KL_crf_rx: (\d+) checks, (\d+) failures", log)
        fails = [l for l in log.splitlines() if "[FAIL]" in l or "FAIL" in l[:8]]
        missing = [e for e in expect if not any(e in l for l in fails)]
        if expect:
            verdict = "CAUGHT" if tally and int(tally[-1][1]) > 0 and not missing else "SURVIVED/UNATTRIBUTED"
        else:
            verdict = "EQUIVALENT(pass)" if tally and int(tally[-1][1]) == 0 else "DIFFERS"
        print(f"{verdict}: {name}; make rc={r.returncode}; tally={tally[-1] if tally else None}; "
              f"expected ids missing={missing}; failing ids="
              f"{sorted(set(re.findall(r'\[[A-Za-z0-9-]+\]', ' '.join(fails))))[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
