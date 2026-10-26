[A674d] REVIEW READY - round 4
Commit: `85da3e4595871c1573c28b4d040b9e98463a41c9` (tree `9ed9c6f592675f0e9bf59858b80a77c6255ccb22`), branch `396-release-gate-plan`. One round-4 commit sits on round 3 `4d69e1923ce8209029af6e084336f13cca834c29`, which is not rewritten. Base is dev `e76a755a`. Not pushed.

Changed (answers R699-3 under issuecomment-6417665116):
- F1, at its cause in the window's labelling.
  - The offset in force before the last change stays a candidate.
  - The offset nearest the one in force is kept while it fits, so each slip takes the smallest size and a slip of whole blocks sits at the first word that shows it.
  - A departure ends at the first word from which every word up to its return fits the offset in force.
  - A whole-block slip's `located_within` runs on to the first word that shows it, the resync included. A corrupted word bounds it only where the tracks differ.
  - Where the bytes allow two readings, the planted-arm log decides at a logged arm. The arm-led reading is taken only with no more DUT events and more arms found, so the log never hides a DUT event, and an arm the capture does not show stays missed.
  - A one-word corruption followed within 64 samples by a whole-block slip is graded as both events, except in byte-identical shapes, which are stated and pinned.
  - After the planted flip arm, or beside any arm at another sample, a DUT slip FAILs with every arm found, at every size swept.
- F2: the constant-mask rule holds in both named shapes.
  - Only the window's trailing words under the closing mask start a hold.
  - A word on the old track is the return, never a release.
  - On return, the excursion ends where the old track's words began, and the rest of the window is graded against the old track.
  - A one-word event within 64 samples on either side is its own event. A code-bit corruption over whole blocks is one `bit-flip` wherever it ends.
- The bit-identical shapes are stated exactly in TESTING 6d, REQ-VER-06 and `counter_limits`, and a self-test arm pins each by comparing bytes:
  - a code-bit corruption that turns its word into the new track's before a slip of whole blocks;
  - the code-bit tie in either order;
  - a slip followed within coincident words by a slip of whole blocks;
  - a DUT slip at a planted slip arm's own sample;
  - a constant-mask corruption that a slip interrupts.
- S1 adopted: the interval decides what is proved clean, not the class. S2 adopted: both void reasons name a channel the DUT never drives with the counter.
- The audio-grader release controls moved to `tb/tools/torture_release_audio_mutants.py`, and the capture helpers to `tests/steps/torture_audio_model.py`, under the 1000-line module rule.

Validation, at this head, foreground except the driver, all rc 0:

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 112 tests OK (108 before) |
| `python3 -B tb/tools/torture_release_mutants.py` | `PASS: 271 mutations killed; source unchanged` (22 added, 4 re-anchored) |
| `cd tests && behave --no-capture -f plain` | 495 scenarios, 2286 steps |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 176 scenarios |
| `docs_check.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base origin/dev`, `check_doc_style.py`, `check_doc_paths.py` under the pinned renderer | 0 findings |
| `check_py_idiom.py`; `check_feature_status.py` and `--self-test` | at ratchets; 0 findings |
| `--coverage-by-area --areas soak,audio,power`; `git diff --check origin/dev HEAD` | complete; clean |

Each new self-test arm fails on `4d69e192`, and 11 of the 14 new scenario examples fail there. The other three are controls.

R699-3's probes, rerun unmodified, byte-identical to the published manifest:
- `r3_arm_void_probe.py`: no NOT RUN line (0 of 256 not FAIL at every size).
- `r3_cluster_probe.py`: FB 654/6, SB 258/2, CF 32/0, CB 40/0, against 433, 89, 28 and 12 deviations before.
- `r3_probe.py`: E 642/6, S 1170/0, M 273/0, A 21/8.
- Every remaining deviation is checked with the reviewer's own encoder and is its stated limit:
  - the FB and SB lines give the same bytes as the slip alone, or one slip of the sum;
  - 4 A lines FAIL with every arm found and with `located_within` holding the slip;
  - 2 A lines put the DUT slip at a slip arm's own sample;
  - 2 A lines are a constant-mask corruption that the planted repeat interrupts;
  - the 6 E lines are S1's case.
- Round-2 probes:
  - compound 30/30;
  - arm probe A2 to A5 FAIL;
  - `grader_probe_r2` has the same OK and DEVIATION per case as at `4d69e192`;
  - the `required_s` port is 110 OK plus P5;
  - N07 at 8214.
- `reviewer_mutants_r2.py`: 31 KILLED, 0 SURVIVED, 1 INVALID. N15, ported to its new line, is killed.
- `r3_reviewer_mutants.py`: 13 KILLED, 0 SURVIVED, 3 INVALID. V07, V09 and V13, ported to their new lines, are killed.
- Two sweeps with the reviewer's encoder place DUT slips of 17 sizes from 1 to 8192 samples, most both ways, 1 to 64 samples either side of all six arms. All 39936 placements FAIL with every arm found.
- R700-3's probes, as byte-identical copies:
  - delta, qualified and ambiguity outputs are byte-identical to `4d69e192`;
  - in the boundary matrix, `compound-4096-1-80000` now meets its compound rule;
  - `compound-4096-5-100` is the stated code-bit tie, read corruption first and pinned by bytes.

Acceptance criteria: unchanged. Items 1, 2 and 5 and the desk half of item 4 are met. Items 3 and 4 need the bench (part B), so the body says "Relates to #396".

Open risks/questions:
- Ties between byte-identical readings take a stated convention: corruption first for the code-bit tie, and the single-bit mask beside a whole-block slip. The planted-arm log decides at a logged arm.
- The serial mutation driver now takes about 90 minutes.
- Owner decision issuecomment-6409128703 is still outside the plan text, and `restore_bound_s = 30` stays provisional, both for the manager to route.

HANDOFF.md, PR-BODY.md (with a Round 4 section), the scripts and the receipts with a generated index are in the assigned output directory. No push, PR operation, merge, hardware or bench action.
