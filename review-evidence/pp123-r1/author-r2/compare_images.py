#!/usr/bin/env python3
"""Rebuild the round-1 inventory at base, round 1 and round 2; require equality."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

scratch = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
evidence = scratch / "evidence/review-evidence/pp123-r1/author"
round1_inventory = json.loads((evidence / "image-digests-before.json").read_text())
round1_probes = json.loads((evidence / "probe-image-digests.json").read_text())


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command, root, log):
    log.write("Command: " + " ".join(command) + "\n")
    log.flush()
    result = subprocess.run(command, cwd=root, stdout=log, stderr=subprocess.STDOUT,
                            timeout=7200)
    assert result.returncode == 0, (command, result.returncode)


images = {}
reports = {}
for label in ("base", "round1", "head"):
    root = scratch / label
    artifacts = scratch / ("images-" + label)
    artifacts.mkdir(exist_ok=True)
    with (out / ("images-" + label + "-build.log")).open("w") as log:
        run([sys.executable, "hdl/aecp/desc/gen_desc_image.py", "-i",
             "hdl/aecp/desc/example_milan_8.json", "-o",
             str(artifacts / "example_milan_8.bin"), "-m",
             str(artifacts / "example_milan_8.map")], root, log)
        for directory, targets in (
            ("desc_store", ["image.bin"]),
            ("acmp_listener", ["ltn_rom.hex"]),
            ("acmp_nvm", ["ltn_rom.hex"]),
            ("pp_top", ["ltn_rom.hex", "ucode.hex"]),
            ("ucpu", ["ucode.hex"]),
        ):
            run(["make", "-B", "-C", "tb/" + directory, *targets], root, log)
        run([sys.executable, "hdl/aecp/ucode/gen_ucode.py", "-o",
             str(artifacts / "yosys_ucode.hex")], root, log)
        run([sys.executable, "hdl/acmp/rom/gen_ltn_rom.py", "-o",
             str(artifacts / "yosys_ltn_rom.hex")], root, log)
    images[label] = {}
    for name, expected in round1_inventory.items():
        path = root / name if name.startswith("tb/") else artifacts / name
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected["sha256"], (label, name)
        assert len(data) == expected["bytes"], (label, name)
        images[label][name] = data
    reports[label] = [(artifacts / "example_milan_8.map").read_bytes(),
                      (root / "tb/desc_store/image.map").read_bytes()]


def record_inventory(data, expected):
    records = {}
    for name in data["base"]:
        values = {label: entries[name] for label, entries in data.items()}
        assert values["base"] == values["round1"] == values["head"], name
        records[name] = {
            "bytes": len(values["head"]),
            "base_sha256": hashlib.sha256(values["base"]).hexdigest(),
            "round1_sha256": hashlib.sha256(values["round1"]).hexdigest(),
            "head_sha256": hashlib.sha256(values["head"]).hexdigest(),
            "byte_identical": True,
            "matches_published_round1": True,
        }
    return records


assert reports["base"] == reports["round1"] == reports["head"]
records = record_inventory(images, round1_inventory)
(out / "image-digests.json").write_text(json.dumps(records, indent=2) + "\n")
tests = load_module("body_key_tests", scratch / "head/tb/desc_store/test_gen_desc_image.py")
case = tests.BodyKeyTest()
probes = {label: {} for label in images}
probe_maps = {label: {} for label in images}
for label in probes:
    generator = load_module("generator_" + label, scratch / label / "hdl/aecp/desc/gen_desc_image.py")
    for form in ("fields", "bytes"):
        for key, typ in case.KEYS:
            name = f"{form}-{type(key).__name__}-{key}.bin"
            image, report = generator.build(case.model(form, key, typ))
            expected = round1_probes[name]
            assert hashlib.sha256(image).hexdigest() == expected["before_sha256"]
            assert len(image) == expected["bytes"]
            probes[label][name] = image
            probe_maps[label][name] = report
assert probe_maps["base"] == probe_maps["round1"] == probe_maps["head"]
probe_records = record_inventory(probes, round1_probes)
(out / "probe-image-digests.json").write_text(json.dumps(probe_records, indent=2) + "\n")
print("All 9 generated image paths and 8 legal probe images are byte-identical at base, round 1 and head.")
print("Every SHA-256 and size matches the published round-1 table; example, store and probe maps also agree.")
