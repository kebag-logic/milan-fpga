[R635] POSITIVE - exact head fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c

Round R635-2, external independent delta review of issue #645 / PR #742.
Tree: `77e1321b1c9684e8899a85710296eb75af7ddf48`.
Source base: `f62602531d415d6c1cae1374a3cc2938faf54049`.
Previously reviewed head: `2639eecf3f94aa1a8be5c922058a05f0a48b1933`.

All five lenses are CLEAN for the assigned delta. No open BLOCKER, MAJOR or MINOR remains from the named prior findings. One prose RESIDUE is recorded below. This is source review, not merge authorization, full gate acceptance or bench acceptance.

Scope and independence

I reconstructed the repository contract and documentation map, issue acceptance and public decisions, applicable media-clock/counter/area authorities, the full base-to-head diff and history, and then the published executable evidence. The two-commit delta is `e0960932045bdae2ac0602b82d0021da18b525af` plus `fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c`; only `sim_main.cpp` and `MEDIA_CLOCK_FOLLOWING.md` change. `hdl/`, the wrapper, controller, mutation driver and campaign driver are unchanged from the previously reviewed head. Their unchanged coverage is retained under the assigned delta-review rule.

The independent verdict and ledger were written before reading either prior public review body. I then reconciled their named findings. No private author material, other checkout, private management material or current-round reviewer report was read. No source edits, builds, simulation campaigns, hardware actions or GitHub writes were performed. Existing raw receipts were sufficient; no new falsification probe was needed.

The [design decision](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187595500) and [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6193474559) are the scope authorities. The latter explicitly leaves the arm unchanged and assigns investigation of the pre-existing simulation residual to #743. Resolving F2 here means correcting this PR's description and evidence, not claiming that the residual has been repaired. The original issue's bench acceptance remains pending.

Evidence and independent calculations

The [published packet](https://github.com/kebag-logic/milan-fpga/tree/512c59ba2c1a6533ee60fb2fe95f1ae3dcf43dc4/review-evidence/645-rc-r1) supplies the author's round-2 receipts under `author-r2/r2/`. B17 input summaries are `review-evidence/645-b17-r1/author/summary/c01.json` through `c10.json` at `bdb96b6685751a424fbbdc952726f33efd17282a`. I verified 2,163 selected author receipt files against the packet's published SHA-256 manifest. The portable reader checks every input it uses again. These Git evidence objects have no embedded signature; this verifies published bytes and immutable object identities, not a digital signature.

Reproduce the review computations from this candidate checkout, with those evidence commits fetched:

```sh
python3 <packet>/audit_receipts.py
python3 <packet>/verify_checkout.py
```

`receipt-audit.txt`, `audit-inputs.sha256`, `publication-verification.txt` and `checkout-integrity.txt` retain the results and identities. Selected raw logs, command arguments, return codes, B17 summaries and area receipts are included under `raw/`.

1. **Supported bound.** Independently grouping the B17 late-PDU records gives cycle 5's first peak of 24.565 us and largest later peak of 30.260 us. One 48-kHz tick is 20.833333 us, giving the lower bound 9.426667 us, printed as 9.427 us. The other nine lower bounds range from 6.741667 to 9.237667 us and upper bounds from 24.968 to 29.309 us; each contains cycle 5's interval. This is the later-burst inference accepted by the public ruling. The calculation never uses the 10-us listing threshold. `sim_main.cpp:180` derives both constants from cycle 5's row, and its classifier at `:1316` retains strict inequalities. The design at `:1286` and PR body explain the same inference; the rejected “since nothing that late slipped it” rationale is absent from all three current artifacts.

2. **Reclassification and paired reproduction.** On the 16-phase grid, the head's cohort is 177 inside / 143 outside. Exactly eight cases moved inside: `bind_j5_p05`, cycles 1–7 and 10, phase 0.3125 with 0–5 us lateness, minimum 9.440 us. Cycles 8 and 9 remain outside at 9.280 us. All eight newly included cases hold on the head and slip one frame at the first burst on the base datapath. All 177 head-inside cases have that same base +2-dup reproduction. Among the other 143 paired base cases, 43 have +2 dups, 99 have +4 and one has +3, with no skips. These are the restated 43 one-frame / 99 two-frame / one frame-and-pair figures.

   The comparison uses the **head-defined cohort**. The base harness's own margin interval extends until the first burst because it has no recentre, and its printed classifier independently counts 171 inside. That does not contradict the paired 177-case comparison. `author-r2/r2/base_on_head_window.py`, the raw logs and the independent audit distinguish these populations.

3. **Head actions and margins.** All 320 binds get one arm, one settle pulse and one render recentre. All 32 runs pass, versus 0/32 for the base. No head post-action slip occurs; all 177 inside cases keep both counters unchanged. The six outside early slips are at phases 0.8125 and 0.875. Measured firing spans 2047.02–2048.02 tick periods, consistent with the rounded 2047.0–2048.0 report and tick phase. Minimum empty/full margins are 3.479/4.884 ticks, rounded in prose to 3.48/4.88. The early-slip upper time rounds to 2.13 ms.

4. **Finer-grid residuals.** These were recomputed from both datapaths' raw results and command records, not accepted from their summary tables:

| Grid | Inside / outside | Inside early +1 dup | Outside early +2 dups | Head passing runs |
|---|---:|---|---|---:|
| 16 phases, ten cycles, 0 and 0–5 us | 177 / 143 | none | 6, two phases, up to 2.13 ms | 32/32 |
| 32 phases, ten cycles, 0–5 us | 151 / 169 | 1, cycle 7 at 0.84375, 0.127 ms | 19, four phases 0.78125, 0.8125, 0.84375, 0.875; up to 2.50 ms | 31/32 |
| 128 phases, cycle 7, 0 and 0–5 us | 140 / 116 | 2, ideal grid phases 0.890625 and 0.9296875; 0.127/0.252 ms | 6, up to 2.88 ms | 254/256 |

The sweep serializes phase arguments to six decimal places, so the last ideal phase is passed as `0.929688`. All 6, 20 and 8 early-slip event records respectively match the base in kind and printed microsecond. Across all 896 head binds there is no post-action slip. The finer grids intentionally fail the whole-cycle zero-slip check for the three in-window +1 cases; those failures are disclosed, not converted into passing coverage or hidden by the lowered bound. The changed design limit at `:1346`, test-plan row at `:1653`, harness header and PR body state that the arm does not remove this pre-existing result and link #743. The revised denominators 151 and 140 correspond to the supported bound; the previous 141 and 132 are historical 10-us classifications.

5. **Regression and controls.** Published round-2 `fr_default.log/.rc` records 48 B8, 18 pull-in and 30 bind checks with zero failures; all four controller rates pass. `fr_mutants.log/.rc` records 15/15 controls caught, including the named NO-BIND-ARM, BIND-RISE and FOLLOWING-ARM failures. The delta changes no stimulus, no control and no existing check: lowering the bound adds whole-cycle assertions for the newly included cases. Published documentation/source checks pass. The retained missing-module environment refusal exits 2; the documented corrected-environment rerun exits 0. Unchanged round-1 banks remain prior author evidence, not newly executed round-2 banks.

6. **Area citation.** `AREA_BUDGET.md:124` is 50,013 LUT against 38,040, an excess of 11,973. The PR body now cites that headline; 3/11,973 is 0.02506%. The unchanged block receipts show 73/93 to 76/94 LUT/registers for the one-stream arm (+3/+1), while the disabled-tap result is 73/93, matching the base and the shipping no-loopback shape. The enabled eight-stream experiment is a different configuration. Neither the block estimate nor this correction establishes full-image resource compliance or placement timing.

Prior findings, resolved at this head

| Prior ID | Severity and all original lenses | Disposition and verification |
|---|---|---|
| R635-1-F1 | MINOR; Conformance, Tests, Docs | RESOLVED. Supported cycle-5 derivation, data-derived constants, rerun paired receipts and corrected counts verified above. |
| R634-1-F1 | MINOR; Conformance, Tests, Docs | RESOLVED for the same cause. Its earlier expectation that the split would stay unchanged is superseded by the eight raw 9.440-us cases; the author correctly reran and reported 177/143. |
| R634-1-F2 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED as scoped by the public ruling. The description, incidence, phases, expanded outside cases, base comparison and #743 link are present. The simulation residual itself remains unresolved under #743 and is not accepted as declared hardware behavior. |
| R634-1-S1 | SUGGESTION; Docs | ADDRESSED. Current 50,013-LUT headline and 11,973 excess used in the PR body. |

Prior finding sources: [R635-1](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6192392408) and [R634-1](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6193454471). No named prior finding is silently dropped.

R635-2-W1

- Severity: **RESIDUE**.
- All attributable lenses: **Docs**.
- Artifact: PR body, “Known limitations / out of scope”, in-window sub-bullet; `PR-BODY.snapshot.md:100`.
- Authority/evidence: the sentence “A bench reading of `SLIP_LB` +1 dup within a bind's first 42.7 ms is this” is an overdefinite cross-reference. #743 explicitly leaves the mechanism and DUT-versus-harness attribution open. The surrounding PR separately leaves bench acceptance pending; no measurement, test, verdict or conformance criterion depends on this sentence.
- Impact: a prose pointer can be read as stronger causal attribution than intended. This does not change the recorded simulation result or excuse any bench result.
- Exact fix: replace that sentence with “Compare a bench reading of `SLIP_LB` +1 dup within a bind's first 42.7 ms with #743; its cause still requires evidence.”
- Verification: read back that PR-body sentence; keep every measured incidence, phase, limit, test and pending bench obligation unchanged. Carry on the manager's residue checklist. This prose-only residue does not unclean a lens.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #645 design and round-2 rulings; REQUIREMENTS.md verification obligations; MEDIA_CLOCK_FOLLOWING.md:1286,1333; sim_main.cpp:180,1316; B17 c01..c10 and paired base/head receipts | R635-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| RTL | CLEAN | Empty `2639eecf..HEAD -- hdl/` diff; unchanged milan_datapath.sv:6616,6635,6641; TIME_SYNC.md:386 and REGISTER_MAP.md:1878; unchanged wrapper and controller | R635-2 delta confirmation; R635-1 unchanged coverage retained | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| Robustness | CLEAN | MEDIA_CLOCK_FOLLOWING.md:1346; six raw campaign populations under author-r2/r2/campaign; early-slip records and #743; unchanged controller at four rates and following control receipts | R635-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| Tests | CLEAN | sim_main.cpp:180,1316,1357; unchanged sweep.py/mutants.py/settle_control.py; fr_default/fr_mutants logs and rc; receipt-audit.txt | R635-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| Docs | CLEAN | MEDIA_CLOCK_FOLLOWING.md:1271,1286,1333,1346,1653; PR-BODY.snapshot.md; AREA_BUDGET.md:124; published gate receipts; W1 prose residue | R635-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |

Real limits and pending manager duties

- Evidence is the author's published source validation. No manager source bank ran at this exact head, and none is inferred. This review does not replace the full parent, processor, synthesis, builder or native banks.
- Exact-head hosted jobs and local workflow acceptance remain the manager's. This round did not poll them or run the local replica. A skipped context is not an executed job. The 1193.2-s default-suite projection remains a projection; obtain the hosted `follow_ring` window and required context acceptance.
- Source validation is distinct from the final merge candidate. The manager must build the candidate against current dev (assignment snapshot `65617779018f41d7e55d1b1ac189ef882bff6367`), publish its exact identities and builder/native receipts, complete independent reviews, and obtain merge authorization. Later source changes can invalidate affected lens coverage.
- Physical calibration was NOT RUN. The “physical gPTP” receipt is a simulation leg, not a hardware experiment; field skips prove no hardware behavior. The ten-bind B17 bench repeat on the resulting image remains #645's post-merge acceptance. #743's mechanism remains unestablished; a matching counter signature alone is no causal proof.
- After merge, perform required containment and documentation/work-item closure only when the public acceptance is satisfied. This report does not close #645 or #743.
- Final integrity: all 1,325 parent tracked blobs match exact committed bytes, kinds, modes and index. All six gitlinks match; the five required submodules also match their pinned HEADs, tracked bytes, modes and indexes. The optional `external` checkout remains uninitialized. The candidate status is clean. All review outputs are outside the candidate; disposable data is under the packet's unpublished `scratch/` directory.

R635-2 FINISHED
