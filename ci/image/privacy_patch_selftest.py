#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise exact patch provenance with real pinned archives and committed diffs."""

import hashlib
import io
from pathlib import Path
import subprocess
import tempfile

from build_selftest import refused
import patch_provenance
import privacy
from privacy_selftest import tar_bytes


def controls(root: Path) -> None:
    """Require unchanged matches, refuse added matches, and authenticate both inputs."""
    policy = privacy.Policy()
    original = b"upstream /home/" + b"fixture-account/source.c\nold\n"
    patch = b"--- a/source.c\n+++ b/source.c\n@@ -1,2 +1,2 @@\n " + original.splitlines(True)[0] + b"-old\n+new\n"
    directory = root / patch_provenance.PATCHES
    directory.mkdir(parents=True)
    series = directory / "apply.sh"
    series.write_text('SERIES=(\n    "fixture fixture.patch"\n)\n')
    path = directory / "fixture.patch"
    path.write_bytes(patch)
    for command in (["git", "init", "--quiet"], ["git", "add", "."],
                    ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                     "commit", "--quiet", "-m", "Record fixture patch"]):
        subprocess.run(command, cwd=root, check=True)
    source = root / "source.tar"
    source.write_bytes(tar_bytes({"upstream/source.c": original}))
    row = {"tool": "fixture", "version": "a" * 40, "filename": source.name,
           "url": "https://example.invalid/public/source", "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
           "size": source.stat().st_size}
    pins = {"sources": [row]}
    proof = patch_provenance.provenance(pins, root, policy)
    result = original.replace(b"old\n", b"new\n")
    allowed = []
    privacy.check_file(io.BytesIO(result), "opt/cpu/source.c", policy, proof, allowed)
    assert allowed[0]["unchanged_matches"] == [{"output_line": 1, "upstream_line": 1}]
    assert allowed[0]["patches"][0]["sha256"] == hashlib.sha256(patch).hexdigest()
    refused(lambda: privacy.check_file(io.BytesIO(result + b"drift"), "opt/cpu/source.c", policy, proof, []),
            "unreproduced patched postimage")
    path.write_bytes(patch + b"changed")
    refused(lambda: patch_provenance.provenance(pins, root, policy), "uncommitted patch change")
    planted = patch.replace(b"+new\n", b"+new /home/" + b"fixture-account/private\n")
    path.write_bytes(planted)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "--quiet", "-m", "Plant added identity"], cwd=root, check=True)
    refused(lambda: patch_provenance.provenance(pins, root, policy), "identity on committed patch-added line")
    source.write_bytes(source.read_bytes() + b"drift")
    refused(lambda: patch_provenance.provenance(pins, root, policy), "changed pinned archive")
    print("PASS: exact patched output, unchanged matches, added identity and input authentication")


def main() -> int:
    """Keep the disposable repository and source fixture outside the checkout."""
    saved = patch_provenance.ROOT
    with tempfile.TemporaryDirectory(prefix="patch-privacy-") as directory:
        patch_provenance.ROOT = Path(directory)
        try:
            controls(Path(directory))
        finally:
            patch_provenance.ROOT = saved
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
