#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Plan and identify power-fail-bounded gPTP-owner QSPI transitions.

The installed owner is not an operator assertion.  It is the owner recorded by
the layout whose SHA-256 and FPGA-part binding matches an exact parsed Xilinx
``.bit`` configuration payload, after that payload has also been matched
against a live offset-zero QSPI dump.  For a full-Linux source,
``deploy.sh flash-pair`` additionally verifies
the FBI CRC and owner marker in the live installed rootfs.  This module keeps
the bit parsing, profile restrictions, ordering decision and readback
classification testable without a programmer.

The guarantee is deliberately bounded at completed, verified programmer-write
boundaries.  A torn erase/program of the single offset-zero bitstream itself
needs an A/B or MultiBoot layout and cannot be repaired by shell ordering.
"""

import argparse
import hashlib
import json
import os
import re
import struct
import sys
import tempfile

from gptp_owner_contract import GPTP_OWNERS


class TransitionError(RuntimeError):
    """The requested transition cannot preserve the owner invariant."""


def _take(raw, pos, count, label):
    end = pos + count
    if count < 0 or end > len(raw):
        raise TransitionError(f"truncated Xilinx .bit {label}")
    return raw[pos:end], end


def bit_info(path):
    """Return (payload, part) as parsed by openFPGALoader's .bit path."""
    try:
        with open(path, "rb") as stream:
            raw = stream.read()
    except OSError as exc:
        raise TransitionError(f"cannot read bitstream {path}: {exc}") from exc

    try:
        first_len = struct.unpack_from(">H", raw, 0)[0]
    except struct.error as exc:
        raise TransitionError("truncated Xilinx .bit initial header") from exc
    _unused, pos = _take(raw, 2, first_len, "initial header")

    prefix, pos = _take(raw, pos, 2, "field prefix")
    if struct.unpack(">H", prefix)[0] != 1:
        raise TransitionError("invalid Xilinx .bit field prefix")

    seen = set()
    fields = {}
    while True:
        type_raw, pos = _take(raw, pos, 1, "field type")
        field_type = type_raw[0]
        if field_type in seen:
            raise TransitionError(
                f"duplicate Xilinx .bit field {chr(field_type)!r}")
        seen.add(field_type)
        if field_type == ord("e"):
            length_raw, pos = _take(raw, pos, 4, "payload length")
            length = struct.unpack(">I", length_raw)[0]
            if length <= 0:
                raise TransitionError("empty Xilinx .bit payload")
            payload, _ = _take(raw, pos, length, "payload")
            # A Xilinx configuration stream contains the bus-width/sync word;
            # requiring it stops an arbitrary file with a forged header from
            # becoming installed-owner evidence.
            if b"\xaa\x99\x55\x66" not in payload[:4096]:
                raise TransitionError(
                    "Xilinx .bit payload has no configuration sync word")
            try:
                part = fields[ord("b")].rstrip(b"\0").decode("ascii")
            except (KeyError, UnicodeError) as exc:
                raise TransitionError(
                    "Xilinx .bit has no ASCII FPGA part field") from exc
            if not part:
                raise TransitionError("Xilinx .bit FPGA part field is empty")
            return payload, part
        if field_type not in b"abcd":
            raise TransitionError(
                f"unknown Xilinx .bit field type 0x{field_type:02x}")
        length_raw, pos = _take(raw, pos, 2, "field length")
        length = struct.unpack(">H", length_raw)[0]
        value, pos = _take(raw, pos, length, "field value")
        fields[field_type] = value


def bit_payload(path):
    """Return the exact bytes openFPGALoader v1.1.1 writes for a .bit file."""
    return bit_info(path)[0]


def bitstream_binding(path):
    """Return the immutable layout fields that bind one parsed .bit payload."""
    payload, part = bit_info(path)
    return {
        "bitstream_payload_sha256": hashlib.sha256(payload).hexdigest(),
        "bitstream_fpga_part": part,
    }


def _load_layout(path):
    try:
        with open(path, encoding="utf-8") as stream:
            layout = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TransitionError(f"cannot read layout {path}: {exc}") from exc
    if not isinstance(layout, dict):
        raise TransitionError("layout root must be an object")
    owner = layout.get("gptp_owner")
    if owner not in GPTP_OWNERS:
        raise TransitionError("layout has no valid gptp_owner enum")
    images = layout.get("images")
    if not isinstance(images, list) or any(not isinstance(row, dict)
                                           for row in images):
        raise TransitionError("layout images must be a list of objects")
    names = [row.get("name") for row in images]
    if any(not isinstance(name, str) or not name for name in names):
        raise TransitionError("every layout image needs a non-empty name")
    if len(names) != len(set(names)):
        raise TransitionError("layout contains duplicate image names")
    return layout


def _profile(layout, label):
    owner = layout["gptp_owner"]
    names = {row["name"] for row in layout["images"]}
    manifest = layout.get("manifest")
    if owner == "fabric":
        if manifest == "baremetal" and names == {"bitstream", "aem"}:
            return owner, "baremetal"
        full = {"bitstream", "kernel", "opensbi", "dtb", "rootfs"}
        if (manifest == "full" and layout.get("complete") is True
                and names == full):
            # Fabric gPTP is autonomous even when Linux is the boot payload;
            # the paired rootfs is unmarked and starts no linuxptp owner.
            return owner, "linux"
        raise TransitionError(
            f"{label} fabric owner is neither an autonomous baremetal nor complete full-Linux image set")
    if owner == "software":
        wanted = {"bitstream", "kernel", "opensbi", "dtb", "rootfs"}
        if (manifest != "full" or layout.get("complete") is not True
                or names != wanted):
            raise TransitionError(
                f"{label} software owner is not a complete full-Linux image set")
        return owner, "linux"
    raise TransitionError(f"{label} owner {owner!r} is not an exact-one profile")


def _bound_payload(layout_path, bit_path, label):
    # Resolve the artifacts themselves, not only their containing spelling: a
    # gateware/foo.bit symlink to another build must not satisfy same-build
    # identity merely because the link was placed under the target directory.
    layout_dir = os.path.dirname(os.path.realpath(layout_path))
    bit_dir = os.path.dirname(os.path.dirname(os.path.realpath(bit_path)))
    if layout_dir != bit_dir:
        raise TransitionError(
            f"{label} BIT and LAYOUT are from different build directories")
    layout = _load_layout(layout_path)
    bit_rows = [row for row in layout["images"]
                if row.get("name") == "bitstream"]
    if len(bit_rows) != 1 or bit_rows[0].get("offset") != 0:
        raise TransitionError(f"{label} layout needs one bitstream at offset zero")
    budget = bit_rows[0].get("budget", bit_rows[0].get("size"))
    if not isinstance(budget, int) or budget <= 0:
        raise TransitionError(f"{label} bitstream has no positive slot budget")
    payload, part = bit_info(bit_path)
    if len(payload) > budget:
        raise TransitionError(
            f"{label} bitstream payload {len(payload)} B exceeds {budget} B slot")
    wanted_digest = layout.get("bitstream_payload_sha256")
    if (not isinstance(wanted_digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", wanted_digest) is None):
        raise TransitionError(
            f"{label} layout has no valid bitstream payload SHA-256 binding")
    got_digest = hashlib.sha256(payload).hexdigest()
    if got_digest != wanted_digest:
        raise TransitionError(
            f"{label} bitstream payload SHA-256 {got_digest} differs from "
            f"layout binding {wanted_digest}")
    wanted_part = layout.get("bitstream_fpga_part")
    if not isinstance(wanted_part, str) or not wanted_part.strip():
        raise TransitionError(
            f"{label} layout has no valid bitstream FPGA part binding")
    if _normal_part(part) != _normal_part(wanted_part):
        raise TransitionError(
            f"{label} bitstream FPGA part {part!r} differs from layout binding "
            f"{wanted_part!r}")
    return layout, payload, part


def _normal_part(part):
    value = part.strip().lower().replace("-", "")
    return value[2:] if value.startswith("xc") else value


def validate_artifact_pair(layout_path, bit_path, expected_fpga_part=None):
    """Bind one layout to the SHA-256 and part of its Xilinx bitstream."""
    layout, payload, part = _bound_payload(layout_path, bit_path, "artifact")
    if (expected_fpga_part is not None and
            _normal_part(part) != _normal_part(expected_fpga_part)):
        raise TransitionError(
            f"artifact FPGA part {part!r} differs from expected programmer part "
            f"{expected_fpga_part!r}")
    return {
        "owner": layout["gptp_owner"],
        "part": part,
        "payload_bytes": len(payload),
    }


def plan(installed_layout, installed_bit, target_layout, target_bit,
         expected_target_owner=None, expected_fpga_part=None):
    """Return source owner, target owner, ordering and readback byte count."""
    old_layout, old_payload, old_part = _bound_payload(
        installed_layout, installed_bit, "installed")
    new_layout, new_payload, new_part = _bound_payload(
        target_layout, target_bit, "target")
    if _normal_part(old_part) != _normal_part(new_part):
        raise TransitionError(
            f"installed FPGA part {old_part!r} differs from target {new_part!r}")
    if (expected_fpga_part is not None and
            _normal_part(new_part) != _normal_part(expected_fpga_part)):
        raise TransitionError(
            f"target FPGA part {new_part!r} differs from programmer part "
            f"{expected_fpga_part!r}")
    old_owner, old_boot = _profile(old_layout, "installed")
    new_owner, new_boot = _profile(new_layout, "target")
    if expected_target_owner is not None and new_owner != expected_target_owner:
        raise TransitionError(
            f"target owner is {new_owner!r}, selected recipe expects "
            f"{expected_target_owner!r}")
    if old_payload == new_payload:
        raise TransitionError(
            "installed and target bitstream payloads are identical; live state is ambiguous")
    # A full-Linux owner change also flips the rootfs permission marker.  With
    # one rootfs slot, writing the bit first produces fabric+marked (two
    # owners), while writing the rootfs first produces software+unmarked (zero
    # owners).  The autonomous fabric/baremetal image is the safe bridge in
    # either direction; do not pretend bit ordering alone solves this case.
    if old_owner != new_owner and (
            (old_owner == "fabric" and old_boot == "linux") or
            (new_owner == "fabric" and new_boot == "linux")):
        raise TransitionError(
            "direct fabric/full-Linux and software/full-Linux owner changes "
            "need a fabric/baremetal bridge")
    if old_owner == "software" and new_owner == "software":
        raise TransitionError(
            "software-to-software persistent refresh has no safe single-slot order")
    if old_owner == "software" and new_owner == "fabric":
        order = "bit-first"
    else:
        # fabric->software and fabric->fabric both keep the old autonomous
        # fabric owner until every target non-bit image has verified.
        order = "images-first"
    return {
        "installed_owner": old_owner,
        "installed_profile": f"{old_owner}-{old_boot}",
        "target_owner": new_owner,
        "target_profile": f"{new_owner}-{new_boot}",
        "order": order,
        "dump_bytes": max(len(old_payload), len(new_payload)),
        "installed_payload_bytes": len(old_payload),
        "target_payload_bytes": len(new_payload),
    }


def identify(dump_path, installed_bit, target_bit, expected_size=None):
    """Classify a live QSPI dump as the exact installed or target payload."""
    old_payload = bit_payload(installed_bit)
    new_payload = bit_payload(target_bit)
    try:
        with open(dump_path, "rb") as stream:
            live = stream.read()
    except OSError as exc:
        raise TransitionError(f"cannot read QSPI dump {dump_path}: {exc}") from exc
    wanted = expected_size if expected_size is not None else max(
        len(old_payload), len(new_payload))
    if len(live) != wanted:
        raise TransitionError(
            f"QSPI dump is {len(live)} B, expected exactly {wanted} B")
    matches = []
    if live[:len(old_payload)] == old_payload:
        matches.append("installed")
    if live[:len(new_payload)] == new_payload:
        matches.append("target")
    if len(matches) != 1:
        state = "neither" if not matches else "both"
        raise TransitionError(
            f"live QSPI bitstream matches {state} supplied artifact(s)")
    return matches[0]


def _fake_bit(path, payload, title=b"fixture", part=b"7a100tfgg484\0"):
    raw = bytearray(struct.pack(">H", 1) + b"X" + struct.pack(">H", 1))
    raw += b"a" + struct.pack(">H", len(title)) + title
    raw += b"b" + struct.pack(">H", len(part)) + part
    raw += b"e" + struct.pack(">I", len(payload)) + payload
    with open(path, "wb") as stream:
        stream.write(raw)


def self_test():
    checks = 0

    def expect_error(fn, needle=None):
        nonlocal checks
        checks += 1
        try:
            fn()
        except TransitionError as exc:
            if needle is not None and needle not in str(exc):
                raise AssertionError(f"{needle!r} not in {str(exc)!r}")
        else:
            raise AssertionError("transition unexpectedly accepted")

    with tempfile.TemporaryDirectory() as temp:
        def build(name, owner, manifest, complete, payload, names):
            root = os.path.join(temp, name)
            os.makedirs(os.path.join(root, "gateware"))
            bit = os.path.join(root, "gateware", "board.bit")
            layout = os.path.join(root, "flashboot_layout.json")
            _fake_bit(bit, b"\xff" * 16 + b"\xaa\x99\x55\x66" + payload)
            rows = [{"name": n, "offset": 0 if n == "bitstream" else
                     0x400000 + i * 0x10000, "budget": 0x400000}
                    for i, n in enumerate(names)]
            body = {"gptp_owner": owner, "manifest": manifest,
                    "complete": complete, "images": rows}
            body.update(bitstream_binding(bit))
            with open(layout, "w", encoding="utf-8") as stream:
                json.dump(body, stream)
            return layout, bit

        fab = build("fab", "fabric", "baremetal", False, b"fabric",
                    ["bitstream", "aem"])
        sw = build("sw", "software", "full", True, b"software",
                   ["bitstream", "kernel", "opensbi", "dtb", "rootfs"])
        sw2 = build("sw2", "software", "full", True, b"software2",
                    ["bitstream", "kernel", "opensbi", "dtb", "rootfs"])
        fab_linux = build(
            "fab-linux", "fabric", "full", True, b"fabric-linux",
            ["bitstream", "kernel", "opensbi", "dtb", "rootfs"])
        fab2 = build("fab2", "fabric", "baremetal", False, b"fabric2",
                     ["bitstream", "aem"])
        partial = build("partial", "software", "kernel", False, b"partial",
                        ["bitstream", "kernel"])

        assert plan(*fab, *sw)["order"] == "images-first"; checks += 1
        assert plan(*sw, *fab)["order"] == "bit-first"; checks += 1
        assert plan(*fab, *fab2)["order"] == "images-first"; checks += 1
        expect_error(lambda: plan(*fab_linux, *sw), "fabric/baremetal bridge")
        expect_error(lambda: plan(*sw, *fab_linux), "fabric/baremetal bridge")
        assert plan(*fab, *fab_linux)["order"] == "images-first"; checks += 1
        expect_error(lambda: plan(*sw, *partial), "complete full-Linux")
        expect_error(lambda: plan(*sw, *sw), "identical")
        expect_error(lambda: plan(*sw, *sw2), "software-to-software")
        expect_error(lambda: plan(*sw, *fab, expected_target_owner="software"),
                     "selected recipe expects")
        expect_error(lambda: plan(*sw, *fab,
                                  expected_fpga_part="xc7a200tfbg484"),
                     "programmer part")
        foreign_link = os.path.join(
            os.path.dirname(fab2[1]), "foreign-build.bit")
        os.symlink(sw[1], foreign_link)
        expect_error(lambda: validate_artifact_pair(
            fab2[0], foreign_link), "different build directories")
        # This is the installed-owner trust seam: a valid bit copied beside a
        # different build's mutable layout used to satisfy the directory test
        # and inherit that layout's owner.  The payload digest must reject it.
        adjacent_wrong = os.path.join(os.path.dirname(fab2[1]),
                                      "adjacent-software.bit")
        with open(sw[1], "rb") as source, open(adjacent_wrong, "wb") as sink:
            sink.write(source.read())
        expect_error(lambda: validate_artifact_pair(
            fab2[0], adjacent_wrong), "payload SHA-256")

        unbound = build("unbound", "fabric", "baremetal", False, b"unbound",
                        ["bitstream", "aem"])
        with open(unbound[0], encoding="utf-8") as stream:
            unbound_layout = json.load(stream)
        del unbound_layout["bitstream_payload_sha256"]
        with open(unbound[0], "w", encoding="utf-8") as stream:
            json.dump(unbound_layout, stream)
        expect_error(lambda: validate_artifact_pair(*unbound),
                     "no valid bitstream payload SHA-256")

        wrong_part = build("wrong-part", "fabric", "baremetal", False,
                           b"wrong-part", ["bitstream", "aem"])
        with open(wrong_part[0], encoding="utf-8") as stream:
            wrong_part_layout = json.load(stream)
        wrong_part_layout["bitstream_fpga_part"] = "xc7a200tfbg484"
        with open(wrong_part[0], "w", encoding="utf-8") as stream:
            json.dump(wrong_part_layout, stream)
        expect_error(lambda: validate_artifact_pair(*wrong_part),
                     "differs from layout binding")

        live = os.path.join(temp, "qspi.bin")
        old_payload = bit_payload(fab[1])
        new_payload = bit_payload(sw[1])
        size = max(len(old_payload), len(new_payload))
        with open(live, "wb") as stream:
            stream.write(old_payload + b"\xff" * (size - len(old_payload)))
        assert identify(live, fab[1], sw[1], size) == "installed"; checks += 1
        with open(live, "wb") as stream:
            stream.write(new_payload + b"\xff" * (size - len(new_payload)))
        assert identify(live, fab[1], sw[1], size) == "target"; checks += 1
        with open(live, "wb") as stream:
            stream.write(b"\x00" * size)
        expect_error(lambda: identify(live, fab[1], sw[1], size), "neither")
        with open(live, "wb") as stream:
            stream.write(b"\x00" * (size - 1))
        expect_error(lambda: identify(live, fab[1], sw[1], size), "expected exactly")

        corrupt = os.path.join(temp, "corrupt.bit")
        with open(corrupt, "wb") as stream:
            stream.write(b"not a bitstream")
        expect_error(lambda: bit_payload(corrupt), "truncated")

    print(f"qspi owner transition self-test: {checks}/{checks} checks pass")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    sub = parser.add_subparsers(dest="command")
    p_plan = sub.add_parser("plan")
    p_plan.add_argument("--installed-layout", required=True)
    p_plan.add_argument("--installed-bit", required=True)
    p_plan.add_argument("--target-layout", required=True)
    p_plan.add_argument("--target-bit", required=True)
    p_plan.add_argument("--expected-target-owner")
    p_plan.add_argument("--expected-fpga-part")
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--layout", required=True)
    p_validate.add_argument("--bit", required=True)
    p_validate.add_argument("--expected-fpga-part")
    p_ident = sub.add_parser("identify")
    p_ident.add_argument("--dump", required=True)
    p_ident.add_argument("--installed-bit", required=True)
    p_ident.add_argument("--target-bit", required=True)
    p_ident.add_argument("--expected-size", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            self_test()
            return 0
        if args.command == "plan":
            result = plan(args.installed_layout, args.installed_bit,
                          args.target_layout, args.target_bit,
                          args.expected_target_owner, args.expected_fpga_part)
            print("\t".join(str(result[key]) for key in (
                "installed_owner", "installed_profile", "target_owner",
                "order", "dump_bytes", "target_profile")))
            return 0
        if args.command == "validate":
            result = validate_artifact_pair(
                args.layout, args.bit, args.expected_fpga_part)
            print("\t".join(str(result[key]) for key in (
                "owner", "part", "payload_bytes")))
            return 0
        if args.command == "identify":
            print(identify(args.dump, args.installed_bit, args.target_bit,
                           args.expected_size))
            return 0
        parser.error("choose plan, validate, identify, or --self-test")
    except TransitionError as exc:
        print(f"qspi owner transition REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
