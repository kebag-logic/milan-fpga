[R762] NEGATIVE - exact head 4cda0aa03b11462f4f8750289f0999d5288b3546

# R762-1: external review of issue #829 / PR #831

Tree `63924b8ce668a9e4e21cb0701a8586fb085551d9`. Delta against source base `1f29f189279f9fc0132f4918e47342b87d22f33a`.

**The logic is right; the delta is not ready to merge.** The root cause reproduces, the fix and the 3770 ns correction hold, GMII behaviour is unchanged, and the generated chain is the generator's own. Eight MINOR findings stay open under `RTL`, `Tests` and `Docs`:

- two required documentation-workflow gates are red because of this delta, and the first cancelled the hosted run;
- two wiring or boundary defects can pass the committed tests;
- one check cannot fail on MII, and another's name is false there;
- two published figures do not trace at this head;
- the delta states GMII `ready` is a constant that folds away, and it is a flop.

Two of the eight, F7 and F8, are prior findings of the internal review. My own pass missed both; I verified them and retain them below. `Conformance` and `Robustness` are covered clean.

## Findings

### R762-F1: MINOR: the documentation style gate is red at this head

- **Lenses:** Docs
- **Path:** `CHANGELOG.md:11,56,59,60,62,63`; `docs/design/GPTP_PLANE.md:276` to `:342` (22 findings)
- **Authority and evidence:** `.github/workflows/docs.yml:227` runs `scripts/check_doc_style.py`. It reports `documentation style: FAIL (28 findings)` at this head and `OK (23 current documents)` at the base: `receipts/check_doc_style_head.txt`, `receipts/check_doc_style_base.txt`. Hosted job `docs-gates-0` (job 124921223253, run 41331113507) failed on the same 28 findings. All four hosted runs then ended cancelled: `receipts/hosted_runs_at_review.txt`. The author's documentation row names `docs_check`, `gen_toc --check` and `check_gptp_docs`, not this gate.
- **Why this is not RESIDUE:** the fix is prose, but the defect changes a required gate's verdict and stops the hosted run.
- **Impact:** no exact-head hosted Verilator, Yosys or elaboration result exists, and none can until this is fixed.
- **Required outcome:** those lines meet the gate's limits, with their figures unchanged.
- **Verification:** `python3 scripts/check_doc_style.py` and `--selftest` rc 0, then the hosted `docs-gates-0` passes on the new head.

### R762-F2: MINOR: the C++ idiom gate is red behind F1

- **Lenses:** Tests
- **Path:** `tb/verilator/gptp_txts/Makefile:90`
- **Authority and evidence:** `.github/workflows/docs.yml:391` runs `scripts/check_cpp_idiom.py`, in the same job as F1, so F1's failure hides it on the hosted run. Locally it reports `FAIL: build without warnings 1 > ratchet 0`. The gate's own reader names this Makefile at head and finds nothing at base: `receipts/docgates/cpp_idiom_probe.txt`. The line is `-CFLAGS "-DGPTP_TXTS_MII"`, without `-Wall -Wextra`. `VFLAGS` does carry both, so this is the gate's line rule, not a lost compiler warning. Adding the two flags to that line clears the reader in the same probe.
- **Impact:** fixing F1 alone leaves the hosted job red at this later step.
- **Required outcome:** the gate passes with the ratchet at 0.
- **Verification:** `python3 scripts/check_cpp_idiom.py` rc 0.

### R762-F3: MINOR: the PHC-window arm does not reach the boundary it claims

- **Lenses:** Tests
- **Path:** `tb/verilator/gptp_txts/sim_main.cpp:941-942`, `:957`; `tb/verilator/gptp_txts/mutants.py` control `mii_history_guard_left_at_the_gmii_floor`
- **Authority and evidence:** AGENTS section 6, `Tests`: each test can fail for the defect it claims. The arm's comment says a load 1120 ns into the MII interval means "the guard has to cover the whole of the longer interval". It does not: that position needs only about 132 of the 188.5 fabric cycles. Probe in `receipts/guard/sweep.txt`:

| Guard, fabric cycles | Load at pad index 8 to 12 | Load at pad index 14 to 22, including the committed 22 |
|---|---|---|
| 203, this head | explicit loss | explicit loss |
| 188 | explicit loss | explicit loss |
| 170 | **published measurement, FAIL** | explicit loss, arm passes |

  So the RTL is correct at 203, and a guard short of the window can still pass the committed arm. The only committed control is the far-off floor of 64.
- **Impact:** a later cut of the guard that leaves about 370 ns of the window unguarded stays green. A frame launched across that PHC step gets a wrong time instead of an explicit loss.
- **Required outcome:** the suite refuses a guard shorter than the whole window on the MII shape, for example with a load at frame octet 0 and a control with the guard just under the interval.
- **Verification:** the suite passes at 203, and a mutant at 170 fails a named check.

### R762-F4: MINOR: no committed gate I could run holds the datapath's shape wiring

- **Lenses:** Tests
- **Path:** `hdl/milan/milan_datapath.sv:8885-8886`
- **Authority and evidence:** AGENTS section 6, `Tests`: real integration wiring is tested where practical. `gptp_txts` instantiates `KL_gptp_shadow` directly, `milan_dp` runs only the GMII default, and gate 1g reads only `milan_soc.py`: `receipts/wiring/references.txt`. I removed both bindings. These all stayed green: `check_port_contracts`, `check_rtl_source_lists`, `check_gptp_docs`, `check_soc_sources`, `check_sv_idiom`, `lint_rtl --check`, gates 1g, 1d and 1f, and `milan_dp gptp` 210 of 210: `receipts/wiring/gates_with_cut.txt`.
- **Limit of this evidence:** the full builder bank is outside this round. The reference search finds no other reader of those names.
- **Impact:** with that cut the Arty plane expects 45 cycles while its observer measures 90, and every frame is lost without a measurement. That is the same visible failure as this issue, and no test I ran catches it.
- **Required outcome:** a gate or an elaboration fails when either binding is cut.
- **Verification:** the same cut then fails a named check.

### R762-F5: MINOR: a check's name is false on the MII shape

- **Lenses:** Tests, Docs
- **Path:** `tb/verilator/gptp_txts/sim_main.cpp:859`; its anchors in `tb/verilator/gptp_txts/mutants.py:58,96,103,110,117`
- **Authority and evidence:** the check is named `bias: the mean error is within one nanosecond of zero`. On MII it passes at a mean of 1.350 ns and 1.335 ns against a limit of 1.754 ns: `receipts/gptp_txts_all.log` lines 111 and 118. The limit itself is justified and documented. The name is not, and it is the anchor four GMII controls and one MII control report.
- **Why this is not RESIDUE:** it is a test identifier, not prose.
- **Impact:** a cold reader of a passing log sees a statement its own mean contradicts.
- **Required outcome:** the name states the shape's actual limit, with the anchors updated.
- **Verification:** the suite and all controls pass under the new name.

### R762-F6: MINOR: two published figures do not trace at this head

- **Lenses:** Docs
- **Path:** issue #829 comment 6561285235; `review-evidence/829-r1/author/receipts/ax7101/checksums.txt`
- **Evidence for the controls:** the comment gives the commit as `4cda0aa0` and says "14 planted controls are caught". At this head `make -C tb/verilator/gptp_txts` runs **10**, all caught: `receipts/gptp_txts_all.log`. The 14 comes from the bench commit, whose extra four are the `latw_*` controls: `author/receipts/regression/txts-mutants-bench.txt` in the public evidence.
- **Evidence for the checksums:** "all 126 implementation checksums" has no public receipt. `checksums.txt` holds three lines per run, and the run logs are not published. The 126 also compares this head with the bench's key-off route, not with `dev` or the record.
- **Why this is not RESIDUE:** both are figures.
- **Impact:** the handoff attributes a measurement to a commit that did not produce it, and a cold reviewer cannot check the other.
- **Required outcome:** the public record states 10 at this head and 14 only for the bench. The checksum comparison is either published in full or stated as what the three published lines show.
- **Verification:** the corrected comment and a receipt.

### R762-F7: MINOR: GMII `ready` is a flop, not a constant that folds away (retains R761-F3)

- **Lenses:** RTL, Docs
- **Path:** `sw/litex/milan_soc.py:2085`, `docs/design/GPTP_PLANE.md:282`, `CHANGELOG.md:62`, `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv:362`, `sw/builder/test_builder.py:18266`, PR #831 change table
- **Authority and evidence:** LiteEth assigns `sink.ready.eq(1)` in `self.sync`: `receipts/prior/liteeth_gmii_tx.txt`. The converted GMII chain declares `reg phy_sink_ready1 = 1'd0`, sets it to 1 and clears it on reset: `receipts/prior/generated_gmii_ready.txt`. So the head observer takes a real flop on GMII, a connection the base does not have. Over a full GMII run `valid` was high without `ready` 0 times in over 100,000 valid clocks: `receipts/prior/gmii_ready_census.log`. Behaviour is safe; the statements are false.
- **Why this is not RESIDUE:** it is a claim about the shipping netlist, and it is the stated reason the AX7101 "cannot move". I cannot settle it as wording only.
- **Impact:** a reader takes the AX7101 netlist to be unchanged by construction. Nothing published shows that: no route of the base exists, and the 126 checksums compare this head with the bench.
- **Required outcome:** the text says `ready` is a flop that is 1 from the first clock after reset, under a reset the observer shares, so GMII holds no octet. "Cannot move" goes.
- **Verification:** read against the two receipts above.

### R762-F8: MINOR: the fragment refusal check cannot fail on MII (retains R761-F4)

- **Lenses:** Tests
- **Path:** `tb/verilator/gptp_txts/sim_main.cpp:926`
- **Authority and evidence:** the check is `records_[target].abort != 0 || records_[target].delta != 45`: `receipts/prior/fragment_arm.txt`. A whole MII frame measures 90, so `delta != 45` is always true on that shape. The control `delta_forced_not_measured` runs only on GMII: `receipts/gptp_txts_all.log`. I confirmed this by reading it and did not rerun the internal review's planted cut.
- **Impact:** `fragment: the observer refused it, by measurement` proves nothing on MII. The later result checks still catch a lost record.
- **Required outcome:** the expected distance scales with `kEthCycPerOctet`, and an MII control shows the check can fail.
- **Verification:** that control is caught on `run-mii`.

## Residue, wording only

| ID | Path | Exact fix |
|---|---|---|
| R762-R1 | `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv:150-151`, `sw/litex/milan_soc.py:2091-2092` | Say the observer's reset clears the LiteEth transmit side, and that `eth_rst` also clears the PHY stage on GMII but does not reach it on MII. `gen_mac_tx_model.py:253-255` already says so, and both lines sit outside the mirrored region, so the artifact does not go stale |
| R762-R2 | `docs/design/GPTP_PLANE.md:323`, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:91-93` | "No other link speed is qualified" reads as if 100 Mb/s were physically qualified. Say the digital bound covers these two shapes, and that 100 Mb/s physical calibration stays open under #583 |
| R762-R3 | PR #831 body, bench table | "650 to 654 ns" are row means. Add "range 631 to 675 ns", per `f-07`, `f-10`, `f-11` |
| R762-R4, retains R761 RES1 | `tb/verilator/gptp_txts/sim_main.cpp:14` | "At both system clocks that board has carried" is not this head's fact: all three Arty configs state 83.333 MHz (`receipts/prior/arty_sys_clock.txt`). Say "at 80 MHz and at 100 MHz" |

## Suggestions, each for its own Issue

- **R762-S1, Docs:** the receive range in `GPTP_PLANE.md:338` is true of its seven phases, and the author's script reproduces it exactly at this head: `receipts/rx_terms_author_script_at_head.txt`. 16 other random phases read 1179.3 ns, 1170.0 to 1190.5, and on GMII 213.8 ns, 203.0 to 225.3: `receipts/rx_distance_80mhz.txt`. Add a denser sweep or call the range a sample.
- **R762-S2, Conformance:** queued frames leave the MII pads 12 clocks apart, 480 ns: `receipts/mii_interframe_gap.txt`. 96 bit times at 100 Mb/s is 960 ns. LiteEth's gap inserter counts 12 cycles at `dw` 8, so this predates the delta and is unchanged by it.
- **R762-S3, Robustness:** `_PHY_MODEL_MIN_MBPS` allows 10 Mb/s on MII. `delta` is a clock count, so there the plane raises no abort and publishes a time wrong by about 33 us. The document states the limit, and by arithmetic the peer delay would leave the 800 ns bound. No such link was run. A runtime refusal would keep the "explicit loss" rule at that speed.
- **R762-S4, Tests:** make `scripts/owned_process.py:30-31`'s fixed 4 s cleanup deadline hold on a loaded host. See check 6 below.

## The seven requested checks

| # | Check | Result | Receipt |
|---|---|---|---|
| 1 | Root cause | **Reproduced independently.** With the observer reading one octet per clock, the seam at cycle 7 holds `0x55` with `nidx=7`, `chk=0`, `cand_w=0`, and `cand_r` falls on that edge. At the same cycle GMII holds `0xD5` and passes. With the fix, MII reaches index 7 at cycles 14 and 15 and holds | `receipts/rootcause/mii_fault.log`, `gmii.log`, `mii_fixed.log` |
| 1 | Regression | Without the fix `run-mii` fails first at `launch: an isolated exchange completes`, 38 failures of 62 checks. **Controls: 10 at this head, not 14** (F6), all caught | `receipts/gptp_txts_all.log` |
| 2 | GMII elaborated default | **Behaviour unchanged; netlist not shown unchanged.** The head observer with `ready` high and the head ledger are formally equivalent to the base's: 780 and 1548 equivalence cells proved, 0 unproven, and two controls show the proof can fail. `ready` is a flop (F7), never low with `valid` in a full GMII run | `receipts/equiv/`, `receipts/prior/gmii_ready_census.log` |
| 2 | Builder export | The builder's output is **byte-identical** at base and head on `endstation_ax7101_1x1_tdm8`, `endstation_ax7101_8x8` and `endstation_arty_current`. That output holds no SoC top. The top must differ by the new `i_gmii_tready_i` connection, by the diff at `milan_soc.py:2112`; the author's "byte-identical" compares this head with the bench | `receipts/export/compare.txt` |
| 2 | Routed 1x1 | Receipt read, not rerun: LUT 51994, FF 54101, slice 15841, WNS +0.236, WHS +0.036, `RESULT: PASS`. **126 does not trace** (F6). Slices are 15841 of 15850 | public `author/receipts/ax7101/gate-axhead.log` |
| 3 | Correction and bound | `(90+2+1) x 40 + 2 x 20 + 10` = 3720 + 50 = **3770 ns**. 3770 x 200 ppm = 0.754, published 0.76. 10 + 1 + 0.76 + 0.76 = 12.52, published 12.6. Guard 188 + 15 = 203. The pad oracle reads an error spread of -9 to +11 ns at both system clocks | `receipts/gptp_txts_all.log` |
| 3 | Receive distances | Stated figures reproduce: 1110 and 1174 (1167 to 1183) on MII, 141 and 215 (207 to 225) on GMII, from the author's script over seven phases. My own stimulus confirms `core.source` at 1110.5 on MII and reads 144.0 on GMII; see S1 for the range | `receipts/rx_terms_author_script_at_head.txt`, `receipts/rx_distance_80mhz.txt` |
| 4 | Generated chain | Re-conversion with the pinned stack is **byte-identical**, both shapes. A hand edit, a removed manifest and a mirrored-region edit are refused at both levels. A manifest edit and a generator edit are refused at the pinned level only, and the plain level's output names the weaker level. Migen and converted pad traces agree, 36 of 36 | `receipts/gen_check_pinned.txt`, `receipts/drift_probe.txt`, `receipts/test_gptp_tx_timestamp.log` |
| 4 | Other gates | Source list and port contract rc 0. Gates 1g, 1d and 1f hold, and 1d refuses a tied `ready` | `receipts/docgates/summary.txt`, `receipts/builder_gate_probe.txt` |
| 5 | Documents state what is shown | No Arty shipping claim. `configs/endstation_arty_current.yaml:253-254` still declares 0/0, as the document says. 10 Mb/s is excluded. One wording residue, R2. **"The 16 NOT RUN arms": I found no such statement.** The delta adds no `NOT RUN`, and the public receipts show only one builder arm per leg | `author/receipts/gates/builder-leg0.tail` |
| 6 | Lifecycle flake | See below | `receipts/flake/summary.txt` |
| 7 | Bench evidence | Every final-image row recomputes with 0 mismatches. Offset -234.9 and -231.5, mean -233; predicted about -237. The sweep adds to 2,192,417 over 65 suites. Stream 460,354 frames at 7999.8/s, no sequence break. Tap-out check not claimed. **Bench evidence only, no hardware run here** | `receipts/bench_recheck.txt` |

**Check 6, judged: the conclusion holds, but its stated basis was not enough.** "Passes at normal load" and "not reproduced on `dev`" did not test `dev` under load.

I ran 18 passes each of head and `dev` concurrently. In the first pass, taken at load 105 to 112, **`dev` failed too, 1 of 6, and head 4 of 6**, with the same `CLEANUP FAILED: owned descendants remain`, at the same call site. The 12 later passes per side, at load 73 and below, all passed. 4 of 6 against 1 of 6 does not separate them (p = 0.24).

The mechanism is a fixed 2 s + 2 s deadline, `scripts/owned_process.py:30-31`. The test's fixtures run a stand-in `make`. The delta changes none of the owned files: `receipts/final_clone_integrity.txt`. So this is a pre-existing load sensitivity and does not count against this PR. It stays a real defect in a required suite, hence S4.

## Clean lenses

```text
[R762] PASS Conformance — hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:280-283, docs/design/GPTP_PLANE.md:290-309, tb/verilator/gptp_txts/sim_main.cpp pad_nibble — acceptance items 1 and 2 reproduced; 3770 ns and the bound recomputed; the pad oracle finds frame octet 0's low nibble from the delimiter on the pads and grades the reference plane inside 11 ns at 80 and 100 MHz
[R762] PASS Robustness — receipts/guard/sweep.txt, tb/verilator/gptp_txts/sim_main.cpp fragment and recovery arms, receipts/gptp_txts_all.log — a PHC load from frame octet 0 onward is an explicit loss at guard 203; fragment and recovery arms pass on MII at both system clocks; by reading LiteEth's converter, a mid-octet MAC reset on MII leaves a stale nibble phase that shortens only the next preamble by one nibble and leaves delta intact
```

The `RTL`, `Tests` and `Docs` work that found nothing is not banked, because those lenses have open findings. For `RTL` it covered: transfer counting at `KL_gptp_gmii_launch.sv:333-410`, delta width (90 under saturation), guard width at `KL_gptp_txret.sv:284-304,471-498` (203 in 8 bits on all three 50 MHz Arty configs), the parameter path at `KL_gptp_shadow.sv:1033-1035` and `milan_datapath.sv:8885-8886`, and the unchanged crossing. For `Tests` and `Docs` it covered: the 10 controls; the migen trace comparison; `check_gptp_docs`, `docs_check`, `gen_toc`, `check_em_dash` and the other documentation gates in `receipts/docgates/summary.txt`; and the comment rule, for which `receipts/comment_rule_scan.txt` is empty: no new lane, round or reviewer label in the reviewed delta's non-document files.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #829 and its comments; `REQUIREMENTS.md:189`; `GPTP_PLANE.md:201-342`; `sim_main.cpp` oracle; `receipts/rootcause/`; `receipts/gptp_txts_all.log` | R762-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| RTL | **UNCLEAN**: F7 | `KL_gptp_gmii_launch.sv`, `KL_gptp_txret.sv`, `KL_gptp_shadow.sv`, `milan_datapath.sv`, `milan_soc.py`; `receipts/equiv/`; `receipts/prior/` | R762-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| Robustness | CLEAN | `receipts/guard/sweep.txt`; fragment, PHC and recovery arms; LiteEth `mii.py`, `gap.py`; `configs/endstation_arty_*.yaml` | R762-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| Tests | **UNCLEAN**: F2, F3, F4, F5, F8 | `tb/verilator/gptp_txts/`, `sw/litex/test_gptp_tx_timestamp.py`, `sw/builder/test_builder.py` gates 1d, 1f, 1g; `receipts/wiring/`; `receipts/flake/` | R762-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| Docs | **UNCLEAN**: F1, F5, F6, F7 | `CHANGELOG.md`, `GPTP_PLANE.md`, `CLOCK_DOMAINS.md`, `TESTING.md`, suite README, PR body, issue comments, public evidence; `receipts/docgates/` | R762-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |

## Prior public findings

The only prior public round at this head is the internal review, R761-1, comment 6561783035. I read it after my verdict and first ledger were written. That first ledger held `RTL` CLEAN. I changed it to UNCLEAN because I verified R761-F3 and my pass had missed it; the verdict was already NEGATIVE.

| R761 item | Disposition at this head | Here |
|---|---|---|
| F1, MAJOR, Docs and Tests | **Retained.** Independently found. I rated it MINOR under Docs alone and do not contest MAJOR, since it blocks merge either way. The internal review also records it under Tests | F1 |
| F2, MAJOR, Tests | **Retained.** Independently found. Same severity note | F2 |
| F3, MINOR, RTL and Docs | **Retained.** Missed by my pass; verified | F7 |
| F4, MINOR, Tests | **Retained.** Missed by my pass; verified by reading | F8 |
| F5, MINOR, Tests | **Retained.** Independently found | F3 |
| F6, MINOR, Docs | **Retained.** Independently found | F6 |
| F7, MINOR, Tests | **Retained.** Independently found. I also record it under Docs | F5 |
| RES1 | **Retained**, verified | R4 |
| S1, MII gap | Same observation | S2 |
| S2, lifecycle cause unknown | **Advanced:** I reproduced the failure on both head and `dev` at load 105 to 112, where R761's load of 43 to 53 did not. The exact trigger inside that deadline is still not traced | S4 |
| S3, clause citation | Same open point | Real limits |
| S4, command table | Consistent with my probe; its count of stale pins is not checked here | Real limits |
| S5, S6 | Not reproduced here, and neither changes my findings. Noted for the manager | None |

My F4, the datapath shape wiring, is new. The internal review ran gate 23m and it passed; that gate compares the SoC with the builder, so it does not read those bindings.

## Real limits

- **Not rerun:** no AX7101 route here, as this host has no router, so the route figures are the author's receipt. No route compares this head with current `dev`, and the record's baseline is older. So the routed effect of this PR alone on the AX7101 is unknown (F7), and with 9 slices free that is worth settling at the candidate.
- **Not run:** no hardware, no Docker or act, no full builder, PP, gPTP or Yosys bank.
- **Scope of the proofs:** the equivalence covers `KL_gptp_gmii_launch` with `ready` high and `KL_gptp_txret`, both at their defaults. `KL_gptp_shadow`'s change is parameter passing, read by eye.
- **Clause text:** the standards are not available here. The PR and the brief cite IEEE 802.1AS-2020 11.3.2 and 8.4.3 for the measurement plane, while the unchanged source headers cite 11.3.9. I checked the plane's behaviour against the first symbol after the delimiter, not the clause numbers. That discrepancy is unresolved.
- **Generator check level on hosted runs:** I did not trace whether the interpreter behind hosted `make -C tb/verilator/gptp_txts` carries the pinned stack. Without it, a generator-only edit passes that target's check, as `receipts/drift_probe.txt` shows for the plain level.
- **CI image inventory:** `scripts/ci_tool_inventory.py --check` refuses at both base and head on an older stale pin of `endstation_builder.py`, even before #787, so I could not tell whether the new `obj_mii` and `obj_pad_mii` build forms also need table entries: `receipts/inventory_probe_head.txt`, `receipts/inventory_probe_pre787.txt`. A search of the workflows finds no direct invocation of that check.
- **Bench:** the bench branch is local, so I could not confirm from public state that its image carries this head's logic. Bench counters are the author's. Mid-run `FRAMES_RX` readings lag `TIMESTAMP_VALID` and meet it only at the end. Nothing is claimed from those mid-run values and I did not explain them.
- **Evidence hashes:** the evidence index hashes differ from the published files for 88 entries and 28 captures are absent. The publication manifest records path redaction and `LARGE-FILES.txt` lists moved captures, so this is expected in kind. I did not reconcile each entry or check the captures.
- **Job limit exceeded:** at one point my concurrent suites, whose Verilator builds use `-j 0`, and 12 lifecycle repeats pushed the load average to about 112, above the 16-job allowance. That load is what produced check 6's first-pass failures. A probe run during it passed or failed on its own receipt, and no other result depends on load.
- **Clone state:** tracked bytes, modes, index and gitlinks verified, 1461 blobs re-hashed with 0 mismatches: `receipts/final_clone_integrity.txt`. Ignored build output remains in the clone.

## Pending manager duties

- Hosted and act acceptance, none of which has run to completion at this head because of F1. The current-`dev` candidate at the merge turn.
- Re-review after fixes: a change to the documents, the suite or the Makefile un-covers the matching lens, and an RTL change un-covers `RTL`.
- Carry R1 to R3 to the residue checklist. Open Issues for S1 to S4 as you judge.
- Physical calibration and the tap-out check remain NOT RUN and owed to the owner. PR #831 says "Relates to #829", so closing the issue stays a manual step.

R762-1 FINISHED
