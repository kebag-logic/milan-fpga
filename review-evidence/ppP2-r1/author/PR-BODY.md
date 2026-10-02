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
