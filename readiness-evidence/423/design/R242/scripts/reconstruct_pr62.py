#!/usr/bin/env python3
"""Reconstruct public FPGA-gPTP PR62 history and measure it (read-only).

    git clone --mirror https://github.com/Mister-M-alt/FPGA-gPTP.git DONOR
    python3 -B reconstruct_pr62.py DONOR TRUSTED_CHECKER PROTOTYPE_CHECKER OUT.json

Reports topology, the redundant-merge shape (G), a tree-identical
parent-isomorphic replay map, raw patch hashes, verbatim patch IDs, the
existing linear replay proof (H), retention at each target tip (T) path by
path, the later commits that touched those paths, and the real CLI exit codes
of the unchanged checker and of the SCRATCH prototype at both targets.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

DONOR, TRUSTED, PROTO, OUT = (os.path.abspath(a) for a in sys.argv[1:5])
HEAD = "3db86812096830fada2f5f276fa5f4d9f37d1d14"
TARGETS = {"issue-base f0f1c055": "f0f1c055ee5226f08e656c27cb1bf4c355be11ae",
           "live-main c1b61743": "c1b617435824929a790739ea8585c3fe1a328cc0"}
ISSUE_PATCH_SHA256 = {
    "3db86812096830fada2f5f276fa5f4d9f37d1d14":
        "fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f",
    "9790ac736e6d10301ad814ffdf73dbe37b59768b":
        "d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3"}
REPLAYS = {"9790ac736e6d10301ad814ffdf73dbe37b59768b":
           "20927af74752620b2ad0f973e8be3203994b5547",
           "3db86812096830fada2f5f276fa5f4d9f37d1d14":
           "5602e70bb4cf70c2e0e39e846e26925e27659e32"}
ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           LC_ALL="C")


def git(*args, raw=False):
    p = subprocess.run(["git", "--no-replace-objects", *args], env=ENV,
                       capture_output=True, text=not raw)
    return p.returncode, (p.stdout if raw else p.stdout.strip())


def parents(c):
    return git("rev-list", "--parents", "--max-count=1", c)[1].split()[1:]


def tree(c):
    return git("rev-parse", c + "^{tree}")[1]


def patch_variants(c):
    p = parents(c)[0]
    flags = ("--no-ext-diff", "--no-textconv", "--no-renames")
    out = {}
    for name, args in {
        "diff --binary --full-index": ("diff", *flags, "--binary", "--full-index", p, c),
        "diff (default)": ("diff", *flags, p, c),
        "show --format= --binary --full-index": ("show", *flags, "--format=",
                                                 "--binary", "--full-index", c),
        "diff-tree -p --no-commit-id --binary --full-index":
            ("diff-tree", "-p", *flags, "--no-commit-id", "--binary", "--full-index", c),
    }.items():
        rc, data = git(*args, raw=True)
        out[name] = hashlib.sha256(data).hexdigest() if rc == 0 else f"rc={rc}"
    return out


def tir_map(head, target):
    """Tree-identical, parent-isomorphic replay map (branch -> target)."""
    rc, out = git("rev-list", "--reverse", "--topo-order", f"{target}..{head}")
    branch = out.split()
    rc, out = git("rev-list", f"{head}..{target}")
    side = out.split()
    by_tree = {}
    for c in side:
        by_tree.setdefault(tree(c), []).append(c)
    mapping = {}
    for c in branch:
        want = [mapping.get(p, p) for p in parents(c)]
        hits = [x for x in by_tree.get(tree(c), []) if parents(x) == want]
        mapping[c] = hits[0] if len(hits) == 1 else (hits or None)
    return mapping


def main():
    os.environ.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    spec = importlib.util.spec_from_file_location("proto", PROTO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    os.chdir(DONOR)
    facts = {"git": git("--version")[1], "head": HEAD,
             "pr62_merge_commit_f5ba2db6_present":
                 git("cat-file", "-e", "f5ba2db636112d1292671b49a047c9fd9daacf7e")[0] == 0}
    interesting = ["7fa64e99490b4648797374d3fdb1fedf08145e91",
                   "9790ac736e6d10301ad814ffdf73dbe37b59768b",
                   "f27b45500cb02a5277b5cb32cef408658c1f914e", HEAD,
                   "20927af74752620b2ad0f973e8be3203994b5547",
                   "377b8c428b226a796adde099fe07152151fd6c5d",
                   "5602e70bb4cf70c2e0e39e846e26925e27659e32",
                   "676d2f6be46b2775b8a008800d394c9855a5efc3"]
    facts["commits"] = {c: {"parents": parents(c), "tree": tree(c)} for c in interesting}
    facts["patches"] = {}
    for orig, rep in REPLAYS.items():
        vo, vr = patch_variants(orig), patch_variants(rep)
        facts["patches"][orig] = {
            "replay": rep, "variants_equal": vo == vr,
            "issue_sha256": ISSUE_PATCH_SHA256[orig],
            "issue_sha256_matches_variant": [k for k, v in vo.items()
                                             if v == ISSUE_PATCH_SHA256[orig]],
            "variants": vo,
            "verbatim_patch_id": [mod._verbatim_patch_id(orig)[0],
                                  mod._verbatim_patch_id(rep)[0]]}
    facts["targets"] = {}
    for label, target in TARGETS.items():
        rc, mbs = git("merge-base", "--all", target, HEAD)
        rc, rng = git("rev-list", "--parents", f"{target}..{HEAD}")
        shape = mod._redundant_merge_shape(HEAD, target)
        replay = mod._linear_patches_contained(HEAD, target)
        retained = mod._retained_at_tip(HEAD, target)
        mb = mbs.split()[0]
        rc, names = git("diff", "--no-ext-diff", "--no-textconv", "--name-only",
                        "--no-renames", "-z", mb, HEAD)
        paths = [n for n in names.split("\0") if n]
        per_path = {}
        for p in paths:
            ents = [mod._tree_entry(c, p)[0] for c in (mb, target, HEAD)]
            noop = (None if ents[1] == ents[2] else mod._merge_is_noop(*ents))
            rc, later = git("log", "--format=%H %s", "--no-renames",
                            f"{REPLAYS[HEAD]}..{target}", "--", p)
            per_path[p] = {"merge_base": ents[0], "tip": ents[1], "head": ents[2],
                           "tip_equals_head": ents[1] == ents[2],
                           "merge_file_noop": noop, "later_commits": later.splitlines()}
        cli = {}
        for name, path in (("trusted", TRUSTED), ("prototype", PROTO)):
            p = subprocess.run([sys.executable, "-B", "-I", path, "--no-fetch",
                                "--base", target, HEAD], capture_output=True,
                               text=True, env=ENV)
            cli[name] = {"rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
        facts["targets"][label] = {
            "target": target, "merge_bases": mbs.split(), "range_with_parents":
            rng.splitlines(), "G_shape": shape, "H_linear_replay": replay,
            "T_retained": retained, "tir_map": tir_map(HEAD, target),
            "paths": per_path, "cli": cli}
    with open(OUT, "w") as fh:
        json.dump(facts, fh, indent=1)
    for label, t in facts["targets"].items():
        print(f"== {label}: G={t['G_shape']} H={t['H_linear_replay']} "
              f"T={t['T_retained']}")
        print(f"   tir_map={t['tir_map']}")
        for name in ("trusted", "prototype"):
            first = (t["cli"][name]["stdout"].strip().splitlines() or [""])[0]
            print(f"   {name}: rc={t['cli'][name]['rc']} {first}")
    for orig, p in facts["patches"].items():
        print(f"patch {orig[:8]}->{p['replay'][:8]} equal={p['variants_equal']} "
              f"issue-hash-matches={p['issue_sha256_matches_variant']} "
              f"patch-id={p['verbatim_patch_id']}")
    print("f5ba2db6 present:", facts["pr62_merge_commit_f5ba2db6_present"])


if __name__ == "__main__":
    main()
