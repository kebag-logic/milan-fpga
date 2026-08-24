#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print the source list of a top named in syn/yosys/run.sh, one path per line.

THE POINT IS THAT THERE IS NO SECOND COPY. A top's source list is the
"<top>|..." entry in syn/yosys/run.sh -- the one the portability gate proves
elaborates on every run -- and the collected `PP_SRCS` that entry references is
read from run.sh as well: its submodule half through scripts/pp_srcs.py, the
generator run.sh itself calls, and its parent half from run.sh's own
composition line. A hand-maintained duplicate in a Vivado .tcl would drift the
first time a module lands, and the drift would show up as a synthesis result
quietly missing a block. So the .tcl execs this instead.

Composing the parent half HERE was the same defect one level down, and it
shipped: a `PARENT_WRAPPERS` tuple in this file happened to agree with run.sh,
and agreement is not derivation. Two run.sh inputs differing only in their
`PP_SRCS` definition produced identical output, and deleting
hdl/milan/KL_pp_shadow.sv from run.sh left this flow green at rc=0 with an
unchanged area figure ([R0] on PR #240). The tuple is gone. `_pp_srcs()` below
parses the composition instead, and every way that parse can come back wrong is
a hard error rather than a shorter list.

Parsing a build file is what caused the earlier escape, so the parse is pinned
rather than trusted. This file lifted the assignment with `PP_SRCS="(.*?)"`
until it became a command substitution, whose inner quotes truncated the
non-greedy capture: 104 sources became 62, exit 0, no diagnostic, and Vivado
said only `module 'KL_pp_shadow' not found`. What is different now is that the
composition line is selected by the generator reference it must contain, that
exactly one line may match, that run.sh's generator call is asserted to be the
one this file makes, that a `$`-prefixed token surviving expansion is an error,
that every named file must exist, and that some emitted source must declare the
top. A truncation fails all but the first of those.

`--top` selects the entry. It defaults to `milan_datapath`, which is the only
top this file served when it was written; `KL_pp_shadow` is the second. That
script assembled its own read set instead -- the submodule half from
scripts/pp_srcs.py plus a hand-named axis_fifo.v -- and the one file the
assembly did not name was the module it passed to `synth_design -top`, so the
documented plane-area recipe read 41 sources and then failed with
`ERROR: [Synth 8-439] module 'KL_pp_shadow' not found` (Issue #235). Hence the
last check below: this file refuses to emit a list in which nothing declares
the top it was asked for, whatever the list was built from.

Used by syn/ooc/milan_datapath_ooc.tcl and syn/ooc/pp_shadow_ooc.tcl.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

#: The generator run.sh must call to derive the submodule half, and the one
#: this file calls. Named once so the two calls cannot become two generators.
GENERATOR = "scripts/pp_srcs.py"

#: How many arms selftest() must run. A deleted arm is a self-test that still
#: prints a pass, so the count is declared and checked rather than counted.
ARMS = 19


def _reader(path):
    with open(path) as fh:
        return fh.read()


def active_code(text):
    """`text` with comments, string literals and conditional regions removed.

    Comments and strings are removed in ONE pass, because they nest the wrong
    way for two passes: `//` inside a string opens no comment, and `"` inside a
    comment opens no string. What is removed is replaced by spaces, so line
    structure -- what the declaration pattern anchors on -- survives.

    Conditional-compilation regions are dropped rather than evaluated. This
    file cannot know the `+define+` set the consumer will pass, and the
    question it has to answer is whether the top is CERTAINLY in the read set;
    a declaration that depends on a define is not certainly anywhere.

    Without this, the check was a text search: an injected source whose only
    occurrence of the top was `/*` newline `module KL_pp_shadow;` newline
    `endmodule` newline `*/` satisfied it at rc=0 with five emitted files
    ([R0] on PR #240), so a semantically absent top still reached Vivado's
    `module not found`.
    """
    out, i, n = [], 0, len(text)
    while i < n:
        two = text[i:i + 2]
        if two == "//":
            j = text.find("\n", i)
            j = n if j < 0 else j
        elif two == "/*":
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
        elif text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            j = min(j + 1, n)
        else:
            out.append(text[i])
            i += 1
            continue
        out.append(re.sub(r"[^\n]", " ", text[i:j]))
        i = j

    kept, depth = [], 0
    for line in "".join(out).split("\n"):
        head = line.lstrip()
        if head.startswith(("`ifdef", "`ifndef")):
            depth += 1
            kept.append("")
        elif head.startswith("`endif"):
            depth = max(0, depth - 1)
            kept.append("")
        elif head.startswith(("`elsif", "`else")):
            kept.append("")
        else:
            kept.append("" if depth else line)
    return "\n".join(kept)


def declares(text, top):
    """True if `text` declares `module <top>` in code the front end sees."""
    return re.search(r"^[ \t]*module\s+(?:automatic\s+|static\s+)?%s\b"
                     % re.escape(top), active_code(text), re.M) is not None


def _pp_srcs(run_sh, derived):
    """run.sh's own `PP_SRCS` composition, expanded. Returns (text, problems).

    Both halves come from run.sh: `$PP_DERIVED` is replaced by what the
    generator run.sh names returned, and every other token is run.sh's, not
    this file's.
    """
    gen = re.search(r"^[ \t]*PP_DERIVED=(.*)$", run_sh, re.M)
    if not gen or GENERATOR not in gen.group(1):
        return None, ["dp_srcs: run.sh has no PP_DERIVED assignment calling %s. "
                      "This file calls it to derive the submodule half, so the "
                      "two would be deriving that half from two generators."
                      % GENERATOR]

    # Selected by the reference it must contain, not by position: run.sh also
    # assigns PP_SRCS a deliberately impossible placeholder on the `--list`
    # path, which derives nothing.
    defs = [d for d in re.findall(r'^[ \t]*PP_SRCS="([^"\n]*)"', run_sh, re.M)
            if "$PP_DERIVED" in d]
    if len(defs) != 1:
        return None, ["dp_srcs: run.sh has %d PP_SRCS definition(s) referencing "
                      "$PP_DERIVED, expected exactly 1. Guessing which one the "
                      "build uses would put the OOC read set and the Yosys one "
                      "back on two authorities." % len(defs)]
    return defs[0].replace("$PP_DERIVED", " ".join(derived)), []


def build(top, run_sh, derived, repo=REPO, exists=os.path.exists, read=_reader):
    """Expand `top`'s entry in run.sh's text. Returns (files, problems, rc).

    `run_sh`, `derived`, `exists` and `read` are the inputs, injected rather
    than read, so that `selftest()` can prove every check below bites without
    editing the repository to do it.
    """
    m = re.search(r'"%s\|(.*?)"\n' % re.escape(top), run_sh, re.S)
    if not m:
        return [], ["dp_srcs: no %s top in run.sh" % top], 2
    srcs = m.group(1)

    # The one collected list that entry references. It used to be three
    # (AECP_SRCS / LWSRP_SRCS / PP_SRCS): the first two named the 1722.1 and
    # SRP planes, which are deleted, and PP_SRCS - the protocol processor that
    # replaced them - is no longer optional, so the datapath entry expands it
    # like any other source. A name listed here that run.sh no longer defines
    # is a hard error on purpose: silently dropping it would emit a source list
    # missing a whole plane, and Vivado would only say "module not found".
    if "$PP_SRCS" not in srcs:
        return [], ["dp_srcs: the %s entry in run.sh no longer references "
                    "$PP_SRCS. Expanding it now would emit a top without its "
                    "control plane, at exit 0." % top], 2
    pp_srcs, problems = _pp_srcs(run_sh, derived)
    if problems:
        return [], problems, 2
    srcs = srcs.replace("$PP_SRCS", pp_srcs)

    env = {
        "R": repo,
        "A": os.path.join(repo, "third_party/verilog-axis/rtl"),
        "C": os.path.join(repo, "hdl/common"),
        "Q": os.path.join(repo, "hdl/ieee8021q/ts"),
        "P": os.path.join(repo, "hdl/ieee8021as/ptp_timestamp"),
        "E": os.path.join(repo, "hdl/common/eth_event_counter"),
        "D": os.path.join(repo, "hdl/ieee17221/adp"),
        "F": os.path.join(repo, "hdl/ieee8021q/filtering"),
        # the protocol-processor submodule root, as run.sh's PP_SRCS spells it
        "PP": os.path.join(repo, "protocol-processor/hdl"),
    }
    # longest key first: "$PP/" must not be eaten by the "$P" rule
    def expand(text):
        for k in sorted(env, key=len, reverse=True):
            text = text.replace("$" + k + "/", env[k] + "/")
        return text

    srcs, pp_srcs = expand(srcs), expand(pp_srcs)

    # A shell variable this file does not know is the truncation's signature:
    # the residue of a half-captured command substitution does not end in
    # .sv/.v either, so the suffix filter below would drop it in silence.
    residue = [t for t in srcs.split() if "$" in t]
    if residue:
        return [], ["dp_srcs: %d token(s) in the %s entry survived expansion "
                    "still naming a shell variable:\n  %s\nThe expansion is "
                    "incomplete, so the list below it would be short at exit 0."
                    % (len(residue), top, "\n  ".join(residue))], 2

    files = [f for f in srcs.split() if f.endswith((".sv", ".v"))]
    missing = [f for f in files if not exists(f)]
    if missing:
        return files, ["dp_srcs: missing sources:\n  " + "\n  ".join(missing)], 1

    # A SHORT LIST AT EXIT 0 IS THE FAILURE THIS FILE CAUSED ONCE ALREADY, so
    # assert what the output must contain rather than trusting the expansion.
    # The old guards could not see it: one only checked that the variable NAME
    # was present, the other only inspected tokens ending in .sv/.v, and the
    # truncation residue ended in neither. Both stayed silent while the control
    # plane vanished from the netlist.
    emitted = set(files)
    lost = [f for f in derived if f not in emitted]
    lost += [f for f in pp_srcs.split()
             if f.endswith((".sv", ".v")) and f not in emitted]
    # ...and name the plane itself, not just a count. A generator that returned
    # a truncated list would satisfy the loop above -- everything it derived
    # survived -- while emitting a top with no processor in it. This is the
    # module milan_datapath.sv and KL_pp_shadow.sv both instantiate, so its
    # absence is not a stale list, it is a netlist that cannot elaborate.
    if not any(os.path.basename(f) == "protocol_processor_top.sv" for f in files):
        lost.append("protocol_processor_top.sv (the control plane itself)")
    if lost:
        return files, ["dp_srcs: %d source(s) were derived but did not survive "
                       "expansion into the %s entry:\n  %s"
                       % (len(lost), top, "\n  ".join(lost))], 2

    # THE TOP ITSELF. Every check above compares the list against what went
    # into it, and all of them pass on a list that contains everything except
    # the one module the consumer will name as `-top`: that is Issue #235,
    # where pp_shadow_ooc.tcl read its 41 sources and Vivado answered
    # `module 'KL_pp_shadow' not found`. So compare the list against the top as
    # well, by resolving the declaration in active code rather than by matching
    # a file name -- a file named after the module is a convention, and the
    # convention is not what synthesis resolves -- and not by matching raw text
    # either, because a commented-out or `ifdef`-guarded declaration is not one.
    if not any(declares(read(f), top) for f in files):
        return files, ["dp_srcs: none of the %d source(s) in run.sh's \"%s|...\" "
                       "entry declares `module %s` in active code. Synthesis "
                       "would read every one of them and then fail with "
                       "`module '%s' not found` (Issue #235), which reads as a "
                       "missing module and is really a read set that never "
                       "contained the top."
                       % (len(files), top, top, top)], 2

    return files, [], 0


def selftest(top="faketop"):
    """Prove every check bites, on synthetic inputs, without editing the tree.

    CONTRIBUTING.md section 3 states the bar for a checker in this repository:
    it carries a self-test that runs in a gate "so the tool cannot rot into a
    green that means nothing". Every arm below drives the real `build()`, so
    stubbing it to return no problems fails this. `.github/workflows/
    rtl-fast.yml` runs it beside scripts/pp_srcs.py's.

    Planting the defect in syn/yosys/run.sh and restoring it afterwards would
    work exactly until the process is killed between the two writes, and it
    cannot run on a read-only checkout. Injecting the inputs instead exercises
    the same function and touches nothing. scripts/pp_srcs.py:selftest makes
    the same argument for the same reason.
    """
    pp = os.path.join(REPO, "protocol-processor/hdl")
    derived = [os.path.join(pp, "common/pp_pkg.sv"),
               os.path.join(pp, "top/protocol_processor_top.sv")]
    wrap_top = os.path.join(REPO, "hdl/milan/wrap_top.sv")
    wrap_two = os.path.join(REPO, "hdl/milan/wrap_two.sv")
    wrap_three = os.path.join(REPO, "hdl/milan/wrap_three.sv")
    axis = os.path.join(REPO, "third_party/verilog-axis/rtl/axis_fifo.v")

    # run.sh, reduced to the two lines this file reads: the generator call and
    # the composition. The parent half is named HERE, in the injected run.sh,
    # which is the whole point -- build() must take it from this text.
    gen_line = ('  PP_DERIVED="$(python3 "$R/%s" --prefix "$PP")" || exit 2\n'
                % GENERATOR)
    comp = '  PP_SRCS="$PP_DERIVED $R/hdl/milan/wrap_top.sv $R/hdl/milan/wrap_two.sv"\n'
    entry = '  "%s|$A/axis_fifo.v $PP_SRCS"\n' % top
    clean = gen_line + comp + entry

    # What each synthetic source contains, for the declaration check.
    text = {f: "module %s;\nendmodule\n" % os.path.basename(f)[:-3]
            for f in derived + [wrap_top, wrap_two, wrap_three, axis]}
    # The real top: declared, and also NAMED in a comment above it, so a clean
    # pass cannot be a pass on the comment.
    real = "// %s: the wrapper this entry is built around\nmodule %s #(\n) ();\nendmodule\n" % (top, top)
    text[wrap_top] = real

    state = {"derived": list(derived), "gone": set()}
    problems, ran = [], 0

    def run(world, tp=top):
        return build(tp, world, state["derived"],
                     exists=lambda f: f not in state["gone"],
                     read=lambda f: text.get(f, ""))

    def arm(name, world, want, tp=top):
        nonlocal ran
        ran += 1
        _files, bad, rc = run(world, tp)
        if not any(want in b for b in bad) or rc == 0:
            problems.append("SELF-TEST FAILED [%s]: expected a finding naming "
                            "%r at rc!=0, got rc=%d %s"
                            % (name, want, rc, bad or "no findings"))

    def decl_arm(name, body):
        """The top occurs in `body`, but not as a declaration the tool sees."""
        saved, text[wrap_top] = text[wrap_top], body
        arm(name, clean, "declares `module %s` in active code" % top)
        text[wrap_top] = saved

    # Arm 0. The clean world is clean. Without this the other arms could all be
    # passing on a check that simply reports everything.
    ran += 1
    files, bad, rc = run(clean)
    if bad or rc or len(files) != len(derived) + 3:
        problems.append("SELF-TEST FAILED [clean]: the well-formed entry must "
                        "expand clean, got rc=%d %s, %d file(s)"
                        % (rc, bad, len(files)))

    # Arm 1. run.sh's PP_SRCS IS READ, not reconstructed. Two worlds differing
    # only in that definition must differ in what comes out. This is [R0]'s
    # experiment on PR #240 -- it produced identical output then -- kept as an
    # arm, because a reintroduced parent-wrapper constant here would pass every
    # other arm in this file.
    ran += 1
    more = clean.replace(' $R/hdl/milan/wrap_two.sv"',
                         ' $R/hdl/milan/wrap_two.sv $R/hdl/milan/wrap_three.sv"')
    a_files, _, a_rc = run(clean)
    b_files, _, b_rc = run(more)
    if a_rc or b_rc or a_files == b_files or wrap_three not in b_files:
        problems.append("SELF-TEST FAILED [pp-srcs-is-read]: changing only "
                        "run.sh's PP_SRCS definition left the emitted list "
                        "unchanged (%d vs %d file(s), rc=%d/%d), so the parent "
                        "half is not being read from run.sh"
                        % (len(a_files), len(b_files), a_rc, b_rc))

    # Arm 2. [R0]'s D2 mutation on PR #240, committed: run.sh drops the wrapper
    # that declares the top. It stayed green at 16,547 LUT when this file
    # composed the parent half itself.
    arm("run-sh-drops-the-top", clean.replace("$R/hdl/milan/wrap_top.sv ", ""),
        "declares `module %s` in active code" % top)

    # Arm 3. A parent source run.sh names that is not on disk any more.
    state["gone"].add(wrap_two)
    arm("stale-parent-source", clean, "missing sources")
    state["gone"].clear()

    # Arm 4. run.sh no longer defines PP_SRCS from the derived half.
    arm("no-pp-srcs-definition", gen_line + entry, "expected exactly 1")

    # Arm 5. Two definitions: nothing here may pick one.
    arm("two-pp-srcs-definitions", gen_line + comp + comp + entry,
        "expected exactly 1")

    # Arm 6. run.sh derives the submodule half from some other generator, so
    # the two halves of "one authority" would be two again.
    arm("generator-diverged",
        '  PP_DERIVED="$(python3 "$R/scripts/other.py")"\n' + comp + entry,
        "no PP_DERIVED assignment calling")

    # Arm 7. A variable this file does not expand. The historical truncation
    # left exactly this residue and nothing saw it.
    arm("unexpanded-variable",
        gen_line + comp.replace("$R/hdl/milan/wrap_two.sv",
                                "$NEW/wrap_two.sv") + entry,
        "still naming a shell variable")

    # Arm 8. The entry is gone, or the top was misspelled by its consumer.
    arm("no-entry", clean, "no othertop top in run.sh", tp="othertop")

    # Arm 9. The entry stops referencing the collected list.
    arm("no-pp-srcs", gen_line + comp + '  "%s|$A/axis_fifo.v"\n' % top,
        "no longer references")

    # Arm 10. A derived source that does not survive the expansion, because
    # the suffix filter below the substitution drops it. That filter is what
    # made the historical truncation invisible: it inspected only tokens
    # ending in .sv/.v, and what was left of the list ended in neither.
    state["derived"] = derived + [os.path.join(pp, "acmp/ghost.svh")]
    arm("derived-source-lost", clean, "did not survive expansion")
    state["derived"] = list(derived)

    # Arm 11. The plane itself missing, which a count-based check cannot see.
    state["derived"] = [os.path.join(pp, "common/pp_pkg.sv")]
    arm("plane-lost", clean, "protocol_processor_top.sv (the control plane")
    state["derived"] = list(derived)

    # Arm 12. ISSUE #235. Every source present and correct, and not one of them
    # declares the top. Vivado's answer to this list is `module not found`.
    decl_arm("top-not-in-read-set", "module something_else;\nendmodule\n")

    # Arm 13. The same, one step subtler: the file is named after the top and
    # does not declare it, which a file-name check would pass.
    decl_arm("named-not-declared", "// %s lives here\n" % top)

    # Arms 14-18. THE DECLARATION IS TEXT, NOT CODE. [R0] on PR #240 injected
    # the block-commented form and got rc=0 with five emitted files; the rest
    # are the same class in the other spellings a real file reaches for.
    #
    # Three of these five bypass a raw-text search and are what `active_code`
    # is for: neuter it to `return text` and block-commented, inactive-
    # conditional and declaration-inside-a-string all go green. The line-
    # commented and prefix arms bind something else -- the pattern's own line
    # anchor and word boundary -- and are here because a later loosening of
    # that pattern is the obvious way to reintroduce the escape.
    decl_arm("block-commented-declaration",
             "/*\nmodule %s;\nendmodule\n*/\n" % top)
    decl_arm("inactive-conditional-declaration",
             "`ifdef SOME_DEFINE\nmodule %s;\nendmodule\n`endif\n" % top)
    decl_arm("declaration-inside-a-string",
             'localparam string S = "\nmodule %s;\n";\n' % top)
    decl_arm("line-commented-declaration",
             "// module %s;\n// endmodule\n" % top)
    decl_arm("prefix-of-the-top-declared",
             "module %s_shim;\nendmodule\n" % top)

    if ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), %s "
                        "declares %d. An arm was deleted or added without "
                        "moving the count." % (ran, __file__, ARMS))
    return problems, ran


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", default="milan_datapath",
                    help="the run.sh entry to expand (default: milan_datapath)")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each check fails on a planted defect")
    args = ap.parse_args()

    if args.selftest:
        bad, ran = selftest()
        for b in bad:
            print("  -", b, file=sys.stderr)
        if bad:
            return 2
        print("dp_srcs self-test: %d arm(s) passed" % ran)
        return 0

    with open(os.path.join(REPO, "syn", "yosys", "run.sh")) as fh:
        run_sh = fh.read()
    pp = subprocess.run(
        [sys.executable, os.path.join(REPO, *GENERATOR.split("/")),
         "--prefix", os.path.join(REPO, "protocol-processor", "hdl")],
        capture_output=True, text=True)
    if pp.returncode != 0:
        sys.stderr.write(pp.stderr)
        return 2
    files, problems, rc = build(args.top, run_sh, pp.stdout.split())
    for p in problems:
        print(p, file=sys.stderr)
    if rc:
        return rc
    print("\n".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
