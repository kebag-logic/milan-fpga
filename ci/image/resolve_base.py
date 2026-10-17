#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Bind the source lock to the verified pinned base's exported layer bytes."""

import argparse
import json
from pathlib import Path
import tarfile

import image_archive
import privacy


def main() -> int:
    """Refuse any export whose top descriptor is not the selected base digest."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    path = Path(__file__).with_name("sources.lock.json")
    pins = json.loads(path.read_text())
    with tarfile.open(args.archive) as archive:
        index = json.load(archive.extractfile("index.json"))
    if len(index["manifests"]) != 1 or index["manifests"][0]["digest"] != pins["base"].split("@")[1]:
        raise ValueError("archive does not identify the locked base")
    upstream = privacy.base_provenance(pins, args.archive, privacy.Policy())
    measured = image_archive.inspect(args.archive, pins["platform"], upstream)
    pins["base_layers"] = measured["layers"]
    status = None
    with tarfile.open(args.archive) as archive:
        for layer in pins["base_layers"]:
            stream = image_archive.blob(archive, layer["oci_digest"])
            with stream, tarfile.open(fileobj=stream, mode="r|*") as entries:
                for member in entries:
                    if member.name == "var/lib/dpkg/status":
                        status = entries.extractfile(member).read().decode()
    if status is None:
        raise ValueError("pinned base has no package status")
    packages = []
    for paragraph in status.split("\n\n"):
        fields = dict(line.split(": ", 1) for line in paragraph.splitlines()
                      if line and not line[0].isspace() and ": " in line)
        if fields.get("Status") == "install ok installed":
            packages.append({key: fields[key] for key in ("Package", "Version", "Provides") if key in fields})
    pins["base_packages"] = sorted(packages, key=lambda row: row["Package"])
    path.write_text(json.dumps(pins, sort_keys=True, indent=2) + "\n")
    print("PASS: source lock records the verified base layers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
