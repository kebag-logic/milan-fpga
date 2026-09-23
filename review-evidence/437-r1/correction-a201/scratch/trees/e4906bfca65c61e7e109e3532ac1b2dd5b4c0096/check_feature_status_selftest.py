#!/usr/bin/env python3
"""Fixture arms for ``check_feature_status.py`` - a clean case and every
required negative control.

This is the ``--self-test`` half of the ledger gate, kept beside it rather
than inside it: the arms are one long list of independent fixtures, and they
have no reader in common with the checking rules they exercise. Run them
through the gate, which is the only supported entry point:

    python3 scripts/check_feature_status.py --self-test

Every case is a ``(name, passed)`` pair, and the groups below are printed in
the order they are concatenated in ``run_self_test``. Adding a case to the
END of its group is what keeps the printed transcript stable.
"""

import json
import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_feature_status import (  # noqa: E402
    BLOCK_END,
    BLOCK_START,
    check_claims,
    check_source_facts,
    is_active_document_text,
    load_ledger_text,
)


class _Fixtures(NamedTuple):
    """The one ledger and the documents every group of arms mutates."""
    base: dict
    fact_row: str
    prose: str
    order_block: str
    row: str
    ordered_row: str
    ledger: dict
    findings: list
    version_text: str
    command_text: str


def _fixtures():
    """The clean ledger and the documents that agree with it."""
    base = {
        "schema_version": 1,
        "facts": {
            "gateware_version": "0x0002_0051",
            "served_aem_operations": ["READ_DESCRIPTOR"],
            "served_mvu_operations": ["GET_MILAN_INFO"],
            "missing_mandatory_aem_operations": ["SET_NAME"]
        },
        "fact_documents": {
            "served_aem_operations": ["one.md", "two.md"]
        },
        "value_documents": {
            "gateware_version": ["one.md", "two.md"]
        },
        "order_documents": {
            "firmware_boot_order": ["one.md"]
        },
        "features": [{
            "id": "aem.read-descriptor",
            "status": "implemented",
            "summary": "fixture",
            "documents": ["one.md", "two.md"]
        }]
    }
    base["facts"]["firmware_boot_order"] = ["configure_fabric",
                                            "load_aem_image",
                                            "entity_advertise"]
    fact_row = (
        "<!-- milan-feature-fact:served_aem_operations:start -->\n"
        "- `READ_DESCRIPTOR`\n"
        "<!-- milan-feature-fact:served_aem_operations:end -->\n"
    )
    prose = ("Status today, VERSION `0x0002_0051`, serving one AEM opcode "
             "plus one MVU command.\n")
    order_block = (
        "<!-- milan-feature-order:firmware_boot_order:start -->\n"
        "1. `configure_fabric()`\n2. `load_aem_image()`\n"
        "3. `entity_advertise()`\n"
        "<!-- milan-feature-order:firmware_boot_order:end -->\n"
    )
    row = (f"{BLOCK_START}\n| Feature ID | Status | Canonical value |\n"
           "|---|---|---|\n"
           "| `aem.read-descriptor` | `implemented` | - |\n"
           f"{BLOCK_END}\n{fact_row}{prose}")
    ordered_row = row + order_block
    ledger, findings = load_ledger_text(json.dumps(base), "fixture")
    return _Fixtures(base, fact_row, prose, order_block, row, ordered_row,
                     ledger, findings,
                     "parameter logic [31:0] VERSION = 32'h0002_0051;",
                     'SERVED = {0: dict(name="READ_DESCRIPTOR")}\n')


def _ledger_and_claim_cases(fx):
    """Ledger shape, document claim agreement, and what is not an authority."""
    base, fact_row = fx.base, fx.fact_row
    row, ordered_row = fx.row, fx.ordered_row
    ledger, findings = fx.ledger, fx.findings
    cases = []
    cases.append(("clean", not findings and not check_claims(
        ledger, {"one.md": ordered_row, "two.md": row})))

    conflict = row.replace("`implemented`", "`missing`")
    conflict_findings = check_claims(
        ledger, {"one.md": row, "two.md": conflict})
    cases.append(("status conflict", any(
        "aem.read-descriptor" in item and "one.md" in item and "two.md" in item
        for item in conflict_findings)))

    duplicate = json.loads(json.dumps(base))
    duplicate["features"].append(dict(duplicate["features"][0]))
    _, duplicate_findings = load_ledger_text(json.dumps(duplicate), "fixture")
    cases.append(("duplicate identifier", any(
        "duplicate feature identifier" in item for item in duplicate_findings)))

    unknown_status = json.loads(json.dumps(base))
    unknown_status["features"][0]["status"] = "available"
    _, status_findings = load_ledger_text(json.dumps(unknown_status), "fixture")
    cases.append(("unknown status", any(
        "unknown status" in item for item in status_findings)))

    non_string_status = json.loads(json.dumps(base))
    non_string_status["features"][0]["status"] = []
    _, non_string_findings = load_ledger_text(
        json.dumps(non_string_status), "fixture")
    cases.append(("non-string status", any(
        "unknown status" in item for item in non_string_findings)))

    unknown_row = row.replace("aem.read-descriptor", "aem.unknown")
    unknown_findings = check_claims(
        ledger, {"one.md": unknown_row, "two.md": row})
    cases.append(("unknown reference", any(
        "unknown feature identifier 'aem.unknown'" in item
        for item in unknown_findings)))

    header_value_row = row.replace(
        "| `aem.read-descriptor` | `implemented` | - |",
        "| `aem.unknown` | `implemented` | Feature ID |")
    header_value_findings = check_claims(
        ledger, {"one.md": header_value_row, "two.md": row})
    cases.append(("header text in value", any(
        "unknown feature identifier 'aem.unknown'" in item
        for item in header_value_findings)))

    fenced = f"```markdown\n{row}```\n"
    fenced_findings = check_claims(
        ledger, {"one.md": row, "two.md": fenced})
    cases.append(("fenced claim ignored", any(
        "not marked in two.md" in item for item in fenced_findings)))

    fenced_example = row + "\n~~~markdown\n" + unknown_row + "~~~\n"
    fenced_example_findings = check_claims(
        ledger, {"one.md": fenced_example, "two.md": row})
    cases.append(("fenced example ignored", not any(
        "aem.unknown" in item for item in fenced_example_findings)))

    unmarked_findings = check_claims(
        ledger, {"one.md": row, "two.md": row.replace(
            f"{BLOCK_START}\n", "").replace(f"{BLOCK_END}\n", "")})
    cases.append(("unmarked claim rejected", any(
        "outside a marked block" in item for item in unmarked_findings)))

    fact_drift = row.replace("`READ_DESCRIPTOR`", "`SET_NAME`")
    fact_drift_findings = check_claims(
        ledger, {"one.md": row, "two.md": fact_drift})
    cases.append(("operation inventory drift", any(
        "feature fact conflict 'served_aem_operations'" in item and
        "two.md" in item for item in fact_drift_findings)))

    missing_fact_findings = check_claims(
        ledger, {"one.md": row, "two.md": row.replace(fact_row, "")})
    cases.append(("missing operation inventory", any(
        "feature fact 'served_aem_operations' is not marked in two.md" in item
        for item in missing_fact_findings)))

    obsolete = "[OBSOLETE + 2026-08-18]\n" + conflict
    cases.append(("obsolete banner", not is_active_document_text(obsolete,
                                                                  "old.md")))
    cases.append(("archive path", not is_active_document_text(
        conflict, "docs/history/v1/old.md")))
    return cases


def _source_fact_cases(fx):
    """Facts tied back to the declarations they are copied from."""
    ledger = fx.ledger
    version_text, command_text = fx.version_text, fx.command_text
    cases = []
    cases.append(("source facts", not check_source_facts(
        ledger, version_text, command_text)))
    cases.append(("source version drift", any(
        "gateware version conflict" in item for item in check_source_facts(
            ledger, version_text.replace("0051", "0052"), command_text))))
    cases.append(("source inventory drift", any(
        "served AEM inventory conflict" in item for item in check_source_facts(
            ledger, version_text,
            command_text.replace("READ_DESCRIPTOR", "SET_NAME")))))
    cases.append(("commented source ignored", not check_source_facts(
        ledger,
        "// parameter logic [31:0] VERSION = 32'h0002_0052;\n" + version_text,
        '# SERVED = {0: dict(name="SET_NAME")}\n' + command_text)))
    return cases


def _prose_claim_cases(fx):
    """Repeated values in prose, and the ordered boot claim (#98)."""
    prose, order_block = fx.prose, fx.order_block
    row, ordered_row = fx.row, fx.ordered_row
    ledger = fx.ledger
    cases = []
    # ---- #98: repeated values in prose, and the ordered boot claim ----
    def _claims(one, two=row):
        return check_claims(ledger, {"one.md": one, "two.md": two})

    drift = ordered_row.replace("VERSION `0x0002_0051`",
                                "VERSION `0x0002_0049`")
    cases.append(("version drift", any(
        "one.md:" in item and "0x0002_0049" in item and "0x0002_0051" in item
        for item in _claims(drift))))
    cases.append(("version drift names every file", len({
        item.split(":")[0] for item in _claims(drift, drift.replace(
            "0x0002_0049", "0x0002_0050")) if "version claim" in item}) == 2))
    historic = drift.replace(
        "Status today", "<!-- milan-feature-value:gateware_version:historic "
        "-->\nStatus today")
    cases.append(("historic marker accepted", not any(
        "version claim" in item for item in _claims(historic))))
    cases.append(("historic marker still needs a live claim", any(
        "value 'gateware_version' is not stated in one.md" in item
        for item in _claims(historic))))
    stale_marker = ordered_row.replace(
        "Status today", "<!-- milan-feature-value:gateware_version:historic "
        "-->\nStatus today")
    cases.append(("historic marker on the current value", any(
        "historic marker on the CURRENT version" in item
        for item in _claims(stale_marker))))
    retired_major = ordered_row.replace("VERSION `0x0002_0051`",
                                        "VERSION `0x0001_000B`")
    cases.append(("retired major is history", not any(
        "version claim" in item for item in _claims(retired_major))))
    minor_only = ordered_row.replace("VERSION `0x0002_0051`",
                                     "VERSION `0x0049`")
    cases.append(("minor-only spelling is history", not any(
        "version claim" in item for item in _claims(minor_only))))
    cases.append(("version presence", any(
        "value 'gateware_version' is not stated in two.md" in item
        for item in _claims(ordered_row, row.replace(prose, "")))))

    count_drift = ordered_row.replace("one AEM opcode", "twenty-six AEM opcodes")
    cases.append(("count drift", any(
        "served_aem_operations count 'twenty-six'" in item and "one.md:" in item
        for item in _claims(count_drift))))
    cases.append(("numeral spelling accepted", not any(
        "count" in item for item in _claims(
            ordered_row.replace("one AEM opcode", "1 AEM opcode")))))
    cases.append(("mvu count drift", any(
        "served_mvu_operations count 'two'" in item for item in _claims(
            ordered_row.replace("one MVU command", "two MVU commands")))))
    cases.append(("count in a fence ignored", not any(
        "count" in item for item in _claims(
            ordered_row + "\n```\nnine AEM opcodes\n```\n"))))
    cases.append(("an adjective is not a count", not any(
        "count" in item for item in _claims(ordered_row.replace(
            "one AEM opcode", "served AEM opcodes")))))
    # Prose wraps, and the corpus quotes: both put a line break (and a `>`)
    # between the number and the noun. A line-at-a-time reader passed the
    # README's real claim silently, which is worse than any false positive.
    wrapped = ordered_row.replace(
        "Status today, VERSION `0x0002_0051`, serving one AEM opcode",
        "Status today, VERSION\n`0x0002_0051`, serving twenty-six AEM\nopcode")
    cases.append(("claim wrapped across lines", any(
        "count 'twenty-six'" in item for item in _claims(wrapped))))
    cases.append(("wrapped version claim still read", not any(
        "value 'gateware_version' is not stated in one.md" in item
        for item in _claims(wrapped))))
    quoted = ordered_row.replace(
        "Status today, VERSION `0x0002_0051`, serving one AEM opcode",
        "> Status today, VERSION `0x0002_0051`, serving twenty-six AEM\n"
        "> opcode")
    cases.append(("claim inside a block quote", any(
        "count 'twenty-six'" in item for item in _claims(quoted))))
    cases.append(("count in a fact block ignored", not any(
        "count" in item for item in _claims(ordered_row.replace(
            "- `READ_DESCRIPTOR`",
            "- `READ_DESCRIPTOR` — nine AEM opcodes")))))

    reversed_block = order_block.replace(
        "1. `configure_fabric()`\n2. `load_aem_image()`",
        "1. `load_aem_image()`\n2. `configure_fabric()`")
    cases.append(("documented order reversed", any(
        "feature order conflict 'firmware_boot_order'" in item and
        "load_aem_image" in item
        for item in _claims(row + reversed_block))))
    cases.append(("order block required", any(
        "feature order 'firmware_boot_order' is not marked in one.md" in item
        for item in _claims(row))))
    cases.append(("order block unregistered", any(
        "feature order 'firmware_boot_order' is not registered for two.md"
        in item for item in _claims(ordered_row, row + order_block))))
    return cases


def _boot_order_cases(fx):
    """The firmware boot order, read out of the C rather than restated."""
    ledger = fx.ledger
    version_text, command_text = fx.version_text, fx.command_text
    cases = []
    # The banner names the LAST step in call shape, before any real call: a
    # reader of the raw text sees `entity_advertise()` first and reports the
    # order reversed. Only stripping strings gets this fixture right, which is
    # what makes the clean arm below load-bearing rather than decorative.
    firmware = ("static void milan_init(void)\n{\n"
                '\tprintf("boot: entity_advertise() runs last\\n");\n'
                "\tconfigure_fabric();\n\taem = load_aem_image();\n"
                "\tentity_advertise(aem);\n}\n")
    cases.append(("boot order source tie", not check_source_facts(
        ledger, version_text, command_text, firmware_text=firmware)))
    cases.append(("boot order reversed in firmware", any(
        "firmware boot-order conflict" in item for item in check_source_facts(
            ledger, version_text, command_text, firmware_text=firmware.replace(
                "\tconfigure_fabric();\n\taem = load_aem_image();",
                "\taem = load_aem_image();\n\tconfigure_fabric();")))))
    cases.append(("boot step absent", any(
        "does not call configure_fabric()" in item
        for item in check_source_facts(
            ledger, version_text, command_text,
            firmware_text=firmware.replace("\tconfigure_fabric();\n", "")))))
    cases.append(("commented boot call ignored", any(
        "does not call configure_fabric()" in item
        for item in check_source_facts(
            ledger, version_text, command_text, firmware_text=firmware.replace(
                "\tconfigure_fabric();", "\t/* configure_fabric(); */")))))
    cases.append(("missing milan_init refused", any(
        "cannot locate milan_init()" in item for item in check_source_facts(
            ledger, version_text, command_text,
            firmware_text="static void other(void)\n{\n}\n"))))
    return cases


def _register_cases(fx):
    """The prose-claim registers a ledger may not simply omit."""
    base = fx.base
    cases = []
    no_register = json.loads(json.dumps(base))
    del no_register["value_documents"]
    _, register_findings = load_ledger_text(json.dumps(no_register), "fixture")
    cases.append(("value register required", any(
        "value_documents must be a non-empty object" in item
        for item in register_findings)))
    unknown_register = json.loads(json.dumps(base))
    unknown_register["order_documents"]["served_aem_operations"] = ["one.md"]
    _, unknown_findings2 = load_ledger_text(
        json.dumps(unknown_register), "fixture")
    cases.append(("unknown register fact", any(
        "order_documents has unknown fact" in item
        for item in unknown_findings2)))
    bad_order = json.loads(json.dumps(base))
    bad_order["facts"]["firmware_boot_order"] = ["configure_fabric"]
    _, bad_order_findings = load_ledger_text(json.dumps(bad_order), "fixture")
    cases.append(("boot order needs two steps", any(
        "firmware_boot_order must be a list" in item
        for item in bad_order_findings)))
    return cases


def run_self_test() -> list:
    """Run every fixture arm, print the transcript, and return the failures."""
    fx = _fixtures()
    cases = (_ledger_and_claim_cases(fx) + _source_fact_cases(fx)
             + _prose_claim_cases(fx) + _boot_order_cases(fx)
             + _register_cases(fx))
    for name, passed in cases:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
    failed = [name for name, passed in cases if not passed]
    print(f"feature_status self-test: {len(cases) - len(failed)}/{len(cases)} passed")
    return failed
