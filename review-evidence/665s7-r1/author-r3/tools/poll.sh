#!/usr/bin/env bash
# poll.sh SECONDS: wait SECONDS (or until the sweep launcher logs), then one compact status line per running thing
S=/data-2/milan/tmp/665s7-a757c; T=$MANAGEMENT/2026-09-23/665s7-a757c/tools
python3 -c "import time; time.sleep(float('$1'))"
echo "launcher: $(grep -c 'shard .* on' $S/sweep-launcher.log) launched; $(tail -n 1 $S/sweep-launcher.log | cut -c1-120)"
echo "gates: $(tail -n 1 $S/gates/gates.out)"
for n in 1 2 3 4; do [ -f $S/ci/local-r$n.out ] && echo "runner $n: $(grep 'local:' $S/ci/local-r$n.out | tail -1)"; done
echo "replay results: $(ls $S/ci/2128daad26b9/jobs/*/result.json | wc -l) of 69; failures: $(grep -l '"result": "failure"' $S/ci/2128daad26b9/jobs/*/result.json 2>/dev/null | xargs -r -n1 dirname | xargs -r -n1 basename | tr '\n' ' ')"
for k in 0 1 2 3; do u=milan-a757c-shard$k; [ -d $S/sweep/shard-$k ] && echo "shard $k: $(systemctl --user show $u -p ActiveState --value) $(ls $S/sweep/shard-$k/logs 2>/dev/null | wc -l) logs"; done
echo "mem: $(tail -n 1 $S/memlog.txt); peak since restart $(awk '$1>"18:00"' $S/memlog.txt | sort -k3 -n -r | head -1)"
