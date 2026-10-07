[A559]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `351ae81f`: the ctrl gate (all arms; `acmp` 67, `acmpwalk` 127, `acmpnvm` 6 tests), the campaign (288 of 288 caught), coverage (100 % after exclusions), the store gate (434 tests), the mbx suite with the co-simulation and both defect campaigns, the contract generator, the builder bank (one arm not run: it needs a Vivado report on disk) and 69 docs-workflow commands, every one rc 0. `665-f3-acmp` -> `dev`.

Stacked on lane FC (#685, head `021b9c1f`), which is not in `dev` yet: until it merges, the
diff against `dev` also shows FC's commits. `dev` is merged here with `--no-ff` once FC lands,
and the gates run again.

## Linked Issue / roles

Relates to #665

Executor: `[A559]`
Internal cleared-context reviewer: `[R530]`
External reviewer: `[R531]`

## Description

Lane F3 of #665: Milan connection management (ACMP) on the bare-metal control core, as a
ports-and-adapters module beside F0's ADP slice. No RTL change; the default all-fabric build,
the shipping image and the register map are unchanged.

| Piece | What it is |
|---|---|
| `sw/firmware/ctrl/acmp/acmp.[ch]` | The core, with no mailbox and no heap. Every listener transition of Milan v1.2 Table 5.30 per sink (BIND_RX, UNBIND_RX, GET_RX_STATE, probing, TMR_NO_RESP 200 ms with one duplicate under the same sequence_id, TMR_RETRY, TMR_DELAY, TMR_NO_TK, the SRP events). The talker's answers of 5.5.4. The discovery machine of 5.6.4 / Table 5.54, with TMR_NO_ADP from the received valid_time. The lock, and responses keyed on the consumer's unique ID. State keyed per AVB interface. One timer port per interface, armed at its sinks' earliest deadline. Owed frames in order, and a sink change reported only after the response that caused it (#653). Every port guarded against re-entry (#678). |
| `sw/firmware/ctrl/acmp/acmp_mbx.[ch]` | The mailbox adapter: the acmp channel, one fabric timer slot per interface with the tag rule, and a tap in front of the adp channel's handler. The tap reaches F0's module through the loop's public binding: ENTITY_AVAILABLE and ENTITY_DEPARTING go to discovery, everything else to ADP unchanged. The service-latency bound of every path and backlog, in mailbox accesses. |
| `sw/firmware/ctrl/acmp/acmp_nvm.[ch]` | The binding owner on lane F1's state port. A saved binding fast-connects from PRB_W_AVAIL; a slot the store cannot read holds its writer and nothing is persisted (F1's rule). |
| `sw/firmware/ctrl/app/ctrl_app.[ch]` | The composition in two calls, compose then open, with ACMP composed after ADP when configured. |
| `sw/firmware/ctrl/test/` | Three arms: `acmp` (67 tests: the core over fakes, the adapter and the H-ACMP/H-DISC bounds on the host model), `acmpwalk` (127: the processor's own F05.3 model of Table 5.30 in lock step, its Table 5.54 transcription, its talker suite's F05.11 constants, cut from the pinned submodule) and `acmpnvm` (6: the real F1 store over the flash model). 195 planted defects in `acmp_mutants.py`; every test of the three arms is named by one, which the campaign proves before planting. |
| `tb/verilator/mbx/cosim_main.cpp` | The co-simulation now composes ACMP too. A BIND_RX goes through its probe, duplicate and retry; then the other commands, and two frames both filters refuse. 12 frames, identical on the RTL and the host model. |
| Docs | `docs/design/MAILBOX_SPLIT.md` "The ACMP module" (units, the adp filter term, service latency, differences from the processor, open items); `sw/firmware/ctrl/README.md`; `sw/firmware/gtest/README.md`; `sw/firmware/ctrl_nvm/README.md`; `tb/verilator/mbx/README.md`. |

Differences from the processor, asserted field for field in `acmpwalk` (the firmware follows
the clause; the submodule is not changed): the lock refusal status (processor 13,
TALKER_MISBEHAVING; IEEE 1722.1-2021 Table 8-3 gives 16, CONTROLLER_NOT_AUTHORIZED);
UNBIND_RX_RESPONSE's talker fields (Table 5.36: 0); the ACMP status after TMR_RETRY with the
talker discovered (5.5.3.5.30 step 2 sets none); DISCONNECT_TX of an unknown source (5.5.4.2
step 1: TALKER_UNKNOWN_ID).

## Authoritative references

- Milan v1.2 5.5 (5.5.2.2 to 5.5.2.7, 5.5.3.1 to 5.5.3.5.48, 5.5.4.1 to 5.5.4.4, Tables 5.22 to 5.48) and 5.6.4 (5.6.4.1 to 5.6.4.5.4, Table 5.54).
- IEEE 1722.1-2021 8.2.1 (Figure 8-1, Tables 8-1 to 8-4), 6.2.2.5 (valid_time units), 7.4.35.
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2 (NFR-SCOUT-02/03/08, H-ACMP, H-DISC); #664 3.4.2.
- `docs/design/MAILBOX_SPLIT.md` (the contract, A1 to A4, the ADP slice); `sw/mailbox/mailbox.yaml` (major 2).
- #653 (response before notification), #678 (no callback into a module from its ports), F1's saved-state store (`sw/firmware/ctrl_nvm/README.md`).

## How to get into the same state

```sh
git fetch origin
git checkout 665-f3-acmp
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install pyyaml
# GoogleTest and GoogleMock (libgtest-dev, libgmock-dev), a host C/C++ compiler,
# Verilator 5.050 on PATH, and for the RV32 arms an RV32 compiler for -mabi=ilp32
# (scripts/ci_rv32_sdk.py installs the CI pin).
```

## How to validate

```sh
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
for k in 1 2 3 4 5 6 7 8 9 10 11 12; do
  python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice "$k/12" || break
done
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
make -C tb/verilator/mbx clean && make -C tb/verilator/mbx && make -C tb/verilator/mbx mutants
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/gen_toc.py --check
```

Expected result / pass criteria: every command exits 0. The ctrl gate passes all arms
(`acmp` 67, `acmpwalk` 127, `acmpnvm` 6 tests). Each campaign slice prints
`mutants: 24 of 24 caught` with no `[ESCAPED]` line. The coverage check reports every file
100 % lines and branches after exclusions (`acmp.c` 690/690 lines, 316/316 branches raw).
The mbx suite passes 285 and 330 checks through the two adapters, and the co-simulation 28
checks over 12 identical frames. The RTL campaign prints `mbx mutants: 67 of 67 caught`.

## Known limitations / out of scope

- **Discovery receives nothing from the fabric yet.** The contract's adp channel passes only
  ENTITY_DISCOVER, and both of its accept terms are in use. Milan v1.2 5.6.4.1 needs every
  ENTITY_AVAILABLE and ENTITY_DEPARTING of a bound talker; adding that term changes the
  elaborated filter (RTL), which this lane may not touch. The decision (which term, and who
  adds it) is open on #665. Until then a restored binding waits in PRB_W_AVAIL. A bound sink
  whose probe fails or times out reaches PRB_W_AVAIL after TMR_RETRY and stays there. H-DISC
  is shown on the host model with records written into the adp ring in the contract's layout.
- **Time is not measured.** The bounds are in mailbox accesses (A4). Every path costs at most
  72 accesses. The full-backlog bounds fit T_svc = 10 ms only at 0.92 us per access or less
  behind a full acmp ring, and 0.46 us behind a full adp ring (H-DISC), which also exceeds the
  20 ms ceiling at 1 us. The measured backlogs stay far below the bounds. H-ACMP's wire round
  trip needs the datapath tap.
- No image links this firmware yet; the host tests and the co-simulation build it.
- The processor differences above are recorded, not fixed (the submodule is out of scope).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the H-DISC delivery through the fabric waits for the filter-term decision)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
