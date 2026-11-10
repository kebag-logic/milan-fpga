#!/usr/bin/env python3
"""Differential probe: the base runner and the head runner under the default command line.

Usage: python3 -I probe_default_equivalence.py <base act_ci.py> <head act_ci.py> <shipping root>

Loads both runners as separate modules and compares, under the default
geometry (no --jobs/--job-cpus/--job-memory), and under the head's explicit
spelling of that default (--jobs 4 --job-cpus 16 --job-memory 8):
  * parse_cpu_ranges over a generated corpus (result or refusal text);
  * job_cpu_ranges over booked-range sets and concurrency 0..10;
  * replay_container_concurrency over every shipping workflow;
  * the complete act command line build_act_command produces per workflow
    (run-directory path, port and token normalised);
  * main()'s status, stderr and reached collaborators for a set of argvs.
Also checks, against an independent oracle written here from the issue's
words (aligned to the chosen width, distinct, within the host), that the
head's parse_cpu_ranges accepts and refuses exactly the right range lists at
every width 16/8/6 and several host sizes.
Prints one line per comparison and a final PROBE: PASS or PROBE: FAIL.
"""
from __future__ import annotations

import contextlib
import contextvars
import importlib.util
import itertools
import json
import os
import pathlib
import random
import sys
from unittest import mock

failures: list[str] = []


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def outcome(module, fn):
    try:
        return ("ok", fn())
    except module.Refusal as exc:
        return ("refused", str(exc))


def report(label: str, ok: bool, detail: str = "") -> None:
    print(("ok   " if ok else "FAIL ") + label + (f" -- {detail}" if detail and not ok else ""))
    if not ok:
        failures.append(label)


def corpus(rng: random.Random) -> list[str]:
    texts = ["", "0-15", "0-11", "0-7", "0-5", "16-31", "0-15,16-31,32-47,48-63",
             "0-11,12-23,24-35,36-47", "0-15,24-35", "0-15,0-15", "8-23", "3-14",
             "00-15", "0-015", "-1-14", " 0-15", "0-15,", ",0-15", "15-0", "48-63,64-79",
             "496-511", "500-511", "512-527", "0-15,16-27", "12-23", "24-35,0-15",
             "0-5,6-11", "0-7,8-15", "a-b", "0 - 15", "0-15,16-31,32-47,48-63,64-79"]
    widths = (16, 12, 8, 6, 4, 32, 10)
    for _ in range(3000):
        parts = []
        for _ in range(rng.randint(1, 9)):
            w = rng.choice(widths)
            first = rng.choice((rng.randrange(0, 600), w * rng.randrange(0, 40)))
            parts.append(f"{first}-{first + w - 1}")
        texts.append(",".join(parts))
    return texts


def oracle(raw: str, widths: tuple[int, ...], host: int) -> bool:
    """Accept iff every range is canonical, of an allowed width, aligned to it, within the host, and disjoint."""
    if not raw:
        return False
    held: set[int] = set()
    for text in raw.split(","):
        ends = text.split("-")
        if len(ends) != 2 or not all(e.isdigit() and (e == "0" or not e.startswith("0")) for e in ends):
            return False
        first, last = int(ends[0]), int(ends[1])
        width = last - first + 1
        if width not in widths or first % width or last >= host:
            return False
        cpus = set(range(first, last + 1))
        if cpus & held:
            return False
        held |= cpus
    return True


def build_commands(module, shipping_root: pathlib.Path, ranges: tuple[str, ...]) -> dict[str, list[str]]:
    fixture = module.selftest_fixture()
    out: dict[str, list[str]] = {}
    with module.temporary_run_directory(False) as root:
        layout = module.make_layout(root, fixture.pr)
        docker = module.selftest_docker_fixture(layout)
        with mock.patch.object(module, "BOOKED_CPU_RANGES",
                               contextvars.ContextVar("probe_ranges", default=ranges)):
            for workflow in module.WORKFLOWS:
                command = module.build_act_command(["act"], workflow, layout, docker.port, docker.boundary)
                text = json.dumps(command).replace(str(root), "<RUN>").replace(str(docker.port), "<PORT>")
                out[workflow] = json.loads(text)
    return out


def main() -> int:
    base = load("act_ci_base", sys.argv[1])
    head = load("act_ci_head", sys.argv[2])
    shipping = pathlib.Path(sys.argv[3]).resolve()
    rng = random.Random(873)
    texts = corpus(rng)

    explicit_default = head.JobGeometry(4, 16, 8)
    report("head default geometry equals explicit 4 x 16 x 8", head.DEFAULT_JOB_GEOMETRY == explicit_default)

    # parse_cpu_ranges, default geometry, several host sizes.
    for host in (1, 12, 16, 32, 64, 128, 512):
        with mock.patch.object(os, "cpu_count", return_value=host):
            diffs = [t for t in texts if outcome(base, lambda t=t: base.parse_cpu_ranges(t or None))
                     != outcome(head, lambda t=t: head.parse_cpu_ranges(t or None))]
        report(f"parse_cpu_ranges identical base vs head (default) over {len(texts)} inputs at {host} host CPUs",
               not diffs, repr(diffs[:3]))
    # job_cpu_ranges.
    booked_sets = [("0-15",), ("0-15", "16-31"), ("0-15", "16-31", "32-47", "48-63"),
                   ("0-11", "12-23", "24-35", "36-47"),
                   ("0-15", "16-31", "32-47", "48-63", "64-79", "80-95")]
    with mock.patch.object(os, "cpu_count", return_value=128):
        diffs = []
        for booked in booked_sets:
            for concurrency in range(0, 11):
                for slot in (0, 1, 63):
                    a = outcome(base, lambda: (mock.patch.object(base, "BOOKED_CPU_RANGES",
                                contextvars.ContextVar("p", default=booked)).start(),
                                base.job_cpu_ranges(slot, concurrency))[1])
                    mock.patch.stopall()
                    b = outcome(head, lambda: (mock.patch.object(head, "BOOKED_CPU_RANGES",
                                contextvars.ContextVar("p", default=booked)).start(),
                                head.job_cpu_ranges(slot, concurrency))[1])
                    mock.patch.stopall()
                    if a != b:
                        diffs.append((booked, concurrency, slot, a, b))
        report("job_cpu_ranges identical base vs head (default) over booked sets x concurrency 0-10 x slots",
               not diffs, repr(diffs[:2]))
    # replay_container_concurrency on the shipping workflows.
    a = {w: outcome(base, lambda w=w: base.replay_container_concurrency(shipping, (w,))) for w in base.WORKFLOWS}
    b = {w: outcome(head, lambda w=w: head.replay_container_concurrency(shipping, (w,))) for w in head.WORKFLOWS}
    all_a = outcome(base, lambda: base.replay_container_concurrency(shipping, tuple(base.WORKFLOWS)))
    all_b = outcome(head, lambda: head.replay_container_concurrency(shipping, tuple(head.WORKFLOWS)))
    print("     shipping concurrency base", a, all_a)
    print("     shipping concurrency head", b, all_b)
    report("replay_container_concurrency identical on every shipping workflow and all together",
           a == b and all_a == all_b)
    # The full act command per workflow.
    with mock.patch.object(os, "cpu_count", return_value=128):
        for booked in booked_sets:
            ca = build_commands(base, shipping, booked)
            cb = build_commands(head, shipping, booked)
            with mock.patch.object(head, "JOB_GEOMETRY",
                                   contextvars.ContextVar("p", default=explicit_default)):
                cc = build_commands(head, shipping, booked)
            report(f"act command identical base vs head default vs head explicit 4x16x8, ranges {','.join(booked)}",
                   ca == cb == cc, json.dumps([w for w in ca if ca[w] != cb[w] or cb[w] != cc[w]]))
        sample = build_commands(head, shipping, booked_sets[2])["rtl-full"]
        idx = sample.index("--concurrent-jobs")
        print("     head default rtl-full act words:", sample[idx:idx + 7])
    # main() through the recorded-collaborator harness, base vs head.
    argvs = [
        (["--pr", "1"], ("0-15", "16-31", "32-47", "48-63")),
        (["--pr", "1"], ("0-11", "12-23")),
        (["--pr", "1"], ("0-7", "8-15")),
        (["--pr", "1"], ("0-5",)),
        (["--pr", "1"], ("0-15", "8-23")),
        (["--pr", "1"], ("3-18",)),
        (["--pr", "1"], ("512-527",)),
        (["--pr", "1"], ()),
        (["--pr", "0"], ("0-15",)),
        (["--pr", "1", "--dry-run"], ("0-15",)),
        (["--interrupt-selftest"], ("0-15",)),
        (["--boundary-selftest"], ("0-15",)),
        (["--selftest", "--pr", "1"], ()),
    ]
    clean = {"PATH": "/usr/bin:/bin"}
    for argv, booked in argvs:
        with mock.patch.object(base, "BOOKED_CPU_RANGES", contextvars.ContextVar("p", default=booked)):
            ra = base.main_with_recorded_collaborators(argv, clean)
        with mock.patch.object(head, "BOOKED_CPU_RANGES", contextvars.ContextVar("p", default=booked)), \
                mock.patch.object(head, "JOB_GEOMETRY", contextvars.ContextVar("g", default=head.DEFAULT_JOB_GEOMETRY)):
            rb = head.main_with_recorded_collaborators(argv, clean)
        extra = [] if "--selftest" in argv else ["--jobs", "4", "--job-cpus", "16", "--job-memory", "8"]
        with mock.patch.object(head, "BOOKED_CPU_RANGES", contextvars.ContextVar("p", default=booked)), \
                mock.patch.object(head, "JOB_GEOMETRY", contextvars.ContextVar("g", default=head.DEFAULT_JOB_GEOMETRY)):
            rc = head.main_with_recorded_collaborators(argv + extra, clean)
        # A usage error prints argparse's usage banner, which at head also lists the
        # three new options; compare the status, the final error line and the
        # collaborators reached, which is what the operator's command line decides.
        def key(result):
            status, stderr, reached = result
            lines = stderr.strip().splitlines()
            return status, (lines[-1] if lines else ""), reached
        same = ra == rb == rc if not ra[1].startswith("usage:") else key(ra) == key(rb) == key(rc)
        report(f"main {' '.join(argv)} --cpu-ranges {','.join(booked) or '<empty>'}: base == head == head explicit default "
               f"(status {ra[0]}, reached {ra[2]}, last line {key(ra)[1]!r})", same, repr((ra, rb, rc)))
    # Oracle: every width, several host sizes.
    for cpus, widths in ((16, (16, 12)), (8, (8,)), (6, (6,))):
        for jobs, mem in ((4, 8), (8, 4)):
            try:
                geometry = head.JobGeometry(jobs, cpus, mem)
            except head.Refusal:
                continue
            for host in (6, 12, 16, 48, 64, 128, 512):
                with mock.patch.object(os, "cpu_count", return_value=host), \
                        mock.patch.object(head, "JOB_GEOMETRY", contextvars.ContextVar("g", default=geometry)):
                    wrong = []
                    for t in texts:
                        got = outcome(head, lambda t=t: head.parse_cpu_ranges(t or None))[0] == "ok"
                        if got != oracle(t, widths, host):
                            wrong.append(t)
                report(f"head parse_cpu_ranges matches the aligned/distinct/within-host oracle at geometry "
                       f"{jobs}x{cpus}x{mem}, widths {widths}, {host} host CPUs", not wrong, repr(wrong[:3]))
    # Every accepted geometry obeys both bounds; every refused one violates a bound or a range (exhaustive).
    bad = []
    for jobs, cpus, mem in itertools.product(range(-1, 11), (0, 4, 6, 8, 12, 16, 32), range(-1, 11)):
        ok = outcome(head, lambda: head.JobGeometry(jobs, cpus, mem))[0] == "ok"
        want = (1 <= jobs <= 8 and cpus in (16, 8, 6) and 1 <= mem <= 8
                and jobs * mem + 4 <= 36 and jobs * cpus <= 64)
        if ok != want:
            bad.append((jobs, cpus, mem))
    report("JobGeometry accepts exactly the shapes with 1<=jobs<=8, width 16/8/6, 1<=mem<=8, "
           "jobs*mem+4<=36 and jobs*width<=64 (exhaustive grid)", not bad, repr(bad[:5]))
    print("PROBE: " + ("PASS" if not failures else f"FAIL ({len(failures)})"))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
