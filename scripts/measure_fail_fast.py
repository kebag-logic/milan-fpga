#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure where a failure could pass for success, and hold the count down.

Why this exists. Rule 6 of the maintainability guide
(docs/development/CODE_QUALITY.md) says an invalid parameter, state or tool
result must be rejected at the nearest responsible boundary and must propagate
a non-success verdict. Three populations in this tree can break that, and they
break it silently:

  1. A PARAMETERISED MODULE WITH NO ELABORATION CONTRACT. 102 first-party
     modules across the superproject and its project-owned processor
     submodules declare parameters; 17 reject an impossible combination at
     elaboration. The rest accept any value the caller passes.
     `rx_mac_filter` documented "true for TDATA_WIDTH>=48" in a banner for
     months - a comment does not stop a build, and at 32 bits the destination
     compare would have read past the end of the beat and filtered on
     undefined bits, which nothing downstream can detect.

     WHAT COUNTS AS A CONTRACT: `$error` or `$fatal` at MODULE OR GENERATE
     SCOPE - outside every always/initial/final block and outside every
     function and task. That is the one form every flow evaluates when the
     parameters are bound. An `initial begin ... $fatal` or an `assert (...)
     else $error` inside `initial` is a simulation check: Verilator builds the
     binary, Vivado and Yosys synthesise the module, and only a simulation run
     refuses - so it is NOT counted (KL_pp_acmp_listener, KL_avtp_common_parser
     are inventoried as unguarded for that reason). A `$error` inside `always`
     is a runtime assertion and is not counted either, so adding one cannot
     empty this ratchet (review found KL_gptp_engine would otherwise have
     counted as guarded on three runtime PathTrace assertions). Nor is a
     CONCURRENT or DEFERRED assertion at module scope: `assert property
     (@(posedge clk) P) else $error` fires its action block at a clock edge
     during simulation, `assert #0 (...) else $error` in the Observed region,
     and neither can refuse an illegal parameter when the parameters are
     bound - review reproduced the concurrent form counting as a contract.
     So the recognition is POSITIVE: the scan starts after the module header
     and descends only into what elaboration evaluates - `generate`,
     `if`/`else`, `for`, `case` and `begin : name ... end` - and steps over
     every other item whole (a procedural block, any assert/assume/cover/
     restrict with its action block, a property/sequence/function/task
     declaration, a preprocessor line, a plain item to its `;`). A `$error`
     the walk never reaches is not the contract.

     WHICH MODULES HAVE PARAMETERS is read with scripts/sv_ports.py, the one
     header parser the Rule 4 and Rule 5 gates already use, so every parameter
     form this tree writes counts: `int unsigned`, `string`, `type`, `real`,
     `longint`, a packed range, and a parameter with no default. The first
     regex here accepted only `parameter int X =` and saw 53 of the 102 -
     none of gptp-processor's - which is why the first budget said 43.

  2. A PIPELINE THAT DISCARDS ITS PRODUCER'S EXIT CODE. In a shell without
     `pipefail`, `gate | tee log` exits with tee's status, so a failing gate
     reads as a pass. This is scored per logical line and only for producers
     that ARE a verdict - a tool run, a make, a gate script, a simulator
     binary, a `.sh` invocation - and for a leftmost `grep`/`cat` that READS A
     FILE: `grep -A2 "LUTs" util.rpt | head` under `set -e` without pipefail
     exits 0 when the report does not exist, which is how a synthesis flow
     whose tools produced nothing was published as measured
     (gptp-processor/syn/ooc/run.sh, at the pin). A pipeline that writes its
     producer's status to a file inside its own group - `{ tool; echo $? > f; }
     | tee out` - keeps the verdict and is not a finding.

  3. A CAPTURED VERDICT WHOSE STATUS IS DISCARDED. `out=$(verilator ...)`
     followed by a grep of the TEXT decides the verdict from what the tool
     printed, never from what it returned. Without errexit the assignment's
     status goes nowhere; with `local`/`export` in front it is the builtin's
     status even under errexit. A verilator that crashes silently, or is not
     installed and shadowed by a stub, prints nothing, matches no `%Error`,
     and reads as LINT OK for every top (protocol-processor/scripts/
     lint_hdl.sh, at the pin). A capture whose status is consulted - `||`,
     `&&`, an `if`/`!`/`[` in front, or `$?` read on the same or the next
     logical line - is not a finding. Only the assignment forms are modelled:
     an argument-form `echo "k=$(tool)"` is a verdict the CONSUMER decides,
     and the one such site here (elaborate.yml's scope publication) is
     fail-closed by the CI contract, which treats an empty publication as
     RTL-relevant.

THE MEASURED POPULATION for 2 and 3 is every first-party `.sh`, every GitHub
workflow `run:` block, and every RECIPE line of every first-party Makefile.
Each logical recipe line is its own `/bin/sh -c`, so a recipe never has
pipefail or errexit unless `.SHELLFLAGS` says so (no Makefile here sets it),
and make variables that name a tool (`$(VERILATOR)`, `$(PY)`, `$(MAKE)`) are
expanded from the file's own definitions before the line is read. Python and
Tcl are NOT measured: review surveyed both at this head - no `os.system`, no
`shell=True`, every `check=False` keeps the return code, Tcl `exec` raises on
a non-zero status and the only `catch` sites are Vivado-generated - and the
guide says so rather than letting the table read as tree-wide.

THE SHELL MODEL is per unit, in order. A `.sh` starts with whatever its
shebang says (`#!/bin/bash -eo pipefail` counts) and is protected only after
its own `set` runs; a later `set` cannot protect an earlier line. Comments are
blanked before that search, so `# set -o pipefail is not used` protects
nothing; a here-document body is text, not commands; a `set` inside `( ... )`
lasts until the subshell closes. GITHUB'S DEFAULT `run` SHELL IS `bash -e {0}`:
errexit, NO pipefail. Only a step that declares `shell: bash` gets
`-eo pipefail`, and options set inside one step never reach the next.

WAIVERS are by SITE - path plus the exact line - and are consulted only after
a line has been found masked: `verilator --version | grep -F "$WANT"` wants
grep's status, because grep IS the assertion. A new site has to be added here
deliberately, and a waiver whose line no longer exists fails the self-test.
Debt that lives in a pinned processor submodule is counted here and fixed
upstream; the pin bump lowers the ratchet.

Usage:
    python3 scripts/measure_fail_fast.py            # the inventories
    python3 scripts/measure_fail_fast.py --check    # the ratchet
    python3 scripts/measure_fail_fast.py --selftest # fixture arms

Exit 0 = at or under all three ratchets in scripts/fail_fast.budget; 1 = over
a ratchet or the budget is unusable; 2 = the population could not be read
(an unterminated here-document makes the rest of a script unreadable).
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "fail_fast.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE
from code_quality_scope import tracked
from sv_ports import declarations

#: archive scope: code_quality_scope.tracked() drops the vendor gitlinks itself
#: (third_party/, external/), so what this filter still owns is the
#: superproject's own archive directory - a historical Makefile is not a build
NOT_FIRST_PARTY = ("third_party/", "external/", "docs/history/v1/")


class Unreadable(Exception):
    """The population cannot be read to the end - a partial scan is not a pass."""


# --- 1. modules ----------------------------------------------------------------

COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
STRING = re.compile(r'"(?:[^"\\\n]|\\.)*"')
IMPORT = re.compile(r"\bimport\b[^;]*;")
ELAB_CHECK = re.compile(r"\$(?:fatal|error)\b")
MODULE = re.compile(r"^\s*module\s+([A-Za-z_]\w*)\b", re.M)
ENDMODULE = re.compile(r"\bendmodule\b")

#: what follows one of these runs at simulation time, not at elaboration
_PROCEDURAL = ("always", "always_ff", "always_comb", "always_latch", "initial", "final")
#: an assertion of any kind - immediate, deferred (`#0`, `final`) or
#: concurrent (`property`, `sequence`) - whose action block is simulation-time
_ASSERTION = ("assert", "assume", "cover", "restrict")
#: declarations that close with their own keyword and hold no generate scope
_OPAQUE = {
    "property": "endproperty", "sequence": "endsequence",
    "function": "endfunction", "task": "endtask", "checker": "endchecker",
    "class": "endclass", "clocking": "endclocking", "covergroup": "endgroup",
    "module": "endmodule", "macromodule": "endmodule",
    "interface": "endinterface", "program": "endprogram", "package": "endpackage",
}
#: a closer met where no opener was walked: stepped over, never descended
_STRAY = ("end", "endcase", "endgenerate", "endmodule", "join", "join_any", "join_none")
_FUNC_TASK = re.compile(r"\bfunction\b.*?\bendfunction\b|\btask\b.*?\bendtask\b", re.S)
_WORD = re.compile(r"[A-Za-z_]\w*")
_BLOCKS = {
    "begin": re.compile(r"\b(?P<open>begin)\b|\b(?P<close>end)\b"),
    "fork": re.compile(r"\b(?P<open>fork)\b|\b(?P<close>join(?:_any|_none)?)\b"),
    "case": re.compile(r"\b(?P<open>case[xz]?)\b|\b(?P<close>endcase)\b"),
}


def _blank(m):
    return "".join(c if c == "\n" else " " for c in m.group(0))


def blank_comments(text):
    return COMMENT.sub(_blank, text)


def _skip_ws(code, i):
    while i < len(code) and code[i].isspace():
        i += 1
    return i


def _skip_parens(code, i):
    """`i` at `(`; the index just past its matching `)`."""
    depth = 0
    while i < len(code):
        if code[i] == "(":
            depth += 1
        elif code[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(code)


def _word_at(code, i):
    m = _WORD.match(code, i)
    return m.group(0) if m else ""


def _block_end(code, i, kind):
    depth = 1
    for m in _BLOCKS[kind].finditer(code, i):
        depth += 1 if m.group("open") else -1
        if depth == 0:
            return m.end()
    return len(code)


def _statement_end(code, i):
    """The index just past the procedural statement that starts at code[i:].

    `begin`/`fork`/`case` blocks run to their closer; `if` (and an immediate
    `assert`) takes a parenthesised condition, a statement and an optional
    `else` statement; loops take a head and a statement; anything else is a
    simple statement that runs to its `;`."""
    i = _skip_ws(code, i)
    if i >= len(code):
        return i
    w = _word_at(code, i)
    if w in ("begin", "fork"):
        return _block_end(code, i + len(w), w)
    if w in ("case", "casez", "casex"):
        return _block_end(code, i + len(w), "case")
    if w == "if" or w in _ASSERTION:
        j = _skip_ws(code, i + len(w))
        if j < len(code) and code[j] == "#":  # deferred immediate: `assert #0 (...)`
            j = _skip_ws(code, j + 1)
            while j < len(code) and code[j].isdigit():
                j += 1
            j = _skip_ws(code, j)
        while _word_at(code, j) in ("property", "sequence", "final"):
            j = _skip_ws(code, j + len(_word_at(code, j)))
        if j < len(code) and code[j] == "(":
            j = _skip_parens(code, j)
        j = _skip_ws(code, j)
        if _word_at(code, j) != "else":
            j = _skip_ws(code, _statement_end(code, j))
        if _word_at(code, j) == "else":
            j = _statement_end(code, j + 4)
        return j
    if w in ("for", "while", "foreach", "repeat"):
        j = _skip_ws(code, i + len(w))
        if j < len(code) and code[j] == "(":
            j = _skip_parens(code, j)
        return _statement_end(code, j)
    if w == "forever":
        return _statement_end(code, i + len(w))
    depth = 0
    while i < len(code):
        if code[i] == "(":
            depth += 1
        elif code[i] == ")":
            depth -= 1
        elif code[i] == ";" and depth <= 0:
            return i + 1
        i += 1
    return len(code)


def _procedural_end(code, i, w):
    """`i` at always*/initial/final: the index just past the whole procedural
    statement, sensitivity list and all."""
    j = _skip_ws(code, i + len(w))
    if j < len(code) and code[j] == "@":
        j = _skip_ws(code, j + 1)
        if j < len(code) and code[j] == "(":
            j = _skip_parens(code, j)
        elif j < len(code) and code[j] == "*":
            j += 1
    return _statement_end(code, j)


def _skip_block_label(code, j):
    """`j` just past `begin`/`end`: past an optional `: name`."""
    k = _skip_ws(code, j)
    if k < len(code) and code[k] == ":" and code[k:k + 2] != "::":
        k = _skip_ws(code, k + 1)
        return k + len(_word_at(code, k))
    return j


_LABEL_TOK = re.compile(r"::|[;?:`()\[\]{}]|\b(?:begin|end)\b")


def _label_end(code, i):
    """`i` at an item that may start with a label - `a1: assert ...`,
    `8, 16: begin`, `default:` - the index just past its `:`, or -1 when no
    label opens the item. A `;`, a ternary `?`, a directive, a `begin` or an
    `end` met first means there is none: the `begin : name` of a block is
    not a label, and reading it as one would walk INTO the block
    (KL_gptp_engine, whose `endif sits right before a named always_ff)."""
    depth = 0
    for m in _LABEL_TOK.finditer(code, i):
        t = m.group(0)
        if t in ("(", "[", "{"):
            depth += 1
        elif t in (")", "]", "}"):
            depth -= 1
        elif t == "::" or depth:
            continue
        elif t == ":":
            return m.end()
        else:
            return -1
    return -1


def _directive_end(code, i):
    """`i` at a backtick: past the preprocessor line and any backslash-
    continued line after it. `ifdef/`else/`endif/`define/`include are
    lines, not items; nothing on such a line opens a scope."""
    while True:
        j = code.find("\n", i)
        if j < 0:
            return len(code)
        if code[i:j].rstrip().endswith("\\"):
            i = j + 1
            continue
        return j + 1


def _walk_one(code, i, found):
    """One generate item at `i`; the index just past it."""
    i = _skip_ws(code, i)
    if i >= len(code):
        return i
    j = _walk_item(code, i, _word_at(code, i), found)
    return j if j > i else i + 1


def _walk_items(code, i, closer, found):
    """Generate items from `i` up to and including `closer` (or the end)."""
    while True:
        i = _skip_ws(code, i)
        if i >= len(code):
            return i
        w = _word_at(code, i)
        if closer is not None and w == closer:
            return _skip_block_label(code, i + len(w))
        j = _walk_item(code, i, w, found)
        i = j if j > i else i + 1


def _walk_item(code, i, w, found):
    """Classify the item at `i` and descend only into what elaboration
    evaluates; record a `$error`/`$fatal` met at that scope in `found`."""
    n = len(code)
    if code[i] == ";":
        return i + 1
    if code[i] == "`":
        return _directive_end(code, i)
    if ELAB_CHECK.match(code, i):
        found.append(i)
        return _statement_end(code, i)
    if w in _PROCEDURAL:
        return _procedural_end(code, i, w)
    if w in _ASSERTION:
        return _statement_end(code, i)
    if w in _OPAQUE:
        m = re.compile(r"\b" + _OPAQUE[w] + r"\b").search(code, i + len(w))
        return m.end() if m else n
    if w == "generate":
        return i + len(w)
    if w == "begin":
        return _walk_items(code, _skip_block_label(code, i + len(w)), "end", found)
    if w in ("if", "for", "case", "casex", "casez"):
        j = _skip_ws(code, i + len(w))
        if j < n and code[j] == "(":
            j = _skip_parens(code, j)
        if w.startswith("case"):
            return _walk_items(code, j, "endcase", found)
        j = _walk_one(code, j, found)
        if w == "if":
            k = _skip_ws(code, j)
            if _word_at(code, k) == "else":
                j = _walk_one(code, k + 4, found)
        return j
    if w in _STRAY:
        return _skip_block_label(code, i + len(w))
    k = _label_end(code, i)
    if k > 0:
        return k
    return _statement_end(code, i)


def elaboration_checks(code):
    """Indexes of every `$error`/`$fatal` reached from module scope through
    generate constructs only. `code` is one module, comments blanked. Strings
    go too (a message may say "always"), then imports (a DPI `import ...
    function` has no `endfunction`), then function and task bodies. The walk
    starts after the module header and descends only into `generate`,
    `if`/`else`, `for`, `case` and `begin : name ... end`; a procedural
    block, an assertion of any kind with its action block (immediate,
    deferred `#0`/`final`, concurrent `property`/`sequence`), a
    property/sequence declaration and every plain item are stepped over
    whole. A `$error` the walk never reaches is not the contract."""
    code = STRING.sub(_blank, code)
    code = IMPORT.sub(_blank, code)
    code = _FUNC_TASK.sub(_blank, code)
    found = []
    _walk_items(code, _statement_end(code, 0), None, found)
    return found


def has_elaboration_check(code):
    """True when `$error`/`$fatal` sits at module or generate scope."""
    return bool(elaboration_checks(code))


def scan_modules(text):
    """Return `(name, has_parameters, has_check)` per module, never per file."""
    code = blank_comments(text)
    with_params = {mod for mod, _n, _d, _mb, kind in declarations(text) if kind == "param"}
    rows = []
    for match in MODULE.finditer(code):
        end = ENDMODULE.search(code, match.end())
        if end is None:
            continue
        name = match.group(1)
        rows.append((name, name in with_params,
                     has_elaboration_check(code[match.start():end.end()])))
    return rows


def scan_module(text):
    """(declares_parameters, has_elaboration_check) for a one-module source."""
    rows = scan_modules(text)
    return (rows[0][1], rows[0][2]) if rows else (False, False)


# --- 2 and 3. shell ------------------------------------------------------------

#: Commands whose exit status IS a verdict: tools, make (bare or as `$MAKE`),
#: gate scripts, any `.sh`, a Verilator simulator binary (`.../V<top>`), and
#: the same names spelled as a shell variable (`$VERILATOR`, `$PY`).
PRODUCER = (
    r"(?:python3?|make|verilator(?:_coverage)?|yosys|sv2v|vivado|xvlog|xelab|xsim"
    r"|iverilog|vvp|behave|pytest|\S*\.sh|\S*/V\w+|scripts/\S+\.py"
    r"|\$\{?(?:MAKE|PY|PYTHON3?|VERILATOR(?:_COVERAGE)?|YOSYS|SV2V|VIVADO|XVLOG"
    r"|XELAB|IVERILOG)\}?)(?=\s|$|;|\))"
)

#: A pipeline whose producer is a verdict-bearing command. `\|\|` is excluded:
#: `a || b` is a fallback, not a pipe. Matched against shell_code(), never the
#: raw line.
PIPE = re.compile(r"^\s*(?P<lhs>.*?(?<![\w.-])(?:\S*/)?" + PRODUCER + r"[^|]*?)\|(?!\|)")

#: A leftmost grep/cat that reads a FILE and feeds a consumer. The file is the
#: flow's product, so its absence is the failure; grep reading stdin is a
#: consumer (an assertion) and is not matched here. Matched against
#: shell_code(), where quoted patterns are already blanked.
FILE_PIPE = re.compile(r"^\s*(?:grep|egrep|fgrep|cat)\b(?P<args>[^|]*)\|(?!\|)")

#: `{ tool; echo $? > file; } | tee out` - the status is written before the
#: pipe can lose it (tb/verilator/tsn_fuzz reads it back on the next line)
STATUS_SAVED = re.compile(r"echo\s+\$\?\s*>")

#: A captured verdict: `$(tool ...)` for the same producers as PIPE. Matched
#: on the RAW logical line (shell_code() blanks substitutions on purpose).
SUBST = re.compile(r"\$\(\s*" + PRODUCER)

#: Pipelines where the CONSUMER is the assertion and its status is the point.
#: Waived by SITE: the path and the exact line, consulted only once the line
#: has been found masked. A new one is added here, deliberately; one whose
#: line is gone fails the self-test.
INTENTIONAL = (
    (".github/workflows/rtl-fast.yml",
     '/opt/verilator/bin/verilator --version | grep -F "${VERILATOR_VERSION#v}"',
     "the grep IS the version assertion; its status is the verdict"),
    (".github/workflows/rtl.yml",
     '/opt/verilator/bin/verilator --version | grep -F "${VERILATOR_VERSION#v}"',
     "the grep IS the version assertion; its status is the verdict"),
)

#: quoted spans, arithmetic, command substitutions and parameter expansions,
#: blanked before the producer search
_QUOTED = re.compile(r"\$\(\([^)]*\)\)|\$\([^()]*\)|\$\{[^}]*\}|'[^']*'|\"[^\"]*\"")
_ARITH_SUBST = re.compile(r"\$\(\([^)]*\)\)|\$\([^()]*\)")
_COMMENT = re.compile(r"(?:^|(?<=\s))#.*$")
_HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*(?:'([A-Za-z_]\w*)'|\"([A-Za-z_]\w*)\"|([A-Za-z_]\w*))")
#: `(`, `)` and every `set` invocation, in line order
_SET_TOKENS = re.compile(r"\(|\)|\bset\s+(?:[-+][\w-]*\s+)*[-+][\w-]*(?:\s+[a-z]+)*")
_PIPEFAIL_OFF = re.compile(r"\+o\s+pipefail\b")
_ERREXIT_ON = re.compile(r"(?:^|\s)-[a-df-zA-Z]*e[a-zA-Z]*\b|-o\s+errexit\b")
_ERREXIT_OFF = re.compile(r"(?:^|\s)\+[a-zA-Z]*e[a-zA-Z]*\b|\+o\s+errexit\b")
_GUARD_PREFIX = re.compile(r"^\s*(?:if|elif|while|until)\b|^\s*!\s|^\s*\[|^\s*test\b")
_BUILTIN_PREFIX = re.compile(r"^\s*(?:local|export|declare|readonly|typeset)\b")
_ASSIGN_PREFIX = re.compile(r"^\s*[A-Za-z_]\w*\+?=")
_SEGMENT = re.compile(r";|&&|\|\||\bthen\b|\bdo\b|\belse\b|\{")
_SHEBANG = re.compile(r"^#!.*\b(?:ba)?sh\b(.*)$")


def _blank_len(m):
    return " " * len(m.group(0))


def shell_code(line):
    """The part of a shell line that is COMMAND, with quotes, arithmetic,
    `$(...)`, `${...}` and the trailing comment blanked out, length kept.

    Two false positives forced the first two. `printf "yosys FAIL: %s" ... |
    head` matched because the tool name was inside a FORMAT STRING, and a pipe
    inside `$(...)` is a substitution feeding an argument - its status is
    never the line's verdict, which is set by the command that consumes it.
    The comment came from review: `# set -o pipefail is not used here` used
    to protect every pipeline after it.
    """
    return _COMMENT.sub(_blank_len, _QUOTED.sub(_blank_len, line))


def logical_lines(lines, start):
    """Join backslash-continued lines; yields (first_line_no, joined)."""
    buf, first = [], None
    for n, line in enumerate(lines, start):
        if first is None:
            first = n
        if line.rstrip().endswith("\\"):
            buf.append(line.rstrip()[:-1])
            continue
        buf.append(line)
        yield first, " ".join(buf)
        buf, first = [], None
    if buf:
        yield first, " ".join(buf)


def shebang_options(text):
    """(pipefail, errexit) a `.sh` starts with: `#!/bin/bash -eo pipefail`."""
    m = _SHEBANG.match(text.split("\n", 1)[0])
    if not m:
        return False, False
    opts = m.group(1)
    return bool(re.search(r"\bpipefail\b", opts)), bool(_ERREXIT_ON.search(opts))


def _apply_set(tok, state):
    """Fold one `set ...` invocation into state = {pipefail, errexit}."""
    if "pipefail" in tok:
        state["pipefail"] = not _PIPEFAIL_OFF.search(tok)
    if _ERREXIT_OFF.search(tok):
        state["errexit"] = False
    elif _ERREXIT_ON.search(tok):
        state["errexit"] = True


def _state_walk(code, state, stack):
    """Yield (position, state-snapshot) for every token that can change the
    shell's options on this line, folding `(`/`)` scoping and `set` into
    `state` in place. The caller reads the snapshot at the position it cares
    about (the pipe, the `$(`)."""
    for m in _SET_TOKENS.finditer(code):
        tok = m.group(0)
        if tok == "(":
            stack.append(dict(state))
        elif tok == ")":
            if stack:
                state.update(stack.pop())
        else:
            _apply_set(tok, state)
        yield m.end(), dict(state)


def _state_at(pos, walk, state0):
    """The option state in force at character `pos`, given the walk."""
    cur = state0
    for end, snap in walk:
        if end > pos:
            break
        cur = snap
    return cur


def scan_pipeline(line):
    """(is_masked, pipe_position) for one shell logical line, ignoring
    options: is there a verdict-bearing producer on the left of a pipe?"""
    if line.lstrip().startswith("#"):
        return False, -1
    code = shell_code(line)
    m = PIPE.match(code)
    if m:
        if STATUS_SAVED.search(m.group("lhs")):
            return False, -1
        return True, m.end() - 1
    m = FILE_PIPE.match(code)
    if m:
        bare = [t for t in m.group("args").split() if not t.startswith("-")]
        # grep: pattern then file(s) - a quoted pattern was blanked, so a bare
        # file token alone means the pattern was quoted; cat: any bare token
        is_cat = code.lstrip().startswith("cat")
        quoted_pattern = bool(re.match(r"^\s*(?:grep|egrep|fgrep)\b[^|]*?[\"']", line))
        needs = 1 if (is_cat or quoted_pattern) else 2
        return len(bare) >= needs, m.end() - 1
    return False, -1


def scan_substitution(line, errexit, next_line=""):
    """(is_masked, form) for one logical line holding `$(producer ...)`.

    Forms: `local/export x=$(...)` is masked whatever errexit says - the status
    is the builtin's. A bare assignment is masked when errexit is off and
    nothing consults the status: no `||`/`&&` after it, no `$?` in the rest of
    the command or at the start of the next line. A test (`if`, `!`, `[`)
    consults it. Any other form is the consumer's verdict and is not modelled
    here."""
    if line.lstrip().startswith("#"):
        return False, "comment"
    m = SUBST.search(line)
    if not m:
        return False, ""
    seg_start = 0
    for s in _SEGMENT.finditer(shell_code(line), 0, m.start()):
        seg_start = s.end()
    head = line[seg_start:m.start()]
    if _BUILTIN_PREFIX.match(head):
        return True, "builtin"
    if _GUARD_PREFIX.match(head):
        return False, "test"
    if _ASSIGN_PREFIX.match(head):
        tail = line[m.end():]
        consulted = ("||" in tail) or ("&&" in tail) or ("$?" in tail) \
            or bool(re.match(r"\s*(?:if\s+|\[\s*|test\s+)?[^;]*\$\?", next_line))
        return (not errexit) and not consulted, "assignment"
    return False, "argument"


_STEP_START = re.compile(r"^\s*-\s+\w+:")
_SHELL_BASH = re.compile(r"^\s*shell:\s*bash\b")


def workflow_steps(text):
    """[(first_line_no, lines, bash_shell)] - one entry per workflow step.

    Text before the first `- key:` is the preamble (one entry, no shell). A
    step declares `shell: bash` before or after its `run:` block, so the whole
    step is read before its lines are scanned."""
    steps, cur, start = [], [], 1
    for n, line in enumerate(text.splitlines(), 1):
        if _STEP_START.match(line) and cur:
            steps.append((start, cur))
            cur, start = [], n
        cur.append(line)
    if cur:
        steps.append((start, cur))
    return [(start, lines, any(_SHELL_BASH.match(l) for l in lines))
            for start, lines in steps]


_MAKE_VAR = re.compile(r"^[ \t]*([A-Za-z_]\w*)[ \t]*[?:+!]*=[ \t]*(.*?)[ \t]*$", re.M)
_MAKE_REF = re.compile(r"\$[({]([A-Za-z_]\w*)[)}]")
_SHELLFLAGS = re.compile(r"^[ \t]*\.SHELLFLAGS[ \t]*[?:+!]*=[ \t]*(.*?)[ \t]*$", re.M)


def make_recipes(text):
    """[(first_line_no, shell_line)] - every logical recipe line of a Makefile
    as the shell will see it: `$$` lowered to `$`, `$(VAR)` expanded from the
    file's own definitions (so `$(VERILATOR)`, `$(PY)` and `$(MAKE)` name
    their tools), leading `@`/`-`/`+` dropped."""
    defs = {"MAKE": "make"}
    for m in _MAKE_VAR.finditer(text):
        defs.setdefault(m.group(1), m.group(2))

    def expand(s):
        for _ in range(4):
            s2 = _MAKE_REF.sub(lambda m: defs.get(m.group(1), m.group(0)), s)
            if s2 == s:
                break
            s = s2
        return s

    out = []
    for n, line in logical_lines(text.splitlines(), 1):
        if not line.startswith("\t"):
            continue
        shell = expand(line.replace("$$", "\0")).replace("\0", "$")
        shell = re.sub(r"^[\t ]*[@+-]*", "", shell)
        out.append((n, shell))
    return out


def _units(text, kind):
    """[(first_line_no, lines, pipefail0, errexit0)] - the scan units.

    A `.sh` file is one unit that starts with its shebang's options. A
    workflow is one unit per step: GitHub's default shell is `bash -e {0}`
    (errexit, no pipefail), and `shell: bash` is `bash --noprofile --norc -eo
    pipefail {0}`; options set inside one step never reach the next. A
    Makefile is one unit per logical recipe line, each its own `/bin/sh -c`
    with only what `.SHELLFLAGS` gives it."""
    if kind == "workflow":
        return [(start, lines, bash, True) for start, lines, bash in workflow_steps(text)]
    if kind == "makefile":
        m = _SHELLFLAGS.search(text)
        flags = m.group(1) if m else ""
        pf, ee = bool(re.search(r"\bpipefail\b", flags)), bool(_ERREXIT_ON.search(flags))
        return [(n, [line], pf, ee) for n, line in make_recipes(text)]
    pf, ee = shebang_options(text)
    return [(1, text.splitlines(), pf, ee)]


def scan_shell(text, kind="sh", rel=""):
    """(masked_pipelines, waived, masked_captures) for one file, each a list
    of (line_no, text-or-reason), respecting activation order per unit."""
    masked, waived, captured = [], [], []
    for start, lines, pipefail0, errexit0 in _units(text, kind):
        state, stack, heredoc = {"pipefail": pipefail0, "errexit": errexit0}, [], None
        logical = list(logical_lines(lines, start))
        for k, (n, line) in enumerate(logical):
            if heredoc is not None:
                if line.strip() == heredoc:
                    heredoc = None
                continue
            code = shell_code(line)
            hd = _HEREDOC.search(_COMMENT.sub(_blank_len, _ARITH_SUBST.sub(_blank_len, line)))
            if hd:
                heredoc = hd.group(1) or hd.group(2) or hd.group(3)
            state0 = dict(state)
            walk = list(_state_walk(code, state, stack))
            is_masked, pos = scan_pipeline(line)
            text = " ".join(line.split())
            if is_masked and not _state_at(pos, walk, state0)["pipefail"]:
                site = next((why for path, txt, why in INTENTIONAL
                             if path == rel and text == txt), None)
                (waived if site else masked).append((n, site or text[:96]))
            m = SUBST.search(line)
            if m:
                nxt = logical[k + 1][1] if k + 1 < len(logical) else ""
                errexit = _state_at(m.start(), walk, state0)["errexit"]
                if scan_substitution(line, errexit, nxt)[0]:
                    captured.append((n, text[:96]))
        if heredoc is not None:
            raise Unreadable(f"{rel or '<text>'}:{start}: here-document `{heredoc}` "
                             f"is never terminated, so the rest of the unit cannot be read")
    return masked, waived, captured


def scan_pipelines(text, workflow=False, rel="", kind=None):
    """Masked and waived pipeline rows - the pipeline half of scan_shell()."""
    masked, waived, _ = scan_shell(text, kind or ("workflow" if workflow else "sh"), rel)
    return masked, waived


def scan_substitutions(text, workflow=False, kind=None):
    """Masked captured-verdict rows - the capture half of scan_shell()."""
    return scan_shell(text, kind or ("workflow" if workflow else "sh"))[2]


# --- the audit -------------------------------------------------------------------

def audit():
    unguarded, guarded = [], []
    for rel in [p for p in tracked("hdl") if p.endswith(".sv") and p not in LINT_EXCLUDE]:
        for name, has_params, has_check in scan_modules(
                (REPO / rel).read_text(errors="replace")):
            if not has_params:
                continue
            unit = f"{rel}:{name}"
            (guarded if has_check else unguarded).append(unit)

    shell = tracked("*.sh", ".github/workflows/*.yml", "syn/**/*.sh", "harness/**/*.sh")
    all_makefiles = tracked("Makefile", "*/Makefile", "*.mk")
    makefiles = [p for p in all_makefiles if not p.startswith(NOT_FIRST_PARTY)]
    population = {"sh": sum(1 for p in shell if p.endswith(".sh")),
                  "workflow": sum(1 for p in shell if p.endswith(".yml")),
                  "makefile": len(makefiles),
                  "vendor_makefiles_excluded": len(all_makefiles) - len(makefiles)}
    masked, waived, captured = [], [], []
    for rel in shell + makefiles:
        text = (REPO / rel).read_text(errors="replace")
        if rel in makefiles:
            kind = "makefile"
        elif rel.startswith(".github/workflows/") or "/.github/workflows/" in rel:
            kind = "workflow"
        else:
            kind = "sh"
        found, exceptions, caught = scan_shell(text, kind, rel)
        masked.extend((rel, n, line) for n, line in found)
        waived.extend((rel, n, why) for n, why in exceptions)
        captured.extend((rel, n, line) for n, line in caught)
    return unguarded, guarded, masked, waived, captured, population


def read_budget():
    if not BUDGET.is_file():
        return None, None
    vals = [int(x) for x in re.findall(r"^\s*(\d+)\s*$", BUDGET.read_text(), re.M)]
    return (vals + [None, None, None])[:3]


def selftest():
    failures = 0
    arms = 0

    def ck(name, ok, detail=""):
        nonlocal failures, arms
        arms += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    # --- modules: which parameter forms count ------------------------------
    ck("a module with parameters and no check is unguarded",
       scan_module("module m #(parameter int W = 8)(); endmodule") == (True, False))
    ck("a module with an elaboration $error is guarded",
       scan_module("module m #(parameter int W = 8)();\n if (W < 2) $error(\"no\");\n"
                   "endmodule") == (True, True))
    ck("a module with no parameters is not counted",
       scan_module("module m (); endmodule") == (False, False))
    for form in ("int unsigned W = 8", "string HEX_P = \"\"", "type T = logic [7:0]",
                 "real R = 1.5", "longint L = 64'd0", "int W", "[3:0] X = 4'd2",
                 "X = 3", "int A = 1, B = 2"):
        ck(f"`parameter {form}` is a parameter",
           scan_module(f"module m #(parameter {form})(); endmodule") == (True, False),
           "the header parser is scripts/sv_ports.py; a private regex saw 53 of 102")
    ck("an $error inside a COMMENT does not count as a guard",
       scan_module("module m #(parameter int W = 8)();\n // $error(\"no\");\n"
                   "endmodule") == (True, False),
       "comments are blanked before the search")
    rows = scan_modules(
        "module guarded #(parameter int A=1)(); if (!A) $error(\"A\"); endmodule\n"
        "module bare #(parameter int B=1)(); endmodule")
    ck("two modules in one file are measured independently",
       rows == [("guarded", True, True), ("bare", True, False)], f"{rows}")

    # --- modules: which $error sites count ---------------------------------
    ck("a runtime $error inside always is NOT an elaboration contract",
       scan_module("module m #(parameter int W=8)(input logic clk);\n"
                   " always @(posedge clk) if (W) $error(\"runtime\");\nendmodule")
       == (True, False), "review: any $error counted, so a runtime assertion emptied the ratchet")
    ck("a $error inside an always_ff begin/end block is not a contract",
       scan_module("module m #(parameter int W=8)(input logic clk);\n"
                   " always_ff @(posedge clk) begin : p\n  if (W) $error(\"r\");\n end : p\n"
                   "endmodule") == (True, False))
    ck("an initial-block $fatal is a simulation check, not an elaboration contract",
       scan_module("module m #(parameter int T_P=0)();\n initial begin : parameter_checks\n"
                   "  if (T_P == 0) $fatal(1, \"T_P must be > 0\");\n end\nendmodule")
       == (True, False), "Verilator builds it, Vivado and Yosys synthesise it; only a run refuses")
    ck("an initial assert ... else $error is not a contract either",
       scan_module("module m #(parameter int D=1)();\n initial begin\n"
                   "  assert (D >= 1) else $error(\"D\");\n end\nendmodule") == (True, False))
    ck("a $error inside a function body is not a contract",
       scan_module("module m #(parameter int W=8)();\n function int f(input int x);\n"
                   "  if (x < 0) $error(\"f\"); return x;\n endfunction\nendmodule")
       == (True, False))
    ck("a module-scope $error in a NAMED generate block is a contract",
       scan_module("module m #(parameter int W=8)();\n if (W < 2) begin : gen_guard\n"
                   "  $error(\"W\");\n end\nendmodule") == (True, True))
    ck("a generate/endgenerate guard is a contract",
       scan_module("module m #(parameter int W=8)();\n generate if (W < 2) begin : g\n"
                   "  $error(\"W\");\n end endgenerate\nendmodule") == (True, True))
    ck("a module-scope $error AFTER an always block is still seen",
       scan_module("module m #(parameter int W=8)(input logic clk, output logic q);\n"
                   " always_ff @(posedge clk) begin q <= ~q; end\n"
                   " if (W < 2) $error(\"W\");\nendmodule") == (True, True),
       "the procedural span must end at its `end`, not at endmodule")
    ck("a single-statement always ends at its `;`",
       scan_module("module m #(parameter int W=8)(input logic clk, output logic q);\n"
                   " always @(posedge clk) q <= ~q;\n if (W < 2) $error(\"W\");\nendmodule")
       == (True, True))
    ck("a single-statement always with an else ends after the else",
       scan_module("module m #(parameter int W=8)(input logic clk, a, output logic q);\n"
                   " always @(posedge clk) if (a) q <= 1; else q <= 0;\n"
                   " if (W < 2) $error(\"W\");\nendmodule") == (True, True))
    ck("a bare initial $readmemh does not swallow the guard after it",
       scan_module("module m #(parameter string F=\"\")();\n logic [7:0] rom [0:3];\n"
                   " initial $readmemh(F, rom);\n if (F == \"\") $error(\"F\");\nendmodule")
       == (True, True))
    ck("the word `always` inside a $error message does not open a procedural block",
       scan_module("module m #(parameter int W=8)();\n"
                   " if (W < 2) $error(\"W is always at least 2\");\nendmodule") == (True, True))

    # --- modules: assertions are simulation-time, whatever scope they sit at --
    ck("a module-scope concurrent `assert property ... else $error` is NOT a contract",
       scan_module("module m #(parameter int W=8)(input logic clk, P);\n"
                   " assert property (@(posedge clk) P) else $error;\nendmodule") == (True, False),
       "review: its action block fires at a clock edge in simulation and cannot refuse a parameter")
    ck("a labelled concurrent assertion with a begin/end action block is not a contract",
       scan_module("module m #(parameter int W=8)(input logic clk, P);\n"
                   " a_p: assert property (@(posedge clk) disable iff (!P) P |-> W > 1)\n"
                   "  else begin $error(\"p\"); end\nendmodule") == (True, False))
    ck("assume property and cover property are not contracts either",
       scan_module("module m #(parameter int W=8)(input logic clk, P);\n"
                   " assume property (@(posedge clk) P) else $error(\"a\");\n"
                   " cover property (@(posedge clk) P) $error(\"c\");\nendmodule") == (True, False))
    ck("a deferred immediate `assert #0 (...) else $error` at module scope is not a contract",
       scan_module("module m #(parameter int W=8)(input logic P);\n"
                   " assert #0 (P) else $error(\"P\");\nendmodule") == (True, False),
       "a deferred assertion is evaluated in the simulator's Observed region; synthesis drops it")
    ck("an `assert final` at module scope is not a contract",
       scan_module("module m #(parameter int W=8)(input logic P);\n"
                   " assert final (P) else $error(\"P\");\nendmodule") == (True, False))
    ck("a $error inside property ... endproperty is not a contract",
       scan_module("module m #(parameter int W=8)(input logic clk, P);\n"
                   " property p; @(posedge clk) P; endproperty\n"
                   " a1: assert property (p) else $error(\"p\");\nendmodule") == (True, False))
    ck("a $error inside sequence ... endsequence is not a contract",
       scan_module("module m #(parameter int W=8)(input logic clk, P);\n"
                   " sequence s; @(posedge clk) P ##1 P; endsequence\n"
                   " cover sequence (s) $error(\"s\");\nendmodule") == (True, False))
    ck("a concurrent assertion NEXT TO a module-scope $error does not hide the guard",
       scan_module("module m #(parameter int W=8)(input logic clk, P);\n"
                   " a1: assert property (@(posedge clk) P) else $error;\n"
                   " if (W < 2) $error(\"W\");\n"
                   " assert property (@(posedge clk) !P) else $error;\nendmodule") == (True, True),
       "the assertion is stepped over whole; the guard beside it is still reached")
    ck("a $error inside an always inside a generate block is still a runtime assertion",
       scan_module("module m #(parameter int W=8)(input logic clk);\n if (W > 1) begin : g\n"
                   "  always @(posedge clk) if (W) $error(\"r\");\n end\nendmodule") == (True, False))

    # --- modules: the generate shapes the positive walk must reach ---------
    ck("a generate-if guard with an else arm is a contract",
       scan_module("module m #(parameter int W=8)();\n generate\n"
                   "  if (W < 2) begin : gen_guard\n   $error(\"W\");\n  end else begin : gen_ok\n"
                   "   wire ok = 1'b1;\n  end\n endgenerate\nendmodule") == (True, True))
    ck("a guard at the end of an else-if chain is a contract",
       scan_module("module m #(parameter int W=8)();\n"
                   " if (W == 8) begin : g8 end else if (W == 16) begin : g16 end\n"
                   " else $error(\"W\");\nendmodule") == (True, True))
    ck("a case-generate default $error is a contract",
       scan_module("module m #(parameter int W=8)();\n case (W)\n  8, 16: begin : ok end\n"
                   "  default: $error(\"W\");\n endcase\nendmodule") == (True, True))
    ck("a guard inside a for-generate body is a contract",
       scan_module("module m #(parameter int N=2)();\n for (genvar i = 0; i < N; i++) begin : g\n"
                   "  if (i > 3) $error(\"N\");\n end\nendmodule") == (True, True))
    ck("a preprocessor directive before a named always block is a line, not a label",
       scan_module("module m #(parameter int W=8)(input logic clk, output logic q);\n"
                   "`ifndef SYNTHESIS\n logic dbg_r;\n`endif\n"
                   " always_ff @(posedge clk) begin : st\n  q <= ~q;\n"
                   "`ifndef SYNTHESIS\n  if (W) $error(\"r\");\n`endif\n end : st\nendmodule")
       == (True, False),
       "KL_gptp_engine: `endif then `begin : st_port` read as a label and the walk entered the block")
    ck("a guard wrapped in `ifdef/`else/`endif is still reached",
       scan_module("module m #(parameter int W=8)();\n`ifdef FOO\n if (W < 2) $error(\"W\");\n"
                   "`else\n if (W < 4) $error(\"W\");\n`endif\nendmodule") == (True, True))
    ck("a guard after a typedef, an instantiation and a DPI import is still reached",
       scan_module("module m #(parameter int W=8)(input logic clk);\n"
                   " import \"DPI-C\" function int f(input int x);\n"
                   " typedef struct packed { logic a; logic b; } t_s;\n"
                   " sub #(.A(1)) u_sub (.clk(clk), .q());\n"
                   " if (W < 2) $error(\"W\");\nendmodule") == (True, True),
       "a plain item runs to its `;`; none of them may swallow what follows")

    # --- pipelines: producers ---------------------------------------------
    ck("a piped gate is masked", scan_pipeline("  python3 scripts/x.py | tee log")[0])
    ck("a piped make is masked", scan_pipeline("  make run | tail -5")[0])
    for cmd in ("$MAKE -C x", "./obj_dir/Vsim +arg", "./lint_hdl.sh", "bash scripts/x.sh",
                "xvlog -sv a.sv", "xelab top", "vivado -mode batch", "iverilog -o a b.v",
                "verilator_coverage --annotate d coverage.dat", "$VERILATOR --lint-only x.sv"):
        ck(f"`{cmd} | tee` is a masked producer", scan_pipeline(f"  {cmd} | tee log")[0],
           "review listed these shapes as unmodelled")
    ck("a fallback is not a pipe", not scan_pipeline("  python3 scripts/x.py || exit 2")[0])
    ck("a comment is not a pipeline", not scan_pipeline("  # python3 x.py | tee log")[0])
    ck("a tool name inside a string is not a producer",
       not scan_pipeline('  printf "yosys FAIL: %s" "$x" | head -1')[0],
       "the match came from a format string, not a command")
    ck("a tool name glued to a suffix is not a producer",
       not scan_pipeline("  ls make.log | head -1")[0])
    ck("a path-qualified tool is a producer",
       scan_pipeline("  /opt/verilator/bin/verilator --version | grep -F 5.050")[0])
    ck("a pipe inside a command substitution is not the line's verdict",
       not scan_pipeline('  msg=$(grep ERROR log | head -1); python3 x.py')[0])
    ck("a pipe inside a parameter expansion is not a pipe",
       not scan_pipeline("  d=${g%%|*}; verilator --lint-only x.sv")[0])
    ck("a group that saves the producer's status before the pipe keeps the verdict",
       not scan_pipeline("  { python3 fuzz.py 2>&1; echo $? > obj/aaf.rc; } | tee obj/aaf.out")[0],
       "tb/verilator/tsn_fuzz reads the .rc back on the next line")
    ck("a file-reading grep piped to head is a producer whose status is lost",
       scan_pipelines('set -e\ngrep -A2 "Slice LUTs\\|DSPs" ucpu_util.rpt | head -20\n')[0]
       == [(2, 'grep -A2 "Slice LUTs\\|DSPs" ucpu_util.rpt | head -20')],
       "a missing report makes grep fail and head succeed: the flow exits 0")
    ck("a file-reading cat piped to a consumer is the same shape",
       scan_pipeline("cat engine_util.rpt | tail -3")[0])
    ck("grep reading stdin is a consumer, not a producer",
       not scan_pipeline('echo "$out" | grep -q FAIL')[0])
    ck("a bare grep pattern with no file reads stdin and is not a producer",
       not scan_pipeline("grep foo | head -1")[0])
    ck("an ordinary command is not a pipeline",
       not scan_pipeline("  python3 scripts/x.py")[0])

    # --- pipelines: the shell model ----------------------------------------
    ck("a line that sets pipefail is not masked",
       not scan_pipelines("set -o pipefail\npython3 x.py | tee log")[0])
    ck("the file-reading grep is protected once pipefail is on",
       not scan_pipelines("set -eo pipefail\ngrep x rpt | head\n")[0])
    ck("a later pipefail cannot protect an earlier pipeline",
       scan_pipelines("python3 x.py | tee log\nset -o pipefail")[0] ==
       [(1, "python3 x.py | tee log")])
    ck("a pipefail mentioned in a COMMENT protects nothing",
       scan_pipelines("# note: set -o pipefail is not used here\npython3 gate.py | tee log")[0]
       == [(2, "python3 gate.py | tee log")], "comments are blanked before the search")
    ck("a pipefail inside a here-document body protects nothing",
       scan_pipelines("cat <<EOF\nset -o pipefail\nEOF\npython3 gate.py | tee log")[0]
       == [(4, "python3 gate.py | tee log")])
    ck("a pipefail set inside a subshell ends with the subshell",
       scan_pipelines("(set -o pipefail; make | tee a)\nmake | tee b")[0]
       == [(2, "make | tee b")], "the pipeline inside the subshell is protected; the next is not")
    ck("a multi-line subshell scopes its pipefail the same way",
       scan_pipelines("(\n  set -o pipefail\n  make | tee a\n)\nmake | tee b")[0]
       == [(5, "make | tee b")])
    ck("a backslash-continued pipeline is one line, found at its first line",
       scan_pipelines("make -C x \\\n  | tee log")[0] == [(1, "make -C x | tee log")])
    ck("a shebang carrying -eo pipefail protects the script",
       not scan_pipelines("#!/bin/bash -eo pipefail\nmake | tee log")[0])
    ck("a plain shebang protects nothing",
       scan_pipelines("#!/usr/bin/env bash\nmake | tee log")[0] == [(2, "make | tee log")])
    ck("the GitHub Actions default run shell has NO pipefail",
       scan_pipelines("    - name: s\n      run: |\n        python3 x.py | tee log\n",
                      workflow=True)[0] == [(3, "python3 x.py | tee log")],
       "GitHub's default is `bash -e {0}`; only `shell: bash` adds pipefail")
    ck("a step that declares shell: bash is protected, before or after its run block",
       not scan_pipelines("    - name: s\n      run: |\n        python3 x.py | tee log\n"
                          "      shell: bash\n", workflow=True)[0])
    ck("pipefail set in one step does not protect the next step",
       scan_pipelines("    - run: |\n        set -euo pipefail\n        python3 a.py | tee a\n"
                      "    - run: |\n        python3 b.py | tee b\n", workflow=True)[0]
       == [(5, "python3 b.py | tee b")])

    # --- pipelines: Makefile recipes --------------------------------------
    mk = ("VERILATOR ?= verilator\nPY = python3\n\ncov:\n"
          "\tverilator_coverage --annotate d --annotate-min 1 coverage.dat \\\n"
          "\t    | tail -2\n"
          "\t$(VERILATOR) --lint-only x.sv | tee lint.log\n"
          "\t$(MAKE) -C sub | tee sub.log\n"
          "\t$(PY) gate.py || exit 1\n"
          "X = a | b\n")
    ck("a Makefile recipe pipe runs under /bin/sh -c with no pipefail and is masked",
       scan_pipelines(mk, kind="makefile")[0] == [
           (5, "verilator_coverage --annotate d --annotate-min 1 coverage.dat | tail -2"),
           (7, "verilator --lint-only x.sv | tee lint.log"),
           (8, "make -C sub | tee sub.log")],
       f"make variables must expand to their tools; got {scan_pipelines(mk, kind='makefile')[0]}")
    ck("a Makefile whose .SHELLFLAGS carries pipefail protects its recipes",
       not scan_pipelines(".SHELLFLAGS = -eo pipefail -c\nt:\n\tmake -C sub | tee log\n",
                          kind="makefile")[0])
    ck("a `$$(...)` in a recipe is the shell's substitution, not a make variable",
       scan_substitutions("t:\n\tout=$$(python3 gen.py); grep ok <<<$$out\n", kind="makefile")
       == [(2, "out=$(python3 gen.py); grep ok <<<$out")])

    # --- captured verdicts -------------------------------------------------
    ck("a captured verdict with no errexit and no guard is discarded",
       scan_substitutions("set -u\nout=$(verilator --lint-only -Wall \\\n  $pkgs $all 2>&1)\n"
                          "if echo \"$out\" | grep -q Error; then rc=1; fi\n")
       == [(2, "out=$(verilator --lint-only -Wall $pkgs $all 2>&1)")],
       "a silent non-zero verilator prints nothing, matches nothing, reads as OK")
    ck("the same capture under errexit is not discarded",
       not scan_substitutions("set -eu\nout=$(verilator --lint-only x.sv 2>&1)\n"))
    ck("errexit switched off later un-protects a later capture",
       scan_substitutions("set -e\nset +e\nout=$(make lint)\n") == [(3, "out=$(make lint)")])
    ck("a local/export assignment discards the status even under errexit",
       scan_substitutions("set -e\nf() {\n  local out=$(make lint)\n}\n") == [(3, "local out=$(make lint)")]
       and scan_substitutions("set -e\nexport OUT=$(python3 x.py)\n") == [(2, "export OUT=$(python3 x.py)")],
       "the builtin's status is what the shell sees")
    ck("a capture whose status is consulted is not discarded",
       not scan_substitutions("x=$(python3 y.py) || exit 2\n")
       and not scan_substitutions("if ! x=$(python3 y.py); then exit 2; fi\n"))
    ck("a capture whose $? is read on the next line is not discarded",
       not scan_substitutions("out=$($VERILATOR --lint-only x.sv 2>&1)\n"
                              "if [ $? -ne 0 ] || echo \"$out\" | grep -q Error; then rc=1; fi\n"),
       "protocol-processor/tb/timer_map/shape_elab.sh reads it immediately")
    ck("a capture through a tool VARIABLE is a capture",
       scan_substitutions("set -u\nout=$($VERILATOR --lint-only x.sv 2>&1)\n"
                          "if echo \"$out\" | grep -q OVERLAP; then ok=1; fi\n")
       == [(2, "out=$($VERILATOR --lint-only x.sv 2>&1)")])
    ck("an argument-form substitution is the consumer's verdict and is not modelled",
       not scan_substitutions('echo "rtl=$(python3 scripts/ci_scope.py)" >> "$OUT"\n'))
    ck("a workflow step starts with errexit, so a bare capture there is not discarded",
       not scan_substitutions("    - run: |\n        rtl=\"$(python3 scripts/ci_scope.py)\"\n",
                              workflow=True))
    ck("a capture inside a comment is not a finding",
       not scan_substitutions("set -u\n# out=$(verilator x)\n"))
    ck("a capture inside a subshell that set errexit is protected only there",
       scan_substitutions("(set -e; a=$(make x))\nb=$(make y)\n") == [(2, "b=$(make y)")])

    # --- waivers -------------------------------------------------------------
    site_path, site_text, site_why = INTENTIONAL[0]
    ck("the version assertion is waived by SITE, with a reason",
       scan_pipelines(f"    - run: |\n        {site_text}\n", workflow=True, rel=site_path)
       == ([], [(2, site_why)]))
    ck("the same line at another path is masked, not waived",
       scan_pipelines(f"    - run: |\n        {site_text}\n", workflow=True, rel="scripts/x.yml")
       == ([(2, site_text)], []))
    ck("a NEW `--version | grep` is masked: the waiver is not a substring",
       scan_pipelines('yosys --version | grep -q "0.0"\n', rel="scripts/run_all_suites.sh")[0]
       == [(1, 'yosys --version | grep -q "0.0"')],
       "review bypassed the ratchet by adding --version to a gate's arguments")
    ck("a gate verdict carrying --version is masked, not waived",
       scan_pipelines("python3 scripts/lint_rtl.py --check --version | grep -c FAIL\n",
                      rel="scripts/run_all_suites.sh")[0]
       == [(1, "python3 scripts/lint_rtl.py --check --version | grep -c FAIL")])
    ck("an unterminated here-document makes the unit unreadable, never a pass",
       _raises(Unreadable, scan_pipelines, "cat <<EOF\nset -o pipefail\nmake | tee log\n"),
       "a partial population is not a pass; the CLI exits 2")

    # --- the live tree --------------------------------------------------------
    unguarded, guarded, masked, waived, captured, population = audit()
    ck("the live scan reads the tree", len(unguarded) + len(guarded) > 80,
       f"{len(unguarded)} + {len(guarded)} modules with parameters")
    ck("the guarded set is not empty", len(guarded) >= 4,
       "an inert scan would report every module unguarded")
    ck("the gptp-processor modules in the `int unsigned`/`string` idiom are in the population",
       all(any(u.endswith(":" + m) for u in unguarded)
           for m in ("KL_gptp_timer", "KL_gptp_ucpu", "KL_gptp_tx_slot")),
       "review: the first regex saw none of gptp-processor")
    ck("KL_media_nco, the house form the guide cites, is counted guarded",
       any(u.endswith(":KL_media_nco") for u in guarded))
    ck("every site waiver names a line that exists and is masked without it",
       sorted((rel, why) for rel, _n, why in waived) == sorted((p, w) for p, _t, w in INTENTIONAL),
       f"waived {[(r, n) for r, n, _ in waived]} vs {len(INTENTIONAL)} sites - a stale waiver "
       "must be removed")
    ck("the live scan reaches both processor submodules' shell wrappers",
       any(rel.startswith("gptp-processor/") for rel, _, _ in masked + captured) and
       any(rel.startswith("protocol-processor/") for rel, _, _ in masked + captured),
       f"masked {[r for r, _, _ in masked]}, captured {[r for r, _, _ in captured]}")
    ck("the Makefile population is first-party only and not empty",
       population["makefile"] > 50
       and not any(rel.startswith(NOT_FIRST_PARTY) for rel, _, _ in masked + captured)
       and [p for p in ("third_party/verilog-axis/tb/Makefile", "external/x/Makefile",
                        "docs/history/v1/tb/Makefile", "tb/verilator/cbs/Makefile")
            if not p.startswith(NOT_FIRST_PARTY)] == ["tb/verilator/cbs/Makefile"],
       f"{population} - a vendor or archive Makefile must never join the population, "
       "whichever layer drops it")

    print(f"\n{arms} checks: {arms - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def _raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet all three counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    try:
        unguarded, guarded, masked, waived, captured, population = audit()
    except Unreadable as exc:
        print(f"UNREADABLE POPULATION: {exc}")
        return 2

    print(f"parameterised modules with no elaboration contract "
          f"({len(unguarded)} of {len(unguarded) + len(guarded)}):")
    for rel in unguarded:
        print(f"   {rel}")
    print(f"\nmeasured shell population: {population['sh']} shell scripts, "
          f"{population['workflow']} workflow files, {population['makefile']} Makefiles "
          f"(recipe lines); Python and Tcl are not measured")
    print(f"\npipelines that discard their producer's exit code ({len(masked)}):")
    for rel, n, line in masked:
        print(f"   {rel}:{n}  {line}")
    print(f"\ncaptured verdicts whose exit status is discarded ({len(captured)}):")
    for rel, n, line in captured:
        print(f"   {rel}:{n}  {line}")
    print(f"\nwaived by site, with a reason ({len(waived)}):")
    for rel, n, why in waived:
        print(f"   {rel}:{n}  {why}")

    if not args.check:
        return 0

    b_unguarded, b_masked, b_captured = read_budget()
    if b_unguarded is None or b_masked is None or b_captured is None:
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} must hold three counts")
        return 1
    bad = False
    if len(unguarded) > b_unguarded:
        print(f"\nFAIL: {len(unguarded)} module(s) without an elaboration contract "
              f"> ratchet {b_unguarded}. A new parameter states what it refuses.")
        bad = True
    if len(masked) > b_masked:
        print(f"\nFAIL: {len(masked)} masked pipeline(s) > ratchet {b_masked}. "
              f"A verdict must not be piped away.")
        bad = True
    if len(captured) > b_captured:
        print(f"\nFAIL: {len(captured)} captured verdict(s) discarded > ratchet "
              f"{b_captured}. A tool's exit status is the verdict; its text is not.")
        bad = True
    if bad:
        return 1
    print(f"\nFAIL-FAST RATCHET: PASS ({len(unguarded)} <= {b_unguarded} modules "
          f"without an elaboration contract, {len(masked)} <= {b_masked} masked "
          f"pipeline(s), {len(captured)} <= {b_captured} discarded captured "
          f"verdict(s), {len(waived)} waived by site)")
    if len(unguarded) < b_unguarded or len(masked) < b_masked or len(captured) < b_captured:
        print(f"  the ratchets can be lowered to {len(unguarded)}, {len(masked)} "
              f"and {len(captured)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
