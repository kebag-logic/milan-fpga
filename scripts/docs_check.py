#!/usr/bin/env python3
"""Docs gate: link integrity + wording deny-list + bare/dead references + local info.

Run from anywhere (the script locates its own repo root):

    python3 scripts/docs_check.py

**No git required.** The file inventory comes from ``git ls-files`` when the tree
is a git working tree, and from a ``.gitignore``-aware filesystem walk otherwise —
so an extracted tarball or a downloaded zip can run the same gate CI runs.

Checks, over every ``*.md`` file in the tree:

1. **Link integrity** — every relative markdown link/image target resolves to
   a file or directory in the tree (http/mailto/anchor-only links skipped), and
   a ``#L123`` / ``#L123-L456`` line anchor names a line the target file still
   has. Documentation cites RTL by line, RTL files grow by hundreds of lines
   between rounds, and an anchor past EOF drops the reader at the bottom of a
   file with no hint that the citation is stale.
2. **Wording deny-list** — terms that must not appear in committed docs.
   Legitimate identifiers containing a denied stem are masked (``ALLOW``).
3. **Bare doc references** — a mention of an existing ``.md`` file that is not
   an actual markdown link (living tree only; generated files, code fences,
   HTML comments and ``historical_now_obsolete/`` are exempt).
4. **Dead references** — a bare mention of a ``.md`` path that points *inside
   this repo* but does not exist (5a), or of a document retired from the tree
   (``RETIRED``, 5b). Rule 3 only sees references to files that still exist, so
   without this a reference left behind by a deletion is invisible to the gate
   and an outside reader follows it into nothing. A document whose job is to
   record retired files (the doc-audit ledger) opts out with an HTML comment
   line holding the token ``docs-check: allow-dead-refs``.
5. **Local information** — bench/host-identifying patterns (hostnames, home
   paths, bench subnet, MAC-derived interface names, USB-serial paths) must
   not appear; also swept over ``docs/**`` diagram sources (``.gen.py``,
   ``.drawio``, ``.svg``).

Exit 0 = clean; exit 1 = findings, one per line as ``path:line: message``.
"""

import fnmatch
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Exact substrings that are legitimate despite containing a denied stem:
# spec field names, schema/repo identifiers, third-party project names.
ALLOW = (
    "certification_version",        # Milan GET_MILAN_INFO wire field (Table 5.20)
    "milan-endstation-config",      # the builder's config-schema repo name
    "OpenAvnu",                     # third-party open-source project
    "openavnu",
)

DENY_CI = re.compile(r"avnu|aets|certif", re.IGNORECASE)

#! Case-SENSITIVE: these are short acronyms whose lowercase forms are ordinary
#! words or live inside longer identifiers. A review found one of them sitting
#! in a tracked document for weeks — the case-insensitive list above could
#! never have matched it, and no stem for a certification LAB name existed.
#! Committed text says "compliance", never a lab.
#!
#! THE TOKENS ARE ASSEMBLED, NOT WRITTEN OUT. This file is tracked on a public
#! repo, and a denylist that spells the names it forbids publishes them just as
#! surely as the document it is meant to catch — the first cut of this gate did
#! exactly that, trading one leaked name for three. `docs_check` scans only
#! *.md, so it cannot catch itself; the assembly is what keeps the rule honest.
_LAB_TOKENS = tuple("".join(chr(c) for c in cs) for cs in (
    (67, 69, 82, 84), (65, 84, 76), (85, 78, 72), (73, 79, 76),
))
DENY_CS = re.compile("|".join(r"\b%s\b" % t for t in _LAB_TOKENS))

# Documents removed from the tree that must never be referenced again.
# The 2026-07-20 privacy scrub untracked these three; the live state they used
# to carry now lives in docs/findings/BENCH_TOPOLOGY.md (bench/board state) and
# docs/findings/PERFORMANCE_GOAL.md (the measured campaign record).
RETIRED = {
    "SESSION_HANDOFF.md",
    "HANDOVER.md",
    "HANDOVER_SMALL.md",
}

# Bench/host-identifying patterns (generic shapes only — never the literals).
LOCAL_RE = re.compile(
    r"amx-|/home/alex|enx[0-9a-f]{8,}|serial/by-id/usb-[A-Za-z0-9]|192\.168\.127"
)

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_SPAN_RE = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
CAND_RE = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)*[\w][\w.-]*\.md)\b")
GENERATED_MARK = re.compile(r"GENERATED", re.IGNORECASE)
# Opt-out for the archive ledger: an HTML-comment line (not a fenced example,
# which starts with a backtick) carrying the token.
ALLOW_DEAD_MARK = re.compile(
    r"^<!--[^\n]*docs-check:\s*allow-dead-refs\b", re.MULTILINE)

# Never walked: VCS metadata, vendored submodules, obvious build scratch.
# ``obj_*`` covers every Verilator scratch dir (obj_dir/obj_win/obj_live/…),
# several of which are only named in per-suite .gitignore files this crude
# reader does not descend into.
ALWAYS_PRUNE = {".git", "__pycache__", "node_modules", ".venv"}
ALWAYS_PRUNE_GLOBS = ("obj_*",)


# --------------------------------------------------------------------------
# file inventory — git when available, .gitignore-aware walk otherwise
# --------------------------------------------------------------------------

def _git_files():
    """Repo-relative paths from git, or None when this is not a working tree."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=REPO,
                             capture_output=True, text=True)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return [p for p in out.stdout.splitlines() if p]


def _ignore_matchers():
    """Crude .gitignore reader: (rooted globs, basename globs).

    Only the shapes this repo uses are honoured — directory entries, rooted
    path globs and bare basenames; nested per-directory ``.gitignore`` files are
    not read (``ALWAYS_PRUNE_GLOBS`` covers what they hide). This reproduces
    ``git ls-files`` exactly today apart from submodule gitlinks, which git
    reports as files and a filesystem walk cannot. To re-check that after
    editing::

        python3 -c "import sys; sys.path.insert(0,'scripts'); import docs_check as d; \
                    g=set(d._git_files()); w=set(d._walk_files()); \
                    print(sorted(g^w))"
    """
    rooted, basenames = [], []
    gi = REPO / ".gitignore"
    if gi.is_file():
        for raw in gi.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith(("#", "!")):
                continue
            line = line.rstrip("/")
            if not line:
                continue
            (rooted if "/" in line.strip("/") else basenames).append(
                line.lstrip("/"))
    return rooted, basenames


def _submodule_paths():
    out = set()
    gm = REPO / ".gitmodules"
    if gm.is_file():
        for line in gm.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip().startswith("path"):
                out.add(line.split("=", 1)[1].strip())
    return out


def _walk_files():
    """Repo-relative paths from the filesystem, minus ignored/vendored trees."""
    rooted, basenames = _ignore_matchers()
    pruned = _submodule_paths()

    def ignored(rel, name):
        if name in ALWAYS_PRUNE or rel in pruned:
            return True
        if any(fnmatch.fnmatch(name, pat) for pat in ALWAYS_PRUNE_GLOBS):
            return True
        if any(fnmatch.fnmatch(name, pat) for pat in basenames):
            return True
        return any(fnmatch.fnmatch(rel, pat) for pat in rooted)

    found = []
    for dirpath, dirnames, filenames in os.walk(REPO):
        base = Path(dirpath).relative_to(REPO)
        dirnames[:] = [
            d for d in dirnames
            if not ignored(str(base / d) if str(base) != "." else d, d)
        ]
        for f in filenames:
            rel = str(base / f) if str(base) != "." else f
            if not ignored(rel, f):
                found.append(rel)
    return sorted(found)


_INVENTORY = None
_INVENTORY_SOURCE = "?"


def inventory():
    global _INVENTORY, _INVENTORY_SOURCE
    if _INVENTORY is None:
        files = _git_files()
        if files is None:
            files, _INVENTORY_SOURCE = _walk_files(), "filesystem walk (no git)"
        else:
            _INVENTORY_SOURCE = "git ls-files"
        _INVENTORY = files
    return _INVENTORY


def tracked(pattern):
    """Files matching a git-pathspec-style glob (``*`` also matches ``/``)."""
    return [p for p in inventory() if fnmatch.fnmatch(p, pattern)]


# --------------------------------------------------------------------------
# reference resolution
# --------------------------------------------------------------------------

def norm_join(base, ref):
    parts = []
    for seg in (str(base) + "/" + ref).replace("\\", "/").split("/"):
        if seg == "..":
            if parts:
                parts.pop()
            else:
                return None
        elif seg not in (".", ""):
            parts.append(seg)
    return "/".join(parts)


def make_resolver(tracked_md):
    tracked_set = set(tracked_md)
    by_base = Counter(Path(p).name for p in tracked_md)

    def resolve(ref, filedir):
        for base in (filedir, Path("."), Path("docs")):
            n = norm_join(base, ref)
            if n and n in tracked_set:
                return n
        if "/" not in ref and by_base.get(ref, 0) == 1:
            for p in tracked_md:
                if Path(p).name == ref:
                    return p
        return None

    return resolve


def dead_inside_repo(ref, filedir, tracked_set):
    """Repo-internal path that does not exist, or None.

    A reference counts as repo-internal only when its *parent directory* is a
    real directory of this repo — so ``fpga/docs/X.md`` (a sibling repo) and
    ``patches/README.md`` (upstream LiteX) are correctly left alone, while
    ``../findings/GONE.md`` and ``docs/findings/GONE.md`` are caught.
    """
    if "/" not in ref:
        return None
    for base in (filedir, Path(".")):
        n = norm_join(base, ref)
        if not n or n in tracked_set:
            continue
        parent = str(Path(n).parent)
        if parent not in ("", ".") and (REPO / parent).is_dir():
            return n
    return None


LINE_ANCHOR_RE = re.compile(r"^L(\d+)(?:-L(\d+))?$")


def anchor_overruns(resolved, frag):
    """Why a ``#L123`` anchor cannot land, or None when it can.

    A citation like ``KL_acmp_lstn_ctx.sv:463`` is only useful as a link if the
    file still HAS a line 463 - and RTL files in this tree grow by hundreds of
    lines between documentation rounds. This catches the mechanical half of
    that rot; the half where the line exists but no longer holds what the row
    claims is not machine-checkable, which is why the traceability pages carry
    a snapshot date and say the anchors drift.
    """
    m = LINE_ANCHOR_RE.match(frag)
    if not m or not resolved.is_file():
        return None
    try:
        n = len(resolved.read_bytes().split(b"\n"))
    except OSError:
        return None
    top = int(m.group(2) or m.group(1))
    return f"file has {n} lines" if top > n else None


def check_md(path, relpath, resolve, tracked_set):
    findings = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{relpath}:0: not valid UTF-8"]
    lines = text.splitlines()
    generated = bool(GENERATED_MARK.search(text[:400]))
    historical = relpath.startswith("historical_now_obsolete/")
    allow_dead = bool(ALLOW_DEAD_MARK.search(text))
    filedir = Path(relpath).parent

    in_fence = in_comment = False
    for lineno, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence

        # --- wording deny-list + local info (everywhere, fences included) ---
        masked = line
        for allow in ALLOW:
            masked = masked.replace(allow, "#" * len(allow))
        m = DENY_CI.search(masked) or DENY_CS.search(masked)
        if m:
            findings.append(f"{relpath}:{lineno}: denied wording '{m.group(0)}'")
        lm = LOCAL_RE.search(line)
        if lm:
            findings.append(f"{relpath}:{lineno}: local info '{lm.group(0)}'")

        if in_fence:
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue

        # --- link integrity (target, then line anchor) ---
        for lk in LINK_RE.finditer(line):
            target = lk.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target, _, frag = target.partition("#")
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                findings.append(f"{relpath}:{lineno}: broken link -> {target}")
                continue
            over = anchor_overruns(resolved, frag)
            if over:
                findings.append(f"{relpath}:{lineno}: line anchor past end of "
                                f"file -> {target}#{frag} ({over})")

        # --- bare + dead doc references (living, non-generated files only) ---
        if generated or historical:
            continue
        stripped = LINK_SPAN_RE.sub(" ", line)
        for cm in CAND_RE.finditer(stripped):
            ref = cm.group(1)
            if ref == Path(relpath).name and "/" not in ref:
                continue
            target = resolve(ref, filedir)
            if target and target != relpath:
                findings.append(
                    f"{relpath}:{lineno}: bare reference to {target} — make it a link"
                )
                continue
            if target or allow_dead:
                continue
            if Path(ref).name in RETIRED:
                findings.append(
                    f"{relpath}:{lineno}: dead reference to retired doc {ref} — "
                    f"repoint at the living doc or drop it"
                )
                continue
            gone = dead_inside_repo(ref, filedir, tracked_set)
            if gone:
                findings.append(
                    f"{relpath}:{lineno}: dead reference to {gone} — no such file "
                    f"in the tree"
                )
    return findings


def main():
    findings = []
    md = tracked("*.md")
    resolve = make_resolver(md)
    tracked_set = set(md)
    for rel in md:
        findings.extend(check_md(REPO / rel, rel, resolve, tracked_set))
    # local-info sweep over diagram sources (text formats only)
    for pattern in ("docs/*.gen.py", "docs/*/*.gen.py", "docs/*.drawio",
                    "docs/*/*.drawio", "docs/*.svg", "docs/*/*.svg"):
        for rel in tracked(pattern):
            for lineno, line in enumerate(
                    (REPO / rel).read_text(encoding="utf-8",
                                           errors="replace").splitlines(), 1):
                lm = LOCAL_RE.search(line)
                if lm:
                    findings.append(f"{rel}:{lineno}: local info '{lm.group(0)}'")
    findings = sorted(set(findings))
    for f in findings:
        print(f)
    print(f"docs_check: {len(findings)} finding(s) across {len(md)} md files "
          f"[{_INVENTORY_SOURCE}]")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
