#!/usr/bin/env python3
"""One markdown table of every reviewer case: base 759da623, reviewed head
a13b6e2e and this head, each with the pinned SDK and with no compiler.
A refusal is shown with the rule that answered, shortened."""

import json
import sys
from pathlib import Path

PROBES = Path(sys.argv[1])
RULES = (
    ("under the arm selection", "selection: "),
    ("the firmware's casts to a pointer are pinned", "cast set"),
    ("the firmware's stores through a pointer are pinned", "store set"),
    ("the firmware's inline asm is pinned", "asm set"),
    ("firmware must not select boot code with the preprocessor", "reach ban"),
    ("firmware must not splice physical source lines", "splice ban"),
    ("firmware must not paste tokens", "## ban"),
    ("a backslash-newline JOINS two tokens inside", "six-body splice ban"),
    ("a `##` paste reaches", "six-body ## ban"),
    ("is #defined more than once", "one definition"),
    ("a literal that no quote closes on its line", "open literal"),
    ("a raw string literal", "raw literal"),
    ("carries a trigraph", "trigraph"),
    ("hides milan_read() inside a macro body", "macro-body rule"),
    ("materialises one elsewhere", "census"),
    ("STORES into the Milan CSR window", "resolver store"),
    ("not from entity_advertise()", "resolver choke"),
    ("is not the boot path the compiler COMPILES", "-E comparison"),
    ("transfers control through a register", "resolver entrance"),
    ("enters entity_advertise()", "resolver entrance"),
    ("stores through milan_reg()'s return", "resolver helper"),
    ("verdict argument against zero", "resolver verdict test"),
    ("must be cleared before the AEM image", "pre-AEM clear rule"),
    ("AEM verifier non-zero return must be textually after", "verifier return rule"),
    ("may be set only inside the entity-advertise choke point", "choke-point rule"),
    ("must test the verdict it is handed", "verdict-test rule"),
    ("a pinned include resolved to a file", "-H resolution"),
    ("the firmware's directory is pinned", "directory pin"),
    ("could not build the", "census compile"),
)


def rule(reason: str) -> str:
    """The rules a refusal names, outermost first."""
    found = []
    for needle, name in RULES:
        at = reason.find(needle)
        if at >= 0:
            found.append((at, name))
    names = [name for _at, name in sorted(found)]
    if not names:
        return reason[:60]
    return (names[0] + " + ".join(names[1:])) if names[0].endswith(": ") \
        else " + ".join(names)


def load(name: str) -> dict:
    return {r["label"]: r for r in
            json.loads((PROBES / name).read_text())["results"]}


def main() -> None:
    for kind in ("hostile", "accepted"):
        cols = [(f"{rev} {mode}", load(f"{rev}-{kind}-{mode}.json"))
                for rev in ("base", "a13b", "head")
                for mode in ("sdk", "absent")]
        print(f"\n### {kind}\n")
        print("| Case | " + " | ".join(name for name, _ in cols) + " |")
        print("|---|" + "---|" * len(cols))
        for label in cols[0][1]:
            cells = []
            for _name, rows in cols:
                row = rows[label]
                cells.append("ACCEPTED" if row["verdict"] == "ACCEPTED"
                             else "REFUSED (" + rule(row["reason"]) + ")")
            print(f"| {label} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
