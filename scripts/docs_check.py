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
6. **Writing hygiene** (living pages only, fences and HTML comments exempt) —
   no process/meta narration (handover/round/session-of-authoring language),
   no decisions attributed to a person or quoted conversation, no section
   sign in prose, and no un-anchored ``X.md Section N`` pointers. The archive
   and in-place-obsolete pages (first line ``[OBSOLETE + date]``, the regex
   lifted from ``check_archive.py``) are records of their time and exempt.
7. **gPTP ownership semantics** — a present-tense claim that assigns linuxptp
   normal-operation, policy-plane, BMCA or servo ownership is rejected unless
   the surrounding text marks it as retired history (#259). The product is
   bare-metal only with exactly one fabric owner; no software-owner,
   option-off or comparison image exists any more, so that wording no longer
   qualifies a claim. Diagram sources and generated text artifacts are
   checked as well as Markdown.

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

# The in-place-obsolete predicate is OWNED by check_archive.py (its rule 4
# routes links to such pages); this gate lifts the same regex rather than
# re-deriving it, so the two gates can never disagree on what "obsolete" is.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_archive import OBSOLETE_HEADER_RE

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

# --------------------------------------------------------------------------
# Writing-hygiene rules (issue #94). Living documentation describes the
# SYSTEM; how a page was produced is not information about the system, and a
# decision is justified by a clause, a measurement or a defect - never by who
# asked for it. These rules run only on LIVING pages (not the archive, not
# in-place-obsolete pages - both are records of what was written at the time)
# and only outside code fences and HTML comments, so a page may still QUOTE
# the forbidden text when explaining a rule.

#: process/meta narration: the page talks about its own authoring process.
#: Note for AGENTS.md and anything else whose SUBJECT is the workflow: this
#: rule fires on their subject matter, not on meta-commentary about the page.
#: Say "executor" (the role AGENTS.md section 3 defines) rather than
#: "authoring session". Do NOT add the phrase to HYGIENE_ALLOW to silence it:
#: that mask is global, so it would retire this rule on every living page.
PROCESS_RE = re.compile(
    r"handover|context reset|context window|\bthis round\b|\blast round\b"
    r"|picking up|continuing from|(previous|next|authoring|last) session",
    re.IGNORECASE)

#: attribution: a decision credited to a person or a quoted conversation.
ATTRIB_RE = re.compile(
    r"USER:|USER RULE|USER STANDING|USER rule|USER['’]s"
    r"|[Uu]ser (asks|asked|wants|requested|said|directive|rule|standing)"
    r"|[Aa]s requested|per the (user|USER|directive)|forget the")

#: the section sign; prose writes the word "Section" (or "Sections").
SECTION_SIGN_RE = re.compile(r"§")

#: `X.md Section 7` (or the sign) with nothing to follow: an un-anchored
#: section pointer. An anchored link is validated by this gate and by
#: gen_toc --verify-anchors; a trailing "Section 7" is validated by nothing.
BARE_SECTION_PTR_RE = re.compile(r"\.md[`)]?,? +(Section|§) *[0-9A-Za-z]")

#: exact substrings that legitimately contain a stem the rules above match,
#: masked before matching (same mechanism as ALLOW for the deny-list).
HYGIENE_ALLOW = ()

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

# linuxptp was the software gPTP owner and is retired (#259); it may appear
# in committed text only as retired history.  Look at a three-line claim
# window so normal Markdown wrapping cannot hide an unqualified ownership
# statement.  Only retirement markers qualify: the former software-owner /
# option-off / comparison wording named an image that no longer exists, so
# it cannot excuse an ownership claim (#259 removed that allowance).
GPTP_LINUX_RE = re.compile(r"\blinuxptp\b", re.IGNORECASE)
GPTP_OWNER_CLAIM_RE = re.compile(
    r"normal operation|policy[- ]shaped|policy plane|gPTP stack|BMCA|servo",
    re.IGNORECASE,
)
GPTP_OWNER_QUALIFIER_RE = re.compile(
    r"retired|#259|historical|older|verification[- ]only",
    re.IGNORECASE,
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
    obsolete = bool(lines and OBSOLETE_HEADER_RE.fullmatch(lines[0]))
    allow_dead = bool(ALLOW_DEAD_MARK.search(text))
    filedir = Path(relpath).parent

    in_fence = in_comment = h_in_comment = False
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

        # --- writing hygiene (living pages only; see the rules above) ---
        # Runs BEFORE the whole-line comment skip below, because only the
        # comment SPAN is exempt: visible text sharing a line with a comment
        # opener or closer is still prose and still checked. The hygiene
        # rules keep their own span tracker (h_in_comment) so exempting a
        # span here cannot change what the reference rules below see.
        if not (historical or obsolete):
            hvis = line
            if h_in_comment:
                if "-->" in hvis:
                    hvis = hvis.split("-->", 1)[1]
                    h_in_comment = False
                else:
                    hvis = ""
            if not h_in_comment:
                hvis = re.sub(r"<!--.*?-->", "", hvis)
                if "<!--" in hvis:
                    hvis = hvis.split("<!--", 1)[0]
                    h_in_comment = True
            hmasked = hvis
            for allow in HYGIENE_ALLOW:
                hmasked = hmasked.replace(allow, "#" * len(allow))
            hm = PROCESS_RE.search(hmasked)
            if hm:
                findings.append(
                    f"{relpath}:{lineno}: process/meta language "
                    f"'{hm.group(0)}' — describe the system, not how the "
                    f"page was produced (if this page is ABOUT the agent "
                    f"workflow, see the note at PROCESS_RE in "
                    f"scripts/docs_check.py)")
            hm = ATTRIB_RE.search(hmasked)
            if hm:
                findings.append(
                    f"{relpath}:{lineno}: attribution '{hm.group(0)}' — "
                    f"state the clause, measurement or defect, not who asked")
            if SECTION_SIGN_RE.search(hmasked):
                findings.append(
                    f"{relpath}:{lineno}: section sign — write the word "
                    f"'Section'")
            hm = BARE_SECTION_PTR_RE.search(hmasked)
            if hm:
                findings.append(
                    f"{relpath}:{lineno}: un-anchored section pointer "
                    f"'{hm.group(0).strip()}…' — link the heading anchor "
                    f"instead")

        # --- whole-line comment skip for the REFERENCE rules below ---
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


def check_gptp_owner_claims(text, relpath, *, exempt_obsolete=True):
    """Reject claims that make the retired (#259) linuxptp an active gPTP owner."""
    lines = text.splitlines()
    if relpath.startswith("historical_now_obsolete/"):
        return []
    if (exempt_obsolete and lines
            and OBSOLETE_HEADER_RE.fullmatch(lines[0])):
        return []
    findings = []
    for index, line in enumerate(lines):
        if not GPTP_LINUX_RE.search(line):
            continue
        lo, hi = max(0, index - 1), min(len(lines), index + 2)
        window = " ".join(lines[lo:hi])
        if (GPTP_OWNER_CLAIM_RE.search(window)
                and not GPTP_OWNER_QUALIFIER_RE.search(window)):
            findings.append(
                f"{relpath}:{index + 1}: linuxptp gPTP-owner claim without "
                "a retirement marker, the software owner is retired (#259) "
                "and the fabric plane is the only gPTP owner")
    return findings


def main():
    findings = []
    md = tracked("*.md")
    resolve = make_resolver(md)
    tracked_set = set(md)
    for rel in md:
        path = REPO / rel
        findings.extend(check_md(path, rel, resolve, tracked_set))
        findings.extend(check_gptp_owner_claims(
            path.read_text(encoding="utf-8", errors="replace"), rel))
    # local-info sweep over diagram sources (text formats only)
    for pattern in ("docs/*.gen.py", "docs/*/*.gen.py", "docs/*.drawio",
                    "docs/*/*.drawio", "docs/*.svg", "docs/*/*.svg"):
        for rel in tracked(pattern):
            diagram_text = (REPO / rel).read_text(
                encoding="utf-8", errors="replace")
            findings.extend(check_gptp_owner_claims(
                diagram_text, rel, exempt_obsolete=False))
            for lineno, line in enumerate(diagram_text.splitlines(), 1):
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
