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

BLOCKED on one gate -- 63/63 suites, 2,186,679 checks, 0 failures; Yosys 58/58; xvlog 0 findings; 29 static gates rc 0; route-1x1 routed and timed (WNS +0.363 ns, WHS +0.015 ns, fully routed) but **the resource gate exits 1: LUT 50,158, +545 against the record's 500 tolerance** (+746 against the base route). The two changed modules net -1 LUT; the growth is optimization movement elsewhere (see Description). Accepting it means re-recording the route, a reviewed decision this lane does not make (`docs/design/AREA_BUDGET.md`). `765-unsupported-format` -> `dev`, head `cc71db3a557bb6160c81e69a52fd3ceed6622dc5`, three commits on PR #767's head `4191b098` (itself two commits on dev `e9cbb676`); it merges dev once #767 lands.

## Linked Issue / roles

Closes #765

Executor: `[A657]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

A PDU whose format differs from its Stream Input's current format now counts UNSUPPORTED_FORMAT and is discarded (Milan v1.2 Table 5.6 with Table 5.16, 4.4.2.2). Two gaps closed:

| Piece | Change |
|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:492-523` (AAF inputs) | the compare adds the full 10-bit `channels_per_frame` (`fsh[49:40]`) against the current format's `[31:22]`; a mismatch has no accept verdict, so the depacketizer drops it. The comment citing the superseded Base Audio Formats v1.1 reading is replaced with the Milan v1.2 / IEEE 1722-2016 I.2.4 basis |
| `hdl/ieee1722/crf/KL_crf_rx.sv:321-333` (CRF input) | a Stream Data AVTPDU on the input's stream_id is received on it whatever its subtype; a non-CRF subtype is a format reject (counted, not accepted, lock kept, sequence unmoved) |
| `tb/verilator/avtp_rxmon` | N=4 stack `[UF]`: matching PDU, another channel count, a 264-channel PDU (high bits), the format a controller sets, stream 0's `fmt0_i` path; `format_mutants.py` plants five compare defects, each caught by its named check. The lockstep reference gains the same compare in its own lines (the #762 precedent) |
| `tb/verilator/crf_rx` | `[FMT]`: an AAF PDU on the CRF stream_id, a matching CRF PDU, the sequence after the reject; three mutants in `mutants.py` |
| `tb/verilator/milan_dp` | 11 cases (36 checks) fed STREAM_INPUT 0 a channel count other than its current format; they now carry it: GET_STREAM_FORMAT in `sim_nxn.cpp`, the declared format out of the shape header (`IN0_FMT_TB`) in `sim_main.cpp`/`sim_prune.cpp`. No check removed or weakened |
| docs | FR-STR-03 and its status row, a live 4.4.2.2 row in the compliance matrix, `CRF_STATUS[15:8]`, `MEDIA_CLOCK_FOLLOWING.md`, `TESTING.md` |

No register map layout, top-level port or parameter changes.

Resources, route-1x1 against the base route of `4191b098` (same recipe, tool build, pins and Tcl): `avtp_rx_monitor` 778 -> 749 LUT, `crf_rx` 253 -> 281; design 49,411 -> 50,157 LUT. Synthesis alone already moves +621 LUT, +369 of it in the SoC CPU and +248 in top-level glue, neither reached by this RTL. `AREA_BUDGET.md` charges such movement to the change.

## Authoritative references

- Milan v1.2 4.4.2.2 (discard a PDU outside the configured format); 5.3.8.10 Table 5.6 UNSUPPORTED_FORMAT; 5.4.2.25 Table 5.16; 6.2, 6.4, 6.5 Table 6.2 (the channel count is part of the format).
- IEEE 1722-2016 7.3 Figure 26 (10-bit `channels_per_frame`); Annex I.2.4 (`ut` zero in a current format), I.2.4.1 (`channels_per_frame` matches the PDU).
- `docs/reference/FR_NFR.md` FR-STR-03; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.4.2.2 row.

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
syn/yosys/run.sh
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
```

Expected result / pass criteria: every suite rc 0, `format_mutants.py` 6/6, crf_rx mutants 18/18, unb-mutants 6/6; Yosys 58/58. The resource gate exits 1 at this head (see Status) until the route is accepted and re-recorded.

## Known limitations / out of scope

- Inputs above 0 read their current format only from LCTX words 2/3 (the CSR window); SET_STREAM_FORMAT reaches input 0 only, and no firmware writes those words. Pre-existing; the compare now depends on it for the channel count too. The shipping 1x1 shape has one input.
- On the pruned 1x1 leg, a bare 86-octet 2-channel frame is accepted by the monitor but not emitted by the depacketizer (16 accepted, 0 emitted; the same at `4191b098`); padded to 120 octets 15, to 230 all 16. `sim_prune.cpp` pads to 230 to keep its subject. Recommended as a new issue.
- samples_per_frame has no PDU field (IEEE 1722-2016 I.2.4.1); no check is added.
- The flat `KL_avtp_rx_monitor` (a test instrument, not shipped) keeps no channel compare; the engine's banner records the delta.
- The only record of the old family compare as a 4.4.2.2 divergence is the archived `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md`, which never defines current behaviour; it is left as evidence and the live matrix row says it is closed.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (resource gate exits 1)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
