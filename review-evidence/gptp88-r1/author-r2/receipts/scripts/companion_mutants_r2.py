"""Plant each round-2 companion mutant in a scratch milan-fpga clone, one at
a time, run gptp_shadow and the milan_dp gPTP leg, and keep every FAIL line.

usage: companion_mutants_r2.py <parent clone> <out dir> [mutant name ...]
Engine mutants are the lane's own arm entries, taken by name from the
clone's gptp-processor/tb/verilator/engine/mutants.py and planted in its
gptp-processor/hdl. Parent mutants are listed below. Every planted file is
restored with `git checkout --` after its runs.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

P = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
G = P / "gptp-processor"
sys.path.insert(0, str(G / "tb"))
spec = importlib.util.spec_from_file_location(
    "eng", G / "tb/verilator/engine/mutants.py")
eng = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eng)
ARM = {e[0]: e for e in eng.MUTATIONS}


def engine(name):
    _, fname, pat, rep, _ = ARM[name]
    return name, G / "hdl" / fname, eng.edits_of(pat, rep)


SHADOW = P / "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
DP = P / "hdl/milan/milan_datapath.sv"
MUTANTS = [
    # C2: the 0x7E4 generation watches entries 1..7 only
    ("C2 the shadow path generation compares entries 1..7 only", SHADOW,
     [("      || (pub_path_next_w != pub_path_o);\n",
       "      || (pub_path_next_w[8*64-1:64] != pub_path_o[8*64-1:64]);\n")]),
    # C3: the Table 5.22 AS_PATH comparator loses its entry-0 term
    ("C3 the AS_PATH comparator drops its entry-0 term", DP,
     [("                    && ((asp_live_head_w != gsi_asp_head_q_r)\n"
       "                        || (asp_live_count_w != gsi_asp_count_q_r)\n",
       "                    && ((asp_live_count_w != gsi_asp_count_q_r)\n")]),
    ("GET_AS_PATH entry 0 served from the grandmaster (the old datapath)", DP,
     [("  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? gptp_pub_path_head_w\n",
       "  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? cfg_adp_gptp_gm\n")]),
    ("the shadow drops entry 0 (the old seven-slot canonicaliser)", SHADOW,
     [("        if (4'(pk + 1) <= pub_path_count_next_w)\n",
       "        if ((pk != 0) && (4'(pk + 1) <= pub_path_count_next_w))\n")]),
    ("the shadow drops entry 1", SHADOW,
     [("        if (4'(pk + 1) <= pub_path_count_next_w)\n",
       "        if ((pk != 1) && (4'(pk + 1) <= pub_path_count_next_w))\n")]),
    engine("the received path is published without thisClock"),
    engine("thisClock lands one slot early"),
    engine("the appended entry is the announcing source"),
    engine("the received head replaced by the grandmaster"),
]
SUITES = [
    ("gptp_shadow", ["make", "-C", "tb/verilator/gptp_shadow", "run"]),
    ("milan_dp_gptp", ["make", "-C", "tb/verilator/milan_dp", "gptp"]),
]


def restore():
    subprocess.run(["git", "checkout", "--", "."], cwd=G, check=True)
    subprocess.run(["git", "checkout", "--", "hdl", "tb"], cwd=P, check=True)


restore()
WANT = sys.argv[3:]
for name, path, edits in MUTANTS:
    if WANT and name not in WANT:
        continue
    text = path.read_text()
    for pat, rep in edits:
        assert text.count(pat) == 1, (name, pat[:80])
        text = text.replace(pat, rep)
    path.write_text(text)
    tag = "".join(c if c.isalnum() else "_" for c in name)[:60]
    lines = [f"mutant: {name}", f"planted in: {path.relative_to(P)}"]
    for sname, cmd in SUITES:
        r = subprocess.run(cmd, cwd=P, capture_output=True, text=True)
        out = r.stdout + r.stderr
        fails = [l.strip() for l in out.splitlines()
                 if l.startswith("FAIL ") or l.lstrip().startswith("[FAIL]")]
        tally = [l for l in out.splitlines() if "checks:" in l]
        lines.append(f"== {sname}: rc {r.returncode}; "
                     + (tally[-1].strip() if tally else "no tally"))
        lines += fails
    (OUT / f"{tag}.log").write_text("\n".join(lines) + "\n")
    print("done", name, flush=True)
    restore()
print("all done")
