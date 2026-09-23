#!/usr/bin/env python3
"""AC4: classification of every tracked Markdown page under three walks.

Usage: corpus_ac4.py OUT.json TREE...
Walks: base 88e9276b (single module), start 4741498f (single module), and the
working tree's walk (gen_toc.py with its two walk modules). For each tree
(a commit, or WORKTREE for the checkout) every tracked *.md page is
classified by each walk: refusals, blocks, line_kinds, headings with anchors,
plan, generated_block and owns. A difference between walks on any page and
field is reported by page and field.
"""
import hashlib, importlib.util, json, subprocess, sys, tempfile
from pathlib import Path

REPO = "$LANES/437-container-paragraph-scopes"
WALKS = {"base-88e9276b": "88e9276b2a220c716f64a843f7e1eb8f9265e896",
         "start-4741498f": "4741498f3b2b4f67f431037d327c96cf65691278"}


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], check=True, capture_output=True).stdout


def load_rev(rev, tag):
    d = Path(tempfile.mkdtemp(prefix=f"ac4.{tag}."))
    (d / "gen_toc.py").write_bytes(git("show", f"{rev}:scripts/gen_toc.py"))
    spec = importlib.util.spec_from_file_location(f"gen_toc_{tag.replace('-', '_')}", d / "gen_toc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def classify(mod, rel, text):
    ref = mod.refusals(text)
    row = {"refusals": ref, "owns": mod.owns(rel, text)}
    if not ref:
        row.update(blocks=mod.blocks(text), line_kinds=mod.line_kinds(text),
                   headings=mod.headings(text), plan=mod.plan(text),
                   generated_block=mod.generated_block(text, rel))
    return row


def pages(tree):
    if tree == "WORKTREE":
        names = [n for n in git("ls-files", "-z", "*.md").decode().split("\0") if n]
        return {n: (Path(REPO) / n).read_text() for n in names if (Path(REPO) / n).is_file()}
    names = [n for n in git("ls-tree", "-r", "-z", "--name-only", tree).decode().split("\0")
             if n.endswith(".md")]
    return {n: git("show", f"{tree}:{n}").decode() for n in names}


def main():
    out, trees = Path(sys.argv[1]), sys.argv[2:]
    walks = {name: load_rev(rev, name) for name, rev in WALKS.items()}
    sys.path.insert(0, f"{REPO}/scripts")
    import gen_toc
    walks["new-worktree"] = gen_toc
    report = {"walk_sources": {n: hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()
                               for n, m in walks.items()},
              "new_walk_modules": {n: hashlib.sha256((Path(REPO) / "scripts" / n).read_bytes()).hexdigest()
                                   for n in gen_toc.WALK_MODULES},
              "trees": {}}
    for tree in trees:
        texts = pages(tree)
        diffs, digests = [], {}
        rows = {name: {rel: classify(mod, rel, t) for rel, t in texts.items()} for name, mod in walks.items()}
        for name in walks:
            digests[name] = hashlib.sha256(json.dumps(rows[name], sort_keys=True, default=str).encode()).hexdigest()
        ref = rows["base-88e9276b"]
        for name in walks:
            for rel in texts:
                for field in ref[rel]:
                    if rows[name][rel].get(field) != ref[rel][field]:
                        diffs.append({"walk": name, "page": rel, "field": field})
        lines = sum(len(t.split("\n")) for t in texts.values())
        report["trees"][tree] = {"pages": len(texts), "lines": lines, "digests": digests,
                                 "differences": diffs}
        print(f"{tree}: {len(texts)} pages, {lines} lines, {len(diffs)} differences; digests "
              + " ".join(f"{k}={v[:12]}" for k, v in digests.items()))
        for d in diffs[:20]:
            print("   ", d)
    out.write_text(json.dumps(report, indent=1) + "\n")
    return 1 if any(t["differences"] for t in report["trees"].values()) else 0


if __name__ == "__main__":
    sys.exit(main())
