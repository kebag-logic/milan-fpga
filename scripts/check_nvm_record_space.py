#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: the persisted record set must fit the NVM record namespace at EVERY
shipped shape, not just the erase block.

WHY THIS EXISTS. The first version of
`docs/design/SAVED_STATE_FASTCONNECT.md` sized the saved set in BYTES and
concluded that whole-image A/B promotion was affordable. That part was right.
What it never checked was the other capacity in the same design: the processor's
NVM port (`KL_pp_nvm_port` in the protocol-processor submodule) addresses a
record by `record_id[7:0]`, and the donor's F07.8 framing says "one record per
item group and index". One record per
writable name at the 8x8 shape needs 235 ids on its own; the whole persisted
inventory needs 292. The namespace holds 256. The design could not have been
built as written, and no gate said so, because every check in the tree was
counting bytes.

WHAT IT CHECKS, per config, for the full persisted inventory of Milan v1.2
5.3.5.1 / 5.3.7.1 / 5.3.7.6 / 5.3.8.1 / 5.3.8.2 / 5.3.8.3 / 5.3.8.7 / 5.3.9.1 /
5.3.10.1 / 5.3.11.1 / 5.3.13 plus the three design-affirmative items (donor
`docs/architecture/07_memory_maps.md` 5.1: configuration index, system unique
id, media clock reference):

  1. every allocated record id is unique          -- no aliasing
  2. every id is inside the 8-bit namespace       -- < 256
  3. every group stays inside its allocated block -- shape growth is caught
     at the block boundary, not by a later collision
  4. every record payload fits `MAX_PAYLOAD_P`    -- the port refuses a stream
     it cannot delimit BEFORE any device traffic
  5. the whole image fits one 64 KiB erase block  -- the A/B slot geometry

The BINDING block base is READ from the donor RTL (`REC_ID_BASE_P` in
`KL_acmp_nvm_shadow`), never mirrored here: that parameter is already fixed in
landed gateware, so the allocation contract has to bend around it rather than
restate it. The file it is read from is DERIVED through `scripts/pp_srcs.py`
rather than named, so a donor that moves or renames the module is followed
instead of silently missed.

USAGE
  scripts/check_nvm_record_space.py              # every configs/endstation_*.yaml
  scripts/check_nvm_record_space.py --config configs/endstation_ax7101_8x8.yaml
  scripts/check_nvm_record_space.py --flat       # the pre-review allocation:
                                                 # one record per item, no banking
  scripts/check_nvm_record_space.py --mutate collide   # one negative control
  scripts/check_nvm_record_space.py --self-test        # run them all

`--flat` and every `--mutate` arm are negative controls and are EXPECTED to
exit 1. `--self-test` runs all five and fails if ANY of them passes, so no
assertion here can quietly become vacuous: each arm perturbs exactly one fixed
point and must be caught by the check that owns it.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---- the fixed points, all of them measured or read, none invented ---------

ID_SPACE = 256          # record_id[7:0], KL_pp_nvm_port manager face
MAX_PAYLOAD = 1024      # KL_pp_nvm_port MAX_PAYLOAD_P default
ERASE_BLOCK = 64 * 1024  # N25Q128 smallest erase unit = one A/B slot
REC_HDR = 8             # F07.8: magic, layout_version, record_id, plen, crc16
NAME_BYTES = 64         # AEM name field
NAMES_PER_BANK = 8      # the banking factor the design page fixes
KLJ2_HDR = 40           # KLJ2 container header, 10 words
KLJ2_TRAILER = 4        # CRC-32 word, last
ALIGN = 4               # the record area is zero-padded to a word boundary

# Payload widths in bytes. BINDING is the one the donor already fixed
# (KL_acmp_nvm_shadow: payload_length = 20); the rest are the AEM field widths.
PAY = {
    "CFG_IDX": 2,       # configuration_index u16
    "SUID": 8,          # system_unique_id u64
    "RATE": 4,          # current_sampling_rate u32
    "CLKSRC": 2,        # clock_source_index u16
    "MCR": 66,          # user_mcr_prio u8 + MC domain name 64 B + pad
    "BINDING": 20,      # measured: KL_acmp_nvm_shadow payload_length
    "FMT_IN": 8,        # stream_format u64
    "FMT_OUT": 8,
    "PT_OFS": 4,        # presentation time offset u32 ns
}
MAP_ENTRY = 8           # {stream_index, stream_channel, cluster_offset,
                        #  cluster_channel} x u16

# The banked allocation contract. Each entry is {base, block} and the group's
# index must satisfy 0 <= index < block.
ALLOC = {
    "CFG_IDX":    (0x00, 1),
    "SUID":       (0x01, 1),
    "RATE":       (0x02, 8),
    "CLKSRC":     (0x0A, 8),
    "MCR":        (0x12, 8),
    "BINDING":    (None, 16),   # base READ from the donor RTL
    "FMT_IN":     (0x30, 16),
    "FMT_OUT":    (0x40, 16),
    "PT_OFS":     (0x50, 16),
    "MAPS_IN":    (0x60, 16),
    "MAPS_OUT":   (0x70, 16),
    "NAMES_BANK": (0x80, 128),
}


def _mut_collide():
    """Two groups share a base -- the uniqueness assertion must fire."""
    ALLOC["FMT_OUT"] = (ALLOC["FMT_IN"][0], ALLOC["FMT_IN"][1])


def _mut_block():
    """A group's block is too small for the shape -- capacity must fire."""
    b, _ = ALLOC["NAMES_BANK"]
    ALLOC["NAMES_BANK"] = (b, 8)


def _mut_payload():
    """A bank grows past what the port can delimit -- payload must fire."""
    global NAMES_PER_BANK
    NAMES_PER_BANK = 32


def _mut_image():
    """The slot shrinks below the image -- the byte bound must fire."""
    global ERASE_BLOCK
    ERASE_BLOCK = 8 * 1024


MUTATIONS = {
    "collide": _mut_collide,
    "block": _mut_block,
    "payload": _mut_payload,
    "image": _mut_image,
}

SHADOW_STEM = "KL_acmp_nvm_shadow"
BASE_RE = re.compile(r"parameter\s+logic\s*\[7:0\]\s+REC_ID_BASE_P\s*=\s*8'h([0-9A-Fa-f]{2})")


def shadow_path() -> Path:
    """Locate the ACMP NVM shadow through the derived submodule source list."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import pp_srcs
    hits = [s for s in pp_srcs.pp_sources()
            if Path(s).stem == SHADOW_STEM]
    if len(hits) != 1:
        sys.exit(f"FATAL: expected exactly one {SHADOW_STEM} source in the "
                 f"derived submodule list, found {len(hits)}. The donor "
                 f"renamed or duplicated it and this gate must be re-pointed, "
                 f"not relaxed.")
    return ROOT / hits[0]


def binding_base() -> int:
    """Read REC_ID_BASE_P out of the donor RTL rather than mirroring it."""
    shadow = shadow_path()
    m = BASE_RE.search(shadow.read_text())
    if not m:
        sys.exit(f"FATAL: REC_ID_BASE_P not found in {shadow.name}; the donor "
                 f"moved the parameter and this gate must be re-pointed, not "
                 f"relaxed.")
    return int(m.group(1), 16)


def build(cfg: Path, out: Path) -> tuple[int, dict, list, list]:
    """Build one config and return (writable names, descriptor counts, ports)."""
    subprocess.run([sys.executable, str(ROOT / "sw/builder/endstation_builder.py"),
                    str(cfg), "-o", str(out)],
                   check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    stem = cfg.stem
    overlay = out / stem / "aem_overlay.json"
    img = out / f"{stem}.img.bin"
    subprocess.run([sys.executable, str(ROOT / "avdecc/gen_aemi_image.py"),
                    "--overlay", str(overlay), "-o", str(img),
                    "--line-bytes", "576"],
                   check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    blob = img.read_bytes()
    _, names = struct.unpack_from(">HH", blob, 8)
    o = json.loads(overlay.read_text())
    ports = o["stream_ports"]
    return names, o["descriptor_counts"], ports["input"], ports["output"]


def inventory(names, dc, spi, spo, base, flat):
    """Return the record list: (group, index, id, payload_bytes)."""
    recs = []

    def add(group, index, payload):
        b, block = ALLOC[group]
        if group == "BINDING":
            b = base
        if index >= block:
            recs.append((group, index, None, payload, block))
        else:
            recs.append((group, index, b + index, payload, block))

    add("CFG_IDX", 0, PAY["CFG_IDX"])
    add("SUID", 0, PAY["SUID"])
    for u in range(dc["AUDIO_UNIT"]):
        add("RATE", u, PAY["RATE"])
    for d in range(dc["CLOCK_DOMAIN"]):
        add("CLKSRC", d, PAY["CLKSRC"])
        add("MCR", d, PAY["MCR"])
    for k in range(dc["STREAM_INPUT"]):
        add("BINDING", k, PAY["BINDING"])
        add("FMT_IN", k, PAY["FMT_IN"])
    for i in range(dc["STREAM_OUTPUT"]):
        add("FMT_OUT", i, PAY["FMT_OUT"])
        add("PT_OFS", i, PAY["PT_OFS"])
    for p in spi:
        add("MAPS_IN", p["index"], p["clusters"] * MAP_ENTRY)
    for p in spo:
        add("MAPS_OUT", p["index"], p["clusters"] * MAP_ENTRY)

    if flat:
        # The pre-review allocation: one record per writable name, laid out
        # straight after the last per-index group. This is what the first
        # version of the design page adopted from F07.8 unchanged.
        first = ALLOC["NAMES_BANK"][0]
        for n in range(names):
            recs.append(("NAME", n, first + n, NAME_BYTES, names))
    else:
        banks = (names + NAMES_PER_BANK - 1) // NAMES_PER_BANK
        b, block = ALLOC["NAMES_BANK"]
        for k in range(banks):
            recs.append(("NAMES_BANK", k, b + k if k < block else None,
                         NAMES_PER_BANK * NAME_BYTES, block))
    return recs


def check_one(cfg, out, base, flat, verbose):
    names, dc, spi, spo = build(cfg, out)
    recs = inventory(names, dc, spi, spo, base, flat)
    findings = []

    seen = {}
    top = -1
    for group, index, rid, payload, block in recs:
        if rid is None:
            findings.append(
                f"{cfg.stem}: {group}[{index}] has no id -- the group's block "
                f"holds {block} and this shape needs {index + 1}")
            continue
        top = max(top, rid)
        if rid >= ID_SPACE:
            findings.append(
                f"{cfg.stem}: {group}[{index}] wants record_id {rid} but the "
                f"port's namespace is record_id[7:0] -- {ID_SPACE} ids")
        if rid in seen:
            findings.append(
                f"{cfg.stem}: record_id 0x{rid:02X} is claimed by both "
                f"{seen[rid]} and {group}[{index}] -- one of them is lost")
        seen[rid] = f"{group}[{index}]"
        if payload > MAX_PAYLOAD:
            findings.append(
                f"{cfg.stem}: {group}[{index}] payload is {payload} B, over "
                f"MAX_PAYLOAD_P = {MAX_PAYLOAD} -- the port refuses it")

    body = sum(REC_HDR + p for _, _, _, p, _ in recs)
    body += (-body) % ALIGN
    image = KLJ2_HDR + body + KLJ2_TRAILER
    if image > ERASE_BLOCK:
        findings.append(
            f"{cfg.stem}: image is {image} B, over one {ERASE_BLOCK} B erase "
            f"block -- whole-image A/B promotion no longer fits a slot")

    if verbose:
        print(f"{cfg.stem:<28} names={names:3d} records={len(recs):3d} "
              f"top_id={'--' if top < 0 else f'0x{top:02X}'} "
              f"image={image:6d} B  ({image * 100 // ERASE_BLOCK}% of a slot)")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", action="append", type=Path,
                    help="config to check (default: every configs/endstation_*.yaml)")
    ap.add_argument("--flat", action="store_true",
                    help="the pre-review allocation, one record per item "
                         "(negative control: MUST fail at 8x8)")
    ap.add_argument("--mutate", choices=sorted(MUTATIONS),
                    help="perturb one fixed point so the matching assertion "
                         "must fire (negative control: MUST fail)")
    ap.add_argument("--self-test", action="store_true",
                    help="run every negative control and require each to "
                         "redden, then run the real check")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.mutate:
        MUTATIONS[args.mutate]()

    if args.self_test:
        controls = ["--flat"] + [f"--mutate={m}" for m in sorted(MUTATIONS)]
        for c in controls:
            r = subprocess.run([sys.executable, __file__, c, "--quiet"],
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode == 0:
                print(f"SELF-TEST FAILED: negative control {c} PASSED. The "
                      f"assertion it targets is vacuous and this gate is "
                      f"green because it stopped looking.")
                return 1
            first = next((ln for ln in r.stdout.splitlines()
                          if ln.startswith("FINDING:")), "(no FINDING line)")
            print(f"self-test OK: {c:<18} exits {r.returncode} -- {first}")
        print()

    cfgs = args.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    base = binding_base()
    if not args.quiet:
        print(f"BINDING base read from the donor: REC_ID_BASE_P = 0x{base:02X}")

    findings = []
    with tempfile.TemporaryDirectory(prefix="nvmrec.") as tmp:
        for cfg in cfgs:
            findings += check_one(cfg, Path(tmp), base, args.flat,
                                  not args.quiet)

    if findings:
        print()
        for f in findings[:12]:
            print(f"FINDING: {f}")
        if len(findings) > 12:
            print(f"... and {len(findings) - 12} more of the same shape")
        print(f"\n{len(findings)} finding(s) across {len(cfgs)} config(s)")
        return 1
    if not args.quiet:
        print(f"\n0 finding(s) across {len(cfgs)} config(s): every persisted "
              f"record has a unique id inside record_id[7:0], every group is "
              f"inside its block, every payload fits MAX_PAYLOAD_P and every "
              f"image fits one erase block")
    return 0


if __name__ == "__main__":
    sys.exit(main())
