#!/usr/bin/env python3
"""Apply one named source mutation to a disposable tree and run its control.

Usage: mutate.py <pristine-tree> <work-root> <log-dir> <name>
Each mutation replaces one exact literal that must occur exactly once, so a
probe never passes because its edit silently missed. The pristine tree is
copied; it is never modified. Writes <log-dir>/<name>.json.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

MUTATIONS = {
    # R636-2-S1: accept the drivers' real "failed" outcome.
    "s1-accept-failed": ("scripts/ci_case_receipts.py",
                         'outcome not in ("pass", "caught")',
                         'outcome not in ("pass", "caught", "failed")',
                         ["scripts/ci_case_receipts_selftest.py"]),
    # R636-2-S2: allow skipped steps in completion_errors.
    "s2-allow-skipped": ("scripts/ci_manifest.py",
                         'if observed["outcome"] != "success" or observed["skip_reason"] is not None:',
                         'if observed["outcome"] not in ("success", "skipped"):',
                         ["scripts/ci_manifest_selftest.py"]),
    # R636-2-S4: remove the single-scope check.
    "s4-drop-single-scope": ("scripts/ci_gate_receipts.py",
                             "if len(scopes) != 1 or sorted(seen)",
                             "if sorted(seen)",
                             ["scripts/ci_gate_workflows_selftest.py"]),
    # Item 1: generator check disabled.
    "i1-check-noop": ("scripts/ci_suite_workflows.py",
                      '    readers = ("scripts/ci_suite_pieces.py",',
                      '    return\n    readers = ("scripts/ci_suite_pieces.py",',
                      ["scripts/ci_gate_workflows_selftest.py"]),
    # Item 1: collector loses its preparation (generator only; committed YAML unchanged).
    "i1-collector-unprepared": ("scripts/ci_runtime_workflows.py",
                                "                inventory_dependencies(),\n",
                                "",
                                ["scripts/ci_gate_workflows_selftest.py", "scripts/ci_gate_workflows.py --check",
                                 "scripts/ci_events.py --check"]),
    # Item 1: a conditional preparation must not count as prepared.
    "i1-conditional-prep-accepted": ("scripts/ci_suite_workflows.py",
                                     'if body.strip() == preparation and "if" not in step and not step.get("continue-on-error"):',
                                     'if body.strip() == preparation:',
                                     ["scripts/ci_gate_workflows_selftest.py"]),
    # Item 2: collector records a raw-skipped leg as success.
    "i2-skip-as-success": ("scripts/ci_runtime_evidence.py",
                           '                results[key] = "skipped"\n',
                           '                results[key] = "success"\n',
                           ["scripts/ci_runtime_evidence_selftest.py"]),
    # Item 2: collector ignores raw skipped names (old behaviour).
    "i2-collector-no-raw": ("scripts/ci_runtime_evidence.py",
                            '    skipped = source.get("skipped", {}).get(path, {})\n',
                            '    skipped = {}\n',
                            ["scripts/ci_runtime_evidence_selftest.py"]),
    # Item 2: collector stops refusing raw/expanded overlap.
    "i2-collector-overlap": ("scripts/ci_runtime_evidence.py",
                             '                if key in results:\n                    raise ValueError("API expanded and unexpanded matrix jobs overlap")\n',
                             '',
                             ["scripts/ci_runtime_evidence_selftest.py"]),
    # Item 2: watcher stops refusing unknown names.
    "i2-watcher-unknown": ("scripts/ci_fail_fast.py",
                           '        raise ValueError("API returned an unplanned job name")',
                           '        pass',
                           ["scripts/ci_runtime_evidence_selftest.py", "scripts/ci_fail_fast_selftest.py"]),
    # Item 3: collector treats an observer outage as a genuine failure.
    "i3-collector-outage-fails": ("scripts/ci_runtime_evidence.py",
                                  "        except OSError as exc:\n            observer_error(exc)\n",
                                  "        except OSError as exc:\n            raise\n",
                                  ["scripts/ci_runtime_evidence_selftest.py"]),
    # Item 3: collector reads lose their shared budget.
    "i3-no-shared-budget": ("scripts/ci_runtime_evidence.py",
                            'api = API(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"], RETRY_BUDGET_SECONDS)',
                            'api = API(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"])',
                            ["scripts/ci_runtime_evidence_selftest.py"]),
    # Item 3: tail guard honours collector observer-only output no longer.
    "i3-tail-ignores-collector": ("scripts/ci_fail_fast.py",
                                  'job in ("ci-fail-fast", "ci-manifest")',
                                  'job == "ci-fail-fast"',
                                  ["scripts/ci_runtime_evidence_selftest.py", "scripts/ci_fail_fast_selftest.py"]),
    # Item 3: watcher outage returns a failed conclusion again.
    "i3-watcher-outage-fails": ("scripts/ci_fail_fast.py",
                                "        observer_error(exc)\n        return 0\n",
                                "        observer_error(exc)\n        return 2\n",
                                ["scripts/ci_fail_fast_selftest.py"]),
    # Item 3: collector limit no larger than its read budget.
    "i3-collector-limit": ("scripts/ci_runtime_workflows.py",
                           '"timeout-minutes": 15,',
                           '"timeout-minutes": 10,',
                           ["scripts/ci_runtime_evidence_selftest.py"]),
    # Item 3: collector observer-only output dropped from the generated graph.
    "i3-collector-no-output": ("scripts/ci_runtime_workflows.py",
                               "steps.ci_collect.outcome == 'success' && steps.ci_upload.outcome == 'success' }}\"},",
                               "steps.ci_collect.outcome == 'success' }}\"},",
                               ["scripts/ci_runtime_evidence_selftest.py"]),
    # Item 4: contract gates fall back onto worker zero.
    "i4-contract-on-worker0": ("scripts/ci_gate_workflows.py",
                               '"leg": (2 if name == "docs" and step.get("name") in CONTRACT_GATES',
                               '"leg": (0 if name == "docs" and step.get("name") in CONTRACT_GATES',
                               ["scripts/ci_gate_workflows_selftest.py"]),
    # Item 4: Yosys build returned to the timed synthesis worker.
    "i4-yosys-inline": ("scripts/ci_suite_workflows.py",
                        "    separate_yosys_build(source)\n",
                        "",
                        ["scripts/ci_gate_workflows_selftest.py"]),
    # Item 5: tool build bound raised to all CPUs.
    "i5-unbounded-tool-build": ("scripts/ci_runtime_workflows.py",
                                "tool_build=$(( cpus < 8 ? cpus : 8 ))",
                                "tool_build=$cpus",
                                ["scripts/ci_gate_workflows_selftest.py"]),
}


def main() -> int:
    pristine, work, logs, name = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    path, old, new, controls = MUTATIONS[name]
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(pristine, tree, symlinks=True)
    target = tree / path
    text = target.read_text()
    count = text.count(old)
    record = {"mutation": name, "file": path, "matches": count, "controls": []}
    if count != 1:
        record["error"] = "literal must match exactly once"
    else:
        target.write_text(text.replace(old, new))
        for control in controls:
            argv = [sys.executable, *control.split()]
            start = time.monotonic()
            result = subprocess.run(argv, cwd=tree, capture_output=True, text=True)
            output = result.stdout + result.stderr
            (logs / f"{name}--{Path(control.split()[0]).stem}.log").write_text(output)
            record["controls"].append({
                "command": "python3 " + control, "rc": result.returncode,
                "seconds": round(time.monotonic() - start, 3),
                "log_sha256": hashlib.sha256(output.encode()).hexdigest(),
                "tail": output.strip().splitlines()[-3:]})
    record["caught"] = bool(record["controls"]) and any(c["rc"] != 0 for c in record["controls"])
    (logs / f"{name}.json").write_text(json.dumps(record, indent=2) + "\n")
    shutil.rmtree(tree)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
