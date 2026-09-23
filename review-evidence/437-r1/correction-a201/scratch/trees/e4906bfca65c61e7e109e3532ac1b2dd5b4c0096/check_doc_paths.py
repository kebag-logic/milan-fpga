#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: every repo path a committed document cites in backticks must exist.

Why this exists. The documentation is full of "the RTL is in `hdl/lwsrp/`"
pointers, and they are the first thing a reader follows. They are also the
first thing to rot, because nothing links them to the tree: a file can be
moved, renamed or retired and every document that names it stays green.

That is not hypothetical. Two tree-wide moves left 33 dangling citations:

  * the spec-aligned reorganisation (2026-07-22) moved `hdl/lwsrp/` to
    `hdl/ieee8021q/srp/`, `hdl/adp/` to `hdl/ieee17221/adp/`, and so on -
    13 stale `hdl/` citations across 5 documents, every one of them sending
    a reader to a directory that does not exist;
  * the documentation overhaul retired pages into versioned history;
    citations still referenced their previous locations.

Markdown *links* were fine throughout - all 1218 of them resolved. Only the
inline backtick citations rotted, because a link is visibly broken in a
rendered page and a backtick is not.

Scope. Committed markdown outside versioned history includes `docs/`,
`harness/`, and repository-root pages. `docs/history/v1/` is excluded.
Historical references intentionally preserve their recorded context.

Usage:
    python3 scripts/check_doc_paths.py           # gate (exit 1 on a dangling path)
    python3 scripts/check_doc_paths.py --list    # every citation and its verdict
"""
import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

#: prefixes that name something in THIS repo. A backticked token starting with
#: one of these is a claim about the tree, so it is checkable.
PREFIXES = ("hdl/", "sw/", "tb/", "syn/", "scripts/", "harness/", "tests/",
            "docs/", "third_party/", "sim/")

#: `path/like/this.sv` - the backticked-token shape, before punctuation strip
CITE_RE = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./+-]*)`")

#: a citation carrying any of these is a TEMPLATE, not a path: `tb/<suite>/`,
#: `hdl/**/*.sv`, `docs/{a,b}.md`. Nothing to check.
PLACEHOLDER = set("<>*?{}|")

#: `tb/utests/.../tb_x.sv` - an elided path, same idea as a `<placeholder>`
ELIDED = "/.../"

#: A page carrying this marker is a LEDGER: naming documents that were archived
#: or removed is its job. Same opt-out `scripts/docs_check.py` already honours,
#: spelled the same way, so a page opts out of both rules at once.
LEDGER_MARKER = "docs-check: allow-dead-refs"

#: Paths deliberately absent from the tree, with the reason. Each is a real
#: reference a reader may need - naming a file to say it is gone is legitimate
#: prose - so they are recorded here rather than deleted. The gate refuses
#: SILENT additions: a new dangling path fails until someone writes the reason.
ALLOW = {
    "tb/utests/802_1q_traffic_shaper/tb_credit_based_shaper.sv":
        "removed bench, named by REQUIREMENTS/TODO to record that "
        "tb/verilator/cbs supersedes it",
    "third_party/verilog-axi":
        "planned vendoring (THIRD_PARTY.md 'Planned'), not present yet",
    # The virtual-E2E environment cites artifacts a reader GENERATES by
    # following the very docs that cite them - a fresh checkout does not
    # carry them and must not (build outputs; the harness scripts land
    # with the QEMU-lane work when it resumes).
    "harness/transport.py":
        "virtual-E2E harness lane, generated/landed when the QEMU work "
        "resumes (VIRTUAL_E2E_QEMU.md is its design doc)",
    "harness/transport_virtual.py":
        "virtual-E2E harness lane, generated/landed when the QEMU work "
        "resumes",
    "sw/litex/build_milan_sim/":
        "sim BUILD OUTPUT directory - created by the build the doc "
        "teaches, never tracked",
    "sw/litex/build_milan_sim/gateware/build_sim.sh":
        "sim build output, created by the documented build",
    "sw/litex/build_milan_sim/gateware/sim.v":
        "sim build output, created by the documented build",
    "sw/litex/build_milan_sim/software/bios/bios.bin":
        "sim build output, created by the documented build",
}


def tracked() -> set[Path]:
    """Paths git knows about. An UNTRACKED page is a local working file - a
    handover, a scratch note - and it is allowed to point at anything,
    including other local-only files. Gating it would fail the gate on
    somebody's private notes."""
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z", "*.md"],
                         capture_output=True, text=True, check=True).stdout
    return {REPO / p for p in out.split("\0") if p}


def scanned_files() -> Iterator[Path]:
    """Committed markdown outside the archive."""
    known = tracked()
    for d in ("docs", "harness"):
        yield from (
            p
            for p in sorted((REPO / d).rglob("*.md"))
            if p in known
            and not p.relative_to(REPO).as_posix().startswith("docs/history/v1/")
        )
    yield from (p for p in sorted(REPO.glob("*.md")) if p in known)


def citations(text: str) -> Iterator[str]:
    """The backticked tokens in a page that are CLAIMS ABOUT THIS TREE. A
    template (`tb/<suite>/`) or an elided path names no single file, so it is
    not a claim and is dropped rather than reported as dangling."""
    for m in CITE_RE.finditer(text):
        tok = m.group(1)
        if not tok.startswith(PREFIXES):
            continue
        if PLACEHOLDER & set(tok) or ELIDED in tok:
            continue
        # trailing sentence punctuation is not part of the path
        yield tok.rstrip(".,;:")


def resolves(tok: str, md: Path) -> bool:
    """A citation may be repo-relative (`hdl/foo.sv`) or relative to the page
    that makes it (`harness/README.md` saying `tests/test_harness.py`). Both
    are honest ways to point at a file, so either resolving is a pass."""
    return (REPO / tok).exists() or (md.parent / tok).exists()


def ignored(toks: list[str]) -> set[str]:
    """Which of these paths git is told to ignore.

    A gitignored path is a BUILD ARTIFACT: `sw/builder/out/` exists in a clone
    where the builder has been run and not in a fresh worktree. Whether it is
    on disk is a fact about your machine, not about the documentation, and a
    gate that changes verdict between two checkouts of the same commit is
    worse than no gate - it trains people to ignore it. Naming an output
    directory in prose is legitimate, so these are accepted either way.
    """
    if not toks:
        return set()
    r = subprocess.run(["git", "-C", str(REPO), "check-ignore", "--stdin"],
                       input="\n".join(toks), capture_output=True, text=True)
    return {l.strip() for l in r.stdout.split("\n") if l.strip()}


#: A `#L123` line anchor that points past the end of its file is a SILENTER
#: rot than a dangling path: the link still resolves, the forge just clamps
#: to the last line, and the reader lands somewhere plausible and wrong. The
#: citation gate above cannot see it, because the PATH is fine - only the
#: line moved. Ranges are judged on their HIGH end, which is the one a
#: shrinking file invalidates first.
ANCHOR_RE = re.compile(r"\[([^\]]+)\]\(([^)#\s]+)#L(\d+)(?:-L(\d+))?\)")


def stale_anchors(md: Path) -> list[tuple[str, int, int]]:
    """(link target, cited last line, real line count) for anchors that
    overshoot. Missing targets are NOT reported here - the citation gate
    owns those, and reporting both would print one move as two findings."""
    out = []
    for _label, rel, lo, hi in ANCHOR_RE.findall(md.read_text()):
        target = (md.parent / rel).resolve()
        if not target.is_file():
            continue
        n = sum(1 for _ in target.open(errors="replace"))
        last = int(hi or lo)
        if last > n:
            out.append((rel, last, n))
    return out


def main() -> int:
    """The gate: every cited repo path resolves and every line anchor still
    lands inside the file it names. Build artifacts and ledger pages are
    excused; an ALLOW entry whose path came back is a note, not a failure."""
    listing = "--list" in sys.argv[1:]
    dangling, checked, allowed, ledgers = [], 0, 0, 0
    anchors_checked, overshoot = 0, []

    for md in scanned_files():
        rel = md.relative_to(REPO)
        text = md.read_text()
        if LEDGER_MARKER in text:
            ledgers += 1
            if listing:
                print(f"  ledger {rel} (opted out: {LEDGER_MARKER})")
            continue
        anchors_checked += len(ANCHOR_RE.findall(text))
        for rel_t, last, n in stale_anchors(md):
            overshoot.append((rel, rel_t, last, n))
            if listing:
                print(f"  ANCHOR {rel_t}#L{last} > {n} lines  <- {rel}")

        for tok in citations(text):
            checked += 1
            if resolves(tok, md):
                if listing:
                    print(f"  ok    {tok}")
                continue
            if tok in ALLOW:
                allowed += 1
                if listing:
                    print(f"  allow {tok}  ({ALLOW[tok]})")
                continue
            dangling.append((rel, tok))
            if listing:
                print(f"  DANGL {tok}  <- {rel}")

    # Build artifacts are not documentation facts - drop them before reporting.
    art = ignored([t for _, t in dangling])
    if art:
        dangling = [(r, t) for r, t in dangling if t not in art]
        allowed += len(art)

    if dangling:
        # group by path so one move does not print as twenty findings
        by_tok = {}
        for rel, tok in dangling:
            by_tok.setdefault(tok, []).append(str(rel))
        print(f"doc path gate: {len(by_tok)} dangling path(s) "
              f"in {len({r for r, _ in dangling})} document(s)\n")
        for tok, where in sorted(by_tok.items()):
            print(f"  MISSING  {tok}")
            for w in sorted(set(where)):
                print(f"           cited by {w}")
        print("\nA cited path that does not exist sends the reader nowhere. "
              "Repoint it, or\nif it is deliberately absent add it to ALLOW "
              "in this script WITH the reason.")
        return 1

    # An ALLOW entry whose path now EXISTS is itself stale - the exemption has
    # outlived its reason. Warn rather than fail: a file coming back is a good
    # change, and failing the gate on it would teach people to delete the gate.
    for tok, why in sorted(ALLOW.items()):
        if (REPO / tok).exists():
            print(f"note: ALLOW entry '{tok}' is stale - the path exists now "
                  f"({why}). Drop it from ALLOW in {Path(__file__).name}.")

    if overshoot:
        print(f"doc path gate: {len(overshoot)} line anchor(s) point past the "
              f"end of the file they cite\n")
        for src, tgt, last, n in sorted(overshoot):
            print(f"  ANCHOR   {tgt}#L{last}  but that file has {n} line(s)")
            print(f"           cited by {src}")
        print("\nThe path still resolves, so the reader is sent to the wrong "
              "place rather than\nnowhere. Repoint the anchor at the lines it "
              "meant.")
        return 1

    print(f"doc path gate: OK ({checked} cited paths all resolve"
          f"{f', {allowed} allowlisted' if allowed else ''}"
          f"{f', {ledgers} ledger page(s) skipped' if ledgers else ''}"
          f"; {anchors_checked} line anchor(s) within their file)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
