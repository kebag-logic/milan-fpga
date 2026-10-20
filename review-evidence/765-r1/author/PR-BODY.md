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

Green locally at `75db4b57`, review ready; `765-unsupported-format` -> `dev` (dev `78ca9bdf` merged in). Full sweep: 63/63 suites, 2,187,823 checks, 0 failures. tsn_fuzz: AAF/AVTP 164/0 and gPTP 677/0. Mutant drivers: `format_mutants.py` 6/6, `lockstep_mutants.py` 14/14, crf_rx `mutants.py` 21/21, `unb-mutants` 6/6, `render_mutants.py` 6/6. The `[762-DP]` wiring plants are 8/8 (three plants and a clean control on two legs). Yosys 58/58, xvlog 0 findings, builder bank 103 gates. route-1x1 fully routed (WNS +0.137 ns, WHS +0.024 ns), and the resource gate passes (LUT +244 over the record, tolerance 500).

## Linked Issue / roles

Closes #765
Relates to #762

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
| `tb/verilator/milan_dp` | 12 cases fed STREAM_INPUT 0 a channel count other than its current format, and now carry it: round 1's 11 (36 checks), and #762's `[762-DP]` (`sim_nxn.cpp:6764-6772`). In `sim_nxn.cpp` the count comes from GET_STREAM_FORMAT; in `sim_main.cpp` / `sim_prune.cpp` it is the format declared in the shape header (`IN0_FMT_TB`). No check is removed or weakened |
| docs | FR-STR-03 and its status row, a live 4.4.2.2 row in the compliance matrix, `CRF_STATUS[15:8]`, `MEDIA_CLOCK_FOLLOWING.md`, `TESTING.md`, the milan_dp README's `[762-DP]` paragraph |

No register map layout, top-level port or parameter change from this lane.

**History.** The branch holds this lane's three commits (`31903ec1`, `91aaa6bd`, `cc71db3a`), then a merge of PR #767's round-2b head (`2f33a9ce`) and a reference fix (`4605409b`). On top are a merge of `dev` at `78ca9bdf` (`7f84892a`; PR #767 and PR #766 merged), with no conflict, and the `[762-DP]` stimulus change (`75db4b57`). Nothing is rebased.

**`[762-DP]` and #765.** #767's `[762-DP]` case fed STREAM_INPUT 0 a fixed 2-channel PDU. Under this compare that PDU is a format reject wherever the input's current format has another channel count. At the merge commit `7f84892a` the case fails 4 checks on `obj_dynmap` (8 channels) and on `obj_nxn4c` (4 channels): no gap is seen, nothing relocks, nothing counts after START. `75db4b57` reads the input's current format with GET_STREAM_FORMAT, as the 5.3.8.7 discard section before it already does, and builds the PDUs with it. Its counts keep their meaning on all five legs that run it (`obj_dynmap`, `obj_nxn`, `obj_nxndv`, `obj_nxn8`, `obj_nxn4c`). While stopped, SEQ_NUM_MISMATCH and MEDIA_UNLOCKED each move +1 and STREAM_INTERRUPTED stays +0; after START, STREAM_INTERRUPTED moves +1. #762's three wiring plants at `milan_datapath.sv:6308` each still fail exactly their named checks on `obj_dynmap` and `obj_nxn4c`: the tie-off, sink 1's level and the bound level.

**Resources**, route-1x1, measured against PR #767's own route of `eef90b42` (same recipe, export script, tool build and pins). `avtp_rx_monitor` goes 800 -> 697 LUT after place and `crf_rx` 276 -> 282. Design LUT goes 49,597 -> 49,857 (+260): **+244 over the recorded baseline, inside the 500 tolerance; the resource gate exits 0.** FF 52,400 -> 52,291, BRAM and DSP unchanged. WNS +0.189 -> +0.137 ns, WHS +0.014 -> +0.024 ns, fully routed. After synthesis the design moves +27 LUT; the rest of the movement after place lands in blocks this RTL does not reach. The route at `75db4b57` reproduces the one at `2f33a9ce` exactly: same figures, same timing report body, same utilization tables. Since `2f33a9ce`, build inputs have changed by two RTL comment lines only.

## Authoritative references

- Milan v1.2 4.4.2.2 (discard a PDU outside the configured format); 5.3.8.10 Table 5.6 UNSUPPORTED_FORMAT; 5.4.2.25 Table 5.16; 6.2, 6.4, 6.5 Table 6.2 (the channel count is part of the format); 5.3.8.7 and 5.4.2.20 (`[762-DP]`, a stopped input).
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
python3 scripts/docs_check.py
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
TSN_GEN_ROOT="$TSN_GEN" make -C tb/verilator/tsn_fuzz
syn/yosys/run.sh
python3 scripts/xvlog_gate.py --check
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
```

`$TSN_GEN` is a tsn-gen checkout at the CI pin (`TSN_GEN_REV` in `.github/workflows/rtl.yml`), with `packet_gen` built. `$WORK` is the route-1x1 work directory of `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`. The builder bank runs as `docs/testing/CI_WORKFLOWS.md` gives it (`scripts/ci_builder_legs.py run 0`, `run 1`, then `union --workflow elaborate`).

The `[762-DP]` wiring plants are a one-line edit of `hdl/milan/milan_datapath.sv:6308`, the `.stopped_i` connection, followed by the leg run in a scratch copy of the tree:

```sh
make -C tb/verilator/milan_dp run-dynmap
make -C tb/verilator/milan_dp run-nxn4c
```

The three plants are `('0)`, `(acmpl_stopped_v_w[N_STREAMS:1])` and `(acmpl_bound_v_w[N_STREAMS-1:0])`. Leave the same slice at `:5952`, the clock meter, alone.

Expected result / pass criteria: every command rc 0. avtp_rxmon: `format_mutants.py` 6/6 and `lockstep_mutants.py` 14/14. crf_rx: `mutants.py` 21/21 (three clean controls and 18 planted mutants, #762's seven and #765's three among them). milan_dp: every leg passes (`obj_dynmap` 201 checks, `obj_nxn4c` 1983) and each `[762-DP]` section logs input 0's current format. `unb-mutants` 6/6. tsn_fuzz: AAF/AVTP 164/0 and gPTP 677/0, freshness PASS. Yosys 58/58. xvlog 0 findings. Resource gate `RESULT: PASS`. Each `[762-DP]` plant exits nonzero. The tie-off and sink-1 plants fail exactly `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` and `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0`; the bound-level plant fails exactly `[762-DP] 4 started gap: STREAM_INTERRUPTED +1`.

## Known limitations / out of scope

- Inputs above 0 read their current format only from LCTX words 2/3 (the CSR window). SET_STREAM_FORMAT reaches input 0 only, and no firmware writes those words. This predates the lane, but the compare now depends on it for the channel count too. The shipping 1x1 shape has one input.
- On the pruned 1x1 leg, a bare 86-octet 2-channel frame is accepted by the monitor but not emitted by the depacketizer (16 accepted, 0 emitted; the same at `4191b098`). Padded to 120 octets, 15 are emitted; padded to 230, all 16. `sim_prune.cpp` pads to 230 to keep its subject. Recommended as a new issue.
- samples_per_frame has no PDU field (IEEE 1722-2016 I.2.4.1), so no check is added.
- The flat `KL_avtp_rx_monitor` (a test instrument, not shipped) keeps no channel compare; the engine's banner records the difference.
- The only record of the old family compare as a 4.4.2.2 divergence is the archived `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md`, which never defines current behaviour. It is left as evidence; the live matrix row says the gap is closed.
- `make dynmap-mutants` (the `[DYNMAP]` campaign) was not re-run for the `[762-DP]` change, which touches only the case that follows `[DYNMAP]` on a fresh boot.

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
