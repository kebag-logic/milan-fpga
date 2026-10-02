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
     the device never presents a payload READ's 10th byte. A second drops `wvalid` likewise
     while the device never takes a WRITE's 20th byte. Each ends in one err, cause
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
