[R552] NEGATIVE - exact head 96d3b78384f34a630d6056ebd8fa5e30f6836650

# R552-1: internal independent review of processor PR #171 (Closes #168)

- Subject: Mister-M-alt/protocol-processor-control-plane-avb-milan PR #171, branch `pp168-acmp-fields`
- Exact head `96d3b78384f34a630d6056ebd8fa5e30f6836650`, tree `37ee429d6fb58f8c3f93d735131e4821f5240004`. Both are verified in the review clone, which is byte-exact after all probes: 582 tracked blobs and modes match, the index equals HEAD, there are no gitlinks in HEAD and none are expected, and nothing is untracked (`receipts/verify-tree.txt`).
- Source base `ed340b9b85258194247334b85e62cf9c23d4d051`; merged main `09e357fb4bf3d35c8a9deba9a787e13f74d08c83` (PR target and area baseline)
- Review start: PR #171 comment 6085210630. Role: internal reviewer, cleared context, own clone.

## Verdict summary

The six RTL corrections are right against their clauses, every new check has a planted defect that its named witness kills, and the area result reproduces exactly. The OOC 1x1 synthesis gives +29 LUT / +14 FF against 09e357fb, inside the +40 / +40 ceiling. No top-level port, parameter or register-map change was made. The merge of main is byte-identical to a clean three-way merge. All 33 suites, lint, `make check`, the matrix check and the Yosys flow return 0 at the head. The three campaigns I re-ran (ACMP, GSI and talker retry) also return 0 at the head.

The verdict is NEGATIVE because the change makes four sets of statements in the normative architecture and compliance documents false. None of them is updated or tracked by the PR (R552-F1 to R552-F4, all MINOR). They describe:

- DISCONNECT_TX status;
- the A5/A12 status rule;
- the F07.6 sink-record layout and its new private overlay;
- which side owns GET_STREAM_INFO selector 6.

These are clause, behaviour, layout and interface-contract claims, and fixing F07.6 also means regenerating a rendered figure, so they are not RESIDUE. The original assignment scoped edits to `hdl/acmp` and its tests. Closing these findings therefore needs a manager decision: authorise the document edits in this PR, or record a tracked follow-up that lists every location.

## Findings

### R552-F1 - MINOR - Docs, Conformance - DISCONNECT_TX still documented and claimed as "always SUCCESS"
- Where:
  - `docs/architecture/05_acmp_engine.md:13` (scope table);
  - `docs/architecture/05_acmp_engine.md:387` (figure F05.11, node r5 "SUCCESS no-op ... nothing changes");
  - `docs/architecture/01_overview.md:139` (delta Δ4 in F01.4, "DISCONNECT_TX → SUCCESS no-op");
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:96` and `:391` (REQ-ACMP-007 "DISCONNECT_TX → SUCCESS no-op");
  - `docs/guides/operator.md:52` ("always `SUCCESS`, and it changes nothing").
- Evidence: the head answers TALKER_UNKNOWN_ID for an invalid source (`hdl/acmp/KL_acmp_talker.sv:1302-1307`). This is the issue's TD1 ruling (Milan v1.2 5.5.4.2 step 1, Table 5.44 govern over the 5.5.2.7 overview). The suite checks it (`tb/acmp_talker/sim_main.cpp:1187-1194`), and three planted controls kill it (`receipts/acmp_mutants-head/results.json`). `docs/README.md` §2 says Milan/IEEE deltas live only in F01.4, and the compliance matrix is the repository's conformance claim. `docs/guides/hdl-engineer.md` §7 says expectations are built from the documents.
- Impact: the compliance matrix and the delta table now claim a behaviour the RTL no longer has. A verifier or integrator who builds expectations from F05.11 or Δ4 expects SUCCESS for an invalid source. The author's published handoff calls this prose "an out-of-scope documentation follow-up", but the PR body and the issue record no follow-up.
- Required outcome: correct these locations to "TALKER_UNKNOWN_ID for an invalid talker_unique_id, otherwise SUCCESS with no state change", citing Milan 5.5.4.2 step 1 and Table 5.44. If the manager keeps the edit out of this PR's scope, a tracked follow-up linked from the PR must name every location before merge.
- Verification: `grep -n 'DISCONNECT_TX' docs/architecture/05_acmp_engine.md docs/architecture/01_overview.md docs/00_MILAN_COMPLIANCE_REVIEW.md docs/guides/operator.md` shows no unconditional-SUCCESS claim, and `make check` returns 0.

### R552-F2 - MINOR - Docs - Listener action legend still clears acmpsta unconditionally in A5 and A12
- Where: `docs/architecture/05_acmp_engine.md:283` (A5 "... pbsta←ACTIVE, acmpsta←0") and `:290` (A12 "arm `T-ACMP-DELAY`; pbsta←ACTIVE, acmpsta←0").
- Evidence: the head keeps acmpsta on T-ACMP-RETRY in A12 (`hdl/acmp/KL_pp_acmp_listener.sv:1273`, Milan 5.5.3.5.30 step 2) and on T-ACMP-DELAY in A5 (`:1345`, Milan 5.5.3.5.10). The listener's independent C++ model was changed to match (`tb/acmp_listener/sim_main.cpp:457-482`). The action legend is the normative source that the ROM generator and that model are transcribed from (`hdl/acmp/rom/gen_ltn_rom.py` header).
- Impact: the normative legend and the tested behaviour now disagree on LD2, the issue's own item. The next author who transcribes the legend reintroduces the defect.
- Required outcome: state the conditions in the A5 and A12 legend rows (acmpsta←0 except on T-ACMP-DELAY for A5 and on T-ACMP-RETRY for A12), citing the two clauses. Otherwise, include these rows in the tracked follow-up of R552-F1.
- Verification: read the two legend rows; `make check` returns 0.

### R552-F3 - MINOR - Docs - F07.6 sink-record layout is stale, and the private controller overlay is undocumented
- Where: `docs/architecture/07_memory_maps.md:495-496` (F07.6 WaveDrom source "settled vlan_id" 12 bits plus a 4-bit "rsv", and its rendered `docs/diagrams/wavedrom/fig-07-sinkrec.svg`), and `docs/architecture/05_acmp_engine.md:131` (05 §5 "`stream_vlan_id` (12)").
- Evidence: `hdl/acmp/pp_acmp_pkg.sv:152` now declares `settled_vlan` as 16 bits [319:304] and removes `rsv1`. While a probe is outstanding, the listener also reuses the private `settled_stream_id` word to hold the sent probe's controller: it is written in A5 (`KL_pp_acmp_listener.sv:1340`), read by the guard in PRB_W_RESP/PRB_W_RESP2 (`:527-538`) and by the transmitted controller octets (`:729-741`). It is masked to zero only on the published write view (`:789-797`), and A10 deliberately no longer clears it (`:1258-1259`). `docs/README.md` §2: "Record/memory layouts only in 07".
- Impact: the single home of the record layout no longer matches the RTL. The field's dual lifetime is a non-obvious invariant that exists only in code comments and `tb/acmp_listener/README.md`. My probe `published_mask_removed` shows that removing the mask leaks a previous binding's controller EID into the published record in UNBOUND, PRB_W_AVAIL and PRB_W_DELAY: for example, `F05.3 BIND_SAME x UNB: settled got 0099aabbccddeeff ... want 0` (`receipts/r552-probes/results.json`). The listener suite catches that, but a future editor who reads only 05/07 would not know the mask is load-bearing.
- Required outcome: update F07.6 to 16-bit `settled vlan_id` with no reserved nibble, and re-render the figure with `make wavedrom`. Update 05 §5 to 16 bits. Add one sentence in 05 §5 or 07 §4 on the overlay: the private word holds the sent probe controller in PRB_W_RESP/RESP2, and the published view reads zero until settlement. Or include all of this in the tracked follow-up.
- Verification: `make check` returns 0 (wavedrom-check freshness), and the F07.6 source matches `acmp_rec_t`.

### R552-F4 - MINOR - Docs - GET_STREAM_INFO selector 6 ownership changed without updating the interface contract
- Where:
  - `docs/architecture/06_aecp_engine.md:331-337` ("For STREAM_INPUT, the top serves selectors 5 and 7 internally ... Other input words ... remain integrator-owned");
  - `docs/architecture/06_aecp_engine.md:419-423` (F06.13 reads paragraph names selectors 4, 5 and 7 only);
  - `docs/architecture/02_interfaces.md:412` ("an input's selectors 5 and 7 and selector 4's failure-code byte are served inside the processor");
  - `docs/guides/integrator.md:569-574` ("Keep serving the other selectors").
- Evidence: `hdl/top/protocol_processor_top.sv:3535-3539` now replaces the upper 16 bits (stream_vlan_id) of kind-0 selector 6 for every Stream Input. The value is `bound_vlan_r` when PROBING_COMPLETED, otherwise zero, and the integrator's `gsi_data_i[63:48]` is discarded. The manager's ruling 6050554601 authorises the behaviour ("GET_RX_STATE and GET_STREAM_INFO then report the received value"). The test expectations were changed to match (`tb/pp_top/sim_main.cpp:5314`, `tb/pp_top/gsi_internal.hpp:93`).
- Impact: an integrator reading 02, 06 or the integrator guide still believes its selector-6 VLAN half is used. The F06.13 lineage and the integrator guide are the documents that tell the integrator which words are its own.
- Required outcome: name selector 6's VLAN half as served internally for inputs (settled value, otherwise zero; flags_ex half still integrator-owned) in 06 §6.2, the F06.13 reads paragraph, 02 §4.4 and the integrator guide. Or include it in the tracked follow-up.
- Verification: read the four locations; `make check` returns 0.

### RESIDUE
None.

### Suggestions (do not affect the verdict)
- R552-S1 (RTL, area): the A12 status clear (`KL_pp_acmp_listener.sv:1273`) is functionally dead for every event other than TMR_RETRY. A12 otherwise runs on TK_DISC from PRB_W_AVAIL and on the conditional cells from SETTLED_*, and acmpsta is already zero in all of them. My probe `a12_status_never_cleared` survives the listener suite as an equivalent mutant. Dropping the clear, or recording why it stays, may save area.
- R552-S2 (Tests): the SRP service VID slice `lstn_act_settle_vlan_w[11:0]` (`protocol_processor_top.sv:2714`) is graded only with VLAN values below 0x100. My probe `srp_vid_from_upper_bits`, which feeds `{[15:12],[7:0]}`, survives the full pp_top run. A settle with VID bits 8-11 set, checked at the SRP matcher, would grade the slice. A natural shift mutant would likely still be caught by the existing VID-2 matching.
- R552-S3 (Tests): TD1's checks use only out-of-range source IDs (8, 0xFFFF). An in-range but unconfigured source (`cfg_src_en_i` clear, "source exists in the current configuration") is also TALKER_UNKNOWN_ID through the same `uid_valid_w`, and it is not exercised for DISCONNECT_TX.
- R552-S4 (RTL): post-synthesis OOC TNS moves from -2063 ns / 2821 endpoints to -3601 ns / 4008 endpoints. WNS is unchanged at -5.416 ns on the same pre-existing path. The author's single-item runs show the same swing for unrelated items: LD1 alone, a pure deletion, gives -5592 ns / 4129, and VLAN alone gives -3747 ns / 3943 (`receipts/author-ooc-timing-summary.txt`). This is synthesis variance, not an attributable regression. Routed timing in the parent image remains the authority.

## Judgement against the review focus

### (1) Clause items, each with a planted mutant
| Item | Head location | Clause | Behaviour verified | Check / planted defect (all KILLED at head) |
|---|---|---|---|---|
| LD1 | `KL_pp_acmp_listener.sv:680-684` | Milan v1.2 Table 5.36 | successful UNBIND_RX_RESPONSE has zero talker_entity_id/unique_id; error forms unchanged | `unbind_talker_echo` (9 failures) |
| LD2 | `:1273` (A12), `:1345` (A5) | Milan 5.5.3.5.30 step 2; 5.5.3.5.10 | status kept through discovered retry and the following delay expiry; BIND_NEW still clears (my probe `a5_status_never_cleared` is killed by `F05.3 BIND_NEW x PWT`) | `retry_status_cleared`, `retry_probe_status_cleared` (listener and pp_top) |
| LD3 | `pp_acmp_pkg.sv:123` | IEEE 1722.1-2021 Table 8-3 (13 TALKER_MISBEHAVING, 16 CONTROLLER_NOT_AUTHORIZED) | both lock refusals answer 16 and leave the binding untouched | `lock_status_13`, `lock_gate_bypassed` |
| TD1 | `KL_acmp_talker.sv:1302-1307` | Milan 5.5.4.2 step 1, Table 5.44 (ruling: governs over 5.5.2.7) | invalid source returns TALKER_UNKNOWN_ID (2) with no source action; valid source keeps SUCCESS | `disconnect_invalid_success`, `disconnect_changes_gate`, `disconnect_not_accepted` |
| 16-bit VLAN | listener `:187`, `:698`, `:808`, `:1300`; pkg `:152`; top `:1021`, `:1042`, `:1901`, `:1921`, `:3535-3539` | Milan 5.3.8.9, Table 5.38, 5.4.2.10; ruling 6050554601 | settle action, record, GET_RX_STATE and selector-6 GSI carry all 16 bits; `acmp_bound_vlan_o` is bits [11:0] (port width unchanged); SRP service gets [11:0] | `settled_vlan_truncated` (x2), `settlement_vlan_truncated`, `stored_vlan_truncated`, `gsi_vlan_external`, `parent_vlan_shifted`; my probes `gsi_vlan_settle_gate_removed` (killed by the GI WITHDRAWAL byte-exact checks) and `parent_vid_saturates` are also killed |
| probe guard | `:527-538`, `:729-741`, `:1340`, `:789-797` | Milan 5.5.3.5.16 step 1, .17 step 2, .18 step 1 | response accepted against the sent probe's controller; replacement controller rejected; retry byte-identical after a same-talker rebind; published record unchanged | `probe_guard_current_controller`, `probe_retry_current_controller`; my probes `overlay_write_removed` (297 failures), `published_mask_removed` (97), `guard_select_always_private` (6) and `ctlr_window_short` (67) are all killed by the listener suite |

Overlay soundness, reasoned from the ROM (`hdl/acmp/rom/gen_ltn_rom.py`) and the action order (`act_order_f`):
- PRB_W_RESP and PRB_W_RESP2 are entered only through A5 (BIND_NEW, TMR_DELAY) or A13 from PRB_W_RESP.
- A5 is the last action step and writes the private word after A8, which clears it, and A2, which sets `bind_ctlr_eid`.
- A6 and A13 leave the word untouched, so the guard and the duplicate read the controller that was actually sent.
- A15 replaces the word with the stream ID at settlement. GET_RX_STATE gates stream_id on settled states, and the published and NVM-shadow view masks non-settled states.

### (2) Area
- My own OOC 1x1 runs use the repository recipe `syn/ooc/protocol_processor_ooc.tcl` (sha256 3bd999f4..., the same at base and head), part xc7a100tfgg484-2, `-tclargs <tree> 1 1`, on exact `git archive` trees.
  - Base 09e357fb: **21,614 LUT / 18,908 FF**.
  - Head 96d3b78: **21,643 LUT / 18,922 FF**.
  - Delta **+29 LUT / +14 FF**, inside +40 / +40.
  - Both runs are bit-identical to the author's published reports for those trees: same LUT, FF, WNS, TNS and endpoint counts (`receipts/ooc-base/`, `receipts/ooc-head/`).
- The input hashes of the author's base and selected measurement (`compare-byte/inputs.json`) equal every `hdl/` blob at 09e357fb and at the exact head (`scripts/cmp_inputs.py`). Each of the six published single-item patches applies cleanly to base. Each reproduces its item's 55 recorded input hashes and touches only that item's files (`receipts/item-attribution-inputs.txt`). I did not re-synthesise the single-item builds; their figures are the author's.
- The attribution table is consistent with that evidence: the items sum to +27 / +4, the unreduced combination is +127 / +14, and the selected reduction is +29 / +14.
- The reduction keeps every clause behaviour and test:
  - Comparators: the controller comparisons are done before the state selection.
  - Byte selection: the controller octet is selected before its source.
  - The A10 private-word clear is dropped.
  - The full ACMP campaign kills 51 of 51 with 6 goldens passing, all 33 suites pass, and the probes above grade the reduced logic.

### (3) No register-map, top-level port or parameter change
`receipts/port-param-diff.txt` compares the module headers and parameter/localparam declarations at 09e357fb and the head:
- `protocol_processor_top` and `KL_acmp_talker` headers and parameters: no change.
- `KL_pp_acmp_listener`: only the authorised internal `act_settle_vlan_o` width (12 to 16) and its comment.
- `pp_acmp_pkg`: only the status constant 13 to 16.

`acmp_bound_vlan_o` stays `[N_STREAM_IN_P*12-1:0]` (`protocol_processor_top.sv:692`). Outside `hdl/acmp`, `tb/` and the top, no file changed against 09e357fb, so there is no side-port, register-map or document change.

### (4) Gates at the exact head (my runs, pinned simulator 5.050, identity verified)
| Gate | rc | Result |
|---|---|---|
| `scripts/run_suites.sh` | 0 | 33 suites, 1,028,384 checks, 0 failing; per-suite counts equal the author's head table (acmp_listener 3167, acmp_talker 1376, pp_top 10470, aecp_notify 67) |
| `scripts/lint_hdl.sh` | 0 | LINT OK for every module |
| `make check` | 0 | lint, wavedrom, links, matrix, modmatrix, params, ids, figures, stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `syn/yosys/run.sh` | 0 | 42 tops |
| `tb/pp_top/acmp_mutants.py --jobs 4` | 0 | 51 of 51 KILLED by named checks, 6 goldens PASS; none of the 18 added controls has a missing witness |
| `tb/pp_top/gsi_mutants.py --jobs 3` | 0 | 20 detected by named checks, golden and restored PASS |
| `tb/acmp_talker/retry_mutants.py --jobs 4` | 0 | 62 killed, 7 equivalence controls, 1 performance control, baseline and restored rc 0 |
| reviewer probes (`scripts/r552_probes.py`, using the repository's own grading) | 0 | 11 probes on 2 goldens: 8 KILLED and 3 SURVIVED. The survivors are `a12_status_never_cleared` (equivalent, S1), `srp_vid_from_upper_bits` (S2), and `published_mask_removed` / `guard_select_always_private` at pp_top level, where they are unobservable but are killed by the listener suite |

I did not re-run the other ten affected campaigns (d3, notify, aecp, aecp-dispatch, ctr, name_wr, adp_engine, maap, srp_top, srp_admission) at base or head. For those I rely on the author's published base and head receipts (rc 0 at both, with unchanged canonical records). Base-revision gates are likewise the author's receipts.

### (5) Merge of main 09e357fb
`git merge-tree --write-tree ba3f3f3 09e357fb` returns 0 and gives tree `58e1fcfe5e57...`, equal to the tree of merge commit `fee74ef` (`receipts/merge-tree.txt`), so the merge introduces no content of its own. The only file both sides changed is `tb/pp_top/README.md`, which merged cleanly. The merge-touched suites (aecp_notify, pp_top) pass in my head bank. The author's published merge receipts (aecp_notify 67 checks rc 0, pp_top rc 0) cover the pre-reduction merge revision.

## Lens evidence
- **Conformance.** Each corrected item is checked against the clause cited in the issue's frozen table and the manager's two rulings. IEEE 1722.1-2021 Table 8-3 codes are 2 / 13 / 16. The talker's invalid-source rule follows the TD1 ruling. LD2's extension to A5 (5.5.3.5.10) is the necessary consequence of 5.5.3.5.30 step 2, because otherwise the kept status would be cleared one transition later. It is stated and tested. The probe-from-wrong-interface behaviour is unchanged and remains within clause, as the issue records. Unclean only through R552-F1: the compliance matrix and Δ4 are conformance claims and are now false.
- **RTL.** I reviewed the full diff against 09e357fb and ed340b9b and the round-2 commit. The overlay lifetime was traced through the ROM and the action order. Byte selection is checked for bytes 12..19, big-endian. Port and parameter immutability are verified, the record width stays 384 bits, lint and Yosys are clean, and the OOC area is reproduced. CLEAN.
- **Robustness.** Reset and X_INIT sweep zero the record and preload builds PRB_W_AVAIL with a zero word. A stale controller in the private word is unreachable: it is read only in PRB_W_RESP/RESP2, after A5 rewrites it. Published and NVM-shadow views are masked. GSI selector 6 is range-gated and PROBING_COMPLETED-gated. Out-of-range descriptor indices give zero. The talker's invalid-source path does nothing to the DA gate, allocator or timers (`disconnect_changes_gate` is killed). CLEAN.
- **Tests.** Every expectation change carries a stated clause reason (`tb/acmp_listener/README.md:127-174`, `tb/acmp_talker/README.md:330-343`, `tb/pp_top/README.md:2816-2843`). The 18 added controls are all killed by their named witnesses at the head, and 8 independent reviewer probes are killed. Suggestions S2 and S3 are optional extensions. CLEAN.
- **Docs.** The testbench READMEs and the RTL banner and comment updates are accurate. The architecture, compliance and guide documents are stale in four areas (R552-F1 to R552-F4). UNCLEAN.

## Reviewer-owned ledger
| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R552-F1) | issue #168 table, ruling 6050554601 and the TD1 ruling; `KL_pp_acmp_listener.sv`, `KL_acmp_talker.sv`, `pp_acmp_pkg.sv`, `protocol_processor_top.sv` diffs; `docs/00_MILAN_COMPLIANCE_REVIEW.md`; `docs/architecture/01_overview.md` F01.4 | R552-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| RTL | CLEAN | full `hdl/` diff ed340b9b..head and 09e357fb..head; round-2 commit; ROM generator and action order; port/param diff; lint; Yosys; OOC base/head reproduction | R552-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| Robustness | CLEAN | reset/init/preload paths; published-record mask; overlay lifetime; GSI gating; talker no-side-effect path; reviewer probes | R552-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| Tests | CLEAN | `tb/acmp_listener/{sim_main.cpp,field_cases.hpp}`, `tb/acmp_talker/sim_main.cpp`, `tb/pp_top/{sim_main.cpp,gsi_internal.hpp,acmp_mutants.py}`; suite bank; ACMP, GSI and talker campaigns; 11 reviewer probes | R552-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| Docs | UNCLEAN (R552-F1, F2, F3, F4) | tb READMEs; `docs/architecture/{01,02,05,06,07}`; `docs/00_MILAN_COMPLIANCE_REVIEW.md`; `docs/guides/{operator,integrator,hdl-engineer}.md`; `docs/README.md`; PR body | R552-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |

## Prior public review findings
None existed on PR #171 or issue #168 before this round: 0 reviews and 0 review comments on the PR, and only the two start notices. The concurrent external review for this round was posted while this review ran. I did not read it, to keep the two reviews independent, so nothing in this report depends on it.

## Hosted CI at the exact head (observed, not accepted; the manager owns hosted acceptance)
`receipts/gh-check-runs.tsv`, `receipts/gh-pr-checks.txt`:
- pull_request run 37960994447: docs-gates success, portability success, suites still in progress when last observed.
- push run 37960989290: portability success, suites in progress, docs-gates failure. Its log (`receipts/gh-docs-gates-push-failed-tail.txt`) shows the failure is `npm error code ECONNRESET` in the dependency-install step. That is infrastructure: `make check` did not execute in that job.

## Real limits
- The Milan v1.2 and IEEE 1722.1-2021 texts were not available to this review. Clause judgements rest on the issue's frozen clause table (checked by two reviewers and the manager), the manager's two rulings, and the Table 8-3 code assignments.
- Single-item OOC figures were not re-synthesised. Only base and final were reproduced (exactly); the items are verified by input hashes only.
- Ten affected campaigns and every base-revision gate were not re-run by me; for those I rely on the author's published receipts. The 17 parent consumer commands at the scratch parent and the author's parent report-calibration arm (unrun, disclosed) were not executed by me.
- No manager source bank ran at this head, and none is claimed. Physical calibration was not run, and field skips are not hardware proof. Post-synthesis timing is an estimate (S4).

## Pending manager duties
- Decide the scope for R552-F1 to R552-F4: authorise the document edits on this branch, or open a tracked follow-up that lists every location and link it from the PR.
- Donor bank (9) and parent consumer bank (17) at dev 5603c353; current-dev merge-candidate builder and native banks at the merge turn, with receipts linked on the PR.
- Hosted CI acceptance: the suites jobs were still running at observation, and the push-run docs-gates failure was a network install error.
- Carry the parent-side handling of a stream_vlan_id that is not a valid VID (out of scope by ruling 6050554601).

## Receipts
All receipt paths are relative to this packet and listed in `MANIFEST.sha256`:
- `receipts/head-*.log|rc`: suites, lint, make check, matrix, Yosys, campaigns.
- `receipts/r552-probes.log|rc`: reviewer probes.
- `receipts/ooc-*.log|rc`: OOC run logs.
- `receipts/acmp_mutants-head/`, `gsi_mutants-head/`, `talker_retry-head/`, `r552-probes/`: per-run logs and `results.json`.
- `receipts/ooc-base/`, `receipts/ooc-head/`: util, util_hier, timing, synthesis log.
- `receipts/port-param-diff.txt`, `receipts/item-attribution-inputs.txt`, `receipts/author-ooc-timing-summary.txt`, `receipts/merge-tree.txt`, `receipts/verify-tree.txt`, and the hosted-CI captures.
- `scripts/`: the portable runner, probe, comparison and verification scripts used.

R552-1 FINISHED
