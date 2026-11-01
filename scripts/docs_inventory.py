#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Documentation inventory: generate docs/DOCUMENTATION_AUDIT.md and gate its freshness (#797).

Why this exists. #797 asks for an audit that lists every Markdown document and README with its purpose,
audience, the code or specification it describes and a status, regenerated from the files rather than
written by hand. The hand-written page it replaced described 54 suites and 14 features long after both moved.

What is read from the files, and what this script owns:

  * the population is every tracked `*.md` file and every tracked README (`git ls-files`; a filesystem walk
    when the tree has no Git metadata);
  * the area is the page's directory, the line count is the page's own;
  * the purpose is the page's first `#` heading;
  * what a page describes is counted from the repository paths and the standards it cites, so it moves when
    the page does;
  * the audience comes from an `Audience:` line in the page's first lines, or else from `AUDIENCES`, a
    mapping table this script owns;
  * the status is decided by `status()`, each with its evidence: `obsolete` for the versioned archive,
    `superseded` for a page carrying a supersession banner (or a judgement recorded in the data file),
    `stale` for a page with a recorded verified contradiction, `current` otherwise.

The status rule (#797): a page with an open finding is never current; it renders stale. `--check` also fails
when the committed page marks current a page its own Findings table lists, so a generator that lost the rule fails.

The verified contradictions live in `scripts/docs_inventory.json`. Each one quotes the statement exactly, so
the generator finds its line at every head; a quote that is no longer on its page is rendered as needing
re-verification rather than silently dropped, and an area lane that fixes a statement removes its entry in the
same change, once no copy row of it remains.

The cross-page rule (#797): every recorded statement, and each spelling its entry lists under `also`, is
searched across every inventoried page, normalised for case, line wrapping, list and quote markers, emphasis
and code spans. Each other page carrying it gets its own Findings row, so the status rule applies there too.
A paraphrase is found only once `also` records its spelling.

What `--check` sees: the committed page against a fresh render. A document added or removed, or edited in
its line count, title, audience line, cited paths or standards, or in a quoted finding statement, makes the
page stale. An edit that changes none of those renders the same page and passes; the gate ties the inventory
to the files, not every sentence to its source.

Usage: python3 scripts/docs_inventory.py --write | --check | --selftest | --findings-dir DIR

Exit status: 0 fresh or written, 1 stale or a failed control, 2 refused (bad data, arguments or population).
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import unicodedata
from bisect import bisect_right
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = "docs/DOCUMENTATION_AUDIT.md"
DATA = "scripts/docs_inventory.json"
STATUSES = ("current", "stale", "superseded", "obsolete")
ARCHIVE_PREFIX = "docs/history/"
ARCHIVE_INDEX = "docs/history/v1/README.md"
EM_DASH = "—"

#: Directories whose paths a page can cite as "the code it describes".
CODE_ROOTS = ("hdl", "sw", "tb", "syn", "configs", "scripts", "avdecc", "tests", "ci", "tools",
              "protocol-processor", "gptp-processor", "third_party")
#: The module directories #797 requires a README in, with their first level.
MODULE_ROOTS = ("hdl", "sw", "tb", "syn", "configs", "scripts")
#: Where a two-component directory is too coarse to say what a page describes.
DEEPER = ("tb/verilator", "sw/firmware", "hdl/common", "hdl/ieee1722", "hdl/ieee17221",
          "hdl/ieee8021as", "hdl/ieee8021q", "hdl/milan")
CITED_PATH_RE = re.compile(r"(?<![\w./-])((?:%s)/[\w./+-]*[\w+-])" % "|".join(re.escape(r) for r in CODE_ROOTS))
LINK_TARGET_RE = re.compile(r"\]\(([^)\s#]+)")
#: The six clause families #797 cites, in the order the page lists them.
STANDARDS = (
    ("Milan v1.2", re.compile(r"\bMilan v?1\.2\b|\bMilan (?:Section |section )?\d+\.\d+")),
    ("1722.1-2021", re.compile(r"\b1722\.1\b")),
    ("1722-2016", re.compile(r"\b1722(?!\.1)(?:-2016)?\b")),
    ("802.1Q", re.compile(r"\b802\.1Q")),
    ("802.1AS", re.compile(r"\b802\.1AS\b")),
    ("802.1BA", re.compile(r"\b802\.1BA\b")),
)
#: The release-facing pages #797 verifies statement by statement: the README,
#: `docs/README.md`, guides, integration, reference, `REQUIREMENTS.md` and `FR_NFR.md`.
RELEASE_FACING = re.compile(r"README\.md|REQUIREMENTS\.md|docs/README\.md|docs/(guides|integration|reference)/.*")
#: The area lane that owns each page in the sweep, first match wins.
LANES = (
    (r"docs/history/.*", "archive"),
    (r"(AGENTS|CONTRIBUTING|CHANGELOG)\.md|docs/DOCUMENTATION_AUDIT\.md", "repository contract"),
    (r"(README|QUICKSTART)\.md|docs/(README|GLOSSARY|DOC_GENERATION)\.md", "overview and guides"),
    (r"docs/(guides|overview|limitations|diagrams)/.*", "overview and guides"),
    (r"(REQUIREMENTS|THIRD_PARTY)\.md|docs/(reference|integration|traceability)/.*", "reference"),
    (r"docs/(design|fpga|litex)/.*|docs/[A-Z0-9_]+\.md", "design"),
    (r"docs/(testing|development)/.*|\.github/.*", "testing and CI"),
    (r"docs/findings/.*", "findings"),
    (r"(hdl|sw|tb|syn|tests|avdecc|configs|scripts)/.*|docs/templates/.*", "module READMEs"),
)
#: The issue's five audiences, plus "all readers" for the entry pages.
AUDIENCES = (
    (r"(README|QUICKSTART|REQUIREMENTS)\.md|docs/(README|GLOSSARY)\.md|docs/overview/.*"
     r"|docs/guides/README\.md|docs/reference/(FR_NFR|MILAN_COMPLIANCE_MATRIX|MILAN_FEATURE_STATUS)\.md",
     "all readers"),
    (r"docs/integration/BAREMETAL_FIRMWARE\.md|docs/reference/(MAILBOX_CONTRACT|TRACE_EVENTS)\.md"
     r"|sw/(firmware|trace|mailbox)/.*|docs/design/(TRACE_LOGGING|MAILBOX_SPLIT|SPLIT_CONTROL_MEMORY)\.md"
     r"|docs/ARCHITECTURE_HW_SW_SPLIT\.md", "firmware developer"),
    (r"docs/guides/(gptp/)?SYSTEM_INTEGRATOR\.md|docs/integration/.*|docs/litex/.*|THIRD_PARTY\.md"
     r"|docs/reference/.*|sw/(README|builder/README-parameters)\.md|avdecc/.*", "integrator"),
    (r"docs/guides/(BOARD_DEPLOYMENT|PROJECT_MANAGER|gptp/MANAGER)\.md|docs/findings/.*"
     r"|docs/limitations/TROUBLESHOOTING\.md|docs/testing/(MILAN_V12_AUDIT_2026-08-16|726_STREAM_COUNTERS)\.md",
     "bench/qualification"),
    (r"docs/guides/(VERIFICATION_DEVELOPER|gptp/TEST_DEVELOPER)\.md|docs/(testing|traceability|templates)/.*"
     r"|tb/.*|tests/.*|hdl/.*(README-tests|TEST_RESULTS)\.md", "verification"),
    (r".*", "maintainer"),
)
AUDIENCE_LINE_RE = re.compile(r"^\**Audience\**:\**\s*(.+?)\s*$", re.IGNORECASE)
#: The markers a generated page carries in its first lines, as this tree spells them; a page that
#: merely mentions generated artifacts is not one.
GENERATED_RE = re.compile(r"\*\*GENERATED\b|<!-- GENERATED\b|^Generated by\b|do not hand-?edit|DO NOT EDIT",
                          re.MULTILINE | re.IGNORECASE)
GENERATOR_RE = re.compile(r"`?((?:scripts|sw|docs|tb|avdecc)/[\w./-]+\.py)`?")
BANNER_RE = re.compile(r"\b(superseded|deprecated|replaced)\b[^\n]*\]\(([^)\s#]+)", re.IGNORECASE)
SUCCESSOR_RE = re.compile(r"^> Current successor: \[[^\]]+]\(([^)]+)\)$", re.MULTILINE)
HEADING_RE = re.compile(r"^#\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
BANNER_SCAN_LINES = 15
#: What a copy of a statement may differ by at the start of a line, and inside it.
LINE_MARKER_RE = re.compile(r"^\s*(?:>\s*)*(?:[-*+]\s+|\d+\.\s+)?")
INLINE_MARKUP_RE = re.compile(r"[`*]")
#: The variables that point Git at another repository than the `-C` directory. A Git hook sets
#: them, and the self-test's fixture must never write to, or list, the repository running it.
GIT_LOCATION = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE", "GIT_PREFIX")
#: An inventory or Findings row: the first cell of one, the second of the other, links a page.
ROW_LINK_RE = re.compile(r"^\[(.+?)(?: \(historical\))?\]\([^)]*\)$")
#: The first lines of the generated page, which also stand for its own row.
OWN_HEAD = ("# Documentation audit", "",
            "**GENERATED** by `scripts/docs_inventory.py` from the tracked documents.",
            "Do not hand-edit.")


@dataclass(frozen=True)
class Finding:
    """One verified contradiction: the exact statement and what contradicts it."""

    ident: str
    page: str
    quote: str
    source: str
    correction: str
    also: tuple[str, ...] = ()
    #: The page the statement is recorded on, when this row is a copy found on another page.
    origin: str = ""


@dataclass(frozen=True)
class Page:
    """Everything the inventory row says about one document."""

    path: str
    area: str
    lines: int
    audience: str
    purpose: str
    describes: str
    status: str
    evidence: str
    verified: str
    lane: str


@dataclass(frozen=True)
class Tree:
    """The tracked listing every column is derived from, so no column reads the disk's extras.

    A cited directory is judged against the TRACKED directories, and a path
    inside a submodule stands for that submodule, so the page renders the same
    with or without the submodules initialised and with or without build
    output lying in the checkout.
    """

    root: Path
    files: tuple[str, ...]
    directories: frozenset[str]
    submodules: tuple[str, ...]


class Refusal(Exception):
    """A population or data file the generator will not render (exit 2)."""


def first_match(table: tuple[tuple[str, str], ...], path: str) -> str:
    """The value of the first rule whose pattern matches the whole path."""
    for pattern, value in table:
        if re.fullmatch(pattern, path):
            return value
    return "unassigned"


def is_document(path: str) -> bool:
    """A Markdown file or a README of any extension."""
    name = PurePosixPath(path).name
    return path.endswith(".md") or name.upper().startswith("README")


def git_environment() -> dict[str, str]:
    """This process's environment without the variables that redirect Git elsewhere."""
    return {name: value for name, value in os.environ.items() if name not in GIT_LOCATION}


def listing(root: Path) -> Tree:
    """Every tracked file (`git ls-files`), or a walk that skips submodules without Git."""
    modules = tuple(sorted(re.findall(r"^\s*path\s*=\s*(\S+)", (root / ".gitmodules").read_text(),
                                      re.MULTILINE))) if (root / ".gitmodules").is_file() else ()
    if (root / ".git").exists():
        listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True,
                                text=True, check=False, env=git_environment())
        if listed.returncode != 0:
            raise Refusal("git ls-files failed: " + listed.stderr.strip())
        paths = [p for p in listed.stdout.split("\0") if p and p not in modules]
    else:
        paths = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
        paths = [p for p in paths if not p.startswith(".git/")
                 and not any(p == m or p.startswith(m + "/") for m in modules)]
    directories = {str(parent) for path in paths for parent in PurePosixPath(path).parents if str(parent) != "."}
    return Tree(root, tuple(sorted(paths)), frozenset(directories), modules)


def population(tree: Tree) -> list[str]:
    """Every tracked document present on disk, and the audit page itself."""
    found = sorted({p for p in tree.files if is_document(p) and (tree.root / p).is_file()} | {OUTPUT})
    if found == [OUTPUT]:
        raise Refusal("the document population is empty")
    return found


def line_count(text: str) -> int:
    """Lines as `wc -l` counts them, plus an unterminated last line."""
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def cell(text: str) -> str:
    """Text safe inside one table cell: no pipe, no newline, no em dash."""
    return " ".join(text.replace(EM_DASH, "-").replace("|", "\\|").split())


def purpose_of(text: str, path: str) -> str:
    """The page's first level-one heading outside a fence, else its file name."""
    fenced = False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        match = None if fenced else HEADING_RE.match(line)
        if match:
            return cell(re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", match.group(1)))
    return cell(PurePosixPath(path).name)


def audience_of(text: str, path: str) -> str:
    """The page's own `Audience:` line, else the mapping table's answer."""
    for line in text.split("\n")[:BANNER_SCAN_LINES]:
        match = AUDIENCE_LINE_RE.match(line.strip())
        if match:
            return cell(match.group(1))
    return first_match(AUDIENCES, path)


def relative(target: PurePosixPath, start: PurePosixPath) -> str:
    """`target` as a link written from directory `start`, both repo-relative."""
    return posixpath.relpath(str(target), str(start))


def normalise(base: PurePosixPath, ref: str) -> str | None:
    """A link target resolved against the page's directory, repo-relative, or None outside it."""
    parts: list[str] = list(base.parts)
    for part in PurePosixPath(ref).parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts) if parts else None


def directory_of(tree: Tree, path: str) -> str | None:
    """The tracked directory a cited path stands for, at the depth that says something."""
    for module in tree.submodules:
        if path == module or path.startswith(module + "/"):
            return module
    parts = PurePosixPath(path).parts
    if not parts or parts[0] not in CODE_ROOTS:
        return None
    depth = 3 if "/".join(parts[:2]) in DEEPER else 2
    for size in range(min(depth, len(parts)), 0, -1):
        candidate = "/".join(parts[:size])
        if candidate in tree.directories:
            return candidate
    return None


def describes_of(tree: Tree, text: str, path: str) -> str:
    """The three directories a page cites most, then the standards it cites."""
    base = PurePosixPath(path).parent
    cited: Counter[str] = Counter()
    own = directory_of(tree, base.as_posix())
    if own:
        cited[own] += 1000
    refs = [m.group(1) for m in CITED_PATH_RE.finditer(text)]
    refs += [r for r in (normalise(base, m.group(1)) for m in LINK_TARGET_RE.finditer(text)
                         if "://" not in m.group(1)) if r]
    for ref in refs:
        directory = directory_of(tree, ref)
        if directory:
            cited[directory] += 1
    top = sorted(cited.items(), key=lambda item: (-item[1], item[0]))[:3]
    names = ["`" + name + "`" for name, _ in top]
    names += [label for label, pattern in STANDARDS if pattern.search(text)]
    return ", ".join(names) if names else "--"


def load_data(root: Path, paths: list[str]) -> tuple[str, str, dict[str, tuple[str, str]], list[Finding]]:
    """The two baselines, the recorded judgements and findings; refuses a malformed file."""
    source = root / DATA
    if not source.is_file():
        return "--", "--", {}, []
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as error:
        raise Refusal(f"{DATA}: not valid JSON: {error}") from error
    known = set(paths)
    judged: dict[str, tuple[str, str]] = {}
    for page, entry in sorted(data.get("judged", {}).items()):
        if page not in known or entry.get("status") not in STATUSES or not entry.get("evidence"):
            raise Refusal(f"{DATA}: judged entry {page!r} needs a tracked page, a status and evidence")
        judged[page] = (entry["status"], entry["evidence"])
    findings: list[Finding] = []
    for entry in data.get("findings", []):
        fields = [entry.get(key, "") for key in ("id", "page", "quote", "source", "correction")]
        if not all(isinstance(value, str) and value.strip() for value in fields):
            raise Refusal(f"{DATA}: finding {entry.get('id')!r} needs id, page, quote, source and correction")
        if fields[1] not in known:
            raise Refusal(f"{DATA}: finding {fields[0]} names an untracked page {fields[1]}")
        also = entry.get("also", [])
        if not isinstance(also, list) or not all(isinstance(value, str) and value.strip() for value in also):
            raise Refusal(f"{DATA}: finding {fields[0]} needs `also` to be a list of statements")
        findings.append(Finding(*fields, tuple(also)))
    idents = Counter(f.ident for f in findings)
    duplicated = sorted(ident for ident, count in idents.items() if count > 1)
    if duplicated:
        raise Refusal(f"{DATA}: duplicate finding ids: {', '.join(duplicated)}")
    return str(data.get("verified_at", "--")), str(data.get("cited_at", "--")), judged, findings


def locate(text: str, quote: str) -> int | None:
    """The first line carrying the quoted statement, or None once it has left the page."""
    for number, line in enumerate(text.split("\n"), start=1):
        if quote in line:
            return number
    return None


def normal_form(text: str) -> str:
    """One line or statement without what a copy may differ by."""
    plain = INLINE_MARKUP_RE.sub("", LINE_MARKER_RE.sub("", unicodedata.normalize("NFKC", text)))
    return " ".join(plain.split()).casefold()


def flatten(text: str) -> tuple[str, list[int]]:
    """A page in normal form on one line, and each line's offset; a blank line leaves two spaces, a break."""
    flat = ""
    starts: list[int] = []
    for line in text.split("\n"):
        starts.append(len(flat))
        flat += normal_form(line) + " "
    return flat, starts


def carried_line(flat: tuple[str, list[int]], statement: str) -> int | None:
    """The line of a flattened page that starts the statement, whole words only, or None."""
    needle = normal_form(statement)
    if needle not in flat[0]:
        return None
    left = r"(?<!\w)" if needle[:1].isalnum() else ""
    right = r"(?!\w)" if needle[-1:].isalnum() else ""
    match = re.search(left + re.escape(needle) + right, flat[0])
    return bisect_right(flat[1], match.start()) if match else None


def copies(findings: list[Finding], texts: dict[str, str]) -> list[Finding]:
    """One row per finding and other page carrying its statement, unless a row there holds or is held by it."""
    flats = {path: flatten(text) for path, text in texts.items()}
    held: dict[str, list[str]] = {}
    for finding in findings:
        held.setdefault(finding.page, []).append(normal_form(finding.quote))
    rows = {(finding.ident, finding.page) for finding in findings}
    found: list[Finding] = []
    for finding in findings:
        for statement in (finding.quote, *finding.also):
            needle = normal_form(statement)
            for path, flat in flats.items():
                if (finding.ident, path) in rows or carried_line(flat, statement) is None:
                    continue
                if any(needle in words or words in needle for words in held.get(path, [])):
                    continue
                rows.add((finding.ident, path))
                held.setdefault(path, []).append(needle)
                found.append(Finding(finding.ident, path, statement, finding.source, finding.correction,
                                     origin=finding.page))
    return found


def archive_evidence(text: str, path: str) -> str:
    """The archive banner's successor, as a link from the audit page."""
    if path == ARCHIVE_INDEX:
        return "archive index, held by `scripts/check_archive.py`"
    match = SUCCESSOR_RE.search(text)
    if not match:
        return "versioned archive under `docs/history/`"
    target = normalise(PurePosixPath(path).parent, match.group(1))
    if not target:
        return "versioned archive under `docs/history/`"
    link = relative(PurePosixPath(target), PurePosixPath(OUTPUT).parent)
    return f"versioned archive; successor [{target}]({link})"


def status(text: str, path: str, judged: dict[str, tuple[str, str]]) -> tuple[str, str]:
    """(status, evidence) for one page before the status rule, by the rules in the module docstring."""
    if path.startswith(ARCHIVE_PREFIX):
        return ("current" if path == ARCHIVE_INDEX else "obsolete"), archive_evidence(text, path)
    if path in judged:
        return judged[path]
    head = "\n".join(text.split("\n")[:BANNER_SCAN_LINES])
    banner = BANNER_RE.search(head)
    if banner:
        line = head[:banner.start()].count("\n") + 1
        return "superseded", f"banner at line {line} names `{normalise(PurePosixPath(path).parent, banner.group(2))}`"
    generated = GENERATED_RE.search(head)
    if generated:
        tool = GENERATOR_RE.search(head)
        return "current", ("generated by `" + tool.group(1) + "`") if tool else "generated page"
    return "current", "no recorded contradiction"


def status_rule(state: str, evidence: str, page_findings: list[Finding]) -> tuple[str, str]:
    """#797's status rule: a page with an open finding is never current; it renders stale.

    It overrides every source of `current`: a recorded judgement, a generated
    page and the archive index alike. A superseded or obsolete page keeps its
    status, which already tells the reader not to trust it.
    """
    if page_findings and state == "current":
        return "stale", f"{len(page_findings)} finding(s): " + ", ".join(f.ident for f in page_findings)
    return state, evidence


def area_of(path: str) -> str:
    """The page's directory group: the top level, `docs/<part>` or `docs`."""
    parts = PurePosixPath(path).parts
    if len(parts) == 1:
        return "root"
    if parts[0] == "docs":
        return "docs" if len(parts) == 2 else "docs/" + parts[1]
    return parts[0]


def build(tree: Tree, paths: list[str],
          own_lines: int) -> tuple[list[Page], list[tuple[Finding, int | None]], str, str]:
    """Every row, every located finding, the statements' baseline and the citations' baseline.

    The audit page's own row is read from the header this script writes, never
    from the file on disk, so the row cannot depend on the page it is part of.
    """
    verified_at, cited_at, judged, findings = load_data(tree.root, paths)
    texts = {path: "\n".join(OWN_HEAD) if path == OUTPUT
             else (tree.root / path).read_text(encoding="utf-8", errors="replace") for path in paths}
    by_page: dict[str, list[Finding]] = {}
    for finding in findings + copies(findings, texts):
        by_page.setdefault(finding.page, []).append(finding)
    pages: list[Page] = []
    located: list[tuple[Finding, int | None]] = []
    for path, text in texts.items():
        page_findings = by_page.get(path, [])
        located += [(f, carried_line(flatten(text), f.quote) if f.origin else locate(text, f.quote))
                    for f in page_findings]
        state, evidence = status_rule(*status(text, path, judged), page_findings)
        if path.startswith(ARCHIVE_PREFIX):
            verified = "archive"
        elif RELEASE_FACING.fullmatch(path):
            verified = "D0"
        else:
            verified = "area lane"
        pages.append(Page(path, area_of(path), own_lines if path == OUTPUT else line_count(text),
                          audience_of(text, path), purpose_of(text, path), describes_of(tree, text, path),
                          state, evidence, verified, first_match(LANES, path)))
    return pages, located, verified_at, cited_at


def page_link(path: str) -> str:
    """A link to the page from the audit page; archive pages say they are historical."""
    link = relative(PurePosixPath(path), PurePosixPath(OUTPUT).parent)
    label = path + (" (historical)" if path.startswith(ARCHIVE_PREFIX) and path != ARCHIVE_INDEX else "")
    return f"[{label}]({link})"


def anchor(text: str) -> str:
    """GitHub's heading anchor for one of this page's own headings."""
    return re.sub(r"[^a-z0-9 _-]", "", text.lower()).replace(" ", "-")


def module_rows(tree: Tree, paths: list[str]) -> list[str]:
    """One row per module directory and first-level tracked subdirectory, with its README count."""
    readmes = {str(PurePosixPath(p).parent) for p in paths if PurePosixPath(p).name.upper().startswith("README")}
    rows = []
    for top in MODULE_ROOTS:
        if top not in tree.directories:
            continue
        children = sorted(d for d in tree.directories if str(PurePosixPath(d).parent) == top)
        for directory in [top] + children:
            inside = sorted(p for p in readmes if p == directory or p.startswith(directory + "/"))
            here = "yes" if directory in readmes else "no"
            rows.append(f"| `{directory}/` | {here} | {len(inside)} |")
    return rows


def summary_rows(pages: list[Page]) -> list[str]:
    """Counts by status, and by lane with each lane's status split."""
    rows = ["| Status | Pages | Lines |", "|---|---:|---:|"]
    for state in STATUSES:
        chosen = [p for p in pages if p.status == state]
        rows.append(f"| {state} | {len(chosen)} | {sum(p.lines for p in chosen):,} |")
    rows.append(f"| **total** | **{len(pages)}** | **{sum(p.lines for p in pages):,}** |")
    rows += ["", "| Lane | Pages | Current | Stale | Superseded | Obsolete | Verified by D0 |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for lane in sorted({p.lane for p in pages}):
        chosen = [p for p in pages if p.lane == lane]
        counts = " | ".join(str(sum(p.status == s for p in chosen)) for s in STATUSES)
        rows.append(f"| {lane} | {len(chosen)} | {counts} | {sum(p.verified == 'D0' for p in chosen)} |")
    return rows


RULES = (
    "| Status | Rule | Evidence shown |",
    "|---|---|---|",
    "| obsolete | The page is in the versioned archive under `docs/history/`. "
    "| The archive banner's current successor. |",
    "| superseded | A banner in the first 15 lines names a replacement, "
    "or the data file records the judgement. | The banner line or the recorded judgement. |",
    "| stale | The data file records a verified contradiction on the page, or the page carries a statement "
    "recorded on another page. A page with an open finding is never current, and the gate fails a committed "
    "page that says otherwise. | The finding identifiers. |",
    "| current | None of the above holds. | The page's generator, or no recorded contradiction. |",
)


def source_of(finding: Finding) -> str:
    """What contradicts the statement; a copy row says where the statement is recorded."""
    if finding.origin:
        return f"Copy of the {finding.ident} statement on `{finding.origin}`. {finding.source}"
    return finding.source


def render(tree: Tree, paths: list[str], own_lines: int = 0) -> str:
    """The whole audit page for one population."""
    pages, located, verified_at, cited_at = build(tree, paths, own_lines)
    areas = sorted({p.area for p in pages}, key=lambda a: (a != "root", a))
    out = list(OWN_HEAD) + ["",
           "Regenerate after any document change, then run the gate.", "",
           "```sh", "python3 scripts/docs_inventory.py --write",
           "python3 scripts/docs_inventory.py --check", "```", "",
           "## Contents", "",
           "- **[Summary](#summary)** -- Counts by status and by lane.",
           "- **[Status rules](#status-rules)** -- How each status is decided.",
           "- **[Module directories](#module-directories)** -- Which code directories carry a README.",
           "- **[Inventory](#inventory)** -- Every document, grouped by area.",
           "- **[Findings](#findings)** -- Verified contradictions, with their corrections.", "",
           "## Summary", "",
           f"Statements on D0 pages were checked at dev `{verified_at}`.",
           "Other pages wait for their area lane.", "",
           f"Findings cite source lines at dev `{cited_at}` and its submodule pins.", ""]
    out += summary_rows(pages)
    out += ["", "## Status rules", ""] + list(RULES)
    out += ["", "## Module directories", "",
            "The README count includes subdirectories.", "",
            "| Directory | README here | READMEs below |", "|---|---|---:|"] + module_rows(tree, paths)
    out += ["", "## Inventory", "", "Areas follow the directory tree.", ""]
    out += [f"- [{a}](#{anchor(a)}) ({sum(p.area == a for p in pages)})" for a in areas]
    for area in areas:
        out += ["", f"### {area}", "",
                "| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |",
                "|---|---:|---|---|---|---|---|---|---|"]
        out += [f"| {page_link(p.path)} | {p.lines} | {p.audience} | {p.purpose} | {p.describes} "
                f"| {p.status} | {cell(p.evidence)} | {p.verified} | {p.lane} |" for p in pages if p.area == area]
    out += ["", "## Findings", "",
            "Each statement is quoted exactly from its page.",
            "Its area lane fixes it.", "",
            "A copy row shows the recorded spelling.",
            "It names the recording page.", "",
            "Remove an entry once no copy row remains.",
            "An archive copy stays as written.", "",
            "| ID | Page | Line | Statement | Contradicted by | Correction |",
            "|---|---|---:|---|---|---|"]
    for finding, line in located:
        where = str(line) if line else "re-verify: quote not found"
        out.append(f"| {finding.ident} | {page_link(finding.page)} | {where} | {cell(finding.quote)} "
                   f"| {cell(source_of(finding))} | {cell(finding.correction)} |")
    if not located:
        out.append("| -- | -- | -- | No recorded finding. | -- | -- |")
    return "\n".join(out) + "\n"


def generate(root: Path) -> str:
    """The page with its own row's line count equal to its rendered length."""
    tree = listing(root)
    paths = population(tree)
    draft = render(tree, paths, 0)
    final = render(tree, paths, line_count(draft))
    if line_count(final) != line_count(draft):
        raise Refusal("the audit page's own line count did not settle")
    return final


def write_findings(root: Path, directory: Path) -> int:
    """One Markdown file per lane: page, line, statement, source, correction."""
    tree = listing(root)
    pages, located, verified_at, cited_at = build(tree, population(tree), 0)
    lanes = {p.path: p.lane for p in pages}
    directory.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[tuple[Finding, int | None]]] = {}
    for finding, line in located:
        grouped.setdefault(lanes[finding.page], []).append((finding, line))
    for lane, entries in sorted(grouped.items()):
        slug = re.sub(r"[^a-z0-9]+", "-", lane.lower()).strip("-")
        body = [f"# D0 findings: {lane}", "", f"Verified against dev `{verified_at}`.",
                f"Source lines cite dev `{cited_at}`.", ""]
        for finding, line in entries:
            body += [f"## {finding.ident}: {finding.page}:{line or '?'}", "",
                     f"- Statement: {finding.quote}", f"- Contradicted by: {source_of(finding)}",
                     f"- Correction: {finding.correction}", ""]
        (directory / f"{slug}.md").write_text("\n".join(body), encoding="utf-8")
        print(f"{directory / (slug + '.md')}: {len(entries)} finding(s)")
    return 0


def cells(row: str) -> list[str]:
    """The cells of one rendered table row, split on its unescaped pipes."""
    return [part.strip() for part in re.split(r"(?<!\\)\|", row)[1:-1]]


def current_with_findings(page: str) -> list[str]:
    """Pages an audit page marks current although its own Findings table lists them.

    Read from the page text alone, so it judges the committed page whatever
    generator produced it.
    """
    states: dict[str, str] = {}
    listed: set[str] = set()
    section = ""
    for row in page.split("\n"):
        if row.startswith("## "):
            section = row[3:].strip()
            continue
        if not row.startswith("| "):
            continue
        parts = cells(row)
        if section == "Inventory" and len(parts) == 9:
            link = ROW_LINK_RE.match(parts[0])
            if link:
                states[link.group(1)] = parts[5]
        elif section == "Findings" and len(parts) == 6:
            link = ROW_LINK_RE.match(parts[1])
            if link:
                listed.add(link.group(1))
    return sorted(path for path in listed if states.get(path) == "current")


def check(root: Path) -> int:
    """The freshness gate: the status rule holds on the committed page, which equals a fresh render."""
    expected = generate(root)
    target = root / OUTPUT
    actual = target.read_text(encoding="utf-8") if target.is_file() else ""
    broken = current_with_findings(actual)
    for path in broken:
        print(f"{OUTPUT}: {path} carries an open finding but is marked current (the status rule)")
    if actual == expected and not broken:
        print(f"documentation inventory: OK ({expected.count(chr(10))} lines, {OUTPUT} is fresh)")
        return 0
    if actual != expected:
        old, new = actual.split("\n"), expected.split("\n")
        changed = [n for n in range(max(len(old), len(new)))
                   if (old[n] if n < len(old) else None) != (new[n] if n < len(new) else None)]
        print(f"{OUTPUT}: STALE ({len(changed)} lines differ); first difference at line {changed[0] + 1}:")
        print("  committed: " + (old[changed[0]] if changed[0] < len(old) else "(end of file)")[:200])
        print("  generated: " + (new[changed[0]] if changed[0] < len(new) else "(end of file)")[:200])
    print("regenerate with: python3 scripts/docs_inventory.py --write")
    return 1


def track(root: Path) -> str | None:
    """Stage every file of a fixture, as committing them would; the failure, or None."""
    added = subprocess.run(["git", "-C", str(root), "add", "-A"], capture_output=True, text=True,
                           check=False, env=git_environment())
    return None if added.returncode == 0 else "git add failed: " + added.stderr.strip()


def fixture(root: Path) -> str | None:
    """A Git-initialised tree with one page of each status and one finding, all staged; the failure, or None."""
    pages = {
        "README.md": "# Fixture " + EM_DASH + " landing page\n\nSee `hdl/milan/top.sv` and IEEE 1722.1.\n",
        "docs/README.md": "# Documentation index\n\nAudience: integrator\n",
        "docs/guides/A.md": "# Guide A\n\nThe register resets to 0x1.\n",
        "docs/guides/B.md": "# Guide B\n\nCalls `protocol-processor/hdl/core.sv`.\n",
        "docs/guides/C.md": "# Guide C\n\nNo final newline",
        ".gitmodules": '[submodule "protocol-processor"]\n\tpath = protocol-processor\n',
        "docs/history/v1/README.md": "# Archive index\n",
        "docs/history/v1/OLD.md": ("[OBSOLETE + 2026-01-01]\n\n> Status: Historical\n>\n"
                                   "> Current successor: [open](../../guides/B.md)\n\n# Old page\n"),
        "hdl/milan/README-tests.md": "# `milan` tests\n",
        "hdl/milan/top.sv": "module top; endmodule\n",
        "scripts/tool.py": "\n",
        "tb/README": "# Testbenches\n",
    }
    for path, text in pages.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    data = {"verified_at": "0000000", "cited_at": "1111111",
            "findings": [{"id": "D0-001", "page": "docs/guides/A.md", "quote": "resets to 0x1",
                          "source": "`hdl/milan/top.sv` line 1", "correction": "It resets to 0x0."}]}
    (root / DATA).write_text(json.dumps(data), encoding="utf-8")
    made = subprocess.run(["git", "-C", str(root), "init", "-q"], capture_output=True, text=True,
                          check=False, env=git_environment())
    return track(root) if made.returncode == 0 else "git init failed: " + made.stderr.strip()


def gate(root: Path, *argv: str) -> tuple[int, str]:
    """The command line the workflow runs, on another root: its exit status and what it printed."""
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        code = main(list(argv), root)
    return code, printed.getvalue()


Mutation = Callable[[Path], None]


def control(name: str, mutate: Mutation, want: int, needle: str | tuple[str, ...] = "", says: str = "",
            absent: str | tuple[str, ...] = "") -> str | None:
    """One planted control on a fresh Git fixture; the failure message, or None when it held.

    The fixture's page is written with `--write`, the mutation applied, and
    `--check`, the workflow's own command, must exit `want` and print `says`.
    Unless it refused (2), `--write` must then heal the tree, and the page it
    regenerates must carry every `needle`, lack `absent` and carry no em dash.
    """
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        broken = fixture(root)
        if broken:
            return f"{name}: {broken}"
        code, printed = gate(root, "--write")
        if code != 0:
            return f"{name}: --write on the fixture exited {code}: {printed.strip()[:300]}"
        mutate(root)
        code, printed = gate(root, "--check")
        if code != want:
            return f"{name}: --check exited {code}, expected {want}: {printed.strip()[:300]}"
        if says not in printed:
            return f"{name}: --check did not print {says!r}"
        if want == 2:
            return None
        written, _ = gate(root, "--write")
        healed, printed = gate(root, "--check")
        if written != 0 or healed != 0:
            return f"{name}: --write did not heal the tree ({written}, {healed}): {printed.strip()[:300]}"
        rendered = (root / OUTPUT).read_text(encoding="utf-8")
        for text in (needle,) if isinstance(needle, str) else needle:
            if text not in rendered:
                return f"{name}: rendered page lacks {text!r}"
        for text in (absent,) if isinstance(absent, str) else absent:
            if text and text in rendered:
                return f"{name}: rendered page carries {text!r}"
        if EM_DASH in rendered:
            return f"{name}: rendered page carries an em dash"
        return None


def append(path: str, text: str) -> Mutation:
    """A mutation appending text to one fixture file."""
    def mutate(root: Path) -> None:
        """Append the text, creating the file and its directory when absent."""
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        with (root / path).open("a", encoding="utf-8") as handle:
            handle.write(text)
    return mutate


def replace(path: str, old: str, new: str) -> Mutation:
    """A mutation rewriting text in one fixture file."""
    def mutate(root: Path) -> None:
        """Rewrite the text."""
        target = root / path
        target.write_text(target.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
    return mutate


def edit_data(change: Callable[[dict], object]) -> Mutation:
    """A mutation applied to the fixture's data file."""
    def mutate(root: Path) -> None:
        """Apply the change to the parsed data file."""
        data = json.loads((root / DATA).read_text(encoding="utf-8"))
        change(data)
        (root / DATA).write_text(json.dumps(data), encoding="utf-8")
    return mutate


def add_tracked(path: str, text: str) -> Mutation:
    """A mutation adding one page and staging it; a failed stage leaves it untracked and the control fails."""
    def mutate(root: Path) -> None:
        """Write the page and stage it."""
        append(path, text)(root)
        track(root)
    return mutate


def without_git(root: Path) -> None:
    """A tree with no Git metadata whose submodule is checked out: an archive of a recursive clone."""
    shutil.rmtree(root / ".git")
    append("protocol-processor/README.md", "# Submodule page\n")(root)


def plant_copy(also: tuple[str, ...] = ()) -> Mutation:
    """A statement recorded on the README, with a wrapped and marked-up copy on the requirements page."""
    def mutate(root: Path) -> None:
        """Record the statement, write it on the README and add the requirements page."""
        edit_data(lambda d: d["findings"].append(
            {"id": "D0-002", "page": "README.md", "quote": "All five default to firmware.", "also": list(also),
             "source": "`scripts/tool.py` line 1", "correction": "Say that all five stay in fabric."}))(root)
        append("README.md", "\nAll five default to firmware.\n")(root)
        add_tracked("REQUIREMENTS.md", ("# Requirements\n\n> **All five** default\n> to `FIRMWARE`.\n"
                                        "\nThe Mark II default places\n  them on the core.\n"))(root)
    return mutate


def in_order(*mutations: Mutation) -> Mutation:
    """The mutations in order, with the page regenerated after every one but the last."""
    def mutate(root: Path) -> None:
        """Apply each mutation in turn."""
        for mutation in mutations[:-1]:
            mutation(root)
            gate(root, "--write")
        mutations[-1](root)
    return mutate


def copy_controls() -> tuple:
    """The cross-page rule's arms: a copy gets a row and a stale page, and only a real copy does."""
    copy_row = "| D0-002 | [REQUIREMENTS.md](../REQUIREMENTS.md) | 3 |"
    copy_status = "| Requirements | -- | stale | 1 finding(s): D0-002 |"
    first_copy = "> **All five** default\n> to `FIRMWARE`.\n"
    spelling = ("The Mark II default places them on the core.",)
    return (
        ("the README's statement copied onto the requirements page", plant_copy(), 1,
         (copy_row, copy_status, "| D0-002 | [README.md](../README.md) | 5 |",
          "Copy of the D0-002 statement on `README.md`."), "STALE"),
        ("a spelling found only through `also` gets a row",
         in_order(plant_copy(spelling), replace("REQUIREMENTS.md", first_copy, "Open.\n")), 1,
         ("| D0-002 | [REQUIREMENTS.md](../REQUIREMENTS.md) | 5 |", copy_status), "STALE"),
        ("two spellings on one page give one row", plant_copy(spelling), 1, copy_row, "STALE",
         "| D0-002 | [REQUIREMENTS.md](../REQUIREMENTS.md) | 6 |"),
        ("a copy cannot be marked current by hand",
         in_order(plant_copy(), replace(OUTPUT, copy_status, "| Requirements | -- | current | no recorded |")), 1,
         copy_status, "REQUIREMENTS.md carries an open finding but is marked current"),
        ("a fixed copy loses its row and its page recovers",
         in_order(plant_copy(), replace("REQUIREMENTS.md", first_copy, "Open.\n")), 1,
         "| Requirements | -- | current | no recorded contradiction |", "STALE", "| D0-002 | [REQUIREMENTS.md]"),
        ("a copy on an archive page gets a row and stays obsolete",
         append("docs/history/v1/OLD.md", "The register resets to 0x1.\n"), 1,
         ("| D0-001 | [docs/history/v1/OLD.md (historical)](history/v1/OLD.md) | 8 |",
          "| Old page | -- | obsolete | versioned archive;"), "STALE"),
        ("a longer word is not a copy", append("docs/guides/B.md", "It presets to 0x1, or resets to 0x10.\n"), 1, "",
         "STALE", "| D0-001 | [docs/guides/B.md]"),
        ("a statement across a blank line is not a copy", append("docs/guides/B.md", "It resets to\n\n0x1.\n"), 1,
         "", "STALE", "| D0-001 | [docs/guides/B.md]"),
        ("a page already recording the words gets no second row",
         in_order(append("docs/guides/B.md", "It resets to 0x1 here.\n"),
                  append("docs/guides/A.md", "It resets to 0x1 here.\n"), edit_data(lambda d: d["findings"].append(
                      {"id": "D0-003", "page": "docs/guides/B.md", "quote": "It resets to 0x1 here.",
                       "source": "`scripts/tool.py` line 1", "correction": "It resets to 0x0."}))),
         1, "| D0-003 | [docs/guides/B.md](guides/B.md) | 4 |", "STALE",
         ("| D0-001 | [docs/guides/B.md]", "| D0-003 | [docs/guides/A.md]")),
        ("the audit page quoting every statement is not searched", lambda root: None, 0, "", "is fresh",
         "| D0-001 | [docs/DOCUMENTATION_AUDIT.md]"),
        ("`also` that is not a list", edit_data(lambda d: d["findings"][0].update(also="x")), 2, "", "REFUSED"),
        ("`also` with an empty statement", edit_data(lambda d: d["findings"][0].update(also=[" "])), 2, "", "REFUSED"),
    )


def selftest() -> int:
    """`--check` itself on Git fixtures: every status rule, planted stale pages and the data refusals."""
    stale_cell = "| stale | 1 finding(s): D0-001 |"
    controls = (
        ("unchanged tree is fresh through `git ls-files`", lambda root: None, 0, "| D0-001 |", "is fresh"),
        ("planted stale page: one added line", append("docs/guides/B.md", "Added line.\n"), 1, "", "STALE"),
        ("planted edited quote in the data file",
         edit_data(lambda d: d["findings"][0].update(quote="resets to 0x2")), 1, "re-verify: quote not found",
         "STALE"),
        ("fixed statement asks for re-verification", replace("docs/guides/A.md", "0x1", "0x0"), 1,
         "re-verify: quote not found", "STALE"),
        ("new tracked page without a row", add_tracked("docs/guides/NEW.md", "# New\n"), 1,
         "| [docs/guides/NEW.md](guides/NEW.md) |", "STALE"),
        ("untracked page stays out of the population", append("docs/guides/UNTRACKED.md", "# Untracked\n"), 0,
         "", "is fresh", "UNTRACKED"),
        ("tracked page removed", lambda root: (root / "docs/guides/B.md").unlink(), 1, "", "STALE",
         "| [docs/guides/B.md](guides/B.md) |"),
        ("hand-edited audit page", append(OUTPUT, "hand edit\n"), 1, "", "STALE"),
        ("hand-edited status hides a finding",
         replace(OUTPUT, stale_cell, "| current | no recorded contradiction |"), 1, stale_cell,
         "docs/guides/A.md carries an open finding but is marked current"),
        ("finding marks its page stale", lambda root: None, 0, stale_cell),
        ("a recorded current judgement cannot hide a finding", edit_data(lambda d: d.update(
            judged={"docs/guides/A.md": {"status": "current", "evidence": "judged"}})), 0, stale_cell),
        # Each needle starts a line, so it reads the inventory row and never the Findings row.
        ("lines as wc -l counts them", lambda root: None, 0, "\n| [docs/guides/A.md](guides/A.md) | 3 |"),
        ("an unterminated last line counts", lambda root: None, 0, "\n| [docs/guides/C.md](guides/C.md) | 3 |"),
        ("a README without .md is a document", lambda root: None, 0, "| [tb/README](../tb/README) |"),
        ("the walk without Git renders the same page and skips a checked-out submodule", without_git, 0,
         "", "is fresh", "protocol-processor/README.md"),
        ("supersession banner", append("docs/guides/B.md", "\n> Superseded by [A](A.md).\n"), 1,
         "| superseded | banner at line 5 names `docs/guides/A.md` |", "STALE"),
        ("archive page is obsolete with its successor", lambda root: None, 0,
         "| obsolete | versioned archive; successor [docs/guides/B.md](guides/B.md) |"),
        ("archive index stays current", lambda root: None, 0, "archive index"),
        ("audience line overrides the table", lambda root: None, 0, "| integrator | Documentation index |"),
        ("described code and standards", lambda root: None, 0, "`hdl/milan`, 1722.1-2021"),
        ("a submodule path stands for its submodule, checked out or not", lambda root: None, 0,
         "| `protocol-processor` |"),
        ("em dash in a title is rewritten", lambda root: None, 0, "Fixture - landing page"),
        ("module directory without a README", lambda root: None, 0, "| `scripts/` | no | 0 |"),
        ("finding on an untracked page", edit_data(lambda d: d["findings"][0].update(page="docs/NO.md")),
         2, "", "REFUSED"),
        ("duplicate finding id", edit_data(lambda d: d["findings"].append(dict(d["findings"][0]))),
         2, "", "REFUSED"),
        ("finding without a correction", edit_data(lambda d: d["findings"][0].update(correction="")),
         2, "", "REFUSED"),
        ("judgement with an unknown status", edit_data(lambda d: d.update(
            judged={"docs/guides/B.md": {"status": "retired", "evidence": "x"}})), 2, "", "REFUSED"),
        ("the citations' baseline is on the page", lambda root: None, 0, "at dev `1111111`"),
        ("malformed data file", lambda root: (root / DATA).write_text("{", encoding="utf-8"), 2, "", "REFUSED"),
    ) + copy_controls()
    failures = [message for message in (control(*arm) for arm in controls) if message]
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        broken = fixture(root)
        page = "" if broken else generate(root)
        if broken or f"| {page_link(OUTPUT)} | {line_count(page)} |" not in page:
            failures.append(broken or "the audit page's own row does not carry its own line count")
    for message in failures:
        print("selftest: FAIL " + message)
    if failures:
        return 1
    print(f"documentation inventory selftest: OK ({len(controls) + 1} controls)")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    """Write, check or self-test the inventory of `root`; 2 on a refusal."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true", help="regenerate " + OUTPUT)
    modes.add_argument("--check", action="store_true", help="exit 1 when " + OUTPUT + " is stale")
    modes.add_argument("--selftest", action="store_true", help="run the planted controls")
    modes.add_argument("--findings-dir", type=Path, help="write one findings file per lane there")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        if args.findings_dir:
            return write_findings(root, args.findings_dir)
        if args.check:
            return check(root)
        (root / OUTPUT).write_text(generate(root), encoding="utf-8")
        print(f"wrote {OUTPUT}")
        return 0
    except Refusal as refusal:
        print(f"REFUSED: {refusal}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
