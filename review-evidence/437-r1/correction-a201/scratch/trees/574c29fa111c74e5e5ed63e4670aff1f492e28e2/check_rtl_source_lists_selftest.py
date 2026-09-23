#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arms for ``check_rtl_source_lists.py`` - the drift gate's own tests.

This is the ``--selftest`` half of the source-list drift gate, kept beside it
rather than inside it: the arms are one long list of independent fixtures and
they share no reader with the closure and consumer rules they exercise. Run
them through the gate, which is the only supported entry point:

    python3 scripts/check_rtl_source_lists.py --selftest

Every arm removes or breaks something and demands the right complaint, so each
fails when the defect it guards is put back. ``run_arms()`` prints one line per
arm in the order the groups below are called, then the totals, and returns the
exit code. Adding an arm to the END of its group keeps the transcript stable.

The imports below reach two of the gate's private consumer readers on purpose:
these arms exist to run the shipped emit paths, not copies of them.
"""

import re
import subprocess
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_rtl_source_lists import (  # noqa: E402
    CONSUMERS,
    INST_RE,
    PACKAGE_REF_RE,
    REPO,
    SOC,
    TOPS_BUDGET,
    Answer,
    Consumer,
    Row,
    _from_make,
    _from_vivado_list,
    audit,
    compare_tops,
    declaration_index,
    declared_modules,
    default_goal_is_print_srcs,
    drop_source_token,
    module_file,
    mutated_copy,
    parse_tops_array,
    processor_tops_audit,
    read_tops_budget,
    spliced,
    units_by_file,
    verdict,
)


def _probe_children(path, extra_index=None):
    """The direct children the walk derives from one unit file - the same
    derivation `closure()` applies at every node, run on a copy so the tree is
    never edited. `extra_index` adds fixture declarations to the lookup."""
    index = dict(declaration_index())
    index.update(extra_index or {})
    interfaces = [n for n, (kind, _p) in index.items() if kind == "interface"]
    text, included, _bad = spliced(Path(path))
    children = set(INST_RE.findall(text))
    children |= {n for n in PACKAGE_REF_RE.findall(text)
                 if index.get(n, (None,))[0] == "package"}
    children |= {n for n in interfaces if re.search(r"\b" + re.escape(n) + r"\b", text)}
    for inc in included:
        children |= set(units_by_file().get(inc.resolve(), ()))
    return {c for c in children if c in index}


class _Tally:
    """The self-test's running verdict: one line per arm, and the totals."""

    def __init__(self):
        self.checks = 0
        self.failures = 0

    def ck(self, name: str, ok: bool, detail: str = "") -> None:
        """Record and print one arm's verdict, with its detail when it fails."""
        self.checks += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            self.failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")


def _arms_closure_shape(ck, cl, need):
    """The live closure: non-empty, resolved, transitive, and complete."""
    modules = cl.units
    ck("the closure is non-empty", len(need) > 5, f"got {len(need)} file(s)")
    ck("the closure resolves every module it names", not cl.unresolved,
       f"unresolved: {sorted(cl.unresolved)}")
    ck("every `include in the closure resolves to a file", not cl.bad_includes,
       f"unresolved includes: {cl.bad_includes}")
    ck("the closure is transitive, not one hop",
       "KL_aaf_latency_taps" in modules,
       "a module instantiated by a CHILD of milan_datapath must be in the closure")
    ck("a declared child needs no approved naming prefix",
       "timestamp_counter" in modules,
       "the closure must follow declarations, not silently omit a new name "
       "family (timestamp_counter carries no KL_ prefix)")
    ck("package dependencies are part of the file closure",
       "pp_pkg" in modules and "ethernet_packet_pkg" in modules,
       "removing a package-only source must fail before compilation")
    ck("interface dependencies are part of the file closure",
       "axi_stream_if" in modules,
       "an interface declaration is a source dependency even though it is not a module")
    ck("a module sharing another module's file needs no entry of its own",
       modules.get("KL_aaf_latency_chain") == modules.get("KL_aaf_latency_taps")
       and modules.get("KL_aaf_latency_chain") is not None,
       "two modules in one file must resolve to ONE required file")


def _arms_instantiation_shapes(ck):
    """Each instantiation shape the walk must follow, on a copy of the datapath."""
    # THE SHAPES, on a copy of the live datapath: each probe is the exact
    # instantiation shape the round-2 review inserted, and the walk over the
    # copy must reach the probed module. The probes name real declared modules
    # that milan_datapath does not otherwise reach.
    dp = REPO / "hdl/milan/milan_datapath.sv"
    base = dp.read_text()
    end = base.rfind("endmodule")
    probes = (
        # The shaper chain that instantiated traffic_class_map at column 0 left
        # milan_datapath with #259, so the shape is probed on a copy; the module
        # is still declared in the tree.
        ("a column-0 instantiation is followed (traffic_class_map at column 0)",
         "\n\ntraffic_class_map u_zz_col0_plain ();\n", "traffic_class_map"),
        ("a column-0 instantiation under a non-blank line is followed",
         "\nassign zz_probe_a = 1'b0;\nKL_aes3_tx u_zz_col0 ();\n", "KL_aes3_tx"),
        ("a tab-indented instantiation under a non-blank line is followed",
         "\nassign zz_probe_b = 1'b0;\n\tKL_aes3_rx u_zz_tab ();\n", "KL_aes3_rx"),
        ("an arrayed instance is followed",
         "\n  KL_lat_history_ring u_zz_arr [1:0] ();\n", "KL_lat_history_ring"),
        ("an interface used through a modport not named master/slave/monitor is followed",
         "\n  zz_probe_if.tx zz_bus2;\n", "zz_probe_if"),
    )
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "zz_probe_if.sv").write_text(
            "interface zz_probe_if;\n  logic x;\n  modport tx (output x);\nendinterface\n")
        (d / "zz_probe_body.svh").write_text("KL_aes3_tx u_zz_inc ();\n")
        for name, insert, want in probes:
            (d / "milan_datapath.sv").write_text(base[:end] + insert + base[end:])
            got = _probe_children(d / "milan_datapath.sv", extra_index={
                "zz_probe_if": ("interface", d / "zz_probe_if.sv")})
            ck(name, want in got, f"the walk over the copy reached {sorted(got & {want})}")
            ok_decl = want == "zz_probe_if" or module_file(want) is not None
            if not ok_decl:
                ck(f"probe module {want} is declared in the tree", False)
        (d / "milan_datapath.sv").write_text(
            base[:end] + "\n`include \"zz_probe_body.svh\"\n" + base[end:])
        got = _probe_children(d / "milan_datapath.sv")
        ck("an instantiation inside an included body is followed",
           "KL_aes3_tx" in got, f"got {sorted(got)}")


def _arms_consumer_mutation(ck, need, rows):
    """Removing one closure file from a COPY of each consumer must be reported."""
    reached = [r for r in rows if r.kind == "ok"]
    ck("every consumer answered, so the arms below grade all of them",
       len(reached) == len(rows),
       "; ".join(f"{r.label}: {r.why}" for r in rows if r.kind != "ok"))

    # THE MUTATION, through each consumer's OWN emit path. Copy the consumer,
    # remove one closure file from the copy, ask the copy. Set arithmetic on
    # an already-fetched list would pass with every fetcher stubbed to return
    # the closure; this cannot.
    before = {c.source: (REPO / c.source).read_bytes() for c in CONSUMERS}
    bitten, reasons = [], []
    for c in CONSUMERS:
        real = c.fetch()
        if real.kind != "ok":
            continue
        text = (REPO / c.source).read_text()
        victim = next((f for f in sorted(need & real.files)
                       if drop_source_token(text, Path(f).name) != text), None)
        if victim is None:
            reasons.append(f"{c.label}: no closure file is literal in {c.source}")
            continue
        with mutated_copy(c, Path(victim).name) as copy:
            mutated = c.fetch(copy) if copy else None
        if mutated is None or mutated.kind != "ok":
            reasons.append(f"{c.label}: the mutated copy could not answer: "
                           f"{mutated.why if mutated else 'no copy'}")
        elif victim in mutated.files:
            reasons.append(f"{c.label}: removed '{victim}' from a copy of {c.source} "
                           f"and its emit path still lists it")
        elif mutated.files | {victim} != real.files:
            reasons.append(f"{c.label}: the removal was not surgical, differs in "
                           f"{sorted((mutated.files ^ real.files) - {victim})}")
        else:
            bitten.append(c.label)
    ck("removing one file from a COPY of each consumer is reported by that consumer's own emit path",
       len(bitten) == len(reached) and not reasons, "; ".join(reasons))
    stray = [p.name for p in (REPO / "syn/yosys").iterdir() if p.name.startswith(".selftest-")]
    ck("the mutation arm left every consumer byte-identical and no copy behind",
       all((REPO / c.source).read_bytes() == before[c.source] for c in CONSUMERS)
       and not stray, f"stray {stray}")


def _arms_vivado_row_comment(ck, need):
    """A commented-out Vivado row carries no files, however the text reads."""
    # the Vivado escape class the round-2 review ran: a row commented out is
    # still text, and a text regex still counted it. The reader is imported
    # from check_soc_sources.py; this arm proves the consumer above it uses it.
    soc_text = SOC.read_text()
    row = next((l for l in soc_text.splitlines()
                if '"hdl/common/cdc_handshake.sv"' in l), None)
    with tempfile.TemporaryDirectory() as td:
        copy = Path(td) / "milan_soc.py"
        copy.write_text(soc_text.replace(row, "#" + row, 1) if row else soc_text)
        answer = _from_vivado_list(copy)
    ck("commenting out a row of the Vivado list removes its files from what the consumer carries",
       row is not None and answer.kind == "ok"
       and "hdl/common/cdc_handshake.sv" in need
       and "hdl/common/cdc_handshake.sv" not in answer.files,
       f"row {row!r}, kind {answer.kind}, carried "
       f"{'hdl/common/cdc_handshake.sv' in (answer.files or set())}")


def _arms_asking_is_not_doing(ck, cl, need):
    """Asking a consumer must not run it, and a defect must reach the exit code."""
    # ASKING must not become DOING, and a consumer that cannot answer, or that
    # answers with a defect, must reach the exit code. Fixture makefiles run
    # through the real _from_make and the real verdict.
    with tempfile.TemporaryDirectory() as td:
        good = Path(td) / "good"; good.mkdir()
        (good / "Makefile").write_text(
            ".PHONY: all print-srcs\nall:\n\t@echo ran\nprint-srcs:\n\t@echo a.sv\n")
        bad = Path(td) / "bad"; bad.mkdir()
        (bad / "Makefile").write_text(
            ".PHONY: all print-srcs\nprint-srcs:\n\t@echo a.sv\nall:\n\t@echo ran\n")
        broken = Path(td) / "broken"; broken.mkdir()
        (broken / "Makefile").write_text(
            ".PHONY: all print-srcs\nall:\n\t@echo ran\nprint-srcs:\n\t@false\n")
        ck("a correctly ordered makefile is accepted",
           default_goal_is_print_srcs(good, good / "Makefile") is False)
        ck("print-srcs as the default goal is caught",
           default_goal_is_print_srcs(bad, bad / "Makefile") is True,
           "a bare make would print the list instead of running the suite")
        complete = Consumer("fixture complete list",
                            lambda copy=None: Answer(set(need), "ok", None), "-", False)
        goal = Consumer("fixture default-goal suite",
                        lambda copy=None: _from_make("milan_dp", bad / "Makefile"),
                        "-", False)
        dead = Consumer("fixture emit path that fails",
                        lambda copy=None: _from_make("milan_dp", broken / "Makefile"),
                        "-", False)
        _cl, _need, r_goal = audit((complete, goal))
        rc, lines = verdict(cl, need, r_goal, [])
        ck("a default-goal regression through the real emit path exits 1",
           rc == 1 and any(l.startswith("DEFAULT GOAL") for l in lines),
           f"rc {rc}: {lines}")
        rc, _ = verdict(cl, need, r_goal, [], allow_skip=True)
        ck("a diagnosed defect is never skippable", rc == 1, f"rc {rc}")
        _cl, _need, r_dead = audit((complete, dead))
        rc, lines = verdict(cl, need, r_dead, [])
        ck("an emit path that fails exits 2 by default",
           rc == 2 and any(l.startswith("CANNOT ASK") for l in lines),
           f"rc {rc}: {lines}")
        rc, lines = verdict(cl, need, r_dead, [], allow_skip=True)
        ck("--allow-skip turns it into a loud SKIPPED marker and a covered verdict",
           rc == 0 and any(l.startswith("!! SKIPPED") for l in lines)
           and any("NOT covered" in l for l in lines), f"rc {rc}: {lines}")
        _cl, _need, r_only_dead = audit((dead,))
        rc, _ = verdict(cl, need, r_only_dead, [], allow_skip=True)
        ck("a run in which every consumer was skipped is not a pass", rc == 2, f"rc {rc}")
        _cl, _need, r_complete = audit((complete,))
        tops_gone = [("protocol-processor", "syn/yosys/run.sh", set(), set(), [], [], [],
                      "protocol-processor/syn/yosys/run.sh is absent at this pin")]
        rc, lines = verdict(cl, need, r_complete, tops_gone)
        ck("a processor tops list that cannot be read exits 2 by default",
           rc == 2 and any(l.startswith("CANNOT ASK") for l in lines), f"rc {rc}: {lines}")
        rc, lines = verdict(cl, need, r_complete, tops_gone, allow_skip=True)
        ck("--allow-skip skips an unreadable tops list loudly and covers the rest",
           rc == 0 and any(l.startswith("!! SKIPPED") for l in lines), f"rc {rc}: {lines}")


def _arms_closure_is_a_walk(ck, need):
    """The closure is an instantiation walk, not a listing of hdl/."""
    # the closure is a WALK: it must not be every file in the tree
    every = {p.relative_to(REPO).as_posix() for p in (REPO / "hdl").rglob("*.sv")}
    ck("the closure is a walk, not a directory listing", bool(every - need),
       "the closure covers every .sv under hdl/ - the instantiation walk is inert")


def _arms_processor_tops_fixtures(ck, cl, need):
    """The processor tops array read as bash reads it, on known-answer fixtures."""
    # THE PROCESSOR-NATIVE LIST. Fixtures whose answer is known by construction,
    # then the live pin, where the budget must name exactly the drift and
    # nothing else.
    tops = parse_tops_array("set -eu\ntops=(KL_a KL_b\n      KL_c)\nwork=x\n")
    ck("a multi-line tops array is read whole", tops == {"KL_a", "KL_b", "KL_c"},
       f"got {tops}")
    ck("a script without a tops array is told apart from an empty one",
       parse_tops_array("set -eu\nfor t in a b; do :; done\n") is None)
    # THE ARRAY IS READ AS BASH READS IT. The fixture below is the PR #277
    # review's: split() on the raw body returned `#`, `KL_a`, `KL_b`, bash runs
    # only KL_a, and the commented-out top passed as covered. Each fixture's
    # answer is known by construction, and bash itself is the oracle for all
    # of them (the literals are constants here; the processor's script is
    # never run, because its expansion path is Yosys).
    bash_fixtures = (
        ("a commented-out top is not covered: the review's fixture",
         "tops=(KL_a\n # KL_b\n)\n", {"KL_a"}),
        ("a quoted name is unquoted and covered",
         "tops=('KL_a' \"KL_b\")\n", {"KL_a", "KL_b"}),
        ("an inline comment after a name runs to the end of its line only",
         "tops=(KL_a # KL_b retired\n KL_c)\n", {"KL_a", "KL_c"}),
        ("a `#` that does not start a word is not a comment, quoted or bare",
         "tops=(\"KL_a#x\" 'KL_b#y' KL_c#z)\n", {"KL_a#x", "KL_b#y", "KL_c#z"}),
        ("a `)` inside a comment or quotes does not close the array",
         "tops=(KL_a # (was KL_b)\n 'KL_c)' KL_d)\n", {"KL_a", "KL_c)", "KL_d"}),
    )
    for name, fixture, want in bash_fixtures:
        got = parse_tops_array(fixture)
        ck(name, got == want, f"got {got}")
    fx_tops = parse_tops_array(bash_fixtures[0][1])
    ck("the commented-out top is refused as unrecorded, not credited",
       compare_tops(fx_tops, {"KL_a", "KL_b"}, {}) == (["KL_b"], []),
       f"got {compare_tops(fx_tops, {'KL_a', 'KL_b'}, {})}")
    fx_row = ("protocol-processor", "syn/yosys/run.sh", fx_tops, {"KL_a", "KL_b"},
              [], *compare_tops(fx_tops, {"KL_a", "KL_b"}, {}), None)
    rc, lines = verdict(cl, need, [Row("fixture complete list", "ok", [], [], None)],
                        [fx_row])
    ck("the commented-out top reaches the verdict as TOPS DRIFT and exit 1",
       rc == 1 and any(l.startswith("TOPS DRIFT") and "KL_b" in l for l in lines),
       f"rc {rc}: {lines}")
    oracle = []
    for name, fixture, want in bash_fixtures:
        run = subprocess.run(["bash", "-c", fixture + 'printf "%s\\n" "${tops[@]}"'],
                             capture_output=True, text=True)
        said = set(run.stdout.splitlines()) if run.returncode == 0 else None
        if said != want:
            oracle.append(f"{name}: bash said {said}, the fixture expects {want}")
    ck("bash itself reads every fixture the way the parser does",
       not oracle, "; ".join(oracle))
    ck("an array that is never closed is refused, not read to the end of the file",
       parse_tops_array("tops=(KL_a\n # KL_b)\n") is None)
    declared = declared_modules(
        "package p_pkg; endpackage\nmodule KL_a; endmodule\n"
        "interface bus_if; endinterface\n  module KL_new #(parameter W=1)(); endmodule\n")
    ck("declarations are modules only - packages and interfaces are not tops",
       declared == {"KL_a", "KL_new"}, f"got {declared}")
    ck("adding a declared module that the tops array does not name is refused",
       compare_tops({"KL_a"}, {"KL_a", "KL_new"}, {}) == (["KL_new"], []))
    ck("a recorded omission is debt, not a refusal",
       compare_tops({"KL_a"}, {"KL_a", "KL_new"}, {"KL_new": "drift"}) == ([], []))
    ck("a recorded name that became a top is refused as stale",
       compare_tops({"KL_a", "KL_new"}, {"KL_a", "KL_new"}, {"KL_new": "drift"})
       == ([], ["KL_new"]))
    ck("removing a declared module from the tops array is refused",
       compare_tops({"KL_a"}, {"KL_a", "KL_b"}, {}) == (["KL_b"], []),
       "a top dropped from the array is exactly the drift the gate exists for")
    budget = read_tops_budget("# c\nKL_x  why x\n\nKL_y why y # trailing\n")
    ck("the budget names each omission with its reason",
       budget == {"KL_x": "why x", "KL_y": "why y"}, f"got {budget}")


def _arms_processor_tops_live(tally, cl, need):
    """The live processor pin: the budget names exactly the drift and no more."""
    ck = tally.ck
    live = [r for r in processor_tops_audit() if r[7] is None]
    ck("the live processor tops array was read", bool(live) and len(live[0][2]) >= 30,
       "no PROCESSOR_TOPS entry was reachable, or the array parsed as nearly empty")
    if live:
        sub, script, l_tops, l_decl, l_rec, l_unrec, l_stale, _ = live[0]
        ck("every recorded omission is real drift at this pin, and every drift is recorded",
           not l_unrec and not l_stale,
           f"unrecorded {l_unrec}, stale {l_stale}")
        ck("the record is non-empty at this pin, so the refusal arms grade a live population",
           bool(l_rec), "an empty record would make the stale/unrecorded arms vacuous here")
        mutated = compare_tops(l_tops, l_decl | {"KL_zz_probe"},
                               read_tops_budget(TOPS_BUDGET.read_text()))
        ck("a new declared processor module is refused by the live comparison",
           mutated[0] == ["KL_zz_probe"], f"got {mutated}")
    else:
        tally.failures += 3
        tally.checks += 3


def run_arms() -> int:
    """Run every arm, print the transcript, and return the exit code."""
    tally = _Tally()
    ck = tally.ck
    cl, need, rows = audit()
    _arms_closure_shape(ck, cl, need)
    _arms_instantiation_shapes(ck)
    _arms_consumer_mutation(ck, need, rows)
    _arms_vivado_row_comment(ck, need)
    _arms_asking_is_not_doing(ck, cl, need)
    _arms_closure_is_a_walk(ck, need)
    _arms_processor_tops_fixtures(ck, cl, need)
    _arms_processor_tops_live(tally, cl, need)
    print(f"\n{tally.checks} checks: {tally.checks - tally.failures} PASS, "
          f"{tally.failures} FAIL")
    return 1 if tally.failures else 0
