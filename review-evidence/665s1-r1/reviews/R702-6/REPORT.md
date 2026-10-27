[R702] POSITIVE - exact head 424b1489ccd8062180f90158556d343589b9e1e5

Round R702-6. This is the external, cleared-context review of PR #795 (issue #665, lane S1, `665-s1-faces` -> `dev-soft-core`). Tree `244ebb72d396e05e7b8cc6026e2a37732a355360`.

This is a delta round. The previously reviewed head is `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44` (R702-5, NEGATIVE, three MINOR findings). I judged `6d2b77bb..424b1489`: 4 commits and 12 files, covering the AECP core (`aecp.c`, `aecp_commands.c`, `aecp.h`, `aecp_internal.h`, `aecp_face.h`), `test_aecp.cpp`, `aecp_mutants.py`, and docs in `ARCHITECTURE_HW_SW_SPLIT.md`, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` and both READMEs. I then checked every named round-5 finding against its cause.

The delta touches nothing under `hdl/`, `tb/`, `syn/`, `sw/mailbox/`, `sw/litex/` or `.github/`, and no generated file (`receipts/checkout-integrity.txt`, "delta outside fw/docs: 0"). So the census, the contract-2.3 RTL and generated artifacts, the all-fabric export and the `KL_mbx` out-of-context evidence keep their prior lens verdicts. Nothing in this delta changes what they depend on.

Production firmware is byte-identical between `e493dccd` and the head; the two later commits touch only `test_aecp.cpp`. So the ledger's "firmware of `e493dccd`" is the head's firmware.

Scope came from the issue body and the S1 public record on #665:
- the assignment 6409739310;
- rulings 6410169666, 6412739248, 6421238472 and 6425357821;
- the owner clarification 6410301079;
- decisions 6409738976 (D1, D3);
- the round-6 assignment 6426858104.

The round-6 assignment asks for these, and all are met:
- R702-5 F1, first option;
- R701-5 F1, option (a);
- R702-5 F2 and F3;
- the residue W1-W3 and RES1-RES3;
- memory: the ledgered point at or under 57.5, the other three at or under 56.

**Verdict: POSITIVE.** No BLOCKER, MAJOR, MINOR or RESIDUE is open. Four SUGGESTIONs follow, all optional.

## What the delta does, checked at its cause

1. **An expired lock holds by its owner until its release is acknowledged** (`aecp.c:199-204`, `:372`, `:487-506`; `aecp_commands.c:16-28`, `:606-609`).
   - At 60 s, `asynchronous()` clears `locked`, commits LOCK_HELD 0 through `changed`, sets `unlocked`, and now keeps `lock_owner`.
   - `aecp_other_lock()` treats `locked || unlocked` as the lock in force. It is the single predicate behind:
     - the lock check (`aecp_foreign_lock`);
     - the ENTITY_LOCKED-to-ENTITY_MISBEHAVING mapping (`aecp.c:372`);
     - the MVU guard.
   - ENTITY_AVAILABLE (command 2, IEEE 1722.1-2021 7.4.3) and `aecp_locked` (the ACMP owner's reader, `ctrl_app_aecp.c:10-13`) read the same lock in force.
   - The owner is dropped only when the notification is built (`aecp.c:500-501`).
   - The face writer still publishes `core->locked` (`aecp_face.c:41`), so the datapath is given the release while the core still reports the lock held. That is the direction ruling 6421238472 item 3 requires.
   - I checked every other reader of `locked` or `lock_owner` (a search of all of `sw/firmware/ctrl`):
     - `arm()` (timer arming);
     - `lock()`, which cannot run while `unlocked`, because `refusing` is set (`aecp.c:347`) and the lock check refuses first;
     - the face writer.

     None of them presents state to a controller.
2. **SET_SYSTEM_UNIQUE_ID while refusing** (`aecp.c:271-289`). It answers ENTITY_MISBEHAVING with the `system_unique_id` in force and changes nothing.
   - Under another controller's lock it keeps NOT_IMPLEMENTED, as before this lane.
   - A SET of zero, and GET, are unchanged.
3. **Tests and plants.** There are three new `Core` tests and one new `Face` test, plus 9 new plants: 137 in total, 59 in the face section that begins `# contract 2.3 (#665)`. That matches the README's 59 at `sw/firmware/ctrl/README.md:602` and `aecp/README.md:197` (my count from the table: 59 at the head, 50 at `6d2b77bb`).
4. **Docs.** They describe exactly the behaviour above. The ledger's +64 B `rom` / +0 `sram` is reproduced independently (below).

## Findings

None of severity BLOCKER, MAJOR, MINOR or RESIDUE.

### SG1 - SUGGESTION - Tests, Docs - `sw/firmware/gtest/coverage.ratchet` - the ratchet's recorded totals lag the head

- **Evidence.** `receipts/fw_coverage_check.out` (rc 0) measures at this head:

  | File | Lines | Branches | Ratchet records |
  |---|---|---|---|
  | `aecp.c` | 417/417 | 360/360 | 358/358 and 308/308 |
  | `aecp_commands.c` | 450/450 | 374/374 | 427 and 364 |
  | `aecp_face.c` | 172 | 152 | 166 and 144 |
  | `mbx.c` | 302 | 150 | 300 and 144 |
  | `aecp_mbx.c` | 104 lines | | 101 |
  | `ctrl_app_aecp.c` | 164 | 124 | 161 and 122 |

- `compare()` (`fw_coverage.py:391-405`) compares fractions, so the gate is correct and 100 % holds. But the file no longer records what the merge head measures.
- **Suggested outcome.** Run `fw_coverage.py --write` at the final head, so that the ratchet's totals describe the code that merges. This is optional; no claim depends on the totals.

### SG2 - SUGGESTION - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 (`:155-191`) - the tile counts depend on the runtime, and the ledger does not identify it

- **Evidence.** I linked the four points at `6d2b77bb` and at this head with one runtime: the host's bare-metal newlib-nano `libc_nano.a` and `libgcc.a` for rv32i/ilp32 (`receipts/image_points_delta.txt`, `receipts/images/*`, `scripts/image_points.sh`). The delta is exactly +64 B `rom` and +0 B `sram` at all four points. That confirms the ledger's sentence at `:177` and the author's `linked-images.txt`.
  - The `sram` figures match the ledger exactly: 46,256, 57,648, 86,832 and 112,992.
  - With this runtime, `rom` is 1,776 B larger at every point. So the shipping point plans 37.5, not 37.0.
  - The 8x8 two-interface point plans 58.0, and the planner refuses it even with the `8x8-two-interfaces` override. This incidentally confirms that the override refuses past 57.5.
  - The ledger says "one runtime for both" and the PR body says the runtime is built with `-fno-stack-protector`. Neither records the archives' hashes, which `ctrl_srp_image.py` already reports.
- **Suggested outcome.** Name the runtime archives' sha256 beside the ledger table, so that the 24 B margin before 37.5 and the 1,032 B before 58.0 can be reproduced. The runtime itself is S3's work under ruling 6412739248 item 2, so this is optional here.

### SG3 - SUGGESTION - Docs - `docs/design/MAILBOX_SPLIT.md:1304` - a review comment cited as authority

This repeats R701-5 S5, unchanged and outside this delta. The text cites outcome (a) by PR comment 6421229873. Citing ruling 6425357821 alone, which adopted it, would keep a review report out of the authoritative chain.

### SG4 - SUGGESTION - Robustness - `aecp_commands.c` `aecp_keep`, `aecp.c:103-112` `refuse()` - carried unchanged

These are R701-5 S1/S2 and R702-5 S1, carried unchanged. `aecp_keep` silently saturates at `AECP_KEPT` and trusts `n <= 8`. `refuse()` re-runs the held command with the held response as its input, which is correct only while every `AECP_WAITS` handler echoes its command layout and reaches the lock check first. None of this is reachable with the shipped models.

## Prior findings at this head

I read these after my own pass over the delta and my probes.

| Prior item | Status at `424b1489` | Evidence |
|---|---|---|
| R702-5 F1 (MINOR: ENTITY_AVAILABLE and a refused LOCK_ENTITY report the lock released before LOCK_HELD 0 is acknowledged) | **Resolved**, first option | Code as in item 1 above. R702-5's `probe_release_reads.cpp` (sha256 `00c00f26…`, equal to the published copy) rerun **unchanged** by me in all four arms (`receipts/probe2/baseline-*.log`): `pending-release ENTITY_AVAILABLE status=0 flags=2 lock_owner=1020304050607081`, `pending-release foreign LOCK_ENTITY status=3 locked_id=1020304050607081`, `after-applied ENTITY_AVAILABLE flags=0 lock_owner=0`. Permanent test `Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease` (`test_aecp.cpp:872`), five plants, all caught by me (below). |
| R702-5 F2 (MINOR: the final response's egress interface is untested) | **Resolved** | `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn` (`test_aecp.cpp:950`) asks on interface 1 while interface 0 is answered, and checks the `Send` port's egress for the IN_PROGRESS, the SUCCESS and the failure. Plant `waiting-response-leaves-on-the-last-interface` is caught (`receipts/probe1/plant-waiting-response-leaves-on-the-last-interface.log`). R702-5's `probe_held_interface.cpp` (`28942187…`) rerun unchanged: passes at two interfaces (`egress=1`); at one interface it skips itself by design, which the harness tallies as a failure, as the author states. |
| R702-5 F3 (MINOR: the 120 ms IN_PROGRESS cadence has no failing test) | **Resolved** | `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` (`test_aecp.cpp:2476`) measures on the model's millisecond clock and never reads `AECP_WAIT_MS`. It adds `aecp_service_limit_ns` (10 ms, `aecp_latency_policy.hpp:4`) and checks 120 ms from the IN_PROGRESS and 240 ms from the command. The author's plants at 130 and 115 ms are caught, and so is my own at **111 ms** (`receipts/probe1/plant-review-wait-bound-111.log`). The test is tight to within about 1 ms of the cadence. |
| RES1 / R701-5 W1 (reviewer ID in a source comment) | **Resolved** | `test_aecp.cpp:720-721` now reads "(#665; IEEE 1722.1-2021 7.4.15.1)". There are no reviewer, executor, lane, round or comment IDs in any added source line of the delta (my scan of the `+` lines under `sw/`). |
| RES2 / R701-5 W2 ("fails, changing nothing") | **Resolved** | `ARCHITECTURE_HW_SW_SPLIT.md:111-112` and `aecp_face.h:16-17` now state that the core keeps the values in force and that the datapath ends there once it takes the republished block. The link points at the in-tree `MAILBOX_SPLIT.md#the-firmwares-writer`, which `check_doc_paths.py` resolves. |
| RES3 / R701-5 W3 (the 224 B `sram` list) | **Resolved** | `SPLIT_CONTROL_MEMORY.md:176` lists the held response with its interface, length and requester, the four recorded values, the noted change, the wait's deadline and its three flags. |
| R701-5 F1 (MINOR: MVU SET_SYSTEM_UNIQUE_ID answered NOT_IMPLEMENTED while refusing) | **Resolved**, option (a), as assigned | `aecp.c:273-280`. `Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs` covers the pending wait and the failed wait, then under a foreign lock, applied or not. Plant `system-id-refusal-not-implemented` is caught. My own plants `review-mvu-set-taken-while-refusing` and `review-mvu-refusal-reports-request` are caught too. R701-5's `probe_wait_refusals.cpp` (hash equal to the published copy) passes in the author's rerun (`status=10` twice, `author-r6/receipts/probes/r701-5-probe-wait-refusals-app-if2.log`). |
| R702-5 S2 / R701-5 S3 (stray blank line) | **Resolved** | Removed between `aecp_note` and `aecp_stream_read` (`aecp_commands.c:61-63`). |
| R702-5 S4 (the shipping point's margin) | **Carried, informational** | Now 24 B before 37.5 with the author's runtime; see SG2. |
| R702-5 S3 (IDs in the `Ledgered` reason string) | Carried, outside the delta | - |
| Rounds 3 and 4 MAJORs (R702-4 F1/F2, R701-4 F1/F2) | Stay resolved | The delta strengthens R702-4 F2's area: the expiry is still notified once and only after LOCK_HELD is acknowledged. `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease` and `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken` pass in my arms. |

## My probes and gates at this head

The scripts are in `scripts/`. Every probe ran on copies under the unpublished `scratch/`, and the clone was never written.

| What | Result | Receipt |
|---|---|---|
| AECP arms, `core` and `app`, 1 and 2 interfaces, the head's whole `test_aecp.cpp` plus my three probe tests (`scripts/probe_tests.cpp`, driver `scripts/r702_6_probe.py`) | core 59/59 at each width, app 104/104 at each width (the author's 101 plus my 3). The four new tests pass in every arm they compile in; the `Face` test is in the app arm only | `receipts/probe1/baseline-*.log`, `receipts/probe1_results.json`, `receipts/probe1.out` |
| P1: the owner's unlock waits for the face across the lock's 60 s deadline, then is taken | exactly one unlock notification, released with no owner, no second expiry notification, ENTITY_AVAILABLE unlocked | same |
| P2: as P1, but the wait fails | ENTITY_MISBEHAVING for the unlock. The lock then expires and holds by its owner (ENTITY_AVAILABLE flags 2 with the owner; a foreign LOCK_ENTITY refused ENTITY_LOCKED naming it), then one expiry notification once applied, the owner dropped, and another controller takes the lock | same |
| P3: GET_SYSTEM_UNIQUE_ID during a wait, and a SET of the value already in force | GET SUCCESS with the value in force; the same-value SET refused ENTITY_MISBEHAVING (consistent with "every change is refused") | same |
| The round's 9 new plants (the author's table, run individually against their named checks, app arm at 2 interfaces) | 9/9 caught | `receipts/probe1/plant-*.log` |
| 6 plants of my own: the old refusal-status predicate restored at `aecp.c:372`; the MVU refusing branch disabled; ENTITY_AVAILABLE's or LOCK_ENTITY's owner zeroed while released; the MVU refusal storing the request; `AECP_WAIT_MS` 111 | 6/6 caught | `receipts/probe1/plant-review-*.log` |
| R702-5 probes rerun unchanged (concatenated copy in `receipts/probe2/`) | release reads pass in all four arms; held interface passes at 2 interfaces and skips by design at 1 | `receipts/probe2/*`, `receipts/r702-5-probe-hashes.txt`, `receipts/probe2_r5probes.out` |
| `fw_coverage.py --check --jobs 16` | rc 0, 31 files at 100 %: `aecp.c` 417/417 and 360/360, `aecp_commands.c` 450/450 and 374/374, with no new exclusion | `receipts/fw_coverage_check.out`, `.rc` |
| Linked split images, the four points, `6d2b77bb` against the head, one shared host runtime | +64 B `rom`, +0 `sram` at every point (see SG2 for the absolute figures) | `receipts/image_points_delta.txt`, `receipts/images/` |
| `check_cpp_idiom.py`, `check_py_idiom.py`, `check_doc_paths.py`, `check_doc_style.py`, `docs_check.py` | 5/5 rc 0 (1,062 cited paths resolve; 0 findings across 210 md files) | `receipts/gate_*.out`, `.rc` |
| Evidence packet `17fa488f` `review-evidence/665s1-r1` against `MANIFEST.json` | 1,071 entries, 0 mismatched or missing, 0 unlisted; `author-r6/**` 186 entries, all matching. The packet commit is **unsigned** (verification reason `unsigned`), so integrity rests on the manifest alone | `receipts/evidence_manifest_check.txt`, `scripts/verify_manifest.py` |
| The author's receipts at `424b1489` (spot-checked) | `aecp-mutants` 137/137 caught across four shards; four firmware self-test shards `PASS rc=0`; `linked-images.txt` matches section 5 row for row, with symbol growth `aecp_other_lock +64 … aecp_foreign_lock -48`, totalling +64 | packet `author-r6/receipts/` |
| Hosted, read-only snapshot at 2026-10-27T00:01Z | 17 jobs succeeded (among them `firmware-unit`, `firmware-aecp-mutants`, `firmware-boundary`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `full-ci-gate`). `Physical gPTP` was **skipped**. 20 were in progress and 8 queued, among them `publication-census`, the Verilator and Yosys shards, `docs-gates-0` and `elaborate-gates-1`. None had failed. This snapshot is not acceptance | `receipts/hosted-check-runs.txt` |
| Checkout integrity after the probes | HEAD and tree as above. 0 porcelain lines. Index equals the tree (1,454 entries, with modes). 0 blob hash mismatches. The five initialized submodules are at their gitlinks and clean; the optional `external` is not initialized | `receipts/checkout-integrity.txt` |

## Lens results at this head

- `[R702] PASS Conformance — aecp.c:271-289,372,487-506; aecp_commands.c:16-28,606-609; test_aecp.cpp:872,950,2476 (the four new tests)`. I checked against ruling 6421238472 items 1, 3 and 4, Milan v1.2 5.4.2.2 (60 s release, notification once acknowledged), IEEE 1722.1-2021 7.4.2/7.4.3 field offsets (`locked_id` at +42, `lock_controller` at +50, both read in the tests and probes), and 9.3.2.6 as `FR_NFR.md:363` reads it (240 ms and the 120 ms IN_PROGRESS cadence, measured with the service bound). Only acknowledged lock state is visible, and every refusal is the single status the docs state.
- `[R702] PASS RTL — aecp_face.c:41 (LOCK_HELD from core->locked); the firmware-to-datapath applied contract in MAILBOX_SPLIT.md "The firmware's writer"; git diff 6d2b77bb..424b1489 -- hdl tb syn sw/mailbox sw/litex (empty)`. I checked that the release reaches the datapath at expiry while the core holds the lock until the acknowledgement, so no F value is promised before its commit. No HDL, generated or bench file changed, so the prior RTL examination of those artifacts carries.
- `[R702] PASS Robustness — aecp.c:347,575-617 with probes P1-P3`. I covered the lock expiring under a waiting owner's unlock, both when the wait succeeds and when it fails; a never-acknowledging face, where the lock holds and changes are refused, as ruled for an unacknowledged face; a same-value SET while waiting; a foreign controller during the held release; and repeated drains, where there is no duplicate notification.
- `[R702] PASS Tests — test_aecp.cpp:866-975, :2471-2497; aecp_mutants.py:679-727`. The 9 new plants and my own 6 independent plants each fail a named test. The new tests can fail for the defect they claim (my 111 ms plant shows the cadence test's resolution). Coverage holds at 100 % with no new exclusion. The existing regressions stay green in all four arms.
- `[R702] PASS Docs — ARCHITECTURE_HW_SW_SPLIT.md:58,111-112; MAILBOX_SPLIT.md:1267-1294 and the verification row; SPLIT_CONTROL_MEMORY.md:155-191; aecp/README.md:56-83,194-233; ctrl/README.md:602; aecp.h:101-113; aecp_face.h:13-23`. Each statement matches the code and the receipts above. The figures are reproduced as deltas. There is no comment-rule residue in the delta. The PR body states the three fixtures that differ by design, the limits and the runtime.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp.c`, `aecp_commands.c` lock and MVU paths; the four new tests; `FR_NFR.md:363`; rulings 6421238472 and 6426858104 | R702-6 | `424b1489ccd8062180f90158556d343589b9e1e5` |
| RTL | CLEAN | `aecp_face.c:41` and the `applied` contract; the empty `hdl/ tb/ syn/ sw/mailbox/ sw/litex/` delta since `6d2b77bb` | R702-6 | `424b1489ccd8062180f90158556d343589b9e1e5` |
| Robustness | CLEAN | probes P1-P3; `aecp_poll` wait and expiry ordering; the never-acknowledged face | R702-6 | `424b1489ccd8062180f90158556d343589b9e1e5` |
| Tests | CLEAN | 4 new tests, 9 new plants and 6 independent plants, the coverage gate, the four arms | R702-6 | `424b1489ccd8062180f90158556d343589b9e1e5` |
| Docs | CLEAN | the doc and header sites listed above; the PR body; the docs and idiom gates | R702-6 | `424b1489ccd8062180f90158556d343589b9e1e5` |

## Real limits

- **No manager source bank** exists at this exact head, and none is claimed or inferred. Source-head execution evidence beyond my focused runs is the author's published receipts. The current-dev merge candidate (source base `e76a755a`; live `dev` `76de691e5625cc4ea2f9a19def9e07c1183a14ee`) is not validated by this review.
- **Not run by me:**
  - the whole firmware self-test;
  - the full `aecp_mutants.py` campaign (I ran only the 9 new plants and 6 of my own);
  - `test_builder.py`, whose gate 11 the author also could not run without a local Arty build report;
  - `behave`;
  - the Verilator sweep;
  - the census;
  - `gen_mailbox.py`;
  - Yosys and xvlog;
  - the out-of-context run;
  - the all-fabric export digest.

  None of their inputs changed in this delta, and I used no Verilator.
- **Absolute image figures are runtime-dependent** (SG2). I reproduced the deltas, not the author's absolute `rom` bytes.
- **Not checked against the clause text:** the MVU status set. I could not check whether Milan v1.2 permits ENTITY_MISBEHAVING (10) as an MVU status, because the specification text is not in the repository. The behaviour is the manager's assigned option (a) of R701-5 F1, and the docs state it.
- **Integrity:** the evidence packet commit is unsigned, so its integrity is the manifest's hashes alone.
- **Hardware:** physical calibration was NOT RUN. The skipped field and physical contexts are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head. At my snapshot, `publication-census`, the Verilator and Yosys shards and two gate jobs were still running or queued.
- The current-dev merge-candidate builder and native banks, with their receipts linked on the PR.
- The second independent review (R701-6) and the full completion bar.
- An explicit maintainer authorization to merge.
- Optionally, SG1-SG4 for the residue and suggestion checklist.

R702-6 FINISHED
