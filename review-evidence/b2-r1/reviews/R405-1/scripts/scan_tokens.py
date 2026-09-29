#!/usr/bin/env python3
"""Token scan for private host/peer/switch/instrument/interface/account/MAC-derived identities.

usage: scan_tokens.py <git clone> <prior-public ref>... -- <root>...
Environment: SCAN_PRIVATE_PATTERNS=<json file> adds the private deny-list (host, vendor
and account tokens), which is held outside the published packet on purpose.
Output never prints an identifier or a private token: each hit is shown as its category,
a kind label and sha256[:12] of the token, with paths relative to the scanned roots.
"""
import hashlib, json, os, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

i = sys.argv.index("--")
repo, refs, roots = sys.argv[1], sys.argv[2:i], [Path(p) for p in sys.argv[i + 1:]]
PAT = {
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "mac-colon": r"\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b",
    "eui64-fffe": r"\b[0-9a-fA-F]{6}fffe[0-9a-fA-F]{6}\b",
    "abs-path": r"(?:/home/|/Users/|/root/|/data/|/mnt/|/srv/|/opt/|[A-Z]:\\\\)",
    "hostname": r"\b[\w-]+\.(?:local|lan|internal|home|corp)\b|\b\w+@[\w-]+(?:\.[\w-]+)+\b",
    "iface": r"\b(?:eth\d+|en[ospx][0-9a-z]+|wl[a-z0-9]+|br-\w+|docker\d|virbr\d|tap\d+|usb\d)\b",
    "serial": r"(?i)\b(?:serial(?:\s*(?:no|number))?|s/n|sn:)\s*[:#]?\s*\w+",
}
priv = os.environ.get("SCAN_PRIVATE_PATTERNS")
if priv:
    PAT.update(json.load(open(priv)))
print(f"categories: {sorted(PAT)}; private deny-list loaded: {bool(priv)}")
h = lambda t: hashlib.sha256(t.lower().encode()).hexdigest()[:12]
hits = defaultdict(lambda: defaultdict(set))
files = []
for r in roots:
    files += [(r.name, f.relative_to(r) if r.is_dir() else Path(r.name), f) for f in (sorted(r.rglob("*")) if r.is_dir() else [r]) if f.is_file()]
for root, rel, f in files:
    txt = f.read_text(errors="replace")
    for cat, pat in PAT.items():
        for m in re.finditer(pat, txt):
            hits[cat][m.group(0)].add(f"{root}/{rel}")
print(f"scanned {len(files)} files")


def kind(tok):
    t = tok.lower().replace(":", "")
    if t.startswith("020000"):
        return "DUT (locally administered)"
    if t.startswith("91e0f0"):
        return "MAAP multicast stream destination"
    if re.fullmatch(r"(?:\d+\.){3}\d+", tok):
        return "dotted number"
    return "other"


for cat in PAT:
    print(f"\n[{cat}] distinct {len(hits[cat])}")
    for tok, fs in sorted(hits[cat].items(), key=lambda x: -len(x[1])):
        print(f"  sha256:{h(tok)} kind={kind(tok)} files={len(fs)} e.g. {sorted(fs)[0]}")


def public(tok):
    return [r[:12] for r in refs if subprocess.run(["git", "-C", repo, "grep", "-q", "-i", "-F", tok, r], capture_output=True).returncode == 0]


print("\n[identifier classification: EUI-64 (fffe form) and EUI-48 tokens]")
ids = defaultdict(int)
for _, _, f in files:
    for m in re.finditer(r"\b[0-9a-f]{16}\b|\b[0-9a-f]{12}\b|\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b", f.read_text(errors="replace")):
        t = m.group(0).lower().replace(":", "")
        if (len(t) == 16 and t[6:10] == "fffe") or (len(t) == 12 and t[:6] != "000000" and not t.isdigit()):
            ids[t] += 1
for t in sorted(ids, key=h):
    grp = int(t[:2], 16) & 1
    local = int(t[:2], 16) & 2
    k = "group (multicast)" if grp else ("locally administered" if local else "universally administered (vendor OUI)")
    print(f"  sha256:{h(t)} len={len(t)} {k}; {kind(t)}; occurrences={ids[t]}; exact token in public refs: {public(t) or 'NO'}")

print("\n[16-hex identifiers sharing a vendor OUI with a universally administered EUI-64 above (entity/stream IDs without fffe)]")
ouis = {t[:6] for t in ids if len(t) == 16 and not int(t[:2], 16) & 3}
sh = defaultdict(int)
for _, _, f in files:
    for m in re.finditer(r"\b[0-9a-f]{16}\b", f.read_text(errors="replace")):
        t = m.group(0)
        if t[:6] in ouis and t[6:10] != "fffe":
            sh[t] += 1
for t in sorted(sh, key=h):
    print(f"  sha256:{h(t)} OUI-sha256:{h(t[:6])}; occurrences={sh[t]}; exact token in public refs: {public(t) or 'NO'}")
