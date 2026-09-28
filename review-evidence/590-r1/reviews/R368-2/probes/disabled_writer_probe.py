#!/usr/bin/env python3
"""Review probe R368-2: does a disabled (not retired) writer heartbeat?

Usage: python3 -B disabled_writer_probe.py <repo-root> <work-dir>
Uses the repository's own host bench (test_nvm_firmware.make_bench/run) on
the 1x1 AX7101 shape. Preconditions are planted, not the behavior under test:
  shape-mismatch : nvm_shape_consistent() reports a mismatch, so nvm_boot()
                   prints "persistence disabled" and returns early
  csr-id-mismatch: milan_init() sees a wrong CSR identity and returns
                   before nvm_boot()
The firmware's reaction afterwards (dispatch hook, handlers) is unchanged.
Firmware versions: the head, the head with an empty dispatch hook, the
round-1 head 792a57b0 and the source base 8bc97021 (older texts get an empty
hook definition so they link with the head host driver).
Reports the HOST summary hb (heartbeat strobes), backed, stale and valid after
one console line, after two lines, and after one line followed by 2500 ms of
unserviced time (T-NVM-WRITER-ALIVE is 2000 ms).
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as gate  # noqa: E402

cfg = root / "configs/endstation_ax7101_1x1_tdm8.yaml"
head = gate.FIRMWARE.read_text()


def at(rev):
    return subprocess.run(["git", "-C", str(root), "show",
                           f"{rev}:sw/firmware/milan_baremetal/milan_baremetal.c"],
                          check=True, capture_output=True, text=True).stdout


STUB = "\nvoid command_dispatch_hook(void);\nvoid command_dispatch_hook(void)\n{\n}\n"
HOOK = "void command_dispatch_hook(void)\n{\n\tnvm_heartbeat_tick();\n}"
assert head.count(HOOK) == 1
FIRMWARES = {
    "head": head,
    "head-empty-hook": head.replace(HOOK, "void command_dispatch_hook(void)\n{\n}"),
    "round1-792a57b0": at("792a57b092efaee8920f344faacb7675c8e163bd") + STUB,
    "base-8bc97021": at("8bc97021f28fb7f729418d3a00851c84ea0b50fd") + STUB,
}
SHAPE = ("\treturn count == NVM_N_REC && bytes == NVM_AREA_RAW &&",
         "\treturn 0 && count == NVM_N_REC && bytes == NVM_AREA_RAW &&")
CSRID = ("\tif (id != MILAN_ID_MAGIC) {", "\tif (1) {")
PLANTS = {"none": None, "shape-mismatch": SHAPE, "csr-id-mismatch": CSRID}
LINES = {"empty-line": "", "milan_status": "milan_status"}
rows = []
for fw_name, text in FIRMWARES.items():
    for plant_name, plant in PLANTS.items():
        t = text
        if plant:
            assert t.count(plant[0]) == 1, (fw_name, plant_name)
            t = t.replace(plant[0], plant[1])
        bench = gate.make_bench(cfg, work / f"{fw_name}-{plant_name}", t)
        for line_name, line in LINES.items():
            out, s, _ = gate.run(bench, "--boot", "--uart", line, "--idle-ms", "0")
            _, s2, _ = gate.run(bench, "--boot", "--uart", line, "--uart", line)
            _, s3, _ = gate.run(bench, "--boot", "--uart", line, "--idle-ms", "2500")
            disabled = ("persistence disabled" in out) or ("identity mismatch" in out)
            print(f"fw={fw_name:16s} plant={plant_name:15s} line={line_name:12s} "
                  f"disabled_msg={int(disabled)} hb={s.get('hb')} backed={s.get('backed')} "
                  f"stale={s.get('stale')} valid={s.get('valid')} | after 2 lines: "
                  f"hb={s2.get('hb')} backed={s2.get('backed')} | +2500 ms: backed={s3.get('backed')} "
                  f"stale={s3.get('stale')} losses={s3.get('losses')}", flush=True)
