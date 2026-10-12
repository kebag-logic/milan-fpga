#!/usr/bin/env python3
"""Planted layout defects against the head's own `ci_events.py --check`.

Each probe copies the head's workflow directory and policy page into a fresh
temporary root (from git objects at HEAD_SHA), applies one textual edit, and runs
the head's ci_events.py --check --root on it. A probe passes when --check exits
non-zero (the defect is caught). The control (no edit) must exit 0.
Usage: layout_pin_probes.py CLONE HEAD_SHA SCRATCH OUT_JSON
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

clone, sha, scratch, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
WF = ".github/workflows/rtl-fast.yml"
POL = "docs/testing/CI_WORKFLOWS.md"


def srp_job(text: str) -> tuple[int, int]:
    start = text.index("\n  firmware-srp-mutants:\n")
    end = text.index("\n  # This stable aggregate", start)
    return start, end


def drop_srp_job(t: str) -> str:
    s, e = srp_job(t)
    t = t[:s] + t[e:]
    t = t.replace(", firmware-srp-mutants]", "]")
    t = t.replace('          FIRMWARE_SRP_MUTANTS_RESULT: ${{ needs.firmware-srp-mutants.result }}\n', "")
    return t.replace('"firmware-aecp-mutants:$FIRMWARE_AECP_MUTANTS_RESULT" \\\n            '
                     '"firmware-srp-mutants:$FIRMWARE_SRP_MUTANTS_RESULT"; do',
                     '"firmware-aecp-mutants:$FIRMWARE_AECP_MUTANTS_RESULT"; do')


def in_srp(t: str, old: str, new: str) -> str:
    s, e = srp_job(t)
    seg = t[s:e]
    assert old in seg, old
    return t[:s] + seg.replace(old, new, 1) + t[e:]


PROBES = {
    "control-no-edit": (WF, lambda t: t),
    "aggregate-needs-drops-srp-mutants": (WF, lambda t: t.replace(", firmware-srp-mutants]", "]")),
    "aggregate-loop-drops-srp-mutants": (WF, lambda t: t.replace(
        ' \\\n            "firmware-srp-mutants:$FIRMWARE_SRP_MUTANTS_RESULT"; do', '; do')),
    "aggregate-needs-drops-publication-census": (WF, lambda t: t.replace(
        "yosys-elaboration, publication-census, firmware-unit", "yosys-elaboration, firmware-unit")),
    "srp-job-deleted-entirely": (WF, drop_srp_job),
    "srp-job-runs-shard-2": (WF, lambda t: in_srp(t, "--shard 3/4", "--shard 2/4")),
    "unit-job-runs-unsharded-default": (WF, lambda t: t.replace(
        "--jobs 4 --shard 0/4", "--jobs 4", 1)),
    "srp-job-condition-false": (WF, lambda t: in_srp(
        t, "if: ${{ needs.changes.outputs.rtl == 'true' }}", "if: ${{ false }}")),
    "srp-job-drops-needs-changes": (WF, lambda t: in_srp(t, "    needs: changes\n", "")),
    "srp-job-timeout-60": (WF, lambda t: in_srp(t, "timeout-minutes: 45", "timeout-minutes: 60")),
    "srp-job-caches-build-output": (WF, lambda t: in_srp(
        t, "path: ~/br-milan-rv32/host", "path: |\n            ~/br-milan-rv32/host\n            /tmp/ctrl-fw-build")),
    "srp-job-drops-sdk-verify": (WF, lambda t: in_srp(t, "python3 scripts/ci_rv32_sdk_selftest.py\n          ", "")),
    "srp-job-drops-require-rv32": (WF, lambda t: in_srp(t, "--require-rv32 --self-test --jobs 4 --shard 3/4",
                                                        "--self-test --jobs 4 --shard 3/4")),
    "srp-job-drops-lwsrp-fetch": (WF, lambda t: in_srp(
        t, "gptp-processor third_party/lwSRP", "gptp-processor")),
    "policy-row-aecp-budget-changed": (POL, lambda t: t.replace(
        "| `firmware-aecp-mutants` | 45 min | 1890 s | 1620 s |", "| `firmware-aecp-mutants` | 45 min | 2400 s | 1620 s |")),
}


def main() -> int:
    results = {}
    for name, (rel, edit) in PROBES.items():
        root = scratch / ("pin-" + name)
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        tar = subprocess.run(["git", "-C", str(clone), "archive", sha], check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(root)], input=tar, check=True)
        path = root / rel
        before = path.read_text()
        after = edit(before)
        if name != "control-no-edit" and after == before:
            results[name] = {"applied": False}
            continue
        path.write_text(after)
        res = subprocess.run([sys.executable, str(clone / "scripts/ci_events.py"), "--check", "--root", str(root)],
                             capture_output=True, text=True)
        lines = [l for l in res.stdout.splitlines() if re.search(r"FAIL|finding|differs|must|missing|refuse", l)]
        results[name] = {"applied": True, "rc": res.returncode, "first_findings": lines[:4],
                         "caught": res.returncode != 0}
        shutil.rmtree(root)
    ok = results["control-no-edit"]["rc"] == 0 and all(
        v.get("caught") for k, v in results.items() if k != "control-no-edit")
    out.write_text(json.dumps({"ok": ok, "probes": results}, indent=1) + "\n")
    for k, v in results.items():
        print(k, {x: v[x] for x in ("applied", "rc", "caught") if x in v}, (v.get("first_findings") or [""])[0][:200])
    print("ALL CAUGHT" if ok else "NOT ALL CAUGHT")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
