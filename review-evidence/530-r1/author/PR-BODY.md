[A229] Gate every talker on the processor's ACTIVE and adopt its per-type LeaveAll (#530 items 1 to 3)

## Contents

- **[Status](#status)** -- Green, the gate tally, and `530-crf-talker-licence` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- #530 stays open for the silicon rerun.
- **[Description](#description)** -- The pin, the licence repoint, the new leg, and item 3.
- **[Authoritative references](#authoritative-references)** -- The Milan and 802.1Q clauses and the decisions.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and submodules.
- **[How to validate](#how-to-validate)** -- The commands and their expected tallies.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What simulation cannot show.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

GREEN at `c593cbeffaffa647cda70fb1a233455bf9c80d55` (tree `6459e8f0866f9a807d01d7dc325997c3a4e4e938`): five commits on live dev `50e78097564244c124e1ec30dd8821f83951ab06`. `530-crf-talker-licence` -> `dev`.

## Linked Issue / roles

Relates to #530. The issue closes after the manager's silicon rerun, so this PR does not close it.

Executor: `[A229]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

| commit | change |
|---|---|
| `e8c273ff` | Pins the protocol processor at `09f9bf38`, the merge of processor PR 107. Its tree `495bfb5d` equals the reviewed head `5f8cb132` (R271-3 POSITIVE at that head, R270-2 POSITIVE at its ancestor `27763677` with no `hdl/` change after it). Moves every parent consumer of the pin: `SUBMODULES.md`, the boundary diagram and its PNG manifest, `rom_digests.tsv` (new pin rows; both images hash as before), two line citations of `KL_srp_top.sv` / `KL_srp_listener_fsm.sv` that the new banner moved, and the traceability row MRP-5, which stated per-application receive semantics. |
| `8eca7031` | **Item 2.** `lwsrp_stream_gate` now takes `pp_cd_srp_active_w`, the processor's ACTIVE, instead of `pp_cd_srp_sr_admitted_w`. The CRF licence (`crft_emit_en_w`), the AAF source 0 gate and every AAF talker gate read it. `CRFT_CTRL[6]`/`[7]`, `LWSRP_STATUS[8]` and the `0x82C` talker lobs follow. The CBS slope enable keeps the raw verdict. Adds the `obj_crflic` leg that proves items 1 to 3, its explicit `crflic-mutants` campaign, a BDD scenario pinning the gate's source text, and the doc rows. |
| `ae51a17f` | **Item 3.** The talker counter banner cited Milan v1.2 5.3.7.10, which does not exist; Table 5.4 is 5.3.7.7. |
| `dd286c01` | Idiom and test-evidence gate fixes for the new harness and driver. |
| `c593cbef` | The leg prints the CRF licence and ACTIVE edges in its timeline and grades that a Listener Lv closes ACTIVE within 50 ms. |

**Item 1: a bound CRF talker keeps its Talker Advertise.** `obj_crflic` elaborates `endstation_ax7101_1x1_tdm8` with the processor and `KL_maap` millisecond on one 100-cycle grid. It plays the Run B listener and switch port. The switch scopes a received LeaveAll per attribute type, re-declares only the flagged types, and sends its own LeaveAll 9.99 s after each DUT LeaveAll in the capture's byte layout. Phase `[C]` holds the CRF output bound for 76 s across five DUT and five switch LeaveAll MRPDUs, 61 s of it held by the Listener registration alone. There is no Talker Advertise Leave, no licence or ACTIVE drop, and no CRF gap over 1.5 periods. Every DUT LeaveAll flags all four MSRP types. **At the previous pin `424c688f`** the same leg fails 17 of 85: each DUT LeaveAll flags only the Domain. ACTIVE and the licence fall six times, each 5.0 s after a LeaveAll that aged the registration with no re-declaration. The DUT withdraws its Talker Advertise four times: once 5.0 s after a switch LeaveAll, three times 15.1 s after the latest probe. Those are Run B's burst ends.

**Item 2: nothing is emitted before a reservation exists.** The leg was first run against the datapath with only the gate line reverted: 23 of 85 fail with the Run B signature. The licence opens at 1770.38 ms, 1.34 ms after the first probe and before its TALKER_DEST_MAC_FAIL answer (1772.00 ms). The first CRF PDU leaves 3.85 s before the first Listener Ready, and the licence never closes again, through Asking Failed and the unbind. At the head: in `[A]` the DUT declares Talker Advertise and is admitted for 3.9 s with no Listener Ready, and no CRF or AAF PDU leaves. `[B]` opens each gate on the cycle ACTIVE rises. `[B2]`, `[D]` and `[E]` close it on the cycle ACTIVE falls: an AAF unbind, an Asking Failed registration, a CRF unbind inside a fresh probe window. On every cycle the CRF licence equals ACTIVE[CRF], and the AAF gate is never open without ACTIVE[AAF]. `make crflic-mutants` plants each consumer back on the raw verdict (whole gate, CRF slot, AAF source 0) and catches all three.

**Item 3: FRAMES_TX 16 is the documented semantics; explained, not fixed.** Milan v1.2 5.3.7.7 Table 5.4 FRAMES_TX is "Incremented at the end of every observation interval during which at least one Stream Data AVTPDU has been transmitted", with an interval of at most 1 s, "Reset to 0 each time the Talker starts streaming". The fabric's interval is 1 s. Run B's last burst lasted 15.00 s, so it touched 16 intervals. The PDU total is `CRFT_COUNT` (`0x764`), whose register row now says so. Table 5.6 (5.3.8.10) is the Stream Input set and does not define FRAMES_TX. Phase `[F]` grades both sides: FRAMES_TX equals the intervals since STREAM_START, far below the PDU count, and restarts at the next STREAM_START.

VERSION is unchanged (`0x0002_0060`); the CHANGELOG entry is Unreleased and the release step owns the bump. No descriptor, AEM image or CSR address changes.

## Authoritative references

- Milan v1.2 5.3.7.3 (streaming state), 5.3.7.7 Table 5.4 (Stream Output counters), 4.3.3.1 (Talker DA validity)
- IEEE 802.1Q-2014 10.7.5.20 NOTE and b) 2), 10.8.2.6, 10.8.2.8 f
- #530: the DECISION https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5797078565, the manager decisions 5797128389 and 5798177316, the assignment 5806344022
- Processor issue 106 and PR 107 (merge `09f9bf38`)
- The #117 findings page, Run B (branch `117-silicon-evidence`, `docs/findings/117_GPTP_SILICON_EVIDENCE.md`)
- `docs/reference/REGISTER_MAP.md` rows `0x750`, `0x764`, `0x694`, `0x82C`; `docs/traceability/ieee8021q.md` MRP-4 and MRP-5

## How to get into the same state

```sh
git fetch origin 530-crf-talker-licence
git checkout c593cbeffaffa647cda70fb1a233455bf9c80d55
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git submodule status protocol-processor   # 09f9bf3846511f8388d995126502ed92eaa65213
```

## How to validate

```sh
make -C tb/verilator/milan_dp crflic            # checks: 85   failures: 0
make -C tb/verilator/milan_dp crflic-mutants    # 4 checks: 4 PASS, 0 FAIL
make -C tb/verilator/milan_dp                   # every leg, render_mutants included
make -C tb/verilator/pp_shadow                  # pp_shadow: 371 checks, 0 failures
(cd tests && behave --no-capture -f plain)      # 317 scenarios passed
# the item 1 failing arm, by hand; restore the pin afterwards
git -C protocol-processor checkout 424c688fa2205b934a7689a58f2aa766420f2326
make -C tb/verilator/milan_dp crflic CRFLIC_MDIR=obj_crflic_oldpin   # 17 of 85 fail
git -C protocol-processor checkout 09f9bf3846511f8388d995126502ed92eaa65213
```

Expected result: every command above passes except the by-hand arm, which fails as stated.

## Known limitations / out of scope

- The switch model is the Run B one: its LeaveAll 9.99 s after each DUT LeaveAll. A switch with a fixed LeaveAll period is not modelled.
- This station's leavealltimer still does not restart on a received LeaveAll (Table 10-5): processor issue 108, not changed here.
- ACTIVE takes the processor's optimistic admission window (three admission rounds after a fresh declaration). It can open the gate before the round that adds the slope to the shaper's sum only if a Listener Ready is registered within those rounds. The `milan_datapath` comment records this corner.
- `AAF_CTRL[1]` still bypasses the licence (audit B9, unchanged).
- The new leg's hosted time is unmeasured. Locally it builds in about 14 s and runs in about 20 s; the mutants take 169 s and are an explicit target, outside the sweep's deadline.
- Not run by the executor: act/Docker, hosted CI, `syn/yosys` (portability and OOC pricing), builder gate 11 (needs the physical build tree), hardware.
- Seen, not changed: `sw/litex/milan_soc.py:2123` cites `protocol_processor_top.sv:113` for `DESC_MEM_TMO_CYC_P`, which sits at line 120 at both the old and the new pin.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (simulation parts here; the silicon rerun is the manager's)
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
