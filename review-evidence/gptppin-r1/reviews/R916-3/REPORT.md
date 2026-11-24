[R916] POSITIVE - exact head fc6870cab13f74149864b80b6480ddb3641cb936

Round R916-3, external independent review of issue #994 / PR #995. Both remaining test findings are resolved at their causes. All five lenses are CLEAN for this narrow re-review. No new finding, suggestion or wording residue was found. This is a source-review verdict, not merge authorization or a claim that the complete merge bar has passed.

Reviewed tree: `47c0ec30481efe50fd892060ebeb61ef9bc423c2`. The round delta is `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21..fc6870cab13f74149864b80b6480ddb3641cb936`: commits `567eaa48ba` and `fc6870cab1`, six paths, tests and documentation only. The overall adoption was located against train head `300da99beed5bb1c77e4b04af0bb4f9369856e0d`; unchanged implementation keeps its previous verdict, with dependency identity checked here.

Authorities examined: AGENTS.md and CONTRIBUTING.md, docs/README.md, [#994's frozen acceptance](https://github.com/kebag-logic/milan-fpga/issues/994), REQUIREMENTS.md section 4, GPTP_PLANE.md integration seams, GM_LOSS_RECOVERY.md, the ticket/ledger contracts, and [#818's route floor](https://github.com/kebag-logic/milan-fpga/issues/818). Public evidence is the [packet at 1fe0516a](https://github.com/kebag-logic/milan-fpga/tree/1fe0516af44a9d94eb1f5667d32eb67919851eba/review-evidence/gptppin-r1), especially `author-r3`. The issue snapshot has no comments; the retrieved PR discussion supplies review starts and prior findings, not a manager source bank.

**Resolved findings**

| Prior ID | Severity and attributable lenses | Disposition and exact-head evidence |
|---|---|---|
| R916-2-F1 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED. `tb/verilator/gptp_shadow/sim_main.cpp:2751` defines the boundary, and `:2761` requires `fall != 0 && txf_cyc[i] < fall`; the following assertion requires exactly one matching Announce. README.md:36 names the same boundary. The stalled-transport replay fails this exact check. |
| R915-2-F1 | MINOR; Tests, Robustness | RESOLVED. `sim_main.cpp:2851` adds the unfenced reserve arm. It holds a real Sync record, reaches five outstanding frames, checks the reserve, asCapable, unsealed state and absence of a barrier, then grades silence and retry. Removing only ANNTX's credit gate fails `#106 reserve: no master Announce reaches the lane without credit`. The seal arm remains separately and accurately described as retry coverage. |
| R915-2-R1 | RESIDUE; Docs | RESOLVED. SUBMODULES.md:984 now gives the complete rule before the 1x1 instance, in the requested sentence order. |
| R915-2-R2 | RESIDUE; Docs | RESOLVED. Source section/function comments, README phase rows and campaign references, SUBMODULES record and PR table use 19/20/21. The existing PHC trajectory remains phase 18. |
| R915-2-R3 | RESIDUE; Docs | RESOLVED. CHANGELOG.md:71 reads “The cadence counts from that Announce (802.1AS-2011 Figure 10-15).” |
| R916-1-F1 / R915-1-F1 | MAJOR; Conformance, Robustness, Tests | RESOLVED in full for the requested platform coverage. Round 2 established the takeover/rate coverage; this round closes the ordering and credit clauses. The original delayed-Announce and retained-rate defects still produce completed failing tallies. |
| R915-1-F2 | MINOR; Robustness, Docs | Tracking finding remains RESOLVED. [#997](https://github.com/kebag-logic/milan-fpga/issues/997) is open, records both-pin reproduction and requires no-retry detection; the PR and adoption record link it. The original finding explicitly required public tracking. The underlying pre-existing AECP silence is NOT fixed or credited as clean behavior here. |
| R915-1-R1/R2/R3; R916-1-R1 | RESIDUE; Docs | Remain RESOLVED. The shipping-selection rule, recipe order and figure edition are correct; the PR now counts eight later first-parent commits after the routed commit. |
| R915-1-S1 | SUGGESTION; Docs | Remains adopted. The PR distinguishes the extra +0.030 ns hold test from #818's zero hold floor and records the 0.012 ns hold fall. |

The race observations use the same bench cycle: accepted last beats are recorded at `sim_main.cpp:373`, and the post-edge published-role transition at `:438`. Strict inequality rejects an Announce on or after the re-election edge. No recorded fall yields zero qualifying frames and fails. Frame selection checks the Announce message type and this station's grandmaster identity at `:2489`.

The reserve arm's outstanding count is ledger entries plus queued results. Its `8 - 4` threshold agrees with the unchanged wrapper defaults and `hdl/ieee8021as/gptp_plane/KL_gptp_txticket.sv:259`. It runs before the seal arm so a defective sealed takeover cannot prevent reaching the new credit assertion. Releasing the hold first disables re-arming, drains results and grades both the first retry and subsequent cadence.

**Executable evidence checked**

These are published author executions, verified against the published manifest and inspected against the source. They are not new reviewer simulation runs.

| Case at exact head | Completed tally | Relevant observation |
|---|---|---|
| Pristine shadow run | 424 PASS, 0 FAIL; rc 0 | Race last beat +285 clocks; re-election +1,281. Reserve has five outstanding frames; first released Announce at +2,000,103. |
| Original ordering probe's transport stall | 423 PASS, 1 FAIL; rc 2 | Last beat +4,659, re-election +1,281; named race assertion fails. |
| Original ANNTX no-credit probe | 421 PASS, 3 FAIL; rc 2 | Named reserve assertion sees one forbidden Announce; retry count and timing also fail. |
| Original delayed-Announce probe | 416 PASS, 6 FAIL; rc 2 | Immediate-send, race and both retry arms fail. |
| Original retained-slave-rate probe | 420 PASS, 4 FAIL; rc 2 | Zero-rate and oscillator counter-advance assertions fail for both settled signs. |

`receipt_check.py` verifies that the published stall replay and the campaign mutation produce identical current-head bytes. The original order-probe patch's first hunk is the same stall; its old diagnostic-only second hunk is superseded by the source's own clock print. The no-credit campaign edit removes exactly the gate removed by the prior probe. All thirteen current mutation anchors are unique.

The campaign receipts cover 13/13 controls. The two new controls and both adopted donor controls fail their named checks. Two interrupted slices retain one completed detection each; their remaining controls have separate completed receipts. A timeout alone was not counted as a detection. Three inherited controls still fail other checks than their expected names; this remains disclosed, and is not misreported as thirteen named detections. The exact-head lifecycle receipt passes with thirteen controls. Its fixtures test orchestration; the real fault receipts establish behavioral detection.

`artifact-audit.log` verifies all 322 published author files: 89 from round 1, 57 from round 2 and 176 from round 3. Every `published_sha256` matches. The evidence commit has no signature header and the packet supplies no detached signature; content integrity is verified, but cryptographic signer authentication is not claimed.

**Carry judgment and image identity**

The carry of both `milan_dp` legs is accepted for this source delta. Their round-2 receipts at `f97e49fe` each finish 212/212, including the 0x22 and 0xFE clockAccuracy cases. The exact-head attempts end at the foreground-window timeout and remain NOT COMPLETED.

The entire delta consists of four shadow-harness files and two Markdown files. The integration Makefile, source, generators, configuration, local headers and all gitlinks are unchanged. Independently expanding both integration recipes finds 125 existing file arguments in this fresh checkout, none changed; the author's receipt reports 127 file arguments. These counts have different populations: this audit requires each file to exist. No local integration file references the changed shadow harness directory. This is unchanged-input ancestor evidence, not an exact-head execution pass, and does not waive the manager's hosted or candidate gates.

All 291 diagram/gitlink entries are identical to `f97e49fe`. The two pin-bearing PNG hashes remain:

| Artifact | SHA-256 |
|---|---|
| `docs/diagrams/submodule_boundaries.png` | `f5768392ef1ef67e7432aa7247e2cc7b0e61266fc764318b9fc5b8994c04ee66` |
| `docs/diagrams/timesync_chain.png` | `d209354a3748c15dd2f7f865462e4a9234d93317de24b4dddd04011fe08b7655` |

All 24 firmware digest receipts agree across rounds; no firmware image was rebuilt or independently retrieved from its original build directory. Independent default-ROM regeneration produces SHA-256 `4eb21cefc8d769df4a764402aead970b59be96cb3fa267d25af9d1857935f083`, matching the tracked image and ledger. No synthesis input changed in this round. The prior selected route receipts therefore carry: 8x8/1if 46,246 LUT, -375 against base, worst WNS/WHS +0.066/+0.036 ns; 1x1/1if 32,639 LUT, -41, +0.170/+0.024 ns. Both meet #818 at all four corners. This review performed no route or builder run.

**Retained optional suggestions**

These retain their prior severity; none blocks coverage.

- **R915-2-S1 | SUGGESTION | Docs, Tests** - README.md:35 now records the slewing arm's opposite frequency-change sign and its presence-only grade. The disclosure is adopted. The optional donor investigation remains pending; its purpose is to assess the frequency-change meaning after a phase transient, not to claim it was fixed. Verification would be a donor issue and clause-backed evidence.
- **R915-2-S2 | SUGGESTION | Robustness, Tests, Docs** - `sim_main.cpp:2734` / SUBMODULES.md:1045. An Announce already queued before takeover remains an optional additional ordering arm. The current arm arrives within the deadline millisecond and detects the old delayed-beat fault. The adoption record now states that resolution accurately. The author declined expansion; any future arm should demonstrate its actual pre-takeover queue order and defect detection.
- **R915-2-S3 | SUGGESTION | Tests, Docs** - `scripts/suite_shards.py` / `author-r3/receipts/rtl/shard-projection.txt`. Exact-head hosted runtime remains unmeasured here. The 840-950 s estimate and projections are not measurements. The manager should record completed hosted duration before replacing the registered value; verify the measured shard still meets its budget.
- **R915-2-S4 | SUGGESTION | Tests, Robustness** - `test_mutant_lifecycle.py:345`, unchanged `ownership()` fixture. The inherited quiet-make sensitivity remains outside this narrow fix. Optional outcome: isolate its make flags and verify both ordinary and quiet invocations. No repair is claimed.
- **R915-2-S5 | SUGGESTION | Tests, Docs** - `mutants.py`, `credit_never_withheld`, and its round-3 slice receipt. The stale expected-check name remains disclosed; that distinct wrapper fault is detected by quiet-start guards, not the new ANNTX reserve assertion. Optional outcome: track and repair the named-check mismatch, then demonstrate that exact control failing its intended assertion. No new issue was created by this review.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #994 acceptance; REQUIREMENTS.md:172; GPTP_PLANE.md:57; sim_main.cpp:2751,2851; unchanged route/input receipts | R916-3 | fc6870cab13f74149864b80b6480ddb3641cb936 |
| RTL | CLEAN | six-path delta; unchanged wrapper and product/gitlink identities; KL_gptp_txticket.sv:259; sim_main.cpp:347,438,2835 | R916-3 | fc6870cab13f74149864b80b6480ddb3641cb936 |
| Robustness | CLEAN | sim_main.cpp:2741,2773,2851,2910; stall/no-credit receipts; retained reset and rate arms' unchanged inputs | R916-3 | fc6870cab13f74149864b80b6480ddb3641cb936 |
| Tests | CLEAN | mutants.py:65,183; test_mutant_lifecycle.py:161; complete control/fault tallies; thirteen-control union; integration input audit | R916-3 | fc6870cab13f74149864b80b6480ddb3641cb936 |
| Docs | CLEAN | README.md:35,90; SUBMODULES.md:983,1036; CHANGELOG.md:71; PR phase/limitation text; unchanged diagram and image hashes | R916-3 | fc6870cab13f74149864b80b6480ddb3641cb936 |

Each lens was applied to the delta and its dependencies. RTL coverage carries the previous production assessment after identity checks; it is not a fresh full-bank review. Source comments added here describe behavior and reason without prohibited bench/lane/reviewer identifiers. No new source-comment residue was found.

**Limits, procedure and pending duties**

`independent-pass.md` records the delta verdict and ledger before deliberate prior-finding reconciliation. An initial unfiltered public-discussion response exposed earlier review text before that record; this is a procedural limitation. No private author material or management source bank was consulted. No other review report was deliberately used to form the delta verdict; the subsequent reconciliation read finding sections. The review should not be represented as having avoided all prior-text exposure.

No new behavioral campaign was needed to falsify an unresolved claim: the current-head published probes already reproduce the exact requested faults, and the independent anchor/input/hash audits establish their correspondence. The scoped simulator's 5.050 identity was verified; no simulation was executed by this reviewer. No full bank, hardware access, source fix, commit, push, GitHub write, container run or merge occurred.

Source validation is separate from the final current-dev candidate. There is no manager source bank at this head and none is inferred. The manager still owns both-review completion, hosted/local-replica acceptance, actual runtime evidence, construction and validation of the candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, publication of builder/native candidate receipts, merge authorization, post-merge containment and issue completion. Hosted job execution was not audited here; skipped contexts are not counted as executed jobs. Physical calibration was NOT RUN. Field skips, simulations and route timing are not hardware proof.

`integrity.log` proves tracked blob bytes, executable modes and complete index equality at the exact source head and all five initialized submodule gitlinks. The unused external gitlink remains unchanged and uninitialized. Source status is clean. Disposable extraction and ROM output reside only under `scratch/`, excluded from publication.

Reproduce the read-only audits with `python3 -B audit.py SOURCE PACKET` and `python3 -B receipt_check.py SOURCE PACKET` after fetching evidence commit `1fe0516a`. `MANIFEST.sha256` lists the scripts and raw receipts retained for publication; it excludes scratch. Source gates and author fault receipts remain explicitly distinguished throughout this report.

R916-3 FINISHED
