#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Program the Milan v1.2 entity identity into the NIC CSR 0x600 (ADP) group and
# enable it. The AECP/AEM listener reads the SAME group, so this one script
# configures both ADP advertise and AEM responses. Run on the board (busybox
# devmem) after loading a gateware that has the AECP listener (build_ax7101_*aecp*).
#
#   sh aecp_csr_setup.sh            # AX7101 (CSR base 0x90000000)
#   BASE=0x90000000 sh aecp_csr_setup.sh
#
# entity_id 02:00:00:FF:FE:00:00:01 matches the ADP EID the peer already knows.
set -e
B="${BASE:-0x90000000}"
w() { devmem $(printf '0x%x' $(( B + $1 ))) 32 "$2"; }

# identity (0x604..0x638)
w 0x604 0xFE000001     # ENTITY_ID low
w 0x608 0x020000FF     # ENTITY_ID high  -> 0x020000FF_FE000001
w 0x60C 0x00000000     # entity_model_id low
w 0x610 0x00000000     # entity_model_id high
w 0x614 0x0000C588     # entity_capabilities: AEM|CLASS_A|GPTP|VU|IDENTIFY|IFACE_IDX
w 0x618 0x48010008     # ADP_TALK  {talker_caps=0x4801, talker_sources=8}
w 0x61C 0x48010008     # ADP_LIST  {listener_caps=0x4801, listener_sinks=8}
w 0x620 0x00000000     # controller_capabilities
w 0x624 0x00000000     # gPTP grandmaster id low
w 0x628 0x00000000     # gPTP grandmaster id high
w 0x62C 0x00000000     # gPTP domain number
w 0x630 0x00000000     # ADP_IDX0: current_configuration_index = 0
w 0x634 0x00000000     # ADP_IDX1: identify/interface index = 0
w 0x638 0x00000000     # association id low

# enable: ADP_CTRL[0]=enable, valid_time=0x1F (validity 62 s)
w 0x600 0x00001F01

echo "identity programmed; ADP+AECP enabled. status:"
printf '  ADP_CTRL   0x600 = '; devmem $(printf '0x%x' $(( B + 0x600 ))) 32
printf '  AECP_STAT0 0x648 = '; devmem $(printf '0x%x' $(( B + 0x648 ))) 32
printf '  AECP_STAT1 0x64C = '; devmem $(printf '0x%x' $(( B + 0x64C ))) 32
