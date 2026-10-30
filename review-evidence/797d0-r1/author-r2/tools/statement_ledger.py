#!/usr/bin/env python3
"""Split the release-facing pages into statements and mark the numeric or normative ones.

Usage: python3 -I statement_ledger.py <tree> <out.jsonl>

A statement is one table body row, one list item (with its continuation
lines), or one sentence of a paragraph. Headings, the generated feature-status
blocks, HTML comments and the contents lists are skipped. A fenced code block
is one statement of kind `code` (its commands are checked separately).

A statement is numeric when its text, links and inline code removed, still
carries a digit, a hex literal or an issue reference; it is normative when it
carries one of the NORMATIVE words. Every statement that is either is in the
denominator the HANDOFF reports per page.
"""
import json
import re
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]), Path(sys.argv[2])
PAGES = ["README.md", "docs/README.md"] + sorted(
    str(p.relative_to(tree)) for d in ("docs/guides", "docs/integration", "docs/reference")
    for p in (tree / d).rglob("*.md"))
NORMATIVE = re.compile(
    r"\b(must|shall|should|never|always|only|every|all|none|no|not|default|defaults|reset|resets|required|"
    r"requires|implemented|supported|unsupported|pending|open|closed|remains|until|refuses?|rejects?|fails?|"
    r"passes|guarantees?|exactly|at most|at least|is the|are the|cannot|can't|does not|do not|won't|"
    r"mandatory|optional|forbidden|ships?|shipping|merged|landed|deleted|removed|retired|replaced)\b",
    re.IGNORECASE)
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
CODE = re.compile(r"`[^`]*`")
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*\[(#0-9])")


def numeric(text: str) -> bool:
    bare = CODE.sub(" ", LINK.sub(r"\1", text))
    return bool(re.search(r"\d|#\d+", bare)) or bool(re.search(r"0x[0-9A-Fa-f]", text)) or bool(
        re.search(r"(?<![\w/])#\d{2,4}\b", text))


def statements(path: str):
    lines = (tree / path).read_text(encoding="utf-8").split("\n")
    fence = None
    para: list[tuple[int, str]] = []
    item: list[tuple[int, str]] = []
    skip_block = False
    section = ""

    def flush_para():
        nonlocal para
        if para:
            first = para[0][0]
            text = " ".join(t.strip() for _, t in para)
            for s in SENT.split(text):
                if s.strip():
                    yield ("sentence", first, s.strip(), section)
        para = []

    def flush_item():
        nonlocal item
        if item:
            yield ("item", item[0][0], " ".join(t.strip() for _, t in item), section)
        item = []

    for n, raw in enumerate(lines, 1):
        line = raw.rstrip()
        if fence:
            fence[1].append(line)
            if re.match(r"^\s*(```|~~~)", line):
                yield ("code", fence[0], "\n".join(fence[1]), section)
                fence = None
            continue
        if re.match(r"^\s*(```|~~~)", line):
            yield from flush_para()
            yield from flush_item()
            fence = (n, [line])
            continue
        if "milan-feature-status:start" in line or line.strip().startswith("<!--") and "start" in line:
            skip_block = True
        if skip_block:
            if "end -->" in line or "milan-feature-status:end" in line:
                skip_block = False
            continue
        if line.strip().startswith("<!--"):
            continue
        if re.match(r"^#{1,6}\s", line):
            yield from flush_para()
            yield from flush_item()
            section = line.lstrip("#").strip()
            continue
        if section == "Contents":
            continue
        if line.startswith("|"):
            yield from flush_para()
            yield from flush_item()
            if re.match(r"^\|[\s:|-]+\|?$", line):
                continue
            yield ("row", n, line, section)
            continue
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            yield from flush_para()
            yield from flush_item()
            item = [(n, m.group(3))]
            continue
        if not line.strip():
            yield from flush_para()
            yield from flush_item()
            continue
        if item and (line.startswith("  ") or line.startswith("\t")):
            item.append((n, line))
            continue
        if item:
            yield from flush_item()
        if line.lstrip().startswith(">"):
            line = line.lstrip()[1:]
        para.append((n, line))
    yield from flush_para()
    yield from flush_item()


with out.open("w", encoding="utf-8") as handle:
    totals = {}
    for page in PAGES:
        rows = list(statements(page))
        # Table header rows: the first row of each table carries no claim.
        seen_tables = set()
        for kind, line, text, section in rows:
            if kind == "row":
                prev = (tree / page).read_text(encoding="utf-8").split("\n")[line - 2] if line > 1 else ""
                if not prev.startswith("|"):
                    continue  # header row
            if kind == "code":
                body = "\n".join(text.split("\n")[1:-1])
                lang = text.split("\n")[0].strip("`~ ").lower()
                # A command block is a claim that the commands run; a diagram counts by its numbers.
                num = lang in ("sh", "bash", "console", "shell", "") and bool(body.strip()) or bool(
                    re.search(r"\d", body))
                norm = False
            else:
                num, norm = numeric(text), bool(NORMATIVE.search(text))
            handle.write(json.dumps({"page": page, "line": line, "kind": kind, "section": section,
                                     "numeric": num, "normative": norm, "text": text},
                                    ensure_ascii=False) + "\n")
            t = totals.setdefault(page, [0, 0])
            t[0] += 1
            t[1] += bool(num or norm)
    for page, (alls, counted) in totals.items():
        print(f"{counted:5d} / {alls:5d}  {page}")
    print(f"{sum(c for _, c in totals.values()):5d} / {sum(a for a, _ in totals.values()):5d}  total")
