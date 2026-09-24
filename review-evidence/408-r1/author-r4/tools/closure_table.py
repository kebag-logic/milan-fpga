#!/usr/bin/env python3
"""Tabulate gate 1b's character-closure table cell by cell (#408, PR #535
round four): for every `_closure_corpus()` cell, what S does (the allowlist,
another rule of S by its pin, or admitted), what the readers keep, what the
pinned GCC keeps (measured now, not read from the record), and the outcome:

  A  refused by the character allowlist (the cell is outside it)
  a  as A, and the readers would have read it differently from GCC
  S  refused by another rule of S (the pin is listed below the table)
  =  admitted, and the readers keep what GCC keeps
  X  admitted, and the readers and GCC disagree  (a hole)
  !  the allowlist refused a cell inside it, left a cell outside it to
     another rule, or admitted a cell outside it the readers happen to read
     as GCC does  (a rule violation, not a hole)

usage: closure_table.py <lane> <riscv32-linux-gcc> <out-dir> [patch.json]
A patch (a JSON list of [old, new], each old occurring once) is applied to
the gate source in memory first: that is how a disconnect is tabulated.
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_extract  # noqa: E402
import record_closure  # noqa: E402  (its measure() is the gate's)


def main():
    lane, out = Path(sys.argv[1]), Path(sys.argv[3])
    source = (lane / "sw/builder/test_builder.py").read_text(encoding="utf-8")
    for patch in sys.argv[4:]:
        for old, new in json.loads(Path(patch).read_text(encoding="utf-8")):
            assert source.count(old) == 1, f"{patch}: {old[:60]!r}"
            source = source.replace(old, new, 1)
    ns, missing = gate_extract.load(lane, source)
    assert not missing, missing
    pins = {value: name for name, value in ns.items()
            if name.endswith("_PIN") and isinstance(value, str)}
    cells = ns["_closure_corpus"]()
    gcc = record_closure.measure([text for _l, text, _r, _o in cells])
    readers = ns["lexer_readers"]
    rows, counts, other = [], Counter(), Counter()
    for (label, text, reader, outside), found in zip(cells, gcc):
        read = readers[reader](text)
        try:
            ns["assert_within_lexical_subset"](text)
            verdict, pin = "admitted", ""
        except AssertionError as exc:
            pin = next((name for value, name in pins.items()
                        if value in str(exc)), "UNPINNED")
            verdict = "refused"
        allowlist = pin == "SUBSET_CHARACTER_PIN"
        if verdict == "refused" and allowlist != outside:
            code = "!"
        elif verdict == "admitted" and outside:
            code = "X" if read != found else "!"
        elif allowlist:
            code = "a" if read != found else "A"
        elif verdict == "refused":
            code = "S"
            other[pin] += 1
        else:
            code = "=" if read == found else "X"
        counts[code] += 1
        rows.append({"label": label, "text": text.encode(
            "utf-8", errors="surrogateescape").hex(), "outside": outside,
            "S": verdict, "pin": pin, "readers": read, "gcc": found,
            "code": code})
    out.mkdir(parents=True, exist_ok=True)
    (out / "closure-cells.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    positions = [where for where, *_rest in ns["_CLOSURE_POSITIONS"]]
    spelled = len(cells) // len(positions)
    grid = ["| sequence | " + " | ".join(
        f"P{index + 1}" for index in range(len(positions))) + " |",
        "|---|" + "---|" * len(positions)]
    for at in range(spelled):
        name = rows[at]["label"][:-len(" " + positions[0])]
        grid.append(f"| {name} | " + " | ".join(
            rows[p * spelled + at]["code"] for p in range(len(positions)))
            + " |")
    legend = "\n".join(f"- P{index + 1}: {where}"
                       for index, where in enumerate(positions))
    summary = (f"{len(cells)} cells ({spelled} sequences x {len(positions)} "
               f"positions): " + ", ".join(f"{code} {counts[code]}"
                                           for code in "AaS=X!") +
               "; other rules of S: " + ", ".join(
                   f"{pin} {n}" for pin, n in sorted(other.items())))
    (out / "closure-table.md").write_text(
        f"# Character-closure table\n\n{summary}\n\n{legend}\n\n" +
        "\n".join(grid) + "\n", encoding="utf-8")
    print(summary)
    bad = [row for row in rows if row["code"] in "X!"]
    for row in bad[:40]:
        print("  ", row["code"], row["label"], row["pin"], row["readers"],
              row["gcc"])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
