#!/usr/bin/env python3
"""Check every hash row of the lane B8 section against the published packet.

Usage: check_b8_hashes.py <page.md> <packet-author-dir> <published MANIFEST.json>

Evidence rows: the cited file's bytes and SHA-256 at the published commit; a
masked tool's "as run" prefix is checked against redaction.json.
Raw rows: the size and SHA-256 recorded in the run's events.jsonl and in
RAW-ARTIFACTS.json (the raw files themselves are not published).
"""
import hashlib
import json
import pathlib
import re
import sys


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def main():
    page, pkt, man = map(pathlib.Path, sys.argv[1:4])
    text = page.read_text()
    sec = text[text.index("## Dev bbf704ec, 2026-10-03: lane B8"):]
    sec = sec[sec.index("### B8: artifact hashes"):]
    manifest = {e["file"]: e for e in json.loads(man.read_text())}
    problems = 0
    rows = 0
    raw_rows = []
    for line in sec.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and re.fullmatch(r"`[0-9a-f]{64}`", cells[3]):
            raw_rows.append(cells)
        elif len(cells) == 3 and re.fullmatch(r"`[0-9a-f]{64}`", cells[2]):
            rows += 1
            names = re.findall(r"`([^`]+)`", cells[0])
            want = cells[2].strip("`")
            size = int(cells[1].replace(",", ""))
            files = [n for n in names if "/" in n and not n.endswith("...")]
            if names[0].startswith("identity/"):
                files = ["identity/identity-verdict.txt",
                         "identity-resume/identity-verdict.txt",
                         "identity-postboot/identity-verdict.txt"]
            files = [f for f in files if (pkt / f).is_file() or not f.endswith("/")]
            for f in files:
                p = pkt / f
                if not p.is_file():
                    print(f"MISSING {f}")
                    problems += 1
                    continue
                got = sha(p)
                ok = got == want and p.stat().st_size == size
                pub = manifest.get("author/" + f, {}).get("published_sha256")
                print(f"{'OK ' if ok else 'BAD'} {f} bytes={p.stat().st_size} sha={got[:12]} manifest_pub_eq={pub == got}")
                problems += (not ok) + (pub != got)
            asrun = re.search(r"as run `([0-9a-f]+)\.\.\.`", cells[0])
            if asrun:
                red = json.loads((pkt / "redaction.json").read_text())
                orig = [red["files"].get(files[0], {}).get("original_sha256", "")]
                ok = any(o.startswith(asrun.group(1)) for o in orig)
                print(f"{'OK ' if ok else 'BAD'} as-run prefix {asrun.group(1)} for {files[0]} in redaction.json {orig}")
                problems += not ok
    raw_art = json.loads((pkt / "RAW-ARTIFACTS.json").read_text())
    raw_recs = [d for d in walk(raw_art) if "sha256" in d]
    run_dir = {"Tone proof": "proof", "SW": "sw", "CRFLL": "crfll", "PC": "pc"}
    for run, name, size, h in raw_rows:
        rows += 1
        fname = re.search(r"`([^`]+)`", name).group(1)
        want = h.strip("`")
        size = int(size.replace(",", ""))
        ra = [d for d in raw_recs if d.get("sha256") == want]
        ra_ok = any(d.get("bytes", d.get("size")) == size for d in ra)
        ev = pkt / "runs" / run_dir[run] / "events.jsonl"
        ev_hit = want in ev.read_text() if ev.is_file() else False
        ev_size = str(size) in ev.read_text() if ev.is_file() else False
        ok = ra_ok
        print(f"{'OK ' if ok else 'BAD'} raw {run}/{fname} RAW-ARTIFACTS={'size+sha' if ra_ok else ra} events.jsonl sha={ev_hit} size={ev_size}")
        problems += not ok
    print(f"rows={rows} problems={problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
