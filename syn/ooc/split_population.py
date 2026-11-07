#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""split_population.py - the full-split population in a Yosys elaboration of every shape (#665 F-INT PR 2).

THE QUESTION. A split image must hold no protocol processor and no fabric MAAP
engine, and one mailbox and one gPTP plane: pp_placement.limits("full-split").
The measurement recipes check that after Vivado's synthesis; this check holds
it on the RTL, in every shape the builder builds, before any route.

THE ELABORATION is the census's recipe (sw/mailbox/census_elab.py): CI's
sources, defines and include directories, each shape's generated header and
the builder's parameters, the pinned sv2v and Yosys. Here nothing is a
blackbox: sv2v lowers every source, and ``hierarchy -check`` elaborates the
datapath at the shape with ``CTRL_SPLIT_P = 1``, and every module below it.
The mailbox side is one more elaboration, of KL_mbx_cdc and KL_mbx, which
milan_soc.py's split SoC instantiates once each beside the datapath.

THE COUNT walks each tree from its top through every cell, so a module counts
once per instance, wherever it sits, and a parameterised copy counts as its
module. Each role of pp_placement.MODULES must then be within
pp_placement.limits("full-split", role) in every shape.

    python3 syn/ooc/split_population.py --check [--jobs N]
    python3 syn/ooc/split_population.py --selftest [--jobs N]

``--selftest`` plants the processor back into the split, and the fabric MAAP
engine, each required to fail on its role by name, beside the tracked sources,
which must pass, in the recipe's shape.
"""

from __future__ import annotations

import argparse
import multiprocessing
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path[:0] = [str(HERE), str(REPO / "sw/mailbox")]
import census_elab as ce  # noqa: E402
import pp_placement  # noqa: E402

PLACEMENT = "full-split"
#: the mailbox side the split SoC adds, one KL_mbx_cdc and one KL_mbx, and its sources (milan_soc.py's lists)
MAILBOX_SOURCES = ("hdl/milan/mailbox/KL_mbx_pkg.sv", "hdl/milan/mailbox/KL_mbx_ring.sv",
                   "hdl/milan/mailbox/KL_mbx_rx.sv", "hdl/milan/mailbox/KL_mbx_tx.sv",
                   "hdl/milan/mailbox/KL_mbx_evt.sv", "hdl/milan/mailbox/KL_mbx.sv",
                   "hdl/common/cdc_handshake.sv", "hdl/milan/mailbox/KL_mbx_cdc_window.sv",
                   "hdl/milan/mailbox/KL_mbx_cdc.sv")
def base_name(module: str) -> str:
    """The module a (possibly parameterised) Yosys module name copies."""
    m = re.match(r"^\$paramod(?:\$[0-9a-f]+)?\\([^\\]+)", module)
    return m.group(1) if m else module.lstrip("\\")


def rtlil_modules(text: str) -> tuple[dict[str, list[str]], set[str]]:
    """({module: the types of its cells}, the modules marked top) of an RTLIL dump."""
    mods: dict[str, list[str]] = {}
    tops, attrs, cur = set(), [], None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("attribute "):
            attrs.append(s)
        elif s.startswith("module "):
            cur = s.split()[1]
            mods[cur] = []
            if any(a.startswith("attribute \\top ") for a in attrs):
                tops.add(cur)
            attrs = []
        elif s.startswith("cell ") and cur is not None:
            mods[cur].append(s.split()[1])
            attrs = []
        elif s == "end" or not s.startswith("attribute "):
            attrs = [] if not s.startswith("attribute ") else attrs
    return mods, tops


def tree_counts(text: str, top: str) -> Counter:
    """Every instance below top, by its module's base name, top included."""
    mods, tops = rtlil_modules(text)
    start = next((m for m in tops if base_name(m) == top), None) or next(
        (m for m in mods if base_name(m) == top), None)
    if start is None:
        raise ce.CensusError(f"the elaborated design holds no module {top}")
    count, todo = Counter(), [start]
    while todo:
        m = todo.pop()
        count[base_name(m)] += 1
        todo += [c for c in mods[m] if c in mods]
    return count


def elaborate_tree(files: list[Path], incdirs: list[Path], defines: tuple[str, ...], top: str,
                   params: tuple[tuple[str, int], ...], overlay: dict[Path, str], work: Path) -> Counter:
    """sv2v over files, Yosys's hierarchy at top with params, and the instance counts below top."""
    tree = work / "tree"
    tree.mkdir(parents=True, exist_ok=True)
    for _gen, image in ce.ROMS:       # $readmemh reads them from the elaborator's directory
        shutil.copy(ce.WORK.path() / image, work / image)
    srcs = []
    for f in files:
        dst = tree / f.relative_to(REPO)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if f in overlay:
            dst.write_text(overlay[f], encoding="utf-8")
        else:
            dst.symlink_to(f)
        srcs.append(str(dst))
    inc = []
    for d in incdirs:
        inc += ["-I", str(d)]
    text = ce.run([ce.tool("sv2v"), *(f"-D{d}" for d in defines), *inc, *srcs], work,
                  "the front end (sv2v) refused the split's sources")
    (work / "all.v").write_text(text, encoding="utf-8")
    bind = "".join(f" -chparam {k} {v}" for k, v in params)
    ce.run([ce.tool("yosys"), "-q", "-p", f"read_verilog -defer {work / 'all.v'}; "
            f"hierarchy -check -top {top}{bind}; write_rtlil {work / 'net.il'}"], work,
           f"the elaborator (Yosys) refused {top}")
    return tree_counts((work / "net.il").read_text(), top)


def shape_counts(job: tuple[int, dict[str, str]]) -> tuple[str, dict[str, int]]:
    """(shape, every role's count) of the split image in one shape: the datapath and the mailbox side."""
    index, overlay_text = job
    overlay = {Path(p): t for p, t in overlay_text.items()}
    shape = ce.shapes()[index]
    rcp = ce.shaped(ce.recipe(), shape)
    work = Path(tempfile.mkdtemp(prefix="split-population-"))
    try:
        ce.WORK.roms()
        dp = elaborate_tree([Path(s).resolve() for s in rcp.sources], [Path(d).resolve() for d in rcp.incdirs],
                            rcp.defines, ce.TOP, (*shape.params, ("CTRL_SPLIT_P", 1)), overlay, work / "dp")
        side_dir = work / "mbx"
        side_dir.mkdir()
        mb = _mailbox([REPO / f for f in MAILBOX_SOURCES], overlay, side_dir)
        both = dp + mb
        return shape.name, {role: both.get(module, 0) for role, module in pp_placement.MODULES.items()}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _mailbox(files: list[Path], overlay: dict[Path, str], work: Path) -> Counter:
    """The mailbox side's instances: KL_mbx_cdc and KL_mbx, each elaborated as its own top."""
    out = Counter()
    for top in ("KL_mbx_cdc", "KL_mbx"):
        sub = work / top
        sub.mkdir()
        out += elaborate_tree(files, [], (), top, (), overlay, sub)
    return out


def findings(rows: dict[str, dict[str, int]]) -> list[str]:
    """Every role of every shape outside the full-split limits."""
    out = []
    for shape, counts in sorted(rows.items()):
        for role, count in counts.items():
            low, high = pp_placement.limits(PLACEMENT, role)
            if not low <= count <= high:
                out.append(f"shape {shape}: wrong placement {PLACEMENT}: {role} ({pp_placement.MODULES[role]}) "
                           f"count {count}, expected {low}..{high}")
    return out


def survey(jobs: int, overlay: dict[Path, str] | None = None, only: int | None = None) -> dict[str, dict[str, int]]:
    """Every shape's role counts, or one shape's."""
    ce.toolchain()
    picks = range(len(ce.shapes())) if only is None else [only]
    work = [(i, {str(p): t for p, t in (overlay or {}).items()}) for i in picks]
    with multiprocessing.get_context("fork").Pool(max(1, min(jobs, len(work)))) as pool:
        return dict(pool.map(shape_counts, work))


#: (name, the planted text in milan_datapath.sv, the finding's words)
PLANTS = (
    ("the processor left in the split", "  generate if (CTRL_SPLIT_P == 0) begin : g_af_pp\n",
     "  generate if (1) begin : g_af_pp\n", "wrapper (KL_pp_shadow) count 1, expected 0..0"),
    ("the fabric MAAP engine left in the split", "  generate if ((MAAP_P != 0) && (CTRL_SPLIT_P == 0)) begin : g_maap\n",
     "  generate if (MAAP_P != 0) begin : g_maap\n", "maap (KL_maap) count 1, expected 0..0"),
)


def selftest(jobs: int) -> int:
    """The tracked sources pass in the recipe's shape; each plant fails on its role."""
    dp = REPO / "hdl/milan/milan_datapath.sv"
    text = dp.read_text()
    bad = 0
    clean = findings(survey(1, only=0))
    print(f"{'ok  ' if not clean else 'FAIL'} control: the tracked sources: {clean or 'every role within its limits'}")
    bad += bool(clean)
    for label, old, new, words in PLANTS:
        if text.count(old) != 1:
            print(f"FAIL {label}: its anchor is not in the datapath once")
            bad += 1
            continue
        got = findings(survey(1, {dp: text.replace(old, new)}, only=0))
        ok = any(words in f for f in got)
        print(f"{'ok  ' if ok else 'FAIL'} {label}: {got}")
        bad += not ok
    print(f"split population self-test: {len(PLANTS) + 1 - bad} of {len(PLANTS) + 1} arms as required")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--check", action="store_true", help="every shape's split population within its limits")
    ap.add_argument("--selftest", action="store_true", help="the plants fail, the tracked sources pass")
    ap.add_argument("--jobs", type=int, default=1)
    args = ap.parse_args()
    if args.selftest:
        return selftest(args.jobs)
    if not args.check:
        ap.error("give --check or --selftest")
    rows = survey(args.jobs)
    for shape, counts in sorted(rows.items()):
        print(f"shape {shape}: " + ", ".join(f"{role} {n}" for role, n in counts.items()))
    out = findings(rows)
    print("\n".join(out) or f"split population: {len(rows)} shape(s), every role within the {PLACEMENT} limits")
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
