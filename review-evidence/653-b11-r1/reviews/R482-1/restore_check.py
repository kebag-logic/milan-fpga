#!/usr/bin/env python3
"""Identity aggregate, census, counters, NVM and servo figures the page states, read
from the public evidence. usage: restore_check.py <author_dir>"""
import json, re, sys
from pathlib import Path
A = Path(sys.argv[1]); R = A / "restore"; fails = 0
def chk(n, ok, d=""):
    global fails; fails += not ok; print(("PASS " if ok else "FAIL ") + n + (" :: " + d if d else ""))
iv = (A / "identity/identity-verdict.txt").read_text()
fl = [json.loads(l)["check"] for l in iv.splitlines() if l.startswith("{") and json.loads(l)["result"] == "FAIL"]
chk("identity tool aggregate FAILs only on the three live fields the page names", fl == ["aecp-STREAM_INPUT 0", "aecp-CLOCK_DOMAIN 0", "get-clock-source"], f"aggregate line: {iv.strip().splitlines()[-1]}; FAIL checks {fl}")
offs = {json.loads(l)["check"]: json.loads(l)["detail"].get("differing_offsets") for l in iv.splitlines() if l.startswith("{") and isinstance(json.loads(l)["detail"], dict) and "differing_offsets" in json.loads(l)["detail"]}
chk("differing offsets are STREAM_INPUT current_format (74..81) and CLOCK_DOMAIN clock_source_index (70..71)", offs["aecp-STREAM_INPUT 0"] == [78] and offs["aecp-CLOCK_DOMAIN 0"] == [71])
ev = (A / "identity/identity-entity-verdict.txt").read_text()
chk("entity facts PASS (the lane's STOP gate)", "ENTITY FACTS: PASS" in ev and ev.count('"PASS"') == 4)
chk("CRCs equal", all(f'"{k}", "result": "PASS"' in iv for k in ("crc-aem", "crc-rom", "crc-payload")))
chk("UART grader 10/10 start and end", "10/10" in (A / "identity/grader-identity.txt").read_text() and "10/10" in (R / "grader-end.txt").read_text())
cc = [json.loads(l) for l in (R / "census-compare.txt").read_text().splitlines() if l.startswith("{")]
d = cc[1]; same = cc[-1]
pa, pb = int(d["a"]["payload"][-24:-16], 16), int(d["b"]["payload"][-24:-16], 16)
chk("census 45 of 46, the one difference GET_AVB_INFO propagation delay 381 -> 387 ns", same == {"same": 45, "compared": 46} and d["a"]["cmd"] == "GET_AVB_INFO" and (pa, pb) == (381, 387), f"{pa} -> {pb}")
def ctr(f):
    out = {}
    for l in (R / f).read_text().splitlines():
        if l.startswith("{"):
            e = json.loads(l); p = e.get("payload", "")
            if e.get("cmd") == "GET_COUNTERS" and e.get("role") == "dut":
                out[(int(p[0:4], 16), int(p[4:8], 16))] = (int(p[16:24], 16), int(p[24:32], 16))
    return out
s, e = ctr("counters-start.jsonl"), ctr("counters-end.jsonl")
chk("STREAM_INPUT 0 and 1 counters 1/1 at start and end", s[(5, 0)] == s[(5, 1)] == e[(5, 0)] == e[(5, 1)] == (1, 1))
chk("CLOCK_DOMAIN 0 counters 3/3 -> 6/6 (three lock/unlock pairs)", s[(0x24, 0)] == (3, 3) and e[(0x24, 0)] == (6, 6))
nv = lambda f: re.search(r"image seq (\d+).*?commits ok=(\d+)", (R / f).read_text(), re.S).groups()
a, b = nv("dut-start.txt"), nv("dut-end.txt")
chk("NVM seq 51 -> 98, commits 20 -> 67 (47)", a == ("51", "20") and b == ("98", "67"))
sb, sa = (R / "servo-before-release.txt").read_text(), (R / "servo-after-release.txt").read_text()
chk("servo trim 0xffa40035 before the release, 0x00000020 after", "35 00 a4 ff" in sb and "20 00 00 00" in sa)
cr = [json.loads(l) for l in (R / "clock-release.jsonl").read_text().splitlines() if l.startswith("{") and l.find('"cmd"') > 0]
seq = [(x["cmd"], x["payload"][-8:-4]) for x in cr]
chk("clock release: SET 0 then SET 1, each read back, ends on source 1", seq == [("GET_CLOCK_SOURCE", "0001"), ("SET_CLOCK_SOURCE", "0000"), ("GET_CLOCK_SOURCE", "0000"), ("SET_CLOCK_SOURCE", "0001"), ("GET_CLOCK_SOURCE", "0001"), ("GET_CLOCK_SOURCE", "0001")], str(seq))
print("FAILS", fails); sys.exit(1 if fails else 0)
