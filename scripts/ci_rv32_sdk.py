#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Install the #504 Bootlin SDK; prove provenance before using a cache.

Only disposable CI runners use the default destination. Local experiments
must supply a new --destination. Existing unreceipted trees are never replaced.
The receipt detects accidental cache drift; GitHub cache scoping is the trust
boundary, not a signature made by this installer over its own output.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import tarfile
import tempfile
import urllib.request


RELEASE = "riscv32-ilp32d--glibc--stable-2025.08-1"
ARCHIVE_SHA256 = "d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f"
ARCHIVE_URL = ("https://toolchains.bootlin.com/downloads/releases/toolchains/"
               f"riscv32-ilp32d/tarballs/{RELEASE}.tar.xz")
INSTALLER_REVISION = 1
RECEIPT = ".milan-rv32-sdk.json"
COMPILER = "bin/riscv32-linux-gcc"


def digest(path: Path) -> str:
    """Hash bytes without loading the SDK into memory."""
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def host_identity() -> dict[str, str]:
    """The selected archive contains Linux x86-64 host executables."""
    system, machine = platform.system(), platform.machine()
    if (system, machine) != ("Linux", "x86_64"):
        raise ValueError(f"unsupported SDK host: {system}/{machine}")
    return {"os": system, "architecture": machine}


def provenance(destination: Path) -> dict[str, object]:
    """Inputs a restored receipt must match exactly."""
    return {"archive_url": ARCHIVE_URL, "archive_sha256": ARCHIVE_SHA256,
            "release": RELEASE, "installer_revision": INSTALLER_REVISION,
            "installer_sha256": digest(Path(__file__).resolve()),
            "host": host_identity(), "destination": str(destination)}


def inventory(destination: Path) -> dict[str, object]:
    """Bind every installed file, mode and link, including compiler support files."""
    records = {}
    for path in sorted(destination.rglob("*")):
        relative = path.relative_to(destination).as_posix()
        if relative == RECEIPT:
            continue
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            records[relative] = {"link": os.readlink(path)}
        elif stat.S_ISREG(mode):
            records[relative] = {"sha256": digest(path),
                                 "mode": stat.S_IMODE(mode)}
        elif not stat.S_ISDIR(mode):
            raise ValueError(f"unexpected SDK entry: {relative}")
    return records


def identify(destination: Path) -> dict[str, str]:
    """Prove relocation and compiler identity using the exact selector spelling."""
    compiler = destination / COMPILER
    realpath = compiler.resolve(strict=True)
    if not realpath.is_relative_to(destination):
        raise ValueError("compiler realpath escapes SDK destination")
    values = {}
    for name, option in (("version", "--version"),
                         ("gcc_version", "-dumpfullversion"),
                         ("target", "-dumpmachine"),
                         ("sysroot", "-print-sysroot")):
        argv = [str(compiler), option]
        print("SDK argv: " + json.dumps(argv), flush=True)
        values[name] = subprocess.run(argv, check=True, text=True,
                                      capture_output=True).stdout.strip()
    if values["gcc_version"] != "14.3.0":
        raise ValueError("SDK GCC version mismatch")
    if values["target"] != "riscv32-buildroot-linux-gnu":
        raise ValueError("SDK target mismatch")
    sysroot = Path(values["sysroot"]).resolve(strict=True)
    if not sysroot.is_relative_to(destination):
        raise ValueError("SDK sysroot is not relocated into destination")
    if (destination / "share/buildroot/sdk-location").read_text().strip() != str(destination):
        raise ValueError("SDK relocation receipt mismatch")
    return {**values, "compiler": str(compiler), "realpath": str(realpath)}


def verify(destination: Path) -> dict[str, object]:
    """Check provenance and installed bytes before executing a cached tool."""
    receipt_path = destination / RECEIPT
    if receipt_path.is_symlink() or not receipt_path.is_file():
        raise ValueError("missing regular SDK provenance receipt; incomplete install")
    receipt = json.loads(receipt_path.read_text())
    if not isinstance(receipt, dict) or set(receipt) != {"provenance", "inventory", "tools"}:
        raise ValueError("malformed SDK provenance receipt")
    if receipt["provenance"] != provenance(destination):
        raise ValueError("SDK provenance mismatch")
    actual = inventory(destination)
    if not actual or receipt["inventory"] != actual:
        raise ValueError("SDK inventory mismatch; incomplete or corrupt install")
    if receipt["tools"] != identify(destination):
        raise ValueError("SDK tool identification mismatch")
    print("SDK verified: " + json.dumps(receipt["provenance"], sort_keys=True))
    print("SDK tools: " + json.dumps(receipt["tools"], sort_keys=True))
    return receipt


def extract(archive: Path, destination: Path) -> None:
    """Verify before extraction; execute only the pinned relocation script."""
    actual = digest(archive)
    if actual != ARCHIVE_SHA256:
        raise ValueError(f"SDK archive digest mismatch: {actual}")
    print(f"SDK archive verified: {archive} sha256={actual}", flush=True)
    # The digest authenticates this exact upstream tar layout. Reject an
    # unexpected root before asking tar to strip it into the final prefix.
    with tarfile.open(archive, "r:xz") as stream:
        if any(Path(member.name).parts[0] != RELEASE for member in stream):
            raise ValueError("SDK archive root mismatch")
    destination.mkdir(parents=True)
    subprocess.run(["tar", "-xJf", str(archive), "--strip-components=1",
                    "-C", str(destination)], check=True)
    argv = [str(destination / "relocate-sdk.sh")]
    print("SDK argv: " + json.dumps(argv), flush=True)
    subprocess.run(argv, cwd=destination, check=True)
    tools = identify(destination)
    receipt = {"provenance": provenance(destination),
               "inventory": inventory(destination), "tools": tools}
    (destination / RECEIPT).write_text(json.dumps(receipt, sort_keys=True) + "\n")


def install(destination: Path, archive: Path | None = None) -> None:
    """Install into an absent prefix, or validate an existing receipt without repair."""
    host_identity()
    if destination.is_symlink() or destination.absolute() != destination.resolve():
        raise ValueError("SDK destination must be an absolute path without symlink parents")
    destination = destination.absolute()
    if archive is not None and digest(archive) != ARCHIVE_SHA256:
        raise ValueError("SDK archive digest mismatch")
    if destination.exists():
        verify(destination)
        print("SDK cache hit: verified")
        return
    if archive is None:
        with tempfile.TemporaryDirectory(prefix="milan-rv32-download-") as tmp:
            downloaded = Path(tmp) / f"{RELEASE}.tar.xz"
            print(f"SDK download: {ARCHIVE_URL}", flush=True)
            with urllib.request.urlopen(ARCHIVE_URL, timeout=120) as response:
                with downloaded.open("wb") as output:
                    while block := response.read(1024 * 1024):
                        output.write(block)
            extract(downloaded, destination)
    else:
        extract(archive, destination)
    verify(destination)
    print("SDK fresh installation: verified")


def main() -> None:
    """Explicit local destination; settled home-relative default only for CI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path,
                        default=Path.home() / "br-milan-rv32/host")
    parser.add_argument("--archive", type=Path,
                        help="offline input, still checked against the pinned digest")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        verify(args.destination)
    else:
        install(args.destination, args.archive)


if __name__ == "__main__":
    main()
