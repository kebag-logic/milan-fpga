#!/usr/bin/env python3
"""Verify every published diagram PNG and its editable source."""

from __future__ import annotations

import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from png_artifact import (
    Chunk,
    encode_chunks,
    inspect_png,
    parse_chunks,
    source_digest,
)


ROOT = Path(__file__).resolve().parents[1]
DRAWIO_HASH_KEY = "Milan-Drawio-SHA256"
WAVEDROM_HASH_KEY = "Milan-WaveDrom-JSON-SHA256"


@dataclass(frozen=True)
class Artifact:
    png: str
    source: str
    key: str
    minimum_width: int = 1200
    minimum_height: int = 500


ARTIFACTS = (
    Artifact("docs/DOC_MAP.png", "docs/DOC_MAP.drawio", DRAWIO_HASH_KEY),
    Artifact(
        "docs/diagrams/submodule_boundaries.png",
        "docs/diagrams/submodule_boundaries.drawio",
        DRAWIO_HASH_KEY,
    ),
    Artifact(
        "docs/diagrams/wd_axis_backpressure.png",
        "docs/diagrams/wd_axis_backpressure.json",
        WAVEDROM_HASH_KEY,
    ),
    Artifact(
        "docs/diagrams/wd_cdc_handshake.png",
        "docs/diagrams/wd_cdc_handshake.json",
        WAVEDROM_HASH_KEY,
    ),
)


def validate(root: Path) -> list[str]:
    """Return every PNG availability, raster, and provenance error."""
    errors: list[str] = []
    for artifact in ARTIFACTS:
        png = root / artifact.png
        source = root / artifact.source
        if not source.is_file():
            errors.append(f"{artifact.source}: editable source is missing")
            continue
        if not png.is_file():
            errors.append(f"{artifact.png}: required PNG is missing")
            continue
        try:
            info = inspect_png(png)
        except (OSError, ValueError) as error:
            errors.append(f"{artifact.png}: invalid PNG raster: {error}")
            continue
        if info.width < artifact.minimum_width:
            errors.append(
                f"{artifact.png}: width {info.width} is below "
                f"{artifact.minimum_width}"
            )
        if info.height < artifact.minimum_height:
            errors.append(
                f"{artifact.png}: height {info.height} is below "
                f"{artifact.minimum_height}"
            )
        try:
            expected = source_digest(source)
        except OSError as error:
            errors.append(f"{artifact.source}: unreadable source: {error}")
            continue
        if info.text.get(artifact.key) != expected:
            errors.append(
                f"{artifact.png}: provenance differs from {artifact.source}"
            )
    return errors


def copy_fixture(destination: Path) -> None:
    """Copy only the eight files the gate consumes."""
    for artifact in ARTIFACTS:
        for relative in (artifact.png, artifact.source):
            source = ROOT / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def expect_failure(root: Path, needle: str, label: str) -> bool:
    errors = validate(root)
    if not any(needle in error for error in errors):
        print(f"selftest: {label} escaped: {errors}")
        return False
    return True


def expect_invalid(path: Path, content: bytes, needle: str, label: str) -> bool:
    path.write_bytes(content)
    try:
        inspect_png(path)
    except ValueError as error:
        if needle in str(error):
            return True
        print(f"selftest: {label} returned the wrong error: {error}")
        return False
    print(f"selftest: {label} escaped")
    return False


def selftest() -> int:
    baseline_errors = validate(ROOT)
    if baseline_errors:
        print("selftest: committed PNG precondition failed")
        for error in baseline_errors:
            print(error)
        return 1

    with tempfile.TemporaryDirectory(prefix="diagram-png-selftest-") as directory:
        fixture = Path(directory)
        copy_fixture(fixture)
        if validate(fixture):
            print("selftest: copied baseline failed")
            return 1

        for artifact in ARTIFACTS:
            png = fixture / artifact.png
            source = fixture / artifact.source
            png_bytes = png.read_bytes()
            source_bytes = source.read_bytes()

            png.unlink()
            if not expect_failure(fixture, artifact.png, f"missing {artifact.png}"):
                return 1
            png.write_bytes(png_bytes)

            png.write_bytes(b"not a PNG raster\n")
            if not expect_failure(fixture, artifact.png, f"non-raster {artifact.png}"):
                return 1
            png.write_bytes(png_bytes)

            source.write_bytes(source_bytes + b"\n")
            if not expect_failure(fixture, artifact.png, f"stale {artifact.png}"):
                return 1
            source.write_bytes(source_bytes)

        sample = fixture / ARTIFACTS[0].png
        original = sample.read_bytes()
        chunks = parse_chunks(original)

        no_idat = encode_chunks([chunk for chunk in chunks if chunk.kind != b"IDAT"])
        if not expect_invalid(sample, no_idat, "missing PNG image data", "missing IDAT"):
            return 1

        no_iend = encode_chunks([chunk for chunk in chunks if chunk.kind != b"IEND"])
        if not expect_invalid(sample, no_iend, "missing PNG end marker", "missing IEND"):
            return 1

        metadata_only = encode_chunks(
            [
                chunk
                for chunk in chunks
                if chunk.kind in (b"IHDR", b"tEXt", b"IEND")
            ]
        )
        if not expect_invalid(
            sample,
            metadata_only,
            "missing PNG image data",
            "metadata-only PNG",
        ):
            return 1

        truncated_chunks = list(chunks)
        last_idat = max(
            index
            for index, chunk in enumerate(truncated_chunks)
            if chunk.kind == b"IDAT"
        )
        payload = truncated_chunks[last_idat].payload
        if not payload:
            print("selftest: baseline carries an empty final IDAT")
            return 1
        truncated_chunks[last_idat] = Chunk(b"IDAT", payload[:-1])
        truncated = encode_chunks(truncated_chunks)
        if not expect_invalid(sample, truncated, "PNG raster", "truncated raster"):
            return 1

    print("diagram PNG selftest: OK (4 rasters, 16 mutation controls)")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:
        print(__doc__)
        return 2
    errors = validate(ROOT)
    if errors:
        for error in errors:
            print(error)
        print(f"diagram PNGs: FAIL ({len(errors)} findings)")
        return 1
    print(f"diagram PNGs: OK ({len(ARTIFACTS)} decoded source-bound rasters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
