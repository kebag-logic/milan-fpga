[R529] NEGATIVE - exact head 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70

R529-1 is complete. All five lenses were applied independently. One MAJOR and one MINOR remain open. The shipping all-fabric implementation is unchanged by the F2 delta.

**Scope and reconstruction**

Reviewed tree `3a359107aafc930166375961fc18a3e93392e7e5`. Read the operating contract, contribution rules, documentation index, frozen #665 acceptance and public decisions, linked requirements and interfaces, then changes and executable evidence. The assigned `021b9c1f..1a5d70fa` range includes the FC follow-up. F2 itself is the single commit `db9aa8c9b135b34ff3d070a979dee70440b37cc6..1a5d70faba6a9b01aab6bb868c12e4c7023e0c70`, affecting 23 files. FC-only changes were examined as context, without claiming a new FC review.

The protocol authority was IEEE Std 1722-2016 Annex B, including B.2, every Table B.7 cell, Table B.8, B.3.4-.6 and B.4. The parent engine was a differential subject, not the oracle. [Static examination](receipts/static-review.md) records the cell-by-cell results, CSR consumer trace and artifact references. [Identity receipt](receipts/identity.json) identifies the standard, simulator and public author archive. No other reviewer's report or private author material was read.

**R529-1-F1 - MAJOR - Conformance, RTL, Robustness, Tests**

Artifact: `sw/firmware/ctrl/app/ctrl_app.c:52` (attachment and channel opening at lines 52-54), with `sw/firmware/ctrl/loop/ctrl_loop.c:74` and `sw/firmware/ctrl/test/test_maap_mbx.cpp:249`.

Title: The MAAP application enables reception without enabling its receive interrupt.

Authority/evidence: #665's bare-metal directive requires the mailbox-driven event loop; NFR-SCOUT-03 and H-MAAP require service from original RX publication within 10 ms. `ctrl_app_start_maap` calls `ctrl_app_start`, which opens the loop while only ADP is bound. `ctrl_loop_open` consequently writes an ADP-plus-events IRQ mask. Attaching MAAP and changing FILTER_EN afterward never adds its RX interrupt bit.

The independent probe reproduces this at both one and two interfaces: `FILTER_EN=0x9`, `IRQ_ENABLE=0x101`, a complete 17-word MAAP RX record pending, and IRQ low. Enabling precisely the missing MAAP bit raises IRQ for that same pending record; explicit service then handles its conflict. The eleven standing host cases still pass in each probe binary. See [one-interface receipt](receipts/review-probes-if1.log), [two-interface receipt](receipts/review-probes-if2.log), and [probe source](scripts/review_probes.cpp).

Impact: With the supported waiting/WFI platform port, an accepted MAAP packet arriving after the loop sleeps cannot wake it. Handling waits for an unrelated event, potentially far beyond the 10 ms budget. Conflict DEFEND and allocation-loss handling are affected. The present application test inspects filter/state/slot setup and calls service directly, so it does not detect the missing wake-up.

Required outcome: The explicit MAAP composition must configure the MAAP receive interrupt while preserving ADP and event interrupts. An idle loop must wake and service an accepted MAAP record within the original input budget.

Verification: Add a standing test through `ctrl_app_start_maap` and the wait/wake path at one and two interfaces, including a planted missing-interrupt defect. Retain the filter, timer-slot, default-entry and allocation tests. Re-run H-MAAP and coverage at the corrected head.

**R529-1-F2 - MINOR - Conformance, Tests, Docs**

Artifact: `sw/firmware/ctrl/test/test_maap_differential.cpp:45`, `:52`, `:102`; `sw/firmware/ctrl/maap/README.md:146`; the public PR description's claim that known #686 deviations are explicitly checked.

Title: The differential does not grade the known probe-interval deviation.

Authority/evidence: Assignment #665 requires a shared-stimulus differential, and #686 explicitly records the parent's 500..627 ms probe draws against B.3.3/Table B.8 and B.3.4.2. The software differential timer port discards the requested delay; acquisition invokes three expiries immediately. The cadence case checks bytes/counts and a limited announcement observation, but never records or compares probe intervals. Its listed #686 deltas also omit probe timing.

A disposable source mutation setting every firmware probe delay to **1 ms**, while retaining the announcement expression, passes all eleven differential cases. See [mutation and result](receipts/differential-timing-escape.json), [raw differential receipt](receipts/differential-timing-escape.log), and [portable reproducer](scripts/differential_timing_probe.py).

Impact: This required differential evidence accepts arbitrary probe timing divergence. The separate core unit suite does check the correct constants and draw endpoints; this finding does not claim that the unmodified core uses 1 ms intervals or that the entire unit gate misses that mutation.

Required outcome: Explicitly observe and grade the probe timing delta against Annex B, with the known parent deviation named, and make the published differential coverage claims match what executes. Any claimed cadence comparison must reject an incorrect interval rather than merely ignore its timer arguments.

Verification: A named differential timing check must fail the 1 ms probe mutation and exercise the relevant strict interval boundaries. Retain the existing eleven cases and their controls. This changes a conformance/coverage claim, so it is not wording-only RESIDUE.

**Executed evidence**

| Check | Result | Receipt |
|---|---|---|
| Complete controller baseline with required RV32I build | PASS, all arms; 32 new core/CSR cases, 11 host cases at each interface count, one debug case | [baseline](receipts/ctrl-baseline.log), [exit and duration](receipts/ctrl-baseline.rc.json) |
| Firmware coverage ratchet | PASS, all 17 files; core 205/205 lines and 138/138 branches, adapter 98/98 and 60/60, CSR 39/39 and 18/18; no new exclusion | [coverage](receipts/coverage.log) |
| Unmodified parent/core differential | PASS, 11 cases | [differential](receipts/differential.log) |
| Independent controller mutation audit | 180/180 caught, 185 named obligations, zero build failures counted as catches; two disjoint 90-entry partitions | [final audit](receipts/mutation-final-audit.json), [campaign](receipts/mutation-campaign.log), individual raw logs under `receipts/mutations/` |
| Exact catalog delta and declared eight-way partition scheme | 97 inherited + 83 added = 180; complete/disjoint current catalog | [catalog delta](receipts/catalog-delta.json), [partition census](receipts/declared-partitions.json) |
| Differential sensitivity controls | 11/11 caught by their named tests | [controls](receipts/differential-controls.log) |
| Independent removal of actual reentry refusal | Named debug test fails, as required | [guard removal](receipts/reentry-guard-removed.json), [raw failure](receipts/reentry-guard-removed.log) |
| Independent application wake-up tests | Reproduce F1 at one and two interfaces; runtime enable-bit positive control passes | [probe results](receipts/review-probes.json) |
| Independent 1 ms timing mutation | Escapes the differential; F2 | [timing probe](receipts/differential-timing-escape.json) |
| Raw bytes, file modes, index entries and required submodules | PASS at completion | [final integrity](receipts/integrity-final.json) |

The full controller catalog includes the requested samples across core wire/timers, all eighteen receive table cells, interface/tag handling and CSR address/loss paths. A mutation is credited only for its named failure, with compilation refusals separated. Two negative runs include runtime termination: the inherited free-list control expects that termination, and the missing-initial-PROBE control first fails its named assertion before a later test crashes. Those receipts are retained; they are not represented as complete green executions of every test under mutation. The original campaign summary used `new_maap` for a name-prefix census; the final audit explicitly corrects that label and proves the actual 83-entry source delta.

The supplied public archive contains the author handoff and PR body, with hashes for other retained logs. Those unavailable underlying logs were not independently hash-verified. The results above are fresh executions at this head, not an attestation of unpublished author logs. No full parent, processor, gPTP, builder or synthesis bank was run by this reviewer.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | IEEE 1722-2016 Annex B; `maap.c:23`, `:61`, `:103`, `:254`; `ctrl_app.c:52`; H-MAAP and differential | R529-1 applied; F1/F2 open | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| RTL | UNCLEAN | `maap.c:140`; `maap_mbx.c:13`, `:34`, `:94`; `maap_csr.c:43`; `ctrl_app.c:52`; CSR/packetizer consumers in static receipt; F2 diff inventory | R529-1 applied; F1 open | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| Robustness | UNCLEAN | malformed/range/queue/reentry cases in `test_maap.cpp:200`; stale/foreign/link/stall cases in `test_maap_mbx.cpp:139`; independent wake-up tests | R529-1 applied; F1 open | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| Tests | UNCLEAN | baseline, coverage ratchet/exclusions, 180-entry campaign, differential and sensitivity receipts, independent probes | R529-1 applied; F1/F2 open | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| Docs | UNCLEAN | frozen #665 decisions; `FR_NFR.md:409`; `MAILBOX_SPLIT.md:420`; MAAP README clause/proof map; public author evidence | R529-1 applied; F2 open | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |

No lens is banked clean while these findings remain. No RESIDUE or SUGGESTION is recorded.

**Prior findings, limits and manager duties**

After the independent diff pass, the public PR had no formal reviews, inline review comments or prior findings; its two conversation comments were review-start notices. There was therefore no earlier finding to resolve or retain. [Checkpoint receipt](receipts/prior-findings.json).

Host H-MAAP results use the stated 100 ns mailbox-access assumption and 1 ms timer resolution. They do not establish target CPU, bus arbitration, NVM interference, wire departure, in-flight media quiescence or physical timing. CSR tracing confirms ordered programming and admission closure, not physical frame quiescence. Physical calibration was NOT RUN, and field/vendor skips supply no hardware proof. One and two interfaces were exercised; this is not redundancy acceptance.

Hosted checks and local workflow replication remain the manager's responsibility and were not inspected or run here. Source validation is distinct from the final current-dev merge candidate. The manager must obtain fixes and exact-head re-reviews, finish the independent review bar, refresh the candidate against current dev, validate that candidate, secure explicit merge authorization, and perform post-merge containment and public issue/project updates. Neither this review nor the provided source-bank passes authorize a merge or a shipping-default flip.

All probes used disposable copies/builds under packet scratch. No repository source fixes, commits, pushes, GitHub writes, privileged actions or hardware operations were performed. The final integrity proof hashes 1,154 superproject files plus 558 protocol-processor, 104 gPTP-processor and 214 verilog-axis files against their committed objects, checks modes and index entries, and verifies each required gitlink/HEAD. The unused `external` submodule remains uninitialized. Peak recorded review-unit memory was below the 12 GB cap; independent runs were joined, with at most sixteen compiler jobs concurrently.

Portable commands are in `scripts/`: `run_banks.py`, `mutations_audit.py --jobs 8 --workers 2`, `run_differential_controls.py`, `run_probes.py`, `differential_timing_probe.py`, `reentry_guard_probe.py`, and `verify_integrity.py`. Each takes the source and packet paths; `run_banks.py` also requires `--verilator`, and differential scripts use `VERILATOR`. Set TMPDIR to packet scratch. `MANIFEST.sha256` lists every publishable receipt and script; scratch is excluded.

R529-1 FINISHED
