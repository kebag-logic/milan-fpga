[R829] NEGATIVE - exact head 8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3

# R829-4: internal cleared-context delta review of PR #892 (issue #665), the merge of dev-soft-core `0fb66211` into the tsn-c-stack pin move

- **Head:** `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3`, tree `3fc10918a16904288ed2c62e8f2649fd2b1485b1`. It is one merge commit, with parents `32b43973` (round 3, POSITIVE from R829-3 and R830-3) and `0fb66211` (dev-soft-core).
- **Delta reviewed:** `git show --remerge-diff 8bc1dfc0` (5 files), both parents' diffs from the old base `1d6bf555`, and the PR's whole diff against its new merge base `0fb66211` (26 files).
- **Verdict: NEGATIVE.** Three MINOR findings are open: F1 (Docs), F2 (Docs) and F3 (Tests, Docs).
  - No BLOCKER or MAJOR finding.
  - The merge itself is correct. Both conflicts are resolved by measurement, not by picking a side. The owner's flip-ROM decision is respected in code and tests, the seven auto-merged files keep both sides, no gitlink moved, and every gate I ran passes.
  - What fails is three published claims around the merge:
    - F1: the "tightest point" headroom claim misses a 16 B `sram` margin.
    - F2: a harness README still states the fixture's old ledger value.
    - F3: the published explanation of the `nvm_store.c` ratchet line is contradicted by the author's own receipt and by hosted CI.
  - None of the three needs a code, test or generated-artifact change.
- **Also recorded:** five RESIDUE items (two new, three retained or updated from prior rounds) and four new SUGGESTIONs. Prior optional suggestions are retained.

## Reconstruction (public state only)

1. `AGENTS.md` and `CONTRIBUTING.md` give the five lenses, the severities and the three-column ledger.
2. Issue #665:
   - the owner's flip-ROM decision, issuecomment-6824896581, read in full;
   - REVIEW READY, issuecomment-6829628610;
   - the review start on PR #892, issuecomment-6829687352.
3. Interface authorities:
   - `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6;
   - `sw/litex/ctrl_memory.py` (`LEDGERED`, `banks`);
   - `sw/litex/ctrl_memory_ledger.py` and `sw/litex/test_ctrl_memory.py`;
   - `sw/firmware/gtest/fw_coverage.py` (`compare`).
4. The diff and history:
   - `git show --remerge-diff 8bc1dfc0` (`receipts/remerge-diff.txt`);
   - `1d6bf555..32b43973` and `1d6bf555..0fb66211` per shared file;
   - `0fb66211..8bc1dfc0` (`receipts/pr-diff-vs-merge-base.txt`);
   - dev's first-parent range since `1d6bf555`: #874, #880, #889 and #888.
5. Executable evidence:
   - the author packet `review-evidence/tsnpin-r1/author-r4` at archive `c621aff3`, checked against its `MANIFEST.json`;
   - my own runs on the exact head (listed below).
6. The live PR body (`receipts/pr-body-live-at-review.md`).
7. Prior public review reports R829-3 and R830-3, read only after my own pass over the merge.

## The assignment's checks

### (1) The two conflicted files: each value derived by measurement

**`sw/litex/ctrl_memory.py:246-255` (platform 8x8/2if key).**
- The conflict was the PR's `(nvm_stage 13,264, ctrl_plat 21,392)` against dev's `(13,594, 21,240)`. The base `1d6bf555` had `(13,264, 21,240)`.
- So the PR changed only `ctrl_plat`, by +152, and dev changed only `nvm_stage`, to KLJ3. The resolution `(13,594, 21,392)` is the composition of the two.
- It is measured, not chosen:
  - the merged platform build reports `nvm_stage` 13,594 B (`platform-merge/8x8-if2.size.json`, `largest_bss`);
  - its `ctrl_plat` members show `app` 10,216 against 10,064 at `0fb66211` (+152, the same at every point);
  - that image plans 59.0 under `ledgered: platform-8x8-two-interfaces` with link rc 0, which the planner accepts only when both symbols match the key.
- The ledger constants agree: `ctrl_memory_ledger.py:30,34` hold `STAGE_*` = 3,454 / 13,594 (dev's) and `PLAT_*` = 18,584 / 20,080 / 19,240 / 21,392 (the PR's).

**`docs/design/SPLIT_CONTROL_MEMORY.md` section 3 table (`:124-131`).**
- Fixture `nvm_stage` 13,594 + `image_allocation` 16 at 58.0; platform 13,594 + `ctrl_plat` 21,392 at 59.0.
- These are identical to `LEDGERED` and to what `test_ctrl_memory.py` holds (`receipts/logs/test_ctrl_memory.log:13`).

**Section 5's composed table (`:369-374`) and the plans.**
- I recomputed all 16 receipt points (4 points x fixture/platform x `0fb66211`/merge) with the head's own `ctrl_memory.banks` (`scripts/headroom.py`, `receipts/headroom.txt`).
- Every bank list and every tile figure matches the receipts:
  - fixture 37.5 / 41.0 / 51.0 / 58.0;
  - platform 39.5 / 42.0 / 52.5 / 59.0;
  - at `0fb66211`: 37.5 / 41.0 / 51.0 / 57.5 and 39.0 / 42.0 / 52.5 / 59.0.
- Every "(+N)" delta in the table equals merge minus `0fb66211` in the receipts.
- The two plan moves reproduce exactly:
  - fixture 8x8/2if: 121,064 B is 232 B over 120,832 (five banks), and plans 122,880 B in four banks;
  - platform 1x1/1if: 110,760 B is 168 B over 110,592, and gains a fifth bank of 2,048 B.
- I did not re-link the images myself. The receipts' byte counts are self-consistent with the head's planner. Links are rc 0 at all eight merged points (`*.rc`), and the packet's hashes verify.

### (2) The owner's flip-ROM decision (issuecomment-6824896581)

- **The decision:** platform 60.0, cap 60.5; fixture 58.0, cap 58.5; every other point at most 56; it supersedes, for the flip only, the "56 at every point with S14 merged" line.
- **`SPLIT_CONTROL_MEMORY.md:382-385`** states this correctly.
- **`LEDGERED`** holds the measured tiles: fixture 58.0, which is the owner's figure, and platform 59.0, which is under the owner's 60.0. It refuses half a tile past either.
  - That is stricter than the caps, never looser, so the decision is respected.
  - Every non-ledgered point is at most 52.5.
- **`ctrl_memory_ledger.py`** moved consistently:
  - `OWN` and `HELD` are at 58.0;
  - "half a tile past" is now 58.5;
  - the other images, a missing symbol and the platform's image are refused at 58.0;
  - the planted "fixture's entry at the platform's 59.0" still widens it.
- **`test_ctrl_memory.py`:** the docstring and the check text follow. The suite passes on the head: `receipts/logs/test_ctrl_memory.log`, 0 failures, `RESULT: PASS`. Ledger rows 13-16 and 49-65, planted ledgers 191-197 and the mapper rows 198-205 all show the new values.

### (3) The seven auto-merged files lose neither side

The seven files: `MAILBOX_SPLIT.md`, `sw/firmware/ctrl/README.md`, `plat_arms.py`, `gtest/README.md`, `ctrl_service_budget/README.md`, plus `coverage.ratchet` and `ctrl_memory_ledger.py`, which were auto-merged and then edited.

- **The five plain auto-merges:** for each, the PR side's changed-line set (`1d6bf555..32b43973`) equals the merge's diff against dev, and dev's changed-line set (`1d6bf555..0fb66211`) equals the merge's diff against the PR side. Both sides are carried verbatim.
- **Semantic check:** the hunks are disjoint in meaning.
  - `plat_arms.py`: the PR's `__lshrdi3` check sits beside dev's `shape_header(shape)` call.
  - The READMEs: the PR's pin links and kept-command text sit beside dev's #870 timing-cut, KLJ3 and region-decode text.
- **The two edited files** differ only by the resolution edits in the remerge diff, reviewed under (1), (2) and (4).
- **No new stale pin link:** every `70936b77` mention at the head is one of the round-3 set, with the same files and counts (`ci/image/exec-audit-receipt.json`, which the PR body explains, and historical "at `70936b77`" statements).

### (4) `coverage.ratchet` and the `nvm_store.c` 459/459 explanation

- **The ratchet value is right.** My `fw_coverage.py --check` on the head passes with 35 files and measures `nvm_store.c` 459/459 lines (`receipts/logs/fw_cov_check_head.log:50`).
- **The explanation does not hold** (F3).
  - REVIEW READY says "the same generator at `0fb66211` alone writes dev's ratchet byte for byte, so the extra line is the composed builds' instrumentation".
  - The author's own `fw_coverage-write-at-0fb66211.log:34,51` measures `ctrl_app_aecp.c` 165/165 and `nvm_store.c` 459/459 at `0fb66211`, where dev's committed ratchet reads 164 and 458.
  - The receipt `fw_coverage-write-at-0fb66211-diff.txt` shows `coverage.ratchet | 4 ++--, 2 insertions(+), 2 deletions(-)`, followed by the annotation "(empty: … unchanged)". The stat is right and the annotation is wrong.
  - Hosted firmware-unit job 130955656991 ran on `55cb2491`, whose tree is identical to `0fb66211`, with Ubuntu GCC 13.3.0. It also measures 459/459 and 165/165 (`receipts/coverage-provenance.txt`).
  - In my kept coverage data, each of the 14 builds that compile `nvm_store.c` instruments the same 459 lines (`receipts/nvm_store_gcov_lines.txt`). That includes the saved-state suites, which nothing in this PR touches.
  - So the extra line is not a composition effect. Dev's committed ratchet lines sit one below dev's own measurement on both toolchains, and the merge's `--write` records the measurement.
- **Gate impact: none.** `compare` reads fractions (`fw_coverage.py:403`), so 458/458 and 459/459 are both 100 %.

### (5) No submodule pin moved

- Every gitlink at `8bc1dfc0` equals its value at `32b43973`: `external`, `gptp-processor`, `protocol-processor`, `lwSRP`, `verilog-axis`, and `tsn-c-stack` at `715589c1` (the PR's move from `70936b77`).
- The merge's diff against `0fb66211` touches only the `tsn-c-stack` gitlink, which is the PR's own change.
- After my runs, the clone's index, write-tree (`3fc10918…`) and every submodule checkout are unchanged (`receipts/restore-check.txt`).

### My runs on the exact head

- **SDK:** the pinned RV32 SDK, installed from its archive (sha256 `d42680e9…`, equal to `ARCHIVE_SHA256`) into a disposable home and verified fresh. It reports Buildroot 2021.11-18033-g83947c7bb6, GCC 14.3.0 (`receipts/logs/sdk-install.log`).
- **`sw/litex/test_ctrl_memory.py`** (LiteX venv, RV32 on PATH): 0 failures, PASS.
- **`test_ctrl_firmware.py --require-rv32 --self-test`**, shards 0/4 to 3/4: all rc 0, `test_ctrl_firmware: PASS`.
  - The control campaign reports "mutants: 586 of 586 caught".
  - `acmp-redelivery-past-a-decline` and `wire-put-be-shifts-64-bits` are caught by name.
- **`fw_coverage.py --check`:** PASS with 35 files; `acmp_mbx.c` 106/106 and 42/42; `nvm_store.c` 459/459.
- **Docs gates:** all rc 0 (`receipts/logs/docs_gates.txt`). The eleven gates: `docs_check.py`, `check_feature_status.py`, `check_doc_style.py`, `check_gptp_docs.py`, `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `submodule_boundaries.gen.py --check`, `check_submodule_docs.py`, `check_nvm_klj3.py`, `check_nvm_format_32x32.py` and `check_wire_accountability.py`.
- **Author packet:** 479 entries listed, 0 missing, 0 hash mismatches, 0 unlisted (`receipts/author-packet-manifest-check.txt`). The archive commit is not signed (git signature status N), so the packet's integrity rests on its hash list only.

## Findings

### F1 — MINOR — Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:380` (and the live PR body line 81) — the "tightest point" omits a 16 B `sram` margin at the platform's ledgered point

- **Authority / evidence:** the claim is "The tightest point is now the platform's 1x1 with two interfaces, 288 B of `rom` before its next granule."
  - Recomputed with the head's `ctrl_memory.banks` from the merged receipts (`receipts/headroom.txt`): the platform's 8x8/2if `sram` needs 114,672 B in banks of 114,688 B, which leaves **16 B**.
  - The smallest `rom` margin is indeed 288 B (platform 1x1/2if). That point's `sram` margin is also 288 B.
  - At round 3 the same sentence ("88 B of `rom`") was the minimum over both regions. At `0fb66211` this `sram` margin was 176 B, and the merge took 160 of it.
- **Impact:** a reader planning the next lane (S2b's sync, S14) takes 288 B as the nearest plan move.
  - In fact 16 B more `.bss` or stack at the platform's 8x8/2if plans 59.5.
  - That is within the owner's 60.0 / 60.5, but `LEDGERED` holds 59.0, so `ctrl_plat_image.py` would refuse that image until the ledger is re-measured and moved.
  - This changes a measurement-derived claim, not only its wording.
- **Required outcome:** section 5 and the PR body state the smallest margin of each region at the merge: `rom` 288 B (platform 1x1/2if) and `sram` 16 B (platform 8x8/2if, whose next granule plans 59.5 against its 59.0 ledger key). Alternatively they qualify "tightest" as `rom` only and add the `sram` figure.
- **Verification:** `python3 -I scripts/headroom.py <repo> <author-r4/receipts/round4>` reproduces both minima. Re-read `:380` and the PR body.

### F2 — MINOR — Docs — `tb/verilator/ctrl_service_budget/README.md:44` and `:114` — the harness README states the fixture's ledgered point at 57.5

- **Authority / evidence:** at the head, `ctrl_memory.LEDGERED["8x8-two-interfaces"].tiles` is 58.0 (`ctrl_memory.py:247-249`).
  - The harness reads it through `split_soc.ledgered_plan` (`split_soc.py:456-457`), which reads `ctrl_memory.LEDGERED`, so the harness's behaviour follows the ledger.
  - But the README says, in the present tense, that `8x8-two-interfaces` "may plan 57.5 RAMB36" (`:44`) and that at `8x8` its plan "is held to the ledgered point's 57.5 RAMB36 (`split_soc.ledgered_plan`)" (`:114`).
- **Why this is not covered by the PR's known-limitations line:** that line says the harness READMEs "record measurements at the old pin". These two lines are not measurements. They state the harness's configuration, and the merge changed it.
- **Impact:** the harness's authoritative page misstates the planner limit its own 8x8 build runs under. A cold reader of S2's figures is told a ceiling that no longer holds.
- **Required outcome:** both lines state 58.0, or name `ctrl_memory.LEDGERED` without restating the number.
- **Verification:** `git grep -n '57\.5' -- tb/verilator/ctrl_service_budget/README.md` returns only historical, dated figures.
- (A related but weaker case, `SAVED_STATE_FORMAT_32X32.md:473`, is S2.)

### F3 — MINOR — Tests, Docs — REVIEW READY #665 issuecomment-6829628610 (`coverage.ratchet` bullet), the same text in `receipts/round4/review-ready-comment.md`, and the receipt `author-r4/receipts/round4/fw_coverage-write-at-0fb66211-diff.txt` — the `nvm_store.c` 459/459 provenance claim is false

- **Authority / evidence:** see check (4) above and `receipts/coverage-provenance.txt`.
  - The author's own write at `0fb66211` gives 459/459 and 165/165, against dev's committed 458 and 164.
  - The receipt's stat (2 insertions, 2 deletions) contradicts its "(empty …)" note.
  - Hosted CI with GCC 13.3 on the identical tree gives 459/459 and 165/165.
  - Every individual build instruments the same 459 lines, so there is no composition effect.
- **Impact:** the PR's evidence explains a generated test artifact's change by a cause that its own receipt refutes.
  - A cold reviewer would conclude that the pin move or the composition changes `nvm_store.c`'s instrumentation. Neither does: dev's ratchet lines are simply one below dev's measurement.
  - This is the same mechanism as round 3's `ctrl_app_aecp.c` 164 -> 165, which this text does not mention.
  - No gate or tracked value is wrong. The ratchet at the head equals my measurement.
- **Required outcome:**
  - The public evidence states the real provenance: at `0fb66211` the generator, and hosted CI, already measure 459/459 for `nvm_store.c` and 165/165 for `ctrl_app_aecp.c`, so the merge's `--write` records dev's current measurement, which dev's committed ratchet under-recorded by one line in each file.
  - The receipt's annotation is corrected or replaced.
  - No tree change is required.
- **Verification:** the corrected text matches `fw_coverage-write-at-0fb66211.log:34,51` and hosted job 130955656991's `fw_coverage --check` lines.

### RES-1 — RESIDUE (new) — Docs — `sw/litex/ctrl_memory.py:249`, an issue-comment ID in a new source string

- The resolution adds "the owner's 6824896581: 58.0, at most 58.5" to the fixture's `owed` string.
- The field's own contract (`:228`, "the lane that recovers the tiles, and the ruling") invites a ruling citation, and the entry's older IDs predate this delta (#746 tracks them). But the comment rule bars issue-comment IDs in new source text.
- The platform's entry (`:251-254`) does not cite the same decision, which gives it 60.0, at most 60.5.
- **Exact fix:** `"…; the owner's decision of 2026-11-12: 58.0, at most 58.5)"`. Optionally add `"; the owner's decision of 2026-11-12: at most 60.0, cap 60.5"` to the platform's string.

### RES-2 — RESIDUE (new) — Docs — `SPLIT_CONTROL_MEMORY.md:366`; live PR body line 57; REVIEW READY — the dev range is four PRs, not two

- "`0fb66211`, which carries the split's KLJ3 stage (#823) and #888 and #889", and the PR body's "(S9 #889 and #791 #888 on `dev-soft-core`)".
- Since the old base `1d6bf555`, dev landed #874 (S7, lwSRP's transmit path), #880 (saved-state format for shapes up to 32x32), #889 and #888.
- The figures are measured against `0fb66211` by SHA, so none changes.
- **Exact fix (`:366`):** "On dev-soft-core `0fb66211`, which carries #874 (lane S7's lwSRP transmit path), #880 and #889 (the split's KLJ3 stage, #823) and #888, …". Make the same change in the PR body row.

### RES-3 — RESIDUE (new) — Docs — live PR body line 164 — S2b's owed ledger is stated "against the ledgered 57.5"

- At this head the fixture's ledger is 58.0.
- **Exact fix:** "its 8x8/2if size fixture's ledger (122,984 B of `rom`, measured on S2b's head; this head's ledger holds that point at 58.0, so S2b restates the key only if its image's symbols or tiles differ)". Use whatever S2b's ruling, issuecomment-6811790762 item 4, now requires.

### RES-4 — RESIDUE (retained, R830-3 RES2) — Docs — `tb/verilator/ctrl_service_budget/scenario.py:312`

- The docstring anchor "MAILBOX_SPLIT.md:649-661" is further off now. The "ACMP service latency" heading is at `MAILBOX_SPLIT.md:689` after the merge brought dev's lines.
- **Exact fix (unchanged):** "ACMP's rows (MAILBOX_SPLIT.md, section ACMP service latency)".

### RES-5 — RESIDUE (retained, R829-3 RES-A = R830-3 RES3) — Docs — live PR body line 62

- The text "Every RV32 build in this PR's figures and gates used the pinned SDK" is unchanged.
- **Exact fix (unchanged):** "Every RV32 build in this PR's figures, and every gate at `8bc1dfc0`, used the pinned SDK, …".

### S1 — SUGGESTION — Docs — `SPLIT_CONTROL_MEMORY.md:250` and `:284`

- Both lines still say "The flip (S13) … requires 56 RAMB36 or fewer at every point, with S14 merged".
- `:382` supersedes that for the flip only, as the owner asked. A forward pointer at each would stop a reader stopping early: "(superseded for the flip by the owner's decision of 2026-11-12, below)".

### S2 — SUGGESTION — Docs — `docs/design/SAVED_STATE_FORMAT_32X32.md:473`

- "Its area evidence is the split memory plan, 57.5 RAMB36 at the ledgered point" is true of KLJ3's own measurement, but reads as current.
- Suggested: "57.5 RAMB36 at the ledgered point when KLJ3 was measured; 58.0 with the tsn-c-stack pin move (SPLIT_CONTROL_MEMORY.md section 5)".

### S3 — SUGGESTION — Tests — `sw/litex/ctrl_memory_ledger.py:74-75`

- The unheld-name case keeps `Case(STAGE_8X8, 1, None, 57.5)`. It is refused by name whatever its tiles, so it is correct.
- Writing it as `OWN[FIXTURE].tiles` would keep it at the ledgered point's tiles the next time the ledger moves, as the moved rows do.

### S4 — SUGGESTION — evidence packet (no lens) — `author-r4`

- The archive commit `c621aff3` is unsigned. Integrity rests on `MANIFEST.json`, whose 479 `author-r4` entries all verify.
- If "signed packet" is meant literally, sign the archive commit or a detached manifest.

### Prior-round suggestions, retained as optional

The delta does not touch `acmp_mbx.c`/`.h`, `test_acmp_mbx.cpp` or `acmp_owed_mutants.py`; all are byte-identical to `32b43973`. So these keep their scope and stay optional:

- R829-2 S1 = R830-2 S3;
- R829-2 S2;
- R829-2 S3 = R830-2 S1;
- R830-2 S2, S4 and S6;
- R830-3 S1 and S2;
- R829-3 S-1.

## Prior public findings: resolved or retained at this head

| Prior finding | State at `8bc1dfc0` | Evidence |
|---|---|---|
| R829-2 F1 = R830-2 N1 (MINOR, Tests and Robustness): the stop at a decline | **CLOSED**, stays closed | K8 and its plant are unchanged since `32b43973`. `acmp-redelivery-past-a-decline` is caught by name in my shard run, and the campaign caught 586/586 |
| R829-2 F2 (MINOR, Docs): builder leg 0's compiler | **CLOSED**, stays closed | `round4/builder-legs/builder_leg0.log` names the pinned Buildroot 2021.11 build. The PR body says so |
| R829-3 RES-A = R830-3 RES3 (PR body SDK sentence) | **OPEN**, retained as RES-5 | live PR body line 62 |
| R829-3 RES-B = R830-3 RES1 (reused-step claim) | **CLOSED** (superseded) | Nothing is reused at this head (REVIEW READY: "Nothing is reused from round 3"). The PR body no longer makes the claim |
| R830-3 RES2 (`scenario.py:312` anchor) | **OPEN**, retained as RES-4 | `scenario.py:312`; `MAILBOX_SPLIT.md:689` |
| R829-2 RES1-RES3 = R830-2 RES2-RES3 | **CLOSED**, stays closed | the text is unchanged since `32b43973` |
| The optional suggestions listed above | retained | their scope is untouched by the delta |

## Lens results at `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3`

```text
[R829] PASS Conformance — sw/litex/ctrl_memory.py:246-255; SPLIT_CONTROL_MEMORY.md:124-131,382-385; receipts/headroom.txt; receipts/logs/test_ctrl_memory.log:13-16,49-65 — LEDGERED and the doc checked against the owner's decision 6824896581 (fixture 58.0 <= its 58.0 / cap 58.5, platform 59.0 <= its 60.0 / cap 60.5, every other point <= 52.5 <= 56); both keys equal the composed images' measured symbols; no protocol behaviour changed (acmp_mbx.c/.h identical to 32b43973)
[R829] PASS RTL — receipts/pr-diff-vs-merge-base.txt — the PR's 26-file diff against 0fb66211 contains no hdl/, .sv/.v, syn/ or SoC-builder file, so the merge's RTL is dev's byte for byte; the ctrl_memory.py change is ledger data only, and the planner's bank and decode code is unchanged by the resolution
[R829] PASS Robustness — ctrl_memory_ledger.py:47-78,115-128; receipts/logs/test_ctrl_memory.log:49-65,191-197 — the override stays fail-closed at the moved value: half a tile past (58.5), other points at its tiles, the other image, a missing symbol and unheld names are each refused; the planted widenings are caught; the 16 B sram margin (F1) is a documentation defect, the ledger refusing growth there is the designed behaviour
[R829] UNCLEAN Tests — F3: author-r4/receipts/round4/fw_coverage-write-at-0fb66211-diff.txt and REVIEW READY's provenance claim for the regenerated ratchet are refuted by fw_coverage-write-at-0fb66211.log:34,51 and hosted job 130955656991. Otherwise applied clean: test_ctrl_memory PASS; test_ctrl_firmware --require-rv32 --self-test shards 0-3 PASS (586/586); fw_coverage --check PASS (receipts/logs/*)
[R829] UNCLEAN Docs — F1 SPLIT_CONTROL_MEMORY.md:380 (and PR body line 81); F2 tb/verilator/ctrl_service_budget/README.md:44,114; F3 REVIEW READY coverage bullet. Otherwise applied clean: section 3 and 5 tables and section 6 match LEDGERED and the receipts; the eleven docs gates rc 0 (receipts/logs/docs_gates.txt)
```

## Reviewer-owned ledger

| Lens | CLEAN / UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | owner decision 6824896581; `ctrl_memory.py:246-255`; `SPLIT_CONTROL_MEMORY.md:124-131,366-385,404`; `receipts/headroom.txt` (16 points recomputed); `test_ctrl_memory.log` | R829-4 | `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3` |
| RTL | CLEAN | `receipts/pr-diff-vs-merge-base.txt` (no RTL against `0fb66211`); remerge diff (5 files, none RTL) | R829-4 | `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3` |
| Robustness | CLEAN | `ctrl_memory_ledger.py` REFUSED and planted lists; `test_ctrl_memory.log:49-65,191-205` | R829-4 | `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3` |
| Tests | UNCLEAN (F3) | `test_ctrl_memory`, `test_ctrl_firmware` shards 0-3 and `fw_coverage --check` logs; `coverage-provenance.txt`; `nvm_store_gcov_lines.txt` | R829-4 | `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3` |
| Docs | UNCLEAN (F1, F2, F3) | `SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6; the five auto-merged docs and code files (both-sides check); `ctrl_service_budget/README.md`; live PR body; REVIEW READY; docs gates | R829-4 | `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3` |

## Real limits

- **No images linked by me.** I did not rebuild the fixture or platform images. The plans rest on the author's receipts (hash-verified) and my recomputation of every bank and tile from their byte counts with the head's planner. `ctrl_plat` totals (for example 21,392) are not printed in the receipts. I corroborated them through the +152 member delta and the planner accepting the keyed override at rc 0.
- **No dev-side coverage run by me.** A shared-clone setup at `0fb66211` was not permitted in this session. F3 rests on the author's own receipt and the hosted dev job, which agree with each other.
- **RESUME items not located.** I could not find a public text for the "RESUME items 1 to 4" that REVIEW READY cites, so I judged against the five checks of this assignment, which match the author's list.
- **Not run by me:** the full S2 harness, the sweep, builder legs, `behave`, `ctrl_boundary` and the Yosys and Verilator banks (out of scope or not allowed). Those claims rest on the author's receipts.
- **Hosted CI at this head was still queued or in progress** when I read it; I report no hosted result.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Ignored files in the clone.** My gate runs left ignored, untracked build outputs (`__pycache__/`, `configs/generated/*.hex`). Tracked bytes, modes, index and gitlinks are exactly the head's (`receipts/restore-check.txt`).

## Pending manager duties

- Carry F1-F3 to the author.
  - Each is a text or evidence correction: no code, test or generated-artifact change.
  - F1 and F2 touch tracked docs. A fix commit un-covers Docs (and Conformance only if section 5's claims change) and needs re-review at the new head.
  - F3 can be closed in public evidence alone.
- Carry RES-1 to RES-5 to the residue checklist.
- Own the hosted and act acceptance of the exact head. The check runs were queued or in progress when I read them.
- Own the current-dev candidate validation at the merge turn (source base `1d6bf555`, live dev `fa6c094b`), which this review does not claim.

R829-4 FINISHED
