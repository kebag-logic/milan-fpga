[R522] POSITIVE - exact head db9aa8c9b135b34ff3d070a979dee70440b37cc6

# R522-2: internal independent review of PR #685 (issue #665, lane FC, round 2)

- **Exact head:** `db9aa8c9b135b34ff3d070a979dee70440b37cc6`, tree `86d60d1102b4018b2d4be85864c80f29c5c88535`. Before and after review, the detached clone was verified at both, with a clean worktree and index and unchanged submodule gitlinks (`receipts/clone-integrity.txt`).
- **Delta:** seven one-line commits on the round-1 head `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`, each with one parent and no trailers: 18 files, 424 lines added, 116 removed. **Whole PR:** 13 commits and 37 files on source base `6714181d0c8a16e2983f85b724f4d688f5111835`.
- **Scope reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md (sections 1, 5, 6 and 6.1) and docs/README.md;
  - the #665 body, the FC assignment (6021509373), the F2 STOP (6026825549), the round-2 assignment (6026839422) and the REVIEW READY post (6027701132);
  - REQUIREMENTS.md section 1; FR_NFR.md NFR-SCOUT-02, NFR-SCOUT-08, H-MAAP and the trace row; MAILBOX_SPLIT.md;
  - IEEE Std 1722-2016, read from a licensed local copy: B.2.1, B.2.2 and Table B.1 (printed pages 154-155), and B.2.5 to B.2.8, B.3.5.6, B.3.6.6 and Table B.10 (pages 155-163);
  - the diff and its history, then the author packet `review-evidence/665fc-r1/author-r2/` at `6a0ea99c` and the PR body.

  Prior public findings (R522-1, R523-1) were read only after this round's draft verdict and ledger were written. One severity changed after that reading; see the severity note under Verdict. The concurrent external round was not read.

## Verdict

**POSITIVE.** All five lenses were applied to the whole PR at the exact head, and each is CLEAN. No BLOCKER, MAJOR or MINOR is open.

- **New this round:** two SUGGESTIONs (S1, S2) and two RESIDUE items (RES1, RES2).
- **Retained from round 1:** two SUGGESTIONs (R522-1 S1 and S2) and one RESIDUE (R523-1-R1).

None of these affects lens coverage.

**Severity note.** The draft verdict, written before the prior findings were read, recorded S1 as MINOR, which left Tests UNCLEAN and made the verdict NEGATIVE. After reading R522-1, S1 was set to SUGGESTION to match R522-1 S1 on this PR, which is the same class: a guard the reviewer's probe proves correct, which the PR's suite does not reach, on runt input only. The change rests on consistency with that precedent; no new fact about the head was learned. If the manager holds the stricter reading, S1 is a MINOR under Tests, and the verdict is NEGATIVE until a suite check is added.

The round-2 rule is correct against the clause. IEEE 1722-2016 B.2.1 (page 154) reads: "All MAAP_PROBE and MAAP_ANNOUNCE frames are sent with a multicast destination MAC address set to the reserved MAAP multicast address defined in Table B.10. All MAAP_DEFEND frames are sent with a destination MAC address set to the source MAC address received in the MAAP_PROBE frame that caused the sending of the MAAP_DEFEND frame."

- Table B.1 assigns MAAP_DEFEND the value 2.
- Figure B.1 puts message_type in the low nibble of the AVTPDU's second byte, which is wire byte 15.
- B.2.5, B.2.6 and B.3.6.6 copy the PROBE's requested range into the DEFEND. The unchanged term "the requested range overlaps this entity's range" is therefore the right identity test for a DEFEND that answers this entity's probe.

## Reviewer evidence

Every run is at the exact head unless the row says otherwise. Scripts are in `scripts/` and raw output in `receipts/`.

| Run | rc | Result | Receipt |
|---|---:|---|---|
| `gen_mailbox.py --check --crosscheck` | 0 | 0 findings | `gen-check.*` |
| The same at the contract commit `49006984` | 0 | 0 findings. The generated files changed in the same commit as the YAML and the generator, and they match the generator. | `gen-check-49006984.*` |
| `gen_mailbox.py --selftest` | 0 | All 16 output arms and 15 contract arms are detected or refused. The two-interface variant is clean; the four-interface variant is refused. | `gen-selftest.*` |
| `make -j4 run-wb run-axil run-cosim run-if2` (pinned Verilator 5.050) | 0 | Wishbone 316/0, AXI4-Lite 361/0, cosim 13/0. Two interfaces: 316/0 and 361/0, and the host model 316/0. | `mbx-suite-head.*`, `verilator-identity.txt` |
| `mutants.py --jobs 10` (the full RTL table) | 0 | Both controls green; 81 of 81 caught, each by its named check | `mbx-mutants-full.*` |
| `scripts/rtl_arms.py` | 0 | The PR's 14 round-2 arms and the re-pointed `rx-subtype-ignored` are caught, with every failing check listed. Of 10 reviewer arms, 8 are caught and 2 escape (S1). | `rtl-arms.log`, `rtl-arms.json`, `rtl-arms.rc` |
| `scripts/model_arms.py` | 0 | The `model` arm control passes (22 tests). The 4 round-2 model twins are caught by their named Q11 checks, and so are 2 reviewer model arms. | `model-arms.*` |
| `scripts/diff/rx_diff.cpp`: round-1 vs round-2 `KL_mbx_rx`, 8 seeds x 25,000 frames | 0 | The traces are identical, ring write for ring write and counter for counter. A DEFEND to the own MAC goes to round 1 with the multicast destination instead, and its two destination words are masked in both traces. Sensitivity controls (the round-1 RTL without that rewrite, and two planted round-2 defects) all differ. | `rx-diff-result.txt`, `rx-diff-coverage.txt`, `rx-diff-build-*.log` |
| The same runs, counting cycles where `rx_ready_o` is low while a byte is offered | n/a | Round 1: 0 cycles in about 141,000 frames of 17 bytes or more. Round 2: about 0.87 per such frame, never more than one (S2). | `rx-ready-bubble.txt` |
| Verilator `--lint-only -Wall` on `KL_mbx_rx`, round 1 and round 2 | 1, 1 | 197 warnings each, all UNUSEDPARAM: no new warning | `lint-rx-head.log`, `lint-rx-r1.log` |
| `scripts/yosys_mbx.sh` (sv2v, generic `synth`, `check -assert`) on `KL_mbx`, `KL_mbx_wb` and `KL_mbx_axil` | 0 | All three pass at the head. On `KL_mbx` the flip-flop count rises by 8 over round 1 (1,555 to 1,563), matching the published +8 FF. | `yosys-mbx-*.log`, `yosys-stat-KL_mbx-*.txt` |
| Hosted contexts at the exact head (read only) | n/a | **Green:** rtl-fast, firmware-unit, docs-check, docs-check-no-git, verilator-lint, yosys-elaboration, Yosys shards 0-3, Verilator shard 3, bdd-conformance, wire-accountability, full-ci-gate, changes. **In progress:** elaborate, Verilator shards 0, 1, 2 and 4. **Skipped:** Physical gPTP. | `hosted-checks-snapshot.txt` |

Three receipts contained the build host's home directory in compiler include paths. It was replaced with `$HOME`, and nothing else was edited.

## Findings

No BLOCKER, MAJOR or MINOR.

### R522-2-S1: SUGGESTION. No suite check covers the live-subtype branch for a frame that ends at byte 14

- **Lenses:** Tests. Robustness is not attributed, because the RTL behaviour itself was verified correct (below).
- **Location:** `hdl/milan/mailbox/KL_mbx_rx.sv:163`:

  ```systemverilog
  subtype = (cnt_r == 11'(MBX_SUBTYPE_BYTE_C)) ? rx_data_i : sub_r;
  ```

  A frame that ends at byte 14 is classified on the live byte; every longer frame uses the held `sub_r`.
- **Evidence:**
  - The reviewer arm `rev-short-frame-stale-subtype` (`subtype = sub_r;`) escapes the suite through both adapters: Wishbone 316/0 and AXI4-Lite 361/0 (`receipts/rtl-arms.log`).
  - The only suite frame that ends at byte 14 is Q11's DEFEND cut (`tb/verilator/mbx/suite.hpp:1211`). Its outcome does not depend on the subtype, and the frame before it has the same subtype.
  - The reviewer differential detects the same plant (24,765 differing trace lines), and the head matches round 1 exactly.
- **Impact:** none at this head.
  - A regression would change only FILTER_MISMATCH for a frame that ends at byte 14, which is a runt.
  - It cannot change delivery. Every tuple that names a subtype has an identity term that needs bytes past 15, and the SRP tuples read no subtype.
  - The severity is set to match R522-1 S1, which is the same class: a guard the reviewer's probe proves correct that the PR's regression suite does not reach.
- **Suggested outcome (optional):** a suite check that ends a frame at byte 14 with a different subtype from the preceding frame, where that subtype decides the count. For example:
  - after an ADP frame, a 15-byte frame to the ADP address with subtype `0xFD` counts once;
  - after a MAAP frame, a 15-byte frame to the ADP address with subtype `0xFA` counts nothing.
- **Verification:** `rev-short-frame-stale-subtype` (in `scripts/rtl_arms.py`) reddens that check on both adapters.

### R522-2-S2: SUGGESTION. The later decision adds a one-cycle ingress stall at byte 16

- **Lenses:** RTL, Docs.
- **Location:** `hdl/milan/mailbox/KL_mbx_rx.sv`:
  - `:134`, where `rx_ready_o` needs `q_cnt_r < 4`;
  - `:157`, where `cls_at_w` fires at byte 15;
  - `:230`, where a drain needs `cls_done_r`.
- **Evidence:**
  - Byte 15 is taken with three words queued and pushes the fourth. `rx_ready_o` is then low for one cycle before byte 16 while word 0 drains.
  - In round 1, draining started the cycle after byte 14, so this cycle did not exist.
  - Measured (`receipts/rx-ready-bubble.txt`): round 1 had 0 ready-low cycles in about 141,000 frames; round 2 has about 0.87 per frame of 17 bytes or more, never more than one.
  - `KL_mbx_rx.sv:41-42` and `MAILBOX_SPLIT.md:170` say "the decision at byte 15 never waits for a drain", which is true. The PR body's shorter "so nothing waits" is not (RES1).
- **Impact:** none functionally.
  - The ingress is a valid/ready stream, and every frame end already stalls it for the FIN drain and the two header writes.
  - The SoC holds the ingress idle (`sw/litex/milan_soc.py:2549`).
  - The datapath-tap lane will need to absorb one more cycle per frame.
- **Suggested outcome (optional):** either state the per-frame cycle in `MAILBOX_SPLIT.md`'s filter section for the tap lane, or deepen the queue to five words if a stall-free ingress is wanted.
- **Verification:** the doc line exists. With a deeper queue, the stall count in `rx-ready-bubble.txt` drops to 0 for round-2 frames.

### R522-2-RES1: RESIDUE. The PR body says "nothing waits"

- **Lens:** Docs.
- **Artifact:** PR #685 body, Description table, row "Round 2: the MAAP DEFEND": "the four-word queue holds bytes 0 to 15, so nothing waits."
- **Evidence:** `receipts/rx-ready-bubble.txt` (S2). The statement is prose in the PR body. No code, test, measurement, figure, generated artifact or clause claim depends on it.
- **Exact fix:** replace it with "the four-word queue holds bytes 0 to 15, so the decision needs no drain first; byte 16 then waits one cycle while word 0 drains."
- **Verification:** the PR body carries the new sentence.

### R522-2-RES2: RESIDUE. The PR body status says the branch is unpushed

- **Lens:** Docs.
- **Artifact:** PR #685 body, Status: "No hosted or `act_ci.py` run: the branch has not been pushed."
- **Evidence:** `db9aa8c9` is the published PR head, and hosted contexts have run on it (`receipts/hosted-checks-snapshot.txt`). The sentence is prose only.
- **Exact fix:** replace it with "Pushed as the PR head; the hosted contexts and the local replica are recorded by the manager."
- **Verification:** the PR body carries the new sentence.

## Prior public findings at this head

| Finding | Severity | Status at `db9aa8c9` | Evidence |
|---|---|---|---|
| R522-1 S1: no suite check reaches three filter guards (saturation, the `mis_r` clear, `own_if_w`; now `KL_mbx_rx.sv:412`, `:375` and `:172`) | SUGGESTION | **Retained.** Round 2 adds no check for any of them. Q9 is unchanged. Q11 does not saturate the counter, send a frame shorter than 15 bytes after a mismatch, or use an all-zero destination. Round 2 does not touch the three guarded lines. They were not re-planted this round. | `suite.hpp:1131-1151`, `:1180-1219`; the round-2 diff of `KL_mbx_rx.sv` |
| R522-1 S2: the generator self-test plants two of the three TPIDs | SUGGESTION | **Retained.** It still plants only `0x8100` and `0x88A8`. | `receipts/gen-selftest.log` lines 25-26 |
| R523-1-R1: nine U+2014 characters in the PR body (Contents and Status) | RESIDUE | **Retained.** The current PR body still has nine. No line the branch adds has one (diff `6714181d..db9aa8c9` scanned). | the PR body at review time |

## Clean lens results

[R522] PASS Conformance - `sw/mailbox/mailbox.yaml:521-524`; `hdl/milan/mailbox/KL_mbx_pkg.sv:632-644,751`; `hdl/milan/mailbox/KL_mbx_rx.sv:157-182`; `sw/firmware/ctrl/host/mbx_model.c:303-331`; `tb/verilator/mbx/suite.hpp:958,1180-1219`; REQUIREMENTS.md:62,73,91-94 - The maap row matches B.2.1, Table B.1, Figure B.1 (byte 15, low nibble), B.2.5, B.2.6 and B.3.6.6, and item 1 of the round-2 assignment. A frame matches the row in one of two ways, and the unchanged range term (mask 0xE, offset 26) then applies:
- destination 91:E0:F0:00:FF:00, with any message type;
- destination equal to the arrival interface's OWN_MAC, EtherType 0x22F0, subtype 0xFE and message_type 2 (mask 0x4).

Checked on the RTL and the model:
- **Refused and counted once:** a PROBE, an ANNOUNCE and each of the 13 reserved types sent to the own MAC, and a DEFEND sent to a foreign unicast. Q11 checks this, and the differential matches round 1, which counted each once.
- **DEFEND to the own MAC:** treated exactly as round 1 treated the same frame sent multicast. Over 8 seeds there were 2,064 such frames; 206 were delivered, and the rest were refused the same way.
- **Multicast DEFEND:** still passes (Q11).
- **Unchanged rules:** tagged frames, foreign unicast, FILTER_MISMATCH and the token buckets (identical differential traces).

Round 1's conformance of the other rows (R522-1) still holds: their tuples carry mask 0xFFFF and classify exactly as before.

[R522] PASS RTL - `hdl/milan/mailbox/KL_mbx_rx.sv:104,134,152-182,230,289,325-332,353-361`; `KL_mbx_pkg.sv:632-644,751`; `receipts/lint-rx-*.log`, `yosys-mbx-head.log`, `yosys-stat-KL_mbx-*.txt`, `rx-diff-result.txt` - The checks:
- **Decision point:** taken once per frame, at byte 15 or at a last byte at index 14. Frames that end earlier keep round 1's `cnt_r < 14` path.
- **Queue:** byte 15 is accepted with three words queued (`q_cnt_r < 4`), so the decision never needs a drain first.
- **No hang:** the head completes every suite frame and every one of 200,000 random frames of 1 to 1,517 bytes with random idle gaps.
- **Subtype register:** `sub_r` is reset, and it is written at byte 14 before it is read at byte 15.
- **Widths:** the `{1'b0, msg}` index is 5 bits into a 32-bit constant, the same idiom as the term mask. The mask table is generated per tuple, and unused tuples carry mask 0.
- **Tools:** no new Verilator warning. Yosys synth with `check -assert` passes on all three tops, and the +8 flip-flops are `sub_r`.
- **Untouched by round 2:** `KL_mbx.sv`, its ports and every register, `KL_mbx_wb.sv`, `KL_mbx_axil.sv` and `milan_soc.py`. In `mbx_contract.h` only tuple constants change, and only the host model reads them.

The one-cycle stall is S2 (SUGGESTION). Round 1's RTL review (R522-1) covers the unchanged rest.

[R522] PASS Robustness - `receipts/rx-diff-result.txt`, `rx-diff-coverage.txt`, `rtl-arms.log`, `model-arms.log`; `suite.hpp:1206-1216` - The truncated-input boundary was checked, and round 2 is identical to round 1 throughout.
- **Differential stream:** about 37 % of frames are 1 to 20 bytes or exactly 14 to 17. The rest are mixed lengths of 60 to 71, 62 to 67, 126 to 131 and up to 1,517 bytes. Frames arrive on interface index 0 and on an index with no interface. Channels are randomly closed, MAAP_COUNT is randomly 0, and the ring is sometimes left unconsumed so RX_DROP moves.
- **Cut DEFENDs (Q11):** cut at byte 14, it counts once; cut at byte 15, it counts nothing; the next DEFEND passes.
- **Repeated and reserved types to the own MAC:** each counts once.
- **Tokens:** refusals take none. Q10 is unchanged, and the full table catches `rx-refusal-takes-a-token`.
- **Two-interface variant:** passes on both adapters and the model, including Q8's DEFEND per interface index.

[R522] PASS Tests - `tb/verilator/mbx/suite.hpp:958,1001-1002,1083-1118,1174-1219`; `tb/verilator/mbx/mutants.py:69-72,244-286`; `sw/firmware/ctrl/test/ctrl_mutants.py:395-415`; `sw/mailbox/gen_mailbox.py:238-244,270-274` - The reviewer reran the suite (316/361/13; on two interfaces 316/361/316) and the full RTL table (81 of 81). Each round-2 arm was also planted separately, with every failing check listed, and each fails for its own defect through both adapters:
- **Fail the Q11 delivery, refusal or count checks:** the dropped tuple; the message type read off by one, read before the decision, or taken from the register; the ignored mask; the uncounted own-MAC refusal; and the any-unicast defect.
- **Fails the byte-14 count check:** the short frame that is never classified.
- **Model twins:** all four fail their named Q11 checks. `model-tuple-msg-type-ignored` compiles as re-planted at `db9aa8c9` and is caught.
- **Re-pointed arm:** `rx-subtype-ignored` now points at the held subtype and is still caught by C0.
- **Reviewer plants caught:** the mask widened to every type, the mask set to PROBE, the decision taken twice, the message type from the register, and two model arms.
- **One escape:** the stale subtype on a frame that ends at byte 14. This is S1 (SUGGESTION), the same class as R522-1 S1.

No existing check was removed or weakened. Q2's multicast-row branch is narrowed so that the multicast row keeps `kAdpAcmpMac`, and the DEFEND row uses `kForeignMac`. The generator gains 2 output arms and 3 contract arms, and each detects or refuses its plant.

[R522] PASS Docs - REQUIREMENTS.md:58-99; `docs/reference/FR_NFR.md:328,409,427,599`; `docs/design/MAILBOX_SPLIT.md:76-90,163-206,498-501,581-597`; `docs/reference/MAILBOX_CONTRACT.md` (generated, `--check` clean); `tb/verilator/mbx/README.md:61-69,186-198`; `sw/firmware/ctrl/README.md:98-104`; `sw/firmware/gtest/README.md:160-164`; file banners `KL_mbx_rx.sv:9-42` and `mbx_model.c:6-14`; the PR body; the author packet `author-r2/` - The checks:
- **The row:** each document states the amended row as the code implements it: the multicast address, or own unicast on the receiving interface for MAAP_DEFEND (message_type 2) only, then the range term, citing B.2.1.
- **Requirements:** NFR-SCOUT-08 and H-MAAP carry the rule and its three behaviours. The status lines (REQUIREMENTS.md:98, FR_NFR.md:427 and :599) say PR #685 implements the filter.
- **Counts:** the suite counts (316 and 361) and the arm counts (16 and 15; 7 x 2 plus 4; 22 model tests) match the reviewer's runs.
- **Area:** the table matches the published packet, and its +8 FF matches the reviewer's synthesis.
- **NFR-SCOUT-02:** left unedited. Its four-field tuple wording defers to NFR-SCOUT-08, and a tuple that also reads message_type does not contradict it.
- **Wording rules:** no line the branch adds carries U+2014.

The prose-only defects are RES1 and RES2, and R523-1-R1 is retained.

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 1722-2016 B.2.1, B.2.2, Table B.1, Figure B.1, B.2.5-B.2.8, B.3.5.6, B.3.6.6 and Table B.10; `mailbox.yaml`; `KL_mbx_pkg.sv`; `KL_mbx_rx.sv`; `mbx_model.c`; REQUIREMENTS.md section 1; FR_NFR.md; suite Q0-Q11; the reviewer differential | R522-2 | `db9aa8c9b135b34ff3d070a979dee70440b37cc6` |
| RTL | CLEAN (S2 SUGGESTION open) | `KL_mbx_rx.sv`; `KL_mbx_pkg.sv`; the round-2 diff of `KL_mbx.sv`, the adapters and `milan_soc.py` (empty); Verilator lint; Yosys synth of three tops; the stall measurement; R522-1 for the round-1 files round 2 left untouched | R522-2 | `db9aa8c9b135b34ff3d070a979dee70440b37cc6` |
| Robustness | CLEAN | The differential (200,000 frames: boundary lengths, closed channels, empty range, an index with no interface, ring pressure); Q8, Q9, Q10 and Q11; the two-interface runs | R522-2 | `db9aa8c9b135b34ff3d070a979dee70440b37cc6` |
| Tests | CLEAN (S1, R522-1 S1 and R522-1 S2 SUGGESTIONs open) | `suite.hpp`; `mutants.py` (81 of 81, plus 15 round-2 arms planted separately); `ctrl_mutants.py` (4 twins and 2 reviewer arms); the generator self-test; the `model` arm (22 tests). Round 2 does not touch the firmware production code, so its R522-1 gtest, coverage and ratchet evidence stands. | R522-2 | `db9aa8c9b135b34ff3d070a979dee70440b37cc6` |
| Docs | CLEAN (RES1, RES2 and R523-1-R1 RESIDUE carried) | REQUIREMENTS.md; FR_NFR.md; MAILBOX_SPLIT.md; MAILBOX_CONTRACT.md; the mbx, ctrl and gtest READMEs; file banners; the PR body; the author-r2 packet; REVIEW READY 6027701132 | R522-2 | `db9aa8c9b135b34ff3d070a979dee70440b37cc6` |

Round 2 touches an artifact in every lens's scope, so every lens was re-applied to the whole PR at this head. R522-1 (`021b9c1f`) is cited only for what round 2 left byte-identical: `KL_mbx.sv`, the adapters, the firmware production sources and their unit tests, and the default-build export.

## Real limits

- **Area:** not re-measured, because no Vivado run was made. The published figures were checked for plausibility only: the +8 FF matches the reviewer's generic synthesis, but the +15 LUT was not checked. The author's OOC reports are published as hashes only.
- **Gates not rerun this round:** the full firmware gate with `--self-test` (97 arms, which needs the processor submodule and the lwSRP pin), coverage, the ctrl_nvm gate, the builder bank, lint_rtl, xvlog and the docs gates. Round 2 changes no firmware production source, and the reviewer ran the `model` arm and the round-2 model arms. The manager's banks and the hosted firmware-unit and docs-check contexts cover the rest.
- **Default-build export:** not repeated. Round 2 changes no file the default build reads: `milan_soc.py` and the source list are untouched, and the mailbox sources are read only under `--ctrl-mailbox`.
- **Hosted and physical:** at the snapshot, hosted Verilator shards 0, 1, 2 and 4 and `elaborate` were still in progress, and Physical gPTP was skipped. Physical calibration was NOT RUN, and no hardware claim is made.
- **Differential scope:** it drives `KL_mbx_rx` alone with one interface. The two-interface build was exercised through the suite (both adapters and the model), not the differential.

## Pending manager duties

- **Owner approval:** the owner must approve the amended MAAP row (REQUIREMENTS.md section 1, NFR-SCOUT-08, H-MAAP) before merge (#665 comment 6026839422, item 4). Once the approval exists, consider citing it beside the "owner filter decision" link at REQUIREMENTS.md:59-60, which today names only the original decision.
- **Residue:** carry RES1, RES2 and R523-1-R1 to the residue checklist.
- **Hosted and local replica:** acceptance at the exact head, including the four Verilator shards and `elaborate` that were still in progress.
- **Merge candidate:** build the final current-dev candidate (source base `6714181d`, live dev `79b086d4`), then post-merge containment.
- **Second review:** the completion bar also needs the external round: two independent positive reviews and the full ledger.

R522-2 FINISHED
