"""Execute actual CLI checker mutants against isolated gate-input snapshots."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys


def load(source):
    spec = importlib.util.spec_from_file_location("ci_events_probe", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--phase", choices=("before", "after"), required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    source = (args.root / "scripts/ci_events.py").read_text()
    ce = load(args.root / "scripts/ci_events.py")
    fixture = args.output / "inputs"
    for rel, data in ce.read_tree(args.root).items():
        target = fixture / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(data)
    compare = "c.item(tuple(lines) == canonical, path,"
    record = "c.item(recorded, path,"
    start = source.index("def check_carrier_script(")
    end = source.index("\ndef check_carrier_steps(", start)
    helper = source[start:end]
    assert helper.count(compare) == helper.count(record) == 1
    comparators = {
        "M5b": "len(lines) == len(canonical) and all("
        "(re.sub(r' \\|\\| true$', '', a) == re.sub(r' \\|\\| true$', '', b)) "
        "if i < len(lines) - 1 else a == b "
        "for i, (a, b) in enumerate(zip(lines, canonical)))",
        "prefix-only": "tuple(lines[:len(canonical)]) == canonical",
        "order-insensitive": "sorted(lines) == sorted(canonical)",
        "removed-comparator": "True",
    }
    variants = {"real": source}
    variants.update({name: source.replace(helper, helper.replace(compare, f"c.item({expression}, path,"))
                     for name, expression in comparators.items()})
    variants["removed-record-enforcement"] = source.replace(helper, helper.replace(record, "c.item(True, path,"))
    (args.output / "definitions.json").write_text(json.dumps({
        "comparison_original": compare, "comparators": comparators,
        "record_original": record, "record_replacement": "c.item(True, path,",
    }, indent=2) + "\n")
    results = []
    for name, variant in variants.items():
        mutant = args.output / f"{name}.py"
        mutant.write_text(variant)
        row = {"mutant": name}
        for mode in ("--check", "--selftest"):
            command = [sys.executable, "-B", str(mutant), mode, "--root", str(fixture)]
            proc = subprocess.run(command, text=True, capture_output=True)
            log = args.output / f"{name}-{mode[2:]}.log"
            log.write_text(proc.stdout + proc.stderr)
            failures = [line for line in proc.stdout.splitlines() if line.startswith("  FAIL ")]
            row[mode[2:]] = {"command": command, "exit": proc.returncode,
                            "last_line": proc.stdout.splitlines()[-1], "failures": len(failures)}
            expected = 0 if mode == "--check" or name == "real" else 1
            if args.phase == "before" and name in ("M5b", "prefix-only", "order-insensitive"):
                expected = 0
            assert proc.returncode == expected, (name, mode, proc.returncode, expected, log)
            if args.phase == "after" and name == "M5b" and mode == "--selftest":
                assert any("Python idiom gate" in line and "line 1" in line for line in failures)
        module = load(mutant)
        pristine = module.parse_world(module.read_tree(fixture))
        world = copy.deepcopy(pristine)
        step = next(s for s in world[module.DOCS]["jobs"]["docs-check"]["steps"]
                    if s.get("name") == "Python idiom gate")
        assert step["run"].splitlines()[0] == "python3 scripts/check_py_idiom.py"
        step["run"] = step["run"].replace("python3 scripts/check_py_idiom.py\n",
                                        "python3 scripts/check_py_idiom.py || true\n", 1)
        findings = module.check(world).findings
        row["ac5_analogue_findings"] = findings
        if name == "real":
            assert len(findings) == 1 and "line 1" in findings[0]
        elif name == "M5b":
            assert not findings
        results.append(row)
        print(name, row["check"]["last_line"], row["selftest"]["last_line"],
              "AC5 findings:", len(findings), flush=True)
        (args.output / "results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
