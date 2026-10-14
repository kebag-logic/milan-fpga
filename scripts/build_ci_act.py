#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build the pinned local dispatcher with atomic fail-fast job admission.

All downloads, compiler caches and binaries stay beneath the supplied scratch
directory. Existing upstream tests are unchanged. The patch adds a separate
dispatcher and selects it only for workflow job scheduling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ACT_COMMIT = "4f411281417e88660bea1c1a1749aa71ae0bd60f"
ACT_SHA256 = "0d151c0a14455ea2ee1d2bff5258aadef9ac96e35f9756e6bcd8af323780ae98"
GO_SHA256 = "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613"
VERSION = "0.2.89+milan-ci1"


def digest(path: Path) -> str:
    """Hash an artifact without retaining its binary data in the receipt."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(url: str, path: Path, expected: str) -> None:
    """An existing archive still requires its exact source digest."""
    if not path.exists():
        with urllib.request.urlopen(url, timeout=120) as response, path.open("xb") as output:
            shutil.copyfileobj(response, output)
    if digest(path) != expected:
        raise ValueError("archive digest differs: " + path.name)


def extract(archive: Path, directory: Path) -> None:
    """Use the data-only extractor and a new destination for each verified source."""
    directory.mkdir()
    with tarfile.open(archive) as source:
        source.extractall(directory, filter="data")


def build(directory: Path) -> dict:
    """Run scheduling controls, unchanged upstream controls and a reproducible compiler invocation."""
    directory.mkdir(parents=True, exist_ok=False)
    compiler = directory / "go1.25.0.linux-amd64.tar.gz"
    archive = directory / "act.tar.gz"
    download("https://go.dev/dl/" + compiler.name, compiler, GO_SHA256)
    download("https://github.com/nektos/act/archive/" + ACT_COMMIT + ".tar.gz", archive, ACT_SHA256)
    extract(compiler, directory / "compiler")
    extract(archive, directory / "source")
    source = directory / "source" / ("act-" + ACT_COMMIT)
    go = directory / "compiler/go/bin/go"
    patch = ROOT / "ci/act/fail-fast.patch"
    controls = ROOT / "ci/act/parallel_executor_test.go"
    subprocess.run(["patch", "--batch", "--fuzz=0", "-p1", "-i", str(patch)], cwd=source, check=True)
    shutil.copyfile(controls, source / "pkg/common/milan_parallel_executor_test.go")
    environment = dict(os.environ, GOCACHE=str(directory / "cache"), GOPATH=str(directory / "modules"),
                       GOTOOLCHAIN="local", GOMAXPROCS="4", TMPDIR=str(directory))
    commands = (
        ["test", "-p", "4", "-race", "./pkg/common", "-run", "Test(Bounded|CancelledParent)", "-count=20"],
        ["test", "-p", "4", "./pkg/common"],
        ["build", "-p", "4", "-trimpath", "-buildvcs=false", "-ldflags", "-X main.version=" + VERSION,
         "-o", str(directory / "act"), "main.go"],
    )
    for command in commands:
        subprocess.run([str(go), *command], cwd=source, env=environment, check=True)
    version = subprocess.check_output([str(directory / "act"), "--version"], text=True).strip()
    if version != "act version " + VERSION:
        raise ValueError("built dispatcher version differs")
    return {"version": VERSION, "source_commit": ACT_COMMIT, "source_sha256": ACT_SHA256,
            "compiler_sha256": GO_SHA256, "patch_sha256": digest(patch),
            "controls_sha256": digest(controls), "recipe_sha256": digest(Path(__file__)),
            "binary_sha256": digest(directory / "act"), "binary_bytes": (directory / "act").stat().st_size}


def main() -> int:
    """Build only outside the repository and retain a small provenance receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve()
    if directory == ROOT or ROOT in directory.parents:
        parser.error("the build directory must be outside the repository")
    receipt = build(directory)
    directory.joinpath("build-receipt.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
