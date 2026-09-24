#!/usr/bin/env python3
"""Mutation arms for the #536 correction round 1 (R280-1 and R281-1 F1 to F3).

Each arm applies one exact substitution to a disposable copy of the lane's
`tests/` tree, runs the contract feature there, and compares the set of
failing or erroring scenarios (by feature line) with the set the arm is
expected to fail. The lane itself is never written: every other top-level
entry of the lane is symlinked into the copy, so the model's `ROOT` still
resolves the pinned protocol-processor.

An arm is RED-EXACT when it fails exactly its expected scenarios, RED-OTHER
when it fails but not exactly those, and SURVIVED when the feature stays
green. The run fails unless every arm is RED-EXACT and both controls are green.

usage: python3 -B mutations.py <lane-root> <scratch-dir>
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path(sys.argv[1]).resolve()
SHADOW = Path(sys.argv[2]).resolve() / "a230mut"
MODEL = "tests/steps/aecp_engine_model.py"
STEPS = "tests/steps/aecp_engine_steps.py"
FEATURE = "tests/features/aecp_response_contract.feature"

# feature lines at the head under test (fb84de54e)
ROW_0000, ROW_0001, ROW_0002, ROW_0003, ROW_0004 = 131, 136, 137, 138, 139
QUADLETS = 150
OCTET = {22: 181, 23: 182, 24: 183, 25: 184, 26: 185, 27: 188}
NIBBLE_HI, NIBBLE_LO = 186, 187
ONE_BIT, R_BIT, SHORT = 189, 190, 191
JUNK_RESERVED, LONG_24, LONG_112 = 196, 197, 198
MT_ROW = {0: 219, 2: 220, 4: 221, 8: 222, 10: 223, 12: 224, 14: 225}
RTL_GATE = 233

PID_GUARD = "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n"
MT_GUARD = "    if msg_type != MT_VU_COMMAND or len(cmd_payload) < MVU_CMD_PLD:\n"
SERVED_MVU_END = '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n}'


def row_cell(row, old, new):
    """Replace one cell of one Examples row, anchored on the row's first cell."""
    return (FEATURE, re.compile(r"^(\s+\| %s\s+\|.*?\| )%s(\s+\|)" % (row, re.escape(old)),
                                re.M), r"\g<1>%s\g<2>" % new)


def pid_arm(expr):
    """The protocol_id comparison replaced by `expr`."""
    return (MODEL, PID_GUARD, "    if %s:\n" % expr)


def served_mvu(ct, name, clause):
    """SERVED_MVU widened by one Table 5.18 command."""
    return (STEPS, SERVED_MVU_END,
            SERVED_MVU_END[:-1] + '    %#06x: dict(name="%s", clause="Milan %s"),\n}'
            % (ct, name, clause))


ARMS = [
    # ---- F2: each RECOMMENDED row in its own figure ----------------------
    ("F2 R280 R10: an MVU command walked and echoed only to Figure 5.3's 8 octets",
     (MODEL, "        pld_cmd = min(cdl_pld, PLD_MAX, slot_pld)\n",
      "        pld_cmd = min(cdl_pld, PLD_MAX, slot_pld)\n"
      "        if msg_type == MT_VU_COMMAND:\n"
      "            pld_cmd = min(pld_cmd, MVU_CMD_PLD)\n"),
     {ROW_0001, ROW_0003}),
    ("F2 R281: the MVU NOT_IMPLEMENTED echo capped at 8 payload octets",
     (MODEL, "        pld = pld_cmd if echo else min(max(resp_len - 12, 0), PLD_MAX)\n",
      "        pld = ((min(pld_cmd, MVU_CMD_PLD) if msg_type == MT_VU_COMMAND\n"
      "                else pld_cmd) if echo\n"
      "               else min(max(resp_len - 12, 0), PLD_MAX))\n"),
     {ROW_0001, ROW_0003}),
    ("F2: SET_SYSTEM_UNIQUE_ID sent without Figure 5.5's system_unique_id",
     (MODEL, '             struct.pack(">Q", 0x0102030405060708)),\n', '             b""),\n'),
     {ROW_0001}),
    ("F2: SET_MEDIA_CLOCK_REFERENCE_INFO sent without Figure 5.6's @32..@103",
     (MODEL, '             struct.pack(">BBBBI64s", 0x03, 0, 0, 0x80, 0, b"DEFAULT")),\n',
      '             b""),\n'),
     {ROW_0003}),
    ("F2: row 0x0001 cdl cell back to 20", row_cell("0x0001", "28 ", "20 "), {ROW_0001}),
    ("F2: row 0x0003 cdl cell back to 20", row_cell("0x0003", "92 ", "20 "), {ROW_0003}),
    ("F2: row 0x0001 names Figure 5.3 (the form guard)",
     row_cell("0x0001", "Figure 5.5", "Figure 5.3"), {ROW_0001}),
    ("F2: row 0x0004 names Figure 5.3 (the form guard)",
     row_cell("0x0004", "Figure 5.7", "Figure 5.3"), {ROW_0004}),
    ("F2: row 0x0000 status 0 -> 1", row_cell("0x0000", "0 ", "1 "), {ROW_0000}),
    ("F2: row 0x0001 status 1 -> 0", row_cell("0x0001", "1 ", "0 "), {ROW_0001}),
    ("F2: row 0x0002 status 1 -> 0", row_cell("0x0002", "1 ", "0 "), {ROW_0002}),
    ("F2: row 0x0003 status 1 -> 0", row_cell("0x0003", "1 ", "0 "), {ROW_0003}),
    ("F2: row 0x0004 status 1 -> 0", row_cell("0x0004", "1 ", "0 "), {ROW_0004}),
    ("F2: SERVED_MVU declares 0x0001", served_mvu(1, "SET_SYSTEM_UNIQUE_ID", "5.4.4.2"),
     {ROW_0001, RTL_GATE}),
    ("F2: SERVED_MVU declares 0x0002", served_mvu(2, "GET_SYSTEM_UNIQUE_ID", "5.4.4.3"),
     {ROW_0002, RTL_GATE}),
    ("F2: SERVED_MVU declares 0x0003",
     served_mvu(3, "SET_MEDIA_CLOCK_REFERENCE_INFO", "5.4.4.4"), {ROW_0003, RTL_GATE}),
    ("F2: SERVED_MVU declares 0x0004",
     served_mvu(4, "GET_MEDIA_CLOCK_REFERENCE_INFO", "5.4.4.5"), {ROW_0004, RTL_GATE}),
    ("F2 R280 R11: command_type not read",
     (MODEL, "    return _be16(cmd_payload, 4)\n", "    return MVU_GET_MILAN_INFO\n"),
     {ROW_0001, ROW_0002, ROW_0003, ROW_0004, R_BIT}),
    ("F2: the model reverted, MVU dispatch arm never taken",
     (MODEL, "        elif _mvu_command_type(msg_type, raw_ct, cmd_payload) in self.mvu_served:\n",
      "        elif False and _mvu_command_type(msg_type, raw_ct, cmd_payload) in self.mvu_served:\n"),
     {ROW_0000, QUADLETS, JUNK_RESERVED, LONG_24, LONG_112}),
    # ---- F1: the protocol_id, one octet at a time (pp_top M8) -------------
    ("F1: @22 not compared", pid_arm(
        "raw_ct[1:2] + cmd_payload[0:4] != MILAN_PROTOCOL_ID[1:6]"), {OCTET[22]}),
    ("F1: @23 not compared", pid_arm(
        "raw_ct[0:1] + cmd_payload[0:4] != MILAN_PROTOCOL_ID[0:1] + MILAN_PROTOCOL_ID[2:6]"),
     {OCTET[23]}),
    ("F1: @24 not compared", pid_arm(
        "raw_ct + cmd_payload[1:4] != MILAN_PROTOCOL_ID[0:2] + MILAN_PROTOCOL_ID[3:6]"),
     {OCTET[24]}),
    ("F1: @25 not compared", pid_arm(
        "raw_ct + cmd_payload[0:1] + cmd_payload[2:4] != MILAN_PROTOCOL_ID[0:3] + MILAN_PROTOCOL_ID[4:6]"),
     {OCTET[25]}),
    ("F1: @26 not compared", pid_arm(
        "raw_ct + cmd_payload[0:2] + cmd_payload[3:4] != MILAN_PROTOCOL_ID[0:4] + MILAN_PROTOCOL_ID[5:6]"),
     {OCTET[26], NIBBLE_HI, NIBBLE_LO}),
    ("F1: @27 not compared", pid_arm(
        "raw_ct + cmd_payload[0:3] != MILAN_PROTOCOL_ID[0:5]"), {OCTET[27], ONE_BIT}),
    ("F1: @26 cut down to its high nibble (the OUI-36's last)", pid_arm(
        "raw_ct + cmd_payload[0:2] + bytes((cmd_payload[2] & 0xF0,)) + cmd_payload[3:4]"
        " != MILAN_PROTOCOL_ID[0:4] + bytes((0xC0,)) + MILAN_PROTOCOL_ID[5:6]"), {NIBBLE_LO}),
    ("F1: @26 cut down to its low nibble (the protocol id's top)", pid_arm(
        "raw_ct + cmd_payload[0:2] + bytes((cmd_payload[2] & 0x0F,)) + cmd_payload[3:4]"
        " != MILAN_PROTOCOL_ID[0:4] + bytes((0x01,)) + MILAN_PROTOCOL_ID[5:6]"), {NIBBLE_HI}),
    ("F1 R280 R2 / R281 pid_only_27: only @27 compared", pid_arm(
        "cmd_payload[3:4] != MILAN_PROTOCOL_ID[5:6]"),
     {OCTET[22], OCTET[23], OCTET[24], OCTET[25], OCTET[26], NIBBLE_HI, NIBBLE_LO}),
    # ---- F1: the message type ---------------------------------------------
    ("F1 R281 mt_guard_dropped: message_type not compared",
     (MODEL, MT_GUARD, "    if len(cmd_payload) < MVU_CMD_PLD:\n"), set(MT_ROW.values())),
] + [
    ("F1: message_type %d also decoded as MVU" % mt,
     (MODEL, MT_GUARD, "    if msg_type not in (MT_VU_COMMAND, %d) or len(cmd_payload) < MVU_CMD_PLD:\n"
      % mt), {row})
    for mt, row in MT_ROW.items()
] + [
    ("F1: the step leaves the frame at message_type 6",
     (STEPS, "    frame[ETH_HDR + 1] = (frame[ETH_HDR + 1] & 0xF0) | (mt & 0x0F)\n", ""),
     set(MT_ROW.values())),
    # ---- F1: the length is a floor, not an exact size ----------------------
    ("F1 R281 len_exact_20: the length guard made exact",
     (MODEL, MT_GUARD, "    if msg_type != MT_VU_COMMAND or len(cmd_payload) != MVU_CMD_PLD:\n"),
     {LONG_24, LONG_112}),
    ("F1: the length capped at Figure 5.3 plus a quadlet",
     (MODEL, MT_GUARD, "    if msg_type != MT_VU_COMMAND or not (MVU_CMD_PLD <= len(cmd_payload)"
      " <= MVU_CMD_PLD + 4):\n"), {LONG_112}),
    ("F1: row cdl 24 status 0 -> 1",
     (FEATURE, "| 0x0000 | 0x0000   | 24     | 0      |", "| 0x0000 | 0x0000   | 24     | 1      |"),
     {LONG_24}),
]


def build_shadow():
    """A fresh copy of tests/ beside read-only links to everything else."""
    if SHADOW.exists():
        shutil.rmtree(SHADOW)
    SHADOW.mkdir(parents=True)
    for entry in LANE.iterdir():
        if entry.name not in (".git", "tests"):
            (SHADOW / entry.name).symlink_to(entry)
    shutil.copytree(LANE / "tests", SHADOW / "tests",
                    ignore=shutil.ignore_patterns("__pycache__"))


def apply(rel, old, new):
    """One exact substitution in the shadow copy; an anchor that is not unique refuses."""
    path = SHADOW / rel
    text = path.read_text(encoding="utf-8")
    if isinstance(old, re.Pattern):
        out, n = old.subn(new, text)
    else:
        n = text.count(old)
        out = text.replace(old, new)
    if n != 1:
        raise SystemExit("anchor in %s matched %d times: %r" % (rel, n, old))
    path.write_text(out, encoding="utf-8")


def restore(rel):
    shutil.copyfile(LANE / rel, SHADOW / rel)


def run():
    """The contract feature in the shadow; returns (exit, failing lines, tally)."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(["behave", "--no-capture", "-f", "plain",
                           "features/aecp_response_contract.feature"],
                          cwd=SHADOW / "tests", env=env, capture_output=True,
                          text=True, check=False, timeout=600)
    out = proc.stdout + proc.stderr
    lines = set(int(n) for n in re.findall(
        r"^\s+features/aecp_response_contract\.feature:(\d+)\s", out, re.M))
    tally = [ln.strip() for ln in out.splitlines() if "scenarios passed" in ln]
    return proc.returncode, lines, tally[-1] if tally else "no tally: " + out[-400:]


def main():
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=LANE, capture_output=True,
                          text=True, check=True).stdout.strip()
    print("lane head %s" % head)
    build_shadow()
    rc, failing, tally = run()
    print("CONTROL before: exit %d, %s" % (rc, tally))
    ok = rc == 0 and not failing
    exact = 0
    for name, (rel, old, new), expect in ARMS:
        apply(rel, old, new)
        try:
            rc, failing, tally = run()
        finally:
            restore(rel)
        if rc == 0:
            verdict = "SURVIVED"
        elif failing == expect:
            verdict = "RED-EXACT"
            exact += 1
        else:
            verdict = "RED-OTHER"
        print("[%s] %s\n    file %s; %s\n    failing lines %s; expected %s"
              % (verdict, name, rel, tally, sorted(failing), sorted(expect)))
    rc, failing, tally = run()
    print("CONTROL after: exit %d, %s" % (rc, tally))
    ok = ok and rc == 0 and not failing
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=LANE, capture_output=True,
                           text=True, check=True).stdout
    print("%d arms, %d RED-EXACT; lane worktree %s"
          % (len(ARMS), exact, "clean" if not dirty.strip() else "DIRTY:\n" + dirty))
    shutil.rmtree(SHADOW)
    return 0 if ok and exact == len(ARMS) and not dirty.strip() else 1


if __name__ == "__main__":
    sys.exit(main())
