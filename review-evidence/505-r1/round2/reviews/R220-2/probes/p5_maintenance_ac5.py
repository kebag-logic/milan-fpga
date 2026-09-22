"""P5: maintenance, whitespace and native AC5 analogue through the ACTUAL CLI.

Each scenario is a disposable scratch root filled by `git archive` from the
review clone (workflows, policy page, scripts/ci_events.py), then edited
textually. The scratch copy of ci_events.py is run as the CLI with --root.

Scenarios at HEAD:
  S0 pristine                         --check OK, --selftest PASS
  S1 workflow-only edit (idiom step)  --check refuses job/step/line; --selftest fails
  S2 S1 + matching record update      --check OK; --selftest PASS, arm count grows
  S3 record-only edit                 --check refuses (record != live)
  S4 whitespace-only reformat          --check OK (idiom and ratchet steps)
  S5 elaborate body edit + record     --check OK; --selftest PASS
  S6 AC5 tamper `|| true` on line 1   --check refuses step 34 line 1 (HEAD, R1);
                                       accepted at BASE
"""
from __future__ import annotations

import io
import json
import pathlib
import subprocess
import sys
import tarfile
import tempfile

from common import BASE, CLONE, HEAD, R1

IDIOM = ("          python3 scripts/check_py_idiom.py\n"
         "          python3 scripts/check_py_idiom.py --selftest\n")
IDIOM_REC = ("        {\"name\": \"Python idiom gate\",\n"
             "         \"run\": (\n"
             "             'python3 scripts/check_py_idiom.py',\n"
             "             'python3 scripts/check_py_idiom.py --selftest',\n"
             "         )},\n")
RATCHET = ("          python3 scripts/measure_naming.py --check\n"
           "          python3 scripts/measure_naming.py --selftest\n")
APPLY = "        run: sw/litex/patches/apply.sh\n"
APPLY_REC = ("         \"run\": (\n"
             "             'sw/litex/patches/apply.sh',\n"
             "         )},\n")


def scratch(rev: str, td: pathlib.Path, tag: str) -> pathlib.Path:
    root = td / f"{rev[:8]}-{tag}"
    root.mkdir()
    blob = subprocess.run(["git", "-C", str(CLONE), "archive", "--format=tar", rev,
                           ".github/workflows", "docs/testing/CI_WORKFLOWS.md",
                           "scripts/ci_events.py"], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
        tf.extractall(root, filter="data")
    return root


def edit(path: pathlib.Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, (path, old)
    path.write_text(text.replace(old, new), encoding="utf-8")


def cli(root: pathlib.Path, flag: str) -> dict:
    p = subprocess.run([sys.executable, "-B", str(root / "scripts/ci_events.py"), flag,
                        "--root", str(root)], capture_output=True, text=True, timeout=900)
    out = p.stdout + p.stderr
    fails = [l.strip() for l in out.splitlines() if l.startswith("  FAIL ")]
    tail = [l for l in out.splitlines() if l.startswith(("ci_events:", "selftest:"))]
    return {"rc": p.returncode, "tail": tail, "fail_count": len(fails),
            "fails": [f[:400] for f in fails[:4]]}


def main() -> int:
    res = {}
    with tempfile.TemporaryDirectory(prefix="r220-2-p5-") as td:
        tdp = pathlib.Path(td)
        # S0
        r = scratch(HEAD, tdp, "s0")
        res["S0 pristine HEAD"] = {"check": cli(r, "--check"), "selftest": cli(r, "--selftest")}
        # S1 workflow-only edit
        r = scratch(HEAD, tdp, "s1")
        edit(r / ".github/workflows/docs.yml", IDIOM,
             IDIOM + "          python3 scripts/check_py_idiom.py --list-rules\n")
        res["S1 workflow-only edit"] = {"check": cli(r, "--check"), "selftest": cli(r, "--selftest")}
        # S2 edit + matching record update
        r = scratch(HEAD, tdp, "s2")
        edit(r / ".github/workflows/docs.yml", IDIOM,
             IDIOM + "          python3 scripts/check_py_idiom.py --list-rules\n")
        edit(r / "scripts/ci_events.py", IDIOM_REC, IDIOM_REC.replace(
            "             'python3 scripts/check_py_idiom.py --selftest',\n",
            "             'python3 scripts/check_py_idiom.py --selftest',\n"
            "             'python3 scripts/check_py_idiom.py --list-rules',\n"))
        res["S2 workflow edit + record update"] = {"check": cli(r, "--check"),
                                                   "selftest": cli(r, "--selftest")}
        # S3 record-only edit
        r = scratch(HEAD, tdp, "s3")
        edit(r / "scripts/ci_events.py", IDIOM_REC, IDIOM_REC.replace(
            "'python3 scripts/check_py_idiom.py',", "'python3 scripts/check_py_idiom.py --strict',"))
        res["S3 record-only edit"] = {"check": cli(r, "--check")}
        # S4 whitespace-only reformat of two bodies
        r = scratch(HEAD, tdp, "s4")
        edit(r / ".github/workflows/docs.yml", IDIOM,
             "          python3   scripts/check_py_idiom.py\t\n\n"
             "          python3 \\\n            scripts/check_py_idiom.py    --selftest\n")
        edit(r / ".github/workflows/docs.yml", RATCHET,
             "          python3 scripts/measure_naming.py \\\n            --check\n\n"
             "          python3\tscripts/measure_naming.py --selftest   \n")
        res["S4 whitespace-only reformat"] = {"check": cli(r, "--check")}
        # S5 elaborate body edit + record
        r = scratch(HEAD, tdp, "s5")
        edit(r / ".github/workflows/elaborate.yml", APPLY,
             "        run: sw/litex/patches/apply.sh --verify\n")
        text = (r / "scripts/ci_events.py").read_text(encoding="utf-8")
        anchor = "        {\"name\": \"Apply the toolchain patch series\", \"if\": BUILDER_IF,\n" + APPLY_REC
        assert text.count(anchor) == 1
        (r / "scripts/ci_events.py").write_text(text.replace(anchor, anchor.replace(
            "'sw/litex/patches/apply.sh',", "'sw/litex/patches/apply.sh --verify',")), encoding="utf-8")
        res["S5 elaborate edit + record"] = {"check": cli(r, "--check"),
                                             "selftest": cli(r, "--selftest")}
        # S6 AC5 native analogue at three revisions (the scratch #506 edit)
        for rev in (BASE, R1, HEAD):
            r = scratch(rev, tdp, "s6")
            edit(r / ".github/workflows/docs.yml",
                 "          python3 scripts/check_py_idiom.py\n",
                 "          python3 scripts/check_py_idiom.py || true\n")
            res[f"S6 AC5 tamper at {rev[:8]}"] = {"check": cli(r, "--check")}
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    for k, v in res.items():
        print(k)
        for mode, r in v.items():
            print(f"   {mode}: rc={r['rc']} {r['tail']} fails={r['fail_count']}")
            for f in r["fails"][:2]:
                print(f"      {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
