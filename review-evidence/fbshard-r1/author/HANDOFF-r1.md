# HANDOFF r1: #980 firmware-boundary shards ([A827])

**Status:** REVIEW READY at `b7b351935f65416c8632c21dd13e08fb2e9c1d9c`. Three local commits on `pf-fbshard-1`, base `dev-soft-core` `854bd7236`. Not pushed.
**ETA:** the code is done. What remains is the manager's push and PR, then one hosted `rtl-fast` run on the PR head for the per-shard hosted times (about 14 minutes of wall time), then review.

**Posted on #980:**
- [A827] TAKEN: https://github.com/kebag-logic/milan-fpga/issues/980#issuecomment-7093891351
- [A827] REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/980#issuecomment-7096297282

## Commits

```
b7b351935 Document the firmware-boundary shards, their judging aggregate and their measured times on the CI workflows page (#980)
1ea1205d8 Read the boundary shards' table when their plan is checked, so a planted table reaches the check (#980)
d7da99cf6 Shard the firmware-boundary builds into three capture jobs judged as one by an aggregate that requires every unit of the compile set exactly once (#980)
```

11 files changed, +662/-98 (`receipts/diffstat.txt`).

## Design in one paragraph

The `--without verilator` compile set has 8 units: one per builder run, with the control gate cut into `--build-part 0/2` and `1/2`. `ctrl_configs.SHARDS` assigns them to 3 shards. Each `firmware-boundary shard k/3` job builds its units under its own capture and judges nothing, then uploads that capture's records, manifest and texts. `firmware-boundary` keeps its name and needs every shard. It downloads the three captures and runs `--shards 3 --capture ...`, which requires each unit's run exactly once. It then judges the union as one capture, with the self-test and all controls run once. A failed shard skips it, and `rtl-fast` also requires the shards' result. The workflow is generated: the template changed and was regenerated. `ci_events.py` records the new jobs.

## Measured (local, shared host, four builder jobs each)

- **Shards** at `d7da99cf`: **462 s / 393 s / 449 s**.
- **Judging run** over upload-shaped captures: 259 s, and 250 s at the head.
- **Unsharded builds** at `854bd723`: control gate 714 s, coverage gate 378 s, store 96 s, RV32 self-test 9 s. That is 1.19 times hosted run 45071981993, whose step took 1273 s.
- **Projection:** about 8 minutes per hosted shard job, about 5 for the judging job. Every job is well under 15.
- **Unsharded run not timed end to end locally.** It runs about 25 minutes here, longer than one foreground command can take. The run at the base also stopped at `test_ctrl_memory.py` for lack of `migen` in the default Python. Its build phases above are measured, and the judging phase is measured separately.

## Proofs and plants

- **Unit union:** all 8 units once across the 3 captures.
- **Source union:** the whole control-gate build and its two parts give 1262 = 1262 distinct compiles, 0 missing, 0 extra.
- **Dropped shard capture:** rc 2, refused by name.
- **Duplicated shard capture:** rc 2, refused by name.
- **Table with a unit dropped or duplicated:** rc 2, refused by name before building.
- **Self-test:** 4 shard controls `[ok]`.
- **`--build-part`:** a dropped suite and a duplicated suite are both refused.
- **Gates:** 28 CI and docs gates at the head, all rc 0. `ci_events --selftest` passes.

Receipts: `receipts/INDEX.md`.

## For the manager and the reviewer

1. **Push and open the PR.** Push `pf-fbshard-1` and open the PR against `dev-soft-core` with `PR-BODY.md`.
2. **Run the act replica.** Per AGENTS.md section 5, run it from a trusted clean `dev` worktree once the PR head exists: `python3 -I <trusted>/scripts/act_ci.py --pr <N> --cpu-ranges ...`. I did not run it; there was no PR head.
3. **Record the hosted run.** On the first hosted `rtl-fast` run, record each `firmware-boundary shard k/3` job time and the `firmware-boundary` time on #980. That is acceptance item 3, still open.
4. **Issue bookkeeping.** The Issue still needs a named independent reviewer and its Project state (AGENTS.md section 5). I did not set them.
5. **Known gaps** (also in the REVIEW READY comment):
   - The artifact round trip has only been emulated locally.
   - `ci/image/*.json` inventories were not regenerated. They need the image's pinned `shfmt`, and no hosted job checks them.
   - Runner minutes go up, while the critical path goes down.

REVIEW READY b7b351935f65416c8632c21dd13e08fb2e9c1d9c
