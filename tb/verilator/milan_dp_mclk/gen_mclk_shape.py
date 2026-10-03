#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the TWO-STREAM shape the #629 root media-clock leg follows.

The shipping AX7101 TDM8 image carries one AAF listener, so the switch rows
of docs/design/MEDIA_CLOCK_FOLLOWING.md's test plan - AAF input 0 to input 1,
the two talkers at opposite `mr` levels - cannot be driven on it. This writes
the shipping config with a second listener, through the same document edit
tb/verilator/milan_dp_render's two-stream leg makes (its
`multi_stream_document()`, imported rather than restated), and a second
talker. The talker keeps the shape inside the datapath's supported matrix:
N_STREAMS counts both directions, and the CRF Media Clock Output's context is
the one after the AAF talkers only when the entity declares N_STREAMS of them
(milan_datapath's ACMP_SRC_C rule), which is where the leg reads the CRF
output's MEDIA_RESET counter. The Makefile runs the real builder on it. The builder's class order then lists INTERNAL 0,
CRF 1, AAF input 0 at 2 and AAF input 1 at 3 (#629 D1), and `--check-header`
asserts that on the generated shape header before anything is elaborated: a
shape whose sources moved would let the leg poke the wrong index and still
run.

Build-time artifact, like ltn_rom.hex: never tracked, regenerated per make.
"""

import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
#: `sys.path` and `endstation_builder`'s own `load_config(path: str)` are both
#: string interfaces; every path INSIDE this module is a `Path`.
sys.path.insert(0, str(ROOT / "sw" / "builder"))
sys.path.insert(0, str(ROOT / "tb" / "verilator" / "milan_dp_render"))

import endstation_builder as eb  # noqa: E402
import gen_tdm8r_multi_shape as multi  # noqa: E402

#: where the written config lands, and the name the builder derives its output
#: directory from
OUT_DIR = HERE / "gen_mclk"
OUT_YAML = OUT_DIR / "endstation_mclk.yaml"
#: the class order the leg's clock-source pokes depend on (#629 D1): the
#: per-index kind and STREAM_INPUT tables of the generated shape header
WANT_KIND = "'{2'd0, 2'd1, 2'd2, 2'd2}"
WANT_SI = "'{16'hFFFF, 16'd2, 16'd0, 16'd1}"


def write_config() -> None:
    """Write the two-stream config and assert it declares two of each."""
    doc = multi.multi_stream_document()
    talkers = doc["streams"]["talkers"]
    if len(talkers) != 1:
        raise SystemExit("the shipping TDM8 config no longer declares exactly "
                         "one talker; this generator's premise is gone")
    talkers.append({"name": "Stream Out 1", "channels": 8,
                    "map_mode": "dynamic"})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_YAML.open("w") as fh:
        yaml.safe_dump(doc, fh, sort_keys=False)
    cfg = eb.load_config(str(OUT_YAML))
    if len(cfg["listeners"]) != 2 or len(cfg["talkers"]) != 2:
        raise SystemExit(f"expected 2 listeners and 2 talkers, got "
                         f"{len(cfg['listeners'])} and {len(cfg['talkers'])}")
    print(f"media-clock root shape: 2 AAF listeners, 2 AAF talkers; "
          f"config {OUT_YAML.relative_to(ROOT)}")


def table_of(text: str, name: str) -> str:
    """The initializer of the generated localparam `name`."""
    for line in text.splitlines():
        if f" {name} " in line and "=" in line:
            return line.split("=", 1)[1].strip().rstrip(";")
    raise SystemExit(f"the shape header declares no {name}")


def check_header(path: Path) -> None:
    """Assert the generated clock-source tables are the order the leg pokes."""
    text = path.read_text()
    kind = table_of(text, "AEM_CLKSRC_KIND_C")
    si = table_of(text, "AEM_CLKSRC_SI_C")
    if kind != WANT_KIND or si != WANT_SI:
        raise SystemExit(f"clock-source tables {kind} / {si} are not "
                         f"{WANT_KIND} / {WANT_SI}: the leg's index pokes "
                         "would name other sources")
    print(f"media-clock root shape: clock sources INTERNAL 0, CRF 1, "
          f"AAF 0 at 2, AAF 1 at 3 ({path.name})")


def main() -> None:
    """Write the config, or with `--check-header PATH` grade its header."""
    if len(sys.argv) == 3 and sys.argv[1] == "--check-header":
        check_header(Path(sys.argv[2]))
    else:
        write_config()


if __name__ == "__main__":
    main()
