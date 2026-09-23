#!/usr/bin/env python3
"""Reviewer-owned full-check record-fault probes for issue 439.

Usage: python3 probe_record_faults.py <head-clone> <work-dir> [jobs]

For each of the 38 scoped run steps, a copy of the checker gets a data patch
(injected before the CLI entry point) that damages ONLY that step's record:
removed, empty tuple, a list instead of a tuple, or stale (line 1 replaced).
Workflows stay pristine. The FULL `--check` must exit 1 and name the job,
the step and either the missing-record reason or the stale first line.
"""
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import probe_workflow_mutations as pw  # noqa: E402

MARK = 'if __name__ == "__main__":'
FAULTS = {
    "missing": "_e.pop('run')",
    "empty": "_e['run'] = ()",
    "list-typed": "_e['run'] = list(_e['run'])",
    "stale": "_e['run'] = ('echo stale record', *_e['run'][1:])",
}


def run_one(args):
    idx, tmpl, work, rel, jid, at, name, fault = args
    pdir = work / "rec" / f"r{idx:03d}"
    if pdir.exists():
        shutil.rmtree(pdir)
    shutil.copytree(tmpl, pdir)
    src = (pdir / "scripts/ci_events.py").read_text()
    patch = (f"_e = RTL_SEQUENCE_PINS[({rel!r}, {jid!r})][{at}]\n"
             f"assert _e.get('name') == {name!r}\n{FAULTS[fault]}\n\n")
    (pdir / "scripts/ci_events.py").write_text(src.replace(MARK, patch + MARK))
    proc = subprocess.run(
        [sys.executable, "-B", str(pdir / "scripts/ci_events.py"), "--check",
         "--root", str(pdir)], capture_output=True, text=True)
    fails = [l[7:] for l in (proc.stdout + proc.stderr).splitlines()
             if l.startswith("  FAIL ")]
    what = f"job `{jid}` step {at + 1} (`{name}`)"
    want = (f"{what} script is not the canonical form: line 1 must be "
            "'echo stale record'" if fault == "stale" else
            f"{what} must record a canonical normalized `run` script")
    ok = proc.returncode == 1 and any(want in f for f in fails)
    shutil.rmtree(pdir)
    return (idx, "PASS" if ok else "UNEXPECTED", proc.returncode, jid, at + 1,
            fault, len(fails), (fails[0] if fails else "")[:200])


def main():
    head, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    tmpl, digest = pw.build(head, work)
    print(f"# checker sha256 {digest}")
    args, i = [], 0
    for rel in pw.SEVEN:
        text = (tmpl / rel).read_text()
        for jid, at, name, _, _ in pw.scoped_steps(text, rel):
            for fault in FAULTS:
                args.append((i, tmpl, work, rel, jid, at, name, fault))
                i += 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(jobs, 8)) as ex:
        results = sorted(ex.map(run_one, args))
    for r in results:
        print("\t".join(str(x) for x in r))
    bad = sum(r[1] != "PASS" for r in results)
    print(f"# probes={len(results)} unexpected={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
