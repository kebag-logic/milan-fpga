#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# gptp_probe.sh <tag> [alinx-ip] [arty-ip]
#
# One snapshot of the whole gPTP domain, for the D7 acceptance procedure in
# docs/findings/GPTP_GM_LOSS_UNDER_RX_LOAD.md. RUNS ON THE PEER HOST (the dev
# box is never on the AVB subnet).
#
# WHY pmc AND NOT OUR OWN CSRs. 0x624/0x628 is a MIRROR published by the
# gptp2csr.sh daemon; it tells you what software last wrote, not what the BMCA
# decided. `pmc GET PORT_STATS_NP` is ptp4l's own per-message-type counter, so
# two samples give the ACTUAL Announce/Sync/Pdelay rates over the window - the
# only way to tell "the grandmaster went silent" from "the peers got picky".
# Both are printed: when they disagree, the CSR is the stale one.
#
# THREE STACKS, ON PURPOSE. The peer, the ALINX and the Arty each run an
# independent ptp4l. A grandmaster change agreed by all three is a fact about
# the segment; one seen only in our own registers is a fact about our daemon.
#
# TWO TRAPS THIS SCRIPT ALREADY AVOIDS:
#   * `pmc -u` needs `-t 1` here. The profile is gPTP (transportSpecific 0x1)
#     and ptp4l silently ignores management messages whose transportSpecific
#     does not match - it prints "sending: ..." and then nothing, which looks
#     exactly like a dead daemon.
#   * On the peer, pass `-s /var/run/ptp4l` explicitly; the default client
#     socket path fails to bind there ("uds: bind failed").
#
# devmem costs ~0.75 s per call, so everything compared is read in ONE ssh.

set -u
TAG=${1:-sample}
ALINX=${2:-192.168.127.1}
ARTY=${3:-192.168.127.3}

SSHO="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=6"
FILT='rx_Announce|rx_Sync |rx_Pdelay_Resp |rx_Follow_Up|tx_Announce|tx_Sync |tx_Pdelay_Req|gmPresent|gmIdentity|master_offset|grandmasterIdentity|grandmasterPriority1|portState'
# ptp4l's own words for a BMCA event - counting these is how you tell a real
# re-election from a servo wobble.
BM='selected best master|assuming the grand master|TIMEOUT_EXPIRES|new foreign master|to MASTER|to SLAVE|to UNCALIBRATED|to LISTENING|to FAULTY'

echo "### tag=$TAG wall=$(date +%s.%N)"

echo "--- peer ---"
cd /tmp || exit 1
sudo pmc -u -b 0 -t 1 -s /var/run/ptp4l \
  'GET PORT_STATS_NP' 'GET TIME_STATUS_NP' 'GET PARENT_DATA_SET' 'GET PORT_DATA_SET' 2>&1 \
  | grep -aE "$FILT" | tr -s ' \t' ' '

for B in "$ALINX" "$ARTY"; do
  echo "--- board $B ---"
  timeout 20 ssh $SSHO "root@$B" "cd /tmp; \
    pmc -u -b 0 -t 1 'GET PORT_STATS_NP' 'GET TIME_STATUS_NP' 'GET PARENT_DATA_SET' 'GET PORT_DATA_SET' 2>&1 \
      | grep -aE '$FILT' | tr -s ' \t' ' '; \
    echo -n ' version_04='; devmem 0x90000004 32; \
    echo -n ' csr_gm_lo_624='; devmem 0x90000624 32; \
    echo -n ' csr_gm_hi_628='; devmem 0x90000628 32; \
    echo -n ' csr_linkg_774='; devmem 0x90000774 32; \
    echo -n ' csr_clkv_stat_77C='; devmem 0x9000077C 32; \
    echo -n ' csr_tucnt_780='; devmem 0x90000780 32; \
    echo -n ' rx_pkts='; cat /sys/class/net/eth0/statistics/rx_packets; \
    echo -n ' rx_drop='; cat /sys/class/net/eth0/statistics/rx_dropped; \
    echo -n ' tx_pkts='; cat /sys/class/net/eth0/statistics/tx_packets; \
    echo -n ' bmca_events='; cat /var/log/messages.0 /var/log/messages 2>/dev/null \
      | grep -a ' ptp4l:' | grep -acE '$BM'" \
    2>&1 | grep -av Warning
done
