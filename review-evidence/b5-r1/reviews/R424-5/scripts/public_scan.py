#!/usr/bin/env python3
"""Public-text scan: names, wiring, channel map, counts, capture layout, clock topology.

Usage: public_scan.py <file> [<file> ...]
Each rule first fires on a planted control in memory. Output: file, line,
rule label only (never the matched text), so the receipt repeats nothing.
"""
import codecs
import re
import sys

R = lambda t: codecs.decode(t, "rot13")
V = lambda *w: r"\b(?:" + "|".join(w) + r")\b"
RULES = {
    # Name lists are stored rot13-encoded so the script does not spell them out.
    "vendor/product (audio, switch, instrument)": re.compile(V(*R('zbgh|y-npbhfgvpf|zrlre|q&o|ezr|nivq|cerfbahf|sbphfevgr|oruevatre|fpneyrgg|hzp\\q*|nhqvb cerpvfvba|nck\\q*|yhzvark|argtrne|rkgerzr|pvfpb|ovnzc|d-flf|dfp|lnznun|nyyra ?& ?urngu|qvtvpb|yno\\.tehccra|gnfpnz|mbbz|fgrvaoret|havirefny nhqvb|nagrybcr|sreebsvfu|kzbf|uvir').split("|")), re.I),
    "host name or account": re.compile(R('\\ocj\\q\\o|\\ohohagh\\o|\\oohvyq ?obk\\o|\\o[n-m0-9-]+\\.ybpny\\o|/ubzr/|\\onyrk\\o'), re.I),
    "address or interface": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b|\b(?:enp|enx|eth|wlan|wlp|usb)\d\w*", re.I),
    "wiring": re.compile(r"\b(?:cable[sd]?|wired|wiring|patch(?:ed)?|plugged|connector|S/?PDIF|AES ?3|ADAT|optical|XLR|BNC|RJ45|switch port|port \d+ of)\b", re.I),
    "channel map / capture layout": re.compile(r"channel map|\bch ?\d+\b|capture channels? \d+|channels? \d+ (?:and|to) \d+ of the capture|<capture-|<peer-channel", re.I),
    "peer count of streams/ports/clusters": re.compile(r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|sixteen|thirty-two) (?:reference[- ]peer |peer |of the peer's |peer's )?(?:streams?|stream ports?|stream states?|clusters?|stream inputs?|stream outputs?)\b", re.I),
    "clock topology": re.compile(r"word ?clock|clock (?:distribution|cable|master|tree)|\bwordclock\b|grandmaster is|gm is the|\bprovides? the clock\b", re.I),
}
CONTROLS = {
    "vendor/product (audio, switch, instrument)": R('n Sbphfevgr havg'),
    "host name or account": R('ba cj1 gbqnl'),
    "address or interface": "via 10.0.0.2",
    "wiring": "the optical cable",
    "channel map / capture layout": "the channel map",
    "peer count of streams/ports/clusters": "the peer's 8 streams",
    "clock topology": "a word clock line",
}


def main(*files):
    for k, r in RULES.items():
        assert r.search(CONTROLS[k]), f"control failed: {k}"
    print(f"controls: {len(RULES)} of {len(RULES)} rules fire on their planted control")
    for f in files:
        n = 0
        for ln, line in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
            for k, r in RULES.items():
                if r.search(line):
                    n += 1
                    print(f"{f}:{ln}: {k}")
        print(f"{f}: {n} hit(s)")


if __name__ == "__main__":
    main(*sys.argv[1:])
