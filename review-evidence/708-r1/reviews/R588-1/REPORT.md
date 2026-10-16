[R588] NEGATIVE - exact head 5c6f50eefa4c5545f052ec843363ace5e7936e8a

# R588-1 internal cleared-context review: issue #708 / PR #754

- Head: `5c6f50eefa4c5545f052ec843363ace5e7936e8a`, tree `d4b0e17fdf530ddb2ca8ec8c3986bcc4a9189254` (verified in the review clone: index tree, worktree and every gitlink equal the head; receipt `receipts/clone_integrity.txt`).
- Source base: dev `734eb780dc93896a5961cd95180f79475a401650` (an ancestor of the head; merged at `a1dfbfad`). Live dev `8eacc40839d95ff0e8cb26d0169cc1638800a44d` was not merged or validated here.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #708 body and its assignment, 08:46 ruling, flow decision (6100507393) and resume ruling (6207474061), the PR body, the diff `734eb780..5c6f50ee` and its ten commits, the processor range `2ad2f845..2cbed0a9`, the Milan v1.2 and IEEE 1722.1-2021 texts, and the public evidence archive `review-evidence/708-r1` at `af691a78` (all 57 manifest entries re-hashed and matching).
- One open MINOR (F1, Docs) makes this round NEGATIVE. Conformance, RTL, Robustness and Tests are covered clean at this head.

## Findings

### F1 - MINOR - Docs - the pin page understates the #168 VLAN change: input GET_STREAM_INFO and GET_RX_STATE now carry the processor's 16-bit VLAN, and the parent's halfword is no longer used

- Where: `docs/reference/SUBMODULES.md:199` (the #168 row: "listener records keep 16 VLAN bits"), `docs/reference/SUBMODULES.md:208-210` ("The parent's `acmp_bound_vlan_o` keeps 12 bits per sink. Only the processor's internal record widens to 16."). The PR body's Scope row for #168 says the same thing ("16 VLAN bits in the processor's record (`acmp_bound_vlan_o` stays 12 bits)").
- Evidence. At the adopted pin `2cbed0a9`:
  - `protocol-processor/hdl/top/protocol_processor_top.sv:3536-3539` (`gsi_answer`): for a STREAM_INPUT (`gsi_input_w`), GET_STREAM_INFO selector 6 replaces bits [63:48] with `bound_vlan_r[gsi_sink_w]`. That is all 16 received bits while probing is COMPLETED, and 0 otherwise. The integrator's `gsi_data_i[63:48]` is never used for an input. This arm is new in this range: at `2ad2f845` selector 6 passed `gsi_data_i` through.
  - `protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv:698`: GET_RX_STATE_RESPONSE's `stream_vlan_id` is now the 16-bit `settled_vlan`. Before, it was `{4'd0, 12 bits}`.
  - The processor's own guide documents the ownership move (`protocol-processor/docs/guides/integrator.md:575-577`: "Input selector 6 replaces bits [63:48] with all 16 received VLAN bits while settled, or zero while unsettled. Your VLAN halfword is unused for inputs").
  - The parent's `hdl/milan/milan_datapath.sv:5190-5192` still serves the input halfword (`gsi_setl_w ? {4'd0, pp_cd_acmp_bound_vlan_w[...]}`). Unlike selectors 4 and 7 (`:5174-5175`, `:5198`), it carries no note that the processor now replaces it.
- Impact. The parent's authoritative pin page tells a reader that only an internal record widened, but the change is visible on the wire in two responses, and the ownership of one GET_STREAM_INFO field moved from the parent into the processor. Someone working from SUBMODULES.md or the datapath arm would believe the parent's 12-bit halfword is what a controller reads, and could change or test the wrong side. This misses the completion bullet "no undocumented requirement/interface change remains". It is not wording only: it is a claim about interface behaviour.
- Required outcome. The #708 section of `docs/reference/SUBMODULES.md` and the PR body state three things:
  - the processor now serves STREAM_INPUT GET_STREAM_INFO selector 6's `stream_vlan_id`: all 16 received bits while settled, and 0 otherwise;
  - GET_RX_STATE_RESPONSE carries the full 16 bits;
  - the parent's selector-6 input VLAN halfword is no longer used, while `acmp_bound_vlan_o` stays 12 bits.

  A matching one-line note at `milan_datapath.sv`'s selector 6, as for selectors 4 and 7, is the natural companion, but the required outcome is the documentation statement.
- Verification. Read the revised text against `protocol_processor_top.sv:3536-3539` and `KL_pp_acmp_listener.sv:698` at `2cbed0a9`. `docs_check.py`, `check_em_dash.py --base 734eb780`, `gen_toc.py --check` and `check_submodule_docs.py` exit 0. If the RTL comment is touched, lint and the pp_shadow/milan_dp suites stay green.

### R1 - RESIDUE - Docs - an issue-comment ID was carried into a rewritten source comment

- Where: `sw/firmware/ctrl/test/acmp_walk.cpp:64` "(#665, comment 6030067436)".
- Evidence. The owner's 2026-10-15 rule, restated in #708's resume ruling: source comments never show issue-comment IDs. This paragraph was rewritten in `afc0b831`, and the ID was kept. The instance existed at base `734eb780` and is not among #746's listed known instances.
- Exact fix: replace "(#665, comment 6030067436)" with "(#665)". The design page `docs/design/MAILBOX_SPLIT.md:805` keeps the ruling link.
- Line 5's pre-existing "#665 lane F3" is outside the delta and is noted for #746's re-scan, not as a finding here.

### R2 - RESIDUE - Docs - the history sentence says the old walk normalised only LD1 and LD2

- Where: `sw/firmware/ctrl/test/acmp_walk.cpp:43` ("this walk normalised LD1 and LD2 before comparing") and `docs/design/MAILBOX_SPLIT.md:784` ("normalised the first two before comparing").
- Evidence. Base `734eb780`'s `ListenerScenario.LD3TheLockRefusalStatus` also overwrote the processor frame's status byte with 16 before its byte compare (`e.frames[0].b[2] = ...`, removed in `afc0b831`). The sentence describes removed code only. No current test, check or figure depends on it.
- Exact fix: "normalised LD1 and LD2 in the walk, and LD3's status byte in its scenario, before comparing". On MAILBOX_SPLIT.md: "normalised the first two in the walk and the third's status byte in its scenario before comparing".

### S1 - SUGGESTION - Tests - two more #168 convergences are not observable in the walk

- Evidence. Against processor `2ad2f845`, the new walk's failing tests are exactly the eight `UNBIND_*` cells, `TMR_RETRY_PWT_disc` and `LD3TheLockRefusalStatus` (`receipts/acmpwalk_oldpin_newwalk.log`).
- Two other changes in processor PR 171 are therefore not distinguished by the walk:
  - a probe sent on TMR_DELAY keeps the prior ACMP status (`KL_pp_acmp_listener.sv`, the A5 arm: "Milan 5.5.3.5.10 leaves the prior probe status unchanged");
  - the outstanding probe keeps its original controller across a same-talker rebind ("Milan 5.5.3.5.17/.18").
- The firmware already behaves this way (tsn-c-stack `src/acmp.c`: `probe()` leaves the status, and `probe_controller` is saved per probe), so nothing differs today.
- Optional: walk a TMR_DELAY reached from TMR_RETRY with a non-zero status, and a same-talker BIND_RX from a second controller in PRB_W_RESP. Raw comparison would then guard both against regression.

### S2 - SUGGESTION - Tests - the processor's sv2v 0.0.12 nvm_port guard failure wants its own issue

- Evidence. The author's declared note reproduces:
  - `protocol-processor/tb/nvm_port` `make elab` with sv2v v0.0.12 ends `YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the guard's $finish` at both `2cbed0a9` and `2ad2f845`;
  - with v0.0.13 it passes at both (`receipts/nvm_port_elab_*.log`).
- The parent pins v0.0.12 (`.github/workflows/elaborate.yml:85`, `docs.yml:286`). The processor's own workflow installs the latest release (`protocol-processor/.github/workflows/hdl.yml:108`).
- The failure is independent of the pin and of the adoption, so it is not a finding against this PR. Filing the version disagreement as its own issue is the right disposition.

## Lens coverage (each applied at the head)

| Lens | Result | Artifacts examined | What was checked and against what |
|---|---|---|---|
| Conformance | PASS | `sw/firmware/ctrl/test/acmp_walk.cpp:41-66,435-447,523-540,796-799`; processor `hdl/acmp/KL_pp_acmp_listener.sv`, `KL_acmp_talker.sv:1301-1306`, `pp_acmp_pkg.sv:123`, `tb/acmp_listener/sim_main.cpp` (model `f_unbind`, cases 5 and 12), `tb/acmp_talker/sim_main.cpp:1187-1194`; Milan v1.2 Table 5.36, 5.5.3.5.10, 5.5.3.5.30, 5.5.4.2, Table 5.44; IEEE 1722.1-2021 8.2.1.5 and Table 8-3 | LD1: success UNBIND_RX_RESPONSE talker fields are 0, as Table 5.36 gives. LD2: 5.5.3.5.30 step 2 sets no status. LD3: Table 8-3 gives 13 TALKER_MISBEHAVING and 16 CONTROLLER_NOT_AUTHORIZED. TD1: 5.5.4.2 step 1 and Table 5.44 give TALKER_UNKNOWN_ID. Every reading in the walk, MAILBOX_SPLIT.md and the PR matches the text. Acceptance 1: the gitlink is `2cbed0a9` (processor `main`, a descendant of `2ad2f845`), set by `75a28523` alone, and the merge keeps it. Acceptance 2: re-baselined under the AREA_BUDGET.md rule, route at +0.215 with no exception. Acceptance 3: firmware/ROM images equal dev's in both route manifests, and `check_nvm_capture.py` rc 0. Acceptance 4: author receipts plus the focused runs below, with the image difference judged below. |
| RTL | PASS | gitlink `protocol-processor` (`git ls-tree`), `scripts/port_docs.budget`, `hdl/milan/KL_pp_shadow.sv:678,1326`, `hdl/milan/milan_datapath.sv:5170-5200`; processor `hdl/top/protocol_processor_top.sv` ports and `gsi_answer` (`:3500-3545`); route manifests `cand2-route-manifest.json` vs `base2-route-manifest.json` | No parent `hdl/` file is in the delta. New processor top ports are the parameter `N_AVB_IF_P` (default 1) and input `rx_if_index_i` (default 0); the parent connects neither, and at 1 the new latches are empty generate bodies. The census line for `u_normalizer.rx_if_index_i` is removed because the processor now connects it, and the writer reproduces the budget byte for byte. `acmp_bound_vlan_o` stays 12 bits. The GSI overlay is gated by `gsi_input_w`, so STREAM_OUTPUT words are untouched; the documentation side is F1. The route inputs differ from dev `734eb780`'s only in the six processor RTL files; generics and memory images are identical. Lint is 90 <= 90 (`receipts/lint_rtl_check.log`). |
| Robustness | PASS | processor `tb/acmp_talker` (invalid sources 8 and 0xFFFF, state unchanged), `tb/acmp_listener` field cases; `tb/verilator/pp_shadow` and `tb/verilator/milan_dp` at the head (every shape it builds, 1x1 through 8x8 and its divergent fixture) | Feature- and configuration-dependent behaviour: one interface per shape and every shape elaborates and passes (pp_shadow 317 checks, 0 failures; milan_dp rc 0, every shape PASS; `receipts/suite_*.log`). Malformed input: an invalid DISCONNECT_TX source is refused at both edges of the range and leaves state unchanged (talker suite 1,376/0). The listener suite passes 3,167/0. LD1 is scoped to SUCCESS frames, so the locked-refusal echo of talker fields stays correct. No new timeout, reset or backpressure path enters the parent. |
| Tests | PASS (S1, S2 optional) | `acmp_walk.cpp`; `scripts/measure_test_evidence_readers.py`; the receipts `acmpwalk_*`, `test_evidence_without_patch.log` | At the head the walk passes 127/127. Against processor `2ad2f845` it fails LD1 in all eight UNBIND cells, LD2 in TMR_RETRY x PWT (discovered) and LD3, each by name, and the raw byte compares fail with them. The base walk passes at `2ad2f845` and fails at `2cbed0a9`, which shows the update was owed. The mutant expectations that name these checks (`acmp_mutants.py:177,491`) still match the retained message prefixes. The pp170 patch is byte-identical to `review-evidence/pp170-r1/author/parent-name-evidence.patch`. Removing only its entry makes `measure_test_evidence.py --check` exit 1 naming `protocol-processor/tb/name_state/mutants.py: UNEXPLAINED`. |
| Docs | UNCLEAN (F1 MINOR; R1, R2 residue) | `docs/reference/SUBMODULES.md:186-212`, `docs/design/MAILBOX_SPLIT.md:775-806,1110`, `sw/firmware/ctrl/README.md:517-532`, `sw/firmware/ctrl/aecp/README.md:136-155`, `docs/design/AREA_BUDGET.md:10-140,386-390,423-430,486-494`, `docs/design/MARK_II_AREA_PLAN.md:56,110,655-660`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-117`, `syn/ooc/pp_resource_baseline.json`, `syn/yosys/rom_digests.tsv`, `docs/diagrams/submodule_boundaries.*`, `PNG_MANIFEST.json` | Every resource figure, difference and percentage in the four pages matches the JSON and the gate receipts (49,613 / 63,400 = 78.25 %, 11,573 over, 86.5 tiles, 125 free, 11,541 = 38,040 - (49,613 - 23,114), deltas -400/-1,953/-28, -0.018/+0.019, +135/+42, +76/+71, +7.446, +0.336). The JSON diff changes only `measured` notes, figures, scopes and input digests; no policy. ROM digests regenerate equal (`rom_regen_2cbed0a9.log`). The boundary diagram, PNG, port census and naming budget match their generators. The docs gates are rc 0 with the pinned renderer. F1 is open. |

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | walk LD1-LD3/TD1 against Milan v1.2 Table 5.36, 5.5.3.5.30, 5.5.4.2, Table 5.44 and IEEE 1722.1-2021 Table 8-3; #708 acceptance 1-4 | R588-1 | `5c6f50eefa4c5545f052ec843363ace5e7936e8a` |
| RTL | CLEAN | gitlink, processor top ports and GSI overlay, parent shadow/datapath wiring, route input manifests, lint | R588-1 | `5c6f50eefa4c5545f052ec843363ace5e7936e8a` |
| Robustness | CLEAN | processor ACMP talker/listener suites at the pin, pp_shadow, milan_dp (all shapes) | R588-1 | `5c6f50eefa4c5545f052ec843363ace5e7936e8a` |
| Tests | CLEAN | walk controls at both pins, base walk at both pins, patch control, mutant message prefixes | R588-1 | `5c6f50eefa4c5545f052ec843363ace5e7936e8a` |
| Docs | UNCLEAN (F1) | pin page, MAILBOX_SPLIT, firmware READMEs, AREA_BUDGET, MARK_II plan, #234 findings, records and generators | R588-1 | `5c6f50eefa4c5545f052ec843363ace5e7936e8a` |

## Judged items from the assignment

- **Gitlink.** `2ad2f845 -> 2cbed0a9` arrives only in `75a28523` (one path changed), and `a1dfbfad` keeps it. The first-parent range carries processor PRs 165, 166, 169, 171 and 172. 165 and 166 are accepted by the 08:46 ruling and listed on the pin page and in the PR. No other processor change is present.
- **Patch.** Byte-identical to the pp170 lane's published patch, and the disposition describes the driver accurately: `tb/name_state/mutants.py` plants edits in copies and grades named assertions. The control fails without it.
- **Retired normalisation.** The walk compares frames and records raw. LD1-LD3 fail by name when the old processor answers return, demonstrated against the real `2ad2f845` model, not a synthetic plant. The issue's acceptance "a control that fails if the fabric echo returns" is met.
- **Regenerated records.** ROM digests: the generators at `2cbed0a9` give `23cc67ee...` / `518b900c...`, equal to the new rows (and to the `2ad2f845` rows). The pin page passes `check_submodule_docs.py`. The boundary diagram passes `submodule_boundaries.gen.py --check` and `check_diagram_pngs.py`. The port census and naming budget writers, run in a probe copy at the head, leave no diff.
- **Resource re-baseline.**
  - The rule followed is AREA_BUDGET.md: the PR measures all three endpoints on its merge result and writes them with `record --write`, the policy unchanged.
  - Checks before the write: route-1x1, ooc-1x1 and ooc-8x8 each `RESULT: PASS` against #696's record. After the write, each passes again at zero delta, and `check-baseline` passes (re-run here: rc 0).
  - Gate identity matched, so the recipe and flow commands are unchanged.
  - All 122 repository route inputs of the measured route equal the head's bytes; the other entries are 3 CPU sources outside the repository and 2 generated files. Its inputs differ from a dev `734eb780` export only in the six processor RTL files, so there is no new constraint and no pblock.
  - Timing at all four corners is at or above the floors: WNS +0.215 (Slow) / +1.683 (Fast), WHS +0.102 / +0.036. That is 0.185 above the +0.030 floor, with falls of 0.018 from the record and 0.131 from dev's +0.346 reference.
  - The flow ruling (6100507393) required no logic cut; none was made, and no directive, pblock or floor exception was used.
  - The record now also absorbs dev's Mark II M7 movement (-2 RAMB18, most of -1,953 FF). The findings page and AREA_BUDGET.md attribute it openly, and the manager's assignment required the record. That is consistent with the rule.
- **Firmware digest.** Unchanged: the `images` lists of the candidate and base route manifests (memory, ROM and SRAM inits) are identical, and the firmware sources in the delta change only a host test. `check_nvm_capture.py` passes, so the capture correctly was not re-measured.
- **Declared image difference.** Accepted as declared. The bitstream is the gated route's own checkpoint with the shipping configuration properties, DRC clean, and its four corners are recorded. It is therefore a measured image of the adopted design. The shipping launcher's eight-worker synthesis is a different implementation of the same inputs, and nothing in this PR measures its timing. BUILDING.md section 5 says the +0.03/0 thresholds are not enforced automatically. That is carried below as a manager duty, not a finding.
- **sv2v 0.0.12 note.** Accurate and independent of the pin (S2).

## Commands run here (all at the head unless stated; receipts under `receipts/`)

- `scripts/acmpwalk_only.py` (runs only the gate's `acmpwalk` arm through the checkout's own pin proof):
  - at the head: 127/0, rc 0;
  - head walk on processor `2ad2f845`: rc 1, LD1 x8, LD2, LD3 by name;
  - base walk on `2ad2f845`: rc 0;
  - base walk on `2cbed0a9`: rc 1.
- `scripts/verify_route_manifest.py`:
  - measured route manifest vs head: 122 match, the 3 non-matching being CPU sources outside the repository;
  - dev manifest vs dev `734eb780`: 112 match, the rest being external sources or submodules not initialised in the probe copy;
  - between the two: six processor files differ, and images and generics are equal;
  - standalone manifests vs head: every repository file matches.
- Exit 0 at the head:
  - `pp_resource_gate.py check-baseline`, `measure_test_evidence.py --check`, `check_submodule_docs.py`, `submodule_boundaries.gen.py --check`, `check_diagram_pngs.py`, `check_port_contracts.py`, `measure_naming.py --check`, `check_nvm_capture.py`;
  - with the pinned Markdown lock in a scratch environment: `check_em_dash.py --base 734eb780` (0 findings over 192 added lines), `docs_check.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_doc_style.py`, `check_doc_paths.py`.
- Lint, with Verilator 5.050 (identity verified): `lint_rtl.py --check` PASS, 90 <= 90.
- Suites, with Verilator 5.050:
  - `tb/verilator/pp_shadow` (`make -j16`): PASS, 317/0;
  - `tb/verilator/milan_dp` (`make -j16`): rc 0, every shape PASS;
  - processor `tb/acmp_listener` 3,167/0 and `tb/acmp_talker` 1,376/0 at `2cbed0a9`;
  - processor `tb/nvm_port` `make elab` with sv2v v0.0.12 and v0.0.13 at both pins: 0.0.12 fails at both, 0.0.13 passes at both.
- ROM generators at `2cbed0a9` into scratch: digests equal the new rows.
- Probes ran in disposable clones under the packet's scratch directory. The review clone was only read, and it ends equal to the head (`receipts/clone_integrity.txt`).
- Receipt paths are rewritten to placeholders by `scripts/sanitize_receipts.py`.

## Prior public review findings at this head

- I checked these only after the verdict, findings and ledger above were written. When this round started, the PR held only the two review-start comments: no review submissions, no inline comments and no findings.
- One public review comment appeared during this round, R589-1 (comment 6219051857). It carries one finding, R589-1-R1, RESIDUE, Docs, `sw/firmware/ctrl/test/acmp_walk.cpp:64` (issue-comment ID in a source comment).
  - **Retained** at this head: the line is unchanged. It is the same defect as R1 above, and either exact fix resolves both.
- That round records Docs CLEAN. This round's F1 is an independent Docs finding that it does not address. The disagreement is recorded here for the manager, not resolved by either round.

## Real limits

- No Vivado run here. The route, standalone and corner figures are the author's receipts, checked for internal consistency, gate output, input-manifest equality with the head and with dev, and arithmetic. They were not re-measured.
- Not run here: the 63-suite sweep, the processor and gPTP full sweeps, the physical gPTP suite, Yosys, `xvlog`, the builder elaboration bank, the firmware mutation campaigns and BDD. Those rest on the author's published receipts.
- Hosted contexts at the exact head were partly still in progress at the snapshot (`receipts/hosted_checks_snapshot.txt`). `Physical gPTP (nightly and manual)` is a skipped context, not execution evidence. This round claims no hosted or act acceptance.
- No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Candidate-merge validation against live dev `8eacc408` (builder and native banks) at the merge turn, with receipts linked on the PR.
- Hosted `rtl-fast`, `verilator-suites` and `yosys-portability` at the exact head.
- Acceptance 5: post-merge flash and soak. If the flashed image comes from the shipping launcher rather than the measured route's bitstream, grade its signoff corners by hand against WNS >= +0.03 ns and WHS >= 0 (BUILDING.md section 5) before flashing, since that implementation was not measured here.
- Carry R1 and R2 to the residue checklist. Consider an issue for S2's sv2v version disagreement.
- Re-review after F1 is answered.

R588-1 FINISHED
