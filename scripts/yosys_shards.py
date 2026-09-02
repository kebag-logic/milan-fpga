#!/usr/bin/env python3
"""Select deterministic weighted shards from the Yosys top inventory.

The selector uses longest-processing-time scheduling with measured cache-hit
weights. The heaviest tops therefore get isolated workers while the original
inventory order is preserved inside each shard. The no-shard default remains
the complete serial inventory.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Sequence

SHARD_RE = re.compile(r"^(0|[1-9][0-9]*)/([1-9][0-9]*)$")
NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# Approximate cache-hit seconds from run 32406467657, which ran the floating
# apt Yosys of its day (0.33-5build2 on ubuntu-latest). CI has pinned Yosys
# v0.66 since #287 and per-top wall time moves non-uniformly between the two
# (37.9 s -> 9.1 s on avtp_stream_parser, 40.8 s -> 42.3 s on KL_gptp_shadow),
# so these hints describe the retired tool until #286's measurement harness
# re-takes them on the pinned one under its own comparability rules.
# Unlisted tops are small and receive one unit. These values are scheduling
# hints, never pass criteria.
WEIGHTS: dict[str, int] = {
    "milan_datapath": 1550,
    "KL_pp_shadow": 465,
    "KL_gptp_shadow": 43,
    "avtp_stream_parser": 39,
    "milan_csr": 34,
    "axis_fifo": 27,
    "KL_i2s_playback": 22,
    "KL_chan_map_capture": 17,
    "KL_tone_gen": 12,
    "KL_aaf_rx_depacketizer": 10,
    "KL_aaf_packetizer": 10,
    "credit_based_shaper": 9,
    "KL_avtp_rx_monitor_ctx": 8,
    "KL_crf_rx": 6,
    "KL_crf_tx": 3,
    "KL_mmcm_drp_servo": 4,
    "KL_chan_map_render": 4,
    "KL_aes3_rx": 3,
    "KL_maap": 3,
    "queues_wrap": 2,
    "classifier_wrap": 2,
    "rx_mac_filter": 2,
}
DEFAULT_WEIGHT = 1


def parse_shard(value: str) -> tuple[int, int]:
    """Return a zero-based index and worker count."""
    match = SHARD_RE.fullmatch(value)
    if not match:
        raise ValueError("shard must be INDEX/TOTAL using non-negative integers")
    index, total = (int(part) for part in match.groups())
    if index >= total:
        raise ValueError(f"shard index {index} is outside 0..{total - 1}")
    return index, total


def validate_names(names: Iterable[str]) -> list[str]:
    """Return a validated ordered inventory."""
    ordered = list(names)
    if not ordered:
        raise ValueError("top inventory is empty")
    invalid = [name for name in ordered if not NAME_RE.fullmatch(name)]
    if invalid:
        raise ValueError(f"invalid top name(s): {', '.join(invalid)}")
    duplicates = sorted({name for name in ordered if ordered.count(name) > 1})
    if duplicates:
        raise ValueError(f"duplicate top name(s): {', '.join(duplicates)}")
    return ordered


def assignments(names: Sequence[str], total: int) -> tuple[dict[str, int], list[int]]:
    """Assign each top with deterministic longest-processing-time scheduling."""
    ordered = validate_names(names)
    loads = [0] * total
    owners: dict[str, int] = {}
    for name in sorted(ordered, key=lambda item: (-WEIGHTS.get(item, DEFAULT_WEIGHT), item)):
        owner = min(range(total), key=lambda index: (loads[index], index))
        owners[name] = owner
        loads[owner] += WEIGHTS.get(name, DEFAULT_WEIGHT)
    return owners, loads


def select_names(names: Sequence[str], index: int, total: int) -> list[str]:
    """Return one shard while preserving the source inventory order."""
    owners, _ = assignments(names, total)
    return [name for name in names if owners[name] == index]


def selftest() -> int:
    names = [
        "milan_datapath",
        "KL_pp_shadow",
        "KL_gptp_shadow",
        "avtp_stream_parser",
        "milan_csr",
        "axis_fifo",
        *(f"small_top_{number:02d}" for number in range(40)),
    ]
    failures = 0

    for total in (1, 2, 4, 7):
        shards = [select_names(names, index, total) for index in range(total)]
        flattened = [name for shard in shards for name in shard]
        complete = sorted(flattened) == sorted(names)
        disjoint = len(flattened) == len(set(flattened))
        deterministic = shards == [select_names(names, index, total)
                                   for index in range(total)]
        ok = complete and disjoint and deterministic
        print(
            f"  {'ok  ' if ok else 'FAIL'} {total:>2} shard(s): "
            f"complete={complete} disjoint={disjoint} deterministic={deterministic}"
        )
        failures += 0 if ok else 1

    owners, loads = assignments(names, 4)
    heavy_ok = owners["milan_datapath"] == 0 and owners["KL_pp_shadow"] == 1
    print(
        f"  {'ok  ' if heavy_ok else 'FAIL'} four-worker heavy owners: "
        f"milan_datapath={owners['milan_datapath']} "
        f"KL_pp_shadow={owners['KL_pp_shadow']} loads={loads}"
    )
    failures += 0 if heavy_ok else 1

    for value in ("", "1", "-1/4", "01/4", "4/4", "5/4", "0/0", "a/4"):
        try:
            parse_shard(value)
            ok = False
        except ValueError:
            ok = True
        print(f"  {'ok  ' if ok else 'FAIL'} reject shard {value!r}")
        failures += 0 if ok else 1

    for inventory in ([], ["good", "good"], ["bad-name"]):
        try:
            validate_names(inventory)
            ok = False
        except ValueError:
            ok = True
        print(f"  {'ok  ' if ok else 'FAIL'} reject inventory {inventory!r}")
        failures += 0 if ok else 1

    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return 1 if failures else 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shard", default="0/1", metavar="INDEX/TOTAL")
    parser.add_argument("--show-loads", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument(
        "names",
        nargs="*",
        help="top names; when omitted, read one name per stdin line",
    )
    args = parser.parse_args(argv[1:])

    if args.selftest:
        return selftest()

    raw_names = args.names or [line.strip() for line in sys.stdin if line.strip()]
    try:
        index, total = parse_shard(args.shard)
        names = validate_names(raw_names)
        owners, loads = assignments(names, total)
    except ValueError as exc:
        parser.error(str(exc))

    if args.show_loads:
        print(
            "estimated shard loads: "
            + ", ".join(f"{worker}={load}" for worker, load in enumerate(loads)),
            file=sys.stderr,
        )

    for name in names:
        if owners[name] == index:
            print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
