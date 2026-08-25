#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Parse every hdl/ module with Vivado's xvlog, so a construct Vivado's
front-end REJECTS but Verilator/sv2v ACCEPT is caught by a cheap local check.

WHY THIS EXISTS (issue #132). The whole verification bar shares one front-end
family: the 52-suite Verilator sweep, `scripts/lint_rtl.py`, and the
`syn/yosys/run.sh` portability gate all lower SystemVerilog through
Verilator or sv2v. Any construct where Vivado's front-end is STRICTER than
that family is invisible to the entire bar. Use-before-declaration is the
first one found: `KL_gptp_shadow.sv` used a signal above its declaration,
Verilator accepted it, every local gate was green, and Vivado answered

    ERROR: [VRFC 10-3380] identifier 'full_w' is used before its declaration
    ERROR: [VRFC 10-8530] module 'KL_gptp_shadow' is ignored ...

`synth_design` only WARNS (Synth 8-6901) and still builds, so even a bitstream
run would not have failed; and the file becomes ineligible for the xsim benches
under tb/utests and tb/itests. There will be other such constructs. This gate
is a second front-end opinion, run before Vivado's, on a bench box.

WHAT IT DOES. `xvlog -sv` ANALYSES (it does not elaborate or synthesise), so it
needs no project, no submodule instances, and a few seconds per file. Packages
are compiled first into one work library - detected by reading each file for a
`package` declaration, the same way scripts/pp_srcs.py does, never by filename -
then every other module is compiled INDEPENDENTLY against that library. Compiling
independently is load-bearing: xvlog stops analysing a compilation unit at the
first module error, so a single bad file in a shared compile masks every file
after it. One module per invocation enumerates them all, which a ratchet needs.

WHAT IT ANALYSES, exactly (widened by #224 and #236 - read the next paragraph
before narrowing it again): every TRACKED `.sv` AND `.v` under hdl/, and every
tracked design source under protocol-processor/hdl and gptp-processor/hdl. Those
two are not third-party leaf IP - they are the control plane milan_datapath
elaborates on every build, and the same sources scripts/pp_srcs.py hands the
Verilator sweep, the Yosys portability gate and both Vivado OOC flows, so #132's
argument applies to them exactly as it applies to hdl/. third_party/ and
external/ are NOT analysed: leaf IP this repository neither owns nor edits, which
scripts/lint_rtl.py already treats as resolution-only, never linted. The census
prints that scope in full every run, because the defect both issues reported was
a census claiming more than the measurement covered - "every hdl/ module" over a
set that excluded one tracked `.v` and every processor source.

THE #186 INVARIANT IS KEPT BY REFUSING, NOT BY NARROWING. This banner used to say
the gate reads only hdl/, so that an uninitialised submodule cannot make the tree
look cleaner than it is. That reason stands and is not weakened here; the
conclusion drawn from it does not, because its price was that the very class this
gate exists to catch had live occurrences in the pinned processors with no gate
at all (#236 measured 37 at the pin on dev, 51 at the pin PR #227 proposes). So
the scope widens and the invariant is enforced directly instead: unless every
processor tree IS the revision the superproject pins, the gate REFUSES - exit 2,
naming the state, the expected and actual revisions and the remediation - rather
than reporting a set the pin does not stand behind. That is scripts/lint_rtl.py's
shape, which #186 forced on the lint ratchet for this same reason.

THE POPULATION COMES FROM THE GITLINK, NOT FROM THE PATH. Proving each path is
the top of SOME repository holding tracked sources is not the same claim, and
[R0] on PR #242 reproduced both escapes it leaves open: standalone clones dropped
at the two gitlink paths (`git submodule status` prints `-` for both) and a
registered submodule moved off the pin (`+44489453` against a pinned `a25b5cc9`)
were each counted as "the pinned processors" - and a default run, measured, then
rewrote scripts/xvlog.budget from that 48-file population, turning 3 banked
findings into 5. TreeState below enumerates every state that answers REFUSE and
why each one would otherwise pass; nothing is enumerated until the tree is the
pinned population.

AND THE GITLINK IS READ WHOLE, NOT FILTERED. [R0] round 2 reproduced the same
class one level down: an index record set of `160000` stage 2 beside `100644`
stage 3, and a one-sided `160000` stage 2, are both UNMERGED - `git submodule
status` prints `U000...` - yet keeping the one surviving `160000` SHA made each
read as a resolved pin and enumerated all 40 processor sources. The accepted
index shape is now exactly ONE record at the path, mode `160000`, stage `0`;
any other stage, any other mode, any extra record, an unparsable record or a
record only UNDER the path refuses before enumeration, census, budget read or
budget write. _index_pin below is that enumeration.

AND THE BYTES ARE PROVED, NOT INFERRED FROM AN INDEX ANSWER. [R0] round 3 found
the same class a THIRD time, one level down again: the checkout side asked git
`diff --name-only HEAD --`, and git answers that question with the index's
worktree hints applied. `git update-index --assume-unchanged` and
`--skip-worktree` each make a changed or a deleted file invisible to it, to
`git status` and to `git ls-files`'s idea of what is there; a real
use-before-declaration planted under `assume-unchanged` was analysed, printed
as the pinned census, reported as an ordinary ratchet regression and exited 1,
not the setup 2. Enumerating those two hints - and then the next one - would be
the fourth instance of one class, so the shape changes instead: the question is
no longer asked at all.

The pinned population is now DERIVED FROM THE PIN OBJECT (`git ls-tree -r <pin>`
inside the checkout, never `git ls-files`), and every file in it must hash to
the blob id the pin records, over the exact bytes on disk that xvlog will open,
before anything is analysed. That is a POSITIVE per-file proof rather than the
absence of known-bad signals: no index record, no stage, no refresh hint, no
sparse or skip-worktree state, no fsmonitor, no `.git` file indirection and no
clean/smudge filter participates in it, so a state nobody has enumerated yet
cannot make the proof succeed - it can only fail to reproduce a blob id. The
state names below exist to give a reader the right message and the right fix.
They never decide acceptance; the hash equality does.

THE PARENT'S OWN hdl/ IS NOT PROVED THAT WAY, deliberately: it IS the tree
under test. A local edit under hdl/ is exactly what the author is gating, so
the bytes on disk are the population by definition and there is no revision
they should equal. The processors are the opposite case - the superproject
DECLARES which revision they are, so a local edit there makes the census claim
bytes nobody committed and lets a default run bank a ratchet from them.

ONE FINDING PER MODULE, NOT ONE PER OCCURRENCE. xvlog stops at the first error in
a compilation unit and prints only the 10-8530 cascade after it, so a module with
many use-before-declaration occurrences yields ONE finding, naming the first
identifier. Measured 2026-08-24 on the processor top that `synth_design` reports
with 35 `Synth 8-6901` warnings: xvlog prints exactly one 10-3380 plus the
cascade, and `xvlog --help` in 2026.1 offers no continue-on-error switch. Fixing
that first occurrence banks one key and raises the next, so --check fails in both
directions at once and the new front is re-banked deliberately. That is the
ratchet working, not churn: the finding set changed, and it said so.

WHAT IT STILL CANNOT SEE: elaboration. Splitting a declaration-with-initialiser
(`reg [7:0] r = 8'd0;`) into a declaration plus a continuous `assign` is NOT
equivalent - an initialiser runs once at time zero, a continuous assign drives
forever - and xvlog, Verilator 5.050 under -Wall, sv2v and Yosys all accept the
broken form silently (#224). Only `xelab` rejects it, with VRFC 10-9171, and
`xelab` appears nowhere in this repository: the required `elaborate` context is
the LiteX/Verilator elaboration in sw/builder/test_builder.py. #224 leaves that
arm deliberately open; a lane doing declaration-order work has no gate for it.

TOOL ABSENCE IS A SKIP, NEVER A FALSE GREEN. With no xvlog on the box (CI has
none) the gate prints a visible SKIP marker and exits 0, the tsn-gen precedent.
The skip is decided BEFORE the setup refusal, on purpose: with no tool
nothing can be measured at all, so refusing there would turn a gate CONTRIBUTING
section 3 calls inert in CI into a red one, and a skip already reads as not a
pass.

THE RATCHET keys on the finding IDENTITY `path|CODE|identifier`, not on a count.
A count ratchet cannot see a compensating swap - one finding fixed while another
appears in the same commit nets to zero (the lesson of #150). An identity set
fails on any NEW finding AND on any grandfathered finding that has silently
vanished (bank the improvement deliberately), so neither direction is silent.
Today's backlog is grandfathered in scripts/xvlog.budget and printed in full;
the underlying defects are their own ticket, not this gate's to fix.

THE BUDGET HAS TWO SECTIONS, hdl/ and the pinned processors, and a key cannot
move between them: a finding's section is DERIVED from its own path and a budget
filing a key under the other section is rejected as malformed. Donor debt can
therefore never be traded against hdl/ debt, and the empty hdl/ section #193
reached stays visibly empty instead of being absorbed into a joint total.

A PROCESSOR KEY IS SPELLED `<submodule>:<path>`, never `<submodule>/<path>`.
scripts/pp_srcs.py --check - a required `rtl-fast` context - fails any tracked
file outside its PROSE_OK table that names a submodule source literally, and this
ratchet is a tracked file whose whole job is to name them. Measured 2026-08-24
against pp_srcs.check(): the `/` spelling fails it, the `:` spelling does not.
Widening PROSE_OK instead would put a hand-maintained list of submodule sources
back in the tree, which is the defect pp_srcs.py exists to prevent. The colon
also carries the population inside the key, which is what the two sections above
are checked against.

    scripts/xvlog_gate.py            # analyse, print the census, LOWER the ratchet
    scripts/xvlog_gate.py --check    # gate: fail on a NEW or a vanished finding
    scripts/xvlog_gate.py --selftest # prove the gate reddens on a planted fault

Exit 0 = at the ratchet (or skipped), 1 = regression / vanished finding / a
package that will not analyse, 2 = usage or setup error, including a processor
tree that is not the revision this commit pins, and a malformed budget.
"""

import argparse
import contextlib
import hashlib
import io
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

#: Repository root, from this file's location.
ROOT = pathlib.Path(__file__).resolve().parent.parent
HDL = ROOT / "hdl"
BUDGET = ROOT / "scripts" / "xvlog.budget"

#: Include search path and defines, the same set syn/yosys/run.sh hands the
#: portability sweep, so the two front-ends see the same preprocessor world.
INCLUDE_DIRS = [
    "hdl/common",
    "hdl/common/csr",
    "hdl/ieee8021q/ts",
    "hdl/common/eth_event_counter",
    "hdl/ieee17221/adp",
    "hdl/ieee8021as/ptp_timestamp",
]
DEFINES = ["SYNTHESIS"]

#: The pinned processor trees analysed alongside hdl/, each with the reason its
#: sources belong in a gate about THIS repository's front-end risk, printed by
#: the refusal when it is not the pinned checkout. Nothing here is resolved or
#: elaborated - xvlog analyses one file at a time - so unlike lint_rtl.py's
#: REQUIRED_TREES this list deliberately omits third_party/verilog-axis (leaf IP,
#: resolution only) and external/ (SSH-only; CONTRIBUTING 2.2 keeps it out of the
#: documented local-bar init, so requiring it would refuse on every lane).
SUBMODULE_TREES = [
    ("protocol-processor", "protocol-processor/hdl",
     "the ATDECC/SRP control plane milan_datapath elaborates via KL_pp_shadow"),
    ("gptp-processor", "gptp-processor/hdl",
     "the 802.1AS engine milan_datapath elaborates via KL_gptp_shadow"),
]

#: Budget/census sections, in print order, with the words the census uses for
#: each. A finding belongs to exactly one, derived from its path.
SECTIONS = ["hdl", "submodules"]
SECTION_LABEL = {"hdl": "hdl/", "submodules": "pinned processors"}

#: Where a bench install puts Vivado (docs/reference: 2026.1). $XVLOG wins, then
#: these, then PATH. Read, not restated in three places.
XVLOG_CANDIDATES = [
    "/home/alex/Xilinx/2026.1/Vivado/bin/xvlog",
    "/home/alex/Xilinx2/2026.1/Vivado/bin/xvlog",
]

#: The cascade line xvlog prints AFTER a real error ("module X is ignored due to
#: previous errors"). It is a consequence, not a finding, and naming it as one
#: would double-count every defect.
_CASCADE = "VRFC 10-8530"

_PACKAGE_RE = re.compile(r"^\s*package\s+\w+\s*;", re.M)
_CODE_RE = re.compile(r"\[(VRFC \d+-\d+)\]")
_IDENT_RE = re.compile(r"identifier '([^']+)'")
_LOC_RE = re.compile(r"\[([^\]\s]+):(\d+)\]\s*$")


def display_path(rel):
    """The path a finding is KEYED on: `<submodule>:<path>` inside a processor.

    A processor source is spelled with a colon rather than a slash because
    scripts/pp_srcs.py --check fails any tracked file outside its PROSE_OK table
    that names a submodule source literally, and scripts/xvlog.budget is a
    tracked file that must name exactly those sources (see the module docstring
    for the measurement). Everything else is unchanged, so an hdl/ key reads
    today as it read before, and an absolute path - the self-test's planted
    temp file - passes straight through.
    """
    for label, _tree, _why in SUBMODULE_TREES:
        if rel.startswith(label + "/"):
            return label + ":" + rel[len(label) + 1:]
    return rel


def section_of(key_or_path):
    """Which budget section a finding key (or its path) belongs to.

    Derived from the path, never stored alongside it: a section a writer could
    choose independently of the finding is a section a hand edit can move a key
    into, which is exactly the trade between donor and hdl/ debt the two
    sections exist to prevent.
    """
    head = key_or_path.split("|", 1)[0]
    for label, _tree, _why in SUBMODULE_TREES:
        if head.startswith(label + ":"):
            return "submodules"
    return "hdl"


class Finding:
    """One xvlog defect, keyed on identity, carrying every line it occurs on.

    The key is path + code + identifier and deliberately omits the line: a
    line number drifts as the file is edited, and one identifier used before
    its declaration in several places is ONE defect (the fix, moving the
    declaration up, addresses them together). The lines are kept as detail.
    """

    def __init__(self, path, code, identifier, line, message):
        self.path = path            # hdl-relative path of the module compiled
        self.code = code            # e.g. "VRFC 10-3380", or "" if none parsed
        self.identifier = identifier or ""
        self.lines = [line] if line else []
        self.message = message

    def merge(self, other):
        for ln in other.lines:
            if ln not in self.lines:
                self.lines.append(ln)

    @property
    def key(self):
        # Most VRFC errors name an identifier, and that is the stable key. Some
        # (a syntax error, an unopenable include) carry none, and keying two
        # DISTINCT such defects in one file as `path|code|` would collapse them:
        # once one is grandfathered, a different one of the same code hides
        # behind the banked key. So an identifier-less finding is discriminated
        # by a short hash of its message - stable across line moves, unlike the
        # line number, and distinct per defect ([R1] on PR #194).
        # The discriminator is prefixed `~`, NOT `#`: the budget's trailing
        # `# line(s) N` comment is stripped at the first `#`, so a `#`-keyed
        # finding wrote one key and read back a different, truncated one --
        # it could never be banked, only re-reported forever ([R0] on
        # PR #222 proved it end to end). `~` cannot appear in a path, a
        # VRFC code or an identifier.
        # An ESCAPED SystemVerilog identifier is terminated by whitespace,
        # which is a delimiter and not part of the name. It must not reach
        # the key: the budget is line-based, so a trailing space would be
        # invisible, would make `git diff --check` refuse the generated
        # file, and would not survive the reader's strip.
        ident = (self.identifier or "").strip() or (
            "~" + hashlib.sha1(self.message.encode("utf-8",
                                                   "replace")).hexdigest()[:8])
        return f"{self.path}|{self.code}|{ident}"

    def detail(self):
        loc = f":{','.join(self.lines)}" if self.lines else ""
        ident = f" '{self.identifier}'" if self.identifier else ""
        return f"{self.path}{loc}  [{self.code}]{ident}  {self.message}"


def find_xvlog():
    """An xvlog executable, or None."""
    env = os.environ.get("XVLOG")
    if env and os.path.exists(env):
        return env
    for cand in XVLOG_CANDIDATES:
        if os.path.exists(cand):
            return cand
    return shutil.which("xvlog")


def _split_packages(files):
    """(packages, modules) - a package is a file that DECLARES one, read.

    Keying on a `_pkg.sv` suffix is a naming convention; a package in a file
    named otherwise would sort after its importers and fail to analyse. Same
    rule, same reason, as scripts/pp_srcs.py.
    """
    pkgs = [f for f in files if _PACKAGE_RE.search((ROOT / f).read_text())]
    rest = [f for f in files if f not in set(pkgs)]
    return pkgs, rest


def hdl_sources():
    """Tracked hdl/ design sources, packages first then the rest, both sorted.

    Tracked only (git ls-files): analysing an untracked stray source is a build
    no other checkout can reproduce - the same rule pp_srcs.py keeps.

    BOTH `.sv` AND `.v`. The glob was `*.sv` alone and silently excluded
    hdl/milan/milan_dma_wrapper.v, the one tracked Verilog-2001 module under
    hdl/, while the census claimed every hdl/ module (#224). It is a real
    module - bd/build.tcl ships it and scripts/lint_rtl.py carries a named
    LINT_EXCLUDE waiver for it - and being outside the fabric build is a reason
    not to LINT it, not a reason to leave it out of a parse census that says
    "every". `.svh` is not matched: an include header is analysed through the
    file that includes it, and compiling one alone is not a compilation unit.
    """
    out = _git(["ls-files",
                "hdl/**/*.sv", "hdl/*.sv", "hdl/**/*.v", "hdl/*.v"], ROOT)
    if out.returncode:
        raise SystemExit(f"git ls-files failed: {out.stderr.strip()}")
    files = sorted(set(out.stdout.split()))
    if not files:
        raise SystemExit("no tracked hdl/ .sv or .v files found")
    return _split_packages(files)


#: Environment variables that REDIRECT what a `git -C <dir>` call reads - the
#: git directory, the index, the object store, the ref namespace. They are
#: cleared for every call below so that `cwd` means what it says. The byte
#: proof itself does not need this (a pin SHA comes from the superproject's own
#: index record, the object it names is content-addressed, and the file bytes
#: come from the filesystem), but the states decided AROUND it - which
#: repository the path is, what its HEAD is - would otherwise be answerable
#: from a different repository entirely.
_GIT_ENV_OVERRIDES = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                      "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
                      "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE")


def _git(args, cwd):
    """One git invocation, captured. `cwd` must already be known to be a repo."""
    env = {k: v for k, v in os.environ.items()
           if k not in _GIT_ENV_OVERRIDES}
    return subprocess.run(["git"] + args, cwd=str(cwd),
                          capture_output=True, text=True, env=env)


class TreeState:
    """What the superproject PINS at one processor path, and what is there.

    THE POPULATION IS ESTABLISHED FROM THE SUPERPROJECT'S GITLINK, never from
    whatever happens to sit at the path. Proving the path is the top of *some*
    repository holding tracked sources is not that proof, and [R0] on PR #242
    reproduced both escapes it leaves open, from a fresh checkout:

      - standalone clones dropped at the two gitlink paths, submodules never
        initialised: `git submodule status` printed the `-` prefix for both,
        yet the refusal returned nothing, the plan counted 46 processor files
        and the census called them "the pinned processors";
      - the superproject pinned at a25b5cc9 with the protocol checkout at
        44489453: `git submodule status` printed `+44489453`, the refusal again
        returned nothing, and a DEFAULT run (no --check) rewrote
        scripts/xvlog.budget from that 48-file population - measured, 3 banked
        findings became 5, with a line number silently moved.

    That is the pin-bump false green #236 exists to close, so the check is now
    the superproject's declaration compared against the checkout, and it
    refuses BEFORE anything is enumerated.

    Reading the CHECKOUT loosely is that class once more, and [R0] round 3
    reproduced it on the tracked source KL_pp_prng.sv: with
    `git update-index --assume-unchanged` (or `--skip-worktree`) set, an edited
    file is invisible to `git status` and to `git diff --name-only HEAD --`,
    which is the question the old check asked. No question is asked now. The
    population comes from the pin's own tree object and every file in it is
    HASHED and compared to the blob id the pin records, so acceptance is a
    positive proof over the bytes xvlog opens rather than the absence of a
    known-bad signal.

    Reading that declaration LOOSELY is the same class one level down, and
    [R0] round 2 reproduced it twice: an index holding `160000` stage 2 beside
    `100644` stage 3, and one holding only `160000` stage 2. `git submodule
    status` printed `U000...` for both; keeping the surviving `160000` SHA
    made each read as a resolved pin and enumerated all 40 sources. The index
    shape is therefore matched whole against the ONE usable shape (see
    _index_pin), never filtered down to the records that look usable.

    `state` is one of, in the order they are decided:

      unregistered    the index carries no stage 0 160000 gitlink AT the
                      path - no record at all, a tracked file or symlink at
                      the path, or the contents committed as ordinary files
                      under it - or .gitmodules does not name it
      conflicted      the index is UNMERGED at the path: any record at stage
                      1, 2 or 3, more than one record, or a record that will
                      not parse. There is no revision the next commit carries,
                      whatever surviving SHA a filter would have kept
      absent          registered, but there is nothing at the path - no
                      directory, or the empty one a fresh clone and
                      `git worktree add` leave behind
      not-a-directory registered, but a file or a symlink sits at the gitlink
                      path where the checkout must be
      uninitialised   registered, a directory, but the superproject has no
                      `submodule.<name>.url`: whatever is at the path is NOT
                      the registered checkout. This is git's own definition of
                      the `-` prefix and it is exactly what a standalone clone
                      dropped at the path looks like
      no-repository   the directory is not that repository's own top level. An
                      aborted `submodule update` leaves one, and `git -C` WALKS
                      UP from it to the SUPERPROJECT - the gate would answer
                      with hdl/ twice and call the processors covered
      wrong-revision  HEAD is not the pinned revision (git's `+` prefix)
      unreadable      HEAD is the pinned revision, but the pin's own tree
                      cannot be read (an object format whose blob ids this
                      gate cannot reproduce, an unreadable or unparsable tree
                      record): there is no population to prove
      unpinnable      the PIN ITSELF names a `.sv`/`.v` entry that is not a
                      regular-file blob - a committed symlink or a nested
                      gitlink. Its bytes are not the entry's bytes, so it
                      cannot be proved byte-identical and is not analysed
      empty           the pin carries no `.sv`/`.v` source at all
      incomplete      a pinned source is not present in the working tree as a
                      regular file: deleted, never checked out (sparse or
                      skip-worktree), replaced by a symlink or a directory, or
                      unreadable. A symlink is refused even when its target
                      holds the pinned bytes - the pin names a file
      modified        every pinned source is present, but one of them does not
                      HASH to the blob id the pin records. Same class as
                      wrong-revision: the analysed population is not the
                      pinned one. Files that are not in the pin are ignored,
                      whatever their state - they are never analysed, and
                      local gates litter a tree with generated `.hex`
      ok              every pinned source is present and byte-identical to the
                      pin - only then are its files used

    `expected` and `actual` carry the two revisions so the refusal can name
    them; `files` is filled only for `ok`.
    """

    __slots__ = ("label", "tree", "why", "state", "expected", "actual", "files")

    def __init__(self, label, tree, why, state,
                 expected="", actual="", files=None):
        self.label = label
        self.tree = tree
        self.why = why
        self.state = state
        self.expected = expected
        self.actual = actual
        self.files = files

    @property
    def ok(self):
        return self.state == "ok"


#: What each refusable state IS, and how to get out of it. Keyed on the state
#: so a state cannot be added without a remediation, and read by the refusal
#: rather than restated at the print site.
_STATE_WHAT = {
    "unregistered": "not a registered submodule of this commit (no stage 0 "
                    "160000 gitlink in the index, or no .gitmodules entry)",
    "conflicted": "the gitlink is UNMERGED - the pin itself is in conflict, "
                  "so the index names NO revision the next commit carries",
    "absent": "registered, but nothing is checked out at the path "
              "(no directory, or an empty one)",
    "not-a-directory": "registered, but what sits at the path is NOT a "
                       "directory - a file or a symlink where the checkout "
                       "must be",
    "uninitialised": "NOT the registered checkout - the superproject has no "
                     "submodule url for it (`git submodule status` prints `-`)",
    "no-repository": "a directory that is not that repository's own top level "
                     "(an aborted `git submodule update` leaves one)",
    "wrong-revision": "checked out at the WRONG revision "
                      "(`git submodule status` prints `+`)",
    "unreadable": "at the pinned revision, but the PIN's OWN TREE cannot be "
                  "read (an object format whose blob ids this gate cannot "
                  "reproduce, or a tree record it cannot parse), so there is "
                  "no population to prove",
    "unpinnable": "at the pinned revision, but the PIN ITSELF names a source "
                  "that is not a regular file - a committed symlink or a "
                  "nested gitlink - whose bytes cannot be proved to be the "
                  "entry's bytes",
    "incomplete": "at the pinned revision, but the working tree does not hold "
                  "every pinned source AS A REGULAR FILE: deleted, never "
                  "checked out (sparse or skip-worktree), replaced by a "
                  "symlink or a directory, or unreadable",
    "modified": "at the pinned revision, but a pinned source's BYTES do not "
                "hash to the blob id the pin records, so the sources are not "
                "the pinned sources. An index hint cannot hide this: the "
                "bytes are hashed, never asked about",
    "empty": "checked out at the pinned revision, whose tree carries no "
             ".sv/.v source at all",
}

_STATE_FIX = {
    "unregistered": "nothing to initialise: {label} is not a gitlink in this "
                    "commit. Check out a commit that pins it.",
    "conflicted": "resolve the conflicted gitlink, then "
                  "`git submodule update --init {label}`",
    "absent": "git submodule update --init {label}",
    "not-a-directory": "remove the file or symlink at {label}, then "
                       "`git submodule update --init {label}`",
    "uninitialised": "git submodule update --init {label}   "
                     "(move any standalone checkout at the path aside first)",
    "no-repository": "git submodule update --init {label}",
    "wrong-revision": "git submodule update --init --checkout {label}",
    "unreadable": "git submodule update --init --force {label}; if it "
                  "persists, that checkout's object store cannot serve the "
                  "pin and must be re-cloned",
    "unpinnable": "nothing local to fix: the PIN names a source this gate "
                  "cannot prove. Bump {label} to a revision whose sources are "
                  "regular files.",
    "incomplete": "restore every pinned source, then `git submodule update "
                  "--init --force {label}`. A sparse or skip-worktree "
                  "checkout of {label} is not the pinned population: clear it "
                  "with `git -C {label} sparse-checkout disable` and "
                  "`git -C {label} update-index --no-skip-worktree <path>`",
    "modified": "commit or drop the local changes, then "
                "`git submodule update --init --force {label}`. Clear any "
                "index hint first - `git -C {label} ls-files -v` prints `h` "
                "for assume-unchanged and `S` for skip-worktree",
    "empty": "git submodule update --init --force {label}",
}


def _gitmodules_name(label, root=None):
    """The submodule NAME whose registered path is `label`, or None.

    Looked up rather than assumed equal to the path: git allows them to
    differ, and `submodule.<name>.url` - the key that decides initialised -
    is keyed on the NAME.
    """
    out = _git(["config", "-f", ".gitmodules", "--get-regexp",
                r"^submodule\..*\.path$"], root or ROOT)
    if out.returncode:
        return None
    for line in out.stdout.splitlines():
        key, _sep, value = line.partition(" ")
        if value.strip() == label and key.endswith(".path"):
            return key[len("submodule."):-len(".path")]
    return None


#: One `git ls-files --stage -z` record: mode, object, stage, path. Anchored
#: and total on purpose - a record this does not match is REFUSED rather than
#: guessed at, because a record the gate cannot read is a pin it cannot prove.
_INDEX_RECORD_RE = re.compile(r"^([0-7]{6}) ([0-9a-f]{40,64}) ([0-3])\t(.*)$",
                              re.S)


def _index_pin(label, root=None):
    """Classify the INDEX at `label`. Returns `(kind, revision, detail)`.

    `kind` is `ok`, `conflicted` or `unregistered`; `revision` is filled only
    for `ok`; `detail` is what the refusal prints as the ACTUAL state.

    THE PINNED POPULATION IS EXACTLY ONE INDEX RECORD: mode `160000`, stage
    `0`, at exactly this path. That is the only index shape in which git names
    a revision the next commit will carry, so it is the only shape accepted,
    and every other shape is refused BY CONSTRUCTION - the whole record set is
    matched against the one usable shape, never filtered down to the records
    that look usable. [R0] round 2 on PR #242 reproduced two escapes from
    filtering, both on a tree where `git submodule status` printed
    `U000...`: `160000` stage 2 beside `100644` stage 3, and a one-sided
    `160000` stage 2 with no other side. Keeping the surviving `160000` SHA
    made each read as a resolved pin, all 40 sources were enumerated, and a
    default run would have rewritten the ratchet from one side of an
    unresolved conflict.

    Every index state a submodule path can be in, and where each lands:

      no record at the path            unregistered  (tracked files UNDER the
                                                      path are counted and
                                                      named: contents
                                                      committed as ordinary
                                                      files are not a gitlink)
      one record, stage 0, `160000`    ok            <- the only pin
      one record, stage 0, other mode  unregistered  (a file or a symlink is
                                                      tracked AT the path)
      any record at stage 1, 2 or 3    conflicted    (unmerged: git's `U`)
      more than one record             conflicted
      a record this cannot parse       conflicted

    Records are matched on path EQUALITY: `git ls-files -- <dir>` also lists
    everything under a tracked directory, and a processor whose contents were
    committed as ordinary files must read as "no gitlink", never as "many
    conflict stages".

    Read with `git ls-files --stage`, which PRINTS the record. `git status`
    and `git diff` would instead compute a comparison, and a comparison is
    what an index worktree hint can silence (see _unpinned_bytes), so an
    `assume-unchanged` or `skip-worktree` bit on the gitlink path itself
    cannot change what is read here either.

    The INDEX, not HEAD, on purpose: that is what `git submodule status`
    compares a checkout against, and it is the revision the next commit will
    carry. A deliberate pin bump that is staged therefore agrees with a
    checkout moved to match it; a checkout moved on its own does not, and that
    disagreement is precisely the false green #236 closes.
    """
    out = _git(["ls-files", "--stage", "-z", "--", label], root or ROOT)
    if out.returncode:
        return ("unregistered", "",
                "`git ls-files --stage` could not read the index at the path")
    at, under = [], 0
    for entry in out.stdout.split("\0"):
        if not entry:
            continue
        m = _INDEX_RECORD_RE.match(entry)
        if m is None:
            return ("conflicted", "",
                    f"an index record this gate cannot parse: {entry!r}")
        mode, obj, stage, path = (m.group(1), m.group(2),
                                  int(m.group(3)), m.group(4))
        if path == label:
            at.append((mode, obj, stage))
        else:
            under += 1
    shown = ", ".join(f"stage {s} mode {m} {o}" for m, o, s in at)
    if len(at) > 1 or any(s for _m, _o, s in at):
        return ("conflicted", "", f"{len(at)} index record(s): {shown}")
    if not at:
        return ("unregistered", "",
                "no index record at the path"
                + (f", and {under} tracked file(s) under it" if under else ""))
    mode, obj, _stage = at[0]
    if mode != "160000":
        return ("unregistered", "",
                f"a stage 0 mode {mode} entry ({obj}) - a tracked file or "
                "symlink AT the path, not a gitlink")
    return ("ok", obj, f"stage 0 mode 160000 {obj}")


def _foreign_head(path):
    """What is actually at an unregistered path, so the refusal can name it.

    The top-level check comes FIRST because `git -C <dir>` walks UP out of a
    plain directory and would answer with the SUPERPROJECT's HEAD - the one
    revision that must never be reported as this tree's.
    """
    top = _git(["rev-parse", "--show-toplevel"], path)
    if top.returncode or \
            pathlib.Path(top.stdout.strip()).resolve() != path.resolve():
        return "a directory that is not a repository of its own"
    head = _git(["rev-parse", "HEAD"], path).stdout.strip()
    return (f"{head} in an unregistered repository at the path"
            if head else "an unregistered repository with no HEAD")


#: How a blob id is spelled, per object format, and the hash that reproduces
#: one from bytes. `git hash-object` is deliberately NOT used to reproduce it:
#: that command applies the checkout's clean filters and .gitattributes, which
#: are themselves worktree state, and a proof ABOUT worktree state must not be
#: computed through worktree state. A format not listed here is refused, never
#: guessed at.
_OBJECT_HASH = {"sha1": hashlib.sha1, "sha256": hashlib.sha256}

#: One `git ls-tree -r -z <commit>` record: mode, type, object, path. Anchored
#: and total for the same reason _INDEX_RECORD_RE is - a record this cannot
#: read is a population this gate cannot prove, so it refuses.
_TREE_RECORD_RE = re.compile(r"^([0-7]{6}) (\w+) ([0-9a-f]{40,64})\t(.*)$",
                             re.S)

#: What counts as a source, matched against the PIN's own tree. `.svh` is
#: excluded here for the same reason hdl_sources() excludes it: an include
#: header is analysed through the file that includes it.
_SOURCE_SUFFIXES = (".sv", ".v")


def _blob_id(data, algo):
    """The object id git records for exactly these bytes.

    Computed here rather than shelled out to, so that no repository
    configuration - filters, .gitattributes, core.autocrlf - can stand between
    the bytes on disk and the id they are compared against.
    """
    h = _OBJECT_HASH[algo]()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def _pinned_entries(path, pin, rel):
    """The population the PIN declares: `(entries, kind, detail)`.

    `entries` is `[(blob id, path relative to the checkout)]` sorted by path,
    or None with a refusable `kind` when the pin's own tree cannot be turned
    into a population that can be proved.

    Read from the PIN OBJECT, never from `git ls-files`: the index is worktree
    state (a `git rm --cached`, a sparse or skip-worktree entry, a conflicted
    stage) and the population must not be a function of it. What the next
    commit carries is what the pin's tree holds.
    """
    listed = _git(["ls-tree", "-r", "-z", pin, "--", rel], path)
    if listed.returncode:
        first = (listed.stderr.strip().splitlines() or ["git ls-tree failed"])[0]
        return (None, "unreadable",
                f"the pinned commit's tree could not be read: {first}")
    entries, unprovable = [], []
    for record in listed.stdout.split("\0"):
        if not record:
            continue
        m = _TREE_RECORD_RE.match(record)
        if m is None:
            return (None, "unreadable",
                    f"a tree record this gate cannot parse: {record!r}")
        mode, kind, obj, name = (m.group(1), m.group(2),
                                 m.group(3), m.group(4))
        if not name.endswith(_SOURCE_SUFFIXES):
            continue
        if kind != "blob" or mode not in ("100644", "100755"):
            unprovable.append(f"{name} (mode {mode} {kind})")
        else:
            entries.append((obj, name))
    if unprovable:
        shown = ", ".join(sorted(unprovable)[:3]) + \
            (", ..." if len(unprovable) > 3 else "")
        return (None, "unpinnable",
                f"{len(unprovable)} pinned source(s) are not regular-file "
                f"blobs: {shown}")
    return (sorted(entries, key=lambda e: e[1]), "", "")


def _unpinned_bytes(path, entries, algo):
    """`(missing, differing)` - the pinned sources this worktree does not hold.

    Every file is OPENED and HASHED. That is the whole answer to [R0] round 3:
    `git status` and `git diff --name-only HEAD --` are answers git computes
    THROUGH the index, and `git update-index --assume-unchanged` /
    `--skip-worktree` tell it not to look. Nothing here consults the index, so
    no hint - present, future, or not yet thought of - can change the verdict.

    A symlink is `missing`, not read through: the pin names a regular file,
    and a link whose target happens to hold the pinned bytes is still not that
    file. The same for a directory and for an unreadable path.

    What this is NOT: a lock. The bytes are proved once, before enumeration; a
    file rewritten between the proof and the xvlog run that opens it is a race
    with a local writer, not a state the tree can be found in, and no gate that
    hands paths to a compiler can close it.
    """
    missing, differing = [], []
    for obj, name in entries:
        fp = path / name
        if fp.is_symlink():
            missing.append(f"{name} (a symlink, not the pinned regular file)")
            continue
        try:
            if not fp.exists():
                missing.append(f"{name} (not present)")
                continue
            if not fp.is_file():
                missing.append(f"{name} (not a regular file)")
                continue
            data = fp.read_bytes()
        except OSError as exc:
            missing.append(f"{name} (unreadable: {exc.strerror})")
            continue
        if _blob_id(data, algo) != obj:
            differing.append(name)
    return missing, differing


def tree_state(label, tree, why, root=None):
    """Resolve one processor tree against the superproject's own gitlink.

    Every refusable state is decided BEFORE the tree's files are listed, so a
    tree that is not the pinned population never reaches enumeration, the
    census or the budget.
    """
    root = root or ROOT

    def state(name, expected="", actual="", files=None):
        return TreeState(label, tree, why, name, expected, actual, files)

    kind, expected, detail = _index_pin(label, root)
    if kind == "conflicted":
        return state("conflicted", "", detail)
    name = _gitmodules_name(label, root)
    if kind != "ok":
        return state("unregistered", "", detail)
    if name is None:
        return state("unregistered", expected,
                     "a stage 0 gitlink, but .gitmodules names no submodule "
                     "at this path")
    path = root / label
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        # Decided BEFORE is_dir(): a symlink to a directory answers True to
        # is_dir(), and git never checks a submodule out as one.
        return state("not-a-directory", expected,
                     "a symlink at the gitlink path, not a checkout"
                     if path.is_symlink() else
                     "a file at the gitlink path, not a checkout")
    if not path.is_dir() or not any(path.iterdir()):
        # An EMPTY directory is `absent`, not `uninitialised`: a fresh clone
        # and `git worktree add` both leave the gitlink path as an empty
        # directory, and that is the common case. Calling it "not the
        # registered checkout" would send the reader hunting for a stray
        # repository that is not there.
        return state("absent", expected)
    if _git(["config", "--get", f"submodule.{name}.url"], root).returncode:
        return state("uninitialised", expected, _foreign_head(path))
    top = _git(["rev-parse", "--show-toplevel"], path)
    if top.returncode or \
            pathlib.Path(top.stdout.strip()).resolve() != path.resolve():
        return state("no-repository", expected)
    head = _git(["rev-parse", "HEAD"], path)
    actual = head.stdout.strip() if head.returncode == 0 else ""
    if actual != expected:
        return state("wrong-revision", expected, actual or "(no HEAD)")
    # From here the population is the PIN's own tree and every file in it is
    # proved byte-identical. Nothing below asks git what changed: that answer
    # is computed through the index, and an index hint can silence it ([R0]
    # round 3). Only a tree that IS the pinned population is enumerated.
    fmt = _git(["rev-parse", "--show-object-format"], path).stdout.strip()
    if fmt not in _OBJECT_HASH:
        return state("unreadable", expected,
                     "an object format whose blob ids this gate cannot "
                     f"reproduce: {fmt or '(none reported)'}")
    rel = tree[len(label) + 1:] if tree.startswith(label + "/") else tree
    entries, kind, detail = _pinned_entries(path, expected, rel)
    if entries is None:
        return state(kind, expected, f"{actual} - {detail}")
    if not entries:
        return state("empty", expected, actual)
    missing, differing = _unpinned_bytes(path, entries, fmt)
    if missing:
        shown = ", ".join(missing[:3]) + (", ..." if len(missing) > 3 else "")
        return state("incomplete", expected,
                     f"{actual} + {len(missing)} of {len(entries)} pinned "
                     f"source(s) not held as the pinned file: {shown}")
    if differing:
        shown = ", ".join(differing[:3]) + (", ..." if len(differing) > 3 else "")
        return state("modified", expected,
                     f"{actual} + {len(differing)} of {len(entries)} pinned "
                     f"source(s) whose bytes do not hash to the pinned blob: "
                     f"{shown}")
    return state("ok", expected, actual,
                 [f"{label}/{name}" for _obj, name in entries])


def submodule_sources(label, tree):
    """Tracked design sources under one processor tree, or None if unusable.

    None means REFUSE. It is the pinned population or nothing: see TreeState
    for every state that answers None and why each one would otherwise be
    counted as "the pinned processors".
    """
    st = tree_state(label, tree, "")
    return st.files if st.ok else None


def submodule_states(states=None):
    """A TreeState per SUBMODULE_TREES entry.

    `states` overrides the resolver so the self-test can drive every arm on any
    box, with no submodule present or absent - lint_rtl.py's shape.
    """
    resolve = states or tree_state
    return [resolve(label, tree, why) for label, tree, why in SUBMODULE_TREES]


def unusable_submodule_trees(states=None):
    """Every processor tree that is not the pinned population, worst first.

    Empty means every tree in SUBMODULE_TREES is the exact revision the
    superproject pins, clean, and carries sources.
    """
    return [st for st in submodule_states(states) if not st.ok]


def source_plan():
    """(packages, modules, {section: tracked file count}) for the whole scope.

    Every package in the scope is analysed into the one work library before any
    module, hdl/ first and then each processor tree in SUBMODULE_TREES order.
    Within a tree the order is the sorted one pp_srcs.py emits, which is what
    the Yosys and Verilator consumers already build with; a cross-package
    dependency the order got wrong would surface as a package error, and the
    gate refuses to grade any module when a package will not analyse.

    Callers must have cleared unusable_submodule_trees() first: this function
    silently omits a tree that is not the pinned population, which is
    precisely the mis-report the refusal exists to prevent.
    """
    pkgs, mods = hdl_sources()
    counts = {"hdl": len(pkgs) + len(mods), "submodules": 0}
    for label, tree, _why in SUBMODULE_TREES:
        files = submodule_sources(label, tree)
        if not files:
            continue
        sub_pkgs, sub_mods = _split_packages(files)
        pkgs += sub_pkgs
        mods += sub_mods
        counts["submodules"] += len(sub_pkgs) + len(sub_mods)
    return pkgs, mods, counts


def _xvlog_cmd(xvlog, path):
    cmd = [xvlog, "-sv", "--work", "work"]
    for d in DEFINES:
        cmd += ["-d", d]
    for inc in INCLUDE_DIRS:
        cmd += ["-i", str(ROOT / inc)]
    cmd.append(str(ROOT / path))
    return cmd


def _parse(path, text):
    """Every real ERROR in one xvlog run, attributed to `path`."""
    findings = []
    for line in text.splitlines():
        if not line.startswith("ERROR"):
            continue
        if _CASCADE in line:
            continue
        code = _CODE_RE.search(line)
        ident = _IDENT_RE.search(line)
        loc = _LOC_RE.search(line)
        # The human message is the text after the [CODE] tag with the trailing
        # [file:line] bracket removed - that location is parsed out separately
        # and its absolute path has no place in a committed finding.
        msg = line.split("]", 1)[-1].strip() if "]" in line else line
        msg = _LOC_RE.sub("", msg).strip()
        findings.append(Finding(
            path=path,
            code=code.group(1) if code else "",
            identifier=ident.group(1) if ident else "",
            line=loc.group(2) if loc else "",
            message=msg,
        ))
    return findings


def _dedup(findings):
    """Collapse findings sharing a key, merging their line lists."""
    by_key = {}
    for f in findings:
        if f.key in by_key:
            by_key[f.key].merge(f)
        else:
            by_key[f.key] = f
    return sorted(by_key.values(), key=lambda x: x.key)


def analyse(xvlog, extra_modules=None, workdir=None):
    """Compile packages then every module; return (findings, package_errors).

    `extra_modules` replaces the module list (the self-test passes a planted
    file); `workdir` overrides the scratch dir. Packages always come from the
    tree, because a planted module may import one - including the processor
    packages, so a planted PROCESSOR file analyses in the same library the real
    ones do and the self-test cannot pass on a world the gate never builds.
    """
    pkgs, rest, _counts = source_plan()
    modules = rest if extra_modules is None else extra_modules
    findings, pkg_errors = [], []
    made = workdir is None
    workdir = workdir or tempfile.mkdtemp(prefix="xvlog-gate-")
    try:
        for p in pkgs:
            r = subprocess.run(_xvlog_cmd(xvlog, p), cwd=workdir,
                               capture_output=True, text=True)
            if r.returncode:
                pkg_errors += _parse(display_path(p), r.stdout + r.stderr)
        if pkg_errors:
            return findings, pkg_errors
        for m in modules:
            r = subprocess.run(_xvlog_cmd(xvlog, m), cwd=workdir,
                               capture_output=True, text=True)
            if r.returncode:
                findings += _parse(display_path(m), r.stdout + r.stderr)
    finally:
        if made:
            shutil.rmtree(workdir, ignore_errors=True)
    return _dedup(findings), pkg_errors


_BUDGET_HEADER = [
    "# GENERATED by scripts/xvlog_gate.py - the Vivado front-end ratchet: the",
    "# set of xvlog findings (path|CODE|identifier) this tree is grandfathered",
    "# to carry. A normal run REWRITES this to the current set; --check FAILS on",
    "# any finding not listed (a regression) and on any listed finding that no",
    "# longer occurs (bank the fix). Keyed on identity, not a count, so a",
    "# compensating swap cannot hide (issue #150's lesson).",
    "#",
    "# An entry is a construct Vivado's front-end REJECTS that the",
    "# Verilator/sv2v bar cannot see - use-before-declaration is the first",
    "# such class found (#132). Fixing one means changing the source, not",
    "# this file; banking the fix is a normal commit:",
    "#     scripts/xvlog_gate.py && git add scripts/xvlog.budget",
    "# An EMPTY list is the goal state, reached for the whole hdl/ tree by",
    "# #193: the gate then fails on the first NEW finding rather than on a",
    "# count, and no entry can be traded away against a fix.",
    "#",
    "# TWO SECTIONS, and a key cannot move between them (#236). The `hdl`",
    "# section is this repository's own RTL; `submodules` is the pinned",
    "# processor control plane, whose keys are spelled `<submodule>:<path>`",
    "# so that scripts/pp_srcs.py --check does not read this generated file",
    "# as a hand-written copy of the submodule source list. A section is",
    "# DERIVED from each key's path when this file is read, so grandfathering",
    "# donor debt cannot bank an hdl/ finding and vice versa, and the empty",
    "# hdl section #193 reached stays visible as its own zero.",
    "#",
    "# xvlog stops at the FIRST error in a module, so one entry can stand for",
    "# many occurrences of the same class in that file. Fixing the first one",
    "# raises the next: --check then reports one vanished and one new key, and",
    "# both are re-banked in the same deliberate commit.",
]


_LOC_COMMENT_RE = re.compile(r"\s+# line\(s\) [\d,]+\s*$")
_SECTION_RE = re.compile(r"^#\s*---\s*section (\w+):")


class BudgetError(Exception):
    """The budget file cannot be read as written - a setup error, not a finding."""


def read_budget(path=None):
    """{section: {key}} for the grandfathered findings, or None if absent.

    The trailing `  # line(s) N` note is stripped by its OWN shape, not by
    cutting at the first `#`: a key may legitimately contain that character
    (an escaped SystemVerilog identifier such as ``\\hash#in~side``), and a
    reader that cuts at it returns a key the writer never wrote, so the
    finding can be reported forever and never banked ([R0] on PR #222 found
    the `#`-prefixed discriminator case; this is the same defect's general
    form). A whole-line `#` comment is still a comment - except the section
    marker, which is a comment the reader parses.

    A key filed under a section its own path does not derive raises
    BudgetError rather than being silently re-filed. Silently re-filing is
    the trade the sections exist to stop, and accepting it would make the
    file's own section headers decorative.
    """
    path = path or BUDGET
    if not path.exists():
        return None
    sections = {name: set() for name in SECTIONS}
    # Keys before the first marker belong to `hdl`: that is the shape of every
    # budget written before #236 added sections, and those keys are hdl/ paths.
    current = SECTIONS[0]
    for line in path.read_text().splitlines():
        marker = _SECTION_RE.match(line)
        if marker:
            current = marker.group(1)
            if current not in sections:
                raise BudgetError(f"unknown section {current!r} in {path}")
            continue
        if line.lstrip().startswith("#"):
            continue
        line = _LOC_COMMENT_RE.sub("", line).strip()
        if not line:
            continue
        derived = section_of(line)
        if derived != current:
            raise BudgetError(
                f"{path}: key {line!r} is filed under section {current!r} but "
                f"its path derives {derived!r}. A key does not move between "
                "sections; fix the file rather than the finding.")
        sections[current].add(line)
    return sections


def write_budget(findings, path=None):
    """Rewrite the ratchet: one block per section, in SECTIONS order.

    No blank lines anywhere, deliberately. The previous format carried a blank
    separator that had to be suppressed for an empty list, because a trailing
    blank line at EOF is what `git diff --check` refuses and the merge bar runs
    that check; with a section per population the same conditional would have
    to be right in four combinations instead of two. A comment line before each
    block reads the same and cannot end the file wrong.
    """
    by_section = {name: [] for name in SECTIONS}
    for f in findings:
        by_section[section_of(f.key)].append(f)
    lines = list(_BUDGET_HEADER)
    for name in SECTIONS:
        entries = sorted(by_section[name], key=lambda x: x.key)
        lines.append("#")
        lines.append(f"# --- section {name}: {len(entries)} finding(s) "
                     f"({SECTION_LABEL[name]}) ---")
        for f in entries:
            loc = f"  # line(s) {','.join(f.lines)}" if f.lines else ""
            lines.append(f"{f.key}{loc}")
    (path or BUDGET).write_text("\n".join(lines) + "\n")


def _scope_lines(counts):
    """The census's coverage claim, printed EVERY run, findings or not.

    The claim and the measurement are the same sentence on purpose. Both #224
    and #236 are the same defect - a census line reading "every hdl/ module"
    over a set that excluded one tracked `.v` and every processor source - so
    the counts here are computed from the list actually analysed, and what is
    NOT analysed is named rather than left to be inferred from a green line.

    The word "pinned" is printed WITH the revision each tree resolved at. The
    run has already refused unless every one of them IS the superproject's
    gitlink, so a reader can check this line against `git submodule status`
    instead of taking it: [R0] on PR #242 printed this same sentence over an
    uninitialised standalone clone and over a wrong-revision checkout.
    """
    trees = ", ".join(tree for _label, tree, _why in SUBMODULE_TREES)
    pins = "; ".join(f"{st.label}@{st.expected[:8]}"
                     for st in submodule_states()) or "none"
    return [
        f"  analysed: {counts['hdl']} tracked .sv/.v file(s) under hdl/ and "
        f"{counts['submodules']} under the pinned processors ({trees})",
        f"  pinned at: {pins} - the superproject gitlink, which each checkout "
        "was required to BE before anything was enumerated",
        "  NOT analysed: third_party/ and external/ (leaf IP this repo neither "
        "owns nor edits), and",
        "                any defect only ELABORATION rejects - xvlog analyses; "
        "the split-initialiser",
        "                class needs xelab, which nothing in this repo runs "
        "(#224)",
    ]


def _print_census(findings, counts):
    total = len(findings)
    print(f"xvlog gate: {total} finding(s) across "
          f"{len({f.path for f in findings})} module(s)")
    for line in _scope_lines(counts):
        print(line)
    for name in SECTIONS:
        here = sorted((f for f in findings if section_of(f.key) == name),
                      key=lambda x: x.key)
        print(f"  {SECTION_LABEL[name]}: {len(here)} finding(s)")
        for f in here:
            print(f"    {f.detail()}")


def cmd_selftest(xvlog):
    """Plant a use-before-declaration into a clean module; require it to show.

    Detection cannot be proved without the tool, so this SKIPS (not passes)
    when xvlog is absent - the same honesty the gate keeps everywhere else.
    """
    problems = _selftest_logic()
    if xvlog is None:
        for p in problems:
            print(f"  SELFTEST FAILED: {p}")
        if problems:
            return 1
        print("xvlog gate selftest: parser/dedup/ratchet arms PASS; live "
              "detection arm SKIPPED (no xvlog on this box)")
        return 0
    _pkgs, rest = hdl_sources()
    donor = "hdl/ieee8021q/ts/credit_based_shaper.sv"
    if donor not in rest:
        donor = rest[0]
    # Each analyse() call builds a FRESH work library holding only the packages
    # plus the one file passed, so the donor never clashes with the real module
    # of the same name and needs no rename.
    with tempfile.TemporaryDirectory(prefix="xvlog-selftest-") as tmp:
        src = (ROOT / donor).read_text().splitlines()
        # Reference a net one line above its declaration, just before endmodule.
        idx = max(i for i, l in enumerate(src) if "endmodule" in l)
        planted = src[:idx] + [
            "  logic kl_selftest_use_w;",
            "  assign kl_selftest_use_w = kl_selftest_late_w;  // planted fault",
            "  logic kl_selftest_late_w;",
        ] + src[idx:]
        clean = pathlib.Path(tmp) / "clean.sv"
        faulted = pathlib.Path(tmp) / "faulted.sv"
        clean.write_text("\n".join(src) + "\n")
        faulted.write_text("\n".join(planted) + "\n")

        clean_f, perr = analyse(xvlog, extra_modules=[str(clean)])
        if perr:
            return _fail_setup(perr)
        if clean_f:
            problems.append(f"the unplanted donor produced findings: "
                            f"{[f.detail() for f in clean_f]}")
        bad_f, perr = analyse(xvlog, extra_modules=[str(faulted)])
        if perr:
            return _fail_setup(perr)
        hit = [f for f in bad_f
               if f.code == "VRFC 10-3380"
               and f.identifier == "kl_selftest_late_w"]
        if not hit:
            problems.append("the planted use-before-declaration produced no "
                            f"matching finding; got {[f.detail() for f in bad_f]}")

    for p in problems:
        print(f"  SELFTEST FAILED: {p}")
    if problems:
        return 1
    print("xvlog gate selftest: PASS (a planted use-before-declaration reddens "
          "the gate and names the identifier; the clean donor does not)")
    return 0


def _diff(keys, budget):
    """(new findings, vanished grandfathered findings)."""
    return sorted(keys - budget), sorted(budget - keys)


def _setup_refusal_lines(bad):
    """The refusal text for trees that are not the pinned population.

    Returned as lines rather than printed so the self-test can assert that
    every refusal names the state, the EXPECTED and ACTUAL revisions and a
    remediation - a refusal that says only "missing" sent a reader looking for
    an absent directory when the real state was a wrong revision.
    """
    lines = ["XVLOG SETUP: REFUSED - a source tree this gate analyses is not "
             "the revision this commit pins, so the finding set would not be "
             "the pinned population:"]
    for st in bad:
        lines.append(f"  {st.label}"
                     + (f"  ({st.why})" if st.why else ""))
        lines.append(f"      state:    {_STATE_WHAT[st.state]}")
        lines.append(f"      expected: {st.expected or '(no gitlink)'}"
                     "   <- the superproject gitlink for this path")
        lines.append(f"      actual:   {st.actual or '(nothing usable)'}")
        lines.append("      fix:      "
                     + _STATE_FIX[st.state].format(label=st.label))
    lines.append("  A fresh clone or `git worktree add` inherits no "
                 "submodules, and a standalone clone dropped at the path is "
                 "NOT one.")
    lines.append("  Refused rather than counted: over a tree that is not the "
                 "pinned one the gate would print a finding set the pin does "
                 "not stand behind - smaller (#186's trap) or simply "
                 "different - and a default run would then rewrite the "
                 "ratchet from it (#236).")
    return lines


def _refuse_setup(bad):
    """Print the setup refusal and return its exit code.

    Exit 2, a setup refusal, deliberately NOT the exit-1 regression path: a
    finding set measured over the wrong population proves nothing, must not
    read as a pass, and must not invite anyone to bank a ratchet from it.
    Same shape and same reasoning as scripts/lint_rtl.py's LINT SETUP refusal.
    """
    for line in _setup_refusal_lines(bad):
        print(line, file=sys.stderr)
    return 2


def _selftest_tree_state():
    """Drive tree_state() against REAL git fixtures, one per refusable state.

    The injected-state arms below prove the REFUSAL reports each state; this
    proves the CLASSIFIER reaches it, which is where [R0] on PR #242 found the
    escape - the old check asked only whether the path was the top of some
    repository with tracked sources, so a standalone clone at the gitlink path
    and a checkout moved off the pin both classified as usable. Round 2 found
    the same class in the INDEX parser: an unmerged path whose one surviving
    `160000` record was read as a resolved pin. The arms below therefore drive
    the real index through `git update-index --index-info` and check git's own
    `U` verdict beside the classifier's.

    Everything is built by hand in a temp dir: a donor repository with three
    revisions, and a superproject whose .gitmodules and INDEX gitlink are
    written directly (`git update-index --index-info`). No network, no
    `submodule add`, so no `protocol.file.allow` and no transport policy - the
    arm runs on any box, CI included, where no real submodule is checked out.
    """
    problems = []
    if not shutil.which("git"):
        return ["tree_state: no git on PATH, so the setup refusal cannot be "
                "proved against real fixtures"]
    ident = ["-c", "user.name=xvlog gate selftest",
             "-c", "user.email=selftest@example.invalid",
             "-c", "commit.gpgsign=false"]
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="xvlog-treestate-"))
    label, tree = "protocol-processor", "protocol-processor/hdl"
    try:
        donor = tmp / "donor"
        donor.mkdir()
        _git(["init", "-q", "-b", "main", "."], donor)

        def commit(msg):
            _git(["add", "-A", "."], donor)
            _git(ident + ["commit", "-q", "-m", msg], donor)
            return _git(["rev-parse", "HEAD"], donor).stdout.strip()

        (donor / "README.md").write_text("donor\n")
        rev_empty = commit("no sources yet")
        (donor / "hdl").mkdir()
        (donor / "hdl" / "a.sv").write_text("module a; endmodule\n")
        rev_one = commit("one source")
        (donor / "hdl" / "b.sv").write_text("module b; endmodule\n")
        rev_two = commit("two sources")

        super_ = tmp / "super"
        super_.mkdir()
        _git(["init", "-q", "-b", "main", "."], super_)
        (super_ / ".gitmodules").write_text(
            f'[submodule "{label}"]\n\tpath = {label}\n\turl = {donor}\n')

        def index_info(text):
            """Write raw index records - the only way to build a fixture that
            is unmerged, or mixed-mode, without a real merge conflict."""
            subprocess.run(["git", "update-index", "--index-info"],
                           cwd=str(super_), input=text,
                           capture_output=True, text=True)

        def pin(*entries):
            """Rewrite the index record(s) AT the path, clearing them first.

            An entry is `(rev, stage)` - a gitlink - or `(mode, obj, stage)`
            for the non-gitlink modes an unmerged path can carry. Several
            entries, or any nonzero stage, is what git calls unmerged.
            """
            text = f"0 {'0' * 40} 0\t{label}\n"
            for entry in entries:
                mode, obj, stage = (entry if len(entry) == 3
                                    else ("160000",) + entry)
                text += f"{mode} {obj} {stage}\t{label}\n"
            index_info(text)

        def git_agrees_unmerged(case):
            """git's own verdict on the fixture, so the arm cannot pass over a
            state git does not consider unmerged in the first place."""
            got = _git(["submodule", "status", label], super_).stdout.strip()
            if not got.startswith("U"):
                problems.append(f"tree_state [{case}]: the fixture is not "
                                f"unmerged to git either - `git submodule "
                                f"status` printed {got!r}, so the arm proves "
                                "nothing")

        def state():
            return tree_state(label, tree, "the selftest fixture", root=super_)

        #: Every state a real fixture below actually drove the classifier to.
        #: Asserted against _STATE_WHAT at the end, so a state cannot be added
        #: to the enumeration with only an injected arm behind it.
        covered = set()

        def hidden(case):
            """git's OWN answer to the question the old check asked.

            An arm that plants an index hint proves nothing unless git really
            does report the tree as clean underneath it, so both answers the
            old shape relied on are asserted empty here.
            """
            seen = _git(["diff", "--name-only", "HEAD", "--"],
                        checkout).stdout.strip()
            short = _git(["status", "--short"], checkout).stdout.strip()
            if seen or short:
                problems.append(f"tree_state [{case}]: git reported the "
                                f"change after all (diff {seen!r}, status "
                                f"{short!r}), so this fixture does not "
                                "reproduce the escape it is named for")

        def want(case, expect_state, expect_expected=None, expect_actual=None):
            st = state()
            covered.add(st.state)
            if st.state != expect_state:
                problems.append(f"tree_state [{case}]: classified "
                                f"{st.state!r}, not {expect_state!r} - the "
                                "state this fixture is in")
                return st
            if expect_expected is not None and st.expected != expect_expected:
                problems.append(f"tree_state [{case}]: expected revision "
                                f"{st.expected!r}, not the gitlink "
                                f"{expect_expected!r}")
            if expect_actual is not None and expect_actual not in st.actual:
                problems.append(f"tree_state [{case}]: actual {st.actual!r} "
                                f"does not name {expect_actual!r}")
            if expect_state != "ok" and st.files is not None:
                problems.append(f"tree_state [{case}]: a refused tree was "
                                "enumerated anyway, so the population reached "
                                "the census before the refusal")
            return st

        checkout = super_ / label
        _git(["clone", "-q", str(donor), str(checkout)], tmp)
        _git(["config", f"submodule.{label}.url", str(donor)], super_)
        pin((rev_two, "0"))

        st = want("pinned", "ok", rev_two, rev_two)
        if st.state == "ok" and st.files != [f"{tree}/a.sv", f"{tree}/b.sv"]:
            problems.append(f"tree_state [pinned]: enumerated {st.files}, not "
                            "the two tracked sources at the pin")

        # (2) the review's second escape: registered, moved off the pin. git
        # prints `+`; the old check returned nothing and the census counted it.
        _git(["checkout", "-q", "--detach", rev_one], checkout)
        want("wrong-revision", "wrong-revision", rev_two, rev_one)

        _git(["checkout", "-q", "--detach", rev_two], checkout)
        (checkout / "hdl" / "a.sv").write_text("module a; wire x; endmodule\n")
        want("modified", "modified", rev_two, "hdl/a.sv")
        _git(["checkout", "-q", "--", "hdl/a.sv"], checkout)

        # [R0] round 3: the index can be told to LIE about the worktree, and
        # the old check asked it. `assume-unchanged` and `skip-worktree` are
        # set BEFORE the file is touched, exactly as the review's fixtures
        # did, and hidden() asserts that git itself then reports nothing -
        # over a CHANGED file (the review's planted VRFC 10-3380) and over a
        # MISSING one (the sparse/skip-worktree boundary the review named).
        for flag, mark in (("assume-unchanged", "h"), ("skip-worktree", "S")):
            _git(["update-index", "--" + flag, "--", "hdl/a.sv"], checkout)
            marks = _git(["ls-files", "-v", "--", "hdl/a.sv"],
                         checkout).stdout.split()
            if not marks or marks[0] != mark:
                problems.append(f"tree_state [{flag}]: the fixture did not "
                                f"take - `git ls-files -v` printed {marks!r}, "
                                f"not the {mark!r} mark, so the arm proves "
                                "nothing")
            (checkout / "hdl" / "a.sv").write_text(
                "module a; wire hidden_w; endmodule\n")
            hidden(flag + "-modified")
            want(flag + "-modified", "modified", rev_two, "hdl/a.sv")
            (checkout / "hdl" / "a.sv").unlink()
            hidden(flag + "-missing")
            want(flag + "-missing", "incomplete", rev_two, "hdl/a.sv")
            _git(["update-index", "--no-" + flag, "--", "hdl/a.sv"], checkout)
            _git(["checkout", "-q", "--", "hdl/a.sv"], checkout)
            want(flag + "-restored", "ok", rev_two, rev_two)

        # A pinned source DELETED with no hint at all: the same class, and the
        # boundary a diff-shaped check happens to catch. Kept so the byte
        # proof is shown to cover it too.
        (checkout / "hdl" / "b.sv").unlink()
        want("pinned-source-deleted", "incomplete", rev_two, "hdl/b.sv")
        _git(["checkout", "-q", "--", "hdl/b.sv"], checkout)

        # ...and the population must not be a function of the checkout's
        # INDEX either. Dropping a record leaves the pinned bytes on disk, so
        # this is still the pinned population - an ls-files-shaped enumeration
        # would have analysed one file and called it the pinned processors.
        _git(["rm", "-q", "--cached", "--", "hdl/b.sv"], checkout)
        st = want("index-record-dropped", "ok", rev_two, rev_two)
        if st.state == "ok" and st.files != [f"{tree}/a.sv", f"{tree}/b.sv"]:
            problems.append(f"tree_state [index-record-dropped]: enumerated "
                            f"{st.files} - the population followed the index "
                            "rather than the pin")
        _git(["reset", "-q", "HEAD", "--", "hdl/b.sv"], checkout)

        # A symlink whose TARGET holds the pinned bytes is still not the
        # pinned file: reading through it makes the population a function of
        # whatever the link resolves to, which is the thing being proved.
        twin = checkout / "hdl" / "twin.sv"
        twin.write_bytes((checkout / "hdl" / "a.sv").read_bytes())
        (checkout / "hdl" / "a.sv").unlink()
        (checkout / "hdl" / "a.sv").symlink_to(twin)
        want("symlink-holding-the-pinned-bytes", "incomplete", rev_two,
             "a symlink")
        (checkout / "hdl" / "a.sv").unlink()
        twin.unlink()
        _git(["checkout", "-q", "--", "hdl/a.sv"], checkout)

        # A PIN that itself names a source which is not a regular-file blob.
        # Its recorded bytes are the link target's name, so byte-identity
        # cannot be proved for it and the gate refuses rather than analysing
        # whatever the link resolves to on this box.
        (donor / "hdl" / "c.sv").symlink_to("a.sv")
        rev_link = commit("a source committed as a symlink")
        _git(["fetch", "-q", "origin"], checkout)
        _git(["checkout", "-q", "--detach", rev_link], checkout)
        pin((rev_link, "0"))
        want("pin-names-a-symlink", "unpinnable", rev_link, "hdl/c.sv")
        _git(["checkout", "-q", "--detach", rev_two], checkout)
        pin((rev_two, "0"))
        want("pin-restored", "ok", rev_two, rev_two)

        # (1) the review's first escape: a real repository holding the pinned
        # content, at the gitlink path, that is NOT the registered checkout.
        _git(["config", "--unset", f"submodule.{label}.url"], super_)
        want("uninitialised", "uninitialised", rev_two, rev_two)
        _git(["config", f"submodule.{label}.url", str(donor)], super_)

        aside = tmp / "aside"
        checkout.rename(aside)
        checkout.mkdir()
        want("absent-empty-dir", "absent", rev_two)
        (checkout / "hdl").mkdir()
        (checkout / "hdl" / "a.sv").write_text("module a; endmodule\n")
        want("no-repository", "no-repository", rev_two)
        shutil.rmtree(checkout)
        want("absent", "absent", rev_two)

        aside.rename(checkout)
        _git(["checkout", "-q", "--detach", rev_empty], checkout)
        pin((rev_empty, "0"))
        want("empty", "empty", rev_empty)

        pin((rev_one, "1"), (rev_two, "2"), (rev_empty, "3"))
        want("conflicted", "conflicted")
        git_agrees_unmerged("conflicted")

        # [R0] round 2 on PR #242: the shapes a filter that keeps only the
        # 160000 records cannot see. Both were reproduced on the real
        # protocol-processor gitlink, and both classified `ok` at 40 files.
        # A blob object so a stage can carry a non-gitlink mode; any content
        # will do, only the mode is under test.
        blob = _git(["hash-object", "-w", str(donor / "README.md")],
                    super_).stdout.strip()
        # The checkout is put back ON the surviving stage's revision on
        # purpose: that is the reviewer's state, and it is the only one where
        # a filter's leftover SHA reads as a FALSE GREEN rather than merely as
        # the wrong refusal. Without it these arms would still pass over a
        # `wrong-revision` verdict and prove far less.
        _git(["checkout", "-q", "--detach", rev_two], checkout)

        pin((rev_two, "2"), ("100644", blob, "3"))
        st = want("conflicted-gitlink-vs-file", "conflicted")
        git_agrees_unmerged("conflicted-gitlink-vs-file")
        if st.state == "conflicted" and (rev_two not in st.actual
                                         or blob not in st.actual):
            problems.append("tree_state [conflicted-gitlink-vs-file]: the "
                            "refusal does not name both sides of the "
                            "conflict, so a reader cannot tell which is which")
        # ...and the classifier must reach the exit-2 SETUP refusal from a
        # real index fixture, not only from an injected state. Guarded on the
        # verdict: _refuse_setup only ever sees unusable states in production,
        # and handing it an `ok` one would crash the arm that is already
        # reporting the real failure.
        if not st.ok:
            buf = io.StringIO()
            with contextlib.redirect_stderr(buf):
                rc = _refuse_setup([st])
            if rc != 2 or "REFUSED" not in buf.getvalue():
                problems.append(f"tree_state [conflicted-gitlink-vs-file]: "
                                f"the refusal exited {rc} with "
                                f"{len(buf.getvalue())} byte(s) on stderr, "
                                "not 2 with a printed reason")

        pin((rev_two, "2"), ("120000", blob, "3"))
        want("conflicted-gitlink-vs-symlink", "conflicted")
        git_agrees_unmerged("conflicted-gitlink-vs-symlink")

        pin((rev_two, "2"))
        want("conflicted-one-sided", "conflicted")
        git_agrees_unmerged("conflicted-one-sided")

        # A stage 0 record that is not a gitlink at all: the path is TRACKED,
        # so `git ls-files` answers, but nothing pins a revision there.
        pin(("100644", blob, "0"))
        want("tracked-file-at-the-path", "unregistered")

        # The contents committed as ordinary files. `git ls-files -- <path>`
        # lists everything UNDER the path too, so more than one record turns
        # up here as well; calling that "many conflict stages" would refuse
        # with the wrong reason and the wrong fix. TWO of them, so an arm that
        # matched by prefix instead of by equality cannot pass this by
        # reaching the same verdict through the mode check.
        nested = [f"{label}/hdl/a.sv", f"{label}/hdl/b.sv"]
        pin()
        index_info("".join(f"100644 {blob} 0\t{n}\n" for n in nested))
        want("contents-committed-as-files", "unregistered", "",
             "2 tracked file(s) under it")
        index_info("".join(f"0 {'0' * 40} 0\t{n}\n" for n in nested))

        pin((rev_two, "0"))
        aside = tmp / "file-at-the-path"
        checkout.rename(aside)
        checkout.write_text("not a checkout\n")
        want("not-a-directory", "not-a-directory", rev_two, "a file")
        checkout.unlink()
        checkout.symlink_to(aside)
        want("symlink-at-the-path", "not-a-directory", rev_two, "a symlink")
        checkout.unlink()
        aside.rename(checkout)

        pin()
        want("unregistered", "unregistered")

        # A state in the enumeration that no REAL fixture reaches is a state
        # whose classifier arm is a promise. `unreadable` is the single
        # exclusion and it is named: git will not construct a repository
        # whose object format it cannot itself read, so that state is driven
        # only as an injected one in _selftest_logic.
        unfixtured = set(_STATE_WHAT) - covered - {"unreadable"}
        if unfixtured:
            problems.append(f"tree_state: {sorted(unfixtured)} are in the "
                            "refusal enumeration but no real git fixture "
                            "drives the classifier to them")
        if "ok" not in covered:
            problems.append("tree_state: no fixture reached `ok`, so these "
                            "arms prove only that the gate refuses")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return problems


def _selftest_logic():
    """Arms that need no xvlog: the parser, the dedup, the ratchet diff.

    These are the parts that rot silently when xvlog output or the budget
    format changes, so they run on every box, CI included, where the live
    detection arm can only skip.
    """
    problems = []
    real = ("INFO: [VRFC 10-311] analyzing module milan_csr\n"
            "ERROR: [VRFC 10-3380] identifier 'lctx_wr_p_r' is used before its "
            "declaration [/abs/hdl/common/csr/milan_csr.sv:900]\n"
            "ERROR: [VRFC 10-8530] module 'milan_csr' is ignored due to "
            "previous errors [/abs/hdl/common/csr/milan_csr.sv:85]")
    got = _parse("hdl/common/csr/milan_csr.sv", real)
    if len(got) != 1:
        problems.append(f"parse: expected 1 finding (the 10-8530 cascade "
                        f"dropped), got {len(got)}")
    else:
        f = got[0]
        if f.code != "VRFC 10-3380" or f.identifier != "lctx_wr_p_r" \
                or f.lines != ["900"]:
            problems.append(f"parse: wrong fields {f.detail()!r}")
        if "/abs/" in f.detail():
            problems.append(f"parse: absolute path leaked into the finding "
                            f"{f.detail()!r}")

    merged = _dedup([Finding("m.sv", "VRFC 10-3380", "x", "10", "m"),
                     Finding("m.sv", "VRFC 10-3380", "x", "20", "m")])
    if len(merged) != 1 or merged[0].lines != ["10", "20"]:
        problems.append(f"dedup: same key not merged with both lines: "
                        f"{[f.detail() for f in merged]}")

    new, gone = _diff({"a", "c"}, {"a", "b"})
    if new != ["c"] or gone != ["b"]:
        problems.append(f"diff: expected new=['c'] gone=['b'], "
                        f"got new={new} gone={gone}")

    # Identifier-less findings must not collapse: two DISTINCT ones in a file
    # get distinct keys (by message hash), two identical ones share a key.
    a = Finding("m.sv", "VRFC 10-2989", "", "1", "cannot resolve ALPHA")
    b = Finding("m.sv", "VRFC 10-2989", "", "2", "cannot resolve BETA")
    c = Finding("m.sv", "VRFC 10-2989", "", "9", "cannot resolve ALPHA")
    if a.key == b.key:
        problems.append("empty-identifier: distinct messages collapsed to one "
                        f"key {a.key}")
    if a.key != c.key:
        problems.append("empty-identifier: identical messages got different "
                        f"keys {a.key} vs {c.key}")
    if "#" in a.key:
        problems.append(f"empty-identifier: key {a.key} contains the budget's "
                        "comment character, so read_budget would truncate it")

    # ...and the budget must SERIALIZE and ROUND-TRIP in both its goal state
    # (empty) and populated states. A populated list has one blank separator
    # before its entries; an empty list ends at the total instead, because a
    # trailing blank line fails `git diff --check`. A key the writer emits and
    # the reader cannot parse makes the finding unbankable, which is the only
    # escape hatch --check offers once the ratchet is empty (#193).
    # The tracked ratchet is NEVER touched by this: the round-trip runs
    # against a scratch file. run_all_suites.sh runs --selftest at the start
    # of every sweep, so an arm that wrote scripts/xvlog.budget in place
    # would leave synthetic entries in a tracked file if the process were
    # killed mid-call, and SIGTERM/SIGKILL cannot be caught ([R0] on #222).
    sub_label = SUBMODULE_TREES[0][0]
    sub = Finding(f"{sub_label}:hdl/top/t.sv", "VRFC 10-3380", "late_w", "5", "m")
    scratch = pathlib.Path(tempfile.mkdtemp(prefix="xvlog-budget-")) / "b"
    try:
        for case in ([], [a], [a, b], [sub], [a, sub],
                     [a, Finding("m.sv", "VRFC 10-3380", "x", "3", "m"), sub]):
            write_budget(case, scratch)
            rendered = scratch.read_text()
            for name in SECTIONS:
                n = len([f for f in case if section_of(f.key) == name])
                if f"# --- section {name}: {n} finding(s)" not in rendered:
                    problems.append(f"budget serialization: no section header "
                                    f"for {name} with {n} finding(s)")
            if "\n\n" in rendered:
                problems.append("budget serialization: blank line in the file "
                                "- `git diff --check` refuses one at EOF and "
                                "the merge bar runs it")
            back = read_budget(scratch)
            want = {name: {f.key for f in case if section_of(f.key) == name}
                    for name in SECTIONS}
            if back != want:
                problems.append(f"budget round-trip: wrote {want}, read back "
                                f"{back}")
            for name in SECTIONS:
                new_k, gone_k = _diff(want[name], (back or {}).get(name, set()))
                if new_k or gone_k:
                    problems.append(f"budget round-trip [{name}]: --check would "
                                    f"report new={new_k} gone={gone_k} against "
                                    "its own freshly written budget")
        # a key carrying the comment character must survive too: the reader
        # strips the location note by shape, not by cutting at the first `#`
        esc = Finding("m.sv", "VRFC 10-3380", "\\hash#in~side ", "7", "m")
        if esc.key.endswith(" ") or "\n" in esc.key:
            problems.append(f"key {esc.key!r} carries trailing whitespace, "
                            "which the budget format cannot represent")
        write_budget([esc], scratch)
        if read_budget(scratch) != {"hdl": {esc.key}, "submodules": set()}:
            problems.append("budget round-trip: a key containing '#' (an "
                            "escaped identifier) did not survive the reader")
        # A key filed under the wrong section must be REFUSED, not re-filed:
        # silently re-filing it is the donor-against-hdl/ trade the sections
        # exist to stop, and would make the headers decorative.
        scratch.write_text("# --- section hdl: 1 finding(s) ---\n"
                           f"{sub.key}\n")
        try:
            read_budget(scratch)
            problems.append("budget sections: a submodule key filed under "
                            "`hdl` was accepted; a hand edit can then trade "
                            "donor debt against hdl/ debt")
        except BudgetError:
            pass
    finally:
        shutil.rmtree(scratch.parent, ignore_errors=True)

    # ---- scope arms (#224, #236) -------------------------------------------
    # These need no xvlog, so they run in CI too, where the live detection arm
    # can only skip. They are what re-narrowing the scope would break.
    if display_path(f"{sub_label}/hdl/top/t.sv") != f"{sub_label}:hdl/top/t.sv":
        problems.append("display_path: a processor source is not keyed with "
                        "its `<submodule>:` prefix, so scripts/pp_srcs.py "
                        "--check would read the budget as a hand-written copy "
                        "of the submodule source list")
    if display_path("hdl/common/x.sv") != "hdl/common/x.sv":
        problems.append("display_path: an hdl/ key changed spelling, which "
                        "would orphan every banked hdl/ entry")
    if (section_of(f"{sub_label}:hdl/top/t.sv|C|i") != "submodules"
            or section_of("hdl/common/x.sv|C|i") != "hdl"):
        problems.append("section_of: a finding lands in the wrong budget "
                        "section")

    # ---- the setup refusal, one arm per state ([R0] on PR #242) ------------
    # Injected states, so every arm runs on every box - CI included, where no
    # submodule is checked out and the live arm can only skip. The two the
    # review reproduced are `uninitialised` (a standalone clone dropped at the
    # gitlink path) and `wrong-revision` (a registered submodule moved off the
    # pin); the previous refusal returned NOTHING for both and the census
    # called them "the pinned processors". Round 2 reproduced two more, both
    # `conflicted`: an unmerged index whose one surviving `160000` record was
    # read as a resolved pin.
    _PIN = "a25b5cc9794b8e7f70f738548f4d674e9669b469"
    _OFF = "44489453cf362c7a41c9e020f4896f967dc2a4d1"

    def _fixed(state, expected=_PIN, actual="", files=None):
        return lambda label, tree, why: TreeState(label, tree, why, state,
                                                  expected, actual, files)

    refusing = {
        "absent": _fixed("absent"),
        "unregistered": _fixed("unregistered", expected="",
                               actual="no index record at the path"),
        # The round-2 escape shape: unmerged, with no stage 0 to name. The
        # refusal has no single expected revision to print, so it must print
        # the whole record set instead - that is what tells a reader which
        # side is which.
        "conflicted": _fixed("conflicted", expected="",
                             actual=f"2 index record(s): stage 2 mode 160000 "
                                    f"{_PIN}, stage 3 mode 100644 {_OFF}"),
        "not-a-directory": _fixed("not-a-directory",
                                  actual="a file at the gitlink path, not a "
                                         "checkout"),
        "uninitialised": _fixed("uninitialised",
                                actual=f"{_OFF} in an unregistered "
                                       "repository at the path"),
        "no-repository": _fixed("no-repository"),
        "wrong-revision": _fixed("wrong-revision", actual=_OFF),
        "unreadable": _fixed("unreadable",
                             actual="an object format whose blob ids this "
                                    "gate cannot reproduce: (none reported)"),
        "unpinnable": _fixed("unpinnable",
                             actual=f"{_PIN} - 1 pinned source(s) are not "
                                    "regular-file blobs: hdl/x.sv "
                                    "(mode 120000 blob)"),
        "incomplete": _fixed("incomplete",
                             actual=f"{_PIN} + 1 of 40 pinned source(s) not "
                                    "held as the pinned file: hdl/x.sv "
                                    "(not present)"),
        "modified": _fixed("modified",
                           actual=f"{_PIN} + 1 of 40 pinned source(s) whose "
                                  "bytes do not hash to the pinned blob: "
                                  "hdl/x.sv"),
        "empty": _fixed("empty", actual=_PIN),
    }
    # Exhaustive by construction: a state added to the enumeration without a
    # refusal arm fails here rather than shipping with an unproved message.
    if set(refusing) != set(_STATE_WHAT):
        problems.append(f"setup refusal: "
                        f"{sorted(set(refusing) ^ set(_STATE_WHAT))} is in one "
                        "of _STATE_WHAT / the refusal arms and not the other, "
                        "so a refusable state has no proved message")
    every_label = {label for label, _tree, _why in SUBMODULE_TREES}
    for name, resolver in refusing.items():
        bad = unusable_submodule_trees(states=resolver)
        if {st.label for st in bad} != every_label:
            problems.append(f"setup refusal [{name}]: not every processor "
                            f"tree is refused, got {sorted(st.label for st in bad)}")
            continue
        text = "\n".join(_setup_refusal_lines(bad))
        if _STATE_WHAT[name] not in text:
            problems.append(f"setup refusal [{name}]: the refusal does not "
                            "name what the state IS")
        if _STATE_FIX[name].format(label=sub_label) not in text:
            problems.append(f"setup refusal [{name}]: the refusal does not "
                            "name a remediation")
        want_actual = resolver("x", "y", "z").actual
        if want_actual and want_actual not in text:
            problems.append(f"setup refusal [{name}]: the refusal does not "
                            "name the ACTUAL revision found")
        if name not in ("unregistered",) and _PIN not in text:
            problems.append(f"setup refusal [{name}]: the refusal does not "
                            "name the EXPECTED gitlink revision")
    if unusable_submodule_trees(states=_fixed("ok", actual=_PIN,
                                              files=["hdl/x.sv"])):
        problems.append("setup refusal: a tree at the pinned revision was "
                        "refused, so the gate would refuse on every lane")
    # The refusal must exit 2, the SETUP code, not 1: exit 1 is the ratchet
    # path and reads as "the tree got worse", which invites banking a smaller
    # or different set rather than fixing the checkout.
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        rc = _refuse_setup(unusable_submodule_trees(
            states=_fixed("wrong-revision", actual=_OFF)))
    if rc != 2:
        problems.append(f"setup refusal: exited {rc}, not 2 - exit 1 is the "
                        "ratchet path and would read as a regression")
    if "REFUSED" not in buf.getvalue():
        problems.append("setup refusal: nothing was printed to stderr, so the "
                        "run would exit 2 with no reason given")

    # ...and main() itself must reach that refusal BEFORE the census, before
    # the budget is read and before it is written, in --check AND in default
    # mode. [R0] round 3 measured the escape end to end: a hidden edit was
    # analysed, printed as the pinned census, reported as an ordinary ratchet
    # regression and exited 1 - the code that reads as "the tree got worse"
    # and invites re-banking. $XVLOG is pointed at an executable that exists
    # so the tool-absence SKIP (decided first, on purpose) does not stand in
    # for the refusal; it is never run, because the refusal comes first.
    budget_before = BUDGET.read_bytes() if BUDGET.exists() else None
    saved_resolver = globals()["tree_state"]
    saved_xvlog = os.environ.get("XVLOG")
    globals()["tree_state"] = _fixed(
        "modified", actual=f"{_PIN} + 1 of 40 pinned source(s) whose bytes do "
                           "not hash to the pinned blob: hdl/x.sv")
    os.environ["XVLOG"] = sys.executable
    try:
        for extra in ([], ["--check"]):
            mode = extra[0] if extra else "default"
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), \
                    contextlib.redirect_stderr(err):
                rc = main(["xvlog_gate.py"] + extra)
            if rc != 2:
                problems.append(f"main [{mode}]: exited {rc} over a tree that "
                                "is not the pinned population, not the setup "
                                "code 2 - exit 1 is the ratchet path")
            if "REFUSED" not in err.getvalue():
                problems.append(f"main [{mode}]: printed no refusal on stderr")
            if out.getvalue().strip():
                problems.append(f"main [{mode}]: printed "
                                f"{out.getvalue().strip()[:120]!r} on stdout - "
                                "the census must not be reached over a "
                                "population the pin does not stand behind")
            after = BUDGET.read_bytes() if BUDGET.exists() else None
            if after != budget_before:
                problems.append(f"main [{mode}]: scripts/xvlog.budget changed "
                                "under a setup refusal")
    finally:
        globals()["tree_state"] = saved_resolver
        if saved_xvlog is None:
            os.environ.pop("XVLOG", None)
        else:
            os.environ["XVLOG"] = saved_xvlog

    # The byte proof's own arithmetic, checked against git rather than against
    # itself: a blob id this reproduces differently from `git hash-object` is
    # a proof that would refuse every clean tree, on both object formats git
    # offers. sha256 needs a repository of that format to ask in.
    payload = b"module a;\n  logic x;\nendmodule\n"
    hash_tmp = pathlib.Path(tempfile.mkdtemp(prefix="xvlog-blobid-"))
    try:
        for algo in sorted(_OBJECT_HASH):
            repo = hash_tmp / algo
            repo.mkdir()
            init = _git(["init", "-q", f"--object-format={algo}", "."], repo)
            if init.returncode:
                problems.append(f"blob id [{algo}]: this git cannot create a "
                                f"{algo} repository, so the arm could not run")
                continue
            got = subprocess.run(["git", "hash-object", "-t", "blob",
                                  "--stdin"], cwd=str(repo), input=payload,
                                 capture_output=True).stdout.decode().strip()
            if got != _blob_id(payload, algo):
                problems.append(f"blob id [{algo}]: computed "
                                f"{_blob_id(payload, algo)}, git says {got} - "
                                "the byte proof would refuse a clean tree")
    finally:
        shutil.rmtree(hash_tmp, ignore_errors=True)

    # ...and the CLASSIFIER those states come from, against real git fixtures.
    problems += _selftest_tree_state()

    # #224: the one tracked `.v` under hdl/ is in the analysed set. Asserted
    # against git, not against a hardcoded name, so the arm still bites when
    # another `.v` is added.
    out = _git(["ls-files", "hdl/**/*.v", "hdl/*.v"], ROOT)
    tracked_v = set(out.stdout.split()) if out.returncode == 0 else set()
    pkgs, mods = hdl_sources()
    analysed = set(pkgs) | set(mods)
    if tracked_v - analysed:
        problems.append(f"hdl scope: tracked Verilog file(s) "
                        f"{sorted(tracked_v - analysed)} are not analysed, so "
                        "the census claims more modules than it measures")
    if any(f.endswith(".svh") for f in analysed):
        problems.append("hdl scope: an include header reached the module list; "
                        "it is analysed through its includer, not alone")

    # #236: a checked-out processor tree really does contribute sources. When
    # it is absent the gate refuses, so there is nothing to assert.
    _p, plan_mods, counts = source_plan()
    for label, tree, _why in SUBMODULE_TREES:
        if submodule_sources(label, tree) is None:
            continue
        if not any(m.startswith(tree + "/") for m in _p + plan_mods):
            problems.append(f"submodule scope: {tree} is checked out but "
                            "contributes no analysed source")
    if counts["hdl"] != len(analysed):
        problems.append(f"census: the printed hdl/ count {counts['hdl']} is "
                        f"not the number of files analysed ({len(analysed)})")
    return problems


def _fail_setup(pkg_errors):
    print("xvlog gate: a package will not analyse, so no module can be graded:",
          file=sys.stderr)
    for f in pkg_errors:
        print(f"  {f.detail()}", file=sys.stderr)
    return 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="fail on a new or a vanished finding; write nothing")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the gate reddens on a planted fault")
    args = ap.parse_args(argv[1:])

    xvlog = find_xvlog()

    if args.selftest:
        return cmd_selftest(xvlog)

    # Order matters, and the docstring says why: with no tool nothing can be
    # measured, so the skip is decided BEFORE the missing-tree refusal.
    if xvlog is None:
        print("xvlog gate: SKIPPED (no Vivado xvlog found; set $XVLOG or install "
              "to /home/alex/Xilinx/2026.1). A skip is not a pass.")
        return 0

    bad = unusable_submodule_trees()
    if bad:
        return _refuse_setup(bad)

    _pkgs, _mods, counts = source_plan()
    findings, pkg_errors = analyse(xvlog)
    if pkg_errors:
        return _fail_setup(pkg_errors)
    _print_census(findings, counts)

    keys = {f.key for f in findings}
    try:
        budget = read_budget()
    except BudgetError as exc:
        print(f"xvlog gate: {exc}", file=sys.stderr)
        return 2

    if args.check:
        if budget is None:
            print("xvlog gate: no scripts/xvlog.budget to check against; run "
                  "scripts/xvlog_gate.py once to create it", file=sys.stderr)
            return 1
        rc = 0
        for name in SECTIONS:
            here = {k for k in keys if section_of(k) == name}
            new, gone = _diff(here, budget[name])
            for k in new:
                print(f"  REGRESSION [{name}]: {k} is not grandfathered in "
                      f"scripts/xvlog.budget - fix it or add it with a reason",
                      file=sys.stderr)
            for k in gone:
                print(f"  BANK IT [{name}]: {k} no longer occurs - run "
                      f"scripts/xvlog_gate.py to lower the ratchet",
                      file=sys.stderr)
            if new or gone:
                rc = 1
        if rc:
            return rc
        per = ", ".join(f"{len(budget[n])} {SECTION_LABEL[n]}" for n in SECTIONS)
        print(f"xvlog gate: PASS ({len(keys)} finding(s) == ratchet; {per})")
        return 0

    write_budget(findings)
    print(f"wrote {BUDGET.relative_to(ROOT)}: {len(findings)} grandfathered "
          f"finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
