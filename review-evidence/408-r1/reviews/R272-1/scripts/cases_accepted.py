"""R272-1 accepted-case cross-check.

At HEAD (the gate defines `retired_rule_cases`): write every retired-rule
accepted case to DUMP and grade each through assert_boot_contract(), plus the
directory case (README and notes.txt planted beside a copy of the firmware).
At BASE (no such table): read DUMP and grade the same texts, the directory
case as base's own listing argument (the whole directory listing).

Each case carries the BASE sentence of the rule the page says it retires, so
the base run reports whether the refusal is on that rule's own sentence."""
import json
import os
from pathlib import Path

DUMP = Path(os.environ.get(
    "R272_ACCEPTED_DUMP",
    "$REVIEWS/408-r272-1-packet/scratch/retired_rule_cases.json"))

BASE_SENTENCE = {
    "an #ifdef around a debug printf INSIDE milan_init()":
        "a conditional group reaching",
    "a benign statement in an arm the census tree drops, inside "
    "configure_fabric()": "a conditional group reaching",
    "an #ifdef/#else choosing a #define, read in a UART command handler":
        "a conditional group carrying #define",
    "a ## token paste building a call outside the boot path":
        "firmware must not paste tokens",
    "a token-joining backslash-newline inside a macro body":
        "firmware must not splice physical source lines with backslash-newline",
    "a read-only #define accessor over milan_read()":
        "hides milan_read() inside a macro body",
    "a fifth cast to a pointer, resolving outside the window":
        "the firmware's casts to a pointer are pinned",
    "a fifth store through a pointer, resolving outside the window":
        "the firmware's stores through a pointer are pinned",
    "parse_u64() and seconds_to_ns() exchanged, with nothing added or "
    "removed": "the firmware's stores through a pointer are pinned",
    "a fifth inline-asm statement, a fence in a UART command handler":
        "the firmware's inline asm is pinned",
}
DIRECTORY = "a README and a notes.txt beside the firmware"


def cases(ns):
    at_head = "retired_rule_cases" in ns
    if at_head:
        table = dict(ns["retired_rule_cases"])
        assert sorted(table) == sorted(BASE_SENTENCE), sorted(table)
        DUMP.write_text(json.dumps(table), encoding="utf-8")
    else:
        table = json.loads(DUMP.read_text(encoding="utf-8"))
    for label, firmware in table.items():
        case = {"label": label, "firmware": firmware}
        if not at_head:
            case["because"] = BASE_SENTENCE[label]
        yield case
    listing = ("README", "notes.txt") if at_head else tuple(sorted(
        ("Makefile", "milan_baremetal.c", "README", "notes.txt")))
    case = {"label": DIRECTORY, "firmware": ns["firmware_source"],
            "listing": listing}
    if not at_head:
        case["because"] = "the firmware's directory is pinned to"
    yield case
