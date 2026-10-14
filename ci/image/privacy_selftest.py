#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove provenance never blesses changed, unknown or first-party files."""

import hashlib
import io
import json
from pathlib import Path
import tempfile
import tarfile

from build_selftest import refused
import image_archive
import privacy


def tar_bytes(files: dict[str, bytes]) -> bytes:
    """Make a small real archive, including a full OCI fixture's blobs."""
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        for name, payload in files.items():
            member = tarfile.TarInfo(name)
            member.size = len(payload)
            archive.addfile(member, io.BytesIO(payload))
    return stream.getvalue()


def descriptor(payload: bytes) -> dict[str, object]:
    """Describe the exact fixture bytes, without mocking their authentication."""
    return {"digest": "sha256:" + hashlib.sha256(payload).hexdigest(), "size": len(payload)}


def fixture(path: Path, files: dict[str, bytes], settings: dict[str, object]) -> None:
    """Write one-layer OCI bytes with ordinary metadata plus the selected plant."""
    layer = tar_bytes(files)
    config = {"os": "linux", "architecture": "amd64", "rootfs": {"diff_ids": [descriptor(layer)["digest"]]},
              "config": {}, "history": []}
    config.update(settings)
    content = json.dumps(config).encode()
    layer_record = {**descriptor(layer), "mediaType": "application/vnd.oci.image.layer.v1.tar"}
    manifest = json.dumps({"config": descriptor(content), "layers": [layer_record]}).encode()
    blobs = {"blobs/" + descriptor(data)["digest"].replace(":", "/"): data for data in (layer, content, manifest)}
    blobs["index.json"] = json.dumps({"manifests": [descriptor(manifest)]}).encode()
    path.write_bytes(tar_bytes(blobs))


def provenance_controls(root: Path, policy: privacy.Policy) -> None:
    """Use a pinned archive to prove original, altered, absent and excluded files."""
    payload = b"upstream /home/" + b"fixture-account/source.c\n"
    source = root / "source.tar"
    source.write_bytes(tar_bytes({"upstream/source.c": payload}))
    row = {"tool": "fixture", "version": "a" * 40, "filename": source.name,
           "url": "https://example.invalid/public/source", "sha256": descriptor(source.read_bytes())["digest"][7:],
           "size": source.stat().st_size}
    pins = {"sources": [row], "packages": []}
    upstream = privacy.provenance(pins, root, policy)
    allowed = []
    privacy.check_file(io.BytesIO(payload), "opt/cpu/source.c", policy, upstream, allowed)
    assert len(allowed) == 1 and allowed[0]["member_sha256"] == hashlib.sha256(payload).hexdigest()
    for name, data in (("modified upstream", payload + b"changed"), ("unknown file", payload + b"unknown")):
        refused(lambda: privacy.check_file(io.BytesIO(data), "opt/cpu/source.c", policy, upstream, []), name)
    refused(lambda: privacy.check_file(io.BytesIO(payload), "opt/tsn-gen/source.c", policy, upstream, []),
            "first-party placement")
    row["url"] = "https://github.com/kebag-logic/fixture"
    assert not privacy.provenance(pins, root, policy)
    row["url"] = "https://example.invalid/public/source"
    source.write_bytes(source.read_bytes() + b"changed")
    refused(lambda: privacy.provenance(pins, root, policy), "modified source archive")
    print("PASS: per-file upstream identity, source authentication and first-party exclusion")


def layer_controls(root: Path, policy: privacy.Policy) -> None:
    """Exercise every table class in contents, history, labels and environment."""
    table = json.loads(Path(__file__).with_name("privacy.json").read_text())
    plants = [b"/home/" + b"fixture-account/source", b"192" + b".168.42.7", bytes((97, 109, 120)) + b"-fixture",
              b"ghp_" + b"a" * 36, str(Path.home()).encode() + b"/private"]
    plants += [bytes(row["codepoints"]) for row in table["rules"] if "codepoints" in row]
    plants += [privacy.socket.gethostname().encode(), privacy.pwd.getpwuid(privacy.os.getuid()).pw_name.encode()]
    archive = root / "fixture.tar"
    for plant in plants:
        if plant == b"root":
            continue
        assert policy.matches(plant), "plant did not select a policy class"
        text = plant.decode()
        cases = [({"file": plant}, {}), ({}, {"history": [{"created_by": text}]}),
                 ({}, {"config": {"Labels": {"fixture": text}}}),
                 ({}, {"config": {"Env": ["FIXTURE=" + text]}})]
        for files, settings in cases:
            fixture(archive, files, settings)
            refused(lambda: image_archive.inspect(archive, "linux/amd64"), "protected class in OCI surface")
    fixture(archive, {"opt/tsn-gen/__pycache__/fixture.pyc": b"clean"}, {})
    refused(lambda: image_archive.inspect(archive, "linux/amd64"), "oracle bytecode")
    fixture(archive, {"opt/tsn-gen/build/CMakeCache.txt": b"clean"}, {})
    refused(lambda: image_archive.inspect(archive, "linux/amd64"), "oracle build log")
    fixture(archive, {"opt/cpu/clean.c": b"int x;"}, {})
    assert image_archive.inspect(archive, "linux/amd64")["upstream_allowances"] == []
    print("PASS: every protected class and OCI metadata surface; oracle leftovers")


def main() -> int:
    """Run only disposable offline fixtures with no Docker authority."""
    with tempfile.TemporaryDirectory(prefix="image-privacy-") as directory:
        root = Path(directory)
        policy = privacy.Policy()
        provenance_controls(root, policy)
        layer_controls(root, policy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
