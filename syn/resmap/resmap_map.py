#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Whole-image resource map (issue #649): rank every block and tie the sums.

Input is one directory written by syn/resmap/route_map.tcl from a routed
checkpoint: the full-depth hierarchical utilization, the flat utilization and
the primitive census with each cell's placed site and BEL. Output is every
block of the rebuilt hierarchy with LUT (logic, LUTRAM, SRL), FF, RAMB36,
RAMB18, DSP, CARRY4 and an attributed slice count, ranked, and a list of ties
that must all hold before any figure is printed.

A BLOCK is a leaf of the reported hierarchy: an instance with no reported
child, or the parenthesized own-logic row of an instance that has children.
For FF, I/O-tile FF, RAMB36, RAMB18, DSP, CARRY4 and slices the leaves
partition the image: their sums are the image's totals. The four LUT columns
do not. The report counts a LUT site that holds cells of two blocks (the two
halves of one LUT6_2 site) once in each block, so the leaves' LUT sum exceeds
the image's by the number of such sites. Each parent's excess over its parts
is its SHARING ADJUSTMENT (never positive); the leaves plus every adjustment
equal the top row. That sum is an identity of the definition, not a tie: what
ties each adjustment is tie 2, which counts the shared sites in the census.

THE TIES. Each compares two independent readings of the same quantities, and
the self-test plants a wrong figure for each and requires it caught under that
tie's own name:

  1. Ancestry. Every instance equals its own row plus its children for FF,
     RAMB36, RAMB18 and DSP, exactly; for the four LUT columns its sharing
     adjustment must not be positive (a parent can never hold MORE than its
     parts).
  2. Census. Against the census of placed primitive cells: each leaf's FF,
     RAMB36, RAMB18 and DSP equal its count of those cells (a flip-flop in an
     I/O tile counted apart, as the report's FF column is slice registers);
     every row's four LUT columns, leaf or parent, equal the number of
     distinct LUT sites (slice and LUT letter) its cells occupy, split by
     primitive into logic, LUTRAM and SRL, so every leaf's LUT figure and
     every sharing adjustment is read twice; and no census cell is owned by a
     row that is not a leaf.
  3. Flat report. The top row and the slice count equal the flat utilization
     report.
  4. Record. The top row, the slice count and the census's CARRY4 equal the
     recorded route (syn/ooc/pp_resource_baseline.json, the route-1x1
     endpoint unless another is named), and every processor scope that record
     lists equals the map's row for it.
  5. Depth. The deepest reported row lies above the requested depth, so the
     report was not truncated. The census plays no part in this one.

SLICES are attributed, not read: every occupied slice is divided among the
leaves whose cells sit in it, in proportion to the BELs each occupies. Their
sum is the occupied-slice count, which ties 3 and 4 compare.

Two further checks are implied by ties 1 and 2 and kept only as guards on this
script's own bookkeeping, so no arm can isolate them and they are not called
ties: the census totals equal the top row, and the top's own cells split by
name sum to its row.

Usage:

    resmap_map.py map <route_map directory> [--baseline FILE] [--endpoint E]
                      [--out DIR]
    resmap_map.py --selftest

`map` exits 0 when every tie holds, 1 when one fails (each failure printed),
and 2 when an input cannot be read. `--selftest` builds a small consistent
image, proves it ties, then plants one wrong figure per arm and requires each
caught by the tie the arm names.
"""

import argparse
import json
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ooc"))
from pp_baseline_rank import hierarchy, whole  # noqa: E402

REPO = HERE.parent.parent
BASELINE = REPO / "syn" / "ooc" / "pp_resource_baseline.json"
COLUMNS = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP")
ADDITIVE = ("FF", "RAMB36", "RAMB18", "DSP")
SHARED = ("LUT", "logic_LUT", "LUTRAM", "SRL")
#: Census primitive name prefixes per column the census can count exactly.
CENSUS_KINDS = {"FF": ("FDRE", "FDSE", "FDCE", "FDPE"), "RAMB36": ("RAMB36E1",),
                "RAMB18": ("RAMB18E1",), "DSP": ("DSP48E1",), "CARRY4": ("CARRY4",)}
SLICE_SITE = re.compile(r"SLICE_X[0-9]+Y[0-9]+")
#: Primitive levels that occupy a BEL; a MACRO is a wrapper around INTERNAL cells.
BEL_LEVELS = ("LEAF", "INTERNAL")
#: A LUT BEL: the slice's LUT letter, either half (6LUT or 5LUT) of the one LUT site.
LUT_BEL = re.compile(r"SLICE[LM]\.([A-D])[56]LUT")
#: The report's LUT sub-column each primitive on a LUT BEL is counted in.
LUT_KINDS = ((re.compile(r"LUT[1-6]"), "logic_LUT"), (re.compile(r"RAM[DS](32|64E)"), "LUTRAM"),
             (re.compile(r"SRL(16E|C32E)"), "SRL"))
#: Flat-report rows and the map column each one must equal.
FLAT_ROWS = {"Slice LUTs": "LUT", "Slice Registers": "FF", "Slice": "SLICE",
             "RAMB36/FIFO*": "RAMB36", "RAMB18": "RAMB18", "DSPs": "DSP"}
#: The recorded scopes are relative to the wrapper; the map names it in full.
WRAPPER_SUFFIX = "/milan_datapath/pp_shadow"
#: The SoC top is one flat generated module, so its own row is split by cell NAME: a register keeps its
#: signal's name, so flip-flops attribute exactly; a LUT the optimizer renamed is counted as anonymous.
#: First match wins. Every cell lands in exactly one class, so the classes sum to the own row.
NAME_CLASSES = (
    ("DDR3 controller", r"milansoc_sdram|subfragments_bankmachine|subfragments_multiplexer|subfragments_refresher"),
    ("DDR3 PHY", r"milansoc_a7ddrphy|ddram_|OSERDESE2|ISERDESE2|IDELAYE2|IDELAYCTRL|IOBUF"),
    ("Ethernet MAC and PHY", r"milansoc_liteeth|milansoc_maceth|milansoc_mac_|eth0_|eth_|milansoc_packetfifo"),
    ("Milan NIC bridge", r"milansoc_milannic"),
    ("SPI flash", r"milansoc_spiflash|subfragments_litespi|milansoc_mmap|spiflash"),
    ("CSR banks and bus", r"csr_bankarray|socbushandler|milansoc_milansoc|interface[0-9]|milansoc_csr"),
    ("Clock-domain crossings", r"impl_xilinxmultireg|milansoc_.*_cc"),
    ("BIOS ROM and SRAM", r"rom_dat|sram|mem_dat"),
    ("SPI master", r"milansoc_master_"),
    ("Generated FIFO storage", r"storage_"),
    ("Anonymous LUT", r"alinx_ax7101_LUT"),
)


class TieError(Exception):
    """One or more ties failed; the message lists every failure."""


def read_census(path: Path) -> list[tuple[str, str, str, str, str]]:
    """Return (cell, primitive, level, site, bel) for every census row, refusing a short row."""
    rows = []
    lines = path.read_text().splitlines()
    if not lines or lines[0].split("\t") != ["cell", "primitive", "level", "site", "bel"]:
        raise ValueError(f"{path.name}: not a route_map census (bad header)")
    for number, line in enumerate(lines[1:], 2):
        fields = line.split("\t")
        if len(fields) != 5 or not all(fields):
            raise ValueError(f"{path.name}:{number}: expected five non-empty fields")
        rows.append((fields[0], fields[1], fields[2], fields[3], fields[4]))
    return rows


def read_flat(path: Path) -> dict[str, int]:
    """Return the used counts of the flat report's rows named in FLAT_ROWS."""
    found: dict[str, int] = {}
    for line in path.read_text().splitlines():
        fields = [field.strip() for field in line.split("|")[1:-1]]
        if len(fields) >= 2 and fields[0] in FLAT_ROWS and FLAT_ROWS[fields[0]] not in found:
            found[FLAT_ROWS[fields[0]]] = whole(fields[1], f"flat report row {fields[0]!a}")
    missing = sorted(set(FLAT_ROWS.values()) - set(found))
    if missing:
        raise ValueError(f"{path.name}: flat report lacks {missing}")
    return found


def requested_depth(path: Path) -> int:
    """The -hierarchical_depth the report's own command line names."""
    match = re.search(r"-hierarchical_depth ([0-9]+)", path.read_text())
    if not match:
        raise ValueError(f"{path.name}: report names no -hierarchical_depth")
    return int(match.group(1))


def tree_of(rows: dict[str, dict[str, int]]) -> tuple[str, dict[str, list[str]]]:
    """The root instance key and each instance's direct child keys, own rows included."""
    roots = [key for key in rows if "/" not in key]
    if len(roots) != 1:
        raise ValueError(f"expected one top row, found {len(roots)}")
    children: dict[str, list[str]] = defaultdict(list)
    for key in rows:
        if "/" in key:
            children[key.rsplit("/", 1)[0]].append(key)
    return roots[0], dict(children)


def leaves_of(rows: dict[str, dict[str, int]], children: dict[str, list[str]]) -> list[str]:
    """Own rows and childless instances: the blocks that partition the image."""
    return [key for key in rows if key not in children]


def owner_of(cell: str, root: str, instances: set[str], children: dict[str, list[str]]) -> str:
    """The leaf a census cell belongs to: its deepest reported instance, or that one's own row."""
    parts = cell.split("/")[:-1]
    for cut in range(len(parts), -1, -1):
        key = "/".join([root, *parts[:cut]])
        if key in instances:
            return f"{key}/@own" if key in children else key
    raise ValueError(f"census cell {cell!a} has no reported ancestor")


def census_by_leaf(census: list[tuple[str, str, str, str, str]], root: str,
                   rows: dict[str, dict[str, int]], children: dict[str, list[str]]) -> dict[str, dict]:
    """Per leaf: census counts of each CENSUS_KINDS column, and slice shares."""
    instances = {key for key in rows if not key.endswith("/@own")}
    counts: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    occupancy: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for cell, primitive, level, site, _bel in census:
        leaf = owner_of(cell, root, instances, children)
        for column, kinds in CENSUS_KINDS.items():
            if primitive in kinds:
                # The report's FFs are slice registers; a flip-flop packed into an I/O tile is counted apart.
                counts[leaf]["IOB_FF" if column == "FF" and not SLICE_SITE.fullmatch(site) else column] += 1
        if level in BEL_LEVELS and SLICE_SITE.fullmatch(site):
            occupancy[site][leaf] += 1
    for site_cells in occupancy.values():
        total = sum(site_cells.values())
        for leaf, number in site_cells.items():
            counts[leaf]["SLICE"] += number / total
    return {leaf: dict(values) for leaf, values in counts.items()}


def lut_sites(census: list[tuple[str, str, str, str, str]], root: str,
              rows: dict[str, dict[str, int]], children: dict[str, list[str]]) -> dict[str, dict[str, set]]:
    """Per row, leaf or parent: the distinct LUT sites (slice, LUT letter) its cells occupy, for LUT and for
    the sub-column the primitive belongs to. A primitive on a LUT BEL that no LUT_KINDS entry names is refused."""
    instances = {key for key in rows if not key.endswith("/@own")}
    sites: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for cell, primitive, level, site, bel in census:
        match = LUT_BEL.fullmatch(bel)
        if level not in BEL_LEVELS or not match:
            continue
        column = next((name for pattern, name in LUT_KINDS if pattern.fullmatch(primitive)), None)
        if column is None:
            raise ValueError(f"census cell {cell!a}: primitive {primitive} on LUT BEL {bel} has no LUT column")
        node = owner_of(cell, root, instances, children)
        while True:
            for name in ("LUT", column):
                sites[node][name].add((site, match.group(1)))
            if node == root:
                break
            node = node.removesuffix("/@own") if node.endswith("/@own") else node.rsplit("/", 1)[0]
    return sites


def census_sharing(sites: dict[str, dict[str, set]], children: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    """Per parent: the LUT sites the census finds counted in two of its children, per LUT column."""
    return {parent: {column: sum(len(sites.get(kid, {}).get(column, ())) for kid in kids)
                     - len(sites.get(parent, {}).get(column, ())) for column in SHARED}
            for parent, kids in children.items()}


def own_by_name(census: list[tuple[str, str, str, str]], root: str, rows: dict, children: dict) -> dict:
    """The top's own cells split by NAME_CLASSES: FF, LUT cells, LUT-RAM cells, RAMB36, RAMB18, DSP."""
    instances = {key for key in rows if not key.endswith("/@own")}
    own = f"{root}/@own"
    classes: dict[str, dict[str, int]] = {}
    for cell, primitive, level, site, _bel in census:
        if owner_of(cell, root, instances, children) != own or level == "MACRO":
            continue
        label = next((name for name, pattern in NAME_CLASSES if re.match(pattern, cell)), "Other named cells")
        entry = classes.setdefault(label, dict.fromkeys(("FF", "IOB_FF", "LUT_cells", "LUTRAM_cells", "RAMB36",
                                                         "RAMB18", "DSP"), 0))
        if primitive in CENSUS_KINDS["FF"]:
            entry["FF" if SLICE_SITE.fullmatch(site) else "IOB_FF"] += 1
        elif re.fullmatch(r"LUT[1-6]", primitive):
            entry["LUT_cells"] += 1
        elif re.fullmatch(r"RAM[DS](32|64E)|SRL.*", primitive):
            entry["LUTRAM_cells"] += 1
        elif primitive in ("RAMB36E1", "RAMB18E1", "DSP48E1"):
            entry[{"RAMB36E1": "RAMB36", "RAMB18E1": "RAMB18", "DSP48E1": "DSP"}[primitive]] += 1
    return classes


def ancestry_ties(rows: dict[str, dict[str, int]], children: dict[str, list[str]]) -> tuple[list[str], dict]:
    """Tie 1: return the failures and each instance's LUT-sharing adjustment."""
    failures, adjustments = [], {}
    for parent, kids in children.items():
        delta = {column: rows[parent][column] - sum(rows[kid][column] for kid in kids) for column in COLUMNS}
        for column in ADDITIVE:
            if delta[column]:
                failures.append(f"ancestry: {parent} {column} is {rows[parent][column]}, its parts sum to "
                                f"{rows[parent][column] - delta[column]}")
        for column in SHARED:
            if delta[column] > 0:
                failures.append(f"ancestry: {parent} {column} exceeds its parts by {delta[column]}")
        adjustments[parent] = {column: delta[column] for column in SHARED}
    return failures, adjustments


def record_ties(top: dict[str, float], flat: dict[str, int], figures: dict, scopes: dict,
                scope_rows: dict[str, dict]) -> list[str]:
    """Ties 3 and 4: the map's totals against the flat report and the recorded route."""
    failures = []
    for column, value in flat.items():
        if abs(top.get(column, -1) - value) > 1e-6:
            failures.append(f"flat report: {column} is {value}, the map's is {top.get(column)}")
    for column in ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4", "SLICE"):
        if column not in figures:
            failures.append(f"record: no {column} figure to tie")
        elif abs(top.get(column, -1) - figures[column]) > 1e-6:
            failures.append(f"record: {column} recorded {figures[column]}, the map's is {top.get(column)}")
    for scope, recorded in scopes.items():
        mine = scope_rows.get(scope)
        if mine is None:
            failures.append(f"record: scope {scope!a} is not in the map")
            continue
        for column, value in recorded.items():
            if mine.get(column) != value:
                failures.append(f"record: scope {scope!a} {column} recorded {value}, the map's is {mine.get(column)}")
    return failures


def census_ties(rows: dict, leaves: list[str], by_leaf: dict, sites: dict, root: str) -> list[str]:
    """Tie 2: the census agrees with every leaf's FF, RAMB and DSP, with every row's four LUT columns, and owns
    no cell outside the leaves; then the census totals, a bookkeeping guard the tie implies."""
    failures = []
    for leaf in leaves:
        for column in ADDITIVE:
            counted = by_leaf.get(leaf, {}).get(column, 0)
            if counted != rows[leaf][column]:
                failures.append(f"census: {leaf} {column} counts {counted:g} cells, "
                                f"the report says {rows[leaf][column]}")
    for key in rows:
        for column in SHARED:
            counted = len(sites.get(key, {}).get(column, ()))
            if counted != rows[key][column]:
                failures.append(f"census: {key} {column} counts {counted} LUT sites, "
                                f"the report says {rows[key][column]}")
    stray = sorted(set(by_leaf) - set(leaves))
    if stray:
        failures.append(f"census: cells owned by non-leaf rows {stray[:3]}")
    for column in ADDITIVE:
        total = sum(values.get(column, 0) for values in by_leaf.values())
        if total != rows[root][column]:
            failures.append(f"census totals: {column} totals {total:g}, the top row is {rows[root][column]}")
    return failures


def rollup(rows: dict, children: dict, leaves: list[str], by_leaf: dict) -> dict[str, dict[str, float]]:
    """Every row with its report columns plus CARRY4, IOB_FF and SLICE summed up from the leaves."""
    table = {key: dict(rows[key]) for key in rows}
    for key in table:
        table[key].update(CARRY4=0, IOB_FF=0, SLICE=0.0)
    for leaf in leaves:
        extra = by_leaf.get(leaf, {})
        node = leaf
        while True:
            for column in ("CARRY4", "IOB_FF"):
                table[node][column] += int(extra.get(column, 0))
            table[node]["SLICE"] += extra.get("SLICE", 0.0)
            if "/" not in node:
                break
            node = node.rsplit("/", 1)[0]
    return table


def build(directory: Path, figures: dict, scopes: dict) -> dict:
    """Read one route_map directory, tie everything, and return the map or raise TieError."""
    report = directory / "map_hierarchy.rpt"
    rows = hierarchy(report)
    root, children = tree_of(rows)
    leaves = leaves_of(rows, children)
    census = read_census(directory / "map_cells.tsv")
    by_leaf = census_by_leaf(census, root, rows, children)
    sites = lut_sites(census, root, rows, children)
    failures, adjustments = ancestry_ties(rows, children)
    failures += census_ties(rows, leaves, by_leaf, sites, root)
    table = rollup(rows, children, leaves, by_leaf)
    wrapper = next((key for key in table if key.endswith(WRAPPER_SUFFIX)), None)
    scope_rows = {}
    if wrapper is not None:
        scope_rows = {key.removeprefix(wrapper + "/"): table[key] for key in table if key.startswith(wrapper + "/")}
        scope_rows["wrapper"] = table[wrapper]
    failures += record_ties(table[root], read_flat(directory / "map_utilization.rpt"), figures, scopes, scope_rows)
    depth = max(key.count("/") for key in rows)
    if depth >= requested_depth(report):
        failures.append(f"depth: rows reach depth {depth}, the request was {requested_depth(report)}: truncated")
    by_name = own_by_name(census, root, rows, children)
    for column in ("FF", "RAMB36", "RAMB18", "DSP"):
        if sum(entry[column] for entry in by_name.values()) != rows[f"{root}/@own"][column]:
            failures.append(f"names: the top's own {column} by name does not sum to its row")
    if failures:
        raise TieError("\n".join(failures))
    return {"root": root, "leaves": leaves, "table": table, "adjustments": adjustments, "depth": depth,
            "census_sharing": census_sharing(sites, children), "top_own_by_name": by_name}


def ranked(result: dict) -> list[dict]:
    """Every leaf, ranked by LUT then FF, with its share of the image."""
    table, root = result["table"], result["root"]
    order = sorted(result["leaves"], key=lambda key: (-table[key]["LUT"], -table[key]["FF"], key))
    out = []
    for rank, key in enumerate(order, 1):
        row = {"rank": rank, "block": key.removeprefix(root + "/"), **table[key]}
        row["LUT_pct_of_image"] = round(100.0 * table[key]["LUT"] / table[root]["LUT"], 3)
        row["SLICE"] = round(row["SLICE"], 2)
        out.append(row)
    return out


def write_outputs(result: dict, out: Path) -> None:
    """The ranked leaves and every row as TSV, and the whole result as JSON."""
    out.mkdir(parents=True, exist_ok=True)
    rows = ranked(result)
    header = list(rows[0])
    lines = ["\t".join(header)] + ["\t".join(str(row[name]) for name in header) for row in rows]
    (out / "blocks_ranked.tsv").write_text("\n".join(lines) + "\n")
    names = ["instance", "depth", *COLUMNS, "CARRY4", "IOB_FF", "SLICE"]
    every = ["\t".join(names)]
    for key, values in result["table"].items():
        cells = [key, str(key.count("/")), *(str(values[c]) for c in COLUMNS), str(values["CARRY4"]),
                 str(values["IOB_FF"]), f"{values['SLICE']:.2f}"]
        every.append("\t".join(cells))
    (out / "rows_all.tsv").write_text("\n".join(every) + "\n")
    (out / "map.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    (out / "blocks_ranked.md").write_text(markdown_ranking(rows))
    (out / "partition.md").write_text(markdown_partition(result))
    (out / "lut_sharing.md").write_text(markdown_sharing(result))


def number(value: float) -> str:
    """A count as the findings pages print it: thousands separated, slices to one decimal."""
    return f"{value:,.1f}" if isinstance(value, float) and not value.is_integer() else f"{int(value):,}"


PARTITION_COLUMNS = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "IOB_FF", "RAMB36", "RAMB18", "DSP", "CARRY4")


def markdown_partition(result: dict) -> str:
    """The three partition tables, one after another."""
    return "\n".join(partition_tables(result))


def partition_tables(result: dict) -> list[str]:
    """Three tables: the image's direct children, milan_datapath's direct children, the SoC top's own cells by name."""
    table, root = result["table"], result["root"]
    head = ("| Scope | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices "
            "| LUT % of image |\n|---|" + "---:|" * 12 + "\n")
    out = []
    for parent in (root, f"{root}/milan_datapath"):
        kids = sorted((key for key in table if key.rsplit("/", 1)[0] == parent and "/" in key),
                      key=lambda key: (-table[key]["LUT"], key))
        lines = [_partition_row(key.removeprefix(root + "/"), table[key], table[root]["LUT"]) for key in kids]
        adjust = result["adjustments"].get(parent, {})
        lines.append(f"| sharing adjustment | {adjust.get('LUT', 0):,} | {adjust.get('logic_LUT', 0):,} | "
                     f"{adjust.get('LUTRAM', 0):,} | {adjust.get('SRL', 0):,} |" + " 0 |" * 6 + " 0.0 | - |")
        lines.append(_partition_row(f"**{parent.removeprefix(root + '/') if parent != root else root}**",
                                    table[parent], table[root]["LUT"]))
        out.append(head + "\n".join(lines) + "\n")
    names = ("| Name class | FF | IOB FF | LUT cells | LUT-RAM cells | RAMB36 | RAMB18 | DSP |\n"
             "|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for label, entry in sorted(result["top_own_by_name"].items(), key=lambda item: (-item[1]["FF"], item[0])):
        names += (f"| {label} | {entry['FF']:,} | {entry['IOB_FF']:,} | {entry['LUT_cells']:,} | "
                  f"{entry['LUTRAM_cells']:,} | {entry['RAMB36']} | {entry['RAMB18']} | {entry['DSP']} |\n")
    return [*out, names]


def markdown_sharing(result: dict) -> str:
    """The LUT reconciliation: the leaves' LUT sums, every parent's sharing adjustment beside the shared LUT
    sites the census counts under it, and the image's top row, which the first two sum to."""
    table, root = result["table"], result["root"]
    head = ("| Scope | LUT | Logic | LUTRAM | SRL | Shared LUT sites in the census |\n"
            "|---|---:|---:|---:|---:|---:|\n")
    parents = sorted((key for key, adjust in result["adjustments"].items() if any(adjust.values())),
                     key=lambda key: (result["adjustments"][key]["LUT"], key))
    leaves = {column: sum(table[leaf][column] for leaf in result["leaves"]) for column in SHARED}
    lines = [f"| all {len(result['leaves'])} blocks (leaves) | "
             + " | ".join(number(leaves[column]) for column in SHARED) + " | - |"]
    for key in parents:
        adjust, shared = result["adjustments"][key], result["census_sharing"][key]
        label = f"`{key.removeprefix(root + '/')}`" if key != root else f"`{root}` (the image)"
        lines.append(f"| sharing adjustment, {label} | " + " | ".join(number(adjust[column]) for column in SHARED)
                     + f" | {number(shared['LUT'])} |")
    total = {column: sum(adjust[column] for adjust in result["adjustments"].values()) for column in SHARED}
    lines.append(f"| sum of the {len(parents)} adjustments | " + " | ".join(number(total[c]) for c in SHARED)
                 + f" | {number(sum(result['census_sharing'][key]['LUT'] for key in parents))} |")
    lines.append(f"| **image (top row)** | " + " | ".join(f"**{number(table[root][c])}**" for c in SHARED) + " | - |")
    return head + "\n".join(lines) + "\n"


def _partition_row(label: str, values: dict, image_luts: int) -> str:
    """One partition row: a scope's every column, its slices and its share of the image's LUTs."""
    shown = label if label.startswith("**") else f"`{label}`"
    cells = [shown, *(number(values[c]) for c in PARTITION_COLUMNS), f"{values['SLICE']:,.1f}",
             f"{100.0 * values['LUT'] / image_luts:.2f}"]
    return "| " + " | ".join(cells) + " |"


def markdown_ranking(rows: list[dict]) -> str:
    """The ranked leaves as one Markdown table, every column the map carries."""
    head = ("| Rank | Block | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices "
            "| LUT % of image |\n|---:|---|" + "---:|" * 12 + "\n")
    lines = []
    for row in rows:
        cells = [str(row["rank"]), f"`{row['block']}`",
                 *(number(row[c]) for c in ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "IOB_FF", "RAMB36", "RAMB18",
                                            "DSP", "CARRY4")),
                 f"{row['SLICE']:,.1f}", f"{row['LUT_pct_of_image']:.2f}"]
        lines.append("| " + " | ".join(cells) + " |")
    return head + "\n".join(lines) + "\n"


def load_record(baseline: Path, endpoint: str) -> tuple[dict, dict]:
    """The recorded figures and processor scopes of one baseline endpoint."""
    record = json.loads(baseline.read_text())["endpoints"][endpoint]["record"]
    return record["figures"], record.get("scopes", {})


def command_map(args: argparse.Namespace) -> int:
    """Tie one route_map directory against the record, then write the map."""
    try:
        figures, scopes = load_record(args.baseline, args.endpoint)
        result = build(args.directory, figures, scopes)
    except TieError as failure:
        print(f"TIE FAILED:\n{failure}")
        return 1
    except (OSError, ValueError, KeyError) as failure:
        print(f"NOT READABLE: {failure}")
        return 2
    if args.out:
        write_outputs(result, args.out)
    top = result["table"][result["root"]]
    print(f"TIED: {len(result['leaves'])} blocks, depth {result['depth']}; LUT {top['LUT']}, FF {top['FF']}, "
          f"slices {top['SLICE']:.2f}, CARRY4 {top['CARRY4']}, RAMB36 {top['RAMB36']}, RAMB18 {top['RAMB18']}, "
          f"DSP {top['DSP']}")
    return 0


# ---------------------------------------------------------------- self-test


def _row(indent: int, name: str, values: tuple[int, ...]) -> str:
    """One hierarchical report table row at the given indentation."""
    cells = " | ".join(str(value) for value in values)
    return f"|{' ' * indent}{name} | m | {cells} |"


def _fixture(directory: Path) -> tuple[dict, dict]:
    """A consistent three-block image: top own logic, a leaf, and a wrapper with one child."""
    report = [
        "| Command : report_utilization -hierarchical -hierarchical_depth 64",
        _row(1, "top", (10, 9, 1, 0, 8, 1, 0, 1)),
        _row(3, "(top)", (3, 3, 0, 0, 2, 0, 0, 0)),
        _row(3, "leaf", (2, 2, 0, 0, 2, 1, 0, 0)),
        _row(3, "milan_datapath", (6, 5, 1, 0, 4, 0, 0, 1)),
        _row(5, "pp_shadow", (6, 5, 1, 0, 4, 0, 0, 1)),
    ]
    (directory / "map_hierarchy.rpt").write_text("\n".join(report) + "\n")
    flat = ["| Slice LUTs | 10 |", "| Slice Registers | 8 |", "| Slice | 3 |", "| RAMB36/FIFO* | 1 |",
            "| RAMB18 | 0 |", "| DSPs | 1 |"]
    (directory / "map_utilization.rpt").write_text("\n".join(flat) + "\n")
    census = ["cell\tprimitive\tlevel\tsite\tbel",
              "a\tFDRE\tLEAF\tSLICE_X0Y0\tAFF", "b\tFDRE\tLEAF\tSLICE_X0Y0\tBFF",
              "pad_q\tFDRE\tLEAF\tOLOGIC_X0Y1\tOLOGICE2.OUTFF",
              "leaf/c\tFDRE\tLEAF\tSLICE_X1Y0\tAFF", "leaf/d\tFDRE\tLEAF\tSLICE_X1Y0\tBFF",
              "leaf/m\tRAMB36E1\tLEAF\tRAMB36_X0Y0\tRAMB36E1",
              "milan_datapath/pp_shadow/e\tFDRE\tLEAF\tSLICE_X2Y0\tAFF",
              "milan_datapath/pp_shadow/f\tFDRE\tLEAF\tSLICE_X2Y0\tBFF",
              "milan_datapath/pp_shadow/g\tFDRE\tLEAF\tSLICE_X2Y0\tCFF",
              "milan_datapath/pp_shadow/h\tFDRE\tLEAF\tSLICE_X2Y0\tDFF",
              "milan_datapath/pp_shadow/k\tCARRY4\tLEAF\tSLICE_X2Y0\tCARRY4",
              "milan_datapath/pp_shadow/p\tDSP48E1\tLEAF\tDSP48_X0Y0\tDSP48E1",
              # Ten LUT sites: own logic and the leaf share site X1Y0 A (top's adjustment -1), and the processor's
              # one LUT-RAM cell sits inside a MACRO wrapper the census lists apart.
              "o1\tLUT6\tLEAF\tSLICE_X0Y0\tSLICEL.A6LUT", "o2\tLUT6\tLEAF\tSLICE_X0Y0\tSLICEL.B6LUT",
              "o3\tLUT5\tLEAF\tSLICE_X1Y0\tSLICEL.A5LUT",
              "leaf/l1\tLUT6\tLEAF\tSLICE_X1Y0\tSLICEL.A6LUT", "leaf/l2\tLUT6\tLEAF\tSLICE_X1Y0\tSLICEL.B6LUT",
              *(f"milan_datapath/pp_shadow/q{letter}\tLUT6\tLEAF\tSLICE_X2Y0\tSLICEL.{letter}6LUT"
                for letter in "ABCD"),
              "milan_datapath/pp_shadow/q5\tLUT6\tLEAF\tSLICE_X0Y0\tSLICEL.C6LUT",
              "milan_datapath/pp_shadow/rm\tRAM32M\tMACRO\tSLICE_X0Y0\tSLICEM.D6LUT",
              "milan_datapath/pp_shadow/rm/RAMD_D1\tRAMD32\tINTERNAL\tSLICE_X0Y0\tSLICEM.D6LUT"]
    (directory / "map_cells.tsv").write_text("\n".join(census) + "\n")
    figures = {"LUT": 10, "FF": 8, "SLICE": 3, "RAMB36": 1, "RAMB18": 0, "DSP": 1, "CARRY4": 1}
    scopes = {"wrapper": {"LUT": 6, "FF": 4, "DSP": 1, "CARRY4": 1}}
    return figures, scopes


def _plant(directory: Path, name: str, old: str, new: str) -> None:
    """Replace one exact text in a fixture file, refusing a plant that does not land."""
    path = directory / name
    text = path.read_text()
    if text.count(old) != 1:
        raise AssertionError(f"self-test plant {old!a} does not occur exactly once in {name}")
    path.write_text(text.replace(old, new))


#: (what is planted, file, exact old text, new text, the failure text that must appear). Every tie the module
#: docstring names has at least one arm whose failure text only that tie prints, so removing the tie fails the arm:
#: ancestry (child FF, parent LUT), census (flip-flop, I/O flip-flop, leaf LUT, shared LUT site, LUT-RAM, stray
#: owner), flat report (flat LUT), record (recorded total and scope below, CARRY4, slice) and depth.
PLANTS = (
    ("a child FF figure", "map_hierarchy.rpt", "| m | 2 | 2 | 0 | 0 | 2 | 1", "| m | 2 | 2 | 0 | 0 | 3 | 1",
     "ancestry: top FF"),
    ("a parent LUT above its parts", "map_hierarchy.rpt", "|     pp_shadow | m | 6", "|     pp_shadow | m | 5",
     "milan_datapath LUT exceeds its parts"),
    ("the flat LUT total", "map_utilization.rpt", "| Slice LUTs | 10 |", "| Slice LUTs | 11 |",
     "flat report: LUT"),
    ("a census flip-flop", "map_cells.tsv", "leaf/c\tFDRE", "leaf/c\tLUT6", "census: top/leaf FF"),
    ("a census CARRY4", "map_cells.tsv", "pp_shadow/k\tCARRY4", "pp_shadow/k\tLUT6", "record: CARRY4"),
    ("an occupied slice", "map_cells.tsv", "leaf/d\tFDRE\tLEAF\tSLICE_X1Y0", "leaf/d\tFDRE\tLEAF\tSLICE_X9Y9",
     "record: SLICE"),
    ("a truncated depth", "map_hierarchy.rpt", "-hierarchical_depth 64", "-hierarchical_depth 2", "truncated"),
    ("an I/O flip-flop counted as a slice register", "map_cells.tsv", "pad_q\tFDRE\tLEAF\tOLOGIC_X0Y1",
     "pad_q\tFDRE\tLEAF\tSLICE_X0Y0", "census: top/@own FF"),
    ("a leaf's LUT figure outside the recorded scopes", "map_hierarchy.rpt", "|   leaf | m | 2 | 2 |",
     "|   leaf | m | 7 | 7 |", "census: top/leaf LUT counts"),
    ("a LUT site shared by two blocks", "map_cells.tsv", "o3\tLUT5\tLEAF\tSLICE_X1Y0\tSLICEL.A5LUT",
     "o3\tLUT5\tLEAF\tSLICE_X1Y0\tSLICEL.C5LUT", "census: top LUT counts"),
    ("a LUT-RAM cell counted as logic", "map_cells.tsv", "rm/RAMD_D1\tRAMD32", "rm/RAMD_D1\tLUT6",
     "census: top/milan_datapath/pp_shadow LUTRAM counts"),
    ("a cell owned by a row that is not a leaf", "map_cells.tsv",
     "milan_datapath/pp_shadow/p\tDSP48E1\tLEAF\tDSP48_X0Y0\tDSP48E1",
     "milan_datapath/pp_shadow/p\tDSP48E1\tLEAF\tDSP48_X0Y0\tDSP48E1\nmilan_datapath/s\tFDRE\tLEAF\tSLICE_X2Y0\t"
     "SLICEL.A5FF", "census: cells owned by non-leaf rows"),
)


def selftest() -> int:
    """The consistent fixture must tie; every planted wrong figure must be caught by name."""
    problems = []
    with tempfile.TemporaryDirectory(prefix="resmap-map-") as tmp:
        clean = Path(tmp) / "clean"
        clean.mkdir()
        figures, scopes = _fixture(clean)
        result = build(clean, figures, scopes)
        if round(result["table"]["top"]["SLICE"], 6) != 3 or ranked(result)[0]["block"] != "milan_datapath/pp_shadow":
            problems.append("clean fixture: slices or ranking wrong")
        record_plants = (("a recorded total", {**figures, "FF": 9}, scopes, "record: FF"),
                         ("a recorded processor scope", figures, {"wrapper": {"LUT": 7}}, "scope 'wrapper' LUT"))
        for what, planted_figures, planted_scopes, want in record_plants:
            problems += _expect_failure(what, clean, planted_figures, planted_scopes, want)
        for index, (what, name, old, new, want) in enumerate(PLANTS):
            planted = Path(tmp) / f"plant{index}"
            planted.mkdir()
            _fixture(planted)
            _plant(planted, name, old, new)
            problems += _expect_failure(what, planted, figures, scopes, want)
    for problem in problems:
        print(f"SELF-TEST FAILED: {problem}")
    arms = len(PLANTS) + 3
    print(f"resmap_map self-test: {arms - len(problems)} of {arms} arms passed")
    return 1 if problems else 0


def _expect_failure(what: str, directory: Path, figures: dict, scopes: dict, want: str) -> list[str]:
    """One planted arm: the build must raise TieError naming `want`."""
    try:
        build(directory, figures, scopes)
    except TieError as failure:
        return [] if want in str(failure) else [f"{what}: caught, but not as {want!a}: {failure}"]
    return [f"{what}: a planted wrong figure tied clean"]


def main() -> int:
    """The CLI: `map` ties and writes one directory; `--selftest` proves the ties bite."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true", help="plant wrong figures and require each caught")
    sub = parser.add_subparsers(dest="command")
    mapper = sub.add_parser("map", help="tie and rank one route_map.tcl directory")
    mapper.add_argument("directory", type=Path)
    mapper.add_argument("--baseline", type=Path, default=BASELINE)
    mapper.add_argument("--endpoint", default="route-1x1")
    mapper.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.command == "map":
        return command_map(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
