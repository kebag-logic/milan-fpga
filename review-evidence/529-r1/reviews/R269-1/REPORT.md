[R269] NEGATIVE - exact head f815577559d4922c945dcf1436d4394ff2c10567

Round R269-1. External cleared-context review of issue #529 / PR #534.

- Base `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- Head `f815577559d4922c945dcf1436d4394ff2c10567`, tree `39ac12103fecf088ab5d19a494acbc43c2b35367`.
- Gitlinks (unchanged from base): protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`,
  gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`,
  third_party/verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
- Four one-line commits with no trailers, linear on the base.

## Summary

- The RTL at this head is correct. All ten `KL_crf_rx` Table 5.16 outputs are
  bound to the right root wires. The new row serves them at their IEEE Table
  7-157 quadlets under `counters_valid = 0xF3F`, which is exactly Milan v1.2
  Table 5.16. The dirty pulse reaches the processor's per-descriptor
  one-second limiter as {STREAM_INPUT, `N_STREAMS`}. AAF rows and undeclared
  indices are unchanged.
- **F1 (MAJOR)**: the root-wire tests cannot detect a permuted port binding
  at the `KL_crf_rx` instance. Six of the seven newly connected tallies can be
  swapped in pairs and every leg stays green. The docs cite these tests as
  proof of the binding.
- Five SUGGESTIONs (S1-S5). They do not affect lens coverage.
- Verdict NEGATIVE: F1 is open under Conformance, Tests and Docs. RTL and
  Robustness are covered clean at this head.

## Reconstruction

These were read in order, before any other reviewer's material:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #529: the body, the A10 assignment, and the A204 TAKEN and REVIEW
   READY comments.
3. The frozen acceptance: REGISTER_MAP "Closure criteria for the CRF Stream
   Input counter gap" 1-4 at base `ede8d48e`.
4. Milan v1.2 5.3.8.10 (Table 5.6 and its reset sentence), 5.4.2.25 (Table
   5.16) and 5.4.5.2 (Table 5.22).
5. IEEE 1722.1-2021 7.4.42.2, Tables 7-156 and 7-157.
6. `git diff ede8d48e..f8155775` and the history.
7. The processor's `KL_aecp_notify` counter-event map.
8. The public author packet `review-evidence/529-r1/author-a204`
   (RECEIPTS, HANDOFF, Yosys logs, mutant M2) at `56531731`.

Scope decisions are taken from the A10 assignment. The silicon Milan-compatible
verdict follows the merge on the bench. This lane is root wiring only.

## Findings

### F1 - MAJOR - Conformance, Tests, Docs

```text
[R269] MAJOR Conformance, Tests, Docs - hdl/milan/milan_datapath.sv:5489-5496 with tb/verilator/milan_dp/sim_nxn.cpp:3313-3329,3409-3422 - The root-wire tests cannot detect a permuted KL_crf_rx port binding
```

**Requirement and evidence**

- Frozen closure criterion 1 connects the complete bank. Criterion 4 asks
  for root-wire tests of "reset, wrap, descriptor isolation, and controller
  decoding".
- The base text said a standalone `crf_rx` pass is not evidence that the root
  serves these counters.
- The `[CTRS-CRF]` signature arm seeds each tally through its root wire name,
  `milan_datapath__DOT__crf_<x>_w` (sim_nxn.cpp:3318-3327).
- The instance is flattened in the simulated model. Receipt 18 shows that no
  port-local tally symbol exists. So seeding `crf_mrcnt_w` writes whichever
  `KL_crf_rx` flop the port map binds to that wire, and the arm proves only
  the mux. It restates the datapath's own naming.
- Only three tallies are driven by real events at the root: FRAMES_RX,
  STREAM_INTERRUPTED and SEQ_NUM_MISMATCH (the wrap arm).
- Reviewer mutants, each one pairwise swap at the instance, all stay green on
  every leg that was run (receipt 30):
  - mx1: `mr_cnt_o` with `tu_cnt_o`
  - mx2: `cnt_locked_o` with `cnt_unlocked_o`
  - mx3: `late_cnt_o` with `early_cnt_o`
- Legs and results under each of those mutants:
  - nxn: 1687/0
  - nxn8: 3115/0
  - notify: 143/0
  - main: 230/0
- Control mx4 swaps `cnt_intr_o` with `cnt_locked_o` and is red. The failing
  check is "[CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0".
- None of the author's eight recorded mutations edits the instance port map.
  Their M2 swaps the mux (quadlet 0 and 1 sources).
- The same gap covers `fmt_err_o`, whose semantic is not driven at the root.
- Repository precedent: `milan_datapath.sv:7157-7166` records "could be
  swapped at the port map and every suite would stay green" as a review
  defect that needed bench coverage.

**The docs overclaim this**

- REGISTER_MAP:846-859 maps each quadlet to a named `KL_crf_rx` output.
- REGISTER_MAP:873-877 cites the signature arm as criterion 1's evidence.
- sim_nxn.cpp:3409-3411 claims that "a permuted, truncated, missing or
  constant quadlet fails here".
- README:507-508 and :519-521 make the same claim.

**Impact**

- Suppose the binding regresses, for example in a merge or a refactor of this
  hot file. A controller would then decode MEDIA_RESET in TIMESTAMP_UNCERTAIN's
  quadlet, or LATE in EARLY's.
- It could also decode MEDIA_LOCKED and MEDIA_UNLOCKED reversed. That breaks
  Table 5.6's LOCKED = UNLOCKED or UNLOCKED + 1 invariant on the wire.
- Every gate named as #529's evidence would still pass.
- Criterion 4's "controller decoding" is therefore demonstrated for three of
  the ten counters, not ten.

**Required change**

- Each of the ten served quadlets must be shown to carry the `KL_crf_rx`
  output that REGISTER_MAP:846-859 names.
- The check must be one that a pairwise swap at the instance port map turns
  red. Examples are distinct real-event counts per counter at the root, or
  seeding through names that the port map cannot relabel. The design choice is
  the author's.
- Alternatively, the docs must stop citing the signature arm as proof of the
  binding and state the gap. The criterion 4 closure claim then has to be
  revisited publicly.

**Verification**

- Rebuild the nxn leg against `mx1`, `mx2` and `mx3` from
  `scripts/make_mutants.py` with `scripts/probe_leg.sh`. Each must turn at
  least one `[CTRS-CRF]` check red.
- The exact head must stay 1687/0.

### Suggestions

**S1 - Robustness, Tests - the `crf_sink: false` shape is unexercised**

- Location: `milan_datapath.sv:3524` and `:7206-7216`.
- `crf_sink: false` is a supported builder configuration
  (`endstation_builder.py:3792`, `:3830-3842`).
- No suite leg elaborates it. Every generated shape declares the CRF sink.
- The reviewer lint-elaborated a generated 4x4 `crf_sink: false` shape at
  this head: 0 errors, and warnings identical to the CRF shape.
- Suggested: a leg or an elaboration gate for that shape. It could grade
  STREAM_INPUT `N_STREAMS` as NO_SUCH_DESCRIPTOR, with no arbiter event.

**S2 - Tests - the one-second floor is 990 ms**

- Location: `sim_nxn.cpp:1337-1343` against the section header at
  `:1061-1062`.
- The header says "released after >= 1000 ms". `[NOTIFY-CRF]` grades
  `>= 990 ms`, because its cycle stamp skips the lever writes.
- The reviewer measured 997 ms on the stamp.
- Suggested: stamp from a monotone cycle count so that the floor can be
  1000 ms.

**S3 - Docs - config comments still point at B4**

- Location: `configs/endstation_arty_4x4.yaml:103`,
  `endstation_ax7101_8x8.yaml:153` and `endstation_arty_8ch.yaml:139`.
- They still say runtime gaps are graded in "the current audit B3 and B4".
  B4 is now closed.

**S4 - Docs - the frozen criterion wording was paraphrased**

- Location: `REGISTER_MAP.md:869-895`.
- The frozen closure-criteria wording was replaced by paraphrases. Criterion
  2's word "compact" is gone.
- The reviewer confirms the author's published reading against the normative
  text. Milan v1.2 Table 5.16 bit values are 0x1, 0x2, 0x4, 0x8, 0x10, 0x20,
  0x100, 0x200, 0x400 and 0x800. That is `0xF3F` at the IEEE offsets, and only
  Table 5.17 compacts.
- Suggested: quote the frozen text beside the resolution. The issue's pointer
  ("the REGISTER_MAP closure criteria 1-4") would then still resolve to it.

**S5 - Conformance, Docs - `Closes #529` with an open silicon item**

- `Closes #529` will close the issue at merge.
- The issue's second acceptance item (a Milan controller reports the entity
  Milan-compatible on silicon) is post-merge by A10's decision.
- Suggested: the manager records where that item is carried, for example #117
  acceptance 4, or keeps #529 open until the bench verdict.

## Clean-lens evidence

```text
[R269] PASS RTL - hdl/milan/milan_datapath.sv:1785-1796,3327-3372,3511-3560,5438-5501,7184-7301; hdl/ieee1722/crf/KL_crf_rx.sv (receipt 13); receipts 14, lint_head_crf_4x4, lint_head_nocrf_4x4 - see the notes below
[R269] PASS Robustness - milan_datapath.sv:3524-3552,7206-7299; KL_aecp_notify.sv:433-451,788-797; receipts lint_head_nocrf_4x4, leg_nxn_ma4, leg_nxn_ma6, leg_base_* - see the notes below
```

**RTL: what was checked and against what**

- The code-only diff is exactly the new row, the seven bindings, the dirty
  bind and the widened arbiter (receipt 14).
- The `KL_crf_rx` change is comment-only (receipt 13).
- The binding at 5485-5500 was checked port by port against the mux at
  3528-3543 and against Table 7-157.
- The guard `ctr_crf_w` is exclusive with `ctr_sin_w`, and it is a structural
  false without the CRF sink. The mixed-sign compare is unsigned-safe.
- `PP_CTR_SIN_N_C` sizing, the pick and clear loops and the round-robin
  re-arm were checked for 1x1, 4x4 and 8x8.
- Every new declaration precedes its first use, so no xvlog
  use-before-declaration exposure.
- There is no new clock domain or FSM.
- Lint-only elaboration is clean with and without the sink.
- Focused gates: `lint_rtl.py --check` 90<=90, `check_port_contracts` OK and
  `check_rtl_source_lists` OK (receipt 12).

**Robustness: what was checked and against what**

- Undeclared or out-of-range indices: the exact-match guard, and the
  processor's descriptor refusal at N+1.
- The wrap at 0xFFFFFFFF.
- A re-pulse while pending, and a pulse in the clear cycle. Both are absorbed.
  The processor re-reads current state at push time.
- Reset: both reset styles clear the bank and the pending bits.
- Feature-disabled: an unbound sink does not count, and `crf_sink: false`
  elaborates.
- Reads have no side effects.
- The isolation mutants ma4 and ma6 are red.

## Focus items checked

**All ten `KL_crf_rx` outputs connected**

- Yes (milan_datapath.sv:5482-5500).
- The binding is correct by inspection. F1 is about the tests, not the RTL.

**`counters_valid` and quadlet placement**

- `0xF3F` equals Milan v1.2 Table 5.16.
- Quadlets 0-5 and 8-11 match IEEE Table 7-157 offsets @0-@20 and @32-@44.
- TIMESTAMP_VALID and TIMESTAMP_NOT_VALID are unclaimed, and those quadlets
  read zero. This matches `tests/features/counters_contract_milan.feature:462-467`.
- Mutant ma1 (mask `0xFFF`) is red, with 3 checks.

**32-bit wrap**

- All seven engine tallies are 32-bit wrapping (`KL_crf_rx.sv`, unchanged
  code).
- Served full width.
- The wrap is graded at the root through real PDUs for FRAMES_RX and
  STREAM_INTERRUPTED.
- Mutant ma5 (16-bit slice) is red.

**AAF rows unchanged**

- `ctr_sin_w` and `CTR_VALID_SIN_C = 0xFFF` are untouched.
- ma4 is red: 7 `[CTRS]` checks plus isolation.
- ma6 is red: 18 checks.

**Undeclared indices**

- N+1 answers NO_SUCH_DESCRIPTOR with an empty body at the root (nxn and
  nxn8).

**Rate-limited notification**

- `KL_aecp_notify.sv:436-439` accepts STREAM_INPUT index <
  `N_STREAM_IN_P = ACMP_SINKS_C`.
- `:788-797` holds each descriptor at >= 1000 processor ms.
- `[NOTIFY-CRF]` 8/8 passes on the timed leg: withheld at 900 ms, released
  once, 997 ms on the stamp (see S2).
- ma3 (dirty removed) is red: 8 checks on notify, and the arbiter bit on nxn.
- The healthy-FRAMES_RX push exclusion inherited from `KL_crf_rx` is the
  recorded #60 decision. It is not a new deviation.

**Root-wire tests fail under mutation**

- Seven of the author's eight recorded mutations were re-derived and all are
  red (receipt 30).
- The instance-binding class is not covered: see F1.

**Resource impact**

- The author reports +1,134 generic cells (+0.07%) on `milan_datapath`.
- That is plausible for seven retained 32-bit tallies, their incrementers and
  one arm.
- Not reproduced here, because focused synthesis of this top exceeds this
  round's limits.

**Docs, compliance matrix and CHANGELOG**

- The claims are consistent with the RTL, except the binding-evidence
  overclaim in F1 and S3/S4.
- `check_em_dash` found 0 findings over 121 added lines (receipt 10).
- `docs_check` found 0, `gen_module_matrix --check` is up to date, and
  `gen_toc --check` is OK (receipt 11).

## Probes

All probes ran on the pinned simulator (5.050; receipt 01), with at most 8
jobs, in a disposable copy of the exact head. The leg recipes mirror
`tb/verilator/milan_dp/Makefile` `run`.

| Leg | Exact head | Instance swaps mx1/mx2/mx3 | Other mutants |
|---|---|---|---|
| nxn (4x4) | 1687/0 | green, green, green | mx4 red (1); ma1 red (3); ma2 red (2); ma3 red (1); ma4 red (8); ma5 red (2); ma6 red (18); ma7 red (18) |
| nxn8 (8x8) | 3115/0 | green, green, green | - |
| notify (timed 1x1) | 143/0 | green, green, green | ma3 red (8) |
| main (1x1, sim_main) | 230/0 | green, green, green | - |

In `ma7` the reader is removed. It marks the seven wires `public_flat_rw`, as
the author's recipe does.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Milan v1.2 5.3.8.10/Table 5.6, 5.4.2.25/Table 5.16, 5.4.5.2/Table 5.22; IEEE 1722.1-2021 Tables 7-156/7-157; `milan_datapath.sv:3511-3552,5482-5500,7200-7301`; `KL_aecp_notify.sv:433-451,788-797`; frozen criteria at `ede8d48e` | R269-1 | f815577559d4922c945dcf1436d4394ff2c10567 |
| RTL | CLEAN | `milan_datapath.sv:1785-1796,3327-3372,3511-3560,5438-5501,7184-7301`; receipts 13, 14, 12, lint_head_crf_4x4, lint_head_nocrf_4x4 | R269-1 | f815577559d4922c945dcf1436d4394ff2c10567 |
| Robustness | CLEAN | `milan_datapath.sv:3524-3552,7206-7299`; `KL_aecp_notify.sv:433-451,788-797`; receipts lint_head_nocrf_4x4, leg_nxn_ma4/ma6, leg_base_* | R269-1 | f815577559d4922c945dcf1436d4394ff2c10567 |
| Tests | UNCLEAN (F1) | `sim_nxn.cpp:1305-1345,3284-3493`; receipts leg_* and 30 (4 legs, 11 mutants), 18 | R269-1 | f815577559d4922c945dcf1436d4394ff2c10567 |
| Docs | UNCLEAN (F1) | `REGISTER_MAP.md:130-140,846-895`; `tb/verilator/milan_dp/README.md:502-523`; `MILAN_COMPLIANCE_MATRIX.md` 5.4.2.25 and 5.4.5.1/.2; audit B4; `REGISTER_MAP_CLASSES.md`; `FR_NFR.md`; roadmap; `ENDSTATION_BUILDER.md`; `CHANGELOG.md`; receipts 10, 11 | R269-1 | f815577559d4922c945dcf1436d4394ff2c10567 |

## Prior public findings

- They were read after the independent pass and the draft verdict.
- PR #534 has no reviews and no review comments. Its comments are the
  manager's round-start notices for R268-1 and R269-1.
- Issue #529 has no review content after REVIEW READY.
- So no prior finding exists to resolve or retain at this head.

## Real limits

- Not run by this reviewer:
  - the full milan_dp recipe (legs nxndv, nxn4c, nolpf, prune, ax1x1, aclk,
    gptp and gptplat)
  - render mutants
  - pp_shadow, milan_dp_render, crf_rx and behave
  - xvlog, `check_sv_idiom` and the HDL reference build
  - Yosys, any synthesis or timing, and act
- The resource figure is the author's. No timing evidence exists for the added
  answer arm.
- No behavioural test of the `crf_sink: false` shape exists. Only lint
  elaboration was done.
- Hosted contexts were read only (receipt 20). All seven required contexts
  report success at this head. The Verilator and Yosys shards executed.
  "Physical gPTP (nightly and manual)" is skipped. Acceptance of hosted and
  act evidence is the manager's.
- Physical calibration was NOT RUN, and field skips are not hardware proof. No
  silicon or controller verdict exists for this head.
- The manager's source static/builder and native banks for this head were not
  seen or inferred.

## Pending manager duties

- Publish the source static/builder and native bank results for this head.
- Accept the hosted and act evidence.
- Build and gate the final current-dev candidate at the merge turn. The source
  base is `ede8d48e`; live dev is `759da623`.
- Decide how the silicon acceptance item is carried when `Closes #529` fires
  (S5).
- Re-review F1's fix at the new head. Conformance, Tests and Docs must be
  re-covered there. Any change to `milan_datapath.sv` also re-opens RTL and
  Robustness.

## Clone restoration

- No tracked file in the clone was edited. All mutants and builds lived in the
  disposable copy.
- Ignored bytecode caches created by read-only script runs were removed.
- `scripts/verify_clone.sh` confirms all of the following (receipt 99):
  - HEAD and tree match.
  - Index records equal HEAD tree records.
  - There are 0 tracked blob byte or mode mismatches.
  - There is no untracked or ignored residue.
  - The three required gitlinks are at mode 160000, at their pins, with clean
    worktrees.

## Reproduce

1. `scripts/setup_scratch.sh <clean clone at head>`.
2. `VERILATOR=<pinned 5.050> scripts/probe_leg.sh <nxn|nxn8|notify|main> <dp.sv> <tag>`.
3. `scripts/lint_shape.sh`.

The mutant hashes are in receipt 15. Every published file is listed in
`MANIFEST.sha256`.

R269-1 FINISHED
