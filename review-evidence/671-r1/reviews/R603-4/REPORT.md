[R603] NEGATIVE - exact head 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe

External independent review, issue #671 / PR #715, round R603-4.
Tree: `70ee92ab909f37d435caa0b94daab84bff83d60d`.
Source base: `e8454e2751d05b02ee8e5a571857589ab358ab86`.

One MAJOR finding remains: different CRC-clean refused containers collapse to the same refusal digest. The unchanged firmware then acknowledges a commit that loses saved state. All five lenses were applied independently. The existing host suite passes all five shapes and catches its 46 controls; the focused integration suite passes 465/465. Those results do not cover this counterexample.

**Scope and reconstruction**

Read AGENTS.md, CONTRIBUTING.md and docs/README.md; then the issue body and public scope decisions; linked requirements and interfaces; the complete 15-file source diff and 23-commit history; then public executable evidence. The independent verdict and ledger were written before reading the six prior review reports. No other current-round report was read. No private author material was used.

Authorities examined:

- [Issue #671](https://github.com/kebag-logic/milan-fpga/issues/671), Required and Acceptance 1-3; assignment comments [6098494890](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6098494890), [6100704879](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6100704879), [6103025987](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6103025987), and [6104799677](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6104799677).
- REQUIREMENTS.md product ownership and release acceptance; SAVED_STATE_FASTCONNECT sections 6.2, 7 and 9; SAVED_STATE_MATERIALIZATION section 6.3; SAVED_STATE_SNAPSHOT_OWNERSHIP section 7; ctrl_nvm/README.md Boot items 3, 4 and 9.
- [Decision 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997929153) and the [byte-agreement decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999350068): differing refused reads are media faults; a content refusal needs agreement, within the bound.

The accepted scope is boot authority in the shipping firmware, including writer re-attachment. Only firmware derives the generation. `hdl/milan/KL_nvm_backend.sv:424,439,482,490,582` stores and reads back word 2; its generation has no control consumer. The pinned processor writer, port, arbiter and binding manager operate on records and carry no slot generation. No processor adoption is needed. The pointer-based mapped read exposes wrong bytes without a media-error signal; the public decisions define the observable fault rule. Runtime prefill remains explicitly outside this task under #717.

**R603-4-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

**Artifact.** `sw/firmware/milan_baremetal/milan_baremetal.c:763` computes the refusal digest over `rd.bytes`, including the CRC trailer. `:770` equates verdict, length and that digest; `:793` accepts the second matching refusal. The fault families in `sw/firmware/nvm_hosttest/read_fault_cases.py:142` do not cover distinct CRC-clean semantic refusals. `docs/integration/BAREMETAL_FIRMWARE.md:2023` and `docs/design/SAVED_STATE_FASTCONNECT.md:796` claim agreement of the returned bytes.

**Authority and evidence.** #671 requires unknown authority to prevent persistence until the slot can be read without a media fault. The #665 byte-agreement decision requires different refused bytes to trigger bounded retries. The digest here cannot implement that rule for CRC-clean containers: CRC-32 over a message followed by its own little-endian CRC is the constant residue `0x2144df1c`. The alias is deterministic, not a rare accidental collision.

`probe_refusal_digest.py` compiles the unchanged head firmware. Only the disposable host adapter changes. On each of the valid slot's first two judgement reads, it returns a complete container with a different foreign entity ID and a recomputed, closing CRC. Stored flash is untouched. These are two distinct wrong read views, each refused as `VD_ENT`; the following read would be clean. The probe also executes a clean control for every case.

At 1x1, the two prefix CRCs are `0xb28933bb` and `0xc3856556`, while both whole-container CRCs are `0x2144df1c`. Both shapes exhibit the same collapse. The boot reports `VD_ENT seq 0`, `unread=0`, takes no third judgement read, and enables persistence. After a real changed name, it acknowledges sequence 1.

| Product shape | Originally authoritative slot, seq 0x5A5A5 | Faulty boot's commit | Clean reboot |
|---|---|---|---|
| 1x1 TDM8 | A | A, seq 1, acknowledged | Changed name survives; 53 other saved records lost |
| 1x1 TDM8 | B | A, seq 1, acknowledged | B wins; acknowledged change lost |
| 8x8 | A | A, seq 1, acknowledged | Changed name survives; 163 other saved records lost |
| 8x8 | B | A, seq 1, acknowledged | B wins; acknowledged change lost |

All four clean controls acknowledge the change and preserve every saved record. Raw transcripts and assertions are in `receipts/refusal-digest.log`; exit 0 means the defect and its clean controls reproduced, not that the product passed.

This is outside the documented identical-wrong-bytes limit: the views differ. It is also distinct from an address fault returning a container that the reader accepts as valid: neither view is accepted. Two differing rejected containers are precisely what the agreement mechanism is meant to distinguish.

**Impact.** The original generation-reset loss remains reachable. An authoritative slot can also be erased while authority is unknown, losing other saved records. The firmware/backend boundary presents `backed=1` after an acknowledged commit that does not preserve the state. The current tests miss this fault class, and the documented byte-agreement claim is unmet. These are the reasons F1 applies to all five lenses, including architecture and documentation; it is not prose-only residue.

**Required outcome.** Refused-read comparison must distinguish these different CRC-clean containers without collapsing to the trailer's fixed residue. Preserve the three-read bound, validated-only generation, fallback and hold behavior. Add this class to the standing tests, with a control restoring the defective agreement that must fail by name. Update the mechanism's documentation as necessary. No particular replacement algorithm is prescribed.

**Verification.** On both slot orientations and both product shapes, two distinct rejected read views followed by a clean view must preserve the change and all saved records, or persistence must be refused and reported. Include the sequence boundaries and both boot entry paths. Re-run the generated-window suite and its named controls. Any firmware change owes the required capture remeasurement and size accounting. The published probe provides the failing scenario without modifying tracked source.

**Acceptance and lens evidence**

Acceptance 1 and the Required behavior are not satisfied for F1's transient fault: persistence is neither safely preserved nor refused. Acceptance 2's existing restart-at-zero controls do fail as intended; they do not detect F1. The A/B erase/program/verify transaction functions are unchanged and the integration regressions pass, but Acceptance 3 cannot be declared clean while F1 lets boot select an unsafe authoritative target.

The read and re-stage loops otherwise retain three attempts. Failed re-stage candidates are removed before the other is offered, so the fallback terminates after at most two candidates. Accepted generation and window bytes come from the judged stage; stage capacity admits the entire 64 KiB slot. No HDL, clock, reset, record-format, register-map or gitlink change is present. The backend's heartbeat/loss logic remains unchanged, and the focused integration run exercises its real record paths with the firmware. The fault concerns the firmware's authority decision feeding that interface.

The generated campaign contains 2,158 cases per shape: 1,119 cold boots and 1,039 restarts. Byte-fault cases represent all 53 cold windows and 49 restart windows in both orientations. Sequence values rotate as authorized; the same-byte/accepted-address limits are explicitly excluded. Each case checks an exact read count and hold expectation. The remaining gap is the content of the refused views, not window enumeration.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | #671 Required/Acceptance; FASTCONNECT 6.2/7/9; milan_baremetal.c:740,784,814,1632; refusal-digest receipt | R603-4 | 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe |
| RTL | UNCLEAN, F1 | KL_nvm_backend.sv:439,490,582,631; pinned processor record interfaces; milan_baremetal.c:763,918,1077,1592; integration receipt | R603-4 | 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe |
| Robustness | UNCLEAN, F1 | judgement/re-stage bounds, fallback, cold/restart holds, refused-generation and console cases; generated-window and distinct-refusal probes | R603-4 | 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe |
| Tests | UNCLEAN, F1 | nvm_host.c:536; read_fault_cases.py:142,188,245; test_nvm_firmware.py:672,738,932; writer_restart.py; host and integration receipts | R603-4 | 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe |
| Docs | UNCLEAN, F1 | FASTCONNECT:781; BAREMETAL_FIRMWARE:2014; SNAPSHOT_OWNERSHIP:725,1626; both suite READMEs; measurements.json; issue/PR evidence | R603-4 | 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe |

**Prior public findings: disposition at this head**

Reviewed the published [R603-1](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6100671345), [R602-1](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6100699429), [R603-2](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6102963708), [R602-2](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6103023016), [R602-3](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6104687947) and [R603-3](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6104797818) findings after recording the independent verdict. No formal or inline review findings were returned by the public endpoints.

| Prior IDs | Disposition | Evidence examined at this head |
|---|---|---|
| R603-1-F1; R602-1-S2 | RESOLVED | Body faults and both-valid layouts in GROUPS; `reboot_findings` compares every saved record; header-only digest, fresh-fill, no-fallback and missing-unread controls all caught on three shapes. F1 here is a different refused-content class. |
| R603-1-F2; R602-1-F1 | RESOLVED | Current PR body explicitly estimates ten 64 KiB refusals plus two container reads, 16.4/17.1 s, with restart liveness qualification. The read-count bound matches the loops. Per-read timing was not remeasured here. |
| R603-1-R1; R602-1-R2 | RESOLVED | Host README numbers fourteen checks and identifies 13/14 consistently. |
| R603-1-S1; R602-1-S3 | RESOLVED | Explicit operator wipe exception in firmware and documentation; `grade_hold_console` checks both erases. |
| R603-1-S2 | RESOLVED | Separate `nvm_held`; all four retire causes checked by `grade_hold_console`. |
| R603-1-S3 | RESOLVED | `--read-other` and `r_restage_any_seq` exercise sequence-specific re-stage; named control caught on three shapes. |
| R602-1-R1 | RESOLVED | FASTCONNECT:785 distinguishes the two stores' loss modes. |
| R602-1-R3; R602-2-R1 | RESOLVED | SNAPSHOT_OWNERSHIP section 18 distinguishes writer hold from backend capture hold and names the console change. |
| R602-1-R4 | RESOLVED BY SUPERSEDING DESCRIPTION | Host README now describes generated all-FF windows and precisely excludes indistinguishable cases, matching `expect` and the 2,158-case population. |
| R602-1-S1 | RESOLVED | Read-fault count explicitly documented as a floor at milan_baremetal.c:482. |
| R603-2-F1; R602-2-F1 | RESOLVED | Shared writer-static reset, `--restart`, 1,039 restart cases, and `r_reattach_goes_live` caught on all three required shapes. |
| R603-2-R1 | RESOLVED | SNAPSHOT_OWNERSHIP:725 explicitly publishes and holds on unread re-derivation. |
| R603-2-S1 | RESOLVED | Reference-model exact counts and `r_judge_four_tries` caught on three shapes. |
| R603-2-S2 | RESOLVED | Firmware prints `re-attached and HELD`; `restart_findings` grades it. |
| R602-2-S1 | RESOLVED | BAREMETAL_FIRMWARE Boot states every-boot hold and destructive operator-wipe recovery. |
| R603-2-OBS-1; R602-2-S2 | RETAINED OUTSIDE SCOPE | Runtime prefill is unchanged; the public round-3 decision assigns it separately to #717. This is not claimed fixed or used to clear F1. |
| R602-3-F1; R603-3-F1 | RESOLVED | Every full-bound start and length 1-4 plus whole-boot; exact model counts; `p_restage_unbounded` and `r_restage_four_tries` caught by `want exactly` on three shapes in this run. |
| R602-3-F2 | RESOLVED | Current PR body attributes 645/124 explicitly to `9112a0df`, satisfying the finding's alternative outcome, and documents the base's 15-static adaptation. New 2,660/124 counts are author evidence, not independently rerun here. |
| R603-3-S1 | RESOLVED | `nvm_unstaged` and `nvm_print_unread` distinguish failed judgement from failed re-stage; the reference model checks the cause. |
| R602-3-S1 | RESOLVED | BAREMETAL_FIRMWARE and SNAPSHOT_OWNERSHIP explain diagnostic sequence publication while the retained window stays unchanged. |

No earlier in-scope finding remains open. R603-4-F1 is new. No new RESIDUE or SUGGESTION is filed.

**Execution and provenance**

All review commands ran in the foreground; the check driver awaited its concurrent children. Host tests used four workers; integration used four build jobs and four simulation workers. Disposable files stayed under this packet's `scratch/`. No source fixes, commits, pushes, GitHub writes, hardware access, shared installs, full banks or privileged orchestration were performed.

| Reviewer execution | Result | Receipt |
|---|---|---|
| `test_nvm_firmware.py --self-test --jobs 4` | PASS, five shapes; 46 controls caught; 467.53 s | `receipts/host-selftest.log`, `.rc` |
| Scoped `nvm_cosim` driver, both shapes, `--jobs 4 --pool 4 --skip-mutants` | 465 PASS, 0 FAIL; 79.45 s; integration mutants not run | `receipts/cosim-shipping.log`, `.rc` |
| `scripts/check_nvm_capture.py` | PASS, including built-in controls | `receipts/capture-receipt.log`, `.rc` |
| `audit_artifacts.py <repo>` | PASS, window population, firmware digest and six capture-arm arithmetic checks | `receipts/artifact-audit.log`, `.rc` |
| `probe_refusal_digest.py <repo>` | DEFECT REPRODUCED in four cases; four clean controls pass | `receipts/refusal-digest.log`, `.rc` |
| `verify_checkout.py <repo>` | PASS, exact tracked bytes/modes/index and required gitlinks | `receipts/checkout-integrity.log`, `.rc` |

`run_checks.py <repo> --simulator-dir <pinned-directory>` reproduces the standard checks with scratch outputs. The first review integration entry script had a quoting syntax error before any suite execution; its corrected rerun produced the passing receipt above. The version identity was verified before use and recorded. No source validation is attributed to that failed setup attempt.

The [author's round-4 evidence comment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6106272193) names this head and reports source gate execution, size, capture and exclusions. Those full-bank claims were not independently rerun. The linked immutable `25ad3f94:review-evidence/671-r1` contains round-1 receipts: selected host, integration, firmware-unit and capture logs were hash-checked against its manifest and read. They are historical evidence only, as recorded in `receipts/public-r1-provenance.json`; they are not current-head bank receipts. No manager source bank ran at this head, and none is inferred.

The current capture receipt binds firmware SHA-256 `41000488944bea651733b9708fa0c3a72926ce2308034c51209f2dd95a27b2a2`. All six arms contain sixteen clean captures. Recomputed maxima agree: 8x8 contract 13.86328 ms, margin 10.63672 ms to 24.5 ms and floor ratio 3.5345; 1x1 maximum 3.96548 ms. The receipt was checked, not physically remeasured. Firmware size (+1,954 text bytes, +16 bss over base) and estimated worst boot times remain attributed to the author's public evidence.

`receipts/hosted-snapshot.json` records exact-head status metadata, not downloaded execution logs: twelve contexts succeeded, seven were running, and the physical context was skipped. Neither that skip nor any field skip is hardware proof. Hosted acceptance belongs to the manager.

Final checkout verification hashes 1,272 parent blobs and the exact index against the review tree, and verifies modes and file kinds. Required registered submodules match their gitlinks and tracked bytes: processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` (562 blobs), gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104), axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). The two unused submodules remain uninitialized. Tracked source was never modified.

**Limits and pending manager duties**

The new probe is a host fault model, not evidence of a measured physical fault rate. It demonstrates the rule's failure on different CRC-clean refused bytes. The existing identical-byte and accepted-address limits remain separate. The CPU-only restart model assumes retained fabric/window state and does not prove physical reset retention. Physical calibration was NOT RUN. Capture simulation and modeled read timing do not discharge release hardware obligations.

Return F1 to the implementation lane and obtain independent re-review after correction. All five lenses are unclean at this head. The manager owns publication of this packet, current-head source receipts and hosted/local-replica acceptance. Final current-dev candidate validation is distinct: combine source head with live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` at the merge turn, or its then-current successor, and publish builder/native receipts for that candidate. No such candidate or manager source bank is claimed here. Merge authorization, two positive independent reviews, completed lens coverage, no review in flight, post-merge containment and issue/project closure remain required. This negative review does not authorize merge.

Every publishable script and receipt is listed in MANIFEST.sha256. Scratch files are excluded.

R603-4 FINISHED
