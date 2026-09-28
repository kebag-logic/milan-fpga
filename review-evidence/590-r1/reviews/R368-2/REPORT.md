[R368] NEGATIVE - exact head c64f8cd896a4462bd42c4b90b32861ac7fd35176

# R368-2 internal independent review: issue #590 / PR #609 (with #592 and #599 simulation scope)

- Head reviewed: `c64f8cd896a4462bd42c4b90b32861ac7fd35176`, tree `d83fe0c35f7675c7408dd19c18fd3094f0044a3b`, in a clean detached clone.
- Delta reviewed: `792a57b0..c64f8cd8`, two commits: `ececc631` (fix) and `c64f8cd8` (capture and service re-measure, docs).
- Whole lane re-read where the delta interacts with it: `git diff 8bc97021..c64f8cd8`, with lane-owned changes separated from dev through the merged parent `20aa4eabf`.
- Round: R368-2. My round-1 findings (R368-1 F1-F3, S1, S2) are resolved or retained below. The other reviewer's round-1 public findings (R369-1) were read only after this verdict and ledger were written; their disposition has its own section below.
- Authorities read:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - Issue #590: the round-2 assignment 5862495507, which records the option (a) decision, [A402] TAKEN and REVIEW READY 5865308902.
  - The #592 body, including acceptance 1-4.
  - `docs/design/SAVED_STATE_FASTCONNECT.md` section 9 (the `nvm_backed` contract).
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 18 and 20.
  - `hdl/milan/KL_nvm_backend.sv` (the backed/stale next-state logic).
  - IEEE 802.3 22.3.4 read timing.
  - The pinned LiteX `a1e1c365` (`bios/main.c`, `bios/readline*.c`, `libliteeth/mdio.c`, `bios/Makefile`, `integration/builder.py`, `bios/cmds/*`) and the pinned liteeth `276c9e37` (`LiteEthPHYMDIO`).
- Public evidence:
  - `0f817be1:review-evidence/590-r1` and the `590-review-evidence` branch hold only round-1 archives: the executor packet and the two round-1 reviews.
  - At 07:44Z the branch tip `28e9df9e` added only the current-round external review archive, which was not read.
  - No round-2 manager or executor receipt had been published at that time.
  - The exact-head hosted check-run snapshot is in `receipts/hosted_check_runs.txt`.

## Verdict summary

NEGATIVE. All five of my round-1 items are resolved at this head: the MDIO phase blocker, the dispatch-coverage major, the untested record edge and both suggestions. Two new MINOR findings are open, and four SUGGESTIONs are optional.

What holds at this head, verified in this round:
- **F1 is fixed.**
  - `phy_mdio_bit` samples with MDC low before each rising edge.
  - The read clocks two turnaround bits (sampling the second as `ack`) and then samples 16 data bits. This matches the pinned LiteX `libliteeth/mdio.c` phase.
  - Both peers launch frame bit k+1 on edge k.
  - My unchanged round-1 IEEE-timed peer now reads BMSR `0x796d` and publishes 13.
  - Three planted phase errors fail, and so does the old peer convention.
  - The committed `late-sample` mutant is caught by the host PHY test.
- **F2 is fixed.**
  - `0006-bios-dispatch-hook.patch` applies cleanly to the pinned LiteX, at its stated line numbers, and reverses cleanly.
  - The hook sits after `readline` in the one console loop, so every line reaches it.
  - The library is linked `--whole-archive`, so the firmware's strong definition replaces the weak default.
  - The five per-handler ticks are gone.
  - The residual for long built-ins is documented accurately.
- **F3 is fixed.**
  - My round-1 `edge-cross` mutant is killed on all five shapes, with both named findings.
  - A stronger two-byte crossing is also killed, as is a copy that ignores ownership.
- **S1 and S2 are taken as described.**
- **The capture receipt binds the head firmware** (`2e715af6…`).
  - All 96 captures pass with zero mismatches and zero open records.
  - The 8x8 maximum is 13.22872 ms, 11.27128 ms under 24.5 ms, a 3.7041x ratio to the 49 ms floor.
  - `check_nvm_capture` passes.
- There is no RTL, processor or builder change in the delta.

Why the verdict is NEGATIVE:
1. **N1: the new dispatch hook heartbeats for a writer that has disabled itself.**
   - `nvm_boot()` disables persistence without retiring the writer on a shape mismatch. `milan_init()` returns before `nvm_boot()` on a CSR identity mismatch.
   - At the source base neither state can ever heartbeat.
   - At this head one console line, even an empty one, raises `nvm_backed` with `img_valid=0`. `stale=1` follows 2 s later.
   - The firmware's own rule is that a writer which will never commit stops answering, so the fabric reads "a port with no writer".
2. **N2: the authoritative snapshot-ownership design page still states the superseded capture measurement.**
   - It gives 24.30246 ms, a 2.0163x margin, 0.19754 ms of headroom, "ON is 0.78591 ms faster than OFF" at 100 MHz, and a pinned firmware.
   - It links the same receipt, which this lane replaced; the lane's own harness README sends readers to that section.

## Round-1 findings (R368-1): resolution at this head

| ID | Round-1 severity | Status at `c64f8cd8` | Evidence |
| --- | --- | --- | --- |
| F1 | BLOCKER | RESOLVED | `milan_baremetal.c:788-823`; `phy_host.c:52-58`; `phy.hpp:23-27`; `build.py:115-121`; `run.py:527-541`; `receipts/mdio_phase_probe.log`; `receipts/test_phy_firmware.log` |
| F2 | MAJOR | RESOLVED (option a) | `0006-bios-dispatch-hook.patch` against LiteX `a1e1c365`; `milan_baremetal.c:933-938`; five handler ticks removed; `run.py:49-50,353-355,465-466`; `build.py:110-114`; BAREMETAL_FIRMWARE.md:1896-1909; 397_SERVICE_BUDGET.md:185-196 |
| F3 | MINOR | RESOLVED | `test_nvm_firmware.py:538-577`; `nvm_host.c:393-399,724-730`; `receipts/mutant_r1probe_edge_cross.log`; `receipts/mutant2_*.log`; `receipts/edge_residues.log` |
| S1 | SUGGESTION | TAKEN | `nvm_capture_cpu/run.py:85-110,142-152`; README:78-91 |
| S2 | SUGGESTION | TAKEN | `nvm_capture_cpu/README.md:105-108`; `soc.py:137` (`with_mac=False`) |

Details:

- **F1: the MDIO read phase.**
  - `phy_mdio_bit` now drives the pins with MDC low, waits 32 cycles, samples, and only then raises MDC. The sample for bit k is therefore taken before rising edge k.
  - `phy_mdio_read` clocks 46 command bits and discards the first turnaround sample (the released line). It checks the second turnaround sample (bit 47) as the zero `ack`, then reads D15..D0 before edges 48..63.
  - This is the IEEE 802.3 22.3.4 point. Pinned LiteX `raw_turnaround()` plus `raw_read()` produce the same phase: two unsampled turnaround clocks, then a sample before each data edge.
  - The pin mapping MDC=1, OE=2, OUT=4 and the MultiReg input match `LiteEthPHYMDIO` at the pinned liteeth.
  - Both peers set the reply at edge k to frame bit k+1: TA zero at 46, D15 at 47, the released 1 at 63. Before edge 46 they reply 1.
  - My probe (`probes/mdio_phase_probe.py` with the unchanged round-1 `mdio_peer_probe.c`) ran eight arms:
    - The head reader with the IEEE peer published 13 and read BMSR `0x796d`.
    - The head reader with the old convention failed.
    - `late-sample` with the IEEE peer read `0xf2db` and published 0, which is the round-1 defect.
    - One-TA-clock and three-TA-clock readers both failed.
    - The late reader with the old convention published 13. This is the round-1 pair, which agreed by construction.
  - The committed `test_phy_firmware.py` catches `no-publish`, `defer-recovery` and `late-sample`.
  - The target control:
    - `build.py` plants the same late-sample text, and `report_verdict` requires the named finding "PHY initial gigabit negotiation was not published".
    - Traced against the peer: `phy.hpp` BMSR `0x0124` read late is `0x0249`, so link=0 and the first publication is 0. That is the finding.
    - I did not execute the target run (see limits).
  - The "independent peer" wording is replaced by an IEEE statement in the findings page, BAREMETAL_FIRMWARE.md:1935-1937 and the fw_service_budget README.
- **F2: the dispatch hook.**
  - The patch applies to pinned LiteX `a1e1c365` with `git apply --check` (hunks at 172 and 344) and reverses cleanly. It stacks with 0004, which touches a different file.
  - In the patched `bios/main.c`, `command_dispatch_hook()` runs immediately after `readline()` and before `printf("\n")`, before the empty-line test and before `get_param`/`command_dispatcher`. That is the only console loop, and both readline variants use it. So built-ins, unknown commands, whitespace-only lines and empty lines all reach it.
  - The BIOS links `ALWAYS_LINK_LIBS` inside `--whole-archive` (`bios/Makefile:60`), and `milan_soc.py:3865` adds `libmilan_baremetal` with `always_link=True`. The firmware's strong `command_dispatch_hook` therefore replaces the weak no-op.
  - The override calls only `nvm_heartbeat_tick()`, which is rate-limited and includes the PHY poll. It does not call `nvm_service`, so no idle auto-commit can start mid-line.
  - All five `define_command` entry ticks are removed.
  - `queued-builtins`:
    - The plan is 350 × (`mem_read 0x40000000 128`, empty line, `unknown_command`) plus `milan_status`, 1051 lines in total.
    - Each line must show `tick_calls > 0` inside its own `command_start..command_end` window.
    - The sim feeds RX bytes at core speed (`sim_main.cpp` drive/uart_sample), so the idle hook cannot fire mid-line.
    - `--self-test` refuses a queue under 133 bytes.
  - `remove-dispatch` now empties the hook body, and `report_verdict` requires "continuous backing lost". My host-bench probe independently shows that emptying the hook removes every console-line heartbeat (the `head-empty-hook` arms in `receipts/disabled_writer_probe.log`).
  - The residual text in BAREMETAL_FIRMWARE.md, the findings page and the fw_service_budget README matches the BIOS sources. `mem_test`/`mem_read` and every other built-in body (`crc`, `mem_speed`, `mem_copy`, `sdram_*`, `flash_*`) have no service opportunity, and "long BIOS built-ins" is stated generically with examples.
  - Builder gate 23h reads apply.sh's SERIES and requires the live tree to equal upstream plus the whole series, so 0006 is enforced there. The bench LiteX tree at the pinned revision already carries the hook (read-only check).
  - The target-run figures (both shapes pass with zero unbacked cycles; the hook-removal control shows an 8238.99363 ms gap) come from the executor's report and the findings page. Their raw logs are reported lost; see limits.
- **F3: the record-edge test.**
  - The host bench drives an ownership vector through `--open-record`. The new grade picks the first contiguous pair whose right record starts unaligned. It poisons the open record, header included, changes the closed predecessor, commits, and compares the stage and slot bytes.
  - My round-1 `probes/host_mutant.py edge-cross` (unchanged, `>= 1u`) is killed on all five shapes, Arty included, with both named findings.
  - Added this round (`probes/host_mutant2.py`):
    - `edge-cross-2` (`>= 2u`) is killed on all five shapes.
    - `ignore-ownership` (`copy = 1`, keeping `own` referenced so the host `-Werror` build compiles) is killed on all five shapes.
    - `byte-only` survives the host gate, as it must: it is a timing control graded by the capture harness.
    - `edge-cross-3` (`>= 3u`) survives. `probes/edge_residues.py` shows every contiguous unaligned edge in every shipped shape has residue 2, so a one-byte crossing cannot occur on any shipped layout. That is an equivalent mutant, not a gap.
  - The committed `--self-test` catches `edge_cross` through its named assertion.
- **S1: byte-only grading.**
  - Each byte-only capture must exceed 1.5x the matched optimized maximum on shape, clocks, phase and traffic.
  - The boundary (15 against 10 accepted, 14.99999 refused) and a mismatched scenario are checked before every measurement.
  - The measured ratio of 1.83666x is from the executor's report; its raw log is reported lost.
- **S2: the capture README** says the capture SoC omits `milan_mac` and compiles the PHY path out. `soc.py:137` confirms `with_mac=False`.

## New findings (R368-2)

### N1: MINOR: the dispatch hook heartbeats for a writer that has disabled itself without retiring (shape mismatch) or that never started (CSR identity mismatch)

- **Lenses:** Conformance, RTL, Robustness, Tests.
- **Where:**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:933-938`: `command_dispatch_hook` calls `nvm_heartbeat_tick()` unconditionally.
  - `:918-931`: `nvm_heartbeat_tick` stops only when `nvm_retired` is set.
  - `:1435-1438`: `nvm_boot` returns with "persistence disabled" and sets neither `nvm_ready` nor `nvm_retired`.
  - `:1625-1628`: `milan_init` returns before `nvm_boot` on "CSR identity mismatch; fabric remains disabled".
- **Authority and evidence:**
  - `SAVED_STATE_FASTCONNECT.md:1055` defines `nvm_backed` as live evidence that "a writer answered within T-NVM-WRITER-ALIVE". Section 9's opening names a false durability claim as "the false-success condition issue #70 exists to remove".
  - The firmware's own rule (`milan_baremetal.c:417-421` and `:923`): a writer that will never commit "stops answering the liveness deadline, so the fabric revokes nvm_backed and a controller reads the state as what it is, a port with no writer".
  - `KL_nvm_backend.sv:647-651,676-678`: one heartbeat sets `backed` and `ever_backed`.
  - The probe `probes/disabled_writer_probe.py` uses the repository's own host bench with planted preconditions only, leaving the firmware's reaction unchanged (receipt `receipts/disabled_writer_probe.log`):

    | Firmware | Shape mismatch, one empty line | CSR identity mismatch, one empty line | +2500 ms (either state) |
    | --- | --- | --- | --- |
    | Head | `hb=1 backed=1 valid=0` | `hb=1 backed=1 valid=0` | `backed=0 stale=1 losses=1` |
    | Source base `8bc97021` | `hb=0 backed=0` | `hb=0 backed=0` | `stale=0` |
    | Head with the hook body emptied | `hb=0 backed=0` | `hb=0 backed=0` | `stale=0` |
    | Round-1 head `792a57b0` | `hb=0` (empty line) | `hb=0` (empty line) | — |

  - At the round-1 head the fault already occurs through the `milan_status` handler tick. That latent path is in the lane and I missed it in round 1. This round's hook widens it to every console line, including a bare Enter.
- **Impact:**
  - On a build whose generated shape disagrees with the record walk, persistence is announced disabled, yet PP_STAT advertises durable backing while an operator uses the console. After the last line it reports a writer *loss* (`stale=1`) instead of the honest never-backed state.
  - A controller or test reading PP_STAT gets the false-success report the contract exists to exclude.
  - On a CSR identity mismatch, firmware that promised to leave a foreign fabric untouched now reads its TOD and writes its `PP_NVM_STAT` strobe on every console line.
  - No committed test covers either disabled state under console input.
  - The source base had no such path.
- **Required outcome:**
  - No heartbeat reaches the backend unless the writer is live (or deliberately answering by an existing documented rule): not from the dispatch hook, not from a Milan command.
  - This covers the shape-mismatch disable and the pre-`nvm_boot` identity-mismatch return, for example by retiring or gating the writer in both paths. The tag-mismatch path's existing behavior is outside this finding.
  - A committed host test drives console lines, including an empty line, in both states and requires `hb=0`, `backed=0` and `stale=0`. The unguarded hook must fail it.
- **Verification:** `probes/disabled_writer_probe.py` shows `hb=0 backed=0 stale=0` for the head in both planted states and unchanged healthy arms. The new committed test reddens on the current hook.

### N2: MINOR: the snapshot-ownership design page states the superseded capture measurement against the receipt this lane replaced

- **Lenses:** Docs.
- **Where:** `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`:
  - section 18 "Cost", lines 1591-1630 and 1654-1662;
  - section 20 item 6, lines 1779-1786.

  These are reached from `tb/verilator/nvm_capture_cpu/README.md:136` ("Section 18 quantifies both arms"), a file this lane edits.
- **Authority and evidence:**
  - The page still says:
    - "The worst 8x8 measurement is 24.30246 ms", with a 2.0163x margin;
    - "It leaves 0.19754 ms below the assigned limit";
    - "The product firmware is pinned in the refreshed receipt";
    - "Firmware and hold behavior are unchanged by this remeasurement";
    - "At 100 MHz, ON is 0.78591 ms faster than OFF. This is why both arms determine the maximum";
    - and in section 20.6, "The worst 8x8 copy is 24.30246 ms".
  - It links `measurements.json` as the receipt holding "all 96 captures".
  - At this head that receipt holds a different firmware (`2e715af6…`) and 8x8 50 MHz ON 13.22872 / OFF 13.07044 ms. At 100 MHz, ON (9.94948) is 0.00854 ms *slower* than OFF (9.94094). The 1x1 figures are 3.88578/3.84214 (`receipts/capture_receipt_rows.txt`).
  - The page came from dev (`d02db63c3`, already in the merged parent `20aa4eabf`). The lane's first re-measure (`ba3a4781`) replaced its figures, and neither round updated it. I missed this in round 1.
  - #592 exists to recover this headroom; acceptance 2 asks for "the new 8x8 maximum and the margin gained". The only repository prose that states the margin now states the superseded one.
  - AGENTS.md section 6, Docs lens: changed contracts and evidence must be reflected in authoritative docs.
- **Impact:**
  - A reader planning 8x8 growth (#584's name records, #70's remaining items) is told only 0.2 ms of headroom remains, when the measured headroom is 11.27 ms.
  - The traffic-arm conclusion at 100 MHz is inverted.
  - The page and its linked receipt contradict each other.
- **Required outcome:** Section 18 and section 20.6 either state the current receipt's figures and identity, or clearly mark the old ones as the pre-#592 measurement. They must state the new 8x8 maximum and margin, and must not claim the linked receipt pins the old firmware.
- **Verification:** each figure on the page equals `measurements.json` at the merge head (the reviewer recomputes from the receipt), and the page names the receipt's firmware digest or defers to it.

## Suggestions (optional; do not affect coverage)

- **T1, product build prototype warning.**
  - `milan_baremetal.c:935` defines the external `command_dispatch_hook` with no prior prototype. LiteX `common.mak` compiles with `-Wmissing-prototypes`.
  - Host gcc with the same prototype flags gives 0 warnings for `792a57b0` and exactly one ("no previous prototype for 'command_dispatch_hook'") at head.
  - The file already declares its other external interfaces (`:355`, `:767-769`), so a declaration beside the definition keeps the product build warning-clean.
- **T2, the series record in `apply.sh`.** The header comment (`apply.sh:6-15`) still lists only 0002, 0004 and 0005, while SERIES (`:35`) and the README list 0006. The README also opens a new list with a blank line before the 0006 bullet. The SERIES array, which is what gate 23h reads, is correct.
- **T3, an unchecked receipt field.** `measurements.json:1377` `bios_dispatch_patch_sha256` has no producer or consumer in the repository. `check_nvm_capture` does not check it. Either bind it in the gate or say it is informational.
- **T4, the findings-page deadline column.** In `397_SERVICE_BUDGET.md:82-96` and the 8x8 table, "Empty line" and "Unknown line" show a 500 ms deadline while `milan_status` and `mem_read` show N/A. The harness assigns the same 500 ms row budget to all four, and none carries a protocol deadline, so the column is inconsistent.

## Findings of the other reviewer's round 1 (R369-1): resolution at this head

I read [R369-1](https://github.com/kebag-logic/milan-fpga/pull/609#issuecomment-5862463802) only after the verdict, the findings above and the ledger were written. Nothing in it changes them. The current-round external report was not read.

| R369-1 item | Severity | Status at `c64f8cd8` | Evidence |
| --- | --- | --- | --- |
| F1 MDIO reader samples one bit late | BLOCKER | RESOLVED | Its public probe (`review-evidence/590-r1/reviews/R369-1/probe_mdio_phase.{py,c}` at `a1c4d79f`, run unchanged) prints `PHASE=1 BMSR true=0x796d firmware_reader=0x796d`, `PHYID1 … firmware_reader=0x001c` and `published link_status=13` (`receipts/r369_1_probe_mdio_phase_at_head.log`). Its other required outcomes (IEEE peers, a planted-phase control, re-established claims) are covered by my F1 resolution above. |
| F2 queued built-ins get no dispatch opportunity | MINOR | RESOLVED | Same resolution as my F2 (option a, the recorded decision 5862495507): the hook covers built-in, unknown and empty lines; the `queued-builtins` plan and hook-removal control are committed; the docs state the long-built-in residual. The target-run figures are subject to the limits below. |
| S1 PHY discovery rate and error hold | SUGGESTION | NOT TAKEN; retained as optional | `phy_link_tick` (`milan_baremetal.c:874-908`) is unchanged in this round. Discovery now also runs from the per-line hook, which adds no new failure mode. |
| S2 byte-only control not self-grading | SUGGESTION | TAKEN | Same as my S1: `nvm_capture_cpu/run.py:85-110,142-152`. |
| S3 literal 4 in the builder fixture | SUGGESTION | NOT TAKEN; retained as optional | No builder file changed in this round. |
| S4 no CHANGELOG entry | SUGGESTION | NOT TAKEN; retained as optional | `CHANGELOG.md` is unchanged in the lane. CONTRIBUTING has no rule requiring an entry. The authoritative page that states superseded capture figures is my N2. |

## Lens coverage and clean-result evidence

| Lens | Result | Examined artifacts at `c64f8cd8` |
| --- | --- | --- |
| Conformance | UNCLEAN (N1) | Round-2 assignment items 1-3 and the taken S1/S2; the #592 acceptance 1-4; IEEE 22.3.4 against `milan_baremetal.c:788-823` and both peers; option (a) against the patched pinned `bios/main.c`; the section 9 `nvm_backed` contract against the hook paths; receipt digest `2e715af6…` equals `sha256(milan_baremetal.c)`; 96 captures clean; 8x8 13.22872 ms under 24.5 ms. |
| RTL | UNCLEAN (N1) | No `hdl/` change in `792a57b0..c64f8cd8` or the lane (gitlinks `16be6768`/`5dce647a`/`48ff7a7e` unchanged). The `LiteEthPHYMDIO` pin contract and MultiReg (pinned liteeth) match the firmware constants. `KL_nvm_backend.sv:630-697` backed/stale next-state reviewed against the new heartbeat callers. N1 breaks the firmware-to-fabric identity contract ("fabric remains disabled"). |
| Robustness | UNCLEAN (N1) | Every console-line class through the hook (built-in, unknown, whitespace, empty); rate limit and no auto-commit from the hook; retired writer; the shape-mismatch, identity-mismatch and tag-mismatch paths; long built-in residual; edge residues of all shipped layouts; ownership-vector fixture reset on RELOAD (`nvm_host.c:212,326`). |
| Tests | UNCLEAN (N1) | Re-ran at head: `test_phy_firmware.py` (3 mutants caught); `test_nvm_firmware.py --self-test` (5 shapes, 5 planted defects, PHY mutants); `check_nvm_capture.py` (7 controls); `fw_service_budget/run.py --self-test` (43 grading, 14 flash). Probes: MDIO phase (8 arms), host mutants (5), edge residues, disabled writer (24 arms). The gap is N1 (no test of disabled states). |
| Docs | UNCLEAN (N2) | BAREMETAL_FIRMWARE.md runtime, capture and PHY paragraphs; `397_SERVICE_BUDGET.md` delta; nvm_hosttest, fw_service_budget and nvm_capture_cpu READMEs; `sw/litex/patches/README.md` and `apply.sh`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 18 and 20; `check_doc_paths` and `check_doc_style` rc 0. |

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN | Round-2 assignment; #592 acceptance; IEEE 22.3.4 against the reader and peers; patched pinned BIOS; section 9 contract; capture receipt | R368-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| RTL | UNCLEAN | Delta has no RTL; MDIO pin contract; `KL_nvm_backend.sv` backed logic; CSR identity contract | R368-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| Robustness | UNCLEAN | Console-line classes; disabled and retired writer paths; built-in residual; record-edge residues | R368-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| Tests | UNCLEAN | Host PHY, host NVM self-test, capture gate, service self-test re-runs; MDIO, mutant, residue and disabled-writer probes | R368-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| Docs | UNCLEAN | BAREMETAL_FIRMWARE; 397 findings; three harness READMEs; patch series README and apply.sh; snapshot-ownership sections 18 and 20 | R368-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |

## Real limits

- **No product-CPU simulation was run in this review.** The scoped Verilator path named in the assignment (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host; only an unpinned system Verilator 5.052 is present. There is also no LiteX Python environment or RV32 toolchain in the permitted areas.
- **Not reproduced here:**
  - the target `queued-builtins` pass on both shapes;
  - the target `remove-dispatch` and `late-sample` controls;
  - the service re-measure (largest heartbeat gap 322.45756 ms; 8x8 reserve 4.46169 ms);
  - the byte-only ratio of 1.83666x.

  I checked their grading code and anchors. The figures come from the executor's report and the findings page, and the executor states the raw logs and native builds were lost to a host restart, leaving size and SHA-256 bindings only.
- **Round-2 manager receipts.** None were published when this report was written, so these figures rest on the manager's native bank receipts once they land.
- **N1's probe runs on the host bench**, the repository's own model of the backend, with planted preconditions. The backend RTL logic it relies on (one heartbeat sets `backed`) was read, not simulated here.
- **Some docs gates were NOT RUN.** `gen_toc --check` and `check_em_dash` need the pinned Markdown renderer, which is not installed; nothing was installed.
- **No builder bank was run** (not permitted). No builder file changed in the delta, and no builder gate reads the tick placement.
- **Physical calibration was not run.** Field skips and simulation are not hardware proof; the MDIO phase on silicon is #599 acceptance 4 (the post-merge bench lane).

## Pending manager duties

- Hosted acceptance at the exact head. At the 07:44Z snapshot (`receipts/hosted_check_runs.txt`), these were green: `rtl-fast`, lint, all Yosys shards, `yosys-elaboration`, `elaborate`, and Verilator shards 0 and 3. Verilator shards 1, 2 and 4 and `docs-check` were in progress. Physical gPTP was skipped, which is not an executed job.
- Local act replication.
- The final current-dev candidate at the merge turn (source base `8bc97021`, live dev `54ce8773`).
- Publishing the round-2 native bank receipts: `queued-builtins`, `remove-dispatch`, `late-sample`, byte-only, capture arms.
- Routing N1 and N2 to the executor.
- The external review ([R369]).
- The #599 physical re-run after merge. The bench LiteX tree already carries the 0006 hook.

## Receipts and probes (listed in MANIFEST.sha256)

- `probes/mdio_phase_probe.py` with `probes/mdio_peer_probe.c` (the round-1 peer, unchanged) → `receipts/mdio_phase_probe.log`.
- `probes/host_mutant2.py` (edge-cross-2, edge-cross-3, ignore-ownership, byte-only) → `receipts/mutant2_*.log`.
- The round-1 `host_mutant.py edge-cross`, run unchanged from the round-1 packet → `receipts/mutant_r1probe_edge_cross.log`.
- `probes/edge_residues.py` → `receipts/edge_residues.log`.
- `probes/disabled_writer_probe.py` → `receipts/disabled_writer_probe.log` (N1).
- The R369-1 public probe, run unchanged → `receipts/r369_1_probe_mdio_phase_at_head.log`.
- Committed gates:
  - `receipts/test_phy_firmware.log`;
  - `receipts/test_nvm_firmware_selftest.log`;
  - `receipts/check_nvm_capture.log`;
  - `receipts/fw_service_selftest.log`;
  - `receipts/doc_checks.log`;
  - `receipts/capture_receipt_rows.txt` (my recomputation from the receipt, used by N2).
- `receipts/hosted_check_runs.txt` and `receipts/clean_state.txt`.

## Post-probe state

- `receipts/clean_state.txt`:
  - HEAD `c64f8cd8…`, tree `d83fe0c3…`; the index writes the same tree.
  - Empty porcelain status, untracked files included; no index/HEAD mode, blob or path difference.
  - `protocol-processor 16be6768`, `gptp-processor 5dce647a` and `third_party/verilog-axis 48ff7a7e` are checked out at their gitlinks and clean; `external` is uninitialized, as at clone time.
- All mutants and probes ran from temporary copies or `scratch/`.
- No source edit, commit, push or GitHub write was made.

R368-2 FINISHED
