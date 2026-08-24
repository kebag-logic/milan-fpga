#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Fail-closed gateware/rootfs gPTP-owner artifact check.

The gateware build records its resolved owner in flashboot_layout.json.  A
Linux rootfs grants the software owner permission with exactly one regular
``etc/milan-gptp-software-owner`` entry.  This checker reads gzip/xz/raw newc
archives with the Python standard library so deploy hosts and CI do not need
cpio/libarchive just to enforce the pairing contract.
"""

import argparse
import gzip
import json
import lzma
import os
import stat
import sys
import tempfile

from gptp_owner_contract import GPTP_OWNERS

OWNERS = GPTP_OWNERS
MARKER = b"etc/milan-gptp-software-owner"
NEWC_MAGICS = (b"070701", b"070702")


class ContractError(RuntimeError):
    pass


def _read_exact(stream, count, label):
    chunks = []
    left = count
    while left:
        chunk = stream.read(left)
        if not chunk:
            raise ContractError(f"truncated cpio while reading {label}")
        chunks.append(chunk)
        left -= len(chunk)
    return b"".join(chunks)


def _consume(stream, count, checksum=False):
    total = 0
    left = count
    while left:
        chunk = stream.read(min(left, 1024 * 1024))
        if not chunk:
            raise ContractError("truncated cpio file payload")
        if checksum:
            total = (total + sum(chunk)) & 0xFFFF_FFFF
        left -= len(chunk)
    return total


def _normal_name(name):
    if name.startswith(b"/"):
        raise ContractError("absolute path in rootfs cpio")
    parts = []
    for part in name.split(b"/"):
        if part in (b"", b"."):
            continue
        if part == b"..":
            raise ContractError("parent traversal in rootfs cpio path")
        parts.append(part)
    return b"/".join(parts)


def _archive_stream(path):
    try:
        with open(path, "rb") as source:
            prefix = source.read(6)
    except OSError as exc:
        raise ContractError(f"cannot read rootfs {path}: {exc}") from exc
    if prefix.startswith(b"\xfd7zXZ\x00"):
        return lzma.open(path, "rb"), "xz"
    if prefix.startswith(b"\x1f\x8b"):
        return gzip.open(path, "rb"), "gzip"
    if prefix in NEWC_MAGICS:
        return open(path, "rb"), "raw newc"
    raise ContractError(
        "unsupported rootfs archive (need raw newc, .cpio.gz, or .cpio.xz)")


def marker_rows(path):
    """Return mode values for exact normalized marker entries."""
    stream, encoding = _archive_stream(path)
    rows = []
    try:
        while True:
            header = _read_exact(stream, 110, "newc header")
            magic = header[:6]
            if magic not in NEWC_MAGICS:
                raise ContractError(
                    f"unsupported/corrupt cpio header magic {magic!r}")
            try:
                fields = [int(header[6 + 8 * i:14 + 8 * i], 16)
                          for i in range(13)]
            except ValueError as exc:
                raise ContractError("non-hex field in cpio newc header") from exc
            mode, size, namesize, wanted_sum = (
                fields[1], fields[6], fields[11], fields[12])
            if namesize < 1 or namesize > 1024 * 1024:
                raise ContractError(f"invalid cpio name size {namesize}")
            raw_name = _read_exact(stream, namesize, "cpio name")
            if raw_name[-1:] != b"\0":
                raise ContractError("cpio name is not NUL terminated")
            name = _normal_name(raw_name[:-1])
            _consume(stream, (-(110 + namesize)) & 3)
            got_sum = _consume(stream, size, checksum=(magic == b"070702"))
            _consume(stream, (-size) & 3)
            if magic == b"070702" and got_sum != wanted_sum:
                raise ContractError(
                    f"cpio CRC mismatch for {name!r}: {got_sum:#x} != "
                    f"{wanted_sum:#x}")
            if name == MARKER:
                rows.append(mode)
            if name == b"TRAILER!!!":
                if size:
                    raise ContractError("cpio trailer carries a payload")
                trailing = stream.read()
                if any(trailing):
                    raise ContractError("non-padding data follows cpio trailer")
                break
    except ContractError:
        raise
    except (EOFError, OSError, lzma.LZMAError) as exc:
        raise ContractError(f"corrupt {encoding} rootfs archive: {exc}") from exc
    finally:
        stream.close()
    return rows


def _load_layout(path):
    try:
        with open(path, encoding="utf-8") as stream:
            layout = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read layout {path}: {exc}") from exc
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
    return layout, owner


def check_pair(layout_path, rootfs_path=None, expected_owner=None):
    layout, owner = _load_layout(layout_path)
    if expected_owner is not None and owner != expected_owner:
        raise ContractError(
            f"layout owner is {owner!r}, selected build expects "
            f"{expected_owner!r}")

    has_rootfs = any(row.get("name") == "rootfs"
                     for row in layout["images"])
    # A software owner always runs from Linux, including the supported partial
    # `kernel` layout whose rootfs arrives later over serialboot.  It still has
    # to name that exact archive here; otherwise the flash operation would
    # certify only half of the one-owner boot set.
    needs_rootfs_check = has_rootfs or owner == "software"
    if not needs_rootfs_check:
        return owner, "layout carries no rootfs image"
    if not rootfs_path:
        reason = ("layout carries rootfs" if has_rootfs
                  else "software-owned partial layout still boots a serial rootfs")
        raise ContractError(
            f"{reason}, but ROOTFS was not supplied for owner pairing")

    rows = marker_rows(rootfs_path)
    if len(rows) > 1:
        raise ContractError(
            f"rootfs contains {len(rows)} software-owner marker entries; want exactly one or zero")
    if rows and not stat.S_ISREG(rows[0]):
        raise ContractError("rootfs software-owner marker is not a regular file")
    marked = len(rows) == 1
    want_marked = owner == "software"
    if marked != want_marked:
        state = "present" if marked else "absent"
        wanted = "present" if want_marked else "absent"
        raise ContractError(
            f"rootfs software-owner marker is {state}, but gateware owner "
            f"{owner!r} requires it {wanted}")
    return owner, f"rootfs marker {'present' if marked else 'absent'}"


def _newc(entries):
    """Tiny deterministic newc writer used only by --self-test."""
    out = bytearray()
    ino = 1
    rows = list(entries) + [(b"TRAILER!!!", b"", stat.S_IFREG)]
    for name, payload, mode in rows:
        raw_name = name + b"\0"
        fields = (ino, mode | 0o644, 0, 0, 1, 0, len(payload),
                  0, 0, 0, 0, len(raw_name), 0)
        out.extend(b"070701" + b"".join(f"{value:08x}".encode()
                                         for value in fields))
        out.extend(raw_name)
        out.extend(b"\0" * ((-len(out)) & 3))
        out.extend(payload)
        out.extend(b"\0" * ((-len(out)) & 3))
        ino += 1
    out.extend(b"\0" * ((-len(out)) & 511))
    return bytes(out)


def self_test():
    checks = 0

    def expect(ok, layout, rootfs=None, expected=None):
        nonlocal checks
        checks += 1
        try:
            check_pair(layout, rootfs, expected)
        except ContractError:
            if ok:
                raise
        else:
            if not ok:
                raise AssertionError("owner mismatch unexpectedly passed")

    with tempfile.TemporaryDirectory() as temp:
        archives = {}
        for marked in (False, True):
            entries = [(b"etc/hostname", b"milan\n", stat.S_IFREG)]
            if marked:
                entries.append((b"./etc/milan-gptp-software-owner",
                                b"explicit option-OFF\n", stat.S_IFREG))
            raw = _newc(entries)
            for suffix, data in (("cpio", raw),
                                 ("cpio.gz", gzip.compress(raw)),
                                 ("cpio.xz", lzma.compress(raw))):
                path = os.path.join(temp, f"{'marked' if marked else 'plain'}.{suffix}")
                with open(path, "wb") as stream:
                    stream.write(data)
                archives[marked, suffix] = path

        def layout(owner, key=True):
            path = os.path.join(temp, f"layout-{owner}-{key}.json")
            body = {"images": [{"name": "rootfs", "offset": 1}]}
            if key:
                body["gptp_owner"] = owner
            with open(path, "w", encoding="utf-8") as stream:
                json.dump(body, stream)
            return path

        for suffix in ("cpio", "cpio.gz", "cpio.xz"):
            expect(True, layout("software"), archives[True, suffix])
            expect(True, layout("fabric"), archives[False, suffix])
            expect(True, layout("none"), archives[False, suffix])
            expect(False, layout("software"), archives[False, suffix])
            expect(False, layout("fabric"), archives[True, suffix])
            expect(False, layout("none"), archives[True, suffix])

        expect(False, layout("fabric"), None)
        expect(False, layout("fabric", key=False), archives[False, "cpio.xz"])
        expect(False, layout("unknown"), archives[False, "cpio.xz"])
        expect(False, layout("fabric"), archives[False, "cpio.xz"], "software")

        corrupt = os.path.join(temp, "corrupt.cpio.xz")
        with open(corrupt, "wb") as stream:
            stream.write(lzma.compress(_newc([]))[:-5])
        expect(False, layout("fabric"), corrupt)
        unsupported = os.path.join(temp, "rootfs.ext4")
        with open(unsupported, "wb") as stream:
            stream.write(b"not a cpio archive")
        expect(False, layout("fabric"), unsupported)

        duplicate = _newc([
            (MARKER, b"one", stat.S_IFREG),
            (b"./etc//milan-gptp-software-owner", b"two", stat.S_IFREG),
        ])
        duplicate_path = os.path.join(temp, "duplicate.cpio.gz")
        with open(duplicate_path, "wb") as stream:
            stream.write(gzip.compress(duplicate))
        expect(False, layout("software"), duplicate_path)

        wrong_type = os.path.join(temp, "directory-marker.cpio.xz")
        with open(wrong_type, "wb") as stream:
            stream.write(lzma.compress(_newc([
                (MARKER, b"", stat.S_IFDIR),
            ])))
        expect(False, layout("software"), wrong_type)

        unsafe = os.path.join(temp, "absolute-marker.cpio.gz")
        with open(unsafe, "wb") as stream:
            stream.write(gzip.compress(_newc([
                (b"/" + MARKER, b"lease", stat.S_IFREG),
            ])))
        expect(False, layout("software"), unsafe)

        duplicate_layout = os.path.join(temp, "layout-duplicate-images.json")
        with open(duplicate_layout, "w", encoding="utf-8") as stream:
            json.dump({"gptp_owner": "software", "images": [
                {"name": "rootfs"}, {"name": "rootfs"}]}, stream)
        expect(False, duplicate_layout, archives[True, "cpio.xz"])

        partial = os.path.join(temp, "layout-software-partial.json")
        with open(partial, "w", encoding="utf-8") as stream:
            json.dump({"gptp_owner": "software", "manifest": "kernel",
                       "images": [{"name": "kernel"}]}, stream)
        expect(False, partial)
        expect(True, partial, archives[True, "cpio.xz"])
        expect(False, partial, archives[False, "cpio.xz"])

        baremetal = os.path.join(temp, "layout-fabric-baremetal.json")
        with open(baremetal, "w", encoding="utf-8") as stream:
            json.dump({"gptp_owner": "fabric", "manifest": "baremetal",
                       "images": [{"name": "aem"}]}, stream)
        expect(True, baremetal)

    print(f"[gptp-owner] self-test: {checks}/{checks} checks pass")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout")
    parser.add_argument("--rootfs")
    parser.add_argument("--expected-owner", choices=OWNERS)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if not args.layout:
        parser.error("--layout is required")
    try:
        owner, detail = check_pair(
            args.layout, args.rootfs, args.expected_owner)
    except ContractError as exc:
        print(f"[gptp-owner] REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"[gptp-owner] OK: gateware owner={owner}; {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
