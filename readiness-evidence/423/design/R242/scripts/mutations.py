#!/usr/bin/env python3
"""Mutation check: is every guard of the candidate arm load-bearing?

    python3 -B mutations.py PROTOTYPE_CHECKER FIXTURE_ROOT

Re-evaluates contained("refs/heads/pr", "refs/heads/main") in every fixture
repository built by fixtures.py, first with the prototype as written and then
with one guard weakened at a time.  A mutation is KILLED when at least one
fixture's verdict class (contained / UNKNOWN / STRANDED) changes.  Exit 0 only
when every mutation is killed.
"""
import importlib.util
import os
import sys

PROTO, ROOT = (os.path.abspath(a) for a in sys.argv[1:3])
os.environ.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, LC_ALL="C")
spec = importlib.util.spec_from_file_location("proto", PROTO)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ORIG = {n: getattr(mod, n) for n in ("_redundant_merge_shape", "_retained_at_tip",
                                     "_redundant_merge_replay_verdict",
                                     "_merge_is_noop")}


def shape_variant(count=True, parent=True, tree=True, cap=True):
    def shape(branch, base):
        rc, out = mod._git("rev-list", "--min-parents=2", "--parents",
                           f"{base}..{branch}")
        rows = [line.split() for line in out.splitlines() if line.strip()]
        if not rows or (cap and len(rows) != 1):
            return (False, "merge count")
        for merge, *parents in rows:
            if count and len(parents) != 2:
                return (False, "count")
            first, second = parents[0], parents[1]
            fields = mod._git("rev-list", "--parents", "--max-count=1", second)[1].split()
            if parent and fields[1:] != [first]:
                return (False, "parent")
            if tree and (mod._git("rev-parse", merge + "^{tree}")[1]
                         != mod._git("rev-parse", second + "^{tree}")[1]):
                return (False, "tree")
        return (True, None)
    return shape


def verdict_variant(use_h=True, use_t=True):
    def verdict(branch, base, ahead):
        shape, why = mod._redundant_merge_shape(branch, base)
        if shape is None:
            return (None, None, why)
        if not shape:
            return None
        if use_h:
            replayed, err = mod._linear_patches_contained(branch, base)
            if replayed is None:
                return (None, None, err)
            if not replayed:
                return None
        if use_t:
            retained, detail = mod._retained_at_tip(branch, base)
            if retained is None:
                return (None, None, "unmeasurable")
            if not retained:
                return (None, None, "not retained")
        return (True, ahead, "candidate")
    return verdict


def noop_variant(compare=True, errors_ok=False):
    def noop(o, t, b):
        same, err = ORIG["_merge_is_noop"](o, t, b)
        if err:
            return (True, None) if errors_ok else (None, err)
        if not compare:
            # clean-only: ask merge-file again and ignore the tip comparison
            import subprocess, tempfile
            blobs = [b"" if e is None else mod._blob(e[2])[0] for e in (t, o, b)]
            with tempfile.TemporaryDirectory() as td:
                names = []
                for i, data in enumerate(blobs):
                    names.append(os.path.join(td, str(i)))
                    with open(names[-1], "wb") as fh:
                        fh.write(data)
                p = subprocess.run(("git", "merge-file", "-p", "-q", *names),
                                   capture_output=True)
            return (p.returncode == 0, None)
        return (same, None)
    return noop


def retained_variant(mode=True, exact_only=False):
    orig = ORIG["_retained_at_tip"]

    def retained(branch, base):
        if exact_only:
            rc, out = mod._git("merge-base", "--all", base, branch)
            mb = out.split()[0]
            rc, names = mod._git("diff", *mod.RAW_DIFF_FLAGS, "--name-only",
                                 "--no-renames", "-z", mb, branch)
            lost = [p for p in names.split("\0") if p and
                    mod._tree_entry(base, p)[0] != mod._tree_entry(branch, p)[0]]
            return (not lost, lost)
        if not mode:
            saved = mod._tree_entry

            def entry(commit, path):
                e, err = saved(commit, path)
                return ((("100644",) + e[1:]) if e else e, err)
            mod._tree_entry = entry
            try:
                return orig(branch, base)
            finally:
                mod._tree_entry = saved
        return orig(branch, base)
    return retained


MUTATIONS = {
    "G: admit any number of merges": {"_redundant_merge_shape": shape_variant(cap=False)},
    "G: accept any parent count": {"_redundant_merge_shape": shape_variant(count=False)},
    "G: drop first-parent==parent(second)": {"_redundant_merge_shape": shape_variant(parent=False)},
    "G: drop merge-tree==second-tree": {"_redundant_merge_shape": shape_variant(tree=False)},
    "H: skip replay proof": {"_redundant_merge_replay_verdict": verdict_variant(use_h=False)},
    "T: skip retention (published shortcut)": {"_redundant_merge_replay_verdict": verdict_variant(use_t=False)},
    "T: exact tip equality only": {"_retained_at_tip": retained_variant(exact_only=True)},
    "T: ignore file modes": {"_retained_at_tip": retained_variant(mode=False)},
    "T: clean merge without tip comparison": {"_merge_is_noop": noop_variant(compare=False)},
    "T: merge errors count as retained": {"_merge_is_noop": noop_variant(errors_ok=True)},
}


def classify(ok):
    return {True: "contained", None: "UNKNOWN", False: "STRANDED"}[ok]


def evaluate():
    out = {}
    for name in sorted(os.listdir(ROOT)):
        os.chdir(os.path.join(ROOT, name))
        ok, _ahead, _note = mod.contained("refs/heads/pr", "refs/heads/main")
        out[name] = classify(ok)
    return out


def main():
    base = evaluate()
    print("baseline:", {k: v for k, v in base.items()})
    survivors = 0
    for label, patch in MUTATIONS.items():
        for n, f in patch.items():
            setattr(mod, n, f)
        try:
            got = evaluate()
        finally:
            for n in ORIG:
                setattr(mod, n, ORIG[n])
        killed = {k: f"{base[k]}->{v}" for k, v in got.items() if v != base[k]}
        survivors += not killed
        print(f"{'KILLED  ' if killed else 'SURVIVED'} {label}: {killed}")
    print("RESULT", "PASS" if not survivors else f"FAIL ({survivors} survived)")
    return 0 if not survivors else 1


if __name__ == "__main__":
    sys.exit(main())
