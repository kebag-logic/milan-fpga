# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fw_coverage_selftest.py - the planted cases of the firmware coverage gate (#665 lane FT).

Each case hands fw_coverage.py's reader, exclusions and ratchet a planted
measurement and requires the verdict planted: a clean measurement passes, and
every drop, every file in one table and not the other, and every exclusion
that is unreasoned, misplaced, ambiguous, stale or moved is refused. The last
three cases run the real gcc and gcov over programs they build, so the reader
and the exclusions are held to the tool's own output on the host or runner
that runs them, not only to the fixtures here: the planted source as
planted, a compensating swap (one uncovered branch covered and another
uncovered in the same function, its totals unchanged), and a condition over
two lines.

Run through `python3 sw/firmware/gtest/fw_coverage.py --selftest`.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

import fw_coverage as cov

FILE = "sw/firmware/ctrl/x.c"
#: The planted source, its lines numbered as the fixtures below number them.
SOURCE = ("int f(int a, int b)\n"  # 1
          "{\n"  # 2
          "\tif (a > 0 && b > 0)\n"  # 3
          "\t\treturn 1;\n"  # 4
          "\treturn 0;\n"  # 5
          "}\n"  # 6
          "int g(int a)\n"  # 7
          "{\n"  # 8
          "\tif (a == 7)\n"  # 9
          "\t\treturn 9;\n"  # 10
          "\treturn a;\n"  # 11
          "}\n")  # 12
#: The planted source's record: f whole, and g's `a == 7` excluded.
FULL = f"{FILE}  lines 7/7  branches 5/5\n"


def ln(n: int, count: int, arcs: tuple[int, ...] = ()) -> dict:
    """One gcov line entry, its arcs alternately the fallthrough."""
    return {"line_number": n, "count": count,
            "branches": [{"count": a, "throw": False, "fallthrough": k % 2 == 0} for k, a in enumerate(arcs)]}


def doc(file: str, *, f_arcs: tuple[int, ...] = (2, 1, 1, 1), line4: int = 1, g_arcs: tuple[int, int] = (0, 3),
        line10: int = 0, line11: int = 3) -> dict:
    """A gcov JSON document of SOURCE: f fully covered unless told, g's `if` never true."""
    return {"files": [{"file": file,
                       "functions": [{"name": "f", "start_line": 1, "end_line": 6},
                                     {"name": "g", "start_line": 7, "end_line": 12}],
                       "lines": [ln(1, 2), ln(3, 2, f_arcs), ln(4, line4), ln(5, 1), ln(7, 3), ln(9, 3, g_arcs),
                                 ln(10, line10), ln(11, line11)]}]}


def merged_of(*docs: dict) -> dict[str, cov.Source]:
    """The reader's view of some documents."""
    out: dict[str, cov.Source] = {}
    for d in docs:
        cov.read_gcov_json(d, out)
    return out


def row(statement: str = "if (a == 7)", uncovered: str = "arc 1 of 2; line `return 9;`", reason: str = "never 7",
        function: str = "g") -> cov.Exclusion:
    """One exclusion row of the planted source."""
    return cov.Exclusion(FILE, function, statement, uncovered, reason)


class Planted:
    """A scratch repository holding the planted source, as fw_coverage's ROOT."""

    def __init__(self) -> None:
        """Make the scratch tree and point the reader at it."""
        self.tmp = tempfile.TemporaryDirectory(prefix="fw-cov-selftest.")
        self.root = Path(self.tmp.name).resolve()
        (self.root / FILE).parent.mkdir(parents=True)
        (self.root / FILE).write_text(SOURCE, encoding="utf-8")
        self.saved = cov.ROOT
        cov.ROOT = self.root

    def close(self) -> None:
        """Put the reader back."""
        cov.ROOT = self.saved
        self.tmp.cleanup()

    def doc(self, **kw: object) -> dict:
        """A document naming the planted file by its scratch path."""
        return doc(str(self.root / FILE), **kw)

    def verdict(self, docs: list[dict], rows: list[cov.Exclusion], ratchet: str) -> list[str]:
        """Every finding of the exclusions and the ratchet over a planted measurement."""
        kept, found = cov.apply_exclusions(merged_of(*docs), rows, self.root)
        return found + cov.compare(cov.tally(kept), cov.read_ratchet(ratchet))

    def not_firmware(self) -> list[str]:
        """A test, a host model and a source outside the tree are never measured."""
        paths = (self.root / "sw/firmware/ctrl/test/t.cpp", self.root / "sw/firmware/ctrl_nvm/host/m.c",
                 self.root.parent / "elsewhere/x.c")
        return [f"measured {rel}" for rel in merged_of(*(doc(str(p)) for p in paths))]

    def stack_scope(self) -> list[str]:
        """The TSN stack's sources and public headers are measured; its tests, examples and scripts never are
        (#697)."""
        stack = self.root / "third_party/tsn-c-stack"
        measured = ("src/x.c", "include/x.h")
        never = ("tests/t.cpp", "examples/p.c", "scripts/s.c")
        got = merged_of(*(doc(str(stack / rel)) for rel in measured + never))
        want = {f"third_party/tsn-c-stack/{rel}" for rel in measured}
        return ([f"measured {rel}" for rel in sorted(set(got) - want)] +
                [f"did not measure {rel}" for rel in sorted(want - set(got))])

    def moved_out(self) -> list[str]:
        """R506-1-S1's measurement: g's excluded branch is taken now and its
        line runs, while another arc and another line of g go uncovered, so
        g's totals are what its row states."""
        moved = {"files": [{"file": str(self.root / FILE),
                            "functions": [{"name": "f", "start_line": 1, "end_line": 6},
                                          {"name": "g", "start_line": 7, "end_line": 12}],
                            "lines": [ln(1, 2), ln(3, 2, (2, 1, 1, 1)), ln(4, 1), ln(5, 1), ln(7, 3),
                                      ln(9, 3, (1, 2)), ln(10, 1), ln(11, 3, (0, 3)), ln(12, 0)]}]}
        return self.verdict([moved], [row()], FULL)

    def throw_edge(self) -> list[str]:
        """An exception edge is not a branch arc."""
        line = {"line_number": 3, "count": 1, "branches": [{"count": 1}, {"count": 0, "throw": True}]}
        got = cov.tally(merged_of({"files": [{"file": str(self.root / FILE), "lines": [line]}]}))[FILE]
        return [] if got.branches == (1, 1) else [f"a throw edge was counted: branches {got.branches}"]


def cases(p: Planted) -> list[tuple[str, Callable[[], list[str]], str]]:
    """(what, the findings it produces, a fragment the planted verdict holds: '' for none)."""
    clean = [p.doc()]
    return [
        ("the control: the only gap excluded, at its record", lambda: p.verdict(clean, [row()], FULL), ""),
        ("a branch of f no longer taken", lambda: p.verdict([p.doc(f_arcs=(2, 0, 1, 1))], [row()], FULL),
         "branches 4/5 fell below the recorded 5/5"),
        ("a line of f no longer run", lambda: p.verdict([p.doc(line4=0)], [row()], FULL),
         "lines 6/7 fell below the recorded 7/7"),
        ("the record is a floor: a measurement over it passes",
         lambda: p.verdict(clean, [row()], f"{FILE}  lines 6/7  branches 4/5\n"), ""),
        ("a measured file the ratchet does not record", lambda: p.verdict(clean, [row()], ""),
         "the ratchet does not record it"),
        ("a recorded file nothing measured", lambda: p.verdict([], [], FULL), "nothing measured it"),
        ("an exclusion with no reason", lambda: p.verdict(clean, [row(reason="")], FULL), "no reason given"),
        ("an exclusion whose statement is not in its function",
         lambda: p.verdict(clean, [row(statement="if (a == 8)")], FULL), "occurs 0 times"),
        ("an exclusion whose statement is not one statement",
         lambda: p.verdict(clean, [row(statement="return")], FULL), "occurs 2 times"),
        ("an exclusion naming no function measured", lambda: p.verdict(clean, [row(function="h")], FULL),
         "no such function"),
        ("an exclusion gone stale: the arc it names is covered now",
         lambda: p.verdict([p.doc(g_arcs=(1, 3), line10=1)], [row()], FULL),
         "arcs [] of the statement's 2 are uncovered, the row names [1]"),
        ("an exclusion gone stale: the line it names runs now",
         lambda: p.verdict([p.doc(g_arcs=(1, 3), line10=1)], [row()], FULL), "line 10 `return 9;` runs now"),
        ("an exclusion that names less than is uncovered",
         lambda: p.verdict(clean, [row(uncovered="arc 1 of 2")], FULL),
         "line 10 is unexecuted, and no row names it"),
        ("the uncovered arc moved to the statement's other arc",
         lambda: p.verdict([p.doc(g_arcs=(3, 0), line10=3, line11=0)], [row()], FULL),
         "arcs [2] of the statement's 2 are uncovered, the row names [1]"),
        ("the uncovered arc and line moved to another statement, the function's totals unchanged",
         p.moved_out, "line 11 arc 1 is uncovered, and no row names it"),
        ("an exclusion whose statement has another number of arcs",
         lambda: p.verdict(clean, [row(uncovered="arc 1 of 3; line `return 9;`")], FULL),
         "has 2 arcs, the row says 3"),
        ("an exclusion naming a line no line from the statement on holds",
         lambda: p.verdict(clean, [row(uncovered="arc 1 of 2; line `return 8;`")], FULL),
         "no line from the statement's on holds `return 8;`"),
        ("two exclusions naming one arc", lambda: p.verdict(clean, [row(), row()], FULL),
         "another row of the function names"),
        ("an exclusion whose items cannot be read", lambda: p.verdict(clean, [row(uncovered="one arc")], FULL),
         "cannot read"),
        ("two builds of one source merge to the union",
         lambda: p.verdict([p.doc(f_arcs=(2, 0, 1, 1)), p.doc(f_arcs=(0, 1, 0, 0))], [row()], FULL), ""),
        ("a build with fewer arcs on a line covers none of the longer build's",
         lambda: p.verdict([p.doc(f_arcs=(1, 1)), p.doc(f_arcs=(2, 0, 1, 1))], [row()], FULL),
         "branches 4/5 fell below the recorded 5/5"),
        ("a test, a host model and a source outside the tree are not measured", p.not_firmware, ""),
        ("the stack's sources and headers are measured, its tests and examples are not", p.stack_scope, ""),
        ("an exception edge is not a branch", p.throw_edge, ""),
        ("gcc and gcov on this host read as planted", lambda: real_gcov(p), ""),
        ("gcc: a compensating swap, the control measurement", lambda: real_swap(p, swapped=False), ""),
        ("gcc: a compensating swap, refused with the function's totals unchanged",
         lambda: real_swap(p, swapped=True), "arcs [] of the statement's 2 are uncovered, the row names [1]"),
        ("gcc: a condition over two lines, the control measurement", lambda: real_two_lines(p, swapped=False), ""),
        ("gcc: a condition over two lines, its other operand uncovered instead",
         lambda: real_two_lines(p, swapped=True), "arcs [3] of the statement's 4 are uncovered, the row names [4]"),
    ]


#: The compensating swap's source: two independent branches of one function.
SWAP_FILE = "sw/firmware/ctrl/swap.c"
SWAP = ("int h(int x)\n"  # 1
        "{\n"  # 2
        "\tif (x == 7)\n"  # 3
        "\t\treturn 7;\n"  # 4
        "\tif (x == 9)\n"  # 5
        "\t\treturn 9;\n"  # 6
        "\treturn 0;\n"  # 7
        "}\n")  # 8
#: A condition over two lines; gcc files all four of its arcs under one line.
TWO_LINES_FILE = "sw/firmware/ctrl/two_lines.c"
TWO_LINES = ("int m(int a, int b)\n"  # 1
             "{\n"  # 2
             "\tif (a > 0 &&\n"  # 3
             "\t    b > 0)\n"  # 4
             "\t\treturn 1;\n"  # 5
             "\treturn 0;\n"  # 6
             "}\n")  # 7


def gcc_run(p: Planted, name: str, file: str, text: str, main: str) -> dict[str, cov.Source] | str:
    """Build a source of the planted tree with gcc --coverage, link it with
    `main` (calls, no coverage), run it once and read what gcov leaves (read
    afresh on every call: the exclusions edit what they are given); or why
    not."""
    if shutil.which("gcc") is None or shutil.which("gcov") is None:
        return "no gcc or gcov on this host"
    build = p.root / "build" / name
    if not build.exists():
        build.mkdir(parents=True)
        (p.root / file).write_text(text, encoding="utf-8")
        (build / "main.c").write_text(main, encoding="utf-8")
        for argv in (["gcc", "-O0", "--coverage", "-c", str(p.root / file), "-o", str(build / "x.o")],
                     ["gcc", "-O0", "-c", str(build / "main.c"), "-o", str(build / "main.o")],
                     ["gcc", "--coverage", str(build / "x.o"), str(build / "main.o"), "-o", str(build / "prog")],
                     [str(build / "prog")]):
            res = subprocess.run(argv, capture_output=True, text=True, check=False)
            if res.returncode != 0:
                return f"{Path(argv[0]).name} exited {res.returncode}: {res.stderr.strip()[:200]}"
    merged = cov.collect([build])
    return merged if file in merged else "gcov's output names no planted source"


def real_gcov(p: Planted) -> list[str]:
    """The planted source built with gcc --coverage, f(1, 1), f(0, 0) and g(3)
    run, gcov's gzipped JSON read: f's `b > 0` is never false (its fourth
    arc, no line), g's `a == 7` is never true (its first arc) and its
    `return 9;` never runs; and the planted row of g holds on it."""
    merged = gcc_run(p, "planted", FILE, SOURCE, "int f(int, int);\nint g(int);\n"
                     "int main(void) { return f(1, 1) + f(0, 0) + g(3) - 4; }\n")
    if isinstance(merged, str):
        return [merged]
    source = merged[FILE]
    want = {"f": ({(3, 3)}, set()), "g": ({(9, 0)}, {10})}
    got = {name: cov.uncovered_in(source, source.functions.get(name, (0, 0))) for name in want}
    wrong = [f"{name}(): {got[name]} (arcs, lines) uncovered, want {want[name]}" for name in want
             if got[name] != want[name]]
    return wrong or cov.apply_exclusions(merged, [row()], p.root)[1]


def real_swap(p: Planted, swapped: bool) -> list[str]:
    """R507-1-F2's case on gcc's own output. h's `x == 7` is excluded, its
    first arc and its `return 7;`. The control calls h(0) and h(9), and is
    held to its own tally as the ratchet. The swap calls h(0) and h(7):
    `x == 7` is covered now and `x == 9`'s arc and line are not, so h's
    totals are unchanged, and the swap must be refused."""
    rows = [cov.Exclusion(SWAP_FILE, "h", "if (x == 7)", "arc 1 of 2; line `return 7;`", "never 7")]
    control = gcc_run(p, "swap-control", SWAP_FILE, SWAP, "int h(int);\nint main(void) { return h(0) + h(9) - 9; }\n")
    if isinstance(control, str):
        return [control]
    kept, found = cov.apply_exclusions(control, rows, p.root)
    floor = cov.tally(kept)
    if not swapped:
        return found
    swap = gcc_run(p, "swap", SWAP_FILE, SWAP, "int h(int);\nint main(void) { return h(0) + h(7) - 7; }\n")
    if isinstance(swap, str):
        return [swap]
    kept, found = cov.apply_exclusions(swap, rows, p.root)
    raw = cov.tally(cov.collect([p.root / "build" / "swap"]))
    if raw[SWAP_FILE] != cov.tally(cov.collect([p.root / "build" / "swap-control"]))[SWAP_FILE]:
        return ["the swap changed h's totals: it is not the compensating case"]
    return found + cov.compare(cov.tally(kept), floor)


def real_two_lines(p: Planted, swapped: bool) -> list[str]:
    """A condition over two lines, `a > 0 &&` / `b > 0)`: its row names the
    statement by its first line and counts the arcs over both. The control
    calls m(1, 1) and m(0, 0), leaving `b > 0` never false, its fourth arc;
    the other calls m(1, 0) and m(0, 0), leaving it never true, its third,
    and `return 1;` unrun, which the row does not name."""
    calls = "m(1, 0) + m(0, 0)" if swapped else "m(1, 1) + m(0, 0) - 1"
    merged = gcc_run(p, f"two-lines-{int(swapped)}", TWO_LINES_FILE, TWO_LINES,
                     f"int m(int, int);\nint main(void) {{ return {calls}; }}\n")
    if isinstance(merged, str):
        return [merged]
    rows = [cov.Exclusion(TWO_LINES_FILE, "m", "if (a > 0 &&", "arc 4 of 4", "b is never 0 here")]
    return cov.apply_exclusions(merged, rows, p.root)[1]


def run_cases() -> int:
    """Every planted case; 0 when each reads as planted."""
    p = Planted()
    failures = 0
    try:
        planted = cases(p)
        for what, findings, want in planted:
            got = findings()
            ok = not got if want == "" else any(want in f for f in got)
            print(f"[{'ok' if ok else 'FAIL'}] {what}: {got[0] if got else 'no finding'}")
            failures += 0 if ok else 1
    finally:
        p.close()
    print(f"coverage self-test: {len(planted) - failures} of {len(planted)} planted cases read as planted")
    return 1 if failures else 0
