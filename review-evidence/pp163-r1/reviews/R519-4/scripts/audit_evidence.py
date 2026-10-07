#!/usr/bin/env python3
"""Check measurement summaries, image generation and unchanged source identities."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("source", type=Path)
ap.add_argument("packet", type=Path)
args = ap.parse_args()
source, packet = args.source.resolve(), args.packet.resolve()
out = packet / "receipts"
public = out / "public"
measurement = public / "author-r3/measurement-m3final"
evidence = public / "author-r3/evidence"
sha = lambda data: hashlib.sha256(data).hexdigest()
manifest = {x["file"]: x for x in json.loads((public / "MANIFEST.json").read_text())}
verified = []
for path in sorted(public.rglob("*")):
    if not path.is_file() or path.name == "MANIFEST.json":
        continue
    rel = path.relative_to(public).as_posix()
    digest = sha(path.read_bytes())
    assert digest == manifest[rel]["published_sha256"], rel
    verified.append(dict(path=rel, sha256=digest))
record = json.loads((measurement / "record-m3final.stdout").read_text())
summary = json.loads((evidence / "measurement-m3final.json").read_text())
assert record["figures"]["WNS_ns"] == summary["timing"]["setup"]["worst_slack_ns"] == 3.337
assert record["figures"]["WHS_ns"] == summary["timing"]["hold"]["worst_slack_ns"] == 0.159
histogram = summary["cone"]["histogram"]
assert sum(histogram.values()) == summary["cone"]["pairs"] == 17990
assert max(map(int, histogram)) == summary["cone"]["max_levels"] == 16
assert sum(v for k, v in histogram.items() if int(k) > 20) == summary["cone"]["above_20"] == 0
assert record["identity"]["standalone_clock_ns"] == ["20.000"]
assert "set_param general.maxThreads 2" in record["identity"]["flow"]
rcs = {p.name: int(p.read_text()) for p in measurement.glob("*.rc")}
assert len(rcs) == 6 and set(rcs.values()) == {0}
params = json.loads((measurement / "ooc-m3final/baseline_parameters.json").read_text())
numeric = dict(item.split("=", 1) for item in (measurement / "ooc-m3final/baseline_chparam.txt").read_text().split())
assert numeric == {k: str(v) for k, v in params.items() if isinstance(v, int)}
assert len(numeric) == 19
images = {Path(x["path"]).name: x for x in json.loads((measurement / "inputs-digest/baseline_images.json").read_text())}
image_work = packet / "scratch/image-regeneration"
image_work.mkdir(exist_ok=True)
image_results = []
for name, generator in [("ltn_rom.hex", "hdl/acmp/rom/gen_ltn_rom.py"), ("ucode.hex", "hdl/aecp/ucode/gen_ucode.py")]:
    destination = image_work / name
    run = subprocess.run(["python3", str(source / generator), "-o", str(destination)],
                         cwd=image_work, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                         text=True, capture_output=True)
    (out / (name + "-generation.log")).write_text(run.stdout + run.stderr)
    (out / (name + "-generation.rc")).write_text(str(run.returncode) + "\n")
    assert run.returncode == 0
    data = destination.read_bytes()
    assert sha(data) == images[name]["sha256"] and len(data) == images[name]["bytes"]
    image_results.append(dict(name=name, bytes=len(data), sha256=sha(data), match=True))
assert images["alinx_ax7101_sram.init"]["sha256"] == sha(b"")
image_results.append(dict(name="alinx_ax7101_sram.init", bytes=0, sha256=sha(b""), match=True))
def blob(rev, path):
    return subprocess.check_output(["git", "-C", str(source), "rev-parse", rev + ":" + path], text=True).strip()
donors = []
for path, donor in [("hdl/aecp/KL_aecp_notify.sv", "c9f74b68"), ("hdl/packet_engine/KL_pp_tx_arbiter.sv", "cd9825c9")]:
    current, previous = blob("HEAD", path), blob(donor, path)
    assert current == previous
    donors.append(dict(path=path, donor=donor, head_blob=current, donor_blob=previous, match=True))
own_base = json.loads((evidence / "measurement-m3base.json").read_text())["area"]
own_head = summary["area"]
own_delta = {kind: sum(own_head[k][kind] - own_base[k][kind] for k in ["(u_pp)", "u_tx_arbiter"]) for kind in ["lut", "ff"]}
assert own_delta == {"lut": -110, "ff": 6}
result = dict(public_blobs_validated=len(verified), public_manifest_matches=verified,
              numeric_parameters=19, regenerated_images=image_results,
              other_images="Firmware ROM, auxiliary memory and clock-processor image identities are from the published manifest/audit, not fresh builds.",
              source_donor_matches=donors, reported_measurement=dict(wns=3.337, whs=0.159, pairs=17990, max_levels=16, above_20=0, own_delta=own_delta),
              published_execution_rcs=rcs,
              limits="Summary arithmetic/result linkage checked; no synthesis, route or full path-table replay performed.")
(out / "evidence-audit.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "public_manifest_matches"}, indent=2))
