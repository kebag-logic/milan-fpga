#!/usr/bin/env python3
"""One-time source edit: write reviewed literal records, never a runtime generator."""
import ast
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path.cwd() / "scripts"))
import ci_events as ci
path = Path("scripts/ci_events.py")
source = path.read_text()
world = ci.parse_world(ci.read_tree(Path.cwd()))
lines = source.splitlines(keepends=True)
offsets = [0]
for line in lines:
    offsets.append(offsets[-1] + len(line))

def location(row, column):
    return offsets[row-1] + column

def render_script(body, indent):
    chunks = ["("]
    for line in body:
        # Split Python string literals without changing the recorded bytes.
        while len(repr(line)) + indent > 112:
            cut = line.rfind(" ", 0, 82)
            if cut < 1:
                break
            chunks.append(" " * indent + repr(line[:cut+1]))
            line = line[cut+1:]
        chunks.append(" " * indent + repr(line) + ",")
    chunks.append(" " * (indent-4) + ")")
    return "\n".join(chunks)

common = {}
for jid, name, constant in (
    ("verilator-shards", "Fetch RTL dependencies", "RTL_FETCH_SCRIPT"),
    ("verilator-shards", "Build Verilator from source on cache miss", "RTL_VERILATOR_BUILD_SCRIPT"),
    ("yosys-shards", "Build Yosys from source on cache miss", "RTL_YOSYS_BUILD_SCRIPT"),
    ("yosys-shards", "Install the pinned Yosys and prove the version", "RTL_YOSYS_INSTALL_SCRIPT"),
):
    step = next(s for s in ci.steps(ci.jobs(world[ci.RTL_FULL])[jid]) if s.get("name") == name)
    common[tuple(ci.normalize_script(step["run"]))] = constant
edits = []
for node in ast.parse(source).body:
    if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
        continue
    table = node.targets[0].id
    if table not in ("RTL_STEP_LISTS", "RTL_SIBLING_STEP_LISTS"):
        continue
    for key_node, entries_node in zip(node.value.keys, node.value.values):
        # Only trusted local repository literals/constants are evaluated.
        key = eval(compile(ast.Expression(key_node), "record-key", "eval"), vars(ci))
        if table == "RTL_SIBLING_STEP_LISTS" and key != (ci.RTL_FULL, ci.GATE_JOB):
            continue
        workflow, jid = key
        ss = ci.steps(ci.jobs(world[workflow])[jid])
        for at, entry_node in enumerate(entries_node.elts):
            step = ss[at]
            if "run" not in step:
                continue
            if table == "RTL_SIBLING_STEP_LISTS" and step.get("id") != ci.PIN_STEP_ID:
                continue
            body = tuple(ci.normalize_script(step["run"]))
            if (workflow, jid, step["name"]) in ci.ENV_FILE_WRITERS:
                value = f"ENV_FILE_WRITERS[({workflow!r}, {jid!r},\n" + " " * 34 + repr(step["name"]) + ")]"
                value = value.replace(repr(ci.RTL_FULL), "RTL_FULL").replace(repr(ci.RTL_FAST), "RTL_FAST")
            elif body == ci.CANONICAL_OWNERSHIP_SCRIPT:
                value = "CANONICAL_OWNERSHIP_SCRIPT"
            elif (jid, step["name"]) in ci.AGGREGATE_SCRIPTS:
                constant = next(k for k,v in vars(ci).items() if k.endswith("_STEP") and v == step["name"])
                value = f"AGGREGATE_SCRIPTS[({jid!r}, {constant})]"
            elif body == ci.SV2V_INSTALL:
                value = "SV2V_INSTALL"
            elif body == (ci.OOC_SH_SELFTEST,):
                value = "(OOC_SH_SELFTEST,)"
            else:
                value = common.get(body, render_script(body, 13))
            end = location(entry_node.end_lineno, entry_node.end_col_offset)-1
            edits.append((end, ',\n         "run": ' + value))
for end, insertion in sorted(edits, reverse=True):
    source = source[:end] + insertion + source[end:]
constants = "#: #439: shared literal scripts of the seven RTL jobs. Update these with\n#: the matching workflow bodies; never derive expected text during checking.\n"
for body, constant in common.items():
    constants += constant + " = " + render_script(body, 4) + "\n"
source = source.replace("RTL_STEP_LISTS = {", constants + "\nRTL_STEP_LISTS = {", 1)
path.write_text(source)
print(f"Recorded {len(edits)} run scripts; reused specialized constants and {len(common)} shared RTL scripts")
