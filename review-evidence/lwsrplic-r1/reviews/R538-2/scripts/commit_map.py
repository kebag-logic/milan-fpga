#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Map pre-rewrite commits to rewritten commits and diff their trees.

Usage: TERMS_FILE=<terms> commit_map.py <mirror-git-dir> <branch-clone-git-dir>

"Old" commits are reachable in the mirror (which includes GitHub pull refs)
but not from the branch clone.  Each old commit is matched to a new commit
with identical author, author date, committer, committer date and message.
For each pair the script prints the paths whose blobs differ; path names
matching a term are redacted.  For a modified file it prints the number of
added and removed lines and whether each removed line matches a term.
"""
import os
import re
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          check=True).stdout.decode(errors="replace")


def commits(repo, *refs):
    out = git(repo, "log", "--format=%H%x00%T%x00%P%x00%an <%ae> %ad%x00"
              "%cn <%ce> %cd%x00%B%x01", "--date=raw", *refs)
    res = {}
    for rec in out.split("\x01"):
        rec = rec.lstrip("\n")
        if not rec:
            continue
        h, t, p, a, c, msg = rec.split("\x00")
        res[h] = dict(tree=t, parents=p.split(), key=(a, c, msg.strip()))
    return res


def main():
    mirror, plain = sys.argv[1], sys.argv[2]
    pats = [re.compile(t.strip(), re.I) for t in open(os.environ["TERMS_FILE"])
            if t.strip()]

    def red(s):
        for n, p in enumerate(pats):
            s = p.sub(f"[TERM{n}]", s)
        return s

    allc = commits(mirror, "--all")
    new = commits(plain, "--all")
    old = {h: v for h, v in allc.items() if h not in new}
    # GitHub-generated test merges of open PRs are not rewritten commits.
    ghmerge = set(git(mirror, "for-each-ref", "--format=%(objectname)",
                      "refs/pull/*/merge").split())
    for h in sorted(ghmerge & set(old)):
        par = " ".join(x[:12] + ("(rewritten)" if x in new else "(pre-rewrite)")
                       for x in old[h]["parents"])
        print(f"GITHUB-MERGE-REF {h[:12]} parents={par}")
        del old[h]
    bykey = {}
    for h, v in new.items():
        bykey.setdefault(v["key"], []).append(h)
    mapping = {}
    bad = 0
    for h, v in sorted(old.items(), key=lambda kv: kv[1]["key"][0].split()[-2]):
        cand = bykey.get(v["key"], [])
        if len(cand) != 1:
            print(f"UNMAPPED old={h} candidates={len(cand)}")
            bad += 1
            continue
        n = cand[0]
        mapping[h] = n
    for h, n in mapping.items():
        o, w = old[h], new[n]
        mp = [mapping.get(p, p) for p in o["parents"]]
        par_ok = mp == w["parents"]
        diff = git(mirror, "diff-tree", "-r", "--no-renames", o["tree"], w["tree"])
        items = []
        for line in diff.splitlines():
            meta, path = line.split("\t", 1)
            _, _, ob, nb, st = meta.split()
            if st == "M":
                d = git(mirror, "diff", "-U0", ob, nb).splitlines()
                rem = [x for x in d if x.startswith("-") and not x.startswith("---")]
                add = [x for x in d if x.startswith("+") and not x.startswith("+++")]
                hit = sum(1 for x in rem if any(p.search(x) for p in pats))
                items.append(f"M {red(path)} -{len(rem)}(term-lines {hit}) +{len(add)}")
            else:
                items.append(f"{st} {red(path)}")
        same_tree = o["tree"] == w["tree"]
        print(f"old={h[:12]} new={n[:12]} author/committer/message=identical "
              f"parents-mapped={'yes' if par_ok else 'NO'} "
              f"tree={'identical' if same_tree else 'differs: ' + '; '.join(items)}")
        if not par_ok:
            bad += 1
    unchanged = sorted(h for h in new if h in allc and h not in mapping.values())
    for h in unchanged:
        print(f"UNCHANGED-HASH new={h[:12]} (also present before the rewrite)")
    print(f"old={len(old)} new={len(new)} mapped={len(mapping)} "
          f"unchanged={len(unchanged)} problems={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
