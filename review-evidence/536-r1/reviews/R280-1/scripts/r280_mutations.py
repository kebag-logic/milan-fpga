#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Review mutation probes against the MVU sub-decode of the offline model.

usage: r280_mutations.py <milan-fpga checkout> <scratch dir>

The checkout is never written. A shadow root is built under the scratch dir:
`tests/` is COPIED, every other top-level entry of the checkout is symlinked
(read-only use), so `ROOT = parents[2]` in the model still resolves the pinned
protocol-processor. Each arm applies one exact substitution to the copy, runs
the contract feature, records which scenarios failed, then restores the copy.
An arm SURVIVES when the feature stays green.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
shadow = Path(sys.argv[2]).resolve() / "mutroot"
if shadow.exists():
    shutil.rmtree(shadow)
shadow.mkdir(parents=True)
for entry in repo.iterdir():
    if entry.name in (".git", "tests"):
        continue
    (shadow / entry.name).symlink_to(entry)
shutil.copytree(repo / "tests", shadow / "tests",
                ignore=shutil.ignore_patterns("__pycache__"))

MODEL = shadow / "tests" / "steps" / "aecp_engine_model.py"
FEATURE = "features/aecp_response_contract.feature"

GUARD = "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n"
MTGUARD = ("    if msg_type != MT_VU_COMMAND or len(cmd_payload) < MVU_CMD_PLD:\n")
ARMS = [
    ("R1 protocol_id head @22..@23 not compared", MODEL, GUARD,
     "    if cmd_payload[0:4] != MILAN_PROTOCOL_ID[2:6]:\n"),
    ("R2 only @27 compared", MODEL, GUARD,
     "    if cmd_payload[3:4] != MILAN_PROTOCOL_ID[5:6]:\n"),
    ("R3 @24..@26 not compared", MODEL, GUARD,
     "    if (raw_ct != MILAN_PROTOCOL_ID[0:2]\n"
     "            or cmd_payload[3:4] != MILAN_PROTOCOL_ID[5:6]):\n"),
    ("R4 message_type guard dropped", MODEL, MTGUARD,
     "    if len(cmd_payload) < MVU_CMD_PLD:\n"),
    ("R5 ADDRESS_ACCESS also decoded as MVU", MODEL, MTGUARD,
     "    if (msg_type not in (MT_VU_COMMAND, MT_AA_COMMAND)\n"
     "            or len(cmd_payload) < MVU_CMD_PLD):\n"),
    ("R6 length guard at pp_top M6's 6 octets", MODEL, MTGUARD,
     "    if msg_type != MT_VU_COMMAND or len(cmd_payload) < 6:\n"),
    ("R7 served MVU answered with status NOT_IMPLEMENTED", MODEL,
     "        return ST_SUCCESS, 12 + len(body)\n",
     "        return ST_NOT_IMPLEMENTED, 12 + len(body)\n"),
    ("R8 served MVU emitted as an echo", MODEL,
     '            program, echo = "MVU", False\n',
     '            program, echo = "MVU", True\n'),
    ("R9 MVU arm ahead of the AEM arms", MODEL,
     "        if aem and opcode == OP_READ_DESCRIPTOR and not short:\n",
     "        if _mvu_command_type(msg_type, raw_ct, cmd_payload) in "
     "self.mvu_served:\n            program, echo = \"MVU\", False\n"
     "        elif aem and opcode == OP_READ_DESCRIPTOR and not short:\n"),
    ("R10 an MVU command walked and echoed only to the Figure 5.3 8 octets",
     MODEL, "        pld_cmd = min(cdl_pld, PLD_MAX, slot_pld)\n",
     "        pld_cmd = min(cdl_pld, PLD_MAX, slot_pld)\n"
     "        if msg_type == MT_VU_COMMAND:\n"
     "            pld_cmd = min(pld_cmd, MVU_CMD_PLD)\n"),
    ("R11 command_type not read: every whole Milan MVU command served",
     MODEL, "    return _be16(cmd_payload, 4)\n",
     "    return MVU_GET_MILAN_INFO\n"),
]


def run_feature():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(["behave", "--no-capture", "-f", "plain", FEATURE],
                       cwd=shadow / "tests", env=env, capture_output=True,
                       text=True, timeout=600)
    out = p.stdout + p.stderr
    tally = re.search(r"(\d+) scenarios passed, (\d+) failed, (\d+) skipped"
                      r"(?:, (\d+) error)?", out)
    return p.returncode, (tally.group(0) if tally else "no tally"), out


rc, tally, _ = run_feature()
print("CONTROL (no mutation): exit %d, %s" % (rc, tally))
survivors = 0
for name, path, old, new in ARMS:
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, "%s: anchor not unique" % name
    path.write_text(text.replace(old, new), encoding="utf-8")
    try:
        rc, tally, out = run_feature()
    finally:
        path.write_text(text, encoding="utf-8")
    verdict = "RED" if rc != 0 else "SURVIVED"
    survivors += rc == 0
    print("[%s] %s: exit %d, %s" % (verdict, name, rc, tally))
    fails = re.findall(r"^\s+(features/\S+\s+.*)$", out.split(
        "Failing scenarios:")[-1], re.M) if "Failing scenarios:" in out else []
    for f in fails:
        print("    fails: %s" % f.strip())
rc, tally, _ = run_feature()
print("CONTROL after restore: exit %d, %s" % (rc, tally))
print("%d arms, %d survived" % (len(ARMS), survivors))
