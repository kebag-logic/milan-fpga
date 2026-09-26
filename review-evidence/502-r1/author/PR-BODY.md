[A338]

Closes #502

## Status

Local implementation and requested validation complete at `87e263fd1d71b1a7a04a2e9c9339220f35e4348f`.
Independent review and hosted checks remain outstanding.

## Description

SET_NAME and map edits could change live state before their NVM marks.
During that program tail, persistence status could still read durable.
The parent now samples accepted name writes and map phase 5 immediately,
then keeps them pending until reset. Later marks retain command-completion
semantics. No name/map record materializer is introduced.

Adopts processor `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`, connects `aecp_name_wr_o`, and regenerates the
ROM ledger and submodule diagram. Both saved-state contracts describe
the clock, acceptance and clear rules.

## How to reproduce

Run `make -C tb/verilator/pp_shadow pending-mutant`.
The clean real-command harness passes 159 checks.
The late-mark mutant fails K10 and K12, exposing 1881 falsely durable
cycles for the name change and 15 for each map direction.

## How to validate

All requested gate commands returned exit 0. The complete default sweep
passed all 55 suites and 2125050 checks with zero failures.
The focused shadow, NVM co-simulation and backend suites also passed.
The optional AAF/AVTP and gPTP field campaigns and their freshness checks
did not run because `tsn-gen` is absent; they contribute zero to that total.
Both full builder modes passed: pinned SDK and explicitly absent RV32
compilers. The unavailable board calibration report is excluded in both;
the absent mode also excludes the RV32 census, which the SDK mode covers.

The same-pin OOC comparison changes LUTs by -89. Flip-flops, LUTRAM,
BRAM and DSP counts remain unchanged. Firmware is unchanged, and the
capture census passes without remeasurement. The handoff records exact
commands, exit codes, logs, source hashes and all static/documentation gates.

## Definition of done

- Accepted live writes immediately revoke durable status.
- Real name and both map paths pass K10/K12.
- Unchanged commands, refusal, reset and acknowledgement controls pass.
- The late-mark mutant fails both named checks.
- Requested local gate commands pass and evidence is handed off.
- Independent review, hosted checks and merge remain with maintainers.
