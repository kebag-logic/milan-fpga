#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Refuse to flash a persistent image set whose gPTP owner is not the fabric.

THE PRODUCT IS BARE-METAL ONLY (#259, USER directive 2026-08-25). The one
supported persistent image set is {bitstream, aem} with the fabric gPTP plane
as its sole PHC and publication owner. This tool is the deploy-time gate for
that fact: it validates the layout's compiled owner enum, refuses every
retired Linux boot-chain artifact, and (when the bitstream is supplied) binds
the layout to the exact parsed configuration payload and FPGA part.

RETIRED ROLE, EXPLICITLY. Until #259 this tool also graded a Linux rootfs
archive against the gateware owner: newc parsing, versioned owner profiles,
linuxptp payload rules and init-lifecycle semantics. That was the product
contract for the option-OFF software owner, and #259 retires that owner
entirely: there is no rootfs, no ptp4l/phc2sys, and no software lifecycle to
grade. An option-OFF elaboration remains only as verification-only hardware
and is NOT flashable, so a layout recording any owner other than 'fabric' is
refused here rather than paired. The old `--rootfs` argument is gone; passing
it is an argparse error, never a silently ignored input.

Exit 0 = the layout records a flashable fabric-owner bare-metal set (and, if
supplied, the bitstream binding holds). Exit 2 = refusal.
"""
import argparse
import json
import sys

from gptp_owner_contract import GPTP_OWNERS
from qspi_owner_transition import (TransitionError, validate_artifact_pair)

OWNERS = GPTP_OWNERS
#: Image rows only a retired Linux boot chain carries. Their presence in a
#: layout means the artifact predates #259 or was hand-built against the
#: retired contract; either way it is not a product image.
RETIRED_LINUX_IMAGES = ("kernel", "opensbi", "dtb", "rootfs")
RETIRED_MANIFESTS = ("full", "kernel")


class ContractError(RuntimeError):
    pass


def _load_layout(path):
    try:
        with open(path, encoding="utf-8") as stream:
            layout = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read layout {path}: {exc}") from exc
    if not isinstance(layout, dict):
        raise ContractError("layout root must be an object")
    owner = layout.get("gptp_owner")
    if owner not in OWNERS:
        raise ContractError(
            "layout has no valid gptp_owner enum "
            "(expected 'none', 'fabric', or 'software')")
    images = layout.get("images")
    if not isinstance(images, list) or any(not isinstance(row, dict)
                                           for row in images):
        raise ContractError("layout images must be a list of objects")
    names = [row.get("name") for row in images]
    if any(not isinstance(name, str) or not name for name in names):
        raise ContractError("every layout image needs a non-empty string name")
    if len(names) != len(set(names)):
        raise ContractError("layout contains duplicate image names")
    return layout, owner, set(names)


def check_pair(layout_path, expected_owner=None,
               bit_path=None, expected_fpga_part=None):
    layout, owner, names = _load_layout(layout_path)

    retired_rows = sorted(names & set(RETIRED_LINUX_IMAGES))
    if retired_rows:
        raise ContractError(
            f"layout names retired Linux boot images {retired_rows}: the "
            "product is bare-metal only (#259) and no Linux image set can "
            "be flashed")
    manifest = layout.get("manifest")
    if manifest in RETIRED_MANIFESTS:
        raise ContractError(
            f"layout manifest {manifest!r} is a retired Linux boot chain "
            "(#259): the product manifest is 'baremetal'")
    # [R-parallel] on #228: a manifest merely NOT-retired passed, so
    # {manifest: 'not-baremetal', images: []} was approved as a flashable
    # set. The one product manifest is 'baremetal', exactly, and the one
    # product row set is exactly {bitstream, aem}: an absent row is an
    # unflashable set, a surplus row is an unreviewed write.
    if manifest != "baremetal":
        raise ContractError(
            f"layout manifest {manifest!r} is not the bare-metal product "
            "manifest 'baremetal'")
    required = {"bitstream", "aem"}
    if names != required:
        missing = sorted(required - names)
        surplus = sorted(names - required)
        raise ContractError(
            "layout images are not exactly the bare-metal {bitstream, aem} "
            f"set: missing {missing}, surplus {surplus}")

    if owner != "fabric":
        detail = ("has no gPTP owner" if owner == "none"
                  else "records the retired software owner (#259: no "
                       "ptp4l/phc2sys product path exists)")
        raise ContractError(
            f"layout owner {owner!r} {detail}; the bare-metal product's one "
            "PHC and publication owner is the fabric plane")
    if expected_owner is not None and owner != expected_owner:
        raise ContractError(
            f"layout owner is {owner!r}, selected build expects "
            f"{expected_owner!r}")
    if expected_fpga_part is not None and bit_path is None:
        raise ContractError("--expected-fpga-part requires --bit")
    if bit_path is not None:
        try:
            bound = validate_artifact_pair(
                layout_path, bit_path, expected_fpga_part)
        except TransitionError as exc:
            raise ContractError(
                f"layout/bitstream binding failed: {exc}") from exc
        if bound["owner"] != owner:
            raise ContractError("layout owner changed during bitstream binding")
    return owner, "fabric-owned bare-metal image set"


def self_test():
    import os
    import tempfile
    from qspi_owner_transition import _fake_bit, bitstream_binding
    checks = 0

    def expect(ok, layout, expected=None, bit=None, part=None):
        nonlocal checks
        checks += 1
        try:
            check_pair(layout, expected, bit, part)
        except ContractError:
            if ok:
                raise
        else:
            if not ok:
                raise AssertionError("owner mismatch unexpectedly passed")

    with tempfile.TemporaryDirectory() as temp:
        def layout(owner, key=True, manifest="baremetal", extra_rows=(),
                   name=None, rows="both"):
            path = os.path.join(
                temp, name or f"layout-{owner}-{key}-{manifest}.json")
            bit_row = {"name": "bitstream", "offset": 0, "budget": 0x400000}
            aem_row = {"name": "aem", "offset": 0x400000, "budget": 0x10000}
            rows = {"both": [bit_row, aem_row], "empty": [],
                    "no-aem": [bit_row], "no-bitstream": [aem_row]}[rows]
            rows += [dict(row) for row in extra_rows]
            body = {"images": rows}
            if manifest is not None:
                body["manifest"] = manifest
            if key:
                body["gptp_owner"] = owner
            with open(path, "w", encoding="utf-8") as stream:
                json.dump(body, stream)
            return path

        # The one product shape.
        expect(True, layout("fabric"))
        # Owner enum refusals: none, the retired software owner, a missing
        # key, and an unknown spelling.
        expect(False, layout("none"))
        expect(False, layout("software"))
        expect(False, layout("fabric", key=False))
        expect(False, layout("unknown"))
        # The recipe binding still bites in both directions.
        expect(True, layout("fabric"), expected="fabric")
        expect(False, layout("fabric"), expected="software")
        # Every retired Linux image row is an independent refusal, and so are
        # the retired manifests, even with the fabric owner recorded.
        for row_name in RETIRED_LINUX_IMAGES:
            expect(False, layout(
                "fabric", extra_rows=({"name": row_name, "offset": 0x500000,
                                       "budget": 0x1000},),
                name=f"retired-{row_name}.json"))
        for manifest in RETIRED_MANIFESTS:
            expect(False, layout("fabric", manifest=manifest,
                                 name=f"retired-{manifest}.json"))
        # [R-parallel] on #228: the exact reproduction this tool approved,
        # {manifest: 'not-baremetal', fabric owner, cpu_xlen, no rows}, and
        # each exact-set refusal beside it: the manifest must be exactly
        # 'baremetal' and the rows exactly {bitstream, aem}.
        repro = os.path.join(temp, "repro-not-baremetal.json")
        with open(repro, "w", encoding="utf-8") as stream:
            json.dump({"manifest": "not-baremetal", "gptp_owner": "fabric",
                       "cpu_xlen": 32, "images": []}, stream)
        expect(False, repro)
        expect(False, layout("fabric", manifest=None,
                             name="manifest-missing.json"))
        expect(False, layout("fabric", manifest="Baremetal",
                             name="manifest-case.json"))
        expect(False, layout("fabric", rows="empty", name="no-rows.json"))
        expect(False, layout("fabric", rows="no-aem", name="no-aem.json"))
        expect(False, layout("fabric", rows="no-bitstream",
                             name="no-bitstream.json"))
        expect(False, layout("fabric",
                             extra_rows=({"name": "extra",
                                          "offset": 0x500000,
                                          "budget": 0x1000},),
                             name="surplus-row.json"))
        # Malformed layouts stay refusals, never crashes.
        expect(False, layout("fabric", extra_rows=({"name": "aem",
                                                    "offset": 0x600000},),
                             name="duplicate-aem.json"))
        broken = os.path.join(temp, "broken.json")
        with open(broken, "w", encoding="utf-8") as stream:
            stream.write("{not json")
        expect(False, broken)

        # Bitstream binding arms: the exact parsed payload digest and FPGA
        # part must hold, and a part mismatch against the programmer refuses.
        paired = os.path.join(temp, "paired")
        os.makedirs(os.path.join(paired, "gateware"))
        paired_bit = os.path.join(paired, "gateware", "board.bit")
        _fake_bit(paired_bit, b"\xff" * 16 + b"\xaa\x99\x55\x66paired")
        paired_layout = os.path.join(paired, "flashboot_layout.json")
        body = {"gptp_owner": "fabric", "manifest": "baremetal",
                "images": [
                    {"name": "bitstream", "offset": 0, "budget": 0x400000},
                    {"name": "aem", "offset": 0x400000, "budget": 0x10000},
                ]}
        body.update(bitstream_binding(paired_bit))
        with open(paired_layout, "w", encoding="utf-8") as stream:
            json.dump(body, stream)
        expect(True, paired_layout, bit=paired_bit, part="xc7a100tfgg484")
        expect(False, paired_layout, bit=paired_bit, part="xc7a200tfbg484")
        expect(False, paired_layout, part="xc7a100tfgg484")
        expect(False, layout("fabric"), bit=paired_bit,
               part="xc7a100tfgg484")
        corrupt_bit = os.path.join(paired, "gateware", "corrupt.bit")
        with open(corrupt_bit, "wb") as stream:
            stream.write(b"not a Xilinx bitstream")
        expect(False, paired_layout, bit=corrupt_bit, part="xc7a100tfgg484")
        adjacent_bit = os.path.join(paired, "gateware", "other-owner.bit")
        _fake_bit(adjacent_bit, b"\xff" * 16 + b"\xaa\x99\x55\x66other")
        expect(False, paired_layout, bit=adjacent_bit, part="xc7a100tfgg484")

        # The retired rootfs argument is an argparse REFUSAL, not an ignored
        # input: a caller still holding the pre-#259 pairing contract must
        # learn it here rather than flash unpaired.
        checks += 1
        rc = main(["--layout", paired_layout, "--rootfs", "any.cpio"])
        if rc == 0:
            raise AssertionError("--rootfs was accepted; the retired Linux "
                                 "pairing role must be refused")

    print(f"[gptp-owner] self-test: {checks}/{checks} checks pass")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout")
    parser.add_argument("--expected-owner", choices=OWNERS)
    parser.add_argument("--bit")
    parser.add_argument("--expected-fpga-part")
    parser.add_argument("--self-test", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse exits 2 on unknown arguments (--rootfs included); keep
        # that as a plain refusal code for scripted callers.
        return exc.code if isinstance(exc.code, int) else 2
    if args.self_test:
        self_test()
        return 0
    if not args.layout:
        parser.error("--layout is required")
    try:
        owner, detail = check_pair(
            args.layout, args.expected_owner,
            args.bit, args.expected_fpga_part)
    except ContractError as exc:
        print(f"[gptp-owner] REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"[gptp-owner] OK: gateware owner={owner}; {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
