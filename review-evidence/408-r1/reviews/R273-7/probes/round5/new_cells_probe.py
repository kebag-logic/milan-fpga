#!/usr/bin/env python3
"""R273-7: can the fourteen round-five closure positions fail, and do they
catch what the nine round-four positions and the two lexer corpora miss?

For the intact head and for each in-memory MUTATION of the gate's phase code
(count-checked string patches of sw/builder/test_builder.py, written to a
disposable copy under <work>; the lane is never edited), the gate's own code
is loaded unmodified otherwise (r6_extract) and three of its own checks run:

  corpora  assert_lexer_matches_compiler()  (fixed + generated corpus)
  full     assert_character_closure() on all 23 positions
  nine     assert_character_closure() with the table cut to the first nine
           positions (and their recorded letters; the lone-# named refusal
           then has no cell, so the name list is emptied for that run)

The RV32 re-measure is stubbed off (census_used = {}): this probe asks
whether the READERS still agree with the recorded GCC letters, which is
what the table checks on every machine. Every closure cell the mutation
makes the readers misread (admitted by S, not named as refused, reader !=
recorded) is listed by position.
usage: new_cells_probe.py <repo-root> <work-dir> <out.json>"""
import json, shutil, sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lexer_extract_head as base  # noqa: E402
import r6_extract  # noqa: E402

MUTATIONS = {
    # a splice's blank run widened by U+00A0 (the author's control, redone)
    "splice-blank+U+00A0": [(
        '_C_PHASE12_RE = re.compile(r"\\\\[ \\t\\f\\v\\0]*(?:\\r\\n|\\r|\\n)|\\r\\n?")',
        '_C_PHASE12_RE = re.compile(r"\\\\[ \\t\\f\\v\\0\\u00a0]*(?:\\r\\n|\\r|\\n)|\\r\\n?")')],
    # C23 digit separators: a quote right after a digit opens no literal
    "digit-separator-quote": [(
        "        elif char in \"\\\"'\":\n            stop, closed = _c_literal_end(raw, i + 1, char)\n",
        "        elif char == \"'\" and i and raw[i - 1].isdigit():\n            i += 1\n            continue\n"
        "        elif char in \"\\\"'\":\n            stop, closed = _c_literal_end(raw, i + 1, char)\n")],
    # a tolerant block-comment closer: `*`, blanks, `/` closes it
    "closer-tolerates-blanks": [(
        '            stop = raw.find("\\n" if raw[i + 1] == "/" else "*/", i + 2)\n',
        '            _m = re.compile(r"\\*[ \\t]*/").search(raw, i + 2)\n'
        '            stop = raw.find("\\n", i + 2) if raw[i + 1] == "/" else (_m.end() - 2 if _m else -1)\n')],
    # a backslash that no longer escapes a double quote in a literal
    "escape-skips-quote": [(
        '        at += 2 if raw[at] == "\\\\" and raw[at + 1:at + 2] not in ("", "\\n") \\\n',
        '        at += 2 if raw[at] == "\\\\" and raw[at + 1:at + 2] not in ("", "\\n", "\\"") \\\n')],
    # a NUL no longer a splice blank
    "splice-blank-NUL": [(
        '_C_PHASE12_RE = re.compile(r"\\\\[ \\t\\f\\v\\0]*(?:\\r\\n|\\r|\\n)|\\r\\n?")',
        '_C_PHASE12_RE = re.compile(r"\\\\[ \\t\\f\\v]*(?:\\r\\n|\\r|\\n)|\\r\\n?")')],
}
EXTRA = {"assert_character_closure", "assert_lexer_matches_compiler",
         "assert_lexer_reads", "lexer_measured", "LEXER_PIN",
         "SUBSET_CHARACTER_PIN", "assert_directive_set_is_closed",
         "line_marker_re", "lexer_names", "c_identifier_re"}


def load(root):
    saved = set(base.NESTED)
    base.NESTED |= EXTRA
    try:
        ns, missing = r6_extract.load(root)
    finally:
        base.NESTED.clear(); base.NESTED |= saved
    ns["census_compiler"] = lambda: None
    ns["census_used"] = {}
    return ns


def run(fn):
    try:
        return {"ok": True, "said": str(fn())[:400]}
    except AssertionError as exc:
        return {"ok": False, "said": str(exc)[:600]}
    except Exception:
        return {"ok": False, "said": "ERROR " + traceback.format_exc()[-800:]}


def misreads(ns):
    """Every cell the readers misread (S admits it, not a named refusal)."""
    out = {}
    for (label, text, reader, _o), letter in zip(ns["_closure_corpus"](), ns["_CLOSURE_KEPT"]):
        try:
            ns["assert_within_lexical_subset"](text)
        except AssertionError:
            continue
        if label in ns["_CLOSURE_READERS_REFUSE"]:
            continue
        if ns["lexer_readers"][reader](text) != ns["_LEXER_OUTCOMES"][letter]:
            where = label.split(" ", 2)[2] if label.startswith("byte ") else label.split(" ", 1)[1]
            out.setdefault(where, []).append(label.split(" ")[0] + " " + label.split(" ")[1])
    return out


def main():
    root, work, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    source = (root / "sw/builder/test_builder.py").read_text(encoding="utf-8")
    results = {}
    for name, patches in [("intact", [])] + list(MUTATIONS.items()):
        text = source
        for old, new in patches:
            assert text.count(old) == 1, (name, old, text.count(old))
            text = text.replace(old, new)
        copy = work / name
        (copy / "sw/builder").mkdir(parents=True, exist_ok=True)
        (copy / "sw/builder/test_builder.py").write_text(text, encoding="utf-8")
        ns = load(copy)
        row = {"corpora": run(ns["assert_lexer_matches_compiler"]),
               "full": run(ns["assert_character_closure"])}
        row["misread_full"] = misreads(ns)
        positions, kept, named = ns["_CLOSURE_POSITIONS"], ns["_CLOSURE_KEPT"], ns["_CLOSURE_READERS_REFUSE"]
        per = len(kept) // len(positions)
        ns["_CLOSURE_POSITIONS"], ns["_CLOSURE_KEPT"], ns["_CLOSURE_READERS_REFUSE"] = positions[:9], kept[:9 * per], ()
        row["nine"] = run(ns["assert_character_closure"])
        row["misread_nine"] = misreads(ns)
        ns["_CLOSURE_POSITIONS"], ns["_CLOSURE_KEPT"], ns["_CLOSURE_READERS_REFUSE"] = positions, kept, named
        results[name] = row
        print(f"{name:26} corpora={'PASS' if row['corpora']['ok'] else 'FAIL'} "
              f"nine={'PASS' if row['nine']['ok'] else 'FAIL'} "
              f"full={'PASS' if row['full']['ok'] else 'FAIL'}  "
              f"misread positions (full): { {k: len(v) for k, v in row['misread_full'].items()} }")
        for key in ("corpora", "nine", "full"):
            if not row[key]["ok"]:
                print(f"    {key}: {row[key]['said'][:260]}")
    out.write_text(json.dumps(results, indent=1, ensure_ascii=False))


main()
