#!/usr/bin/env python3
"""Probe distinct CRC-clean refusals during a transient boot read fault."""
import argparse
import dataclasses
import json
import os
import shutil
from pathlib import Path
import struct
import sys
import zlib

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
a = ap.parse_args()
repo = a.repo.resolve()
packet = Path(__file__).resolve().parent
work = packet / "scratch" / "refusal-digest"
work.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(packet / "scratch")
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t

# Test adapter only: an address/read fault returns two distinct containers,
# both CRC-clean, each naming a foreign entity. No product source is changed.
text = t.HARNESS.read_text()
old = """else if (rf.mode == RF_OTHER)
		memcpy(flash_view + rf.slot, nvm_host_flash + rf.other, 0x10000u);"""
new = r"""else if (rf.mode == RF_OTHER) {
        uint32_t length = 0, crc = 0xffffffffu;
        uint8_t *v = flash_view + rf.slot;
        memcpy(v, nvm_host_flash + rf.slot, 0x10000u);
        for (unsigned int j = 0; j < 4; ++j)
            length |= (uint32_t)v[16 + j] << (8 * j);
        if (length < 44 || length > 65536) exit(2);
        v[20] ^= (uint8_t)(1 + ((k - rf.skip) % 2));
        for (uint32_t j = 0; j < length - 4; ++j) {
            crc ^= v[j];
            for (unsigned int b = 0; b < 8; ++b)
                crc = (crc >> 1) ^ ((crc & 1) ? 0xedb88320u : 0);
        }
        crc ^= 0xffffffffu;
        for (unsigned int j = 0; j < 4; ++j)
            v[length - 4 + j] = (uint8_t)(crc >> (8 * j));
        printf("PROBE distinct foreign read %u entity-low=%u length=%u\n",
               k, (unsigned int)v[20], length);
    }"""
assert text.count(old) == 1
adapter = work / "nvm_host_distinct.c"
adapter.write_text(text.replace(old, new))
shutil.copytree(t.HARNESS.parent / "stubs", work / "stubs", dirs_exist_ok=True)
t.HARNESS = adapter
fw = t.FIRMWARE.read_text()
for name in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    shape_work = work / name
    shape_work.mkdir(exist_ok=True)
    bench = t.make_bench(repo / "configs" / (name + ".yaml"), shape_work, fw)
    fr = t.fault_run(bench)
    image = fr.containers[(0x5a5a5, False)]
    length = struct.unpack_from("<I", image, 16)[0]
    views = []
    for flip in (1, 2):
        v = bytearray(image[:length])
        v[20] ^= flip
        v[-4:] = struct.pack("<I", zlib.crc32(v[:-4]))
        views.append(bytes(v))
    print(json.dumps({"shape": name, "distinct": views[0] != views[1],
                      "verdicts": [t.VERDICT_NAME[bench.verdict(v)] for v in views],
                      "whole_crc32": [hex(zlib.crc32(v)) for v in views],
                      "prefix_crc32": [hex(zlib.crc32(v[:-4])) for v in views]}))
    for slot, skip in (("a", 1), ("b", 3)):
        a_bytes, b_bytes = (image, b"\xff" * t.SLOT) if slot == "a" else (b"\xff" * t.SLOT, image)
        slot_a, slot_b = shape_work / "a.bin", shape_work / "b.bin"
        slot_a.write_bytes(a_bytes); slot_b.write_bytes(b_bytes)
        out_a, out_b = shape_work / "out_a.bin", shape_work / "out_b.bin"
        clean_out, clean_state, _ = t.run(bench, "--slot-a", slot_a.name, "--slot-b", slot_b.name,
            "--boot", "--change", f"{fr.off}:{fr.changes[0].hex()}", "--idle-ms", "1500",
            "--dump-slot-a", out_a.name, "--dump-slot-b", out_b.name)
        clean_ddr = shape_work / "clean_reboot.bin"
        t.run(bench, "--slot-a", out_a.name, "--slot-b", out_b.name,
              "--boot", "--dump-ddr", clean_ddr.name)
        clean_got, clean_lost = t.restored(bench, clean_ddr, fr.want[1], fr.key)
        assert clean_state.get("acks") == 1 and clean_got == fr.want[1][fr.key] and clean_lost == 0
        print(f"CLEAN CONTROL {name} slot={slot}: commit acknowledged; change and all saved records survive")
        out, state, boot = t.run(bench, "--slot-a", slot_a.name, "--slot-b", slot_b.name,
            "--read-other", f"{slot}:{skip}:2", "--boot",
            "--change", f"{fr.off}:{fr.changes[0].hex()}", "--idle-ms", "1500",
            "--dump-slot-a", out_a.name, "--dump-slot-b", out_b.name)
        print(f"CASE {name} slot={slot}")
        print(out)
        ddr = shape_work / "reboot.bin"
        reboot, state2, _ = t.run(bench, "--slot-a", out_a.name, "--slot-b", out_b.name,
                                  "--boot", "--dump-ddr", ddr.name)
        got, lost = t.restored(bench, ddr, fr.want[1], fr.key)
        print(reboot)
        print(json.dumps({"shape":name,"slot":slot,"commit_acks":state.get("acks"),
                          "held":"the writer is HELD until reset" in out,
                          "changed_record_survived":got == fr.want[1][fr.key],
                          "other_records_lost":lost}))
        assert state.get("acks") == 1 and "the writer is HELD until reset" not in out
        assert lost > 0 if slot == "a" else got != fr.want[1][fr.key]
print("REPRODUCED: all four faulty cases lose acknowledged state or other saved records; four clean controls preserve both")
