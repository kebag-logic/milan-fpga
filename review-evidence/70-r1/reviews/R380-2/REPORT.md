[R380] NEGATIVE - exact head e796c68a460fe6946e28cb9da0349a382c868352

# R380-2: internal independent re-review of PR #610 (issue #70, lane 0: adopt the D3 contract)

- Head `e796c68a460fe6946e28cb9da0349a382c868352`, tree `2bbb410b9af6b0f8513e2693e4726a1c3bde4205`. The parent is `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769`, the round-1 head.
- Delta under review: `6029890c..e796c68a`, one commit, "docs: reconcile D3 processor contracts and ruled retry policy". It has a one-line subject with no body or trailers.
- Whole PR: `c07232228c12b72805dd20e6852bf93f25794da0..e796c68a`, three commits, five documentation files.
- Processor gitlink `16be6768f710e79450aace277abacd6c2c3336e5`. All four gitlinks are unchanged (`receipts/20`, `receipts/90`).
- Verdict: **NEGATIVE**. One MINOR finding is open (F1). It leaves Conformance, RTL and Docs unclean. Robustness and Tests are covered clean at this head.
- Every round-1 finding is resolved at this head: R380-1 F1 to F3, R381-1 F1 and F2, and the taken suggestions R381-1 S1 and S2.
- F1 is new. My own sweep of the pinned processor tree, which the round-2 assignment asked for, found processor statements that D3 falsifies and that neither the section 15.2 table nor its named sweep reaches.

## Reconstruction (public state only)

I read these sources in this order:

1. AGENTS.md and CONTRIBUTING.md (the project instructions).
2. docs/README.
3. The issue #70 body and its comments, including:
   - the audit, 5862191328;
   - the lane-0 assignment, 5862193501;
   - the manager rulings DR1a to DR6, 5862405632, which are fixed and not reopened here;
   - the round-2 assignment, 5862910366;
   - [A405] TAKEN and REVIEW READY, 5863078929.
4. The D3, FASTCONNECT and snapshot-ownership contracts, and BAREMETAL_FIRMWARE.
5. The processor tree at `16be6768` (docs, hdl, tb).
6. Parent firmware at the base.
7. The delta diff and the whole-PR diff, with their history.
8. Public evidence:
   - the tree `6cf46c2a:review-evidence/70-r1`;
   - the exact-head hosted check runs.

My own round-1 packet was read-only input. I read the R381-1 report only after my own pass over the diff and the processor tree.

## Round-2 focus items

1. **Processor F07.9 edit table completeness.** Section 15.2 now has 35 rows over 27 files. Every path exists at `16be6768`, and all 37 links pin that commit (`receipts/40`).
   - Every location that R380-1 F1 and R381-1 F1 named now has a matching row with the required change (`receipts/42`):
     - integrator `:334`, `:336` and `:47-105`;
     - diagram 21;
     - operator `:197-227`;
     - 01_overview `:170`;
     - 02_interfaces `:532-536`.
   - The cited line ranges were spot-checked at the pin (`receipts/43`). The `KL_acmp_nvm_shadow` claim is accurate: `RETRY_MAX_P = 2`, and the error paths at `:864-873` and `:885-893` go straight back to `H_FL_RD`.
   - My own sweep over nine superseded-contract probes (`scripts/independent_sweep.sh`, `receipts/41`) found one residual class. Processor text still presents the AECP commit mark as the persistence trigger or mechanism: `gen_ucode.py`, `06_aecp_engine.md` 6.2.1/6.5 and `00_MILAN_COMPLIANCE_REVIEW.md:208`. There is no row or named sweep for it (**F1**).
   - The other hits that lack a row are not falsified:
     - `lsn_admit`, `adp_engine` and `side_port` enable comments stay true at the requested/combined split that D3 keeps;
     - `fig-02-nvmwave` says "bounded retry then side-port alarm", which is still true under DR2c;
     - the originator/listener ACMP retries are unrelated;
     - the normalizer "ROM lands in P4" is unrelated;
     - the `tb/*` wrappers and `tb/nvm_port/README.md:45` describe raw binding and port facts.
2. **Stale pin and wiring lines.**
   - FASTCONNECT `:119` now cites processor `16be6768`: the arbiter at top `:2523` and manager 1 tied idle at `:2540-2546`. Both were verified at the pin.
   - `:131-134` gives the reconciliation pin, which matches D3 `:71-72`.
   - `:136-142` dates the `2faa5af8` repair as historical.
   - `:121` keeps its "Historical ... at `44489453`" label.
   - No present-tense stale pin or wiring line remains in the four pages (`receipts/42`).
3. **Debounce no longer presented as open.**
   - FASTCONNECT `:1287-1291`, D3 `:1959-1960` and BAREMETAL_FIRMWARE `:1899-1900` now use the DR2a wording.
   - No "still open" or "provisional ... section 14" statement remains in the four pages.
   - The two source-comment citations (`milan_baremetal.c:340`, `scripts/nvm_shape.py:146`) are recorded as lane-2 obligations at D3 `:2559-2566`. Lane 0 leaves those files unchanged.
4. **Writer state machine follows DR2c.**
   - Rule 4 (`:309-314`), the 6.1 policy and table (`:621-648`) and 6.3 (`:683-690`, `:750-752`) define at most three attempts, counted at grant, with 500 ms BACKOFF from the err. BACKOFF owns neither the bus nor the port, relatching does not replenish the count, the alarm is sticky until reset, and a later success or heartbeat cannot clear it.
   - The count arithmetic is consistent. With `RETRY_MAX_P = 2`, attempts 1 and 2 go to BACKOFF and attempt 3 gives up.
   - The firmware policy (`:754-761`, snapshot `:1093-1100`, BAREMETAL_FIRMWARE `:1913-1917`) is three transaction attempts per unchanged captured work set, 1,000 ms apart, with no ACK for a failed slot. This is the ruled DR2c default text (`:2231`).
   - Current behaviour is stated as a required change, not as current behaviour:
     - the binding writer's immediate retry is a lane-1 row (`:2324`, `:2512`);
     - the firmware "lacks its bound" and the fix is lane 2's (`:761`, `:2557`).
   - At the base, `milan_baremetal.c:1068-1087` handles a failed transaction by clearing `nvm_dirty_since`, so the next service re-arms the debounce with no attempt count. That agrees with the statement.
5. **Taken suggestions.**
   - R381-1 S1 is at FASTCONNECT `:1561-1562`: "Every lost change was reported at the cut. Its reporter was producer pending or `nvm_dirty`."
   - R381-1 S2 is at D3 `:586-587`: "lines 1450 and 1220-1221", with the calls at 1453-1454. Verified against `milan_baremetal.c` at the base.
6. **Scope and frozen items.**
   - The delta touches exactly four files: FASTCONNECT, D3, SNAPSHOT_OWNERSHIP and BAREMETAL_FIRMWARE.
   - FASTCONNECT section 16 has the same 5 checked and 21 unchecked states, in the same order, at the base, at the round-1 head and at this head. S1 adds oracle text to an unchecked line and changes no state.
   - The entire D3 section 15.1 is byte-identical to round 1, with 10 rows RULED.
   - `scripts/compare_rulings.py` shows every "Selected option" cell equal to ruling 5862405632 (`receipts/11`, rc 0).

## Findings

### F1: MINOR. Lenses: Conformance, RTL, Docs. Processor text still presents the commit mark as the persistence trigger, and neither the 15.2 table nor its sweep reaches it.

- **Where:** `docs/design/SAVED_STATE_MATERIALIZATION.md:2291-2360`, the section 15.2 table and the contract sweep at `:2344-2360`.
- **Authority:**
  - D3 `:297`: "Triggers are the live writes, never the commit marks".
  - D3 `:423`: "Command-completion marks remain notification effects, without record-selection authority".
  - D3 `:530`: the IDENTIFY exclusion is the writer's change snoop ("Selector 7 and an out-of-range index set nothing").
  - FASTCONNECT `:1408`: "Live writes select records; marks retain command-completion meaning".
  - Round-2 assignment item 1: every processor document and source contract that the adopted D3 falsifies has a row.
- **Evidence at `16be6768`** (`scripts/f1_mark_semantics.sh`, `receipts/50`):
  - `hdl/aecp/ucode/gen_ucode.py`, the microcode source of `NVM_MARK`:
    - `:2091` `NVM_MARK imm=7  # naming persistence trigger`;
    - `:1364`, `:1439`, `:1675`, `:1925` and `:2002` `# ... persist it`;
    - `:1791` `# persist changed map state`;
    - `:1582-1584`: IDENTIFY is volatile because there is "No NVM_MARK", "so committing it to flash would ...".

    Section 15.2 has no row for this file (0 rows).
  - `docs/architecture/06_aecp_engine.md`:
    - `:341-344` (6.2.1): SET_NAME "emits the naming persistence and notification triggers ... the trigger alone does not make the update survive power loss";
    - `:422-425` (6.5): a map change "marks the mapping persistence class dirty".

    The 06 row (`:2308`) requires snooping, ownership, capture, map faces and IDENTIFY exclusion. It does not require restating these mark statements as completion notifications. By contrast, the 02 row (`:2307`) and the integrator row (`:2315`) do require that.
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:208`: "Name updates now emit the persistence trigger". The 00 row (`:2336`) cites only GAP-09 and the REQ entries.
  - The named sweep pattern (`:2349`) matches none of these 15 lines: all show sweep-miss in `receipts/50`. The only D3 sentence about them, `:2358`, says "microprogram marks stay valid" and "do not need rewriting".
- **Impact:** a lane 1 that applies section 15.2 and runs the named sweep, exactly as its acceptance requires (`:2510-2511`), still ships a processor whose microcode source and AECP architecture page say the mark persists the change. That is the model D3 rule 3 replaced, and the one the historical K10/K12 defect came from (D3 `:241-247`). The same failure mode R380-1 F1 named is left for a smaller set of files.
- **Required outcome:**
  - Section 15.2 carries a row for `hdl/aecp/ucode/gen_ucode.py` (the `NVM_MARK` comments and the IDENTIFY rationale).
  - The 06 row names the 6.2.1 and 6.5 mark statements with the completion-notification restatement.
  - The 00 row covers `:208`.
  - Alternatively, the named sweep is extended so that it provably matches these statements, and `:2358` does not exempt their wording. The marks themselves remain valid either way.
- **Verification:** re-run `scripts/f1_mark_semantics.sh`. Each listed line must be either named by a 15.2 row or matched by the named sweep pattern.

### Suggestions (non-blocking; they do not affect coverage)

- **S1 (RTL, Docs).** D3 5.1 Parameters (`:544`) lists `DEB_TICKS_P`, `RETRY_MAX_P` and `RS_TMO_CYC_P`, but gives no time base for the new 500 ms BACKOFF (`:625`, `:689`). The 15.2 01_overview row (`:2312`) already expects a "backoff" parameter mapped to top declarations. Name its unit and product value in 5.1.
- **S2 (Robustness, Docs).** The firmware DR2c exhaustion alarm has no named status surface. FASTCONNECT 9.2 (`:1099-1109`) sets `nvm_backed` again on any heartbeat, and its `alarm` loss term is the port's alarm. Naming in lane 2's contract (`:2557`) the level that carries firmware exhaustion would give the "clear on heartbeat" control (`:2588`) a concrete observable.
- **S3 (Docs).** The snapshot contents line (`:188`) says "Seven items this contract does not settle". Section 20 now leaves eight items unsettled (1, 4, 5, 6, 8, 9, 10 and 11), because item 7 is now RULED. The count was already inconsistent at the base (nine).
- R380-1 S3 to S5 were not taken. They were suggestions, so this has no effect on coverage.

## Prior public review findings: resolved or retained at this head

| Finding | State | Evidence |
|---|---|---|
| R380-1 F1 (four processor documents missing from 15.2) | RESOLVED | Rows exist for integrator `:334-336` (D3 `:2315`), the parameter inventory `:47-105` (`:2313`), diagram 21, operator `:197-227` (`:2317`) and 01_overview `:170` (`:2312`) (`receipts/42`, `receipts/43`). The residual found this round is a different statement class, filed as F1 above. |
| R380-1 F2 (debounce presented as open) | RESOLVED | See focus item 3 (`receipts/42`). |
| R380-1 F3 (writer FSM retries immediately) | RESOLVED | See focus item 4 (`receipts/42`). |
| R381-1 F1 (15.2 incomplete: 02 boot paragraph, integrator `:334`/`:336`, operator `:202-206`, 01_overview `:170`) | RESOLVED | Rows at D3 `:2307`, `:2315`, `:2317` and `:2312` (`receipts/42`). |
| R381-1 F2 (stale pin and wiring in FASTCONNECT `:119`, `:131-133`) | RESOLVED | See focus item 2. |
| R381-1 S1, S2 (taken) | APPLIED | See focus item 5. |

## Lens results (clean lens lines carry their evidence)

```text
[R380] PASS Robustness — D3 :309-314, :621-648, :683-690, :750-761; snapshot :1093-1100; BAREMETAL_FIRMWARE :1913-1917; processor KL_acmp_nvm_shadow.sv:864-893; parent milan_baremetal.c:1068-1087 @c0723222 — DR2c error paths: bounded count (3 attempts, counted at grant; giveup at 1+RETRY_MAX_P), 500 ms/1,000 ms spacing, no bus/port held in BACKOFF, relatch without budget replenishment, taint/change priority kept, reset-only alarm, failed slot never ACKed, capture refusal distinct from media attempts; current immediate/unbounded retry stated as lane-1/lane-2 change, not as behaviour
[R380] PASS Tests — FASTCONNECT §16 checkbox states base/round-1/head identical (receipts/20); :1557-1563 oracle strengthened, not weakened; D3 §18.1 :2532-2533 and §18.2 :2587-2588 DR2c negative controls (no backoff, fourth attempt, alarm forgiveness, ACK of failed slot) each bound to a named assertion; §18.1 :2510-2512 sweep and DR2c acceptance; nine lane-0 gates rc 0 at head (receipts/30); 165 fragment links resolve (receipts/31)
[R380] MINOR Conformance — see F1
[R380] MINOR RTL — see F1
[R380] MINOR Docs — see F1
```

These artifacts were also checked under the unclean lenses and found nothing further:

- **Conformance:**
  - the register against the ruling (`receipts/11`);
  - round-2 items 2 to 6;
  - the whole-PR file list.
- **RTL:**
  - the table's processor citations at the pin (`receipts/43`);
  - the shadow retry path;
  - the arbiter and idle manager 1;
  - the DR2c FSM arithmetic.
- **Docs:**
  - the four changed pages;
  - the stale-pin search;
  - the debounce and forgiveness searches;
  - anchors.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | round-2 assignment items 1-6; ruling 5862405632 vs D3 §15.1 (receipts/11); D3 §15.2 vs processor tree (receipts/40, 41, 50); FASTCONNECT §16 states (receipts/20) | R380-2 | e796c68a460fe6946e28cb9da0349a382c868352 |
| RTL | UNCLEAN (F1) | processor `16be6768`: `gen_ucode.py`, `06_aecp_engine.md`, top `:124-130/:647-668/:2513-2546`, `KL_acmp_nvm_shadow.sv:864-893`, arb, port, guard, dyn_state (receipts/43, 50); D3 §5.1, §6.1-6.3 | R380-2 | e796c68a460fe6946e28cb9da0349a382c868352 |
| Robustness | CLEAN | D3 §6.1/6.3 DR2c error paths, rule 4, firmware transaction policy; snapshot `:1093-1100`; BAREMETAL_FIRMWARE `:1913-1917`; shadow and firmware failure paths | R380-2 | e796c68a460fe6946e28cb9da0349a382c868352 |
| Tests | CLEAN | FASTCONNECT §16 checkbox states (receipts/20); D3 §18.1/18.2 DR2c negative controls; lane-0 gates (receipts/30); anchors (receipts/31) | R380-2 | e796c68a460fe6946e28cb9da0349a382c868352 |
| Docs | UNCLEAN (F1) | the four delta pages; FASTCONNECT pin/wiring and debounce text; snapshot §12/§20/§21; D3 §15.2 rows and sweep; processor docs at pin | R380-2 | e796c68a460fe6946e28cb9da0349a382c868352 |

## Real limits

- **Manager bank receipts.** I did not find the manager's source static/builder and native bank receipts for this head in public state:
  - the evidence tree `6cf46c2a:review-evidence/70-r1` holds the round-1 author logs only (`receipts/61`);
  - no manager evidence comment was on #70 or PR #610 when I fetched them, around 04:10-04:15 UTC.

  This review does not rely on those receipts and did not run those banks.
- **Hosted checks at 04:13 UTC** (`receipts/60`):
  - executed and succeeded: `rtl-fast`, `bdd-conformance`, `changes`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `wire-accountability`;
  - still in progress: `docs-check`;
  - skipped, so not executed evidence: `verilator-suites`, `yosys-portability`, the shard jobs, `verilator-lint`, `yosys-elaboration` and `Physical gPTP`.
- **Live `dev` has moved.** It was `54ce877371ee6e8878cf67294e86c2a8481b62f6` at 04:15 UTC, not `c0723222`. That commit is not present in this clone. The final current-dev candidate therefore differs from the source base, and this review says nothing about it.
- **Documentation gates.** All nine gates were run with the repository's hash-locked renderer wheels and PyYAML 6.0.3, in a disposable environment under the packet's scratch directory. Each gate's own exit status was recorded.
- **No probes.** No simulation, mutation or probe was run, because the delta is documentation only. The scoped Verilator was not used, so its identity was not checked.
- **Milan clause text** was not re-read this round. The delta changes no clause-bearing claim.
- **No hardware.** Physical calibration was NOT RUN. No hardware was used, and nothing here is hardware proof.
- **Clone state.** The clone was left at exact head bytes. HEAD, tree and index file digest `f1f3fbc8...` are the same before and after. The index entries equal HEAD's tree, porcelain is empty, all four gitlinks are unchanged and the processor checkout is clean (`receipts/00`, `receipts/90`).

## Pending manager duties

- Publish this report and obtain R381-2.
- Have the executor address F1. After that, Conformance, RTL and Docs must be covered again at a head that includes the change. Robustness and Tests are banked at `e796c68a` unless their scope is touched.
- Wait for hosted `docs-check` to finish at the exact head, and own hosted and act acceptance.
- Publish the bank receipts for this head.
- Build and validate the current-dev candidate against live `dev` (`54ce8773` at inspection) at the merge turn.
- Later, not this lane: DR3a ratification after lane 1 measures.

R380-2 FINISHED
