#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""area_baseline.py - the area/timing baseline for an optimisation round.

WHY THIS EXISTS. Every area campaign in this tree has started by hand-reading
Vivado reports out of whichever build directory happened to be newest, and
every one of them has been misled at least once by doing it slightly
differently than the last. The three recorded traps:

  1. yosys `-flatten` LUT numbers run 1.0x-2.6x high and DO NOT PRESERVE RANK
     ORDER against Vivado. KL_chan_map_render is #3 by yosys OOC and #33 in
     the real build, because its DEFAULT parameters are a 64-channel crossbar
     and the ship shape binds 8. Grading a proposal on an OOC number alone is
     how you optimise a block that costs 26 LUT.
  2. POST-SYNTH is not POST-PLACE. LUT combining moves the shipping number by
     ~4000 (57,512 -> 53,542 on eppo_t540). A saving must be measured against
     the same stage it will be judged in.
  3. The headline in docs/design/AREA_BUDGET.md goes stale silently. It says
     97.7% from a 2026-07-27 8x8 build; the tree today ships 1x1_tdm8 at
     90.71%. The tree wins over the doc - so this script reads the tree.

USAGE
  # newest build, headline + ranked hierarchy
  scripts/area_baseline.py

  # a specific build
  scripts/area_baseline.py --build ~/litex-milan/work/build_ax7101_eppo_t540

  # BEFORE vs AFTER a change - the number that actually settles a proposal
  scripts/area_baseline.py --build <after> --compare <before>

  # add the yosys out-of-context column (slow: ~20 min, synthesises every top)
  scripts/area_baseline.py --ooc

  # machine-readable, for a campaign harness
  scripts/area_baseline.py --json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_WORK = os.path.expanduser("~/litex-milan/work")


# ---------------------------------------------------------------- discovery --
def find_builds(work: str) -> list[str]:
    """Build dirs that actually carry a placed utilization report, newest first.

    A directory with only a synth report is a build that died before place;
    quoting its LUT number as the design's area is the post-synth/post-place
    trap above, so those are not offered.
    """
    out = []
    for d in glob.glob(os.path.join(work, "build_*")):
        if not os.path.isdir(d):
            continue
        if glob.glob(os.path.join(d, "gateware",
                                  "*utilization_hierarchical_place.rpt")):
            out.append(d)
    return sorted(out, key=os.path.getmtime, reverse=True)


def rpt(build: str, suffix: str) -> str | None:
    hits = glob.glob(os.path.join(build, "gateware", f"*{suffix}"))
    return hits[0] if hits else None


# ------------------------------------------------------------------ parsing --
_SUMMARY_KEYS = {
    "Slice LUTs": "lut",
    "Slice Registers": "ff",
    "Block RAM Tile": "bram",
    "DSPs": "dsp",
    "F7 Muxes": "f7",
    "F8 Muxes": "f8",
}


def parse_summary(path: str) -> dict:
    """`| Slice LUTs* | 57512 | 0 | 0 | 63400 | 90.71 |`"""
    res: dict[str, dict] = {}
    if not path or not os.path.exists(path):
        return res
    for line in open(path, errors="replace"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        name = cells[0].rstrip("*").strip()
        key = _SUMMARY_KEYS.get(name)
        if not key or key in res:
            continue
        try:
            res[key] = {"used": int(cells[1]), "avail": int(cells[-2]),
                        "pct": float(cells[-1])}
        except ValueError:
            continue
    return res


def parse_timing(path: str) -> dict:
    """The design-wide WNS/TNS/WHS row, plus the MET/VIOLATED verdict."""
    if not path or not os.path.exists(path):
        return {}
    txt = open(path, errors="replace").read()
    m = re.search(r"WNS\(ns\).*?\n\s*-+.*?\n\s*([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+"
                  r"(\d+)\s+([-\d.]+)\s+([-\d.]+)", txt, re.S)
    if not m:
        return {}
    wns, tns, fail_ep, tot_ep, whs, ths = m.groups()
    return {"wns": float(wns), "tns": float(tns),
            "failing_endpoints": int(fail_ep), "total_endpoints": int(tot_ep),
            "whs": float(whs), "ths": float(ths),
            "met": float(wns) >= 0.0 and float(whs) >= 0.0}


def parse_hier(path: str) -> list[dict]:
    """Utilization-by-Hierarchy rows. Indentation carries the depth."""
    rows: list[dict] = []
    if not path or not os.path.exists(path):
        return rows
    started = False
    for line in open(path, errors="replace"):
        if line.startswith("+---") :
            started = True
            continue
        if not started or not line.startswith("|"):
            continue
        raw = line.rstrip("\n").strip("|").split("|")
        if len(raw) < 10:
            continue
        inst_raw = raw[0]
        if inst_raw.strip() in ("Instance", ""):
            continue
        depth = (len(inst_raw) - len(inst_raw.lstrip())) // 2
        try:
            nums = [int(c.strip()) for c in raw[2:10]]
        except ValueError:
            continue
        rows.append({
            "instance": inst_raw.strip(), "module": raw[1].strip(),
            "depth": depth, "lut": nums[0], "logic_lut": nums[1],
            "lutram": nums[2], "srl": nums[3], "ff": nums[4],
            "ramb36": nums[5], "ramb18": nums[6], "dsp": nums[7],
        })
    return rows


# --------------------------------------------------------------------- yosys --
def run_ooc() -> dict[str, dict]:
    """syn/yosys/ooc.sh, parsed. SLOW. Numbers are DEFAULT-parameter, so they
    are a block-identity signal and a rank hint, never a shipping area."""
    sh = os.path.join(REPO, "syn", "yosys", "ooc.sh")
    if not os.path.exists(sh):
        return {}
    try:
        p = subprocess.run([sh], cwd=os.path.dirname(sh), capture_output=True,
                           text=True, timeout=7200)
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  ! ooc.sh did not complete ({e}); OOC column omitted",
              file=sys.stderr)
        return {}
    out: dict[str, dict] = {}
    for line in (p.stdout or "").splitlines():
        f = line.split()
        if len(f) >= 7 and f[0] not in ("top",) and f[1].isdigit():
            out[f[0]] = {"lut": int(f[1]), "ff": int(f[2])}
    return out


# ------------------------------------------------------------------ display --
def headline(build: str, summ: dict, tim: dict) -> None:
    print(f"build   : {build}")
    for k, label in (("lut", "Slice LUTs"), ("ff", "Slice Registers"),
                     ("bram", "Block RAM Tile"), ("dsp", "DSPs")):
        if k in summ:
            v = summ[k]
            print(f"{label:16s}: {v['used']:>7} / {v['avail']:>7}"
                  f"  = {v['pct']:5.2f} %")
    if tim:
        verdict = "MET" if tim["met"] else "VIOLATED"
        print(f"{'timing':16s}: WNS {tim['wns']:+.3f} ns  WHS {tim['whs']:+.3f} ns"
              f"  TNS {tim['tns']:.3f}  {verdict}"
              f"  ({tim['failing_endpoints']} failing of"
              f" {tim['total_endpoints']})")


def table(rows: list[dict], ooc: dict, depth: int, top: int) -> None:
    sel = [r for r in rows if r["depth"] == depth]
    sel.sort(key=lambda r: -r["lut"])
    if not sel:
        print(f"  (no instances at depth {depth}; try --depth 1 or 3)")
        return
    hdr = (f"{'instance':<44}{'module':<30}{'LUT':>7}{'LUTRAM':>8}"
           f"{'FF':>7}{'R36':>5}{'R18':>5}{'DSP':>5}")
    if ooc:
        hdr += f"{'oocLUT':>8}{'ratio':>7}"
    print(hdr)
    print("-" * len(hdr))
    for r in sel[:top]:
        line = (f"{r['instance'][:43]:<44}{r['module'][:29]:<30}"
                f"{r['lut']:>7}{r['lutram']:>8}{r['ff']:>7}"
                f"{r['ramb36']:>5}{r['ramb18']:>5}{r['dsp']:>5}")
        if ooc:
            o = ooc.get(r["module"], {}).get("lut")
            if o and r["lut"]:
                line += f"{o:>8}{o / r['lut']:>6.2f}x"
            else:
                line += f"{'-':>8}{'-':>7}"
        print(line)


def compare(now: list[dict], before: list[dict], top: int) -> None:
    """Per-instance LUT delta. This is the only number that settles a
    proposal: 'measure before AND after' is a standing rule here."""
    # Match on instance path, then fall back to (module, depth).
    #
    # The fallback is not cosmetic: Vivado sizes the Instance column to the
    # widest name IN THAT REPORT, so a long hierarchical name (the VexiiRiscv
    # hash paths, typically) is truncated to a DIFFERENT width in two builds
    # of the same design. Keyed on the raw string those look like a whole
    # block appearing and an almost-identically-named one disappearing, which
    # lands as a five-figure phantom delta and swamps the real total.
    b_inst = {r["instance"]: r for r in before}
    b_modd: dict[tuple, list] = {}
    for r in before:
        b_modd.setdefault((r["module"], r["depth"]), []).append(r)

    used, deltas, renamed = set(), [], 0
    for r in now:
        prev = b_inst.get(r["instance"])
        if prev is None:
            cand = [x for x in b_modd.get((r["module"], r["depth"]), [])
                    if id(x) not in used]
            if len(cand) != 1:
                # the hash-bearing generated names (VexiiRiscvLitex_<hash>)
                # truncate in BOTH the instance and the module column, so an
                # exact module match fails too - fall back to prefix identity
                # at the same depth, which is unambiguous in practice
                cand = [x for x in before
                        if x["depth"] == r["depth"] and id(x) not in used
                        and (x["module"].startswith(r["module"][:24])
                             or r["module"].startswith(x["module"][:24]))
                        and (x["instance"].startswith(r["instance"][:24])
                             or r["instance"].startswith(x["instance"][:24]))]
            if len(cand) == 1:
                prev, renamed = cand[0], renamed + 1
        if prev is None:
            deltas.append((r["lut"], r["instance"], r["module"], None, r["lut"]))
            continue
        used.add(id(prev))
        if prev["lut"] != r["lut"]:
            deltas.append((r["lut"] - prev["lut"], r["instance"], r["module"],
                           prev["lut"], r["lut"]))
    deltas += [(-v["lut"], k, v["module"], v["lut"], None)
               for k, v in b_inst.items() if id(v) not in used]
    if renamed:
        print(f"  ({renamed} instance(s) matched by module+depth - the report's "
              f"Instance column is width-truncated per build)")
    if not deltas:
        print("  no per-instance LUT change")
        return
    deltas.sort(key=lambda t: t[0])
    print(f"{'delta':>8}  {'was':>7} -> {'now':>7}  instance")
    print("-" * 72)
    for d, inst, _mod, was, nowv in deltas[:top]:
        print(f"{d:>+8}  {('-' if was is None else was):>7} -> "
              f"{('-' if nowv is None else nowv):>7}  {inst[:44]}")
    print("-" * 72)
    print(f"{sum(d for d, *_ in deltas):>+8}  net LUT change across "
          f"{len(deltas)} changed instance(s)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", help="build dir (default: newest placed one)")
    ap.add_argument("--compare", help="baseline build dir to diff against")
    ap.add_argument("--work", default=DEFAULT_WORK, help="where builds live")
    ap.add_argument("--depth", type=int, default=2,
                    help="hierarchy depth to rank (2 = milan_datapath's children)")
    ap.add_argument("--top", type=int, default=25, help="rows to print")
    ap.add_argument("--ooc", action="store_true",
                    help="also run syn/yosys/ooc.sh (SLOW, ~20 min)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    builds = find_builds(a.work)
    build = a.build or (builds[0] if builds else None)
    if not build:
        print(f"no placed build under {a.work}\n"
              f"  (a build with only a synth report is skipped on purpose - "
              f"post-synth LUTs are ~4000 high on this design)", file=sys.stderr)
        return 2

    summ = parse_summary(rpt(build, "utilization_synth.rpt"))
    tim = parse_timing(rpt(build, "timing.rpt"))
    hier = parse_hier(rpt(build, "utilization_hierarchical_place.rpt"))
    ooc = run_ooc() if a.ooc else {}

    if a.json:
        print(json.dumps({"build": build, "summary": summ, "timing": tim,
                          "hierarchy": hier, "ooc": ooc}, indent=1))
        return 0

    print("=" * 78)
    headline(build, summ, tim)
    print("=" * 78)
    if hier:
        tot = hier[0]
        print(f"post-place total: {tot['lut']} LUT "
              f"({tot['lutram']} LUTRAM, {tot['srl']} SRL), {tot['ff']} FF, "
              f"{tot['ramb36']}x RAMB36 + {tot['ramb18']}x RAMB18\n")
    table(hier, ooc, a.depth, a.top)

    if a.compare:
        base = parse_hier(rpt(a.compare, "utilization_hierarchical_place.rpt"))
        if not base:
            print(f"\n! no placed hierarchy report in {a.compare}", file=sys.stderr)
            return 2
        bs = parse_summary(rpt(a.compare, "utilization_synth.rpt"))
        bt = parse_timing(rpt(a.compare, "timing.rpt"))
        print("\n" + "=" * 78)
        print(f"COMPARE vs {a.compare}")
        if "lut" in bs and "lut" in summ:
            d = summ["lut"]["used"] - bs["lut"]["used"]
            print(f"  synth LUT {bs['lut']['used']} -> {summ['lut']['used']}"
                  f"  ({d:+})   {bs['lut']['pct']:.2f}% -> {summ['lut']['pct']:.2f}%")
        if bt and tim:
            print(f"  WNS {bt['wns']:+.3f} -> {tim['wns']:+.3f} ns"
                  f"   ({'MET' if bt['met'] else 'VIOLATED'} ->"
                  f" {'MET' if tim['met'] else 'VIOLATED'})")
        print("=" * 78)
        compare(hier, base, a.top)

    if len(builds) > 1 and not a.build:
        print(f"\n(newest of {len(builds)} placed builds; --build to pick, "
              f"--compare to diff)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
