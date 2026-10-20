[A657]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Green locally at `4605409b`, review ready; `765-unsupported-format` -> `dev` (stacked on PR #767; it merges after #767). Full sweep: 63/63 suites, 2,187,728 checks, 0 failures. tsn_fuzz: AAF/AVTP 164/0 and gPTP 677/0. Mutant drivers: `format_mutants.py` 6/6, `lockstep_mutants.py` 14/14, crf_rx `mutants.py` 21/21, `unb-mutants` 6/6. Yosys 58/58. route-1x1 fully routed (WNS +0.137 ns, WHS +0.024 ns), and the resource gate passes (LUT +244 over the record, tolerance 500).

## Linked Issue / roles

Closes #765
Relates to #767

Executor: `[A657]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

A PDU whose format differs from its Stream Input's current format now counts UNSUPPORTED_FORMAT and is discarded (Milan v1.2 Table 5.6 with Table 5.16, 4.4.2.2). This closes two gaps:

| Piece | Change |
|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:501,508,512-528` (AAF inputs) | the compare adds the full 10-bit `channels_per_frame` (`fsh[49:40]`) against the current format's `[31:22]`. A mismatch gets no accept verdict, so the depacketizer drops it. The comment citing the superseded Base Audio Formats v1.1 reading now gives the Milan v1.2 / IEEE 1722-2016 I.2.4 basis |
| `hdl/ieee1722/crf/KL_crf_rx.sv:323-335` (CRF input) | a Stream Data AVTPDU on the input's stream_id is received on it whatever its subtype. A non-CRF subtype is a format reject: counted, not accepted, lock kept, sequence unmoved |
| `tb/verilator/avtp_rxmon` | N=4 stack `[UF]`: a matching PDU, another channel count, a 264-channel PDU (high bits), the format a controller sets, and stream 0's `fmt0_i` path. `format_mutants.py` plants five compare defects, each caught by its named check. The lockstep reference gains the same compare in its own lines (the #762 precedent) |
| `tb/verilator/crf_rx` | `[FMT]`: an AAF PDU on the CRF stream_id, a matching CRF PDU, and the sequence after the reject; three mutants in `mutants.py` |
| `tb/verilator/milan_dp` | 11 cases (36 checks) fed STREAM_INPUT 0 a channel count other than its current format; they now carry it. In `sim_nxn.cpp` it comes from GET_STREAM_FORMAT; in `sim_main.cpp` / `sim_prune.cpp` it is the format declared in the shape header (`IN0_FMT_TB`). No check is removed or weakened |
| docs | FR-STR-03 and its status row, a live 4.4.2.2 row in the compliance matrix, `CRF_STATUS[15:8]`, `MEDIA_CLOCK_FOLLOWING.md`, `TESTING.md` |

No register map layout, top-level port or parameter change from this lane.

**Stacking.** The branch holds this lane's three commits (`31903ec1`, `91aaa6bd`, `cc71db3a`, first stacked on PR #767's round-1 head `4191b098`), then a merge of PR #767's round-2b head `eef90b42` (`2f33a9ce`, #767's history not rewritten). On top sits one commit that re-points two references the merge moved (`4605409b`, docs and a harness comment only). Both behaviours are kept. #762's stopped-input rules for silence and sequence gap (`stopped_i`) are byte-identical to `eef90b42`, and this lane's format compare is byte-identical to `cc71db3a`. In `KL_crf_rx.sv` the two do not interact: a format reject is not an accepted PDU, so it never reaches the interruption events that `stop_i` gates. Five test/doc files conflicted and were resolved by keeping both sides (`TESTING.md`, `crf_rx/sim_main.cpp` and `mutants.py`, `avtp_rxmon/Makefile`, the lockstep reference's header).

**Resources**, route-1x1 against PR #767's own route of `eef90b42` (same recipe, export script, tool build and pins): `avtp_rx_monitor` 800 -> 697 LUT after place, `crf_rx` 276 -> 282. Design LUT 49,597 -> 49,857 (+260): **+244 over the recorded baseline, inside the 500 tolerance; the resource gate exits 0.** FF 52,400 -> 52,291, BRAM and DSP unchanged. WNS +0.189 -> +0.137 ns, WHS +0.014 -> +0.024 ns, fully routed. After synthesis the design moves +27 LUT; the rest of the movement after place lands in blocks this RTL does not reach.

## Authoritative references

- Milan v1.2 4.4.2.2 (discard a PDU outside the configured format); 5.3.8.10 Table 5.6 UNSUPPORTED_FORMAT; 5.4.2.25 Table 5.16; 6.2, 6.4, 6.5 Table 6.2 (the channel count is part of the format).
- IEEE 1722-2016 7.3 Figure 26 (10-bit `channels_per_frame`); Annex I.2.4 (`ut` zero in a current format), I.2.4.1 (`channels_per_frame` matches the PDU).
- `docs/reference/FR_NFR.md` FR-STR-03; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.4.2.2 row.
- `docs/design/AREA_BUDGET.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (route-1x1).

## How to get into the same state

```sh
git fetch origin
git checkout 765-unsupported-format
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
```

## How to validate

```sh
make -C tb/verilator/avtp_rxmon
make -C tb/verilator/crf_rx
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp unb-mutants
python3 scripts/lint_rtl.py --check
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
TSN_GEN_ROOT="$TSN_GEN" make -C tb/verilator/tsn_fuzz
syn/yosys/run.sh
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
```

`$TSN_GEN` is a tsn-gen checkout at the CI pin (`TSN_GEN_REV` in `.github/workflows/rtl.yml`); `$WORK` is the route-1x1 work directory of `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

Expected result / pass criteria: every command rc 0. avtp_rxmon: `format_mutants.py` 6/6 and `lockstep_mutants.py` 14/14. crf_rx: `mutants.py` 21/21 (three clean controls and 18 planted mutants, #762's seven and #765's three among them). `unb-mutants` 6/6. tsn_fuzz: AAF/AVTP 164/0 and gPTP 677/0, freshness PASS. Yosys 58/58. Resource gate `RESULT: PASS`.

## Known limitations / out of scope

- Inputs above 0 read their current format only from LCTX words 2/3 (the CSR window). SET_STREAM_FORMAT reaches input 0 only, and no firmware writes those words. This predates the lane, but the compare now depends on it for the channel count too. The shipping 1x1 shape has one input.
- On the pruned 1x1 leg, a bare 86-octet 2-channel frame is accepted by the monitor but not emitted by the depacketizer (16 accepted, 0 emitted; the same at `4191b098`). Padded to 120 octets, 15 are emitted; padded to 230, all 16. `sim_prune.cpp` pads to 230 to keep its subject. Recommended as a new issue.
- samples_per_frame has no PDU field (IEEE 1722-2016 I.2.4.1), so no check is added.
- The flat `KL_avtp_rx_monitor` (a test instrument, not shipped) keeps no channel compare; the engine's banner records the difference.
- The only record of the old family compare as a 4.4.2.2 divergence is the archived `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md`, which never defines current behaviour. It is left as evidence; the live matrix row says the gap is closed.
- PR #767 has moved past `eef90b42` (round 3, `f3fef856`). In those commits the RTL changes only two comment lines; the rest is a `milan_dp` test case, a probe file and README text. That head is not merged here. Git merges it into this head without a textual conflict. Its new `[762-DP]` case still feeds STREAM_INPUT 0 a fixed 2-channel PDU, though, and this lane's compare rejects that PDU wherever the input's current format differs. So taking that head will need the same current-format stimulus change the 11 existing cases got. This is inferred from the source; it has not been run. This branch merges dev once #767 lands.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
