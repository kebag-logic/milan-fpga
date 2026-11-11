[R822] NEGATIVE - exact head b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702

# R822-1: external review of PR #881 (issue #871, Mark II split S11, AECP REBOOT on the CPU)

- Head `b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702`, tree `d8f59879fc1cd1fbf2553155fd89b05ca32b63f5`, six commits on `dev-soft-core` `1d6bf555`.
- Cleared-context external review. Public scope only: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #871 body and its two public comments, plan decision D9 and the S6/S11 rulings in #665, `docs/design/REBOOT_RESET.md` (#787), the processor's REBOOT contract (`protocol-processor/docs/architecture/06_aecp_engine.md` section 6.11, `03_packet_engine.md` REBOOT gate), the diff `1d6bf555..b29f94d7`, and the author's published receipts at archive `5cbba57e` (`review-evidence/665s11-r1/author/receipts`). The handoff page in that archive was not read.
- Prior public review findings on this PR: none. At review time the PR carries only the two review-start comments for R821-1 and R822-1 and no review objects, so there is nothing to resolve or retain.
- Verdict: **NEGATIVE**. One MAJOR and two MINOR findings are open, plus one RESIDUE and four SUGGESTIONs.

## What I ran at the exact head (receipts under `receipts/`)

| Run | Result |
|---|---|
| `test_ctrl_firmware.py --jobs 4` (host gate, no self-test) | PASS: 56 arms, 0 failed; `platboot` if1 and if2 include B11 to B18 (`host_firmware.log`) |
| The 11 REBOOT defects of `aecp_mutants.py`, through its own `campaign()` (`scripts/reboot_aecp_mutants.py`) | 11 of 11 caught, each by its named test on its own words (`reboot_aecp_mutants.log`) |
| The 10 REBOOT defects of `plat_mutants.py`, plus the moved `plat-loop-before-ready`, through `ctrl_mutants.campaign()` (`scripts/reboot_plat_mutants.py`) | 11 of 11 caught on their named words (`reboot_plat_mutants.log`) |
| `publication_census.py --check --selftest` with the pinned sv2v v0.0.12 and Yosys 0.66 | rc 0: 6 shapes, 246 checks, 0 failures; 0 of 164 self-test arms failed; 0 of 57 rules unproven. The REBOOT arms are refused on their own words: port census "read past its terminal", split "from another port" and split "tied off" (`publication_census.log`) |
| `tb/verilator/ctrl_reboot/run.py --self-test`, pinned Verilator 5.050, `PYTHONHASHSEED` unset (the PR's documented command) | **rc 2, REFUSED**: "the SoC's csr.csv depends on the image". The cause is `config_cpu_isa` extension order across export processes (finding F3; `reboot_sim_hashseed_refusal.txt`) |
| The same, with `PYTHONHASHSEED=0` | rc 0, PASS, 9 of 9 plants and controls. Every figure is identical to the author's receipt: REBOOT RXE 142044928, SUCCESS 142261495, notification 142275859, DEPARTING 142424819, port 142490635; 445,707 bus or 222,853 CPU cycles; drain 582.094 ms durable; first AVAILABLE 4,590.218 ms of 20,000 ms (`reboot_sim_pythonhashseed0.log`) |
| A disposable host probe appended to `test_plat_boot.cpp`, then removed (`scripts/run_probe_window.sh`, `probe_window.cpp.inc`) | A BIND_RX received after the SUCCESS has left the mailbox, but before the port, **is applied and answered**. Its ACMP and SRP frames leave after ENTITY_DEPARTING, then the port fires (finding F1; `probe_window_if1.out`, `probe_window_driver.log`) |

After every probe the clone was restored and checked:

- `HEAD` is `b29f94d7`, and the worktree and index both equal `HEAD`.
- The `git ls-files -s` digest equals the `HEAD` tree digest (`80b5a7ab...`), modes and gitlinks included.
- No file is untracked, and none is marked assume-unchanged or skip-worktree.
- The gitlinks are unchanged: protocol-processor `a9e84b66`, gptp-processor `135afd04`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8`, tsn-c-stack `70936b77` (`external` uninitialised, as CONTRIBUTING intends).

## The focus points

1. **Statuses and the notification** (`sw/firmware/ctrl/aecp/aecp_commands.c:539-569`, `aecp.c:378-401`, `aecp.c:479-497`). These match the processor's REBOOT table (06 section 6.11) route for route.
   - A body shorter than Figure 7-68's four bytes gets BAD_ARGUMENTS.
   - Any type other than ENTITY gets NOT_SUPPORTED, because no MEMORY_OBJECT firmware image exists (7.4.43.1).
   - Any ENTITY index other than 0 gets NO_SUCH_DESCRIPTOR.
   - Another controller's lock gets ENTITY_LOCKED (7.4.43.2). A refusing state is mapped to ENTITY_MISBEHAVING through `aecp_foreign_lock`.
   - Otherwise the answer is SUCCESS. Every answer is at cdl 16, and short-body padding is zero (`header()` memsets the response, `aecp.c:66`).
   - The SUCCESS sets `notify`. `transmit()` then sends one u=1 copy to each registered controller other than the requester, on every interface, with that controller's own sequence_id (7.5.2; Milan v1.2 5.4.5.1, 5.4.5.2).
   - Without a port the command is NOT_IMPLEMENTED with its body echoed.
   - The host tests (`Core.Reboot*`, B13, B14), the REFUSE grade and the 11 AECP defects all hold this.
   - The clause texts themselves were not in the workspace. They were checked against the in-tree quotations and the processor contract (see Limits).
2. **Order.**
   - `aecp_poll` runs `transmit()` before it captures `reboot_end`, so the response and every notification are handed over first (`aecp.c:590-640`).
   - `aecp_reboot_due` waits for `tx_done` to reach `reboot_end`, and older completions are ignored (`aecp.c:200-203`, `453-456`).
   - The platform then disables ADP, waits for each `departing_owed` and for ADP's ring to drain, and writes the port once (`ctrl_plat.c:180-201`).
   - The measured CPU-simulation order reproduces exactly: SUCCESS, notification, DEPARTING, port.
   - **No AECP command is taken after SUCCESS** (`aecp.c:197`, defect `reboot-serves-after-its-success`). **ACMP and ADP commands are still taken** until the port fires. Frames other than ADP's can follow ENTITY_DEPARTING: finding F1.
3. **Port, crossing and census.**
   - `CtrlReboot` is one `CSRStorage(1)`, pinned at `n_locs - 3`, below the mailbox bank (`milan_soc.py:3171-3193`). It is added only under `--ctrl-mailbox`.
   - A `MultiReg` crosses it into `dp.milan_cd` (`milan_soc.py:3214-3216`), the clock the datapath's `axis_clk` is driven from (`milan_soc.py:861`). It lands on `i_i_reboot_req` → `i_reboot_req` (`milan_soc.py:1380-1383`).
   - The split branch drives `pp_reboot_req_w` from it alone (`milan_datapath.sv:10147-10149`), into the unchanged `KL_reboot_ctrl`. That block latches the level into DRAIN on the first cycle it reads 1 (`KL_reboot_ctrl.sv:277`).
   - The split's drain inputs come from `i_ctl_nvm`, the F_NVM that `quiet()` keeps publishing (`milan_datapath.sv:10037`, `ctrl_plat.c:332-347`).
   - The CDC census now counts 4 `MultiReg` call sites (`cdc_census.gen.py:120`; diagram regenerated). `CLOCK_DOMAINS.md:236` has the row.
   - `G_CARRIED` (`census_split.py:248-252`, `582-594`) holds the net to that one port, and both new plants are refused on their words.
   - The all-fabric build is unchanged by construction: the port is connected only under `ctrl_split`, the CSR only under `--ctrl-mailbox`, and the `CTRL_SPLIT_P = 0` branch never reads `i_reboot_req`.
   - `mailbox.yaml` is not in the diff.
4. **Journal** (item 4).
   - The REBOOT arrives 62 bus cycles after the write's erase, and all 14 page programs follow it. The last program is 434.8 ms after the erase, and the drain ends `durable`.
   - Every item reads back after the reset.
   - The cut run is cut 1 cycle after the first page program of its write, and its replay reads the saved snapshot whole.
   - `write-torn` and `plat-reboot-stops-the-store` are refused on their words.
   - B16 holds the same on the host model.
5. **Item 1 is honestly partial.**
   - The shipping shape has one configuration and one AUDIO_UNIT rate (48 kHz), so those two items read back unchanged and are reported NOT RUN, not graded.
   - The other six items and the binding pass the #396 grader `check_release_state_restored`.
   - The PR body says "Relates to #871 (not closed ...)", and no commit message says Closes.
6. **Plants and mutants.**
   - The AECP defects (11/11), the platform defects (10/10 plus the moved anchor), the census REBOOT plants (3/3) and the CPU simulation's five controls are each refused by their own words.
   - The CPU plants `request-ignored`, `write-torn` and `any-descriptor-type` are refused by their own words.
   - **`reset-before-the-response` is not**: its SUCCESS and notification still leave before the port. It is caught only by the DEPARTING-order and frame-after-port words (finding F2).
7. **S2 harness.**
   - At 8x8/2if the head's `acmp.probe_tx.if1` is 13.602 ms, run with `--record-budget-findings`, rc 0, "57 T_svc misses (... 29 of 129 paths)" (author receipt `s2_8x8.log:341`). It is recorded and not graded, and its budget belongs to S2b (#810).
   - The base figure (5.416 ms) and "31 at the base" have no published receipt (SUGGESTION S2).

## Acceptance (#871, frozen)

| # | Status at this head | Evidence |
|---|---|---|
| 1 | Partly met, and stated as partial | CPU simulation RESTORE PASS over 6 items and the binding; configuration and rate NOT RUN; first ENTITY_AVAILABLE at 4,590.218 ms against the 20,000 ms valid time (Milan v1.2 5.6.2), with TMR_DELAY 500.667 ms after the reset inside Table 5.50's 4 s |
| 2 | Met (mutant evidence: host) | Host defect `plat-reboot-before-the-response` fails B12 "no reset while the mailbox holds the response"; AECP defect `reboot-due-before-its-frames-complete` fails "not due before the response has left"; CPU ORDER grade and its control `response-after-the-port`. The CPU plant cited for this item does not show it (F2) |
| 3 | Met | `request-ignored` (ORDER: never fired, NOREQ), `plat-reboot-ignored` (B11, B15, B16), `reboot-never-accepted` |
| 4 | Met | As focus point 4 |
| 5 | Met | REFUSE grade, B13, `Core.RebootRefusalsLeaveTheEntityInService`; plant `any-descriptor-type`, defects `reboot-any-descriptor-type`, `reboot-any-entity-index` |

Measurements: the request-to-reset bound reproduces exactly (445,707 bus cycles, 222,853 CPU cycles, 4.457 ms). I did not re-measure the linked-size delta (+868 B ROM). The ledger value 21,272 B is consistent between `ctrl_memory.py`, `ctrl_memory_ledger.py` and `SPLIT_CONTROL_MEMORY.md`.

## Findings

### R822-F1 MAJOR: Between the REBOOT's SUCCESS and the reset port, the split still takes ACMP and ADP commands and sends their frames after ENTITY_DEPARTING

- **Lenses:** Conformance, RTL (architecture: the split must keep the contract of the processor it replaces), Robustness, Tests, Docs.
- **Where:**
  - `sw/firmware/ctrl/plat/ctrl_plat.c:348-356`: the full `ctrl_loop_step` runs until `reboot == 2`.
  - `sw/firmware/ctrl/plat/ctrl_plat.c:180-201`: no lane is gated between acceptance and the port.
  - `sw/firmware/ctrl/aecp/aecp.c:197`: only AECP refuses.
- **Authority and evidence:**
  - The processor's REBOOT contract, which the lane adopted, says: "the top discards, whole, every frame that starts on `rx_*` after it, so no ACMP, ADP or AECP command reaches an engine". It also says "after the final ENTITY_DEPARTING nothing is sent until the reset" (06 section 6.11; `03_packet_engine.md:494`, REQ-FWX-001). The processor's RBT7 and RBT9 grade both.
  - The lane's TAKEN comment says the AECP owner answers "as 7.4.43 and the processor do" and "takes no further command". `REBOOT_RESET.md:270` says "No command is taken after it". The PR says "No command after it".
  - Probe (`receipts/probe_window_if1.out`), the B12 shape: the response is released and the mailbox is held at ADP's DEPARTING commit. Then a BIND_RX arrives.
    - It is applied (`sink.bound` 1) and answered: 2 ACMP frames.
    - The mailbox order is AECP SUCCESS, ADP DEPARTING, ACMP, ACMP, two channel-4 frames, then the port write.
  - The author's own CPU receipt shows the same window. The `reset-before-the-response` plant's "a frame given after the reset port fired was taken" is the `after-port-bind` BIND_RX, served because the loop still ran.
  - The difference is not in `aecp/README.md:303`'s observed-differences table.
- **Impact:**
  - For as long as the response or the DEPARTING waits in the mailbox (2.3 ms here, unbounded under backpressure), a controller's ACMP command changes and persists state and is answered, after the entity accepted its reset.
  - ACMP, SRP and MAAP frames can reach the wire after the entity's own ENTITY_DEPARTING, which controllers have acted on.
  - The split placement differs from the all-fabric placement on the wire, with no record.
- **Tests:** B11 (`test_plat_boot.cpp:41`, `585-587`) and the ORDER grade (`run.py:256`, `549`; `README.md:77`) claim "no command answered after the SUCCESS". Each sends only an AECP GET_CONFIGURATION after the SUCCESS and a BIND_RX after the port, so nothing tests the window.
- **Required outcome:** either
  - (a) from the REBOOT's acceptance the platform takes no ADP, ACMP or AECP command, and from the commit of the last ENTITY_DEPARTING it commits no frame but ADP's until the port, as the processor does. A host test and a CPU-simulation grade send a non-AECP command in the window, each with a plant refused on its own words; or
  - (b) a recorded maintainer decision accepts the difference. It is then entered in the observed-differences table and in `REBOOT_RESET.md` section 8, and every "no command after the SUCCESS" claim is narrowed to AECP.
- **Verification:** `scripts/run_probe_window.sh` at the corrected head reports `sink.bound` 0 and no ACMP frame, and its plants fail. Or, under (b), the decision and the narrowed text are linked.

### R822-F2 MINOR: The CPU simulation's `reset-before-the-response` plant does not fire the reset before the response, and is refused by other words

- **Lenses:** Tests, Docs.
- **Where:** `tb/verilator/ctrl_reboot/run.py:650-654` (the plant), `run.py:730` (the self-test matches the grade prefix only), `tb/verilator/ctrl_reboot/README.md` (the plants table), and the PR body's item-2 row.
- **Evidence:** in my run and in the author's receipt the plant produces no "SUCCESS left the mailbox after the reset port fired" finding and no notification-count finding. The response is committed in `aecp_poll` before the console poll writes the port. The plant is caught only by "ENTITY_DEPARTING did not leave between the notification and the reset port" and "a frame given after the reset port fired was taken".
- **Impact:** the item-2 evidence row cites a mutant that never puts the reset before the response. Item 2 is still evidenced on the host by `plat-reboot-before-the-response` (B12, its own words).
- **Required outcome:** either
  - the plant reproduces its named defect, so the port fires before the SUCCESS leaves the mailbox, and is required to give that finding; or
  - it is renamed, and the PR's item-2 row and the README restate what it proves.

  In both cases `plant_point` requires each plant's expected finding text, not just its grade.
- **Verification:** `run.py --self-test` prints the plant caught with the response-order words.

### R822-F3 MINOR: The REBOOT simulation's verdict depends on Python hash randomisation

- **Lens:** Tests.
- **Where:** `tb/verilator/ctrl_reboot/run.py:356` compares every `csr.csv` row of exports made in separate child processes (`run.py:299-306`).
- **Evidence:**
  - LiteX's VexiiRiscv builds `config_cpu_isa` from a Python `set` (`isa_map`), so the extension order follows each process's hash seed.
  - The PR's documented command, run at the exact head with no seed exported, exited 2 (REFUSED). The rows differ only as `rv32i2p0__zicsr_zifencei` against `rv32i2p0__zifencei_zicsr` (`receipts/reboot_sim_hashseed_refusal.txt`).
  - With `PYTHONHASHSEED=0` it passes with identical figures.
  - The sibling harness pins the seed (`tb/verilator/ctrl_service_budget/run.py:320`, `build.py:757`).
- **Impact:** the acceptance evidence for items 1 to 5 is not reproducible by its own documented command. A run can refuse or pass by chance.
- **Required outcome:** the harness pins the seed for every export, or compares only the rows the image's map is generated from.
- **Verification:** two runs of the documented command, with no seed in the environment, both pass.

### R822-R1 RESIDUE: MAILBOX_SPLIT.md's "Default build" still describes one added CSR bank

- **Lens:** Docs.
- **Where:** `docs/design/MAILBOX_SPLIT.md:1594-1598`.
- **What is wrong:** the paragraph says the switch adds "a CSR bank pinned below the existing observer's page so no existing bank moves, and one interrupt". At this head it also adds `ctrl_reboot` below the mailbox's bank.
- **Exact fix:** "..., a CSR bank pinned below the existing observer's page so no existing bank moves, the REBOOT reset port's one-bit bank pinned below that (#871), and one interrupt."

### SUGGESTIONs (do not affect coverage)

- **S1 (Tests).** The cut and replay leg of JOURNAL (`grade_cut`) has no grader control. Add one that edits the replay log to a mixed snapshot.
- **S2 (Docs).** Publish the base `results.json` and the `s2_compare.py` output behind "5.416 ms at the base" and "31 at the base". Only the head side is receipted.
- **S3 (Docs).** The generated CDC census row still reads "single-bit status/IRQ levels" (`cdc_census.gen.py:122`), but a request level now crosses there too.
- **S4 (Robustness).** The firmware's wait from SUCCESS to the port has no bound: a datapath that never completes a frame keeps the entity mute and unreset. This is stated in the PR's limits and matches the processor. A bound, or a line in `REBOOT_RESET.md` section 8, would make it durable.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `aecp_commands.c:539-569`, `aecp.c:197-203,378-401,453-456,467-497,590-640` against Figure 7-68, 7.4.43.1/.2, 7.5.2, Milan 5.4.5.1/.2 and the processor contract 06 section 6.11; `ctrl_plat.c:180-201,332-356` against Milan 5.6.3.3; CPU-simulation REFUSE, ORDER and ADP figures reproduced; the probe | R822-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| RTL | UNCLEAN (F1, architecture) | `milan_datapath.sv:613-618,10037,10147-10149,10177-10195`; `KL_reboot_ctrl.sv` (unchanged; level latched at `:277`); `milan_soc.py:861,1377-1383,3171-3216`; `census_split.py:248-252,582-594`; `census_ports.py:59-69`; `cdc_census.gen.py:107-125`; census rc 0 (246 checks; 164 arms; REBOOT plants refused). Clean within RTL proper: CSR width and pin, the MultiReg domain, the single driver, the all-fabric branch unread, no `mailbox.yaml` change | R822-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| Robustness | UNCLEAN (F1) | Commands during the REBOOT window (probe); held response, full ADP ring and refused DEPARTING (B12, B18 and their defects); short, padded, other-type and other-index bodies; lock and refusing states; no port (B14); older completions; reentrancy (`Core.RebootIsAnswered...`); journal write in progress and cut; reset after the port (B17) | R822-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| Tests | UNCLEAN (F1, F2, F3) | Host gate PASS (56 arms); 11/11 AECP and 11/11 platform REBOOT defects on their own words; census self-test 0/164 failed; `ctrl_reboot --self-test` 9/9 with the seed pinned, REFUSED without it; plant and control word analysis (`run.py:640-760`) | R822-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| Docs | UNCLEAN (F1, F2; R1 is RESIDUE) | `REBOOT_RESET.md:23,260-297`; `MAILBOX_SPLIT.md:1176-1188,1477-1491,1594-1598,1878-1886`; `CLOCK_DOMAINS.md:236`; `SYSTEM_INTEGRATOR.md:41`; `INTEGRATION_GUIDE.md:80`; `check_solution_docs.py:181-185`; `SPLIT_CONTROL_MEMORY.md:97`; `aecp/README.md:154-166,303`; `plat/README.md:81-83,121-130`; `ctrl_reboot/README.md`; PR body and #871 comments; no em dash added; commits one line, no trailers | R822-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |

Comment rule (owner 2026-10-15):

- The added source and test lines carry no lane label, review round, reviewer ID or issue-comment ID.
- The test IDs `B11` to `B18` in `test_plat_boot.cpp` and `plat_mutants.py` continue the base file's `B1` to `B10` test-case numbering (65 base occurrences), and the mutant table matches assertions by them. I read them as test identifiers, not bench lane labels. The manager should rule if the owner's `B17` example is meant to cover them; if so, they are RESIDUE alongside #746.
- Plan-stage names (`S11`, `S12`) appear only in design-doc and README prose, as at the base.

## Real limits

- The IEEE 1722.1-2021 and Milan v1.2 texts were not in the workspace. Clauses were checked against the repository's quotations and the processor's documented contract, not the standard's pages.
- The CPU simulation builds no datapath: "on the wire" is the mailbox's transmit face. Its `KL_reboot_ctrl` is a testbench model with a 1,000 ms drain cap and 50 ms of the 3,500 ms hold. The IPROG word and the configuration load are not simulated.
- I did not re-measure the all-fabric gateware-export identity, the linked-size delta, the four-shard sweep, `fw_coverage.py`, `behave`, `test_builder.py`, the docs workflow or S2 at either point, either the base or the head. For those I read the author's receipts. No manager source bank ran at this head, and I claim none.
- Physical calibration is NOT RUN. No hardware was used, and field skips are not hardware proof.
- Hosted contexts at this head, read once at about 07:50 CET: many jobs passed, among them `elaborate`, `publication-census`, `split-cdc`, the firmware jobs and most Verilator shards. Yosys shards 0 to 3, `yosys-elaboration` and `verilator-lint` were queued, several Verilator shards were in progress, and `Physical gPTP (nightly and manual)` was skipped. That is a reading, not acceptance.

## Pending manager duties

- Rule on F1's (a) or (b), and re-review the corrected head with every lens re-covered where its scope changed.
- Carry R822-R1, and the `B11` to `B18` question, to the residue checklist.
- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `46c971fa`) with the builder and native banks at the merge turn, and link its receipts on the PR.
- Own hosted and act acceptance at the exact head, once the queued Yosys and lint contexts finish.

R822-1 FINISHED
