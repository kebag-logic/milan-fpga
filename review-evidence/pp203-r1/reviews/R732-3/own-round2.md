[R732] NEGATIVE - exact head ec1ff275a72d885f0908fd213d8009e9e4dda4d9

Issue #203 / PR #209, round R732-2. Tree `be6818cf5ccccf5d327cc43adaec34c1df51b98c`; source base `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`; delta from `1be824fccbda5d3341737f5fe033d60edd27af57`. One MAJOR and one MINOR remain open. The original post-DEPARTING leak is fixed, but a non-advertising entity can raise its reset request during another producer's frame. The live PR presents superseded validation measurements as current.

The independent verdict and ledger are recorded in [independent-verdict.txt](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/independent-verdict.txt). No other reviewer's report was read. The prior public R732-1 findings were consulted only after the independent diff pass. Public review submissions and inline comments were empty; the conversation contained the R732-1 findings and review-start notices ([public-pr-comments.json](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/public-pr-comments.json), [public-reviews.json](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/public-reviews.json), [public-inline-comments.json](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/public-inline-comments.json)).

**Prior findings**

- **R732-F1, MAJOR — RESOLVED at its named post-DEPARTING cause.** The common request mask at `hdl/top/protocol_processor_top.sv:4689` and `:4920` closes non-ADP arbitration once ADP finishes building. ADP's effective enable remains low. The exact published observation-only [probe patch](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/post-departure-probe.patch) applies and passes: **128 checks, zero failures**, including its all-frame assertion ([log](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/post-departure-probe.log), [return code](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/post-departure-probe.rc)). The exact-head control passes **127 checks**. RBT9–11 additionally exercise delayed reset, live producer requests, EOF backpressure and slot exhaustion. The separate no-DEPARTING edge F3 prevents an overall clean terminal-state disposition.
- **R732-F2, RESIDUE — RESOLVED.** `hdl/top/protocol_processor_top.sv:824` now reads `REBOOT request (REQ-FWX-001; IEEE 1722.1-2021 §7.4.43; issue #203)`. Commit `aede92e` makes the requested comment-only correction. No new prohibited bench-lane label, reviewer identifier or review-round provenance was found in the delta's source comments.

**R732-F3 — MAJOR — reset request precedes completion of a non-ADP frame when no DEPARTING is required.**

**Attributable lenses:** Conformance, RTL, Robustness, Tests, Docs.

**Locations:** `hdl/top/protocol_processor_top.sv:4920–4940`, particularly the `RB_DEP` exit at `:4938`; `hdl/packet_engine/KL_pp_tx_arbiter.sv` selection/start/stream lifecycle; `tb/pp_top/sim_main.cpp:12737` (RBT8). Contradicted interface statements: `docs/architecture/02_interfaces.md:582` and `docs/guides/integrator.md:697`. `docs/architecture/06_aecp_engine.md:1127–1129` acknowledges that a frame selected in the closing interval can still go, without reconciling that with the request's unconditional silence contract.

**Authority/evidence:** issue #203's terminal transmit-quiet and frame-integrity acceptance, [public round-two scope decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/203#issuecomment-6503153894), REQ-FWX-001, and F02.10's explicit promise that nothing leaves `tx_*` from the request's rise until reset. This finding rests on that project/interface contract, not an inferred blanket ACMP prohibition from an IEEE clause.

The [portable probe](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/nonadvertising-probe.patch) uses real interfaces and unchanged RTL. It boots with advertising disabled, raises link-up, registers one other controller, binds eight sinks to a discovered talker and takes the lock. It holds the required REBOOT notification's EOF for 5 seconds, as RBT11 does, leaving every standard TX slot occupied. It then releases the notification and withholds reset. SUCCESS and the required notification complete; no DEPARTING is generated, as appropriate. The request rises at cycle **16184473**, with a frame already in progress (`in_frame=1`, one byte collected, `tx_valid_o=1`). An autonomous ACMP frame, subtype `0xFC`, message `0x00`, finishes at **16184542**, **69 cycles after the request**. The suite reports **134 checks, one failure**, solely the new no-byte-after-request assertion ([raw log](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/nonadvertising-probe.log), [return code](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/nonadvertising-probe.rc)). The held-request and legitimate no-advertising shutdown checks pass.

**Cause/impact:** the gate prevents future arbitration but preserves a selected frame. `RB_DEP` waits only for ADP's builder, queue and flight. With ADP already down, those conditions are empty while another producer's frame selected during shutdown can remain active. The new terminal gate depends on a final ADP frame to establish whole-plane drainage. An integrator resetting immediately on the documented request can interrupt that active frame; an integrator delaying reset observes transmission during the promised quiet interval. This dependency and the strengthened interface claim are directly affected by the delta.

**Required outcome:** establish terminal silence before asserting the request even without a DEPARTING. Close further admission and account for every already selected or active frame across all producers, preserving frame integrity, required SUCCESS/notifications, advertised shutdown ordering and the held request. Reconcile the interface and guide statements with the implemented guarantee.

**Verification:** retain RBT1–11 and the original reviewer probe. Add a non-advertising shutdown with autonomous work queued behind a held notification; check every offered byte from the request through delayed reset. Hold the selected non-ADP frame at EOF and require the request to stay low until completion. A plant removing that whole-plane completion condition must fail. RBT8 currently supplies no competing autonomous work; RBT9–11 exercise advertising and miss this edge.

**R732-F4 — MINOR — live PR validation claims still describe round one.**

**Attributable lenses:** Tests, Docs. **Artifact:** [live PR #209 body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/209), captured with exact head in [public-pr.json](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/public-pr.json), sections “Tests and mutants,” “Gates,” and “Consumer gate.”

**Authority/evidence:** the PR must describe the reviewed implementation and its actual evidence. The [current readiness comment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/203#issuecomment-6510359081), exact-head receipts and independently checked logs disagree with the unqualified live body:

| Live body | Current published evidence |
|---|---|
| RBT 79 checks; 17 REBOOT arms | 127 checks; 30 arms, including 13 new gate plants |
| Early-request plant: 12 failing checks | 17 failing checks |
| Source sweep 1,030,845; pp_top 10,984 | 1,030,893; pp_top 11,032 |
| 259 executed requirement-evidence lines | 262 |
| Dispatch campaign 86 arms; counts agree with README | 99 arms, five controls; current counts audited |
| Scratch consumer OOC −101 LUT, +9 FF | −257 LUT, +9 FF at the round-two scratch pin |

**Impact:** readers cannot determine which revision the live validation/area claims cover; the body also omits the terminal gate and its added coverage. This changes measurements and test claims, so it is **not RESIDUE** under the owner's rule.

**Required outcome:** update the live description around the final delta and exact-head receipts, explicitly labelling any historical results. Correct the figures above and describe RBT9–11 and the 13 added plants. Preserve the distinction between author source/scratch-consumer evidence and the future manager candidate. **Verification:** compare the revised body to the pinned logs, README cells and head metadata. This review made no GitHub write.

**Five-lens examination**

The supplied AGENTS instruction was read; repository/ancestor AGENTS.md and repository CONTRIBUTING.md were absent. `docs/README.md`, the issue body and public decisions, requirement/interface authorities and linked integration issues established scope. The complete base-to-head diff/history was reconstructed, with detailed reassessment of the three-commit, 25-file delta. Only the production top changes RTL in this round; no production port, parameter, register map, command model or microprogram changes relative to the prior head. Unaffected status/refusal, lock/acquire, response and notification paths retain their prior reviewed disposition and authority limits.

| Lens | Artifact-specific assessment |
|---|---|
| Conformance | REQ-FWX-001, F02.10, AECP §6.11 and public acceptance require the shutdown frames and terminal silence. RBT preserves refusal/status behavior and notification/departure ordering; F3 violates the unconditional request interface promise. |
| RTL | Examined all eight `arb_want_w` assignments, common mask, current-valid arbitration qualification, frame-atomic ownership, and ADP pending/build/queue/flight and permanent disable. The mask solves F1 without truncation or suppressed required notifications. F3 lacks non-ADP flight accounting. |
| Robustness | RBT9 holds DEPARTING EOF 1.5 seconds and delays reset 75 seconds; RBT10 covers originator demand for 65 seconds; RBT11 fills slots behind a held notification. These pass. Combining slot pressure with ADP already down exposes F3. |
| Tests | Reviewed new taps, all-byte offer tracking, frame accounting, lock expiry, live producer demand, reset recovery, RBT7 admission checks, changed named checks and all 13 new plants. Audited 30 raw plant logs against exact-head labels and README counts. F3 is absent coverage; F4 misstates validation. |
| Docs | Reviewed compliance/gap changes, interfaces, packet arbitration, ADP, AECP, integrator/operator guides, bench README, port comments and live PR. Post-DEPARTING claims match execution; request-wide silence fails F3 and live measurements fail F4. The unchanged diagram retains its prior-round disposition. |

**Executable evidence**

Independent executions used disposable copies, with the scoped simulator identity checked as **5.050** before compilation ([identity](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/simulator-identity.log)). [run-probes.py](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/run-probes.py) accepts the checkout as its argument, builds with `make -j16` and bounds compiler parallelism to eight. Commands ran in the foreground; no job remains running. Peak observed unit memory was **3,592,044,544 bytes**, below the requested 12 GB cap.

| Independent execution | Result |
|---|---|
| Exact-head REBOOT control | **127 checks, 0 failures**, [log](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/reboot-control.log) |
| Published round-one reviewer probe | **128 checks, 0 failures**, [log](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/post-departure-probe.log) |
| Non-advertising pending-frame probe | **134 checks, 1 failure**, defect demonstration, [log](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/nonadvertising-probe.log) |
| Receipt/source audit | **90 public files match published SHA-256**; all 30 REBOOT plants complete and fail their named checks with exact README counts; patches apply at this head; [audit](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/audit.log), [plant ledger](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/mutation-audit.json) |

All 13 new plants were verified from published completed raw executions, not represented as independent reruns:

| Plant | Named failing check | Failing checks |
|---|---|---:|
| `rbt-quiet-gate-dropped` | RBT9 silence | 3 |
| `rbt-quiet-from-the-request` | RBT9 silence | 1 |
| `rbt-quiet-opens-notifications` | RBT9 silence | 2 |
| `rbt-quiet-opens-originator` | RBT10 silence | 1 |
| `rbt-quiet-opens-listener` | RBT9 silence | 2 |
| `rbt-quiet-opens-maap` | RBT9 silence | 1 |
| `rbt-quiet-opens-srp` | RBT9 silence | 3 |
| `rbt-adp-reenabled` | RBT10 silence | 2 |
| `rbt-quiet-opens-talker-answers` | RBT10 silence | 2 |
| `rbt-quiet-opens-aecp-answers` | RBT9 silence | 10 |
| `rbt-quiet-at-the-shutdown` | RBT11 departure/request progress | 2 |
| `rbt-quiet-closes-departing` | RBT6 required DEPARTING | 22 |
| `rbt-quiet-closes-notifications` | RBT6 required notification | 28 |

Each has a completed simulation tally and required named failure; compilation failures do not count as kills. The two existing admission plants preserve their defects and now observe RBT7's open-gate interval and the engine command count, so the transmit mask cannot hide bad admission.

The [pinned public packet](https://github.com/kebag-logic/milan-fpga/tree/6ea82be431a475f5f52593a97bd751177a01e6bb/review-evidence/pp203-r1) supplies **author source-head** receipts: documentation, both lint versions, synthesis/elaboration, 93 elaboration checks, executed requirement tags, and **1,030,893 suite checks with zero failures**. Campaign receipts remain passing: dispatch 99 arms plus five controls; AECP 67 checks; D3 union 110/110; notification 137/137; counter 18; ACMP 101/101; stream-info 30; name-write control; elaboration mutants 160/160; command decode 17/17; ADP 62 checks. D3's first part is incomplete as a standalone run; the union combines its 38 completed arms with the 72-arm second part. It is not represented as one complete first run.

Public scratch-consumer records name parent `8fb40ef07279aafa83bc535196278de2f3d6ec0b`, processor gitlink `ec1ff275a72d885f0908fd213d8009e9e4dda4d9`, and gPTP gitlink `f97c18035be6ef5345e5af27db2124c5697c1b40`. The tally reports 64 suites / 2,191,694 checks / zero failures, with 38 passing static gates. These are author scratch-consumer receipts, **not manager source-bank or final-candidate runs**.

Hashes were verified against [published-manifest.json](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/published-manifest.json). Cryptographic signing was **not** verified: the public evidence commit reports `unsigned`, with null signature/payload ([evidence-commit.json](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/evidence-commit.json)); no detached signature appears in the inspected inventory. Hash matching is not a signature claim.

At the hosted snapshot, exact-head runs [40969151829](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/40969151829) and [40969144341](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/40969144341) had successful documentation and portability jobs; suites remained in progress. The simulator-build step was skipped for the cache, and later campaigns/evidence steps were pending. Skipped/pending contexts are not execution evidence. Captured job records are manifested; hosted/act acceptance remains the manager's duty.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN — F3** | frozen scope; REQ-FWX-001; F02.10; AECP §6.11; shutdown wire checks | R732-2 delta; R732-1 unchanged paths | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| RTL | **UNCLEAN — F3** | top gate/sequence; arbitration/stream; ADP pending/flight/disable; AECP hold dependencies | R732-2 delta; R732-1 unchanged paths | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| Robustness | **UNCLEAN — F3** | held EOF; full slots; delayed reset; producer demand; non-advertising probe | R732-2 | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| Tests | **UNCLEAN — F3, F4** | RBT1–11; reviewer probes; 30 plants; source receipts; PR claims | R732-2 delta; R732-1 unaffected gates | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| Docs | **UNCLEAN — F3, F4** | conventions; requirement/interface/engine changes; guides; README; heading; live PR | R732-2 delta; R732-1 unchanged artifacts | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |

**Limits and pending manager duties**

- Full licensed IEEE 1722.1-2021 and Milan v1.2 texts were unavailable in the clone. Public primary-source lookup did not provide those clause texts: the [IEEE publication page](https://standards.ieee.org/ieee/1722.1/6670/) provides access information; the [current Milan download page](https://avnu.org/resource/milan-specification/) offers a later revision. The prior primary-text limitation remains, including unsupported-target status interpretation. This delta review preserves the frozen explicit status decisions and claims no fresh normative certification. F3 is independently established against the project interface contract.
- No full processor/parent/gPTP/synthesis/builder bank, route, hardware or physical calibration was run by this reviewer. **Physical calibration NOT RUN**; field skips and digital simulations are not hardware proof. No separate multi-interface REBOOT campaign was executed; that prior coverage limit remains.
- The manager owns hosted/act acceptance and the **final current-dev merge candidate**, including builder/native banks and published receipts. Source base `f65c8ff7` and live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141` are distinct from that future candidate. No manager source bank exists or is inferred here. Parent reset wiring, persistence/reset policy, adoption edits and physical recovery proof remain integration duties under #787 and the release gates.
- Resolve F3 and F4 and obtain the required independent positive reviews before merge. F2 requires no residue carry-forward. No additional wording-only residue or suggestion was identified in this delta.
- The original checkout was never mutated. Final audit verifies **749 tracked blobs, modes and index entries** against the exact head/tree; status is clean and this processor tree has **no submodule gitlinks**. Disposable changes are confined to `scratch/`. No source fix, commit, push, GitHub write, author contact, shared installation or other-checkout edit occurred. Only REPORT.md and files listed in [MANIFEST.sha256](https://github.com/kebag-logic/milan-fpga/blob/95ef1fda641e7fd17e5b75643f1d1941b08af413/review-evidence/pp203-r1/reviews/R732-2/MANIFEST.sha256) are publishable; `scratch/` is excluded.

R732-2 FINISHED

