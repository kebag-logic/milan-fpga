#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer mutation probe for PR #543 (issue #536), round R281-1.

Each arm is ONE literal substitution in a disposable copy of the candidate's
tests/ tree; the clone itself is never written.  Every other top-level entry of
the clone is symlinked read-only into the probe tree so the model's ROOT-relative
reads (protocol-processor/, scripts/) resolve to the exact-head bytes.

Usage:
  mutate_model.py --clone <path-to-exact-head-clone> --scratch <dir> --out <log>

An arm is KILLED when the contract feature goes red and SURVIVED when it stays
green.  The script refuses to run an arm whose substitution does not match
exactly once, so a stale arm cannot report a false survivor.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

MODEL = "tests/steps/aecp_engine_model.py"
FEATURE = "features/aecp_response_contract.feature"

# (name, file, old, new, what it removes from the engine's sub-decode)
ARMS = [
    ("baseline", None, None, None, "unmodified exact-head copy"),
    ("mt_guard_dropped", MODEL,
     "    if msg_type != MT_VU_COMMAND or len(cmd_payload) < MVU_CMD_PLD:\n",
     "    if len(cmd_payload) < MVU_CMD_PLD:\n",
     "the message_type 6 conjunct (RTL: cmd_r.protocol == PP_PROTO_MVU)"),
    ("len_exact_20", MODEL,
     "len(cmd_payload) < MVU_CMD_PLD:\n",
     "len(cmd_payload) != MVU_CMD_PLD:\n",
     "the >= side of the length guard (RTL: pld_cmd_r >= MVU_CMD_PLD_C)"),
    ("len_off_by_one", MODEL,
     "len(cmd_payload) < MVU_CMD_PLD:\n",
     "len(cmd_payload) < MVU_CMD_PLD - 1:\n",
     "the Figure 5.3 floor lowered by one octet"),
    ("pid_head_22_23_dropped", MODEL,
     "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n",
     "    if cmd_payload[0:4] != MILAN_PROTOCOL_ID[2:6]:\n",
     "the @22..@23 compare (RTL: raw_ct_r == MVU_PID_HI_C)"),
    ("pid_24_25_dropped", MODEL,
     "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n",
     "    if raw_ct + cmd_payload[2:4] != MILAN_PROTOCOL_ID[0:2] + MILAN_PROTOCOL_ID[4:6]:\n",
     "the @24..@25 compare (RTL: cfg_ix_r == MVU_PID_MD_C)"),
    ("pid_26_dropped", MODEL,
     "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n",
     "    if raw_ct + cmd_payload[0:2] + cmd_payload[3:4] != MILAN_PROTOCOL_ID[0:4] + MILAN_PROTOCOL_ID[5:6]:\n",
     "the @26 compare (RTL: pid_lo_r[1])"),
    ("pid_only_27", MODEL,
     "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n",
     "    if cmd_payload[3:4] != MILAN_PROTOCOL_ID[5:6]:\n",
     "40 of the 48 protocol_id bits: only @27 compared"),
    ("pid_27_dropped", MODEL,
     "    if raw_ct + cmd_payload[0:4] != MILAN_PROTOCOL_ID:\n",
     "    if raw_ct + cmd_payload[0:3] != MILAN_PROTOCOL_ID[0:5]:\n",
     "the @27 compare (RTL: pid_lo_r[0])"),
    ("served_as_echo", MODEL,
     '            program, echo = "MVU", False\n',
     '            program, echo = "MVU", True\n',
     "the served program emitted at the command's length"),
]


def build_tree(clone: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for entry in clone.iterdir():
        if entry.name in (".git", "tests"):
            continue
        os.symlink(entry, dest / entry.name)
    shutil.copytree(clone / "tests", dest / "tests",
                    ignore=shutil.ignore_patterns("__pycache__"))


def apply(dest: Path, rel: str, old: str, new: str) -> None:
    path = dest / rel
    text = path.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise SystemExit("arm substitution matches %d times in %s: %r" % (n, rel, old))
    path.write_text(text.replace(old, new), encoding="utf-8")


def run_feature(dest: Path) -> tuple[int, str]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(["behave", "--no-capture", "-f", "plain", FEATURE],
                       cwd=dest / "tests", env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=600)
    return p.returncode, p.stdout


def failing_scenarios(out: str) -> list[str]:
    fails, cur = [], None
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("Scenario"):
            cur = s
        if (" ... failed" in s or " ... error" in s or "undefined" in s) and cur:
            fails.append(cur)
            cur = None
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True, type=Path)
    ap.add_argument("--scratch", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    lines = []
    for name, rel, old, new, what in ARMS:
        dest = a.scratch / name
        build_tree(a.clone.resolve(), dest)
        if rel:
            apply(dest, rel, old, new)
        rc, out = run_feature(dest)
        tail = [l for l in out.splitlines() if "scenarios passed" in l]
        verdict = ("GREEN" if rc == 0 else "RED") if name == "baseline" else \
                  ("SURVIVED" if rc == 0 else "KILLED")
        lines.append("%-24s %-8s rc=%d %s | %s" % (name, verdict, rc,
                                                   tail[0].strip() if tail else "?", what))
        for f in failing_scenarios(out):
            lines.append("    fails: " + f)
        (a.scratch / (name + ".log")).write_text(out, encoding="utf-8")
    a.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
