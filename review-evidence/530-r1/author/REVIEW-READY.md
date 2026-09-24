[A229] REVIEW READY
Commit: `c593cbeffaffa647cda70fb1a233455bf9c80d55` on branch `530-crf-talker-licence` (tree `6459e8f0`), five one-line commits on live dev `50e78097`. Nothing is pushed and no PR is open. The PR body ("Relates to #530"), the handoff and the receipts are in the review packet.

Changed:
- **Pin.** The protocol processor moves from `424c688f` to `09f9bf38`, the merge of processor PR 107. Its tree `495bfb5d` equals the reviewed head `5f8cb132`. Every parent consumer of the pin moved: `SUBMODULES.md`, the boundary diagram and its PNG manifest, `rom_digests.tsv` (new pin rows, both images unchanged), two `KL_srp_*` line citations the new banner shifted, and traceability row MRP-5.
- **Item 2.** `milan_datapath.sv` now drives `lwsrp_stream_gate` from `pp_cd_srp_active_w`, the processor's ACTIVE, instead of `pp_cd_srp_sr_admitted_w`. The CRF licence and every AAF talker gate read it; the CBS slope enable keeps the raw verdict. `CRFT_CTRL[6]`/`[7]`, `LWSRP_STATUS[8]` and the `0x82C` talker lobs follow, and their register rows say so.
- **New `milan_dp` leg `obj_crflic`** (`sim_crf_licence.cpp`) on the AX7101 1x1 TDM8 shape. The processor millisecond and MAAP's share one 100-cycle grid. The leg plays the Run B listener and a switch port that scopes a received LeaveAll per attribute type and sends its own LeaveAll, in the capture's layout, 9.99 s after each DUT LeaveAll. Its mutation campaign is the explicit target `make crflic-mutants`. A BDD scenario pins the gate's source text.
- **Item 3.** Explained below. The talker counter banner's clause citation is corrected to 5.3.7.7, and the `CRFT_COUNT` row now says it is the PDU total.

Validation (simulator 5.050, 8 jobs):
- `make -C tb/verilator/milan_dp crflic`: 85 checks, 0 failures.
- `make -C tb/verilator/milan_dp crflic-mutants`: 4 of 4. Each of the three gate plants is caught on its named check, and the clean leg passes.
- `milan_dp` legs:
  - main 230/0, notify 146/0, nxn 1708/0, nxn8 3136/0. The counts are identical on the base datapath.
  - nxndv 1710/0, nxn4c 1708/0, nolpf 230/0, prune 33/0, ax1x1 227/0, aclk 139/0, gptp 181/0, gptp-lat 181/0.
  - render_mutants 6/6.
- Other suites and gates:
  - pp_shadow 371/0.
  - `test_builder.py`: all gates pass except gate 11, NOT RUN because it needs the physical build tree.
  - `lint_rtl --check`: 90 <= 90.
  - behave: 317 scenarios passed.
  - check_rtl_source_lists and `xvlog_gate --check` (PASS, 4 = ratchet, pinned `09f9bf38`): pass.
  - check_cpp_idiom, check_py_idiom and measure_test_evidence: pass.
  - The docs gates, including `check_em_dash --base 50e78097`: pass.
  - `git diff --check 50e78097..HEAD` is clean.

Acceptance criteria:
- **Item 1: met in simulation.** In `[C]` the CRF output stays bound for 76 s across five DUT and five switch LeaveAll MRPDUs, 61 s of it on the Listener registration alone. There is no Talker Advertise Leave and no licence drop, and every DUT LeaveAll flags all four MSRP types.
  - **Failing arm:** at pin `424c688f` 17 of 85 checks fail with Run B's burst ends. Every DUT LeaveAll flags only the Domain. The DUT sends four Talker Advertise Leaves: one 5.0 s after a switch LeaveAll, three 15.1 s after the latest probe.
- **Item 2: met in simulation.**
  - **Reproduced first,** with the gate line reverted: 23 of 85 fail. The licence opens 1.34 ms after the first probe, before its TALKER_DEST_MAC_FAIL answer, and the first CRF PDU leaves 3.85 s before the first Listener Ready.
  - **At the head,** nothing leaves during 3.9 s of declared and admitted with no Listener Ready. The licence and the AAF gate follow ACTIVE on every cycle as it opens and closes, through Ready, Asking Failed, Ready Failed and the unbind.
- **Item 3: explained, not fixed.** Milan v1.2 5.3.7.7 Table 5.4 defines FRAMES_TX as a count of observation intervals (at most 1 s; 1 s here) that carried at least one transmitted PDU. It resets at each STREAM_START. Run B's last burst lasted 15.00 s and touched 16 intervals. The PDU total is `CRFT_COUNT` (`0x764`). Milan v1.2 5.3.8.10 Table 5.6 is the Stream Input set, where FRAMES_RX lives. Phase `[F]` grades the counter.
- **Silicon rerun:** pending, the manager's.

Open risks/questions:
- The switch model is Run B's, with its LeaveAll 9.99 s after each DUT LeaveAll; a fixed-period switch is not modelled. Processor #108 (no leavealltimer restart on a received LeaveAll) is unchanged.
- ACTIVE takes the processor's optimistic admission window, which leaves a corner: the gate can open before the slope joins the shaper's sum. This happens only if a Listener Ready registers within three admission rounds of a fresh declaration. The datapath comment records it.
- The new leg's hosted time is unmeasured; locally it builds in about 14 s and runs in about 20 s. The mutants are an explicit target outside the sweep's deadline.
- Not run: act/Docker, hosted CI, `syn/yosys`, hardware.
- VERSION is unchanged (Unreleased changelog entry), and no descriptor changes.
- Seen, not changed: `sw/litex/milan_soc.py:2123` cites `protocol_processor_top.sv:113` for `DESC_MEM_TMO_CYC_P`, which is line 120 at both pins.
