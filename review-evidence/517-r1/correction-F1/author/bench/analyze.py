#!/usr/bin/env python3
"""Summarise one observed milan_dp run (issue #517 benchmark; not repository code).

    analyze.py RUN_DIR LANE_DIR [--json OUT]

Reads RUN_DIR/milan_dp.log and RUN_DIR/samples.jsonl written by run_suite.sh /
observe.py. Prints and optionally writes:

* per ordinary leg: transcript SHA-256 (from its command echo line up to the
  next leg's banner or echo, the render banner or the render command), its
  tallies read with the lane's own scripts/suite_tally.py scan(), and from the
  /proc samples its first/last sighting, observed life, CPU seconds, peak RSS
  (VmHWM), argv, cwd, fd 0 target and environment hash;
* the leg phase: first ordinary leg seen to last ordinary leg seen, the
  maximum and time-weighted mean number of ordinary legs alive, and the peak
  summed RSS of the ordinary legs and of the whole observed tree;
* the gPTP prerequisite legs and the render_mutants.py phase the same way;
* the whole-suite wall time and exit status from summary.json.

Sampling is every ~0.5 s, so a first/last sighting is within one interval of
the true start/end. None of these numbers is a test result.
"""

import hashlib
import json
import sys
from pathlib import Path

ORDINARY = (
    "./obj_dir/Vmilan_dp_sim", "./obj_notify/Vmilan_dp_notify",
    "./obj_nxn/Vmilan_dp_nxn", "./obj_nxndv/Vmilan_dp_nxndv",
    "./obj_nxn8/Vmilan_dp_nxn8", "./obj_nxn4c/Vmilan_dp_nxn4c",
    "./obj_nolpf/Vmilan_dp_nolpf", "./obj_prune/Vmilan_dp_prune",
    "./obj_ax1x1/Vmilan_dp_ax1x1", "./obj_aclk/Vmilan_dp_aclk",
)
GPTP = ("./obj_gptp/Vmilan_dp_gptp", "./obj_gptplat/Vmilan_dp_gptplat")
BANNERS = (
    "---- Milan 5.4.5 notifications, TIMED on the compressed processor timebase ----",
    "---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----",
    "---- the shipping Arty shape: 4 streams x 4 wire channels ----",
    "---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----",
    "---- all six tier-1 blocks pruned ----",
    "---- THE SHIPPING ALINX SHAPE: 1 stream x 8 wire channels, TDM8 master ----",
    "---- the same shape at the TRUE clk_audio ratio (391/1591) ----",
    "---- #386 render law: the same leg against mutated setpoint stages and datapath ----",
)
STOP = set(ORDINARY) | set(GPTP) | set(BANNERS) | {"python3 render_mutants.py"}


def split_log(text: str) -> dict[str, str]:
    """{echo line: its transcript} for every leg echo and the render section."""
    lines = text.splitlines(keepends=True)
    out: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in lines:
        bare = line.rstrip("\n")
        if bare in STOP:
            if current is not None:
                out[current] = "".join(buf)
            current = bare if bare not in BANNERS else None
            buf = [line] if current else []
            continue
        if current is not None:
            if line.startswith("verilator ") or line.startswith("make: Leaving"):
                out[current] = "".join(buf)
                current, buf = None, []
                continue
            buf.append(line)
    if current is not None:
        out[current] = "".join(buf)
    return out


def main() -> int:
    run = Path(sys.argv[1])
    lane = Path(sys.argv[2])
    sys.path.insert(0, str(lane / "scripts"))
    from suite_tally import scan, log_reports_failure  # noqa: E402

    text = (run / "milan_dp.log").read_text(errors="replace")
    sections = split_log(text)
    procs: dict[int, dict] = {}
    samples = []
    for raw in (run / "samples.jsonl").read_text().splitlines():
        s = json.loads(raw)
        samples.append(s)
        for p in s["procs"]:
            rec = procs.setdefault(p["pid"], {"argv": p["argv"], "first": s["t"],
                                              "cwd": p["cwd"], "fd0": p["fd0"]})
            rec["last"] = s["t"]
            if p["state"] != "Z":
                rec["last_alive"] = s["t"]
            rec["hwm_kb"] = max(rec.get("hwm_kb", 0), p["hwm_kb"])
            rec["cpu_s"] = max(rec.get("cpu_s", 0), p["cpu_s"])
            if "env_sha256" in p:
                rec["env_sha256"] = p["env_sha256"]
                rec["env_keys"] = p["env_keys"]

    def legs_named(names):
        found = {}
        for pid, rec in procs.items():
            if rec["argv"] and rec["argv"][0] in names:
                found.setdefault(rec["argv"][0], []).append((pid, rec))
        return found

    ordinary = legs_named(ORDINARY)
    report = {"run": run.name, "summary": json.loads((run / "summary.json").read_text())}
    legs = []
    for name in ORDINARY:
        entries = ordinary.get(name, [])
        section = sections.get(name)
        tally = scan(section) if section is not None else None
        leg = {"leg": name, "sightings": len(entries),
               "transcript_sha256": hashlib.sha256(section.encode()).hexdigest() if section else None,
               "transcript_bytes": len(section.encode()) if section else None,
               "checks": tally[0] if tally else None, "failures": tally[1] if tally else None,
               "tallies": [m[3] for m in tally[2]] if tally else None,
               "verdict_failure": log_reports_failure(section)[1] if section else None}
        if entries:
            pid, rec = entries[0]
            leg.update(first_t=rec["first"], last_t=rec.get("last_alive", rec["last"]),
                       life_s=round(rec.get("last_alive", rec["last"]) - rec["first"], 3),
                       cpu_s=rec["cpu_s"], hwm_kb=rec["hwm_kb"], argv=rec["argv"],
                       cwd=rec["cwd"], fd0=rec["fd0"], env_sha256=rec.get("env_sha256"),
                       env_keys=rec.get("env_keys"))
        legs.append(leg)
    report["legs"] = legs
    seen = [l for l in legs if "first_t" in l]
    if seen:
        start = min(l["first_t"] for l in seen)
        end = max(l["last_t"] for l in seen)
        alive_counts = []
        grouped_counts = []
        group_overlap_samples = 0
        grouped = set(ORDINARY[1:6])
        tree_rss = []
        leg_rss = []
        for s in samples:
            alive = [p for p in s["procs"] if p["argv"] and p["argv"][0] in ORDINARY and p["state"] != "Z"]
            if start <= s["t"] <= end:
                alive_counts.append((s["t"], len(alive)))
                group_count = sum(p["argv"][0] in grouped for p in alive)
                grouped_counts.append(group_count)
                group_overlap_samples += int(group_count > 0 and len(alive) > group_count)
                leg_rss.append(sum(p["rss_kb"] for p in alive))
            tree_rss.append(sum(p["rss_kb"] for p in s["procs"]))
        weighted = 0.0
        for (t0, n0), (t1, _n1) in zip(alive_counts, alive_counts[1:]):
            weighted += n0 * (t1 - t0)
        report["leg_phase"] = {
            "first_leg_seen_t": start, "last_leg_seen_t": end,
            "span_s": round(end - start, 3),
            "max_alive": max(n for _t, n in alive_counts) if alive_counts else None,
            "max_group_alive": max(grouped_counts),
            "group_independent_overlap_samples": group_overlap_samples,
            "mean_alive": round(weighted / (end - start), 3) if end > start else None,
            "sum_leg_life_s": round(sum(l["life_s"] for l in seen), 3),
            "sum_leg_cpu_s": round(sum(l["cpu_s"] for l in seen), 3),
            "peak_leg_rss_kb": max(leg_rss) if leg_rss else None,
            "peak_tree_rss_kb": max(tree_rss) if tree_rss else None,
            "load1_during": [min(s["load1"] for s in samples if start <= s["t"] <= end),
                             max(s["load1"] for s in samples if start <= s["t"] <= end)],
            "host_busy_mean": round(sum(s["host_busy"] or 0 for s in samples if start <= s["t"] <= end)
                                    / max(1, sum(1 for s in samples if start <= s["t"] <= end)), 3),
        }
    gptp = legs_named(GPTP)
    report["gptp"] = {name: {"life_s": round(rec.get("last_alive", rec["last"]) - rec["first"], 3),
                             "first_t": rec["first"], "cpu_s": rec["cpu_s"], "hwm_kb": rec["hwm_kb"]}
                      for name, ((_pid, rec), *_rest) in gptp.items()}
    render = [rec for rec in procs.values()
              if len(rec["argv"]) >= 2 and rec["argv"][1].endswith("render_mutants.py")]
    if render:
        rec = render[0]
        report["render"] = {"first_t": rec["first"], "last_t": rec["last"],
                            "span_s": round(rec["last"] - rec["first"], 3)}
    whole = scan(text)
    report["whole_log"] = {"checks": whole[0], "failures": whole[1], "tallies": len(whole[2]),
                           "unparsed": whole[3], "verdict": log_reports_failure(text)}
    report["sections_found"] = sorted(sections)
    out = json.dumps(report, indent=1)
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(out + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
