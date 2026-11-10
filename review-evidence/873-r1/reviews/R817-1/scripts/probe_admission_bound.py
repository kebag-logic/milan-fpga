#!/usr/bin/env python3
"""Probe: act's admission word stays bounded by the geometry when more ranges are booked than jobs.

Usage: python3 -I probe_admission_bound.py <head act_ci.py>

The memory bound jobs x cap + service <= slot holds for the replay only if
act admits at most `jobs` containers. build_act_command passes act
`--concurrent-jobs min(jobs, booked ranges)`; this probe prints that word,
and the dispatcher's admission limit it implies, for booked-range counts
below, equal to and above the job count, at the default and at 8 x 6 x 4.
"""
from __future__ import annotations

import contextvars
import importlib.util
import os
import sys
from unittest import mock

spec = importlib.util.spec_from_file_location("act_ci_head", sys.argv[1])
head = importlib.util.module_from_spec(spec)
sys.modules["act_ci_head"] = head
spec.loader.exec_module(head)

failures = 0
fixture = head.selftest_fixture()
with mock.patch.object(os, "cpu_count", return_value=512), head.temporary_run_directory(False) as root:
    layout = head.make_layout(root, fixture.pr)
    docker = head.selftest_docker_fixture(layout)
    for geometry in (head.DEFAULT_JOB_GEOMETRY, head.JobGeometry(8, 6, 4), head.JobGeometry(2, 16, 8)):
        width = geometry.range_widths[0]
        for booked in (1, geometry.jobs, geometry.jobs + 1, 12):
            ranges = tuple(f"{n * width}-{n * width + width - 1}" for n in range(booked))
            with mock.patch.object(head, "JOB_GEOMETRY", contextvars.ContextVar("g", default=geometry)), \
                    mock.patch.object(head, "BOOKED_CPU_RANGES", contextvars.ContextVar("r", default=ranges)):
                command = head.build_act_command(["act"], "rtl-full", layout, docker.port, docker.boundary)
                admitted = int(command[command.index("--concurrent-jobs") + 1])
                memory = admitted * geometry.memory_gib + head.SLOT_SERVICE_MEMORY_GIB
            ok = admitted == min(geometry.jobs, booked) and memory <= head.SLOT_MEMORY_GIB
            failures += not ok
            print(f"{'ok  ' if ok else 'FAIL'} geometry {geometry.jobs}x{geometry.cpus}x{geometry.memory_gib}g, "
                  f"{booked} booked ranges: --concurrent-jobs {admitted}, slot memory need {memory} of "
                  f"{head.SLOT_MEMORY_GIB} GiB")
print("PROBE: " + ("PASS" if not failures else f"FAIL ({failures})"))
raise SystemExit(1 if failures else 0)
