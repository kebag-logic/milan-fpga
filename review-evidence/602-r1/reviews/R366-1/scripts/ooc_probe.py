#!/usr/bin/env python3
"""OOC area probe for PR #603 (reviewer R366-1).

Runs syn/yosys/ooc.sh's milan_datapath row, with the shaped-default recipe the
executor published (review-evidence/602-r1/author/ooc_measure.py: parameters
patched into a private datapath copy, OOC_SHAPE set), for several datapath
variants. The only change to the ooc.sh copy is the yosys command: the same
`synth_xilinx -family xc7 -top milan_datapath -flatten` is split at the
`map_luts` label, with a `stat` written BEFORE LUT mapping (pre-ABC gate
netlist) and the usual `stat` after it. The final stat is comparable with
the published ones (checked in the report).

Usage: ooc_probe.py <repo> <work> <variant>... ; variants: base head c1 c2
Environment: JOBS (parallel yosys runs, default 4).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
VARIANTS = sys.argv[3:]
BASE = "6d5ebd7357c1e468e446f18a61527c5be6118a04"
DPREL = "hdl/milan/milan_datapath.sv"

base_src = subprocess.run(["git", "-C", str(ROOT), "show", f"{BASE}:{DPREL}"],
                          capture_output=True, text=True, check=True).stdout
head_src = (ROOT / DPREL).read_text()
BASE_EXPR = ("  wire mcr_restart_p_w = (crf_clk_selected_r\n"
             "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w))\n"
             "                       | media_rebase_p_w;\n")
HEAD_EXPR = ("  wire mcr_restart_p_w = crf_clk_selected_r\n"
             "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w);\n")
assert base_src.count(BASE_EXPR) == 1 and head_src.count(HEAD_EXPR) == 1


def variant(name):
    if name == "base":
        return base_src, "base 6d5ebd73 datapath"
    if name == "head":
        return head_src, "head 49012143 datapath"
    if name == "c1":
        # comparable one-term functional edit ELSEWHERE in the same OR: the
        # base with the received-CRF-mr echo term removed, re-base term kept
        return base_src.replace(BASE_EXPR, BASE_EXPR.replace(" | crf_mr_toggle_p_w", "")), \
            "control c1: base minus the crf_mr_toggle_p_w term (one-term edit of equal size)"
    if name == "c2":
        # semantically identical to head, operands reordered
        return head_src.replace(HEAD_EXPR,
                                "  wire mcr_restart_p_w = (crf_mr_toggle_p_w | (~crf_locked_w & tkd_crflk_q_r))\n"
                                "                          & crf_clk_selected_r;\n"), \
            "control c2: head expression with operands reordered (logically identical)"
    raise SystemExit(name)


common = dict(MILAN_CLK_FREQ_HZ=50000000, TALKER_WIRE_CHANS_P=8,
              AUDIO_IF_MASTER_P=1, GPTP_INGRESS_LAT_NS_P=656, GPTP_EGRESS_LAT_NS_P=219,
              I2SPB_P=0, LPF_P=0)
shapes = {
    "endstation_ax7101_1x1_tdm8": dict(N_STREAMS=1, AUDIO_IF_SLOTS_P=8,
                                       AUDIO_IF_CLK_HZ_P=24576000, AUDIO_IF_RENDER_SLOTS_P=8, LOOPBACK_P=1),
    "endstation_ax7101_8x8": dict(N_STREAMS=8, AUDIO_IF_SLOTS_P=32,
                                  AUDIO_IF_CLK_HZ_P=98304000, AUDIO_IF_RENDER_SLOTS_P=0, LOOPBACK_P=0,
                                  LTAP_P=0, DPROBES_P=0),
}
SYNTH_OLD = "synth_xilinx -family xc7$nodsp -top $top -flatten; stat; write_json $TMP/$top.ooc.json"
SYNTH_NEW = ("synth_xilinx -family xc7$nodsp -top $top -flatten -run :map_luts; "
             "tee -q -o $TMP/$top.preabc.stat stat; "
             "synth_xilinx -family xc7$nodsp -top $top -flatten -run map_luts:; "
             "stat; write_json $TMP/$top.ooc.json")


def stat_block(text):
    start = text.rfind("=== milan_datapath ===")
    cells = {}
    for line in text[start:].splitlines():
        m = re.match(r"\s+(\d+)\s+(\S+)$", line)
        if m:
            cells[m.group(2)] = int(m.group(1))
        if "Executing" in line or "End of script" in line:
            break
    return cells


def one(job):
    name, shape = job
    source, label = variant(name)
    params = common | shapes[shape]
    work = WORK / f"{name}-{shape}"
    work.mkdir(parents=True, exist_ok=True)
    shaped = source
    for key, value in params.items():
        shaped, count = re.subn(r"(parameter (?:int|bit)(?: unsigned)? " + key + r"\s*= )[^,\n]+",
                                lambda m: m[1] + str(value), shaped)
        assert count == 1, (key, count)
    dp = work / "milan_datapath.sv"
    dp.write_text(shaped)
    script = (ROOT / "syn/yosys/ooc.sh").read_text()
    script = script.replace('. "$(dirname "$0")/malloc.sh"', '. "' + str(ROOT / "syn/yosys/malloc.sh") + '"')
    script = script.replace('R="$(cd "$(dirname "$0")/../.." && pwd)"', 'R="' + str(ROOT) + '"')
    assert script.count("$R/hdl/milan/milan_datapath.sv") == 1 and script.count(SYNTH_OLD) == 1
    script = script.replace("$R/hdl/milan/milan_datapath.sv", str(dp)).replace(SYNTH_OLD, SYNTH_NEW)
    (work / "ooc.sh").write_text(script)
    env = dict(os.environ, OOC_SHAPE=str(ROOT / "configs/generated" / shape), OOC_TMP=str(work / "artifacts"))
    with open(work / "ooc.stdout", "w") as out:
        rc = subprocess.run(["bash", str(work / "ooc.sh"), "milan_datapath"], cwd=str(ROOT), env=env,
                            stdout=out, stderr=subprocess.STDOUT).returncode
    art = work / "artifacts"
    pre = (art / "milan_datapath.preabc.stat").read_text() if (art / "milan_datapath.preabc.stat").exists() else ""
    log = (art / "milan_datapath.ooc.log").read_text() if (art / "milan_datapath.ooc.log").exists() else ""
    rec = dict(variant=name, label=label, shape=shape, rc=rc,
               source_sha256=hashlib.sha256(source.encode()).hexdigest(),
               shaped_sha256=hashlib.sha256(shaped.encode()).hexdigest(),
               pre_abc=stat_block(pre), post=stat_block(log))
    (WORK / f"{name}-{shape}.json").write_text(json.dumps(rec, indent=2) + "\n")
    return rec


jobs = [(v, s) for v in VARIANTS for s in shapes]
with ThreadPoolExecutor(int(os.environ.get("JOBS", "4"))) as ex:
    recs = list(ex.map(one, jobs))
print(json.dumps([dict(variant=r["variant"], shape=r["shape"], rc=r["rc"]) for r in recs]))
sys.exit(1 if any(r["rc"] for r in recs) else 0)
