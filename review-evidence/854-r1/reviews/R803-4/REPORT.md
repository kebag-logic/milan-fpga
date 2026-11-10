[R803] POSITIVE - exact head b5d17214f811b48836ecc0cac5adb361454ccfd5

# Internal review R803-4: issue #854 / PR #862 (delta: the dev merge)

- **Head reviewed:** `b5d17214f811b48836ecc0cac5adb361454ccfd5`, tree `abad3b6f8c588e0c93fa707d4692c28c6652aefd`. This is the merge of `dev` `123f57a922bf07476cd69f91867f3b6f07080804` (#825, the generated register reference) into `a853461dd57f8e493ca079e0faa1f07229c3cb16`.
- **Prior head:** R803-3 and R804-3 were POSITIVE at `a853461d`. Those verdicts stand for everything this delta does not touch.
- **Source base:** `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`. When I started, `dev` was `123f57a9`.
- **The head has moved.** During this review the PR head moved to `9405010ff5def3275eecda7271a4b1ccc1aa2be0` (pushed 05:57Z). That commit merges `dev` `45c0b56c` (#835) and touches four docs files (`receipts/ls-remote-at-check.txt`, `receipts/new-head-9405010f.txt`). This round does **not** cover it. See "Limits and pending manager duties".

## Verdict basis

**POSITIVE at `b5d17214`.** I found no BLOCKER, MAJOR or MINOR, and one RESIDUE (R803-4-R1).

The merge's own claims hold:
- **Hand resolution:** only three files were resolved by hand. Each differs from `dev` by one line.
- **Generated page:** `REGISTER_MAP.md` equals the generator's output.
- **Wording:** the new text matches the RTL at this head.
- **Gates:** `docs_inventory.py --check` returns 0, and so does `git diff --check`, against both `dev` and `a853461d`.
- **`pp_shadow` suite:** passes at this head (317 checks, 0 failures), as does `drops-mutant` (8 of 8 arms killed, both clean controls pass).

## Check 1: the hand-made lines

I saved `git diff 123f57a9 b5d17214 -- docs/reference scripts/register_descriptions.json docs/design/CSR_REGISTER_NOTES.md` as `receipts/diff-dev-head-resolution.patch`. It holds three one-line changes and nothing else:

- **`scripts/register_descriptions.json:3919`:** `PP_RX_DROPS` changes from "Control frames lost to a full ingress FIFO." to "Control frames lost to a full ingress FIFO, or longer than the FIFO; saturates at 255."
- **`docs/design/CSR_REGISTER_NOTES.md:1243`:** one sentence is appended to the "Why an RX drop counter exists here at all" paragraph. A normalised search finds it byte-identical to the sentence the PR added to `a853461d:docs/reference/REGISTER_MAP.md` (`receipts/wording-and-integrity.txt`).
- **`docs/reference/REGISTER_MAP.md:4416`:** the generated `PP_RX_DROPS` row. It follows from the JSON line.

No source comment in these lines shows a lane label, round, reviewer ID or comment ID. The only ID is `#854`, which the comment rule allows.

## Check 2: every other path is one side's, unchanged

`scripts/classify_merge.py` compares each path's mode and object id across the head, `a853461d`, `123f57a9` and `ac0a01e3`. I did not rely on the merge note for this. Results (`receipts/merge-classification.txt`):

- **1,452** paths are identical in all four trees.
- **264** are `dev` changes taken unchanged.
- **14** are this PR's changes, taken unchanged.
- **3** were hand-made: the files in check 1.
- **0** paths dropped one side's change.

Related results:
- `a853461d..b5d17214` changes 267 paths. `ac0a01e3..123f57a9` also changes 267, and the two sets of paths are the same (`receipts/diff-*.name-status.txt`).
- The six gitlinks equal `dev`'s, and the submodule checkouts match them.

**`REGISTER_MAP.md` is regenerated, not hand-edited.** `gen_register_reference.py --check` returns 0, with `wavedrom==2.0.3.post3` in a scratch venv (`receipts/venv-freeze.txt`): "register reference: fresh (203 registers, 34 modules, 240 files)". `--selftest` also returns 0.

## Check 3: the wording against the RTL and the `a853461d` text

- **`hdl/milan/KL_pp_shadow.sv` at this head:** this file is unchanged since `a853461d`.
  - `:203` sets `RX_FIFO_BYTES_P = 4096`, and no instance in `hdl/` overrides it.
  - `:883-897` set `DEPTH (RX_FIFO_BYTES_P)`, `FRAME_FIFO 1`, `DROP_OVERSIZE_FRAME 1` and `DROP_WHEN_FULL 1`.
  - `:857-873` define `drop_evt_w = ff_overflow_w & last_kept_r`.
  - `:1640` reads `if (drop_evt_w & (rx_drops_o != 8'hFF))`.
  - So the counter counts a frame lost to a full FIFO, or a frame longer than the 4,096-byte FIFO, and saturates at 255. That is what the JSON field and the notes sentence say.
- **`milan_csr.sv`:**
  - `:982` maps `{tx[15:0], drops[7:0], rx[7:0]}` at `0x930`, which matches the generated `15:8` row.
  - `:699`'s port comment matches the wording.
- **Against the `a853461d` page text:**
  - The page's paragraph sentence carries over verbatim.
  - The page's `[15:8]` row read "control frames lost to a full ingress FIFO, or longer than the FIFO, counted rather than silently absorbed". The generated field keeps "or longer than the FIFO" and adds "saturates at 255", which `:1640` supports. Dev's new field format has no "counted rather than ..." clause.
  - One copy of the row's prose was not carried. See R803-4-R1.

## Check 4: gates and suite at this head

The packet lists each log and rc file.

| Command | rc | Result |
|---|---|---|
| `python3 scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK (533 lines, ...)` |
| `git diff --check 123f57a9 HEAD` | 0 | empty |
| `git diff --check a853461d HEAD` | 0 | empty |
| `gen_register_reference.py --check` / `--selftest` (wavedrom 2.0.3.post3) | 0 / 0 | fresh |
| `make -j16 -C tb/verilator/pp_shadow VERILATOR=<pinned 5.050>` | 0 | `pp_shadow: 317 checks, 0 failures`, `RESULT: PASS` |
| `make -C tb/verilator/pp_shadow drops-mutant` (pinned 5.050 on PATH) | 0 | `PASS: [DR] catches every arm (8 of 8); both clean controls pass` |

- **Toolchain:** the pinned wrapper reports `Verilator 5.050 2026-07-01 rev v5.050`, and the suite log shows it invoked. The system `verilator` is 5.054, and I did not use it.
- **`[DR]` figures:** they equal the author's published figures: burst 108 offered, 77 handed out, 31 lost, count 31. The 4,096-byte frame is kept and not counted. The 4,097-byte frame is counted +1. The flood of 501 losses saturates at `0xFF` and holds there.
- **Where it ran:** both builds ran on byte copies of this clone under `scratch/`.

## Findings

### R803-4-R1: RESIDUE, lens `Docs`. The register's long-form text in the design notes misses "or longer than the FIFO"

- **Where:** `docs/design/CSR_REGISTER_NOTES.md:1257`, section "PP_DIAG (offset 0x930)". The generated row links to this section as "Rationale and history".
- **Evidence:**
  - #825 moved the old reference-table cell for `PP_DIAG` here verbatim, from before this PR's correction. It reads "`[15:8]` **RX drops** -- control frames lost to a full ingress FIFO, counted rather than silently absorbed".
  - At `a853461d` that same cell read "... lost to a full ingress FIFO, or longer than the FIFO, counted rather than silently absorbed". That was R803-1-F3, taken "in all five places".
  - The merge carried the correction into the JSON field and the paragraph at `:1243`, but not into this copy (`receipts/wording-and-integrity.txt`).
- **Impact:** wording only. The generated field, the paragraph six lines above, the RTL comments and the tests all state both causes. No figure, test, code, generated artifact or clause claim changes.
- **Exact fix:** at `:1257`, change "control frames lost to a full ingress FIFO, counted rather than silently absorbed" to "control frames lost to a full ingress FIFO, or longer than the FIFO, counted rather than silently absorbed".
- **Verification:** `grep -n "lost to a full ingress FIFO" docs/design/CSR_REGISTER_NOTES.md` shows the full wording. `docs_inventory.py --check` and `gen_register_reference.py --check` still return 0, because the notes page is not generated.

## Prior findings at this head

I read these only after my own pass.

- **R803-3-S1** (`234_PP_SHADOW_AREA_BASELINE.md:126`, "340 at 1x1 and 341 at 8x8") and **R803-3-S2** (PR body LUT-share framing): both optional SUGGESTIONs. Retained: the file is byte-identical to `a853461d`, and the merge did not touch the PR body.
- **R804-3:** published no findings.
- **Rounds 1 and 2:**
  - every MINOR or MAJOR was resolved at `a853461d`: R803-1-F1, R803-2-F1, R804-1-F1 and R804-2-F1;
  - every RESIDUE was resolved there: R803-1-F2, R804-1-R1, R804-1-R2 and R804-2-R1;
  - none of the paths those fixes are on was changed by the merge. Check 2 shows all 14 PR paths byte-identical to `a853461d`.
- **R803-1-F3** (SUGGESTION, oversize wording): taken at `a853461d`. It is preserved at this head in the RTL, the CSR comment, the JSON field and the notes paragraph, except for one copy that #825 moved, which is R803-4-R1.
- **R803-2-S1 = R804-2-S2** and the reset part of R803-1-F4: carried to #495 by ruling. Unchanged.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #854 Required items, against `KL_pp_shadow.sv:203,857-897,1640` (byte-identical to `a853461d`) and `milan_csr.sv:699,982,2278`; the `[DR]` results in `receipts/pp_shadow-suite.log` (31 lost = count 31, the oversize frame counted, saturation at 255) | R803-4 | `b5d17214` |
| RTL | CLEAN | `receipts/merge-classification.txt`: `hdl/` paths are PR-only or dev-only and unchanged, and there is no hand resolution in `hdl/`; gitlinks equal dev's (`receipts/wording-and-integrity.txt`); `KL_pp_shadow.sv:857-897,1636-1640` re-read at the head | R803-4 | `b5d17214` |
| Robustness | CLEAN | `receipts/pp_shadow-suite.log` (refused, runt, oversize and saturation legs) and `receipts/drops-mutant.log` (8 of 8 killed, including `RXFILT=0`), on the merged tree with dev's 264 changes present | R803-4 | `b5d17214` |
| Tests | CLEAN | `tb/verilator/pp_shadow/*` byte-identical to `a853461d` (`merge-classification.txt`); suite rc 0 (317 checks, 0 failures) and `drops-mutant` rc 0 at this head with pinned Verilator 5.050 | R803-4 | `b5d17214` |
| Docs | CLEAN (R803-4-R1 RESIDUE, not counted) | `receipts/diff-dev-head-resolution.patch` (3 one-line changes); `scripts/register_descriptions.json:3919`; `docs/design/CSR_REGISTER_NOTES.md:1243,1257`; `docs/reference/REGISTER_MAP.md:4416`; `gen_register_reference.py --check` rc 0; `docs_inventory.py --check` rc 0; `git diff --check` against dev and `a853461d`, rc 0 | R803-4 | `b5d17214` |

## Limits and pending manager duties

- **The live PR head is `9405010f`, not `b5d17214`.**
  - That commit merges `dev` `45c0b56c` (#835). It changes `docs/design/AREA_BUDGET.md` (+5 -3), `docs/design/MAILBOX_SPLIT.md`, `docs/design/MARK_II_AREA_PLAN.md` and `docs/findings/README.md`, in an area the `Docs` lens covers.
  - Under AGENTS.md section 7, this ledger's `Docs` coverage does not reach `9405010f` until that delta is reviewed.
  - The manager owns routing it.
- **Hosted at `b5d17214`: incomplete, not failed.**
  - Recorded: 27 success, 28 cancelled, 6 queued, 1 skipped (Physical gPTP, nightly) and 3 failure (`receipts/hosted-check-runs.txt`).
  - Each of the three failures is an aggregation step that refused because a dependency was cancelled, not a test failure (`receipts/hosted-failures.txt`, `receipts/hosted-job-*.log`). Two of them assert on the `verilator-shards` result `cancelled`, a dependency's verdict, not a run of their own.
    - `docs-check` "Require every gate exactly once": `docs-gates-0` "dependent job failed, cancelled or skipped".
    - `Union pp_shadow`: `verilator-shards: cancelled`.
    - `Union milan_dp_mclk`: `verilator-shards: cancelled`.
  - The cancellations follow the push of `9405010f`. Hosted and act acceptance belong to the manager.
- **What I did not run:** no manager source bank and no full parent, PP, gPTP or Yosys bank. Source-head execution evidence beyond the gates above is the author's published receipts at `a853461d`, which R803-3 and R804-3 verified.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **Merge turn:** the manager validates the current-dev merge candidate there. I do not claim it.
- **Receipt redaction:** in `receipts/pp_shadow-suite.log`, the pinned toolchain's private install path is replaced by `<pinned-verilator-root>` and `<home>`. No other receipt is altered.
- **Clone integrity:** I removed two ignored `__pycache__` directories my runs created. Afterwards `git status --short --ignored` is empty, the worktree and index match the head, and the gitlinks equal dev's.

R803-4 FINISHED
