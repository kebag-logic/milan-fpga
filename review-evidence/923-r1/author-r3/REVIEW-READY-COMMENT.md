[A789] REVIEW READY (#923 and #924, round 3: R848-1 and R847-1 answered)
Commit: `d06ded5a` (branch `923-aecp-maps`, on round 2's `70c100da`; local, the manager pushes)

Changed (tests, one plant table, two comments or docs; no compiled source):
- R848-1 F1, the late-reply store model (`sw/firmware/ctrl/test/test_aecp.cpp` `Far`, `88676700`). The release engine reserves the transaction at an accepted commit-begin, and each record's commit and the finish complete without back-pressure (`KL_aecp_engine.sv:465`). The model now follows that contract.
  - A begin, validation or commit-begin with no answer is held and not taken.
  - A commit or finish with no answer is taken, and only its reply is lost.
  - `Face.AnUnansweredEditFailsUntilItsCommitIsReserved` checks store/map agreement after its phase-5 and phase-2 cases.
  - New: `Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing`. A two-record ADD and REMOVE, the second then the first record's reply lost.
  - New: `Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing`. The restore's removal of the reset set, with the restored map empty, and its addition of a restored set, each record's reply lost in turn.
  - Each case asserts SUCCESS (the command cases), the lost reply counted, the map, and `agree(14)`.
  - Plant `window-lost-reply-stops-the-commit`: the face stops committing at a lost reply. Caught by both new tests by name.
  - The AECP README states the guarantee. Delivery loss after the commit-begin is outside the contract, with no recovery invented.
- R847-1 F1, the face's `pick` (`d06ded5a`). New: `Face.AnEditCommitsTheMappingsTheCorePicksAndNoOthers`, through the face and the `EDIT` window.
  - An ADD of a held and a new mapping validates and commits the new one alone, COUNT 1.
  - A REMOVE naming a mapping twice commits each distinct mapping once, COUNT 2.
  - The records are asserted, and `agree(14)` after each.
  - Plant `window-pick-ignored`: caught by name.
- F2 (both reviews, `08901183`): `plat/README.md:111` now gives 1,280 B of `rom` past what 56.0 held, section 5's figure.
- R848-1 F3 / R847-1 R1 (`63c60ad9`): the ledger comment names the cold-code-to-flash work in place of a lane.

Validation (clean clones of `d06ded5a` unless named):
- Workflow jobs of `rtl-fast.yml`, `elaborate.yml` and `docs.yml`, step by step (`verify_wf.py`): 118 steps rc 0, 130 not run with their reasons, 0 bad: among them the AECP (331 of 331), SRP (421 of 421) and control (716 of 716) campaigns, `fw_coverage.py --check` (PASS, 39 files), the docs jobs, the publication census and `ctrl_boundary.py`.
- AECP app arm, 1 and 2 interfaces: 164 tests PASS (161 before, plus 3).
- Every edit, window and restore plant (32, at `88676700`) is caught by name, and `window-pick-ignored` by its own run; the whole AECP campaign is 331 of 331 at `d06ded5a` (above). R847-1's `r847_probe_mutants.py --only face-pick-ignored`: the new test fails; the unplanted control passes.
- Round 2's model, which dropped the write with the reply, on a scratch copy: all three late-reply tests fail on "GET_AUDIO_MAP and the datapath's store hold the same mappings". A suppressed write no longer passes.
- The platform images are byte-identical to `70c100da`'s and the routed ones, by `ctrl_app.elf` sha256:
  - 1x1/1if `caec0abc`;
  - 8x8/1if `59b9b736`.

  Their exports are identical: init files, and the Verilog outside its comments. The release image is byte-identical (`bios.bin` at both configs). So round 2's routes, CPU budget harness and 4-shard sweep carry unchanged. That includes the 1x1/1if hold miss, owed to #927 (issuecomment-6923091710).

Acceptance criteria: #923 and #924 met, as at `70c100da`. The review findings are fixed with tests that fail for their defects.

Open risks/questions: none new. SET_STREAM_INFO bodies past 84 octets are #926's. The 1x1/1if hold miss is #927's. R847-1's suggestions S1-S4 are not taken in this round.
