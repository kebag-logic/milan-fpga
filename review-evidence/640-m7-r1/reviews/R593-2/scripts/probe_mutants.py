#!/usr/bin/env python3
"""Reviewer mutation probes (R593-2) beyond the suite's own controls.

Usage: python3 -I probe_mutants.py <exact-head tree copy> <work dir> <verilator> <out dir>

Each probe copies the minimal source set of the exact-head tree into its
own work directory, plants one defect (exactly-once anchor), and runs
`make run` in tb/verilator/gptp_tables, and for the probes marked so, also
in tb/verilator/gptp_shadow and tb/verilator/gptp_txts (gptp_txts is run
only when its generated chain inputs are present). Up to 8 builds run at
once. Each run's log and rc go to <out dir>/<probe>.<suite>.{log,rc}. The
script reports, per probe and suite, whether the run's tally showed
failures and which named checks failed. It never edits the source tree.
"""
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

TREE, WORK, VERILATOR, OUT = (Path(a) for a in sys.argv[1:5])
SHADOW = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
RET = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
TIMER = "gptp-processor/hdl/common/KL_gptp_timer.sv"
COPY = ["hdl", "gptp-processor/hdl", "third_party/verilog-axis/rtl",
        "tb/verilator/gptp_tables", "tb/verilator/gptp_shadow",
        "tb/verilator/gptp_txts", "tb/common", "scripts", "sw/litex"]

#: (name, file, old, new, suites)
PROBES = [
    ("baseline", None, None, None, ("gptp_tables",)),
    ("rx_fifo_deeper", SHADOW,
     "    .DEPTH               (RX_FIFO_BEATS_C),",
     "    .DEPTH               (RX_FIFO_BEATS_C * 2),", ("gptp_tables",)),
    ("results_seq_write_index", RET,
     "      res_seq_r [res_tail_w] <= led_head_seq_w;",
     "      res_seq_r [res_head_r] <= led_head_seq_w;", ("gptp_tables",)),
    ("ledger_type_write_index", RET,
     "      led_type_r[led_tail_w] <= alloc_type_i;",
     "      led_type_r[led_head_r] <= alloc_type_i;", ("gptp_tables",)),
    ("timer_write_alias", TIMER,
     "      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
     "      deadline_r[{1'b0, arm_slot_i[SW_C-2:0]}] <= ms_now_r + arm_delta_ms_i;",
     ("gptp_tables",)),
    ("results_ok_stuck1", RET,
     "      res_ok_r  [res_tail_w] <= res_ok_w;",
     "      res_ok_r  [res_tail_w] <= 1'b1;", ("gptp_tables", "gptp_shadow")),
    ("results_gen_stuck", RET,
     "      res_gen_r [res_tail_w] <= gen_r;",
     "      res_gen_r [res_tail_w] <= TXTS_GEN_W_P'(1);", ("gptp_tables", "gptp_shadow")),
    ("ledger_tag_stuck1", RET,
     "      led_tag_r [led_tail_w] <= alloc_tagged_i;",
     "      led_tag_r [led_tail_w] <= 1'b1;", ("gptp_tables", "gptp_shadow")),
]

TALLY = re.compile(r"^== (\S+): checks: (\d+) +failures: (\d+) ==", re.M)


def prepare(name, rel, old, new):
    root = WORK / name
    if root.exists():
        shutil.rmtree(root)
    for c in COPY:
        src = TREE / c
        if src.exists():
            shutil.copytree(src, root / c, symlinks=True,
                            ignore=shutil.ignore_patterns("obj_dir", "gptp_ucode.hex"))
    if rel:
        p = root / rel
        text = p.read_text()
        assert text.count(old) == 1, (name, old)
        p.write_text(text.replace(old, new, 1))
    return root


def run(name, root, suite):
    log = OUT / f"{name}.{suite}.log"
    with open(log, "w") as fh:
        rc = subprocess.run(["make", "-s", "run", f"VERILATOR={VERILATOR}",
                             "VERILATOR_JOBS=2"],
                            cwd=root / "tb/verilator" / suite, stdout=fh,
                            stderr=subprocess.STDOUT).returncode
    (OUT / f"{name}.{suite}.rc").write_text(f"{rc}\n")
    text = log.read_text(errors="replace")
    t = TALLY.search(text)
    fails = sorted({l.strip()[7:].split("  got=")[0].strip()
                    for l in text.splitlines() if l.strip().startswith("[FAIL] ")})
    return name, suite, rc, (t.group(2), t.group(3)) if t else None, fails


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for name, rel, old, new, suites in PROBES:
        root = prepare(name, rel, old, new)
        for s in suites:
            jobs.append((name, root, s))
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda j: run(*j), jobs))
    for name, suite, rc, tally, fails in results:
        verdict = ("NO TALLY" if tally is None else
                   ("CAUGHT" if int(tally[1]) else "SURVIVED"))
        print(f"{name:26s} {suite:12s} rc={rc} tally={tally} {verdict} {fails[:4]}")


if __name__ == "__main__":
    main()
