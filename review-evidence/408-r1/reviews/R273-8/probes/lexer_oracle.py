#!/usr/bin/env python3
"""Independent oracle for gate 1b's lexer corpora (R273-4).

Loads the gate's own phase code and readers unmodified (lexer_extract_head),
rebuilds the fixed and the GENERATED corpus, and asks the pinned GCC about
every spelling as ONE file per invocation (the gate batches 64 per
invocation; this does not). Each entry is compared three ways: recorded,
gate readers, GCC. Then the EXTRA spellings below, which neither corpus
holds, are read by the gate's `_c_phases()` view and by GCC.

usage: lexer_oracle.py <repo-root> <riscv32-linux-gcc> <out.jsonl>
"""
import concurrent.futures
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lexer_extract_head  # noqa: E402

#: spellings outside both corpora: does the gate's phase-3 view keep the
#: `int` lines GCC keeps? (lexer_keeps() reads only #ifdef-style conditions,
#: so an `#if` expression is compared on the view: the `int` names left in
#: it after the directive lines, against GCC's.)
EXTRA = (
    ("__has_include with an angled header name holding /* (if !)",
     "int a;\n#if !__has_include(<x/*y>)\nint b; // */\n#endif\nint z;\n"),
    ("__has_include with an angled header name holding /* (else)",
     "int a;\n#if __has_include(<x/*y>)\n#else\nint b; // */\n#endif\n"
     "int z;\n"),
    ("__has_include with a quoted header name holding /* (control)",
     "int a;\n#if !__has_include(\"x/*y\")\nint b; // */\n#endif\nint z;\n"),
    ("__has_include with an angled header name holding // (control)",
     "int a;\n#if !__has_include(<x//y>)\nint b;\n#endif\nint z;\n"),
)


def gcc_ints(gcc, text):
    with tempfile.TemporaryDirectory(prefix="r273-oracle-") as tmp:
        src = Path(tmp) / "t.c"
        src.write_bytes(text.encode("utf-8"))
        run = subprocess.run([gcc, "-std=gnu99", "-E", str(src)],
                             capture_output=True)
    if run.returncode:
        return None
    keep, out = False, []
    for line in run.stdout.decode("utf-8", "replace").split("\n"):
        marker = re.match(r'^#\s+\d+\s+"([^"]*)"', line)
        if marker:
            keep = Path(marker.group(1)).name == "t.c"
            continue
        if keep:
            out.append(line)
    return tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(out)))


def main():
    root, gcc, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    ns, missing = lexer_extract_head.load(root)
    generated = ns["_lexer_generated_corpus"]()
    record = ns["_LEXER_GENERATED_KEPT"]
    outcomes = ns["_LEXER_OUTCOMES"]
    assert len(generated) == len(record), (len(generated), len(record))
    rows = [("fixed", label, text, None if kept is None else tuple(kept),
             "keeps") for label, text, kept in ns["lexer_corpus"]]
    rows += [("generated", label, text, outcomes[letter], reader)
             for (label, text, reader), letter in zip(generated, record)]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        measured = list(pool.map(lambda r: gcc_ints(gcc, r[2]), rows))
    bad = {"record_vs_gcc": 0, "gate_vs_record": 0}
    with out.open("w") as stream:
        if missing:
            stream.write(json.dumps({"missing": sorted(missing)}) + "\n")
        for (kind, label, text, kept, reader), found in zip(rows, measured):
            gate = ns["lexer_readers"][reader](text)
            bad["record_vs_gcc"] += found != kept
            bad["gate_vs_record"] += gate != kept
            if found != kept or gate != kept:
                stream.write(json.dumps({"set": kind, "label": label,
                                         "text": text, "recorded": kept,
                                         "gcc": found, "gate": gate}) + "\n")
        extra_bad = 0
        for label, text in EXTRA:
            view = ns["_c_phases"](text).view
            lines = [line for line in view.split("\n")
                     if not re.match(r"[ \t]*#", line)]
            gate = tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(lines)))
            found = gcc_ints(gcc, text)
            # the gate keeps a superset of what any one arm keeps: a name
            # GCC keeps and the view has LOST is a line hidden from the gate
            lost = [n for n in (found or ()) if n not in gate]
            extra_bad += bool(lost)
            stream.write(json.dumps({"set": "extra", "label": label,
                                     "text": text, "view": view,
                                     "gcc_keeps": found,
                                     "view_keeps": gate,
                                     "lost_from_view": lost}) + "\n")
        summary = {"fixed": len(ns["lexer_corpus"]),
                   "generated": len(generated), **bad,
                   "extra": len(EXTRA), "extra_lost": extra_bad}
        stream.write(json.dumps({"summary": summary}) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
