#!/usr/bin/env python3
"""Classify a changed-file list as docs-only or RTL/tooling relevant.

A submodule pointer is never docs-only. The gitlink entries (`protocol-processor`,
`gptp-processor`, `external`, `third_party/...`) and `.gitmodules` itself move
the RTL the sweep elaborates without touching a file under `hdl/`, so they are
read from `.gitmodules` and classified relevant before any documentation rule
is consulted ([R1] on PR #204). Without `.gitmodules` the rule has nothing to
read and the documentation rules alone decide, which still classifies a bare
gitlink path as relevant because it carries no documentation suffix.

Documentation is a path no gate that the docs-only path skips reads without
`docs-check` reading it too (#444, [R197] F2): a top-level `*.md`, anything
under `LICENSES/`, or a `*.md`, `*.drawio`, `*.svg` or `*.png` under `docs/`
other than the pages in GATE_READ_DOCS. Everything else is relevant whatever its suffix: every file
under `tb/`, `hdl/`, `sw/`, `syn/`, `scripts/`, `tests/` and `configs/` (the
campaign records under `hdl/**/doc/` are read by the tsn_fuzz suite), and
every generator, manifest and budget under `docs/`. A page some skipped gate
also reads stays documentation only where an always-run docs.yml job runs
the same check on it; the policy page names each reader.

The list a classifier-gated workflow hands in names BOTH sides of a rename:
each builds it with `git diff --no-renames --name-only` ([R198] N2), so
renaming a file a skipped gate reads to a documentation path is relevant
through its source side, as a deletion is through its own path.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Sequence

#: LISTS, not tuples, for the same reason as SUBMODULE_PATHS below: the
#: selftest's mutation arm edits the real rule table in place.
#: Everything below one of these prefixes is documentation.
DOC_PREFIXES = ["LICENSES/"]
#: Under `docs/`, prose and the diagram assets are documentation; a
#: generator, a manifest or a budget beside them is not.
DOCS_TREE = "docs/"
DOCS_TREE_SUFFIXES = [".md", ".drawio", ".svg", ".png"]
#: At the top level, prose only.
TOP_LEVEL_SUFFIXES = [".md"]
#: Pages under `docs/` that Python in GATED_PY_ROOTS names, so a gate the
#: docs-only path skips may read them. Not a list written from memory: the
#: selftest derives the same set from the tree and refuses any difference.
#: The behave suite (rtl-fast's `bdd-conformance`, which docs.yml never runs)
#: asserts on the first two; the third is the page the trace catalogue
#: generator's `--check` compares.
GATE_READ_DOCS = [
    "docs/reference/REGISTER_MAP.md",
    "docs/reference/TRACE_EVENTS.md",
    "docs/testing/MILAN_V12_AUDIT_2026-08-16.md",
]
#: Where the classifier-gated jobs run code that no docs.yml job runs. The
#: selftest scans the Python, the Makefiles and the shell there for a
#: documentation path, in the spellings this tree uses (#444, [R197] F5,
#: [R198] N3): a whole path, a path a literal ENDS in, and a bare file name
#: left by an `os.path.join` piece, a pathlib join or a `$(DOCS)/NAME.md`
#: recipe. What it cannot see is stated with the rule on the policy page.
#: test_builder.py is left out because docs.yml's `docs-check` runs it on
#: every pull request, every arm that reads a page included;
#: `--require-elaboration` in `elaborate` changes only how a skipped LiteX
#: arm is graded.
GATED_ROOTS = ("tests", "tb", "syn", "sw", "hdl", "avdecc")
GATED_SUFFIXES = (".py", ".sh", ".mk")
GATED_NAMES = ("Makefile",)
DOCS_JOB_PY = ("sw/builder/test_builder.py",)

ROOT = pathlib.Path(__file__).resolve().parent.parent
GITMODULES = ROOT / ".gitmodules"


def submodule_paths(gitmodules: pathlib.Path = GITMODULES) -> tuple[str, ...]:
    """The `path = ...` entries of .gitmodules, derived rather than listed."""
    try:
        text = gitmodules.read_text(encoding="utf-8")
    except OSError:
        return ()
    return tuple(m.group(1).strip()
                 for m in re.finditer(r"^\s*path\s*=\s*(\S+)", text, re.M))


#: The rule table `is_submodule_path` consults. A LIST, not a tuple, so the
#: selftest's mutation arm can edit the real table in place: rebinding a
#: module global from inside a function needs a `global` statement, and the
#: arm binds nothing at all if it mutates a copy instead.
SUBMODULE_PATHS = list(submodule_paths()) + [".gitmodules"]


def is_submodule_path(clean: str) -> bool:
    """Whether a path is a gitlink or lives under one, checked before any doc rule."""
    return (clean in SUBMODULE_PATHS
            or clean.startswith(tuple(p + "/" for p in SUBMODULE_PATHS)))


def is_doc_only_path(path: str) -> bool:
    """Whether one changed path carries documentation and nothing a skipped
    gate reads.

    A submodule pointer is excluded first: it names no suffix of its own, so
    the documentation rules alone would let a moved gitlink pass as prose.
    """
    clean = path.strip()
    while clean.startswith("./"):
        clean = clean[2:]
    if not clean:
        return True
    if is_submodule_path(clean) or clean in GATE_READ_DOCS:
        return False
    if clean.startswith(tuple(DOC_PREFIXES)):
        return True
    if clean.startswith(DOCS_TREE):
        return clean.endswith(tuple(DOCS_TREE_SUFFIXES))
    return "/" not in clean and clean.endswith(tuple(TOP_LEVEL_SUFFIXES))


_LITERAL = re.compile(r"""(["'])([^"'\n]*)\1""")
_DOCS_JOIN = re.compile(r"""(["'])docs\1((?:\s*/\s*(["'])[^"'\n]+\3)+)""")
_SEGMENT = re.compile(r"""["']([^"'\n]+)["']""")
#: A quoted string in a recipe or a shell line, the words left once those are
#: taken out, and the marks that stand in for a directory a variable holds.
_QUOTED = re.compile(r"""(["'])(.*?)\1""")
_SHELL_WORDS = re.compile(r"""[\s;:=()<>|&,]+""")
_PLACEHOLDER = re.compile(r"""[{$%]""")


def gated_files(root: pathlib.Path = ROOT) -> list[str]:
    """The Python, Makefile and shell files under GATED_ROOTS, tracked ones
    when git can say, else whatever the tree holds (the no-git docs job runs
    this too)."""
    run = subprocess.run(["git", "-C", str(root), "ls-files", "--",
                          *GATED_ROOTS], capture_output=True, text=True,
                         check=False)
    if run.returncode == 0 and run.stdout.strip():
        found = run.stdout.split()
    else:
        found = [p.relative_to(root).as_posix() for r in GATED_ROOTS
                 for p in (root / r).rglob("*") if p.is_file()]
    return sorted(p for p in found
                  if (p.endswith(GATED_SUFFIXES)
                      or p.rsplit("/", 1)[-1] in GATED_NAMES)
                  and p not in DOCS_JOB_PY)


def documentation_files(root: pathlib.Path = ROOT) -> list[str]:
    """Every documentation-class page the tree holds, gate-read pages
    included: what a gated module must not be able to name unnoticed."""
    run = subprocess.run(["git", "-C", str(root), "ls-files"],
                         capture_output=True, text=True, check=False)
    if run.returncode == 0 and run.stdout.strip():
        found = run.stdout.split()
    else:
        found = [p.relative_to(root).as_posix() for p in root.glob("*.md")]
        for place in [DOCS_TREE, *DOC_PREFIXES]:
            found += [p.relative_to(root).as_posix()
                      for p in (root / place).rglob("*") if p.is_file()]
    return sorted(p for p in found
                  if p in GATE_READ_DOCS or is_doc_only_path(p))


def pages_named_by_fragment(fragment: str, by_path: frozenset[str],
                            by_name: dict[str, list[str]]) -> list[str]:
    """The documentation pages one path-shaped fragment of source names.

    Three spellings resolve: the page's own path, a path that ENDS in it (a
    relative literal, or an f-string whose head is a variable), and a bare
    file name, which is what an `os.path.join` piece, a pathlib join and a
    `$(DOCS)/NAME.md` recipe leave behind. A bare name resolves only where
    the directory is absent or is itself a variable, so a fragment naming a
    real directory elsewhere in the tree names that file and not its
    namesake under `docs/`. A fragment holding a blank is prose, not a path.
    """
    frag = fragment.strip()
    if not frag or any(char.isspace() for char in frag):
        return []
    while frag.startswith("./"):
        frag = frag[2:]
    if frag in by_path:
        return [frag]
    ends = sorted(page for page in by_path if frag.endswith("/" + page))
    if ends:
        return ends
    head, _, name = frag.rpartition("/")
    if name in by_name and (not head or _PLACEHOLDER.search(head)):
        return by_name[name]
    return []


def path_fragments(line: str, python: bool) -> list[str]:
    """The path-shaped fragments one source line offers. Python offers its
    string literals and its `"docs" / ...` joins; a recipe or a shell line
    offers its words, less any quoted string holding a blank, which is a
    message rather than a path."""
    if python:
        found = [m.group(2) for m in _LITERAL.finditer(line)]
        return found + ["docs/" + "/".join(_SEGMENT.findall(m.group(2)))
                        for m in _DOCS_JOIN.finditer(line)]
    found, rest, end = [], [], 0
    for m in _QUOTED.finditer(line):
        rest.append(line[end:m.start()])
        end = m.end()
        if not any(char.isspace() for char in m.group(2)):
            found.append(m.group(2))
    rest.append(line[end:])
    return found + _SHELL_WORDS.split(" ".join(rest))


def docs_named_by_gated_code(root: pathlib.Path = ROOT) -> dict[str, str]:
    """Each documentation page a gated module names, mapped to the first
    `file:line` that names it. Comment lines are skipped, and a page cited
    inside a message is prose rather than a read."""
    pages = documentation_files(root)
    by_path = frozenset(pages)
    by_name: dict[str, list[str]] = {}
    for page in pages:
        by_name.setdefault(page.rsplit("/", 1)[-1], []).append(page)
    named: dict[str, str] = {}
    for rel in gated_files(root):
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        python = rel.endswith(".py")
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            for fragment in path_fragments(line, python):
                for page in pages_named_by_fragment(fragment, by_path,
                                                    by_name):
                    named.setdefault(page, f"{rel}:{n}")
    return named


def is_rtl_relevant(paths: Iterable[str]) -> bool:
    """Whether a changed-file list can move the RTL, so the heavy jobs must run."""
    changed = [path.strip() for path in paths if path.strip()]
    # An empty diff is treated conservatively. A broken base selection must not
    # turn a real change into a docs-only green.
    return not changed or any(not is_doc_only_path(path) for path in changed)


Case = tuple[list[str], bool]


def _cases() -> list[Case]:
    """The classification table: changed paths and whether they are RTL
    relevant."""
    return [
        (["docs/testing/CI_WORKFLOWS.md"], False),
        (["README.md", "AGENTS.md"], False),
        (["LICENSES/CERN-OHL-W-2.0.txt"], False),
        (["docs/diagrams/x.drawio", "docs/diagrams/x.svg",
          "docs/diagrams/x.png"], False),
        # #444 ([R197] F2): nothing a skipped gate reads is documentation.
        # The campaign records check_results_fresh.py compares in tsn_fuzz.
        (["hdl/ieee1722/avtp/doc/TEST_RESULTS.md"], True),
        (["hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md"], True),
        # The pages the behave suite and the trace generator read.
        (["docs/reference/REGISTER_MAP.md"], True),
        (["docs/testing/MILAN_V12_AUDIT_2026-08-16.md"], True),
        (["docs/reference/TRACE_EVENTS.md"], True),
        # Under docs/, a generator, a manifest, a budget or other non-prose.
        (["docs/traceability/gen_module_matrix.py"], True),
        (["docs/diagrams/PNG_MANIFEST.json"], True),
        (["docs/traceability/untested.budget"], True),
        (["docs/notes.txt"], True),
        # Outside docs/, a test bench README and the diagram assets.
        (["tb/verilator/milan_dp/README.md"], True),
        (["hdl/ieee1722/aaf/doc/x.svg"], True),
        (["cdc_census.drawio"], True),
        (["cdc_census.svg"], True),
        (["docs/x.md", "hdl/ieee1722/avtp/doc/TEST_RESULTS.md"], True),
        # #444 ([R198] N2): a rename reaches the classifier as both of its
        # sides, because every gated workflow builds the list with
        # `git diff --no-renames --name-only`. The source side is what
        # decides: a gate-read page or an RTL source renamed to a
        # documentation path is relevant, and so is a deletion.
        (["docs/testing/MILAN_V12_AUDIT_2026-10-01.md",
          "docs/testing/MILAN_V12_AUDIT_2026-08-16.md"], True),
        (["docs/design/KL_pp_shadow.md", "hdl/milan/KL_pp_shadow.sv"], True),
        (["hdl/milan/KL_pp_shadow.sv"], True),
        # #444: outside the documentation classes nothing is documentation.
        ([".github/ISSUE_TEMPLATE/task.yml"], True),
        (["LICENSE"], True),
        (["notes.rst"], True),
        (["docs/x.md", "hdl/ieee1722/aaf/doc/x.svg.in"], True),
        (["requirements.txt"], True),
        (["hdl/milan/milan_datapath.sv"], True),
        (["scripts/lint_rtl.py"], True),
        ([".github/workflows/rtl.yml"], True),
        (["docs/x.md", "tb/verilator/cdc/Makefile"], True),
        ([], True),
        # Submodule pointers move RTL without a file under hdl/ ([R1], PR #204).
        (["gptp-processor"], True),
        (["protocol-processor"], True),
        (["external"], True),
        (["third_party/verilog-axis"], True),
        ([".gitmodules"], True),
        (["docs/x.md", "gptp-processor"], True),
    ]


def _gate_read_arms() -> int:
    """#444 ([R197] F2): the gate-read table is derived, not remembered. The
    pages the gated Python names must be exactly the pages the table files
    as relevant. Returns the failure count."""
    failures = 0
    named = docs_named_by_gated_code()
    for page in sorted(set(named) | set(GATE_READ_DOCS)):
        where = named.get(page, "no gated module")
        ok = page in named and page in GATE_READ_DOCS
        print(f"  {'ok  ' if ok else 'FAIL'} gate-read page {page} "
              f"(named at {where}) is relevant")
        failures += 0 if ok else 1
    return failures


#: #444 ([R197] F5, [R198] N3): the page a planted reader names. It is
#: documentation until a gated module names it, so a spelling the scan misses
#: files it as documentation with every arm green, and a later docs-only diff
#: edits the input of a gate that skips.
NEW_PAGE = "docs/reference/EGRESS_QUEUE_MAP.md"
NEW_TOP_PAGE = "QUICKSTART.md"
NEW_PAGE_NAME = NEW_PAGE.rsplit("/", 1)[-1]
NEW_READER_PY = "tb/tools/new_reader.py"
NEW_READER_MK = "tb/verilator/new_suite/Makefile"
NEW_READER_SH = "syn/yosys/new_reader.sh"


def _reader_spellings() -> list[tuple[str, str, str, tuple[str, ...]]]:
    """Every way this tree's idioms name a page: the title, the file the
    planted reader lands in, its text, and the pages the scan must name. The
    last three are mentions rather than reads and must name nothing, or the
    table fills with prose."""
    return [
        ("a whole path literal", NEW_READER_PY,
         f'TEXT = open("{NEW_PAGE}").read()\n', (NEW_PAGE,)),
        ("a pathlib join of literals", NEW_READER_PY,
         f'TEXT = (ROOT / "docs" / "reference" / "{NEW_PAGE_NAME}").read_text()\n',
         (NEW_PAGE,)),
        ("os.path.join of its pieces", NEW_READER_PY,
         f'TEXT = open(os.path.join(ROOT, "docs", "reference", "{NEW_PAGE_NAME}"))\n',
         (NEW_PAGE,)),
        ("a docs directory constant joined later", NEW_READER_PY,
         'DOCS = ROOT / "docs"\n'
         f'TEXT = (DOCS / "reference" / "{NEW_PAGE_NAME}").read_text()\n',
         (NEW_PAGE,)),
        ("an f-string over a directory variable", NEW_READER_PY,
         f'TEXT = open(f"{{DOCS}}/reference/{NEW_PAGE_NAME}").read()\n',
         (NEW_PAGE,)),
        ("an f-string over a literal directory", NEW_READER_PY,
         f'TEXT = open(f"{{ROOT}}/{NEW_PAGE}").read()\n', (NEW_PAGE,)),
        ("a relative literal", NEW_READER_PY,
         f'TEXT = open("../../{NEW_PAGE}").read()\n', (NEW_PAGE,)),
        ("a join wrapped over two lines", NEW_READER_PY,
         "TEXT = (DOCS_DIR /\n"
         f'        "{NEW_PAGE_NAME}").read_text()\n', (NEW_PAGE,)),
        ("a bare file name handed to a helper", NEW_READER_PY,
         f'TEXT = read_page(DOCS_DIR, "{NEW_PAGE_NAME}")\n', (NEW_PAGE,)),
        ("a top-level page as a whole literal", NEW_READER_PY,
         f'TEXT = open("{NEW_TOP_PAGE}").read()\n', (NEW_TOP_PAGE,)),
        ("a recipe reading it through a directory variable", NEW_READER_MK,
         f"check:\n\tpython3 compare.py $(DOCS)/{NEW_PAGE_NAME}\n", (NEW_PAGE,)),
        ("a recipe reading its whole path", NEW_READER_MK,
         f"check:\n\tdiff -q {NEW_PAGE} $(OUT)\n", (NEW_PAGE,)),
        ("a shell line reading it", NEW_READER_SH,
         f'cat "{NEW_PAGE}" > "$OUT"\n', (NEW_PAGE,)),
        ("a comment naming it", NEW_READER_PY,
         f'# the procedure is in {NEW_PAGE}\nTEXT = ""\n', ()),
        ("a message naming it", NEW_READER_SH,
         f'echo "see {NEW_PAGE} for the procedure" >&2\n', ()),
        ("a reader docs-check runs too", DOCS_JOB_PY[0],
         f'TEXT = open("{NEW_PAGE}").read()\n', ()),
    ]


def _new_reader_arms() -> int:
    """#444 ([R197] F5, [R198] N3): plant a new reader of a documentation
    page in a scratch tree, one spelling at a time, and require the scan to
    name it. An empty `.git` keeps the walk, not this repository's index,
    from answering. Returns the failure count."""
    failures = 0
    for title, rel, text, want in _reader_spellings():
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / ".git").mkdir()
            for page in (NEW_PAGE, NEW_TOP_PAGE, rel):
                (root / page).parent.mkdir(parents=True, exist_ok=True)
                (root / page).write_text("page\n", encoding="utf-8")
            (root / rel).write_text(text, encoding="utf-8")
            named = sorted(docs_named_by_gated_code(root))
        ok = named == sorted(want)
        print(f"  {'ok  ' if ok else 'FAIL'} a new reader spelt as {title} "
              f"names {named or 'nothing'}")
        failures += 0 if ok else 1
    return failures


def _mutation_arms(cases: list[Case]) -> int:
    """A classifier whose rules file any one pointer, or any gate-read file,
    as documentation must be caught by the cases, or they bind nothing. The
    mutation edits the real rule tables, not a copy of the logic. Returns
    the failure count."""
    failures = 0
    pristine_paths, pristine_prefixes = list(SUBMODULE_PATHS), list(DOC_PREFIXES)
    pristine_tree = list(DOCS_TREE_SUFFIXES)
    pristine_top = list(TOP_LEVEL_SUFFIXES)
    pristine_read = list(GATE_READ_DOCS)
    try:
        for victim in ("gptp-processor", "protocol-processor", "external",
                       "third_party/verilog-axis", ".gitmodules"):
            SUBMODULE_PATHS[:] = [x for x in pristine_paths if x != victim]
            DOC_PREFIXES[:] = pristine_prefixes + [victim]
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            DOC_PREFIXES[:] = pristine_prefixes
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: {victim} filed "
                  "as docs-only is rejected")
            failures += 0 if caught else 1
        # #444: each widening of the documentation classes, among them each
        # gate-read file filed back as documentation ([R197] F2), is caught
        # by a case.
        for table, widened in (
                (DOC_PREFIXES, ".github/ISSUE_TEMPLATE/"),
                (DOC_PREFIXES, "LICENSE"),
                (TOP_LEVEL_SUFFIXES, ".rst"),
                (DOC_PREFIXES, "docs/"),
                (DOC_PREFIXES, "hdl/ieee1722/avtp/doc/"),
                (DOC_PREFIXES, "hdl/ieee8021as/gptp_plane/doc/"),
                (DOC_PREFIXES, "tb/"),
                (DOCS_TREE_SUFFIXES, ".py"),
                (DOCS_TREE_SUFFIXES, ".json"),
                (TOP_LEVEL_SUFFIXES, ".svg")):
            table.append(widened)
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            table.remove(widened)
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: {widened} filed "
                  "as docs-only is rejected")
            failures += 0 if caught else 1
        for page in pristine_read:
            GATE_READ_DOCS.remove(page)
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            derived = docs_named_by_gated_code()
            GATE_READ_DOCS[:] = pristine_read
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: gate-read "
                  f"{page} filed as docs-only is rejected")
            failures += 0 if caught else 1
            ok = page in derived
            print(f"  {'ok  ' if ok else 'FAIL'} mutation: the scan still "
                  f"names {page} once the table drops it")
            failures += 0 if ok else 1
    finally:
        SUBMODULE_PATHS[:] = pristine_paths
        DOC_PREFIXES[:] = pristine_prefixes
        DOCS_TREE_SUFFIXES[:] = pristine_tree
        TOP_LEVEL_SUFFIXES[:] = pristine_top
        GATE_READ_DOCS[:] = pristine_read
    return failures


def selftest() -> int:
    """Prove the classification table, the derived gate-read table, and that
    dropping any one submodule pointer or gate-read file from the rules is
    caught by a case; 0 when every arm holds."""
    cases = _cases()
    failures = 0
    for paths, expected in cases:
        got = is_rtl_relevant(paths)
        ok = got == expected
        print(f"  {'ok  ' if ok else 'FAIL'} {paths!r}: rtl={got}")
        failures += 0 if ok else 1

    # The submodule rule is derived from .gitmodules, so prove the derivation
    # saw the tree: every pointer this repository carries must be listed.
    for want in ("protocol-processor", "gptp-processor", "external",
                 "third_party/verilog-axis", ".gitmodules"):
        ok = want in SUBMODULE_PATHS
        print(f"  {'ok  ' if ok else 'FAIL'} submodule rule names {want}")
        failures += 0 if ok else 1

    failures += _gate_read_arms() + _new_reader_arms() + _mutation_arms(cases)
    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return 1 if failures else 0


def main(argv: Sequence[str]) -> int:
    """Classify the paths given on argv or read from stdin, printing true/false."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv[1:])
    if args.selftest:
        return selftest()
    paths = args.paths or [line.rstrip("\n") for line in sys.stdin]
    print("true" if is_rtl_relevant(paths) else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
