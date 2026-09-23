#!/usr/bin/env python3
"""Download-path authentication probe (no network).

Usage: probe_download_auth.py <clone> <scratch-dir>
Serves a well-formed but UNPINNED archive (correct root, hostile
relocate-sdk.sh that writes a marker) through a mocked urlopen, i.e. the
exact path the hosted jobs take (no --archive). Runs it against:
  A. the exact-head installer, and
  B. the same installer with only extract()'s digest check deleted.
The exact-head self-test passes for B (see mutate_installer.py), so this
probe shows what that surviving mutant would admit.
"""

import contextlib
import io
import json
import shutil
import sys
import tarfile
from pathlib import Path
from unittest.mock import patch
import importlib.util

clone, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=False)
source = (clone / "scripts/ci_rv32_sdk.py").read_text()
check = ("    if actual != ARCHIVE_SHA256:\n"
         "        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n")
assert source.count(check) == 1
variants = {"A-exact-head": source, "B-extract-digest-check-deleted": source.replace(check, "")}


def load(name, text):
    path = scratch / f"{name}.py"
    path.write_text(text)
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hostile_archive(sdk, root: Path) -> bytes:
    """Correct top-level root, fixture compiler, marker-writing relocation."""
    tree = root / sdk.RELEASE
    (tree / "bin").mkdir(parents=True)
    (tree / "sysroot").mkdir()
    (tree / "share/buildroot").mkdir(parents=True)
    (tree / "share/buildroot/sdk-location").write_text("/old\n")
    tool = tree / "bin/fixture-gcc"
    tool.write_text("#!/bin/sh\nroot=\"$(cd \"$(dirname \"$0\")/..\" && pwd)\"\n"
                    "case \"$1\" in --version) echo x;; -dumpfullversion) echo 14.3.0;;\n"
                    " -dumpmachine) echo riscv32-buildroot-linux-gnu;;\n"
                    " -print-sysroot) echo \"$root/sysroot\";; esac\n")
    tool.chmod(0o755)
    (tree / "bin/riscv32-linux-gcc").symlink_to("fixture-gcc")
    reloc = tree / "relocate-sdk.sh"
    marker = root / "HOSTILE-RELOCATION-EXECUTED"
    reloc.write_text(f"#!/bin/sh\ntouch '{marker}'\npwd > share/buildroot/sdk-location\n")
    reloc.chmod(0o755)
    archive = root / "unpinned.tar.xz"
    with tarfile.open(archive, "w:xz") as stream:
        stream.add(tree, arcname=sdk.RELEASE)
    return archive.read_bytes()


for name, text in variants.items():
    sdk = load(name, text)
    work = scratch / name
    work.mkdir()
    payload = hostile_archive(sdk, work)
    marker = work / "HOSTILE-RELOCATION-EXECUTED"
    destination = work / "host"
    response = io.BytesIO(payload)
    with patch.object(sdk.urllib.request, "urlopen") as urlopen:
        urlopen.return_value.__enter__.return_value = response
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                sdk.install(destination)
            outcome = "INSTALLED AND VERIFIED"
        except Exception as exc:  # noqa: BLE001 - recording the refusal
            outcome = f"REFUSED: {type(exc).__name__}: {exc}"
    print(json.dumps({"installer": name, "outcome": outcome[:160],
                      "relocate_sdk_executed": marker.exists(),
                      "prefix_created": destination.exists()}))
