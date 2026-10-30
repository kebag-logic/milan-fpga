#!/usr/bin/env python3
"""Reviewer probe: load the shipping configuration with one key changed and
print whether the builder accepts it, using the generator's own loader.

Usage: python3 probe_claims.py <repo-root>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "builder"))
import gen_key_reference as g  # noqa: E402

CASES = [
    # (base, key, value, what the page claims)
    ("endstation_ax7101_1x1_tdm8", "board.constraints.num_queues", 6, "page meaning: must equal the RTL's queue count"),
    ("endstation_ax7101_1x1_tdm8", "board.constraints.num_queues", 8, "page: integer above srp.class_queue"),
    ("endstation_ax7101_1x1_tdm8", "clocking.audio_unit_rates_hz", [48000, 44100], "page: base rates"),
    ("endstation_ax7101_1x1_tdm8", "clocking.audio_unit_rates_hz", [48000, 96000, 192000], "page: base rates"),
    ("endstation_ax7101_1x1_tdm8", "board.constraints.uart_baudrate", -5, "page: an integer"),
    ("endstation_ax7101_1x1_tdm8", "board.constraints.uart_baudrate", "abc", "page: ValueError"),
    ("endstation_ax7101_1x1_tdm8", "entity.vendor_name", "v" * 200, "page: no length check"),
    ("endstation_ax7101_1x1_tdm8", "entity.group_name", "g" * 63, "page: at most 63"),
    ("endstation_ax7101_1x1_tdm8", "entity.group_name", "g" * 64, "page: at most 63"),
    ("endstation_ax7101_1x1_tdm8", "entity.locale", "l" * 64, "page: at most 64"),
    ("endstation_ax7101_1x1_tdm8", "entity.locale", "l" * 65, "page: at most 64"),
    ("endstation_ax7101_1x1_tdm8", "srp.class_queue", 7, "page: below num_queues, fits 3 bits"),
    ("endstation_ax7101_1x1_tdm8", "srp.bandwidth_limit_pct", 0, "page: integer up to 75"),
    ("endstation_ax7101_1x1_tdm8", "platform.pp_mem_phys", 0x4FE00800, "page: page-aligned"),
    ("endstation_ax7101_1x1_tdm8", "gptp.priority1", 0, "page: 0 to 255"),
    ("endstation_ax7101_1x1_tdm8", "streams.listeners[].channels", 32, "page: 1 to 32"),
    ("endstation_ax7101_1x1_tdm8", "streams.listeners[].channels", 33, "page: 1 to 32"),
    ("endstation_ax7101_1x1_tdm8", "board.constraints.floorplan", "no", "page: any value read as boolean"),
    ("endstation_ax7101_1x1_tdm8", "audio_interface.cluster_mapping.fabric.loopback_lane", "no", "page: any value read as boolean"),
    ("endstation_ax7101_1x1_tdm8", "board.features.maap", False, "page: refused"),
    ("endstation_ax7101_1x1_tdm8", "clocking.default_source", "crf", "page: member of media_clock_sources"),
    ("endstation_ax7101_1x1_tdm8", "entity.firmware_rev", True, "page: non-negative integer"),
    ("endstation_ax7101_1x1_tdm8", "srp.stream_dmac_base", "maap", "page: maap or multicast"),
    ("endstation_ax7101_1x1_tdm8", "board.constraints.sys_clk_hz", 50000000, "page: at least milan_clk_hz"),
    ("endstation_ax7101_1x1_tdm8", "board.constraints.sys_clk_hz", 49999999, "page: at least milan_clk_hz"),
    ("endstation_ax7101_1x1_tdm8", "soc.timing_opt", "no", "page: any value"),
]


def main() -> int:
    with g.at_root():
        cache = {}
        for base, key, value, claim in CASES:
            if base not in cache:
                cache[base] = g.base_document(base)
            rel, doc = cache[base]
            got = g.load(rel, g.with_key(doc, key, value))
            shown = value if not (isinstance(value, str) and len(value) > 20) else f"<{len(value)} chars>"
            verdict = "ACCEPTED" if got.ok else f"REFUSED {got.kind} in {got.function}: {got.message[:110]}"
            print(f"{key} = {shown!r} [{claim}] -> {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
