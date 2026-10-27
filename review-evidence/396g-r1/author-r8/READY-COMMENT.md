[A674h] REVIEW READY - round 8
Commit: `a7a514fbf5572ce08394cd727c9cc9085745c79f` (tree `7bdbb8703e4e4dd34c86adb234af37ec68a2e6d3`), branch `396-release-gate-plan`.
One round-8 commit sits on the round-7 head `5fdabc1c4c76206bd2528435c56d88466c0f972e`, which is not rewritten. Base is dev `e76a755a`. Not pushed.

Changed (answers R699-7 under issuecomment-6443031364):
- **Item 1, the rule.** REQ-VER-06, TESTING 6d, `AUDIO_COUNTER_LIMITS[0]`, the `audio.counter-classified` text and the PR body now state:
  - a capture with a DUT event the bytes show never grades PASS;
  - each such event is covered, on each channel it changes, by at least one listing whose samples overlap its first word minus 63 to its last word plus 63 (a listing's samples are its words, and for a slip `located_within` as well);
  - a DUT event inside a constant-mask excursion on the same channel may be covered by that excursion's listing alone;
  - inside the exactness scope each listing begins within 63 samples of the event's first word (at its `capture_index`); outside it, coverage, not position.
  - Every outside-scope sentence about where a listing begins is dropped. That includes the interrupted-excursion limit's "listed from its first word", in TESTING 6d and `counter_limits`. It also includes the pin's name: it is now `test_audio_excursion_a_slip_interrupts_keeps_its_bit_flip`, with its assertions unchanged, recording one reading.
  - Kept from the head the STOP ruling sent to review, and flagged here, because the rule is false at pinned cases without them: "the bytes show" (events that cancel, or only move an arm within its tolerance, leave a clean run's bytes) and the void exception (an event that masks a planted arm at its sample voids the run).
- **Item 2, the gate.** `reaches` already was the ruling's overlap, so no gate logic changed. Its docstrings and failure words now say "covered". The fuzz asserts coverage for every unit of its 384 compositions (288 arm-led, 96 nested). The two sweeps still assert exact listing in the scope.
  - New control #298, a DUT slip's listing removed on channel 3: the gate fails at seed 0, `('a DUT event is not covered', 'slip', 245, 3, 'FAIL', …)`.
  - R699-7's `probe_reach.py`, unchanged at this head: its five outputs are byte-identical to R699-7's receipts. An independent check of each unit it reports finds **0 uncovered by the rule**. The 12 gate units, and 450 of the 454 in seeds 0-1999, are covered by the excursion's own listing; another overlapping listing covers the other 4.
  - Census over the gate's 384 compositions and 10,000 per family and capture length: the gate refuses none. Every uncovered unit-channel is void beside a missed arm or excused as cancelled or clean.
- **Item 3, residue.** R1 as written ("slips in three draws of seven", in TESTING, the `_fuzz_nested` docstring and the PR body). R2 as written: the PR body says the lower edge was ruled in issuecomment-6442502921 and closes that risk with the same link.
- **S1** not adopted: with control #295 applied, every event stays covered, so `_fuzz_check` and the gate pass and only the pin fails. What #295 changes is a position outside the scope. **S2** not adopted: a void blocks the release.

STOP check (a swept case changes its grade or listing): **not met.** No grader line changed. Every capture of both in-tree sweeps (445) dumps byte-identically at `5fdabc1c` and this head. Inside the scope, all 4,356 swept events in captures that do not void have a listing beginning within 1 sample of the first word on each channel.

Validation, at this head, foreground except the driver, all rc 0:

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 120 tests OK |
| `python3 -B tb/tools/torture_release_mutants.py` | `PASS: 298 mutations killed; source unchanged`, 2 h 51 min (1 added) |
| R699-7's `probe_reach.py`, `probe_dump.py`, `probe_new_mutants.py` (last 4 controls) | byte-identical / byte-identical / all 4 killed by their named tests |
| `cd tests && behave --no-capture -f plain` | 495 scenarios, 2286 steps |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 176 scenarios |
| `docs_check.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base origin/dev` (and `--base e76a755a`), `check_doc_style.py`, `check_doc_paths.py` under the pinned renderer | 0 findings |
| `check_py_idiom.py`; `check_feature_status.py` and `--self-test` | at ratchets; 0 findings |
| `--coverage-by-area --areas soak,audio,power`; `git diff --check origin/dev HEAD` | complete; clean |

Acceptance: unchanged. Items 1, 2 and 5 and the desk half of 4 are met at the desk. Items 3 and 4 are part B, so the body says "Relates to #396".
Open risks/questions:
- The two kept qualifiers above are not in the ruling's words.
- issuecomment-6409128703 (REBOOT, sine limits) and `restore_bound_s = 30` stay with part B, as ruled.
