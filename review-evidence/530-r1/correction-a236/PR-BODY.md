[A236] Gate every talker on the processor's ACTIVE and adopt its per-type LeaveAll (#530 items 1 to 3)

## Contents

- **[Status](#status)** -- Green, the gate tally, and `530-crf-talker-licence` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- #530 stays open for the silicon rerun.
- **[Description](#description)** -- The pin, the licence repoint, the new leg, item 3, and the correction round.
- **[Review findings and their disposition](#review-findings-and-their-disposition)** -- R284-1 and R285-1, item by item.
- **[Authoritative references](#authoritative-references)** -- The Milan and 802.1Q clauses and the decisions.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and submodules.
- **[How to validate](#how-to-validate)** -- The commands and their expected tallies.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What simulation cannot show.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

GREEN at `446e79b977640d13fa1e5dc0f9896d6c5a70391d` (tree `9f1c9511ca70d889ea2eb2b0a9a3f06d3b29f7fb`): ten commits on `50e78097564244c124e1ec30dd8821f83951ab06`. Live `dev` is now `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`; candidate-merge validation against it is still to run. `530-crf-talker-licence` -> `dev`.

The last five commits (`9f607f7d` to `446e79b9`) are the docs-only correction round for R284-1 and R285-1. They change comments and Markdown only. `hdl/milan/milan_datapath.sv` with its `//` comments stripped is byte-identical to `c593cbef`, and no file under `tb/`, `tests/`, `scripts/`, `syn/` or `sw/` changes. The gitlinks do not change either.

## Linked Issue / roles

Relates to #530. The issue closes after the manager's silicon rerun, so this PR does not close it.

Executor: `[A229]` (implementation), `[A236]` (docs-only correction round 1)
Internal cleared-context reviewer: `[R284]`
External reviewer: `[R285]`

## Description

| commit | change |
|---|---|
| `e8c273ff` | Pins the protocol processor at `09f9bf38`, the merge of processor PR 107. Its tree `495bfb5d` equals the reviewed head `5f8cb132` (R271-3 POSITIVE at that head, R270-2 POSITIVE at its ancestor `27763677` with no `hdl/` change after it). The pin range also carries processor PRs 96, 100, 101, 103 and 105. Their only HDL change is the `SRP_DOM_DEF_VID_P` parameter, which defaults to 2, the Milan value, and this parent leaves it at that default. Moves every parent consumer of the pin: `SUBMODULES.md`, the boundary diagram and its PNG manifest, `rom_digests.tsv` (new pin rows; both images hash as before), two line citations of `KL_srp_top.sv` / `KL_srp_listener_fsm.sv` that the new banner moved, and the traceability row MRP-5, which stated per-application receive semantics. |
| `8eca7031` | **Item 2.** `lwsrp_stream_gate` now takes `pp_cd_srp_active_w`, the processor's ACTIVE, instead of `pp_cd_srp_sr_admitted_w`. The CRF licence (`crft_emit_en_w`), the AAF source 0 gate and every AAF talker gate read it. `CRFT_CTRL[6]`/`[7]`, `LWSRP_STATUS[8]` and the `0x82C` talker lobs follow. `LWSRP_STATUS[9]` and `LWSRP_SLOPE` `0x698` keep the raw verdict and the slope sum. They are status only: no shaper is instantiated to read them. Adds the `obj_crflic` leg that proves items 1 to 3, its explicit `crflic-mutants` campaign, a BDD scenario pinning the gate's source text, and the doc rows. |
| `ae51a17f` | **Item 3.** The talker counter banner cited Milan v1.2 5.3.7.10, which does not exist; Table 5.4 is 5.3.7.7. |
| `dd286c01` | Idiom and test-evidence gate fixes for the new harness and driver. |
| `c593cbef` | The leg prints the CRF licence and ACTIVE edges in its timeline and grades that a Listener Lv closes ACTIVE within 50 ms. |
| `9f607f7d` | **R284-1/R285-1 F1.** The `milan_datapath.sv` SRP block now states that no shaper reads the raw verdict or the slope sum in this wrapper. They reach one status word each: `LWSRP_STATUS[9]` and `LWSRP_SLOPE` `0x698`. The bandwidth gate's "no stream transmits against an unbudgeted slope" invariant is scoped to the retained, uninstantiated chain. The opening-edge corner is described by its real effect: status skew. The CHANGELOG line is corrected the same way. The t>0 AAF gate's SRP term is named ACTIVE, and the class-D face's consumer list drops the CBS slope MUX. |
| `c08d7c09` | **R284-1/R285-1 F2.** `ieee8021q.md` Q-9 names `srp_active_o` as the stream gate (the raw verdict was the gate until #530). The page's slope/gate-ordering bullet, Q-10 and its class-D summary line no longer claim a shaper consumes the slope. `EGRESS_QUEUE_MAP.md` "Credit-based shaping" is scoped to the uninstantiated chain and gives the ACTIVE caveat. The same claims are corrected on `FR_NFR.md` (FR-SRP-01/02/03, where the admission bit was said to drive the AAF gate) and on `REGISTER_MAP.md` (the slope-ordering paragraph, the LIVE list, `0x680[4:2]`, `0x694[9]`, `0x698`). |
| `a018575e` | The CRF row-map note in `milan_datapath.sv` said the class-A queue budgets the CRF slope. It now says the processor's Sigma counts it and no shaper reads that Sigma. |
| `1ac86025` | `FR_NFR.md` FR-CONN-01/02 no longer says the CBS/classifier programming follows the reservation. |
| `446e79b9` | The SRP block says the raw verdict and the slope sum reach one status word each. `over_limit` is a third admission output, and it has its own word. |

**Item 1: a bound CRF talker keeps its Talker Advertise.** `obj_crflic` elaborates `endstation_ax7101_1x1_tdm8` with the processor and `KL_maap` millisecond on one 100-cycle grid. It plays the Run B listener and switch port. The switch scopes a received LeaveAll per attribute type, re-declares only the flagged types, and sends its own LeaveAll 9.99 s after each DUT LeaveAll in the capture's byte layout. Phase `[C]` holds the CRF output bound for 76 s across five DUT and five switch LeaveAll MRPDUs, 61 s of it held by the Listener registration alone. There is no Talker Advertise Leave, no licence or ACTIVE drop, and no CRF gap over 1.5 periods. Every DUT LeaveAll flags all four MSRP types. **At the previous pin `424c688f`** the same leg fails 17 of 85: each DUT LeaveAll flags only the Domain. ACTIVE and the licence fall six times, each 5.0 s after a LeaveAll that aged the registration with no re-declaration. The DUT withdraws its Talker Advertise four times: once 5.0 s after a switch LeaveAll, three times 15.1 s after the latest probe. Those are Run B's burst ends.

**Item 2: nothing is emitted before a reservation exists.** The leg was first run against the datapath with only the gate line reverted: 23 of 85 fail with the Run B signature. The licence opens at 1770.38 ms, 1.34 ms after the first probe and before its TALKER_DEST_MAC_FAIL answer (1772.00 ms). The first CRF PDU leaves 3.85 s before the first Listener Ready, and the licence never closes again, through Asking Failed and the unbind. At the head: in `[A]` the DUT declares Talker Advertise and is admitted for 3.9 s with no Listener Ready, and no CRF or AAF PDU leaves. `[B]` opens each gate on the cycle ACTIVE rises. `[B2]`, `[D]` and `[E]` close it on the cycle ACTIVE falls: an AAF unbind, an Asking Failed registration, a CRF unbind inside a fresh probe window. On every cycle the CRF licence equals ACTIVE[CRF], and the AAF gate is never open without ACTIVE[AAF]. `make crflic-mutants` plants each consumer back on the raw verdict (whole gate, CRF slot, AAF source 0) and catches all three.

**Item 3: FRAMES_TX 16 is the documented semantics; explained, not fixed.** Milan v1.2 5.3.7.7 Table 5.4 FRAMES_TX is "Incremented at the end of every observation interval during which at least one Stream Data AVTPDU has been transmitted", with an interval of at most 1 s, "Reset to 0 each time the Talker starts streaming". The fabric's interval is 1 s. Run B's last burst lasted 15.00 s, so it touched 16 intervals. The PDU total is `CRFT_COUNT` (`0x764`), whose register row now says so. Table 5.6 (5.3.8.10) is the Stream Input set and does not define FRAMES_TX. Phase `[F]` grades both sides: FRAMES_TX equals the intervals since STREAM_START, far below the PDU count, and restarts at the next STREAM_START.

VERSION is unchanged (`0x0002_0060`); the CHANGELOG entry is Unreleased and the release step owns the bump. No descriptor, AEM image or CSR address changes.

## Review findings and their disposition

| finding | disposition at `446e79b9` | where |
|---|---|---|
| R284-1 F1 / R285-1 F1, MINOR (RTL, Docs): the corner and "the shaper keeps the raw verdict" describe a shaper this wrapper does not have | **Fixed.** No text says a shaper budgets or consumes the raw verdict or the slope in the shipping datapath. The only consumers are named: `LWSRP_STATUS[9]` and `LWSRP_SLOPE` `0x698`. The corner is stated as status skew between `LWSRP_STATUS[8]` and `[9]`/`0x698` for at most three admission rounds. If the round refuses the stream, ACTIVE falls inside the window and the declaration swaps to Talker Failed. The budgeting invariant is scoped to the retained, uninstantiated chain. No RTL logic line changes. | `milan_datapath.sv` SRP block, t>0 SRP term, class-D consumer list, CRF row-map note; `CHANGELOG.md`; this body's item 2 row and Known limitations |
| R284-1 F2 / R285-1 F2, MINOR (Docs): Q-9 names the raw verdict as the stream gate; the EGRESS_QUEUE_MAP opening-edge sentence | **Fixed.** Q-9 names `srp_active_o`; `srp_sr_admitted_o` appears only as "the gate until #530". The EGRESS_QUEUE_MAP section is scoped to the uninstantiated chain and states the ACTIVE caveat. The same stale claims are corrected where they recur: `ieee8021q.md` (the class-D summary line, the ordering bullet, Q-10), `FR_NFR.md` (FR-SRP-01/02/03, FR-CONN-01/02) and `REGISTER_MAP.md` (the ordering paragraph, the LIVE list, `0x680[4:2]`, `0x694[9]`, `0x698`). | `c08d7c09`, `1ac86025` |
| R285-1 S2 (Docs): the t>0 "bandwidth gate" term; the `ieee8021q.md:35` idleSlope wording; processor PRs 96 to 105 unnamed | Taken with F1 and F2 (`9f607f7d`, `c08d7c09`). The processor PRs are named in the `e8c273ff` row above. | as listed |
| R284-1 S1 / R285-1 S3 (Tests, Docs): mutant campaign time 139 s against 169 s | This body now gives the measured range (below). The Makefile and leg README keep 139 s, because they sit in the Tests scope that R284-1 and R285-1 banked at `c593cbef`. | How to validate |
| R284-1 S2 (Tests): the item 1 old-pin arm runs by hand only | Not taken in this docs-only round (Tests scope). | - |
| R285-1 S1 (Tests): t>0 AAF gates graded by source text only | Not taken in this docs-only round (Tests scope). | - |
| R285-1 S3 (Tests): an absolute `CRFLIC_MDIR` breaks `make crflic` | Not taken in this docs-only round (Makefile, Tests scope). | - |
| R284-1 observation: t>0 AAF gates have no `~cfg_lwsrp_enable` escape | Unchanged from base and intentional (`milan_datapath.sv`, the t>0 SRP term). Not a finding against this PR. | - |

## Authoritative references

- Milan v1.2 5.3.7.3 (streaming state), 5.3.7.7 Table 5.4 (Stream Output counters), 4.3.3.1 (Talker DA validity)
- IEEE 802.1Q-2014 10.7.5.20 NOTE and b) 2), 10.8.2.6, 10.8.2.8 f
- `REQUIREMENTS.md` section 5 (the 802.1Qav chain is not instantiated in the shipping datapath)
- #530: the DECISION https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5797078565, the manager decisions 5797128389 and 5798177316, the assignments 5806344022 and 5807728605
- Reviews: R284-1 https://github.com/kebag-logic/milan-fpga/pull/549#issuecomment-5807622007, R285-1 https://github.com/kebag-logic/milan-fpga/pull/549#issuecomment-5807724033
- Processor issue 106 and PR 107 (merge `09f9bf38`)
- The #117 findings page, Run B (branch `117-silicon-evidence`, `docs/findings/117_GPTP_SILICON_EVIDENCE.md`)
- `docs/reference/REGISTER_MAP.md` rows `0x750`, `0x764`, `0x694`, `0x698`, `0x82C`; `docs/traceability/ieee8021q.md` MRP-4, MRP-5, Q-9, Q-10; `docs/reference/EGRESS_QUEUE_MAP.md` "Credit-based shaping"

## How to get into the same state

```sh
git fetch origin 530-crf-talker-licence
git checkout 446e79b977640d13fa1e5dc0f9896d6c5a70391d
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git submodule status protocol-processor   # 09f9bf3846511f8388d995126502ed92eaa65213
```

## How to validate

```sh
make -C tb/verilator/milan_dp crflic            # checks: 85   failures: 0
make -C tb/verilator/milan_dp crflic-mutants    # 4 checks: 4 PASS, 0 FAIL (about 140 to 170 s: 139 s recorded, 167 to 169 s in three later runs)
make -C tb/verilator/milan_dp                   # every leg, render_mutants included
make -C tb/verilator/pp_shadow                  # pp_shadow: 371 checks, 0 failures
(cd tests && behave --no-capture -f plain)      # 317 scenarios passed
# the item 1 failing arm, by hand; restore the pin afterwards
git -C protocol-processor checkout 424c688fa2205b934a7689a58f2aa766420f2326
make -C tb/verilator/milan_dp crflic CRFLIC_MDIR=obj_crflic_oldpin   # 17 of 85 fail
git -C protocol-processor checkout 09f9bf3846511f8388d995126502ed92eaa65213
# the correction round (docs and comments)
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 50e78097564244c124e1ec30dd8821f83951ab06
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check && python3 scripts/gen_toc.py --verify-anchors
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/xvlog_gate.py --check           # PASS, 4 findings == ratchet, 0 in hdl/
git diff --check 50e78097564244c124e1ec30dd8821f83951ab06 HEAD
```

Expected result: every command above passes except the by-hand arm, which fails as stated.

The simulation tallies above were recorded at `c593cbef`. They carry to `446e79b9` because the correction round changes no RTL logic, harness, Makefile or BDD step. `git diff -U0 c593cbef 446e79b9 -- hdl/` has 83 changed lines, all `//` comments, and the comment-stripped `milan_datapath.sv` is byte-identical at both heads.

## Known limitations / out of scope

- The switch model is the Run B one: its LeaveAll 9.99 s after each DUT LeaveAll. A switch with a fixed LeaveAll period is not modelled here (R284-1 probed 10.0 s, 12.5 s and 3.3 s fixed periods: 85 / 0 each).
- This station's leavealltimer still does not restart on a received LeaveAll (Table 10-5): processor issue 108, not changed here.
- ACTIVE takes the processor's optimistic admission window: up to three admission rounds of `N_SOURCES` cycles after a fresh declaration. When a Listener Ready is already registered at the declaration, ACTIVE, the talker gates and `LWSRP_STATUS[8]` can rise before `LWSRP_STATUS[9]` and `LWSRP_SLOPE` `0x698` include the stream. If the round then refuses it, ACTIVE falls inside the window and the declaration swaps to Talker Failed. No shaper reads the raw verdict or the slope sum in the shipping datapath (`REQUIREMENTS.md` section 5), so this status skew is the corner's only effect. The R284-1 early-Ready probe did not trigger it; its bound rests on reading the processor source. The `milan_datapath` SRP block records this corner.
- `AAF_CTRL[1]` still bypasses the licence (audit B9, unchanged).
- The new leg's hosted time is unmeasured. Locally it builds in about 14 s and runs in about 20 s; the mutants take about 140 to 170 s and are an explicit target, outside the sweep's deadline.
- Not run by the executors: act/Docker, hosted CI, `syn/yosys` (portability and OOC pricing), builder gate 11 (needs the physical build tree), hardware. The correction round ran the docs, source-list, idiom and xvlog gates and the BDD suite at `446e79b9`. It ran no simulation, because it changes no logic.
- Seen, not changed: `sw/litex/milan_soc.py:2123` cites `protocol_processor_top.sv:113` for `DESC_MEM_TMO_CYC_P`, which sits at line 120 at both the old and the new pin.
- Seen in the correction round, not changed: `REGISTER_MAP.md` "Bench warning (2026-07-26 silicon)" still speaks of the CBS slope mux disengaging. It is a dated silicon observation that predates the shaper's removal, not a claim about the raw verdict or the gate.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (simulation parts here; the silicon rerun is the manager's)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
