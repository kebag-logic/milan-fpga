[R834] POSITIVE - exact head 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b

# R834-1: external review of PR #898 (issue #897), Mark II split GET_AS_PATH

- **Head:** `5e6fef3ee74dcf6766ac3923349ae83524bc0e7b`, tree `3f0b90490650e0bc4b51f2f55ecb10c20dab5a06`. The clone was verified at the start and the end (`receipts/clone-verify.txt`).
- **Delta:** `7f50ee6a..5e6fef3e`, four commits, 16 files, +346/-54. The base `7f50ee6a` is #810's round 29 tip. The PR is stacked on `665-s2b-cycles`.
- **Authority:**
  - issue #897 acceptance 1-4 as amended;
  - the ruling issuecomment-6828659285, option (a): a datapath window that does not answer within its bound keeps ENTITY_MISBEHAVING, and acceptance 5 is a bench item, out of scope;
  - IEEE 1722.1-2021 7.4.41 (as cited by the issue, the STOP comment and the processor's 6.10 table);
  - Milan v1.2 5.4.2.24 and Table 5.22;
  - `mbx_contract.h` GSI window;
  - `hdl/milan/milan_datapath.sv` kind 2 answer;
  - protocol-processor `docs/architecture/06_aecp_engine.md` 6.10, the reference word table.
- **Lenses applied:** Conformance, RTL, Robustness, Tests, Docs. All five are clean at this head.
- **Prior public review findings on this PR:** none existed when this round started or when its verdict was written. The PR has 0 reviews and 0 review comments. The issue and PR threads hold only the TAKEN, STOP, ruling and review-start notices. There is nothing to resolve or retain.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE. Three optional suggestions:

**[R834] SUGGESTION RTL, Tests: `sw/firmware/ctrl/aecp/aecp_face.c:254-268` against `hdl/milan/milan_datapath.sv:6297-6343,6570-6581`. No executable check of the firmware's kind 2 read on the split RTL.**
- **Evidence:**
  - The face tests (`test_aecp.cpp:2823` model) and B11 (`test_plat_boot.cpp:108` model) encode the processor's word table in a host model.
  - The RTL answer block they rely on runs only through the all-fabric engine (`tb/verilator/milan_dp/sim_gptp.cpp:1091-1103`, `sim_ax1x1gptp.cpp:985-991`).
  - I checked by reading the RTL that the split path (`g_sp_ctrl`, `milan_datapath.sv:10062-10071`; `KL_mbx.sv:636-652,714`) feeds the same block, with selector 0 `{60'0,count}`, selector 8 the entry at its ordinal, and one snapshot per count request.
- **Impact:** none found. A future change to the split wiring would be caught only on the bench (acceptance 5).
- **Optional outcome:** a split-RTL or split-boot leg issuing one GET_AS_PATH, in a later lane.
- **Verification:** that leg fails with the face's ordinal or selector planted wrong.

**[R834] SUGGESTION Robustness: `hdl/milan/milan_datapath.sv:6316-6321` (reset clears `asp_resp_*`), read with `aecp_face.c:258-264`. A datapath reset between the count read and the entry reads.**
- **Evidence, from reading the RTL only (not executed):**
  - A reset that lands after the count read clears the snapshot. The later entry reads then answer 0, because the ordinal is at or above count 0.
  - The response would be SUCCESS with the old count and zero ClockIdentities.
  - GET_AVB_INFO's snapshot has the same property at the base. A datapath reset leaves every observation's notice pending (`aecp.h:65-67`), so the next unsolicited GET_AS_PATH carries the served path.
- **Impact:** a transient wrong path, which the reset's notice corrects. It is not ENTITY_MISBEHAVING, so acceptance 3 is unaffected.
- **Optional outcome:** a follow-up issue could decide whether the face re-reads the count after the entries.
- **Verification:** a face test with the model changing its count between the two reads.

**[R834] SUGGESTION Docs: `docs/design/SPLIT_CONTROL_MEMORY.md:293`. The every-port arm's 123,756 B has no published build receipt.**
- **Evidence:** the packet publishes the N8 cost sample (`harness/sample-N8.md`) but not that build's size line. The figure is also stated in the packet's handoff. It is consistent with the rest: 123,420 B + 336 B, where 336 B is the face's +328 B (`receipts/rom-face-object-sizes.txt`) plus the arm's added port assignment. Its margin is 1,172 B, and no gate reads it.
- **Optional outcome:** add the arm build's size line to the packet.

**Outside the delta, for the manager's tracking (not a finding against this PR).**
- **What:** `sw/firmware/ctrl/plat/README.md:113` and `:139` still say the platform's 8x8/2if image "plans 58.5 RAMB36, within the 59.0 ledgered".
- **Why it is stale:** the author's base and head plans both give 59.5 tiles, refused by the tree's 59.0 entry (`receipts/rom/images-base-7f50ee6a.md`, `images-head-6de1475f.md`). `SPLIT_CONTROL_MEMORY.md:282` at this head says 59.5.
- **Why it is not this PR's:** the line was already stale at the base, and the delta does not change the tile count.

## Per-lens results

**[R834] PASS Conformance: `sw/firmware/ctrl/aecp/aecp_face.c:248-268`, `sw/firmware/ctrl/aecp/aecp_commands.c:453-483`, `sw/firmware/ctrl/app/ctrl_app_aecp.c:176-177`, `hdl/milan/milan_datapath.sv:6668-6669`, protocol-processor `06_aecp_engine.md:1001-1008`.** Checked against #897 acceptance 1-4 as amended, the ruling, IEEE 1722.1-2021 7.4.41.2 and Milan Table 5.22:
- **(1) The read.**
  - Kind 2 count at selector 0, then each entry at selector 8, ordinal k = 0..n-1.
  - Type AVB_INTERFACE, the descriptor index, through the interface's own window (the core passes `index, index`).
  - Bounded by the caller's capacity, `AECP_PATH_ITEMS` = 64. The `_Static_assert` at `:253` guarantees that every carried ordinal fits `MBX_GSI_SEL_ORD_WIDTH` = 8.
  - A count past the bound fails at the count and reads no entry. A word with no answer fails there.
  - This is exactly the processor's 6.10 table and the datapath's answer block.
  - Byte order: the 64-bit word goes out big-endian by `aecp_put64`, as GET_AVB_INFO's gm_id and the all-fabric gather do. The reviewer's byte-swap plant is killed.
- **(2) The payload.** descriptor_index @0 and count @2 (16 bit), path_sequence @4 at 8 B each; cdl 16 + 8n.
  - The unsolicited AS_PATH_CHANGED response (event bit 2, `4u`) is built through the same `path` port, so it carries the datapath's sequence (`AppFace.AnAsPathChangeNotifiesTheDatapathsSequence`).
- **(3) No ENTITY_MISBEHAVING with an answering datapath.** That status leaves `avb(path=true)` only:
  - at `index >= cfg.interfaces`, which the ruling puts out of scope and no shipped image reaches;
  - on `!ok || count > AECP_PATH_ITEMS`.
  - The face's `!ok` needs an unanswered word or a count above 64. The datapath's count is 4 bits wide (at most 15), so an answering datapath cannot reach either.
- **(4) Acceptance 1's reference.** The split serves from the same `asp_resp_*` snapshot and `gsi_answer` block that the all-fabric gather reads.

**[R834] PASS RTL: `git diff 7f50ee6a..HEAD -- hdl/` is empty; `hdl/milan/milan_datapath.sv:2459-2477,6297-6343,6570-6581,6665-6671,10062-10071`; `hdl/milan/mailbox/KL_mbx.sv:636-652,714`; `mbx_contract.h:704-717,833` (`receipts/rtl-and-core-excerpts.txt`).**
- No RTL, CDC or contract change.
- The snapshot is captured on the count request's rising edge (`gsi_req_q_r`). The window raises and drops `gsi_req_o` per request (busy is cleared on answer or on its own `MBX_WIN_GSI_WAIT_CYCLES` timeout), so each GET_AS_PATH gets one snapshot and a PUBLISH cannot splice into it.
- Widths are safe:
  - the count is `{60'0, 4-bit}`, and the face compares the whole 64-bit word against `size_t` capacity;
  - the `(unsigned)n` cast happens only after `n <= 64`;
  - `*count` is written only on success.

**[R834] PASS Robustness: `aecp_face.c:254-268`, `sw/firmware/ctrl/mbx/mbx.c:380-405`, `receipts/probes/` (`au-a`, `au-b`, `rv-a`, `rv-b`, `rv-c`).**
- **Failure paths:**
  - count unanswered: one counted timeout, no entry read;
  - entry k unanswered: fails at k, nothing after it is read;
  - count 0: SUCCESS with an empty sequence, as the processor answers;
  - count at the bound (64) carried whole; 65 and 2^32 refused at the count;
  - a capacity smaller than 64 is honoured (the reviewer's plant ignoring it is killed).
- **Bounds:** at most 1 + n ≤ 65 window reads, each bounded by `mbx_win_read`. Per the ruling, a failed port answers ENTITY_MISBEHAVING (unchanged `Core.ObservationRefusals`).
- **Feature-disabled:** an option-off or no-GM datapath serves count 0 (`milan_datapath.sv:2469-2477`), which answers SUCCESS with an empty sequence.
- **Harness:** no harness group stages GET_AS_PATH or an AS_PATH event. The test SoC ties `i_asp_chg_p_i=0` (`tb/verilator/ctrl_service_budget/split_soc.py:263`). The arms' port replacement is otherwise unchanged: every variant applies uniquely at head, checked by `build.variant_fixture` for all four variants.
- **Reset:** see the second suggestion.

**[R834] PASS Tests: `sw/firmware/ctrl/test/test_aecp.cpp:3088,3118,3153,3665`, `test_plat_boot.cpp:415`, `aecp_mutants.py:664-695`, `plat_mutants.py:194-197`, `gtest/coverage.ratchet:10,26`; receipts `probes/SUMMARY.md` and `fw_coverage-check-head.log`.**
- **Baseline:** app mode at 1 and 2 interfaces PASS (129 tests each); plat, platboot1 and platboot2 PASS. The five new tests ran OK.
- **Author plants:** all nine AECP plants and the one platform plant (at both platboot1 and platboot2) are killed by name, on their own words, with the repository's readers.
- **Reviewer plants:** nine further independent plants are killed (count not reported, caller capacity ignored, ordinal +1, last entry skipped, byte order swapped, entry index 0, count type 0, entries through window 0, AS_PATH event dropped). One more platform plant (count reported as 1) is killed at both shapes. Two probe forms that the compiler itself refuses under `-Werror` are recorded as refusals, not escapes.
- **Coverage:** `fw_coverage.py --check` passes (rc 0, 39 files). `aecp_face.c` is at 179/179 lines and 160/160 branches, equal to the ratchet, and `ctrl_plat.c` passes its ratchet.
- **Plant totals:** `aecp_mutants.DEFECTS` is 236 (227 + 9). `plat_mutants` is 42 (41 + 1), so the README's 42 is right.
- **Tests do more than mirror the implementation:** the request words are checked against literal contract positions (kind LSB 0, selector LSB 4, ordinal LSB 8), which match `mbx_contract.h:704-717`.
- **Real wiring:** see the first suggestion.

**[R834] PASS Docs: `sw/firmware/ctrl/plat/README.md:81-84,122,126` (the "Not yet done" item removed), `sw/firmware/ctrl/aecp/README.md:335`, `aecp_face.h:26-35,47,59`, `docs/design/MAILBOX_SPLIT.md:1304,1400-1406,1640`, `docs/design/SPLIT_CONTROL_MEMORY.md:282,293`, `tb/verilator/ctrl_service_budget/README.md:210`, PR #898 body.**
- Every stale statement that GET_AS_PATH is unavailable or comes from the platform is gone. A repository grep finds only the plant's own comment.
- **ROM figures** (from the author's `rom/images-*.md`):
  - per-point deltas of +328 B for the fixture and +312 B for the platform;
  - margins of 1,488 B and 1,600 B, both correct by arithmetic;
  - the face object's own `.text` grows 3,384 to 3,712 B (+328) in the reviewer's independent RV32IM compile (`receipts/rom-face-object-sizes.txt`).
- **Caps:** the 60.5 platform cap and the 58.5 fixture cap match the owner decision (#665 issuecomment-6824896581).
- **Comment rule:** the added source lines carry no lane label, lane name, review round, reviewer ID or comment ID. B11 is the test file's own case numbering, B1-B10 already existing.
- `docs_check.py` reports 0 findings (`receipts/docs_check-head.log`).

## Checks requested by the manager

1. **Face read against the datapath:** matches on byte order, ordinal, the bound, a count past the bound, and a word with no answer (Conformance, RTL, Robustness above).
2. **Payload and AS_PATH_CHANGED:** the payload matches 7.4.41.2 field by field, and the AS_PATH_CHANGED notice carries the datapath's sequence.
3. **ENTITY_MISBEHAVING:** no valid AVB_INTERFACE read with an answering datapath can return it.
4. **Plants and coverage:** all nine AECP plants and the one platform plant are killed, and `aecp_face.c` is at 100 % of lines and branches. Re-run by this round.
5. **ROM:** 312-328 B per image with no extra tile, the fixture at 58.0 and the platform at 59.5 under its 60.5 cap.
   - These figures are the author's receipts. They are consistent with this round's object-level measurement, but the linked images were not rebuilt here.
   - The tree's own 59.0 entry refuses the platform's 8x8/2if image at the base and at the head alike.
   - **Load:** 1x1/1if at 0.486. `load_grade.py --check` re-run at head: PASS, 0.486 and 0.483 against 0.70 (`receipts/load_grade-check-head.log`). These are stated tables, not re-measured.
6. **The three red gates are the base's:**
   - **C/C++ idiom ratchet:** re-run at head, FAIL with 1 > 0 at `test_aecp.cpp:1428`, a line last touched by `bdb0ae52`, an ancestor of the base. Per-file counts are identical at base and head for every changed C/C++ file.
   - **Hooks self-test:** its plant anchor occurs 0 times in `acmp_mbx.c` at both base and head, and the delta does not touch that file or `ctrl_service_hooks`.
   - **Firmware boundary:** the refused `flip_grade.py` has the same blob `bfe4691c` at base and head, the delta adds no file, and `ctrl_configs.py` is unchanged.
   - Evidence: `receipts/red-gates-attribution.txt` and `cpp_idiom-head.log`.

## Ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_face.c:248-268`, `aecp_commands.c:453-483`, `ctrl_app_aecp.c:176-177`, `milan_datapath.sv:6668-6669`, PP `06_aecp_engine.md:1001-1008`, #897 acceptance 1-4 and ruling 6828659285 | R834-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| RTL | CLEAN | empty `hdl/` diff, `milan_datapath.sv:2459-2477,6297-6343,6570-6581,6665-6671,10062-10071`, `KL_mbx.sv:636-652,714`, `mbx_contract.h:704-717,833` | R834-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| Robustness | CLEAN | `aecp_face.c:254-268`, `mbx.c:380-405`, `split_soc.py:263`, `build.py:118-262` (variants applied), probes `au-b`, `rv-a`, `rv-c` | R834-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| Tests | CLEAN | `test_aecp.cpp:2823,3088,3118,3153,3665`, `test_plat_boot.cpp:108,415`, `aecp_mutants.py:664-695`, `plat_mutants.py:194-197`, `coverage.ratchet:10,26`, `receipts/probes/*`, `fw_coverage-check-head.log` | R834-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| Docs | CLEAN | `plat/README.md:81-84,122,126`, `aecp/README.md:335`, `aecp_face.h:26-35`, `MAILBOX_SPLIT.md:1304,1400-1406,1640`, `SPLIT_CONTROL_MEMORY.md:282,293`, harness `README.md:210`, PR #898 body, `docs_check-head.log` | R834-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |

## What this round did not do

**Not run by this round.** For these I rely on the author's published gate receipts (`review-evidence/897-r1`, archive `299a7500`) and on attribution by unchanged artifacts:
- the full firmware self-test in its four shards;
- the complete AECP campaign (236) and control campaign (697);
- `test_builder.py`, `behave`, the split boot simulations, the twin;
- the CPU-budget harness builds and samples, and the ROM plan (`ctrl_memory`) on #810's runtime archives;
- the hooks self-test and the firmware boundary gate.

No manager source bank ran at this head, and none is claimed.

**Hosted evidence.** A read-only snapshot at 16:18Z is in `receipts/hosted-checks-snapshot.tsv`.
- Executed and green: `firmware-aecp-mutants`, `firmware-srp-mutants`, `docs-gates-1` and `-2`, `docs-check-no-git`, `bdd-conformance`, `verilator-lint`, `elaborate-gates-0`, `wire-accountability`, `full-ci-gate`.
- Still running or queued: the Verilator shards, `firmware-unit`, `firmware-control-mutants`, `firmware-boundary`, `docs-gates-0`, `yosys-elaboration` and others.
- `Physical gPTP` was skipped.
- The manager owns hosted and act acceptance.

**Other limits.**
- **Standards text:** I did not have the IEEE 1722.1-2021 or Milan v1.2 text. I checked the clauses as the issue, the STOP comment, the ruling and the processor's 6.10 table cite them.
- **Harness datapath:** the harness's test SoC holds the datapath idle, so no harness measures the CPU cost of answered window reads at any head. This is a base property. The PR discloses that the change's read is not staged.
- **Hardware:** no hardware was used. Physical calibration was NOT RUN, and acceptance 5 (the bench) is not evidenced here. Skipped field checks are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate after #810 merges (source base `7f50ee6a`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`). Show the three base red gates green at the composed head, as the ruling requires.
- Accept the hosted exact-head contexts still running at the snapshot, and the act replica.
- Carry acceptance 5 to the bench lane.
- Track the pre-existing `plat/README.md:113,139` tile statement outside this delta.
- Optionally open issues for the three suggestions.
- Merge only with explicit maintainer authorization.

R834-1 FINISHED
