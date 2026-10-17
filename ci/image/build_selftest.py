#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove that source pins, downloads and recipe identity fail closed."""

import copy
from concurrent.futures import ThreadPoolExecutor
from collections.abc import Callable
import hashlib
import io
import json
from pathlib import Path
import tempfile
import tarfile
import threading
import urllib.error
from unittest.mock import patch

import build


def refused(operation: Callable[[], None], name: str) -> None:
    """A negative control must fail before any image can be accepted."""
    try:
        operation()
    except ValueError:
        print(f"PASS: {name} refused")
    else:
        raise AssertionError(name)


def main() -> int:
    """Plant wrong versions, hashes, paths and cached bytes without Docker."""
    pins = json.loads((build.HERE / "sources.lock.json").read_text())
    build.validate_pins(pins)
    for tool, field, value in (("verilator", "version", "v0.1"),
                               ("rv32-sdk", "sha256", "0" * 64),
                               ("cmarkgfm", "sha256", "0" * 64),
                               ("sbt", "filename", "../../escaped")):
        changed = copy.deepcopy(pins)
        next(row for row in changed["sources"] if row["tool"] == tool)[field] = value
        refused(lambda: build.validate_pins(changed), f"changed {tool} {field}")
    changed = copy.deepcopy(pins)
    changed["sources"] = [row for row in changed["sources"] if row["tool"] != "verilator"]
    refused(lambda: build.validate_pins(changed), "missing workflow tool")
    changed = copy.deepcopy(pins)
    changed["sources"].append(changed["sources"][0])
    refused(lambda: build.validate_pins(changed), "duplicate source")
    changed = copy.deepcopy(pins)
    changed["base"] = "ubuntu:latest"
    refused(lambda: build.validate_pins(changed), "different base")
    payload = b"verified artifact\n"
    row = {"tool": "fixture", "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest(),
           "url": "https://example.invalid/fixture"}
    with tempfile.TemporaryDirectory(prefix="image-selftest-") as directory:
        target = Path(directory) / "artifact"
        with patch("urllib.request.urlopen", return_value=io.BytesIO(payload)):
            build.verified_download(row, target)
        assert target.read_bytes() == payload
        retained = {**row, "fallback_urls": ["https://example.invalid/snapshot/fixture"]}
        target.unlink()
        missing = urllib.error.HTTPError(row["url"], 404, "superseded", {}, None)
        with patch("urllib.request.urlopen", side_effect=[missing, io.BytesIO(payload)]) as fetch:
            build.verified_download(retained, target)
        assert [call.args[0] for call in fetch.call_args_list] == [row["url"], retained["fallback_urls"][0]]
        assert target.read_bytes() == payload
        target.unlink()
        with patch("urllib.request.urlopen", side_effect=[missing, io.BytesIO(b"x" * len(payload))]):
            refused(lambda: build.verified_download(retained, target), "corrupt retained package")
        assert not target.exists()
        with patch("urllib.request.urlopen", return_value=io.BytesIO(payload)):
            build.verified_download(row, target)
        print("PASS: primary 404 uses retained URL with the original size and checksum")
        with patch("urllib.request.urlopen", side_effect=AssertionError("cache should be reused")):
            build.verified_download(row, target)
        target.write_bytes(b"x" * len(payload))
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b"x" * len(payload))):
            refused(lambda: build.verified_download(row, target), "same-size corrupt cached and remote bytes")
        assert not target.with_name("artifact.part").exists()
        with patch("urllib.request.urlopen", return_value=io.BytesIO(payload)):
            build.verified_download(row, target)
        assert target.read_bytes() == payload
        print("PASS: repaired download re-verifies exact bytes")
        for attempt in range(10):
            duplicate = Path(directory) / f"duplicate-{attempt}"
            barrier = threading.Barrier(2)

            def response(*args: object, **kwargs: object) -> io.BytesIO:
                """Force both transfers to start before either can finish."""
                barrier.wait(timeout=10)
                return io.BytesIO(payload)

            with patch("urllib.request.urlopen", side_effect=response), ThreadPoolExecutor(max_workers=2) as pool:
                list(pool.map(lambda _: build.verified_download(row, duplicate), range(2)))
            assert duplicate.read_bytes() == payload
            assert not list(Path(directory).glob("*.part"))
        print("PASS: ten simultaneous duplicate downloads preserve verified bytes")
        archive = Path(directory) / "litex.tar.gz"
        source = b'git_setup("VexiiRiscv", ndir, "public", "dev", "' + b"a" * 40 + b'")\n'
        with tarfile.open(archive, "w:gz") as stream:
            member = tarfile.TarInfo("litex/litex/soc/cores/cpu/vexiiriscv/core.py")
            member.size = len(source)
            stream.addfile(member, io.BytesIO(source))
        derived = {"sources": [{"tool": "litex", "filename": archive.name},
                               {"tool": "VexiiRiscv", "version": "a" * 40}]}
        build.validate_derived_pin(Path(directory), derived)
        derived["sources"][1]["version"] = "b" * 40
        refused(lambda: build.validate_derived_pin(Path(directory), derived), "changed derived CPU pin")
    before = build.recipe_digest()
    inputs = build.recipe_inputs()
    inputs["ci/image/sources.lock.json"] = "0" * 64
    with patch.object(build, "recipe_inputs", return_value=inputs):
        assert build.recipe_digest() != before
    print("PASS: source pin change changes recipe identity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
