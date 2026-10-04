#!/usr/bin/env python3
"""Cut the published extracts out of one Vivado run directory of the #232 lane.

Usage: vivado_extract.py KIND RUN_DIR FIGURES_JSON OUT_DIR
  KIND is route (a gateware directory of #638's integrated route) or ooc (a
  standalone KL_pp_shadow synthesis directory of #638's recipe).

Small reports are copied whole. From the large ones only the named sections
are cut, each preceded by its source file and line range. sources.tsv records
the full sha256 and size of every source file read, so each extract can be
matched to its raw file, which stays in scratch.
"""
import collections
import hashlib
import re
import shutil
import sys
from pathlib import Path

DIAG = ("Synth 8-7186", "Synth 8-4445", "Synth 8-6901")
SCOPES = ("u_notify", "u_aecp/u_resp", "u_aecp/u_d3")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def section(lines: list[str], start: re.Pattern, stop: re.Pattern, src: str,
            nth: int = 0, skip: int = 1) -> str:
    """The nth block from a line matching start up to (not including) a stop line."""
    found = [i for i, l in enumerate(lines) if start.search(l)]
    if len(found) <= nth:
        return f"## {src}: section {start.pattern!r} #{nth + 1} not found\n"
    i = found[nth]
    j = i + skip
    while j < len(lines) and not stop.search(lines[j]):
        j += 1
    return f"## {src}:{i + 1}-{j}\n" + "".join(lines[i:j]) + "\n"


def timing(path: Path, label: str) -> str:
    lines = path.read_text(errors="replace").splitlines(keepends=True)
    out = section(lines, re.compile(r"^\| Design Timing Summary"),
                  re.compile(r"^\| Clock Summary"), f"{label} {path.name}", skip=1)
    return out[: out.rfind("-----")] if "Clock Summary" in out else out


def worst_path(path: Path, kind: str) -> str:
    """The path of least slack among every clock's Max (setup) or Min (hold) Delay
    Paths group, from its Slack line to its detailed slack line."""
    lines = path.read_text(errors="replace").splitlines(keepends=True)
    group, best = "", None
    for i, line in enumerate(lines):
        if line.startswith(("Max Delay Paths", "Min Delay Paths")):
            group = line
        m = re.match(r"^Slack \((?:MET|VIOLATED)\) :\s+(-?[0-9.]+)ns", line)
        if m and group.startswith(kind) and (best is None or float(m.group(1)) < best[0]):
            best = (float(m.group(1)), i)
    if best is None:
        return f"## {path.name}: no {kind}\n"
    i = best[1]
    j = i + 1
    while j < len(lines) and not re.match(r"^\s+slack\s+-?\d", lines[j]):
        j += 1
    return (f"## {path.name}:{i + 1}-{j + 1} (least slack of every '{kind}' group)\n"
            + "".join(lines[i:j + 1]) + "\n")


def log_extract(log: Path) -> str:
    lines = log.read_text(errors="replace").splitlines(keepends=True)
    out = [f"# extract of {log.name} ({len(lines)} lines)\n\n"]
    head = [l for l in lines[:400] if re.search(r"Vivado v\.|Build \d|-part |part: |Command: ", l)]
    out.append("## identity lines (first 400 lines)\n" + "".join(head[:8]) + "\n")
    stop = re.compile(r"^-{20,}|^\s*$")
    for title in ("Block RAM: Final Mapping Report", "Distributed RAM: Final Mapping Report"):
        n = sum(1 for l in lines if l.startswith(title))
        for k in range(n):
            out.append(section(lines, re.compile("^" + re.escape(title)), stop, log.name, nth=k))
    for d in DIAG:
        hits = [(i + 1, l) for i, l in enumerate(lines) if d in l]
        real = [(i, l) for i, l in hits if "set_msg_config" not in l]
        out.append(f"## {d}: {len(real)} diagnostic line(s) ({len(hits) - len(real)} echoed set_msg_config)\n")
        out.extend(f"{log.name}:{i}: {l}" for i, l in hits)
        out.append("\n")
    tail = [(i + 1, l) for i, l in enumerate(lines)
            if re.search(r"(route_design|synth_design|place_design|opt_design) completed successfully", l)]
    out.append("## completion lines\n" + "".join(f"{log.name}:{i}: {l}" for i, l in tail) + "\n")
    return "".join(out)


def census(cells: Path, prefix: str) -> str:
    """Primitive counts per scope and for the arrays the inventory names."""
    scopes: dict[str, collections.Counter] = {s: collections.Counter() for s in SCOPES}
    arrays = {"u_notify rows_r_reg": collections.Counter(),
              "u_notify ctr_last_r_reg": collections.Counter(),
              "u_notify g_ix_row": collections.Counter(),
              "u_notify cmdq_": collections.Counter()}
    with cells.open(errors="replace") as f:
        next(f)
        for row in f:
            name, _, prim = row.rstrip("\n").partition("\t")
            for s in SCOPES:
                if f"{prefix}{s}/" in name:
                    scopes[s][prim] += 1
            if f"{prefix}u_notify/" in name:
                local = name.split(f"{prefix}u_notify/", 1)[1]
                for key in arrays:
                    if local.startswith(key.split(" ", 1)[1]):
                        arrays[key][prim] += 1
    out = ["scope\tprimitive\tcells\n"]
    for s, c in list(scopes.items()) + list(arrays.items()):
        for prim, n in sorted(c.items()):
            out.append(f"{s}\t{prim}\t{n}\n")
    return "".join(out)


def main() -> int:
    kind, run, figures, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    out.mkdir(parents=True, exist_ok=True)
    read: list[Path] = []
    if kind == "route":
        whole = ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_pp_utilization.rpt",
                 "baseline_scope_timing.tsv", "baseline_images.json",
                 "alinx_ax7101_utilization_place.rpt", "alinx_ax7101_utilization_hierarchical_place.rpt",
                 "alinx_ax7101_route_status.rpt", "alinx_ax7101_signoff_grade.txt"]
        whole += [f"alinx_ax7101_signoff_{c}_negative.rpt" for c in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")]
        timing_files = ["baseline_timing.rpt", "alinx_ax7101_timing.rpt"] + [f"alinx_ax7101_signoff_{c}_timing.rpt"
                                                     for c in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")]
        log, cells, prefix = run / "baseline.log", run / "baseline_cells.tsv", "u_pp/"
    else:
        whole = ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_scope_timing.tsv",
                 "baseline_parameters.json", "baseline_chparam.txt", "baseline_images.json"]
        timing_files = ["baseline_timing.rpt"]
        log, cells, prefix = run / "baseline.log", run / "baseline_cells.tsv", "u_pp/"
    for name in whole:
        src = run / name
        shutil.copyfile(src, out / name)
        read.append(src)
    text = []
    for name in timing_files:
        src = run / name
        text.append(timing(src, ""))
        read.append(src)
    main_timing = run / timing_files[0]
    lines = main_timing.read_text(errors="replace").splitlines(keepends=True)
    text.append(section(lines, re.compile(r"^\| Intra Clock Table"),
                        re.compile(r"^\| Inter Clock Table"), main_timing.name))
    text.append(worst_path(main_timing, "Max Delay Paths"))
    text.append(worst_path(main_timing, "Min Delay Paths"))
    (out / "timing-extract.txt").write_text("".join(text))
    (out / "log-extract.txt").write_text(log_extract(log))
    read.append(log)
    (out / "census.tsv").write_text(census(cells, prefix))
    read.append(cells)
    shutil.copyfile(figures, out / "figures.json")
    read.append(figures)
    with (out / "sources.tsv").open("w") as f:
        f.write("source\tbytes\tsha256\n")
        for src in read:
            f.write(f"{src.name}\t{src.stat().st_size}\t{sha(src)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
