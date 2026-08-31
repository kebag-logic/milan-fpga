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
from dataclasses import dataclass
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
SUCCESSOR_RE = re.compile(
    r"^> Current successor: \[[^\]]+]\(([^)]+)\)$", re.MULTILINE
)


@dataclass(frozen=True)
class Metadata:
    original: str
    archived: str
    relocated: str
    successor: Path


def tracked_markdown() -> list[str]:
    output = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z", "*.md"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return sorted(path for path in output.split("\0") if path)


def archived_pages(paths: list[str]) -> list[Path]:
    return [
        REPO / path
        for path in paths
        if path.startswith(ARCHIVE_PREFIX) and (REPO / path) != INDEX
    ]


def current_pages(paths: list[str]) -> list[Path]:
    return [REPO / path for path in paths if not path.startswith(ARCHIVE_PREFIX)]


def resolve_link(source: Path, raw_target: str) -> Path | None:
    target = raw_target.split("#", 1)[0].split("?", 1)[0].strip("<>")
    if not target or target.startswith("/") or "://" in target:
        return None
    return (source.parent / target).resolve()


def parse_metadata(path: Path) -> tuple[Metadata | None, list[str]]:
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
        if successor_path is None or not successor_path.exists():
            errors.append(f"{relative}: current successor does not exist")
    if errors:
        return None, errors
    return Metadata(
        original.group(1),
        archived.group(1),
        relocated.group(1),
        successor_path,
    ), []


def index_rows(index: Path = INDEX) -> list[tuple[Path, Path, str]]:
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
    lowered = text.lower()
    return any(word in lowered for word in ("archiv", "histor", "obsolete"))


def selftest() -> int:
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
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        page = root / "old.md"
        current = root / "current.md"
        current.write_text("# Current\n", encoding="utf-8")
        page.write_text(good, encoding="utf-8")
        metadata, errors = parse_metadata(page)
        if errors or metadata is None or metadata.original != "old.md":
            print(f"archive selftest: valid fixture failed: {errors}")
            return 1
        for name, (old, new) in mutations.items():
            page.write_text(good.replace(old, new, 1), encoding="utf-8")
            _metadata, errors = parse_metadata(page)
            if not errors:
                print(f"archive selftest: {name} mutation escaped")
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
    if not link_is_marked("historical result"):
        print("archive selftest: marked link failed")
        return 1
    if link_is_marked("old result"):
        print("archive selftest: unmarked link passed")
        return 1
    print("archive selftest: OK (10 controls)")
    return 0


def main() -> int:
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
    metadata: dict[Path, Metadata] = {}
    originals: list[str] = []
    for page in pages:
        parsed, errors = parse_metadata(page)
        problems.extend(errors)
        if parsed is not None:
            metadata[page.resolve()] = parsed
            originals.append(parsed.original)
            if (REPO / parsed.original).exists():
                problems.append(
                    f"{page.relative_to(REPO)}: original path still exists"
                )
        if listing:
            print(f"  {'ok' if not errors else 'BAD':<4} {page.relative_to(ARCHIVE)}")

    duplicates = sorted(
        original for original, count in Counter(originals).items() if count != 1
    )
    if duplicates:
        problems.append("duplicate original paths: " + ", ".join(duplicates))

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

    for page in current_pages(tracked):
        text = page.read_text(encoding="utf-8")
        lines = text.splitlines()
        if lines and OBSOLETE_HEADER_RE.fullmatch(lines[0]):
            problems.append(f"obsolete page remains current: {page.relative_to(REPO)}")
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
