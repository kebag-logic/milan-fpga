#!/usr/bin/env python3
"""Check the #117 findings page's hashes and counts against the pinned archive.

Usage: verify_page_vs_archive.py PAGE.md ARCHIVE_ROOT
  ARCHIVE_ROOT is an extraction of review-evidence/117-r1 at the pinned commit.

Checks, each printed as CHECK <name> PASS|FAIL <detail>:
  - every MANIFEST.json entry's published_sha256 equals the bytes at the pin;
  - every file at the pin (bar MANIFEST.json) has exactly one entry;
  - redacted / path-only / identity counts, per packet;
  - each packet MANIFEST.sha256 line hash equals that file's original_sha256,
    and the number of lines sha256sum -c would report FAILED per packet;
  - every 64-hex value on the page, classified: resolves via MANIFEST.json
    (original or published), or is outside the archive;
  - the Raw artifacts tables: how many hashes name redacted files, by kind;
  - every 8-hex '...' prefix in the Tool revisions table, resolved against
    MANIFEST.json originals, and which of those are redacted.
"""
import hashlib, json, os, re, sys, collections


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    page, root = sys.argv[1], sys.argv[2]
    text = open(page, encoding="utf-8").read()
    lines = text.splitlines()
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    by_file = {e["file"]: e for e in man}
    fails = 0

    def check(name, ok, detail):
        nonlocal fails
        print(f"CHECK {name} {'PASS' if ok else 'FAIL'} {detail}")
        if not ok:
            fails += 1

    # 1. published hashes match bytes
    bad = [e["file"] for e in man if sha(os.path.join(root, e["file"])) != e["published_sha256"]]
    check("published-sha-matches-pin", not bad, f"entries={len(man)} mismatches={len(bad)} {bad[:5]}")
    # 2. coverage
    files = set()
    for dp, dn, fn in os.walk(root):
        for f in fn:
            files.add(os.path.relpath(os.path.join(dp, f), root))
    files.discard("MANIFEST.json")
    dup = [f for f, c in collections.Counter(e["file"] for e in man).items() if c > 1]
    check("manifest-covers-every-file", files == set(by_file) and not dup,
          f"files={len(files)} entries={len(by_file)} missing={sorted(files - set(by_file))[:5]} "
          f"extra={sorted(set(by_file) - files)[:5]} dup={dup}")
    # 3. counts
    red = [e for e in man if e["original_sha256"] != e["published_sha256"]]
    ident = [e for e in red if e.get("identity_redacted")]
    path_only = [e for e in red if not e.get("identity_redacted")]
    per = collections.Counter(e["file"].split("/")[0] for e in red)
    flag_mismatch = [e["file"] for e in man if bool(e.get("path_redacted")) != (e["original_sha256"] != e["published_sha256"])]
    print(f"INFO redacted={len(red)} identity={len(ident)} path_only={len(path_only)} per_packet={dict(per)}")
    print("INFO path_only_files=" + ",".join(sorted(e["file"] for e in path_only)))
    check("page-count-77", len(red) == 77 and "77 files are published redacted" in text, f"archive={len(red)}")
    check("page-count-6-path-only", len(path_only) == 6 and "Six carry only local paths" in text, f"archive={len(path_only)}")
    check("page-count-71-identity", len(ident) == 71 and "The other 71" in text, f"archive={len(ident)}")
    check("page-count-20-57", per.get("bench-a200") == 20 and per.get("bench-a202") == 57
          and "20 in the A200 packet, 57 in the A202 packet" in text, f"archive={dict(per)}")
    check("path_redacted-flag-consistent", not flag_mismatch, f"mismatches={flag_mismatch[:5]}")
    # 4. packet MANIFEST.sha256
    for pk in ("bench-a200", "bench-a202"):
        mp = os.path.join(root, pk, "MANIFEST.sha256")
        n = nfail = nbad = 0
        listed = set()
        for ln in open(mp, encoding="utf-8"):
            m = re.match(r"([0-9a-f]{64})  (.+)$", ln.rstrip("\n"))
            if not m:
                continue
            h, rel = m.group(1), m.group(2)
            rel = rel[2:] if rel.startswith("./") else rel
            key = f"{pk}/{rel}"
            n += 1
            listed.add(key)
            e = by_file.get(key)
            if e is None or e["original_sha256"] != h:
                nbad += 1
                print(f"  UNMATCHED {key}")
            p = os.path.join(root, key)
            if not os.path.exists(p) or sha(p) != h:
                nfail += 1
        unlisted = sorted(k for k in by_file if k.startswith(pk + "/") and k not in listed and not k.endswith("MANIFEST.sha256"))
        check(f"{pk}-MANIFEST.sha256-lists-originals", nbad == 0,
              f"lines={n} not-equal-to-original={nbad} sha256sum-c-FAILED={nfail} unlisted={len(unlisted)} {unlisted[:6]}")
    # 5. page 64-hex values
    orig = collections.defaultdict(list)
    pub = collections.defaultdict(list)
    for e in man:
        orig[e["original_sha256"]].append(e)
        pub[e["published_sha256"]].append(e)
    hexes = re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", text)
    uniq = list(dict.fromkeys(hexes))
    resolved, outside = [], []
    for h in uniq:
        if h in orig or h in pub:
            resolved.append(h)
        else:
            outside.append(h)
    print(f"INFO page_64hex_total={len(hexes)} unique={len(uniq)} resolve_via_manifest={len(resolved)} outside={len(outside)}")
    for h in outside:
        ln = next(i + 1 for i, l in enumerate(lines) if h in l)
        print(f"  OUTSIDE line={ln} {h[:16]}... :: {lines[ln-1][:90]}")
    # Raw artifacts tables
    start = next(i for i, l in enumerate(lines) if l.startswith("## Raw artifacts"))
    raw_rows = []
    for i in range(start, len(lines)):
        m = re.match(r"\| (.+?) \| `([0-9a-f]{64})` \|$", lines[i])
        if m:
            raw_rows.append((i + 1, m.group(1), m.group(2)))
    unresolved_rows = [r for r in raw_rows if r[2] not in orig]
    check("raw-artifact-rows-resolve-as-original", not unresolved_rows,
          f"rows={len(raw_rows)} unresolved={[(r[0], r[1]) for r in unresolved_rows]}")
    red_rows = []
    for ln, label, h in raw_rows:
        es = orig.get(h, [])
        if any(e["original_sha256"] != e["published_sha256"] for e in es):
            red_rows.append((ln, label, [e["file"] for e in es]))
    uniq_red_hashes = {h for ln, label, h in raw_rows if any(e["original_sha256"] != e["published_sha256"] for e in orig.get(h, []))}
    print(f"INFO raw_rows={len(raw_rows)} rows_naming_redacted={len(red_rows)} unique_redacted_hashes={len(uniq_red_hashes)}")
    kinds = collections.Counter()
    for ln, label, fl in red_rows:
        f = fl[0]
        k = ("capture" if f.endswith(".pcap") else "analysis" if "/analysis." in f else
             "census" if "census" in f else "entity" if "/entity_" in f else "lock" if f.endswith("lock.txt") else "other:" + f)
        kinds[k] += 1
        print(f"  REDACTED-ROW line={ln} {label} -> {','.join(fl)}")
    print(f"INFO redacted_row_kinds={dict(kinds)}")
    check("page-count-29", len(red_rows) == 29 and "29 of them name files published only in redacted form" in text,
          f"archive={len(red_rows)}")
    # 6. Tool revisions prefixes
    ts = next(i for i, l in enumerate(lines) if l.startswith("## Tool revisions"))
    te = next(i for i in range(ts + 1, len(lines)) if lines[i].startswith("## "))
    prefixes = re.findall(r"`([0-9a-f]{8})\.\.\.`", "\n".join(lines[ts:te]))
    table_end = next(i for i in range(ts + 1, te) if lines[i].startswith("Full hashes"))
    table_prefixes = list(dict.fromkeys(re.findall(r"`([0-9a-f]{8})\.\.\.`", "\n".join(lines[ts:table_end]))))
    for p in list(dict.fromkeys(prefixes)):
        es = [e for e in man if e["original_sha256"].startswith(p)]
        eps = [e for e in man if e["published_sha256"].startswith(p) and not e["original_sha256"].startswith(p)]
        if es:
            desc = ";".join(f"{e['file']}{' REDACTED' if e['original_sha256'] != e['published_sha256'] else ''}" for e in es)
        elif eps:
            desc = "published-only:" + ";".join(e["file"] for e in eps)
        else:
            desc = "NOT-IN-ARCHIVE"
        print(f"  TOOLPREFIX {p} {'table' if p in table_prefixes else 'paragraph'} -> {desc}")
    red_quoted = [p for p in table_prefixes if any(e["original_sha256"].startswith(p) and e["original_sha256"] != e["published_sha256"] for e in man)]
    check("tool-table-redacted-quoted-is-four", len(red_quoted) == 4, f"redacted quoted prefixes={red_quoted}")
    print(f"RESULT fails={fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
