#!/usr/bin/env python3
"""R272-6: which of gate 1b's lexical proofs a lexer mutation trips.

The gate source at <tree>/sw/builder/test_builder.py is executed IN MEMORY,
after optional count-checked --patch replacements (JSON list of [old, new]),
with a hook inserted immediately before `subset_note =
assert_subset_refuses()`. At the hook, in the gate's own namespace, and
without asking any compiler (the recorded GCC answers are the oracle; the
SDK run of the unpatched head re-measures them), it reports:

  * subset: whether assert_subset_refuses() still passes;
  * lexer: how many of the fixed + generated lexer corpus spellings the
    readers read differently from the recorded GCC answer;
  * closure: per closure-table position, cells where S's allowlist verdict
    disagrees with the cell's `outside` flag, admitted cells (not named in
    _CLOSURE_READERS_REFUSE) the readers read differently from the recorded
    GCC answer, and named cells the readers no longer refuse; split into the
    first nine positions (round four) and the rest (round five).

Every cross compiler is hidden, as in test_firmware_compiler.py --absent.
No file in <tree> is written.

Usage: mutation_power.py --tree <repo> --out <json> [--patch <json> ...]
"""
import argparse
import json
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from unittest.mock import patch

ANCHOR = "    subset_note = assert_subset_refuses()\n"
HOOK = ("    if _R272_HOOK is not None:\n"
        "        return _R272_HOOK(locals())\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--patch", type=Path, action="append", default=[])
    args = parser.parse_args()
    tree = args.tree.resolve()
    builder_path = tree / "sw/builder/test_builder.py"
    source = builder_path.read_text(encoding="utf-8")
    for patch_file in args.patch:
        for old, new in json.loads(patch_file.read_text(encoding="utf-8")):
            assert source.count(old) == 1, \
                f"{patch_file}: anchor occurs {source.count(old)} times: {old!r}"
            source = source.replace(old, new, 1)
    assert source.count(ANCHOR) == 1
    source = source.replace(ANCHOR, HOOK + ANCHOR, 1)
    sys.path.insert(0, str(tree / "scripts"))
    sys.path.insert(0, str(tree / "sw/builder"))
    result = {"patches": [str(p) for p in args.patch]}

    def hook(ns):
        mod = sys.modules["test_builder"]
        try:
            ns["assert_subset_refuses"]()
            result["subset"] = "pass"
        except AssertionError as exc:
            result["subset"] = "FAIL: " + str(exc)[:300]
        readers = ns["lexer_readers"]
        spellings = [(label, text, kept, "keeps")
                     for label, text, kept in ns["lexer_corpus"]] + [
            (label, text, mod._LEXER_OUTCOMES[letter], reader)
            for (label, text, reader), letter in
            zip(mod._lexer_generated_corpus(), mod._LEXER_GENERATED_KEPT)]
        lex_bad = []
        for label, text, kept, reader in spellings:
            try:
                read = readers[reader](text)
            except Exception as exc:  # recorded, not hidden
                read = ("EXC", type(exc).__name__)
            if read != kept:
                lex_bad.append(label)
        result["lexer"] = {"spellings": len(spellings),
                           "mismatch": len(lex_bad), "first": lex_bad[:5]}
        cells = mod._closure_corpus()
        per = len(cells) // len(mod._CLOSURE_POSITIONS)
        pos = {}
        for index, ((label, text, reader, outside), letter) in enumerate(
                zip(cells, mod._CLOSURE_KEPT)):
            where = mod._CLOSURE_POSITIONS[index // per][0]
            row = pos.setdefault(where, {"index": index // per,
                                         "allowlist_flag_wrong": 0,
                                         "admitted_disagree": 0,
                                         "named_not_refused": 0,
                                         "examples": []})
            kept = mod._LEXER_OUTCOMES[letter]
            try:
                ns["assert_within_lexical_subset"](text)
                verdict = "admitted"
            except AssertionError as exc:
                verdict = "allowlist" if ns["SUBSET_CHARACTER_PIN"] in \
                    str(exc) else "other"
            if (verdict == "allowlist") != outside:
                row["allowlist_flag_wrong"] += 1
            if verdict != "admitted":
                continue
            try:
                read = readers[reader](text)
            except Exception as exc:
                read = ("EXC", type(exc).__name__)
            if label in mod._CLOSURE_READERS_REFUSE:
                if read is not None:
                    row["named_not_refused"] += 1
                continue
            if read != kept:
                row["admitted_disagree"] += 1
                if len(row["examples"]) < 3:
                    row["examples"].append([label, list(read or ()) if
                                            read is not None else None,
                                            kept])
        result["closure"] = pos

        def total(first, last):
            return sum(r["allowlist_flag_wrong"] + r["admitted_disagree"] +
                       r["named_not_refused"] for r in pos.values()
                       if first <= r["index"] < last)
        result["summary"] = {
            "subset_trips": result["subset"] != "pass",
            "lexer_corpora_trip": len(lex_bad),
            "round4_positions_trip": total(0, 9),
            "round5_positions_trip": total(9, 10 ** 6)}
        return None

    module = types.ModuleType("test_builder")
    module.__file__ = str(builder_path)
    module._R272_HOOK = hook
    sys.modules["test_builder"] = module
    exec(compile(source, str(builder_path), "exec"), module.__dict__)
    import test_firmware_compiler as tfc
    with tempfile.TemporaryDirectory(prefix="r272-6-power-") as tmp:
        with (Path(tmp) / "audit.jsonl").open("w") as stream:
            audit = tfc.CompilerAudit(stream, None)
            with patch.object(subprocess, "run", side_effect=audit.invoke), \
                    patch.object(sys, "argv", [str(builder_path)]), \
                    patch.object(module, "OUT", Path(tmp)), \
                    patch.object(module, "SKIPPED", []):
                module.test_baremetal_profile_contract()
    args.out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
