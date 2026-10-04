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
    """Least squares of target on 1 and the named terms; coefficients, residuals and their summary."""
    design = np.array([[1.0] + [row[t] for t in terms] for row in rows])
    values = np.array([row[target] for row in rows])
    coefficients, _, rank, _ = np.linalg.lstsq(design, values, rcond=None)
    residuals = values - design @ coefficients
    return {"coefficients": dict(zip(("fixed", *terms), (round(float(c), 2) for c in coefficients))),
            "residuals": [round(float(r), 2) for r in residuals], "points": len(rows), "rank": int(rank),
            "rms": round(float(np.sqrt(np.mean(residuals ** 2))), 2),
            "max_abs": round(float(np.max(np.abs(residuals))), 2)}


def refusals(summary: dict, name: str) -> list[str]:
    """The elaboration guards that fired on one point, as yosys_sweep.py guards recorded them."""
    return summary.get(name, {}).get("guards", {}).get("refusals", [])


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
        if point["top"] != top or name == reference or name not in summary:
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
        if name not in summary or "opt" not in data:
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
        if point["name"] in summary:
            slots = params.get("AUDIO_IF_SLOTS_P", plan["tops"]["milan_datapath"]["params"]["AUDIO_IF_SLOTS_P"])
            rows.append({"point": point["name"], "x": float(slots),
                         **yosys_measures(summary[point["name"]]["hierarchical"]["totals"])})
    rows.sort(key=lambda row: row["x"])
    return {"data": rows, **{m: fit(rows, ("x",), m) for m in MEASURES}} if len(rows) >= 2 else {}


def build(work: Path, map_dir: Path | None) -> dict:
    """Every model and table from one work directory."""
    plan = yosys_sweep.load_plan(yosys_sweep.PLAN)
    summary = json.loads((work / "summary.json").read_text())
    known = {part for point in summary.values() for block in point["hierarchical"]["blocks"]
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
    result["guards"] = {"checked": sorted(name for name in summary if "guards" in summary[name]),
                        "unchecked": sorted(name for name in summary if "guards" not in summary[name]),
                        "refused": {name: refusals(summary, name) for name in summary if refusals(summary, name)}}
    if map_dir is not None and "ship" in anchors:
        result["in_context"] = in_context(vivado_rows(map_dir / "map_hierarchy.rpt"), anchors["ship"], known)
    return result


# ------------------------------------------------------------ self-test


def selftest() -> int:
    """A fit recovers known coefficients exactly; a planted point shows in its residual; reports parse."""
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
    result = build(args.work.resolve(), args.map)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "models.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(f"models: {', '.join(f'{k} {len(v)}' for k, v in result.items())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
