# HANDOFF — lane P2 round 2 ([A502])

**Status: REVIEW READY.** All six items are done in order, and every gate in section 4 is rc 0 at the head.

- Branch `p2-nvm-port-robustness`, round-1 head `70bf017d62d60b4401126c7b1bb087f4cb115c5a`.
- Round-2 head `c26b14b316f14abdbe1080f2649f7df83bce061a`, local only: this lane does not push.
- Assignment: processor #15 comment 5956438390, items in order. Reviews: R436-1
  (PR #145 comment 5956427403) and R437-1 (5956174225).
- Posted on #15: TAKEN, comment 5956443297 (2026-10-02 16:14Z); REVIEW READY, comment 5959067531 (2026-10-02 18:45Z).
- Every `file:line` below is at the round-2 head unless it names another revision.

| Commit | Subject (abridged) | Item |
|---|---|---|
| `e42870e` | Assert T1's erased tail only on a backend with erase semantics, a harness switch both lazy-erase rows set | 1 |
| `6b6f309` | Grade the owed command's end and drain from a waiting request in tb/nvm_port T28, with D18-D23 as figures-gate rows | 2, 3 |
| `ff2cce1` | Pause the NVM port's deadline count on a cycle that owes nothing, and owe nothing in a wait state whose terminal is latched; T29 with D24-D26 | 4 |
| `06db35e` | Derive every tb/nvm_port wait that meets the deadline from TMO, build the suite a second time at 37, figures gate requires both builds | 5 |
| `36abf30` | The reviewers' R1 wording | 6 |
| `c26b14b` | `-Wall -Wextra` on the per-build `-CFLAGS` group, as the parent's C++ idiom gate requires | the parent gates |

Commits 1 to 5 each passed `make -C tb/nvm_port figures` (rc 0) at their own tree before the
next began. The full gate set ran at the head (section 4).

STOP conditions: no port changed on any module, and no parameter beyond the ruled two
(`MEM_TIMEOUT_CYC_P`, `NVM_MEM_TMO_CYC_P`) was added. `git diff 70bf017d..HEAD` touches 10
files: the port RTL, the top (one comment word), `tb/nvm_port` (sim_main, README,
measure_figures, Makefile), 02, 08, 09 and the integrator guide.

## 1. Findings, the change for each, and the check that fails without it

### R436-1 F2 = R437-1 F1 (MINOR): #21 item 4 unmet, T1 red under lazy erase. Outcome (a)

**Changes:**
- `tb/nvm_port/sim_main.cpp:929`. T1 asserts the erased tail only on a backend with erase
  semantics: `h.lazy_erase || store[3][32] == 0xFF`. Its bus checks are unchanged (`:917-922`):
  - `T1 op0 = ERASE region 3 len 0`;
  - `T1 erase pulsed region 3 once`.
- `:197-202`, `:489`. Lazy erase is the harness's own switch, `lazy_erase`; ERASE leaves the
  array when it is set.
- `tb/nvm_port/measure_figures.py:486`. `_LAZY` sets the switch, and both lazy-erase rows
  use it. Before, the model was a code edit spliced in from the gate.
- `tb/nvm_port/README.md`. The model table: both lazy rows now read **343 PASS, 0 FAIL**
  (`:991-992`). The array rule's `done` clause and its single exception; the count of
  array-dependent sites (18: 3 condition on the array, 1 on erase semantics, 14 neither);
  the `err` clause list; the "Covered:" line.

**Contract served:** #21 item 4: "the existing checks stay green under every model the port
is contractually required to tolerate". Lazy erase is one, by the banner's own words
(`KL_pp_nvm_port.sv:33-34`).

**What fails without it:**
- At `70bf017` both lazy rows measured 325/1, `T1 erase visible past the record`. Both
  reviewers and the round-1 gate record it.
- At `e42870e` both rows measure 326/0. At the head they measure 343/0, and also 343/0 at
  the second bound, 37.
- Measured at the head (scratch probe, the build at 100): T1 with its condition removed
  gives 342/1 under lazy erase, `T1 erase visible past the record, on a backend with erase
  semantics`. Under pristine it gives 343/0. The condition is live in CI, because the
  pristine model asserts the erased tail.

### R436-1 F1 (MINOR): three planted defects in the owed-command logic pass all checks

### R437-1 F2 (MINOR): X12, X17, X18, X24 not pinned

**Changes.** `tb/nvm_port/sim_main.cpp`, T28 in two functions:
- `owed_terminals_are_credited_to_no_operation`, `:2159-2213`;
- `owed_events_restart_a_waiting_request`, `:2220-2262`.

Each case starts the next operation while the device still carries the abandoned command.
The helper `wait_on_owed`, `:2140-2148`, requires the port busy, the device owing, and no
command taken. The cases:

| Check | Scenario | Contract (banner `KL_pp_nvm_port.sv:85-99`, 02 §8) | Planted defect it kills |
|---|---|---|---|
| T28a `:2172` | owed payload READ ended by err while a restore waits in `S_RHREQ`; restore served byte-exact | the owed command's done or err is its end, "credited to no operation" | D18 = W15 = X24 (`S_RHREQ`'s `if (!owed_r)` removed): 1 of 343 |
| T28b `:2186` | owed ERASE ended by err while a commit waits in `S_WEREQ`; commit served | same | D19 = W15b: 1 of 343 |
| T28c `:2201` | WRITE abandoned in `S_WWAIT` (done three deadlines late); next commit requests nothing, ends DEADLINE; served after the done | "a deadline in any state that owns a command leaves it owed" | D22 = X12: 2 of 343 (T28c, RW3) |
| T28d `:2240` | owed READ drains one byte every `TMO` / 2 for more than ten deadlines while a restore waits; served, never DEADLINE | "every grant, byte and terminal restarts the count" (the drained bytes) | D20 = W16 = X18: 1 of 343 (3 of 343 at 37) |
| T28e `:2257` | owed ERASE's done three fifths of a deadline into a restore's wait, grant three fifths later; served | the owed terminal is progress | D21 = X17: 1 of 343 |

`measure_figures.py:381-399` holds the rows D18-D23. D23 removes the `S_WWREQ` and
`S_RPREQ` guards together and fails 0. It is measured as an equivalence: a command becomes
owed only as an operation ends, so the next operation meets it in `S_WEREQ` or `S_RHREQ`.
R437-1's X24b, all four guards removed, is killed by D18 and D19.

**Docs:**
- the README's T28 bullet and the D18-D23 list (`README.md:510-525`, `:569-587`);
- "T24 grades all of it", now "T24, T28 and T29";
- every figure re-measured; the mutation count is fifty-nine;
- 09 §8.5, two rows: T28c with D22 in the owed-state row, and a new row for T28a, T28b,
  T28d, T28e with D18-D21 and D23.

### R436-1 S1 (SUGGESTION, taken as item 4): the watchdog cleared rather than paused

**The count**, `hdl/packet_engine/KL_pp_nvm_port.sv:278-282`. It restarts on `prog_w` (a
grant, byte, err or owned/owed done) and is zero in `S_IDLE`. It counts a cycle with
`owe_w`, and holds on any other cycle.

**A wait state whose terminal is latched owes nothing**, `:258-260` (`&& !done_seen_r`).
Without this term the pause breaks the coincident model, a contract freedom:
- the header READ's done rides its eighth byte;
- `S_RHWAIT`'s consuming cycle counted;
- the pause carried that count across `S_RHFWD` into `S_RPREQ`;
- so the tolerated grant at `TMO` was refused.

The reviewers measured W6 under the pristine model only. Measured here under the coincident
model, it fails 5 (T24 S_RPREQ's tolerated arm, its timing and late-grant checks, the slow
restore, RW4).

**Banner and comments**, `:69-83`, `:247-250`, `:273-275`. They are rewritten at the same
line count, so every line citation stays valid.

**Contract served:** R436-1 S1 and the assignment: "no manager handshake pattern can keep a
silent device from the deadline; every grant, byte and terminal still restarts the count".

**Check that fails without it:**
- T29 (`a_manager_strobe_never_holds_the_deadline_off`, `sim_main.cpp:2105-2134`):
  - T29a: a manager drops `rready` one cycle in `TMO` / 2 against a payload READ whose
    10th byte never comes;
  - T29b: the same with `wvalid`, against a WRITE whose 20th byte is never taken.

  Each requires one err, DEADLINE, with pulse gap == `TMO` + 2 + the held cycles (> 0).
- The harness counts the held cycles: `mgr_drop_every`, `held_since_evt`, `pulse_held`
  (`:298-301`, `:260`, `:675-703`).
- Rows, at both bounds:
  - D24, the round-1 count, cleared on every cycle owing nothing: 3 (T29a, T29b, RW1:
    both operations unanswered);
  - D25, not zeroed between operations: 7;
  - D26, the latched-terminal term removed: 0 pristine, and 5 under the coincident model
    (D26/coincident);
  - D4 re-anchored: 38.

**Docs:**
- 02 §8 (`02_interfaces.md:530-552`);
- F08.1's `T-NVM-PORT-DEADLINE` row, value and description (`08_timing.md:46`);
- the integrator guide's `NVM_MEM_TMO_CYC_P` row (`integrator.md:99`);
- the top's parameter comment (`protocol_processor_top.sv:165`);
- 09 §8.5's new pause row;
- the README's deadline section, the T29 bullet and D24-D26.

### R436-1 S2 (SUGGESTION, taken as item 5): harness constants not derived from TMO

**`TMO` comes from the Makefile.** `sim_main.cpp:48-55`: `TMO = NVM_PORT_TMO`, which the
Makefile passes per build, with `static_assert(TMO >= 20)`.

**Derived waits.** `:63-68` and their uses. Each keeps its old value at 100, so no figure
moved:

| Wait | Was | Now |
|---|---|---|
| `kOpTimeoutCycles` | 100,000, which failed the variant at 1,000 | `1000L * TMO` |
| `kDrainCycles` | 30 | `3 * TMO / 10` |
| `kStageCycles` (T6's poke, T25's stages b, c, f, T25g/h) | 40 | `2 * TMO / 5`; the midpoints `/4`, `/2` |
| T6's `op_delay` | 30 | `3 * TMO / 10` |
| the served branch's late resume | `TMO + 60` | `TMO + 3 * TMO / 5` |
| strays' spacing | 30 | `3 * TMO / 10` |
| `power_cut`'s window | 50 | `TMO / 2` |
| T25g/h's window | 60 | `3 * TMO / 5` |
| T27's first-command wait | 200 | `2 * TMO` |

**`tb/nvm_port/Makefile`:**
- `TMO = 100` and `TMO_ALT = 37`;
- the `suite` macro builds into its own `--Mdir`;
- `run` runs the elaboration guard, then both builds; each appends its tally to
  `obj_dir/build_tally.txt` (`NvmPortSuite::report`, `sim_main.cpp:2596`), and an `awk`
  line prints the sum;
- `primary` is the build at `TMO` alone.

**`measure_figures.py`:**
- every row is measured with `make primary` (`:628`);
- `both_builds_disagree` (`:644-659`) requires `make run` to give exactly
  `[(343, 343, 0), (343, 343, 0), (686, 686, 0)]`.

**README:** the opening paragraph, and a "Two bounds" section (`README.md:605-632`).

**Contract served:** R436-1 S2, "derive the harness timing constants from `TMO`, and run a
second build at another legal bound".

**What fails without it:** at `70bf017`, built at 37 the suite failed 4 checks (T24's "a
commit meanwhile ends DEADLINE", T25h twice, RW4), and at 1,000 it failed 3 (T24's two
manager-stall checks, RW1). Both reviewers measured this. At the head the second build is
343/343 and is part of `make`.

### RESIDUE R1 (item 6)

**R436-1's exact text,** `tb/nvm_port/README.md:899-902`: "The first of those is
coincident completion: the device raises `dev_done_i` on the same edge that moves a pump's
final byte, which `KL_pp_nvm_port.sv:319-323` says the sticky `done_seen_r` latch exists
for."
- The sentence matches the reviewer's verbatim, in the whitespace-normalised README.
- The `:319-323` citation is still exact, because the RTL kept its line count.

**R437-1's R1, in the same sentence pair:** "below" becomes "above".

**Not taken:** R437-1's R2-R5 were not assigned. They stay for the residue checklist.

## 2. Per item: models and mutations, with the check each reddens

**Item 1.** The models at the head (the figures gate; `fastfig` scratch copies at 37):

| model | at 100 | at 37 |
|---|---|---|
| pristine, half-page, page-buffered NOR, lazy erase, lazy + page-buffered, coincident, unsolicited | 343 PASS, 0 FAIL each | 343 PASS, 0 FAIL each |
| short read (broken) | 265 PASS, 78 FAIL, every RW check passes | 265 PASS, 78 FAIL, every RW check passes |
| silent (broken) | 115 PASS, 228 FAIL, every RW check passes | 115 PASS, 228 FAIL, every RW check passes |

**Items 2 and 3.** D18-D23 above (fails of 343 at 100; at 37 the same, except D20, which
fails 3).

**Item 4:**
- **the rows:** D24, D25, D26, D26/coincident and D4 above;
- **W6 measured as the reviewers planted it:** pristine 326/0, coincident 321/5;
- **round-1 rows that moved with the pause** (fails of 343): D1 64, D2 35, D3 39, D5 4,
  D6 3 (the T29 arm in that pump now fails as well), D8 35, C1 65, M1 65, M3 117, and the
  latch deletion under coincident 216.

**Item 5:** the second build itself (343/343). The figures gate refuses unless both builds
pass.

**Every row of the figures gate at the head:** 12 arms, 59 mutations and probes, 9 models
(10 claim rows) and the 6-row pre-fix matrix. It measures 87 rows in 88 builds, and all
agree.

## 3. The parent-visible list

1. **`KL_pp_shadow`: no edit.** No port and no parameter was added; `NVM_MEM_TMO_CYC_P`
   still follows `CLK_HZ_P`, so the port-contract gate's count is unchanged.
2. **The deadline's counting changed.**
   - A cycle in which the port or a manager holds the operation now pauses the count, where
     it used to clear it.
   - In-tree managers and the arbiter hold `wvalid` and `rready` through a data phase
     (`KL_acmp_nvm_shadow.sv:963`, `:966`; `KL_aecp_nvm_writer.sv:1092`, `:1094`;
     `KL_pp_nvm_mgr_arb.sv:178-182`), so the board behaves as in round 1. `tb/acmp_nvm`
     stays 388/388 on the paused RTL.
   - A manager that drops its strobe can no longer keep a silent device unanswered.
   - A wait state whose terminal rode the final byte (the coincident freedom) no longer
     charges its consuming cycle to the next request.
3. **`parent-adoption-p2-cdf49d1a.patch` is unchanged.** sha256
   `3dda850924ffe4150aa33703ac82c0784035e3387070b7c9b5fc537a7467d08b`, 9,728 bytes.
   `parent-adoption-c4c6-ea3fb388.patch` is unchanged too: sha256
   `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`.
   - The assignment allows an update only if the banner text it amends changes.
   - The patch never quotes the banner's counting rule. It says "a device that owes the
     port an event and gives none for `NVM_MEM_TMO_CYC_P` clocks", which remains exact:
     the clocks counted are the owed ones.
4. **Processor documents the parent reads.** 02 §8 (anchor `sec-02-nvm-deadline`), F08.1,
   the integrator guide's `NVM_MEM_TMO_CYC_P` row, 09 §8.5. Diagram 21 and its PNG are
   unchanged: parameters 28 = 28 = 28.

## 4. Gate tables, at the head `c26b14b316f14abdbe1080f2649f7df83bce061a`

Pinned Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050`). Every processor
command ran on a `git archive` export of `c26b14b316f14abdbe1080f2649f7df83bce061a` under `$VALIDATION_STORAGE/ppP2-a502/gates/`.
The exception is the figures gate, which reads pinned git revisions and ran in the lane
tree; the tree stayed clean, ignored files included. Logs and rc files are in the scratch
area; none is in this directory.

**Processor, all rc 0:**

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map gate (61 constants, 89 entry points), M9 opcode gate (30); 33 suites, 1,019,688 checks, 0 failing: `nvm_port` 686 = 343 + 343 over its two builds (326 in round 1), `acmp_nvm` 388, `pp_top` 9,151; 963 s. (Round 1's table said 37 suites; its own log at `70bf017` has the same 33 suite lines.) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules, LINT OK |
| `make check` | 0 | 41 mermaid + 18 WaveDrom; links 1,045; REQ matrix 115 rows, 17 GAP; module matrix 94 rows, 0 untested; parameters 28 = 28 = 28 |
| `make -C tb/nvm_port figures` | 0 | 88 builds: 1 baseline, 2 for `make run`, 12 arms, 59 mutations and probes, 9 models, 5 matrix. Baseline 343/343; `make run` 343 + 343; all 87 measured rows agree; the RW checks pass under every model; one waiver (2 illustrative phrasings) |
| `./syn/yosys/run.sh` | 0 | 36 tops and the Xilinx memory-map check |
| `make -C tb/srp_top mutants`, `tb/maap`, `tb/adp_engine` | 0, 0, 0 | 78 of 78 (assertion coverage 65/65, 11 controls), 29 of 29 (3 controls), 30 of 30 (2 controls) killed |
| `make -C tb/pp_top aecp-mutants`, `aecp-dispatch-mutants` | 0, 0 | 55 of 55 (5 controls), 35 of 35 (3 controls) killed |
| `python3 tb/pp_top/d3_mutants.py --jobs 3` | 0 | goldens pass (`tb/acmp_nvm`, `pp_top`, `rx_validator`); **83 of 83 KILLED** by their named checks; 2,085 s |

**The figures gate, at each item's own commit** (each a lane-tree run, rc 0, "all measured
figures agree with the tree"):

| After | Builds | Baseline | Elapsed |
|---|---:|---|---:|
| item 1, `e42870e` | 76 | 326/326; lazy rows 326/0 | 449 s |
| items 2-3, `6b6f309` | 82 | 339/339 | 737 s |
| item 4, `ff2cce1` | 86 | 343/343 | 624 s |
| item 5, `06db35e` | 88 | 343/343; `make run` 343 + 343 | 566 s |
| the head, `c26b14b` | 88 | 343/343; `make run` 343 + 343 | 651 s |

**tb/acmp_nvm on the paused RTL** (scratch copy at `ff2cce1`'s tree): rc 0, 372 + 16 =
388/388.

**Parent consumer set (16)** at milan-fpga dev `cdf49d1a`, in `$VALIDATION_STORAGE/ppP2-a502/parent`:
- built by `mkparent.sh` (scratch): a `git archive` of the trusted checkout, 984 index
  entries;
- gptp-processor `5dce647a` and verilog-axis `48ff7a7e`, exported from the build-dev
  worktree's submodules and made repositories at their pins;
- the processor gitlink at `c26b14b316f14abdbe1080f2649f7df83bce061a`;
- `parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-p2-cdf49d1a.patch`, each
  `git apply --check` clean, committed;
- the porcelain empty before the gates and after them.

All rc 0:

| # | Command | rc | Result |
|---:|---|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | every ratchet within budget: 167 translation units, long function 0 <= 0, build without warnings 0 <= 0; Python long function 9 <= 9, long module 10 <= 10 |
| 3, 4 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `check_port_contracts.py` | 0 | processor 1,757 ports (unchanged), undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 96 candidates, all recorded; 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 8, 9 | `docs_check.py`, `xvlog_gate.py --check` | 0, 0 | 0 findings over 185 md + 956 files; 4 findings == ratchet, the same four |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | 0, 0 | all gates pass except gate 11, not run (it needs a local build tree, as before); 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS; the mutant arms pass |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 0 failures; 5 of 5 leg-defect arms caught |

**The first parent run, at `36abf30`, found one defect of this lane's own:**
- `check_cpp_idiom.py` rc 1: "build without warnings 1 > ratchet 0". Item 5's per-build
  `-CFLAGS "-DNVM_PORT_TMO=..."` group lacked `-Wall -Wextra`, and the gate requires them in
  every group.
- Gates 2-11 passed at that head. The logs are in `pgates-36abf30/`.
- `c26b14b` adds the flags, and the whole set above ran again at `c26b14b`.
- The processor runs started at `36abf30` were stopped and restarted at `c26b14b`.

**Not run:**
- the other mutation drivers outside CI (`notify_mutants.py`, `acmp_mutants.py`,
  `gsi_mutants.py`, `retry_mutants.py`, `srp_admission/mutants.py`, `name_wr_mutant.py`).
  They plant edits in modules this lane does not change, and the suites they drive pass
  above;
- hosted CI and act;
- Vivado (the OOC cost is Yosys, as in round 1).

## 5. Out-of-context cost

`KL_pp_nvm_port` as its own top: sv2v v0.0.13, then Yosys 0.66 `synth_xilinx -family xc7
-flatten`. That is round 1's recipe, re-run here for all three revisions.

| Configuration | LUT | FF | CARRY4 | MUXF7 | MUXF8 | vs main |
|---|---:|---:|---:|---:|---:|---|
| main `2ebd4fe8` | 197 | 118 | 14 | 15 | 6 | - |
| round 1 `70bf017`, default | 257 | 148 | 21 | 25 | 9 | +60 LUT, +30 FF, +7 CARRY4 |
| round 1, `MEM_TIMEOUT_CYC_P` = 1 | 249 | 122 | 14 | 14 | 5 | +52 LUT, +4 FF |
| **round 2, the default, 100,000,000** (27-bit count) | 245 | 148 | 21 | 29 | 11 | **+48 LUT, +30 FF, +7 CARRY4** |
| **round 2, the smallest legal value, 1** | 248 | 122 | 14 | 20 | 6 | **+51 LUT, +4 FF** |
| round 2, 125,000,000 | 261 | 148 | 21 | 17 | 6 | +64 LUT, +30 FF, +7 CARRY4 |
| round 2, the largest legal value, 2^31 - 1 | 266 | 152 | 22 | 27 | 8 | +69 LUT, +34 FF, +8 CARRY4 |
| round 2 with the verdict tied off, default | 222 | 119 | 14 | 12 | 3 | +25 LUT, +1 FF |
| the same netlist, tied off, at 1 | 237 | 119 | 14 | 20 | 5 | +40 LUT, +1 FF |

- **The watchdog and owed command alone** (round 2 minus its tied-off self): +23 LUT,
  +29 FF, +7 CARRY4 at the default, and +26 LUT, +3 FF at 1.
- **FF figures are exact.** The pause adds no register. The FFs are the count's width plus
  `owed_r`, `owed_rd_r` and `lg_r`, as in round 1.
- **LUT figures are ABC's mapping and move by a few in either direction.** The two
  tied-off rows are logically identical and differ by 15 LUT. Read the round-2 default's
  -12 LUT against round 1 in that light, not as a saving.
- **Inputs** (scratch, `$VALIDATION_STORAGE/ppP2-a502/ooc/`):
  - the port sources are `git show` of each revision;
  - sha256 of the round-2 source: `20525cbd5ed14436fc725cf525c89567e43cabd5b43299703dea5db0404efbf2`.

## 5a. Scratch, not in this directory

All under `$VALIDATION_STORAGE/ppP2-a502/`:
- **gate logs and rc files:** `gates/`, `pgates/`, `logs/`;
- **parent copy:** `parent/`;
- **the scratch measurement tools:**
  - `fastfig.py`: the gate's own tables, measured in parallel copies;
  - `compare.py`, `apply_figs.py`: put measured numerators into the claim spans; every
    change was reviewed, and the real gate re-measured each one;
  - `probe.py`, `mkparent.sh`, `ooc/ooc.sh`.

The lane tree stayed clean, ignored files included, after every gate.
