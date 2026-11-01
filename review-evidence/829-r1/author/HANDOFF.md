# A725b HANDOFF: gPTP plane on the MII port at 100 Mb/s (#829)

PRIVATE. Nothing pushed. `REPORT.md` holds the results and the one table; this file holds the state, the changes, the gates and what went wrong. Receipts: `receipts/INDEX.md`, generated from the files present.

## Status

| Item | State |
|---|---|
| TAKEN on #829 | posted, issuecomment-6558541888 |
| REVIEW READY on #829 | posted, issuecomment-6561285235 |
| `829-mii-gptp` | `4cda0aa03b11462f4f8750289f0999d5288b3546`, clean |
| `829-bench` | `7fa8332ead95330cf7c1c2eb97ed460e75082535`, clean, in worktree `$VALIDATION_STORAGE/829-a725/wt-bench`. The image and bench run are at `b474b534`; the one commit since touches two documents |
| a. Fault 3 | Closed: not a plane fault, see below |
| b. Accounting | Done: no logic error, 15 to 35 ns unexplained |
| c. Runtime correction | Done, on `829-bench` only |
| d. True pair | Done: Arty 894.8, zero 890.6, `PDELAY_NS` 888.2 |
| e. Tap compensation, sync, stream | Done: asCapable and sync for 10 min 40 s; stream passed |
| f. Tap-out check | **Owed, not run**: needs the owner |
| g. AX7101 route | Passes its record, rc 0; key off is the same netlist, see below |
| h. Bench left | On this image with the compensation written |
| i. Before and after | `REPORT.md`; `$VALIDATION_STORAGE/829-a725b/table.md` is its generated source |

## Correction: "sends no frame" was wrong

The #583 bring-up captured another link. The second tap, `<MAC-derived-interface-name>`, carries switch port 7's frames; the Arty's link is now on `<MAC-derived-interface-name>`. On the Arty's own link gPTP frames leave, and the fault was that none was timed. The issue's own correction comment already says this. `CHANGELOG.md` said "fell silent" and now says "timed no frame".

## Root cause, fault 1

Failing signal: `KL_gptp_gmii_launch.cand_r`. **First wrong cycle: seam cycle 7 of the first frame**, `chk_w` 0 on the delimiter check, because `phy.sink` holds each MII octet for two clocks and the observer read one octet per clock. The record never comes, the ledger never drains, the engine's response claim holds the next Pdelay_Req at the queue head, and the event queue fills.

Same bench, GMII timing: the delimiter is at cycle 7, the candidate holds, and every check passes. Receipts: `regression/first-wrong-mii.txt`, `regression/first-wrong-gmii.txt`.

Neither issue suspect in its stated form: the reset seal lifts on this image, and the observer's fault is a lost record, not a lost timestamp alone. The 80 MHz clock plays no part: `run-mii` passes at 80 MHz and at 100 MHz.

## Fault 2, the calibration, and fault 3

Fault 2 is `REPORT.md` section b: 1,509 ns of fixed distances, 1,174 ns of them digital and in the MAC's receive chain. No logic error.

Fault 3 is `REPORT.md` section a. Before 13:47 the MAC never received the follow-ups, so the plane had nothing to publish; after the re-plug every start measures. It does not need a link event, and link events did not cure it. **Why that link dropped those frames is unexplained**: no capture of it exists. The AX7101 runs the same plane and has no such fault to see.

**The board ran a scratch probe image up to 15:26.** "The same image" in the brief is A725's `probe3`, built from `wt-probe`, not the plain fix: its `GPTP_LAT` is a probe word and its peer delay clamp is removed. The two uncalibrated rows in the table are from it, and they say so.

## Changes on `829-mii-gptp`

| Commit | File:line | Reason |
|---|---|---|
| `d2112191` | `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv:363` | Count an octet where `valid` and `ready` coincide; on GMII `ready` is the constant 1 |
| | `KL_gptp_gmii_launch.sv:136`, `:206` | `ETH_CYC_PER_OCTET_P`, and the elaboration check that scales the expected distance by it |
| | `KL_gptp_txret.sv:105`, `:281` | The first-symbol term in the reconstruction: 3770 ns on MII, 426 ns on GMII |
| | `KL_gptp_txret.sv:287` | PHC history guard scales to the window, 203 cycles on MII |
| | `KL_gptp_shadow.sv:96`, `:1034`; `milan_datapath.sv:92`, `:8885` | Carry the shape; defaults are GMII |
| | `sw/litex/gen_mac_tx_model.py`, `tb/verilator/gptp_txts/` | Convert the MII stages and run the closed loop on them |
| `50642585` | `gen_mac_tx_model.py`, generated files | No trailing blank line in the new generated file |
| `3cc89f5f` | `sw/litex/milan_soc.py:1444`, `:1448`; `sw/builder/endstation_builder.py:5010` | One table states the shape per PHY model, and the builder reads it |
| `4cda0aa0` | `docs/design/GPTP_PLANE.md`, `CHANGELOG.md` | Correct the receive distances (1,164 ns was wrong, 1,110 ns at `core.source`, 1,174 ns at the stamp) and the fault's wording |

Constant at MII, per IEEE 802.1AS-2020 11.3.2 and 8.4.3: `(90 + 2 + 1) x 40 + 2 x 20 + 10` = **3770 ns**, onto the registered launch of frame octet 0's low nibble, the first symbol after the delimiter.

`dbg_busy_o` stays open at `milan_datapath.sv`. A725's diagnosis needed scratch probes, and publishing it costs logic on the AX7101 image, which the brief rules out.

## Changes on `829-bench`, carried to the #583 PR

`829-bench` is `d2112191`, `50642585`, the clock commit `eaed9b8d`, then `cde19ead` (`3cc89f5f` cherry-picked), then:

| Commit | Subject | Carries |
|---|---|---|
| `cb7129fb` | Let CSR 0x540 and 0x544 move the plane's latency corrections... | The key, the plumbing, the tests, the documents |
| `b9103d50` | Correct the MII receive distances... | `4cda0aa0` cherry-picked |
| `0a1928bd` | Calibrate the Arty's gPTP latency pair... (#583) | **The true calibration**: 1409/100 in `endstation_arty_current.yaml`, the term table in `GPTP_PLANE.md`, gate 36's sum for it |
| `55563149` | Name the pinned-ingress control... | Test name only |
| `b474b534` | Hold the writable corrections' flops in the datapath... | Moves the flops out of `milan_csr` |
| `7fa8332e` | Say what the writable key's off state leaves... | Two documents: an overstated line, and how far one link-up's sum can be trusted |

The manager's carry onto #583 should keep `0a1928bd` separate. `cb7129fb` and `b474b534` are one feature in two commits, because a rebase is not allowed here.

| File:line at `b474b534` | Reason |
|---|---|
| `hdl/milan/milan_datapath.sv:1714-1735` | One flop per direction under the key, written on the CSR block's AWREADY; constants otherwise; `GPTP_LAT` reads them |
| `hdl/common/csr/milan_csr.sv:1582`, `:2037` | Reset image of the two words is the build's pair under the key, zero otherwise. **Port list unchanged**, because `tb/verilator/csr` locks it to a frozen reference |
| `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:125`, `:400` | Ingress: the port under the key, the constant otherwise, into the same subtractor |
| `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:310`, `:639` | Egress: one registered net, 18 signed bits, so the 64-bit subtractor keeps a registered operand |
| `sw/builder/endstation_builder.py:4144`, `:4180`, `:4958`, `:5045` | The key, its refusal, the flag and the parameter, each absent when off |
| `sw/builder/endstation_builder.py:3536`, `:5396` | Out of the model hash and the overlay: it changes no descriptor |
| `sw/litex/milan_soc.py:999` | `p_GPTP_LAT_WRITABLE_P`, emitted only when asked |
| `configs/endstation_arty_current.yaml:227` | Key on, `current` only. `4x4` and `8ch` fit no device and keep their zeros |
| Documents | `REGISTER_MAP.md`, `GPTP_PLANE.md`, `REQUIREMENTS.md`, `TIME_SYNC.md`, `CLOCK_DOMAINS.md`, `DATAPLANE_WALKTHROUGH.md`, `ENDSTATION_BUILDER.md`, `BOARD_PORTING_AX7101.md`, `TESTING.md`, the suite README, `CHANGELOG.md` |

`REGISTER_MAP.md` has no generator beyond its contents list; `gen_toc.py --check` passes. No VERSION change, because a change there would move the AX7101 image.

## Regression tests

**The MII fix.** `make -C tb/verilator/gptp_txts run-mii`, control `mii_observer_ignores_ready`. Without the fix:

```
[FAIL] launch: an isolated exchange completes     (repeated)
RESULT: FAIL
make: *** [Makefile:89: run-mii] Error 1
```

With it: `== gptp_txts: checks: 89 failures: 0 ==`, `RESULT: PASS`, at 80 MHz and 100 MHz.

**The writable pair, both link shapes.** `make -C tb/verilator/gptp_txts run-latw`:

```
zero pair: ingress gap 0 ns, net 3770 ns, pad error +3 ns          (GMII: net 426 ns)
pair 777/333: t2 moved 777 ns, t3 moved 333 ns
pair 1409/100: t2 moved 1409 ns, t3 moved 100 ns
pair 1/65535: t2 moved 1 ns, t3 moved 65535 ns
pair 65535/1: t2 moved 65535 ns, t3 moved 1 ns
142 of the writes landed inside the stamps' interval               (GMII: 71)
checks: 921 failures: 0                                            (GMII: 495)
```

Four controls in `mutants.py` catch it: `latw_ingress_port_not_read`, `latw_egress_port_not_read`, `latw_egress_sign_reversed`, `latw_ingress_pinned_at_one_value`. `controls: 14 failures: 0`.

**The real CSR block.** `make -C tb/verilator/milan_dp gptp-latw`, 235 checks. With the wiring cut from the plane:

```
FAIL [T-LATW] the written ingress moves t2 by exactly it got 0000000000000128 exp 0000000000000309
FAIL [T-LATW] the written egress moves t3 by exactly it got 0000000000000068 exp 000000000000014d
...
235 checks: 227 PASS, 8 FAIL
```

That cut is a hand mutation at `0a1928bd`, not a committed control; it is in `regression/milan-dp-latw-wiring-cut-failing.txt`. The leg's own wiring did not change when the flops moved.

**Builder.** Gate 36a, `test_gptp_latency_writable_key`: off keeps the argv, on adds one flag, the model hash holds, a non-boolean is refused, and no AX7101 shape may state it.

## Gates

**On `829-mii-gptp` `4cda0aa0`:**

| Gate | Command | Result |
|---|---|---|
| Full sweep | `native-shards.py 829-a725b ... 4 0-11 12-23 24-35 36-47`, out `$VALIDATION_STORAGE/829-a725b/native-2` | **65 of 65 with shard 1 rerun as `shard-1b`**: shards 0, 2, 3 passed 15, 17 and 16; shard 1 failed 1 of 17, its rerun passed 17 of 17. 2,192,417 checks, 0 in-suite failures |
| rtl-fast bdd | `cd tests && behave` | rc 0, 508 scenarios, 2330 steps |
| Builder legs | `ci_builder_legs.py run 0` and `run 1`, `--require-rv32` | rc 0, rc 0, tree clean; `ALL GATES PASS EXCEPT 1 NOT RUN` |
| Lint | `lint_rtl.py --check` | rc 0, 89 at ratchet 89 |
| Documents | `docs_check.py`, `gen_toc.py --check`, `check_gptp_docs.py` | rc 0 each |
| Whitespace | `git diff --check` against the merge base | rc 0 |

A725's sweep on `3cc89f5f` finished 64 of 65 suites PASS. Its one failure was `gptp_shadow`'s `test_mutant_lifecycle.py`, `CLEANUP FAILED: owned descendants remain`, after the isolated SIGKILL case, while all 325 RTL checks and 9 controls passed. That is process cleanup under load, not RTL.

**The same test failed once in the final sweep too**, in `outer_cancellation`: `REFUSED: process ownership: CLEANUP FAILED: owned descendants remain`, at a host load near 100, with its 325 RTL checks and 9 controls passing. It passed in my cancelled sweep, in `shard-1b`, in a suite rerun, and in four repeats alone on this head and four on `dev` at load 10 to 30. This branch does not touch `scripts/owned_process.py` or the test. It failed in 2 of the 6 sweeps on this host that have run it, both on this branch, so a reviewer should know: I read it as a load-sensitive test with a 2 s grace, not as caused here, but I have not reproduced it on `dev`. `receipts/sweep/`.

**On `829-bench` `b474b534`:**

| Gate | Result |
|---|---|
| `csr` including both lockstep legs | rc 0 |
| `gptp_shadow`, `gptp_plane` | rc 0 each |
| `gptp_txts`, both shapes, writable, 14 controls | rc 0 |
| `milan_dp` `gptp`, `gptp-lat` | rc 0, 210 of 210 each |
| `milan_dp` `gptp-latw` | rc 0, 235 of 235 |
| Builder legs | rc 0, rc 0, tree clean; `ALL GATES PASS EXCEPT 1 NOT RUN`, a report not on this host's disk |
| Lint, `behave`, documents, whitespace, sweep shape | rc 0 at `b474b534`; documents and whitespace again at `7fa8332e` |

A full sweep has **not** run on `829-bench`.

## AX7101

**Route on `829-mii-gptp` `4cda0aa0`**, one 1x1 route by `PP_SHADOW_BASELINE_RECIPE.md`, `--single-thread-synthesis`, judged `--shipping-selection` against `route-1x1`. `pp_resource_gate.py` rc 0, route status complete.

| Figure | Record | Route | Delta | Verdict |
|---|---:|---:|---:|---|
| LUT | 52012 | 51994 | -18 | ok |
| FF | 53707 | 54101 | +394 | ok |
| Slice | 15780 | 15841 | +61 | ok |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 27 | 0 | ok |
| DSP | 13 | 13 | 0 | ok |
| WNS | +0.440 | +0.236 | -0.204 | ok, floor +0.030 |
| WHS | +0.036 | +0.036 | 0 | ok, floor 0 |

Corners: Slow +0.236 / +0.077, Fast +1.633 / +0.036. Slices are 15841 of 15850, 9 free, against 70 free on the record. **That is tight and worth a reviewer's look**: it is inside the gate's tolerance, but it is one placement. The record's baseline is an older dev, so this delta is not all this change's.

**Key off, on `829-bench` `b474b534`: the same netlist.** A second route of the AX7101 1x1, with all the writable RTL present and the key off:

- The argv and `.xdc` are identical, and the generated top `.v` is byte-identical apart from the order of a comment tree (`receipts/ax7101/top-compare.txt`).
- Every figure above is the same to the digit.
- All 126 implementation checksums in the two run logs match, ending `Ending Routing Task | Checksum: 200e845fc` (`receipts/ax7101/checksums.txt`).

So the shipping AX7101 image does not change through the key. No bench run on the AX7101: it is away.

## The final Arty image

`$WORKSPACE_HOME/litex-milan/work/build_arty_a725bcal2` at `b474b534`; keep it, as the installed build a later `flash-pair` must name. 52528 LUT (82.85%), 50312 FF, 15768 slices of 15850, 65 BRAM tiles, 13 DSP. Signoff corners: Slow +0.190 / +0.115, Fast +1.634 / +0.006. Bitstream sha256 in `receipts/build/artifacts-final.sha256`.

`build_arty_a725bcal1` (`0a1928bd`) was the first image: its rows are the `m-*` receipts. Safe to delete. A725's probe builds are safe to delete too.

## Exact commands

```sh
# one table row, under the bench lock it takes itself
POLL_PERIOD=5 $VALIDATION_STORAGE/829-a725b/tools/measure.sh <out> 70
# write the pair from math: true, or tap compensation on the true pair
flock -w 200 /tmp/milan-bench.lock python3 tools/setpair.py <row.json> true <transcript>
flock -w 200 /tmp/milan-bench.lock python3 tools/setpair.py <true-pair-row.json> tap <transcript>
# or by hand
flock -w 200 /tmp/milan-bench.lock python3 tools/lat.py <transcript> write 1409 581
# offset against the grandmaster, from one capture
python3 tools/offset.py <cap.pcap> <extra_egress_ns>
```

Tools are copied to `receipts/tools/`. Captures over 200 KB are in `$VALIDATION_STORAGE/829-a725b/large/`, recorded by hash in `receipts/LARGE-FILES.txt`.

## What went wrong

**I killed my own first sweep.** To stop my bench suites I ran `pgrep -f "suites[.]sh"` and killed the result, which also matched the four shards' `scripts/run_all_suites.sh`. All four were mine and no other lane's sweep was running, so nothing of anyone else's died. They had run about an hour. I relaunched as `native-2` on 12-CPU ranges, as only three 16-CPU ranges were free.

**My first design broke a frozen oracle.** The flops started inside `milan_csr` with two new output ports. `tb/verilator/csr/gen_lockstep.py` refuses any port list but the frozen reference's, and it refused it. Editing that gate would have weakened a test, so I moved the flops to the datapath, which needed a new image and a second run of the whole table. I found this only after the first image's bench run, because I had run `milan_dp` and `gptp_txts` and not `csr` first. The `m-*` receipts are from that first image and agree with the final one.

**Two `pkill -f` lines killed my own shell**, because the pattern matched the command itself. Nothing else was affected.

**Bench gates ran under the wrong interpreter first.** My `env.sh` picks a venv with no `pidfd`, so `gptp_shadow`'s lifecycle test refused; the same run in a `--shared` clone had the builder legs refuse on a submodule's origin. Reruns used the sweep's PATH and A725's worktree. All rc values above are from the reruns.

**The 829-bench worktree stayed A725's**: `$VALIDATION_STORAGE/829-a725/wt-bench`. I also moved `wt-gates` and `wt-dev` to other commits for routes, leaving them detached and clean.

## Not verified

- **Tap-out check**: true pair, near-zero peer delay, asCapable, sync. Needs the owner.
- **The true offset**: never measured under the true pair, since the tap breaks the bound.
- **The split**: assigned. The tap gives only the sum.
- **The 15 to 35 ns remainder**, and why the old link dropped follow-ups.
- **Cold power-on**: still none, on any image. Boots were flash configurations and console resets.
- **A full sweep on `829-bench`**.
- **Sustained streaming**: one connection of 57.6 s. No audio content was checked, only counters and frames.
- **Arty talker to peer listener**: not run. The one connection had the peer as talker, so no peer configuration changed.
- **Signoff hook for the Arty**: its corners are a report on the routed checkpoint, as in the bring-up. I/O timing is still unconstrained there.
