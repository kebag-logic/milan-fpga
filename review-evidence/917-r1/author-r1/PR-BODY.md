[A784]

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

GREEN on every gate below at `3926c271` (three commits on `cec88385`), awaiting review: `917-aecp-hold` -> `dev-soft-core` (the Mark II flip train's base, #665).

## Linked Issue / roles

Closes #917
Relates to #665

Executor: `[A784]`
Internal cleared-context reviewer: to be named
External reviewer: to be named

## Description

The split's AECP ingress budget (`rate: {burst: 16, refill_ms: 5}`) dropped a controller's command
that arrived with no token, which costs a controller that keeps one command in flight a timeout and
a retry (IEEE 1722.1-2021 9.2.2.4); at about 1 kHz a controller lost about one command in 21. This
implements the default of the ruling on #665 (issuecomment-6894152131, item 2): the table's figures
stay, a frame that finds no token is **held** and committed at the next refill, and only a frame
arriving behind a held one may be dropped, and it is **counted**.

| Piece | Change |
|---|---|
| `hdl/milan/mailbox/KL_mbx_rx.sv` | A per-channel write head (`wr_head_r`) runs ahead of `RX_HEAD` by a held record, and a held flag. A frame that passes the filter and finds the bucket empty is written as a committed one is (words while it arrives, header after the verdict) but `RX_HEAD` stays; the channel's next refill commits it and takes that refill's token. A frame that finds the bucket empty while one is held is refused in `RATE_DROP` (and `IRQ_STATUS.ERR`). The next frame's words and free space are based on the write head, so they never touch the held record; a tail ahead of `RX_HEAD` inside the held record still leaves no free word. A refill landing between the verdict and the header writes commits the frame at once, so a channel never holds a frame beside a token. A frame that finds a token takes the same clocks as before. |
| Contract | No register, field, ring, rate figure or version change: `RATE_DROP` ("frames the channel's rate limiter refused") is the counter of the frames dropped behind a held one. `mailbox_emit.py`'s filter sentence and the YAML's filter comment describe the hold; `gen_mailbox.py --write` leaves `KL_mbx_pkg.sv`, `KL_mbx.sv` and `mbx_contract.h` byte-identical and moves only `docs/reference/MAILBOX_CONTRACT.md`. |
| Scope | Generic: every channel of the table carries a rate and the buckets are per channel, so every channel holds its frame the same way. The committed rate is unchanged (every commit, held or not, spends one token), so is the load. |
| Fabric host model | `sw/firmware/ctrl/host/mbx_model.{c,h}` follows the RTL (a held record's words past `RX_HEAD`, committed by the refill), so the shared suite and the co-simulation keep grading the RTL and the model with one set of expectations. It is compiled into no firmware image. |
| Tests | `tb/verilator/mbx`: T0, T1, Q10 and V0 graded for the ruling; new group `HeldNotDropped` (B0 to B4) on the RTL through both adapters and on the host model, B5 and B6 on the RTL at the clock; seven planted defects, `rx-drop-instead-of-hold` in the default `make`; the model's twin in `ctrl_mutants.py`. `test_acmp_mbx.cpp`'s three ring-fill loops count committed records from `RX_PASS` and wait out a held one; their expectations are unchanged. |
| Docs | `docs/design/MAILBOX_SPLIT.md` (the filter section, "The held frame", the verification table's counts at this head), `tb/verilator/mbx/README.md`, the Makefile's target list. |

New checks and the planted defect each catches (failing words in quotes):

| Check | What | Planted defect |
|---|---|---|
| B0 | fifty AECP READ_DESCRIPTORs, one in flight, each at line rate as the one before it is delivered: all delivered, in order, byte for byte; the burst at once, every later one within one refill period; nothing counted, no ERR | `rx-drop-instead-of-hold`: "B0 fifty AECP commands, each sent at line rate as the one before it is delivered, are all delivered" |
| B1 | three commands back to back on one token: the first at once, the third (behind the held second) dropped and counted in `RATE_DROP` with ERR, the second at the next refill, the third never | `rx-hold-behind-a-held-frame`, `rx-next-frame-over-the-held-record` |
| B2 | a controller at one command a millisecond, one in flight: none of a hundred lost (the hardware finding) | `rx-drop-instead-of-hold` |
| B3 | a reset forgets a held frame; the bucket is full again | |
| B4 | a tail ahead of `RX_HEAD` inside the held record leaves no free word (`RX_DROP`), the held record committed whole once the tail is back | `rx-tail-inside-the-held-record-frees-space` |
| B5 (RTL) | a refill in the clock of each header word and the clock after commits the frame then, once | `rx-refill-in-the-header-clock-missed` (+`-axil`) |
| B6 (RTL) | over every clock of every check, no channel holds a frame while its bucket holds a token | the same |
| T0, T1 | the burst passes, the frame past it is held (not committed) until the next refill, whose commit moves `RX_HEAD` over it; it keeps its arrival NOW_MS and spends that refill's token; only the frame behind it counts | `rx-held-record-never-committed`, `rx-bucket-never-drains`, `rx-refill-slow` |

Evidence, every run on a clean clone (the receipts' index lists each file):

| Gate | Head | Result |
|---|---|---|
| Verilator sweep, all suites, as four native shards | `84d8a214` | 65 of 65 suites pass |
| Its shard 1/4, which holds `mbx`, again | `3926c271` | 17 of 17 pass (`mbx`: 607 Wishbone, 652 AXI4-Lite, 32 co-simulation, 614 and 659 at two interfaces, 532 on the host model, 13 of 13 quick mutants) |
| `make -C tb/verilator/mbx mutants` | `3926c271` | 238 of 238 planted defects caught by their named checks, after four positive controls |
| rtl-fast, elaborate, docs and the rtl yosys jobs, step by step | `3926c271` | 139 steps rc 0, 226 not run with a stated reason (hosted orchestration, package installs this host already has), 0 bad; firmware control mutants 699 of 699 caught |
| Firmware images | `3926c271` and `84d8a214` against `cec88385` | byte-identical: 46 fixture images (every config, one and two interfaces, flat and split, the ledgered 8x8/2if), and the split platform images 1x1/1if (`bb04b696...`, 145,496 B) and 8x8/1if (`506a1ae4...`, 158,176 B) with their ROM bank images |
| Split boot | `84d8a214` (RTL and firmware equal at `3926c271`) | 1x1 and 8x8 PASS |
| AX7101 split image, S9's recipe, three directives | `3926c271` | best AltSpreadLogic_high: WNS +0.203 ns, WHS +0.036 ns over every corner, 0 failing endpoints (ExtraTimingOpt +0.063 / +0.036 also meets; ExtraPostPlacementOpt +0.202 / +0.016 misses the hold floor); the base met the +0.030 hold floor on none |
| Area, placed, against the base's route | | LUT +74 to +181 by directive, FF +75/+76, LUTRAM 0/+1, BRAM (78.5 tiles: 60 RAMB36, 37 RAMB18) and DSP unchanged; `KL_mbx_rx` +124 to +133 LUT, +77 FF |
| CPU budget harness 1x1, base against head | `cec88385` and `84d8a214` | all 94 groups' simulation logs, scripts and graded results, and `table.md`, byte-identical base against head (283 of 284 files; `results.json` differs only in its `build` digest of the changed RTL); 0 refusals at both, the same 7 recorded budget misses at both (pre-existing) |


## Authoritative references

- #917 (acceptance) and the ruling on #665, issuecomment-6894152131, item 2 (the default implemented here).
- IEEE 1722.1-2021 9.2.2.4: a controller's command timeout and retry.
- [REQUIREMENTS.md section 1](../REQUIREMENTS.md#1-product-ownership) and NFR-SCOUT-02/08 ([FR_NFR.md 3.4](../docs/reference/FR_NFR.md#34-fabric-scale-out-and-future-ports)): per-channel token buckets remain in force; they do (the committed rate is the table's).
- `sw/mailbox/mailbox.yaml`: the rate table, `RX_TAIL` (a value ahead of `RX_HEAD` leaves no free word), `RATE_DROP`.
- [docs/design/MAILBOX_SPLIT.md, The held frame](../docs/design/MAILBOX_SPLIT.md#the-held-frame).

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git && cd milan-fpga
git fetch origin 917-aecp-hold && git checkout --detach 3926c271
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the pinned Verilator 5.050 on PATH (or VERILATOR=), the pinned RV32 SDK for the firmware gate (MILAN_RV32_CC=)
```

## How to validate

```sh
make -C tb/verilator/mbx                 # both adapters, co-simulation, two interfaces, host model, 13 quick mutants, the mover
make -C tb/verilator/mbx mutants         # every planted defect, after the positive controls
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
python3 -B sw/mailbox/gen_mailbox.py --check
python3 scripts/lint_rtl.py --check
```

Expected result / pass criteria: every command exits 0. The mailbox suite ends `checks: 607   failures: 0`
(Wishbone), `652` (AXI4-Lite), `32` (co-simulation), `614` and `659` (two interfaces), `532` (host model),
`mbx mutants: 13 of 13 caught`; `make mutants` ends `mbx mutants: 238 of 238 caught`; the firmware gate ends
`test_ctrl_firmware: PASS`.

## Known limitations / out of scope

- The on-hardware acceptance (three descriptor walks with none unanswered) needs the test machine and is not run here.
- Printing the drop counters on the console waits until after the flip (ruling item 2); `RATE_DROP` is readable now.
- The owner may still choose to flip with the limit documented instead (ruling item 2); this PR is the default.
- A frame held when its channel is closed is still committed at the next refill: it passed the filter while the channel was open, as a frame committed just before the close is.
- The fabric host model and three host-test loops live under `sw/firmware/ctrl/` but are not firmware image sources; every firmware image is byte-identical to the base's (see Status).
- The CPU budget harness (`tb/verilator/ctrl_service_budget`) Verilates this RTL but is not a CI gate; it was compared at the shipping 1x1 point (identical, above), not at 8x8. Its composed rows empty the adp, aecp and srp buckets (acmp and maap are bounded by their rings) and its save windows empty every bucket at each burst, but no scenario sends a frame into an empty bucket, which the base would have refused and its grader would have failed. It cites MAILBOX_SPLIT.md by line number, already stale at the base; worth an Issue of its own.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench criteria here; the hardware walks remain)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
