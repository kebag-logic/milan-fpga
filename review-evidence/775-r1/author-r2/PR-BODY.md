[A666]

## Contents

- **[Status](#status)** - Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** - Public task, executor, and independent reviewers.
- **[Description](#description)** - What changed and why.
- **[Authoritative references](#authoritative-references)** - Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** - Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** - Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** - What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** - The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN, review ready at `c2a080ae` (round 2); `775-offformat-seq-advance` -> `dev` (based on dev `a032c6d6`, still the dev tip).

Round 2 (`c2a080ae`): full sweep as four shards: 64/64 suites, 2,189,642 checks, 0 failures. avtp_rxmon: NX 194/0, `format_mutants.py` 11/11, `lockstep_mutants.py` 14/14, lockstep N=1 116/0 and N=8 119/0. 30 static gates rc 0, lint 89 <= 89. The docs workflow's gates under GNU Make 4.3: 42 run, all rc 0. The RTL changes only in comments (identical after comment stripping), so route-1x1 was not rerun.

Round 1 (`c7e87c8c`): full sweep as four shards: 64/64 suites, 2,189,615 checks, 0 failures. avtp_rxmon: NX 169/0, `format_mutants.py` 9/9, `lockstep_mutants.py` 14/14. crf_rx: unit 15,714/0, `mutants.py` 23/23. Yosys 60/60 tops. Lint at its ratchet. 30 static gates rc 0. The docs workflow's gates under GNU Make 4.3: 42 run, all rc 0. route-1x1 is fully routed, with WNS +0.141 ns and WHS +0.019 ns. The resource gate passes against the 2026-10-23 record: SLICE 15,833 (-2), LUT +54, FF +10, RAMB/DSP unchanged.

## Linked Issue / roles

Closes #775
Relates to #765

Executor: `[A666]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

On the bench, one PDU of an in-order stream replaced by a PDU of another format (another channel count on an AAF input, or an AAF PDU on the CRF input) counted UNSUPPORTED_FORMAT +1, which is #765's fix, and SEQ_NUM_MISMATCH +1 on both inputs. The discarded PDU did not advance the input's sequence state, so the next in-order PDU looked non-sequential.

The ruling on #775 (Milan v1.2 Table 5.6): an off-format Stream Data AVTPDU is a received PDU. Its sequence_num advances the input's sequence state, while it counts only UNSUPPORTED_FORMAT and presents nothing.

| Commit | File:line at `c7e87c8c` (round 1) | Change |
|---|---|---|
| `0ee987f4` | `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:1009-1020` | AAF input. In M_PDEC_S's `!fmt_ok_w` branch the walker keeps MON_STATE and replaces only prev_seq (`[7:0]`) with the PDU's sequence_num, which is what an accepted PDU writes there. Then it moves to the new state `M_PSEQ_S` (`:292`, write `:638-642`, exit `:1061`), which writes that one word and returns to idle. Lock, settle, wire_chans and the mr reference keep their values. No accept verdict is given, no timestamp word is written and no counter walks. Only the UNSUPPORTED_FORMAT flag is raised, as before |
| `0ee987f4` | `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:15-16,292,619-623,990-993,1045` | the lockstep reference takes the same edit in the same lines (the #762 and #765 precedent). Its soak sends off-format PDUs, so the cycle-exact `[LS]`/`[GC]` compare stays exact. #775 is graded by `[SQ]` by count, never against this copy |
| `6ff2880a` | `hdl/ieee1722/crf/KL_crf_rx.sv:603-607` | CRF input. The rejected branch sets `exp_seq_r <= seq_i + 1`. `have_seq_r` is unchanged, so only an accepted PDU seeds the cursor (the first-PDU behaviour is kept) |
| `c7e87c8c` | `docs/reference/FR_NFR.md` FR-STR-03, `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.4.2.2 / Table 5.6 row, `docs/testing/TESTING.md` avtp_rxmon and crf_rx rows | state the rule and its tests |

A discarded AAF PDU now takes one more walker cycle (PDEC, PSEQ, idle instead of PDEC, idle). That is still fewer than an accepted PDU takes. No register-map, port, parameter or interface change.

**New checks** (round 1; lines at `c7e87c8c`).

- `tb/verilator/avtp_rxmon/sim_main_nx.cpp:991-1075`, `[SQ]`, 22 checks. Stream 3 is freshly bound and locked. One 2-channel PDU against the current 8 channels arrives mid-stream. It carries a toggled mr, tu and a timestamp already past.
  - It has no accept verdict and emits no payload.
  - prev_seq becomes its sequence_num. LAST_TSD and wire_chans are unchanged.
  - Six in-order PDUs follow, over two observation intervals. UNSUPPORTED_FORMAT moves +1. SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, LATE_TIMESTAMP, EARLY_TIMESTAMP, STREAM_INTERRUPTED and MEDIA_UNLOCKED do not move. FRAMES_RX moves +6.
  - Then a second off-format PDU (early) is followed by a gap of one lost PDU. SEQ_NUM_MISMATCH moves +1 and STREAM_INTERRUPTED does not move, so the gap is measured from the off-format PDU's sequence_num. Without the advance, two PDUs would count as lost.
- `tb/verilator/crf_rx/sim_main.cpp:1570-1685`, `[SQ]`, 23 checks. The same shape on the CRF input: an AAF PDU in a CRF PDU's slot, carrying a toggled mr, tu and a late (later early) reference timestamp.
  - It is not accepted, gives no timing point, leaves delta_o and keeps the lock.
  - The same counter holds as on AAF follow, over two intervals, and the same gap-of-one result.
  - `[SQ-d]`: an AAF PDU first in a fresh era seeds nothing. The first accepted PDU counts no SEQ_NUM_MISMATCH and no STREAM_INTERRUPTED, whatever sequence_num it carries.

**Planted mutants**, each required to fail its named check (`format_mutants.py`, crf_rx `mutants.py`):

| Mutant (where) | Named check | All checks it fails |
|---|---|---|
| no advance (`ctx.sv:1019` writes `ram_q_r` back) | `[SQ2c] SEQ_NUM_MISMATCH unchanged: the next PDU was in sequence` | `no mismatch across bad-format PDUs`, `[UF2g]`, `[SQ1c]`, `[SQ2c]`, `[SQ3c]` |
| whole state (`ctx.sv:1019` writes `monst_next_w`) | `[SQ2d] MEDIA_RESET unchanged` | `[UF2e]`, `[UF4g]`, `[SQ1e]`, `[SQ2d]`, `[SQ3f]` |
| accepted walk (`ctx.sv:1020` goes to `M_PWR_S`) | `[SQ1d] ...and it writes no timestamp word (LAST_TSD)` | `[SQ1d]` |
| CRF no advance (`crf_rx.sv:607` removed) | `[SQ-b2] SEQ_NUM_MISMATCH unchanged: the next PDU was in sequence` | `[5t-a5]`, `[ST-c3]`, `[FMT-c1]`, `[SQ-b2]`, `[SQ-c2]`, plus 170 per-PDU replica compares |
| CRF reject seeds (`have_seq_r <= 1` added) | `[SQ-d1] an AAF PDU first in an era seeds no SEQ_NUM_MISMATCH` | `seq skip: ONE interval tick`, `clean resume: seq_err holds at 1`, `[SQ-d1]`, `[SQ-d2]`, plus 1,972 per-PDU replica compares |

The head's harnesses built against dev `a032c6d6`'s two RTL files fail as the bench did. The AAF harness fails 5 checks, among them `[SQ2c]` (got 1, expected 0) and `[SQ3c]`. The CRF harness fails `[FMT-c1]`, `[SQ-b2]` and `[SQ-c2]` among 175 failures. The discontinuity harness fails `rejected marker never seeds the reference`.

### Round 2: the lock and settle state across a reject (R685-1)

R685-1 F1 found that the AAF `[SQ]` cases ran on a locked, settled stream only. A reject that set media_locked, or stepped the settle count, survived every avtp_rxmon leg when it was planted in the engine and the lockstep reference together. The testing guide also claimed "writes only prev_seq", which the cases did not grade. The RTL was correct: `{ram_q_r[31:8], seq}` keeps bits 8 to 31. This round adds the two missing arms and corrects the guide, with no logic change.

| Commit | File:line at `c2a080ae` | Change |
|---|---|---|
| `50275e29` | `tb/verilator/avtp_rxmon/sim_main_nx.cpp:1066-1085` `[SQ4]` | An off-format PDU first in a fresh era, on an unlocked stream. The stream stays unlocked and counts no MEDIA_LOCKED at the reject. MEDIA_LOCKED counts once at the first accepted PDU after it, which locks the stream |
| `50275e29` | `sim_main_nx.cpp:1092-1119` `[SQ5]` | An off-format PDU inside the settle window, with one PDU of the window left. A gap at that PDU counts nothing, so the window was not shortened; the next gap counts SEQ_NUM_MISMATCH once, so it was not restarted |
| `50275e29` | `sim_main_nx.cpp:1007-1017,1123-1179` | Each new arm keeps the existing counter checks (UNSUPPORTED_FORMAT +1; MEDIA_RESET, TIMESTAMP_UNCERTAIN, LATE, EARLY, STREAM_INTERRUPTED, MEDIA_UNLOCKED +0; FRAMES_RX the accepted PDUs only). `[SQ]` is split into three phases with shared helpers so no function exceeds the 100-line ratchet. `[SQ0]` to `[SQ3]` are unchanged |
| `50275e29` | `tb/verilator/avtp_rxmon/format_mutants.py:22-31,91-104,130-150,200-204` | Two arms, the review's `lock_set` and `settle_dec`. Each is the defect in the engine and in the same line of the lockstep reference. The arm fails if the reference no longer carries that line |
| `3f5cebd0` | `docs/testing/TESTING.md:617` | It states the three points of a stream `[SQ]` grades and the counters at each, that the mr reference and seed are graded through MEDIA_RESET, and that the 100 ms silence watchdog across a reject is not graded |
| `c2a080ae` | `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:15-23,96-100` | Comments only (R685-1 F2). #775 is listed among the N=1 deltas from the flat monitor, and the contract line no longer puts it inside the flat module's contract |

| Mutant (engine and reference together) | Named check | Every check it fails |
|---|---|---|
| lock set: the reject writes `{ram_q_r[31:13], 1'b1, ram_q_r[11:8], seq}` | `[SQ4f] MEDIA_LOCKED +1 at the first accepted PDU` (got 0) | `[SQ4c]`, `[SQ4f]` |
| settle step: the reject writes `settle == 0 ? 0 : settle - 1` | `[SQ5c] a gap at the window's last PDU counts no SEQ_NUM_MISMATCH` (got 1) | `[SQ5c]`, `[SQ5d]`, `[SQ5g]` |

The review's own probes were rerun at `c2a080ae`. With both defects planted in the engine and the reference, the N=4 stack now fails the named `[SQ]` checks, while the lockstep still passes, at N=1 116/0 and N=8 119/0. The review's 13-mutant probe catches 12, where it caught 10. The survivor is a reject that refreshes the 100 ms silence watchdog. That behaviour predates #775 and is out of scope for this change.

The RTL file is identical after comment stripping (`verilator -E -P`, 804 lines each, the same SHA-256), so route-1x1 was not rerun. The round-1 route at `c7e87c8c` stands for the logic.

### Round 1

**Stimulus that reused a sequence number across a reject now consumes one.** Under the ruling a reused number is a real repeat: a SEQ_NUM_MISMATCH and, mod 256, a 255-PDU loss. Each site now drives an in-order stream with one PDU replaced. No check, count or expectation changes.

- avtp_rxmon `[G5]` (`sim_main_nx.cpp:339,346-348`), `[UF2]`, `[UF3]`, `[UF4c]` (`:931,938-939,949,960`).
- crf_rx: every reject site (`sim_main.cpp`, `m.bad_pdu(seq++)`). The replica's `bad_pdu(seq)` (`:191-197`) advances its cursor the same way.
- crf_rx `sim_discontinuity.cpp:138,198`.
- milan_dp `[CTRS-CRF]` event arm (`sim_nxn.cpp:7047,7065-7067`). Its planned counts are unchanged, because P2's two lost PDUs are now counted from the last reject.

## Authoritative references

- Milan v1.2 5.3.8.10 Table 5.6: SEQ_NUM_MISMATCH counts a Stream Data AVTPDU received with a non-sequential sequence_num. UNSUPPORTED_FORMAT counts one that "has been received with a format that did not match". 4.4.2.2: the Listener discards it.
- #775 and its ruling, #765 / PR #769 (the format compare this follows), FR-STR-03.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `docs/design/AREA_BUDGET.md`, `syn/ooc/pp_resource_baseline.json` (the 2026-10-23 record, #632/#764).

## How to get into the same state

```sh
git fetch origin
git switch --detach c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

Verilator 5.050 first on `PATH` (the CI pin), sv2v v0.0.12, Yosys 0.66, Vivado 2026.1.

## How to validate

```sh
make -C tb/verilator/avtp_rxmon
make -C tb/verilator/crf_rx
logs="$(mktemp -d)"
for k in 0 1 2 3; do bash scripts/run_all_suites.sh "$logs/$k" --wait --shard "$k/4"; done
syn/yosys/run.sh
python3 scripts/lint_rtl.py --check
python3 syn/ooc/pp_resource_gate.py check <route-1x1 gateware dir> --endpoint route-1x1
```

Expected result / pass criteria:

- avtp_rxmon: rc 0. Flat 97/0, NX 194/0, lockstep N=1 116/0 and N=8 119/0, `lockstep_mutants.py` 14/14, `format_mutants.py` 11/11.
- crf_rx: rc 0. Unit 15,714/0, talker step 69/0, `mutants.py` 23/23.
- Sweep: every shard rc 0, 64/64 suites, 2,189,642 checks, 0 failures.
- Yosys: rc 0. Lint: rc 0 at the ratchet (89 <= 89).
- route-1x1 (round 1, at `c7e87c8c`; round 2 changes RTL comments only): the shipping AX7101 1x1 export per `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (`pp_baseline.py --single-thread-synthesis`), one Vivado run under the exclusive lock. Routed with all constraints met; the resource gate gives rc 0, RESULT: PASS (SLICE 15,833 against the record's 15,835; LUT 51,313 against 51,259; FF 53,218 against 53,208; WNS +0.141 ns; WHS +0.019 ns). The worst setup path is in the SoC bus (`axilite2wishbone` -> `spiflash_phy`), not the changed logic

## Known limitations / out of scope

- `[SQ]` does not grade the AAF input's 100 ms silence watchdog across a reject: a reject that refreshed it would pass every avtp_rxmon leg. That behaviour predates #775 and is unchanged here; it is left to the maintainer as a possible new issue (R685-1 F3).
- The flat test instrument `KL_avtp_rx_monitor` is unchanged. No shipping module instantiates it; it is the DUT of tsn_fuzz and of avtp_rxmon's flat leg. Its reject path still leaves `prev_seq_r` untouched (`KL_avtp_rx_monitor.sv:265-269`). Whether it should follow is left to the maintainer as a possible new issue.
- tsn_fuzz was not run: it builds only the flat instrument, which this change does not touch.
- The advance takes the off-format PDU's own sequence_num. A gap or repeat on the off-format PDU itself is not counted, because a rejected PDU counts only UNSUPPORTED_FORMAT (the ruling). The next PDU is measured from it.
- No hardware or bench run here. The bench check of #775 (in-order stream, one PDU replaced, SEQ_NUM_MISMATCH +0) is for the test machine.

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
