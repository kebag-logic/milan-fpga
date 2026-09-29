#!/usr/bin/env python3
"""Round-5 positive check of the PR body's Round 2 F2 bullet against the archive.

Usage: census_sentence_r5.py <archived author dir> <pr-body.md>

census_sentence_r4.py checks the F7 phrase only when the old wording
"<n> ACMP commands all to the peer's input" is present, so it passes
vacuously once the phrase is reworded. This script requires the reworded
census to be present and correct, and it rejects any unqualified
"<n> ACMP commands" count left in the bullet.

Recount (byte-duplicate snapshot.jsonl excluded, as in round 4): the ACMP
transactions by message type (6 CONNECT_RX_COMMAND, 8 DISCONNECT_RX_COMMAND,
IEEE 1722.1 Table 8.1) and listener unique id. Checks, OK/FAIL per claim,
exit 1 on any FAIL:
  1. the bullet opens its derivation with
     "<n> state-changing ACMP commands (<c> `CONNECT_RX`, <d> `DISCONNECT_RX`),
     all to the peer's input", with n == c + d == archive total, c and d equal to
     the archive's per-type counts, and every one to the peer's listener uid 8;
  2. no "<n> ACMP commands" count in the bullet lacks the state-changing
     qualifier;
  3. the leading count agrees with the later sentence "The <m> `CONNECT_RX` and
     `DISCONNECT_RX` went to the reference peer" (n == m);
  4. the later sentence "no state-changing command addressed one" is still
     present, and the named reads still include GET_RX_STATE, so the opening
     phrase no longer contradicts it.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

A, body = Path(sys.argv[1]), Path(sys.argv[2]).read_text()

files = [p for p in sorted(A.rglob("*.jsonl"))
         if not (p.name == "snapshot.jsonl" and (p.parent / "snapshot-after.jsonl").read_bytes() == p.read_bytes())]
by_mt, uids = Counter(), set()
for p in files:
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        resp = r.get("response") if isinstance(r.get("response"), dict) else {}
        if r.get("kind") == "transaction":
            by_mt[r["mt"]] += 1
            uids.add(resp.get("listener_uid"))
total = sum(by_mt.values())
peer_only = uids == {8}
print("archive: state-changing ACMP by mt", dict(by_mt), "total", total, "listener uids", sorted(uids, key=str))

bullet = next((ln for ln in body.splitlines() if ln.startswith("- **F2, the saved-state layer.**")), "")
print("bullet found:", bool(bullet))
fails = 0


def check(name, ok):
    global fails
    fails += not ok
    print(("OK   " if ok else "FAIL ") + name)


m = re.search(r"(\d+) state-changing ACMP commands \((\d+) `CONNECT_RX`, (\d+) `DISCONNECT_RX`\), all to the peer's input", bullet)
n, c, d = (int(x) for x in m.groups()) if m else (None, None, None)
check(f"opening census '{n} state-changing ACMP commands ({c} CONNECT_RX, {d} DISCONNECT_RX), all to the peer's input'"
      f" == archive {total} ({by_mt[6]} mt6, {by_mt[8]} mt8), peer only {peer_only}",
      bool(m) and n == c + d == total and c == by_mt[6] and d == by_mt[8] and peer_only and set(by_mt) == {6, 8})
unq = [x.group(0) for x in re.finditer(r"(?<![\w-])(\d+) ACMP commands", bullet)]
check(f"no unqualified '<n> ACMP commands' count in the bullet (found {unq})", not unq)
m2 = re.search(r"The (\d+) `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer", bullet)
check(f"opening count {n} agrees with the later sentence's {m2.group(1) if m2 else '?'}",
      bool(m2) and n == int(m2.group(1)))
check("later sentences intact: 'no state-changing command addressed one' and the reads name GET_RX_STATE",
      "no state-changing command addressed one" in bullet and re.search(r"were reads, which write no record: \d+ GET_RX_STATE", bullet) is not None)
print("fails:", fails)
sys.exit(1 if fails else 0)
