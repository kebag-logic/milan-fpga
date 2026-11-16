[A784]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — Each round-1 finding, where it is closed and how that is checked.
- **[Round 3](#round-3)** — Each round-2 finding, where it is closed and how that is checked.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN on every gate below at `394612c5` (six commits on `cec88385`: round 1 `84d8a214`, `bb001e10`, `3926c271`; round 2 `8f73ade5`; round 3 `93163957`, `394612c5`), awaiting re-review: `917-aecp-hold` -> `dev-soft-core` (the Mark II flip train's base, #665).

Author packets: [`review-evidence/917-r1/author-r1` and `author-r2`](https://github.com/kebag-logic/milan-fpga/tree/24755cf4/review-evidence/917-r1) on branch `917-review-evidence`; round 3's receipts join them as `author-r3` when published.

## Linked Issue / roles

Closes #917
Relates to #665

Executor: `[A784]`
Internal cleared-context reviewer: `[R845]` (R845-1 NEGATIVE at `3926c271`; R845-2 NEGATIVE at `8f73ade5`; round 3 review R845-3)
External reviewer: `[R846]` (R846-1 NEGATIVE at `3926c271`; R846-2 NEGATIVE at `8f73ade5`; round 3 review R846-3)

## Description

The split's AECP ingress budget (`rate: {burst: 16, refill_ms: 5}`) dropped a command that arrived with no token. #917 measured a controller that keeps one command in flight: at about 1 kHz it lost about one command in 21 once the burst was spent, each costing it its transaction timeout and a retry (IEEE 1722.1-2021 9.3.2.6, 9.3.6). One in flight is that workload, not a rule of the protocol (a controller may pipeline commands, 9.2.2). This implements the default of the ruling on #665 (issuecomment-6894152131, item 2): the table's figures stay, a frame that finds no token is **held** and committed at the next refill, and only a frame arriving behind a held one may be dropped, and it is **counted**.

| Piece | Change |
|---|---|
| `hdl/milan/mailbox/KL_mbx_rx.sv` | A per-channel write head (`wr_head_r`) runs ahead of `RX_HEAD` by a held record, and a held flag. A frame that passes the filter and fits and finds the bucket empty is written as a committed one is (words while it arrives, header after the verdict) but `RX_HEAD` stays; the channel's next refill commits it and takes that refill's token, open channel or not. A frame that passes and fits and finds the bucket empty while one is held is refused in `RATE_DROP` (and `IRQ_STATUS.ERR`); one the filter refuses counts nowhere and one that does not fit counts in `RX_DROP`, as anywhere else. The next frame's words and free space are based on the write head, so they never touch the held record; a tail ahead of `RX_HEAD` inside the held record still leaves no free word. A refill landing between the verdict and the header writes commits the frame at once, so a channel never holds a frame beside a token. A frame that finds a token takes the same clocks as before. Round 2 changed only its comments (the sv2v output is byte-identical); round 3 changes no RTL. |
| Contract | No register, field, ring, rate figure or version change: `RATE_DROP` ("frames the channel's rate limiter refused") counts the frames refused behind a held one. `gen_mailbox.py --write` leaves `KL_mbx_pkg.sv`, `KL_mbx.sv` and `mbx_contract.h` byte-identical and moves only `docs/reference/MAILBOX_CONTRACT.md`: its filter sentence describes the hold, and its channel table now derives each channel's held-record ingress allowance from `mailbox.yaml`'s `refill_ms` (adp 11 ms, acmp 6, aecp 6, maap 21, srp 3). It also keeps the written columns of FR_NFR.md 3.4.1's response-margin table (round 3, [`mailbox_margins.py`](../sw/mailbox/mailbox_margins.py)). |
| Ingress allowance | Per path ([FR_NFR.md 3.4.1](../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)): a record that finds a token keeps its 1 ms (published within 64 clocks of its last byte); a held record's is one refill period of its channel plus that 1 ms, 6 ms on AECP. Every response margin is computed at both: ACMP 178 / 173 ms (188 / 183 at the 10 ms proposal), AECP 218 / 213 (228 / 223), AECP at the controller's 250 ms timeout 228 / 223 (238 / 233), MVU 218 / 213 (228 / 223). No bound moves. Round 3: `gen_mailbox.py` writes the table's ingress and margin columns from each row's channel's `refill_ms`, and `--check` fails, naming the row, when one differs or a margin is not positive. |
| Scope | Generic: every channel of the table carries a rate and the buckets are per channel, so every channel holds its frame the same way. The committed rate is unchanged (every commit, held or not, spends one token), so is the load. The hold serves the one-in-flight workload; a second frame within the refill period (a second controller, a pipelined command, a response to this entity as a controller) is refused and counted. |
| Fabric host model | `sw/firmware/ctrl/host/mbx_model.{c,h}` follows the RTL (a held record's words past `RX_HEAD`, committed by the refill), so the shared suite and the co-simulation keep grading the RTL and the model with one set of expectations. It is compiled into no firmware image. |
| Mailbox tests | `tb/verilator/mbx`: T0, T1, Q10 and V0 graded for the ruling; group `HeldNotDropped` (B0 to B4, B7 to B9) on the RTL through both adapters and on the host model, B5 and B6 on the RTL at the clock; eleven planted defects, nine with two of them also run through AXI4-Lite (`rx-drop-instead-of-hold` in the default `make`); the model's twin in `ctrl_mutants.py`. `test_acmp_mbx.cpp`'s three ring-fill loops count committed records from `RX_PASS` and wait out a held one; their expectations are unchanged. |
| CPU budget harness | `tb/verilator/ctrl_service_budget`: the hold and the held commit observed passively (`hold_w`, `rel_w`: `RXH` and `RXR` lines); a held record's commit credited to its own frame ([`held.py`](../tb/verilator/ctrl_service_budget/held.py)), never to a frame ended since or another channel's, with a commit following no hold, a second hold, a commit outside the allowance, a commit stamped at or before its hold and any other commit on the channel while it holds one (round 3) refused, and a record never committed not served; group `aecp-held` measures a READ_DESCRIPTOR sent into an empty bucket from its last byte, so its ingress delay counts against the AECP row's bound; the flip's 8x8/1if point (`--point 8x8-1if`). |
| Docs and CI scope | `docs/design/MAILBOX_SPLIT.md` ("The held frame": where it waits, when it is committed, its ingress allowance, what is dropped, its limit; the verification table's counts), `docs/reference/FR_NFR.md` 3.4.1, both benches' READMEs, the Makefile's target list; round 3: `scripts/ci_scope.py` holds FR_NFR.md as a page gated code reads, and `docs/testing/CI_WORKFLOWS.md` says so. |

New mailbox checks and the planted defect each catches (failing words in quotes):

| Check | What | Planted defect |
|---|---|---|
| B0 | fifty AECP READ_DESCRIPTORs, one in flight, each at line rate as the one before it is delivered: all delivered, in order, byte for byte; the burst at once, every later one by the next refill (the bench's deadline); nothing counted, no ERR | `rx-drop-instead-of-hold`: "B0 fifty AECP commands, each sent at line rate as the one before it is delivered, are all delivered" |
| B1 | three commands back to back on one token: the first at once, the third (behind the held second) dropped and counted in `RATE_DROP` with ERR, the second at the next refill, the third never | `rx-hold-behind-a-held-frame`, `rx-next-frame-over-the-held-record` |
| B2 | a controller at one command a millisecond, one in flight: none of a hundred lost (the hardware finding) | `rx-drop-instead-of-hold` |
| B3 | a reset forgets a held frame; the bucket is full again | |
| B4 | a tail ahead of `RX_HEAD` inside the held record leaves no free word (`RX_DROP`), the held record committed whole once the tail is back | `rx-tail-inside-the-held-record-frees-space` |
| B5 (RTL) | a refill in the clock of each header word and the clock after commits the frame then, once | `rx-refill-in-the-header-clock-missed` (+`-axil`) |
| B6 (RTL) | over every clock of every check, no channel holds a frame while its bucket holds a token | the same |
| B7 | a ring filled to room for one record, which the held one takes: the frame behind it counts in `RX_DROP`, not `RATE_DROP`; every unread record and the held one byte for byte | `rx-space-from-the-committed-head` (+`-axil`): "B7 with the ring holding room for one record, the held one takes it: the next frame counts in RX_DROP" |
| B8 | behind a held one, a command for another target, a frame cut inside `target_entity_id` and a 14-byte stub: counted nowhere, no ERR; the held record then committed whole | `rx-refused-behind-held-counted`: "B8 a frame the filter refuses behind a held one counts nowhere" |
| B9 | a frame held when `FILTER_EN` closes its channel: committed whole at the next refill; nothing more taken or counted | `rx-release-gated-on-open`: "B9 a frame held when its channel closes is still committed at the next refill" |
| T0, T1 | the burst passes, the frame past it is held (not committed) until the next refill, whose commit moves `RX_HEAD` over it; it keeps its arrival NOW_MS and spends that refill's token; only the frame behind it counts | `rx-held-record-never-committed`, `rx-bucket-never-drains`, `rx-refill-slow` |

Evidence, every run on a clean clone (the receipts' index lists each file):

| Gate | Head | Result |
|---|---|---|
| `make -C tb/verilator/mbx` | `394612c5` | `mbx`: 622 Wishbone, 667 AXI4-Lite, 32 co-simulation, 629 and 674 at two interfaces, 547 on the host model, 0 failures; 13 of 13 quick mutants; the mover 520,041 checks, 24 of 24 mutants |
| `test_ctrl_firmware.py --require-rv32` | `394612c5` | `test_ctrl_firmware: PASS` |
| `make -C tb/verilator/mbx mutants` | `394612c5` | 242 of 242 planted defects caught by their named checks, after four positive controls |
| `gen_mailbox.py --check`, `--crosscheck`, `--selftest`; `ci_scope.py --selftest` | `394612c5` | 0 findings; the self-test's margin arms each named and the regenerated rows moved, 0 arms failed; the scope self-test PASS, FR_NFR.md held as gate-read |
| Probe P1 (R845-2 F1): AECP `refill_ms` 5 -> 10 in a disposable clone | `394612c5` | `--check` fails on the three AECP rows before `--write`; after it they read 11 ms and 208/218/208 ms, and every gate is clean |
| Local gates: lint, docs_check, doc paths, em-dash, Python/C++/SV/shell idioms | `394612c5` | all pass, each idiom count at its ratchet |
| docs, rtl-fast `changes`, rtl `full-ci-gate` and the elaborate gate jobs, step by step | `394612c5` | 77 steps rc 0, 49 not run with a stated reason (hosted orchestration, installs this host already has), 0 bad |
| CPU budget harness self-test | `394612c5` | `self-test: 0 failures`, 216 planted defects caught (214 at `8f73ade5`, plus the two ordering guards removed) |
| CPU budget harness, `aecp-held`, 8x8 (two interfaces) | `394612c5` | measured 5.310 ms from the held frame's last byte, ingress 4.986 ms of its 6 ms allowance, within the 20 ms bound; 0 refusals, 0 misses, no stated-cost line |
| `aecp-held` at 1x1 and 8x8/1if, the no-hold `aecp` control at 8x8/1if, and the 94-group 1x1 population of `cec88385` and `84d8a214`, regraded by the round-3 grader | recorded at `8f73ade5`, `cec88385`, `84d8a214` | every `table.md` and every group grade byte-identical to its recorded run (1, 1, 1, 94 and 94 groups); 0 refusals; the population's 7 pre-existing misses |
| RTL, firmware, contract | `394612c5` against `8f73ade5` | `hdl/`, `sw/firmware/`, `configs/`, `mailbox.yaml` and the generated package, skeleton, header and reference page are the same git trees and blobs; `hdl/` has been unchanged since `8f73ade5`, whose `KL_mbx_rx.sv` lowers byte-identically to `3926c271`'s |
| Firmware images | `394612c5` against `cec88385` | byte-identical: 46 fixture images (every config, one and two interfaces, flat and split, the ledgered 8x8/2if), and the split platform images 1x1/1if (`bb04b696...`, 145,496 B) and 8x8/1if (`506a1ae4...`, 158,176 B) with their ROM bank images and constraints |
| CPU budget harness, `aecp-held`, 1x1 and 8x8/1if (round 2) | `8f73ade5` | 5.236 ms and 5.114 ms, each with 4.986 ms ingress of 6, within 20 ms; at 8x8/1if three stated-cost lines of the point, not of #917 (Known limitations) |
| Verilator sweep, all suites, as four native shards (round 1), and its shard 1/4 again (round 2) | `84d8a214`, `8f73ade5` | 65 of 65; 17 of 17 |
| rtl-fast, elaborate, docs and the rtl yosys jobs, every job (round 2) | `8f73ade5` | 139 steps rc 0, 226 not run with a stated reason, 0 bad; firmware control mutants 699 of 699 |
| AX7101 split image, S9's recipe, three directives (round 1) | `3926c271` | best AltSpreadLogic_high: WNS +0.203 ns, WHS +0.036 ns over every corner, 0 failing endpoints (ExtraTimingOpt +0.063 / +0.036 also meets; ExtraPostPlacementOpt +0.202 / +0.016 misses the #870 +0.030 hold floor); the base met that floor on none; the RTL logic is unchanged since |
| Area, placed, against the base's route (round 1) | | LUT +74 to +181 by directive, FF +75/+76, LUTRAM 0/+1, BRAM (78.5 tiles: 60 RAMB36, 37 RAMB18) and DSP unchanged; `KL_mbx_rx` +124 to +133 LUT, +77 FF |
| Split boot (round 1) | `84d8a214` (RTL logic and firmware equal at `394612c5`) | 1x1 and 8x8 PASS |

## Round 2

Both round-1 reviews at `3926c271` were NEGATIVE: R845-1 ([PR comment](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6899723183)) and R846-1 ([PR comment](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6899591157)). Every finding is answered in `8f73ade5`; lines below are at that head. R846-1 F2 is implemented as the manager ruled for round 2: the ingress allowance per path, stated once and derived from `refill_ms`, every margin recomputed, the grader's attribution fixed, a held-record scenario at 1x1 and 8x8/1if with a negative control caught by name, and no bound changed.

| Finding | Closed by | Verification |
|---|---|---|
| R845-1 F1 (MINOR; Tests, Robustness, Docs): the free space past a held record has no check that can fail | B7, `tb/verilator/mbx/suite.hpp:1652-1692` (`check_held_space_and_refusals`, called from `check_held_not_dropped` at `:1645`): records fill the AECP ring to room for one more, the held record takes it, the frame behind it counts in `RX_DROP` and not `RATE_DROP`, every unread record and the held one byte for byte. Arm `rx-space-from-the-committed-head` (+`-axil`), `tb/verilator/mbx/mutants.py:679`, plants the space from `RX_HEAD`. The `rx-tail-inside-the-held-record-frees-space` row now says what it plants, `tb/verilator/mbx/README.md:452` (the guard on a tail ahead of `RX_HEAD` dropped, the space read from the write head alone); its new arm's row `:453`. | B7 green through both adapters and on the host model; both arms caught by "B7 with the ring holding room for one record, the held one takes it: the next frame counts in RX_DROP" (got 0, expected 1); `make mutants` 242 of 242 |
| R845-1 F2 (MINOR; Tests, Robustness): no filtered frame and no runt behind a held one | B8, `suite.hpp:1694-1720`: behind a held record, a command for another target, a frame cut inside `target_entity_id` (22 bytes) and a 14-byte stub; `RATE_DROP`, `RX_DROP` and the mismatch count stay 0, no `IRQ_STATUS.ERR`, the held record committed whole. Arm `rx-refused-behind-held-counted`, `mutants.py:683` (`rule_pass_w` dropped from `vd_rate_r`). | B8 green on both adapters and the model; the arm caught by "B8 a frame the filter refuses behind a held one counts nowhere" (got 2, expected 0) |
| R845-1 F3 (MINOR; Tests, Robustness): the close-with-a-frame-held behaviour is not graded | The documented behaviour is kept (`docs/design/MAILBOX_SPLIT.md:296-299`) and graded: B9, `suite.hpp:1722-1745`, closes the channel with `FILTER_EN` while a frame is held; it waits for the refill, is committed whole at it, and the closed channel then takes and counts nothing. Arm `rx-release-gated-on-open`, `mutants.py:687`. | B9 green on both adapters and the model; the arm caught by "B9 a frame held when its channel closes is still committed at the next refill" (got 16, expected 17) |
| R845-1 R1 and R846-1 R1 (residue; Docs): an issue-comment ID in source comments | `KL_mbx_rx.sv:39`, `mailbox.yaml:1098`, `suite.hpp:785` and `:1544`, `mutants.py:647` now read "#917; #665 ruling item 2" or "#665 ruling item 2"; the reasons stay. | `git diff cec88385..8f73ade5` adds no line carrying `6894152131`; no source file in the tree carries it |
| R845-1 R2 (residue; Docs): "What is dropped" overstates | `MAILBOX_SPLIT.md:306-311`: "every later frame of the channel that passes the filter and fits finds no token and is refused, in `RATE_DROP`"; one the filter refuses is dropped uncounted, one that does not fit counts in `RX_DROP`. The RTL header (`KL_mbx_rx.sv:46-49`) and `mailbox.yaml`'s filter comment say the same. | B8 (counted nowhere) and B7 (`RX_DROP`) grade both cases |
| R845-1 S1 (suggestion; Conformance, Docs): state the limit of the one-in-flight reading | Taken: `MAILBOX_SPLIT.md:312-317` ("Its limit"): once the burst is spent and a frame is held, any second frame of the channel within the refill period is refused and counted, naming a second controller, a pipelining controller and a response to this entity as a controller; it does not admit fifty commands sent with no wait. Also in Known limitations below. | B1 grades the refusal and its count |
| R846-1 F1 (MINOR; Conformance, Docs): one in flight attributed to 9.2.2.4; the bench deadline called a timeout | One in flight is now #917's measured workload, not a protocol restriction; pipelining is permitted (9.2.2); timeout and retry are cited as 9.3.2.6 and 9.3.6: `KL_mbx_rx.sv:38-43`, `MAILBOX_SPLIT.md:277-281`, `suite.hpp:393-400` (B0's deadline is next-refill delivery, not the 250 ms timeout), `suite.hpp:1544-1549`, this PR's Description and references. 9.2.2.4 is cited only for the message_type field (filter table rows, unchanged). | B0, B1, B2 and `rx-drop-instead-of-hold` unchanged and green (caught by B0 by name); the clauses checked against IEEE 1722.1-2021 |
| R846-1 F2 (MAJOR; Conformance, Tests, Docs): the held path invalidates the published ingress allowance and the budget harness's attribution | **Allowance**, stated once: [FR_NFR.md 3.4.1](../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing) (`docs/reference/FR_NFR.md:422-438`), per path: a token record keeps 64 clocks / 1 ms, a held record one refill period of its channel plus 1 ms; [MAILBOX_SPLIT.md "Its ingress allowance"](../docs/design/MAILBOX_SPLIT.md#the-held-frame) (`:300-305`) points there. The per-channel figure is generated, never mirrored: `sw/mailbox/mailbox_emit.py:217-231` derives it from `refill_ms` into `MAILBOX_CONTRACT.md`'s channel table. **Margins**: `FR_NFR.md:429-434` gives every response row, token and held, at the bound and at the 10 ms proposal (ACMP 173/183, AECP 213/223 and 223/233, MVU 213/223 held); no other margin subtracts ingress. **Attribution**: `tb/verilator/ctrl_service_budget/held.py:33-70`: a hold (`RXH`) binds the frame just ended to its channel; the channel's commit (`RXR`) is credited to that frame, never to a frame ended since (refused or filtered) or another channel's; a commit on a channel holding none (a duplicate or another channel's), a second hold, a commit before its frame's last byte or past the allowance (misordered or late) are refused, and a record never committed (missing) is not served. `grade.py:149-170` (`last_frame`, `owner`), `:199`, `:266`, `:364`, `:480`, `:618`; `observe.vlt:41-42`, `sim_main.cpp:120-124`, `build.py` (the `rx_hold` and `rx_release` accessors). **Scenario**: group `aecp-held`, `held.py:88-119`: sixteen AECP frames the core ignores empty the bucket just after a refill, then a READ_DESCRIPTOR is held, followed by a command for another target (filtered) and one from a second controller (refused); the probe starts at the held frame's last byte (`rxh:2`). **Negative control**: `selftest_mutants.py:446` restores the old rule (the commit to the last frame ended). | Self-test (`selftest_held.py`): nine checks, among them "a held record's commit belongs to its own held frame, measured from its last byte" and "the frame refused behind a held one is not credited with its commit"; the old rule caught by name by the first; `self-test: 0 failures`. On the real logs, 1x1 and 8x8/1if: the held record credited to the probe, the two followers refused, and the old rule refusing the log ("the receive commit at 100500065 follows no frame"). Rows: 1x1 5.236 ms, 8x8/1if 5.114 ms, each with 4.986 ms ingress of its 6 ms allowance, both within 20 ms; no bound changed. The 94-group population's recorded `cec88385` and `84d8a214` logs regraded byte-identical; `gen_mailbox.py --check`, `--crosscheck` and `--selftest` pass |

For the reviewers' ledger: `KL_mbx_rx.sv` changed in comments only at `8f73ade5` (sv2v output byte-identical to `3926c271`, where both reviews found the RTL lens CLEAN); whether that coverage stands is the reviewers' call. Every other lens's artifacts changed.

## Round 3

Both round-2 delta reviews at `8f73ade5` were NEGATIVE, each with one MINOR: R845-2 ([PR comment](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6903179473)) and R846-2 ([PR comment](https://github.com/kebag-logic/milan-fpga/pull/918#issuecomment-6903058735)). Every finding is answered in `93163957` and `394612c5`; lines below are at `394612c5`. No RTL, firmware, contract figure, bound or budget changed.

| Finding | Closed by | Verification |
|---|---|---|
| R845-2 F1 (MINOR; Conformance, Docs, Tests): FR_NFR's held allowance and held margins are an unchecked copy of the generated figure | Generated, the remedy the review preferred. The margin table sits between `<!-- response-margins:start -->` and `<!-- response-margins:end -->` (`docs/reference/FR_NFR.md:432-439`). Each row states its deadline, its channel (a new column, `acmp` or `aecp`), its timeout, bound and `T_egress`; the header states the 10 ms proposal. [`sw/mailbox/mailbox_margins.py`](../sw/mailbox/mailbox_margins.py) writes the other six cells (`:54-68`): the token `T_ingress` (`T_INGRESS_MS`, the channel table's own), both token margins, the held `T_ingress` (the row's channel's `refill_ms` plus 1 ms) and both held margins. Its `findings()` (`:90-105`) names every row whose written cells differ, and every margin that is not positive. `gen_mailbox.py --check` runs it (`sw/mailbox/gen_mailbox.py:180`) and `--write` rewrites the cells (`:183-199`). The sentence the review cited at `:425` is replaced by `FR_NFR.md:425-430`, which describes this mechanism. `--selftest` (`gen_mailbox.py:489-520`) names a hand edit of a held cell, a rate change nobody regenerated, a margin that is not positive and a row naming no channel; it also regenerates with AECP's `refill_ms` 5 ms longer and requires only AECP's held cells to move, by those 5 ms. `scripts/ci_scope.py:65-66`, `:75` and `:295` hold FR_NFR.md as a page gated code reads; its self-test refused the change until they did. `docs/testing/CI_WORKFLOWS.md:208-211` and `docs/design/MAILBOX_SPLIT.md:305-307` say so. | P1 rerun on a disposable clone of `394612c5` with `refill_ms` 5 -> 10. Before regenerating, `--check` fails on each of the three AECP rows ("reads 1 ms / 218 ms / 228 ms / 6 ms / 213 ms / 223 ms, the contract gives 1 ms / 218 ms / 228 ms / 11 ms / 208 ms / 218 ms"). `--write` moves them to 11 ms and 208, 218 and 208 ms (218, 228 and 218 at the proposal) and leaves ACMP's row as it was; then `--check`, `--crosscheck` and `docs_check` are clean. A hand edit of a regenerated cell is named. At the unchanged head the figures are as published and every gate passes; `--selftest` 0 arms failed |
| R846-2 F1 (MINOR; Tests, Robustness): commit-order validation remains incomplete | Two guards in [`held.py`](../tb/verilator/ctrl_service_budget/held.py). `overtaken()` (`:42-47`) refuses a commit (`RXC`) on a channel while it holds a record: that is a later frame overtaking it, which `KL_mbx_rx` cannot produce, since it refuses every passing frame of a channel holding one at its verdict. `follows_hold()` (`:50-54`) refuses a held record's commit stamped at or before its hold, since a refill commits only a record held in an earlier clock. `commit()` (`:57-61`) applies the first to every `RXC` (`grade.py:196`), and `release()` (`:64-77`) the second to every `RXR`. Other channels commit as before. Standing controls in `selftest_held.py:72-94`: both of the review's histories are refused; a valid commit on another channel between the hold and its commit, and another channel's commit in the held record's own clock, are each credited to its own frame. `selftest_mutants.py:449-452` removes each guard. No RTL change, no budget relaxation | The review's `probe_attribution.py` against `394612c5` refuses both invalid histories by name ("overtakes the record it holds"; "does not follow its hold at 1070"); the valid held-and-follower and other-channel cases stay measured. Self-test: the 13 held checks pass. With `overtaken` removed, "a commit on the channel holding a record is refused: a later frame does not overtake it" fails; with `follows_hold` removed, "a held record's commit stamped before its hold is refused" fails. `self-test: 0 failures`, 216 planted defects caught. The recorded `aecp-held` logs, the no-hold control and the 94-group population all regrade byte-identically |
| R845-2 R1 and R846-2 R1 (residue; Docs): bench labels in a source comment | `tb/verilator/mbx/suite.hpp:1648-1650` now reads as both reviews' exact fix; the check names stay | No comment line added in `cec88385..394612c5` carries a bench label; the mailbox suites and `make mutants` pass as before |
| R845-2 R2 (residue; Docs): the population bullet's reason | Known limitations, the CPU budget harness bullet, now gives the review's reason word for word | |
| R845-2 S1 (suggestion; Tests): `aecp-held` at the two-interface 8x8 point | Taken: run at `8x8` (two interfaces) at `394612c5`: 5.310 ms, ingress 4.986 ms of 6, within 20 ms; 0 refusals, 0 misses, no stated-cost line. `aecp-held` has run at 1x1, 8x8/1if and 8x8 | Receipts |
| R845-2 S2 (suggestion; evidence): the author-r2 INDEX is stale for four files | Round 2's INDEX matches all 430 of its files as handed over; the four workflow logs differ only in the published copies. Round 3's INDEX is generated last, after the last sanitizing pass | |
| R845-2 S3 (suggestion; Docs): say that the held row's figure already contains its ingress | Taken: `FR_NFR.md:444` and the harness README (`tb/verilator/ctrl_service_budget/README.md:396`) | |

For the reviewers' ledger: since `8f73ade5`, `hdl/`, `sw/firmware/`, `configs/`, `mailbox.yaml` and every generated contract output are unchanged (the same git trees). The changed artifacts are the mailbox generator and FR_NFR's margin table, the CPU budget grader and its self-test, the CI scope table, one `suite.hpp` comment and the documentation.

## Authoritative references

- #917 (acceptance) and the ruling on #665, issuecomment-6894152131, item 2 (the default implemented here); the manager's ruling on R846-1 F2 for round 2 (a per-path ingress allowance; its terms are restated in the Round 2 section).
- IEEE 1722.1-2021 9.2.2 (a controller may pipeline commands), 9.3.2.6 (the 250 ms timeout; respond within 240 ms) and 9.3.6 (the controller's in-flight commands, timeout and retry).
- [REQUIREMENTS.md section 1](../REQUIREMENTS.md#1-product-ownership) and NFR-SCOUT-02/08 ([FR_NFR.md 3.4](../docs/reference/FR_NFR.md#34-fabric-scale-out-and-future-ports)): per-channel token buckets remain in force; they do (the committed rate is the table's).
- [FR_NFR.md 3.4.1](../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing): `T_ingress` per path and the response margins, whose ingress and margin columns `gen_mailbox.py` writes.
- `sw/mailbox/mailbox.yaml`: the rate table, `RX_TAIL` (a value ahead of `RX_HEAD` leaves no free word), `RATE_DROP`.
- [docs/design/MAILBOX_SPLIT.md, The held frame](../docs/design/MAILBOX_SPLIT.md#the-held-frame); [the CPU budget harness, A held record](../tb/verilator/ctrl_service_budget/README.md#a-held-record).

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git && cd milan-fpga
git fetch origin 917-aecp-hold && git checkout --detach 394612c5
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the pinned Verilator 5.050 on PATH (or VERILATOR=), the pinned RV32 SDK for the firmware gate (MILAN_RV32_CC=);
# for the CPU budget harness, its README's prerequisites (the LiteX environment, the RV32 SDK, offline sbt)
```

## How to validate

```sh
make -C tb/verilator/mbx                 # both adapters, co-simulation, two interfaces, host model, 13 quick mutants, the mover
make -C tb/verilator/mbx mutants         # every planted defect, after the positive controls
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
python3 -B sw/mailbox/gen_mailbox.py --check --crosscheck
python3 -B sw/mailbox/gen_mailbox.py --selftest
python3 -B scripts/ci_scope.py --selftest
python3 scripts/lint_rtl.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --groups aecp-held
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --groups aecp-held
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <dir> --groups aecp-held
```

Expected result / pass criteria: every command exits 0 but the 8x8-1if run, which exits 1 on the three stated-cost lines of that point (Known limitations) and on nothing else. The mailbox suite ends `checks: 622   failures: 0` (Wishbone), `667` (AXI4-Lite), `32` (co-simulation), `629` and `674` (two interfaces), `547` (host model), `mbx mutants: 13 of 13 caught`; `make mutants` ends `mbx mutants: 242 of 242 caught`; the firmware gate ends `test_ctrl_firmware: PASS`; `gen_mailbox.py` ends `gen_mailbox: 0 finding(s)` and `selftest: 0 arm(s) failed`, `ci_scope.py` `selftest: PASS`; the budget self-test ends `self-test: 0 failures`; each `aecp-held` run reports `1 groups graded, 0 refusals, 0 budget misses`, and its `results.json` row `aecp.held.read_descriptor.if0` is `measured`, `within_budget`, with `ingress_ms` under `ingress_allowance_ms` (6.0).

## Known limitations / out of scope

- The on-hardware acceptance (three descriptor walks with none unanswered) needs the test machine and is not run here; `Closes #917` should wait for it, or the Issue be reopened until the bench records it.
- Printing the drop counters on the console waits until after the flip (ruling item 2); `RATE_DROP` is readable now.
- The owner may still choose to flip with the limit documented instead (ruling item 2); this PR is the default.
- The hold serves one command in flight (MAILBOX_SPLIT "Its limit"): a second AECP frame within the refill period, from a second controller, a pipelining controller or a response to this entity as a controller, is refused and counted in `RATE_DROP`.
- A frame held when its channel is closed is still committed at the next refill (B9): it passed the filter while the channel was open, as a frame committed just before the close did.
- At 8x8/1if the harness's stated-cost check reports three MRPDU build passes during link-up over `ctrl_loop.h`'s one-interface stated costs, which `MBX_N_IF` alone chooses (the 1x1 figures): 120,704 and 117,875 CPU cycles against 101,000, and a build-one pass of 95,723 against 43,000. The existing `aecp` group, which holds nothing, reports the same three at the same cycles, so they belong to the point, not to #917; every row of both groups fits its bound. No cost or bound is changed here; they are for #914's 8x8/1if measurement.
- `gen_mailbox.py --check` runs in no hosted job ([CI_WORKFLOWS.md](../docs/testing/CI_WORKFLOWS.md): "No `docs-check` step runs it"), for FR_NFR's margin table as for MAILBOX_CONTRACT.md before it: it is a local gate, in How to validate above. A hosted job running it is a CI change of its own; worth an Issue.
- `aecp-held` has run alone at 1x1, 8x8/1if and 8x8; it is part of every point's population, which no run here has repeated.
- The fabric host model and three host-test loops live under `sw/firmware/ctrl/` but are not firmware image sources; every firmware image is byte-identical to the base's (see Status).
- The CPU budget harness is not a CI gate. Its 94-group population was not rerun: the round-2 and round-3 graders regrade the recorded base and head logs byte-identically, and none of them holds a record (the base, which drops a frame its bucket has no token for, and `84d8a214`, which holds it, recorded byte-identical logs for all 94 groups, so no frame of the population met an empty bucket). It cites MAILBOX_SPLIT.md by line number in places, already stale at the base; worth an Issue of its own.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench criteria here; the hardware walks remain)
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
