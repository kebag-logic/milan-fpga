#!/usr/bin/env python3
"""Audit the owner binding rule in each run's ctl.jsonl: before every bind a talker
(DUT STREAM_OUTPUT) and listener (peer STREAM_INPUT) format read; when they differ a
listener-only SET to the talker's format, read back equal; the talker never set; the
listener restored and read back after the last unbind.
usage: binding_rule_audit.py <run ctl.jsonl>..."""
import json, sys

FOUND = "0205022001006000"
bad_total = 0
for f in sys.argv[1:]:
    lines = [json.loads(l) for l in open(f)]
    talker = listener = None
    seen_t = seen_l = False
    pending_set = None
    binds = unbinds = 0
    sets = []
    bad = []
    last_unbind_i = None
    after_unbind_set = None
    after_unbind_read = None
    cur = None
    for i, o in enumerate(lines):
        rq = o.get("req")
        ln = o.get("line", {})
        if rq:
            cur = rq
            if rq.get("op") == "bind":
                binds += 1
                if not (seen_t and seen_l):
                    bad.append(f"bind {binds}: missing read (talker {seen_t}, listener {seen_l})")
                elif talker != listener:
                    bad.append(f"bind {binds}: formats differ at bind {talker} {listener}")
                if pending_set is not None:
                    bad.append(f"bind {binds}: set not read back")
                seen_t = seen_l = False
            if rq.get("op") == "unbind":
                unbinds += 1
                last_unbind_i = i
                after_unbind_set = after_unbind_read = None
            continue
        cmd = ln.get("cmd")
        if cmd == "GET_STREAM_FORMAT":
            dt = ln["payload"][0:4]; fmt = ln["payload"][8:24]
            if ln["role"] == "dut" and dt == "0006":
                talker, seen_t = fmt, True
            elif ln["role"] == "peer" and dt == "0005":
                listener, seen_l = fmt, True
                if pending_set is not None:
                    if fmt != pending_set:
                        bad.append(f"set {pending_set} read back {fmt}")
                    pending_set = None
                if last_unbind_i is not None and after_unbind_set is not None:
                    after_unbind_read = fmt
            else:
                bad.append(f"unexpected format read {ln['role']} {dt}")
        elif cmd == "SET_STREAM_FORMAT":
            dt = ln["payload"][0:4]; fmt = ln["payload"][8:24]
            sets.append((ln["role"], dt, fmt, ln["status"]))
            if ln["role"] != "peer" or dt != "0005":
                bad.append(f"SET on {ln['role']} dtype {dt}: talker or non-listener changed")
            if ln["status"] != "SUCCESS":
                bad.append(f"SET status {ln['status']}")
            pending_set = fmt
            if last_unbind_i is not None:
                after_unbind_set = fmt
        elif ln.get("what") in ("bind", "unbind") and "status" in ln:
            if ln["status"] != 0:
                bad.append(f"{ln['what']} status {ln['status']}")
            if ln["what"] == "bind" and ln.get("conn_count") != 1:
                bad.append(f"bind conn_count {ln.get('conn_count')}")
    if binds and (after_unbind_set != FOUND or after_unbind_read != FOUND):
        bad.append(f"restore after last unbind: set {after_unbind_set} read {after_unbind_read}")
    print(f"{f}: binds {binds} unbinds {unbinds} sets {sets} -> {'OK' if not bad else bad}")
    bad_total += len(bad)
sys.exit(1 if bad_total else 0)
