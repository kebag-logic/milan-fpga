[A582]

## Contents

- **[Status](#status)** -- Green locally, test tally, and `665-int-split` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- The publication block, its writers, the measurements and the fixes found while validating.
- **[Authoritative references](#authoritative-references)** -- Rulings, clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, dependencies and environment.
- **[How to validate](#how-to-validate)** -- Exact commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GREEN locally: every gate run exits 0 at the head. `665-int-split` -> `dev`.
This is PR 1 of 2 for F-INT, as ruled on #665 (comment 6088423771).
Base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`; head
`25bbe4d956e79de979783d7e4706a5581c0742a7` (11 commits, 47 files).

- Mailbox bench: 401 checks through Wishbone, 446 through AXI4-Lite, 32 in the
  co-simulation, and 403 / 448 / 388 at two interfaces (RTL through both
  adapters, host model), 0 failures. 167 of 167 RTL plants caught.
- Firmware: 51 arms; 492 of 492 `ctrl_mutants.py` and 186 of 186
  `srp_mutants.py` plants caught. Coverage ratchet holds at 22 files, with every
  writer file at 100 % of lines and branches.
- The all-fabric export is unchanged against `dev`; the mailbox block adds
  446 LUT and 1,136 FF out of context. Firmware grows by 1,008 B (1x1) and
  1,184 B (8x8), at 35.5 % and 54.0 % of 224 KB.

Independent review has not started.

## Linked Issue / roles

Relates to #665

Executor: `[A582]`
Internal cleared-context reviewer: `[R582]`
External reviewer: `[R583]`

Assignment: #665 comment 6087047553. Ruling for this PR: 6088423771 (decision
2 (a) and "PR 1"). Context: rulings 6087214078, 6087462816 and 6087654804;
round-1 STOP 6088406545.

## Description

In the split placement the firmware owns ADP, ACMP, MAAP and SRP, so the
fabric datapath can no longer read the protocol processor's class-D outputs.
This PR adds the values the datapath consumes to the mailbox window as a
publication block (contract 2.2, additive). It also adds the firmware writers,
each placed before the response that promises its value. The datapath's
build-time selection of the block is PR 2, after F5.

**The block** (`sw/mailbox/mailbox.yaml`, generated into `KL_mbx`, the
package, the C header and the contract reference). Interface i's block starts
at `0x800 + 0x200 * i`:

| Register | Fields | Stands for (processor output) |
|---|---|---|
| `DA_GATE` | `OPEN`, bit s per talker source | `acmp_declaring_o` |
| `LICENCE` | `ACTIVE`, bit s per talker source | `srp_active_o` AND `srp_sr_admitted_o` |
| `IDLE_SLOPE` | `BPS` | `srp_sum_slope_bps_o` |
| `SR_DOMAIN` | `VID`, `PRIORITY`, `ADOPTED` | `class_a_vid_o`, `class_a_prio_o`, `srp_domain_adopted_o` |
| sink k at `+0x100 + 0x10 * k`: `SID_LO`, `SID_HI`, `BINDING` | the stream_id; `BOUND`, `SID_VALID` | `acmp_bound_sid_o`, `acmp_bound_o` |

Every register resets to 0. Holes, an entry's fourth word and absent
interfaces read 0 and take no write, and a partial strobe is refused and
counted in `BUS_ERR`. Each field leaves on its own `pub_*_o` port. The
stream_id is published with `SID_VALID`. The driver writes `BINDING` with it
clear, then both halves, then sets it. The consumer takes `pub_sid_o` only
while `pub_sid_valid_o` is set, so a half-written stream_id never reaches it.

**The writers**, each before the response that promises the value:

| Owner | Writes | Before |
|---|---|---|
| ACMP core, publish port, through its adapter | `BINDING` and the settled stream_id of each sink whose pair moved | any frame of the entry (the BIND_RX and UNBIND_RX responses), and the store and notifier |
| MAAP adapter | `DA_GATE` | the allocation is reported (a PROBE_TX_RESPONSE then promises the address) |
| SRP adapter | `LICENCE` | each licence report, and the revocations of a reset or of destroy |
| SRP adapter | `IDLE_SLOPE`, `SR_DOMAIN` | the declarations they admit or carry |

ADP owns no value the split datapath consumes, so it gets no writer
(`docs/design/MAILBOX_SPLIT.md`, The publication block). Every write is counted
in its path's access bound, measured on the host model.

**Tests.** The mailbox suite checks the block through both adapters, at two
interfaces and on the host model: reset values, field masks, per-interface
and per-sink isolation, each output, the stream_id gating, holes, absent
interfaces and partial strobes. It has ten RTL plants. For every writer the
host tests have the three plants the ruling names: the publish moved after the
response, a wrong field, and the publish skipped. Each is caught by a named
test.

**Fixed while validating** (three commits on the implementation):

- The generated `KL_mbx.sv` read the publication storage before declaring it,
  which Vivado's front end rejects. The generator now emits the block before
  the read-back.
- The new port `pub_idle_slope_o` hid its unit and is now
  `pub_idle_slope_bps_o`, as the naming ratchet requires.
- An existing SRP plant, `cancelled-link-never-recovers`, escaped on the
  branch and is caught on `dev`. Its test relies on a LINK record staying held
  while the level drops and returns. The reset's new publication writes made
  the host model post it. The model gains `mbx_model_evt_pause`, which holds
  the event poster as a full RTL ring does. The test holds it and asserts that
  the record stayed held, and a new plant proves that assertion fails when the
  hold is ignored.

**Measurements** (the ruling's three):

- *All-fabric image.* Both AX7101 shipping configs were exported at `dev` and
  at the branch from one tree path. Of 3,876 files each, 3,856 are
  byte-identical, 5 differ only in date lines, and 13 archives have identical
  members. For 1x1, the generated Verilog matches in all 30,946 lines outside
  date lines and LiteX's comment-only hierarchy tree; two sibling lines in
  that tree swapped places. Every checkout and submodule file the TCL reads is
  unchanged. No bitstream was built.
- *Firmware size* (`ctrl_srp_image.py`, AECP not yet linked): 1x1 at one
  interface 80,368 -> 81,376 B; 8x8 at two 122,672 -> 123,856 B; the limit is
  229,376 B.
- *Mailbox area.* The M0s recipe's all-fabric selection measures zero, since
  that image has no mailbox. Its split selections need PR 2's route. The
  block's own out-of-context figure is +446 LUT, +1,136 FF, block RAM
  unchanged, WNS +0.329 ns at 10 ns. It is recorded in
  `docs/design/MAILBOX_SPLIT.md`; no resource record is re-recorded.

**Choices made public** for PR 2's comparison: the published stream_id is the
stream the sink listens to, from settlement until SRP stops, whereas the
processor holds the last settled one until the unbind. `LICENCE` is the
firmware's licence, which already requires admission. `SR_DOMAIN.ADOPTED`
follows the processor's F10.2 rule.

VERSION is unchanged. Outside the mailbox contract, its outputs, its bench,
the firmware and its tests, and the docs, only the `--ctrl-mailbox` instance in
`sw/litex/milan_soc.py` changes: it names the nine ports as unread signals.

## Authoritative references

- #665 ruling 6088423771 (decision 2 (a), PR 1 scope), assignment 6087047553.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1 (a value is written before the
  response that promises it) and section 7.
- `docs/design/MAILBOX_SPLIT.md`, The publication block, Verification and
  Measured area; `docs/reference/MAILBOX_CONTRACT.md` (generated).
- Milan v1.2 5.5.4.1 (the talker destination address a PROBE_TX_RESPONSE
  carries) and 5.5.3.5 (ACMP listener settlement and GET_RX_STATE).
- IEEE 802.1Q-2018 clause 35 (MSRP Domain and talker declarations).
- `docs/design/MARK_II_AREA_PLAN.md` (the 224 KB firmware limit, M0s);
  #640 M0s STOP 6087021702; PR #702.
- `CONTRIBUTING.md` section 3 (verification bar).

## How to get into the same state

```sh
git fetch origin
git checkout 665-int-split
git rev-parse HEAD
git submodule update --init third_party/verilog-axis third_party/lwSRP protocol-processor gptp-processor
git submodule status
```

Expected: HEAD is `25bbe4d956e79de979783d7e4706a5581c0742a7`, and no
submodule line starts with `-`, `+` or `U`. The firmware gates need the
pinned RV32 SDK (`scripts/ci_rv32_sdk.py`), GoogleTest and GoogleMock; the
Verilator gates need Verilator 5.050; the front-end gate needs Vivado 2026.1.

## How to validate

```sh
python3 sw/mailbox/gen_mailbox.py --check
python3 sw/mailbox/gen_mailbox.py --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
make -C tb/verilator/mbx
python3 -B tb/verilator/mbx/mutants.py
python3 scripts/lint_rtl.py --check --self-test
python3 scripts/xvlog_gate.py --check
python3 scripts/measure_naming.py --check
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 2
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2
syn/yosys/run.sh
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
git diff --check "$(git merge-base origin/dev HEAD)" HEAD
```

Expected result / pass criteria: every command exits 0. The mailbox `make`
prints 401, 446, 32, 403, 448 and 388 checks with 0 failures and 6 of 6 quick
plants; `mutants.py` prints 167 of 167. The firmware gate prints
`492 of 492 caught` and `test_ctrl_firmware: PASS`, and the coverage gate
`firmware coverage: PASS (22 files)`. Yosys passes 58 of 58 tops, and the
front-end gate reports 0 findings.

## Known limitations / out of scope

- No build switch and no datapath consumer: the `pub_*_o` ports are unread in
  the `--ctrl-mailbox` SoC and absent from the default build. The selection,
  the two-placement simulation and both images are PR 2, after F5.
- No ADP writer (above).
- The M0s split selections were not run: their route does not exist before
  PR 2, and PR #702 is open. The area figure is the block's own
  out-of-context measurement.
- The size fixture does not link AECP; F5 owns that figure against 224 KB.
- The all-fabric proof is at the export level: Vivado's inputs are identical
  apart from comments, and no bitstream was built.
- Not run: the full 64-suite `scripts/run_all_suites.sh` sweep. Of its suites,
  only `mbx` reads the changed RTL or firmware, and it ran in full;
  `fw_service_budget`, which imports `milan_soc.py`, passes on its own, as do
  the five LiteX simulations. `scripts/act_ci.py --pr` waits for a PR number.
- Independent review has not run.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
