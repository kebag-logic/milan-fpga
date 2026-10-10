[R558] NEGATIVE - exact head 6de3904ec2d6b2f04325c94c7686519ecd92a202

# R558-6 - issue #696 / PR #706 - internal cleared-context review

- Head: `6de3904ec2d6b2f04325c94c7686519ecd92a202`, tree `4e0c5d5fc3bf69e7ebaf1c6d234bb144df658e43`.
- Source base: `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. The head already contains live dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (merge `941ba746`, tree `03143567`, plus the docs-only commit `6de3904e`).
- Review start: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097280603
- All five lenses were applied at this head: Conformance, RTL, Robustness, Tests, Docs.

## Verdict in one paragraph

The MAAP engine's #696 corrections are implemented as the rulings describe, and every committed check reproduces at this head.
- Unit: 172 checks, 0 failures. Real datapath: 3 checks, 0 failures.
- Campaign: 52 rows, 0 failures. The 50 planted defects fail their named checks, and both clean controls pass.
- Coverage: 215/215 lines. Firmware differential: 12/12 cases, and 17/17 defects caught.
- The six static and documentation gates I ran pass.

**One MINOR finding is open, so the verdict is NEGATIVE (R558-6-F1).** The first Begin! address draw takes the raw low 16 bits of the first-enable seed (`enable_seed_w[15:0]`, `KL_maap.sv:307-308`), with no generator step. Under identical timing and clock, I measured two cases at this head:
- Stations whose MACs differ only in bits 16..31 claim the **identical** first block, with the identical first probe interval.
- Adjacent MACs claim **overlapping** 8-address blocks: 0x1447 and 0x1448 in the committed datapath fixture itself.

That is the M4 symptom ("the station MAC never enters the draws") for the address draw, in the equal-timing scenario M4's acceptance uses. No committed check grades the first address draw. A plant that restores the pre-#696 first-draw expression `rand_offset(lfsr_next_w, …)` passes all 172 unit checks and all 3 datapath checks. The fix is small and needs LUTs only; it can also be closed by clause justification and a manager decision. Everything else is clean or is wording residue.

## 1. How the task was reconstructed (public state only)

1. `AGENTS.md`, `CONTRIBUTING.md` (verification bar, section 3), `docs/README.md`.
2. Issue #696, body: acceptance 1-4 and the M1-M8 table. Assignment and rulings in its comments:
   - assignment 6076750392;
   - rulings 6076940309 (M8: discard, no counter), 6079087547 (ceiling on `g_maap.maap_engine`, M6 reduce then decide), 6079463350 (differential consumer test), 6080332335 (documentation authority) and 6089712293 (merge dev, re-measure, no floor exception);
   - round-2 assignment 6093171536 (M5 loss/return contract).

   I also read the author's STOP and REVIEW READY posts.
3. Authorities:
   - MAAP design and behaviour: `docs/design/MAAP_FABRIC.md`, `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md`.
   - The C core the differential compares against: `sw/firmware/ctrl/maap/README.md` and `maap.c`.
   - The sibling engine's PortOperational!/Release! reading: `protocol-processor/docs/architecture/11_maap_engine.md`.
   - `REQUIREMENTS.md` (MAAP rows).
   - Area and records: `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `syn/ooc/pp_resource_baseline.json`.
   - Input digest and image inventory: `syn/ooc/pp_resource_gate.py`, `pp_baseline.py`.
4. `git diff 6aa25dec..6de3904e`: 119 files. Of these, the lane's own content is the 17 files whose blob differs from live dev `e8454e27` (`receipts/provenance.txt`). The rest is dev's #700, #701 and #702, carried by the merge. I read the full lane diff of `KL_maap.sv`, `milan_datapath.sv` (two ports and one comment), every harness, campaign and Makefile change, both firmware differential files and all eight documentation pages, plus the merge and `6de3904e`.
5. Public evidence: the `review-evidence/696-r1` tree at `97f433d6`, listed. It holds author receipts at earlier heads, up to `030eb98a` and its merge result. The manager's evidence comments, and the exact-head hosted check list (section 7).
6. Prior public review findings on this PR were read only after this round's own pass, its probes and its F1 evidence were complete (section 4).

**Scope derived from the acceptance.** M4 first, in RTL: seed at enable or MAC programming, plus a datapath check that two MACs draw different intervals, and a plant. Then M2, M7 and M8, with M8 discard-only by ruling. Then M1, M5, M6 and M3 within +60 LUT / +60 FF on `g_maap.maap_engine`. Every conformed item needs a suite check and a planted defect, or a clause justification in `MAAP_FABRIC.md`. The three endpoints are re-recorded through the recipe on the merge result, with no WNS floor exception. Acceptance 4 (bench interop) belongs to the post-merge bench lane. There is no register-map, filter or mailbox change.

## 2. Findings

### R558-6-F1 - MINOR - Conformance, RTL, Robustness, Tests - `hdl/ieee1722/maap/KL_maap.sv:306-308` (with `:146-149`, `:172`, `:352-355`); `tb/verilator/maap/sim_integration.cpp:129-141`; `tb/verilator/maap/sim_main.cpp:903-953` - the first Begin! address draw uses the raw low 16 seed bits and is graded by no check

- **Authority:**
  - Issue #696 M4 (B.3.4 NOTE, B.3.6.1) records the defect as: "every shipping station seeds `0xACE1` and the station MAC never enters the draws".
  - M3 (B.3.6.1) asks for a generator "seeded from the MAC and the real-time clock". B.3.6.1 is generate_address, the address-range draw.
  - Acceptance 1: "Each item is either conformed, with a suite check and a planted defect, or justified by clause in MAAP_FABRIC.md."
  - `KL_maap.md:5` states: "Randomness uses a 32-bit LFSR with period 2^32 - 1 (offset choice + interval draws). First enable samples the low 32 bits of the programmed MAC plus the local real-time clock."
  - Table B.7 note b judges a conflict by range overlap.
- **Evidence at this head:**
  - At first enable, `new_off_w = rand_offset(enable_seed_w[15:0], count_i)`, which folds the sum `mac[31:0] + clock` and uses only its low 16 bits (`:307-308`). The first probe re-arm then reads `lfsr_r[5:0]` of that same seed (`:172`, `:353`). No generator step separates the seed from either first draw.
  - Probe `scripts/first_draw_probe.cpp` (`receipts/first_draw_probe.log`) runs the head RTL with equal reset/enable timing and an equal clock:

    | MAC pair | First offsets | First probe intervals (cycles) | 8-address blocks |
    |---|---|---|---|
    | `02:00:00:00:00:01` / `02:00:00:00:00:02` | 0x0001 / 0x0002 | 5190 / 5200 | overlap |
    | `02:00:00:00:00:01` / `02:00:00:01:00:01` | 0x0001 / 0x0001 | 5190 / 5190 | identical |
    | `02:00:00:0a:12:34` / `02:00:00:5b:12:34` | 0x123b / 0x123b | 5770 / 5770 | identical |
    | `02:00:11:00:12:34` / `02:00:22:00:12:34` | 0x1234 / 0x1234 | 5700 / 5700 | identical |

  - The committed datapath fixture shows the same thing on the real CSR path. With the stations' first-PROBE `requested_start` printed and nothing else changed (`scripts/sim_integration_offsets.patch`, `scripts/p7_offset_check.sh`, `receipts/p7chk_head.log`), MACs `…:01` and `…:02` claim 0x1447 and 0x1448: overlapping blocks. The check at `sim_integration.cpp:140` passes because it compares interval vectors only.
  - The firmware C core, the differential's reference, steps its xorshift32 before its first draw (`sw/firmware/ctrl/maap/maap.c:31-54,108`). Adjacent seeds therefore do not give adjacent first offsets there.
  - Planted defect p7 (`scripts/p7_first_offset_ignores_seed.patch`) restores the pre-#696 first-draw expression `rand_offset(lfsr_next_w[15:0], count_i)`. Every station then claims the same first block (0x7c4f in the datapath fixture; 0xc73c in the probe). It **escapes** the unit harness (172 checks, 0 failures) and the real-datapath harness (3 checks, 0 failures) (`receipts/probes.log`, `receipts/p7chk_p7.log`). The M3 seed check (`sim_main.cpp:939`) grades `lfsr_r` after enable, not the address drawn at that enable.
- **Impact:**
  - In M4's own scenario (identical boot timing), the two cases in the table above both collide on their first claim, which is the failure M4 set out to remove. Stations whose MACs agree in their last two octets claim the identical block. Adjacent MACs, the normal case within one vendor batch, claim overlapping blocks. compare_MAC resolves the collision with an extra walk, but M4 and B.3.6.1 seed from the MAC precisely so that this first draw differs.
  - Any regression of the first-draw seeding, including a literal revert of the pre-#696 expression, is invisible to the suite. Acceptance 1 is met for intervals and generator state, not for the address draw.
- **Required outcome:**
  1. A suite check, unit or datapath, grades the first Begin! range across equally timed stations. At minimum, different MACs (and, separately, different clocks) must give different first offsets. A planted defect equivalent to p7 must fail that named check in the default campaign.
  2. Either the first offset (and preferably the first interval) depends on the full 32-bit seed, so that MAC pairs which differ only in bits 16..31, or are adjacent, do not claim identical or overlapping first blocks under equal timing; or `MAAP_FABRIC.md` justifies, by clause and with a manager decision, that the first draw is the seed's low 16 bits and records the collision cases above. Option 1 needs combinational mixing or a stepped generator value, so LUTs only: the FF allowance is fully used, and the LUT side has 54 left against `6aa25dec`.
- **Verification:**
  - Rerun `scripts/reviewer_probes.py` (p7 rows must become CAUGHT), `scripts/first_draw_probe.cpp` (no identical or overlapping pair, if option 1 is taken) and the default MAAP target (unit, datapath and campaign, all rc 0).
  - If the RTL changes: OOC MAAP area against the ceiling, and the endpoint records per the recipe or a manager decision.

### R558-6-R1 - RESIDUE - Docs - PR #706 body, "Status", "How to get into the same state" and the review-round table - stale head (carries R558-4-R1 forward)

- **Evidence:** the body still says "review ready at `f909d6c4…`" and `git rev-parse HEAD   # f909d6c460344527f102f24b8e7a77f09959e755`. The branch is now `6de3904e`, which adds `b9b38961`, `30073ee9`, the merge of live dev `e8454e27` (`941ba746`) and `6de3904e`. Its round table ends at round 2.
- **Why residue:** no figure, count, command or verdict in the body changes at this head. Unit 172, datapath 3 and campaign 52 rows all reproduce here.
- **Exact fix:**
  - Replace both `f909d6c460344527f102f24b8e7a77f09959e755` with `6de3904ec2d6b2f04325c94c7686519ecd92a202`.
  - Add rows for round 3 ("R558-3-F1 / R559-3-F1: the datapath derivations clear inherited make flags and pass the job bound explicitly; an empty list is refused | `b9b38961`, `30073ee9`") and for the composition ("merge of dev `e8454e27` (`941ba746`); R558-5-F1: the M0s step-1 status names #696's record as the comparison anchor | `6de3904e`").
- **Verification:** read the PR body.

### Suggestions (optional; no lens effect)

- **R558-6-S1 - Tests - `KL_maap.sv:241-252,449`.** Probe p6 replaces the own-count snapshot `{8'd0, tx_own_cnt_r}` with live `count_i`, and it escapes (172/0). The documentation says reconfiguration during a frame is not protected (`MAAP_FABRIC.md:71-72`), so no claim is broken. A one-line check would keep the snapshot from regressing silently.
- **R558-6-S2 - Docs - `MAAP_FABRIC.md:104-111`.** The fabric engine keeps walking, with `addr_valid_o` held, through a link outage (ruled contract). The C core withdraws on link loss (`maap.c:226-243`, `withdraw()` publishes invalid). The protocol-processor engine treats link loss as Release! (`11_maap_engine.md:103,135-147`). One sentence naming this difference would warn a later placement switch (M0s F2) that the observable `addr_valid` behaviour during an outage changes.

## 3. Results per lens

Each line names what was examined at this head and against what.

### Conformance - UNCLEAN (R558-6-F1)

```text
[R558] PASS Conformance (all items except F1's first-draw part) - KL_maap.sv:146-149,157,193-195,212-222,229,248-273,283-297,301-308,352-355,371-413,431-466; milan_datapath.sv:7168-7176 - checked against IEEE 1722-2016 Annex B as cited by issue #696 and its rulings
```

- **M1:** compare_MAC in rProbe!/PROBE and rDefend!/DEFEND (`:286-288`); TRUE = no action (note d).
- **M2:** the DEFEND echoes the PROBE's 16-bit requested_start/count (`:251-252`, `:408-409`); conflict_* = exact overlap (B.2.7/B.2.8).
- **M5:** a rising `port_operational_i` revokes and re-probes, without counting a conflict (`:157`, `:433-439`). Loss is no event, per ruling 6093171536.
- **M6:** one shared buffer. A PROBE parsed during PROBE/ANNOUNCE transmission is defended once the wire is free. Further PROBEs while the buffer is occupied are lost, as documented.
- **M7:** the supplied range is refused unless it fits [0, 0xFE00), the end inclusive at 0xFE00 (`:301-303`).
- **M8:** a frame is accepted only with every byte through conflict_count present, and keep strobes are honoured (`:193-195`, `:371`, `:393-394`). Counting was withdrawn by ruling.
- **M3:** the generator is a 32-bit maximal LFSR, seeded once from MAC + PHC.
- **M4:** the seed is taken at first enable, not in reset. **Open:** the first generate_address uses the raw low 16 seed bits (F1).
- **Documented by clause:** the pool-fold bias (B.3.6.1), the M6 capacity (Table B.7, B.3.6.6) and M8 counting (B.2).

### RTL - UNCLEAN (R558-6-F1: seed truncated to 16 bits into the first draw, `:307-308`)

```text
[R558] PASS RTL (except F1) - KL_maap.sv:135-480; milan_datapath.sv:2924-2960,3000-3001,7166-7190 - clock/reset, CDC, FSM, widths and contract checked against the datapath's synchronous-input contract and the module header
```

- **Clock and CDC:**
  - `port_operational_i` is `eff_link_w`, an axis-domain level already consumed synchronously by the counters and the processor (`milan_datapath.sv:3000,3589,8174`).
  - `realtime_ns_i` is `ptp_now_w[31:0]`. The datapath documents `gtx_clk == axis_clk` in every real instantiation (`:2934-2935`), so no new crossing is created.
- **Reset:** every new register resets (`:317-342`). After reset, `port_operational_r` = 0 can produce one rising pulse when the link is already up. It lands in IDLE, where it has no effect (it only clears an empty pending buffer).
- **FSM:** the default arm is retained. Priority: disable, then restart/PortOperational!, then sDefend, then the timer.
- **Widths:** the seed and range ends use 17-bit math (`:210-211`, `:301`).
- **TX path:** the frame builder selects the echo or own fields by message type. The own and echo snapshots are separate, so an ANNOUNCE on the wire cannot be rewritten by a buffered PROBE (`:248-252`, `:405-412`).
- **Area and timing:** the author's routed evidence gives +4.037 ns on the engine's worst incoming setup path. Not re-measured here.

### Robustness - UNCLEAN (R558-6-F1: identical or overlapping first blocks under equal timing)

```text
[R558] PASS Robustness (except F1) - KL_maap.sv:193-195,296-297,371,393-413,421,433-440; sim_main.cpp:384-404,464-497,705-803,826-872; reviewer probes p1-p5,p8,p9 (receipts/probes.log) - malformed/truncated input, boundary seeds, reset/disable/link-return during a pending response, backpressure at every beat
```

- **Truncation:** probe p1 (beat-5 keep accepts one byte) is caught.
- **Pending response:** p2 (link return keeps a stale DEFEND) and p3 (restart keeps it) are caught.
- **Seed range:** p4 (end of the supplied range unchecked) is caught.
- **Conflict counter:** p5 (link return counts a conflict) is caught.
- **Echo:** p8 (count echo truncated to 8 bits) is caught.
- **Seed bits:** p9 (seed from the MAC's high bits) is caught.
- **Outage:** a link outage longer than a walk leaves the walk running, and only the return restarts it (`m5_restart_on_link_loss` caught).
- **Open:** equally timed stations collide on the first claim (F1).

### Tests - UNCLEAN (R558-6-F1: the first-draw seeding is ungraded; p7 escapes both harnesses)

```text
[R558] PASS Tests (except F1) - tb/verilator/maap/{sim_main.cpp,sim_integration.cpp,mutants.py,Makefile,integration.mk}; sw/firmware/ctrl/test/{maap_differential.py,test_maap_differential.cpp} - re-executed at this head (receipts/unit.log 172/0, integration.log 3/0, mutants_par.log 52 rows 0 failures, coverage.log 215/215, differential_summary.log 12/12 + 17/17)
```

- Each committed plant fails its *named* check. The driver requires a successful build, rc 1 and the named `[FAIL]` line, and it never counts a compiler error.
- The M3 period proof learns the RTL's one-step linear map and checks its order against the prime factors of 2^32 - 1. That is a real proof, not a sample.
- The M8 comparison is cycle-matched against an idle RX tap.
- The M5 loss check outlasts a whole walk.
- **Escapes:** p6 escapes (S1, no claim affected). **p7 escapes both harnesses (F1).**

### Docs - CLEAN

```text
[R558] PASS Docs - MAAP_FABRIC.md:33-230; KL_maap.md:5,20-35; sw/firmware/ctrl/maap/README.md:186-195; AREA_BUDGET.md:10-170,345-376,404-462; MARK_II_AREA_PLAN.md:25-147,630-660; 234_PP_SHADOW_AREA_BASELINE.md:1-105; findings/README.md:25 - checked against pp_resource_baseline.json, the rulings and the RTL at this head
```

- **Figures against the record:**
  - All 22 rows of the Mark II current inventory (66 figures) equal the record's `scopes` (`receipts/check_mark2_inventory.log`, rc 0).
  - The route figures equal the record: 50,230 / 54,308 / 15,823 / +0.114 / +0.036.
  - The derived figures agree: 79.23 %, 12,190 over, 27 slices free, 10,683-LUT wrapper target, a 0.185 ns fall and 0.084 ns above the floor.
- **R558-5-F1 fix:** `6de3904e`'s two sentences (`AREA_BUDGET.md:368`, `MARK_II_AREA_PLAN.md:653-654`) match R558-5-F1's required text exactly.
- **MAAP behaviour pages:** they describe M1-M8 as implemented. Seeding, PortOperational!, the shared buffer and the M7/M8 contracts are consistent with `KL_maap.sv`.
- **Gates:** `docs_check`, `gen_toc --check` and `check_em_dash --base e8454e27` exit 0.
- **Residue only:** R558-6-R1, plus the retained items in section 4.

## 4. Prior public findings on this PR, at this head

| Finding | State at `6de3904e` | Evidence |
|---|---|---|
| R558-1-F1 (MINOR, Docs) | Resolved; still resolved | `MAAP_FABRIC.md:140-148` states 441/340 at `39571196` and 445/340 (+6/+60; lane +2/+60) at `0df48637` |
| R559-1-F1 (MINOR, Tests) | Resolved; still resolved | `sim_main.cpp:767-803`; `m5_restart_on_link_loss` caught (`receipts/mutants_par.log`) |
| R559-1-F2 (MINOR, Docs) | Resolved; still resolved | MARK_II inventory equals the record (66/66); gate row at `:56` |
| R559-1-F3 (MINOR, Docs, Tests) | Resolved; still resolved | `MAAP_FABRIC.md:227-228`; `sim_main.cpp:645-646` name `02:00:00:00:00:00`, clock 0 |
| R558-3-F1 = R559-3-F1 (BLOCKER, `integration.mk`) | Resolved; still resolved | `integration.mk` unchanged since `30073ee9`; the derivation passes here (`receipts/integration.log`, four datapath rows `[ok]`). Hosted shards at this head are still pending (section 7) |
| R558-5-F1 (MINOR, Docs, composition) | **Resolved at this head** | `6de3904e` applies the required text verbatim |
| R558-5-R1 (RESIDUE) | Retained | `AREA_BUDGET.md:359,376`, `MARK_II_AREA_PLAN.md:666` unchanged |
| R558-2-R1 / R559-2-R1 (RESIDUE) | Retained | `MARK_II_AREA_PLAN.md:66-67`, `:317` and the "current three-endpoint record" row (now `:1007`) unchanged |
| R558-4-R1 (RESIDUE, PR body head) | Retained, updated as R558-6-R1 | the body still names `f909d6c4` |
| R558-1-S1 | Applied | - |
| R559-1-S1..S4, R558-3-S1/S2, R559-3-S1, R558-4-S1/S2, R559-4-S1/S2 (SUGGESTION) | Retained, optional | sources unchanged |

None of the prior findings concerns the first-draw seeding. R558-6-F1 is new.

## 5. Executed evidence at this head

All runs were in a shared clone detached at `6de3904e`, with the three submodules at their gitlinks, using the pinned 5.050 simulator and its own coverage reader. Tracked bytes still equalled HEAD after every run (`receipts/provenance.txt`).

| Run | Result | Receipt |
|---|---|---|
| `make run` (unit) | 172 checks, 0 failures, rc 0 | `receipts/unit.log` |
| `make integration-build` + run | 3 checks, 0 failures, rc 0; intervals 5249/5290/5360 vs 5259/5550/5270; link return 4 PROBEs after 504 cycles | `receipts/integration.log` |
| `make coverage` | `KL_maap.sv` 215/215 lines, gate PASS, rc 0 | `receipts/coverage.log` |
| Campaign, the committed `MUTANTS` table and `run_case()`, run in parallel by `scripts/parallel_maap_mutants.py` | 52 rows, 0 failures: 2 controls pass, 50 plants fail their named checks, including the 3 datapath plants | `receipts/mutants_par.log` |
| `maap_differential.py --self-test` | 12/12 cases; 17/17 differential defects caught; rc 0 | `receipts/differential_summary.log` |
| Reviewer probes p1-p9 (`scripts/reviewer_probes.py`) | 7 caught; p6 and p7 (unit + datapath) escape | `receipts/probes.log` |
| First-PROBE `requested_start`, datapath, head vs p7 | head 0x1447 / 0x1448; p7 0x7c4f / 0x7c4f; both 3/0 | `receipts/p7chk_head.log`, `receipts/p7chk_p7.log` |
| First-draw probe, unit | table in F1 | `receipts/first_draw_probe.log` |
| `docs_check.py`; `gen_toc.py --check`; `check_em_dash.py --base e8454e27`; `measure_test_evidence.py --check`; `pp_resource_gate.py check-baseline`; `lint_rtl.py --check` | all rc 0 (lint 90 <= 90) | `receipts/static/*.log` |
| Mark II inventory against the record | 22 rows, 66 figures, 0 mismatches | `receipts/check_mark2_inventory.log` |

A first serial campaign attempt was stopped by me to rerun the same table in parallel. A first parallel attempt shared stdout between threads and produced an unreadable log. Its rc was 0, but it is not used. Neither is evidence; `receipts/serial_mutants_aborted.log` is kept for completeness.

## 6. Resource records (read, not re-measured)

- `pp_resource_baseline.json` records the three endpoints measured on merge result `0df48637`.
- `check-baseline` passes.
- Between `0df48637` and this head, nothing changed under `hdl/`, the submodule pins, `configs`, `constraints` or `sw/litex` (`receipts/provenance.txt`).
- Dev's `8b61b709..e8454e27` changes touch `sw/firmware/ctrl`, `syn/ooc` gate/recipe code, docs and one TDM8 harness. The shipping ROM links `sw/firmware/milan_baremetal` (`milan_soc.py:3991`), which neither depends on `ctrl/` nor changed.
- So, by inspection, this head's measured design inputs are those recorded. I did not rebuild or hash an image.
- The MAAP area (445 LUT / 340 FF, +6/+60 against `6aa25dec`, within the ruled ceiling) is the author's figure. I did not re-measure it.

## 7. Hosted evidence at this head (snapshot 2026-10-10T12:22Z)

- **Executed and passing:** `changes`, `full-ci-gate`, `bdd-conformance`.
- **Skipped:** `Physical gPTP (nightly and manual)`. That is a skipped context, not evidence.
- **Pending or queued:** all five Verilator shards, all four Yosys shards, `elaborate`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `firmware-unit`, `verilator-lint`, `yosys-elaboration`.

See `receipts/hosted_checks_snapshot.tsv`. The manager owns hosted and act acceptance.

## 8. Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R558-6-F1) | `KL_maap.sv` (all lane hunks), `milan_datapath.sv:7168-7176`, issue rulings, `maap.c`, `11_maap_engine.md` | R558-6 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| RTL | UNCLEAN (R558-6-F1) | `KL_maap.sv:135-480`, `milan_datapath.sv:2924-2960,3000-3001,7166-7190` | R558-6 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| Robustness | UNCLEAN (R558-6-F1) | malformed/boundary/reset/backpressure paths; probes p1-p5, p8, p9; first-draw probe | R558-6 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| Tests | UNCLEAN (R558-6-F1) | unit, datapath, campaign (52), coverage, differential; probes p6, p7 escape | R558-6 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| Docs | CLEAN (R558-6-R1 is residue) | `MAAP_FABRIC.md`, `KL_maap.md`, firmware MAAP README, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, `234_PP_SHADOW_AREA_BASELINE.md`, `findings/README.md`, record JSON | R558-6 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |

## 9. Real limits

- I have no copy of the IEEE 1722-2016 text. Clause readings rest on the issue, the rulings and the repository's own clause-cited pages. For the PortOperational! loss contract, those pages differ between the fabric (no event), the C core (withdraw) and the processor engine (Release!).
- No Vivado, route, OOC, parent suite bank, processor or gPTP bank, Yosys bank, field campaign or behaviour suite ran in this review. Their status at this head rests on the author's receipts at `0df48637` and the merge argument in section 6.
- Physical calibration was NOT RUN, and the hosted field/physical skips are not hardware proof. Acceptance 4 (bench interop) is not evidenced and belongs to the post-merge bench lane.
- The first-draw probe and the p7 offset print are reviewer harnesses, not committed suites. Their sources and patches are in `scripts/`.

## 10. Pending manager duties

- Decide R558-6-F1's outcome (RTL first-draw mixing plus a graded check, or a clause justification) and route it to the author. If RTL changes, the MAAP OOC ceiling check and the endpoint records follow under the recipe.
- Carry R558-6-R1 (it supersedes R558-4-R1), R558-5-R1 and R558-2-R1 / R559-2-R1 to the residue checklist.
- Hosted acceptance at the head once the pending shards finish, and the act replica.
- Build the current-dev merge candidate (builder and native banks) at the merge turn and link its receipts.
- Post-merge containment, and the bench lane for acceptance 4.
- No source bank was run by the manager at this exact head, and none is claimed here.

R558-6 FINISHED
