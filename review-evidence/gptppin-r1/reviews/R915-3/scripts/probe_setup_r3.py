#!/usr/bin/env python3
"""Build disposable probe trees for the gptp_shadow regression, round 3.
Usage: probe_setup_r3.py SOURCE_CLONE HEAD OUT [CASE...]

Each case is a fresh shared clone of SOURCE_CLONE at HEAD with gptp-processor
and verilog-axis at their pins. A probe edits files inside its own clone
only; each edit must match exactly once, and its diff is written next to
the clone (superproject and gptp-processor).

  head            no edit (control)
  order-stall     harness: the wide lane's ready input held low from before
                  the race's takeover until the queued Announce has been
                  injected (the stall hunk of the external reviewer's
                  round-2 order probe, verbatim)
  order-stall-short  harness: the same race, but the lane is held only
                  from the queued Announce's injection to 2 ms after it,
                  so a stall that starts AFTER the takeover is also graded
  p106-nocredit   generator: the Announce leg drops its transmit-credit
                  gate (this reviewer's round-2 probe, verbatim)
"""
import re
import subprocess
import sys
from pathlib import Path

src, head, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
GEN = "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
SIM = "tb/verilator/gptp_shadow/sim_main.cpp"
RACE = ("        run_to(t0 + a1_after);\n"
        "        announce(tk_seq++, 100, GMID, PEER_CID, 0x00);\n")


def sh(args, cwd):
    subprocess.run([str(a) for a in args], cwd=cwd, check=True)


def once(path, old, new):
    t = path.read_text()
    assert t.count(old) == 1, (path, t.count(old))
    path.write_text(t.replace(old, new, 1))


def edit_in_function(text, func, old, new):
    m = re.search(rf"^def {func}\(.*?(?=^def )", text, re.S | re.M)
    assert m, func
    body = m.group(0)
    assert body.count(old) == 1, (func, old, body.count(old))
    return text[:m.start()] + body.replace(old, new, 1) + text[m.end():]


def order_stall(tree):
    once(tree / SIM, RACE, "        dut->tx_tready_i = 0;\n" + RACE +
         "        dut->tx_tready_i = 1;\n")


def order_stall_short(tree):
    once(tree / SIM, RACE, "        run_to(t0 + a1_after);\n"
         "        dut->tx_tready_i = 0;\n"
         "        announce(tk_seq++, 100, GMID, PEER_CID, 0x00);\n"
         "        run_to(cyc + 2 * kMsTicks);\n"
         "        dut->tx_tready_i = 1;\n")


def p106_nocredit(tree):
    p = tree / GEN
    p.write_text(edit_in_function(p.read_text(), "prog_leg_anntx",
                                  '    e_credit_gate(p, "skip")\n', ""))


CASES = {"head": None, "order-stall": order_stall,
         "order-stall-short": order_stall_short, "p106-nocredit": p106_nocredit}
for case in sys.argv[4:] or CASES:
    tree = out / case
    sh(["git", "clone", "--quiet", "--shared", "--no-checkout", src, tree], out)
    sh(["git", "checkout", "--quiet", "--detach", head], tree)
    for sub in ("gptp-processor", "third_party/verilog-axis"):
        sh(["git", "config", f"submodule.{sub}.url", src / sub], tree)
        sh(["git", "-c", "protocol.file.allow=always", "submodule", "update",
            "--quiet", "--init", sub], tree)
    if CASES[case]:
        CASES[case](tree)
    with open(out / f"{case}.probe.diff", "w") as f:
        subprocess.run(["git", "diff"], cwd=tree, stdout=f, check=True)
        subprocess.run(["git", "diff"], cwd=tree / "gptp-processor", stdout=f, check=True)
        subprocess.run(["git", "rev-parse", "HEAD"], cwd=tree / "gptp-processor",
                       stdout=f, check=True)
    print(case, "ready", flush=True)
