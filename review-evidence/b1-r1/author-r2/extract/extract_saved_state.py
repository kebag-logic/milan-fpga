#!/usr/bin/env python3
"""The DUT saved-state layer over the lane's session, from the captures.

Reads, in time order:
  * the identity-gate and final-restore console readbacks in this packet
    (r1/identity/console-identity.txt, r1/restore/console-final.txt), matched
    to the round-1 packet manifest r1/MANIFEST.sha256: the `milan_nvm`
    lines and PP_STAT;
  * every 250 ms PP_STAT sample of the nineteen hash-checked action consoles:
    [4] nvm_alarm, [6] nvm_backed, [8] nvm_dirty, [10] nvm_img_valid,
    [11] nvm_pend, [15:12] verdict (docs/reference/REGISTER_MAP.md, PP_STAT);
  * every hash-checked controller transcript, for the commands that can
    change saved state (ACMP CONNECT_RX / DISCONNECT_RX, message types 6 and
    8, and any AECP SET_ command), and for the DUT listener's binding as
    polled (stream input 1: talker, stream ID, destination, VLAN, count and
    flags; the controller field is not printed).

usage: extract_saved_state.py <raw-root> <repo-at-head>
"""
import datetime
import hashlib
import re
import sys

from b1r2_common import PACKET, Inputs, jsonl

ACTIONS = (["dryrun", "bmsr-proof", "baseline-bound"] + [f"cycle{n:02d}" for n in range(1, 11)]
           + [f"gm{n:02d}" for n in range(1, 6)] + ["final"])
OTHER_TRANSCRIPTS = ["census-start-raw.jsonl", "setup-raw.jsonl", "post-slave-test-snapshot.jsonl",
                     "restore-raw.jsonl", "census-end-raw.jsonl", "identity-aecp-raw.jsonl",
                     "peer-config1-desc-raw.jsonl"]
BINDING_KEYS = ("talker", "talker_uid", "stream_id", "dmac", "vlan", "conn_count", "flags")


def utc(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%H:%M:%S.%f")[:-4] + "Z"


def bits(pp):
    return dict(alarm=pp >> 4 & 1, backed=pp >> 6 & 1, dirty=pp >> 8 & 1, img_valid=pp >> 10 & 1,
                pend=pp >> 11 & 1, verdict=pp >> 12 & 0xF)


def readback(rel):
    p = PACKET / "r1" / rel
    man = dict(reversed(x.split(None, 1)) for x in (PACKET / "r1" / "MANIFEST.sha256").read_text().splitlines() if x.strip())
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    ok = man.get(rel) == digest
    print(f"READBACK r1/{rel} {digest} {'= round-1 manifest' if ok else 'MISMATCH round-1 manifest'}")
    if not ok:
        sys.exit(2)
    t = p.read_text()
    stamp = re.search(r"^### (\S+) cmd='milan_nvm'", t, re.M).group(1)
    pp = int(re.search(r"PP_STAT=([0-9a-f]{8})", t).group(1), 16)
    nvm = re.findall(r"^NVM: .*$", t, re.M)
    print(f"  milan_nvm at {stamp}; PP_STAT {pp:08x} {bits(pp)}")
    for x in nvm:
        print("  " + x)
    return t


def mutating(rec):
    """Return a short label when a controller record is a state-changing command."""
    what = rec.get("what", "")
    resp = rec.get("response") or {}
    cmd = resp.get("cmd", "") if isinstance(resp, dict) else ""
    if re.fullmatch(r"acmp-(6|8)", what) or cmd.startswith("SET_") or cmd in ("START_STREAMING", "STOP_STREAMING"):
        if cmd:
            return f"{rec.get('role')} {cmd} status {resp.get('status')} payload {resp.get('payload')}"
        kind = {"acmp-6": "CONNECT_RX", "acmp-8": "DISCONNECT_RX"}[what]
        return (f"{rec.get('role')} {kind} status {resp.get('status')}: listener uid {resp.get('listener_uid')} "
                f"talker uid {resp.get('talker_uid')} conn_count {resp.get('conn_count')}")
    return None


def main():
    inp = Inputs(sys.argv[1], sys.argv[2])
    print("== identity gate")
    first = readback("identity/console-identity.txt")
    timeline = []
    for rel in OTHER_TRANSCRIPTS:
        for r in jsonl(inp.path(rel)):
            m = mutating(r)
            if m:
                timeline.append((r["t"], rel, m))
    print("\n== actions: PP_STAT per 250 ms sample, and the controller's own commands")
    all_pp = set()
    dut_binding = {}
    samples = []
    for action in ACTIONS:
        rows = [r for r in jsonl(inp.path(f"{action}/console.jsonl")) if r["cmd"] == "milan_status"]
        pps = [int(re.search(r"PP_STAT=([0-9a-f]{8})", r["raw"]).group(1), 16) for r in rows]
        all_pp |= set(pps)
        samples += [(r["t"], p) for r, p in zip(rows, pps)]
        pend = sorted({bits(p)["pend"] for p in pps})
        dirty = sorted({bits(p)["dirty"] for p in pps})
        ctl = [r for r in jsonl(inp.path(f"{action}/controller.jsonl")) if "what" in r]
        muts = [mutating(r) for r in ctl if mutating(r)]
        whats = sorted({r["what"] for r in ctl})
        b = sorted({tuple(str(r["response"].get(k)) for k in BINDING_KEYS)
                    for r in ctl if r["role"] == "dut" and r["what"] == "state-5-1"
                    and r["response"].get("status") == 0})
        dut_binding[action] = b
        print(f"{action:15s} {utc(rows[0]['t'])}-{utc(rows[-1]['t'])} samples {len(pps):3d} "
              f"PP_STAT {sorted('%08x' % p for p in set(pps))} pend {pend} dirty {dirty}; "
              f"controller {len(ctl)} answers, labels {whats}, state-changing {len(muts)}")
    print("\nPP_STAT values over all samples:", sorted("%08x" % p for p in all_pp))
    for p in sorted(all_pp):
        print(f"  {p:08x} {bits(p)}")
    print("\n== state-changing controller commands in the other transcripts")
    for t, rel, m in sorted(timeline):
        print(f"{utc(t)} {rel}: {m}")
    print("\n== DUT stream input 1 as polled: distinct (talker, talker uid, stream ID, destination, VLAN,"
          " connection count, flags)")
    for action in ACTIONS:
        print(f"{action:15s} {dut_binding[action] if dut_binding[action] else 'not polled'}")
    print("\n== final restore")
    last = readback("restore/console-final.txt")
    seq0 = re.search(r"image seq (\d+)", first).group(1)
    seq1 = re.search(r"image seq (\d+)", last).group(1)
    ok0 = re.search(r"commits ok=(\d+) failed=(\d+)", first).groups()
    ok1 = re.search(r"commits ok=(\d+) failed=(\d+)", last).groups()
    print(f"\nimage seq {seq0} -> {seq1}; commits ok/failed {ok0[0]}/{ok0[1]} -> {ok1[0]}/{ok1[1]}; "
          f"state-changing commands: {len(timeline)}")
    samples.sort()
    last0 = max(t for t, p in samples if not bits(p)["pend"])
    first1 = min(t for t, p in samples if bits(p)["pend"])
    between = [m for t, _, m in timeline if last0 < t < first1]
    print(f"nvm_pend: 0 in every sample up to {utc(last0)}, 1 in every sample from {utc(first1)}; "
          f"never 0 after it: {all(bits(p)['pend'] for t, p in samples if t >= first1)}")
    print(f"  state-changing commands between those samples: {len(between)}")
    for m in between:
        print("    " + m)
    print(f"nvm_dirty (PP_STAT[8]) set in {sum(bits(p)['dirty'] for _, p in samples)} of {len(samples)} samples; "
          f"nvm_alarm set in {sum(bits(p)['alarm'] for _, p in samples)}; verdict nibble values "
          f"{sorted({bits(p)['verdict'] for _, p in samples})}")
    bound = [a for a in ACTIONS if dut_binding[a] and all(x[5] == "1" for x in dut_binding[a])]
    talkers = {(x[0], x[1], x[6]) for a in bound for x in dut_binding[a]}
    print(f"DUT stream input 1 bound (count 1) in every poll of {len(bound)} actions ({bound[0]} to {bound[-1]}); "
          f"talker, uid and flags over them: {sorted(talkers)}")


if __name__ == "__main__":
    main()
