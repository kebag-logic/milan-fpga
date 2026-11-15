[R833] NEGATIVE - exact head eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd

# R833-5: delta review of PR #898 (issue #897), rounds 4-5, `f098f893` -> `eca1b9ca`

- **Head:** `eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd`, tree `3e89a06074625b43bf61ac8c81fdc47151f01a61`. PR #898 is not a draft, base `dev-soft-core`, stacked on #902's round-13 head `234bc149`.
- **Delta reviewed:**
  - `b58a5430`, the sync onto `234bc149`;
  - `2170b22e`, the ledger;
  - `3079bb1e`, GET_AS_PATH's record;
  - `6ef7a8ff`, the AVB_INTERFACE 0 probe fix;
  - `eca1b9ca`, the two restatements and section 13.
  - #902's own commits that the merge brings in are its own lane's, and are judged only where this delta composes with them.
- **Authority:**
  - #897's round-5 ruling, issuecomment-6890824581;
  - #902's rulings, #894 issuecomment-6883864236, -6886633874 and -6888782796;
  - the owner's block-RAM direction of 2026-11-15, #665 issuecomment-6892332745;
  - AGENTS.md sections 6 and 7.
- **Verdict: NEGATIVE, on two MINOR findings.** Both are Tests and evidence weaknesses around one claim: that the pass holds GET_AS_PATH's answered 8-entry record.
  - **F1** is a guard that does not enforce what it states.
  - **F2** is an evidence-publication gap for the round's focus figures.
  - No product code, figure or verdict is wrong. Every STOP condition of the ruling is clear.
  - Everything else in the five checks of the assignment holds. That includes the sync, the ledger, the restatements by the rule, the rows, the load, the pace, the slice and the full pass.
- **Residue:** five items, wording only. Each has its exact fix (RES1-RES5).
- **Suggestions:** carried or new (S1-S4).

## How this round was done

Context was loaded in this order: AGENTS.md, then the ruling and the REVIEW READY (#897 issuecomment-6894799910), then the owner's direction. The diff came next: `git diff 7f50ee6a..eca1b9ca`, focused on `f098f893..eca1b9ca` and the merge's remerge-diff. Then the author's round-5 packet in archive `1ae0a6a4` (`review-evidence/897-r1/author-r5`). Prior public findings (R833-3 and R833-4) were read only after the independent pass.

Probes, all at the exact head:
- The harness self-test and the graders, rerun: `flip_grade.py --check --point 1x1/1if`, `load_grade.py --check` and `--selftest`, `flip_grade.py --selftest`, `tier_grid.py`, `paced_rows.choice`.
- A subset of the AECP campaign, with the table's drift controls: every `face-as-path-*` plant and every SET_CONFIGURATION plant, with an unmutated baseline of their named tests.
- `path_round.py` rerun on the published scratch inputs.
- A disposable mutation probe of the answering-ports arm's `path` port (F1).
- Packet verification against `INDEX.md` and `MANIFEST.json`.
- Every probe restored the exact head: `receipts/clone-clean.txt` shows the HEAD, tree, index, worktree and the five submodule gitlinks all clean, with 0 untracked files.

## The five checks of the assignment

### (1) The sync `b58a5430` onto `234bc149`

`git show --remerge-diff b58a5430` (`receipts/delta/remerge-b58a5430.diff`, `remerge-conflicts.txt`) shows exactly three conflicts. The resolution removes 12 marker lines and leaves 0.

- **`docs/design/SPLIT_CONTROL_MEMORY.md`.** #902's "The one-row edit" section is kept, and #897's "GET_AS_PATH through the face" follows it whole. The #897 text was then still round 3's. `eca1b9ca` restates it, which covers R833-3 R1 and R2, below.
- **`sw/firmware/ctrl/test/aecp_mutants.py`.** `DEFECTS` concatenates both new tables, `aecp_face_mutants.ROWS` (#897) and `aecp_configuration_mutants.ROWS` (#894). At head the table has 308 defects with 308 unique names. It holds all 9 face rows, all 13 configuration rows and all 37 map rows.
- **`sw/firmware/ctrl/test/test_aecp.cpp`** (`:3631-3660`). `Far` keeps both sides:
  - #897's `asp`, `asp_count` and `asked`, with the kind-2 branch of `answer`;
  - #894's `selectors`, pushed for every GSI request before the kind-2 branch.
  - #897's AS_PATH tests close with their `}` before #894's running-check tests (`:3894-4070`).
- **Every plant of both sides is caught by name** (`receipts/probes/aecp-subset-shard{0,1,2}.log`). The run covers the 9 `face-as-path-*` plants and the 13 SET_CONFIGURATION plants: 22 of 22 `[ok]`, each on its own named test.
  - The whole table's drift control (`aecp_mutants.controls`) passes at head.
  - The 10 named tests pass unmutated at two interfaces (`aecp-subset-baseline.log`, rc 0).
  - The author's full campaign gives the remaining totals: AECP 308, control 717 of 717 (`plat-as-path-unavailable` among them) and SRP passing (`receipts/gates/wf/rtl-fast__firmware-*-mutants__ci_step_9*`).

### (2) The ledger `2170b22e` against #901's `8238156d`

`receipts/delta/ledger-vs-8238156d.txt`:

- **`ctrl_memory_ledger.py` and `test_ctrl_memory.py`.** The changed lines of `2170b22e` are byte-identical to `8238156d`'s (same hunk hash).
  - At head, `test_ctrl_memory.py` equals `8238156d`'s.
  - `ctrl_memory_ledger.py` differs only where the trees differ. `PLAT_1X1_2` and `PLAT_8X8_2` are 19,008 and 20,288 here, against #895's 19,072 and 20,352. This tree's `ctrl_plat` is the one `plat_ledger` reads.
- **`ctrl_memory.py`** (`:244-276`). The entry is 60.5, refused at 61.0. Its reason names this tree's 168 B and #897's ruling, item 1, in place of #895's 184 B.
  - The arithmetic holds. 131,240 - 131,072 = 168 B past 60.0, and 133,120 - 131,240 = 1,880 B left.
  - The debt is 60.5 - 56 = 4.5 RAMB36, which is 18,432 B.
  - The planted ledgers move with the entry: its own image at 61.0, the other images at 60.5, and the fixture at the platform's 60.5 (`ctrl_memory_ledger.py:56-73,116-130`).
- **Docs.** Section 3's row and section 5's plan and paragraph are adapted, and `plat/README.md` matches.
- **The author's gates** (`receipts/ledger/`): `ctrl_memory` rc 0, `plat_ledger` PASS (`POINT 8x8-if2: rom 131,240 B ... 60.5 RAMB36 (platform-8x8-two-interfaces) ... PASS`) and `fixtures` rc 0. The ledger is consistent with the owner's 2026-11-15 direction: an image past its entry is reported, not a stop.

### (3) GET_AS_PATH's record (`3079bb1e`, `6ef7a8ff`)

**`arm_path.B_PATH` against the product's `aecp_face.c:258-272` (`path`) and `:142-157` (`gsi`).** The arm's port reads the same words:
- request word 0 is type `9u` (AVB_INTERFACE) and index `n`;
- the count is kind 2, selector 0;
- each entry is kind 2, selector 8, at its ordinal;
- each read goes through `mbx_win_read(i, MBX_WIN_GSI, ...)`.

It answers `min(cap, 8)` entries, the shipped datapath's most. Where it differs, it ignores each read's status and the count read. That is the stand-in the docstring states, since the test SoC never answers a window. `build.py:138,145` puts it in the answering-ports arm's ports.

**The probe.** `scenario.py` sends GET_AS_PATH on AVB_INTERFACE 0 at every interface (`answers.AS_PATH`, `answers.py:103-106`), as `get_avb_info` does. `selftest_answers.as_path` (`:123-140`) holds the command, its four bytes and its length 16, and states SUCCESS in arm B and ENTITY_MISBEHAVING elsewhere. My rerun of the self-test reports 0 failures and 249 of 249 mutants. Among them (`receipts/probes/harness-selftest-as-path-lines.txt`):
- "get_as_path sent on AVB_INTERFACE 9, a descriptor no image has";
- "stated SUCCESS on the image as linked";
- "sent as GET_AVB_INFO".

**`record_classes.py`.** The record is named `GET_AS_PATH` and held as an ordinary record in arm B's `aecp` group (`HELD_IN_ARM_B`). A pass with no answered GET_AS_PATH is refused. The two planted controls pass in my self-test: "the record classes refuse a pass missing arm B's GET_AS_PATH" and "... a GET_AS_PATH over record.aecp". F1 below covers what this guard does not hold.

**The figures, by the rule** (cycles / 100 x 1.05, rounded up to 5 us; recomputed in `receipts/probes/pace-and-rule.txt`):

| Figure | Cycles | By the rule | Against |
|---|---:|---:|---|
| 1x1/1if | 16,208 | 175 us | the ordinary 245 |
| 8x8/2if | 16,397 and 15,966 | 175 and 170 us | 265 |
| arm A, refused | 10,948 and 11,328 | 115 and 120 us | |
| the 18 skipped data-word reads added to 1x1/1if | 17,288 | 185 us | |

- The 8x8/2if 16,397 and 11,328 are receipted (`8x8/records-8x8.txt`, `command 0x0028 status 0 ... 16,397 ... 175 us (aecp)`).
- The 1x1/1if figure is bounded by a published receipt but not stated in one (F2). `compare/records-1x1-restated.txt:101` gives arm B's `aecp` group a most of 19,399 cycles (SET_NAME), so the record is at most 205 us. `restate/record_classes-legs.txt` is `RESULT: PASS` with GET_AS_PATH held.
- **`6ef7a8ff`.** At `3079bb1e` the 8x8 legs were refused NO_SUCH_DESCRIPTOR on AVB_INTERFACE 1, because each image holds one (KNOWN, raised for a decision). The fix sends AVB_INTERFACE 0. The 1x1 scripts are unchanged, since interface 0 is the only interface there. The changed mutant row is caught.

### (4) The restatements `eca1b9ca`

- **`record.aecp` at 1x1/1if: 235 -> 245 us** in both `load_grade.STATED_US` and `STATED_US_DONOR`.
  - The answering-every-port arm's SET_NAME is 23,051 cycles in all 16 groups (`compare/records-1x1-restated.txt`), so 245 by the rule.
  - The attribution receipts measure the same group at `234bc149`: 22,236 cycles (`harness/attribution/atEbase-notice-every-0.txt`).
  - `layout-atEbase-vs-atEhead.txt` shows the code shift.
- **The paced class at 1x1/1if: 300 -> 305 us** (`edit_rows.PACED`).
  - Arm B's accepted SET_CONFIGURATION is 28,752 cycles, so 305 by the rule.
  - With the earlier stub port it is 28,357 (`athead-aecp-fanout.txt`). `layout-athead-vs-mB1.txt` shows the 120 B larger `b_path` moving 159 symbols 304 B.
  - The restatement is driven by the arm's own layout. The rule still requires it, because that record is held.
- **No stated cost is below its measurement.**
  - `compare/compare-1x1-restated.txt` leaves only the two class-attributed raw lines: the largest legal notice, held at 365 by its own class, and SET_CONFIGURATION at 305 of 305 paced.
  - `restate/record_classes-legs.txt` holds long 925 of 975, other 245 of 245, paced 305 of 305, and at 8x8/2if 1540/1650, 210/265 and 585/595.
  - Measured against the stated table (from `compare/costs.txt`): build of one 730 of 735; AECP's timer slot 70 of 70; TICK 50 of 55; SRP record 280 of 280.
- **Rows, load, pace and slice, rerun by me at head**, byte-identical in their tables to the author's receipts (`receipts/probes/flip-1x1.log`, `load-check.log`, `tier_grid-1x1.log`, `pace-and-rule.txt`):
  - `flip_grade.py --check --point 1x1/1if` PASS: R4 13.25, R4L 188.48, ACMP 29.14, ADP 27.49, MAAP 27.61, first 14.67, R5 74.32, R6 72.41, last 127.52 of 130, tx 33.57, txL 48.61 of 49.
  - The load is 0.518 and 0.514 against 0.70.
  - `paced_rows.choice` is 8, with no statement finding.
  - `tier_grid` holds 6 of 420 and chooses the built 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2, margin +0.0080.
  - The load self-test refuses 26 of 26 and the flip self-test 585 of 585.

### (5) The full pass

- **Packet integrity** (`receipts/packet-verify-author-r5.txt`). 579 INDEX rows, with 0 missing and 0 mismatched. 4 rows differ only by the manifest's recorded path redaction, with the original hash equal to the INDEX row. The 621 manifest entries all match their published hashes.
- **Workflows** (`receipts/gates/verify-table.md`, counted by me): 365 steps, 139 at rc 0, 226 NOT RUN with a stated reason, 0 bad.
- **Lane gates** (`receipts/gates/lane/summary`). Every gate is at rc 0 except 4 by-design exits: `rows_tiers_report`, `flip_check`, `flip_check_8x8` and `flip_check_1x1_as_built`. Each refuses the same rows as at `234bc149` (`exits-1-vs-234bc149/`, compared by me row for row).
- **The Verilator sweep.** 64 of 65 suites passed in the shards. `milan_dp` timed out under contention and passed on its rerun (`receipts/sweep/rerun-milan_dp`). I take the sweep from the author's receipts, not from a run of mine.
- **CPU-harness legs at the final head.** Each ELF equals its measurement build (`harness/final-eca1b9ca/images.txt`, 6 of 6 `identical`).
- **The answered notice.** The scratch arm `cl-path5.diff` and its inputs are published, and `path_round.py` reproduces from them. One notice is 28,098 cycles, admitted at 34,000. Three are 65,576, admitted at 85,000 (`receipts/probes/path_round-rerun.txt`).

### (6) R833-3's R1 and R2, and earlier findings

The prior findings were read after the independent pass.

| Prior finding | Status at `eca1b9ca` | Evidence |
|---|---|---|
| R833-3 F1 (MINOR): scratch receipts unpublished | Resolved at R833-4. This round's answered-notice scratch is published and reproduces | `harness/scratch/cl-path5.diff`, the inputs, `receipts/probes/path_round-rerun.txt` |
| R833-3 R1 (RESIDUE): "at the merge of `5b264bf2`" as current | **Resolved** | `SPLIT_CONTROL_MEMORY.md:490` "At the merge of #894's tiers at its round-13 head, `894-tiers` `234bc149`"; `:2530` "On the merge of `894-tiers` `234bc149`" |
| R833-3 R2 (RESIDUE): 16 vs 18 data-word reads | **Resolved** | `SPLIT_CONTROL_MEMORY.md:2532` "The nine answers' two data words each (18 reads)" |
| R833-3 R3 (RESIDUE): PR body reviewer lines | Resolved. Its round-5 analogue is RES4 | PR body lines 31-37 |
| R833-3 S1: `ctrl_loop.h` 725 us | Resolved by #902's restatement | `ctrl_loop.h:323,328` 735 us; compare build of one 730 of 735 |
| R833-3 S2 / R833-2 F3: INDEX not regenerated after redaction | Retained as S2 | `receipts/packet-verify-author-r5.txt`, the 4 rows |
| R833-1 S1: the answering arms' `path` stand-ins answer an empty sequence | **Resolved for arm B** (`arm_path.py`). Retained as S3 for the answering-every-port arm, whose `a_path` still stands in (`build.py:195-227`) | |
| R833-2 F4: `build.py:124-126` comment widths | Retained (S4). The lines are re-wrapped no better at `:122-134` | |
| R834-1 SUGGESTIONs: no executable check of the kind-2 read on the split RTL; a datapath reset between the count and the entry reads | Retained, unchanged. No `hdl/` file and no product-firmware hunk of this lane changed | `receipts/delta/own-side-firmware.txt` |

## Findings

### F1 - MINOR - Tests - `tb/verilator/ctrl_service_budget/record_classes.py:196-198` (and the module docstring `:26-28`) - the GET_AS_PATH guard holds a SUCCESS, not the answered read it states

**Authority and evidence:**
- Ruling item 4 asks for GET_AS_PATH's record "measured in a tracked answering-ports group ... and held as an ordinary record".
- The guard says it refuses a pass whose arm B ran no GET_AS_PATH "answered SUCCESS in aecp, whose answered read no other arm reaches". The docstring concludes that the held record "is the answered GET_AS_PATH's".
- The check is `r.command == GET_AS_PATH and r.status == 0` alone.
- The port that answered before `arm_path.py` also answers SUCCESS. That port read nothing and answered an empty sequence (`*count = 0; return true;`).
- Probe (`scripts/probe_stub_path.sh`, `receipts/probes/stub-path/`): `build.py`'s `arm_path.B_PATH` was replaced by that stub. Both suites still pass:
  - `run.py --self-test`: 0 failures;
  - `record_classes.py --selftest`: 13 of 13 controls refused, rc 0.
- No check reads the response's entries or its control_data_length of 80. `answers.aem(0x0028, ...)` states the status alone.

**Impact:** a merge or edit that loses the reading port would leave every pass green. A stub-like edit of `B_PATH` would have the same effect. GET_AS_PATH's held record would then be an empty answer's, about 5,000 cycles under the answered read (10,948 to 11,328 refused vs 16,208 answered). That is the unseen-drift failure the record classes exist to stop (the module docstring's #894 case).

**Required outcome:** a pass is refused unless arm B's GET_AS_PATH record at 1x1/1if is the answered 8-entry read. One way is to check its response's control_data_length (80) or entry count, as read from the response frame `read_leg` already parses. Another is to pin `build.py`'s port to `arm_path.B_PATH` in the self-test. A planted control must hold it: a GET_AS_PATH answered SUCCESS with no entries, refused by name.

**Verification:** rerun `scripts/probe_stub_path.sh`. It must fail by name, either in the self-test or on a regraded arm-B leg. The head's arm-B legs must still pass.

### F2 - MINOR - Docs, Tests - `docs/design/SPLIT_CONTROL_MEMORY.md:2532`; REVIEW READY (#897 issuecomment-6894799910); packet `author-r5/receipts/` - the round's focus figures at 1x1/1if are stated as measured, with no published receipt

**Authority and evidence:**
- The round's focus is GET_AS_PATH's record at 1x1/1if. Section 13 and the REVIEW READY state, as measured:
  - 16,208 cycles (175 us);
  - arm A's refused 10,948;
  - the 8x8/2if interface-1 figure 15,966;
  - "the response carries the eight entries, a control_data_length of 80".
- Not one of these figures is in any published receipt; I searched every receipt in the packet.
- The 1x1 harness tables give the probe's response span (23,858), not the record. `records-1x1-restated.txt` lists only each group's most.
- The 8x8 figures 16,397 and 11,328 are receipted (`8x8/records-8x8.txt`).
- The bound is receipted: at most 19,399 cycles, 205 us, in arm B's `aecp` group, and `record_classes` PASS. So the verdict on the class holds. The figure itself and the 8-entry answer, which F1 shows no check holds, rest on prose.
- AGENTS.md section 6, Docs: "The PR and Issue contain enough evidence for another cold reviewer". The precedent is R833-3 F1, an unreceipted design-doc measurement graded MINOR.

**Impact:** a cold reviewer cannot confirm the 175 us record or that the measured response carried 8 entries, so the record's identity cannot be checked from public state.

**Required outcome:** publish a receipt from the head's arm-B and arm-A 1x1/1if legs (`mB1`/`fB1`, `mA1`/`fA1`) and the 8x8/2if interface-1 leg. Per command and status it must list each record's cycles, as `records-8x8.txt` does, with each GET_AS_PATH response's control_data_length. Add a manifest entry for it. No source commit is needed for F2.

**Verification:** the receipt shows `command 0x0028 status 0 ... 16,208` at 1x1/1if, 15,966 at 8x8/2if interface 1, `status 10 ... 10,948` in arm A, and a control_data_length of 80.

## Residue (wording only; does not affect the verdict or any lens)

- **RES1 - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2557`.** This bullet's load figures were updated in this delta. It still states "under the tiers every 1x1/1if row holds by every source at the rule's 950 us slice, R4 13.10 ms" as current, but at head R4 is 13.25 (the table row at `:2388`).
  - **Exact fix:** "R4 13.25 ms (13.10 at the final pass's restatements)".
- **RES2 - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2526`.** The paragraph reads "At 950 us every 1x1/1if row holds by every source (the table [above](#the-tiers)): R4 13.10 ms, the last queued notice 127.21, ACMP 28.95 and txL 48.43; the load is 0.516 and 0.512". The table it points to now carries GET_AS_PATH's row. The delta already put FR_NFR 3.4.1's twin sentence in the past tense ("held").
  - **Exact fix:** "At 950 us every 1x1/1if row held by every source ... the load was 0.516 and 0.512 (with GET_AS_PATH's restatements, [below](#get_as_path-through-the-face))".
- **RES3 - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2532`.** The text reads "175 us by the rule, within the 235 us of an ordinary record", but the same subsection restates that class to 245.
  - **Exact fix:** "within the 245 us of an ordinary record (235 before the restatements below)".
- **RES4 - PR body - PR #898 body line 35.** It reads "round 5: one delta review ... not yet started", but the review started publicly at issuecomment-6894859654.
  - **Exact fix:** name R833-5 at `eca1b9ca` and its verdict once published.
- **RES5 - REVIEW READY - #897 issuecomment-6894799910, "Lane gates".** It says the by-design exits refuse "as built at 1x1/1if R4, first and last". `flip_check_1x1_as_built_exits_1.log` refuses R4 and last only. The first queued notice is 20.00 of 20 (+0.00), at its bound and not refused, as at `234bc149`.
  - **Exact fix:** "as built at 1x1/1if R4 and last (the first queued notice at its 20 ms bound)".

The comment rule is clean. The added source lines since `b58a5430` contain no lane labels, review rounds, reviewer IDs or issue-comment IDs (`receipts/delta/comment-rule-scan.txt`, 0 matches).

## Suggestions (optional; no lens effect)

- **S1 - Tests.** `arm_path.B_PATH` answers `min(cap, 8)` whatever the count read returned, and ignores each read's status. A one-line comment saying that this is the stand-in, as the docstring does, would help at the code site. Optionally, also use the count word the way the product does (`n > capacity` refused).
- **S2 - Docs (packet, retained from R833-2 F3 and R833-3 S2).** `author-r5/INDEX.md` still carries pre-redaction hashes for the 4 path-redacted workflow logs. Separately, `STAGING-NOTE.md` describes one redaction, while `MANIFEST.json` records 21 `path_redacted` files in `author-r5` (4 logs and 17 scripts). Regenerating the INDEX, or a note naming all 21, would remove the ambiguity.
- **S3 - Tests (retained from R833-1 S1).** The answering-every-port arm's `a_path` (`build.py:195-227`) still answers without a read. Its answered notice is measured only in the uncommitted scratch arm `cl-path5`. A committed reading port there, like `arm_path.py`, would make the notice's read part of every pass.
- **S4 - Docs (retained from R833-2 F4).** The comment wrapping at `build.py:122-134` is ragged.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 6890824581 items 1 and 4 against `2170b22e`/`3079bb1e`/`eca1b9ca`; `arm_path.py:19-37` vs `aecp_face.c:142-157,258-272`; `answers.py:103-106` (GET_AS_PATH 0x0028, IEEE 1722.1-2021 7.4.41.1); `selftest_answers.py:123-140`; the lane's product-firmware hunks unchanged since round 3, so the response on the wire is unchanged (`receipts/delta/own-side-firmware.txt`); the stated-cost rule recomputed (`pace-and-rule.txt`); `record_classes-legs.txt` | R833-5 | `eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd` |
| RTL | CLEAN | `git diff --name-only 234bc149 eca1b9ca -- hdl` empty, and no `hdl/` change on the lane's side since round 3 (`own-side-firmware.txt`); the composition of `aecp_face.c` (#897 `path`, #894 `stream` running check) as separate functions, with the hunk hash unchanged; `ctrl_memory.py:244-276` widths and limits (60.5/61.0, 133,120 B) | R833-5 | `eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd` |
| Robustness | CLEAN | the product `path` failure paths (count unanswered, entry unanswered, count past capacity), caught by their plants after the merge (`aecp-subset-shard*.log`: `face-as-path-count-unanswered-ignored`, `-entry-unanswered-ignored`, `-truncated-at-its-bound`, `-bound-off-by-one`); the ledger's planted refusals at 61.0 and the cross-image cases (`ctrl_memory_ledger.py:56-73,116-130`; `ledger/ctrl_memory.log`); AVB_INTERFACE 9 refused in the scenario self-test | R833-5 | `eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd` |
| Tests | UNCLEAN (F1 MINOR, F2 MINOR) | `record_classes.py:177-275` and the stub probe (`receipts/probes/stub-path/`); the AECP subset 22 of 22 and the table drift controls; the harness self-test 249 of 249 at head; the load 26/26 and flip 585/585 self-tests; the merged `test_aecp.cpp:3631-3660,3894-4070` with its baseline; the by-design exits row for row | R833-5 | `eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd` |
| Docs | UNCLEAN (F2 MINOR; RES1-RES3 wording) | `SPLIT_CONTROL_MEMORY.md` sections 3 and 5 (`:135-146,266-275,486-500`) and section 13 (`:2356-2390,2505-2541,2557`); `FR_NFR.md:383`; the harness README `:186`; `plat/README.md:110-140`; `edit_rows.py:34-40`; `load_grade.py:132-186`; PR body; REVIEW READY; packet INDEX/MANIFEST | R833-5 | `eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd` |

**What clears the two MINORs:**
- **F1** needs a source commit, which un-covers Tests; re-review the new head under Tests.
- **F2** needs only a published receipt. A Docs re-check at the same head clears it if no source changes.
- The residue does not hold a lens.

## Real limits

- I did not build or run the CPU service budget harness (SoC, CPU netlist, image). The figures 16,208, 15,966, 10,948, the 8-entry response, 23,051 and 28,752 come from the author's receipts and prose, not from a run of mine. F2 covers the ones with no receipt.
- I reran only a 22-plant subset of the AECP campaign, with its drift controls. The control (717) and SRP campaigns, the full AECP 308, the workflow replay, the lane gates and the Verilator sweep are taken from the author's published receipts.
- I ran no Docker, act, builder, Yosys or Vivado. The hosted contexts at the exact head were incomplete when I looked (45 success, 1 skipped, 13 Verilator shards in progress). The manager owns hosted and act acceptance.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- No manager source bank runs at this head, and none is claimed.

## Pending manager duties

- Validate the current-dev merge candidate (source base `7f50ee6a`, live `dev` `6b66f66d`), with its builder and native banks.
- Ruling item 3: grade the composed #901 + #898 platform image at 8x8/2if against 133,120 B after #901's review head. Over 60.5 goes to the owner.
- The order of merges #902, #901, #898. #902 has moved to `478ff78c`, and its trial merge conflicts in FR_NFR 3.4.1's paced paragraph.
- Route the one-AVB_INTERFACE-per-image question at two interfaces for its separate decision. Report the 8x8/2if datapath event costs over their statement (#890). Both are known, not findings.
- Carry RES1-RES5 to the residue checklist.

R833-5 FINISHED
