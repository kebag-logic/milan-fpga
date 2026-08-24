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
    out = subprocess.run(["git", "ls-files",
                          "hdl/**/*.sv", "hdl/*.sv", "hdl/**/*.v", "hdl/*.v"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"git ls-files failed: {out.stderr.strip()}")
    files = sorted(set(out.stdout.split()))
    if not files:
        raise SystemExit("no tracked hdl/ .sv or .v files found")
    return _split_packages(files)


def _git(args, cwd):
    """One git invocation, captured. `cwd` must already be known to be a repo."""
    return subprocess.run(["git"] + args, cwd=str(cwd),
                          capture_output=True, text=True)


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
    refuses BEFORE anything is enumerated. `state` is one of, in the order
    they are decided:

      unregistered    the path is not a 160000 gitlink in the superproject
                      index, or .gitmodules does not name it
      conflicted      the gitlink is unmerged - several index stages
      absent          registered, but there is nothing at the path - no
                      directory, or the empty one a fresh clone and
                      `git worktree add` leave behind
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
      modified        HEAD is the pinned revision, tracked files under it are
                      not. Same class: the analysed population is not the
                      pinned one. Untracked files are IGNORED - `git ls-files`
                      never analyses them, and local gates litter a tree with
                      generated `.hex`
      empty           pinned and clean, but nothing tracked to analyse
      ok              the pinned population - only then are its files used

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
    "unregistered": "not a registered submodule of this commit "
                    "(no 160000 gitlink in the index, or no .gitmodules entry)",
    "conflicted": "the gitlink is UNMERGED - the pin itself is in conflict",
    "absent": "registered, but nothing is checked out at the path "
              "(no directory, or an empty one)",
    "uninitialised": "NOT the registered checkout - the superproject has no "
                     "submodule url for it (`git submodule status` prints `-`)",
    "no-repository": "a directory that is not that repository's own top level "
                     "(an aborted `git submodule update` leaves one)",
    "wrong-revision": "checked out at the WRONG revision "
                      "(`git submodule status` prints `+`)",
    "modified": "at the pinned revision with LOCAL MODIFICATIONS to tracked "
                "files, so the sources are not the pinned sources",
    "empty": "checked out at the pinned revision but carries no tracked "
             ".sv/.v source",
}

_STATE_FIX = {
    "unregistered": "nothing to initialise: {label} is not a gitlink in this "
                    "commit. Check out a commit that pins it.",
    "conflicted": "resolve the conflicted gitlink, then "
                  "`git submodule update --init {label}`",
    "absent": "git submodule update --init {label}",
    "uninitialised": "git submodule update --init {label}   "
                     "(move any standalone checkout at the path aside first)",
    "no-repository": "git submodule update --init {label}",
    "wrong-revision": "git submodule update --init --checkout {label}",
    "modified": "commit or drop the local changes, then "
                "`git submodule update --init --force {label}`",
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


def _gitlink_revisions(label, root=None):
    """Every index stage's gitlink revision at `label` (usually one, or none).

    The INDEX, not HEAD, on purpose: that is what `git submodule status`
    compares a checkout against, and it is the revision the next commit will
    carry. A deliberate pin bump that is staged therefore agrees with a
    checkout moved to match it; a checkout moved on its own does not, and that
    disagreement is precisely the false green #236 closes. More than one entry
    means an unmerged gitlink.
    """
    out = _git(["ls-files", "--stage", "--", label], root or ROOT)
    if out.returncode:
        return []
    revs = []
    for line in out.stdout.splitlines():
        parts = line.split(None, 2)
        if len(parts) >= 2 and parts[0] == "160000":
            revs.append(parts[1])
    return revs


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


def tree_state(label, tree, why, root=None):
    """Resolve one processor tree against the superproject's own gitlink.

    Every refusable state is decided BEFORE the tree's files are listed, so a
    tree that is not the pinned population never reaches enumeration, the
    census or the budget.
    """
    root = root or ROOT

    def state(name, expected="", actual="", files=None):
        return TreeState(label, tree, why, name, expected, actual, files)

    revs = _gitlink_revisions(label, root)
    if len(revs) > 1:
        return state("conflicted", " / ".join(sorted(set(revs))))
    name = _gitmodules_name(label, root)
    if not revs or name is None:
        return state("unregistered")
    expected = revs[0]
    path = root / label
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
    dirty = _git(["diff", "--name-only", "HEAD", "--"], path)
    if dirty.returncode or dirty.stdout.strip():
        names = dirty.stdout.split()
        shown = ", ".join(names[:3]) + (", ..." if len(names) > 3 else "")
        return state("modified", expected,
                     f"{actual} + {len(names)} modified tracked file(s)"
                     f"{': ' + shown if shown else ''}")
    # Only a tree that IS the pinned population is enumerated. A pin whose
    # revision carries no `tree` directory at all reads as empty, not as a
    # crash: subprocess raises on a cwd that does not exist.
    files = []
    if (root / tree).is_dir():
        listed = _git(["ls-files", "*.sv", "*.v"], root / tree)
        if listed.returncode == 0:
            files = sorted(set(listed.stdout.split()))
    if not files:
        return state("empty", expected, actual)
    return state("ok", expected, actual, [f"{tree}/{f}" for f in files])


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
    and a checkout moved off the pin both classified as usable.

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

        def pin(*entries):
            """Rewrite the index gitlink; several entries = an unmerged pin."""
            text = f"0 {'0' * 40} 0\t{label}\n"
            text += "".join(f"160000 {rev} {stage}\t{label}\n"
                            for rev, stage in entries)
            subprocess.run(["git", "update-index", "--index-info"],
                           cwd=str(super_), input=text,
                           capture_output=True, text=True)

        def state():
            return tree_state(label, tree, "the selftest fixture", root=super_)

        def want(case, expect_state, expect_expected=None, expect_actual=None):
            st = state()
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

        pin()
        want("unregistered", "unregistered")
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
    # called them "the pinned processors".
    _PIN = "a25b5cc9794b8e7f70f738548f4d674e9669b469"
    _OFF = "44489453cf362c7a41c9e020f4896f967dc2a4d1"

    def _fixed(state, expected=_PIN, actual="", files=None):
        return lambda label, tree, why: TreeState(label, tree, why, state,
                                                  expected, actual, files)

    refusing = {
        "absent": _fixed("absent"),
        "unregistered": _fixed("unregistered", expected=""),
        "conflicted": _fixed("conflicted", expected=f"{_PIN} / {_OFF}"),
        "uninitialised": _fixed("uninitialised",
                                actual=f"{_OFF} in an unregistered "
                                       "repository at the path"),
        "no-repository": _fixed("no-repository"),
        "wrong-revision": _fixed("wrong-revision", actual=_OFF),
        "modified": _fixed("modified", actual=f"{_PIN} + 1 modified "
                                              "tracked file(s): hdl/x.sv"),
        "empty": _fixed("empty", actual=_PIN),
    }
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

    # ...and the CLASSIFIER those states come from, against real git fixtures.
    problems += _selftest_tree_state()

    # #224: the one tracked `.v` under hdl/ is in the analysed set. Asserted
    # against git, not against a hardcoded name, so the arm still bites when
    # another `.v` is added.
    out = subprocess.run(["git", "ls-files", "hdl/**/*.v", "hdl/*.v"],
                         cwd=ROOT, capture_output=True, text=True)
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
