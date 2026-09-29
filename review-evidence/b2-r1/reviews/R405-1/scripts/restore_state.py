#!/usr/bin/env python3
"""Reviewer checks of the restore, saved-state, reset-epoch, console and host-clock claims.

usage: restore_state.py <packet author dir>
Reads console transcripts, controller census/snapshot JSONL and action transcripts only.
"""
import json, re, sys
from pathlib import Path

A = Path(sys.argv[1]); fails = []
SID = "0200000000010001"


def check(c, m):
    print(("OK   " if c else "FAIL ") + m)
    if not c:
        fails.append(m)


# --- saved-state layer: every milan_nvm read in the packet, in file order
print("# saved-state layer (milan_nvm) reads")
nvm = []
for f in sorted(A.rglob("console*.txt")) + sorted(A.rglob("*.stdout")):
    t = f.read_text(errors="replace")
    for m in re.finditer(r"^### (\S+) cmd='milan_nvm'[^\n]*\n(?:milan_nvm\n)?(NVM: slot[^\n]*)\n(NVM: PP_NVM_STAT[^\n]*)\n", t, re.M):
        nvm.append((m[1], str(f.relative_to(A)), m[2].strip(), m[3].strip()))
for x in nvm:
    print(" ", x[0], x[1]); print("    ", x[2]); print("    ", x[3])
check(len(nvm) >= 2, f"{len(nvm)} milan_nvm reads found")
if nvm:
    check(nvm[0][2:] == nvm[-1][2:], "first and last saved-state reads identical (slots, sequences, records, pend, commit counts)")
    pend = [re.search(r" pend=(\d)", x[3])[1] for x in nvm]
    print("  nvm pend values:", pend)
# PP_STAT nvm_pend (bit 11) across every milan_status read
pp = []
for f in sorted(A.rglob("console*.txt")):
    for m in re.finditer(r"PP_STAT=([0-9a-f]{8})", f.read_text(errors="replace")):
        pp.append(int(m[1], 16))
print(f"  PP_STAT reads: {len(pp)}, distinct: {sorted({hex(v) for v in pp})}, nvm_pend bit11 values: {sorted({(v >> 11) & 1 for v in pp})}")
check(len({(v >> 11) & 1 for v in pp}) == 1, "PP_STAT nvm_pend bit constant over every console sample")

# --- reset epoch and console predicate over every action
print("# reset epoch and console predicate")
eps, sync_bad = set(), []
for an in sorted(A.rglob("analysis.json")):
    a = json.loads(an.read_text())
    eps.update(a["rst_epoch_before_after"])
for f in sorted(A.rglob("console-*.txt")):
    for m in re.finditer(r"SYNC=(\d) ASCAPABLE=(\d) TU=(\d)", f.read_text(errors="replace")):
        if m.groups() != ("1", "1", "0"):
            sync_bad.append(str(f.relative_to(A)))
check(eps == {1}, f"reset epoch over every action before/after: {sorted(eps)}")
check(not sync_bad, f"every console sample reads SYNC=1 ASCAPABLE=1 TU=0 ({len(sync_bad)} exceptions)")

# --- census comparison, recomputed
print("# census start/end")
def census(p):
    out = {}
    for l in p.read_text().splitlines():
        x = json.loads(l)
        out[(x.get("role"), x.get("what"))] = x.get("response")
    return out
cs, ce = census(A / "restore/census-start.jsonl"), census(A / "restore/census-end.jsonl")
check(set(cs) == set(ce), f"same {len(cs)} census keys")
noncounter = [k for k in cs if not str(k[1]).startswith("counter")]
def strip(r):
    # GET_AVB_INFO bytes 12-15 are the measured propagation delay (a measurement, not a setting)
    if not isinstance(r, dict):
        return r
    r = {k: v for k, v in r.items() if k not in ("seq", "rtt_ms", "t", "decoded")}
    if r.get("cmd") == "GET_AVB_INFO":
        r["payload"] = r["payload"][:24] + "********" + r["payload"][32:]
    return r
diff = [k for k in noncounter if strip(cs[k]) != strip(ce[k])]
print(f"  non-counter reads {len(noncounter)}, differing {diff}; GET_AVB_INFO pdelay start/end: {cs[('dut', 'avb')]['decoded']['pdelay_ns']} / {ce[('dut', 'avb')]['decoded']['pdelay_ns']} ns")
check(len(noncounter) == 53 and not diff, "53 non-counter census reads equal")
states = [k for k in ce if str(k[1]).startswith("state-")]
cc = {k: ce[k].get("conn_count") for k in states}
check(len(states) == 18 and all(v == 0 for v in cc.values()), f"{len(states)} stream states at end, all connection count 0")
check(all(cs[k].get("conn_count") == 0 for k in states), "all 18 stream states also unbound at start")

# --- host-clock intervals (controller host) for the bind/unbind sequence
print("# host-clock intervals")
def tx(d, name, mt):
    for l in (A / "bind" / d / f"{name}.jsonl").read_text().splitlines():
        x = json.loads(l)
        if x.get("kind") == "transaction" and x["mt"] == mt:
            return x["start"], x["end"]
for n in range(1, 5):
    b = tx(f"bind-{n}", "bind", 6); u = tx(f"unbind-{n}", "unbind", 8); nb = tx(f"bind-{n + 1}", "bind", 6)
    print(f"  unbind {n}: command {u[0] - b[1]:.4f} s after bind {n} response; bind {n + 1}: {nb[0] - u[1]:.1f} s unbound")
page_after = ["25.7", "7.9", "7.9", "8.1"]; page_unb = ["39.3", "36.9", "37.0", "36.9"]
check([f"{tx(f'unbind-{n}', 'unbind', 8)[0] - tx(f'bind-{n}', 'bind', 6)[1]:.1f}" for n in range(1, 5)] == page_after, "unbind 'after bind response' column")
check([f"{tx(f'bind-{n + 1}', 'bind', 6)[0] - tx(f'unbind-{n}', 'unbind', 8)[1]:.1f}" for n in range(1, 5)] == page_unb, "bind 'unbound before' column")

# --- DUT MSRP refresh spacing in baseline and final
print("# DUT MSRP spacing (baseline/final)")
for w in ("baseline", "final"):
    ts = sorted({float(l.split("\t")[0]) for l in (A / "bind" / w / "msrp.tsv").read_text().splitlines()[1:] if l.split("\t")[1] == "DUT"})
    gaps = [round(b - a, 3) for a, b in zip(ts, ts[1:])]
    print(f"  {w}: {len(ts)} DUT MRPDUs, gaps {sorted(set(gaps))}")
    an = json.loads((A / "bind" / w / "analysis.json").read_text())
    if w == "final":
        check(an["target_valid_pdus"] == 0 and an["target_invalid_or_misdirected"] == 0 and an["crft_count_before_after"][0] == an["crft_count_before_after"][1],
              "final capture: no target CRF PDU and the DUT CRF transmit count did not move")
ra = json.loads((A / "bind/unbind-restore/analysis.json").read_text())
check(ra["pdus_after_lv_plus_period"] == 0 and ra["result"] == "SETTLED" and ra["dut_out1_start_stop_delta"] == [0, 1], "restore unbind stopped within one PDU, STOP +1")
print("\nFAILURES:", len(fails))
for f in fails:
    print("  ", f)

# --- appendix: DUT MRPDU cadence; short gaps must belong to a LeaveAll round (LeaveAll + join-period follow-ups)
print("# DUT MRPDU cadence detail")
for w in ("baseline", "final"):
    allrows = [l.split("\t") for l in (A / "bind" / w / "msrp.tsv").read_text().splitlines()[1:]]
    rows = [r for r in allrows if r[1] == "DUT"]
    ts = sorted({float(r[0]) for r in rows}); la = sorted({float(r[0]) for r in allrows if r[3] == "LeaveAll"})
    ph = sorted({round((t - ts[0]) % 1.0, 3) % 1.0 for t in ts})
    short = [(round(a, 3), round(b - a, 3)) for a, b in zip(ts, ts[1:]) if round(b - a, 3) < 1.0]
    off = [t for t in ts if round((t - ts[0]) % 1.0, 3) % 1.0 != 0.0]
    tied = all(any(0 <= t - l <= 0.25 for l in la) for t in off)
    print(f"  {w}: off-grid DUT MRPDUs {[round(t, 3) for t in off]}")
    print(f"  {w}: LeaveAll PDUs at {[round(x, 3) for x in la]}; phases of all DUT MRPDUs mod 1 s {ph}; short gaps {short}; every off-grid DUT MRPDU is a LeaveAll or within one join period (0.25 s) after one, either sender: {tied}")
    check(tied, f"{w}: DUT refresh on a 1.000 s grid; off-grid MRPDUs only in LeaveAll rounds")
    periodic = [t for t in ts if round((t - ts[0]) % 1.0, 3) % 1.0 == 0.0]
    print(f"  {w}: MRPDUs on the 1.000 s grid: {len(periodic)} of {len(ts)}")
