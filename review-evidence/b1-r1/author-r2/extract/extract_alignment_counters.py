#!/usr/bin/env python3
"""Reproduce the #387 page's standalone alignment-test claim.

Claim (docs/findings/387_SOFTWARE_GM_STEP.md, stimulus): for about 2 s the
aligning port held a clockClass-255 master role; a standalone test confirmed
that this role changed no grandmaster; the DUT's and the peer's
GPTP_GM_CHANGED stayed at 22 and 60.

The test ran between cycle 10 and run 1, under its own bench-lock window.
Its window is read from the LOCK/UNLOCK lines of the packet's
r1/gm/slave-test.log. The counters come from three hash-checked controller
transcripts: the last poll of cycle10/controller.jsonl (before),
post-slave-test-snapshot.jsonl (after), and the first poll of
gm01/controller.jsonl (after run 1's own alignment phase, before its
takeover; the run's events.jsonl dates both).

AVB_INTERFACE GET_COUNTERS payload: descriptor type and index (4 bytes),
counters_valid (4 bytes), then 32 four-byte counters; IEEE 1722.1 places
LINK_UP at 0, LINK_DOWN at 1 and GPTP_GM_CHANGED at 5. GET_AVB_INFO carries
the grandmaster identity at bytes 4-11; it is printed by role only.

usage: extract_alignment_counters.py <raw-root> <repo-at-head>
"""
import datetime
import re
import sys

from b1r2_common import PACKET, Inputs, gm_role, jsonl


def utc(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%H:%M:%S.%fZ")[:-4] + "Z"


def avb_if_counters(payload):
    b = bytes.fromhex(payload)
    valid = int.from_bytes(b[4:8], "big")
    c = [int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big") for i in range(32)]
    return valid, c[0], c[1], c[5]


def snapshot(records, pick):
    """{role: (t, GM role, LINK_UP, LINK_DOWN, GPTP_GM_CHANGED)} from one poll per role."""
    out = {}
    for role in ("dut", "peer"):
        cnt = [r for r in records if r.get("role") == role and r.get("what") == "counter-9-0"]
        avb = [r for r in records if r.get("role") == role and r.get("what") == "avb"]
        rc, ra = pick(cnt), pick(avb)
        valid, up, down, gmc = avb_if_counters(rc["response"]["payload"])
        assert valid & 0x23 == 0x23, "LINK_UP, LINK_DOWN and GPTP_GM_CHANGED must be valid"
        gm = ra["response"]["payload"][8:24]
        out[role] = (rc["t"], gm_role(gm), up, down, gmc)
    return out


def controller_records(path):
    """Command answers only; ADP and carrier records carry no `what`."""
    return [r for r in jsonl(path) if "what" in r]


def main():
    inp = Inputs(sys.argv[1], sys.argv[2])
    log = (PACKET / "r1" / "gm" / "slave-test.log").read_text()
    lock = re.search(r"^LOCK (\S+)", log, re.M).group(1)
    unlock = re.search(r"^UNLOCK (\S+)", log, re.M).group(1)
    master = [x for x in log.splitlines() if "assuming the grand master role" in x or "selected best master clock" in x]
    print(f"standalone test window (r1/gm/slave-test.log): LOCK {lock} to UNLOCK {unlock}")
    for x in master:
        # keep the log's own timestamp and the event; the local clock identity is not printed
        m = re.match(r"\S+\[([\d.]+)\]: (?:port 1 \([^)]*\): )?(.*)", x)
        ev = m.group(2)
        if ev.startswith("selected best master clock"):
            ev = "selected best master clock " + ("switch" if ev.split()[-1] == "3cc0c6.fffe.fe0210" else "other")
        print(f"  log {m.group(1)}: {ev}")
    phases = [
        ("before: last poll of cycle10", controller_records(inp.path("cycle10/controller.jsonl")), lambda xs: xs[-1]),
        ("after: post-test snapshot", jsonl(inp.path("post-slave-test-snapshot.jsonl")), lambda xs: xs[0]),
        ("run 1: first poll of gm01", controller_records(inp.path("gm01/controller.jsonl")), lambda xs: xs[0]),
    ]
    ev = {e["kind"]: e["t"] for e in jsonl(inp.path("gm01/events.jsonl")) if e["kind"] != "clock"}
    print(f"run 1 events: alignment converged {utc(ev['gm-prep-converged'])}, offset applied "
          f"{utc(ev['gm-prep-offset'])}, takeover start {utc(ev['gm-start'])}")
    results = []
    for label, recs, pick in phases:
        s = snapshot(recs, pick)
        results.append(s)
        for role in ("dut", "peer"):
            t, gm, up, down, gmc = s[role]
            print(f"{label:30s} {role:4s} {utc(t)} GM {gm:8s} LINK_UP/DOWN {up}/{down} GPTP_GM_CHANGED {gmc}")
    same = all(r["dut"][4] == 22 and r["peer"][4] == 60 and r["dut"][1] == "switch" and r["peer"][1] == "switch"
               for r in results)
    print("CLAIM GPTP_GM_CHANGED stayed 22 (DUT) and 60 (peer), switch GM throughout:",
          "REPRODUCED" if same else "NOT REPRODUCED")
    sys.exit(0 if same else 1)


if __name__ == "__main__":
    main()
