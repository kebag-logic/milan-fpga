#!/usr/bin/env python3
"""Docs gate: link integrity + wording deny-list + bare/dead references + local info.

Run from anywhere (the script locates its own repo root):

    python3 scripts/docs_check.py
    python3 scripts/docs_check.py --selftest   # the scrub arms alone

**No git required.** The file inventory comes from ``git ls-files`` when the tree
is a git working tree, and from a ``.gitignore``-aware filesystem walk otherwise —
so an extracted tarball or a downloaded zip can run the same gate CI runs.

The **privacy scrub** (rule 5) reads every tracked TEXT file, not just markdown:
this repo is public, and #247 found the peer's product name sitting in a
testbench comment where no gate could see it — the same blind spot that had let
a sibling token reach 22 tracked files on 2026-08-09. Vendored code
(``third_party/``) is out of scope, submodule gitlinks are not files here, and a
file carrying a NUL byte in its first 8 KiB is skipped exactly as ``git grep -I``
skips it, so the gate and the ``git grep -nI`` acceptance oracle cannot disagree.
The scrub's own arms run on EVERY invocation (``scrub self-test N/N`` in the
summary): a scrub that has never failed once is not evidence that it works.

Checks, over every ``*.md`` file in the tree:

1. **Link integrity** — every relative markdown link/image target resolves to
   a file or directory in the tree (http/mailto/anchor-only links skipped), and
   a ``#L123`` / ``#L123-L456`` line anchor names a line the target file still
   has. Documentation cites RTL by line, RTL files grow by hundreds of lines
   between rounds, and an anchor past EOF drops the reader at the bottom of a
   file with no hint that the citation is stale.
2. **Wording deny-list** — terms that must not appear in committed docs.
   Legitimate identifiers containing a denied stem are masked (``ALLOW``).
   Markdown only, deliberately: these are rules about how PROSE reads, and
   the stems are ordinary words elsewhere in the tree — the CRF format's
   normative name appears in RTL banners, and gate comments say "certify"
   about their own checks. The absolute rules live in the scrub (rule 5).
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
5. **Privacy scrub** (every tracked text file, see above) — private identities
   (the reference peer's product name, the compliance lab and suite names) and
   bench/host-identifying patterns (home paths, bench addresses, bench host
   prefix, MAC-derived interface names, USB-serial paths) must not appear.
   Every class is judged on every line, so one line can carry two findings: a
   ``continue`` between them would mean a correct scrub REVEALS a new finding
   and the gate could never be driven green in one pass. A finding names its
   CLASS and column and never quotes the match — CI logs are public too.
6. **Writing hygiene** (living pages only, fences and HTML comments exempt) —
   no process/meta narration (handover/round/session-of-authoring language),
   no decisions attributed to a person or quoted conversation, no section
   sign in prose, and no un-anchored ``X.md Section N`` pointers. The archive
   and in-place-obsolete pages (first line ``[OBSOLETE + date]``, the regex
   lifted from ``check_archive.py``) are records of their time and exempt.
Exit 0 = clean; exit 1 = findings, one per line as ``path:line: message``;
exit 2 = a scrub arm did not bite, which makes rule 5 unproven, not clean.
"""

import argparse
import fnmatch
import os
import re
import subprocess
import sys
import tempfile
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

DENY_CI = re.compile(r"avnu|certif", re.IGNORECASE)


#! THE PRIVATE TOKENS ARE ASSEMBLED, NOT WRITTEN OUT. This file is tracked on a
#! public repo, and a denylist that spells the names it forbids publishes them
#! just as surely as the document it is meant to catch — the first cut of this
#! gate did exactly that, trading one leaked name for three. Until #247 the
#! gate read only *.md, so it could not catch itself and the suite stem sat in
#! `DENY_CI` above as the last occurrence in the tree; the scrub now reads this
#! file like any other, and the assembly is what keeps it green honestly.
def _asm(*codes):
    """A literal from its code points, so the source never spells it."""
    return "".join(chr(c) for c in codes)


#! Case-SENSITIVE: these are short acronyms whose lowercase forms are ordinary
#! words or live inside longer identifiers. A review found one of them sitting
#! in a tracked document for weeks — the case-insensitive list above could
#! never have matched it, and no stem for a certification LAB name existed.
#! Committed text says "compliance", never a lab.
_LAB_TOKENS = tuple(_asm(*cs) for cs in (
    (67, 69, 82, 84), (65, 84, 76), (85, 78, 72), (73, 79, 76),
))
DENY_CS = re.compile("|".join(r"\b%s\b" % t for t in _LAB_TOKENS))

#: The privacy scrub (rule 5), tree-wide: (pattern, class, what to write). The
#: class is what a finding prints — never the match, because the CI log of a
#: public repo republishes whatever a finding quotes.
#:
#: The peer stem carries a trailing ``\w*`` because the model designation has a
#: long and a short spelling and #247 found one of each; the stem plus the
#: word boundary catches both, and any third spelling, without listing them.
#: Case-insensitive: neither private token is an ordinary word in any case.
_SUITE_TOKEN = _asm(97, 101, 116, 115)
_PEER_TOKEN = _asm(68, 83, 50, 48)
IDENTITY_RULES = (
    (DENY_CS, "compliance lab name", "committed text says 'compliance'"),
    (re.compile(r"\b%s\w*" % _SUITE_TOKEN, re.IGNORECASE),
     "compliance suite name", "committed text says 'compliance'"),
    (re.compile(r"\b%s\w*" % _PEER_TOKEN, re.IGNORECASE),
     "peer product name", "the public tree says 'the peer' or 'a test device'"),
)

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
    # #259 removed the retired host software stack from the tracked tree.
    # DOC_GENERATION.md section 5: retiring a document means registering its
    # basename here, or the next bare mention of it is invisible to rule 4.
    "APLAY_SOFTWARE_PATH_AUDIT_0803.md",
    "CPPI_DMA_REDESIGN.md",
    "DOC_AUDIT.md",
    "FULLY_FPGA_RISCV_MIGRATION.md",
    "GPTP_GM_LOSS_UNDER_RX_LOAD.md",
    "GPTP_RXPAD_ROOTCAUSE.md",
    "HANDOVER_0728.md",
    "HANDOVER_0731.md",
    "HANDOVER_0801.md",
    "HANDOVER_0802.md",
    "HANDOVER_0805.md",
    "HISTORY_PRE_SHORTEN_0731.md",
    "HOWTO_PLAY_MUSIC.md",
    "M-A2-2026-08-01.md",
    "PIPEWIRE_AVB_PEER.md",
    "PTP_TS_METADATA_FIX.md",
    "REF_LISTENER_TIMESTAMP_SWEEP_0727.md",
    "RX_FANOUT_AND_TX_CEILING.md",
    "RX_MEMORY_HIERARCHY_PLAN.md",
    "TCP_THROUGHPUT_COLLAPSE_0803.md",
    "TRUE_E2E_REQUIREMENTS.md",
    "VIRTUAL_E2E_HOWTO.md",
    "VIRTUAL_E2E_PLAN.md",
    "VIRTUAL_E2E_QEMU.md",
    "VIRTUAL_E2E_TEST_PROCEDURE.md",
    "VIRTUAL_SWITCH_RESEARCH.md",
    "kl-eth-tx-debug.md",
    "virtual-e2e-all-2026-08-01.md",
    "virtual-e2e-env-check-2026-08-01.md",
    "virtual-e2e-env.md",
    "virtual-e2e-t1-2026-08-01.md",
    "virtual-e2e-t2-prep-2026-08-01.md",
}

#: Bench/host-identifying patterns, same shape as IDENTITY_RULES. Generic
#: SHAPES wherever a shape exists: the home-path and address rules used to
#: name this bench's account and subnet, which made the gate the one file in
#: the tree carrying them and let any other account's path through. Only the
#: bench host prefix has no shape, so it is assembled. The board harness keeps
#: a stricter arm of its own over harness/board (test_harness.py
#: test_board_scripts); this sweep is the tree-wide floor under it.
_BENCH_HOST_TOKEN = _asm(97, 109, 120)
LOCAL_RULES = (
    (re.compile(r"/home/[a-z][a-z0-9._-]*"), "home path",
     "write ~ or $HOME"),
    (re.compile(r"\b192\.168\.\d+"), "bench address",
     "name the link, not its address"),
    (re.compile(r"\b%s-" % _BENCH_HOST_TOKEN), "bench host prefix",
     "name the role, not the host"),
    (re.compile(r"\benx[0-9a-f]{8,}"), "MAC-derived interface name",
     "name the port, not the interface"),
    (re.compile(r"serial/by-id/usb-[A-Za-z0-9]"), "USB serial path",
     "name the adapter, not its serial"),
)

#: Rule 5 in full. One table, one loop, one message shape.
SCRUB_RULES = IDENTITY_RULES + LOCAL_RULES

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
    """Crude .gitignore reader: (rooted globs, basename globs, un-ignore globs).

    Only the shapes this repo uses are honoured — directory entries, rooted
    path globs, bare basenames, and ``!`` re-inclusions of a directory an
    earlier rule excluded; nested per-directory ``.gitignore`` files are not
    read (``ALWAYS_PRUNE_GLOBS`` covers what they hide). The ``!`` half is what
    keeps the five tracked ``configs/generated/*/gen/*.svh`` emissions in the
    inventory: ``configs/generated/*/*`` excludes their directory and
    ``!configs/generated/*/gen/`` puts it back, so dropping the negation made
    the no-git walk five files short of ``git ls-files`` — invisible while the
    inventory only fed markdown link checks, a hole in the privacy scrub (rule
    5) once it reads every tracked text file. This reproduces ``git ls-files``
    exactly today apart from submodule gitlinks, which git reports as files and
    a filesystem walk cannot. To re-check that after editing::

        python3 -c "import sys; sys.path.insert(0,'scripts'); import docs_check as d; \
                    g=set(d._git_files()); w=set(d._walk_files()); \
                    print(sorted(g^w))"
    """
    rooted, basenames, unignored = [], [], []
    gi = REPO / ".gitignore"
    if gi.is_file():
        for raw in gi.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            negated = line.startswith("!")
            line = line.lstrip("!").rstrip("/")
            if not line:
                continue
            if negated:
                unignored.append(line.lstrip("/"))
            else:
                (rooted if "/" in line.strip("/") else basenames).append(
                    line.lstrip("/"))
    return rooted, basenames, unignored


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
    rooted, basenames, unignored = _ignore_matchers()
    pruned = _submodule_paths()

    def reincluded(rel):
        """``rel``, or a directory above it, is named by a ``!`` rule."""
        here = Path(rel)
        candidates = [str(here)] + [str(p) for p in here.parents if str(p) != "."]
        return any(fnmatch.fnmatch(c, pat)
                   for c in candidates for pat in unignored)

    def ignored(rel, name):
        if name in ALWAYS_PRUNE or rel in pruned:
            return True
        if any(fnmatch.fnmatch(name, pat) for pat in ALWAYS_PRUNE_GLOBS):
            return True
        # A `!` rule re-includes the directory it names and everything under
        # it. git resolves rules in file order; this tree only ever negates
        # AFTER the exclusion, so last-match-wins and negation-wins agree.
        if reincluded(rel):
            return False
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

        # --- wording deny-list (everywhere, fences included) ---
        # Prose only. The privacy scrub reads this page too, as one of the
        # tracked text files, so nothing here repeats it.
        masked = line
        for allow in ALLOW:
            masked = masked.replace(allow, "#" * len(allow))
        m = DENY_CI.search(masked)
        if m:
            findings.append(f"{relpath}:{lineno}: denied wording '{m.group(0)}'")

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


# --------------------------------------------------------------------------
# rule 5: the privacy scrub, over every tracked text file
# --------------------------------------------------------------------------
def scrub_text(relpath, text):
    """Findings for one file's text: every rule, every line, class not match."""
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern, label, remedy in SCRUB_RULES:
            m = pattern.search(line)
            if m:
                findings.append(f"{relpath}:{lineno}: {label} at column "
                                f"{m.start() + 1} — {remedy}")
    return findings


def scrub_files(root, relpaths):
    """(findings, files scanned) for the scrub over ``relpaths`` under ``root``.

    Three exclusions, each of them arm-covered in ``scrub_selftest``:
    ``third_party/`` is vendored code this repo does not write; a gitlink is a
    directory here, not a file; and a NUL byte in the first 8 KiB means binary,
    which is exactly what ``git grep -I`` skips — the acceptance oracle for
    #247 is a ``git grep -nI``, and a gate that disagreed with its own oracle
    would go green on a tree the oracle calls dirty. Undecodable bytes are NOT
    an exclusion: they are replaced, so a latin-1 file is still read.
    """
    findings, scanned = [], 0
    for rel in relpaths:
        if rel.startswith("third_party/"):
            continue
        path = Path(root) / rel
        if not path.is_file():
            continue
        try:
            raw = path.read_bytes()
        except OSError as exc:
            findings.append(f"{rel}:0: unreadable — {exc.strerror}")
            continue
        if b"\0" in raw[:8000]:
            continue
        scanned += 1
        findings.extend(scrub_text(rel, raw.decode(errors="replace")))
    return findings, scanned


def scrub_selftest():
    """Plant each class in a NON-markdown file and require the scrub to bite.

    (problems, arms, skipped). #247: "a scrub gate that has never failed once
    is not evidence that it works", so these run on every invocation, not
    behind a flag nobody types.
    """
    problems, arms, skipped = [], 0, []

    def arm(name, rel, body, expect_label):
        """One planted file. ``expect_label`` None = the fixture must stay clean."""
        nonlocal arms
        arms += 1
        with tempfile.TemporaryDirectory(prefix="docscheck.") as tmp:
            target = Path(tmp) / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body if isinstance(body, bytes)
                               else body.encode())
            findings, _ = scrub_files(tmp, [rel])
        text = "\n".join(findings)
        if expect_label is None:
            if findings:
                problems.append(f"[{name}] clean fixture flagged:\n{text}")
        elif not findings:
            problems.append(f"[{name}] planted defect not caught")
        elif expect_label not in text:
            problems.append(f"[{name}] caught, but not as {expect_label!r}:"
                            f"\n{text}")

    # Every rule in the table has a fixture, and the fixture is in a file type
    # the gate could not see before #247. A count floor with no content floor
    # is how an arm list quietly stops covering a rule it used to cover.
    fixtures = (
        # (name, path, line, expected class)
        ("peer-long", "tb/verilator/x/sim_main.cpp",
         f"    //! the peer ({_PEER_TOKEN}D declared 4ch) accepts\n",
         "peer product name"),
        ("peer-short-lowercase", "scripts/probe.py",
         f"# the {_PEER_TOKEN.lower()} answered the probe\n",
         "peer product name"),
        ("suite", "tests/features/x.feature",
         f"    # {_SUITE_TOKEN} es-4.5 covers this step\n",
         "compliance suite name"),
        ("lab", "hdl/milan/x.sv",
         f"// verified at the {_LAB_TOKENS[0]} plugfest\n",
         "compliance lab name"),
        # The four shape fixtures are SPLIT at the exact junction their rule
        # matches on, so building them here cannot make this file a finding of
        # its own sweep. Join one back into a single literal and the
        # gate-scans-itself arm below reddens: the discipline is self-enforcing.
        ("home-path", "syn/yosys/x.py",
         "    # resolved to /home/" + "someone/work instead\n", "home path"),
        ("bench-address", "tests/features/y.feature",
         "    # iperf3 -c 192.168." + "127.1 -u -b 950M\n", "bench address"),
        ("bench-host", "harness/board/x.sh",
         f"# {_BENCH_HOST_TOKEN}-pi drives outlet 4\n", "bench host prefix"),
        ("interface-name", "configs/x.yaml",
         "  iface: enx" + "0011223344ff\n", "MAC-derived interface name"),
        ("usb-serial", "docs/diagrams/x.svg",
         "<svg><text>/dev/serial/by-id/usb-" + "FTDI_x</text></svg>\n",
         "USB serial path"),
    )
    for name, rel, body, label in fixtures:
        arm(name, rel, body, label)
    covered = {label for _, _, _, label in fixtures}
    declared = {label for _, label, _ in SCRUB_RULES}
    if covered != declared:
        problems.append(f"[coverage] no fixture for {sorted(declared - covered)}"
                        if declared - covered else
                        f"[coverage] fixture for a retired class "
                        f"{sorted(covered - declared)}")

    # negative controls: what the rules deliberately do NOT catch
    arm("clean-control", "hdl/milan/clean.sv",
        "//! the peer's listener accepts the declared format\n", None)
    arm("lab-lowercase-is-a-word", "scripts/clean.py",
        f"# a stale base can {_LAB_TOKENS[0].lower()}ify the wrong tree\n", None)
    arm("peer-stem-inside-a-word", "scripts/clean2.py",
        f"# thousan{_PEER_TOKEN.lower()}00 samples\n", None)
    arm("vendored-code-is-out-of-scope",
        f"third_party/verilog-axis/{_PEER_TOKEN.lower()}.v",
        f"// {_PEER_TOKEN}D\n", None)
    arm("binary-is-skipped-like-git-grep-I", "syn/ooc/work/ucode.bin",
        b"\x00\x01" + f"{_PEER_TOKEN}D".encode(), None)

    # one line, two classes: a `continue` here would hide the second finding
    # until the first was fixed, and the gate could never be driven green in
    # one pass. Checked on the FINDING COUNT, which a class needle cannot see.
    arms += 1
    with tempfile.TemporaryDirectory(prefix="docscheck.") as tmp:
        rel = "scripts/two.py"
        (Path(tmp) / "scripts").mkdir()
        (Path(tmp) / rel).write_text(
            f"# {_PEER_TOKEN}D notes under /home/" + "someone/bench\n")
        both, _ = scrub_files(tmp, [rel])
    if len(both) != 2:
        problems.append(f"[two-classes-one-line] expected 2 findings, got "
                        f"{len(both)}:\n" + "\n".join(both))

    # This file is tracked text on a public repo, so the scrub reads it like
    # any other. Green here IS the proof that the assembly discipline holds.
    arms += 1
    own, _ = scrub_files(REPO, ["scripts/docs_check.py"])
    if own:
        problems.append("[gate-scans-itself] the gate spells what it forbids:"
                        "\n" + "\n".join(own))

    # What the scrub covers must not depend on whether the reader has git: the
    # no-git walk has to reach every file git tracks, submodule gitlinks aside
    # (git reports those as files, a walk cannot). Costs one walk, ~0.05 s.
    git_files = _git_files()
    if git_files is None:
        skipped.append("inventory parity (needs a git working tree)")
    else:
        arms += 1
        missed = set(git_files) - set(_walk_files()) - _submodule_paths()
        if missed:
            problems.append(f"[inventory-parity] the no-git walk misses "
                            f"{len(missed)} tracked file(s), so the scrub "
                            f"would not read them there: "
                            f"{sorted(missed)[:5]}")
    return problems, arms, skipped


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true",
                    help="run the rule-5 scrub arms and stop")
    args = ap.parse_args(argv)

    # Before any verdict: the scrub must still bite. An unproven rule 5 is
    # rc 2 (unproven), never rc 0 (clean) — those are different answers.
    problems, arms, skipped = scrub_selftest()
    for p in problems:
        print("  -", p, file=sys.stderr)
    if problems:
        print(f"docs_check: FATAL: {len(problems)} scrub arm(s) of {arms} did "
              f"not hold", file=sys.stderr)
        return 2
    note = f", {len(skipped)} skipped: {'; '.join(skipped)}" if skipped else ""
    if args.selftest:
        print(f"docs_check scrub selftest: PASS ({arms} arm(s){note})")
        return 0

    findings = []
    md = tracked("*.md")
    resolve = make_resolver(md)
    tracked_set = set(md)
    for rel in md:
        path = REPO / rel
        findings.extend(check_md(path, rel, resolve, tracked_set))
    # rule 5 over the whole tracked tree, markdown and diagram sources
    # included — before #247 this was a hand-listed sweep of six docs/ globs,
    # and everything outside them was invisible.
    scrub, scanned = scrub_files(REPO, inventory())
    findings.extend(scrub)
    findings = sorted(set(findings))
    for f in findings:
        print(f)
    print(f"docs_check: {len(findings)} finding(s) across {len(md)} md files "
          f"+ {scanned} scrubbed text files, scrub self-test {arms}/{arms}"
          f"{note} [{_INVENTORY_SOURCE}]")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
