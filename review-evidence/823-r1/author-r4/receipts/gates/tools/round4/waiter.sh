#!/usr/bin/env bash
# waiter.sh: start each pending job of this round in its own unit, on a range cpu_ranges.py picks, one at a time.
set -u
H=30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14
S=<scratch>; T=$S/gates/tools
PICK=<management>/2026-09-23/cpu_ranges.py
launch() {  # launch <unit suffix> <command string>
  local r
  until r=$(python3 $PICK pick 2>/dev/null); do sleep 60; done
  echo "$(date +%T) $1 on $r"
  systemd-run --user --unit=milan-823-a753d-$1 --collect --property=MemoryMax=10G --setenv=HOME=<home> \
    --setenv=PATH=<home>/.local/bin:/usr/local/bin:/usr/bin:/bin /usr/bin/taskset -c "$r" /bin/bash -c "$2"
  sleep 30
}
launch gates-c "bash $T/drive.sh $H $S/gates/final $T/r4-c.txt > $S/drive-c.log 2>&1"
launch ctrlnvm "bash $T/extra_gate.sh $H ctrl_nvm_selftest python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8"
launch twin "bash $T/extra_gate.sh $H twin bash -c 'make -j8 -C tb/verilator/milan_dp twin && make -j8 -C tb/verilator/milan_dp twin-plants'"
echo "$(date +%T) all launched"
