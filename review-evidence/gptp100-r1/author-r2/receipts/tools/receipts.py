"""Build the output directory's receipts from the recorded runs, scrubbed of host paths.

usage: receipts.py <out dir>

Each recorded-gates spec becomes receipts/<label>/ with its logs (host paths and
the host name replaced by placeholders) and a results.md table; the engine arm's
job files become receipts/engine-arm-<head>/jobs.md; the OOC reports become
receipts/ooc-<label>/ plus ooc-figures.md. INDEX.md lists every file present
with its size and sha256, generated last from the directory itself.
"""
import hashlib
import json
import re
import socket
import sys
from pathlib import Path

S = Path("<scratch>")
OUT = Path(sys.argv[1])
VROOT = ("<home>/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff")
SUBS = [
    (VROOT, "<verilator-5.050>"),
    (str(S / "runs" / "r2-fast"), "<repo@head>"),
    (str(S / "runs" / "r2-arm"), "<repo@head>"),
    (str(S / "runs" / "main-ooc"), "<repo@main>"),
    ("<parent-B>", "<parent-B>"),
    ("<parent-A>", "<parent-A>"),
    (str(S), "<scratch>"),
    ("<lane>", "<lane>"),
    ("<data>", "<data>"),
    ("<vivado>", "<vivado>"),
    ("<vivado>", "<vivado>"),
    ("<home>", "<home>"),
]
HOST = socket.gethostname()
LIMIT = 200 * 1024


def scrub(text: str) -> str:
    for old, new in SUBS:
        text = text.replace(old, new)
    text = re.sub(rf"\b{re.escape(HOST)}\b", "<host>", text)
    return re.sub(r"\balex\b", "<user>", text)


def put(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = scrub(text).encode()
    assert len(data) < LIMIT, (path, len(data))
    path.write_bytes(data)


def gate_receipt(label: str, spec_dir: Path) -> None:
    res = json.loads((spec_dir / "results.json").read_text())
    done = json.loads((spec_dir / "complete.json").read_text()) if (spec_dir / "complete.json").exists() else None
    rows = ["| # | Command | rc | Seconds | Log | Log sha256 |", "|---:|---|---:|---:|---|---|"]
    for i, r in enumerate(res["results"], 1):
        cmd = r["command"]
        cmd = cmd[cmd.index("VERILATOR_JOBS=4") + 1:]
        src = Path(r["log"])
        raw = src.read_bytes()
        name = f"{i:02d}.log"
        put(OUT / "receipts" / label / name, raw.decode(errors="replace"))
        rows.append(f"| {i} | `{' '.join(cmd)}` | {r['exit_code']} | {r['seconds']} | [{name}]({name}) "
                    f"| `{hashlib.sha256(raw).hexdigest()[:16]}` |")
    head = [f"# {label}", "", f"- Head: `{res['head']}`", f"- Base: `{res['base']}`",
            f"- Finished: {done['finished'] if done else 'NOT FINISHED'}; runner exit {done['exit_code'] if done else '-'}",
            "- Environment: the pinned Verilator 5.050, `VERILATOR_JOBS=4`, `MAKEFLAGS=-j4`, one unit, MemoryMax 10G.",
            "- Log sha256 is of the original log; the copy here has host paths replaced by placeholders.", ""]
    put(OUT / "receipts" / label / "results.md", "\n".join(head + rows) + "\n")


def arm_receipt(label: str, arm_dir: Path) -> None:
    jobs = sorted(arm_dir.glob("[0-9][0-9][0-9].json"))
    rows, ok = [], 0
    for j in jobs:
        d = json.loads(j.read_text())
        ok += bool(d["ok"])
        rows.append(f"## {j.stem} {'ok' if d['ok'] else 'NOT OK'}: {d['name']} ({d['seconds']} s)\n")
        rows.extend(f"    {line}\n" for line in d["lines"])
        rows.append("\n")
    head = (f"# {label}\n\nThe engine mutation arm (`tb/verilator/engine/mutants.py`) run by arm_jobs.py: "
            "job 000 is the arm's own unmutated control, every other job is `mutants.run_mutant()` on one "
            "MUTATIONS entry, in parallel workers (8 for a full arm, 3 for the fix check).\n\n"
            f"Tally: {len(jobs)} checks: {ok} PASS, {len(jobs) - ok} FAIL\n\n")
    put(OUT / "receipts" / label / "jobs.md", head + "".join(rows))


def util(rpt: str) -> dict:
    want = {"Slice LUTs*": "LUT", "LUT as Logic": "LUT logic", "LUT as Memory": "LUTRAM",
            "Slice Registers": "FF", "Block RAM Tile": "BRAM tile", "DSPs": "DSP"}
    out = {}
    for line in rpt.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) > 1 and cells[0] in want and want[cells[0]] not in out:
            out[want[cells[0]]] = cells[1]
    return out


def timing(rpt: str) -> dict:
    lines = rpt.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("WNS(ns)") and "TNS(ns)" in line:
            v = lines[i + 2].split()
            return {"WNS ns": v[0], "TNS ns": v[1], "failing": v[2], "endpoints": v[3]}
    return {}


def ooc_receipt(label: str, work: Path) -> dict:
    figs = {}
    for top in ("ucpu", "engine"):
        u = (work / f"{top}_util.rpt").read_text()
        t = (work / f"{top}_timing.rpt").read_text()
        put(OUT / "receipts" / label / f"{top}_util.rpt", u)
        put(OUT / "receipts" / label / f"{top}_timing.rpt", t)
        figs[top] = {**util(u), **timing(t)}
    return figs


def index() -> None:
    rows = ["# Receipt index", "", "Generated from the files present (size in bytes, sha256).", "",
            "| File | Bytes | sha256 |", "|---|---:|---|"]
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "INDEX.md":
            data = p.read_bytes()
            rows.append(f"| [{p.relative_to(OUT)}]({p.relative_to(OUT)}) | {len(data)} "
                        f"| `{hashlib.sha256(data).hexdigest()}` |")
    (OUT / "INDEX.md").write_text("\n".join(rows) + "\n")


if __name__ == "__main__":
    H, M = "84fd227", "5184fb3"
    gates = [("final/repo-gates-" + H, S / "specs" / "r2-fast"),
             ("final/parent-A-" + H, S / "specs" / "pA"), ("final/parent-B-" + H, S / "specs" / "pB"),
             ("base/ooc-run-" + M, S / "specs" / "main-ooc"), ("final/engine-arm-run-" + H, S / "specs" / "r2-arm")]
    for label, d in gates:
        if (d / "results.json").exists():
            gate_receipt(label, d)
    if (S / "arm-84fd227").exists():
        arm_receipt("final/engine-arm-" + H, S / "arm-84fd227")
    figs = {}
    for label, work in (("ooc-" + M, S / "runs" / "main-ooc" / "syn/ooc/work"),
                        ("ooc-" + H, S / "runs" / "r2-fast" / "syn/ooc/work")):
        if (work / "engine_timing.rpt").exists():
            figs[label] = ooc_receipt(label, work)
    if figs:
        keys = ["LUT", "LUT logic", "LUTRAM", "FF", "BRAM tile", "DSP", "WNS ns", "TNS ns", "failing", "endpoints"]
        rows = ["# OOC area and timing (syn/ooc/run.sh, `make ooc`, part xc7a100tfgg484-2, clk 10 ns)", "",
                "| Run | Top | " + " | ".join(keys) + " |", "|---|---|" + "---:|" * len(keys)]
        for label, f in figs.items():
            for top, v in f.items():
                rows.append(f"| {label} | {top} | " + " | ".join(v.get(k, "-") for k in keys) + " |")
        put(OUT / "receipts" / "ooc-figures.md", "\n".join(rows) + "\n")
    for tool in ("arm_jobs.py", "mkspec.py", "launch.sh", "receipts.py"):
        put(OUT / "receipts" / "tools" / tool, (S / "tools" / tool).read_text())
    index()
    print("receipts written")
