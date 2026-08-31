#!/usr/bin/env python3
"""Validate PNG rasters and attach source provenance.

The validator uses only Python's standard library.
It verifies chunks, checksums, compression, and scanlines.
Only non-interlaced PNG files are accepted.
"""

from __future__ import annotations

import hashlib
import shutil
import struct
import subprocess
import tempfile
import zlib
from dataclasses import dataclass
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_PIXELS = 100_000_000


@dataclass(frozen=True)
class Chunk:
    kind: bytes
    payload: bytes


@dataclass(frozen=True)
class PngInfo:
    width: int
    height: int
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

    fields: dict[str, str] = {}
    for chunk in chunks:
        if chunk.kind != b"tEXt" or b"\0" not in chunk.payload:
            continue
        key_bytes, value_bytes = chunk.payload.split(b"\0", 1)
        key = key_bytes.decode("latin-1")
        if key in fields:
            raise ValueError(f"duplicate PNG text key: {key}")
        fields[key] = value_bytes.decode("latin-1")
    return PngInfo(width, height, fields)


def source_digest(path: Path) -> str:
    """Return the exact source-file digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
