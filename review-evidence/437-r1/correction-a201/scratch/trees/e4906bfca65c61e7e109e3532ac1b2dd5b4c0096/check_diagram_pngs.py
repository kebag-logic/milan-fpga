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
    load_pixel_manifest,
    parse_chunks,
    source_digest,
    verify_pixel_manifest,
    zero_raster_bytes,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("docs/diagrams/PNG_MANIFEST.json")
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
        "docs/diagrams/timesync_chain.png",
        "docs/diagrams/timesync_chain.drawio",
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
    Artifact(
        "docs/diagrams/wd_gptp_pdelay.png",
        "docs/diagrams/wd_gptp_pdelay.json",
        WAVEDROM_HASH_KEY,
    ),
)


def validate(root: Path) -> list[str]:
    """Return every PNG availability, raster, and provenance error."""
    errors: list[str] = []
    manifest_ok = False
    try:
        manifest = load_pixel_manifest(root / MANIFEST)
    except ValueError as error:
        errors.append(f"{MANIFEST}: {error}")
    else:
        artifacts = manifest["artifacts"]
        assert isinstance(artifacts, dict)
        expected = {artifact.png for artifact in ARTIFACTS}
        actual = set(artifacts)
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            errors.append(
                f"{MANIFEST}: artifact set differs: missing={missing}, extra={extra}"
            )
        else:
            manifest_ok = True
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
        if manifest_ok:
            try:
                verify_pixel_manifest(
                    root / MANIFEST,
                    artifact.png,
                    artifact.source,
                    png,
                    source,
                )
            except (OSError, ValueError) as error:
                errors.append(f"{artifact.png}: {error}")
    return errors


def copy_fixture(destination: Path) -> None:
    """Copy only the files the gate consumes."""
    manifest = destination / MANIFEST
    manifest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / MANIFEST, manifest)
    for artifact in ARTIFACTS:
        for relative in (artifact.png, artifact.source):
            source = ROOT / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def expect_failure(root: Path, needle: str, label: str) -> bool:
    """Whether the mutated fixture made `validate` report an error naming `needle`.

    A mutation that escapes is printed with the errors that were raised
    instead, because a silent False here is indistinguishable from a gate
    that checks nothing.
    """
    errors = validate(root)
    if not any(needle in error for error in errors):
        print(f"selftest: {label} escaped: {errors}")
        return False
    return True


def expect_invalid(path: Path, content: bytes, needle: str, label: str) -> bool:
    """Whether `content` is rejected by the decoder with `needle` in the reason.

    Accepting the wrong reason counts as a failure: a raster missing IDAT and
    one missing IEND must not be diagnosed with the same message.
    """
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
    """Prove every assertion this gate makes can fail.

    The committed rasters are copied to a fixture and broken one way at a
    time - deleted, replaced by non-PNG bytes, desynchronised from their
    source, blanked to a valid but empty raster, stripped of IDAT or IEND,
    truncated - and each mutation is required to be caught.
    """
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

            png.write_bytes(zero_raster_bytes(png))
            inspect_png(png)
            if not expect_failure(
                fixture,
                "raster differs from reviewed manifest",
                f"valid blank raster {artifact.png}",
            ):
                return 1
            png.write_bytes(png_bytes)

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

    print("diagram PNG selftest: OK (6 rasters, 28 mutation controls)")
    return 0


def main() -> int:
    """Check the committed diagrams, or run the mutation arm under --selftest;
    1 on findings, 2 on an argument this gate does not take."""
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
    print(
        f"diagram PNGs: OK ({len(ARTIFACTS)} decoded, source-bound, "
        "review-pinned rasters)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
