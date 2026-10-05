#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Render the issue #649 models as the Markdown tables its findings page quotes.

Input is models.json from syn/resmap/resmap_models.py, the sweep's
summary.json, the route_map.tcl directory (tied again here through
syn/resmap/resmap_map.py, so the map's tables come from the same check) and the
SoC sweep's exports.json and prices.json, and optionally the out-of-context prices
of the CPU, cache and L2 variants (--soc-variants). Output is tables.md: one
`<!-- table: NAME -->` block per table, so a page quotes each block whole and a
rerun regenerates it byte for byte. Nothing here measures. It formats, and fits
only the SoC variants' per-unit lines, with resmap_models.fit.

Usage:

    resmap_tables.py --work DIR --models DIR --map DIR --out FILE [--soc-variants FILE]
                     [--page PAGE [--write]]
    resmap_tables.py --selftest

With --page, every delimited block in the page is compared with a fresh
generation (exit 1 when one differs or has no generated table); --write fills
them instead.
"""

import argparse
import contextlib
import io
import json
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import resmap_map  # noqa: E402
import resmap_models  # noqa: E402

MEASURES = resmap_models.MEASURES
#: Optional-block points and the routed instance that is the block in the shipping image, when it ships.
ROUTED_BLOCK = {
    "no-mcservo": "milan_datapath/g_mmcm_servo.mmcm_servo",
    "no-ltap": "milan_datapath/aaf_latency_tap_bank",
    "no-maap": "milan_datapath/g_maap.maap_engine",
    "no-rxfilt": "milan_datapath/g_rx_filter.rx_filter",
    "no-gptp-plane": "milan_datapath/g_gptp_plane.u_gptp_shadow",
    "no-aaf-meter": "milan_datapath/g_aaf_meter.aaf_clock_meter",
    "render-0": "milan_datapath/g_tdm_render_live.g_master.chan_tdm_render",
}


def num(value: float | None, places: int = 0) -> str:
    """A figure with thousands separators; a dash for a missing one."""
    if value is None:
        return "-"
    return f"{value:,.{places}f}" if places else f"{round(value):,}"


def signed(value: float, places: int = 0) -> str:
    """A change, always signed."""
    text = num(abs(value), places)
    return ("-" if value < 0 else "+") + text if round(value, places) else "0"


def block_label(path: str) -> str:
    """A Yosys block path without its top, as code."""
    return f"`{path.split('/', 1)[1] if '/' in path else path}`"


def table(head: list[str], rows: list[list[str]], right_from: int = 1, text_last: bool = False) -> str:
    """A Markdown table; columns from `right_from` on are right-aligned, except a last text column."""
    rule = ["---"] * right_from + ["---:"] * (len(head) - right_from)
    if text_last:
        rule[-1] = "---"
    lines = ["| " + " | ".join(head) + " |", "|" + "|".join(rule) + "|"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def stream_tables(models: dict) -> dict[str, str]:
    """The Yosys stream and channel model: total coefficients, per-point data, and the blocks that scale."""
    sm = models["stream_models"]
    total = sm["@total"]
    coefficient_rows = [[m, num(total[m]["coefficients"]["fixed"], 1), num(total[m]["coefficients"]["N"], 1),
                         num(total[m]["coefficients"]["C"], 1), num(total[m]["coefficients"]["NC"], 1),
                         str(total[m]["points"]), num(total[m]["rms"], 1), num(total[m]["max_abs"], 1)]
                        for m in MEASURES]
    data_rows = [[row["point"], str(row["N"]), str(row["C"]), *(num(row[m], 1 if m == "BRAM" else 0) for m in MEASURES),
                  num(total["LUT"]["residuals"][i], 0)] for i, row in enumerate(total["data"])]
    scaling = sorted((b for b in sm if b != "@total"),
                     key=lambda b: -(abs(sm[b]["LUT"]["coefficients"]["N"]) + abs(sm[b]["LUT"]["coefficients"]["NC"])))
    block_rows = [[block_label(b), num(sm[b]["LUT"]["coefficients"]["fixed"]),
                   num(sm[b]["LUT"]["coefficients"]["N"], 1),
                   num(sm[b]["LUT"]["coefficients"]["C"], 1), num(sm[b]["LUT"]["coefficients"]["NC"], 1),
                   num(sm[b]["LUT"]["rms"], 1), num(sm[b]["FF"]["coefficients"]["N"], 1), num(sm[b]["FF"]["rms"], 1)]
                  for b in scaling[:14]]
    return {
        "yosys-stream-total": table(["Measure", "Fixed", "Per stream", "Per channel", "Per stream-channel", "Points",
                                     "Residual RMS", "Largest residual"], coefficient_rows),
        "yosys-stream-data": table(["Point", "N", "C", *MEASURES, "LUT residual"], data_rows),
        "yosys-stream-blocks": table(["Block", "LUT fixed", "LUT per stream", "LUT per channel", "LUT per N*C",
                                      "LUT RMS", "FF per stream", "FF RMS"], block_rows),
    }


def vivado_tables(models: dict) -> dict[str, str]:
    """The Vivado anchors: totals per stream count and the per-stream fit, after synthesis and optimization."""
    out = {}
    for stage, label in (("opt", "after optimization"), ("synth", "after synthesis")):
        stage_models = models["vivado_stream_models"].get(stage)
        if not stage_models:
            continue
        total = stage_models["@total"]
        rows = [[row["point"], str(row["N"]), *(num(row[m], 1 if m == "BRAM" else 0) for m in MEASURES),
                 num(total["LUT"]["residuals"][i])] for i, row in enumerate(total["data"])]
        fits = [[m, num(total[m]["coefficients"]["fixed"], 1), num(total[m]["coefficients"]["N"], 1),
                 str(total[m]["points"]), num(total[m]["rms"], 1), num(total[m]["max_abs"], 1)] for m in MEASURES]
        out[f"vivado-{stage}-data"] = table(["Anchor", "N", *MEASURES, "LUT residual"], rows)
        out[f"vivado-{stage}-fit"] = table(["Measure " + label, "Fixed", "Per stream", "Points", "Residual RMS",
                                            "Largest residual"], fits)
        blocks = sorted((b for b in stage_models if b != "@total"),
                        key=lambda b: -abs(stage_models[b]["LUT"]["coefficients"]["N"]))
        out[f"vivado-{stage}-blocks"] = table(
            ["Block", "LUT at N=1", "LUT per stream", "LUT RMS", "FF per stream", "BRAM per stream"],
            [[block_label(b), num(stage_models[b]["data"][0]["LUT"]),
              num(stage_models[b]["LUT"]["coefficients"]["N"], 1),
              num(stage_models[b]["LUT"]["rms"], 1), num(stage_models[b]["FF"]["coefficients"]["N"], 1),
              num(stage_models[b]["BRAM"]["coefficients"]["N"], 2)] for b in blocks[:14]])
    return out


def marginal_table(marginals: dict, routed: dict | None, ratio: float | None) -> str:
    """Each point against its reference: the change, and the blocks that moved most."""
    rows = []
    for name, entry in marginals.items():
        delta = entry["delta"]
        moved = "; ".join(f"{block_label(b)} {signed(c['LUT'])}" for b, c in entry["moved"][:3])
        block = ROUTED_BLOCK.get(name)
        in_image = routed.get(block) if routed and block else None
        label = f"{name} (refused by a guard)" if entry.get("refusals") else name
        rows.append([label, ", ".join(f"`{k}`={v}" for k, v in entry["changes"].items()) or entry["shape"],
                     *(signed(delta[m], 1 if m == "BRAM" else 0) for m in MEASURES),
                     num(delta["LUT"] * ratio) if ratio else "-",
                     f"{num(in_image['LUT'])} / {num(in_image['FF'])}" if in_image else "-", moved])
    return table(["Point", "Change", "LUT", "FF", "BRAM", "DSP", "LUT x calibration", "Routed block LUT / FF",
                  "Blocks that moved most (LUT)"], rows, right_from=2, text_last=True)


def parameter_table(models: dict) -> str:
    """Each processor parameter: its points, per-unit cost and residuals."""
    rows = []
    for key, entry in models["processor_models"].items():
        xs = ", ".join(num(row["x"]) for row in entry["data"])
        rows.append([f"`{key}`", xs, num(entry["LUT"]["coefficients"]["x"], 2),
                     num(entry["FF"]["coefficients"]["x"], 2),
                     num(entry["BRAM"]["coefficients"]["x"], 3), num(entry["LUT"]["rms"], 1),
                     num(entry["LUT"]["max_abs"], 1)])
    return table(["Parameter", "Values", "LUT per unit", "FF per unit", "BRAM per unit", "LUT residual RMS",
                  "Largest LUT residual"], rows, right_from=2)


def calibration_tables(models: dict) -> dict[str, str]:
    """Vivado over Yosys at each anchor, totals and per block; routed over out of context at 1x1."""
    rows = []
    for name, entry in models["calibration"].items():
        totals = entry["totals"]
        flat = totals["yosys_flat"] or {}
        for m in ("LUT", "FF"):
            rows.append([name, m, num(totals["yosys_hier"][m]), num(flat.get(m)),
                         num((totals["vivado_synth"] or {}).get(m)), num(totals["vivado_opt"][m]),
                         num(totals["vivado_opt"][m] / totals["yosys_hier"][m], 3),
                         num(totals["vivado_opt"][m] / flat[m], 3) if flat.get(m) else "-"])
    out = {"calibration-totals": table(["Anchor", "Measure", "Yosys hierarchical", "Yosys flattened", "Vivado synth",
                                        "Vivado opt", "Opt / hierarchical", "Opt / flattened"], rows, right_from=2)}
    ship = models["calibration"].get("ship")
    context = models.get("in_context", {})
    if ship:
        blocks = sorted(ship["blocks"].items(), key=lambda item: -item[1]["vivado"]["LUT"])
        out["calibration-blocks"] = table(
            ["Block", "Yosys LUT", "Vivado opt LUT", "Opt / Yosys LUT", "Opt / Yosys FF", "Routed LUT", "Routed / opt"],
            [[block_label(b), num(e["yosys"]["LUT"]), num(e["vivado"]["LUT"]), num(e["ratio_LUT"], 3),
              num(e["ratio_FF"], 3), num((context.get(b) or {}).get("routed", {}).get("LUT")),
              num((context.get(b) or {}).get("ratio_LUT"), 3)] for b, e in blocks])
    return out


def soc_tables(work: Path) -> dict[str, str]:
    """The SoC variants: each one's flags as the plan states them, its outcome, and the prices of the accepted."""
    exports = json.loads((work / "soc" / "exports.json").read_text())
    prices = json.loads((work / "soc" / "prices.json").read_text())
    variants = json.loads(resmap_models.yosys_sweep.PLAN.read_text())["soc"]["variants"]
    outcome = []
    for name, record in exports.items():
        spec = variants[name]
        flags = [f"`{flag} {value}`" for flag, value in spec.get("set", {}).items()]
        flags += [f"`{flag}`" for flag in spec.get("add", [])]
        outcome.append([name, ", ".join(flags) or "as shipped", "accepted" if record["rc"] == 0 else "refused",
                        f"`{record['refusal'].split('error: ', 1)[-1]}`" if record["refusal"] else "-"])
    priced = [[name, part, *(num(p[part]["totals"][c]) for c in ("LUT_TOT", "FF", "RAMB36", "RAMB18", "DSP"))]
              for name, p in prices.items() for part in ("cpu", "top")]
    return {"soc-outcomes": table(["Variant", "Changed flags", "Outcome", "Refusal"], outcome, right_from=4),
            "soc-prices": table(["Variant", "Part", "LUT", "FF", "RAMB36", "RAMB18", "DSP"], priced, right_from=2)}


#: The SoC variant parameters with a numeric axis, the unit each is fitted per, and the variants on it (the
#: shipping variant is the 1 of the CPU-count axis; the L2 and L1 lines start at their smallest present size).
#: The L2 line is on the core with both L1 caches: the cacheless shipping core's generator instantiates no L2.
SOC_AXES = (("L2 bytes, both L1 caches", "KiB of L2", ("l1l2-8k", "l1l2-16k", "l1l2-32k")),
            ("CPU count", "core", ("ship", "cpu2", "cpu4")),
            ("L1 caches", "way of both L1 caches", ("l1-caches", "l1-w2", "l1-w4")))
PROFILE = "not buildable under the shipping software profile"
#: The order the variant tables list parameters in; within one, by the axis value, then by name.
SOC_ORDER = ("shipping", "CPU count", "XLEN", "recipe --with-fpu", "ISA extensions", "FPU (core option)", "L1 caches",
             "L2 bytes", "L2 bytes, both L1 caches", "core")


def soc_order(item: tuple[str, dict]) -> tuple:
    """Sort key of one priced variant: its parameter's place in SOC_ORDER, its axis value, its name."""
    name, entry = item
    place = SOC_ORDER.index(entry["parameter"]) if entry["parameter"] in SOC_ORDER else len(SOC_ORDER)
    return place, entry.get("x") or 0, name


def soc_variant_tables(prices: dict, stage: str = "synth") -> dict[str, str]:
    """The CPU, cache and L2 variants priced out of context from the scratch recipe copy, after synthesis (the
    black-boxed datapath stops opt_design): each variant's SoC and CPU-core figures and its change from the
    shipping variant, the per-unit fits on the numeric axes, the variants that could not be generated with the
    reason, and each run's receipt."""
    ship = vivado_measures_of(prices["ship"][stage]["total"])
    rows, missing = [], []
    for name, entry in sorted(prices.items(), key=soc_order):
        if name == "ship-tracked":
            continue
        if stage not in entry:
            reason = entry["export"].get("reason") or (entry["export"].get("error_tail") or ["no report"])[-1]
            missing.append([name, entry["parameter"], entry["value"], f"`{reason.strip()[:150]}`"])
            continue
        total, cpu = vivado_measures_of(entry[stage]["total"]), vivado_measures_of(entry[stage]["cpu"])
        rows.append([name, entry["parameter"], entry["value"], "ships" if name == "ship" else PROFILE,
                     *(num(total[m], 1 if m == "BRAM" else 0) for m in MEASURES),
                     *(signed(total[m] - ship[m], 1 if m == "BRAM" else 0) for m in MEASURES),
                     *(num(cpu[m], 1 if m == "BRAM" else 0) for m in MEASURES)])
    fits = []
    for parameter, unit, names in SOC_AXES:
        present = [n for n in names if stage in prices.get(n, {})]
        if len(present) < 3:
            fits.append([parameter, unit, ", ".join(present), "fewer than three points", *["-"] * 5])
            continue
        data = [{"x": float(prices[n]["x"] if n != "ship" else 1), **vivado_measures_of(prices[n][stage]["total"])}
                for n in present]
        model = {m: resmap_models.fit(data, ("x",), m) for m in ("LUT", "FF", "BRAM")}
        fits.append([parameter, unit, ", ".join(num(row["x"]) for row in data), str(len(data)),
                     num(model["LUT"]["coefficients"]["x"], 1), num(model["FF"]["coefficients"]["x"], 1),
                     num(model["BRAM"]["coefficients"]["x"], 2), num(model["LUT"]["rms"], 1),
                     num(model["LUT"]["max_abs"], 1)])
    head = ["Variant", "Parameter", "Value", "Profile", *(f"SoC {m}" for m in MEASURES),
            *(f"Change {m}" for m in MEASURES), *(f"CPU core {m}" for m in MEASURES)]
    out = {"soc-variant-prices": table(head, rows, right_from=4),
           "soc-variant-fits": table(["Parameter", "Per", "Values", "Points", "LUT per unit", "FF per unit",
                                      "BRAM per unit", "LUT residual RMS", "Largest LUT residual"], fits,
                                     right_from=2)}
    out["soc-variant-not-generated"] = table(["Variant", "Parameter", "Value", "Why it was not generated"],
                                             missing or [["none", "-", "-", "-"]], right_from=4)
    receipts = ["| Variant | rc | Minutes under the lock | Log | Log SHA-256, first 16 | Log bytes |",
                "|---|---:|---:|---|---|---:|"]
    for name, entry in sorted(prices.items(), key=soc_order):
        run = entry.get("vivado")
        if run is None:
            continue
        minutes = (datetime.fromisoformat(run["end"]) - datetime.fromisoformat(run["start"])).total_seconds() / 60
        receipts.append(f"| {name} | {run['rc']} | {num(minutes, 1)} | `ooc.log` | `{run['log_sha256'][:16]}` | "
                        f"{num(run['log_bytes'])} |")
    out["soc-variant-receipts"] = "\n".join(receipts) + "\n"
    return out


def vivado_measures_of(counts: dict) -> dict[str, float]:
    """A hierarchical-report row in the four model columns."""
    return resmap_models.vivado_measures(counts)


def redundancy_table(map_dir: Path) -> str:
    """The plan's per-port blocks, each as the route places it, and their sum."""
    spec = json.loads(resmap_models.yosys_sweep.PLAN.read_text())["redundancy"]
    rows_by_path = {key.split("/", 1)[1]: counts for key, _module, counts in
                    resmap_models.vivado_rows(map_dir / "map_hierarchy.rpt") if "/" in key}
    rows, total = [], dict.fromkeys(("LUT", "FF", "RAMB36", "RAMB18", "DSP"), 0)
    for block in spec["blocks"]:
        counts = rows_by_path[block]
        rows.append([f"`{block}`", *(num(counts[c]) for c in total)])
        for column in total:
            total[column] += counts[column]
    rows.append(["**sum**", *(f"**{num(total[c])}**" for c in total)])
    return table(["Routed block", "LUT", "FF", "RAMB36", "RAMB18", "DSP"], rows)


def refusal_table(guards: dict) -> str:
    """Every refused point, who refused it (the builder, before any shape existed, or an elaboration
    guard) and the refusal, its location prefix dropped."""
    builder = set(guards.get("by_builder", []))
    rows = [[name, "builder" if name in builder else "elaboration guard",
             "; ".join(f"`{message.split(': ', 1)[-1]}`" for message in messages)]
            for name, messages in sorted(guards["refused"].items())]
    return table(["Point", "Refused by", "Refusal"], rows or [["none", "-", "-"]], right_from=3)


def render(sections: dict[str, str]) -> str:
    """Every table in a named, delimited block."""
    return "".join(f"<!-- table: {name} -->\n{body}<!-- end table: {name} -->\n\n" for name, body in sections.items())


def fill(page: str, sections: dict[str, str]) -> tuple[str, list[str]]:
    """The page with every delimited block replaced by its generated table, and the names it lacks a table for."""
    missing = []

    def replace(match: re.Match) -> str:
        """One block: its generated body, or the block unchanged and its name recorded."""
        name = match.group(1)
        if name not in sections:
            missing.append(name)
            return match.group(0)
        return f"<!-- table: {name} -->\n{sections[name]}<!-- end table: {name} -->"

    return BLOCK.sub(replace, page), missing


#: One delimited table block in a page.
BLOCK = re.compile(r"<!-- table: ([a-z0-9-]+) -->\n.*?<!-- end table: \1 -->", re.S)


def build(args: argparse.Namespace) -> dict[str, str]:
    """Every table from the four inputs, by name."""
    models = json.loads((args.models / "models.json").read_text())
    routed_rows = resmap_models.vivado_rows(args.map / "map_hierarchy.rpt")
    routed = {f"milan_datapath/{key.split('/milan_datapath/', 1)[1]}": resmap_models.vivado_measures(counts)
              for key, _module, counts in routed_rows if "/milan_datapath/" in key}
    ratio = None
    ship = models["calibration"].get("ship")
    if ship:
        ratio = ship["totals"]["vivado_opt"]["LUT"] / ship["totals"]["yosys_hier"]["LUT"]
    figures, scopes = resmap_map.load_record(resmap_map.BASELINE, "route-1x1")
    image = resmap_map.build(args.map, figures, scopes)
    image_table, datapath_table, names_table = resmap_map.partition_tables(image)
    sections = {"map-image": image_table, "map-datapath": datapath_table, "map-soc-names": names_table,
                "map-lut-sharing": resmap_map.markdown_sharing(image),
                "map-ranking": resmap_map.markdown_ranking(resmap_map.ranked(image)),
                **stream_tables(models), **vivado_tables(models)}
    sections["datapath-marginals"] = marginal_table(models["datapath_marginals"], routed, ratio)
    sections["processor-marginals"] = marginal_table(models["processor_marginals"], None, None)
    sections["processor-parameters"] = parameter_table(models)
    sections["adp-marginals"] = marginal_table(models["adp_marginals"], None, None)
    if models.get("tdm_model"):
        tdm = models["tdm_model"]
        sections["tdm-model"] = table(["Point", "Capture slots", *MEASURES],
                                      [[row["point"], num(row["x"]), *(num(row[m], 1 if m == "BRAM" else 0)
                                                                        for m in MEASURES)] for row in tdm["data"]])
    sections.update(calibration_tables(models))
    sections["redundancy-blocks"] = redundancy_table(args.map)
    sections["guard-refusals"] = refusal_table(models["guards"])
    if (args.work / "soc" / "prices.json").is_file():
        sections.update(soc_tables(args.work))
    if args.soc_variants is not None:
        sections.update(soc_variant_tables(json.loads(args.soc_variants.read_text())))
    return sections


def selftest() -> int:
    """Formatting: separators, signs, the block delimiters and who refused each refused point."""
    problems = []
    if num(50767) != "50,767" or num(0.5, 1) != "0.5" or num(None) != "-":
        problems.append("num formats wrong")
    if signed(-12) != "-12" or signed(3) != "+3" or signed(0) != "0":
        problems.append("signed formats wrong")
    filled, missing = fill("x\n<!-- table: a -->\nold\n<!-- end table: a -->\n<!-- table: b -->\n"
                           "<!-- end table: b -->\n", {"a": "new\n"})
    if filled != ("x\n<!-- table: a -->\nnew\n<!-- end table: a -->\n<!-- table: b -->\n<!-- end table: b -->\n")\
            or missing != ["b"]:
        problems.append(f"fill wrong: {filled!a} {missing}")
    text = render({"a": table(["X", "Y"], [["1", "2"]])})
    if "<!-- table: a -->\n| X | Y |\n|---|---:|\n| 1 | 2 |\n<!-- end table: a -->" not in text:
        problems.append(f"render wrong: {text!a}")
    problems += _selftest_page_check()
    problems += _selftest_soc_variants()
    refused = refusal_table({"refused": {"g": ["a.sv:1:5: N_P=9 outside 1..8"], "b": ["CONFIG ERROR: 9 names"]},
                             "by_builder": ["b"]})
    if "| b | builder | `9 names` |" not in refused or "| g | elaboration guard | `N_P=9 outside 1..8` |" \
            not in refused:
        problems.append(f"refusal table: who refused each point is wrong: {refused!a}")
    for problem in problems:
        print(f"SELF-TEST FAILED: {problem}")
    print(f"resmap_tables self-test: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


def _selftest_soc_variants() -> list[str]:
    """The SoC variant tables: changes are taken from the shipping variant, an exact L2 line fits with no
    residual, an axis with fewer than three priced points is said so, and an ungenerated variant is listed."""
    def priced(lut: float, x: float | None, parameter: str) -> dict:
        """One priced variant: the SoC at `lut` LUTs, its core at a tenth of that."""
        counts = {"LUT": lut, "FF": 2 * lut, "RAMB36": 1, "RAMB18": 0, "DSP": 0}
        return {"parameter": parameter, "value": str(x), "x": x, "export": {"rc": 0},
                "synth": {"total": counts, "cpu": {**counts, "LUT": lut / 10}}}
    prices = {"ship": priced(1000, None, "shipping"), "cpu2": priced(1900, 2, "CPU count"),
              **{f"l1l2-{k}k": priced(1100 + 3 * k, k, "L2 bytes, both L1 caches") for k in (8, 16, 32)},
              "fpu-f": {"parameter": "FPU", "value": "F", "x": None,
                        "export": {"rc": 1, "error_tail": ["[error] Can't find the service X"]}}}
    out = soc_variant_tables(prices)
    problems = []
    if "| l1l2-8k | L2 bytes, both L1 caches | 8 | " + PROFILE + " | 1,124 | 2,248 | 1.0 | 0 | +124 | +248 | 0 | 0 |" \
            not in out["soc-variant-prices"]:
        problems.append(f"soc variants: the change from shipping is wrong: {out['soc-variant-prices']!a}")
    if "| L2 bytes, both L1 caches | KiB of L2 | 8, 16, 32 | 3 | 3.0 | 6.0 | 0.00 | 0.0 | 0.0 |" \
            not in out["soc-variant-fits"]:
        problems.append(f"soc variants: the exact L2 line was not recovered: {out['soc-variant-fits']!a}")
    if "| CPU count | core | ship, cpu2 | fewer than three points |" not in out["soc-variant-fits"]:
        problems.append("soc variants: a two-point axis was fitted")
    if "| fpu-f | FPU | F | `[error] Can't find the service X` |" not in out["soc-variant-not-generated"]:
        problems.append("soc variants: the ungenerated variant is not listed with its reason")
    return problems


def _selftest_page_check() -> list[str]:
    """The page check passes a page equal to a fresh generation and fails a stale block and a block with
    no generated table, and --write fills the stale page to equality."""
    problems = []
    sections = {"a": "new\n"}
    with tempfile.TemporaryDirectory(prefix="resmap-tables-") as tmp:
        page = Path(tmp) / "page.md"
        for label, body, want in (("an equal page", "<!-- table: a -->\nnew\n<!-- end table: a -->\n", 0),
                                  ("a stale block", "<!-- table: a -->\nold\n<!-- end table: a -->\n", 1),
                                  ("a block with no table", "<!-- table: z -->\nx\n<!-- end table: z -->\n", 1)):
            page.write_text(body)
            with contextlib.redirect_stdout(io.StringIO()):
                got = check_page(argparse.Namespace(page=page, write=False), sections)
            if got != want:
                problems.append(f"page check: {label} gave {got}, wanted {want}")
        page.write_text("<!-- table: a -->\nold\n<!-- end table: a -->\n")
        with contextlib.redirect_stdout(io.StringIO()):
            check_page(argparse.Namespace(page=page, write=True), sections)
            if check_page(argparse.Namespace(page=page, write=False), sections):
                problems.append("page check: a filled page does not then check equal")
    return problems


def main() -> int:
    """The CLI; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work", type=Path)
    parser.add_argument("--models", type=Path)
    parser.add_argument("--map", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--soc-variants", type=Path,
                        help="the CPU, cache and L2 variants' out-of-context prices (the scratch pricing receipts)")
    parser.add_argument("--page", type=Path, help="a page whose delimited table blocks are checked, or filled")
    parser.add_argument("--write", action="store_true", help="fill the page's blocks instead of checking them")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if None in (args.work, args.models, args.map, args.out):
        parser.print_help()
        return 2
    sections = build(args)
    args.out.write_text(render(sections))
    print(f"tables: {args.out}")
    if args.page is None:
        return 0
    return check_page(args, sections)


def check_page(args: argparse.Namespace, sections: dict[str, str]) -> int:
    """Fill (--write) or check the page's delimited blocks: 1 when a block has no generated table or,
    checking, when any block differs from a fresh generation."""
    text, missing = fill(args.page.read_text(), sections)
    if missing:
        print(f"page: no generated table for {missing}")
        return 1
    if args.write:
        args.page.write_text(text)
        print(f"page: {args.page} filled")
        return 0
    stale = text != args.page.read_text()
    print(f"page: {'tables differ from a fresh generation' if stale else 'every table equals a fresh generation'}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
