#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Program the Milan v1.2 entity identity into the NIC CSR 0x600 group and
# enable the entity. Run on the board (busybox devmem) after loading a
# gateware.
#
#   sh aecp_csr_setup.sh            # AX7101 (CSR base 0x90000000)
#   BASE=0x90000000 sh aecp_csr_setup.sh
#
# WHAT THIS SCRIPT NO LONGER DOES (2026-08-12). It used to be true that "the
# AECP/AEM listener reads the SAME group, so this one script configures both
# ADP advertise and AEM responses". THAT LISTENER IS DELETED - the whole
# hdl/ieee17221/{aecp,acmp} plane and hdl/ieee8021q/srp with it - and the
# protocol-processor submodule advertises now. This device answers NO
# AECP/AEM command, so nothing here configures an AEM response.
#
# WHICH WRITES STILL DO SOMETHING. Every register below was checked against
# the KL_pp_shadow / protocol_processor_top port map in
# hdl/milan/milan_datapath.sv. A word with no port on that plane is ACCEPTED
# BY THE CSR BLOCK AND READ BY NOTHING, and the ones that were in that state
# have been REMOVED from this script rather than left looking effective:
#
#   LIVE - reaches the advertising plane:
#     0x604/0x608  entity_id            -> entity_id_i
#     0x60C/0x610  entity_model_id      -> entity_model_id_i
#     0x624/0x628  gPTP grandmaster id  -> gm_id_i (an edge also raises
#                                         gm_change_i, the 1722.1-2021 6.2.6
#                                         re-advertise event)
#     0x630        current_configuration_index -> current_cfg_i
#     0x634        identify/interface index    -> identify_index_i
#     0x600 bit 0  entity enable        -> enable_i (either this bit or
#                                         PP_CTRL.en at 0x920 bit 0 enables
#                                         the entity; there is one plane now)
#
#   REMOVED - accepted by the CSR block, no port on the plane, read by
#   nothing. Writing them looked like configuration and was not:
#     0x614        entity_capabilities
#     0x620        controller_capabilities
#     0x638        association_id
#     0x600 valid_time field (the 0x1F this script used to set): the plane
#                  owns its own validity timing.
#
#   NEVER WRITTEN HERE, deliberately:
#     0x618/0x61C  talker_stream_sources / listener_stream_sinks are READ-ONLY
#                  words hardwired from gen/adp_shape_defaults.svh (the
#                  elaborated shape). A stream count is a physical fact about
#                  the built bitstream - software cannot make a ninth stream
#                  engine by writing a register - and a writable count is how
#                  the 8x8 board came to advertise 1 source / 2 sinks on
#                  2026-07-27. Read them back:  r 0x618 ; r 0x61C
#     0x62C        gPTP domain number resets to ADP_GPTP_DOMAIN_C, generated
#                  from the config's `gptp.domain` - the SAME number the
#                  builder writes into /etc/gptp.<board>.cfg as domainNumber.
#                  This line used to hardcode 0 and agreed with the config
#                  only because the shipping config says 0. The register
#                  stays WRITABLE (Milan v1.2 5.3.6.1 makes the gPTP domain
#                  number dynamic state), it just must not be clobbered here.
#                  Milan 2 pins [802.1AS] to 802.1AS-2011 +Cor1 +Cor2 (NOT
#                  -2020), whose 8.1 says "The domain number of a gPTP domain
#                  shall be 0" - on a Milan network this reads 0 or the
#                  network is wrong.  Read it back:  r 0x62C
#
# entity_id 02:00:00:FF:FE:00:00:01 matches the ADP EID the peer already knows.
set -e
B="${BASE:-0x90000000}"
w() { devmem $(printf '0x%x' $(( B + $1 ))) 32 "$2"; }

# identity (0x604..0x634) - every line below has a port on the advertising
# plane; see the header for the ones that did not and were dropped.
w 0x604 0xFE000001     # ENTITY_ID low
w 0x608 0x020000FF     # ENTITY_ID high  -> 0x020000FF_FE000001
w 0x60C 0x00000000     # entity_model_id low
w 0x610 0x00000000     # entity_model_id high
w 0x624 0x00000000     # gPTP grandmaster id low
w 0x628 0x00000000     # gPTP grandmaster id high
w 0x630 0x00000000     # ADP_IDX0: current_configuration_index = 0
w 0x634 0x00000000     # ADP_IDX1: identify/interface index = 0

# enable the entity: ADP_CTRL[0]
w 0x600 0x00000001

echo "identity programmed; entity enabled. status:"
printf '  ADP_CTRL   0x600 = '; devmem $(printf '0x%x' $(( B + 0x600 ))) 32
# the ELABORATED shape, read-only - this is the answer to "what did this
# bitstream actually get built as". The old AECP_STAT0/1 readback at
# 0x648/0x64C is gone: with no AECP engine behind them those words are
# structural zeros, and printing a zero as if it were a status is worse than
# printing nothing.
printf '  ADP_TALK   0x618 = '; devmem $(printf '0x%x' $(( B + 0x618 ))) 32
printf '  ADP_LIST   0x61C = '; devmem $(printf '0x%x' $(( B + 0x61C ))) 32
printf '  GPTP_DOM   0x62C = '; devmem $(printf '0x%x' $(( B + 0x62C ))) 32
