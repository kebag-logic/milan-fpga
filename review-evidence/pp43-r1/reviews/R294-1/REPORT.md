[R294] NEGATIVE - exact head 5771578784c77e945980c78faa52f3e54bcf5e2d

# R294-1 independent review: PR #111 (issues #43, #49)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head 5771578784c77e945980c78faa52f3e54bcf5e2d, tree 8f898477a082ea32bf33533cf3ec8c8bd109363a
- Source base 939c143333d11e2378a514f1c7b6abd4c3259bfd (two commits: 0452c49, 5771578)
- Role: internal independent reviewer, cleared context, isolated detached clone
- Verdict: **NEGATIVE**. There is one open MAJOR finding (R294-1-F1) and three SUGGESTIONs.

## 1. What was reconstructed

1. **Contributor rules.** The repository has no AGENTS.md or CONTRIBUTING.md. The binding rules are in README.md, docs/README.md (single-source rules, section 2), hdl/README.md (Rules 1-5, in particular Rule 3: "every RTL commit carries its tb/<suite>/ update") and docs/guides/hdl-engineer.md section 6 (suite README mutation records).
2. **Frozen scope.**
   - Issue #43 body: REQ-NET-003 and GAP-04. Its acceptance originally asked for a new port.
   - Issue #49 body: REQ-ACMP-023 and GAP-02. Its acceptance allows "answers gsi selector 7 ... from the listener record itself". Item 4 requires a pbsta mutation recorded in tb/pp_top/README.md.
   - Manager seam decision, issue 43 comment 5813138046 (same text on #49: 5813138341). Selectors 5 and 7 are served inside the processor from SRP and the ACMP listener record, with no new top-level port. The decision fixes the response-level acceptance list and names the mutants that must fail.
   - The review-ready note (43#issuecomment-5813813612) and the PR body were read as claims to verify.
3. **Authorities in the tree:**
   - F02.10 (docs/architecture/02_interfaces.md:411-435)
   - 06 section 6.2 and F06.13 (docs/architecture/06_aecp_engine.md:209-320)
   - 10 section 6.4 (docs/architecture/10_srp_engine.md:290-311)
   - F05.3 and the listener ROM (hdl/acmp/rom/gen_ltn_rom.py:60-96)
   - integrator guide section 8 (docs/guides/integrator.md:285-310)
4. **Diff and history.** Read in full: `git diff 939c1433..57715787` (15 files, +684/-73) and both commits.
5. **Public evidence.**
   - kebag-logic/milan-fpga@5d49561f review-evidence/pp43-r1 (MANIFEST.json, 106 entries). The Vivado utilization reports I used match their published sha256 values.
   - Hosted runs at the exact head: see section 5.

## 2. Findings

### R294-1-F1: MAJOR. A changed Talker Failed FailureInformation now re-declares the SRP Listener attribute with MRP New on the wire

- **Lenses:** Conformance, RTL, Tests, Docs.
- **Where:**
  - hdl/srp/KL_srp_listener_fsm.sv:428-434. The new `ind_reg_w` term is true when `fcode_r`/`fsysid_r` differ from the event while Failed stays registered.
  - :532-535. The same `ind_reg_w` sets `decl_pend_r <= D_DECLARE_C`.
  - :473. The applicant then takes `AE_NEW_C`.
  - :694. It also raises `evt_tk_registered_o`.
  - The strobe also feeds the event router in hdl/top/protocol_processor_top.sv:2813. The ACMP listener receives it as `LEV_TK_REG`, which is an F05.3 dash (inert) cell in SETTLED_RSV_OK (gen_ltn_rom.py:92-95).
  - The strobe also feeds the notification OR at :3133.
- **Authority:**
  - The module's own contract (banner :19-35; 10 section 6.4 lines 297-305) says the Listener declaration "follows the match". It re-declares only on a fresh registration or on the Advertise↔Failed type change, which 802.1Q §35.2.6 treats as an implicit rLv plus a new registration.
  - A FailureInformation change is not a change of the Listener declaration. The Listener attribute (stream_id, AskingFailed) is identical, and MRP New denotes a new or changed declaration.
  - The PR's own documentation claims only the notification effect:
    - 10_srp_engine.md:307-311: "allowing the GET_STREAM_INFO notification path ... to report it"
    - banner :41-43
    - F06.13 row 06_aecp_engine.md:310
  - The PR's scope (the seam decision) is to serve GET_STREAM_INFO fields and their notifications. It does not cover changing MSRP Listener signalling.
- **Evidence (reviewer probes on disposable copies):**
  - P1, unit level, `scripts/probe_srp_redeclare.sh`, receipts `p1-srp-redeclare-{head,base}.log`. The applicant is first quiet with Failed registered. Then a Failed refresh with changed code and bridge is fed.
    - Head: `reg_strobes=1`, and the next join tick pushes `[type=3 code=0 fp=1]`, a Listener **New** with AskingFailed.
    - Base: `reg_strobes=0`, and no push.
    - An unchanged refresh is silent in both.
  - P2, processor top, GI phase, `scripts/probe_top_redeclare.sh`, receipt `p2-top-redeclare-head.log`.
    - After the changed refresh, the processor transmits two MSRP Listener declarations with event 0 (New) and fourpack 1 for sink 0's stream, plus the periodic JoinMt.
    - After the unchanged refresh, it transmits only the periodic JoinMt.
    - The GI suite still passes (416/0). No existing check reads MSRP traffic around this transition.
- **Impact:**
  - Every change of a remote bridge's failure code or bridge ID for a registered Talker Failed now makes the endpoint emit an extra MRP New burst.
  - This is on-wire behaviour outside the issue scope. It is undocumented and untested, and it is driven by remote network state.
  - It is reachable on the shipping 1x1 shape.
  - The ACMP listener also now routinely receives a registration event that its F05.3 table classifies as impossible (dash) in SETTLED_RSV_OK. The event is inert, but it is noise on a documented "impossible" class.
  - Rule 3 (hdl/README.md): the RTL change to KL_srp_listener_fsm has no update in its module suites (tb/srp_stream_fsms, tb/srp_top). Their READMEs and checks still cover only the fresh-registration and type-swap strobes.
- **Required outcome:**
  - Keep the GET_STREAM_INFO notification for a changed FailureInformation.
  - Stop driving the Listener applicant from it. For example, derive a separate failure-change strobe used only by the notification path, and keep `decl_pend_r`/`AE_NEW_C` on fresh registration or type change. Decide explicitly whether the event router and ACMP listener should see it; preferably they should not.
  - Document the result in 10 section 6.4 and F06.13.
  - Add module-level checks in tb/srp_stream_fsms: a changed Failed refresh gives a notification strobe and no Listener push; an unchanged refresh gives neither. Record a mutation in its README.
  - Optionally add a top-level check that no Listener New follows the GI FAILED-REFRESH step.
- **Verification:** At the fixed head, P1 must print `changed-failure next tick pushes=0` while GI FAILED-REFRESH still passes. P2 must show no `event=0` Listener declaration in the `changed-failure` window. The new unit check must turn red when the decoupling is reverted.

### R294-1-S1: SUGGESTION. The selector-0 sample (81 FF) is an untested claim; either prove it or drop it for area

- **Lenses:** Tests, RTL (area).
- **Where:** hdl/top/protocol_processor_top.sv:3088-3106. The documentation claims "captures ... together when selector 0 is accepted" (06_aecp_engine.md:312-316; 02 F02.10 row :427).
- **Evidence:** Reviewer mutant `live-unsampled-fields` (bridge read live at the selector-5 beat) **survives** the GI phase (`receipts/extra-mutants/results.json`).
- **Impact:** The sample duplicates SRP-owned values for the addressed sink. It costs 81 FF regardless of shape, which is about 27% of the estimated 1x1 register delta. The coherence it buys, with the integrator's selector-0 validity flags, is real but unverified.
- **Suggested outcome:** Either add a directed check that changes FailureInformation while selector 4 is held by `gsi_wait_i`, so that the response must show the selector-0 sample, or remove the sample and document per-beat semantics. The second option follows the owner's area directive.

### R294-1-S2: SUGGESTION. The index guard before narrowing is untested

- **Lenses:** Tests.
- **Where:** hdl/top/protocol_processor_top.sv:3101 (`32'(gsi_desc_index_o) < N_STREAM_IN_P`).
- **Evidence:** Reviewer mutant `index-guard-removed` survives. The GI image never carries a STREAM_INPUT index at or above N_STREAM_IN_P.
- **Suggested outcome:** Add an image whose STREAM_INPUT index is at least N_STREAM_IN_P, and check for zero internal fields in the solicited and unsolicited responses.

### R294-1-S3: SUGGESTION. Area follow-ups at the shipping shape

- **Lenses:** Docs, RTL (area).
- syn/ooc/protocol_processor_ooc.tcl measures only the default 8x8 shape. An optional shape argument, or a recorded 1x1 run, would let the owner's area directive be judged on the shape that ships.
- The SRP decoder keeps `evt_failure_system_id_o` as a registered copy of `sysid_r` (hdl/srp/KL_srp_decoder.sv:156, :440, :539). This pre-existing 64 FF, independent of shape, is now kept alive by this PR. It is a candidate saving, outside this diff.

## 3. Lens results (each with its own artifacts)

- **Conformance: UNCLEAN (F1).**
  - Field lineage is correct:
    - SRP `fcode_r`/`fsysid_r` are gated to `tk_reg_state == FAILED` (KL_srp_listener_fsm.sv:808-809) and flow through `srp_snk_fail_*_w`, then the selector-0 sample, then the selector-4 byte and the selector-5 qword, landing at response bytes 72 and 74-81.
    - Listener record RAM write bus (single writer: `recwr_en_w` covers X_INIT, X_PRELOAD and X_WB, KL_pp_acmp_listener.sv:739-766) feeds `lstn_gsi_status_r`, then the sample, then selector 7 `{pbsta, acmpsta}`, landing at byte 90.
  - Response values match F05.3 for these transitions:
    - A5/A12 give ACTIVE
    - A14 gives acmpsta 7
    - A17 gives PASSIVE
    - A15 gives COMPLETED
    - A10 gives DISABLED
    - TK_UNREG in SETTLED_RSV_OK, via cond/A8, gives ACTIVE
  - The acmpsta-zero rule holds.
  - Table 5.22: the replaced triggers (arm, disarm, settle, teardown) each coincide with a pbsta/acmpsta change in every F05.3 cell I walked. The new trigger adds the double-timeout and retry edges.
  - Open: F1, the wire-level MRP side effect.
- **RTL: UNCLEAN (F1).**
  - The internal intercept is correct:
    - Only kind 0, STREAM_INPUT, selectors 5/7 are withheld from `gsi_req_o`.
    - Selector 4 still asks for the DA.
    - The engine's missing-descriptor guard (KL_aecp_engine.sv:1827-1832, :2015) also covers GET_DYNAMIC_INFO through the same µCPU status.
    - A wedged face voids the body (`gxf_fail_r`, :2004, :2275), so a stale sample cannot escape.
    - Only E_GSTRI requests selectors 4/5/7, and it issues selector 0 first (gen_ucode.py:1040-1063).
  - Scoped lint of protocol_processor_top at 8x8 and 1x1, KL_srp_listener_fsm at 8 and 1, and KL_aecp_engine gives 0 findings (`receipts/scoped-lint.txt`).
  - Open: F1, the coupling of notification and declaration through `ind_reg_w`.
- **Robustness: CLEAN.** Covered:
  - reset over erased NVM (GI RESET, RESET-LIVE)
  - missing descriptor with a live ACTIVE record (GI MISSING, plus the retained mutant)
  - single-writer status mirror (no drift path)
  - out-of-range index guard, present by inspection (see S2 for its missing test)
  - the gather-wedge void path
  - clamped sink-index width at N=1 (lint and a 1x1 synthesis elaborate cleanly)
  - the missing-descriptor gather request suppressed, so no internal sample is taken
- **Tests: UNCLEAN (F1).** Re-run at the exact head:
  - pp_top full 1876/0
  - GI-only 416/0
  - srp_stream_fsms 1068/0
  - srp_top 255/0
  - acmp_listener 2540/0
  - aecp_notify 10/0
  - The author's 8 retained mutants all fail their named checks. Golden and restored runs pass (`receipts/gsi-mutants/results.json`).
  - Reviewer mutants killed: `srp-failure-strobe-removed` (GI FAILED-REFRESH), `sel4-integrator-byte` (GI RESET/BIND-ACTIVE failure code), `notify-every-write` (GI BIND-TIMEOUT).
  - Reviewer mutants that survived: `live-unsampled-fields` (S1), `index-guard-removed` (S2).
  - All seam-decision acceptance items are covered at the response level with state-machine-originated values: DISABLED, PASSIVE, ACTIVE+7, COMPLETED, acmpsta 0 elsewhere, code plus full 64-bit bridge per sink, Advertise replacement, withdrawal, two distinct sinks, and solicited = unsolicited body.
  - Issue #49 item 4 (mutation record in tb/pp_top/README.md) is present.
  - Open: F1 has no check at any level, and the SRP module suites are not updated (Rule 3).
- **Docs: UNCLEAN (F1).**
  - F02.10 gains internal rows and an internal-row note, and names stay single-sourced.
  - F06.13 lineage and the sampling paragraph match the RTL.
  - Integrator guide section 8 states the no-new-port seam and points to F06.13.
  - The tb/pp_top README records GI and the mutation table.
  - The syn/ooc README documents the new instrument.
  - `gen_matrix.py --check` passes: 92 rows, 0 untested.
  - Open: F1. 10 section 6.4, the SRP listener banner and F06.13 describe the new strobe as notification-only while it also re-declares.

## 4. Area judgement (owner directive: keep area low)

| Source | Shape | ΔLUT | ΔFF | ΔBRAM |
|---|---|---|---|---|
| Author Vivado OOC (published, hashes verified) | 8x8 | +640 | +784 | 0 |
| Reviewer generic xc7 mapping (yosys synth_xilinx, `scripts/area_top.sh`) | 8x8 | +1942 | +805 | 0 |
| Same reviewer mapping | **1x1 (shipping)** | **+106** | **+307** | 0 |

Vivado per-instance attribution at 8x8 (`receipts/vivado-hier-delta.txt`):

| Instance | ΔFF | ΔLUT | What it is |
|---|---|---|---|
| srp/u_listener | +512 | +808 | 8 × 64-bit per-sink bridge, previously pruned as unconnected |
| srp/u_decoder | +128 | +96 | FailureInformation system-ID capture plus output register, previously pruned the same way |
| top | +153 | | 64 status mirror + 8 change flags + 81 sample |

The rest is placement noise, for example admission −291 LUT / −32 FF.

The author's attribution ("most FF are per-sink bridge state previously pruned") holds for 640 of the 784 FF.

Estimated shipping 1x1 cost:

| Item | FF |
|---|---|
| Listener bridge | 64 |
| Decoder capture | 128 |
| Status mirror | 8 |
| Change flag | 1 |
| Sample | 81 |
| **Total** | **≈282 (the mapper measured +307, about +1.4% of the design's FF)** |

The 1x1 LUT delta is about +100 to +250. The mapper measured +106, and the listener comparator alone is +116 at N=1 (`receipts/a1-srp-listener-area.txt`).

Necessity:

- **Bridge and decoder state:** required by Milan §5.3.8.8 and owned by SRP. Not duplicate.
- **Status mirror (9 FF per sink):** a write-bus mirror of RAM-owned bits, the same single-writer pattern as `strm_started_o`. It is the cheapest option without a second record-RAM read port. Acceptable.
- **81-FF sample:** duplicates owned SRP state for coherence that no test proves. See S1.

## 5. Hosted evidence at the exact head (inspected; hosted acceptance is the manager's)

The `hdl` workflow ran twice at 5771578: push run 35997571621 and pull_request run 35997575834. Both concluded success.

In both runs, all three jobs executed: suites (lint + every suite + matrix + nvm figures), docs-gates and portability. The only skipped step is "Build Verilator v5.050", a cache hit; it is not a skipped gate (`receipts/hosted-runs.txt`).

## 6. Prior public review findings

After my independent pass, PR #111 has no prior-round findings. It carries:

- two review-start notices (R294-1, R295-1)
- the manager validation note 111#issuecomment-5814055772, which has no findings
- a same-round concurrent R295-1 report, which is not a prior round and which I left unread to keep this review independent
- zero review submissions and zero inline comments

There is nothing to resolve or retain.

## 7. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #43/#49 bodies and seam decision; F02.10, F06.13, 10 §6.4, F05.3/ROM; KL_srp_listener_fsm.sv, protocol_processor_top.sv; probes P1/P2 | R294-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| RTL | UNCLEAN (F1) | full HDL diff; KL_aecp_engine gather/void/missing paths; gen_ucode E_GSTRI; listener record write bus; SRP decoder; scoped lint 8x8/1x1; mutants | R294-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| Robustness | CLEAN | reset/erased NVM, missing descriptor, wedge void, index guard, mirror single-writer, N=1 clamp (lint and synthesis) | R294-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| Tests | UNCLEAN (F1) | tb/pp_top gsi_internal.hpp, sim_main.cpp adaptations, gsi_mutants.py; six focused suites re-run; 8 retained and 5 reviewer mutants; SRP module suites | R294-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| Docs | UNCLEAN (F1) | 02, 06, 10 architecture diffs; integrator guide section 8; tb/pp_top README; syn/ooc README; gen_matrix check | R294-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |

## 8. Real limits

- I did not run the full processor banks (run_suites.sh, lint_hdl.sh, make check, yosys portability), any parent or gPTP bank, the builder, or Vivado. For those I rely on the exact-head hosted runs and the published evidence.
- Response-level GI tests exist only at the 8-sink shape. The 1x1 shape is covered here only by lint and synthesis elaboration, plus the manager's parent consumer receipts, which I did not re-run.
- The reviewer area numbers come from a generic open-source mapping. They are estimates, not the Vivado OOC instrument and not routed results.
- The specification PDFs are not in the repository. Conformance judgements rest on the repository's architecture documents and cited clause numbers.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## 9. Pending manager duties

- The parent consumer gates with this head as gitlink at parent dev fa65182adfe2eae15d1a2dbb15e40fb0594b5d66 are manager receipts. The manager note 111#issuecomment-5814055772 reports donor bank 9/9 PASS and parent consumer gates 7/7 PASS, with the parent committed locally and not pushed. I did not re-run these.
- The manager builds the final current-dev candidate at the merge turn: source base 939c1433, live dev fa65182a.
- The manager owns hosted and act acceptance.
- Parent #508 adoption: the integrator gather for input selectors 5/7 becomes unused. MSRP_FAILURE_VALID and the other validity flags stay integrator-owned and must be derived coherently with `srp_tk_reg_state`.
- Re-review after F1 is resolved.

## 10. Reproduction

Scripts are in `scripts/`. They take extracted trees (`git archive`) and never touch a checkout.

- `probe_srp_redeclare.sh <tree> <log>`: P1
- `probe_top_redeclare.sh <tree> <log>`: P2
- `extra_mutants.py <tree> <scratch> <out> <verilator>`: the five reviewer mutants
- `area_srp_listener.sh`, `area_top.sh <tree> <n_in> <n_out> <out> <tag>`: area estimates
- `vivado_hier_delta.py <base.rpt> <cand.rpt>`: per-instance area delta
- `verilator8`: the pinned Verilator 5.050 wrapper capped at 8 jobs (`receipts/tool-identity.txt`)

After the probes, the review clone was verified identical to the exact head (`receipts/clone-integrity.txt`):

- HEAD 5771578, tree and index write-tree 8f89847
- worktree identical in content and mode
- no untracked or ignored files
- the repository has no gitlinks (mode 160000 count 0)

R294-1 FINISHED
