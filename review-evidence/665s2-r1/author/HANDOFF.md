# [A681] #665 lane S2: the CPU cycle and latency budget (HANDOFF)

Status: **STOP (owner decision D4)**, 2026-10-26. The measured rows miss T_svc = 10 ms at both points, in both arms. The harness, its controls and its mutants are complete and green. The STOP is the measurement's result, as the assignment predicts ("Expect a STOP into S2b").

- Head: `d58c8e22e9bd96237b9a28ea1ddd55b0426380c4`, one commit on `e76a755a`. Subject `Measure every split service path in CPU cycles on the shipping core (#665)`, no body, no trailers.
- Branch `665-s2-cpu-budget`, base `origin/dev-soft-core` `e76a755afc0536453161e3cd33f6f4d2dcd7641f` (verified). The PR targets `dev-soft-core`.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified).
  - `third_party/lwSRP` (08ee86e8) and `third_party/tsn-c-stack` (70936b77) were not initialised in the lane.
  - `git submodule update --init` initialised them at the recorded gitlinks, with their own origins verified.
  - No tracked file outside the new directory changed.
- Assignment: issuecomment-6409745905. Decisions: issuecomment-6409738976 (D3, D4, D5). Branch policy: issuecomment-6409455089. TAKEN: issuecomment-6409842373. STOP: issuecomment-6413662864, whose body is the copy in `STOP-COMMENT.md`.
- Nothing pushed. No PR, no issue or comment edit. No Vivado, bench or hardware.
- No shipping RTL, SoC, firmware, CI or workflow file changed.

## Contents

1. [Result](#1-result)
2. [Acceptance](#2-acceptance)
3. [Changes, file:line and reason](#3-changes-fileline-and-reason)
4. [New checks, planted mutants and failing words](#4-new-checks-planted-mutants-and-failing-words)
5. [Gate table](#5-gate-table)
6. [Run history and reproducibility](#6-run-history-and-reproducibility)
7. [Defects found, each for its own issue](#7-defects-found-each-for-its-own-issue)
8. [Open risks and questions](#8-open-risks-and-questions)

## 1. Result

Every figure is a measured clock count on the shipping cacheless VexiiRiscv: CPU at 50 MHz, bus at 100 MHz.

- The full tables are in `tb/verilator/ctrl_service_budget/README.md` (Results) and `receipts/measured-drivers/report.md`.
- Every probe is in `receipts/{A1,A8,B1,B8}/table.md` and `results.json`.

There are two arms:

- **Arm A** is the image as linked. It is the formal measurement.
- **Arm B** is a labelled second arm whose four fixture observation callbacks answer. It changes test code only: a scratch copy of `ctrl_aecp_image.c`.

| Figure | 1x1, one interface | 8x8, two interfaces |
|---|---|---|
| Mailbox read / write | 9 / 9 CPU cycles (0.18 us); `KL_mbx` answers in 1 bus cycle | same |
| BRAM fetch (max) | 9.10 (303) CPU cycles | 9.15 (303) |
| Flash-window read | 263 mean (138 to 303) | same |
| CPI, fetches per instruction | 9.72, 1.73 | 9.62, 1.70 |
| Fetch share of CPU bus transactions, arm A | 0.858 to 0.892 | 0.850 to 0.889 |
| Code fetched, boot / service (largest run) | 11,160 / 40,532 B of 85,912 B `.text` | 11,396 / 43,060 B of 87,596 B |
| Idle pass, A | 65,703 to 72,358 cycles (1.31 to 1.45 ms) | 102,152 to 185,315 (2.04 to 3.71 ms) |
| Worst pass, A | 1,552,161 (31.04 ms) | 2,989,496 (59.79 ms) |
| Composed maximum, A / B | 27.83 / 13.70 ms | 42.82 / 26.04 ms |

Backlog rows (`MAILBOX_SPLIT.md:753-758`), in ms at the measured phase, with the pass bound in brackets:

| Row | A 1x1 | A 8x8 | B 1x1 | B 8x8 |
|---|---:|---:|---:|---:|
| an event behind 15 others | 14.12 (27.14) | 40.51 (67.64) | 14.12 | 40.51 |
| an ACMP command behind a full acmp ring | 60.35 (67.08) | 101.98 (113.42) | 60.36 | 101.98 |
| an ENTITY_AVAILABLE behind a full adp ring | 43.90 (52.85) | 48.63 (65.42) | 7.90 | 15.28 |
| a response with 7 frames owed ahead | 75.76 (78.70) | 98.93 (106.92) | 75.78 | 98.93 |

T_svc misses: A1 10, A8 44, B1 3, B8 4 (`receipts/head/*-regrade.log`). Every probe was measured, with 0 refusals.

Decision input:

- **D4.** Per-pass CPU work, not mailbox accesses, sets the time. The consumers, in order:
  - byte-loop `memset` and `memcpy`. Each AECP response zeroes its 1,514-byte frame (`aecp.c:58`) and its 1,476-byte payload (`aecp_commands.c:555`), about 154,000 cycles in a READ_DESCRIPTOR pass;
  - lwSRP `mrp_mad`, 474,000 cycles in the 8x8 link-up pass;
  - the two AECP polls, about 47,000 cycles of every 1x1 pass and 94,000 at 8x8;
  - software multiply and divide (RV32I has no M extension).
- **The admitted backlog is already small.** It is min(burst, ring room): 8 ADP, 12 GET_RX_STATE, 16 AECP and 7 MAAP records. Shrinking it shortens the ring rows by whole passes, but no single 40 ms pass gets shorter.
- **The #397 one-hart rule fails.** A pass is the only tick opportunity, so every pass must be well under T_svc. Single passes reach 31 ms (1x1) and 60 ms (8x8).
- **Arm A's AECP retries every millisecond** (`aecp.c:461-495`, `retry_at = a->now + 1u`).
  - The fixture's ports report unavailable, so after a bind every pass costs 1.06 to 1.55 M cycles.
  - Arm B takes the same H-DISC paths in 0.35 to 0.99 ms at 1x1.
  - The retry has no backoff, so a real port that reports unavailable would do the same.
- **D5** (the smaller core, deferred until after the flip). The shipping core already misses at both points, so a slower core would miss by more until S2b's cap lands.
- **D3 / S14.** A flash-window read costs about 29 times a BRAM fetch on the product's 1x SPI (`milan_soc.py:3065`). The core is fetch-bound, so no path inside T_svc can be fetched from flash. The hot set is at least 40,532 B (1x1) and 43,060 B (8x8).

## 2. Acceptance

| Item (issuecomment-6409745905) | Status | Evidence |
|---|---|---|
| Cycles per mailbox read and write | met | README "Per access"; the SUMMARY lines of `receipts/A1/*.log` |
| Each response path, `MAILBOX_SPLIT.md:495-502` | **partly met**: SHUTDOWN has no input in the fixture and is not run; the other six rows are measured | README "ADP" |
| Each response path, `:645-657` | met: every row, both arms | README "ACMP" |
| AECP and SRP paths | met: READ_DESCRIPTOR for each descriptor type and 11 commands; SRP startup, Listener Ready, malformed and Domain; MAAP | README "AECP", "SRP and MAAP" |
| Worst pass at the composed maximum | met | README "Passes" |
| Each backlog row, 1x1/1if and 8x8/2if | met | README "Backlog rows" |
| Against T_svc and the 3.4.1 ceiling | met: every probe | `table.md` of each arm |
| A planted over-budget path is caught | met | section 4 |
| The marker, clock-ratio and deadline graders are each mutated and fail | met: 12 mutants | section 4 |
| #397 one-hart rule | measured: **fails** | section 1 |
| Instruction-fetch share per path, and the memory-region share (D3, S14) | met | `table.md` (fetch share); `results.json` (region counts per taking pass) |
| D4: a row misses T_svc | **STOP** with the measured table | this file |

So the PR body says "Relates to #665", not "Closes".

## 3. Changes, file:line and reason

Every file is new and under `tb/verilator/ctrl_service_budget/`. No existing file changed.

| File:line | What | Reason |
|---|---|---|
| `split_soc.py:61` `fixture_addresses` | Reads the image's bus addresses from `ctrl_build.RV32_FLAGS` and `ctrl_nvm/test/rv32/generated/{csr.h,mem.h}`, and checks the LiteSPI master and timer0 register layouts (`:57-58`) | The image must run unmodified, and it addresses placeholders, not the split SoC (section 7.2) |
| `split_soc.py:97` `mailbox_sources` | One interface: the shipped `KL_mbx` sources. Two: `gen_mailbox.write_variant`, written into the build directory | The 8x8 point needs the two-interface RTL, and the shipped tree has only one |
| `split_soc.py:111` `power_of_two_cover` | Hands the CPU generator each region at its power-of-two cover (256 KiB for `rom` and `sram`) | The generator decode defect (section 7.1). The two netlists differ only in address-hit and PMA lines (`receipts/pma/netlist-224-vs-256.diff`) |
| `split_soc.py:159` `StimulusMailbox`; `:196` the unread publication tie-offs | The harness's own `KL_mbx` behind `KL_mbx_wb`, with CtrlMailbox's hookup, its datapath side on pads, and a ms tick divider | The assignment says "This harness owns its own stimulus top", and `CtrlMailbox`'s idle tie-offs stay untouched |
| `split_soc.py:212` `FlashBoundary`; `:228` `add_devices` | LiteSPI's crossbar, mmap reader and command master at the fixture's addresses, with CSR banks pinned (`spiflash_master` n=6, `timer0` n=7), the flash at the fixture's window, 1x fast read | The image's NVM path runs as linked. The serial device is `fw_service_budget/flash.hpp` |
| `split_soc.py:255` `CpuPatches` | Reads the shipping CPU arguments (`with_dma=True`) and applies the cover inside `generate_netlist_name` | The netlist must be the shipping core's |
| `split_soc.py:288` `build` | Builds the SoC through `nvm_capture_cpu/soc.py` (read-only), and writes `soc.json` with the SoC's and the CPU's region lists | Reuse, as assigned |
| `build.py:39` `MUTATIONS` | `slow-adp-rx`: a scratch copy of the firmware with a 16,000-iteration volatile loop after its `adp_rx` call | The planted over-budget path (section 4) |
| `build.py:53` `VARIANTS`; `:68` | `answering-ports`: five anchor edits in a scratch copy of `ctrl_aecp_image.c` | Arm B, labelled. Test code only |
| `build.py:99` `firmware` | Runs `runtime_ssp.py`, then the unmodified `ctrl_srp_image.py --with-aecp --layout split` | The assigned image |
| `build.py:123` `symbols`; `:150` `code_modules`; `:179` `member_paths` | The text symbols; each linked input section's module, from the link map; the Verilator member paths of the observed signals | Per-module cycle attribution, and observers found by name, not guessed |
| `build.py:253` `config_header` | Generates `budget_config.hpp`: constants, accessors, the region table, the code spans and the TMR_CMD word | One source for the bench's addresses and widths |
| `build.py:299` `verilate`; `:324` `build`; `:352` `reused` | Verilator `--cc --exe` and `make -j16`; `build.json` with every input's digest; reuse refused on any changed input | Reproducibility: a stale reuse cannot be graded |
| `observe.vlt` | `public_flat_rd` on the WhiteboxerPlugin commits and traps, the FetchCacheless/LsuCacheless cmd/rsp (with error), the `KL_mbx_rx` commit and the `KL_mbx_evt` writes | Passive observation only |
| `sim_main.cpp:116` `drive` | Drives the RX frames, link, GM, tx-ready and reply patches from the script | Stimulus on the mailbox's datapath side |
| `sim_main.cpp:178-240` `*_sample` | The host port; egress (TX commits); ingress (the RX commit); flash operations; CPU fetch, load and store per region; traps and bus errors | Every printed figure is an observed clock count |
| `sim_main.cpp:305` `pass_boundary`; `:315` `finish_pass`; `:341` `flush_idle` | A pass runs from one committed entry of `ctrl_loop_service` to the next, with its modules, accesses and writes; idle runs are aggregated | The pass and pass-bound definitions |
| `sim_main.cpp:350` `satisfied`; `:365` `run_script` | Script steps with bounded waits (`within N`) | No wait can hang. The run limit is 60 s |
| `frames.py` | ADP, ACMP, AECP/AEM, MVU, MAAP and MSRP frame builders, with clause comments | The stimulus frames |
| `scenario.py:79-80` | T_svc 10 ms and the 3.4.1 ceilings | The graded budget |
| `scenario.py:92` `Probe`; `:107` `Group`; `:146` `tagged` | A probe is a mark, a stimulus and a bounded wait, and the probe's frame carries a tag | One phase per probe, and the start is never mistaken |
| `scenario.py:236-468` | The ADP, ACMP (with H-DISC), AECP, MAAP and SRP groups | Every assigned path |
| `scenario.py:498` `admitted`; `:505` `backlog_groups` | The four backlog rows under the composed load, each ring offered min(burst, room) | The fabric's admitted backlog, not the desk's |
| `scenario.py:585` `control_groups`; `:602` `boot_fault_groups`; `:610` `fixture_groups` | The control group, the as-built boot and the 1x1 fixture rows | Controls and self-test input |
| `grade.py:70` `parse`; `:146` `tx_records` | Parses the log, and decodes TX frames from ring words in two phases | Ends are read off committed records |
| `grade.py:186` `cpu_cycles`; `:190` `ms` | CPU cycles = bus cycles x 50/100, rounded up; ms from the bus count | The clock conversion (mutated in section 4) |
| `grade.py:195` `start`; `:219` `end`; `:295` `combine_ends` | The 3.4.1 markers: the tagged RX commit, a level change, an armed deadline; the last required output | The marker graders (mutated) |
| `grade.py:260` `taking_pass`; `:268` `pass_bound` | The pass that commits the output, and the bound from the start of the running pass, or the longest idle pass before it | One phase is one sample, so a bound is reported |
| `grade.py:300` `verdicts` | Within T_svc (+W), inclusive; within the ceiling | The deadline grader (mutated) |
| `run.py:85` `select`; `:103` `graded`; `:123` `verdict` | Selects groups and separates refusals from misses. A control must be caught by name, counting only its `control.` paths (`:130`) | A missing or malformed probe always fails, and misses fail unless `--record-budget-findings` |
| `selftest.py:83` `checks`; `:147` `mutant`; `:226` `MUTANTS`; `:258` `main` | 19 checks on the committed trace and on synthetic logs, and 12 grader mutants | Section 4 |
| `selftest.py:234` `write_fixture` | Trims a `fixture` group log and pins its graded rows | The only way to regenerate `fixture.log` and `oracle.json` |
| `fixture.log`, `oracle.json` | Generated by `selftest.py --write-fixture` from the `fixture` group of the measuring 1x1 run | The portable self-test needs no build |
| `runtime_ssp.py:21` | Adds `-fno-stack-protector` to the runtime recipe's compiles, and to nothing else | #723 is open (section 7.3) |
| `fixture_variant.py` | Runs `ctrl_srp_image.py` with its `HERE` set to the variant's scratch tree | Arm B, without touching the shipped fixture |
| `README.md` | Run and reproduce; the test SoC and its address table; markers and grading; results, findings, controls and limits | Documents the harness and its result |

There is no Makefile, on purpose. The serial sweep discovers every Makefile, and `scripts/suite_shards.py` would then have to register the suite, a CI change outside this lane.

## 4. New checks, planted mutants and failing words

The self-test is `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` (`receipts/gates/selftest.log`).

- All 19 checks PASS, 12 of 12 mutants are caught, and it prints `self-test: 0 failures`, rc 0.
- A failing check prints `FAIL: <check>: <detail>`.
- An uncaught mutant prints `MUTANT ESCAPED: <mutant>` and fails the run.

| Planted mutant (`selftest.py:147-223`) | Failing check, as printed |
|---|---|
| marker: the frame tag is ignored | `MUTANT caught: marker: the frame tag is ignored: tagged start` |
| marker: a timer path starts when its record is posted | `... : fixture row fixture.tmr_no_resp1.if0` |
| marker: any response on the channel ends the path | `... : sequence and interface` |
| marker: the interface is ignored | `... : sequence and interface` |
| marker: the first required output ends the path | `... : fixture row fixture.set_name.if0` |
| clock ratio: CPU cycles equal bus cycles | `... : fixture row fixture.link_up.if0` |
| clock ratio: inverted | `... : fixture row fixture.link_up.if0` |
| clock ratio: milliseconds from the CPU clock | `... : fixture row fixture.link_up.if0` |
| deadline: T_svc 20 ms | `... : ceilings pinned` |
| deadline: strictly below the budget | `... : exact budget passes` |
| deadline: the normative wait is not added | `... : W + T_svc passes` |
| deadline: the ACMP ceiling is the transaction timeout | `... : ceilings pinned` |

The self-test also plants an over-budget path (`selftest.py:132-142`, check `planted over-budget path is caught`). It moves the fixture's recorded BIND_RX response to one bus cycle past T_svc, which must grade `within_t_svc` False.

The full-harness controls were rerun at the head, on byte-identical builds (`receipts/head/C-slow.log`, `C-asbuilt.log`):

| Control | Plant | Failing words | Verdict |
|---|---|---|---|
| `--mutation slow-adp-rx` | a 16,000-iteration loop after `adp_rx`, in a scratch firmware copy (`build.py:39`) | `BUDGET control.discover.if0: 24.614 ms over T_svc 10 ms`; the unplanted image measures 0.294 ms | `CONTROL slow-adp-rx caught: every control path missed T_svc`, rc 0 |
| `--cpu-regions as-built` | the CPU generated from the SoC's 224 KiB regions | `REFUSED boot-fault: the CPU trapped or saw a bus error: ['TRAP 330592 0 1 00006880', ...]` | `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 |

An escape prints `CONTROL <name> ESCAPED: ...` and returns 1.

History, stated plainly: the first slow-adp-rx run (`receipts/measured-drivers/C-slow.log`) printed `ESCAPED: 1 of 3 control paths missed T_svc`, rc 1.

- The verdict then counted the group's two setup probes, LINK_UP and TMR_DELAY, which the plant does not slow.
- The verdict now counts only the group's `control.`-named paths (`run.py:130`).
- The planted path itself measured 24.614 ms, over T_svc, in both runs. No threshold or plant changed.

## 5. Gate table

Every gate ran at the head `d58c8e22`, in the foreground and unpiped. The logs are in `receipts/gates/`, with the rc on each log's last line, and `HEAD.txt` records the head.

| Gate | Command | rc |
|---|---|---:|
| Harness self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | 0 |
| BDD conformance (rtl-fast) | `cd tests && behave`: 14 features, 406 scenarios, 1977 steps | 0 |
| Docs wording and links | `python3 scripts/docs_check.py` | 0 |
| Doc cited paths | `python3 scripts/check_doc_paths.py` | 0 |
| Doc style, and its self-test | `python3 scripts/check_doc_style.py`, `--selftest` | 0, 0 |
| Archive, and its self-test | `python3 scripts/check_archive.py`, `--selftest` | 0, 0 |
| Em dash, and its self-test | `python3 scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f` (364 added lines judged), `--selftest`, in the pinned Markdown renderer env | 0, 0 |
| Per-page contents | `python3 scripts/gen_toc.py --selftest`, `--verify-anchors`, `--check`, in the pinned renderer env | 0, 0, 0 |
| Python idiom, and its self-test | `python3 scripts/check_py_idiom.py`, `--selftest` | 0, 0 |
| C++ idiom, and its self-test | `python3 scripts/check_cpp_idiom.py`, `--selftest` | 0, 0 |
| Hygiene | `python3 scripts/check_hygiene.py --check` | 0 |
| TODO ownership | `python3 scripts/check_todo_ownership.py` | 0 |
| SoC sources | `python3 scripts/check_soc_sources.py` | 0 |
| RTL source lists | `python3 scripts/check_rtl_source_lists.py` | 0 |
| Whitespace | `git diff --check e76a755a HEAD` | 0 |
| Regrade at the head, 4 arms | `run.py --point P --build-dir B --reuse-build --regrade [--variant answering-ports] --record-budget-findings --out O` | 0 each, 0 refusals |
| Controls, 2 | section 4 | 0, 0 |

The full serial sweep was not run. The lane adds only new files under `tb/verilator/`, and no shared file changed, as the brief allows.

## 6. Run history and reproducibility

The driver logs in `receipts/measured-drivers/` record the measuring runs as they happened:

- The first full runs refused the three MAAP PROBE probes at each interface (`unexpected response: no MAAP type 1`) and the owed row (`no origin`), rc 1 (`A1-short.log`, `A8-long.log`).
- They also printed misses from the first `backlog-adp` design (`A1-short.log`).

Fixes followed in the grader (transmit-record decode) and in the scenario (the owed row fills the TX ring first; `backlog-adp` takes a GM-matched AVAILABLE). The redesigned groups were rerun (`*-backlog.log`, `*-badp.log`, `*-control.log`), and every group's last log was regraded (`*-regrade.log`).

At the head, that regrade was repeated with the committed grader:

- It refuses any group whose recorded script the committed scenario no longer generates. It refused none, so every graded log came from the committed scenario.
- Every grade, `table.md` and `results.json` is byte-identical to the measuring regrade's (`receipts/head/*-regrade.log`).

Each measured build was also rebuilt at the clean head into a fresh directory (`receipts/head/repro-compare.txt`, `h-*.log`). The builds were 1x1, 8x8, both arm-B builds, the slow control and the as-built control. In each:

- the native model's sha256, the ELF and `budget_config.hpp` are identical;
- `sim.v` differs in its two LiteX date lines.
- In the arm-B 1x1 rebuild only, it also differs in two lines of LiteX's header hierarchy comment, which lists the black boxes `KL_mbx` and `KL_mbx_wb` in the other order (`receipts/head/repro1v-sim-diff.txt`). The comment is not compiled, and the model is byte-identical.

The two controls were rerun at the clean head on those builds (`receipts/head/C-slow.log`, `C-asbuilt.log`); both are caught, rc 0.

## 7. Defects found, each for its own issue

1. **The split image cannot run on the CPU the split SoC builds.**
   - The CPU generator decodes a region whose size is not a power of two wrongly. For the 224 KiB `rom` at 0 the fetch and load checks are `(address & 0xfffc8000) == 0`, which excludes every address with bit 15 set.
   - Generated from the shipping split region list, the decode is the same (`receipts/pma/pma-decode.md`).
   - The image's first call above 0x8000 (`jal aecp_image_load`, 0x6880 to 0xb1ec) takes an instruction access fault, cause 1, and restarts forever.
   - Recommendation: a new issue for the split SoC (the region sizes in `ctrl_memory.py` / `milan_soc.add_ctrl_memory`) or for the generator pin, before M8a-2's boot.
2. **The linked image addresses placeholders.**
   - The image uses `CTRL_MBX_BASE=0x80000000u`, LiteSPI master 0xf0003000, timer0 0xf0003800 and flash 0x20000000.
   - The split SoC uses 0x90100000, 0xf0002810, 0xf0003000 and 0x01000000.
   - S3's target firmware owns the real addresses. The cost of an access does not depend on its address.
3. **#723 is open.**
   - The runtime recipe builds without `-fno-stack-protector`, so the image does not link with the pinned SDK.
   - `runtime_ssp.py` is the workaround. Remove it when #723 lands.

## 8. Open risks and questions

- Each probe measures one phase. The reported pass bound covers every phase under the same passes, but not other loads.
- Not run:
  - SHUTDOWN, which has no input in the fixture;
  - START_STREAMING, which calls a port the fixture leaves empty.
- The fixture's sources are never allocated, so Listener Ready grants no licence.
- Ends are mailbox commits. Wire time, ingress and egress, and the network round trip are not in the figures.
- Flash erase and program waits are zero, so F1's commit is CPU work only. S4 owns the target port.
- The firmware polls (`CTRL_MBX_WFI` undefined), as the fixture is linked.
- The self-test is portable, but no CI job runs it, because registering it is a CI change outside this lane. A follow-up is recommended.
- Arm B changes test code only. Its figures are labelled and are not the formal result.
