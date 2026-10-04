#!/usr/bin/env python3
"""Independent of the grader: from the provided decoder's published outputs,
rebuild (a) the line order of the UNBIND_RX response vs the first unsolicited
GET_COUNTERS for the input whose MUNLOCK exceeds every earlier one, and (b) the
intervals. The decoder prints (S - S0)/1e6 with S = lo*2^32 + hi (words swapped),
so for intervals under 2^32 ns the true interval is round(dS/2^32) mod 2^32 ns."""
import json, re, sys
from pathlib import Path
A = Path(sys.argv[1]); G = json.loads((A / "summary/o653-grade.json").read_text())
fails = 0
for k, v in G.items():
    if k.endswith("_session"): continue
    s, tag = k.split("/"); li = v["library"]["listener"]
    lines = (A / f"summary/decode/b11-a535-{s}-{tag}.decode.txt").read_text().splitlines()
    P = [(float(l.split(" ms ")[0]), l) for l in lines]
    ic = next(i for i, (_, l) in enumerate(P) if "ACMP UNBIND_RX_CMD" in l)
    ir = next(i for i, (_, l) in enumerate(P) if "ACMP UNBIND_RX_RESP" in l)
    mu = lambda l: int(re.search(r"MUNLOCK=(\d+)", l).group(1)) if "MUNLOCK=" in l else 0
    push = [i for i, (_, l) in enumerate(P) if "UNSOL GET_COUNTERS" in l and f"desc=0x5/{li} " in l + " "]
    before = max([mu(P[i][1]) for i in push if i < ic], default=0)
    iu = next(i for i in push if i > ic and mu(P[i][1]) > before)
    earlier_unsol_after_cmd = [i for i in push if ic < i < iu]
    order = "RESPONSE_FIRST" if ir < iu else "COUNTERS_FIRST"
    iv = lambda a, b: (round((P[b][0] - P[a][0]) * 1e6 / 2**32) % 2**32) / 1e3  # microseconds
    c2r, r2p = round(iv(ic, ir), 1), round(iv(ir, iu), 1)
    w = v["wire"]
    ok = order == w["order"] and c2r == w["cmd_to_rsp_us"] and abs(r2p - w["rsp_to_push_us"]) <= 0.1 and not earlier_unsol_after_cmd
    # the control: the probe's own solicited GET_COUNTERS response, ctl differs from the pushes
    extra = ""
    if "control" in w:
        io = next(i for i, (_, l) in enumerate(P) if "AECP RSP GET_COUNTERS" in l and "UNSOL" not in l)
        extra = f" own_rsp_line={io} rsp_line={ir} own->cmd={round(iv(io, ic),1)}us vs_own={'COUNTERS_FIRST' if io < ir else 'RESPONSE_FIRST'}"
        ok = ok and io < ir and round(iv(io, ic), 1) == w["control"]["own_rsp_to_cmd_us"]
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {k} order={order} cmd->rsp={c2r}us rsp->unlock={r2p}us pushed_MU={mu(P[iu][1])} before={before}{extra}")
print("FAILS", fails); sys.exit(1 if fails else 0)
