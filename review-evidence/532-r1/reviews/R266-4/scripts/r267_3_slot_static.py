#!/usr/bin/env python3
"""Static check of R267-3's published slot mutants against a head's scripts/act_ci.py.

usage: r267_3_slot_static.py SLOT_MUTANTS_PY ACT_CI_PY

Nothing from act_ci.py is executed. For each mutant it reports whether every
edit applies exactly once to ACT_CI_PY. For the refusal-count mutants it then
evaluates a hand-written model of the mutated guard (`exhausted = ...;
if <cond>: refuse`) on each OOM fixture of selftest_slot_memory_cap, and says
which fixtures would stop being refused, i.e. which arms must fail.
"""
import ast
import pathlib
import re
import sys


def load_mutants(path: pathlib.Path):
    """The MUTANTS list and REPORT_PRINT of the published script, read without running it."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    values = {}
    for node in tree.body:
        target = getattr(node, "target", None) or (node.targets[0] if isinstance(node, ast.Assign) else None)
        if isinstance(target, ast.Name) and target.id in {"MUTANTS", "REPORT_PRINT"}:
            values[target.id] = node.value
    report_print = ast.literal_eval(values["REPORT_PRINT"])
    mutants = []
    for element in values["MUTANTS"].elts:
        ident, described, edits = element.elts
        pairs = []
        for pair in edits.elts:
            old, new = pair.elts
            old_value = report_print if isinstance(old, ast.Name) else ast.literal_eval(old)
            pairs.append((old_value, ast.literal_eval(new)))
        mutants.append((ast.literal_eval(ident), ast.literal_eval(described), pairs))
    return mutants


def fixtures(source: str):
    """The (events, described) fixtures that the head's arm loop expects refused for an OOM at the cap."""
    body = source[source.index("def selftest_slot_memory_cap"):]
    body = body[: body.index("\ndef ", 1)]
    found = [(ast.literal_eval(f'"{events}"'), described)
             for events, described in re.findall(r'\(\s*"([^"]*oom [0-9][^"]*)",\s*"([^"]+)"', body)]
    # Only the fixtures refused for an OOM: both counts present and a nonzero oom.
    return [(events, described) for events, described in found
            if {"oom", "max"} <= set(dict(e.split() for e in events.splitlines()))
            and int(dict(e.split() for e in events.splitlines())["oom"])]


# Hand-written model of each refusal-count variant: exhausted count, then the refusal test.
MODELS = {
    "head": (lambda e: int(e["oom"]), lambda x, h: bool(x)),
    "S04": (lambda e: int(e.get("oom_kill", 0)), lambda x, h: bool(x)),
    "S06": (lambda e: int(e["oom"]), lambda x, h: False),
    "S07": (lambda e: int(e["oom"]), lambda x, h: x > 1),
    "S09": (lambda e: int(e.get("oom", 0)), lambda x, h: bool(x)),
    "S10": (lambda e: int(e.get("oom_group_kill", e["oom"])), lambda x, h: bool(x)),
}


def main() -> int:
    mutants = load_mutants(pathlib.Path(sys.argv[1]))
    source = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    cases = fixtures(source)
    print(f"# OOM fixtures in the head's selftest_slot_memory_cap: {len(cases)}")
    for events, described in cases:
        print(f"#   {described!r}: {events!r}")
    for ident, described, edits in mutants:
        counts = [source.count(old) for old, _new in edits]
        applies = all(count == 1 for count in counts)
        line = f"{ident} applies={'once' if applies else counts} | {described}"
        if ident in MODELS:
            count, refuses = MODELS[ident]
            lost = []
            for events, fixture in cases:
                parsed = dict(entry.split() for entry in events.splitlines())
                if not refuses(count(parsed), int(parsed["max"])):
                    lost.append(fixture)
            line += f" | fixtures no longer refused (their arms must fail): {lost or 'none'}"
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
