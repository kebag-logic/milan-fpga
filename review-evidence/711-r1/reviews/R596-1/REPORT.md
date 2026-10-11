[R596] POSITIVE - exact head 49b437f445e34b558106c8799c1ffc0a5dc844cf

# R596-1: internal cleared-context review of kebag-logic/milan-fpga PR #718 (issue #711)

- Head under review: `49b437f445e34b558106c8799c1ffc0a5dc844cf`, tree `3bb600ec7a1e16887bed81cdf7f36e1d55f6a793`, two commits on dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Role: internal cleared-context reviewer `[R596]`. Executor `[A589]`, external reviewer `[R597]` (per the assignment comment on #711).
- Scope: lwSRP gitlink `9197193e` to `08ee86e8` (lwSRP PR #18, grouped same-type VectorAttributes), `ctrl_arms.py` pin check, `srp_latency.cpp` MVRP LeaveAll walk, regenerated submodule diagram, ledger row and pin prose.
- Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #711 (body, assignment, TAKEN and REVIEW READY comments), lwSRP issue #17 and the lwSRP `9197193e..08ee86e8` source diff, the base..head diff, and the author's published evidence at `643de7f0` (`review-evidence/711-r1`). Prior public findings on the PR were read only after this verdict and ledger were written (section 7).

## 1. Verdict

POSITIVE. Acceptance 1 to 5 are met at this head, with two premise notes under acceptance 3 and 5 that the author already published (section 3). There is no BLOCKER, MAJOR or MINOR finding. I record two SUGGESTIONs and three observations. All five lenses are covered clean at this exact head (section 5).

Every claim the focus asked me to check reproduced independently:
- The old walk with the new assertion fails at `08ee86e8` at IF=1 and IF=2. The new walk passes at both pins, IF=1 and IF=2.
- My own decoder, which shares no code with the lane's decoder, gives the author's figures exactly: 4,186 MRPDUs, 2,201 byte-identical, 1,985 layout-only, 0 decoded differently, and every head MRPDU grouped. My planted-change controls fail as they should.
- The firmware unit job at the head gives 59 arms ok, 1,191 cases, coverage 30 files at 100 % equal to the ratchet, and 784 of 784 planted defects caught.

## 2. Findings

### S1 SUGGESTION, lenses Docs and Conformance: `sw/firmware/ctrl/srp/README.md:344`, the clause citation can read as a mandate

- Evidence: line 344 reads "Its PR #18 sends one Message per AttributeType in each MRPDU (IEEE 802.1Q-2018 10.8.1.2)." 10.8.1.2 defines the MRPDU/Message/AttributeList structure and permits all three layouts: one Message per value, grouped, and "+k" packed. lwSRP #17 says this itself ("All three encodings are valid under IEEE 802.1Q-2018 10.8.1/10.8.2"), and gives the reason for grouping as the interoperability baseline the project chose, set by the captured reference end station. The sentence is true, because the clause defines the structure it names. A reader could still take the parenthesis as the clause requiring the grouping.
- Impact: none on behaviour. A future reader might treat a peer's per-value MRPDUs as non-conforming.
- Optional outcome: e.g. "Its PR #18 sends one Message per AttributeType in each MRPDU, a layout IEEE 802.1Q-2018 10.8.1.2 permits, matching the reference end station's captured layout (lwSRP #17)."
- Verification: read the line.

### S2 SUGGESTION, lens Tests: `sw/firmware/ctrl/test/srp_latency.cpp:81-84`, the end assertion cannot tell a Message EndMark from the MRPDU EndMark in MVRP

- Evidence: probe `m2-noendskip` drops the `off+=2;` that skips the Message EndMark. It still passes at IF=1 and IF=2 (`receipts/walk/m2-noendskip.log`). MVRP has a single AttributeType (11.2.3.1), so a grouped MVRP MRPDU's only Message EndMark is immediately followed by the MRPDU EndMark. The walk then stops one EndMark early and still lands on `00 00`. This is an equivalent mutant for every frame the arm sees, not a missed defect: LeaveAll detection reads the first vector, and that is unchanged.
- The probes that matter fail as they should:
  - `m1-vecsize` (vector size without the ThreePackedEvents rounding), `m3-onevector` (only the first vector of a Message read) and `e1-oldwalk-assert` (the old walk) fail at IF=1 and IF=2 on the new assertion.
  - So the multi-vector loop is exercised, by the grouped LeaveAll Message's LeaveAll vector plus VID vector.
- Optional outcome: none required. If wanted, assert that the octets after the walk's EndMark are only the second EndMark or frame padding.
- Verification: rerun `m2-noendskip` with any such strengthening.

### Observations (not findings)

- O1, Tests: the H-SRP rows that `srp_latency` prints change slightly, base against head, because grouped PDUs are shorter.
  - Service time changes by -500 ns to +200 ns per path, and accesses change by -12 to 0 (`receipts/walk/hsrp-base-vs-head.txt`). The +200 ns is "Talker RX to Listener", with 2 fewer accesses: its origin shifts.
  - Every row stays under the 10 ms allowance.
  - No tracked record holds these rows: a search of `H-SRP` finds only prose. The gate's printed output does not include them either, so the HANDOFF's "differs in exactly three ways" claim is accurate for the gate output it describes.
- O2, Conformance: the published reference-capture statement is the lwSRP #17 issue body. A Milan-certified reference end station encodes one Message per AttributeType holding one VectorAttribute per value, with NumberOfValues 1, ascending FirstValue and no "+k".
  - The `08ee86e8` encoder (`src/core/mrp_mad.c` `tx_message`/`tx_assemble`) and my grader agree with that statement on every head MRPDU: one Message per type, types ascending, a NumberOfValues-0 LeaveAll vector only first, every other vector NumberOfValues 1, FirstValue strictly ascending.
  - The capture itself is not in any artifact I could open, and its LeaveAll placement is not stated publicly. This review therefore confirms agreement with the published statement, not with the capture bytes (section 6).
- O3, Robustness: the grouped layout is never longer than the per-value layout. Per type it saves the Message header, and for LeaveAll types the separate Message, on every value after the first.
  - So no buffer or channel bound can be newly exceeded: `srp_mbx.c:800` passes `sizeof(m->frame) - 14u`, unchanged.
  - The measured octets confirm it: base 289,969 against head 285,067.
  - `tx_assemble` returns `-SHLAN_ERROR_INVALID` on an `encode_attr` length mismatch without committing a prepared PDU, as the old code returned the encoder's error mid-loop.

## 3. Acceptance (issue #711, frozen)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Gitlink at `08ee86e8`, no other lwSRP change | Met | `receipts/gitlinks.txt`: the only gitlink change is `160000 9197193e4 -> 08ee86e81`. `.gitmodules` is unchanged. No vendored lwSRP source is in the tree. `08ee86e8` is on lwSRP `main` with tree `67b35af9`, equal to the reviewed head `a44eeedf`'s tree. Its `src/` diff touches only `mrp_mad.c` and `mrp.h`. |
| 2 | Firmware arms, including the F4 SRP set at IF=1/2, pass; coverage 100 % with the same denominator; every campaign keeps its kills; changed byte-level expectations are updated, cited and listed in HANDOFF.md | Met | Arms and campaigns: `receipts/fw/head-selftest.log`, `head-selftest-tally.txt`, rc 0 at the exact head. It shows 59 arms ok, `mutants: 471 of 471 caught`, 313 of 313 later verdicts (AECP 74, SRP 169, SRP one-interface 68, pin 2), 0 escaped, and the pin refusals naming `08ee86e8`. Coverage: `head-cov-check.log` rc 0, 30 files; `head-cov-vs-ratchet.txt` has 30 of 30 rows equal to the unchanged `coverage.ratchet`. The only byte-level expectation change is the walk at `srp_latency.cpp:76-84`, cited to 802.1Q-2018 10.8.1.2 in the code and listed in the published `author/HANDOFF.md` "Byte-level SRP expectations". The grep in section 4 finds no other tracked expectation tied to the old layout. |
| 3 | Capture re-measured; candidate logs equal base apart from attributed lwSRP changes; `check_nvm_capture.py` passes | Met (premise note) | `check_nvm_capture.py` rc 0 at the head (`receipts/docs/subset-sys-check_nvm_capture.log`). The capture inputs are unchanged: an empty diff under `tb/verilator/nvm_capture_cpu` and `sw/firmware/milan_baremetal`. `sha256(milan_baremetal.c)` = `a73ecc25…` equals the receipt's `product_firmware_sha256`. lwSRP is absent from the capture and shipping builds (grep, section 4). The author published nine byte-identical base/candidate logs (`author/evidence/capture/capture--compare.json`). The issue's premise "the firmware digest moves" is false for this receipt; the author published that, and the invariant holds with nothing to attribute. I did not rerun the capture campaign (section 6). |
| 4 | Every pin-derived record re-recorded through its generator | Met | `submodule_boundaries.gen.py --check` and `--selftest` rc 0 ("5 exact gitlinks, decoded PNG"). `check_submodule_docs.py` and `--selftest` rc 0. `check_diagram_pngs.py` and `--selftest` rc 0. `PNG_MANIFEST.json` digests are bound. No other tracked file names the old pin, apart from the deliberate PR #15 history sentence at `srp/README.md:292`. |
| 5 | All-fabric shipping image unaffected beyond firmware ROM bytes, which match the documented digest | Met (premise note) | lwSRP is compiled only into `sw/firmware/ctrl` test and size fixtures. The shipping ROM's sources (`milan_baremetal`, LiteX BIOS) contain no lwSRP reference (section 4), so this lane cannot move the ROM. The author's published three-export comparison and route receipts show the ROM identical (`a14e34e7…` 1x1, `cf2c371f…` 8x8) and `route-1x1` identical, with a PASS at zero delta. No tracked record documented a shipping ROM digest before this lane, and the author published that. The digests are now documented in the PR and HANDOFF. I did not rerun the export or Vivado (section 6). |

## 4. Work done (all at the exact head unless stated; receipts listed in MANIFEST.sha256)

1. Firmware unit job (`firmware-unit` steps) in a clean shared clone at `49b437f4` with lwSRP `08ee86e8`, the other submodules at their gitlinks, and the pinned RV32 SDK installed offline by `scripts/ci_rv32_sdk.py`. The archive sha256 `d42680e9…` equals `ARCHIVE_SHA256`; the compiler is GCC 14.3.0 from Buildroot `2021.11-18033-g83947c7bb6`. Host toolchain: GCC 16.2.1, GoogleTest/GoogleMock 1.18.0.
   - `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`: rc 0. 59 arms ok, 471 of 471, 313 of 313, `test_ctrl_firmware: PASS`.
   - `fw_coverage.py --selftest`: rc 0, 28 of 28. `fw_coverage.py --check --jobs 4`: rc 0, `firmware coverage: PASS (30 files)`, `srp_mbx.c` 515/515 lines and 478/478 branches.
   - `tally_selftest.py`, `fw_rv32_selftest.py --require-rv32` and `test_ctrl_nvm.py --require-rv32`: rc 0 (435 tests, 5 shapes).
   - The tree was still clean afterwards (`receipts/fw/head-tree-state.txt`).
2. Walk matrix: `scripts/make_probes.sh`, `scripts/run_probes.sh` and `scripts/latency_arm.py`. Each tree's own `srp_arms.arm_srp(..., test="srp_latency.cpp")` ran at IF=1 and IF=2 under that tree's own lwSRP pin check. Probe diffs are in `receipts/walk/*.diff`; `receipts/walk/summary.tsv` gives 10 of 10 as expected, apart from the equivalent mutant described in S2:

   | Probe | Tree | lwSRP | Expected | Result |
   |---|---|---|---|---|
   | head-exact | `49b437f4` | `08ee86e8` | pass | pass |
   | base-exact | `e8454e27` | `9197193e` | pass | pass |
   | e1 old walk + new assertion | head | `08ee86e8` | fail | FAIL at IF=1 and IF=2: `walk must end on the MRPDU EndMark` |
   | e2 new walk | base | `9197193e` | pass | pass |
   | e3 old walk + assertion | base | `9197193e` | pass | pass |
   | e4 first commit `55ef91b7` (old walk, no assertion) | | `08ee86e8` | pass | pass (the gap the assertion closes) |
   | m1 vector size `n/3` | head | `08ee86e8` | fail | FAIL at both |
   | m2 Message EndMark not skipped | head | `08ee86e8` | fail | pass: equivalent mutant (S2) |
   | m3 one vector per Message | head | `08ee86e8` | fail | FAIL at both |
   | m4 old walk, no assertion | head | `08ee86e8` | pass | pass |

3. Decoded SRP behaviour.
   - Instrumentation: `scripts/instrument_model.py` adds a dump hook to `sw/firmware/ctrl/host/mbx_model.c` in two disposable clones (base with `9197193e`, head with `08ee86e8`). It records every SRP-channel TX frame and every model reset; it is standard C only.
   - `test_ctrl_firmware.py --require-rv32` (no self-test) ran in both clones: rc 0 on both sides, 59 arms ok, and the 59 verdict lines are identical.
   - `scripts/mrpdu_compare.py` is my own decoder, written from 802.1Q-2018 10.8.1.2, 10.8.2.4 to 10.8.2.10, 35.2.2 and 11.2.3.1. It decoded 35 executables' frames, including all SRP suites, `srp_shape` at five shapes, and AECP mailbox at IF=1/2. Result: 4,186 MRPDUs, 2,201 byte-identical, 1,985 layout-only, 0 decoded differently, 8,278 values, 173 LeaveAll types, 122 non-MRP frames, octets 289,969 / 285,067, 0 problems. LeaveAll precedes its type's values on both sides, and every head MRPDU passes the grouped grader. 647 base MRPDUs carry a type in two Messages.
   - The raw frame dumps are archived as `receipts/decode/dump2-base-head.tar.xz`. Rerun with `python3 -I scripts/mrpdu_compare.py dump2/base dump2/head` after extracting; it reproduces the counts above.
   - Controls (`receipts/decode/controls.tsv`): a dropped event, a changed event, and one changed ThreePacked octet in a head frame each exit 1 with one DECODED DIFFERENTLY. Swapping the sides reports 2,177 non-grouped base PDUs.
   - Normalised arm output differs, base against head, only in the lwSRP revision line, the `srp_app` transmitting-poll figure (48 to 46 at IF=1, 91 to 89 at IF=2, bounds 770 and 1,540 unchanged), and RV32 `core_mrp_mad.o` text 12,709 to 13,309 (+600) with the largest static frame unchanged.
4. Author's decoder (`author/evidence/scripts/decode_compare.py`): I read it. It is written from the same clauses, decodes MSRP FirstValue increments (my decoder instead refuses MSRP NumberOfValues above 1, and none occurred), and rejects trailing non-zero octets. My counts equal its published counts field for field.
5. lwSRP encoder review at `08ee86e8` (`src/core/mrp_mad.c:1288-1500`):
   - The Message header is 2 octets, or 4 for MSRP with AttributeListLength.
   - AttributeListLength covers the vectors and the list EndMark, consistent with the old encoder's `list` term.
   - A LeaveAll vector (header `0x2000`, zero FirstValue) is emitted first per type, then one NumberOfValues-1 vector per value, insertion-sorted by FirstValue octets.
   - Messages come in ascending type order, then the MRPDU EndMark.
   - The capacity accounting charges the Message header and EndMark once per type, and reserves 3 octets for ProtocolVersion and the MRPDU EndMark.
   - MSRP room is capped at 65,535. A refused send keeps the prepared PDU, as before.
6. Docs at the head: `docs_check.py`, `check_em_dash.py --base e8454e27` (0 findings over 11 added lines), `check_doc_style.py` and `--selftest`, `DOC_MAP.gen.py --check`/`--selftest`, `check_solution_docs.py` and `--selftest`, `check_feature_status.py --self-test`, `gen_module_matrix.py --check`, `gen_toc.py --selftest`/`--verify-anchors`/`--check`, and `ci_events.py --check`: all rc 0 (`receipts/docs/summary.txt`, `subset.tsv`). Four environment-only refusals are recorded and were rerun to rc 0:
- `check_diagram_pngs.py` rc 1 under isolated mode, which drops the script directory from the import path;
- `check_em_dash.py` rc 2 without the hash-locked Markdown renderer;
- `check_nvm_capture.py` and `ci_events.py --check` without pyyaml in the Markdown environment. The moved lwSRP permalinks cite text identical to the old lines (`receipts/docs/permalinks.txt`).
7. Pin consumers, grep at the head:
   - `9197193e` remains only in the deliberate PR #15 history line.
   - `third_party/lwSRP` and `mrp_mad.c` appear only in firmware test and size fixtures, CI, docs and act tooling. Nothing in `syn/`, `sw/builder`, `sw/firmware/milan_baremetal` or `tb/verilator/nvm_capture_cpu` refers to them.
   - No tracked record holds a control-firmware size, H-SRP row or poll figure that this change moves.

## 5. Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #711 acceptance 1 to 5 against section 3 evidence. `srp_latency.cpp:76-84` against 802.1Q-2018 10.8.1.2 (MRPDU ::= ProtocolVersion Message... EndMark; AttributeList to EndMark), 10.8.2.8/10.8.2.10.1 (ceil(N/3) ThreePackedEvents) and 11.2.3.1 (MVRP has no FourPackedEvents). lwSRP `08ee86e8` `src/core/mrp_mad.c:1288-1500` encoder structure and AttributeListLength. Decoded equivalence over 4,186 MRPDUs with my decoder (`receipts/decode/compare.json`). The grouped form against the lwSRP #17 reference statement (O2). | R596-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| RTL | CLEAN | `receipts/gitlinks.txt`: no `hdl/`, `syn/` or `tb/` file in the diff; the only code-bearing change is a firmware-library gitlink. lwSRP's absence from every RTL, synthesis, builder, shipping-ROM and capture source (grep, section 4.7). The processor ROM pins are unchanged (`2ad2f845`, `5dce647a`). Hosted exact-head `elaborate`, `yosys-elaboration`, Yosys shards 0-3 and `verilator-lint` read success (`receipts/hosted-check-runs.tsv`; the manager owns the hosted verdict). The author's published route/export receipts show identical ROM and route figures. | R596-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| Robustness | CLEAN | `srp_latency.cpp:69-84` bounds: every header read is guarded by `off+2<=f->len`, and an overrun ends in the assertion. Probes m1 and m3 fail and e1 fails at both interface counts. `mrp_mad.c` capacity accounting, the 65,535 cap, the retained-PDU path and the encode-failure path (O3). The grouped layout is never longer than per-value (O3); `srp_mbx.c:800` capacity is unchanged. The 8x8 and 4x4 shapes at IF=1/2 are in the decoded set. | R596-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| Tests | CLEAN (S2 is a SUGGESTION) | `receipts/fw/head-selftest.log`: 59 arms, 784 of 784 planted defects. `receipts/fw/head-cov-check.log` against `coverage.ratchet`: 30 of 30 rows equal. `receipts/walk/summary.tsv`: 10-probe matrix at IF=1/2. `receipts/decode/controls.tsv`: 4 controls. `srp_latency.cpp` walk can fail for the defect it claims (e1, m1, m3). | R596-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| Docs | CLEAN (S1 is a SUGGESTION) | `docs/reference/SUBMODULES.md:26,229`, `sw/firmware/ctrl/README.md:340-342`, `sw/firmware/ctrl/srp/README.md:75-76,292-293,343-345`, `docs/design/MAILBOX_SPLIT.md:295`, `docs/diagrams/submodule_boundaries.{drawio,svg,png}` and `PNG_MANIFEST.json` through their generators and checkers. Permalink text identity (`receipts/docs/permalinks.txt`). Documentation gates (`receipts/docs/`). The published HANDOFF and PR body are sufficient for a cold reviewer, with the acceptance 3/5 premise notes stated publicly. | R596-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |

## 6. Real limits

- No hardware, bench, flashing or physical calibration. Physical calibration was NOT RUN; field skips are not hardware proof.
- I did not rerun the saved-state capture campaign, the all-fabric export or the Vivado `route-1x1`. Acceptance 3 and 5 rest on unchanged inputs and the lwSRP-absence analysis I verified, plus the author's published receipts.
- I did not run the Yosys bank, the Verilator sweep, `tsn_fuzz`, `xvlog_gate.py`, the docs workflow commands that need the gPTP submodule build, `act_ci.py` or its self-test (not permitted or not applicable).
- The reference end-station capture is not public in any artifact I could open. O2 confirms agreement with the published lwSRP #17 statement, not with the capture bytes, and the peer's decoding of grouped MRPDUs was not observed.
- I had no licensed copy of IEEE 802.1Q-2018. The clause structure was checked against the repository's own restatement (`docs/traceability/ieee8021q.md` MRP-1/MRP-5) and lwSRP's comments. The lettered sub-items the PR cites (10.8.1.2 b, c, d) were not checked against the standard text.
- The walk and decode probes ran on disposable clones, not on the review clone. The review clone's tracked bytes were not modified (section 9).
- This is a source-head review only. No manager source bank ran at this head, and none is claimed or inferred.

## 7. Prior public findings on PR #718

I read the PR's issue comments, reviews and review comments only after sections 1 to 6 and the ledger were written (`receipts/ordering.txt`). At that point the PR carried two `[A10] INDEPENDENT REVIEW STARTED` comments (R596-1, R597-1) and no review or inline comment. No prior public finding exists on PR #718, so there is nothing to resolve or retain. I did not read the parallel external reviewer's report.

## 8. Pending manager duties

- Validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks at the merge turn, and link the receipts.
- Own hosted and local-replica acceptance. At snapshot 2026-10-11T00:29:43Z, exact-head `firmware-unit`, `docs-check`, `elaborate`, `yosys-elaboration`, Yosys shards 0-3 and Verilator shard 3 read success. Verilator shards 0, 1, 2 and 4 were in progress and the `rtl-fast` aggregate was queued. "Physical gPTP" was skipped (not executed).
- Accept or rule on the acceptance 3 and 5 premise readings the author published: no capture digest move, and no prior documented shipping ROM digest.
- Carry S1 and S2 as optional.

## 9. Clone integrity

`receipts/clone-integrity.txt`: the review clone at `$REVIEWS/r596-1-711` is still at HEAD `49b437f4`.
- The index tree (`write-tree`) equals `HEAD^{tree}` `3bb600ec…`.
- The worktree equals HEAD in tracked bytes and modes, and there are no untracked files.
- The submodule status is unchanged from the start of the review: `third_party/lwSRP` gitlink `08ee86e8` (uninitialised, as at start); `protocol-processor` `2ad2f845`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` at their gitlinks.
- Every probe, build and edit ran in disposable clones under the packet's `scratch/`. Nothing was committed, pushed or written to GitHub.

R596-1 FINISHED
