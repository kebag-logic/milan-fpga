#!/usr/bin/env python3
"""Exhaustive per-page probes of `docs_inventory.py --check` on disposable clones of the exact head.

Usage: realtree_probes_r787.py SOURCE_CLONE HEAD_SHA WORKDIR RECEIPT
Every page gets every mutation, each followed by the real CLI gate; every mutation is undone by restoring bytes.
Length-only mutations must leave rc 0; status, banner and page-set mutations must give rc 1.
"""
import json, re, subprocess, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GATE = [sys.executable, "-I", "scripts/docs_inventory.py", "--check"]
AUDIT = "docs/DOCUMENTATION_AUDIT.md"
DATA = "scripts/docs_inventory.json"
LENGTH = ("top1", "top20", "mid", "end", "del_blank", "squeeze_head")

def sh(cwd, *cmd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

def gate(cwd):
    r = sh(cwd, *GATE)
    return r.returncode, (r.stdout + r.stderr).strip()

def edit(text, kind):
    lines = text.split("\n")
    if kind == "top1": return "\n" + text
    if kind == "top20": return "\n" * 20 + text
    if kind == "mid":
        n = len(lines) // 2
        return "\n".join(lines[:n] + ["", "Added line.", ""] + lines[n:])
    if kind == "end": return text + "\nAdded line.\n"
    if kind == "del_blank":
        for i, l in enumerate(lines):
            if not l.strip():
                return "\n".join(lines[:i] + lines[i + 1:])
        return None
    if kind == "squeeze_head":
        head = [l for l in lines[:60] if l.strip()]
        return "\n".join(head + lines[60:]) if len(head) != len(lines[:60]) else None
    raise ValueError(kind)

def page_probes(cwd, page):
    rows = []
    target = cwd / page
    original = target.read_bytes()
    text = original.decode("utf-8", "replace")
    for kind in LENGTH:
        new = edit(text, kind)
        if new is None:
            rows.append((page, kind, "skip", "no such line")); continue
        target.write_bytes(new.encode("utf-8"))
        rc, out = gate(cwd)
        target.write_bytes(original)
        rows.append((page, kind, rc, out.splitlines()[0:3] if rc else ""))
    target.write_bytes(b"> Superseded by [root](/README.md).\n" + original)
    rc, out = gate(cwd); target.write_bytes(original)
    rows.append((page, "banner", rc, out.splitlines()[0:3] if rc == 0 else ""))
    target.unlink(); rc, out = gate(cwd); target.write_bytes(original)
    rows.append((page, "rm_disk", rc, ""))
    sh(cwd, "git", "rm", "-q", "--cached", page); target.unlink()
    rc, out = gate(cwd)
    target.write_bytes(original); sh(cwd, "git", "add", page)
    rows.append((page, "rm_index", rc, ""))
    data_path = cwd / DATA
    raw = data_path.read_bytes(); data = json.loads(raw)
    data.setdefault("judged", {})[page] = {"status": "superseded", "evidence": "probe"}
    data_path.write_text(json.dumps(data)); rc, out = gate(cwd); data_path.write_bytes(raw)
    rows.append((page, "judged_status", rc, ""))
    return rows

def worker(args):
    index, source, sha, work, pages = args
    cwd = work / f"w{index}"
    sh(work, "git", "clone", "-q", "--shared", "--no-checkout", str(source), cwd.name)
    sh(cwd, "git", "checkout", "-q", "--detach", sha)
    assert gate(cwd)[0] == 0
    rows = []
    for page in pages:
        rows += page_probes(cwd, page)
    rc, out = gate(cwd)
    state = sh(cwd, "git", "status", "--porcelain").stdout
    return rows, (rc, state)

def main():
    source, sha, work, receipt = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    listed = sh(source, "git", "ls-files").stdout.split("\n")
    audit = (source / AUDIT).read_text()
    pages = [m.group(1).replace(" (historical)", "") for m in re.finditer(r"^\| \[([^\]]+)\]\([^)]*\) \|", audit, re.M)
             if "|" in m.group(0)]
    pages = sorted({p for p in pages if p in listed and p != AUDIT})
    shards = [pages[i::16] for i in range(16)]
    with ThreadPoolExecutor(16) as pool:
        got = list(pool.map(worker, [(i, source, sha, work, s) for i, s in enumerate(shards)]))
    rows = [r for g in got for r in g[0]]
    tally, odd = {}, []
    for page, kind, rc, note in rows:
        tally.setdefault(kind, {}).setdefault(str(rc), 0)
        tally[kind][str(rc)] += 1
        bad = (kind in LENGTH and rc not in (0, "skip")) or (kind not in LENGTH and rc != 1)
        if bad:
            odd.append(f"{kind} | {page} | rc={rc} | {note}")
    out = [f"pages probed: {len(pages)} (the audit page itself excluded), head {sha}"]
    out += [f"{kind}: {json.dumps(tally[kind], sort_keys=True)}" for kind in tally]
    out += [f"workers restored clean: {all(g[1] == (0, '') for g in got)}", f"unexpected: {len(odd)}"] + odd
    receipt.write_text("\n".join(out) + "\n")
    print("\n".join(out)[:6000])

main()
