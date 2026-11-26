[R936] NEGATIVE - exact head f4833e16a07d07494277aba8dc7a5de19320c20b

R936-2, external independent delta review of issue #970 / PR #1015.
Tree: `acc0b819bec698855f98c81f52a4a04abcde6afd`.
Source base: `4df125b8c11f0e1706b3c1e489f3e66a5d856b18`.
Previous reviewed head: `0ad0e5180558a376f6064d0b33884ed40af6e196`.

The fresh-sample implementation and all five named prior findings are resolved at their causes. One new MINOR remains: the budget harness publishes a stale numeric model-access count. Two wording residues and one presentation suggestion are also recorded. This is not merge authorization or closure of #970.

## Scope and independence

Reconstructed AGENTS.md/CONTRIBUTING.md, docs/README.md, the issue body and public rulings, requirements and interface authorities, the 23-file source-base diff and five-commit delta history, then public executable evidence. The independent verdict and five-lens ledger were written before opening the prior public review findings. The final numeric cross-check below changed that initial verdict. No other current-round review was read.

The [accepted scope](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7174054394) retains immediate LINK_UP delivery and the declared 6.0 s. Milan v1.2 5.6.3.5.2/.3 and Tables 5.49-5.51 retain the 0-2,000/0-4,000 ms draws; IEEE 1722.1-2021 6.2.4.2.2 supplies the distribution and seed authority. Fresh sampling at each qualified transition is the explicit project ruling. The later attribution decision is context, not extra scope or physical proof supplied by this review.

## New finding

### R936-2-F1 - MINOR - RTL, Tests, Docs

**Artifact:** `tb/verilator/ctrl_service_budget/scenario.py:266` and `:944`; propagation through `grade.py:639` and `run.py:568`; `sw/firmware/ctrl/adp/adp_mbx.h:123` and `test/test_adp.cpp:146`.

**Title:** LINK_UP's published model-access count remains 11 after the fallback path grows to 12.

**Authority/evidence:** The scenario's `Probe.accesses` is explicitly the host model's measured or bounded accesses (`scenario.py:112`). `grade.py` copies it into `model_accesses`; `run.py` publishes it in the numeric “Mailbox accesses (model)” column. Both the ordinary advertised sequence and the self-test fixture still set it to 11.

The core now samples on LINK_UP. Without a wired clock, `adp_mbx.c:63` therefore performs one additional `mbx_now_ms()` read. The header and MAILBOX_SPLIT correctly update that path to 12. The independently executed real adapter/model test prints:

```text
C0 LINK_UP -> TMR_DELAY armed                 12 accesses (bound 12)
```

`receipts/focused/adp-baseline.log:107` records that measurement. `check_model_accesses.py` instantiates both scenario constructors at 1x1/1if and 8x8/1if: all four publish 11 against the measured 12 (`receipts/model-accesses.json`, exit 1). The corrected-value control agrees with the measured bound. The budget image is the size-fixture composition (`build.py:343` and `sw/firmware/ctrl/test/ctrl_aecp_image.c`); it does not call `adp_mbx_set_clock`. The platform's separately wired clock does not make the size fixture's fallback count 11.

**Impact:** Generated CPU evidence understates this model comparison by one access. The measured CPU times and deadline verdicts are not computed from this field and are not invalidated by this finding. It changes a numeric evidence artifact, so the owner's RESIDUE exception does not apply. This delta introduced the dependency change even though the two literals themselves were retained.

**Required outcome:** Make both emitted model counts agree with the exercised fallback composition, currently 12, and refresh affected generated evidence. Preserve the distinction from the wired platform path. No timing budget needs widening.

**Verification:** The focused adapter measurement remains 12; both constructors emit that value; `check_model_accesses.py` exits 0. Spot-check the regenerated `model_accesses` field and report column at both CPU points. Retain a consistency check that detects stale count metadata.

## Wording residue and suggestion

### R936-2-R1 - RESIDUE - Docs

- **Artifact:** `sw/firmware/ctrl/test/adp_first_mutants.py:121`.
- **Evidence/authority:** The new comment says “the reviews of PR #1015”; the owner requires source comments to describe behavior and reason with issue/requirement IDs, rather than review history.
- **Impact:** Process narration only; no test or clause claim changes.
- **Exact required fix:** Replace the line with `# #970: each qualified rise samples through the adapter and platform (IEEE 1722.1-2021 6.2.4.2.2).`
- **Verification:** Added-comment inspection. H9/B25-style identifiers elsewhere name executable cases, not bench lanes.

### R936-2-R2 - RESIDUE - Docs

- **Artifact:** `docs/reference/SUBMODULES.md:1199-1207`.
- **Evidence/authority:** The new PR #40 block separates “Parent tests accept 57 to 2047” from “They refuse 0 and 55.” Documentation should keep the referent clear.
- **Impact:** Paragraph flow only; all values and claims remain unchanged.
- **Exact required fix:** Move “They refuse 0 and 55.” directly after “Parent tests accept 57 to 2047.”
- **Verification:** Read the resulting paragraph; preserve the numbers verbatim.

### R936-2-S1 - SUGGESTION - Docs

- **Artifact:** Live PR body, opening and “Linked Issue / roles”.
- **Evidence:** Duplicate `[A847]` opening and three “to be assigned” placeholders, despite the public review-start records.
- **Impact:** Presentation only; the public task can still be reconstructed.
- **Suggested outcome:** Keep one opening prefix and replace the placeholders with the already recorded executor/internal/external role identities.
- **Verification:** Compare the body with the public role records. Optional; no lens is unclean because of this suggestion.

## Prior findings reconciled

The prior findings are [R936-1](https://github.com/kebag-logic/milan-fpga/pull/1015#issuecomment-7178340125) and [R935-1](https://github.com/kebag-logic/milan-fpga/pull/1015#issuecomment-7179085015). Their dispositions apply to this exact head:

| Prior ID | Disposition and root evidence |
|---|---|
| R936-1-F1, MAJOR, all five lenses | Resolved. Pinned `src/adp.c:98` samples in `leave_down`; startup and qualified LINK_UP call it behind the guards. The adapter only returns the sample. H9 counts calls, H10 varies only the link-time clock, B27 exercises both interfaces through the platform. Removing LINK_UP sampling fails H9, H10 and B27; the current documentation describes the actual pin. New F1 above is separately retained. |
| R935-1-F1, MAJOR, Tests/Docs | Source causes resolved. Python idiom exits 0, long modules 10/10 and overlong lines 0/0. The pinned contents gate exits 0, including CHANGELOG. Local raw logs retained. Hosted completion remains a manager prerequisite, not a claimed pass. |
| R935-1-F2, MINOR, Docs/RTL | Resolved. SPLIT_CONTROL_MEMORY now names `c34e7d8b` and its four actual baseline values; the four new deltas are +264/+272/+264/+256 B. See the receipt reconciliation below. |
| R935-1-F3, MINOR, Tests | Resolved. B25 clears the clock binding on reset and uses three origins one microsecond apart. Millisecond, 1,024-us-granule and late-wiring controls each fail B25 by name. |
| R935-1-F4, MINOR, Docs/Conformance | Resolved by implementation, not retitling: the merged stack pin now takes the fresh LINK_UP sample. The current handoff and title are true. Historical ready text remains historical evidence, not current execution evidence. |
| R935-1-R1 | Resolved: FR_NFR now attributes distribution to H4-H6 and seed terms to H7. |
| R935-1-S1/S2 | Addressed: the co-simulation README explains the mixed NOW_MS fallback; the boot fixture resets clock origins and binding. |
| R935-1-S3 | Addressed in the PR: fixed-duration runs change idle polling with the draw, so whole-run CPI is not presented as work cost. CPU row/share comparisons are retained. |
| R935-1-S4 | Remains an explicitly disclosed, pre-existing generator-order limitation. Published boot receipts use `PYTHONHASHSEED=0`; deterministic generation remains separate follow-up work. No new regression is attributed to this delta. |

## Independent examination and execution

**Conformance:** Read FR_NFR 2.1.1 and MAILBOX_SPLIT's ADP contract against the pinned event paths. The sum remains 4,311 ms with 1,689 ms margin inside 6.0 s. Draw ceilings, GM-in-DELAY handling, GM-in-WAITING advertising and available_index remain intact. No link hold or direct adapter write to core state was added. H7 covers plain MAC-plus-clock modulo 2^32, including wrap; zero generator state is guarded. Statistical claims are limited to the tested ensembles.

**RTL/architecture:** No parent HDL, mailbox contract, configuration or SoC-source delta against `4df125b8`. Reviewed the clock callback lifetime and boot ordering (`ctrl_plat.c:135,401,432`), fallback access growth, core-owned mixing, submodule ancestry and the merged dependency boundaries. `c3bff8f3dea03870ea7ae62965db360b509ee3b3` is a two-parent merge, and its tree `4064709bec5ebb15b18f16b13a5bae94688a4d56` equals `95902060`'s. The source base is an ancestor. F1 is the remaining resource-evidence inconsistency.

**Robustness/Tests:** Ran 84 ADP tests, 59 one-interface boot tests and 60 two-interface boot tests, all passing. They include first/subsequent rises, startup while up/down, duplicate and disabled events, fallback clock, wrap/zero behavior, GM ordering, stale timer tags, owed-frame backpressure and interface isolation. H10 produced 915 distinct first delays from 1,024 link-time samples, chi-square 17.2 against 30.58. Eighteen distinct planted defects produced 19 required failing executions, all caught by the intended assertions. These include missing/ignored transition samples, duplicate/disabled sampling, missing seed terms and all three platform defects. Three concurrent workers used four compile jobs each; all were joined.

The published focused `plants.log` ends `rc=1`: it catches 28/28 defects but runs the global test-name census against a narrowed table, reporting 141 unnamed tests. It is scoped kill evidence, not a green full campaign. Independently inspecting the intact 865-entry table reports zero unnamed tests (`receipts/audit.json`). No compile refusal is counted as a caught defect.

**Docs:** Both previously failing gates were rerun successfully. An initial contents-gate attempt refused missing dependencies; its refusal is retained, followed by the successful pinned-environment run. Reviewed changed contracts, pin records/diagram manifest, memory figures, reboot arithmetic and co-simulation timing. The longer scenario waits admit the unchanged 4 s range without relaxing service budgets. The co-simulation's shutdown at 32 s follows the fourth advertisement's 31.05 s worst-case schedule. F1 affects generated numeric documentation.

## Published evidence reconciliation

Verified all 42 author files against their published manifest digests: first packet at `40ce56ee579d00874e4c9db98893f0742498aee3`, current packet at `af092a85bcda1d60fab649ca42e2b013996ee21e`, directory `review-evidence/adp970-r2/author`. These are author source-head receipts, not a manager source bank. No detached signature was supplied and the evidence commit is unsigned; hash integrity is verified, independent signature authentication is not claimed.

After recording the independent verdict, also checked the two prior public baseline ledger receipts and their matching manifest hashes. The current source-head ledger gives:

| Point | Baseline ROM B | Current ROM B | Delta B | SRAM B | Planned tiles |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 127,568 | 127,832 | +264 | 56,736 | 45.5 |
| 1x1/2if | 129,352 | 129,624 | +272 | 59,168 | 46.5 |
| 8x8/1if | 141,680 | 141,944 | +264 | 100,096 | 59.5 |
| 8x8/2if | 143,432 | 143,688 | +256 | 117,632 | 64.5 |

The measured `c34e7d8b` and `5de21ff3` baseline figures agree. Compared with `4df125b8`, the relevant parent platform/memory sources remain unchanged; the public pin-only ledger reports no additional cost from `a795471c`. Thus the stated baseline is explicit and reproducible. No new four-point image build was run by this review. Platform structure sizes remain 18,048/19,840/19,136/21,888 B.

CPU receipts at both points were inspected and compared, not rerun: 75 paired probes at 1x1, no misses; 90 at 8x8, the same seven pre-existing backlog-owed misses. Work-pass maxima are 1.468 and 1.820 ms, below 2 ms. Maximum reported positive row shifts are +0.411 and +0.621 ms; no new deadline miss is reported. Round-4/current comparisons have no row differing by more than 0.1 ms. Existing misses remain misses. The source packet also records successful firmware/coverage, boot, twin, co-simulation, reboot, hooks, budget self-test and memory-plan checks. Reboot arithmetic is 851.665 + 3,500 + 3 + 92.325 = 4,446.990 ms, leaving 15,553.010 ms; configuration load remains unmeasured.

## Reviewer-owned ledger

UNCLEAN rows name the applying round; they do not bank clean coverage.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #970 rulings; FR_NFR 2.1.1; pinned adp.c:98,254,263; G1-G5/H7-H10 execution | R936-2 | f4833e16a07d07494277aba8dc7a5de19320c20b |
| RTL | UNCLEAN (F1) | adp_mbx.c:60; ctrl_plat.c:401,432; source-base HDL diff; memory/CPU receipts; scenario.py:266,944 | R936-2 applied; none clean | f4833e16a07d07494277aba8dc7a5de19320c20b |
| Robustness | CLEAN | test_adp.cpp H8-H10 and adapter/owed-frame cases; test_plat_boot.cpp B25-B27; focused named-failure logs | R936-2 | f4833e16a07d07494277aba8dc7a5de19320c20b |
| Tests | UNCLEAN (F1) | focused/results.json; both docs-gate logs; model-accesses.json; scenario.py/grade.py evidence path | R936-2 applied; none clean | f4833e16a07d07494277aba8dc7a5de19320c20b |
| Docs | UNCLEAN (F1) | MAILBOX_SPLIT, FR_NFR, SPLIT_CONTROL_MEMORY, SUBMODULES, reboot/co-simulation records; run.py:568 numeric report | R936-2 applied; none clean | f4833e16a07d07494277aba8dc7a5de19320c20b |

## Reproduction, limits and pending duties

From the packet directory, pass the exact checkout and packet paths:

```sh
python3 -B verify_evidence.py CHECKOUT PACKET
python3 -B focused_checks.py CHECKOUT PACKET
python3 -B audit_receipts.py CHECKOUT PACKET
python3 -B check_model_accesses.py CHECKOUT PACKET
python3 -B verify_checkout.py CHECKOUT PACKET
```

The model-access check is expected to exit 1 at this head. The other commands exit 0. Documentation commands were `python3 -B scripts/check_py_idiom.py` and `scripts/gen_toc.py --check` under an isolated environment installed from `tools/markdown/requirements.txt` with required hashes. Disposable environments, source copies and builds stay under `scratch/`, excluded from publication.

Tracked bytes, file kinds, executable modes and stage-0 indexes were directly compared with committed blobs: 3,360 entries across the parent and five required initialized submodules. All match; the optional external gitlink remains uninitialized. No source edits, commits, pushes, GitHub writes, full banks, local workflow replica or hardware work were performed.

One read-only hosted snapshot is retained. Documentation jobs were running; wire-accountability and docs-check-no-git had executed successfully. The exhaustive selector succeeded, but preflight was running and the exhaustive shards were queued. No completed exhaustive acceptance is claimed. Pending/skipped contexts are not execution evidence.

There is no manager source bank at this head. The manager owns hosted/local-replica acceptance and the final current-dev candidate, using source base `4df125b8c11f0e1706b3c1e489f3e66a5d856b18` and live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, with builder/native receipts linked at the merge turn. Source-head tests do not validate that candidate. Fix and re-review F1, carry the residues, obtain the required independent approvals and explicit merge authorization, then perform post-merge containment.

Physical calibration: NOT RUN. Field skips are not hardware proof. Deterministic clock/identity ensembles do not measure physical boot entropy or establish hardware delivery within 6.0 s. The issue's remaining physical acceptance and wider release obligations remain with the manager.

R936-2 FINISHED
