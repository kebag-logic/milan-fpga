#!/usr/bin/env python3
"""R242 offline fixture matrix for #423 (disposable, deterministic Git repos).

    python3 -B fixtures.py TRUSTED_CHECKER PROTOTYPE_CHECKER FIXTURE_ROOT OUT.json

Builds one fresh repository per scenario under FIXTURE_ROOT (fixed identities
and dates, so object IDs are reproducible for a given Git), then runs BOTH the
unchanged trusted checker and the SCRATCH prototype through their real CLI
(`--no-fetch --base main <branch>`) and records the actual exit codes and
verdict lines, plus the prototype's G/H/T components.  Exit 0 only when every
observed outcome equals the expectation written next to its scenario.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

TRUSTED, PROTO, ROOT, OUT = (os.path.abspath(a) for a in sys.argv[1:5])
BASE_ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                GIT_COMMITTER_NAME="Fixture",
                GIT_COMMITTER_EMAIL="fixture@example.invalid", LC_ALL="C")
TICK = [1790000000]


def env():
    TICK[0] += 60
    e = dict(BASE_ENV)
    e["GIT_AUTHOR_DATE"] = e["GIT_COMMITTER_DATE"] = f"@{TICK[0]} +0000"
    return e


def git(*args, check=True):
    p = subprocess.run(["git", "-c", "commit.gpgsign=false", "-c",
                        "core.autocrlf=false", *args], env=env(),
                       capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {args}: {p.stderr}")
    return p.stdout.strip()


def write(path, text, mode=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(text if isinstance(text, bytes) else text.encode())
    if mode:
        os.chmod(path, mode)


def read(path):
    with open(path) as fh:
        return fh.read()


def commit(msg):
    git("add", "-A")
    git("commit", "-q", "-m", msg)
    return git("rev-parse", "HEAD")


def replace_line(path, old, new):
    text = read(path)
    assert text.count(old) >= 1, (path, old)
    write(path, text.replace(old, new, 1))


MOD = "".join(f"line {i:02d}\n" for i in range(1, 41))
ADDED = ('def stage(work, tag, mutate=None):\n    """Stage one suite."""\n'
         '    return work / tag\n\n\n'
         'def build(suite):\n    """Build one suite."""\n    return suite\n\n\n'
         'def main():\n    return 0\n')


def seed():
    """O, the PR61-like incoming commit A, redundant merge M, PR62-like C."""
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD)
    write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    write("added.py", ADDED)
    a = commit("A original (PR61-like)")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "-m", "M redundant merge of incoming", "incoming")
    m = git("rev-parse", "HEAD")
    replace_line("added.py", "    return work / tag\n",
                 '    return work / f"suite_{tag}"\n')
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C original (PR62-like)")
    return dict(O=o, A=a, M=m, C=c)


def replay(ids, with_c=True, c_mutator=None):
    """Target history: A', redundant M', C' on a side branch, merge M2'."""
    git("checkout", "-q", "main")
    git("checkout", "-q", "-b", "replay-a", ids["O"])
    git("cherry-pick", ids["A"])
    git("commit", "-q", "--amend", "-m", "A' replay")
    git("checkout", "-q", "main")
    git("merge", "-q", "--no-ff", "-m", "M' replayed redundant merge", "replay-a")
    if not with_c:
        return
    git("checkout", "-q", "-b", "replay-c", "main")
    if c_mutator is None:
        git("cherry-pick", ids["C"])
        git("commit", "-q", "--amend", "-m", "C' replay")
    else:
        c_mutator()
        commit("C' altered replay")
    git("checkout", "-q", "main")
    git("merge", "-q", "--no-ff", "-m", "M2' replayed PR merge", "replay-c")


def later(msg, fn):
    git("checkout", "-q", "main")
    fn()
    return commit(msg)


def far_extension():
    replace_line("mod.txt", "line 35\n", "line 35 later extension\n")


def s_positive():
    ids = seed(); replay(ids)
    later("L far extension of a touched file", far_extension)


def s_positive_two_later():
    ids = seed(); replay(ids)
    later("L far extension", far_extension)
    later("L2 unrelated new file", lambda: write("new.txt", "new\n"))


def s_pr62_faithful():
    ids = seed(); replay(ids)

    def rewrite():
        replace_line("added.py", "def stage(work, tag, mutate=None):\n",
                     "def stage(work: Path, tag: str, mutate=None) -> Path:\n")
        far_extension()
    later("L annotate a PR-introduced line (0ac3e2c-like) + far edit", rewrite)


def s_adjacent_extension():
    ids = seed(); replay(ids)
    later("L extension adjacent to the replayed hunk", lambda: replace_line(
        "mod.txt", "line 05 changed by A\n",
        "line 05 changed by A\nline 05b later extension\n"))


def s_no_later():
    ids = seed(); replay(ids)


def _revert_c():
    git("checkout", "-q", "main")
    git("revert", "--no-edit", "main^2")


def s_revert_all():
    ids = seed(); replay(ids)
    _revert_c()
    git("revert", "--no-edit", git("rev-parse", "main~2^2"))


def s_revert_c():
    ids = seed(); replay(ids)
    _revert_c()


def s_revert_partial_hunk():
    ids = seed(); replay(ids)
    later("L restore only the A hunk of mod.txt", lambda: replace_line(
        "mod.txt", "line 05 changed by A\n", "line 05\n"))


def s_revert_plus_extension():
    ids = seed(); replay(ids)
    _revert_c()
    later("L far extension after revert", far_extension)


def s_revert_then_reapply():
    ids = seed(); replay(ids)
    _revert_c()
    git("revert", "--no-edit", "HEAD")


def s_omit_linear():
    ids = seed(); replay(ids, with_c=False)
    later("L far extension", far_extension)


def s_omit_partial():
    ids = seed()

    def only_added():
        replace_line("added.py", "    return work / tag\n",
                     '    return work / f"suite_{tag}"\n')
    replay(ids, c_mutator=only_added)
    later("L far extension", far_extension)


def s_whitespace():
    ids = seed()

    def spaced():
        replace_line("added.py", "    return work / tag\n",
                     '    return work /  f"suite_{tag}"\n')
        replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    replay(ids, c_mutator=spaced)
    later("L far extension", far_extension)


def _seed_resolution():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    write("added.py", ADDED)
    a = commit("A original")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "--no-commit", "incoming")
    write("resolution.txt", "resolution work only in the merge\n")
    git("add", "-A"); git("commit", "-q", "-m", "M merge WITH resolution work")
    m = git("rev-parse", "HEAD")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C original")
    return dict(O=o, A=a, M=m, C=c)


def s_resolution_missing():
    ids = _seed_resolution(); replay(ids)
    later("L far extension", far_extension)


def s_resolution_present():
    ids = _seed_resolution(); replay(ids)
    later("L resolution content landed separately",
          lambda: write("resolution.txt", "resolution work only in the merge\n"))
    later("L far extension", far_extension)


def s_octopus():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "in1")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    a = commit("A")
    git("checkout", "-q", "-b", "in2", o)
    write("added.py", ADDED)
    a2 = commit("A2")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "-m", "octopus", "in1", "in2")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    for x in (a, a2, c):
        git("cherry-pick", x)
    later("L far extension", far_extension)


def s_octopus_absorbed():
    """Octopus whose tree equals its second parent: only the count refuses."""
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    write("keep.txt", "keep A\n")
    a = commit("A")
    git("checkout", "-q", "-b", "side", o)
    write("keep.txt", "keep A\n")
    x = commit("X (its change is also inside A)")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "-m", "octopus absorbing X", "incoming", "side")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "-b", "replay-x", o)
    git("cherry-pick", x)
    git("checkout", "-q", "main")
    git("cherry-pick", a)
    git("merge", "-q", "--no-ff", "-m", "merge X replay", "replay-x")
    git("cherry-pick", c)
    later("L far extension", far_extension)


def s_disabling_rewrite():
    ids = seed(); replay(ids)
    later("L rewrite a PR-introduced line to disable it", lambda: replace_line(
        "added.py", "def main():\n    return 0\n",
        "def main():\n    raise SystemExit('disabled')\n"))


def s_unrelated_parent():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "--orphan", "unrelated")
    git("rm", "-q", "-rf", ".")
    write("u.txt", "unrelated history\n")
    u = commit("U unrelated root")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "--allow-unrelated-histories", "-m",
        "merge unrelated root", "unrelated")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    write("u.txt", "unrelated history\n"); commit("u.txt landed linearly")
    git("cherry-pick", c)
    later("L far extension", far_extension)


def _seed_multi(redundant_second=True):
    ids = seed()
    git("checkout", "-q", "-b", "side2", ids["C"])
    replace_line("mod.txt", "line 30\n", "line 30 changed by D\n")
    d = commit("D")
    git("checkout", "-q", "pr")
    if not redundant_second:
        git("checkout", "-q", "-b", "side3", ids["M"])
        write("x.txt", "x\n")
        commit("X diverging from M")
        git("checkout", "-q", "pr")
        git("merge", "-q", "--no-ff", "-m", "M2 non-redundant", "side3")
    else:
        git("merge", "-q", "--no-ff", "-m", "M2 second redundant merge", "side2")
    replace_line("added.py", "def main():\n    return 0\n",
                 "def main():\n    return 1\n")
    e = commit("E")
    return ids, d, e


def s_multi_redundant():
    ids, d, e = _seed_multi()
    replay(ids)
    git("checkout", "-q", "main")
    git("cherry-pick", d); git("cherry-pick", e)
    later("L far extension", far_extension)


def s_mixed_merges():
    ids, d, e = _seed_multi(redundant_second=False)
    replay(ids)
    git("checkout", "-q", "main")
    write("x.txt", "x\n"); commit("X landed")
    git("cherry-pick", e)
    later("L far extension", far_extension)


def s_distance_two():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A1\n")
    a1 = commit("A1")
    write("added.py", ADDED)
    a2 = commit("A2")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "-m", "M of a two-commit branch", "incoming")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    for x in (a1, a2, c):
        git("cherry-pick", x)
    later("L far extension", far_extension)


def s_evil_byte():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    a = commit("A")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "--no-commit", "incoming")
    replace_line("mod.txt", "line 10\n", "line 10 \n")
    git("add", "-A"); git("commit", "-q", "-m", "M with a one-byte evil change")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    git("cherry-pick", a); git("cherry-pick", c)
    later("L far extension", far_extension)


def s_reversed_parents():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    replace_line("mod.txt", "line 03\n", "line 03 base\n")
    o2 = commit("O2")
    git("checkout", "-q", "-b", "incoming")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    a = commit("A")
    tree = git("rev-parse", a + "^{tree}")
    m = git("commit-tree", tree, "-p", a, "-p", o2, "-m",
            "M: incoming first, its parent second")
    git("checkout", "-q", "-b", "pr", m)
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    git("cherry-pick", a); git("cherry-pick", c)
    later("L far extension", far_extension)


def s_linear_revert_control():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "pr")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    a = commit("A")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    git("cherry-pick", a); git("cherry-pick", c)
    git("revert", "--no-edit", "HEAD"); git("revert", "--no-edit", "HEAD~2")


def s_linear_extension_control():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "pr")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    a = commit("A")
    git("checkout", "-q", "main")
    git("cherry-pick", a)
    later("L adjacent extension", lambda: replace_line(
        "mod.txt", "line 05 changed by A\n", "line 05 changed by A\nline 05b\n"))


def s_mode_loss():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    write("tool.sh", "#!/bin/sh\necho tool\n", 0o755)
    a = commit("A adds an executable")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "-m", "M redundant", "incoming")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    git("cherry-pick", a); git("cherry-pick", c)
    later("L drops the executable bit", lambda: os.chmod("tool.sh", 0o644))


def s_binary_later_edit():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD); write("keep.txt", "keep\n")
    write("data.bin", b"\x00\x01head\x00" + b"\x00" * 64 + b"tail\x00\n")
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    write("data.bin", b"\x00\x01HEAD\x00" + b"\x00" * 64 + b"tail\x00\n")
    a = commit("A edits a binary")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "-m", "M redundant", "incoming")
    replace_line("mod.txt", "line 20\n", "line 20 changed by C\n")
    c = commit("C")
    git("checkout", "-q", "main")
    git("cherry-pick", a); git("cherry-pick", c)
    later("L edits the binary elsewhere", lambda: write(
        "data.bin", b"\x00\x01HEAD\x00" + b"\x00" * 64 + b"TAIL\x00\n"))


def s_delete_later():
    ids = seed(); replay(ids)
    later("L deletes a touched file", lambda: os.remove("mod.txt"))


def s_hostile_config():
    ids = seed(); replay(ids)
    _revert_c()
    git("revert", "--no-edit", git("rev-parse", "main~2^2"))
    later("L attributes asking for an 'ours' merge driver",
          lambda: write(".gitattributes", "* merge=ours diff=quiet\n"))
    git("config", "merge.ours.driver", "true")
    git("config", "merge.ours.name", "always keep ours")
    git("config", "diff.quiet.textconv", "true")


def s_repeated_block():
    git("init", "-q", "-b", "main")
    block = "a\nb\nc\nold\nd\ne\nf\n"
    sep = "".join(f"separator-{i}\n" for i in range(10))
    write("rep.txt", block + sep + block); write("mod.txt", MOD)
    o = commit("O base")
    git("checkout", "-q", "-b", "incoming")
    replace_line("mod.txt", "line 05\n", "line 05 changed by A\n")
    a = commit("A")
    git("checkout", "-q", "-b", "pr", o)
    git("merge", "-q", "--no-ff", "-m", "M redundant", "incoming")
    write("rep.txt", (block + sep + block).replace("old", "new", 1))
    c = commit("C edits the FIRST block")
    git("checkout", "-q", "main")
    git("cherry-pick", a)
    before, after = read("rep.txt").rsplit("old", 1)
    write("rep.txt", before + "new" + after)
    commit("C' edits the SECOND block (same verbatim patch-id)")
    later("L far extension", far_extension)


# name: (builder, expected trusted rc/word, expected prototype rc/word, class)
SCENARIOS = [
    ("positive-replay-far-extension", s_positive, (1, "STRANDED"), (0, "contained"), "positive"),
    ("positive-replay-two-later-commits", s_positive_two_later, (1, "STRANDED"), (0, "contained"), "positive"),
    ("two-redundant-merges", s_multi_redundant, (1, "STRANDED"), (1, "STRANDED"), "conservative FN (one-merge cap; per-merge variant would accept)"),
    ("control-replay-no-later-edit", s_no_later, (0, "contained"), (0, "contained"), "control: existing path arm"),
    ("control-revert-then-reapply", s_revert_then_reapply, (0, "contained"), (0, "contained"), "control: existing path arm"),
    ("pr62-faithful-later-rewrite", s_pr62_faithful, (1, "STRANDED"), (1, "UNKNOWN"), "conservative FN (mirrors actual PR62)"),
    ("later-disabling-rewrite", s_disabling_rewrite, (1, "STRANDED"), (1, "UNKNOWN"), "negative: reversion by edit (twin of pr62-faithful)"),
    ("published-shape-adjacent-extension", s_adjacent_extension, (1, "STRANDED"), (1, "UNKNOWN"), "conservative FN (legit extension adjacent to a replayed hunk)"),
    ("later-deletion-of-touched-file", s_delete_later, (1, "STRANDED"), (1, "UNKNOWN"), "refused: later deletion removes replayed work"),
    ("later-exec-bit-loss", s_mode_loss, (1, "STRANDED"), (1, "UNKNOWN"), "refused: later exec-bit reversion"),
    ("later-binary-edit", s_binary_later_edit, (1, "STRANDED"), (1, "UNKNOWN"), "explicitly unresolved: binary later edit unmeasurable"),
    ("exact-revert-whole-replay", s_revert_all, (1, "STRANDED"), (1, "UNKNOWN"), "negative: later reversion"),
    ("exact-revert-pr-commit", s_revert_c, (1, "STRANDED"), (1, "UNKNOWN"), "negative: later reversion"),
    ("partial-revert-one-hunk", s_revert_partial_hunk, (1, "STRANDED"), (1, "UNKNOWN"), "negative: later reversion"),
    ("revert-plus-far-extension", s_revert_plus_extension, (1, "STRANDED"), (1, "UNKNOWN"), "negative: later reversion"),
    ("revert-under-hostile-merge-config", s_hostile_config, (1, "STRANDED"), (1, "UNKNOWN"), "negative: reversion + ours driver/textconv"),
    ("omitted-linear-commit", s_omit_linear, (1, "STRANDED"), (1, "STRANDED"), "negative: omitted linear work"),
    ("omitted-part-of-a-commit", s_omit_partial, (1, "STRANDED"), (1, "STRANDED"), "negative: omitted linear work"),
    ("whitespace-different-postimage", s_whitespace, (1, "STRANDED"), (1, "STRANDED"), "negative: whitespace"),
    ("repeated-block-other-location", s_repeated_block, (1, "STRANDED"), (1, "STRANDED"), "negative: hunk position"),
    ("merge-resolution-work-missing", s_resolution_missing, (1, "STRANDED"), (1, "STRANDED"), "negative: resolution work"),
    ("merge-resolution-work-present", s_resolution_present, (1, "STRANDED"), (1, "STRANDED"), "conservative FN (AC2 'unless')"),
    ("merge-one-byte-evil-change", s_evil_byte, (1, "STRANDED"), (1, "STRANDED"), "negative: resolution work"),
    ("octopus-merge", s_octopus, (1, "STRANDED"), (1, "STRANDED"), "negative: octopus"),
    ("octopus-absorbed-third-parent", s_octopus_absorbed, (1, "STRANDED"), (1, "STRANDED"), "conservative FN (scope: two parents only)"),
    ("unrelated-parent-merge", s_unrelated_parent, (1, "STRANDED"), (1, "STRANDED"), "negative: unrelated parent"),
    ("redundant-plus-nonredundant-merge", s_mixed_merges, (1, "STRANDED"), (1, "STRANDED"), "negative: multiple merges"),
    ("first-parent-is-grandparent", s_distance_two, (1, "STRANDED"), (1, "STRANDED"), "conservative FN (distance 2)"),
    ("reversed-parent-order", s_reversed_parents, (1, "STRANDED"), (1, "STRANDED"), "negative: shape"),
    ("linear-control-exact-revert", s_linear_revert_control, (0, "contained"), (0, "contained"), "pre-existing linear historical arm (unchanged)"),
    ("linear-control-adjacent-extension", s_linear_extension_control, (0, "contained"), (0, "contained"), "pre-existing linear historical arm (unchanged)"),
]


def run_checker(path, branch):
    p = subprocess.run([sys.executable, "-B", "-I", path, "--no-fetch", "--base",
                        "main", branch], capture_output=True, text=True,
                       env=dict(BASE_ENV))
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    return p.returncode, (lines[0].strip() if lines else p.stderr.strip()[:200])


def components(mod, branch):
    shape, why = mod._redundant_merge_shape(branch, "main")
    rep, err = mod._linear_patches_contained(branch, "main")
    ret, detail = mod._retained_at_tip(branch, "main")
    return {"G_shape": shape, "G_note": why, "H_replay": rep,
            "T_retained": ret, "T_detail": detail}


def main():
    os.environ.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    spec = importlib.util.spec_from_file_location("proto", PROTO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)
    os.makedirs(ROOT)
    rows, bad = [], 0
    for name, build, want_t, want_p, klass in SCENARIOS:
        repo = os.path.join(ROOT, name)
        os.makedirs(repo)
        os.chdir(repo)
        TICK[0] = 1790000000
        build()
        branch = "pr"
        tip = git("rev-parse", "main")
        head = git("rev-parse", branch)
        t_rc, t_line = run_checker(TRUSTED, branch)
        p_rc, p_line = run_checker(PROTO, branch)
        comp = components(mod, branch)
        ok = (t_rc == want_t[0] and want_t[1] in t_line
              and p_rc == want_p[0] and want_p[1] in p_line)
        bad += not ok
        rows.append({"scenario": name, "class": klass, "branch_head": head,
                     "base_tip": tip, "trusted_rc": t_rc, "trusted": t_line,
                     "prototype_rc": p_rc, "prototype": p_line, **comp,
                     "expected": {"trusted": want_t, "prototype": want_p},
                     "as_expected": ok})
        print(f"{'ok  ' if ok else 'FAIL'} {name:<38} trusted rc={t_rc} "
              f"proto rc={p_rc} G={comp['G_shape']} H={comp['H_replay']} "
              f"T={comp['T_retained']} :: {p_line[:150]}")
    with open(OUT, "w") as fh:
        json.dump({"git": subprocess.run(["git", "--version"], capture_output=True,
                                         text=True).stdout.strip(),
                   "rows": rows}, fh, indent=1)
    print("RESULT", "PASS" if not bad else f"FAIL ({bad})")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
