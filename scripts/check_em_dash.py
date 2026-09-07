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
refused, never counted clean. Every added line carrying the character is a
finding unless it is an entry of the page's real, unfenced Contents block
whose label equals, after gen_toc's own label transform, a heading of the
BASE version of the same page - and then only the label span is exempt: the
link target, the separator, the description and any other character of the
line are judged. The exemption is decided from the base page's headings,
never from the label text alone, so a label that mirrors a heading the same
change introduces is refused with its heading, and a Contents block quoted
inside a fence is fenced text like any other.

The base is explicit. Locally pass the merge base; the docs workflow passes
the pull request's base SHA or a push's ``before`` SHA and refuses an event
carrying neither rather than guessing one. The planted controls run on every
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
from gen_toc import HEAD_RE, TOC_ENTRY_RE, TOC_HEAD, fenced, headings, label

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
#: Four spaces (or a tab) of indentation start an indented code block, which
#: renders as code, not as navigation ([R0] round 4 on PR #384). Such a run
#: cannot interrupt a paragraph, so it begins only after a blank line.
INDENT_CODE_RE = re.compile(r"^(?: {4}|\t)")
COMMENT_OPEN, COMMENT_CLOSE = "<!--", "-->"


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


@dataclass(frozen=True)
class Shape:
    """What a page's lines are, by index (fenced line, heading, table row
    or prose line), and the span of its real, unfenced Contents block as
    (index of the heading, index of the next section heading), or None."""

    kinds: list[str]
    contents: tuple[int, int] | None


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


def _comment_spans(lines: list[str], fences: list[bool]) -> list[bool]:
    """Per line: does it BEGIN inside an HTML comment? A commented Contents
    block renders nothing at all, so no line of one is a navigation entry
    ([R0] round 4 on PR #384). Fenced lines cannot open or close a comment:
    inside a code block the delimiters are text."""
    out, inside = [], False
    for line, in_fence in zip(lines, fences):
        out.append(inside)
        if in_fence:
            continue
        scan = line
        while scan:
            if inside:
                at = scan.find(COMMENT_CLOSE)
                if at < 0:
                    break
                scan, inside = scan[at + len(COMMENT_CLOSE):], False
            else:
                at = scan.find(COMMENT_OPEN)
                if at < 0:
                    break
                scan, inside = scan[at + len(COMMENT_OPEN):], True
    return out


def shape(text: str) -> Shape:
    """A page's line kinds and the span of its real Contents block.

    Everything here decides ONE question: which added lines may carry the
    label exemption. Only a line that renders as a navigation entry may, so
    three spans are held apart from prose, each of them an escape a review
    round measured on this gate: a fenced block (the fence walk is
    gen_toc's, with CommonMark's delimiter, length, closer and indentation
    rules), an indented code block, and an HTML comment. A Contents block
    written inside any of them renders as code, or as nothing, and its
    heading is not this page's Contents heading either -- so the block
    starts at the first `## Contents` heading that is none of those things,
    and ends at the next such `## ` heading.

    An indented list continuation elsewhere on a page is called an indented
    code line here too. That decides no exemption (it is not in a Contents
    block, and an entry is bounded at three spaces of indentation anyway);
    it changes only which word a finding uses for the line.
    """
    lines = text.split("\n")
    fences = fenced(text)
    comments = _comment_spans(lines, fences)
    kinds, start, end = [], None, None
    code, prev_blank = False, True
    for i, line in enumerate(lines):
        blank = not line.strip()
        if fences[i] or comments[i]:
            code = False
        elif INDENT_CODE_RE.match(line):
            code = code or prev_blank
        elif not blank:
            code = False
        prev_blank = blank
        if fences[i]:
            kinds.append("fenced line")
        elif comments[i]:
            kinds.append("commented line")
        elif code and not blank:
            kinds.append("indented code line")
        elif HEAD_RE.match(line):
            kinds.append("heading")
            if start is None and line.strip() == TOC_HEAD:
                start = i
            elif start is not None and end is None and line.startswith("## "):
                end = i
        elif line.lstrip().startswith("|"):
            kinds.append("table row")
        else:
            kinds.append("prose line")
    if start is None:
        return Shape(kinds, None)
    return Shape(kinds, (start, len(kinds) if end is None else end))


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
    """Every finding one page's added lines carry, appended to
    ``verdict``. The page's HEAD text is read only when an added line
    carries the character, to place it in the Contents block or name what
    it is."""
    added = added_lines(repo, base, change)
    verdict.judged += len(added)
    hits = [a for a in added if EM_DASH in a.text]
    if not hits:
        return
    page = shape(git(repo, "show", f"HEAD:{change.path}"))
    exempt_labels = None
    for hit in hits:
        where = f"{hit.path}:{hit.lineno}"
        kind = page.kinds[hit.lineno - 1]
        entry = None
        if kind == "prose line" and page.contents is not None \
                and page.contents[0] < hit.lineno - 1 < page.contents[1]:
            entry = TOC_ENTRY_RE.match(hit.text)
        if entry is None:
            verdict.findings.append(
                f"{where}: U+2014 (em dash) in an added {kind} -- {REMEDY}")
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
    verdict.findings.sort()
    return verdict


# --------------------------------------------------------------------------
# the planted controls, each in a repository built here
# --------------------------------------------------------------------------

#: A page with a Contents block that predates the rule: em-dash separators,
#: one label mirroring an em-dash heading. The anchors are gen_toc's.
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


def _fixture_repo(repo: Path) -> str:
    """The base commit: both pages as they stood before the branch."""
    _fixture_git(repo, "init", "-q", "--initial-branch=main")
    (repo / "WITH_TOC.md").write_text(_WITH_TOC, encoding="utf-8")
    (repo / "NO_TOC.md").write_text(_NO_TOC, encoding="utf-8")
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


#: The em-dash heading both fixture pages carry, and its Contents entry as
#: _WITH_TOC writes it, with the em-dash separator.
_OLD_HEADING = f"## Old {EM_DASH} heading"
_OLD_ENTRY = f"- **[Old {EM_DASH} heading](#old--heading)** {EM_DASH} "
#: An ordinary prose edit of _NO_TOC introducing the character at line 5.
_PROSE_DASH = ("NO_TOC.md", "Body.\n\n## Plain",
               f"Body {EM_DASH} more body.\n\n## Plain")


def _controls() -> tuple[Control, ...]:
    """The four controls #378 names, then the boundaries of the rule."""
    return _issue_controls() + _boundary_controls()


def _issue_controls() -> tuple[Control, ...]:
    """The four controls #378 names."""
    old_heading, block = _OLD_HEADING, _WITH_TOC[
        _WITH_TOC.index("## Contents"):_WITH_TOC.index(_OLD_HEADING)]
    return (
        Control("added prose em dash is refused",
                lambda r: _edit(r, *_PROSE_DASH),
                1, ("NO_TOC.md:5:", "added prose line")),
        Control("mirrored label of a pre-existing heading passes",
                lambda r: _edit(r, "NO_TOC.md", old_heading,
                                _NEW_BLOCK + old_heading),
                0, exempt=1),
        Control("new heading with an em dash is refused, label included",
                lambda r: (_edit(r, "WITH_TOC.md", "\n\n## Old",
                                 f"\n- **[New {EM_DASH} section]"
                                 "(#new--section)** -- Body.\n\n## Old"),
                           _edit(r, "WITH_TOC.md", "## Plain",
                                 f"## New {EM_DASH} section\n\nBody.\n\n"
                                 "## Plain")),
                2, ("added heading", "mirrors no heading")),
        Control("separator change to -- passes",
                lambda r: _edit(r, "WITH_TOC.md", block,
                                block.replace(f"** {EM_DASH} ", "** -- ")),
                0, exempt=1),
    )


def _boundary_controls() -> tuple[Control, ...]:
    """The boundaries of the rule: only the label span of a real entry is
    exempt, and what git's own attributes may not take out of the
    judgement."""
    return _label_controls() + _scope_controls()


def _label_controls() -> tuple[Control, ...]:
    """Only the label span of an entry in the page's real Contents block
    is exempt; every other character of the line is judged."""
    old_heading, old_entry = _OLD_HEADING, _OLD_ENTRY
    return (
        Control("em dash in the link target of an exempt entry is refused",
                lambda r: _edit(r, "NO_TOC.md", old_heading,
                                _NEW_BLOCK.replace("(#old--heading)",
                                                   f"(#old-{EM_DASH}-heading)")
                                + old_heading),
                1, ("link target",), exempt=1),
        Control("em dash in the description of an exempt entry is refused",
                lambda r: _edit(r, "WITH_TOC.md", old_entry + "What",
                                f"{old_entry[:-2]}-- What {EM_DASH} what"),
                1, ("Contents description",), exempt=1),
        Control("added entry keeping the em-dash separator is refused",
                lambda r: _edit(r, "WITH_TOC.md", "\n\n## Old",
                                f"\n- **[Extra](#extra)** {EM_DASH} More.\n"
                                "\n## Old"),
                1, ("Contents separator",)),
        Control("fenced example of a mirrored label is refused",
                lambda r: _fenced_example(r, "```", "```"),
                1, ("added fenced line",), exempt=0),
        # The two constructs that render no navigation at all ([R0] round
        # 4 on PR #384): four spaces of indentation make the block code,
        # and an HTML comment makes it invisible. Neither is an entry.
        Control("indented-code copy of a mirrored label is refused",
                lambda r: _fenced_example(
                    r, "", "", indent="    "),
                1, ("added indented code line",), exempt=0),
        Control("commented-out copy of a mirrored label is refused",
                lambda r: _fenced_example(r, "<!--", "-->"),
                1, ("added commented line",), exempt=0),
        # The fence shapes that a laxer walk read as prose ([R0] round 2 on
        # PR #384): the block below carries a three-backtick line of its
        # own, so only a four-backtick closer ends it.
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
    )


def _scope_controls() -> tuple[Control, ...]:
    """What is judged beyond the Contents block, what a rename keeps, and
    what git's own attributes may not take out of the judgement."""
    old_entry = _OLD_ENTRY
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
                           _edit(r, "MOVED.md", old_entry,
                                 old_entry.replace(f"** {EM_DASH} ", "** -- "))),
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
    return problems, arms


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
