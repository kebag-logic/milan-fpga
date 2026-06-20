# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# behave environment setup for AECP BDD tests

import os
import subprocess

TSAGEN_DIR = os.environ.get("TSAGEN_DIR", "/home/alex/tsn-gen")
PROTOCOLS_DIR = os.path.join(TSAGEN_DIR, "protocols")
DUT_SOCKET   = os.environ.get("DUT_SOCKET", "/work/sock/aecp.sock")
PACKET_GEN   = os.path.join(TSAGEN_DIR, "build/traffic-gen/packet_gen")

def before_all(context):
    context.protocols_dir = PROTOCOLS_DIR
    context.dut_socket    = DUT_SOCKET
    context.packet_gen    = PACKET_GEN
    context.has_packet_gen = os.path.isfile(PACKET_GEN)
    context.entity_id     = 0x001BC5FFFE112233
    context.controllers   = {}

def before_scenario(context, scenario):
    context.seq_id = 0
    context.last_response = None

def after_scenario(context, scenario):
    pass
