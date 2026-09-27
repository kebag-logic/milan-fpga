[R349] POSITIVE - exact head ff75a70807c151517860c73a06d7ea36e2a46008

Round R349-2 is the external independent delta review of PR #588 for issue #397. The head is
`ff75a70807c151517860c73a06d7ea36e2a46008` with tree `aa2fd7c8fe3499303efa316650e73b45b341dcf5`:
one commit on the round-1 head `7f997b60d5a74d46beca5c263d27496ccce0ae4f`. The source base is
`ac18b50968b12efe4d15c0a06301264b35656b31`. I applied all five lenses to `7f997b60..ff75a708`
and re-read the unchanged surroundings the delta depends on.

## Summary

Every round-1 finding on this PR is closed at this head, from this reviewer (F1-F5, S1) and from
the internal reviewer (F1-F4, S1, S2). No BLOCKER, MAJOR or MINOR is open, so the verdict is
POSITIVE. There are three new SUGGESTIONs. The main results:

- **Reproducibility.** I built both shapes fresh at the head and ran all eight named plans. All
  eight reproduce the ten published receipts **bit-for-bit**: log SHA-256, rows, heartbeat,
  liveness and findings.
- **Documentation tables.** A reviewer-owned parser that uses no harness code re-derived every
  numeric cell of the duty, opportunity and schedule tables: 318 cells, 0 mismatches.
- **Unchanged probes.**
  - P1 and P2 reproduce byte-for-byte.
  - P3 on the head binary reproduces every pre-existing marker at the same cycle, and the
    liveness lapse (backing 1 through command 8, 0 from command 9).
  - The internal reviewer's three-command probe (PD) again sees the backend clear backing at
    2,893.00065 ms, 1,999.0381 ms after the only kick.
- **Mutation suites.** Both unchanged suites now fail the self-test for every mutant: 11/11 and
  15/15.
- **Gates.** The three builder gates that failed at round 1 pass, and so does every other listed
  gate.

## Reconstruction

Read in order:

- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- Issue #397: the body and comments 5854692469, 5854787465, 5855879265 (round-2 assignment and
  decision: queued console input is in scope for the product rule; the lane stays
  measurement-only) and 5856728560 (REVIEW READY). Issue #590 (the firmware defect and its
  acceptance).
- The PR #588 body and the manager comment 5855512699 (builder-bank failure).
- SAVED_STATE_FASTCONNECT.md section 9.4 and `hdl/milan/KL_nvm_backend.sv:625-690` (liveness
  arming and expiry).
- `milan_baremetal.c` (heartbeat call sites, `load_aem_image`, boot order).
- `git diff 7f997b60..ff75a708` (12 files) and the commit (one line, no body or trailers).
- The public evidence branch `397-review-evidence` at `bcc86c8dc`, `review-evidence/397-r1/author-r2/`.

I read the prior public review findings, R349-1 (my own) and R348-1 (comment 5855875344), only
after my independent pass and findings were settled. No private material was read.

## Round-1 findings: disposition at this head

| ID | Round-1 severity | Status | Evidence at this head |
| --- | --- | --- | --- |
| R349-1 F1 = R348-1 F1 | MAJOR | **CLOSED** | See the itemized evidence below. |
| R349-1 F2 = R348-1 F2 | MINOR | **CLOSED** | `run.py:342-372` regrades three fixed traces in `oracle.json` and requires exact `rows`, `budget_findings`, `heartbeat` and `liveness`. Those traces equal the published receipts `round2-1x1-all`, `round2-8x8-all` and `round2-1x1-uart-paced`. The unchanged round-1 suite: 11/11 mutants fail the self-test, control passes (`receipts/mutation_round1_suite.txt`). The internal reviewer's unchanged suite: 15/15 fail, including `hb-marker-bitmask`, which fails the added combined-word control (`receipts/mutation_r348_suite.txt`). run.py now emits the complete receipt: same key set as published (`receipts/receipt_keys.txt`), and README:86 documents this. |
| R349-1 F3 = R348-1 F3 | MINOR | **CLOSED** | `flash.hpp:101-104` `aem_read()` matches the first 3-byte-address read at `0x400000`. `run.py:289-291` bounds AEM from that read to entity enable. That is the source address `load_aem_image` dereferences (`milan_baremetal.c:1406-1418`). 1x1 `all` gives 55.77034 ms, 2.60082 ms after walk end; my round-1 walk-end-to-enable figure was 58.37116 ms = 2.60082 + 55.77034. The other reviewer's read-completion observer gives 55.76477 ms (findings :47-48). The "no narrower marker" claim is gone. |
| R349-1 F4 (R348-1 S1) | MINOR | **CLOSED** | Boot is compared with 20,000 ms (Milan v1.2 5.6.2/5.6.3, `valid_time = 10` x 2 s) per the round-2 decision: `run.py:290`, findings :102-106, README. The BIOS CRC, delay and memory-test exclusions are stated, and no physical boot claim is made. |
| R349-1 F5 | MINOR | **CLOSED** | The erase and page waits are separate (`sim_main.cpp:20-22`, `run.py:426-427, 466-468`). `validate_waits` (`run.py:51-56`) accepts 0..3,000,000 / 0..5,000 us. The datasheet corner executed in both shapes: 3 s erase with 12 strobes at 250.00068 ms maximum spacing; commits 3,339.59461 / 4,307.68299 ms (`receipts/device_max_rows.txt`). Out-of-range values refuse before a build directory exists (`receipts/wait_refusals.txt`: 5 cases, rc 1, directory absent). Worst supported plan: 12.5 s WIP + ~5.5 s simulated work < 30 s guard (`sim_main.cpp:225`). |
| R349-1 S1 | SUGGESTION | **TAKEN** | Findings :279-285 and README:148 state that the substitution is optimistic, with the per-boundary costs. |
| R348-1 F4 | MINOR | **CLOSED** | `flash_test.cpp:67-75` sets WEL after completion, then programs at an earlier busy cycle. Deleting `cycle < busy_until_` from `flash.hpp:72` makes exactly "program while busy refused" fail, rc 1 (`receipts/flash_busy_mutant.txt`). |
| R348-1 S2 | SUGGESTION | **TAKEN (partly)** | README:31 notes that ignored generated ROMs are written into the checkout. The bytecode caches I saw came from the gate scripts, not the builder. |
| Builder bank (manager, 5855512699) | gate failure | **CLOSED** | `docs/findings/397_SERVICE_BUDGET_{1X1,8X8}.json` are removed. `pp_srcs --check`, `check_baremetal_only --check` and `check_entity_shape --self-test` all return rc 0 (`receipts/gate_*.txt`). The ten receipts are published at `bcc86c8dc:review-evidence/397-r1/author-r2/receipts/`, and their SHA-256 values equal the findings table at :362-373 (10/10; `receipts/tool_and_custody.txt`). The two round-1 receipts hash to the original `7f997b60` blobs. |

Evidence for F1 = R348-1 F1 (MAJOR, CLOSED), item by item:

- **Tick opportunities.** `observe.vlt` and `build.py:104-126` passively read the single CPU
  commit port.
  - Commit-valid means ready, not cancelled and committed (netlist line 18183; netlist SHA-256
    `c208df0b...` is unchanged).
  - The entry PC comes from the linked ELF.
  - The firmware has 5 source call sites and 5 non-inlined `jal` sites to
    `nvm_heartbeat_tick`.
  - Every heartbeat strobe in all eight receipts follows a tick entry.
- **Per-duty stretch and bounds.**
  - `run.py:75-133` reconstructs the longest no-tick stretch per duty.
  - The conditional period is 250 ms + stretch + TX, compared with 500 ms and with
    2,000 ms.
  - Findings :136-172 give every duty; all 56 opportunity rows re-derived independently.
- **Schedule dependence.** Findings :174-177 and :207-216 state which intervals each gap spans,
  and that queued input suppresses the idle hook.
- **Heartbeat row.** The "Maximum heartbeat gap" duty row is gone. It survives only as a
  plan-qualified schedule row with endpoints, a right-censoring flag, both margins and the
  printed backing samples (:190-199).
- **Named modes.** `uart-paced` and `queued-input` are harness modes (`run.py:20, 41-48`,
  README:43-60).
- **Liveness.** Queued input lapses liveness in both shapes (:7, :194, :198, :218-222), owned
  by #590. P3 is stated.
- **Device-length WIP.** Covered by P2, PC and the device-wait plan (:236, :239, :256-277).
- **Liveness arming.** "Unarmed prefix" is correct: `alive_r` resets to 0 and is armed only by
  a kick (`KL_nvm_backend.sv:668-679`).
- Every item in both reviewers' required outcomes is present.

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### S2 - SUGGESTION - Tests - the self-test does not exercise a zero backing sample or the queued-plan composition

Artifacts: `tb/verilator/fw_service_budget/run.py:136-150` (`liveness_report`), `:41-48`
(`command_plan`), `:338` (`heartbeat_500ms_met`), `oracle.json`.

Evidence: I ran 19 reviewer mutants of the new round-2 analysis code
(`scripts/mutate_r2.py`, `receipts/mutation_r2_newcode.txt`). 16 fail the self-test. Three
pass:

- `backed = 1 if match` (a parser that never reports a lapse). All three oracle traces carry only
  backing 1.
- The 1x1 queued plan cut from 12 to 11 status commands. The plan is used both to drive the run
  and to take its census, so it is self-consistent.
- The unused `heartbeat_500ms_met` threshold.

The published queued receipts and my independent parser both show the zeros (1x1 command 9
onward; 8x8 command 2 onward), so no current evidence is affected. The schedule row still
exposes a lapse by its > 2,000 ms gap.

Impact: a later edit to the liveness parser or the named plan could hide a lapse, or drift from
P3, and still pass the portable gate. #590's acceptance ("keeps `backed=1`") is measured with
this harness, but #590 also requires its own failing control.

Suggested outcome: add a fixed queued-input trace, or a synthetic zero-sample control, to the
oracle. Pin the queued plan text (133 bytes at 1x1). Optionally drop the unused flag.

### S3 - SUGGESTION - Docs - the receipt table carries a lane-state sentence and no direct locator

Artifact: `docs/findings/397_SERVICE_BUDGET.md:356-360`.

Evidence: "The packet is prepared for the manager to publish; this lane has no push authority"
describes the lane at handoff. It stops being true once the packet is published
(`397-review-evidence` at `bcc86c8dc`, `review-evidence/397-r1/author-r2/receipts/`). The
hashes bind the content, and :225-226 links the branch.

Suggested outcome: in a later docs touch, name the branch path for the receipts and drop the
lane-state sentence.

### S4 - SUGGESTION - Docs, Conformance - the page summary names only the queued-input lapse

Artifact: `docs/findings/397_SERVICE_BUDGET.md:7-9` (against :168-169, :196-199).

Evidence: the round-1 page opened by stating that 8x8 misses the 500 ms heartbeat period. The
round-2 opening mentions only the queued-input liveness lapse. The tables still show that 8x8
misses the section 9.4 500 ms period without queued input:

- the `uart-paced` schedule gap is 991.91598 ms;
- the single device-max commit plan gap is 588.61054 ms;
- a single NVM status command has an 800.91654 ms no-tick stretch.

#590's acceptance item 2 owns the repair, so nothing is unowned.

Suggested outcome: a one-line summary that 8x8 misses the 500 ms period under paced input and in
a device-max commit, owned by #590.

## Other checks (delta)

- **Protected inputs.** `git diff --stat 7f997b60..HEAD` and `ac18b509..HEAD` over
  `sw/firmware/milan_baremetal` and `tb/verilator/nvm_capture_cpu` are empty. The firmware
  SHA-256 `0bf43cd4...` matches the page. `check_nvm_capture.py` returns rc 0 (7 controls). The
  submodule gitlinks are unchanged.
- **Receipt custody.** Six of the eight published round-2 receipts carry `media` without the
  `shape` key that head `fixtures()` now adds. They were regraded from earlier native runs, as
  :346 says. My fresh head runs add the key, and every log hash and analysis field still matches,
  so this is provenance only.
- **Paced mode.**
  - The frame is 8,681 system cycles, `(sys_hz + 11519) / 11520`, and README:57-58 states it.
  - P1 (8,680 cycles, unchanged round-1 driver) gives a 332.34734 ms gap. The head paced mode
    gives 332.34992 ms.
  - Both appear on the page (:193, :235).
- **Hosted status at the exact head** (`receipts/hosted_checks_exact_head.txt`). Executed and
  successful: rtl-fast, verilator-suites (5 shards), yosys-portability (4 shards),
  yosys-elaboration, elaborate, docs-check, docs-check-no-git, bdd-conformance, verilator-lint,
  wire-accountability, changes and full-ci-gate. Skipped context: Physical gPTP (nightly and
  manual). Hosted and local-replica acceptance remains the manager's.

## Clean-lens record and ledger

[R349] PASS Conformance - `docs/findings/397_SERVICE_BUDGET.md:1-397` against SAVED_STATE 9.4 (500/2,000/3,500/8,000 ms), the Milan 5.6.2/5.6.3 20 s window, issue #397 comment 5855879265 items 1-8 and #590; `run.py:229-339`; `KL_nvm_backend.sv:625-690`; `milan_baremetal.c:757-769, 1404-1455` - every assigned item is met. All 318 table cells re-derived from 8 bit-identical head reruns. P3 and PD lapses reproduced. The deadline constants match the authorities. S4 only.

[R349] PASS RTL - `observe.vlt:1-4`, `build.py:89-126`, generated `retirement.hpp` (1x1 `0x6658`, 8x8 `0x66ec`), `sim_main.cpp:17-160, 215-240`, `flash.hpp:98-106`, CPU netlist `c208df0b...` line 18183 - no product RTL changed. The commit-port read is passive and single-lane, and sampled on CPU rising edges aligned with the 100 MHz edges. The tick blocks flush at every external boundary. The AEM marker matches the firmware's memory-mapped source address. The paced handshakes gate only the harness-side valid and ready.

[R349] PASS Robustness - `run.py:51-72, 75-99, 216-339, 435-486`; `sim_main.cpp:225`; `receipts/wait_refusals.txt`, `receipts/regrade_cli.txt` - out-of-range waits refuse early. A block that straddles a boundary, an invalid tick maximum and an unordered marker all refuse. The default regrade refuses budget findings (rc 1) and the reporting-mode regrade records them (rc 0). The device corner and queued input executed in both shapes.

[R349] PASS Tests - `run.py:342-410`, `oracle.json`, `flash_test.cpp:34-81`; `receipts/mutation_round1_suite.txt` (11/11), `receipts/mutation_r348_suite.txt` (15/15), `receipts/flash_busy_mutant.txt`, `receipts/mutation_r2_newcode.txt` (16/19), `receipts/rerun_vs_published.txt` (8/8 identical), `receipts/probes_P1_P2_P3.txt`, `receipts/gates_summary.txt` (21 rc 0) - the grader mutants and the busy predicate are pinned. S2 only.

[R349] PASS Docs - `docs/findings/397_SERVICE_BUDGET.md`, `tb/verilator/fw_service_budget/README.md`, `docs/integration/BAREMETAL_FIRMWARE.md:1882-1885`, `docs/findings/README.md:11`, `docs/testing/TESTING.md:403-406`; `receipts/doc_tables_check.txt` - tables are exact and claims were checked against executed evidence. There are no stale references to the removed receipts. S3 and S4 only.

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN (S4 only) | findings page vs section 9.4, Milan 5.6.2/5.6.3, assignment 5855879265, #590; `run.py` grading; backend liveness RTL; firmware heartbeat/AEM paths; 8 reruns, P3, PD | R349-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| RTL | CLEAN | `observe.vlt`, `build.py` retirement header, `sim_main.cpp`, `flash.hpp`, CPU netlist commit port, ELF call sites | R349-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| Robustness | CLEAN | wait validation and refusals, tick-block integrity, regrade binding and refusal, device-corner and queued runs | R349-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| Tests | CLEAN (S2 only) | self-test and oracle, flash controls, 11 + 15 + 19 mutants, busy mutant, 8 bit-identical reruns, P1/P2/P3/PD, 21 gates | R349-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| Docs | CLEAN (S3, S4 only) | findings page, harness README, BAREMETAL_FIRMWARE, findings index, TESTING entry; 318-cell table check | R349-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |

Coverage is banked against this head only. Any commit that touches the harness, the findings
documents, the oracle or the firmware un-covers the affected lenses.

## Reproduction

The scripts are under `scripts/`. The round-1 scripts (`make_probe.py`, `mutate.py`,
`regrade_check.py`, `lapse_analysis.py`, `independent_intervals.py`, `env_run.sh`,
`compare_receipt.py`, `phy_timing.py`, `gates.sh`) are byte-identical to the published R349-1
copies. The internal reviewer's scripts were used unchanged from the evidence branch; their
hashes are in `receipts/tool_and_custody.txt`.

```sh
scripts/run_plans.sh <repo> <packet> <export of 7f997b60 harness> <R348-1 scripts> <R349-1 receipts>
python3 scripts/compare_runs.py <published-receipts> round2-1x1-all=<b1x1>/service-all-1-0-0.json ...
python3 scripts/independent_r2.py <8 receipts>        # then check_doc_tables.py <findings.md> <output>
python3 scripts/compare_probes.py <R349-1 receipts> <runs> <published-receipts>
python3 scripts/stream_equiv.py <R349-1 probe_queued.raw.log> <runs>/queued1x1/raw.log
python3 scripts/erase_heartbeats.py <raw.log>
python3 scripts/mutate.py <overlay-with-legacy-receipt-paths> <scratch>    # round-1 suite, unchanged
python3 <R348-1>/mutate_grader.py <overlay-copy> <out.json>                # internal reviewer suite, unchanged
python3 scripts/mutate_r2.py <repo> <scratch>
scripts/flash_busy_mutant.sh <repo> <scratch>; scripts/wait_refusals.sh <repo> <scratch>
scripts/gates_r2.sh <repo> <outdir> <pinned-markdown-venv-python>
scripts/restore_verify.sh <repo> <head> <tree>
```

## Real limits

- The scoped 5.050 simulator path in the brief does not exist on this host. The installed HDL
  simulator 5.052 was used unmodified; round-1 receipts recorded the same version. The results
  are bit-identical to the published receipts.
- The eight measurement slots ran as detached processes, polled to completion by foreground
  commands, because single runs exceed the per-command time limit. All exited rc 0
  (`receipts/runs_status_and_log_hashes.txt`). At most eight simulations ran at once.
- P3 was run on the head native binary, whose argument list changed. Its log equals the round-1
  P3 log in every pre-existing marker and in the UART text. Only the newline framing around the
  new passive lines differs.
- The internal reviewer's PC probe was not rerun (not in this round's brief); the device-wait plan
  covers the same corner.
- Pacing and queuing are simulation models. Physical calibration, hardware and the release-gates
  torture were NOT RUN. Field skips are not hardware proof.
- Not run: the local CI replica, the full parent, PP, gPTP, Yosys or builder banks, and a
  candidate merge. Only the three named builder gates ran individually.
- The product builds and gate scripts wrote ignored files into the review clone:
  `configs/generated/{ltn_rom,ucode}.hex` and three `__pycache__` directories, one inside the
  protocol-processor submodule. I removed them. `receipts/restore_verification.txt` shows:
  - HEAD, HEAD tree and index tree all equal `aa2fd7c8...`;
  - no diff-index entries;
  - an empty porcelain-with-ignored status in the parent and both checked-out submodules;
  - the gitlinks unchanged.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Hosted and local-replica acceptance at the exact head.
- The final candidate on live dev `682ecf0cb995473b72d5b4921088053ba753fc93` at the merge turn,
  and the merge authorization.
- Collect the internal reviewer's round-2 verdict. Merge still needs two independent positive
  reviews and an accepted ledger.
- Optional disposition of S2-S4.
- Carry forward #590 (queued-input and 8x8 500 ms heartbeat repair) and the open #397 hart
  decision and AX7101 torture.

R349-2 FINISHED
