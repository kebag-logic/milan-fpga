#!/usr/bin/env python3
"""Reviewer-owned matching-maintenance probes for issue 439.

Usage: python3 probe_maintenance.py <head-clone> <work-dir> [jobs]

For each of the 38 scoped run steps: append `echo maintained` to the
workflow body (YAML text edit) AND to that step's record in a copy of the
checker (a data patch injected before the CLI entry point, replacing only
that entry's `run` tuple), then run the FULL `--check`. The content pin
must not refuse the step; any remaining finding must come from a
separately specialized pin (reported, documented as expected). Output: TSV.
"""
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import probe_workflow_mutations as pw  # noqa: E402

MARK = 'if __name__ == "__main__":'


def run_one(args):
    idx, tmpl, work, rel, jid, at, name, newtext = args
    pdir = work / "maint" / f"m{idx:03d}"
    if pdir.exists():
        shutil.rmtree(pdir)
    for f in pw.FILES + ("scripts/ci_events.py",):
        d = pdir / f
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(tmpl / f, d)
    (pdir / rel).write_text(newtext)
    src = (pdir / "scripts/ci_events.py").read_text()
    assert src.count(MARK) == 1
    patch = (f"_k = ({rel!r}, {jid!r})\n"
             f"_e = RTL_SEQUENCE_PINS[_k][{at}]\n"
             f"assert _e.get('name') == {name!r}\n"
             "_e['run'] = (*_e['run'], 'echo maintained')\n\n")
    (pdir / "scripts/ci_events.py").write_text(src.replace(MARK, patch + MARK))
    proc = subprocess.run(
        [sys.executable, "-B", str(pdir / "scripts/ci_events.py"), "--check",
         "--root", str(pdir)], capture_output=True, text=True)
    fails = [l[7:] for l in (proc.stdout + proc.stderr).splitlines()
             if l.startswith("  FAIL ")]
    what = f"job `{jid}` step {at + 1} (`{name}`) script is not the canonical form"
    content_refusal = any(what in f for f in fails)
    shutil.rmtree(pdir)
    verdict = ("ACCEPTED" if proc.returncode == 0 else
               "CONTENT-PIN-REFUSED" if content_refusal else
               "SPECIALIZED-PIN-ONLY")
    first = fails[0][:220] if fails else ""
    return (idx, verdict, proc.returncode, jid, at + 1, name, len(fails), first)


def main():
    head, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    tmpl, digest = pw.build(head, work)
    print(f"# checker sha256 {digest}")
    args, i = [], 0
    for rel in pw.SEVEN:
        text = (tmpl / rel).read_text()
        for jid, at, name, vnode, knode in pw.scoped_steps(text, rel):
            lines = pw.norm(vnode.value)
            new = pw.replace_run(text, vnode, knode, [*lines, "echo maintained"])
            args.append((i, tmpl, work, rel, jid, at, name, new))
            i += 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(jobs, 8)) as ex:
        results = sorted(ex.map(run_one, args))
    for r in results:
        print("\t".join(str(x) for x in r))
    bad = sum(r[1] == "CONTENT-PIN-REFUSED" for r in results)
    acc = sum(r[1] == "ACCEPTED" for r in results)
    print(f"# steps={len(results)} accepted={acc} "
          f"specialized_only={len(results) - acc - bad} content_pin_refused={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
