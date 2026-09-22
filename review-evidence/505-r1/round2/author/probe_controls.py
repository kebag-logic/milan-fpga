"""Preservation, reason-specific arms and actual CLI maintenance controls."""
import ast
from collections import Counter
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys


def load(path):
    spec = importlib.util.spec_from_file_location("ci_events_controls", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def functions(source):
    return {node.name: ast.dump(node, include_attributes=False)
            for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}


root, out = map(Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
baseline = out.parent / "before/real.py"
before = load(baseline)
after = load(root / "scripts/ci_events.py")
pristine = after.parse_world(after.read_tree(root))
old_arms = {name: (mutate, want) for name, mutate, want in before._mutations(pristine)}
new_arms = after._mutations(pristine)
assert len({name for name, _, _ in new_arms}) == len(new_arms)
new_by_name = {name: (mutate, want) for name, mutate, want in new_arms}
assert old_arms.keys() <= new_by_name.keys()
for name, (mutate, want) in old_arms.items():
    changed_before, changed_after = copy.deepcopy(pristine), copy.deepcopy(pristine)
    mutate(changed_before)
    new_by_name[name][0](changed_after)
    assert new_by_name[name][1] == want and changed_before == changed_after, name
old_functions = functions(baseline.read_text())
new_functions = functions((root / "scripts/ci_events.py").read_text())
changed_functions = [name for name, tree in old_functions.items() if tree != new_functions[name]]
assert set(changed_functions) == {"_carrier_script_edits", "_carrier_script_arms"}
assert before.CARRIER_STEP_LISTS == after.CARRIER_STEP_LISTS

rows = []
for name, mutate, want in new_arms:
    if name in old_arms:
        continue
    world = copy.deepcopy(pristine)
    mutate(world)
    findings = after.check(world).findings
    matching = [finding for finding in findings if want in finding]
    assert matching, (name, want, findings)
    rows.append({"name": name, "expected": want, "matching": matching})
(out / "new-arm-reasons.json").write_text(json.dumps(rows, indent=2) + "\n")

swallowing = []
for path, jid, at, step in after._carrier_run_steps(pristine):
    lines = after.normalize_script(step["run"])
    for n, line in enumerate(lines):
        lever = "or-true" if n == len(lines) - 1 else f"or-true-line-{n + 1}"
        label = f"carrier-script-407 {jid} step {at + 1} {lever}"
        mutate, want = new_by_name[label]
        assert f"line {n + 1} must be {line!r}" in want
        world = copy.deepcopy(pristine)
        mutate(world)
        actual = after.normalize_script(after._job_steps(world, path, jid)[at]["run"])
        expected = list(lines)
        expected[n] += " || true"
        assert actual == expected
        swallowing.append({"arm": label, "job": jid, "step": at + 1,
                           "name": step["name"], "line": n + 1, "command": line})
(out / "swallowing-inventory.json").write_text(json.dumps(swallowing, indent=2) + "\n")
bounded = [row for row in swallowing if " --check" in row["command"]]
(out / "check-call-inventory.json").write_text(json.dumps(bounded, indent=2) + "\n")

# Existing specialized refusals must still work when the carrier-body helper is disabled.
real_helper = after.check_carrier_script
after.check_carrier_script = lambda *args, **kwargs: None
specialized = [arm for arm in new_arms if not arm[0].startswith("carrier-script-407 ")]
for name, mutate, want in specialized:
    world = copy.deepcopy(pristine)
    mutate(world)
    assert any(want in finding for finding in after.check(world).findings), name
after.check_carrier_script = real_helper

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    whitespace_problems, whitespace_arms = after._selftest_whitespace(pristine)
    record_problems, record_arms = after._selftest_carrier_script_pins(pristine)
assert not whitespace_problems and not record_problems
(out / "positive-controls.log").write_text(buf.getvalue())

# Exercise documented maintenance through actual CLI, changing only a scratch workflow and record.
fixture = out / "maintenance"
for rel, content in after.read_tree(root).items():
    target = fixture / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
workflow = fixture / after.DOCS
needle = "          python3 scripts/check_py_idiom.py --selftest\n"
assert workflow.read_text().count(needle) == 1
workflow.write_text(workflow.read_text().replace(needle, needle + "          echo maintenance\n", 1))
source = (root / "scripts/ci_events.py").read_text()
record_needle = "'python3 scripts/check_py_idiom.py --selftest',"
assert source.count(record_needle) == 1
updated = source.replace(record_needle, record_needle + "\n             'echo maintenance',", 1)
(fixture / "ci_events.py").write_text(updated)
results = []
for name, script, mode, expected_rc in [
    ("workflow-only", root / "scripts/ci_events.py", "--check", 1),
    ("matching-record-check", fixture / "ci_events.py", "--check", 0),
    ("matching-record-selftest", fixture / "ci_events.py", "--selftest", 0),
]:
    command = [sys.executable, "-B", str(script), mode, "--root", str(fixture)]
    proc = subprocess.run(command, text=True, capture_output=True)
    (out / f"{name}.log").write_text(proc.stdout + proc.stderr)
    assert proc.returncode == expected_rc, name
    results.append({"name": name, "command": command, "exit": proc.returncode,
                    "last_line": proc.stdout.splitlines()[-1]})
    if name == "workflow-only":
        assert "Python idiom gate" in proc.stdout and "line 3" in proc.stdout

source_delta = subprocess.check_output(["git", "diff", "--name-only", "6af65a151663e1301f1983a6c9d22650a0b35da9"],
                                       cwd=root, text=True).splitlines()
assert set(source_delta) == {"scripts/ci_events.py", "docs/testing/CI_WORKFLOWS.md"}
summary = {
    "preserved_old_mutations": len(old_arms), "preserved_specialized_refusals": len(specialized),
    "changed_functions": changed_functions, "new_reason_pinned_arms": len(rows),
    "new_by_lever": dict(Counter(row["name"].rsplit(" ", 1)[1].split("-line-")[0] for row in rows)),
    "all_mutation_arms": len(new_arms), "carrier_mutation_arms": len(after._carrier_script_arms(pristine)),
    "swallowing_lines": len(swallowing), "check_calls": len(bounded),
    "carrier_run_bodies": len(list(after._carrier_run_steps(pristine))),
    "whitespace_control_arms": whitespace_arms, "record_control_arms": record_arms,
    "maintenance": results, "changed_paths": source_delta,
}
(out / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
