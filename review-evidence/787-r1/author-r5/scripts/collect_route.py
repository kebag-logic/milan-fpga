"""collect_route.py <dest>: copy round 5's route receipts, host paths redacted, into <dest>.

Per routed run (the merge head f7d5fc3c's three directives): the route status, the flat post-route utilization the gate
reads, the placed hierarchical utilization, the IOB packing report, the clock interaction and check_timing reports,
the CDC report's summary, the Design Timing Summary table of every timing report, and the Vivado log's CONSTRAINTS,
IOB-PACK, CRITICAL WARNING, ERROR and step-time lines. Plus the gate, figure, #607, xvlog and self-test logs from
the scratch results (the redacted copies; a *.raw.log is skipped), the slot wrapper logs and the prep log. A file
over 200 KB, and every checkpoint and full log, is recorded by SHA-256 and size in large.sha256. (Round 3's
collect.py, its paths and runs changed.)"""
import hashlib
import sys
from pathlib import Path

dest = Path(sys.argv[1])
S = Path("$VALIDATION_STORAGE/787-a700f")
WORK = S / "route/w1"
REDACT = ((str(WORK), "<work>"), (str(S), "<scratch>"), ("$VALIDATION_STORAGE/scratch", "<scratch-root>"),
          ("$VALIDATION_STORAGE", "<tmp-root>"), ("$LANES", "<lanes>"), ("$WORKSPACE_HOME", "<home>"))
RUNS = {"head-f7d5fc3c/EPPO": WORK / "ax7101/gateware",
        "head-f7d5fc3c/ASLH": WORK / "ax7101-AltSpreadLogic_high",
        "head-f7d5fc3c/ETO": WORK / "ax7101-ExtraTimingOpt"}


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
for sub in ("results", "offline"):
    for path in sorted((S / sub).glob("*")):
        if path.name.endswith(".raw.log"):
            continue
        put(f"{sub}/{path.name}", path.read_text(errors="replace"))
for path in sorted((S / "r/xvlog").glob("*")):
    put(f"xvlog/{path.name}", path.read_text(errors="replace"))
for path in sorted((S / "slotlogs").glob("*.log")):
    put(f"slotlogs/{path.name}", path.read_text(errors="replace"))
put("prep/prep.log", (S / "route/prep.log").read_text(errors="replace"))
put("prep/synth-dcp.sha256", (WORK / "synth-dcp.sha256").read_text())
print("collected into", dest)
