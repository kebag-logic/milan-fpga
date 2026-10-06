#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gen_nvm_window.py - a saved-state window for a datapath leg to serve.

The firmware boots the saved state by copying a verified KLJ2 slot into the
reserved main-memory window, telling KL_nvm_backend where the record area is
(the section 8.2 control tuple) and marking it valid; the restore walk then
reads records through the backend's memory face (docs/design/
SAVED_STATE_MATERIALIZATION.md section 5.3). A desk leg that wants a restore
with something to restore needs the same three things, and this script makes
them from the repository's own codec rather than from a second description of
the record layout:

  * the record set and every payload length come from scripts/nvm_shape.py's
    inventory of the named config (the one check_nvm_record_space.py and the
    firmware's generated constants read);
  * each record is framed by scripts/nvm_klj2.py, an ERASED span unless the
    command line names it, and the container is assembled by the same module;
  * the container is decoded again by that module's section 6.2 acceptance
    rules, and nothing is written unless it is accepted with exactly the named
    records applied.

Usage: gen_nvm_window.py <config.yaml> <out.txt> [--record ID=HEXPAYLOAD]...

ID is a record id (0x30 is STREAM_INPUT 0's format) and HEXPAYLOAD its payload
bytes, big-endian, as the D3 writer frames them. The output is line-based for a
C++ reader: `img_len N` (the record area's length, PP_NVM word 1), one
`map_in K WORD` / `map_out K WORD` per port (the channel-map table words,
`(framed length << 16) | prefix`), `record ID OFFSET PLEN` per framed record
and one `area HEX` line holding the record area itself.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "../../../scripts"))

import nvm_shape  # noqa: E402
from nvm_contract import KLJ2_HDR, KLJ2_TRAILER, REC_HDR, VD_OK, Donor, Ident, Shape  # noqa: E402
from nvm_klj2 import erased_record, frame_record, klj2_assemble, klj2_decode  # noqa: E402


def parse_records(items: list[str]) -> dict[int, bytes]:
    """{record id: payload} from the ID=HEX arguments."""
    out = {}
    for item in items:
        rid_s, _, hex_s = item.partition("=")
        if not hex_s:
            sys.exit(f"FATAL: --record {item!r} is not ID=HEXPAYLOAD")
        out[int(rid_s, 0)] = bytes.fromhex(hex_s)
    return out


def main() -> int:
    """Write the window description; exit 1 if the codec refuses it."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("config", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--record", action="append", default=[])
    args = ap.parse_args()
    # nvm_shape.build runs the builder from the repository root
    args.config = args.config.resolve()
    framed = parse_records(args.record)

    with tempfile.TemporaryDirectory(prefix="nvm-window-") as td:
        names, dc, spi, spo = nvm_shape.build(args.config, Path(td))
        overlay = json.loads((Path(td) / args.config.stem / "aem_overlay.json").read_text())
    shape = Shape(cfg=args.config, names=names, dc=dc, spi=spi, spo=spo)
    donor = Donor(base=nvm_shape.binding_base(), layout=nvm_shape.layout_version())
    ident = Ident(seq=1, entity_id=int(overlay["adp"]["entity_id"], 0),
                  model_id=int(overlay["entity"]["entity_model_id"], 0))
    rows = nvm_shape.inventory(shape, donor.base)
    if any(rid is None for _g, _i, rid, _p, _b in rows):
        sys.exit(f"FATAL: {args.config.name} overflows a record block")

    frames, expect, plen_of = {}, {}, {}
    for group, index, rid, plen, _block in rows:
        expect[(group, index)] = plen
        plen_of[rid] = plen
        frames[rid] = (frame_record(rid, framed[rid], donor.layout)
                       if rid in framed else erased_record(plen))
    for rid, payload in framed.items():
        if plen_of.get(rid) != len(payload):
            sys.exit(f"FATAL: record {rid:#04x} is not a {len(payload)}-byte "
                     f"record of {args.config.name} (shape length "
                     f"{plen_of.get(rid)})")

    blob, offs = klj2_assemble(frames, donor, ident)
    verdict, applied = klj2_decode(blob, donor, ident, expect)
    applied_ids = {rid for group, index, rid, _p, _b in rows if (group, index) in applied}
    if verdict != VD_OK or applied_ids != set(framed):
        print(f"FATAL: the assembled window decodes to verdict {verdict} with "
              f"records {sorted(applied_ids)} applied, not VD_OK with "
              f"{sorted(framed)}", file=sys.stderr)
        return 1

    area = blob[KLJ2_HDR:len(blob) - KLJ2_TRAILER]
    lines = [f"# {args.config.name}: {len(rows)} records, binding base "
             f"{donor.base:#04x}, layout {donor.layout:#04x}",
             f"img_len {len(area)}"]
    for label, group in (("map_in", "MAPS_IN"), ("map_out", "MAPS_OUT")):
        prefix = 0
        for g, index, _rid, plen, _block in rows:
            if g != group:
                continue
            flen = REC_HDR + plen
            lines.append(f"{label} {index} {(flen << 16) | prefix:#010x}")
            prefix += flen
    for rid in sorted(framed):
        lines.append(f"record {rid:#04x} {offs[rid]} {plen_of[rid]}")
    lines.append(f"area {area.hex()}")
    args.out.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
