[R285] NEGATIVE - exact head c593cbeffaffa647cda70fb1a233455bf9c80d55

# R285-1: external review of PR #549 (Relates to #530)

- Round: R285-1, external, cleared context.
- Head: `c593cbeffaffa647cda70fb1a233455bf9c80d55`, tree `6459e8f0866f9a807d01d7dc325997c3a4e4e938`.
- Source base: `50e78097564244c124e1ec30dd8821f83951ab06` (five commits on it).
- Protocol processor gitlink at head: `09f9bf3846511f8388d995126502ed92eaa65213`.
- Verdict: NEGATIVE, on two open MINORs.
  - F1 (lenses RTL and Docs): found independently. It matches R284-1 F1.
  - F2 (lens Docs): retained from R284-1 F2 after an independent check at this
    head.
- The behaviour is right. Items 1 and 2 are fixed and item 3 is explained.
  All three reproduce in simulation. Both MINORs are prose: one describes a
  shaper this wrapper does not have, and one still names the pre-#530 gate.

## Reconstruction (public state only)

- Contract: AGENTS.md, CONTRIBUTING.md, docs/README.md.
- Issue #530 body. Acceptance: root cause for items 1 and 2, a simulation
  reproduction and a fix; a silicon rerun; item 3 explained by the documented
  semantics or fixed.
- Decisions on #530:
  - A205 DECISION 5797078565 and BLOCKED 5797083855.
  - Manager DECISIONs 5797128389 and 5798177316.
  - Assignment 5806344022.
  - A229 REVIEW READY 5807302041.
- The assignment sets the scope for this lane:
  - adopt processor main `09f9bf38` under the exact-reviewed-head rule;
  - item 1: a simulation with a failing arm;
  - item 2: every talker gate follows ACTIVE, reproduced and fixed with a
    failing arm;
  - item 3: explained or fixed;
  - the PR Relates to #530, and the issue closes after the silicon rerun.
- PR #549 body, and `git diff 50e78097..c593cbef` with its five commits.
- Authorities read:
  - Milan v1.2 5.3.7.2, 5.3.7.3, 5.3.7.7 Table 5.4 and 5.3.8.10.
  - IEEE 802.1Q-2014 10.7.5.20 (with its NOTE), 10.8.2.6 and 10.8.2.8.
  - Processor sources at the pin:
    - `protocol_processor_top.sv:498-506`, the ACTIVE and raw-verdict ports.
    - `KL_srp_top.sv:416-445`, `:772-781` and `:848-862`, the optimistic window.
    - `KL_srp_admission.sv:91-163`, the one-source-per-cycle walk.
    - `KL_srp_talker_fsm.sv:25-41`, `:612-640` and `:793-803`: ACTIVE, the Milan
      4.2.7.2.2 rLv deviation (Δ13), and the per-type LeaveAll lanes.
- Public evidence tree `a146bb36`, `review-evidence/530-r1`: it holds only the
  author packet (receipts, arms, scripts).
  - I found no manager bank receipt in that tree or in any issue or PR
    comment. The manager's bank result is taken as the manager's statement;
    this round does not rely on it.

## Findings

### F1: MINOR (lenses RTL, Docs): new text says a shaper budgets the raw verdict, and no shaper exists

- **Where the PR added it:**
  - `hdl/milan/milan_datapath.sv:6595-6598`: "The shaper keeps the RAW
    verdict: it budgets every admitted declaration, licensed or not, which is
    the conservative side of the gate above."
  - `hdl/milan/milan_datapath.sv:6565-6577`: the OPENING EDGE corner. It says
    "the first frames leave against a Sigma at most three rounds stale".
  - `hdl/milan/milan_datapath.sv:6588-6592`: the invariant "HOLDS on the
    closing edge". The invariant is "no stream ever transmits against a slope
    the shaper has not budgeted".
  - `CHANGELOG.md:39`: "The CBS slope enable keeps the raw verdict."
  - The PR body: "Known limitations" and the item 2 table row.
- **What the tree says instead:**
  - `milan_datapath.sv:634-651`: "NO GENERAL-DATA TX CHAIN". The 802.1Qav CBS
    shaper left this wrapper, and every product source joins the TX trunk after
    the point the shaper occupied.
  - `milan_datapath.sv:6751-6754`: "HONEST BOUND: neither AAF nor CRF is
    credit-shaped."
  - `hdl/common/csr/milan_csr.sv:20-27`: the CBS window has been write-only
    scratch since `0x0002_0056`.
  - `docs/reference/FR_NFR.md:208-209`, in a paragraph this PR edits: "the
    classifier/CBS chain is not instantiated".
  - Where the two signals go:
    - `lwsrp_slope_en` goes only to `LWSRP_STATUS[9]` (`milan_datapath.sv:2502`).
    - `lwsrp_idle_slope` goes only to `LWSRP_SLOPE` `0x698` (`:2507`,
      `milan_csr.sv:2333`).
    - No other consumer exists in `hdl/`, `sw/` or `syn/` (searched).
- **Impact:**
  - The PR states its one new corner in terms of a shaper budget. The
    manager's brief repeats it: "ACTIVE may open before the shaper budgets a
    fresh declaration". No shaper budget exists.
  - What the corner really does, from the processor sources:
    - ACTIVE can lead the raw verdict by at most three admission rounds. Each
      round takes N_SOURCES cycles, so the lead is tens of cycles.
    - It happens only when a Listener Ready is already registered at a fresh
      (re)declaration.
    - Its only visible effect is ordering. `LWSRP_STATUS[8]` and the gates can
      rise before `LWSRP_STATUS[9]` and `0x698` include the stream.
    - If the round then refuses the stream, ACTIVE falls inside that window,
      and the talker swaps to Talker Failed.
  - A reader of the new text will believe three things that are false:
    - that class-A AAF and CRF traffic is credit-budgeted by `sum_r`;
    - that keeping the raw verdict on "the CBS slope enable" is a conservative
      bandwidth choice;
    - that the risk to judge is bandwidth, not status-bit ordering.
  - The PR also contradicts itself: its own FR_NFR paragraph says the CBS
    chain is not instantiated.
- **Required outcome:**
  - The `milan_datapath.sv` SRP block comment and `CHANGELOG.md:39` say that
    no shaper consumes the slope in this wrapper.
  - They name the real consumers: `LWSRP_STATUS[9]` and `LWSRP_SLOPE` `0x698`.
  - They state the corner's real effect, in the words above or equivalent.
  - The PR body's limitation line matches.
  - The RTL does not change.
- **Verification:**
  - A reviewer reads the new text at the corrected head against
    `milan_datapath.sv:634-651` and `:6751-6754` and `FR_NFR.md:208`.
  - `docs_check`, `check_em_dash --base 50e78097` and `rtl-fast` stay green.

### F2: MINOR (lens Docs): an authoritative page still names the raw verdict as the stream gate (retained from R284-1 F2)

- **Where:**
  - `docs/traceability/ieee8021q.md:85`, row Q-9: "`srp_sr_admitted_o` is the
    per-source stream gate".
  - The PR edits the same page at `:35`, which now says "`srp_active_o` as the
    per-source stream gate since #530". It also edits MRP-4 and MRP-5, but
    leaves Q-9 as it was.
  - Secondary: `docs/reference/EGRESS_QUEUE_MAP.md:66-71`, "Credit-based
    shaping". This PR does not change it. It says "Opening a source and
    accounting its slope occur on the same admission-round edge ... no stream
    can transmit against an unbudgeted slope".
    - The page header (`:3-12`) scopes the chain as not instantiated.
    - The gate is no longer the admission verdict, so the opening-edge sentence
      no longer holds in the optimistic corner. Fix it together with F1.
- **Authority:**
  - AGENTS.md section 6, Docs lens: "Changed contracts are reflected in
    authoritative docs".
  - The gate contract changed at `milan_datapath.sv:6594`.
- **Evidence:**
  - I read both pages at this head.
  - `git diff 50e78097..HEAD` leaves `EGRESS_QUEUE_MAP.md` unchanged.
  - A search of `docs/{traceability,reference,testing,design,overview,fpga,integration}`
    for `sr_admitted` finds only Q-9 still naming it as the stream gate.
- **Impact:** one traceability page gives two contradicting answers about
  which processor output gates emission.
- **Required outcome:**
  - Q-9 names `srp_active_o` as the stream gate, or keeps only the admission
    (75 %) subject.
  - The EGRESS_QUEUE_MAP sentence is scoped or given the caveat, consistent
    with F1.
- **Verification:**
  - At the new head, a search of the docs finds no current-tense claim that
    `sr_admitted` is the stream gate.
  - The docs gates stay green.

### S1: SUGGESTION (lens Tests): the t>0 AAF gates are covered only by the source text

- Where: `hdl/milan/milan_datapath.sv:2019-2025` and
  `docs/testing/TESTING.md:266`.
- Nothing grades the t>0 AAF gates by behaviour:
  - `obj_crflic` elaborates the AX7101 1x1 shape, where `N_STREAMS = 1`, so
    `g_aaf_stream_en` builds nothing.
  - The multi-stream `nxn` legs tally 1708/0 at the base datapath and at the
    head (author receipts `30-base-nxn.log` and `52-final-nxn.log`). They do
    not tell ACTIVE from the raw verdict.
- What does guard them: the BDD pin of `lwsrp_stream_gate` (probed below) and
  the fact that each t>0 term reads `lwsrp_stream_gate[gs]`. That is adequate
  for this change.
- A mutant of line 2024 would survive every current gate. So the TESTING.md
  row, which lists `aaf_stream_en_raw_w` among the guarded sites, overstates
  what `crflic-mutants` can reach for index > 0.
- Optional outcome: either say "index 0 only" in that row, or add a t>0 arm on
  a multi-stream shape.

### S2: SUGGESTION (lens Docs): a stale term and an unstated pin scope

- `milan_datapath.sv:1994` still names the t>0 term "the processor's
  per-stream bandwidth gate". Since #530 it is ACTIVE. Optional: reword it
  with the F1 fix.
- `docs/traceability/ieee8021q.md:35` keeps "`srp_sum_slope_bps_o` as the
  class-A queue's idleSlope". That text predates this PR, but it is the same
  shaper story as F1.
- The pin move also adopts processor PRs 96, 100, 101, 103 and 105. They are
  on main before `fbc1f71`, which is an ancestor of the reviewed head
  `5f8cb132`, so review covered them.
  - Their only HDL change is `SRP_DOM_DEF_VID_P = 16'd2`. That equals the
    previous hard-coded `DOM_DEF_VID_P` default, so behaviour is unchanged.
  - Neither CHANGELOG nor SUBMODULES names them. Optional: name them.

### S3: SUGGESTION (lens Tests): an absolute object directory breaks `make crflic`

- `tb/verilator/milan_dp/Makefile:366` runs `./$(CRFLIC_MDIR)/...`. An
  absolute `CRFLIC_MDIR` therefore builds, then fails to run (Error 127,
  receipt `crflic_gate_reverted.log`).
- The mutants driver is not affected, because it uses `crflic-build`.
- The campaign time is recorded as 139 s in the Makefile and README, and as
  169 s in the PR body. This round measured 167 s.

## Independent evidence at this head

The simulator is the scoped 5.050 build. Its wrapper is sha256 `905795b9...`,
and `--version` prints version 5.050, rev v5.050, dated 2026-07-01. Compiles
used 8 jobs. Local paths in the receipts are redacted to `<PACKET>` and
`<CLONE>`.

| probe | result | receipt |
|---|---|---|
| `make crflic` at head | 85 checks, 0 failures; built and ran in 39 s | `receipts/crflic_head.log` |
| `make crflic-mutants` | 4 checks: 4 PASS; each mutant caught on its named check; 167 s | `receipts/crflic_mutants_head.log` |
| item 2 reproduction: stream gate back on the raw verdict | 23 of 85 fail. Licence rises at 1770.38 ms, 1.34 ms after the probe at 1769.04 and before the status 3 answer at 1772.00. First CRF PDU at 1966.30, first Listener Ready at 5814.65 (3.85 s later). 31 AAF PDUs leave in `[A]` | `receipts/crflic_gate_reverted.log` |
| item 1 failing arm: processor at `424c688f` | 17 of 85 fail. Every DUT LeaveAll has mask 8 (Domain only). ACTIVE and licence fall 6 times, 4 Talker Advertise Leaves, 6 re-probes. Pin restored | `receipts/crflic_oldpin.log` |
| BDD scenario against a planted pre-#530 gate | the new scenario fails with the planted expression; the file is restored with no diff | `receipts/bdd_gate_probe.txt` |
| BDD feature at head | 5 scenarios passed | `receipts/behave_streaming_licence.txt` |
| em-dash gate `--base 50e78097` | 0 findings over 138 added lines, arms 57/57 | `receipts/check_em_dash.txt` |
| ROM digests regenerated at the pin | `ltn_rom.hex` and `ucode.hex` MATCH `rom_digests.tsv`. They are equal to the `424c688f` rows | `receipts/rom_digest_check.txt` |
| clone integrity after all probes | HEAD, tree, index, tracked bytes and modes, and three gitlinks: CLEAN. No ignored build or cache output is left in the clone or the processor checkout | `receipts/verify_clone.txt` |
| exact-head hosted check runs (read only) | see "Limits" | `receipts/hosted_check_runs.txt` |

## Per-lens results

- [R285] PASS Conformance: `hdl/milan/milan_datapath.sv:6594`,
  `:1912-1915`, `:2020-2024` and `:5278-5305`, against processor
  `KL_srp_talker_fsm.sv:800-803` and Milan v1.2 5.3.7.3.
  - Every talker gate and the CRF licence read `srp_active_o`. That is
    declaring Talker Advertise, not failed, a Listener Ready or Ready Failed
    registered, and admitted: the 5.3.7.3 condition.
  - Asking Failed licenses nothing and Ready Failed does (`[D]` passes).
  - Item 1 was checked against 802.1Q-2014 10.7.5.20 NOTE and b) 2),
    10.8.2.6, and 10.8.2.8 f:
    - every DUT LeaveAll now flags all four types (mask 15, `[C]`);
    - its LeaveAll-only vectors parse, with 0 malformed.
  - Item 3 was checked against Milan v1.2 5.3.7.7 Table 5.4, quoted verbatim
    from the specification:
    - FRAMES_TX counts intervals of at most 1 s, and resets at STREAM_START;
    - the `[F]` run reads 37 intervals, FRAMES_TX 38, and 155 PDUs;
    - 5.3.8.10 Table 5.6 is the Stream Input set, so the banner fix to
      5.3.7.7 is right.
  - Acceptance items 1 and 2 are met in simulation, and item 3 is explained.
  - The silicon rerun belongs to the manager.
- [R285] UNCLEAN RTL: F1.
  - The logic itself is correct:
    - the repoint is one assign;
    - no new clock crossing: `KL_crf_tx`, `aaf_gate` and the processor face are
      all on `axis_clk` (`milan_datapath.sv:5626` and `:7360`);
    - the widths are unchanged (`SRP_TALKERS_C` slice);
    - `lwsrp_slope_en` keeps the raw verdict;
    - `crft_stat_c[6]/[7]`, `LWSRP_STATUS[8]` and `acmp_lobs_v_w[gj>0]` follow
      the gate;
    - the four `public_flat_rd` pragmas only change simulation visibility.
  - The corner's mechanism is right. Its stated consumer is not.
- [R285] PASS Robustness: `tb/verilator/milan_dp/sim_crf_licence.cpp` phases
  `[A]` to `[E]` and `[INV]`, on every sampled cycle, with the paths below
  read in `milan_datapath.sv`.
  - Input ordering and repetition:
    - a refused first probe, and a MAAP grant after it;
    - repeated DUT and switch LeaveAll cycles (5 and 5);
    - an rLv both outside and inside a fresh probe window;
    - Asking Failed to Ready Failed.
  - Configuration: the escape hatches (`cfg_aaf_bypass`, `~cfg_lwsrp_enable`,
    `~cfg_lwsrp_talker_en`) are unchanged at `:1912-1915` and `:5303-5305`.
  - The optimistic-window boundary was bounded from the processor sources (F1
    impact). Its effect is benign.
  - No software reads `CRFT_CTRL[6]/[7]`, `LWSRP_STATUS[8]` or `0x82C` live
    bits (`git grep` over `sw`, `tools` and `scripts`).
- [R285] PASS Tests: `sim_crf_licence.cpp`, `crflic_mutants.py`,
  `Makefile:234-259` and `:364-375`, and
  `tests/steps/milan_streaming_licence_steps.py:167-183`.
  - Each new check was shown to fail for its defect:
    - three RTL mutants caught;
    - the gate-reverted arm fails 23;
    - the old-pin arm fails 17;
    - the BDD pin fails on the planted gate.
  - The campaign stays out of the default run: `run` builds and runs only the
    `obj_crflic` leg, and `crflic-mutants` is its own target.
  - The leg adds about 40 s locally to `milan_dp`, whose declared hosted budget
    carries an 885 s margin (`scripts/run_all_suites.sh:240-245`).
  - The S1 and S3 suggestions do not affect coverage.
- [R285] UNCLEAN Docs: two open findings.
  - F1: `milan_datapath.sv:6565-6598` and `CHANGELOG.md:39`.
  - F2, retained: `docs/traceability/ieee8021q.md:85`, and
    `EGRESS_QUEUE_MAP.md:66-71`.
  - The rest was checked and is accurate:
    - `REGISTER_MAP.md` rows `0x750`, `0x764`, `0x694`, `0x82C` and the
      `LWSRP_STATUS[8]` note;
    - `ieee8021q.md` MRP-4 and MRP-5;
    - the FR_NFR note;
    - the compliance-matrix row, still partial with B9;
    - TROUBLESHOOTING;
    - TESTING (S1);
    - `SUBMODULES.md` and the diagram: the text diff only changes the pin;
    - `rom_digests.tsv`, regenerated and matching;
    - the moved citations `KL_srp_top.sv:207` and
      `KL_srp_listener_fsm.sv:795-796`, verified at the pin;
    - the milan_dp README leg and phase tables;
    - the VERSION note.
  - The PR and the issue hold enough for a cold reviewer.

## Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:1912-1915,2020-2024,5278-5305,6594`; processor `KL_srp_talker_fsm.sv:793-803`, `KL_srp_encoder/decoder` via the `[C]` masks; Milan v1.2 5.3.7.2/5.3.7.3/5.3.7.7; 802.1Q-2014 10.7.5.20/10.8.2.6/10.8.2.8; `crflic_head.log`, `crflic_oldpin.log`, `crflic_gate_reverted.log` | R285-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| RTL | UNCLEAN (F1) | `milan_datapath.sv:634-651,1640-1651,1871-1915,2013-2025,2490-2510,5270-5320,5620-5630,6530-6620,6745-6755`; processor `protocol_processor_top.sv:490-506`, `KL_srp_top.sv:416-445,762-781,848-862`, `KL_srp_admission.sv:91-208`; pin delta `424c688f..09f9bf38` | R285-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| Robustness | CLEAN | `sim_crf_licence.cpp` `[A]`..`[E]`, `[INV]`; escape-hatch terms `milan_datapath.sv:1912-1915,5303-5305`; the optimistic window from the processor sources; software readers searched | R285-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| Tests | CLEAN | `sim_crf_licence.cpp`, `crflic_mutants.py`, `Makefile`, the BDD feature and steps, `measure_test_evidence.py:607-609`; `crflic_mutants_head.log`, `bdd_gate_probe.txt`, both failing arms | R285-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| Docs | UNCLEAN (F1, F2) | `CHANGELOG.md`, `REGISTER_MAP.md`, `EGRESS_QUEUE_MAP.md`, `FR_NFR.md`, `MILAN_COMPLIANCE_MATRIX.md`, `TROUBLESHOOTING.md`, `TESTING.md`, `SUBMODULES.md`, diagram, `ieee8021q.md`, `milan_dp/README.md`, `KL_talker_diag_ctx.sv:83`, `rom_digests.tsv`, `pp_shadow/sim_main.cpp:2849`, the in-RTL comments; `check_em_dash.txt`, `rom_digest_check.txt` | R285-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |

## Judgements the brief asked for

- **The pin.**
  - `09f9bf38` is the merge of processor PR 107. Its tree `495bfb5d` equals the
    tree of the reviewed head `5f8cb132`.
  - First-parent main before the merge (`fbc1f71`) is an ancestor of
    `5f8cb132`.
  - `424c688f` is an ancestor of the new pin.
  - The ROM digests were re-recorded and verified by regeneration.
- **Item 1.** Met in simulation, with a real failing arm (17 fail at
  `424c688f`).
- **Item 2.** Met in simulation, with a real failing arm (23 fail with the gate
  reverted).
  - The CRF licence follows the processor ACTIVE on every cycle. So do the
    index 0 AAF gate and, by structure, every AAF gate (S1).
  - The CBS slope-enable status bit keeps the raw verdict.
  - `crflic-mutants` is 4/4.
- **Item 3.** Explained correctly against Milan v1.2 5.3.7.7 Table 5.4, and the
  banner citation is corrected.
- **The stated corner.** Real, narrow and benign. It is described against a
  shaper that does not exist (F1).
- **VERSION.** Stays `0x0002_0060` (`milan_csr.sv:196`), with an Unreleased
  changelog entry. This matches the preceding Unreleased #529 entry. No
  descriptor or CSR address changes.
- **The mutants.** Kept out of the default run.

## Limits

- Physical calibration and silicon were NOT RUN. Simulation passes are not
  hardware proof, and the #530 silicon rerun is outstanding.
- The switch model follows Run B: its LeaveAll comes 9.99 s after each DUT
  LeaveAll.
  - A fixed-period switch is not modelled.
  - Processor issue 108 (no leavealltimer restart on a received LeaveAll) is
    unchanged.
- Not run by this round, per scope:
  - the full parent, processor, gPTP, Yosys and builder banks;
  - act or Docker;
  - the other `milan_dp` legs;
  - `pp_shadow`.
  Their evidence here is the author receipts and the hosted shards.
- Exact-head hosted state, first read at 04:24 UTC and re-read at 04:28 UTC
  on 2026-09-24, with the same state both times:
  - these completed with success:
    - `rtl-fast`;
    - `docs-check`, `docs-check-no-git`, `wire-accountability`,
      `bdd-conformance`;
    - `elaborate`, `yosys-elaboration`, `verilator-lint`;
    - Verilator shards 0/5 to 3/5;
    - Yosys shards 0/4 to 3/4;
    - `full-ci-gate`.
  - Physical gPTP was skipped by design.
  - Verilator shard 4/5 (`milan_dp` alone, which now includes `obj_crflic`)
    was still in progress.
  - The `verilator-suites` and `yosys-portability` aggregate contexts were not
    yet emitted.
  - The manager owns hosted and act acceptance.
- Processor PR 107's internal correctness is taken from its own review rounds.
  This round checked only the parent-visible behaviour through `obj_crflic`.

## Pending manager duties

- Resolve F1 and F2, then have a re-review at the new head cover RTL and Docs.
  - The fix should touch comments and docs only.
  - If it leaves the RTL logic, the leg, the mutants, the Makefile and the BDD
    step unchanged, Conformance, Robustness and Tests stay banked at
    `c593cbef` for an ancestor-clean head.
- Hosted:
  - exact-head `verilator-suites` (shard 4/5 wall clock with the new leg);
  - `yosys-portability`;
  - act.
- Candidate merge validation on live dev `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`.
- Post-merge containment.
- The #530 silicon rerun, which is the issue's closing acceptance.

## Prior public findings on this PR

I read these only after the verdict above, F1, S1 to S3 and the ledger were
written. At 04:28 UTC the PR had no review objects and no inline comments.

Its issue comments were:
- two review-start notices;
- R284-1 (`[R284] NEGATIVE`, comment 5807622007).

R284-1 is resolved at this head as follows:

| R284-1 item | disposition at `c593cbef` | basis |
|---|---|---|
| F1 MINOR (Docs, RTL): the corner and the "shaper keeps the raw verdict" argument describe a shaper that does not exist | **RETAINED**, as this round's F1, found independently | `milan_datapath.sv:634-651,6565-6598,6751-6754`; `CHANGELOG.md:39`; the only consumers are at `:2502` and `:2507` |
| F2 MINOR (Docs): ieee8021q.md Q-9 and the EGRESS_QUEUE_MAP opening-edge sentence | **RETAINED**, as this round's F2, re-verified by reading both pages at this head | `ieee8021q.md:85` against `:35`; `EGRESS_QUEUE_MAP.md:66-71`, unchanged by the PR |
| S1 (Docs): mutant campaign time 139 s against 169 s | retained as a suggestion; covered by this round's S3. This round measured 167 s | `Makefile:372`, `README.md`, the PR body |
| S2 (Tests): the old-pin arm runs by hand only | retained as a suggestion. It reproduced here, 17/85, through a portable script (`scripts/run_crflic_oldpin.sh`) | `receipts/crflic_oldpin.log` |
| Observation: t>0 AAF gates have no `~cfg_lwsrp_enable` escape | not a finding against this PR. It is unchanged from base and intentional: `milan_datapath.sv:1994-2007` gives the reason (engine off leaves t>0 dark) | read at head |

No prior finding is resolved as fixed, because no commit follows `c593cbef`.

R285-1 FINISHED
