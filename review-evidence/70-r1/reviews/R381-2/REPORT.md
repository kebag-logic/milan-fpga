[R381] NEGATIVE - exact head e796c68a460fe6946e28cb9da0349a382c868352

# R381-2: external re-review of PR #610 (issue #70 lane 0, D3 contract adoption), round 2

- Head under review: `e796c68a460fe6946e28cb9da0349a382c868352`, tree `2bbb410b9af6b0f8513e2693e4726a1c3bde4205`. This is also the published PR head. Clone integrity is in `receipts/integrity.txt`.
- Delta reviewed: `6029890c..e796c68a`. It is one commit, [A405]'s `docs: reconcile D3 processor contracts and ruled retry policy`, with a one-line subject and no body or trailers.
- Whole PR base: `c07232228c12b72805dd20e6852bf93f25794da0`.
- Processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`. PR #109 (`008edbbf`) and PR #110 (`939c1433`) are ancestors of it.
- Authorities, in the order read:
  - AGENTS.md and CONTRIBUTING.md;
  - docs/README.md;
  - the issue #70 body;
  - the status audit 5862191328, the lane-0 assignment 5862193501, the rulings 5862405632 (fixed, not re-opened) and the round-2 assignment 5862910366;
  - the [A405] TAKEN and REVIEW READY comments;
  - the processor sources and documents at the pin;
  - the delta and the history;
  - the public evidence tree `review-evidence/70-r1` at `6cf46c2a`, and the hosted checks at the exact head.
- Prior round-1 findings (R381-1 and R380-1) were read only after the independent pass.

The round-2 work is mostly right:

- The five locations R381-1 F1 named and the four documents R380-1 F1 named now all have rows in section 15.2, and every row is accurate at the pin.
- The stale pin and wiring lines are corrected or dated.
- No document still presents the debounce as open.
- The producer writer's state machine now follows DR2c exactly.
- Both taken suggestions landed.
- Only the four assigned documents changed. The register and all 26 checkbox states are byte-identical.

The verdict is NEGATIVE because of two open MINOR findings:

- **F1** (retained from round 1, narrowed): at the pin, some processor statements that the adopted D3 falsifies still have no row. The table's own named sweep does not find them.
- **F2** (new, introduced by the DR2c fix): the firmware-side "alarm kept until reset" has no carrier in the status contract. It also contradicts FASTCONNECT section 9.2's recovery rule and its Recovery acceptance line.

## Findings

### F1: MINOR: Conformance, RTL, Docs: `docs/design/SAVED_STATE_MATERIALIZATION.md:2291-2360` (section 15.2 and its contract sweep): processor statements D3 falsifies remain outside every row, and the named sweep misses them

- **Authority.** Round-2 assignment item 1 requires section 15.2 to include "every processor document and source contract that the adopted D3 falsifies". Lane 1's acceptance (`:2510-2511`) is to "Apply the complete processor contract table in section 15.2" and "Complete its named contract sweep".
- **What D3 now says.**
  - Section 3 rule 3 (`:297-304`): "Triggers are the live writes, never the commit marks".
  - Section 3.1 (`:423`): marks "remain notification effects, without record-selection authority".
  - Section 3 rule 2 (`:292-296`): the latch runs "in ONE window in which no AECP program runs and none is dispatched". Section 12 (`:1939-1941`) measures that hold-off at up to 179 cycles.
  - The 02 and arbiter rows assign manager 1 to the processor D3 writer.
- **Evidence.** These statements at `16be6768` are reproduced by `scripts/finding_evidence.sh` (output in `receipts/finding_evidence.txt`). Every one prints "matched by the named sweep: 0".

  | Statement at the pin | What it claims | Row status |
  |---|---|---|
  | `hdl/aecp/ucode/gen_ucode.py:2091` "naming persistence trigger"; `:1364`, `:1439`, `:1675`, `:1925`, `:2002` "persist it"; `:1791` "persist changed map state" | the mark is the persistence trigger | no row for the file. The sweep also says "microprogram marks stay valid. They do not need rewriting merely because this search finds them" (`:2358-2359`), which invites leaving these comments |
  | `docs/architecture/06_aecp_engine.md:342-344` (6.2.1), `:365` (6.4, SET_NAME chain), `:423` (6.5) | SET_NAME "emits the naming persistence ... triggers"; a map change "marks the mapping persistence class dirty" | the 06 row names "4/5 and state/name/format/map interfaces", and its required change never says the mark stops being a persistence trigger |
  | `docs/00_MILAN_COMPLIANCE_REVIEW.md:208` (GAP-08) | "Name updates now emit the persistence trigger" | the row names GAP-09 and the REQ rows only |
  | `docs/architecture/03_packet_engine.md:236`, ordering rule (d) | "NVM commits are asynchronous and never delay responses" | no row for the file. D3's latch window holds dispatch. `02_interfaces.md:492` cites this rule and also sits outside its row's `532-572` range |
  | `hdl/top/protocol_processor_top.sv:2448-2451` | "Manager 1 is the platform's saved-state writer" | the rows name `124-130`, `424-454`, `647-668` and `2513-2546` |
  | `tb/acmp_nvm/README.md:15` | "manager 1 is a harness face, as the platform's saved-state writer will be" | the row names debounce, retry, alarm and group coverage only |

  The named regular expression (`:2349`) also fails on the arbiter banner itself (`KL_pp_nvm_mgr_arb.sv:15-16`), because "integrating" and "platform's" fall on separate lines. That location is saved only because the arbiter has its own row.
- **What is resolved.** 35 rows over 27 files now exist. Every path exists at the pin, every cited line range lies inside its file, and the spot-checked contents match (`scripts/check_edit_table.py`, `receipts/edit_table_rows.txt`). The previously missing locations now have rows:
  - `02_interfaces.md:532-536`;
  - `integrator.md:334/336`, the parameter inventory (`:47-105`) and diagram 21;
  - `operator.md:197-227`;
  - `01_overview.md:100-107,170`.
- **Impact.** A lane 1 that applies every row and runs the named sweep still leaves processor documents and source comments that call the completion mark the persistence trigger, that give manager 1 to the platform, and that promise persistence never delays a response. Those are the three contracts D3 rules 2, 3 and 5 replace, and integrators read them.
- **Required outcome.**
  - Section 15.2 carries rows (or extends existing rows' locations and required changes) for every statement above. The mark-trigger rows should say explicitly that the marks stay but stop being persistence triggers.
  - The named sweep finds them, for example by adding `persist|platform's|never delay` or equivalent terms. Alternatively, the table states why a listed location is out of scope.
  - The microprogram-mark exemption is narrowed so that it cannot cover trigger-describing comments.
- **Verification.** Re-run `scripts/finding_evidence.sh`. Every F1 location maps to a 15.2 row, and the named sweep prints a non-zero match for each.

### F2: MINOR: Conformance, Robustness, Tests, Docs: firmware DR2c "alarm until reset" has no status carrier and conflicts with FASTCONNECT 9.2

- **Where.**
  - `docs/design/SAVED_STATE_MATERIALIZATION.md:754-761` ("The alarm remains until reset; failed slots never receive ACK").
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1093-1100` (`:1097`).
  - `docs/integration/BAREMETAL_FIRMWARE.md:1913-1917` (`:1916`).
  - Lane 2's acceptance `:2557` ("reset-only alarm") and its negative control `:2588` ("Clear an exhausted alarm on heartbeat or later success").
- **Authority and evidence.**
  - The lane-0 scope requires one normative home per rule, with the two pages agreeing. FASTCONNECT section 9 is the home for the status bits (D3 section 1 authority list; D3 section 17, Status rows).
  - The only reset-sticky alarm FASTCONNECT 9.2 defines is the port's `nvm_alarm` (`:1106-1109`, `:1122-1130`). That is a processor producer's exhaustion signal, which firmware cannot raise.
  - A firmware media failure is a `VD_*` verdict loss, and 9.2's next-state rule clears it on recovery: `stale' = loss ? 1 : (backed' AND NOT dirty') ? 0 : stale` (`:1161-1167`). The unchanged Recovery acceptance line (`:1539-1541`) requires `nvm_stale` to clear once a commit completes with `nvm_dirty` 0.
  - None of the four pages, nor `docs/reference/REGISTER_MAP.md`, names a signal that carries firmware transaction exhaustion (`receipts/finding_evidence.txt`, F2 section: 0 matches in each).
- **Impact.**
  - Lane 2 is told to implement a firmware reset-only alarm and to kill a mutant that clears it on later success.
  - The normative status contract, and an acceptance line lane 5 must meet, require the same later success to clear the only state such an exhaustion leaves.
  - The two oracles cannot both pass, unless an undefined new carrier exists. Choosing between them would be a private interpretation of DR2c.
- **Required outcome.** The contract states which observable signal or state carries firmware transaction exhaustion, and how it composes with FASTCONNECT 9.2's recovery rule and the Recovery and healed-outage acceptance lines. That can be a new sticky state with a 9.2 cross-reference, or a statement that the ruled alarm applies to producer alarms only while firmware exhaustion stays a 9.2 loss. DR2c is fixed. If reconciling it needs the manager's reading, the conflict is published for a ruling rather than decided in the text (AGENTS.md section 2).
- **Verification.**
  - `scripts/finding_evidence.sh`, F2 section: a named carrier appears, and FASTCONNECT 9.2 or 16 cross-references it.
  - The lane-2 negative control and the FASTCONNECT Recovery line no longer demand opposite outcomes for the same sequence.

## Round-2 focus items, checked independently

1. **15.2 completeness against `16be6768`.** Partially met; see F1.
   - Every R381-1 F1 location now has a row: `02_interfaces.md:532-536`, `integrator.md:334`, `integrator.md:336`, `operator.md:202-206` and `01_overview.md:170`.
   - Every R380-1 F1 document now has a row: integrator 334/336, the integrator parameter table plus diagram 21, `operator.md:210-226` and `01_overview.md:170`.
   - My own sweep of the pinned `docs`, `hdl` and `tb` trees, and the top-level processor files, found the F1 residue. The author's named sweep (`receipts/sweep_author_pattern.txt`, 262 matches) additionally hits `KL_adp_engine.sv`, `KL_pp_side_port.sv`, `KL_pp_acmp_lsn_admit.sv` and the test benches. I reviewed those matches and found no falsified contract: the side port keeps requested enable, and the admission gate's "the top's `restore_done_o` ... takes it" remains a true necessary condition.
   - The diagram rules match the processor's `docs/diagrams/README.md`: 21 is an SVG master with a generated PNG, and 20, 23 and 24 are hand-authored.
2. **Stale pin and wiring lines.** Resolved.
   - FASTCONNECT `:119` names `16be6768`, the arbiter at top `:2523` and manager 1 tied idle at `:2540-2546`. These match the pin.
   - `:131-134` states that parent `c0723222` pins `16be6768`, matching D3 `:71-72`.
   - The `2faa5af8` repair is dated historical (`:136-142`).
   - The mark row (`:121`) and section 12.1 (`:1360-1364`) are pinned to `44489453`, and section 4 to `e743dcdc`.
   - No other present-tense processor pin or top-line citation remains in the three design pages.
3. **Debounce presented as open.** Resolved.
   - No Markdown outside `docs/history` presents the debounce as open or provisional. FASTCONNECT `:1287-1291`, `:1424`, `:1454`, D3 `:1959`, snapshot `:1808` and BAREMETAL `:1899` all cite DR2a.
   - The only remaining source citations are `milan_baremetal.c:340` and `scripts/nvm_shape.py:146-148`. Both are recorded as lane-2 corrections (D3 `:2559-2566`), and lane 0 may not edit source. `sw/` is unchanged from base to head.
4. **DR2c writer text.** Producer side resolved.
   - Rule 4 (`:307-317`), 6.1 (`:621-648`) and 6.3 (`:683-690`, `:750-752`) give three attempts, including the initial write. `RETRY_MAX_P = 2` counts additional retries.
   - After each failed attempt, BACKOFF waits 500 ms, holding neither the bus nor the port, and relatches. No fourth attempt follows, and the alarm is sticky until reset.
   - The counter arithmetic is consistent: an increment on grant, retry while below 3, and giveup at 3.
   - The pinned binding writer's immediate retry is stated as a required lane-1 change (15.2 row; 18.1 `:2512`). I verified it at `KL_acmp_nvm_shadow.sv:120` (`RETRY_MAX_P = 2`) and `:865-895` (error goes to `H_FL_RD` with no wait), and the top does not override it.
   - Current firmware is stated as lacking the bound.
   - The firmware alarm half is F2.
5. **Taken suggestions.** Both resolved.
   - S1: FASTCONNECT `:1561-1562` now states the oracle inline.
   - S2: D3 `:583-587` cites `milan_baremetal.c` 1450, 1220-1221 and 1453-1454 at `c0723222`. All three were verified: the "before the entity model is loaded" comment, the "after the AEM image is in place" comment, and the `nvm_boot()` / `load_aem_image()` calls.
6. **Change-set limits.** Met.
   - The delta touches exactly the four listed documents (`receipts/delta_files.txt`).
   - The D3 15.1 register section is byte-identical at `6029890c` and the head. All ten selected-option cells are byte-equal to ruling 5862405632.
   - The FASTCONNECT section 16 checkbox sequence (26 lines, 5 checked) is identical at the base, at `6029890c` and at the head (`receipts/register_checklist.txt`).
   - The S1 sentences sit under the existing unchecked Status-10 line, as that taken suggestion requested.

## Prior public review findings: disposition at this head

| Finding | Disposition at `e796c68a` |
|---|---|
| R381-1 F1 (MINOR; Conformance, RTL, Docs) | Named locations resolved. **Retained, narrowed, as R381-2 F1** for the residual statements above |
| R381-1 F2 (MINOR; Docs) | Resolved (item 2) |
| R381-1 S1, S2 (SUGGESTION) | Taken and resolved (item 5) |
| R380-1 F1 (MINOR; Conformance, RTL, Docs) | The four documents are resolved; the residual is carried by R381-2 F1 |
| R380-1 F2 (MINOR; Conformance, Docs) | Resolved (item 3) |
| R380-1 F3 (MINOR; Conformance, RTL, Robustness, Docs) | Resolved for the producer and binding writers (item 4). The firmware-side extension introduced R381-2 F2 |
| R380-1 S1-S5 (SUGGESTION) | Not taken by the round-2 assignment. Not re-assessed as findings |

## Executed checks (exact head, foreground)

| Check | Result | Receipt |
|---|---|---|
| `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base c0723222`, `check_baremetal_only.py --check`, `ci_scope.py --selftest`, `check_feature_status.py`, `git diff --check`, `git diff --check c0723222 HEAD` | all exit 0 (hash-locked Markdown dependencies, PyYAML 6.0.3, in a disposable environment) | `scripts/run_gates.sh`, `receipts/gates.txt` |
| 15.2 rows: pin links, paths, line ranges | 35 rows, 27 files, 0 bad | `scripts/check_edit_table.py`, `receipts/edit_table_rows.txt` |
| Register versus ruling; checkbox states | 10/10 byte-equal; the sequence is identical | `scripts/check_register_and_checklist.py`, `receipts/register_checklist.txt` |
| Relative links added by the delta | 8 links, 0 unresolved | `scripts/check_delta_anchors.py`, `receipts/delta_anchors.txt` |
| Author's named sweep at the pin | 262 matches, reviewed | `receipts/sweep_author_pattern.txt` |
| Finding evidence F1/F2 | reproduced | `scripts/finding_evidence.sh`, `receipts/finding_evidence.txt` |
| Hosted checks at the exact head (read-only) | See the limits below | `receipts/hosted_checks.txt` |
| Clone integrity after all checks | HEAD and tree equal; the index (mode, blob, path) hash equals HEAD's; 0 porcelain entries; 4 gitlinks unchanged; processor clean at the pin | `scripts/integrity.sh`, `receipts/integrity.txt` |

No probe or mutation edited the clone. No simulator was run, because the change is documentation only and no RTL is under review.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | round-2 assignment items 1-4 and S1/S2 against D3 15.2 (`:2291-2360`), 6.1/6.3, rule 4, 18.1/18.2; ruling 5862405632 against 15.1 (`receipts/register_checklist.txt`); FASTCONNECT 9.2/16 against the DR2c text; processor tree at `16be6768` (`receipts/finding_evidence.txt`) | R381-2 | `e796c68a460fe6946e28cb9da0349a382c868352` |
| RTL | UNCLEAN (F1) | `KL_acmp_nvm_shadow.sv:14,30-31,117-122,865-895`; `protocol_processor_top.sv:124-130,1645,2448-2451,2513-2547,4200`; `KL_pp_nvm_mgr_arb.sv:11-54`; `KL_aecp_desc_mem_guard.sv:18-21,54`; `KL_aecp_dyn_state.sv:68`; `gen_ucode.py` mark sites; D3 6.3 attempt/backoff next-state functions against the binding FSM | R381-2 | `e796c68a460fe6946e28cb9da0349a382c868352` |
| Robustness | UNCLEAN (F2) | D3 6.1 BACKOFF and exhaustion transitions, `:686-690` giveup/retry boundary (attempt 3 against `1 + RETRY_MAX_P`), taint during backoff, LATCH-MAP overflow during retry; firmware exhaustion path against FASTCONNECT 9.2 loss and recovery (`:1106-1167`); snapshot `:1093-1100` capture refusal distinct from media attempts | R381-2 | `e796c68a460fe6946e28cb9da0349a382c868352` |
| Tests | UNCLEAN (F2) | D3 18.1 `:2532-2533` and 18.2 `:2587-2589` DR2c negative controls against FASTCONNECT 16 Recovery `:1539-1541` and healed-outage `:1542-1545`; Status-10 oracle `:1557-1563`; 26-line checkbox sequence at base, `6029890c` and head | R381-2 | `e796c68a460fe6946e28cb9da0349a382c868352` |
| Docs | UNCLEAN (F1, F2) | the four changed pages at head (`receipts/delta_files.txt`); new anchors (`receipts/delta_anchors.txt`); docs gates (`receipts/gates.txt`); pin and history labelling FASTCONNECT `:115-142`, `:1360-1364`; open-debounce search across parent Markdown and sources; processor documents and diagrams at the pin | R381-2 | `e796c68a460fe6946e28cb9da0349a382c868352` |

## Real limits

- The public evidence tree at `6cf46c2a` (`review-evidence/70-r1`) contains the round-1 author gate logs only. At fetch time (2026-09-28T04:12Z), no manager evidence comment for this head had been posted on #70 or #610, and I could not locate the manager's static, builder or native bank receipts for `e796c68a`. I did not re-run those banks; that is outside this review's allowance.
- Hosted checks at the exact head, at fetch time:
  - succeeded: `rtl-fast`, `full-ci-gate`, `elaborate`, `changes`, `bdd-conformance`, `wire-accountability` and `docs-check-no-git`;
  - still in progress: `docs-check`;
  - skipped, not executed, and not evidence here: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, the sharded Verilator and Yosys matrices, and physical gPTP.
- The Milan v1.2 and IEEE texts were not re-read. This round's delta introduces no new clause interpretation.
- The historical EXECUTED claims in D3 and the out-of-tree evidence branch were not re-run. The delta does not change them.
- There is no physical evidence. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Publish this report, and obtain R380-2's verdict.
- Route F1 and F2 to the executor. F2 may need the manager's reading of DR2c's firmware "alarm" before the text can be reconciled; DR2c itself stays fixed. Re-review at the new head. Because both fixes are documentation, Conformance, RTL, Robustness, Tests and Docs must be covered again at a head that includes them.
- Confirm hosted `docs-check` succeeds at the exact head. Publish the static, builder and native bank receipts for this head. Own hosted and act acceptance.
- Build and validate the final current-dev candidate at the merge turn. The source base and live dev were both `c07232228c12b72805dd20e6852bf93f25794da0` when this round started.
- After merge: DR3a ratification or revision after lane 1's measurements, before lane 2 implements. #70 stays open; this lane does not close it.

R381-2 FINISHED
