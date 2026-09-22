#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""I437 list paragraph fixtures and the five retained heading omissions.

These are fresh reconstructions of PR #428 R86-5's public descriptions,
not copies of its unpublished shapes files. GitHub's GFM renderer supplies
the expected heading presence. The boundary and reset rows independently
hold the content column, item lifetime and block precedence. This module
contains no Markdown classifier; gen_toc owns every decision.
"""
import tempfile
from pathlib import Path
from types import ModuleType

from gen_toc import HTML, TEXT, blocks, headings


def probe_rows() -> list[tuple[str, str, str, bool]]:
    """(Name, predecessor, tag, whether Old renders), measured with GFM."""
    return [
        ("two spaces", "- item\n\n  text", "span", False),
        ("three spaces", "- item\n\n   text", "span", False),
        ("star item", "* item\n\n  text", "span", False),
        ("ordered item", "1. item\n\n   text", "span", False),
        ("two paragraphs", "- item\n\n  first\n\n  text", "span", False),
        ("task item", "- [ ] item\n\n  text", "span", False),
        ("interrupting item", "text\n- item\n\n  text", "span", False),
        ("bold tag", "- item\n\n  text", "b", False),
        ("two blank lines", "- item\n\n\n  text", "span", False),
        ("plus item", "+ item\n\n  text", "span", False),
        ("custom tag", "- item\n\n  text", "custom-tag", False),
        ("one space outside item", "- item\n\n text", "span", True),
        ("four spaces", "- item\n\n    text", "span", False),
        ("quote boundary", "> item\n\n  text", "span", True),
        ("footnote two spaces", "[^1]: note\n\n  text", "span", True),
        ("footnote four spaces", "[^1]: note\n\n    text", "span", False),
        ("tab continuation", "- item\n\n\ttext", "span", False),
        ("no item", "plain\n\n  text", "span", True),
        ("padding outside", "-  item\n\n  text", "span", True),
        ("padding inside", "-  item\n\n   text", "span", False),
        ("ordered outside", "1. item\n\n  text", "span", True),
        ("marker indent outside", " - item\n\n  text", "span", True),
        ("marker indent inside", " - item\n\n   text", "span", False),
        ("code padding uses one", "-     code\n\n  text", "span", False),
        ("four padding columns", "-    item\n\n   text", "span", True),
        ("tab padding columns", "- \titem\n\n   text", "span", True),
        ("empty item ends at blank", "-\n\n  text", "span", True),
        ("empty padded item ends at blank", "-   \n\n  text", "span", True),
        ("empty item gains content", "-\n  first\n\n  text", "span", False),
        ("empty item ignores padding", "-   \n  first\n\n  text", "span", False),
        ("nested item retains outer column", "- item\n  - nested\n\n  text", "span", False),
        ("sibling replaces column", "- item\n\n1. item\n\n  text", "span", True),
        ("fresh dedented paragraph ends item", "- item\n\noutside\n\n  text", "span", True),
        ("lazy line retains item", "- item\nlazy\n\n  text", "span", False),
        ("heading ends item", "- item\n\n## Outside\n\n  text", "span", True),
        ("fenced marker is inert", "```\n- item\n```\n\n  text", "span", True),
        ("commented marker is inert", "<!--\n- item\n-->\n\n  text", "span", True),
        ("HTML marker is inert", "<div>\n- item\n</div>\n\n  text", "span", True),
        ("code marker is inert", "    - item\n\n  text", "span", True),
        ("thematic break is no item", "- - -\n\n  text", "span", True),
        ("noninterrupting ordinal is no item", "text\n2. item\n\n   text", "span", True),
        ("setext dash is no item", "text\n-\n\n  text", "span", True),
    ]


def _probe_holds(visible: bool) -> object:
    """Check the probe's block label, its anchor, and recovery after HTML."""
    return lambda page: (blocks(page)[-5] == (TEXT if visible else HTML)
                         and ("old" in [h[2] for h in headings(page)]) == visible
                         and headings(page)[-1] == (2, "Real", "real"))


def container_arms() -> list[tuple[str, str, object]]:
    """Raw classification and heading assertions, independent of policy."""
    arms = [(f"I437 {name}", f"{prefix}\n<{tag}>\n## Old\n</{tag}>\n\n## Real\n",
             _probe_holds(visible)) for name, prefix, tag, visible in probe_rows()]
    for name, page in [
        ("equals setext", "Alpha\n===\n"),
        ("hyphen setext", "text\n---\n"),
        ("single hyphen setext", "text\n-\n"),
        ("quoted heading", "> ## Q\n"),
        ("list heading", "- item\n\n  ## Inner\n"),
    ]:
        arms.append((f"I437 limitation {name}", page, lambda text: headings(text) == []))
    return arms


def em_dash_arms(gate: ModuleType) -> tuple[list[str], int]:
    """Judge copied labels through real Git base/head commits and provenance.

    Every head contains legitimate generated navigation; an absent base
    heading must yield the specific mirrors-no-heading finding. Positive
    boundary controls must still obtain exactly one exemption.
    """
    rows, problems = probe_rows(), []
    heading = "## Old \u2014 heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    navigation = ("## Contents\n\n"
                  "- **[Old \u2014 heading](#old--heading)** -- Copied.\n"
                  "- **[Alpha](#alpha)** -- What alpha holds.\n"
                  "- **[Beta](#beta)** -- What beta holds.\n"
                  "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    with tempfile.TemporaryDirectory(prefix="i437.emdash.") as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for i, (_, prefix, tag, _) in enumerate(rows):
            (repo / f"page{i}.md").write_text(
                f"# Page\n\n{prefix}\n<{tag}>\n{heading}</{tag}>\n{tail}", encoding="utf-8")
        base = gate._commit(repo, "I437 base")
        for i in range(len(rows)):
            (repo / f"page{i}.md").write_text("# Page\n\n" + navigation + heading + tail, encoding="utf-8")
        gate._commit(repo, "I437 head")
        for i, (name, _, _, visible) in enumerate(rows):
            verdict = gate.Verdict()
            path = f"page{i}.md"
            gate.judge_page(repo, base, gate.Change(path, path), verdict)
            expected = (0, 1) if visible else (1, 0)
            if (len(verdict.findings), verdict.exempt) != expected:
                problems.append(f"[I437 {name}] expected findings/exempt {expected}, "
                                f"got {len(verdict.findings)}/{verdict.exempt}: {verdict.findings}")
            if not visible and not any("mirrors no heading" in note for note in verdict.findings):
                problems.append(f"[I437 {name}] absent base heading was not the refusal reason")
    return problems, len(rows)
