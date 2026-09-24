[R284] NEGATIVE - exact head c593cbeffaffa647cda70fb1a233455bf9c80d55

Round R284-1, internal cleared-context independent review of issue #530 / PR #549.
Head `c593cbeffaffa647cda70fb1a233455bf9c80d55`, tree `6459e8f0866f9a807d01d7dc325997c3a4e4e938`, source base `50e78097564244c124e1ec30dd8821f83951ab06` (five one-line commits, no trailers, `git diff --check` clean).

The behaviour is right. I reproduced item 1, item 2 and both failing arms independently, and they hold under switch timings the lane did not model. The verdict is NEGATIVE because two MINOR documentation findings are open (F1, F2). They leave `RTL` and `Docs` unclean. `Conformance`, `Robustness` and `Tests` are covered clean at this head.

## Reconstruction

In order, I read:
1. `AGENTS.md` and `CONTRIBUTING.md`.
2. The docs map.
3. The issue #530 body and every issue comment: the A205 DECISION, the A205 BLOCKED, the manager decisions of 2026-09-23, the processor issue 106 evidence note, the A229 assignment and REVIEW READY.
4. The PR #549 body.
5. `REQUIREMENTS.md` section 5, `docs/reference/FR_NFR.md`, `docs/reference/EGRESS_QUEUE_MAP.md` and `docs/traceability/ieee8021q.md`.
6. The processor's ACTIVE and admission contract at the pin: `protocol_processor_top.sv:497-506`, `KL_srp_top.sv:415-445,772-781,852-862`, `KL_srp_talker_fsm.sv:28-41,794-803` and `KL_srp_admission.sv:107-200`.
7. The full diff `50e78097..c593cbef` and its history.

After my own findings were written, I read the prior public PR comments. There are two, and both are review-start notices from the manager, so no prior findings exist to resolve or retain.

Scope as frozen by the A229 assignment:
- Adopt processor `09f9bf38` under the exact-reviewed-head rule.
- Item 1: a simulation with a failing arm.
- Item 2: every gate follows the processor's ACTIVE, reproduced first and then fixed, with a failing arm.
- Item 3: explain or fix.

`Relates to #530`: the issue closes after the manager's silicon rerun.

## Findings

### F1 - MINOR - lenses: Docs, RTL - the stated corner and the "shaper keeps the raw verdict" argument describe a shaper the shipping datapath does not have

- **Where.**
  - `hdl/milan/milan_datapath.sv:6570-6598` is the rewritten SRP block. The new OPENING EDGE paragraph (`:6570-6581`) says the first frames "leave against a Sigma at most three rounds stale". The new sentence at `:6596-6598` reads "The shaper keeps the RAW verdict: it budgets every admitted declaration, licensed or not, which is the conservative side of the gate above". The CLOSING EDGE paragraph that the change retained (`:6583-6587`) repeats "The shaper goes on budgeting bandwidth".
  - `CHANGELOG.md:38` says "The CBS slope enable keeps the raw verdict".
  - The PR body's Known limitations frame the same corner as opening "before the round that adds the slope to the shaper's sum".
- **Authority and evidence.**
  - `REQUIREMENTS.md:136-146` (section 5): the 802.1Qav classifier/queue/shaper chain "is not instantiated in the shipping datapath". `docs/reference/EGRESS_QUEUE_MAP.md:3-12` and `docs/reference/FR_NFR.md:207-209` say the same thing.
  - At this head no `credit_based_shaper` or `traffic_shaping_core` instance exists outside `hdl/ieee8021q/ts/`.
  - `lwsrp_slope_en` (`milan_datapath.sv:6599`) has one reader: `LWSRP_STATUS[9]` (`:2502`).
  - `lwsrp_idle_slope` (`:6600`) has one reader: `LWSRP_SLOPE` `0x698` (`:2507`). No firmware reads it (`sw/` search).
  - So "the shaper budgets", "Sigma stale" and "conservative side" have no object on the wire.
- **Reviewer judgement on the corner itself (acceptable).**
  - The corner is real at the processor face. ACTIVE takes `opt_r | adm_admitted` (`KL_srp_top.sv:445`), and the raw verdict can lag it by three admission rounds.
  - A round walks one source per cycle and runs continuously (`KL_srp_admission.sv:167-200`), so the window is about three times `N_SOURCES` cycles.
  - In this product its only effect is that `LWSRP_STATUS[9]` and `0x698` can briefly disagree with `[8]`.
  - A probe that declared Listener Ready before the Talker Advertise did not trigger it: ACTIVE rose only after a Ready that followed the declaration (`receipts/probe_earlyready.log`). The corner is conformance-acceptable, and I retain no Conformance finding.
- **Impact.** The new text tells a later reader that class-A emission is budgeted by a shaper that keeps the raw verdict "on the conservative side". The product sends paced-by-source, unshaped class-A traffic (`REQUIREMENTS.md` section 5, a separate lane). A lane that re-instantiates the shaper, or reasons about FR-SRP-03, would inherit a false safety argument, and the PR records as its limitation a wire risk that cannot occur.
- **Required outcome.**
  - The datapath comment, the CHANGELOG line and the PR's limitation state that no shaper consumes the raw verdict or Sigma in the shipping datapath. The corner's actual effect is status skew between `LWSRP_STATUS[8]` and `[9]`/`0x698`, lasting at most three admission rounds.
  - Any budgeting argument is scoped explicitly to the retained, uninstantiated chain.
- **Verification.** Read the revised text at the new head against `REQUIREMENTS.md` section 5. No claim may remain that a shaper budgets or consumes the raw verdict in the shipping datapath. The docs gates stay green.

### F2 - MINOR - lens: Docs - two authoritative pages still describe the pre-#530 gate

- **Where.**
  - `docs/traceability/ieee8021q.md:85` (row Q-9) says "`srp_sr_admitted_o` is the per-source stream gate". The PR edited the same page at `:32-33` to say `srp_active_o` is the per-source stream gate since #530, and edited MRP-4 and MRP-5, but left Q-9 unchanged.
  - `docs/reference/EGRESS_QUEUE_MAP.md:66-71` says "Opening a source and accounting its slope occur on the same admission-round edge ... no stream can transmit against an unbudgeted slope". The PR's own datapath text (`milan_datapath.sv:6570-6581`) now says the opening edge can lead the slope round in the optimistic corner.
- **Authority and evidence.** AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs". The gate contract changed at `milan_datapath.sv:6594`.
- **Impact.** One traceability page gives two contradicting answers about which processor output gates emission. The egress-queue reference asserts an ordering invariant that the change gave up in the corner.
- **Required outcome.**
  - Q-9 names `srp_active_o` as the stream gate, or drops the gate claim and keeps the admission (75 %) subject.
  - The EGRESS_QUEUE_MAP paragraph is reconciled with the ACTIVE gate. Either it is scoped to the uninstantiated chain, or it states the optimistic-window caveat. This is consistent with F1.
- **Verification.** Search the docs for `sr_admitted` or "admitted" used as the stream gate at the new head. Only historical ("until #530") mentions may remain. The docs gates stay green.

### Suggestions (do not affect coverage)

- **S1 (Docs).** `tb/verilator/milan_dp/Makefile:372` and the leg README (`README.md:405`) give the mutant campaign as 139 s. The PR body gives 169 s, and I measured 168 s (`receipts/crflic_mutants.log`). One number, or a range, would do.
- **S2 (Tests).** The item 1 failing arm (the previous processor pin) is by hand only. A scripted explicit target, like `crflic-mutants`, would keep it reproducible. It reproduced exactly as recorded (below).

### Observation outside scope (not a finding against this PR)

At `milan_datapath.sv:2020-2024` the AAF talkers `gs >= 1` gate on `lwsrp_stream_gate[gs]` without the `~cfg_lwsrp_enable |` escape that source 0 has (`:1915`). With `LWSRP_CTRL[0]` clear, those streams never emit. This is unchanged from base `50e78097`. It is noted for triage as a possible new Issue.

## What was independently verified at this head

The simulator was the scoped 5.050 (`receipts/identity_*.txt`), with at most 8 compile jobs.

| claim | my result | receipt |
|---|---|---|
| `make crflic` is 85 checks, 0 failures | 85 / 0, rc 0, 41 s wall including the build | `receipts/crflic_head.log` |
| `make crflic-mutants` is 4 / 4 | clean control passes; all three plants caught on their named checks; 168 s | `receipts/crflic_mutants.log` |
| item 2 arm: the gate line reverted gives 23 / 85 | 23 / 85; licence rises 1770.38 ms, TALKER_DEST_MAC_FAIL at 1772.00 ms, first CRF PDU 1966.30 ms, first Listener Ready 5814.65 ms | `receipts/crflic_gate_reverted.log`, `scripts/probe_gate_reverted.sh` |
| item 1 arm: pin `424c688f` gives 17 / 85 | 17 / 85; every DUT LeaveAll mask 8 (Domain only); six ACTIVE and licence falls; four CRF Talker Advertise Leaves (25207, 40806, 56406, 72007 ms) | `receipts/crflic_oldpin.log`, `receipts/oldpin_identity.txt`, `scripts/probe_oldpin.sh` |
| item 1 holds for a switch the lane did not model | fixed-period switch LeaveAll at 10.0 s, 12.5 s and 3.3 s (6, 5 and 20 switch LeaveAlls in `[C]`): 85 / 0 each | `receipts/probe_fixedla*.log`, `scripts/probe_variants.py` |
| optimistic corner, early Listener Ready | not triggered: ACTIVE first rose at 5816.09 ms, after the post-declaration Ready; raw verdict at 1771.06 ms | `receipts/probe_earlyready.log` |
| BDD scenario pins the gate source | 5 / 5 scenarios at head; an `active \| sr_admitted` mutant fails the new scenario | `receipts/behave_licence_head.log`, `receipts/behave_licence_mutant_or.log` |
| ROM digests re-recorded, images unchanged | regenerated `ucode.hex` `23605682...` and `ltn_rom.hex` `23cc67ee...` equal `syn/yosys/rom_digests.tsv:7-8` and the `424c688f` rows `:15-16` | `receipts/oldpin_identity.txt` (the same images at both pins) |
| pin under the exact-reviewed-head rule | `09f9bf38^{tree}` = `495bfb5d` = `5f8cb132^{tree}` (processor PR 107 head, `[R271] POSITIVE` at `5f8cb132`); `[R270] POSITIVE` at `27763677`, with only `tb/` changed after it; `424c688f` is an ancestor | read-only `git` and the processor PR 107 verdict lines |

The pin range also carries processor PRs 96, 100, 101, 103 and 105. All of them are contained in the reviewed tree. The only parent-facing interface change is a new `SRP_DOM_DEF_VID_P` parameter, which defaults to 2, the Milan value, and the parent leaves it at that default.

## Lens results (R284-1, exact head `c593cbef`)

```text
[R284] PASS Conformance - hdl/milan/milan_datapath.sv:6594,1912-1915,2020-2024,5278-5305; protocol-processor hdl/srp/KL_srp_talker_fsm.sv:800-803; protocol_processor_top.sv:497-506; hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:229-264; milan_datapath.sv:240; syn/yosys/rom_digests.tsv:7-8; hdl/common/csr/milan_csr.sv:196 - every talker gate and the CRF licence read ACTIVE (Advertise declared, not failed, Ready/ReadyFailed registered, admitted; Milan v1.2 5.3.7.3 as #530's DECISION cites it); the CBS slope enable keeps the raw verdict; item 1 pin per-type LeaveAll (802.1Q-2014 10.7.5.20) at an exact reviewed tree; item 3 Table 5.4 interval semantics with a 1 s interval and reset at STREAM_START, citation 5.3.7.7 consistent repo-wide; VERSION 0x0002_0060 unchanged (Unreleased entry); stated corner judged acceptable (F1 covers only how it is described)
[R284] UNCLEAN RTL - F1 open - hdl/milan/milan_datapath.sv:6547-6600 plus consumers :2502,:2507 and the processor's KL_srp_top.sv:445 and KL_srp_admission.sv:167-200 were checked: the change is a single slice repoint in the same class-D domain as before (no new CDC), the widths are unchanged, `public_flat_rd` is only an annotation, map edits are held by amap_edit_out_resv_r (:2013-2017), and STREAM_START/STOP and the map-edit refusal now follow the licence consistently (:3055,:4036,:4102)
[R284] PASS Robustness - receipts/probe_fixedla10000.log, probe_fixedla12500.log, probe_fixedla3300.log, probe_earlyready.log, crflic_head.log phases [B2] [D] [E] [INV] - closing edges (Listener Lv, Asking Failed, unbind inside a fresh probe window) close the gate within 50 ms on the cycle ACTIVE falls (processor Δ13, Milan 4.2.7.2.2, documented at KL_srp_talker_fsm.sv:37-41); Ready Failed reopens it; per-cycle licence == ACTIVE; item 1 survives three switch LeaveAll timings the lane did not model; issue 108 (no leavealltimer restart) stays a documented deviation
[R284] PASS Tests - tb/verilator/milan_dp/sim_crf_licence.cpp (read in full), crflic_mutants.py, Makefile:243-260,364-375,467-472, docs/testing/TESTING.md:266, tests/steps/milan_streaming_licence_steps.py:167-183; receipts crflic_head.log, crflic_mutants.log, crflic_gate_reverted.log, crflic_oldpin.log, behave_licence_*.log - item 2 is wire-anchored ([A] no PDU, [B] first PDU after the licence, which rises only after the external Ready); both failing arms reproduce with the recorded counts and times; the leg runs in the default `make` and the mutants stay an explicit target; the BDD pin fails for a mutant
[R284] UNCLEAN Docs - F1 and F2 open - also checked and correct: REGISTER_MAP.md rows 0x750 [6]/[7], 0x764, 0x694 [8], 0x82C [2] against milan_datapath.sv:1860-1886,5278-5317,2500-2503; SUBMODULES.md and the boundary diagram pin; ieee8021q.md MRP-4/MRP-5; FR_NFR.md:210-213; MILAN_COMPLIANCE_MATRIX 5.3.7.3; TROUBLESHOOTING.md:733-738; milan_dp README leg section (1770.38 ms, 1966.30 ms, 23/85 and 17/85 match my receipts); CHANGELOG entry
```

## Reviewer-owned completion ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gate and licence RTL, processor ACTIVE and admission, pin tree identity and the processor review verdicts, Table 5.4 implementation, ROM digests, VERSION | R284-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| RTL | UNCLEAN (F1) | `milan_datapath.sv` SRP block and gate consumers, slope/status consumers, processor admission cadence | R284-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| Robustness | CLEAN | leg closing and reopening phases, per-cycle invariant, three fixed-period switch probes, the early-Ready probe | R284-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| Tests | CLEAN | leg source, mutant driver, Makefile wiring, BDD step, both failing arms, mutant campaign | R284-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |
| Docs | UNCLEAN (F1, F2) | REGISTER_MAP, traceability, FR_NFR, EGRESS_QUEUE_MAP, compliance matrix, TROUBLESHOOTING, TESTING, SUBMODULES, diagram, leg README, CHANGELOG, PR body | R284-1 | `c593cbeffaffa647cda70fb1a233455bf9c80d55` |

For RTL and Docs to become clean, a fix commit that touches only comments and docs must be re-reviewed under those lenses at the new head. Conformance, Robustness and Tests stay banked at this head only as long as the fix leaves their scope untouched: the RTL logic, the leg, the mutants, the Makefile and the BDD step.

## Limits of this round

- **Not run** (outside my permission or the round's scope):
  - the full `milan_dp` sweep, `pp_shadow`, lint and `xvlog` ratchets;
  - Yosys, the builder, the processor and gPTP banks, the docs gates;
  - act/Docker, and any hardware.
- **Spec text.** I did not consult the Milan v1.2 and 802.1Q-2014 clause text directly. Clause readings rest on the repository's and the processor's documents, and on the #530 DECISION.
- **Scripted peers.** The listener and switch are scripted models. The fixed-period probes widen the switch timing but do not reproduce a real bridge.
- **Corner bound.** The early-Ready probe did not trigger the optimistic corner, so its bound (three rounds of `N_SOURCES` cycles) rests on reading the code.
- **Physical calibration.** NOT RUN. Simulation at compressed time is not silicon evidence.
- **Receipts.** Simulator include paths in the three build logs are redacted to `<SIM_ROOT>`.

## Pending manager duties

- **Hosted exact-head evidence.** When I read it:
  - `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate`, `bdd-conformance`, Verilator shards 0, 2 and 3, and Yosys shards 0 to 3 were success.
  - Verilator shards 1/5 and 4/5 (4/5 is `milan_dp`, which now carries the new leg) were in progress.
  - The `verilator-suites` and `yosys-portability` aggregates were not yet emitted.
  - "Physical gPTP (nightly and manual)" was skipped. A skipped context is not execution evidence.
  - Snapshot: `receipts/hosted_check_runs.tsv`.
- **act replication** and hosted acceptance.
- **Measure the new leg's hosted time** against the `milan_dp` 2700 s budget (`scripts/run_all_suites.sh:240-246`).
- **Candidate merge validation** against live dev `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`, with the full local bar.
- **The #530 silicon rerun.** A bound CRF talker must stream continuously with no self-Leave and no emission before Listener Ready. The issue closes only after it.
- **Re-review.** After F1 and F2 are fixed, re-review RTL and Docs at the new head.

## Clone restoration

After every probe, the clone is at exact head:
- 874 tracked files are byte- and mode-exact against the index.
- The index equals HEAD's tree, and no hide flags are set.
- The gitlinks `protocol-processor 09f9bf38`, `gptp-processor c1b61743` and `third_party/verilog-axis 48ff7a7e` equal their checkouts, and each checkout is byte-exact too.
- Every build and cache artifact this round created was removed.

Receipt: `receipts/restore_verification.txt`, produced by `scripts/verify_restore.py`. Probe copies lived only under `scratch/`.

Publishable receipts and scripts are listed in `MANIFEST.sha256`.

R284-1 FINISHED
