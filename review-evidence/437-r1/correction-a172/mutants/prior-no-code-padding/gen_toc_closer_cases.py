#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""I440 controls: literal HTML closers, fence trailers, and copied labels.

Only fixtures and expected answers live here; gen_toc owns every Markdown
decision. Character rows reconstruct the population in PR #428 R85-8 and
R86-9: Python whitespace outside space/tab/LF, plus valid blank controls,
inner blanks, ASCII capitals, Unicode folds and cross-name closers. The
raw walk keeps CR inside a line; shipped text readers normalize it first.
These controls preserve that boundary and the existing refusal policy.
"""
import tempfile
from pathlib import Path
from types import ModuleType

from gen_toc import FENCE, HTML, TEXT


# Independent of REFUSED and RAW_HTML_TAGS to hold both name-set boundaries.
_CHARACTERS = ("\v\f\r\x1c\x1d\x1e\x1f\x85\xa0\u1680\u2000\u2001\u2002"
               "\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028"
               "\u2029\u202f\u205f\u3000")
_NAMES = ("pre", "script", "style", "textarea")
_OTHER_NAMES = ("div", "title", "xmp")
_FOLDS = ("\u017fcript", "\u017ftyle", "scr\u0131pt", "scr\u0130pt")


def _probe_kind(expected: str) -> object:
    """The probe heading's block kind, immediately before the final LF."""
    return lambda kinds: kinds[-2] == expected


def closer_arms() -> list[tuple[str, str, object]]:
    """I440 raw-walk arms, graded before refusal can mask a wrong closer."""
    arms = []
    for fence in ("```", "~~~"):
        for trailer in ("", " ", "\t", " \t "):
            arms.append((f"I440-F-valid {fence!r} {trailer!r}",
                         f"{fence}\n{fence}{trailer}\n## Probe\n", _probe_kind(TEXT)))
        for trailer in _CHARACTERS + "x":
            arms.append((f"I440-F-invalid {fence!r} U+{ord(trailer):04X}",
                         f"{fence}\n{fence}{trailer}\n## Probe\n", _probe_kind(FENCE)))
    for opener in _NAMES:
        for joiner in ("\n", "x"):
            for closer in _NAMES:
                for name in (closer, closer.upper()):
                    arms.append((f"I440-T-valid {opener}/{name} {joiner!r}",
                                 f"<{opener}>{joiner}</{name}>\n## Probe\n", _probe_kind(TEXT)))
            for blank in (*_CHARACTERS, " ", "\t", "  ", " \t "):
                arms.append((f"I440-T-inner {opener} {joiner!r} {blank!r}",
                             f"<{opener}>{joiner}</{opener}{blank}>\n## Probe\n", _probe_kind(HTML)))
            for name in _FOLDS:
                arms.append((f"I440-T-fold {opener}/{name} {joiner!r}",
                             f"<{opener}>{joiner}</{name}>\n## Probe\n", _probe_kind(HTML)))
            for name in _OTHER_NAMES:
                arms.append((f"I440-T-other-name {opener}/{name} {joiner!r}",
                             f"<{opener}>{joiner}</{name}>\n## Probe\n", _probe_kind(HTML)))
    arms += [
        ("I440-T-embedded closer anywhere in the line",
         "<pre>\ntext </sTyLe> tail\n## Probe\n", _probe_kind(TEXT)),
        ("I440-T-prefix longer names are no closer",
         "<pre>\n</prelude>\n## Probe\n", _probe_kind(HTML)),
        ("I440-T-slash blank after slash is no closer",
         "<pre>\n</ pre>\n## Probe\n", _probe_kind(HTML)),
        ("I440-T-reset a subsequent block still needs its own closer",
         "<pre></style>\n<script>\n## Probe\n", _probe_kind(HTML)),
        ("I440-T-precedence a type-1 closer cannot end type 6",
         "<div>\n</pre>\n## Probe\n", _probe_kind(HTML)),
        ("I440-F-precedence a type-1 closer cannot end a fence",
         "```\n</pre>\n## Probe\n", _probe_kind(FENCE)),
    ]
    return arms


def _label_rows() -> list[tuple[str, str, int, int]]:
    """(ID, prefix before old heading, findings, exemptions) after unwrap.

    Findings count the copied LABEL, with the heading retained by Git's
    diff. Refused base characters add a named refusal finding. CR rows
    pass through real Git text reads and therefore use normalized lines.
    """
    return [
        ("I440-E-space", "<pre>\n</pre >\n", 1, 0),
        ("I440-E-tab", "<pre>\n</pre\t>\n", 1, 0),
        ("I440-E-inline", "<pre>x</pre >\n", 1, 0),
        ("I440-E-inline-tab", "<pre>x</pre\t>\n", 1, 0),
        ("I440-E-cross", "<pre>\n</style>\n", 0, 1),
        ("I440-E-cross-inline", "<pre>x</TEXTAREA>\n", 0, 1),
        ("I440-E-ascii", "<script>\n</SCRIPT>\n", 0, 1),
        ("I440-E-other-div", "<pre>\n</div>\n", 1, 0),
        ("I440-E-other-title", "<pre>\n</title>\n", 1, 0),
        ("I440-E-other-xmp", "<pre>\n</xmp>\n", 1, 0),
        ("I440-E-other-div-inline", "<pre>x</div>\n", 1, 0),
        ("I440-E-other-title-inline", "<pre>x</title>\n", 1, 0),
        ("I440-E-other-xmp-inline", "<pre>x</xmp>\n", 1, 0),
        ("I440-E-long-s", "<script>\n</\u017fcript>\n", 1, 0),
        ("I440-E-dotless-i", "<script>\n</scr\u0131pt>\n", 1, 0),
        ("I440-E-dotted-i", "<script>x</scr\u0130pt>\n", 1, 0),
        ("I440-E-fence-ff", "```\n```\f\n", 2, 0),
        ("I440-E-fence-nbsp", "~~~\n~~~\u00a0\n", 2, 0),
        ("I440-E-inner-ff", "<pre>\n</pre\f>\n", 2, 0),
        ("I440-E-fence-tab", "```\n```\t\n", 0, 1),
        ("I440-E-fence-crlf", "```\r\n```\r\n", 0, 1),
        # Git's LF-delimited diff adds the heading even though its text
        # reader normalizes CR and the copied label is correctly exempt.
        ("I440-E-fence-cr", "```\r```\r", 1, 1),
        ("I440-E-inner-cr", "<pre>\n</pre\r>\n", 1, 0),
    ]


def em_dash_arms(gate: ModuleType) -> tuple[list[str], int]:
    """Exercise the shipped gate on real base/head commits, one row per page.

    The head has legitimate generated navigation. Only the base's actual
    headings can authorize its label, so a wrong closer cannot hide behind
    missing provenance. No alternate Markdown parser or gate lives here.
    """
    rows, problems = _label_rows(), []
    heading = "## Old \u2014 heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    navigation = ("## Contents\n\n"
                  "- **[Old \u2014 heading](#old--heading)** -- Copied.\n"
                  "- **[Alpha](#alpha)** -- What alpha holds.\n"
                  "- **[Beta](#beta)** -- What beta holds.\n"
                  "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    with tempfile.TemporaryDirectory(prefix="i440.emdash.") as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for name, prefix, _, _ in rows:
            (repo / f"{name}.md").write_bytes(("# Page\n\n" + prefix + heading + tail).encode("utf-8"))
        base = gate._commit(repo, "I440 base")
        for name, _, _, _ in rows:
            (repo / f"{name}.md").write_text("# Page\n\n" + navigation + heading + tail, encoding="utf-8")
        gate._commit(repo, "I440 head")
        for name, _, findings, exemptions in rows:
            verdict = gate.Verdict()
            path = f"{name}.md"
            gate.judge_page(repo, base, gate.Change(path, path), verdict)
            if (len(verdict.findings), verdict.exempt) != (findings, exemptions):
                problems.append(f"[{name}] findings/exempt expected {findings}/{exemptions}, "
                                f"got {len(verdict.findings)}/{verdict.exempt}: {verdict.findings}")
            if findings and not exemptions and not any("mirrors no heading" in note for note in verdict.findings):
                problems.append(f"[{name}] copied label was not judged against the base heading")
            if findings == 2 and not any("at column" in note for note in verdict.findings):
                problems.append(f"[{name}] base character refusal was not named")
    return problems, len(rows)
