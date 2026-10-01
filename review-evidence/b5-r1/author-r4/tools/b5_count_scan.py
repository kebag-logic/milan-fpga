#!/usr/bin/env python3
"""Scan for the reference peer's stream, stream port, stream state and cluster counts.

usage: b5_count_scan.py <local_lane_packet> <repo> <range>[,<range>...]
                        <allowed_eui64>[,<allowed_eui64>...] <path>...

The counts are derived in memory from the local lane packet and never written:
the peer's stream input, stream output and stream state counts (start census),
its stream port and cluster counts (the survey's descriptor reads), the
highest cluster index, and the totals that contain them: DUT plus peer stream
states, the census entry count, that count less 1, and twice the peer stream
state count. Each is matched as digits or as a word.

Labels:
  peer-derived count   a derived count, then up to three words joined only by
                       spaces or commas, then a stream, cluster, port, census,
                       entry, read or state noun; also "all <count> unbound"
                       and "<count> of <count> entries"
  peer index range     "0 to <highest cluster index>"
  peer stream ports    the word for 2, or "both", before the stream port noun
  unlisted EUI-64      a 16-hex identifier not in <allowed_eui64>, on a line
                       that does not carry "sha256" (the table proof prints
                       16-hex SHA-256 prefixes)

Searched, case-insensitively: every file under each <path>, the lines each
range adds, and each range's commit messages. A hit prints the label and the
place only, never the matched text. Positive control, in memory before the
scan: every derived count is planted in a line and must hit.
"""
import glob
import json
import os
import re
import subprocess
import sys

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
         "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
NOUN = r"(?:streams?|stream states?|clusters?|ports?|census|entr(?:y|ies)|reads?|states?)(?![\w-])"


def derived(packet):
    r = os.path.join(packet, "restore")
    cen = [json.loads(x) for x in open(os.path.join(r, "census-start.jsonl"))]
    what = [str(x.get("what", "")) for x in cen]
    rx = sum(w.startswith("rx-state-peer-") for w in what)
    tx = sum(w.startswith("tx-state-peer-") for w in what)
    dut = sum(w.startswith(("rx-state-dut-", "tx-state-dut-")) for w in what)
    descs = [json.loads(x) for x in open(os.path.join(r, "peer-descs-2.jsonl"))]
    seen = {str(x.get("what", "")) for x in descs}

    def n(t):
        return len({w for w in seen if w.startswith(f"desc-peer-1-{t}-")})

    ports = n("0x000e") + n("0x000f")
    clusters = n("0x0010")
    vals = {rx, tx, rx + tx, ports, clusters, rx + tx + dut, len(cen), len(cen) - 1,
            2 * (rx + tx)}
    return sorted(v for v in vals if v > 0), clusters - 1


def main():
    packet, repo, ranges, allowed = sys.argv[1:5]
    paths = sys.argv[5:]
    allowed = {a.lower() for a in allowed.split(",")}
    vals, top = derived(packet)
    alt = "|".join([str(v) for v in vals] + [WORDS[v] for v in vals if v < len(WORDS)])
    pats = [
        ("peer-derived count", re.compile(
            r"(?<![\w.,/-])(?:" + alt + r")(?![\w]|[.,/]\d)(?:[\s,]+[\w'-]+){0,3}?[\s,]+" + NOUN
            + r"|\ball (?:" + alt + r")\s+(?:\w+\s+)?unbound\b"
            + r"|(?<![\w.,])(?:" + alt + r") of (?:" + alt + r") entries\b", re.I)),
        ("peer index range", re.compile(r"\b0 to " + str(top) + r"\b", re.I)),
        ("peer stream ports", re.compile(r"\b(?:two|both)\s+(?:of\s+the\s+)?(?:[\w']+\s+)?stream ports\b", re.I)),
    ]
    eui = re.compile(r"\b[0-9a-f]{16}\b", re.I)
    planted = [f"x {v} stream states y" for v in vals] + [f"x 0 to {top} y",
                                                          "x " + "bo" + "th stream ports y",
                                                          "x " + "0123456789" + "abcdef y"]
    ok = sum(bool(pats[0][1].search(p)) for p in planted[:len(vals)])
    ok += bool(pats[1][1].search(planted[-3])) + bool(pats[2][1].search(planted[-2]))
    ok += bool(eui.search(planted[-1]) and planted[-1][2:18] not in allowed)
    print(f"derived counts built in memory: {len(vals)}; labels: "
          f"{[lab for lab, _ in pats] + ['unlisted EUI-64']}; allowed EUI-64: {len(allowed)}")
    print(f"positive control in memory: {ok} of {len(planted)} planted lines hit")
    if ok != len(planted):
        print("positive control FAILED; scan not run")
        return 2
    texts = []
    for rng in ranges.split(","):
        diff = subprocess.run(["git", "-C", repo, "diff", "-U0", rng], check=True,
                              capture_output=True, text=True).stdout
        cur, n = None, 0
        for line in diff.splitlines():
            if line.startswith("+++ "):
                cur = line[6:]
            elif line.startswith("@@"):
                n = int(re.search(r"\+(\d+)", line).group(1))
            elif line.startswith("+"):
                texts.append((f"{rng} added {cur}", n, line[1:]))
                n += 1
        log = subprocess.run(["git", "-C", repo, "log", "--format=%B", rng], check=True,
                             capture_output=True, text=True).stdout
        for i, line in enumerate(log.splitlines(), 1):
            texts.append((f"{rng} commit messages", i, line))
    nfiles = 0
    for p in paths:
        for f in sorted(glob.glob(os.path.join(p, "**"), recursive=True)) if os.path.isdir(p) else [p]:
            if os.path.isfile(f):
                nfiles += 1
                for i, line in enumerate(open(f, errors="replace").read().splitlines(), 1):
                    texts.append((os.path.relpath(f, p) if os.path.isdir(p) else os.path.basename(f), i, line))
    hits = 0
    for place, i, line in texts:
        for lab, rx in pats:
            if rx.search(line):
                hits += 1
                print(f"HIT {lab}: {place}:{i}")
        if "sha256" not in line.lower() and any(m.lower() not in allowed for m in eui.findall(line)):
            hits += 1
            print(f"HIT unlisted EUI-64: {place}:{i}")
    print(f"scanned: {nfiles} files, {len(texts)} lines in all")
    print(f"hits: {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
