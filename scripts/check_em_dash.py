#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: no U+2014 (the em dash) in the Markdown lines a change adds.

Why this exists. Since #98, #99 and #101 every merged documentation change
has replaced the em dash with ``--`` or `` - `` on the lines it touched and
reviewers have refused new ones, but no page stated the rule and no gate
read the character: on PR #370 two reviewers disagreed on the same added
line (#378). The rule, as CONTRIBUTING.md states it: no U+2014 in any text
a branch writes - prose, headings, table cells, fenced text and the
separator of a Contents entry. One exemption: a Contents label that
gen_toc.py copies verbatim from a heading the page already had at the base,
because rewording such a heading moves its anchor. Existing pages are not
rewritten - the tree carries the character on 145 of its 158 pages - so the
gate judges the lines a change ADDS between a base commit and HEAD, never
the tree.

What is judged. ``git diff -U0 -M --text <base> HEAD`` over every tracked
``*.md``, renames followed so a moved page is judged on its changed lines
only, and every page compared as text whatever a ``.gitattributes`` entry
says: a ``-diff`` attribute made git print ``Binary files differ`` with no
hunk at all, and a page with no hunk was a page with nothing to judge ([R0]
on PR #384). Should git still report a binary difference, the page is
refused, never counted clean. A rename git does not pair with its old path
is judged as a new page, which is the safe direction.

Every added line carrying the character is a finding unless PROVENANCE says
it is generated navigation: the line must be byte-identical, at its own
position, to the line ``gen_toc.py`` renders for that page, which that
script answers through ``generated_block``. Nothing here parses Markdown.
Five review rounds on PR #384 showed why: this gate carried its own fence,
comment and indentation walks, and each round found another construct the
two readers disagreed about -- a longer fence, a tilde fence, an indented
opener, an indented code block, an HTML comment, a raw ``<pre>`` block --
until the walk refused a legitimate page over a fence marker inside an old
comment. Provenance ends the class: hand-written text is judged wherever it
sits, and a copy of a block written where nothing renders it is hand-written
text. Even on a generated line only the LABEL span can be exempt, and only
when the heading it copies is one the BASE version of the page rendered, so
a label mirroring a heading the same change introduces is refused with its
heading, and one mirroring heading syntax that exists only inside a comment
is refused too. The page must also be one whose Contents block that script
writes: the two documentation indexes, the historical tree and pages another
generator owns carry no generated navigation, so nothing on them is exempt.

The base is explicit and, in CI, DERIVED. Locally pass the merge base. The
docs workflow fetches the pull request's base BRANCH and takes the merge
base against the checked-out tree, because GitHub freezes
``pull_request.base.sha`` when the request opens while the job builds the
merge into the current base tip, so the recorded oid attributes to this
branch every line merged into the base since. A push judges from its own
``before`` SHA, and an event carrying neither is refused rather than guessed
at. The planted controls run on every
invocation, before any verdict: a gate that has never failed once is not
evidence that it works.

    python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
    python3 scripts/check_em_dash.py --selftest    # the planted controls alone

Exit 0 = clean; 1 = findings, one per line as ``path:line: message``; 2 =
cannot judge (no git, a base that is not a commit, a page git will only
report as binary) or an arm that did not bite, which is unproven, not clean.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# The Contents entry, the heading, the fence and the label transform are
# OWNED by gen_toc.py, which writes the entries this gate reads; lifting them
# rather than restating them is what keeps the two from disagreeing.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_toc import (TOC_ENTRY_RE, generated_block, headings, label,
                     refusal_notes,
                     line_kinds)

REPO = Path(__file__).resolve().parent.parent

#: Assembled from its code point, so this file never carries the character
#: it refuses and the self-test fixtures never spell it either.
EM_DASH = "\u2014"
HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
#: `--text` compares every page as text whatever its diff attribute or
#: driver says; `--no-textconv` and `--no-ext-diff` keep a configured driver
#: from rewriting what is compared; the prefixes are fixed so a user's
#: `diff.noprefix` cannot change the header shape.
DIFF_FLAGS = ("-U0", "-M", "--text", "--no-textconv", "--no-color",
              "--no-ext-diff", "--diff-algorithm=myers", "--src-prefix=a/",
              "--dst-prefix=b/")
REMEDY = "write --, a colon or a plain sentence"


class Refusal(Exception):
    """The judgement cannot run: no git, a revision that is not a commit,
    or a page whose added lines git will not establish."""


@dataclass(frozen=True)
class Change:
    """One changed page: its path at HEAD, and at the base (None when new)."""

    path: str
    base_path: str | None


@dataclass(frozen=True)
class Added:
    """One line HEAD adds: the page, its line number there, and its text."""

    path: str
    lineno: int
    text: str


@dataclass
class Verdict:
    """What one judgement found: the findings, how many added lines it read
    over how many pages, and how many mirrored labels the exemption passed."""

    findings: list[str] = field(default_factory=list)
    judged: int = 0
    pages: int = 0
    exempt: int = 0


def git(repo: Path, *args: str, env: dict[str, str] | None = None) -> str:
    """stdout of one git command in ``repo``; a failure is a Refusal."""
    try:
        out = subprocess.run(["git", "-C", str(repo), *args],
                             capture_output=True, text=True,
                             encoding="utf-8", errors="replace", env=env)
    except OSError as exc:
        raise Refusal(f"cannot run git: {exc}") from exc
    if out.returncode != 0:
        why = out.stderr.strip() or f"exit {out.returncode}"
        raise Refusal(f"git {' '.join(args[:2])}: {why}")
    return out.stdout


def require_commit(repo: Path, rev: str) -> str:
    """The full SHA of ``rev``, or a Refusal naming it: the base is the
    contract, and a guessed one judges other lines."""
    try:
        return git(repo, "rev-parse", "--verify", "--quiet",
                   f"{rev}^{{commit}}").strip()
    except Refusal as exc:
        raise Refusal(f"`{rev}` is not a commit in this repository") from exc


def changed_pages(repo: Path, base: str) -> list[Change]:
    """Every tracked Markdown page HEAD adds, modifies or renames since
    ``base``, in git's order; a deleted page adds no line."""
    raw = git(repo, "diff", "--name-status", "-z", "-M", base, "HEAD",
              "--", "*.md")
    fields = raw.split("\0")
    out, i = [], 0
    while i < len(fields) and fields[i]:
        status = fields[i][0]
        if status in "RC":
            out.append(Change(fields[i + 2], fields[i + 1]))
            i += 3
            continue
        if status != "D":
            out.append(Change(fields[i + 1],
                              None if status == "A" else fields[i + 1]))
        i += 2
    return out


def added_lines(repo: Path, base: str, change: Change) -> list[Added]:
    """The lines HEAD adds to one page, with their HEAD line numbers, as
    git's own diff reports them. Both paths of a rename are named so the
    rename is detected inside the pathspec and only its changed lines are
    added; `:(literal)` keeps a glob character in a path from expanding. A
    page git will only report as a binary difference is refused: its added
    lines cannot be established, so it cannot be counted clean."""
    spec = [f":(literal){p}" for p in dict.fromkeys(
        (change.path, change.base_path)) if p]
    raw = git(repo, "diff", *DIFF_FLAGS, base, "HEAD", "--", *spec)
    out, lineno, in_hunk = [], 0, False
    for line in raw.split("\n"):
        if line.startswith("diff --git "):
            in_hunk = False
            continue
        if not in_hunk and line.startswith("Binary files "):
            raise Refusal(f"{change.path}: git reports a binary difference, "
                          "so its added lines cannot be established")
        m = HUNK_RE.match(line)
        if m:
            lineno, in_hunk = int(m.group(1)), True
            continue
        if not in_hunk:
            continue
        if line.startswith("+"):
            out.append(Added(change.path, lineno, line[1:]))
            lineno += 1
        elif line.startswith(" "):
            lineno += 1
    return out


def base_labels(repo: Path, base: str, change: Change) -> set[str]:
    """The Contents labels gen_toc writes for the headings the BASE version
    of the page carries: the whole exemption, decided here and nowhere
    else."""
    if change.base_path is None:
        return set()
    text = git(repo, "show", f"{base}:{change.base_path}")
    return {label(raw) for _, raw, _ in headings(text)}


def _entry_findings(where: str, hit: Added, entry: re.Match[str],
                    exempt_labels: set[str], verdict: Verdict) -> None:
    """The findings one added Contents entry carries. Only the label span
    can be exempt, and only when the base page had that heading; the link
    target, the separator, the description and every other character of
    the line are judged as the rule judges any added text."""
    lab = entry.group(1)
    if EM_DASH in lab:
        if lab in exempt_labels:
            verdict.exempt += 1
        else:
            verdict.findings.append(
                f"{where}: U+2014 (em dash) in a Contents label that mirrors "
                "no heading the base version of this page had -- reword the "
                "new heading, then regenerate the block")
    parts = (("in the link target of a Contents entry -- the anchor is "
              "gen_toc's to write", entry.group(2)),
             ("as the Contents separator -- switch this page's separator "
              "to --", entry.group(3)),
             (f"in a Contents description -- {REMEDY}", entry.group(4)))
    named = 0
    for what, part in parts:
        if EM_DASH in part:
            named += part.count(EM_DASH)
            verdict.findings.append(f"{where}: U+2014 (em dash) {what}")
    rest = hit.text[:entry.start(1)] + hit.text[entry.end(1):]
    if rest.count(EM_DASH) > named:
        verdict.findings.append(
            f"{where}: U+2014 (em dash) outside the label of a Contents "
            f"entry -- {REMEDY}")


def judge_page(repo: Path, base: str, change: Change,
               verdict: Verdict) -> None:
    """Every finding one page's added lines carry, appended to ``verdict``.

    The exemption is decided by PROVENANCE, not by context: an added line
    can carry a copied heading label only when it is byte-identical to the
    line `gen_toc.py` itself renders for this page at this position, which
    that script answers through `generated_block`. Nothing here parses
    Markdown. Anything a person wrote by hand is judged wherever it sits,
    which is what makes a Contents block quoted inside a fence, an indented
    code block, an HTML comment or a raw HTML block judged text without a
    rule for each ([R0] rounds 4 and 5 on PR #384). The page's HEAD text is
    read only when an added line carries the character.
    """
    added = added_lines(repo, base, change)
    verdict.judged += len(added)
    hits = [a for a in added if EM_DASH in a.text]
    if not hits:
        return
    text = git(repo, "show", f"HEAD:{change.path}")
    # A page the walk REFUSES to read has no provenance at all, so no
    # label on it can be exempt; say why, or the author sees only that a
    # generated line was refused ([R85] F1, [R86] F1, round 9 on PR #428).
    verdict.findings += [f"{note}, so no Contents label on it is exempt"
                         for note in refusal_notes(change.path, text)]
    # The PATH is part of the question: `gen_toc.py` does not write a
    # Contents block for the two documentation indexes, for the historical
    # tree or for another generator's pages, so nothing on them is ever
    # generated navigation ([R0] round 6 on PR #384).
    kinds = line_kinds(text)
    block = generated_block(text, change.path)
    exempt_labels = None
    for hit in hits:
        where = f"{hit.path}:{hit.lineno}"
        at = hit.lineno - 1
        entry = None
        if block is not None and 0 <= at - block[0] < len(block[1]) \
                and hit.text == block[1][at - block[0]]:
            entry = TOC_ENTRY_RE.match(hit.text)
        if entry is None:
            verdict.findings.append(
                f"{where}: U+2014 (em dash) in an added "
                f"{kinds[at] if at < len(kinds) else 'line'} -- {REMEDY}")
            continue
        if exempt_labels is None:
            exempt_labels = base_labels(repo, base, change)
        _entry_findings(where, hit, entry, exempt_labels, verdict)


def judge(repo: Path, base: str) -> Verdict:
    """The verdict over every Markdown page changed between ``base`` and
    HEAD, findings sorted; a Refusal when either is not a commit."""
    for rev in (base, "HEAD"):
        require_commit(repo, rev)
    verdict = Verdict()
    for change in changed_pages(repo, base):
        verdict.pages += 1
        judge_page(repo, base, change, verdict)
    # By page, then by line NUMBER: a string sort puts line 100 before
    # line 10 ([R10] round 5 on PR #384).
    verdict.findings.sort(key=lambda f: (f.rsplit(":", 2)[0],
                                         int(f.rsplit(":", 2)[1])))
    return verdict


# --------------------------------------------------------------------------
# the planted controls, each in a repository built here
# --------------------------------------------------------------------------

#: A page with a Contents block that predates the rule: em-dash separators,
#: one label mirroring an em-dash heading. The anchors are gen_toc's. The
#: filler lines are load-bearing: git pairs a renamed file with its old path
#: by CONTENT similarity, and on a page of a dozen lines a legitimate edit
#: drops below the default threshold, so the rename control would prove
#: nothing about renames.
_WITH_TOC = f"""# With a contents list

Prose with no dash.

## Contents

- **[Old {EM_DASH} heading](#old--heading)** {EM_DASH} What the old section holds.
- **[Plain](#plain)** {EM_DASH} What the plain section holds.
- **[Table](#table)** {EM_DASH} A table.

## Old {EM_DASH} heading

Body.

## Plain

Body.

## Table

| Column | Value |
|---|---|
| a | b |

Filler sentence 1 keeps this page long enough for git to pair it across a rename.
Filler sentence 2 keeps this page long enough for git to pair it across a rename.
Filler sentence 3 keeps this page long enough for git to pair it across a rename.
Filler sentence 4 keeps this page long enough for git to pair it across a rename.
Filler sentence 5 keeps this page long enough for git to pair it across a rename.
Filler sentence 6 keeps this page long enough for git to pair it across a rename.
Filler sentence 7 keeps this page long enough for git to pair it across a rename.
Filler sentence 8 keeps this page long enough for git to pair it across a rename.
Filler sentence 9 keeps this page long enough for git to pair it across a rename.
Filler sentence 10 keeps this page long enough for git to pair it across a rename.
Filler sentence 11 keeps this page long enough for git to pair it across a rename.
Filler sentence 12 keeps this page long enough for git to pair it across a rename.
"""

#: The same headings with no Contents block yet: the branch writes the
#: block for the first time, with the separator gen_toc now defaults to.
_NO_TOC = f"""# Without a contents list

## Old {EM_DASH} heading

Body.

## Plain

Body.

## Table

Body.

Filler sentence 1 keeps this page long enough for git to pair it across a rename.
Filler sentence 2 keeps this page long enough for git to pair it across a rename.
Filler sentence 3 keeps this page long enough for git to pair it across a rename.
Filler sentence 4 keeps this page long enough for git to pair it across a rename.
Filler sentence 5 keeps this page long enough for git to pair it across a rename.
Filler sentence 6 keeps this page long enough for git to pair it across a rename.
Filler sentence 7 keeps this page long enough for git to pair it across a rename.
Filler sentence 8 keeps this page long enough for git to pair it across a rename.
Filler sentence 9 keeps this page long enough for git to pair it across a rename.
Filler sentence 10 keeps this page long enough for git to pair it across a rename.
Filler sentence 11 keeps this page long enough for git to pair it across a rename.
Filler sentence 12 keeps this page long enough for git to pair it across a rename.
"""

#: The Contents block gen_toc writes for _NO_TOC once the rule is in force.
_NEW_BLOCK = f"""## Contents

- **[Old {EM_DASH} heading](#old--heading)** -- What the old section holds.
- **[Plain](#plain)** -- What the plain section holds.
- **[Table](#table)** -- Body only.

"""


def _fixture_git(repo: Path, *args: str) -> str:
    """git in the fixture repository, isolated from every config of the
    host: no global or system file, a fixed identity, no signing."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("GIT_", "XDG_CONFIG_HOME"))}
    env.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "arm", "GIT_AUTHOR_EMAIL": "arm@localhost",
                "GIT_COMMITTER_NAME": "arm",
                "GIT_COMMITTER_EMAIL": "arm@localhost"})
    return git(repo, "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/",
               *args, env=env)


def _commit(repo: Path, message: str) -> str:
    """Stage everything and commit it; the new HEAD's SHA."""
    _fixture_git(repo, "add", "-A")
    _fixture_git(repo, "commit", "-q", "-m", message)
    return _fixture_git(repo, "rev-parse", "HEAD").strip()


#: A base page whose em-dash heading exists ONLY inside a comment: it
#: renders no heading, so it has no anchor to preserve and authorises no
#: label ([R0] round 5 F2 on PR #384).
_COMMENTED = f"""# Commented heading page

<!--
## Old {EM_DASH} heading
-->

## Alpha

Body.

## Beta

Body.

## Gamma

Body.
"""

#: A base page whose em-dash heading sits in a TIGHT type-6 HTML block: no
#: blank line ends the block, so the heading renders as text and has no
#: anchor to preserve ([R0] and [R10] round 7 on PR #384).
_DIV_BASE = f"""# Div-wrapped heading page

<div>
## Old {EM_DASH} heading
</div>

## Alpha

Body.

## Beta

Body.

## Gamma

Body.
"""

#: A base page whose em-dash heading sits in a TIGHT type-7 HTML block
#: tucked directly under a heading: no blank line ends the block and none
#: precedes it, so the heading renders as text and has no anchor to
#: preserve ([R85] F1 and [R86] F1, round 1 on PR #428).
_SPAN_BASE = f"""# Span-wrapped heading page

## Wrapper
<span>
## Old {EM_DASH} heading
</span>

## Alpha

Body.

## Beta

Body.

## Gamma

Body.
"""

#: A base page that opens with a comment carrying a fence marker. Its
#: Contents block is legitimate and must stay exempt: a walk that let the
#: marker open a fence refused this page ([R0] round 5 F3 on PR #384).
_FENCE_IN_COMMENT = """<!--
```
-->

# Fence marker in an old comment

## Old {EM_DASH} heading

Body.

## Plain

Body.

## Table

Body.
""".replace("{EM_DASH}", EM_DASH)


def _fixture_repo(repo: Path) -> str:
    """The base commit: every page as it stood before the branch."""
    _fixture_git(repo, "init", "-q", "--initial-branch=main")
    (repo / "WITH_TOC.md").write_text(_WITH_TOC, encoding="utf-8")
    (repo / "NO_TOC.md").write_text(_NO_TOC, encoding="utf-8")
    (repo / "COMMENTED.md").write_text(_COMMENTED, encoding="utf-8")
    (repo / "FENCE_COMMENT.md").write_text(_FENCE_IN_COMMENT, encoding="utf-8")
    (repo / "DIV.md").write_text(_DIV_BASE, encoding="utf-8")
    (repo / "SPAN.md").write_text(_SPAN_BASE, encoding="utf-8")
    # One page at a path `gen_toc.py` deliberately skips: it IS a table of
    # contents, so this script writes no block for it and no line of it can
    # be generated navigation.
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "README.md").write_text(_NO_TOC, encoding="utf-8")
    return _commit(repo, "base")


def _edit(repo: Path, name: str, old: str, new: str) -> None:
    """Replace ``old`` with ``new`` in one fixture page, refusing to edit
    nothing."""
    page = repo / name
    text = page.read_text(encoding="utf-8")
    assert old in text, f"fixture drift: {old!r} not in {name}"
    page.write_text(text.replace(old, new, 1), encoding="utf-8")


def _write(repo: Path, name: str, text: str) -> None:
    """Write one fixture file whole."""
    (repo / name).write_text(text, encoding="utf-8")


def _fenced_example(repo: Path, opener: str, closer: str,
                    indent: str = "") -> None:
    """Quote the generated Contents block of `_NO_TOC` inside a fence, a
    comment or an indented code block: the block copies a heading the base
    page already had, and none of it renders as a navigation label, so
    every line of it is judged. `opener` may carry more than one line, so a
    control can put content between the delimiter and the block; `indent`
    is what makes the block code rather than a list."""
    block = "".join(indent + l if l.strip() else l
                    for l in _NEW_BLOCK.splitlines(keepends=True))
    quoted = "\n".join(x for x in (opener, block + closer) if x)
    _edit(repo, "NO_TOC.md", "Body.\n\n## Table", f"{quoted}\n\n## Table")


def _unwrap(repo: Path, name: str, opener: str, closer: str) -> None:
    """Take the em-dash heading of one fixture page out of the `opener` ..
    `closer` lines it sits between and write, above `## Alpha`, a Contents
    block that copies it, then the heading itself as a real one. The head
    page is a valid generated block, so provenance holds and the exemption
    is really asked: the answer is no, because the base rendered no such
    heading. The heading line itself is not an added line: the base
    carried the same text inside the wrapper, so git pairs it."""
    _edit(repo, name, f"{opener}\n{_OLD_HEADING}\n{closer}\n\n", "")
    _edit(repo, name, "## Alpha",
          "## Contents\n\n"
          f"- **[Old {EM_DASH} heading](#old--heading)** -- Copied.\n"
          "- **[Alpha](#alpha)** -- What alpha holds.\n"
          "- **[Beta](#beta)** -- What beta holds.\n"
          "- **[Gamma](#gamma)** -- What gamma holds.\n"
          f"\n{_OLD_HEADING}\n\nBody.\n\n## Alpha")


@dataclass(frozen=True)
class Control:
    """One planted change and the verdict the rule promises for it: the
    finding count, the fragments the findings must name, and how many
    mirrored labels the exemption must have passed (None = not checked)."""

    name: str
    edit: object
    findings: int
    needles: tuple[str, ...] = ()
    exempt: int | None = None


#: The em-dash heading the fixture pages carry, and its Contents entry as
#: _WITH_TOC writes it, with the em-dash separator.
_OLD_HEADING = f"## Old {EM_DASH} heading"
_OLD_ENTRY = f"- **[Old {EM_DASH} heading](#old--heading)** {EM_DASH} "
#: An ordinary prose edit of _NO_TOC introducing the character at line 5.
_PROSE_DASH = ("NO_TOC.md", "Body.\n\n## Plain",
               f"Body {EM_DASH} more body.\n\n## Plain")


def _controls() -> tuple[Control, ...]:
    """The four controls #378 names, then the boundaries of the rule."""
    return (_issue_controls() + _label_controls() + _context_controls()
            + _provenance_controls() + _scope_controls())


def _issue_controls() -> tuple[Control, ...]:
    """The four controls #378 names."""
    block = _WITH_TOC[_WITH_TOC.index("## Contents"):
                      _WITH_TOC.index(_OLD_HEADING)]
    return (
        Control("added prose em dash is refused",
                lambda r: _edit(r, *_PROSE_DASH),
                1, ("NO_TOC.md:5:", "added prose line")),
        Control("mirrored label of a pre-existing heading passes",
                lambda r: _edit(r, "NO_TOC.md", _OLD_HEADING,
                                _NEW_BLOCK + _OLD_HEADING),
                0, exempt=1),
        Control("new heading with an em dash is refused, label included",
                # The entry sits where the generator puts it, so the line
                # has provenance and the exemption is really asked: the
                # answer is no, because the base page had no such heading.
                # The page's separator is the em dash, so the added entry
                # line is refused for that too.
                lambda r: (_edit(r, "WITH_TOC.md", "- **[Plain](#plain)**",
                                 f"- **[New {EM_DASH} section](#new--section)**"
                                 f" {EM_DASH} Body.\n- **[Plain](#plain)**"),
                           _edit(r, "WITH_TOC.md", "## Plain",
                                 f"## New {EM_DASH} section\n\nBody.\n\n"
                                 "## Plain")),
                3, ("added heading", "mirrors no heading",
                    "Contents separator"), exempt=0),
        Control("separator change to -- passes",
                lambda r: _edit(r, "WITH_TOC.md", block,
                                block.replace(f"** {EM_DASH} ", "** -- ")),
                0, exempt=1),
    )


def _label_controls() -> tuple[Control, ...]:
    """Only the label span of a generated entry is exempt; the separator,
    the description and an entry the generator would not write are all
    judged."""
    return (
        Control("em dash in the description of an exempt entry is refused",
                lambda r: _edit(
                    r, "NO_TOC.md", _OLD_HEADING,
                    _NEW_BLOCK.replace("What the old section holds.",
                                       f"What the old {EM_DASH} section holds.")
                    + _OLD_HEADING),
                1, ("Contents description",), exempt=1),
        Control("an added entry keeping the em-dash separator is refused",
                lambda r: (_edit(r, "WITH_TOC.md", f"](#table)** {EM_DASH} A table.",
                                 f"](#table)** {EM_DASH} A table.\n"
                                 f"- **[Extra](#extra)** {EM_DASH} More."),
                           _edit(r, "WITH_TOC.md", "| a | b |\n",
                                 "| a | b |\n\n## Extra\n\nBody.\n")),
                1, ("Contents separator",), exempt=0),
        Control("an entry whose anchor is not the generator's is refused",
                lambda r: _edit(r, "NO_TOC.md", _OLD_HEADING,
                                _NEW_BLOCK.replace("(#old--heading)",
                                                   f"(#old-{EM_DASH}-heading)")
                                + _OLD_HEADING),
                1, ("added prose line",), exempt=0),
        Control("an entry indented four spaces is refused",
                lambda r: _edit(r, "NO_TOC.md", _OLD_HEADING,
                                _NEW_BLOCK.replace("- **[Old",
                                                   "    - **[Old")
                                + _OLD_HEADING),
                1, ("NO_TOC.md",), exempt=0),
    )


def _context_controls() -> tuple[Control, ...]:
    """A copy of a generated block written where nothing renders it: every
    construct both review rounds built, kept as one regression each."""
    return (
        Control("fenced copy of a mirrored label is refused",
                lambda r: _fenced_example(r, "```", "```"),
                1, ("added fenced line",), exempt=0),
        Control("four-backtick fence around a mirrored label is refused",
                # The three-backtick line is CONTENT of the longer fence,
                # not its closer, so the block below is still quoted.
                lambda r: _fenced_example(r, "````markdown\n```", "````"),
                1, ("added fenced line",), exempt=0),
        Control("tilde fence around a mirrored label is refused",
                lambda r: _fenced_example(r, "~~~", "~~~"),
                1, ("added fenced line",), exempt=0),
        Control("indented fence around a mirrored label is refused",
                lambda r: _fenced_example(r, "   ```", "   ```"),
                1, ("added fenced line",), exempt=0),
        Control("indented-code copy of a mirrored label is refused",
                lambda r: _fenced_example(r, "", "", indent="    "),
                1, ("added indented code line",), exempt=0),
        Control("commented-out copy of a mirrored label is refused",
                lambda r: _fenced_example(r, "<!--", "-->"),
                1, ("added commented line",), exempt=0),
        Control("raw HTML copy of a mirrored label is refused",
                lambda r: _fenced_example(r, "<pre>", "</pre>"),
                1, ("added raw HTML line",), exempt=0),
    )


def _provenance_controls() -> tuple[Control, ...]:
    """Where the exemption comes from: a heading the base page really
    rendered, and a page whose own commented text must not disturb it."""
    return (
        Control("a heading that exists only in a comment authorises nothing",
                lambda r: _edit(r, "COMMENTED.md", "## Alpha",
                                "## Contents\n\n"
                                f"- **[Old {EM_DASH} heading]"
                                "(#old--heading)** -- Copied.\n"
                                "- **[Alpha](#alpha)** -- What alpha holds.\n"
                                "- **[Beta](#beta)** -- What beta holds.\n"
                                "- **[Gamma](#gamma)** -- What gamma holds.\n"
                                "\n## Alpha"),
                1, ("COMMENTED.md", "added prose line"), exempt=0),
        Control("a page the walk refuses to read exempts nothing",
                # The same edit as "mirrored label of a pre-existing
                # heading passes", with one no-break space planted in the
                # prose: the walk refuses the page, so the label that was
                # exempt there is judged here and the refusal is named.
                lambda r: (_edit(r, "NO_TOC.md", _OLD_HEADING,
                                 _NEW_BLOCK + _OLD_HEADING),
                           _edit(r, "NO_TOC.md", "Filler sentence 1 ",
                                 "Filler\u00a0sentence 1 ")),
                2, ("U+00A0 at column", "no Contents label on it is exempt",
                    "in an added prose line"), exempt=0),
        Control("a second comment on a closing line still hides the block",
                lambda r: _fenced_example(r, "<!-- first --> <!-- second",
                                          "-->"),
                1, ("added commented line",), exempt=0),
        Control("an index page this generator skips is never exempt",
                lambda r: _edit(r, "docs/README.md", _OLD_HEADING,
                                _NEW_BLOCK + _OLD_HEADING),
                1, ("docs/README.md", "added prose line"), exempt=0),
        Control("a heading wrapped in a tight HTML block authorises nothing",
                lambda r: _unwrap(r, "DIV.md", "<div>", "</div>"),
                1, ("mirrors no heading",), exempt=0),
        Control("a heading wrapped in a tight type-7 block under a heading "
                "authorises nothing",
                # The twin of the type-6 control, with the wrapper a lone
                # inline tag that no blank line precedes: the base rendered
                # no such heading there either. Decided by `headings()`,
                # so a walk that reads the tag as paragraph text exempts
                # the label and this arm does not hold.
                lambda r: _unwrap(r, "SPAN.md", "## Wrapper\n<span>",
                                  "</span>"),
                1, ("mirrors no heading",), exempt=0),
        Control("an entry-shaped line outside the block is not exempt",
                # The page carries a VALID generated block, so only the
                # position and byte equality of a line decide provenance:
                # the stray copy below sits outside the block and is
                # judged, while the block's own label stays exempt.
                lambda r: _edit(r, "NO_TOC.md", _OLD_HEADING,
                                _NEW_BLOCK + _OLD_HEADING + "\n\n"
                                f"- **[Old {EM_DASH} heading]"
                                "(#old--heading)** -- Stray copy."),
                1, ("added prose line",), exempt=1),
        Control("a fence marker in an old comment refuses nothing",
                lambda r: _edit(r, "FENCE_COMMENT.md", _OLD_HEADING,
                                _NEW_BLOCK + _OLD_HEADING),
                0, exempt=1),
    )


def _scope_controls() -> tuple[Control, ...]:
    """What is judged beyond the Contents block, what a rename keeps, and
    what git's own attributes may not take out of the judgement."""
    block = _WITH_TOC[_WITH_TOC.index("## Contents"):
                      _WITH_TOC.index(_OLD_HEADING)]
    return (
        Control("added table row is refused",
                lambda r: _edit(r, "WITH_TOC.md", "| a | b |\n",
                                f"| a | b |\n| c | d {EM_DASH} e |\n"),
                1, ("added table row",)),
        Control("added fenced line is refused",
                lambda r: _edit(r, "NO_TOC.md", "Body.\n\n## Table",
                                f"```\nout {EM_DASH} in\n```\n\n## Table"),
                1, ("added fenced line",)),
        Control("a moved page keeps its exemption",
                lambda r: (_fixture_git(r, "mv", "WITH_TOC.md", "MOVED.md"),
                           _edit(r, "MOVED.md", block,
                                 block.replace(f"** {EM_DASH} ", "** -- "))),
                0, exempt=1),
        Control("a page marked -diff is still compared as text",
                lambda r: (_write(r, ".gitattributes", "NO_TOC.md -diff\n"),
                           _edit(r, *_PROSE_DASH)),
                1, ("NO_TOC.md:5:", "added prose line")),
        Control("a deleted page adds no line",
                lambda r: (r / "WITH_TOC.md").unlink(), 0),
        Control("text outside Markdown is not read",
                lambda r: _write(r, "notes.txt", f"a {EM_DASH} b\n"), 0),
    )


def _run_control(repo: Path, base: str, control: Control) -> list[str]:
    """Plant one control on top of the base and compare its verdict with
    the promised one; the problems, if any."""
    _fixture_git(repo, "reset", "-q", "--hard", base)
    control.edit(repo)
    _commit(repo, control.name)
    verdict = judge(repo, base)
    text = "\n".join(verdict.findings)
    problems = []
    if len(verdict.findings) != control.findings:
        problems.append(f"[{control.name}] expected {control.findings} "
                        f"finding(s), got {len(verdict.findings)}:\n{text}")
    for needle in control.needles:
        if needle not in text:
            problems.append(f"[{control.name}] no finding names "
                            f"{needle!r}:\n{text}")
    if control.exempt is not None and verdict.exempt != control.exempt:
        problems.append(f"[{control.name}] expected {control.exempt} "
                        f"exempt label(s), got {verdict.exempt}:\n{text}")
    if control.exempt and verdict.judged == 0:
        problems.append(f"[{control.name}] read no added line, so the "
                        "exemption was never exercised")
    return problems


def _base_derivation_arms() -> tuple[list[str], int]:
    """The base a run judges from is DERIVED, never the one recorded when a
    pull request opened.

    (problems, arms). GitHub freezes `pull_request.base.sha` at open while
    the checkout builds the merge of the head into the CURRENT base tip, so
    the recorded oid attributes to this branch every line merged into the
    base since -- measured on PR #384 itself, where two other pull
    requests' lines were reported as this branch's. The workflow step
    therefore takes the merge base against the base BRANCH, and this arm
    plants exactly that situation: an unrelated commit lands on the base
    branch after the branch opens, the base is merged in as the merge ref
    does, and the derived base must attribute nothing of it while the
    frozen one still does.
    """
    problems, arms = [], 0
    with tempfile.TemporaryDirectory(prefix="emdash.base.") as tmp:
        repo = Path(tmp)
        frozen = _fixture_repo(repo)
        _fixture_git(repo, "checkout", "-q", "-b", "topic")
        _edit(repo, "NO_TOC.md", "Body.\n\n## Plain",
              "Body, and more body.\n\n## Plain")
        _commit(repo, "this branch's own clean change")
        _fixture_git(repo, "checkout", "-q", "main")
        _edit(repo, "WITH_TOC.md", "Prose with no dash.",
              f"Prose {EM_DASH} with a dash.")
        other = _commit(repo, "another branch's change, merged into the base")
        _fixture_git(repo, "checkout", "-q", "topic")
        _fixture_git(repo, "merge", "-q", "--no-edit", "main")
        derived = _fixture_git(repo, "merge-base", "HEAD", "main").strip()
        arms += 1
        if derived != other:
            problems.append("[base derivation] the merge base of the merge "
                            "ref with the base branch is not the base tip")
        arms += 1
        mine = judge(repo, derived)
        if mine.findings:
            problems.append("[base derivation] the derived base attributes "
                            "another branch's lines:\n"
                            + "\n".join(mine.findings))
        arms += 1
        recorded = judge(repo, frozen)
        if not any("WITH_TOC.md" in f for f in recorded.findings):
            problems.append("[base derivation] the frozen base no longer "
                            "reproduces the defect this arm guards, so it "
                            "proves nothing")
    return problems, arms


def selftest() -> tuple[list[str], int]:
    """Plant each control in a repository built here and require the
    verdict the rule promises. (problems, arms)."""
    problems, arms = [], 0
    with tempfile.TemporaryDirectory(prefix="emdash.") as tmp:
        repo = Path(tmp)
        try:
            base = _fixture_repo(repo)
        except Refusal as exc:
            return [f"[fixture] cannot build the repository: {exc}"], 1
        for control in _controls():
            arms += 1
            # A Refusal from inside an arm is an arm that did not hold, and
            # this file promises rc 2 for that ([R10] round 4 on PR #384);
            # letting it escape printed a traceback and exited 1, the code
            # that means "findings".
            try:
                problems += _run_control(repo, base, control)
            except Refusal as exc:
                problems.append(f"[{control.name}] cannot judge: {exc}")
        # A base that is not a commit is refused, never judged as empty.
        arms += 1
        try:
            judge(repo, "no-such-revision")
            problems.append("[bad base] judged against a revision that is "
                            "not a commit")
        except Refusal:
            pass
    found, more = _base_derivation_arms()
    return problems + found, arms + more


def main(argv: list[str] | None = None) -> int:
    """0 clean, 1 findings, 2 cannot judge or an arm did not bite."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--base", metavar="REV",
                      help="judge the Markdown lines HEAD adds since REV "
                           "(pass the merge base)")
    mode.add_argument("--selftest", action="store_true",
                      help="run the planted controls and stop")
    args = ap.parse_args(argv)

    # Before any verdict: the controls must still bite. An unproven rule is
    # rc 2, never rc 0 - those are different answers.
    problems, arms = selftest()
    for problem in problems:
        print("  -", problem, file=sys.stderr)
    if problems:
        print(f"check_em_dash: FATAL: {len(problems)} of {arms} arm(s) did "
              "not hold", file=sys.stderr)
        return 2
    if args.selftest:
        print(f"check_em_dash selftest: PASS ({arms} arm(s))")
        return 0

    try:
        base = require_commit(REPO, args.base)
        verdict = judge(REPO, base)
    except Refusal as exc:
        print(f"check_em_dash: cannot judge: {exc}", file=sys.stderr)
        return 2
    for finding in verdict.findings:
        print(finding)
    print(f"check_em_dash: {len(verdict.findings)} finding(s) over "
          f"{verdict.judged} added line(s) in {verdict.pages} changed "
          f"Markdown page(s), {verdict.exempt} mirrored label(s) exempt, "
          f"arms {arms}/{arms} [{base[:8]}..HEAD]")
    return 1 if verdict.findings else 0


if __name__ == "__main__":
    sys.exit(main())
