[R391] NEGATIVE - exact head 2b38d68e704e8a62fbeae8171c9195ca93728488

# R391-2: independent external review of processor PR #132 (issue #131, D3 lane 1), round 2

- **Repository.** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #132, issue #131, round R391-2.
- **Head.** Exact head `2b38d68e704e8a62fbeae8171c9195ca93728488`, tree `d11f358f887845fd5a8d9a63984b64792e0dff0e`. The PR's live head reads the same sha. Base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`.
- **Delta reviewed.** `e1ae468f..2b38d68e`, six commits: `380a3e4`, `83e708a`, `b06130d`, `85b2f6f`, `2fbe792`, `2b38d68`. It touches 22 files (+1,335 / -118).
- **Authorities.**
  - Parent contract: milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md`. It is byte-identical at `7a7582f0` and at live dev `7390b436`. I used §6.2, §6.3, §8.1 and §18.1.
  - DR3a/DR4 ratification: milan-fpga #70, comment 5873060660.
  - AECP hold-admission ruling: issue #131, comment 5873580386.
  - Round-2 assignment: issue #131, comment 5873696947.
- **Reconstruction order.**
  1. Processor README, docs/README and hdl/README. The processor repository has no AGENTS.md or CONTRIBUTING.md.
  2. The issue body, the assignment, the two rulings and the ratification.
  3. The contract sections above.
  4. `git diff c951a9ff..2b38d68e`, the round-2 delta and its per-commit history.
  5. Public evidence: milan-fpga `b657a2de` `review-evidence/pp131-r1`. From the round-2 author packet at `cb9884de` I read only `PR-BODY.md` (for the declarations) and `GATES.md`.
- **My round-1 packet.** `pp131-r391-1-packet` was read-only input.
- **Other reviews.** No private material was read. The other reviewer's round-1 findings were re-read only after the verdict, findings and ledger below were written (last section).

## Verdict

NEGATIVE. Every round-1 finding of mine is resolved at this head.

- **The DR3a aggregate is enforced.** It is derived from `CLK_HZ_P` and takes the per-wait path. My slow-but-inside probe now ends at the bound.
- **The AECP hold admission meets the ruling.** At every AECP backlog I sent (0 to 16 commands, mixed kinds, no inter-frame gap), in CLOSED and during a slowed walk, ACMP answers in the idle 168 cycles. Word 37 counts exactly the drops, and the one held command is answered byte-exact at the release.
- **The round-1 mutants are killed.** All seven of my round-1 mutants are KILLED by named checks. The in-tree driver kills 62 of 62 from the tree, with README records.
- **The consumer gates are back under their ratchets.** Port contracts: 111 <= 111. Naming: no candidate added over base.

Two new MINOR findings remain open. Both come from probing the new aggregate counter.

1. **F1 MINOR (Conformance, Tests).** Two properties of the aggregate have no killing check, although the RTL implements them and its banner states them: the counter is inert after the terminal, and it fires only with no event in hand. Each mutant passes all 7,839 pp_top checks. Yet one rolls back a COMPLETE restore at the bound, and the other wedges the NVM device face.
2. **F2 MINOR (Conformance, Robustness, Tests, Docs).** Suppose the bound falls while the D3 writer still waits for the binding walk. The restore then ends CLOSED, with AECP and the ADP enable held until reset, even for a device that meets every per-wait deadline. The integrator guide tells integrators such a device "ends the restore on defaults ... rather than holding AECP and the enable". The RTL follows the contract's literal `closed'` equation, so the terminal needs a manager ruling, and the docs and tests need to follow it.

One SUGGESTION (S1) does not affect the verdict.

## Findings

### F1 - MINOR - Conformance, Tests - the aggregate's post-terminal inertness and its no-event-in-hand firing are unguarded

- **Where.**
  - `hdl/aecp/KL_aecp_nvm_writer.sv:546-548`:
    - `agg_live_w = ... && !agg_fired_r && !done_r && !closed_r`;
    - `agg_expire_w = ... && (stall_w || !wait_w)`.
  - The same file's banner (`:58-71`, `:539-542`) promises "counted until the terminal" and "the bound fires once, in a cycle whose wait has no event in hand ... so no granted READ is orphaned".
  - The only aggregate check is D3R13 (`tb/pp_top/d3_phases.hpp:1570`), which grades the bound and its terminal.
  - The in-tree AGGREGATE mutants (`tb/pp_top/d3_mutants.py:293`) cover removal, mirroring, the start event and the per-wait floor. None of them touches either property.
- **Authority.**
  - Contract §18.1, Negative controls: "Each must fail a named ... assertion".
  - The ratification: on expiry the walk takes "the D3 terminal path the walk would take on a per-wait timeout". A per-wait deadline can fire neither after the terminal nor with its event in hand (`stall_w`).
- **Evidence.** Both mutants are in `scripts/r391_mutants2.py`. `receipts/mutants-r391-2-d3only.log` shows them surviving the D3 section (104 of 104). `receipts/mutants-r391-2-survivors-fullsuite.log` shows them surviving the full pp_top run (7,839 of 7,839). Each is a real defect when present:
  - **`agg_not_stopped_at_terminal`** (the `!done_r && !closed_r` gate removed).
    - P7 (`receipts/probe-P7-postterminal.log`, bound overridden to 2,800 in a probe copy): a restore ends COMPLETE at clock 2,698 with 27 records applied.
    - At the bound it is aborted from W_DONE: `restore_fail_o` rises with cause 3, every restored row is cleared, and the writer sits in W_RELOC.
    - The golden is unchanged at clock 20,000.
    - The P6 sweep on this mutant (`receipts/probe-P6-mutant-agg_not_stopped_at_terminal.log`) shows the same in all 508 runs that ended before the bound.
  - **`agg_fires_with_event_in_hand`** (the `(stall_w || !wait_w)` term removed). The P6 sweep on this mutant (`receipts/probe-P6-mutant-agg_fires_with_event_in_hand.log`) has 17 of 5,802 runs where the bound fell in W_RQ with the grant in hand (10 in pass 0, 7 in pass 1). The granted READ is orphaned (`m_abort_o` covers only W_RD), and a later SET is never persisted. The golden sweep has 0 such runs (`receipts/probe-P6-aggsweep.log`).
- **Impact.** Two regressions would pass every gate: one that turns the aggregate into a roll-back of a COMPLETE restore, and one that wedges the device face. The unmutated RTL behaves correctly on both counts (golden P6: 5,802 runs, 0 deviations).
- **Required outcome.** Named checks that fail on each mutant:
  - A restore that ended COMPLETE (and one that ended DEFAULTS or CLOSED) is observed past the aggregate bound with its verdicts and rows unchanged.
  - An expiry that lands with a grant (or a byte, or an answer) in hand leaves no orphaned READ, and a later SET persists.

  Both mutants join `d3_mutants.py` and its README records, KILLED.
- **Verification.**
  - `scripts/r391_mutants2.py --only agg_not_stopped_at_terminal agg_fires_with_event_in_hand` reports 2 of 2 KILLED.
  - `tb/pp_top/d3_mutants.py` kills every mutant from the tree, and the goldens pass.

### F2 - MINOR - Conformance, Robustness, Tests, Docs - an aggregate expiry while the binding walk still runs ends CLOSED for a device inside every per-wait deadline; the integrator guide says it ends on defaults

- **Where.**
  - `hdl/aecp/KL_aecp_nvm_writer.sv:546-548` fires in W_WAITGO, which has no wait (`wait_w = 0`). The abort then takes `!proven_r` to CLOSED (`:634-636`).
  - The writer banner (`:62-67`) and `docs/architecture/07_memory_maps.md:661` state this path ("the aggregate bound before the image is proven (the binding walk still running ...) | 3 | CLOSED").
  - `docs/guides/integrator.md:405-407` says the opposite: "a device slow enough to reach that bound ends the restore on defaults (`rs_cause_o` 3) rather than holding AECP and the enable".
  - `docs/guides/integrator.md:91` says "DEFAULTS, or CLOSED before the image is proven". An integrator who loaded and CRC-checked the image before `PP_CTRL[1]` would not read that as covering a slow binding walk.
  - `docs/architecture/08_timing.md:45` gives the rationale "a slow but live device must not hold AECP and the enable".
- **Authority.**
  - The ratification (5873060660) says the aggregate exists because "ADP stays gated by `restore_done_o` for that whole time". On expiry it takes "the D3 terminal path the walk would take on a per-wait timeout (roll back to DEFAULTS or CLOSED as the state requires)".
  - Contract §6.2 gives "ABORT before the image was proven: CLOSED". §6.3 gives `closed' = (abort AND (rolling OR NOT image proven))`. "Image proven" is set only in the D3 IMAGE state.
  - So the RTL matches the contract's letter. The terminal the state "requires" in WAIT-GO, before the D3 walk has started and possibly with a validated image, is not settled by any ruling.
  - Contract §18.1 requires indefinitely-delayed inputs to be graded by named checks.
- **Evidence.**
  - **P8, case A** (`receipts/probe-P8-byteslow.log`). This runs at the top's own derived deadlines: the bench clock is 1,000,001 Hz, the per-wait deadline 20,001 and the aggregate 1,000,001, with no override. The 8 default sinks each hold a saved binding. The device withholds each header byte 2,450 clocks and each payload byte 19,801 clocks (the port gathers the 8-byte header before the walk sees progress).
    - The longest binding wait is 19,802, so no per-wait deadline fires, and the binding walk runs to clock 3,325,363.
    - The D3 writer, still in WAIT-GO, ends CLOSED at exactly clock 1,000,001, cause 3.
    - At clock 6,000,006 it is still closed 1, done 0 and `own` 1, and `restore_done_o` has never risen. So the ADP enable (`entity_enable_i && restore_done_o`) cannot rise until reset, and the same device repeats this on every boot.
  - **P8, case B.** The same device slowing only the D3 walk ends DEFAULTS at 1,000,544 (rolled back, `own` 0).
  - **P6.** With a small bound, all 450 sweep runs whose expiry fell in WAIT-GO ended CLOSED (`receipts/probe-P6-aggsweep.log`).
  - **The suite never reaches this path.** D3R13's device grants each request 200 cycles inside the deadline, and its binding walk ends at 158,530 clocks.
- **Impact.** The ratification's own negative-control device, if its slowness falls in the binding walk, now leaves the entity dark with AECP held until reset, on every boot. Grant-only slowness reaches this with about 51 or more sinks; per-byte slowness with the default 8. At round 1 the same device eventually came up.
  - Practical exposure is low for a device sized per the guide (a record read well under 20 ms).
  - Even so, the integrator guide and the 08 rationale promise the opposite outcome, and no check pins the path either way.
- **Required outcome.**
  1. The manager rules the terminal for an aggregate expiry while the D3 writer still waits for the binding walk: CLOSED (the contract's literal equation), or DEFAULTS when a validated image is present and nothing was applied.
  2. The RTL implements the ruled path.
  3. `integrator.md` step 3 and the `NVM_RS_AGG_CYC_P` row, 08's T-NVM-RS-AGGREGATE rationale and 01's F01.5 row state the ruled path consistently with 07 and name the case (a binding walk that alone outlasts the bound).
  4. A named check grades an expiry while the binding walk still runs, with a mutant of that path killed.
- **Verification.**
  - `R391_P8=1 scripts/run_probes2.sh` shows the ruled terminal in case A.
  - The new check and its mutant appear in `d3_mutants.py`.
  - Re-read the listed rows.

### S1 - SUGGESTION - Tests - the admission's resident count is never decremented while it matters

The `resident_never_returned` mutant survives the full pp_top suite (`receipts/mutants-r391-2-survivors-fullsuite.log`). It ties `aecp_rx_out_w` to 0 (`protocol_processor_top.sv:2636`).

- **Why it is equivalent here.** While the hold is on, the engine takes no AECP head. With the optional external drain tied 0 (`pp_top_wrap.sv:481`, and the pop face's documented default), nothing can return an AECP slot. So the mutant is equivalent in every configuration the processor documents as normal.
- **Where it would matter.** It is observable only if an integrator uses the `aecp_txn_ready_i` / `aecp_rxs_free_i` drain during the hold.
- **Suggestion.** Note that in the banner, or grade it if that drain is ever supported.

## Round-1 findings of this reviewer, at this head

| R391-1 item | Disposition at 2b38d68e | Evidence |
|---|---|---|
| F1 MAJOR, DR3a aggregate absent | **Resolved** | See the notes below this table. |
| F2 MAJOR, held AECP exhausts the shared RX slots | **Resolved** per ruling 5873580386 | See the notes below this table. |
| F3 MINOR, four unguarded writer behaviours | **Resolved** | `receipts/mutants-r391-2-d3only.log`: `pass1_read_not_drained` is killed by "D3R5b: once the device ends the drained pass-1 READ a later SET persists (0 WRITEs, unflushed 1)"; `judge_wait_unwatched` by "D3R8b"; `rate_walk_stuck_on_first_lane` by "D3R3b entry 7"; `rate_walk_unbounded` by "D3R3b entry 8". P3/P4 behave on the golden. The in-tree driver kills the same four (`receipts/d3_mutants-intree-results.json`). |
| F4 MINOR, port-contract ratchet and unit naming | **Resolved** | `receipts/port-contract-count.log` uses the parent's own `sv_ports.py` at `7390b436`: 111 undocumented at base and at head (114 at round 1; the three writer ports gone). `receipts/naming-delta.log` uses the parent's own `measure_naming.py` scanner on the processor `hdl/`: base 22 candidates, round 1 25 (the three parameters the manager reported), head 22 with none new. `DEB_TICKS_P` became `DEB_MS_P`; 01/07/08 note the binding manager keeps `DEB_TICKS_P` for the same count. |
| S1, one conversion and two roundings | **Taken** | `NVM_RS_TMO_CYC_P = ceil(CLK_HZ_P / 50)` (`protocol_processor_top.sv:136-137`). 08 §2 states one rule, ceil(`P-CLK-HZ` × t / 1000). The bench's odd 1,000,001 Hz clock separates ceil from floor, and the `per_wait_floor` mutant is KILLED by "D3R8 deadline". |

**Notes on F1 (aggregate).**

- **The counter.** It starts at `restore_go_i`: `rs_go_i`, wired from the top at `:3613`. It is `NVM_RS_AGG_CYC_P = CLK_HZ_P`.
- **P5** (`receipts/probe-P1-P5.log`). Every D3 READ after the release is granted 19,801 late. The restore ends DEFAULTS with a roll-back at clock 1,000,544 against a bound of 1,000,001, cause 3, `own` 0. At round 1 the same stimulus ran to 63x the per-wait deadline.
- **D3R13** passes at exactly the bound. The DR3a line reports "terminal 1000000 DEFAULTS cause 3" (`receipts/pp_top-dr3a-head.log`).
- **P6 sweep.** Over 5,802 runs, the expiry falls in 12 writer states. Every run takes the documented path: CLOSED in WAIT-GO/IMG/RELOC, DEFAULTS in pass 0, a roll-back in pass 1. The expiry edge is at most 8 clocks after the bound, and every seventh run shows a later SET persisting.
- **Mutants.** `no_aggregate_deadline`, `aggregate_mirrored` and `aggregate_from_the_walk` are KILLED from the tree.
- **Docs and declaration.** 01/03/07/08, the integrator and operator guides and diagram 21 are updated. The parameter is declared.

**Notes on F2 (AECP admission).**

- **CLOSED (P1).** For n = 0, 3, 4, 5, 6, 8 and 16 AECP commands, ACMP answers in 168 cycles before, after and after again. Word 37 = n - 1, no AECP response, `own` 1.
- **Mixed traffic (P1b).** Nine frames: responses, other-entity commands and multicast. ACMP 168, word 37 = 8.
- **No inter-frame gap (P1c).** Eight AECP/GET pairs back to back: 8 of 8 GET_RX_STATE answered.
- **Slowed walk (P2).** For n = 6, 8 and 16: ACMP 168 during the walk. At the terminal exactly one held command is answered byte-exact, word 37 = n - 1, and ACMP is 168 afterwards.
- **Named controls.** D3O5 and D3O6 pass. `aecp_hold_unbounded`, `held_drop_uncounted` and `validator_admits_held_aecp` are KILLED from the tree.
- **My own admission mutants** (`hold_admits_two`, `hold_released_in_closed`, `held_gate_drops_every_subtype`, `resident_counts_acmp`) are KILLED by D3O5/D3O6. The sixth (`resident_never_returned`) is equivalent in the documented configuration (S1).
- **Structure.** The header beat commits at t_end+3, before the next frame's subtype byte can arrive (byte 14 of the next frame), so no second AECP frame can pass the gate unseen.
- **Docs.** The three corrections are made: `integrator.md:302` and the descriptor-memory row `:309`, `07_memory_maps.md` (CLOSED row and word 37), and `03_packet_engine.md` rule (d). 05 is also updated, and rule (e) states the boot-hold exception.
- **Declaration.** The counter is declared as snapshot word 37.

## Assignment items at this head

1. **The enforced 1,000 ms aggregate takes the per-wait terminal path, and a just-inside device ends at the aggregate: met.**
   - Evidence: P5, D3R13, the P6 sweep and P8 case B.
   - F1 and F2 are open against its test coverage and against the WAIT-GO terminal and its documentation.
2. **The AECP hold admission: met.**
   - At most one AECP record while held; the rest dropped and counted in word 37.
   - Non-AECP latency is unchanged (168 = idle in every case).
   - My GET_RX_STATE probes are answered in CLOSED with `RX_SLOTS_P + 2` = 6 AECP commands (and up to 16), and during a slowed restore with 6 queued (and up to 16).
   - The unbounded-gating mutant fails D3O5 and D3O6.
   - The three documentation corrections are made.
3. **Each round-1 mutant is KILLED by a named check: met.**
   - My 7 mutants, re-run at this head: the four of F3 above, plus the other reviewer's items 2-4 as I planted them. `backoff_holds_dispatch` is killed by "D3S10 backoff: 999936 owned cycles"; `disagree_whole_then_blank_only` by "D3R4b"; `rollback_strobe_one_cycle` by "D3R4 strobe".
4. **`tb/pp_top/d3_mutants.py` runs from the tree: met.**
   - From an exported copy it runs to "62 of 62 KILLED by their named checks; goldens PASS" (`receipts/d3_mutants-intree.log`, `receipts/d3_mutants-intree-results.json`).
   - All 62 names appear in the pp_top, acmp_nvm or rx_validator README mutation records. 09 §7 points to the driver.
5. **Port contracts and parameter unit naming: met** (111 <= 111; no naming candidate over base).
6. **Parent-visible changes declared: met.** `receipts/top-iface-diff.log` holds the mechanical base-to-head diff.
   - Against base: exactly five new ports (`d3_unflushed_o`, `restore_cause_o[1:0]`, `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`) and two new parameters (`NVM_RETRY_BACKOFF_CYC_P`, `NVM_RS_AGG_CYC_P`). `NVM_RS_TMO_CYC_P`'s default expression changed.
   - Against round 1: only `NVM_RS_AGG_CYC_P` is added.
   - The live PR body (Round 2 section present) and the author packet's `PR-BODY.md` declare all of these:
     - `NVM_RS_AGG_CYC_P`;
     - the per-wait ceil default;
     - snapshot word 37 (host word 0x20025);
     - the admission behaviour;
     - the aggregate terminals ("DEFAULTS or CLOSED");
     - the five round-1 ports;
     - the classifier disposition line for `protocol-processor/tb/pp_top/d3_mutants.py`.
   - F2 may change what that declaration has to say about CLOSED.

## Judgement per section 18.1 sentence (delta only)

| Sentence | Judgement at 2b38d68e | Evidence |
|---|---|---|
| Hold AECP ownership from reset through the D3 terminal | met, and it no longer starves the shared ingress | P1/P2, D3O1-D3O6 |
| Both passes, semantic validation, combined restore outputs | met | D3R1-R8b pass; the rate walk to its eight-entry bound (D3R3b) |
| Stage 1 rolls back both stores together; debt survives local roll-back | met | D3R4 (strobe at least two cycles), D3R4b, D3R10 |
| DR2c for both producers, including the binding retry backoff | met | D3S10 on the derived 500,001-clock backoff, with dispatch free while it runs; acmp_nvm E8-E11 |
| Measure DR3a per-wait and aggregate (now: enforce the ratified aggregate) | met as a bound; F1/F2 open | P5, P6, P8, D3R13 |
| Apply the processor contract table in 15.2 | met for the rows I re-read, except F2's integrator/08 statements | 01, 03, 05, 07, 08, 09, the integrator and operator guides, diagram 21, the suite READMEs; `make check`, `check-integrator-params.py` (26 = 26 = 26) and `gen_matrix.py --check` rc 0 |
| Negative controls, each failing a named assertion | met for every listed control, except F1's two aggregate properties and F2's WAIT-GO expiry | in-tree 62/62; mine 13 of 15 killed, 1 equivalent (S1), 2 surviving (F1) |
| Validation: pp_top real AECP commands, named suites, full gates | met for my focused runs | pp_top 7,859/7,859 (both builds), rx_validator 437, acmp_nvm 353, dyn_state 118, nvm_port 136, desc_mem_guard 78, desc_store 584, lsn_admit 18 (`receipts/suite-*.log`, all rc 0) |

## IEEE 1722.1 / Milan behaviour relied on

- **Dropped AECP commands.** A dropped command gets no response, and the controller retries after its AECP command timeout, as for any ingress loss. The ruling chose this over answering from undecided state. The held command's response may come later than the IEEE §9.3.2.6 bound, which 03 rule (e) now records as the boot-hold exception, bounded by the aggregate.
- **ADP.** ADP stays in its DOWN state until `restore_done_o`. With F2's CLOSED path the entity is never advertised until reset: fail-closed, as the contract accepts for CLOSED.
- **Responses.** AECP responses are unchanged (byte-exact in D3O6 and P2).

## Hosted evidence (read-only)

- At the exact head, six check runs completed with conclusion success (`docs-gates` x2, `portability` x2, `suites` x2).
- The combined commit status is `pending` with 0 statuses; only check runs are attached.
- Not relied on: hosted and act acceptance are the manager's.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | ratification 5873060660 and hold ruling 5873580386 clause by clause; contract §6.2, §6.3, §8.1, §18.1 against the writer's aggregate (`KL_aecp_nvm_writer.sv:58-71, 507-560, 628-643`), the admission (`protocol_processor_top.sv:2614-2655`, `KL_pp_rx_validator.sv:27-36, 276-282, 601`), the top derivations (`:122-150`); assignment items 1-6 | R391-2 | 2b38d68e704e8a62fbeae8171c9195ca93728488 |
| RTL | CLEAN | full read of the round-2 HDL delta (writer aggregate and its abort interplay, engine pass-through, validator gate and counter, top resident count and hold, snapshot word 37, parameter derivations); header-commit timing against the subtype gate; top port and parameter diff; port contracts (111); unit naming (0 new). F2's terminal matches the contract's literal equation; whether it must change depends on the ruling F2 asks for | R391-2 | 2b38d68e704e8a62fbeae8171c9195ca93728488 |
| Robustness | UNCLEAN (F2) | probes P1, P1b, P1c, P2 (AECP backlog 0-16, mixed, gapless, CLOSED and walk); P3/P4 (silent pass-1 read, silent judge); P5 (slow grants); P6 (5,802-run expiry sweep over 12 states, the device face re-proven after it); P7 (past the bound after COMPLETE); P8 (device inside every per-wait deadline, both walks and D3 only, derived deadlines) | R391-2 | 2b38d68e704e8a62fbeae8171c9195ca93728488 |
| Tests | UNCLEAN (F1, F2) | `tb/pp_top/d3_phases.hpp` D3O5, D3O6, D3S10, D3R3b, D3R4, D3R4b, D3R5b, D3R8, D3R8b, D3R13; `tb/rx_validator` F28; `tb/pp_top/d3_mutants.py` (62/62 from the tree); my 15 mutants (13 killed, 1 equivalent, 2 surviving the full suite); 8 focused suites re-run | R391-2 | 2b38d68e704e8a62fbeae8171c9195ca93728488 |
| Docs | UNCLEAN (F2) | 01 F01.5, 03 V10 and rules (d)/(e), 05 §5, 07 §5.3 table and snapshot text, 08 F08.1 and §2, 09 §7, integrator (parameter table, bring-up step 3, tie-off rows), operator word 37, diagram 21 SVG, the pp_top/acmp_nvm/rx_validator README mutation records; `make check`, `check-integrator-params.py`, `gen_matrix.py --check` rc 0; PR-BODY declarations | R391-2 | 2b38d68e704e8a62fbeae8171c9195ca93728488 |

## Real limits

- **Verilator.** The path named in the brief (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host, as in round 1. I used the sibling wrapper `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` (sha256 `905795b9...`). It executes a binary with sha256 `fb2cc573...` that reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/tool-identity.txt`), the same identity as round 1.
- **What I did not run.** No full processor bank, lint, Yosys, srp_top mutants, nvm_port figures, xvlog or evidence classifier, and no full parent consumer set.
- **Parent gates.** Port contracts and naming were reproduced with the parent's own parser and scanner, fetched from milan-fpga `7390b436`, over the processor `hdl/`. Their ratchet files and full-tree runs were not.
- **Not re-measured.** DR4 area and the DR2a/DR3a figures, beyond the printed DR3a lines.
- **Simulation only.** All evidence is bench simulation. The bench compresses its protocol timebase (1 ms = 100 clocks), while the NVM deadlines are derived from a nominal 1,000,001 Hz clock.
  - P6 and P7 override `NVM_RS_AGG_CYC_P` to 2,800 in a disposable copy, to sweep the expiry's position.
  - P8 adds per-byte latency to a disposable copy of the device model.
  - Physical calibration was NOT RUN, and nothing here is hardware proof.
- **Diagrams.** Checked by source text only, not re-rendered.
- **Clone hygiene.** All builds, probes and mutants ran on exported copies under this packet's `scratch/`. One reviewer action created an ignored `tb/pp_top/__pycache__/` in the clone: importing the in-tree driver to cross-check its mutant names against the READMEs. I removed it. At the end the clone was re-verified (`receipts/clone-integrity.txt`):
  - HEAD, HEAD^{tree} and the index tree equal the head;
  - all 312 work-tree blobs and modes match;
  - status, ignored files included, is empty;
  - there are no gitlinks and no `.gitmodules`.

## Pending manager duties

- Rule on F2: the terminal of an aggregate expiry while the D3 writer still waits for the binding walk. Then adjudicate F1 and F2 into round 3.
- Re-run the donor full bank and the parent consumer gates at this head and at the next one. The author reports `pp_shadow` rc 2 (PINMISSING for the five declared round-1 ports) and the evidence classifier needing the `d3_mutants.py` disposition line; both belong to the pin-adoption lane.
- Own hosted and act acceptance.
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`, live dev `7390b436`).
- Carry the parent-visible declarations into the pin-adoption lane, including whatever F2's ruling changes about CLOSED.
- Record that physical calibration is NOT RUN.

## Receipts and reproduction

Every file below is listed in `MANIFEST.sha256`.

**Scripts.**

- `scripts/run_probes2.sh <processor checkout> <scratch> <verilator dir>` exports the head, then builds and runs the probes. With no variable set it runs P1-P6. `R391_P6_MUTANT=<name>` runs the P6 sweep on one planted mutant, `R391_P7=1` runs P7 (golden and mutant) and `R391_P8=1` runs P8.
- Probe headers: `scripts/r391_probe2.hpp` (P1-P5), `scripts/r391_aggsweep.hpp` (P6), `scripts/r391_postterm.hpp` (P7), `scripts/r391_byteslow.hpp` (P8).
- `scripts/r391_mutants2.py` holds the round-1 set plus the round-2 additions. `--full` runs the whole pp_top suite.
- Gate helpers: `scripts/r391_port_doc_count.py`, `scripts/r391_naming_delta.py` and `scripts/r391_top_iface_diff.py`. They need the parent's `sv_ports.py`, `measure_naming.py` and `code_quality_scope.py`.

**Receipts.**

- Probes: `receipts/probe-P1-P5.log`, `probe-P6-aggsweep.log`, `probe-P6-mutant-*.log`, `probe-P7-postterminal.log`, `probe-P8-byteslow.log`.
- Mutants: `receipts/mutants-r391-2-d3only.log`, `mutants-r391-2-survivors-fullsuite.log`, `d3_mutants-intree.log`, `d3_mutants-intree-results.json`.
- Suites: `receipts/suite-*.log`, `suite-rc.txt`, `pp_top-d3-only-head.log`, `pp_top-dr3a-head.log`.
- Gates and integrity: `receipts/port-contract-count.log`, `naming-delta.log`, `top-iface-diff.log`, `make-check.log`, `check-integrator-params.log`, `gen-matrix-check.log`, `clone-integrity.txt`, `tool-identity.txt`.

## Other public review, round 1 (read after the above was written)

The internal reviewer's R390-1 (PR #132 comment 5873569558) was re-read here, after this round's verdict, findings and ledger were written. No other review at this head was read. Each R390-1 item is resolved or retained at `2b38d68e` below.

| R390-1 item | Disposition at 2b38d68e | Basis |
|---|---|---|
| F1 MAJOR, held AECP starves the shared ingress | **Resolved** (same defect as my R391-1 F2) | Its CLOSED scenario and its slowed-restore scenario with 6 queued are both covered: my P1/P2 show every GET_RX_STATE answered at the idle 168 cycles, and D3O5/D3O6 are the named controls. `aecp_hold_unbounded` is KILLED by both. The three statements it named are corrected: `integrator.md` (now `:302` and `:309`), the 07 CLOSED row (now in the `07_memory_maps.md:658-666` table) and 03 rule (d). ADP and MAAP passing under the hold are graded at the validator (F28); I did not probe them on the top. |
| F2 MAJOR, DR3a aggregate not implemented | **Resolved** (same as my R391-1 F1) | The counter is derived from `CLK_HZ_P`, and F08.1/F01.5/08 §2 carry the ratified values. D3R13 is the ruled control, exact at the bound; D3R8 is the per-wait boundary. The removal mutant is KILLED. Its edges are this round's F1 and F2. |
| F3 MINOR, four rules ungraded | **Resolved** | All four in-tree mutants are KILLED by their named checks (`receipts/d3_mutants-intree-results.json`): `backoff_derivation` by D3S10 timing, `backoff_holds_dispatch` by D3S10 backoff, `disagree_one_direction` by D3R4b and `rollback_one_cycle` by D3R4 strobe. My own plantings of items 2-4 are KILLED too (`receipts/mutants-r391-2-d3only.log`). The bench no longer overrides the backoff, so item 1's derivation is now timed. |
| F4 MINOR, negative controls not reproducible from the tree | **Resolved** | `tb/pp_top/d3_mutants.py` is in the tree and runs to 62 of 62 KILLED with goldens PASS. The pp_top, acmp_nvm and rx_validator READMEs carry a row for every mutant, and 09 §7 points to the driver. |
| S1 (Docs), three more parent-visible changes | **Taken** | The PR body's round-2 declarations name all three. |
| S2 (Docs, Conformance), the rule (e) exception | **Taken** | 03 rule (e) now states the boot-hold exception, bounded by the aggregate. |

My verdict and ledger above are unchanged by this reading: NEGATIVE, with F1 and F2 open; Conformance, Robustness, Tests and Docs unclean; RTL clean.

R391-2 FINISHED
