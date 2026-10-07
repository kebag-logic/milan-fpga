[R528] POSITIVE - exact head 938497af1dffd8a87edebf3ab93663914bf85e5e

# R528-2: internal cleared-context re-review of PR #687 (issue #665, lane F2)

- Head: `938497af1dffd8a87edebf3ab93663914bf85e5e`, tree `b40dfc375f080a96eb4a927e023fa6b916cbe7c1`.
  The PR head on GitHub matches (`receipts/pr687.json`).
- Delta reviewed: `1a5d70fa..938497af`, two one-line commits (`11e195be`, `938497af`), 10 files.
  The delta adds no amend or rebase, and changes no `hdl/`, `sw/litex/`, `configs/`, `sw/builder/`,
  `sw/mailbox/` or submodule file.
- Whole-PR range `021b9c1f..938497af` was re-read. The FC round-2 commits (`021b9c1f..db9aa8c9`)
  belong to PR #685 and its reviews, and are not re-reviewed here.
- Authorities read:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - #665: the body, the F2 assignment 6026720272, the FC resume 6026839422, the round-2
    assignment 6029239721 and REVIEW READY 6029680871.
  - #686: the body and comment 6029233665.
  - IEEE Std 1722-2016 Annex B, printed pages 159-161: Table B.7 with notes a-d, Table B.8,
    B.3.4.1/.2, B.3.5.1-.9 and B.3.6.1-.4.
  - REGISTER_MAP 0x800 window, `milan_datapath.sv:1999-2002` and `KL_pp_maap_shim.sv:76-77`.
- Author packet `review-evidence/665f2-r1/author-r2/` on `665f2-review-evidence`
  (`9776d389`). HANDOFF.md and PR-BODY.md hash to the values in REVIEW READY
  (`receipts/author_r2_sha256.txt`).
- Order of work: my own pass over the delta came first. Only after it did I read the prior
  findings (my R528-1 report and R529-1, PR comment 6028867882).
  - The PR comment list also shows a later R529-2 report at this head. I saw only its
    one-line preview in a comment listing and did not read it.
  - No private author material, lane scratchpad or management path was read.

## Verdict basis

Every prior finding is fixed at this head: R529-1-F1 (MAJOR), R529-1-F2, and R528-1-F1 to F6.
My own defect-sensitive controls show each fix at its root. The optional R528-1-S1 is also
addressed. The whole PR, re-read across all five lenses, has no open BLOCKER, MAJOR or MINOR.
One SUGGESTION and one RESIDUE are recorded. Neither affects the verdict or lens coverage.

## Prior findings: resolution at this head

| Finding | State | Root check (receipt) |
|---|---|---|
| R529-1-F1 MAJOR: MAAP RX interrupt not enabled | RESOLVED | `ctrl_app.c:55-58` writes IRQ_ENABLE = RX(ADP\|MAAP) \| EVT before FILTER_EN, the same order as `ctrl_loop_open`. `test_maap_mbx.cpp:273` asserts that exact mask, enters the real `ctrl_loop_step` -> `mbx_hal_wait` path, injects an accepted MAAP record while idle, requires the IRQ line to rise, then requires the conflict retry to commit within 10 ms of RX_HEAD. It does this per interface (4,700 ns at each, `arms.log`). The repository control `maap-app-missing-rx-interrupt` is caught by its named check in `maap` and in `maap_if2` (`repomut.log`). Four reviewer spellings (MAAP bit dropped, MAAP-only, event bit dropped, enable write removed) are each caught in both arms by `AppWaitWakesForMaapWithinBudget` (`rmut.log`). |
| R529-1-F2 + R528-1-F2: differential did not grade probe timing | RESOLVED | `test_maap_differential.cpp:131-187` grades observed core intervals with the strict predicate 500 < T < 600 (B.3.4.2). It checks the parent at 500..627 ms (both bounds reached over 1,024 phases) and 4 core PROBEs against 3 delayed parent PROBEs. The differential passes 12/12 at head, and 16/16 author controls are caught, including the 1 ms, 500 ms and 600 ms core controls by `ProbeTimingAndParentDelta` (`diffself.log.gz`). My own plants are caught: a 1 ms base, draws reaching 600 and 500, the announce interval used for probes, and 2 retransmissions (`diffr.log.gz`). README:166-173 lists the six deltas of #686: four body items and the count/first-probe comment 6029233665 (`issue686.json`). |
| R528-1-F1: Begin! range lost while not operational | RESOLVED | `maap.c:185` stores the accepted range, `maap.c:230-231` reserves it at the next PortOperational!, and `maap.c:105` consumes it. This matches Table B.7 note a ("supplied with the Begin! or PortOperational! event ... generate_address will not be called"). `test_maap.cpp:311` pins it. `maap-begin-down-forgets-range` (repo), `r2-up-ignores-saved-range` and `r2-up-saved-range-no-send` are caught (`repomut.log`, `rmut.log`). |
| R528-1-F3: Restart! base and octet priority unpinned | RESOLVED | `test_maap.cpp:179` varies each octet alone with all others tied, including the first, both ways. `test_maap.cpp:195` requires a new base and a PROBE for it. My round-1 escapes (`r-reverse-five-octets`, `r-compare-mac-lsb-only`, `r-restart-reuses-range`) are now caught, as are `r2-first-octet-ignored`, `r2-last-octet-ignored` and `r2-forward-octet-order-v2` (`rmut.log`, `rmut2.log`). |
| R528-1-F4: CSR model ignored A_STRM_SEL[8]; order unpinned | RESOLVED | `test_maap.cpp:381` drops listener-direction writes to 0x81C/0x820. `test_maap.cpp:423` walks the whole trace and requires 18 destination words before either enable, with both enables as the last two writes. `r-csr-select-listener` and `r-csr-enable-before-programming` are now caught, plus `r2-csr-crf-enable-before-crf-address`, `r2-csr-aaf-enable-before-window` and `r2-csr-selection-not-restored-v2`. |
| R528-1-F5: interface-1 poll untested | RESOLVED | `test_maap_mbx.cpp:324` stalls interface 1's output for 5 ms. It requires one pass of at most `MAAP_MBX_PASS_MAX` accesses to drain it, the DEFEND to be committed on interface 1, and the time to fall within 10 ms of the original RX_HEAD (5,004,400 ns). `r-poll-first-interface-only` is caught in `maap_if2`. |
| R528-1-F6: talker-gate dependency unrecorded | RESOLVED | `maap/README.md:101-109` and the PR body record that clearing `MAAP_CTRL[0]` disables `KL_maap`, the shim cannot answer ALLOC_DA ok, and `talker_active` never asserts. They name both remedies and the #664 decision-3 default-flip condition. Re-read against `milan_datapath.sv:1999-2002` (`aaf_gate`) and `KL_pp_maap_shim.sv:76-77`. |
| R528-1-S1 (optional) | ADDRESSED | Four generic predicate defects (`maap_mutants.py:63-76`) are each caught by their named check (`repomut.log`). README:143-145 and the PR body state the RV32 `-DNDEBUG`-only limit. |

## Findings at this head

### R528-2-S1 SUGGESTION - Tests

- Where: `sw/firmware/ctrl/maap/maap.h:77-80`, `maap/README.md:31`, `maap.c:105`; test
  `test_maap.cpp:311-328`.
- Evidence: the header promises "The preference is consumed by that reserve". A planted defect
  that never clears `m->preferred` (`r2-saved-range-never-consumed`) passes both the `maap` and
  `maap_if2` arms (`rmut.log`). The only observable difference comes when a link drops and
  returns after a Begin! range has been used: the defect re-probes the old supplied range, while
  the head draws a new one.
- Both behaviours are permitted by Table B.7 note a, so this is not a conformance defect. The
  companion plant `r2-saved-range-reused-on-conflict` is equivalent at head, because the
  preference is already zero when Restart! runs.
- Suggested outcome: either pin the link-bounce case (Begin! range, PortOperational! up, down,
  up: the base is drawn), or drop the "consumed" wording from the header.

### R528-2-R1 RESIDUE - Docs

- Where: `sw/firmware/ctrl/README.md:25`.
- The contents line still says "The seven arms". F2 added `maap`, `maap_if2` and `maap_debug`
  rows to the arm table at lines 53-63, so it now lists ten arms plus the optional `lwsrp`.
- Exact fix: replace "The seven arms" with "The ten arms (and the optional `lwsrp` arm)".
- This is wording only. It changes no measurement, test, code or claim.

## Lens evidence

| Lens | Result | Artifact and what was checked at this head |
|---|---|---|
| Conformance | PASS | `maap.c:102-111,178-200,222-241` against Table B.7. Begin! defers until the port is operational, then the supplied range is used without generate_address (note a). PortOperational! in PROBE/DEFEND restarts with generate_address. probeTimer! sends PROBE, decrements, and probeCount! sends ANNOUNCE in the same action, so there are 4 PROBEs. B.3.4.2 strict draws are 511..589 ms (observed bounds in the differential). B.3.6.4 reverse-octet priority is checked per octet. Unchanged clauses: R528-1 cell-by-cell result at `1a5d70fa`; `maap.c` changed only at lines 105, 185 and 230-234. |
| RTL | PASS | Interface contract: `ctrl_app.c:55-58` against `ctrl_loop.c:59-78` and `mbx_contract.h:117-129`. The mask matches the RX/EVT fields, the write precedes FILTER_EN, and ERR stays disabled as in F0. `git diff --stat 021b9c1f..HEAD -- sw/litex configs sw/builder` and `1a5d70fa..HEAD -- hdl sw/mailbox protocol-processor gptp-processor` are empty. The talker-gate dependency was re-read against `milan_datapath.sv:1999-2002` and `KL_pp_maap_shim.sv:76-77`. CSR offsets are unchanged since R528-1. |
| Robustness | PASS | `maap.c` preference lifecycle. A non-zero preference exists only in INITIAL while not operational (it is cleared by the operational Begin! path and by every reserve). So the reserve at `maap.c:231` never runs with a live timer or queued output. Begin! with an invalid range after a valid one is refused and keeps the stored range (`test_maap.cpp:316`). Release followed by Begin!(0) overwrites the range. Stall/drain at interface 1 is within budget. Wake at both interfaces. Queue, reentry, stale-tag and malformed-input paths are unchanged since R528-1. |
| Tests | PASS (S1 optional) | Positive gate `test_ctrl_firmware.py --require-rv32` rc 0, every arm (`arms.log`): maap 36 + 12, maap_if2 13, maap_debug 1. With the 12 differential cases that makes 74, matching the PR body. `fw_coverage.py --check` passes for 17 files: maap.c 209/209 and 140/140, ctrl_app.c 100 % after its pre-existing exclusion, no exclusion added in the delta (`coverage.log`). 12/12 new repository controls are caught by their named check and words (`repomut.log`). Of 22 reviewer plants, 18 are caught. Two first spellings failed to build and are not counted; their re-spelled versions are among the 18. One escape is S1, and one plant is equivalent. Differential: 16/16 author and 5/5 reviewer controls caught. |
| Docs | PASS (R1 residue) | `maap/README.md` (whole page), PR body, `ctrl/README.md`, `MAILBOX_SPLIT.md:420-423`. The #686 list matches the issue. The count claims (192 defects, 16 controls, 74 cases, 209/140, 4,700 ns, 5,004,400 ns) match my runs. Docs gates in the pinned renderer environment, all rc 0 (`docs_gates.log`): `check_em_dash.py --base 1a5d70fa` and `--base db9aa8c9`, `docs_check.py`, `gen_toc.py --check` and `--verify-anchors`. |

## Commands run at this head (receipts under `receipts/`)

| Command | Exit | Result |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32` | 0 | every arm PASS; rv32 freestanding 12 objects (`arms.log`) |
| `maap_differential.py --self-test` (pinned simulator) | 0 | 12/12 PASS; 16/16 controls (`diffself.log.gz`) |
| `fw_coverage.py --check --jobs 4` | 0 | 17 files PASS (`coverage.log`) |
| `scripts/r528_2_mutants.py ... repo` (12 delta controls, missing-interrupt also in `maap_if2`) | 0 | 12/12 named-caught (`repomut.log`) |
| `scripts/r528_2_mutants.py ... reviewer` | 0 | 20 planted: 16 caught, 2 build failures (re-spelled), 1 escape (S1), 1 equivalent (`rmut.log`) |
| `scripts/r528_2_mutants.py ... reviewer` (re-spelled) | 0 | 2/2 caught (`rmut2.log`) |
| `scripts/r528_2_diff.py` | 0 | 5/5 differential plants caught (`diffr.log.gz`) |
| docs gates (pinned renderer environment) | 0 x5 | `docs_gates.log` |
| `scripts/restore_check.sh` | - | exact head and tree; index = HEAD, worktree = index; no flags; modes match; 0 rehash mismatches; nothing untracked or ignored after removing my bytecode caches; gitlinks match HEAD (`external` uninitialised, as at start) (`restore_check.log`) |

Simulator identity is in `receipts/toolchain.txt` (Verilator 5.050 rev v5.050; the wrapper
sha256 is unchanged from R528-1). Jobs ran with at most 16 concurrent compiler jobs.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `maap.c`/`maap.h` against IEEE 1722-2016 Table B.7 (notes a-d), Table B.8, B.3.4-B.3.6; differential timing; unchanged clauses carried from the R528-1 cell-by-cell pass | R528-2 (delta), R528-1 (unchanged clauses) | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| RTL | CLEAN | `ctrl_app.c:55-58`, `ctrl_loop.c:59-78`, `mbx_contract.h:117-129`, scope diffs, `milan_datapath.sv:1999-2002`, `KL_pp_maap_shim.sv:76-77`; CSR offsets from R528-1 | R528-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| Robustness | CLEAN | preference lifecycle in `maap.c`; wake and stall tests; unchanged queue/guard/tag paths from R528-1 | R528-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| Tests | CLEAN (S1 optional) | positive gate, coverage, 12 repository and 22 reviewer controls, differential 16 + 5 controls | R528-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| Docs | CLEAN (R1 residue) | `maap/README.md`, `ctrl/README.md`, `MAILBOX_SPLIT.md:420-423`, PR body, #686, docs gates | R528-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |

R528-1's ledger at `1a5d70fa` is superseded for every lens. Each lens's scope is touched by the
delta (`maap.c`, `ctrl_app.c`, tests, README), so each was re-covered at this head.

## Real limits

- Host evidence only. There is no target CPU timing, wire capture, bench or hardware run.
  Physical calibration was NOT RUN. The H-MAAP figures rest on the documented assumption of
  100 ns per mailbox access with 1 ms timer resolution.
- The wake test models the platform's wait as a host callback. It does not exercise the RV32
  WFI or interrupt-controller binding. The RV32 arm builds `-DNDEBUG` objects only.
- Not rerun by me: the full 192-defect campaign (I ran the 12 new controls and my own plants),
  `ctrl_nvm`, the mailbox RTL suite, the builder/static bank, Yosys, and the parent, processor
  and gPTP banks. No file in their scope changed in the delta. The manager's source banks at
  this head are cited, not reproduced.
- Hosted contexts at this head were read at 02:51Z (`hosted_checks_final.tsv`). These had
  completed successfully: rtl-fast, firmware-unit, yosys-elaboration, verilator-lint,
  full-ci-gate, changes, bdd-conformance, wire-accountability, docs-check-no-git, Verilator
  shard 3/5 and Yosys shards 0-3. Verilator shards 0, 1, 2 and 4, docs-check and elaborate were
  in progress. Physical gPTP was skipped, which is not an execution.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the in-progress Verilator
  shards, docs-check and elaborate.
- The deferred dev merge round once #683 and #685 are in dev (not a finding). Keep the ilp32d
  SDK builds and the MAAP arms and partitions, then rerun the whole firmware gate set. Build and
  validate the candidate against live dev (`79b086d4` at assignment).
- Carry R528-2-R1 to the residue checklist. R528-2-S1 is optional.
- Merge only with explicit maintainer authorization, followed by post-merge containment.

R528-2 FINISHED
