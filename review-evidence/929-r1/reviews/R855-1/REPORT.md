[R855] POSITIVE - exact head 372556835d03b70134b2e76567b63b25c4cca005

# R855-1: internal cleared-context review of PR #935 (issue #929)

- Head reviewed: `372556835d03b70134b2e76567b63b25c4cca005`, tree `34b71495c92a7dbee90c516354100ed61a51446e`. The PR is five commits on dev-soft-core `70f4056f` (`08ba6efa`, `6b8e5042`, `becca95f`, `a9a48546`, `37255683`).
- Reconstructed from: AGENTS.md, issue #929's body and its three comments (the third finding, TAKEN, REVIEW READY), the PR body, `git diff 70f4056f..37255683` and its history, and the author packet at archive `c836e7a8` (`review-evidence/929-r1/author-r1`). I then ran my own executions on fresh clones.
- Prior public review findings on PR #935: none. The only earlier PR comments are the two review-start notices, so there is nothing to resolve or retain.
- Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. There are two RESIDUE items (wording only) and two SUGGESTIONs.

## What was checked, and the evidence

### (1) The twin: the `split-talker-failed` owed row

**The deletion rests on evidence.** I ran `make twin` on a fresh clone of the head (`receipts/twin/head-twin-then-plants.log`, rc 0).
- The result is `twin: 0 finding(s)`. The owed notes are `stream-output-0-notices`, `entity-available-index`, `fabric-mvrp-leave-all`, `fabric-domain-one-new` and `fabric-vid2-join-in`, matching the PR's expected result.
- Both captures hash identically to the author's base and #932 captures:
  - `fabric.json` `fa6a5a12…`
  - `split.json` `7cc8a5d2…`
  - Receipts: `receipts/twin/head-captures.sha256` against the author's `captures-base-and-932.sha256`.
- So the simulated behaviour is the base's. Only the harness changed.

I decoded the Talker attributes with the twin's own decoder (`scripts/talker_traces.py`, output in `receipts/twin/head-talker-traces.txt`):

| Half | Talker attributes | Messages |
|---|---|---|
| Split | exactly one: Talker Advertise for StreamID `0200000000010000` | New x2 from 5190 ms, JoinMt x19, Lv at 20190 ms |
| Fabric | the same StreamID | New x2 from 5200 ms, JoinMt x15, Lv at 20000 ms, Mt x5 |

- The split declares no Talker Failed for either source.
- The deleted row claimed "Talker Failed for both sources' streams from boot, never withdrawn". That is false at the base and at the head, and the row's stated cause (no SRP adapter entry takes MAAP's allocation) is what #895 removed.
- Deleting the row is what the twin's own rule asks for (README: "the lane that fixes it deletes the row").

**This is not a weakening.** In `twin_compare.py:616`, `owed_msrp` is the set of keys the owed rows select, and `compare_declarations` (`:642`) leaves those keys out.
- At the base, the row's selector (`k[0] in (1, 2)`) took every Talker attribute out of the LeaveAll-boundary comparison.
- With the row gone, the Talker attributes are compared at the boundaries and graded against Table 10-3 like every other MSRP attribute. The check is wider than before.
- What is lost is the row's pin of each half's whole FirstValue, which included TSpec. That is the KNOWN MaxFrameSize item (73 vs 217), excluded here as instructed.

**Plants.** `make twin-plants` passed (rc 0, same log): 42 `REFUSED` lines, 21 plants each refused against its own half and between the placements, and 0 `ESCAPED`.
- `talker-failed-back` (`twin_plants.py:231-263`) re-encodes the split's Talker Advertise vectors in place as Talker Failed:
  - It appends FailureInformation to each FirstValue: a 2-octet zero priority plus the frame's source MAC as Bridge ID, then code 2 (IEEE 802.1Q-2018 35.2.2.8.7, Table 35-6).
  - It sets AttributeLength to 34 and grows AttributeListLength.
  - It is refused by the boundary finding, and the finding names `{Talker Failed stream_id 0200000000010000; ...}`. So the twin decoded the plant as a well-formed Talker Failed, not as a parse fault.
- `srp-plus-k` is now refused by `MSRP Talker Advertise stream_id 0200000000010001`.
- `leave-all-declaration` is refused by the boundary finding, which now starts with the Talker's first boundary.
- Both restated strings are what the head's findings print, verbatim (log lines 1541/1556 and 1718/1732).

**Row restatement.** `stream-output-0-notices` keeps its values. Only its cause and owner are restated (`twin_compare.py:458-473`, README:1388), which is the KNOWN item.

### (2) dynmap-mutants on a fresh clone

The fresh clone has none of the five generated inputs before the run (`# before:` lines in `receipts/dynmap/head-fresh-dynmap-mutants.log`).
- I ran `make -C tb/verilator/milan_dp -j8 dynmap-mutants DYNMAP_MUTANT_JOBS=6` (rc 0, 3782 s).
- Every leg's control printed `[PASS]`, the listener's and the talker's included.
- The result was `71 checks: 71 PASS, 0 FAIL`, with 66 mutants caught.
- Afterwards the listener suite's `ltn_rom.hex`, `ucode.hex` and `tdm8r_aemi.bin`, and the talker suite's two inputs, exist.

`prepare()` (`dynmap_mutants.py:461`, called at `:644`) makes each selected leg's `-o` inputs through that suite's own make rules, and refuses the leg if make fails or an input is absent. This matches `build()`: the inputs are exactly its `-o` list.

I planted two one-off defects of my own on fresh clones, running mutants 36 (listener) and 37 (talker):
- **The make step replaced by `true`** (`receipts/dynmap/plant1-make-skipped.{diff,log}`):
  - `[FAIL] the listener leg's inputs are not made: its suite did not make ltn_rom.hex, ucode.hex, tdm8r_aemi.bin`
  - `[FAIL] the talker leg's inputs are not made: its suite did not make ltn_rom.hex, ucode.hex`
- **The prepare call removed** (`plant2-step-removed.{diff,log}`): `[FAIL] the unmutated gateware does NOT pass the listener leg (caught)`, which is the base's failure back.
- Both plant clones were restored to exact head bytes afterwards (`plant-clones-restored.txt`).

### (3) srp_mbx.cpp at the 8x8 entity

**Base failure reproduced.** I ran the base's `srp_mbx.cpp` with the same firmware (`receipts/srp/base-srp_mbx-4arms.log`):
- `StartupDeclaresTalkersDomainAndVlan` fails at 8x8 with one interface.
- `StartupDeclaresTalkersDomainAndVlan` and `OneLoopOwnsTheGlobalCentisecondDispatch` fail at 8x8 with two interfaces.
- Both 1x1 arms pass.

**Head passes.** `head-srp_mbx-4arms.log` shows 74 of 74 tests passing at 1x1 and 8x8, each at one and two interfaces.

**Firmware unchanged.** `git diff 70f4056f..HEAD -- sw/firmware/ctrl/srp sw/firmware/ctrl/app hdl` touches only `srp/README.md`. The rule the test now holds is the one in `srp_mbx.c:255-305` (`declare_sources`):
- Advertise when the source is allocated and admitted.
- Otherwise Failed, with code 1 if allocated and 2 if not.
- The fixture allocates only source 0 (`srp_fixture.hpp:71`), so the expected type comes from the fixture's input, not from adapter state.

**The test is now stricter, not looser** (`srp_mbx.cpp:281-327`):
- It requires exactly `3*CTRL_SRP_SOURCES` Talker declarations per interface.
- Each source must have three declarations under its own StreamID, with New/New/JoinMt timing, VID 2, MaxFrameSize 224, MaxIntervalFrames 1, PriorityAndRank 0x60, and code 2 when unallocated.
- At 1x1 this is at least the old test.

**The dispatch test is not loosened** (`:712-729`). Its pool is now two of the shape's SRP pools (`SRP_POOL_*`, `srp_mbx.h:140-147`), and it still holds that the second attach is refused.

**Plants.** In the two-interface campaign at 8x8 (`receipts/srp/head-plants-if2.log`, rc 0), every one was `[ok]` by its named words:
- the three new plants;
- the three kept plants that name the two changed tests (`startup-vid`, `duplicate-tick-owner`, `transmit-first-link-up-owes-nothing`), which are all six plants in `srp_mutants.DEFECTS` naming those tests;
- four probes of my own (`scripts/srp_probe.py`):

| Probe | Defect planted | Caught by |
|---|---|---|
| `r855-source5-advertised` | source 5 declared Talker Advertise although unallocated | `source 5 on interface` |
| `r855-last-source-undeclared` | the last 8x8 source never declared | `declares New, New, JoinMt` |
| `r855-vid-past-two` | sources past two declared on VID 3 | the VID check |
| `r855-if1-code-past-two` | the second interface's sources past two carry code 1 | `failure code` |

**At 1x1** (`head-plants-if1-at-1x1.log`), `startup-8x8-sources-past-two-undeclared` and `startup-8x8-failure-code-past-two` are `[ESCAPED]`, as claimed, so only the 8x8 arm catches them. The if1 campaign's name filter (`test_ctrl_firmware.py:209-216`) does not include them, so they cannot make that campaign fail.

**Wiring.** `fw_rv32_selftest.py --require-rv32` followed by `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` (the `firmware-unit` commands) gave rc 0 (`head-firmware-unit-shard0.log`).
- It shows `[ok] arm srp-srp_mbx-if{1,2}-endstation_ax7101_{1x1_tdm8,8x8}`, i.e. four arms.
- The result was `test_ctrl_firmware: PASS`.
- `fw_coverage.py --selftest` and `--check --jobs 4` gave `firmware coverage: PASS (39 files)` (`head-fw-coverage.log`).

### (4) Images

I did not rebuild the release or split images: the LiteX environment the author used is not available to this review.

**By construction, no image input changed.**
- The delta touches only `sw/firmware/ctrl/test/{srp_arms.py,srp_mbx.cpp,srp_mutants.py,test_ctrl_firmware.py}`, `sw/firmware/ctrl/srp/README.md` and `tb/verilator/milan_dp/{Makefile,README.md,dynmap_mutants.py,twin_compare.py,twin_plants.py}`.
- There is no change to hdl, firmware C or headers, or any gitlink.
- The image builders (`ctrl_srp_image.py`, `ctrl_plat_image.py`, `plat_arms.py`, `twin_fw.py`) import only `prepared` and `LWSRP_SOURCES` from `srp_arms`, and the diff leaves both unchanged: it only adds `mbx_entity_arms`.

**The author's receipts agree.**
- The split ledger's 24 hashes are identical between base and head.
- `plat_ledger: PASS` at all four points.
- The release `bios.bin`, disassembly and stripped ELF are identical. Only the whole ELFs differ, which is the stated debug-section path difference.

### Docs and gates

- `scripts/docs_check.py` reported 0 findings (`receipts/docs/head-docs-check.log`).
- `scripts/check_py_idiom.py` and `scripts/check_cpp_idiom.py` gave rc 0 (`head-idiom-gates.log`).
- Comment rule: every added line in the delta was scanned for lane labels, round or reviewer IDs and issue-comment IDs, and none is present. The delta removes one old lane label (the README's "S2b").

## Findings

**R855-1-01 — RESIDUE — Docs — stale plant count and owed-row summary**
- Where: `tb/verilator/milan_dp/Makefile:40` and `docs/design/MAILBOX_SPLIT.md:1650-1651`.
- Evidence: the head has 21 twin plants (`TWIN_PLANTS` 3 + `TWIN_CAPTURE_PLANTS` 12 + `TWIN_FABRIC_PLANTS` 6; the README says "twenty-one"). These two places still say "twenty plants". MAILBOX_SPLIT also says the owed list "holds what the SRP adapter round owes", which names the deleted row's cause.
- Impact: wording only. No figure, test or verdict reads these lines.
- Exact fix:
  - Makefile:40: "its twenty-one plants".
  - MAILBOX_SPLIT.md:1649-1651: "An owed-difference list, apart from the ledger, holds the split's STREAM_OUTPUT 0 notices (#665) and the fabric's #857, #858 and #860. Its twenty-one plants ...".
- Verification: `git grep -n 'twenty plants'` is empty.

**R855-1-02 — RESIDUE — Docs — "plants the row's old behaviour" overstates the plant**
- Where: `tb/verilator/milan_dp/README.md:1405-1406`, and the PR body's twin item ("(the row's old behaviour)").
- Evidence: `plant_talker_failed_back` changes only the declared type: the same single StreamID, events and timing, re-encoded as Talker Failed code 2. The deleted row's behaviour was Talker Failed for both sources, from boot, never withdrawn. The README table row (:1454) states the plant precisely.
- Impact: wording only. The plant is refused, and the fuller old behaviour would differ at more boundaries.
- Exact fix: "`talker-failed-back` plants the row's old declaration type: the split's Talker Advertise re-encoded as Talker Failed, code 2."

**R855-1-03 — SUGGESTION — Tests, Robustness — the talker leg passes without its declared inputs**
- Where: `receipts/dynmap/plant2-step-removed.log`, and the `LEGS["talker"]` entry at `tb/verilator/milan_dp/dynmap_mutants.py:122`.
- Evidence: with `prepare()` removed on a fresh clone, `capture_coherence`'s talker leg passes its clean control and catches mutant 37 with neither `ltn_rom.hex` nor `ucode.hex` present.
- This PR's existence check makes the campaign safe regardless. Still, a leg whose checks do not notice that its ROM and microcode are missing either does not read them, or has a gap.
- Suggested outcome: a new issue to find out which.

**R855-1-04 — SUGGESTION — Tests — the input-step plants are one-off**
- Where: `tb/verilator/milan_dp/dynmap_mutants.py:461`.
- Evidence: the input-step plants were run once, outside the tree.
- Suggested outcome: an in-tree self-check (for example, a leg entry naming an input no rule makes, refused by name) would hold `prepare()`'s refusal against later edits.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #929's items 1-3 against: `twin_compare.py:458-473,616,642`; the twin captures and Talker traces (`receipts/twin/*`); `twin_plants.py:231-263` against IEEE 802.1Q-2018 35.2.2.8.7 and Table 35-6 (FailureInformation layout and code 2); `srp_mbx.c:255-305` (unchanged) against the test at `srp_mbx.cpp:281-327`; Table 10-3 grade results in the twin log | R855-1 | 37255683 |
| RTL | CLEAN | `git diff 70f4056f..HEAD -- hdl external gptp-processor protocol-processor third_party` is empty; gitlinks unchanged (`receipts/integrity-review-clone.txt`); twin captures byte-identical to the base's; dynmap legs' RTL builds pass their controls (`receipts/dynmap/head-fresh-dynmap-mutants.log`); mailbox contract and pool macros unchanged (`srp_mbx.h:140-147`) | R855-1 | 37255683 |
| Robustness | CLEAN | `prepare()` failure paths (make rc, absent input) exercised by plants 1 and 2 on fresh clones; `plant_talker_failed_back` refuses when no Talker Advertise is present (`twin_plants.py:262`); startup test bounds (`ASSERT_LT`, per-interface totals) at 1x1 and 8x8, one and two interfaces; the dispatch test's pool sized from the shape (`srp_mbx.cpp:712-729`) | R855-1 | 37255683 |
| Tests | CLEAN | twin-plants: 21 of 21 refused both ways; SRP: 3 new and 3 kept plants plus 4 reviewer probes caught at 8x8, and the 2 new ones escape at 1x1 (`receipts/srp/*`); base failure reproduced; `firmware-unit` shard 0 PASS with the four `srp_mbx` arms; coverage PASS (39 files); dynmap 71 of 71 from a fresh clone | R855-1 | 37255683 |
| Docs | CLEAN (RESIDUE 01, 02 carried) | `tb/verilator/milan_dp/README.md` diff (:107, :911-916, :1385-1406, :1425-1454, :1472-1490); `sw/firmware/ctrl/srp/README.md:313-318`; `docs/design/MAILBOX_SPLIT.md:1642-1654`; Makefile comments; docs_check 0 findings; idiom gates rc 0; comment-rule scan of every added line | R855-1 | 37255683 |

## Real limits

- The release and split images were not rebuilt. Image identity rests on the construction argument above plus the author's published hashes.
- The native Verilator sweep, the full SRP campaign (424 plants), the control and AECP mutant campaigns, `firmware-boundary`, `firmware-verilator`, `split-cdc` and docs' remaining jobs were not run here.
  - The SRP campaign entries that name the changed tests were all run.
  - The author's step-by-step workflow replays are the source-head evidence for the rest.
- `dynmap-mutants` was run with `DYNMAP_MUTANT_JOBS=6` and `make -j8`, within this review's memory cap, not the documented 8. The campaign caps builds at two concurrently regardless.
- Clause readings (IEEE 802.1Q-2018 35.2.2.8.7, Table 35-6, Table 10-3) are this reviewer's. No clause text is held in the repository.
- Hosted evidence at the exact head was read once (`receipts/hosted/check-runs-snapshot.tsv`): 4 success, 1 skipped, 30 queued or in progress. It is not hosted acceptance.
- Physical calibration was not run. No hardware was used.
- Two logs (`receipts/twin/head-twin-then-plants.log`, `receipts/dynmap/head-fresh-dynmap-mutants.log`) had a host home path rewritten to `<pinned-verilator-root>` or `<home>` before hashing. Nothing else in them was changed.

## Pending manager duties

- Hosted and `act` acceptance at the exact head, including `rtl-fast`, `verilator-suites` and `yosys-portability` once the PR is ready.
- The current-dev merge-candidate validation (source base `70f4056f`, live dev `6b66f66d`), with its builder and native banks.
- Carrying RESIDUE 01 and 02 to the residue checklist.
- Opening the issues for the three KNOWN items (the `stream-output-0-notices` owner, the TSpec MaxFrameSize difference, the milan_dp README's pre-#895 SRP section) and, if accepted, SUGGESTION 03.
- The external review (R856) and merge authorization.

R855-1 FINISHED
