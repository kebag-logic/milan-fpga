# [A439] Lane C2 (MAAP) handoff: issues #66, #67, #68

Status: REVIEW READY at `b03d36f` (items 1 to 4 done; every processor gate and all 17 parent consumer commands rc 0)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `c2-maap-coverage`, base `main` c951a9ff0cb5851fb159d33e966e5a2a9a188fe3
- Head: `b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745` (not pushed; no PR opened)
- Assignment: issue #66 comment 5884446021
- TAKEN posted: issue #66 comment 5884454087
- REVIEW READY posted: issue #66 comment 5886227311 (head `b03d36f`), after a
  resumed session re-verified the clean tree, the head, the receipt checksums and
  that every parent gate log postdates the scratch gitlink move to `b03d36f`
- PR body for the new PR: `PR-BODY.md` beside this file

Commits (one-line subjects, no body, no trailers):

| Commit | Item | Subject |
|---|---|---|
| `15de8b5` | 1 (#66) | Drive the MAAP fit clamp and seed clamp, and clear the draw mark on a mid-draw Release! (#66) |
| `14b6caa` | 2 (#67) | Feed maap_version 0 and 2 PDUs through the real RX validator and the MP section (#67) |
| `3407c84` | 3 (#68) | Complete the MAAP Table B.7 conflict walk with MAC pairs that discriminate the reversed compare_MAC (#68) |
| `b03d36f` | 2 (#67), gate fix | Declare the rx_validator F28 version cases one per line for the parent's C++ rule 11 (#67) |

`b03d36f` exists because the parent's `check_cpp_idiom.py` (rule 11) counted
`const uint8_t versions[] = {2, 0, 31};` in the new F28 as a multi-declarator
declaration: 1 > ratchet 0 at `3407c84`, rc 1. At `b03d36f` it is rc 0, and the
parent's own `scan()` shows no rule-11 counter change against the base for any C++
file this lane touches. It is a separate commit because rebasing is not allowed.

Footprint: 25 files, +823/-56. The only RTL change is `hdl/maap/KL_pp_maap.sv` (+8/-1).
No port, parameter or interface change anywhere.

## Item 1: #66 MAAP fit clamp (IEEE 1722-2016 B.1, Table B.9; REQ-MAAP-001)

Commit `15de8b5`.

Tests (`tb/maap/sim_main.cpp`):
- **U17** reject arm, deterministic: `cfg_count_i` = 255 (the widest), fit limit
  `0xFE00 - 255 = 0xFD01`. A kind-7 stub in `tb/maap/maap_wrap.sv` (harness only,
  kinds 5/6 pass through) scripts `0xFDFF`, `0xFD02`, `0xFD01`. Asserts: three
  kind-7 draws consumed (the two overhangs redrawn), the claim is
  `91:E0:F0:00:FD:01`, the block ends at or below `91:E0:F0:00:FD:FF` (exactly
  at it), and the PROBE is byte-exact (count 255).
- **U17b** Release! (link loss) inside the redraw loop, at four consecutive
  cycles of its request/answer rhythm; each re-engage must reach its first PROBE
  (Table B.7 PortOperational! from INITIAL; B.3.5.9).
- **U18** seeded walk with `cfg_seed_offset_i = 0xFFFF` (> `0xFE00 - 8`): probes
  the clamped `0xFDF8` byte-exact, consumes no kind-7 draw (footnote a), claims
  the block, and grants the last source `91:E0:F0:00:FD:FF`.

RTL fix, found by U17b: `hdl/maap/KL_pp_maap.sv:569-577` (the `W_ADDR` engage-fall
exit) now clears `draw_act_r` (`:576`). Before the fix, an engage fall with a kind-7 draw
in flight left the mark set, the PRNG answer arrived in `W_OFF` unread, and the
next walk's `W_IVAL` waited forever, so no later PortOperational! reached
ReserveAddress! until reset. Clause: IEEE 1722-2016 Table B.7 (PortOperational!
in INITIAL: generate_address + ReserveAddress!) and B.3.5.9. Failing arm before
the fix: U17b phases 1, 2 and 3 plus U18 x3 behind the wedge, 6 FAIL of 89
(receipt `receipts/item1-u17b-before-fix.log`). After the fix, 90 of 90.

Mutants (`tb/maap/mutations/*.patch`, `make -C tb/maap mutants`):

| Arm | Defect | Result |
|---|---|---|
| `fit-compare-forced-true` | compare at `KL_pp_maap.sv:594` (the issue's `:587`, moved 7 lines by the fix) forced true | KILLED: U17 x4, 4 FAIL of 90 |
| `fit-compare-off-by-one` | `<=` to `<` | KILLED: U17 x3 + U17b x4, 7 FAIL of 89 |
| `seed-clamp-removed` | seed clamp (`:581-583`) removed | KILLED: U18 x4, 4 FAIL of 90 |
| `release-keeps-draw-mark` | the fix removed | KILLED: U17b x3 + U18 x3, 6 FAIL of 89 |

Campaign at `15de8b5`: control PASS, 4 of 4 KILLED (`5 checks: 5 PASS, 0 FAIL`).
The counts above are that commit's (90 checks); the head's are in the mutant table below.

## Item 2: #67 maap_version 0 and 2 through the RX validator (B.2, Tables B.1/B.10; REQ-MAAP-002)

Commit `14b6caa`. No RTL change: the validator and engine already accept any
maap_version (B.2.3.2 higher: interpret as ours; B.2.3.4 lower: interpret as that
version, whose fields v1 contains). Only the tests were missing.

Tests:
- `tb/rx_validator` **F28a/F28b/F28c**: MAAP PROBEs to `91:E0:F0:00:FF:00` with
  maap_version 2, 0 and 31 (31 sets all five bits of the lane). Each is accepted
  (no drop counter moves, one commit, one hdr beat, slot bytes exact),
  demuxed to `PP_PROTO_MAAP`, and `hdr_status_o` equals the received version;
  field-by-field hdr compare against the independent offset model. The builder
  `maap_pdu()` gains a `maap_version` argument (default 1). 393 to 453 checks.
- `tb/pp_top` **MP7**: after MP6, against the DEFEND-state claim, a conflicting
  maap_version-2 PROBE (and then a maap_version-0 PROBE) enters through the real
  validator, normalizer and dispatch; each is answered by a byte-exact unicast
  DEFEND (our version 1, echoed requested_*, B.3.6.6 overlap), the defend counter
  moves by one and the claim is kept. 7,751 to 7,755 checks at `14b6caa` (7,756 at
  the head, after item 3's MP4 premise check). New entry
  `make -C tb/pp_top maap-internal` (`--maap-internal-only`) runs the MP section
  alone (32 checks at `14b6caa`, 33 at the head) for the campaign.

Mutant `validator-maap-version-1-only` (adds `maap_version == 1` to the V8 drop in
`KL_pp_rx_validator.sv`): KILLED on both suites: rx_validator F28 x47, 47 FAIL
of 453; pp_top MP7 x4, 4 FAIL of 32 (33 at the head).

## Item 3: #68 Table B.7 conflict walk, discriminating compare_MAC (B.3.5.5-.7, Table B.7, B.3.6.4; REQ-MAAP-005)

Commit `3407c84`. No RTL change: the reversed compare and every cell were correct;
the tests could not tell a forward compare apart.

Disagreeing pairs against `tb/maap` OWN_MAC `02:AA:BB:CC:DD:EE` (reversed
`EE:DD:CC:BB:AA:02`), each with a premise CHECK (`only_reversed_lower`):
- `WIN_MAC` `00:11:22:33:44:FF`: forward-lower, reversed-higher. compare_MAC TRUE (we win);
  a forward compare says we lose.
- `LOSE_MAC` `F2:11:22:33:44:01`: forward-higher, reversed-lower. compare_MAC FALSE (we
  lose); a forward compare says we win.

| Cell | We win | We lose |
|---|---|---|
| PROBE / rProbe! | U9 (now `WIN_MAC`): walk unmoved, claims the contested range | **U19 (new)**: yields, re-address counted, fresh range, byte-exact PROBE |
| DEFEND / rAnnounce! | U7 (now `WIN_MAC`): claim stands | U8 (now `LOSE_MAC`): yield, 8 conflicts, fresh 4-probe walk |
| DEFEND / rDefend! | **U20 (new)**: claim stands, nothing sent | **U21 (new)**: yield, 8 conflicts, fresh range |

Also new: **U22** PROBE / rAnnounce! from a peer we beat in both orders
(`F2:FF:EE:DD:CC:FF`) still yields (no tie-break). One helper grades every new yield:
one re-address, the claim not valid, the next frame a byte-exact PROBE of a
different in-pool range. `tb/maap` 90 to 114 checks.

`tb/pp_top` MP4: the winner is now `F2:11:22:33:44:01` against OWN_MAC
`0A:0B:0C:0D:0E:0F`: reversed-lower (`01:44:…` < `0F:0E:…`) and forward-higher,
with a premise CHECK. MP section 32 to 33 checks.

Mutants (all KILLED):

| Arm | Suite | Named failures |
|---|---|---|
| `compare-mac-forward` (`cmp_mac_true_w = own_mac_i < rxm_sa_r`) | maap | U7, U8, U9 x2, U10, U19 x2, U20, U21: 9 FAIL of 112 |
| same | pp_top MP | MP4 x5: 5 FAIL of 33 |
| `probe-rprobe-never-yields` | maap | U19 x2: 2 of 114 |
| `defend-rdefend-ignored` | maap | U21 x4 + U22 x4: 8 of 112 |
| `defend-rdefend-no-tiebreak` | maap | U20 + U21: 2 of 114 |
| `probe-rannounce-tiebreak` | maap | U10 x3 + U22 x2: 5 of 114 |
| `yield-reuses-range` | maap | U8, U10, U15, U19, U21, U22: 6 of 114 |

`tb/maap/README.md` now carries the mutation ledger (all 13 arm runs) and the
campaign description, following the SRP suites' form.

## Item 4: parent-visible list

1. **No port, parameter or interface change.** `protocol_processor_top`, `KL_pp_maap`
   and `KL_pp_rx_validator` port lists are byte-identical to `c951a9ff`.
2. **One RTL behaviour change, dark in the parent.** `KL_pp_maap.sv:569-577` (the
   `W_ADDR` engage-fall exit clears the draw mark) acts only when
   `cfg_maap_internal_i = 1`. The parent ties it to `1'b0`
   (`hdl/milan/milan_datapath.sv:7695` at dev `13eda870`), so the shipping fabric
   does not change and no parent test needs a change for it.
3. **Parent test-evidence ratchet may be tightened (optional).**
   `scripts/measure_test_evidence.py --check` passes at the head with 74 <= 77 suites
   without a mutation arm and prints "can be lowered to 74". At the base pin
   `c951a9ff`, measured in a second scratch parent, it reports 75 <= 77 ("can be
   lowered to 75"). The one suite this lane arms is `tb/maap`, through its `mutants`
   driver (the inventory diff shows exactly that line). The driver is not an
   unexplained DUT-source reader (0 <= 0) and uses no host time (3 <= 3), so no
   `DUT_READER_DISPOSITIONS` row is needed. Lowering the budget is the pin-adoption
   lane's call.
4. **New processor entry points** a parent evidence inventory may pick up:
   `make -C tb/maap mutants` (the campaign, now also in the processor HDL workflow)
   and `make -C tb/pp_top maap-internal` (the MP section alone).
5. Nothing else. The parent's xvlog findings (4, all in files whose RTL this lane
   does not touch) are unchanged and within the ratchet.

## Suite table (processor, at head `b03d36f` unless stated)

| Entry point | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, **1,015,919 checks**, 0 failing (base `c951a9ff`: 1,015,815). Deltas: maap 75 to 114, rx_validator 393 to 453, pp_top 7,751 to 7,756 |
| `./scripts/lint_hdl.sh` | rc 0, 40 modules LINT OK |
| `make check` | rc 0 (lint 41 mermaid + 18 wavedrom, links 925, matrix 115 REQ / 17 GAP, modmatrix 92 rows 0 untested, params 24/24/24) |
| `python3 scripts/gen_matrix.py --check` | rc 0 (92 rows, 0 untested) |
| `git diff --check c951a9ff HEAD` | rc 0 |
| `make -C tb/maap mutants` | rc 0, `16 checks: 16 PASS, 0 FAIL` (3 controls + 13 arm runs KILLED) |
| `make -C tb/srp_top mutants` | at `3407c84`, in five `--only` batches (the full run exceeds one 10-minute foreground call): 56 of 56 KILLED, every control PASS, assertion coverage 49/49 computed over the batch logs. `b03d36f` changes no file the campaign copies |
| `make -C tb/nvm_port figures` | at `3407c84` (after `git fetch --no-tags origin refs/pull/13/head`, as CI does): rc 0, "all measured figures agree with the tree". `b03d36f` changes no file it reads |
| `./syn/yosys/run.sh` | at `3407c84`: rc 0, 36 YOSYS OK (including `KL_pp_maap`, `KL_pp_rx_validator`), no failure. `b03d36f` changes no HDL |
| `make -C tb/pp_top gsi-internal` / `name-writes` / `maap-internal` | rc 0: 6,182 / 85 / 33 checks, 0 failures |
| `make -C tb/pp_top` (both builds, fixture guards included) | rc 0 inside the sweep: 7,756 checks |

## Mutant table (`make -C tb/maap mutants`, head `b03d36f`)

| Arm | Item | Suite | Verdict | Named failures / suite checks |
|---|---|---|---|---|
| (control) | | maap / pp_top `maap-internal` / rx_validator | PASS | 114/0, 33/0, 453/0 |
| `fit-compare-forced-true` | #66 | maap | KILLED | U17 x4; 4 of 114 |
| `fit-compare-off-by-one` | #66 | maap | KILLED | U17 x3, U17b x4; 7 of 113 |
| `seed-clamp-removed` | #66 | maap | KILLED | U18 x4; 4 of 114 |
| `release-keeps-draw-mark` | #66 (the fix) | maap | KILLED | U17b x3, U18 x3, U19-U22 x16; 22 of 110 |
| `validator-maap-version-1-only` | #67 | rx_validator | KILLED | F28 x47; 47 of 453 |
| `validator-maap-version-1-only` | #67 | pp_top MP | KILLED | MP7 x4; 4 of 33 |
| `compare-mac-forward` | #68 | maap | KILLED | U7, U8, U9 x2, U10, U19 x2, U20, U21; 9 of 112 |
| `compare-mac-forward` | #68 | pp_top MP | KILLED | MP4 x5; 5 of 33 |
| `probe-rprobe-never-yields` | #68 | maap | KILLED | U19 x2; 2 of 114 |
| `defend-rdefend-ignored` | #68 | maap | KILLED | U21 x4, U22 x4; 8 of 112 |
| `defend-rdefend-no-tiebreak` | #68 | maap | KILLED | U20, U21; 2 of 114 |
| `probe-rannounce-tiebreak` | #68 | maap | KILLED | U10 x3, U22 x2; 5 of 114 |
| `yield-reuses-range` | #68 | maap | KILLED | U8, U10, U15, U19, U21, U22; 6 of 114 |

## Parent consumer gate table

Scratch parent: `$VALIDATION_STORAGE/ppC2-a439-parent` = `git archive` of the trusted
checkout at milan-fpga dev `13eda870d1a6`, committed into a scratch repository.
Submodules are real checkouts registered as gitlinks: `protocol-processor` cloned
from this lane's tree at `b03d36f` (the gitlink is `b03d36f`), `gptp-processor` at
`5dce647`, `third_party/verilog-axis` at `48ff7a7`, and `external` left
uninitialised (SSH-only, read by no gate). The trusted checkout was not modified.

**Which 16 commands.** The manager's exact 16-command list is not in any source I
may read. I reconstructed it:
- The #606 pin-adoption lane's evidence (milan-fpga PR #609 comment 5881540622)
  names 11: `sw/builder/test_builder.py --require-elaboration --require-rv32`,
  `make -C tb/verilator/pp_shadow`, and nine scripts.
- The manager's PR #132 bank (processor comment 5880274287) adds `nvm_cosim` lint
  and quick, `milan_dp` and `milan_dp_render`, which makes 15.
- For the sixteenth I ran both plausible candidates: the processor's own
  `check-integrator-params.py` from the parent (the check `docs/reference/SUBMODULES.md`
  documents) and `scripts/lint_rtl.py --check`.

17 commands, each started in the foreground. Two outran the 10-minute tool limit
(`test_builder.py`, `milan_dp`), were moved to the background automatically, and
were awaited to completion; their rc is their own.

| # | Command (from the scratch parent root) | rc | Result |
|---|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet at or under budget; multi-declarator 0 <= 0 (was 1 > 0 at `3407c84`, fixed by `b03d36f`) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | all ratchets within budget |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet, all pre-existing in files whose RTL this lane does not touch |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK, 106 files, 4/4 consumer lists; processor 35/41 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 6 | `python3 scripts/check_port_contracts.py` | 0 | OK, processor 111 <= 111 undocumented |
| 7 | `python3 scripts/measure_naming.py --check` | 0 | PASS, 96 recorded |
| 8 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 74 <= 77 unarmed suites ("can be lowered to 74"), 10 <= 10 unseeded, 0 <= 0 unexplained readers, 3 <= 3 wall-clock. Base pin `c951a9ff` in a second scratch parent: rc 0, 75 <= 77; the only inventory difference is `tb/maap` armed by `mutants.py` |
| 9 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 10 | `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 (placement calibration), whose build report is absent on this host, the same arm the #606 lane recorded as NOT RUN. 15m53s, moved to the background by the 10-minute tool limit and awaited |
| 11 | `make -C tb/verilator/pp_shadow` | 0 | 4 legs PASS: 595 + 595 + 635 + 295 = 2,120 checks, 0 failures, no PINMISSING |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 | 84 warnings, none fatal |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 14 | `make -C tb/verilator/milan_dp` | 0 | 27m31s, moved to the background by the 10-minute tool limit and awaited. Every leg PASS, 0 RESULT: FAIL: gptp 181/181, gptp-lat 181/181, gmstep 103/103, main 234, notify 381, crflic 415, nxn 1,844, nxndv 1,846, nxn8 3,524, nxn4c 1,844, nolpf 234, prune 33, ax1x1 231, aclk 190; `render_mutants.py` 6/6 and `gmstep_mutants.py` 6/6 |
| 15 | `make -C tb/verilator/milan_dp_render` | 0 | tdm8_render 152/152 and 65/65, `--leg-defects` 5/5 |
| 16a | `python3 protocol-processor/scripts/check-integrator-params.py` | 0 | top 24, guide 24, diagram 24, OK |
| 16b | `python3 scripts/lint_rtl.py --check` | 0 | PASS, 90 <= 90 |

## What remains, and observations not acted on

- **Manager's bank.** The official 16-command consumer bank, hosted CI at the head,
  and the two independent reviews ([R400], [R401]). The branch is not pushed and no
  PR is opened; `PR-BODY.md` is ready for it.
- **Observation A (reasoned from the source, not driven, not changed).** The
  `W_ADDR` engage-fall exit fixed here does not re-arm the footnote-a seed
  (`seed_used_r`), which `docs/architecture/11_maap_engine.md` §6 says Release! does. It is reachable only when a
  Release! lands while generate_address runs after the seed was already consumed
  (a Restart! following a seeded walk). The next engage then draws a random range
  instead of re-probing the seed. That is benign under footnote a ("may ... attempt
  to reuse") but disagrees with the engine document.
- **Observation B (reasoned from the source, not driven, not changed).** `W_IVAL` and
  the TX states do not test `eng_w`. An engage fall while a PROBE or ANNOUNCE is
  being drawn or built still lets that frame leave before the teardown, a window of
  one draw plus about 70 cycles. Footnote c says Release! sends no PDU. On a link
  loss the MAC does not transmit anyway; on a `cfg_maap_internal_i` fall it could.
  Neither observation is in #66-#68's acceptance; each would need its own issue,
  test and fix.
- `docs/00_MILAN_COMPLIANCE_REVIEW.md` is unchanged: the REQ-MAAP-001/002/005 rows
  already name the right Ver categories, and GAP-04's residue column points at #78,
  not at these issues.

## Receipts

`receipts/` beside this file (logs under 200 KB). Larger scratch logs stay in
`$VALIDATION_STORAGE/ppC2-a439/` and are listed with size and sha256 in
`receipts/SHA256SUMS`.
