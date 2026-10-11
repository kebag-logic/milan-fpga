#!/usr/bin/env python3
"""Disposable fault probes against a COPY of the reviewed tree.

Usage: python3 -I probes.py PROBE_TREE OUT_JSON
Each probe edits one file in PROBE_TREE, runs the check that should catch it,
records the exit code and the matching finding, and restores the file bytes.
Expectation "fail" means the check must exit nonzero; "pass" means it must
stay green (a legitimate change such as a new shape).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
WF = ".github/workflows/rtl-fast.yml"
DRV = "sw/firmware/ctrl/test/test_ctrl_firmware.py"
DOC = "docs/testing/CI_WORKFLOWS.md"
CHECK = ["python3", "-I", "scripts/ci_events.py", "--check", "--root", str(TREE)]
CENSUS = ["python3", "-I", "scripts/ci_events.py", "--firmware-census", "--root", str(TREE)]
SHARDS = ["python3", "-s", "-B", "sw/firmware/ctrl/test/test_ctrl_firmware_shards.py"]


def replace_once(rel, old, new, count=1):
    def edit(text):
        assert text.count(old) >= count, (rel, old, text.count(old))
        return text.replace(old, new, count)
    return rel, edit


def nth(rel, old, new, n):
    """Replace only the n-th (1-based) occurrence."""
    def edit(text):
        parts = text.split(old)
        assert len(parts) > n, (rel, old, len(parts) - 1)
        return old.join(parts[:n]) + new + old.join(parts[n:])
    return rel, edit


def new_file(rel, content):
    return rel, ("create", content)


PROBES = [
    # --- controls: the unmodified probe tree must pass every check ---
    ("control-unmodified-check", "pass", CHECK, ("README.md", lambda s: s + "\n")),
    ("control-unmodified-shards", "pass", SHARDS, ("README.md", lambda s: s + "\n")),
    # --- workflow layout (ci_events --check) ---
    ("wf-control-job-runs-shard0", "fail", CHECK,
     replace_once(WF, "--jobs 4 --shard 1/4", "--jobs 4 --shard 0/4")),
    ("wf-srp-job-runs-shard2-duplicate", "fail", CHECK,
     replace_once(WF, "--jobs 4 --shard 3/4", "--jobs 4 --shard 2/4")),
    ("wf-unit-job-drops-shard-arg", "fail", CHECK,
     replace_once(WF, "--jobs 4 --shard 0/4", "--jobs 4")),
    ("wf-aggregate-needs-drops-srp", "fail", CHECK,
     replace_once(WF, "firmware-aecp-mutants, firmware-srp-mutants]", "firmware-aecp-mutants]")),
    ("wf-aggregate-loop-drops-control", "fail", CHECK,
     replace_once(WF, '            "firmware-control-mutants:$FIRMWARE_CONTROL_MUTANTS_RESULT" \\\n', "")),
    ("wf-aggregate-env-wrong-job", "fail", CHECK,
     replace_once(WF, "${{ needs.firmware-aecp-mutants.result }}", "${{ needs.firmware-unit.result }}")),
    ("wf-aecp-job-if-false", "fail", CHECK,
     nth(WF, "    if: ${{ needs.changes.outputs.rtl == 'true' }}\n", "    if: false\n", 5)),
    ("wf-srp-timeout-60", "fail", CHECK,
     nth(WF, "    timeout-minutes: 45\n    steps:\n      - uses: actions/checkout@v4\n      - name: Fetch RTL dependencies",
         "    timeout-minutes: 60\n    steps:\n      - uses: actions/checkout@v4\n      - name: Fetch RTL dependencies", 4)),
    ("wf-control-adds-build-output-cache", "fail", CHECK,
     replace_once(WF, "      - name: Run the control mutation campaign\n",
                  "      - name: Cache firmware builds\n        uses: actions/cache@v4\n        with:\n"
                  "          path: /tmp/ctrl-fw-build\n          key: fw-build-${{ github.sha }}\n"
                  "      - name: Run the control mutation campaign\n")),
    ("wf-unit-drops-coverage-check", "fail", CHECK,
     replace_once(WF, '          python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$(nproc)"\n', "")),
    ("wf-unit-drops-coverage-check-census", "fail", CENSUS,
     replace_once(WF, '          python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$(nproc)"\n', "")),
    ("wf-control-step-gated-off", "fail", CHECK,
     replace_once(WF, "      - name: Run the control mutation campaign\n",
                  "      - name: Run the control mutation campaign\n        if: ${{ false }}\n")),
    ("wf-control-step-gated-off-census", "fail", CENSUS,
     replace_once(WF, "      - name: Run the control mutation campaign\n",
                  "      - name: Run the control mutation campaign\n        if: ${{ false }}\n")),
    ("wf-continue-on-error-srp", "fail", CHECK,
     replace_once(WF, "      - name: Run both SRP mutation campaigns and pin controls\n",
                  "      - name: Run both SRP mutation campaigns and pin controls\n        continue-on-error: true\n")),
    ("doc-budget-row-raised", "fail", CHECK,
     replace_once(DOC, "| `firmware-srp-mutants` | 45 min | 1890 s | 1620 s |",
                  "| `firmware-srp-mutants` | 45 min | 2400 s | 1620 s |")),
    # --- shard dispatch (test_ctrl_firmware_shards.py, also run by every sharded job) ---
    # Observation-point limits (expected to stay green; recorded as a SUGGESTION, not a defect at head):
    # the inventory records invocations, not whether each result reaches the verdict.
    ("limit-shard-mode-discards-one-suite-outcome", "pass", SHARDS,
     replace_once(DRV, "                ctrl_arms.arm_reentry_debug(tree), ctrl_arms.arm_reentry_release(tree)]\n",
                  "                ctrl_arms.arm_reentry_debug(tree), ctrl_arms.arm_reentry_release(tree)]\n"
                  "    if args.shard is not None:\n        outcomes.pop()\n")),
    ("limit-shard-mode-ignores-aecp-verdict", "pass", SHARDS,
     replace_once(DRV, "                failed = aecp_mutants.campaign(out / \"aecp-mutants\", args.jobs, aecp_shard) or failed\n",
                  "                aecp_failed = aecp_mutants.campaign(out / \"aecp-mutants\", args.jobs, aecp_shard)\n"
                  "                failed = (aecp_failed and args.shard is None) or failed\n")),
    ("drv-shard-mode-skips-srp-if1", "fail", SHARDS,
     replace_once(DRV, "    failed = srp_mutants.campaign(out / \"srp-mutants\", lwsrp, args.jobs)\n",
                  "    failed = srp_mutants.campaign(out / \"srp-mutants\", lwsrp, args.jobs)\n"
                  "    if args.shard is not None:\n        return failed\n")),
    ("drv-shard-mode-skips-pin-controls", "fail", SHARDS,
     replace_once(DRV, "    return ctrl_mutants.lwsrp_pin_arms(out / \"mutants\", lwsrp) != 0 or failed\n",
                  "    if args.shard is not None:\n        return failed\n"
                  "    return ctrl_mutants.lwsrp_pin_arms(out / \"mutants\", lwsrp) != 0 or failed\n")),
    ("drv-shard-mode-halves-control-table", "fail", SHARDS,
     replace_once(DRV, "                                               args.slice, args.mutation_shard) or failed\n",
                  "                                               (1, 2) if args.shard else args.slice, args.mutation_shard) or failed\n")),
    ("drv-shard-mode-aecp-in-two-shards", "fail", SHARDS,
     replace_once(DRV, "    return PHASES if shard is None else (PHASES[shard[0]],)\n",
                  "    return PHASES if shard is None else ((PHASES[shard[0]], \"aecp\") if shard[0] == 1 else (PHASES[shard[0]],))\n")),
    ("drv-shard-mode-loses-srp-phase", "fail", SHARDS,
     replace_once(DRV, "    return PHASES if shard is None else (PHASES[shard[0]],)\n",
                  "    return PHASES if shard is None else (PHASES[min(shard[0], 2)],)\n")),
    # a real future shape: a new endstation config is discovered without any ownership edit
    ("future-endstation-shape", "pass", SHARDS,
     new_file("configs/endstation_r620_probe.yaml", None)),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def main():
    results = []
    for name, expect, cmd, (rel, edit) in PROBES:
        path = TREE / rel
        before = sha(path)
        original = path.read_bytes() if path.exists() else None
        if isinstance(edit, tuple):
            src = TREE / "configs/endstation_arty_4x4.yaml"
            path.write_bytes(src.read_bytes())
        else:
            text = original.decode()
            mutated = edit(text)
            assert mutated != text, name
            path.write_text(mutated)
        try:
            proc = subprocess.run(cmd, cwd=TREE, capture_output=True, text=True, timeout=900)
            rc, out = proc.returncode, proc.stdout + proc.stderr
        finally:
            if original is None:
                path.unlink()
            else:
                path.write_bytes(original)
        assert sha(path) == before, f"{name}: restore failed"
        key = [ln for ln in out.splitlines()
               if any(w in ln for w in ("FINDING", "differs", "must", "Assertion", "escaped", "PASS:", "preserved",
                                        "live invocations", "Error", "not "))][-4:]
        ok = (rc != 0) if expect == "fail" else (rc == 0)
        if expect == "fail" and cmd is SHARDS:
            ok = ok and "AssertionError" in out and "Traceback" in out and "ModuleNotFoundError" not in out
        results.append({"probe": name, "expect": expect, "rc": rc, "ok": ok, "file": rel,
                        "command": " ".join(c if c != str(TREE) else "<probe-tree>" for c in cmd),
                        "evidence": key})
        print(f"{'OK ' if ok else 'BAD'} {name}: expect {expect}, rc={rc} :: {key[:2]}")
    OUT.write_text(json.dumps(results, indent=1) + "\n")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
