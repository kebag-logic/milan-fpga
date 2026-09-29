#!/usr/bin/env python3
"""R405-4: full command census of the archived B2 controller transcripts.

Independent of the labels the controller wrote into "what": the AECP command
is taken from response.cmd and the addressed descriptor from the payload
(GET_COUNTERS: type,index at bytes 0-3; READ_DESCRIPTOR: type,index at
bytes 4-7); the ACMP message type from the paired transaction record where
present, otherwise from the "what" label, and the addressed listener/talker
from the response fields.

Checks the round-4 wording:
  - no state-changing command addressed a DUT stream input;
  - the 210 CONNECT_RX and DISCONNECT_RX went to the reference peer;
  - every AECP command was a GET_ or READ_;
  - commands that addressed a DUT stream input: 228 GET_RX_STATE,
    228 GET_COUNTERS, 4 READ_DESCRIPTOR, all reads.
Also reports the ACMP command total (for the PR body's "210 ACMP commands").

Usage: r405_4_census.py <author-dir> <MANIFEST.json>
Exit 0 only if every expectation holds."""
import collections, glob, hashlib, json, os, sys

root, manifest = sys.argv[1], sys.argv[2]
DUT, PEER = "020000fffe000001", "3cc0c60102030000"
ACMP_NAMES = {0: "CONNECT_TX", 2: "DISCONNECT_TX", 4: "GET_TX_STATE", 6: "CONNECT_RX",
              8: "DISCONNECT_RX", 10: "GET_RX_STATE", 12: "GET_TX_CONNECTION"}
ACMP_READS = {"GET_TX_STATE", "GET_RX_STATE", "GET_TX_CONNECTION"}
fails = []

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# 1. archive integrity against the published manifest
m = json.load(open(manifest))
entries = m if isinstance(m, list) else m.get("files", m)
pub = {}
def walk(x):
    if isinstance(x, dict):
        k = x.get("path") or x.get("file")
        if k and "published_sha256" in x:
            pub[k] = x["published_sha256"]
        for v in x.values(): walk(v)
    elif isinstance(x, list):
        for v in x: walk(v)
walk(m)
files = sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True))
ok = bad = unlisted = 0
for p in files:
    rel = os.path.relpath(p, root)
    key = next((k for k in pub if k.endswith("/author/" + rel) or k == rel or k.endswith("author/" + rel)), None)
    if key is None: unlisted += 1
    elif pub[key] == sha(p): ok += 1
    else: bad += 1
print(f"jsonl files {len(files)}: published_sha256 equal {ok}, differ {bad}, not in manifest {unlisted}")
if bad or unlisted or len(files) != 561: fails.append("archive integrity")

# 2. copies excluded: snapshot.jsonl must be a byte copy of snapshot-after.jsonl
copies = [p for p in files if os.path.basename(p) == "snapshot.jsonl"]
noncopy = [p for p in copies if not os.path.exists(os.path.join(os.path.dirname(p), "snapshot-after.jsonl"))
           or sha(p) != sha(os.path.join(os.path.dirname(p), "snapshot-after.jsonl"))]
print(f"snapshot.jsonl copies {len(copies)}, not a byte copy of snapshot-after.jsonl: {len(noncopy)}")
if noncopy: fails.append("copies")
counted = [p for p in files if os.path.basename(p) != "snapshot.jsonl"]

# 3. classify every record
cmds = []            # (file-kind, protocol, name, entity, target-kind, index)
other = collections.Counter()
txn = collections.Counter()
actions = collections.Counter()
for p in counted:
    base = os.path.basename(p)
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("{"):
            other[(base, "non-json")] += 1; continue
        d = json.loads(line)
        if d.get("kind") == "transaction":
            r = d["response"]; txn[(ACMP_NAMES.get(d["mt"], d["mt"]), r.get("listener"), r.get("listener_uid"))] += 1
            continue
        if d.get("type") == "aem" and "cmd" in d:        # identity AECP reads (no role field)
            name = d["cmd"]; pl = bytes.fromhex(d.get("payload", ""))
            tk, ix = (int.from_bytes(pl[4:6], "big"), int.from_bytes(pl[6:8], "big")) if name == "READ_DESCRIPTOR" and len(pl) >= 8 else (None, None)
            cmds.append((base, "AECP", name, d.get("target"), tk, ix, "identity"))
            continue
        if d.get("kind") == "controller":
            actions[d.get("action")] += 1; continue
        if "role" not in d:
            other[(base, d.get("type") or d.get("kind") or "?")] += 1; continue
        role, what, r = d["role"], d["what"], d["response"]
        ent = DUT if role == "dut" else PEER
        if "cmd" in r:                                   # AECP
            name = r["cmd"]; pl = bytes.fromhex(r.get("payload", ""))
            if name == "GET_COUNTERS" and len(pl) >= 4:
                tk, ix = int.from_bytes(pl[0:2], "big"), int.from_bytes(pl[2:4], "big")
            elif name == "READ_DESCRIPTOR" and len(pl) >= 8:
                tk, ix = int.from_bytes(pl[4:6], "big"), int.from_bytes(pl[6:8], "big")
            else:
                tk, ix = None, None
            cmds.append((base, "AECP", name, ent, tk, ix, what))
        else:                                            # ACMP
            if what.startswith("state-5-"):
                name, ent2, ix = "GET_RX_STATE", r.get("listener") or ent, int(what.split("-")[2])
                # response names the listener; for a failed read it may be zero
                ent2 = ent if ent2 in (None, "0000000000000000") else ent2
                cmds.append((base, "ACMP", name, ent2, 5, ix, what))
            elif what.startswith("state-6-"):
                cmds.append((base, "ACMP", "GET_TX_STATE", ent, 6, int(what.split("-")[2]), what))
            elif what.startswith("acmp-"):
                mt = int(what.split("-")[1]); name = ACMP_NAMES.get(mt, str(mt))
                cmds.append((base, "ACMP", name, r.get("listener"), 5, r.get("listener_uid"), what))
                if name == "CONNECT_RX" and not (r.get("talker") == DUT and r.get("talker_uid") == 1):
                    fails.append("CONNECT_RX talker not DUT output 1")
            else:
                other[(base, "unclassified:" + what)] += 1

print("non-command records by (file, type):", dict(other))
print("controller invocations logged in events.jsonl by action:", dict(actions))
if set(actions) - {"snapshot", "bind", "unbind", "cycle"}: fails.append("unexpected controller mode")
print("ACMP transaction records by (message, listener, listener_uid):", dict(txn))

by = collections.Counter((proto, name, "DUT" if ent == DUT else "PEER" if ent == PEER else ent, tk) for _, proto, name, ent, tk, ix, _ in cmds)
print("\ncommands by (protocol, command, entity, descriptor type):")
for k, v in sorted(by.items(), key=str): print("  ", k, v)

aecp_names = sorted({n for _, pr, n, *_ in cmds if pr == "AECP"})
print("\nAECP command names seen:", aecp_names)
if any(not (n.startswith("GET_") or n.startswith("READ_")) for n in aecp_names): fails.append("AECP non-read")

changing = [c for c in cmds if (c[1] == "ACMP" and c[2] not in ACMP_READS) or
            (c[1] == "AECP" and not (c[2].startswith("GET_") or c[2].startswith("READ_")))]
chg = collections.Counter((c[2], "DUT" if c[3] == DUT else "PEER" if c[3] == PEER else c[3], c[5]) for c in changing)
print("state-changing commands by (command, addressed entity, index):", dict(chg))
if chg != collections.Counter({("CONNECT_RX", "PEER", 8): 105, ("DISCONNECT_RX", "PEER", 8): 105}):
    fails.append("state-changing census")

dut_in = [c for c in cmds if c[3] == DUT and c[4] == 5]
di = collections.Counter(c[2] for c in dut_in)
print("commands addressed to a DUT stream input (descriptor type 5):", dict(di),
      "total", len(dut_in), "by index", dict(collections.Counter((c[2], c[5]) for c in dut_in)))
if di != collections.Counter({"GET_RX_STATE": 228, "GET_COUNTERS": 228, "READ_DESCRIPTOR": 4}):
    fails.append("DUT stream-input reads")
if [c for c in dut_in if c[2] not in ("GET_RX_STATE", "GET_COUNTERS", "READ_DESCRIPTOR")]:
    fails.append("DUT stream-input non-read")

acmp_all = collections.Counter((c[2], "DUT" if c[3] == DUT else "PEER") for c in cmds if c[1] == "ACMP")
print("\nACMP commands in total:", sum(acmp_all.values()), dict(acmp_all))
print("ACMP commands to the peer's input 8:", sum(1 for c in cmds if c[1] == "ACMP" and c[3] == PEER and c[4] == 5 and c[5] == 8))

# 4. wire cross-check: every ACMP command frame in the 112 action captures
wire = collections.Counter()
for p in sorted(glob.glob(os.path.join(root, "**", "acmp.tsv"), recursive=True)):
    for row in list(open(p))[1:]:
        f = row.rstrip("\n").split("\t")
        mt = int(f[2])
        if mt % 2 == 0:                                  # commands are even message types
            wire[(ACMP_NAMES.get(mt, mt), "DUT" if f[7] == DUT else "PEER" if f[7] == PEER else f[7], f[8],
                  "talker DUT" if f[5] == DUT else "talker PEER" if f[5] == PEER else "talker " + f[5], f[6])] += 1
print("\nwire (acmp.tsv, 112 action captures) ACMP command frames by (msg, listener, luid, talker, tuid):")
for k, v in sorted(wire.items(), key=str): print("  ", k, v)
bad_wire = {k: v for k, v in wire.items() if k[1] == "DUT" and k[0] not in ACMP_READS}
print("wire commands naming a DUT listener that are not reads:", bad_wire)
if bad_wire: fails.append("wire state-changing to DUT listener")

print("\nRESULT:", "PASS" if not fails else "FAIL " + ", ".join(fails))
sys.exit(1 if fails else 0)
