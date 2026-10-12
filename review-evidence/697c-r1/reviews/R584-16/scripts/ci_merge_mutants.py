#!/usr/bin/env python3
"""ci_merge_mutants.py <clone> <workdir>: undo each round-18 merge choice in a copy.

Each mutant takes `git archive HEAD .github scripts docs` of the clone, plants
one text edit (scoped to one job's block where named) and runs the copy's own
`ci_events.py --check --root <copy>`. M0 (no edit) must give rc 0, every other
mutant rc != 0. Prints one line per mutant and exits 0 when all hold.
"""
import subprocess
import sys
from pathlib import Path

clone, work = Path(sys.argv[1]), Path(sys.argv[2])
WF = ".github/workflows/rtl-fast.yml"
DOC = "docs/testing/CI_WORKFLOWS.md"
TSN = " third_party/tsn-c-stack"


def job_edit(job, old, new):
    def edit(text):
        start = text.index(f"\n  {job}:\n")
        nxt = text.find("\n  ", start + 3)
        while nxt != -1 and text[nxt + 3] == " ":
            nxt = text.find("\n  ", nxt + 3)
        block = text[start:nxt]
        assert old in block, (job, old)
        return text[:start] + block.replace(old, new, 1) + text[nxt:]
    return edit


def plain(old, new):
    def edit(text):
        assert old in text, old
        return text.replace(old, new, 1)
    return edit


MUTANTS = [
    ("M0-pristine", None, None),
    ("M1-control-mutants-fetch-without-tsn", WF, job_edit("firmware-control-mutants", TSN, "")),
    ("M2-aecp-mutants-fetch-without-tsn", WF, job_edit("firmware-aecp-mutants", TSN, "")),
    ("M3-srp-mutants-fetch-without-tsn", WF, job_edit("firmware-srp-mutants", TSN, "")),
    ("M4-unit-fetch-without-tsn", WF, job_edit("firmware-unit", TSN, "")),
    ("M5-boundary-fetch-without-tsn", WF, job_edit("firmware-boundary", TSN, "")),
    ("M6-needs-drop-firmware-boundary", WF, job_edit("rtl-fast", ", firmware-boundary, firmware-verilator]", ", firmware-verilator]")),
    ("M7-needs-drop-firmware-aecp-mutants", WF, job_edit("rtl-fast", " firmware-aecp-mutants,", "")),
    ("M8-loop-drop-firmware-verilator", WF, job_edit(
        "rtl-fast", ' \\\n            "firmware-verilator:$FIRMWARE_VERILATOR_RESULT"; do', "; do")),
    ("M9-loop-drop-firmware-srp-mutants", WF, job_edit(
        "rtl-fast", '            "firmware-srp-mutants:$FIRMWARE_SRP_MUTANTS_RESULT" \\\n', "")),
    ("M10-env-drop-control-mutants", WF, job_edit(
        "rtl-fast", "          FIRMWARE_CONTROL_MUTANTS_RESULT: ${{ needs.firmware-control-mutants.result }}\n", "")),
    ("M11-unit-without-shard", WF, plain("--jobs 4 --shard 0/4", "--jobs 4")),
    ("M12-srp-job-runs-shard-2", WF, plain("--jobs 4 --shard 3/4", "--jobs 4 --shard 2/4")),
    ("M13-boundary-without-require-rv32", WF, plain(
        "ctrl_boundary.py --require-rv32 --selftest --without verilator",
        "ctrl_boundary.py --selftest --without verilator")),
    ("M14-verilator-job-timeout-45", WF, job_edit("firmware-verilator", "timeout-minutes: 40", "timeout-minutes: 45")),
    ("M15-doc-aecp-budget-row-dropped", DOC, plain("| `firmware-aecp-mutants` | 45 min | 1890 s | 1620 s |\n", "")),
    ("M16-doc-skip-list-drops-boundary", DOC, plain(
        "all four firmware jobs, `firmware-boundary` and `firmware-verilator`.",
        "all four firmware jobs and `firmware-verilator`.")),
    ("M17-control-mutants-job-removed", WF, None),
]


def remove_job(text, job):
    start = text.index(f"\n  {job}:\n")
    nxt = text.find("\n  ", start + 3)
    while nxt != -1 and text[nxt + 3] == " ":
        nxt = text.find("\n  ", nxt + 3)
    return text[:start] + text[nxt:]


bad = 0
for name, path, edit in MUTANTS:
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    arc = subprocess.run(["git", "-C", str(clone), "archive", "HEAD", ".github", "scripts", "docs"],
                         check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(d)], input=arc, check=True)
    if name == "M17-control-mutants-job-removed":
        p = d / WF
        p.write_text(remove_job(p.read_text(), "firmware-control-mutants"))
    elif edit is not None:
        p = d / path
        before = p.read_text()
        after = edit(before)
        assert after != before, name
        p.write_text(after)
    r = subprocess.run([sys.executable, "-I", str(d / "scripts/ci_events.py"), "--check", "--root", str(d)],
                       capture_output=True, text=True)
    lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
    first = next((ln for ln in lines if "OK" in ln or "FINDING" in ln.upper() or "finding" in ln), lines[0] if lines else "")
    want_ok = name == "M0-pristine"
    held = (r.returncode == 0) == want_ok
    bad += not held
    print(f"{name:42} rc={r.returncode} {'HELD' if held else 'ESCAPED'} | {first[:200]}")
    if not want_ok:
        detail = [ln for ln in lines if any(k in ln for k in ("tsn", "firmware", "needs", "shard", "budget",
                                                               "require", "timeout", "census", "skip"))]
        for ln in detail[:2]:
            print(f"    {ln[:240]}")
print("RESULT", "PASS" if not bad else f"FAIL ({bad})")
sys.exit(1 if bad else 0)
