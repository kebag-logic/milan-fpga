#!/usr/bin/env python3
"""B16c dry run (offline): a stand-in for b8_ctl.py's agent with the same JSON line protocol, holding a model of
both entities' formats, binds and clock sources. Every state-changing request is appended to ops.jsonl (the order
under test). Fault injection by environment: FAKE_REFUSE_DUT_SET=1 (the DUT's SET_CLOCK_SOURCE refused),
FAKE_DIE_AT_BIND=1 (the agent ends, unanswered, at the first bind of the DUT's STREAM_INPUT 0),
FAKE_PEER_CLK0=<k> (the peer's as-found clock source)."""
import json
import os
import sys
import time

D = os.environ["FAKE_DIR"]
DUT = "020000fffe000001"
st_path = os.path.join(D, "model.json")
if os.path.exists(st_path):
    M = json.load(open(st_path))
else:
    M = dict(clk={"dut": 0, "peer": int(os.environ.get("FAKE_PEER_CLK0", "1"))},
             fmt={"dut-in-0": "0205022001006000", "dut-in-1": "041060010000bb80", "peer-in-0": "0205022002006000",
                  "peer-out-0": "0205022001006000", "peer-out-2": "041060010000bb80", "dut-out-0": "0205022002006000"},
             rx={"dut-0": None, "dut-1": None, "peer-0": [DUT, 0], "peer-8": [DUT, 1]}, set_t=None)


def save():
    json.dump(M, open(st_path, "w"))


def emit(o):
    sys.stdout.write(json.dumps(o) + "\n")
    sys.stdout.flush()


def op_log(**kw):
    with open(os.path.join(D, "ops.jsonl"), "a") as f:
        f.write(json.dumps(dict(t=time.time(), **kw)) + "\n")


def rxrow(who, i, what="rx"):
    b = M["rx"].get(f"{who}-{i}")
    if b:
        return dict(what=what, status=0, conn_count=1, stream_id="0200000000010000" if b[0] == DUT else "1111111111110000",
                    talker=b[0], talker_uid=b[1], flags="0x0082", dmac="91e0f000dd85")
    return dict(what=what, status=0, conn_count=0, stream_id="0000000000000000", talker="0000000000000000",
                talker_uid=0, flags="0x0000", dmac="000000000000")


save()
emit(dict(type="agent-ready"))
for line in sys.stdin:
    q = json.loads(line)
    op = q["op"]
    emit(dict(type="req", req=q))
    if op == "fmt":
        k = f"{q['who']}-{q['dir']}-{q['idx']}"
        emit(dict(status="SUCCESS", cmd="GET_STREAM_FORMAT", payload="00050000" + M["fmt"].get(k, "0205022001006000")))
    elif op == "setfmt":
        M["fmt"][f"{q['who']}-in-{q['idx']}"] = q["fmt"]
        op_log(op="setfmt", who=q["who"], idx=q["idx"], fmt=q["fmt"])
        emit(dict(status="SUCCESS", cmd="SET_STREAM_FORMAT", payload="00050000" + q["fmt"]))
    elif op in ("bind", "unbind"):
        lw = "dut" if q["l"] == DUT else "peer"
        if (os.environ.get("FAKE_DIE_AT_BIND") == "1" and op == "bind" and lw == "dut" and q["lu"] == 0
                and not os.path.exists(os.path.join(D, "died"))):
            open(os.path.join(D, "died"), "w").close()
            save()
            sys.exit(3)     # the agent ends without a reply (a dropped session)
        M["rx"][f"{lw}-{q['lu']}"] = [q["t"], q["tu"]] if op == "bind" else None
        op_log(op=op, talker=q["t"][:6], tu=q["tu"], l=lw, lu=q["lu"])
        emit(dict(what=op, status=0))
        emit(rxrow(lw, q["lu"], "rx-state-after"))
    elif op == "rx":
        emit(rxrow(q["who"], q["idx"]))
    elif op == "tx":
        emit(dict(what="tx", status=0, conn_count=1, stream_id="1111111111110000", talker="x", talker_uid=0, flags="0x0", dmac="x"))
    elif op == "map":
        emit(dict(status="SUCCESS", payload=("000e000000000001000400000000000000000000000000010001000000000002000200000000000300030000"
                                             if q["dtype"] == 0x000E else
                                             "000f00000000000100080000" + "".join("0000%04x%04x0000" % (c, c) for c in range(8)))))
    elif op == "counters":
        emit(dict(status="SUCCESS", payload="00050000" + "00000001" + "".join("%08x" % (i + 1) for i in range(32))))
    elif op == "clk":
        emit(dict(what=f"clock-{q['who']}", status="SUCCESS", payload="00240000%04x" % M["clk"][q["who"]]))
    elif op == "setclk":
        refused = q["who"] == "dut" and os.environ.get("FAKE_REFUSE_DUT_SET") == "1" and q["src"] != 0
        if not refused:
            M["clk"][q["who"]] = q["src"]
            if q["who"] == "dut":
                M["set_t"] = time.time()
        op_log(op="setclk", who=q["who"], src=q["src"], refused=refused)
        emit(dict(cmd="SET_CLOCK_SOURCE", status="NOT_SUPPORTED" if refused else "SUCCESS",
                  what=f"set-clock-{q['who']}-{q['src']}", payload="00240000%04x" % M["clk"][q["who"]]))
        emit(dict(what=f"clock-{q['who']}", status="SUCCESS", payload="00240000%04x" % M["clk"][q["who"]]))
    elif op == "quit":
        save()
        break
    save()
    emit(dict(type="done", op=op))
emit(dict(type="agent-exit"))
