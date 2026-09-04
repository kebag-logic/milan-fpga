#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check concise prose inside current audience documentation."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    ROOT / "CHANGELOG.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "DOC_GENERATION.md",
    ROOT / "docs" / "diagrams" / "README.md",
    ROOT / "docs" / "guides" / "README.md",
    ROOT / "docs" / "guides" / "IMPLEMENTATION_DEVELOPER.md",
    ROOT / "docs" / "guides" / "VERIFICATION_DEVELOPER.md",
    ROOT / "docs" / "guides" / "SYSTEM_INTEGRATOR.md",
    ROOT / "docs" / "guides" / "PROJECT_MANAGER.md",
    ROOT / "docs" / "integration" / "INTEGRATION_GUIDE.md",
    ROOT / "docs" / "reference" / "SUBMODULES.md",
    ROOT / "docs" / "DOCUMENTATION_AUDIT.md",
    ROOT / "docs" / "history" / "v1" / "README.md",
)
MAX_SENTENCE_WORDS = 10
MAX_PARAGRAPH_WORDS = 20
MAX_PARAGRAPH_SENTENCES = 2
WORD = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?(?:-[A-Za-z0-9]+)*")
LIST_ITEM = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+")
INLINE_CODE = re.compile(r"`[^`]*`")
IMAGE = re.compile(r"^\s*!\[[^]]*]\([^)]*\)\s*$")
LINK = re.compile(r"\[([^]]+)]\([^)]*\)")
REFERENCE_LINK = re.compile(r"\[([^]]+)]\[[^]]*]")
RAW_URL = re.compile(r"https?://\S+")


@dataclass(frozen=True)
class Block:
    line: int
    text: str
    paragraph: bool


@dataclass(frozen=True)
class Finding:
    line: int
    reason: str
    text: str


def prose_blocks(text: str) -> list[Block]:
    """Every block the word limits apply to, in the order a reader meets them.

    Fenced code, HTML comments, headings, tables, block quotes, indented code
    and a line that is only an image are flushed rather than measured. None of
    them is prose, and counting them would have the gate demand that a table
    row or a command line be rewritten shorter.
    """
    blocks: list[Block] = []
    paragraph: list[str] = []
    paragraph_line = 0
    fenced = False
    comment = False

    def flush() -> None:
        """Emit the paragraph accumulated so far; anything non-prose ends one."""
        nonlocal paragraph, paragraph_line
        if paragraph:
            blocks.append(Block(paragraph_line, " ".join(paragraph), True))
            paragraph = []
            paragraph_line = 0

    for line_number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith(("```", "~~~")):
            flush()
            fenced = not fenced
            continue
        if fenced:
            continue
        if comment:
            if "-->" in stripped:
                comment = False
            continue
        if stripped.startswith("<!--"):
            flush()
            comment = "-->" not in stripped
            continue
        if not stripped:
            flush()
            continue
        if (
            stripped.startswith(("#", "|", ">"))
            or raw.startswith("    ")
            or IMAGE.match(stripped)
        ):
            flush()
            continue
        if LIST_ITEM.match(raw):
            flush()
            blocks.append(Block(line_number, LIST_ITEM.sub("", raw), False))
            continue
        if not paragraph:
            paragraph_line = line_number
        paragraph.append(stripped)
    flush()
    return blocks


def normalized_prose(text: str) -> str:
    """Prose with code spans, link targets, raw URLs and emphasis removed, so
    that a long path or a long URL cannot read as a long sentence."""
    text = INLINE_CODE.sub("", text)
    text = LINK.sub(r"\1", text)
    text = REFERENCE_LINK.sub(r"\1", text)
    text = RAW_URL.sub("", text)
    return re.sub(r"[*_~]", "", text).strip()


def sentences(text: str) -> list[str]:
    """One block's sentences; empty when nothing prose-like survives normalisation."""
    normalized = normalized_prose(text)
    if not normalized:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", normalized) if part.strip()]


def analyze(text: str) -> list[Finding]:
    """Every limit one document breaks: sentence words, then paragraph words
    and paragraph sentences, which only whole paragraphs are held to."""
    findings: list[Finding] = []
    for block in prose_blocks(text):
        block_sentences = sentences(block.text)
        for sentence in block_sentences:
            count = len(WORD.findall(sentence))
            if count > MAX_SENTENCE_WORDS:
                findings.append(
                    Finding(
                        block.line,
                        f"sentence has {count} words; maximum is {MAX_SENTENCE_WORDS}",
                        sentence,
                    )
                )
        if not block.paragraph:
            continue
        paragraph_words = sum(len(WORD.findall(item)) for item in block_sentences)
        if paragraph_words > MAX_PARAGRAPH_WORDS:
            findings.append(
                Finding(
                    block.line,
                    f"paragraph has {paragraph_words} words; maximum is {MAX_PARAGRAPH_WORDS}",
                    block.text,
                )
            )
        if len(block_sentences) > MAX_PARAGRAPH_SENTENCES:
            findings.append(
                Finding(
                    block.line,
                    "paragraph has too many sentences",
                    block.text,
                )
            )
    return findings


def selftest() -> int:
    """Prove the limits fire at eleven words and never on exempt material."""
    ten_words = "One two three four five six seven eight nine ten."
    eleven_words = ten_words[:-1] + " eleven."
    exemptions = """# Heading words never count here

| A very long table sentence exceeds every prose limit safely. |

> A quoted normative statement may exceed the prose limit safely.

```sh
one very long command line remains exempt from prose policy checks
```

![A deliberately extensive image description stays exempt](diagram.svg)
"""
    if analyze(ten_words):
        print("selftest: exact-limit sentence failed")
        return 1
    if not any("sentence has 11 words" in item.reason for item in analyze(eleven_words)):
        print("selftest: long sentence escaped")
        return 1
    if analyze(exemptions):
        print("selftest: exempt material failed")
        return 1
    long_paragraph = ("One two three four five six seven. "
                      "Eight nine ten eleven twelve thirteen fourteen. "
                      "Fifteen sixteen seventeen eighteen nineteen twenty twenty-one.")
    reasons = {item.reason for item in analyze(long_paragraph)}
    if "paragraph has too many sentences" not in reasons:
        print("selftest: long paragraph escaped")
        return 1
    print("documentation style selftest: OK")
    return 0


def main() -> int:
    """Judge every current audience document; 1 on any finding, 2 on a bad argument."""
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:
        print(__doc__)
        return 2

    missing = [path for path in DOCUMENTS if not path.is_file()]
    if missing:
        for path in missing:
            print(f"missing current document: {path.relative_to(ROOT)}")
        return 1

    failures = 0
    for path in DOCUMENTS:
        for finding in analyze(path.read_text(encoding="utf-8")):
            failures += 1
            excerpt = " ".join(finding.text.split())
            print(f"{path.relative_to(ROOT)}:{finding.line}: {finding.reason}: {excerpt}")
    if failures:
        print(f"documentation style: FAIL ({failures} findings)")
        return 1
    print(f"documentation style: OK ({len(DOCUMENTS)} current documents)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
