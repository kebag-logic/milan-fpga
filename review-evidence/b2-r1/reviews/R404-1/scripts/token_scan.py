#!/usr/bin/env python3
"""Privacy token scan over the two findings pages and the archived packet.

Usage: token_scan.py <repo-clone> <packet-root> [<packet-root> ...]
Optional: PRIVATE_TOKENS=<file> names a file of extra case-insensitive regular
expressions (one per line) for site-private names; the file is not published
and its patterns are never printed, only their hit counts.

Applies the repository gate's own SCRUB_RULES (imported from the clone's
scripts/docs_check.py, never copied) and generic shapes: IPv4 addresses,
colon MAC addresses, interface names, home and user paths, tty/USB serial
paths, e-mail addresses, host-like names, temporary paths, EUI-64 identifiers
built from a MAC (the ...fffe... insertion) and 16-hex identifiers carrying a
vendor prefix. Identifier classes are printed masked, with file counts per
page/packet, so the receipt never republishes an identity.
"""
import importlib.util
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

GENERIC = [
    ("ipv4", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("colon-mac", re.compile(r"\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b")),
    ("iface", re.compile(r"\b(?:enp\d|ens\d|eno\d|enx[0-9a-f]|eth\d|wlan\d|wlp\d|br-[a-z0-9]|veth|docker\d)\w*")),
    ("home/user path", re.compile(r"/(?:home|Users|root)/[A-Za-z0-9._-]+")),
    ("tty/usb", re.compile(r"/dev/(?:tty(?:USB|ACM)\d+|serial/by-(?:id|path)/\S+)")),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("hostname-ish", re.compile(r"\b[a-z][a-z0-9-]*\.(?:local|lan|home|internal|corp)\b", re.I)),
    ("tmp path", re.compile(r"/tmp/[A-Za-z0-9._/-]+")),
    ("eui64-from-mac", re.compile(r"\b[0-9a-fA-F]{6}[fF]{3}[eE][0-9a-fA-F]{6}\b")),
    ("hex16-vendor", re.compile(r"\b[0-9a-fA-F]{16}\b")),
]
# Prefixes that are protocol constants, zero fill or the DUT's synthetic
# locally administered address, not a device identity.
SAFE = re.compile(r"^(?:91e0f0|0180c2|020000|01005e|ffffff|000000|041060|000200|002400)", re.I)
SAFE_MAC = re.compile(r"^(?:91:e0:f0|01:80:c2|02:00:00|01:00:5e|ff:ff:ff)", re.I)
MASKED = {"eui64-from-mac", "hex16-vendor", "colon-mac"}


def load_rules(repo: Path):
    spec = importlib.util.spec_from_file_location("docs_check", repo / "scripts" / "docs_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SCRUB_RULES


def mask(tok):
    return "<%d-hex %s identifier>" % (len(tok), "fffe-form" if "fffe" in tok.lower() else "vendor-prefix")


def main():
    repo = Path(sys.argv[1])
    roots = [Path(p) for p in sys.argv[2:]]
    rules = load_rules(repo)
    private = []
    if os.environ.get("PRIVATE_TOKENS"):
        private = [re.compile(l.strip(), re.I) for l in open(os.environ["PRIVATE_TOKENS"]) if l.strip()]
    pages = [repo / "docs/findings/606_FIRST_BIND_MEASUREMENT.md",
             repo / "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md"]
    files = [("page", p) for p in pages]
    for r in roots:
        files += [("packet", p) for p in sorted(r.rglob("*")) if p.is_file()]
    hits = defaultdict(lambda: defaultdict(set))   # (where, cls) -> token -> files
    for where, f in files:
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            for pat, cls, _fix in rules:
                if pat.search(line):
                    hits[(where, "gate:" + cls)]["<gate class>"].add(str(f))
            for i, pat in enumerate(private):
                if pat.search(line):
                    hits[(where, "private-pattern-%d" % i)]["<private>"].add(str(f))
            for cls, pat in GENERIC:
                for m in pat.finditer(line):
                    tok = m.group(0)
                    if cls in ("eui64-from-mac", "hex16-vendor") and SAFE.match(tok):
                        continue
                    if cls == "hex16-vendor" and (not re.search(r"[a-fA-F]", tok[:6]) or "fffe" in tok.lower()):
                        continue   # digits from float text, or already counted as EUI-64
                    if cls == "colon-mac" and SAFE_MAC.match(tok):
                        continue
                    if cls == "ipv4" and not all(int(x) <= 255 for x in tok.split(".")):
                        continue
                    hits[(where, cls)][tok].add(str(f))
    print(f"files scanned: {len(files)} (2 pages + {len(files) - 2} packet files); private patterns: {len(private)}")
    for (where, cls) in sorted(hits):
        toks = hits[(where, cls)]
        print(f"== {where} {cls}: {len(toks)} distinct, {len(set().union(*toks.values()))} files")
        for tok, fs in sorted(toks.items(), key=lambda kv: -len(kv[1]))[:12]:
            shown = mask(tok) if cls in MASKED else tok
            ex = sorted(fs)[0]
            base = roots[0] if where == "packet" else repo
            print(f"   {shown}\t{len(fs)} files\te.g. {os.path.relpath(ex, base)}")
    if not any(w == "page" for (w, _c) in hits):
        print("pages: no hit in any class")


if __name__ == "__main__":
    main()
