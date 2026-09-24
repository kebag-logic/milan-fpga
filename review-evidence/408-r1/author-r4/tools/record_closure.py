#!/usr/bin/env python3
"""Record `_CLOSURE_KEPT` for gate 1b's character-closure table (#408, PR #535
round four): what the pinned GCC 14.3 keeps of every `_closure_corpus()` cell
at -std=gnu99 -E, one `_LEXER_OUTCOMES` letter per cell, measured exactly as
the gate's lexer_measured() measures (64 files an invocation, GCC's own line
markers, a refusal by the diagnostic naming the file, ASCII-mode readers).

usage: record_closure.py <lane> <riscv32-linux-gcc> [--write]
With --write the recorded string replaces `_CLOSURE_KEPT` in the lane's
sw/builder/test_builder.py; without it the string is only printed.
"""
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LANE, GCC = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(LANE / "sw/builder"))
import test_builder as tb  # noqa: E402

LINE_MARKER = re.compile(r'^#\s+\d+\s+"([^"]*)"', re.ASCII)


def measure(texts):
    with tempfile.TemporaryDirectory(prefix="a254-closure-") as tmp:
        files = []
        for index, text in enumerate(texts):
            files.append(Path(tmp) / f"lex{index:05d}.c")
            files[-1].write_bytes(text.encode("utf-8", errors="surrogateescape"))
        batches = [files[at:at + 64] for at in range(0, len(files), 64)]
        with ThreadPoolExecutor(8) as pool:
            builds = list(pool.map(lambda batch: subprocess.run(
                [GCC, "-std=gnu99", "-E", *map(str, batch)],
                capture_output=True), batches))
    lines, refused = {}, set()
    for build in builds:
        named = set(re.findall(
            r"(?m)(lex\d{5}\.c):\d+(?::\d+)?: (?:fatal )?error:",
            build.stderr.decode("utf-8", errors="replace")))
        assert named or not build.returncode, build.stderr.decode()[:2000]
        refused |= named
        name = None
        for line in build.stdout.decode("utf-8", errors="replace").split("\n"):
            marker = LINE_MARKER.match(line)
            if marker:
                name = Path(marker.group(1)).name
                continue
            lines.setdefault(name, []).append(line)
    return [None if file.name in refused else tuple(re.findall(
        r"\bint\s+(\w+)\s*;", "\n".join(lines.get(file.name, [])), re.ASCII))
        for file in files]


def main():
    cells = tb._closure_corpus()
    kept = measure([text for _label, text, _reader, _outside in cells])
    letter_of = {outcome: letter for letter, outcome in tb._LEXER_OUTCOMES.items()}
    letters = []
    for (label, _text, _reader, _outside), found in zip(cells, kept):
        if found not in letter_of:
            sys.exit(f"UNMAPPED outcome {found!r} for {label}")
        letters.append(letter_of[found])
    record = "".join(letters)
    body = "\n".join(f'    "{record[at:at + 66]}"'
                     for at in range(0, len(record), 66))
    literal = f"_CLOSURE_KEPT = (\n{body}\n)"
    print(f"{len(cells)} cells recorded on {GCC}")
    if "--write" in sys.argv:
        path = LANE / "sw/builder/test_builder.py"
        source = path.read_text(encoding="utf-8")
        found = re.search(r'(?ms)^_CLOSURE_KEPT = (?:""|\(\n.*?\n\))$', source)
        assert found, "no _CLOSURE_KEPT assignment to replace"
        path.write_text(source[:found.start()] + literal + source[found.end():],
                        encoding="utf-8")
        print(f"wrote {path}")
    else:
        print(literal)


if __name__ == "__main__":
    main()
