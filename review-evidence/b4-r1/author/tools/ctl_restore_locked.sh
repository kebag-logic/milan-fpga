#!/usr/bin/env bash
# Put the controller NIC back as found, under the bench lock, after the timing run's
# slave-only gPTP daemon has exited: PHC frequency and trajectory (phc_restore_b4.py,
# lane B1's method) and hardware timestamping off (tx_type 0, rx_filter 0), as the
# start baseline read it. Checks first that no gPTP daemon runs. The gPTP profile is
# not touched.
# usage: ctl_restore_locked.sh <packet_dir>
# Endpoints come from the private file named by B4_ENV (not in this packet).
set -u
. "${B4_ENV:?}"
P=$1
timeout -k 5 150 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 30 scp -q "$P/tools/phc_restore_b4.py" "$CTL_HOST:/tmp/a468/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "if pgrep -a ptp4l; then echo DAEMON_RUNNING_NOT_RESTORED; exit 3; fi; \
  sudo -n $HWSTAMP_CTL -i $CTL_IFACE; cd /tmp/a468 && python3 -B phc_restore_b4.py $PHC_CTL $CTL_IFACE; echo PHC_RESTORE_RC=\$?; \
  sudo -n $HWSTAMP_CTL -i $CTL_IFACE -t 0 -r 0; echo HWSTAMP_SET_RC=\$?; sudo -n $HWSTAMP_CTL -i $CTL_IFACE; \
  sudo -n $PHC_CTL $CTL_IFACE freq cmp" > "$P/restore/r2-controller-restore.txt" 2>&1
echo "RESTORE_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P"
echo "LOCK_RC=$?"
