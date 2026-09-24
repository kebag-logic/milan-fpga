#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R302-3 probes for the U13 PI-resume check (round-3 item R303-2 S1).

Usage: VERILATOR=<5.050> resume_probes.py <clone> <scratch> <out-dir>
Builds the servo unit harness (tb/verilator/mmcm_servo, sim_main.cpp) from
`git archive` trees in <scratch>; the clone is only read. Rows:
  head/clean          head harness, head servo            expect PASS
  head/never_resumes  head harness, shipped mutant        expect FAIL on the resume check only
  prior/never_resumes d04a6167 harness, shipped mutant    expect PASS (the old U13 cannot see it)
  head/no_offset      head harness with the +90 ppm offset replaced by the clean rate,
                      head servo: ripple alone must NOT satisfy the check -> expect FAIL
  head/instrumented   head harness printing trim before/after the offset -> margin
  head/resume_on_idle_only  PI latched off after invalidity until CRF is
                      deselected (a second non-resume shape) -> expect FAIL
The mutant text is taken from the shipped mutants.py construction.
"""
import os, re, subprocess, sys
from pathlib import Path

HEAD = "0c61d458941088f3847513b7c6fe6589c75b4270"
PRIOR = "d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1"
ANCHOR = "\n                           && crf_rate_valid_i;"
RESUME_ANCHOR = "  always_ff @(posedge clk_i) begin : servo_engine"
LATCH = """  logic invalid_seen_r;
  always_ff @(posedge clk_i) begin : latch_invalid_sample
    if (!rst_n) invalid_seen_r <= 1'b0;
    else if (!crf_rate_valid_i) invalid_seen_r <= 1'b1;
  end
"""

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def tree(clone, rev, dst):
    if not dst.exists():
        dst.mkdir(parents=True)
        a = subprocess.Popen(["git", "-C", clone, "archive", rev], stdout=subprocess.PIPE)
        subprocess.run(["tar", "-x", "-C", str(dst)], stdin=a.stdout, check=True)
        assert a.wait() == 0
    return dst

def never_resumes(servo):
    assert servo.count(ANCHOR) == 1 and servo.count(RESUME_ANCHOR) == 1
    s = servo.replace(RESUME_ANCHOR, LATCH + RESUME_ANCHOR)
    return s.replace(ANCHOR, ANCHOR[:-1] + " && !invalid_seen_r;")

def run(root, name, harness_edit, servo_text, out):
    d = root / "tb/verilator" / f"mmcm_servo_{name}"
    if d.exists():
        subprocess.run(["rm", "-rf", str(d)], check=True)
    subprocess.run(["cp", "-r", str(root / "tb/verilator/mmcm_servo"), str(d)], check=True)
    sm = d / "sim_main.cpp"
    txt = sm.read_text()
    if harness_edit:
        txt = harness_edit(txt)
    sm.write_text(txt)
    rtl = d / "servo_probe.sv"
    rtl.write_text(servo_text)
    b = sh(["make", "-s", "-C", str(d), "unit-build", f"SERVO_RTL={rtl}",
            "UNIT_MDIR=obj_probe", f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}"])
    if b.returncode:
        (out / f"{name}.log").write_text(b.stdout[-3000:] + b.stderr[-3000:])
        return "BUILD_FAIL", []
    r = sh([str(d / "obj_probe/Vservo_sim")], timeout=1200)
    log = r.stdout + r.stderr
    (out / f"{name}.log").write_text(log)
    fails = re.findall(r"\[FAIL\][^\n]*|\[ *FAIL *\][^\n]*", log)
    tot = re.search(r"KL_mmcm_drp_servo: (\d+) checks, (\d+) failures", log)
    return ("rc=%d %s" % (r.returncode, tot.group(0) if tot else "no-total")), fails

def main():
    clone, scratch, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    h = tree(clone, HEAD, scratch / "rp-head")
    p = tree(clone, PRIOR, scratch / "rp-prior")
    servo_h = (h / "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv").read_text()
    servo_p = (p / "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv").read_text()
    assert servo_h == servo_p, "servo differs between heads"
    off = "dut->crf_rate_i = rate_for_ppm(+90.0);"
    def no_offset(t):
        assert t.count(off) == 1
        return t.replace(off, "dut->crf_rate_i = clean;")
    def instr(t):
        chk = 'ck("[U13] valid offset resumes PI trim"'
        assert t.count(chk) == 1
        return t.replace(chk, 'printf("  probe: U13 trim resumed=%d after=%d delta=%d need>80\\n",'
                         ' (int)resumed, (int)trim(), (int)trim() - (int)resumed);\n        ' + chk)
    # Variant: PI stays off until CRF deselection (never, in U13).
    slow = never_resumes(servo_h).replace(
        "else if (!crf_rate_valid_i) invalid_seen_r <= 1'b1;",
        "else if (!crf_rate_valid_i) invalid_seen_r <= 1'b1;\n    else if (!servo_sel_w) invalid_seen_r <= 1'b0;")
    rows = [
        ("head_clean", h, None, servo_h, "PASS"),
        ("head_never_resumes", h, None, never_resumes(servo_h), "FAIL:[U13] valid offset resumes PI trim"),
        ("prior_never_resumes", p, None, never_resumes(servo_p), "PASS"),
        ("head_no_offset", h, no_offset, servo_h, "FAIL:[U13] valid offset resumes PI trim"),
        ("head_instrumented", h, instr, servo_h, "PASS"),
        ("head_resume_on_idle_only", h, None, slow, "FAIL:[U13] valid offset resumes PI trim"),
    ]
    ok = True
    lines = []
    for name, root, edit, servo, expect in rows:
        res, fails = run(root, name, edit, servo, out)
        if expect == "PASS":
            good = res.startswith("rc=0") and "0 failures" in res
        else:
            want = expect.split(":", 1)[1]
            good = res.startswith("rc=1") and any(want in f for f in fails)
        ok &= good
        lines.append(f"{'OK ' if good else 'BAD'} {name}: expect {expect}; got {res}; fails={len(fails)}")
        for f in fails:
            lines.append(f"      {f.strip()}")
    lines.append("overall: " + ("PASS" if ok else "FAIL"))
    (out / "SUMMARY.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
