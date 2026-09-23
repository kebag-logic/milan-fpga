# [A218] HANDOFF — processor #92 and #93, one lane

- Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`
- Branch: `92-93-boot-restore`, base `main` at `fbc1f7156d711e5b7f511da8a16d9494256b017b`
- Head: `3691340` (full hash in `logs/gate-summary.txt`; not pushed; no PR opened)
- Commits (one-line subjects, no trailers):
  - `3bde3c3` Hold the ACMP listener's work faces from reset until the binding walk ends (#92)
  - `daab6a5` Name the NVM port's error cause, bound the binding walk's reads and drain an abandoned read (#93)
  - `d6448ab` Grade the talker-event level against the binding walk's read deadline (#93)
  - `3691340` Record the gate-deleted pp_top mutant at the current check count (#92)
    (README only)
- State: both issues implemented, every gate green, tree clean. `hdl/srp/*` untouched
  (`git diff --stat fbc1f715..HEAD -- hdl/srp` is empty). Independent reviews pending.
- Session note: the previous session was cut by a usage limit after `3bde3c3` with the
  #93 work uncommitted. This session kept that work, fixed the two failing N5b checks
  (the stall counter read one past its bound for a cycle after expiry, and the check
  keyed on the header command rather than the drained operation), added N5c, N6, N7 and
  pp_top BW3, re-measured every figure, wrote the docs, and committed.

## What changed

### #92 (commit `3bde3c3`)
`KL_pp_acmp_lsn_admit` (new, `hdl/acmp/`) sits in `protocol_processor_top` in front of
the listener's four work faces and owns them from `rst_n` until the binding walk's
drained terminal: dispatch transaction and talker event held at their producers (valid
and ready both masked), START/STOP valid masked (completion passes), listener-owner
expiries refused and counted. The top's `restore_done_o` is the shadow's terminal AND
the release. The listener is unchanged. Contract: `docs/architecture/05_acmp_engine.md`
§5.1; integrator/operator guides; `tb/lsn_admit` (unit), `tb/acmp_nvm` group L,
`tb/pp_top` section BW.

### #93 (commits `daab6a5`, `d6448ab`)
- **S1 port**: `KL_pp_nvm_port.nvm_err_cause_o[1:0]` (1 DEVICE, 2 UNFRAMED, 3 reserved,
  0 without err).
- **S1 manager**: `KL_acmp_nvm_shadow` takes a zero-byte err as the per-record default
  only when UNFRAMED; a zero-byte DEVICE err fails the whole walk.
- **S3**: the shadow's read phase (`H_RS_REQ`, `H_RS_STREAM`) has a no-progress deadline
  `RS_TMO_CYC_P`; expiry fails the whole walk and, if a read was issued, pulses
  `nvm_abort_o`. New `restore_cause_o` (1 torn, 2 device, 3 deadline).
- **Arbiter**: `KL_pp_nvm_mgr_arb` (new, `hdl/packet_engine/`) between the port and two
  managers (shadow = manager 0; manager 1 tied idle in the top for the future D3
  writer). Per-operation ownership; manager 0's busy covers manager 1's grant cycle;
  an abandoned READ is drained (rready held, bytes and ending swallowed, no grant) until
  the device's own done/err, never on time.
- **S4**: delivered by the #92 gate; #93's extra faces are graded here (L01-L07, N7).
- **Top**: `NVM_RS_TMO_CYC_P = CLK_HZ_P / 50` (20 ms) passed to the shadow; arbiter
  wired between shadow and port; `restore_cause_o` kept internal.
- Docs: 01 F01.5 (`P-NVM-RS-TMO-CYC`), 02 §8 (`err_cause`) and new §8.2 (the arbiter),
  05 §5.1 ("the walk always ends"), 07 §5.3 (how a walk ends: the per-record vs
  whole-walk table), 08 F08.1 (`T-NVM-RS-DEADLINE`), integrator and operator guides,
  dataflow diagram caption, module matrix, yosys top list.

## Interface and parameter decisions recorded (for the reviewers and the parent)

1. `KL_acmp_nvm_shadow.RS_TMO_CYC_P` default 2,000,000; top `NVM_RS_TMO_CYC_P` default
   `CLK_HZ_P / 50` (20 ms at the reference 100 MHz). Documented as `P-NVM-RS-TMO-CYC`
   and `T-NVM-RS-DEADLINE`. It is a clock counter in the manager, not a timer slot.
2. Progress is the awaited event **at the manager face**: the port collects and checks
   the 8-byte header before forwarding, so that lag counts toward the stall (N5 measures
   it, 10 cycles on the bench, and places the boundary against it). The counter clears
   on expiry.
3. `restore_cause_o` is **not** exported at the top (an internal wire): a new top output
   would change the consumer's instantiation, which is the parent's T1/T4 surface. The
   D3 integration can export it.
4. **Consumer-visible behaviour change**: a device face that answers a READ with `err`,
   or with `done` before the eight header bytes, now fails the whole walk
   (`restore_fail_o`, cause 2) instead of reading blank. A blank or unbacked face must
   answer as erased media (grant, deliver the requested bytes as 0xFF, `done`). This is
   exactly the issue's S1 contract (C01/C03), and the integrator guide says so; the
   parent's consumer gates must use a device model that does the same.
5. `restore_fail_o` at the top now also covers a device error and the deadline; a
   failed walk of any cause reports `restore_blank_o`.
6. Manager 1 of the arbiter is tied idle in the top until the D3 writer lands.

## Not done here, stated so nobody relies on it

- Issue #15 is not delivered: the port has no deadline or cancellation. A device that
  never ends an abandoned read keeps the port quarantined until reset (graded: N3,
  documented 02 §8.2, 07 §5.3, operator guide). #15 and #20 stay open; this work
  relates to both (#20's zero-byte-DEVICE-as-blank defect is the B02 arm, now red).
- The issue's cost estimates were not re-measured (the out-of-context instrument is not
  in this lane).
- Evidence cases that need the D3 writer (L13 roll-back; "before the D3 terminal") have
  no subject in the processor: there is no D3 writer. Service after the release
  depends on nothing else, and "before the enable" is graded at the top (BW1, BW3 with
  `entity_enable_i` low).
- The evidence repository's own `run.py` recipe was not executed (no other checkouts in
  this lane). The pinned L05 control was reproduced in the product repository instead:
  the `acmp_nvm` bench built with the pinned wiring (`make pinned`,
  `ACMP_NVM_PINNED_WIRING`: producers wired straight to the listener as the base top
  wires them, listener/shadow/port RTL as at base) fails L05a with
  "sink 0 holds 000000000000000000000000" — `logs/92-L05-pinned-wiring-base.log`
  (58 of 190, taken before the fix) and `logs/93-acmp_nvm-pinned-wiring.log` (96 of 332
  at head).
- The parent-side reconciliation of the normative documents named in the parent
  contract's §15.1 is the parent's.

## Reproduce (from the repository root)

```sh
export PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH  # simulator 5.050
make -C tb/acmp_nvm            # 332 checks, exit 0
make -C tb/acmp_nvm pinned     # control: exit non-zero, 96 of 332 fail, L05a among them
make -C tb/nvm_port            # 136 checks
make -C tb/nvm_port figures    # README figures, C1-C4 included; exit 0
make -C tb/pp_top              # 1427 checks (1407 + 20)
./scripts/run_suites.sh        # 31 suites, 15237 checks, exit 0
./scripts/lint_hdl.sh          # exit 0
make check                     # diagrams, wavedrom, links, matrix, gen_matrix --check, stale
./syn/yosys/run.sh             # exit 0
git diff --check fbc1f715..HEAD
```

Mutants: `tools/mutate.py NAME SUITE FILE OLD NEW` (backup, mutate, run, restore; the
log lands in `logs/93-<suite>-mutant-<NAME>.log`). The exact OLD/NEW strings are in the
first lines of each log.

## Receipts (`logs/`)

| File | What |
|---|---|
| `gate-summary.txt` | every gate at the head |
| `gate-run_suites.log`, `suite-*.log` | the suite runner and each suite (from clean build dirs) |
| `gate-lint.log`, `gate-make-check.log`, `gate-yosys.log`, `93-nvm_port-figures.log` | the other gates |
| `92-L05-pinned-wiring-base.log`, `93-acmp_nvm-pinned-wiring.log` | the L05 control at base wiring |
| `92-pp_top-mutant-LG01-gate-deleted.log`, `93-pp_top-mutant-LG01-gate-deleted.log` | pp_top with the gate deleted (M32), at 1,401 and at 1,407 checks: 5 FAIL each |
| `93-acmp_nvm-mutant-*.log` | 15 mutants at 332 checks |
| `93-pp_top-mutant-B01*.log`, `93-pp_top-mutant-B03*.log` | pp_top M33, M34 |

## Posted

- #92 REVIEW READY: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/92#issuecomment-5804802940
- #93 REVIEW READY: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/93#issuecomment-5804806453
- No TAKEN comment was posted in either session.

## Next steps

1. Two independent reviews (requested in the REVIEW READY comments on #92 and #93).
2. The manager runs the parent consumer gates against this head; watch item 4 above
   (device models that answer err or a short header on a blank boot now see
   `restore_fail_o`).
3. After review: push, PR with `PR-BODY.md`, merge by the manager.
