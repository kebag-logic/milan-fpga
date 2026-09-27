[R329] NEGATIVE - exact head 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e

Round R329-2 is the external independent re-review of kebag-logic/milan-fpga PR #579 for issue #502. It is a delta review.

- **Head:** `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e`, tree `06e4ce62c7c5fdabc6c9a79f9f1f47e39f94ee64`.
- **Delta judged:** `104c8a54..5d4cf33e`, which is two commits: `220c9d56` (option (a)) and `5d4cf33e` (minimal-form predicates).
- **Base:** source base `831f94f4`. My round R329-1 covered `831f94f4..104c8a54` in full.

Lenses applied this round: Conformance, RTL, Robustness, Tests, Docs (all five).

**Result:** Conformance, RTL, Robustness and Tests are CLEAN. Docs is UNCLEAN because of one MINOR finding: R329-2-F1, a stale one-line CHANGELOG statement of the superseded trigger.

- Every round-1 finding, mine and R328-1's, is closed at this head, with evidence below.
- The RTL delta is exactly equivalent for the map store.
- The new pulse is exactly the store's actual-write condition.
- Every round-1 mutant, now at the new anchor, is killed by a named committed check.

## Reconstruction

1. I read AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. I read the issue #502 decisions: 5844866872, 5845129498 and 5846418959. I also read the round-2 assignment 5848417938 (option (a), items 1-7) and REVIEW READY 5853687615.
3. I read the PR #579 body at the head.
4. Authorities:
   - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 6.1 and the section 11 table;
   - `SAVED_STATE_MATERIALIZATION.md` sections 1, 2 and 5.2;
   - the `docs/testing/TESTING.md` explicit-campaign table;
   - the processor top contract at pin `870ff88a` (`protocol_processor_top.sv:358-364`, `:660-667`).
5. I read `git diff 104c8a54..5d4cf33e` and each commit: 9 paths, and no firmware, CSR, configuration or gitlink path.
6. Public executable evidence: the author round-2 packet `review-evidence/502-r1/author-r3` on the evidence branch at `c5b80faa`. I read only the anchor adapter `adapt-reviewers.py`, its results, and the default-sweep, equivalence and priority records. Every claim I rely on was re-executed independently.

The R328-1 findings are known to me from my own round-1 report. I re-read its public text only after the verdict and ledger of this round were drafted (see "Round-1 findings").

## Verification of the assigned questions

### (1) Equivalence of the phase-5 write behaviour

**RTL delta.** The parent (`hdl/milan/milan_datapath.sv:4246-4271`) names four signals:

- `amap_edit_beat_w`, the de-duplicated held beat;
- `amap_edit_in_change_w`, the old input-branch comparison;
- `amap_edit_out_change_w`, the old output-branch comparison: word, owner valid, owner and cluster;
- `amap_edit_live_wr_p = axis_resetn && beat && phase==5 && context && (in_change || out_change)`.

The store keeps its if / else-if (`:4371`, `:4382`), and `.amap_live_wr_i(amap_edit_live_wr_p)` is connected at `:7498`. In the shadow, `aecp_live_wr_w = aecp_name_wr_w | amap_live_wr_i` (`hdl/milan/KL_pp_shadow.sv:945-946`), and the new port contract is at `:385-388`.

**Mechanical expansion.** `scripts/r329_equiv_expand.py` (`receipts/equiv-expand.log`) does the following:
- inlines the three named assigns into the head's `amap_edit_commit` block;
- deletes the head-only declarations, assigns and port connection;
- compares the whole comment-stripped token stream of `milan_datapath.sv` against `104c8a54`.

It finds 29642 against 29652 tokens and 6 residual hunks. All six are insertions:
- four are parentheses around `&&` chains (associative);
- two are the `pp_amap_edit_req_w && (...)` of `amap_edit_beat_w` in `end else if (beat)`. That branch is the else of `if (!pp_amap_edit_req_w)`, so the extra term is 1 there.

Therefore:
- the phase-5 in-key path, out-key path, priority, REMOVE handling and owner/cluster/changed updates are token-identical to the base;
- the de-dup, phase 0-4 and CSR paths are unchanged.

This agrees with the author's `resume-minimal-equivalence.log`.

**The pulse is the actual-write condition on the same edge.** In `amap_edit_commit` a store write happens exactly when all of these hold:
- `axis_resetn` is high (async reset branch not taken);
- `req && beat`;
- `case 5`;
- `(context && in_change) || (context && out_change)`.

That is literally `amap_edit_live_wr_p`, evaluated from the same registers in the same `axis_clk` cycle.
- The shadow runs on `clk_i = axis_clk` and `rst_n = axis_resetn`, so no CDC is introduced.
- The backend registers `pend_i` on that edge, per round 1 (`KL_nvm_backend.sv:755-790`).
- The `axis_resetn` term makes the port contract's "low during reset" true. It is redundant with the shadow's synchronous reset.

**In/out key exclusivity.** This is confirmed structurally:
- `amap_edit_in_key_v_w` and `amap_edit_out_key_v_w` are both cleared at `milan_datapath.sv:4081-4082`;
- each is set only inside the mutually exclusive `if (desc_type == STREAM_PORT_IN)` / `else if (desc_type == STREAM_PORT_OUT)` branches (`:4157-4164`, `:4182-4189`).

So `in_change && out_change` is unsatisfiable. The OR in the pulse cannot differ from the priority chain, and the priority is preserved anyway.

**Executable differential.** I built the `milan_dp` 4x4 `sim_nxn` leg at `104c8a54` and at the head (`scripts/r329_nxn_diff.sh`). It covers the dynamic-map T66/DMAP/#67 ADD, REMOVE, idempotent, late-invalid, cross-port, running and lock cases.
- Both runs give 1844 checks, 0 failures.
- The outputs are byte-identical apart from the header line (`receipts/nxn4x4-*.log`, `receipts/nxn4x4-diff.txt`).

**Area.** I ran single-top OOC (`syn/yosys/ooc.sh`, Yosys 0.66, `receipts/ooc-*.log`):

| top | tree | LUT | LUTRAM | LUT_TOT | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---|---|---|---|---|---|---|---|---|
| milan_datapath | 104c8a54 | 90652 | 6640 | 97292 | 43475 | 17 | 20 | 15 | 3629 |
| milan_datapath | 5d4cf33e | 89526 | 6640 | 96166 | 43475 | 17 | 20 | 15 | 3629 |
| KL_pp_shadow | 104c8a54 (R329-1 receipt) | 60766 | 6136 | 66902 | 30187 | 15 | 4 | 6 | 2104 |
| KL_pp_shadow | 5d4cf33e | 60846 | 6136 | 66982 | 30187 | 15 | 4 | 6 | 2104 |

This reproduces the reported deltas exactly: datapath -1126 LUT and shadow +80 LUT, with every other column identical.
- The token proof shows the RTL behaviour is identical, and the 4x4 differential shows identical executable behaviour. The datapath reduction therefore comes from the synthesis flow's structural sensitivity to how the same expressions are written, not from lost behaviour.
- In the shadow OOC, `amap_live_wr_i` is a free input where it used to be an internal gate. The +80 is mapping variance of the same kind.
- No timing claim is made or checked.

### (2) Round-1 mutants and probes, rerun unchanged

**Tools.** Verilator 5.050 (`receipts/tool-identity.txt`). The scripts `r329_mutants.py` and `r329_probe.py` are byte-identical to my round-1 publication: sha256 `3aeb65eb...` and `378391e9...`. The author's copies carry the same hashes.

**Unchanged campaign** (`scripts/r329_campaign.sh`; `receipts/mutant-campaign.txt`, `receipts/mutants/unchanged.*`):
- control: dyn 263/0, static 173/0;
- M3 (no pulse bypass): FAIL dyn 12 and static 8, on named `pending_from_accepting_edge` / `no_durable_claim_over_unsaved` checks, including `K12 remove input/output`;
- M7 (no sticky): FAIL dyn 29 and static 19;
- M1, M2, M4, M5, M6, M8, M9 and M10: `REFUSED anchor count 0`. The map term is now a port, so a stale anchor is a refusal, never counted as a kill.

**Anchor adapter.** `scripts/r329_mutants_adapter.py` rebinds only the old LIVE anchor to the new line. It keeps every round-1 replacement expression byte-for-byte; an in-script check printed ANCHOR-ONLY for each. It also adds round-2 variants U1, U5, U6, U8 and U11 that re-express each defect class on the shipping input.

The author's `adapt-reviewers.py` (sha256 and text in `receipts/adapter-comparison.txt`) also only rebinds entries whose anchor equals `LIVE`, with the replacement kept. **Confirmed: it changes only anchors.** Its published results match mine for all 16 mutant-legs, down to the failure counts.

| mutant | dyn | static | killed by (named committed checks) |
|---|---|---|---|
| M1 drop map | FAIL 20 | FAIL 10 | K12 input/output/remove `no_durable_claim_over_unsaved`, `pending_from_accepting_edge`, sticky |
| M2 drop name | FAIL 13 | FAIL 11 | K10 durability/accepting-edge/sticky |
| M4 phase 2 | FAIL 16 | FAIL 8 | K12 ADD/REMOVE accepting-edge, duplicate and zero-record sticky |
| **M5 phase 4** (R329-F2 = R328-F1) | FAIL 8 | FAIL 4 | **`K12 refused record input/output sticky_pending_PP_STAT/_PP_NVM_STAT`**, duplicate sticky |
| **M6 add-only** (R329-F1) | FAIL 14 | FAIL 7 | **`K12 remove input/output no_durable_claim_over_unsaved`, `pending_from_accepting_edge`, sticky** |
| M8 input ports only | FAIL 12 | FAIL 2 | K12 output ADD/REMOVE (dyn); duplicate (static) |
| M9 any phase | FAIL 12 | FAIL 8 | refused-record, duplicate, zero-record, static-refused sticky |
| M10 late mark | FAIL 12 | FAIL 8 | K10/K12 durability and accepting edge, including REMOVE |
| U1 drop map (new input) | FAIL 20 | FAIL 10 | as M1 |
| U5 shipping + phase-4 | FAIL 8 | FAIL 4 | `K12 refused record input/output` sticky |
| **U6 shipping, REMOVE gated off** | FAIL 10 | FAIL 5 | **only** `K12 remove input/output` durability, accepting edge and sticky, plus `K commit preserves unmaterialized pending` |
| U8 shipping, input ports only | FAIL 10 | PASS (no dynamic output in this leg) | K12 output ADD/REMOVE |
| **U11 104c8a54 trigger (req && phase 5)** (R329-F3) | FAIL 4 | FAIL 2 | **only** `K12 duplicate input/output sticky_pending_*` |

**Parent-side mutants** of the new derivation (`scripts/r329_dp_mutants.py`, `receipts/dp_mutants/*`). Each changes only the `amap_edit_live_wr_p` assign; the store branches are untouched.
- D1 (pulse without out_change): dyn FAIL 10 on the K12 output ADD/REMOVE checks; static PASS, because that leg has no dynamic output.
- D2 (pulse without in_change): FAIL 10 in each leg on the K12 input ADD/REMOVE checks.
- D3 (pulse on every phase-5 record): FAIL dyn 4 and static 2, on only the duplicate sticky checks.

So the committed suite constrains both the shadow consumption and the parent derivation.

**Probe, run unchanged** (`receipts/probe/summary.*.txt`, `probe.*.log`):
- **Shipping, 295 checks, 0 failures:**
  - P1: REMOVE from a durable baseline passes, with pending from the accepting edge.
  - P2: the refused ADD (stream 7) returns status 7 with pending clear.
  - **P3: `duplicate ADD status 0, phase-5 records 1, marks 0, mappings after 1, PP_STAT[11] pend 0, durable 1`.** Pending stays clear for an unchanged duplicate.
- **Mutants:**
  - M6 and U6 fail P1 with 0x605B falsely-durable cycles.
  - M5 fails P2's sticky checks.
  - U11 fails only P3's durable-baseline checks and reports pend 1, the round-1 behaviour.

**Committed controls exist in both legs** (`sim_main.cpp:1442-1479`, `:1499-1511`; tallies in `receipts/pp_shadow-default.log`). Each starts from its own `pending_boot` durable baseline.
- **Refused at record validation:** `K12 refused record input` (stream 0x7fff, status 7, map empty, pending clear) runs in all four builds. `... output` runs on the dynamic fixture.
- **REMOVE:** `K12 remove input/output` uses a CSR preload with `K12 preloaded baseline durable`, then checks durability, accepting edge and sticky.
- **Duplicate:** `K12 duplicate input/output` checks SUCCESS, a map count of 1 with the exact record, `live_state_changed` 0 and sticky pending 0.
- The static builds keep `K12 static output refused`.

**Default run:** `make -C tb/verilator/pp_shadow` gives 575 + 575 + 575 + 263 checks, 0 failures, and `make pending-mutant` gives `PASS: late-mark mutant killed by K10 and K12; clean control passes` (`receipts/pp_shadow-default.log`, `receipts/pending-mutant.log`).

### (3) Observer anchored on live state

`pending_live_state()` (`sim_main.cpp:292-302`) snapshots:
- the name RAM `u_store.name_r`;
- `amap_in_store_r`, `amap_out_owner_v_r`, `amap_out_owner_r` and `amap_out_cluster_r`;
- `cmap_flat_w`.

It does so before (`:307`) and after (`:328`) every edge. A difference starts the unsaved interval, and the trigger-derived start was removed. Watching starts in `inject_rx` before the first command byte (`:744`), so boot and CSR preloads stay outside the interval. The probes are read-only `public_flat_rd` (`pending_probes.vlt`).

The oracle is non-tautological:
- U6, M6 and D1/D2 are caught through storage changes without pending;
- U11 and D3 are caught through pending without a storage change (`live_state_changed` 0 against sticky 1).

`pending.maps` still counts raw phase-5 beats, but only against literal expected counts.

### (4) Documentation

- `KL_pp_shadow.sv:934`: "The parent shares its actual write enable; unchanged maps raise nothing."
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 6.1 (`:961`, `:968-971`) names `amap_live_wr_i`/`amap_edit_live_wr_p`, the shared conditions, the input priority and "Unchanged duplicate records produce no pulse". The section 11 row (`:1263`) reads "actual phase-5 map write enable".
- `SAVED_STATE_MATERIALIZATION.md`:
  - section 1 (`:128-134`) now names the three `pend_i` sources and the head triggers;
  - the table rows (`:145-146`) cite `amap_edit_commit` and the sticky pulses;
  - section 2 (`:224-247`) states the duplicate and refusal behaviour;
  - section 5.2 (`:485`) names `aecp_live_pend_r`, which exists (`KL_pp_shadow.sv:957`).
- `TESTING.md:268` lists `make -C tb/verilator/pp_shadow pending-mutant`, with the files whose change requires it.
- `tb/verilator/pp_shadow/README.md:53-92` matches the committed controls and the observer.
- A search of the RTL, both design pages, TESTING.md, the pp_shadow tree and CHANGELOG.md finds no "conservative" or "conservatively" wording.
- **Exception:** `CHANGELOG.md:39` still describes the superseded trigger (R329-2-F1).
- The PR body is accurate on controls and results. Its status line is stale (R329-2-S1).
- `SAVED_STATE_MATERIALIZATION.md:460` and `:2117` are the future record writer's proposed trigger in sections 5.1 and 15. They are not the #502 pending source, and I raise nothing there.

### (5) Firmware, capture, sweep and gates

**Firmware and scope** (`receipts/firmware-and-scope.log`):
- `git diff 104c8a54..5d4cf33e` and `831f94f4..5d4cf33e` over `sw hdl/common/csr configs` are empty.
- The firmware blob is `a4e560fb...` at all three commits. Its sha256 `0bf43cd4...` equals `product_firmware_sha256`.
- `check_nvm_capture.py` passes.
- The gitlinks are unchanged, with `protocol-processor` at `870ff88a`.
- `KL_pp_shadow` has a single instantiation (`milan_datapath.sv:7393`), so the new input is connected everywhere.

**Gates.** All 23 gate commands exited 0 in a clean disposable copy (`scripts/r329_gates.sh`, `receipts/gates.log`); the Markdown gates used a private venv from `tools/markdown/requirements.txt --require-hashes`:
- `git diff --check` against `831f94f4` and against `104c8a54`;
- `docs_check`, `check_em_dash --base 831f94f4`, `check_doc_style`, `gen_toc --check`/`--verify-anchors`, `check_doc_paths`;
- `gen_module_matrix --check`, `check_rtl_source_lists`, `check_sv_idiom`, `lint_rtl --check`;
- `check_cpp_idiom`, `check_py_idiom`, `check_port_contracts`, `measure_naming --check`, `measure_test_evidence --check`, `ci_events --check`, `xvlog_gate --check`;
- `check_submodule_docs`, `check_diagram_pngs`, `submodule_boundaries.gen.py --check`, `check_nvm_capture`.

**Default sweep.** I did not rerun it; the full bank is out of my scope. The author's receipt `resume-default-sweep.log` shows 55/55 suites, 2125319 checks, 0 failures, and 4 declared tsn-gen skips contributing 0. I independently reran the two suites the delta touches (pp_shadow, and the milan_dp 4x4 leg), which reproduce as above.

## Findings

### R329-2-F1 MINOR - Docs - `CHANGELOG.md:39` - the changelog still states the superseded "every commit beat" map trigger

**Authority.**
- Decision 5848417938 (option (a)): "The map pending source rises only on a phase-5 record that the datapath actually writes ... An unchanged duplicate then raises nothing".
- AGENTS section 6 Docs: "Changed contracts are reflected in authoritative docs".
- `docs/README.md:102` lists CHANGELOG.md as the current changelog.

**Evidence.**
- The #502 entry still reads "Accepted map commit beats raise the same sticky source." It was written for `87e263fd`, and neither round-2 commit touches CHANGELOG.md.
- In this repository's own vocabulary a commit beat is every phase-5 record, including unchanged ones. `SAVED_STATE_MATERIALIZATION.md:2117` says "An edit that changes nothing still raises commit beats".
- At the head, an accepted duplicate commit beat raises nothing: committed `K12 duplicate input/output`, probe P3 pend 0. Mutants U11 and D3, which make every commit beat raise pending, are killed.
- So the changelog asserts the exact behaviour the round-2 decision removed, while the RTL, design pages, README and PR body all state the delivered behaviour.

**Impact.** A reader of the current changelog concludes that re-sending an existing mapping marks state unsaved until reset. That is the over-report R329-F3 raised and the maintainer rejected. It is a documentation-accuracy defect only; behaviour and tests are correct.

**Required outcome.** The #502 CHANGELOG entry states the delivered source: accepted map writes that change the parent's map raise pending, and an unchanged duplicate does not. It must no longer claim that every commit beat does.

**Verification.** Read `CHANGELOG.md` at the corrected head against `milan_datapath.sv:4269-4271`, and confirm the docs, em-dash, style and TOC gates pass.

### R329-2-S1 SUGGESTION - Docs - PR #579 body, "Status" section - stale publication sentence

The live PR body says "This body is prepared locally and has not been applied to the PR." It is the applied body. Deleting the sentence would stop a cold reader from wondering which body is authoritative. This is optional.

There is no BLOCKER or MAJOR finding.

## Clean-lens evidence

`[R329] PASS Conformance - milan_datapath.sv:4246-4271,4371,4382,7498; KL_pp_shadow.sv:385-388,945-946 @5d4cf33e - option (a) of 5848417938 checked:`
- the map source is the store's actual-write condition;
- the name source and the accepting-edge property are unchanged;
- an unchanged duplicate, a record-validation refusal and zero-record/static refusals raise nothing, and changed ADD/REMOVE raise pending on the write edge;
- evidence: committed K12 controls in both legs, probe P1-P3, and the token equivalence against `104c8a54`;
- firmware, CSR, configuration and pins are unchanged.

`[R329] PASS RTL - milan_datapath.sv:4054-4271,4282-4422,7393-7498; KL_pp_shadow.sv:385-388,930-957 @5d4cf33e - checked:`
- the phase-5 store is token-identical to `104c8a54` after expansion (`receipts/equiv-expand.log`);
- in/out key validity is structurally exclusive (`:4081-4082`, `:4157`/`:4182`);
- the pulse is on the same `axis_clk` edge and in the same reset domain, low in reset, with no CDC and a 1-bit width;
- there is a single instantiation;
- the 4x4 map-edit differential is byte-identical (1844 checks);
- OOC: datapath -1126 LUT and shadow +80 LUT, other columns identical, explained by equivalent logic;
- lint, SV idiom and port-contract gates pass.

`[R329] PASS Robustness - sim_main.cpp:1442-1479 @5d4cf33e; receipts/probe/*; receipts/mutants/* - checked:`
- malformed record (stream 0x7fff and 7, status 7) with pending clear, in both directions;
- REMOVE and duplicate from a CSR-preloaded durable baseline;
- zero-record, static-refused, repeated SET_NAME and held-beat de-dup (`amap_edit_beat_w`);
- reset separating every scenario (`pending_boot`), and snapshot ACK not retiring pending;
- configuration dependence: static and dynamic output legs.

`[R329] PASS Tests - tb/verilator/pp_shadow/{sim_main.cpp:266-340,744,1374-1515, pending_probes.vlt, pending_mutant.py:40, README.md} @5d4cf33e - checked:`
- 38 executed mutant legs: 6 unchanged-script legs (control, M3, M7), 26 adapter legs (13 mutants) and 6 parent-side legs (D1-D3).
- Every mutant is killed in each leg where its defect is observable. The only static-leg survivors, U8 and D1, alter only the dynamic-output path, which the static leg lacks. The dyn leg kills both.
- Each round-1 finding's mutant is killed by the named check the finding asked for: M6/U6 by `K12 remove *`, M5/U5 by `K12 refused record *`, U11/D3 by `K12 duplicate *`.
- The observer is anchored on storage, not triggers.
- The default run passes (575x3 + 263), and pending-mutant passes.

The Docs lens is UNCLEAN (R329-2-F1). Clean within Docs:
- section 6.1 and the section 11 row;
- MATERIALIZATION sections 1, 2 and 5.2;
- the TESTING.md row;
- the pp_shadow README;
- the RTL comment;
- the PR body controls and results text.

## Completion ledger (reviewer-owned)

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | decision 5848417938 items 1-7; `milan_datapath.sv:4246-4271,4371,4382,7498`; `KL_pp_shadow.sv:385-388,945-946`; processor top :358-364; probe P1-P3; committed K12 controls; firmware/scope receipt | R329-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| RTL | CLEAN | `milan_datapath.sv:4054-4271,4282-4422,7393-7498`; `KL_pp_shadow.sv:385-388,930-957`; token-expansion proof; 4x4 nxn differential base/head; OOC datapath and shadow at 104c8a54/head; lint/idiom/port gates | R329-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| Robustness | CLEAN | `sim_main.cpp:1327-1352,1442-1515`; refused/duplicate/REMOVE/zero-record/reset/held-beat paths; probes P1-P3; mutants M5/M6/U5/U6/U11/D1-D3 | R329-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| Tests | CLEAN | `sim_main.cpp:266-340,744,1374-1515`; `pending_probes.vlt`; `pending_mutant.py`; pp_shadow default and pending-mutant receipts; unchanged + adapter campaign (32 legs, 8 refusals); parent-side mutants (6 legs); author adapter comparison | R329-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| Docs | UNCLEAN (R329-2-F1) | `CHANGELOG.md:35-44`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:950-975,1263`; `SAVED_STATE_MATERIALIZATION.md:125-146,224-247,460,485,2117`; `TESTING.md:266-268`; `tb/verilator/pp_shadow/README.md:51-92`; `KL_pp_shadow.sv:905-935`; PR #579 body | R329-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |

## Round-1 findings: closed or retained at this head

- **R329-F1 (MINOR, Tests/Robustness; REMOVE never observed from a durable baseline, M6 survived): CLOSED.**
  - `K12 remove input/output` (`sim_main.cpp:1472-1478`) runs from a CSR-preloaded durable baseline.
  - M6 is killed in both legs by `K12 remove * no_durable_claim_over_unsaved / pending_from_accepting_edge / sticky`.
  - U6 (the REMOVE-only defect on the shipping input) is killed only by those checks.
- **R329-F2 = R328-F1 (MINOR, Tests/Robustness; no refused-at-validation control, phase-4 trigger survived): CLOSED.**
  - `K12 refused record input/output` (`:1451-1457`) grades status 7, an empty map and pending clear.
  - M5, which is the same expression as R328's `phase4_validate`, is killed in both legs by the refused-record sticky checks. U5 is killed likewise.
  - The author's published replay of R328's script (`r328-reanchored-results.txt`: `phase4_validate static=KILLED(4) dynamic=KILLED(8)`) agrees. I did not rerun R328's script; that is R328's round.
- **R329-F3 = R328-S1 (unchanged duplicate sets pending until reset): CLOSED by option (a).**
  - P3 reads pend 0, durable 1.
  - The committed `K12 duplicate input/output` controls assert a clear pending bit and no storage change.
  - U11 (the `104c8a54` trigger) and D3 are killed only by those checks.
- **R328-F2 (MINOR, Docs; stale MATERIALIZATION section 1 and 5.2): CLOSED.** The section 1 prose and table and the section 5.2 register name are correct at the head, as in (4).
- **R328-F3 (MINOR, Docs; campaign missing from TESTING.md): CLOSED.** `TESTING.md:268`.
- **R328-S2 (SUGGESTION, Tests; observer anchored on triggers): CLOSED.** The observer is anchored on live storage, as in (3).
- **R328 oracle totals:**
  - The PR body and REVIEW READY now state them as two totals: static 138 and dynamic 193, zero failures in each, with 10/14 explicit assertions. They are not a fraction.
  - The author's `resume-r328-oracle-driver.log` tail shows `193 checks, 0 failures` for the dynamic leg.
  - I did not rerun R328's oracle. My own committed-observer, probe and mutant evidence covers the same property.

Open set at this head: MINOR R329-2-F1 and SUGGESTION R329-2-S1.

## Real limits

- **Simulator path.** The assigned `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a private copy of the identical wrapper (sha256 `905795b9...`) from `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`. It reports `Verilator 5.050 2026-07-01 rev v5.050`, `verilator_bin` sha256 `44898b22...` (`receipts/tool-identity.txt`).
- **Not run:**
  - the full parent/PP/gPTP/Yosys/builder banks and the default 55-suite sweep (the author's receipt is cited, not reproduced);
  - nvm_backend, nvm_cosim and behave;
  - the no-git docs mode;
  - R328's own scripts and oracle;
  - act/Docker and the hosted contexts.
- **Area.** Only single-top OOC of `milan_datapath` (at both commits) and `KL_pp_shadow` (at the head) was run. The `104c8a54` shadow row is my round-1 receipt, included as `receipts/ooc-104c8a54-KL_pp_shadow.round1.log`.
- **Differential scope.** Only the 4x4 `sim_nxn` leg. The 1x1, divergent, 8x8 and other `milan_dp` legs were not rerun.
- **Hosted snapshot** (`receipts/hosted-snapshot.txt`, 07:50Z): exact-head runs completed successfully, including `rtl-fast`, docs, `elaborate`, `wire-accountability`, `full-ci-gate`, Verilator shards 0, 2, 3 and 4, and Yosys shards 0-3. Verilator shard 1/5 was in progress. The physical gPTP job was skipped, which is not hardware proof. Hosted acceptance is the manager's.
- **Hardware.** No hardware or physical calibration was run.
- **Out of scope.** The firmware channel-map CSR path still writes the live map without pending. It is pre-existing and firmware-owned, as in round 1.
- **Receipt redaction.** Container-store paths in receipts are redacted to `<container-store>`.

## Clone integrity

- All builds, mutants, probes, gates and OOC runs ran in disposable copies under the packet's `scratch/`. The review clone was never edited.
- `scripts/r329_restore_check.sh` (`receipts/restore-check.log`) reports RESULT OK:
  - HEAD `5d4cf33e...` and tree `06e4ce62...` are exact;
  - index equals HEAD and the worktree equals the index;
  - there are 0 untracked or ignored entries;
  - every tracked blob rehashes to its index id;
  - the gitlinks `protocol-processor@870ff88a`, `gptp-processor@5dce647a` and `third_party/verilog-axis@48ff7a7e` are recorded, checked out and clean.

## Pending manager duties

- Route R329-2-F1 (one CHANGELOG line) to the executor. A re-review at the corrected head must re-cover Docs.
- If only CHANGELOG.md changes, nothing within the other lenses' scope is touched. The four CLEAN lenses at `5d4cf33e` then remain banked for a head descending from it.
- Hosted/act acceptance at the exact head, including the in-progress Verilator shard.
- The current-dev candidate merge (source base `831f94f4`, live dev `8c8e7bb0`) and post-merge containment.
- Maintainer merge authorization.

R329-2 FINISHED
