[A153] REVIEW READY

Commit: page `e67a586f92506c8623079c341e4f56a9c5ae165a` on `500-d3-materialization-adr` (PR #503).

Heads:
- Evidence (never merged): `fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293` on `500-design-evidence`. The executed run is its ancestor `bf88b71f22d225ac3671317ab6cc720c41c76d4e`. The three commits after it change only `COMMAND_RESULTS.md`, adding its digest table and naming the commit that table was taken at (`git diff --stat bf88b71f fc2e3a62`: 1 file, 71 insertions).
- Examined base: dev `07294a76e833f1831d9fcbceb8123b8380c4ae76`, an ancestor of the page head.
- Pins in both checkouts: protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, third_party/verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. `external` is not initialized in the page checkout.
- Round-two reviews answered: R217-r2 and R218-r2, both NEGATIVE at `40d14d92bfcf3823ed7b227537630f444b1f4f73`.

## Changed

The page `docs/design/SAVED_STATE_MATERIALIZATION.md` changes in two commits over `40d14d92`: `229d6a7b` revises the design, and `e67a586f` adds the failure-dependency audit. Revision c does four things.

**1. Three proposed prerequisite seams** for stage 1 and every shippable stage:
- **S1, the port's terminal cause:** DEVICE or UNFRAMED on `KL_pp_nvm_port`.
- **S2, descriptor-memory response isolation:** a new guard, plus `desc_debt` on the roll-back.
- **S3, a bounded binding walk** in `KL_acmp_nvm_shadow`.

Each seam is prototyped on the evidence branch only. The amended pinned modules are renamed and generated from the pinned files by declared amendments that `run.py` checks. The tracked glue keeps the pinned modules.

**2. The restore transaction now covers every dependency:**
- the passes agree record by record;
- a failed rule or revert fetch aborts (cause 6) and is never a refusal;
- an unproven image ends CLOSED (cause 7);
- the roll-back holds the owners in reset while the memory owes a burst;
- a failed restore is never blank.

Section 8.8 audits each dependency once: the image walk, the binding walk, both D3 passes, the rule fetch, the state-bus write, the edit, judge and map faces, the roll-back and re-walk, late answers and the firmware.

**3. Availability.** Commands and the persistence device are separate contracts. Both walks are bounded, so AECP is served on defaults with restore fail set. An abandoned port read stays quarantined until the device ends it, for ever if it never does. No reuse is claimed. Issue 15 is neither closed nor amended.

**4. The format judge.** The product's own verdict, `sfv_supported_w`, is transcribed as the SHIPPING judge, with the three V1s cases under it. The synthetic judge and every case that relies on it are labelled.

On the evidence branch:
- **Prototypes:** a new guard; amended copies of the port and binding manager; the writer; the arbiter.
- **Harness and runner:**
  - the descriptor memory is modelled as an in-order FIFO;
  - new fault knobs;
  - 31 new cases, which replace revision b's W14 and W15 and bring the total from 67 to 96; W13 is also redefined;
  - 14 new mutants;
  - a mutant with several killers counts as killed only when all of them fail;
  - 8 process controls.
- **Other files:** 4 new OOC rows; reviewer probes; T1 to T4 revised; T8 rewritten; T9 new; README; command record.

## Validation

All evidence commands ran synchronously from EMPTY `$D3_OUT`, `$OOC_OUT` and `$PROBE_OUT`, with `TMPDIR` in a separate scratch directory. They were pinned to CPUs 96-127 and used one build pool with at most 8 jobs.

Tools: Verilator 5.052, gcc 16.2.1, sv2v v0.0.13, Yosys 0.66 (86f2ddebc), Python 3.14.7.

| Command (from `design-evidence/500-materialization/proposal-evidence`) | Exit | Result |
|---|---|---|
| `python3 -B run.py prep` | 0 | shapes 1x1 (53 records), 8x8 (156), synthetic 1x1r2 (53); amended prototypes checked against their pinned sources |
| `python3 -B run.py build <every fourth build, four commands> --pool 1 --jobs 8` | 0, 0, 0, 0 | 69 built: 3 base shapes, the tracked glue, 65 mutants |
| `python3 -B run.py run --pool 8` | 0 | `SUMMARY FULL builds 69, runs 312, checks 3462, verdict failures 0`; 65 of 65 mutants killed by every named check in completed runs; K15 premise reached at g3; M13 vacuity control as required; tracked glue: 7 must-fail fail, 4 must-pass pass |
| `python3 -B run.py controls --pool 8` | 0 | `CONTROLS 8, not as required 0`; the controls' own exits 1, 1, 1, 1, 1, 2, 1, 2 as required |
| `python3 -B ../reviewer-probes/r217_probes.py`, then `r217_check.py` | 0, 0 | `R217 PROBES: 9 runs, 0 not as demanded` |
| `python3 -B ../reviewer-probes/r218_probe_headers.py`, then `r218_check.py` | 0, 0 | `R218 PROBES: 6 runs, 0 not as demanded` |
| R217's own `check_probes.py` (at `7d9da877`) on the same results | 1 | `AssertionError` at its line 19, the first round-two counterexample assertion: the counterexample no longer holds |
| `ooc/run_ooc.sh` (inside `$OOC_OUT`) | 0 | 20 rows |
| `syn/yosys/ooc.sh KL_nvm_backend` (1x1, `N_NAME_P=30`, repository root) | 0 | 1030 LUT, 468 FF, 6 DSP, 114 CARRY4, the same as row `cal-backend-1x1-n30` |
| `python3 -B run.py receipts` | 0 | 59 digests, 44 evidence files and 15 repository inputs, 0 mismatches against immutable Git blobs (replacement objects disabled) |

The page gates were run on the committed head `e67a586f`, from the page checkout. Every one exited 0:

| Command | Exit | Verdict line |
|---|---|---|
| `python3 scripts/docs_check.py` | 0 | 0 findings across 163 md files + 826 scrubbed text files |
| `python3 scripts/check_doc_style.py` | 0 | OK (22 current documents) |
| `python3 scripts/check_doc_paths.py` | 0 | OK (822 cited paths) |
| `python3 scripts/gen_toc.py --check` | 0 | OK (105 pages) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | 144 cross-page fragment links reproduced |
| `python3 scripts/check_em_dash.py --base 07294a76e833f1831d9fcbceb8123b8380c4ae76` | 0 | 0 findings over 1765 added lines in 4 pages |
| `python3 scripts/check_hygiene.py --check` | 0 | PASS (705 files) |
| `python3 scripts/check_solution_docs.py` | 0 | OK |
| `python3 scripts/check_feature_status.py` | 0 | 0 findings |
| `python3 scripts/ci_scope.py --selftest` | 0 | PASS |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | up to date (69 modules) |
| `python3 scripts/measure_naming.py --check` | 0 | PASS (96 recorded) |
| `python3 scripts/measure_fail_fast.py --check` | 0 | PASS (82 <= 84, 4 <= 4, 0 <= 0) |
| `python3 scripts/measure_test_evidence.py --check` | 0 | PASS (75 <= 77, 10 <= 10, 0 <= 0, 3 <= 3) |

`git diff --check 07294a76..e67a586f` is clean. Both checkouts are clean at their heads.

## Acceptance criteria

Each of issue #500's five items is met in the page (section 16), pending independent review:
- who writes and where: section 4, candidate (b), with the seams;
- the trigger and the clear rule: sections 6 and 7;
- the restore: section 8, including the transaction, the dependency audit and the availability split;
- what must not persist: section 9;
- the stages: section 10, with S1 to S3, #501 and #502 as gates.

The six round-two findings are answered in `RESPONSE.md`: R217 R2-F1, R2-F2 and R2-F3; R218 F1, F6 and F7. Each keeps its reviewer's severity and lenses, and none is claimed cleared.

## Area

These are MEASURED out of context. They are estimates of prototypes, not bounds on an integrated implementation.

| Item | 1x1 | 8x8 |
|---|---|---|
| (b), the writer plus arbiter, worst mapping | 2,377 LUT, 888 FF | 3,116 LUT, 1,109 FF |
| S2, the guard | 5 LUT, 1 FF | 5 LUT, 1 FF |
| S1 increment, the amended port against the pinned one | +4 LUT, +2 FF | +4 LUT, +2 FF |
| S1 and S3 increment, the binding manager | +107 LUT, +34 FF | +103 LUT, +34 FF |
| Total with the seams | 2,493 LUT, 925 FF | 3,228 LUT, 1,146 FF |

The totals are 3.93 and 5.09 percent of the XC7A100T's LUT. None of these items uses BRAM or DSP.

The pinned port, the pinned binding manager and `KL_nvm_backend` are EXISTING hardware and are listed for scale only. The calibration still reproduces 1030 LUT, 468 FF, 6 DSP and 114 CARRY4.

## Model limits

The full list is in page section 14 and in the audit at the end of section 8.8.

*Build and time:*
- one process per build, one clock;
- a 1 MHz model clock, with DDR answering in 2 or 3 cycles;
- CPU instructions take no model time.

*Models and proxies:*
- The µCPU is a bus-functional model.
- The map plane is C++.
- The descriptor memory is an in-order FIFO.
- The edit face is a single staged set, where the product has phases 0 to 5.
- The model's reset map set is non-empty; the product's dynamic ports reset to empty.
- The rate proof uses the synthetic 1x1r2 configuration.
- The output-format ordering cases use the synthetic judge; they are labelled.

*Not modelled:*
- microprogram timing;
- the GET_AUDIO_MAP hold;
- real flash and placement;
- firmware change 2;
- the listener's preload backpressure (the binding deadline covers the read phase only);
- the product memory paths' CDC FIFOs, and `pp_desc_bridge`'s watchdog and poison.

No hardware ran.

## Open risks and questions

1. The live-write amendment (page 15 item 1) still needs the contract acceptance to record it.
2. S1 to S3 are proposals. T8 and T9 must be filed and accepted by the processor repository, and a stage-1 lane does not merge before they land.
3. #501 (stage 3) and #502 (every shippable stage) remain OPEN.
4. Live dev moved to `2d8fd62f` (the #498 merge). This revision was not rebased, and that commit is not in the local object store; it was not fetched. The manager's input check against it must cover the 15 inputs this record digests, including `hdl/milan/milan_datapath.sv`, which is new in revision c.
5. `RS_TMO_CYC_P` at the product clock (20 ms proposed) and all board timing are unmeasured.
6. The pinned descriptor store does not re-arm its watchdog after a response timeout (V23, T9). The failure is honest, and it is recorded, not changed.
7. Not run here:
   - the full native merge bar, `act` and the hosted contexts;
   - the extra focused gates R218 ran beyond the 14 listed above;
   - Vivado and placement.
