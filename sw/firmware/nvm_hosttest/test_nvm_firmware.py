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
 10. `milan_nvm wipe` erases both slots.

NEGATIVE CONTROLS. `--self-test` plants four writer defects into a copy of
the firmware, one at a time, and requires the suite to redden on each: the
ascending-id check removed, the heartbeat dropped from the erase poll loop,
the read-back verify skipped, and the erased-record rule accepting a header
alone. A control that stays green is reported as the finding it is.

Usage:
    sw/firmware/nvm_hosttest/test_nvm_firmware.py            # every shipped shape
    sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
    sw/firmware/nvm_hosttest/test_nvm_firmware.py --config configs/endstation_ax7101_8x8.yaml

Exit 0 = every check passed (and every control reddened), 1 = a finding,
2 = the harness could not be built or run.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
import tempfile
import zlib
from dataclasses import dataclass
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

FIRMWARE = ROOT / "sw/firmware/milan_baremetal/milan_baremetal.c"
HARNESS = HERE / "nvm_host.c"
STUBS = HERE / "stubs"
#: the map, read out of the SoC source the way every other consumer reads it
RESERVED = literal("FLASHBOOT_RESERVED")
LAYOUT = literal("FLASHBOOT_LAYOUT")
JOURNAL = RESERVED["journal"]["offset"]
SLOT = RESERVED["journal"]["size"] // 2
AEM_OFFSET = LAYOUT["aem"]["offset"]
#: the staged container's band inside the host's window array: the same
#: place milan_soc.py puts it, the erase block below the response buffer
IMAGE_OFF = 0x100000 - 0x1000 - 0x10000
AEM_STUB = b"AEMI"
FENCE_RE = re.compile(r'__asm__ volatile\("fence[^"]*" ::: "memory"\);')
BOOT_RE = re.compile(
    r"Milan NVM: slot A (\S+) seq (\d+), slot B (\S+) seq (\d+); "
    r"offered (\S) seq (\d+) \((\S+)\)")
SUMMARY_RE = re.compile(r"^HOST (.*)$", re.M)

#: (label, the text that must occur exactly once, its replacement) - each is
#: one writer defect the suite must catch
MUTATIONS = {
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


def constants_header(shape: Shape, donor: Donor, ident: Ident) -> str:
    """The stub `generated/soc.h`: the constants milan_soc.py publishes, from
    the SAME derivation, plus the host addresses the bases resolve to."""
    lines = ["#pragma once", "#include <nvm_host.h>",
             "#define CONFIG_CLOCK_FREQUENCY 100000000"]
    values = {
        "MILAN_ENTITY_ID_LO": ident.entity_id & 0xFFFF_FFFF,
        "MILAN_ENTITY_ID_HI": ident.entity_id >> 32,
        "MILAN_MODEL_ID_LO": ident.model_id & 0xFFFF_FFFF,
        "MILAN_MODEL_ID_HI": ident.model_id >> 32,
        "MILAN_STATION_MAC_LO": 0x0403_0201, "MILAN_STATION_MAC_HI": 0x0605,
        "MILAN_N_TALKERS": 1, "MILAN_SR_VID": 2, "MILAN_LWSRP_CTRL_RESET": 0,
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
    lines.append(f"#define MILAN_NVM_IMAGE_BASE ((uintptr_t)nvm_host_ddr + 0x{IMAGE_OFF:x}u)")
    return "\n".join(lines) + "\n"


def compile_bench(work: Path, firmware_text: str, header: str) -> Path:
    """Build the harness and the (fence-blanked) firmware into `work`."""
    (work / "generated").mkdir(parents=True, exist_ok=True)
    (work / "generated/soc.h").write_text(header)
    fw = work / "milan_baremetal.c"
    fw.write_text(FENCE_RE.sub("(void)0;", firmware_text))
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
    overlay = json.loads((work / "builder" / cfg.stem / "aem_overlay.json").read_text())
    ident = Ident(seq=0, entity_id=int(overlay["adp"]["entity_id"], 16),
                  model_id=int(overlay["entity"]["entity_model_id"], 16))
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), donor.layout)
              for g, i, r, p, _b in inventory(shape, donor.base) if r is not None}
    binary = compile_bench(work, firmware_text, constants_header(shape, donor, ident))
    return Bench(cfg=cfg, shape=shape, donor=donor, ident=ident, binary=binary,
                 work=work, frames=frames, expect=expected_payloads(shape))


def run(bench: Bench, *args: str) -> tuple[str, dict[str, int], re.Match | None]:
    """One harness run: its transcript, the HOST summary and the boot line."""
    r = subprocess.run([str(bench.binary), *args], capture_output=True, text=True,
                       cwd=bench.work, timeout=600)
    if r.returncode:
        raise SystemExit(f"harness failed ({r.returncode}): {' '.join(args)}\n"
                         f"{r.stdout}\n{r.stderr}")
    summary = {}
    for line in SUMMARY_RE.findall(r.stdout):
        if line.startswith("hb="):
            summary = {k: int(v) for k, v in (kv.split("=") for kv in line.split())}
    return r.stdout, summary, BOOT_RE.search(r.stdout)


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

    With nothing outstanding the loss the commit deadline inflicts heals on
    the next heartbeat (section 9.2's clean recovery), so the loss is counted
    rather than sampled; with a change outstanding, `nvm_stale` must still
    stand after the deadline, because the retry fails the same way.
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
               f"the commit deadline did not revoke the claim after a failed {mode}: {s}")
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


GRADES = (grade_blank_boot, grade_restore_change_commit, grade_ab_rule,
          grade_parity, grade_failures, grade_liveness)


def grade(bench: Bench) -> list[str]:
    """Every check for one shape."""
    findings = []
    for g in GRADES:
        findings += [f"{bench.cfg.stem}: {x}" for x in g(bench)]
    return findings


def self_test(cfg: Path, work: Path, firmware_text: str) -> list[str]:
    """Each planted defect must redden the suite; a green control is a finding."""
    findings = []
    for label, (old, new) in MUTATIONS.items():
        if firmware_text.count(old) != 1:
            findings.append(f"self-test: the {label} plant no longer matches the firmware")
            continue
        sub = work / label
        sub.mkdir(parents=True)
        bench = make_bench(cfg, sub, firmware_text.replace(old, new))
        got = grade(bench)
        if not got:
            findings.append(f"self-test: the {label} defect was NOT caught")
        else:
            print(f"  self-test OK: {label:<22} caught by {len(got)} finding(s); "
                  f"first: {got[0]}")
    return findings


def main() -> int:
    """Grade every shipped shape; with --self-test, the controls too."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--config", action="append", type=Path,
                    help="configs to grade (default: every configs/endstation_*.yaml)")
    ap.add_argument("--self-test", action="store_true",
                    help="also plant each writer defect and require a finding")
    a = ap.parse_args()
    cfgs = a.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    firmware_text = FIRMWARE.read_text()
    findings = []
    with tempfile.TemporaryDirectory(prefix="nvmfw.") as tmp:
        for cfg in cfgs:
            work = Path(tmp) / cfg.stem
            work.mkdir()
            bench = make_bench(cfg, work, firmware_text)
            got = grade(bench)
            findings += got
            print(f"{cfg.stem:<28} records={len(bench.frames):3d} image={bench.img_len:5d} B "
                  f"{'OK' if not got else f'{len(got)} finding(s)'}")
        if a.self_test and not findings:
            findings += self_test(cfgs[0], Path(tmp) / "selftest", firmware_text)
    for x in findings:
        print(f"FINDING: {x}")
    if findings:
        return 1
    print(f"saved-state writer gate: OK across {len(cfgs)} shape(s)"
          + (", and every planted defect reddened" if a.self_test else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
