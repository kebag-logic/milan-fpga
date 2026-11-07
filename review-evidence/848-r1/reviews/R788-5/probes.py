#!/usr/bin/env python3
"""Disposable probes of scripts/docs_inventory.py at one exact head.

Usage: probes.py REPO SHA WORKDIR
Every probe runs on its own copy under WORKDIR; REPO is only read.
"""
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO, SHA, WORK = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
SCRIPT = "scripts/docs_inventory.py"
DATA = "scripts/docs_inventory.json"
AUDIT = "docs/DOCUMENTATION_AUDIT.md"


def run(cwd, *cmd):
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return done.returncode, (done.stdout + done.stderr).strip()


def clone(name):
    target = WORK / name
    if target.exists():
        shutil.rmtree(target)
    run(WORK, "git", "clone", "-q", "--no-hardlinks", "--no-checkout", str(REPO), str(target))
    run(target, "git", "checkout", "-q", "--detach", SHA)
    return target


def export(name):
    target = WORK / name
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", str(REPO), "archive", SHA], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(target)], input=tar, check=True)
    return target


def inv(root, *argv):
    return run(root, sys.executable, "-I", SCRIPT, *argv)


def tail(text, count=2):
    return " / ".join(text.splitlines()[-count:])[:300]


def d0_rows(root):
    rows = [line for line in (root / AUDIT).read_text(encoding="utf-8").splitlines() if line.startswith("| [")]
    return sum(1 for row in rows if re.split(r"(?<!\\)\|", row)[7].strip() == "D0")


def edit(root, path, old, new):
    target = root / path
    text = target.read_text(encoding="utf-8")
    assert old in text, old
    target.write_text(text.replace(old, new), encoding="utf-8")


OLD_RULE = ('RELEASE_FACING = re.compile(r"README\\.md|REQUIREMENTS\\.md|docs/README\\.md|'
            'docs/(guides|integration|reference)/.*")\n')
BRANCH = 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked else "area lane"'


def p_baseline():
    root = clone("base")
    check, out = inv(root, "--check")
    selftest, sout = inv(root, "--selftest")
    print(f"head clone: --check rc {check} [{tail(out, 1)}]; --selftest rc {selftest} [{tail(sout, 1)}]; "
          f"D0 rows {d0_rows(root)}")
    print("module lines", len((root / SCRIPT).read_text(encoding="utf-8").splitlines()))


def p_nogit():
    root = export("nogit")
    code, out = inv(root, "--check")
    print(f"no .git export: exists {(root / '.git').exists()}; --check rc {code} [{tail(out, 1)}]")
    work = WORK / "shallow"
    if work.exists():
        shutil.rmtree(work)
    run(WORK, "git", "clone", "-q", "--depth", "1", "--no-checkout", f"file://{REPO}", str(work))
    run(work, "git", "fetch", "-q", "--depth", "1", "origin", SHA)
    run(work, "git", "checkout", "-q", "--detach", SHA)
    has, _ = run(work, "git", "cat-file", "-e", "1e80128f0a467b58bf884b7d9bf62e013a2fb141^{commit}")
    commits = run(work, "git", "rev-list", "--count", "HEAD")[1]
    code, out = inv(work, "--check")
    print(f"one-commit clone: commits {commits}; baseline object rc {has}; --check rc {code} [{tail(out, 1)}]")


def p_old_rule():
    root = clone("oldrule")
    edit(root, SCRIPT, "#: The area lane that owns each page", OLD_RULE + "#: The area lane that owns each page")
    edit(root, SCRIPT, BRANCH, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else '
         '"D0" if RELEASE_FACING.fullmatch(path) else "area lane"')
    code, out = inv(root, "--selftest")
    print(f"old path rule restored: --selftest rc {code}\n  {out[:700]}")
    code, out = inv(root, "--check")
    print(f"old path rule restored: --check on the real tree rc {code} [{tail(out, 1)}]")


def p_union_rule():
    root = clone("union")
    edit(root, SCRIPT, "#: The area lane that owns each page", OLD_RULE + "#: The area lane that owns each page")
    edit(root, SCRIPT, BRANCH, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else '
         '"D0" if path in checked or RELEASE_FACING.fullmatch(path) else "area lane"')
    code, out = inv(root, "--selftest")
    print(f"list OR path rule: --selftest rc {code}\n  {out[:400]}")


def p_added_pages():
    for area in ("guides", "integration", "reference"):
        root = clone(f"add_{area}")
        (root / f"docs/{area}/PROBE_NEW.md").write_text("# Probe\n", encoding="utf-8")
        run(root, "git", "add", "-A")
        first, _ = inv(root, "--check")
        wrote, _ = inv(root, "--write")
        second, _ = inv(root, "--check")
        row = [line for line in (root / AUDIT).read_text(encoding="utf-8").splitlines() if "PROBE_NEW" in line]
        cell = re.split(r"(?<!\\)\|", row[0])[7].strip()
        print(f"added docs/{area}/PROBE_NEW.md: --check rc {first}; --write rc {wrote}; --check rc {second}; "
              f"Verified `{cell}`; D0 rows {d0_rows(root)}")


def p_refusal():
    listed = "docs/reference/TRACE_EVENTS.md"
    root = clone("rename")
    run(root, "git", "mv", listed, "docs/reference/TRACE_EVENTS_NEW.md")
    check, out = inv(root, "--check")
    write, wout = inv(root, "--write")
    print(f"listed page renamed: --check rc {check}; --write rc {write}\n  {out[:300]}")
    edit(root, DATA, f'"{listed}"', '"docs/reference/TRACE_EVENTS_NEW.md"')
    after = inv(root, "--write")
    print(f"  after the list entry alone is updated: --write rc {after[0]} [{tail(after[1], 1)}]")

    root = clone("remove")
    run(root, "git", "rm", "-q", "docs/guides/gptp/MANAGER.md")
    check, out = inv(root, "--check")
    print(f"listed page removed: --check rc {check} [{tail(out, 1)}]")
    edit(root, DATA, '  "docs/guides/gptp/MANAGER.md",\n', "")
    after = inv(root, "--write")
    again = inv(root, "--check")
    print(f"  entry removed: --write rc {after[0]}; --check rc {again[0]} [{tail(again[1], 1)}]; D0 rows {d0_rows(root)}")

    root = export("remove_nogit")
    (root / listed).unlink()
    check, out = inv(root, "--check")
    print(f"listed page removed, no Git: --check rc {check} [{tail(out, 1)}]")

    root = clone("rename_unlisted")
    run(root, "git", "mv", "docs/reference/STRICTER_READINGS.md", "docs/reference/STRICTER_NEW.md")
    check, out = inv(root, "--check")
    print(f"unlisted page renamed: --check rc {check} [{tail(out, 1)}]")

    root = clone("untracked_entry")
    run(root, "git", "rm", "-q", "--cached", listed)
    check, out = inv(root, "--check")
    print(f"listed page untracked but on disk: --check rc {check} [{tail(out, 1)}]")


def p_data_shapes():
    cases = {
        "key absent": ('"verified_pages": [', '"unused_pages": ['),
        "null": None,
    }
    root = clone("key_absent")
    edit(root, DATA, *cases["key absent"])
    check, _ = inv(root, "--check")
    write, _ = inv(root, "--write")
    print(f"`verified_pages` key absent: --check rc {check}; --write rc {write}; D0 rows {d0_rows(root)}")

    root = clone("archive_listed")
    edit(root, DATA, '"verified_pages": [\n', '"verified_pages": [\n  "docs/history/v1/README.md",\n')
    check, out = inv(root, "--check")
    print(f"archive page listed: --check rc {check} [{tail(out, 1)}]")


def mutant(name, *edits, script_check=False):
    root = clone("m_" + re.sub(r"\W+", "_", name))
    for old, new in edits:
        edit(root, SCRIPT, old, new)
    code, out = inv(root, "--selftest")
    print(f"mutant {name}: --selftest rc {code} [{out.splitlines()[0][:170] if out else ''}]")
    return root


def p_mutants():
    known = 'all(isinstance(page, str) and page in known for page in checked)'
    mutant("identity")
    mutant("no membership check", (known, "all(isinstance(page, str) for page in checked)"))
    mutant("any for all", (known, 'any(isinstance(page, str) and page in known for page in checked)'))
    mutant("no list check", ('not isinstance(checked, list) or not all(', 'not all('))
    mutant("no str check", (known, "all(page in known for page in checked)"))
    mutant("archive test lost", (BRANCH, 'verified = "D0" if path in checked else "area lane"'))
    mutant("every page D0", (BRANCH, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0"'))
    mutant("no page D0", (BRANCH, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "area lane"'))
    swap = 'verified = "D0" if path in checked else "archive" if path.startswith(ARCHIVE_PREFIX) else "area lane"'
    mutant("D0 before archive", (BRANCH, swap))
    arm = ('("archive page is obsolete with its successor", lambda root: None, 0,',
           '("archive page is obsolete with its successor", '
           'edit_data(lambda d: d["verified_pages"].append("docs/history/v1/OLD.md")), 0,')
    root = mutant("control only: archive arm lists the archive page", arm)
    print(f"  module lines with that control {len((root / SCRIPT).read_text(encoding='utf-8').splitlines())}")
    mutant("D0 before archive, with that control", (BRANCH, swap), arm)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    for probe in (p_baseline, p_nogit, p_old_rule, p_union_rule, p_added_pages, p_refusal, p_data_shapes, p_mutants):
        print(f"--- {probe.__name__}", flush=True)
        probe()
        sys.stdout.flush()


if __name__ == "__main__":
    main()
