# [A229] HANDOFF: kebag-logic/milan-fpga #530, parent lane

Branch `530-crf-talker-licence`, head `c593cbeffaffa647cda70fb1a233455bf9c80d55`
(tree `6459e8f0866f9a807d01d7dc325997c3a4e4e938`), five one-line commits on live
dev `50e78097564244c124e1ec30dd8821f83951ab06`. Nothing is pushed, no PR is
open, nothing is merged. The PR body is `PR-BODY.md` ("Relates to #530"; the
issue closes after the silicon rerun).

## For the manager

1. Push `530-crf-talker-licence` to `c593cbef`. The processor gitlink is
   `09f9bf38`, already on processor `main`, so nothing needs pushing there.
2. Open the PR against `dev` from `PR-BODY.md`, as a draft or ready as you
   decide, and run the act replica and the hosted gates.
3. Assign the internal cleared-context and external reviewers.
4. After merge: the #530 silicon rerun. What it should show if the fix holds:
   - no CRF PDU before the first Listener Ready;
   - a bound CRF output streaming continuously across the DUT's and the
     switch's LeaveAll cycles, with no DUT Talker Advertise Leave;
   - Stream Output 1 STREAM_START staying 1 while bound, and FRAMES_TX equal
     to the seconds it has streamed;
   - emission stopping when the Listener withdraws, not 15 s after the last
     probe.

## Commits

| commit | subject |
|---|---|
| `e8c273ff8f000f0cf9b12b797fa7577ac5bb65fb` | Pin the protocol processor at its merged per-type LeaveAll 09f9bf38, re-record its ROM digests and move the parent's line citations and MRP-5 row with it |
| `8eca7031d508a8807f71e89645c99ba29ed41c9c` | Gate every talker on the processor's ACTIVE instead of its raw admission verdict and grade #530's Run B shapes in a compressed-time obj_crflic leg |
| `ae51a17f0435e3933a581f34e7f3629f91fb29c5` | Cite the Stream Output counters where Milan v1.2 puts them, 5.3.7.7 Table 5.4, in the talker counter banner |
| `dd286c01340ae236e8a4d63e9a766f72c8d469d3` | Hold obj_crflic's per-source peer state in one struct, document its SIGTERM handler and record its mutation driver as a classified DUT reader |
| `c593cbeffaffa647cda70fb1a233455bf9c80d55` | Print the CRF licence and ACTIVE edges in obj_crflic's timeline, grade that a Listener Lv closes ACTIVE within 50 ms, and record both failing arms' measured timelines |

## The pin (item 1's parent half)

- `09f9bf38` is the merge of processor PR 107. Its tree `495bfb5d` equals the
  reviewed head `5f8cb132`: R271-3 POSITIVE at that exact head; R270-2
  POSITIVE at the ancestor `27763677`, and `git diff 27763677 5f8cb132 -- hdl/`
  is empty. The old pin `424c688f` is an ancestor.
- Parent consumers moved: gitlink, `docs/reference/SUBMODULES.md`, the
  regenerated boundary diagram (`.drawio`, `.svg`, `.png`, `PNG_MANIFEST.json`),
  `syn/yosys/rom_digests.tsv` (`ooc.sh --record-rom-digests`; both images hash
  as at `424c688f`), the `KL_srp_top.sv:193` -> `:207` and
  `KL_srp_listener_fsm.sv:783-784` -> `:795-796` citations
  (`milan_datapath.sv`, `pp_shadow/sim_main.cpp`), and traceability row MRP-5.
- The pin range also carries processor PRs 96 to 105 (the SRP Domain default
  VID parameter `SRP_DOM_DEF_VID_P`, default 2, and fixture guards). The
  parent keeps the default, so no instance change is needed.

## Items

- **Item 1**: `tb/verilator/milan_dp` `obj_crflic` `[C]`: 85/0 at the head.
  The same leg at `424c688f` fails 17 of 85 with the Run B burst ends
  (receipt `62`).
- **Item 2**: reproduced first with the gate line reverted (receipts `02`,
  `61`: 23 of 85 fail; licence open at 1770.38 ms, first CRF PDU 3.85 s
  before the first Listener Ready), then fixed in `milan_datapath.sv`.
  `make crflic-mutants` catches all three consumer plants (receipt `70`).
  The BDD scenario pins the gate's source text; its step fails on the
  reverted line (receipt `74`).
- **Item 3**: explained, not fixed. See the PR body and the
  `tb/verilator/milan_dp/README.md` section "FRAMES_TX is an interval count".
  The assignment names Milan v1.2 5.3.8.10 Table 5.6; that is the Stream Input
  set. The Stream Output FRAMES_TX is 5.3.7.7 Table 5.4, and the RTL banner
  that cited a nonexistent 5.3.7.10 is corrected.

## Gates (simulator 5.050 from the pinned tool bin, `-j 8`)

| gate | head | result | receipt |
|---|---|---|---|
| milan_dp main (`obj_dir`) | `dd286c01` | 230 / 0 | `50` |
| milan_dp notify | `dd286c01` | 146 / 0 | `51` |
| milan_dp nxn | `dd286c01` | 1708 / 0 | `52` |
| milan_dp nxn8 | `dd286c01` | 3136 / 0 | `53` |
| milan_dp crflic | `c593cbef` | 85 / 0 | `60`, `70` |
| milan_dp crflic-mutants | `c593cbef` | 4 / 4 PASS | `70` |
| milan_dp nxndv, nxn4c, nolpf, prune, ax1x1, aclk, gptp, gptp-lat | pre-commit tree of `8eca7031`, comment-only RTL difference | 1710, 1708, 230, 33, 227, 139, 181, 181, all 0 failures | `14`-`21` |
| milan_dp render_mutants | `c593cbef` | 6 / 6 PASS | `73` |
| count control: nxn, nxn8, notify on the base datapath | base `milan_datapath.sv`, new pin | 1708, 3136, 146 (unchanged by the fix) | `30`-`32` |
| pp_shadow | `dd286c01` | 371 / 0 | `55` |
| test_builder.py | `dd286c01` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, needs the physical build tree) | `42` |
| lint_rtl --check | `dd286c01` | PASS 90 <= 90 | `43` |
| quick gates: check_rtl_source_lists, xvlog_gate --check (PASS, 4 = ratchet, pinned `09f9bf38`), check_cpp_idiom, check_py_idiom, docs_check, check_em_dash --base 50e78097, doc style, TOC, anchors, doc paths, feature status, module matrix, DOC_MAP, hygiene, pp_srcs, naming, port contracts, fail-fast, test evidence, TODO ownership, sv/sh idiom, submodule docs and diagram, `git diff --check` | `c593cbef` | all rc 0 | `71` |
| behave (whole suite) | `c593cbef` | 317 scenarios passed | `72` |

`c593cbef` changed only the harness timeline and labels and the README relative
to `dd286c01`; `milan_datapath.sv` is byte-identical between them.

Not run: act/Docker, hosted CI, `syn/yosys/run.sh` and `ooc.sh` pricing,
builder gate 11, hardware.

## Open points for review

- The optimistic admission window corner (`milan_datapath.sv` SRP block
  comment): ACTIVE can precede the round that adds the slope to the sum only
  if a Listener Ready is registered within three admission rounds of a fresh
  declaration.
- The switch model follows Run B: its LeaveAll 9.99 s after each DUT
  LeaveAll. A fixed-period switch is not modelled. Processor issue 108 (no
  leavealltimer restart on a received LeaveAll) is unchanged.
- The mutants are an explicit target, `make crflic-mutants`, listed in
  `docs/testing/TESTING.md`, to keep the stated `milan_dp` deadline margin.
  The leg itself is in the default sweep. Its hosted time is unmeasured
  (local: about 14 s build, 20 s run).
- `LWSRP_STATUS[8]`, `CRFT_CTRL[6]` and the `0x82C` talker lobs change value
  (they now read ACTIVE). No address, width or access changes. VERSION
  unchanged; CHANGELOG entry Unreleased.
- Seen, not changed: `sw/litex/milan_soc.py:2123` cites
  `protocol_processor_top.sv:113` for `DESC_MEM_TMO_CYC_P`, which is line 120
  at both pins. It is not a consumer this pin moved; it may merit its own
  issue.

## Packet

`receipts/` (logs), `arms/` (the gate-reverted and base datapath copies),
`scripts/` (`quick_gates.sh`, `leg.py`, the recorded `make -n run` commands),
`MANIFEST.sha256`.

## Posted

`[A229] REVIEW READY`: https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5807302041
