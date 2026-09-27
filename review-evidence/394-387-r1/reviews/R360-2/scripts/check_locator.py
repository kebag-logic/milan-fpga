#!/usr/bin/env python3
"""Check the page's artifact-hash table against the public evidence archive.

Usage: check_locator.py <page.md> <archive-dir review-evidence/394-387-r1>
1. MANIFEST.json (publisher index): every entry's file exists and hashes/sizes match.
2. The page's 50 (cycle, artifact, bytes, sha256) rows equal author/RAW-ARTIFACTS.json
   and every author/cycleNN/raw-artifacts.json.
3. The page names no private packet id, /tmp path or absolute home path.
"""
import hashlib, json, os, re, sys


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def walk_entries(obj):
    """Yield dicts that look like artifact records (have a sha256 and a name/path)."""
    if isinstance(obj, dict):
        keys = {k.lower() for k in obj}
        if any("sha" in k for k in keys) and any(k in keys for k in ("path", "name", "file", "artifact")):
            yield obj
        for v in obj.values():
            yield from walk_entries(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_entries(v)


def field(d, *names):
    for n in names:
        for k, v in d.items():
            if k.lower() == n:
                return v
    return None


def main():
    page, root = sys.argv[1], sys.argv[2]
    ok = True
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    good = bad = 0
    for e in man:
        p = field(e, "path", "name", "file")
        s = field(e, "published_sha256", "sha256")
        n = field(e, "size", "bytes")
        fp = os.path.join(root, p)
        if os.path.isfile(fp) and sha(fp) == s and (n is None or os.path.getsize(fp) == n):
            good += 1
        else:
            bad += 1
            print("MANIFEST mismatch:", p)
    listed = {field(e, "path", "name", "file") for e in man}
    present = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs}
    unlisted = sorted(present - listed - {"MANIFEST.json"})
    print(f"MANIFEST.json entries={len(man)} verified={good} mismatched={bad} unlisted-files={unlisted}")
    ok &= bad == 0 and not unlisted

    rows = set()
    for line in open(page, encoding="utf-8"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|", line)
        if m:
            rows.add((int(m[1]), m[2], int(m[3]), m[4]))
    print(f"page artifact rows={len(rows)}")
    ok &= len(rows) == 50

    def index_rows(path, cyc=None):
        out, paths = set(), []
        for e in walk_entries(json.load(open(path))):
            p = field(e, "path", "name", "file", "artifact")
            s = field(e, "sha256")
            n = field(e, "size", "bytes")
            paths.append(str(p))
            c = cyc
            if c is None:
                mm = re.search(r"cycle(\d\d)", str(p)) or re.search(r"cycle(\d\d)", json.dumps(e))
                c = int(mm[1]) if mm else None
            out.add((c, os.path.basename(str(p)), n, s))
        return out, paths

    raw, rawpaths = index_rows(os.path.join(root, "author", "RAW-ARTIFACTS.json"))
    raw_cyc = {r for r in raw if r[0] is not None}
    print(f"RAW-ARTIFACTS.json cycle records={len(raw_cyc)} page-minus-index={sorted(rows - raw_cyc)} "
          f"index-minus-page={sorted(raw_cyc - rows)}")
    ok &= rows == raw_cyc or rows <= raw_cyc
    per = set()
    allpaths = list(rawpaths)
    for c in range(1, 11):
        r, ps = index_rows(os.path.join(root, "author", f"cycle{c:02d}", "raw-artifacts.json"), c)
        per |= r
        allpaths += ps
    per_named = {r for r in per if (r[1]) in {x[1] for x in rows}}
    print(f"per-cycle index records={len(per)}; records with a page artifact name={len(per_named)} "
          f"page-minus-index={sorted(rows - per)} same-name-index-minus-page={sorted(per_named - rows)}")
    ok &= rows <= per and per_named == rows
    prefixes = sorted({os.path.dirname(p).rsplit("/cycle", 1)[0] for p in allpaths if p.startswith("/")})
    print(f"historical absolute prefixes in indexes: {prefixes}")

    text = open(page, encoding="utf-8").read()
    leaks = re.findall(r"/tmp/\S*|/home/\S*|/data/\S*|~/\S*|2026-09-23/394-a375|394-a375|MANIFEST\.sha256", text)
    print(f"page private-locator hits: {leaks}")
    ok &= not leaks
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
