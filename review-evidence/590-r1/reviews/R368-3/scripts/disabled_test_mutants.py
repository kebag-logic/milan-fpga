#!/usr/bin/env python3
"""R368-3 probe: can the committed disabled-writer grade fail for the defects it claims?

Usage: python3 -B disabled_test_mutants.py <repo-root> <work-dir>
Runs sw/firmware/nvm_hosttest/test_disabled_writer.grade() unchanged on the
AX7101 1x1 shape against firmware variants:
  head                      : expect no finding
  round2-c64f8cd8           : the actual unguarded round-2 firmware (+ marker
                              declaration so it links with the head host)
  guard-in-hook-only        : guard moved from nvm_heartbeat_tick into the
                              dispatch hook, so Milan commands that tick
                              directly (milan_nvm wipe) are unguarded
  admit-before-shape        : nvm_started = 1 before the shape check
  admit-in-init             : nvm_started = 1 at the top of milan_init
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402
import test_disabled_writer as dw  # noqa: E402

cfg = root / "configs/endstation_ax7101_1x1_tdm8.yaml"
head = nvm.FIRMWARE.read_text()
GUARD = "\tif (!nvm_started)\n\t\treturn;\n"
HOOK = "void command_dispatch_hook(void)\n{\n\tnvm_heartbeat_tick();\n}"
SHAPE = "\tif (!nvm_shape_consistent()) {"
ADMIT = "\tnvm_started = 1;\n"
INIT = "\tuint32_t id = milan_read(MILAN_ID);\n"
for a in (GUARD, HOOK, SHAPE, ADMIT, INIT):
    assert head.count(a) == 1, a
r2 = subprocess.run(["git", "-C", str(root), "show",
                     "c64f8cd896a4462bd42c4b90b32861ac7fd35176:sw/firmware/milan_baremetal/milan_baremetal.c"],
                    check=True, capture_output=True, text=True).stdout
variants = {
    "head": head,
    "round2-c64f8cd8": r2,
    "guard-in-hook-only": head.replace(GUARD, "").replace(
        HOOK, "void command_dispatch_hook(void)\n{\n\tif (!nvm_started)\n\t\treturn;\n\tnvm_heartbeat_tick();\n}"),
    "admit-before-shape": head.replace(ADMIT, "").replace(SHAPE, ADMIT + SHAPE),
    "admit-in-init": head.replace(ADMIT, "").replace(INIT, INIT + ADMIT),
}
for name, text in variants.items():
    try:
        got = dw.grade(cfg, work / name, text)
    except Exception as exc:  # noqa: BLE001
        print(f"variant={name}: ERROR {exc}", flush=True)
        continue
    states = sorted({s for s in ("shape", "identity") if any(s in f for f in got)})
    print(f"variant={name}: findings={len(got)} states_failed={states}", flush=True)
    for f in got[:4]:
        print("   ", f)
