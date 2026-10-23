#!/usr/bin/env python3
r"""Balance the physical serial inventory and the case-partitioned CI inventory.

The serial sweep still discovers every Makefile and excludes only the scheduled
physical gPTP suite. CI expands six registered parents into driver-owned case
partitions. Only leg counts and measured duration estimates are registered here;
the case names come from each driver, and executed receipts prove their union.

Longest-first scheduling balances sixteen standard workers. The tsn-gen owner
stays at worker 1 and the netlist owner at worker 3. One continuous media-clock
history runs alone on the final worker under issue 737s explicit timing exception.
Every other worker must project at most 1620 seconds including setup. The older
60-percent timeout bound remains an additional gate, including for the exception.

New suites must enter both the discovered inventory and duration table. Until a
hosted window is measured, register the exact run_all_suites.sh timeout as a
provisional estimate; the selftest checks that value against the driver. Never
hide a new suite by omitting it from selection. A changed count or timeout is read
from the generated workflow, and omission, ownership, overflow and deterministic
selection controls must still pass.

    python3 scripts/suite_shards.py --suite-root tb/verilator --ci-pieces --shard 0/16
    python3 scripts/suite_shards.py --measure worker.log
    python3 scripts/suite_shards.py --selftest
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Collection, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple


SHARD_RE = re.compile(r"^(0|[1-9][0-9]*)/([1-9][0-9]*)$")
SCHEDULED_SUITES = frozenset({"milan_dp_gptp"})
#: #444: milan_dp is the one default suite whose hosted wall clock is most of
#: a worker's. It measured 1726-1773 s passing on the slower hosted runner
#: class, and it shared worker 0 with eleven suites that ran after it, so that
#: worker set the required context's latency. The suites of a worker run one
#: at a time, so a dedicated worker changes no suite's deadline (the driver's
#: suite_timeout table owns that); it takes the other suites off its path.
DEDICATED_SUITES = ("milan_dp_mclk__0",)

#: The workflow installs tsn-gen only on worker 1 and Yosys/sv2v only on
#: worker 3, keyed by the worker's index, and its ownership step proves these
#: owners at run time. They hold at the workflow's worker count.
PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}

#: #727: no worker may be predicted above this share of its job timeout.
HEADROOM_PERCENT = 60

#: The tree this file belongs to, and the three things its head arms read.
HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "rtl.yml"
SUITE_ROOT = ROOT / "tb" / "verilator"
DRIVER = ROOT / "scripts" / "run_all_suites.sh"
VERILATOR_JOB = "verilator-shards"

#: #727: hosted seconds per default suite, rounded up, by the rule in the
#: module docstring. Dev run 38217650945 at c6bd08c6, all five Verilator
#: workers, except `maap`: #696 lengthens it, measured on its worker 1/5 in
#: run 38208503834 at 26e2748f (dev's own window was 185 s), and `gptp_tables`
#: (#713): the larger of its hosted windows, worker 0/6 of dev run 38601263345
#: at f6260253, where that worker passed all eight of its suites (its
#: pull-request run 38538854504 at 7fb3664b measured 474 s).
SUITE_SECONDS = {
    "aaf": 73,
    "aaf_audio_loop": 6,
    "aaf_clock_meter": 1055,
    "aaf_latency_tap_bank": 16,
    "aaf_latency_taps": 6,
    "adp_tx": 12,
    "aes3": 6,
    "avtp_parser": 27,
    "avtp_rxmon": 73,
    "avtp_stream": 11,
    "capture_coherence": 1737,
    "cbs": 6,
    "cdc": 6,
    "chmap_capture": 168,
    "chmap_render": 6,
    "classifier": 6,
    "clkvalid": 16,
    "cls": 6,
    "controller_rate": 9,
    "crf_rx": 832,
    "crf_tx": 6,
    "csr": 306,
    "datapath": 6,
    "eth_tx_reset": 6,
    "follow_ring": 1158,
    "fw_service_budget": 2,
    "gptp_plane": 784,
    "gptp_shadow": 393,
    "gptp_tables": 568,
    "gptp_txts": 72,
    "i2spb": 6,
    "ifg": 6,
    "lat_history_ring": 6,
    "link_guard": 7,
    "maap": 1375,
    "mac_rmon": 11,
    "mbx": 82,
    "media_grid_align": 255,
    "media_nco": 17,
    "media_phase": 900,
    "milan_dp": 2797,
    "milan_dp_gm_steps": 926,
    "milan_dp_mclk": 2038,
    "milan_dp_render": 1264,
    "mmcm_servo": 1145,
    "mmcm_servo_autorepair": 6,
    "nvm_backend": 34,
    "nvm_cosim": 775,
    "pair_fill": 6,
    "pcmlpf": 6,
    "pp_shadow": 1251,
    "ptp": 26,
    "ptp_sync": 11,
    "ptp_ts": 127,
    "queues": 6,
    "render_queue": 93,
    "rx_filter": 18,
    "shaper_core": 6,
    "tcam": 27,
    "tcam_csr": 6,
    "tdm": 6,
    "tdm_render": 6,
    "tkdiag": 28,
    "tsn_fuzz": 60,
}

#: Suites whose SUITE_SECONDS figure is provisional: the wall clock the
#: driver's suite_timeout gives a new suite, until the change's own hosted run
#: measures it (step 3 of the module docstring's new-suite steps).
PROVISIONAL_SUITES: frozenset[str] = frozenset({"media_phase"})

#: Seconds of each worker's job outside its suite windows in the same dev run:
#: checkout, the Verilator cache, tsn-gen on worker 1, Yosys and sv2v on worker
#: 3, the ownership step and the sweep's preflight self-tests, then the tally.
WORKER_OVERHEAD_SECONDS = (122,) * 16

# Physical inventory stays available to the serial gate and log ownership.
SERIAL_SUITE_SECONDS = SUITE_SECONDS.copy()
# Projected seconds: hosted parent windows at 7032bca5 apportioned by local
# leg wall time. Media-clock legs use the full-run speed ratio instead, since
# its continuous histories overlap in the full campaign. See CI_WORKFLOWS.md.
PIECE_SECONDS = {
    "milan_dp": (378, 1483, 1156, 231),
    "milan_dp_mclk": (1910, 1450, 1399, 836),
    "capture_coherence": (632, 508, 331, 246),
    "maap": (329, 361, 302, 311),
    "milan_dp_render": (354, 30, 652),
    "pp_shadow": (217, 232, 234, 347),
}


def concrete_job_limits(workflow: str) -> tuple[int, ...] | None:
    """Read each materialized worker own limit, refusing holes and duplicate IDs."""
    blocks = re.split(r"(?m)^  ([A-Za-z0-9_-]+):\s*$", workflow)
    workers = {}
    for index in range(1, len(blocks), 2):
        match = re.fullmatch(re.escape("verilator-shards") + r"-(0|[1-9][0-9]*)", blocks[index])
        if match is None:
            continue
        number = int(match[1])
        limits = re.findall(r"(?m)^    timeout-minutes: ([0-9]+)\s*$", blocks[index + 1])
        if len(limits) != 1 or number in workers:
            raise ValueError("materialized worker has a missing or duplicate timeout or ID")
        workers[number] = int(limits[0])
    if not workers:
        return None
    if set(workers) != set(range(len(workers))):
        raise ValueError("materialized worker inventory or timeouts differ")
    return tuple(workers[index] for index in range(len(workers)))



def expand_suites(suites: list[str]) -> list[str]:
    """Replace each registered parent by every leg, retaining all other suites."""
    pieces = [f"{suite}__{leg}" for suite in suites if suite in PIECE_SECONDS
              for leg in range(len(PIECE_SECONDS[suite]))]
    # Receipts bind clean source before legacy suites can refresh dated reports.
    return pieces + [suite for suite in suites if suite not in PIECE_SECONDS]

for _parent, _durations in PIECE_SECONDS.items():
    del SUITE_SECONDS[_parent]
    SUITE_SECONDS.update({f"{_parent}__{leg}": seconds
                          for leg, seconds in enumerate(_durations)})


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


def table_problems(suites: Sequence[str],
                   seconds: Mapping[str, int]) -> list[str]:
    """Where the duration table and the inventory disagree; empty when they
    name the same suites and every duration is a positive whole second."""
    inventory = set(suites)
    problems = [f"{suite}: inventory suite with no recorded duration in "
                "SUITE_SECONDS (a new suite follows the module docstring's "
                "new-suite steps: record suite_timeout's figure for it as "
                "provisional, add a worker if one is then predicted over "
                f"{HEADROOM_PERCENT}% of timeout-minutes, and replace the "
                "figure from the change's own hosted run)"
                for suite in suites if suite not in seconds]
    problems += [f"{suite}: SUITE_SECONDS names a suite that is not in the "
                 "inventory" for suite in sorted(set(seconds) - inventory)]
    problems += [f"{suite}: recorded duration {seconds[suite]!r} is not a "
                 "positive whole number of seconds" for suite in suites
                 if suite in seconds and not (
                     isinstance(seconds[suite], int) and seconds[suite] > 0)]
    return problems


def balance(suites: Sequence[str], total: int,
            seconds: Mapping[str, int] = SUITE_SECONDS,
            overhead: Sequence[int] = WORKER_OVERHEAD_SECONDS,
            dedicated: Sequence[str] = DEDICATED_SUITES,
            ) -> tuple[dict[str, int], list[int]]:
    """Return each suite's zero-based worker and each worker's predicted
    seconds, refusing a table that disagrees with the inventory.

    Dedicated suites take the last workers alone once there are more workers
    than dedicated suites. At the workflow's worker count, the length of
    `overhead`, each worker starts from its overhead and PINNED_SUITES keep
    their workers. The rest go longest first to the least-loaded worker.
    """
    problems = table_problems(suites, seconds)
    if problems:
        raise ValueError("; ".join(problems))
    balanced = total - len(dedicated) if total > len(dedicated) else total
    layout = total == len(overhead)
    load = list(overhead) if layout else [0] * total
    fixed = {}
    if balanced != total:
        fixed.update((suite, balanced + offset)
                     for offset, suite in enumerate(dedicated))
    if layout:
        fixed.update(PINNED_SUITES)
    owners = {}
    for suite in suites:
        if suite in fixed:
            owners[suite] = fixed[suite]
            load[fixed[suite]] += seconds[suite]
    for suite in sorted((suite for suite in suites if suite not in fixed),
                        key=lambda suite: (-seconds[suite], suite)):
        worker = min(range(balanced), key=lambda worker: (load[worker], worker))
        owners[suite] = worker
        load[worker] += seconds[suite]
    return owners, load


def select_suites(suites: Sequence[str], index: int, total: int,
                  seconds: Mapping[str, int] = SUITE_SECONDS,
                  dedicated: Sequence[str] = DEDICATED_SUITES) -> list[str]:
    """Select one shard from an already ordered inventory. One worker runs
    everything in order and needs no table; a sharded split needs one."""
    if total == 1:
        return list(suites)
    owners, _ = balance(suites, total, seconds, dedicated=dedicated)
    return [suite for suite in suites if owners[suite] == index]


def verilator_worker_limits(workflow: str) -> tuple[int, ...]:
    """Read each worker own timeout without borrowing another matrix leg limit."""
    concrete = concrete_job_limits(workflow)
    if concrete is not None:
        return concrete
    # Generated YAML uses block arrays and a literal two-budget expression.
    workflow = re.sub(r"(?m)^        total:\n          - ([0-9]+) *$", r"        total: [\1]", workflow)
    lines = workflow.splitlines()
    starts = [n for n, line in enumerate(lines)
              if line.rstrip() == f"  {VERILATOR_JOB}:"]
    if len(starts) != 1:
        raise ValueError(f"rtl.yml has {len(starts)} `{VERILATOR_JOB}:` jobs, "
                         "not one")
    block = []
    for line in lines[starts[0] + 1:]:
        if line.strip() and not line.startswith("   ") \
                and not line.lstrip().startswith("#"):
            break
        block.append(line)
    found = {}
    for key, pattern in (("timeout-minutes", r"    timeout-minutes: *(.*?) *"),
                         ("matrix total", r"        total: *\[ *([0-9]+) *\] *")):
        values = [match.group(1) for line in block
                  if (match := re.fullmatch(pattern, line))]
        if len(values) != 1:
            raise ValueError(f"rtl.yml job `{VERILATOR_JOB}` has {len(values)} "
                             f"{key} values, not one")
        found[key] = values[0]
    workers = int(found["matrix total"])
    timeout = found["timeout-minutes"]
    if timeout.isdigit() and int(timeout) > 0 and workers > 0:
        return (int(timeout),) * workers
    expression = re.fullmatch(r"\$\{\{ matrix.shard == ([0-9]+) && ([0-9]+) \|\| ([0-9]+) \}\}", timeout)
    if expression is None:
        raise ValueError("unsupported worker timeout expression")
    special, extended, regular = map(int, expression.groups())
    if special >= workers or min(extended, regular) < 1:
        raise ValueError("worker timeout expression has an invalid index or limit")
    return tuple(extended if index == special else regular for index in range(workers))


def verilator_job_limits(workflow: str) -> tuple[int, int]:
    """Fixture range only; production enforcement reads each worker limit separately."""
    limits = verilator_worker_limits(workflow)
    return max(limits), len(limits)




SUITE_TIMEOUT_ARM_RE = re.compile(
    r" +([A-Za-z0-9_]+|\*)\) +printf '%s\\n' \"\$\{SUITE_TIMEOUT:-([0-9]+)\}\" ;;")


def driver_timeouts(driver: str) -> tuple[dict[str, int], int]:
    """Return the wall clock run_all_suites.sh's suite_timeout gives each
    suite it names, and its `*` default, from the script's text. Every line
    of the function's `case` is read, and an arm of any other shape, a name
    given twice, or a `*` arm that is not the one last arm is refused."""
    lines = driver.splitlines()
    starts = [n for n, line in enumerate(lines) if line == "suite_timeout() {"]
    if len(starts) != 1:
        raise ValueError(f"run_all_suites.sh has {len(starts)} suite_timeout "
                         "functions, not one")
    body = lines[starts[0] + 1:]
    body = body[:body.index("}")] if "}" in body else []
    if body[:1] != ['  case "$1" in'] or body[-1:] != ["  esac"]:
        raise ValueError("run_all_suites.sh's suite_timeout is not one "
                         "`case \"$1\"` closed by its own brace")
    arms = []
    for line in body[1:-1]:
        arm = SUITE_TIMEOUT_ARM_RE.fullmatch(line)
        if not arm:
            raise ValueError(f"run_all_suites.sh's suite_timeout arm "
                             f"{line.strip()!r} is not a figure for one name")
        arms.append((arm.group(1), int(arm.group(2))))
    names = [name for name, _ in arms]
    if len(set(names)) != len(names) or names[-1:] != ["*"]:
        raise ValueError("run_all_suites.sh's suite_timeout names a suite twice "
                         "or has no `*` arm last")
    return dict(arms[:-1]), arms[-1][1]


def provisional_problems(driver: str,
                         seconds: Mapping[str, int] = SUITE_SECONDS,
                         provisional: Collection[str] = PROVISIONAL_SUITES,
                         ) -> list[str]:
    """Where a provisional figure is not the wall clock the driver's
    suite_timeout gives its suite: its own arm, otherwise the `*` default."""
    named, default = driver_timeouts(driver)
    problems = []
    for suite in sorted(provisional):
        expected = named.get(suite, default)
        if suite not in seconds:
            problems.append(f"{suite}: PROVISIONAL_SUITES names a suite with no "
                            "figure in SUITE_SECONDS")
        elif seconds[suite] != expected:
            problems.append(f"{suite}: provisional figure {seconds[suite]!r} s is "
                            f"not the {expected} s that run_all_suites.sh's "
                            "suite_timeout gives it")
    return problems


def bound_seconds(timeout_minutes: int) -> int:
    """The most a worker may be predicted to take under this job timeout."""
    return timeout_minutes * 60 * HEADROOM_PERCENT // 100


def headroom_problems(suites: Sequence[str], workflow: str,
                      seconds: Mapping[str, int] = SUITE_SECONDS,
                      overhead: Sequence[int] = WORKER_OVERHEAD_SECONDS,
                      ) -> tuple[list[str], list[int], list[int]]:
    """The gate: (problems, predicted seconds per worker, bounds) for this
    inventory against the table and rtl.yml's Verilator job."""
    limits = verilator_worker_limits(workflow)
    workers = len(limits)
    bounds = [bound_seconds(limit) for limit in limits]
    problems = table_problems(suites, seconds)
    if len(overhead) != workers:
        problems.append(f"WORKER_OVERHEAD_SECONDS describes {len(overhead)} "
                        f"workers; rtl.yml runs {workers}")
    if problems:
        return problems, [], bounds
    _, load = balance(suites, workers, seconds, overhead)
    problems += [f"worker {worker}/{workers} is predicted at {value} s, over "
                 f"{bounds[worker]} s ({HEADROOM_PERCENT}% of timeout-minutes {limits[worker]})"
                 for worker, value in enumerate(load) if value > bounds[worker]]
    # The continuous media-clock history has an explicit owner exception.
    # Every other worker has a stricter, absolute 27-minute scheduling budget.
    problems += [f"worker {worker}/{workers} exceeds the 1620 s CI budget: {value} s"
                 for worker, value in enumerate(load[:-len(DEDICATED_SUITES)]) if value > 1620]
    return problems, load, bounds


class LogTimes(NamedTuple):
    """One hosted worker log, measured."""
    index: int
    total: int
    seconds: dict[str, int]
    overhead: int | None


LOG_LINE_RE = re.compile(r"^[^\t]*\t[^\t]*\t\ufeff?"
                         r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d+))?Z (.*)$")
SHARD_LINE_RE = re.compile(r"shard: (\d+)/(\d+) +selected suites: (\d+)")
RESULT_LINE_RE = re.compile(r"(PASS|FAIL|TIMEOUT) +(\S+).*")
TICKS_PER_SECOND = 10_000_000


def log_ticks(stamp: str, fraction: str | None) -> int:
    """A log timestamp in exact 100 ns ticks, so no window rounds twice."""
    whole = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S")
    seconds = int(whole.replace(tzinfo=timezone.utc).timestamp())
    return seconds * TICKS_PER_SECOND + int((fraction or "").ljust(7, "0")[:7])


def measure_log(text: str) -> LogTimes:
    """Measure one `gh run view --log` worker log by the module's rule. A
    suite that did not pass has no completion time, so it is refused; a log
    cut off before its summary measures its suites but has no overhead."""
    first = last = shard = summary = None
    results = []
    for line in text.splitlines():
        match = LOG_LINE_RE.match(line)
        if not match:
            continue
        ticks = log_ticks(match.group(1), match.group(2))
        message = match.group(3)
        first = ticks if first is None else first
        last = ticks
        if shard is None:
            found = SHARD_LINE_RE.fullmatch(message)
            if found:
                shard = (ticks, *(int(part) for part in found.groups()))
            continue
        if summary is not None:
            continue
        result = RESULT_LINE_RE.fullmatch(message)
        if result:
            if result.group(1) != "PASS":
                raise ValueError(f"{result.group(2)} reports {result.group(1)}, "
                                 "so its window is not a completion time")
            results.append((ticks, result.group(2)))
        elif message.startswith("suites: "):
            summary = ticks
    if shard is None:
        raise ValueError("no `shard: I/N   selected suites: K` line")
    start, index, total, selected = shard
    windows, previous = {}, start
    for ticks, suite in results:
        windows[suite] = -(-(ticks - previous) // TICKS_PER_SECOND)
        previous = ticks
    overhead = None
    if summary is not None:
        if len(results) != selected:
            raise ValueError(f"{len(results)} result lines for {selected} "
                             "selected suites")
        outside = (start - first) + (last - previous)
        overhead = -(-outside // TICKS_PER_SECOND)
    return LogTimes(index, total, windows, overhead)


def measure_main(paths: Sequence[Path]) -> int:
    """Print SUITE_SECONDS and WORKER_OVERHEAD_SECONDS from worker logs; a
    suite or worker present in more than one log keeps its largest figure."""
    seconds: dict[str, int] = {}
    overhead: dict[int, int] = {}
    totals = set()
    for path in paths:
        try:
            times = measure_log(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"suite_shards: cannot measure {path}: {exc}", file=sys.stderr)
            return 2
        totals.add(times.total)
        for suite, value in times.seconds.items():
            seconds[suite] = max(value, seconds.get(suite, 0))
        if times.overhead is not None:
            overhead[times.index] = max(times.overhead,
                                        overhead.get(times.index, 0))
    if len(totals) != 1:
        print(f"suite_shards: the logs come from {len(totals)} worker counts",
              file=sys.stderr)
        return 2
    total = totals.pop()
    print("SUITE_SECONDS = {")
    for suite in sorted(seconds):
        print(f'    "{suite}": {seconds[suite]},')
    print("}")
    if sorted(overhead) == list(range(total)):
        print("WORKER_OVERHEAD_SECONDS = ("
              + ", ".join(str(overhead[worker]) for worker in range(total)) + ")")
    else:
        print(f"# no WORKER_OVERHEAD_SECONDS: complete logs for workers "
              f"{sorted(overhead)} of 0..{total - 1}")
    return 0


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
        seconds = {"future_suite": 1, "milan_dp": 1}
        ok = (SCHEDULED_SUITES == frozenset({"milan_dp_gptp"})
              and not SCHEDULED_SUITES & set(DEDICATED_SUITES)
              and default == ["future_suite", "milan_dp"]
              and physical == ["milan_dp_gptp"]
              and sorted(default + physical) == sorted(names)
              and all("milan_dp_gptp" not in select_suites(default, i, total,
                                                           seconds)
                      for total in (4, 5) for i in range(total)))
        print(f"  {'ok  ' if ok else 'FAIL'} scheduled/default partition: "
              f"default={default} physical={physical}")
        return ok


def dedicated_alone(suites: Sequence[str], total: int,
                    dedicated: Sequence[str],
                    seconds: Mapping[str, int]) -> bool:
    """Whether each name in `dedicated` is the only suite of its own worker.
    An empty `dedicated` sets nothing apart and proves nothing, so it is
    False rather than vacuously True."""
    first = total - len(dedicated)
    return bool(dedicated) and all(
        select_suites(suites, first + offset, total, seconds, dedicated)
        == [suite] for offset, suite in enumerate(dedicated))


def dedicated_selftest(suites: Sequence[str],
                       seconds: Mapping[str, int]) -> int:
    """Prove the dedicated workers hold their suite alone and move no other."""
    bad = 0
    rest = [suite for suite in suites if suite not in DEDICATED_SUITES]
    for total in (2, 4, 5, 7, 23):
        alone = dedicated_alone(suites, total, DEDICATED_SUITES, seconds)
        # Every other suite keeps the owner it has with no worker set aside.
        owners, _ = balance(suites, total, seconds, ())
        plain, _ = balance(rest, total - len(DEDICATED_SUITES),
                           {suite: seconds[suite] for suite in rest}, (), ())
        stable = all(owners[suite] == plain[suite] for suite in rest)
        ok = alone and stable
        print(f"  {'ok  ' if ok else 'FAIL'} {total:>2} shard(s): "
              f"dedicated alone={alone} balanced owners unchanged={stable}")
        bad += 0 if ok else 1

    # Negative control, and it runs through the helper itself ([R197] S2):
    # under a rule that sets nothing aside no worker holds a dedicated suite
    # alone, and `dedicated_alone` must say so for the arm above to prove
    # anything about the rule. Its two answers here are the ones a weakened
    # helper gets wrong: with nothing set aside a helper that always returns
    # True says yes, and with no more workers than dedicated suites the
    # dedicated suite shares worker 0 with every other, so a helper that
    # tests membership instead of equality says yes as well.
    plain = [select_suites(suites, index, 5, seconds, ()) for index in range(5)]
    unset = dedicated_alone(suites, 5, (), seconds)
    shared = (len(suites) > len(DEDICATED_SUITES)
              and dedicated_alone(suites, len(DEDICATED_SUITES),
                                  DEDICATED_SUITES, seconds))
    caught = (bool(DEDICATED_SUITES)
              and all([suite] not in plain for suite in DEDICATED_SUITES)
              and not unset and not shared)
    print(f"  {'ok  ' if caught else 'FAIL'} a rule without the dedicated "
          f"worker is caught (alone with none set aside={unset}, alone "
          f"while sharing worker 0={shared})")
    return bad + (0 if caught else 1)


def split_selftest(suites: Sequence[str], seconds: Mapping[str, int]) -> int:
    """Prove the split stays complete, disjoint and deterministic."""
    bad = 0
    for total in (1, 2, 4, 5, 7, 23):
        shards = [select_suites(suites, index, total, seconds)
                  for index in range(total)]
        flattened = [suite for shard in shards for suite in shard]
        complete = sorted(flattened) == sorted(suites)
        disjoint = len(flattened) == len(set(flattened))
        deterministic = shards == [select_suites(suites, index, total, seconds)
                                   for index in range(total)]
        ok = complete and disjoint and deterministic
        print(f"  {'ok  ' if ok else 'FAIL'} {total:>2} shard(s): "
              f"complete={complete} disjoint={disjoint} "
              f"deterministic={deterministic}")
        bad += 0 if ok else 1
    return bad


def measure_selftest() -> int:
    """Prove the log reader's windows, overhead and refusals on a known log."""
    def log(*rows: tuple[str, str]) -> str:
        """These rows as one worker's lines in `gh run view --log` form."""
        return "".join(f"Verilator shard 1/2\tUNKNOWN STEP\t{stamp}Z {message}\n"
                       for stamp, message in rows)
    head = (("\ufeff2026-01-01T00:00:00.5000000", "Current runner version"),
            ("2026-01-01T00:01:00.5000000", "shard: 1/2   selected suites: 2"),
            ("2026-01-01T00:01:10.6000000", "PASS     alpha"))
    tail = (("2026-01-01T00:03:10.6000000", "PASS     beta"),
            ("2026-01-01T00:03:10.6000001", "suites: 2   passed: 2   failed: 0"),
            ("2026-01-01T00:03:12.6000000", "Cleaning up orphan processes"))
    times = measure_log(log(*head, *tail))
    # alpha starts at the shard line, not at the job: 10.1 s rounds up to 11.
    # The overhead is 60 s of setup and 2 s after the last result.
    ok = times == LogTimes(1, 2, {"alpha": 11, "beta": 120}, 62)
    cut = measure_log(log(*head)) == LogTimes(1, 2, {"alpha": 11}, None)
    refused = []
    for bad_text in (log(*head[:2], ("2026-01-01T00:01:10.6000000",
                                     "TIMEOUT  alpha   (1800s wall clock)")),
                     log(*head[:1], *tail),
                     log(*head, ("2026-01-01T00:03:10.6", "suites: 1   passed")),):
        try:
            measure_log(bad_text)
            refused.append(False)
        except ValueError:
            refused.append(True)
    ok = ok and cut and all(refused)
    print(f"  {'ok  ' if ok else 'FAIL'} log windows {times.seconds}, overhead "
          f"{times.overhead} s, truncated log without overhead={cut}, "
          f"refused timeout/no shard line/short count={refused}")
    return 0 if ok else 1


def in_checkout() -> bool:
    """Whether this file is a tree's own scripts/suite_shards.py. A copy run
    from elsewhere, as test_suite_cancellation.py runs one, has no inventory
    and no workflow beside it to read."""
    return HERE.name == "suite_shards.py" and HERE.parent.name == "scripts"


def with_verilator_key(workflow: str, key: str, value: object) -> str:
    """rtl.yml's text with only the Verilator job's `key`, given with its
    indentation, set to `value`."""
    timeout, workers = verilator_job_limits(workflow)
    if key.strip() == "total":
        workers = int(str(value).strip("[]"))
    elif key.strip() == "timeout-minutes":
        timeout = int(value)
    else:
        raise ValueError("unknown worker fixture key")
    return (f"jobs:\n  {VERILATOR_JOB}:\n    timeout-minutes: {timeout}\n"
            f"    strategy:\n      matrix:\n        total: [{workers}]\n")


def with_driver_arm(driver: str, name: str, value: int) -> str:
    """run_all_suites.sh's text with suite_timeout's arm for `name` (or `*`)
    set to `value`, added just before the `*` arm when it has none."""
    lines = driver.splitlines(keepends=True)
    arm = f"    {name}) printf '%s\\n' \"${{SUITE_TIMEOUT:-{value}}}\" ;;\n"
    for number in range(lines.index("suite_timeout() {\n") + 1, len(lines)):
        if lines[number].lstrip().startswith(f"{name})"):
            lines[number] = arm
            return "".join(lines)
        if lines[number].lstrip().startswith("*)"):
            lines.insert(number, arm)
            return "".join(lines)
    raise ValueError("fixture drift: suite_timeout has no `*` arm")


def report(planted: str, caught: bool) -> int:
    """Print one planted defect's verdict; 1 when the gate let it through."""
    print(f"  {'[ok]   ' if caught else 'ESCAPED'} {planted}")
    return 0 if caught else 1


def planted_selftest(suites: Sequence[str], workflow: str,
                     load: Sequence[int], bounds: Sequence[int]) -> int:
    """Plant, on the head's own inventory, table and rtl.yml, each defect the
    gate exists for; the number the gate let through."""
    timeout, workers = verilator_job_limits(workflow)
    bound = max(bounds)
    bad = 0
    found, _, _ = headroom_problems([*suites, "unmeasured_suite"], workflow)
    bad += report("an inventory suite with no recorded duration is refused",
                  any(p.startswith("unmeasured_suite:") for p in found))
    try:
        select_suites(sorted([*suites, "unmeasured_suite"]), 0, workers)
        refused = False
    except ValueError:
        refused = True
    bad += report("a sharded selection refuses it too", refused)
    found, _, _ = headroom_problems(suites, workflow,
                                    {**SUITE_SECONDS, "retired_suite": 1})
    bad += report("a recorded duration with no inventory suite is refused",
                  any(p.startswith("retired_suite:") for p in found))
    zero = suites[0]
    found, _, _ = headroom_problems(suites, workflow, {**SUITE_SECONDS, zero: 0})
    bad += report(f"a recorded duration of 0 s ({zero}) is refused",
                  any(p.startswith(f"{zero}: recorded duration") for p in found))

    # The tightest timeout-minutes in rtl.yml that the head's busiest worker
    # exceeds must be refused, and one minute more must not: the bound moves
    # with the workflow's own value.
    peak = max(load)
    tight = max((m for m in range(1, timeout + 1) if bound_seconds(m) < peak),
                default=0)
    over, _, over_bound = headroom_problems(
        suites, with_verilator_key(workflow, "    timeout-minutes", tight))
    under, _, under_bound = headroom_problems(
        suites, with_verilator_key(workflow, "    timeout-minutes", tight + 1))
    bad += report(f"rtl.yml timeout-minutes {tight} (bound {bound_seconds(tight)}"
                  f" s) is refused for a {peak} s worker", bool(over))
    bad += report(f"and {tight + 1} minutes is not", not under)

    # The 60% itself. Every threshold above comes from bound_seconds, so a
    # looser percentage or formula moves them all together and they pass.
    # This one is computed without it: 60% of a minute is 36 s.
    applied = {timeout: bound, tight: max(over_bound), tight + 1: max(under_bound)}
    expected = {minutes: minutes * 36 for minutes in applied}
    bad += report(f"the bound applied at each timeout-minutes is 36 s a minute "
                  f"(60%): {dict(sorted(applied.items()))}, expected "
                  f"{dict(sorted(expected.items()))}", applied == expected)

    # The worker count is read from rtl.yml too, so one more worker there
    # than the overhead table describes must be refused.
    found, _, _ = headroom_problems(
        suites, with_verilator_key(workflow, "        total", f"[{workers + 1}]"))
    bad += report(f"rtl.yml at {workers + 1} workers is refused for the "
                  f"{len(WORKER_OVERHEAD_SECONDS)}-worker overhead table",
                  any(p.startswith("WORKER_OVERHEAD_SECONDS describes")
                      for p in found))

    # Planted heavy durations. The dedicated suite exactly at the bound with
    # its worker's overhead passes and one second more does not; a balanced
    # suite grown past every balanced worker's spare time together must put
    # one of them over, wherever the rule places it.
    last = workers - len(DEDICATED_SUITES)
    dedicated = DEDICATED_SUITES[0]
    at = bound - WORKER_OVERHEAD_SECONDS[last]
    found_at, _, _ = headroom_problems(suites, workflow,
                                       {**SUITE_SECONDS, dedicated: at})
    found_over, _, _ = headroom_problems(suites, workflow,
                                         {**SUITE_SECONDS, dedicated: at + 1})
    bad += report(f"{dedicated} at {at} s puts worker {last} exactly at the "
                  "bound and passes", not found_at)
    bad += report(f"{dedicated} at {at + 1} s puts it over and is refused",
                  bool(found_over))
    spare = sum(bound - load[worker] for worker in range(last))
    heavy = max((suite for suite in suites
                 if suite not in DEDICATED_SUITES and suite not in PINNED_SUITES),
                key=lambda suite: (SUITE_SECONDS[suite], suite))
    grown = SUITE_SECONDS[heavy] + spare + 1
    found, _, _ = headroom_problems(suites, workflow,
                                    {**SUITE_SECONDS, heavy: grown})
    bad += report(f"{heavy} grown by {spare + 1} s to {grown} s puts a balanced "
                  "worker over and is refused", bool(found))
    own = workflow.replace("|| 45", "|| 29")
    found, _, actual_bounds = headroom_problems(suites, own)
    bad += report("regular 29-minute workers retain their own 1044-second bound",
                  actual_bounds[:-1] == [1044] * (workers - 1)
                  and any("1044 s (60% of timeout-minutes 29)" in problem for problem in found))
    # Isolate the absolute rule from the percentage rule with deliberately wide limits.
    wide = with_verilator_key(workflow, "    timeout-minutes", 120)
    over_budget = {suite: 1 for suite in suites}
    over_budget[heavy] = 1621 - WORKER_OVERHEAD_SECONDS[0]
    found_at, at_load, _ = headroom_problems(
        suites, wide, {**over_budget, heavy: over_budget[heavy] - 1})
    bad += report("1620-second regular worker passes the absolute budget",
                  not found_at and max(at_load) == 1620)
    found, _, _ = headroom_problems(suites, wide, over_budget)
    bad += report("1621-second regular worker is refused below its own-limit bound",
                  any("exceeds the 1620 s CI budget" in problem for problem in found))
    return bad


def provisional_selftest(driver: str) -> int:
    """Plant provisional figures against the head's own run_all_suites.sh;
    the number of defects the gate let through."""
    _, default = driver_timeouts(driver)
    new = "provisional_suite"

    def held(text: str, value: int) -> bool:
        """Whether a provisional `new` at `value` s passes against `text`."""
        return not provisional_problems(text, {new: value}, {new})

    bad = report(f"a provisional suite at {default} s, suite_timeout's figure "
                 f"for it, passes, and at {default + 1} s is refused",
                 held(driver, default) and not held(driver, default + 1))
    # Read from the script, not mirrored: with the `*` arm planted a minute
    # longer that figure passes and the head's is refused, and a suite given
    # its own arm is held to that arm rather than to the default.
    longer = with_driver_arm(driver, "*", default + 60)
    bad += report(f"with suite_timeout's `*` arm planted at {default + 60} s, "
                  f"{default + 60} s passes and {default} s is refused",
                  held(longer, default + 60) and not held(longer, default))
    armed = with_driver_arm(driver, new, default + 120)
    bad += report(f"with its own arm planted at {default + 120} s, "
                  f"{default + 120} s passes and {default} s is refused",
                  held(armed, default + 120) and not held(armed, default))
    bad += report("a provisional suite with no figure in SUITE_SECONDS is "
                  "refused", bool(provisional_problems(driver, {}, {new})))
    return bad


def head_selftest() -> int:
    """Hold this tree's table to its inventory and rtl.yml's bound, prove
    the specialized owners, and plant each defect; the number of failures."""
    if not in_checkout():
        # A copy may skip only where there is nothing to read, so a test
        # that wrongly says "not a checkout" in a checkout fails instead.
        beside = [str(path.relative_to(ROOT))
                  for path in (WORKFLOW, SUITE_ROOT, DRIVER) if path.exists()]
        if beside:
            print(f"  FAIL head: {HERE.name} would skip its head arms with "
                  f"{', '.join(beside)} beside it")
            return 1
        print(f"  skip head arms: {HERE.name} is not scripts/suite_shards.py "
              "of a checkout, so there is no inventory or rtl.yml to read")
        return 0
    try:
        suites = expand_suites(sweep_suites(SUITE_ROOT))
        workflow = WORKFLOW.read_text(encoding="utf-8")
        driver = DRIVER.read_text(encoding="utf-8")
        problems, load, bounds = headroom_problems(suites, workflow)
        provisional = provisional_problems(driver)
    except (OSError, ValueError) as exc:
        print(f"  FAIL head: {exc}")
        return 1
    for problem in provisional:
        print(f"  FAIL head: {problem}")
    if not provisional:
        figures = {suite: SUITE_SECONDS[suite] for suite in sorted(PROVISIONAL_SUITES)}
        print(f"  ok   head provisional figures {figures} are what "
              "run_all_suites.sh's suite_timeout gives")
    # Table problems leave nothing to predict; otherwise each problem is a
    # worker over the bound, printed once on its own worker's line.
    for problem in problems if not load else ():
        print(f"  FAIL head: {problem}")
    for worker, value in enumerate(load):
        print(f"  {'ok  ' if value <= bounds[worker] else 'FAIL'} head worker "
              f"{worker}/{len(load)} predicted {value} s ({value / 60:.1f} "
              f"min), bound {bounds[worker]} s")
    if problems or provisional:
        return len(problems) + len(provisional)

    # The run-time half is the workflow's ownership step: tsn-gen and
    # Yosys/sv2v are installed on workers 1 and 3, and the last worker must run
    # milan_dp_mclk__0 alone, so a rule that moves any of them must fail here. The
    # balance alone can put a suite on its owner by chance, so each
    # specialized suite is also planted as the lightest and the heaviest.
    owners, _ = balance(suites, len(load))
    landmarks = {"tsn_fuzz": 1, "chmap_capture": 3, "milan_dp_mclk__0": len(load) - 1}
    got = {suite: owners.get(suite) for suite in landmarks}
    alone = dedicated_alone(suites, len(load), DEDICATED_SUITES, SUITE_SECONDS)
    specialized = ("tsn_fuzz", "chmap_capture")
    held = all(
        balance(suites, len(load),
                {**SUITE_SECONDS, **dict.fromkeys(specialized, planted)}
                )[0][suite] == landmarks[suite]
        for planted in (1, max(SUITE_SECONDS.values()) + 1)
        for suite in specialized)
    ok = got == landmarks and alone and held
    print(f"  {'ok  ' if ok else 'FAIL'} specialized owners {got}, "
          f"media-clock history alone={alone}, held at any planted duration={held}")
    shards = [select_suites(suites, index, len(load)) for index in range(len(load))]
    return ((0 if ok else 1) + seeded_selftest(shards)
            + planted_selftest(suites, workflow, load, bounds)
            + provisional_selftest(driver))


def seeded_selftest(shards: Sequence[Sequence[str]]) -> int:
    """Prove each worker gets the same list in its own process: every
    `--shard I/N` list printed under hash seeds 1 and 2 is the one selected
    here. Comparing two selections in one process cannot see a split that
    follows the process's hash seed."""
    total = len(shards)
    printed = []
    for seed in ("1", "2"):
        runs = [subprocess.run([sys.executable, str(HERE), "--suite-root",
                                str(SUITE_ROOT), "--ci-pieces", "--shard", f"{index}/{total}"],
                               capture_output=True, text=True, check=False,
                               env={**os.environ, "PYTHONHASHSEED": seed})
                for index in range(total)]
        printed.append([run.stdout.split() if run.returncode == 0 else None
                        for run in runs])
    ok = all(lists == [list(shard) for shard in shards] for lists in printed)
    print(f"  {'ok  ' if ok else 'FAIL'} the {total} --shard lists printed under "
          "hash seeds 1 and 2 are the ones selected here")
    return 0 if ok else 1


def selftest() -> int:
    """Prove the split stays complete, disjoint and stable; 0 when it does."""
    suites = sorted([f"suite-{number:02d}" for number in range(17)]
                    + list(DEDICATED_SUITES))
    seconds = {suite: 1 + (37 * number) % 101
               for number, suite in enumerate(suites)}
    bad = split_selftest(suites, seconds)
    bad += dedicated_selftest(suites, seconds)
    bad += 0 if scheduled_partition_selftest() else 1
    bad += measure_selftest()
    bad += head_selftest()

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
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--suite-root", type=Path,
                        help="directory containing one subdirectory per suite")
    parser.add_argument("--shard", default="0/1", metavar="INDEX/TOTAL",
                        help="zero-based shard to print (default: 0/1)")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--measure", nargs="+", type=Path, metavar="LOG",
                        help="print the duration tables from hosted worker logs")
    parser.add_argument("--ci-pieces", action="store_true",
                        help="use the driver-owned CI case partitions")
    parser.add_argument("--physical-gptp", action="store_true",
                        help="only the scheduled physical suite; absent from default shards")
    args = parser.parse_args(argv[1:])

    if args.selftest:
        return selftest()
    if args.measure:
        return measure_main(args.measure)
    if args.suite_root is None:
        parser.error("--suite-root is required unless --selftest or --measure is used")

    try:
        index, total = parse_shard(args.shard)
        if args.physical_gptp and (index, total) != (0, 1):
            raise ValueError("--physical-gptp uses its own unsharded job (0/1)")
        suites = sweep_suites(args.suite_root, physical=args.physical_gptp)
        if not suites:
            parser.error(f"no suite Makefiles found under {args.suite_root}")
        if args.ci_pieces:
            if args.physical_gptp:
                raise ValueError("the physical suite is never internally partitioned")
            suites = expand_suites(suites)
            selected = select_suites(suites, index, total)
        else:
            selected = select_suites(suites, index, total, SERIAL_SUITE_SECONDS, ())
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    for suite in selected:
        print(suite)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
