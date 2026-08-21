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

TOOL ABSENCE IS A SKIP, NEVER A FALSE GREEN. With no xvlog on the box (CI has
none) the gate prints a visible SKIP marker and exits 0, the tsn-gen precedent.
It reads only hdl/ and include dirs under hdl/, so an uninitialised submodule
cannot make the tree look cleaner than it is (the #186 trap): the finding set
does not depend on submodule checkout.

THE RATCHET keys on the finding IDENTITY `path|CODE|identifier`, not on a count.
A count ratchet cannot see a compensating swap - one finding fixed while another
appears in the same commit nets to zero (the lesson of #150). An identity set
fails on any NEW finding AND on any grandfathered finding that has silently
vanished (bank the improvement deliberately), so neither direction is silent.
Today's backlog is grandfathered in scripts/xvlog.budget and printed in full;
the underlying defects are their own ticket, not this gate's to fix.

    scripts/xvlog_gate.py            # analyse, print the census, LOWER the ratchet
    scripts/xvlog_gate.py --check    # gate: fail on a NEW or a vanished finding
    scripts/xvlog_gate.py --selftest # prove the gate reddens on a planted fault

Exit 0 = at the ratchet (or skipped), 1 = regression / vanished finding / a
package that will not analyse, 2 = usage or setup error.
"""

import argparse
import hashlib
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
        ident = self.identifier or (
            "#" + hashlib.sha1(self.message.encode("utf-8",
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


def hdl_sources():
    """Tracked hdl/ SystemVerilog, packages first then the rest, both sorted.

    Tracked only (git ls-files): analysing an untracked stray .sv is a build no
    other checkout can reproduce - the same rule pp_srcs.py keeps.
    """
    out = subprocess.run(["git", "ls-files", "hdl/**/*.sv", "hdl/*.sv"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"git ls-files failed: {out.stderr.strip()}")
    files = sorted(out.stdout.split())
    if not files:
        raise SystemExit("no tracked hdl/*.sv files found")
    pkgs = [f for f in files if _PACKAGE_RE.search((ROOT / f).read_text())]
    rest = [f for f in files if f not in set(pkgs)]
    return pkgs, rest


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
    tree, because a planted module may import one.
    """
    pkgs, rest = hdl_sources()
    modules = rest if extra_modules is None else extra_modules
    findings, pkg_errors = [], []
    made = workdir is None
    workdir = workdir or tempfile.mkdtemp(prefix="xvlog-gate-")
    try:
        for p in pkgs:
            r = subprocess.run(_xvlog_cmd(xvlog, p), cwd=workdir,
                               capture_output=True, text=True)
            if r.returncode:
                pkg_errors += _parse(p, r.stdout + r.stderr)
        if pkg_errors:
            return findings, pkg_errors
        for m in modules:
            r = subprocess.run(_xvlog_cmd(xvlog, m), cwd=workdir,
                               capture_output=True, text=True)
            if r.returncode:
                findings += _parse(m, r.stdout + r.stderr)
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
    "# These are use-before-declaration defects real on dev and invisible to the",
    "# Verilator/sv2v bar; fixing them (moving each declaration above first use)",
    "# is issue #193, not this gate's lane. Lowering an entry is a normal commit:",
    "#     scripts/xvlog_gate.py && git add scripts/xvlog.budget",
]


def read_budget():
    """The grandfathered finding keys, or None if the file is absent."""
    if not BUDGET.exists():
        return None
    keys = set()
    for line in BUDGET.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            keys.add(line)
    return keys


def write_budget(findings):
    lines = list(_BUDGET_HEADER)
    lines.append(f"#\n# total {len(findings)} finding(s)")
    lines.append("")
    for f in sorted(findings, key=lambda x: x.key):
        loc = f"  # line(s) {','.join(f.lines)}" if f.lines else ""
        lines.append(f"{f.key}{loc}")
    BUDGET.write_text("\n".join(lines) + "\n")


def _print_census(findings):
    if not findings:
        print("xvlog gate: 0 findings - every hdl/ module analyses under "
              "Vivado's front-end")
        return
    print(f"xvlog gate: {len(findings)} finding(s) across "
          f"{len({f.path for f in findings})} module(s):")
    for f in sorted(findings, key=lambda x: x.key):
        print(f"  {f.detail()}")


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

    if xvlog is None:
        print("xvlog gate: SKIPPED (no Vivado xvlog found; set $XVLOG or install "
              "to /home/alex/Xilinx/2026.1). A skip is not a pass.")
        return 0

    findings, pkg_errors = analyse(xvlog)
    if pkg_errors:
        return _fail_setup(pkg_errors)
    _print_census(findings)

    keys = {f.key for f in findings}
    budget = read_budget()

    if args.check:
        if budget is None:
            print("xvlog gate: no scripts/xvlog.budget to check against; run "
                  "scripts/xvlog_gate.py once to create it", file=sys.stderr)
            return 1
        new, gone = _diff(keys, budget)
        for k in new:
            print(f"  REGRESSION: {k} is not grandfathered in scripts/"
                  f"xvlog.budget - fix it or add it with a reason", file=sys.stderr)
        for k in gone:
            print(f"  BANK IT: {k} no longer occurs - run scripts/xvlog_gate.py "
                  f"to lower the ratchet", file=sys.stderr)
        if new or gone:
            return 1
        print(f"xvlog gate: PASS ({len(keys)} finding(s) == ratchet)")
        return 0

    write_budget(findings)
    print(f"wrote {BUDGET.relative_to(ROOT)}: {len(findings)} grandfathered "
          f"finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
