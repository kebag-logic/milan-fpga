#!/usr/bin/env python3
"""Check the report contract and seal only the explicitly publishable trees."""
import argparse
import hashlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = args.packet.resolve()
    report = (packet / "REPORT.md").read_text()
    assert report.splitlines()[0] == "[R633] POSITIVE - exact head 7c862ad980dfe829ef4d85ff8f4fb4fab451984f"
    assert report.splitlines()[-1] == "R633-5 FINISHED"
    assert "SKELETON" not in report
    for lens in ["Conformance", "RTL", "Robustness", "Tests", "Docs"]:
        assert f"[R633] PASS {lens} - " in report
        assert f"| {lens} | CLEAN |" in report
    paths = sorted(path for path in packet.iterdir() if path.is_file() and path.name != "MANIFEST.sha256")
    for directory in ["public-source", "public-state"]:
        paths.extend(sorted(path for path in (packet / directory).rglob("*") if path.is_file()))
    entries = []
    for path in sorted(paths):
        assert not path.is_symlink()
        data = path.read_bytes()
        for private in (bytes.fromhex("2f686f6d652f616c65782f"), bytes.fromhex("2f646174612f6d696c616e2f"), bytes.fromhex("2e636f6465782f")):
            assert private not in data, (path.relative_to(packet), private)
        relative = path.relative_to(packet).as_posix()
        assert not relative.startswith("scratch/")
        entries.append(f"{hashlib.sha256(data).hexdigest()}  {relative}\n")
    (packet / "MANIFEST.sha256").write_text("".join(entries))
    print(f"Sealed {len(entries)} files, including REPORT.md; scratch excluded")


if __name__ == "__main__":
    main()
