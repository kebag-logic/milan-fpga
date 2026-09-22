#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""I437 list paragraph fixtures and the five retained heading omissions.

These are fresh reconstructions of PR #428 R86-5's public descriptions,
not copies of its unpublished shapes files or a per-ID correspondence.
GitHub's GFM renderer supplies the expected heading presence. The reset rows
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


def correction_rows() -> list[tuple[str, str, bool]]:
    """Public R237/R238 counterexamples plus synthetic paragraph boundaries.

    R238 C/D/P rows preserve the published page bytes. R237's marker
    controls indent the closer so a falsely seeded item remains observable.
    Matrix rows vary the tag column independently of the item's column.
    """
    rows = [
        ("R238 C01",
            "- item\n\n  text\n  <span>\n## Old\n  </span>\n\n## Real\n", True),
        ("R238 C02",
            "- item\n\n  text\n   <span>\n## Old\n   </span>\n\n## Real\n", True),
        ("R238 C03",
            "1. item\n\n   text\n   <span>\n## Old\n   </span>\n\n## Real\n", True),
        ("R238 C04",
            "- item\n\n  text\n  <span>\n```\n\n## Old\n```\n\n## Real\n", False),
        ("R238 C05",
            "- item\n\n  text\n  <span>\n<!--\n\n## Old\n-->\n\n## Real\n", False),
        ("R238 C06",
            "- item\n\n  text\n  <span>\n<pre>\n\n## Old\n</pre>\n\n## Real\n", False),
        ("R238 C07",
            "- item\n\n  text\nlazy\n  <span>\n```\n\n## Old\n```\n\n## Real\n", False),
        ("R238 C08",
            "1. item\n\n   text\n   <span>\n```\n\n## Old\n```\n\n## Real\n", False),
        ("R238 P01",
            "- item\n  <span>\n```\n\n## Old\n```\n\n## Real\n", False),
        ("R238 P04",
            "- item\n  <span>\n## Old\n  </span>\n\n## Real\n", True),
        ("R238 D01",
            "- item\n> quote\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
        ("R238 D02",
            "- item\n[^1]: note\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
        ("R238 D03",
            "- item\n> quote\n\n  text\n<span>\n```\n\n## Old\n```\n\n## Real\n", False),
        ("R238 D04",
            "- item\n[^1]: note\n\n  text\n<span>\n```\n\n## Old\n```\n\n## Real\n", False),
        ("R238 D05",
            "- item\n\n> quote\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
        ("R238 D06",
            "- item\n  > quote\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", False),
        ("R238 D07",
            "-   item\n  > quote\n\n    text\n<span>\n## Old\n</span>\n\n## Real\n", False),
        ("R237 fenced-marker-indented-closer",
            "```\n- fake item\n  ```\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
        ("R237 comment-marker-indented-closer",
            "<!--\n- fake item\n  -->\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
        ("R237 HTML-marker-indented-closer",
            "<div>\n- fake item\n  </div>\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
    ]
    for phase, prefix in [("first", "- item"), ("resumed", "- item\n\n  text")]:
        for column in range(5):
            for form, tag in [("open", "<span>"), ("close", "</span>"),
                              ("attribute", '<span title="x">')]:
                name = f"{phase} tag column {column} {form}"
                start = f"{prefix}\n{' ' * column}{tag}\n"
                rows.append((name, start + "## Old\n</span>\n\n## Real\n", column >= 2))
                if column >= 2:
                    for kind, opener, closer in [("fence", "```", "```"),
                                                  ("comment", "<!--", "-->"),
                                                  ("pre", "<pre>", "</pre>")]:
                        rows.append((f"{name} then {kind}",
                                     start + f"{opener}\n\n## Old\n{closer}\n\n## Real\n", False))
                else:
                    for kind, opener in [("fence", "```"), ("closed comment", "<!--\n-->"), ("pre", "<pre>")]:
                        rows.append((f"{name} swallows {kind}",
                                     start + f"{opener}\n\n## Old\n</span>\n\n## Real\n", True))
    for name, prefix, tag_column, visible in [
        ("ordered first", "1. item", 3, True),
        ("ordered below column", "1. item\n\n   text", 2, False),
        ("star first", "* item", 2, True),
        ("plus resumed", "+ item\n\n  text", 2, True),
        ("empty gains paragraph", "-\n  text", 2, True),
        ("empty resumed paragraph", "-\n  text\n\n  more", 2, True),
        ("lazy resumed paragraph", "- item\n\n  text\nlazy", 2, True),
        ("sibling first paragraph", "- item\n1. next", 3, True),
        ("sibling replaces boundary", "- item\n1. next", 2, False),
    ]:
        rows.append((name, f"{prefix}\n{' ' * tag_column}<span>\n## Old\n</span>\n\n## Real\n", visible))
    for kind, marker in [("quote", "> quote"), ("footnote", "[^1]: note")]:
        for column in range(3):
            prefix = f"- item\n{' ' * column}{marker}\n\n  text\n<span>\n"
            rows.append((f"{kind} column {column} releases iff dedented",
                         prefix + "## Old\n</span>\n\n## Real\n", column < 2))
    return rows


def _correction_holds(visible: bool) -> object:
    """Score the heading and the navigation plan, including block recovery."""
    from gen_toc import plan
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    return lambda page: ([h[1] for h in headings(page)] == (["Old", "Real"] if visible else ["Real"])
                         and ("old" in [h[2] for h in plan(page + tail)]) == visible)


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
    arms.extend((f"I437 {name}", page, _correction_holds(visible))
                for name, page, visible in correction_rows())
    return arms


def em_dash_arms(gate: ModuleType) -> tuple[list[str], int]:
    """Judge copied labels through real Git base/head commits and provenance.

    Every head contains legitimate generated navigation; an absent base
    heading must yield the specific mirrors-no-heading finding. Positive
    boundary controls must still obtain exactly one exemption.
    """
    rows = [(name, f"{prefix}\n<{tag}>\n## Old\n</{tag}>\n", visible)
            for name, prefix, tag, visible in probe_rows()] + correction_rows()
    problems = []
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
        for i, (_, page, _) in enumerate(rows):
            (repo / f"page{i}.md").write_text(
                "# Page\n\n" + page.replace("## Old\n", heading).replace("\n## Real\n", "") + tail, encoding="utf-8")
        base = gate._commit(repo, "I437 base")
        for i in range(len(rows)):
            (repo / f"page{i}.md").write_text("# Page\n\n" + navigation + heading + tail, encoding="utf-8")
        gate._commit(repo, "I437 head")
        for i, (name, _, visible) in enumerate(rows):
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
