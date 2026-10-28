[R701] POSITIVE - exact head c3ba2b2647aee7fdfe220cac6634827cf5a47ec1

# R701-9: internal independent review, issue #665 / PR #795 (lane S1, merge round 2)

- **Head:** `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1`, tree `76dfd8d7b935592d82cc6851afe2ce682c29e08d`. The PR head on GitHub is the same; the base is `dev-soft-core` at `05439833`.
- **Scope:** the delta `614635b7..c3ba2b26`. That is the merge `c6ab3432` of `dev-soft-core` `05439833` (S2c, PR #796), then `8669b9f4` (R701-8-W2), `b198a2e1` (two README claims) and `c3ba2b26` (the ledgered plan moved into `build.build`). R701-8's POSITIVE at `614635b7` stands for the S1 content the delta does not touch.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR is open. One RESIDUE (wording only) and two optional SUGGESTIONs are recorded. R701-8-W1 and W2 are resolved at this head.
- **Not used:** private author material, lane scratchpads, management directories other than this packet, and other reviewers' reports. I read prior public findings only after my own pass over the diff.

## What the delta is, reconstructed

The assignment (issue #665, issuecomment-6474448163) has three items:

1. Merge `05439833` as a merge commit and keep both sides: S1's contract 2.3 hookup and 64-cycle acknowledgement, and S2c's fetch-L1 options and arms.
2. Apply R701-8-W1 and W2 as written.
3. Run the round-8 gates plus a real harness build at both points, arm A, one group, with the cache on.

### Merge checks

| Check | Method | Result |
|---|---|---|
| Merge shape | `git log --format='%H %P'` | `c6ab3432` has parents `614635b7` and `05439833`. Nothing is rebased. |
| Every file, by side (merge base `6660a1a0`) | `scripts/sides.sh` → `receipts/sides.txt` | 55 files changed on S1 only, 10 on S2c only, 11 on both. Every one-sided file equals its side at head (`one-sided-mismatch=0`). No file changed at head that neither side changed, and every file either side changed is changed at head. |
| What a person resolved | `git merge-tree --write-tree 614635b7 05439833`, diffed against `c6ab3432` → `receipts/merge-resolution.diff` | Five harness files conflicted: README, `build.py`, `selftest.py`, `selftest_mutants.py`, `split_soc.py`. Each hunk keeps both sides. `milan_soc.py`, `ctrl_configs.py`, `run.py` and three docs merged automatically, with no hand edit. `test_soc_options.py` was changed by S2c only and equals S2c's version. No conflict markers remain. |
| Mutant set | `scripts/count_mutants.py` → `receipts/mutant-union.txt` | Head's `MUTANTS` is exactly the union of both sides: 62 at the base, plus 6 from S1 and 8 from S2c, gives 76. |
| `milan_soc.py` auto-merge | Read both sides' hunks | S1 adds `ctrl_mailbox_face_ports` and its use in `CtrlMailbox` (`:2645-2747`). S2c adds `CTRL_FETCH_L1`, `ctrl_cpu_args` and the `if ctrl_mailbox:` cache arguments (`:2848-2936`). The hunks are disjoint and use no name the other side renamed. |
| Post-merge commits | `receipts/post-merge.diff` | README wording (`8669b9f4`, `b198a2e1`). Then `c3ba2b26`: `split_soc.build` drops its seventh parameter, and `build.build:560-561` holds the call under `split_soc.ledgered_plan(ledgered_point(...))`. `ctrl_memory.plan` is called in one place only on this path (`milan_soc.py:2807`, inside `add_ctrl_memory`), so widening the context from `add_ctrl_memory` to the whole `split_soc.build` does not change behaviour. `split_soc.build` has no other caller. |
| Gitlinks and hardware sources | `git ls-tree`, `git diff --stat -- hdl *.sv *.v sw/mailbox` | All six gitlinks are identical at `614635b7` and at head. No HDL, mailbox contract or firmware C changed in the delta. |

## Findings

### R701-9-W1 - RESIDUE - Docs - `tb/verilator/ctrl_service_budget/README.md:847`

- **Text:** "`as-built`: handed the SoC's regions, the cached CPU takes the same instruction access fault, cause 1, at the same call (`0x6880`). The cache does not change #791's decode."
- **Evidence:** The next line (`:848`, from `b198a2e1`) says that at this head the cached CPU is caught with cause 5. My own cached control at head gives `TRAP 195 0 5 00000020` (`receipts/asbuilt-split-1x1-head.log`). Line `:223` already scopes the section's figures to the firmware of `e76a755a`. Even so, the bullet's present tense ("takes") contradicts the line after it.
- **Impact:** Wording only. No figure, test or verdict changes.
- **Exact fix:** "`as-built`: handed the SoC's regions, the cached CPU took the same instruction access fault, cause 1, at the same call (`0x6880`), on the firmware of `e76a755a`. The cache does not change #791's decode."
- **Verification:** Read `:847-848` together.

### R701-9-S1 - SUGGESTION - Tests, Robustness - `tb/verilator/ctrl_service_budget/selftest.py:859`, `build.py:560`

- The portable self-test's `built()` fixture stubs `split_soc.ledgered_plan` as `contextlib.nullcontext()`. So it does not see whether `build.build` still holds the SoC build under the ledgered plan.
- My mutant drops that wrap (`receipts/mut-noledger.diff`). The self-test would still pass, but the real 8x8 build refuses it in 6 s: `allocation over budget: 57.5 RAMB36 ... exceeds the 56-RAMB36 budget`, rc 1 (`receipts/mut-noledger-8x8.log`).
- So the defect fails loudly on the only build that measures that point, and this is not a regression: at `614635b7` no portable check covered the hand-off either.
- **Optional:** have the stub record the name it is handed. Then require `8x8-two-interfaces` at 8x8 and `None` at 1x1, with a mutant that drops the wrap.

### R701-9-S2 - SUGGESTION - Docs - `tb/verilator/ctrl_service_budget/README.md:1022`

- The limit says the self-test's build check replaces the SoC export with a recorder. It could add that the ledgered plan is replaced with a no-op, so only the real 8x8 build attests the plan (see S1).

## Prior findings at this head

| Prior item | Disposition at `c3ba2b26` |
|---|---|
| **R701-8-W1** (RESIDUE; PR body, the `as-built` limitation) | **Resolved.** The live PR body (`receipts/prbody-snapshot.md:259`) carries the exact fix: "`lw` at 0x24, reading 0x197b0; ... the cause and the last committed PC (0x20 here ...)". |
| **R701-8-W2** (RESIDUE; README) | **Resolved.** `README.md:995` matches the exact fix word for word. My disassembly of this head's 1x1 image confirms `20: bgeu t1,t2` and `24: lw t3,0(t0)`, with `t0` = `_fdata_rom` 0x197b0 (`receipts/asbuilt-start-disasm.txt`). |
| R701-8-S1 (no standing check of `ack_deviations`, `mailbox_pins_missing`, the idle-input refusal) | **Carried**, optional. The resolution keeps these guards unchanged. At head both real builds pass the acknowledgement check, and the only PINMISSING lines are the CPU's `dma_bus_{ar,aw}region`, not mailbox pins. |
| R701-8-S2 (`build.py:115`, "an anchor is not unique") | **Carried**, unchanged. |
| R701-8-S3 (PR body, "neither changes a file they read") | **Resolved.** The PR body now reads "neither merge changes a file they read" (`:124`), and "read no file either merge or round 8 changes" (`:222`). |
| R701-7-S1 (`ctrl_configs.py:180`, "(#665 S1)" in a runtime string) | **Carried**, optional. The delta does not touch it. |
| R701-7-F1, R701-7-F2 and all earlier findings | **Remain resolved.** At head, the 8x8 point builds under its ledger (57.5 tiles, `ledgered: 8x8-two-interfaces`), and the face hookup and bound acknowledgement are intact (see Conformance). |
| Older SUGGESTIONs (R701-6, R701-5, R701-4, R702-6) | Carried, unchanged. The delta does not touch their causes. |

## Executable evidence

### My own runs

All runs were at exact head, with pinned Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050`, identity `Verilator 5.050 2026-07-01 rev v5.050`). Each log records the head and the tool.

| Run | Receipt | Result |
|---|---|---|
| Harness self-test | `receipts/harness-selftest.log` | 97 PASS, 76 mutants caught, 0 failures, rc 0 |
| `sw/builder/test_soc_options.py` | `receipts/test-soc-options.log` | PASS: 52 constructor and 18 CLI cases, 9 killed controls. The split cache test: the all-fabric CPU stays `--xlen=32`, and the split CPU adds exactly `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`. All 6 controls are killed (cache lost, cache leaked to the all-fabric CPU, LSU L1 added, larger, second way, smaller). |
| `scripts/check_py_idiom.py`, plus `--selftest` | `receipts/check-py-idiom*.log` | `too many parameters: 7 <= 7`, rc 0. Self-test 54 of 54. |
| `sw/litex/test_ctrl_memory.py` | `receipts/test-ctrl-memory.log` | 0 failures |
| Real build, 8x8/2if, arm A, `aecp`, cache on | `receipts/real-8x8-head.log`, `.table.md`, `.soc.json` | 39 of 39, 0 misses, rc 0. `fetch_l1 split`, `[64, 1]`, netlist `VexiiRiscvLitex_2c4bb987...`, plan 57.5 with `ledgered: 8x8-two-interfaces`. `table.md` is **byte-identical** to the author's `runs/A8`. |
| Real build, 1x1/1if, arm A, `aecp`, cache on | `receipts/real-1x1-head.log`, `.table.md` | 25 of 25, 0 misses, rc 0. `table.md` is **byte-identical** to the author's `runs/A1`. |
| `as-built` control, 1x1, cache on | `receipts/asbuilt-split-1x1-head.log` | `TRAP 195 0 5 00000020`, `CONTROL as-built caught`, rc 0 |
| Mutant: `build.build` without the ledgered plan, 8x8 | `receipts/mut-noledger.diff`, `mut-noledger-8x8.log` | Refused at the plan, over budget, rc 1. The clone was restored afterwards. |
| Arm B (`answering-ports`, `aecp-fanout`, cacheless), 1x1 and 8x8 | `receipts/armB-fanout-*-none.log`, `B1/B8.table.md` | 1x1: 4 of 14 miss T_svc. 8x8: 22 of 22 miss, 4 of them over the 24 ms ceiling. Both rc 0. This equals the PR body's carried figures. |
| `slow-adp-rx` control, 1x1, cacheless | `receipts/slow-adp-rx-1x1-none.log`, `SA1.table.md` | `control.discover.if0` 24.614 ms, `CONTROL slow-adp-rx caught`, rc 0. Equals the carried figure. |
| Docs gates | `receipts/docs-gates.txt` | `check_doc_paths`, `check_doc_style`, `check_em_dash --base 05439833` and `--base 614635b7`, `docs_check`, `check_hygiene --check`, `check_baremetal_only --check`, `check_cpp_idiom`, `check_sh_idiom`: all rc 0. `git diff --check 614635b7 c3ba2b26` is clean. |

### Published evidence verified

- **Evidence tree:** `d972e10a84602bcd18c2c55349eb5dcf92a29c95`, `review-evidence/665s1-r1/author-r9`.
- **Signatures:** the evidence commit and the PR head are both unsigned (GitHub `verification.reason = unsigned`), so integrity rests on the evidence tree's `MANIFEST.json`.
- **Spot check:** I downloaded 95 files: `runs/*`, merge checks, gate receipts, image plans, comparisons and probes. Every one matches its git blob id and its `published_sha256` in `MANIFEST.json` (2,248 entries), with 0 mismatched and 0 unlisted (`receipts/evidence-manifest-check.txt`). I did not open `HANDOFF.md`.
- **Author's runs:** `runs/A1` and `runs/A8` record `HEAD c3ba2b26 DIRTY 0` and rc 0, and their `soc.json` carries the cache arguments. `runs/C-asbuilt-{none,split}` carry `TRAP 166 0 5 00000020` and `TRAP 195 0 5 00000020`. The `-8669b9f4` copies are marked superseded.
- **Author's gate receipts:** `merge-checks.txt` agrees with my side classification. `idiom-params-by-revision.txt` shows the merge commit at 7 parameters and head at 6, which is why `c3ba2b26` exists.

### Hosted runs

Exact-head hosted runs were in progress when I checked (`receipts/hosted-checks.txt`): 14 success, 1 skipped, 30 queued or in progress (the Verilator and Yosys shards among them). I make no claim about their outcome. Hosted and act acceptance is the manager's.

## Lens results

```text
[R701] PASS Conformance - assignment issuecomment-6474448163 items 1-3; c6ab3432 parents; receipts/sides.txt, merge-resolution.diff, mutant-union.txt; split_soc.py:423-467 (ack_deviations before export, ledgered_plan); build.py:134-143,560-561; milan_soc.py:2645-2747,2848-2936; README.md:995; PR body :259; receipts/real-{1x1,8x8}-head.* - item 1: a merge commit, every one-sided file equals its side, every conflict hunk keeps both sides; the acknowledgement check passes and AECP opens (it opens only on an acknowledged commit), so the 64-cycle bound and the face hookup are live at head; the fetch-L1 options and arms are intact, and the option test pins the exact arguments. Item 2: W1 and W2 match their exact fixes. Item 3: both real builds, cache on, reach the measurement, and my tables are byte-identical to the author's.
[R701] PASS RTL - receipts/real-8x8-head.soc.json (vexii_args, fetch_l1_geometry, ctrl_plan), the H8 verilate log's PINMISSING lines, git ls-tree gitlinks, git diff --stat -- hdl *.sv *.v sw/mailbox - no HDL, mailbox contract or submodule changed. The merged SoC instantiates the split CPU with S2c's 64x1 fetch L1 and S1's face ports. The only unconnected pins are the CPU's dma_bus_{ar,aw}region, not mailbox ports. The SoC plan is the ledgered 57.5 at 8x8 and 37.0 at 1x1, naming none.
[R701] PASS Robustness - build.py:560-561, split_soc.py:423-430, ctrl_memory.py:213-221; receipts/mut-noledger-8x8.log; the author's images/*.plan*.txt receipts - the ledger is named at 8x8/2if only; with the wrap removed, the 8x8 build refuses at the plan (rc 1); the planner refuses the override on any image that lacks the point's symbols; the XIP arm hands the rom image to the same plan, so an XIP build at a ledgered point fails loudly rather than mismeasuring. One optional hardening is S1.
[R701] PASS Tests - receipts/harness-selftest.log (97/76/0), test-soc-options.log, check-py-idiom*.log, test-ctrl-memory.log, mutant-union.txt, mut-noledger-8x8.log, armB-fanout-*-none.log, slow-adp-rx-1x1-none.log; selftest.py:845-860,915 - checks() runs build_checks, cache_checks and cache_build_checks; the run.main stub matches split_soc.build's six parameters; every mutant is caught; the option test's six controls are killed; the carried cacheless arm B and slow-adp-rx figures reproduce on the merged harness. The portable self-test cannot see the ledgered-plan hand-off (S1), but the real build does.
[R701] PASS Docs - README.md:45,54,114,223,847-848,995,1011-1012,1022; PR body (receipts/prbody-snapshot.md) :16-62,:222-259; receipts/docs-gates.txt - the README and PR body match the code and my runs: the firmware scope of each figure (S2c's figures were measured on e76a755a's firmware; e76a755a..05439833 changes no compiled firmware source, only ctrl_configs.py and a gtest README), the cacheless-only acknowledgement comparison, and the cached as-built result. The disclosure that arm B and slow-adp-rx were not re-run is accurate, and my runs reproduce those figures. No new source comment in the human-authored delta carries a lane label, review round, reviewer ID or comment ID. One wording slip is RESIDUE (W1). The lens stays clean under the owner rule.
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge parents and side classification, resolution diff, `split_soc.py`, `build.py`, `milan_soc.py`, README `:995`, PR body `:259`, real builds at both points | R701-9 | `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1` |
| RTL | CLEAN | soc.json and verilate logs from my 8x8 build, gitlinks, HDL and mailbox stat | R701-9 | `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1` |
| Robustness | CLEAN (S1 optional) | ledgered-plan move, the plan's refusal, the no-ledger mutant at 8x8 | R701-9 | `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1` |
| Tests | CLEAN (S1 optional) | harness self-test, option test, idiom gate, memory test, mutant union, arm B and controls re-run | R701-9 | `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1` |
| Docs | CLEAN (W1 RESIDUE, S2 optional) | harness README, PR body, docs gates | R701-9 | `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1` |

## Real limits

- **Hardware:** no physical calibration and no Vivado run. Field skips are not hardware proof.
- **Not re-run at this head (by me or the author):** arm B, `slow-adp-rx` and `slow-adp-shutdown` on the split's cache, the full group set at either point, and the one-cycle acknowledgement comparison on the cache. I re-ran arm B (`aecp-fanout`) and `slow-adp-rx` on the cacheless core only.
- **Not reproduced:** I did not run the four-shard Verilator sweep, the firmware self-test shards, coverage, `ctrl_boundary`, behave or `test_builder.py`. For those, this round relies on the author's published receipts, which I verified against the manifest and spot-checked rather than re-ran.
- **Hosted runs:** in progress at the time of review; no outcome is claimed.
- **Manager bank:** no manager source bank exists at this head, and none is inferred.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `e76a755a`, live dev `5fcec84b1aa72c43048eff28bb63a982add830dd`) with the builder and native banks, and link its receipts.
- Own hosted and act acceptance of the exact head: `rtl-fast`, `verilator-suites` and `yosys-portability`.
- Carry R701-9-W1 to the residue checklist. S1, S2 and the carried suggestions are optional.
- Obtain the second, external positive review that CONTRIBUTING requires.
- Obtain maintainer authorization before any merge.

R701-9 FINISHED
