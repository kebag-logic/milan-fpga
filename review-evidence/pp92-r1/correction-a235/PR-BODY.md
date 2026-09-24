[A235] Boot restore: a read-only command can no longer erase a saved binding, even after a failed walk, and the binding walk always ends

Closes #92
Closes #93

Relates to #15 (the port still has no deadline or cancellation; an abandoned read that the device never ends keeps it quarantined until reset) and #20 (a zero-byte DEVICE error is no longer read as a blank region). Neither is closed here.

## What changes

**#92: the listener belongs to the binding walk until the walk ends.** A new `KL_pp_acmp_lsn_admit` sits in `protocol_processor_top` in front of the ACMP listener's four work faces. The listener itself is unchanged. From `rst_n` the gate:

- holds the dispatch transaction and the talker event at their producers, masking both valid and ready, so a pop is exactly a take;
- masks the START/STOP valid (the completion passes, and none can fire while the listener's holder is empty from reset);
- refuses and counts listener-owner timer expiries.

It releases once, when all of these hold:
- the shadow's walk has reached its terminal, failed or not;
- no preload is presented;
- the listener is idle;
- its last A4 arm has gone.

The top's `restore_done_o` is that terminal AND the release, and `restore_busy_o` covers the gap between them. A read-only `GET_RX_STATE` in the window is answered after the walk from the restored image, and a later BIND or UNBIND still wins because it comes later. The contract is in 05 §5.1.

**#92 after a failed walk: the walk rejects the image, not the media.** After the atomic reject the listener runs on its defaults and writes its record back for every command it serves. `KL_acmp_nvm_shadow`'s capture compare now treats two unbound records as equal whatever their other fields hold: an unbound record carries no binding, and no walk preloads one. So a read-only `GET_RX_STATE` after a failed walk writes nothing, whether it was held from the boot window or is a later poll, and the next boot on a healthy device restores every saved binding. A BIND still replaces its sink's record, and an UNBIND of a bound sink is still written. This is in 07 §5.3 ("A failed walk keeps the saved records").

**#93 S1: the port names its error.** `KL_pp_nvm_port.nvm_err_cause_o` returns 1 DEVICE (any device error, or a header read the device ended short) or 2 UNFRAMED (a header the port refused after the device delivered it whole, or a bad commit header). It reads 0 whenever `err` is low. The binding manager treats a zero-byte err as the record's default only when the port says UNFRAMED. A zero-byte DEVICE err fails the whole walk.

**#93 S3: the walk's read phase has a deadline.** `KL_acmp_nvm_shadow` gains `RS_TMO_CYC_P` (top: `NVM_RS_TMO_CYC_P`, default `CLK_HZ_P/50` = 20 ms), and a value below 1 is refused at elaboration. If the walk waits that many consecutive clocks with no progress, the whole walk fails. A silent device therefore ends the walk: the listener is released and answers on defaults, and an enable gated on `restore_done_o` follows. A new `restore_cause_o` reports 1 torn, 2 device or 3 deadline.

When an issued read is abandoned, the manager pulses `nvm_abort_o` to a new `KL_pp_nvm_mgr_arb` in front of the port. The arbiter drains that read: it holds rready, swallows the bytes and the ending, and grants no manager until the device ends the read. That arbiter's manager 1 is tied idle in the top for the future saved-state writer.

**#93 S4** is the #92 gate. #93's further faces are graded here: the talker-event level, START/STOP, expiries, and the level combined with the deadline.

**Guides.** The operator and integrator guides now say what each NVM tie-off reports:

| Behind the device face | Done | Failed |
|---|---|---|
| erased media (each byte 0xFF, then done) | 1 | 0, blank |
| a face that errs, or ends a read before the 8-byte header | 1 | 1 (device) |
| a face that never answers | 1, at the deadline | 1 (deadline), port quarantined |

`restore_go_i` stays outside the tie-off: it must be pulsed on every boot.

## Decisions for review

1. The deadline counts clocks at the manager face, so the port's 8-byte header-collection lag counts toward the stall. N5 measures that lag and places its boundary against it.
2. `restore_cause_o` is not exported at the top. A new top output would change the consumer's instantiation, which belongs to the parent's integration surfaces.
3. **Consumer-visible:** a device face that answers a READ with `err`, or with `done` before the eight header bytes, now fails the walk instead of reading blank. This is the S1 contract. A blank or unbacked face must answer as erased media (0xFF bytes, then `done`), and the integrator guide says so.
4. `restore_fail_o` now also covers a device error and the deadline, and a failed walk of any cause reports `restore_blank_o`.
5. **After a failed walk, a command that leaves a sink unbound writes nothing.** This includes an UNBIND of a sink the failed walk left unbound: the listener cannot tell it from a GET, since both restate an unbound record. That sink's saved binding therefore returns on the next healthy boot. The alternative, persisting every unbound write-back, is exactly the loss #92 forbids. The behaviour is stated in 07 §5.3 and the operator guide, and graded in acmp_nvm N8b.

## Evidence

All results are from the CI-pinned simulator 5.050, starting from clean build directories.

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | 31 suites, 15,797 checks, exit 0 |
| `make -C tb/nvm_port figures` | exit 0, every README figure re-measured |
| `./scripts/lint_hdl.sh` | exit 0, 39 of 39 |
| `make check` (links, matrix, `gen_matrix --check`, wavedrom, stale) | exit 0 |
| `./syn/yosys/run.sh` | exit 0 |
| `git diff --check 09f9bf38..HEAD` | clean |
| parent `scripts/check_cpp_idiom.py`, `scripts/check_py_idiom.py`, gitlink at this head | exit 0, every ratchet at its budget, none widened |

**Control (the recorded L05 failure):** `make -C tb/acmp_nvm pinned` builds the same bench with the producers wired straight to the listener, as the base top wires them. It exits non-zero with 107 of 349 checks failing. Among the failures is L05a, `sink 0 holds 000000000000000000000000`, with an unbound reply and a reset that restores nothing.

### Every correction's failing arm

Each arm fails a completed-scenario assertion. None relies on a timeout or a process failure. Counts are at 349 acmp_nvm checks and 1,414 pp_top default-build checks.

| Arm | Suite | Result |
|---|---|---|
| gate deleted (pinned wiring) | acmp_nvm / pp_top | 107 of 349 / 8 of 1,414 (BW1-BW4) |
| transaction valid admitted / ready passed | acmp_nvm | 71 / 45 |
| talker valid admitted / ready passed | acmp_nvm | 19 / 7 |
| expiries admitted / START-STOP admitted | acmp_nvm | 5 / 12 |
| release without the terminal | acmp_nvm | 108 |
| port cause deleted / collapsed to DEVICE / to UNFRAMED / ungated | nvm_port | 10 / 4 / 6 / 1 of 136 |
| zero-byte err read as blank (#20's defect) | acmp_nvm | 12 (N1a-d, N8b, N9b) |
| UNFRAMED failing the walk | acmp_nvm | 120 of 342 (A2, the F4 blank boot, N9c) |
| walk cause collapsed | acmp_nvm | 13 |
| no read deadline | acmp_nvm / pp_top | 20 / 2 (BW3) |
| abort never raised | acmp_nvm | 15 |
| abandoned read not drained | acmp_nvm / pp_top | 10 / 2 (BW3) |
| arbiter grant-cycle busy term deleted | acmp_nvm | 1 (N6: 92 of 200 offsets lose the walk) |
| capture compare without the unbound rule (a failed walk's GET persisted) | acmp_nvm / pp_top | 9 (N8a-c) / 2 (BW3: byte 8 `03 -> 00` before any BIND) |
| top `restore_done_o` without the release | pp_top | 2 (BW4) |
| top `restore_busy_o` without the gap term | pp_top | 1 (BW4) |

### New and extended cases

- `tb/nvm_port` T23a-k: each cause case, graded from a reset of its own.
- `tb/acmp_nvm`, with the real listener, gate, shadow, arbiter and port:
  - L00-L22 and L01-L07: every work face, from reset and against the later sink, including L05s at every presentation cycle.
  - N1-N7: device error, UNFRAMED, silence in both read states, the deadline boundary one cycle each side, a drain the device ends 2,000 cycles late, the arbiter race, and the talker level at the deadline.
  - N8a-c: sinks 0, 3 and 7 are saved and the walk fails after storing sink 0, with cause 1, 2 or 3. A GET held through the window, a GET of each saved sink afterwards and (N8b) an UNBIND of a sink the walk left unbound are answered on the default. Nothing is written, every saved record stays byte-exact, and a healthy reset restores all three.
  - N9a-c: the unwired faces as the integrator guide states them. No grant gives cause 3 and quarantines the port. Err on every READ gives cause 2. Erased media gives done, not failed, blank, and nothing written.
- `tb/pp_top`:
  - BW0-BW2: a saved binding, a GET before and inside the walk, and a reset round trip.
  - BW3: a device silent mid-walk. The walk fails at its deadline and the held GET is answered on the default before the enable. The late read is drained, and every flush then runs out with sink 0's saved record untouched. A BIND then persists, and a reset restores it.
  - BW4: in every cycle of every walk of the run, `restore_busy_o || restore_done_o` holds, `restore_done_o` never reads 1 while the gate owns the listener, and no preload write or discovery arm lands at or after `restore_done_o`.
- `tb/lsn_admit`: the gate on its own against a model, including every release term.

### Review round 1 (R278-1, R279-1 at 156c206c)

| Finding | Resolution |
|---|---|
| R278 F1 = R279 F3 (MAJOR): a read-only GET after a failed walk erased saved bindings | Capture compare's unbound rule, acmp_nvm N8a-c and pp_top BW3; reviewer probes P1 16/16, P2 PASS, FW 358/358 at this head (all failing at 156c206c) |
| R278 F2 = R279 F2: the top's done/busy composition had no arm | pp_top BW4; both reviewer mutants killed |
| R279 F1: the guides described an unwired face as done without fail | operator §6 table, integrator tie-off cell and §7 qualified; acmp_nvm N9a-c |
| R278 S1, R279 S4, R279 S5 | deadline guard at elaboration, PNG re-rendered, port comment corrected |
| R279 S1, S2, S3, S6 | not taken; optional |

### Not covered here

- The issue's cost estimates were not re-measured.
- The cases that need the D3 writer have no subject in the processor.
- The parent's §15.1 reconciliation is the parent's work.
