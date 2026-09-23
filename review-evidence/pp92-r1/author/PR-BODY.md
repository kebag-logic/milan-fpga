[A218] Boot restore: a read-only command can no longer erase a saved binding, and the binding walk always ends

Closes #92
Closes #93

Relates to #15 (the port still has no deadline or cancellation; an abandoned read that the device never ends keeps it quarantined until reset) and #20 (a zero-byte DEVICE error is no longer read as a blank region). Neither is closed here.

## What changes

**#92: the listener belongs to the binding walk until the walk ends.** A new `KL_pp_acmp_lsn_admit` sits in `protocol_processor_top` in front of the ACMP listener's four work faces, and the listener itself is unchanged. From `rst_n` the gate:

- holds the dispatch transaction and the talker event at their producers, masking both valid and ready, so a pop is exactly a take;
- masks the START/STOP valid (the completion passes, and none can fire while the listener's holder is empty from reset);
- refuses and counts listener-owner timer expiries.

It releases once, when the shadow's walk has reached its terminal (failed or not), no preload is presented, the listener is idle and its last A4 arm has gone. The top's `restore_done_o` is now that terminal AND the release. A read-only `GET_RX_STATE` in the window is answered after the walk from the restored image, and a later BIND or UNBIND still wins because it comes later. The contract is in 05 §5.1.

**#93 S1: the port names its error.** `KL_pp_nvm_port.nvm_err_cause_o` returns 1 DEVICE (any device error, or a header read the device ended short) or 2 UNFRAMED (a header the port refused after the device delivered it whole, or a bad commit header). It reads 0 whenever `err` is low. The binding manager treats a zero-byte err as the record's default only when the port says UNFRAMED. A zero-byte DEVICE err fails the whole walk.

**#93 S3: the walk's read phase has a deadline.** `KL_acmp_nvm_shadow` gains `RS_TMO_CYC_P` (top: `NVM_RS_TMO_CYC_P`, default `CLK_HZ_P/50` = 20 ms). If the walk waits that many consecutive clocks with no progress, the whole walk fails. A silent device therefore ends the walk: the listener is released and answers on defaults, and an enable gated on `restore_done_o` follows. A new `restore_cause_o` reports 1 torn, 2 device or 3 deadline.

When an issued read is abandoned, the manager pulses `nvm_abort_o` to a new `KL_pp_nvm_mgr_arb` in front of the port. The arbiter drains that read: it holds rready, swallows the bytes and the ending, and grants no manager until the device ends the read. That arbiter's manager 1 is tied idle in the top for the future saved-state writer.

**#93 S4** is the #92 gate. #93's further faces are graded here: talker-event level, START/STOP, expiries, and the level combined with the deadline.

## Decisions for review

1. The deadline counts clocks at the manager face, so the port's 8-byte header-collection lag counts toward the stall. N5 measures that lag and places its boundary against it.
2. `restore_cause_o` is not exported at the top. A new top output would change the consumer's instantiation, which belongs to the parent's integration surfaces.
3. **Consumer-visible:** a device face that answers a READ with `err`, or with `done` before the eight header bytes, now fails the walk instead of reading blank. This is the S1 contract. A blank or unbacked face must answer as erased media (0xFF bytes, then `done`), and the integrator guide says so.
4. `restore_fail_o` now also covers a device error and the deadline, and a failed walk of any cause reports `restore_blank_o`.

## Evidence

All results are from the CI-pinned simulator 5.050, starting from clean build directories.

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | 31 suites, 15,237 checks, exit 0 |
| `make -C tb/nvm_port figures` | exit 0 (README figures re-measured; T23 added) |
| `./scripts/lint_hdl.sh` | exit 0 |
| `make check` (links, matrix, `gen_matrix --check`, wavedrom, stale) | exit 0 |
| `./syn/yosys/run.sh` | exit 0 (new tops `KL_pp_acmp_lsn_admit`, `KL_pp_nvm_mgr_arb`) |
| `git diff --check fbc1f715..HEAD` | clean |

**Control (the recorded L05 failure):** `make -C tb/acmp_nvm pinned` builds the same bench with the producers wired straight to the listener, as the base top wires them. It exits non-zero with 96 of 332 failing. Among the failures is L05a: `sink 0 holds 000000000000000000000000`, with an unbound reply and a reset that restores nothing. Before the fix the same control failed 58 of 190.

### Every correction's failing arm

Each arm fails a completed-scenario assertion. None relies on a timeout or a process failure.

| Arm | Suite | Result |
|---|---|---|
| gate deleted (pinned wiring) | acmp_nvm / pp_top | 96 of 332 (L01-L22, N) / 5 of 1,407 (BW1, BW2) |
| transaction valid admitted / ready passed | acmp_nvm | 55 / 40 of 332 |
| talker valid admitted / ready passed | acmp_nvm | 19 / 7 of 332 |
| expiries admitted / START-STOP admitted | acmp_nvm | 5 / 12 of 332 |
| release without the terminal | acmp_nvm | 97 of 332 |
| port cause deleted / collapsed to DEVICE / to UNFRAMED / ungated | nvm_port | 10 / 4 / 6 / 1 of 136 |
| zero-byte err read as blank (#20's defect) | acmp_nvm | 9 of 332 (N1a-d) |
| UNFRAMED failing the walk | acmp_nvm | 128 of 325 (A2, F4 blank boot) |
| walk cause collapsed | acmp_nvm | 9 of 332 |
| no read deadline | acmp_nvm / pp_top | 16 of 332 / 2 of 1,407 (BW3) |
| abort never raised | acmp_nvm | 13 of 332 |
| abandoned read not drained | acmp_nvm / pp_top | 9 of 332 / 2 of 1,407 (BW3) |
| arbiter grant-cycle busy term deleted | acmp_nvm | 1 of 332 (N6: 92 of 200 offsets lose the walk) |

### New and extended cases

- `tb/nvm_port` T23a-k: each cause case, graded from a reset of its own.
- `tb/acmp_nvm` (the real listener, gate, shadow, arbiter and port):
  - L00-L22 and L01-L07: every work face, from reset and against the later sink, including L05s at every presentation cycle.
  - N1-N7: device error, UNFRAMED, silence in both read states, the deadline boundary one cycle each side, a drain the device ends 2,000 cycles late, the arbiter race, and the talker level at the deadline.
- `tb/pp_top`:
  - BW0-BW2: a saved binding, a GET before and inside the walk, and a reset round trip.
  - BW3: a device silent mid-walk. The walk fails at its deadline and the held GET is answered on the default before the enable. The late read is drained, then a BIND persists and a reset restores it.
- `tb/lsn_admit`: the gate on its own against a model, including every release term.

### Not covered here

- The issue's cost estimates were not re-measured.
- The cases that need the D3 writer have no subject in the processor.
- The parent's §15.1 reconciliation is the parent's work.
