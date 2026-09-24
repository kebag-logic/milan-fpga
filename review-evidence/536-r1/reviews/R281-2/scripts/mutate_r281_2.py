#!/usr/bin/env python3
"""Reviewer-chosen mutation arms against the head's MVU model and steps.

Usage: mutate_r281_2.py --repo <clone at the head> --work <scratch dir>

Each arm gets its own disposable copy of tests/ (git archive of HEAD) with a
read-only link to the clone's protocol-processor, applies ONE text
substitution (which must match exactly once), runs the contract feature, and
compares the failing scenario lines with the expected set.  `SURVIVE` arms
are the ones the reviewer expects no row to see.  The clone is never written.
"""
import argparse
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True)
ap.add_argument("--work", required=True)
args = ap.parse_args()
REPO = Path(args.repo).resolve()
WORK = Path(args.work).resolve()
FEAT = (REPO / "tests/features/aecp_response_contract.feature").read_text()
FEAT_LINES = FEAT.splitlines()
MODEL = "tests/steps/aecp_engine_model.py"
STEPS = "tests/steps/aecp_engine_steps.py"


def row(*needles):
    """Feature line (1-based) of the unique line containing every needle."""
    hits = [i + 1 for i, l in enumerate(FEAT_LINES)
            if all(n in l for n in needles)]
    assert len(hits) == 1, (needles, hits)
    return hits[0]


G = "| 0x0000 | 0x0000   | 20     | 1"          # guard row tail, cdl 20
R = {
    "mvu0": row("| 0x0000       | GET_MILAN_INFO"),
    "mvu1": row("| 0x0001       | SET_SYSTEM_UNIQUE_ID"),
    "mvu2": row("| 0x0002       | GET_SYSTEM_UNIQUE_ID"),
    "mvu3": row("| 0x0003       | SET_MEDIA_CLOCK"),
    "mvu4": row("| 0x0004       | GET_MEDIA_CLOCK"),
    "quad": row("Scenario: GET_MILAN_INFO reports protocol_version 1"),
    "g22": row("| FF-1B-C5-0A-C1-00 |"), "g23": row("| 00-FF-C5-0A-C1-00 |"),
    "g24": row("| 00-1B-FF-0A-C1-00 |"), "g25": row("| 00-1B-C5-FF-C1-00 |"),
    "g26": row("| 00-1B-C5-0A-FF-00 |"), "g26h": row("| 00-1B-C5-0A-D1-00 |"),
    "g26l": row("| 00-1B-C5-0A-C2-00 |"), "g27": row("| 00-1B-C5-0A-C1-FF |"),
    "g27b": row("| 00-1B-C5-0A-C1-01 |"),
    "gr1": row("| 0x8000 | 0x0000   | 20"),
    "g19": row("| 19     | 1      | 19"),
    "junk": row("| 0xDEAD   |"),
    "l24": row("| 24     | 0      | 32"), "l112": row("| 112    | 0      | 32"),
    "mt0": row("|  0 | AEM_COMMAND"), "mt2": row("|  2 | ADDRESS_ACCESS"),
    "mt4": row("|  4 | AVC_COMMAND"), "mt8": row("|  8 | HDCP_APM"),
    "mt10": row("| 10 | reserved"), "mt12": row("| 12 | reserved"),
    "mt14": row("| 14 | EXTENDED_COMMAND"),
    "gate": row("Scenario: the served MVU command types are the ones"),
    "oui83a": 262, "oui83b": 263,   # checked against the head file below
}
assert FEAT_LINES[261].strip() == "| 0x8004 |" and FEAT_LINES[262].strip() == "| 0xFC1B |", \
    (FEAT_LINES[261], FEAT_LINES[262])
ALLG = ["g22", "g23", "g24", "g25", "g26", "g26h", "g26l", "g27", "g27b"]
MTS = ["mt0", "mt2", "mt4", "mt8", "mt10", "mt12", "mt14"]

ARMS = [
    ("A01 length floor 8 -> 7", MODEL,
     "len(cmd_payload) < MVU_CMD_PLD:", "len(cmd_payload) < MVU_CMD_PLD - 1:",
     ["g19"]),
    ("A02 length ceiling at 100 payload octets (cdl 112 still served)", MODEL,
     "len(cmd_payload) < MVU_CMD_PLD:",
     "len(cmd_payload) < MVU_CMD_PLD or len(cmd_payload) > 100:", []),
    ("A03 length ceiling at 99 payload octets", MODEL,
     "len(cmd_payload) < MVU_CMD_PLD:",
     "len(cmd_payload) < MVU_CMD_PLD or len(cmd_payload) > 99:", ["l112"]),
    ("A04 command reserved field forwarded into the Figure 5.4 body", MODEL,
     ">HHIII\", MVU_GET_MILAN_INFO, 0, MILAN_PROTOCOL_VERSION,",
     ">HHIII\", MVU_GET_MILAN_INFO, _be16(buf, 18), MILAN_PROTOCOL_VERSION,",
     ["junk"]),
    ("A05 protocol_id head (@22..@23) not compared", MODEL,
     "if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:",
     "if cmd_payload[0:4] != MILAN_PROTOCOL_ID[2:6]:", ["g22", "g23"]),
    ("A06 @26 compared on its high nibble only", MODEL,
     "if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:",
     "if (raw_ct + cmd_payload[0:2] != MILAN_PROTOCOL_ID[0:4] or "
     "cmd_payload[2] & 0xF0 != 0xC0 or cmd_payload[3] != 0):", ["g26l"]),
    ("A07 @26 compared on its low nibble only", MODEL,
     "if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:",
     "if (raw_ct + cmd_payload[0:2] != MILAN_PROTOCOL_ID[0:4] or "
     "cmd_payload[2] & 0x0F != 0x01 or cmd_payload[3] != 0):", ["g26h"]),
    ("A08 message_type 14 also decoded as MVU", MODEL,
     "if msg_type != MT_VU_COMMAND or", "if msg_type not in (MT_VU_COMMAND, 14) or",
     ["mt14"]),
    ("A09 r bit masked off the @28 word", MODEL,
     "    return _be16(cmd_payload, 4)\n", "    return _be16(cmd_payload, 4) & 0x7FFF\n",
     ["gr1"]),
    ("A10 every whole MVU command runs the GET_MILAN_INFO program", MODEL,
     "elif _mvu_command_type(msg_type, raw_ct, cmd_payload) in self.mvu_served:",
     "elif _mvu_command_type(msg_type, raw_ct, cmd_payload) is not None:",
     ["mvu1", "mvu2", "mvu3", "mvu4", "gr1"]),
    ("A11 VU echo capped at 20 payload octets", MODEL,
     "pld = pld_cmd if echo else",
     "pld = (min(pld_cmd, 20) if msg_type == 6 else pld_cmd) if echo else",
     ["mvu3"]),
    ("A12 Figure 5.4 body one quadlet long", MODEL,
     "MILAN_FEATURES_FLAGS, MILAN_CERTIFICATION_VERSION)",
     "MILAN_FEATURES_FLAGS, MILAN_CERTIFICATION_VERSION) + bytes(4)",
     ["mvu0", "junk", "l24", "l112"]),
    ("A13 Figure 5.6 name field 32 octets (cdl 60)", MODEL,
     'struct.pack(">BBBBI64s", 0x03, 0, 0, 0x80, 0, b"DEFAULT")',
     'struct.pack(">BBBBI32s", 0x03, 0, 0, 0x80, 0, b"DEFAULT")', ["mvu3"]),
    ("A14 Figure 5.5 system_unique_id dropped (cdl 20)", MODEL,
     "struct.pack(\">Q\", 0x0102030405060708)", "b\"\"", ["mvu1"]),
    ("A15 guard step ignores its protocol_id cell", STEPS,
     "build_mvu_command(int(word, 0), bytes.fromhex(pid.replace(\"-\", \"\")),",
     "build_mvu_command(int(word, 0), MILAN_PROTOCOL_ID,", ALLG),
    ("A16 guard step sends cdl > 20 without the extra octets", STEPS,
     "int(reserved, 0), bytes(range(max(cdl - 20, 0))),",
     "int(reserved, 0), b\"\",",
     # cdl 24 stays legal and over-length without the fill: a 46-octet
     # AVTPDU is padded to the 60-octet Ethernet minimum, so the 4 claimed
     # octets are pad zeros and the row is unchanged in meaning (equivalent)
     ["l112"]),
    ("A17 other-type step leaves message_type at 6", STEPS,
     "frame[ETH_HDR + 1] = (frame[ETH_HDR + 1] & 0xF0) | (mt & 0x0F)",
     "frame[ETH_HDR + 1] = frame[ETH_HDR + 1]", MTS),
    ("A18 VU response u-bit mask applied to message_type 6", MODEL,
     "f.append(raw_ct[0] & 0x7F if cmd_msg_type == MT_AEM_COMMAND",
     "f.append(raw_ct[0] & 0x7F if cmd_msg_type in (MT_AEM_COMMAND, 6)",
     # the two pre-existing issue #83 OUI rows (head 0x80..) see it too
     ["g22", "oui83a", "oui83b"]),
    ("A19 gate regex misses SET_ constants", STEPS,
     r'MVU_((?:GET|SET)_"', r'MVU_((?:GET)_"', []),
    ("A20 MVU dispatch arm made unreachable", MODEL,
     "elif _mvu_command_type(msg_type, raw_ct, cmd_payload) in self.mvu_served:",
     "elif False:", ["mvu0", "quad", "junk", "l24", "l112"]),
]


def run_arm(i, arm):
    name, rel, old, new, expect = arm
    d = WORK / ("arm%02d" % i)
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    subprocess.run("git -C %s archive HEAD tests | tar -x -C %s" % (REPO, d),
                   shell=True, check=True)
    # every other top-level entry is a read-only link to the clone, since
    # behave imports every step module and some read tb/ and scripts/
    for e in REPO.iterdir():
        if e.name not in ("tests", ".git"):
            (d / e.name).symlink_to(e)
    p = d / rel
    src = p.read_text()
    if old is not None:
        assert src.count(old) == 1, (name, src.count(old))
        p.write_text(src.replace(old, new, 1))
    r = subprocess.run([sys.executable, "-B", "-m", "behave", "--no-capture",
                        "-f", "plain",
                        "features/aecp_response_contract.feature"],
                       cwd=d / "tests", capture_output=True, text=True,
                       timeout=600)
    failing = sorted({int(m) for m in re.findall(
        r"aecp_response_contract\.feature:(\d+)",
        r.stdout.split("Failing scenarios:")[-1])} if "Failing scenarios:"
        in r.stdout else set())
    tail = [l for l in r.stdout.splitlines() if "scenarios passed" in l]
    want = sorted(R[k] for k in expect)
    return name, want, failing, r.returncode, tail[-1] if tail else "?"


arms = [("A00 control (no substitution)", MODEL, None, None, [])] + ARMS
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    res = list(ex.map(lambda a: run_arm(*a), enumerate(arms)))
ok = 0
for name, want, failing, rc, tail in res:
    exact = want == failing
    ok += exact
    print("%s | %s | expect %s | failing %s | %s" % (
        "EXACT" if exact else "DIFF", name, want or "SURVIVE", failing or "none",
        tail.strip()))
print("%d of %d arms exactly as expected" % (ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
