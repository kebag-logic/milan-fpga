# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fw_coverage_selftest.py - the planted cases of the firmware coverage gate (#665 lane FT).

Each case hands fw_coverage.py's reader, exclusions and ratchet a planted
measurement and requires the verdict planted: a clean measurement passes, and
every drop, every file in one table and not the other, and every exclusion
that is unreasoned, misplaced, ambiguous or stale is refused. The last case
runs the real gcc and gcov over a program it builds, so the reader is held to
the tool's own output on the host or runner that runs it, not only to the
fixtures here.

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


def doc(file: str, *, f_arcs: tuple[int, ...] = (2, 1, 1, 1), line4: int = 1, g_arcs: tuple[int, int] = (0, 3),
        line10: int = 0) -> dict:
    """A gcov JSON document of SOURCE: f fully covered unless told, g's `if` never true."""
    def ln(n: int, count: int, arcs: tuple[int, ...] = ()) -> dict:
        """One line entry, its arcs alternately the fallthrough."""
        return {"line_number": n, "count": count,
                "branches": [{"count": a, "throw": False, "fallthrough": k % 2 == 0} for k, a in enumerate(arcs)]}
    return {"files": [{"file": file,
                       "functions": [{"name": "f", "start_line": 1, "end_line": 6},
                                     {"name": "g", "start_line": 7, "end_line": 12}],
                       "lines": [ln(1, 2), ln(3, 2, f_arcs), ln(4, line4), ln(5, 1), ln(7, 3), ln(9, 3, g_arcs),
                                 ln(10, line10), ln(11, 3)]}]}


def merged_of(*docs: dict) -> dict[str, cov.Source]:
    """The reader's view of some documents."""
    out: dict[str, cov.Source] = {}
    for d in docs:
        cov.read_gcov_json(d, out)
    return out


def row(statement: str = "if (a == 7)", uncovered: str = "1 arc, 1 line", reason: str = "never 7",
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
        ("an exclusion gone stale: what it names is covered now",
         lambda: p.verdict([p.doc(g_arcs=(1, 3), line10=1)], [row()], FULL),
         "the rows say 1 arcs and 1 lines uncovered, the measurement 0 and 0"),
        ("an exclusion that states less than is uncovered", lambda: p.verdict(clean, [row(uncovered="1 arc")], FULL),
         "the rows say 1 arcs and 0 lines uncovered, the measurement 1 and 1"),
        ("an exclusion whose count cannot be read", lambda: p.verdict(clean, [row(uncovered="one arc")], FULL),
         "cannot read"),
        ("two builds of one source merge to the union",
         lambda: p.verdict([p.doc(f_arcs=(2, 0, 1, 1)), p.doc(f_arcs=(0, 1, 0, 0))], [row()], FULL), ""),
        ("a build with fewer arcs on a line covers none of the longer build's",
         lambda: p.verdict([p.doc(f_arcs=(1, 1)), p.doc(f_arcs=(2, 0, 1, 1))], [row()], FULL),
         "branches 4/5 fell below the recorded 5/5"),
        ("a test, a host model and a source outside the tree are not measured", p.not_firmware, ""),
        ("an exception edge is not a branch", p.throw_edge, ""),
        ("gcc and gcov on this host read as planted", lambda: real_gcov(p), ""),
    ]


def real_gcov(p: Planted) -> list[str]:
    """Build the planted source with gcc --coverage, run f(1, 1), f(0, 0) and
    g(3), and read gcov's gzipped JSON: f's `b > 0` is never false (one arc,
    no line), g's `a == 7` is never true (one arc) and its `return 9;` never
    runs (one line)."""
    if shutil.which("gcc") is None or shutil.which("gcov") is None:
        return ["no gcc or gcov on this host"]
    build = p.root / "build"
    build.mkdir(exist_ok=True)
    main = build / "main.c"
    main.write_text("int f(int, int);\nint g(int);\nint main(void) { return f(1, 1) + f(0, 0) + g(3) - 4; }\n",
                    encoding="utf-8")
    for argv in (["gcc", "-O0", "--coverage", "-c", str(p.root / FILE), "-o", str(build / "x.o")],
                 ["gcc", "-O0", "-c", str(main), "-o", str(build / "main.o")],
                 ["gcc", "--coverage", str(build / "x.o"), str(build / "main.o"), "-o", str(build / "prog")],
                 [str(build / "prog")]):
        res = subprocess.run(argv, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            return [f"{Path(argv[0]).name} exited {res.returncode}: {res.stderr.strip()[:200]}"]
    source = cov.collect([build]).get(FILE)
    if source is None:
        return ["gcov's output names no planted source"]
    want = {"f": (1, 0), "g": (1, 1)}
    got = {name: cov.uncovered_in(source, source.functions.get(name, (0, 0))) for name in want}
    return [f"{name}(): {got[name]} (arcs, lines) uncovered, want {want[name]}" for name in want
            if got[name] != want[name]]


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
