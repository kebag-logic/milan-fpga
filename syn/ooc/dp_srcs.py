#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print the source list of a top named in syn/yosys/run.sh, one path per line.

THE POINT IS THAT THERE IS NO SECOND COPY, AND NO SECOND READER. A top's source
list is the "<top>|..." entry in syn/yosys/run.sh -- the one the portability
gate proves elaborates on every run -- and this file does not read that entry.
It asks run.sh for it: `syn/yosys/run.sh --emit <top>` prints bash's own
expansion of the row the gate is about to synthesize, as `top=` / `define=` /
`incdir=` / `derived=` / `src=` lines, and everything below is that record.

Two earlier shapes of this file both failed, in the same direction, and the
second failure is why the shape changed rather than the spelling:

1. A `PARENT_WRAPPERS` tuple here happened to agree with run.sh, and agreement
   is not derivation. Deleting hdl/milan/KL_pp_shadow.sv from run.sh left this
   flow green at rc=0 with an unchanged area figure ([R0] on PR #240).
2. Parsing run.sh instead of duplicating it moved the defect one level down. A
   recogniser accepts what it has modelled, and bash accepts something else. At
   the previous head, suffixing the generator to `scripts/pp_srcs.py.broken`
   still gave rc=0 with 43 files, because the check accepted the expected path
   as a substring while run.sh would have executed a nonexistent file and taken
   its `|| exit 2`. Pointing the generator's `--prefix` at a tree that does not
   exist gave rc=0 with 43 files. Prepending the shell comment
   `# "KL_pp_shadow|$PP_SRCS"` -- which bash ignores entirely -- made the
   selector pick the comment and emit 42 files, silently dropping axis_fifo.v.
   Adding a positional `ghost.svh` gave rc=0 with 43 files, because the suffix
   filter dropped the token before the missing-source check could see it. All
   four are [R0] on PR #240, round two, and all four are arms below.

So the recogniser is gone. `ask_authority()` executes run.sh; `parse_record()`
models the whole record and refuses any line it has not modelled, because
silently filtering an input is exactly how the fourth escape worked. A mutation
of run.sh now either moves this consumer the same way it moves Yosys, or fails
both.

THE TOP MUST RESOLVE, NOT MERELY APPEAR. The other half of Issue #235 is a read
set that contains every source except the module the consumer passes to
`synth_design -top`: pp_shadow_ooc.tcl read 41 sources and Vivado answered
`ERROR: [Synth 8-439] module 'KL_pp_shadow' not found`. Checking for the text
`module <top>` is not that check. A block comment satisfied it ([R0], round
one), and after comments were stripped an unexpanded macro body still did: the
three lines `` `define UNUSED `` / `module KL_pp_shadow;` / `endmodule`, joined
by trailing backslashes, returned rc=0 with 43 files while sv2v answered
`Could not find top module KL_pp_shadow` and Yosys `Module 'KL_pp_shadow' not
found` ([R0], round two). Both answers are the preprocessor's, not the text's.
So `declares()` runs `preprocess()` -- a model of the directive layer that
consumes a `define` and everything its backslashes carry, drops conditional
regions unevaluated, and drops every other directive line -- and
`sv2v_verdict()` asks the front end the gate itself uses. Both must say yes.
Neither alone is trusted: the model runs where no front end is installed, and
the front end catches a model that has drifted from the language.

`--top` selects the entry; it defaults to `milan_datapath`.
Used by syn/ooc/milan_datapath_ooc.tcl and syn/ooc/pp_shadow_ooc.tcl.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

#: The authority, and the flag that makes it hand over one top's record. Named
#: once: a second spelling of either is a second authority.
RUN_SH = os.path.join(REPO, "syn", "yosys", "run.sh")
EMIT = "--emit"

#: Every key the record may carry. A line whose key is not here is a hard error
#: rather than a skipped line -- see escape 4 in the module docstring.
KEYS = ("top", "define", "incdir", "derived", "src")

#: What a consumer of this list can hand to `read_verilog`. A token that is not
#: one of these is not filtered out, it is refused.
SOURCE_SUFFIXES = (".sv", ".v")

#: The module that IS the control plane. Named rather than counted: a generator
#: that returned a truncated list would satisfy a count.
PLANE = "protocol_processor_top.sv"

#: The front end the mandatory Yosys gate already runs over these same source
#: lists (syn/yosys/run.sh calls `sv2v --top=<top> <inc> <srcs>`), so asking it
#: here adds no tool the gate does not already require.
FRONT_END = "sv2v"

#: Repository entries the authority resolves paths against. Only used by the
#: self-test, which runs mutated copies of run.sh from a shadow root of links.
LINKED = ("hdl", "scripts", "protocol-processor", "gptp-processor",
          "third_party", "configs", "tb")

#: How many arms selftest() must run. A deleted arm is a self-test that still
#: prints a pass, so the count is declared and checked rather than counted.
ARMS = 33


def _reader(path):
    with open(path) as fh:
        return fh.read()


# --------------------------------------------------------------------------
# the authority


def ask_authority(top, run_sh=RUN_SH, runner=subprocess.run):
    """Run `run_sh --emit <top>` and parse its record. Returns (rec, bad, rc).

    `bash` explicitly, not the executable bit: a checkout that lost the mode
    bit would otherwise turn one authority back into none.
    """
    out = runner(["bash", run_sh, EMIT, top], capture_output=True, text=True)
    if out.returncode != 0:
        err = (out.stderr or out.stdout or "").strip() or "(no diagnostic)"
        return None, ["dp_srcs: %s %s %s exited %d, so there is no read set to "
                      "emit. That script is the authority for what this top is "
                      "built from; its refusal is this flow's refusal.\n  %s"
                      % (os.path.relpath(run_sh, REPO), EMIT, top,
                         out.returncode, err.replace("\n", "\n  "))], 2
    return parse_record(out.stdout, top, run_sh)


def parse_record(text, top, run_sh=RUN_SH):
    """The `--emit` record, fully modelled. Returns (rec, problems, rc).

    NOTHING IS SKIPPED. The escape this replaces filtered every token it did
    not recognise, so a source the authority named and this file could not
    handle became invisible instead of fatal.
    """
    rec = {k: [] for k in KEYS}
    for n, line in enumerate(text.split("\n"), 1):
        if not line.strip():
            continue
        key, sep, value = line.partition("=")
        if not sep or key not in KEYS or not value:
            return None, ["dp_srcs: line %d of the %s %s record is not one of "
                          "the modelled %s lines:\n  %r\nIt is refused rather "
                          "than skipped: skipping an input the authority named "
                          "is how a source list goes short at exit 0."
                          % (n, os.path.relpath(run_sh, REPO), EMIT,
                             "/".join(KEYS), line)], 2
        rec[key].append(value)

    if rec["top"] != [top]:
        return None, ["dp_srcs: asked %s for %r and the record names %r. The "
                      "list and the module a consumer passes to -top would be "
                      "about two different entries."
                      % (EMIT, top, rec["top"])], 2
    if not rec["src"]:
        return None, ["dp_srcs: the %s record for %s names no source. An empty "
                      "read set elaborates nothing and reports no error."
                      % (EMIT, top)], 2
    return rec, [], 0


# --------------------------------------------------------------------------
# does the read set declare the top


DIRECTIVE = re.compile(r"^[ \t]*`(\w+)")


def preprocess(text):
    """`text` reduced to what the directive layer would hand the parser.

    Comments and string literals go first, in ONE pass, because they nest the
    wrong way for two: `//` inside a string opens no comment, and `"` inside a
    comment opens no string. What is removed becomes spaces, so line structure
    -- what the declaration pattern anchors on -- survives.

    Then the directive layer, line by line:

    * a `define` line, and every line a trailing backslash carries after it, is
      MACRO TEXT. It is not code until something expands the macro, and nothing
      here does. This is the escape that reopened after round one: three lines
      of unexpanded macro body read as a module declaration to any text search
      and to no front end.
    * `ifdef`/`ifndef`/`elsif`/`else`/`endif` regions are dropped rather than
      evaluated. This file cannot know the `+define+` set the consumer passes,
      and the question is whether the top is CERTAINLY in the read set.
    * every other directive line -- `include`, `timescale`, `undef`, a bare
      macro invocation -- is dropped with its continuations for the same
      reason: what it brings in is not visible from here.

    The bias is deliberate. A declaration this model cannot see is reported as
    absent even when a front end would find it; that is a refusal to emit, not
    a silent pass, and `sv2v_verdict()` below distinguishes the two cases.
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

    kept, depth, carried = [], 0, False
    for line in "".join(out).split("\n"):
        continues = line.rstrip().endswith("\\")
        if carried:
            kept.append("")
            carried = continues
            continue
        directive = DIRECTIVE.match(line)
        if directive:
            name = directive.group(1)
            if name in ("ifdef", "ifndef"):
                depth += 1
            elif name == "endif":
                depth = max(0, depth - 1)
            kept.append("")
            carried = continues
            continue
        kept.append("" if depth else line)
    return "\n".join(kept)


def declares(text, top):
    """True if `text` declares `module <top>` where the parser would see it."""
    return re.search(r"^[ \t]*module\s+(?:automatic\s+|static\s+)?%s\b"
                     % re.escape(top), preprocess(text), re.M) is not None


def sv2v_verdict(files, top, incdirs, defines,
                 which=shutil.which, runner=subprocess.run):
    """Ask the front end whether it resolves `top` in `files`.

    Returns (verdict, note): True, False, or None when the front end gave no
    top-resolution answer -- absent, or failed for some other reason. None is
    never treated as a pass; it is reported, and `--require-front-end` turns it
    into a refusal so a gate cannot lose this oracle without saying so.

    The invocation is the one syn/yosys/run.sh already makes for the same list.
    """
    exe = which(FRONT_END)
    if exe is None:
        return None, ("%s is not on PATH, so no front end confirmed the "
                      "declaration" % FRONT_END)
    argv = [exe, "--top=" + top]
    argv += ["-D" + d for d in defines]
    for d in incdirs:
        argv += ["-I", d]
    argv += list(files)
    out = runner(argv, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                 text=True)
    err = (out.stderr or "").strip()
    if out.returncode == 0:
        return True, ""
    if re.search(r"find top module\s+%s\b" % re.escape(top), err):
        return False, err.split("\n")[0]
    return None, ("%s exited %d without a top-resolution verdict: %s"
                  % (FRONT_END, out.returncode,
                     err.split("\n")[0] if err else "(no diagnostic)"))


# --------------------------------------------------------------------------
# the checks


def build(top, rec, exists=os.path.exists, read=_reader,
          front_end=sv2v_verdict, require_front_end=False):
    """Check the authority's record for `top`. Returns (files, problems, rc)."""
    files = rec["src"]

    # 1. EVERY TOKEN IS A SOURCE. The previous shape kept only tokens ending in
    # .sv/.v and dropped the rest without a word, so a positional `ghost.svh`
    # in run.sh's PP_SRCS never reached the missing-source check ([R0]).
    unaccounted = [f for f in files if not f.endswith(SOURCE_SUFFIXES)]
    if unaccounted:
        return files, ["dp_srcs: the authority named %d token(s) for %s that "
                       "are not %s sources:\n  %s\nrun.sh passes them to sv2v "
                       "and this flow would pass them to read_verilog. Dropping "
                       "them here is what made a bad entry look clean."
                       % (len(unaccounted), top, "/".join(SOURCE_SUFFIXES),
                          "\n  ".join(unaccounted))], 2

    seen, duplicate = set(), []
    for f in files:
        if f in seen:
            duplicate.append(f)
        else:
            seen.add(f)
    if duplicate:
        return files, ["dp_srcs: the %s entry names %d source(s) twice:\n  %s\n"
                       "read_verilog would redeclare their modules."
                       % (top, len(duplicate),
                          "\n  ".join(sorted(set(duplicate))))], 2

    missing = [f for f in files if not exists(f)]
    if missing:
        return files, ["dp_srcs: missing sources:\n  " + "\n  ".join(missing)], 1

    # 2. THE GENERATED HALF SURVIVES WHOLE OR NOT AT ALL. `derived=` is what
    # scripts/pp_srcs.py returned to run.sh. A top that pulls in part of it is
    # a netlist missing part of a plane, which Vivado reports as a module it
    # cannot find rather than as a list it was not given.
    kept = [f for f in rec["derived"] if f in seen]
    if kept:
        lost = [f for f in rec["derived"] if f not in seen]
        if lost:
            return files, ["dp_srcs: the %s entry takes %d of the %d generated "
                           "source(s) run.sh derived, not all of them. Missing:"
                           "\n  %s" % (top, len(kept), len(rec["derived"]),
                                       "\n  ".join(lost))], 2
        if not any(os.path.basename(f) == PLANE for f in files):
            return files, ["dp_srcs: the %s entry carries the generated half "
                           "but not %s (the control plane itself), so the "
                           "generator returned a truncated list."
                           % (top, PLANE)], 2

    # 3. THE TOP ITSELF -- ISSUE #235. Every check above compares the list
    # against what went into it, and all of them pass on a list that contains
    # everything except the one module the consumer names as `-top`. Resolve it
    # the way the toolchain does: through the directive layer, and through the
    # front end the gate runs. Both must agree, in both directions.
    modelled = any(declares(read(f), top) for f in files)
    verdict, note = front_end(files, top, rec["incdir"], rec["define"])

    if verdict is False:
        return files, ["dp_srcs: %s does not resolve `%s` in the %d source(s) "
                       "run.sh names for it:\n  %s\nSynthesis reads every one "
                       "of them and then fails with `module '%s' not found` "
                       "(Issue #235), which reads as a missing module and is "
                       "really a read set that never declared the top.%s"
                       % (FRONT_END, top, len(files), note, top,
                          "" if not modelled else
                          "\n  This file's own model DID see a declaration, so "
                          "the model is wrong about the language here and must "
                          "be fixed, not relaxed.")], 2
    if not modelled:
        return files, ["dp_srcs: none of the %d source(s) run.sh names for %s "
                       "declares `module %s` where the directive layer leaves "
                       "it: a commented, `ifdef`-guarded or unexpanded-macro "
                       "declaration is not one. Synthesis would read every "
                       "source and fail with `module '%s' not found` "
                       "(Issue #235).%s"
                       % (len(files), top, top, top,
                          ("\n  %s resolved it, so the declaration is "
                           "reachable only through expansion this file will "
                           "not perform; declare the module plainly."
                           % FRONT_END) if verdict is True else "")], 2
    if verdict is None and require_front_end:
        return files, ["dp_srcs: --require-front-end was given and no front end "
                       "confirmed `module %s`: %s. A gate that silently loses "
                       "this oracle is a gate that stops testing the escape it "
                       "was added for." % (top, note)], 2
    return files, [], 0


# --------------------------------------------------------------------------
# self-test


def _shadow(text, tmp):
    """A repository root whose syn/yosys/run.sh is `text` and whose every other
    entry links to this one.

    Lets an arm run a MUTATED REAL AUTHORITY under real bash without writing
    into the checkout. The previous shape could not do this at all: it injected
    run.sh's text into a parser, so the parser's disagreement with bash was
    invisible by construction, which is what round two of [R0] measured.
    """
    root = tempfile.mkdtemp(dir=tmp, prefix="authority-")
    os.makedirs(os.path.join(root, "syn", "yosys"))
    for name in LINKED:
        target = os.path.join(REPO, name)
        if os.path.exists(target):
            os.symlink(target, os.path.join(root, name))
    path = os.path.join(root, "syn", "yosys", "run.sh")
    with open(path, "w") as fh:
        fh.write(text)
    return root, path


def selftest(top="faketop", real_top="KL_pp_shadow"):
    """Prove every check bites. Returns (problems, arms run).

    CONTRIBUTING.md section 3 states the bar: a checker carries a self-test that
    runs in a gate "so the tool cannot rot into a green that means nothing".
    Every arm drives the real `build()`, `parse_record()` or `ask_authority()`,
    so stubbing any of them to return no problems fails this.

    Three groups. The record arms inject a synthetic record, so they need no
    tree. The declaration arms inject synthetic text and a stub front end. The
    authority arms run REAL BASH over a mutated copy of the real
    syn/yosys/run.sh from a link farm, and the last of them runs the real front
    end over the real read set: those need the protocol-processor and
    verilog-axis submodules and sv2v, and they refuse rather than skip when
    either is absent, because every escape of round two lived exactly in the gap
    between what a parser modelled and what bash and the front end do.
    """
    problems, ran = [], 0
    src = ["/r/a.sv", "/r/b.sv", "/r/" + PLANE, "/r/top.sv"]
    derived = ["/r/a.sv", "/r/" + PLANE]

    def record(**over):
        rec = {"top": [top], "define": ["SYNTHESIS"], "incdir": ["/r/inc"],
               "derived": list(derived), "src": list(src)}
        rec.update(over)
        return rec

    text = {f: "module %s;\nendmodule\n" % os.path.basename(f)[:-3] for f in src}
    # The real top: declared, and ALSO named in a comment above it, so a clean
    # pass cannot be a pass on the comment.
    text["/r/top.sv"] = ("// %s: the wrapper this entry is built around\n"
                         "module %s #(\n) ();\nendmodule\n" % (top, top))
    gone = set()

    def stub_front_end(verdict, note=""):
        return lambda *a, **k: (verdict, note)

    def run(rec, fe=None, require=False):
        return build(top, rec, exists=lambda f: f not in gone,
                     read=lambda f: text.get(f, ""),
                     front_end=fe or stub_front_end(True),
                     require_front_end=require)

    def arm(name, want, rec=None, fe=None, require=False, call=None):
        nonlocal ran
        ran += 1
        if call:
            _rec, bad, rc = call()
        else:
            _files, bad, rc = run(rec, fe, require)
        if not any(want in b for b in bad) or rc == 0:
            problems.append("SELF-TEST FAILED [%s]: expected a finding naming "
                            "%r at rc!=0, got rc=%d %s"
                            % (name, want, rc, bad or "no findings"))

    def decl_arm(name, body, fe=None, want=None):
        saved, text["/r/top.sv"] = text["/r/top.sv"], body
        arm(name, want or "declares `module %s` where the directive layer" % top,
            record(), fe)
        text["/r/top.sv"] = saved

    # ---- record arms -----------------------------------------------------
    # Arm 0. ANTI-VACUITY: the well-formed record expands clean. Without it
    # every other arm could be passing on a check that reports everything.
    ran += 1
    files, bad, rc = run(record())
    if bad or rc or files != src:
        problems.append("SELF-TEST FAILED [clean]: a well-formed record must "
                        "expand clean, got rc=%d %s, %d file(s)"
                        % (rc, bad, len(files)))

    # Arm 1. The authority refuses. Its exit status is this flow's exit status.
    class _Refused(object):
        returncode, stdout, stderr = 2, "", "planted authority refusal\n"

    arm("authority-refuses", "so there is no read set to emit",
        call=lambda: ask_authority(top, "/r/run.sh", lambda *a, **k: _Refused))

    # Arm 2. A line the record model does not know. Refused, NOT skipped: the
    # skip is how a positional ghost.svh stayed invisible ([R0] round two).
    arm("unmodelled-record-line", "is not one of the modelled",
        call=lambda: parse_record("top=%s\nsrc=/r/a.sv\nwat=1\n" % top, top))

    # Arm 3. The record answers about a different top.
    arm("record-names-another-top", "the record names",
        call=lambda: parse_record("top=other\nsrc=/r/a.sv\n", top))

    # Arm 4. A record with no source at all.
    arm("record-has-no-source", "names no source",
        call=lambda: parse_record("top=%s\n" % top, top))

    # Arm 5. A token that is not a source. This is [R0]'s ghost.svh, at the
    # level where it is decided: nothing may be filtered out.
    arm("unaccounted-token", "are not .sv/.v sources",
        record(src=src + ["/r/ghost.svh"]))

    # Arm 6. The same source twice.
    arm("duplicate-source", "twice", record(src=src + ["/r/a.sv"]))

    # Arm 7. A source the authority names and the tree does not carry.
    gone.add("/r/b.sv")
    arm("stale-source", "missing sources", record())
    gone.clear()

    # Arm 8. Part of the generated half in the entry, part not.
    arm("generated-half-split", "not all of them",
        record(derived=derived + ["/r/missing_from_entry.sv"]))

    # Arm 9. The generated half present and the plane itself not, which no
    # count-based check can see.
    arm("plane-lost", "(the control plane itself)",
        record(src=["/r/a.sv", "/r/top.sv"], derived=["/r/a.sv"]))

    # ---- declaration arms ------------------------------------------------
    # Arm 10. ISSUE #235: every source present and correct, none declares the
    # top. Vivado's answer to this list is `module not found`.
    decl_arm("top-not-in-read-set", "module something_else;\nendmodule\n")

    # Arm 11. One step subtler: the file is NAMED after the top and does not
    # declare it, which a file-name check would pass.
    decl_arm("named-not-declared", "// %s lives here\n" % top)

    # Arms 12-16. THE DECLARATION IS TEXT, NOT CODE ([R0] round one).
    decl_arm("block-commented-declaration",
             "/*\nmodule %s;\nendmodule\n*/\n" % top)
    decl_arm("inactive-conditional-declaration",
             "`ifdef SOME_DEFINE\nmodule %s;\nendmodule\n`endif\n" % top)
    decl_arm("declaration-inside-a-string",
             'localparam string S = "\nmodule %s;\n";\n' % top)
    decl_arm("line-commented-declaration",
             "// module %s;\n// endmodule\n" % top)
    decl_arm("prefix-of-the-top-declared", "module %s_shim;\nendmodule\n" % top)

    # Arms 17-19. THE DECLARATION IS TEXT, NOT PREPROCESSED CODE ([R0] round
    # two). An unexpanded macro body is not a declaration; arm 17 is the exact
    # three-line construct the reviewer drove the real `build()` with.
    decl_arm("macro-body-declaration",
             "`define UNUSED \\\nmodule %s; \\\nendmodule\n" % top)
    decl_arm("macro-body-one-line",
             "`define UNUSED module %s; endmodule\n" % top)
    decl_arm("macro-body-after-a-comment",
             "`define UNUSED /* keep */ \\\nmodule %s; \\\nendmodule\n" % top)

    # Arm 20. The front end resolves no such top and the model saw one. The
    # front end wins, and the finding says the model must be fixed.
    arm("front-end-refuses-what-the-model-saw", "does not resolve",
        record(), stub_front_end(False, "Could not find top module"))

    # Arm 21. The other direction: the front end resolves it and the model
    # cannot. Also a refusal -- an emitted list must be provable from here too.
    decl_arm("front-end-only", "module something_else;\nendmodule\n",
             stub_front_end(True),
             want="reachable only through expansion")

    # Arm 22. No front end, and a caller that said it required one.
    arm("front-end-required-and-absent", "--require-front-end was given",
        record(), stub_front_end(None, "sv2v is not on PATH"), require=True)

    # ---- authority arms --------------------------------------------------
    # These run REAL BASH over a mutated real run.sh, and the reviewer's four
    # round-two counterexamples are four of them. A tree without submodules
    # cannot answer them, and a skip here is the false green they exist to
    # close, so their absence is reported as a failure.
    if not (os.path.exists(RUN_SH) and shutil.which("bash")
            and os.path.exists(os.path.join(REPO, "protocol-processor", "hdl"))
            and os.path.exists(os.path.join(REPO, "third_party",
                                            "verilog-axis", "rtl"))):
        problems.append("SELF-TEST FAILED [authority-arms]: syn/yosys/run.sh, "
                        "bash and the protocol-processor and verilog-axis "
                        "submodules are all required. The round-two escapes "
                        "were all disagreements between a parser and bash, so "
                        "skipping these arms is skipping the finding.")
        return problems, ran
    if shutil.which(FRONT_END) is None:
        problems.append("SELF-TEST FAILED [authority-arms]: %s is not on PATH. "
                        "It is the oracle for the macro-body escape, and the "
                        "Yosys gate already requires it." % FRONT_END)
        return problems, ran

    real = _reader(RUN_SH)
    tmp = tempfile.mkdtemp(prefix="dp-srcs-selftest-")
    try:
        def relative(root, rec):
            """The record's sources as the authority's own tree spells them.
            Each arm gets its own shadow root, so absolute paths differ by
            construction and only the tree-relative set is comparable."""
            return [] if rec is None else [os.path.relpath(f, root)
                                           for f in rec["src"]]

        def authority(name, mutate, want, expect_src=None):
            nonlocal ran
            ran += 1
            root, path = _shadow(mutate(real), tmp)
            rec, bad, rc = ask_authority(real_top, path)
            if rc == 0:
                _files, bad, rc = build(real_top, rec)
            if expect_src is not None:
                if rc != 0 or relative(root, rec) != expect_src:
                    problems.append("SELF-TEST FAILED [%s]: bash ignores this "
                                    "mutation, so the read set must be "
                                    "unchanged; got rc=%d, %d source(s) %s"
                                    % (name, rc, len(relative(root, rec)), bad))
                return
            if rc == 0 or not any(want in b for b in bad):
                problems.append("SELF-TEST FAILED [%s]: expected a finding "
                                "naming %r at rc!=0, got rc=%d %s"
                                % (name, want, rc, bad or "no findings"))

        # Arm 23. ANTI-VACUITY over the REAL authority: the untouched run.sh
        # expands clean through real bash and the real front end.
        ran += 1
        base_root, base_path = _shadow(real, tmp)
        base, bad, rc = ask_authority(real_top, base_path)
        base_src = relative(base_root, base) if rc == 0 else []
        if rc == 0:
            _f, bad, rc = build(real_top, base, require_front_end=True)
        if rc or bad or len(base_src) < 2:
            problems.append("SELF-TEST FAILED [real-authority-clean]: the "
                            "untouched run.sh must expand clean, got rc=%d %s, "
                            "%d source(s)" % (rc, bad, len(base_src)))

        # Arm 24. [R0] round two, mutation 1: the generator token is suffixed.
        # The old recogniser accepted the expected path as a SUBSTRING and
        # returned rc=0 with 43 files; bash executes a nonexistent file and
        # takes run.sh's own `|| exit 2`.
        authority("generator-token-suffixed",
                  lambda t: t.replace('"$R/scripts/pp_srcs.py"',
                                      '"$R/scripts/pp_srcs.py.broken"'),
                  "so there is no read set to emit")

        # Arm 25. Mutation 2: the generator's --prefix points at a tree that
        # does not exist. The old recogniser ignored the invocation it claimed
        # to validate and ran its own; bash hands sv2v paths that are not there.
        authority("generator-prefix-diverted",
                  lambda t: t.replace('--prefix "$PP"',
                                      '--prefix "$PP/not-the-tree"'),
                  "missing sources")

        # Arm 26. Mutation 3: a valid shell COMMENT above the live row, spelt
        # so a text selector prefers it. The old recogniser emitted 42 files and
        # dropped axis_fifo.v; bash ignores the line entirely, so the correct
        # answer is the unchanged read set -- which is the property that proves
        # this consumer follows bash rather than the text.
        authority("commented-decoy-row",
                  lambda t: t.replace(
                      '  "KL_pp_shadow|$A/axis_fifo.v $PP_SRCS"\n',
                      '  # "KL_pp_shadow|$PP_SRCS"\n'
                      '  "KL_pp_shadow|$A/axis_fifo.v $PP_SRCS"\n'),
                  None, expect_src=base_src)

        # Arm 27. Mutation 4: a positional that is not a source. The old
        # recogniser filtered it out before the missing-source check.
        authority("unaccounted-positional",
                  lambda t: t.replace('PP_SRCS="$PP_DERIVED ',
                                      'PP_SRCS="$PP_DERIVED $PP/ghost.svh '),
                  "are not .sv/.v sources")

        # Arm 28. The same positional spelt as a source that is not on disk.
        authority("missing-positional",
                  lambda t: t.replace('PP_SRCS="$PP_DERIVED ',
                                      'PP_SRCS="$PP_DERIVED $PP/ghost.sv '),
                  "missing sources")

        # Arm 29. [R0] round one, mutation D2, now through real bash: run.sh
        # drops the wrapper that declares the top. It stayed green at
        # 16,547 LUT when this file composed the parent half itself.
        authority("run-sh-drops-the-top",
                  lambda t: t.replace(" $R/hdl/milan/KL_pp_shadow.sv", ""),
                  "does not resolve `%s`" % real_top)

        # Arm 30. A top no row defines. run.sh answers, this flow reports it.
        ran += 1
        _rec, bad, rc = ask_authority("othertop", _shadow(real, tmp)[1])
        if rc == 0 or not any("unknown top: othertop" in b for b in bad):
            problems.append("SELF-TEST FAILED [unknown-top]: expected the "
                            "authority's own refusal, got rc=%d %s" % (rc, bad))

        # Arm 31. THE ROUND-TWO BLOCKER, END TO END. The real read set, with the
        # file that declares the top replaced on disk by the reviewer's exact
        # unexpanded macro body, driven through real bash and the REAL front
        # end. `sv2v --top` answers `Could not find top module`; so must this.
        ran += 1
        shadow_src = os.path.join(tmp, "KL_pp_shadow.sv")
        with open(shadow_src, "w") as fh:
            fh.write("`define UNUSED \\\nmodule %s; \\\nendmodule\n" % real_top)
        macro_root, macro_path = _shadow(
            real.replace("$R/hdl/milan/KL_pp_shadow.sv", shadow_src), tmp)
        rec, bad, rc = ask_authority(real_top, macro_path)
        if rc == 0:
            _f, bad, rc = build(real_top, rec, require_front_end=True)
        if rc == 0 or not any("does not resolve" in b for b in bad):
            problems.append("SELF-TEST FAILED [macro-body-real-front-end]: the "
                            "real read set with an unexpanded macro body in "
                            "place of the top must be refused by %s; got rc=%d "
                            "%s" % (FRONT_END, rc, bad))
        if len(relative(macro_root, rec)) != len(base_src):
            problems.append("SELF-TEST FAILED [macro-body-real-front-end]: the "
                            "mutation must change only the top's TEXT, and it "
                            "changed the read set (%d vs %d source(s))"
                            % (len(relative(macro_root, rec)), len(base_src)))

        # Arm 32. THE SAME SET WITH NO FRONT END AT ALL. A Vivado host need not
        # carry sv2v, so the directive-layer model has to close this escape on
        # its own; this arm is what stops a later change from leaning on the
        # oracle and leaving that host with the round-two behaviour.
        ran += 1
        rec, bad, rc = ask_authority(real_top, macro_path)
        if rc == 0:
            _f, bad, rc = build(real_top, rec,
                                front_end=lambda *a, **k: (None, "no front end"))
        want = "declares `module %s` where the directive layer" % real_top
        if rc == 0 or not any(want in b for b in bad):
            problems.append("SELF-TEST FAILED [macro-body-model-alone]: with no "
                            "front end the model must still refuse the macro "
                            "body; got rc=%d %s" % (rc, bad))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), %s "
                        "declares %d. An arm was deleted or added without "
                        "moving the count." % (ran, __file__, ARMS))
    return problems, ran


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", default="milan_datapath",
                    help="the run.sh entry to expand (default: milan_datapath)")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each check fails on a planted defect")
    ap.add_argument("--require-front-end", action="store_true",
                    help="refuse unless %s confirms the top resolves"
                         % FRONT_END)
    args = ap.parse_args()

    if args.selftest:
        bad, ran = selftest()
        for b in bad:
            print("  -", b, file=sys.stderr)
        if bad:
            return 2
        print("dp_srcs self-test: %d arm(s) passed" % ran)
        return 0

    files, problems, rc = [], [], 0
    rec, problems, rc = ask_authority(args.top)
    if rc == 0:
        files, problems, rc = build(args.top, rec,
                                    require_front_end=args.require_front_end)
    for p in problems:
        print(p, file=sys.stderr)
    if rc:
        return rc
    print("\n".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
