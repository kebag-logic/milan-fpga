[R547] POSITIVE - exact head ba080007a402dced74fa74656338710e0b6cb880

R547-2 is the external independent delta review of issue #691 / PR #693. All five lenses are CLEAN. No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION remains open from this round. The prior blocking findings and wording residues are resolved. This source-review verdict does not establish merge readiness.

The reviewed tree is `6e18c4f36d5bf75ab61a5a7fd8d691d9644d985a`. The complete source range is `e21c1ca024d37ea188ad15b5c8f9c2dae18628df..ba080007a402dced74fa74656338710e0b6cb880`; the assigned delta is the single commit after `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd`, changing seven files. The capture patch is byte-identical to that baseline. The remote PR head was rechecked and matches. See `review-scope.json`, `history.txt`, `full-source.diff` and `round2.diff`.

Context was reconstructed from AGENTS.md / CONTRIBUTING.md, docs/README.md, [the frozen issue](https://github.com/kebag-logic/milan-fpga/issues/691), its assignments and public scope rulings, REQUIREMENTS.md's CSR/MAC/reset and release contracts, docs/litex/CLOCK_DOMAINS.md, BUILDING.md, the production integration and packing contract, then the diff/history and [public executable evidence](https://github.com/kebag-logic/milan-fpga/tree/c963b35b67e973bec9e5c4bbfbaacfaf1db8509d/review-evidence/691-r1). Ruling [6045752839](https://github.com/kebag-logic/milan-fpga/issues/691#issuecomment-6045752839) accepts the kept best-WNS build on each tree. Assignment [6046111178](https://github.com/kebag-logic/milan-fpga/issues/691#issuecomment-6046111178) freezes this correction's scope.

The independent verdict and ledger were written to `INDEPENDENT-VERDICT.md` before opening either prior public review body. Their findings were reconciled afterwards. PR review objects and inline comments contain no additional findings; see `prior-findings-census.json`.

[R547] PASS Conformance - `sw/litex/patches/0007-liteeth-gmii-rx-capture.patch:13`, `sw/litex/milan_soc.py:1445`, `model.log`, `capture.log`, `placement.log`, `public-receipts/TIMING.json` - The delta meets the frozen correction outcomes and preserves the accepted capture mechanism. All nine required input captures remain direct and resetless; sampled reset acts after capture. The generated receiver now matches that mechanism. The shipping integration selects GMII; MII has no required RX IOB capture. No default-selection, CSR, product-source or submodule change is introduced. The historical full-image results remain applicable to the unchanged production capture, subject to the separate final-candidate duty.

[R547] PASS RTL - `tb/verilator/gptp_txts/generated/mac_tx_chain.v:52,825,2207`, `manifest.json:17`, `sw/litex/gmii_rx_capture.xdc:3`, `gmii_rx_capture_check.tcl:19` - The generated HDL diff is confined to RX declarations, post-capture masks and the RX sampling process. The sampled reset is `eth_rx_rst` in the existing receiver domain. Data width remains eight; startup outputs remain zero; no extra pipeline stage or crossing is added. Valid/data are zeroed by reset sampled on their edge, and last remains current pad-valid deassertion combined with the preceding sampled valid. Fixture pin locations match `platforms/alinx_ax7101.py:55`; live placement puts all nine good-fixture captures in ILOGIC.

[R547] PASS Robustness - `sw/litex/test_gmii_rx_capture.py:44,110`, `capture.log`, `gptp-txts.log`, `placement-reset_before_d.rpt` - The 1,036 comparisons cover all byte values, both valid/reset levels, active-frame reset, repeated reset, recovery and frame ends, with ready/error changes. The six structural plants separately exercise valid reset, data reset, valid input logic, data input logic, capture enable and a missing data bit; each is caught. The preserved LUT-before-D fixture fails specifically on every pad, while the good fixture passes. Existing timestamp checks also reject disconnection, shifted observation, removed correction terms and forced rather than measured frame distance.

[R547] PASS Tests - `sw/litex/gen_mac_tx_model.py:396`, `tb/verilator/gptp_txts/Makefile:77`, `mutants.py`, `test_gmii_rx_capture.py:96`, `gmii_rx_capture_check.tcl:25`, `probe_model.py` - Fresh pinned SDK sources plus all five patches produce byte-identical Verilog AND serialized manifest. The exact old pair is refused. The default timestamp make target passes the strong model check, all 85 checks and all six mutants, each by its named assertion. The checker self-test passes 22 arms and catches 21 mutants; the simulation runner self-test passes 10/10. The placement driver requires exact positive/negative counts, zero INERT rows and the expected failure message. The tracked artifact census found no second committed LiteEth RX conversion needing regeneration.

[R547] PASS Docs - `docs/integration/BUILDING.md:607`, `sw/litex/patches/README.md:11`, `patches/apply.sh:9`, PR #693 Description - The documentation correctly explains sampled reset, unchanged latency/last behavior, unused RX error and MII scope. The documented emitter plus committed XDC/driver reproduces the promised result from this tree. Both exact wording repairs are present. The documentation gate and changed-Markdown gate pass. The public evidence distinguishes the failed unkept timing row and unavailable calibration from passing measurements.

Prior review reconciliation, retaining the original severity and lenses:

| ID | Severity | All recorded lenses | Outcome and verification |
|---|---|---|---|
| R546-1-F1 | MAJOR | Tests, Conformance, RTL | RESOLVED. `generated/mac_tx_chain.v:52,825,2207` and `manifest.json:17` now satisfy the generator/Makefile reconstruction contract and acceptance 3. The stale receiver is gone. `model.log`, `model-control.log`, `gptp-txts.log` and `round2.diff` prove exact regeneration, refusal of the old pair, RX-only change, 85/0 checks and 6/6 named controls. |
| R546-1-F2 | MINOR | Docs, Tests | RESOLVED. `BUILDING.md:619`, `gmii_rx_capture.xdc:1` and `gmii_rx_capture_check.tcl:1` supply the previously missing reproducible placement procedure required by acceptance 3 and the public reconstruction contract. `placement.log` and both placement reports prove nine ILOGIC passes and nine failures naming "no register reads the pad", driver rc 0. |
| R546-1-R1 | RESIDUE | Docs | RESOLVED. `patches/apply.sh:9` contains the exact requested two-line 0007 header entry; the stated patch inventory now agrees with the five-entry series. Exact text checked in `prior-finding-reconciliation.json`. |
| R546-1-R2 | RESIDUE | Docs | RESOLVED. PR Description contains exactly: "Default selection and register map are unchanged; the shipping image changes only in the GMII RX capture structure, and nothing was deployed." The ambiguous image statement is replaced; see `public-pr-body.txt` and exact-text receipt. |
| R546-1-S1 | SUGGESTION | Tests | IMPLEMENTED. `test_gmii_rx_capture.py:96` checks unconditional direct capture and all eight data bits; all six controls at line 110 are caught in `capture.log`. |
| R546-1-S2 | SUGGESTION | Docs | IMPLEMENTED. `public-receipts/ROUND2-IOB.json` supersedes the two-row summary. All six entries independently agree with the six raw reports: 21 PASS, one INERT, zero FAIL, including nine RX ILOGIC captures in every row. |

The [R547-1 baseline](https://github.com/kebag-logic/milan-fpga/pull/693#issuecomment-6046044240) had no open finding. The [R546-1 findings](https://github.com/kebag-logic/milan-fpga/pull/693#issuecomment-6046104655) are all disposed above. No finding was deferred to another issue or downgraded to obtain coverage.

The reviewer-owned ledger applies the five lenses at this exact head. Baseline evidence supports unchanged behavior; it does not substitute for examining the round-2 artifacts.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #691 acceptance/rulings; patch 0007:13; milan_soc.py:1445; model/capture/placement receipts; historical timing and six IOB reports | R547-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| RTL | CLEAN | generated/mac_tx_chain.v:52,825,2207; manifest.json:17; gmii_rx_capture.xdc:3; gmii_rx_capture_check.tcl:19; platform pin map | R547-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| Robustness | CLEAN | test_gmii_rx_capture.py:44,110; capture.log; gptp-txts.log; both live fixture reports | R547-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| Tests | CLEAN | generator:396; timestamp Makefile/default target and mutants.py; structural checker:96; fixture driver:25; model-control, IOB and runner self-tests; artifact census | R547-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| Docs | CLEAN | BUILDING.md:607-631; patches/README.md:11; apply.sh:9; PR Description; docs-check.log; focused-docs.log; public evidence reconciliation | R547-2 | ba080007a402dced74fa74656338710e0b6cb880 |

Focused execution receipts:

| Command / artifact | Observed result |
|---|---|
| Fresh pinned SDK extraction plus complete `apply.sh` | Five patches applied; all seven imports resolve inside isolated SDK sources |
| `gen_mac_tx_model.py --check` and `probe_model.py` | Strong reconstruction; both files byte-identical; exact old artifacts refused |
| `make -j16 -C tb/verilator/gptp_txts` | rc 0; 85/0 checks; six mutants caught by named checks |
| `test_gmii_rx_capture.py --emit-dir ...` | rc 0; 1,036 comparisons; six structural controls caught |
| BUILDING.md compact placement command | rc 0; nine ILOGIC PASS / nine specific expected FAIL; no full-image implementation |
| `iob_pack_selftest.py` | rc 0; 22 arms, 21 mutants, zero failures |
| `run_litex_sims.sh --selftest` | rc 0; 10/10 |
| `docs_check.py`; `check_em_dash.py --base e21c1ca0...` | rc 0; zero findings |
| Actual blob/mode/index/gitlink audits | Both review and disposable probe trees match the exact head and pins |

Twenty-one selected public evidence artifacts were hash-checked against the immutable published manifest; see `public-evidence-verified.json`. The round-2 builder log retains one calibration arm NOT RUN; the public standalone log reports five passed, zero skipped. Historical timing is accepted under ruling 6045752839: both trees keep ExtraPostPlacementOpt. Minimum setup/hold across their reported corners is +0.492/+0.007 ns for dev and +0.238/+0.036 ns for the #645 overlay, above the +0.030/0 ns floors. The unkept overlay ExtraTimingOpt row still has +0.013 ns slow WNS and fails the setup floor. These are retained full-image measurements, not measurements rerun in this review.

Limits and pending manager duties:

- Full parent, processor, datapath, portability and builder banks were not rerun. Source validation and the reported source-bank passes are distinct from the final merge candidate. This review's source base is `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`; the assignment's live dev is `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`. The manager must build and validate the final current-dev candidate at the merge turn.
- Placement was rerun only for the two compact fixtures, with the documented threshold 100 and four-thread driver. No full-image routing, implementation sweep, hardware action or physical calibration was performed. NOT RUN calibration, field skips and simulated physical clocks provide no hardware proof.
- `hosted-checks.json` is a read-only exact-head snapshot, not acceptance. It records executed successful jobs, running jobs and the explicitly skipped physical job separately. Several required workflows were still running; no complete hosted aggregate pass is claimed. The manager owns hosted completion and the local workflow replica.
- The manager must publish both independent reviews and the completion ledger, ensure no review is in flight, satisfy the remaining gates and obtain merge authorization. Post-merge containment, authoritative documentation/PR completion state and issue/project closure remain manager duties. Shared SDK users must apply the complete patch series through the maintained workflow.

No source fix, commit, push, GitHub write, merge, author contact, shared install, hardware action or edit to another existing checkout occurred. All disposable SDK sources and builds are under `scratch/`. The initial SDK setup refusal and its correction are recorded in `environment-notes.txt`. All launched foreground commands and their child campaigns have completed.

Final integrity checks compared actual bytes and executable modes with immutable blobs, independently of status flags: 1,168 parent blobs, 214 stream-library blobs, 558 protocol-processor blobs and 104 time-plane processor blobs match. The index trees and required gitlinks match; the optional external gitlink is unchanged and its checkout is outside validation inputs. See `restored-review-tree.log` and `restored-probe-tree.log`.

Portable scripts, complete focused diagnostics, command/exit receipts, generated compact fixtures and selected public evidence are listed in `MANIFEST.sha256`. Local locations in focused logs are replaced with portable placeholders, with original/published hashes recorded in `receipt-normalization.json`. Original output remains under unpublished `scratch/`. Only manifest-listed files and this report are publishable.

R547-2 FINISHED
