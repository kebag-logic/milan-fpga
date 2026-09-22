"""P3: comparator mutants run through the ACTUAL CLI, before and after.

For each revision (round-1 head 6af65a15 and HEAD ad624931), a disposable
scratch root receives that revision's four workflow files, its policy page
and its scripts/ci_events.py (via `git archive`, so the review clone is only
read). Each mutant is a source-text edit of `check_carrier_script` (the #407
comparison) or its call site. Each variant is run as
`python3 -B <scratch>/scripts/ci_events.py --check|--selftest --root <scratch>`
and the exit codes, the self-test tail and the names of every arm the
self-test reports as not caught are recorded.

A mutant models a named defect: a weakened comparison that --check cannot
see on the pristine tree. The new arms claim that --selftest fails for it.
"""
from __future__ import annotations

import io
import json
import pathlib
import re
import subprocess
import sys
import tarfile
import tempfile

from common import CLONE, HEAD, R1

CMP_ANCHOR = ("    c.item(tuple(lines) == canonical, path,\n"
              '           f"{what} script is not the canonical form: "\n')
REC_ANCHOR = "    c.item(recorded, path,\n"
CALL_ANCHOR = '        if path in (DOCS, ELABORATE) and "uses" not in entry:\n'
DEF_ANCHOR = "def check_carrier_script("

HELPERS = r'''
def _r220_strip_or_true(seq, which):
    """Strip one trailing ` || true` from the selected line indexes."""
    out = []
    for i, l in enumerate(seq):
        if which(i, len(seq), l) and l.endswith(" || true"):
            l = l[: -len(" || true")]
        out.append(l)
    return out


def _r220_cmp(lines, canonical):
    mode = _R220_MODE
    lines, canonical = list(lines), list(canonical)
    if mode == "M5b-nonlast-or-true":
        nonlast = lambda i, n, l: i < n - 1
        return _r220_strip_or_true(lines, nonlast) == _r220_strip_or_true(canonical, nonlast)
    if mode == "M5a-any-or-true":
        anyl = lambda i, n, l: True
        return _r220_strip_or_true(lines, anyl) == _r220_strip_or_true(canonical, anyl)
    if mode == "M5c-last-or-true":
        last = lambda i, n, l: i == n - 1
        return _r220_strip_or_true(lines, last) == _r220_strip_or_true(canonical, last)
    if mode == "M-check-lines-or-true":
        chk = lambda i, n, l: " --check" in l
        return _r220_strip_or_true(lines, chk) == _r220_strip_or_true(canonical, chk)
    if mode == "M-ac5-idiom-only":
        idi = lambda i, n, l: l.startswith("python3 scripts/check_py_idiom.py")
        return _r220_strip_or_true(lines, idi) == _r220_strip_or_true(canonical, idi)
    if mode == "M4-prefix-only":
        return lines[: len(canonical)] == canonical
    if mode == "M1-order-insensitive":
        return sorted(lines) == sorted(canonical)
    if mode == "M-truncation-accepted":
        return bool(lines) and lines == canonical[: len(lines)]
    if mode == "M-first-line-only":
        return lines[:1] == canonical[:1]
    if mode == "M-length-only":
        return len(lines) == len(canonical)
    if mode == "M-flags-ignored":
        f = lambda s: [re.sub(r" --(?:self-test|selftest|check)(?= |$)", "", l) for l in s]
        return f(lines) == f(canonical)
    if mode == "M-noop-accepted":
        return lines == canonical or lines == ["true"]
    if mode == "M-comparison-removed":
        return True
    raise AssertionError(mode)


'''

CMP_MODES = ("M5b-nonlast-or-true", "M5a-any-or-true", "M5c-last-or-true",
             "M-check-lines-or-true", "M-ac5-idiom-only", "M4-prefix-only",
             "M1-order-insensitive", "M-truncation-accepted",
             "M-first-line-only", "M-length-only", "M-flags-ignored",
             "M-noop-accepted", "M-comparison-removed")


def variant(source: str, mode: str) -> str:
    assert source.count(CMP_ANCHOR) == 1 and source.count(DEF_ANCHOR) == 1
    if mode == "pristine":
        return source
    if mode == "M-record-enforcement-removed":
        assert source.count(REC_ANCHOR) == 1
        return source.replace(REC_ANCHOR, "    c.item(True, path,\n")
    if mode == "M-elaborate-skipped":
        assert source.count(CALL_ANCHOR) == 1
        return source.replace(CALL_ANCHOR, CALL_ANCHOR.replace("(DOCS, ELABORATE)", "(DOCS,)"))
    src = source.replace(CMP_ANCHOR, "    c.item(_r220_cmp(lines, canonical), path,\n"
                                     '           f"{what} script is not the canonical form: "\n')
    return src.replace(DEF_ANCHOR, f"_R220_MODE = {mode!r}\n" + HELPERS + DEF_ANCHOR)


def scratch_root(rev: str, td: pathlib.Path) -> pathlib.Path:
    root = td / rev[:8]
    root.mkdir()
    blob = subprocess.run(["git", "-C", str(CLONE), "archive", "--format=tar", rev,
                           ".github/workflows", "docs/testing/CI_WORKFLOWS.md",
                           "scripts/ci_events.py"], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
        tf.extractall(root, filter="data")
    return root


def run(root: pathlib.Path, script: pathlib.Path, flag: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-B", str(script), flag, "--root", str(root)],
                       capture_output=True, text=True, timeout=900)
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    modes = ("pristine",) + CMP_MODES + ("M-record-enforcement-removed",
                                         "M-elaborate-skipped")
    results = {}
    with tempfile.TemporaryDirectory(prefix="r220-2-p3-") as td:
        tdp = pathlib.Path(td)
        for rev in (R1, HEAD):
            root = scratch_root(rev, tdp)
            original = (root / "scripts/ci_events.py").read_text(encoding="utf-8")
            for mode in modes:
                script = root / "scripts" / f"ci_events_{mode}.py"
                script.write_text(variant(original, mode), encoding="utf-8")
                rc_check, out_check = run(root, script, "--check")
                rc_self, out_self = run(root, script, "--selftest")
                missed = re.findall(r"FAIL mutation not caught: \[([^\]]+)\]", out_self)
                other_fail = [l for l in out_self.splitlines()
                              if l.startswith("  FAIL ") and "mutation not caught" not in l]
                tail = [l for l in out_self.splitlines() if l.startswith("selftest:")]
                results[f"{rev[:8]} {mode}"] = {
                    "check_rc": rc_check,
                    "check_tail": out_check.strip().splitlines()[-1:],
                    "selftest_rc": rc_self, "selftest_tail": tail,
                    "arms_not_caught": len(missed),
                    "not_caught_by_lever": dict(sorted(
                        {lev: sum(1 for m in missed if re.sub(r"^carrier-script-407 \S+ step \d+ ", "", m).split("-line-")[0] == lev)
                         for lev in {re.sub(r"^carrier-script-407 \S+ step \d+ ", "", m).split("-line-")[0] for m in missed}}.items())),
                    "ac5_arm_named": any(m == "carrier-script-407 docs-check step 34 or-true-line-1" for m in missed),
                    "other_failures": other_fail[:5],
                    "other_failure_count": len(other_fail),
                    "not_caught_sample": missed[:6],
                }
                # Receipt: complete self-test output per variant.
                out_dir = pathlib.Path(sys.argv[1]).parent / "p3-cli"
                out_dir.mkdir(exist_ok=True)
                (out_dir / f"{rev[:8]}-{mode}-selftest.log").write_text(
                    f"$ python3 -B {script.name} --selftest --root <scratch {rev[:8]}>\n"
                    f"rc={rc_self}\n" + out_self, encoding="utf-8")
                (out_dir / f"{rev[:8]}-{mode}-check.log").write_text(
                    f"$ python3 -B {script.name} --check --root <scratch {rev[:8]}>\n"
                    f"rc={rc_check}\n" + out_check, encoding="utf-8")
                print(f"{rev[:8]} {mode:32s} check_rc={rc_check} selftest_rc={rc_self} "
                      f"not_caught={len(missed):4d} ac5_named={results[f'{rev[:8]} {mode}']['ac5_arm_named']} "
                      f"other={len(other_fail)} {tail}", flush=True)
    json.dump(results, open(sys.argv[1], "w"), indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
