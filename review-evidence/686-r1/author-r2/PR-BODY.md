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

Round 2: `686-maap-annexb` -> `dev` (dev `291710b1` merged in), head
`48f12dc14099a3630a98eb07e9ec790695a72bfb`. Part A (`b2e786bb1`,
`359c42da7`, `30fce4b0a`) answers the R548-1 and R549-1 findings on
`c7b69cd0`. Part B merges dev with #682 (processor `2ad2f845`, baseline F) as
`e519e31f`. It re-records route-1x1, ooc-1x1 and ooc-8x8 on that merge
result through the recipe, with `--single-thread-synthesis` as F requires
(`48f12dc1`). See [Round 2](#round-2) under Description.
Every gate exits 0 at this head:

- The maap suite passes 130 checks, and its campaign 27 rows (26 planted defects caught). Coverage of `KL_maap.sv` is 100 % (169/169).
- milan_dp 12,065, pp_shadow 2,184, capture_coherence 21,194, milan_dp_mclk 168 and milan_dp_render 334 checks pass: 36,102, 0 failures.
- The crflic leg passes 417 checks, and its campaign 7/7.
- The ctrl suite passes with its RV32 arm. The differential passes 12/12, and its self-test catches 16/16 controls.
- Lint holds at 90 <= 90. The parser ratchet has 0 findings.
- Yosys OOC gives 515 / 278. Yosys portability passes.
- Test evidence passes `--check` and `--selftest`. The docs and code-quality gates pass, including the em-dash check against the dev tip.
- The shipping route and both standalone endpoints pass `pp_resource_gate.py check` against F. Their re-record passes `check-baseline`, and the gate's self-test and mutation campaign pass.

Round 1 head `c7b69cd0fb2bdf980546ab413b3b82198267cbd8`: every gate exited 0.
That covered the maap suite (120 checks) and its campaign (23/23 rows). It covered
milan_dp 12,065, pp_shadow 2,184, capture_coherence 21,194, milan_dp_mclk 168 and
milan_dp_render 334 checks (36,088, 0 failures), and the crflic leg (417 checks)
with its campaign (7/7). It covered the ctrl suite with the differential (12/12,
controls 16/16), lint, the parser ratchet, docs and code-quality gates, and Yosys
OOC and portability. It also covered the shipping route, both standalone
endpoints, the resource gate and its re-record.

## Linked Issue / roles

Closes #686
Relates to #665, #682, #687

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
| 1 | B.2.1 | `control_data_length` 28 in every frame; DEFEND to `91:E0:F0:00:FF:00` | 16 in every frame; DEFEND to the source MAC of the PROBE that caused it, latched when the DEFEND is requested | `KL_maap.sv:118`, `:240`, `:333-337`, `:385` |
| 2 | B.3.3 Table B.8, B.3.4.1, B.3.4.2 | probe 500..627 ms, announce 3000..5047 ms | probe draw 518..581 ms, announce draw 30488..31511 ms: strictly inside 500..600 ms and 30..32 s with margin for the tick phase and a frame in flight | `:124-129`, `:170-171` |
| 3 | B.3.2 Table B.7 notes b and d; B.2.5-B.2.8; B.3.6.4 | ANNOUNCE judged on its conflict_* fields (zero by B.2.7/B.2.8, so never a conflict); inclusive range ends; no compare_MAC | ANNOUNCE judged on requested_*; half-open overlap, an empty range never conflicts (one predicate for all three PDUs); rAnnounce! applies compare_MAC in DEFEND and yields in PROBE | `:196-219`, `:266-277` |
| 4 | Table B.7 ReserveAddress!/probetimer!/probeCount! | three PROBEs, the first one probe interval late; first ANNOUNCE 3 to 5 s after the third | four PROBEs, the first at once at Begin! and at every Restart!; the first ANNOUNCE at once after the fourth | `:123`, `:363-412` |

Two supporting changes keep the new reactions sound. Every per-frame field a
protocol event can change (message type, destination, requested offset,
conflict range) is latched at the send request (`:222-234`, `:250`). A
Restart! or a received PDU taken while a frame waits on the wire therefore
cannot rewrite that frame. requested_count and the source MAC follow `count_i`
and `station_mac_i`, and are not protected against reconfiguration during a
frame. The walk takes one decision per cycle in priority order: disable,
Restart!, sDefend, then the timer's own send (`:358-412`). Line numbers are at
the round 2 head.

Tests and consumers:

- `tb/verilator/maap/sim_main.cpp`: re-pointed to the standard. Every check names
  its clause: golden Figure B.1 frames, the four-PROBE walk at Begin! and
  Restart!, the DEFEND destination under backpressure, every conflict cell with
  its note b range edges, a Restart! during an ANNOUNCE on the wire, a
  conflicting PROBE parsed while an ANNOUNCE is part-way out, strict B.3.4
  intervals over 150 walks and 24 announcements, and random timer draws for a
  zero-seed station MAC. 130 checks.
- `tb/verilator/maap/mutants.py` (new, in the suite's default target): 26
  planted defects, at least one per item, each required to fail its named check.
  Defects that grade a supporting change carry item 0 and do not count toward
  the per-item guard.
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
  re-recorded through the recipe on the merge with current `dev`;
  `docs/design/AREA_BUDGET.md`, the #234 findings header and the findings index
  name the new record.

Area and timing (the dev column is baseline F, #682's record at dev `291710b1`,
except where noted):

| Measurement | dev | this PR | Delta | Budget / floor |
|---|---|---|---|---|
| Yosys OOC `KL_maap` (`syn/yosys/ooc.sh`) | 637 LUT / 268 FF / 74 CARRY4 | 515 / 278 / 59 | -122 LUT / +10 FF | +40 / +40 |
| Vivado in context, `g_maap.maap_engine` | 479 / 267 ([649 resource map](../docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md), same `KL_maap.sv`) | 429 / 279 | -50 / +12 | +40 / +40 |
| Shipping route WNS / WHS | +0.124 / +0.031 ns | +0.241 / +0.029 ns | +0.117 / -0.002 | floors +0.03 / 0 ns, fall 0.25 ns: met |
| Shipping route LUT / FF / slices | 49,957 / 54,274 / 15,734 | 50,391 / 54,263 / 15,788 | +434 / -11 / +54 | gate +500 / +600 / +80: PASS |
| Shipping route RAMB36 / RAMB18 / DSP | 74 / 27 / 14 | 74 / 27 / 14 | 0 | +0: PASS |
| Standalone ooc-1x1 / ooc-8x8 LUT | 23,179 / 30,135 | 23,179 / 30,135 | 0 / 0 | PASS (FF and storage identical too) |

The shipping route follows the recipe ("Integrated measurements", 1x1,
`ExtraPostPlacementOpt`, default seed, `synth.maxThreads 1`, `general.maxThreads
32`). All 100,934 routable nets are routed, with no routing error.
`pp_resource_gate.py check` passes all three endpoints against F. The records
were then rewritten with `record --write` and their `measured` notes updated,
every tolerance, floor and ceiling unchanged, and `check-baseline` passes. The
route's +434 LUTs are not in `KL_maap`, which fell, nor in the wrapper (-47).
The repository inputs differ from F's only in `KL_maap.sv` and comment lines of
`milan_datapath.sv`. The movement lies in blocks this change does not touch, a
flattening boundary in the gPTP shadow and tens of LUTs in `ts_counter`,
`crf_rx` and `csr`, which is optimization responding to the new inputs. Slice
headroom is 62 of 15,850 (116 under F). The worst setup path is 41 logic
levels inside the processor.

The zero-seed fix moved the Yosys figure from 474 to 515 LUT. About 20 of those
LUTs are abc mapping noise: the round 1 logic with only the seed routed through
the new wire maps to 496.

The raw recipe receipts of these records, and of round 1's, accompany the round
2 evidence as `resource-receipts/`. They hold the executed Tcl, the route and
standalone reports, an input manifest per endpoint, every
`pp_resource_gate.py` output, and the route status and timing summaries. A
script there regenerates each record from them and compares it with the
committed JSON: all six are equal.

### Round 2

R548-1 and R549-1 reviewed `c7b69cd0`, and both were NEGATIVE. The answers are
in `b2e786bb1`, `359c42da7` and `30fce4b0a` (Part A), then `e519e31f` and
`48f12dc1` (Part B, the merge with dev and the re-record):

| Finding | Change |
|---|---|
| R549-1-F1 = R548-1-F3 (MAJOR): a station MAC with `mac[15:0] ^ mac[31:16]` = `0xACE1` seeded the LFSR with zero, its fixed point, so both B.3.4 timer draws were constant | The reset seed takes `0xACE1` when the MAC seed is zero (`KL_maap.sv:141-149`, `:292`). Every other MAC keeps its seed. The LFSR step is invertible, so no state reaches zero. Bounds are unchanged. A new section requires a zero-seed MAC (`02:00:00:00:AC:E1`) to draw more than one distinct timer-to-timer probe and announce interval, each strictly inside its bounds. Two mutants restore the zero seed. |
| R548-1-F1: the in-flight guard on the DEFEND path was ungraded | A named check stalls an ANNOUNCE mid-frame under backpressure and injects a conflicting PROBE. The frame must leave byte-identical and no DEFEND may follow. The mutant `defend_rewrites_the_frame_on_the_wire` removes `!tx_busy_r` and is caught. No RTL change. |
| R548-1-F2: the undefended mid-frame PROBE deviation misread Table B.7 | MAAP_FABRIC now says PROBEs one to three are repeated, while a missed fourth PROBE is settled by the prober's ANNOUNCE and compare_MAC, which can move this station |
| R549-1-F2 = R548-1-F4: the all-fields snapshot claim | Restated in the banner, MAAP_FABRIC and this description: requested_count and the source MAC are live |
| R549-1-F3 = R548-1-F5: the unconditional pool claim | A random block is clipped to the pool. A supplied seed is used as given, not range-checked. Supplied-seed validation joins the follow-up deviation list. |
| R549-1-F4: no public receipts for the resource records | `resource-receipts/`, above: the records committed now (`48f12dc1`) and round 1's (`c7b69cd0`), each regenerated equal |
| R548-1-S1, S3, S4 | This station's empty range (`count_i` 0) gets a check and a mutant. Supporting-change mutants carry item 0. The stale `milan_datapath.sv` comments are refreshed. |

## Authoritative references

- IEEE 1722-2016 Annex B: B.2.1, B.2.3, B.2.5 to B.2.8, B.3.2 with Table B.7
  (notes a, b and d), B.3.3 Table B.8, B.3.4.1, B.3.4.2, B.3.6.4, B.4 Tables B.9
  and B.10.
- [REQUIREMENTS.md section 1](../REQUIREMENTS.md#1-product-ownership): B.2.1
  DEFEND destination; both placements preserve wire behavior and normative
  timeouts.
- [FR-MAAP-01](../docs/reference/FR_NFR.md) and the
  [Annex B contract](../docs/design/MAAP_FABRIC.md#annex-b-contract).
- Assignment: issue #686 comment 6043036997; TAKEN 6043296747. Round 2:
  comment 6047563934, answering PR #695 comments 6047555468 (R548-1) and
  6047415775 (R549-1).

## How to get into the same state

```sh
git fetch origin
git checkout 686-maap-annexb      # head 48f12dc14099a3630a98eb07e9ec790695a72bfb
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
python3 scripts/check_em_dash.py --base 291710b180ca9196780a6d17f2517957c9bcb89c
python3 scripts/gen_toc.py --check
python3 docs/traceability/gen_module_matrix.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
# Vivado: the recipe's route and standalone measurements, every one prepared
# with --single-thread-synthesis, then
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101-ooc" --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax8x8-ooc" --endpoint ooc-8x8
# The committed records from their receipts (R=<the resource-receipts/ directory>):
for e in route-1x1 ooc-1x1 ooc-8x8; do
  python3 "$R/scripts/regen_record.py" . "$R/r2-48f12dc1/$e" "$e" \
    --git 48f12dc14099a3630a98eb07e9ec790695a72bfb
  python3 "$R/scripts/regen_record.py" . "$R/r1-c7b69cd0/$e" "$e" \
    --git c7b69cd0fb2bdf980546ab413b3b82198267cbd8
done
```

Expected result / pass criteria: every command exits 0. The maap suite reports
`KL_maap: 130 checks, 0 failures` and `maap mutants: checks: 27   failures: 0`.
Coverage is 100 % of `KL_maap.sv`. The differential passes 12 cases, and its
self-test catches 16 of 16. Each regeneration prints `record EQUAL`. The
shipping route is the recipe in
[PP_SHADOW_BASELINE_RECIPE.md](../docs/testing/PP_SHADOW_BASELINE_RECIPE.md).

## Known limitations / out of scope

- Annex B deviations outside #686's four items are recorded, not changed, in
  the [Annex B contract](../docs/design/MAAP_FABRIC.md#annex-b-contract), for a
  follow-up decision: compare_MAC in the rProbe!/PROBE and rDefend!/DEFEND cells
  (Table B.7 note d); the DEFEND's requested_* echo (B.3.6.6); the
  generate_address generator and seed (B.3.6.1); no PortOperational! input
  (B.3.5.9); a PROBE parsed while a frame is on the wire is not defended (a
  missed fourth PROBE is then settled by the prober's ANNOUNCE and
  compare_MAC, which can move this station); tagged MAAP PDUs are not parsed;
  a supplied seed (`seed_offset_i`) is not validated against the Table B.9
  pool.
- A truncated MAAP PDU's acceptance gate (`rbeat_r >= 3'd5`) has no check. That
  is pre-existing and outside #686, and is a candidate for the same follow-up
  (R548-1-S2).
- Acceptance 4, the MAAP exchange with the reference peer on the bench, is the
  manager's duty after merge. The new wire differs from the old in
  `control_data_length` 16, a unicast DEFEND and a 30 to 32 s announcement.
- Code comments in other suites that give the claim walk as "3 probes x ~500 ms"
  (`tb/verilator/milan_dp/sim_main.cpp:633`, `sim_nxn.cpp` seven copies,
  `tb/verilator/pp_shadow/Makefile:53` and `sim_main.cpp:1986`) are unchanged.
  They state the claim's duration, still about 1.5 s to first order, and no
  check reads them. The two in `hdl/milan/milan_datapath.sv` are refreshed.
- Slice headroom in the shipping image is 62 of 15,850 (116 under F), and the
  route grew by 434 LUTs, under the gate's +500. The growth is outside
  `KL_maap` and the wrapper, in blocks this change does not touch. The records
  describe the merge with dev `291710b1`. Dev has since moved to `99e4eb6c`
  (PR #693, GMII RX capture placement: a LiteX patch and its constraints, no
  resource record). That changes the shipping export, so the area budget's
  re-baseline rule applies to the candidate merge result.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (1 to 3 here; 4 is the manager's bench duty after merge)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (every gate in the status, rc 0 at the round 2 head)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
