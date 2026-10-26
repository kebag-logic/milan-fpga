#!/usr/bin/env python3
"""Round-2 rerun of round1/probe_key_inputs.py at a head whose tool key carries a `hashFiles` term.

Usage: probe_key_inputs_r2.py <head-tree> <receipt-dir>

Part 1 runs round 1's probe body unchanged; only its `resolved_key` is extended to
resolve `hashFiles('<path>', ...)` the way the hosted runner does (SHA-256 of the
concatenated per-file SHA-256 digests, over the checkout). The unmodified round-1
probe stops on that term with an AssertionError, which is recorded separately.
Part 2 adds the edits round 2 is asked to plant: environment inputs the delta now
claims to bind, a content edit of the script the build reads, and edits that only
schedule the tool job, which must leave the key unchanged.
"""
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import sys
from contextlib import redirect_stdout
from unittest.mock import patch

HERE = pathlib.Path(__file__).resolve().parent


def github_hash_files(tree: pathlib.Path, paths: list[str], override: dict[str, bytes]) -> str:
    """hashFiles over literal paths: SHA-256 over the concatenated per-file SHA-256 digests."""
    outer = hashlib.sha256()
    for path in sorted(paths):
        data = override.get(path, (tree / path).read_bytes())
        outer.update(hashlib.sha256(data).digest())
    return outer.hexdigest()


def main() -> int:
    tree, receipts = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    receipts.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("round1_probe", HERE / "round1" / "probe_key_inputs.py")
    round1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(round1)
    override: dict[str, bytes] = {}
    plain = round1.resolved_key.__code__

    def resolved_key(workflow: dict) -> str:
        step = next(s for s in workflow["jobs"][round1.TOOL]["steps"] if s.get("name") == "Cache the pinned Yosys build")
        key = step["with"]["key"]
        key = re.sub(r"\$\{\{\s*hashFiles\(([^)]*)\)\s*\}\}",
                     lambda m: github_hash_files(tree, re.findall(r"'([^']*)'", m.group(1)), override), key)
        step = copy.deepcopy(workflow)
        next(s for s in step["jobs"][round1.TOOL]["steps"]
             if s.get("name") == "Cache the pinned Yosys build")["with"]["key"] = key
        return original(step)

    original = round1.resolved_key
    round1.resolved_key = resolved_key
    out = io.StringIO()
    sys.argv = [sys.argv[0], str(tree), str(receipts / "part1")]
    with redirect_stdout(out):
        round1.main()
    part1 = out.getvalue()
    assert plain is original.__code__

    # Part 2: the round-2 plants, through the same generator and resolution.
    gen = sys.modules["ci_gate_workflows"]
    runtime = importlib.import_module("ci_runtime_workflows")
    template = gen.load_template(tree, "rtl-fast")
    base = resolved_key(gen.generate("rtl-fast", template))

    def key_of(changed: dict) -> str:
        return resolved_key(gen.generate("rtl-fast", changed))

    def with_template(edit) -> str:
        changed = copy.deepcopy(template)
        edit(changed)
        return key_of(changed)

    budget = runtime.cpu_budget_step

    def budget_export(*args):
        step = budget(*args)
        step["run"] = step["run"].replace("} >> \"$GITHUB_ENV\"", "  printf 'CXXFLAGS=%s\\n' -O0\n} >> \"$GITHUB_ENV\"")
        return step

    def patched_budget() -> str:
        with patch.object(runtime, "cpu_budget_step", budget_export):
            return key_of(copy.deepcopy(template))

    def script_content() -> str:
        path = "scripts/ci_install_cache.py"
        override[path] = (tree / path).read_bytes() + b"\n# planted content edit\n"
        try:
            return key_of(copy.deepcopy(template))
        finally:
            override.clear()

    consumer = round1.CONSUMER
    rows = [
        ("E1 workflow env gains CXXFLAGS=-O0 (planted environment edit)", True,
         with_template(lambda t: t["env"].__setitem__("CXXFLAGS", "-O0"))),
        ("E2 yosys-elaboration job env gains CXXFLAGS=-O0 (carried into the tool job)", True,
         with_template(lambda t: t["jobs"][consumer].__setitem__("env", {"CXXFLAGS": "-O0"}))),
        ("E3 workflow defaults: run shell changed", True,
         with_template(lambda t: t.__setitem__("defaults", {"run": {"shell": "bash --noprofile --norc -eo pipefail {0}"}}))),
        ("E4 generated job-budget step exports CXXFLAGS=-O0", True, patched_budget()),
        ("E5 content edit of scripts/ci_install_cache.py (read by the build's package step)", True, script_content()),
        ("E6 yosys-elaboration if gains && !cancelled() (schedules the tool job only)", False,
         with_template(lambda t: t["jobs"][consumer].__setitem__(
             "if", "${{ needs.changes.outputs.rtl == 'true' && !cancelled() }}"))),
        ("E7 yosys-elaboration timeout 30 -> 25 (consumer only)", False,
         with_template(lambda t: t["jobs"][consumer].__setitem__("timeout-minutes", 25))),
        ("E8 'Fetch RTL dependencies' body edit in yosys-elaboration (outside the build)", False,
         with_template(lambda t: next(s for s in t["jobs"][consumer]["steps"]
                                      if s.get("name") == "Fetch RTL dependencies").__setitem__(
             "run", "git submodule update --init --depth 1 third_party/verilog-axis protocol-processor gptp-processor"))),
    ]
    lines = ["pristine key: " + base]
    result = []
    for label, changes_tool, key in rows:
        stale = changes_tool and key == base
        spurious = not changes_tool and key != base
        verdict = "STALE-SERVED" if stale else ("OVER-BOUND  " if spurious else "ok          ")
        lines.append(verdict + " tool-changes=" + str(changes_tool) + " key-changed=" + str(key != base) + "  " + label)
        result.append({"edit": label, "changes_built_tool": changes_tool, "key_changed": key != base, "key": key})
    (receipts / "part2.json").write_text(json.dumps({"pristine_key": base, "rows": result}, indent=1) + "\n")
    print("== part 1: round-1 probe body, hashFiles resolved ==")
    print(part1, end="")
    print("== part 2: round-2 plants ==")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
