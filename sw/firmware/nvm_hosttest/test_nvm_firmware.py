#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: the bare-metal saved-state writer, graded on a host model per shape.

WHY THIS EXISTS. Design page section 6.3 owes "a pinned golden image per
shape, byte for byte, produced by the firmware encoder and reproduced by the
fabric decoder, plus one refused case per verdict code". The writer lives in
`sw/firmware/milan_baremetal/milan_baremetal.c`, a translation unit the board
runs and no gate could execute, so every claim about it was going to be text
until it had a host. This file gives it one: `nvm_host.c` and the stub
headers beside it stand in for the LiteX-generated headers, the Milan CSR
window, the QSPI mapping, the LiteSPI command master and the clock, and the
firmware is compiled AS SHIPPED (only its two RISC-V fences are blanked,
because a host assembler has no `fence`) and run through its boot, its idle
hook and its console command.

WHAT IT GRADES, per shipped shape, all on bytes:

  1. a blank board stages an all-erased container that equals
     `nvm_klj2.klj2_assemble` of every record erased, byte for byte, and the
     backend is told the base, the length and the channel-map tables;
  2. `milan_nvm commit` from that state promotes the container into slot A,
     acknowledged once, page-aligned, and the slot decodes VD_OK;
  3. a golden image the Python encoder wrote into slot B is chosen, copied
     into the window byte for byte, and after one record changes the
     container the firmware writes into slot A equals the Python encoder's
     for the same records at the next sequence -- the two encoders agree,
     and the Python decoder reads the changed payload back;
  4. the debounce holds the commit for its window and no longer;
  5. the A/B rule: the newer accepted slot wins, a torn newer slot falls back
     to the older, and two torn slots boot blank with the failure named;
  6. VERDICT PARITY: for every section 6.2 refusal and the erased-record
     rule's faces, the verdict the firmware prints for a slot equals the
     verdict `klj2_decode` returns for the same bytes;
  7. a failed erase, a failed program and a failed read-back each publish
     their transaction verdict and withhold the acknowledgement, and the
     commit deadline then revokes the claim;
  8. the heartbeat is serviced through a datasheet-worst-case erase, at most
     500 ms apart (section 9.4's normative requirement on the writer);
  9. an idle board stays backed and never stale;
 10. `milan_nvm wipe` erases both slots;
 11. an open record beside an unaligned closed predecessor keeps its staged
     bytes while the predecessor's change commits byte-identically;
 12. rejected shape/identity startup never heartbeats under console input;
 13. a boot read fault leaves the authority unknown (#671): every fault
     window starting within the boot's read bound, one read long to one past
     the per-loop bound, and the whole boot (`read_fault_cases.fault_cases`,
     on the cold boot and on a writer restart without a fabric reset,
     `writer_restart.py`), over a header, sequence or record-area byte, the
     blank or older slot's, an entity or record-area byte under a CRC closed
     over the faulty bytes, an all-0xFF read or the other slot's container,
     one slot valid and the other blank or both valid, both ways round, is
     followed by a change, its commit and a clean reboot. The boot line
     names each slot as its bytes read or UNREAD and offers the newer slot it
     accepts, the window is that slot's container byte for byte (a restart
     leaves it as it was), and every saved record and the change survive, or
     the writer was HELD, persisted nothing and named each unread slot and
     why; the reads opened and the hold are the reference model's
     (`read_fault_cases.expect`);
 14. a cleanly read but refused slot names no generation: with no slot
     accepted, the first commit is at sequence 1.

NEGATIVE CONTROLS. `--self-test` plants nineteen writer defects into a copy
of the firmware, one at a time, and requires the suite to redden on each:
the ascending-id check removed, the heartbeat dropped from the erase poll
loop, the read-back verify skipped, the erased-record rule accepting a header
alone, a word copy crossing into an open neighbour, and fourteen #671
defects, each planted into the first shape and both product shapes and
caught there by its own named finding (`read_fault_cases.READ_FAULT_MUTATIONS`
says what each is). A control that stays green is reported as the finding
it is.

Usage:
    sw/firmware/nvm_hosttest/test_nvm_firmware.py            # every shipped shape
    sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
    sw/firmware/nvm_hosttest/test_nvm_firmware.py --config configs/endstation_ax7101_8x8.yaml
    sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4

Exit 0 = every check passed (and every control reddened), 1 = a finding,
2 = the harness could not be built or run.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import threading
import zlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw/litex"))

from nvm_contract import (                                    # noqa: E402
    KLJ2_HDR, KLJ2_TRAILER, REC_HDR, VD_BLANK, VD_CRC, VD_ERASE, VD_OK,
    VD_PROGRAM, VD_REC, VD_VERIFY, VERDICT_NAME, Donor, Ident, Shape)
from nvm_klj2 import (crc16_ccitt, erased_record, frame_record,  # noqa: E402
                      klj2_assemble, klj2_decode, payload_bytes, rid_of_key)
from nvm_shape import (binding_base, build, firmware_constants,  # noqa: E402
                       inventory, layout_version)
from check_nvm_record_space import expected_payloads          # noqa: E402
from flash_map import literal                                  # noqa: E402
from boot_policy import fabric_constants                       # noqa: E402
from read_fault_cases import (BOTH_VALID_SEQS, FAULT_SEQS, HELD_LINE,  # noqa: E402
                              PRODUCT_SHAPES, READ_FAULT_MUTATIONS, RETIRE_CAUSES,
                              UNREAD_RE, FaultCase, expect, fault_cases, hold_findings,
                              line_findings, read_findings, restart_findings)
from writer_restart import host_restart                        # noqa: E402

FIRMWARE = ROOT / "sw/firmware/milan_baremetal/milan_baremetal.c"
HARNESS = HERE / "nvm_host.c"
STUBS = HERE / "stubs"
#: the map, read out of the SoC source the way every other consumer reads it
RESERVED = literal("FLASHBOOT_RESERVED")
LAYOUT = literal("FLASHBOOT_LAYOUT")
JOURNAL = RESERVED["journal"]["offset"]
SLOT = RESERVED["journal"]["size"] // 2
AEM_OFFSET = LAYOUT["aem"]["offset"]
#: the LIVE window's band inside the host's window array: the same place
#: milan_soc.py puts it, the erase block below the response buffer
IMAGE_OFF = 0x100000 - 0x1000 - 0x10000
#: the writer's PRIVATE STAGE, one erase block below the live window
#: (snapshot-ownership section 17), derived here the same way
STAGE_OFF = IMAGE_OFF - 0x10000
AEM_STUB = b"AEMI"
FENCE_RE = re.compile(r'__asm__ volatile\("fence[^"]*" ::: "memory"\);')
BOOT_RE = re.compile(
    r"Milan NVM: slot A (\S+) seq (\d+), slot B (\S+) seq (\d+); "
    r"offered (\S) seq (\d+) \((\S+)\)")
SUMMARY_RE = re.compile(r"^HOST (.*)$", re.M)

#: (label, the text that must occur exactly once, its replacement) - each is
#: one writer defect the suite must catch
MUTATIONS = {
    "edge_cross": (
        "if ((i & 3u) == 0 && next - i >= 4u &&",
        "if ((i & 3u) == 0 && next - i >= 1u &&"),
    "no_ascending_check": (
        "\t\t\tif (!rec.ok || (int)rec.id <= last)\n",
        "\t\t\tif (!rec.ok)\n"),
    "no_heartbeat_in_wait": (
        "\t\t\treturn 1;\n\t\tnvm_heartbeat_tick();\n",
        "\t\t\treturn 1;\n"),
    "verify_skipped": (
        "\t\tvd = VD_VERIFY;\n",
        "\t\tvd = VD_OK;\n"),
    "erased_header_only": (
        "\t\t\tif (!nvm_all_erased(img + pos + REC_HDR, rec.plen))\n"
        "\t\t\t\treturn VD_REC;\n",
        ""),
}


@dataclass
class Bench:
    """One shape's compiled harness and the Python side of its image."""

    cfg: Path
    shape: Shape
    donor: Donor
    ident: Ident
    binary: Path
    work: Path
    frames: dict[int, bytes]
    expect: dict
    #: the threads check 13 walks its cases on
    jobs: int = 1

    @property
    def img_len(self) -> int:
        """The container length this shape's record set implies."""
        return len(self.assemble(self.frames, 0))

    def assemble(self, frames: dict[int, bytes], seq: int) -> bytes:
        """The Python encoder's container for `frames` at sequence `seq`."""
        ident = Ident(seq=seq, entity_id=self.ident.entity_id,
                      model_id=self.ident.model_id)
        return klj2_assemble(frames, self.donor, ident)[0]

    def offsets(self) -> dict[int, int]:
        """record_id -> byte offset inside the record area."""
        return klj2_assemble(self.frames, self.donor, self.ident)[1]

    def verdict(self, blob: bytes) -> int:
        """What `klj2_decode` says about `blob` for this shape."""
        return klj2_decode(blob, self.donor, self.ident, self.expect)[0]

    def erased_frames(self) -> dict[int, bytes]:
        """Every record of the shape erased."""
        return {rid: erased_record(len(fr) - REC_HDR)
                for rid, fr in self.frames.items()}


def constants_header(shape: Shape, donor: Donor,
                     boot_constants: dict[str, int]) -> str:
    """The stub `generated/soc.h`: the constants milan_soc.py publishes, from
    the SAME derivation, plus the host addresses the bases resolve to."""
    lines = ["#pragma once", "#include <nvm_host.h>",
             "#define CONFIG_CLOCK_FREQUENCY 100000000"]
    values = {
        **boot_constants,
        "MILAN_AEM_FLASH_OFFSET": AEM_OFFSET,
        "MILAN_AEM_IMAGE_BYTES": len(AEM_STUB),
        "MILAN_AEM_IMAGE_CRC32": zlib.crc32(AEM_STUB) & 0xFFFF_FFFF,
        "MILAN_FLASH_JOURNAL_OFFSET": JOURNAL,
        "MILAN_FLASH_JOURNAL_SIZE": RESERVED["journal"]["size"],
        "MILAN_NVM_IMAGE_MAX": 0x10000,
    }
    values.update(firmware_constants(shape, donor))
    lines += [f"#define {n} {v}u" for n, v in values.items()]
    lines.append("#define MILAN_AEM_DESC_BASE ((uintptr_t)nvm_host_ddr)")
    # The contract-3 generator (snapshot-ownership section 14):
    # MILAN_NVM_IMAGE_BASE is withdrawn and the live window, the private
    # stage and the contract number are published instead.
    lines.append(f"#define MILAN_NVM_LIVE_BASE ((uintptr_t)nvm_host_ddr + 0x{IMAGE_OFF:x}u)")
    lines.append(f"#define MILAN_NVM_STAGE_BASE ((uintptr_t)nvm_host_ddr + 0x{STAGE_OFF:x}u)")
    lines.append("#define MILAN_NVM_CONTRACT 3u")
    return "\n".join(lines) + "\n"


def compile_bench(work: Path, firmware_text: str, header: str) -> Path:
    """Build the harness and the (fence-blanked) firmware, with the writer's
    CPU-only reset appended (`writer_restart.host_restart`), into `work`."""
    (work / "generated").mkdir(parents=True, exist_ok=True)
    (work / "generated/soc.h").write_text(header)
    fw = work / "milan_baremetal.c"
    fw.write_text(FENCE_RE.sub("(void)0;", firmware_text) + host_restart(firmware_text))
    common = ["gcc", "-std=gnu11", "-O1", "-g", "-Wall", "-Wextra", "-Werror",
              f"-I{work}", f"-I{STUBS}"]
    host_defs = [f"-DNVM_HOST_JOURNAL_OFFSET=0x{JOURNAL:x}u",
                 f"-DNVM_HOST_AEM_OFFSET=0x{AEM_OFFSET:x}u",
                 f"-DNVM_HOST_IMAGE_OFF=0x{IMAGE_OFF:x}u"]
    steps = [
        common + host_defs + ["-c", str(HARNESS), "-o", str(work / "host.o")],
        common + ["-Wno-format", "-c", str(fw), "-o", str(work / "fw.o")],
        ["gcc", str(work / "host.o"), str(work / "fw.o"), "-o", str(work / "fw")],
    ]
    for cmd in steps:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"host build failed: {' '.join(cmd)}\n{r.stderr}")
    return work / "fw"


def make_bench(cfg: Path, work: Path, firmware_text: str) -> Bench:
    """Run the builder for `cfg`, derive its shape and compile its harness."""
    names, dc, spi, spo = build(cfg, work / "builder")
    shape = Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    donor = Donor(base=binding_base(), layout=layout_version())
    generated = work / "builder" / cfg.stem
    overlay = json.loads((generated / "aem_overlay.json").read_text())
    lwsrp = json.loads((generated / "lwsrp_table.json").read_text())
    ident = Ident(seq=0, entity_id=int(overlay["adp"]["entity_id"], 16),
                  model_id=int(overlay["entity"]["entity_model_id"], 16))
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), donor.layout)
              for g, i, r, p, _b in inventory(shape, donor.base) if r is not None}
    header = constants_header(shape, donor, fabric_constants(overlay, lwsrp))
    binary = compile_bench(work, firmware_text, header)
    return Bench(cfg=cfg, shape=shape, donor=donor, ident=ident, binary=binary,
                 work=work, frames=frames, expect=expected_payloads(shape))


def run(bench: Bench, *args: str) -> tuple[str, dict[str, int], re.Match | None]:
    """One harness run: its transcript, the HOST summary and the boot line."""
    r = subprocess.run([str(bench.binary), *args], capture_output=True, text=True,
                       cwd=bench.work, timeout=600)
    if r.returncode:
        raise SystemExit(f"harness failed ({r.returncode}): {' '.join(args)}\n"
                         f"{r.stdout}\n{r.stderr}")
    return r.stdout, host_state(r.stdout), BOOT_RE.search(r.stdout)


def host_state(text: str) -> dict[str, int]:
    """The last HOST summary in a transcript, field by field."""
    lines = [x for x in SUMMARY_RE.findall(text) if x.startswith("hb=")]
    return {k: int(v) for k, v in (kv.split("=") for kv in lines[-1].split())} if lines else {}


def slot_file(bench: Bench, name: str, blob: bytes) -> str:
    """Write `blob` as a slot image the harness loads."""
    path = bench.work / name
    path.write_bytes(blob)
    return str(path)


def reseal(blob: bytes) -> bytes:
    """Recompute the CRC-32 trailer after an edit above it."""
    return blob[:-4] + struct.pack("<I", zlib.crc32(blob[:-4]) & 0xFFFF_FFFF)


def _check(findings: list[str], ok: bool, what: str) -> None:
    if not ok:
        findings.append(what)


def grade_blank_boot(bench: Bench) -> list[str]:
    """Checks 1 and 2: the blank board and its first commit."""
    f = []
    ddr = bench.work / "ddr.bin"
    out, s, boot = run(bench, "--boot", "--dump-ddr", str(ddr))
    _check(f, boot is not None and boot.group(1) == "VD_BLANK" and
           boot.group(3) == "VD_BLANK" and boot.group(5) == "-",
           f"blank boot did not report two blank slots and no offer: {boot and boot.group(0)}")
    _check(f, s.get("valid") == 1 and s.get("verdict") == VD_BLANK and
           s.get("blank") == 1 and s.get("fail") == 0 and s.get("done") == 1 and
           s.get("backed") == 1 and s.get("base_ok") == 1,
           f"blank boot state: {s}")
    _check(f, s.get("img_len") == bench.img_len - KLJ2_HDR - KLJ2_TRAILER,
           f"backend image length {s.get('img_len')} != record area")
    staged = ddr.read_bytes()[:bench.img_len]
    _check(f, staged == bench.assemble(bench.erased_frames(), 0),
           "the staged all-erased container differs from the Python encoder's")
    slot_a = bench.work / "a.bin"
    out, s, _ = run(bench, "--boot", "--uart", "milan_nvm commit",
                    "--dump-slot-a", str(slot_a))
    pages = -(-bench.img_len // 256)
    _check(f, s.get("acks") == 1 and s.get("starts") == 1 and s.get("erases") == 1
           and s.get("programs") == pages and s.get("pagewrap") == 0 and
           s.get("seq") == 1 and s.get("verdict") == VD_OK and s.get("dirty") == 0,
           f"first commit state: {s}")
    got = slot_a.read_bytes()[:bench.img_len]
    _check(f, got == bench.assemble(bench.erased_frames(), 1),
           "the committed all-erased container differs from the Python encoder's")
    _check(f, bench.verdict(got) == VD_OK, "the committed container does not decode")
    _check(f, "acknowledged" in out, "the commit did not report itself acknowledged")
    return f


def grade_restore_change_commit(bench: Bench) -> list[str]:
    """Checks 3 and 4: the golden restore, one change, the debounce, the
    encoder agreement and the decoder reading the change back."""
    f = []
    golden = bench.assemble(bench.frames, 5)
    rid = max(bench.frames)                          # the last name record
    new_payload = bytes((0x40 + j) & 0xFF for j in range(len(bench.frames[rid]) - REC_HDR))
    new_frame = frame_record(rid, new_payload, bench.donor.layout)
    off = KLJ2_HDR + bench.offsets()[rid]
    ddr, a1, a2 = (bench.work / n for n in ("ddr3.bin", "a3_early.bin", "a3.bin"))
    out, s, boot = run(bench, "--slot-b", slot_file(bench, "b3.bin", golden),
                       "--boot", "--dump-ddr", str(ddr),
                       "--change", f"{off}:{new_frame.hex()}",
                       "--idle-ms", "600", "--dump-slot-a", str(a1),
                       "--idle-ms", "1200", "--dump-slot-a", str(a2))
    _check(f, boot is not None and boot.group(5) == "B" and boot.group(6) == "5"
           and boot.group(7) == "VD_OK", f"golden slot B not offered: {boot and boot.group(0)}")
    _check(f, ddr.read_bytes()[:bench.img_len] == golden,
           "the golden container was not copied into the window byte for byte")
    _check(f, a1.read_bytes()[:KLJ2_HDR] == b"\xff" * KLJ2_HDR,
           "a commit landed inside the debounce window")
    changed = dict(bench.frames)
    changed[rid] = new_frame
    want = bench.assemble(changed, 6)
    got = a2.read_bytes()[:bench.img_len]
    _check(f, got == want,
           "the container the firmware committed after one change differs "
           "from the Python encoder's for the same records at sequence 6")
    vd, applied = klj2_decode(got, bench.donor, bench.ident, bench.expect)
    key = ("NAME", rid - 0x80)
    _check(f, vd == VD_OK and applied.get(key) == new_payload,
           f"the changed record does not read back: {VERDICT_NAME[vd]}")
    _check(f, s.get("acks") == 1 and s.get("seq") == 6 and s.get("dirty") == 0
           and s.get("stale") == 0 and s.get("backed") == 1,
           f"post-commit state: {s}")
    return f


def grade_ab_rule(bench: Bench) -> list[str]:
    """Check 5: newer wins, torn newer falls back, two torn boot blank."""
    f = []
    older = bench.assemble(bench.frames, 9)
    newer = bench.assemble(bench.frames, 10)
    torn = newer[:KLJ2_HDR + 3] + bytes([newer[KLJ2_HDR + 3] ^ 0x80]) + newer[KLJ2_HDR + 4:]
    a, b = slot_file(bench, "a5.bin", older), slot_file(bench, "b5.bin", newer)
    _, _, boot = run(bench, "--slot-a", a, "--slot-b", b, "--boot")
    _check(f, boot is not None and boot.group(5) == "B" and boot.group(6) == "10",
           f"the newer slot was not chosen: {boot and boot.group(0)}")
    bt = slot_file(bench, "b5t.bin", torn)
    _, _, boot = run(bench, "--slot-a", a, "--slot-b", bt, "--boot")
    _check(f, boot is not None and boot.group(5) == "A" and boot.group(6) == "9"
           and boot.group(3) == "VD_CRC",
           f"a torn newer slot did not fall back to the older: {boot and boot.group(0)}")
    at = slot_file(bench, "a5t.bin", older[:-1] + bytes([older[-1] ^ 1]))
    _, s, boot = run(bench, "--slot-a", at, "--slot-b", bt, "--boot")
    _check(f, boot is not None and boot.group(5) == "-" and boot.group(7) == "VD_CRC"
           and s.get("blank") == 1 and s.get("fail") == 0 and s.get("verdict") == VD_CRC,
           f"two torn slots did not boot blank naming the failure: {boot and boot.group(0)} {s}")
    return f


def parity_cases(bench: Bench) -> list[tuple[str, bytes]]:
    """Every refusal of section 6.2 and the erased-record rule, as bytes."""
    full = bench.assemble(bench.frames, 3)
    rids = sorted(bench.frames)
    first, last = rids[0], rids[-1]
    offs = bench.offsets()
    plen_last = len(bench.frames[last]) - REC_HDR

    def patched(blob: bytes, at: int, new: bytes, seal: bool = True) -> bytes:
        """`blob` with `new` written at `at`, its trailer recomputed unless
        the corruption under test is the trailer itself."""
        out = blob[:at] + new + blob[at + len(new):]
        return reseal(out) if seal else out

    def with_frames(frames: dict[int, bytes], nrec: int | None = None) -> bytes:
        """The container for `frames`, its N_REC word overridden when asked."""
        blob = bench.assemble(frames, 3)
        if nrec is not None:
            blob = patched(blob, 12, struct.pack("<I", nrec))
        return blob

    def id_rewritten(rid: int, new_rid: int) -> dict[int, bytes]:
        """The golden frames with record `rid` re-framed under `new_rid`, its
        crc16 recomputed so only the id is wrong."""
        fr = bench.frames[rid]
        hdr = fr[:2] + bytes([fr[2], new_rid]) + fr[4:6]
        crc = struct.pack(">H", crc16_ccitt(hdr + fr[REC_HDR:]))
        frames = dict(bench.frames)
        frames[rid] = hdr + crc + fr[REC_HDR:]
        return frames

    erased = bench.erased_frames()
    half = dict(bench.frames)
    for rid in rids[::2]:
        half[rid] = erased[rid]
    torn_erased = dict(bench.frames)
    torn_erased[last] = erased_record(plen_last)[:-1] + b"\x00"
    trunc = dict(bench.frames)
    del trunc[last]
    return [
        ("full image", full),
        ("every record erased", bench.assemble(erased, 3)),
        ("every other record erased", bench.assemble(half, 3)),
        ("bad magic", patched(full, 0, b"KLJ1")),
        ("major version 1", patched(full, 4, struct.pack("<I", 0x0001_0000))),
        ("IMG_LEN 43", patched(full, 16, struct.pack("<I", 43))),
        ("IMG_LEN 65537", patched(full, 16, struct.pack("<I", 65537))),
        ("bad CRC", patched(full, KLJ2_HDR + 1, bytes([full[KLJ2_HDR + 1] ^ 1]), False)),
        ("foreign entity", patched(full, 20, struct.pack("<I", 0xDEAD_0001))),
        ("foreign model", patched(full, 28, struct.pack("<I", 0xDEAD_0002))),
        ("record layout off", patched(full, 36, struct.pack("<I", bench.donor.layout + 1))),
        ("record magic", patched(full, KLJ2_HDR + offs[first], b"\x17\x23")),
        ("unknown record id", with_frames(id_rewritten(last, 0xFE))),
        ("duplicate record id", with_frames(id_rewritten(last, last - 1))),
        ("truncated by one record", with_frames(trunc)),
        ("N_REC one too many", with_frames(bench.frames, len(rids) + 1)),
        ("N_REC one too few", with_frames(bench.frames, len(rids) - 1)),
        ("erased header, live payload", bench.assemble(torn_erased, 3)),
        ("erased span short by one", with_frames({r: erased[r] for r in rids[:-1]})),
    ]


def grade_parity(bench: Bench) -> list[str]:
    """Check 6: the firmware's slot verdict equals klj2_decode's, case by case."""
    f = []
    for n, (label, blob) in enumerate(parity_cases(bench)):
        want = VERDICT_NAME[bench.verdict(blob)]
        _, _, boot = run(bench, "--slot-a", slot_file(bench, f"p{n}.bin", blob), "--boot")
        got = boot.group(1) if boot else "(no boot line)"
        _check(f, got == want, f"parity: {label}: firmware {got}, klj2_decode {want}")
    return f


def grade_failures(bench: Bench) -> list[str]:
    """Check 7: erase, program and read-back failures, each by name.

    The REPORTED verdict is what revokes the claim now, not the 8 s commit
    deadline behind it (SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 12: waiting
    for the deadline advertises durability for up to eight seconds after a
    known failure). With nothing outstanding the loss heals on the next
    heartbeat (section 9.2's clean recovery), so the loss is counted rather
    than sampled; with a change outstanding, `nvm_stale` must still stand,
    because the retry fails the same way.
    """
    f = []
    for mode, code in (("erase", VD_ERASE), ("program", VD_PROGRAM), ("verify", VD_VERIFY)):
        out, s, _ = run(bench, "--fail", mode, "--boot", "--uart", "milan_nvm commit",
                        "--idle-ms", "9000")
        _check(f, s.get("acks") == 0 and s.get("starts") == 1 and s.get("verdict") == code,
               f"a failed {mode} was not published as {VERDICT_NAME[code]} unacknowledged: {s}")
        _check(f, f"FAILED: {VERDICT_NAME[code]}" in out,
               f"a failed {mode} was not named on the console")
        _check(f, s.get("losses", 0) >= 1,
               f"the reported verdict did not revoke the claim after a failed {mode}: {s}")
    _, s, _ = run(bench, "--fail", "erase", "--boot", "--dirty", "--idle-ms", "12000")
    _check(f, s.get("acks") == 0 and s.get("starts") >= 1 and s.get("dirty") == 1
           and s.get("stale") == 1 and s.get("losses", 0) >= 1,
           f"a change the media cannot take did not stay dirty and stale: {s}")
    return f


def grade_liveness(bench: Bench) -> list[str]:
    """Checks 8, 9 and 10: the heartbeat through an erase, an idle board, wipe."""
    f = []
    _, s, _ = run(bench, "--erase-ms", "3000", "--boot", "--uart", "milan_nvm commit")
    _check(f, s.get("acks") == 1 and s.get("hb") >= 6 and s.get("max_hb_gap_ms") <= 500,
           f"the heartbeat was not serviced through a 3 s erase: {s}")
    _, s, _ = run(bench, "--boot", "--idle-ms", "5000")
    _check(f, s.get("backed") == 1 and s.get("stale") == 0 and s.get("hb") >= 10,
           f"an idle board did not stay backed: {s}")
    a = bench.work / "wipe_a.bin"
    out, s, _ = run(bench, "--boot", "--uart", "milan_nvm commit", "--uart", "milan_nvm wipe",
                    "--uart", "milan_nvm", "--dump-slot-a", str(a))
    _check(f, a.read_bytes() == b"\xff" * SLOT and s.get("erases") == 3,
           "wipe did not erase both slots")
    _check(f, "NVM: slot A VD_BLANK" in out, "the status command did not report the wiped slots")
    return f


def grade_snapshot_contract(bench: Bench) -> list[str]:
    """Checks 11 to 14: the window load, the capture and the retired state.

    The writer sequence of SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 7. What
    this bench can reach is the WRITER's side of it, because the host backend
    model has no device-face producer: the orderings that need one (a grant
    inside a hold, a concurrent record change, an acknowledgement racing a completion)
    are graded against the real RTL and the real donor in
    tb/verilator/nvm_cosim.
    """
    f = []
    # 11. the cold boot loads the window once and the backend accepts it, so
    # every record closes and the pending bit falls
    out, s, _ = run(bench, "--boot")
    _check(f, s.get("reloads") == 1 and s.get("ld_acc") == 1 and
           s.get("ld_pend") == 0 and s.get("rl_ref") == 0 and s.get("unres") == 0,
           f"the cold boot did not load the window exactly once: {s}")
    # 12. a commit arms a capture and the acknowledgement quotes its identity
    out, s, _ = run(bench, "--boot", "--uart", "milan_nvm commit")
    _check(f, s.get("arms") == 1 and s.get("cap_id") == 1 and s.get("acks") == 1
           and s.get("ack_ref") == 0 and s.get("arm_ref") == 0,
           f"the commit did not acknowledge under capture 1: {s}")
    _check(f, "capture 1 acknowledged" in out,
           "the commit did not name the capture it acknowledged")
    # ... and one quoting ANOTHER capture names nothing the backend holds
    _, s, _ = run(bench, "--boot", "--stray-ack", "4242", "--uart", "milan_nvm commit")
    _check(f, s.get("ack_ref") == 0 and s.get("acks") == 1 and s.get("dirty") == 0,
           f"a stray acknowledgement was not refused before the real one: {s}")
    # 13. one refused load: the writer repeats from the re-base and converges
    out, s, _ = run(bench, "--refuse-loads", "1", "--boot", "--uart", "milan_nvm commit")
    _check(f, s.get("reloads") == 2 and s.get("ld_acc") == 1 and
           s.get("acks") == 1 and s.get("unres") == 0,
           f"a refused window load did not converge on the repeat: {s}")
    _check(f, "refused 1 window load(s); accepted at attempt 2" in out,
           "the repeated window load was not named on the console")
    # 14. four refused loads: the terminal row of section 5.3. The writer
    # retires, so nothing is captured, no slot is touched, nvm_backed falls
    # and the pending bit stands
    out, s, _ = run(bench, "--refuse-loads", "4", "--boot", "--uart", "milan_nvm commit",
                    "--idle-ms", "9000", "--uart", "milan_nvm")
    _check(f, s.get("reloads") == 4 and s.get("ld_acc") == 0 and s.get("rl_ref") == 1,
           f"four refused loads did not leave the load unaccepted: {s}")
    _check(f, s.get("arms") == 0 and s.get("acks") == 0 and s.get("erases") == 0
           and s.get("valid") == 0 and s.get("unres") == 1 and s.get("cap_id") == 0,
           f"the terminal state captured, committed or validated something: {s}")
    _check(f, s.get("backed") == 0,
           f"a retired writer kept nvm_backed asserted: {s}")
    _check(f, "refused 4 window loads" in out and "disabled until the next reset" in out,
           "the terminal state was not named on the console")
    _check(f, "unresolved records" in out,
           "the console did not name the records the terminal state leaves open")
    return f


def grade_partial_ownership(bench: Bench) -> list[str]:
    """An open record keeps staged bytes beside an unaligned closed edge."""
    findings = []
    offsets = bench.offsets()
    rids = sorted(bench.frames, key=offsets.get)
    pairs = [(left, right) for left, right in zip(rids, rids[1:])
             if offsets[right] % 4 and offsets[left] + len(bench.frames[left]) == offsets[right]]
    if not pairs:
        return ["partial ownership fixture has no unaligned record boundary"]
    closed, opened = pairs[0]
    golden = bench.assemble(bench.frames, 5)
    closed_frame = bench.frames[closed]
    payload = bytes(byte ^ 0x55 for byte in closed_frame[REC_HDR:])
    changed = frame_record(closed, payload, bench.donor.layout)
    # Poison the open record's header too: crossing even one byte is visible.
    poison = bytes(byte ^ 0xff for byte in bench.frames[opened])
    stage = bench.work / "partial-stage.bin"
    slot = bench.work / "partial-slot.bin"
    _, state, _ = run(bench, "--slot-b", slot_file(bench, "partial-golden.bin", golden),
                      "--boot", "--open-record", str(opened),
                      "--change", f"{KLJ2_HDR + offsets[opened]}:{poison.hex()}",
                      "--change", f"{KLJ2_HDR + offsets[closed]}:{changed.hex()}",
                      "--uart", "milan_nvm commit", "--dump-stage", str(stage),
                      "--dump-slot-a", str(slot))
    kept = dict(bench.frames)
    kept[closed] = changed
    expected = bench.assemble(kept, 6)
    start = KLJ2_HDR + offsets[opened]
    end = start + len(bench.frames[opened])
    _check(findings, stage.read_bytes()[start:end] == golden[start:end],
           "partial ownership: open record changed across unaligned predecessor edge")
    _check(findings, stage.read_bytes()[:bench.img_len] == expected
           and slot.read_bytes()[:bench.img_len] == expected and state.get("acks") == 1,
           "partial ownership: closed change and preserved open record did not commit byte-identically")
    return findings


@dataclass
class FaultRun:
    """Check 13's fixtures on one shape: the containers its slots hold, the
    change made after the faulty boot and after the recovery, and every
    record each clean reboot must restore."""

    containers: dict[tuple[int, bool], bytes]   # (seq, the older one) -> container
    off: int                                    # the changed record in the container
    key: tuple                                  # the changed record, as klj2_decode names it
    changes: tuple[bytes, bytes]
    want: tuple[dict, dict, dict]               # the saved records, then with each change


def fault_run(bench: Bench) -> FaultRun:
    """The newer container is the shape's records; the older one, a sequence
    below it, differs in the last two names, so a boot that falls back to it
    is told apart by more than the record a change rewrites."""
    rid = max(bench.frames)                          # the last name record
    older = dict(bench.frames)
    for r, base in ((rid, 0x11), (rid - 1, 0x67)):
        older[r] = frame_record(r, bytes((base + j) & 0xFF for j in range(len(bench.frames[r]) - REC_HDR)),
                                bench.donor.layout)
    plen = len(bench.frames[rid]) - REC_HDR
    changes = tuple(frame_record(rid, bytes((b + j) & 0xFF for j in range(plen)), bench.donor.layout)
                    for b in (0x40, 0x21))
    saved = klj2_decode(bench.assemble(bench.frames, 1), bench.donor, bench.ident, bench.expect)[1]
    key = ("NAME", rid - 0x80)
    containers = {}
    for seq in FAULT_SEQS + BOTH_VALID_SEQS:
        containers[(seq, False)] = bench.assemble(bench.frames, seq)
        containers[(seq, True)] = bench.assemble(older, (seq - 1) & 0xFFFF_FFFF)
    return FaultRun(containers, KLJ2_HDR + bench.offsets()[rid], key, changes,
                    (saved, {**saved, key: changes[0][REC_HDR:]}, {**saved, key: changes[1][REC_HDR:]}))


def restored(bench: Bench, path: Path, want: dict, key: tuple) -> tuple[bytes | None, int]:
    """The record `key` in the window a boot loaded, and how many of the
    other records in `want` that window does not hold as `want` says."""
    vd, applied = klj2_decode(path.read_bytes()[:bench.img_len], bench.donor,
                              bench.ident, bench.expect)
    if vd != VD_OK:
        return None, len(want) - 1
    return applied.get(key), sum(1 for k, v in want.items() if k != key and applied.get(k) != v)


def boot_findings(bench: Bench, case: FaultCase, boot: re.Match, unread: int,
                  slots: dict[str, bytes], ddr: Path) -> list[str]:
    """What the faulty boot's own line and window must show: each slot as
    its bytes read, or UNREAD; the offer the slots its line accepts make; and
    a window holding that offer's container byte for byte, or the blank
    image when there is none."""
    f = line_findings(case, boot, unread)
    got = boot.group(5)
    image = slots[got][:bench.img_len] if got in slots else \
        bench.assemble(bench.erased_frames(), 0)
    window = ddr.read_bytes()[:bench.img_len]
    if window != image:
        vd = bench.verdict(window)
        f.append(f"{case.name}: the window holds another valid container than the one the boot "
                 f"offered ({got}), at seq {struct.unpack_from('<I', window, 8)[0]:#x}"
                 if vd == VD_OK else
                 f"{case.name}: the window the boot loaded is not the container it judged: it "
                 f"reads {VERDICT_NAME[vd]}")
    return f


def reboot_findings(bench: Bench, fr: FaultRun, name: str, held: bool, w: Path,
                    seen: dict | None = None) -> list[str]:
    """The clean reboot after a faulty boot. Every saved record and the
    change survive it, or the faulty boot held and it restores every saved
    record; a held case then runs on through a change, its commit and
    another clean reboot, which must restore that change and the rest. The
    harness is deterministic, so `seen` keeps each reboot's findings by the
    slots it boots, and a case leaving the same slots is not booted again."""
    key = (held, (w / "rf_a1.bin").read_bytes(), (w / "rf_b1.bin").read_bytes())
    if seen is not None and key in seen:
        return [f"{name}: {x}" for x in seen[key]]
    tail = ("--change", f"{fr.off}:{fr.changes[1].hex()}", "--idle-ms", "1500",
            "--dump-slot-a", str(w / "rf_a2.bin"), "--dump-slot-b", str(w / "rf_b2.bin")) \
        if held else ()
    out, s, boot = run(bench, "--slot-a", str(w / "rf_a1.bin"), "--slot-b", str(w / "rf_b1.bin"),
                       "--boot", "--dump-ddr", str(w / "rf_ddr1.bin"), *tail)
    f = []
    _check(f, boot is not None and HELD_LINE not in out and boot.group(5) != "-",
           f"the clean reboot did not offer a slot: {boot and boot.group(0)}")
    if not held:
        got, lost = restored(bench, w / "rf_ddr1.bin", fr.want[1], fr.key)
        _check(f, got == fr.want[1][fr.key],
               f"the change committed after the faulty boot was lost on the clean reboot: "
               f"it restored {got and got[:4].hex()}, want {fr.want[1][fr.key][:4].hex()}")
        _check(f, lost == 0, f"{lost} other saved record(s) did not survive the faulty "
                             "boot's commit and the clean reboot")
    else:
        got, lost = restored(bench, w / "rf_ddr1.bin", fr.want[0], fr.key)
        _check(f, got == fr.want[0][fr.key] and lost == 0,
               f"the held boot changed the saved state: the clean reboot restored "
               f"{got and got[:4].hex()}, want the saved {fr.want[0][fr.key][:4].hex()}, and "
               f"{lost} other saved record(s) differ")
        _check(f, s.get("acks") == 1, f"the writer did not recover on the clean reboot: {s}")
        run(bench, "--slot-a", str(w / "rf_a2.bin"), "--slot-b", str(w / "rf_b2.bin"),
            "--boot", "--dump-ddr", str(w / "rf_ddr2.bin"))
        got, lost = restored(bench, w / "rf_ddr2.bin", fr.want[2], fr.key)
        _check(f, got == fr.want[2][fr.key],
               "the change committed after the recovery was lost on the clean reboot")
        _check(f, lost == 0, f"{lost} other saved record(s) did not survive the recovery")
    if seen is not None:
        seen[key] = f
    return [f"{name}: {x}" for x in f]


def grade_restart_case(bench: Bench, fr: FaultRun, case: FaultCase, w: Path,
                       tail: tuple[str, ...], seen: dict | None = None) -> list[str]:
    """One check-13 case on a writer restart: a clean cold boot, the fault
    armed for the restart's own reads, the restart with the fabric kept,
    then `tail` (a change, the debounce, the slots dumped) and the clean
    reboot. A re-attach never reloads the window."""
    out, s, _ = run(bench, "--slot-a", str(w / "rf_a.bin"), "--slot-b", str(w / "rf_b.bin"), "--boot",
                    "--idle-ms", "100", "--dump-ddr", str(w / "rf_ddr0.bin"), *case.fault, "--restart",
                    "--dump-ddr", str(w / "rf_ddr_r.bin"), *tail)
    restart = out.split("HOST restarting\n", 1)[1].split("HOST restarted\n", 1)[0]
    f, held = restart_findings(case, restart, BOOT_RE.search(restart), host_state(restart), s)
    if (w / "rf_ddr_r.bin").read_bytes() != (w / "rf_ddr0.bin").read_bytes():
        f.append(f"{case.name}: the writer restart reloaded the window it re-attached to")
    return f + reboot_findings(bench, fr, case.name, held, w, seen)


def grade_fault_case(bench: Bench, fr: FaultRun, case: FaultCase, w: Path,
                     seen: dict | None = None) -> list[str]:
    """One check-13 case, its files in `w`: the faulty boot (or restart), a
    real change, the debounce commit, then the clean reboot (`seen`, as
    `reboot_findings` keeps it)."""
    newer = fr.containers[(case.seq, False)]
    other = fr.containers[(case.seq, True)] if case.older else b"\xff" * SLOT
    slots = {case.valid.upper(): newer, case.other.upper(): other}
    (w / "rf_a.bin").write_bytes(slots["A"])
    (w / "rf_b.bin").write_bytes(slots["B"])
    # a restart the model holds idles past T-NVM-WRITER-ALIVE, so its claim lapses
    tail = ("--change", f"{fr.off}:{fr.changes[0].hex()}",
            "--idle-ms", "3000" if case.restart and expect(case).unread else "1500",
            "--dump-slot-a", str(w / "rf_a1.bin"), "--dump-slot-b", str(w / "rf_b1.bin"))
    if case.restart:
        return grade_restart_case(bench, fr, case, w, tail, seen)
    out, s, boot = run(bench, "--slot-a", str(w / "rf_a.bin"), "--slot-b", str(w / "rf_b.bin"),
                       *case.fault, "--boot", "--dump-ddr", str(w / "rf_ddr0.bin"), *tail)
    name = case.name
    f = read_findings(case, s.get("boot_reads", 0))
    if boot is None:
        return f + [f"{name}: the faulty boot printed no boot line"]
    tally = UNREAD_RE.search(out)
    unread = int(tally.group(2)) if tally else 0
    held = HELD_LINE in out
    f += boot_findings(bench, case, boot, unread, slots, w / "rf_ddr0.bin") + hold_findings(case, held, unread, out)
    if held:
        _check(f, s.get("erases") == 0 and s.get("programs") == 0 and
               s.get("starts") == 0 and s.get("acks") == 0 and s.get("backed") == 0
               and s.get("dirty") == 1 and s.get("hb") == 0,
               f"{name}: the held writer persisted something or claimed backing: {s}")
        _check(f, unread != 0, f"{name}: the boot line did not name the unread slot")
    else:
        _check(f, s.get("acks") == 1 and s.get("dirty") == 0,
               f"{name}: the change was neither committed nor refused: {s}")
    return f + reboot_findings(bench, fr, name, held, w, seen)


def grade_read_faults(bench: Bench, until: str = "") -> list[str]:
    """Check 13 (#671): a boot read fault leaves the authority unknown.

    The shipping writer reads a slot through the memory-mapped window, which
    always returns bytes, so a media fault can only return wrong ones. Each
    case (read_fault_cases.fault_cases) boots with a valid container in one
    slot and a blank or older one in the other, plants a read fault, makes a
    real change and lets the debounce commit it, then boots again clean.
    The faulty boot's line, offer and window must be what its reads proved,
    and every saved record and the change survive the reboot, or the faulty
    boot HELD the writer, persisted nothing, said so, and the reboot
    restores every saved record. `bench.jobs` threads walk the cases, each in
    a directory of its own; with `until`, the walk stops at the first
    finding carrying those words, which is all a planted control needs.
    """
    fr = fault_run(bench)
    cases = fault_cases(KLJ2_HDR + (bench.img_len - KLJ2_HDR - KLJ2_TRAILER) // 2)
    found, seen = threading.Event(), {}

    def walk(k: int) -> list[tuple[int, list[str]]]:
        """Every bench.jobs-th case from the k-th, until a named finding."""
        w = bench.work / f"rf{k}"
        w.mkdir(exist_ok=True)
        done = []
        for i in range(k, len(cases), bench.jobs):
            if found.is_set():
                break
            got = grade_fault_case(bench, fr, cases[i], w, seen)
            if until and any(until in item for item in got):
                found.set()
            done.append((i, got))
        return done

    with ThreadPoolExecutor(max_workers=bench.jobs) as pool:
        walked = sorted(x for part in pool.map(walk, range(bench.jobs)) for x in part)
    f = [item for _, got in walked for item in got]
    return f if found.is_set() else f + grade_hold_console(bench)


def grade_hold_console(bench: Bench) -> list[str]:
    """Check 13's console. A held writer refuses the console's commit and
    reports the hold; the operator's explicit wipe still erases both slots,
    as for a retired writer; and a writer that retires with a slot unread,
    for any cause RETIRE_CAUSES names, names the retire, not the slot."""
    f = []
    w = bench.work
    held = ("--slot-a", slot_file(bench, "rf_a.bin", bench.assemble(bench.frames, 0x5A5A5)),
            "--slot-b", slot_file(bench, "rf_b.bin", b"\xff" * SLOT),
            "--read-fault", "a:0:0:64", "--boot")
    out, s, _ = run(bench, *held, "--uart", "milan_nvm commit", "--uart", "milan_nvm",
                    "--idle-ms", "3000")
    _check(f, "refused; slot A gave no standing verdict in 3 reads at boot" in out and
           "writer HELD" in out and "unread=1." in out and s.get("erases") == 0 and
           s.get("acks") == 0 and s.get("backed") == 0,
           f"the held writer did not refuse the console's commit and report the hold: {s}")
    _, s, _ = run(bench, *held, "--uart", "milan_nvm wipe",
                  "--dump-slot-a", str(w / "rf_a1.bin"), "--dump-slot-b", str(w / "rf_b1.bin"))
    _check(f, s.get("erases") == 2 and (w / "rf_a1.bin").read_bytes() == b"\xff" * SLOT
           and (w / "rf_b1.bin").read_bytes() == b"\xff" * SLOT,
           f"the operator's wipe did not erase both slots while the writer was held: {s}")
    for cause, opts, line, state in RETIRE_CAUSES:
        out, s, _ = run(bench, *opts, *held, "--uart", "milan_nvm commit", "--uart", "milan_nvm")
        _check(f, "unread=1." in out and line in out and state in out and "writer HELD" not in out
               and "gave no standing verdict" not in out and HELD_LINE not in out,
               f"a writer retired by {cause} with a slot unread named the slot on the console, "
               f"not the retire: {s}")
    return f


def grade_refused_generation(bench: Bench) -> list[str]:
    """Check 14 (#671): a slot whose bytes read cleanly but fail validation is
    not authoritative and names no generation. With the other slot blank, no
    slot is accepted, and the first commit after a change is at sequence 1,
    whatever the refused slot's header says."""
    f = []
    golden = bench.assemble(bench.frames, 0x5A5A5)
    foreign = reseal(golden[:20] + struct.pack("<I", 0xDEAD_0001) + golden[24:])
    torn = golden[:KLJ2_HDR + 1] + bytes([golden[KLJ2_HDR + 1] ^ 1]) + golden[KLJ2_HDR + 2:]
    rid = max(bench.frames)
    new = frame_record(rid, bytes((0x40 + j) & 0xFF for j in range(len(bench.frames[rid]) - REC_HDR)),
                       bench.donor.layout)
    blank = b"\xff" * SLOT
    for label, refused in (("foreign entity", foreign), ("bad CRC", torn)):
        for where in "ab":
            a, b = (refused, blank) if where == "a" else (blank, refused)
            name = f"slot {where.upper()} refused ({label})"
            out, s, boot = run(bench, "--slot-a", slot_file(bench, "rg_a.bin", a),
                               "--slot-b", slot_file(bench, "rg_b.bin", b), "--boot",
                               "--change", f"{KLJ2_HDR + bench.offsets()[rid]}:{new.hex()}",
                               "--idle-ms", "1500", "--dump-slot-a", str(bench.work / "rg_a1.bin"))
            seq_seen = boot and boot.group(2 if where == "a" else 4)
            _check(f, boot is not None and boot.group(5) == "-" and seq_seen == "0",
                   f"{name}: a generation was taken from a refused slot: the boot line "
                   f"reports {boot and boot.group(0)}")
            got = (bench.work / "rg_a1.bin").read_bytes()[:bench.img_len]
            committed = struct.unpack_from("<I", got, 8)[0]
            _check(f, s.get("acks") == 1 and bench.verdict(got) == VD_OK and committed == 1,
                   f"{name}: a generation was taken from a refused slot: the first commit "
                   f"is at seq {committed:#x}, want 1: {s}")
    return f


#: checks 1 to 12, which the first five planted defects are graded by
WRITER_GRADES = (grade_blank_boot, grade_restore_change_commit, grade_ab_rule,
                 grade_parity, grade_failures, grade_liveness,
                 grade_snapshot_contract, grade_partial_ownership)
#: checks 13 and 14 (#671), which the read-fault defects are graded by
READ_FAULT_GRADES = (grade_read_faults, grade_refused_generation)
GRADES = WRITER_GRADES + READ_FAULT_GRADES


def grade(bench: Bench, grades: tuple = GRADES) -> list[str]:
    """Every check in `grades` for one shape."""
    findings = []
    for g in grades:
        findings += [f"{bench.cfg.stem}: {x}" for x in g(bench)]
    return findings


def self_test(cfg: Path, work: Path, firmware_text: str) -> list[str]:
    """Each planted writer defect must redden checks 1 to 12; a green control is a finding."""
    findings = []
    for label, (old, new) in MUTATIONS.items():
        if firmware_text.count(old) != 1:
            findings.append(f"self-test: the {label} plant no longer matches the firmware")
            continue
        sub = work / label
        sub.mkdir(parents=True)
        bench = make_bench(cfg, sub, firmware_text.replace(old, new))
        got = grade(bench, WRITER_GRADES)
        if label == "edge_cross" and not any("open record changed across unaligned" in item for item in got):
            findings.append("self-test: edge_cross missed its named partial ownership assertion")
        if not got:
            findings.append(f"self-test: the {label} defect was NOT caught")
        else:
            print(f"  self-test OK: {label:<22} caught by {len(got)} finding(s); "
                  f"first: {got[0]}")
    return findings


def replant(bench: Bench, work: Path, firmware_text: str) -> Bench:
    """`bench` with another firmware text compiled into `work`; the shape
    and its generated constants are reused, not rebuilt."""
    work.mkdir(parents=True)
    header = (bench.work / "generated/soc.h").read_text()
    return replace(bench, binary=compile_bench(work, firmware_text, header), work=work)


def self_test_read_faults(benches: list[Bench], work: Path, firmware_text: str) -> list[str]:
    """Each #671 defect, planted into a copy of the firmware on every bench,
    must be caught by a finding carrying its own words. Check 14 runs first,
    and check 13 stops at the first named finding."""
    findings = []
    for label, (pairs, words) in READ_FAULT_MUTATIONS.items():
        planted = firmware_text
        for old, new in pairs:
            if planted.count(old) != 1:
                findings.append(f"self-test: the {label} plant no longer matches the firmware")
                break
            planted = planted.replace(old, new)
        else:
            for bench in benches:
                pb = replant(bench, work / label / bench.cfg.stem, planted)
                got = grade_refused_generation(pb)
                if not any(words in item for item in got):
                    got += grade_read_faults(pb, until=words)
                named = [item for item in got if words in item]
                if not named:
                    findings.append(f"self-test: the {label} defect was NOT caught on "
                                    f"{bench.cfg.stem} by a finding naming {words!r} "
                                    f"({len(got)} other finding(s))")
                else:
                    print(f"  self-test OK: {label:<28} {bench.cfg.stem:<27} caught by "
                          f"{len(named)} named finding(s); first: {named[0]}")
    return findings


def main() -> int:
    """Grade every shipped shape; with --self-test, the controls too."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--config", action="append", type=Path,
                    help="configs to grade (default: every configs/endstation_*.yaml)")
    ap.add_argument("--self-test", action="store_true",
                    help="also plant each writer defect and require a finding")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4,
                    help="threads check 13 walks its cases on")
    a = ap.parse_args()
    cfgs = a.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    firmware_text = FIRMWARE.read_text()
    import test_boot_walk as bootwalk
    import test_disabled_writer as disabled

    findings = []
    benches = []
    with tempfile.TemporaryDirectory(prefix="nvmfw.") as tmp:
        for cfg in cfgs:
            work = Path(tmp) / cfg.stem
            work.mkdir()
            bench = replace(make_bench(cfg, work, firmware_text), jobs=max(1, a.jobs))
            benches.append(bench)
            got = grade(bench)
            got += disabled.grade(cfg, work / "disabled", firmware_text)
            got += bootwalk.grade(cfg, work / "boot-walk", firmware_text, bench)
            disabled.check_link_guard(bench)
            findings += got
            print(f"{cfg.stem:<28} records={len(bench.frames):3d} image={bench.img_len:5d} B "
                  f"{'OK' if not got else f'{len(got)} finding(s)'}")
        if a.self_test and not findings:
            findings += self_test(cfgs[0], Path(tmp) / "selftest", firmware_text)
            findings += self_test_read_faults(
                [b for b in benches if b is benches[0] or b.cfg.stem in PRODUCT_SHAPES],
                Path(tmp) / "read-fault-mutant", firmware_text)
            findings += disabled.self_test(cfgs[0], Path(tmp) / "disabled-mutant", firmware_text)
            findings += bootwalk.self_test(cfgs[0], Path(tmp) / "boot-walk-mutant", firmware_text)
            subprocess.run([sys.executable, str(HERE / "test_phy_firmware.py")],
                           check=True, timeout=180)
    for x in findings:
        print(f"FINDING: {x}")
    if findings:
        return 1
    print(f"saved-state writer gate: OK across {len(cfgs)} shape(s)"
          + (", and every planted defect reddened" if a.self_test else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
