# Reviewer scripts and commands (round R712-3)

`CLONE` is a detached clone at `4f58214f457e963243a1fe6b86c6af161e97f26f`; `PACKET` is this directory's parent.
The pinned Verilator 5.050 wrapper is linked as `$PACKET/scratch/bin/verilator` and put first on `PATH` by `bg.sh`.
`V` is the LiteX environment's Python (`$HOME/litex-milan/venv/bin/python3`).

| Script | Purpose |
|---|---|
| `verify_packet.py <evidence dir>` | Hashes every file of the round 13 author packet against `MANIFEST.json` and `receipts/INDEX.md`; lists hash-only receipts. Run on `git archive b7d1afef review-evidence/665s2b-r1/author-r13 review-evidence/665s2b-r1/MANIFEST.json`. |
| `check_estimate.py <SPLIT_CONTROL_MEMORY.md>` | Recomputes section 14's U, L and S columns (S both from the printed 1x1 column and from arm A's 1x1 figure) and the gPTP additions. |
| `plant.py <copy> <name>` | Plants one reviewer mutant in a disposable copy: `step-beside-input`, `both-builds`, `room-is-deadline`. |
| `bg.sh NAME CMD...` | Runs a command detached with its log and rc in `receipts/`. |
| `redact.py <dir> <path>=<placeholder>...` | Replaces host paths in receipts. |

Commands (each its own log and rc under `receipts/`):

```sh
bg.sh fw_gate python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --lwsrp third_party/lwSRP --jobs 4 --build-dir $PACKET/scratch/fw
bg.sh nvm_gate python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
bg.sh harness_selftest python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
bg.sh h8_save $V -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $PACKET/scratch/h8 \
  --groups 'backlog-adp,backlog-adp@blank-7,backlog-adp@program-3,backlog-adp@verify-1,save' --jobs 5 \
  --record-budget-findings --record-share-findings
bg.sh boot_1x1 sh -c "$V -B tb/verilator/ctrl_split_boot/run.py --build-dir $PACKET/scratch/boot1 && \
  $V -B tb/verilator/ctrl_split_boot/run.py --build-dir $PACKET/scratch/boot1 --self-test"
bg.sh boot_selftest_seed0 env PYTHONHASHSEED=0 $V -B tb/verilator/ctrl_split_boot/run.py --build-dir $PACKET/scratch/boot1s --self-test
# reviewer plants, each in its own copy of the clone (cp -a), then:
plant.py $PACKET/scratch/m1 step-beside-input   # then the firmware gate in m1 (plant_step_beside_input)
plant.py $PACKET/scratch/m2 both-builds         # then the firmware gate in m2 (plant_both_builds)
plant.py $PACKET/scratch/m3 room-is-deadline    # then the store gate in m3 (plant_room_is_deadline)
```
