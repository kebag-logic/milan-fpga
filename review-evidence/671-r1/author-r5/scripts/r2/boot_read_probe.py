"""Price the shipping boot's slot reads on the product CPU (#671 round 2).

Runs the fw_service_budget native simulator, which executes the unchanged
product firmware on the cacheless RV32I CPU at 50 MHz behind the product
LiteSPI master and a 12.5 MHz single-lane serial flash model, over crafted
slot fixtures, and reads the simulator's own marker events. The span from the
first AEM flash read to the restore walk's start holds the AEM copy and CRC
(the same in every fixture) and all of nvm_boot()'s slot reads; the
difference between two fixtures is the cost of the reads that differ.

usage: boot_read_probe.py REPO BUILD_DIR WORK SHAPE FIXTURE...
  FIXTURE = name:A:B, each of A and B one of
    blank      every byte 0xFF
    valid      the harness's own valid container (sequence 1)
    long<N>    that container with its length word set to N: tests 1 to 3
               pass, so the read copies N bytes and the CRC refuses it
"""
import struct
import subprocess
import sys
from pathlib import Path

repo, build, work, shape = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(repo / "tb/verilator/fw_service_budget"))
import run as service  # noqa: E402

media = service.fixtures(build, shape, True)
valid = (build / "slots.bin").read_bytes()[:media["image_bytes"]]


def slot(spec: str) -> bytes:
    """One 64 KiB slot as the fixture names it."""
    if spec == "blank":
        return b"\xff" * 0x10000
    if spec == "valid":
        return valid + b"\xff" * (0x10000 - len(valid))
    if spec.startswith("long"):
        body = bytearray(valid + b"\xff" * (0x10000 - len(valid)))
        struct.pack_into("<I", body, 16, int(spec[4:]))
        return bytes(body)
    raise SystemExit(f"bad slot {spec}")


print(f"PROBE shape={shape} valid_container={len(valid)} B")
for fixture in sys.argv[5:]:
    name, a, b = fixture.split(":")
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "slots.bin").write_bytes(slot(a) + slot(b))
    (d / "commands.txt").write_text("milan_gettime\n")
    argv = [str(build / "native/Vsim"), str(build / "aem_desc.bin"), str(d / "slots.bin"),
            str(d / "commands.txt"), "0", "0", "0"]
    with (d / "sim.log").open("w") as log:
        rc = subprocess.run(argv, cwd=build / "gateware", stdout=log, stderr=subprocess.STDOUT,
                            check=False).returncode
    raw = (d / "sim.log").read_text(errors="replace")
    events = service.read_events(raw)
    writes = [e for e in events if e["kind"] == "write"]
    aem = next(e for e in events if e["kind"] == "aem_read")["cycle"]
    walk = next(e for e in writes if e["address"] == 0x920 and e["value"] & 2)["cycle"]
    enable = next(e for e in writes if e["address"] == 0x920 and e["value"] & 1)["cycle"]
    reads = sum(1 for e in events if e["kind"] == "flash" and aem <= e["cycle"] <= walk)
    line = next((ln for ln in raw.splitlines() if ln.startswith("Milan NVM: slot A")), "no boot line")
    print(f"PROBE {name} A={a} B={b} rc={rc} aem_to_walk_ms={(walk - aem) / 100_000:.5f} "
          f"boot_to_enable_ms={(enable - 64) / 100_000:.5f} flash_ops_aem_to_walk={reads}")
    print(f"PROBE   {line[:240]}")
