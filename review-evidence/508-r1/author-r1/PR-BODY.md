[A274]

## Contents

- **[Status](#status)** -- Blocked on one decision; every other gate green; `508-pp-pin-adopt` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The public task and its reviewers.
- **[Description](#description)** -- The pin move, the seam, and what the new pin changed for the parent.
- **[Authoritative references](#authoritative-references)** -- Milan clauses and processor contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and submodules.
- **[How to validate](#how-to-validate)** -- The commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this does not do.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

BLOCKED on one decision, otherwise green at head `35f0695815c202392b6b4806bb9f59dd110687ed`.
Three parent gates in the required `docs-check` context refuse processor content new at `a8f8ce81`.
Each gate forbids the parent from adding the identity or raising the ratchet, and the fix is processor-side.

| Gate | Finding at the new pin | Processor PR |
|---|---|---|
| `scripts/check_port_contracts.py` | 7 literal-bound `u_nvm_arb.m1_*` connections in `protocol_processor_top.sv` with no rationale comment directly above their runs | #109 |
| `scripts/measure_naming.py --check` | `KL_aecp_desc_mem_guard:s_rsp_data_o` and `protocol_processor_top:srp_sr_admitted_o` document a unit their names lack | #110, #114 |
| `scripts/measure_test_evidence.py --check` | 3 new processor mutation drivers pass a host `timeout=`: wall-clock files 6 > ratchet 3 | #110, #111, #114 |

Recommended: a processor follow-up for the three, then this lane re-pins to the fixed main (gitlink, digest rows and pin text only).
The alternative is an explicit maintainer exception.
The parent-owned half is done here: the three new processor mutation drivers carry DUT-reader dispositions.

## Linked Issue / roles

Closes #508

Adopted processor changes (Mister-M-alt/protocol-processor-control-plane-avb-milan):

- #92 and #93 (PR #109): a saved binding survives boot restore; the walk has a deadline; the listener waits for the walk.
- #94 (PR #110): the descriptor-memory guard holds a late burst.
- #43 and #49 (PR #111): GET_STREAM_INFO selectors 5 and 7 are served from processor state, with no new port.
- #112 (PR #114): the admission grant stays low until the current TSpec is evaluated.

Executor: `[A274]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

| Piece | Change |
|---|---|
| Pin | `protocol-processor` `09f9bf38` -> `a8f8ce81`; ROM digests re-recorded with `syn/yosys/ooc.sh --record-rom-digests` (images unchanged); SUBMODULES.md, the generated submodule diagram and the CHANGELOG follow |
| Seam (#508) | `milan_datapath.sv` no longer answers STREAM_INPUT selectors 5 and 7 and leaves the selector 4 failure-code byte zero: the processor owns probing/ACMP status, failure code and failure bridge id. The bound/settled approximation and the zero bridge id are deleted |
| Evidence | `sim_nxn.cpp` `[GSI]`, in the timed `obj_notify` leg on the shipping AX 1x1 shape (AAF sink 0, CRF sink 1): DISABLED, ACTIVE with 0, 7 and 3, PASSIVE, COMPLETED; per-sink Talker Failed code and 64-bit bridge id; refresh, change, withdrawal, STOP_STREAMING exclusion, reset, missing descriptor; every push equals the solicited answer. 345/345 |
| Mutants | `make gsi-mutants`: bridge tied to zero, selector 5 back to the datapath, code tied to zero, code byte left to the datapath, status tied to zero, wrong sink, and the old approximation restored. All seven fail their named check |
| Boot (new pin) | the processor holds its ACMP listener until the NVM walk ends, and `PP_CTRL[1]` starts it. Every harness that binds a sink now starts the walk, as the firmware's `nvm_boot()` does. Without it the 1x1 leg failed 24 checks and the render multi leg 30 |
| Co-simulation | `nvm_cosim`'s transcription of the producer path now wires the manager arbiter, error cause, abort and walk deadline as the processor top does; it failed 3 power-cycle cases before |
| Docs | integration guide (GET_STREAM_INFO owners, per-boot walk), REGISTER_MAP (`PP_CTRL[1]`, `LWSRP_STATUS[9]`/`LWSRP_SLOPE` after processor #112), troubleshooting section 27, compliance matrix, TESTING, the suite README, wrapper comments, stale processor line citations |

## Authoritative references

- Milan v1.2 5.3.8.6, 5.3.8.8, 5.4.2.10, 5.4.5.2 Table 5.22, 5.5.3.5.3, 5.5.3.5.29.
- Processor `docs/architecture/06_aecp_engine.md` F06.13, `02_interfaces.md` F02.10, `05_acmp_engine.md` 5.1, `docs/guides/integrator.md`.
- `docs/reference/SUBMODULES.md`, `REQUIREMENTS.md` sections 1, 2 and 8.

## How to get into the same state

```sh
git fetch origin && git checkout 508-pp-pin-adopt
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git submodule status   # protocol-processor at a8f8ce810ddba1816cd129d0afcd71e6e02ade1b
```

## How to validate

```sh
make -C tb/verilator/milan_dp notify        # checks: 345 failures: 0
make -C tb/verilator/milan_dp gsi-mutants   # 8 checks: 8 PASS
make -C tb/verilator/milan_dp               # every leg PASS, render mutants 6/6
make -C tb/verilator/milan_dp_render        # 152/0, 60/0, leg defects 5/5
make -C tb/verilator/nvm_cosim              # 465/465, 39/39 mutants
make -C tb/verilator/pp_shadow              # 371/0
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/check_port_contracts.py     # FAILS until the processor follow-up lands
```

Local results at the head: builder with the pinned SDK and without an RV32 compiler both rc 0; Yosys 54/54 tops; behave 344 scenarios; docs gates in both modes, em-dash, style, contents, paths, module matrix, xvlog, source lists, C++ and Python idiom all rc 0.

## Known limitations / out of scope

- Acceptance 2 names PASSIVE after a bind. The processor probes at the bind, so a bind is ACTIVE and PASSIVE follows an unanswered probe's retry (processor PR #111). The leg grades that order.
- The firmware's `nvm_boot()` returns before starting the walk when its record shape is inconsistent. The builder refuses such a build, so this is reported, not changed.
- #551's cold-pipeline case is not flipped here; #553 does that.
- The scheduled `milan_dp_gptp` physical suite and the live SoC elaboration were not run locally.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (2-6)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (three processor-content gates, above)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
