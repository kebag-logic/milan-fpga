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

THE TOP MUST RESOLVE, NOT MERELY APPEAR, AND ONLY A FRONT END SAYS SO. The other
half of Issue #235 is a read set that contains every source except the module
the consumer passes to `synth_design -top`: pp_shadow_ooc.tcl read 41 sources
and Vivado answered `ERROR: [Synth 8-439] module 'KL_pp_shadow' not found`.
Whether a `module` keyword is code is decided by the directive layer, and three
successive MODELS of that layer were each accepted here and then broken, all in
the same direction, all by [R0] on PR #240:

1. round one -- a text search for `module <top>`. A block comment satisfied it.
2. round two -- comments and strings stripped first. An unexpanded macro body
   still satisfied it: `` `define UNUSED `` / `module KL_pp_shadow;` /
   `endmodule`, joined by trailing backslashes, returned rc=0 while sv2v
   answered `Could not find top module KL_pp_shadow` and Yosys `Module
   'KL_pp_shadow' not found`.
3. round three -- `define` bodies consumed and directive lines dropped. A
   multiline macro INVOCATION still satisfied it: `` `define DISCARD(x) ``,
   then `` `DISCARD( `` / the declaration / `)`. The model dropped the
   invocation line and read its ARGUMENT text as code; sv2v again answered
   `Could not find top module KL_pp_shadow`.

Three rounds, three spellings, one question: which of these `module` keywords
survives macro expansion. Answering that completely is a preprocessor, and a
preprocessor is the front end -- so the model is GONE rather than patched a
fourth time. `sv2v_verdict()`, the front end syn/yosys/run.sh already runs over
these same lists, is now the ONLY answerer. No front end therefore means no
answer, and no answer is a refusal: there is no mode in which this file
approximates top resolution, because an approximation that disagrees with the
toolchain is exactly what all three rounds measured. That costs no new tool --
`sv2v` is already required by syn/yosys/run.sh, the authority that defines this
read set, and listed in README.md's tool table.

`--top` selects the entry; it defaults to `milan_datapath`.
Used by syn/ooc/milan_datapath_ooc.tcl and syn/ooc/pp_shadow_ooc.tcl.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

#: The authority, and the flag that makes it hand over one top's record. Named
#: once: a second spelling of either is a second authority.
RUN_SH = REPO / "syn" / "yosys" / "run.sh"
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
ARMS = 35

#: One `--emit` record: the authority's own values, one list per modelled key.
#:
#: THE VALUES ARE STRINGS AND STAY STRINGS. Every path this file OWNS is a
#: `Path` -- REPO, RUN_SH, the self-test's shadow roots -- but a record value is
#: not this file's path, it is the authority's own token, printed back verbatim
#: on stdout and handed to `sv2v` and to `read_verilog` exactly as bash spelled
#: it. `Path` would normalise it (`./x.sv` and `a//b.sv` are what bash emits and
#: not what a Path prints), and the checks below ask a source token whether it
#: `endswith` a suffix, which a Path cannot answer. The conversion happens where
#: a token is USED as a path -- `_on_disk()`, `_under()` -- and nowhere else.
Record = dict[str, list[str]]

#: What ask_authority() and parse_record() answer: (record, problems, exit
#: status). The record is None exactly when the problems are fatal.
Answer = tuple[Record | None, list[str], int]

#: What build() answers: (sources, problems, exit status).
Expansion = tuple[list[str], list[str], int]

#: What a front end answers: (does the top resolve, diagnostic). None is "no
#: verdict at all", which is a refusal here and not a weaker pass.
Verdict = tuple[bool | None, str]


def _on_disk(token: str) -> bool:
    """Does the authority's source token name a file that is there?"""
    return Path(token).exists()


def _named(path: Path | str) -> str:
    """How a finding spells `path`: repo-relative when it is under the repo.

    `Path.relative_to` refuses a path outside its argument where the old
    `os.path.relpath` answered with a chain of `..`, so the outside case
    answers with the path itself -- the self-test drives this file from
    shadow roots in /tmp, and `../../../tmp/authority-xxxx/...` named nothing
    a reader could act on anyway.

    `str` is accepted as well as `Path` because this only ever runs on the
    REFUSAL path: `ask_authority()`'s `run_sh` is a `Path` now, and a caller
    still passing the old spelling must get that caller's diagnostic and not
    an `AttributeError` raised while producing it.
    """
    try:
        return str(Path(path).relative_to(REPO))
    except ValueError:
        return str(path)


def _under(root: Path, token: str) -> str:
    """The authority's source token as `root`'s own tree spells it.

    Same refusal, same answer: arms 32-34 point run.sh at a file OUTSIDE the
    shadow root on purpose, and those arms compare how MANY sources came back,
    so an unrelatable one keeps its own spelling instead of raising.
    """
    try:
        return str(Path(token).relative_to(root))
    except ValueError:
        return token


# --------------------------------------------------------------------------
# the authority


def ask_authority(top: str, run_sh: Path = RUN_SH,
                  runner: Callable[..., object] = subprocess.run) -> Answer:
    """Run `run_sh --emit <top>` and parse its record. Returns (rec, bad, rc).

    `bash` explicitly, not the executable bit: a checkout that lost the mode
    bit would otherwise turn one authority back into none.

    `runner` need only answer like `subprocess.run` - `returncode`, `stdout`,
    `stderr` - which is how the self-test plants a refusal without a shell.
    """
    out = runner(["bash", str(run_sh), EMIT, top], capture_output=True,
                 text=True)
    if out.returncode != 0:
        err = (out.stderr or out.stdout or "").strip() or "(no diagnostic)"
        return None, ["dp_srcs: %s %s %s exited %d, so there is no read set to "
                      "emit. That script is the authority for what this top is "
                      "built from; its refusal is this flow's refusal.\n  %s"
                      % (_named(run_sh), EMIT, top,
                         out.returncode, err.replace("\n", "\n  "))], 2
    return parse_record(out.stdout, top, run_sh)


def parse_record(text: str, top: str, run_sh: Path = RUN_SH) -> Answer:
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
                          % (n, _named(run_sh), EMIT,
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
# does the read set declare the top -- asked of the front end, of nothing else


def sv2v_verdict(files: list[str], top: str, incdirs: list[str], defines: list[str],
                 which: Callable[[str], str | None] = shutil.which,
                 runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> Verdict:
    """Ask the front end whether it resolves `top` in `files`.

    Returns (verdict, note): True, False, or None when the front end gave no
    top-resolution answer -- absent, or failed for some other reason. None is
    not a weaker pass, and there is no flag that makes it one: `build()` refuses
    on it. The alternative is this file answering from its own model of the
    language, and that is the escape of all three [R0] rounds.

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


def build(top: str, rec: Record, exists: Callable[[str], bool] = _on_disk,
          front_end: Callable[..., Verdict] = sv2v_verdict) -> Expansion:
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
        if not any(Path(f).name == PLANE for f in files):
            return files, ["dp_srcs: the %s entry carries the generated half "
                           "but not %s (the control plane itself), so the "
                           "generator returned a truncated list."
                           % (top, PLANE)], 2

    # 3. THE TOP ITSELF -- ISSUE #235. Every check above compares the list
    # against what went into it, and all of them pass on a list that contains
    # everything except the one module the consumer names as `-top`. Only the
    # front end answers this. Whether a `module` keyword is code is a question
    # about macro expansion, three models of the directive layer were each
    # broken here by a construct they did not model (module docstring), and a
    # fourth model would be a fourth round -- so no front end is a REFUSAL, not
    # a quietly weaker check, and this file has no tool-absent mode at all.
    verdict, note = front_end(files, top, rec["incdir"], rec["define"])

    if verdict is None:
        return files, ["dp_srcs: no front end resolved `module %s` in the %d "
                       "source(s) run.sh names for %s: %s. This flow does not "
                       "answer that question itself: three text/directive "
                       "models of it were each accepted and then broken by a "
                       "construct they did not model ([R0] on PR #240, rounds "
                       "one to three), so an unanswered question is a refusal "
                       "and not an emission. Install %s -- README.md's tool "
                       "table has it, and syn/yosys/run.sh, which owns this "
                       "read set, already requires it."
                       % (top, len(files), top, note, FRONT_END)], 2
    if verdict is False:
        return files, ["dp_srcs: %s does not resolve `%s` in the %d source(s) "
                       "run.sh names for it:\n  %s\nSynthesis reads every one "
                       "of them and then fails with `module '%s' not found` "
                       "(Issue #235), which reads as a missing module and is "
                       "really a read set that never declared the top."
                       % (FRONT_END, top, len(files), note, top)], 2
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
    root = Path(tempfile.mkdtemp(dir=tmp, prefix="authority-"))
    (root / "syn" / "yosys").mkdir(parents=True)
    for name in LINKED:
        target = REPO / name
        if target.exists():
            (root / name).symlink_to(target)
    path = root / "syn" / "yosys" / "run.sh"
    path.write_text(text)
    return root, path


def _relative(root, rec):
    """The record's sources as the authority's own tree spells them.
    Each arm gets its own shadow root, so absolute paths differ by
    construction and only the tree-relative set is comparable."""
    return [] if rec is None else [_under(root, f) for f in rec["src"]]


def _record_arms(top, problems):
    """Arms 0-10: the RECORD model, with the front end stubbed out.

    A synthetic record goes in and `build()` judges it, so what these arms
    measure is the record model alone. Findings are appended to `problems`;
    the return value is how many arms ran.
    """
    ran = 0
    src = ["/r/a.sv", "/r/b.sv", "/r/" + PLANE, "/r/top.sv"]
    derived = ["/r/a.sv", "/r/" + PLANE]
    gone = set()

    def record(**over: list[str]) -> Record:
        """A well-formed record, with `over` replacing the field an arm mutates."""
        rec = {"top": [top], "define": ["SYNTHESIS"], "incdir": ["/r/inc"],
               "derived": list(derived), "src": list(src)}
        rec.update(over)
        return rec

    def stub_front_end(verdict: bool | None, note: str = "") -> Callable[..., Verdict]:
        """A front end that always answers `verdict`: these arms judge the record."""
        return lambda *a, **k: (verdict, note)

    def run(rec: Record, fe: Callable[..., Verdict] | None = None) -> Expansion:
        """`build()` over a synthetic record, with `gone` standing in for the tree."""
        return build(top, rec, exists=lambda f: f not in gone, front_end=fe or stub_front_end(True))

    def arm(name: str, want: str, rec: Record | None = None,
            fe: Callable[..., Verdict] | None = None, call: Callable[[], Answer] | None = None) -> None:
        """One arm: the finding must name `want` at rc!=0, because an arm that
        passes at rc=0 is the escape this self-test exists to catch."""
        nonlocal ran
        ran += 1
        _emitted, bad, rc = call() if call else run(rec, fe)
        if not any(want in b for b in bad) or rc == 0:
            problems.append("SELF-TEST FAILED [%s]: expected a finding naming "
                            "%r at rc!=0, got rc=%d %s"
                            % (name, want, rc, bad or "no findings"))

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
        call=lambda: ask_authority(top, Path("/r/run.sh"),
                                   lambda *a, **k: _Refused))

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

    # Arm 10. THE CONTRACT: no front end, no answer, no emission. The record is
    # well-formed and its sources are on disk; nothing answered whether the top
    # resolves, and that alone is the refusal. Deleting the `verdict is None`
    # arm of build() is what this bites, and that deletion is the whole of what
    # the tool-absent mode used to be.
    arm("no-front-end-is-a-refusal", "no front end resolved",
        record(), stub_front_end(None, "sv2v is not on PATH"))
    return ran


def _tooling_refusal():
    """Why arms 11-34 may not run, or None when everything they need is here.

    They refuse rather than skip: every escape this file has had lived in the
    gap between something modelled here and what bash and the front end
    actually do, so a skipped arm is a skipped finding.
    """
    if not (RUN_SH.exists() and shutil.which("bash")
            and (REPO / "protocol-processor" / "hdl").exists()
            and (REPO / "third_party" / "verilog-axis" / "rtl").exists()):
        return ("SELF-TEST FAILED [front-end-and-authority-arms]: "
                "syn/yosys/run.sh, bash and the protocol-processor and "
                "verilog-axis submodules are all required. The "
                "round-two escapes were all disagreements between a "
                "parser and bash, so skipping these arms is skipping "
                "the finding.")
    if shutil.which(FRONT_END) is None:
        return ("SELF-TEST FAILED [front-end-and-authority-arms]: %s is "
                "not on PATH. It is the only answerer for the "
                "declaration question, and the Yosys gate already "
                "requires it." % FRONT_END)
    return None


def _front_end_arms(top, tmp, problems):
    """Arms 11-23: one synthetic source, the REAL front end, nothing between.

    Each arm puts a construct in a one-file read set and asks sv2v, so what is
    asserted is the toolchain's answer and not a belief about the language.
    Returns how many arms ran.
    """
    ran = 0
    def one_file(name: str, body: str, want: str = "does not resolve", clean: bool = False) -> None:
        """One synthetic source, the real front end, nothing in between.

        `clean=True` is the other direction: the front end resolves the top
        and the flow must emit. Two arms use it, because a group of arms
        that only ever expects a refusal passes on a front end that refuses
        everything.
        """
        nonlocal ran
        ran += 1
        path = tmp / (name + ".sv")
        path.write_text(body)
        # `str(path)`: a record value is the authority's own token, and every
        # check below asks it a string question.
        _files, bad, rc = build(top, {"top": [top], "define": [],
                                      "incdir": [], "derived": [],
                                      "src": [str(path)]})
        if clean:
            if rc or bad:
                problems.append("SELF-TEST FAILED [%s]: %s resolves this "
                                "declaration, so the list must expand "
                                "clean; got rc=%d %s"
                                % (name, FRONT_END, rc, bad))
            return
        if rc == 0 or not any(want in b for b in bad):
            problems.append("SELF-TEST FAILED [%s]: expected a finding "
                            "naming %r at rc!=0, got rc=%d %s"
                            % (name, want, rc, bad or "no findings"))

    # Arm 11. ANTI-VACUITY for this group: a plain declaration expands
    # clean through the real front end.
    one_file("plain-declaration", "module %s;\nendmodule\n" % top,
             clean=True)

    # Arm 12. ISSUE #235 itself: sources present and correct, none of them
    # declaring the top. This is the list Vivado answers `module not found`.
    one_file("top-not-in-read-set", "module something_else;\nendmodule\n")

    # Arm 13. One step subtler: a file NAMED after the top that does not
    # declare it, which a file-name check would pass.
    one_file("named-not-declared", "// %s lives here\n" % top)

    # Arms 14-18. THE DECLARATION IS TEXT, NOT CODE ([R0] round one).
    one_file("block-commented-declaration",
             "/*\nmodule %s;\nendmodule\n*/\n" % top)
    one_file("line-commented-declaration",
             "// module %s;\n// endmodule\n" % top)
    one_file("inactive-conditional-declaration",
             "`ifdef SOME_DEFINE\nmodule %s;\nendmodule\n`endif\n" % top)
    one_file("declaration-inside-a-string",
             'module other;\n'
             '  localparam string S = "module %s; endmodule";\n'
             'endmodule\n' % top)
    one_file("prefix-of-the-top-declared",
             "module %s_shim;\nendmodule\n" % top)

    # Arms 19-21. THE DECLARATION IS TEXT, NOT PREPROCESSED CODE ([R0]
    # round two): an unexpanded macro BODY, in its three spellings.
    one_file("macro-body-declaration",
             "`define UNUSED \\\nmodule %s; \\\nendmodule\n" % top)
    one_file("macro-body-one-line",
             "`define UNUSED module %s; endmodule\n" % top)
    one_file("macro-body-after-a-comment",
             "`define UNUSED /* keep */ \\\nmodule %s; \\\nendmodule\n"
             % top)

    # Arm 22. [R0] ROUND THREE, the construct that closed the model: the
    # declaration is the ACTUAL ARGUMENT of a multiline macro invocation,
    # so it is argument text the expansion discards. The round-two model
    # dropped the invocation line and read the argument as code.
    one_file("macro-argument-declaration",
             "`define DISCARD(x)\n`DISCARD(\nmodule %s;\nendmodule\n)\n"
             % top)

    # Arm 23. The OTHER direction, and the reason a model cannot stand in
    # for the front end even conservatively: here the text carries no
    # declaration at all and the expansion produces one. The front end
    # resolves it, so the flow must emit -- the deleted model refused this.
    one_file("macro-expanded-declaration",
             "`define D module %s; endmodule\n`D\n" % top, clean=True)
    return ran


def _authority_baseline(real_top, real, tmp, problems):
    """Arm 24: ANTI-VACUITY over the REAL authority.

    Returns (arms run, the untouched read set as the authority's own tree
    spells it) - the mutation arms below compare against that set.
    """
    ran = 0
    # Arm 24. ANTI-VACUITY over the REAL authority: the untouched run.sh
    # expands clean through real bash and the real front end.
    ran += 1
    base_root, base_path = _shadow(real, tmp)
    base, bad, rc = ask_authority(real_top, base_path)
    base_src = _relative(base_root, base) if rc == 0 else []
    if rc == 0:
        _f, bad, rc = build(real_top, base)
    if rc or bad or len(base_src) < 2:
        problems.append("SELF-TEST FAILED [real-authority-clean]: the "
                        "untouched run.sh must expand clean, got rc=%d %s, "
                        "%d source(s)" % (rc, bad, len(base_src)))
    return ran, base_src


def _authority_mutation_arms(real_top, real, tmp, base_src, problems):
    """Arms 25-31: REAL BASH over a mutated real run.sh.

    The reviewer's four round-two counterexamples are four of them. Returns
    how many arms ran.
    """
    ran = 0
    def authority(name: str, mutate: Callable[[str], str], want: str | None,
                  expect_src: list[str] | None = None) -> None:
        """One mutation of the real run.sh, through real bash. `expect_src` is
        the other direction: bash ignores the mutation, so the read set may not
        move - which is what proves this consumer follows bash and not text."""
        nonlocal ran
        ran += 1
        root, path = _shadow(mutate(real), tmp)
        rec, bad, rc = ask_authority(real_top, path)
        if rc == 0:
            _files, bad, rc = build(real_top, rec)
        if expect_src is not None:
            if rc != 0 or _relative(root, rec) != expect_src:
                problems.append("SELF-TEST FAILED [%s]: bash ignores this "
                                "mutation, so the read set must be "
                                "unchanged; got rc=%d, %d source(s) %s"
                                % (name, rc, len(_relative(root, rec)), bad))
            return
        if rc == 0 or not any(want in b for b in bad):
            problems.append("SELF-TEST FAILED [%s]: expected a finding "
                            "naming %r at rc!=0, got rc=%d %s"
                            % (name, want, rc, bad or "no findings"))
    # Arm 25. [R0] round two, mutation 1: the generator token is suffixed.
    # The old recogniser accepted the expected path as a SUBSTRING and
    # returned rc=0 with 43 files; bash executes a nonexistent file and
    # takes run.sh's own `|| exit 2`.
    authority("generator-token-suffixed",
              lambda t: t.replace('"$R/scripts/pp_srcs.py"',
                                  '"$R/scripts/pp_srcs.py.broken"'),
              "so there is no read set to emit")

    # Arm 26. Mutation 2: the generator's --prefix points at a tree that
    # does not exist. The old recogniser ignored the invocation it claimed
    # to validate and ran its own; bash hands sv2v paths that are not there.
    authority("generator-prefix-diverted",
              lambda t: t.replace('--prefix "$PP"',
                                  '--prefix "$PP/not-the-tree"'),
              "missing sources")

    # Arm 27. Mutation 3: a valid shell COMMENT above the live row, spelt
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

    # Arm 28. Mutation 4: a positional that is not a source. The old
    # recogniser filtered it out before the missing-source check.
    authority("unaccounted-positional",
              lambda t: t.replace('PP_SRCS="$PP_DERIVED ',
                                  'PP_SRCS="$PP_DERIVED $PP/ghost.svh '),
              "are not .sv/.v sources")

    # Arm 29. The same positional spelt as a source that is not on disk.
    authority("missing-positional",
              lambda t: t.replace('PP_SRCS="$PP_DERIVED ',
                                  'PP_SRCS="$PP_DERIVED $PP/ghost.sv '),
              "missing sources")

    # Arm 30. [R0] round one, mutation D2, now through real bash: run.sh
    # drops the wrapper that declares the top. It stayed green at
    # 16,547 LUT when this file composed the parent half itself.
    authority("run-sh-drops-the-top",
              lambda t: t.replace(" $R/hdl/milan/KL_pp_shadow.sv", ""),
              "does not resolve `%s`" % real_top)

    # Arm 31. A top no row defines. run.sh answers, this flow reports it.
    ran += 1
    _rec, bad, rc = ask_authority("othertop", _shadow(real, tmp)[1])
    if rc == 0 or not any("unknown top: othertop" in b for b in bad):
        problems.append("SELF-TEST FAILED [unknown-top]: expected the "
                        "authority's own refusal, got rc=%d %s" % (rc, bad))
    return ran


def _real_text_arms(real_top, real, tmp, base_src, problems):
    """Arms 32-34: the two reopened escapes, end to end, on the real read set.

    Only the top's TEXT moves, which each arm asserts by comparing the source
    count with the baseline arm's. Returns how many arms ran.
    """
    ran = 0
    # Arms 32-34. THE TWO REOPENED ESCAPES, END TO END, ON THE REAL READ
    # SET. The file that declares the top is replaced on disk by the
    # round-two construct and then by the round-three one, and the whole
    # real record is driven through real bash. Only the top's TEXT moves,
    # which each arm asserts by comparing the source count with arm 24's.
    def real_set_with(name: str, body: str) -> tuple[Path, Path]:
        """A shadow root whose run.sh reads `body` where the file declaring the
        top used to be, so the mutation moves the top's TEXT and nothing else."""
        path = tmp / (name + ".sv")
        path.write_text(body)
        # run.sh is shell TEXT, so the substitution is a string one: this is
        # the one place a Path has to be spelled out before it goes in.
        return _shadow(
            real.replace("$R/hdl/milan/KL_pp_shadow.sv", str(path)), tmp)

    def real_text_arm(name: str, root: Path, path: Path,
                      fe: Callable[..., Verdict], want: str) -> None:
        """Drive the whole real record through bash with `fe` answering: the
        finding must name `want`, and the read set must still be arm 24's."""
        nonlocal ran
        ran += 1
        rec, bad, rc = ask_authority(real_top, path)
        if rc == 0:
            _f, bad, rc = build(real_top, rec, front_end=fe)
        if rc == 0 or not any(want in b for b in bad):
            problems.append("SELF-TEST FAILED [%s]: expected a finding "
                            "naming %r at rc!=0, got rc=%d %s"
                            % (name, want, rc, bad or "no findings"))
        if len(_relative(root, rec)) != len(base_src):
            problems.append("SELF-TEST FAILED [%s]: the mutation must "
                            "change only the top's TEXT, and it changed "
                            "the read set (%d vs %d source(s))"
                            % (name, len(_relative(root, rec)),
                               len(base_src)))

    macro_root, macro_path = real_set_with(
        "round2_body", "`define UNUSED \\\nmodule %s; \\\nendmodule\n"
        % real_top)
    arg_root, arg_path = real_set_with(
        "round3_argument",
        "`define DISCARD(x)\n`DISCARD(\nmodule %s;\nendmodule\n)\n"
        % real_top)

    # Arm 32. Round two's unexpanded macro body, real front end.
    real_text_arm("macro-body-real-front-end", macro_root, macro_path,
                  sv2v_verdict, "does not resolve")

    # Arm 33. ROUND THREE's macro argument, real front end. At the previous
    # head this same input reached `build()` and the front end refused it
    # there too; what had to change is the arm below.
    real_text_arm("macro-argument-real-front-end", arg_root, arg_path,
                  sv2v_verdict, "does not resolve")

    # Arm 34. ROUND THREE with NO FRONT END -- the path a Vivado host that
    # has not installed sv2v takes. At the previous head this returned rc=0
    # with no findings, because a model of the directive layer answered in
    # the front end's place; there is no such model now, so the answer is a
    # refusal naming the missing tool. Restoring the `verdict is None` pass
    # is what reddens here.
    real_text_arm("macro-argument-no-front-end", arg_root, arg_path,
                  lambda *a, **k: (None, "no front end"),
                  "no front end resolved")
    return ran


def selftest(top: str = "faketop", real_top: str = "KL_pp_shadow") -> tuple[list[str], int]:
    """Prove every check bites. Returns (problems, arms run).

    CONTRIBUTING.md section 3 states the bar: a checker carries a self-test that
    runs in a gate "so the tool cannot rot into a green that means nothing".
    Every arm drives the real `build()`, `parse_record()` or `ask_authority()`,
    so stubbing any of them to return no problems fails this.

    Three groups, and the middle one CHANGED SHAPE in round three. The record
    arms inject a synthetic record and stub the front end, because they are
    about the record. The front-end arms used to assert what a model of the
    directive layer believed about a construct; they now put each construct in a
    one-file read set and ask the REAL `sv2v`, so what is asserted is the
    toolchain's answer and not a belief about the language. Two of them run the
    other way -- a plain declaration and a macro-EXPANDED one must both expand
    clean -- so this group cannot be passing on a front end that refuses
    everything. The authority arms run REAL BASH over a mutated copy of the real
    syn/yosys/run.sh from a link farm.

    The front-end and authority arms need `sv2v` and the protocol-processor and
    verilog-axis submodules, and they refuse rather than skip when either is
    absent: every escape this file has had lived in the gap between something
    modelled here and what bash and the front end actually do.
    """
    problems = []
    ran = _record_arms(top, problems)

    # ---- front-end arms --------------------------------------------------
    # From here the REAL front end runs, so its absence is a failure and not a
    # skip: these arms ARE the top-resolution check now.
    refusal = _tooling_refusal()
    if refusal:
        problems.append(refusal)
        return problems, ran

    real = RUN_SH.read_text()
    tmp = Path(tempfile.mkdtemp(prefix="dp-srcs-selftest-"))
    try:
        ran += _front_end_arms(top, tmp, problems)
        # ---- authority arms ----------------------------------------------
        # These run REAL BASH over a mutated real run.sh, and the reviewer's
        # four round-two counterexamples are four of them.
        base_ran, base_src = _authority_baseline(real_top, real, tmp,
                                                 problems)
        ran += base_ran
        ran += _authority_mutation_arms(real_top, real, tmp, base_src,
                                        problems)
        ran += _real_text_arms(real_top, real, tmp, base_src, problems)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), %s "
                        "declares %d. An arm was deleted or added without "
                        "moving the count." % (ran, __file__, ARMS))
    return problems, ran


def main() -> int:
    """Emit one top's source list, or its whole record, or run the self-test.
    The authority's refusal and the front end's silence are both this flow's
    exit status: there is no mode in which a list is printed unchecked."""
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", default="milan_datapath",
                    help="the run.sh entry to expand (default: milan_datapath)")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each check fails on a planted defect")
    ap.add_argument("--record", action="store_true",
                    help="print the whole consumable record -- top=/define=/"
                         "incdir=/src= lines, authority order -- rather than "
                         "the bare source list. A consumer that must also "
                         "PREPROCESS these sources (Vivado, sv2v) needs the "
                         "defines and the include path, and an include path "
                         "spelled by hand is the drift this file exists to "
                         "prevent: syn/yosys/run.sh puts the elaboration-shape "
                         "config dir FIRST for milan_datapath, and any other "
                         "order silently selects a different entity shape.")
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
        files, problems, rc = build(args.top, rec)
    for p in problems:
        print(p, file=sys.stderr)
    if rc:
        return rc
    if args.record:
        out = ["top=" + t for t in rec["top"]]
        out += ["define=" + d for d in rec["define"]]
        out += ["incdir=" + i for i in rec["incdir"]]
        out += ["src=" + f for f in files]
        print("\n".join(out))
        return 0
    print("\n".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
