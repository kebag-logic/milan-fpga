"""R272-6: a seeded differential fuzz WITHIN S, run inside gate 1b's own
namespace by scripts/r1/probe_gate1b.py (anchor: accepted). Grades no
firmware; returns no cases.

Each sample is

    int a;\\n J1 \\n#define FOO\\n J2 \\n L1 #ifdef FOO\\nint b;\\n L2 #endif\\nint z;\\n

with J1 and J2 random runs of 0 to 7 fragments from comment, literal,
splice, line-end, blank and code pieces (no `#`, `%`, `?` or `$`, so no
directive, digraph, trigraph or `$` is spelled by the junk itself), and L1,
L2 random line leads (blanks, controls, comments, splices). Every sample is
put to assert_within_lexical_subset(); each one S admits is read by the
gate's `keeps` reader and by the pinned GCC (one `-std=gnu99 -E -P` per
file, R272_GCC). Any admitted sample where the two differ is reported.

Environment: R272_GCC, R272_OUT, R272_FUZZ_N (default 30000),
R272_FUZZ_SEED (default 272006).
"""
import concurrent.futures
import json
import os
import random
import re
import subprocess
import tempfile
from pathlib import Path

INT_RE = re.compile(r"\bint\s+(\w+)\s*;", re.ASCII)
FRAGMENTS = ("/*", "*/", "//", "\"", "'", "\\", "\\\n", "\\ \n", "\\\t\n",
             "\\\r\n", "\\\r", "\n", "\r", "\r\n", " ", "\t", "\f", "\v", "\0",
             "x", "1", "R", "u8", "L", "u", "U", "<", ">", "*", "/", "=", ";",
             ".", "e+", "0x", "a'b", "\"x\"", "'c'", "/**/", "é",
             " ", " ", "\\ \n", "\\\f\n", "\\\v\n", "\\\0\n")
LEADS = ("", "", " ", "\t", "\f", "\v", "\0", "/**/", "/* x */", "\\\n",
         "/*\n*/", " \\\n ", "\f\v")


def sample(rng):
    def run():
        return "".join(rng.choice(FRAGMENTS)
                       for _ in range(rng.randint(0, 7)))
    return ("int a;\n" + run() + "\n#define FOO\n" + run() + "\n" +
            rng.choice(LEADS) + "#ifdef FOO\nint b;\n" + rng.choice(LEADS) +
            "#endif\nint z;\n")


def gcc_keeps(gcc, texts):
    def one(item):
        index, text = item
        with tempfile.TemporaryDirectory(prefix="r272-6-fz-") as tmp:
            path = Path(tmp) / f"f{index:06d}.c"
            path.write_bytes(text.encode("utf-8", errors="surrogateescape"))
            done = subprocess.run([gcc, "-std=gnu99", "-E", "-P", str(path)],
                                  capture_output=True)
        if done.returncode:
            return None
        return tuple(INT_RE.findall(done.stdout.decode("utf-8", "replace")))
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        return list(pool.map(one, enumerate(texts)))


def cases(ns):
    gcc = os.environ["R272_GCC"]
    out = Path(os.environ["R272_OUT"])
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(int(os.environ.get("R272_FUZZ_SEED", "272006")))
    count = int(os.environ.get("R272_FUZZ_N", "30000"))
    texts = list(dict.fromkeys(sample(rng) for _ in range(count)))
    admitted, refused = [], {"allowlist": 0, "other": 0}
    for text in texts:
        try:
            ns["assert_within_lexical_subset"](text)
            admitted.append(text)
        except AssertionError as exc:
            refused["allowlist" if ns["SUBSET_CHARACTER_PIN"] in str(exc)
                    else "other"] += 1
    found = gcc_keeps(gcc, admitted)
    disagree, outcomes = [], {}
    for text, kept in zip(admitted, found):
        try:
            read = ns["lexer_readers"]["keeps"](text)
        except Exception as exc:
            read = ("EXC", type(exc).__name__)
        outcomes[str(kept)] = outcomes.get(str(kept), 0) + 1
        if read != kept:
            disagree.append({"text": text, "reader": read, "gcc": kept})
    summary = {"samples": len(texts), "refused": refused,
               "admitted": len(admitted), "gcc_outcomes": outcomes,
               "admitted_disagree": len(disagree)}
    (out / "fuzz.json").write_text(json.dumps(
        {"summary": summary, "disagree": disagree}, indent=1,
        default=str) + "\n", encoding="utf-8")
    print("FUZZ", json.dumps(summary), flush=True)
    for row in disagree[:20]:
        print("  DISAGREE", json.dumps(row, default=str)[:300], flush=True)
    return ()
