[R837] NEGATIVE - exact head 234bc149ff888eb96659ecaaa5ce6e4fb27319d4

R837-7: the internal, cleared-context delta review of PR #902 (issue #894, Mark II split tier rows), rounds 12 and 13. The delta runs from `9606b3a9` (round 11; R837-6 and R838-6 both NEGATIVE) to `234bc149`, tree `9b54edcc9bd235b734ad559291cdf1ec6da4716c`: fifteen one-line commits by the author over 24 files.

## Verdict

- **NEGATIVE, on one MINOR finding: R837-7-F1 (Docs).** Round 12 moved the build of one to 735 us. Round 13 moved the slice to 950 us and the load to 0.516 / 0.512. Four current-tense figures were not refreshed:
  - `SPLIT_CONTROL_MEMORY.md:2197` (section 13) still states the build of one at 725 us;
  - `sw/firmware/ctrl/srp/README.md:238` still states tx at 33.01 ms at the 900 us slice;
  - the PR body's closure of R838-6-F2 (line 203) quotes the load as 0.515 and 0.511, round 11's figures;
  - the PR body's findings-table row for R838-6-F2 (line 282) gives the current summary as R4 13.05 and the last queued notice 132.71 over 130, which are round 12's figures.

  This is R838-6-F2's cause again: stale current figures after the model moved. That finding was closed site by site, not by a sweep.
- **Everything else in the focus list checks out at this head.** I verified it against the code, the signed packet and my own runs:
  - the SET_CONFIGURATION cut, the pace stamp and the paced class;
  - `record_classes.py` and its 11 controls;
  - the SRP drain constant and its check;
  - the four restatements by the rule;
  - the survey over arm A, the answering-every-port arm and B1F;
  - the slice as the rule's choice, with the self-tests reading the header;
  - every 1x1/1if row and the load;
  - the 8x8/2if carry by hash and the `hooks.py`-only carry;
  - the hooks self-test fix.
- **Item 5 (no late-acknowledged completion on the product port) is a proof from the code, not an assumption.** It has one precondition it does not name: the sys and datapath clock domains come off one PLL with a joint reset. I checked that precondition in `sw/litex/milan_soc.py:282-288` (SUGGESTION R837-7-S1).
- **No new comment-rule instance in the delta's source comments.** One wording residue (R837-7-R1) and three suggestions are recorded. R837-6 and R838-6's findings are each resolved at their cause, except R838-6-F2, which recurs as R837-7-F1.

## Method and scope

- **Context, in order:** AGENTS.md, CONTRIBUTING.md and docs/README; then the #894 rulings 6883864236 (round 12), 6886633874 (the SRP drain) and 6888782796 (round 13); then REVIEW READY 6890460677.
- **Code:** `git diff 9606b3a9..234bc149` and its history; then the author packets `author-r12` and `author-r13` at archive `9222da67`; then the live PR body.
- **Prior public findings:** R837-6 (6884063444) and R838-6 (6884009601), read only after my own pass over the diff. No private author material, lane scratchpad or other reviewer's round-13 report was read.
- **Clone:** detached at the exact head. Two disposable plants in `ctrl_loop.h` were restored by `git checkout`, and their sha256 was rechecked. At the end the worktree and index equal HEAD and every gitlink is unchanged (`receipts/clone-integrity.txt`).

## Evidence verification

- **Packet integrity:** all 394 `author-r12/` and `author-r13/` files match the archive's `MANIFEST.json` published sha256, and none is unlisted (`receipts/carry-and-index-check.txt`, `scripts/carry_and_index_check.py`). The archive commit itself is not GPG-signed (`%G?` = N); the integrity claim rests on the manifest.
- **INDEX against the files (R837-6-S1):**
  - Every receipt row matches.
  - Five script files per packet differ from their INDEX rows. In every case the INDEX hash equals the manifest's `original_sha256`, with `path_redacted: true`.
  - So the author's packet now indexes after sanitizing, and the remaining difference is the archive's own publication-side redaction, which the outer manifest records. See R837-7-S3.

## My own runs at the exact head (`receipts/`)

| Command | Result |
|---|---|
| `record_classes.py --selftest` | 11 of 11 planted controls refused, rc 0 |
| `load_grade.py --selftest` / `--check` | 26 of 26; HELD 0.516 at the pin and 0.512 in the second column, PASS |
| `rows_tiers.py --selftest` | 1,033 of 1,033 refused, rc 0 |
| `tier_grid.py --point 1x1/1if` | CHOSEN 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2, +0.0116 (the built design) |
| `flip_grade.py --check --point 1x1/1if` | PASS. R4 13.10, R5 74.07, R6 69.86, first 14.66, last 127.21 (of 130), R4L 188.48, ACMP 28.95, ADP 27.30, MAAP 27.42, tx 33.38, txL 48.43 (of 49) |
| `ctrl_service_hooks/run.py --self-test` | 28 of 28 checks; 96 of 96 mutants caught |
| `docs_check.py` | 0 findings over 219 md files |
| AECP app arm, 1 and 2 interfaces (`scripts/config_mutants_probe.py`) | 147 of 147 tests pass at each count |
| The 13 `aecp_configuration_mutants.py` rows planted on a copy | 13 of 13 caught by name |
| PLANT `CTRL_LOOP_SLICE_US` 900u at one interface, then `rows_tiers.py --selftest` | refused: "ESCAPED the built design's slice not the rule's", 1,032 of 1,033, rc 1. `tier_grid` still chooses 950. Restored |
| PLANT `CTRL_LOOP_SRP_UNIT_US` 250u at one interface, then `load_grade.py --check` | "OVER 1x1/1if: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US 250 us, not the load gate's record.srp 280 us", FAIL. Restored |
| `scripts/record_classes_unanswered_probe.py` | an over-cost record in arm B's `aecp-fanout` that answers after the next record starts is reported, not held (R837-7-S2) |

Two runs I could not complete:
- **`check_em_dash.py`** could not judge: the pinned Markdown renderer is not installed here, and shared installs are not allowed. The author's lane part a receipt at `234bc149` gives `em_dash rc=0`.
- **The whole firmware unit gate** run natively did not finish within my 10-minute foreground window (`receipts/firmware-unit-head.txt`, rc 124, no verdict). I ran the AECP arms it contains directly instead (above).

## Checks against the assignment

### (1) The SET_CONFIGURATION cut (`f275b619`)

- **The running check:** `running()` (`aecp_commands.c:125-130`) observes through `observe()` with `{.brief = true}`. The face reads selector 0 alone when `brief` is set (`aecp_face.c:169`).
  - Bound comes from the ACMP view (`ctrl_app_aecp.c:52-55`) and running from the SRP licence (`aecp_face.c`, `mbx_pub_licensed`). So the one word is only the proof that the window answers.
  - A silent window still gives ENTITY_MISBEHAVING.
- **`aecp_stream_read`** still zeroes and reads whole. It has three callers: GET_STREAM_INFO, `aecp_maps.c:111` and the app wrapper. All of them read whole, and the brief flag survives the wrapper.
- **Statuses and their order are unchanged:**
  - the order is length, `any_running`, foreign lock, then index range (`aecp_commands.c:186-195`);
  - the response field is unchanged;
  - the notify rule is unchanged: a note only when the index moved or the override was not yet set.
- **The stream entries:** they are written only when `changed`'s index is 1, that is, when the index moved (`aecp_face.c:119`).
  - Every other consumer of a CONFIGURATION change ignores its index (`aecp_nvm.c:138`).
  - The wait path re-notes with the stored index (`aecp.c:918`). So a moved configuration that completes, or stays undone, republishes every stream of the configuration in force.
- **No wire-visible change against Milan v1.2 5.4.2.5 or IEEE 1722.1-2021 7.4.7.**
- **The record, from the traces:** 33,724 to 28,509 cycles at 1x1/1if and 78,332 to 55,377 at 8x8/2if, at `f275b619` (PR body section 2).
  - On the final images it is 28,376 at B1F and 56,474 at B8F (`compare-1x1.txt`, `compare-8x8.txt`, `record-classes-ed0df35b.txt`).
  - The 8x8/2if move from 55,377 to 56,474 is the pace stamp's code. The two-interface images are identical from `30a01422` (round 12) to `c274b9f5` by hash.

### (2) The pace stamp and the paced class (`fe0cef5b`, `e4d80a8a`)

- **The stamp:** `a->edited_ms = a->now` sits in the accepted branch only (`aecp_commands.c:196`). It covers an accepted SET naming the index in force, as the ruling's "an accepted SET_CONFIGURATION" reads.
- **Firmware plants catch it:**
  - `configuration-unpaced` and `configuration-paced-when-refused` are caught by `Mailbox.AnAcceptedConfigurationHoldsTheNextRecordForThePace` on my run;
  - the test checks 1 to 7 ms held and taken at 8 ms, never dropped;
  - a refused SET (STREAM_IS_RUNNING) holds nothing.
- **The paced class:** `edit_rows.PACED` (`edit_rows.py:38`) takes the dearer member: 260 against 300 at 1x1/1if, so 300; 325 against 595 at 8x8/2if, so 595. Both are at or above their measurements by the rule:
  - 28,376 cycles is 297.9 by the rule, which states 300;
  - 56,474 is 593.0, which states 595;
  - the one-row edits are 245 against 260 and 30,124 (316.3) against 325.
- **The planted ordinary-charge control:** "an unpaced SET_CONFIGURATION charged as ordinary" fails by name in both `edit_rows.controls` (within the 1,033) and `record_classes.controls` ("SET_CONFIGURATION not paced").
- **`record_classes.py`:**
  - It holds the answering-ports arm's `aecp-fanout` SET_CONFIGURATION and SET_STREAM_INFO records whatever their class (`held`, `:134`).
  - It refuses a pass whose 1x1/1if answering-ports leg lacks an accepted SET_CONFIGURATION or a SET_STREAM_INFO (controls 7 and 8).
  - It names a record only by a response committed at or after its start and before the next record's (`named`, `:102`; control 11, "command unanswered"). That resolves R837-6-S2 at its cause.
  - My probe shows one residual gap, given as SUGGESTION R837-7-S2.
- **Over every leg:** `record-classes-ed0df35b.txt` gives RESULT PASS, with arm A's four quarters (96 groups), E1's 16 groups and B1F. The 1x1/1if paced class is held at 28,376 (300 of 300).

### (3) The SRP drain (`1c0ca94b`, `a47cd3f2`)

- **The constant:** `CTRL_LOOP_SRP_UNIT_US` is `(MBX_N_IF == 1u ? 280u : 365u)` (`ctrl_loop.h:284`). That equals `max(record.srp)` over both load-gate columns at each point: 280 and 280 at 1x1/1if, 365 at 8x8/2if.
- **The check:** `srp_unit()` (`load_grade.py:268`) is part of `--check`'s findings. It plants 250 at one interface and 300 at two in `srp_unit_controls`. My in-tree plant of 250 fails `--check` by name.
- **Who reads it:**
  - `ctrl_loop.c:201` and `:322`;
  - `test_port_loop.cpp:1408-1473`, the drain test, which reads the constant;
  - `loop_step_mutants.py:222`, which anchors on the limit expression. That anchor is unchanged, so the control campaign's 716 of 716 at `ed0df35b` carries by identity.
- **Its measurement:** 26,366 cycles, 280 by the rule, in `E1/notice-every-2`, at 280 of 280 (`compare-1x1.txt`).

### (4) The four restatements and the survey (R837-6-F1)

Each is at or above its measurement by the rule:

| Restatement | Measurement | By the rule | Stated |
|---|---|---|---|
| Build of one | 69,635 | 731.2 | 735 (`ctrl_loop.h:328`, both `load_grade` columns' `item.mrpdu`/`build_one`, `poll_grade` `mrpdu`) |
| TICK | 4,784 at `a47cd3f2` | 50.2 | 55, both columns |
| AECP timer slot | 6,206 | 65.2 | 70, both columns |
| LINK | 14,715 | 154.5 | 155 (`rows_grade.ROW_COSTS`) |

- **The TICK at the final image:** 4,692 cycles, 50 by the rule against the stated 55. That is above the rule, not a defect.
- **The survey reads every stated table over every leg:**
  - `compare-1x1.txt` lines are prefixed by leg: `A1/` to `A4/` (arm A's 96 groups), `E1/` (the answering-every-port arm's 16 groups) and `B1F/`.
  - The tables read: `load_grade.GRADED`, `load_grade.STATED_US`, `poll_grade.STATED_US[1]`, `poll_grade.record_us`, `whole_grade.stated_us(1)`, `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US` and `LONG_NOTICE_US`.
  - The only OVER lines are the class lines, each within its own class:
    - A2's REMOVE at 245, paced (300);
    - B1F's SET_CONFIGURATION at 300, paced (300);
    - B1F's largest legal notice at 365, held to `aecp_long` 365.
  - `compare-8x8.txt` reads the 8x8 legs. Its OVER lines are known and reported-only: the build of one at 1,530 against 1,215 (owed to #872), the largest notice, and the paced SET_CONFIGURATION against ordinary.
- **R837-6-F1 is resolved at its cause.**

### (5) The slice (`c274b9f5`)

- **The header:** `ctrl_loop.h:263-279` states the rule and 950 us.
- **The self-tests read the header and the rule, with no literal:**
  - `selftest_round.slice_checks` compares against `rows_tiers.ruled(scenario.ROOT)` (`selftest_round.py:110`);
  - `rows_tiers.tree_controls` reads the stated line by regex and holds `ruled(root) == built` (`rows_tiers.py:882`);
  - my 900 us plant is refused by name.
- **`CTRL_LOOP_BUILD_MOST`** is `(SLICE >= BUILD_PASS ? 2 : 1)` (`ctrl_loop.h:332`). 950 < 1,010, so it is 1.
- **`tier_grid`** chooses the built design (10 of 420 hold, +0.0116).
- **The rows:** every 1x1/1if row by every source is within its bound (table above). The load is 0.516 / 0.512.
- **The pace and the joins:**
  - the pace is 8 by its rule (`pace-slice-ed0df35b.txt`);
  - joins are 185.486 to 190.147 ms over 16 legs and 187.994 to 190.021 in arm A (`joins.txt`; arm A logs' `JOINS` lines), all within 181 to 239.
- **The image delta from round 12:** only the four one-interface images' `ctrl_loop.o`, ELF and binary change, 12 of 332 files.

### (6) Item 5, no late-acknowledged completion

I checked the chain link by link:
1. KL_mbx_cdc's commit is a rising edge crossed by `cdc_pulse`. The datapath takes the bus on the destination pulse, with no ready signal. The same pulse is the acknowledgement's source, crossed back (`KL_mbx_cdc.sv:265-280`).
2. `mbx_face_commit` reads `F_STATUS` up to `MBX_FACE_ACK_CYCLES + 1` times after GO, each read at least one bus cycle (`mbx.c:337-350`). So it outwaits contract 2.3's 64 cycles.
3. `sim_split.cpp` measures 2 polls on the composed split (`milan_dp-face-lines.txt`).
4. `publish` owes an interface only when it is already owed, when a change waits, when the block is busy or when a commit is not OK (`aecp_face.c:79-101`).

So with the datapath clock running and out of reset, no commit is late and the core's wait is unreachable. That one precondition is not stated in the receipt. It holds by construction: `cd_milan` is a clock output of the same PLL as `cd_sys` (`milan_soc.py:282-288`), so the two reset domains are released, and asserted, by the same lock. I judge item 5 a proof from the code (SUGGESTION R837-7-S1: name the precondition). The fault path stays tested by `Face.ALateCommitIsOwedAndPublishedAgainWhole`.

### (7) The carries

- **The 8x8/2if legs:**
  - 6 of 6 harness ELFs are identical (`harness-elf-sha256.txt`).
  - 166 of 166 two-interface image files are identical between `image-sha256-30a01422.txt` and `image-sha256-c274b9f5.txt`; my script recomputes this from the receipts.
- **`ed0df35b` to `234bc149`:** `git diff --stat` shows only `tb/verilator/ctrl_service_hooks/hooks.py`. `git grep` finds no reader of `ctrl_service_hooks` or `hooks.py` outside its own directory, so no workflow job or sweep suite reads it.
  - Its one reader, the hooks self-test, ran at `234bc149` in lane part a (28/28, 96/96) and again on my run.
  - `verify_wf-combined.txt` gives 139 ran rc 0, 226 not run with a reason, 0 bad, over the two heads. Each per-head file's "bad" rows are the other head's steps.
- **The sweep:** four shards, each command rc 0, at `ed0df35b`.
- **The hooks fix:** the face plant's anchor `publish(f, i, settings, i == home ? stream : NULL, every);` occurs once in `aecp_face.c`. The replacement keeps `every` referenced.

### (8) The R837-6 and R838-6 findings at this head

| Prior finding | At `234bc149` |
|---|---|
| R837-6-F1 (MINOR) | Resolved (4 above) |
| R838-6-F1 / R837-6-R2 (per-image rom) | Resolved. Section 13's per-image deltas (+224 in each 1x1 image, +208 in each 8x8 image; round 12's +216, and +224 in the 1x1/1if fixture) match `author-r12/receipts/images/rom-per-image.txt` row by row. 8x8/2if: 130,920 of 131,072, 152 B spare |
| R838-6-F2 (stale current figures) | The named sites are fixed: section 13's summary gives R4 13.10 (`:2525`), and the PR validation example gives 0.516 and 0.512. **The cause recurs, as R837-7-F1** |
| R838-6-R1 / R837-6-R1 (rounds and lanes in source comments) | Resolved. The cited lines name the issue, the cut and the measured commits. A scan of every added source-comment and docstring line in the delta finds no review round, lane, reviewer ID or issue-comment ID |
| R838-6-R2 / R837-5-R1 (historical margins) | Resolved ("The margins in round 30's measurements"; "at this head" dropped) |
| R838-6-R3 (identity wording) | Resolved (PR body: "none ... changes the compiled firmware output, as the image and object identity receipts show") |
| R837-6-S1 (INDEX before sanitizing) | Resolved at the author's packet. The residual is publication-side redaction (S3) |
| R837-6-S2 (naming by a later response) | Resolved by `named()` and control 11. The residual gap is S2 |

## Findings

### R837-7-F1 - MINOR - Docs - current-tense figures left stale by the round-12 and round-13 moves (R838-6-F2's cause again)

- **Artifacts** (`receipts/stale-figures.txt`):
  - `docs/design/SPLIT_CONTROL_MEMORY.md:2197`, section 13: "a build of both ... or a build of one is stated at 975, 1,010 and 725 us at 1x1/1if". `ctrl_loop.h:328` states 735, which `99626ee4` set.
  - `sw/firmware/ctrl/srp/README.md:238`: "By every source it is 33.01 ms there at the 900 us slice". The head gives tx 33.38 ms at the 950 us slice (`flip_grade --check`). Round 13's docs commit `ed0df35b` edited this README for 950 us elsewhere.
  - PR #902 body, line 203 (section 8, "No stale current figure"): "this body's validation examples give this head's load (`load_grade.py --check`: 0.515 and 0.511)". The head gives 0.516 and 0.512, as the body's own line 324 does.
  - PR #902 body, line 282 (findings table, the R838-6-F2 row): "its current summary (R4 13.05, the last queued notice 132.71 over 130)". At the head the current summary gives R4 13.10 (`:2525`), and the last queued notice is 127.21 within 130. 13.05 and 132.71 are round 12's 900 us figures. The row also cites `:2524` for `:2525`.
- **Authority:**
  - #894 issuecomment-6888782796, item 3: rerun on the rebuilt images, with the documents at the rule's slice;
  - #894 issuecomment-6881287231: every stated figure the head's own;
  - the assignment's item 8: no stale figure in section 13 or the PR body;
  - R838-6-F2, the same defect class, which that reviewer classified MINOR because the correction changes figures.
- **Impact:**
  - A cold reader of section 13 takes 725 us as the build-of-one statement the model reads.
  - A reader of the SRP README takes 33.01 ms at 900 us as the tx row.
  - The PR's finding-closure evidence misreports the head's load and summary.
  - No bound is broken. The code, tables and tests carry the right figures.
- **Required outcome:** sweep every current-tense figure the round-12 and round-13 moves touch: the build of one, the TICK, AECP's timer slot, LINK, the SRP drain, the slice, the load and the rows. Do it in section 13, FR_NFR 3.4.1, the READMEs and the PR body, and make each either the head's figure or explicitly historical. At minimum:
  - `:2197` should read 735;
  - `srp/README.md:238` should read "33.38 ms there at the 950 us slice" (with "33.01 at 900 us under round 12's costs" as history if kept);
  - PR line 203 should read 0.516 and 0.512;
  - PR line 282 should read R4 13.10 and the last queued notice 127.21 within 130 at 950 us, citing `:2525`.
- **Verification:** compare each site with `flip_grade.py --check --point 1x1/1if`, `load_grade.py --check` and `ctrl_loop.h` at the new head. A reviewer greps the four sites and the moved figures (725, 33.01, 900 us, 0.515, 13.05, 132.71) for current-tense use.
- **Lens attribution:** Docs alone. No test, executable claim or measurement is wrong. The Tests lens examined the tests and receipts themselves.

### R837-7-R1 - RESIDUE - Docs - `ctrl_loop.h:322` attributes the cut to the pace commit

- **Artifact:** "69,635 under #894's SET_CONFIGURATION cut (fe0cef5b)". The cut is `f275b619`. `fe0cef5b` is the pace stamp, the image where the figure was measured. `load_grade.py` says "(f275b619, paced at fe0cef5b)".
- **Exact fix:** "and 69,635 under #894's SET_CONFIGURATION cut, measured at fe0cef5b, the same build moved by the cut's code". No token or figure changes.

### R837-7-S1 - SUGGESTION - Docs, Robustness - item 5's receipt leaves its clock and reset precondition implicit

`receipts/item5-no-late-completion.md`'s chain holds because the datapath clock is a clock output of the sys PLL, with a joint lock and reset (`milan_soc.py:282-288`). Suggested outcome: name that link in the receipt and in the face's contract note, so a later independent datapath reset or clock is seen to reopen the late-completion path.

### R837-7-S2 - SUGGESTION - Tests, Robustness - an unanswered over-cost record in arm B's `aecp-fanout` is reported, not held

- **Artifacts:** `record_classes.py:134` (`held`) and `scripts/record_classes_unanswered_probe.py`.
- **Evidence:** a record that answers after the next record starts is named unanswered, so its command is None. In the answering-ports arm's `aecp-fanout` it is then neither paced nor in `HELD_COMMANDS`. A 40,000-cycle record (420 us) whose SET_CONFIGURATION answer lands after the next record is reported only. The presence check needs only one accepted SET_CONFIGURATION.
- **Why this is a suggestion:** the pace holds the record after an accepted SET_CONFIGURATION for 8 ms, so the poll commits its answer first. No published span shows this happening.
- **Suggested outcome:** hold every unanswered record in a held group, or refuse it, with a control.

### R837-7-S3 - SUGGESTION - Docs - the archive's path redaction leaves five script rows per packet off their INDEX hashes

The outer `MANIFEST.json` records each one (`original_sha256` = the INDEX row; `path_redacted: true`). Suggested outcome: state in INDEX.md that the outer manifest is authoritative for redacted scripts, or index the published bytes.

## Lens results

- **`[R837] PASS Conformance`**
  - Artifacts: `aecp_commands.c:99-130,182-219`; `aecp_face.c:105-123,159-185`; `ctrl_app_aecp.c:48-66`; `edit_rows.py:38-41`.
  - Checked:
    - statuses and order unchanged against Milan v1.2 5.4.2.5 and IEEE 1722.1-2021 7.4.7;
    - an accepted SET_CONFIGURATION stamps THE PACE (ruling 6883864236, item 3);
    - the paced class is the dearer member;
    - the slice is the rule's within 650 to 1,100 us (ruling 6888782796, item 1);
    - item 5 checked from the code;
    - the stated costs are at or above their measurements by the rule (`compare-1x1.txt`, `compare-8x8.txt`).
- **`[R837] PASS RTL`**
  - Artifacts: `ctrl_loop.h:263-332`; `ctrl_loop.c:199-203,322`; `KL_mbx_cdc.sv:252-282`; `mbx.c:337-350`; `milan_soc.py:282-288`.
  - Checked:
    - the SRP drain limit equals the stated record;
    - `BUILD_MOST` is 1 at 950;
    - the static asserts hold;
    - the commit/acknowledgement crossing has no backpressure and a bounded wait;
    - the clock domains share a PLL;
    - only one-interface `ctrl_loop.o` changes (`image-sha256-*.txt`).
- **`[R837] PASS Robustness`**
  - Artifacts: `aecp.c:906-929`; `aecp_face.c:79-101`; `aecp_nvm.c:135-151`; `record_classes.py:102-111`; `receipts/record-classes-unanswered-probe.txt`.
  - Checked:
    - the wait and re-note path with a moved index;
    - an override-only SET publishes the settings alone;
    - a silent window still gives ENTITY_MISBEHAVING;
    - a refused SET holds no pace;
    - a record that answers nothing is never named by a later record's response.
  - S2 is optional.
- **`[R837] PASS Tests`**
  - Artifacts: `test_aecp.cpp` (five new tests); `aecp_configuration_mutants.py`, 13 of 13 caught on my run; `record_classes.py` controls 11 of 11; `load_grade.py` `srp_unit_controls`; `rows_tiers.py:876-886`; `selftest_round.py:105-112`.
  - Checked:
    - my 900 us slice plant and 250 us drain plant are each refused by name;
    - the hooks self-test is 28/28 and 96/96;
    - the AECP app arm passes 147/147 at 1 and 2 interfaces.
- **`[R837] UNCLEAN Docs`**
  - Artifacts: `SPLIT_CONTROL_MEMORY.md:2197`; `srp/README.md:238`; PR body lines 203 and 282 (R837-7-F1).
  - The rest of the docs delta checks against the head: section 13's new subsections at `:2484-2510`, FR_NFR 3.4.1 at `:383`, MAILBOX_SPLIT, the harness, AECP and gtest READMEs, and section 13's rom figures against `rom-per-image.txt`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_commands.c`, `aecp_face.c`, `ctrl_app_aecp.c`, `edit_rows.py`, rulings 6883864236, 6886633874 and 6888782796, `compare-1x1.txt`, `compare-8x8.txt`, item 5 receipt | R837-7 | `234bc149ff888eb96659ecaaa5ce6e4fb27319d4` |
| RTL | CLEAN | `ctrl_loop.h`, `ctrl_loop.c`, `KL_mbx_cdc.sv`, `mbx.c`, `milan_soc.py`, image hash receipts | R837-7 | `234bc149ff888eb96659ecaaa5ce6e4fb27319d4` |
| Robustness | CLEAN | `aecp.c` wait path, `aecp_face.c` publish and applied, `aecp_nvm.c`, `record_classes.py` naming, unanswered probe | R837-7 | `234bc149ff888eb96659ecaaa5ce6e4fb27319d4` |
| Tests | CLEAN | `test_aecp.cpp`, `aecp_configuration_mutants.py` (13/13 on my run), `record_classes`/`load_grade`/`rows_tiers`/hooks self-tests, two in-tree plants | R837-7 | `234bc149ff888eb96659ecaaa5ce6e4fb27319d4` |
| Docs | UNCLEAN (R837-7-F1 open) | `SPLIT_CONTROL_MEMORY.md` section 13, FR_NFR 3.4.1, MAILBOX_SPLIT, the SRP, AECP, gtest and harness READMEs, the live PR body | R837-7 | `234bc149ff888eb96659ecaaa5ce6e4fb27319d4` |

A fix for F1 that touches only `SPLIT_CONTROL_MEMORY.md`, `srp/README.md` and the PR body changes nothing in the scope of the other four lenses. A Docs re-review of that change can bank Docs at the new head, with the other four carried from this head.

## Real limits

- **Hosted CI does not run on split PRs.** Source-head execution evidence is the author's published receipts:
  - lane part a at `234bc149`;
  - parts b and c, the workflow steps and the sweep at `ed0df35b`;
  - the legs at `c274b9f5`.

  I re-ran the model gates, the hooks self-test, `docs_check`, the AECP arms and the 13 configuration mutants at the exact head. I did not re-run the leg campaigns, the sweep, lane parts b and c, the full AECP (299) or control (716) campaigns, or the full firmware unit gate (my native run timed out).
- **`check_em_dash.py` could not run here** (the pinned renderer is not installed); I rely on the author's `em_dash rc=0` at `234bc149`.
- **The archive commit is not signed.** Integrity rests on `MANIFEST.json`'s hashes, which all verify.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. No manager source bank runs at this head, and none is claimed or inferred.

## Pending manager duties

- Validate the current-dev merge candidate (source base `66f71326`, live dev `6b66f66d`) with the builder and native banks at the merge turn, and link its receipts.
- Hosted and act acceptance.
- Carry R837-7-R1 to the residue checklist.
- Route R837-7-F1's fix to a Docs re-review at the new head.
- The 8x8/2if figures go to #894's 8x8 lane and #890. The 8x8/1if legs' known exits go to that lane and #910. These are KNOWN, not findings here.

R837-7 FINISHED
