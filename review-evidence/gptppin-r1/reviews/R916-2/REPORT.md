[R916] NEGATIVE - exact head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21

Round R916-2, external review of #994 / PR #995. All five lenses were applied. One MINOR test finding remains; under this repository's coverage rule it prevents approval. No new production RTL defect was found. The original two restored faults are now detected by the platform regression.

## Scope and reconstruction

Reviewed tree `90eef089759111d73b0316ded772250ee95a9735`, the full adoption diff from `300da99beed5bb1c77e4b04af0bb4f9369856e0d`, and principally the delta from prior reviewed head `bbfdb6746d585e490508783dc8a88c79fbab02c0`. The intervening train merge `3a8bdbf063` has exactly the prior head's tree. The two subsequent commits change the shadow harness and documentation; no product synthesis input changes. Unchanged product behavior retains the earlier review's coverage, subject to the new test finding below.

Read AGENTS.md, CONTRIBUTING.md, docs/README.md, #994's frozen criteria, REQ-PTP-01/05/07, GPTP_PLANE.md, the donor integration contract, #818 and BUILDING.md section 5, then source/history and public executable evidence. #994 currently has no comments; no nonexistent manager source-head evidence is inferred. The public PR body names the current head and the stacked base `dev-soft-core`.

Evidence archive: [public packet at 2fcbd468](https://github.com/kebag-logic/milan-fpga/tree/2fcbd46885448a4b4b80e6f39f8a8320667ae84a/review-evidence/gptppin-r1). All 245 files match their published SHA-256 manifest entries. The archive commit contains no embedded cryptographic signature: this review verifies published content integrity, not a signer identity. See `evidence.py` and `evidence.log`.

## Finding

### R916-2-F1 | MINOR | Conformance, Robustness, Tests, Docs

**Artifacts:** `tb/verilator/gptp_shadow/sim_main.cpp:2749`, `:2753`, `:2754`; `tb/verilator/gptp_shadow/README.md:36`; `docs/reference/SUBMODULES.md:1033` and `:1045`; PR body, platform-regression phase 19. Executable evidence: `order_probe.py`, `order-probe.patch`, `order-probe.log`, `order-probe.rc`.

**Authority/evidence:** R916-1-F1 requires grading the master Announce before queued re-election through parent transport. CONTRIBUTING section 3 and AGENTS section 6 require self-checking integration tests that can fail for the claimed defect. REQ-PTP-05 and the adopted first-Announce contract supply the behavior being tested.

The new test records the re-election cycle in `fall`, and checks that re-election happens within two milliseconds. However, its purported before-re-election check counts frames with `txf_cyc[i] < rise + 2 * kSyncTicks`, not frames with `txf_cyc[i] < fall`. Those bounds differ substantially: the count window is 500,000 cycles, while the control's re-election is 1,281 cycles after takeover.

A disposable transport probe holds the wide lane's ready input low across this one race, then releases it after the peer Announce has been processed. It changes neither product RTL nor any existing assertion or expected value. An added print records the actual last-beat and re-election cycles:

```text
INFO #106 race: master at +5999366, re-elected at +6000647
ORDER PROBE: Announce last beat 73666191, re-election 73662813, before=0
408 checks: 408 PASS, 0 FAIL
```

The Announce arrives 3,378 cycles after re-election, yet the check explicitly claiming the opposite passes. This probe demonstrates an oracle gap. It does not assert that stalled transport violates the unstalled product contract or that product RTL needs changing.

**Impact:** a regression that queues the master Announce until after re-election can satisfy this race check. Detecting the old missing-Announce fault proves presence coverage, but not the ordering that the test name and its documentation claim. This is a test/coverage defect, not purely wording, so it is not RESIDUE. The remaining issue is narrower than the previous absence of any platform regression, hence MINOR.

**Required outcome:** in the existing unstalled race, require exactly one relevant master Announce to cross the chosen lane boundary after takeover and strictly before the measured re-election. Preserve the missing-Announce, cadence and credit assertions. Make the documented boundary agree with the measured boundary. No product change or expanded backpressure guarantee is requested.

**Verification:** the pristine run must still pass; both original fault probes must still fail their named checks. The supplied delayed-transport observation must no longer satisfy the before-re-election assertion. A direct comparison against `fall`, with a valid recorded transition, is sufficient for the existing last-beat interpretation.

No other new findings, suggestions or wording residue were identified in the reviewed delta.

## Original faults and consumer evidence

Own executions used the scoped compiler reporting version 5.050, revision v5.050. Its launcher SHA-256 is `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`. Three disposable builds ran concurrently, with five compiler jobs each and `make -j16`; no repository source was changed. `probes.py` takes repository, packet and compiler arguments and replays the exact published round-1 patches.

| Execution | Result | Meaning |
|---|---|---|
| Pristine `gptp_shadow run` | 408/408, rc 0 | Real transport, PHC, four masterships, cadence and credit arms execute |
| Old 2 ms Announce arm plus END at SELF | 403/407, rc 2 | First-at-once, race-presence and two credit checks fail |
| Word 3 applied only during slew | 404/408, rc 2 | Both +100 and -100 ppm rate-zero and real-counter-advance checks fail |
| Lifecycle test | rc 0, eleven controls | Repeated detection, survivors, failed builds, input refusals, cancellation and isolation controls pass |
| Ordering observation | 408/408, rc 0 | Incorrectly accepts an Announce after re-election; F1 |

The pristine settled trims are +13,402 and -13,366 Q8.24 units. The retained-rate fault leaves +13,402 and -13,434 units after takeover. The test measures the actual effective counter adjustment, exact counter advance, slew level and adjtime strobes; it also checks the Follow_Up frequency change, phase-change field and mastership indicator. The slewing and repeated/no-new-rate arms execute. The first unstalled Announce completes 285 cycles after takeover. The credit-refusal arm postpones it to 2,000,103 cycles, then grades cadence.

The published mutation slices cover 4 + 4 + 3 = 11 controls. Both newly added controls fail their own named checks. Their receipts are at `d616b1c6`; comparison with the reviewed head proves that every campaign input is identical. The existing credit control is detected through other checks and already has this limitation at the prior head; the PR discloses it. It is not a new delta finding.

Source-head consumer results below are the author's manifest-verified receipts, not new manager or reviewer bank executions:

| Consumer | Published completed evidence |
|---|---|
| `gptp_plane run` | 31/31 |
| `phc-step` | 62-check clean run, positive control and all six planted-defect arms; eight arms across the recorded windows |
| `gptp_tables` | 36 checks, limits check, 26 controls across two completed slices |
| `gptp_txts` | 13/13 controls |
| `milan_dp gptp` | 212/212; clockQuality 0xF822436A |
| `milan_dp gptp-lat` | 212/212; clockQuality 0xF8FE436A |

Interrupted 585-second aggregate windows are not claimed as successful commands. Their completed arms plus the later completed slices provide the stated coverage. Raw published receipts are under `published/author-r2/receipts/`; `evidence.log` records the relevant tails and source attribution.

## Prior findings and residue

| Prior item | Disposition at this head |
|---|---|
| R916-1-F1 / R915-1-F1, MAJOR | Substantially repaired: real platform tests detect both exact restored faults, including both settled rate signs, slew, repeated takeover, cadence and credit. The strict before-re-election requirement remains open as narrower MINOR R916-2-F1. The original requirement is not declared fully resolved. |
| R915-1-F2, MINOR | Resolved as a tracking omission. Open issue [#997](https://github.com/kebag-logic/milan-fpga/issues/997) records the AECP silence, both-pin reproduction, no-retry acceptance and intended fix. PR known limitations, SUBMODULES.md:1053 and CHANGELOG.md:81 link or name it. The underlying anomaly remains open and is not claimed fixed. |
| R915-1-R1, RESIDUE | Resolved. SUBMODULES.md:984-992 says the first qualifying first directive ships; otherwise all three run and the best worst-corner WNS ships. Splitting the sentence preserves that meaning. |
| R915-1-R2, RESIDUE | Resolved. PR recipe order is ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt. |
| R915-1-R3, RESIDUE | Resolved. CHANGELOG.md:71 identifies 802.1AS-2011 Figure 10-15. |
| R915-1-S1, SUGGESTION | Adopted. PR explains the separate stricter hold-floor failure and the 0.012 ns WHS fall. |
| R916-1-R1, RESIDUE | Resolved. PR commit table now counts six later commits, matching first-parent history after the routed commit. |

## Lens evidence and reviewer-owned ledger

**Conformance:** examined #994's three criteria against pin checkers, exact gitlinks, ROM ledger, consumer receipts and both release routes. These frozen criteria have evidence. The mandatory self-checking behavioral verification remains incomplete only at F1's ordering predicate. Images meet the #818 floor: 8x8/1if is 46,246 LUT, -375 from base, worst WNS/WHS +0.066/+0.036 ns; selected 1x1/1if is 32,639 LUT, -41, +0.170/+0.024 ns. All recorded signoff corners qualify. No route was rerun here.

**[R916] PASS RTL - `tb/verilator/gptp_shadow/gptp_shadow_wrap.sv:208`, `:259`, `:303`, `:413`; `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:784`; `hdl/milan/milan_datapath.sv:3259` - new taps expose existing slew and step nets without changing product logic, clocks, reset, widths or CDC. The real counter consumes the observed adjustment. The adopted engine and generator bytes are unchanged from round 1.** The aged-head fixture now disables its hold before release, preventing rearming from contaminating later phases; its original checks still pass.

**Robustness:** examined timed Announce arrival, no-credit retry, both rate signs, active slew, repeated mastership without a slave-rate write, quiet-state preconditions, and the fixture's existing reset/backpressure checks. The transport probe leaves this lens unclean at F1.

**Tests:** examined `sim_main.cpp:2368-2819`, `mutants.py:146-175` and `:272-290`, `test_mutant_lifecycle.py:115-168`, the Makefile's default targets and exact input-copy rules. Applied both original faults independently and ran lifecycle controls. F1 concerns the ordering oracle, not a build failure or a non-executing arm.

**Docs:** checked changed pages against source and receipts, all prior wording fixes, and new comments for prohibited reviewer/round/bench-lane identifiers. New uses of “lane” describe the transport interface, not an implementation lane. Documentation, pin and style checkers pass. Phase 19's claimed grading remains unclean with F1; the rule is not satisfied by weakening that claim.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | #994; REQUIREMENTS.md:172; SUBMODULES.md:949-1059; ROM and route/consumer receipts; sim_main.cpp:2753 | R916-2, applied | f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| RTL | CLEAN | gptp_shadow_wrap.sv:208,259,303,413; KL_gptp_shadow.sv:784; milan_datapath.sv:3259; unchanged donor blobs | R916-2 | f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| Robustness | UNCLEAN, F1 | sim_main.cpp:2482-2819; original fault logs; order-probe.log | R916-2, applied | f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| Tests | UNCLEAN, F1 | sim_main.cpp:2753; mutants.py; test_mutant_lifecycle.py; control/fault/lifecycle logs | R916-2, applied | f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| Docs | UNCLEAN, F1 | README.md:36; SUBMODULES.md:1033,1045; CHANGELOG.md; test guide; PR body; docs-checks.log | R916-2, applied | f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |

## Image identity, limits and pending duties

The two raw firmware ledger receipts independently yield the same 24 SHA-256/path pairs. No firmware image was rebuilt here. Both pin-bearing PNGs also remain byte-identical to round 1:

- `submodule_boundaries.png`: `f5768392ef1ef67e7432aa7247e2cc7b0e61266fc764318b9fc5b8994c04ee66`.
- `timesync_chain.png`: `d209354a3748c15dd2f7f865462e4a9234d93317de24b4dddd04011fe08b7655`.

`checkout-before.log` and `checkout-after.log` prove the exact head/tree, all 1,962 parent tracked files' bytes and modes, index equality, and all tracked bytes/indexes of the five required submodules at their gitlinks. The unused historical `external` checkout remains uninitialized. Probes touched only disposable copies under scratch. No source fixes, commits, pushes, GitHub writes, hardware activity or full banks were performed.

Review-sequence limitation: after the independent source/diff pass, an unfiltered public PR-comment read exposed the prior R915-1 review body before this round's verdict and ledger were written. This did not comply with the requested report-read ordering. No private author material, management source bank or concurrent round-2 reviewer report was consulted. The manager must account for this limitation when judging independent-review acceptance; this report does not claim strict compliance with that sequencing condition.

The IEEE standard itself was not reopened; unchanged clause interpretations inherit the prior review, with the delta checked against repository and donor interface authorities. Physical calibration was NOT RUN. Field skips and the so-called physical simulation leg are not hardware proof. No manager source-head bank ran, and none is claimed. Hosted/act acceptance was not inspected or executed here and remains the manager's responsibility.

The manager still owns the current-dev merge candidate, using source base `300da99beed5bb1c77e4b04af0bb4f9369856e0d` and the supplied live-dev reference `e275d7950ef3385753e6a15d2e191ba855b171ed`, or its latest successor. Build and run the required builder/native banks on that candidate and link its receipts separately from source-head evidence. Resolve F1, obtain corrected-head review for affected lenses, finish both reviews, and satisfy hosted/act gates before any authorized merge. Post-merge containment and issue completion remain pending.

Raw execution receipts are retained, with local filesystem paths redacted in publishable copies. Portable scripts and every publishable receipt are enumerated in MANIFEST.sha256; scratch trees and unredacted temporary originals are excluded.

R916-2 FINISHED
