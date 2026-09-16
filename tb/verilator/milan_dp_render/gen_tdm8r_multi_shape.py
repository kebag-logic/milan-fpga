#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the MULTI-STREAM render shape for the #447 render-lane leg.

The shipping AX7101 TDM8 image carries ONE listener stream, so two properties
of the render lane cannot be observed on it at all:

  * the epoch's bind-fall mask is STREAM QUALIFIED. A bind fall on a stream
    the lane does not render must leave the lane running; a fall on one it
    does render must close the epoch. With one stream the two cases are the
    same event.
  * an in-range cluster key with NO physical projection. On the shipping shape
    every declared input cluster projects onto a TDM slot, so the legal
    NONPHYSICAL key - the one whose CSR write is suppressed at the crossbar
    and still mirrors into the AECP protocol store - does not exist there, and
    a key one past the block is a different defect class (out of range).

This writes a second end-station config beside the shipping one, differing in
exactly two declarations, and lets the REAL builder derive everything else:

  streams.listeners            gains "Stream In 1", 8 channels, dynamic
  cluster_mapping.policy       cluster-per-stream-channel

The policy swap is what makes the second port's clusters honestly VIRTUAL:
under the wire-truth rule the physical render channels bind in order to the
first clusters of the direction, so port 0 keeps keys 0..7 on render keys
2..9 and port 1's keys 8..15 project nowhere. Under role-pools every input
port would claim the same eight physical channels, which would alias two
ports onto one set of pins - the opposite of what issue #447 asks for. The
config's role pools and fabric block are dropped with the policy, because the
builder refuses a config that declares settings its policy would ignore.

The Makefile runs sw/builder/endstation_builder.py on the written config, so
the elaborated shape header AND the served entity image are produced by the
same two tools a board build uses. Build-time artifact, like ltn_rom.hex:
never tracked, regenerated per make.
"""

import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
#: `sys.path` and `endstation_builder`'s own `load_config(path: str)` are both
#: string interfaces; every path INSIDE this module is a `Path`.
sys.path.insert(0, str(ROOT / "sw" / "builder"))

import endstation_builder as eb  # noqa: E402

#: where the written config lands, and the name the builder derives its output
#: directory from
OUT_DIR = HERE / "gen_tdm8r_multi"
OUT_YAML = OUT_DIR / "endstation_tdm8r_multi.yaml"


def multi_stream_document() -> dict:
    """The shipping TDM8 document with a second listener and the legacy
    cluster policy, asserted to have actually changed both."""
    with (ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml").open() as fh:
        doc = yaml.safe_load(fh)
    listeners = doc["streams"]["listeners"]
    if len(listeners) != 1:
        raise SystemExit("the shipping TDM8 config no longer declares exactly "
                         "one listener; this generator's premise is gone")
    listeners.append({"name": "Stream In 1", "channels": 8,
                      "map_mode": "dynamic"})
    mapping = doc["audio_interface"]["cluster_mapping"]
    mapping["policy"] = "cluster-per-stream-channel"
    #: both are role-pools-only settings; the builder refuses a config that
    #: carries a block its policy would silently ignore
    mapping.pop("pools", None)
    mapping.pop("fabric", None)
    return doc


def main() -> None:
    """Write the multi-stream config and state the shape it produces.

    The two properties the leg stands on are asserted HERE, before anything
    is elaborated: a shape where port 1 turned out physical, or where the
    lane's key window stopped being port 0's, would let the leg run green and
    prove neither of the things it exists to prove.
    """
    doc = multi_stream_document()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_YAML.open("w") as fh:
        yaml.safe_dump(doc, fh, sort_keys=False)

    cfg = eb.load_config(str(OUT_YAML))
    ports = cfg["ports_in"]
    if len(ports) != 2:
        raise SystemExit(f"expected 2 STREAM_PORT_INPUTs, got {len(ports)}")
    roles = [tuple(sorted(g["role"] for g in p["pool"])) for p in ports]
    if roles != [("physical",), ("virtual",)]:
        raise SystemExit(
            f"port roles {roles} are not (physical, virtual): the nonphysical "
            "in-range key this shape exists to supply would not exist")
    base1 = ports[1]["base_cluster"]
    print(f"multi-stream render shape: ports_in={len(ports)} "
          f"port0 keys {ports[0]['base_cluster']}..{base1 - 1} physical, "
          f"port1 keys {base1}..{base1 + ports[1]['clusters'] - 1} "
          f"NONPHYSICAL; config {OUT_YAML.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
