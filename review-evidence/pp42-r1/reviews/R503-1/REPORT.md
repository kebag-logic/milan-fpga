[R503] NEGATIVE - exact head 72facc6d48807808e4d97a454a0ecceb2769ac9e

Issue #42 / PR #164, round R503-1. Tree `3274eac801f2ebb6b96ca031c12752a2a1b91bcc`; source base `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`. One open MINOR finding makes Docs UNCLEAN. The requested notification behavior and all nine new controls pass review. No BLOCKER, MAJOR, RESIDUE or SUGGESTION findings.

**R503-1-F1 — MINOR — attributable lenses: Docs.** The documented Domain-notification latency uses the wrong starting point.

- **Location:** [`tb/pp_top/README.md:2497`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/72facc6d48807808e4d97a454a0ecceb2769ac9e/tb/pp_top/README.md#L2497). The public handoff's “Measured on the wire” paragraph repeats the claim.
- **Authority/evidence:** The README says 495 clocks after the MRPDU's last byte. `NotifyBench::feed`, `notify_phases.hpp:83–94`, clocks four idle cycles after injecting that byte. <bench-switch-model> and DN2 take `t0` after this helper returns (`:1755–1757`, `:1772–1774`). An observation-only disposable probe records the received final byte, helper return and transmitted final byte using the same bench clock convention. Adoption: 340030 → 340034 → 340529; return to default: 580098 → 580102 → 580597. Both are **499 clocks from the final injected byte**, or 495 from helper return. See [raw trace](receipts/timing-probe.log), [parsed timestamps](receipts/timing-probe.json), and [reproduction script](scripts/probe_timing.py). The unchanged 15 checks still pass.
- **Impact:** The public measurement understates that interval by four clocks. This does not invalidate the notification checks or establish an RTL defect. It changes a reported measurement and therefore does not qualify as RESIDUE under the supplied rule.
- **Required outcome:** Correct the README's 495 to **499** when measuring from the final injected byte. Alternatively, explicitly identify helper return as the start of the 495-clock interval and state its four-clock offset. Carry the same correction into the next public evidence summary, superseding the immutable handoff's incorrect caption. No RTL or acceptance weakening is needed.
- **Verification:** Re-run the observation-only probe at the revised head, retain DN's 15 passing checks, and confirm that the documented interval and its endpoints agree with the trace. No source fix was made during this review.

Reconstruction followed the requested order. No tracked AGENTS.md or CONTRIBUTING.md was present; the supplied workspace instructions were read first, followed by `docs/README.md` and repository entry points. The [issue body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/42) and [frozen assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/42#issuecomment-6008771904) supplied acceptance. Authorities examined next were REQ-NET-002/REQ-SRP-004, `02_interfaces.md` §4.3, `06_aecp_engine.md` §§6.10/7, `08_timing.md` F08.1 and `10_srp_engine.md` §6.1. The complete diff and all three commits were then examined independently, before public executable evidence and prior review findings. [Authority excerpts](receipts/authority-excerpts.txt), [diff](receipts/source.diff), and [history](receipts/history.txt) preserve the examined artifacts.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen acceptance; REQ-NET-002; interface §4.3; AECP §§6.10/7; SRP §6.1; DN stimulus/oracle; captured frame bytes | R503-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| RTL | CLEAN | Complete diff; `KL_srp_domain.sv:143–184`; top event OR at `:4018–4020`; notification selection/pending at `KL_aecp_notify.sv:665–672,1073`; unchanged counter limiter at `:1098–1106` | R503-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| Robustness | CLEAN | Fresh-model isolation; boot/registration premises; isolated link trigger; frame count/silence windows; completed-run mutation grader; nine executed controls and exact planting audit | R503-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| Tests | CLEAN | DN 15/15; GSI 6182/6182; counter spacing 9/9; nine named kills; independent byte comparison; baseline/head control definitions; default-build dispatch | R503-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| Docs | UNCLEAN | README DN/mutation record; verification §8.4; public PR body/handoff; measured latency discrepancy R503-1-F1 | R503-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |

The Conformance pass established that DN feeds a differing Class A declaration after registration, expects exactly one unsolicited GET_AVB_INFO at the registered controller, and compares the complete frame. Both identical declarations expect no DOMAIN_CHANGE and no frame. DN2 returns the operating values to the default through the received-declaration adoption arm at `KL_srp_domain.sv:184`. The LINK_DOWN revert at `:157` is a distinct transition; the assignment asks for a declaration, and the source/README distinguish these correctly. The integrator's static mapping fixture is outside the requested live-state integration scope.

The RTL pass found exactly five changed test/documentation files, +297/−12, and no RTL, port, register or parameter change. The Domain strobe and independent link edge still feed the AVB notification OR; the path-change input remains separate. Link grading runs at DEFAULTS and checks that neither edge raises DOMAIN_CHANGE, making deletion of the link term observable. The one-second limiter remains specific to GET_COUNTERS. DN's spacing helper and 1.2-second observation windows respect the requested spacing without modifying the limiter.

The Robustness pass checked missing registration, incomplete restore, missing Domain strobe, duplicate identical-declaration notifications, wrong descriptor, extra GET_AS_PATH, and either missing event input. Each fails named checks. The campaign requires a successful build, completed tally, nonzero run exit, and every named failure; a refusal or build failure cannot count as a kill. All 15 new checks are covered by observed failure sets.

**Reviewer-executed evidence**

| Check | Result | Receipt |
|---|---|---|
| Unmodified DN | 15 checks, 0 failures | [domain-golden.log](receipts/domain-golden.log), rc 0 |
| Existing integrated GSI path | 6,182 checks, 0 failures | [existing-gsi.log](receipts/existing-gsi.log), rc 0 |
| Counter spacing | 9 checks, 0 failures; closest gaps 115077 / 115070 / 115077 clocks | [counter-spacing.log](receipts/counter-spacing.log), rc 0 |
| New mutation campaign | golden PASS; 9/9 KILLED; all builds rc 0 and mutant runs rc 1 | [results.json](receipts/domain-mutants/results.json), [campaign log](receipts/domain-campaign.log), rc 0 |
| Older control preservation | all 56 definitions, edits, suite commands and named checks unchanged; all 65 controls plant exactly once | [control-audit.json](receipts/control-audit.json) |
| Independent frame comparison | all four 66-byte frames exact; u=1, SUCCESS, cdl 40, AVB_INTERFACE 0, sequences 0–3 | [wire-audit.json](receipts/wire-audit.json), [script](scripts/audit_wire.py) |
| Static checks | diff whitespace check passes; module matrix 94 rows, 0 untested | [diff-check.rc](receipts/diff-check.rc), [matrix.log](receipts/matrix.log) |
| Observation-only timing probe | 15 checks, 0 failures; confirms F1 | [timing-probe.log](receipts/timing-probe.log), rc 0 |

| New control | Observed failing checks |
|---|---|
| `avb_domain_term_dropped` | DN1b, DN1c, DN2b, DN2c |
| `avb_link_term_dropped` | DN4b, DN4c, DN4d, DN4e |
| `asp_takes_domain` | DN1b, DN2b |
| `avb_notify_not_interface` | DN4c, DN4e, DN1c, DN2c |
| `domain_same_readopted` | DN3, DN3b |
| `adoption_no_strobe` | <bench-switch-model>, DN1b, DN1c, DN2, DN2b, DN2c |
| `revert_strobes_at_defaults` | DN4 |
| `registry_never_claims` | DN0, DN4b–DN4e, DN1b, DN1c, DN2b, DN2c |
| `restore_never_done` | shared boot premise |

The campaign and independent focused build ran concurrently under a foreground coordinator; children were joined before completion. The driver used `--jobs 2`, make used `-j16`, and a wrapper capped nested compilation at four workers per build, at most twelve together. The pinned compiler's 5.050 identity was verified before use. [Resource evidence](receipts/resources.json) records memory below the 12 GiB cap. No full processor/parent/gPTP/builder/synthesis bank, hardware run, container workflow, source fix, commit, push, merge or GitHub write was performed.

**Public evidence and prior findings**

The [immutable public packet](https://github.com/kebag-logic/milan-fpga/tree/355c335c33fc42c3b9c406d1032ce5e4108eca2b/review-evidence/pp42-r1) contains a handoff, PR body, adoption patch and publication manifest. All three published hashes match that manifest. Its tables report the full source sweep, pp_top 10,444 → 10,459, preservation of older campaign records, 65/65 notification controls, and the 17 consumer gates at parent `28f9666feab2b2ba287643c63ed3a16b1e0bb863` with the #148 patch. Those broad results were not independently rerun here; raw broad-bank logs are not present in that directory. Local DN corroborates the added 15 checks, and the diff confines their execution to the first/default build. Older controls' planting and definition preservation were independently checked; their complete execution history remains the public handoff's evidence.

The published #148 patch is 966 bytes with SHA-256 `bbd0301dc7e576f51f92d24c8d140eda0666f9c6699806649365110e7ecfea83`. Public parent metadata confirms companion gitlinks: external `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`, gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and stream support `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. See [parent-gitlinks.json](receipts/parent-gitlinks.json). No local parent candidate was built or claimed.

At the recorded exact-head hosted snapshot, documentation and portability jobs succeeded in both [PR](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37427673979) and [push](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37427666734) runs. Suite jobs were still in progress and are not counted as passes. The compiler-build step was skipped after successful cache restoration; it is not an executed test. See [hosted checks](receipts/hosted-checks-final.json) and [PR job steps](receipts/hosted-pr-jobs-final.json). Hosted/local workflow acceptance remains the manager's duty.

The [independent verdict and ledger](receipts/independent-verdict.md) were written before checking prior public review findings. The PR returned **zero formal reviews and zero inline review comments**; its two issue comments were review-start notices. There are consequently no prior public FINDINGS to resolve or retain at this head. The issue returned the assignment, taken notice and review-ready notice; no additional manager bank-evidence comments were available in these snapshots. The supplied manager-bank pass is distinguished from independently executed receipts above. No other reviewer's report or private author material was read.

**Limits and pending manager duties**

This verdict covers the exact source head, not a future integration commit. Resolve F1 and obtain review of the revised head. The manager must make the single final merge incorporating processor main's #134 and #22 changes, build the current-dev candidate from the stated live dev `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`, publish its evidence, and return that delta for review. Source validation against `e6a759de` and the older parent consumer run do not certify that candidate.

The manager owns final hosted/local workflow acceptance, the full completion bar, the second independent review, and publication. The public consumer builder summary includes one NOT RUN gate; field skips and **physical calibration NOT RUN** are not hardware proof. This review used no board or calibration, did not inspect copyrighted specification PDFs, and does not claim live integrator mapping-state coverage or isolated notification coverage of the LINK_DOWN Domain-revert strobe.

Final [before](receipts/tree-before.json)/[after](receipts/tree-after.json) audits are identical: all **556 tracked blobs and executable/symlink modes** match HEAD, the index tree matches the required tree, status is empty, and this processor repository contains **zero submodule gitlinks**. Disposable builds and probes remain under `scratch/`, excluded from publication. Reproduction scripts accept an exact-head source directory and pinned compiler path; use a fresh packet directory for new disposable builds. `MANIFEST.sha256` lists publishable files using packet-relative paths.

R503-1 FINISHED
