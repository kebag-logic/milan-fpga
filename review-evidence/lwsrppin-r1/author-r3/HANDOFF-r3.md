# HANDOFF r3: [A834] lane lwsrppin, sync round (merge dev-soft-core 2509db68 into the lwSRP d1bb4f4e pin)

Status (14:30 CET 2026-11-24): **DONE, review ready.** The merge commit
`507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` is on `20-lwsrp-pin-d1bb4f4`, local and **not pushed**. Every gate the
brief names passes at that head. The images changed, so the routed 8x8/1if merge condition was re-shown, and it is
met: LUT -24 against `2509db68`, and the #818 floor is met at every corner on the first directive. Nothing of this lane
is running.
ETA: none. The next step is the manager's push.

Outputs: `REVIEW-READY.md` (the merge, its conflicts and resolutions, every gate), `receipts/INDEX.md` (128 files,
all text and under 200 KB, no .gz).

## Brief items

| # | Item | Outcome |
|---|---|---|
| 1 | Fetch and merge dev-soft-core | Done. FETCH_HEAD `2509db68`, `git merge --no-ff`. Two files conflicted. `srp_arms.py`: both new functions kept, `own_leaveall_arms`, then the train's `LINK_PASS` and `link_pass_arms`. `test_ctrl_firmware.py`: both `outcomes.extend` calls kept, and both docstring clauses kept, re-wrapped. The six automatically merged files the pin touches still name `d1bb4f4e` where the pin did, and the train's hunks are intact (144 of 145 train paths SAME; the 145th is the hand-resolved docstring). No figure in the conflicted text needed re-deriving |
| 2 | Gates at the merge head | Firmware gate 4 shards rc 0: 98 arms, 844 of 844 mutants, 398 and 664 `[ok]`. Inventory 2,005 live invocations in exactly one shard. srp_own_leaveall arms 44 of 44 at both points, worst 185 ms of 240. `make twin` 0 findings, self-test OK (11). Plants 16 of 16 refused twice, 32 refusals per run. kept_grade self-test PASS (32). ctrl_boundary `--require-rv32 --selftest` PASS (117/192/4 controls, 0 misbehaved). plat_ledger PASS both sides, controls 9 of 9. docs.yml 46 of 46 steps rc 0, both builder legs included |
| 2 | Image ledgers | Changed. Against `2509db68`: only lwSRP `mrp_mad.o` changes, +60 B `.text` in every image (ROM +56/+56/+64/+64); tiles, SRAM and `ctrl_plat` are unchanged. Against `30796098`: the train's content (ROM +976/+1,160/+2,312/+2,488; RAMB36 45 -> 45.5, 46 -> 46.5, 58.5 -> 59.5, 63 -> 64.5; the 8x8 AEM image changes); plat_ledger accepts every point |
| 2 | Routed 8x8/1if | Re-shown, through `vivado-slot.sh`, 2 Vivado runs at once, MemAvailable 61 GB. Merge 45,958 LUT / 53,337 FF against base 45,982 / 53,337: **-24 LUT**, 0 FF. Tiles 98.5 at both. Worst WNS +0.038 (base +0.035), WHS +0.036 (base +0.036). 0 failing endpoints, 0 routing errors, 0 CRITICAL WARNING |

## Notes for the manager

1. **ctrl_boundary's first run was REFUSED by the environment, not by the head.** `tb/verilator/mbx`'s
   `dma-mutants` exited 2. `dma_mutants.py` runs `make -s -C … print-dma-vflags` and executes what it prints. Under
   the capture's outer `make -C`, GNU make 4.3 (first on this lane's PATH) still prints "make[1]: Entering directory",
   so the script tried to execute that line. It was re-run as the other lanes' boundary runs do it
   (`MAKEFLAGS="-j8 --no-print-directory"`), and `make -C tb/verilator/mbx` then exits 0 and the gate passes. Neither
   side touches `tb/verilator/mbx`. Observation, not in scope: the script depends on the make version and MAKEFLAGS.
   The first run's log is kept as `selftests/ctrl_boundary-run1-make43-refused.log`.
2. **A race of my own in the first `make twin`, no result taken.** The firmware gate shards rewrite
   `configs/generated/*/gen/adp_shape_defaults.svh` in place in the checkout (the content is unchanged afterwards and
   porcelain stays 0). A `make twin` running at the same time read an empty `ADP_STRIN0_FMT_C` and failed to compile
   (`-DTWIN_IN0_FMT=0xULL`). I stopped it and the plants run behind it. Twin, plants and docs were then run in the lane
   checkout only after the shards ended, and the boundary self-test ran in a separate worktree at the same commit.
   The aborted logs are in `twin/aborted-race/`. The shards also leave `dispatch-build/keys/` untracked in the
   checkout. That confirms round 1's unconfirmed note 5. I moved it to scratch, since the builder legs refuse
   untracked files.
3. **Re-review scope (AGENTS.md section 7).** The merge changes artifacts in the scope of `Tests`
   (`srp_arms.py`, `test_ctrl_firmware.py`), `Docs` (the gate docstring) and `RTL` (the embedded image and its route).
   A lens covered at `30796098` and touched by the merge must be covered again at `507bce7f`. The resolution is
   additive. `git diff 2509db68 507bce7f` is the pin's 18 paths, and `git diff 30796098 507bce7f` is the train's
   145 paths.
4. **Push, then CI.** Push `507bce7f` to `20-lwsrp-pin-d1bb4f4`. AGENTS.md section 5 then wants the act replica from a
   trusted dev worktree (`scripts/act_ci.py --pr 992`). It was not run, because nothing is pushed.
5. **Not re-run this round (not in the brief):** harness arm A and answering-every-port, the load and flip budget
   model, the OOC memory map, srptx, and the reproduction at `08ee86e8`. `sw/litex/test_ctrl_memory.py --build-only`
   ran inside the boundary capture.
6. **Commit.** The commit message is one line with no trailers, as CONTRIBUTING.md and the brief require. This
   repository has no hooks installed, so none was bypassed.
7. **Housekeeping.** The round-1 base worktree `/data-2/milan/tmp/lwsrppin-a834/base` is now detached at `2509db68`.
   The round-2 worktree `/data-2/milan/tmp/lwsrppin-r2` is detached at `507bce7f`; its branch `lwsrp-pin-r2` still
   points at `30796098`. Both hold ignored builder outputs from the route. Scratch to delete when done:
   `/data-2/milan/tmp/lwsrppin-a834/{route (0.9 GB), fw3 (1.4 GB), r3}`. To free disk at the start (97 % full), I
   deleted this lane's round-1 scratch (`harness`, `fw`, `docs-402834ac`) and the round-2 scratch, as the earlier
   handoffs allowed. The lane checkout holds ignored twin build trees.
8. No push, no comments, no bench or board access. Every command ran in the foreground, except the long gates (the
   shards, the routes, twin and plants, the boundary self-test and docs). Those ran detached with `setsid`, because
   the foreground cap is 10 minutes, and this session waited on each in foreground loops, as in rounds 1 and 2.

REVIEW READY 507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698
