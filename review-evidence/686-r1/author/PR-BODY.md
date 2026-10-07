[A565]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Green. `686-maap-annexb` -> `dev` (base `e21c1ca0`), head `c7b69cd0fb2bdf980546ab413b3b82198267cbd8`.
Every local gate exits 0: the maap suite (120 checks) and its campaign (23/23 rows);
milan_dp 12,065, pp_shadow 2,184, capture_coherence 21,194, milan_dp_mclk 168 and
milan_dp_render 334 checks (36,088, 0 failures); the crflic leg (417 checks) and its
campaign (7/7); the ctrl suite with the differential (12/12, controls 16/16); lint,
the parser ratchet, docs and code-quality gates; Yosys OOC and portability; the
shipping route, both standalone endpoints, the resource gate and its re-record.

## Linked Issue / roles

Closes #686
Relates to #665, #687

Executor: `[A565]`
Internal cleared-context reviewer: `[R548]`
External reviewer: `[R549]`

## Description

The fabric MAAP engine `KL_maap` is the all-fabric shipping allocator. It followed
a reference implementation's bytes instead of IEEE 1722-2016 Annex B. This PR
conforms it on the four #686 items, grades each item against its clause with a
named check and a planted defect, and moves every consumer that pinned the old
behaviour. Ports, CSR fields, `state_o` encoding, the filter and the mailbox are
unchanged.

| # | Clause | Before (dev `e21c1ca0`) | After | Where |
|---|---|---|---|---|
| 1 | B.2.1 | `control_data_length` 28 in every frame; DEFEND to `91:E0:F0:00:FF:00` | 16 in every frame; DEFEND to the source MAC of the PROBE that caused it, latched when the DEFEND is requested | `KL_maap.sv:114`, `:227`, `:320-324`, `:372` |
| 2 | B.3.3 Table B.8, B.3.4.1, B.3.4.2 | probe 500..627 ms, announce 3000..5047 ms | probe draw 518..581 ms, announce draw 30488..31511 ms: strictly inside 500..600 ms and 30..32 s with margin for the tick phase and a frame in flight | `:120-125`, `:161-162` |
| 3 | B.3.2 Table B.7 notes b and d; B.2.5-B.2.8; B.3.6.4 | ANNOUNCE judged on its conflict_* fields (zero by B.2.7/B.2.8, so never a conflict); inclusive range ends; no compare_MAC | ANNOUNCE judged on requested_*; half-open overlap, an empty range never conflicts (one predicate for all three PDUs); rAnnounce! applies compare_MAC in DEFEND and yields in PROBE | `:187-210`, `:253-264` |
| 4 | Table B.7 ReserveAddress!/probetimer!/probeCount! | three PROBEs, the first one probe interval late; first ANNOUNCE 3 to 5 s after the third | four PROBEs, the first at once at Begin! and at every Restart!; the first ANNOUNCE at once after the fourth | `:119`, `:350-399` |

Two supporting changes keep the new reactions sound. Every per-frame field,
including the requested offset, is latched at the send (`:213-220`, `:237`),
so a Restart! taken while a frame waits on the wire cannot rewrite that frame.
The walk takes one decision per cycle in priority order: disable, Restart!,
sDefend, then the timer's own send (`:345-399`).

Tests and consumers:

- `tb/verilator/maap/sim_main.cpp`: re-pointed to the standard. Every check names
  its clause: golden Figure B.1 frames, the four-PROBE walk at Begin! and
  Restart!, the DEFEND destination under backpressure, every conflict cell with
  its note b range edges, a Restart! during an ANNOUNCE on the wire, and strict
  B.3.4 intervals over 150 walks and 24 announcements.
- `tb/verilator/maap/mutants.py` (new, in the suite's default target): 22
  planted defects, at least one per item, each required to fail its named check.
- `sw/firmware/ctrl/test/test_maap_differential.cpp` and `maap_differential.py`:
  the six #686 parent deltas become equalities with the Annex B core; the
  parent's frames now equal the core's for every shared stimulus.
- `tb/verilator/milan_dp/sim_crf_licence.cpp`: the crflic leg probed right after
  ANNOUNCE and silently relied on the processor's 100 ms DA retry round not
  landing in that window. It now probes while the claim is in flight, as Run B
  did, so the refusal is deterministic.
- `scripts/measure_test_evidence_readers.py`: the new campaign's DUT-source
  reader disposition.
- Docs: `docs/design/MAAP_FABRIC.md` now carries the clause-by-clause Annex B
  contract and the remaining deviations; FR-MAAP-01's ledger row, TESTING.md,
  the module page, the firmware MAAP README and two suite READMEs follow.
- `syn/ooc/pp_resource_baseline.json`: the three resource-gate records,
  re-recorded through the recipe; `docs/design/AREA_BUDGET.md`, the #234 findings
  header and the findings index name the new record.

Area and timing:

| Measurement | dev | this PR | Delta | Budget / floor |
|---|---|---|---|---|
| Yosys OOC `KL_maap` (`syn/yosys/ooc.sh`) | 637 LUT / 268 FF / 74 CARRY4 | 474 / 278 / 59 | -163 LUT / +10 FF | +40 / +40 |
| Vivado in context, `g_maap.maap_engine` | 479 / 267 ([649 resource map](../docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md), same `KL_maap.sv`) | 435 / 279 | -44 / +12 | +40 / +40 |
| Shipping route WNS / WHS | +0.108 / +0.036 ns (2026-10-05 record) | +0.317 / +0.036 ns | | floors +0.03 / 0 ns: met |
| Shipping route LUT / FF / slices | 50,318 / 54,214 / 15,789 | 50,088 / 54,188 / 15,843 | -230 / -26 / +54 | gate +500 / +600 / +80: PASS |
| Standalone ooc-1x1 / ooc-8x8 LUT | 23,178 / 29,853 | 23,178 / 29,853 | 0 / 0 | PASS |

The shipping route follows the recipe ("Integrated measurements", 1x1,
`ExtraPostPlacementOpt`): all 100,981 routable nets routed, no routing error,
TNS and THS 0. `pp_resource_gate.py check` passes on all three endpoints against
the previous record. The three records were re-written with `record --write`,
every tolerance, floor and ceiling unchanged, and `check-baseline` passes.
[AREA_BUDGET.md](../docs/design/AREA_BUDGET.md#protocol-processor-budget-and-resource-gate)
and the findings index now name this measurement as the gate's record.

## Authoritative references

- IEEE 1722-2016 Annex B: B.2.1, B.2.3, B.2.5 to B.2.8, B.3.2 with Table B.7
  (notes a, b and d), B.3.3 Table B.8, B.3.4.1, B.3.4.2, B.3.6.4, B.4 Tables B.9
  and B.10.
- [REQUIREMENTS.md section 1](../REQUIREMENTS.md#1-product-ownership): B.2.1
  DEFEND destination; both placements preserve wire behavior and normative
  timeouts.
- [FR-MAAP-01](../docs/reference/FR_NFR.md) and the
  [Annex B contract](../docs/design/MAAP_FABRIC.md#annex-b-contract).
- Assignment: issue #686 comment 6043036997; TAKEN 6043296747.

## How to get into the same state

```sh
git fetch origin
git checkout 686-maap-annexb      # head c7b69cd0fb2bdf980546ab413b3b82198267cbd8
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
export VERILATOR=<pinned Verilator 5.050>
export VERILATOR_JOBS=2
export TMPDIR=<disk-backed scratch>
```

## How to validate

```sh
make -C tb/verilator/maap                       # harness + mutants.py
make -C tb/verilator/maap coverage              # 95 % line gate
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
MILAN_RV32_CC=<verified SDK>/bin/riscv32-linux-gcc \
  python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
for s in milan_dp pp_shadow capture_coherence milan_dp_mclk milan_dp_render; do
  make -C tb/verilator/$s
done
make -C tb/verilator/milan_dp crflic-mutants
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check           # Vivado front end
bash syn/yosys/ooc.sh KL_maap
bash syn/yosys/run.sh --top KL_maap
python3 scripts/measure_test_evidence.py --check
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df
python3 scripts/gen_toc.py --check
python3 docs/traceability/gen_module_matrix.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
# Vivado: the recipe's route and standalone measurements, then
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101-ooc" --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax8x8-ooc" --endpoint ooc-8x8
```

Expected result / pass criteria: every command exits 0. The maap suite reports
`KL_maap: 120 checks, 0 failures` and `maap mutants: checks: 23   failures: 0`;
coverage is 100 % of `KL_maap.sv`; the differential passes 12 cases and its
self-test catches 16 of 16. The shipping route is the recipe in
[PP_SHADOW_BASELINE_RECIPE.md](../docs/testing/PP_SHADOW_BASELINE_RECIPE.md).

## Known limitations / out of scope

- Annex B deviations outside #686's four items are recorded, not changed, in
  the [Annex B contract](../docs/design/MAAP_FABRIC.md#annex-b-contract), for a
  follow-up decision: compare_MAC in the rProbe!/PROBE and rDefend!/DEFEND cells
  (Table B.7 note d); the DEFEND's requested_* echo (B.3.6.6); the
  generate_address generator and seed (B.3.6.1); no PortOperational! input
  (B.3.5.9); a PROBE parsed while a frame is on the wire is not defended.
- Acceptance 4, the MAAP exchange with the reference peer on the bench, is the
  manager's duty after merge. The new wire differs from the old in
  `control_data_length` 16, a unicast DEFEND and a 30 to 32 s announcement.
- Code comments in other suites that give the claim walk as "3 probes x ~500 ms"
  (`tb/verilator/milan_dp/sim_main.cpp:633`, `sim_nxn.cpp` seven copies,
  `tb/verilator/pp_shadow/Makefile:53` and `sim_main.cpp:1986`) and
  `hdl/milan/milan_datapath.sv:267,280` are unchanged: they state the claim's
  duration, still about 1.5 s to first order, and no check reads them.
- Slice headroom in the shipping image is now 7 of 15,850 (61 at the previous
  record), although LUTs and FFs both fell. This is a placement packing effect
  inside the gate's +80-slice tolerance. The image delta also spans dev
  `506d91db`..`e21c1ca0`, so it is not this change's alone. If dev moves before
  merge, the area budget's re-baseline rule applies to the merge result.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (1 to 3 here; 4 is the manager's bench duty after merge)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (every gate in the status, rc 0 at `c7b69cd0`)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
