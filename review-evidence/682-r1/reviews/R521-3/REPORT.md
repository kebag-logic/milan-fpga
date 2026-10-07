[R521] POSITIVE - exact head fe8294978dd306706d659dc06468d0c07d43ce3e

External independent review of issue #682 / PR #692, round R521-3.
Tree: `1d9982e2943098fd1003e069dc7df8cc210d98ca`.
Source base and observed live dev: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.

All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains.
No new finding was raised. One existing wording residue and one optional
suggestion remain, as recorded below. This verdict covers the stated source
head and does not authorize merge or discharge physical acceptance.

The review followed the repository contract and documentation index, then
[issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/682), the
[assignment](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6018127147),
[render ruling](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028334443),
requirements and interface authorities, full source diff and history, and
[immutable public evidence](https://github.com/kebag-logic/milan-fpga/tree/8d4e0732588d09f1f94f41aea7c7c39110da09a2/review-evidence/682-r1).
The independent verdict and ledger were written to `independent_pass.md`
before opening prior review bodies. Prior findings and the
[round-3 correction assignment](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6043632388)
were then reconciled against that pass. No private author material was read.

The full `e21c1ca0..fe829497` diff has 18 changed paths. The scoped
`5428b044..fe829497` delta has exactly three: `CHANGELOG.md`,
`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, and `docs/reference/SUBMODULES.md`.
The two round-3 commits are direct descendants without an intervening merge.
No source, test, record, generated artifact or gitlink changed after `5428b044`.
The `cb359db3..fe829497` correction is exactly the prescribed two-line removal
of synchronous-reset attribution to C11. Receipts: `source_delta.patch`,
`round3_delta.patch`, `manager_correction.patch`, `history.txt`, and
`tree_integrity.json`.

Every claim in `CHANGELOG.md:44-71` was checked:

| Lines | Claim and evidence |
|---|---|
| 46-48 | The adopted pin contains exactly the six first-parent processor merges for PRs #159, #156, #161, #160, #162 and #164. Public merge SHAs and ancestry are recorded in `claim_checks.json`. |
| 49-50 | GET_COUNTERS spacing follows the waiting job through grant, with the post-grant MAC-stall limitation retained. Checked against PR #159 and `protocol-processor/hdl/aecp/KL_aecp_notify.sv:1444`. No wire-gap guarantee is asserted. |
| 51-52 | `tb/verilator/milan_dp/sim_nxn.cpp:973` extends observation only while a frame remains incomplete, bounded by `cyc + 2048`. |
| 53-54 | PR #156 documents byte interfaces, TX backpressure and complete FCS-good RX frames; checked against its merge and `protocol-processor/docs/architecture/02_interfaces.md:135-160`. The synchronous-reset wording was already present at `ead80360`; commit `371505db` belongs to PR #157's ancestry. |
| 55-56 | PR #160 and the talker/listener registrar branches implement expiry-then-reception outcomes: Lv/LeaveAll finish MT; New/Join renew IN and cancel obsolete timers. Checked at `KL_srp_talker_fsm.sv:720-744` and `KL_srp_listener_fsm.sv:747-782`. |
| 57-59 | PR #161 and `KL_aecp_notify.sv:1253` defer held DEREGISTER until the active round ends. Subsequent controllers retain the round's notification; the held job's contents remain unchanged. |
| 60-61 | PR #162 moves existing declarations above use in originator and RX validator. `scripts/xvlog.budget:33` records zero processor findings; the published per-file synthesis table records zero processor Synth 8-6901 across all 46 sources, separately retaining one parent warning. |
| 62-63 | PR #164 adds Domain and link-edge notification tests in `tb/pp_top/notify_phases.hpp:1643-1847`. It grades triggers; mapping words remain integrator-owned, consistent with the processor interface guide and parent GET_AVB_INFO face. |
| 64-65 | The complete `hdl/top/protocol_processor_top.sv` bytes match across pins. Processor changes add no parent-facing port, parameter or register requiring adaptation. |
| 66 | The committed resource JSON is byte-identical to the public combination-F record. All three endpoints identify F; policies equal the source base. |
| 67 | Both `2ad2f845` ROM ledger digests equal the `ead80360` rows. ROMs were not regenerated in this delta round. |
| 68, 71 | Product firmware, capture harness/receipt, parent HDL and configurations match source dev. Fresh capture checking regrades the receipt and confirms its firmware digest. VERSION remains unchanged. |
| 69-70 | The named withdrawal cycles and default-map read are manager duties in acceptance 5. The stream/counter soak remains required by the issue, despite its omission from these two bullets. |

`docs/reference/SUBMODULES.md:158-185` gives the same adoption account.
The corrected C11 row no longer attributes reset documentation to this pin.
`claim_checks.json` supplies independent top, ROM, firmware, flow and ancestry
checks. The public baseline F, effective recipes, synthesis table, image
receipt, source-closure record and render differential were inspected at the
immutable evidence commit. Nine selected public payloads were verified against
their Git blob identities; `public_evidence_receipts.json` retains their hashes.
The two actual public clean-epoch outputs are byte-identical, 3,746 bytes,
SHA-256 `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b`.
This corroborates retained evidence; it is not a new render campaign.

The recipe now matches baseline F. Its five measurement-preparation commands
all include `--single-thread-synthesis`, and lines 105-113 require it for
`route-1x1`, `ooc-1x1` and `ooc-8x8`. Each recorded flow starts with
`set_param synth.maxThreads 1`, retains `general.maxThreads 32`, and preserves
its directives. The existing `--integrated-clock` instruction remains necessary
for standalone comparisons; F records 20 ns. Three direct calls to the gate's
`judge` function accept identical endpoint records with result 0. Removing
only the worker setting gives result 2 for all three endpoints, naming the
flow mismatch. These are comparison-layer probes, not synthesis or CLI runs.
The helper self-test separately exercises actual CLI preparation for default
and capped scripts, inventory refusals, endpoint refusals and clock controls.

[R521] PASS Conformance - `CHANGELOG.md:44-71`, `SUBMODULES.md:158-185`, issue #682 acceptance and public scope rulings, processor PRs #156/#159-#162/#164 - The adoption claims and recipe reflect the accepted scope. No acceptance, clause or interface requirement changes in this delta. Source engineering evidence remains bound to the unchanged artifacts; acceptance 5 remains manager-owned.

[R521] PASS RTL - `round3_delta.patch`, `protocol-processor/hdl/top/protocol_processor_top.sv`, notification/SRP branches cited above, `tree_integrity.json` - No RTL or integration wiring changed since the reviewed engineering baseline. Top identity and the new prose's clock, interface and state-transition claims agree with the pinned implementation.

[R521] PASS Robustness - `PP_SHADOW_BASELINE_RECIPE.md:105-113`, `syn/ooc/pp_resource_gate.py:310-324`, `claim_checks.json`, `sim_nxn.cpp:973` - Wrong-flow comparisons fail closed at all three endpoints. Frame-observation extension remains bounded, and the grant/wire distinction is explicit. No new reset, malformed-input, ordering or backpressure implementation path is introduced.

[R521] PASS Tests - `focused_results.json`, `pp_baseline_selftest.log`, `capture_check.log`, `resource_policy.log`, `tree_integrity.json` - Every requested gate passes at the reviewed bytes. Helper controls distinguish default from capped preparation; capture controls detect census/clock/timing faults. Test artifacts are unchanged from the settled engineering baseline, whose behavior probes were not rerun.

[R521] PASS Docs - `CHANGELOG.md:11,44-71`, `SUBMODULES.md:163`, `PP_SHADOW_BASELINE_RECIPE.md:105-113,124-126,189-192,265-268,457-464`, `manager_correction.patch` - Every new changelog claim and the mandatory worker-cap procedure were checked against source, history and records. The precise reset-attribution correction is present, and all documentation gates pass.

| Executed command | Result | Receipt |
|---|---|---|
| `python3 scripts/gen_toc.py --check` | 0; 139 annotated pages | `gen_toc.log`, `.rc` |
| `python3 scripts/docs_check.py` | 0; zero findings | `docs_check.log`, `.rc` |
| `python3 scripts/check_doc_style.py` | 0 | `check_doc_style.log`, `.rc` |
| `python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0; 313 added lines, 339/339 controls | `check_em_dash.log`, `.rc` |
| `python3 syn/ooc/pp_baseline.py --selftest` | 0; default and capped preparations pass | `pp_baseline_selftest.log`, `.rc` |
| `python3 scripts/check_nvm_capture.py` | 0; census, clocks, firmware and both timing arms agree | `capture_check.log`, `.rc` |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0; three endpoints | `resource_policy.log`, `.rc` |
| `git diff --check e21c1ca024d37ea188ad15b5c8f9c2dae18628df HEAD` | 0 | `git_diff_check.log`, `.rc` |

The first contents/em-dash attempts returned 2 because the locked Markdown
renderer was absent. Their refusal receipts are retained separately. Installing
the exact hashed dependencies inside `scratch/markdown-venv` enabled both final
passes. No shared installation changed. Other successful gates were not
repeated. All child processes were awaited by foreground commands.

Prior public findings are reconciled at `fe8294978dd306706d659dc06468d0c07d43ce3e`:

| Finding | Disposition | Evidence |
|---|---|---|
| R520-1-F1, MINOR Docs | RESOLVED | New changelog section and generated contents entry; full claim audit above. |
| R520-1-F2, MINOR Docs | RESOLVED | Required flag in prose and all five preparations, matching all endpoint identities; helper and flow controls pass. |
| R520-1-S1, SUGGESTION Docs | RESOLVED | PR validation block uses `(cd tb/verilator/milan_dp_render && make tdm8render-mutants)`. |
| R520-2-F1, MINOR Docs | RESOLVED | Exact prescribed two-line fix; reset wording traces to the previous pin through PR #157. |
| R520-2-S1, SUGGESTION Docs | RETAINED, optional | Changelog and SUBMODULES still omit the soak from their two named post-merge duties; issue acceptance 5 retains it. |
| R520-3-R1, RESIDUE Docs | RETAINED | Current PR reproduction paragraph still names the predecessor head, as detailed below. |
| R521-1 | No finding to resolve | Positive engineering baseline at `5428b044176f95248e6916dc00dd89c0df154078`; changed documentation has been reviewed afresh here. |
| R521-2 | VOID | Stopped before verdict; no coverage is banked from it. |

R520-2-S1 - SUGGESTION - Docs - `CHANGELOG.md:69-70`; `docs/reference/SUBMODULES.md:181-183`.
Authority/evidence: issue #682 acceptance 5 also requires stream/counter soak.
Impact: these two summaries name only the other two bench duties; they do not
claim to replace the acceptance list. Optional outcome: add
`The manager also soaks all streams and counters.` after each default-map line.
Verification: compare both summaries with acceptance 5. This optional suggestion
leaves Docs CLEAN.

R520-3-R1 - RESIDUE - Docs - PR #692 body, "How to get into the same state",
expected-values paragraph.
Authority/evidence: it names `cb359db3424c895010e89b4f9688347857008c85` as the
expected checkout head, although the Status section correctly records the
manager correction and the current head is `fe8294978dd306706d659dc06468d0c07d43ce3e`.
Impact: a reproducer sees a stale expected SHA. This is PR-body wording only;
no measured result, test, code, generated artifact, clause claim or privacy rule
changes. Required exact fix: replace only that expected parent-head value with
`fe8294978dd306706d659dc06468d0c07d43ce3e`. Keep historical validation heads unchanged.
Verification: re-read that paragraph against the published head. The manager
carries this item to the residue checklist; it leaves Docs CLEAN.

The prior findings were read from
[R520-1](https://github.com/kebag-logic/milan-fpga/pull/692#issuecomment-6043628972),
[R520-2](https://github.com/kebag-logic/milan-fpga/pull/692#issuecomment-6044553004),
and, after the independent verdict, the findings sections of
[R520-3](https://github.com/kebag-logic/milan-fpga/pull/692#issuecomment-6044736430).
The latest inventory has no formal reviews or inline comments.
`public_inventory.json` identifies the observed public artifacts.

Reviewer-owned coverage ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue and decisions; CHANGELOG:44-71; SUBMODULES:158-185; processor PR ancestry/interfaces; baseline/capture records | R521-3 | fe8294978dd306706d659dc06468d0c07d43ce3e |
| RTL | CLEAN | Full source and round-3 diffs; pinned top; notification/SRP branches; parent HDL and gitlink byte audit | R521-3 | fe8294978dd306706d659dc06468d0c07d43ce3e |
| Robustness | CLEAN | Recipe:105-113; resource gate:310-324; three matching and three wrong-flow controls; frame drain:973 | R521-3 | fe8294978dd306706d659dc06468d0c07d43ce3e |
| Tests | CLEAN | Five required gates; helper CLI controls; capture/resource checks; unchanged test-artifact census | R521-3 | fe8294978dd306706d659dc06468d0c07d43ce3e |
| Docs | CLEAN | Changelog claim table; SUBMODULES correction; five recipe commands; public scope/evidence; prior-finding reconciliation | R521-3 | fe8294978dd306706d659dc06468d0c07d43ce3e |

This is a delta review, not a new full engineering campaign. The settled
R521-1 engineering baseline is retained only for unchanged artifacts. Full
parent/processor/time-plane/synthesis/builder banks, image builds and hardware
were not run. The manager's reported source banks remain distinct from the
final current-dev candidate. Public REVIEW READY comments provide author
results at their stated heads; private round-3 logs and private implementation
artifacts were not inspected. No hosted job or local workflow replica was run
or accepted by this reviewer. A skipped hosted context is not an executed test.

Physical calibration NOT RUN, field skips, simulation results and offline
image preflight are not hardware proof. The known #657 differential exception,
post-grant MAC-stall limitation, unmet 60% LUT objective, and existing timing
coverage limitations retain their previously recorded scope. No new evidence
here reopens their settled engineering disposition.

The manager still owns protected hosted/local-replica acceptance, the final
current-dev candidate build and required validation, completion of independent
review coverage, explicit merge authorization, merge and containment. After
merge, acceptance 5 requires the #608 withdrawal cycles, #658 default-map read,
and all-stream/counter soak before issue completion. The residue above remains
on the manager's checklist. This report performs no GitHub write.

Final checkout verification hashes every tracked blob's actual bytes and checks
filesystem modes and index entries directly against HEAD, with replacement
objects disabled. It verifies 1,164 parent blobs, 562 processor blobs, 104
time-plane blobs and 214 stream-library blobs. Required gitlinks and checkouts
are `2ad2f845dd583f8310075fa2380cb60a04fd091a`,
`5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and
`48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused historical external
checkout remains uninitialized; its gitlink is verified. No candidate file
was edited, so no source restoration was necessary.

To reproduce, use the exact checkout and initialized required submodules.
Run `python3 fetch_public.py` from the packet to fetch public inputs into its
`scratch/`. From the checkout, run the packet's `audit_tree.py` and
`verify_claims.py`. Run `run_focused.py` using an interpreter with
`tools/markdown/requirements.txt` installed with `--require-hashes`; all five
requested gates execute and are awaited. Run the two additional capture/resource
commands in the table with the repository's normal Python dependencies.
Scripts reside in the packet and take the checkout from the current directory.
No build or campaign output belongs in the checkout.

`MANIFEST.sha256` lists every publishable receipt and script, with paths relative
to the packet. `REPORT.md` is also listed. `scratch/` is never published.
The helper log replaces only its absolute packet prefix with `$PACKET`;
all result lines are retained, and the original remains in scratch.
`log_normalization.json` records both hashes. No private reasoning is included.

R521-3 FINISHED
