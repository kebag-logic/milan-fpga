[R603] POSITIVE - exact head c7d0ad63510cf1aaee41ef440675d110ad2730d7

External independent review of issue #671 / PR #715, round R603-6.
Tree: `06f494ec738a0c0eb0147a22b7b57c3545f5d6f9`.
Source base: `e8454e2751d05b02ee8e5a571857589ab358ab86`.
Delta: `793641131` and `c7d0ad635` after `0c276b621d638c9a83e82f71fbf07bc153517bf7`.

R603-5-F1 and R602-5-F1 are resolved under the [round-6 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6112358549). All five lenses are CLEAN at this head. No new BLOCKER, MAJOR, MINOR or RESIDUE is filed. The two existing optional suggestions remain optional. This is a source-review verdict; hosted acceptance and current-dev candidate validation remain separate manager duties.

**Independence and reconstruction**

Read AGENTS.md, CONTRIBUTING.md and docs/README.md; issue #671's frozen acceptance and public scope decisions; linked requirements and saved-state authorities; the full source-base diff, round-6 delta and history; then public executable evidence. No private author material, management workspace or other reviewer's current-round report was read. `receipts/independent-verdict.md` records my own verdict and ledger before prior review findings were opened. All ten prior public review bodies were subsequently reconciled. Formal-review and inline-comment endpoints contained no additional findings.

Authorities include [issue #671](https://github.com/kebag-logic/milan-fpga/issues/671), its [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6098494890), [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6100704879), [round-3 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6103025987), [round-4 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6104799677), [round-5 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6107082416), and round 6. REQUIREMENTS.md sections 1/8, FASTCONNECT sections 6.2/7, MATERIALIZATION section 6.3, SNAPSHOT_OWNERSHIP's restart/capture contract and ctrl_nvm README Boot 3/4/9 establish the boundaries. The [authority-after-fault decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997929153) and [byte-agreement decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999350068) remain applicable.

**Round-6 results**

`sw/firmware/nvm_hosttest/read_fault_cases.py:24` lists the four terms once in `COMPARISON`. Generated controls at `:143`, `term_class` at `:299`, diagnostic naming at `:314`/`:451`, and `comparison_findings` at `:323` derive from it. The firmware expression is compared against this list when the normal gate runs (`test_nvm_firmware.py:973`). The removal controls alter exactly one equality to `1` in disposable firmware copies.

| Term | Fault construction | Observed class cases per shape | Named removal control |
|---|---|---:|---|
| Verdict | Change identity/model words and forge the prefix CRC to the unchanged trailer | 32 | `r_omit_verdict` |
| Byte count | Grow declared length, move the unchanged trailer, and forge an unchanged mismatching prefix CRC | 32 | `r_omit_byte_count` |
| Prefix CRC | XOR the last byte before the trailer (`-5`) | 32 | `r_omit_prefix_crc` |
| Trailer | XOR the trailer's last byte (`-1`) | 32 | `r_omit_trailer` |

My `scripts/audit_terms.py` instrumented only a disposable firmware copy at the return from `nvm_read_slot`. Across the first shape and both product shapes, all **384 cases** produced two refusals whose actual `(verdict, bytes, digest, tail)` tuples differed in exactly the intended field, then VD_OK. This observes the tuples the production comparison consumes, rather than inferring isolation from fault labels. The raw transcripts and tuple records are `receipts/terms-*.log` and `.json`.

Each term covers both orientations, sequences 1 / 0x5A5A5 / 0x80000000 / 0xFFFFFFFF with the other slot blank, cold boot and writer restart. The additional both-valid classes cover newer and older fault targets at 0x5A5A5 and the sequence wrap. There are 128 term cases per shape. The complete campaign contains **3,550 cases**, 1,839 cold boots and 1,711 restarts. The earlier full read-bound windows remain intact; round 6 adds the specifically ruled two-refusals-then-clean classes.

For all 384 term cases I also ran the standing case graders with reboot caching disabled: exact reads, expected hold, boot offer/window, acknowledged change, changed-record restoration and every other saved record passed. The independent tuple probe additionally asserted six/seven reads with a blank peer slot and five/six with both valid (restart/cold), no hold and unread zero. The separate full campaign covers unresolved-fault hold, no erase/program/acknowledgement, liveness expiry, console refusal, fallback and recovery.

All four removal controls fail by **their own term diagnostic on all three required shapes** in my full self-test. The nine completeness self-test arms reject four absent classes, four absent controls and an unlisted firmware term. `scripts/audit_inputs.py` additionally removed just one required combination from each class; every omission was rejected as exactly one missing place. Thus completeness does not merely count labels.

The production firmware is byte-identical to round 5 and to the measured firmware commit. SHA-256: `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`. No production comparison change or STOP condition occurred. No RTL, register-map, container-format, required gitlink or A/B transaction change is introduced by round 6.

**Executable evidence**

| Execution in this review | Result | Receipt |
|---|---|---|
| Complete writer gate, `--self-test --jobs 4` | Five shapes pass; 61 firmware-control runs rejected as expected, plus nine comparison-check arms; 268.0 s, exit 0 | `receipts/writer.log` / `.rc` |
| Independent actual-tuple audit | 384/384 isolated-term cases pass, including complete record assertions and real clean reboots | `receipts/term-audit.log`, `receipts/terms-*.log`, `receipts/terms-*.json` |
| Shipping co-simulation, both product shapes, `--jobs 8 --pool 4 --skip-mutants` | 465/465 checks pass, 0 not expressible; exit 0 | `receipts/cosim.log` / `.rc` |
| Capture receipt gate | Firmware/census/clocks/timing arms and built-in controls pass; exit 0 | `receipts/capture.log` / `.rc` |
| Documentation gate | Zero findings; scrub controls 23/23, routing arms 4/4; exit 0 | `receipts/docs.log` / `.rc` |
| Input/completeness audit | Firmware identity, unchanged interfaces, case counts, missing-class/control checks and capture identities pass | `receipts/input-audit.log` / `.rc` |
| Original public R603-5 comparison probe | Head: 0/48 focused failures per shape. Omission: 16/48. Old inclusive comparison: 32/48. Omission now has 78 standing findings per shape, 32 naming trailer-only disagreement | `receipts/prior-r603.log`, `receipts/comparison.json` |
| Original public R602-5 standing probe, `no_tail,digest_short` | Both plants produce 78 findings on each of three shapes, including their own trailer/prefix-CRC diagnostics | `receipts/prior-r602.log` / `.rc` |

The two prior scripts were fetched from the fixed public evidence commit and retained byte-for-byte; `receipts/prior-probe-provenance.json` records their blob IDs and SHA-256 values. Their successful process exits are not alone proof that a plant was caught: I inspected the emitted case findings and counts. The R602 script always returns zero by design.

The public [author evidence](https://github.com/kebag-logic/milan-fpga/tree/4c4d44f8a9cc76d7a16945eb555c5b1b1777d084/review-evidence/671-r1/author-r6/receipts/r6) separately records the 275.27-second exact-head self-test, six builder parts, harness equivalence, term matrix/views and final gate summary. Selected original published blobs and identity receipts are under `receipts/public-author/` and `receipts/public-author-provenance.json`. Their source-head results are author evidence, not a manager source bank. I did not execute those full banks. Published stored receipts may normalize local paths; their public blob identity is verified, and their manifest distinguishes original from stored bytes.

The capture receipt's firmware, measured tree and all listed harness hashes match. Its 8x8 contract maximum remains 13.86328 ms, with 10.63672 ms margin to 24.5 ms and a 3.5345x floor ratio; 1x1 remains 3.96548 ms. I regraded the receipt, not the underlying measurements. Firmware size is unchanged from round 5 by byte identity; the author's recorded +2,050 B text and +16 B bss over the source base were not rebuilt here.

**Applied lenses**

- `[R603] PASS Conformance - read_fault_cases.py:24,143,299,323; milan_baremetal.c:742,776,793,825,1601,1641; receipts/term-audit.log -` All six round-6 obligations and acceptance 1-3 checked against the public rulings. One list drives all four isolated classes and controls; missing coverage fails; production comparison is unchanged. Existing staged validation, validated-only generation, bounded judgement/re-stage and both entry-path holds remain intact.
- `[R603] PASS RTL - hdl/milan/KL_nvm_backend.sv:424,439,482,490,582; protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv, packet_engine/KL_pp_nvm_port.sv, packet_engine/KL_pp_nvm_mgr_arb.sv, acmp/KL_acmp_nvm_shadow.sv at pin 2ad2f845; receipts/cosim.log; receipts/input-audit.log -` Backend sequence is a stored/read-back word; firmware owns authority. The processor record interface carries no slot generation. No HDL/CDC/reset/interface change occurs. Firmware read lengths remain 40 or 44..65,536 bytes, subtraction of four stays bounded, the stage fits a slot, and failed picks leave a terminating fallback. The unchanged A/B path passes integration.
- `[R603] PASS Robustness - nvm_host.c:584,603,666,965; writer_restart.py:18,26; read_fault_cases.py:393,487,502,523; test_nvm_firmware.py:661,698,720 -` New length/verdict faults are bounded and construct the intended CRC relationships. Terminal and pre-terminal byte faults, both orientations, all required boundaries, cold/restart paths, exact counts, holds and all-record preservation were driven. Retained reset/window assumptions are explicit.
- `[R603] PASS Tests - test_nvm_firmware.py:661,698,720,775,912,973; read_fault_cases.py:323,350; receipts/writer.log; receipts/prior-r603.log; receipts/prior-r602.log -` Every new term has a fault that isolates it and a removal plant rejected by its own diagnostic on the three required shapes. All missing-class/control arms reject. Both previous escaping plants now produce standing behavioral findings. Tests compare the actual persisted records after clean reboot, not merely a model verdict.
- `[R603] PASS Docs - sw/firmware/nvm_hosttest/README.md:52,151,227,256; docs/design/SAVED_STATE_FASTCONNECT.md:781; docs/integration/BAREMETAL_FIRMWARE.md:2014,2181; docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1626; PR #715 body; receipts/docs.log -` Comparison, artificial collision construction, case/control inventory, hold/restart behavior, timing provenance and limits checked against code and execution. Source receipts, merge-candidate duties and physical proof are distinguished.

**Prior findings at this head**

| Prior IDs | Disposition | Current evidence |
|---|---|---|
| R603-5-F1; R602-5-F1 (MAJOR, Tests/Robustness) | RESOLVED | Four ruled term classes and controls; actual tuple isolation; original probes now report 78 standing findings per plant/shape. Trailer and last-prefix-byte regressions are both detected. Resolution follows the round-6 class ruling. |
| R603-4-F1 (MAJOR, all five lenses) | RESOLVED | Unchanged corrected prefix CRC plus exact trailer; sealed classes retained; `r_digest_with_trailer` fails on three shapes. Original comparison probe's head sealed cases pass and inclusive mutant cases fail. |
| R603-3-F1; R602-3-F1 | RESOLVED | Full cold/restart window sets, exact model read counts and unbounded/four-try re-stage controls remain; self-test rejects each by name. |
| R602-3-F2 | RESOLVED | PR attributes 645/124 to round-2 head 9112a0df and explains the base's 15-static adaptation. Later base-reproduction counts are historical author evidence, not claimed rerun here. |
| R603-3-S1 | RESOLVED | `nvm_unstaged`/`nvm_print_unread` distinguish failed judgement and re-stage; hold grader checks the cause. |
| R602-3-S1 | RESOLVED | Snapshot/firmware pages describe diagnostic sequence publication over the retained window, with liveness expiry. |
| R603-2-F1; R602-2-F1 | RESOLVED | Shared complete writer-static reset, 1,711 restart cases per shape and re-attach-only control rejected on three shapes. |
| R603-2-S1; R603-2-S2 | RESOLVED | Exact read counts and four-try judgement control; `re-attached and HELD` emitted and graded. |
| R603-2-R1; R602-2-S1 | RESOLVED | Snapshot restart bullet includes hold; firmware page states every-boot hold and operator wipe recovery. |
| R603-1-F1; R602-1-S2 | RESOLVED | Body faults, both-valid layouts and every-record restoration remain; header-only digest, fresh-fill and no-fallback controls rejected on three shapes. |
| R603-1-F2; R602-1-F1 | RESOLVED | PR estimates ten 64 KiB refused reads plus two container reads, 16.4/17.1 s, with restart-liveness qualification. The read bound matches the code; costs were not remeasured here. |
| R603-1-S1; R602-1-S3 | RESOLVED | Explicit operator-wipe exception and both erases checked by `grade_hold_console`. |
| R603-1-S2 | RESOLVED | Separate `nvm_held`; four retire causes retain and pass their own console checks. |
| R603-1-S3 | RESOLVED | Other-slot fault and `r_restage_any_seq` exercise sequence-specific re-stage. |
| R603-1-R1; R602-1-R2 | RESOLVED | Fourteen numbered checks; read-fault/generation checks consistently 13/14. |
| R602-1-R1 | RESOLVED | FASTCONNECT section 7 distinguishes shipping overwrite from the other store's stale-slot selection. |
| R602-1-R3; R602-2-R1 | RESOLVED | Snapshot cost section distinguishes writer hold and capture hold and names console changes. |
| R602-1-R4 | RESOLVED by superseding description | README describes generated all-FF windows and precisely excludes indistinguishable reads. |
| R602-1-S1 | RESOLVED | Firmware documents the read-fault count as a floor. Numerical grading remains the separate optional R602-4-S1. |
| R602-4-S1; R602-4-S2 | RETAINED, SUGGESTION | See retained suggestions below. |
| R603-2-OBS-1; R602-2-S2 | RETAINED outside scope | Runtime prefill still reads flash afresh; the public round-3 decision assigns #717. No fix is claimed and no review finding is cleared merely by moving it. |

**Retained optional suggestions**

- **R602-4-S1 | SUGGESTION | Tests.** Artifact: `read_fault_cases.py:203` (`UNREAD_RE`) and `test_nvm_firmware.py:758` (only unread group used). Evidence: the diagnostic `read faults=` number still lacks a numerical assertion; persistence/hold/read-count assertions do run. Impact: diagnostic counter regressions can escape. Optional outcome: assert the documented floor for representative read sequences. Verification: a counter-only mutation must fail its diagnostic check. This remains optional under the public disposition.
- **R602-4-S2 | SUGGESTION | Tests, Robustness.** Artifact: `nvm_host.c:196` (`struct read_fault`) and `read_fault_cases.py:185` (`GROUPS`). Evidence: the model arms one slot fault at a time, so generated cases do not fault both slots simultaneously. Impact: less direct coverage of combined unread paths. Optional outcome: add independent faults for both slots and verify hold/no persistence/recovery. Verification: dual-fault cases and corresponding controls. Round 6 does not require this expansion.

**Reviewer-owned completion ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance/rulings; FASTCONNECT 6.2/7; firmware read/judge/re-stage/hold; COMPARISON/class/control/check; term audit | R603-6 | c7d0ad63510cf1aaee41ef440675d110ad2730d7 |
| RTL | CLEAN | Full source-base diff; backend sequence/liveness; pinned processor NVM interfaces; bounded stage/read logic; co-simulation; capture/input identities | R603-6 | c7d0ad63510cf1aaee41ef440675d110ad2730d7 |
| Robustness | CLEAN | Fault construction/CRC forging; generated boundaries/windows; writer restart; hold/count/all-record graders; actual tuples and prior probes | R603-6 | c7d0ad63510cf1aaee41ef440675d110ad2730d7 |
| Tests | CLEAN | Full writer self-test; 384 observed term cases; missing-class/control checks; prior omission/short-prefix probes; 465 integration checks | R603-6 | c7d0ad63510cf1aaee41ef440675d110ad2730d7 |
| Docs | CLEAN | Host README; FASTCONNECT; firmware page; snapshot/capture receipt; PR/issue public state; public author receipts and local docs check | R603-6 | c7d0ad63510cf1aaee41ef440675d110ad2730d7 |

**Hosted snapshot and limits**

At `2026-10-11T20:48:32.354325+00:00`, the exact-head snapshot contains 10 executed successful checks, nine in-progress checks and one skipped physical job. `wire-accountability` and `docs-check-no-git` succeeded. `docs-check`, `elaborate`, `firmware-unit`, `yosys-elaboration` and all five simulation shards remain in progress. The four portability shards succeeded; their `yosys-portability` aggregate is not yet present. Neither `rtl-fast` nor `verilator-suites` has yet been emitted. `full-ci-gate` succeeded. The physical nightly/manual job is SKIPPED. No failed conclusion appears in this snapshot. The hosted standalone saved-state writer step is still pending behind the builder step, so no successful hosted writer execution is claimed at this head. `receipts/hosted-snapshot.json` retains job/step status and direct run links. The manager owns final hosted and local-replica acceptance; this review did not wait for hosted completion.

Physical calibration **NOT RUN**. Field skips and simulated capture timing provide no hardware proof. The host model substitutes mapped flash/CSR behavior and CPU time; co-simulation does not prove board timing, CDC or physical reset retention. Writer restart assumes retained fabric/window state. Identical wrong reads, repeated erased views, some valid address substitutions and genuine CRC collisions remain the documented detection limits. Constructed collision classes establish term sensitivity, not fault frequency.

No manager source bank ran at this head, and none is inferred. The author's published gate receipts provide broader source validation; my executions are the focused checks above. I did not run full parent/processor/timing/builder/portability banks, local hosted-workflow replicas, physical hardware, fresh capture measurements or firmware-size builds. The co-simulation run here excluded its mutation bank; the author's public 39/39 result is not presented as my execution.

**Pending manager duties**

- Complete hosted and local-replica acceptance at this exact head, including distinguishing executed checks from skipped contexts.
- Validate the final candidate against current `dev` with builder and native banks and publish receipts. The supplied live-dev tip is `cfadd767a7ad47aaee68de655e1066cc000fb8a0`; it differs from the source base. Refresh it at the merge turn. This source verdict is not candidate validation.
- Obtain both independent positive reviews, finish all in-flight reviews and secure explicit maintainer merge authorization; then perform required post-merge containment and issue/project completion.
- Carry the optional suggestions and separately scoped #717 work. Track the unchanged Mark II refusal-digest collapse reported under round-5 item 2 in its own issue, as ruled. This review claims no fix there.

**Reproduction and containment**

Portable scripts take the clone and packet paths. Run `scripts/run_focused.py TREE PACKET`, `scripts/run_cosim.py TREE PACKET PINNED_SIMULATOR`, `scripts/audit_terms.py TREE PACKET`, `scripts/run_prior.py TREE PACKET`, `scripts/audit_inputs.py TREE PACKET` and `scripts/verify_checkout.py TREE`. The prior scripts' original arguments and the concurrent wrappers are retained. Logs and explicit exit-status files accompany executions. Concurrent commands remained in the foreground; disposable trees and builds are confined to `scratch/`.

Final verification compares raw tracked blob bytes, file kinds, executable modes and the complete index against the exact commit, independently of status flags. It also verifies each required registered submodule's gitlink, HEAD, raw bytes, modes and index: processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, time-synchronization processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, stream library `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Tracked source was never changed; the detached clone remains exact. Two unused submodules remain uninitialized.

Term transcripts replace the absolute packet path with `<review-packet>`; `receipts/transcript-provenance.json` records original and published hashes. No observation or diagnostic was changed.

Only REPORT.md and files listed in MANIFEST.sha256 are designated for publication. Scratch is excluded. All checks and probes have finished; no execution remains pending in this review session.

R603-6 FINISHED
