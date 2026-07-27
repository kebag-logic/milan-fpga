# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! The final report, rebuilt from the JSONL alone.
#!
#! It is reconstructed from the records rather than from in-memory state on
#! purpose: that is what proves the claim "a run is fully reconstructable from
#! the logs afterwards". `--report-only <run>` regenerates it from a finished or
#! crashed run with no bench present.

from __future__ import annotations

import json
from pathlib import Path

from . import log as logmod

VERDICT_ORDER = (logmod.FAIL, logmod.BLOCKED, logmod.PASS, logmod.SKIP)


def build(records: list[dict]) -> dict:
    """Fold the JSONL into the report model."""
    items: dict[str, dict] = {}
    outages, alerts, counter_rows = [], [], []
    quality, latency, seed = {}, {}, None
    registry_tally, registry_error = None, ""

    for rec in records:
        kind, item, verdict = rec.get("kind"), rec.get("item", ""), rec.get("verdict")
        if kind == "outage":
            outages.append(rec)
            continue
        if kind == "alert":
            alerts.append(rec)
            continue
        if kind == "info" and item == "harness":
            m = rec.get("measured") or {}
            seed = m.get("seed", seed)
            registry_tally = m.get("registry", registry_tally)
            registry_error = m.get("registry_error", registry_error)
            continue
        if kind in ("check", "blocked") and item:
            if item.startswith("counters/") and (rec.get("measured") or {}).get("counter"):
                counter_rows.append(rec)
            if "/thdn" in item:
                quality[item] = rec
            if "latency" in item or item == "quality/pto-sweep":
                latency[item] = rec
            cur = items.get(item)
            # Worst verdict wins, so a later PASS cannot bury an earlier FAIL.
            if cur is None or _worse(verdict, cur["verdict"]):
                items[item] = {"verdict": verdict, "detail": rec.get("detail", ""),
                               "phase": rec.get("phase", ""), "ts": rec.get("ts")}
    return {
        "items": items, "outages": outages, "alerts": alerts,
        "counter_rows": counter_rows, "quality": quality, "latency": latency,
        "seed": seed, "registry": registry_tally,
        "registry_error": registry_error,
        "tally": _tally(items),
    }


def _worse(a: str, b: str) -> bool:
    try:
        return VERDICT_ORDER.index(a) < VERDICT_ORDER.index(b)
    except ValueError:
        return False


def _tally(items: dict) -> dict:
    out = {v: 0 for v in VERDICT_ORDER}
    for meta in items.values():
        out[meta["verdict"]] = out.get(meta["verdict"], 0) + 1
    return out


def render(model: dict, *, run_id: str, interrupted: bool = False) -> str:
    t = model["tally"]
    es_items = {k: v for k, v in model["items"].items() if k.startswith("es-")}
    lines = [
        f"# Milan validation campaign - {run_id}",
        "",
        f"* items recorded: **{len(model['items'])}**",
        f"* PASS {t.get(logmod.PASS, 0)} | FAIL {t.get(logmod.FAIL, 0)} | "
        f"BLOCKED {t.get(logmod.BLOCKED, 0)} | SKIP {t.get(logmod.SKIP, 0)}",
        f"* matrix seed: `{model['seed']}` (replay with `--seed {model['seed']}`)",
        f"* bench outages recorded: {len(model['outages'])}",
        "",
    ]

    # --- the verdict line -------------------------------------------------
    lines += ["## Verdict", ""]
    if interrupted:
        lines.append("Run **interrupted** - resumable with no arguments.")
    elif t.get(logmod.FAIL, 0):
        first = next((k for k, v in model["items"].items()
                      if v["verdict"] == logmod.FAIL), "?")
        lines.append(f"**FAILED** - first failure: `{first}`.")
    elif t.get(logmod.BLOCKED, 0):
        lines.append(
            f"Everything that could run passed; **{t[logmod.BLOCKED]} item(s) "
            f"BLOCKED** (the harness could not run them - not defects). A "
            f"\"Milan validated\" verdict needs those cleared.")
    else:
        lines.append("**Milan validated** - every item passed.")
    lines.append("")

    # --- items ------------------------------------------------------------
    lines += ["## Items", ""]
    if model["registry"]:
        r = model["registry"]
        lines += [f"Registry: {r.get('total')} rows, "
                  f"{r.get('implemented')} implemented, "
                  f"{r.get('not_implemented')} not-implemented "
                  f"(`{r.get('source', '')}`).", ""]
    elif model["registry_error"]:
        lines += [f"Registry unavailable: {model['registry_error']}", ""]
    if es_items:
        lines += ["| item | verdict | detail |", "|---|---|---|"]
        for iid in sorted(es_items, key=_es_key):
            v = es_items[iid]
            lines.append(f"| `{iid}` | {v['verdict']} | {_cell(v['detail'])} |")
        lines.append("")
    other = {k: v for k, v in model["items"].items() if not k.startswith("es-")}
    if other:
        lines += ["### Harness steps", "", "| step | verdict | detail |",
                  "|---|---|---|"]
        for k in sorted(other):
            lines.append(f"| `{k}` | {other[k]['verdict']} | "
                         f"{_cell(other[k]['detail'])} |")
        lines.append("")

    # --- counter audit ----------------------------------------------------
    lines += ["## Counter audit", ""]
    if model["counter_rows"]:
        lines += ["| counter | verdict | delta | expect | neighbours held |",
                  "|---|---|---|---|---|"]
        for rec in model["counter_rows"]:
            m = rec.get("measured") or {}
            moved = m.get("moved_neighbours") or []
            held = "yes" if not moved else "**NO: " + ", ".join(moved) + "**"
            lines.append(f"| `{m.get('counter')}` | {rec['verdict']} | "
                         f"{m.get('delta')} | `{m.get('expect')}` | {held} |")
        lines.append("")
    else:
        lines += ["_no counter rows recorded in this run_", ""]

    # --- quality + latency ------------------------------------------------
    lines += ["## Quality and latency", ""]
    for key, rec in sorted(model["quality"].items()):
        m = rec.get("measured") or {}
        chans = m.get("channels") or []
        worst = max((c.get("thdn_dbfs", 0) for c in chans), default=None)
        lines.append(f"* `{key}`: {rec['verdict']} - worst channel "
                     f"{worst if worst is None else round(worst, 2)} dBFS "
                     f"(accept <= {m.get('accept_dbfs')}), window: "
                     f"{m.get('window')}")
    for key, rec in sorted(model["latency"].items()):
        m = rec.get("measured") or {}
        if key == "quality/pto-sweep":
            for p in m.get("points", []):
                lines.append(f"* pto {p.get('pto_us')} us -> measured "
                             f"{round(p.get('measured_us', 0), 1)} us "
                             f"(error {p.get('error_us')} us) "
                             f"{'OK' if p.get('ok') else 'OFF BUDGET'}")
        else:
            for d in ("rx", "tx"):
                ins = (m.get(d) or {}).get("in_system")
                if ins:
                    lines.append(
                        f"* `{key}` {d}: last {round(ins['last_us'], 2)} us / "
                        f"max {round(ins['max_us'], 2)} us vs budget "
                        f"{ins['budget_us']} us "
                        f"(excludes {ins['excluded_stage']}) - "
                        f"{'within' if ins.get('within_budget') else 'OVER'}")
    lines.append("")

    # --- operational ------------------------------------------------------
    lines += ["## Operational", ""]
    if model["alerts"]:
        a = (model["alerts"][0].get("measured") or {})
        lines.append(f"* alert fired once: sent={a.get('sent')} "
                     f"channels={len(a.get('channels', []))} "
                     f"{a.get('why', '')}")
    else:
        lines.append("* no alert fired (silence on success is the requirement)")
    if model["outages"]:
        total = sum((o.get("measured") or {}).get("outage_s", 0)
                    for o in model["outages"])
        lines.append(f"* {len(model['outages'])} outage retr(y|ies) recorded, "
                     f"~{round(total)}s cumulative - survived, not aborted")
    lines.append("")
    return "\n".join(lines) + "\n"


def _es_key(iid: str):
    try:
        g, m = iid.split("-", 1)[1].split(".")
        return (int(g), int(m))
    except (ValueError, IndexError):
        return (999, 999)


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")[:180]


def write_report(ctx, run: logmod.RunDir, *, interrupted: bool = False) -> Path:
    model = build(run.read_records())
    md = render(model, run_id=run.rid, interrupted=interrupted)
    path = run.dir / "report.md"
    path.write_text(md, encoding="utf-8")
    (run.dir / "report.json").write_text(
        json.dumps(model, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8")
    return path


def report_only(root: Path, rid: str) -> Path:
    """Regenerate a report from a finished or crashed run, with no bench."""
    run = logmod.RunDir(root, rid)
    return write_report(None, run)
