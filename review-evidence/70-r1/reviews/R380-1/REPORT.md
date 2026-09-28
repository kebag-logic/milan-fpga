[R380] NEGATIVE - exact head 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769

# R380-1: internal independent review of PR #610 (issue #70, lane 0: adopt the D3 contract)

- Head `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769`, tree `071521406d21866951d6f424f87bea90b405a17e`.
- Base `c07232228c12b72805dd20e6852bf93f25794da0` (live `dev` at inspection).
- Processor gitlink `16be6768f710e79450aace277abacd6c2c3336e5`.
- Two commits, `0309a9ee` and `6029890c`. Each has a one-line subject with no body or trailers.
- Four documentation files change. Nothing outside `docs/` changes and every gitlink is unchanged (`receipts/40_pr610_meta.json`, `receipts/90_final_identity.txt`).
- Verdict: NEGATIVE. Three MINOR findings are open (F1 to F3), and each leaves its lenses unclean. No BLOCKER or MAJOR finding was found.

## Reconstruction (public state only)

I read these sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The issue #70 body and its comments. These include:
   - the status audit, 5862191328;
   - the assignment, 5862193501;
   - the TAKEN and REVIEW READY notes;
   - the manager rulings, 5862405632.
4. REQUIREMENTS.md sections 1 and 8, including REQ-VER-06.
5. The Milan v1.2 saved-state clauses: 5.3.4.1/.2, 5.3.5.1, 5.3.7.1/.6, 5.3.8.1/.2/.3/.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.12 and 5.3.13.
6. The processor sources at `16be6768`.
7. The full diff `c0723222..6029890c` and its history.
8. The public evidence tree at `6cf46c2a` under `review-evidence/70-r1`: the manifest, the author gate logs and the contract-check log.
9. The exact-head hosted check runs.

Prior public review findings on PR #610: none exist. At inspection the PR had zero reviews, zero inline comments and two issue comments, both review-start notices. So there is nothing to resolve or retain. The R217/R218 findings from the earlier #500 rounds are still mapped in D3 section 16, and this diff does not alter that mapping.

## What was verified clean

1. **D3 is Accepted, and every acceptance line has a home.**
   - The D3 header now reads "ACCEPTED contract; materializer not implemented" (D3:6).
   - FASTCONNECT section 16 still has 26 checkboxes, and exactly the same 5 are checked at the base and at the head.
   - D3 section 17 maps all 26 lines in group order (`receipts/22_acceptance_map.txt`).
   - Each rule has one owner and a cross-reference from the other page:
     - triggers per live-write group: D3 3.1; nine groups, with formats and maps split by direction and all names in one group;
     - IDENTIFY exclusion: D3 3.1/9;
     - dirty retirement: D3 7.1;
     - boot transaction and AEM-first order: D3 5.3/8.1;
     - rollback, debt and CLOSED: D3 8.6/8.8.
   - FASTCONNECT 9.3, 10, 12.2, 13, 14, 15 and 16 all point back to these homes.
   - 147 fragment links in the four pages resolve (`receipts/32_anchor_check.txt`).
2. **The register reproduces the manager's rulings.**
   - All ten rows (DR1a to DR6) read RULED.
   - The "Selected option" cells match the ruling comment byte for byte (`scripts/compare_rulings.py`, `receipts/21_compare_rulings.txt`, rc 0).
   - DR3a's ratification point, "the manager ratifies or revises both before lane 2 implements", appears in D3 8.8, 15, 15.1 and 18 (all lanes), and in FASTCONNECT 14, 15 and 16.
   - DR4's scope appears in FASTCONNECT 8.3 and 16 and in D3 10, 15.1, 17 and 18.1 to 18.5. That scope is 1x1 TDM8 shipping acceptance, with the 8x8 post-place obligation "open and blocked, not waived" and the 8x8 non-shipping until it fits (`receipts/50_lane_contract_carry.txt`).
3. **The processor facts cited are correct at `16be6768`.**
   - #109 (S1/S3/S4) and #110 (S2) are merged into the pin.
   - `KL_pp_nvm_mgr_arb`, `KL_aecp_desc_mem_guard` and `KL_pp_acmp_lsn_admit` exist.
   - Manager 1 is tied idle (`protocol_processor_top.sv:2540`).
   - The binding record carries started/sw/talker_uid/talker_eid/ctlr_eid.
   - The F07.9 line ranges given for 07 5.3 (447-458, 459-475) and 02 8.1/8.2 (538-572) are accurate (`receipts/10_pp_0707_lines.txt`).
   - Parent firmware `milan_baremetal.c:1254` returns on shape mismatch before the walk. `:1438` begins `milan_init`, which calls `nvm_boot` before `load_aem_image`.
4. **Every lane 1 to 5 contract has its required parts.**
   - Each states acceptance, validation, negative controls and dependencies, plus the physical result it still owes (`receipts/50_lane_contract_carry.txt`).
   - Lane 5's physical result matches REQ-VER-06:
     - seven days;
     - 200 cold cuts, 160 idle and 40 during commits;
     - T0 + 20 s first advertisement;
     - the provisional 30 s restoration ceiling;
     - reconnect under 1 s.
5. **No implementation or proof is claimed, and nothing is silently weakened.**
   - Checkbox states are unchanged.
   - The eight-mark and SET_CONTROL mark lines are replaced by nine trigger deletions, nine replay deletions and an IDENTIFY exclusion that is at least as strong. This replacement is recorded openly in D3 3 rule 3, 15 item 1 and 17.
   - The debounce-cut oracle keeps two properties: nothing older than the last verified snapshot is lost, and every unsaved change is reported by pending or dirty.
   - The area narrowing is the ruled DR4.
   - Every clause in D3's item-8 name list (entity_name, group_name, CONFIGURATION, AUDIO_UNIT, STREAM_INPUT/OUTPUT, AVB_INTERFACE, CLOCK_SOURCE, AUDIO_CLUSTER, CLOCK_DOMAIN, IDENTIFY CONTROL) matches Milan 5.3.13.
   - PTOF's 2 ms default matches Milan 5.3.7.6.
   - The configuration index is correctly recorded as design-affirmative, since Milan does not specify it.
6. **All gates pass at the head.** All nine lane-0 gates return 0 (`receipts/30_docs_gates.txt` and `receipts/31_docs_gates_pinned_renderer.txt`; see Limits). This agrees with the author's published `gate-results.json`.

## Findings

### F1: MINOR. Lenses: Conformance, RTL, Docs. The processor edit table misses four documents that the contract falsifies.

- **Where:** `docs/design/SAVED_STATE_MATERIALIZATION.md:2250-2269` (section 15.2). The need for this table is stated at D3:544 ("lists the required synchronized processor documentation edits"). Lane 1's acceptance (D3:2420) is to "Apply the processor documentation table in section 15.2".
- **Evidence:** at `16be6768` these processor documents state contracts that D3 replaces, and section 15.2 lists none of them (`receipts/51_f079_table_coverage.txt`):
  - `docs/guides/integrator.md:334` says to OR `nvm_unflushed_o` with `aecp_dyn_dirty_o` for the pending bit. D3 5.2 makes pending `nvm_unflushed | d3_unflushed` and removes the dyn level.
  - `docs/guides/integrator.md:336` says "Nothing in the processor writes a record for 6 or 7". D3 makes the processor writer own groups 6 and 7.
  - The integrator parameter table (`:75-105`) and diagram 21 have their parameter inventory compared against the top's declarations by `check-integrator-params.py` (`:104`). D3 adds `DEB_TICKS_P`, `RETRY_MAX_P`, `RS_TMO_CYC_P` and new exports.
  - `docs/guides/operator.md:210-226` has a restore table and `restore_blank_o` text ("a failed walk included"). It has no DEFAULTS or CLOSED rows. D3 15.2's own 07 row says "a failed product restore is never blank".
  - `docs/architecture/01_overview.md:170` (F01.5, P-NVM-RS-TMO-CYC) has only the binding read deadline, with no D3 walk deadline or aggregate budget.
- **Impact:** lane 1 can meet its "apply the table" acceptance and still leave the processor's integrator and operator contracts contradicting D3. That misstates the pending composition and the restore verdicts, and it breaks a documentation gate. Assignment item 3 asks for the complete edit list.
- **Required outcome:** section 15.2 lists every processor document whose contract D3 changes, at minimum the four above, each with its section and the required change. Alternatively, it states explicitly why one is out of scope.
- **Verification:** grep the processor at the pin for the superseded statements quoted above. Each one must map to a row in 15.2.

### F2: MINOR. Lenses: Conformance, Docs. Text still says the debounce is open after DR2a ruled it.

- **Where:** `docs/design/SAVED_STATE_FASTCONNECT.md:1281-1282` reads: "`T-NVM-DEBOUNCE` is a different quantity and is still open; section 14 says so and section 13 says what the PR that picks it owes."
- **Evidence:** the same head's FASTCONNECT section 14 (`:1445`) says "DR2a settles debounce policy", and section 13 (`:1415`) says "DR2a rules both first-dirty windows". The snapshot page (`:1797`) says the same. Three other citations of FASTCONNECT section 14 now state the opposite of what that section says:
  - `docs/integration/BAREMETAL_FIRMWARE.md:1899`: "the provisional value section 14 leaves open";
  - the source comments `sw/firmware/milan_baremetal/milan_baremetal.c:340` and `scripts/nvm_shape.py:146`;
  - D3:1919 still says "its provisional 1,000 ms debounce".

  (`receipts/52_debounce_consistency.txt`)
- **Impact:** the assignment requires that "the two pages must agree". FASTCONNECT contradicts itself about whether a ruled policy is open, and the firmware documentation points readers to a section that no longer says what is quoted.
- **Required outcome:**
  - FASTCONNECT 9.4 and BAREMETAL_FIRMWARE agree with DR2a, or cross-reference D3 15.1.
  - D3 12 uses ruled wording.
  - Lane 0 may not change code, so the two source-comment citations are recorded as an explicit obligation of the lane that next changes those files (lane 2 by D3 18.2).
- **Verification:** the grep in `scripts/static_receipts.sh` (receipt 52) finds no "still open" or "provisional ... section 14" statement in documentation. Any remaining source-comment citation is named in a lane contract.

### F3: MINOR. Lenses: Conformance, RTL, Robustness, Docs. The writer state machine still retries immediately, which contradicts DR2c.

- **Where:** `docs/design/SAVED_STATE_MATERIALIZATION.md:626` (6.1: "STREAM or WAIT | the port pulses err | ACQUIRE again (a fresh latch), or RUN with the alarm after `RETRY_MAX_P` retries"), `:662` (6.3: `giveup = port err AND retries = RETRY_MAX_P`) and `:310` (rule 4).
- **Evidence:** DR2c is RULED at `:2190`: "At most 3 write attempts per record, 500 ms apart", "Specify attempts versus retries explicitly". The header (D3:66) says "Sections 3 through 13 define the accepted D3 architecture". Sections 6.1 to 6.3 have no spacing or backoff state and no attempt/retry definition (`receipts/53_retry_fsm_vs_dr2c.txt`). The debounce, by contrast, got a DR2a precedence note at `:719-721`. The retry path got none.
- **Impact:** the accepted next-state functions, which lane 1 implements, describe back-to-back retries. The accepted ruling requires 500 ms spacing and at most three attempts. The retry rule therefore has two contradictory normative statements. An implementation that follows 6.1 exactly violates DR2c on the error path.
- **Required outcome:** 6.1, 6.3 and rule 4 either state DR2c's spacing and attempt bound, or explicitly defer to DR2c the way 6.3 defers debounce to DR2a. Either way, one retry rule is normative.
- **Verification:** 6.1 to 6.3 contain either the DR2c spacing and attempt count or an explicit DR2c precedence statement. No section describes an unspaced retry as accepted behaviour.

### Suggestions (non-blocking; they do not affect coverage)

- **S1** `SAVED_STATE_FASTCONNECT.md:70`, "Milan requires eight non-binding item groups": the configuration index comes from the compliance plan and a design decision (Milan does not specify it; D3 16 says "design-affirmative"). Suggested wording: "Milan and the compliance plan require ...".
- **S2** `SAVED_STATE_FASTCONNECT.md:1211`, "must not permanently block ordinary commands": the removed text said the entity keeps answering AECP, keeps accepting SETs and never claims durability when the writer wedges. D3 8.8 still carries the runtime rule. Restating it here would avoid reading "not permanently" as a relaxation.
- **S3** `hdl/milan/KL_pp_shadow.sv:943` says marks "remain available for future materialization", but D3 3.1 gives marks no authority to select records. Record this as a lane-2 comment correction.
- **S4** Two D3 17 rows name two pages as their "normative home": Status 4 (FASTCONNECT 9.3; snapshot 6.1) and Area 1 (D3 DR4; FASTCONNECT 8.3/16). Consider naming which page owns which part.
- **S5** The new FASTCONNECT area box says "Explain historical backend-bound divergence" but drops the number that triggers the explanation. The old box said 781 LUT against the 8.3 OOC bound, and 8.3 now also reports 993 LUT OOC for the shipping module. Naming the bound keeps the backend check testable.

## Lens results (clean lens lines carry their evidence)

```text
[R380] PASS Tests — D3 §17 (26 rows) vs FASTCONNECT §16 checklist base/head (receipts/22), D3 §18.1-18.5 negative controls, D3 §3.1/§8.2/§9 controls, lane-0 gates (receipts/30,31,32) — every acceptance line keeps its checkbox state and gains a mapped oracle; each of nine groups has independent TRG/RPL deletions that must fail a value check; the cleared-first vacuity control and the IDENTIFY exclusion (pending, record write, flash activity, zero after cycle) are retained or strengthened; every lane requires each control to fail a named assertion; all nine gates rc 0 at the head
[R380] MINOR Conformance — see F1, F2, F3
[R380] MINOR RTL — see F1, F3
[R380] MINOR Robustness — see F3
[R380] MINOR Docs — see F1, F2, F3
```

These artifacts were also checked under each unclean lens and found nothing further:

- **Conformance:**
  - the register against the ruling (receipt 21);
  - REQ-VER-06 against lane 5;
  - Milan 5.3.x against the D3 15.1 inventory;
  - the removed mark acceptance against D3 3.1 and 17.
- **RTL:**
  - the processor at `16be6768`: arb, guard, admit, the idle manager 1 and the binding record fields;
  - D3 6.3 next-state priorities (change wins over done, taint, group and index clear);
  - the three release points in 8.1 against the terminals in 8.8.
- **Robustness:**
  - D3 6.2 and 8.8 abort, rollback and CLOSED paths;
  - lane negative controls for zero, boundary, corrupt, delayed, over-capacity and malformed inputs, cuts at every stage, and disabled-writer and shape-mismatch boot.
- **Docs:**
  - the 4 changed pages, docs/README and REGISTER_MAP rows;
  - stale-reference search across the repository.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | issue #70 scope, ruling, audit, assignment; REQUIREMENTS §1/§8 REQ-VER-06; Milan v1.2 5.3.x saved-state clauses; D3 §3.1/§15.1/§17/§18; FASTCONNECT §16 | R380-1 | 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769 |
| RTL | UNCLEAN (F1, F3) | D3 §5.1/§6.1-6.4/§8.1/§8.6/§8.8; processor `16be6768` top, arb, guard, admit, `KL_acmp_nvm_shadow`, docs 02/05/06/07/08/09, guides; parent `milan_baremetal.c:1254,1438` | R380-1 | 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769 |
| Robustness | UNCLEAN (F3) | D3 §6.2 abort/rollback/CLOSED, §8.8 deadlines/quarantine, §15.1 DR1a/DR2c/DR3b, §18 negative controls | R380-1 | 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769 |
| Tests | CLEAN | D3 §17, §18 controls, §3.1/§8.2/§9; FASTCONNECT §16 base/head; lane-0 gates rerun; anchor check | R380-1 | 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769 |
| Docs | UNCLEAN (F1, F2, F3) | 4 changed pages, docs/README, REGISTER_MAP, BAREMETAL_FIRMWARE, repository-wide stale-reference search, processor docs at pin | R380-1 | 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769 |

## Real limits

- On the first run in the host environment, `gen_toc.py --check` and `check_em_dash.py` exited 2. The pinned Markdown renderer was not installed there, so those runs reached no verdict.
  - Both were rerun with the repository's hash-locked wheels (cmarkgfm 2025.10.22, html5lib 1.1) in a disposable environment under the packet's scratch directory. Both returned 0.
  - `docs_check.py` and `check_doc_style.py` also returned 0 in that environment (receipt 31).
- No simulation, mutation or RTL probe was run. The change is documentation only. The pinned Verilator was not needed, so its identity was not checked.
- The public evidence tree `6cf46c2a:review-evidence/70-r1` holds the author's gate logs and manifest only. I did not find the manager's full source static/builder and native bank logs in it, and this review does not rely on them.
- Hosted runs at the exact head, at 03:36 UTC:
  - executed and succeeded: `rtl-fast`, `wire-accountability`, `bdd-conformance`, `elaborate`, `full-ci-gate`, `changes`, `docs-check-no-git`;
  - still in progress: `docs-check`;
  - skipped, so not executed evidence: `verilator-suites`, `yosys-portability`, the shard jobs, `verilator-lint`, `yosys-elaboration` and `Physical gPTP`.

  (receipt 41)
- Milan clause text was read from a locally held copy of the consolidated v1.2 specification. That text is not reproduced in the packet.
- Physical calibration was NOT RUN. No hardware was used, and nothing here is hardware proof.
- The clone was left at exact head bytes: HEAD, tree, index digest and gitlinks are the same before and after, and the worktree and index are clean (receipts 00 and 90).

## Pending manager duties

- Hosted `docs-check` completion at the exact head. The manager also owns hosted and act acceptance.
- The external review (R381), and a re-review of F1 to F3 at the corrected head.
- Candidate-merge validation against live `dev` at the merge turn. The source base and live `dev` are both `c0723222` at inspection.
- Later, not this lane: DR3a ratification after lane 1 measures, and assigning executors and reviewers for lanes 1 to 5.

R380-1 FINISHED
