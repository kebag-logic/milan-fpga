# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# behave environment setup for AECP BDD tests

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.model import Scenario
    from behave.runner import Context

TSAGEN_DIR = Path(os.environ.get("TSAGEN_DIR", "~/tsn-gen")).expanduser()
PROTOCOLS_DIR = TSAGEN_DIR / "protocols"
DUT_SOCKET   = Path(os.environ.get("DUT_SOCKET", "/work/sock/aecp.sock"))
PACKET_GEN   = TSAGEN_DIR / "build/traffic-gen/packet_gen"

def before_all(context: Context) -> None:
    """Seed the context every feature shares: the bench paths, the entity id
    and an empty controller table.

    The three path values are historical. The frame-generating tier is gone and
    no surviving scenario reads them (tests/README.md T1); they stay so that a
    scenario needing a real generator can still gate on ``has_packet_gen``
    rather than discovering its absence as a crash.
    """
    context.protocols_dir = PROTOCOLS_DIR
    context.dut_socket    = DUT_SOCKET
    context.packet_gen    = PACKET_GEN
    context.has_packet_gen = PACKET_GEN.is_file()
    context.entity_id     = 0x001BC5FFFE112233
    context.controllers   = {}

def before_scenario(context: Context, scenario: Scenario) -> None:
    """Clear the per-scenario AECP sequence id and response slot, so one
    scenario cannot pass on an answer another scenario left behind."""
    context.seq_id = 0
    context.last_response = None

def after_scenario(context: Context, scenario: Scenario) -> None:
    """Deliberately nothing: these steps are offline and own no socket,
    subprocess or temporary file that a teardown would have to reclaim."""
    pass
