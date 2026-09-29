#!/usr/bin/env python3
"""R405-2: independent re-derivation of the saved-state layer claims on the
#606 and #608/#75 pages from the archived B2 author packet (console captures,
ACMP tables, controller snapshots).  Usage: r405_saved_state.py <author-dir>"""
import collections, glob, json, os, re, sys

root = sys.argv[1]
PP_STAT_ADDR, PP_NVM_STAT_ADDR = 0x90000924, 0x9000093C

def sections(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"^### (\S+) cmd='([^']*)'[^\n]*\n(.*?)(?=^### |\Z)", txt, re.S | re.M):
        yield m.group(1), m.group(2), m.group(3)

consoles = sorted(p for p in glob.glob(os.path.join(root, "**", "console*.txt"), recursive=True))
print("console .txt files:", len(consoles))
ppstat = collections.Counter(); nvm = []; addrs = collections.Counter(); action_ts = []
status_samples = 0
for p in consoles:
    rel = os.path.relpath(p, root)
    for ts, cmd, body in sections(p):
        if cmd == "milan_status":
            status_samples += 1
            m = re.search(r"PP_STAT=([0-9a-f]{8})", body); ppstat[m.group(1)] += 1
        elif cmd == "milan_nvm":
            nvm.append((ts, rel, " | ".join(l.strip() for l in body.splitlines() if l.startswith("NVM:"))))
        elif cmd.startswith("mem_read"):
            addrs[int(cmd.split()[1], 16)] += 1
        if rel.startswith(("bind/", "cycles/")):
            action_ts.append(ts)
print("milan_status samples:", status_samples)
print("PP_STAT values:", dict(ppstat))
for v in ppstat:
    x = int(v, 16)
    print(f"  {v}: alarm[4]={x>>4&1} backed[6]={x>>6&1} dirty[8]={x>>8&1} stale[9]={x>>9&1} img_valid[10]={x>>10&1} pend[11]={x>>11&1} tag={x>>24:#x}")
print("milan_nvm reads:", len(nvm))
for ts, rel, line in nvm:
    print("  ", ts, rel, "::", line)
print("mem_read addresses:", {hex(a): n for a, n in sorted(addrs.items())})
print("PP_STAT (0x924) read by mem_read:", addrs.get(PP_STAT_ADDR, 0), " PP_NVM_STAT (0x93c) read by mem_read:", addrs.get(PP_NVM_STAT_ADDR, 0))
print("action console samples (bind/ + cycles/ files):", len([p for p in consoles if os.path.relpath(p, root).startswith(("bind/", "cycles/"))]),
      " first/last section ts:", min(action_ts), max(action_ts))

# ACMP commands on the tap: count controller commands by message type
MT = {0: "CONNECT_TX_CMD", 1: "CONNECT_TX_RSP", 2: "DISCONNECT_TX_CMD", 3: "DISCONNECT_TX_RSP", 4: "GET_TX_STATE_CMD",
      5: "GET_TX_STATE_RSP", 6: "CONNECT_RX_CMD", 7: "CONNECT_RX_RSP", 8: "DISCONNECT_RX_CMD", 9: "DISCONNECT_RX_RSP",
      10: "GET_RX_STATE_CMD", 11: "GET_RX_STATE_RSP", 12: "GET_TX_CONNECTION_CMD", 13: "GET_TX_CONNECTION_RSP"}
cnt = collections.Counter(); targets = collections.Counter()
for p in sorted(glob.glob(os.path.join(root, "**", "acmp.tsv"), recursive=True)):
    rows = [l.rstrip("\n").split("\t") for l in open(p)][1:]
    for r in rows:
        mt = int(r[2]); cnt[MT.get(mt, mt)] += 1
        if mt in (6, 8):
            targets[(MT[mt], r[5], r[6], r[7], r[8])] += 1
print("ACMP message types on the tap:", dict(cnt))
for k, v in sorted(targets.items()): print("  ", k, v)

# AECP commands issued by the controller: every "cmd" in every jsonl response
aecp = collections.Counter(); polls = 0; in_cc = collections.Counter()
for p in sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)):
    for line in open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line.startswith("{"): continue
        try: d = json.loads(line)
        except Exception: continue
        r = d.get("response")
        if isinstance(r, dict) and "cmd" in r:
            aecp[r["cmd"]] += 1
        w = d.get("what", "")
        if d.get("role") == "dut" and re.fullmatch(r"state-5-\d+", w or "") and isinstance(r, dict):
            polls += 1; in_cc[(w, r.get("conn_count"))] += 1
print("AECP/ACMP-controller command names in jsonl:", dict(aecp))
print("DUT stream-input state polls:", polls, dict(in_cc))
