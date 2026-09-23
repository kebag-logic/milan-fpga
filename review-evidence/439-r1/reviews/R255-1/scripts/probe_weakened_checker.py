#!/usr/bin/env python3
"""Reviewer-owned weakened-checker controls for issue 439.

Usage: python3 probe_weakened_checker.py <tmpl-dir> <work-dir>

<tmpl-dir> is the byte-identical template probe_workflow_mutations.py built
(four workflows, the policy page and the checker at the head under review).
Each weakening is one exact source replacement in a COPY of the checker;
the copy runs `--selftest --root <tmpl>`. "DETECTED" means the self-test
exits non-zero. W-derive additionally runs `--check` on a candidate whose
SHA-pin mismatch block is deleted, to characterize the trust boundary.
"""
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

COND = ('        if "uses" not in entry and (\n'
        '                path in (DOCS, ELABORATE) or (path, jid) in RTL_STEP_LISTS\n'
        '                or (path == RTL_FULL and jid == GATE_JOB\n'
        '                    and entry.get("id") == PIN_STEP_ID)):\n')
CMP = ('    lines = normalize_script(step["run"])\n'
       '    c.item(tuple(lines) == canonical, path,\n')
REC = ('    canonical = entry.get("run")\n'
       '    recorded = (isinstance(canonical, tuple) and bool(canonical)\n')
MARK = 'if __name__ == "__main__":'
DERIVE = '''
def _w_derive():
    import yaml as _y
    for (_p, _j), _entries in RTL_SEQUENCE_PINS.items():
        if (_p, _j) not in RTL_STEP_LISTS and _j != GATE_JOB:
            continue  # only the 38 #439 records, never the physical leg's
        _wf = _y.safe_load((ROOT / _p).read_text())
        for _at, _e in enumerate(_entries):
            if "run" in _e and (_j != GATE_JOB or _e.get("id") == PIN_STEP_ID):
                _live = _wf["jobs"][_j]["steps"][_at].get("run")
                if isinstance(_live, str):
                    _e["run"] = tuple(normalize_script(_live))
_w_derive()

'''

WEAKENINGS = [
    ("W1-drop-rtl-job-condition", COND, COND.replace(
        " or (path, jid) in RTL_STEP_LISTS", "")),
    ("W2-drop-sha-step-condition", COND, (
        '        if "uses" not in entry and (\n'
        '                path in (DOCS, ELABORATE) or (path, jid) in RTL_STEP_LISTS):\n')),
    ("W3-exclude-one-rtl-job", COND, COND.replace(
        "(path, jid) in RTL_STEP_LISTS",
        '((path, jid) in RTL_STEP_LISTS and jid != "bdd-conformance")')),
    ("W4-prefix-compare", CMP, CMP.replace(
        "tuple(lines) == canonical", "tuple(lines)[:len(canonical)] == canonical")),
    ("W5-order-insensitive-compare", CMP, CMP.replace(
        "tuple(lines) == canonical", "sorted(lines) == sorted(canonical)")),
    ("W6-ignore-comment-lines", CMP, CMP.replace(
        "tuple(lines) == canonical",
        "tuple(l for l in lines if not l.startswith('#')) == "
        "tuple(l for l in canonical if not l.startswith('#'))")),
    ("W7-missing-record-derived-from-live", REC, REC.replace(
        'canonical = entry.get("run")',
        'canonical = entry.get("run") or tuple(normalize_script(step["run"]))')),
    ("W8-ignore-true-lines", CMP, CMP.replace(
        "tuple(lines) == canonical",
        "tuple(l for l in lines if l != 'true') == "
        "tuple(l for l in canonical if l != 'true')")),
    ("W9-drop-content-compare-for-rtl-full", CMP, CMP.replace(
        "tuple(lines) == canonical", "(path == RTL_FULL or tuple(lines) == canonical)")),
    ("W10-derive-records-from-disk-at-import", MARK, DERIVE + MARK),
]


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def one(args):
    name, old, new, tmpl, work = args
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(tmpl, d)
    src = (d / "scripts/ci_events.py").read_text()
    assert src.count(old) == 1, name
    (d / "scripts/ci_events.py").write_text(src.replace(old, new))
    rc, out = run([sys.executable, "-B", str(d / "scripts/ci_events.py"),
                   "--selftest", "--root", str(d)])
    fails = [l for l in out.splitlines() if l.startswith("  FAIL ")]
    rtl = [l for l in fails if "rtl-script-439" in l]
    last = out.strip().splitlines()[-1] if out.strip() else ""
    extra = ""
    if name.startswith("W10"):
        wf = d / ".github/workflows/rtl.yml"
        t = wf.read_text()
        blk = ('          if [ "$head" != "$GITHUB_SHA" ]; then\n'
               '            echo "checkout HEAD $head is not GITHUB_SHA $GITHUB_SHA" >&2\n'
               '            exit 1\n'
               '          fi\n')
        assert t.count(blk) == 1
        wf.write_text(t.replace(blk, ""))
        crc, cout = run([sys.executable, "-B", str(d / "scripts/ci_events.py"),
                         "--check", "--root", str(d)])
        extra = f"candidate-without-mismatch-block --check exit={crc}: " + \
            cout.strip().splitlines()[-1]
    shutil.rmtree(d)
    return (name, "DETECTED" if rc != 0 else "NOT-DETECTED", rc, len(fails),
            len(rtl), (rtl[0] if rtl else (fails[0] if fails else ""))[:240],
            last[:120], extra)


def main():
    tmpl, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    work.mkdir(parents=True, exist_ok=True)
    args = [(n, o, w, tmpl, work) for n, o, w in WEAKENINGS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(one, args):
            print("\t".join(str(x) for x in r))


if __name__ == "__main__":
    main()
