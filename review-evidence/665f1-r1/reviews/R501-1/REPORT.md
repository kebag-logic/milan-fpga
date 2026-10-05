[R501] NEGATIVE - exact head 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e

Round R501-1, external independent review of issue #665, F1 / PR #669.
Reviewed tree a574cf75a8d3a233ad7dc6b31ca31fbf1f214848 against source base fa450d301805881ad713b67521477bf042ddadfd.

All five lenses were applied independently before consulting prior public review findings. Four MAJOR findings remain. The supplied suites pass; the additional fault probes below reproduce behavior they do not exercise. No source changes or external writes were made.

## Findings

Short file paths below are relative to `sw/firmware/ctrl_nvm/`. Design page names refer to `docs/design/`. Probe exit 0 means the stated defect was reproduced; it is not a passing product verdict. No RESIDUE or SUGGESTION is filed.

### R501-1-F1 - MAJOR - Conformance, RTL, Robustness, Tests

Artifact: `sw/firmware/ctrl_nvm/nvm_store.c:143`, `:148`, `:158`, `:172`, `:275`; `test/nvm_checks.py:262`.

Authority/evidence: FASTCONNECT sections 6.2 and 7 require CRC-validated input and selection of the newer accepted generation. `nvm_slot_check` checks a streamed CRC, then rereads the header/body without checking that reread's CRC and takes SEQ from it. The final in-RAM validation does not require that its SEQ equals the sequence used for selection/publication. `probe_store.c` changes exactly one bit in byte 8 of slot A's post-CRC body reread, leaving flash unchanged. Valid A=5 and B=6 become selection metadata A=13 and B=6. `store-probes.log` records `auth=0 published_seq=13 staged_seq=5 restored_name=55`, where the newer B requires `auth=1 seq=6 name=66`.

Impact: a transient read fault restores the older saved state as COMPLETE, publishes a sequence not present in its validated container, and makes the actual newer slot the next erase target. Rechecking the staged container alone does not protect the authority decision.

Required outcome: derive selection and published authority from the same validated generation bytes. A subsequent read discrepancy must be detected and handled without selecting an older slot on corrupted metadata or publishing a different sequence.

Verification: extend read-fault tests to the post-CRC reread's sequence/header bytes, both slots and wrap boundaries; require the correct selected payload and equality between published and validated generation. Retain a planted control that restores this gap. Reproduce with `run_probes.py`.

### R501-1-F2 - MAJOR - Conformance, RTL, Robustness, Tests

Artifact: `sw/firmware/ctrl_nvm/nvm_store.c:298`, `:398`, `:611`; `test/nvm_checks_write.py:149`.

Authority/evidence: D3 section 15.1 DR2c and section 6.3 allow at most three firmware attempts per unchanged work set, separated by 1,000 ms. `nvm_store_commit_now` checks only IDLE, sets force, and calls `nvm_capture_begin`, bypassing the backoff and exhaustion checks in `nvm_idle`. The header documents bypassing debounce, not overriding DR2c. The unchanged-source probe holds one work set against erase-stuck faults and calls this public entry point after failures. `store-probes.log` records a fourth erase/failed transaction despite `exhausted=1`, with successive erase-start gaps 22,071 / 22,072 / 22,071 us.

Impact: console requests can defeat both the attempt cap and failure spacing, repeatedly erasing a failing target without any new accepted change.

Required outcome: every transaction entry point preserves the DR2c work-set budget and spacing. Any exception requires an explicit public owner decision rather than an implicit console bypass.

Verification: test forced commits during backoff and after exhaustion, with unchanged and genuinely changed work sets, on both ports; require no fourth attempt and no early retry. Plant independent bypass controls. Reproduce with `run_probes.py`.

### R501-1-F3 - MAJOR - Conformance, RTL, Robustness, Tests

Artifact: `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c:171`; `nvm_store.c:305`, `:307`, `:452`; `nvm_flash.c:9`.

Authority/evidence: F1's time port supports DR2a/DR2c windows and the FASTCONNECT section 9.4 failure deadlines. The port clamps a backward PHC step to the prior maximum until the PHC catches up. This is nondecreasing but does not preserve elapsed time. The probe keeps firmware and media state intact, steps the PHC backward by 60 seconds after accepting a change, and services the loop for three seconds. `store-probes.log` records `raw_elapsed_us=3000026 port_elapsed_us=0 erases=0 dirty=1 phase=1`.

Impact: legal clock correction extends debounce/backoff and media timeouts by the backward step's magnitude. A hung operation's timeout can stop progressing; repeated corrections can postpone it indefinitely. The same clock makes the blocking helper's timeout unreliable.

Required outcome: use an elapsed-time source or compensation that continues advancing across PHC corrections, with stated bounds for the F0 time seam. Nondecreasing timestamps alone are insufficient for these timers.

Verification: exercise forward/backward PHC changes during debounce, retry backoff, erase/program hangs and the wait helper. Assert elapsed deadlines against an independent running clock. Reproduce the backward-step case with `run_probes.py`.

### R501-1-F4 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

Artifact: `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c:59`, `:71`; `nvm_flash.h:23`; `README.md:133`; `test/nvm_checks_write.py:213`; `host/litespi_model.c:47`.

Authority/evidence: F1 requires bounded service steps and a usable event-loop seam; the port and README claim every operation-start returns and every service step is bounded. `ls_open` drains RX indefinitely, and `ls_xfer` waits indefinitely for TX and RX readiness. These loops occur inside `busy`, `program` and `erase`, before the store's timeout can run. The host controller model always supplies immediate readiness. `run_controller_probe.py` links the unchanged port and injects fixed CSR status at the host boundary. TX-not-ready, RX-not-ready and RX-never-drains each fail to return within a one-second process deadline; `controller-probe.log` records all three.

Impact: a stalled controller traps the single event loop inside one service call; the flash-operation timeout and other protocols cannot run. The stated per-call bound is unsupported on these failure paths. This is a code/verification/contract defect, not wording residue.

Required outcome: bound each controller wait and return a media fault with chip select/controller state safely released, or provide an equivalently bounded nonblocking port state machine. The documented bound must state its actual assumptions and include failure paths.

Verification: inject delayed and permanently stalled TX/RX status and a nonempty RX that never drains; assert bounded call completion, failed-transaction accounting, intact authoritative media and continued loop service. Retain the three reviewer probes and planted controls.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue #665 body and scope comments 5993775541 / 5992455815; #640 D4/D5 5991591637; #658 ruling 5988843004; FASTCONNECT 4.2/6/7/9.4; MATERIALIZATION 6/7/8/15.1; SNAPSHOT_OWNERSHIP 7; `nvm_klj2.c`, `nvm_store.c`, flash port; F1-F4 | R501-1 | 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e |
| RTL | UNCLEAN | No HDL diff; pinned `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv` ownership/restore/write rules; `nvm_state.h`, store FSM and static shape; LiteSPI port vs shipping access routines; F1-F4 | R501-1 | 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e |
| Robustness | UNCLEAN | Codec refusal paths, erased spans, sequence wrap, D3 rollback/CLOSED, dirty/inflight separation, retries, page and journal guards; flash/controller/state fault models; reviewer probes; F1-F4 | R501-1 | 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e |
| Tests | UNCLEAN | Entire `test/` driver/check/mutant/RV32 set and `host/` models; recorded 1x1/8x8 vectors; baseline gates plus fault probes; F1-F4 | R501-1 | 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e |
| Docs | UNCLEAN | `docs/README.md` diff, module README, public PR body and published HANDOFF, source gate receipts, capture measurements; per-step bound fails F4 | R501-1 | 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e |

## Checks and positive evidence

- Reconstruction followed the requested public order. The reviewed change is 32 new/changed files, +4,751 lines, in `ctrl_nvm` plus one documentation-index row; eight one-line commits.
- Independently reran `test_ctrl_nvm.py --require-rv32 --self-test`: all five shapes, 26 checks each, 24 on both ports, all 46 planted defects caught. `store-suite.log` and `.rc` retain the raw result.
- Independently reran the shipping writer suite with `--self-test`, and `scripts/check_nvm_capture.py`: both rc 0. The three independent gates ran concurrently under a foreground coordinator with individual logs/return codes; no detached jobs remain.
- Codec byte order, framing, CRC variants, exact record inventory, ascending IDs, erased-record acceptance and refusal ordering were checked against the authorities and reference codec. The ordinary wrap comparison and default tie rule are sound for sequential A/B generations; F1 concerns unverified metadata, not the comparison arithmetic.
- Boot tests exercise valid/blank/torn/version/corrupt input, erased defaults, re-stage data corruption, apply/settle faults and rollback failure. The apply/settle/name order and release only at COMPLETE/BLANK/DEFAULTS are implemented; CLOSED retires service. The state port remains an abstract adapter: actual SET judges, owner writes, reset/debt containment and #658 clipping are not integrated or proved by its synthetic host implementation.
- Ordinary writes preserve the authoritative slot, program ascending pages and move authority only after byte-equal read-back. Dirty and in-flight bitmaps preserve changes accepted after their record's capture. DR2a first-dirty behavior, DR2b verified-byte suppression and DR5 blank-slot preference pass their named checks. F2 identifies the untested alternate transaction entry point.
- The 3,126 cut cases are 6 times the per-shape counts 81+121+45+61+213: three starting media states, two ports, four fractions of every erase/page program, and one cut on entering read-back. This enumerates every media-changing operation at those fractions, not every physical cell or CPU instruction. Capture/seal/blankcheck and read-back do not write media; a reset there reduces to the intact old image or fully programmed new image. The read-back case is representative, not a sweep of every read-back step. The recovery check commits another change and reboots. No hardware power-cut claim follows.
- The recorded-vector round trip compares full container bytes to the independent encoder and checks the recorded length, CRC and every record offset before booting the same values. The existing 1x1 and 8x8 records remain unchanged.
- RV32I freestanding sizes reproduced exactly: bss 4,000 bytes at 1x1 and 14,360 at 8x8; stage 3,344 / 13,264 bytes; largest payload 136 / 576 bytes; chunk 256 bytes. Every production buffer is static; the inspected production sources contain no heap or OS service.
- The nominal `max(256, 2P+6)` figure counts selected payload/CRC work in the store; it is not a cycle count or all memory accesses including callbacks. The 1.2 ms estimate scales the older capture's measured byte-copy rate to different work. README explicitly calls it DERIVED and excludes CPU/hardware proof. That qualification is honest; it cannot discharge #640 D5 or establish a worst-case CPU service bound, especially with F4's unbounded waits. The existing 24.5 ms receipt still grades only the unchanged shipping writer.
- `scope.log` proves the shipping writer, its Makefile and the SoC source are byte-identical to base. No build input links `ctrl_nvm` into any image at this head. The default-off F0 switch and eventual state-owner adapters remain separate integration obligations. Service/change hooks and a replaceable time callback are a credible seam, subject to F3/F4.
- Examined published executable evidence at commit `38e93660c8e2d4c190a00e8538611de01fece598`, `review-evidence/665f1-r1`: HANDOFF, cut table, store and builder logs/receipts, docs check and record-space log. The source builder receipt says rc 0 with gate 11 NOT RUN (missing physical calibration report). It is not hardware evidence or final-current-dev candidate evidence.

## Limits and manager duties

No full parent/processor/gPTP/synthesis/builder banks were rerun, and no container, privileged, shared-install or hardware action was used. No physical calibration or field campaign was run. Hosted/replica acceptance remains manager-owned; this review does not count skipped contexts as executed jobs.

Fix F1-F4 and re-review the affected artifacts at the new exact head. The manager must reconcile independent reviews, publish the packet, own source/candidate/hosted acceptance, validate the final merge candidate against then-current dev, obtain explicit merge authorization and perform post-merge containment. Issue #665 remains open for its other lanes. The shipping writer's separately reported VD_REC/VD_LEN discrepancy is unchanged by F1 and needs its own public follow-up.

## Public finding reconciliation

After writing this independent verdict and ledger, read all PR #669 issue comments, reviews and inline review comments. The public PR had two review-start comments, zero reviews and zero inline comments; no prior public FINDING was available to resolve or retain. The issue #665 comment audit likewise found no reviewer entry for F1/PR #669. `prior-findings.log` records the retrieval time and counts. No other reviewer's report was consulted before the independent verdict.

## Final integrity and reproduction

`integrity.log` / `integrity.rc` prove 1,043 superproject blobs and modes plus the full index against the exact head/tree, and all tracked bytes/modes/indexes in the required submodules:

- `protocol-processor`: 472 blobs, pin `631eeb342ca1e3fa80e734077a56a943aee76ff1`;
- `gptp-processor`: 104 blobs, pin `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`;
- `third_party/verilog-axis`: 214 blobs, pin `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

The optional `external` checkout was uninitialized and unused; its gitlink/index entry is unchanged. The checkout is clean, with no source edits to restore. All compilations and disposable test data were confined to the packet's `scratch/` directory. No job remains running.

From the packet directory, supply the path of an exact checkout:

```sh
python3 run_checks.py /path/to/exact-checkout
python3 run_probes.py /path/to/exact-checkout
python3 run_controller_probe.py /path/to/exact-checkout
python3 verify_integrity.py /path/to/exact-checkout
sha256sum -c MANIFEST.sha256
```

The first command retains per-gate raw logs and return codes. The second builds the shared shape header needed by the third. The published raw probe results are `store-probes.log` and `controller-probe.log`, with their return codes. `scope.log` records the unchanged shipping inputs, and `public-evidence.log` identifies the examined public receipts. `MANIFEST.sha256` is the publication allowlist; `scratch/` is excluded.

R501-1 FINISHED
