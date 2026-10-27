"""Plant each companion mutant in a scratch milan-fpga clone, one at a time,
run the three parent suites the companion changes, and keep every FAIL line.

usage: companion_mutants.py <parent clone> <out dir> [mutant name ...]
Engine mutants are the lane's own arm entries, taken by name from the
clone's gptp-processor/tb/verilator/engine/mutants.py and planted in its
gptp-processor/hdl. Parent mutants are listed below. Every planted file is
restored with `git checkout --` after its runs.
"""
import importlib.util, os, subprocess, sys
from pathlib import Path

P = Path(sys.argv[1]).resolve(); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
G = P / "gptp-processor"
sys.path.insert(0, str(G / "tb"))
spec = importlib.util.spec_from_file_location("eng", G / "tb/verilator/engine/mutants.py")
eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
ARM = {e[0]: e for e in eng.MUTATIONS}

def engine(name):
    _, fname, pat, rep, _ = ARM[name]
    return name, G / "hdl" / fname, eng.edits_of(pat, rep)

MUTANTS = [
    engine("the path-head refusal restored"),
    engine("the path-count refusal restored"),
    engine("the empty-path refusal restored"),
    engine("the empty sequence published without a TLV"),
    engine("the received head replaced by the grandmaster"),
    engine("(b) the stepsRemoved refusal removed"),
    ("GET_AS_PATH entry 0 served from the grandmaster (the old datapath)",
     P / "hdl/milan/milan_datapath.sv",
     [("  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? gptp_pub_path_head_w\n",
       "  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? cfg_adp_gptp_gm\n")]),
    ("the shadow publishes entry 0 as the grandmaster",
     P / "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv",
     [("        pub_gm_id_o     <= pub_gm_raw_w;\n",
       "        pub_gm_id_o     <= (|pub_path_count_raw_w) ? pub_path_raw_w[63:0]\n"
       "                                                : pub_gm_raw_w;\n")]),
    ("a TLV-less Announce is dropped at the event queue",
     G / "hdl/top/KL_gptp_engine.sv",
     [("                   !ann_event_capture_r;\n",
       "                   (!ann_event_capture_r || !bank_wdata_w[63]);\n")]),
    ("a TLV-less Announce is refused by the parser",
     G / "hdl/wire/KL_gptp_rx_parser.sv",
     [("                          (!pt_seen_r ||\n",
       "                          (pt_seen_r &&\n")]),
    ("the shadow drops entry 0 (the old seven-slot canonicaliser)",
     P / "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv",
     [("        if (4'(pk + 1) <= pub_path_count_next_w)\n",
       "        if ((pk != 0) && (4'(pk + 1) <= pub_path_count_next_w))\n")]),
]
SUITES = [
    ("gptp_shadow", ["make", "-C", "tb/verilator/gptp_shadow", "run"]),
    ("milan_dp_gptp", ["make", "-C", "tb/verilator/milan_dp", "gptp"]),
    ("tsn_fuzz_ptp", ["make", "-C", "tb/verilator/tsn_fuzz", "ptp"]),
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
        tally = [l for l in out.splitlines() if "checks:" in l or " pass, " in l]
        lines.append(f"== {sname}: rc {r.returncode}; " + (tally[-1].strip() if tally else "no tally"))
        lines += fails
    (OUT / f"{tag}.log").write_text("\n".join(lines) + "\n")
    print("done", name, flush=True)
    restore()
print("all done")
