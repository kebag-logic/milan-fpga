<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# nvm_cosim -- the saved-state snapshot ownership co-simulation

This suite grades the contract of
[`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`](../../../docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md)
against the shipping pair: `hdl/milan/KL_nvm_backend.sv` and the writer in
`sw/firmware/milan_baremetal/milan_baremetal.c`, compiled for the host with
its two CSR primitives routed to the model, exactly as
`sw/firmware/nvm_hosttest` routes them.

`tb/verilator/nvm_backend` grades the same module and is not replaced by this
one. That suite grades the module's byte pump, its region decode against a
byte-exact KLJ2 image and its section 9 status, against a harness that drives
the device face directly. This suite grades the PAIR against ORDERINGS: the
acknowledgement race of issue #418, the ERASE-error counterexample, the
one-pulse re-arm failure of issue #420, the capture hold, the window load, the
identity an acknowledgement quotes and the writer's restart. Neither is a
superset of the other, and both run in the sweep.

## Contents

- **[What is real here, and what is a model](#what-is-real-here-and-what-is-a-model)** -- The donor, the backend and the writer are real; the flash, the DDR and the clock are not, and no physical timing is.
- **[Running it](#running-it)** -- Four targets, and the one tally line the sweep counts.
- **[How a case is graded](#how-a-case-is-graded)** -- The case file is stimulus only; every verdict is a NAMED check over a decoded journal.
- **[Four ways this suite tries to show its checks are not vacuous](#four-ways-this-suite-tries-to-show-its-checks-are-not-vacuous)** -- A mutant per named check, an identity that must alias, an identity that must wrap, and the pre-contract source that must go red.
- **[The one expected failure](#the-one-expected-failure)** -- E3 without donor scope D1, labelled with its reason and its donor issue.
- **[Files](#files)** -- What each file in the suite is.

## What is real here, and what is a model

REAL, at the pinned revision:

- `KL_acmp_nvm_shadow`, the binding record manager -- the only record writer
  the donor has -- with its own debounce and its bounded retries;
- `KL_pp_nvm_port`, the device-face initiator, including its rule that
  `dev_req_o` is held until `dev_gnt_i`, which is what makes a deferral a
  withheld grant rather than a refusal;
- `KL_aecp_dyn_state`, the AECP dynamic-state store whose sticky level the
  parent consumes as `pend_i`;
- `KL_nvm_backend`, the shipping file;
- the shipping writer, the shipping generator's constants, and the
  repository's own `scripts/nvm_klj2.py` decoding the journal the oracle
  compares against records it frames independently.

A MODEL, in `cosim_host.c` and `cosim_bridge.cpp`: the flash (with injectable
erase, program and read-back failures and one 3 s erase), the reserved DDR
window, the clock, and `PP_STAT`, which is composed from the RTL's outputs the
way `hdl/common/csr/milan_csr.sv` composes it. `cosim_top.sv` carries the
parent glue transcribed from `hdl/milan/KL_pp_shadow.sv`.

**NOT MODELLED, and it matters to every timing number this suite prints:** CPU
instruction time, DDR and bus latency and arbitration, clock-domain crossings,
the product's clock rate, and real flash timing. The backend clock is 1 MHz of
MODEL time, so one cycle is one microsecond and the hold, the deadlines and
the heartbeat are counted in it; firmware execution between two CSR accesses
takes zero model time. A hold "bounded at 50 ms" here is bounded in model
time, and the page's section 18 derives the real copy time separately.

The writer restart of W1 to W4 is modelled by returning every file-scope
variable of the writer to its initial value and running its boot again.
`run_cases.py` refuses to build it unless it names every such variable, so a
new static cannot survive the modelled reset unnoticed. NOTHING ELSE of a CPU
reset is modelled -- not the boot code's memory initialisation, not the memory
holding the live window, not the bus fabric -- so those four cases ASSUME
obligation O4 of the page and cannot test it.

## Running it

```sh
make            # every executed case of section 9 at BOTH shapes, the
                # identity control, the identity-wrap arm, and every mutant
                # the page names
make quick      # the shipping builds at 1x1 only: the local loop
make wrap       # the identity-wrap arm alone, at 2 identity bits, the
                # contract's minimum (issue #484 rounds 2 and 3)
make lint       # Verilator lint of the shipping module and the wrapper
```

`make` is what the sweep runs. It prints one tally line in the shape
`scripts/suite_tally.py` reads; the per-build lines are deliberately NOT in a
countable shape, or the sweep would add them to the total.

## How a case is graded

`cosim_cases.cpp` is STIMULUS ONLY: it drives the control face, the producer
and the injected failures, and dumps the journal slots and a status
observation at named points. Every verdict is taken in `run_cases.py`, which
decodes those slots and compares them with records it frames itself. A check
carries a NAME (`last_verified_kept@end:0x20`, `converged@end`,
`four_refusal_terminal_row@boot`), and that name is what the contract page
cites and what the mutant table below aims at.

## Four ways this suite tries to show its checks are not vacuous

1. **Mutants, each with ONE named killer.** `mutate.py` plants one defect in a
   copy of the shipping backend, the shipping writer or this suite's parent
   glue -- 39 of them, every one the page names -- and `run_cases.py` requires
   the SINGLE check the page names for it to go red. A mutant killed only by
   some other check fails the suite the same way a surviving mutant does: it
   was aimed at the wrong place. Seams are matched exactly and must hit once,
   so a line that moves breaks the build rather than compiling unchanged.

2. **The identity control.** A 2-bit capture identity MUST alias on `A8`,
   which is what makes the 16-bit one evidence rather than an assumption.

3. **The identity-wrap arm** (`make wrap`), which asks the opposite question
   of the same narrow build. The backend's identity is a plain wrapping
   counter (section 5.4), so one capture in every `2**CAP_ID_W_P` carries the
   identity 0; at 2 bits that capture is the fourth, INSIDE a case, where at
   the shipping 16 bits it is the 65,536th. Five cases are run at 2 bits and
   compared with THEMSELVES at 16: how many acknowledgements the writer
   strobed, how many commits it deferred for an unattested capture, and its
   own `commits ok`, `captures refused` and `acks refused` counters
   (`--status`) must all be the same, and at least one acknowledgement must
   quote the identity 0 -- one the WRITER strobed, never one a case injected
   at the device face, which is why the arm counts only `stray == 0`.
   Five pairs, five acknowledgements quoting 0. `C2`
   reaches a fourth capture unaided and is the only case here with a capture
   the backend genuinely does not attest, so the arm cannot be satisfied by a
   writer that has merely stopped refusing; the other four carry a commit
   tail (`--commits`, three further committing changes run after the case
   body and all of its observations) that takes them past the wrap. The tail
   is applied identically to both members of a pair, so the identity width
   stays the only thing that moves between the two runs.

   **Two bits, and nothing narrower.** `CAP_ID_W_P` outside `2..16` is an
   elaboration error the backend raises itself (`g_refuse_capid`), so this
   suite passes `-Werror-USERERROR` on every Verilator invocation, here and
   in `make lint`. `-Wno-fatal` alone would demote that `$error` to a warning
   nothing reads, and the arm would grade the shipping module in a shape the
   module disclaims and still print `RESULT: PASS`. The rule is
   [`docs/development/CODE_QUALITY.md`](../../../docs/development/CODE_QUALITY.md)
   under rule 6, "Where the contract is enforced, and where it is not".

4. **The pre-contract control, the direction a mutant cannot give.** With
   `LEGACY_DIR` pointing at a checkout of `KL_nvm_backend.sv` and
   `milan_baremetal.c` from before the contract:

   ```sh
   make control LEGACY_DIR=/path/to/pre-contract-sources
   ```

   the three historical defects MUST reproduce there -- `A2 :
   ack_retires_only_slot@post_ack:0x20` (#418), `B1 :
   last_verified_kept@end:0x20` (the ERASE-error counterexample) and `E1 :
   no_durable_claim_unmaterialized@end` (#420) -- and the suite refuses to
   report success if any of them passes on that source. Its other failures are
   printed as REPRODUCED, not as failures: they are the defects the contract
   answers, on the source they were reported against.

## The one expected failure

`E3_binding_inside_manager_debounce` at `d1=0` fails
`no_durable_claim@in_debounce`, and is labelled EXPECTED-FAIL with its reason.
It is a KNOWN LIMITATION, not a defect of this change: donor scope D1 of the
page's section 13 (one `protocol_processor_top` output port exporting the
binding manager's unflushed sinks) does not exist at the pinned processor, so
the parent cannot see a binding the manager is still debouncing and that
binding can read durable. It is filed as
`protocol-processor-control-plane-avb-milan` issue 90; `KL_pp_shadow.sv` ties
the term to zero at the one place it will connect. The same case at `d1=1`,
which models the export, passes.

The label cannot outlive the limitation: the expectation is keyed on the exact
`(case, variant, check)` triple, any other check of that case fails the suite
normally, and that check PASSING is reported as `UNEXPECTED-PASS` and fails
the suite too. So the round that lands donor scope D1 is told to retire the
label rather than inheriting a green run that still carries it.

## Files

| File | What it is |
|---|---|
| `run_cases.py` | builds every build, runs the cases, reports |
| `cosim_oracle.py` | what a container SHOULD hold, framed independently |
| `cosim_checks.py` | every named check, built over that oracle |
| `cosim_case_map.py` | which checks each case is graded by, and where it runs |
| `mutate.py` | the 39 named mutants and their exact seams |
| `cosim_top.sv` | the RTL wrapper: donor, backend and the transcribed parent glue |
| `cosim_cases.cpp` | the case scripts, stimulus only |
| `cosim_bridge.{h,cpp}` | the Verilated model, the clock and the CSR forwarding |
| `cosim_host.c` | the flash, the DDR window and `PP_STAT` |
| `cosim_api.h` | the C/C++ seam |
| `stubs/` | the headers the writer is compiled against on the host |
