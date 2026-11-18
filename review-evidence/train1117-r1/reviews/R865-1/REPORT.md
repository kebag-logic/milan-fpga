[R865] POSITIVE - exact head 732726660a88cd79a568d650d955d535fe79c720

# R865-1: composition review of PR #945 (the Mark II flip train)

- PR: kebag-logic/milan-fpga #945, branch `flip-train-1117-p11` onto `dev-soft-core` `cb96336d`.
- Exact head `732726660a88cd79a568d650d955d535fe79c720`, tree `11d45104e6c71b7623cec24bcac27610c5a402be` (both verified in the
  isolated clone; the clone is clean at the end, see Restoration).
- Issues: #665, #871, #894, #917, #929, #919, #920, #923, #924, #925, #930, #936, #927.
- Role: internal, cleared-context, independent reviewer. Scope is the train's one composition review (#665
  issuecomment-6939574513): the resolutions, the composition commits, the restated figures, the step-11 merge, the
  release record and the gates at the final head. Each constituent PR's own content is covered by its two source
  reviews and is not re-reviewed here.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md, the PR body, #665's rulings (issuecomment-6939460730,
  6939574513, 6950343235, 6959600243, 6967930396, 6972255348, 6975966775, 6979461559, 6979996755, 6981065172), the
  public evidence archive `66fea879` (`review-evidence/train1117-r1/author-r1` to `author-r5`), `git diff
  cb96336d..732726660a` and its history. No private author material, lane scratchpad or other reviewer's report was
  read before this verdict and ledger were written.

## Verdict

POSITIVE. All five lenses are applied and clean at the exact head. Two RESIDUEs (wording in a design document and in
a comment header) are recorded with their exact fixes. No BLOCKER, MAJOR or MINOR is open.

## Findings

### R865-1-RES-1: AREA_BUDGET.md still calls #883's measurement the gate's record

- Severity: RESIDUE (wording only).
- Lens: Docs.
- Where: `docs/design/AREA_BUDGET.md:139` ("That measurement is the gate's record") and `docs/design/AREA_BUDGET.md:142`
  ("The route record's placement directive is ExtraPostPlacementOpt, the one flow difference the gate allows").
- Evidence: at the head, `syn/ooc/pp_resource_baseline.json`'s `route-1x1` endpoint is the train's record of
  2026-11-18 (`73272666`). Its flow line names `place_design -directive ExtraTimingOpt`, and its `measured` note names
  the train's final head. So both sentences describe a record that is no longer the gate's. The commit is record-only
  by #665 issuecomment-6979461559 item 3, and the PR's Known limitations disclose the stale utilisation table and the
  #234 findings page.
- Impact: none on any gate, measurement or figure. The gate reads the JSON. A reader of the area document is told the
  wrong current record and directive.
- Required outcome (exact fix): line 139 reads "That measurement was the gate's record until the flip train's
  record-only re-record of 2026-11-18 (#665 issuecomment-6979461559; `route-1x1` at 54,002 LUT, 55,203 FF, 15,849
  slices, 71 RAMB36, ExtraTimingOpt selected; the growth is #640 debt)." Line 142 reads "The route record's placement
  directive is the one the gate selected, ExtraTimingOpt since 2026-11-18; it is the one flow difference the gate
  allows." The utilisation table and the #234 findings page follow on the residue checklist, as the PR already states.
- Verification: `git grep -n "is the gate's record" docs/design/AREA_BUDGET.md` names no superseded record, and
  `docs_check.py` and `gen_toc.py --check` pass.

### R865-1-RES-2: issue-comment IDs in the split hot list's header

- Severity: RESIDUE (wording only, owner's comment rule of 2026-10-15).
- Lens: Docs.
- Where: `sw/firmware/ctrl/plat/ctrl_split_hot.txt:14` ("issuecomment-6959600243, item 1") and `:19`
  ("issuecomment-6967930396, item 1"). Both are added by the composition commits that relearn the list (`b5802de9`;
  the procedure text from round 4's relearn).
- Evidence: the rule keeps issue-comment IDs out of source comments. This header is the comment block of a link-order
  input and states its procedure. This item was first published by the concurrent review (its R866-1-R2). It was read
  only after this verdict and ledger were written, and reproduced at the head here (the widened scan below).
- Impact: none. `ctrl_hot.py` reads only the entries, and the images do not change.
- Required outcome (exact fix): line 14 reads "#665's ruling of 2026-11-17 on the third trace window, item 1"; line 19
  reads "(#665's ruling of 2026-11-18 on the link filter, item 1)". Every other word stays.
- Verification: `git grep -n issuecomment- sw/firmware/ctrl/plat/ctrl_split_hot.txt` prints nothing, `ctrl_hot.py
  --self-test` passes, and the 12 split images stay hash-equal (the header is not linked).

No other finding. Observations that are not findings:

- `082d0037`'s commit message says the moved `declared_verdict` body is unchanged. The AST differs only because, in
  its own module, the function drops the self-import and reads `PATHS` and `CONTROLS` unqualified. The behaviour is
  identical (receipts/check_refactors.txt). A commit message cannot be amended on a frozen train, so nothing is owed.
- The `+541` LUT growth compares the ExtraTimingOpt route with an ExtraPostPlacementOpt record. The `+400` and `+110`
  attribution is EPPO against EPPO (510). The difference of 31 is the directive. The PR body and the ruling say
  "about", which is accurate.

## What was examined, by review item

### (1) Train shape and frozen heads

- All eleven frozen heads (`d3e61e37`, `e1ecce20`, `394612c5`, `37255683`, `1a1e6665`, `81c9a1a0`, `d06ded5a`,
  `0fdfdba7`, `544fd72c`, `d1aa4c44`, `0297a19a`) are ancestors of the head.
- Each equals its PR's current GitHub `headRefOid`, and each is the second parent of its `--no-ff` merge on the first
  parent chain (receipts/frozen_heads.txt).
- Submodule gitlinks at the head are #934's: `gptp-processor` `1616fc8f`, `protocol-processor` `801ef228`.

### (2) Conflict resolutions

Every first-parent merge was replayed with `git merge-tree` and compared with the recorded merge
(scripts/replay_merges.sh, receipts/replay_merges.txt).

- In every step, the files the recorded tree resolves differently from git's merge are the conflicted files. The only
  exceptions each have a resolution row:
  - step 7: `ctrl_plat_image.py` (by `own_point`) and the split-boot README;
  - step 8: the split-boot README;
  - step 9: `CSR_REGISTER_NOTES.md` (#919's sentence carried out of the generated register page).
- No RTL file conflicted in any step. Both sides changed `hdl/milan/milan_datapath.sv` at step 9 and at step 11, and
  `tb_split_top.sv` at step 11; git auto-merged them. The split suites at the head cover them (see (6)).
- Step 11 (#939): the recorded merge differs from the replay only in the README conflict, and that resolution is the
  union ("thirty-one defects"; #839's transmit-gate sentence and #927's three EDIT-record defects). For every one of
  #939's 20 files except that README, step 11's delta equals #939's own delta line for line. At the head,
  `split_mutants.py` catches 31 of 31.
- The resolutions that touch firmware logic got full reading:
  - step 1, `AECP_QUEUED_MS` 140 by `queued_bound`: the 1x1/1if last queued notice is 137.97 ms at the head, within
    140;
  - step 2, THE SHAPES `ctrl_loop.h` (285 / 35 at 1x1/1if; 8x8/1if's own row);
  - step 5, `ctrl_plat.c`/`.h`/`_main.c`/`_gen.py`: the PHY frame in the refused-stage branch; REBOOT's departure
    keeps the loop, and with it THE STEP's PHY poll, stopped by design;
  - step 7, the `test_aecp.cpp` fixture `answer` (each window its own answer).
  These are exercised by the four firmware shards and the 797-plant control campaign at the head.

### (3) Composition commits

Each composition commit fixes only what the union broke, or does what a #665 ruling orders.

- **THE STEP, `03c92617`.** It implements ruling 6950343235 item 2 exactly (`sw/firmware/ctrl/plat/ctrl_plat_phy.c`,
  `ctrl_plat_phy_store_step`):
  - with `nvm_store_owed()` false and a frame owed, only the PHY steps;
  - otherwise the store's step comes first, and no frame follows a save's step.
  The return value is unchanged, because `nvm_store_step` never reports a non-centisecond step as owed. The four
  plants and L5/L6 are caught in the campaign. `6ad5c259`'s `(owes(ctx) || true)` keeps the plant compiling under
  `-Werror` and is still the ruled defect.
- **The cuts.** Each was checked for unchanged wire behaviour:
  - `ab4bc245`: `format_channels(p)` equals `channels(wire_be64(p))` bit for bit (bits 63..56 are `p[0]`; bits 31..22
    are `p[4]` and the top two bits of `p[5]`). The port geometry is read after `port->length >= 20` is checked.
  - `067c319d`: the per-buffer source-MAC cache is swapped with the buffers. Both start invalid (`~0u`), so the copy in
    `other` is written before its first use.
  - `7b3c1c94`: `acmp_listener_registered` only sets the flag. Its `enter()` side effect (`now_read = false`) is reset
    by every public entry, so skipping the call when the flag already agrees is behaviour-preserving.
  - `0bc158a7`: the inline commit and the include.
- **Oracle, `eafe4a16`.** The Listener-copy oracle now uses #925's rule. It reads `latest_kind` from the copy, but
  #925's own plants on the record of `latest_kind` (`srp_kind_mutants.py`) are caught by `SrpTalkerKinds.*`, so a
  defect there is still caught.
- **Re-anchored controls.** Each still fails for its defect:
  - `7a536fc5`: the SET_CONFIGURATION control moves to the first point where that command is the paced class's dearer
    member, because at 1x1/1if the defect would change no figure;
  - `c8ff391a`: it covers every 8x8/1if record and event where it checked one;
  - `4374cc27`: it reads the expected figure from `OWN_MEASURED` through `rule_us`.
- **Idiom-gate refactors** (receipts/check_refactors.txt).
  - AST-identical where claimed: `6fef44b8` (`build.py`, `grade.py`), `45708d9e` (`plat_mutants.py`) and `4a5bfb32`
    (`grade.py`, docstrings aside).
  - Tables equal when imported: `b1af3b54`'s `aecp_mutants.DEFECTS` (361) and `afbbde54`'s `plat_mutants.mutants`
    (121).
  - The two selftest moves (`7431b6ba`, `4a5bfb32`) carry every removed line into the new module, apart from one
    comment line.
- **Comment rule.** Every line the 30 composition-authored commits add, and every line new to both parents in the
  merges, was scanned.
  - My first pass covered code files only. Widened to every non-Markdown file, it finds one new instance, RES-2
    (`ctrl_split_hot.txt`).
  - The two `issuecomment-6906679024` strings and the `6412739248` string in `sw/litex/ctrl_memory.py` were already
    on the train side before composition (tracked by #746).

### (4) Restated figures

scripts/recompute_statements.py writes receipts/recompute_statements.txt. It reads the published spec and survey
receipts and recomputes each figure as 100 MHz cycles plus 5 %, rounded up to 5 us:

| Point | Figure | Cycles | Rule | Head |
|---|---|---:|---:|---:|
| 1x1/1if | one-row edit | 29,331 | 310 | 310 |
| 8x8/1if | polls base | 28,417 | 300 | 300 |
| 8x8/1if | apply | 35,350 | 375 | 375 |
| 8x8/1if | MAAP record | 16,682 | 180 | 180 |
| 8x8/1if | ADP record | 12,779 | 135 | 135 |
| 8x8/1if | SRP record | 35,547 | 375 | 375 |
| 8x8/2if | MAAP record | 14,770 | 160 | 160 |
| 8x8/2if | events' fixed part | 4,069 | 45 | 45 |
| 8x8/2if | AECP timer event | 11,404 | 120 | 120 |

- All 208 survey rows (41d2bc2b at 1x1/1if and 8x8/2if; unit375 at 8x8/1if): no statement at the head is under its
  rule.
- `CTRL_LOOP_SRP_UNIT_US` is 375 at 8x8/1if, the SRP record's own figure.
- `CTRL_LOOP_TX_MS` is 77, at most 80. `SRP_REDECLARE_CS`'s term `(77 + 9) / 10` is 8, so the withdrawn Talker's
  hold-off stays 8 cs.
- The owner bounds are unchanged: the load ceilings 0.70 and 0.75 (0.75 came with #914, not with composition), the
  last notice 140, ACMP 30 and txL 49. At the head, `flip_grade.py --check`:
  - at 1x1/1if: ACMP 29.93 of 30, txL 48.89 of 49, the last notice 137.97 of 140; `load_grade --check` 0.522 of 0.70;
  - at 8x8/1if: PASS, load 0.744 of 0.75, and THE TRANSMIT's row HELD at 76.81 of 77.
- Without `--point`, it fails on exactly the eleven 8x8/2if rows that the base `cb96336d` fails on, with no twelfth
  (both runs are in receipts/quick/).

### (5) Step 11, the CPU carry and the routes

Both receipts of ruling 6975966775 item 2 were checked.

- **Hash equality, rebuilt independently.** I rebuilt all twelve split firmware images (three points, four arms) at
  the exact head, with the pinned SDK whose archive hash is verified. All twelve `ctrl_app.elf` sha256 values equal the
  published p11 hashes (receipts/images/hashes-head.txt). Those equal the measured candidate's and U's images in the
  author's image-hash receipts.
- **Confirmation diff.** `regrade/confdiff-final.txt` covers seven groups: 8x8/1if `srp-talker-held` and the
  answering-ports arm's three measured groups, 1x1/1if `aecp-largest-notice` and `aecp-fanout`, and 8x8/2if
  `aecp-fanout`. Each is script-equal and log byte-identical, with 0 differing SPAN lines. The diff is EMPTY.
- **Independent confirmation run.** I ran 8x8/1if valid-destinations `srp-talker-held` again at the head, from its own build (image `e764b2fe…`). Its group log is byte-identical to the published one: sha256 `25617b7dac2047cbebe6c526f0f36c80f9cd285b4982a1916e29c39c4b231378`, 761,187 SPAN lines. The STEPS, SLICES, JOINS (187.150 to 190.414 ms), SAVE and grading lines diff empty against the published `c81vd.log`, with 0 budget misses (receipts/confirm-summary.txt).
- **Routes.** In `fit-summary-p11.txt`, 1x1/1if meets #818's floor on all three directives (EPPO +0.141 / +0.033 ns).
  8x8/1if meets it on its best of three (EPPO +0.073 / +0.034). Its ETO route is +0.064 / +0.027 and its
  AltSpreadLogic_high route misses at +0.006, as the PR states.

### (6) Release record and CDC

- **Record-only.** `73272666` changes `syn/ooc/pp_resource_baseline.json` alone, and only `route-1x1`'s `record` and
  `measured`. Tolerance, floor, ceiling, the other two endpoints and the schema are unchanged.
- **The record equals the receipts.** The committed record equals the published `record --write` and dry-run outputs
  field for field (receipts/record_compare.txt). It also equals the ruling's values and the selected route's placed
  utilisation report: LUT 54,002, FF 55,203, SLICE 15,849, RAMB36 71, RAMB18 27, DSP 15, WNS 0.194, WHS 0.017.
- **Gates.** `pp_resource_gate.py check-baseline` and `--selftest` pass at the head.
- **Attribution.** The hierarchy diff totals +400 LUT, +262 FF and -3 RAMB36. That is `u_fcdc` +192 FF and -3
  RAMB36, with its 128 LUTRAMs hoisted to `milan_datapath`, the meter +41 / -18, the EDIT claim registers +96 FF, and
  about +238 LUT elsewhere. This matches ruling 6979996755 item 5.
- **CDC.** `fcdc-summary.txt` shows:
  - Asynchronous Clock Groups cover the storage-to-register paths, slack inf;
  - 201 of 201 endpoints are Safe;
  - CDC-15 x192 on `u_fcdc` at the release image and at 1x1/1if; no CDC-26; nothing in methodology;
  - no render master at 8x8/1if.
  This matches ruling 6981065172.
- **Corrected premise.** No tree text calls the distributed-RAM branch split-only. `cdc_pair_fifo.sv`,
  `KL_tdm_render_master.sv` and the PR body say it is shared.

### (7) Gates at the final head

My runs are on disposable clones of the exact head; the logs and rc files are in receipts/.

- **Firmware.** `test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 .. 3/4` passes on all four shards. The
  control campaign catches 797 of 797. `fw_coverage.py --check` passes.
- **milan_dp.** `split` (145 checks, 0 failures) passes. `split-mutants` catches 31 of 31. `split-cdc`, `dynmap`,
  `maprec8` and `maprec4` pass. `twin`, `twin-plants` (16 plants, each refused), `twin-maps` and `twin-maps-plants`
  pass.
- **Render, clock meter and mailbox.** `milan_dp_render tdm8render tdm8render-mutants`, `aaf_clock_meter all mutants`
  and `mbx all dma-mutants` pass: 32 of 32 render checks, including #927's distributed-storage mutant; clock meter mutants 38 of 38; record mover mutants 25 of 25. The first run was killed by the host reset, kept as receipts/gates/dp_b.killed-by-reset.log, and re-run in full.
- **Docs and hygiene.** `docs_check`, `check_py_idiom`, `check_hygiene --check`, `gen_toc --check` and
  `--verify-anchors` pass. `git diff --check cb96336d...HEAD` prints nothing.
- **CPU budget harness.** `run.py --self-test` reports 0 failures. The `flip_grade` and `load_grade` results are in
  (4).
- **ROM ledger.**
  - `plat_ledger.py --self-test` passes with 9 of 9 controls. The four platform images are at the ledgered sizes:
    `ctrl_plat` 18,048 / 19,712 / 18,944 / 21,568 B, and 8x8/1if at 58.0 with 137,472 B of rom.
  - `test_ctrl_memory.py` passes.
  - The twelve fixture images build and link within their entries, including the fixture at 60.5.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_plat_phy.c` `ctrl_plat_phy_store_step` against #665 issuecomment-6950343235 item 2 (IEEE 802.3 22.2.4.2.13, 802.1AS-2011 10.2.4.11, Milan v1.2 4.2.6.2.5); `aecp_maps.c` `format_channels` and `geometry` (wire-identical AECP map responses, IEEE 1722.1-2021 7.4.44/45); `aecp.c` `fan_out` source cache (IEEE 1722.1-2021 9.2.1.1 source address); `ctrl_app_srp.c` `deliver`; `ctrl_loop.h` THE SHAPES (77 ms, 375 us, `SRP_REDECLARE_CS` 8 cs, 802.1Q 35.2.2.8); every restated figure against rulings 6967930396 and 6972255348; the record against 6979461559, 6979996755 and 6981065172 | R865-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| RTL | CLEAN | merge replay of all 16 first-parent merges (receipts/replay_merges.txt); step 11's 20 files against #939's delta; `milan_datapath.sv` both-sides auto-merges (steps 9 and 11); `cdc_pair_fifo.sv` and `KL_tdm_render_master.sv` (DIST_RAM_P shared); `fcdc-summary.txt` (CDC-15 x192, 201/201 Safe, async groups); `fit-summary-p11.txt` routes against #818's floor; release `resource_gate.log` and `hier-diff.txt` | R865-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| Robustness | CLEAN | THE STEP's call types (centisecond owed, frame owed, neither; room under `CTRL_PLAT_PHY_STEP_US`); REBOOT departure with the PHY idle (step-5 resolution); `aecp_map_command` with zero mappings and a short port (length >= 20 checked before `geometry`); `fan_out` held and lost frames with the swapped buffers and source caches; `acmp_listener_registered`'s `enter()` side effects when skipped; L5/L6 and B12 plants in the 797-plant campaign | R865-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| Tests | CLEAN | four firmware shards (797/797), milan_dp `split` to `twin-maps-plants` (31/31 split mutants, 16 twin plants), render/meter/mbx suites, `run.py --self-test` 0 failures, `flip_grade` at three points plus all points against the base, `load_grade --check`, `fw_coverage --check`, `plat_ledger --self-test` 9/9, `test_ctrl_memory`, `pp_resource_gate --selftest`; the re-anchored controls `7a536fc5`, `c8ff391a` and `4374cc27`; the oracle `eafe4a16` against #925's plants; refactor identity (receipts/check_refactors.txt); 12 images rebuilt hash-equal; an independent `srp-talker-held` confirmation | R865-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| Docs | CLEAN (RES-1 and RES-2 recorded as RESIDUE) | `docs_check`, `gen_toc --check`/`--verify-anchors`, `check_hygiene`; `0b054867` (FR_NFR.md, SPLIT_CONTROL_MEMORY.md, the SRP README); `d7c8cd95` and `dccca6ec`; `AREA_BUDGET.md:139,142` (RES-1); `ctrl_split_hot.txt:14,19` (RES-2); comment-rule scan of every composition-authored non-Markdown line; RESOLUTIONS r1 to r5 rows against every resolved file; PR body tables against receipts | R865-1 | 732726660a88cd79a568d650d955d535fe79c720 |

## Prior public findings

PR #945 had no review rounds before this one. A concurrent independent review (R866, POSITIVE at this head) was read
only after this verdict and ledger were written. Its two wording-only items are dispositioned as follows:

- **R866-1-R2** (the issue-comment IDs in `ctrl_split_hot.txt`): reproduced, and retained as RES-2.
- **R866-1-R1** (`test_plat_boot.cpp:91,95,116,119`): not retained as a separate item. The labels there are the
  file's own GoogleTest identifiers (`Boot.B24`, `Phy.B11`, `Phy.L5`, `Phy.L6`) in its index of tests. Steps 1 and 5
  renumbered or added them, and they are not bench lane labels. If the manager reads them as labels, they are still
  wording only and RESIDUE, so the verdict does not move.

## Real limits

- No manager source bank runs at this head, and none is claimed. Source-head execution evidence is the author's
  published receipts plus my own focused runs listed above. The current-dev merge candidate (base `cb96336d`, live dev
  `e275d795`) is the manager's, and none of it was built here.
- No Vivado run was made. The routes, the release resource figures, the hierarchy diff and the CDC reports are read
  from the published receipts, not regenerated.
- The CPU service-budget rows are not re-measured in full. They are carried, as the ruling permits, by hash equality
  (rebuilt here), the published empty confirmation diff and one independent confirmation group.
- Hardware was not used. Physical calibration was NOT RUN, and field skips are not hardware proof. The S12b bench is
  the manager's.
- Hosted CI and act results were not inspected as acceptance. The manager owns them.
- `check_refactors.py` could not import the harness `selftest_mutants.MUTANTS` table without the processor submodule
  in a snapshot. Those two moves were checked by source line, and the head's `run.py --self-test` imports and runs the
  table.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks), and link its receipts.
- Carry RES-1, RES-2, the AREA_BUDGET.md utilisation table and the #234 findings page update to the residue checklist.
- Keep #495's CDC-15 listing for the render crossing beside the capture crossing (ruling 6981065172 item 5).
- Hosted exact-head gates and the S12b bench on the final bitstream.
- The merge needs two independent positive reviews and the maintainer's explicit authorization.

## Restoration

No source was edited in the reviewed clone; every probe ran in disposable clones under the packet's scratch. At the end, in the reviewed clone (receipts/restore.txt):

- HEAD `732726660a88cd79a568d650d955d535fe79c720`; tree and `git write-tree` are both `11d45104e6c71b7623cec24bcac27610c5a402be`;
- 0 index-vs-HEAD and 0 worktree-vs-index differences (tracked blob bytes and modes), and no untracked file;
- the five gitlinks and checkouts at `1616fc8f`, `801ef228`, `08ee86e8`, `715589c1` and `48ff7a7e`, each clean.

The host reset at 16:20 killed two runs, the render, meter and mailbox chain and the confirmation group. Both were re-run, and every receipt cited above is complete. No comment was posted by this review.

R865-1 FINISHED
