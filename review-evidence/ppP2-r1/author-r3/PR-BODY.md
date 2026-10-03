[A498]
Closes #15
Closes #18
Closes #19
Closes #20
Closes #21

Lane P2, NVM port robustness, implemented as ruled on #15 (comment 5952386396, after the
design STOP 5952358239). Base `main` `2ebd4fe8`; head `70bf017d62d60b4401126c7b1bb087f4cb115c5a`.

## Items, in the assignment's order

1. **#21 and #19: the handshake device models and the mutations they redden.** Four
   standing variants in `tb/nvm_port`, beside the four array models and selected the same
   way (`measure_figures.py` `MODELS`), each justified against the port's banner and on
   the README's line between a contract freedom and a broken backend:
   - **unsolicited completion** (refusal (c), `KL_pp_nvm_port.sv:52-62`): freedom, 326 of
     326 checks green;
   - **coincident completion** (the latch, `:319-323`): freedom, 326 green;
   - **short read**, every other READ ended after three eighths of its bytes (refusal (d),
     `:63-67`): a broken backend;
   - **silent**, every command granted and never answered (the deadline, `:69-108`): a
     broken backend.

   The two broken backends fail service checks only. Nine run-wide checks (RW1-RW9) grade
   what every operation is owed: answered exactly once, no device request while the
   backend owes one, no invented DEADLINE, device errors and short reads named DEVICE.
   The figures gate requires them to PASS under every model. #21's four mutations, each
   under its model (fails of 326):
   - the latch armed in every state, under unsolicited completion: 222;
   - the latch deleted, under coincident completion: 200;
   - the header short-read defence off, under short read: 146;
   - the deadline verdict off, under silent: 267, RW1 among them (the wedge).

   #19's four, each failing a check that names it:
   - the low magic byte (T26a/b, M2-lo): 5;
   - the payload bound at its legal edge, a record of exactly `MAX_PAYLOAD_P` committed and
     restored (T26c/d, M7): 4;
   - the sticky `done_seen_r` latch (T21/T22): 21;
   - the short-read defence (T23c, M8): 22.

   The existing array models keep their rows. Lazy erase's single FAIL is the pre-existing
   T1, a check of the backend's own erase side effect that the README names as that rule's
   one known exception.
2. **#15: the timeout.**
   - **Parameter.** `MEM_TIMEOUT_CYC_P` on `KL_pp_nvm_port` (`:121`), class E's name and
     idiom (`KL_aecp_resp_buf.sv:103-111`, `KL_aecp_desc_store.sv:176-183`). Legal 1 to
     2^31 - 1, refused outside at elaboration by name (`:185-190`). At the top it is bound
     as `NVM_MEM_TMO_CYC_P = CLK_HZ_P` (`protocol_processor_top.sv:161-173`, `:2885-2887`).
   - **Default, as a derivation** (F01.5 `P-NVM-MEM-TMO-CYC`, F08.1 `T-NVM-PORT-DEADLINE`):
     20 times the parent backend's longest legal stall, its 50 ms grant hold. That is
     1,000 ms, equal to `T-NVM-RS-AGGREGATE` and 50 times the walks' per-wait deadline.
   - **What it counts.** A no-progress count runs only on a cycle in which the device owes
     the port an event: a grant, a byte the port presents or is ready for, or the terminal
     of a command whose data phase is over (`:246-282`). Every event restarts it, and a
     manager stall is never charged. A slow but valid device is therefore never refused:
     T24 has one answering every event `TMO` cycles late, over more than forty deadlines'
     worth of cycles.
   - **What err and busy do.** On the (`MEM_TIMEOUT_CYC_P` + 1)-th silent owed cycle the
     port gives one `err`, cause 3 DEADLINE (02 §8's reserved code), never `done`. Busy is
     low at the pulse, exactly `MEM_TIMEOUT_CYC_P` + 2 clocks after the last handshake. T24
     grades this in all twelve owed states, at `TMO` (tolerated) and at `TMO` + 1 (refused).
   - **The abandoned command stays owed** (`:283-306`). The port requests nothing over it,
     drains an owed READ's bytes, and takes the device's next done or err as its end. A
     grant one cycle after a deadline withdrew the request is owed too, because the
     parent's backend registers its grant.
   - **The abandoned WRITE is contained, as ruled.** It ends only with the device's own
     terminal or a reset; the managers' unchanged error, retry and alarm path reports it.
   - **Refusal (d).** A command the device ends before its final byte is one err, cause
     DEVICE, at once, in all four data phases (T27). It used to wedge the port.
   - **Criterion 2, as the ruling reads it.** `nvm_busy_o` falls at the DEADLINE pulse, and
     every later request is answered within the bound. It is served once the device has
     ended the abandoned command (T24 served branch), and answered with one err DEADLINE,
     with no device command, while the device stays silent (T24 DEADLINE branch). Both
     branches are graded.
   - **The silent-device model** is a standing variant (item 1).
3. **#18: reset mid-commit.** T25 asserts `rst_n` at six stages named on the bus, with
   port and device reset together. It pins the port idle and silent after release, the
   neighbour byte-exact, the next commit byte-exact, and the torn record refused at its
   header or forwarded whole and refused by the crc16. Two more resets hit the port alone.
   The torn image that restores as well-formed is documented as the manager's to refuse,
   with the crc16 named (`KL_acmp_nvm_shadow.sv:391-395`, `KL_aecp_nvm_writer.sv:482-485`).
   `tb/acmp_nvm` group R shows it on the real binding manager. The README's "power cut"
   section now says which phases tear by a device err (T15-T18) and which by a reset (T25).
4. **#20: a dying flash is not a blank region.** This was met at main: a zero-byte DEVICE
   err fails the whole walk (`KL_acmp_nvm_shadow.sv:584-586`; N1a-d), while a clean done
   or an UNFRAMED err is the blank default (A2/A2b, F4, N2a-b, N9c, with G2 green), and B02
   is killed. This PR adds the DEADLINE arm in a second `tb/acmp_nvm` build, whose port
   deadline is below the walk's:
   - N12a, N12d: a silent device fails the walk with cause 2, never blank;
   - N12e: an erased face stays done, not failed, blank, with no alarm;
   - N12b-c: the amended alarm path.

   07 §5.3's DEVICE row now says "or DEADLINE".
5. **The parent-visible list** (below).

## Validation

At the head, pinned Verilator 5.050, every command on a `git archive` export except the
figures gate, which reads pinned git revisions and ran in the lane tree:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 37 suites, 1,019,328 checks, 0 failing (`nvm_port` 326, was 136; `acmp_nvm` 388 over two builds, was 360; `pp_top` 9,151, unchanged) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules |
| `make check` | 0 | 41 mermaid + 18 WaveDrom; links 1,045; matrices; `gen_matrix.py --check` 94 rows, 0 untested; parameters 28 = 28 = 28 |
| `make -C tb/nvm_port figures` | 0 | 76 builds; every figure agrees; the RW checks pass under all nine models |
| `./syn/yosys/run.sh` | 0 | 36 tops and the Xilinx memory-map check |
| `make -C tb/srp_top mutants`, `tb/maap`, `tb/adp_engine` | 0, 0, 0 | 78 of 78 (coverage 65/65), 29 of 29, 30 of 30 killed; every control passes |
| `make -C tb/pp_top aecp-mutants`, `aecp-dispatch-mutants` | 0, 0 | 55 of 55, 35 of 35 killed; every control passes |
| `python3 tb/pp_top/d3_mutants.py --jobs 3` | 0 | goldens pass (`tb/acmp_nvm` in its two builds, `pp_top`, `rx_validator`); **83 of 83 KILLED** by their named checks; 1,960 s |

The parent consumer set (16 commands) ran at milan-fpga dev `cdf49d1a` in a scratch copy, with the
processor at this head and both patches applied in order (`git apply --check` clean). It was all
rc 0:
- the C++ and Python idiom ratchets;
- the source lists (107 files, 4 of 4, processor 36/42 tops);
- the port contracts (processor 1,757 ports, unchanged);
- naming (96 recorded);
- test evidence (72 <= 77, 0 unexplained DUT readers);
- `docs_check` (0 findings);
- `xvlog_gate` (4 == ratchet);
- the builder (all gates pass except gate 11, which needs a local build tree, as before);
- `lint_rtl` (90 <= 90);
- `pp_shadow` (311, 0 failures);
- `nvm_cosim` lint and quick (315 of 315);
- `milan_dp` (9 benches PASS);
- `milan_dp_render` (65 + 152, 5 of 5 leg-defect arms).

Two of these gates first failed on this lane's code, and the last commit fixes both: the idiom
ratchet (two functions over 100 lines, now split with no check changed) and the naming ratchet
(a unit word in the cause port's comment).

Out-of-context cost of `KL_pp_nvm_port` (sv2v, then Yosys `synth_xilinx`), against main's
197 LUT and 118 FF:

| Setting | Cost |
|---|---|
| the default, 100,000,000 | +60 LUT, +30 FF, +7 CARRY4 |
| the smallest legal value, 1 | +52 LUT, +4 FF |
| the watchdog and owed command alone, at the default | +29 LUT, +29 FF |
| the watchdog and owed command alone, at 1 | +21 LUT, +3 FF |

## Parent-visible list

1. **`KL_pp_shadow`: no edit.** The new top parameter follows `CLK_HZ_P` like the other NVM
   times, and there is no new top port.
2. **Consumer gates.** `nvm_cosim` instantiates the port with no parameters, so the module
   default (100 s at its 1 MHz) leaves D4c-D4e unchanged, as ruled. `pp_shadow` is
   unchanged. All 16 commands pass (above).
3. **On the board.** A silent device face now gives three failed attempts and
   `nvm_alarm_o`, which revokes `nvm_backed` and drops the change's pending bit, instead of
   pending for ever. Quarantine is still never released by time alone.
4. **`parent-adoption-p2-cdf49d1a.patch`.** Docs only, applied after
   `parent-adoption-c4c6-ea3fb388.patch` (unchanged). It amends the saved-state contract's
   W13, §8.8 and §15 item 4, and two sentences that would otherwise contradict them (§6.4
   and the stage table's release notes).
5. **Processor documents the parent reads.** 02 §8 and §8.2, 07 §5.3, 08 §2, F01.5, F08.1,
   the integrator guide, and diagram 21 with its PNG (parameters 28 = 28 = 28).

## What remains

- Hosted CI on this PR, and its reviews.
- The parent adopts both patches when it moves its processor pin.
- Unchanged from main: three `*REQ` error arms that no phase arms (an err in place of the
  ERASE, WRITE or payload READ's grant), and the randomized cut points
  `09_verification.md:56` asks for.
- Re-grading the parent's `nvm_cosim` under the top's derivation, which was ruled out of
  this lane.

## Round 2

Round 2 answers R436-1 and R437-1, both NEGATIVE on two MINORs each, as assigned on #15
(comment 5956438390), in the assignment's item order. Six commits on `70bf017d`; head
`c26b14b316f14abdbe1080f2649f7df83bce061a`.

No port changed on any module, and no parameter was added: the deadline is still
`MEM_TIMEOUT_CYC_P` on the port and `NVM_MEM_TMO_CYC_P = CLK_HZ_P` at the top.

| Commit | Item |
|---|---|
| `e42870e` | 1: T1 asserts the erased tail only on a backend with erase semantics |
| `6b6f309` | 2 and 3: T28, the owed command's end and drain seen from a waiting request; D18-D23 |
| `ff2cce1` | 4: the count pauses on a cycle that owes nothing; T29; D24-D26 |
| `06db35e` | 5: every harness wait derived from `TMO`; a second build at 37 |
| `36abf30` | 6: the reviewers' R1 wording |
| `c26b14b` | the parent's C++ idiom gate: `-Wall -Wextra` on the new per-build `-CFLAGS` group |

1. **T1 and #21 item 4 (R436-1 F2 = R437-1 F1): outcome (a).**
   - T1 keeps its bus checks: the whole-region ERASE is requested once, before the WRITE,
     and region 3 is erased once.
   - The erased tail past the record is now asserted only on a backend with erase semantics
     (`tb/nvm_port/sim_main.cpp:929`).
   - Lazy erase is now the harness's own switch, `lazy_erase` (`:202`, `:489`), the way the
     handshake models are. Both lazy-erase rows of the figures gate set it, and T1 reads it.
   - Both rows now read **343 PASS, 0 FAIL**. They were 325/1 at `70bf017` and 326/0 at the
     item's own commit. The README's table and its prose (the array rule's `done`
     clause, the count of array-dependent checks, the `err` clause's exceptions) say so,
     and the figures gate agrees.
   - **#21 item 4 is now met in full.** Every model the port must tolerate leaves every
     check green: pristine, half-page, page-buffered, lazy erase, lazy erase +
     page-buffered, coincident completion and unsolicited completion. That holds at both
     bounds (item 5). The PR keeps its closing line for #21.
2. **The owed command's ends and drains (R436-1 F1)**, and
3. **the unpinned properties (R437-1 F2).**

   T28 (`owed_terminals_are_credited_to_no_operation`,
   `owed_events_restart_a_waiting_request`, `sim_main.cpp:2159-2262`) starts the next
   operation while the device still carries the abandoned command, and checks that it
   waits in its request state with no command taken:
   - (a) an owed payload READ is ended by the device's err while a restore waits in
     `S_RHREQ`. The err is credited to no operation and the restore is served byte-exact;
   - (b) the same for an owed ERASE ended by err while a commit waits in `S_WEREQ`;
   - (c) a deadline in the WRITE's completion window (`S_WWAIT`) leaves the WRITE owed. The
     next commit requests nothing over it and ends DEADLINE, and once the device's done
     ends the WRITE the following commit is served;
   - (d) an owed READ drains one byte every `TMO` / 2 cycles while a restore waits, for more
     than ten deadlines. The restore is served, never DEADLINE;
   - (e) an owed ERASE's done comes three fifths of a deadline into a restore's wait, and
     the grant comes three fifths of a deadline after it. The restore is served.

   Each defect is a figures-gate row (fails of 343):

   | Row | Planted defect (review IDs) | Fails | Named by |
   |---|---|---:|---|
   | D18 | `S_RHREQ` not blocked by the owed command (W15, X24) | 1 | T28a |
   | D19 | the same in `S_WEREQ` (W15b) | 1 | T28b |
   | D20 | a drained byte of an owed READ is not progress (W16, X18) | 1 | T28d |
   | D21 | the owed command's done is not progress (X17) | 1 | T28e |
   | D22 | a deadline in `S_WWAIT` leaves nothing owed (X12) | 2 | T28c, RW3 |
   | D23 | the same guard dropped from `S_WWREQ` and `S_RPREQ` | 0 | equivalent, recorded as such |

   D23 cannot fail, and it is measured rather than asserted. A command becomes owed only
   as an operation ends, so the next operation meets it in its first request state,
   `S_WEREQ` or `S_RHREQ`. Removing all four guards (R437-1's X24b) is killed by D18 and
   D19.

   The README's claim "T24 grades all of it" now reads "T24, T28 and T29". 09 §8.5 names
   T28 and D9-D23, with D23 as the equivalence. The README's mutation count is
   fifty-nine, and the figures gate runs 88 builds.
4. **The watchdog pauses (R436-1 S1, taken).**
   - **The count.** It restarts only at a device event (`prog_w`) and is zero in `S_IDLE`.
     It counts every owed cycle and holds on any other
     (`hdl/packet_engine/KL_pp_nvm_port.sv:278-282`). No manager handshake pattern can
     therefore keep a silent device from the deadline. Every grant, byte and terminal
     still restarts it.
   - **A second term was needed: a wait state whose terminal is already latched owes
     nothing** (`:258-260`, `&& !done_seen_r`). R436-1 measured its pause (W6) under the
     pristine model only, where it passes every check. Under the coincident model it fails
     5. There the
     header READ's done rides its eighth byte. `S_RHWAIT`'s cycle that consumes the latched
     done was an owed cycle, and a pause carries it across `S_RHFWD` into the payload
     request. The tolerated grant `TMO` cycles late is then refused, and RW4 fails. D26
     records this: 0 under pristine, **5 under the coincident model**.
   - **No citation moved.** The banner (`:69-83`) and the comments were rewritten at the
     same line count, so every `KL_pp_nvm_port.sv:NNN` citation in the tree, in this body
     and in both reviews still points where it did.
   - **Documents.** The banner, 02 §8 (`sec-02-nvm-deadline`), F08.1's
     `T-NVM-PORT-DEADLINE` row (value and description), the integrator guide's
     `NVM_MEM_TMO_CYC_P` row, the top's parameter comment and 09 §8.5.
   - **Graded by T29** (`a_manager_strobe_never_holds_the_deadline_off`,
     `sim_main.cpp:2105-2134`). A manager drops `rready` one cycle in every `TMO` / 2 while
     the device never presents a payload READ's 11th byte. A second drops `wvalid` likewise
     while the device never takes a WRITE's 21st byte. Each ends in one err, cause
     DEADLINE, exactly `TMO` + 2 cycles after the device's last byte plus the cycles the
     manager held. The harness counts the held cycles and requires more than none.
   - **Rows** (fails of 343):
     - D24, the round-1 count (cleared on every cycle owing nothing): 3, namely T29a, T29b
       and RW1, both operations unanswered;
     - D25, the count not zeroed between operations: 7;
     - D26/coincident: 5, as above;
     - D4, progress no longer restarting the count, re-anchored: 38.
   - **Out-of-context cost** of `KL_pp_nvm_port`, measured with the same recipe as round 1
     (sv2v, then Yosys `synth_xilinx -family xc7 -flatten`; main 197 LUT, 118 FF,
     14 CARRY4):

     | Setting | Round 1 | Round 2 |
     |---|---|---|
     | the default, 100,000,000 | +60 LUT, +30 FF, +7 CARRY4 | +48 LUT, +30 FF, +7 CARRY4 |
     | the smallest legal value, 1 | +52 LUT, +4 FF | +51 LUT, +4 FF |
     | the largest legal value, 2^31 - 1 | +47 LUT, +34 FF, +8 CARRY4 | +69 LUT, +34 FF, +8 CARRY4 |
     | 125,000,000 | +53 LUT, +30 FF, +7 CARRY4 | +64 LUT, +30 FF, +7 CARRY4 |
     | the watchdog and owed command alone, at the default | +29 LUT, +29 FF, +7 CARRY4 | +23 LUT, +29 FF, +7 CARRY4 |

     The pause adds no register: every FF figure is unchanged. The LUT figures move by a
     few with ABC's mapping, in either direction. The same netlist with the verdict tied
     off maps to 222 LUT at the default and to 237 LUT at 1.
5. **Harness constants (R436-1 S2, taken).**
   - **Every wait derived from `TMO`.** Every harness wait that meets the deadline is now
     derived from `TMO`, and each keeps its old value at 100. That covers:
     - `run_op`'s guard: `1000L * TMO`, which was the 100,000 that made the variant at
       1,000 fail;
     - the drain past a pulse: 3 * `TMO` / 10;
     - the staged cut and poke windows of T6 and T25, and their midpoints: 2 * `TMO` / 5;
     - the late resume of the served branch: `TMO` + 3 * `TMO` / 5;
     - the strays' spacing, the reset-silence windows and T27's wait for a first command.

     The harness refuses to build below `TMO` = 20. The fixed protocol delays still left
     (1 to 9 cycles) stop being legal there.
   - **A second build at 37.** `make` now builds the suite at `-GMEM_TIMEOUT_CYC_P=100`
     and again at 37, and hands each value to the C++ as `TMO` (`tb/nvm_port/Makefile`).
     Each build prints its own tally, and the last line is the sum. `make run` gives
     343 + 343, all PASS.
   - **The figures gate.** It measures every row at 100 (`make primary`). It also requires
     `make run` to give exactly 343, 343 and their sum, all PASS (`both_builds_disagree`).
   - **Other models and the review's defects at 37.** In scratch copies at 37:
     - the seven contract-legal models are 343/0 each;
     - short read is 265/78 and silent 115/228, the same as at 100, with every RW check
       passing;
     - D18-D26 fail as at 100, except D20, which fails 3.
6. **RESIDUE R1, in the reviewer's exact text.**
   - R436-1's R1 sentence now reads "The first of those is coincident completion: the
     device raises `dev_done_i` on the same edge that moves a pump's final byte, which
     `KL_pp_nvm_port.sv:319-323` says the sticky `done_seen_r` latch exists for." Its
     citation is still exact, because of item 4's constant line count.
   - R437-1's R1 is in the same sentence pair: "below" becomes "above".
   - R437-1's R2-R5 were not assigned and are left to the residue checklist.

**The issues after round 2:** #15, #18, #19 and #20 are met as in round 1, and #21 is now
met in full (item 1), so all five close.

### Round 2 validation

At head `c26b14b316f14abdbe1080f2649f7df83bce061a`, pinned Verilator 5.050. Every processor command ran
on a `git archive` export of the head, except the figures gate, which ran in the lane tree.

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

Parent consumer set at milan-fpga dev `cdf49d1a`, in a scratch copy: a `git archive` of the
trusted checkout (984 index entries), gptp-processor and verilog-axis at their pins, the
processor gitlink at this head, and `parent-adoption-c4c6-ea3fb388.patch` then
`parent-adoption-p2-cdf49d1a.patch` applied (`git apply --check` clean, porcelain empty):

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

The first parent run at `36abf30` failed one gate on this lane's own code. The parent's C++
idiom gate requires `-Wall -Wextra` in every `-CFLAGS` group of a testbench Makefile, and
item 5's per-build group lacked them. `c26b14b` adds them, and every gate above ran again
at that head.

### Round 2 parent-visible list

1. **No port or parameter change.** `KL_pp_shadow` needs no edit. The port-contract count
   is unchanged.
2. **The deadline's counting changed.** A cycle the port or a manager holds the operation
   now pauses the count rather than clearing it. In-tree managers and the arbiter hold
   their strobes for a whole data phase, so nothing changes on the board with them. A
   manager that drops `wvalid` or `rready` can no longer keep a silent device unanswered.
   A wait state whose terminal rode its final byte no longer charges its consuming cycle
   to the next request.
3. **`parent-adoption-p2-cdf49d1a.patch` is unchanged** (sha256 `3dda8509...d08b`, 9,728
   bytes), and so is `parent-adoption-c4c6-ea3fb388.patch`. The banner text the p2 patch
   relies on, "a device that owes the port an event and gives none for
   `NVM_MEM_TMO_CYC_P` clocks", is still exact: the clocks counted are the owed ones.
4. **Processor documents the parent reads:** 02 §8, F08.1, the integrator guide's
   `NVM_MEM_TMO_CYC_P` row, and 09 §8.5. Diagram 21 and parameters 28 = 28 = 28 are
   unchanged.

### What remains after round 2

- Hosted CI and the reviewers' re-review at this head.
- Not assigned here, so left for the residue checklist: R437-1's residue R2-R5, and its
  suggestion S2 (a late grant that carries err, X20). Both of R436-1's suggestions were
  taken (items 4 and 5).
- As before: three `*REQ` error arms no phase arms, and the randomized cut points
  `09_verification.md:56` asks for.

## Round 2b

Round 2b is a merge and nothing else, as assigned on #15 (comment 5959104191) before the
delta review. One delta review covers rounds 2 and 2b. One commit on `c26b14b3`, a merge
commit made with `git merge --no-ff` (no rebase). Head
`c0715410418b47ffaccf5feed55b71617fcfaf82`, parents `c26b14b3` and `main` `631eeb34` (PR #142, P141).

No port, parameter, register or RTL change. `git diff c26b14b3 c0715410 -- hdl` is main's
comment in `hdl/aecp/ucode/gen_ucode.py` alone, and the ucode ROM it generates is
byte-identical at both heads (26,624 bytes, sha256 `518b900c...37f8`). The port source
is byte-identical to round 2's (sha256 `20525cbd...efbf2`).

### 1. The merge

Main brought P141's SET/GET_CLOCK_SOURCE work: `tb/pp_top` section D3C and its six
mutants, the comment in `gen_ucode.py`, and the L6, REQ-AEM-013, REQ-MDL-005, 06 §6.4 and
09 §8.2 records. It touches no file under `hdl/nvm`, `hdl/packet_engine`, `hdl/top`,
`tb/nvm_port` or `tb/acmp_nvm`. The two sides share two files:

| File | Merge | Result |
|---|---|---|
| `docs/architecture/07_memory_maps.md` | auto-merged, disjoint hunks | main's L6 row (`:135`) beside this lane's restore-table rows and drain paragraph (`:639`, `:649-657`, `:701`) |
| `docs/architecture/09_verification.md` | one conflict: §8.2's closing paragraph (`:208-215`) | both sides kept: main's D3C row (`:206`), its 87-control count, and its sentence placing the two SET_CLOCK_SOURCE range-check controls in `aecp_dispatch_mutants.py`'s `d3` target. This lane's pointer stays: "the port's own deadline, resets and handshake models are §8.5's". It replaced the base's "#18, #19 and #21 are not closed by this evidence", which main's side carried re-wrapped and otherwise unchanged. |

After the resolution, every file only main changed equals `631eeb34`, and every file only
this lane changed equals `c26b14b3`.

- **Section number.** This lane's section stays **09 §8.5**. Main's 09 ends at §8.4.
  Lane C8 (PR #144) also adds an §8.5. Whichever of the two merges second renumbers, so
  nothing is renumbered here for C8.
- **Citations.** The merge moves 09 by two lines from `:206` on; §8.5's heading moves
  from `:293` to `:295`. No citation points there. The tree's 14 `file:line` citations
  and this body's 14 name files main did not change, or `09_verification.md:56`, which
  sits above main's hunk. Main's new text cites no line in a file this lane changed. No
  heading changed on either side, and the link gate checks 1,045 links, as in round 2.
  No citation needed a fix.

### 2. Re-measured at `c0715410`

Pinned Verilator 5.050. Every processor command ran on a `git archive` export of the head,
except the figures gate, which ran in the lane tree (clean afterwards, ignored files
included). All rc 0:

| Command | rc | Result |
|---|---:|---|
| `git apply --check`, every campaign patch, at the tree root as the drivers apply them | 0 | 207 of 207 apply: `tb/srp_top` 73, `tb/pp_top/mutations` 42, `tb/pp_top/aecp_dispatch_mutations` 37 (main's two new `sclks-*` and refreshed `lk-prefix-zero-body` among them), `tb/adp_engine` 28, `tb/maap` 27 |
| `./scripts/run_suites.sh` | 0 | UPC map gate (61 constants, 89 entry points), M9 opcode gate (30); 33 suites, 1,019,705 checks, 0 failing; 1,042 s. Every suite's tally equals round 2's except `pp_top`, 9,168 = 9,151 + main's 17 D3C checks. `nvm_port` 686 = 343 + 343, `acmp_nvm` 388 |
| `make -C tb/nvm_port figures` | 0 | 88 builds: 1 baseline, 2 for `make run`, 12 arms, 59 mutations and probes, 9 models, 5 matrix. Baseline 343/343; `make run` 343 + 343; all 87 measured rows agree, the same figures as round 2; one waiver (2 illustrative phrasings); 593 s |
| CI's docs job one by one (`check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale`), `make check`, `gen_matrix.py --check` | 0 | 41 mermaid + 18 WaveDrom; links 1,045; REQ matrix 115 rows, 17 GAP; module matrix 94 rows, 0 untested; parameters 28 = 28 = 28 |
| `./scripts/lint_hdl.sh` | 0 | 41 modules, LINT OK |

**Campaigns re-run**, each because it builds `tb/pp_top` (main changed `d3_phases.hpp`,
`sim_main.cpp` and `pp_top_wrap.sv`) and the generated ucode, or is itself a file main
changed:

| Campaign | rc | Result |
|---|---:|---|
| `make -C tb/pp_top aecp-mutants` | 0 | 5 controls PASS, 55 of 55 KILLED; every arm's failing count equals round 2's |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 4 controls PASS, 37 of 37 KILLED. Against round 2, only main's `d3` control and its two arms are new, failing 11 and 6 as P141 records |
| `python3 tb/pp_top/d3_mutants.py --jobs 3` | 0 | goldens PASS (`tb/acmp_nvm`, `pp_top`, `rx_validator`); **87 of 87 KILLED** by their named checks; 2,388 s. All 75 `tb/pp_top` failing counts equal that README's table. The 12 `tb/acmp_nvm` and 2 `tb/rx_validator` rows equal round 2's. The only moves are P141's: `TRG_clks` 5 to 10, `RPL_clks` 3 to 5, `rule_ignored` 3 to 7, `unframed_reads_as_device_error` 38 to 42, `done_without_d3` 42 to 45, and the four new `clks_*` at 10, 2, 4 and 4 |
| `make -C tb/maap mutants`, `make -C tb/adp_engine mutants` | 0, 0 | 29 of 29 (3 controls), 30 of 30 (2 controls) KILLED; every arm equals round 2's |
| `python3 tb/pp_top/acmp_mutants.py --jobs 2` | 0 | 19 of 19 KILLED, 3 goldens PASS; every failing count equals the `tb/pp_top`, `tb/acmp_listener` and `tb/rx_validator` records |
| `python3 tb/pp_top/notify_mutants.py --jobs 2` | 0 | 40 of 40 KILLED, goldens PASS; every failing count equals the README |
| `python3 tb/pp_top/gsi_mutants.py`, `name_wr_mutant.py` | 0, 0 | 20 detected, golden and restored PASS; `decode` killed, golden and restored PASS |
| `./syn/yosys/run.sh` (it runs `gen_ucode.py`) | 0 | 36 tops and the Xilinx memory-map check |

**Not re-run, since no file they read changed in the merge:** `make -C tb/srp_top mutants`
(round 2: 78 of 78), `tb/acmp_talker/retry_mutants.py`, `tb/srp_admission/mutants.py`
and `tb/desc_mem_guard/mutate.py`. None builds `tb/pp_top` or runs the ucode generator.
The out-of-context cost of `KL_pp_nvm_port` stands as round 2 measured it. Its only
input, the port source, is byte-identical.

**Parent consumer set (16)** at milan-fpga dev `cdf49d1a`, in a scratch copy built as in
round 2: a `git archive` of the trusted checkout (984 index entries), gptp-processor
`5dce647a` and verilog-axis `48ff7a7e` at their pins, and the processor gitlink at
`c0715410`. `parent-adoption-c4c6-ea3fb388.patch` and then
`parent-adoption-p2-cdf49d1a.patch` were each applied after a clean `git apply --check`.
The porcelain was empty before the gates and after them. All rc 0, every result equal to
round 2's:

| # | Command | rc | Result |
|---:|---|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | every ratchet within budget: build without warnings 0 <= 0, long function 0 <= 0; Python long function 9 <= 9, long module 10 <= 10 (294 modules; 31 more lines, main's) |
| 3, 4 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `check_port_contracts.py` | 0 | processor 1,757 ports (unchanged), undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | logs identical to round 2's |
| 8, 9 | `docs_check.py`, `xvlog_gate.py --check` | 0, 0 | 0 findings over 185 md + 956 files; 4 findings == ratchet, the same four |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | 0, 0 | all gates pass except gate 11, not run (it needs a local build tree, as before); 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 606, 606, 646 and 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS; the 4 mutant arms caught, as in round 2 |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 0 failures; 5 of 5 leg-defect arms caught |

### Round 2b parent-visible list

1. **Nothing the parent instantiates changed.** No port or parameter changed, and the
   port, arbiter and top sources equal round 2's. `KL_pp_shadow` needs no edit, and the
   port-contract count is unchanged.
2. **Both patches are unchanged**: `parent-adoption-p2-cdf49d1a.patch` (sha256
   `3dda8509...d08b`, 9,728 bytes) and `parent-adoption-c4c6-ea3fb388.patch` (sha256
   `67bcd698...7bd7c`, 2,687 bytes). Both apply cleanly at `cdf49d1a`.
3. **Processor documents the parent reads** (02 §8, F08.1, the integrator guide's
   `NVM_MEM_TMO_CYC_P` row, 09 §8.5) are unchanged. 09 §8.5 keeps its number.

**The issues after round 2b:** unchanged from round 2. The merge alters no acceptance
evidence, so #15, #18, #19, #20 and #21 are met in full and all five close.

### What remains after round 2b

- Hosted CI and the delta review of rounds 2 and 2b at this head.
- Lane C8 (PR #144): whichever of it and this PR merges second renumbers its 09 §8.5.
- As after round 2: R437-1's residue R2-R5 and suggestion S2, three `*REQ` error arms no
  phase arms, and the randomized cut points `09_verification.md:56` asks for.

## Round 3

Round 3 answers R436-2 (one MINOR) and R437-2 (three MINOR), both NEGATIVE, as assigned on
#15 (comment 5961238126), in the assignment's item order. Every finding was a test gap in
round 2's watchdog pause; the RTL the reviews read was right. Seven commits on `c0715410`,
the last two `git merge --no-ff` merges of main (no rebase); head
`527662d659b4ead97675744d12a43af1ea92b9b3`.

No port changed on any module, and no parameter was added: the deadline is still
`MEM_TIMEOUT_CYC_P` on the port and `NVM_MEM_TMO_CYC_P = CLK_HZ_P` at the top. Item 2 adds
one internal count to the port, the bound the reviews suggested; it is no register-map
register and no parameter.

| Commit | Item |
|---|---|
| `593f291` | 1: T30, the randomized harness at bounds 1, 2, 3 and 37, T6's poke on the bus, a third build at 20, every review plant a figures row |
| `ae1cb85` | 2: the owed READ's drain bounded by what it still owes; T28f, the harness's babble mode, D27-D30 |
| `355e7d3` | 3: a late grant that carries `err` (T24, D31, X20) |
| `6fb74ad` | the parent's Python idiom gate: a docstring on item 2's nested helper |
| `f4519fe` | 4: R436-2's R1 and R2 in the reviewer's exact text |
| `46796bf` | 5: merge of main `88969246` (#144, lane C8); this lane's 09 section is now §8.6 |
| `527662d` | 5: merge of main `c74711d4` (#146, `--jobs N` for eight campaign drivers); no conflict |

1. **The pause logic's test gaps.**
   - **R436-2 F1 and R437-2 F1/F2: T30** (`tb/nvm_port/sim_main.cpp:2187-2272`), each arm
     from a reset of its own:
     - (a) an ERASE answered on its own grant, then the WRITE granted `TMO` cycles after its
       request: served. It pins `S_WEWAIT`'s member of the latched-terminal term
       (`KL_pp_nvm_port.sv:260-261`; R436d, Z2);
     - (b) a header READ answered on its eighth byte, then the payload READ granted `TMO`
       cycles late: served. It pins `S_RHWAIT`'s member under the pristine model, where
       round 2 pinned it only under the coincident one;
     - (c) the payload READ's 11th byte presented `TMO` cycles late, on the one cycle the
       manager drops `rready`, the count at its bound, and (d) the WRITE's 21st byte on a
       dropped `wvalid`: each taken the next cycle and served. A paused cycle at the bound
       is never a verdict (`:277`; R436e, Z1a, Z1b);
     - (e) the control: the byte one owed cycle later ends DEADLINE `TMO` + 3 cycles after
       the last byte, the held cycle counted (R436f).

     The bound-cycle drop is the harness's `mgr_drop_gap` (`sim_main.cpp:312`, `:696`). No
     silence is armed in (a)-(d), so RW4 grades them as well. `S_WWAIT`'s and `S_RPWAIT`'s
     members are equivalent: a latched done takes them to `S_FIN` and then `S_IDLE`, which
     zeroes the count. The README and 09 §8.6 now say which wait states are pinned.
   - **The reviewers' fuzz modes, folded in as a standing check.** `tb/nvm_port/fuzz_main.cpp`
     is R436-2's randomized probe rewritten to this tree's C++ rules: its own device,
     manager and owed-cycle oracle, written from the banner. `make` builds it at bounds 1,
     2, 3 and 37, three seeds, six hundred operations per mode and seed.
     - FZ1-FZ4 (legal): never a DEADLINE against a legal device, every operation answered
       once, errs only where the device erred, byte-exact.
     - FZ5, FZ6 (silent): one err DEADLINE, on exactly the (`TMO` + 1)-th owed cycle.
     - FZ7, FZ8 (resume): served if the device ends the abandoned command within the bound,
       DEADLINE if not, both branches taken.

     Each property is one named check per build, so a false DEADLINE fails `make run` and
     `run_suites.sh`.
   - **R437-2 F3: T6's poke is named on the bus** (`sim_main.cpp:1021-1049`). It lands once
     the backend has taken the ERASE, inside the commit at every bound; it used to come
     2 * `TMO` / 5 cycles after the accept, after the commit had ended from 500 up under the
     coincident model. **"The smallest legal bound", as read here:** the suite's own floor is
     `TMO` = 20 (`static_assert`, its 1-9 cycle protocol delays), so `make` now builds the
     suite at 100, 37 and 20. The port's smallest legal bounds, 1, 2 and 3, are the
     randomized harness's.
   - **Measured at other bounds** (scratch, nine models, `make primary TMO=t`):
     - the seven legal models are 0 FAIL at 20, 37, 100, 1,000, 4,096 and 100,000;
     - short read and silent fail the same checks at every one, the RW checks passing;
     - the figures gate keeps one of these as rows: the coincident model at 4096, 0 FAIL,
       and the same with round 2's T6, 16 FAIL (R437-2 measured 15-16 from 500 up).
   - **Every review plant is a figures-gate row with the reviewer's own edit text**
     (`tb/nvm_port/deadline_rows.py`, compared byte for byte against both review packets by
     script). Fails of 356 at `TMO` = 100, pristine model:

     | Plants | Fails | Named by |
     |---|---|---|
     | Q1 = Y1 (`S_WEWAIT`'s latched cycle owes) | 2 | T30a, RW4 |
     | Q2 = Y2 (`S_RHWAIT`'s) | 2 | T30b, RW4 |
     | Q9 = Y16 (a verdict on any busy cycle), Y11 (on a paused pump cycle) | 4 each | T30c-e, RW4 |
     | Q5, Y5 (the count runs on cycles that owe nothing) | 17 each | T24, T29a-b, T30a-b, RW4 |
     | Q6 = Y13, Q7 = Y14 (a dropped strobe clears the count) | 3, 2 | T29a, T30e, RW1; T29b, RW1 |
     | Y6, Y7, Y8, Y9, Y10, Y15 | 7, 10, 12, 9, 15, 68 | T24 among them, each with its own T28/T29/T30 checks |
     | Q3 = Y3, Q4 = Y4, Q8, Q10, Y12 | 0 | equivalent, each argued in the README |

     Q1 and Q9 under the randomized harness at bound 3 each fail 4 of its 9 checks (FZ2,
     FZ3, FZ6, FZ7). D26, the whole latched term dropped, now fails 3 under the pristine
     model; round 2 measured 0 there.
2. **The owed READ's drain, bounded by what it still owes** (R436-2 S1 = R437-2 S1, taken).
   - **RTL** (`hdl/packet_engine/KL_pp_nvm_port.sv`): `owed_left_r` (`:222`) takes the
     abandoned READ's length less the bytes that moved before the deadline. That is all of
     a request's length (`dev_len_o`) and none in a wait state (`left_w`, `:285-296`). It is
     taken with the command's kind, only while nothing is owed, and is one less per byte
     drained (`:323-327`). The drain `drain_w` (`:296`, `:610`) takes those bytes and no
     more. Bytes past them are not taken, so they are not progress; a request waiting on
     the READ ends DEADLINE, as against a silent device.
   - **The contract it serves:** the banner (`:85-99`, at its old line count) and 02 §8
     (`sec-02-nvm-deadline`): a READ owes at most its length, and no device holds a
     waiting request off.
   - **Graded by T28f** (`sim_main.cpp:2402-2438`). A payload READ abandoned before its
     11th byte, whose device then presents bytes past its length, one every `TMO` / 2
     cycles, for ever, is drained of exactly the 30 it owed. The restore waiting on it ends
     DEADLINE `TMO` + 2 cycles after the last of them, and the device's own done then ends
     the READ.
   - **Graded by the reviewers' babble mode.**
     - It is folded in as FZ9 at all four fuzz bounds; about 740 such operations per
       bound are answered DEADLINE.
     - R436-2's own harness in babble mode, unchanged, answers every waiting request at
       1, 2, 3, 37 and 100 (196 to 224 per bound). Its round-2 run answered none.
   - **Rows** (fails of 356):
     - D27, round 2's unbounded drain: 3, T28f twice and RW1;
     - D28, the whole length taken: 1;
     - D29, a drained byte not counted: 3;
     - D30, what is owed retaken at a later deadline: 3;
     - D27 under the randomized harness at bound 3: 1 of 9, FZ9.
   - **Out-of-context cost** of `KL_pp_nvm_port`, round 2's recipe (sv2v, then Yosys
     `synth_xilinx -family xc7 -flatten`). Round 2 reproduces exactly:

     | Setting | Main `631eeb34` | Round 2 | Round 3 | Round 3 against round 2 |
     |---|---|---|---|---|
     | the default, 100,000,000 | 197 LUT, 118 FF, 14 CARRY4 | 245, 148, 21 | 296, 164, 30 | +51 LUT, +16 FF, +9 CARRY4 |
     | the smallest legal value, 1 | | 248, 122, 14 | 287, 138, 23 | +39 LUT, +16 FF, +9 CARRY4 |
     | 2^31 - 1 | | 266, 152, 22 | 301, 168, 31 | +35 LUT, +16 FF, +9 CARRY4 |
     | 125,000,000 | | 261, 148, 21 | 309, 164, 30 | +48 LUT, +16 FF, +9 CARRY4 |

     The 16 FF are the count, kept 16 bits wide like `bcnt_r` and `plen_r`. Against main
     the port now costs +99 LUT, +46 FF and +16 CARRY4 at the default, and +90 LUT,
     +20 FF and +9 CARRY4 at 1.
   - **Lines moved.** The declaration and the drain logic move every `KL_pp_nvm_port.sv`
     citation below `:221` by 1 or 21. Each in-tree citation and the figures gate's ARMS
     table were updated. The earlier sections of this body cite their own heads.
3. **A late grant that carries `err`** (R437-2 S2, cheap, taken). The harness's backend can
   now fail a command on the grant that takes it (`gnt_err_with_grant`,
   `sim_main.cpp:173`, `:494`, `:552`). T24 grades the late registered grant that carries
   it: DEADLINE, nothing owed, and the next commit served at once
   (`late_grants_that_leave_nothing_owed`, `:1936-1972`, split out of T24 to keep it under
   the parent's 100-line function rule). X20, run as D31, fails 2 of 356. D11, which drops
   both terminals, now fails 4.
4. **RESIDUE R436-2 R1 and R2, in the reviewer's exact text.**
   - The README sentence now reads "… as its end. T24, T28 and T29 grade all of it at
     `TMO` = 100, …".
   - T29's withheld bytes are the payload READ's 11th and the WRITE's 21st.
   - The same two ordinals are corrected in this body's Round 2 item 4.
5. **Main moved.**
   - **The merge.** Before this post `origin/main` was `88969246`: PR #144 (lane C8, the
     descriptor model lint) had merged at 21:50Z. It was merged with
     `git merge --no-ff`, parents `f4519fe` and `88969246`.
   - **The one conflict** was 09's new section: both sides appended an §8.5 before
     "To add once …". Both are kept. C8's "The descriptor model lint" keeps §8.5, since it
     merged first. This lane's section follows it as **§8.6**, and §8.2's pointer reads
     "the port's own deadline, resets and handshake models are §8.6's". No other file in
     the tree cites this lane's section by number, and C8's "09 §8.5" citations
     (`00_MILAN_COMPLIANCE_REVIEW.md`, the `tb/desc_store` README) still name its own.
   - **Auto-merged:** 01, 07 and the integrator guide. In each, every hunk of either side
     survives intact, and every file only one side changed equals that side.
   - **Re-run.** The merge changed `KL_aecp_desc_store.sv`, the descriptor generator,
     `tb/desc_store` and docs. Every gate that reads them was re-run at `46796bf` (below).
     Gates whose inputs the merge left byte-identical stand as measured at `f4519fe`: the
     figures gate, the reviewers' scripts, the out-of-context cost and the SRP campaign.
     `git diff f4519fe 46796bf -- tb/nvm_port hdl/packet_engine tb/common` is empty, and
     the SRP campaign reads only `hdl/common` and `hdl/srp`.
   - **Main moved again.** At the next fetch before this post it was `c74711d4`: PR #146 had
     merged at 23:58Z. It adds `--jobs N` to eight mutation drivers, through a shared
     `tb/common/mutant_pool.py`, and updates their READMEs. It was merged the same way:
     `527662d`, parents `46796bf` and `c74711d4`, no conflict. Every file it changed equals
     main's, and `hdl`, `docs`, `tb/nvm_port` and `tb/acmp_nvm` are unchanged by it.
   - **Re-run after the second merge** (below): the eight changed campaigns, at their
     default `--jobs`, the docs gates and the parent's light gates (1-11), whose idiom
     ratchets scan the new Python. Nothing else reads a file that merge changed.

**The issues after round 3:** unchanged from round 2b. Every finding was a test or harness
gap, and item 2 adds a refusal no acceptance item depends on, so #15, #18, #19, #20 and #21
are met in full and all five close.

### Round 3 validation

Pinned Verilator 5.050. Every processor command ran on a `git archive` export, except the
figures gate, which ran in the lane tree (clean afterwards). All rc 0. The gates ran in
three waves:
- at `f4519fe`, the last round-3 commit;
- at `46796bf`, the first merge, for every gate that reads a file it changed;
- at the head `527662d`, the second merge, for every gate that reads a file it changed.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh`, at `f4519fe` and `46796bf` | 0, 0 | UPC map gate (61 constants, 89 entry points), M9 opcode gate (30); 33 suites, 1,020,123 checks, 0 failing; 1,326 s and 1,284 s. `nvm_port` 1,104 = 356 at each of 100, 37 and 20, and 9 in each of the four randomized builds (686 in round 2). `acmp_nvm` 388, `pp_top` 9,168, `timer_map` 1,360 and `desc_store` 584 are unchanged |
| `make -C tb/nvm_port figures`, at `f4519fe` (its inputs are byte-identical at the head) | 0 | 129 builds: 1 baseline, 7 for `make run`, 12 arms, 95 mutations and probes, 9 models, 5 matrix. Baseline 356/356; `make run` 356 x 3 and 9 x 4, all PASS; all measured figures agree; one waiver (2 illustrative phrasings); 1,203 s |
| CI's docs job one by one, `make check`, `gen_matrix.py --check`, at all three | 0, 0, 0 | 41 mermaid + 18 WaveDrom; links 1,060 since the first merge (1,045 before); REQ matrix 115 rows, 17 GAP; module matrix 94 rows, 0 untested; parameters 28 = 28 = 28 |
| `./scripts/lint_hdl.sh`, `./syn/yosys/run.sh`, at `f4519fe` and `46796bf` | 0, 0 | 41 modules, LINT OK; 36 tops and the Xilinx memory-map check |

**Campaigns.** Every campaign that builds the top was run at `f4519fe` and `46796bf`. The
eight whose drivers #146 changed were run again at `527662d`, at their default `--jobs`.
Every arm's verdict equals the earlier waves', and round 2b's:

| Campaign | rc | Result |
|---|---:|---|
| `python3 tb/pp_top/d3_mutants.py --jobs 3` | 0, 0 | goldens PASS; **87 of 87 KILLED** by their named checks; 2,821 s and 2,535 s |
| `make -C tb/pp_top aecp-mutants`, `aecp-dispatch-mutants` | 0, 0, 0 | 55 of 55 (5 controls), 37 of 37 (4 controls) KILLED |
| `make -C tb/maap mutants`, `tb/adp_engine mutants` | 0, 0, 0 | 29 of 29 (3 controls), 30 of 30 (2 controls) KILLED |
| `make -C tb/srp_top mutants`, at `f4519fe` and `527662d` | 0, 0 | 78 of 78 KILLED, assertion coverage 65/65, 11 controls |
| `tb/pp_top/acmp_mutants.py`, `notify_mutants.py` (`--jobs 2`) | 0, 0 | 19 of 19, 40 of 40 KILLED, goldens PASS |
| `tb/pp_top/gsi_mutants.py`, `name_wr_mutant.py` | 0, 0 | 20 detected, golden and restored PASS; `decode` killed |
| `tb/srp_admission/mutants.py`, `tb/acmp_talker/retry_mutants.py` (`--jobs 2`), at `527662d` | 0, 0 | 12 of 12 PASS; 62 mutants killed, 7 equivalence controls, 1 performance control, baseline and restored rc 0 |

**The reviewers' own scripts at `f4519fe`.** The copies are byte-identical to the packets,
except R437-2's `probe.py`, whose one `HEAD =` line names `f4519fe`. Their inputs are
byte-identical at the head.

| Script | Result |
|---|---|
| R436-2 `plant.py` (all plants, four models, its own fuzz at 37 and 3) | every plant that is not equivalent fails a named check under every model; Q1 fails T30a and RW4, Q9 fails T30c-e and RW4; the head is 0 everywhere |
| R436-2 `directed.py` | the head passes R436d-f in all three suite builds; Q1, Q9, Q2 and D26 fail them and T30 |
| R436-2 `rerun_round1.py` | every round-1 probe fails its named check as before; W6 on the round-1 source now fails under the pristine model too (T30a, T30b) |
| R436-2 `pause_fuzz.cpp`, legal, silent, resume and babble at 1, 2, 3, 37 and 100 | 0 false DEADLINEs, silent exact, resume served iff r <= TMO; babble answers every waiting request (196-224 per bound) |
| R437-2 `spec_y_pause.py`, `spec_z2_directed.py` | Y1, Y2, Y5-Y11 and Y13-Y16 fail named checks under every model run at 100 and 37; Y3, Y4 and Y12 0; Z1a, Z1b and Z2 pass on the head under the seven legal models and fail on Y1, Y11 and Y16 |
| R437-2 `spec_bounds.py`, `spec_bounds2.py`, `spec_babble.py`, `spec_r1_reprobe.py` | pristine, coincident, unsolicited and lazy erase 0 FAIL at 20, 21, 64, 1,000 and 1,001, and coincident 0 FAIL at every bound from 200 to 100,000; BABBLE 358/0; round-1 probes as above |

**Parent consumer set (16)** at milan-fpga dev `cdf49d1a`, in scratch copies built as in
round 2: a `git archive` of the trusted checkout (984 index entries), gptp-processor
`5dce647a` and verilog-axis `48ff7a7e` at their pins, and the patches each applied after a
clean `git apply --check`, with the porcelain empty.

- **At `f4519fe`, with `parent-adoption-c4c6-ea3fb388.patch` then
  `parent-adoption-p2-cdf49d1a.patch`: all 16 rc 0.**
- **Since the first merge, with those two patches alone: gates 10 and 15 fail, on main's
  change and not this lane's.** The other 14 are rc 0 at `46796bf`, and 1-9 and 11 again
  at `527662d`.
  - C8's packer now lints by default (07 §3.1 L1-L12), and refuses the parent's 8x8 model:
    "L1 port-cluster-minimum … a Stream Port contains at least one AUDIO_CLUSTER".
  - `sw/builder/test_builder.py` stops on that refusal (`test_listener_buffer_contract`).
    `milan_dp`'s image generator emits no image, so its NxN leg fails 117 checks that need
    the descriptor image.
  - Plain main `88969246` with the same two patches fails gate 10 with the same traceback.
  - PR #144 states that the parent needs `parent-adoption-c8-cdf49d1a.patch` for these
    gates. It is published on milan-fpga's `ppC8-review-evidence` branch (sha256
    `aa5a88eb…`, 8,482 bytes, as PR #144 records).
- **With c4c6, then C8's patch, then p2: all 16 rc 0**, with results equal to `f4519fe`'s.
  - Gates 1-11 ran at `46796bf` and again at `527662d`; gates 12-16 ran at `46796bf`.
  - #146 changed no file those five read: it touched only campaign drivers, their
    READMEs and `tb/common/mutant_pool.py`.
  - The c8 and p2 patches touch disjoint files.

| # | Command | `f4519fe`, c4c6 + p2 | merges, c4c6 + c8 + p2 | Result |
|---:|---|---:|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | 0, 0 | every ratchet within budget: long function 0 <= 0, multi-declarator 0 <= 0, build without warnings 0 <= 0 (`fuzz_main.cpp` and the third `-CFLAGS` group included); Python long module 10 <= 10, undocumented public function 0 <= 0 (300 modules at the head) |
| 3, 4 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | 0, 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `check_port_contracts.py` | 0 | 0 | processor 1,757 ports (unchanged), undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 0, 0 | 96 candidates, all recorded; 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 8, 9 | `docs_check.py`, `xvlog_gate.py --check` | 0, 0 | 0, 0 | 0 findings over 185 md + 956 files; 4 findings == ratchet, the same four |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | 0, 0 | 0, 0 | all gates pass except gate 11, not run (it needs a local build tree, as before); 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 0 | 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 0 | 9 benches RESULT: PASS; the mutant arms caught |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 0 | 65 + 152 checks, 0 failures; 5 of 5 leg-defect arms caught |

### Round 3 parent-visible list

1. **No port or parameter change.** `KL_pp_shadow` needs no edit; the parent's port-contract
   count is unchanged (1,757 processor ports).
2. **One behaviour change at the device face.** After a deadline, a backend that keeps
   presenting an abandoned READ's bytes past its length is no longer drained. The port
   takes the bytes the READ still owes and no more, and the next request ends DEADLINE until
   the backend ends the READ or a reset. `KL_nvm_backend` and the parent's responder never
   present more than a READ's length, so nothing changes with them.
3. **The patches are unchanged**: `parent-adoption-p2-cdf49d1a.patch` (sha256
   `3dda8509...d08b`, 9,728 bytes) and `parent-adoption-c4c6-ea3fb388.patch` (sha256
   `67bcd698...7bd7c`, 2,687 bytes). The banner sentence the p2 patch paraphrases is
   unchanged. Its "drains an owed read's bytes" still holds, since bytes past a READ's
   length are not the READ's.
4. **Processor documents the parent reads:**
   - 02 §8: the drain's bound;
   - 09 §8.6, renumbered from §8.5 by the merge: T28f, T30, the randomized harness, the
     three builds, D27-D31 and the plants;
   - this round changes none of F01.5, F08.1, the integrator guide's NVM rows and
     diagram 21, and the parameters stay 28 = 28 = 28.
5. **Adopting this head needs C8's patch too.** The head carries main's C8, so a parent
   moving its processor pin here applies `parent-adoption-c4c6-ea3fb388.patch`, then C8's
   `parent-adoption-c8-cdf49d1a.patch`, then `parent-adoption-p2-cdf49d1a.patch`, as above.
   With c4c6 and p2 alone, gates 10 and 15 fail on C8's default lint (validation, above).

### What remains after round 3

- Hosted CI and the reviewers' re-review at this head. The review scripts run at this head
  unchanged, except R437-2's `probe.py` with its head pin updated. Every reviewer plant
  that is not equivalent fails a named check.
  - The one probe that cannot run is R437-2's T6 attribution probe (`spec_t6stage.py`). Its
    anchor was the old staging line, which T6 no longer has.
  - R437-2's `spec_babble.py` now passes (358/0).
- As before:
  - R437-1's residue R2-R5;
  - the three `*REQ` error arms no phase arms;
  - the randomized commit cut points `09_verification.md:56` asks for. The new randomized
    harness grades the deadline, not cut points.
