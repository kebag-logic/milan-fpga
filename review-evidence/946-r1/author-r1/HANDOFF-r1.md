# [A797] #946 round 1 — monitor-context format for streams above 0 — handoff

Status (21:00): **REVIEW READY. FIRMWARE-ONLY fix in the split platform; every gate done.** Lane head `66c6edf3`
(dev-soft-core `cb96336d` + 6 commits); train composition `d6d71354` (scratch only: PR #945 `b1f1161b` + the lane,
`git merge-tree` clean). Passing on both bases: the firmware gate (units and all planted-defect campaigns, the 19 new
ones among them), fw_coverage, the receive stack's suite with the new N=8 contract and its 4 engine defects, the docs
workflow steps; on the composition, the sweep (65/65 suites, 2,713,122 checks), the twin and its plants, and the split
boot simulation (the product image writes inputs 1-7's formats before ready). The CPU budget rows carry (budget images
hash-equal to the train's). One finding, not a STOP: the ROM ledger is half a RAMB36 past at one point on each base
(section 6, S14 debt by the owner's loose-BRAM rule); the lane leaves the ledger untouched, so it merges cleanly.
Posted: `[A797] TAKEN` (issuecomment-6986707046) and `[A797] REVIEW READY` (issuecomment-6989883608). Nothing
pushed, no PR opened (the manager's).

## 1. Task and authority
- Issue #946 (part of #665). Lane `946-ctx-fmt` from dev-soft-core `cb96336d`. Composition: PR #945
  `flip-train-1117` `b1f1161b`, this lane as step 12.
- Evidence: the gating handoff 11.5 F-G1/F-G2/F-G3 and its `e-streams/` receipts (inputs 1-7 bound alone: FRAMES_RX 0,
  UNSUPPORTED_FORMAT about +1/s, GET_STREAM_INFO CONNECTED in `0205022002006000`).
- Posted: `[A797] TAKEN`, #946 issuecomment-6986707046 (18:5x). Nothing else posted. Nothing pushed.

## 2. Cause, confirmed on the RTL (line numbers at `cb96336d`)
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:525-531` `fmt_ok_w` compares each PDU against `fmt_r`; a mismatch
  raises UNSUPPORTED_FORMAT and the PDU gets no accept verdict (`:596-597`, `:1011-1021`).
- Stream 0: `fmt_r <= fmt0_i` (`:948-951`), wired to `aecp_in0_fmt` (`hdl/milan/milan_datapath.sv:7836`).
- Streams above 0: `fmt_r` is read from LCTX w2/w3 (`:734-735`, `:1001-1006`). The engine writes CFG words only for
  stream 0 (`:1175-1177`; the writes `:692-711`). The only other writer is the window port (`:719-723`), driven solely
  by the CSR 0x800 window (`milan_datapath.sv:7855-7856`; `hdl/common/csr/milan_csr.sv:1888-1897`).
- No shipping firmware writes it. Every harness that receives on a stream above 0 writes the FMT words itself, which is
  why none saw F-G1: `tb/verilator/avtp_rxmon/sim_main_nx.cpp:433-434`, `:583-584`, `:914-915`;
  `tb/verilator/milan_dp/sim_nxn.cpp:6320-6321`, `:8034-8035`.
- **Reproduced on the RTL at N=8** (`sim_ctxfmt.cpp` [CF1], section 5): with the format words unwritten, inputs 1-7
  each give no accept verdict and count UNSUPPORTED_FORMAT for an in-format PDU; input 0 receives.
- **Failing test first, at the level of the defect (firmware):** with the platform's writes removed (the shipped
  behaviour, planted as `sink-open-unwritten` / `sink-change-unfollowed`), `Sinks.S1` fails at 8x8/1if for each of
  inputs 1-7 by name ("input 1 holds none" ... "input 7 holds none"), and S2 fails ("SET_STREAM_FORMAT's new format
  reaches input 7's context"). With the fix they pass.

## 3. Decision: FIRMWARE-ONLY (no RTL, no re-route, no mailbox change)
The split firmware can write each input's format into its monitor context race-free:
- **Reachable.** The split CPU's `milan_csr` region is the datapath CSR window (`plat/ctrl_plat_csr.h:4-13`); shipping
  split firmware already writes the 0x800 window (MAAP's talker DMACs, `plat/ctrl_plat.c:49-74` ->
  `maap/maap_csr.c:52-60`). MBX_N_IF is 1 (`mbx/mbx_contract.h:27`).
- **CDC.** None between the window and the context RAM: `milan_csr` and the monitor both run on `axis_clk`
  (`milan_datapath.sv:2824`, `:7820`). The CPU->CSR crossing is the SoC's existing AXI-Lite crossing
  (`sw/litex/milan_soc.py:802-829`), the one every split CSR write takes.
- **Arbitration.** A window write is accepted in any cycle the engine does not write
  (`KL_avtp_rx_monitor_ctx.sv:719-723`). The CSR holds the request until accepted and holds off the next AXI write
  (`milan_csr.sv:1112-1118`, `:1665`). The engine never writes FMT for s>0, so a window-written format survives every
  bind walk (`:1175-1177`; held by [CF2]-[CF5]).
- **Race-free.**
  - A format moves only while its input is unbound: SET_STREAM_FORMAT on a bound STREAM_INPUT answers
    STREAM_IS_RUNNING (`aecp/aecp_commands.c:125-129`, `:327-328`), SET_CONFIGURATION refuses while any stream is
    bound (`:182-188`). Held by S2 and its plant `set-format-bound-accepted`.
  - A PDU reaches context s only while entry s is bound and its stream_id matches (`avtp_stream_parser.sv:193-196`;
    `KL_avtp_rx_monitor_ctx.sv:431-432`); the stream_id is published only after the probe's response.
  - The formats are written: after the open (every face acknowledged), before ADP starts, so before any probe (S1);
    for SET_STREAM_FORMAT, synchronously once its commit is acknowledged (S2); for a change the face defers (commit
    late, IN_PROGRESS, done again) or a change of another kind, at the platform's poll once a later commit is
    acknowledged (S4, S5). Never for a commit that is not acknowledged (S3, S4), so the monitor never judges against a
    format no controller sees.
  - The window's last write (the selection restored) is held off at the CSR until FMT_HI was accepted, so both words
    are in the RAM before the firmware continues.
  - Stream 0 unchanged (keeps `fmt0_i`; never selected, S1). Unbind: the format is the STREAM_INPUT's, kept, and the
    next binding receives at once ([CF5]).
- **Clauses.** Milan v1.2 Table 5.6 and 4.4.2.2 (only a PDU not in the current format is UNSUPPORTED_FORMAT and
  discarded); IEEE 1722.1-2021 8.2 (each sink binds independently) and 7.4.16 (GET_STREAM_INFO's current format).
- The RTL fallback is not needed (and is outside this lane's allowed changes).
- **Design change at 19:1x (from the 18:46 report):** the first implementation (`f4f28b11`) added a port to the AECP
  face. `aecp_face.c` is compiled into every CPU-budget image and its `publish` is on the split image's hot list, so
  every budget image would have moved, with 8x8/1if's TRANSMIT row at 76.81 of 77 ms. `56a98dde` moved the whole
  mechanism into the platform; the face is byte-identical to base.

## 4. Changes (file:line at `0749e0d8`, reason)
- `sw/firmware/ctrl/plat/ctrl_plat_csr.c:70-80` `ctrl_plat_csr_sink_format`: read STRM_SEL, select listener n, write
  FMT_LO then FMT_HI, write the selection back. `:82-104` `ctrl_plat_csr_sink_context`: an AAF STREAM_INPUT above 0
  on AVB_INTERFACE 0 in the configuration in force, with its current format; not a short descriptor.
  `ctrl_plat_csr.h:60-62`, `:140-161`: offsets and contracts.
- `sw/firmware/ctrl/plat/ctrl_plat.c:129-201`: `sink_write` (every context, or one), the face's `changed` port wrapped
  (`sink_changed`: SET_STREAM_FORMAT written once interface 0 owes nothing after the call; anything else owed with the
  commit count before it), and `plat_poll` (owed formats once a later commit is acknowledged, then the console).
  `:300-303` wraps the port at composition; `:335` registers `plat_poll` in the console's slot (the poll table is full,
  8 of 8); `:357-359` writes every input after `ctrl_app_open_aecp`. State is a file static: `struct ctrl_plat` and
  its ledgered size are unchanged.
- `sw/firmware/ctrl/plat/README.md`: the ports (the receive monitor's formats) and the tests (`platsinks`).
- Tests: `test/test_plat.cpp` C5, C6; new `test/test_plat_sinks.cpp` S1-S5; `test/plat_arms.py` `arm_platsinks`,
  `sink_arms` (8x8/1if, 1x1/1if); `test/test_ctrl_firmware.py` runs them in the suites and the coverage run;
  `test/sink_mutants.py` (19 defects) registered in `test/ctrl_mutants.py` (named sources, table, arm map).
- RTL contract test: `tb/verilator/avtp_rxmon/sim_ctxfmt.cpp` [CF1]-[CF5] at N=8, `ctxfmt_mutants.py` (4 defects),
  Makefile targets `ctxfmt-build`/`ctxfmt` in `run`; `avtp_rxmon_nx_wrap.sv:93-97`, `:137` sizes the testbench wrap's
  match index by its stream count (was 2 bits, folding streams 4-7 onto 0-3 at N=8; N=4 unchanged, 218/218).
- `scripts/measure_test_evidence_readers.py`: the new driver's DUT-source disposition.
- No RTL, no mailbox contract, no AECP face, no budget bound. Every edit sits in hunks the train does not touch.

## 5. New checks and their planted mutants
| Check | Holds | Planted defects (each caught by its words) |
|---|---|---|
| `Plat.C5SinkFormatSelectsTheInputWritesItsFormatAndRestores` | SEL read, SEL=n, FMT_LO, FMT_HI, SEL restored, exact | `sink-format-halves-swapped`, `sink-talker-selected`, `sink-selection-not-restored`, `sink-selection-not-read` |
| `Plat.C6SinkContextIsAnAafInputAboveZeroOnInterfaceZero` | AAF input above 0, interface 0, configuration in force, length >= 128; not 0, CRF, another type/interface/configuration, short | `sink-input-zero-written`, `sink-crf-input-written`, `sink-other-type-written`, `sink-other-interface-written`, `sink-other-configuration-written`, `sink-short-descriptor-read` |
| `Sinks.S1...AtReady` (8x8/1if) | inputs 1-7 hold their current format after the open's acknowledged READY publication and before ADP starts; 0 and CRF 8 never selected; SEL restored | `sink-open-unwritten` (shipped behaviour: "input 1 holds none" ... "input 7 holds none"), plus the C5/C6 window defects |
| `Sinks.S2...ABoundInputRefuses` | unbound input 7 SET_STREAM_FORMAT 2ch: SUCCESS, context 7 alone, right after its acknowledged commit; bound: STREAM_IS_RUNNING, nothing written | `sink-change-unfollowed`, `sink-change-before-commit`, `set-format-bound-accepted` |
| `Sinks.S3...WritesNoContext` | a face never acknowledged writes nothing | `sink-open-before-acknowledgement` |
| `Sinks.S4...WrittenOnceInForce` | commit held: IN_PROGRESS, nothing written; acknowledged: done again, SUCCESS, input 7's context holds 2ch after an acknowledged commit | `sink-change-unacknowledged`, `sink-owed-before-acknowledgement`, `sink-owed-unwritten` (S4's deferred path) |
| `Sinks.S5...InForce` | SET_NAME and a STREAM_OUTPUT's SET_STREAM_FORMAT leave every context at its format in force | `sink-owed-from-its-own-commit` |
| `[CF1]`-`[CF5]` (`sim_ctxfmt.cpp`, N=8, 96 checks) | unwritten: inputs 1-7 discard; written unbound: survives the bind, first PDU accepted, words read back; each context its own words; written the cycle before the bind; unbind + 100 ms silence keep it | bind walk taking `fmt0_i` for every stream ([CF3]), `fmt0_i`'s count for s>0 ([CF3]), window write in the neighbouring context ([CF2]), unlock walk over FMT_HI ([CF5]) |

19 of 19 firmware defects and 4 of 4 engine defects caught (receipts `firmware/`, `rtl/`). The same suite at 1x1/1if
(no AAF input above 0): nothing written at boot; input 0's SET_STREAM_FORMAT is published and writes nothing.

## 6. Gate table
Heads: lane `66c6edf3` (code and tests as `0749e0d8`; `66c6edf3` adds two README lines); composition `d6d71354`
(scratch only; its tree differs from the gated `8dbd0a48` by those two lines).

| Gate | Lane | Composition |
|---|---|---|
| New firmware arms (plat 12, platsinks 5 + 5) | PASS | PASS |
| Firmware gate `test_ctrl_firmware.py --require-rv32 --self-test`: suites | PASS (75 verdicts, 0 failed) | PASS (74 verdicts, 0 failed) |
| ... control campaign | 736 of 736 caught (19 `sink-*`/`set-format-*` among them) | 816 of 816 caught |
| ... AECP and SRP campaigns, pins | PASS: 1,546 defects caught in all, 0 escaped; `test_ctrl_firmware: PASS` | PASS: 1,778 caught, 0 escaped; `test_ctrl_firmware: PASS` |
| `fw_coverage.py --check` | PASS (39 files); `ctrl_plat.c`, `ctrl_plat_csr.c` 100 % lines and branches after exclusions | PASS (40 files), same |
| `avtp_rxmon` suite (pinned Verilator 5.050) | PASS: flat, N=4 stack 218/218, lockstep N=1 116 / N=8 119, lockstep and format mutants 14/14 and 13/13, CTXFMT N=8 96/96, its mutants 5/5 | in the sweep |
| Twin, twin plants | twin: the one finding dev-soft-core `cb96336d` has itself (owed row `split-talker-failed`), captures byte-identical to the base's (`split.json`, `fabric.json`, `report.json`) | twin 0 findings, every plant refused (rc 0) |
| Sweep, 4 shards (`run_all_suites.sh`) | hosted CI | PASS at `8dbd0a48`: 65 of 65 suites, 2,713,122 checks, 0 failures; declared skips: tsn_fuzz's 4 external-generator campaigns |
| Docs workflow steps | PASS, 92 applicable (5 train-only scripts absent) | PASS 97/97 |
| Split boot simulation 8x8 | - | PASS: ready 67.241 ms, 49 writes before ready, the first 18 equal; writes 22-49 = SEL k, FMT_LO 02006000, FMT_HI 02050220, SEL back, k = 1..7, 2,858 bus cycles; against the train head: +28 writes, +0.107 ms to ready (67.134 -> 67.241); 1x1: no write, +0.042 ms (27.981 -> 28.022) |
| CPU budget images (arm A) | - | hash-equal to the train's recorded p11 images: 1x1 `55484254e638ed7f`, 8x8/1if `175418f4b5b1a9d4`; no budget-image input changed, so every row carries (the train's rule: hashes equal) |
| Platform image ledger (`plat_ledger.py --self-test`) | FINDING 8x8/1if 56.5 RAMB36 past the 56 budget (rom 131,464 B, 392 B past 64 half tiles); 1x1 43/44, 8x8/2if 60.5 within its entry | FINDING 8x8/2if 63 RAMB36 past its 62.5 entry (rom 140,008 B, 744 B past); 1x1 45/46, 8x8/1if 58.0 within its entry |
| Release (all-fabric) image | no input changed | no input changed |

**ROM (S14 debt, not a STOP):** the platform code is +980 B of RV32 text (`ctrl_plat.o` +544, `ctrl_plat_csr.o` +436).
Each base loses half a RAMB36 at one point: dev-soft-core's 8x8/1if (56 -> 56.5, no entry there; the train already
carries `platform-8x8-one-interface` at 58.0) and the train's 8x8/2if (`platform-8x8-two-interfaces` 62.5 -> 63.0).
The lane does not edit the ledger, so it merges cleanly; the composition needs `platform-8x8-two-interfaces` raised to
63.0 by the owner's rule (an image past its entry raises it).

## 7. F-G2, F-G3, the release image
- **F-G2: not the same cause.** The parser classifies a PDU to ONE context: its match loop keeps the highest matching
  enabled entry (`hdl/ieee1722/avtp/avtp_stream_parser.sv:193-196`). With inputs 0 and 1 bound to one stream_id,
  every PDU goes to input 1 only; with this fix input 1 receives and input 0 still receives nothing. Fan-out of one
  stream to two inputs needs RTL (parser, monitor, depacketizer) and a ruling on whether it is required. Own ticket.
- **F-G3: already owned by open #943**: the datapath's GSI face answers a STREAM_OUTPUT's `stream_dest_mac` from the
  fabric MAAP engine the split does not build; the train's twin pins it as owed row `stream-output-0-dest-mac`.
- **Release (all-fabric) image: shares F-G1, left byte-identical.** Its firmware writes none of the words either. Its
  AECP is the fabric's, so a firmware write could follow the boot default but not a SET_STREAM_FORMAT; the fix there
  is RTL (the engine taking each sink's format on the bind edge, as for stream 0), with area and timing risk. Own
  ticket.

## 8. Open questions / STOP conditions
None. No mailbox-contract change, no budget row moved (the budget images are unchanged), no RTL.

## 9. Posting
- `[A797] REVIEW READY`: `REVIEW-READY-comment.md`, posted on #946 as issuecomment-6989883608.
- `PR-BODY.md`: base `dev-soft-core`, `Closes #946`, `Relates to #665`. The manager pushes and opens the PR.
- For the composition (step 12): raise `platform-8x8-two-interfaces` in `sw/litex/ctrl_memory.py` from 62.5 to 63.0
  RAMB36 by the owner's rule (its image's rom 140,008 B needs 69 half tiles; `receipts/ledger/`).
- `bench-diagnosis.md` in this directory is the gating lane's note of 18:18 (not this lane's): the hand-write
  diagnosis was not run on the bench because nothing there can make the CPU write the window; it names "firmware that
  writes the three words on a bind" as what a fix needs, which is what this change does. Left as found.
- Scratch state (outside the checkout, not in this directory): the composition and gate clones under the lane's
  scratch directory; no unit of this lane is running.
