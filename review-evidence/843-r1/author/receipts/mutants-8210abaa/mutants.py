#!/usr/bin/env python3
"""#843 planted mutants: each plants one defect in a clean clone, runs the named check, records rc, the
check's failing lines and whether every expected failing phrase appears; then restores the clone.
usage: mutants.py <clone> <outdir> [<name>...]"""
import json, os, subprocess, sys, time
from pathlib import Path

ENV = dict(os.environ, PATH="<data>/tools/pinned-verilator-5.050:<data>/tools/sv2v-v0.0.12:<home>/.local/bin:/usr/local/bin:/usr/bin:/bin",
           VERILATOR="<data>/tools/pinned-verilator-5.050/verilator", MAKEFLAGS="-j4 --no-print-directory")
B = "sw/builder/endstation_builder.py"
G26 = ["python3", "sw/builder/test_builder.py", "--gates", "test_gptp_dataset_matches_engine_announce,test_gptp_clock_accuracy_per_board"]
G1B = ["python3", "sw/builder/test_builder.py", "--gates", "test_baremetal_profile_contract"]
LAT = ["make", "-C", "tb/verilator/milan_dp", "gptp-lat"]
LEG = ["make", "-C", "tb/verilator/milan_dp", "gptp"]
MUTANTS = [
    ("MB1 the builder passes the generator default 0x22 for every config", B,
     "\"--clock-accuracy\", f\"0x{cfg['gptp']['clock_accuracy']:02X}\"]", "\"--clock-accuracy\", \"0x22\"]",
     [("gate 26c", G26, ["gate 26c: arty_current passes --clock-accuracy 0x22, its board decided 0xFE"]),
      ("milan_dp gptp-lat", LAT, ["FAIL [CA] every DUT Announce carries the config's clockAccuracy"]),
      ("gate 1b", G1B, ["clockAccuracy: mutation did not reach gptp_ucode.hex"])]),
    ("MB2 the builder passes no --clock-accuracy", B,
     ",\n            \"--clock-accuracy\", f\"0x{cfg['gptp']['clock_accuracy']:02X}\"]", "]",
     [("gate 26c", G26, ["carry no --clock-accuracy"])]),
    ("MB3 an omitted gptp.clock_accuracy resolves to 0x22", B,
     "GPTP_CLOCK_ACCURACY_UNKNOWN = 0xFE", "GPTP_CLOCK_ACCURACY_UNKNOWN = 0x22",
     [("gate 26b", G26, ["omitted gptp.clock_accuracy resolved to 0x22, 802.1AS-2011 8.6.2.3 b) says 0xFE"])]),
    ("MB4 any octet is accepted", B,
     "    if v not in GPTP_CLOCK_ACCURACY_VALUES:", "    if not 0 <= v <= 0xFF:",
     [("gate 26c", G26, ["gate 26c: gptp.clock_accuracy 0x0 was ACCEPTED"])]),
    ("MB5 the descriptor takes the engine default, not the config", B,
     "            clock_accuracy=_gptp_clock_accuracy_key(gp_raw),", "            clock_accuracy=0x22,",
     [("gate 26b", G26, ["arty_4x4: gptp.clock_accuracy 0x22, the board's decided value is 0xFE (#843)"])]),
    ("MH1 gptp_shadow's OUR_CQ is the old literal", "tb/verilator/gptp_shadow/Makefile",
     "-DOUR_CQ_TB=$(OUR_CQ)", "-DOUR_CQ_TB=0xF8FE436A",
     [("gptp_shadow run", ["make", "-C", "tb/verilator/gptp_shadow", "run"], ["FAIL as master: every Announce carries this image's clockQuality"])]),
    ("MH2 gptp_plane's OUR_CQ is the old literal", "tb/verilator/gptp_plane/Makefile",
     "-DOUR_CQ_TB=$(OUR_CQ)", "-DOUR_CQ_TB=0xF8FE436A",
     [("gptp_plane run", ["make", "-C", "tb/verilator/gptp_plane", "run"], ["FAIL grandmaster Announce carries this image's clockQuality"])]),
    ("ML1 the gptp leg runs the Arty image while expecting the AX7101's 0x22", "tb/verilator/milan_dp/Makefile",
     "GPTP_LEG_CONFIG = ../../../configs/endstation_ax7101_1x1_tdm8.yaml", "GPTP_LEG_CONFIG = ../../../configs/endstation_arty_current.yaml",
     [("milan_dp gptp", LEG, ["FAIL [CA] every DUT Announce carries the config's clockAccuracy"])]),
]

def main():
    clone, out = Path(sys.argv[1]), Path(sys.argv[2])
    want = set(sys.argv[3:])
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, path, old, new, checks in MUTANTS:
        tag = name.split()[0]
        if want and tag not in want:
            continue
        f = clone / path
        text = f.read_text()
        n = text.count(old)
        row = dict(mutant=name, file=path, anchors=n, checks=[])
        if n != 1:
            row["error"] = "anchor not found exactly once"
            rows.append(row); continue
        f.write_text(text.replace(old, new))
        try:
            for label, cmd, phrases in checks:
                t0 = time.time()
                p = subprocess.run(cmd, cwd=clone, env=ENV, capture_output=True, text=True)
                log = p.stdout + p.stderr
                lf = out / f"{tag}-{label.replace(' ', '_')}.log"
                lf.write_text(log)
                fails = [l for l in log.splitlines() if l.startswith("FAIL") or "AssertionError" in l or "gate 26" in l and ("!=" in l or "ACCEPTED" in l or "resolved" in l or "carry no" in l or "passes --clock" in l or "decided" in l) or "mutation did not reach" in l]
                row["checks"].append(dict(check=label, rc=p.returncode, seconds=round(time.time() - t0),
                                          caught=all(any(ph in l for l in log.splitlines()) for ph in phrases),
                                          phrases=phrases, failing_lines=fails[:12], log=lf.name))
        finally:
            f.write_text(text)
            subprocess.run(["git", "checkout", "--", path], cwd=clone)
        rows.append(row)
        (out / "mutants.json").write_text(json.dumps(rows, indent=1) + "\n")
    st = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=clone, capture_output=True, text=True).stdout
    (out / "mutants.json").write_text(json.dumps(dict(rows=rows, tree_after=st), indent=1) + "\n")
    (out / "DONE").write_text("done\n")

main()
