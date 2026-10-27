[R699] POSITIVE - exact head a7a514fbf5572ce08394cd727c9cc9085745c79f

# R699-8: internal cleared-context delta review, issue #396 part A, PR #786

- **Head:** `a7a514fbf5572ce08394cd727c9cc9085745c79f`, tree `7bdbb8703e4e4dd34c86adb234af37ec68a2e6d3`.
- **Source base:** `e76a755a`.
- **Previously reviewed head:** `5fdabc1c` (R699-7, NEGATIVE, one MINOR).
- **Delta:** one commit, `a7a514fb`, with a one-line message and no trailers. It touches four files:
  - `REQUIREMENTS.md`
  - `docs/testing/TESTING.md`
  - `tb/tools/torture_campaign.py`
  - `tb/tools/torture_release_audio_mutants.py`

## Scope reconstructed

- **Acceptance.** Issue #396 acceptance 1, 2 and 5, plus the desk half of 4, per the part-A assignment (issuecomment-6408079016). Items 3 and 4 need the bench (part B), so the PR correctly says "Relates to #396".
- **Owner decisions:**
  - 2026-09-27, the `mr`/`tu` correction;
  - 2026-10-04, the audio signal design;
  - 2026-10-26, 24 h, 200 cycles (150 cold, 50 of them during a commit, plus 50 soft resets), the stricter criteria, and the gate written in both documents;
  - 2026-10-26 follow-ups: REBOOT, and sine limits at baseline + 6 dB.
- **Round-8 assignment (issuecomment-6443031364).** It rules R699-7 F1 by option (b): outside the exactness scope the promise is coverage, not position.
  - **Item 1, the rule.** No capture with a DUT event grades PASS. Every DUT event is covered, on each channel it changes, by a listing whose sample span overlaps [first word - 63, last word + 63]. An event inside a constant-mask excursion on the same channel may be covered by that excursion's listing alone.
    - Inside the scope, the listing begins within 63 samples of the first word.
    - This must be stated in five places: REQ-VER-06, TESTING 6d, `AUDIO_COUNTER_LIMITS[0]`, the assertion text and the PR body.
    - Every outside-scope sentence about where a listing begins must be dropped.
  - **Item 2, the gate.** The fuzz asserts coverage for every unit, and still asserts exact listing in the swept scope. A control must leave a DUT event uncovered on one channel and be killed. `probe_reach.py` must show 0 units uncovered by the rule.
  - **Item 3, residue.** R1 and R2 are applied, and the PR body says the lower edge is ruled.
  - **STOP condition:** any swept case changes its grade or its listing.
- **Earlier ruling (issuecomment-6442502921).** The round-7 STOP was ruled, and the lower edge stands.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open. There is one RESIDUE item (PR-body wording) and two SUGGESTIONs.

- **The rule is stated in all five places the ruling names, consistently.**
  - `REQUIREMENTS.md:408-419`
  - `docs/testing/TESTING.md:1487-1501`
  - `AUDIO_COUNTER_LIMITS[0]` (`tb/tools/torture_campaign.py:3752-3759`)
  - the `audio.counter-classified` text (`:3338-3348`)
  - the PR body's `audio` row and Round 8 section
- **The old position claims are gone.**
  - Neither "no earlier than 63 … no later than 63" nor "listed from its first word" remains in any current-state statement.
  - The only remaining matches are quoted findings, and Round 6 and 7 history paragraphs that each say Round 8 replaced the bound.
  - Some stated limits still describe where a reading places a slip, for example "the corruption reads first and the slip is located after it". These are pinned readings of bit-identical byte patterns, not promises about where a listing begins, and they do not contradict the coverage rule.
- **The gate checks exactly the ruled overlap.** `_fuzz_reach` (`:9437-9442`) returns `max(low - last, first - high, 0)`. `reaches` (`:9479-9482`) accepts a distance of at most `AUDIO_GUARD_FRAMES` (= 63, `:3715`), on a channel the unit changes, from a DUT listing. That is overlap with [first - 63, last + 63], where a slip's samples include `located_within`, as the documents now define.
- **No grader line changed** (the `git diff 5fdabc1c..a7a514fb` delta).
  - The commit changes strings, docstrings, two failure messages, one test name and one added control.
  - So the STOP condition cannot be met by this delta. The author's swept-case dumps are byte-identical across both heads (hash-verified below).
- **The two kept qualifiers are needed and were flagged publicly.** They are "the bytes show" and the void exception.
  - They are not in the ruling's words.
  - Without them the rule is false at the gate's pinned `clean`, `cancelled` and `masked` cases (`:9520-9526`).
  - They were already present at the head the STOP ruling sent to review.
  - The executor named them as an open risk in the REVIEW READY comment, so they are not a hidden assumption. Manager acknowledgement is listed under pending duties.

## Findings

### R1 RESIDUE: Docs. A Round 7 history sentence in the PR body reads as a current bound

- **Where:** the PR body, Round 7 section, the sentence after "**One point of the ruling was left for a decision.**" (line 167 of `receipts/pr_body.txt`): "The ruling's bound, outside the scope, is that each listing falls at or after the event's first word and no later than 63 samples after its last word."
- **Evidence:**
  - The sentence before it says the STOP ruling stands for the lower edge (no earlier than 63).
  - "The ruling's bound … is" then refers to the round-7 assignment's stricter wording, in the present tense.
  - Two different rulings sit in adjacent sentences, and neither is the current rule, which is coverage.
- **Impact:** wording only. A cold reader may take "at or after the first word" as a current bound. It changes no figure, test, code or verdict.
- **Exact fix:** replace "The ruling's bound, outside the scope, is that" with "The round-7 assignment's bound, outside the scope, was that".

### S1 SUGGESTION: Tests, Docs. Pin the coverage rule's text in the plan

- **Where:** `test_release_assertion_text` (`tb/tools/torture_campaign.py:7606-7617`).
- **Evidence:**
  - That test pins only the class names of `audio.counter-classified`.
  - No test or control pins the coverage sentence, either in the assertion text or in `AUDIO_COUNTER_LIMITS[0]`.
  - So an edit that dropped "overlap its first word minus 63 to its last word plus 63", or "coverage, not position", from the emitted plan would pass every gate. This is not new in this round: the round-7 bound was not pinned either.
- **Optional change:** add those phrases to the test's `(name, phrase)` list, and optionally one text control in the mutant driver.

### S2 SUGGESTION: Docs. The gate test's name predates the coverage wording

- **Where:** `test_audio_compositions_never_pass_and_list_every_event` (`:9507`). The name appears in TESTING 6d, the mutant driver and the PR body.
- **Evidence:** the rule is now "covered … by at least one listing". "List every event" is still true in a loose sense, so this is cosmetic.
- **Optional change:** a later rename to `..._never_pass_and_cover_every_event`. Not needed for this round.

## Prior findings at this head

R699-7's report was read after my own pass over the delta.

| Finding | Status at `a7a514fb` | Evidence |
|---|---|---|
| R699-7 F1 (MINOR): an event inside a constant-mask excursion is listed only by the excursion's listing, or after its return, outside the stated bound | **Resolved by the round-8 ruling, option (b).** The documents now promise coverage outside the scope, and the gate's overlap check is exactly that promise. The gate now asserts coverage for every unit of its 384 compositions. | **Text:** the five statements listed under Verdict.<br>**Gate:** `:9437-9512`.<br>**Control #298** (`tb/tools/torture_release_audio_mutants.py:233-237`): my named-test run kills it at seed 0 with `('a DUT event is not covered', 'slip', 245, 3, 'FAIL', …)` (`receipts/probe_m298.log`), and the pristine copy passes (`receipts/probe_pristine.log`).<br>**My independent coverage count** (not using `_fuzz_reach`) over the gate's seeds: 1,771 unit-channels, all covered (`receipts/fresh/arm_16384_0_288.jsonl`, `nested_{8192,16384}_0_48.jsonl`). The author's census also reports 1,771. |
| R699-7 R1 (RESIDUE): "mostly slips" | **Applied.** It now reads "slips in three draws of seven". | `docs/testing/TESTING.md:1510`, `_fuzz_nested` docstring `:9421`. In the PR body, the phrase now appears only in the quoted finding. |
| R699-7 R2 (RESIDUE): the lower edge was called an open decision | **Applied.** The PR body now says "(as ruled in issuecomment-6442502921)", and the known-limitations risk is closed with the same link. | PR body, Round 7 item 1 and the risk list (`receipts/pr_body.txt`). |
| R699-7 S1 (SUGGESTION): let the nested family reach control #295 | Not adopted, with a reason. Under the coverage rule, #295 only moves a listing that still covers its event, and the pin keeps the reading visible. This is optional and consistent with the ruling's last sentence. | PR body, Round 8 table |
| R699-7 S2 (SUGGESTION): the masked allowance is wide | Not adopted, because a void blocks the release. It stays optional. | `:9489-9492` |
| R699-6 and earlier R699 findings; R700-1 to R700-3 findings | **Resolved** as recorded at their heads. No grader, plan, soak or power line changed in this delta, so their causes are untouched. | `git diff 5fdabc1c..a7a514fb`, string and docstring hunks only |

## Probes and gates at this head

All runs are rc 0 unless stated. Receipts are in `receipts/`.

**Gates**

- `torture_campaign.py --self-test`: 120 tests OK in 31 s (`selftest_head.log`).
- `python3 -B -m behave tests/features/torture_campaign_plan.feature`: 176 scenarios and 665 steps passed (`behave_plan.log`).
- `docs_check.py` and `check_doc_paths.py` (both run under the system and the pinned renderer environment), `check_doc_style.py`, `check_py_idiom.py`, `git diff --check e76a755a HEAD`: all clean.
- `gen_toc.py --check`, `gen_toc.py --verify-anchors` and `check_em_dash.py --base e76a755a`: 0 findings. These ran under the existing pinned renderer environment (cmarkgfm 2025.10.22, html5lib 1.1, CPython 3.14.8), which the repository's renderer check accepts. Without it they exit 2, and those runs were overwritten and are not counted.
- **Delta lines:** no em dash, and no lane label, review round, reviewer ID or comment ID (scan of the added lines). `L3` is the methodology level tag (`docs/testing/methodology.md:63`), not a lane label.

**Control and edge probes**

Each probe runs the two named tests (the gate and the interrupted-excursion pin) against a scratch copy, using `scripts/run_named.py` and `scripts/gen_mutants.py`:

- **pristine:** both pass.
- **m298** (control #298 exactly as the driver states it): the gate fails at seed 0, "a DUT event is not covered". Killed.
- **s64** (DUT slip listings on channel 3 moved 64 samples later): the gate fails at seed 0, "not covered". Killed. The coverage edge is tight from outside.
- **s63** (the same shift, 63 samples): seed 0's coverage holds. The gate then fails at seed 35, on the stray check, because a slip whose `located_within` lay after its word moves beyond 63. This is informational: it is consistent with the overlap rule, and it is not a coverage refusal.

**Fresh-seed falsification** (`scripts/fresh_seeds.py`, `scripts/run_fresh.sh`, summary in `receipts/fresh_summary.txt`)

- **What was run:** 16,000 new compositions, 4,000 per family and capture length, at seeds 20,000 to 23,999. These lie outside both the gate's seeds and the author's 0 to 9,999 census. The gate's own 384 compositions were run as well.
- **Gate result:** the head's `_fuzz_check` refuses none, and no composition with a DUT unit grades PASS.
- **Independent coverage count**, by my own overlap code:
  - 79,173 unit-channels, of which 79,080 are covered.
  - The 93 uncovered ones all fall in runs the gate excuses:
    - `masked`: void (NOT RUN), with a missed arm at the unit;
    - `cancelled`: the channel's words equal a clean run's without the unit, so "the bytes show" nothing.
  - None is unexcused.

**Author evidence** (public evidence branch, commit `9bae445a`, `receipts/author_evidence_check.txt`)

- **Manifest:** all 82 `author-r8/` files match their `MANIFEST.json` digests, and none is unlisted. Neither the evidence commit nor the head commit is GPG-signed, so integrity here rests on the manifest digests.
- **Gate summary:** `rc.txt` shows every gate at rc 0.
- **Mutant driver:** "PASS: 298 mutations killed; source unchanged", from 13:39:15Z to 16:30:47Z. Its recorded file hashes equal the exact-head bytes of all three planner and driver files.
- **Head identity:** `head.txt` names this head, this tree and the base gitlinks.
- **Sweep comparison:** `sweeps_compare.log` reads IDENTICAL, 445 cases, sha256 `284796a0…`. The digest JSON reads `5f0b7f12…`, the same at both heads.
- **Not rerun:** I did not rerun the 2 h 51 min serial driver; I ran the new control myself.

**Hosted, inspected only** (`hosted_checks.txt`, read during the review): 8 success, 1 skipped, 31 queued or in progress. The docs and Yosys shards were still pending. The manager owns hosted and act acceptance.

**Clone restored** (`restore_check.log`)

- Porcelain, including ignored files, is empty.
- Index and worktree match HEAD.
- The `ls-files -s` digest equals the tree digest.
- All six gitlinks equal the base `e76a755a`.
- No non-document, non-`tb/tools`, non-`tests` path changed since the base.

## Lens coverage

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-8 ruling items 1 to 3 and the STOP ruling, checked against `REQUIREMENTS.md:408-419`, `TESTING.md:1454-1457`, `:1487-1501` and `:1532-1535`, `AUDIO_COUNTER_LIMITS[0]` `:3752-3759` and the interrupted-excursion limit `:3812-3814`, the assertion text `:3338-3348`, and the PR body's `audio` row and Round 8 section. Gate semantics at `:9437-9512` were checked against the ruled overlap. Fresh-seed probe. | R699-8 | `a7a514fbf5572ce08394cd727c9cc9085745c79f` |
| RTL | CLEAN | No RTL, firmware, builder or gitlink change in `5fdabc1c..a7a514fb` or since the base (`restore_check.log`). No grader logic line changed in the delta: the hunks in `torture_campaign.py` are strings, docstrings, messages and a test name. The rest is carried from R699-7 at `5fdabc1c`, whose scope this delta does not touch. | R699-8 (delta); R699-7 (rest) | `a7a514fbf5572ce08394cd727c9cc9085745c79f` |
| Robustness | CLEAN | 16,000 fresh compositions over both families and both capture lengths, plus the gate's 384, with independent coverage, excuse classes, refusals and PASS counted (`receipts/fresh/`). Edge probes s63 and s64. | R699-8 | `a7a514fbf5572ce08394cd727c9cc9085745c79f` |
| Tests | CLEAN (S1 optional) | Gate `:9460-9541`: `_fuzz_check`, `reaches`, the stray check and the failure words. Renamed pin `:9575-9600`, with its assertions unchanged (diff). Control #298 at `tb/tools/torture_release_audio_mutants.py:233-237`, killed by name. s64 killed. Self-test 120 OK. Plan feature 176 scenarios. The author's 298-control driver receipt was hash-verified against the head bytes. | R699-8 | `a7a514fbf5572ce08394cd727c9cc9085745c79f` |
| Docs | CLEAN (R1 is RESIDUE, S2 optional) | `REQUIREMENTS.md:396-432`, `TESTING.md:1405-1540`, `AUDIO_COUNTER_LIMITS`, and the docstrings of `_close` `:4859-4862`, `_fuzz_nested`, `_fuzz_check` and the gate. The PR body, with every line citation it gives for round 8 opened and matched. Docs, path, TOC, anchor, em-dash, style and idiom gates. | R699-8 | `a7a514fbf5572ce08394cd727c9cc9085745c79f` |

## Real limits

- My probes are seeded samples, not exhaustive. The counts bound nothing beyond the seeds run.
- I did not rerun the full 298-control serial driver. I ran the new control and two edge probes, and hash-checked the author's driver receipt against the exact-head bytes.
- I did not run the full `cd tests && behave` tier, only the torture plan feature. The full tier is in the author's `rc.txt` (`bdd_conformance` 0).
- Physical calibration was NOT RUN. Acceptance items 3 and 4 are part B, and field skips are not hardware proof.
- No manager source bank runs at this head, and I claim none. Source-head execution evidence is the author's published receipts and my focused runs above.

## Pending manager duties

- Acknowledge or rule on the two qualifiers kept beside the ruling's words: "the bytes show" and the void exception (`REQUIREMENTS.md:408` and `:413`). This review finds both necessary for the rule to be true at the gate's pinned allowances.
- Carry R1 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `e76a755a`, live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`), and link the builder and native receipts on the PR.
- Hosted and act acceptance at the exact head. The docs and Yosys shards were pending when read.
- Part-B routing stays open: REBOOT and the sine limits (issuecomment-6409128703), and `restore_bound_s = 30`.

## Receipts

- **Where they are listed:** `MANIFEST.sha256`. `receipts/pr_body.txt` is a copy of the public PR body, read at this head.
- **How the scripts run:** as `python3 -I <script> …`. They import only a scratch copy of `tb/tools/torture_campaign.py`, or, in `gen_mutants.py`, `tb/tools/torture_release_audio_mutants.py` from the clone.
- **Not published:** the evidence clone and the mutant copies, which live under `scratch/`.

R699-8 FINISHED
