"""Plant each merge-round companion mutant or control in a scratch milan-fpga
clone, one at a time, run the suites it names, and keep every FAIL line.

usage: companion_mutants_r3.py <parent clone> <out dir> <tsn-gen root> [name ...]
Engine mutants are the lane's own arm entries, taken by name from the
clone's gptp-processor/tb/verilator/engine/mutants.py and planted in its
gptp-processor/hdl. Parent mutants and controls are listed below. Every
planted file is restored with `git checkout --` after its runs.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

P = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
TSN_GEN = sys.argv[3]
OUT.mkdir(parents=True, exist_ok=True)
G = P / "gptp-processor"
sys.path.insert(0, str(G / "tb"))
spec = importlib.util.spec_from_file_location(
    "eng", G / "tb/verilator/engine/mutants.py")
eng = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eng)
ARM = {e[0]: e for e in eng.MUTATIONS}


def engine(name, suites):
    _, fname, pat, rep, _ = ARM[name]
    return name, G / "hdl" / fname, eng.edits_of(pat, rep), suites


DP = P / "hdl/milan/milan_datapath.sv"
ENG = G / "hdl/top/KL_gptp_engine.sv"
SIM = P / "tb/verilator/milan_dp/sim_gptp.cpp"
FUZZ = P / "tb/verilator/tsn_fuzz/fuzz_ptp_timing.py"
HOLD = ("      for (int n = 0; n < 400; n++) {     // s2's event arrives against"
        " full\n        *eng = 4; dut->eval();\n        run(dut, 1);\n      }\n")
ONCE = "      run(dut, 400);                      // s2's event arrives against full\n"
MUTANTS = [
    # K1 control: the round-2 #207 arm, its level poked once, on this stack
    ("K1 the #207 arm pokes the full level once (the round-2 arm)", SIM,
     [(HOLD, ONCE)], ["milan_dp_gptp"]),
    # K2: the engine stops counting a full-queue refusal
    ("K2 a full-queue refusal is not counted", ENG,
     [("      if (pev_valid_w && (evq_full_w || ann_reject_w))\n",
       "      if (pev_valid_w && ann_reject_w)\n")], ["milan_dp_gptp"]),
    # K3 control: the BTCA adoptions without the pair heard as master
    ("K3 the BTCA adoptions send no Sync pair first", FUZZ,
     [("        self.become_gm()\n        self._sync_pair(0)\n"
       "        kw.setdefault(\"gm_identity\", 0x2222)\n",
       "        self.become_gm()\n"
       "        kw.setdefault(\"gm_identity\", 0x2222)\n")], ["tsn_fuzz"]),
    engine("the path-head refusal restored", ["tsn_fuzz"]),
    engine("the path-count refusal restored", ["tsn_fuzz"]),
    # K6 control: the end-of-leg probes without the pair that clears ageing
    ("K6 the served-head probe sends no Sync pair first", SIM,
     [("    run_selected(dut, 20000);\n"
       "    announce(dut, 0x710B,",
       "    announce(dut, 0x710B,")], ["milan_dp_gptp"]),
    ("GET_AS_PATH entry 0 served from the grandmaster (the old datapath)", DP,
     [("  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? gptp_pub_path_head_w\n",
       "  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? cfg_adp_gptp_gm\n")],
     ["milan_dp_gptp"]),
    ("C3 the AS_PATH comparator drops its entry-0 term", DP,
     [("                    && ((asp_live_head_w != gsi_asp_head_q_r)\n"
       "                        || (asp_live_count_w != gsi_asp_count_q_r)\n",
       "                    && ((asp_live_count_w != gsi_asp_count_q_r)\n")],
     ["milan_dp_gptp"]),
    engine("a TLV-less Announce publishes {thisClock}", ["milan_dp_gptp"]),
]
SUITES = {
    "milan_dp_gptp": ["make", "-C", "tb/verilator/milan_dp", "gptp"],
    "tsn_fuzz": ["make", "-C", "tb/verilator/tsn_fuzz", "ptp"],
}


def restore():
    subprocess.run(["git", "checkout", "--", "."], cwd=G, check=True)
    subprocess.run(["git", "checkout", "--", "hdl", "tb"], cwd=P, check=True)


restore()
WANT = sys.argv[4:]
env = dict(os.environ, TSN_GEN_ROOT=TSN_GEN)
for name, path, edits, suites in MUTANTS:
    if WANT and name not in WANT:
        continue
    text = path.read_text()
    for pat, rep in edits:
        assert text.count(pat) == 1, (name, pat[:80])
        text = text.replace(pat, rep)
    path.write_text(text)
    tag = "".join(c if c.isalnum() else "_" for c in name)[:60]
    lines = [f"mutant: {name}", f"planted in: {path.relative_to(P)}"]
    for suite in suites:
        r = subprocess.run(SUITES[suite], cwd=P, env=env, capture_output=True,
                           text=True)
        out = r.stdout + r.stderr
        fails = [ln for ln in out.splitlines()
                 if ln.startswith("FAIL ") or ln.startswith("  BTCA")
                 or " fail, " in ln]
        tally = [ln for ln in out.splitlines()
                 if " checks: " in ln or "field campaign" in ln]
        lines.append(f"{suite}: rc {r.returncode}; "
                     + (tally[-1].strip() if tally else "no tally"))
        lines += fails
    (OUT / f"{tag}.log").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:3]), flush=True)
    restore()
