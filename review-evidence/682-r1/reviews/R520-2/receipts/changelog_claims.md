# CHANGELOG.md "Unreleased - processor pin 2ad2f845" claim check

Head `cb359db3424c895010e89b4f9688347857008c85`. Line numbers are `CHANGELOG.md` at that head.
Evidence names an artifact a second reader can open.

| Line | Claim | Result | Evidence |
|---|---|---|---|
| 11 | Contents entry for the section | TRUE | `gates/gen_toc_check.log` rc 0; probes P1/P2 (`probes/`) show the check refuses a missing or renamed entry |
| 46-48 | Issue #682 adopts `2ad2f845`; PRs #156, #159 to #162, and #164 | TRUE | `pp_pin_delta_audit.txt`: first-parent merges `ead80360..2ad2f845` are exactly PRs 159, 156, 161, 160, 162, 164; gitlink in `integrity.json` |
| 49 | GET_COUNTERS spacing measured at grant (#148) | TRUE (wording accepted at round 2) | processor `hdl/aecp/KL_aecp_notify.sv` N_EMIT_WAIT: the stamp follows the clock until `core_done_w`; processor PR #159 body; `SUBMODULES.md:162`, `:175` |
| 50 | Later MAC stalls remain a wire-gap limitation | TRUE | `SUBMODULES.md:177`; the stamp stops at engine completion, not on the wire |
| 51-52 | Capture harness finishes frames crossing its window, at most 2,048 extra cycles | TRUE | `tb/verilator/milan_dp/sim_nxn.cpp:973` bound `c < cyc + 2048` while a frame is in progress |
| 53 | C11 documents landed byte interfaces and TX backpressure | TRUE | processor PR #156 (#27): 02 section 3 byte ports; "TX stalls on `tx_ready_i`" added |
| 54 | C11 also documents synchronous reset | NOT TRUE for this pin | `reset_attribution.txt`: reset wording byte-identical at `ead80360` and `2ad2f845`; introduced by `371505d` via PR #157, already in `ead80360`; PR #156 changes no "synchronous" line; its body says that wording came from PR #157. Finding R520-2-F1 |
| 54 | C11 documents complete FCS-good RX frames | TRUE | PR #156 (#71): integrator section 3 and REQ-REU-003 FCS-good obligation added |
| 55-56 | SRP expiry precedes same-clock reception (#134); Lv and LeaveAll finish MT; New and Join renew IN | TRUE | listener/talker FSM reorder in the pin diff; processor PR #160 body |
| 57-59 | Held DEREGISTER waits for the round boundary (#158); later controllers keep notifications; contents unchanged, delivery later | TRUE | `KL_aecp_notify.sv` `dh_v_r && !em_active_r`; processor PR #161 body; `SUBMODULES.md:179` |
| 60-61 | Declarations precede use (#22); parent analysis budget has zero processor findings | TRUE | processor PR #162; `scripts/xvlog.budget` submodule section "0 finding(s)" |
| 62-63 | Domain/link-edge trigger tests (#42); parent still owns GET_AVB_INFO mapping words | TRUE | processor PR #164: tests only; msrp_mappings words are the integrator's |
| 64 | Processor top byte-identical to `ead80360` | TRUE | `pp_pin_delta_audit.txt`: `hdl/top` identical; top blob `098c5381` at both pins |
| 65 | No port, parameter or register change requires parent adaptation | TRUE | `pp_pin_delta_audit.txt`: the only changed declaration line is a trailing comment on `wr_data_i` in `KL_pp_trace_ring.sv` |
| 66 | Resource gate records this image as baseline F | TRUE | `syn/ooc/pp_resource_baseline.json` three endpoints; `AREA_BUDGET.md:102` "combination F"; `gates/pp_resource_gate_check_baseline.log` rc 0 |
| 67 | ROM ledger adds `2ad2f845` rows; both ROMs unchanged | TRUE | `syn/yosys/rom_digests.tsv:15-16` equal the `ead80360` rows at `:59-60` |
| 68 | Capture census, receipt and product firmware unchanged | TRUE | `git diff e21c1ca0..cb359db3` (18 files) touches no capture, firmware or NVM-capture path |
| 69-70 | Manager repeats #608 cycles and reads #658's map after merge | TRUE as a duty statement | issue #682 acceptance 5, which also lists the stream and counter soak (SUGGESTION R520-2-S1) |
| 71 | VERSION unchanged | TRUE | no parent HDL or CSR change in `e21c1ca0..cb359db3`; `hdl/common/csr/doc/milan_csr.md:22` still `0x0002_0060` |
