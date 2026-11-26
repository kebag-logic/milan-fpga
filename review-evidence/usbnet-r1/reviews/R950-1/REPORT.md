[R950] NEGATIVE - exact head cc49123d2db1e01e80859efa10f8da43a01344ef

Round R950-1, external independent review of PR #1020, relating to #1011 and #1018.
Tree: `0ffb57980a908eb6b330ce5968a9a6bc8c690496`.
Reviewed range: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350..cc49123d2db1e01e80859efa10f8da43a01344ef`, eight commits, 22 changed files.

All five lenses were applied independently. Three findings remain open: one MAJOR and two MINOR. This verdict concerns the implemented round-1 tap and LEDs. It is neither issue completion nor merge acceptance.

## Scope and authorities

Read AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue bodies and public scope rulings, REQUIREMENTS.md (especially REQ-CSR-03, REQ-CBS-*, REQ-CLS-03/06/09 and REQ-VER-*), the register/interface and reset contracts, then the diff/history, then the public author receipts. No private author material or other review report informed the independent findings below.

- [Issue #1011](https://github.com/kebag-logic/milan-fpga/issues/1011): filtered receive copy, checked best-effort injection, rate limit, unchanged SR shaping, routed cost/timing, and physical concurrent-stream acceptance.
- [Station-record amendment](https://github.com/kebag-logic/milan-fpga/issues/1011#issuecomment-7186353239) and [scope rulings](https://github.com/kebag-logic/milan-fpga/issues/1011#issuecomment-7188062527): local forwarding in BOTH directions is required; the -2x destination exclusion and PCP > 1 rejection are accepted; the FX3 document owns the forthcoming record format.
- [Issue #1018](https://github.com/kebag-logic/milan-fpga/issues/1018): LD0 activity/link, LD1 working SuperSpeed path, LD2 connected streams, LD3 selected-clock satisfaction, AECP selection tests and board observations.
- [FX3 NETWORK.md at its published head](https://github.com/kebag-logic/usb-audio/blob/ca34e0d2272eb14e126f8f6d67a98ee596057ff6/docs/NETWORK.md): two-word length/kind header and 16-byte station payload. The present FPGA one-word FRAME/HOST/DETACH format is different. Adoption, local forwarding and the bus binding remain OPEN SCOPE, not findings against functionality already present in this head. The FPGA tap is thread-agnostic and its bus is terminated.
- [Published author evidence](https://github.com/kebag-logic/milan-fpga/tree/7ca25ea258496fab3ab73d76b7c7138cb503c1f4/review-evidence/usbnet-r1/author) is source execution evidence. No manager source bank exists or is claimed here.

## Findings

### R950-1-01 - MAJOR - Conformance, RTL, Robustness, Tests

**Artifact:** `hdl/usbnet/KL_usbnet_tx_inject.sv:314`, `:340`, `:345`; `tb/verilator/usbnet/sim_main.cpp:507`; receipt `rate-hold.log` and reproducer `rate_hold_probe.cpp`.

**Authority/evidence:** #1011 requires a rate limit. `docs/design/USB_NET_PATH.md:105` defines a wire-octet token bucket with a 3,200-octet burst. `start_w` spends tokens when preparing an output frame, independently of arbitration or acceptance. While that frame waits, the bucket refills to its full capacity. The pending, already-paid frame then leaves in addition to the full bucket.

The exact-head tap, using its existing 1 MHz / 800 kb/s test parameters, was given four 1,000-octet frames with injection disabled. After the pending frame's tokens refilled, injection was enabled. First-beat times were 1, 1605, 3210 and 4814 clocks after enabling. The fourth frame brings the wire charge to 4,096 octets; the allowed envelope is only 3,681.4 octets. Even at the fourth frame's simulated wire completion, after 6415 clocks, the completed 4096 octets exceed the 3841.5-octet envelope. Both independent assertions fail (exit 1). A blocked arbitration grant has the same accounting mechanism. The ordinary steady-rate suite and all existing rate plants pass, so they do not detect this defect.

**Impact:** releasing a held injection permits more than the advertised burst, by as much as one previously reserved frame's cost. This does not demonstrate changed CBS arithmetic or loss of datapath priority; it demonstrates that the output traffic fails its stated limiter envelope.

**Required outcome:** account for a pending frame so the actual injection stream obeys the specified rate/burst envelope after arbitrary grant or downstream waits. Preserve full-frame, gapless transmission and datapath priority.

**Verification:** add an independently calculated cumulative wire-octet envelope check after a long disabled-injection interval, arbitration delay and MAC backpressure, using short and maximum-size frames. It must fail this head and pass the correction, alongside the existing rate and priority suites.

### R950-1-02 - MINOR - Tests

**Artifact:** `tb/verilator/usbnet/sim_main.cpp:218`, `:306`; `hdl/usbnet/KL_usbnet_rx_copy.sv:236`; receipts `last-plant.log`, `last-plant.rc`; reproducer `run_last_probe.py`.

**Authority/evidence:** the bus contract in `docs/design/USB_NET_PATH.md:150` requires `last` on each record's final word so the transfer can be committed. The harness captures only `up_data_o` and reconstructs records from lengths. It never observes `up_last_o`. A disposable plant replacing the receive block's final-word marker with constant zero passes all nine cases, including “records toward the computer are well formed”, with exit 0.

**Impact:** a broken transfer-commit marker can pass the current tests while preventing the receiving bus adapter from committing valid transfers. The unmodified RTL does produce the marker; this is a demonstrated verification hole, not a claim that the present marker logic is broken.

**Required outcome:** independently grade exactly one accepted terminator per record, precisely on its final word, including odd lengths and stalled final words; grade marker stability while stalled.

**Verification:** the constant-zero plant and premature/extra-marker plants must fail their dedicated checks; the original exact-length streams must pass.

### R950-1-03 - MINOR - Conformance, RTL, Robustness, Tests, Docs

**Artifact:** `docs/design/USB_NET_PATH.md:137`; `hdl/usbnet/KL_usbnet_rx_copy.sv:45`; `hdl/usbnet/KL_usbnet_tap.sv:105`; receipts `rx-length.log`, `rx-length.rc`; reproducer `rx_length_probe.cpp`.

**Authority/evidence:** the current FPGA bus-record table specifies FRAME lengths 14 through 1518 in BOTH directions. The integrated receiver instead uses the default `MAX_LEN_P=2000`. An exact-head probe presents broadcast frames of 1518, 1519, 2000 and 2001 octets: the first three produce records with those respective lengths; only 2001 is dropped. The current receive tests stop at 1514 and do not compare the upper boundary to the stated interface contract.

**Impact:** a consumer implementing the documented record limit can receive an out-of-contract record. This is a mismatch inside the present FPGA contract, separate from the already acknowledged adoption of the FX3 format next round. It is not pure prose residue because the disputed text specifies an interface length and the observable output violates it.

**Required outcome:** make the integrated receive limit and the authoritative direction-specific record limits agree, consistently with the approved downstream contract. Do not silently enlarge a consumer's accepted range.

**Verification:** test maximum-minus-one, maximum and maximum-plus-one in both directions, checking output bytes, length, verdict, terminator and recovery of the following valid frame. Reconcile the document and integration parameter with those results.

## Applied lenses and executable evidence

**Conformance:** examined the complete `KL_usbnet_pkg.sv` rules against #1011 and its amendments: host/other unicast, broadcast/multicast, both reserved destination blocks, AVTP subtype bit 7, both recognised VLAN tags, stacked-tag rejection, source identity and PCP 0/1 versus higher priorities. Inspected the corresponding 26 RX classes (attached and detached), 21 TX cases and unknown-record recovery. Findings 01 and 03 leave this lens unclean. The local path and station-record adoption are explicitly pending scope.

**RTL:** examined all six added RTL files and `sw/litex/usbnet_soc.py`, plus each changed SoC hook. Traced speculative FIFO rollback/commit, whole-frame admission, synchronous reads, last-byte conversion, strict priority after `tx_sf`, outstanding datapath-frame accounting and request/ack crossings. Compared the substituted frame-end toggle to `docs/design/REBOOT_RESET.md` and the gPTP destination observer. Reviewed the input register added in the final commit against the preceding version. The same-clock observer never drives RX backpressure. The existing shaper and queue sources are unchanged. Findings 01 and 03 leave this lens unclean.

**Robustness:** examined malformed/short/stacked-tag handling, unknown records, invalid station addresses, detach/stale host records, FIFO full/drop/rollback, odd-byte padding, stalled injection, token replenishment, link-down activity and reset domains. Existing full-buffer, contention, stalled-MAC and detach cases pass. Added held-injection and receive-size boundary probes fail as recorded above. No exhaustive reset-phase sweep or physical clock-loss test was run. Findings 01 and 03 leave this lens unclean.

**Tests:** independently executed the two exact-head RTL baseline harnesses; all 43 named RTL plants were detected. Independently executed the unchanged CBS, shaping-core and queue suites: all pass. Executed the four firmware LED tests on the shipping configuration and every checked-in Arty model (`arty_4x4`, `arty_8ch`, `arty_current`), and all eight LED plants: all detected by their specified assertions. Inspected `test_aecp.cpp:294` onward: all three LD3 cases invoke SET_CLOCK_SOURCE and check the descriptor update; locks and binding come from explicit mocks. Traced those observations into `ctrl_app_aecp.c`, `aecp_face.c` and the fabric counters; these unit cases are not a real MMIO/board demonstration. Findings 01, 02 and 03 leave this lens unclean.

**Docs:** compared the new design page, source port comments, CSR placement and firmware map generation against the implementation and public scope decisions. Reviewed the public receipt index, gate results, ALINX identity, firmware identity, CSR row diff, route recipe, timing extracts, utilisation and hierarchy. No new prohibited lane/review marker was found in added source comments. The receive-size contract mismatch is substantive (03). The subsequent scope update must carry the already-approved local forwarding and FX3 record adoption into the implementation and its published contract; they remain explicitly open scope here.

## Reviewer-owned ledger

All rows name the exact source head examined. No clean covering round is claimed where a finding remains open.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (01,03) | #1011/#1018 and rulings; REQUIREMENTS.md sections 3/5/6/8; KL_usbnet_pkg.sv; USB_NET_PATH.md; rate-hold.log; rx-length.log | R950-1 applied; no clean coverage | cc49123d2db1e01e80859efa10f8da43a01344ef |
| RTL | UNCLEAN (01,03) | hdl/usbnet/*.sv; sw/litex/usbnet_soc.py; milan_soc.py changed hooks; REBOOT_RESET.md | R950-1 applied; no clean coverage | cc49123d2db1e01e80859efa10f8da43a01344ef |
| Robustness | UNCLEAN (01,03) | rx_copy/tx_inject/tx_arb; sim_main.cpp; sim_leds.cpp; held-grant and RX-size probes | R950-1 applied; no clean coverage | cc49123d2db1e01e80859efa10f8da43a01344ef |
| Tests | UNCLEAN (01,02,03) | rtl/summary.json; firmware/summary.json; firmware/arty-summary.json; shapers/summary.json; last-plant.log; test_aecp.cpp | R950-1 applied; no clean coverage | cc49123d2db1e01e80859efa10f8da43a01344ef |
| Docs | UNCLEAN (03) | docs/design/USB_NET_PATH.md; docs/DOCUMENTATION_AUDIT.md delta; public author/receipts; PR body and public scope rulings | R950-1 applied; no clean coverage | cc49123d2db1e01e80859efa10f8da43a01344ef |

## Evidence boundaries and pending duties

The author receipts report ALINX SoC-export equality for three shapes, with timestamps normalised and generated comment order treated as a multiset, plus equality of all 136 referenced RTL sources. This is not a new ALINX physical build. The separate firmware receipt records identical base/head ELF hashes and map headers for the 1x1 and 8x8 product images. The feature-disabled compile guards and board-only hooks support that scope by inspection. These large builds were not rerun here.

The routed Arty evidence is for integration head `660ed296780e3ff1e5cdc88b9b1ce32d08e94b49`, containing this change and the Arty split work, not a stand-alone source-head route or the final current-dev candidate. The selected recipe is 80 MHz system / 50 MHz datapath, one stream, split firmware, `--usb-net`, `AltSpreadLogic_high`, four implementation threads. The published JSON reports Slow/Fast at 0/85 C all met, worst setup 0.601 ns, worst hold 0.050 ns, zero failing endpoints and routing errors. The retained raw extracts cover the two 0 C reports; the 85 C values are reported by the author's JSON, not independently remeasured here. The alternate final recipe also meets at 0.072 ns setup. Against its published pristine integration baseline, the selected totals change by +1221 LUT, +832 FF, +2 RAMB36, +415 slices; the tap accounts for 1019 LUT, 791 FF, 2 RAMB36. The CSR comparison adds rows without moving old rows. Physical calibration NOT RUN; no field skip or desk pass is hardware proof.

The manager still owns the current-dev candidate construction and builder/native bank validation, hosted/local workflow acceptance and public receipts, the added LED task's Arty service census, review reconciliation, and eventual containment. The source base is c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350; the assigned live-dev reference is e275d7950ef3385753e6a15d2e191ba855b171ed, which must be refreshed at the merge turn. This review did not execute or infer a manager source bank, run prohibited full banks, run a physical build, or claim skipped hosted contexts as executed jobs.

Local forwarding both ways, the adopted FX3 station/frame records, bus scheduling/wiring, physical controller operation with saturated networking and clean audio counters, and each LED observed on the board remain open. No merge, issue closure or acceptance-criteria completion is authorised by this report.

## Prior public findings and preservation

After the independent findings, verdict and ledger were written, the public PR review submissions, inline threads and conversation were read. There were zero review submissions, zero inline threads, and two review-start notices; there were no prior public findings to resolve or retain. `prior-public-review-state.json` records that returned public state. Neither another review report nor another reviewer's private material was read.

`tree-verification.json` verifies all 1998 parent tracked blobs, their executable/symlink modes and exact index entries directly against the stated head. It also verifies populated submodule heads, tracked blob bytes/modes and index entries for the protocol processor, gPTP processor, stream primitives, TSN stack and SRP library. All required gitlinks match. The unused `external` gitlink remains unpopulated, as permitted by CONTRIBUTING.md. No source edit, commit, push or GitHub write was made. Disposable plants, builds and downloaded evidence remain under `scratch/` and are excluded from publication.

`execution.txt` gives the foreground commands, expected return codes and receipt limitations. `MANIFEST.sha256` enumerates the publishable scripts and receipts. The receipt paths are relative to this packet; private installation paths in diagnostics are replaced with role placeholders without changing results. All started campaigns and probes have finished.

R950-1 FINISHED
