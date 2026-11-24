#!/usr/bin/env python3
"""Build disposable probe trees for the gptp_shadow regression.
Usage: probe_setup.py SOURCE_CLONE HEAD OUT

Each case is a fresh shared clone of SOURCE_CLONE at HEAD with gptp-processor
and verilog-axis at their pins (protocol-processor too, for gptp_tables).
A probe edits files inside its own clone only; the edit is checked to
match exactly once and its diff is written next to the clone.

  head        no edit (control)
  oldpin      gptp-processor checked out at 1616fc8f, the previous pin
  p106-beat   generator: SELF ends in END and BECOME arms the 2 ms
              Announce beat again (the defect FPGA-gPTP #106 repaired)
  p107-gate   engine: PHC word 3 applies only while a slew is active
              (the defect FPGA-gPTP #107 repaired)
  p107-est    generator: BECOME's word-3 low word is the retained rate
              estimate (0 - integrator) instead of rate 0, so the engine
              applies the slave's estimate on every mastership
  p106-nocredit  generator: the Announce leg drops its transmit-credit gate
"""
import re
import subprocess
import sys
from pathlib import Path

src, head, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
GEN = "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
ENG = "gptp-processor/hdl/top/KL_gptp_engine.sv"


def sh(args, cwd):
    subprocess.run([str(a) for a in args], cwd=cwd, check=True)


def edit_in_function(text, func, old, new):
    """Replace `old` exactly once inside Python function `func`."""
    m = re.search(rf"^def {func}\(.*?(?=^def )", text, re.S | re.M)
    assert m, func
    body = m.group(0)
    assert body.count(old) == 1, (func, old, body.count(old))
    return text[:m.start()] + body.replace(old, new, 1) + text[m.end():]


def p106(tree):
    p = tree / GEN
    t = p.read_text()
    t = edit_in_function(t, "prog_self", 'p.emit("BR", label=LB["ANNTX"])', 'p.emit("END")')
    sync = '    p.emit("WRST", ra=RT, imm=RG_TMR | 1, fmt=FMT_Q)  # sync now\n'
    t = edit_in_function(t, "prog_become", sync,
                         sync + '    p.emit("MOVE", rd=RT, ra=0, imm=2)\n'
                                '    p.emit("WRST", ra=RT, imm=RG_TMR | 3, fmt=FMT_Q)  # announce now\n')
    p.write_text(t)


def p107_gate(tree):
    p = tree / ENG
    t = p.read_text()
    old = ("                phc_addend_we_o <= 1'b1;\n"
           "                phc_addend_o    <= st_wdata_w[31:0];\n"
           "                phc_slew_left_r   <= 2'd0;\n")
    assert t.count(old) == 1
    t = t.replace(old, "                if (phc_slew_active_o) begin\n"
                       "                  phc_addend_we_o <= 1'b1;\n"
                       "                  phc_addend_o    <= st_wdata_w[31:0];\n"
                       "                end\n"
                       "                phc_slew_left_r   <= 2'd0;\n")
    p.write_text(t)


def p107_est(tree):
    p = tree / GEN
    t = p.read_text()
    t = edit_in_function(t, "prog_become",
                         'p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_SHL, imm=32)',
                         'p.emit("ALU", rd=RT, ra=R0, rb=RT, cnd=ALU_SUB)')
    p.write_text(t)


def p106_nocredit(tree):
    """generator: the Announce leg sends without its transmit-credit gate,
    so phase 20's withheld credit no longer withholds a master Announce"""
    p = tree / GEN
    t = p.read_text()
    t = edit_in_function(t, "prog_leg_anntx", '    e_credit_gate(p, "skip")\n', "")
    p.write_text(t)


CASES = {"head": None, "oldpin": "oldpin", "p106-beat": p106,
         "p107-gate": p107_gate, "p107-est": p107_est,
         "p106-nocredit": p106_nocredit}
for case in sys.argv[4:] or CASES:
    tree = out / case
    sh(["git", "clone", "--quiet", "--shared", "--no-checkout", src, tree], out)
    sh(["git", "checkout", "--quiet", "--detach", head], tree)
    for sub in ("gptp-processor", "third_party/verilog-axis", "protocol-processor"):
        sh(["git", "config", f"submodule.{sub}.url", src / sub], tree)
        sh(["git", "-c", "protocol.file.allow=always", "submodule", "update",
            "--quiet", "--init", sub], tree)
    action = CASES[case]
    if action == "oldpin":
        sh(["git", "checkout", "--quiet", "1616fc8f"], tree / "gptp-processor")
    elif action:
        action(tree)
    with open(out / f"{case}.probe.diff", "w") as f:
        subprocess.run(["git", "diff"], cwd=tree / "gptp-processor", stdout=f, check=True)
        subprocess.run(["git", "rev-parse", "HEAD"], cwd=tree / "gptp-processor",
                       stdout=f, check=True)
    print(case, "ready", flush=True)
