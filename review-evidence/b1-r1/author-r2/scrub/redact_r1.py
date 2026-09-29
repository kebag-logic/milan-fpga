#!/usr/bin/env python3
"""Copy the round-1 author packet into r1/, redacted, and record every change.

usage: redact_r1.py <round-1-packet-dir> <out-r1-dir> <private-token-file>

The token file is private and stays outside the packet: a JSON list of
{"kind": ..., "token": ...}. Kinds map to fixed placeholders, so no private
value is written. Excluded from the copy: interpreter bytecode, and packet
captures (pcap), which carry host MAC addresses in every frame; the round-1
publication excluded both as well. Their original SHA-256 values stay in
r1/MANIFEST.sha256 and r1/REDACTION.json.

Writes r1/REDACTION.json: one entry per round-1 file with its original
SHA-256, the published SHA-256 (or null when excluded) and the number of
replacements per placeholder.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

PLACEHOLDER = {
    "account": "<account>",
    "capture-if": "<capture-host-if>",
    "tap_if": "<capture-host-if>",
    "capture-mac": "<capture-host-mac>",
    "ctl_if": "<controller-host-if>",
    "controller-clock": "<controller-host-eui64>",
    "controller-mac": "<controller-host-mac>",
    "controller": "<controller-host>",
    "tap_host": "<capture-host>",
    "strip_host": "<power-strip-host>",
    "local-host": "<operator-host>",
    "console_port": "<console-port>",
    "console-serial": "<console-port>",
    "instrument": "<tap-driver>",
}
CHECK_ONLY = {"controller-core"}  # must be gone after the replacements above


def main():
    src, out, tokfile = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    toks = json.loads(tokfile.read_text())
    subs = []
    home = next(t["token"] for t in toks if t["kind"] == "account")
    subs.append(("home", re.compile(re.escape("/home/" + home), re.I), "~"))
    for t in sorted(toks, key=lambda x: -len(x["token"])):
        if t["kind"] in CHECK_ONLY:
            continue
        tok = re.escape(t["token"])
        if len(t["token"]) < 8 or t["kind"] in ("account", "ctl_if", "capture-if", "tap_if"):
            tok = r"(?<![A-Za-z0-9_])" + tok + r"(?![A-Za-z0-9_])"
        subs.append((t["kind"], re.compile(tok, re.I), PLACEHOLDER[t["kind"]]))
    residue = [re.compile(re.escape(t["token"]), re.I) for t in toks]
    if out.exists():
        shutil.rmtree(out)
    entries = []
    for p in sorted(x for x in src.rglob("*") if x.is_file()):
        rel = p.relative_to(src).as_posix()
        raw = p.read_bytes()
        orig = hashlib.sha256(raw).hexdigest()
        if "__pycache__" in p.parts or p.suffix == ".pcap":
            entries.append(dict(file=rel, original_sha256=orig, published_sha256=None,
                                excluded="bytecode" if p.suffix == ".pyc" else "packet capture"))
            continue
        text = raw.decode("utf-8")
        counts = {}
        for kind, pat, rep in subs:
            text, n = pat.subn(rep, text)
            if n:
                counts[rep] = counts.get(rep, 0) + n
        for pat in residue:
            if pat.search(text):
                raise SystemExit(f"residue of a private token in {rel}")
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        data = text.encode("utf-8")
        dst.write_bytes(data)
        pub = hashlib.sha256(data).hexdigest()
        entries.append(dict(file=rel, original_sha256=orig, published_sha256=pub,
                            redacted=pub != orig, replacements=counts))
    (out / "REDACTION.json").write_text(json.dumps(entries, indent=1) + "\n")
    n_red = sum(1 for e in entries if e.get("redacted"))
    n_exc = sum(1 for e in entries if e.get("published_sha256") is None)
    print(f"round-1 files {len(entries)}: copied {len(entries) - n_exc}, redacted {n_red}, excluded {n_exc}")
    for e in entries:
        if e.get("redacted"):
            print(f"  redacted {e['file']}: {e['replacements']}")
        elif e.get("published_sha256") is None:
            print(f"  excluded {e['file']} ({e['excluded']})")


if __name__ == "__main__":
    main()
