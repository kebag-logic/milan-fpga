#!/usr/bin/env python3
"""Select a deterministic, disjoint shard of the Verilator suite inventory.

The unsharded default is the existing lexical sweep. With ``--shard I/N``, a
stable SHA-256 digest assigns each suite to one worker. Unlike position-based
round robin, adding or deleting one suite does not move every later suite to a
different worker. The rule is deterministic, reviewable, and cannot silently
omit a suite when the inventory changes.

A suite named in DEDICATED_SUITES runs alone on one of the LAST workers, and
every other suite hashes over the workers before them, so the hashed owners at
N + len(DEDICATED_SUITES) workers are exactly the plain owners at N. With no
more workers than dedicated suites (the serial 0/1 default) nothing is set
aside.
"""

import argparse
import hashlib
import re
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path


SHARD_RE = re.compile(r"^(0|[1-9][0-9]*)/([1-9][0-9]*)$")
SCHEDULED_SUITES = frozenset({"milan_dp_gptp"})
#: #444: milan_dp is the one default suite whose hosted wall clock is most of
#: a worker's. It measured 1726-1773 s passing on the slower hosted runner
#: class, and it shared worker 0 with eleven suites that ran after it, so that
#: worker set the required context's latency. The suites of a worker run one
#: at a time, so a dedicated worker changes no suite's deadline (the driver's
#: suite_timeout table owns that); it takes the other suites off its path.
DEDICATED_SUITES = ("milan_dp",)


def parse_shard(value: str) -> tuple[int, int]:
    """Return (zero-based index, worker count), rejecting ambiguous forms."""
    match = SHARD_RE.fullmatch(value)
    if not match:
        raise ValueError("shard must be INDEX/TOTAL using non-negative integers")
    index, total = (int(part) for part in match.groups())
    if index >= total:
        raise ValueError(f"shard index {index} is outside 0..{total - 1}")
    return index, total


def discover_suites(root: str | Path) -> list[str]:
    """Return suite directory names in the serial sweep's lexical order."""
    root = Path(root)
    return sorted(
        path.name for path in root.iterdir()
        if path.is_dir() and (path / "Makefile").is_file()
    )


def sweep_suites(root: str | Path, *, physical: bool = False) -> list[str]:
    """Select the default or scheduled inventory, shared with the tally reader."""
    return [suite for suite in discover_suites(root)
            if (suite in SCHEDULED_SUITES) == physical]


def select_suites(suites: Sequence[str], index: int, total: int,
                  dedicated: Sequence[str] = DEDICATED_SUITES) -> list[str]:
    """Select one shard from an already ordered inventory."""
    return [suite for suite in suites
            if shard_owner(suite, total, dedicated) == index]


def shard_owner(suite: str, total: int,
                dedicated: Sequence[str] = DEDICATED_SUITES) -> int:
    """Return the stable zero-based owner of one suite name.

    A dedicated suite owns one of the last workers alone once there are more
    workers than dedicated suites; every other suite hashes over the rest.
    """
    hashed = total - len(dedicated) if total > len(dedicated) else total
    if hashed != total and suite in dedicated:
        return hashed + list(dedicated).index(suite)
    digest = hashlib.sha256(suite.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % hashed


def scheduled_partition_selftest() -> bool:
    """Prove physical/default separation while admitting future default suites."""
    # The physical-rate leg has a separate schedule and never consumes a PR
    # shard's deadline. Unknown future suites still join the default sweep.
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        names = ["milan_dp", "milan_dp_gptp", "future_suite"]
        for name in names:
            (root / name).mkdir()
            (root / name / "Makefile").touch()
        default = sweep_suites(root)
        physical = sweep_suites(root, physical=True)
        ok = (SCHEDULED_SUITES == frozenset({"milan_dp_gptp"})
              and not SCHEDULED_SUITES & set(DEDICATED_SUITES)
              and default == ["future_suite", "milan_dp"]
              and physical == ["milan_dp_gptp"]
              and sorted(default + physical) == sorted(names)
              and all("milan_dp_gptp" not in select_suites(default, i, total)
                      for total in (4, 5) for i in range(total)))
        print(f"  {'ok  ' if ok else 'FAIL'} scheduled/default partition: "
              f"default={default} physical={physical}")
        return ok


def dedicated_alone(suites: Sequence[str], total: int,
                    dedicated: Sequence[str]) -> bool:
    """Whether each name in `dedicated` is the only suite of its own worker.
    An empty `dedicated` sets nothing apart and proves nothing, so it is
    False rather than vacuously True."""
    first = total - len(dedicated)
    return bool(dedicated) and all(
        select_suites(suites, first + offset, total, dedicated) == [suite]
        for offset, suite in enumerate(dedicated))


def dedicated_selftest(suites: Sequence[str]) -> int:
    """Prove the dedicated workers hold their suite alone and move no other."""
    bad = 0
    for total in (2, 4, 5, 7, 23):
        alone = dedicated_alone(suites, total, DEDICATED_SUITES)
        # Every other suite keeps the owner it has with no worker set aside.
        stable = all(shard_owner(suite, total) ==
                     shard_owner(suite, total - len(DEDICATED_SUITES), ())
                     for suite in suites if suite not in DEDICATED_SUITES)
        ok = alone and stable
        print(f"  {'ok  ' if ok else 'FAIL'} {total:>2} shard(s): "
              f"dedicated alone={alone} hashed owners unchanged={stable}")
        bad += 0 if ok else 1

    # Negative control: under a rule that sets nothing aside no worker holds
    # a dedicated suite alone, or the arm above proves nothing about the rule.
    plain = [select_suites(suites, index, 5, ()) for index in range(5)]
    caught = bool(DEDICATED_SUITES) and all(
        [suite] not in plain for suite in DEDICATED_SUITES)
    print(f"  {'ok  ' if caught else 'FAIL'} a rule without the dedicated "
          "worker is caught")
    return bad + (0 if caught else 1)


def selftest() -> int:
    """Prove the split stays complete, disjoint and stable; 0 when it does."""
    suites = sorted([f"suite-{number:02d}" for number in range(17)]
                    + list(DEDICATED_SUITES))
    bad = 0

    for total in (1, 2, 4, 5, 7, 23):
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

    bad += dedicated_selftest(suites)

    # Pin runtime landmarks and the three specialized owners. The workflow
    # installs tsn-gen only for tsn_fuzz's worker and Yosys/sv2v only for
    # chmap_capture's worker, and proves the last worker runs milan_dp alone,
    # so an assignment-rule change must fail here.
    landmarks = {
        "milan_dp": 4,
        "pp_shadow": 1,
        "mmcm_servo": 2,
        "tsn_fuzz": 1,
        "chmap_capture": 3,
    }
    got = {suite: shard_owner(suite, 5) for suite in landmarks}
    ok = got == landmarks
    print(f"  {'ok  ' if ok else 'FAIL'} five-worker runtime landmarks: {got}")
    bad += 0 if ok else 1

    bad += 0 if scheduled_partition_selftest() else 1

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


def main(argv: Sequence[str]) -> int:
    """Print one shard's suite names, one per line, for the sweep to run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite-root", type=Path,
                        help="directory containing one subdirectory per suite")
    parser.add_argument("--shard", default="0/1", metavar="INDEX/TOTAL",
                        help="zero-based shard to print (default: 0/1)")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--physical-gptp", action="store_true",
                        help="only the scheduled physical suite; absent from default shards")
    args = parser.parse_args(argv[1:])

    if args.selftest:
        return selftest()
    if args.suite_root is None:
        parser.error("--suite-root is required unless --selftest is used")

    try:
        index, total = parse_shard(args.shard)
        if args.physical_gptp and (index, total) != (0, 1):
            raise ValueError("--physical-gptp uses its own unsharded job (0/1)")
        suites = sweep_suites(args.suite_root, physical=args.physical_gptp)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if not suites:
        parser.error(f"no suite Makefiles found under {args.suite_root}")

    for suite in select_suites(suites, index, total):
        print(suite)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
