#!/usr/bin/env python3
"""Reviewer mutation campaign against the exact-head containment sources.

Usage: mutate.py <head-scripts-dir> <scratch-dir> <out.jsonl> <env-profile> [name...]

Each mutant copies the head scripts directory, applies exact byte edits (each
'before' must occur exactly once, else the mutant is reported unapplied), and
runs the default self-test in a fresh process.  Killed means the self-test
exits non-zero; the failing case names are recorded, and a crash inside the
self-test's own mutation harness is flagged so it is not counted as a kill by
a real control.  Profiles: default | nolocale (PATH without locale/localedef)
| ascii (ASCII parent).  At most 8 parallel jobs.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R = "merge_containment_replay.py"
G = "merge_containment_git.py"
C = "check_merge_containment.py"
M = "merge_containment_selftest_mutations.py"

MUTANTS = {
    "control-unmutated": [],
    # R244-A: byte transport and output guard
    "A1-lossy-output-guard-dropped": [(G, "if os.fsencode(text) != out:", "if False:")],
    "A2-commit-paths-text": [
        (C, 'rc, names = _git_raw("diff-tree"', 'rc, names = _git("diff-tree"'),
        (C, 'return ([name for name in names.split(b"\\0") if name], None)',
         'return ([name for name in names.split("\\0") if name], None)')],
    "A3-path-arm-text": [
        (C, 'rc, names = _git_raw("diff", *RAW_DIFF_FLAGS, "--name-only",\n'
            '                         "--no-renames", "-z", merge_base, branch)',
         'rc, names = _git("diff", *RAW_DIFF_FLAGS, "--name-only",\n'
         '                         "--no-renames", "-z", merge_base, branch)'),
        (C, 'paths = [n for n in names.split(b"\\0") if n]',
         'paths = [n for n in names.split("\\0") if n]')],
    "A4-patch-text": [
        (C, 'rc, patch = _git_raw("show"', 'rc, patch = _git("show"'),
        (C, 'input=patch.rstrip(b"\\n"),', 'input=__import__("os").fsencode(patch),')],
    "A5-T-lookup-text": [
        (R, "import tempfile\n", "import os\nimport tempfile\n"),
        (R, "entries = [_tree_entry(commit, name)",
         "entries = [_tree_entry(commit, os.fsencode(os.fsdecode(name)))")],
    "A6-T-enumeration-text": [
        (R, 'raw = _measure(_git_bytes, "diff", "--no-ext-diff"',
         'raw = __import__("os").fsencode(_measure(git, "diff", "--no-ext-diff"'),
        (R, '"-z", ancestor, branch)', '"-z", ancestor, branch))')],
    "A7-label-decoded": [(G, "return repr(name)[1:]", "return os.fsdecode(name)")],
    "A8-unknown-note-decoded": [
        (R, "unproved.append(path_label(name))",
         "unproved.append(name.decode('utf-8', 'surrogateescape'))")],
    "A9-stranded-note-decoded": [
        (C, "return ([path_label(n) for n in names.split(b\"\\0\") if n][:6], None)",
         "return ([n.decode('utf-8', 'surrogateescape') for n in names.split(b\"\\0\") if n][:6], None)")],
    "A2b-commit-paths-lossy-bytes": [
        (C, "import subprocess\nimport sys\n", "import os\nimport subprocess\nimport sys\n"),
        (C, 'return ([name for name in names.split(b"\\0") if name], None)',
         'return ([os.fsencode(os.fsdecode(name)) for name in names.split(b"\\0") if name], None)')],
    "A3b-path-arm-lossy-bytes": [
        (C, "import subprocess\nimport sys\n", "import os\nimport subprocess\nimport sys\n"),
        (C, 'paths = [n for n in names.split(b"\\0") if n]',
         'paths = [os.fsencode(os.fsdecode(n)) for n in names.split(b"\\0") if n]')],
    "A4b-patch-lossy-bytes": [
        (C, "import subprocess\nimport sys\n", "import os\nimport subprocess\nimport sys\n"),
        (C, 'input=patch.rstrip(b"\\n"),', 'input=os.fsencode(os.fsdecode(patch.rstrip(b"\\n"))),')],
    "A10-prior-lossy-transport-combined": None,
    # R244-B: byte-exact copies in the self-test's own mutation harness
    "B1-harness-text-copies": [
        (M, '(source_dir / "check_merge_containment.py").read_bytes()',
         '(source_dir / "check_merge_containment.py").read_text().encode("utf-8", "surrogateescape")')],
    # R244-C: named guards
    "C1-T-renames-folded": [
        (R, '"--ignore-submodules=none", "--name-only", "--no-renames",',
         '"--ignore-submodules=none", "--name-only",')],
    "C2-T-submodules-ignorable": [
        (R, '"--ignore-submodules=none", "--name-only", "--no-renames",',
         '"--name-only", "--no-renames",')],
    "C3-single-merge-base": [(R, "if len(bases) != 1:", "if not bases:")],
    "C4-ancestor-type-rule": [(R, "for entry in (original, tip, branch)):",
                               "for entry in (tip, branch)):")],
    "C5-replay-distinctness": [(C, "candidates.remove(match)", "pass")],
    # Other guards in the new arm
    "S01-tree-entry-name-check": [(R, "if (terminator or name != path", "if (terminator")],
    "S02-full-tree": [(R, '"--full-tree", commit, "--", path)', 'commit, "--", path)')],
    "S03-conflict-style-override": [(R, '"-c", "merge.conflictStyle=merge", "merge-file"',
                                     '"merge-file"')],
    "S04-ls-tree-literal-pathspecs": [(R, '_measure(_git_bytes, "--literal-pathspecs", "ls-tree"',
                                       '_measure(_git_bytes, "ls-tree"')],
    "S05-T-ext-diff-textconv": [(R, '"diff", "--no-ext-diff", "--no-textconv",\n                   "--ignore',
                                 '"diff",\n                   "--ignore')],
    "S06-oid-length": [(R, "or len(oid) not in (40, 64)", "or False")],
    "S07-oid-hex": [(R, 'or any(char not in "0123456789abcdef" for char in oid)):', "or False):")],
    "S08-single-record": [(R, "if (terminator or name", "if (False or name")],
    "S09-nul-terminated-set": [(R, 'if not raw or not raw.endswith(b"\\0"):', "if not raw:")],
    "S10-empty-set-accepted": [(R, 'if not raw or not raw.endswith(b"\\0"):',
                                'if raw and not raw.endswith(b"\\0"):')],
    "S11-merge-rc-range": [(R, "if rc < 0 or rc > 127:", "if rc < 0:")],
    "S12-identity-shortcut": [(R, "    if tip == branch:\n        return True\n", "")],
    "S13-absence-refusal": [(R, "    if tip is None or branch is None:\n        return False\n", "")],
    "S14-regular-mode-set": [(R, "entry[0] in REGULAR_MODES", "True")],
    "S15-blob-kind": [(R, 'and entry[1] == "blob")', ")")],
    "S16-per-path-error-attribution": [
        (R, "        except (_MeasurementError, OSError) as exc:\n            unproved.append",
         "        except ZeroDivisionError as exc:\n            unproved.append")],
    "S17-patch-trailing-newline": [(C, 'input=patch.rstrip(b"\\n"),', "input=patch,")],
    "S18-arm-order-before-path": [
        (C, "    if have_merge_base:\n        verdict = _path_scoped_verdict(branch, base, mb, ahead)\n",
         "    verdict = replay_verdict(branch, base, ahead, _git, _linear_patches_contained)\n"
         "    if verdict is not None:\n        return verdict\n"
         "    if have_merge_base:\n        verdict = _path_scoped_verdict(branch, base, mb, ahead)\n")],
    "S19-replay-historical-error": [(R, "if historical is None:\n            raise _MeasurementError(error)",
                                     "if historical is None:\n            return None")],
}


MUTANTS["A10-prior-lossy-transport-combined"] = [
    *MUTANTS["A1-lossy-output-guard-dropped"], *MUTANTS["A2-commit-paths-text"],
    *MUTANTS["A3-path-arm-text"], *MUTANTS["A4-patch-text"], *MUTANTS["A5-T-lookup-text"]]


def apply(src: Path, dst: Path, edits):
    shutil.copytree(src, dst)
    for fname, before, after in edits:
        path = dst / fname
        data = path.read_bytes()
        b, a = before.encode(), after.encode()
        if data.count(b) != 1:
            return f"{fname}: 'before' occurs {data.count(b)} times"
        path.write_bytes(data.replace(b, a))
    return None


def env_for(profile, scratch):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if profile == "nolocale":
        bindir = scratch / "bin-nolocale"
        if not bindir.exists():
            bindir.mkdir()
            for entry in Path("/usr/bin").iterdir():
                if entry.name not in ("locale", "localedef"):
                    (bindir / entry.name).symlink_to(entry)
        env["PATH"] = str(bindir)
    elif profile == "ascii":
        for key in ("LANG", "LANGUAGE", "PYTHONIOENCODING"):
            env.pop(key, None)
        env.update(LC_ALL="C", PYTHONUTF8="0", PYTHONCOERCECLOCALE="0")
    return env


def run(name, edits, src, scratch, profile):
    dst = scratch / "mut" / f"{profile}-{name}" / "scripts"
    if dst.parent.exists():
        shutil.rmtree(dst.parent)
    dst.parent.mkdir(parents=True)
    err = apply(src, dst, edits)
    if err:
        return {"mutant": name, "profile": profile, "applied": False, "error": err}
    r = subprocess.run((sys.executable, str(dst / C), "--selftest"),
                       cwd=scratch / "cwd-repo", env=env_for(profile, scratch),
                       capture_output=True)
    out = r.stdout.decode("ascii", "backslashreplace")
    errtxt = r.stderr.decode("ascii", "backslashreplace")
    fails = re.findall(r"^  FAIL (\S+)", out, re.M)
    return {"mutant": name, "profile": profile, "applied": True, "rc": r.returncode,
            "killed": r.returncode != 0, "fail_count": len(fails), "fails": fails[:40],
            "ok_count": len(re.findall(r"^  ok  ", out, re.M)),
            "not_run": re.findall(r"NOT RUN (\S+)", out),
            "harness_collision": "guard no longer has one source location" in out + errtxt,
            "traceback_tail": (errtxt.strip().splitlines() or [""])[-1][-200:]
            if "Traceback" in errtxt else ""}


def main():
    src, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out, profile = sys.argv[3], sys.argv[4]
    names = sys.argv[5:] or list(MUTANTS)
    env_for(profile, scratch)  # prepare the PATH directory once, before threads
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda n: run(n, MUTANTS[n], src, scratch, profile), names))
    with open(out, "a") as handle:
        for result in results:
            handle.write(json.dumps(result) + "\n")
            print(json.dumps({k: result.get(k) for k in
                              ("mutant", "profile", "applied", "rc", "fail_count",
                               "harness_collision", "not_run")}), flush=True)


if __name__ == "__main__":
    main()
