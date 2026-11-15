[R833] POSITIVE - exact head b15da60ac66d449ebf00b51e6c84ba256e319229

# R833-6: narrow delta re-review of PR #898 (issue #897), round 6, `eca1b9ca` -> `b15da60a`

- **Head:** `b15da60ac66d449ebf00b51e6c84ba256e319229`, tree `e9496fbd3719e1d5dd268fec5ec3228f902a39c9` (verified in the clone; PR head on GitHub equals it, not a draft, base `dev-soft-core`).
- **Delta:** one commit, four files: `docs/design/SPLIT_CONTROL_MEMORY.md` (+3/-3), `tb/verilator/ctrl_service_budget/README.md` (+2/-1), `record_classes.py` (+71/-19), `selftest_mutants.py` (+9). No firmware, RTL, HDL or image change. The six harness ELFs and eight fixture/platform images are byte-identical to `eca1b9ca`'s (`author-r6/receipts/images/images-b15da60a-vs-eca1b9ca.txt`). So round 5's full pass and sweep stand for everything the delta does not touch.
- **Authority:** AGENTS.md sections 6-7; #897's ruling issuecomment-6890824581, item 4 (GET_AS_PATH's record measured in a tracked answering-ports group and held as an ordinary record); IEEE 1722.1-2021 7.4.41.2 (the GET_AS_PATH response: descriptor_index, count, path_sequence of count 8-byte entries); R833-5 (issuecomment-6895817141), F1, F2, RES1-RES5 and S1-S4.
- **Verdict: POSITIVE.** F1 and F2 are resolved at their cause. RES1-RES5 are applied with their exact fixes. No new BLOCKER, MAJOR or MINOR was found. There is one new residue item, which is in the manager-owned staging note and not on the head (RES6), and three new optional suggestions (S5-S7).

## How this round was done

1. I read the delta (`git diff eca1b9ca..b15da60a`) before reading any prior finding, and judged it against the ruling item and the 1722.1 clause.
2. I verified the author's packet `review-evidence/897-r1/author-r6` at evidence commit `109c134b`, and spot-checked the receipts each claim rests on (`receipts/author-r6-spotcheck.txt`).
3. My own runs at the head:
   - `record_classes.py --selftest`;
   - `run.py --self-test`;
   - seven mutants of the new guard, each applied to a disposable archive of the head (`scripts/probe_record_classes.sh`).
4. I did not build or run the CPU harness legs. Their figures come from the author's published receipts.
5. Only after my own pass did I read R833-5's findings and resolve each one.
6. The clone was never modified: worktree clean, index equal to the head tree, tree `e9496fbd`, and the six gitlinks equal to the head's.

## Check (1): F1, the GET_AS_PATH guard now holds the answered read

**The code** (`tb/verilator/ctrl_service_budget/record_classes.py`):
- `:145-147` (`read_leg`) adds each solicited response's control_data_length: `(fr[16] << 8 | fr[17]) & 0x7FF`. That is the 11 low bits after the 5-bit status, at the AVTPDU's bytes 2-3 behind the 14-byte Ethernet header. The decode is correct.
- `:58` sets `ANSWERED_LENGTH = 16 + 8 * arm_path.ENTRIES` = 80. That is controller_entity_id 8 + sequence_id 2 + command_type 2 + descriptor_index 2 + count 2, plus 8 B per path_sequence entry. This matches 7.4.41.2 and the AECPDU's control_data_length, which counts from after target_entity_id. `arm_path.ENTRIES` = 8 (`arm_path.py:15`).
- `:190` `answered_path` requires command 0x0028, status 0 and length 80.
- `:215` refuses a pass with no such record in an answering-ports leg at 1x1/1if.
- `:219` refuses, at every point, any answering-ports `aecp` GET_AS_PATH answered SUCCESS at another length. GET_AS_PATH is sent only in the `aecp` group (`scenario.py:461`), so the README's "any GET_AS_PATH the answering-ports arm answers SUCCESS at another length" is exact.
- `:307` `port_findings` pins `build.VARIANTS['answering-ports']` to `arm_path.B_PATH` and to `image_face.ports.path=b_path;`.
- `selftest_mutants.py:48,632` restores the earlier stub as a named mutant.

**The wire agrees** (`author-r6/receipts/records/fB1-results.txt`):
- arm B's response is 106 B: 14 + 12 + 80;
- count 8 and eight entries `001bc5fffe000000`..`07`;
- arm A's refused response is 42 B: 14 + 12 + 16.

**Refused by name:**
- *In the self-test.* My run: `record classes: 14 of 14 planted controls refused; the answering-ports arm's path port is arm_path.py's`, rc 0 (`receipts/record_classes_selftest.log`). My harness self-test: rc 0, 869 PASS, 0 FAIL, 250 MUTANT caught, 0 not. It includes `PASS: the record classes refuse a GET_AS_PATH answered SUCCESS with no entries`, `PASS: the answering-ports arm's path port is arm_path.py's, which reads the window`, and `MUTANT caught: build: arm B's path port answers no entries at once, reading no window (earlier rule)` (`receipts/harness_selftest-summary.txt`; counts equal to the author's `harness_selftest-checks.txt`).
- *R833-5's own probe at the head.* `author-r6/receipts/gates/lane/stub_probe_refused.log` reports `self-test rc 1; record_classes rc 1; restored`, and the gate greps for the FAIL line by name.
- *On a real arm-B build.* The stub leg `stubB1` (`stub-leg/cl-stub.diff`, the stub in place of `arm_path.B_PATH`) answers `status 0 ... count 0, control_data_length 16` (`stubB1-get_as_path.txt`). `record_classes.py` at `b15da60a` over the legs with it refuses by name: `REFUSED ... answered SUCCESS with control_data_length 16, not the 80 ...` plus the missing-record line, RESULT FAIL, rc 1 (`record_classes-stub-for-arm-b.txt`, `record_classes-with-stub.txt`).
- *Real legs pass.* `record_classes-b15da60a-legs.txt`: RESULT PASS, rc 0, over arm A's four parts, the answering-every-port arm and this head's legs of every arm at both points.

**My mutants of the guard** (`receipts/probes/mutants.txt`; rc 1 means the self-test catches it):

| Mutant | rc | Reading |
|---|---|---|
| M1 `answered_path` drops the length | 1 | caught (the no-entries control escapes) |
| M2 the per-leg refusal removed | 1 | caught |
| M4 `ANSWERED_LENGTH` = 16 | 1 | caught |
| M3 the missing-record check by status alone | 0 | equivalent: any status-0 record at another length is still refused by `:219` |
| M5 decode reads byte 18 for byte 17 | 0 | not exercised by the synthetic self-test; fails closed on real legs, since every answered arm-B record would decode away from 80 and be refused (S5) |
| M6 the `image_face.ports.path=b_path;` wiring check removed | 0 | no planted control; backed by the real-leg length check (S6) |
| M7 the per-leg refusal only at 1x1/1if | 0 | no planted control at 8x8/2if; the port is one source at both points, and 1x1/1if plus `port_findings` hold it (S6) |

None of the surviving mutants opens the F1 failure mode. Losing or stubbing the reading port is refused statically, by `port_findings` and its mutant. It is also refused dynamically, because the answered length no longer equals 80. **F1 is resolved.**

## Check (2): F2, the receipts and section 13

Each record is listed per command, status and control_data_length, and each GET_AS_PATH response is decoded:

| Leg | GET_AS_PATH record | Response | Receipt |
|---|---|---|---|
| arm B, 1x1/1if | 16,208 cycles, 175 us | status 0, control_data_length 80, count 8 | `fB1-results.txt` (and `mB1`) |
| arm A, 1x1/1if | 10,948 cycles | status 10 (ENTITY_MISBEHAVING), length 16 | `fA1-results.txt` (and `mA1-results-q3.txt`) |
| arm B, 8x8/2if | 16,397 on port 0; 15,966 on port 1 | both length 80 | `fB8-results.txt`, `m2B8` |
| arm A, 8x8/2if | 11,328 and 11,150 | both length 16 | `fA8`, `m2A8` |

- `fB1`/`fA1`/`fB8`/`fA8` ran at `eca1b9ca` with images equal to this head's (`images-b15da60a-vs-eca1b9ca.txt`: `cb862ec3`, `c1863c22`, `77d041e7`, `14bf8c34` on both sides). `record_classes` is a post-processor of those legs, so they are this head's measurement.
- The rule (cycles / 100 x 1.05, rounded up to 5 us) gives 175, 170, 175, 115 and 120 us. These are section 13's figures at `SPLIT_CONTROL_MEMORY.md:2532`, within the 245 us (1x1/1if) and 265 us (8x8/2if) ordinary records that `record_classes-b15da60a-legs.txt` states.
- Section 13's other changed figures match the gate logs:
  - R4 13.25 ms (`flip_check_1x1.log`, `| 1x1/1if | R4 | 13.25 | 20 |`);
  - the load 0.518 and 0.514 (`load_check.log` HELD lines).
- The 17,290-cycle estimate is unchanged by the delta and keeps round 5's verdict.

Section 13 states only what the receipts show. **F2 is resolved.**

## Check (3): RES1-RES5

| Item | Status | Evidence |
|---|---|---|
| RES1 | resolved, verbatim | `:2557` "R4 13.25 ms (13.10 at the final pass's restatements)" |
| RES2 | resolved, verbatim | `:2526` "row held ... the load was 0.516 and 0.512 (with GET_AS_PATH's restatements, below)" |
| RES3 | resolved, verbatim | `:2532` "within the 245 us of an ordinary record (235 before the restatements below)" |
| RES4 | resolved | the PR body's round-5 line names R833-5 NEGATIVE at `eca1b9ca` on F1 and F2. The round-6 line awaits this verdict, which is the manager's update |
| RES5 | resolved in place | issuecomment-6894799910 (updated 2026-11-15T14:26:07Z) reads "as built at 1x1/1if R4 and last (the first queued notice at its 20 ms bound)", as `author-r6/receipts/res5-edit.diff` shows |

## Check (4): the gates for what changed

- **Packet integrity** (`receipts/packet-verify-author-r6.txt`):
  - 251 files, each equal to its `MANIFEST.json` published_sha256, with none unlisted;
  - 232 INDEX rows. The two receipts whose bytes differ from the INDEX (`docs__docs-gates-1__gate_25_0.log`, `docs__docs-gates-2__gate_25_1.log`) are manifest path redactions, each with its original_sha256 equal to the INDEX hash. Their verdict lines and rc files are unaffected.
- **Docs workflow:** 61 step rc files, all 0, and each driver reports "failed 0". This matches the REVIEW READY's "61 ran, 34 not run with a stated reason, 0 bad".
- **Lane gates** (`gates/lane/summary.txt`): 24 gates, 20 at rc 0 and the 4 by-design exits at rc 1. Each exit's output body (`rows_tiers_report`, `flip_check`, `flip_check_1x1_as_built`, `flip_check_8x8`) is byte-identical to `author-r5`'s at `eca1b9ca`, apart from the head line, and so is `load_check`'s.
- **The six harness legs at `b15da60a`** (`harness/final-b15da60a/hs-g{A1,A8,B1,B8,E1,N8}.rc`): all rc 0, 0 refusals and 0 budget misses. gB8's "2 of 455 work passes over the per-pass share" is the same as round 5's fB8.
- **Comment rule:** the added source lines in the delta show no lane label, review round, reviewer ID or issue-comment ID (`receipts/comment-rule-scan.txt`). The only pattern hit is the lint code `E402`. "arm B" and "(earlier rule)" are the harness's existing vocabulary.
- **Hosted checks at the exact head**, when inspected: 24 check runs, 3 completed success, 8 in progress, 13 queued. None is claimed here; hosted and act acceptance are the manager's.

## Findings

No BLOCKER, MAJOR or MINOR.

### Residue (wording only; no verdict or lens effect)

- **RES6 - Docs (packet, manager-owned; not on the head) - `review-evidence/897-r1/author-r6/STAGING-NOTE.md`.**
  - **Evidence:** the note says the redacted `scripts/receipts3.py` is published at sha256 `69369db9…` and that "No receipt changed". But `MANIFEST.json` records a second, path redaction of that file (original `69369db9…`, published `45b4068b…`, which is the file's actual hash). It also records path redactions of two receipts (`docs__docs-gates-1__gate_25_0.log`, `docs__docs-gates-2__gate_25_1.log`) and of seven more scripts.
  - **Impact:** none on any figure or verdict. The manifest is complete and correct. A reader trusting the note alone would find two INDEX mismatches and a wrong hash.
  - **Exact fix:** "…published sha256 `69369db9…` after this line's redaction, and `45b4068b…` after the manifest's path redaction. `MANIFEST.json` records 10 path-redacted files in `author-r6`, among them two receipts (`docs__docs-gates-1__gate_25_0.log`, `docs__docs-gates-2__gate_25_1.log`), whose INDEX rows carry their pre-redaction hashes; no receipt changed otherwise."

### Suggestions (optional; no lens effect)

- **S5 - Tests - `record_classes.py:145-147`.** The self-test's synthetic legs bypass `read_leg`, so the frame decode of status and control_data_length is exercised only by real legs. M5 survives the self-test. It fails closed, and both outcomes are evidenced on real frames (80 PASS, the stub's 16 refused). Optionally, add a fixture that runs a 106-byte and a 42-byte AEM response through the answer tuple.
- **S6 - Tests - `record_classes.py:219,316`.** There is no planted control for the build-wiring check (M6) or for the per-leg refusal at 8x8/2if (M7). Both are backed by the real 1x1/1if length check. Optionally, add a plant of each.
- **S7 - Tests - `record_classes.py:319`.** The "answers ENTRIES" half of `port_findings` is a substring test for `8u` in `B_PATH`, which any `8u` literal satisfies. The real-leg length check is the substantive guard. A comment saying so would avoid overstating the static check.
- **S1, S3 and S4 (R833-5)** stay as retained by the author. **S2** is superseded by RES6: the author's INDEX is now generated after sanitizing, and the remaining ambiguity is the manager's later redaction.

## Prior findings at this head

| Finding | Status at `b15da60a` | Where |
|---|---|---|
| R833-5 F1 (MINOR, Tests) | resolved | `record_classes.py:58,145-147,190,215,219,307`; `selftest_mutants.py:48,632`; check (1) |
| R833-5 F2 (MINOR, Docs, Tests) | resolved | `author-r6/receipts/records/`; `SPLIT_CONTROL_MEMORY.md:2532`; check (2) |
| R833-5 RES1-RES5 | resolved | check (3) |
| R833-5 S1, S3, S4 | retained (optional) | `arm_path.py`, `build.py` |
| R833-5 S2 | superseded by RES6 | packet |
| R833-3 F1, R833-3 R1-R3, R833-4 S3-S5 | resolved, as R833-5 recorded; the delta does not touch them | R833-5 table |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 6890824581 item 4 against `record_classes.py:58,190,215` (the held record is the answered read); IEEE 1722.1-2021 7.4.41.2 length 16 + 8n against `ANSWERED_LENGTH` and the decoded wire (`fB1`: 106 B, count 8, length 80; `fA1`: 42 B, status 10 ENTITY_MISBEHAVING); `answers.py:106` unchanged; no firmware change, images identical (`images-b15da60a-vs-eca1b9ca.txt`). Round 5's Conformance coverage of the rest stands | R833-6 | `b15da60ac66d449ebf00b51e6c84ba256e319229` |
| RTL | CLEAN | `git diff --stat eca1b9ca..b15da60a`: no `hdl/`, `sw/` or image change; the 14 images byte-identical; round 5's RTL coverage at `eca1b9ca` stands, since nothing in its scope changed | R833-6 (scope check; R833-5's coverage carried) | `b15da60ac66d449ebf00b51e6c84ba256e319229` |
| Robustness | CLEAN | `record_classes.py:145-147` decode, with the `len(fr) >= 38` filter unchanged and `length` defaulting to None when unanswered (`:84`); `:219` refuses any SUCCESS at another length at every point; the stub (count 0) refused on a real leg; mutants M3/M5/M6/M7 analysed as equivalent or fail-closed | R833-6 | `b15da60ac66d449ebf00b51e6c84ba256e319229` |
| Tests | CLEAN | own `record_classes.py --selftest` (14/14 and the port check, rc 0); own `run.py --self-test` (869 PASS, 0 FAIL, 250/250 mutants, rc 0); own guard mutants M1-M7 (`receipts/probes/`); the author's stub probe and the stub-leg refusal; `record_classes-b15da60a-legs.txt` PASS; lane gates and the 4 by-design exits byte-identical to round 5's; six harness legs rc 0. S5-S7 optional | R833-6 | `b15da60ac66d449ebf00b51e6c84ba256e319229` |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md:2526,2532,2557` against `fB1`/`fA1`/`fB8`/`fA8`, `flip_check_1x1.log` and `load_check.log`; harness `README.md:200,1291` against `record_classes.py` and `selftest_mutants.py`; PR body (RES4); issuecomment-6894799910 (RES5); packet INDEX/MANIFEST (RES6 residue, manager-owned) | R833-6 | `b15da60ac66d449ebf00b51e6c84ba256e319229` |

## Real limits

- I did not build or run the CPU service budget harness (SoC, CPU netlist, images). The leg figures (16,208; 15,966; 10,948; 11,328; the 8-entry, length-80 response; the stub leg's length 16) come from the author's published receipts. I verified them against the manifest and checked that they are consistent with each other and with the rule. I did not reproduce them.
- My mutants ran against `record_classes.py --selftest` only, not against real legs. I did not regrade any leg myself, because the leg directories are not published, only their summaries.
- The Verilator sweep, the AECP/control/SRP campaigns, the workflow replay and the lane gates are taken from the author's receipts and round 5's pass. The delta changes nothing they depend on.
- I ran no Docker, act, builder, Yosys or Vivado. Hosted contexts at the head were mostly in progress or queued when I looked.
- Physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank runs at this head, and none is claimed or inferred.

## Pending manager duties

- Validate the current-dev merge candidate (source base `7f50ee6a`, live `dev` `6b66f66d89cf25d2717687bcc2c3bf617685a99a`) with its builder and native banks, and link its receipts.
- Own hosted and act acceptance at the exact head.
- Carry RES6 to the residue checklist, and update the PR body's round-6 line with this verdict.
- KNOWN, not findings, carried as stated:
  - #902 is at `fe1fd541`, and the train candidate composes it;
  - #902 states the paced class at 300 us where this branch restates 305 by its own measurement;
  - the merge order #902, #901, #898;
  - ruling item 3's composed 8x8/2if platform grade.

R833-6 FINISHED
