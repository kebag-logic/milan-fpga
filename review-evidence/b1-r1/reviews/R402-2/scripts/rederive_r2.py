#!/usr/bin/env python3
"""Independent re-derivation of the round-2 claims on the two B1 findings pages.

Written without the author's extraction code. Reads the retained raw captures
(a directory laid out <action>/<file> plus top-level transcripts) and the
round-1 readbacks in the public author packet. Every raw input is first
matched by size and SHA-256 against the raw-artifact rows of the pages at the
reviewed head (when it has a row) and against the packet's raw index.

Never prints an identity other than the public switch, DUT and peer roles.

usage: rederive_r2.py <raw-root> <repo-at-head> <author-r2-packet-dir>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ACTIONS = (["dryrun", "bmsr-proof", "baseline-bound"] + [f"cycle{n:02d}" for n in range(1, 11)]
           + [f"gm{n:02d}" for n in range(1, 6)] + ["final"])
PAGES = ("docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md")
ROLE = {"alignment port log": "ptp4l-slave.log", "grandmaster port log": "ptp4l-gm.log"}
SWITCH = "3cc0c6fffefe0210"
MAC_CMD, LINK_CMD = "mem_read 0x90000110 4", "mem_read 0xf000181c 4"
READ_CMDS = {"GET_AVB_INFO", "GET_COUNTERS", "GET_CLOCK_SOURCE", "GET_CONFIGURATION",
             "READ_DESCRIPTOR", "GET_SAMPLING_RATE"}
FAILS = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        FAILS.append(label)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return [json.loads(x) for x in open(p) if x.strip()]


class Raw:
    def __init__(self, root, repo, packet):
        self.root = Path(root)
        self.rows = {}
        for page in PAGES:
            for m in re.finditer(r"^\| ([\w-]+) \| (`[^`]+`|alignment port log|grandmaster port log) \| (\d+) \| `([0-9a-f]{64})` \|$",
                                 (Path(repo) / page).read_text(), re.M):
                name = ROLE.get(m.group(2), m.group(2).strip("`"))
                self.rows[f"{m.group(1)}/{name}"] = (int(m.group(3)), m.group(4))
        idx = json.loads((Path(packet) / "r1" / "RAW-ARTIFACTS.json").read_text())
        self.index = {f["path"]: (f["bytes"], f["sha256"]) for f in idx["files"]}
        self.seen = set()

    def get(self, rel):
        p = self.root / rel
        got = (p.stat().st_size, sha(p))
        if rel not in self.seen:
            self.seen.add(rel)
            if got != self.index.get(rel) or (rel in self.rows and got != self.rows[rel]):
                print(f"INPUT MISMATCH {rel}")
                sys.exit(2)
        return p


def status(raw):
    return dict(re.findall(r"(\w+)=(\S+)", raw))


def word(raw):
    m = re.search(r"^0x[0-9a-f]{8}\s+((?:[0-9a-f]{2} ){4})", raw, re.M)
    return int("".join(reversed(m.group(1).split())), 16)


def role(gm):
    return {SWITCH: "switch", "020000fffe000001": "DUT"}.get(gm, "other")


def main():
    raw_root, repo, packet = sys.argv[1:4]
    R = Raw(raw_root, repo, packet)
    print(f"page raw rows parsed: {len(R.rows)}; packet raw index entries: {len(R.index)}")

    # A. console rounds and PP_STAT saved-state bits
    total = agree = 0
    samples = []
    for a in ACTIONS:
        recs = load(R.get(f"{a}/console.jsonl"))
        rounds = []
        for r in recs:
            if r["cmd"] == "milan_status":
                rounds.append({"t": r["t"], "st": status(r["raw"]), MAC_CMD: [], LINK_CMD: []})
            elif rounds and r["cmd"] in (MAC_CMD, LINK_CMD):
                rounds[-1][r["cmd"]].append(word(r["raw"]))
        ok = sum(1 for x in rounds if len(x[MAC_CMD]) == 1 and len(x[LINK_CMD]) == 1 and x[MAC_CMD] == x[LINK_CMD])
        total += len(rounds)
        agree += ok
        for x in rounds:
            samples.append((x["t"], int(x["st"]["PP_STAT"], 16), a))
    print(f"A. {len(ACTIONS)} actions, {total} console rounds, {agree} with one MAC_STATUS and one link_status read, equal")
    check(len(ACTIONS) == 19 and total == 7520 and agree == 7520, "599 page: both words agreed in all 7,520 console rounds of nineteen actions")
    samples.sort()
    pend0 = [t for t, p, _ in samples if not p >> 11 & 1]
    pend1 = [t for t, p, _ in samples if p >> 11 & 1]
    last0, first1 = max(pend0), min(pend1)
    import datetime
    z = lambda t: datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"   nvm_pend 0 up to {z(last0)}, 1 from {z(first1)}; pend never 0 after: {all(t < first1 for t in pend0)}")
    check(z(last0) == "05:38:28" and z(first1) == "05:41:15" and all(t < first1 for t in pend0),
          "599 page: nvm_pend 0 up to 05:38:29Z (bracket) and 1 from 05:41:16Z to the end")
    check(sum(p >> 8 & 1 for _, p, _ in samples) == 0 and sum(p >> 4 & 1 for _, p, _ in samples) == 0,
          "599 page: nvm_dirty 0 (and alarm 0) in all 7,520 samples")

    # B. every controller command in the session
    kinds = {}
    changing = []
    files = [f"{a}/controller.jsonl" for a in ACTIONS] + [
        "census-start-raw.jsonl", "setup-raw.jsonl", "post-slave-test-snapshot.jsonl", "restore-raw.jsonl",
        "census-end-raw.jsonl", "identity-aecp-raw.jsonl", "peer-config1-desc-raw.jsonl"]
    on_disk = sorted(str(p.relative_to(R.root)) for p in R.root.rglob("*.jsonl") if not p.name.startswith(("console", "events")))
    check(sorted(files) == on_disk, f"B. every retained controller transcript is enumerated ({len(on_disk)} files)")
    for f in files:
        for r in load(R.get(f)):
            if r.get("type") in ("adp", "carrier", "start"):
                continue
            resp = r.get("response", r)
            cmd = resp.get("cmd") if isinstance(resp, dict) else None
            what = r.get("what", "")
            if cmd is None and what.startswith("state-"):
                cmd = "GET_RX/TX_STATE"
            if cmd is None and what in ("acmp-6", "acmp-8"):
                cmd = {"acmp-6": "CONNECT_RX", "acmp-8": "DISCONNECT_RX"}[what]
            kinds[cmd] = kinds.get(cmd, 0) + 1
            if cmd not in READ_CMDS and cmd != "GET_RX/TX_STATE":
                changing.append((r["t"], f, r.get("role"), cmd, resp.get("payload") if cmd == "SET_CLOCK_SOURCE" else resp.get("conn_count")))
    print("   command kinds:", dict(sorted(kinds.items(), key=str)))
    for t, f, ro, c, extra in sorted(changing):
        print(f"   state-changing {z(t)}Z {f} {ro} {c} {extra}")
    exp = [("setup-raw.jsonl", "peer", "CONNECT_RX"), ("setup-raw.jsonl", "dut", "CONNECT_RX"),
           ("setup-raw.jsonl", "dut", "SET_CLOCK_SOURCE"), ("restore-raw.jsonl", "dut", "SET_CLOCK_SOURCE"),
           ("restore-raw.jsonl", "peer", "DISCONNECT_RX"), ("restore-raw.jsonl", "dut", "DISCONNECT_RX")]
    check(sorted((f, ro, c) for _, f, ro, c, _ in changing) == sorted(exp)
          and all(last0 < t < first1 for t, f, *_ in changing if f == "setup-raw.jsonl"),
          "599 page: six state-changing commands, three in the setup between the pend samples, three in the restore; every other command a read")

    # C. peer delay at the asCapable clears
    tk, rl, other, holds = [], [], [], []
    for n in range(1, 6):
        run = f"gm{n:02d}"
        t0 = next(e["t"] for e in load(R.get(f"{run}/events.jsonl")) if e["kind"] == "gm-start")
        st = [(r["t"] - t0, status(r["raw"])) for r in load(R.get(f"{run}/console.jsonl")) if r["cmd"] == "milan_status"]
        ac = [int(s["ASCAPABLE"]) for _, s in st]
        pd = [int(s["PDELAY_NS"]) for _, s in st]
        clears = [i for i in range(1, len(st)) if ac[i - 1] == 1 and ac[i] == 0]
        spec = set()
        for k, i in enumerate(clears):
            j = i
            while j < len(pd) and pd[j] == pd[i]:
                spec.add(j)
                j += 1
            holds.append(j - i)
            (tk if k == 0 else rl).append(pd[i])
        other += [pd[i] for i in range(len(pd)) if i not in spec]
        print(f"   {run}: asCapable clears at {[round(st[i][0], 2) for i in clears]} s, PDELAY_NS there {[pd[i] for i in clears]}")
    print(f"C. takeover {tk}, release {rl}, holds {holds} samples, other {len(other)} samples {min(other)}-{max(other)} ns")
    check(tk == [0] * 5 and min(rl) == 4039 and max(rl) == 4701 and min(other) == 373 and max(other) == 389
          and set(holds) <= {4, 5}, "387 page: 0 ns at takeovers, 4,039-4,701 ns at releases, 373-389 ns elsewhere, held 4-5 samples")

    # D. DUT GPTP_GM_CHANGED per edge
    per_edge = []
    for n in range(1, 6):
        run = f"gm{n:02d}"
        ev = {e["kind"]: e["t"] for e in load(R.get(f"{run}/events.jsonl")) if e["kind"] != "clock"}
        polls = [(r["t"], r["response"]["counters"]["5"]) for r in load(R.get(f"{run}/controller.jsonl"))
                 if r.get("role") == "dut" and r.get("what") == "counter-9-0"]
        mid = ev["gm-start"] + 27.0
        v0 = polls[0][1]
        vm = min(polls, key=lambda p: abs(p[0] - mid))[1]
        v1 = polls[-1][1]
        per_edge += [vm - v0, v1 - vm]
        print(f"   {run}: DUT GPTP_GM_CHANGED {v0} -> {vm} (27 s after start) -> {v1}")
    print(f"D. per-edge DUT GPTP_GM_CHANGED deltas {per_edge}")
    check(sorted(per_edge) == [1] + [3] * 9, "387 page: DUT GPTP_GM_CHANGED +3 at nine of ten edges and +1 at the tenth")

    # E. alignment-test counters
    def snap(recs, pick):
        out = {}
        for ro in ("dut", "peer"):
            c = [r for r in recs if r.get("role") == ro and r.get("what") == "counter-9-0"]
            a = [r for r in recs if r.get("role") == ro and r.get("what") == "avb"]
            out[ro] = (pick(c)["response"]["counters"]["5"], role(pick(a)["response"]["decoded"]["gm"]))
        return out
    snaps = [snap(load(R.get("cycle10/controller.jsonl")), lambda x: x[-1]),
             snap(load(R.get("post-slave-test-snapshot.jsonl")), lambda x: x[0]),
             snap(load(R.get("gm01/controller.jsonl")), lambda x: x[0])]
    print(f"E. before / after the standalone test / run 1 first poll: {snaps}")
    check(all(s == {"dut": (22, "switch"), "peer": (60, "switch")} for s in snaps),
          "387 page: DUT and peer GPTP_GM_CHANGED stayed 22 and 60 across the standalone test")

    # F. saved-state readbacks in the packet
    for rel, want in (("identity/console-identity.txt", ("227", "228", "228", "0", "0", "c30000e4", "0", "5b000444")),
                      ("restore/console-final.txt", ("229", "230", "230", "2", "0", "c34000e4", "1", "5b000c44"))):
        t = (Path(packet) / "r1" / rel).read_text()
        m = re.search(r"slot A \w+ seq (\d+), slot B \w+ seq (\d+), .*image seq (\d+)", t)
        c = re.search(r"commits ok=(\d+) failed=(\d+)", t)
        s = re.search(r"PP_NVM_STAT=([0-9a-f]{8}) .* pend=(\d) unres=(\d)", t)
        pp = re.search(r"PP_STAT=([0-9a-f]{8})", t)
        got = m.groups() + c.groups() + (s.group(1), s.group(2), pp.group(1))
        print(f"F. {rel}: slots {got[0]}/{got[1]} image {got[2]}, commits {got[3]}/{got[4]}, PP_NVM_STAT {got[5]} pend {got[6]} unres {s.group(3)}, PP_STAT {got[7]}")
        check(got == want, f"saved-state table column from r1/{rel}")
        nv = int(got[5], 16)
        check(nv >> 22 & 1 == int(got[6]) and (int(got[7], 16) >> 11 & 1) == int(got[6]),
              f"PP_NVM_STAT[22] and PP_STAT[11] agree with the printed pend in r1/{rel}")
    print(f"\nTOTAL fail={len(FAILS)}")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
