#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Fixture arms for ``measure_fail_fast.py`` - one arm per shape it reads.

This is the ``--selftest`` half of the Rule 6 measurement, kept beside it
rather than inside it: the arms are one long list of independent fixtures and
they share no reader with the rules they exercise. Run them through the
measurement, which is the only supported entry point:

    python3 scripts/measure_fail_fast.py --selftest

``run_arms()`` prints one line per arm in the order the groups below are
called, then the totals, and returns the exit code. Adding an arm to the END
of its group is what keeps the printed transcript stable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from measure_fail_fast import (  # noqa: E402
    INTENTIONAL,
    NOT_FIRST_PARTY,
    Unreadable,
    audit,
    scan_module,
    scan_modules,
    scan_pipeline,
    scan_pipelines,
    scan_substitutions,
)


def _raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return True
    return False


class _Tally:
    """The self-test's running verdict: one line per arm, and the totals."""

    def __init__(self):
        self.arms = 0
        self.failures = 0

    def ck(self, name: str, ok: bool, detail: str = "") -> None:
        """Record and print one arm's verdict, with its detail when it fails."""
        self.arms += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            self.failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")


def _arms_module_parameters(ck):
    """Which parameter forms put a module in the population at all."""
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


def _arms_error_sites(ck):
    """Which $error sites are an elaboration contract and which are runtime."""
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


def _arms_assertions_are_runtime(ck):
    """Assertions are simulation-time at every scope, and never a contract."""
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


def _arms_generate_shapes(ck):
    """The generate shapes the positive walk has to reach to find a guard."""
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


def _arms_pipeline_producers(ck):
    """Which command in a pipeline is the producer whose status is lost."""
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


def _arms_shell_model(ck):
    """The pipefail model: where it is set, and how far its protection reaches."""
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


def _arms_makefile_recipes(ck):
    """A recipe runs under /bin/sh -c, so its pipes mask unless .SHELLFLAGS says not."""
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


def _arms_captured_verdicts(ck):
    """A captured verdict nobody consults, and the guards that rescue one."""
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


def _arms_waivers(ck):
    """A site waiver covers one line at one path, and never by substring."""
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


def _arms_live_tree(ck):
    """The live scan: the population it reaches, and the waivers it still needs."""
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


def run_arms() -> int:
    """Run every arm, print the transcript, and return the exit code."""
    tally = _Tally()
    for group in (_arms_module_parameters, _arms_error_sites,
                  _arms_assertions_are_runtime, _arms_generate_shapes,
                  _arms_pipeline_producers, _arms_shell_model,
                  _arms_makefile_recipes, _arms_captured_verdicts,
                  _arms_waivers, _arms_live_tree):
        group(tally.ck)
    print(f"\n{tally.arms} checks: {tally.arms - tally.failures} PASS, "
          f"{tally.failures} FAIL")
    return 1 if tally.failures else 0
