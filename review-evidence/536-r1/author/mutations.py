#!/usr/bin/env python3
"""Mutation arms for the #536 MVU rows.

Each arm applies one exact text substitution to a committed file of the lane,
runs `behave` on the contract feature, records the failing scenarios, and
restores the file from git. An arm is RED when at least one scenario fails or
errors; the expected failing scenarios are listed with each arm.

Run from anywhere: python3 mutations.py <lane-root>
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(sys.argv[1]).resolve()
MODEL = "tests/steps/aecp_engine_model.py"
STEPS = "tests/steps/aecp_engine_steps.py"
FEATURE = "tests/features/aecp_response_contract.feature"
ENGINE = LANE / "protocol-processor/hdl/aecp/KL_aecp_engine.sv"

# a copy of the pinned engine that ALSO declares GET_SYSTEM_UNIQUE_ID, standing
# in for a future pin that serves it; the submodule itself is never edited
FAKE_SV = Path(tempfile.mkdtemp(prefix="a223-")) / "KL_aecp_engine.sv"
FAKE_SV.write_text(ENGINE.read_text(encoding="utf-8").replace(
    "localparam logic [15:0] MVU_GET_MILAN_INFO_C = 16'h0000;",
    "localparam logic [15:0] MVU_GET_MILAN_INFO_C = 16'h0000;\n"
    "  localparam logic [15:0] MVU_GET_SYSTEM_UNIQUE_ID_C = 16'h0002;", 1),
    encoding="utf-8")


def row_flip(ct, old, new):
    """Flip one Examples row's status cell in the MVU outline."""
    pat = re.compile(r"^(\s+\| %s\s+\|[^|]+\|[^|]+\| )%s(\s+\|)" % (ct, old),
                     re.M)
    return ("regex", pat, r"\g<1>%s\g<2>" % new)


ARMS = [
    # (name, file, old, new, expected failing scenarios)
    ("model reverted: the MVU dispatch arm never taken", MODEL,
     "elif _mvu_command_type(msg_type, raw_ct, cmd_payload) in self.mvu_served:",
     "elif False and _mvu_command_type(msg_type, raw_ct, cmd_payload) in self.mvu_served:",
     "row 0x0000, the field scenario, the junk-reserved row"),
    ("row 0x0000 status flipped 0 -> 1", FEATURE, *row_flip("0x0000", "0", "1")[1:],
     "row 0x0000"),
    ("row 0x0001 status flipped 1 -> 0", FEATURE, *row_flip("0x0001", "1", "0")[1:],
     "row 0x0001"),
    ("row 0x0002 status flipped 1 -> 0", FEATURE, *row_flip("0x0002", "1", "0")[1:],
     "row 0x0002"),
    ("row 0x0003 status flipped 1 -> 0", FEATURE, *row_flip("0x0003", "1", "0")[1:],
     "row 0x0003"),
    ("row 0x0004 status flipped 1 -> 0", FEATURE, *row_flip("0x0004", "1", "0")[1:],
     "row 0x0004"),
    ("model serves 0x0001 (declared in SERVED_MVU)", STEPS,
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n}',
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n'
     '    0x0001: dict(name="SET_SYSTEM_UNIQUE_ID", clause="Milan 5.4.4.2"),\n}',
     "row 0x0001 (no program), the RTL gate"),
    ("model serves 0x0002 (declared in SERVED_MVU)", STEPS,
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n}',
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n'
     '    0x0002: dict(name="GET_SYSTEM_UNIQUE_ID", clause="Milan 5.4.4.3"),\n}',
     "row 0x0002 (no program), the RTL gate"),
    ("model serves 0x0003 (declared in SERVED_MVU)", STEPS,
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n}',
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n'
     '    0x0003: dict(name="SET_MEDIA_CLOCK_REFERENCE_INFO", clause="Milan 5.4.4.4"),\n}',
     "row 0x0003 (no program), the RTL gate"),
    ("model serves 0x0004 (declared in SERVED_MVU)", STEPS,
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n}',
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n'
     '    0x0004: dict(name="GET_MEDIA_CLOCK_REFERENCE_INFO", clause="Milan 5.4.4.5"),\n}',
     "row 0x0004 (no program), the RTL gate"),
    ("command_type ignored: every whole Milan MVU command is GET_MILAN_INFO", MODEL,
     "    return _be16(cmd_payload, 4)\n",
     "    return MVU_GET_MILAN_INFO\n",
     "rows 0x0001-0x0004, the r = 1 row"),
    ("Figure 5.3 length guard dropped", MODEL,
     "len(cmd_payload) < MVU_CMD_PLD:", "len(cmd_payload) < 0:",
     "the one-octet-short row"),
    ("protocol_id tail not compared (head only)", MODEL,
     "if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:",
     "if raw_ct != MILAN_PROTOCOL_ID[0:2]:",
     "the foreign 12-bit protocol id row"),
    ("r bit masked off the @28 word", MODEL,
     "    return _be16(cmd_payload, 4)\n",
     "    return _be16(cmd_payload, 4) & 0x7FFF\n",
     "the r = 1 row"),
    ("reserved field forwarded from the command", MODEL,
     '">HHIII", MVU_GET_MILAN_INFO, 0, MILAN_PROTOCOL_VERSION,',
     '">HHIII", MVU_GET_MILAN_INFO, (buf[18] << 8) | buf[19], MILAN_PROTOCOL_VERSION,',
     "the junk-reserved row"),
    ("protocol_version 2", MODEL,
     "MILAN_PROTOCOL_VERSION = 1\n", "MILAN_PROTOCOL_VERSION = 2\n",
     "the field scenario"),
    ("features_flags claims REDUNDANCY", MODEL,
     "MILAN_FEATURES_FLAGS = 0x00000000\n", "MILAN_FEATURES_FLAGS = 0x00000001\n",
     "the field scenario"),
    ("certification_version claims 1.0.0.0", MODEL,
     "MILAN_CERTIFICATION_VERSION = 0x00000000\n",
     "MILAN_CERTIFICATION_VERSION = 0x01000000\n",
     "the field scenario"),
    ("Figure 5.4 body one quadlet short (cdl 28)", MODEL,
     '">HHIII", MVU_GET_MILAN_INFO, 0, MILAN_PROTOCOL_VERSION,\n'
     '            MILAN_FEATURES_FLAGS, MILAN_CERTIFICATION_VERSION)',
     '">HHII", MVU_GET_MILAN_INFO, 0, MILAN_PROTOCOL_VERSION,\n'
     '            MILAN_FEATURES_FLAGS)',
     "row 0x0000, the field scenario, the junk-reserved row"),
    ("a future pin serves GET_SYSTEM_UNIQUE_ID (RTL copy)", STEPS,
     '_ENGINE_SV = (ROOT / "protocol-processor" / "hdl" / "aecp"\n'
     '              / "KL_aecp_engine.sv")',
     '_ENGINE_SV = Path(%r)' % str(FAKE_SV),
     "the RTL gate (and the AEM inventory gate stays green)"),
    ("SERVED_MVU names the command wrongly", STEPS,
     '0x0000: dict(name="GET_MILAN_INFO"', '0x0000: dict(name="GET_MILAN_INFOS"',
     "the RTL gate"),
]


def apply(path, old, new):
    """Substitute exactly once, refusing an arm whose anchor is missing."""
    target = LANE / path
    text = target.read_text(encoding="utf-8")
    if isinstance(old, re.Pattern):
        out, n = old.subn(new, text)
    else:
        n = text.count(old)
        out = text.replace(old, new)
    if n != 1:
        raise SystemExit("anchor for %s matched %d times" % (path, n))
    target.write_text(out, encoding="utf-8")


def run():
    """The feature under test, plain format; returns (exit, failing names, tally)."""
    proc = subprocess.run(
        ["behave", "--no-capture", "-f", "plain", "features/"
         "aecp_response_contract.feature"],
        cwd=LANE / "tests", capture_output=True, text=True, check=False)
    failing = []
    current = None
    for line in proc.stdout.splitlines():
        if line.lstrip().startswith(("Scenario:", "Scenario Outline:")):
            current = line.strip()
        elif (" ... failed" in line or " ... error" in line) and current:
            if current not in failing:
                failing.append(current)
    tally = [ln for ln in proc.stdout.splitlines() if "scenarios passed" in ln]
    return proc.returncode, failing, tally[-1] if tally else "no tally"


def main():
    """Every arm must turn the feature red, and the tree must end clean."""
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=LANE,
                          capture_output=True, text=True, check=True).stdout.strip()
    print("lane head %s" % head)
    rc, failing, tally = run()
    print("CONTROL (no mutation): exit %d, %s" % (rc, tally))
    assert rc == 0 and not failing, "the unmutated feature is not green"
    survivors = 0
    for name, path, old, new, expect in ARMS:
        apply(path, old, new)
        try:
            rc, failing, tally = run()
        finally:
            subprocess.run(["git", "checkout", "--", path], cwd=LANE, check=True)
        verdict = "RED" if rc != 0 and failing else "SURVIVED"
        survivors += verdict == "SURVIVED"
        print("\n[%s] %s\n  file: %s\n  expected to fail: %s\n  %s"
              % (verdict, name, path, expect, tally))
        for f in failing:
            print("    fails: %s" % f)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=LANE,
                           capture_output=True, text=True, check=True).stdout
    print("\n%d arms, %d survived; tree after restore: %s"
          % (len(ARMS), survivors, "clean" if not dirty.strip() else dirty))
    return 1 if survivors or dirty.strip() else 0


if __name__ == "__main__":
    sys.exit(main())
