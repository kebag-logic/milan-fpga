#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""check_image_identity.py - the identity gate of one built image (#665, decision D2).

Before the flip (S13) VERSION does not tell the two placements apart, so a
split image is identified by three things that must agree with what the image
holds: the SoC ident string names the placement, the mailbox's ID register
gives the contract major and minor, and the image manifest
(`image_manifest.json`, which milan_soc.py writes for a split build only)
records the placement, the control firmware ELF's sha256 and the bitstream's
payload sha256. An image directory without a manifest is all-fabric, as every
image before the split was, and its outputs are unchanged.

An image is a milan_soc.py output directory: csr.csv, gateware/ with the top
Verilog, its Vivado script and the rom banks' init files, and the manifest.
The gate reads only what the build wrote there, then refuses, by kind:

  manifest   a manifest that is not schema 1 or names another placement, an
             ident other than the one csr.csv carries, a VERSION or a mailbox
             contract other than the milan_csr.sv and KL_mbx_pkg.sv the
             image's Vivado script reads
  ident      an ident whose last word does not name the placement: `split`
             for a split image, any other word for an all-fabric one
  firmware   a control firmware ELF whose sha256 is not the manifest's, or
             whose rom words are not those the rom banks' init files hold
  bitstream  a bitstream whose payload sha256 or part is not the manifest's,
             or one the manifest does not bind
  placement  a split image whose datapath is not built with CTRL_SPLIT_P = 1
             or that carries no mailbox; an all-fabric image that carries any
             mailbox (a ctrl_mbx region or CSR bank, or a KL_mbx instance)
             or a split datapath

    python3 sw/litex/check_image_identity.py IMAGE [--firmware ELF] [--bitstream BIT]

Exit 0: every rule holds. 1: a finding, one `FINDING <kind>: ...` line each.
2: the image cannot be read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "avdecc"))
import ctrl_memory  # noqa: E402
from aem_descriptors import rtl_version  # noqa: E402
from qspi_owner_transition import TransitionError, bitstream_binding  # noqa: E402

MANIFEST = "image_manifest.json"
SCHEMA = 1
#: The ident's last word in a split image; every other word is the all-fabric ident before the split.
SPLIT_WORD = "split"
#: Each kind of finding, in the order the module docstring gives them.
KINDS = ("manifest", "ident", "firmware", "bitstream", "placement")
MBX_VERSION = re.compile(r"localparam\s+int\s+unsigned\s+MBX_VERSION_(MAJOR|MINOR)_C\s*=\s*32'd(\d+)\s*;")


class Unreadable(Exception):
    """The image lacks a file the gate reads, or a file it cannot parse."""


def _read(path: Path) -> str:
    try:
        return path.read_text()
    except OSError as exc:
        raise Unreadable(f"cannot read {path}: {exc}") from exc


def manifest(ident: str, version: int, mailbox: tuple[int, int], elf: Path, bitstream: Path | None) -> dict:
    """The manifest of a split image, which milan_soc.py writes beside its outputs (#665 S9).

    The firmware path is repository-relative when the ELF is in the tree."""
    data, elf = elf.read_bytes(), elf.resolve()
    return {"schema": SCHEMA, "placement": SPLIT_WORD, "ident": ident, "version": f"0x{version:08x}",
            "mailbox": {"major": mailbox[0], "minor": mailbox[1]},
            "ctrl_firmware": {"path": str(elf.relative_to(ROOT) if elf.is_relative_to(ROOT) else elf),
                              "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)},
            "bitstream": bitstream_binding(bitstream) if bitstream else None}


def mailbox_version(package: Path) -> tuple[int, int]:
    """(major, minor) as a KL_mbx_pkg.sv states them, the ID register's two fields."""
    found = dict(MBX_VERSION.findall(_read(package)))
    if set(found) != {"MAJOR", "MINOR"}:
        raise Unreadable(f"{package}: no MBX_VERSION_MAJOR_C and MBX_VERSION_MINOR_C")
    return int(found["MAJOR"]), int(found["MINOR"])


def _top(gateware: Path) -> tuple[Path, Path]:
    """The image's top Verilog and Vivado script."""
    scripts = sorted(p for p in gateware.glob("*.tcl") if (gateware / (p.stem + ".v")).is_file())
    if len(scripts) != 1:
        raise Unreadable(f"{gateware}: expected one Vivado script beside its top Verilog, found "
                         f"{[p.name for p in scripts]}")
    return gateware / (scripts[0].stem + ".v"), scripts[0]


def _sources(script: str) -> list[Path]:
    """Every source file the Vivado script reads."""
    return [Path(p) for p in re.findall(r"^read_verilog (?:-\w+ )*\{([^}]+)\}", script, re.M)]


def _source(script: str, name: str, gateware: Path) -> Path:
    """The one source file the Vivado script reads under this name."""
    hits = [p for p in _sources(script) if p.name == name]
    if len(hits) != 1:
        raise Unreadable(f"{gateware}: the Vivado script reads {len(hits)} {name}")
    return hits[0]


def _split_param(verilog: str) -> int:
    """The datapath instance's CTRL_SPLIT_P: 0 when the instance leaves it at its default, or there is none."""
    head = re.search(r"^milan_datapath #\((.*?)^\) \w+\s*\(", verilog, re.M | re.S)
    if not head:
        return 0
    value = re.search(r"\.CTRL_SPLIT_P\s*\(\s*(\d+)'d(\d+)\s*\)", head.group(1))
    return int(value.group(2)) if value else 0


def facts(image: Path) -> dict:
    """What the image holds, read from its build outputs."""
    rows = [line.split(",") for line in _read(image / "csr.csv").splitlines()]
    regions = {r[1] for r in rows if r[0] == "memory_region"}
    banks = {r[1] for r in rows if r[0] == "csr_base"}
    idents = [r[2] for r in rows if r[:2] == ["constant", "config_identifier"]]
    if len(idents) != 1:
        raise Unreadable(f"{image}/csr.csv: {len(idents)} config_identifier constants")
    top, tcl = _top(image / "gateware")
    verilog, script = _read(top), _read(tcl)
    inits = sorted((image / "gateware").glob(f"{top.stem}_rom_bank*.init"),
                   key=lambda p: int(p.stem.rsplit("bank", 1)[1]))
    path = image / MANIFEST
    try:
        claimed = json.loads(_read(path)) if path.exists() else None
    except json.JSONDecodeError as exc:
        raise Unreadable(f"{path}: {exc}") from exc
    pkg = [p for p in _sources(script) if p.name == "KL_mbx_pkg.sv"]
    major, minor = rtl_version(_source(script, "milan_csr.sv", image / "gateware"))
    return {
        "manifest": claimed,
        "ident": idents[0],
        "mailbox": sorted({*(n for n in regions | banks if n.startswith("ctrl_mbx")),
                           *re.findall(r"^(KL_mbx\w*) \w+\s*\(", verilog, re.M)}),
        "mailbox_version": mailbox_version(pkg[0]) if len(pkg) == 1 else None,
        "version": (major << 16) | minor,
        "ctrl_split": _split_param(verilog),
        "rom_words": [int(w, 16) for p in inits for w in _read(p).split()],
        "bitstreams": sorted(image.glob("gateware/*.bit")),
    }


def _manifest_rules(got: dict, found: list) -> None:
    claimed = got["manifest"]
    want = {"schema", "placement", "ident", "version", "mailbox", "ctrl_firmware", "bitstream"}
    if not isinstance(claimed, dict) or set(claimed) != want:
        fields = sorted(claimed) if isinstance(claimed, dict) else claimed
        found.append(("manifest", f"the manifest's fields are {fields}, not {sorted(want)}"))
        return
    if claimed["schema"] != SCHEMA or claimed["placement"] != SPLIT_WORD:
        found.append(("manifest", f"the manifest is schema {claimed['schema']} at placement {claimed['placement']!r}; "
                                  f"only a split image has a manifest, schema {SCHEMA}"))
    if claimed["ident"] != got["ident"]:
        found.append(("manifest", f"the manifest's ident {claimed['ident']!r} is not the image's {got['ident']!r}"))
    if claimed["version"] != f"0x{got['version']:08x}":
        found.append(("manifest", f"the manifest's VERSION {claimed['version']} is not the image's "
                                  f"milan_csr.sv 0x{got['version']:08x}"))
    have = got["mailbox_version"]
    if have is None or claimed["mailbox"] != {"major": have[0], "minor": have[1]}:
        found.append(("manifest", f"the manifest's mailbox contract {claimed['mailbox']} is not the image's "
                                  f"KL_mbx_pkg.sv {have}"))


def _firmware_rules(got: dict, firmware: Path | None, found: list) -> None:
    record = got["manifest"]["ctrl_firmware"]
    elf = firmware or Path(record["path"])
    elf = elf if elf.is_absolute() else ROOT / elf
    try:
        data = elf.read_bytes()
    except OSError as exc:
        found.append(("firmware", f"the control firmware {elf} cannot be read: {exc}"))
        return
    if hashlib.sha256(data).hexdigest() != record["sha256"]:
        found.append(("firmware", f"the control firmware {elf} has sha256 {hashlib.sha256(data).hexdigest()}, "
                                  f"the manifest records {record['sha256']}"))
    try:
        words = ctrl_memory.rom_words(ctrl_memory.read_elf(elf))
    except ctrl_memory.Refusal as exc:
        found.append(("firmware", f"the control firmware {elf} is not a split image: {exc}"))
        return
    if words != got["rom_words"]:
        found.append(("firmware", f"the rom banks hold {len(got['rom_words'])} words that are not the "
                                  f"{len(words)} rom words of {elf}"))


def _bitstream_rules(got: dict, bitstream: Path | None, found: list) -> None:
    bound = got["manifest"]["bitstream"] if got["manifest"] else None
    candidates = [bitstream] if bitstream else got["bitstreams"]
    if bound is None:
        if candidates and got["manifest"] is not None:
            found.append(("bitstream", f"the manifest binds no bitstream, the image has "
                                       f"{[str(c) for c in candidates]}"))
        return
    if len(candidates) != 1:
        found.append(("bitstream", f"the manifest binds a bitstream, the image has {len(candidates)}"))
        return
    try:
        have = bitstream_binding(candidates[0])
    except TransitionError as exc:
        found.append(("bitstream", f"{candidates[0]} is not a bitstream: {exc}"))
        return
    if have != bound:
        found.append(("bitstream", f"{candidates[0]} binds {have}, the manifest records {bound}"))


def findings(image: Path, firmware: Path | None = None, bitstream: Path | None = None) -> list[tuple[str, str]]:
    """Every (kind, words) the image breaks; empty when its identity agrees with what it holds."""
    got, found = facts(image), []
    split = got["manifest"] is not None
    if split:
        _manifest_rules(got, found)
        if found:
            return found
        _firmware_rules(got, firmware, found)
    word = got["ident"].rsplit(" ", 1)[-1]
    if split != (word == SPLIT_WORD):
        found.append(("ident", f"the ident {got['ident']!r} does not name the "
                               f"{'split' if split else 'all-fabric'} placement"))
    _bitstream_rules(got, bitstream, found)
    if split and (got["ctrl_split"] != 1 or not got["mailbox"]):
        found.append(("placement", f"a split image whose datapath has CTRL_SPLIT_P = {got['ctrl_split']} and "
                                   f"mailbox {got['mailbox'] or 'none'}"))
    if not split and (got["mailbox"] or got["ctrl_split"]):
        found.append(("placement", f"an all-fabric image carries a mailbox {got['mailbox'] or 'none'} or a "
                                   f"split datapath (CTRL_SPLIT_P = {got['ctrl_split']})"))
    return found


def main() -> int:
    """Grade one image; the exit status is the verdict."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("image", type=Path, help="a milan_soc.py output directory")
    ap.add_argument("--firmware", type=Path, help="the control firmware ELF (default: the manifest's path)")
    ap.add_argument("--bitstream", type=Path, help="the bitstream to bind (default: the image's gateware/*.bit)")
    args = ap.parse_args()
    try:
        found = findings(args.image, args.firmware, args.bitstream)
        placement = "split" if facts(args.image)["manifest"] is not None else "all-fabric"
    except Unreadable as exc:
        print(f"REFUSED: {exc}")
        return 2
    for kind, words in found:
        print(f"FINDING {kind}: {words}")
    if not found:
        print(f"image identity: a {placement} image whose manifest, ident, firmware, bitstream and placement "
              f"agree")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
