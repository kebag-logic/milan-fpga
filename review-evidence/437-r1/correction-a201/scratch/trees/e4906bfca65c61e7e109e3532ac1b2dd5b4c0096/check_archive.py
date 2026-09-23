#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Verify versioned history metadata, routing, and current links."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ARCHIVE = REPO / "docs" / "history" / "v1"
INDEX = ARCHIVE / "README.md"
ARCHIVE_PREFIX = "docs/history/v1/"
OLD_PREFIX = "historical_now_obsolete/"
OBSOLETE_HEADER_RE = re.compile(r"^\[OBSOLETE \+ \d{4}-\d{2}-\d{2}\]$")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
LINK_RE = re.compile(r"\[([^\]]+)]\(([^)]+)\)")
STATUS_RE = re.compile(r"^> Status: Historical$", re.MULTILINE)
ORIGINAL_RE = re.compile(r"^> Original path: `([^`]+)`$", re.MULTILINE)
ARCHIVED_RE = re.compile(r"^> Archived: (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
RELOCATED_RE = re.compile(r"^> Relocated: (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
REPLACED_RE = re.compile(r"^> Replaced in place: yes$", re.MULTILINE)
SUCCESSOR_RE = re.compile(
    r"^> Current successor: \[[^\]]+]\(([^)]+)\)$", re.MULTILINE
)
ARCHIVE_TOTAL_RE = re.compile(
    r"^- Archive total: (\d+) Markdown pages\.$", re.MULTILINE
)
RETIRED_ROLE_PATTERNS = {
    "CHANGELOG.md": re.compile(
        r"measured (?:per-lever )?(?:performance )?ledger|"
        r"per-lever (?:(?:measured|perf(?:ormance)?) )?ledger|"
        r"perf(?:ormance)?-lineage ledger|"
        r"campaign numbers|perf numbers|measured changes",
        re.IGNORECASE,
    ),
}


@dataclass(frozen=True)
class Metadata:
    original: str
    archived: str
    relocated: str
    successor: Path
    replaced_in_place: bool


def tracked_markdown() -> list[str]:
    """Every tracked Markdown path, repo-relative and sorted. Untracked pages
    are somebody's working copy and are not the archive's business."""
    output = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z", "*.md"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return sorted(path for path in output.split("\0") if path)


def archived_pages(paths: list[str]) -> list[Path]:
    """The versioned-history pages themselves, without their own index."""
    return [
        REPO / path
        for path in paths
        if path.startswith(ARCHIVE_PREFIX) and (REPO / path) != INDEX
    ]


def current_pages(paths: list[str]) -> list[Path]:
    """Everything outside versioned history - the pages a reader is sent to."""
    return [REPO / path for path in paths if not path.startswith(ARCHIVE_PREFIX)]


def resolve_link(source: Path, raw_target: str) -> Path | None:
    """The file a Markdown target names, or None when it names no file in this
    tree: an external URL, a site-absolute path, or a bare fragment."""
    target = raw_target.split("#", 1)[0].split("?", 1)[0].strip("<>")
    if not target or target.startswith("/") or "://" in target:
        return None
    return (source.parent / target).resolve()


def parse_metadata(path: Path) -> tuple[Metadata | None, list[str]]:
    """The archive front matter of one page, or None and the reasons it is not
    usable. Metadata is returned only when every field parsed and the successor
    it names is a file that exists - a partial record would route nowhere."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        relative = path.relative_to(REPO)
    except ValueError:
        relative = Path(path.name)
    errors: list[str] = []
    if not lines or not OBSOLETE_HEADER_RE.fullmatch(lines[0]):
        errors.append(f"{relative}: missing obsolete header")
    head = "\n".join(lines[:24])
    if not STATUS_RE.search(head):
        errors.append(f"{relative}: missing historical status")
    original = ORIGINAL_RE.search(head)
    archived = ARCHIVED_RE.search(head)
    relocated = RELOCATED_RE.search(head)
    successor = SUCCESSOR_RE.search(head)
    if original is None:
        errors.append(f"{relative}: missing original path")
    if archived is None or not DATE_RE.fullmatch(archived.group(1)):
        errors.append(f"{relative}: missing archived date")
    if relocated is None or not DATE_RE.fullmatch(relocated.group(1)):
        errors.append(f"{relative}: missing relocation date")
    successor_path = None
    if successor is None:
        errors.append(f"{relative}: missing current successor")
    else:
        successor_path = resolve_link(path, successor.group(1))
        if successor_path is None or not successor_path.is_file():
            errors.append(f"{relative}: current successor does not exist")
    if errors:
        return None, errors
    return Metadata(
        original.group(1),
        archived.group(1),
        relocated.group(1),
        successor_path,
        REPLACED_RE.search(head) is not None,
    ), []


def index_rows(index: Path = INDEX) -> list[tuple[Path, Path, str]]:
    """(historical page, current successor, source line) per archive index row."""
    rows: list[tuple[Path, Path, str]] = []
    for line in index.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        links = LINK_RE.findall(line)
        if len(links) < 2:
            continue
        page = resolve_link(index, links[0][1])
        successor = resolve_link(index, links[-1][1])
        if page is not None and successor is not None:
            rows.append((page, successor, line))
    return rows


def link_is_marked(text: str) -> bool:
    """Whether link text warns that it leads into history. An unmarked link
    hands a reader a retired page with nothing saying it is retired."""
    lowered = text.lower()
    return any(word in lowered for word in ("archiv", "histor", "obsolete"))


def valid_in_place_replacement(metadata: Metadata, original: Path) -> bool:
    """Accept only a real document replacing its exact historical path."""
    return (
        metadata.replaced_in_place
        and original == metadata.successor
        and original.is_file()
    )


def has_retired_role(original: str, line: str) -> bool:
    """Detect an old role assigned to a surviving replacement path."""
    pattern = RETIRED_ROLE_PATTERNS.get(original)
    return pattern is not None and pattern.search(line) is not None


def retired_role_lines(original: str, text: str) -> list[int]:
    """Find surviving-path references retaining their retired role."""
    reference = re.compile(
        rf"(?<![A-Za-z0-9_]){re.escape(original)}(?![A-Za-z0-9_])"
    )
    lines = text.splitlines()
    findings: list[int] = []
    for index, line in enumerate(lines):
        if reference.search(line) is None:
            continue
        context = "\n".join(lines[max(0, index - 1):index + 2])
        if has_retired_role(original, context):
            findings.append(index + 1)
    return findings


def declared_archive_totals(text: str) -> list[int]:
    """Return every inventory total declared by the archive index."""
    return [int(value) for value in ARCHIVE_TOTAL_RE.findall(text)]


def archive_total_problem(totals: list[int], expected: int) -> str | None:
    """Explain a missing, duplicate, or stale archive total."""
    if len(totals) != 1:
        return "archive index needs exactly one inventory total"
    if totals[0] != expected:
        return f"archive inventory total is {totals[0]}, expected {expected}"
    return None


def _selftest_metadata(page: Path) -> int:
    """Parsing arms: the valid fixture, the replacement marker, each mutation."""
    good = """[OBSOLETE + 2026-08-01]

> Status: Historical
>
> Original path: `old.md`
>
> Archived: 2026-08-01
>
> Relocated: 2026-08-31
>
> Current successor: [open current documentation](current.md)
"""
    mutations = {
        "header": ("[OBSOLETE + 2026-08-01]", "# Old page"),
        "status": ("> Status: Historical", "> State: Historical"),
        "original": ("> Original path:", "> Previous path:"),
        "archived": ("> Archived:", "> First archived:"),
        "relocated": ("> Relocated:", "> Moved:"),
        "successor": ("> Current successor:", "> Replacement:"),
        "dead successor": ("current.md", "missing.md"),
    }
    page.write_text(good, encoding="utf-8")
    metadata, errors = parse_metadata(page)
    if errors or metadata is None or metadata.original != "old.md":
        print(f"archive selftest: valid fixture failed: {errors}")
        return 1
    replaced = good.replace(
        "> Current successor:",
        "> Replaced in place: yes\n>\n> Current successor:",
    )
    page.write_text(replaced, encoding="utf-8")
    metadata, errors = parse_metadata(page)
    if errors or metadata is None or not metadata.replaced_in_place:
        print(f"archive selftest: replacement metadata failed: {errors}")
        return 1
    for name, (old, new) in mutations.items():
        page.write_text(good.replace(old, new, 1), encoding="utf-8")
        _metadata, errors = parse_metadata(page)
        if not errors:
            print(f"archive selftest: {name} mutation escaped")
            return 1
    return 0


def _selftest_in_place(root: Path, page: Path, current: Path) -> int:
    """In-place-replacement predicate arms, then the index-row parser."""
    valid_replacement = Metadata(
        "current.md",
        "2026-08-01",
        "2026-08-31",
        current.resolve(),
        True,
    )
    if not valid_in_place_replacement(valid_replacement, current.resolve()):
        print("archive selftest: valid in-place replacement failed")
        return 1
    if valid_in_place_replacement(
        replace(valid_replacement, replaced_in_place=False), current.resolve()
    ):
        print("archive selftest: unmarked in-place replacement escaped")
        return 1
    if valid_in_place_replacement(
        replace(valid_replacement, successor=page.resolve()), current.resolve()
    ):
        print("archive selftest: mismatched in-place successor escaped")
        return 1
    missing = root / "missing.md"
    if valid_in_place_replacement(
        replace(valid_replacement, successor=missing), missing
    ):
        print("archive selftest: missing in-place successor escaped")
        return 1
    index = root / "README.md"
    index.write_text(
        "| Historical page | Current successor |\n"
        "|---|---|\n"
        "| [Old](old.md) | [Current](current.md) |\n",
        encoding="utf-8",
    )
    rows = index_rows(index)
    if len(rows) != 1 or rows[0][0] != page.resolve():
        print("archive selftest: index row parsing failed")
        return 1
    return 0


def _selftest_routes() -> int:
    """Marked-history-link arms, then the retired-replacement-role arms."""
    if not link_is_marked("historical result"):
        print("archive selftest: marked link failed")
        return 1
    if link_is_marked("old result"):
        print("archive selftest: unmarked link passed")
        return 1
    if not has_retired_role("CHANGELOG.md", "[old](CHANGELOG.md), measured ledger"):
        print("archive selftest: retired replacement role escaped")
        return 1
    if has_retired_role("CHANGELOG.md", "[current changelog](CHANGELOG.md)"):
        print("archive selftest: current replacement role failed")
        return 1
    wrapped_route = (
        "[CHANGELOG.md](../../CHANGELOG.md) for the\n"
        "per-lever measured ledger.\n"
    )
    if retired_role_lines("CHANGELOG.md", wrapped_route) != [1]:
        print("archive selftest: wrapped replacement role escaped")
        return 1
    raw_route = "├─ CHANGELOG.md  the measured per-lever performance ledger\n"
    if retired_role_lines("CHANGELOG.md", raw_route) != [1]:
        print("archive selftest: raw replacement role escaped")
        return 1
    historical_route = (
        "[historical ledger](docs/history/v1/PERFORMANCE_CHANGELOG.md)\n"
    )
    if retired_role_lines("CHANGELOG.md", historical_route):
        print("archive selftest: historical target misclassified")
        return 1
    return 0


def _selftest_inventory() -> int:
    """Declared-archive-total parsing arms and the total-drift verdict."""
    if declared_archive_totals("- Archive total: 43 Markdown pages.\n") != [43]:
        print("archive selftest: valid inventory total failed")
        return 1
    if declared_archive_totals("- Archive total: forty-three pages.\n"):
        print("archive selftest: malformed inventory total passed")
        return 1
    if archive_total_problem([43], 43) is not None:
        print("archive selftest: matching inventory total failed")
        return 1
    if archive_total_problem([42], 43) is None:
        print("archive selftest: inventory count drift escaped")
        return 1
    return 0


def selftest() -> int:
    """Every control armed against a fixture that should trip it, so a gate
    that has quietly stopped checking cannot report a pass."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        page = root / "old.md"
        current = root / "current.md"
        current.write_text("# Current\n", encoding="utf-8")
        failed = _selftest_metadata(page) or _selftest_in_place(root, page, current)
    if failed or _selftest_routes() or _selftest_inventory():
        return 1
    print("archive selftest: OK (24 controls)")
    return 0


def _archived_problems(
    pages: list[Path], listing: bool
) -> tuple[list[str], dict[Path, Metadata]]:
    """Front-matter findings on the archived pages, and the metadata parsed."""
    problems: list[str] = []
    metadata: dict[Path, Metadata] = {}
    originals: list[str] = []
    for page in pages:
        parsed, errors = parse_metadata(page)
        problems.extend(errors)
        if parsed is not None:
            metadata[page.resolve()] = parsed
            originals.append(parsed.original)
            original = (REPO / parsed.original).resolve()
            replaced_here = valid_in_place_replacement(parsed, original)
            if original.exists() and not replaced_here:
                problems.append(
                    f"{page.relative_to(REPO)}: original path still exists"
                )
            if parsed.replaced_in_place and not replaced_here:
                problems.append(
                    f"{page.relative_to(REPO)}: invalid in-place replacement"
                )
        if listing:
            print(f"  {'ok' if not errors else 'BAD':<4} {page.relative_to(ARCHIVE)}")

    duplicates = sorted(
        original for original, count in Counter(originals).items() if count != 1
    )
    if duplicates:
        problems.append("duplicate original paths: " + ", ".join(duplicates))
    return problems, metadata


def _index_problems(pages: list[Path], metadata: dict[Path, Metadata]) -> list[str]:
    """Findings in the archive index: coverage, duplicate rows, the inventory."""
    problems: list[str] = []
    rows = index_rows()
    row_counts = Counter(page for page, _successor, _line in rows)
    expected = {page.resolve() for page in pages}
    actual = set(row_counts)
    for missing in sorted(expected - actual):
        problems.append(f"unindexed page: {missing.relative_to(REPO)}")
    for stale in sorted(actual - expected):
        problems.append(f"stale index row: {stale.relative_to(REPO)}")
    for duplicate, count in sorted(row_counts.items()):
        if count != 1:
            problems.append(
                f"duplicate index rows: {duplicate.relative_to(REPO)} ({count})"
            )
    for page, successor, _line in rows:
        if not successor.exists():
            problems.append(f"dead index successor for {page.relative_to(REPO)}")
        parsed = metadata.get(page)
        if parsed is not None and parsed.successor != successor:
            problems.append(
                f"successor mismatch for {page.relative_to(REPO)}"
            )

    totals = declared_archive_totals(INDEX.read_text(encoding="utf-8"))
    total_problem = archive_total_problem(totals, len(pages))
    if total_problem is not None:
        problems.append(total_problem)
    return problems


def _current_problems(
    tracked: list[str], metadata: dict[Path, Metadata], expected: set[Path]
) -> list[str]:
    """Findings on the pages still current: stale header, retired role, link."""
    problems: list[str] = []
    replacement_targets = {
        (REPO / parsed.original).resolve(): parsed.original
        for parsed in metadata.values()
        if parsed.replaced_in_place
    }

    for page in current_pages(tracked):
        text = page.read_text(encoding="utf-8")
        lines = text.splitlines()
        if lines and OBSOLETE_HEADER_RE.fullmatch(lines[0]):
            problems.append(f"obsolete page remains current: {page.relative_to(REPO)}")
        for original in replacement_targets.values():
            for line_number in retired_role_lines(original, text):
                problems.append(
                    f"retired replacement role: {page.relative_to(REPO)}:"
                    f"{line_number}: {original}"
                )
        for line_number, line in enumerate(lines, start=1):
            for link_text, raw_target in LINK_RE.findall(line):
                target = resolve_link(page, raw_target)
                if target not in expected:
                    continue
                if not link_is_marked(link_text):
                    problems.append(
                        f"unmarked history link: {page.relative_to(REPO)}:"
                        f"{line_number}: {link_text!r}"
                    )
    return problems


def main() -> int:
    """The gate: history carries its metadata, the index routes every page to a
    successor that exists, and no current page links into history unmarked."""
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    listing = sys.argv[1:] == ["--list"]
    if sys.argv[1:] not in ([], ["--list"]):
        print(__doc__)
        return 2

    problems: list[str] = []
    tracked = tracked_markdown()
    old_paths = [path for path in tracked if path.startswith(OLD_PREFIX)]
    if old_paths:
        problems.append("legacy archive paths remain: " + ", ".join(old_paths))

    pages = archived_pages(tracked)
    archived, metadata = _archived_problems(pages, listing)
    problems.extend(archived)
    problems.extend(_index_problems(pages, metadata))
    problems.extend(
        _current_problems(tracked, metadata, {page.resolve() for page in pages})
    )

    if problems:
        print(f"archive gate: FAIL ({len(problems)} findings)")
        for problem in problems:
            print("  " + problem)
        return 1

    print(
        f"archive gate: OK ({len(pages)} historical page(s), "
        "each indexed with metadata and a current successor)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
