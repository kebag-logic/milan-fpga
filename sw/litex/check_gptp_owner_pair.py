#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Fail-closed gateware/rootfs gPTP-owner artifact check.

The gateware build records its resolved owner in flashboot_layout.json.  Every
supported Linux rootfs carries one positive, versioned owner profile; marker
absence never grants fabric ownership.  The software profile additionally
contains its permission marker and runnable linuxptp payload, while the fabric
profile must contain no linuxptp executable or boot/service launch reference.
This checker reads gzip/xz/raw newc archives with the Python standard library
so deploy hosts and CI do not need cpio/libarchive just to enforce the pairing
contract.
"""

import argparse
import binascii
import gzip
import io
import json
import lzma
import os
import re
import stat
import struct
import sys
import tempfile

from gptp_owner_contract import GPTP_OWNERS
from qspi_owner_transition import (TransitionError, bitstream_binding,
                                   validate_artifact_pair)

OWNERS = GPTP_OWNERS
PROFILE = b"etc/milan-gptp-owner-profile"
PROFILE_VERSION = b"milan-gptp-owner-profile-v1"
PROFILE_PAYLOADS = {
    owner: PROFILE_VERSION + b":" + owner.encode("ascii") + b"\n"
    for owner in ("fabric", "software")
}
SOFTWARE_MARKER = b"etc/milan-gptp-software-owner"
OWNER_INIT = b"etc/init.d/S65milan-gptp-owner"
SOFTWARE_EXECUTABLES = (
    b"usr/sbin/ptp4l",
    b"usr/sbin/phc2sys",
    b"usr/sbin/pmc",
    b"usr/sbin/ptp4l-rt",
)
SOFTWARE_FILES = (
    b"etc/gptp.cfg",
    b"etc/default/ptp4l",
    b"etc/default/phc2sys",
)
LINUXPTP_BASENAMES = (b"ptp4l", b"ptp4l-rt", b"phc2sys", b"pmc")
LAUNCHER_PREFIXES = (
    b"etc/init.d/",
    b"etc/rc.d/",
    b"etc/systemd/",
    b"etc/cron",
    b"etc/local.d/",
    b"lib/systemd/",
    b"usr/lib/systemd/",
)
LAUNCHER_PATHS = (b"etc/inittab", b"etc/rc.local")
MAX_INSPECT_PAYLOAD = 1024 * 1024
LINUXPTP_TOKEN_RE = re.compile(
    br"(?<![A-Za-z0-9_])(?:ptp4l(?:-rt)?|phc2sys|pmc)"
    br"(?![A-Za-z0-9_])", re.I)
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


def _launcher_path(name):
    """Paths whose contents can participate directly in boot/service launch."""
    return (name in LAUNCHER_PATHS
            or name.endswith((b".service", b".timer", b".socket"))
            or any(name.startswith(prefix) for prefix in LAUNCHER_PREFIXES))


def _payload(stream, size, magic, name, mode):
    """Consume one payload, retaining only owner and launcher semantics.

    Every small executable script is retained, even under a neutral path, so
    an init script cannot hide linuxptp behind `/usr/local/bin/start-clock`.
    Binary executables are discarded after their shebang probe; executable
    *names* are validated separately.  Known launcher records (including
    systemd units, which need no executable bit) are always retained.
    """
    checksum = magic == b"070702"
    inspect_path = name == PROFILE or _launcher_path(name)
    executable = stat.S_ISREG(mode) and bool(mode & 0o111)
    inspect = inspect_path or executable
    if inspect and size > MAX_INSPECT_PAYLOAD:
        if inspect_path:
            raise ContractError(
                f"rootfs launcher/profile {name!r} is too large to inspect "
                f"({size} > {MAX_INSPECT_PAYLOAD} bytes)")
        # Large native executables are not launcher text.  A large shebang
        # script is, and refusing it is safer than certifying uninspected boot
        # behavior.
        prefix = _read_exact(stream, min(size, 2), "executable payload probe")
        got_sum = sum(prefix) & 0xFFFF_FFFF
        if prefix == b"#!":
            raise ContractError(
                f"rootfs executable script {name!r} is too large to inspect")
        got_sum = (got_sum + _consume(
            stream, size - len(prefix), checksum=checksum)) & 0xFFFF_FFFF
        return None, got_sum
    if inspect:
        data = _read_exact(stream, size, "inspectable rootfs payload")
        got_sum = sum(data) & 0xFFFF_FFFF
        # Retain arbitrary data only for named launch records.  A small native
        # executable can contain the word ptp4l in symbols/help text without
        # being a launcher; its basename is still graded below.
        retained = data if inspect_path or data.startswith(b"#!") else None
        return retained, got_sum
    return None, _consume(stream, size, checksum=checksum)


def _archive_stream(path):
    try:
        with open(path, "rb") as source:
            raw = source.read()
    except OSError as exc:
        raise ContractError(f"cannot read rootfs {path}: {exc}") from exc

    payload = raw
    container = ""
    prefix = payload[:6]
    if not (prefix.startswith(b"\xfd7zXZ\x00")
            or prefix.startswith(b"\x1f\x8b")
            or prefix in NEWC_MAGICS):
        # Persistent QSPI stores Linux images as LiteX FBI records:
        # little-endian payload length, CRC32, then the archive.  Accept that
        # exact representation so flash-pair can prove the positive profile and
        # payload semantics in the live installed rootfs rather than trusting a
        # source-side assertion.
        if len(raw) < 8:
            raise ContractError(
                "unsupported rootfs archive (need raw newc, .cpio.gz, .cpio.xz, or an FBI-wrapped form)")
        size, wanted_crc = struct.unpack("<II", raw[:8])
        if size != len(raw) - 8:
            raise ContractError(
                f"invalid FBI rootfs length {size}; file carries {len(raw) - 8} payload bytes")
        payload = raw[8:]
        got_crc = binascii.crc32(payload) & 0xFFFF_FFFF
        if got_crc != wanted_crc:
            raise ContractError(
                f"FBI rootfs CRC mismatch: {got_crc:#x} != {wanted_crc:#x}")
        container = "FBI-wrapped "
        prefix = payload[:6]

    source = io.BytesIO(payload)
    if prefix.startswith(b"\xfd7zXZ\x00"):
        return lzma.LZMAFile(source, "rb"), container + "xz"
    if prefix.startswith(b"\x1f\x8b"):
        return gzip.GzipFile(fileobj=source, mode="rb"), container + "gzip"
    if prefix in NEWC_MAGICS:
        return source, container + "raw newc"
    raise ContractError(
        "unsupported rootfs payload (need raw newc, .cpio.gz, or .cpio.xz)")


def archive_entries(path):
    """Return normalized newc entries as ``name -> [(mode, payload)]``.

    Payload is retained for the small owner-profile record, boot/service
    records and executable scripts. Keeping every normalized name lets the
    profile check reject duplicate security-relevant paths and relocated
    linuxptp executables without extracting an untrusted archive.
    """
    stream, encoding = _archive_stream(path)
    entries = {}
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
            if name == PROFILE and size > 256:
                raise ContractError("rootfs owner profile is unreasonably large")
            payload, got_sum = _payload(stream, size, magic, name, mode)
            _consume(stream, (-size) & 3)
            if magic == b"070702" and got_sum != wanted_sum:
                raise ContractError(
                    f"cpio CRC mismatch for {name!r}: {got_sum:#x} != "
                    f"{wanted_sum:#x}")
            if name == b"TRAILER!!!":
                if size:
                    raise ContractError("cpio trailer carries a payload")
                trailing = stream.read()
                if any(trailing):
                    raise ContractError("non-padding data follows cpio trailer")
                break
            entries.setdefault(name, []).append((mode, payload))
    except ContractError:
        raise
    except (EOFError, OSError, lzma.LZMAError) as exc:
        raise ContractError(f"corrupt {encoding} rootfs archive: {exc}") from exc
    finally:
        stream.close()
    return entries


def _one_regular(entries, name, label, executable=False):
    rows = entries.get(name, [])
    if len(rows) != 1:
        raise ContractError(
            f"rootfs contains {len(rows)} {label} entries; want exactly one")
    mode, payload = rows[0]
    if not stat.S_ISREG(mode):
        raise ContractError(f"rootfs {label} is not a regular file")
    if executable and not mode & 0o111:
        raise ContractError(f"rootfs {label} is not executable")
    return payload


def _validate_rootfs_profile(entries, owner):
    if owner == "none":
        raise ContractError("gptp_owner 'none' cannot be paired with a Linux rootfs")

    payload = _one_regular(entries, PROFILE, "gPTP owner profile")
    wanted = PROFILE_PAYLOADS[owner]
    if payload != wanted:
        raise ContractError(
            f"rootfs gPTP owner profile is not exact versioned {owner!r} profile")

    _one_regular(entries, OWNER_INIT, "gPTP owner lifecycle", executable=True)

    # Canonical paths are necessary for the software profile, but a denylist
    # of those four paths is not sufficient for fabric ownership: Buildroot or
    # an overlay can relocate the exact same executable to usr/bin or opt. Name
    # every executable/symlink leaf independently of its directory. Software
    # may carry only its four canonical payload paths; fabric may carry none.
    allowed_tools = set(SOFTWARE_EXECUTABLES) if owner == "software" else set()
    for path, rows in entries.items():
        leaf = path.rsplit(b"/", 1)[-1].lower()
        linuxptp_leaf = any(
            leaf == name or leaf.startswith(name + b"-")
            or leaf.startswith(name + b".")
            for name in LINUXPTP_BASENAMES)
        # SysV/systemd launch records conventionally prefix/suffix the daemon
        # name (S65ptp4l, milan-ptp4l.service), so exact executable-leaf rules
        # alone are not enough for lifecycle filenames.
        linuxptp_leaf = linuxptp_leaf or (
            _launcher_path(path)
            and any(name in leaf for name in LINUXPTP_BASENAMES))
        for mode, payload in rows:
            executable_asset = (not stat.S_ISDIR(mode)
                                and (not stat.S_ISREG(mode)
                                     or bool(mode & 0o111)))
            if linuxptp_leaf and executable_asset and path not in allowed_tools:
                raise ContractError(
                    "rootfs contains relocated/extra linuxptp executable "
                    f"{path.decode('ascii', 'backslashreplace')}; "
                    "S65milan-gptp-owner must be sole lifecycle authority")

            # A neutral filename is not a neutral launcher. Scan every known
            # boot/service record and every executable script; for the software
            # profile only the one owner lifecycle is allowed to name tools.
            if payload is not None and LINUXPTP_TOKEN_RE.search(payload):
                if not (owner == "software" and path == OWNER_INIT):
                    raise ContractError(
                        "rootfs launcher/script outside the selected owner "
                        "lifecycle references linuxptp: "
                        f"{path.decode('ascii', 'backslashreplace')}")
    if owner == "software":
        _one_regular(entries, SOFTWARE_MARKER, "software-owner marker")
        for path in SOFTWARE_EXECUTABLES:
            _one_regular(entries, path, path.decode("ascii"), executable=True)
        for path in SOFTWARE_FILES:
            _one_regular(entries, path, path.decode("ascii"))
        return "versioned software profile with runnable linuxptp payload"

    forbidden = (SOFTWARE_MARKER,) + SOFTWARE_EXECUTABLES + SOFTWARE_FILES
    for path in forbidden:
        if path in entries:
            raise ContractError(
                f"fabric rootfs contains software-owner asset {path.decode('ascii')}")
    return ("versioned fabric profile without linuxptp executables or "
            "boot/service launch references")


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


def check_pair(layout_path, rootfs_path=None, expected_owner=None,
               bit_path=None, expected_fpga_part=None):
    layout, owner = _load_layout(layout_path)
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
            raise ContractError(f"layout/bitstream binding failed: {exc}") from exc
        if bound["owner"] != owner:
            raise ContractError("layout owner changed during bitstream binding")

    has_rootfs = any(row.get("name") == "rootfs"
                     for row in layout["images"])
    # A software owner always runs from Linux, including the supported partial
    # `kernel` layout whose rootfs arrives later over serialboot.  It still has
    # to name that exact archive here; otherwise the flash operation would
    # certify only half of the one-owner boot set.
    # A serialboot caller supplies a rootfs even when it is not a QSPI-layout
    # row.  Presence of that argument is itself a request to bind the archive;
    # ignoring an incompatible rootfs merely because manifest=none/kernel
    # would recreate the two-owner bypass this checker exists to prevent.
    needs_rootfs_check = (rootfs_path is not None or has_rootfs
                          or owner == "software")
    if not needs_rootfs_check:
        return owner, "layout carries no rootfs image"
    if not rootfs_path:
        reason = ("layout carries rootfs" if has_rootfs
                  else "software-owned partial layout still boots a serial rootfs")
        raise ContractError(
            f"{reason}, but ROOTFS was not supplied for owner pairing")

    detail = _validate_rootfs_profile(archive_entries(rootfs_path), owner)
    return owner, detail


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


def _profile_entries(owner):
    """Return a minimal semantically complete rootfs profile for tests."""
    if owner not in PROFILE_PAYLOADS:
        raise ValueError(f"no Linux rootfs profile for owner {owner!r}")
    rows = [
        (b"etc/hostname", b"milan\n", stat.S_IFREG),
        (PROFILE, PROFILE_PAYLOADS[owner], stat.S_IFREG),
        (OWNER_INIT, b"#!/bin/sh\n", stat.S_IFREG | 0o111),
    ]
    if owner == "software":
        rows.append((SOFTWARE_MARKER, b"explicit option-OFF\n",
                     stat.S_IFREG))
        rows.extend((path, b"tool", stat.S_IFREG | 0o111)
                    for path in SOFTWARE_EXECUTABLES)
        rows.extend((path, b"config\n", stat.S_IFREG)
                    for path in SOFTWARE_FILES)
    return rows


def self_test():
    checks = 0

    def expect(ok, layout, rootfs=None, expected=None, bit=None, part=None):
        nonlocal checks
        checks += 1
        try:
            check_pair(layout, rootfs, expected, bit, part)
        except ContractError:
            if ok:
                raise
        else:
            if not ok:
                raise AssertionError("owner mismatch unexpectedly passed")

    with tempfile.TemporaryDirectory() as temp:
        def write_archive(name, entries, suffix="cpio.xz"):
            raw = _newc(entries)
            if suffix == "cpio.gz":
                raw = gzip.compress(raw)
            elif suffix == "cpio.xz":
                raw = lzma.compress(raw)
            path = os.path.join(temp, f"{name}.{suffix}")
            with open(path, "wb") as stream:
                stream.write(raw)
            return path

        archives = {}
        for rootfs_owner in ("fabric", "software"):
            entries = _profile_entries(rootfs_owner)
            raw = _newc(entries)
            for suffix, data in (("cpio", raw),
                                 ("cpio.gz", gzip.compress(raw)),
                                 ("cpio.xz", lzma.compress(raw))):
                path = os.path.join(temp, f"{rootfs_owner}.{suffix}")
                with open(path, "wb") as stream:
                    stream.write(data)
                archives[rootfs_owner, suffix] = path

        def layout(owner, key=True):
            path = os.path.join(temp, f"layout-{owner}-{key}.json")
            body = {"images": [{"name": "rootfs", "offset": 1}]}
            if key:
                body["gptp_owner"] = owner
            with open(path, "w", encoding="utf-8") as stream:
                json.dump(body, stream)
            return path

        for suffix in ("cpio", "cpio.gz", "cpio.xz"):
            expect(True, layout("software"), archives["software", suffix])
            expect(True, layout("fabric"), archives["fabric", suffix])
            expect(False, layout("none"), archives["fabric", suffix])
            expect(False, layout("software"), archives["fabric", suffix])
            expect(False, layout("fabric"), archives["software", suffix])
            expect(False, layout("none"), archives["software", suffix])

        expect(False, layout("fabric"), None)
        expect(False, layout("fabric", key=False), archives["fabric", "cpio.xz"])
        expect(False, layout("unknown"), archives["fabric", "cpio.xz"])
        expect(False, layout("fabric"), archives["fabric", "cpio.xz"], "software")

        # The old image was software-owning but had no positive owner profile.
        # It is the concrete counterexample that marker-absence inference used
        # to misclassify as fabric.
        legacy_rows = [(b"etc/hostname", b"legacy\n", stat.S_IFREG),
                       (OWNER_INIT, b"#!/bin/sh\n", stat.S_IFREG | 0o111)]
        legacy_rows.extend((path, b"tool", stat.S_IFREG | 0o111)
                           for path in SOFTWARE_EXECUTABLES)
        legacy_rows.extend((path, b"config\n", stat.S_IFREG)
                           for path in SOFTWARE_FILES)
        legacy = write_archive("legacy-unmarked-software", legacy_rows)
        expect(False, layout("fabric"), legacy)
        expect(False, layout("software"), legacy)

        corrupt = os.path.join(temp, "corrupt.cpio.xz")
        with open(corrupt, "wb") as stream:
            stream.write(lzma.compress(_newc([]))[:-5])
        expect(False, layout("fabric"), corrupt)
        unsupported = os.path.join(temp, "rootfs.ext4")
        with open(unsupported, "wb") as stream:
            stream.write(b"not a cpio archive")
        expect(False, layout("fabric"), unsupported)

        duplicate = _newc(_profile_entries("software") + [
            (b"./etc//milan-gptp-software-owner", b"two", stat.S_IFREG),
        ])
        duplicate_path = os.path.join(temp, "duplicate.cpio.gz")
        with open(duplicate_path, "wb") as stream:
            stream.write(gzip.compress(duplicate))
        expect(False, layout("software"), duplicate_path)

        wrong_type = os.path.join(temp, "directory-marker.cpio.xz")
        wrong_type_rows = [row for row in _profile_entries("software")
                           if row[0] != SOFTWARE_MARKER]
        wrong_type_rows.append((SOFTWARE_MARKER, b"", stat.S_IFDIR))
        with open(wrong_type, "wb") as stream:
            stream.write(lzma.compress(_newc(wrong_type_rows)))
        expect(False, layout("software"), wrong_type)

        unsafe = os.path.join(temp, "absolute-marker.cpio.gz")
        unsafe_rows = [row for row in _profile_entries("software")
                       if row[0] != SOFTWARE_MARKER]
        unsafe_rows.append((b"/" + SOFTWARE_MARKER, b"lease", stat.S_IFREG))
        with open(unsafe, "wb") as stream:
            stream.write(gzip.compress(_newc(unsafe_rows)))
        expect(False, layout("software"), unsafe)

        duplicate_profile = write_archive(
            "duplicate-profile",
            _profile_entries("fabric") + [
                (b"./etc//milan-gptp-owner-profile",
                 PROFILE_PAYLOADS["fabric"], stat.S_IFREG),
            ])
        expect(False, layout("fabric"), duplicate_profile)

        wrong_version_rows = [
            (path, (b"milan-gptp-owner-profile-v0:fabric\n"
                    if path == PROFILE else payload), mode)
            for path, payload, mode in _profile_entries("fabric")
        ]
        expect(False, layout("fabric"),
               write_archive("wrong-profile-version", wrong_version_rows))

        missing_tool_rows = [row for row in _profile_entries("software")
                             if row[0] != b"usr/sbin/pmc"]
        expect(False, layout("software"),
               write_archive("software-missing-pmc", missing_tool_rows))

        contaminated_rows = _profile_entries("fabric") + [
            (b"usr/sbin/ptp4l", b"tool", stat.S_IFREG | 0o111),
        ]
        expect(False, layout("fabric"),
               write_archive("fabric-with-linuxptp", contaminated_rows))

        launcher_rows = _profile_entries("fabric") + [
            (b"etc/init.d/S65ptp4l", b"#!/bin/sh\n",
             stat.S_IFREG | 0o111),
        ]
        expect(False, layout("fabric"),
               write_archive("fabric-with-launcher", launcher_rows))

        software_launcher_rows = _profile_entries("software") + [
            (b"etc/init.d/S66phc2sys", b"#!/bin/sh\n",
             stat.S_IFREG | 0o111),
        ]
        expect(False, layout("software"),
               write_archive("software-with-launcher", software_launcher_rows))

        # The original R0 bypass: valid fabric profile, the exact retired
        # daemons relocated from usr/sbin to usr/bin, and a neutral-named init
        # script. Fixed-path and launcher-basename denylists both accepted it.
        relocated_rows = _profile_entries("fabric") + [
            (b"usr/bin/ptp4l", b"tool", stat.S_IFREG | 0o111),
            (b"usr/bin/phc2sys", b"tool", stat.S_IFREG | 0o111),
            (b"etc/timesync.cfg", b"config\n", stat.S_IFREG),
            (b"etc/init.d/S49timesync",
             b"#!/bin/sh\n/usr/bin/ptp4l -f /etc/timesync.cfg\n"
             b"/usr/bin/phc2sys -s CLOCK_REALTIME\n",
             stat.S_IFREG | 0o111),
        ]
        expect(False, layout("fabric"),
               write_archive("fabric-relocated-linuxptp", relocated_rows))

        neutral_launcher_rows = _profile_entries("fabric") + [
            (b"etc/init.d/S49timesync",
             b"#!/bin/sh\nexec /opt/time/ptp4l-custom -f /etc/time.cfg\n",
             stat.S_IFREG | 0o111),
        ]
        expect(False, layout("fabric"), write_archive(
            "fabric-neutral-launcher", neutral_launcher_rows))

        # An init script can name a neutral helper. Inspect executable scripts
        # outside init.d as well, so the second hop cannot hide the daemon.
        indirect_rows = _profile_entries("fabric") + [
            (b"etc/init.d/S49timesync",
             b"#!/bin/sh\nexec /usr/local/bin/start-clock\n",
             stat.S_IFREG | 0o111),
            (b"usr/local/bin/start-clock",
             b"#!/bin/sh\nexec /usr/local/sbin/phc2sys -s CLOCK_REALTIME\n",
             stat.S_IFREG | 0o111),
        ]
        expect(False, layout("fabric"),
               write_archive("fabric-indirect-launcher", indirect_rows))

        systemd_rows = _profile_entries("fabric") + [
            (b"usr/lib/systemd/system/timesync.service",
             b"[Service]\nExecStart=/usr/bin/ptp4l -i eth0\n",
             stat.S_IFREG),
        ]
        expect(False, layout("fabric"),
               write_archive("fabric-systemd-launcher", systemd_rows))

        extra_software_launcher = _profile_entries("software") + [
            (b"etc/init.d/S49timesync",
             b"#!/bin/sh\nexec /usr/sbin/ptp4l -i eth0\n",
             stat.S_IFREG | 0o111),
        ]
        expect(False, layout("software"), write_archive(
            "software-second-lifecycle", extra_software_launcher))

        relocated_symlink_rows = _profile_entries("fabric") + [
            (b"opt/time/ptp4l", b"../../usr/sbin/clockd",
             stat.S_IFLNK | 0o111),
        ]
        expect(False, layout("fabric"), write_archive(
            "fabric-relocated-symlink", relocated_symlink_rows))

        oversized_script_rows = _profile_entries("fabric") + [
            (b"usr/local/bin/start-clock",
             b"#!/bin/sh\n" + b"# pad\n" * (MAX_INSPECT_PAYLOAD // 6 + 1),
             stat.S_IFREG | 0o111),
        ]
        expect(False, layout("fabric"), write_archive(
            "fabric-oversized-script", oversized_script_rows))

        # Documentation may name linuxptp without being executable or a boot
        # record. The gate targets installed ownership semantics, not prose.
        documented_rows = _profile_entries("fabric") + [
            (b"usr/share/doc/milan/README",
             b"The software comparison uses ptp4l; fabric images do not.\n",
             stat.S_IFREG),
        ]
        expect(True, layout("fabric"),
               write_archive("fabric-doc-mention", documented_rows))

        duplicate_layout = os.path.join(temp, "layout-duplicate-images.json")
        with open(duplicate_layout, "w", encoding="utf-8") as stream:
            json.dump({"gptp_owner": "software", "images": [
                {"name": "rootfs"}, {"name": "rootfs"}]}, stream)
        expect(False, duplicate_layout, archives["software", "cpio.xz"])

        partial = os.path.join(temp, "layout-software-partial.json")
        with open(partial, "w", encoding="utf-8") as stream:
            json.dump({"gptp_owner": "software", "manifest": "kernel",
                       "images": [{"name": "kernel"}]}, stream)
        expect(False, partial)
        expect(True, partial, archives["software", "cpio.xz"])
        expect(False, partial, archives["fabric", "cpio.xz"])

        baremetal = os.path.join(temp, "layout-fabric-baremetal.json")
        with open(baremetal, "w", encoding="utf-8") as stream:
            json.dump({"gptp_owner": "fabric", "manifest": "baremetal",
                       "images": [{"name": "aem"}]}, stream)
        expect(True, baremetal)
        expect(True, baremetal, archives["fabric", "cpio.xz"])
        expect(False, baremetal, archives["software", "cpio.xz"])

        none_baremetal = os.path.join(temp, "layout-none-baremetal.json")
        with open(none_baremetal, "w", encoding="utf-8") as stream:
            json.dump({"gptp_owner": "none", "manifest": "baremetal",
                       "images": [{"name": "aem"}]}, stream)
        expect(True, none_baremetal)
        expect(False, none_baremetal, archives["fabric", "cpio.xz"])

        def fbi(payload):
            return (struct.pack("<II", len(payload),
                                binascii.crc32(payload) & 0xFFFF_FFFF)
                    + payload)

        fbi_fabric = os.path.join(temp, "fabric-rootfs.fbi")
        fbi_software = os.path.join(temp, "software-rootfs.fbi")
        fabric_xz = open(archives["fabric", "cpio.xz"], "rb").read()
        software_xz = open(archives["software", "cpio.xz"], "rb").read()
        with open(fbi_fabric, "wb") as stream:
            stream.write(fbi(fabric_xz))
        with open(fbi_software, "wb") as stream:
            stream.write(fbi(software_xz))
        expect(True, layout("fabric"), fbi_fabric)
        expect(True, layout("software"), fbi_software)
        corrupt_fbi = os.path.join(temp, "corrupt-rootfs.fbi")
        with open(corrupt_fbi, "wb") as stream:
            damaged = bytearray(fbi(software_xz))
            damaged[-1] ^= 1
            stream.write(damaged)
        expect(False, layout("software"), corrupt_fbi)

        paired = os.path.join(temp, "paired")
        os.makedirs(os.path.join(paired, "gateware"))
        paired_bit = os.path.join(paired, "gateware", "board.bit")
        from qspi_owner_transition import _fake_bit
        _fake_bit(paired_bit, b"\xff" * 16 + b"\xaa\x99\x55\x66paired")
        paired_layout = os.path.join(paired, "flashboot_layout.json")
        paired_body = {"gptp_owner": "fabric", "manifest": "full",
                       "complete": True, "images": [
                           {"name": "bitstream", "offset": 0,
                            "budget": 0x400000},
                           {"name": "rootfs", "offset": 0x400000,
                            "budget": 0x100000},
                       ]}
        paired_body.update(bitstream_binding(paired_bit))
        with open(paired_layout, "w", encoding="utf-8") as stream:
            json.dump(paired_body, stream)
        fabric_rootfs = archives["fabric", "cpio.xz"]
        expect(True, paired_layout, fabric_rootfs, bit=paired_bit,
               part="xc7a100tfgg484")
        expect(False, paired_layout, fabric_rootfs, bit=paired_bit,
               part="xc7a200tfbg484")
        expect(False, paired_layout, fabric_rootfs,
               part="xc7a100tfgg484")
        expect(False, layout("fabric"), fabric_rootfs, bit=paired_bit,
               part="xc7a100tfgg484")
        corrupt_bit = os.path.join(paired, "gateware", "corrupt.bit")
        with open(corrupt_bit, "wb") as stream:
            stream.write(b"not a Xilinx bitstream")
        expect(False, paired_layout, fabric_rootfs, bit=corrupt_bit,
               part="xc7a100tfgg484")
        adjacent_bit = os.path.join(paired, "gateware", "other-owner.bit")
        _fake_bit(adjacent_bit,
                  b"\xff" * 16 + b"\xaa\x99\x55\x66software-owner")
        expect(False, paired_layout, fabric_rootfs, bit=adjacent_bit,
               part="xc7a100tfgg484")

    print(f"[gptp-owner] self-test: {checks}/{checks} checks pass")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout")
    parser.add_argument("--rootfs")
    parser.add_argument("--expected-owner", choices=OWNERS)
    parser.add_argument("--bit")
    parser.add_argument("--expected-fpga-part")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if not args.layout:
        parser.error("--layout is required")
    try:
        owner, detail = check_pair(
            args.layout, args.rootfs, args.expected_owner,
            args.bit, args.expected_fpga_part)
    except ContractError as exc:
        print(f"[gptp-owner] REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"[gptp-owner] OK: gateware owner={owner}; {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
