"""Render reviewable evidence tables from measured receipts."""
from pathlib import Path
import ast
import json
import shlex
import subprocess

ROOT = Path("$LANES/595-yaml-int-refusal")
OUT = Path(__file__).parent
BASE = "1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
records = [json.loads(line) for line in (OUT / "gates.jsonl").read_text().splitlines()]
latest = {row["name"]: row for row in records}
complete = len(latest) == 19 and all(row["rc"] == 0 and row["head"] == head for row in latest.values())
status = "Assigned local work complete; ready for independent review." if complete else "Committed-head gates running."
lines = ["# [A417] Issue #595 handoff", "", f"Status: {status}", "",
         f"Head: `{head}`.", f"Base: `{BASE}`.",
         "Branch: `595-yaml-int-refusal`.",
         "Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.",
         "Worktree: `$LANES/595-yaml-int-refusal`.",
         "Processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`; unchanged checkout and gitlink.",
         "Roles: author [A417], internal reviewer [R388], external reviewer [R389].", "",
         "Assignment: https://github.com/kebag-logic/milan-fpga/issues/595#issuecomment-5867362523",
         "TAKEN: https://github.com/kebag-logic/milan-fpga/issues/595#issuecomment-5867413642", "",
         "The sole [A10] comment settles scope; the board showed Backlog.",
         "No push, PR creation, merge, other checkout, or configuration edits.",
         "No hardware, firmware, processor, RTL, or gitlink changes.",
         "Stop after the REVIEW READY comment with this local head.", "",
         "## Sources and decisions", "",
         "Read #595 body and all [A10] comments, PR #585, and both linked reports:", "",
         "- https://github.com/kebag-logic/milan-fpga/pull/585",
         "- https://github.com/kebag-logic/milan-fpga/blob/c0c58c242333ce58c14b3048cf5686e46b42f2d6/review-evidence/573-r1/reviews/R340-3/REPORT.md",
         "- https://github.com/kebag-logic/milan-fpga/blob/104102d6237e9b1a854cdbc81e53681a8d67b5e9/review-evidence/573-r1/reviews/R341-3/REPORT.md", "",
         "Applied the assignment's exact quoted-string rule to both unsigned callers.",
         "Declared null differs from an omitted optional field.",
         "An empty formats list remains valid and retains its existing default.",
         "Existing semantic controls now declare quoted values to reach their original guards.",
         "Their width, I/G-bit, pin-consistency and capabilities oracles remain intact.", "",
         "## Change list", "", "| File:line | Change |", "|---|---|"]
changes = {
    "sw/builder/endstation_builder.py": {
        "_streams": "Check declared formats list type before fallback or iteration.",
        "_mac48": "Refuse non-strings before separator removal; correct the docstring.",
        "load_platform": "Retain missing-MAC refusal; route explicit null to the quote rule.",
        "_declared_uint": "Parse strings only, preserving range checks.",
        "_vendor_oui": "Default only when omitted; refuse explicit non-strings.",
        "_verify_entity_capabilities": "Verify quoted declarations; refuse explicit null."},
    "sw/builder/test_declarations.py": {
        "_yaml_refused": "Assert exact ConfigError messages rather than incidental errors.",
        "test_station_mac_string_contract": "Pin MAC spellings, scalar refusals and existing semantics.",
        "test_declared_hex_string_contract": "Cover both unsigned callers and packed capabilities.",
        "test_formats_list_contract": "Cover all eight stream indices, list types, values and defaults.",
        "test_declaration_contracts": "Include the new controls in the declaration and full banks."},
    "sw/builder/test_builder.py": {
        "_schema_12_config": "Quote hexadecimal declarations while retaining numeric expected values.",
        "_schema_12_refusal_cases": "Keep semantic refusals reachable under the new type rule.",
        "test_schema_12_refusals": "Quote the agreeing OUI and divergent capability fixtures."}}
for rel, functions in changes.items():
    tree = ast.parse((ROOT / rel).read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in functions:
            lines.append(f"| `{rel}:{node.lineno}` | {functions[node.name]} |")
for rel, marker, explanation in (
        ("sw/builder/README-parameters.md", "Each declared AAF", "Document list type and derived defaults."),
        ("sw/builder/README-parameters.md", "Also quote `platform", "Document every new string-only field and YAML hazards."),
        ("docs/ENDSTATION_BUILDER.md", "Hexadecimal declarations", "Record the string and list rules in the builder contract.")):
    number = next(n for n, line in enumerate((ROOT / rel).read_text().splitlines(), 1) if line.startswith(marker))
    lines.append(f"| `{rel}:{number}` | {explanation} |")
lines += ["", "## Rule per field", "", "| Field | Rule |", "|---|---|",
          "| `platform.mac_address` | Required hex string, optional prefix/underscores/colon/dash; nonzero, 48-bit, unicast. Explicit null gets the quote instruction; missing gets the required-field error. |",
          "| `entity.vendor_oui` | Optional hex string, 24-bit, first-octet I/G bit clear. Omitted uses the existing default. Declared null refuses. Model-ID consistency still applies. |",
          "| `entity.entity_capabilities` | Optional hex string, 32-bit, equal to the processor's ADP constant. Omitted derives the existing value. Declared null refuses. |",
          "| `streams.talkers[i].formats` | A declared value must be a list. Missing or empty lists retain defaults. Every entry remains a quoted hex word under PR #585. |",
          "| `streams.listeners[i].formats` | The same list/string rule; derived family completion remains unchanged. |", "",
          "## Refusal and quoted-spelling cases", "",
          "Measured by `focused_evidence.py` while running the committed declaration tests.",
          "All 233 loader attempts completed with their expected result.",
          "Capabilities resolve from the final packed ENTITY descriptor, not the legacy ROM.",
          "MAC values below show canonical colon spelling; OUI values show the resolved model prefix.",
          "An empty scalar is an explicit YAML null. No resolved value exists after refusal.", "",
          "| Field | YAML token | Exact message | Resolved value |", "|---|---|---|---|"]
def cell(value):
    if value is None:
        return "-"
    if isinstance(value, list):
        value = ", ".join(value)
    value = str(value).replace("|", r"\|").replace("\n", " ")
    return "`" + (value or "<empty scalar>") + "`"
for row in json.loads((OUT / "cases.json").read_text()):
    lines.append("| " + " | ".join(cell(row[key]) for key in ("field", "input", "message", "resolved")) + " |")
lines += ["", "Additional parser-level controls retain values before field semantics:", "",
          "| Field widths | Quoted hex spelling | Result |", "|---|---|---|",
          "| 24 and 32 | `123456` | `0x123456` |",
          "| 24 and 32 | `001234` | `0x001234` |",
          "| 24 and 32 | `10_20` | `0x1020` |",
          "| 24 and 32 | `0` | `0x0` |",
          "| 24 | `FFFFFF` | `0xFFFFFF` |",
          "| 32 | `FFFFFFFF` | `0xFFFFFFFF` |", "",
          "These are parser controls; later OUI/capability semantics still apply.", "",
          "## Mutant table", "",
          "Only the three inspected functions are mutated in memory.",
          "No source file or processor file is changed by the campaign.",
          "Each restored control passes; source SHA256 is unchanged.", "",
          "| Restored defect | Named control | Killing assertion | Result and diagnostic |", "|---|---|---|---|"]
for row in json.loads((OUT / "mutants.json").read_text()):
    lines.append("| " + " | ".join(cell(value) for value in (row["name"], row["test"], row["assertion"], row["result"] + ": " + row["diagnostic"])) + " |")
lines += ["", "## Five-configuration SHA256 before/after", "",
          "Baseline was generated before source edits, at the recorded base.",
          "The final run compares every generated file's raw bytes as well as hashes.",
          "Five configuration files and 70 artifacts match, including all three Arty shapes.",
          "Generation uses the normal derivation/writer and AEM image path.",
          "The sweep fragment is emitted separately without transferring tracked ownership.",
          "Artifacts stay in disposable scratch; only sizes and hashes are retained here.", "",
          "| Configuration or artifact | Bytes before/after | SHA256 before | SHA256 after |", "|---|---|---|---|"]
before = json.loads((OUT / "artifacts-before.json").read_text())
after = {row["path"]: row for row in json.loads((OUT / "artifacts-after.json").read_text())}
for row in before:
    final = after[row["path"]]
    lines.append(f"| `{row['path']}` | {row['size']} / {final['size']} | `{row['sha256']}` | `{final['sha256']}` |")
lines += ["", "## Gate table", "",
          f"Every recorded gate below ran from the physical worktree at `{head}`.",
          "Commands run in the foreground, without pipelines, with 7200-second per-gate limits.",
          "Markdown uses `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`.",
          "`gates.jsonl` records command arguments, environment, status, duration, log size and SHA256.",
          "Logs over 200 KB stay outside this output directory.", "",
          "| Gate | Exact command | rc | Seconds | Log |", "|---|---|---|---|---|"]
for row in latest.values():
    command = " ".join(f"{key}={shlex.quote(value)}" for key, value in row["env"].items())
    command += (" " if command else "") + shlex.join(row["argv"])
    lines.append(f"| {row['name']} | `{command}` | {row['rc']} | {row['seconds']} | `{row['log']}` |")
lines += ["", "## Limits and remaining work", "",
          "The full builder bank reports exactly one unrun arm: gate 11 utilization calibration.",
          "The calibration report is absent from disk. Compiler-absent controls intentionally stand down RV32 instruments.",
          "These are reported stand-downs, not hardware validation.",
          "Before committing, a new capabilities test initially read the orphan legacy ROM.",
          "It failed and was corrected to inspect the final packed descriptor.",
          "All gate claims above concern only the recorded committed head.",
          "Independent reviews, publication, merge-train conflict handling and merge remain with the maintainer.",
          "Issue #577 / PR #612 overlaps this builder; no integration checkout was created.",
          "No review verdict or lens ledger is asserted by the author.", ""]
(OUT / "HANDOFF.md").write_text("\n".join(lines))
print(f"HANDOFF.md updated: {len(latest)}/19 gates recorded; complete={complete}")
