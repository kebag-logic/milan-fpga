[R532] NEGATIVE - exact head 42a0371affceb2a07a734449d706be01fa5abc9a

# R532-2: internal cleared-context review of PR #690 (issue #665, lane F4), round 2

- Head `42a0371affceb2a07a734449d706be01fa5abc9a`, tree `ab9bd75e4d779adcc76aa958f696f6259ed72bb7`; lwSRP gitlink `23d9a8173b07503a0ee6e8528f922fceab4e67f0`.
- Delta under review: `50d492c1..42a0371a`. That is the `--no-ff` merge of dev `d51b373a`, the lwSRP re-pin and three commits. The full lane content is `d51b373a..42a0371a` (source base `db9aa8c9`).
- Read in this order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #665 body, the F4 assignment (6030279477), the acceptance additions (6009661573, 6030870481), the round-2 assignment (6033558691), the STOP (6034642528) and its ruling (6034653240). Then the authorities: docs/design/MAILBOX_SPLIT.md, `hdl/milan/mailbox/KL_mbx_evt.sv`, and the lwSRP Milan opt-in `23d9a817`. Then the diff and history, the author packets `review-evidence/665f4-r1/author/` (archive `fa19435a`) and `author-r2/` (archive `95f80a0a`), and the exact-head hosted check runs.
- The verdict, findings and ledger below were written (receipt `receipts/verdict_written_before_prior_reports.txt`) before any prior review report was opened. The disposition of prior findings follows the ledger.

## Findings

### R532-2-F1 MAJOR: Conformance, RTL, Robustness, Tests. The link is learned only from LINK records, so an interface can stay dead after re-initialisation or a cancelled level change

- **Where:** `sw/firmware/ctrl/srp/srp_mbx.c:558-566`: `on_event` is the only place `i->link` becomes true. `srp_mbx.c:578-584`: `poll` reads `mbx_link_up` only to detect loss. `i->link` gates receive (`:340`), transmit (`:637`) and the licence (`:609`).
- **Authority and evidence:**
  - Fabric posting rules:
    - MAILBOX_SPLIT.md:125-143: every event source is coalesced, a source "posts its state at posting time", and a LINK record is a level *change*.
    - `KL_mbx_evt.sv:112` posts only while `link_up_i != posted_up_r`; line 235 updates `posted_up_r`.
    - `mbx.c:69-80`: `mbx_open` resumes at the current `EVT_TAIL`.
  - So no record follows when the adapter is destroyed and re-initialised while the link is already up. srp/README.md: "Destroy before reinitializing an already initialized instance". The same holds after a core restart that leaves the mailbox running.
  - It also holds when a DOWN record is held (full ring) and the level returns before it posts. The lane's own `LinkLevelLossAndFirstDownEventAreFailClosed` models that hold. The adapter has already reset on the level and cleared `i->link`, but no UP record ever arrives.
  - Milan v1.2 5.5.2.7 requires Talker declarations for every output from start-up. R533-1-F2 requires recovery after link loss.
- **Executable evidence:** `probes/r532_probe.cpp`, run at the head at IF=1 and IF=2 (`receipts/probes-head-if{1,2}.log`).
  - `P1_ReinitWithLinkAlreadyUpStillDeclares` fails: `adapter.transmitted` stays 0 for 1.5 s and `ifs[0].link` stays false.
  - `P2_LevelLossThenLevelReturnWithoutRecordRecovers` fails: TX is frozen at 5 frames and a fresh Listener Ready cannot register.
  - Control (`receipts/control-fix.diff`): a copy that also raises `i->link` from the level, resetting first if `link_seen`, passes P1-P5 (`receipts/probes-fix-if{1,2}.log`). The same copy passes the lane's `srp_mbx.cpp` 41/41 at IF=1 and IF=2 (`receipts/control-fix-suite-if{1,2}.log`).
- **Impact:** the interface emits no Talker Advertise/Failed, Domain or MVRP declaration, registers no peer, and grants no licence. This lasts until some later physical flap. Round 1 consulted the level on every pass; round 2 removed the raise path.
- **Required outcome:** the operational link state is recovered from the level, or from a contract-guaranteed record, after re-initialisation and after a held-then-cancelled level change. The R533-1-F2 fencing (no stale Domain, no resurrected reservation) is kept. Named lane tests cover both cases, and the README lifecycle text states the rule.
- **Verification:** P1 and P2, or equivalents, pass at both interface counts. A planted defect that removes the level-raise path is caught by a named lane test.

### R532-2-F2 MAJOR: Docs, Tests. The required `docs-check` context fails at the exact head: the new `third_party/lwSRP` submodule is undocumented

- **Where:** `.gitmodules` adds `third_party/lwSRP`. `docs/reference/SUBMODULES.md`, `docs/diagrams/submodule_boundaries.drawio` and the role map in `docs/diagrams/submodule_boundaries.gen.py` do not name it.
- **Evidence:**
  - Hosted `docs-check` job 112715421406 on `42a0371a`, step "Verified submodule documentation gate": `submodule role map disagrees: missing=['third_party/lwSRP'], stale=[]` (rc 1).
  - Local reproduction at the head:
    - `submodule_boundaries.gen.py --check` and `--selftest` both rc 1.
    - `scripts/check_submodule_docs.py` rc 1 with 4 findings: missing path, role map, edge coverage, Draw.io node.
    - Receipts: `receipts/docs_diagrams_submodule_boundaries.gen.py_*.log/.rc` and `receipts/scripts_check_submodule_docs.py*.log/.rc`.
  - The gate predates the PR base (`25f543b9`). `docs-check` is one of the seven required contexts (CONTRIBUTING 2.1).
  - The author's round-2 gate table (`author-r2/ROUND2-GATES.md`) does not list this gate, and the PR body ticks "Documentation is updated where needed".
- **Impact:** the PR cannot meet the merge bar, and the imported-ownership map omits a new dependency and its licence boundary.
- **Required outcome:** lwSRP has its row, role and diagram node, generated artefacts are regenerated, and all four commands of that workflow step pass.
- **Verification:** the four commands rc 0 locally, and hosted `docs-check` succeeds on the new head.

### R532-2-F3 MINOR: Conformance, Robustness, Tests. A shared VID stays declared after its last binding leaves when a never-eligible binding is unbound last

- **Where:** `srp_mbx.c:309-311`. On unbind, `another_sink(..., false)` counts any bound sink on the VID, eligible or not. `vlan_requested` is set only for an eligible sink (`:474-480`). A remaining never-eligible binding therefore suppresses the withdrawal and never inherits the duty.
- **Authority:** srp/README.md "Shared bindings retain their Listener and VLAN until the final user leaves"; IEEE 802.1Q-2018 35.1.2.2 (membership declared for a stream's VLAN while it is needed); R533-1-F3 (reconcile shared declarations across bindings).
- **Evidence:**
  - `P3_SharedVidWithdrawnAfterBothUnbindsInEitherOrder` fails at the head (IF=1 and IF=2): no Lv for VID 7 is sent within 3 s after both unbinds.
  - The control copy, which hands the request to a remaining binding on that VID, passes. The opposite unbind order is already correct.
- **Impact:** a stale MVRP membership is held on the bridge port until link reset. Repeated binds with this ordering accumulate stale VIDs.
- **Required outcome:** a VID that no remaining binding requests is withdrawn in either unbind order, and a test covers both orders.
- **Verification:** P3 or an equivalent passes, and a planted defect restoring the head logic is caught.

### R532-2-F4 MINOR: Tests. The lifecycle and shared-binding tests miss three discriminable planted defects

- **Where:** `sw/firmware/ctrl/test/srp_mbx.cpp` (link lifecycle and shared-identity cases) and `srp_mutants.py`.
- **Evidence:** reviewer plants (`scripts/r532_plants.py`, `receipts/r532_plants.log`) ran against the lane's `srp_mbx.cpp` at IF=2. Nine of 17 were caught. Three of the escapes are discriminated by `probes/r532_gaps.cpp`, which passes at the head (`receipts/gaps-head.log`) and fails exactly on its plant:
  - L1, `reset_interface` keeps `domain_owed`. After a refused peer-Domain change, the old link's peer Domain is adopted after the restart. G1 fails (`receipts/gaps-L1-reset-keeps-owed-domain.log`). This is the R533-1-F2 "no stale Domain" outcome.
  - L3, reset keeps a sink's VLAN request/commit flags. On the new link Ready is declared without re-declaring the sink's VID. G2 fails (`receipts/gaps-L3-reset-keeps-sink-vlan.log`). Authority: Milan v1.2 4.3.2 and 802.1Q 35.1.2.2 ordering.
  - S2, shared reconciliation gates Ready on the first binding's VLAN commit rather than the matching binding's. G3 fails (`receipts/gaps-S2-handler-vlan-gates-all.log`). This is the README rule "Ready contributes only after its own VLAN membership commits" and R533-1-F3.
  - The other escapes are not claimed as gaps:
    - L2, L9 and L4: no discriminating observable was found (L2 and L9 pass G1-G4; L4 is redundant with the poll's loss check).
    - L7: duplicate stop only.
    - S1: an equivalent mutant.
- **Impact:** the tests that bank R533-1-F2/F3 cannot fail for these regressions.
- **Required outcome:** a named lane test fails for each of L1, L3 and S2, and each is added to `srp_mutants.py` with its observable.
- **Verification:** each plant is caught by the campaign at IF=2.

### RESIDUE

- **R532-2-R1:** `sw/firmware/ctrl/README.md:138-139`: "The local upstream topic stack must be published before a clean remote checkout can fetch this revision." This is stale: `23d9a817` is reachable from lwSRP `mark2-port` (PR #12); it was fetched for this review. Exact fix: "The pin is on lwSRP `mark2-port` (PR #12); a hosted checkout still needs read access to the lwSRP repository."
- **R532-2-R2:** PR #690 body, Status: "STOP: local validation incomplete ... No push or PR update was performed." This is stale after ruling 6034653240 and the push. Exact fix: "REVIEW READY under ruling 6034653240; `test_baremetal_profile_contract` is delegated to the manager's candidate builder bank." Re-tick "Documentation is updated where needed" only after F2.

### SUGGESTION

- **R532-2-S1:** the parent has no composition test that MVRP keeps Table 10-4 under `LWSRP_MILAN=1`. A planted lwSRP scope defect (Milan rule for every application) passes the lane suite (`receipts/control-lw-scope-suite.log`, rc 0). It is caught by `P5_MvrpLeaveInInAgesButMsrpLeaveIsImmediate` (`receipts/control-lw-scope-probes.log`) and upstream by lwSRP's `milan-option-scope` reversal. Adopting P5 would close the gap.

## What was verified clean (inside lenses that are unclean because of the findings above)

- **Milan v1.2 4.2.7.2.2 (R533-1-F1 / R532-1-F1):**
  - lwSRP `23d9a817` replaces only the IN/rLv cell (`src/core/mrp_mad.c:558-565`), selected by `.milan_rapid_leave = LWSRP_MILAN != 0` in `msrp.c` only. MVRP/MMRP templates leave it false.
  - `-DLWSRP_MILAN=1` is passed in the host arm, the RV32 arm and the image fixture (`srp_arms.py:59,89`, `ctrl_image.py:61`).
  - Planted lwSRP defects in copies, each run against the lane suite and my probes:
    - LV/rLv restart: caught by `LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline` and by my Talker-side `P4_TalkerLeaveInLvKeepsOriginalDeadline`.
    - Milan off: caught by `InListenerWithdrawalRevokesLicenceImmediately` and `InTalkerWithdrawalImmediatelyWithdrawsListener`.
    - MVRP scope: see S1.
  - Receipts: `receipts/control-lw-*.log`. P4 and P5 pass at the head.
  - D1 text and walk expectation (`srp_walk.cpp:47-49`, srp/README.md D1 row) agree with the rule.
  - The #608 case is kept: Listener and Talker Lv in LV hold the original 5 s deadline.
- **R532-1-F2 parts 1-2:**
  - `AdmissionStraddlesTheExactEthernetCeiling` checks both sides of the 75 % ceiling, at 22,698,667 and 22,698,666 bps for 17,024,000 bps on-wire. Ethernet overhead is 22 + 20 bytes and the minimum frame 68.
  - `ReadyToReadyFailedNeverGlitchesAnActiveLicence` uses the fixture's StrictMock.
  - Plants `tag-overhead-omitted`, `preamble-ifg-omitted`, `ninety-percent-ceiling` and `readyfailed-callback-stop` are all caught (`receipts/srp_campaign.log`).
- **R533-1-F4 (acceptance 6030870481):** `author-r2/ROUND2-SIZE.json` reports four F4 images: 53,856 / 65,104 / 68,592 / 94,576 bytes for 1x1 and 8x8 at IF=1 and IF=2. It also reports eight base images (dev and FC, 18,752-19,696 bytes). These are separate from routed resources and include an explicit 8 KiB stack reservation.
  - The measurement was taken at `181e3e1a`. `git diff --stat 181e3e1a..42a0371a` touches only `srp_mbx.cpp`, `srp_mutants.py` and one file mode, so production bytes are unchanged.
  - 8x8 (9 sources, 9 sinks) is the largest shipped shape (`srp_entity.py` over `configs/endstation_*.yaml`). 94,576 B is below the ~128 KB budget.
  - I did not reproduce the link; see the limits.
- **Dev merge `8b43aed6`:** `git show --remerge-diff` (`receipts/dev-merge-remerge-diff.txt`) shows both sides kept in all eight conflicted files:
  - `rtl-fast.yml` and `ci_events.py` keep `set -euo pipefail` and `--self-test --jobs 4`.
  - The ctrl README keeps dev's assertion row and RV32 prose plus F4's pinned lwsrp row.
  - `ctrl_build.py` keeps dev's flags and `__assert_fail`. F4's `RV32_CANDIDATES` is unreferenced at the head.
  - `ctrl_mutants.py` keeps dev's reentry arms and F4's jobs default.
  - `test_ctrl_firmware.py`, `fw_rv32.py` and `fw_rv32_selftest.py` take dev's text and assert controls.
  - The merge's duplicate `--jobs` option is removed in `181e3e1a`.
- **Gates run by this reviewer at the exact head** (receipts listed in MANIFEST):

  | Command | Result |
  |---|---|
  | `test_ctrl_firmware.py --require-rv32 --jobs 4` | rc 0, all arms incl. RV32 at both IF counts and all five shapes |
  | Lane SRP campaign | 58/58 caught, 0 escaped |
  | `fw_coverage.py --check` | rc 0, `srp_mbx.c` 424/424 lines, 406/406 branches |
  | `make -C tb/verilator/mbx -j16` with pinned Verilator 5.050 | rc 0; WB 316, AXI-Lite 361, model 316 checks; 5/5 mutants |
  | `gen_mailbox.py --check` | rc 0 |
  | `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py` | rc 0 |
  | `gen_toc.py --check` and `--verify-anchors` | rc 0 |
  | `check_em_dash.py --base d51b373a` | rc 0 |
  | `check_hygiene.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `ci_events.py --check` | rc 0 |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | lwSRP `src/core/mrp_mad.c:300-420,550-590`, `src/modules/msrp.c:397-404`, `src/include/shish_lan/{mrp,msrp}.h`; `srp_mbx.c` (all 672 lines); srp/README.md; issue directives 6030279477, 6033558691, 6030870481; `author-r2/ROUND2-SIZE.json`; probes P1-P5 | R532-2 | `42a0371affceb2a07a734449d706be01fa5abc9a` |
| RTL | UNCLEAN (F1) | No hdl/syn/tb change vs dev (`git diff --stat d51b373a..HEAD -- hdl syn tb` empty). Architecture: `srp_mbx.c` lifecycle FSM against MAILBOX_SPLIT.md:120-150, `KL_mbx_evt.sv:95-125,205-240`, `mbx.c:69-80,165-173` (`mbx_rx_mark/before` modulo-2^16 semantics); widths at `srp_mbx.c:94-100,394,627`; `make -C tb/verilator/mbx` | R532-2 | `42a0371affceb2a07a734449d706be01fa5abc9a` |
| Robustness | UNCLEAN (F1, F3) | `srp_mbx.c:283-319,465-652` (bind, reconcile, reset, event, poll); probes P1-P3, G1-G4; 17 reviewer plants | R532-2 | `42a0371affceb2a07a734449d706be01fa5abc9a` |
| Tests | UNCLEAN (F1, F2, F3, F4) | `srp_mbx.cpp` (41 cases), `srp_fixture.hpp`, `srp_walk.cpp`, `srp_mutants.py` (58 plants, rerun), lwSRP `tests/check_reversals.py` Milan cases; coverage ratchet rerun; firmware gate rerun; hosted check runs at the head | R532-2 | `42a0371affceb2a07a734449d706be01fa5abc9a` |
| Docs | UNCLEAN (F2) | srp/README.md, ctrl/README.md, docs/reference/SUBMODULES.md, docs/diagrams/submodule_boundaries.*, PR #690 body, author-r2 packet; docs gates rerun | R532-2 | `42a0371affceb2a07a734449d706be01fa5abc9a` |

## Prior public review findings at this head

These were read after the verdict and ledger above were written. Sources: R533-1 (PR #690 comment 6032452765) and R532-1 (comment 6032564515; archive `95f80a0a`, `reviews/R532-1/REPORT.md`).

| Prior finding | Disposition at `42a0371a` | Evidence |
|---|---|---|
| R533-1-F1 / R532-1-F1 BLOCKER (Milan 4.2.7.2.2) | RESOLVED | MSRP-only IN/rLv cell (lwSRP `mrp_mad.c:558-565`, `msrp.c:400`). The lane's Listener and Talker immediate-withdrawal tests catch the plants `delayed-in-listener` and `delayed-in-talker`. My lwSRP LV-restart plant is caught by the lane's 5 s deadline test and by P4. D1, README, PR body and walk are corrected. MVRP keeps Table 10-4 (P5; S1 notes the missing composition test). |
| R533-1-F2 MAJOR (link loss/recovery) | RESOLVED for both stated failure modes | `AdjacentLinkEdgesResetDomainAndAllPriorRegistrations` and `OldReceiveBacklogCannotRegisterAcrossLinkRestart` pass. Their plants (`short-link-interruption-ignored`, `backlogged-old-prefix-accepted`, `old-prefix-accepted`) are caught. The reworked lifecycle has new open findings R532-2-F1 (no recovery without an UP record) and R532-2-F4/L1 (stale-Domain path untested). |
| R533-1-F3 MAJOR (shared StreamID) | RESOLVED for the stated order-dependent withdrawal | `srp_mbx.c:488-521` reconciles across bindings. `SharedIdentityReconcilesBothBindingOrdersOnTheWire` covers both orders and both VID cases, and plant `shared-identity-overwritten` and my S3/S4 plants are caught. The related VLAN ownership is open as R532-2-F3, and the gating test gap as R532-2-F4/S2. |
| R533-1-F4 MAJOR (linked size) | RESOLVED on author evidence | `author-r2/ROUND2-SIZE.json`: linked ELF/map hashes and sections for both shapes and both interface counts, plus dev and FC bases, kept separate from routed resources. Not re-linked by this reviewer (limits). |
| R532-1-F2 MINOR, parts 1-2 (ceiling, Ready->ReadyFailed) | RESOLVED | Covered in "What was verified clean"; the plants are caught in my rerun of the 58-plant campaign. |
| R532-1-F2 MINOR, part 3 (Table 10-3 notes 4/5) | RESOLVED in the pinned dependency (static) | lwSRP `23d9a817` `tests/unit/integration_test.c:325-345` (`applicant_receive_conditions_follow_link_mode`) asserts VO vs AO for p2p rJoinIn! and QA vs AA for rIn!. `tests/check_reversals.py:74-77` reverses each guard. Static reading shows each reversal flips an asserted state. The cgreen run was not executed by this reviewer (limits). |
| R532-1-S1 (LeaveAll scope regression upstream) | RESOLVED | The pin carries `check_leaveall_scope` (`tests/unit/integration_test.c:71`). |
| R532-1-S2 (LV/rJoinIn! extra Join indication) | RETAINED as SUGGESTION | Carried to lwSRP PR #12 by the manager. The adapter does not depend on it. |
| R532-1-S3 (null participant after failed recreate) | RESOLVED | `srp_mbx.c:588-596,631-634`. `RecreateAllocationFailureIsCountedAndRetried`; plants `reset-skips-recreate` and `failed-interface-starves-peer` are caught. |
| R532-1-R1 (TICK wording) | RESOLVED | srp/README.md:45-46. |
| R532-1-R2 (PR body omits linked size) | RESOLVED | The PR body "Round 2" section reports the linked composition. |

## Real limits

- **Not run by me, by assignment:** the builder bank, including `test_baremetal_profile_contract`, which is delegated to the manager's candidate bank under ruling 6034653240. Also not run: the full parent, processor, gPTP and Yosys banks, Docker/act and hardware. Physical calibration is NOT RUN. Field skips are not hardware proof.
- **lwSRP's own cgreen/behave suites and `check_reversals.py`** were not executed by this reviewer. The only cgreen on this host is in the executor's lane scratch, which I may not use. A standalone replay of the note 4/5 test was not permitted in this session. lwSRP behaviour is instead judged by static review, by composition probes, and by planted lwSRP defects run in copies through the parent arm, with the pin check bypassed only for those copies (`scripts/srp_probe.py --no-pin`).
- **The linked size measurement was not re-linked.** The runtime sources are externally provisioned, and only the author's JSON with hashes was examined.
- **The probes run on the host model** (`mbx_model`). P2 forces the level directly to model a DOWN record held by a full ring, as the lane's own `LinkLevelLossAndFirstDownEventAreFailClosed` does.
- **The Milan v1.2 4.2.7.2.2 wording** is taken from the manager's directive 6033558691; I have no direct access to the specification text.
- **Hosted contexts at `42a0371a`** (read-only inspection):
  - Failed:
    - `docs-check` fails (R532-2-F2).
    - `firmware-unit` fails only at "Fetch RTL dependencies" because the private lwSRP clone is refused.
    - `rtl-fast` fails as their aggregate.
  - Passed: `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, Yosys shards 0-3 and Verilator shard 3.
  - Still in progress when inspected: `elaborate` and Verilator shards 0, 1, 2 and 4.
  - Skipped: `Physical gPTP (nightly and manual)`.
  - The manager owns hosted and act acceptance.

## Pending manager duties

- Carry R532-2-F1..F4 and R532-2-R1/R2 to the executor. The RESIDUE items go to the residue checklist.
- Run the candidate builder bank, including `test_baremetal_profile_contract`, and the current-dev candidate gates at the merge turn.
- Make lwSRP fetchable for hosted CI, review and merge lwSRP PR #12, and move the pin (a later delta). Carry R532-1-S2 to PR #12. The PR body cites a local branch `f4-applicant-notes` (`495520f5`) that is not publicly fetchable; publish it or drop the reference.
- Re-run hosted `docs-check` and `firmware-unit` on the next head.

R532-2 FINISHED
