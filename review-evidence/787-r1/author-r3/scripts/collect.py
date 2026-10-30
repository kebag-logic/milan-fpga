"""collect.py <dest>: copy round 3's receipts, host paths redacted, into <dest>.

Per routed run (head: the three directives; dev: the #814 round 1 routes, for the delta): the route status, the
flat post-route utilization the gate reads, the placed hierarchical utilization, the IOB packing report, the
clock interaction and check_timing reports, the CDC report's summary, the Design Timing Summary table of every
timing report, and the Vivado log's CONSTRAINTS and IOB-PACK lines. Plus the gate, figure, #607, xvlog and
self-test logs from the scratch results. A file over 200 KB is recorded by SHA-256 and size in large.sha256."""
import hashlib
import sys
from pathlib import Path

dest = Path(sys.argv[1])
S = Path("$VALIDATION_STORAGE/787-a700d")
DEV = Path("$VALIDATION_STORAGE/scratch/814-a703/viv-dev/w1")
REDACT = ((str(S / "viv/w1"), "<work>"), (str(DEV), "<dev-work>"), (str(S), "<scratch>"),
          ("$VALIDATION_STORAGE/scratch", "<scratch-root>"), ("$VALIDATION_STORAGE", "<tmp-root>"),
          ("$LANES", "<lanes>"), ("$WORKSPACE_HOME", "<home>"))
RUNS = {"head-667b9bbc/EPPO": S / "viv/w1/ax7101/gateware",
        "head-667b9bbc/ASLH": S / "viv/w1/ax7101-AltSpreadLogic_high",
        "head-667b9bbc/ETO": S / "viv/w1/ax7101-ExtraTimingOpt",
        "dev-1e80128f/EPPO": DEV / "ax7101/gateware",
        "dev-1e80128f/ASLH": DEV / "ax7101-AltSpreadLogic_high",
        "dev-1e80128f/ETO": DEV / "ax7101-ExtraTimingOpt"}


def redact(text):
    for a, b in REDACT:
        text = text.replace(a, b)
    return text


def put(rel, text):
    data = redact(text).encode()
    if len(data) > 200 * 1024:
        with open(dest / "large.sha256", "a") as h:
            h.write(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel} (redacted text)\n")
        return
    out = dest / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(redact(text))


def design_table(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("WNS(ns)") and "THS(ns)" in line:
            return "\n".join(lines[i:i + 3]) + "\n"
    return "no design timing summary found\n"


dest.mkdir(parents=True, exist_ok=True)
(dest / "large.sha256").unlink(missing_ok=True)
for name, run in RUNS.items():
    for pattern, rel in (("*_route_status.rpt", "route_status.rpt"), ("baseline_utilization.rpt", "utilization.rpt"),
                         ("*_utilization_hierarchical_place.rpt", "utilization_hierarchical_place.rpt"),
                         ("*_iob_pack.rpt", "iob_pack.rpt"), ("*_clock_interaction.rpt", "clock_interaction.rpt"),
                         ("*_signoff_check_timing.rpt", "check_timing.rpt"), ("*_signoff_grade.txt", "signoff_grade.txt")):
        found = sorted(p for p in run.glob(pattern) if "signoff_clock" not in p.name)
        if found:
            put(f"{name}/{rel}", found[0].read_text(errors="replace"))
    cdc = sorted(run.glob("*_signoff_cdc.rpt"))
    if cdc:
        text = cdc[0].read_text(errors="replace")
        put(f"{name}/cdc_summary.txt", text.split("\nDetails", 1)[0] + "\n")
    tables = []
    for path in sorted(run.glob("*_timing.rpt")) + sorted(run.glob("baseline_timing.rpt")):
        if path.name.endswith("_synth.rpt"):
            continue
        tables.append(f"== {path.name}\n{design_table(path.read_text(errors='replace'))}")
    put(f"{name}/timing-design-tables.txt", "\n".join(tables))
    log = run / "baseline.log"
    keep = [l for l in log.read_text(errors="replace").splitlines()
            if l.startswith(("CONSTRAINTS:", "IOB-PACK", "CRITICAL WARNING:", "ERROR:"))
            or l.startswith(("synth_design: Time", "opt_design: Time", "place_design: Time", "phys_opt_design: Time",
                             "route_design: Time"))]
    put(f"{name}/log-excerpt.txt", "\n".join(keep) + "\n")
    rc = run / "baseline.log.rc"
    if rc.exists():
        put(f"{name}/vivado.rc", rc.read_text())
    for big in ("alinx_ax7101_route.dcp", "alinx_ax7101_synth.dcp", "baseline.log"):
        p = run / big
        if p.exists():
            data = p.read_bytes()
            with open(dest / "large.sha256", "a") as h:
                h.write(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {name}/{big} (unredacted original)\n")
for path in sorted((S / "results").glob("*")) + sorted((S / "offline").glob("*")):
    if path.name.startswith("rm-"):
        continue
    put(f"{path.parent.name}/{path.name}", path.read_text(errors="replace"))
for path in sorted((S / "xvlog").glob("*")):
    put(f"xvlog/{path.name}", path.read_text(errors="replace"))
for path in sorted((S / "slotlogs").glob("*.log")):
    put(f"slotlogs/{path.name}", path.read_text(errors="replace"))
put("prep/prep.log", (S / "prep.log").read_text(errors="replace"))
put("prep/failed-run-1-tail.txt", "\n".join((S / "failed-run-1/baseline.out").read_text(errors="replace")
                                           .splitlines()[-25:]) + "\n")
put("prep/failed-run-1.rc", (S / "failed-run-1/baseline.log.rc").read_text())
print("collected into", dest)
