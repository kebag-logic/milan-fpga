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

BLOCKED at `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` (round 3, area): every gate below exits 0,
but the bound-talker term costs 357 LUT against a target of 300 (86 FF against 120), so round 3
ends in a STOP on #665 (comment 6033939473) for a decision (see [Known limitations](#known-limitations--out-of-scope)).
The mbx suite passes 380 and 425 checks through the two adapters, the same at two interfaces,
369 on the model and 32 in the co-simulation; its RTL campaign catches 141 of 141; the ctrl gate,
its model-arm defects (27 of 27), coverage, the contract generator, lint, the Vivado and Yosys
front-ends and 74 docs-workflow commands pass. `665-f3-acmp` -> `dev`.

FC round 2 (`db9aa8c9`) and dev (`910f338d`, #679) are merged here with `--no-ff`; FC (#685) is
not in `dev` yet, so until it merges the diff against `dev` also shows FC's commits.

## Linked Issue / roles

Relates to #665

Executor: `[A559]`
Internal cleared-context reviewer: `[R530]`
External reviewer: `[R531]`

## Description

Lane F3 of #665: Milan connection management (ACMP) on the bare-metal control core. Round 2
answers both round-1 reviews (R531-1 and R530-1, every finding accepted) and adds the `adp`
channel's bound-talker term decided on #665 (comment 6029368753). Round 3 makes that term cheap
(the area ruling, comment 6032450078).

**Round 3 (area).** The behaviour is unchanged; the RTL changes only inside the mailbox block.

| Item | What changed |
|---|---|
| The table in distributed RAM | `KL_mbx_rx` holds the bound-talker tables: the host's `BOUND_EID` words in a read-back memory (32 x 32, six RAM32M), and each entry's eight identity bytes in a shift register of its own (SRL16E), byte b at tap b. The 1,040 flip-flops of round 2 are gone. |
| Byte-serial compare | As wire bytes 18 to 25 arrive, identity byte b is compared with byte b of every entry of the arrival interface's table: one 8-bit compare per entry per byte and one match flag per entry, armed by the first byte. The decision point is where it was. |
| The copier | Setting `BOUND_EN`, or writing a `BOUND_EID` word while it is set, owes the entry a copy; the copier shifts its eight bytes in from the read-back memory, one byte in each cycle the host leaves that memory, and starts over on a rewrite. An entry takes part only while `BOUND_EN` is set and no copy is owed, from its first identity byte to the verdict, so a frame whose identity passes a rewrite never matches it. Derived from the RTL: at most 176 clocks for all sixteen entries of an interface, plus a clock per host access to the tables. |
| Reset | Distributed RAM keeps its contents through a reset, so a flag per word makes a `BOUND_EID` word not written since the reset read 0 and copy as 0: the contract's reset value holds. |
| Skeleton | The generator decodes a bound-talker register's interface, entry and register by bit fields (refusing strides that are not powers of two) and passes them to `KL_mbx_rx`; the skeleton reads `BOUND_EID` back only while it is valid. The generator also refuses `eq_bound` terms on two fields. `KL_mbx_pkg.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md` and the YAML are unchanged. |
| Tests | Q14 to Q17 in the shared suite (frames in a row, each identity byte, a rewrite with `BOUND_EN` set, a reset), on both adapters, at two interfaces and on the model; Q18 to Q21 on the RTL only (a frame stalled inside its identity, reads beside a copy, a rewrite at each of 32 clocks). The 12 round-2 RTL defects are planted on the lines that now carry them, with 18 new ones, among them the two the ruling asked for: a wrong byte index and a stale match flag across frames (two forms). |

Out-of-context area, the round-2 recipe (`KL_mbx` behind `KL_mbx_wb`, `xc7a100tfgg484-2`, 10 ns,
placed and routed, under the shared lock): 3,102 LUT and 2,946 FF against FC round 2's 2,745 and
2,860, WNS +0.402 ns, all 6,041 nets routed. The term costs 357 LUT and 86 FF: 64 LUT of shift
registers, 22 of read-back memory and 271 of logic. Two measured variants show what the rest
buys, each a contract change: `BOUND_EID` not cleared by a reset, +337 LUT and +56 FF; that and
`BOUND_EID` write-only, +300 and +56.

**Round 2.**

| Item | What changed |
|---|---|
| The `adp` term | Contract 2.1 (`sw/mailbox/mailbox.yaml`, through the generator only): the adp channel's third accept term `eq_bound` (message types 0 and 1, entity_id at byte 18) admits ENTITY_AVAILABLE and ENTITY_DEPARTING of a talker bound on the receiving interface. It reads a per-interface bound-talker table in the mailbox block (16 entries, one per listener stream: `BOUND_EID_LO`, `BOUND_EID_HI`, `BOUND_EN`). `KL_mbx_rx` compares the captured entity_id with the enabled entries of the arrival interface's table; `KL_mbx` and `KL_mbx_pkg` are regenerated; the host model does the same. The core's new `admit` port keeps the table equal to each bound sink's talker; `acmp_open`, called from `ctrl_app_open`, writes the bindings the store restored at boot. The contract's minor moves: a firmware built against 2.0 leaves the table empty. |
| R531-1-F1 (MAJOR) | Only AVTP version 0 is read: an ACMPDU or ADPDU of another version is discarded before it is decoded, in both receive paths (IEEE 1722-2016 4.4.3.4; IEEE 1722.1-2021 8.2.1.3, 6.2.2.3). |
| R531-1-F2 (MAJOR) | TMR_NO_RESP runs 200 ms from the send the transmit ring accepts, for the probe and its duplicate: an owed probe holds its timer until it leaves, matched by sink and sequence_id, so command order, the single duplicate and its sequence_id are kept (Milan v1.2 5.5.3.5.3 steps 5 to 7, 5.5.3.5.16 steps 1 and 2). |
| R531-1-F3 | The adapter's slot range is compared (`first_slot > MBX_N_TIMERS - MBX_N_IF`), never summed or narrowed. |
| R531-1-F4, F5 | The reviewer's corrections: the owed-frame bound fits T_svc at 1 us; `acmp_poll` sends at most one owed frame. |
| R530-1-F1 | A new arm, `acmpif2`, builds the adapter's tests with the firmware and the model on the contract's two-interface variant; B3, B4, B6, B8 and the C paths run per interface. |
| R530-1-F2, F3, F4 | Tests pinning the BINDING record byte for byte to the processor's payload one flag at a time and refusing other lengths; a D3 roll-back keeping the bindings (at the port and at a real boot); every connection timer, TMR_NO_ADP and the earliest-deadline choice across the 32-bit millisecond wrap. Each with planted defects. |
| R530-1-F5, R1 | TD1 recorded with the 5.5.2.7/5.5.4.2 tension and the ruling; "field for field" limited to LD1 to LD3; the decided term in place of "open decision". |
| Harness | `tb/verilator/mbx` `run-cosim` rebuilds the firmware library on any header change and relinks `Vmbx_cosim` whenever the library is newer. |

Evidence for the term: the suite's Q12 and Q13 on both adapters, at two interfaces and on the
model; 24 planted RTL defects (12 rules, both adapters); H-DISC measured from the adp channel's
`RX_HEAD`, the record committed by the model's filter (C10 35 accesses, C11 29; behind a full adp
ring filled through the filter, pass 13 of 26 records, 333 accesses against 21,912); and the
co-simulation, where the bound talker's ENTITY_AVAILABLE crosses the RTL's filter into discovery
on both fabrics frame for frame. Out-of-context area: 4,025 LUT and 3,907 FF against FC round 2's 2,745 and 2,860 (`KL_mbx` behind `KL_mbx_wb`, `xc7a100tfgg484-2`, 10 ns, placed and routed, WNS +0.283 ns); the term costs 1,280 LUT and 1,047 FF, 1,040 of them the table's flip-flops. Building the entity_id comparators only for the `eq_bound` term (a constant of the term) saved 862 LUT over the first version.

Planted defects: 348 in the ctrl campaign (F3's 251: `acmp_mutants.py`, round 2's 56 in
`acmp_review_mutants.py`), 105 in the RTL campaign. The reviewers' probes replayed at the head:
R530-1's six escaped probes are caught (X3 on the two-interface arm); R531-1's nine independent
probes pass at one and two interfaces.

**Round 1** (unchanged in kind): the core (`acmp.[ch]`: every Table 5.30 transition, the
talker's answers of 5.5.4, the discovery machine of Table 5.54, the lock, responses keyed on the
consumer's unique ID, one timer per interface, owed frames and #653, the #678 guard), the
mailbox adapter (`acmp_mbx.[ch]`), the binding owner on F1's store (`acmp_nvm.[ch]`), the
compose/open split, the processor's ACMP expectations walked in `acmpwalk`, and the docs.

Differences from the processor (processor issue #168): LD1 UNBIND_RX_RESPONSE's talker fields
(Table 5.36: 0), LD2 the ACMP status after TMR_RETRY with the talker discovered (5.5.3.5.30 step
2 sets none) and LD3 the lock refusal status (IEEE 1722.1-2021 Table 8-3: 16) are asserted field
for field against the processor's own model. TD1, DISCONNECT_TX of an unknown source, is
asserted on the firmware's half only (TALKER_UNKNOWN_ID, 5.5.4.2 step 1); the processor's SUCCESS
is read from source (`KL_acmp_talker.sv:1301-1306`). Milan v1.2 5.5.2.7 says DISCONNECT_TX
"always returns SUCCESS"; 5.5.4.2 governs, because 5.5.2.7 is an overview that defers to 5.5.4
and 5.5.4.2 is the "shall" procedure.

## Authoritative references

- Milan v1.2 5.5 (5.5.2.2 to 5.5.2.7, 5.5.3.1 to 5.5.3.5.48, 5.5.4.1 to 5.5.4.4, Tables 5.22 to 5.48) and 5.6.4 (5.6.4.1 to 5.6.4.5.4, Table 5.54).
- IEEE 1722.1-2021 8.2.1 (Figure 8-1, Tables 8-1 to 8-4), 8.2.1.3 and 6.2.2.3 (version), 6.2.2.5 (valid_time units), 7.4.35; IEEE 1722-2016 4.4.3.4.
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2 (NFR-SCOUT-02/03/08, H-ACMP, H-DISC); REQUIREMENTS.md section 1 (the `adp` row).
- #665 comments 6029368753 (the term), 6030067436 (round 2 and the TD1 ruling) and 6032450078 (round 3, the area ruling); the R531-1 and R530-1 reports.
- `docs/design/MAILBOX_SPLIT.md`; `sw/mailbox/mailbox.yaml` (2.1); `docs/reference/MAILBOX_CONTRACT.md`.
- #653, #678; F1's saved-state store (`sw/firmware/ctrl_nvm/README.md`, `nvm_state.h`).

## How to get into the same state

```sh
git fetch origin
git checkout 665-f3-acmp
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install pyyaml
# GoogleTest and GoogleMock (libgtest-dev, libgmock-dev), a host C/C++ compiler,
# Verilator 5.050 on PATH, and for the RV32 arms the CI's RV32 SDK
# (python3 scripts/ci_rv32_sdk.py, or MILAN_RV32_CC).
```

## How to validate

```sh
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
for k in $(seq 1 16); do
  python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice "$k/16" || break
done
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
make -C tb/verilator/mbx clean && make -C tb/verilator/mbx && make -C tb/verilator/mbx mutants
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 scripts/lint_rtl.py --check --self-test
python3 scripts/xvlog_gate.py --check          # with Vivado's xvlog on PATH
syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_sv_idiom.py
python3 scripts/gen_toc.py --check
```

Expected result / pass criteria: every command exits 0. The ctrl gate passes all arms (`acmp`
78, `acmpwalk` 127, `acmpnvm` 7, `acmpif2` 19 tests). Each campaign slice prints `mutants: 22 of
22 caught` (the last `18 of 18`) with no `[ESCAPED]` line. Coverage reports every file 100 %
after exclusions (`acmp.c` 729/729 lines and 342/342 branches raw). The mbx suite passes 380 and
425 checks through the two adapters (Q18 to Q21 included), the same at two interfaces and 369 on
the model, and the co-simulation 32 checks over 14 identical frames. The RTL campaign prints
`mbx mutants: 141 of 141 caught`.

## Known limitations / out of scope

- **Time is not measured (A4).** The bounds are mailbox accesses. Every path costs at most 76.
  The full-backlog bounds fit T_svc = 10 ms only at 0.91 us per access or less behind a full
  acmp ring, and 0.46 us behind a full adp ring (H-DISC), which also exceeds the 20 ms ceiling at
  1 us. Measuring the access time is an acceptance item of the F2 to F5 bench pass. H-ACMP's wire
  round trip needs the datapath tap.
- **The table's area is over its target.** In distributed RAM, compared byte by byte, the term
  costs 357 LUT and 86 FF against 300 and 120 (round 2: 1,280 and 1,047). The rest is per-entry
  logic the contract needs: the compare and its flag, `BOUND_EN`, the owed copy and the
  reset-to-0 of `BOUND_EID`, and its read-back. Measured without the reset clearing `BOUND_EID`,
  +337 LUT; also write-only, +300. Those are contract changes, the owner's to take or refuse
  (the STOP on #665).
- **Copy latency.** A binding takes part once the fabric has copied it, at most 176 clocks
  (1.76 us at 100 MHz) for all sixteen entries of an interface, derived from the RTL; announcements
  are seconds apart.
- No image links this firmware yet; the host tests and the co-simulation build it. The mailbox
  stays behind the default-off `--ctrl-mailbox` switch: the default all-fabric build and the
  shipping image are unchanged.
- The processor differences are processor issue #168; the submodule is not changed.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (lane F3's; #665 is a multi-lane issue)
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
