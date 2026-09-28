"""Replace the receipt only after all six measured arms pass their oracles."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

root = Path.cwd()
sys.path.insert(0, str(root / "tb/verilator/nvm_capture_cpu"))
import run
import firmware

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

receipt_path = root / "tb/verilator/nvm_capture_cpu/measurements.json"
receipt = json.loads(receipt_path.read_text())
rows = []
artifacts = []
for short, shape, cpu in (("1x1", "endstation_ax7101_1x1_tdm8", 50000000),
                           ("8x8", "endstation_ax7101_8x8", 50000000),
                           ("8x8", "endstation_ax7101_8x8", 100000000)):
    for traffic in ("on", "off"):
        build = Path(f"/tmp/a385-final3-capture-{short}-{cpu // 1000000}-{traffic}")
        spec = json.loads((build / "sources.json").read_text())
        measured = json.loads((build / "measurement.json").read_text())
        assert spec["shape"] == shape and spec["cpu_hz"] == cpu
        assert spec["traffic"] == traffic and spec["mutation"] == "none"
        assert spec["captures"] == 16 and spec["sys_hz"] == 100000000
        assert run.grade_rows(measured["rows"], spec) == measured
        with tempfile.TemporaryDirectory(prefix="capture-source-binding-") as temporary:
            generated = firmware.prepare(root, Path(temporary), "none" if traffic == "on" else "no-traffic")
            assert (generated / "milan_baremetal.c").read_bytes() == (build / "measurement_firmware/milan_baremetal.c").read_bytes()
        cpu_sources = [Path(name) for name in spec["sources"] if Path(name).name.startswith("VexiiRiscvLitex_")]
        assert len(cpu_sources) == 1
        measured.update(clock_role="contract" if cpu == 50000000 else "non-contract comparison",
                        command=f'unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py --shape {shape} --cpu-hz {cpu} --captures 16 --traffic {traffic} --build-dir /tmp/capture-{short}-{cpu // 1000000}-{traffic}',
                        cpu_netlist_sha256=digest(cpu_sources[0]),
                        instrumented_firmware_sha256=digest(build / "measurement_firmware/milan_baremetal.c"),
                        bios_sha256=digest(build / "software/bios/bios.bin"),
                        gptp_ucode_sha256=digest(build / "generated" / shape / "gptp_ucode.hex"),
                        config_sha256=digest(root / "configs" / (shape + ".yaml")))
        rows.append(measured)
        for path in (build / "capture.log", build / "measurement.json", build / "software/bios/bios.bin", cpu_sources[0]):
            artifacts.append(dict(path=str(path), size=path.stat().st_size, sha256=digest(path)))
receipt["measurements"] = rows
receipt["maxima"] = []
for shape, cpu in sorted({(row["shape"], row["cpu_hz"]) for row in rows}):
    maximum = run.maximum_ms([row for row in rows if (row["shape"], row["cpu_hz"]) == (shape, cpu)])
    receipt["maxima"].append(dict(shape=shape, cpu_hz=cpu, maximum_ms=maximum, margin=49 / maximum))
for name in receipt["processor_pins"]:
    location = root / name
    assert Path(git("-C", str(location), "rev-parse", "--show-toplevel")) == location
    pin = git("-C", str(location), "rev-parse", "HEAD")
    assert pin == git("ls-tree", "HEAD", name).split()[2]
    receipt["processor_pins"][name] = pin
assert receipt["processor_pins"]["protocol-processor"] == "16be6768f710e79450aace277abacd6c2c3336e5"
receipt["product_firmware_sha256"] = digest(root / "sw/firmware/milan_baremetal/milan_baremetal.c")
for name in receipt["harness_sha256"]:
    receipt["harness_sha256"][name] = digest(root / "tb/verilator/nvm_capture_cpu" / name)
receipt["base"] = git("rev-parse", "HEAD")
receipt["tree"] = git("rev-parse", "HEAD^{tree}")
receipt["date"] = "2026-09-28"
receipt["remeasurement_assignment"] = "https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453"
receipt["provenance"] = "All six arms measure the merged processor pin and the bound firmware digest. Earlier 870ff88a measurements are historical only."
receipt["reproduction_environment"]["PATH"] = "product environment first; host utilities before SDK utilities"
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
out = Path(__file__).parent
(out / "capture-artifacts-final.json").write_text(json.dumps(artifacts, indent=2) + "\n")
print(json.dumps(receipt["maxima"], indent=2))
