# [A194] handoff: issue #504 / PR #521, overlap last-byte control

- Head: `4876423d4cf8e89b820c56f8339f230abefb4827`
- Tree: `b2fb9e0516aa4ed9a17cdedfb1ae25460270d408`
- Parent: `97aa1ec943ac740a27b942210a248f6512ae3ff6`, the head R227-3 and R228-3 reviewed
- Branch: `504-hosted-rv32-compiler`. Committed locally and NOT pushed, by instruction.
- Commit subject, one line with no trailers: `builder: control the store census overlap at a modelled word's last byte`

## Finding answered

This commit answers R227-3 MINOR Tests and R228-F6 MINOR Tests, which are the same finding.
`sw/builder/test_builder.py` `_rv32_forget_overlap` has the low boundary
`key[-1] + 3 >= start`, and no control failed when it was reverted to `>`.

## Change (tests only: `sw/builder/test_builder.py`, +20/-7)

All four probes go into the existing literal resolver control set in
`test_baremetal_profile_contract`.

- **`stale_probes`, the negative arm.** Two new probes. Each must leave the next store unplaced.
  - "a byte store at a frame slot's last byte": `sw a5,-20(s0)`, `sb zero,-17(s0)`, then `lw a4,-20(s0)`.
  - "a byte store at a static word's last byte": `sw a5,0(a3)`, `sb zero,3(a3)`, then `lw a4,0(a3)`.
- **`kept_probes`, the positive arm.** Two new probes. Each must leave the parked word placed at `0x80001000`.
  - "a byte store one past a frame slot's last byte": `sb zero,-16(s0)`.
  - "a byte store one past a static word's last byte": `sb zero,4(a3)`.
  - Together with the negative arm, these pin the boundary from both sides.
- **The comments and the printed `store_classes_note`** name the new shape. The counts are still computed: 15 stale probes and 5 kept probes.

The commit makes no production, docs, workflow or ratchet change. The page's sentence at
`docs/integration/BAREMETAL_FIRMWARE.md:494-496`, "the rewrites above, each against a whole-word
positive arm", already covers the footprint-overlap rewrites. It needed no edit.

## Mutation evidence

Script: `scripts/a194_mutate.py`.

- Each probe runs in a disposable copy of the committed lane tree, with no `.git`.
- Each edit is an exact-string edit, asserted to apply exactly once.
- The gate runs through `sw/builder/test_firmware_compiler.py`.
- Without `--full`, a stop marker is planted right after the stale and kept loops. Reaching it means every literal resolver control up to that point passed.
- The verdict is read from the gate's own assertion sentence.
- Receipts: `receipts/mutants/<id>.{json,log}`.
- The unmutated `test_builder.py` has SHA256 `daee153a…d71`.

| Probe | Edit | Result |
|---|---|---|
| M0-none | none (stop marker only) | reaches the stop marker: every literal control passes at head |
| M1-overlap-last-byte | `key[-1] + 3 >= start` -> `key[-1] + 3 > start` | **KILLED**: "after a byte store at a frame slot's last byte the RV32 resolver still placed the next store ([2147487744])", which is 0x80001000 |
| M1s (static probe alone) | M1 plus the new frame probe deleted | **KILLED**: "after a byte store at a static word's last byte ... still placed the next store" |
| M1x (the finding reproduced) | M1 plus both new stale probes deleted | reaches the stop marker: without the new probes the revert survives, as R227-3 and R228-3 reported |
| M2-overlap-over-forget | `+ 3 >= start` -> `+ 4 >= start` | **KILLED**: "after a byte store one past a frame slot's last byte ... reported the next store as [unplaced(None)]" |
| M2s (static positive arm alone) | M2 plus the new frame kept probe deleted | **KILLED** on the static kept-probe sentence |
| M1 through the complete gate, SDK mapped | M1, no stop marker, `--sdk-destination` | exit 1, **KILLED** on the M1 sentence |
| M1 through the complete gate, absent | M1, no stop marker, `--absent` | exit 1, **KILLED** on the M1 sentence |

## Gate exits at head `4876423d`, run in the lane worktree

Every run used `python3 -B -u` with Python 3.14.7.

| Command | Exit | Result | Receipt |
|---|---|---|---|
| `sw/builder/test_firmware_compiler.py --sdk-destination $VALIDATION_STORAGE/504-manager-r1/sdk-install --audit …` | 0 (366 s) | GATE 1b PASS. 217/217, 17/17 and 4/4, 46/46. 0 NOT RUN, 235 compiles. 242 audited invocations with 0 argv tails changed. All 120 census assemblies are `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`. It printed "15 rewrites of a parked word … while 5 stores … left exactly theirs" | `receipts/head-gate1b-sdk.{log,exit,head}` |
| `sw/builder/test_firmware_compiler.py --absent --audit …` | 0 (301 s) | GATE 1b PASS. 182/182, 17/17 and 4/4, 46/46. 1 NOT RUN (the compiled census), 0 compiles | `receipts/head-gate1b-absent.{log,exit,head}` |
| `sw/builder/test_firmware_compiler.py --selftest` | 0 (2 s) | compiler audit self-test PASS | `receipts/firmware-compiler-selftest.{log,exit}` |
| `scripts/a194_mutate.py` (8 probes) | 0 | 8/8 as expected | `receipts/mutants/` |

- **The SDK was mapped read-only.** A path, size, mtime and mode listing of the SDK tree hashed the same before and after the run.
- **The lane was left clean.** After the runs, `git status --short --ignored` is empty.

## Limits

- **Verilator.** The 46 RTL variants elaborated with the system Verilator 5.052 (`/usr/bin/verilator`), not the pinned 5.050. The change touches no RTL path.
- **Scope of the runs.** Not run, by instruction:
  - the whole `test_builder.py` bank, and the other banks;
  - act, and any hosted job.
  - `test_builder.py` has no separate selftest flag. Its resolver controls run inside `test_baremetal_profile_contract`, which is gate 1b. Gate 1b ran in both modes, together with the gate runner's `--selftest`.
- **The reviewers' compiled plants were not repeated.** These are the byte-3 union plants, and they are reviewer tooling. Both reports said a literal control suffices. The commit changes no production code, so the head's refusals of those plants are unchanged.
- **Optional suggestions not taken.** These are the companion boundary `key[-1] <= start + width - 1` (R228-S8 and R227-3-S1 M16) and R227-3-S1 M17. They remain optional suggestions.

## Next

- **R227 and R228** re-review head `4876423d` once it is pushed. The push is the manager's duty.

## Published

- The REVIEW READY comment is on issue #504: https://github.com/kebag-logic/milan-fpga/issues/504#issuecomment-5794053679
