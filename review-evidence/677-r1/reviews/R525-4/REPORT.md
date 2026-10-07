[R525] POSITIVE - exact head 708e5634f28e6e5a19236a9b0a9a543c3622e52d

R525-4, external independent delta review of issue #677 / PR #684, including the frozen #678 scope. All five lenses are CLEAN. R524-3-F1 is resolved. No BLOCKER, MAJOR, MINOR or RESIDUE remains open in this review. Two prior SUGGESTIONs remain optional. This is a source-review verdict, not merge authorization.

Tree: `5aab27ec48b9ac84d26e92440b6a55b59cf69298`. Previous reviewed head: `34475e774dfe1c92c81fa51293668e64dc95fa85` (R525-3). Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`. Assigned live dev: `910f338dbd050f4efd2d96991ddcf928a583d55f`.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [#677 acceptance and public scope](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6021510152), [#678 ruling](https://github.com/kebag-logic/milan-fpga/issues/678), the linked requirements and interface authorities, then `6714181d..708e5634`, history, the round-4 delta, and public execution evidence. `independent-pass.md` records the independent verdict and ledger written before reading prior review bodies. Prior findings were then reconciled against current source and public artifacts. No private author material was read.

The only change since round 3 is one commit modifying five `text` cells in `sw/firmware/ctrl_nvm/README.md:351-355`. Every cell increases by four bytes. All other README bytes, every other tracked path and all gitlinks are unchanged. `delta.diff`, `history.txt` and `sizes.log` establish this. The source-base diff includes changes already merged through dev; against `910f338d`, this PR's footprint is confined to firmware. Those inherited changes are not new round-4 work.

**Independent execution**

The pinned SDK was extracted only under `scratch/`. Its archive SHA-256 is `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`. The repository installer verified provenance, installed bytes/modes/links, relocation, compiler version 14.3.0 and target identity. `sdk.log`, `sdk.rc` and `sdk.command.json` retain that receipt.

Executed at the exact head:

```sh
MILAN_RV32_CC=<packet>/scratch/sdk/bin/riscv32-linux-gcc \
  python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
```

Return code 0 in 112.923 seconds: **435 tests across five shapes; all five RV32 object builds passed; no skip**. The default gate includes the exact-sized erased-prefix sanitizer case, which passed. It also reports a largest static frame of 128 bytes for every shape. These are object measurements and individual frames, not a linked-image or call-chain stack bound. Raw evidence: `ctrl-nvm.log`, `ctrl-nvm.rc`, `ctrl-nvm.command.json`.

The gate prints shapes in a different order from the README. `compare_sizes.py` matches by unique BSS, then compares clock, text and each reported buffer/state dimension:

| README row / shape | BSS | Measured text | Documented text | Gate log line |
|---|---:|---:|---:|---:|
| 351 / `endstation_arty_current` | 3,160 | 12,116 | 12,116 | 21 |
| 352 / `endstation_ax7101_1x1_tdm8` | 4,048 | 12,132 | 12,132 | 46 |
| 353 / `endstation_arty_4x4` | 5,452 | 12,124 | 12,124 | 7 |
| 354 / `endstation_arty_8ch` | 8,012 | 12,124 | 12,124 | 14 |
| 355 / `endstation_ax7101_8x8` | 14,408 | 12,136 | 12,136 | 57 |

`sizes.log` records a successful comparison and exact five-cell delta check. The initial auxiliary comparator wrongly assumed `data=0`, although the table contains no data column and the gate correctly reports 24. That reviewer-script assumption was removed; only claimed table quantities are compared. `sizes-initial-check.*` and `comparison-note.txt` preserve the correction. The passing firmware gate was neither changed nor rerun.

**Prior finding dispositions**

- **R524-3-F1 | MINOR | Docs | RESOLVED | `sw/firmware/ctrl_nvm/README.md:351-355`.** Authority/evidence: the section claims pinned-SDK object measurements; the exact-head gate and BSS-matched table above now agree for every shape. Impact of the former defect: all five documented text figures were four bytes low. Required outcome: accurate measured figures without unrelated changes. Verification: the required command returned 0, all five comparisons passed, and the delta contains only the five corrections. No required change remains. Original finding: [R524-3](https://github.com/kebag-logic/milan-fpga/pull/684#issuecomment-6030939675).
- **R524-1-F1 / R525-1-F1 | MINOR | Conformance, Docs | RESOLVED, retained | PR #684 authority bullet.** Authority/evidence: the current body attributes the advertiser to Milan v1.2 5.6.3 and the ADPDU to IEEE 1722.1-2021 6.2, matching `sw/firmware/ctrl/adp/adp.h:9`. Impact of the former defect: a wrong clause attribution. Required outcome: correct both citations. Verification: `audit_public.py`, `pr-body.json` and `public-audit.log` confirm the correction remains present. No required change remains.
- **R524-1-F2 / R525-1-F2 | MINOR | Tests, Docs | RESOLVED, retained | #677 comments 6024328677 and 6024757146; `sw/firmware/gtest/README.md:284`.** Authority/evidence: [the correction](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6024757146) states 14 exclusion rows, five ADP rows. Impact of the former defect: an overstated exclusion census. Required outcome: publish the accurate census while preserving the original comment. Verification: the independent audit finds 14 identical file/function/statement/excluded-item identities at source base and head, including five ADP rows; the original and separate correction both remain. No required change remains.
- **R524-3-S1 | SUGGESTION | Tests | RETAINED, optional | `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:150`.** Authority/evidence: the gate prints sizes without checking the README. Impact: future documentation drift can escape the gate. Suggested outcome: tie the table to the measurement, as follow-up under [#495](https://github.com/kebag-logic/milan-fpga/issues/495), per this round's assignment. Verification for that future work: a deliberately stale table must be detected. This round's portable comparator supplies review evidence; it does not add a repository gate. No GitHub update was made here.
- **R525-3-S1 | SUGGESTION | Conformance, RTL | RETAINED, optional | `sw/firmware/gtest/rv32_include/assert.h:17`, `sw/firmware/ctrl/test/ctrl_build.py:46`.** Authority/evidence: [R525-3](https://github.com/kebag-logic/milan-fpga/pull/684#issuecomment-6030841235) records the future target-runtime assertion-handler seam; both named artifacts are unchanged. Impact: none in today's object-only build; a future target link must supply the named handler or align the declaration and allowed name with its runtime. Suggested outcome and verification: resolve the assertion interface when introducing a linked debug image, and prove that image links. No current source change is required.

The public audit found six prior verdict comments, zero submitted reviews and zero inline comments. Round-2 dispositions and both round-3 finding sets are accounted for above. The original severities and all assigned lenses are preserved. No finding is downgraded to RESIDUE.

**Five-lens results**

[R525] PASS Conformance - `sw/firmware/ctrl_nvm/nvm_klj2.h:105`, `nvm_klj2.c:296-301`, `sw/firmware/ctrl/adp/adp.h:130`, `delta.diff` - independently checked the loaded-prefix contract, container-end precedence, and documented single-event-loop no-callback contract against #677/#678. None changes in round 4. The corrected public clause attribution remains accurate.

[R525] PASS RTL - `source.diff`, `history.txt`, `sw/firmware/ctrl/adp/adp.c:21`, `sw/firmware/gtest/rv32_include/assert.h:5`, `integrity-final.log` - checked architecture applicability and the merge history. The six guarded port calls, entry checks, runtime declaration, HDL, clock/reset/CDC paths, shipping build inputs and gitlinks are unchanged since round 3. No new hardware claim arises from the five size cells.

[R525] PASS Robustness - `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:18`, `sw/firmware/ctrl/test/test_adp_reentry.cpp:146`, `delta.diff`, `ctrl-nvm.log:43` - inspected the 40/47/48-byte and last-payload boundaries and both inline-expiry regressions with same/cross-instance coverage. Their code and mutation controls remain unchanged; the default sanitizer case passed again. Round-3 negative-control coverage remains applicable.

[R525] PASS Tests - `sw/firmware/ctrl_nvm/test/nvm_rv32.py:50`, `test_ctrl_nvm.py:145`, `sw/firmware/gtest/fw_gtest.py:78`, `ctrl-nvm.log`, `sizes.log`, `public-audit.log` - traced the compiler selection, object-size sum and emitted measurement to the table comparison. Verified the default sanitizer wiring, unchanged catalogs/ratchet/exclusions, five successful builds and 435 passing tests. No test or expected result changed in the delta.

[R525] PASS Docs - `sw/firmware/ctrl_nvm/README.md:337-355`, `sdk.log`, `ctrl-nvm.log`, `sizes.log`, `pr-body.json` - every changed measurement now matches its row by BSS. The surrounding object-only and stack limits remain accurate. The five-cell change closes R524-3-F1 without altering any other table quantity or contract.

**Reviewer-owned ledger applicable at this head**

R525-3 covered the four untouched lenses at exact head `34475e774dfe1c92c81fa51293668e64dc95fa85`. R525-4 independently checked each lens's applicability and proved that no artifact in its scope changed. That coverage is carried forward to the head below; the full round-3 campaigns are not claimed as rerun. Docs is covered anew, and Tests also has this round's focused execution.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #677/#678; `nvm_klj2.h:105`; `nvm_klj2.c:296`; `adp.h:130`; corrected PR authority; `delta.diff` | R525-3; R525-4 continuity | 708e5634f28e6e5a19236a9b0a9a543c3622e52d |
| RTL | CLEAN | `source.diff`; `history.txt`; `adp.c:21`; `rv32_include/assert.h:5`; `integrity-final.log` | R525-3; R525-4 continuity | 708e5634f28e6e5a19236a9b0a9a543c3622e52d |
| Robustness | CLEAN | `test_nvm_prefix.cpp:18`; `test_adp_reentry.cpp:146`; unchanged mutation sources; `ctrl-nvm.log:43` | R525-3; R525-4 continuity | 708e5634f28e6e5a19236a9b0a9a543c3622e52d |
| Tests | CLEAN | `nvm_rv32.py:50`; `test_ctrl_nvm.py:145`; sanitizer wiring; `ctrl-nvm.log`; `sizes.log`; exclusion audit | R525-3; R525-4 continuity and focused gate | 708e5634f28e6e5a19236a9b0a9a543c3622e52d |
| Docs | CLEAN | `ctrl_nvm/README.md:337-355`; `sdk.log`; `sizes.log`; `delta.diff`; current public corrections | R525-4 | 708e5634f28e6e5a19236a9b0a9a543c3622e52d |

**Evidence limits and pending manager duties**

Selected public executable receipts at [archive 412c0f10](https://github.com/kebag-logic/milan-fpga/tree/412c0f10e12755a47f79ec3f90e08ef5d2ecaa47/review-evidence/677-r1) were verified against the published SHA-256 manifest: store controls, the restored-end sanitizer failure, coverage, its self-test and the 109-caught campaign record. `public-evidence-check.txt` records those checks. Those are historical receipts for `6c94e9f5`, not fresh execution at this head. The round-3 public review and execution comments supply the unchanged broader evidence; this round repeats only the requested focused gate and audits.

The assignment states that the manager's full source static/builder and native banks passed at this head. Their acceptance remains the manager's responsibility. The public snapshot contains no separate manager native-bank receipt; publish or link the exact-head source evidence when establishing the full merge bar. Source validation is distinct from the final current-dev candidate, which the manager must construct and validate at the merge turn.

`hosted-checks.json` is one read-only snapshot at this exact head. `firmware-unit`, the four Yosys shards, lint, conformance and some fast checks had succeeded; other jobs were still running. The long aggregate verdicts were not yet established. Physical gPTP was **skipped**, not executed. Hosted/local-replica acceptance belongs to the manager; this review does not supply it.

No full parent/processor/timing/synthesis/builder bank, full mutation campaign, hardware operation or local workflow replica was run by this round. Physical calibration was **NOT RUN**. Field and calibration skips are not hardware proof. Object builds and host tests establish no board timing, physical power-cut behavior, linked assertion handler or runtime stack bound.

Before and after execution, direct blob hashing verified 1,150 superproject blobs, 214 axis-library blobs, 558 protocol-processor blobs and 104 gPTP-processor blobs, including kinds, executable modes and full index entries. Required gitlinks remain `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, `ead8036035affd53ef4b29979190f2f4f67084c0` and `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` respectively. No source edits or fault probes occurred; no source restoration was needed. All disposable installations/builds stayed in `scratch/`.

The manager still owns publication, the independent internal verdict, completion of all review rounds, exact-head hosted and local gates, current-dev candidate validation, explicit merge authorization, post-merge containment, and Issue/workflow completion. Carry both optional suggestions forward, with the table-to-gate item assigned to #495. Only REPORT.md and files named by MANIFEST.sha256 are publishable; scratch is excluded.

R525-4 FINISHED
