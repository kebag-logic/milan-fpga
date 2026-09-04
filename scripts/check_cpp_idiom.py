#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: first-party C and C++ uses the construct the C++ Core Guidelines name.

Why this exists. Rule 11 of the maintainability guide
(docs/development/CODE_QUALITY.md) says new and touched first-party C++ follows
the isocpp C++ Core Guidelines, and that the rules whose population can be
counted are gated rather than recommended. Rule 10 does that for
SystemVerilog; until this gate there was no equivalent for the 110 first-party
translation units, and no tool in the tree read C++ for anything but trailing
whitespace (`check_hygiene.py`) and TODO ownership (`check_todo_ownership.py`).

Four things are REFUSED and seven are RATCHETED.

REFUSED - the population is zero and may not grow.

  1. A NAKED `new` OR `delete` in first-party C++ (Core Guidelines R.11, R.20,
     C.149). Every one of the 99 harnesses that owned a Verilated model owned
     it with `new` and a hand-written teardown, 75 of them never called
     `final()`, seven never freed the model at all, and 39 had a `return` in
     `main` that ran before whatever teardown the bottom of `main` performed.
     `milan::tb::Model<T>` in `tb/common/verilator_harness.hpp` owns the model
     for a scope instead, so there is no path out that skips the teardown.
     A placement `new` (`new (buffer) T`) is NOT a finding: it allocates
     nothing and there is nothing to own.

  2. `goto` (ES.76). The tree has none. It is refused at zero because the
     construct that replaces it - a named function with an early `return`, or
     a `break` out of a loop - is always available in C++, and a `goto` added
     to a 4 000-line `main` is the one edit no reader can follow.

  3. An UNBOUNDED C STRING OR CONVERSION CALL - `strcpy`, `strcat`, `sprintf`,
     `vsprintf`, `gets`, `scanf`, `atoi` (SL.str.1, ES.50, and for `atoi` the
     fact that it cannot report failure). The tree has none. `memcpy`,
     `memset` and the `malloc` family are deliberately NOT in this list: see
     WHAT IS NOT CHECKED below.

  4. A DRIFTED COPY OF THE SHARED HARNESS HEADER. `tb/common/verilator_harness.hpp`
     exists once per repository - here and in each project-owned processor -
     because a submodule cannot include a file out of the superproject that
     happens to contain it. Three copies with one meaning is Rule 3's problem
     shape, so the gate compares them byte for byte and names the first
     difference. Copy the file; do not edit the copy.

RATCHETED - too large to repair in one behavior-preserving change, so the
count is recorded in `scripts/cpp_idiom.budget` and may only go down.

  5. C-STYLE CASTS (ES.49). `(uint32_t)x` says nothing about which of six
     conversions it performs and silences every one of them; `static_cast`,
     `reinterpret_cast` and `const_cast` each say which. The count is the
     largest single population here and the reason this is a ratchet.

  6. FILE-SCOPE MUTABLE VARIABLES (I.2). A harness that keeps `dut`, `checks`,
     `fails` and thirty sticky capture flags at file scope has no function a
     reader can understand without reading every other function first. `const`
     and `constexpr` file-scope values are NOT counted: they are the fix.

  7. MACRO CONSTANTS (ES.31, Enum.1). `#define CSR_MILAN_CLK_HZ 125000000ULL`
     has no type, no scope and no respect for namespaces. `constexpr` has all
     three. An include guard, a function-like macro and a macro with an empty
     replacement list are not constants and are not counted.

  8. UNNAMED `enum { ... }` CONSTANT BLOCKS (Enum.2, Enum.5). A bare `enum`
     holding twenty register offsets is an untyped integer bag; a named
     `enum class` - or a block of `constexpr` values - carries the type that
     stops a stream index being passed where a byte address belongs.

  9. MULTI-DECLARATOR DECLARATIONS (ES.10). `static long fails = 0, checks = 0;`
     hides the second name from a reader scanning declarations, and
     `int* a, b;` does not declare what it looks like it declares.

 10. FUNCTIONS OVER `LONG_FUNCTION_LINES` LINES (F.3). The measured maximum in
     this tree is a 4 641-line `main`. This ratchet is the one that tracks
     whether the code is becoming readable, and it is deliberately counted in
     FUNCTIONS rather than lines, so splitting one giant into three merely
     large ones still shows as progress.

 11. A TESTBENCH BUILD THAT HANDS THE COMPILER NO WARNING FLAGS (P.4, P.5).
     Counted over Makefiles rather than translation units. Measured before this
     rule: 84 of 84 passed `-CFLAGS "-std=c++17 -O2"`, one added `-Wall`, none
     added `-Wextra`. See the `WARNING_FLAGS` comment for what that cost and
     for the eleven classes Verilator suppresses that `-Wall -Wextra` cannot
     bring back.

WHAT IS NOT CHECKED, deliberately.

  * `printf` IS NOT A FINDING. SL.io.3 prefers iostreams, and a harness whose
    whole output is a column-aligned table of got/expected values is clearer
    with a format string than with a dozen `std::setw` manipulators. Every
    tally line in this tree is a `printf`, `scripts/suite_tally.py` parses
    those lines, and converting them would be a repository-wide edit that
    changes no property any reader or tool can use.

  * `memcpy`, `memset` AND THE `malloc` FAMILY ARE NOT FINDINGS. They are the
    correct tools for assembling a wire packet out of trivially copyable
    bytes, which is most of what these harnesses do, and `sw/trace` is
    freestanding C99 where there is no alternative. 210 calls, all in that
    shape.

  * NAMING IS RULE 4's. This gate counts constructs, never identifiers.

  * C IS JUDGED AS C. A translation unit under `C_ROOTS` is freestanding C99;
    C-style casts, `#define` constants and file-scope statics are the language
    there, not a deviation from it, so checks 5 to 8 do not run on it. Checks
    2, 3, 9 and 10 do - `goto`, `strcpy`, a multi-declarator line and a
    thousand-line function are as unreadable in C as in C++.

WHAT THE POPULATION IS. Every tracked first-party `.c`, `.cpp`, `.h` and
`.hpp` in this repository and in the two pinned project-owned processors,
through the shared scope helper (`code_quality_scope.py`, which refuses an
absent or off-pin processor), minus `EXCLUDED_PREFIXES`. The one exclusion is
`sw/trace/generated/`, which is barectf 3.1.2 output recorded in
THIRD_PARTY.md: it is vendored AND generated, so it is fixed by re-running
barectf, never by hand. It carries an upstream MIT banner rather than a
generated-by banner, so the shared `is_generated` banner test does not see it
and the prefix is named here instead.

Usage:

    python3 scripts/check_cpp_idiom.py                 # the gate
    python3 scripts/check_cpp_idiom.py --list          # per-file counts
    python3 scripts/check_cpp_idiom.py --write-budget  # re-record the ratchets
    python3 scripts/check_cpp_idiom.py --selftest      # the fixture arms

Exit 0 = no refused construct and every ratchet in `scripts/cpp_idiom.budget`
holds; 1 = a finding, or a missing or malformed ratchet entry; 2 = the
population was refused, which no caller may read as a count of zero.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "cpp_idiom.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_quality_scope import PROJECT_SUBMODULES, tracked  # noqa: E402

#: Suffixes this gate reads. `.hpp` is included for completeness even though
#: the tree currently spells every header `.h`.
SCANNED_SUFFIXES = (".c", ".cpp", ".cc", ".cxx", ".h", ".hpp")

#: barectf 3.1.2 output, recorded in THIRD_PARTY.md. Vendored AND generated:
#: fixed by re-running the generator, never by hand. It carries the upstream
#: MIT banner rather than a "generated by" one, so the shared banner test in
#: `check_hygiene.is_generated` does not see it and it is named here.
EXCLUDED_PREFIXES = ("sw/trace/generated/",)

#: Translation units that are freestanding C99, not C++. Checks that ask for a
#: C++ construct do not run here - there is no `static_cast` in C.
C_ROOTS = ("sw/trace/", "sw/firmware/")

#: The population must reach each of these, or the scan is measuring a tree
#: that is not there. A missing processor reports zero of everything, and zero
#: of everything is a clean ratchet unless the gate refuses to count it.
POPULATION_ROOTS = ("tb/verilator/", "sw/") + tuple(
    f"{sub}/tb/" for sub in PROJECT_SUBMODULES)

#: The shared harness header, once per repository. Byte-identical or refused.
HARNESS_HEADER = "tb/common/verilator_harness.hpp"
HARNESS_HEADER_COPIES = (HARNESS_HEADER,) + tuple(
    f"{sub}/{HARNESS_HEADER}" for sub in PROJECT_SUBMODULES)

#: A testbench Makefile that hands the C++ compiler no warning flags. Measured
#: before this rule: 84 of 84 passed `-CFLAGS "-std=c++17 -O2"`, exactly one
#: added `-Wall`, none added `-Wextra`. So the compiler watched 63 000 lines of
#: hand-written VERIFICATION code and said nothing about a tautological
#: comparison - which in a testbench is a check that can never fail, the exact
#: false green Rule 6 exists to stop. Turning the flags on found one in
#: `tb/verilator/aes3` (`dut->pair_ready_o >= 0` on an unsigned word) and two
#: unsequenced-modification lines - undefined behaviour - in
#: `protocol-processor/tb/dispatch`. Verilator's own generated code compiles
#: clean under them, so the flags are low-noise here.
WARNING_FLAGS = ("-Wall", "-Wextra")
#: A quoted `-CFLAGS` group may contain ESCAPED QUOTES: `tb/verilator/avtp_parser`
#: passes `-DSHAPE_NAME=\\\"N8-BE-beats\\\"` so the shape name reaches the
#: harness as a string literal. A pattern that stops at the first `"` reads the
#: group as ending halfway through that define - and the mechanical pass that
#: used such a pattern inserted `-Wall -Wextra` INTO the escape sequence and
#: broke the suite's build (`unexpected EOF while looking for matching quote`).
#: The full sweep caught it; this expression is why it cannot happen again.
#: `re.S` because a group may also be CONTINUED ACROSS LINES: `tb/verilator/crf_rx`
#: splits its defines over two lines with a trailing `\`, and without DOTALL
#: the `\`+newline pair matches neither alternative, the group never closes,
#: and the gate reports flags missing that are plainly there.
CFLAGS_RE = re.compile(
    r"-CFLAGS\s+(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|\S+)", re.S)

#: F.3's threshold. Not a Core Guidelines number - the Guidelines say "fits on
#: a screen" and decline to pick one. 100 is the value `measure_control_flow.py`
#: already reports Python functions against, so the two rules agree.
LONG_FUNCTION_LINES = 100

#: Comment and string-literal bodies are blanked before matching, so a finding
#: quoted in a docstring is not a finding. Newlines survive, so line numbers do.
#: Comments and literals, blanked before any check reads the source.
#:
#: THE DIGIT-SEPARATOR BUG, on the record. The first alternative below is a
#: C++14 digit separator - the `'` in `0x0000'0FFF` - and it must be matched
#: FIRST so the character-literal alternative cannot open on it. Without it,
#: that apostrophe opened a literal that ran to the next apostrophe in the
#: file, which in tb/verilator/pp_shadow/sim_main.cpp was the one in "engine's"
#: twenty lines below. Everything between them was blanked, including a
#: function's closing braces, so `long_functions` counted braces to EOF and
#: then skipped its scan index past the end - and EVERY function from that
#: point to line 2356 went uncounted, along with two C-style casts. A lexer
#: that loses its place silently makes every count downstream of it a guess.
NON_CODE = re.compile(
    r"(?<=[0-9A-Fa-f])'(?=[0-9A-Fa-f])"
    r'|//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)

#: The primitive and Verilator word types a C-style cast is spelled with here.
#: Matching a closed set rather than "any identifier in parentheses" is what
#: keeps `(condition) && x` and a call through a function pointer out of the
#: count.
_CAST_TYPE = (
    r"(?:unsigned\s+|signed\s+|const\s+|volatile\s+|struct\s+)*"
    r"(?:u?int(?:8|16|32|64|ptr|max)_t|unsigned\s+(?:long\s+long|long|int|char|short)"
    r"|long\s+long|size_t|ssize_t|ptrdiff_t|int|long|short|char|bool|float|double"
    r"|[IQCS]Data|WData|VlWide<\d+>)")

#: A cast is the type in parentheses followed by something to convert. The
#: trailing character class is what separates `(uint32_t)value` from the
#: parameter list `(uint32_t index, bool flag)`. `(void)x` is deliberately
#: absent from `_CAST_TYPE`: it discards a value rather than converting one,
#: and `static_cast<void>(x)` says nothing `(void)x` does not.
CAST_RE = re.compile(rf"\(\s*{_CAST_TYPE}\s*\**\s*\)\s*(?=[A-Za-z_(&*\-+~!0-9])")

#: `new`/`delete` as operators. `new` followed by `(` is a placement new, which
#: allocates nothing; `delete` in `= delete` is a deleted function, not a
#: deallocation, and is excluded by requiring a preceding non-`=` context.
NEW_RE = re.compile(r"\bnew\b(?!\s*\()")
DELETE_RE = re.compile(r"(?<![=\s]=\s)\bdelete\b(?!\s*[;)])")

GOTO_RE = re.compile(r"\bgoto\b")

UNBOUNDED_RE = re.compile(
    r"\b(?:strcpy|strcat|sprintf|vsprintf|gets|scanf|atoi|atol|atof)\s*\(")

#: `#define NAME value` with a non-empty replacement list and no parameter
#: list. An include guard is `#define NAME` with nothing after it and does not
#: match; `#define LOG(x) ...` has a parameter list and does not match.
MACRO_CONST_RE = re.compile(r"^[ \t]*#[ \t]*define[ \t]+[A-Za-z_]\w*[ \t]+\S")

UNNAMED_ENUM_RE = re.compile(r"\benum\s*(?:class\s+)?\{")

#: A declaration naming more than one entity. Anchored on a declaration
#: introducer so `f(a, b);` and `for (i = 0, j = 1; ...)` are not declarations.
_DECL_TYPE = (
    r"(?:static\s+|const\s+|constexpr\s+|volatile\s+|unsigned\s+|signed\s+|register\s+)*"
    r"(?:u?int(?:8|16|32|64|ptr|max)_t|long\s+long|size_t|ssize_t|bool|char|short"
    r"|int|long|float|double|auto|[IQCS]Data|WData)")
MULTI_DECL_RE = re.compile(
    rf"^[ \t]*{_DECL_TYPE}[ \t]+\**[A-Za-z_]\w*[^;()\n]*,[^;()\n]*;[ \t]*$", re.M)

#: A file-scope definition of a mutable variable. Applied only to lines at
#: brace depth zero, so a local is never counted. `const`, `constexpr`,
#: `typedef`, `using` and every type-introducing keyword are excluded: a
#: file-scope constant is what I.2 asks for, not what it forbids.
_NOT_A_VARIABLE = (
    "const", "constexpr", "typedef", "using", "namespace", "struct", "class",
    "enum", "union", "template", "return", "else", "extern", "inline",
    "public", "private", "protected", "friend", "operator", "static_assert")
FILE_SCOPE_RE = re.compile(
    r"^(?:static\s+)?([A-Za-z_][\w:]*(?:\s*<[^;{}]*>)?)"
    r"[\s*&]+([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*(?:=[^;]*)?;\s*$")

#: A function definition opening at ANY indentation: a signature ending in `{`.
#: Control-flow keywords are excluded, and so is a line that is only a call.
#:
#: THE INDENTATION BLIND SPOT, on the record. This pattern was anchored at
#: column zero (`^(?!\s)`), which is where a free function and a `main` open.
#: A MEMBER function opens indented inside its class body, so none was ever
#: counted. That made the ratchet answer the wrong question the moment the
#: harnesses were repaired: wrapping a 4 679-line `main` in a harness class
#: turns it into a 4 679-line `run()` that the gate reads as zero findings.
#: Measured at the commit that widened this: the tree reported `long function:
#: 0` while 21 functions were still over the limit, the largest 756 lines. A
#: ratchet that a legitimate refactor can zero without shortening a single
#: function is not a measurement, so the anchor is gone.
#:
#: Four shapes are excluded because they end in `{` without opening a function:
#: a lambda (`auto f = [&](int x) {` — caught by the `=` and `[` guards), a
#: `} else if (...) {` continuation (leading `}`), a class or namespace head
#: (no parameter list), and a brace-initialiser (`Foo x{...}` — no `)` before
#: the brace). A constructor's member-init list spans lines and its `{` lands
#: on a line with no parameter list, so it opens no function here either; the
#: body is still walked, because the walk is driven by brace depth.
FUNC_OPEN_RE = re.compile(
    r"^[ \t]*"
    r"(?!(?:if|for|while|switch|else|do|return|case|default|try|catch)\b)"
    r"(?![}=])"
    r"[A-Za-z_~][\w\s:*&<>,\[\]]*\([^;=]*\)\s*"
    r"(?:const\s*)?(?:noexcept\s*)?(?:override\s*)?(?:final\s*)?\{\s*$")

#: Every ratchet key, in report order. A key missing from the budget file is a
#: failure, never an unbounded allowance.
RATCHETED = (
    "c-style cast",
    "file-scope mutable",
    "macro constant",
    "unnamed enum block",
    "multi-declarator declaration",
    "long function",
    "build without warnings",
)

#: Every refusal key, in report order.
REFUSED = (
    "naked new/delete",
    "goto",
    "unbounded C call",
)


def blank_non_code(text):
    """Comment and string bodies become spaces; newlines and offsets survive."""
    def blank(match):
        matched = match.group(0)
        if matched == "'":
            return "'"       # a digit separator is code, and stays code
        return "".join(c if c == "\n" else " " for c in matched)
    return NON_CODE.sub(blank, text)


def is_c(rel):
    """True when this translation unit is freestanding C, not C++."""
    return rel.startswith(C_ROOTS)


def in_scope(rel):
    return rel.endswith(SCANNED_SUFFIXES) and not rel.startswith(EXCLUDED_PREFIXES)


def sources():
    """Every tracked first-party C/C++ path, across both project processors."""
    return sorted(p for p in tracked(*(f"*{s}" for s in SCANNED_SUFFIXES))
                  if in_scope(p))


def population_problem(paths):
    """Why this population may not be judged, or None when it is complete."""
    if not paths:
        return "the scan found no tracked C or C++ at all"
    missing = [root for root in POPULATION_ROOTS
               if not any(p.startswith(root) for p in paths)]
    if missing:
        return "no tracked C or C++ under " + ", ".join(missing)
    return None


def file_scope_mutables(code):
    """Line numbers of file-scope mutable definitions in already-blanked code."""
    found = []
    depth = 0
    for lineno, line in enumerate(code.splitlines(), 1):
        stripped = line.strip()
        if depth == 0 and stripped and not stripped.startswith("#"):
            match = FILE_SCOPE_RE.match(stripped)
            if match and match.group(1).split()[0] not in _NOT_A_VARIABLE:
                # `static const int A = 1, B = 2;` reaches here with group(1)
                # == "static", so test every leading word, not just the first.
                lead = stripped.split("=")[0].split()
                if not any(word in _NOT_A_VARIABLE for word in lead):
                    found.append(lineno)
        depth = max(0, depth + line.count("{") - line.count("}"))
    return found


def long_functions(code, limit=LONG_FUNCTION_LINES):
    """(line, length) for every function definition longer than `limit`."""
    lines = code.splitlines()
    found = []
    index = 0
    while index < len(lines):
        if not FUNC_OPEN_RE.match(lines[index]):
            index += 1
            continue
        depth = lines[index].count("{") - lines[index].count("}")
        end = index + 1
        while end < len(lines) and depth > 0:
            depth += lines[end].count("{") - lines[end].count("}")
            end += 1
        length = end - index
        if length > limit:
            found.append((index + 1, length))
        index = end
    return found


def scan(text, rel="x.cpp"):
    """Every counted construct in one translation unit's source text."""
    code = blank_non_code(text)
    cpp = not is_c(rel)
    counts = {
        "naked new/delete": (len(NEW_RE.findall(code)) + len(DELETE_RE.findall(code))
                             if cpp else 0),
        "goto": len(GOTO_RE.findall(code)),
        "unbounded C call": len(UNBOUNDED_RE.findall(code)),
        "c-style cast": len(CAST_RE.findall(code)) if cpp else 0,
        "file-scope mutable": len(file_scope_mutables(code)) if cpp else 0,
        "macro constant": len(MACRO_CONST_RE.findall(code)) if cpp else 0,
        "unnamed enum block": len(UNNAMED_ENUM_RE.findall(code)) if cpp else 0,
        "multi-declarator declaration": len(MULTI_DECL_RE.findall(code)),
        "long function": len(long_functions(code)),
        "build without warnings": 0,   # counted over Makefiles, in audit()
    }
    return counts


def sites(text, key, rel="x.cpp"):
    """[(line, snippet)] for one key, so a finding can name where it is."""
    code = blank_non_code(text)
    patterns = {
        "naked new/delete": (NEW_RE, DELETE_RE),
        "goto": (GOTO_RE,),
        "unbounded C call": (UNBOUNDED_RE,),
        "c-style cast": (CAST_RE,),
        "macro constant": (MACRO_CONST_RE,),
        "unnamed enum block": (UNNAMED_ENUM_RE,),
        "multi-declarator declaration": (MULTI_DECL_RE,),
    }
    raw_lines = text.splitlines()
    out = []
    if key == "file-scope mutable":
        out = [(n, raw_lines[n - 1].strip()) for n in file_scope_mutables(code)]
    elif key == "long function":
        out = [(n, f"{length} lines: {raw_lines[n - 1].strip()[:70]}")
               for n, length in long_functions(code)]
    else:
        for pattern in patterns.get(key, ()):
            for match in pattern.finditer(code):
                n = code[:match.start()].count("\n") + 1
                out.append((n, raw_lines[n - 1].strip()[:90]))
    return sorted(out)


def audit(paths):
    """(totals, per_file) over the population."""
    totals = dict.fromkeys(tuple(RATCHETED) + tuple(REFUSED), 0)
    per_file = {}
    for rel in paths:
        counts = scan((REPO / rel).read_text(errors="replace"), rel)
        per_file[rel] = counts
        for key, value in counts.items():
            totals[key] += value
    # Counted over Makefiles, not translation units, so it is added after the
    # per-file walk rather than inside `scan`.
    totals["build without warnings"] = len(makefiles_without_warnings())
    return totals, per_file


def testbench_makefiles():
    """Every tracked Makefile that drives a Verilator testbench build."""
    return sorted(p for p in tracked("Makefile", "*/Makefile")
                  if "/tb/" in f"/{p}" and not p.startswith(EXCLUDED_PREFIXES))


def cflags_missing(text):
    """Which warning flags this Makefile's -CFLAGS groups do not all carry.

    A Makefile may hand -CFLAGS to several verilator invocations - the csr
    suite builds four executables - and a flag enabled for one of them is not
    enabled for the others, so EVERY group must carry it. A Makefile with no
    -CFLAGS at all is not a testbench build and is not judged.
    """
    # A Makefile comment is not a build line. `tb/verilator/rx_filter/Makefile`
    # explains its own `-CFLAGS` quoting in prose, and a first version of this
    # check read that sentence as a build that was missing the flags - and the
    # mechanical pass that used the same expression appended `-Wall -Wextra` to
    # the end of the comment.
    build_lines = "\n".join(line for line in text.splitlines()
                            if not line.lstrip().startswith("#"))
    groups = CFLAGS_RE.findall(build_lines)
    if not groups:
        return []
    return sorted(flag for flag in WARNING_FLAGS
                  if not all(flag in group for group in groups))


def makefiles_without_warnings(paths=None):
    """[(path, flags)] for each testbench Makefile whose -CFLAGS omits a flag."""
    found = []
    for rel in (paths if paths is not None else testbench_makefiles()):
        missing = cflags_missing((REPO / rel).read_text(errors="replace"))
        if missing:
            found.append((rel, " ".join(missing)))
    return found


def header_drift(paths):
    """The first byte-level difference between the harness header copies."""
    present = [rel for rel in HARNESS_HEADER_COPIES if (REPO / rel).is_file()]
    if not present:
        return None
    if HARNESS_HEADER not in present:
        return f"{HARNESS_HEADER} is missing but a processor carries a copy"
    reference = (REPO / HARNESS_HEADER).read_bytes()
    for rel in present:
        if rel == HARNESS_HEADER:
            continue
        other = (REPO / rel).read_bytes()
        if other != reference:
            for offset, (a, b) in enumerate(zip(reference, other)):
                if a != b:
                    line = reference[:offset].count(b"\n") + 1
                    return (f"{rel} differs from {HARNESS_HEADER} at line {line}")
            return (f"{rel} differs from {HARNESS_HEADER} in length "
                    f"({len(other)} vs {len(reference)} bytes)")
    # A harness that includes the header from a repository that has no copy
    # cannot compile, so an absent copy is only a finding when something needs it.
    for rel in paths:
        for sub in PROJECT_SUBMODULES:
            if rel.startswith(f"{sub}/") and f"{sub}/{HARNESS_HEADER}" not in present:
                if "verilator_harness.hpp" in (REPO / rel).read_text(errors="replace"):
                    return (f"{rel} includes the shared harness header but "
                            f"{sub}/{HARNESS_HEADER} does not exist")
    return None


def parse_budget(text):
    """{key: int} from budget text; a malformed value simply has no entry."""
    out = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            key, value = line.split("=", 1)
            if value.strip().isdigit():
                out[key.strip()] = int(value.strip())
    return out


def read_budget():
    return parse_budget(BUDGET.read_text()) if BUDGET.is_file() else {}


def ratchet(totals, budget):
    """A missing or malformed entry is a failure, because an absent budget must
    not read as an unbounded one. A count below its entry is a note that the
    entry can be lowered: a budget only moves downward, and slack in it is
    exactly where the next regression hides."""
    failures, notes = [], []
    for key in RATCHETED:
        limit = budget.get(key)
        if limit is None:
            failures.append(f"NO RATCHET for {key!r} in {BUDGET.relative_to(REPO)} "
                            f"(entry missing or not an integer)")
        elif totals[key] > limit:
            failures.append(
                f"FAIL: {key} {totals[key]} > ratchet {limit}. New C++ uses the "
                f"named construct; see Rule 11 in docs/development/CODE_QUALITY.md.")
        elif totals[key] < limit:
            notes.append(f"  the {key} ratchet can be lowered to {totals[key]}")
    return failures, notes


def write_budget(totals):
    """Re-record the ratchets at the measured counts. Never raises one."""
    previous = read_budget()
    raised = [key for key in RATCHETED
              if key in previous and totals[key] > previous[key]]
    if raised:
        print("REFUSED: --write-budget may only lower a ratchet; these rose: "
              + ", ".join(raised), file=sys.stderr)
        return 1
    width = max(len(key) for key in RATCHETED)
    lines = [
        "# Rule 11 ratchets - the C and C++ idiom debt this tree still carries.",
        "# EVERY NUMBER MAY ONLY GO DOWN. Regenerate with",
        "#   python3 scripts/check_cpp_idiom.py --write-budget",
        "# which refuses to raise one. What each entry counts, and why it is a",
        "# ratchet rather than a refusal, is in the gate's own docstring and in",
        "# docs/development/CODE_QUALITY.md's Rule 11.",
        "",
    ]
    for key in RATCHETED:
        lines.append(f"{key.ljust(width)} = {totals[key]}")
    BUDGET.write_text("\n".join(lines) + "\n")
    print(f"wrote {BUDGET.relative_to(REPO)}")
    return 0


def selftest():
    checks = failures = 0

    def ck(name, ok, detail=""):
        nonlocal checks, failures
        checks += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}" + (f": {detail}" if detail else ""))

    # --- the refusals bite ---------------------------------------------------
    ck("a naked new is a finding", scan("int main(){ auto* p = new Vfoo; }")
       ["naked new/delete"] == 1)
    ck("a naked delete is a finding", scan("void f(){ delete dut; }")
       ["naked new/delete"] == 1)
    ck("a placement new is not a finding",
       scan("void f(char* b){ ::new (b) Foo(); }")["naked new/delete"] == 0,
       "placement new allocates nothing, so there is nothing to own")
    ck("a deleted function is not a finding",
       scan("struct S { S(const S&) = delete; };")["naked new/delete"] == 0,
       "`= delete` is a deleted function, not a deallocation")
    ck("goto is a finding", scan("void f(){ goto done; done: ; }")["goto"] == 1)
    ck("strcpy is a finding", scan("void f(){ strcpy(a, b); }")
       ["unbounded C call"] == 1)
    ck("atoi is a finding", scan("int f(){ return atoi(s); }")
       ["unbounded C call"] == 1,
       "atoi cannot report a failure, so a bad input reads as zero")
    ck("memcpy is deliberately not a finding",
       scan("void f(){ memcpy(a, b, 4); }")["unbounded C call"] == 0,
       "memcpy is the right tool for a wire packet and is recorded as allowed")

    # --- the ratchets count the right thing ----------------------------------
    ck("a C-style cast is a finding",
       scan("void f(){ g((uint32_t)value); }")["c-style cast"] == 1)
    ck("a static_cast is not a finding",
       scan("void f(){ g(static_cast<uint32_t>(value)); }")["c-style cast"] == 0)
    ck("a parameter list is not a cast",
       scan("void f(uint32_t index, bool flag) { g(index, flag); }")
       ["c-style cast"] == 0,
       "`(uint32_t index, ...)` is a declaration, not a conversion")
    ck("a discarding (void) cast is deliberately not a finding",
       scan("void f(int unused) { (void)unused; }")["c-style cast"] == 0,
       "it discards a value rather than converting one")
    ck("a parenthesised condition is not a cast",
       scan("void f(){ if (ready) g(); }")["c-style cast"] == 0)
    ck("a file-scope mutable is a finding",
       scan("static long fails = 0;\n")["file-scope mutable"] == 1)
    ck("a file-scope const is not a finding",
       scan("static const int SRC_HP = 2;\n")["file-scope mutable"] == 0,
       "a file-scope constant is what I.2 asks for, not what it forbids")
    ck("a file-scope constexpr is not a finding",
       scan("constexpr int kSrcHalfPeriod = 2;\n")["file-scope mutable"] == 0)
    ck("a local is not a file-scope mutable",
       scan("void f() {\nlong fails = 0;\n}\n")["file-scope mutable"] == 0,
       "the depth counter is what keeps a function body out of the count")
    ck("a static const list is not a file-scope mutable",
       scan("static const int A = 1, B = 2;\n")["file-scope mutable"] == 0,
       "the first word is `static`, so every leading word must be tested")
    ck("a macro constant is a finding",
       scan("#define CSR_MILAN_CLK_HZ 125000000ULL\n")["macro constant"] == 1)
    ck("an include guard is not a macro constant",
       scan("#define MILAN_TB_HARNESS_HPP\n")["macro constant"] == 0,
       "an include guard has an empty replacement list")
    ck("a function-like macro is not a macro constant",
       scan("#define LOG(x) printf(x)\n")["macro constant"] == 0)
    ck("an unnamed enum block is a finding",
       scan("enum { A_ID = 0, A_VER = 4 };")["unnamed enum block"] == 1)
    ck("a named enum is not a finding",
       scan("enum class Reg { id = 0 };")["unnamed enum block"] == 0)
    ck("a multi-declarator declaration is a finding",
       scan("static long fails = 0, checks = 0;\n")
       ["multi-declarator declaration"] == 1)
    ck("a single declaration is not a finding",
       scan("static long fails = 0;\n")["multi-declarator declaration"] == 0)
    ck("a call with two arguments is not a declaration",
       scan("void f(){ g(a, b); }\n")["multi-declarator declaration"] == 0)
    long_body = "void f() {\n" + "    x++;\n" * (LONG_FUNCTION_LINES + 5) + "}\n"
    ck("a function over the line limit is a finding",
       scan(long_body)["long function"] == 1)
    ck("a short function is not a finding",
       scan("void f() {\n    x++;\n}\n")["long function"] == 0)
    # The indentation blind spot, as fixtures. Every arm below reported 0
    # before FUNC_OPEN_RE lost its column-zero anchor; the first is the one
    # that mattered, because wrapping a giant `main` in a harness class is
    # exactly the repair Rule 11 asks for and it must not zero the ratchet.
    long_member = ("class H {\n void run() {\n" + "    x++;\n" * (LONG_FUNCTION_LINES + 5)
                   + " }\n};\n")
    ck("a long member function is a finding",
       scan(long_member)["long function"] == 1,
       "a member opens indented; the ratchet must still see it")
    ck("a long out-of-line member definition is a finding",
       scan("void H::run() {\n" + "    x++;\n" * (LONG_FUNCTION_LINES + 5) + "}\n")
       ["long function"] == 1)
    ck("a long lambda body is not counted as its own function",
       scan("void f() {\n  auto g = [&](int n) {\n"
            + "    x++;\n" * (LONG_FUNCTION_LINES + 5) + "  };\n}\n")
       ["long function"] == 1,
       "one finding for f, not two: the lambda is part of the function that owns it")
    ck("an else-if continuation is not a function",
       scan("void f() {\n  if (a) {\n    x++;\n  } else if (b) {\n"
            + "    x++;\n" * (LONG_FUNCTION_LINES + 5) + "  }\n}\n")
       ["long function"] == 1)
    ck("a class head is not a function",
       scan("class H {\n" + " int x_ = 0;\n" * (LONG_FUNCTION_LINES + 5) + "};\n")
       ["long function"] == 0)
    ck("a brace-initialiser is not a function",
       scan("void f() {\n  Foo x{1, 2};\n  x++;\n}\n")["long function"] == 0)

    # --- blanking: a finding inside a comment or a string is not a finding ---
    ck("a construct in a line comment is not counted",
       scan("// delete dut; goto done;\n")["naked new/delete"] == 0)
    ck("a construct in a block comment is not counted",
       scan("/*\n  auto* p = new Vfoo;\n*/\n")["naked new/delete"] == 0)
    ck("a construct in a string is not counted",
       scan('void f(){ puts("goto strcpy"); }')["goto"] == 0)
    # The digit separator, as fixtures. The first arm is the shape that hid
    # 755 lines of tb/verilator/pp_shadow/sim_main.cpp from every check.
    ck("a digit separator does not open a character literal",
       scan("void f() {\n  uint32_t m = 0x0000'0FFF;\n}\n"
            "// the engine's mask\nvoid g() {\n  int a = 1, b = 2;\n}\n")
       ["multi-declarator declaration"] == 1,
       "the `'` in 0x0000'0FFF once blanked everything up to \"engine's\"")
    ck("a digit separator leaves brace counting intact",
       scan("void f() {\n  uint32_t m = 0x1'000;\n" + "  x++;\n" * 120 + "}\n"
            "// don't\n")["long function"] == 1)
    ck("a character literal is still blanked",
       scan("void f(){ char c = '}'; }\n")["long function"] == 0,
       "the separator arm must not stop a real literal being non-code")
    ck("a goto inside a character literal is not a finding",
       scan("void f(){ char c = 'g'; }\n")["goto"] == 0)
    ck("blanking preserves line numbers",
       sites("// pad\n// pad\nstatic long fails = 0;\n", "file-scope mutable")
       == [(3, "static long fails = 0;")],
       "the site is reported at line 3, so blanking kept the newlines")

    # --- C is judged as C ----------------------------------------------------
    ck("a C-style cast in C is not a finding",
       scan("void f(){ g((uint32_t)v); }", "sw/trace/milan_trace.c")
       ["c-style cast"] == 0,
       "there is no static_cast in C99")
    ck("a macro constant in C is not a finding",
       scan("#define RING_BYTES 4096\n", "sw/trace/milan_trace.h")
       ["macro constant"] == 0)
    ck("goto in C is still a finding",
       scan("void f(){ goto out; out: ; }", "sw/trace/milan_trace.c")["goto"] == 1,
       "checks 2, 3, 9 and 10 run on C too")
    ck("a long function in C is still a finding",
       scan(long_body, "sw/trace/milan_trace.c")["long function"] == 1)

    # --- budget logic --------------------------------------------------------
    measured = dict.fromkeys(RATCHETED, 0)
    measured["c-style cast"] = 2
    full = dict(measured)
    below = dict(full, **{"c-style cast": 1})
    slack = dict(full, **{"c-style cast": 3})
    ck("a count above its budget fails the ratchet",
       ratchet(measured, below)[0] != [])
    ck("a count equal to its budget passes with no note",
       ratchet(measured, full) == ([], []))
    ck("a count below its budget passes and names the lowerable value",
       ratchet(measured, slack)[0] == [] and "lowered to 2" in ratchet(measured, slack)[1][0])
    ck("a missing budget entry fails the ratchet",
       ratchet(measured, {k: 0 for k in RATCHETED if k != "long function"})[0] != [],
       "an absent entry must never read as an unbounded allowance")
    ck("a malformed budget value is no entry",
       parse_budget("c-style cast = many") == {})
    ck("an absent budget file is an empty budget",
       parse_budget("") == {})
    ck("a comment is stripped from a budget line",
       parse_budget("c-style cast = 7  # the count at the head") ==
       {"c-style cast": 7})

    # --- the live tree -------------------------------------------------------
    paths = sources()
    ck("the scan reaches over 100 first-party translation units", len(paths) > 100,
       f"found {len(paths)}")
    for sub in PROJECT_SUBMODULES:
        ck(f"the scan reaches {sub}", any(p.startswith(f"{sub}/") for p in paths))
    ck("the live population is complete", population_problem(paths) is None,
       str(population_problem(paths)))
    ck("generated barectf output is out of scope",
       not any(p.startswith("sw/trace/generated/") for p in paths),
       "it is vendored AND generated; THIRD_PARTY.md records it")
    ck("an empty population is refused",
       population_problem([]) is not None)
    ck("a population missing a processor is refused",
       population_problem(["tb/verilator/csr/sim_main.cpp", "sw/trace/milan_trace.c"])
       is not None,
       "a partial scan must never establish a smaller baseline")
    totals, _ = audit(paths)
    # ANTI-VACUITY, REBASED ON DETECTION RATHER THAN ON DEBT. This arm used to
    # require some ratcheted population to be above zero, which conflates "the
    # scan is working" with "the tree still carries debt": it holds until the
    # rule is fully complied with and then turns the gate's own self-test red.
    # A rule must not be written so that finishing it is a failure. What the
    # guard is for is a live scan that has gone inert, so it now plants each
    # ratcheted construct into a REAL tree source and requires the live path to
    # count it. That holds at any population, including zero.
    planted_from = next(p for p in paths if str(p).endswith(".cpp"))
    planted_text = (REPO / planted_from).read_text(errors="replace")
    planted_base = scan(planted_text, str(planted_from))
    planted = planted_text + (
        "\nstatic int planted_mutable_;\n"
        "static int planted_one_, planted_two_;\n"
        "void planted_long_function() {\n" + "    planted_mutable_++;\n" * 120 + "}\n")
    planted_totals = scan(planted, str(planted_from))
    for key, added in (("file-scope mutable", 1), ("multi-declarator declaration", 1),
                       ("long function", 1)):
        ck(f"the live scan still detects a planted {key}",
           planted_totals[key] == planted_base[key] + added,
           f"planted into {planted_from}: expected "
           f"{planted_base[key] + added}, got {planted_totals[key]}")
    ck("a clean tree is allowed to be clean",
       all(totals[key] >= 0 for key in RATCHETED),
       "the population may legitimately be zero; the planted arms above are "
       "what prove the scan is not inert")
    budget = read_budget()
    ck("the checked-in budget carries every ratcheted key",
       all(key in budget for key in RATCHETED),
       f"missing {[k for k in RATCHETED if k not in budget]}")
    ck("a build with no warning flags is a finding",
       cflags_missing('\t$(V) -CFLAGS "-std=c++17 -O2" x.cpp\n')
       == ["-Wall", "-Wextra"])
    ck("a build with both warning flags is not a finding",
       cflags_missing('\t$(V) -CFLAGS "-std=c++17 -O2 -Wall -Wextra" x.cpp\n') == [])
    ck("a flag enabled for only one of several builds is a finding",
       cflags_missing('\t$(V) -CFLAGS "-O2 -Wall -Wextra" a.cpp\n'
                      '\t$(V) -CFLAGS "-O2" b.cpp\n') == ["-Wall", "-Wextra"],
       "the csr suite builds four executables; a flag on one is not a flag on all")
    ck("a Makefile with no -CFLAGS is not judged",
       cflags_missing("all:\n\techo hi\n") == [],
       "it is not a testbench build")
    ck("a -CFLAGS group continued across lines is one group",
       cflags_missing('\t$(V) -CFLAGS "-O2 -DA=1 \\\n           -DB=2 -Wall -Wextra"\n')
       == [],
       "crf_rx splits its defines over two lines with a trailing backslash")
    ck("an escaped quote inside a -CFLAGS group does not end it",
       cflags_missing('\t$(V) -CFLAGS "-DNAME=\\\\\\"x\\\\\\" -Wall -Wextra" a.cpp\n')
       == [],
       "avtp_parser passes a quoted shape name; a pattern that stops at the "
       "first quote reads the group as ending inside the escape")
    ck("a -CFLAGS mentioned in a comment is not a build line",
       cflags_missing('# the shell quoting of -CFLAGS survives\n'
                      '\t$(V) -CFLAGS "-O2 -Wall -Wextra" x.cpp\n') == [],
       "rx_filter explains its own quoting in prose, and the first version "
       "read that sentence as a build")
    ck("the testbench Makefile population is non-empty",
       len(testbench_makefiles()) > 50, f"found {len(testbench_makefiles())}")
    ck("the shared harness header exists", (REPO / HARNESS_HEADER).is_file())
    ck("the harness header copies agree", header_drift(paths) is None,
       str(header_drift(paths)))

    print(f"\n{checks} checks: {checks - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true", help="per-file counts")
    parser.add_argument("--write-budget", action="store_true",
                        help="re-record the ratchets at the measured counts")
    parser.add_argument("--selftest", action="store_true",
                        help="run the fixture arms")
    args = parser.parse_args()
    if args.selftest:
        return selftest()

    paths = sources()
    problem = population_problem(paths)
    if problem is not None:
        print(f"POPULATION: REFUSED - {problem}. The gate reads every tracked "
              f"first-party {'/'.join(SCANNED_SUFFIXES)} in this repository and in "
              f"{' and '.join(PROJECT_SUBMODULES)}. Refusing beats counting: a scan "
              f"over a missing tree reports zero of everything, and zero of "
              f"everything is a clean ratchet.", file=sys.stderr)
        return 2

    totals, per_file = audit(paths)

    if args.write_budget:
        return write_budget(totals)

    if args.list:
        width = max(len(p) for p in paths)
        for rel in paths:
            counts = per_file[rel]
            if any(counts.values()):
                summary = "  ".join(f"{k}={v}" for k, v in counts.items() if v)
                print(f"{rel.ljust(width)}  {summary}")
        print()

    findings = []
    for key in REFUSED:
        for rel in paths:
            if per_file[rel][key]:
                for line, snippet in sites((REPO / rel).read_text(errors="replace"),
                                           key, rel):
                    findings.append(
                        f"REFUSED {key.upper()}: {rel}:{line} — {snippet}. "
                        f"Rule 11 in docs/development/CODE_QUALITY.md names the "
                        f"construct that replaces it.")

    drift = header_drift(paths)
    if drift is not None:
        findings.append(
            f"REFUSED HEADER DRIFT: {drift}. The shared harness header is one "
            f"file with three copies; copy it, do not edit the copy.")

    budget_failures, notes = ratchet(totals, read_budget())

    for line in findings + budget_failures:
        print(line, file=sys.stderr)
    if findings or budget_failures:
        return 1

    print(f"cpp idiom: {len(paths)} first-party translation units, "
          f"{sum(1 for p in paths if is_c(p))} of them C")
    for key in REFUSED:
        print(f"  {key}: 0")
    budget = read_budget()
    for key in RATCHETED:
        print(f"  {key}: {totals[key]} <= {budget[key]}")
    for note in notes:
        print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
