#!/usr/bin/env python3
"""Reviewer probe matrix for #514 (disposable, deterministic Git fixtures).

    python3 -B probe_matrix.py BASE_CHECKER HEAD_CHECKER R242_FIXTURES_PY ROOT OUT.json

For every R242 scenario (immutable fixtures.py from badb350c) plus reviewer-
written linear scenarios, build a fresh repository under ROOT and run through
the real CLI (`--no-fetch --base main pr`):
  * the base-commit checker, default options;
  * the head checker, default options;
  * the head checker with --current-retention.
Invariants checked:
  I1 base and head default exit codes and verdict words are identical;
  I2 --current-retention never lowers a default non-zero exit, and never
     prints `retained` unless the default line is `contained`;
  I3 each reviewer scenario's expected retention word and exit hold.
Exit 0 only when every invariant holds.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

BASE, HEAD, FIXTURES, ROOT, OUT = (os.path.abspath(a) for a in sys.argv[1:6])
sys.argv = [FIXTURES, BASE, HEAD, ROOT, OUT + ".r242-unused"]
spec = importlib.util.spec_from_file_location("r242", FIXTURES)
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
git, write, commit, replace_line, read = fx.git, fx.write, fx.commit, fx.replace_line, fx.read
MOD = fx.MOD


def _seed_linear(n_commits=2):
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    commit("O base")
    git("checkout", "-q", "-b", "pr")
    ids = []
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    ids.append(commit("A"))
    if n_commits > 1:
        replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
        write("new.py", "print('C')\n")
        ids.append(commit("C"))
    git("checkout", "-q", "main")
    for c in ids:
        git("cherry-pick", c)
    return ids


def r_fallback_replica():
    """Replica of selftest linear-patch-fallback (append after replay)."""
    git("init", "-q", "-b", "main")
    write("seed", "seed\n"); commit("base")
    git("checkout", "-q", "-b", "pr")
    write("linear", "landed\n"); c = commit("linear")
    git("checkout", "-q", "main")
    write("advance", "first"); commit("advance")
    git("cherry-pick", c)
    with open("linear", "a") as fh:
        fh.write("superseded\n")
    commit("supersede")


def r_two_commit_far_extension():
    _seed_linear()
    fx.later("L far extension", fx.far_extension)


def r_two_commit_revert_first():
    _seed_linear()
    git("revert", "--no-edit", "HEAD~1")


def r_rename_touched_file():
    _seed_linear()
    git("mv", "mod.txt", "moved.txt"); commit("L rename touched file")


def r_delete_added_file():
    _seed_linear()
    os.remove("new.py"); commit("L delete added file")


def r_revert_then_reapply():
    _seed_linear()
    git("revert", "--no-edit", "HEAD")
    git("revert", "--no-edit", "HEAD")


def r_hostile_config_revert():
    _seed_linear()
    git("revert", "--no-edit", "HEAD")
    write(".gitattributes", "* merge=ours diff=quiet\n"); commit("L attributes")
    git("config", "merge.ours.driver", "true")
    git("config", "diff.quiet.textconv", "true")


def r_repeated_block_moved():
    git("init", "-q", "-b", "main")
    block = "a\nb\nc\nold\nd\ne\nf\n"
    sep = "".join(f"separator-{i}\n" for i in range(10))
    write("rep.txt", block + sep + block); commit("O")
    git("checkout", "-q", "-b", "pr")
    write("rep.txt", (block + sep + block).replace("old", "new", 1))
    c = commit("C edits first block")
    git("checkout", "-q", "main")
    git("cherry-pick", c)
    text = read("rep.txt").replace("new", "old", 1)
    before, after = text.rsplit("old", 1)
    write("rep.txt", before + "new" + after); commit("L moves change to second block")


def r_exec_bit_source_then_lost():
    git("init", "-q", "-b", "main")
    write("tool.sh", "echo hi\n"); commit("O")
    git("checkout", "-q", "-b", "pr")
    os.chmod("tool.sh", 0o755); c = commit("make executable")
    git("checkout", "-q", "main")
    git("cherry-pick", c)
    os.chmod("tool.sh", 0o644); commit("L drops exec bit")


def r_ancestry_merge():
    git("init", "-q", "-b", "main")
    write("f", "1\n"); commit("O")
    git("checkout", "-q", "-b", "pr")
    write("f", "2\n"); commit("A")
    git("checkout", "-q", "main")
    write("g", "x\n"); commit("other")
    git("merge", "-q", "--no-ff", "-m", "merge pr", "pr")


def r_linear_no_later():
    _seed_linear()


# name: (builder, expected default word, expected retention word or None, expected option rc)
REVIEWER = [
    ("rv-fallback-replica", r_fallback_replica, "contained", "UNKNOWN", 1),
    ("rv-two-commit-no-later", r_linear_no_later, "contained", "retained", 0),
    ("rv-two-commit-far-extension", r_two_commit_far_extension, "contained", "retained", 0),
    ("rv-two-commit-revert-first", r_two_commit_revert_first, "contained", "UNKNOWN", 1),
    ("rv-rename-touched-file", r_rename_touched_file, "contained", "UNKNOWN", 1),
    ("rv-delete-added-file", r_delete_added_file, "contained", "UNKNOWN", 1),
    ("rv-revert-then-reapply", r_revert_then_reapply, "contained", "retained", 0),
    ("rv-hostile-config-revert", r_hostile_config_revert, "contained", "UNKNOWN", 1),
    ("rv-repeated-block-moved", r_repeated_block_moved, "contained", "UNKNOWN", 1),
    ("rv-exec-bit-lost", r_exec_bit_source_then_lost, "contained", "UNKNOWN", 1),
    ("rv-ancestry-merge", r_ancestry_merge, "contained", "UNKNOWN", 1),
]


def run(checker, *extra):
    p = subprocess.run([sys.executable, "-B", "-I", checker, "--no-fetch", "--base",
                        "main", "pr", *extra], capture_output=True, text=True,
                       env=dict(fx.BASE_ENV))
    return p.returncode, p.stdout, p.stderr


def first_word(out):
    lines = [l.split()[0] for l in out.splitlines() if l.strip()]
    return lines[0] if lines else ""


def retention_words(out):
    return [l.split()[0] for l in out.splitlines() if "current retention:" in l]


def main():
    os.environ.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)
    os.makedirs(ROOT)
    scenarios = [(n, b, None, None, None) for n, b, *_ in fx.SCENARIOS]
    scenarios += [(n, b, w, r, rc) for n, b, w, r, rc in REVIEWER]
    rows, bad = [], 0
    for name, build, want_word, want_ret, want_rc in scenarios:
        repo = os.path.join(ROOT, name)
        os.makedirs(repo); os.chdir(repo)
        fx.TICK[0] = 1790000000
        build()
        heads = {"pr": git("rev-parse", "pr"), "main": git("rev-parse", "main")}
        b_rc, b_out, b_err = run(BASE)
        h_rc, h_out, h_err = run(HEAD)
        o_rc, o_out, o_err = run(HEAD, "--current-retention")
        words = retention_words(o_out)
        problems = []
        if (b_rc, first_word(b_out)) != (h_rc, first_word(h_out)):
            problems.append("I1 default verdict/exit changed")
        if h_rc != 0 and o_rc != h_rc:
            problems.append("I2 option changed a non-zero default exit")
        if "retained" in words and first_word(h_out) != "contained":
            problems.append("I2 retained without contained")
        if o_rc == 0 and "UNKNOWN" in words:
            problems.append("I2 UNKNOWN with exit 0")
        if want_word is not None:
            if first_word(h_out) != want_word:
                problems.append(f"I3 default word {first_word(h_out)} != {want_word}")
            if (o_rc, words) != (want_rc, [want_ret]):
                problems.append(f"I3 option {(o_rc, words)} != {(want_rc, [want_ret])}")
        bad += bool(problems)
        rows.append({"scenario": name, "heads": heads,
                     "base_default": [b_rc, b_out, b_err],
                     "head_default": [h_rc, h_out, h_err],
                     "head_option": [o_rc, o_out, o_err],
                     "problems": problems})
        ret_line = next((l.strip() for l in o_out.splitlines() if "current retention:" in l), "-")
        print(f"{'ok  ' if not problems else 'FAIL'} {name:<36} pr={heads['pr'][:10]} "
              f"main={heads['main'][:10]} base={b_rc}/{first_word(b_out)} "
              f"head={h_rc}/{first_word(h_out)} opt={o_rc}/{words} :: {ret_line[:140]}"
              + (f" !! {problems}" if problems else ""))
    with open(OUT, "w") as fh:
        json.dump({"git": subprocess.run(["git", "--version"], capture_output=True,
                                         text=True).stdout.strip(), "rows": rows}, fh, indent=1)
    print("RESULT", "PASS" if not bad else f"FAIL ({bad})")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
