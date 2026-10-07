[R532] POSITIVE - exact head f74b9403b330ce316eeec6f724846f16def98443

# R532-7: internal cleared-context review of PR #690 (issue #665, lane F4), round 7

- Role: internal independent reviewer `[R532]`, cleared context. Assignment: issue #665 comment 6040189958 (round 7). Review start: PR #690 comment 6040915869.
- Exact head `f74b9403b330ce316eeec6f724846f16def98443`, tree `13e6c9d6e2dceb981c5c2976d85e07fbe287a996`. Both are verified in `receipts/integrity.txt`.
- Delta reviewed: `cce554f6..f74b9403`, one commit, "Bound SRP receive allocation retries by original arrival". It touches six files:
  - `srp/srp_mbx.c` and `srp/srp_mbx.h`;
  - `srp/README.md`;
  - `test/srp_rx_retry.cpp` and `test/srp_mutants.py`;
  - `gtest/coverage.ratchet`.
- Full-lane context: `db9aa8c9..f74b9403`, from the FC r2 head. No HDL file changes in this delta.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open. There is one RESIDUE (R1, wording only) and one SUGGESTION (S1).
- Every round-7 assignment item is met and independently re-executed:
  - R532-6-F1 is resolved;
  - R532-6-F2 is resolved, and the published size table reproduces byte-exactly;
  - R532-6-S1 is addressed.
- Public evidence read:
  - issue #665: the body, lane assignment 6030279477, size acceptance 6030870481, round-7 assignment 6040189958 and REVIEW READY 6040854685;
  - the live PR #690 body;
  - the author packet `review-evidence/665f4-r1/author-r7/` at evidence commit `80a75f9a`. It contains `HANDOFF.md` and `PR-BODY.md`. The `ROUND7-*` files they cite are not published.
- Prior review reports were read only after the independent pass, verdict and ledger below were written.

## Findings

### R1 - RESIDUE - Docs - `sw/firmware/ctrl/srp/README.md:59` - binding retry contract omits expiry

- **Authority / evidence:** the API header `sw/firmware/ctrl/srp/srp_mbx.h:97-98` was updated in this commit to "retry after owed transmission commits and retained reception completes or expires". The README's restatement of the same port contract still reads "Retry after owed transmission commits and retained reception completes."
- **Impact:** wording only. No code, test, figure, measurement or clause claim changes. The binding refusal is released at expiry (`srp_mbx.c:295`, `:388-395`), and the code and header agree.
- **Exact fix:** `Retry after owed transmission commits and retained reception completes or expires.`
- **Verification:** the README line matches `srp_mbx.h:98`.

### S1 - SUGGESTION (non-blocking) - Docs, Robustness - `sw/firmware/ctrl/srp/README.md:81`, `srp_mbx.c:376-377`

- `refused` counts every failed attempt, not every record. Over one held record my probes see 99,903 refusals at up to 50 service passes per simulated millisecond (`receipts/matrix/head-r532_7_bound_probe-if*.log`). `rx_discarded` is the per-record signal.
- Consider saying in the README that `refused` is an attempt count, so that an operator reads `rx_discarded` for lost records.

## Round-7 assignment items (6040189958)

| Item | Disposition | Evidence |
|---|---|---|
| R532-6-F1: bound retention | **RESOLVED.** The bound is 1000 ms from the original mailbox arrival (`srp_mbx.c:20`). `expire_receive` (`:388-395`) uses modular `uint32_t` elapsed time against the fabric `NOW_MS`; the RX record's `ARRIVAL_MS` is the same 32-bit clock (`mbx_contract.h:344-347`). It is checked on the first refusal (`:415`), on a failed eligible retry (`:670`, after a successful retry has had priority at `:667-668`), and on failed participant recreation (`:657-660`). | Head probes below; plants below |
| Discard once, distinct counter | **MET.** `len=0; ++rx_discarded` (`:392-393`). It is neither `received` nor `malformed`. The repeated oversized PDU (8 sends) yields exactly 8 discards, with `malformed=0`. | `R5327.RepeatedOversizedRetransmission` |
| Later input on every interface and the binding port proceed | **MET.** The N=150 record holds a Listener Lv queued on the last interface until 995 ms after the Lv's arrival, and `srp_mbx_bind` returns true at 998 ms (IF=1 and IF=2). | `R5327.TimedHolOneFifty`, `R5327.BindingProgressByTheBound` |
| R533-5 recoverable cases still pass | **MET.** The unchanged `r533_5_independent.cpp` passes 4/4 at IF=1/2. The unchanged R532-6 retry probes pass 6/6. The 11 original receive tests pass, and recovery at exactly the deadline still applies the full record (`RecoveryAtDeadlineStillAppliesTheCompleteRecord`). | `receipts/matrix/head-*.log` |
| IF=1 and IF=2 regressions with a wire-valid over-capacity PDU and later input on another interface | **MET.** `srp_rx_retry.cpp:277` uses 150 Domain vectors with no artificial exhaustion, then an Lv on `MBX_N_IF-1`. At IF=1 the later input is necessarily on the same interface. | 17/17 at IF=1/2 |
| A plant that removes the bound must fail | **MET.** The lane's `receive-retention-unbounded` and `receive-flood-unbounded` plants are caught at IF=1 and IF=2. My independent plants `rv-poll-no-expire` (expiry removed from the retry path) and `rv-retry-renews-deadline` (a moving window) fail the lane suite and my probe at both counts. | `receipts/matrix.tsv` |
| Reviewer probes | **PASS.** See the probe table. | |
| `srp/README.md` states the bound and that every Class A Domain value is retained | **MET.** `README.md:35-36` and `:90-102`, `:131-132`. | |
| R532-6-F2: size deltas with attribution | **RESOLVED.** My 16 links reproduce every published figure exactly. | Size table |
| R532-6-S1 | **ADDRESSED.** `README.md:85` now reads "pending events". | |

### Probe results at head (millisecond-stepped host model, generated entity-sized pool)

| Probe (source) | IF=1 | IF=2 | Bar |
|---|---|---|---|
| `r532_hol_probe.cpp` (unchanged), N=2,12,20,30,150 | 5/5 pass | 5/5 pass | complete or discard; later Lv received |
| `r532_7_bound_probe.cpp` TimedHol N=30 | retained; Lv revoked **995 ms** after its arrival | fits the pool; revoked in 1 ms | < LeaveTime 5000 ms, and <= 1000 + 20 ms |
| TimedHol N=150 | **995 ms** | **995 ms** | same |
| `r532_flood_probe.cpp` (unchanged): 60-frame Domain flood, then Lv | `revoked_after_ms=0` | `revoked_after_ms=0` | < 1000 ms (rapid-leave pass) |
| LeaveDuringDomainFlood: Lv sent while a flood record is retained | 0 ms (the retained record completed when reclaim freed storage) | **998 ms**, 3 discards | <= 1020 ms |
| RepeatedOversizedRetransmission: 150-Domain PDU every 1000 ms, Lv at t+2500 | 500 ms (bounded by the record ahead of it), 8 discards | same | <= 1020 ms |
| BindingProgressByTheBound | bind true at **998 ms** | **998 ms** | <= 1020 ms |
| StorageAfterDiscardInformation (information only) | a fresh Talker Advertise on the last interface is received after the discard | same | none |
| `r533_5_independent.cpp` (unchanged) | 4/4 | 4/4 | pass |
| `r532_retry_probes.cpp` (unchanged) | 6/6 | 6/6 | pass |
| lane `srp_rx_retry.cpp` | 17/17 | 17/17 | pass |

### Plants

- **The lane's 12 new plants** (`srp_mutants.py:575-609`) are planted one per disposable copy and graded with the lane's own `caught()` rule: the named test fails, and its failure block contains the required observable. All 12 are **CAUGHT at IF=1 and at IF=2**: `retention-unbounded/short/late`, `discard-uncounted/malformed/as-success`, `queue-renews-deadline`, `first-refusal-never-expires`, `expiry-precedes-recovery`, `recreate-never-expires`, `flood-unbounded` and `deadline-not-modular`.
- **Reviewer plants** (`scripts/r532_7_matrix.py`). Each fails the lane suite **and** my probe at IF=1 and IF=2, with behavioural failures (rc 1), not build failures:

| Plant | Lane tests that fail |
|---|---|
| `rv-poll-no-expire` | Oversized, RetainedDeadlineCrossesClockWrap, DomainFlood |
| `rv-retry-renews-deadline` | the same three |
| `rv-expire-keeps-record` | five tests |
| `rv-discard-as-refused` | five tests |
| `rv-bound-leavetime` (5000 ms) | five tests |

- **Complete SRP campaign** at this head, sharded across workers (`scripts/r532_7_campaign.py`, the head's `srp_mutants.DEFECTS` and `caught()`):
  - **IF=2, the campaign's defined count: 102/102 caught.**
  - IF=1: 99/102. The three escapes are two-interface plants by construction, and none is in this delta:
    - `peer-reset-cancels-retained-receive`: its test is compiled only under `#if MBX_N_IF > 1`;
    - `failed-interface-starves-peer` needs a peer interface;
    - `failed-init-leaks` needs an earlier interface to leak.
  - A first run from a non-Git export lost five walk/reuse plants to the missing gitlinks. It is retained as `campaign-export-if2.*` and not counted.

### Linked size (R532-6-F2), reproduced independently

- **Build inputs:**
  - the CI-pinned RV32 SDK, installed into scratch by `scripts/ci_rv32_sdk.py` from archive sha256 `d42680e9...`;
  - one runtime built from LiteX `a1e1c365`, picolibc `6a13ccce` and compiler-rt `6eb76609`;
  - each revision's own fixture and lwSRP pin: head and round 6 at `9197193e`, round 5 at `a4cbe41d`;
  - the lane base `db9aa8c9` linked `--without-srp` through the round-5 fixture, because the head fixture requires MAAP sources, which the base lacks.
- Receipts: `receipts/size/*.json`, `TABLE.md`.

| Shape / IF | Text | BSS | RAM span | vs base | vs round 5 | vs round 6 |
|---|---:|---:|---:|---:|---:|---:|
| 1x1 / 1 | 33560 | 18072 | 62688 | +43936 | +8096 | +128 |
| 1x1 / 2 | 34792 | 29424 | 75264 | +56016 | +9424 | +112 |
| 8x8 / 1 | 33500 | 32824 | 77376 | +58624 | +8096 | +112 |
| 8x8 / 2 | 34744 | 58928 | 104720 | +85472 | +9424 | +112 |

- Every span and delta equals the author's published table (PR body and `author-r7/HANDOFF.md`).
- Attribution against round 5, from symbol sizes:
  - `image_srp` +1528 B is the one shared retained `struct mbx_frame`;
  - `image_app` +1104/+2172 B at IF=1/2 is the MAAP application state;
  - `image_allocation` is new, at 8/16 B;
  - text grows +5452/+5708 B, about 5 KB of it MAAP composition. The author attributes 5036/5368 B of that to MAAP text.
- Round 7 alone adds +116 to +120 text bytes, +0 BSS and +112 to +128 span. `image_srp` is unchanged from round 6 in every shape: the new `rx_discarded` word fits existing struct padding. This confirms "no BSS".
- The largest shape is 104720 B, against the roughly 128 KB block-RAM budget in 6030870481.

## What was checked, by lens (independent pass)

[R532] PASS Conformance - `srp_mbx.c:20,388-395,415,657-670`; `srp/README.md:82-136`; `mbx_contract.h:344-347`; assignment 6040189958; Milan Table 4.3 LeaveTime (`README.md:121`, 500 cs); `docs/reference/FR_NFR.md:451`; probes `R5327.*`, `r532_hol_probe`, `r532_flood_probe` at IF=1/2 - Each assignment item is satisfied as tabulated above, including both probe bars: the later withdrawal is received within LeaveTime (995 ms worst case, against 5000 ms), and the flood probe revokes at 0 ms. Discarding a refused PDU is ordinary MRP loss, recovered by peer refresh. The 1000 ms recovery limit is documented as not enlarging the 10 ms service budget (`README.md:101`, `:136`; `FR_NFR.md:451`), so exhaustion latency is still reported as a timing failure, not as conformance. The size acceptance (6030870481) is met: both shapes, both interface counts, and deltas from base and round 5 with attribution, reproduced exactly.

[R532] PASS RTL - `srp_mbx.c:295,347-356,388-418,640-672`; `srp_mbx.h:71,80,97-99`; `ctrl_loop.c:119-160`; delta file list (no HDL); mailbox recipe run `receipts/runs/mailbox.log` - This is a firmware-architecture review; the delta has no HDL. Expiry runs only inside the serialized ports. The SRP `rx_ready` gate still blocks overtaking, and RX is per-channel, so ADP/MAAP are unaffected. Modular subtraction is wrap-safe; the wrap and boundary are tested at UINT32_MAX-499. Constant and comparison widths are `uint32_t`. Inserting the new counter leaves the `struct srp_mbx` storage size unchanged. The binding refusal at `:295` releases at expiry. Destroy (`:270`) and own-interface reset (`:591-592`) still cancel the record. Without an eligible retry there is no expiry: owed TX or pending events block RX and binding anyway, and that is documented (`README.md:92`, PR known limitations). The published mailbox recipe, run from a fresh tracked export with scoped Verilator 5.050, passes Wishbone 316/0, AXI4-Lite 361/0, IF=2 316/0 and 361/0, model 316/0 and cosim 13/0.

[R532] PASS Robustness - `scripts/r532_7_bound_probe.cpp` (6 cases), `r532_hol_probe.cpp`, `r532_flood_probe.cpp`, `r532_retry_probes.cpp`, `r533_5_independent.cpp` at IF=1/2; 5 reviewer plants - Checked:
- the over-capacity single PDU (N=30 at IF=1, N=150 at both counts);
- a flood with the Lv sent mid-retention;
- periodic retransmission of the oversized PDU: every later record is bounded by its own arrival, and a queued record gets no fresh window;
- the binding port during retention;
- recovery at exactly the deadline;
- failed recreation;
- clock wrap;
- repeated discards counted once per record;
- storage after the discard.

No case blocks beyond 998 ms. `malformed` stays 0, and the TearDown pool-leak and bad-free checks pass in every case.

[R532] PASS Tests - `srp_rx_retry.cpp:23-41,277-398`; `srp_mutants.py:575-609`; `coverage.ratchet:19`; `receipts/runs/coverage-check.log`; `receipts/runs/campaign-if{1,2}.log`; `receipts/suites/*` - Results:
- Each of the six new tests fails under at least one of its mapped plants at both counts. Five independent reviewer plants are each caught by the lane suite.
- The full campaign catches 102/102 at IF=2.
- `fw_coverage.py --check` passes all 19 files at 100%, with `srp_mbx.c` at 469/469 lines and 438/438 branches and no exclusion change.
- The remaining SRP suites pass at IF=1/2: 53 adapter, 5 latency, 5 processor-wire differential, 2 composition and 1 shape.
- The tests use the real generated pool, with no artificial exhaustion in the oversized and flood cases. The clock-wrap case independently fixes `model.now_ms` near UINT32_MAX.

[R532] PASS Docs - `srp/README.md:35-36,59,82-136,203-206`; `srp_mbx.h:80,97-99`; live PR #690 body (head `f74b9403`); `author-r7/HANDOFF.md`, `PR-BODY.md`; 27 docs gates `receipts/docs/summary.txt` - Results:
- The bound, its anchoring, check points, precedence, counter and recovery path are stated and match the code.
- "Every valid Class A Domain value" is stated.
- The evidence section describes the new tests and the bound-removal plant.
- The PR body names the current head with no stale publication wording. Its size table matches my reproduction, and its mailbox recipe executes.
- All 27 docs gates exit 0.
- R1 is RESIDUE, wording only, and does not leave the lens unclean.

## Reviewer-owned lens ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 6040189958, acceptance 6030870481; `srp_mbx.c:20,388-418,640-672`; `mbx_contract.h:344-347`; README timer table; FR_NFR 451; probe and size receipts | R532-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| RTL | CLEAN | `srp_mbx.c:270,295,347-418,591-672`; `srp_mbx.h`; `ctrl_loop.c:119-160`; symbol sizes; mailbox recipe receipts (no HDL in delta) | R532-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| Robustness | CLEAN | `r532_7_bound_probe.cpp`, unchanged R532-6 and R533-5 probes at IF=1/2; 5 reviewer plants | R532-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| Tests | CLEAN | `srp_rx_retry.cpp`; `srp_mutants.py`; 12 lane plants at IF=1/2; 102-plant campaign at IF=1/2; coverage check; 5 other SRP suites | R532-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| Docs | CLEAN (R1 RESIDUE) | `srp/README.md`; `srp_mbx.h`; live PR body; author-r7 packet; 27 docs gates | R532-7 | f74b9403b330ce316eeec6f724846f16def98443 |

## Prior public findings at this head (read after the verdict and ledger above were written)

- **Sources:** my R532-6 report (PR #690 comment 6040181124) and the R533-6 report (6040143585). Their disposition tables carry rounds 1 to 5 forward.

| Finding | Disposition at `f74b9403` |
|---|---|
| **R532-6-F1** (MAJOR, unbounded retained record) | **RESOLVED.** See the assignment table, probes and plants above. |
| **R532-6-F2** (MINOR, size delta) | **RESOLVED.** The published table matches my 16 links exactly, with attribution. |
| R532-6-R1 (RESIDUE, PR body publication wording) | **RESOLVED.** The live body names Round 7 head `f74b9403` and the published Round 6 head, with no "unpushed" wording. |
| R532-6-S1 (pending-event wording) | **ADDRESSED.** `README.md:85`. |
| **R533-6-F1** (MINOR, mailbox recipe aborts) | **RESOLVED.** The live recipe archives only existing paths. I executed it from a fresh tracked export: export rc 0, `make` rc 0 in 46 s, with all bus suites passing (`receipts/runs/mailbox*.{log,rc}`). |
| R533-6-R1 (RESIDUE, publication tense) | **RESOLVED.** Same live-body evidence as R532-6-R1. |
| R532-5-F1 / R533-5-F1 (refused receive dropped as malformed) | RESOLVED, retained. The R533-5 probe passes, and the `refusal-malformed` and retry-removal class plants are caught in the campaign. |
| Rounds 1 to 4: R533-1-F1..F4, R532-1-F1/F2, R532-2-F1..F4, R532-3-F1/F2, R533-2-F1/F2 | RESOLVED, retained. Their plants (rapid leave, #608, lifecycle, shared bindings, admission/ReadyFailed, walk) are all in the 102/102 IF=2 campaign at this head. The linked-size finding R533-1-F4 is re-measured above. |
| R532-5-R2, R532-5-S1, R532-5-S2, R532-1-S1..S3, R532-2-S1, R532-1-R1/R2, R532-2-R1, R532-3-R1 | RESOLVED or ADDRESSED, retained. None of their artifacts is touched by this delta. |

## Real limits

- Host model only: no booted image, no target timing, and no hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The 1000 ms recovery limit is a local policy. While a refused record is retained, rapid-leave revocation behind it can take up to about 1 s, which is far above the 10 ms service budget. The lane documents this as a timing failure under exhaustion, and the assigned ceiling is LeaveTime. I graded it against both.
- Not run here:
  - the builder bank and the compiler-absent check (both manager-owned);
  - `test_ctrl_nvm.py`, the MAAP differential, dependency OFF/ON profiles and lwSRP's own suites;
  - the full 75-command docs bank (my 27-gate subset is in `receipts/docs/`);
  - the firmware RV32 shards themselves. Their compile paths are exercised by the 16 RV32 size links.
- Size fixtures are linked, not booted. The 8192-byte stack is a reservation, not a call-chain proof.
- The author packet's `ROUND7-*` receipts are not published. Every figure relied on above was re-executed.
- In the provided review clone `third_party/lwSRP` (and `external`) were not initialized. Its gitlink `9197193e` is unchanged, and builds used a separate clean checkout at that commit (`receipts/submodules-and-tools.txt`). The integrity line "lwSRP MISMATCH" reflects only the uninitialized directory.
- The review clone was never edited. Bytecode caches written by probe imports were removed. The final integrity check shows 1190 tracked files, bytes, modes and index equal to the head tree, and the three initialized submodules at their gitlinks and clean.
- Hosted checks at this head when read (15:42Z, `receipts/hosted-check-runs.tsv`): 14 success, 6 in progress (Verilator shards 0, 1, 2 and 4, docs-check and elaborate), and 1 skipped (Physical gPTP, nightly/manual only). None is counted here.

## Pending manager duties

- Carry R1 to the residue checklist. S1 is optional.
- Hosted and trusted local-replica acceptance at the final head, including the in-progress Verilator, docs-check and elaborate contexts.
- The builder bank and the compiler-absent check.
- Candidate merge validation against live dev (`e21c1ca0` per assignment; this clone's `origin/dev` reads `910f338d`), and post-merge containment.
- External review completion and merge authorization.
- Publication of this packet.

## Receipts

Every publishable file is listed in `MANIFEST.sha256` (paths relative to the packet root). Local roots are normalized to `$PACKET`, `$REPO`, `$PINNED_VERILATOR`, `$DOCS_ENV`, `$SDK_ARCHIVE_DIR`, `$HOME` and `$DATA`. Scratch (exports, builds, SDK, runtime sources, planted copies) is not published.

- `scripts/`:
  - `r532_7_bound_probe.cpp` (new);
  - the unchanged `r532_hol_probe.cpp`, `r532_flood_probe.cpp`, `r532_retry_probes.cpp` and `r533_5_independent.cpp` from the public R532-6 packet;
  - `r532_probe.py` (one change: one build job per probe);
  - the drivers `r532_7_matrix.py`, `r532_7_campaign.py`, `r532_7_sizes.sh` and `r532_7_size_table.py`;
  - `docs_gates.sh`, `integrity.sh` and `fetch_runtime.sh`.
- `receipts/matrix/` and `receipts/matrix.tsv`: head probes, the 12 lane plants with CAUGHT grading, and the 5 reviewer plants at IF=1/2.
- `receipts/runs/`: SDK install, runtime fetch and build, coverage check, the mailbox recipe, the campaigns at IF=1/2 (and the uncounted export attempt) and the docs-gate driver. `.rc` files use the form `<rc> <seconds>s` where timed.
- `receipts/suites/`: the remaining SRP suites at IF=1/2.
- `receipts/size/`: 16 link logs, JSON reports and `TABLE.md`.
- `receipts/docs/`: the 27 docs gates and their summary.
- `receipts/integrity.txt`, `receipts/submodules-and-tools.txt` and `receipts/hosted-check-runs.tsv`.
- How the runs were executed: probes, plants and campaigns ran with at most 16 parallel builds; concurrent jobs were started inside one foreground command and waited on there. Planted copies were disposable exports under scratch.

R532-7 FINISHED
