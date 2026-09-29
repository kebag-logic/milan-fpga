#!/usr/bin/env python3
"""The DUT saved-state layer over lane B2's session, from the archived captures.

usage: saved_state_b2.py <round-1 packet author dir> <archive MANIFEST.json> <lane B1 page at 931c3edf>

Reads, from the round-1 packet (the archive's `author/` tree):
  * the two `milan_nvm` reads, at the identity gate
    (identity/console-identity.txt) and at the final restore
    (restore/console-final.txt): slots, image sequence, records, writer,
    PP_NVM_STAT and the commit counts;
  * the `milan_status` PP_STAT word of every console sample (the before and
    after read of every action, plus the two reads above), decoded per
    docs/reference/REGISTER_MAP.md `0x924`: [4] nvm_alarm, [6] nvm_backed,
    [8] nvm_dirty, [9] nvm_stale, [10] nvm_img_valid, [11] nvm_pend,
    [15:12] verdict;
  * every controller transcript (*.jsonl), for the commands that can change
    saved state (ACMP CONNECT_RX / DISCONNECT_RX, message types 6 and 8, and
    any AECP command other than a GET_ or READ_), and for every poll of the
    DUT's stream inputs (the sinks that index binding records 0x20-0x2F).

Every file read is checked against the archive MANIFEST.json: its sha256 must
equal the entry's original_sha256, and the receipt says whether the archived
(published) bytes are the same file or a redacted copy.

The lane B1 page supplies B1's final-restore column for the inherited-state
comparison. No identifier other than the DUT's own is printed.
"""
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

A = Path(sys.argv[1])
MAN = {e["file"]: e for e in json.load(open(sys.argv[2]))}
B1 = Path(sys.argv[3]).read_text()
READ = {}
FAILS = []


def check(ok, msg):
    print(("OK   " if ok else "FAIL ") + msg)
    if not ok:
        FAILS.append(msg)


def text(p):
    b = p.read_bytes()
    READ[p.relative_to(A).as_posix()] = hashlib.sha256(b).hexdigest()
    return b.decode(errors="replace")


def utc(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%H:%M:%S.%f")[:-4] + "Z"


def bits(pp):
    return dict(alarm=pp >> 4 & 1, backed=pp >> 6 & 1, dirty=pp >> 8 & 1, stale=pp >> 9 & 1,
                img_valid=pp >> 10 & 1, pend=pp >> 11 & 1, verdict=pp >> 12 & 0xF, tag=pp >> 24)


def nvm_read(rel):
    t = text(A / rel)
    m = re.search(r"^### (\S+) cmd='milan_nvm'[^\n]*\nmilan_nvm\n(NVM: slot[^\n]*)\n(NVM: PP_NVM_STAT[^\n]*)\n", t, re.M)
    pp = int(re.search(r"PP_STAT=([0-9a-f]{8})", t).group(1), 16)
    slots, st = m.group(2), m.group(3)
    f = dict(
        at=m.group(1),
        slots="A %s / B %s" % re.search(r"slot A \S+ seq (\d+), slot B \S+ seq (\d+)", slots).groups(),
        slot_verdicts="%s / %s" % re.search(r"slot A (\S+) seq \d+, slot B (\S+) seq", slots).groups(),
        authoritative=re.search(r"authoritative (\S+),", slots).group(1),
        image_seq=re.search(r"image seq (\d+)", slots).group(1),
        records=re.search(r"(\d+) records, (\d+) B", slots).group(1),
        record_bytes=re.search(r"(\d+) records, (\d+) B", slots).group(2),
        writer=re.search(r"writer (\S+)", slots).group(1),
        pp_nvm_stat=re.search(r"PP_NVM_STAT=([0-9a-f]{8})", st).group(1),
        nvm_stat_fields=" ".join(re.search(r"PP_NVM_STAT=[0-9a-f]{8} (.*?);", st).group(1).split()),
        commits="%s / %s" % re.search(r"commits ok=(\d+) failed=(\d+)", st).groups(),
        refusals=re.search(r"(captures refused=\d+ acks refused=\d+)", st).group(1),
        last=re.search(r"last=(\S+)", st).group(1),
        pp_stat="%08x" % pp,
        pp_stat_bits=bits(pp),
    )
    ns = int(f["pp_nvm_stat"], 16)
    f["pp_nvm_stat_decoded"] = dict(tag="%02x" % (ns >> 24), unres=ns >> 23 & 1, pend=ns >> 22 & 1,
                                    commit_busy=ns >> 10 & 1, stale=ns >> 9 & 1, dirty=ns >> 8 & 1,
                                    img_valid=ns >> 7 & 1, backed=ns >> 6 & 1, dev_busy=ns >> 4 & 1)
    return f


print("== saved-state reads (milan_nvm)")
start = nvm_read("identity/console-identity.txt")
end = nvm_read("restore/console-final.txt")
for name, f in (("identity gate", start), ("final restore", end)):
    print(f"{name}: {f['at']}")
    for k, v in f.items():
        if k != "at":
            print(f"    {k}: {v}")
same = {k: (start[k], end[k]) for k in start if k != "at" and start[k] != end[k]}
check(not same, f"identity-gate and final-restore reads identical in every field except the timestamp {same or ''}")

print("\n== every console sample, PP_STAT (milan_status)")
samples = []
for f in sorted(A.rglob("console*.txt")):
    t = text(f)
    for m in re.finditer(r"^### (\S+) cmd='milan_status'[^\n]*\n(?:[^\n]*\n)*?[^\n]*PP_STAT=([0-9a-f]{8})", t, re.M):
        ts = datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()
        samples.append((ts, f.relative_to(A).as_posix(), int(m.group(2), 16)))
samples.sort()
files = {s[1] for s in samples}
print(f"console files {len(files)}, milan_status samples {len(samples)}, first {utc(samples[0][0])} ({samples[0][1]}), "
      f"last {utc(samples[-1][0])} ({samples[-1][1]})")
vals = Counter("%08x" % s[2] for s in samples)
print("distinct PP_STAT:", dict(vals))
for v in vals:
    print(f"  {v}: {bits(int(v, 16))}")
tally = {k: sum(bits(s[2])[k] for s in samples) for k in ("alarm", "backed", "dirty", "stale", "img_valid", "pend")}
print("samples with each bit set:", tally)
check(len(vals) == 1, "PP_STAT constant over every console sample")
check(tally["dirty"] == 0 and tally["alarm"] == 0 and tally["stale"] == 0,
      "nvm_dirty, nvm_alarm and nvm_stale read 0 in every sample")
check(tally["pend"] == len(samples) and tally["backed"] == len(samples),
      "nvm_pend and nvm_backed read 1 in every sample")
check(all(bits(s[2])["verdict"] == 0 for s in samples), "verdict nibble 0 (VD_OK) in every sample")
check(len(files) == 226, "226 console files: identity, final, and before/after of 112 actions")

print("\n== controller transcripts: state-changing commands and DUT sink polls")
acmp = Counter()
aecp = Counter()
other_changing = []
sink_polls = Counter()
sink_values = Counter()
out_polls = Counter()
first_t, last_t = None, None
for f in sorted(A.rglob("*.jsonl")):
    rel = f.relative_to(A).as_posix()
    for line in text(f).splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        what, role, resp = r.get("what"), r.get("role"), r.get("response")
        if isinstance(what, str) and re.fullmatch(r"acmp-(6|8)", what):
            name = {"acmp-6": "CONNECT_RX", "acmp-8": "DISCONNECT_RX"}[what]
            acmp[(name, role, resp.get("listener_uid"), resp.get("talker", "")[:6] == "020000",
                  resp.get("talker_uid"), resp.get("status"))] += 1
            first_t = r["t"] if first_t is None else min(first_t, r["t"])
            last_t = r["t"] if last_t is None else max(last_t, r["t"])
        cmd = resp.get("cmd") if isinstance(resp, dict) else None
        if cmd is None and isinstance(r.get("cmd"), str):
            cmd, role = r["cmd"], role or "dut (identity reader)"
        if cmd:
            aecp[(role, cmd)] += 1
            if not (cmd.startswith("GET_") or cmd.startswith("READ_")):
                other_changing.append((rel, role, cmd))
        if role == "dut" and isinstance(what, str) and what.startswith("state-5-") and isinstance(resp, dict):
            sink_polls[what] += 1
            sink_values[(what, resp.get("status"), resp.get("conn_count"),
                         resp.get("talker") == "0000000000000000", resp.get("stream_id") == "0000000000000000")] += 1
        if role == "dut" and isinstance(what, str) and what.startswith("state-6-"):
            out_polls[what] += 1
for k, v in sorted(acmp.items(), key=str):
    print(f"  {v:3d} x {k[0]} to role={k[1]} listener_uid={k[2]}, talker is the DUT: {k[3]}, talker_uid={k[4]}, status={k[5]}")
print(f"  ACMP state-changing commands between {utc(first_t)} and {utc(last_t)}")
print("  AECP commands by role:", dict(sorted(aecp.items(), key=str)))
print("  AECP commands other than GET_/READ_:", other_changing or "none")
print("  DUT stream input polls (GET_RX_STATE):", dict(sink_polls))
print("  DUT stream input values (what, status, conn_count, talker all-zero, stream all-zero):", dict(sink_values))
print("  DUT stream output polls (GET_TX_STATE):", dict(out_polls))
check(sum(acmp.values()) == 210 and all(k[1] == "peer" and k[2] == 8 and k[5] == 0 for k in acmp)
      and all(k[3] and k[4] == 1 for k in acmp if k[0] == "CONNECT_RX"),
      "210 ACMP state-changing commands (105 CONNECT_RX, 105 DISCONNECT_RX), all to the reference peer's "
      "Stream Input 8 and all SUCCESS; every CONNECT_RX response names DUT Stream Output 1 as the talker")
check(not other_changing, "no AECP command other than GET_ and READ_ in any transcript")
t0 = datetime.strptime(start["at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()
t1 = datetime.strptime(end["at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()
acts = [s for s in samples if not s[1].startswith(("identity/", "restore/"))]
print(f"  action console samples {len(acts)}: {utc(acts[0][0])} ({acts[0][1]}) to {utc(acts[-1][0])} ({acts[-1][1]})")
check(t0 < acts[0][0] and acts[-1][0] < t1 and t0 < first_t and last_t < t1,
      f"the two milan_nvm reads ({utc(t0)}, {utc(t1)}) bracket every action console sample and every ACMP command")
check(all(k[1] == 0 and k[2] == 0 and k[3] and k[4] for k in sink_values),
      "every poll of a DUT stream input read connection count 0 with no talker and no stream")

print("\n== lane B1 final restore (PR #620 page at 931c3edf, Saved-state layer table)")
row = {}
for label in ("NVM slots A / B, image sequence", "Commits ok / failed", "`PP_STAT`, `nvm_pend` (bit 11)", "`PP_NVM_STAT`"):
    m = re.search(r"^\| " + re.escape(label) + r" \| ([^|]*) \| ([^|]*) \|$", B1, re.M)
    row[label] = m.group(2).strip()
    print(f"  {label}: {row[label]}")
b2 = {"NVM slots A / B, image sequence": f"{start['slots'].replace('A ', '').replace('B ', '')}, image {start['image_seq']}",
      "Commits ok / failed": start["commits"],
      "`PP_STAT`, `nvm_pend` (bit 11)": f"`0x{start['pp_stat']}`, {start['pp_stat_bits']['pend']}",
      "`PP_NVM_STAT`": f"`0x{start['pp_nvm_stat']}`, pend {start['pp_nvm_stat_decoded']['pend']}"}
for k in row:
    print(f"  B2 identity gate, same format: {k}: {b2[k]}")
check(all(row[k] == b2[k] for k in row), "B2's identity-gate read equals lane B1's final-restore column in all four rows")

print("\n== inputs against the archive MANIFEST.json (author/ prefix)")
match = redacted = missing = 0
for rel, digest in sorted(READ.items()):
    e = MAN.get("author/" + rel)
    if e is None or e["original_sha256"] != digest:
        missing += 1
        print("  NOT IN ARCHIVE AS READ:", rel)
    elif e["published_sha256"] == digest:
        match += 1
    else:
        redacted += 1
print(f"  files read {len(READ)}: archived bytes identical {match}, archived as a redacted copy {redacted}, unmatched {missing}")
cons = [r for r in READ if Path(r).name.startswith("console")]
check(all(MAN["author/" + r]["published_sha256"] == READ[r] for r in cons),
      f"all {len(cons)} console files read are byte-identical to the archived copies")
check(missing == 0, "every file read matches its archive original_sha256")

print("\nFAILURES:", len(FAILS))
for f in FAILS:
    print("  ", f)
sys.exit(1 if FAILS else 0)
