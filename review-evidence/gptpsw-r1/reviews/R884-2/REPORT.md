[R884] NEGATIVE - exact head 8167b70d89d2a913a07c3b1187f4f2469109eebc

Round R884-2. Tree `66ceef5f516a9804f09a06bb8d02339730cbb02a`. All five lenses applied. One MAJOR finding remains in the revised multiple-response handling. One wording-only RESIDUE is recorded. The original protocol and publication probes pass, but do not clear the new missing-Follow_Up case.

## Findings

### R884-2-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs

**Multiple responders without Follow_Up leave asCapable true throughout the cease.**

**Artifacts:** `sw/firmware/ctrl/gptp/gptp.c:313` (`pd_multi`), `:326` (`pd_send`), `:419` (invalidation only on completion), `:790` (second response while in flight); `sw/firmware/ctrl/test/test_gptp.cpp:430` and `:479`; `docs/design/GPTP_SOFTWARE.md:121`. Reproducer: `probe_multi.inc`, `run_multi.py`, `multi.log`.

**Authority/evidence:** IEEE 802.1AS-2020 11.2.2(c) makes absence of multiple responses a condition for asCapableAcrossDomains, including the single-domain case. Section 10.2.5.1 relates that determination to asCapable. Milan v1.2 4.2.6.2.5 requires ceasing after three successive requests receive responses from multiple clock identities. The new design text also states that any second response is not asCapable.

The probe first earns asCapable with two valid exchanges. It then answers each of three successive requests from two different clock identities, supplying valid request/response stamps but no Pdelay_Resp_Follow_Up. The exact-head output is:

```text
exchange 1: multi=1 run=1 ceased=0 asCapable=1 lost=0
exchange 2: multi=1 run=2 ceased=0 asCapable=1 lost=1
exchange 3: multi=1 run=3 ceased=1 asCapable=1 lost=2
10 seconds after cease: ceased=1 asCapable=1 lost=3
```

`pd_multi` now starts the cease before the exchange completes, but does not clear asCapable. The in-flight path clears it only in `pd_complete`, which requires the absent Follow_Up. The next interval accounts for the outstanding exchange once; subsequent `pd_send` calls return because `ceased` is true. The lost-response counter consequently stays at three instead of reaching its invalidation threshold. The stale state persists until another independent invalidation or the end of the cease. This is a dependency changed by the delta, not an unrelated scope expansion.

The positive control supplies the first responder's Follow_Up after the same two responses: asCapable clears. Both cases compile and execute under UBSan; the failing assertion is the health-state defect, not a compiler or sanitizer failure. `multi.rc` is 1: one failed regression and one passing control. The committed 52 tests and all 40 plants still pass; their multiple-response cases complete the exchange and miss this path after acquiring asCapable.

**Impact:** the port continues publishing a usable peer-delay relationship after detecting multiple responders, retaining it while requests are suspended for the five-minute cease. Time-validity and protocol consumers can trust stale capability. The new documentation's unconditional claim is false for this ordering.

**Required outcome:** multiple-response invalidation must not depend on a later Follow_Up or on future requests that cease prevents. Clear capability/publication consistently with the medium-specific determination, preserve the three-request cease and specified resume rules, and add a regression beginning from an already capable port. Keep the design text consistent with executable behavior.

**Verification:** `python3 -B run_multi.py <checkout>` must pass both cases. Check missing and late Follow_Up, already-completed and still-in-flight exchanges, and same-clock duplicates separately from different-clock cease counting. Preserve the original late-second-responder probe, intervening clean exchange, five-minute/link resume tests, and normal/UBSan campaigns. This retains the affected multi-response portion of R884-1-F3; its originally demonstrated late-second-responder ordering is fixed.

### R884-2-F2 | RESIDUE | Docs

**Artifact:** `tb/verilator/mbx/cdc_pub_mutants.py:48).

**Authority/evidence:** the owner's source-comment rule excludes review-round history from added source comments. The new comment begins `# the defect #966's first review found:`.

**Impact:** wording only; the mutation, expected failure and verdict are unchanged. No privacy or conformance claim is involved.

**Exact fix:** replace the comment with:

```python
# #884, REQ-PTP-07: crossing live words instead of the committed bank can tear a snapshot.
```

**Verification:** inspect the added comment and confirm the mutation tuple is unchanged. Carry to the manager's residue checklist; this item alone would not prevent approval or clean coverage.

## Prior public findings reconciled

The independent delta pass preceded consultation of prior public findings. No current-round report from another reviewer was consulted. Public authorities: [R884-1](https://github.com/kebag-logic/milan-fpga/pull/966#issuecomment-7074604747) and [R883-1](https://github.com/kebag-logic/milan-fpga/pull/966#issuecomment-7075220700).

Procedural limit: the fetched prior public review comment included report material beyond its findings, and was displayed before this round's verdict and ledger were written. That did not preserve the requested written-verdict barrier, although it occurred after the independent delta inspection. The manager should account for this when deciding whether this packet qualifies as the cleared-context external review. The new finding has its own exact-head executable reproduction.

| Prior ID | Disposition | Cause and evidence at this head |
|---|---|---|
| R884-1-F1 | Resolved | `KL_mbx_cdc.sv:479` captures a committed bank; dirty/send-edge accounting preserves a simultaneous commit/latch. Original control and overlapping-update probes each deliver both committed identities, torn=0. CDC bench: 53 checks; five plants caught. Host model: 27 tests including the new snapshot regression. Published split-sw: 152 checks and a failing old-crossing control. |
| R884-1-F2 | Resolved | `gptp.c:619` renews the deadline on a consumed pair; rx_sync records only the pending pair's age. Original two-priority probe expires. Tests also cover continued Announce, separate Announce timeout using complete pairs, and Follow_Up after its own timeout. |
| R884-1-F3 | Original ordering resolved; related handling remains open as F1 above | Original late second-responder probe counts 1, 2, 3 and ceases on the third. Eight-byte clock identity comparison distinguishes duplicate responses; an intervening clean/unanswered request ends the run. Missing Follow_Up exposes the new stale-capability path. |
| R884-1-F4 | Resolved | `gptp.c:714` validates the required TLV before pair/servo updates. Original short-message probe: sync_used=0, sync_ok=0. Tests reject absent, truncated, wrong-type/length/organization/subtype TLVs and accept a further TLV after the valid required one. |
| R884-1-F5 | Resolved | Current PR body and author-r3 exact-head gate README distinguish the rc=124 timeout from the later execution. `xvlog-8167b70d.log`: 90 local HDL plus 52 pinned processor files analyzed, zero findings. No exit-zero skip is called execution. |
| R883-1-F1 | Resolved for reported step/rate defect | `gptp.c:373` bounds/scales unsigned rate spans; `:435` rejects impossible turnaround; `:523` voids local-step-dependent state. All 52 tests pass under UBSan. Original six-case outage table reports zero ms out of asCapable on both ports in every case. The rate-envelope plant is required to fail all five committed step cases; the campaign passes. |
| R883-1-F2 | Resolved | `milan_dp/Makefile:769` appends split-sw to RUN_CASES and serial run; independently executed ci-list ends with split-sw. Scheduling adds 22 seconds to hosted leg 2 and serial duration. Published sweep evidence includes execution. |
| R883-1-F3 | Resolved | `GPTP_SOFTWARE.md:164` names software routes at 9d753fa0 and plane comparison at 40bd7738. All three software receipts agree with the page and meet the documented setup/hold floor. Relevant RTL/firmware are unchanged since the routed ancestor. |
| R883-1-F4 | Resolved | `gptp.h:98` has three callbacks; design page and current PR body say three. Time enters through gptp_port_tick. |
| R883-1-S1 | Taken and verified | Empty paths avoid NULL memory-function arguments at `gptp.c:186`; UBSan passes and the null-comparison plant is caught. |

Remaining prior suggestions are retained as optional. Their code was not changed by this delta:

| ID / severity / attributable lenses | Artifact | Authority, impact, optional outcome and verification |
|---|---|---|
| R883-1-S2 / SUGGESTION / Conformance, RTL, Tests | `milan_datapath.sv`, GPTP_SW_EN_P contract | Exclusivity is enforced by the builder. An RTL elaboration assertion would protect direct instantiations too; verify conflicting parameters fail and supported shapes pass. |
| R883-1-S3 / SUGGESTION / RTL, Tests | `milan_datapath.sv`, g_gptp_sw decode | Fields match current contract literals. Generated constants would prevent future drift; verify unchanged split-sw behavior and field correspondence. |
| R883-1-S4 / SUGGESTION / RTL, Robustness, Tests | `KL_mbx_cdc.sv`, d_ts_take_p_o / ts_send | Present credit/ack ordering holds. Also gating take with !ts_send_r would remove the dependency; verify reordered-credit/ack and normal-throughput cases if adopted. |
| R883-1-S5 / SUGGESTION / Conformance, Robustness | `KL_mbx_rx.sv:737`, shared token bucket | A future second interface can lose tokens to a flooding first interface. Consider per-interface admission with #962; verify isolation under asymmetric flooding. No changed acceptance criterion is inferred. |

## Reviewer-owned coverage ledger

Each lens was applied to changed artifacts and dependencies. Untouched-code conclusions stand, but cannot clear a lens containing the open finding.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | gptp.c:313/373/619/714; mailbox.yaml GPTP_STATE; IEEE 802.1AS-2020 10.2.8.2.1(c), 11.2.2, 11.2.14, 11.2.19.3.3, 11.4.4; Milan v1.2 4.2.6.2.3-6 | R884-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| RTL | UNCLEAN, F1 | KL_mbx_cdc.sv:479; cdc_handshake.sv; milan_dp/sim_split.cpp:693; host publication model; protocol cease/invalidation transitions | R884-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| Robustness | UNCLEAN, F1 | test_gptp.cpp; tb_cdc_pub.sv; protocol/publication/outage/multiple-response probes; wrap, outstanding-transfer reset, partial writes, TLVs, PHC steps | R884-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| Tests | UNCLEAN, F1 | gptp_mutants.py; gptp_arms.py; fw_gtest.py; model_suite.cpp; cdc_pub_mutants.py; milan_dp/Makefile; suite_shards.py; published receipts | R884-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| Docs | UNCLEAN, F1; F2 residue nonblocking | GPTP_SOFTWARE.md:121; MAILBOX_CONTRACT.md; generated mailbox comments; MODULE_MATRIX.md; test READMEs; current PR and author-r3 receipts | R884-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |

## Scope and executed checks

Repository instructions, CONTRIBUTING.md, docs/README.md, issue #884 and its public decisions, requirements/interfaces, history and delta, then public evidence formed the reconstruction. The controlling [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7067495546) permits the fixed-point core and software build while retaining the plane for bench A/B. The [round 2b ruling](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7072401468) freezes held-row/turnaround conditions and records second-MAC/census duties. The original flexPTP-only/no-Vivado proposal is superseded.

`diff-scope.log` binds the full base-to-head diff and the reviewed f15b3a7d..8167b70d delta by SHA-256. The delta spans 27 files. Review concentrated on these changes and every named prior finding at its cause. Actual IEEE 802.1AS-2020, IEEE 802.1AS-2011 and Milan v1.2 texts were consulted; `standards.sha256` identifies them without redistribution.

All execution commands were foreground with children joined. Independent campaigns ran concurrently within 16 jobs. No candidate source edits, commits, pushes, GitHub writes, full banks, hardware runs, Docker/act, host orchestration or sub-agents were used.

| Execution / receipts | Result |
|---|---|
| run_review.py / execution.json | Original protocol/publication probes, core arms and campaign all rc=0 |
| protocol.log | Setup controls pass; both missing-Follow_Up configurations expire; late second responder ceases; missing TLV rejected; zero failed assertions |
| publication-control.log, publication.log | Both committed identities delivered, torn=0 |
| core-arms.log | 52 normal and 52 UBSan tests pass; six original outage cases all zero ms on both ports |
| core-mutants.log | Baseline passes; all 40 plants caught, including earlier 25 and all five required step-case failures |
| run_cdc.py / cdc-baseline.log, cdc-mutants.log | 53 checks, zero failures; five of five plants caught |
| run_model.py / model.log | 27 tests pass, including MbxModelGptp.TheSnapshotIsTheLastCommitWhole |
| run_multi.py / multi.log | rc=1: missing-Follow_Up regression fails; completed-exchange control passes |
| mailbox-generation.log, ci-list.log | Generation/crosscheck/self-test pass; split-sw is final CI case |
| audit_evidence.py / public-evidence.log | All 314 published author-r3 hashes match manifest; YAML identical to prior head excluding doc fields |
| verify_integrity.py / integrity.log | Exact head/tree, tracked bytes/modes, stage-zero indexes and five required initialized submodule pins match; worktree status empty |

Scripts take `<checkout>` as their first argument. Set `VERILATOR` to the scoped 5.050 executable for publication/CDC runs; `tools.log` records its checked identity. Builds/probe copies belong under packet scratch/. The outage adaptation changes only the old global turnaround variable to the current fixture member; original six stimuli/metrics remain. The new probe adds an assertion and positive control without altering production code.

## Published evidence and limits

Source: [evidence commit 86911b961e2f83f3dbe29a5dfc7dd628a5474365](https://github.com/kebag-logic/milan-fpga/tree/86911b961e2f83f3dbe29a5dfc7dd628a5474365/review-evidence/gptpsw-r1), especially author-r3. `verified-evidence.json` records all checked published hashes and redaction status. This verifies published bytes, not unavailable original logs. The commit has no Git signature (%G? = N), and no detached signature was supplied in this packet. Cryptographic signer authentication was not verified; no signed-packet claim is made.

- **Publication:** independent RTL/model probes pass. Published old-crossing controls fail 12/53 checks; the integrated old-crossing control produces the previous torn identity. Corrected split-sw reports 152 checks, zero failures. The bank and handshake were examined together for simultaneous commit/latch priority, queued commits, wrap and resets.
- **Protocol:** completed-pair deadline renewal and required TLV checks match their clauses. Rate arithmetic is bounded before shifting/dividing; local steps void dependent state; the original outage matrix passes. These do not excuse F1's incomplete invalidation.
- **Service conditions at 64a473be:** all seven 8x8/1if held rows meet the unchanged ledger; acmp.last.if0 is 62.41063 ms against 62.62. Turnaround is 0.223/0.309 ms at 1if/2if against 10 ms. Composed maxima are 1.634/1.655 ms against 2 ms; last gptp records are 5.998/7.853 ms. The 2if comparison remains explicitly failed against the 1if-only ledger, not silently accepted or charged as a new finding here.
- **Flood and earlier plants:** unchanged closed-loop receipt at 64a473be reports 48 checks, 490 delivered stamped events, zero unstamped events and zero egress loss with lock retained. All 14 closed-loop and 24 timestamp-unit plants are caught. These are author executions inspected in public receipts, not newly executed full banks.
- **Routes:** 9d753fa0, 8x8/1if --sw-gptp: ExtraTimingOpt WNS/WHS +0.220/+0.056 ns; AltSpreadLogic_high +0.174/+0.056; ExtraPostPlacementOpt +0.154/+0.026. All declared corners exceed the documented +0.03/0 ns floor. Relevant RTL/firmware are unchanged afterward. The page correctly names the plane's separate 40bd7738 route. This reviewer ran no route.
- **Bank provenance:** sweep at 333dc7c5 reports 66/67, tsn_fuzz failing its stale matrix check. Regenerated matrix and tsn_fuzz rerun at 09c5934a pass. Firmware/Yosys/census/harness receipts remain at their stated ancestors with relevant dependencies unchanged. The exact-head 73-check batch includes an xvlog timeout followed by a separately successful execution, both visible. Some larger published files are verdict extracts/hash inventories rather than complete raw logs.
- **Contract:** registers, fields, offsets, channels, events and version remain 2.5 and unchanged from round 2b. Only GPTP_STATE prose and generated comments change. The host snapshot models committed-bank contents at the write, not CDC physical latency.

## Pending manager duties

This is source review, not merge acceptance. Publish this packet, obtain a fix and re-review for F1, carry F2 to the residue checklist, complete the independent review bar, and validate the eventual current-dev candidate with builder/native receipts. Source base `59b098841b1e2826aaf7a38b557faa5345f91c82` and supplied live-dev tip `e275d7950ef3385753e6a15d2e191ba855b171ed` are distinct. No manager source bank at this exact head is claimed or inferred. Hosted/act acceptance remains the manager's duty; hosted contexts were not inspected or accepted here.

The GPTP_SW_EN_P census shape remains owed before onward merge; #962 owns the second product MAC. Bench slave/grandmaster qualification remains owed before deleting the retained plane RTL or shipping this path. Physical calibration is NOT RUN. Field campaigns and simulated oscillator/PHY behavior are not hardware proof. No bench-qualification or 2if-ledger defect is newly charged to this PR.

REPORT.md and files listed in MANIFEST.sha256 form the publishable packet. Scratch is excluded. Published local receipts normalize checkout/packet path prefixes only; receipt-redactions.json records original and published hashes, with original bytes retained under scratch. Fetch the named evidence commit into the checkout before rerunning audit_evidence.py; it extracts only the author-r3 packet and manifest into scratch when needed.

R884-2 FINISHED
