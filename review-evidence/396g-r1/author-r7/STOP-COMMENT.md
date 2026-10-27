[A674g] STOP - round 7
Commit: `5fdabc1c4c76206bd2528435c56d88466c0f972e` (tree `dcf4ae711002ba47e61a61a85eb4369ac63a8fce`), branch `396-release-gate-plan`.
Two round-7 commits sit on the round-6 head `b206d88b937257ca5ccf1753c5fa211605c9f7e6`, which is not rewritten:

- `73be3b36`, F1: an excursion that a slip interrupts is listed from its first word, with its pin and its control;
- `5fdabc1c`, the listing bound in every document, the gate for it and two controls.

Base is dev `e76a755a`. Not pushed.

**Why STOP: one sentence of ruling item 1 cannot be written true without changing swept listings.**
The ruling's bound outside the scope is "each listing falls at or after the event's first word and no later than 63 samples after its last word".
The upper edge is implemented as written. The lower edge, "at or after the event's first word", is false at `b206d88b` and at this head:

- **Inside the scope:** `test_audio_composition_sweep` pins 8 cases listed one sample *before* the event's word.
  Each is a one-word corruption under `0x1E00` on a drop arm's next sample (7493 at 8192 frames, 15685 at 16384, both channel pairs).
  It reads first, at the arm's sample: the stated limit "the bytes are the same either way", which `_sweep_case` checks.
  Making the edge true would move those swept listings, which is this round's STOP condition.
- **Outside the scope:** the gate's own seeds break it.
  - Arm-led seed 14: a DUT repeat of 1024 at 699 beside the flip arm at 700, listed at 698 on channel 1.
  - Nested seed 16: two slips of whole blocks seven samples apart, read as one slip of their sum one sample before the second.
- **Measured:** over 10,000 seeds per family and capture length, the literal edge refuses compositions that this head's gate passes:
  - arm-led family: 30 at 16384 frames and 34 at 8192;
  - nested family: 60 and 51.
  The refused listings are 1 to 5 samples early, each within 64 samples of another event or a planted arm, where a stated limit reads the same bytes with the event earlier.

So the head states the lower edge as round 6's: "no earlier than 63 samples before the event's first word".
**Decision requested:** accept that lower edge (the head is then review-ready as it stands), or rule otherwise.
Ruling otherwise needs a grader change that moves swept listings.

Changed (answers R699-6 under issuecomment-6435672624):
- **F1, item 3, first option (contained).**
  - The cause: `_returned` records the excursion's bit-flip ahead of the window's own events. `_split`'s re-read then replaced the events before the hold with a read of the window's words only, so the bit-flip was lost.
  - `_close` now keeps it apart and records it first. The interrupted-excursion limit says so.
  - Pin `test_audio_excursion_a_slip_interrupts_is_listed_from_its_first_word`: R699-6's minimal case, listed first as `bit-flip 1673 0x00080100` at 4424. It fails when transplanted onto `b206d88b` (first listing `dropped 1021` at 6097). Control #295 fails it.
- **Item 1.** REQ-VER-06, TESTING 6d, `counter_limits[0]`, `audio.counter-classified` and the PR body now state:
  - listed on each channel it changes, unless it masks an arm and voids the run;
  - a listing's samples are its words, and for a slip `located_within` as well;
  - each listing falls no earlier than 63 samples before the event's first word and no later than 63 after its last;
  - inside the scope, within 63 of the first word.
- **Item 2, the gate.**
  - The fuzz measures each event from its words, first to last.
  - Where a run fails without voiding, every DUT listing must also fall so near an event on its channel ("each listing"). A void run's missed arm leaves its own records as DUT listings, so that half skips void runs.
  - A nested family adds 48 compositions per capture length (8192 and 16384). Each is a constant-mask excursion of 64 to 2100 words anywhere, with DUT events inside it, half less than 64 samples before its return. A slip lies inside the excursion in 62 of the 96.
  - Controls #296 (a corruption of two or more words listed after its last word plus 63) and #297 (listed again there) fail it at seed 0. Without the each-listing half, #296 fails at seed 1, "a DUT event is not listed".
- **S1** adopted through the bound: seed 2017152 passes. The nested family found one more oracle artefact (nested seed 3468): the cancellation rebuild reordered units. It now keeps the composition's order.
- **S2** not adopted: a void blocks the release. **S3** adopted in the PR body.

STOP condition check (a swept case changes its grade or its listing): **not met.**
- Every capture of both in-tree sweeps (445, with the stated voids and clean captures) was dumped with verdict, missed arms, reason and full event list. The dumps at `b206d88b` and `5fdabc1c` are byte-identical.
- R699-6's scripts, unchanged at this head:
  - `probe_gap.py`: 0 of 6,720 over 63 (48 at `b206d88b`);
  - `probe_fuzz.py` at 8192 frames, 2,000,000-2,019,999: 0 violations (2 at `b206d88b`);
  - byte-identical to R699-6's receipts: `probe_fuzz.py` at 16384 frames (1M range and 0-287) and `probe_isolated.py` at both lengths.

Validation, at this head, all rc 0:

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 120 tests OK (119 before) |
| `python3 -B tb/tools/torture_release_mutants.py` | `PASS: 297 mutations killed; source unchanged`, 2 h 51 min (3 added) |
| R699-6's `probe_mutants.py`, all controls, 6 jobs | 297 of 297 killed; slowest 352 s |
| `cd tests && behave --no-capture -f plain` | 495 scenarios, 2286 steps |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 176 scenarios |
| `docs_check.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base origin/dev` (and `--base e76a755a`), `check_doc_style.py`, `check_doc_paths.py` under the pinned renderer | 0 findings |
| `check_py_idiom.py`; `check_feature_status.py` and `--self-test` | at ratchets; 0 findings |
| `--coverage-by-area --areas soak,audio,power`; `git diff --check origin/dev HEAD` | complete; clean |

Acceptance: unchanged. Items 1, 2 and 5 and the desk half of 4 are met at the desk. Items 3 and 4 are part B, so the body says "Relates to #396".
Open risks/questions:
- The lower-edge decision above.
- The nested family rarely reaches R699-6's exact late-listing mechanism (15 of 5,000 at `b206d88b`, none of its 96); the pin covers it.
- issuecomment-6409128703 (REBOOT, sine limits) and `restore_bound_s = 30` still need routing, as before.
