#!/usr/bin/env python3
"""Reproduce the #117 B5 page's steps 1 to 3 from one archive commit alone.

usage: b5_repro.py <archive_git_dir> <commit> <scratch_dir>

Extracts only review-evidence/b5-r1/{author,author-r2,author-r3} at <commit> with
`git archive` into a fresh <scratch_dir>, checks every extracted file against the
commit's MANIFEST.json published_sha256, then runs the page's steps:

  1. in author-r2/receipts: gunzip -kf a-long-reads.u16.gz, then sha256 of the record;
  2. b5_attrib.py figures author author-r2/receipts, compared with attribution.txt;
  3. b5_round3.py figures author author-r2/receipts, compared with round3_figures.txt.

Each figures command is run twice: once plainly (the comparison) and once under a
Python audit hook that records every file the tool opens (the input list). The
opened files are intersected with the manifest's path_redacted set. Paths are printed
relative to the extraction root; nothing outside it is named.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile

ROOT = "review-evidence/b5-r1"
DIRS = ("author", "author-r2", "author-r3")
EXPECT_RECORD = "2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961"

TRACER = r"""
import os, runpy, sys
log, base, tool = sys.argv[1], sys.argv[2], sys.argv[3]
seen = []
def hook(event, args):
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        seen.append(os.path.realpath(p))
sys.addaudithook(hook)
sys.argv = [tool] + sys.argv[4:]
try:
    runpy.run_path(tool, run_name="__main__")
finally:
    with open(log, "w") as f:
        for p in seen:
            f.write(p + "\n")
"""


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(gitdir, commit, scratch):
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    tarpath = os.path.join(scratch, "x.tar")
    with open(tarpath, "wb") as f:
        subprocess.run(["git", "-C", gitdir, "archive", "--format=tar", commit]
                       + [f"{ROOT}/{d}" for d in DIRS] + [f"{ROOT}/MANIFEST.json"],
                       stdout=f, check=True)
    ex = os.path.join(scratch, "x")
    with tarfile.open(tarpath) as t:
        t.extractall(ex, filter="data")
    os.remove(tarpath)
    full = subprocess.run(["git", "-C", gitdir, "rev-parse", commit + "^{commit}"],
                          capture_output=True, text=True, check=True).stdout.strip()
    base = os.path.join(ex, ROOT)
    man = json.load(open(os.path.join(base, "MANIFEST.json")))
    os.remove(os.path.join(base, "MANIFEST.json"))
    byfile = {e["file"]: e for e in man}
    redacted = {e["file"] for e in man if e.get("path_redacted")}

    print(f"Reproduction of the page's steps 1-3 at archive commit {full}")
    print(f"Inputs: {ROOT}/{{{','.join(DIRS)}}}/ extracted with git archive; nothing else.")
    print()
    files = []
    for d in DIRS:
        for dp, _, fn in os.walk(os.path.join(base, d)):
            for n in fn:
                files.append(os.path.relpath(os.path.join(dp, n), base))
    files.sort()
    bad = [f for f in files if f not in byfile or byfile[f]["published_sha256"] != sha(os.path.join(base, f))]
    inman = [e["file"] for e in man if e["file"].split("/")[0] in DIRS]
    missing = sorted(set(inman) - set(files))
    print(f"== manifest: {len(files)} extracted files in the three directories; "
          f"{len(inman)} manifest entries there; {len(bad)} mismatched or unlisted; {len(missing)} missing")
    for f in bad + missing:
        print("   PROBLEM", f)
    print(f"   path_redacted in the three directories: {len([f for f in redacted if f.split('/')[0] in DIRS])}")
    print()

    rec = os.path.join(base, "author-r2/receipts")
    before = sha(os.path.join(rec, "a-long-reads.u16"))
    r = subprocess.run(["gunzip", "-kf", "a-long-reads.u16.gz"], cwd=rec)
    after = sha(os.path.join(rec, "a-long-reads.u16"))
    size = os.path.getsize(os.path.join(rec, "a-long-reads.u16"))
    print("== step 1: in author-r2/receipts, gunzip -kf a-long-reads.u16.gz")
    print(f"before: {before}  a-long-reads.u16 (manifest: published copy "
          f"{'matches' if before == byfile['author-r2/receipts/a-long-reads.u16']['published_sha256'] else 'DIFFERS'})")
    print(f"gunzip rc={r.returncode}")
    print(f"after:  {after}  a-long-reads.u16  {size} bytes "
          f"({'equals' if after == EXPECT_RECORD else 'DIFFERS FROM'} the page's hash; "
          f"{'equals' if after == byfile['author-r2/receipts/a-long-reads.u16']['original_sha256'] else 'differs from'} original_sha256)")
    print()

    ok = r.returncode == 0 and after == EXPECT_RECORD and not bad and not missing
    steps = (("2", "author-r2/tools/b5_attrib.py", "author-r2/receipts/attribution.txt"),
             ("3", "author-r3/tools/b5_round3.py", "author-r3/receipts/round3_figures.txt"))
    for n, tool, receipt in steps:
        args = ["figures", "author", "author-r2/receipts"]
        p = subprocess.run([sys.executable, tool] + args, cwd=base, capture_output=True)
        out = hashlib.sha256(p.stdout).hexdigest()
        pub = sha(os.path.join(base, receipt))
        same = p.stdout == open(os.path.join(base, receipt), "rb").read()
        print(f"== step {n}: {os.path.basename(tool)} figures author author-r2/receipts")
        print(f"rc={p.returncode}")
        print(f"stderr bytes: {len(p.stderr)}")
        print(f"output:    {out}  -")
        print(f"published: {pub}  {receipt}")
        print(f"{os.path.basename(receipt)}: {'byte-identical' if same else 'DIFFERENT'}")
        log = os.path.join(scratch, f"opens-{n}.txt")
        q = subprocess.run([sys.executable, "-c", TRACER, log, base, tool] + args,
                           cwd=base, capture_output=True)
        rb = os.path.realpath(base)
        opened = []
        for line in open(log):
            pth = line.rstrip("\n")
            if pth.startswith(rb + os.sep):
                rel = os.path.relpath(pth, rb)
                if rel not in opened and rel != tool:
                    opened.append(rel)
        print(f"traced run: rc={q.returncode}, output {'equal' if q.stdout == p.stdout else 'DIFFERENT'}")
        print("packet files opened (excluding the tool itself):")
        restored = "author-r2/receipts/a-long-reads.u16"
        for rel in opened:
            if rel == restored:
                tag = "path_redacted copy replaced by step 1; read as restored, " + after[:8]
            elif rel in redacted:
                tag = "path_redacted"
            else:
                tag = "not in manifest" if rel not in byfile else "unmasked"
            print(f"   {rel}  [{tag}]")
        masked = [rel for rel in opened if rel in redacted and rel != restored]
        print(f"masked inputs read: {', '.join(masked) if masked else 'none'}")
        ev = [rel for rel in opened if rel.endswith("events.jsonl")]
        print(f"events.jsonl opened: {'yes: ' + ', '.join(ev) if ev else 'no'}")
        print()
        ok = ok and p.returncode == 0 and same and q.returncode == 0 and q.stdout == p.stdout
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
