#!/usr/bin/env python3
"""Reviewer-designed mutation arms for the MVU rows of the AECP contract
feature. Each arm is one textual substitution applied to a disposable copy of
tests/ (the checkout is only read); the arm must make exactly the expected
feature lines fail. Every other top-level entry is a symlink to the checkout,
so the RTL gate reads the real pinned engine.

Usage: model_mutations.py <repo-root> <scratch-dir>
"""
import json
import os
import shutil
import subprocess
import sys

root, scratch = map(os.path.abspath, sys.argv[1:3])
MODEL = "steps/aecp_engine_model.py"
STEPS = "steps/aecp_engine_steps.py"
FEAT = "features/aecp_response_contract.feature"

PID_CMP = "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n"


def pid(expr):
    return PID_CMP, "    if %s != MILAN_PROTOCOL_ID:\n" % expr


ARMS = [
    ("control: unmodified", None, None, None, set()),
    ("MVU dispatch arm unreachable", MODEL,
     "in self.mvu_served:", "in ():", {131, 150, 196, 197, 198}),
    ("@22 not compared", MODEL, *pid(
        "bytes([0x00]) + raw_ct[1:2] + cmd_payload[0:4]"), {181}),
    ("@23 not compared", MODEL, *pid(
        "raw_ct[0:1] + bytes([0x1B]) + cmd_payload[0:4]"), {182}),
    ("@24 not compared", MODEL, *pid(
        "raw_ct + bytes([0xC5]) + cmd_payload[1:4]"), {183}),
    ("@25 not compared", MODEL, *pid(
        "raw_ct + cmd_payload[0:1] + bytes([0x0A]) + cmd_payload[2:4]"), {184}),
    ("@26 not compared", MODEL, *pid(
        "raw_ct + cmd_payload[0:2] + bytes([0xC1]) + cmd_payload[3:4]"),
     {185, 186, 187}),
    ("@26 high nibble only", MODEL, *pid(
        "raw_ct + cmd_payload[0:2] + bytes([(cmd_payload[2] & 0xF0) | 0x01])"
        " + cmd_payload[3:4]"), {187}),
    ("@26 low nibble only", MODEL, *pid(
        "raw_ct + cmd_payload[0:2] + bytes([0xC0 | (cmd_payload[2] & 0x0F)])"
        " + cmd_payload[3:4]"), {186}),
    ("@27 bit 0 ignored", MODEL, *pid(
        "raw_ct + cmd_payload[0:3] + bytes([cmd_payload[3] & 0xFE])"), {189}),
    ("@27 not compared", MODEL, *pid(
        "raw_ct + cmd_payload[0:3] + bytes([0x00])"), {188, 189}),
    ("r bit masked", MODEL, "    return _be16(cmd_payload, 4)\n",
     "    return _be16(cmd_payload, 4) & 0x7FFF\n", {190}),
    ("command_type not read", MODEL, "    return _be16(cmd_payload, 4)\n",
     "    return 0\n", {136, 137, 138, 139, 190}),
    ("length floor one short", MODEL, "len(cmd_payload) < MVU_CMD_PLD",
     "len(cmd_payload) < MVU_CMD_PLD - 1", {191}),
    ("length exact", MODEL, "len(cmd_payload) < MVU_CMD_PLD",
     "len(cmd_payload) != MVU_CMD_PLD", {197, 198}),
    ("length capped at Figure 5.3 + 4", MODEL, "len(cmd_payload) < MVU_CMD_PLD",
     "not MVU_CMD_PLD <= len(cmd_payload) <= MVU_CMD_PLD + 4", {198}),
    ("message_type 0 also MVU", MODEL, "if msg_type != MT_VU_COMMAND or",
     "if msg_type not in (MT_VU_COMMAND, 0) or", {219}),
    ("message_type 10 also MVU", MODEL, "if msg_type != MT_VU_COMMAND or",
     "if msg_type not in (MT_VU_COMMAND, 10) or", {223}),
    ("message_type not compared", MODEL, "if msg_type != MT_VU_COMMAND or",
     "if", set(range(219, 226))),
    ("MVU echo capped at 8 payload octets", MODEL,
     "        pld = pld_cmd if echo else",
     "        pld = (min(pld_cmd, 8) if msg_type == MT_VU_COMMAND else pld_cmd)"
     " if echo else", {136, 138}),
    ("Figure 5.6 reserved quadlet dropped", MODEL,
     'struct.pack(">BBBBI64s", 0x03, 0, 0, 0x80, 0, b"DEFAULT")',
     'struct.pack(">BBBB64s", 0x03, 0, 0, 0x80, b"DEFAULT")', {138}),
    ("Figure 5.5 system_unique_id dropped", MODEL,
     'struct.pack(">Q", 0x0102030405060708)', 'b""', {136}),
    ("Figure 5.7 given 2 extra octets", MODEL,
     '    0x0004: ("Figure 5.7", 0, b""),', '    0x0004: ("Figure 5.7", 0, b"\\0\\0"),',
     {139}),
    ("response forwards command reserved", MODEL,
     "MVU_GET_MILAN_INFO, 0, MILAN_PROTOCOL_VERSION",
     "MVU_GET_MILAN_INFO, _be16(buf, 18), MILAN_PROTOCOL_VERSION", {196}),
    ("protocol_version 2", MODEL, "MILAN_PROTOCOL_VERSION = 1",
     "MILAN_PROTOCOL_VERSION = 2", {150}),
    ("features_flags REDUNDANCY", MODEL, "MILAN_FEATURES_FLAGS = 0x00000000",
     "MILAN_FEATURES_FLAGS = 0x00000001", {150}),
    ("certification_version 1", MODEL,
     "MILAN_CERTIFICATION_VERSION = 0x00000000",
     "MILAN_CERTIFICATION_VERSION = 0x00000001", {150}),
    ("Figure 5.4 body one quadlet short", MODEL,
     '">HHIII", MVU_GET_MILAN_INFO, 0, MILAN_PROTOCOL_VERSION,\n'
     '            MILAN_FEATURES_FLAGS, MILAN_CERTIFICATION_VERSION)',
     '">HHII", MVU_GET_MILAN_INFO, 0, MILAN_PROTOCOL_VERSION,\n'
     '            MILAN_FEATURES_FLAGS)', {131, 150, 196, 197, 198}),
    ("GET_SYSTEM_UNIQUE_ID declared served", STEPS,
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n',
     '    0x0000: dict(name="GET_MILAN_INFO", clause="Milan 5.4.4.1"),\n'
     '    0x0002: dict(name="GET_SYSTEM_UNIQUE_ID", clause="Milan 5.4.4.3"),\n',
     {137, 233}),
    ("message_type step leaves type 6", STEPS,
     "frame[ETH_HDR + 1] = (frame[ETH_HDR + 1] & 0xF0) | (mt & 0x0F)",
     "frame[ETH_HDR + 1] = frame[ETH_HDR + 1]", set(range(219, 226))),
    ("over-length step sends no extra octets", STEPS,
     "bytes(range(max(cdl - 20, 0)))", 'b""', {197, 198}),
]


def failing_lines(tests_dir):
    out = os.path.join(tests_dir, "result.json")
    subprocess.run(["behave", "--no-capture", "-f", "json", "-o", out, FEAT],
                   cwd=tests_dir, capture_output=True, text=True, timeout=600,
                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    bad, total = set(), 0
    for feat in json.load(open(out, encoding="utf-8")):
        for el in feat.get("elements", []):
            if el.get("type") != "scenario":
                continue
            total += 1
            if el.get("status") != "passed":
                bad.add(int(el["location"].rsplit(":", 1)[1]))
    return bad, total


results = []
for name, rel, old, new, expect in ARMS:
    d = os.path.join(scratch, "mut")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    shutil.copytree(os.path.join(root, "tests"), os.path.join(d, "tests"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    for entry in os.listdir(root):
        if entry not in ("tests", ".git"):
            os.symlink(os.path.join(root, entry), os.path.join(d, entry))
    if rel:
        p = os.path.join(d, "tests", rel)
        s = open(p, encoding="utf-8").read()
        n = s.count(old)
        if n != 1:
            results.append("ANCHOR-%d  %s" % (n, name))
            continue
        open(p, "w", encoding="utf-8").write(s.replace(old, new))
    bad, total = failing_lines(os.path.join(d, "tests"))
    verdict = "EXACT" if bad == expect else "DIFF"
    results.append("%-5s %-42s expected %s got %s (%d scenarios)"
                   % (verdict, name, sorted(expect), sorted(bad), total))
    print(results[-1], flush=True)
ok = all(r.startswith("EXACT") for r in results)
print("arms %d, exact %d" % (len(results),
                              sum(r.startswith("EXACT") for r in results)))
sys.exit(0 if ok else 1)
