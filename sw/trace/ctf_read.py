#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctf_read.py - read a Milan CTF trace with nothing but the Python standard library.

WHY THIS EXISTS.  The canonical reader for CTF is `babeltrace2`, and it is the
right tool when it is installed.  It is a C library with its own plugin system,
it is not installed on every machine that will ever have to look at one of these
traces, and it cannot be a dependency of a repo gate.  This reader closes that
gap: `python3 sw/trace/ctf_read.py <segment-or-dir>` decodes a trace anywhere
python3 runs.

IT IS DRIVEN BY THE SHIPPED `metadata`, NOT BY A SECOND COPY OF THE LAYOUT.
That is deliberate, and it is the whole reason this file parses TSDL instead of
hard-coding 23 struct layouts: a reader that carries its own idea of the wire
format is a model that shares the implementation's bugs
(docs/limitations/RECURRING_DEFECT_PATTERNS.md pattern 7), and it would decode a
trace written by a DIFFERENT ABI version into plausible nonsense.  Point it at
the `metadata` that travelled with the segments and it decodes what was actually
written.

TORN TRACES ARE THE NORMAL CASE, not an error path.  A power cut truncates the
segment being written, and a decompressed prefix of an xz stream ends wherever
it ends.  So: every packet is structurally validated before it is trusted
(magic, declared sizes, buffer room), decoding STOPS at the first packet that
does not validate, and the caller is told how many whole packets were recovered.
Reporting "42 packets, then truncated" is the contract; guessing past the damage
is not.

Supported subset: CTF 1.8 as barectf 3.x emits it - byte-aligned integers,
enumerations over integers, null-terminated strings, one data stream type.  A
metadata document using anything else (bit-packed fields, floats, sequences,
variants) is REFUSED with a clear message rather than mis-decoded.

usage:
    ctf_read.py <path> [--metadata PATH] [--format text|json|summary]
                       [--event NAME]... [--min-sev SEV]

    <path>  a directory holding `metadata` plus stream files, OR a single
            stream file (then --metadata is required unless `metadata` sits
            next to it), OR a `.xz` segment (decompressed on the fly, truncated
            input tolerated).
"""

import argparse
import json
import lzma
import re
import struct
import sys
from pathlib import Path
from typing import Any

CTF_MAGIC = 0xC1FC1FC1


# --------------------------------------------------------------------------
# TSDL parsing - the subset barectf emits
# --------------------------------------------------------------------------

class MetadataError(Exception):
    pass


_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


def _strip_comments(text):
    return _COMMENT.sub(" ", text)


def _match_brace(text, i):
    """Index just past the `}` matching the `{` at text[i]."""
    depth = 0
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise MetadataError("unbalanced braces in metadata")


class IntType:
    __slots__ = ("size", "signed", "align", "base", "mapped_clock")

    def __init__(self, props):
        self.size = int(props.get("size", 0))
        self.signed = props.get("signed", "false") == "true"
        self.align = int(props.get("align", 8))
        self.base = int(props.get("base", 10))
        self.mapped_clock = props.get("map")
        if self.size % 8 or self.align % 8:
            raise MetadataError(
                f"bit-packed integer (size={self.size} align={self.align}) - "
                "this reader only supports byte-aligned fields; use babeltrace2")

    @property
    def nbytes(self) -> int:
        """The field's width in whole bytes; the constructor already refused a
        size this reader could not divide."""
        return self.size // 8


class EnumType(IntType):
    __slots__ = ("labels",)

    def __init__(self, props, labels):
        super().__init__(props)
        self.labels = labels


class StrType:
    __slots__ = ()
    size = 0
    align = 8


_PROP = re.compile(r"([A-Za-z_][\w.]*)\s*=\s*([^;]+);")
_LABEL = re.compile(r'"([^"]*)"\s*=\s*(-?\d+)\s*(?:\.\.\.\s*(-?\d+))?\s*,?')


def _props(body):
    return {m.group(1): m.group(2).strip() for m in _PROP.finditer(body)}


def _parse_struct(text):
    """`struct { ... } align(N)` -> [(name, type), ...].  `text` starts at `struct`."""
    i = text.index("{")
    end = _match_brace(text, i)
    body = text[i + 1:end - 1]
    members = []
    pos = 0
    while True:
        m = re.compile(r"\b(integer|enum|string|floating_point|variant|sequence)\b").search(body, pos)
        if not m:
            break
        kind = m.group(1)
        if kind in ("floating_point", "variant", "sequence"):
            raise MetadataError(
                f"unsupported field class `{kind}` - use babeltrace2 for this trace")
        b1 = body.index("{", m.end())
        e1 = _match_brace(body, b1)
        props = _props(body[b1 + 1:e1 - 1])
        if kind == "enum":
            b2 = body.index("{", e1)
            e2 = _match_brace(body, b2)
            labels = {}
            for lm in _LABEL.finditer(body[b2 + 1:e2 - 1]):
                lo = int(lm.group(2))
                hi = int(lm.group(3)) if lm.group(3) else lo
                for v in range(lo, hi + 1):
                    labels[v] = lm.group(1)
            ftype, after = EnumType(props, labels), e2
        elif kind == "string":
            ftype, after = StrType(), e1
        else:
            ftype, after = IntType(props), e1
        semi = body.index(";", after)
        name = body[after:semi].strip()
        # skip static-array declarators - not emitted by our config, refuse loudly
        if "[" in name:
            raise MetadataError(f"array member `{name}` unsupported - use babeltrace2")
        members.append((name, ftype))
        pos = semi + 1
    return members, end


class Metadata:
    """The decode ABI, as parsed from a shipped `metadata` document."""

    def __init__(self, text):
        text = _strip_comments(text)
        self.byte_order = "le"
        self.env = {}
        self.clocks = {}
        self.packet_header = []
        self.packet_context = []
        self.event_header = []
        self.event_context = []
        self.events = {}          # id -> (name, [members])
        self._parse(text)
        self._validate()

    # -- parsing ---------------------------------------------------------
    def _parse(self, text):
        pos = 0
        block = re.compile(r"\b(trace|env|clock|stream|event|typealias|callsite)\b")
        while True:
            m = block.search(text, pos)
            if not m:
                break
            kind = m.group(1)
            try:
                b = text.index("{", m.end())
            except ValueError:
                break
            e = _match_brace(text, b)
            body = text[b + 1:e - 1]
            if kind == "trace":
                self._parse_trace(body)
            elif kind == "env":
                self.env = {k: v.strip().strip('"') for k, v in _props(body).items()}
            elif kind == "clock":
                p = _props(body)
                self.clocks[p.get("name", "?")] = p
            elif kind == "stream":
                self._parse_stream(body)
            elif kind == "event":
                self._parse_event(body)
            pos = e

    def _parse_trace(self, body):
        bo = re.search(r"byte_order\s*=\s*(\w+)\s*;", body)
        if bo:
            self.byte_order = bo.group(1)
        self.packet_header = self._named_struct(body, "packet.header")

    def _parse_stream(self, body):
        self.packet_context = self._named_struct(body, "packet.context")
        self.event_header = self._named_struct(body, "event.header")
        self.event_context = self._named_struct(body, "event.context")

    def _parse_event(self, body):
        eid = re.search(r"\bid\s*=\s*(\d+)\s*;", body)
        name = re.search(r'\bname\s*=\s*"([^"]*)"\s*;', body)
        fields = self._named_struct(body, "fields")
        if eid is None or name is None:
            raise MetadataError("event block without id or name")
        self.events[int(eid.group(1))] = (name.group(1), fields)

    @staticmethod
    def _named_struct(body, label):
        m = re.search(re.escape(label) + r"\s*:=\s*", body)
        if not m:
            return []
        members, _ = _parse_struct(body[m.end():])
        return members

    # -- sanity ----------------------------------------------------------
    def _validate(self):
        names = [n for n, _ in self.packet_header]
        if "magic" not in names:
            raise MetadataError(
                "packet header has no `magic` field - this reader needs it as the "
                "resync anchor for torn traces")
        for want in ("packet_size", "content_size"):
            if want not in [n for n, _ in self.packet_context]:
                raise MetadataError(f"packet context has no `{want}` field")
        if "id" not in [n for n, _ in self.event_header]:
            raise MetadataError("event header has no `id` field")

    @property
    def abi(self) -> str:
        """The trace ABI version the writer stamped into env, or "?" - a
        decode of a trace whose ABI is unknown is still reported as such."""
        return self.env.get("milan_trace_abi", "?")

    def event_ids(self) -> dict[int, str]:
        """{event id: event name} as this metadata declares them."""
        return {eid: n for eid, (n, _) in self.events.items()}


# --------------------------------------------------------------------------
# decoding
# --------------------------------------------------------------------------

class TruncatedTrace(Exception):
    """Raised internally when the buffer runs out mid-structure."""


class _Cursor:
    def __init__(self, buf, off, little):
        self.buf = buf
        self.off = off
        self.little = little

    def align(self, nbits: int) -> None:
        """Advance the cursor to the field's byte alignment."""
        nbytes = max(1, nbits // 8)
        rem = self.off % nbytes
        if rem:
            self.off += nbytes - rem

    def read(self, ftype: IntType | StrType) -> int | str:
        """One field's value, raising TruncatedTrace rather than reading past
        the end of a torn buffer."""
        if isinstance(ftype, StrType):
            end = self.buf.find(b"\0", self.off)
            if end < 0:
                raise TruncatedTrace("unterminated string")
            s = self.buf[self.off:end].decode("utf-8", "replace")
            self.off = end + 1
            return s
        self.align(ftype.align)
        n = ftype.nbytes
        if self.off + n > len(self.buf):
            raise TruncatedTrace("integer past end of buffer")
        raw = self.buf[self.off:self.off + n]
        self.off += n
        return int.from_bytes(raw, "little" if self.little else "big",
                              signed=ftype.signed)

    def read_struct(
            self, members: list[tuple[str, IntType | StrType]]
    ) -> dict[str, int | str]:
        """{field name: value} for one declared structure, read in order."""
        out = {}
        for name, ftype in members:
            out[name] = self.read(ftype)
        return out


def _label(ftype, value):
    if isinstance(ftype, EnumType):
        return ftype.labels.get(value, f"<{value}>")
    return value


class Packet:
    __slots__ = ("header", "context", "events", "offset", "size_bytes")


def decode(
        buf: bytes, meta: Metadata
) -> tuple[list[Packet], list[dict[str, Any]], str | None]:
    """Decode `buf` into (packets, events, note).

    Stops at the first structurally invalid or incomplete packet.  `note` is
    None on a clean decode, otherwise a human-readable reason - which is the
    normal outcome for the segment that was in flight when the power went.
    """
    little = meta.byte_order in ("le", "little_endian")
    packets, events = [], []
    off = 0
    note = None

    while off < len(buf):
        # An erased or zero-padded tail is a normal end, not damage.
        if buf[off:off + 4] in (b"\xff\xff\xff\xff", b"\x00\x00\x00\x00"):
            break
        cur = _Cursor(buf, off, little)
        try:
            hdr = cur.read_struct(meta.packet_header)
            if hdr.get("magic") != CTF_MAGIC:
                note = f"bad packet magic 0x{hdr.get('magic', 0):08X} at byte {off}"
                break
            ctx = cur.read_struct(meta.packet_context)
            psize = ctx["packet_size"] // 8
            csize = ctx["content_size"] // 8
            if psize == 0 or csize > psize:
                note = f"packet {len(packets)}: declared sizes are impossible"
                break
            if off + psize > len(buf):
                note = (f"packet {len(packets)} truncated: needs {psize} B, "
                        f"{len(buf) - off} B left")
                break

            pkt = Packet()
            pkt.header, pkt.context, pkt.events = hdr, ctx, []
            pkt.offset, pkt.size_bytes = off, psize

            base_ts = ctx.get("timestamp_begin", 0)
            last_ts = base_ts
            content_end = off + csize
            while cur.off < content_end:
                eh = cur.read_struct(meta.event_header)
                eid = eh["id"]
                if eid not in meta.events:
                    raise TruncatedTrace(f"unknown event id {eid}")
                name, members = meta.events[eid]
                cc = cur.read_struct(meta.event_context)
                payload = cur.read_struct(members)
                ts = _extend_ts(meta, eh, base_ts, last_ts)
                last_ts = ts
                rec = {
                    "ts": ts,
                    "name": name,
                    "id": eid,
                    "packet": len(packets),
                    "ctx": {k: _label(dict(meta.event_context)[k], v)
                            for k, v in cc.items()},
                    "payload": {k: _label(dict(members)[k], v)
                                for k, v in payload.items()},
                }
                pkt.events.append(rec)
                events.append(rec)
            packets.append(pkt)
            off += psize
        except TruncatedTrace as e:
            note = f"packet {len(packets)}: {e}"
            break

    return packets, events, note


def _extend_ts(meta, eh, base_ts, last_ts):
    """Rebuild a 64-bit timestamp from a possibly truncated event-header field."""
    hdr_types = dict(meta.event_header)
    tname = "timestamp" if "timestamp" in hdr_types else None
    if tname is None:
        return last_ts
    bits = hdr_types[tname].size
    raw = eh[tname]
    if bits >= 64:
        return raw
    mask = (1 << bits) - 1
    ts = (base_ts & ~mask) | raw
    if ts < last_ts:
        ts += mask + 1
    return ts


# --------------------------------------------------------------------------
# input handling
# --------------------------------------------------------------------------

def read_stream_bytes(path: Path) -> tuple[bytes, bool]:
    """Bytes of a stream file, decompressing `.xz` and tolerating truncation.

    A truncated xz stream still yields every byte the decoder could produce -
    MEASURED, not assumed: see docs/design/TRACE_LOGGING.md section 8.  The
    liblzma error at the end is expected and is not a failure.
    """
    raw = path.read_bytes()
    if path.suffix != ".xz":
        return raw, False
    d = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
    out = bytearray()
    truncated = False
    try:
        for i in range(0, len(raw), 65536):
            out += d.decompress(raw[i:i + 65536])
        if not d.eof:
            truncated = True
    except (lzma.LZMAError, EOFError):
        truncated = True
    return bytes(out), truncated


def _looks_like_stream(path):
    """A CTF stream (packet magic) or an xz segment.  Anything else in the
    directory - a stats file, an operator's note - is not a decode failure."""
    if not path.is_file():
        return False
    with path.open("rb") as f:
        head = f.read(6)
    return (head[:6] == b"\xfd7zXZ\x00" or
            int.from_bytes(head[:4], "little") == CTF_MAGIC or
            int.from_bytes(head[:4], "big") == CTF_MAGIC)


def load(
        path: str | Path, metadata_path: str | Path | None = None
) -> tuple[Metadata, list[tuple[str, bytes, bool]]]:
    """(metadata, [(name, bytes, truncated)]) for a dir, a file or an .xz.

    `path` is accepted as either a `str` or a `Path` because callers outside
    this module hand it a `str`; the stream NAMES come back as `str` for the
    same reason - they are report text, not paths, and a caller joins them to
    nothing.  Stream order stays a sort of those names, not of `Path`s, so a
    dotted or dashed segment name keeps the order `ls` would show.
    """
    root = Path(path)
    if root.is_dir():
        mpath = Path(metadata_path) if metadata_path else root / "metadata"
        streams = sorted(f.name for f in root.iterdir()
                         if f.name != "metadata" and not f.name.startswith(".")
                         and _looks_like_stream(f))
        items = [(f,) + read_stream_bytes(root / f) for f in streams]
    else:
        mpath = (Path(metadata_path) if metadata_path
                 else root.parent / "metadata")
        items = [(root.name,) + read_stream_bytes(root)]
    if not mpath.is_file():
        raise MetadataError(
            f"no metadata at {mpath} - a CTF trace cannot be decoded without the "
            "metadata that was written WITH it (pass --metadata)")
    meta = Metadata(mpath.read_text(encoding="utf-8", errors="replace"))
    return meta, items


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

SEVS = ["DEBUG", "INFO", "NOTICE", "WARN", "ERROR", "FATAL"]


def _fmt_value(v):
    if isinstance(v, int) and v > 0xFFFF:
        return f"0x{v:X}"
    return v


def main(argv: list[str] | None = None) -> int:
    """Decode one trace and print it in the requested shape.

    2 when the metadata written WITH the trace could not be read, 0 otherwise:
    a torn trace is reported in the notes, never in the exit status, because
    the recovered prefix is still the evidence the reader came for.
    """
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path")
    ap.add_argument("--metadata")
    ap.add_argument("--format", choices=("text", "json", "summary"),
                    default="text")
    ap.add_argument("--event", action="append", default=[],
                    help="only this event name (repeatable)")
    ap.add_argument("--min-sev", choices=SEVS, default="DEBUG")
    args = ap.parse_args(argv)

    try:
        meta, items = load(args.path, args.metadata)
    except MetadataError as e:
        print(f"ctf_read: {e}", file=sys.stderr)
        return 2

    min_sev = SEVS.index(args.min_sev)
    all_events, notes, npackets = [], [], 0
    for name, blob, xz_trunc in items:
        packets, events, note = decode(blob, meta)
        npackets += len(packets)
        all_events.extend(events)
        if xz_trunc:
            notes.append(f"{name}: xz stream truncated, "
                         f"{len(blob)} B recovered")
        if note:
            notes.append(f"{name}: {note}")

    keep = []
    for e in all_events:
        if args.event and e["name"] not in args.event:
            continue
        sev = e["ctx"].get("sev", "DEBUG")
        if isinstance(sev, str) and sev in SEVS and SEVS.index(sev) < min_sev:
            continue
        keep.append(e)

    if args.format == "json":
        print(json.dumps({"abi": meta.abi, "packets": npackets,
                          "notes": notes, "events": keep}, indent=1))
    elif args.format == "summary":
        counts = {}
        for e in all_events:
            counts[e["name"]] = counts.get(e["name"], 0) + 1
        print(f"abi={meta.abi} packets={npackets} events={len(all_events)}")
        for k in sorted(counts, key=lambda k: -counts[k]):
            print(f"  {counts[k]:8d}  {k}")
        for n in notes:
            print(f"  note: {n}")
    else:
        for e in keep:
            payload = " ".join(f"{k}={_fmt_value(v)}"
                               for k, v in e["payload"].items())
            print(f"[{e['ts']:>16}] {e['ctx'].get('sev', '?'):<6} "
                  f"{e['ctx'].get('src', '?'):<9} {e['name']:<17} {payload}")
        for n in notes:
            print(f"# note: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
