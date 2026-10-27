[R699] NEGATIVE - exact head 910d4b94c4d5334b1869f42e9653c308a15d0dba

# R699-5: internal cleared-context delta review, issue #396 part A, PR #786

- Head `910d4b94c4d5334b1869f42e9653c308a15d0dba`, tree `07ce568e5a407531407917c5e8f81d524cd09947`, base dev `e76a755a`.
- Previously reviewed head (R699-4): `85da3e4595871c1573c28b4d040b9e98463a41c9`.
- The delta is `4a460fc3`, `17a43ef2` and `910d4b94`:
  - `REQUIREMENTS.md` +6/-1;
  - `docs/testing/TESTING.md` +54/-1;
  - `tb/tools/torture_campaign.py` +568/-65;
  - `tb/tools/torture_release_audio_mutants.py` +56/-8;
  - `tb/tools/torture_release_mutants.py` +4/-4.

## Scope reconstructed

I read the following in order: AGENTS.md and CONTRIBUTING.md; issue #396's body; the owner decisions (2026-09-23, 2026-09-27 and its correction, the 2026-10-04 audio design, the 2026-10-26 four decisions, the part-A assignment, and the 2026-10-26 REBOOT/analog limits); and the round-5 ruling (issuecomment-6424374359). Then REQ-VER-06 and TESTING 6d at this head, the full `85da3e45..910d4b94` diff, the round-5 REVIEW READY comment, and the published round-5 receipts at evidence commit `7c4e2a47`. I read the prior review's findings only after my own pass over the diff and my probes.

For this delta, the scope comes from acceptance item 2 (the `audio` area, with exact per-event classification) and from the owner's audio design (decision 1: "Every discontinuity is classified exactly at its sample"; decision 3: a missed control voids the run). The round-5 ruling adds three items:
1. G3 is closed by a balance invariant.
2. G1 and G2 are fixed, or each exception is stated exactly and pinned.
3. A composition sweep becomes a gate.

## Verdict

**NEGATIVE.** Two MINOR findings are open (H1, H2), plus one RESIDUE and three SUGGESTIONs. There is no BLOCKER or MAJOR.

- All four prior MINORs are resolved for the shapes they named (table below). G3's invariant holds: 0 of 7,011 cases are unbalanced on the prior round's unmodified sweep, and my 3,000-case cluster probe found no net violation. All 289 tracked controls are killed. Gates, behave and the self-test pass.
- **Both open findings break claims this delta adds.** The behaviour itself predates the delta: the outputs are the same at `85da3e45`.
  - **H1:** the delta says the planted-arm voids are exactly two one-word shapes, and that a void arises only where no reading of the bytes finds the arm. A multi-word constant-mask excursion that covers a planted slip arm's sample voids the run in 3,848 of 12,480 grid cases. In the worked example, and by construction in the others, the planted truth is a reading with fewer DUT events that finds the arm. 2,160 of the voids use code-bit, channel-number or pad-bit masks, which the new text says "cannot" void.
  - **H2:** the delta says a constant-mask excursion is one `bit-flip` "at any length", and "after a short slip before it", with "no exception" left for G2. An excursion whose mask clears the channel number is split at every all-zero word into `bit-flip` + `silence` + `bit-flip`, with or without the slip. That is 24 of 48 cases, on every channel.
- Every case is fail-safe: FAIL or NOT RUN, never PASS. Each is MINOR because the behaviour contradicts a stated, normative classification rule. The defect is not in the wording alone.

## Findings

### H1 MINOR: Conformance, Robustness, Tests, Docs. A multi-word excursion over a planted slip arm voids the run, outside the two stated voids, although the bytes allow a reading that finds the arm

**Where:**
- The reading choice in `_read`, `tb/tools/torture_campaign.py:4647`: the alternatives at `:4653-4654` ("A slip arm that it misses is tried as the slip into or out of an excursion read as a corruption"), and `ranked` at `:4672`.
- The claims this delta adds:
  - `REQUIREMENTS.md:417` ("The exceptions are the planted-arm voids that TESTING 6d states");
  - `REQUIREMENTS.md:419` ("It cannot place an arm where the bytes leave no reading that finds it, so those shapes void the run");
  - `docs/testing/TESTING.md:1375-1378`;
  - `docs/testing/TESTING.md:1462` ("Two shapes beside a planted arm void the run");
  - `docs/testing/TESTING.md:1468` ("The code bit alone, a channel-number bit or a pad bit cannot");
  - `docs/testing/TESTING.md:1473` ("grades every placement of these shapes and the rest");
  - `AUDIO_COUNTER_LIMITS` `:3769-3776`;
  - the `audio.planted-arms-found` assertion text, `:3366-3369`;
  - the PR body `audio` row ("two shapes beside a planted arm, stated exactly, void the run").

**Authority:**
- The round-5 ruling, item 2: "State each exception exactly (shape, distance, arm kind and mask class)", and "A void stays a release block".
- TESTING 6d at this head, `:1375`: "The grader takes another reading only when it has fewer DUT events, or as many and more arms found".

**Evidence:**
- My grid is `scripts/r5_arm_excursion.py`, with logs `receipts/arm_excursion_head.log` and `receipts/arm_excursion_85da3e45.log`.
  - It places one constant-mask excursion of 2 to 12 words on one channel, starting 8 samples before to 3 after each of the four planted slip arms, so that it covers the arm's sample.
  - It uses 8 mask classes on every channel, on a 16384-frame capture at the release tolerance of 2.
- **3,848 of 12,480 cases are NOT RUN, "void: a planted arm was missed".** By mask:
  - `0x100` 864, `0x01000000` 864 and `0x100000` 432 (code bit, pad bit, channel-number bit): 2,160 in all;
  - position-bit masks: 1,688.
- The round-4 head gives 3,836, so this predates the delta. The delta's new text is what claims otherwise.
- **Example** (`receipts/focus_head.log`, line `S arm 15934 ch2 mask=0x100 lead=0 tail=5`):
  - The capture has the repeat-2 arm at 15934 and `0x100` over channel 2's words 15934 to 15938.
  - The grader reads a `bit-flip` n = 5 of mask `0x00000D00` at 15934, plus a DUT `repeated 2` at 15939. That is two DUT events, and the arm is missed.
  - The planted truth is "the arm at 15934, then one `bit-flip` n = 5 of mask `0x100` against the new track". The synthesizer built the bytes that way, so that reading has them, with one DUT event and every arm found.
  - By `:1375` that reading should win. By `:1378` this shape should not be a void.
- **Origin** (`receipts/fuzz_isolated.log`, `receipts/triage_isolated.log`): seeds 1546, 2160 and 2979. In each, a 126- to 144-word excursion happened to span a planted slip arm, and the run was NOT RUN. These are the only isolated-event deviations left after the stated neighbour-word limit (`TESTING.md:1421`).
- The composition sweep (`:9179`) and the slip-before sweep (`:9207`) never put a multi-word excursion over an arm. So `:1473`'s "every placement of these shapes and the rest" reads wider than what is graded.

**Impact:**
- A DUT corruption that overlaps a planted arm's sample turns a FAIL into a void NOT RUN, and the reason blames the arm.
- Release safety holds: the void blocks the release and the DUT event is still listed.
- But the documents now assert an exact, exhaustive exception list and a reading-choice guarantee, and the grader meets neither. A bench operator who reads a void as "the source missed a control" looks in the wrong place.

**Required outcome:** either of these.
- A multi-word constant-mask excursion over a planted arm reads as that excursion plus the arm, and FAILs with every arm found.
- Or the shape is stated exactly as a further void. The statement gives the excursion's extent relative to the arm, the arm kinds and the mask classes. The exhaustive wording is narrowed to match, at:
  - `REQUIREMENTS.md:417` and `:419`;
  - `TESTING.md:1378`, `:1462`, `:1468` and `:1473`;
  - `counter_limits`, the assertion text and the PR body.

  The shape is then pinned by a self-test arm.

**Verification:**
- `scripts/r5_arm_excursion.py`, unchanged, reports either 0 voids or only voids in the newly stated shape.
- A new self-test arm fails at `910d4b94`.

### H2 MINOR: Conformance, Robustness, Tests, Docs. A constant-mask excursion whose mask clears the channel number is split at each all-zero word into `bit-flip` + `silence` + `bit-flip`

**Where:**
- The window tokenizer turns every all-zero word into a silence token ("Z", `tb/tools/torture_campaign.py:4455-4458`). The token is labelled at `:3975-3976` and emitted as a `silence` event at `:4421-4425`, before any excursion rule joins the masked run. This cause sentence is inferred from the code and the outputs.
- The claims:
  - `REQUIREMENTS.md:412-413` ("one bit-flip, at any length. That holds beside any one-word event, and after a short slip before it");
  - TESTING 6d rule 1 (`:1332`, "A flipped channel number ... is a `bit-flip`") and rule 4 (`:1340`);
  - `:1293` ("No valid word is zero, so silence stays distinct from data"), which does not cover a corrupted word that becomes zero;
  - the PR body's Round 5 G2 row ("No exception remains").

**Authority:**
- Owner audio design, decision 1: "Every discontinuity is classified exactly at its sample".
- The round-5 ruling, item 2.

**Evidence:**
- `scripts/r5_zero_word.py`, with logs `receipts/zero_word_head.log` and `receipts/zero_word_85da3e45.log`.
- Channel c carries number c + 1 in word bits 23:20. The mask `(c + 1) << 20` clears it, so a masked word at block position 0 with code bit 0 is all zero.
- **24 of 48 cases split, on every channel, with no slip, a drop of 3 or a repeat of 2 before.** Examples:
  - 65 words from 4080 under `0x100000` on channel 0 read as `bit-flip` 15, `silence` 1 at 4095 and `bit-flip` 49;
  - a 9,000-word stuck channel-number bit reads as five events, two of them `silence`.
- Excursions that cross no such word, and single words, read as one `bit-flip`.
- The round-4 head gives the same 24 of 48, so this predates the delta.
- My 3,000-case slip-before probe (`receipts/fuzz_before.log`) has 28 deviations, all of them this shape (`0x100000` on channel 0). Otherwise G2's fix held in every case.
- The in-tree slip-before grid (`:9207`) chose masks that leave every channel number intact, so it cannot see this shape.

**Impact:**
- The verdict still FAILs.
- But one corruption is reported as three or more events, including a class (`silence`) that points at a dropout. That misdirects the per-event record, which exists to localize the source.
- It contradicts rule 4, which this delta re-asserted, and the PR body's "No exception remains".

**Required outcome:** either of these.
- An all-zero word inside a constant-mask excursion, under that excursion's mask, is part of the one `bit-flip`.
- Or this is stated exactly as a limit: the mask clears the channel number, and the split falls at each block start whose code bit is 0. Rule 4, REQ-VER-06 `:412-413`, TESTING `:1293` and the PR body's G2 row are narrowed, and the limit is pinned by a self-test arm.

**Verification:**
- `scripts/r5_zero_word.py`, unchanged, reports 0 of 48 split, or only the stated shape.
- A new self-test arm fails at `910d4b94`.

### R1 RESIDUE: Docs. An absolute "no slip that did not happen" sentence

- **Where:** `docs/testing/TESTING.md:1371`: "So no slip that did not happen is ever reported."
- **Why:** the paragraph is about the balance guard. As written, though, the sentence is absolute, and the same section states two shapes that report slips that did not happen, in balance:
  - the position-bit-0 neighbour limit, `:1421`: a corruption read as a slip pair;
  - the first void, `:1464-1466`: `dropped 512` + `repeated 509`, pinned at `:9284-9291`.
- `REQUIREMENTS.md:415` is correctly scoped ("A window no reading balances is one unresolved event, never a slip that did not happen").
- **Exact fix:** "So no unbalanced slip is ever reported." The PR body's `audio` row has the same "never a slip that did not happen"; it can read "a window no reading balances is one `unresolved` event, never an unbalanced slip".

### S1 SUGGESTION: Tests. The mutant-driver timeout margin under load

- With 13 parallel jobs, the slowest control (#195, "block code bit dropped from the word") took 461 s against the driver's 600 s per-mutant limit (`receipts/mutants_all.log`). The author reports 288 s under six jobs.
- A timeout is "no kill", so a loaded host could fail the gate spuriously.
- Consider bounding the slow tests under a broken word layout, for example by failing fast after a clean-capture check, as `910d4b94` did for the sweeps. Or state the host load that the 600 s assumes.

### S2 SUGGESTION: Tests. Widen the two sweeps once H1 and H2 are settled

Both sweeps grade only one-word corruptions, and only under masks that never clear a channel number. Adding a channel-number-clearing mask and a short multi-word excursion over each arm would make both gates as exhaustive as their docstrings read.

### S3 SUGGESTION: Docs. Name a possible DUT cause in the void reason

The prior round's S1 was not adopted, which is the author's option. H1 adds a second case where the void's cause is a DUT corruption, not the source. The reason "void: a planted arm was missed" could add "or masked by a DUT event at its sample".

## Prior findings at this head

| Finding | Status at `910d4b94` | Evidence |
|---|---|---|
| R699-4 G1 (MINOR): a one-word corruption beside an arm voids | **Resolved for its one-word shape.** The prior `r4_arm_corruption_sweep.py`, run unmodified after a hash check, gives 156 not-FAIL of 24,768. They lie only at d = -1 and 0 by a slip arm and d = 0, ±1 by a flip arm, the places the two stated voids name, and the count matches the author's. The in-tree composition sweep checks each case's class from its bytes. The wider claim the fix wrote is falsified by multi-word excursions: H1, new and related. | `receipts/r4_arm_corruption_sweep_at_head.log`; self-test `:9179` |
| R699-4 G2 (MINOR): a slip before a constant-mask excursion | **Resolved for its shape.** My 3,000 random slip-before cases (gaps 1 to 64, slips ±1 to 8, lengths 64 to 2,100, 10 masks) are exact, except H2's zero-word shape (28 cases). The in-tree grid passes. | `receipts/fuzz_before.log`; self-test `:9207` |
| R699-4 G3 (MINOR): an unbalanced whole-block slip | **Resolved.** The prior `r4_net_sweep.py`, unmodified, gives 0 unbalanced of 7,011. My 3,000-case cluster probe (2 to 5 events within 80 samples, whole-block slips included) has 0 net violations. My 3,000-case isolated probe never fires the guard. Tracked controls #271 to #281 (hold offset, re-read, ranking, guard, ledger, reason placement, return) are killed. | `receipts/r4_net_sweep_at_head.log`, `fuzz_cluster.log`, `fuzz_isolated.log`, `mutants_all.log` |
| R699-4 G4 (MINOR): W03 and W07 survive | **Resolved.** Tracked controls #287 and #288 are character-identical to W03 and W07 in the prior `r4_reviewer_mutants.py`. Both are killed by `test_audio_arm_interplay_at_the_release_tolerance`. | `receipts/mutants_all.log` |
| R699-4 R1 (RESIDUE): the reading-choice sentence | **Resolved** at the `_read` docstring `:4655-4656`, at `TESTING.md:1375` and in the PR body's G1 row. | read at head |
| R699-4 S1 and S2 (SUGGESTION) | Not adopted, with reasons in the PR body; both are optional. S1 recurs, widened, as S3 above. | PR body |
| R699-4 S3 (SUGGESTION) | **Adopted:** DUT slips at 3250 and 3240 inside a 100-word excursion (`:8999-9004`). | read at head |
| R699-1 to R699-3 and R700-1 to R700-3 | Judged at `85da3e45` by R699-4 and R700-3. The delta changes the grader they depend on. The author's unmodified reruns of R699-3's, the round-2 and R700-3's probes are byte-identical to `85da3e45`, timing fields aside. I checked those receipts' hashes (below) and reran the two R699-4 sweeps above. Nothing is retained. | `author-r5/receipts/final_head_identical.log` |

## Gates at this head (my receipts; rc 0 unless stated)

| Gate | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 116 tests OK, 27.9 s |
| All 289 tracked release controls, in parallel under the driver's own kill rule and 600 s timeout (`scripts/parallel_mutants.py`, 13 jobs) | 289 of 289 killed; source unchanged; slowest 461 s (S1) |
| `cd tests && behave --no-capture -f plain` | 14 features, 495 scenarios, 2,286 steps passed |
| `behave tests/features/torture_campaign_plan.feature` | 176 scenarios, 665 steps |
| `docs_check.py` | 0 findings, 210 md files |
| `check_doc_paths.py` | OK, 1,065 paths |
| `gen_toc.py --check` and `--verify-anchors`, under the hash-locked renderer pin in a private environment | OK; 538 anchors |
| `check_em_dash.py --base e76a755a`, same environment | 0 findings over 458 added lines |
| `check_doc_style.py`, `check_py_idiom.py`, `check_feature_status.py` | 0 findings |
| `git diff --check e76a755a HEAD` | clean |

The first runs of `gen_toc.py` and `check_em_dash.py`, outside that environment, refused for the missing renderer (rc 2). They were rerun with the pin, as recorded.

**Author evidence, spot-checked** (evidence commit `7c4e2a47`, unsigned at the git level, like the head commit):
- `author-r5/receipts/head.txt` names this head, tree, parent, base and gitlinks. Its sha256 `b2551f43…` matches the published `MANIFEST.json`.
- `INDEX.md`, `behave_all.full.summary.txt`, `final_head_identical.log` and `quick_named_mutants_final.log` also match it.
- The author's counts agree with mine: self-test 116, 289 killed, behave 495 and 2,286, plan 176, and 156 voids in the prior arm sweep.

**Hosted, inspected only** (`receipts/hosted_check_runs.tsv`, 42 check runs when read):
- 11 succeeded, including `bdd-conformance`, `docs-check-no-git`, `verilator-lint` and `docs-gates-2`.
- 19 were in progress and 11 queued, including the Verilator shards, `yosys-elaboration` and "Prepare pinned Yosys".
- 1 was skipped: "Physical gPTP (nightly and manual)", which is not hardware proof.
- The manager owns hosted and replica acceptance.

## Documents and the comment rule

- No line the delta adds contains a lane label, round, reviewer ID or comment ID. The only hits are `L3`, the repository's test-level tag (`docs/testing/methodology.md:63`), which 11 base docstrings already use. There is no new RESIDUE of that kind.
- The changed contracts in REQ-VER-06, TESTING 6d, `counter_limits` and the assertion texts agree with one another and with the code, except where H1, H2 and R1 apply.

## Lens coverage

[R699] PASS RTL - `receipts/rtl_scope.log`: `git diff --stat` from `85da3e45` and from `e76a755a` to this head is empty over `hdl sw protocol-processor gptp-processor external third_party syn constraints`. All six gitlinks equal base and index. `audio_counter_word` is identical to `85da3e45`, so the S32 counter layout is unchanged. There is no RTL, firmware or submodule in the delta.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (H1, H2) | Issue #396 acceptance 2 and owner audio decisions 1 and 3; round-5 ruling items 1 to 3; `REQUIREMENTS.md:402-445`; grader `tb/tools/torture_campaign.py:3956-4320, 4647-4900, 4990`; assertion texts `:3324-3395`; `AUDIO_COUNTER_LIMITS` `:3738-3790`; my probes `r5_fuzz.py` (9,000 seeds), `r5_arm_excursion.py` (12,480 cases), `r5_zero_word.py` (48), `r5_focus.py`; the prior sweeps rerun | R699-5 | `910d4b94c4d5334b1869f42e9653c308a15d0dba` |
| RTL | CLEAN | Empty RTL/firmware/submodule diff; gitlinks; counter word layout (`receipts/rtl_scope.log`) | R699-5 for the delta; R699-1 for the rest, unchanged since | `910d4b94c4d5334b1869f42e9653c308a15d0dba` |
| Robustness | UNCLEAN (H1, H2) | Isolated, slip-before and cluster probes (3,000 each); excursion-over-arm grid; zero-word grid; `r4_net_sweep` (7,011) and `r4_arm_corruption_sweep` (24,768) rerun; each deviating shape compared against `85da3e45` | R699-5 | `910d4b94c4d5334b1869f42e9653c308a15d0dba` |
| Tests | UNCLEAN (H1, H2) | New and changed arms `:8994-9024, 9041-9320`; `tb/tools/torture_release_audio_mutants.py` (18 added, 5 re-anchored); `tb/tools/torture_release_mutants.py` (3 re-anchored); all 289 controls run; W03/W07 identity; self-test, behave tier and plan feature | R699-5 | `910d4b94c4d5334b1869f42e9653c308a15d0dba` |
| Docs | UNCLEAN (H1, H2; R1 is residue) | REQ-VER-06 `REQUIREMENTS.md:409-420`; TESTING 6d `:1284-1480`; `counter_limits`; the `_read`, `_hold`, `_split` and `_unbalanced` docstrings; the PR body's `audio` row and Round 5 section; the docs gates | R699-5 | `910d4b94c4d5334b1869f42e9653c308a15d0dba` |

## Real limits

- **Source validation only.** Gates and probes ran in the isolated clone, and in a `git archive` export of `85da3e45` used only for before-and-after comparison.
  - No manager source bank ran at this head, and none is claimed or inferred.
  - The current-dev merge candidate (base `e76a755a`, live dev `76de691e`) is not validated here.
- **No physical evidence.** Physical calibration was NOT RUN. The soak, the audio run and the power campaign are part B. Field skips are not hardware proof.
- **Synthetic captures only.** They come from the tracked synthesizer. No real capture was graded.
- **Causes are inferred.** H2's cause sentence is inferred from the code and the outputs. H1 names no cause. The required outcomes do not depend on either.
- **The behaviour predates this round.** H1 and H2 predate the delta. They are findings because this delta's text claims them.
- **The probes are seeded samples, not exhaustive.** Seeds 1,000 to 3,999 were used for each family.
- **The serial driver was not run.** I did not run `torture_release_mutants.py` serially. The parallel run applies its exact kill rule and its 600 s timeout.

## Pending manager duties

- Route H1, H2, R1 and S1 to S3.
- Build and validate the current-dev merge candidate (builder and native banks), and link the receipts.
- Hosted and replica acceptance at the final head. Most hosted jobs were still running or queued when read.
- Carried over:
  - record owner decision issuecomment-6409128703 in the plan;
  - ratify `restore_bound_s = 30`;
  - complete the external review at the final head.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`.
- **Scripts:** `scripts/parallel_mutants.py`, `r5_fuzz.py`, `r5_triage.py`, `r5_focus.py`, `r5_arm_excursion.py` and `r5_zero_word.py`.
- **Logs and rc files:** under `receipts/`.
- **`receipts/restore_check.log`:** HEAD, the index tree and both listings equal the exact head, and porcelain is empty. The bytecode caches this review generated were then removed.
- **The prior round's scripts** were run from the published copies at `7c4e2a47`, after a sha256 check against R699-4's `MANIFEST.sha256`. They are not republished.

R699-5 FINISHED
