#!/usr/bin/env python3
"""Try to break the round-4 exit-code contract of the #234 resource gate structurally, as a real process.

Usage: probe_r4_structure.py <repo checkout> <real A route dir> <real A standalone 1x1 dir> <scratch dir>
Every case runs `python3 -B pp_resource_gate.py ...` from the checkout as a separate process with standard
output forced to strict ASCII (PYTHONIOENCODING=ascii:strict), and records the exit status, whether a
traceback appeared, whether standard output was pure printable ASCII, and the reason line.
Cases change only copies: a symlink farm of a real measurement directory with one file replaced, and a
copy of the committed baseline. The script never writes inside the checkout or the measurement directories.
Expectations: 'want' is the exit status the documented contract requires.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

repo, route, ooc, scratch = (Path(arg).resolve() for arg in sys.argv[1:5])
GATE = repo / "syn/ooc/pp_resource_gate.py"
BASE = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
results = []


def farm(src: Path, name: str, changes: dict) -> Path:
    folder = scratch / name
    folder.mkdir()
    for entry in sorted(src.iterdir()):
        if entry.name not in changes:
            (folder / entry.name).symlink_to(entry)
    for file, data in changes.items():
        if data is not None:
            (folder / file).write_bytes(data if isinstance(data, bytes) else data.encode("utf-8", "surrogatepass"))
    return folder


def baseline(name: str, edit=None, raw: str | None = None, zero: str | None = None) -> Path:
    path = scratch / f"{name}.json"
    if raw is not None:
        path.write_text(raw, encoding="utf-8", errors="surrogatepass")
        return path
    data = json.loads(json.dumps(BASE))
    if zero:
        data["endpoints"][zero]["record"]["inputs_sha256"] = "0" * 64
    if edit:
        edit(data)
    path.write_text(json.dumps(data, indent=1))
    return path


def run(label: str, want, argv: list, note: str = "") -> None:
    env = dict(os.environ, PYTHONIOENCODING="ascii:strict")
    result = subprocess.run([sys.executable, "-B", str(GATE), *[os.fsencode(str(a)) if isinstance(a, Path) else a
                                                                   for a in argv]],
                            capture_output=True, env=env, timeout=900, cwd=scratch)
    out, err = result.stdout, result.stderr.decode("ascii", "replace")
    ascii_ok = all(b == 10 or 32 <= b <= 126 for b in out)
    tb = "Traceback" in err
    reason = next((line for line in out.decode("ascii", "replace").splitlines()
                   if line.startswith(("NOT COMPARABLE", "RESULT", "baseline PASS")) or "the key" in line), "")
    if not reason:
        reason = (out.decode("ascii", "replace").strip().splitlines() or err.strip().splitlines() or [""])[-1]
    ok = (result.returncode in want if isinstance(want, tuple) else result.returncode == want) and ascii_ok \
        and (not tb or note == "test-mode")
    results.append((label, want, result.returncode, tb, ascii_ok, ok))
    print(f"{'OK ' if ok else 'BAD'} {label}: rc {result.returncode} want {want} traceback {tb} "
          f"ascii-stdout {ascii_ok} :: {reason[:230]}")
    if tb:
        print("    stderr tail: " + " | ".join(err.strip().splitlines()[-2:])[:300])


def text_of(path: Path) -> str:
    return path.read_text()


B = baseline("committed")
# --- the barrier and argument handling ------------------------------------------------------------
run("control: A route, committed baseline", 0, ["check", route, "--endpoint", "route-1x1", "--baseline", B])
run("control: A standalone 1x1", 0, ["check", ooc, "--endpoint", "ooc-1x1", "--baseline", B])
run("control: check-baseline", 0, ["check-baseline", "--baseline", B])
run("unknown endpoint (the 39e9329b path)", 2, ["check", route, "--endpoint", "route-9x9", "--baseline", B])
run("endpoint name with an undecodable byte", 2, ["check", route, "--endpoint", b"route-\xff", "--baseline", B])
link = scratch / os.fsdecode(b"mesur\xe9-\xff")
link.symlink_to(route)
run("directory named with undecodable bytes (printed in the result)", 0,
    ["check", link, "--endpoint", "route-1x1", "--baseline", B])
run("directory that is a file", 2, ["check", B, "--endpoint", "route-1x1", "--baseline", B])
run("directory name past NAME_MAX", 2, ["check", scratch / ("d" * 300), "--endpoint", "route-1x1", "--baseline", B])
run("baseline that is a directory", 2, ["check", route, "--endpoint", "route-1x1", "--baseline", scratch])
run("budget that is a directory", 2, ["check-baseline", "--baseline", B, "--budget", scratch])
run("standalone endpoint against the route directory", 2, ["check", route, "--endpoint", "ooc-1x1", "--baseline", B])
run("record without --write prints ASCII JSON", 0, ["record", route, "--endpoint", "route-1x1"])

# --- names -----------------------------------------------------------------------------------------
hier = text_of(route / "baseline_hierarchy.rpt")
child = re.search(r"^\|(       )(u_nvm)(\s+)\|", hier, re.M)  # a sub-block of pp_shadow, so it lands in scopes
odd = hier.replace(f"|{child[1]}{child[2]}{child[3]}|", f"|{child[1]}{child[2]}\u00e9\u202e{child[3][2:]}|", 1)
weird = farm(route, "weird-scope", {"baseline_hierarchy.rpt": odd})
run("candidate scope name with non-ASCII and a bidi mark (printed, never validated)", (0, 2),
    ["check", weird, "--endpoint", "route-1x1", "--baseline", baseline("zero-route", zero="route-1x1")])
wb = scratch / "write-target.json"
shutil.copy(B, wb)
before = wb.read_bytes()
run("record --write of that candidate", 2, ["record", weird, "--endpoint", "route-1x1", "--baseline", wb, "--write"])
print(f"    write target unchanged: {wb.read_bytes() == before}")
run("bracketed endpoint name", 2, ["check-baseline", "--baseline",
    baseline("brk-ep", lambda d: d["endpoints"].update({"route[1]": d["endpoints"]["route-1x1"]}))])
run("bracketed policy figure name", 2, ["check-baseline", "--baseline",
    baseline("brk-fig", lambda d: d["endpoints"]["route-1x1"]["tolerance"].update({"LUT[1]": 5}))])
run("bracketed identity key", 2, ["check-baseline", "--baseline",
    baseline("brk-id", lambda d: d["endpoints"]["route-1x1"]["record"]["identity"].update({"tool[1]": "x"}))])
run("bracketed scope name (manager-accepted class)", 0, ["check-baseline", "--baseline",
    baseline("brk-scope", lambda d: d["endpoints"]["route-1x1"]["record"]["scopes"].update(
        {"u_pp/g_x[7].y": dict.fromkeys(("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4"), 1)}))])
run("scope name with a space", 2, ["check-baseline", "--baseline",
    baseline("sp-scope", lambda d: d["endpoints"]["route-1x1"]["record"]["scopes"].update(
        {"u_pp/a b": dict.fromkeys(("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4"), 1)}))])
raw = (repo / "syn/ooc/pp_resource_baseline.json").read_text()
run("repeated key in the file", 2, ["check", route, "--endpoint", "route-1x1", "--baseline",
    baseline("dup", raw=raw.replace('"endpoints": {', '"schema": 1, "endpoints": {', 1))])
run("key of 129 characters", 2, ["check-baseline", "--baseline",
    baseline("long-key", lambda d: d.update({"x" * 129: 1}))])

# --- converters at every site ----------------------------------------------------------------------
L16, L400 = "9" * 16, "1" + "0" * 400


def jsite(label, path, value):
    def edit(d):
        node = d
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = "@@V@@"
    text = text_of(baseline("tmp-" + label, edit)).replace('"@@V@@"', value)
    for command in (["check", route, "--endpoint", "route-1x1"], ["check-baseline"]):
        run(f"JSON {label} = {value[:20]}{'...' if len(value) > 20 else ''} via {command[0]}", 2,
            [*command, "--baseline", baseline("site-" + label, raw=text)])


ep = ("endpoints", "route-1x1")
jsite("figure LUT", ep + ("record", "figures", "LUT"), L16)
jsite("figure WNS", ep + ("record", "figures", "WNS_ns"), "1e400")
jsite("scope count", ep + ("record", "scopes", "wrapper", "FF"), L16)
jsite("tolerance", ep + ("tolerance", "LUT"), L16)
jsite("tolerance decimal", ep + ("tolerance", "WNS_ns"), L400 + ".5")
jsite("floor", ep + ("floor", "WNS_ns"), "-1e400")
jsite("ceiling", ep + ("ceiling", "BRAM_TILE"), L16)
jsite("schema note", ("schema",), L16)
jsite("measured note", ep + ("measured",), "1E999")

Z = baseline("zero", zero="route-1x1")
util = text_of(route / "baseline_utilization.rpt")
lut = re.search(r"^\| Slice LUTs\s*\|\s*(\d+)\s*\|", util, re.M)
tile = re.search(r"^\| Block RAM Tile\s*\|\s*([0-9.]+)\s*\|", util, re.M)
timing = text_of(route / "baseline_timing.rpt")
status = sorted(route.glob("*_route_status.rpt"))[0]


def rsite(label, file, old, new, want, needle):
    text = text_of(route / file) if file != "status" else text_of(status)
    name = file if file != "status" else status.name
    if text.count(old) < 1:
        print(f"BAD {label}: plant text not found")
        return
    folder = farm(route, "r-" + re.sub(r"\W", "_", label), {name: text.replace(old, new, 1)})
    run(f"report {label}", want, ["check", folder, "--endpoint", "route-1x1", "--baseline", Z])
    log = results[-1]
    if needle:
        print(f"    reason names the converter ({needle!r}) - checked below by grep of the case log")


rsite("utilization LUT 16 digits", "baseline_utilization.rpt", lut[0], lut[0].replace(lut[1], L16), 2, "whole")
rsite("utilization LUT 15 digits (reaches judge)", "baseline_utilization.rpt", lut[0],
      lut[0].replace(lut[1], "9" * 15), 1, "")
rsite("half BRAM tile 400 digits", "baseline_utilization.rpt", tile[0], tile[0].replace(tile[1], L400 + ".5"), 2, "finite")
rsite("half BRAM tile 17 digits (finite, judged: ceiling)", "baseline_utilization.rpt", tile[0],
      tile[0].replace(tile[1], "9" * 16 + ".5"), 1, "")
row = [l for l in timing.split("| Design Timing Summary")[1].splitlines() if l.strip()]
heads = next(i for i, l in enumerate(row) if "WNS(ns)" in l)
vals = row[heads + 2].split()
rsite("WNS 400 digits", "baseline_timing.rpt", row[heads + 2], row[heads + 2].replace(vals[0], L400 + ".0", 1), 2,
      "finite")
names = re.split(r"\s{2,}", row[heads].strip())
ths = names.index("THS Total Endpoints")
newrow = row[heads + 2].replace(" " + vals[ths] + " ", " " + L16 + " ", 1)
rsite("THS endpoints 16 digits", "baseline_timing.rpt", row[heads + 2], newrow, 2, "whole")
srow = re.search(r"# of routable nets\.+ :\s+(\d+) :", text_of(status))
rsite("route status routable 16 digits", "status", srow[0], srow[0].replace(srow[1], L16), 2, "whole")
hrow = re.search(r"^\|\s+u_\w+\s+\|[^|]*\|\s*(\d+)\s*\|", hier, re.M)
rsite("hierarchy count 16 digits", "baseline_hierarchy.rpt", hrow[0], hrow[0][:hrow.start(1) - hrow.start(0)] + L16
      + hrow[0][hrow.end(1) - hrow.start(0):], 2, "whole")
budget = text_of(repo / "docs/design/AREA_BUDGET.md")
page = scratch / "budget-huge.md"
page.write_text(budget.replace("| +500 |", f"| +{L400} |", 1))
run("budget cell 400 digits via check-baseline", 2, ["check-baseline", "--baseline", B, "--budget", page])

# --- test modes outside the barrier (documented as everything after argument parsing) --------------
run("--fuzz on a missing --baseline (test mode)", (1, 2),
    ["--fuzz", "3", "check", route, "--endpoint", "route-1x1", "--baseline", scratch / "absent.json"], "test-mode")
run("--fuzz on a missing directory (test mode)", (1, 2),
    ["--fuzz", "3", "check", scratch / "absent-dir", "--endpoint", "route-1x1", "--baseline", B], "test-mode")
run("--fuzz on an endpoint the baseline lacks (test mode)", (1, 2),
    ["--fuzz", "3", "check", route, "--endpoint", "nope", "--baseline", B], "test-mode")

bad = [r for r in results if not r[5]]
tbs = [r for r in results if r[3]]
print(f"structure probe: {len(results)} cases, {len(bad)} off expectation, {len(tbs)} with a traceback "
      f"({', '.join(r[0] for r in tbs) or 'none'})")
