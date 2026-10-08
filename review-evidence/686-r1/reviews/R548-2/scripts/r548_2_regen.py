#!/usr/bin/env python3
"""R548-2: rebuild one resource-gate measurement directory from published
receipts and read it with the reviewed head's own pp_resource_gate.record().

Usage: python3 -I r548_2_regen.py <clone-at-head> <receipt-endpoint-dir> <endpoint> <out-dir>

Independent of the receipts' own regen script: nothing here re-implements a
digest or a parser. The receipt files are placed under their report names
(the CARRY4-only census as baseline_cells.tsv, the timing summary excerpt as
baseline_timing.rpt), the non-repository inputs at paths the executed Tcl
names, and the Tcl's host placeholders are resolved to those paths and to the
clone (read only). gate.record() then computes identity, input digest,
figures and scopes exactly as `pp_resource_gate.py check|record` would, and
gate.routing() reads the route status. The result is compared, key by key,
with the head's committed baseline record. Exit 0 only on full equality and,
for a route, a complete route status.
"""
import gzip
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main() -> int:
    clone, rdir, endpoint, out = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                  sys.argv[3], Path(sys.argv[4]).resolve())
    mods = out / "modules"
    if out.exists():
        shutil.rmtree(out)
    mods.mkdir(parents=True)
    for path in (clone / "syn/ooc").glob("*.py"):
        shutil.copy(path, mods / path.name)
    sys.path.insert(0, str(mods))
    import pp_resource_gate as gate  # noqa: E402  (the head's own gate)

    manifest = json.loads((rdir / "inputs.manifest.json").read_text())
    kind = manifest["kind"]
    meas = out / "meas"
    gen = meas if kind == "route" else out / "gen"
    home = out / "home"
    for d in (meas, gen):
        d.mkdir(parents=True, exist_ok=True)
    skip = {"record.json", "regen.log", "files.sha256", "inputs.manifest.json"}
    for path in rdir.iterdir():
        if not path.is_file() or path.name in skip:
            continue
        data, name = path.read_bytes(), path.name
        if name.endswith(".gz"):
            data, name = gzip.decompress(data), name[:-3]
        name = {"baseline_cells.carry4.tsv": "baseline_cells.tsv",
                "baseline_timing.summary.rpt": "baseline_timing.rpt"}.get(name, name)
        (meas / name).write_bytes(data)
    vex = home / "litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog"
    vex.mkdir(parents=True)
    for entry in manifest["files"]:
        if entry["role"] == "repo":
            continue
        raw = (rdir / entry["copy"]).read_bytes()
        data = gzip.decompress(raw) if entry["copy"].endswith(".gz") else raw
        target = (vex if entry["role"] == "external" else gen) / entry["name"]
        target.write_bytes(data)
    script_name = gate.SCRIPTS[kind]
    script = (meas / script_name).read_text()
    for token, value in (("<repo>", clone), ("<home>", home), ("<measurement>", meas),
                         ("<generated>", gen)):
        script = script.replace(token, str(value))
    left = sorted({w for w in script.split() if w.startswith("<") and w.endswith(">")})
    (meas / script_name).write_text(script)
    rec = gate.record(meas, kind)
    unrouted = gate.routing(meas, kind)
    baseline = json.loads((clone / "syn/ooc/pp_resource_baseline.json").read_text())
    committed = baseline["endpoints"][endpoint]["record"]
    receipt = json.loads((rdir / "record.json").read_text())
    print(f"{endpoint}: kind {kind}; unresolved placeholders {left}")
    print(f"{endpoint}: identity {json.dumps(rec['identity'])}")
    print(f"{endpoint}: inputs_sha256 {rec['inputs_sha256']}")
    print(f"{endpoint}: figures {json.dumps(rec['figures'], sort_keys=True)}")
    ok = True
    for key in gate.RECORD:
        same = rec.get(key) == committed.get(key)
        ok &= same
        print(f"{endpoint}: {key:14s} vs committed head record: {'EQUAL' if same else 'DIFFERENT'}")
    same = rec == receipt
    print(f"{endpoint}: whole record vs receipt record.json: {'EQUAL' if same else 'DIFFERENT'}")
    ok &= same and rec == committed
    if kind == "route":
        print(f"{endpoint}: route status {'complete' if not unrouted else unrouted}")
        ok &= not unrouted
    print(f"{endpoint}: {'RECORD EQUAL' if ok else 'RECORD NOT REPRODUCED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
