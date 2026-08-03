#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# net_throughput_ab.sh [peer-ip] [reps] [cfg ...]
#
# A/B TCP throughput bisect for the board's single RV32 hart. RUNS ON THE BOARD
# (busybox ash); the peer runs `iperf3 -s -p 5201`. Measures BOTH directions so
# an RX-only defect (shield / RSC) separates from a symmetric one (CPU / stack).
#
# Every knob below is RUNTIME and REVERSIBLE - no module reload, no reflash. A
# single EXIT trap restores the as-found posture even on Ctrl-C or timeout, so
# this is safe to run on a live bench. ptp4l and phc2sys are NEVER touched.
#
# Configs (space-separated, default = all):
#   asfound   as-found posture, the number the user sees
#   quiet     console loglevel 1 (netdev_info stops blocking on the 115200 UART)
#   noloops   SIGSTOP the busybox shell-loop daemons (fork/exec churn)
#   coal250   rx-usecs 250 (the driver's KL_RX_USECS_DEFAULT) instead of 5000
#   napi90    raise the napi threads above ktimers/0 (70) and ptp4l (80)
#   best      quiet + noloops + coal250 together
#
# Reported per row: median of `reps` runs, Mbit/s, plus the CPU-idle delta over
# the run window. An idle delta of ~0 means the hart is SATURATED and throughput
# is compute-bound - the single most important number this script produces,
# because per-process CPU accounting (what `time wget` shows) does NOT see the
# softirq/napi/daemon time that actually consumes the hart.

PEER="${1:-192.168.127.2}"
REPS="${2:-2}"
shift 2 2>/dev/null
CFGS="${*:-asfound quiet noloops coal250 napi90 best}"

DUR=6
PORT=5201

# The fork/exec shell loops. Resolved by name so a reboot's new PIDs still hit.
# ptp4l/phc2sys are deliberately absent: stopping them would perturb gPTP.
LOOP_PATS="gptp2csr.sh stream_phc_sync.sh acmp-persist"

loop_pids() {
	for p in $LOOP_PATS; do pgrep -f "$p" 2>/dev/null; done | sort -u
}

# ---- as-found posture, captured before anything is touched --------------------
ORIG_PRINTK=$(cut -f1 /proc/sys/kernel/printk 2>/dev/null)
ORIG_USECS=$(ethtool -c eth0 2>/dev/null | awk '/^rx-usecs:/{print $2}')
NAPI_PIDS=$(pgrep -f 'napi/eth' 2>/dev/null | tr '\n' ' ')
ORIG_NAPI=$(for p in $NAPI_PIDS; do chrt -p "$p" 2>/dev/null | awk '/priority/{print $NF}'; done | head -1)
[ -n "$ORIG_PRINTK" ] || ORIG_PRINTK=7
[ -n "$ORIG_USECS" ] || ORIG_USECS=5000
[ -n "$ORIG_NAPI" ] || ORIG_NAPI=50

restore() {
	for p in $(loop_pids); do kill -CONT "$p" 2>/dev/null; done
	dmesg -n "$ORIG_PRINTK" 2>/dev/null
	ethtool -C eth0 rx-usecs "$ORIG_USECS" 2>/dev/null
	for p in $NAPI_PIDS; do chrt -f -p "$ORIG_NAPI" "$p" 2>/dev/null; done
}
trap restore EXIT INT TERM HUP

apply() {
	# start from as-found every time so configs never leak into each other
	for p in $(loop_pids); do kill -CONT "$p" 2>/dev/null; done
	dmesg -n "$ORIG_PRINTK" 2>/dev/null
	ethtool -C eth0 rx-usecs "$ORIG_USECS" 2>/dev/null
	for p in $NAPI_PIDS; do chrt -f -p "$ORIG_NAPI" "$p" 2>/dev/null; done
	case "$1" in
	asfound) : ;;
	quiet)   dmesg -n 1 2>/dev/null ;;
	noloops) for p in $(loop_pids); do kill -STOP "$p" 2>/dev/null; done ;;
	coal250) ethtool -C eth0 rx-usecs 250 2>/dev/null ;;
	napi90)  for p in $NAPI_PIDS; do chrt -f -p 90 "$p" 2>/dev/null; done ;;
	best)    dmesg -n 1 2>/dev/null
	         for p in $(loop_pids); do kill -STOP "$p" 2>/dev/null; done
	         ethtool -C eth0 rx-usecs 250 2>/dev/null ;;
	esac
	sleep 1
}

# median of stdin (numeric, one per line)
median() { sort -n | awk '{a[NR]=$1} END{ if(NR==0){print "0"} else print a[int((NR+1)/2)] }'; }

# one iperf3 run -> "Mbit/s idle_pct". $1 = "-R" for RX (peer->board) or "".
run_one() {
	u0=$(cut -d' ' -f1 /proc/uptime); i0=$(cut -d' ' -f2 /proc/uptime)
	bw=$(iperf3 -c "$PEER" -p "$PORT" -t "$DUR" $1 2>/dev/null \
	     | awk '/receiver/{print $7}')
	u1=$(cut -d' ' -f1 /proc/uptime); i1=$(cut -d' ' -f2 /proc/uptime)
	[ -n "$bw" ] || bw=0
	echo "$bw $(awk -v a="$u0" -v b="$u1" -v c="$i0" -v d="$i1" \
	      'BEGIN{w=b-a; printf "%.0f", (w>0)?(d-c)*100/w:0}')"
}

printf '%-9s %10s %10s %8s\n' CONFIG 'RX Mbit/s' 'TX Mbit/s' 'idle%'
printf '%-9s %10s %10s %8s\n' --------- ---------- ---------- --------
for cfg in $CFGS; do
	apply "$cfg"
	rxf=/tmp/.ab_rx.$$; txf=/tmp/.ab_tx.$$; idf=/tmp/.ab_id.$$
	: > "$rxf"; : > "$txf"; : > "$idf"
	n=0
	while [ "$n" -lt "$REPS" ]; do
		set -- $(run_one -R); echo "$1" >> "$rxf"; echo "$2" >> "$idf"
		set -- $(run_one);   echo "$1" >> "$txf"
		n=$((n + 1))
	done
	printf '%-9s %10s %10s %8s\n' "$cfg" \
	       "$(median < "$rxf")" "$(median < "$txf")" "$(median < "$idf")"
	rm -f "$rxf" "$txf" "$idf"
done
restore
trap - EXIT INT TERM HUP
echo "[as-found posture restored: printk=$ORIG_PRINTK rx-usecs=$ORIG_USECS napi=$ORIG_NAPI, loops running]"
