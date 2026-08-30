#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""trace_segment.py - workstation trace bundles: pack, unpack, rotate, verify.

A SEGMENT is the unit of compression, rotation and loss.  One segment = one
independent xz stream = one file. An interrupted workstation pack can damage
only the file being replaced; every completed segment remains independently
decodable. That is why rotation is by file rather than by appending to one
growing archive.

The filter chain below is PINNED and MEASURED (docs/design/TRACE_LOGGING.md
section 7).  Do not "improve" it without re-running
sw/trace/test_trace_roundtrip.py, which reports the ratio it actually achieves.

    LZMA2 preset 0, dictionary = the segment size (256 KiB), CRC-32, one block

  Measured on 1.75 MiB of traces this producer really wrote (9 segments), host,
  best of 5:

    preset 0  dict 256 KiB   ratio 0.2104   29.5 MB/s    8.9 ms / 256 KiB
    preset 2  dict 256 KiB   ratio 0.2092   23.8 MB/s   11.0 ms
    preset 3  dict 256 KiB   ratio 0.2092   19.8 MB/s   13.2 ms
    preset 4  dict 256 KiB   ratio 0.1936    6.9 MB/s   38.2 ms
    preset 6e dict 256 KiB   ratio 0.1997    5.3 MB/s   49.6 ms
    xz -9e   (dict 64 MiB)   ratio 0.1997    2.7 MB/s   96.9 ms

  * THE RATIO CLIFF IS THE MATCH FINDER, NOT THE PRESET NUMBER. Presets 0-3
    (HC4) all land within 0.6 % of each other; presets 4+ (BT4) buy ~7 % of the
    bytes for 3-6x the workstation CPU time. Use the cheapest HC4 member.
  * A DICTIONARY LARGER THAN THE SEGMENT IS DEAD WEIGHT: nothing can match
    beyond the start of the input.  Capping it at the segment size holds the
    encoder to a measured ~9.2 MiB of address space, against 101 MiB for
    `xz -6` and 679 MiB for `xz -9`.
  * CRC-32, not the xz default CRC-64: the round-trip gate proves it catches
    damaged bundles without doubling the check field.
  * ONE BLOCK, no `--block-size`.  Independent blocks cost 7-15 % of the ratio
    (measured) and buy nothing here: a truncated single-block xz stream still
    decodes proportionally to the bytes that survived (MEASURED - gate 8 of
    test_trace_roundtrip.py), and CTF packets are self-delimiting, so the reader
    stops cleanly at the last whole packet.  The honest cost of one block is
    that NONE of a truncated segment is check-verified; the reader's CTF packet
    validation is what admits the recovered whole-packet prefix.

usage:
    trace_segment.py pack   <raw.ctf>... -o <dir>       raw CTF -> .ctf.xz
    trace_segment.py unpack <dir> -o <outdir>           -> babeltrace2-ready dir
    trace_segment.py verify <dir>                       decode + report
    trace_segment.py rotate <dir> --budget BYTES        apply the eviction policy
    trace_segment.py ratio  <raw.ctf>...                measure the chain
"""

import argparse
import lzma
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctf_read  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
METADATA = os.path.join(HERE, "generated", "metadata")

# ---- the pinned container format ----------------------------------------
SEGMENT_BYTES = 256 * 1024        # uncompressed segment = 64 packets x 4 KiB
XZ_PRESET = 0
XZ_DICT = SEGMENT_BYTES
XZ_CHECK = lzma.CHECK_CRC32
SEG_RE = re.compile(r"^seg-(\d{6})\.ctf(?:\.xz)?$")

# The workstation bundle keeps the repository's reserved `user` slot as a
# compatibility size ceiling, minus five erase blocks reserved for other
# artifacts. The tool itself writes only the output directory supplied on the
# workstation; it never opens a target path. Expressing the ceiling as
# "slot minus reserve" keeps `budget + reserve == slot` true by construction.
#
# DERIVED, NOT RESTATED. This was `1536 * 1024` while the source map still
# described a 2 MiB slot; flash-map v5 later took `user` down to 1 MiB. The
# constant did not move, so the bundle ceiling became larger than its authority and the
# gate that should have caught it (test_trace_roundtrip gate 1) was asserting
# the old 2 MiB too - two copies of one number, both stale, agreeing with each
# other and with nothing else.  Reading the slot means the budget cannot
# outlive the map again.
def _user_slot(default=(2 * 1024 * 1024, 64 * 1024)):
    """Compatibility ceiling and erase-block size from FLASHBOOT_RESERVED.

    Falls back to `default` when the SoC source is not readable, so this
    module still works in a bare checkout - but says so on stderr.  `default`
    is the stale 2 MiB constant the note above records as a shipped defect, so
    a silent fallback would re-arm it.
    """
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(HERE), "litex"))
        import flash_map as _fm
        rows, _fs, erase = _fm.load_map()
        return [r for r in rows if r[0] == "user"][0][2], erase
    except Exception as exc:
        print(f"trace_segment: WARNING: could not read the flash map "
              f"({exc!r}); falling back to the hardcoded "
              f"{default[0]} B trace-bundle ceiling, which may exceed the map",
              file=sys.stderr)
        return default


#: erase blocks withheld from the compatibility bundle ceiling
USER_RESERVE_BLOCKS = 5

USER_SLOT_BYTES, USER_ERASE_BYTES = _user_slot()
DEFAULT_LOG_BUDGET = USER_SLOT_BYTES - USER_RESERVE_BLOCKS * USER_ERASE_BYTES

# Segment 0 is PINNED: the first fault after a boot is the one that started the
# cascade, and a pure oldest-first ring is guaranteed to evict it first.
PINNED_SEGMENT = 0


def _filters():
    return [{"id": lzma.FILTER_LZMA2, "preset": XZ_PRESET, "dict_size": XZ_DICT}]


def compress(data):
    return lzma.compress(data, format=lzma.FORMAT_XZ, check=XZ_CHECK,
                         filters=_filters())


def decompress_tolerant(blob):
    """(plaintext, truncated).  A truncated stream yields its whole prefix."""
    d = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
    out = bytearray()
    try:
        for i in range(0, len(blob), 65536):
            out += d.decompress(blob[i:i + 65536])
        return bytes(out), not d.eof
    except (lzma.LZMAError, EOFError):
        return bytes(out), True


def segment_number(name):
    m = SEG_RE.match(os.path.basename(name))
    return int(m.group(1)) if m else None


def segments(dirpath):
    """[(number, path)] sorted oldest first."""
    out = []
    for f in os.listdir(dirpath):
        n = segment_number(f)
        if n is not None:
            out.append((n, os.path.join(dirpath, f)))
    return sorted(out)


# ---- commands ------------------------------------------------------------

def cmd_pack(args):
    os.makedirs(args.o, exist_ok=True)
    total_in = total_out = 0
    for src in args.raw:
        data = open(src, "rb").read()
        if len(data) > SEGMENT_BYTES:
            print(f"trace_segment: {src} is {len(data)} B, over the "
                  f"{SEGMENT_BYTES} B segment ceiling", file=sys.stderr)
            return 1
        blob = compress(data)
        n = segment_number(src)
        base = f"seg-{n:06d}.ctf.xz" if n is not None else \
            os.path.basename(src) + ".xz"
        # Write, fsync, then rename on the workstation: the reader must never
        # see a half-written segment.
        tmp = os.path.join(args.o, base + ".partial")
        with open(tmp, "wb") as f:
            f.write(blob)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, os.path.join(args.o, base))
        total_in += len(data)
        total_out += len(blob)
        print(f"  {os.path.basename(src):>20} {len(data):8d} -> {len(blob):8d} B "
              f"({len(blob) / max(1, len(data)):.4f})")
    if not os.path.exists(os.path.join(args.o, "metadata")):
        shutil.copyfile(METADATA, os.path.join(args.o, "metadata"))
    print(f"packed {total_in} -> {total_out} B  ratio "
          f"{total_out / max(1, total_in):.4f}")
    return 0


def cmd_unpack(args):
    """Produce a directory babeltrace2 (and ctf_read.py) can open directly.

    The metadata is COPIED IN, always.  Event-record type ids are assigned by
    sorted event name, so a trace decoded against a different build's metadata
    is not "slightly off", it is wrong - see the header of milan_trace.yaml.
    """
    os.makedirs(args.o, exist_ok=True)
    src_meta = os.path.join(args.dir, "metadata")
    shutil.copyfile(src_meta if os.path.isfile(src_meta) else METADATA,
                    os.path.join(args.o, "metadata"))
    truncated = []
    with open(os.path.join(args.o, "stream_0"), "wb") as out:
        for n, path in segments(args.dir):
            blob = open(path, "rb").read()
            if path.endswith(".xz"):
                data, trunc = decompress_tolerant(blob)
                if trunc:
                    truncated.append(n)
            else:
                data = blob
            out.write(data)
    print(f"unpacked {len(segments(args.dir))} segment(s) -> {args.o}")
    for n in truncated:
        print(f"  note: segment {n} was truncated; its readable prefix was kept")
    print(f"read it with:  python3 {os.path.relpath(__file__)} verify {args.o}")
    print(f"          or:  babeltrace2 {args.o}     (if installed)")
    return 0


def cmd_verify(args):
    meta = ctf_read.Metadata(open(_meta_for(args.dir), encoding="utf-8").read())
    total_pkts = total_evts = 0
    bad = 0
    for n, path in segments(args.dir) or [(None, args.dir)]:
        blob = open(path, "rb").read()
        trunc = False
        if path.endswith(".xz"):
            blob, trunc = decompress_tolerant(blob)
        packets, events, note = ctf_read.decode(blob, meta)
        total_pkts += len(packets)
        total_evts += len(events)
        flag = ""
        if trunc:
            flag += " [xz truncated]"
        if note:
            flag += f" [{note}]"
            bad += 1
        print(f"  seg {n if n is not None else '-'}: {len(packets):4d} packets "
              f"{len(events):6d} events{flag}")
    print(f"total {total_pkts} packets, {total_evts} events, "
          f"{bad} segment(s) with a note")
    return 0


def cmd_rotate(args):
    """Apply the eviction policy and print what it did.

    OLDEST-FIRST, WITH ONE PINNED SEGMENT.  The alternative - stop logging when
    full - guarantees silence exactly when the box has been up long enough to
    hit the interesting bug, which is the opposite of what a fault log is for.
    The known weakness of a pure ring (the first fault gets overwritten by the
    noise it caused) is bought off with one pinned segment rather than by
    changing the policy.
    """
    segs = segments(args.dir)
    sizes = {n: os.path.getsize(p) for n, p in segs}
    total = sum(sizes.values())
    removed = []
    for n, path in segs:
        if total <= args.budget:
            break
        if n == PINNED_SEGMENT and not args.evict_pinned:
            continue
        total -= sizes[n]
        removed.append(n)
        if not args.dry_run:
            os.remove(path)
    print(f"budget {args.budget} B; {len(segs)} segment(s), "
          f"{sum(sizes.values())} B -> {total} B")
    if removed:
        print(f"  evicted oldest-first: {removed}")
    if total > args.budget:
        print("  WARNING: still over budget - the pinned segment alone exceeds it")
        return 1
    return 0


def cmd_ratio(args):
    total_in = total_out = 0
    for src in args.raw:
        data = open(src, "rb").read()
        blob = compress(data)
        total_in += len(data)
        total_out += len(blob)
        print(f"  {os.path.basename(src):>20} {len(data):8d} -> {len(blob):8d} "
              f"({len(blob) / max(1, len(data)):.4f})")
    print(f"chain: LZMA2 preset={XZ_PRESET & 0xFF}"
          f"{'e' if XZ_PRESET & lzma.PRESET_EXTREME else ''} "
          f"dict={XZ_DICT} check=CRC32")
    print(f"total {total_in} -> {total_out} B  ratio "
          f"{total_out / max(1, total_in):.4f} "
          f"({total_in / max(1, total_out):.2f}x)")
    return 0


def _meta_for(dirpath):
    p = os.path.join(dirpath, "metadata")
    return p if os.path.isfile(p) else METADATA


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pack")
    p.add_argument("raw", nargs="+")
    p.add_argument("-o", required=True)
    p.set_defaults(fn=cmd_pack)

    p = sub.add_parser("unpack")
    p.add_argument("dir")
    p.add_argument("-o", required=True)
    p.set_defaults(fn=cmd_unpack)

    p = sub.add_parser("verify")
    p.add_argument("dir")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("rotate")
    p.add_argument("dir")
    p.add_argument("--budget", type=int, default=DEFAULT_LOG_BUDGET)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--evict-pinned", action="store_true")
    p.set_defaults(fn=cmd_rotate)

    p = sub.add_parser("ratio")
    p.add_argument("raw", nargs="+")
    p.set_defaults(fn=cmd_ratio)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
