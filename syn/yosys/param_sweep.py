#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Open-synthesis sweep over PARAMETER CONFIGURATIONS, not just tops.

The problem this closes. `run.sh` synthesises 47 tops, each at its **default**
parameters - it passes no override anywhere. `milan_datapath` defaults to
`N_STREAMS = 1`, `AUDIO_IF_SLOTS_P = 0`, `AAF_PLAYBACK_P = 0`, so the two
shapes that actually ship - AX7101 at 8x8 and Arty at 4x4 - were never
open-synthesised at all. A parameter combination that fails to elaborate is a
build failure, and nothing in CI would have seen it.

Why this is cheap. Two facts make a sweep affordable:

  * **The override happens at sv2v time, not in Yosys.** Yosys `chparam` works
    on a simple top (it moves `tcam` from 4,911 to 19,707 cells) but on
    `milan_datapath` it forces an AST *re-derive*, and derive mode cannot width
    -resolve sv2v's flattened SystemVerilog interface signals:
    `ERROR: Failed to detect width for identifier
    \traffic_controller...classifier_to_queue.tdest`. Every configuration
    failed that way, including the one that only re-set the defaults. So the
    sweep rewrites the parameter DEFAULTS in a scratch copy of the top and lets
    sv2v elaborate the shape, which is the path `run.sh` already proves works.
  * **The space is partitioned before it is sampled** (below), so it never
    grows the way the raw legal-value count suggests.

## Keeping the combination count down

Three reductions, in the order they matter:

1. **Only sweep tops that HAVE shape parameters.** Varying nothing across 47
   tops is 47x the cost for zero extra coverage.

2. **Equivalence-partition each parameter** - pick values that select distinct
   structural branches, not every legal number. `AUDIO_IF_SLOTS_P` accepts
   0/8/16/32, but 8, 16 and 32 all take the same TDM generate branch and
   differ only in width, so {0 (I2S), 8 (TDM narrow), 32 (TDM wide)} covers
   the shapes and 16 buys nothing.

3. **Cover PAIRS, not the product.** Almost every configuration defect is a
   two-parameter interaction, so a 2-way covering array finds them at a small
   fraction of the cost. Here that is 36 combinations reduced to ~10 runs -
   and the gap widens fast: add six binary prune parameters (the tier-1 levers
   in `docs/design/AREA_BUDGET.md`) and the product is 2,304 while pairwise
   stays near a dozen.

**This is sampling, and it is honest about that.** Pairwise cannot see a
defect that needs three specific parameters at once. The pinned configurations
below exist so the cases we care about most are never left to the sampler.

Usage:
    python3 syn/yosys/param_sweep.py --list    # the plan + coverage, no runs
    python3 syn/yosys/param_sweep.py           # run it (exit = failing configs)
    python3 syn/yosys/param_sweep.py --max 6   # tighter budget
"""
import argparse
import itertools
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

#: Parameter -> the values worth synthesising, after equivalence partitioning.
#: Each entry says WHY those values and not the others; a value that selects no
#: distinct structure is cost without coverage.
SPACE = {
    # 1 is the degenerate single-context path (the no-regression default),
    # 4 and 8 are the shipping NxN shapes. Intermediate widths reuse the same
    # generate loop.
    "N_STREAMS": [1, 4, 8],
    # 0 selects KL_aaf_capture_i2s; anything > 0 selects KL_tdm_capture. 8 and
    # 32 are the narrow and wide TDM shapes; 16 takes the identical branch.
    "AUDIO_IF_SLOTS_P": [0, 8, 32],
    # binary: instantiate KL_pcm_tx or prune it
    "AAF_PLAYBACK_P": [0, 1],
    # divider/counter elaboration differs between the two board clocks
    "MILAN_CLK_FREQ_HZ": [50_000_000, 100_000_000],
}

#: Configurations that must ALWAYS run, whatever the sampler decides. These are
#: the ones where a failure is not a curiosity but a broken product.
PINNED = {
    "default": dict(N_STREAMS=1, AUDIO_IF_SLOTS_P=0, AAF_PLAYBACK_P=0,
                    MILAN_CLK_FREQ_HZ=100_000_000),
    "ship-ax-8x8": dict(N_STREAMS=8, AUDIO_IF_SLOTS_P=8, AAF_PLAYBACK_P=1,
                        MILAN_CLK_FREQ_HZ=100_000_000),
    "ship-arty-4x4": dict(N_STREAMS=4, AUDIO_IF_SLOTS_P=0, AAF_PLAYBACK_P=1,
                          MILAN_CLK_FREQ_HZ=50_000_000),
    # the extremes: smallest shape is where degenerate/undriven logic hides,
    # largest is where elaboration blows up
    "min": dict(N_STREAMS=1, AUDIO_IF_SLOTS_P=0, AAF_PLAYBACK_P=0,
                MILAN_CLK_FREQ_HZ=50_000_000),
    "max": dict(N_STREAMS=8, AUDIO_IF_SLOTS_P=32, AAF_PLAYBACK_P=1,
                MILAN_CLK_FREQ_HZ=100_000_000),
}

#: Tops carrying shape parameters. Everything else in run.sh has none, so
#: sweeping it would cost time and cover nothing new.
SWEPT_TOPS = ["milan_datapath"]

DEFAULT_MAX = 12

#: Below this, a single-parameter cell-count delta is not evidence the override
#: did anything - synthesis is not bit-reproducible at that resolution.
MARGINAL_PCT = 0.5


def all_pairs():
    """Every (param, value, param, value) pair the space can produce."""
    out = set()
    for (a, av), (b, bv) in itertools.combinations(SPACE.items(), 2):
        for x in av:
            for y in bv:
                out.add(((a, x), (b, y)))
    return out


def pairs_of(cfg):
    return {((a, cfg[a]), (b, cfg[b]))
            for a, b in itertools.combinations(SPACE, 2)}


def plan(max_runs):
    """Pinned configurations, then a greedy 2-way fill of what they missed."""
    chosen = dict(PINNED)
    covered = set().union(*(pairs_of(c) for c in chosen.values()))
    target = all_pairs()

    # Greedy: repeatedly take the candidate covering the most missing pairs.
    # Not minimal - minimal covering arrays are NP-hard - but within a config
    # or two of it, and the selection is deterministic so CI is reproducible.
    names = list(SPACE)
    while len(chosen) < max_runs and covered < target:
        best, best_gain = None, 0
        for combo in itertools.product(*(SPACE[k] for k in names)):
            cfg = dict(zip(names, combo))
            gain = len(pairs_of(cfg) - covered)
            if gain > best_gain:
                best, best_gain = cfg, gain
        if best is None:
            break
        chosen[f"fill-{len(chosen) - len(PINNED) + 1}"] = best
        covered |= pairs_of(best)

    return chosen, covered, target


#: `  parameter int N_STREAMS = 1,`  ->  capture so the default can be replaced
def _param_re(name):
    return re.compile(rf"(^\s*parameter\s+int\s+{re.escape(name)}\s*=\s*)"
                      rf"([0-9_]+)", re.M)


def convert(top, srcs, inc, cfg, tmp, tag):
    """sv2v the sources with this configuration's parameter defaults applied.

    The top's own source is copied and its parameter DEFAULTS rewritten, so
    sv2v elaborates the requested shape. Only the top is patched; the rest of
    the source list is passed through untouched.
    """
    top_src = next((s for s in srcs if Path(s).name == f"{top}.sv"), None)
    if top_src is None:
        return None, f"cannot find {top}.sv in the source list"
    text = Path(top_src).read_text()
    for k, v in cfg.items():
        text, n = _param_re(k).subn(rf"\g<1>{v}", text)
        if n == 0:
            return None, f"parameter {k} not found in {top}.sv - cannot override"
    patched = tmp / f"{tag}_{top}.sv"
    patched.write_text(text)
    srcs = [str(patched) if s == top_src else s for s in srcs]

    r = subprocess.run(["sv2v", f"--top={top}"] + inc + srcs,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr.strip().split("\n")[0][:110]
    out = tmp / f"{tag}.v"
    out.write_text(r.stdout)
    return out, None


#: `stat` prints ONE BLOCK PER MODULE and only the last block, `=== design
#: hierarchy ===`, is the whole design. Taking the first `N cells` line reads
#: whichever leaf yosys happened to emit first - here `tcam`, which is
#: parameter-independent, so EVERY configuration reported an identical 4,911
#: cells and the sweep looked like it was measuring something. `stat -top`
#: emits the hierarchy block; this anchors on it.
DESIGN_TOTAL_RE = re.compile(r"=== design hierarchy ===.*?^\s+(\d+) cells$",
                             re.M | re.S)


def synth(top, vfile, cfg, tmp):
    script = (f"read_verilog {vfile}; synth -top {top}; hierarchy -check; "
              f"stat -top {top}")
    r = subprocess.run(["yosys", "-p", script], capture_output=True, text=True)
    if r.returncode != 0:
        err = [l for l in (r.stdout + r.stderr).split("\n")
               if l.upper().startswith("ERROR")]
        return None, (err[0] if err else "yosys failed")[:110]
    m = DESIGN_TOTAL_RE.search(r.stdout)
    if not m:
        return None, "no '=== design hierarchy ===' total in stat output"
    return int(m.group(1)), None


def sources_from_run_sh(top):
    """Reuse run.sh's source list verbatim - ONE list, not two that can drift.

    run.sh sets `R` from `$0`, which is meaningless when the prelude is
    evaluated anywhere else (it silently resolved to the caller's home, and every
    source path came out wrong). So `R` is pinned to the repo root here and the
    remaining assignments are evaluated on top of it.
    """
    text = (REPO / "syn/yosys/run.sh").read_text()
    m = re.search(rf'^\s*"{re.escape(top)}\|(.*?)"\s*$', text, re.M)
    if not m:
        return None
    prelude = [l for l in text.split("tops=(")[0].split("\n")
               if re.match(r"^[A-Za-z_]+=", l) and not l.startswith("R=")]
    # `$INC` carries the -I search path; several sources `include` headers that
    # are not resolvable without it.
    script = (f'R={REPO}\n' + "\n".join(prelude)
              + f'\necho {m.group(1)}\necho "---"\necho $INC\n')
    r = subprocess.run(["bash", "-c", script], capture_output=True, text=True,
                       cwd=REPO)
    if r.returncode != 0:
        return None, None
    srcs_txt, _, inc_txt = r.stdout.partition("---")
    srcs = srcs_txt.split()
    missing = [s for s in srcs if not Path(s).is_file()]
    if missing:
        print(f"  [FAIL] {top}: {len(missing)} source(s) not found, first: "
              f"{missing[0]}")
        return None, None
    return srcs, inc_txt.split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--max", type=int, default=DEFAULT_MAX)
    args = ap.parse_args()

    chosen, covered, target = plan(args.max)
    product = 1
    for v in SPACE.values():
        product *= len(v)

    print(f"== parameter sweep plan ==")
    print(f"space: {' x '.join(f'{k}({len(v)})' for k, v in SPACE.items())}"
          f" = {product} combinations")
    print(f"runs:  {len(chosen)}  ({len(PINNED)} pinned + "
          f"{len(chosen) - len(PINNED)} pairwise fill)")
    print(f"2-way coverage: {len(covered)}/{len(target)} pairs "
          f"({100 * len(covered) // len(target)} %)")
    if covered < target:
        # No silent caps: say what the budget dropped.
        print(f"NOT COVERED at --max {args.max}: {len(target - covered)} pair(s) "
              f"- raise --max to close them")
    print()
    for name, cfg in chosen.items():
        print(f"  {name:<14} " + "  ".join(f"{k}={v}" for k, v in cfg.items()))
    if args.list:
        return 0

    for t in ("sv2v", "yosys"):
        if not shutil.which(t):
            print(f"missing tool: {t} (see syn/yosys/README.md)")
            return 2

    fails = 0
    tmp = Path(tempfile.mkdtemp(prefix="paramsweep."))
    try:
        for top in SWEPT_TOPS:
            srcs, inc = sources_from_run_sh(top)
            if not srcs:
                print(f"  [FAIL] {top}: no source list found in run.sh")
                fails += 1
                continue
            print(f"\n== {top} ==")
            base = None
            seen_cells = {}
            for name, cfg in chosen.items():
                t1 = time.time()
                vfile, err = convert(top, srcs, inc, cfg, tmp, name)
                if err:
                    print(f"  [FAIL] {name:<14} sv2v: {err}")
                    fails += 1
                    continue
                cells, err = synth(top, vfile, cfg, tmp)
                if err:
                    print(f"  [FAIL] {name:<14} {err}")
                    fails += 1
                    continue
                seen_cells.setdefault(cells, []).append(name)
                if name == "default":
                    base = cells
                delta = ""
                if base and cells and name != "default":
                    delta = f"  ({cells / base:.2f}x default)"
                print(f"  [PASS] {name:<14} cells={cells:<8} "
                      f"{time.time() - t1:.0f}s{delta}")

            # PER-PARAMETER sensitivity, not "some number moved". The first
            # version of this check only asserted the counts were not all
            # identical, and it passed while the extraction was reading a
            # parameter-independent leaf module: AAF_PLAYBACK_P happened to
            # correlate with the two values seen, so "3 distinct sizes" looked
            # like proof that all four overrides bit. It proved nothing about
            # the other three. Now each parameter is judged on pairs that
            # differ in IT ALONE, and a parameter with no such pair in the plan
            # is reported undetermined rather than assumed working.
            by_cfg = {n: c for n, c in chosen.items()}
            cells_of = {n: c for c, ns in seen_cells.items() for n in ns}
            for pname in SPACE:
                pairs = [(a, b) for a, b in itertools.combinations(by_cfg, 2)
                         if by_cfg[a][pname] != by_cfg[b][pname]
                         and all(by_cfg[a][k] == by_cfg[b][k]
                                 for k in SPACE if k != pname)]
                pairs = [(a, b) for a, b in pairs
                         if a in cells_of and b in cells_of]
                if not pairs:
                    print(f"  [warn] {pname}: no pair in this plan differs in "
                          f"it alone - sensitivity UNDETERMINED, not proven")
                    continue
                # "different" is not "meaningfully different". AUDIO_IF_SLOTS_P
                # 8 -> 32 moved SEVENTEEN cells out of 910,000 - 0.002 %,
                # indistinguishable from synthesis noise - and reporting that as
                # proof the override bit would be the same mistake as the check
                # this replaced. Anything under MARGINAL_PCT is reported as
                # marginal, which is a fact about the parameter (it selects
                # almost the same hardware), not a failure.
                best = max(pairs, key=lambda ab:
                           abs(cells_of[ab[0]] - cells_of[ab[1]]))
                a, b = best
                d = abs(cells_of[a] - cells_of[b])
                pct = 100.0 * d / max(cells_of[a], cells_of[b], 1)
                if d and pct >= MARGINAL_PCT:
                    print(f"  [ok]   {pname}: {cells_of[a]} vs {cells_of[b]} "
                          f"({a} vs {b}) - {d:+} cells, {pct:.2f} % - bites")
                elif d:
                    print(f"  [marg] {pname}: largest single-parameter delta is "
                          f"{d} cells ({pct:.3f} %) between {a} and {b} - the "
                          f"override is WIRED but selects near-identical "
                          f"hardware; do not read this as proof it works")
                else:
                    print(f"  [FAIL] {pname}: {a} and {b} differ ONLY in "
                          f"{pname} yet synthesised to the same "
                          f"{cells_of[a]} cells - that override is not taking "
                          f"effect")
                    fails += 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\nconfigs: {len(chosen) * len(SWEPT_TOPS)}   fail: {fails}")
    print(f"RESULT: {'PASS' if fails == 0 else 'FAIL'}")
    return fails


if __name__ == "__main__":
    sys.exit(main())
