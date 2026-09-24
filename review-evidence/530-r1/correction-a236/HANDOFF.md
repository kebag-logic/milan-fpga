# [A236] HANDOFF: kebag-logic/milan-fpga #530 / PR #549, docs-only correction round 1

Relates to #530.

Branch `530-crf-talker-licence`, local head `446e79b977640d13fa1e5dc0f9896d6c5a70391d`
(tree `9f1c9511ca70d889ea2eb2b0a9a3f06d3b29f7fb`). That is five one-line commits
on the reviewed head `c593cbeffaffa647cda70fb1a233455bf9c80d55` and ten on
`50e78097564244c124e1ec30dd8821f83951ab06`. The remote branch is still at
`c593cbef`. Nothing is pushed, the PR is not edited and nothing is merged.
Live `dev` is `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5807728605
Findings answered: R284-1 F1/F2
(https://github.com/kebag-logic/milan-fpga/pull/549#issuecomment-5807622007) and
R285-1 F1/F2 (https://github.com/kebag-logic/milan-fpga/pull/549#issuecomment-5807724033).

## For the manager

1. Push `530-crf-talker-licence` to `446e79b9` (a fast-forward from `c593cbef`).
2. Replace the PR #549 body with `PR-BODY.md`.
3. Run the act replica and the hosted gates at the new head. The PR head moves,
   so the exact-head `verilator-suites` and `yosys-portability` evidence
   restarts. The RTL logic is byte-identical once comments are stripped
   (`receipts/03`), so any difference from the `c593cbef` hosted results would
   itself be a finding.
4. Re-review RTL and Docs at `446e79b9` (R284 and R285, per the assignment).
   Conformance, Robustness and Tests were banked at `c593cbef`, and nothing in
   their scope changed (`receipts/05`: 0 files under `tb/ tests/ scripts/ syn/ sw/`,
   gitlinks unchanged, `hdl/` comment-only).
5. The rest is unchanged from A229's handoff: candidate merge validation
   against live `dev`, post-merge containment, and the #530 silicon rerun.

## Commits

| commit | subject |
|---|---|
| `9f607f7db495de86a6f33e77fc4ee0f617e0befe` | State in milan_datapath's SRP block and the CHANGELOG that no shaper reads the raw verdict or the slope sum, and describe the ACTIVE opening-edge corner as status skew between LWSRP_STATUS[8] and [9]/0x698 |
| `c08d7c0977c76a7f21575c8d839f10f6d0978f80` | Name ACTIVE as the stream gate in ieee8021q Q-9, FR_NFR and REGISTER_MAP, and scope the slope/gate ordering in EGRESS_QUEUE_MAP and ieee8021q to the uninstantiated shaper chain |
| `a018575e11b14dd3860ed8915f2b2d52e1cfdffd` | Say in milan_datapath's CRF row-map note that the processor's Sigma, which no shaper reads, now counts the CRF slope, not the deleted bw-gate's |
| `1ac860255931bfd7784921d69bfc15e2652c871e` | Say in FR_NFR's FR-CONN-01/02 row that the CBS/classifier programming has no object in the shipped datapath |
| `446e79b977640d13fa1e5dc0f9896d6c5a70391d` | Say in milan_datapath's SRP block that the raw verdict and the slope sum, not every admission output, reach one status word each |

## What the RTL actually does (checked at the pin before writing)

- `lwsrp_stream_gate = pp_cd_srp_active_w[...]` (`milan_datapath.sv:6606`). Every
  talker gate and the CRF licence read it.
- `pp_cd_srp_sr_admitted_w` has one reader, `lwsrp_slope_en`, which goes to
  `LWSRP_STATUS[9]` (`:2504`). `pp_cd_srp_sum_slope_bps_w` has one reader,
  `lwsrp_idle_slope`, which goes to `LWSRP_SLOPE` `0x698` (`:2509`,
  `milan_csr.sv:2333`). `over_limit` goes to `LWSRP_STATUS[7]`.
  `granted_slope_bps` is unread.
- Processor at `09f9bf38`:
  - `KL_srp_top.sv:445`: `sr_adm_fsm_w = opt_r | adm_admitted_w` feeds ACTIVE.
  - `:857-858`: the declaration open sets `opt_r` and `opt_cnt_r = 2`.
  - `:774-778`: `opt_r` clears on the third round end after that.
  - `KL_srp_admission.sv`: a round walks one source per cycle, so it lasts
    `N_SOURCES` cycles, and grant, slopes and sum latch at round end.
    `sr_admitted_o = grant_r & req_i`, the live AND.
  - `KL_srp_talker_fsm.sv:800-803`: ACTIVE is declaring AND not failed AND
    Ready/ReadyFailed AND `sr_admitted_i`. The banner at `:27-30` says that on
    admission loss the declaration swaps to Talker Failed.
- The shaper chain left the wrapper in `915cbcc3` (2026-08-31). The
  `REGISTER_MAP.md` bench warning dates from 2026-07-26, so it records a real
  observation of the time.

## Sites changed, and why each one

| site | finding | before | after |
|---|---|---|---|
| `milan_datapath.sv` SRP block | F1 | "the shaper keeps the RAW verdict", "first frames leave against a Sigma at most three rounds stale", "the shaper goes on budgeting", "the invariant HOLDS" | no shaper here; the two status readers named; the invariant scoped to the uninstantiated chain; the corner stated as `[8]` versus `[9]`/`0x698` skew with the Talker Failed swap; closing edge as status; a warning to a later shaping lane |
| `milan_datapath.sv` t>0 SRP term | F1 (R285 S2) | "per-stream bandwidth gate ... no CBS pacing" | "per-stream ACTIVE (#530)"; no source here is credit-paced |
| `milan_datapath.sv` class-D consumer list | F1 | "the CBS slope MUX" as a consumer | "the SRP status words" |
| `milan_datapath.sv` CRF row-map note | F1 | "the class A queue must budget for the media clock" | the processor's Sigma counts it and no shaper reads that Sigma |
| `CHANGELOG.md` | F1 | "The CBS slope enable keeps the raw verdict." | five 10-word-capped lines: the two status words, no shaper, the corner and its only effect |
| `ieee8021q.md` Q-9 | F2 | "`srp_sr_admitted_o` is the per-source stream gate" | `srp_active_o` is the gate; the raw verdict was the gate until #530 and is status only |
| `ieee8021q.md` line 35, the ordering bullet, Q-10 | F2 (same claim; R285 S2) | idleSlope for the class-A queue; the invariant "HOLDS ... equal on the opening edge" | status only; no object on this wire; the ACTIVE lead |
| `EGRESS_QUEUE_MAP.md` "Credit-based shaping" and its Contents summary | F2 | present-tense same-edge claim, "no stream can transmit against an unbudgeted slope" | scoped to the retained chain in past tense, with the ACTIVE caveat. The Contents block moves to the `--` separator, because an edited Contents line may not carry U+2014 and `gen_toc` takes one separator per page |
| `FR_NFR.md` FR-SRP-01/02/03 | F2 (an authoritative page naming the admission bit as the AAF gate) | "admission bit drive the CBS mux and the AAF gate exactly as before" | ACTIVE drives every talker gate; slope and raw bit are status only |
| `FR_NFR.md` FR-CONN-01/02 | F1 (a shaper consuming the reservation) | "the CBS/classifier programming follows the reservation" | no object in the shipped datapath (as the page's own FR-SRP-03 note says) |
| `REGISTER_MAP.md` ordering paragraph, LIVE list, `0x680[4:2]`, `0x694[9]`, `0x698` | F2 (same claim as EGRESS_QUEUE_MAP) | "asserts its active level and its granted slope in the SAME cycle ... Neither edge lets a stream transmit against an un-budgeted slope"; a hardware mux over `0x400`; "slope mux engaged" | no slope mux; `[9]` is the raw verdict ORed over sources and is status only; `[9]` and `0x698` can trail `[8]` by up to three rounds |

Edited lines that already carried U+2014 had it replaced, because
`check_em_dash` judges a whole edited line.

## Not changed, deliberately

- R284 S1 / R285 S3 timing (139 s in `tb/verilator/milan_dp/Makefile:372` and the
  leg README): the PR body gives the measured range instead. Editing the Makefile
  would move the Tests scope banked at `c593cbef`.
- R284 S2 (script the old-pin arm), R285 S1 (t>0 AAF behavioural arm or an
  "index 0 only" note in `TESTING.md`), R285 S3 (absolute `CRFLIC_MDIR`): all
  Tests scope, and outside the two MINORs.
- `REGISTER_MAP.md` "Bench warning (2026-07-26 silicon)": a dated observation
  from before the shaper left (2026-08-31). It is not a claim about the raw
  verdict or the gate.
- Pre-existing generic text that is not about this datapath's gate:
  `KL_pp_shadow.sv:143,1238` ("a CBS slope MUX needs the granted idleSlope", a
  generic integrator), `docs/AAF_LATENCY_TAPS.md:46` ("pacing comes from the SRP
  admission gate"), and `ieee8021q.md`'s "Shaping is FABRIC and UNCHANGED" bullet
  (about the retained modules).
- A229's `[A229] REVIEW READY` comment keeps its superseded wording. The corrected
  text is in the new PR body and in the `[A236] REVIEW READY` comment.

## Gates (at `446e79b9`, clean tree)

| gate | result | receipt |
|---|---|---|
| docs_check, check_em_dash `--base 50e78097` (0 findings), check_doc_style, gen_toc `--check` and `--verify-anchors`, check_doc_paths, check_feature_status, gen_module_matrix `--check`, DOC_MAP `--check`, check_hygiene, check_wire_accountability, check_rtl_source_lists, check_sv_idiom, measure_naming, check_port_contracts, measure_fail_fast, measure_test_evidence, check_todo_ownership, `git diff --check 50e78097 HEAD` | all rc 0 | `receipts/01-quick-gates.txt` (script `scripts/quick_gates.sh`) |
| `xvlog_gate.py --check` | PASS, 4 findings == ratchet, 0 in `hdl/` | `receipts/02-xvlog-gate.txt` |
| `hdl/` comment-only against `c593cbef` | 83 changed lines, all `//`; comment-stripped `milan_datapath.sv` byte-identical (`ffabcf91a0d986e0` both sides) | `receipts/03-hdl-comment-only.txt` (script `scripts/hdl_comment_only.py`) |
| behave (whole suite) | 317 passed, 0 failed | `receipts/04-behave.log` |
| scope | 6 files; 0 under `tb/ tests/ scripts/ syn/ sw/`; gitlinks unchanged; commit bodies empty | `receipts/05-scope.txt` |
| reviewers' claim search | only historical or "no shaper" hits remain, plus the dated bench warning | `receipts/06-claim-search.txt` |
| full diff | `c593cbef..446e79b9` | `receipts/07-diff-c593cbef-to-head.patch` |

Not run: simulation (no logic changed; the `c593cbef` tallies carry over),
act/Docker, hosted CI, `syn/yosys`, hardware.

## Packet

`PR-BODY.md`, `REVIEW-READY.md` (the text posted on #530), `HANDOFF.md`,
`receipts/`, `scripts/`, `MANIFEST.sha256`.

## Posted

`[A236] REVIEW READY`: https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5808176115
