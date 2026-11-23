[R900] POSITIVE - exact head 66b4def34dcbc0d371ce4eb339d3d0226875befa

External independent delta review R900-2 of [issue #983](https://github.com/kebag-logic/milan-fpga/issues/983) / [PR #986](https://github.com/kebag-logic/milan-fpga/pull/986). All five lenses are CLEAN. Both prior MINOR findings are resolved at their causes. One publication-wording RESIDUE remains. This is a source-head review, not merge authorization or merge-candidate validation.

Tree: `b5bba478993ff213d953aa73ca5fecc8d5476c8a`. Source base: `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. Previous reviewed head: `677d605f37c3a80654df1dd2cde053b57242845b`. One commit changes three files, +78/-13: a dispatch expression, comments, documentation and focused tests. [delta.diff](delta.diff) and [source.diff](source.diff) retain both requested comparisons.

**Authorities and independence.** Reconstructed the repository contract, documentation map, frozen issue acceptance, product/interface authorities, diff/history and public evidence. The [manager scope ruling](https://github.com/kebag-logic/ti-sitara-am65x-bsp/issues/29#issuecomment-7096504049) authorizes descriptor-only generation and a host-only scheduler entry; it does not restore an FPGA operating-system product. REQUIREMENTS sections 1/8, architecture, PP_DESCRIPTOR_OWNERSHIP and ENDSTATION_BUILDER govern the boundary. The [current issue evidence](https://github.com/kebag-logic/milan-fpga/issues/983#issuecomment-7100207805) states the widest-format decision and unchanged calculation.

The independent diff pass preceded reading [R900-1's public findings](https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7099822461). No private author material or other reviewer's report was read. Submitted reviews and inline threads are empty. [public-state.json](public-state.json) and [issue-evidence.json](issue-evidence.json) preserve the public inputs. Untouched code retains prior results as directed; this round checks the delta and its dependencies.

**Prior finding dispositions.**

| Prior ID | Severity and all attributable lenses | Disposition at this head |
|---|---|---|
| R900-1-F1 | MINOR; Conformance, Robustness, Tests | RESOLVED. `endstation_builder.py:4802` uses `_req`, matching `_load_board`. `test_builder.py:30846` adds three malformed-board cases. |
| R900-1-F2 | MINOR; Docs | RESOLVED. `ENDSTATION_BUILDER.md:1248` and `endstation_builder.py:4813` describe shared widest advertised width at the configured rate. No calculation change. |
| R900-1-R1 | RESIDUE; Docs | RETAINED as R900-2-R1 below: Status still describes the current published head as unpushed. |

F1 verification: independent probes reproduce `ConfigError: board: missing required key 'target'` for `[]`, `""`, and `["ax7101"]` at base/current head, versus AttributeError at the prior head. The ADP CLI returns controlled exit 2 without traceback. Gate 42 passes 31/31 plants, retaining valid controls and FPGA-owner cases. The verified published discrimination log shows the three new tests failing under the prior builder. Null/integer boards raise TypeError at base/current head; that pre-existing boundary remains out of scope.

F2 verification: `_check_host_tspec()` returns `(217, 73)`. An independent in-memory current-format mutant fails that test at its intended assertion. Literal arithmetic agrees with Milan v1.2 4.3.3.2 Table 4.4: `24*8+24+1=217`, `24*2+24+1=73`. Both explanations now state maximum `channels_per_frame` across all advertised talker formats, shared across talker rows at `clocking.sampling_rate_hz`.

IEEE 802.1Q-2018 35.2.2.8.4 a) defines the maximum produced frame excluding media framing; 35.2.2.8 requires withdrawal and two LeaveAllTime periods before changed FirstValue reuse. These clauses support the stated conservative fixed-reservation policy. `sw/firmware/ctrl/plat/ctrl_plat.c:226` installs fixed source TSpecs; `sw/firmware/ctrl/aecp/aecp_commands.c:124` and `:307` check running state and format changes. Those dependencies are unchanged. [standards-audit.json](standards-audit.json) identifies the independently consulted primary PDFs by hash and clause. No new sampling-rate-transition or physical behavior is claimed.

**Remaining finding: R900-2-R1.**

[R900] RESIDUE Docs - PR #986 body, Status and reproduction comment - Publication wording predates the current push.

- Authority/evidence: live PR metadata and the review-start comment identify `66b4def34dcbc0d371ce4eb339d3d0226875befa`. Status names `677d605f` as published and says the current commit becomes published when pushed. The checkout command still says “once pushed”. See `public-state.json`.
- Impact: stale publication prose only; no measurement, figure, test, generated artifact, conformance claim, privacy rule or verdict changes. All lenses remain clean under the assigned RESIDUE rule.
- Required outcome / exact fix: replace the complete Status paragraph beginning “Published head:” with: “Published head: `66b4def34dcbc0d371ce4eb339d3d0226875befa`. The evidence below is local source-head evidence; hosted acceptance is tracked separately.” Remove “once pushed” from the checkout command's trailing comment. Preserve incomplete-bank disclosures.
- Verification: compare the revised paragraph and command comment with the PR head. The manager carries this to the residue checklist.

No other finding or suggestion arose from the delta.

**Five-lens results.**

[R900] PASS Conformance - `sw/builder/endstation_builder.py:4802`, `:4821`; `docs/ENDSTATION_BUILDER.md:1248`; `focused-gates.log`; `delta-probes.json` - Controlled validation is restored; documentation matches the unchanged calculation and cited clauses. The host image/generator checks pass. The example remains 5,784 bytes, SHA-256 `9a59e2741913d93e9ad71bba890ce65d75fc4101170e9427997a00aa15ee29dd`, with ENTITY/ADP 1/2 and the required AAF/CRF inventory. The unchanged board-owned entity.conf path retains R900-1's generation evidence; it was not re-executed this round.

[R900] PASS RTL - `delta.diff`; `sw/firmware/ctrl/loop/ctrl_loop.h:393`; `evidence-audit.json`; `delta-probes.json` - No RTL, firmware, scheduler-header, clock/reset/CDC, interface or gitlink delta since R900-1. All three published 245-artifact hash maps match across base/prior/current head: five FPGA configurations, own/split/all-fabric placements. Independently regenerated 45 artifacts for FPGA 1x1, 8x8 and Arty at their own placements match the current published hashes. Gate 41 recompiles host-only selection, refusal without the macro and unchanged listed FPGA rows. Prior RTL coverage is retained and its generator dependency rechecked.

[R900] PASS Robustness - `sw/builder/test_builder.py:30845`, `:30912`; `delta-probes.json`; `focused-gates.log` - The repaired container cases use ConfigError, valid controls load, all 31 refusal plants pass, and the ADP CLI follows its intended error path. Null/integer base behavior is recorded without expanding scope. Prior host-boundary and packer behavior is unchanged.

[R900] PASS Tests - `sw/builder/test_builder.py:30746`, `:30846`; `focused-gates.log`; `delta-probes.json`; published `author-r2/receipts/discriminate.log` - Four selected gates pass: bad configs, documentation key map, host generators, host refusals. Gate 32 retains 116 matching keys. Gate 41 checks 64 host keys, image/three headers, no-build refusal, scheduler guard and TSpec distinction. The new regression fails against the previous dispatch; the current-format mutant fails at the intended assertion. This is focused execution, not a full bank.

[R900] PASS Docs - `docs/ENDSTATION_BUILDER.md:1248`, `:1278`; builder comments at `:4797` and `:4813`; `docs-check.log`; `evidence-audit.json`; PR body - Derivation and refusal descriptions match the implementation. Added source comments state behavior/reason without prohibited lane, round, reviewer or issue-comment identifiers. The independent documentation check reports zero findings. All 24 published documentation/quality command summaries record rc=0, including em-dash, bare-metal and Python checks. R900-2-R1 is wording residue only.

**Reviewer-owned ledger.**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | builder:4802/4821; ENDSTATION_BUILDER:1248; clauses; focused-gates.log; delta-probes.json | R900-2; unchanged scope retained from R900-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| RTL | CLEAN | delta.diff; ctrl_loop.h:393; evidence-audit.json; 45 regenerated artifacts | R900-2 dependency check; unchanged RTL from R900-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| Robustness | CLEAN | test_builder.py:30845/30912; delta-probes.json; focused-gates.log | R900-2; unchanged boundaries from R900-1 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| Tests | CLEAN | test_builder.py:30746/30846; focused-gates.log; delta-probes.json; discrimination receipt | R900-2 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |
| Docs | CLEAN; one RESIDUE | ENDSTATION_BUILDER:1248/1278; builder comments; docs-check.log; published receipts; PR body | R900-2 | 66b4def34dcbc0d371ce4eb339d3d0226875befa |

**Limits and pending manager duties.**

The [immutable packet](https://github.com/kebag-logic/milan-fpga/tree/7095fc64b8b27f841e7dffaab2be953430487b5e/review-evidence/linuxprof-r1) has 55 author/author-r2 files whose published hashes verify. Original path-redacted hashes are not asserted equal to published bytes. The evidence commit has no signature header; signature verification returns 1 without output. Content integrity and the public commit reference are verified, but signer authentication is unavailable. No signed-packet claim is made. Hash equality alone does not prove execution; attribution rests on public source-head receipts, supplemented by independent probes.

No manager source bank exists at this exact head, and none is inferred. Author evidence here covers focused gates, identity and documentation. The earlier 114/115 function-level subset result belongs to `677d605f`, not this head. Gate 1b, the complete builder/native bank union and firmware shards/mutation campaigns remain manager obligations on the final current-dev candidate. Physical calibration was NOT RUN; its function-level pass/skip is not calibration evidence. Field skips and desk checks are not hardware proof.

The manager must construct the candidate from live dev at merge time, validate the required banks and publish receipts. The assigned live-dev reference `e275d7950ef3385753e6a15d2e191ba855b171ed` differs from the source base. No candidate was constructed here. Source-head hosted/act acceptance remains separate: this review credits no executed hosted job, skipped context or full source bank. Two independent positives, no review in flight, explicit merge authorization, containment, issue closure and board completion remain required. The PR snapshot still lacks an assigned internal reviewer.

No scheduling/preemption measurement, physical timing, release soak, daemon installation or board conformance was tested. The disclosed board CRF-clock limitation remains outside this descriptor-generation verdict. No full parent/processor/gPTP/synthesis/builder bank, container runner or host CI orchestrator ran. The scoped RTL simulator was not used. No source fixes, commits, pushes, GitHub writes, author contact, sub-agents or shared installs occurred.

**Reproduction and integrity.**

Portable scripts accept `REPO PACKET`: `audit_evidence.py`, `probe_delta.py`, `check_integrity.py`. Fetch the immutable evidence commit read-only before the audit. Run the audit before probes, which consume its verified manifests. Set `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=PACKET/scratch`. Focused commands, from REPO:

```sh
python3 -B sw/builder/test_builder.py --gates test_bad_configs_rejected,test_builder_doc_key_map,test_host_profile_feeds_the_generators,test_host_profile_refusals
python3 -B scripts/docs_check.py
```

Commands ran in foreground processes; independent probes and documentation checks overlapped within the assigned limits. No job remains running. Disposable trees remain under packet `scratch/` and are excluded from publication.

Initial reviewer setup failures are retained separately: the gate selector required inventory order; a probe initially expected the prior dispatch to give TypeError for null rather than AttributeError; image metadata strings needed encoding before hashing. The corrected probe preserves production tests and base/current-head expectations. These are reviewer harness errors, not source failures or weakened tests.

[integrity-result.json](integrity-result.json) proves exact HEAD/tree, all 1,936 parent blobs' raw bytes/modes, complete stage-zero index equality, and pinned bytes/index for protocol-processor, gPTP processor, verilog-axis, tsn-c-stack and lwSRP. No hidden index flags exist; status is clean. The unused external gitlink remains unchanged and uninitialized. Tracked bytes were never mutated; no restoration was needed.

`MANIFEST.sha256` lists publishable scripts, diffs, logs, statuses and JSON receipts with relative paths. Verify from the packet directory with `sha256sum -c MANIFEST.sha256`. Publish only listed files and this report; never publish `scratch/` or standards extractions.

R900-2 FINISHED
