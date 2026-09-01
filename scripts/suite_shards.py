#!/usr/bin/env python3
"""Select a deterministic, disjoint shard of the Verilator suite inventory.

The unsharded default is the existing lexical sweep. With ``--shard I/N``, a
stable SHA-256 digest assigns each suite to one worker. Unlike position-based
round robin, adding or deleting one suite does not move every later suite to a
different worker. The rule is deterministic, reviewable, and cannot silently
omit a suite when the inventory changes.
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path


SHARD_RE = re.compile(r"^(0|[1-9][0-9]*)/([1-9][0-9]*)$")


def parse_shard(value):
    """Return (zero-based index, worker count), rejecting ambiguous forms."""
    match = SHARD_RE.fullmatch(value)
    if not match:
        raise ValueError("shard must be INDEX/TOTAL using non-negative integers")
    index, total = (int(part) for part in match.groups())
    if index >= total:
        raise ValueError(f"shard index {index} is outside 0..{total - 1}")
    return index, total


def discover_suites(root):
    """Return suite directory names in the serial sweep's lexical order."""
    root = Path(root)
    return sorted(
        path.name for path in root.iterdir()
        if path.is_dir() and (path / "Makefile").is_file()
    )


def select_suites(suites, index, total):
    """Select one stable-hash shard from an already ordered inventory."""
    return [suite for suite in suites if shard_owner(suite, total) == index]


def shard_owner(suite, total):
    """Return the stable zero-based owner of one suite name."""
    digest = hashlib.sha256(suite.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % total


def selftest():
    suites = [f"suite-{number:02d}" for number in range(17)]
    bad = 0

    for total in (1, 2, 4, 7, 23):
        shards = [select_suites(suites, index, total)
                  for index in range(total)]
        flattened = [suite for shard in shards for suite in shard]
        complete = sorted(flattened) == suites
        disjoint = len(flattened) == len(set(flattened))
        deterministic = shards == [select_suites(suites, index, total)
                                   for index in range(total)]
        ok = complete and disjoint and deterministic
        print(f"  {'ok  ' if ok else 'FAIL'} {total:>2} shard(s): "
              f"complete={complete} disjoint={disjoint} "
              f"deterministic={deterministic}")
        bad += 0 if ok else 1

    # Pin runtime landmarks and the two specialized dependency owners. The
    # workflow installs tsn-gen only for tsn_fuzz's worker and Yosys/sv2v only
    # for chmap_capture's worker, so an assignment-rule change must fail here.
    landmarks = {
        "milan_dp": 0,
        "pp_shadow": 1,
        "mmcm_servo": 2,
        "tsn_fuzz": 1,
        "chmap_capture": 3,
    }
    got = {suite: shard_owner(suite, 4) for suite in landmarks}
    ok = got == landmarks
    print(f"  {'ok  ' if ok else 'FAIL'} four-worker runtime landmarks: {got}")
    bad += 0 if ok else 1

    for value in ("", "1", "-1/4", "01/4", "4/4", "5/4", "0/0", "a/4"):
        try:
            parse_shard(value)
            ok = False
        except ValueError:
            ok = True
        print(f"  {'ok  ' if ok else 'FAIL'} reject {value!r}")
        bad += 0 if ok else 1

    print("selftest:", "PASS" if bad == 0 else f"{bad} FAILURE(S)")
    return 1 if bad else 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite-root", type=Path,
                        help="directory containing one subdirectory per suite")
    parser.add_argument("--shard", default="0/1", metavar="INDEX/TOTAL",
                        help="zero-based shard to print (default: 0/1)")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv[1:])

    if args.selftest:
        return selftest()
    if args.suite_root is None:
        parser.error("--suite-root is required unless --selftest is used")

    try:
        index, total = parse_shard(args.shard)
        suites = discover_suites(args.suite_root)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if not suites:
        parser.error(f"no suite Makefiles found under {args.suite_root}")

    for suite in select_suites(suites, index, total):
        print(suite)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
