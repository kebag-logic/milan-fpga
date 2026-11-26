[R936] NEGATIVE - exact head 0ad0e5180558a376f6064d0b33884ed40af6e196

Round R936-1, external independent review of issue #970 / PR #1015.
Tree: `d89ab4e42af51456f1bd2855a4025668bfa0ca57`.
Compared with `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`.
All five lenses were applied independently. One MAJOR finding remains open.
This verdict does not approve merge or close #970.

### R936-1-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

**Artifact:** `sw/firmware/ctrl/adp/adp_mbx.c:72`, `:144`, `:167`; pinned `third_party/tsn-c-stack/src/adp.c:217` and `:247`; `sw/firmware/ctrl/test/test_adp.cpp:872`; published `review-evidence/adp970-r1/author/REVIEW-READY.md:3` at evidence commit `40ce56ee579d00874e4c9db98893f0742498aee3`.

**Title:** Qualified LINK_UP does not take the required fresh sample; the ready statement claims that it does.

**Authority/evidence:** The [public ruling on #970](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7174054394), item 2, requires a fresh sample mixed with entity ID and interface. The requested review scope explicitly requires startup and each qualified LINK_UP. Milan v1.2 5.6.3.5.2/.3 define the two delay ranges; IEEE 1722.1-2021 6.2.4.2.2 requires uniformity and MAC-plus-clock seeding. The fresh-at-LINK_UP requirement here is the explicit project ruling, not an invented quotation from IEEE.

At this head, the adapter provides its clock through `ports.seed`. The pinned core invokes that callback only on enable. `adp_link_change` enters the delay using its existing generator state; it never invokes the seed callback. The adapter's LINK handler directly calls that function. This also affects the first LINK_UP following an enable while down, not merely the second and later rises.

The independent probe in `fresh_sample_probe.cpp`, compiled against the unmodified head through the existing adapter/model composition, records:

- Three qualified rises: sample counter stays at 1, the enable-time call. Delays are 2,113, 667 and 809 ms; the generator advances, but obtains no fresh clock sample.
- Thirty-two otherwise identical boots with distinct clocks only at LINK_UP: one distinct first delay. The enable-time clock remains fixed.
- Duplicate up notifications do not draw or sample, as required.
- The ordinary ADP suite passes 62 checks. With these two additional checks it runs 64 checks and fails exactly those two (`fresh-sample.log`, exit 1).

H4-H6 vary the clock before restarting the application. Their LINK_UP arm does not vary the clock between enable and the rise or count sampling on later rises. Consequently their passing distribution measurements and the 19 caught plants do not detect this omission.

The published ready statement says sampling occurs at startup and each qualified LINK_UP. In contrast, `docs/reference/FR_NFR.md:223`, `CHANGELOG.md:102`, and the live PR's Description/Known limitations explicitly defer fresh LINK_UP sampling to a later stack pin. That disclosed dependency is still absent at the reviewed head. The packet's pin-branch receipts cannot establish behavior at the unchanged `715589c1db7cf67e2f3259fd7083ebc7f0923376` gitlink.

**Impact:** Link-time variability never enters the seed. Identical enable-time state produces identical subsequent draw sequences despite different link timing. The accepted per-transition behavior is incomplete, and the ready evidence overstates exact-head conformance. This is a code, test and conformance defect, not wording-only RESIDUE. Deferring the missing dependency does not resolve it under AGENTS.md section 7.

**Required outcome:** Supply the accepted fresh sampling behavior through the stack's public ownership boundary, including the first down-to-up event after enable. Keep the adapter from writing stack state, preserve the literal draw ranges and immediate LINK_UP delivery, and preserve duplicate/disabled-event semantics. Alternatively, obtain an explicit public scope decision before claiming this partial implementation satisfies the ruling. Align the ready statement and documentation with the actual reviewed head; identify the source head of every receipt.

**Verification:** Retain a clock-call-count test through the real adapter composition for startup, first and subsequent qualified rises, duplicate up, disabled events, and both interfaces. Hold the enable sample fixed and vary the link-time sample; require the latter to affect the draws. Include a plant removing LINK_UP sampling that these tests kill by name. Re-run affected distribution, boundary, boot, memory and CPU paths on the integrated exact head, with any access-budget changes reviewed explicitly. Re-review all affected lenses.

### Independent lens examination

| Lens | Examined artifacts and result |
|---|---|
| Conformance | Read #970 body and both public rulings, REQUIREMENTS.md ownership/acceptance rules, FR_NFR 2.1.1, IEEE 1722.1-2021 6.2.4.2.2 (printed p.56), and Milan v1.2 5.6.3, Tables 5.49-5.51 (printed pp.102-105). The 2,000/4,000 ms constants and 6.0 s declaration remain unchanged. G1-G5 exercise first advertisements, both GM orders and available_index. F1 violates the accepted sampling behavior. |
| RTL | Compared all 14 changed files and all three commits. No RTL or gitlink changed. Examined adapter callbacks, global clock lifetime, platform clock wiring at `ctrl_plat.c:135`/`:401`, enable ordering at `:417`/`:432`, stack seeding, PHY publication, and `sw/litex/mac_link_status.py`. New mixer arithmetic is unsigned and bounded; interface context is established synchronously before enable. No added adapter write to core state and no new CDC. The architecture lens finds the missing sampling call at the pinned core boundary (F1). |
| Robustness | Executed the full focused ADP suite and platform boot/PHY suites for one and two interfaces. Inspected stale timer tags, invalid interfaces, owed-frame backpressure, link down, GM-before/after, zero-seed guard, carry and fallback clock paths. Independent repeated-rise and changed-link-clock probes expose F1. No rejected two-second link hold exists in the adapter or PHY publication path. |
| Tests | Inspected H4-H7, B25/B26, the first-advertisement plants, CPU scenario changes and slow-shutdown mutation anchor. Ran ADP 62/62, platform boot/PHY 58/58 and 59/59, and all 19 focused plants with each required named kill. Existing H4-H6 measure startup variation, not a fresh transition-time sample; F1 survives those tests. Wider scenario waits admit the unchanged 4 s draw; individual service budgets are not relaxed. |
| Docs | Compared CHANGELOG, MAILBOX_SPLIT, SPLIT_CONTROL_MEMORY, FR_NFR, reboot record, live PR body and published author packet. The 4,311 ms derivation and 1,689 ms margin remain unchanged. Memory and reboot figures match the source-head receipt summaries. The ready statement conflicts with the source and explicit deferred dependency (F1). No new bench-lane/review identity comment residue was found in the delta; B25/B26 identify executable test cases. |

### Reviewer-owned coverage ledger

An UNCLEAN entry names the round that applied the lens, not a clean covering round.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #970 ruling; FR_NFR 2.1.1; adp_mbx.c:72/:144; pinned adp.c:217/:247 | R936-1 applied; none clean | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| RTL | UNCLEAN (F1) | 14-file diff; ctrl_plat.c:135/:401/:432; adapter/core seed boundary | R936-1 applied; none clean | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| Robustness | UNCLEAN (F1) | adp.log; platboot1.log; platboot2.log; fresh-sample.log | R936-1 applied; none clean | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| Tests | UNCLEAN (F1) | test_adp.cpp:872; test_plat_boot.cpp:1336; mutation-summary.json; fresh_sample_probe.cpp | R936-1 applied; none clean | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| Docs | UNCLEAN (F1) | author/REVIEW-READY.md:3; FR_NFR.md:223; live PR Known limitations; memory/reboot receipts | R936-1 applied; none clean | 0ad0e5180558a376f6064d0b33884ed40af6e196 |

### Execution and evidence accounting

Reproduce focused checks from this packet:

```sh
python3 -B focused_checks.py /absolute/path/to/exact-head-checkout --jobs 16
python3 -B verify_tree.py /absolute/path/to/exact-head-checkout
```

The driver keeps builds and disposable source copies under `scratch/`, with at most four concurrent checks and four compiler jobs each. The independent defect probes are expected to exit 1 at this head. No source fix was made. An initial reviewer driver attempt omitted the generated walk include; two mutation groups refused compilation. Their initial logs are retained. The corrected driver generates the pinned include, then those two groups passed. No compile refusal counts as a caught plant. `mutation-summary.json` records 19/19 caught, including the two platform wiring plants and the extra-access latency plant.

The 14 published evidence files at commit `40ce56ee579d00874e4c9db98893f0742498aee3` match their published manifest hashes (`public-evidence-integrity.txt`). The following are author-published evidence inspected here, not independently rerun large banks:

- Source-head CPU comparisons: 75 paired probes at 1x1/1if, no misses; 90 at 8x8/1if, the same seven pre-existing misses on both sides. Largest reported positive row changes are about 0.207 and 0.217 ms. Work-pass maxima rise 1.465 to 1.475 ms and 1.759 to 1.774 ms, below 2 ms. Those existing misses are not converted into clean deadline evidence.
- Source-head ledger: ROM 127,856 / 129,680 / 141,968 / 143,744 B, respectively +344 / +384 / +352 / +376 B. SRAM 56,736 / 59,168 / 100,096 / 117,632 B and planned tiles 45.5 / 46.5 / 59.5 / 64.5 remain unchanged, as do the four platform structure sizes. Checked against SPLIT_CONTROL_MEMORY's preceding baseline figures.
- Source-head split boot summaries: 1x1 and 8x8 each PASS, zero findings. Stand-in timing-register failures are explicitly excluded by that harness and provide no physical synchronization evidence.
- Source-head reboot summary matches the revised row: 842.550 + 3,500 + 3 + 871.322 = 5,216.872 ms, leaving 14,783.128 ms of the 20 s allowance. Configuration load is unmodelled.
- `cmp-pin-*`, `pin-ledger.log`, `pin-plants.log` and stack gate receipts belong to the prospective pin change. They were not credited as execution of the reviewed head.

### Limits and pending manager duties

The verified source tree and all five required initialized submodule worktrees retain exact tracked bytes, modes and clean indexes (`tree-integrity.json`). The optional `external` gitlink is recorded and remains uninitialized. No source commit, push, GitHub write, hardware access, or full parent/processor/build bank was performed. The scoped simulator's identity was checked as version 5.050; this review ran native focused tests, not a new large simulation bank.

Hosted status was inspected once and saved in `hosted-checks.jsonl`. Some jobs were successful, others queued/in progress, and the physical job was skipped. A skipped context is not an executed test. No full hosted acceptance is asserted. Hosted/local-replica acceptance remains the manager's responsibility.

There is no manager source bank at this exact head. Source execution evidence is the author's published receipts plus the focused checks above. The manager still owns the current-dev candidate built from this source base and live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, its builder/native receipts and required gates, independent positive re-reviews, merge authorization, and post-merge containment. No candidate validation is inferred from source-head tests.

Physical calibration: NOT RUN. Field skips are not hardware proof. The statistical tests cover their explicit deterministic clock/identity ensembles; they do not measure entropy across physical boots. The lost early frames remain open under #970 and need measurement at the device's port; this review does not establish delivery within the declared discovery time on hardware.

### Prior public findings reconciliation

The independent verdict and ledger were written before this check. The PR discussion contained only the two manager review-start notices. The review-submission and inline-thread queries each returned an empty list (`prior-findings.json`). There are no prior public PR findings to resolve or retain in this snapshot. No other reviewer's report was consulted. The older issue comments describe the abandoned narrowed-delay approach; the subsequent public ruling rejects that approach, and this head retains the full ranges.

R936-1 FINISHED
