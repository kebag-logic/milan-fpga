[R833] NEGATIVE - exact head f098f893d57e0fa3ec95a7e459313c5cfe4f4224

# R833-3: delta review of PR #898 (issue #897), round 3

- **Head:** `f098f893d57e0fa3ec95a7e459313c5cfe4f4224`, tree `3cdb680fe1bd3729d441c02160e69c20f2ac707a`.
- **Delta:** from round 2's head `3bebf03a` (R833-2 POSITIVE). The range composes the branch with #902's review head `7398ec0a` (`894-tiers`, not merged) through the sync merges `e45981f8` and `a3a509d7`, plus three commits: `417f44af`, `25ea917f` and `f098f893`.
- **Scope:** #898's side and the merge only. #902's own changes are reviewed on #902.
- **Verdict:** NEGATIVE, on one MINOR (F1). It is an evidence-publication gap. There is no defect in code, tests or figures:
  - 11 receipts that the author packet's own `INDEX.md` lists, with their sha256, are missing from the published archive `b4ae9cfc`.
  - Those receipts are the only evidence for the measured GET_AS_PATH notice-round and per-word figures that `SPLIT_CONTROL_MEMORY.md` section 13 now states.
- **Everything else holds at this head:**
  - the merge carries both sides with nothing dropped;
  - the 1x1/1if flip check composed with #902 passes, and I reproduced it byte-for-byte;
  - the load is 0.513;
  - the ROM ledger is within every cap at every point;
  - coverage is at 100 %;
  - round 1-2's plants are caught by name;
  - the moved plant table is identical in its 283 rows;
  - the AsPath gtests pass in my own run.
- **Fixing F1 needs no source commit.** Publishing the 11 indexed files, with the redaction they need, resolves it at this same head.

## 1. Reconstruction

Read: AGENTS.md, CONTRIBUTING.md (by reference from AGENTS.md), the issue #897 body (acceptance 1-5) and its public comments:
- the TAKEN comment;
- STOP issuecomment-6828566150;
- ruling issuecomment-6828659285, option (a), which amends acceptance 3;
- REVIEW READY issuecomment-6875785531.

Also read #894's ruling issuecomment-6867393730. Its item (d) is the rule that #898 must pass the 1x1/1if flip check composed with #902.

Then `git diff 7f50ee6a..f098f893` and the delta `3bebf03a..f098f893` with its history, and the author packet `review-evidence/897-r1/author-r3` at `b4ae9cfc`, extracted into its own directory.

I read prior public findings on PR #898 only after my own pass (section 6).

## 2. Merge: each side carried exactly

Method (`scripts/merge_sides_check.sh`, receipts `receipts/mergecheck/`):
- The merge base of `3bebf03a` and `7398ec0a` is `cec88385`.
- For each of #898's 17 files, I compared the +/- lines of `git diff cec88385 3bebf03a` with those of `git diff 7398ec0a f098f893`.
- For each of #902's 85 files, I compared `git diff cec88385 7398ec0a` with `git diff 3bebf03a f098f893`.

The result is 90 SAME. Each of the six DIFF files is explained by hand, and nothing of either side is dropped:

| File | Why it differs | Result |
|---|---|---|
| `tb/verilator/ctrl_split_boot/README.md` | Both sides made the identical one-line 59.5->60.0 edit | The merge equals both sides |
| `sw/firmware/ctrl/plat/README.md` | #902's two 59.5->60.0 lines equal #898's | #898's lines kept: the AECP paragraph, `platboot`, 42 plants, "refused at 60.5", and the "GET_AS_PATH answers unavailable" item removed |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | #898's round-2 table ("At this branch's head ...") is replaced by `25ea917f`'s composed table, which is R833-2 F1's fix | Both history rows, #898's section-6 sentence, #902's whole delta and the new section-13 text are all present |
| `sw/firmware/ctrl/aecp/README.md` | #898's own line, plus `f098f893`'s pointer to `aecp_face_mutants.py` | All of #902's text present |
| `sw/firmware/ctrl/test/aecp_mutants.py` | `f098f893`'s split: one import and one concatenation | All of #902's rows present |
| `sw/firmware/gtest/coverage.ratchet` | #902's rows kept; #898's `aecp_face.c` 179/179 160/160; `ctrl_plat.c` 132/132 as measured on the composed tree (`417f44af`) | Agrees with `gates/lane/fw_coverage_check.log:43` |

Other merge checks:
- **`ctrl_plat.c`, the four-way conflict:** `7398ec0a..f098f893` only removes the `path()` stub, removes `.path = path`, and extends the comment. `3bebf03a..f098f893` only adds #902's `owed` slots and their `#if AECP_MBX_OWED_SLOTS` composition. Both are intact.
- **Gitlinks:** all six are unchanged at `cec88385`, `3bebf03a`, `7398ec0a` and `f098f893` (`receipts/gitlinks.txt`).

## 3. Checks against the round's focus items

| Item | Result | Evidence |
|---|---|---|
| Plant table after the split (`f098f893`) | **Same 283 rows** (name, file, old, new, checks) at `a3a509d7` and at the head. Names are unique; only the order changes. All 9 `face-as-path-*` rows are present. `aecp_mutants.py` is 977 lines | `scripts/defects_equal.py` -> `receipts/defects_equal.txt` |
| Round 1-2 plants caught by name | The 9 `face-as-path-*` plants are `[ok]` on their named tests. `plat-as-path-unavailable` is `[ok]` (first: `Boot.B11GetAsPathAnswersTheDatapathsSequence`). The campaigns are AECP rc 0 / PASS, control 717 of 717, SRP rc 0 | packet `gates/wf/rtl-fast__firmware-aecp-mutants__ci_step_9.log.excerpt.txt:68-100`, `...control-mutants__ci_step_9.log:1164-1165` |
| 1x1/1if flip check, composed | **PASS, reproduced by me, byte-identical to the author's**. R4 12.85/20, R4L 188.39/238, last 126.46/130, tx 29.86/49, txL 48.09/49, ACMP 28.44, ADP 26.83, MAAP 26.95/30 | `receipts/own/flip_check_1x1.log` (rc 0) vs packet `gates/lane/flip_check_1x1.log` |
| Load | **0.513 at the pin, 0.509 with tsn-c-stack#32, ceiling 0.70, reproduced byte-identical** | `receipts/own/load_check.log` (rc 0) |
| Join intervals | Every graded group, at both points, is between 185.403 and 190.181 ms, against the 181.0-239.0 gate | packet `harness/final-f098f893/summary-*.txt` `JOINS` lines |
| ROM ledger, fixture | 41.0 / 41.5 / 54.0 / 59.0 RAMB36. 8x8/2if is at #894's 59.0 fallback entry, 1,288 B before its granule. Everything else is <= 56 | packet `gates/lane/fixtures.log` |
| ROM ledger, platform | 42.5 / 43.5 / 56.0 / 60.0. 8x8/2if is under its override, cap 60.5, 256 B before the half tile. 7 of 7 ledger controls pass | packet `gates/lane/plat_ledger.log` POINT lines |
| ROM ledger, harness arms 8x8/2if | 59.0 each (125,688 / 125,872 / 126,012 B); the nearest is 964 B under | packet `harness/final-f098f893/images.txt` |
| Image deltas vs `5b264bf2` | Fixture +328/+320/+320/+320, platform +312 each, `sram` unchanged. This matches section 5's table and the PR body | packet `rom/tiers/` vs `rom/e45981f8/` |
| Images at the head vs the measurement builds | All 7 harness ELFs are identical to the `e45981f8` measurement builds | packet `harness/final-f098f893/images.txt` |
| Coverage | `fw_coverage --check` PASS, 39 files. `aecp_face.c` 179/179 160/160. `ctrl_plat.c` 100 % | packet `gates/lane/fw_coverage_check.log:27,43` (rc 0) |
| GET_AS_PATH: AS_PATH_CHANGED sink | 30.02 us measured (3,002 cycles, 8 events), against 35 stated | packet `harness/measure/eventcost-hA1.json` |
| GET_AS_PATH: notice round, answered with 8 entries | 46,397 / 47,490 cycles against 59,500 admitted. **No published receipt**: see F1 | `SPLIT_CONTROL_MEMORY.md:2486`; indexed receipts under `harness/scratch/` are not published |
| GET_AS_PATH: record bound | About 19,950 cycles / 200 us against 235. The inputs are partly published: 11,655 (arm A) and 60 (`mbx_read=.../7/60`). The 877 cycles a word comes from the unpublished scratch span (F1) | `SPLIT_CONTROL_MEMORY.md:2487`, packet `harness/measure/mbx_read.txt` |
| Datapath clamp cited by the new text | `KL_gptp_engine.sv:781-785` clamps the published count to 8, so the 9-word maximum holds | `gptp-processor` at its gitlink `135afd04` |
| Disclosed 725 vs 730 us build of one | Measured 69,269 cycles (692.7 us), within the stated 725. **My probe with 730 us passes:** txL 48.10/49, last 126.49/130, load 0.513 | `receipts/probe730/` (a disposable copy with `CTRL_LOOP_BUILD_ONE_PASS_US` and the two tables at 730) |
| Full pass at the head (author) | 65 of 65 suites, 2,713,040 checks, 0 in-suite failures. Lane gates 40 at rc 0 and 4 that exit 1 by design. 139 workflow steps ran, 0 bad. The job clones have 0 tracked changes | packet `sweep/shard-*/summary.log` and `complete.json` (head f098f893, exit 0), `gates/lane/summary.txt`, `gates/job-clones-after.txt` |
| My gates | `check_py_idiom.py` rc 0. `docs_check.py` rc 0 (0 findings, 219 md). The em-dash gate cannot run here because its pinned renderer is not installed; a grep of #898's added lines since `7398ec0a` finds no em or en dash. The AECP mailbox suites at 1x1/1if and 2if: 145 of 145 each, the four AsPath tests OK | `receipts/own/*` |
| Packet integrity | 604 of 604 author-r3 files match `MANIFEST.json` published_sha256. 582 of 593 INDEX rows are published. The 4 rows whose hash differs are the manifest's path-redacted files | `scripts/verify_packet.py` -> `receipts/verify_packet.txt`, `receipts/index_vs_published.txt` |

## 4. Findings

### F1 - MINOR - Docs, Tests

**Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:2486`, and the `877 cycles` input at line 2487. The artifact is archive `b4ae9cfc`, `review-evidence/897-r1/author-r3/receipts/INDEX.md:550-560`.

**Evidence:**
- The packet's own `INDEX.md` lists 11 receipts under `receipts/harness/scratch/`, with sizes and sha256. None of them is in the published archive, and none is in `MANIFEST.json`. They are:
  - `cl-path.diff`, `cl-rows.diff` and `cl-span.diff`;
  - `flip-1x1-build730.log`;
  - `pN1-notice-every-0-mbx_win_read.txt` and `pN1-notice-burst-0-mbx_win_read.txt`;
  - `path_round.txt`;
  - `sA1-aecp-mbx_win_read.txt` and `sA1-datapath-events-mbx_win_read.txt`;
  - `summary-pN1.txt` and `summary-sA1.txt`.
- The authoritative design doc states, as measured:
  - the answered notice's round, 46,397 cycles in `notice-every-0` and 47,490 in `notice-burst-0`, with the eight entries 3,032 of them;
  - the unanswered word, 378 to 796 cycles;
  - the most a word took, 877 cycles.
- The REVIEW READY's acceptance section rests "GET_AS_PATH's cost in the rows" on those numbers.
- The scratch arm that produced them, `cl-path.diff`, is also unpublished. So no cold reviewer can check or reproduce the measurement.
- `scripts/path_round.py` is published, but its input logs are not.

**Impact:**
- This is one of the round's three focus measurements for GET_AS_PATH's cost.
- It closes R833-1 S1's open question (no harness group times an answered path read), but only on unpublished evidence.
- The published figures that bound it (eventcost, `mbx_read`, the arm-A record) do not cover the answered notice round.
- AGENTS.md section 6, Docs lens: "The PR and Issue contain enough evidence for another cold reviewer". This is not met for that claim.

**Required outcome:** publish the 11 indexed receipts in the evidence archive, with whatever path redaction they need and a manifest entry for each, so that their bytes match `INDEX.md` or a recorded redaction. No source commit is needed; the head can stay `f098f893`.

**Verification:** `python3 -I scripts/verify_packet.py <archive>/review-evidence/897-r1` reports `not published 0`. `path_round.py` over the published `pN1` logs prints the 46,397 and 47,490 rounds with their admitted 59,500.

### R1 - RESIDUE - Docs

**Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:488` and line 2483 ("at the merge of `894-tiers` `5b264bf2`").

**Evidence:** the head composes `7398ec0a`, not `5b264bf2`. The figures still hold, because every image is byte-identical (packet `harness/final-f098f893/images.txt`, `trial/`). The text does not say so. The wording repeats the pattern R833-2 F1 fixed.

**Exact fix:** after "`894-tiers` `5b264bf2`" at line 488, add ", and at its merge of `7398ec0a`, every image byte-identical". Add the same at line 2483.

### R2 - RESIDUE - Docs

**Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:2487`.

**Evidence:** the text reads "Eight words more ..., their answers' two data words each ...". Read literally, that is 16 data-word reads. The author's derivation (HANDOFF-r3 table) uses 18, which is nine answered words including the count. The result, about 19,950 cycles (200 us, against 235), is unaffected.

**Exact fix:** replace "their answers' two data words each" with "the nine answers' two data words each (18 reads)".

### R3 - RESIDUE - Docs, PR body only

**Where:** PR #898 body, lines 29-30.

**Evidence:** both reviewer lines end "round 3 as the manager assigns it". The assignment is now public: R833-3, issuecomment-6876669515 (and issuecomment-6876355958), one internal reviewer.

**Exact fix:** name R833-3 at `f098f893` on the internal line, and state that round 3 has no external reviewer, per the manager's assignment.

### S1 - SUGGESTION - Conformance, Docs (new)

**Where:** `sw/firmware/ctrl/loop/ctrl_loop.h:315-323`.

**Evidence:**
- The comment derives 725 us from "68,951 cycles at 1x1/1if".
- On the composed tree, the same measurement is 69,269 cycles, disclosed in REVIEW READY. By the stating rule (plus 5 %, rounded up to 5 us) that gives 730 us.
- The stated 725 still bounds the measurement (692.7 us). My probe shows that the 1x1/1if rows and load hold at 730 (`receipts/probe730/`).

**Optional outcome:** the owner of the figure (#894/#902) restates or confirms it at the merge that lands both. The flip check is the gate, and it passes either way.

### S2 - SUGGESTION - Docs

R833-2 F3 is retained for round 3. The packet's `INDEX.md` was generated before redaction. Its rows for the 4 path-redacted logs (`gates/wf/docs__docs-gates-{1,2}__gate_25_*.log`, `gates/wf/elaborate__elaborate-gates-{0,1}__gate_15_*.log`) still carry their pre-redaction hash. The manifest records `path_redacted: true` and `original_sha256` equal to the INDEX row (`receipts/index_vs_published.txt`). Optional: regenerate the INDEX after redaction.

**Comment rule:** no new source-comment residue.
- The delta's source-comment changes are:
  - `aecp_face_mutants.py:3-7`: issue #897, IEEE 1722.1-2021 7.4.41, Milan v1.2 Table 5.22;
  - the `ctrl_plat.c:121-122` comment brought in by the merge, which is round 1's wording.
- They carry no lane label, round, reviewer ID or comment ID.
- `B11` in `test_plat_boot.cpp` is the file's own boot-rule numbering, as round 1 recorded, and is unchanged by this delta.

## 5. Hosted evidence at the exact head (observation; the manager owns hosted acceptance)

Contrary to the round brief, hosted CI did run at `f098f893`: run 43588304905, `rtl-full`, `pull_request`. Receipts: `receipts/hosted/`.
- 65 jobs succeeded:
  - all 19 Verilator shards;
  - all 4 Yosys shards;
  - `yosys-portability`;
  - every `firmware-*` job.
- 1 job was skipped by design: "Physical gPTP (nightly and manual)".
- `Union milan_dp_mclk` failed at step 5, "Download executed case evidence", with `Failed to GetSignedArtifactURL: Unable to make request: ECONNRESET`. That is an artifact-service network reset, not a test result.
- The aggregate `verilator-suites` failed as a consequence, and "Fail fast across this head" was cancelled.
- No source defect is indicated. The manager should re-run the failed union job before relying on hosted `verilator-suites` at this head.

## 6. Prior public findings on PR #898, at this head

| Prior item | Status at `f098f893` | Evidence |
|---|---|---|
| R834-1 SUGGESTION (RTL, Tests): no executable check of the firmware's kind 2 read on the split RTL | Retained. The delta changes neither side | `aecp_face.c` same hunk hash on both sides (`receipts/mergecheck/own_side_per_file.txt`); no `hdl/` file in `7398ec0a..f098f893` |
| R834-1 SUGGESTION (Robustness): a datapath reset between the count read and the entry reads | Retained, unchanged | as above |
| R834-1 SUGGESTION (Docs): 123,756 B unreceipted | Resolved in round 2; still resolved | the figure is replaced by receipted rows (`SPLIT_CONTROL_MEMORY.md` section 5 history table) |
| R833-1 S1 (Tests, Robustness): the answering arms' path stand-ins answer an empty sequence (`build.py`) | Retained as SUGGESTION. `build.py` is unchanged in the delta. The author's scratch-arm measurement addresses it, but is unpublished (F1) | `tb/verilator/ctrl_service_budget/build.py` same hunk hash on both sides |
| R833-1 O1: plat README 58.5/59.0 | Resolved in round 2; still resolved | `plat/README.md` reads 60.0, "refused at 60.5" |
| R833-2 F1 (RESIDUE): "At this branch's head" paragraph | **Resolved** | `SPLIT_CONTROL_MEMORY.md:488` opens "At the merge of #894's tiers ..." (the remaining "this branch's head" lines, 323, 475 and 517, are base or #902 text, outside this delta) |
| R833-2 F2 (RESIDUE): PR body "round 2 to be assigned" | **Resolved** | PR body line 29 names R833-2 POSITIVE at `3bebf03a`; the round-3 analogue is R3 |
| R833-2 F3 (SUGGESTION): INDEX not regenerated after redaction | Retained as S2 (round 3's packet has the same 4 files) | `receipts/index_vs_published.txt` |
| R833-2 F4 (SUGGESTION): `build.py:124-126` comment widths | Retained, unchanged | `build.py` is not in `3bebf03a..f098f893`'s #898-side changes |

## 7. Per-lens results

- **[R833] PASS Conformance.**
  - Artifacts: `git diff 3bebf03a f098f893 -- sw/firmware/ctrl/aecp sw/firmware/ctrl/app sw/firmware/ctrl/plat/ctrl_plat.c`, which changes only `ctrl_plat.c`'s owed-slot composition from #902, with `aecp_face.c` and `aecp_commands.c` unchanged. Also the AECP and control campaign logs at the head, and the AsPath gtests (`receipts/own/aecp_mailbox_if{1,2}.log`).
  - Round 1-2's verdict against IEEE 1722.1-2021 7.4.41, Table 7-141 (as ruling issuecomment-6828659285 amends acceptance 3) and Milan v1.2 5.4.2.24 / Table 5.22 holds, because the GET_AS_PATH sources are byte-identical in their hunks.
  - #894 ruling (d)'s flip check composed with #902 passes, and I reproduced it.
  - Acceptance 1-4 are met. Acceptance 5 belongs to the bench lane.
  - S1 is optional.
- **[R833] PASS RTL.**
  - No `hdl/` file is among #898's 17 files or in the merged diff `7398ec0a..f098f893`. Gitlinks are unchanged (`receipts/gitlinks.txt`).
  - The new section-13 text's datapath claim (at most 8 entries) matches `gptp-processor/hdl/top/KL_gptp_engine.sv:781-785`.
  - The face and window suites are in the author's sweep at the head (65 of 65) and in the hosted Verilator shards, 19 of 19 successful.
  - Round 1's RTL verdict depends on nothing the delta changed.
- **[R833] PASS Robustness.**
  - The ROM ledger at every point is within its cap: fixture <= 59.0 at 8x8/2if (#894's fallback entry), <= 56 elsewhere; platform 60.0 <= 60.5 at 8x8/2if, <= 56 elsewhere; harness arms 59.0. Half a tile more is refused (`plat_ledger` control `past-its-tiles`, packet `gates/lane/plat_ledger.log`).
  - The data placement is unchanged (packet `early/sram-layout.txt`).
  - The 730 us probe holds the rows (`receipts/probe730/`).
  - The unanswered-window path (`face-as-path-*-unanswered-ignored` caught) is unchanged.
- **[R833] UNCLEAN Tests.**
  - F1: the measured answered-notice round and the per-word figures have no published receipt.
  - Otherwise clean: the 283-row identity of the moved plant table (`receipts/defects_equal.txt`); the face plants and `plat-as-path-unavailable` caught by name; the AsPath gtests passing in my run (145 of 145, both interface counts); coverage at 100 % (`fw_coverage_check.log:27,43`).
- **[R833] UNCLEAN Docs.**
  - F1, as above.
  - R1-R3 are RESIDUE, and S2 is a SUGGESTION.
  - Otherwise clean: section 5's table matches `fixtures.log`, `plat_ledger.log` and `rom/tiers` digit for digit; `plat/README.md`, `aecp/README.md` and `ctrl_split_boot/README.md` are correct; `docs_check.py` 0 findings (`receipts/own/docs_check.log`); no new comment-rule residue.

## 8. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merged diff of `aecp/`, `app/`, `ctrl_plat.c`; campaign logs; AsPath gtests; flip check composed (own run) | R833-3 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| RTL | CLEAN | file set of `7398ec0a..f098f893` (no `hdl/`); gitlinks; `KL_gptp_engine.sv:781-785`; sweep and hosted Verilator shards | R833-3 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| Robustness | CLEAN | `plat_ledger.log`, `fixtures.log`, `images.txt`, `sram-layout.txt`; 730 us probe | R833-3 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| Tests | UNCLEAN (F1 MINOR) | `defects_equal.txt`; AECP/control/SRP campaign logs; `aecp_mailbox_if{1,2}.log`; `fw_coverage_check.log`; packet INDEX vs archive | R833-3 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| Docs | UNCLEAN (F1 MINOR; R1-R3 RESIDUE; S2) | `SPLIT_CONTROL_MEMORY.md` sections 5, 6, 13; `plat/README.md`; `aecp/README.md`; `ctrl_split_boot/README.md`; PR body; packet INDEX/MANIFEST | R833-3 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |

To clear Tests and Docs: F1's 11 receipts are published, and a reviewer re-checks them at this head. No new commit is required. The rest of the coverage above stays banked against `f098f893` unless a later commit touches those artifacts.

## 9. Real limits

- **No full firmware suite run by me.** My run of the full control-firmware suites exceeded the 10-minute foreground window (rc 124, `receipts/own/ctrl_firmware_suites.log`, not a result). I ran the two AECP mailbox suites it had built instead. For everything else, the author's full pass is the source-head execution evidence.
- **Campaigns and sweep not re-run.** I did not re-run the AECP, control or SRP campaigns, the Verilator sweep, the harness legs, `plat_ledger` or the fixtures. I verified their published receipts and the packet's hashes. The AECP campaign excerpt is elided, so "283 of 283" rests on its rc 0 / PASS, plus my table identity check.
- **Em-dash gate not run here.** Its pinned Markdown renderer is not installed, and I did not install it. I grepped the added lines instead.
- **Packet integrity only.** The packet is verified by hash against its manifest. It is not cryptographically signed: the commit shows no signature.
- **No merge candidate validated.** No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN. Bench acceptance 5 is not covered.
- **No current-dev candidate built.** The current-dev merge candidate (source base `7f50ee6a`, live dev `b7d69295`) was not built by me.

## 10. Pending manager duties

- Publish F1's 11 receipts into the evidence archive, or have the author do so. Then a re-check is needed at this head.
- Carry R1-R3 to the residue checklist. Update the PR body (R3).
- Re-run the hosted `Union milan_dp_mclk` job (artifact ECONNRESET) before relying on hosted `verilator-suites` at `f098f893`.
- At the merge turn: build and validate the current-dev merge candidate (builder and native banks) and link its receipts. Check that #902's merge into `dev-soft-core` leaves this branch's composition as reviewed: `7398ec0a` plus the merge commit. Route S1 (725 vs 730 us) to #894/#902's owner.

R833-3 FINISHED
