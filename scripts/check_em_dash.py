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

What is judged. ``git diff -U0 -M <base> HEAD`` over every tracked ``*.md``,
renames followed so a moved page is judged on its changed lines only. Every
added line carrying the character is a finding unless it is an entry of the
page's Contents block whose label equals, after gen_toc's own label
transform, a heading of the BASE version of the same page; that entry's
separator and description are still judged. The exemption is decided from
the base page's headings, never from the label text alone, so a label that
mirrors a heading the same change introduces is refused with its heading.

The base is explicit. Locally pass the merge base; the docs workflow passes
the pull request's base SHA or a push's ``before`` SHA and refuses an event
carrying neither rather than guessing one. The planted controls run on every
invocation, before any verdict: a gate that has never failed once is not
evidence that it works.

    python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
    python3 scripts/check_em_dash.py --selftest    # the planted controls alone

Exit 0 = clean; 1 = findings, one per line as ``path:line: message``; 2 =
cannot judge (no git, a base that is not a commit) or an arm that did not
bite, which is unproven, not clean.
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
from gen_toc import FENCE_RE, HEAD_RE, TOC_ENTRY_RE, existing, headings, label

REPO = Path(__file__).resolve().parent.parent

#: Assembled from its code point, so this file never carries the character
#: it refuses and the self-test fixtures never spell it either.
EM_DASH = "\u2014"
HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
DIFF_FLAGS = ("-U0", "-M", "--no-color", "--no-ext-diff",
              "--diff-algorithm=myers", "--src-prefix=a/", "--dst-prefix=b/")
REMEDY = "write --, a colon or a plain sentence"


class Refusal(Exception):
    """The judgement cannot run: no git, or a revision that is not a commit."""


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
    added; `:(literal)` keeps a glob character in a path from expanding."""
    spec = [f":(literal){p}" for p in dict.fromkeys(
        (change.path, change.base_path)) if p]
    raw = git(repo, "diff", *DIFF_FLAGS, base, "HEAD", "--", *spec)
    out, lineno, in_hunk = [], 0, False
    for line in raw.split("\n"):
        if line.startswith("diff --git "):
            in_hunk = False
            continue
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


def kinds(text: str) -> list[str]:
    """What each line of a page is, by index: a fenced line, a heading, a
    table row or a prose line. The fence walk is gen_toc's, so a heading inside a fence
    is fenced text here exactly as it is no heading there."""
    out, fence = [], None
    for line in text.split("\n"):
        f = FENCE_RE.match(line)
        if f:
            if fence is None:
                fence = f.group(1)
            elif line.startswith(fence):
                fence = None
            out.append("fenced line")
        elif fence is not None:
            out.append("fenced line")
        elif HEAD_RE.match(line):
            out.append("heading")
        elif line.lstrip().startswith("|"):
            out.append("table row")
        else:
            out.append("prose line")
    return out


def base_labels(repo: Path, base: str, change: Change) -> set[str]:
    """The Contents labels gen_toc writes for the headings the BASE version
    of the page carries: the whole exemption, decided here and nowhere
    else."""
    if change.base_path is None:
        return set()
    text = git(repo, "show", f"{base}:{change.base_path}")
    return {label(raw) for _, raw, _ in headings(text)}


def _entry_findings(where: str, entry: re.Match[str],
                    exempt_labels: set[str], verdict: Verdict) -> None:
    """The findings one added Contents entry carries: its separator, its
    description, and its label unless the base page had that heading."""
    lab, sep, desc = entry.group(1), entry.group(3), entry.group(4)
    if sep == EM_DASH:
        verdict.findings.append(
            f"{where}: U+2014 (em dash) as the Contents separator -- "
            "switch this page's separator to --")
    if EM_DASH in desc:
        verdict.findings.append(
            f"{where}: U+2014 (em dash) in a Contents description -- {REMEDY}")
    if EM_DASH not in lab:
        return
    if lab in exempt_labels:
        verdict.exempt += 1
        return
    verdict.findings.append(
        f"{where}: U+2014 (em dash) in a Contents label that mirrors no "
        "heading the base version of this page had -- reword the new "
        "heading, then regenerate the block")


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
    text = git(repo, "show", f"HEAD:{change.path}")
    kind = kinds(text)
    _, start, end, _ = existing(text)
    exempt_labels = None
    for hit in hits:
        where = f"{hit.path}:{hit.lineno}"
        entry = None
        if start is not None and start < hit.lineno - 1 < end:
            entry = TOC_ENTRY_RE.match(hit.text)
        if entry is None:
            verdict.findings.append(
                f"{where}: U+2014 (em dash) in an added "
                f"{kind[hit.lineno - 1]} -- {REMEDY}")
            continue
        if exempt_labels is None:
            exempt_labels = base_labels(repo, base, change)
        _entry_findings(where, entry, exempt_labels, verdict)


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


def _controls() -> tuple[Control, ...]:
    """The four controls #378 names, then the boundaries of the rule."""
    old_heading = f"## Old {EM_DASH} heading"
    old_sep = f"](#old--heading)** {EM_DASH} "
    return (
        Control("added prose em dash is refused",
                lambda r: _edit(r, "NO_TOC.md", "Body.\n\n## Plain",
                                f"Body {EM_DASH} more body.\n\n## Plain"),
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
                lambda r: _edit(r, "WITH_TOC.md",
                                _WITH_TOC[_WITH_TOC.index("## Contents"):
                                          _WITH_TOC.index(old_heading)],
                                _WITH_TOC[_WITH_TOC.index("## Contents"):
                                          _WITH_TOC.index(old_heading)]
                                .replace(f"** {EM_DASH} ", "** -- ")),
                0, exempt=1),
        # The boundaries: what the rule still refuses, and what it does
        # not read at all.
        Control("added entry keeping the em-dash separator is refused",
                lambda r: _edit(r, "WITH_TOC.md", "\n\n## Old",
                                f"\n- **[Extra](#extra)** {EM_DASH} More.\n"
                                "\n## Old"),
                1, ("Contents separator",)),
        Control("em dash in an added Contents description is refused",
                lambda r: _edit(r, "WITH_TOC.md", f"{EM_DASH} A table.",
                                f"-- A table {EM_DASH} of two rows."),
                1, ("Contents description",)),
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
                           _edit(r, "MOVED.md", old_sep,
                                 old_sep.replace(EM_DASH, "--"))),
                0, exempt=1),
        Control("a deleted page adds no line",
                lambda r: (repo_unlink(r / "WITH_TOC.md")), 0),
        Control("text outside Markdown is not read",
                lambda r: (r / "notes.txt").write_text(
                    f"a {EM_DASH} b\n", encoding="utf-8"),
                0),
    )


def repo_unlink(path: Path) -> None:
    """Delete one fixture file."""
    path.unlink()


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
            problems += _run_control(repo, base, control)
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
