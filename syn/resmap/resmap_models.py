#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Models, marginals and calibration for the issue #649 sweep.

Reads what syn/resmap/yosys_sweep.py and syn/resmap/datapath_ooc.tcl left in a
work directory (summary.json and vivado/<point>/*_hierarchy.rpt) and the
whole-image map syn/resmap/resmap_map.py wrote, and writes models.json and
models.md: every table the findings page quotes, generated, so no figure is
copied by hand.

The models:

  streams and channels  per block, y = a + b*N + c*C + d*N*C, fitted by least
                        squares over every point that varies only N (streams
                        per direction) and C (channels per stream); residuals
                        per point, their RMS and their largest magnitude
  Vivado streams        the same blocks at the Vivado anchors, y = a + b*N
  processor parameters  y = a + b*x per parameter over its points, KL_pp_shadow
                        with every other parameter at the shipping value
  marginals             each single-change point minus the shipping point,
                        total and the blocks that moved most
  calibration           Vivado over Yosys at each anchor, per block and total,
                        and the routed image over Vivado out of context

BRAM is counted in tiles: a RAMB36 is one, a RAMB18 half.

GUARDS FAIL CLOSED. A point enters a fit, a calibration ratio or the TDM model only
when its guard record (yosys_sweep.py guards, carried into summary.json) is clean.
A point whose record lists a firing elaboration guard is a shape the product
refuses: it is left out of every fit and shown in the marginal tables as refused.
A point whose shape the builder refused (summary.json's "builder" record, #652)
was never priced: it is refused with the builder's line, left out of every fit,
and has no marginal. A point with no record, or whose lint hit a hard error, is
not known to be buildable, so the build stops naming it rather than fitting it as
clean.

Usage:

    resmap_models.py --work DIR --map DIR --out DIR
    resmap_models.py --selftest
"""

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "ooc"))
import yosys_sweep  # noqa: E402
from pp_baseline_rank import whole  # noqa: E402

VIVADO_FIELDS = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP")
#: The four columns every model and table carries.
MEASURES = ("LUT", "FF", "BRAM", "DSP")
#: The plan parameters that set N and C on a milan_datapath point.
STREAM_PARAM, CHANNEL_PARAM = "N_STREAMS", "TALKER_WIRE_CHANS_P"
UNIQUIFIED = re.compile(r"(?:__parameterized[0-9]+)?(?:_[0-9]+)?$")


def yosys_measures(figures: dict) -> dict[str, float]:
    """Yosys figures in the four model columns: LUT is LUT_TOT (logic plus LUT RAM equivalents)."""
    return {"LUT": figures["LUT_TOT"], "FF": figures["FF"], "BRAM": figures["RAMB36"] + figures["RAMB18"] / 2,
            "DSP": figures["DSP"]}


def vivado_measures(figures: dict) -> dict[str, float]:
    """Vivado report figures in the four model columns: LUT is Total LUTs."""
    return {"LUT": figures["LUT"], "FF": figures["FF"], "BRAM": figures["RAMB36"] + figures["RAMB18"] / 2,
            "DSP": figures["DSP"]}


# --------------------------------------------------------------- Vivado


def vivado_rows(path: Path) -> list[tuple[str, str, dict[str, int]]]:
    """(instance path, module, counts) for every row of a hierarchical report, own rows included."""
    rows, ancestors = [], []
    for line in path.read_text().splitlines():
        fields = line.split("|")[1:-1]
        if len(fields) != 10 or fields[2].strip() == "Total LUTs":
            continue
        indent = len(fields[0]) - len(fields[0].lstrip())
        depth = (indent - 1) // 2
        name = fields[0].strip()
        if name.startswith("("):
            name = "@own"
        else:
            ancestors = ancestors[:depth] + [name]
        key = "/".join(ancestors[:depth] + [name])
        counts = {field: whole(value.strip(), f"{key!a} count") for field, value in zip(VIVADO_FIELDS, fields[2:])}
        rows.append((key, fields[1].strip(), counts))
    if not rows:
        raise ValueError(f"{path}: no hierarchical rows")
    return rows


def vivado_blocks(rows: list, known: set[str]) -> dict[str, dict[str, float]]:
    """The top's own row and each direct child summed by source module name, as Yosys names blocks."""
    top = rows[0][0]
    out: dict[str, dict[str, float]] = {}
    for key, module, counts in rows:
        if key.count("/") != 1:
            continue
        name = "@own" if key.endswith("/@own") else _source_module(module, known)
        entry = out.setdefault(f"{top}/{name}", dict.fromkeys(MEASURES, 0.0))
        for column, value in vivado_measures(counts).items():
            entry[column] += value
    return out


def _source_module(module: str, known: set[str]) -> str:
    """Vivado's uniquified module name mapped back to a source name Yosys also reports, when one matches."""
    stripped = UNIQUIFIED.sub("", module)
    for candidate in (module, stripped, re.sub(r"__parameterized[0-9]+$", "", module)):
        if candidate in known:
            return candidate
    return stripped


# ---------------------------------------------------------------- fits


def fit(rows: list[dict[str, float]], terms: tuple[str, ...], target: str) -> dict:
    """Least squares of target on 1 and the named terms; coefficients, residuals and their summary.
    A design that cannot determine every term (too few or collinear points) is refused, never fitted
    to its minimum-norm solution."""
    design = np.array([[1.0] + [row[t] for t in terms] for row in rows])
    values = np.array([row[target] for row in rows])
    coefficients, _, rank, _ = np.linalg.lstsq(design, values, rcond=None)
    if rank < design.shape[1]:
        raise ValueError(f"fit of {target} on {terms}: rank {rank} over {len(rows)} points, "
                         f"{design.shape[1]} terms needed")
    residuals = values - design @ coefficients
    return {"coefficients": dict(zip(("fixed", *terms), (round(float(c), 2) for c in coefficients))),
            "residuals": [round(float(r), 2) for r in residuals], "points": len(rows), "rank": int(rank),
            "rms": round(float(np.sqrt(np.mean(residuals ** 2))), 2),
            "max_abs": round(float(np.max(np.abs(residuals))), 2)}


class GuardError(ValueError):
    """A point carries no usable guard record, so whether the product can build its shape is unknown."""


def refusals(summary: dict, name: str) -> list[str]:
    """The elaboration guards that fired on one point, as yosys_sweep.py guards recorded them, or the
    builder's refusal of its shape. A point with neither record, or whose lint hit a hard error, raises
    GuardError: an unchecked shape is never clean."""
    builder = summary.get(name, {}).get("builder")
    if builder is not None:
        return [builder["refusal"]]
    guards = summary.get(name, {}).get("guards")
    if guards is None:
        raise GuardError(f"{name}: no guard record; run yosys_sweep.py guards, then summary")
    if guards.get("errors") or (guards.get("rc") and not guards.get("refusals")):
        raise GuardError(f"{name}: the guard lint exited {guards.get('rc')} with hard errors {guards.get('errors')}")
    return guards.get("refusals", [])


def stream_channel_points(plan: dict, summary: dict) -> list[tuple[str, int, int]]:
    """Every milan_datapath point that changes nothing but N and C, with its N and C; a point an
    elaboration guard refuses is left out, as a shape the product cannot build."""
    base = plan["tops"]["milan_datapath"]["params"]
    out = []
    for point in plan["points"]:
        params = point.get("params", {})
        if point["top"] != "milan_datapath" or set(params) - {STREAM_PARAM, CHANNEL_PARAM}:
            continue
        if point.get("patch") or point["name"] not in summary or refusals(summary, point["name"]):
            continue
        shape = point.get("shape", "")
        if shape and not re.fullmatch(r"rm_ax7101_[0-9]+x[0-9]+_tdm8(_[0-9]+ch)?", shape):
            continue
        out.append((point["name"], params.get(STREAM_PARAM, base[STREAM_PARAM]),
                    params.get(CHANNEL_PARAM, base[CHANNEL_PARAM])))
    return out


def stream_models(plan: dict, summary: dict, level: str = "blocks1") -> dict:
    """Per block and total: y = a + b*N + c*C + d*N*C over the stream and channel points (Yosys).

    `level` names the summary's block set: "blocks1" is one level below the top, "blocks" the deeper one.
    """
    points = stream_channel_points(plan, summary)
    blocks = sorted({b for name, _, _ in points for b in summary[name]["hierarchical"][level]})
    models = {}
    for block in ["@total", *blocks]:
        rows = []
        for name, streams, channels in points:
            source = summary[name]["hierarchical"]
            figures = source["totals"] if block == "@total" else source[level].get(block)
            if figures is None:
                figures = dict.fromkeys(yosys_sweep.COLUMNS, 0)
            rows.append({"point": name, "N": streams, "C": channels, "NC": streams * channels,
                         **yosys_measures(figures)})
        models[block] = {"data": rows, **{m: fit(rows, ("N", "C", "NC"), m) for m in MEASURES}}
    return models


def vivado_stream_models(anchors: dict[str, dict], plan: dict, summary: dict) -> dict:
    """Totals and blocks at the Vivado anchors on the stream line (the shipping shape at N streams):
    y = a + b*N, after synthesis and after optimization. An anchor off the line calibrates but is not fitted."""
    line = {name: streams for name, streams, channels in stream_channel_points(plan, summary) if channels == 8}
    streams = {name: line[name] for name in anchors if name in line}
    out = {}
    for stage in ("synth", "opt"):
        present = {name: data[stage] for name, data in anchors.items() if stage in data and name in streams}
        if len(present) < 2:
            continue
        blocks = sorted({b for data in present.values() for b in data["blocks"]})
        stage_models = {}
        for block in ["@total", *blocks]:
            rows = [{"point": name, "N": streams[name],
                     **(data["totals"] if block == "@total" else data["blocks"].get(block, dict.fromkeys(MEASURES, 0)))}
                    for name, data in sorted(present.items(), key=lambda item: streams[item[0]])]
            stage_models[block] = {"data": rows, **{m: fit(rows, ("N",), m) for m in MEASURES}}
        out[stage] = stage_models
    return out


# ------------------------------------------------------------ marginals


def marginals(plan: dict, summary: dict, top: str, reference: str) -> dict:
    """Each point of one top minus its reference point: totals and the five blocks that moved most."""
    if reference not in summary:
        return {}
    base = summary[reference]["hierarchical"]
    out = {}
    for point in plan["points"]:
        name = point["name"]
        if point["top"] != top or name == reference or "hierarchical" not in summary.get(name, {}):
            continue
        mine = summary[name]["hierarchical"]
        delta = {m: yosys_measures(mine["totals"])[m] - yosys_measures(base["totals"])[m] for m in MEASURES}
        moved = []
        for block in set(mine["blocks"]) | set(base["blocks"]):
            zero = dict.fromkeys(yosys_sweep.COLUMNS, 0)
            change = {m: yosys_measures(mine["blocks"].get(block, zero))[m]
                      - yosys_measures(base["blocks"].get(block, zero))[m] for m in MEASURES}
            if any(change.values()):
                moved.append((block, change))
        moved.sort(key=lambda item: (-abs(item[1]["LUT"]), -abs(item[1]["FF"]), item[0]))
        out[name] = {"changes": {**point.get("params", {}), **{k: v for p in point.get("patch", {}).values()
                                                                for k, v in p.items()}},
                     "shape": point.get("shape", ""), "delta": delta, "moved": moved[:5],
                     "refusals": refusals(summary, name)}
    return out


def parameter_models(plan: dict, summary: dict) -> dict:
    """Per processor parameter: y = a + b*x over the shipping point and every point changing only it."""
    groups: dict[str, list[tuple[str, float]]] = {}
    base = plan["tops"]["KL_pp_shadow"]["params"]
    for point in plan["points"]:
        if point["top"] != "KL_pp_shadow" or point["name"] not in summary or refusals(summary, point["name"]):
            continue
        changes = {**point.get("params", {}), **{k: v for p in point.get("patch", {}).values() for k, v in p.items()}}
        key = "+".join(sorted(changes)) or "@ship"
        groups.setdefault(key, []).append((point["name"], min(changes.values()) if changes else 0))
    ship = groups.pop("@ship", [])
    out = {}
    for key, members in groups.items():
        names = key.split("+")
        shipping = SHIPPING_DEFAULTS.get(names[0], base.get(names[0]))
        rows = [{"point": name, "x": float(value), **yosys_measures(summary[name]["hierarchical"]["totals"])}
                for name, value in members]
        if ship and shipping is not None:
            rows.append({"point": ship[0][0], "x": float(shipping),
                         **yosys_measures(summary[ship[0][0]]["hierarchical"]["totals"])})
        rows.sort(key=lambda row: row["x"])
        out[key] = {"data": rows, **{m: fit(rows, ("x",), m) for m in MEASURES}}
    return out


#: Shipping values of the parameters the plan rewrites in a source rather than binds (their RTL defaults).
SHIPPING_DEFAULTS = {"PP_N_CTRL_C": 16, "RX_SLOTS_P": 4, "TX_STD_SLOTS_P": 4, "RX_SLOT_BYTES_P": 576, "N_IF_P": 1}


# ---------------------------------------------------------- calibration


def load_anchor(directory: Path, known: set[str]) -> dict:
    """One Vivado anchor's totals and blocks after synthesis and after optimization."""
    out = {}
    for stage in ("synth", "opt"):
        path = directory / f"{stage}_hierarchy.rpt"
        if path.is_file():
            rows = vivado_rows(path)
            out[stage] = {"totals": vivado_measures(rows[0][2]), "blocks": vivado_blocks(rows, known)}
    return out


def calibration(summary: dict, anchors: dict[str, dict]) -> dict:
    """Vivado over Yosys per anchor, total and per block, for both Yosys instruments."""
    out = {}
    for name, data in anchors.items():
        if name not in summary or "opt" not in data or refusals(summary, name):
            continue
        hierarchical = summary[name]["hierarchical"]
        flat = summary[name].get("flat", {}).get("totals")
        totals = {"yosys_hier": yosys_measures(hierarchical["totals"]),
                  "yosys_flat": yosys_measures(flat) if flat else None,
                  "vivado_synth": data.get("synth", {}).get("totals"), "vivado_opt": data["opt"]["totals"]}
        blocks = {}
        for block, figures in data["opt"]["blocks"].items():
            mine = hierarchical["blocks1"].get(block)
            if mine is None:
                continue
            ys = yosys_measures(mine)
            blocks[block] = {"yosys": ys, "vivado": figures,
                             "ratio_LUT": round(figures["LUT"] / ys["LUT"], 3) if ys["LUT"] else None,
                             "ratio_FF": round(figures["FF"] / ys["FF"], 3) if ys["FF"] else None}
        out[name] = {"totals": totals, "blocks": blocks}
    return out


def in_context(route_rows: list, anchor: dict, known: set[str]) -> dict:
    """Routed milan_datapath blocks (the map's full-depth report) against the shipping anchor's
    out-of-context blocks after optimization."""
    datapath = next(key for key, _, _ in route_rows if key.endswith("/milan_datapath") and key.count("/") == 1)
    routed: dict[str, dict[str, float]] = {}
    for key, module, counts in route_rows:
        if key.count("/") != 2 or not key.startswith(datapath + "/"):
            continue
        name = "@own" if key.endswith("/@own") else _source_module(module, known)
        entry = routed.setdefault(f"milan_datapath/{name}", dict.fromkeys(MEASURES, 0.0))
        for column, value in vivado_measures(counts).items():
            entry[column] += value
    out = {}
    for block, figures in routed.items():
        ooc = anchor["opt"]["blocks"].get(block)
        out[block] = {"routed": figures, "ooc_opt": ooc,
                      "ratio_LUT": round(figures["LUT"] / ooc["LUT"], 3) if ooc and ooc["LUT"] else None}
    return out


def tdm_model(plan: dict, summary: dict) -> dict:
    """Capture slots with the render lane pruned: y = a + b*slots over the TDM points that share it."""
    rows = []
    for point in plan["points"]:
        params = point.get("params", {})
        if point["top"] != "milan_datapath" or params.get("AUDIO_IF_RENDER_SLOTS_P") != 0:
            continue
        if set(params) - {"AUDIO_IF_SLOTS_P", "AUDIO_IF_CLK_HZ_P", "AUDIO_IF_RENDER_SLOTS_P"} or point.get("shape"):
            continue
        if point["name"] in summary and not refusals(summary, point["name"]):
            slots = params.get("AUDIO_IF_SLOTS_P", plan["tops"]["milan_datapath"]["params"]["AUDIO_IF_SLOTS_P"])
            rows.append({"point": point["name"], "x": float(slots),
                         **yosys_measures(summary[point["name"]]["hierarchical"]["totals"])})
    rows.sort(key=lambda row: row["x"])
    return {"data": rows, **{m: fit(rows, ("x",), m) for m in MEASURES}} if len(rows) >= 2 else {}


def build(work: Path, map_dir: Path | None, plan_path: Path = yosys_sweep.PLAN) -> dict:
    """Every model and table from one work directory, under the tracked plan unless another is named."""
    plan = yosys_sweep.load_plan(plan_path)
    summary = json.loads((work / "summary.json").read_text())
    unusable = []
    for name in sorted(summary):
        try:
            refusals(summary, name)
        except GuardError as failure:
            unusable.append(str(failure))
    if unusable:
        raise GuardError("; ".join(unusable))
    known = {part for point in summary.values() for block in point.get("hierarchical", {}).get("blocks", {})
             for part in block.split("/")}
    anchors = {p["name"]: load_anchor(work / "vivado" / p["name"], known)
               for p in plan["points"] if p.get("anchor") and (work / "vivado" / p["name"]).is_dir()}
    anchors = {name: data for name, data in anchors.items() if "opt" in data}
    result = {"stream_models": stream_models(plan, summary),
              "stream_models_detail": stream_models(plan, summary, "blocks"),
              "vivado_stream_models": vivado_stream_models(anchors, plan, summary),
              "datapath_marginals": marginals(plan, summary, "milan_datapath", "ship"),
              "processor_marginals": marginals(plan, summary, "KL_pp_shadow", "pp-ship"),
              "processor_models": parameter_models(plan, summary),
              "adp_marginals": marginals(plan, summary, "KL_adp_engine", "adp-if-1"),
              "calibration": calibration(summary, anchors)}
    result["tdm_model"] = tdm_model(plan, summary)
    result["guards"] = {"checked": sorted(summary),
                        "refused": {name: refusals(summary, name) for name in summary if refusals(summary, name)}}
    builder = sorted(name for name, entry in summary.items() if "builder" in entry)
    if builder:
        result["guards"]["by_builder"] = builder
    if map_dir is not None and "ship" in anchors:
        result["in_context"] = in_context(vivado_rows(map_dir / "map_hierarchy.rpt"), anchors["ship"], known)
    return result


# ------------------------------------------------------------ self-test


def _guard(*fired: str) -> dict:
    """A clean guard record, or one whose lint saw the named guards fire."""
    return {"rc": 0, "refusals": list(fired), "errors": []}


def _selftest_inputs() -> tuple[dict, dict]:
    """A synthetic plan and summary: a stream and channel plane (LUT = 100 + 10 N + C), a TDM line and a
    processor parameter, each with guard-clean points exactly on it and one refused point far off it, so a
    refused point that entered a fit would show as a residual and a changed coefficient."""
    plan = {"tops": {"milan_datapath": {"params": {STREAM_PARAM: 1, CHANNEL_PARAM: 8, "AUDIO_IF_SLOTS_P": 8}},
                     "KL_pp_shadow": {"params": {"P": 1}}}, "points": []}
    summary = {}

    def add(name: str, top: str, params: dict, lut: float, guard: dict) -> None:
        """One point whose every column is a known function of its LUT figure."""
        plan["points"].append({"name": name, "top": top, "params": params})
        figures = {**dict.fromkeys(yosys_sweep.COLUMNS, 0), "LUT_TOT": lut, "FF": 2 * lut}
        summary[name] = {"hierarchical": {"totals": figures, "blocks": {}, "blocks1": {}}, "guards": guard}

    for streams in (1, 2, 4):
        add(f"s{streams}", "milan_datapath", {STREAM_PARAM: streams}, 108 + 10 * streams, _guard())
    for channels in (2, 4):
        add(f"c{channels}", "milan_datapath", {CHANNEL_PARAM: channels}, 110 + channels, _guard())
    add("s4c2", "milan_datapath", {STREAM_PARAM: 4, CHANNEL_PARAM: 2}, 142, _guard())
    add("s8", "milan_datapath", {STREAM_PARAM: 8}, 9999, _guard("N_NAME_P=235 outside 1..128"))
    for slots in (8, 16, 32):
        add(f"t{slots}", "milan_datapath", {"AUDIO_IF_SLOTS_P": slots, "AUDIO_IF_RENDER_SLOTS_P": 0}, 50 + slots,
            _guard())
    add("t64", "milan_datapath", {"AUDIO_IF_SLOTS_P": 64, "AUDIO_IF_RENDER_SLOTS_P": 0}, 9999, _guard("slots"))
    add("pp-ship", "KL_pp_shadow", {}, 205, _guard())
    for value in (2, 4):
        add(f"pp-p{value}", "KL_pp_shadow", {"P": value}, 200 + 5 * value, _guard())
    add("pp-p8", "KL_pp_shadow", {"P": 8}, 9999, _guard("P=8 refused"))
    plan["points"].append({"name": "s16", "top": "milan_datapath", "params": {STREAM_PARAM: 16}})
    summary["s16"] = {"builder": {"refusal": BUILDER_REFUSAL_SELFTEST}}
    return plan, summary


#: The refusal the synthetic builder-refused point carries: it was never priced, so it has no figures.
BUILDER_REFUSAL_SELFTEST = "CONFIG ERROR: this AEM model has 999 writable names"


def _selftest_guards() -> list[str]:
    """A refused point leaves every fit; a point the builder refused is refused with its line and has no
    marginal; a missing or hard-error record stops the models, never reads clean."""
    problems = []
    plan, summary = _selftest_inputs()
    streams = stream_models(plan, summary)["@total"]
    if "s8" in [row["point"] for row in streams["data"]] or streams["LUT"]["max_abs"] > 1e-6:
        problems.append(f"guards: the refused stream point entered the stream fit: {streams['LUT']}")
    processor = parameter_models(plan, summary)["P"]
    if "pp-p8" in [row["point"] for row in processor["data"]] or processor["LUT"]["max_abs"] > 1e-6:
        problems.append(f"guards: the refused processor point entered its parameter fit: {processor['LUT']}")
    tdm = tdm_model(plan, summary)
    if "t64" in [row["point"] for row in tdm["data"]] or tdm["LUT"]["max_abs"] > 1e-6:
        problems.append(f"guards: the refused TDM point entered the TDM model: {tdm['LUT']}")
    anchors = {name: {"opt": {"totals": {"LUT": 1.0, "FF": 1.0, "BRAM": 0.0, "DSP": 0.0}, "blocks": {}}}
               for name in ("s1", "s8")}
    if "s8" in calibration(summary, anchors):
        problems.append("guards: the refused anchor entered the calibration")
    if refusals(summary, "s16") != [BUILDER_REFUSAL_SELFTEST]:
        problems.append(f"guards: the builder-refused point reads {refusals(summary, 's16')}")
    margins = marginals(plan, summary, "milan_datapath", "s1")
    if "s16" in margins or not margins.get("s8", {}).get("refusals"):
        problems.append(f"guards: the marginals hold {sorted(margins)}: the unpriced point has none, s8 is refused")
    for label, damage in (("a missing record", lambda s: s["s2"].pop("guards")),
                          ("a hard-error record", lambda s: s["s2"]["guards"].update(errors=["%Error: x.sv:1"]))):
        _, broken = _selftest_inputs()
        damage(broken)
        try:
            stream_models(plan, broken)
            problems.append(f"guards: {label} was fitted as a guard-clean point")
        except GuardError:
            pass
    return problems


def _selftest_build() -> list[str]:
    """build() over the synthetic inputs names the builder-refused point in guards.by_builder, beside its
    refusal line, and writes no by_builder when no point carries a builder record."""
    problems = []
    plan, summary = _selftest_inputs()
    plan["tops"]["milan_datapath"]["shape"] = yosys_sweep.BASE_CONFIG
    plan["variants"] = {}
    unrefused = {name: entry for name, entry in summary.items() if "builder" not in entry}
    with tempfile.TemporaryDirectory(prefix="resmap-build-") as tmp:
        work = Path(tmp)
        (work / "plan.json").write_text(json.dumps(plan))
        for label, entries, by_builder, line in (
                ("a builder-refused point", summary, ["s16"], [BUILDER_REFUSAL_SELFTEST]),
                ("no builder-refused point", unrefused, None, None)):
            (work / "summary.json").write_text(json.dumps(entries))
            guards = build(work, None, work / "plan.json")["guards"]
            if guards.get("by_builder") != by_builder or guards["refused"].get("s16") != line:
                problems.append(f"build: with {label}, guards.by_builder is {guards.get('by_builder')} and s16 "
                                f"is refused by {guards['refused'].get('s16')}")
    return problems


def selftest() -> int:
    """A fit recovers known coefficients exactly; a planted point shows in its residual; a design that cannot
    determine its terms is refused; reports parse; guard records fail closed."""
    problems = []
    rows = [{"N": n, "C": c, "NC": n * c, "y": 100 + 7 * n + 3 * c + 2 * n * c} for n, c in
            ((1, 8), (2, 8), (4, 8), (8, 8), (1, 2), (1, 4), (4, 2), (8, 2))]
    exact = fit(rows, ("N", "C", "NC"), "y")
    if exact["coefficients"] != {"fixed": 100.0, "N": 7.0, "C": 3.0, "NC": 2.0} or exact["max_abs"] > 1e-6:
        problems.append(f"fit did not recover the generating model: {exact}")
    rows[2]["y"] += 40
    planted = fit(rows, ("N", "C", "NC"), "y")
    if planted["max_abs"] < 10:
        problems.append(f"a planted wrong point left no residual: {planted}")
    try:
        fit([row for row in rows if row["C"] == 8], ("N", "C", "NC"), "y")
        problems.append("a fit whose points never vary C was accepted at minimum norm")
    except ValueError:
        pass
    report = ("| top | (top) | 9 | 9 | 0 | 0 | 7 | 1 | 0 | 0 |\n"
              "|   (top) | (top) | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |\n"
              "|   u_a | KL_gptp_shadow_3 | 5 | 5 | 0 | 0 | 4 | 1 | 0 | 0 |\n"
              "|   u_b | adp_tx_arbiter__parameterized1 | 3 | 3 | 0 | 0 | 2 | 0 | 0 | 0 |\n")
    with tempfile.TemporaryDirectory(prefix="resmap-models-") as tmp:
        path = Path(tmp) / "hierarchy.rpt"
        path.write_text(report)
        blocks = vivado_blocks(vivado_rows(path), {"KL_gptp_shadow", "adp_tx_arbiter"})
    wanted = {"top/@own", "top/KL_gptp_shadow", "top/adp_tx_arbiter"}
    if set(blocks) != wanted or blocks["top/KL_gptp_shadow"]["BRAM"] != 1:
        problems.append(f"report blocks wrong: {blocks}")
    problems += _selftest_guards() + _selftest_build()
    for problem in problems:
        print(f"SELF-TEST FAILED: {problem}")
    print(f"resmap_models self-test: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


def main() -> int:
    """The CLI; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work", type=Path)
    parser.add_argument("--map", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.work is None or args.out is None:
        parser.print_help()
        return 2
    try:
        result = build(args.work.resolve(), args.map)
    except GuardError as failure:
        print(f"models: refused, a point's guard record is not usable: {failure}")
        return 1
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "models.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(f"models: {', '.join(f'{k} {len(v)}' for k, v in result.items())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
