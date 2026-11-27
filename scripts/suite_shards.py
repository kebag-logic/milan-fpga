#!/usr/bin/env python3
r"""Balance the physical serial inventory and the case-partitioned CI inventory.

The serial sweep discovers every Makefile except the scheduled physical gPTP suite.
CI partitions eight parents; driver-owned cases and executed receipts prove their union.

Longest-first scheduling balances the regular workers (#781, #799, #998); the tsn-gen owner stays at worker 1 and
the netlist owner at worker 3. Leg A, one continuous media-clock history, runs alone on the final worker under #737's
explicit timing exception. Every other worker must project at most CI_BUDGET_SECONDS including setup. The older
60-percent timeout bound remains an additional gate, including for the exception.

New suites must enter both the discovered inventory and duration table. Until a
hosted window is measured, register the exact run_all_suites.sh timeout as a
provisional estimate; the selftest checks that value against the driver. Never
hide a new suite by omitting it from selection. A changed count or timeout is read
from the generated workflow, and omission, ownership, overflow and deterministic
selection controls must still pass.

    python3 scripts/suite_shards.py --suite-root tb/verilator --ci-pieces --shard 0/29
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

#: Issue #998, REQ-VER-01, REQ-VER-04: 30 minutes on a runner 1.41 times as slow (CI_WORKFLOWS.md, "The #998 budget").
CI_BUDGET_SECONDS = int(30 * 60 / 1.41)

#: The tree this file belongs to, and the three things its head arms read.
ROOT = Path(__file__).resolve().parents[1]
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
#: pull-request run 38538854504 at 7fb3664b measured 474 s). `media_phase`
#: (#781) keeps its 1400 s suite_timeout figure, above its own hosted window:
#: 582 s passing on worker 4/17 of pull-request run 40131149135 at 8a4fa2f9
#: (job 120983200812, whose suite step ran 655 s for its four suites), while
#: three earlier hosted windows ran past 900 s to TIMEOUT, so its variance is wide.
#: #799: the ruled replay set (CI_WORKFLOWS.md) but media_phase carries its largest window in runs 40724689169 and
#: 40740015218; follow_ring 1493 s, dev run 40460559108. #998 raises what its three runs exceeded (CI_WORKFLOWS.md).
SUITE_SECONDS = {
    "aaf": 77,
    "aaf_audio_loop": 22,
    "aaf_clock_meter": 1055,
    "aaf_latency_tap_bank": 16,
    "aaf_latency_taps": 15,
    "adp_tx": 12,
    "aes3": 6,
    "avtp_parser": 27,
    "avtp_rxmon": 455,
    "avtp_stream": 11,
    "capture_coherence": 1737,
    "cbs": 6,
    "cdc": 6,
    "chmap_capture": 176,
    "chmap_render": 6,
    "classifier": 6,
    "clkvalid": 18,
    "cls": 6,
    "controller_rate": 9,
    "crf_rx": 832,
    "crf_tx": 6,
    "csr": 329,
    "datapath": 6,
    "eth_tx_reset": 6,
    "follow_ring": 1493,
    "fw_service_budget": 2,
    "gptp_plane": 784,
    "gptp_shadow": 679,  # #1008: max(672, 679), runs 45735453538 and 45755846909 at gptp-processor 3ce71b76
    "gptp_tables": 568,
    "gptp_txts": 107,
    "i2spb": 15,
    "ifg": 6,
    "input_loopback": 300,
    "input_loopback_dp": 300,
    "lat_history_ring": 6,
    "link_guard": 7,
    "maap": 1375,
    "mac_rmon": 12,
    "mbx": 299,
    "media_grid_align": 255,
    "media_nco": 17,
    "media_phase": 1400,
    "milan_dp": 2797,
    "milan_dp_gm_steps": 926,
    "milan_dp_mclk": 2038,
    "milan_dp_render": 1264,
    "mmcm_servo": 1145,
    "mmcm_servo_autorepair": 6,
    "nvm_backend": 38,
    "nvm_cosim": 801,
    "pair_fill": 6,
    "pcmlpf": 6,
    "pp_shadow": 1251,
    "ptp": 26,
    "ptp_sync": 11,
    "ptp_ts": 127,
    "queues": 6,
    "reboot_ctrl": 300,
    "render_queue": 126,
    "rx_filter": 18,
    "shaper_core": 7,
    "tcam": 29,
    "tcam_csr": 6,
    "tdm": 7,
    "tdm_render": 21,
    "tkdiag": 28,
    "tsn_fuzz": 62,
    "usbaudio": 900,
