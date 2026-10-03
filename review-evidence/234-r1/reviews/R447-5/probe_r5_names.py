#!/usr/bin/env python3
"""Round-5 probe of the #234 resource gate's name class, as real processes, on every JSON the gate reads.

Usage: probe_r5_names.py <repo checkout> <real A route dir> <real A standalone 1x1 dir> <scratch dir>

The ruling under test (round-5 assignment, item 1): every key of the baseline and of the image manifest,
open objects included (notes, manifest entries), matches [A-Za-z0-9_.:/-]{1,128}; only a sub-block scope
name (endpoints/<any>/record/scopes/<key>) may also hold [ and ]. Anything else exits 2, named.

Every case runs `python3 -B pp_resource_gate.py ...` from the checkout as a separate process with standard
output forced to strict ASCII, and records exit status, traceback, ASCII-ness and the reason line. A case
passes when the exit status is the one the ruling requires, no traceback appears, standard output is pure
printable ASCII, and (where given) the reason line holds the expected text. Cases change only copies: a symlink
farm of a real measurement directory with one file replaced, and copies of the committed baseline.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

repo, route, ooc, scratch = (Path(arg).resolve() for arg in sys.argv[1:5])
GATE = repo / "syn/ooc/pp_resource_gate.py"
BASE = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
MANIFEST = json.loads((route / "baseline_images.json").read_text())
COUNTS = dict.fromkeys(("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4"), 1)
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
        (folder / file).write_text(data, encoding="utf-8", errors="surrogatepass")
    return folder


def baseline(name: str, edit=None, raw: str | None = None) -> Path:
    path = scratch / f"{name}.json"
    if raw is not None:
        path.write_text(raw, encoding="utf-8", errors="surrogatepass")
        return path
    data = json.loads(json.dumps(BASE))
    if edit:
        edit(data)
    path.write_text(json.dumps(data, indent=1))
    return path


def run(label: str, want: int, argv: list, needle: str = "") -> None:
    env = dict(os.environ, PYTHONIOENCODING="ascii:strict")
    result = subprocess.run([sys.executable, "-B", str(GATE), *map(str, argv)], capture_output=True, env=env,
                            timeout=900, cwd=scratch)
    out, err = result.stdout, result.stderr.decode("ascii", "replace")
    text = out.decode("ascii", "replace")
    ascii_ok = all(b == 10 or 32 <= b <= 126 for b in out)
    tb = "Traceback" in err
    reason = next((line for line in text.splitlines()
                   if line.startswith(("NOT COMPARABLE", "RESULT", "baseline PASS")) or "the key" in line), "")
    if not reason:
        reason = (text.strip().splitlines() or err.strip().splitlines() or [""])[-1]
    ok = result.returncode == want and ascii_ok and not tb and needle in text
    results.append(ok)
    print(f"{'OK ' if ok else 'BAD'} {label}: rc {result.returncode} want {want} traceback {tb} "
          f"ascii-stdout {ascii_ok} :: {reason[:260]}")
    if needle and needle not in text:
        print(f"    expected text not found: {needle!a}")


def both(label: str, path: Path, want: int, needle: str = "") -> None:
    """The same baseline through check (A route) and check-baseline."""
    run(f"{label} [check]", want, ["check", route, "--endpoint", "route-1x1", "--baseline", path], needle)
    run(f"{label} [check-baseline]", want, ["check-baseline", "--baseline", path], needle)


def put(*keys, value):
    def edit(data):
        node = data
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value
    return edit


EP = ("endpoints", "route-1x1")
B = baseline("committed")
print(f"committed baseline notes: file {sorted(k for k in BASE if k != 'endpoints')}, "
      f"route-1x1 {sorted(k for k in BASE['endpoints']['route-1x1'] if k not in ('record', 'tolerance', 'floor', 'ceiling'))}")
print(f"real A manifest: {len(MANIFEST)} entries, keys {sorted({k for e in MANIFEST for k in e})}")

# --- controls ------------------------------------------------------------------------------------
both("control: committed baseline", B, 0)
run("control: A standalone 1x1", 0, ["check", ooc, "--endpoint", "ooc-1x1", "--baseline", B])
run("control: record (prints, reads no baseline)", 0, ["record", route, "--endpoint", "route-1x1"])

# --- baseline: notes are open objects, their keys are of NAME -------------------------------------
both("named keys in every note (file description, schema, endpoint measured)",
     baseline("named-notes", lambda d: (put("description", value={"text": "x", "run.2:a/b-c_d": [{"s": 1}]})(d),
                                        put("schema", value={"v": 1})(d),
                                        put(*EP, "measured", value={"scopes": {"u_pp/x": 1}})(d))), 0)
both("128-character key in a note", baseline("k128", put("description", value={"k" * 128: 1})), 0)
both("bracketed key in the file description note", baseline("d-brk", put("description", value={"x[1]": 1})), 2,
     "in /description")
both("bracketed key in the schema note", baseline("s-brk", put("schema", value={"v[0]": 1})), 2, "in /schema")
both("bracketed key in the endpoint measured note", baseline("m-brk", put(*EP, "measured", value={"g[5]": 1})),
     2, "in /endpoints/route-1x1/measured")
both("bracketed key under scopes inside the measured note (path not the record's)",
     baseline("m-scopes", put(*EP, "measured", value={"scopes": {"u_pp/g_rx[5].u": COUNTS}})), 2,
     "in /endpoints/route-1x1/measured/scopes")
both("a whole record-shaped tree inside the description note",
     baseline("d-rec", put("description", value={"endpoints": {"x": {"record": {"scopes": {"g[1]": COUNTS}}}}})),
     2, "in /description/endpoints/x/record/scopes")
both("bracketed key deep in a note list", baseline("d-deep", put("description", value=[[{"a": [{"b[2]": 0}]}]])),
     2, "in /description/0/0/a/0")
both("lone bracket key in a note", baseline("d-rb", put("description", value={"]": 1})), 2)
both("empty key in a note", baseline("d-empty", put("description", value={"": 1})), 2)
both("129-character key in a note", baseline("d-129", put("description", value={"k" * 129: 1})), 2,
     "(129 characters)")
both("non-ASCII key in a note", baseline("d-uni", put("description", value={"café‮": 1})), 2,
     "\\xe9\\u202e")
both("lone-surrogate key in a note (JSON escape)",
     baseline("d-sur", raw=json.dumps(dict(BASE, description="__X__")).replace('"__X__"', '{"\\ud800": 1}')), 2,
     "\\ud800")
both("space key in the measured note", baseline("m-sp", put(*EP, "measured", value={"a b": 1})), 2)

# --- baseline: the one scope-name place -------------------------------------------------------------
both("bracketed scope name at endpoints/<e>/record/scopes",
     baseline("scope-brk", lambda d: d["endpoints"]["route-1x1"]["record"]["scopes"].update(
         {"u_pp/g_x[7].y": COUNTS})), 0)
both("bracketed scope name on the standalone endpoint",
     baseline("scope-brk-ooc", lambda d: d["endpoints"]["ooc-1x1"]["record"]["scopes"].update(
         {"g_rx_pool[5].u_rx_slots": COUNTS})), 0)
both("bracketed count key inside a scope (one level below the scope names)",
     baseline("scope-count-brk", lambda d: d["endpoints"]["route-1x1"]["record"]["scopes"].update(
         {"u_pp/s": dict(COUNTS, **{"LUT[0]": 1})})), 2, "in /endpoints/route-1x1/record/scopes/u_pp/s")
both("scope name with a space", baseline("scope-sp", lambda d: d["endpoints"]["route-1x1"]["record"]["scopes"]
                                         .update({"u_pp/a b": COUNTS})), 2)
both("scope name with a brace", baseline("scope-br", lambda d: d["endpoints"]["route-1x1"]["record"]["scopes"]
                                         .update({"u_pp/{x}": COUNTS})), 2)
both("bracketed record key", baseline("rec-brk", put(*EP, "record", "kind[0]", value="route")), 2,
     "in /endpoints/route-1x1/record")
both("bracketed figure key", baseline("fig-brk", put(*EP, "record", "figures", "LUT[0]", value=1)), 2,
     "in /endpoints/route-1x1/record/figures")
both("bracketed identity key", baseline("id-brk", put(*EP, "record", "identity", "tool[1]", value="x")), 2,
     "in /endpoints/route-1x1/record/identity")
both("bracketed ceiling key", baseline("ceil-brk", put(*EP, "ceiling", "BRAM_TILE[0]", value=1)), 2,
     "in /endpoints/route-1x1/ceiling")
both("bracketed endpoint name", baseline("ep-brk", lambda d: d["endpoints"].update(
    {"route[1]": d["endpoints"]["ooc-1x1"]})), 2, "in /endpoints")
both("bracketed top-level key", baseline("top-brk", put("x[1]", value=1)), 2, "in /")

# --- record --write: the text it would write is read the same way ------------------------------------
wb = scratch / "write-target.json"
shutil.copy(baseline("w-brk", put("description", value={"x[1]": 1})), wb)
before = wb.read_bytes()
run("record --write onto a baseline whose note holds a bracketed key", 2,
    ["record", route, "--endpoint", "route-1x1", "--baseline", wb, "--write"], "in /description")
print(f"    write target unchanged: {wb.read_bytes() == before}")
results.append(wb.read_bytes() == before)

# --- the image manifest: every key of NAME, entries included, no scope-name place -------------------
def manifest(label, want, entries=None, raw=None, needle="", base=route, endpoint="route-1x1", commands=("check",)):
    text = raw if raw is not None else json.dumps(entries)
    folder = farm(base, f"m-{len(results)}", {"baseline_images.json": text})
    for command in commands:
        argv = [command, folder, "--endpoint", endpoint] + (["--baseline", B] if command == "check" else [])
        run(f"manifest: {label} [{command}]", want, argv, needle)


extra = lambda key, value=1, where=0: [dict(e, **{key: value}) if i == where else e for i, e in enumerate(MANIFEST)]
manifest("unchanged copy (control)", 0, MANIFEST, commands=("check", "record"))
manifest("another named key in an entry", 0, extra("bytes"), commands=("check", "record"))
manifest("128-character key in an entry", 0, extra("k" * 128))
manifest("bracketed key in the first entry", 2, extra("x[1]"), needle="in /0", commands=("check", "record"))
manifest("bracketed key in the last entry", 2, extra("g_rx[5].u", where=len(MANIFEST) - 1),
         needle=f"in /{len(MANIFEST) - 1}")
manifest("bracketed key inside an entry's object value", 2, extra("meta", {"x[1]": 1}), needle="in /0/meta")
manifest("bracketed key at the scopes-like path of an entry", 2,
         extra("endpoints", {"e": {"record": {"scopes": {"g[1]": 1}}}}), needle="in /0/endpoints/e/record/scopes")
manifest("129-character key in an entry", 2, extra("k" * 129), needle="(129 characters)")
manifest("non-ASCII key in an entry", 2, extra("é"), needle="\\xe9")
manifest("empty key in an entry", 2, extra(""))
manifest("repeated key in an entry", 2, raw=json.dumps(MANIFEST).replace('"sha256":', '"sha256": "0", "sha256":', 1),
         needle="appears twice")
manifest("manifest as an object with a bracketed key", 2, raw='{"x[1]": []}', needle="in /")
manifest("bracketed key on the standalone measurement", 2,
         json.loads((ooc / "baseline_images.json").read_text()) and
         [dict(e, **{"x[1]": 1}) if i == 0 else e for i, e in enumerate(json.loads((ooc / "baseline_images.json")
                                                                                   .read_text()))],
         base=ooc, endpoint="ooc-1x1", needle="in /0")

print(f"probe_r5_names: {len(results)} checks, {results.count(False)} not as the ruling requires")
sys.exit(1 if results.count(False) else 0)
