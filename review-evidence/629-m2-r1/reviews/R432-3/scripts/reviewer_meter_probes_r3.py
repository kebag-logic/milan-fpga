#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""[R432] round-3 probes of the largest deviation's level (PR #634, head 0b066b6e).

Defects in max_dev_ns_o that the round-3 M1 checks claim to grade, none of them
one of the three named mutants already in tb/verilator/aaf_clock_meter/mutants.py.
Each probe is exact source replacements (every anchor exactly once) on a scratch
copy of KL_aaf_clock_meter.sv; the checkout is never edited. Built with the
meter suite's own `make build` recipe and run on case `rates` (M1).
  CAUGHT  - build ok, exit 1, RESULT: FAIL (failing checks printed)
  ESCAPED - build ok, exit 0, RESULT: PASS
  INVALID - anchor missing/duplicated, build failure, or neither verdict
Usage: reviewer_meter_probes_r3.py <repo> <scratch-dir> [jobs]
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CLR = "        mr_toggle_p_o <= 1'b0;\n        max_dev_r     <= '0;\n"
PROBES = (
    ("Q0_clean_control", ()),
    # a data-caused history restart clears the reading (the design keeps it)
    ("Q1_data_restart_clears",
     (("        restart_cnt_r <= restart_cnt_r + 8'd1;\n",
       "        restart_cnt_r <= restart_cnt_r + 8'd1;\n        max_dev_r     <= '0;\n"),)),
    # saturation threshold one above the field's maximum
    ("Q2_saturation_off_by_one",
     (("if (s2_abs_w > 32'd65535)", "if (s2_abs_w > 32'd65536)"),)),
    # only selection changes and exit clear it; the bind edge and the timeout do not
    ("Q3_clear_only_on_selection",
     ((CLR, "        mr_toggle_p_o <= 1'b0;\n"
            "        if (en_rise_w || idx_chg_w || !en_w) max_dev_r <= '0;\n"),)),
    # the timeout does not clear it (bind edge, selection and exit still do)
    ("Q4_timeout_keeps",
     ((CLR, "        mr_toggle_p_o <= 1'b0;\n"
            "        if (!tout_fire_w) max_dev_r <= '0;\n"),)),
    # the bind edge does not clear it
    ("Q5_bind_edge_keeps",
     ((CLR, "        mr_toggle_p_o <= 1'b0;\n"
            "        if (!bind_rise_w) max_dev_r <= '0;\n"),)),
    # exit (en low) does not hold it at zero; the entry edge still clears it
    ("Q6_not_zero_while_not_following",
     ((CLR, "        mr_toggle_p_o <= 1'b0;\n"
            "        if (en_w) max_dev_r <= '0;\n"),)),
    # the reading is a signed truncation, not |deviation| (negative steps)
    ("Q7_signed_not_abs",
     (("else if (16'(s2_abs_w) > max_dev_r)  max_dev_r <= 16'(s2_abs_w);",
       "else if (16'(s2_dev_r) > max_dev_r)  max_dev_r <= 16'(s2_dev_r);"),
      ("if (s2_abs_w > 32'd65535)", "if (s2_dev_r > 32'sd65535)"))),
)


def run(repo: Path, work: Path, name: str, edits) -> tuple[str, str, str]:
    """Plant one probe, build it, run M1; return (name, verdict, detail)."""
    src = (repo / "hdl/ieee1722/crf/KL_aaf_clock_meter.sv").read_text()
    for anchor, new in edits:
        if src.count(anchor) != 1:
            return name, "INVALID", f"anchor x{src.count(anchor)}: {anchor!r}"
        src = src.replace(anchor, new)
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    rtl = d / "KL_aaf_clock_meter.sv"
    rtl.write_text(src)
    b = subprocess.run(["make", "-s", "-C", str(repo / "tb/verilator/aaf_clock_meter"),
                        "build", f"METER_RTL={rtl}", f"MDIR={d}/obj",
                        f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}",
                        f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '2')}"],
                       capture_output=True, text=True, check=False)
    if b.returncode:
        return name, "INVALID", "build failed: " + b.stderr[-1500:]
    r = subprocess.run([str(d / "obj/Vmeter_sim"), "rates"], capture_output=True,
                       text=True, check=False,
                       cwd=str(repo / "tb/verilator/aaf_clock_meter"))
    out = r.stdout + r.stderr
    (d / "run.log").write_text(out)
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
    if r.returncode == 0 and "RESULT: PASS" in out:
        verdict = "PASS(clean)" if not edits else "ESCAPED"
    elif r.returncode == 1 and "RESULT: FAIL" in out and fails:
        verdict = "UNEXPECTED-FAIL" if not edits else "CAUGHT"
    else:
        verdict = f"INVALID(rc={r.returncode})"
    return name, verdict, "\n".join(fails[:8])


def main() -> int:
    repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = [ex.submit(run, repo, work, n, e) for n, e in PROBES]
        for f in futs:
            name, verdict, detail = f.result()
            print(f"{verdict:16s} {name}")
            if detail:
                print("    " + detail.replace("\n", "\n    "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
