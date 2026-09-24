#!/usr/bin/env python3
"""Every READER-LEVEL spelling a review of PR #535 probed, rounds one to
four, read at a head (#408, round four): what S does with it (refused, and
by which pin, or admitted) and, where S admits it, whether gate 1b's
directive readers (`lexer_keeps`, the reader the lexer corpora measure) keep
the `int` names the pinned GCC keeps at -std=gnu99 -E.

The spellings are taken from the reviewers' own files on the review-evidence
branch, unchanged: their `.c` inputs, and the spelling tables inside their
probe scripts (read as literals, or imported where a script builds its table).

usage: reader_probes.py <lane> <riscv32-linux-gcc> <reviews-dir> <out.jsonl>
       [patch.json ...]
"""
import ast
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_extract  # noqa: E402
import record_closure  # noqa: E402


def literal(path, name):
    """The literal assigned to `name` at module level in `path`."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(f"{name} in {path}")


def spellings(reviews):
    out = []
    for path in sorted((reviews / "R272-1/receipts/cpp").glob("*.c")):
        out.append(("R272-1", f"cpp/{path.name}", path.read_bytes()))
    for label, text in literal(reviews / "R272-2/scripts/gcc_spellings.py",
                               "cases").items():
        out.append(("R272-2", label, text.encode("utf-8")))
    out.append(("R272-3", "dollar_skipped.c",
                (reviews / "R272-3/probes/dollar_skipped.c").read_bytes()))
    for name in ("mid", "comb", "sup2", "eacute"):
        out.append(("R272-4", f"{name}.c", (
            reviews / f"R272-4/receipts/probes/{name}.c").read_bytes()))
    for path in sorted((reviews / "R273-2/receipts/cases").glob("S*.c")):
        out.append(("R273-2", path.name, path.read_bytes()))
    for case in json.loads((reviews / "R273-2/receipts/cases/spellings.json")
                           .read_text(encoding="utf-8")):
        out.append(("R273-2", case["label"], case["text"].encode("utf-8")))
    for label, text in literal(reviews / "R273-3/probes/lexer_probe.py",
                               "EXTRA"):
        out.append(("R273-3", label, text.encode("utf-8")))
    for label, text in literal(reviews / "R273-4/probes/lexer_oracle.py",
                               "EXTRA"):
        out.append(("R273-4", label, text.encode("utf-8")))
    for path in sorted((reviews / "R273-4/receipts/hi-spellings").glob("*.c")):
        out.append(("R273-4", f"hi-spellings/{path.name}", path.read_bytes()))
    probes = reviews / "R273-5/probes"
    sys.path.insert(0, str(probes))
    spec = importlib.util.spec_from_file_location(
        "r273_5_subset_probe", probes / "subset_probe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for label, text in module.SPELLINGS:
        out.append(("R273-5", label, text.encode("utf-8")))
    for case in json.loads((reviews / "R273-5/cases/r2-spellings.json")
                           .read_text(encoding="utf-8")):
        out.append(("R273-5", "r2 " + case["label"],
                    case["text"].encode("utf-8")))
    for name in ("ident.c", "nest.c"):
        out.append(("R273-5", name,
                    (reviews / f"R273-5/receipts/{name}").read_bytes()))
    return out


def main():
    lane, gcc, reviews, out = (Path(sys.argv[1]), sys.argv[2],
                               Path(sys.argv[3]), Path(sys.argv[4]))
    source = (lane / "sw/builder/test_builder.py").read_text(encoding="utf-8")
    for patch in sys.argv[5:]:
        for old, new in json.loads(Path(patch).read_text(encoding="utf-8")):
            assert source.count(old) == 1, f"{patch}: {old[:60]!r}"
            source = source.replace(old, new, 1)
    ns, missing = gate_extract.load(lane, source)
    assert not missing, missing
    pins = {value: name for name, value in ns.items()
            if name.endswith("_PIN") and isinstance(value, str)}
    cases = spellings(reviews)
    texts = [raw.decode("utf-8", errors="surrogateescape")
             for _r, _l, raw in cases]
    record_closure.GCC = gcc
    found = record_closure.measure(texts)
    rows, tally = [], {}
    for (review, label, _raw), text, kept in zip(cases, texts, found):
        try:
            ns["assert_within_lexical_subset"](text)
            pin = ""
        except AssertionError as exc:
            pin = next((name for value, name in pins.items()
                        if value in str(exc)), "UNPINNED")
        read = ns["lexer_keeps"](text)
        outcome = f"REFUSED {pin}" if pin else (
            "AGREE" if read == kept else "DISAGREE")
        tally[outcome.split()[0]] = tally.get(outcome.split()[0], 0) + 1
        rows.append({"review": review, "label": label, "S": pin or "admitted",
                     "readers": read, "gcc": kept, "outcome": outcome})
        print(f"{outcome:32} {review:7} {label}")
    out.write_text("".join(json.dumps(row, ensure_ascii=True) + "\n"
                           for row in rows), encoding="utf-8")
    print(f"{len(rows)} spellings: {tally}")
    return 1 if tally.get("DISAGREE") else 0


if __name__ == "__main__":
    sys.exit(main())
