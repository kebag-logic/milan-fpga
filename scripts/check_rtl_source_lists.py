#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: every list that compiles `milan_datapath` carries every module it needs.

Why this exists, with the receipts. There are FIVE independent lists of the
same RTL - the Vivado sources in `sw/litex/milan_soc.py`, the `milan_datapath`
row in `syn/yosys/run.sh`, `DP_SRCS` in `syn/yosys/ooc.sh`, and the source
lists in `tb/verilator/milan_dp/Makefile` and `tb/verilator/hostplane/Makefile`.
`scripts/check_soc_sources.py` has guarded exactly one of them since a missing
`KL_i2s_feed_mux` entry killed three Vivado runs forty minutes in. The other
four were unguarded, and extracting one module into
`hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv` broke three Verilator suites at
once, each with the same "Cannot find file containing module" - one per list
that nobody had told.

THE AUTHORITY IS THE RTL, NOT ANOTHER LIST. This gate walks the module closure
of `milan_datapath` through the sources themselves: what the datapath
instantiates, what those modules instantiate, transitively. Checking one list
against another would let all five agree and all five be wrong, which is the
same defect wearing a different hat. `scripts/check_soc_sources.py` already
derives the first hop this way, and this gate imports its derivation rather
than writing a second copy of it - a gate about single sources of truth that
forked its own instantiation parser would be self-refuting.

AND THE CONSUMERS ARE ASKED, NOT PARSED. A recogniser accepts what it has
modelled, and `make` and `bash` accept something else - the lesson
`syn/ooc/dp_srcs.py` records after four escapes. So each consumer prints its
own expansion (`make -s print-srcs`, `syn/yosys/run.sh --emit`) and this gate
reads that. The Vivado list is the exception: it is a Python literal with no
expansion step, and `check_soc_sources.py` owns reading it.

The Vivado consumer combines its quoted superproject entries with the
`pp_srcs.py` expansion that `milan_soc.py` itself uses for the project-owned
protocol-processor submodule. A consumer whose tooling is absent is reported
SKIPPED, by name, and the verdict says so. A gate that silently drops a
consumer it could not reach is how a list goes unchecked for months.

Usage:
    python3 scripts/check_rtl_source_lists.py            # gate
    python3 scripts/check_rtl_source_lists.py --list     # closure + per list
    python3 scripts/check_rtl_source_lists.py --selftest # mutation arms

Exit 0 = every reachable consumer carries the whole closure.
Exit 1 = a consumer is missing a module.
Exit 2 = the closure itself could not be built.
"""

import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

#: the first-hop derivation is OWNED by check_soc_sources.py. Importing it is
#: the point of this gate: two instantiation parsers would be two truths.
from check_soc_sources import INST_RE, PREFIXES
from pp_srcs import pp_sources

#: Trees a source list may legitimately draw from. The vendored AXI-stream
#: RTL is here because every consumer must carry it too - it is Verilog, not
#: SystemVerilog, which is why both suffixes are searched. A missing root is a
#: SKIP with its name, never a silently smaller closure.
SEARCH_ROOTS = ("hdl", "protocol-processor/hdl", "gptp-processor/hdl",
                "third_party/verilog-axis/rtl")


def absent_roots():
    return [r for r in SEARCH_ROOTS if not (REPO / r).is_dir()]


@lru_cache(maxsize=1)
def declaration_index():
    """Every module/package/interface declaration, indexed by unit name."""
    found = {}
    for root in SEARCH_ROOTS:
        base = REPO / root
        if not base.is_dir():
            continue
        for path in sorted(list(base.rglob("*.sv")) + list(base.rglob("*.v"))):
            text = path.read_text(errors="replace")
            for kind, name in re.findall(
                    r"^\s*(module|package|interface)\s+([A-Za-z_]\w*)\b",
                    text, re.M):
                found.setdefault(name, (kind, path))
    return found


def module_file(name):
    """The source file declaring `name`, or None.

    Declaration membership, not a naming prefix, decides whether a child is
    first-party/project RTL. Prefixes are retained only to turn a misspelled
    project-looking child into an unresolved error.
    """
    item = declaration_index().get(name)
    return item[1] if item else None


PACKAGE_REF_RE = re.compile(r"\b([A-Za-z_]\w*)::")
INTERFACE_REF_RE = re.compile(r"\b([A-Za-z_]\w*)\.(?:master|slave|monitor)\b")


def closure(top="milan_datapath"):
    """Every project compilation unit reachable from `top`.

    Module instantiations, package-qualified references and interface/modport
    types all add their declaring file. Returns (units, unresolved): the unit
    names, and project-looking module names whose source could not be found.
    """
    start = module_file(top)
    if start is None:
        return {}, {top}
    seen, unresolved, queue = {}, set(), [(top, start)]
    while queue:
        name, path = queue.pop()
        if name in seen:
            continue
        seen[name] = path.relative_to(REPO).as_posix()
        text = path.read_text(errors="replace")
        children = set(INST_RE.findall(text))
        children |= {name for name in PACKAGE_REF_RE.findall(text)
                     if declaration_index().get(name, (None,))[0] == "package"}
        children |= {name for name in INTERFACE_REF_RE.findall(text)
                     if declaration_index().get(name, (None,))[0] == "interface"}
        for child in children:
            if child in seen:
                continue
            child_path = module_file(child)
            if child_path is None:
                if child.startswith(PREFIXES):
                    unresolved.add(child)
            else:
                queue.append((child, child_path))
    return seen, unresolved


# ---------------------------------------------------------------------------
# consumers - each ASKS its own tooling for the expansion it will really use
# ---------------------------------------------------------------------------
def _repo_rel(tokens, cwd):
    """Resolve a consumer's own path tokens to repo-relative posix paths.

    A source list is a list of FILES, and one file may declare several modules
    (`KL_aaf_latency_chain` lives inside `KL_aaf_latency_taps.sv`,
    `event_counter` beside `ethernet_events`). Comparing module names to file
    stems would demand entries that must not exist, so the comparison is made
    where the lists actually live: on files."""
    out = set()
    for tok in tokens:
        if not tok.endswith((".sv", ".v")):
            continue
        try:
            out.add((cwd / tok).resolve().relative_to(REPO).as_posix())
        except ValueError:
            continue          # outside the repo: not something a gate can own
    return out


def _run(cmd, cwd):
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                             timeout=300)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"{cmd[0]}: {exc}"
    if out.returncode != 0:
        return None, f"{' '.join(cmd)} exited {out.returncode}"
    return out.stdout, None


def default_goal_is_print_srcs(directory):
    """True when a bare `make` in `directory` would print the source list.

    Adding a `print-srcs` target ABOVE a makefile's first real target makes it
    the default goal, so the suite stops running and prints a file list. The
    tally gate then reports NOCOUNT rather than a failure, which is a suite
    that measured nothing wearing the costume of a suite that passed. This
    happened here the moment print-srcs was added to the hostplane suite.

    MAKE ASKS ITSELF. A second makefile adds one target that echoes
    `.DEFAULT_GOAL`, which make has already resolved from the FIRST target of
    the first makefile - so this reads make's own answer rather than a model of
    makefile syntax. Comparing a dry run to the printed list does not work: an
    `@`-prefixed recipe makes `-n` print the command, not run it.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        probe = Path(td) / "probe.mk"
        probe.write_text("__kl_show_default_goal:\n\t@echo $(.DEFAULT_GOAL)\n")
        out, err = _run(["make", "-s", "-f", "Makefile", "-f", str(probe),
                         "__kl_show_default_goal"], directory)
    if out is None:
        return False
    return out.strip().splitlines()[-1].strip() == "print-srcs" if out.strip() else False


def _from_make(suite):
    d = REPO / "tb/verilator" / suite
    if not (d / "Makefile").is_file():
        return None, f"tb/verilator/{suite}/Makefile is absent"
    text, err = _run(["make", "-s", "print-srcs"], d)
    if text is None:
        return None, err
    if default_goal_is_print_srcs(d):
        return None, (f"tb/verilator/{suite}: a bare `make` prints the source "
                      f"list instead of running the suite - print-srcs has "
                      f"become the default goal")
    return _repo_rel(text.split(), d), None


def _from_yosys_run():
    text, err = _run(["./run.sh", "--emit", "milan_datapath"], REPO / "syn/yosys")
    if text is None:
        return None, err
    names = set()
    for line in text.splitlines():
        if line.startswith("src="):
            names |= _repo_rel(line[4:].split(), REPO / "syn/yosys")
    return names, None


def _from_yosys_ooc():
    text, err = _run(["./ooc.sh", "--emit-dp"], REPO / "syn/yosys")
    if text is None:
        return None, err
    return _repo_rel(text.split(), REPO / "syn/yosys"), None


#: every quoted source path in milan_soc.py's curated superproject list. The
#: protocol-processor half is expanded by `_pp_sources()` at import time, so it
#: is asked through the same `pp_srcs.py` authority rather than guessed from
#: Python syntax. This gate grades FILE coverage and the vendored `.v` entries
#: count too.
_VIVADO_SRC_RE = re.compile(r'"((?:[\w.-]+/)+[\w.-]+\.(?:sv|v))"')


def _from_vivado_list():
    soc = REPO / "sw/litex/milan_soc.py"
    if not soc.is_file():
        return None, "sw/litex/milan_soc.py is absent"
    tokens = _VIVADO_SRC_RE.findall(soc.read_text()) + pp_sources()
    return _repo_rel(tokens, REPO), None


CONSUMERS = (
    ("Vivado sources (sw/litex/milan_soc.py)", _from_vivado_list),
    ("Yosys milan_datapath row (syn/yosys/run.sh)", _from_yosys_run),
    ("Yosys DP_SRCS (syn/yosys/ooc.sh)", _from_yosys_ooc),
    ("Verilator milan_dp (tb/verilator/milan_dp)", lambda: _from_make("milan_dp")),
    ("Verilator hostplane (tb/verilator/hostplane)", lambda: _from_make("hostplane")),
)


def audit():
    """Returns (need, unresolved, results) with results as
    [(label, missing_sorted_or_None, skip_reason_or_None)]."""
    modules, unresolved = closure()
    need = set(modules.values())
    results = []
    for label, fetch in CONSUMERS:
        have, why = fetch()
        if have is None:
            results.append((label, None, why))
        else:
            results.append((label, sorted(need - have), None))
    return modules, need, unresolved, results


def selftest():
    """Mutation arms. Every one removes something and demands a complaint."""
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    modules, need, unresolved, results = audit()
    ck("the closure is non-empty", len(need) > 5, f"got {len(need)} file(s)")
    ck("the closure resolves every module it names", not unresolved,
       f"unresolved: {sorted(unresolved)}")
    ck("the closure is transitive, not one hop",
       "KL_aaf_latency_taps" in modules,
       "a module instantiated by a CHILD of milan_datapath must be in the closure")
    ck("a declared child needs no approved naming prefix",
       "credit_based_shaper" in modules,
       "the closure must follow declarations, not silently omit a new name family")
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

    reached = [r for r in results if r[2] is None]
    ck("at least one consumer was reachable", bool(reached),
       "every consumer skipped - this run would prove nothing")

    # THE MUTATION. Take a real consumer's real list, remove one file the
    # closure needs, and demand the comparison complains. An arm that only ever
    # sees complete lists cannot tell a working gate from an inert one.
    bitten = 0
    for label, fetch in CONSUMERS:
        have, why = fetch()
        if have is None:
            continue
        victim = sorted(need & have)[0]
        if sorted(need - (have - {victim})) == [victim]:
            bitten += 1
    ck("removing one file from a live list is detected", bitten == len(reached),
       f"{bitten} of {len(reached)} reachable consumers reported the removal")

    # asking a consumer for its list must not become what the consumer DOES
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        good = Path(td) / "good"; good.mkdir()
        (good / "Makefile").write_text(
            ".PHONY: all print-srcs\nall:\n\t@echo ran\nprint-srcs:\n\t@echo a.sv\n")
        bad = Path(td) / "bad"; bad.mkdir()
        (bad / "Makefile").write_text(
            ".PHONY: all print-srcs\nprint-srcs:\n\t@echo a.sv\nall:\n\t@echo ran\n")
        ck("a correctly ordered makefile is accepted",
           not default_goal_is_print_srcs(good))
        ck("print-srcs as the default goal is caught",
           default_goal_is_print_srcs(bad),
           "a bare make would print the list instead of running the suite")

    # the closure is a WALK: it must not be every file in the tree
    every = {p.relative_to(REPO).as_posix() for p in (REPO / "hdl").rglob("*.sv")}
    ck("the closure is a walk, not a directory listing", bool(every - need),
       "the closure covers every .sv under hdl/ - the instantiation walk is inert")

    total = 12
    print(f"\n{total} checks: {total - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()

    modules, need, unresolved, results = audit()
    gone = absent_roots()
    if gone:
        print(f"CANNOT BUILD THE CLOSURE: source root(s) {', '.join(gone)} are "
              f"not checked out, so an unresolved module cannot be told apart "
              f"from a missing tree. Run `git submodule update --init`.")
        return 2
    if not need or unresolved:
        for name in sorted(unresolved):
            print(f"UNRESOLVED MODULE: '{name}' is instantiated but no source in "
                  f"{', '.join(SEARCH_ROOTS)} declares it")
        if not need:
            print("CLOSURE EMPTY: milan_datapath could not be read")
        return 2

    if "--list" in args:
        print(f"file closure of milan_datapath ({len(need)} file(s), "
              f"{len(modules)} module/package/interface unit(s)):")
        for path in sorted(need):
            names = sorted(m for m, p in modules.items() if p == path)
            print(f"   {path}  [{', '.join(names)}]")
        print()

    bad = skipped = 0
    for label, missing, why in results:
        if why is not None:
            skipped += 1
            print(f"SKIPPED  {label}: {why}")
            continue
        if missing:
            bad += 1
            for path in missing:
                names = sorted(m for m, p in modules.items() if p == path)
                print(f"MISSING SOURCE: {label} does not carry '{path}' "
                      f"(declares {', '.join(names)}), which milan_datapath "
                      f"needs -> that consumer cannot build")
        elif "--list" in args:
            print(f"ok       {label}")

    if bad:
        return 1
    verdict = (f"RTL source-list gate: OK ({len(need)} files in the "
               f"milan_datapath closure, {len(results) - skipped} of "
               f"{len(results)} consumer list(s) carry all of them")
    print(verdict + (f"; {skipped} SKIPPED and NOT covered by this verdict)"
                     if skipped else ")"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
