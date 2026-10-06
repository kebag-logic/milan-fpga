#!/usr/bin/env python3
"""Reproduce the read-only composition proof; run from the candidate checkout."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
HEAD = "fa1294279c42f181b6f43c6e6bd812039798705c"
TREE = "610669663833b6aad15ef9cb3e5b312c929c6994"
PARENT = "9e05246c5455b2a1df26038345709437e13c6f18"
SOURCE = "d763fce6f3e48fa9c468aaa835653befb8382d06"
LIVE = "a1e9839e909c2e44fd47307588fbf9da8c28fd53"
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*args):
    return subprocess.run(["git", "-c", "core.commitGraph=false", *args],
                          env=ENV, check=True, capture_output=True).stdout


def tree(rev):
    records = git("ls-tree", "-rz", rev).split(b"\0")
    return {p.decode(): meta.decode().split() for entry in records if entry
            for meta, p in [entry.split(b"\t", 1)]}


def changed(a, b):
    return sorted(p for p in a.keys() | b.keys() if a.get(p) != b.get(p))


def main():
    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
    assert git("show", "-s", "--format=%P", HEAD).decode().split() == [PARENT, SOURCE]
    assert git("rev-parse", PARENT + "^{tree}") == git("rev-parse", LIVE + "^{tree}")
    base = git("merge-base", PARENT, SOURCE).decode().strip()
    b, p, s, h = map(tree, [base, PARENT, SOURCE, HEAD])
    pred, src = changed(b, p), changed(b, s)
    overlap = sorted(set(pred) & set(src))
    assert overlap == ["docs/README.md"], overlap
    for path in set(src) - set(pred):
        assert h.get(path) == s.get(path), path
    for path in set(pred) - set(src):
        assert h.get(path) == p.get(path), path
    for path in (b.keys() | h.keys()) - set(src) - set(pred):
        assert h.get(path) == b.get(path), path
    doc = git("show", HEAD + ":docs/README.md").decode()
    f1 = "| Review the firmware saved-state store | [Saved-state store, F1](../sw/firmware/ctrl_nvm/README.md) |\n"
    f0 = "| Review the firmware mailbox | [Packet mailbox split, F0](design/MAILBOX_SPLIT.md) |\n"
    assert doc.count(f0) == doc.count(f1) == 1
    assert doc.replace(f1, "").encode() == git("show", PARENT + ":docs/README.md")
    assert doc.replace(f0, "").encode() == git("show", SOURCE + ":docs/README.md")
    assert doc.index("## Architecture and integration") < doc.index(f1)
    assert doc.index(f1) < doc.index("| Review saved-state snapshot ownership")
    assert doc.index("| Review saved-state materialization") < doc.index(f0) < doc.index("## Verification")
    for target in ["../sw/firmware/ctrl_nvm/README.md", "design/MAILBOX_SPLIT.md"]:
        assert (Path("docs") / target).is_file(), target
    receipt = {
        "head": HEAD, "tree": TREE, "ordered_parents": [PARENT, SOURCE],
        "live_dev": LIVE, "first_parent_tree_equals_live_dev": True,
        "common_ancestor": base, "predecessor_changed_paths": pred,
        "source_changed_paths": src, "overlapping_paths": overlap,
        "source_only_paths_identical_to_reviewed_source": len(set(src) - set(pred)),
        "predecessor_only_paths_identical_to_reviewed_predecessor": len(set(pred) - set(src)),
        "unchanged_paths_identical_to_common_ancestor": True,
        "index_is_exact_union_preserving_both_parent_orders": True,
        "both_index_targets_exist": True,
        "candidate_gitlinks": {k: v for k, v in h.items() if v[0] == "160000"},
        "result": "PASS",
    }
    for name, args in [
        ("candidate.diff", ["diff", "--no-ext-diff", "--no-textconv", "--no-renames", PARENT, HEAD]),
        ("composition-history.log", ["log", "--format=%H %P %s", "--name-status", base + ".." + HEAD]),
        ("index-composition.diff", ["diff", "--no-ext-diff", "--no-textconv", base, HEAD, "--", "docs/README.md"]),
    ]:
        (PACKET / name).write_bytes(git(*args))
    (PACKET / "composition.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
