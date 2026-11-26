[R949] NEGATIVE - exact head cc49123d2db1e01e80859efa10f8da43a01344ef

# R949-1: internal independent review of PR #1020 (#1011, #1018)

- **Round.** R949-1, internal cleared-context reviewer.
- **Head.** `cc49123d2db1e01e80859efa10f8da43a01344ef`, tree `0ffb57980a908eb6b330ce5968a9a6bc8c690496` (verified in the clone).
- **Base.** Source base `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350` (dev-soft-core), 8 commits, 22 files, +3004/-12.
- **Reconstructed from.** AGENTS.md and CONTRIBUTING.md; docs/README.md; #1011 body and its three owner-side comments (7165838061, the 7186353239 interface amendment, the 7188062527 rulings); #1018 body; the diff and history; the author's evidence packet `review-evidence/usbnet-r1/author` at 7ca25ea2; the hosted check runs at the head.
- **Not read.** No private author material and no other reviewer's report was read before this verdict.
- **Verdict.** NEGATIVE.
  - One BLOCKER: the new suite breaks the mandatory Verilator sweep and its CI shard selection.
  - One MAJOR: after a reset of the system-clock side alone, injection never resumes, and the module header says that reset is harmless.
  - Three MINOR findings, one RESIDUE and two SUGGESTIONs.
  - All five lenses were applied and all five are UNCLEAN at this head.

## Findings

### F1 BLOCKER - Tests, Docs - `tb/verilator/usbnet/` against `scripts/suite_shards.py:80` (SUITE_SECONDS) and `scripts/suite_tally.py` - the new suite is not wired into the sweep, so the sweep fails
- **Authority.**
  - The `suite_shards.py` docstring: "New suites must enter both the discovered inventory and duration table".
  - The `suite_tally.py` NOCOUNT rule: "A suite that measured nothing is an UNKNOWN ... It fails the sweep".
  - CONTRIBUTING section 2.1 step 7 and section 3 make `scripts/run_all_suites.sh` mandatory.
  - AGENTS section 7 requires exact-head `verilator-suites`.
- **Evidence at the head.**
  - `python3 scripts/suite_shards.py --suite-root tb/verilator --ci-pieces --shard 0/27` exits rc 2 with "usbnet: inventory suite with no recorded duration in SUITE_SECONDS" (`receipts/suite_shards_shard0.txt`).
  - `suite_shards.py --selftest` reports `FAIL head: usbnet: ...` and "selftest: 1 FAILURE(S)", rc 1 (`receipts/suite_shards_selftest.txt`).
  - At base c34e7d8b both pass, rc 0 (`receipts/suite_shards_base.txt`), so the failure comes from this change.
  - `run_all_suites.sh:342` aborts on that self-test before running any suite. `rtl.yml:336` and `:596` run the same self-test in the hosted jobs.
  - The suite also prints no tally line in a shape `suite_tally.py` reads ("PASS: 0 failure(s)", "PASS leds: 0 failure(s)"). `suite_tally.py` on its log gives `NOCOUNT usbnet`, ACCOUNTING FAILURE, rc 1 (`receipts/suite_tally_usbnet.txt`). `run_all_suites.sh:502` then exits 90.
  - The suite index (`tb/verilator/README.md`, `docs/testing/TESTING.md`) does not list `usbnet`.
- **Impact.** Neither the mandatory local sweep nor the required hosted `verilator-suites` context can pass at this head. The new checks are never tallied.
- **Required outcome.**
  - `usbnet` is registered in SUITE_SECONDS following the docstring's new-suite steps, with the shard budget re-checked.
  - Both harnesses print a recognised tally shape.
  - The suite appears in the suite index.
- **Verification.**
  - `suite_shards.py --selftest` PASS.
  - The `--ci-pieces` selection exits rc 0.
  - `suite_tally.py` on the usbnet log shows no NOCOUNT.
  - `run_all_suites.sh` and hosted `verilator-suites` pass at the new head.

### F2 MAJOR - RTL, Robustness, Tests, Docs - `hdl/usbnet/KL_usbnet_tx_arb.sv:34-40`, `:96-97`, `:133-137`, `:166-173` - injection stops for good after a reset of the system-clock side alone
- **Mechanism.**
  - The grant needs `out_r == 0 && answered_w`.
  - Suppose the system side is reset after an odd number of granted injections, all answered. `req_r` goes back to 0, but the transmit side's `ack_r` stays 1.
  - The next datapath frame end is then taken as an answer and not toggled. `out_r` counts that frame in but never out, so it stays one high.
  - `grant_lo_w` never holds again.
- **Probe** (`scripts/probe_reset_cases.cpp`, `scripts/build_probe.sh`; `receipts/probe_arb_reset.log`). After a system-side reset following 1 injection:
  - 0 of 3 later computer frames are injected (`tx_passed_o`=3, `tx_injected_o`=0);
  - 3 of 4 datapath frame ends are counted.
  - Controls: after 2 injections, or with both sides reset, 3 of 3 frames are injected and 4 of 4 ends are counted.
- **Authority.**
  - The module's own RESETS paragraph says such a reset "only lengthens the reboot wait to its bound". That is false.
  - AGENTS section 6, Robustness: "reset during activity".
  - CONTRIBUTING section 1 reset rules.
  - No harness case resets either side alone: the bench resets both together, and only at construction.
- **Reachability.**
  - In the product, the `macsys` reset is `sys.rst | reinit`.
  - The link guard raises `eth_rst` together with `reinit`. Both sides are therefore reset, and the counters agree again provided the transmit clock runs (`milan_soc.py:1795-1867`).
  - A system reset during which the transmit side's synchronous reset sees no clock edge reaches the defect. So does any later reset of one side alone.
- **Impact.** The computer's transmit direction stops silently and permanently: frames are counted as passed but never sent, until both sides are reset. The documented reset contract is wrong.
- **Required outcome.**
  - A reset of either side alone leaves the arbiter able to grant again: request and acknowledge resynchronised, or a bounded recovery.
  - The RESETS text states the real behaviour.
  - A harness case resets each side alone during activity, after both odd and even grant counts, with a planted defect it catches.
- **Verification.** The probe's three cases pass, and the new case catches its planted defect.

### F3 MINOR - Conformance, Docs, Tests - `hdl/usbnet/KL_usbnet_rx_copy.sv:45` (`MAX_LEN_P = 2000`, not overridden in `KL_usbnet_tap.sv:102`) against `docs/design/USB_NET_PATH.md:137` - receive records are longer than the bus contract allows
- **Authority.** The page says a FRAME record is "14 to 1518" octets in both directions, and calls itself "the contract the USB device firmware works to".
- **Probe** (`scripts/probe_rx_length_cases.cpp`; `receipts/probe_rx_length.log`). Received broadcasts of 1519, 1600 and 2000 octets are copied with exactly those record lengths. A 2001-octet frame is refused (RXV_SHAPE). The harness's longest RX case is 1514.
- **Impact.** A USB device firmware sized to the documented 1518 limit receives longer records.
- **Required outcome.** The RTL and the contract agree, either by bounding the copy and counting the refusal, or by documenting 2000 with its reason. The boundary is tested.
- **Verification.** The probe at 1518 and 1519 behaves as the chosen contract says, and a planted defect at the bound is caught.

### F4 MINOR - Tests, Docs - stated rules with no test and no planted defect
- **(a) RX length rule.** The length half of RX rule 2 (`KL_usbnet_pkg.sv:122`, `len < need_octets(h)`) can be removed and the harness still passes (`probe_rx_length_rule_removed` survives).
- **(b) TX header-length rule.** The TX header-length rule for frames tagged under 19 octets or AVTP under 15 (`KL_usbnet_pkg.sv:134`) can be removed and the harness still passes (`probe_tx_length_rule_removed` survives).
- **(c) LD3 EXTERNAL rule.**
  - The firmware rule at `sw/firmware/ctrl/plat/ctrl_plat_leds.h:119` is `kind == CTRL_PLAT_LEDS_EXTERNAL && domain_locked`.
  - With the domain lock dropped, `Leds.*` still passes 4 of 4 (`receipts/probe_fw_external.txt`).
  - No checked-in model has an EXTERNAL clock source.
- **Evidence.** `receipts/mutants_parallel.txt` for (a) and (b); the probe was planted, run and restored for (c).
- **Authority.**
  - `USB_NET_PATH.md:236-237` and `:241-242` claim "one per rule".
  - #1011 AC1 asks for a planted defect per filter class.
  - #1018 AC1: "Each rule has a planted defect".
- **Impact.** Breaking these rules goes undetected. A short frame's verdict could be decided by header octets left over from an earlier frame. An unlocked EXTERNAL source would light LD3.
- **Required outcome.** Each rule has a test and a planted defect: short RX and TX frames for each header shape, and an EXTERNAL source in the `Leds` fixture. Otherwise the rule is removed or publicly declared out of scope, and "one per rule" is made true.
- **Verification.** The three reviewer probes fail their named checks.

### F5 MINOR - Docs - `docs/design/REBOOT_RESET.md:104-107` - the authoritative REBOOT page describes the old toggle
- **The page says.** `MilanMAC` flips `ethtxend_tgl` "on the last octet of every frame at LiteEth's `phy.sink`".
- **At this head.** With `--usb-net`, `KL_usbnet_tx_arb` produces the toggle and leaves the computer's frames out of it (`sw/litex/milan_soc.py:1837-1841`, `USB_NET_PATH.md:110-115`). The REBOOT authority was not updated.
- **Impact.** A cold reader of the REBOOT account gets the toggle's source and meaning wrong for the Arty `--usb-net` image.
- **Required outcome.** REBOOT_RESET.md states the `--usb-net` variant or links to USB_NET_PATH.md section 3.
- **Verification.** The doc diff.

### R1 RESIDUE - Docs - `hdl/usbnet/KL_status_leds.sv:40` - port comment names the wrong reset domain
- **The defect.** The `clk_i` comment reads "the system clock, the MAC wrapper's". The block is instantiated on `ClockSignal("sys")` with `ResetSignal("sys")` (`sw/litex/usbnet_soc.py:169`), not in the MAC wrapper's `macsys` domain.
- **Exact fix.** `//! the SoC system clock`.

### S1 SUGGESTION - Conformance - #1011 AC1d disposition
- **The criterion.** AC1d asks that SR class A/B shaping be "unchanged in the existing harness" with injection at its rate limit.
- **Why that harness cannot carry injection.**
  - The product TX trunk has no CBS (`hdl/milan/milan_datapath.sv:826-842`).
  - None of the inputs of the stand-alone `cbs`, `shaper_core` or `queues` suites changed. They pass at the head (`receipts/shaper_suites_head.log`).
- **What does measure it.** The tap harness measures the bound that matters: the worst datapath wait is 2314 or 2337 clocks, against a bound of one injected frame.
- **Suggestion.** Record publicly that this mapping is how AC1d is satisfied, so the frozen criterion is not reinterpreted privately.

### S2 SUGGESTION - Robustness - `hdl/usbnet/KL_usbnet_tx_inject.sv:174-179`, `:241` - HOST and DETACH records can wait behind a stalled frame
- **The behaviour.** A FRAME header waiting for room in P_ROOM holds the HOST and DETACH records behind it.
- **When it shows.** With `inject_en_i` low (internal loopback), or with injection starved:
  - the bus stalls;
  - LD1's freshness lapses;
  - a DETACH is not seen.
- **Suggestion.** Document this, or let host records bypass waiting frames.

### Open scope (not graded as defects, per the #1011 rulings)
- The local path both ways (ruling 1) is not in this head.
- The station-record format is to follow the FX3 side's `docs/NETWORK.md` (amendment and ruling 3).
- The GPIF thread assignment (ruling 4) is undecided.
- Bench items #1011 AC3 and #1018 AC4 are not done.
- The #878 service census has not been re-run with the LED tick.

### Prior public findings
- No review round on PR #1020 published findings before this one.
- A concurrent external round started at the same head after this round began. Its first line appeared in a comment listing; its findings were not read before this verdict and ledger.

## What was checked in each lens

### Conformance (applied; UNCLEAN by F3)
Checked and found correct:
- **Stream subtypes.** The bit-7 stream rule matches IEEE 1722-2016 Table 6, with NTSCF, ESCF and EECF passing as control.
- **Link-local destinations.** The excluded 01-80-C2-00-00-0x block and the 2x block (ruling 2) are both implemented (`KL_usbnet_pkg.sv:92-127`).
- **TX drops.** Source not the computer's, link-local, stream subtype, two tags, priority above 1 (ruling 2) and length (`:131-144`).
- **Rate limit.** 10 Mb/s with a 3200-octet burst; each frame costs at least 60 octets plus 24 (`KL_usbnet_tx_inject.sv:312`). INC_C is exactly 1024 Q.16 at 80 MHz.
- **LED rules against the #1018 table.** The EXTERNAL extension is stated publicly.
- **LD3 over SET_CLOCK_SOURCE in all three cases.** `test_aecp.cpp` `Leds.*` sends AECP command 0x16 and checks the descriptor. It passes on `ax7101_1x1_tdm8` and on the three Arty models at the head (`receipts/firmware_leds_head.txt`).
- **ALINX identity.**
  - By construction: `usb_net_clk_hz is None` and `board == "arty"` guard every change in `milan_soc.py`, and `ctrl_plat_gen.py:162-163` emits `CTRL_PLAT_LEDS` only when the SoC's map has the row.
  - The author's identity receipts agree.
- **CSR map.** Rows are only added. The pinned page `n_locs - 5` is free, since the other pins are `-1` to `-4`.
- **Cost and timing.** +1221 LUT and +2 RAMB36 is inside the "~1-2k LUT, 1-2 BRAM" band, with every corner met (author receipts). The tap's FF count rises from 717 to 791, which equals the 74-bit input register of cc49123d. That supports the claim that the route carried this head's RTL.

### RTL (applied; UNCLEAN by F2)
Checked and found correct:
- **CDC.** Toggle plus synchroniser with ASYNC_REG on req, ack and end. The reset-less `tgl_r` follows CONTRIBUTING section 1.
- **Stream handshakes.** `valid` is never withdrawn at the arbiter.
- **Injection.** Gapless: the read looks one word ahead.
- **Sizing.** `out_r` (63) against the MAC's transmit CDC of 32 words, at most a few frames. Rollback, commit and room arithmetic in both buffers. Widths.

### Robustness (applied; UNCLEAN by F2)
Checked and found correct:
- unknown and wrong-length records are skipped;
- group and universally administered addresses are refused;
- a full buffer drops whole frames;
- the host-record timeout;
- `inject_en_i` low holds frames;
- a stalling MAC.

### Tests (applied; UNCLEAN by F1, F2, F3, F4)
- **Suites reproduced** (`receipts/usbnet_suite_head.log`):
  - the tap suite passes 9 cases (799973 b/s; worst waits 2314 and 2337 clocks);
  - the LED suite passes.
- **Planted defects.** 43 of 43 are caught by their named checks, re-run with an independent parallel driver (`scripts/run_mutants_parallel.py`, `receipts/mutants_parallel.txt`).
- **Firmware LED defect rows.** All 8 apply exactly once (`receipts/fw_led_rows_applicability.txt`). Their campaign was not re-run.
- **Shaper suites.** Pass at the head.

### Docs (applied; UNCLEAN by F1, F2, F3, F4, F5)
- **Checked against the RTL.** USB_NET_PATH.md and the DOCUMENTATION_AUDIT row.
- **Repository gates.** `docs_check.py`, `lint_rtl.py --check`, the SV, Python and C++ idiom gates and the port-contract gate all exit rc 0 (`receipts/gates_head_reviewer.txt`).
- **Em dashes.** No U+2014 in the added Markdown lines by direct search. The `check_em_dash.py` gate itself did NOT RUN, because the pinned renderer is not installed here.
- **Comment rule.** No lane label, round, reviewer or comment ID in the source comments of the delta.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | `KL_usbnet_pkg.sv`, `KL_usbnet_tx_inject.sv`, `KL_usbnet_rx_copy.sv`, `ctrl_plat_leds.h`, `test_aecp.cpp` Leds, `milan_soc.py`/`usbnet_soc.py`, #1011/#1018 AC and rulings, author route/CSR/identity receipts | R949-1 | cc49123d2db1e01e80859efa10f8da43a01344ef |
| RTL | UNCLEAN (F2) | `KL_usbnet_tx_arb.sv`, `KL_usbnet_tx_inject.sv`, `KL_usbnet_rx_copy.sv`, `KL_usbnet_tap.sv`, `KL_status_leds.sv`, `milan_soc.py` reset and transmit-path wiring | R949-1 | cc49123d2db1e01e80859efa10f8da43a01344ef |
| Robustness | UNCLEAN (F2) | the same RTL; `receipts/probe_arb_reset.log` | R949-1 | cc49123d2db1e01e80859efa10f8da43a01344ef |
| Tests | UNCLEAN (F1, F2, F3, F4) | `tb/verilator/usbnet/*`, `mutants.py`, `aecp_leds_mutants.py`, `suite_shards.py`, `suite_tally.py`; `receipts/*` | R949-1 | cc49123d2db1e01e80859efa10f8da43a01344ef |
| Docs | UNCLEAN (F1, F2, F3, F4, F5) | `USB_NET_PATH.md`, `REBOOT_RESET.md`, `DOCUMENTATION_AUDIT.md`, suite index, module headers | R949-1 | cc49123d2db1e01e80859efa10f8da43a01344ef |

## Real limits
- No full parent, PP, gPTP, Yosys, builder or Vivado bank was run, and no xvlog. No hardware was used.
- The physical calibration was NOT RUN.
- The firmware LED defect campaign (`aecp_mutants.py`) was not re-run. Only applicability was checked, plus the `Leds.*` runs and one probe.
- The Arty route evidence is the author's, at integration commit 660ed296, which is not public. Its source identity is supported only by the FF delta.
- The em-dash gate was NOT RUN.
- Hosted checks at the head were still running when this report was written: 1 success, 16 queued or in progress (`receipts/hosted_check_runs.tsv`). Skipped contexts are not results.

## Pending manager duties
- Hosted and act acceptance at the exact head.
- The current-dev merge-candidate build, from source base c34e7d8b against live dev e275d795, with the builder and native banks.
- Confirm that the Arty route's integration tree carries this head's `hdl/usbnet` and `sw/litex/usbnet_soc.py`.
- Decide the AC1d disposition (S1).
- Carry R1 to the residue checklist.
- Re-review after F1 to F5 are fixed. The F1 fix must keep every CI shard within budget.

## Repository state after the probes
- The only planted change in the clone was the firmware EXTERNAL probe. It was restored, and a stray ignored bytecode cache was removed.
- Every one of the 1998 tracked regular blobs re-hashes to its index id, with 0 mismatches. File modes, the index records and all 6 gitlinks equal their state before the probes. `git status --porcelain --ignored` is empty (`receipts/restore_check.txt`).

R949-1 FINISHED
