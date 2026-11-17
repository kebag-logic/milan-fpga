[R853] NEGATIVE - exact head 6ceed75374210935cff4f10d014b9a5ef137615e

# R853-1: internal cleared-context review of PR #934 (issue #665), the sync of dev 6b66f66d into dev-soft-core

- Head `6ceed75374210935cff4f10d014b9a5ef137615e`, tree `340fd990b4a7873d00d173ba3e357d920a8d7437`. Base dev-soft-core `70f4056f`, source base `659d7687`.
- Verdict: **NEGATIVE**. There are two open MINOR findings, F1 and F2, in round 3's new grading (`tb/verilator/ctrl_service_budget/mrpdu_grade.py`). Both are reproduced by a disposable probe.
- Everything else in the composition holds at this head:
  - both merges;
  - the pins;
  - the semantic-conflict commits and their plants;
  - the deleted owed rows;
  - the #847/#852/#893 ledger;
  - clockAccuracy 0x22 and the #840 identity on the split images;
  - the self-test counts;
  - the image and route figures.
- Lenses applied: Conformance, RTL, Robustness, Tests and Docs, all five, each with its artifacts below. RTL is covered clean. The other four are unclean through F1 and F2.
- The verdict and ledger were written before any prior review finding was read.

## Scope reconstructed from public state

- **Ruling #665 issuecomment-6899740728, item 3.** A sync of dev into dev-soft-core must come before the flip's gating run. It must carry the #843 gPTP fixes (clockAccuracy per board, 802.1AS-2011 8.6.2.3; 10.3.9.1; 11.4.1; Milan v1.2 4.2.6.2.6) and the #840 identity. It keeps a ledger naming a split counterpart, or "not applicable", for each of #847, #852 and #893.
- **Ruling issuecomment-6907491626.** The 8x8/1if LeaveAll row is an open miss and cannot be carried. It must be graded at every LeaveAll phase. #840's 1000BASE-T-only advertisement goes to #919.
- **Ruling issuecomment-6930885185.**
  - Q1: THE TRANSMIT's MRPDU row (FR_NFR.md 3.4.1) is measured from the participant's transmit opportunity (IEEE 802.1Q-2018 10.7.4.1), with its bound unchanged. The harness adds a conformance check that a LeaveAll goes out at the first transmit opportunity after expiry, with a planted defect that skips one.
  - Q2: the paced 305/300 record goes to #898.
  - Q3: the #818 floor is +0.030 ns setup and 0 ns hold, on the best of three directives.
- **REVIEW READY:** #665 issuecomment-6932432594. **PR body:** #934.
- **Known, not findings:** #898 (paced SET_CONFIGURATION 305 against 300), #914 (8x8/1if `STATED` lines), #929 (twin), #916 (srptx), #919 (1000BASE-T-only on the split), and the host interruptions of 2026-11-16.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs

- **Where:**
  - `tb/verilator/ctrl_service_budget/mrpdu_grade.py:237-259` (`leave_alls`);
  - `tb/verilator/ctrl_service_budget/README.md`, the "Every LeaveAll timer's run-out" bullet;
  - `docs/reference/FR_NFR.md:388`.
- **Title:** a skipped LeaveAll escapes when another participant's LeaveAll timer runs out inside the skipped participant's join interval.
- **Authority and evidence:**
  - Ruling issuecomment-6930885185 Q1 asks for "a conformance check that a LeaveAll goes out at the first transmit opportunity after expiry, with a planted defect that skips one".
  - The README and the PR body state that "A skipped, late or absent LeaveAll ... fails the run".
  - The log's `ENTRY ... on_la_timer` line is PC-based (`tb/verilator/ctrl_service_budget/sim_main.cpp:336`) and names no participant. lwSRP keeps one LeaveAll timer per application and port (`third_party/lwSRP/src/core/mrp_mad.c:857-862`).
  - So `leave_alls` gives each run-out to the participant whose next unanswered LeaveAll comes first (`sent, who = min(found)`, line 253). It then checks only that participant's first MRPDU after the run-out.
- **Probe:** `scripts/leaveall_attribution_probe.py` builds the log with the self-test's own helpers (`selftest.synthetic`, `selftest.tx_record`, `selftest_leaveall.mrpdu`); receipt `receipts/leaveall_attribution_probe.txt`.
  - Case B: MSRP's LeaveAll timer runs out at 1,050 ms. At its first opportunity, 1,180/1,181 ms, MSRP sends an MRPDU without the LeaveAll, and it sends the LeaveAll at 1,371 ms. MVRP's own LeaveAll timer runs out at 1,185 ms, and MVRP sends its LeaveAll at its opportunity, 1,191 ms.
  - Result: both run-outs grade `sent` (the 1,050 ms run-out is credited to MVRP's 1,191 ms LeaveAll, the 1,185 ms run-out to MSRP's 1,371 ms one). `leave_all.failing` is `[]`, and the run passes.
  - Control A (the self-test's own skip, MSRP alone) still grades `skipped` and fails.
- **Impact:**
  - The window for the escape is one JoinTime (about 190 ms) per LeaveAll, between two participants of one interface. With 10 to 15 s LeaveAll draws this is rare but reachable, and more so at two interfaces.
  - A firmware regression that drops a LeaveAll at a transmit opportunity can then pass THE TRANSMIT's new conformance check at some LeaveAll phases.
  - The ruling's phase-spread argument relies on the check being phase-independent, and it is not.
  - Nothing measured at this head is shown wrong. The published first draws per phase (`leaveall-spread-after.md`) are 400 ms or more apart between MSRP and MVRP.
- **Required outcome:**
  - Each LeaveAll run-out is matched to its own participant, for example by the log recording the callback's application and port.
  - Or the check refuses, or flags, a run whose attribution is ambiguous, so that a skipped LeaveAll cannot be credited to another participant's run-out.
  - Or the README and FR_NFR 3.4.1 state the limit, with an explicit ruling that accepts it.
- **Verification:** the probe's case B fails the run, with "(LeaveAll past its first transmit opportunity)" naming the MSRP participant. A self-test arm and a mutant hold the two-participant case.

### F2 - MINOR - Conformance, Robustness, Tests

- **Where:** `tb/verilator/ctrl_service_budget/mrpdu_grade.py:228-229` (`resolve`, a run-out whose first build sends nothing).
- **Title:** an empty build's lateness restarts at any participant's join-timer callback, so a build 60 ms after its run-out passes.
- **Authority and evidence:**
  - Q1 times the row "from the participant's transmit opportunity".
  - The manager's check (4) asks that the change "cannot hide a real CPU delay".
  - For an empty build, `resolve` takes `joined = [c for c, name in log.entries if name == 'on_join_timer' and entry < c <= run[0]]` and calls the build late only past `max([entry] + joined) + bound`.
  - These are CPU-time callback entries of any participant on any interface. They are not that participant's opportunity, which `opportunity()` derives from posted TICKs.
  - The README discloses "the last join timer's run-out between the two", but not that the run-out may be another participant's.
- **Probe:** `receipts/leaveall_attribution_probe.txt`, cases C0 and C.
  - Case C0: a periodic run-out at 1,300 ms, whose participant's join timer has long run out, with its first, empty build at 1,360 ms. It grades `late` (59.979 ms) and fails, as it did before this commit.
  - Case C: the same log plus one `on_join_timer` callback at 1,330 ms, from a participant with no running timer of its own here. It grades `empty`, and the run passes.
- **Impact:**
  - Starvation of up to the whole window before an unrelated join callback is not counted against a build that resolves a timer.
  - The check is weaker than the one it replaces, and its anchor is not the participant's opportunity the ruling names.
  - A frame late after its opportunity still fails (`resolve` line 226 uses the frame's own participants and the minimum). So the weakness is limited to builds that send nothing.
- **Required outcome:**
  - The empty-build anchor is a participant's transmit opportunity computed as `opportunity()` computes it, from posted TICKs. Where the participant is unknown, use the latest over the interface's participants.
  - It is not the CPU-time callback of any join timer.
  - Or the leniency is ruled acceptable and stated as such in the README.
- **Verification:** the probe's case C grades `late` while C0 still does, and a self-test arm holds it.

### Comment rule and residue

No RESIDUE. The comment rule was checked over the added source lines of `a563a83d`, `dfcd8eed`, `d8c8c4b7`, `1facd42e`, `3c94c76c`, `9715a30a` and `6ceed753`, and the merges' source resolutions:
- No lane label, review round, reviewer ID or issue-comment ID appears in a new source comment.
- "control lane" names the datapath's TX lane.
- "#665's ruling of 2026-11-16, Q1" cites an issue and a date, as existing comments do.

## Per-lens results, with evidence

- **[R853] PASS RTL** - `hdl/milan/milan_datapath.sv:10180-10220` (the split `KL_ctrl_split` instance) against `:9002-9017` (the #839 gate) and `:9915-9917` (the all-fabric wrapper), at `6ceed753`.
  - The split lane drives `pp_txs_tvalid_w` and reads `pp_txs_tready_w`, as the wrapper does. The gate alone drives `pp_tx_tvalid_w`.
  - At `62625941` the split instance drove `pp_tx_tvalid_w` beside the gate's assign and left `pp_txs_tvalid_w` undriven, which is why `a563a83d` is necessary.
  - The split build (`make split`, pinned Verilator 5.050 rev v5.050, `-Wall`) has no UNDRIVEN, MULTIDRIVEN or UNUSED warning on the changed lines (`receipts/split.log`).
  - `git show --remerge-diff` of both merges (`receipts/remerge_*.diff`) shows that no HDL file was resolved by hand, and that no non-conflicted file differs from git's automatic merge.
  - `hdl/ieee8021as` and the `gptp-processor` gitlink equal dev `6b66f66d`.
  - The AX7101 (GMII) gPTP launch takes the RTL defaults in both placements (`sw/litex/milan_soc.py:1495-1497`).
  - `KL_ctrl_split.sv:176-212` already counts the FIFO's oversize drops as dev's #862 now does in `KL_pp_shadow`.
  - The split firmware writes `MAC_ADDR_LO`/`HI` (0x108/0x10C, the addresses `mac_addr_seq` decodes) in `sw/firmware/ctrl/plat/ctrl_plat_csr.c:38-39`, before any transmitter enable.

Other lenses' clean parts, which do not clear them while F1 and F2 are open:

- **Conformance.**
  - Every conflict hunk keeps both sides: `receipts/remerge_62625941.diff` (ten files, thirteen hunks) and `receipts/remerge_10b2fe21.diff` (two docs files).
  - FR_NFR NFR-SCOUT-01 and -03 carry both sides' word changes against the merge base `1f29f189`, and -02 is dev's, where this line had not changed it (`receipts/fr_nfr_scout_3way.txt`).
  - Pins: gptp-processor `1616fc8f` and protocol-processor `801ef228` follow dev, each a fast-forward of `135afd04` and `a9e84b66`. tsn-c-stack stays at `715589c1`, which descends from `70936b77`. No other gitlink moved, and `10b2fe21` moves none.
  - clockAccuracy 0x22 and the #840 MAC reach the split image's gPTP engine ROM. The builder's `gptp_ucode.hex` for the split 1x1 config (`--placement split`) equals the generator's image for `--clock-accuracy 0x22 --mac 0x024b4c4b4c01`, and differs from 0xFE and from another MAC (`receipts/gptp_rom_identity_split_1x1.txt`, script `scripts/gptp_rom_identity.py`). The AEM overlay carries `clock_accuracy` 34 (0x22).
  - The split platform policy carries entity ID `024B4CFF:FE4B4C01` and station MAC `02:4B:4C:4B:4C:01` at both AX7101 configs (`receipts/split_policy_identity.txt`). Both configs equal dev's file for file.
  - The builder run left no generated file different from the tracked one.
  - Processor `801ef228` fixes the deleted rows' defects (`receipts/processor_fixes_857_858_860.diff`):
    - #858 in `db131cb` (KL_adp_engine `last_avail_index_o` into KL_aecp_engine E_RDESCENT);
    - #857 and #860 in `f247533` and `b655100` (KL_srp_domain/KL_srp_vlan Table 10-3 Applicants, the VID Registrar and MVRP LeaveAll).
  - `make twin` at this head reports exactly one finding, #929's known `split-talker-failed` (`receipts/twin.log`). The deleted rows' defects do not reappear unowned.
  - The ledger's split counterparts exist at the cited places:
    - `srp_mbx.c:618, :829, :997, :1045`;
    - lwSRP `mrp_mad.c:149, :779, :1278, :1351, :1410`;
    - `ctrl_app_aecp.c:105-118`;
    - their tests and mutants, `HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep` / `binding-change-not-copied` and `App.EntityReadSeesTheLastAdvertisedIndex`.
  - The `leave_all()` parser follows 802.1Q-2018 10.8.2: LeaveAllEvent 1 in the VectorHeader's top three bits, MSRP's AttributeListLength, ThreePackedEvents, and the Listener FourPackedEvents.
- **Robustness:**
  - The split leg's `[TX]` hold is checked before the MAC write and after its low half alone (`tb/verilator/milan_dp/sim_split.cpp:537-551`).
  - `csr_wr` fails on an unanswered write.
  - For frames, `opportunity()` anchors at posted TICKs and `begin()`/`resolve()` take the minimum over a commit's participants. So a frame late after its participant's opportunity still fails.
- **Tests:**
  - `make split`: 84 checks, 0 failures.
  - The two new plants ("the control lane past the station MAC transmit gate", "the station MAC transmit gate opened by one half") are each caught by its named check after a clean control (`receipts/sm_gate_bypass.log`, `receipts/sm_gate_half.log`).
  - Harness self-test: 871 PASS, `self-test: 0 failures`, 254 of 254 mutants caught, the eight new ones each by its named check, rc 0 (`receipts/harness_selftest.log`).
  - `pp_shadow`: 317 checks, 0 failures, rc 0. `bootsa`: 67 checks, 0 failures, rc 0. Both exercise `9715a30a`'s `g_af_pp` paths.
- **Docs:**
  - `docs_inventory.py --check` is OK (`receipts/docs_inventory_check.txt`).
  - SPLIT_CONTROL_MEMORY section 5 (line 387) says 32 to 40 B over `70f4056f`, and 130,224 B in 131,072 (848 spare) at 8x8/1if and 131,784 in 133,120 at 60.5. The author's image receipts (`images-merge-10b2fe21.txt` against `images-dsc-70f4056f.txt`) give +32 or +40 at all eight points.
  - Nothing after `10b2fe21` touches firmware or RTL.
  - The MARK_II_AREA_PLAN #810/T_svc restatement is correct for this line.
  - FR_NFR 3.4.1 (line 388) and the harness README describe the transmit-opportunity anchor as the code implements it for frames, but see F1.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | both remerge diffs; FR_NFR NFR-SCOUT-01..03 three-way; gitlinks at 1f29f189/659d7687/6b66f66d/62625941/70f4056f/10b2fe21/HEAD; split gPTP ROM and policy; processor `db131cb`, `f247533`, `b655100`; ledger counterparts; `mrpdu_grade.py` against 802.1Q-2018 10.7.4.1 and 10.8.2 | R853-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| RTL | CLEAN | `milan_datapath.sv:9002-9017, 9915-9917, 10180-10220`; `KL_ctrl_split.sv:176-212`; `ctrl_plat_csr.c:28-46`; `milan_soc.py:1495-1497`; split build log; remerge diffs (no HDL hunk) | R853-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| Robustness | UNCLEAN (F1, F2) | `mrpdu_grade.py` `opportunity`, `begin`, `resolve`, `leave_alls`, `leave_all`; `sim_split.cpp` `csr_wr`/`check_tx`; probe receipts | R853-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| Tests | UNCLEAN (F1, F2) | `selftest_leaveall.py`, `selftest_mutants.py` (eight new arms); `split_mutants.py` two new arms; runs of split, the two new split arms, harness self-test, pp_shadow, bootsa, twin | R853-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| Docs | UNCLEAN (F1) | `FR_NFR.md:388`; `ctrl_service_budget/README.md`; `SPLIT_CONTROL_MEMORY.md:387`; `MARK_II_AREA_PLAN.md`; `milan_dp/README.md`; `DOCUMENTATION_AUDIT.md` (inventory check); PR body | R853-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |

## Prior public review findings

- **PR #934.** No review finding was published before this round. The only other review on the PR is a concurrent independent review of the same head (started 2026-11-16 23:27), which this round did not read.
- **Issue #665, from 2026-11-14.** The thread carries manager rulings only (issuecomment-6907491626 and -6930885185), and no reviewer-led finding on this sync.
- So there is nothing to resolve or retain.

## Real limits

- **Mutants.** I ran only the two new #839 split arms of `split_mutants.py`, each with its control. The other 26 arms rest on the author's 28 of 28.
- **Not run by me:**
  - the 65-suite sweep;
  - the four workflows;
  - the CPU budget legs at 1x1/1if and 8x8/1if;
  - the eleven-phase regrade;
  - #901's valid-destinations leg;
  - the routes;
  - the release-export comparison;
  - `twin-plants` and `srptx`.
  For these I read the author's published receipts (archive `2b4066ca`):
  - sweep shards 0 to 3 at `4cb7d7ab` (15+17+17+16 = 65 suites);
  - the re-runs of `pp_shadow`, `milan_dp` and `milan_dp_gm_steps` at `9715a30a`;
  - `floor-818.md` (split 1x1/1if best +0.196/+0.036, split 8x8/1if AltSpreadLogic_high +0.140/+0.036, release +0.209/+0.016);
  - `leaveall-spread-after.md`;
  - `release-export-round1-vs-merge.txt`;
  - the docs tables `verify-docs-at-6ceed753.md` and `verify-wf-at-9715a30a.md`.
  The workflow tally of 154 steps was not recounted.
- **Images.** The 8x8 split image's gPTP ROM and AEM were not built separately. Its config and builder path are the 1x1 config's, and its policy header was checked.
- **Hardware.** Physical calibration was not run, and field skips are not hardware proof. This review is simulation and static evidence only.
- **No manager bank.** No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus this round's own runs above.
- **Hosted runs.** Hosted runs were not inspected.

## Pending manager duties

- Carry F1 and F2 to the lane. Each needs a fix, or an explicit ruling that accepts the limit and a docs statement of it, then re-review at the new head.
- Hosted and act acceptance at the exact head.
- The current-dev merge candidate (builder and native banks) at the merge turn, against live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`.
- The regrade on #898's merge (Q2).
- The 8x8/1if row on #914's composed head.

## Restoration

- The review clone was not edited. Every build, builder run and probe ran in disposable copies under `scratch/`.
- After the probes the clone was verified (`receipts/restore_verify.txt`):
  - HEAD `6ceed753` and tree `340fd990`, equal to the index's tree;
  - no tracked, untracked or ignored change;
  - 1,899 tracked blobs re-hashed with 0 mismatches, and their modes matched;
  - the six gitlinks as stated, with clean submodules.

R853-1 FINISHED
