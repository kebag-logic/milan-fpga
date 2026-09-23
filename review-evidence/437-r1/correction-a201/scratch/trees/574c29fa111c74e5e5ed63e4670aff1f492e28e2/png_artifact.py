#!/usr/bin/env python3
"""Validate PNG rasters and attach source provenance.

The validator uses only Python's standard library.
It verifies chunks, checksums, compression, and scanlines.
Only non-interlaced PNG files are accepted.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import struct
import subprocess
import tempfile
import zlib
from dataclasses import dataclass
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_PIXELS = 100_000_000
PIXEL_MANIFEST_SCHEMA = 1
PIXEL_MANIFEST_POLICY = (
    "Decompressed raster bytes are review-pinned. PNG compression may vary; "
    "renderer changes require regeneration and visual review."
)
SHA256_RE = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True)
class Chunk:
    kind: bytes
    payload: bytes


@dataclass(frozen=True)
class PngInfo:
    width: int
    height: int
    bit_depth: int
    color_type: int
    raster_sha256: str
    text: dict[str, str]


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    """Encode one PNG chunk."""
    if len(kind) != 4:
        raise ValueError("PNG chunk names require four bytes")
    body = kind + payload
    return (
        struct.pack(">I", len(payload))
        + body
        + struct.pack(">I", zlib.crc32(body))
    )


def parse_chunks(data: bytes) -> list[Chunk]:
    """Parse complete chunks and verify every checksum."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("missing PNG signature")
    position = len(PNG_SIGNATURE)
    chunks: list[Chunk] = []
    ended = False
    while position < len(data):
        if position + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[position:position + 4])[0]
        end = position + 12 + length
        if end > len(data):
            raise ValueError("truncated PNG payload")
        kind = data[position + 4:position + 8]
        payload = data[position + 8:position + 8 + length]
        stored_crc = struct.unpack(">I", data[position + 8 + length:end])[0]
        if stored_crc != zlib.crc32(kind + payload):
            raise ValueError("invalid PNG checksum")
        chunks.append(Chunk(kind, payload))
        position = end
        if kind == b"IEND":
            ended = True
            if position != len(data):
                raise ValueError("data follows PNG end marker")
            break
    if not ended:
        raise ValueError("missing PNG end marker")
    return chunks


def encode_chunks(chunks: list[Chunk]) -> bytes:
    """Encode a complete PNG chunk list."""
    return PNG_SIGNATURE + b"".join(
        png_chunk(chunk.kind, chunk.payload) for chunk in chunks
    )


def zero_raster_bytes(path: Path) -> bytes:
    """Return a valid same-shape PNG containing zero-valued samples."""
    chunks = parse_chunks(path.read_bytes())
    header = next(chunk.payload for chunk in chunks if chunk.kind == b"IHDR")
    width, height, depth, color, _compression, _filtering, interlace = struct.unpack(
        ">IIBBBBB", header
    )
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
    if interlace != 0 or color not in channels:
        raise ValueError("zero-raster fixture requires supported non-interlaced PNG")
    row_bytes = (width * channels[color] * depth + 7) // 8
    raster = b"".join(b"\0" + b"\0" * row_bytes for _row in range(height))
    replacement = Chunk(b"IDAT", zlib.compress(raster))
    output: list[Chunk] = []
    inserted = False
    for chunk in chunks:
        if chunk.kind != b"IDAT":
            output.append(chunk)
        elif not inserted:
            output.append(replacement)
            inserted = True
    if not inserted:
        raise ValueError("zero-raster fixture lacks image data")
    return encode_chunks(output)


def inspect_png(path: Path) -> PngInfo:
    """Validate one complete, decodable, non-interlaced raster."""
    chunks = parse_chunks(path.read_bytes())
    if not chunks or chunks[0].kind != b"IHDR":
        raise ValueError("PNG header is not the first chunk")
    headers = [chunk for chunk in chunks if chunk.kind == b"IHDR"]
    if len(headers) != 1 or len(headers[0].payload) != 13:
        raise ValueError("PNG requires one valid header")
    ends = [chunk for chunk in chunks if chunk.kind == b"IEND"]
    if len(ends) != 1 or ends[0].payload or chunks[-1].kind != b"IEND":
        raise ValueError("PNG requires one final empty end marker")

    width, height, depth, color, compression, filtering, interlace = struct.unpack(
        ">IIBBBBB", headers[0].payload
    )
    if width == 0 or height == 0:
        raise ValueError("PNG dimensions must be positive")
    if width * height > MAX_PIXELS:
        raise ValueError("PNG raster exceeds the safety limit")
    if compression != 0 or filtering != 0:
        raise ValueError("unsupported PNG compression or filter method")
    if interlace != 0:
        raise ValueError("interlaced PNG raster is unsupported")

    allowed_depths = {
        0: {1, 2, 4, 8, 16},
        2: {8, 16},
        3: {1, 2, 4, 8},
        4: {8, 16},
        6: {8, 16},
    }
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
    if color not in allowed_depths or depth not in allowed_depths[color]:
        raise ValueError("unsupported PNG color type or bit depth")

    idat_indexes = [
        index for index, chunk in enumerate(chunks) if chunk.kind == b"IDAT"
    ]
    if not idat_indexes:
        raise ValueError("missing PNG image data")
    if idat_indexes != list(range(idat_indexes[0], idat_indexes[-1] + 1)):
        raise ValueError("PNG image-data chunks are not contiguous")
    compressed = b"".join(chunks[index].payload for index in idat_indexes)
    if not compressed:
        raise ValueError("empty PNG image data")

    row_bytes = (width * channels[color] * depth + 7) // 8
    expected_bytes = height * (row_bytes + 1)
    decoder = zlib.decompressobj()
    try:
        raster = decoder.decompress(compressed, expected_bytes + 1)
        if decoder.unconsumed_tail:
            raise ValueError("PNG raster exceeds declared dimensions")
        raster += decoder.flush()
    except zlib.error as error:
        raise ValueError(f"invalid PNG raster compression: {error}") from error
    if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError("truncated or trailing PNG raster data")

    if len(raster) != expected_bytes:
        raise ValueError(
            f"PNG raster length is {len(raster)}, expected {expected_bytes}"
        )
    for row in range(height):
        filter_byte = raster[row * (row_bytes + 1)]
        if filter_byte > 4:
            raise ValueError(f"invalid PNG row filter {filter_byte}")

    if color == 3:
        palette_indexes = [
            index for index, chunk in enumerate(chunks) if chunk.kind == b"PLTE"
        ]
        if len(palette_indexes) != 1 or palette_indexes[0] > idat_indexes[0]:
            raise ValueError("indexed PNG requires one preceding palette")

    visible_metadata = b"".join(
        chunk.kind + struct.pack(">I", len(chunk.payload)) + chunk.payload
        for chunk in chunks
        if chunk.kind in (b"PLTE", b"tRNS")
    )
    raster_material = (
        struct.pack(">IIBB", width, height, depth, color)
        + visible_metadata
        + raster
    )
    raster_sha256 = hashlib.sha256(raster_material).hexdigest()

    fields: dict[str, str] = {}
    for chunk in chunks:
        if chunk.kind != b"tEXt" or b"\0" not in chunk.payload:
            continue
        key_bytes, value_bytes = chunk.payload.split(b"\0", 1)
        key = key_bytes.decode("latin-1")
        if key in fields:
            raise ValueError(f"duplicate PNG text key: {key}")
        fields[key] = value_bytes.decode("latin-1")
    return PngInfo(width, height, depth, color, raster_sha256, fields)


def source_digest(path: Path) -> str:
    """Return the exact source-file digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new_pixel_manifest() -> dict[str, object]:
    """Return an empty manifest with the required review policy."""
    return {
        "schema": PIXEL_MANIFEST_SCHEMA,
        "renderer_policy": PIXEL_MANIFEST_POLICY,
        "artifacts": {},
    }


def load_pixel_manifest(path: Path) -> dict[str, object]:
    """Read and strictly validate one pixel-review manifest."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"pixel manifest is unreadable: {error}") from error
    if not isinstance(value, dict):
        raise ValueError("pixel manifest root must be an object")
    if set(value) != {"schema", "renderer_policy", "artifacts"}:
        raise ValueError("pixel manifest has unexpected root fields")
    if value["schema"] != PIXEL_MANIFEST_SCHEMA:
        raise ValueError("pixel manifest schema differs")
    if value["renderer_policy"] != PIXEL_MANIFEST_POLICY:
        raise ValueError("pixel manifest renderer policy differs")
    artifacts = value["artifacts"]
    if not isinstance(artifacts, dict):
        raise ValueError("pixel manifest artifacts must be an object")
    required = {
        "source",
        "source_sha256",
        "raster_sha256",
        "width",
        "height",
    }
    for name, entry in artifacts.items():
        if not isinstance(name, str) or not name:
            raise ValueError("pixel manifest artifact name is invalid")
        if not isinstance(entry, dict) or set(entry) != required:
            raise ValueError(f"pixel manifest entry is invalid: {name}")
        if not isinstance(entry["source"], str) or not entry["source"]:
            raise ValueError(f"pixel manifest source is invalid: {name}")
        for key in ("source_sha256", "raster_sha256"):
            digest = entry[key]
            if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
                raise ValueError(f"pixel manifest {key} is invalid: {name}")
        for key in ("width", "height"):
            dimension = entry[key]
            if not isinstance(dimension, int) or dimension <= 0:
                raise ValueError(f"pixel manifest {key} is invalid: {name}")
    return value


def verify_pixel_manifest(
    manifest_path: Path,
    artifact_name: str,
    source_name: str,
    png_path: Path,
    source_path: Path,
) -> PngInfo:
    """Match decompressed raster content against the reviewed manifest."""
    manifest = load_pixel_manifest(manifest_path)
    artifacts = manifest["artifacts"]
    assert isinstance(artifacts, dict)
    entry = artifacts.get(artifact_name)
    if not isinstance(entry, dict):
        raise ValueError(f"pixel manifest lacks {artifact_name}")
    if entry["source"] != source_name:
        raise ValueError(f"pixel manifest source path differs for {artifact_name}")
    expected_source = source_digest(source_path)
    if entry["source_sha256"] != expected_source:
        raise ValueError(f"source differs from reviewed manifest: {source_name}")
    info = inspect_png(png_path)
    if (entry["width"], entry["height"]) != (info.width, info.height):
        raise ValueError(f"dimensions differ from reviewed manifest: {artifact_name}")
    if entry["raster_sha256"] != info.raster_sha256:
        raise ValueError(f"raster differs from reviewed manifest: {artifact_name}")
    return info


def reviewed_png_current(
    manifest_path: Path,
    artifact_name: str,
    source_name: str,
    png_path: Path,
    source_path: Path,
    expected_dimensions: tuple[int, int],
    expected_text: dict[str, str],
) -> bool:
    """Check one generated PNG against source and review evidence."""
    try:
        info = verify_pixel_manifest(
            manifest_path,
            artifact_name,
            source_name,
            png_path,
            source_path,
        )
    except (OSError, ValueError):
        return False
    if (info.width, info.height) != expected_dimensions:
        return False
    return all(info.text.get(key) == value for key, value in expected_text.items())


def update_pixel_manifest(
    manifest_path: Path,
    artifact_name: str,
    source_name: str,
    png_path: Path,
    source_path: Path,
) -> PngInfo:
    """Record one newly rendered and visually reviewable raster."""
    if manifest_path.exists():
        manifest = load_pixel_manifest(manifest_path)
    else:
        manifest = new_pixel_manifest()
    artifacts = manifest["artifacts"]
    assert isinstance(artifacts, dict)
    info = inspect_png(png_path)
    artifacts[artifact_name] = {
        "source": source_name,
        "source_sha256": source_digest(source_path),
        "raster_sha256": info.raster_sha256,
        "width": info.width,
        "height": info.height,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    load_pixel_manifest(manifest_path)
    return info


def set_text_fields(path: Path, fields: dict[str, str]) -> None:
    """Replace selected PNG text fields."""
    inspect_png(path)
    keys = set(fields)
    chunks = []
    inserted = False
    for chunk in parse_chunks(path.read_bytes()):
        if chunk.kind == b"tEXt" and b"\0" in chunk.payload:
            key = chunk.payload.split(b"\0", 1)[0].decode("latin-1")
            if key in keys:
                continue
        chunks.append(chunk)
        if chunk.kind == b"IHDR":
            for key, value in fields.items():
                if not key or len(key.encode("latin-1")) > 79 or "\0" in key:
                    raise ValueError(f"invalid PNG text key: {key!r}")
                payload = key.encode("latin-1") + b"\0" + value.encode("latin-1")
                chunks.append(Chunk(b"tEXt", payload))
            inserted = True
    if not inserted:
        raise ValueError("cannot tag PNG without a header")
    path.write_bytes(encode_chunks(chunks))
    inspect_png(path)


def render_svg_png(
    svg: str,
    output: Path,
    width: int,
    fields: dict[str, str],
    background: str = "white",
) -> PngInfo:
    """Render SVG through librsvg, then attach provenance."""
    renderer = shutil.which("rsvg-convert")
    if renderer is None:
        raise RuntimeError("rsvg-convert is required for PNG rendering")
    with tempfile.TemporaryDirectory(prefix="diagram-raster-") as directory:
        source = Path(directory) / "diagram.svg"
        source.write_text(svg, encoding="utf-8")
        subprocess.run(
            [
                renderer,
                "-b",
                background,
                "-w",
                str(width),
                str(source),
                "-o",
                str(output),
            ],
            check=True,
        )
    set_text_fields(output, fields)
    return inspect_png(output)
