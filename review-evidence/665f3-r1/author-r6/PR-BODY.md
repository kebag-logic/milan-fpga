[A559]

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

GREEN at `13e715136b0b7c8d9763e0b730d9709f2c9f5932` (round 6, #665 comment 6037650104), for review. Round 6 merges dev
`e21c1ca0` (lane F2's MAAP core, #687) with `--no-ff`, both sides kept, and composes ADP, ACMP
and MAAP in one app. The composed image with MAAP and ACMP both linked takes 46,608 of 131,072
bytes (35.6 %) at the shipping shape and 56,980 (43.5 %) at the largest, +15,648 over dev.

- Round 6's gates, all rc 0:
  - the ctrl gate, all 16 arms (`acmp` 84 tests, `acmpif2` 22, `maap` 37 + 12, `maap_if2` 13,
    `maap_debug` 1);
  - the ctrl campaign, 465 of 465 (F3's 269 with round 6's 15, F2's 96, F0 and FC's 100);
  - the store gate (5 shapes, 435 tests); coverage, all 20 files at 100 % after exclusions;
  - the mbx suite: 382 and 427 checks, 384 and 429 at two interfaces, 369 on the model, 32 in
    the co-simulation, quick arms 5 of 5; the RTL campaign, 147 of 147;
  - the image self-test (33 checks) and the measurement; the RV32, SDK and tally self-tests;
  - 68 docs-workflow and idiom commands.
- No RTL, contract, register-map, builder or shipping-image change in round 6: the merge needed
  none.
- Not run: the store campaign (`test_ctrl_nvm.py --self-test`), which has no partition option
  and outruns the local memory cap; `sw/firmware/ctrl_nvm` and its tests are identical to dev's
  but for its README.

`665-f3-acmp` -> `dev`.

Round 3 (area) at `4f6216ab`: the term costs 357 LUT and 86 FF against a target of 300 and 120,
accepted as measured on #665 (6033962557). No RTL has changed since, so that figure stands.

dev `e21c1ca0` (F2 #687, after FC #685, #679 and #677) is merged here with `--no-ff`, so the
diff against `dev` is lane F3's alone.

## Linked Issue / roles

Relates to #665

Executor: `[A559]`
Internal cleared-context reviewer: `[R530]`
External reviewer: `[R531]`

## Description

Lane F3 of #665: Milan connection management (ACMP) on the bare-metal control core. Round 2
answers both round-1 reviews (R531-1 and R530-1, every finding accepted) and adds the `adp`
channel's bound-talker term decided on #665 (comment 6029368753). Round 3 makes that term cheap
(the area ruling, comment 6032450078). Round 4 answers R531-2 and R530-2 (comment 6034423349).
Round 5 answers R531-3 and R530-3 (comment 6036721467). Round 6 merges F2 (comment
6037650104).

**Round 6.** dev `e21c1ca0` (F2's MAAP core) is merged with `--no-ff`; the merge commit holds
both sides only, and the composition follows as its own commits.

| Item | What changed |
|---|---|
| Merge | Nine conflicted files, both sides kept: the README, `ctrl_app.c`/`.h`, `ctrl_arms.py`, `ctrl_build.py` (F2's `-DNDEBUG` kept; ACMP's host guard is `CTRL_REENTRY_ASSERT`), `ctrl_mutants.py`, `test_ctrl_firmware.py` (F2's `--mutation-shard` and F3's `--slice` both kept), the ratchet (re-measured) and the mbx `Makefile`. F2's positional `ctrl_app_config` initializers name ACMP's fields. |
| The composition | As merged, F2's `ctrl_app_start_maap` put MAAP on slot `MBX_N_IF`, ACMP's first, and rewrote the IRQ enable and the filter with ADP and MAAP only, dropping ACMP's channel. Now MAAP comes from the configuration like ACMP (`maap_allocation`, NULL for none, `maap_ctx`, `maap_preferred`), on its own slots after ACMP's (`CTRL_APP_MAAP_FIRST_SLOT`, a `_Static_assert` keeping the three runs in the bank). It attaches after ADP and ACMP, before the open, so `ctrl_loop_open()` enables every bound channel's receive interrupt with the events' and opens each at the filter. MAAP starts after the open. F2's preferred-range refusal is unchanged; the attach results are checked. `ctrl_app_start_maap` is `ctrl_app_start` with the three fields, and refuses a missing port. |
| Pass bound | `CTRL_APP_PASS_MAX` = `ACMP_MBX_PASS_MAX` + MAAP's share (8 x 48 + 2 x (20 + 48) + 48 per interface): 1,580 accesses at one interface, 1,659 at two. The design page scales the four backlog bounds by it: 0.57 us per access behind a full acmp ring and 0.28 us behind a full adp ring, for T_svc. |
| Tests | `test_acmp_mbx.cpp` in both ACMP arms. U6: the attach order, FILTER_EN and the IRQ enable exactly (adp, acmp, maap, events), disjoint slots each holding its own module's arm, a restored binding, MAAP acquiring over four seconds beside the other two. U7: the refusals (below the pool, past its end, the last range taken, no talker source, an ACMP refusal before MAAP attaches, the entry without a port), nothing touched. F6: events and the acmp and maap rings backlogged, worst pass 231 of 1,580 (233 of 1,659 at two interfaces). |
| Defects | 15 new (slots overlapping ACMP's or ADP's, MAAP attached after the open, before ACMP, started in the compose or never, its channel unbound, each refusal dropped or off its boundary, the entry taking no port or dropping its range, a MAAP handler overrunning the pass bound). 4 re-planted where the composition moved their text, each with its test and words: F0's pool bound after the mailbox, F3's ACMP never composed, and F2's MAAP interrupt and filter bit, now dropped in `ctrl_loop_open()`, which writes them. |
| Coverage | `ctrl_app.c` 42/42 lines and 40/40 branches. ACMP's attach-refusal exclusion re-keyed; MAAP's attach refusal added, with its proof. |
| Linked image | `image_main.c` composes MAAP on `maap_csr_allocation` beside ACMP; a base with MAAP only through `ctrl_app_start_maap` (dev) links through it. |

Linked RV32I image with MAAP and ACMP, pinned SDK (identity unchanged), against dev `e21c1ca0`
(ADP and MAAP, no ACMP, the same store):

```sh
MILAN_RV32_CC=<pinned SDK>/bin/riscv32-linux-gcc \
  python3 sw/firmware/ctrl/test/ctrl_image.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df
```

| Shape | IN / OUT | text | rodata | data | bss | total | of 128 KB |
|---|---:|---:|---:|---:|---:|---:|---:|
| `endstation_ax7101_1x1_tdm8` (shipping) | 2 / 2 | 33,444 (+10,768) | 748 (+32) | 0 (+0) | 12,416 (+4,848) | 46,608 (+15,648) | 35.6 % |
| `endstation_ax7101_8x8` (largest) | 9 / 9 | 33,448 (+10,768) | 748 (+32) | 0 (+0) | 22,784 (+4,848) | 56,980 (+15,648) | 43.5 % |

- Every image passes the audit: `rv32i2p1`, 8,361 and 8,362 words at the head, 5,669 and 5,670
  at the base.
- Helpers 508 bytes at head and base: MAAP's code adds `__umodsi3` and its 32-bit loop.
- The app is 7,904 bytes at every shape: ACMP 4,720, the loop 1,748, MAAP 1,104, the pool 204,
  ADP 124.

Round 5's table (39,716 and 50,088 bytes, against dev `d51b373a`) measured the app without MAAP;
round 6's supersedes it.

**Round 5.** R531-3-F1 / R530-3-F1 (MINOR): the round-4 linked image did not link with the
pinned SDK, and its toolchain was misattributed. The ruling: link with the pinned SDK, supply
the helpers and report them apart, audit the image as RV32I, regenerate the table and name the
toolchain.

| Item | What changed |
|---|---|
| Cause | The pinned SDK's `libgcc.a` has one multilib, `rv32imafd` with the `ilp32d` ABI (all 125 members: e_flags `0x4`), so it cannot link into a soft-float RV32I image. Round 4's figures came from another build at the CI install path on the measuring host, whose `libgcc` is soft-float but holds M instructions: 58 words per image, the first a `divu` in `__udivdi3` at `0x6b34`. |
| No library | `ctrl_image.py` links no library. The arithmetic helpers come from `test/rv32_image/image_arith.c`: all 13 integer helpers the `rv32` arm admits (it admits no floating-point one, so the firmware reaches none). Each is a shift-and-add or shift-and-subtract loop on RV32I. A helpers object that leaves a symbol open, or calls a helper, is refused before the link: GCC lowers `*` in `__mulsi3` into a call to `__mulsi3`, and turns 64-bit shift-and-add loops into calls to `__muldi3`. They are reported apart, like the runtime stand-ins: 412 bytes (`__lshrdi3`, `__muldi3`, `__mulsi3`, `__udivdi3`, `__umoddi3` and their divide loop). LiteX's `libcompiler_rt` supplies them in the SoC image. |
| Audit | Every image is audited before a figure is read, and any finding refuses the measurement. It must be a little-endian ELF32 RISC-V executable with e_flags 0: no RVC, the soft-float ILP32 ABI, not RVE or Ztso. It must carry one architecture attribute, `rv32i` and its version alone. Every word of every executable section must be an RV32I base instruction. No symbol the inputs reference may be undefined: a weak one links to address 0 and vanishes from the image, so the inputs are read. |
| Identity | `ctrl_image.py` prints it first. Pinned archive `riscv32-ilp32d--glibc--stable-2025.08-1` (`scripts/ci_rv32_sdk.py`, sha256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`). Version line `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`. `libgcc.a` sha256 `d8ebca8cf6ad31cd50695f79e91e86a716d3b1761fbbefd5ee7b0627a2d0af58` (not linked). The README names the build by its revision, because the bare-metal gate refuses the version line's other words in tracked files. |
| Self-test | `ctrl_image_selftest.py --require-rv32`, 33 checks:<br>- the helpers against the host's own arithmetic (edges, every shift count, 200,000 random pairs);<br>- the leaf rule, and two helpers it refuses;<br>- a probe linked as the image is, and every RV32I instruction form, passing;<br>- refused: eleven foreign instruction words (M, C, Zifencei, Zicsr, A, F, privileged, a 6-bit shift, zero), an RV32IM attribute, ten foreign header fields, a weak undefined symbol;<br>- `measure()` at the shipping shape: passing as shipped; refusing an RV32IM soft-float helper library (by the audit), one built for the pinned SDK's own multilib (at the link), and a self-calling helper. |

Linked RV32I image, regenerated with the pinned SDK:

```sh
MILAN_RV32_CC=<pinned SDK>/bin/riscv32-linux-gcc \
  python3 sw/firmware/ctrl/test/ctrl_image.py --base d51b373a...
```

Every source is compiled with its gate's flags plus `-DNDEBUG` and linked with `--gc-sections`
into one 128 KB block-RAM region, with no library. Deltas are from dev `d51b373a`, measured
with the same harness (the app without ACMP, the same store):

| Shape | IN / OUT | text | rodata | data | bss | total | of 128 KB |
|---|---:|---:|---:|---:|---:|---:|---:|
| `endstation_ax7101_1x1_tdm8` (shipping) | 2 / 2 | 27,700 (+10,852) | 736 (+36) | 0 (+0) | 11,280 (+4,848) | 39,716 (+15,736) | 30.3 % |
| `endstation_ax7101_8x8` (largest) | 9 / 9 | 27,704 (+10,852) | 736 (+36) | 0 (+0) | 21,648 (+4,864) | 50,088 (+15,752) | 38.2 % |

- Every image passes the audit: `rv32i2p1`, with 6,925 and 6,926 words at the head and 4,212
  and 4,213 at the base, all RV32I.
- R531-3's own `elf_audit.py` passes the four images (0 M/A instructions). It fails the four
  round-4 ones.
- A fresh, receipt-verified extraction of the pinned archive prints the same table, and its
  ELFs are byte-identical.
- Static objects are unchanged: the app 6,800 bytes at every shape (ACMP's state 4,720 at its
  maxima of 16 sinks, 16 sources and four interfaces); the store's stage 3,344 / 13,264, its
  payload 136 / 576, chunk 256 and state 288; and lwSRP's pool arena 256 (the host tests'
  declaration until F4 sizes it).
- The C runtime is linked from 64 bytes of stand-ins for libbase's. The stack is not counted.

**Round 4.**

| Item | What changed |
|---|---|
| Merge | dev `d51b373a` with `--no-ff`, both sides kept: #677's re-entry arms and `assert.h` with F3's ACMP arms and slices. Re-graded: the ctrl README counts thirteen arms (and lwSRP's), the harness page fifteen coverage exclusions, every one resting on a public header. |
| R531-2-F1 (MAJOR) | TMR_NO_RESP starts from a clock read after the port accepts the probe, for the probe and its duplicate, immediate or owed, even when the entry read the clock before (a timer expiry's), per Milan v1.2 5.5.3.5.3 steps 5 to 7 and 5.5.3.5.16 steps 1 and 2. An expiry's due tests read the latest clock, so a 0 ms TMR_DELAY still probes in the same expiry. FIFO order, the sequence ID, the single duplicate, cancellation and rebind, and the lost-probe policy are unchanged. A30 (three tests, a fake clock that moves inside each send) with three planted defects; the reviewer's four tests pass (two of them fail at `4f6216ab`). The extra clock read is one access: the timer-to-probe paths cost 35 (was 34), a pass 1,012 (was 996), and the backlog bounds move by 1.6 %. |
| R530-2-F1 | Q22: on each interface, a bound talker's ENTITY_AVAILABLE with another talker's frame on another index right behind it passes alone; Q23: with two interfaces, the owed copy gates each interface's own entries. Planted defects for both, through both adapters: the verdict's table from the presented `rx_if_i` (one and two interfaces) and every interface gated by interface 0's owed flags. |
| Linked image (R531-2-F2, R530-2-F2; 6030870481) | `ctrl_image.py` links the composed app (with the binding owner and F1's store on the LiteSPI port) for RV32I at the shipping and the largest shape and measures it against dev; see below. |
| R530-2-F3, R1 to R3 | The design doc's open item takes its access times from the table (now 0.89 us); the reviewer's exact texts for the area item, the contents line and this body; two more stale mentions of the decided term corrected. |

Round 4's linked-image table (42,100 and 52,472 bytes) is superseded by round 5's. It was
attributed to the pinned SDK but was linked with another build's `libgcc`, and that image was not
RV32I (R531-3-F1, R530-3-F1).

**Round 3 (area).** The behaviour is unchanged; the RTL changes only inside the mailbox block.

| Item | What changed |
|---|---|
| The table in distributed RAM | `KL_mbx_rx` holds the bound-talker tables: the host's `BOUND_EID` words in a read-back memory (32 x 32, six RAM32M), and each entry's eight identity bytes in a shift register of its own (SRL16E), byte b at tap b. The 1,040 flip-flops of round 2 are gone. |
| Byte-serial compare | As wire bytes 18 to 25 arrive, identity byte b is compared with byte b of every entry of the arrival interface's table: one 8-bit compare per entry per byte and one match flag per entry, armed by the first byte. The decision point is where it was. |
| The copier | Setting `BOUND_EN`, or writing a `BOUND_EID` word while it is set, owes the entry a copy; the copier shifts its eight bytes in from the read-back memory, one byte in each cycle the host leaves that memory, and starts over on a rewrite. An entry takes part only while `BOUND_EN` is set and no copy is owed, from its first identity byte to the verdict, so a frame whose identity passes a rewrite never matches it. Derived from the RTL: at most 176 clocks for all sixteen entries of an interface, plus a clock per host access to the tables. |
| Reset | Distributed RAM keeps its contents through a reset, so a flag per word makes a `BOUND_EID` word not written since the reset read 0 and copy as 0: the contract's reset value holds. |
| Skeleton | The generator decodes a bound-talker register's interface, entry and register by bit fields (refusing strides that are not powers of two) and passes them to `KL_mbx_rx`; the skeleton reads `BOUND_EID` back only while it is valid. The generator also refuses `eq_bound` terms on two fields. `KL_mbx_pkg.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md` and the YAML are unchanged. |
| Tests | Q14 to Q17 in the shared suite (frames in a row, each identity byte, a rewrite with `BOUND_EN` set, a reset), on both adapters, at two interfaces and on the model; Q18 to Q21 on the RTL only (a frame stalled inside its identity, reads beside a copy, a rewrite at each of 32 clocks). The 12 round-2 RTL defects are planted on the lines that now carry them, with 18 new ones, among them the two the ruling asked for: a wrong byte index and a stale match flag across frames (two forms). |

Out-of-context area, the round-2 recipe (`KL_mbx` behind `KL_mbx_wb`, `xc7a100tfgg484-2`, 10 ns,
placed and routed, under the shared lock): 3,102 LUT and 2,946 FF against FC round 2's 2,745 and
2,860, WNS +0.402 ns, all 6,041 nets routed. The term costs 357 LUT and 86 FF: 64 LUT of shift
registers, 22 of read-back memory and 271 of logic. Two measured variants show what the rest
buys, each a contract change: `BOUND_EID` not cleared by a reset, +337 LUT and +56 FF; that and
`BOUND_EID` write-only, +300 and +56.

**Round 2.**

| Item | What changed |
|---|---|
| The `adp` term | Contract 2.1 (`sw/mailbox/mailbox.yaml`, through the generator only): the adp channel's third accept term `eq_bound` (message types 0 and 1, entity_id at byte 18) admits ENTITY_AVAILABLE and ENTITY_DEPARTING of a talker bound on the receiving interface. It reads a per-interface bound-talker table in the mailbox block (16 entries, one per listener stream: `BOUND_EID_LO`, `BOUND_EID_HI`, `BOUND_EN`). `KL_mbx_rx` compares the captured entity_id with the enabled entries of the arrival interface's table; `KL_mbx` and `KL_mbx_pkg` are regenerated; the host model does the same. The core's new `admit` port keeps the table equal to each bound sink's talker; `acmp_open`, called from `ctrl_app_open`, writes the bindings the store restored at boot. The contract's minor moves: a firmware built against 2.0 leaves the table empty. |
| R531-1-F1 (MAJOR) | Only AVTP version 0 is read: an ACMPDU or ADPDU of another version is discarded before it is decoded, in both receive paths (IEEE 1722-2016 4.4.3.4; IEEE 1722.1-2021 8.2.1.3, 6.2.2.3). |
| R531-1-F2 (MAJOR) | TMR_NO_RESP runs 200 ms from the send the transmit ring accepts, for the probe and its duplicate: an owed probe holds its timer until it leaves, matched by sink and sequence_id, so command order, the single duplicate and its sequence_id are kept (Milan v1.2 5.5.3.5.3 steps 5 to 7, 5.5.3.5.16 steps 1 and 2). |
| R531-1-F3 | The adapter's slot range is compared (`first_slot > MBX_N_TIMERS - MBX_N_IF`), never summed or narrowed. |
| R531-1-F4, F5 | The reviewer's corrections: the owed-frame bound fits T_svc at 1 us; `acmp_poll` sends at most one owed frame. |
| R530-1-F1 | A new arm, `acmpif2`, builds the adapter's tests with the firmware and the model on the contract's two-interface variant; B3, B4, B6, B8 and the C paths run per interface. |
| R530-1-F2, F3, F4 | Tests pinning the BINDING record byte for byte to the processor's payload one flag at a time and refusing other lengths; a D3 roll-back keeping the bindings (at the port and at a real boot); every connection timer, TMR_NO_ADP and the earliest-deadline choice across the 32-bit millisecond wrap. Each with planted defects. |
| R530-1-F5, R1 | TD1 recorded with the 5.5.2.7/5.5.4.2 tension and the ruling; "field for field" limited to LD1 to LD3; the decided term in place of "open decision". |
| Harness | `tb/verilator/mbx` `run-cosim` rebuilds the firmware library on any header change and relinks `Vmbx_cosim` whenever the library is newer. |

Evidence for the term: the suite's Q12 and Q13 on both adapters, at two interfaces and on the
model; 24 planted RTL defects (12 rules, both adapters); H-DISC measured from the adp channel's
`RX_HEAD`, the record committed by the model's filter (C10 35 accesses, C11 29; behind a full adp
ring filled through the filter, pass 13 of 26 records, 333 accesses against 21,912); and the
co-simulation, where the bound talker's ENTITY_AVAILABLE crosses the RTL's filter into discovery
on both fabrics frame for frame. Out-of-context area: 4,025 LUT and 3,907 FF against FC round 2's 2,745 and 2,860 (`KL_mbx` behind `KL_mbx_wb`, `xc7a100tfgg484-2`, 10 ns, placed and routed, WNS +0.283 ns); the term costs 1,280 LUT and 1,047 FF, 1,040 of them the table's flip-flops. Building the entity_id comparators only for the `eq_bound` term (a constant of the term) saved 862 LUT over the first version.

Planted defects: 348 in the ctrl campaign (F3's 251: `acmp_mutants.py`, round 2's 56 in
`acmp_review_mutants.py`), 105 in the RTL campaign. The reviewers' probes replayed at the head:
R530-1's six escaped probes are caught (X3 on the two-interface arm); R531-1's nine independent
probes pass at one and two interfaces.

**Round 1** (unchanged in kind): the core (`acmp.[ch]`: every Table 5.30 transition, the
talker's answers of 5.5.4, the discovery machine of Table 5.54, the lock, responses keyed on the
consumer's unique ID, one timer per interface, owed frames and #653, the #678 guard), the
mailbox adapter (`acmp_mbx.[ch]`), the binding owner on F1's store (`acmp_nvm.[ch]`), the
compose/open split, the processor's ACMP expectations walked in `acmpwalk`, and the docs.

Differences from the processor (processor issue #168): LD1 UNBIND_RX_RESPONSE's talker fields
(Table 5.36: 0), LD2 the ACMP status after TMR_RETRY with the talker discovered (5.5.3.5.30 step
2 sets none) and LD3 the lock refusal status (IEEE 1722.1-2021 Table 8-3: 16) are asserted field
for field against the processor's own model. TD1, DISCONNECT_TX of an unknown source, is
asserted on the firmware's half only (TALKER_UNKNOWN_ID, 5.5.4.2 step 1); the processor's SUCCESS
is read from source (`KL_acmp_talker.sv:1301-1306`). Milan v1.2 5.5.2.7 says DISCONNECT_TX
"always returns SUCCESS"; 5.5.4.2 governs, because 5.5.2.7 is an overview that defers to 5.5.4
and 5.5.4.2 is the "shall" procedure.

## Authoritative references

- Milan v1.2 5.5 (5.5.2.2 to 5.5.2.7, 5.5.3.1 to 5.5.3.5.48, 5.5.4.1 to 5.5.4.4, Tables 5.22 to 5.48) and 5.6.4 (5.6.4.1 to 5.6.4.5.4, Table 5.54).
- IEEE 1722.1-2021 8.2.1 (Figure 8-1, Tables 8-1 to 8-4), 8.2.1.3 and 6.2.2.3 (version), 6.2.2.5 (valid_time units), 7.4.35; IEEE 1722-2016 4.4.3.4.
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2 (NFR-SCOUT-02/03/08, H-ACMP, H-DISC); REQUIREMENTS.md section 1 (the `adp` row).
- #665 comments 6029368753 (the term), 6030067436 (round 2 and the TD1 ruling), 6032450078 and 6033962557 (round 3, the area ruling), 6030870481 (the linked-size acceptance addition), 6034423349 (round 4), 6036721467 (round 5) and 6037650104 (round 6); the R531-1, R530-1, R531-2, R530-2, R531-3, R530-3, R530-4 and R531-4 reports.
- Lane F2's MAAP core (#687): `sw/firmware/ctrl/maap/README.md`; IEEE 1722-2016 Annex B (B.4, Table B.9, the pool).
- REQUIREMENTS.md section 1 and NFR-SCOUT-01 (RV32I); `scripts/ci_rv32_sdk.py` (the pinned SDK).
- `docs/design/MAILBOX_SPLIT.md`; `sw/mailbox/mailbox.yaml` (2.1); `docs/reference/MAILBOX_CONTRACT.md`.
- #653, #678; F1's saved-state store (`sw/firmware/ctrl_nvm/README.md`, `nvm_state.h`).

## How to get into the same state

```sh
git fetch origin
git checkout 665-f3-acmp
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install pyyaml
# GoogleTest and GoogleMock (libgtest-dev, libgmock-dev), a host C/C++ compiler,
# Verilator 5.050 on PATH, and for the RV32 arms the CI's RV32 SDK
# (python3 scripts/ci_rv32_sdk.py, or MILAN_RV32_CC).
# A local install of the pinned SDK, verified against its archive digest:
python3 scripts/ci_rv32_sdk.py --destination "$PWD/../rv32-sdk"
export MILAN_RV32_CC="$PWD/../rv32-sdk/bin/riscv32-linux-gcc"
```

Set `MILAN_RV32_CC` whenever the default destination of `scripts/ci_rv32_sdk.py` may hold another build.
`ctrl_image.py` prints the compiler's identity first, and with the pinned SDK it ends
`(Buildroot 2021.11-18033-g83947c7bb6) 14.3.0; libgcc.a sha256 d8ebca8c...af58 (not linked)`.

## How to validate

```sh
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
for k in $(seq 1 18); do
  python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice "$k/18" || break
done
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/ctrl_image.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df
make -C tb/verilator/mbx clean && make -C tb/verilator/mbx && make -C tb/verilator/mbx run-cosim run-if2
python3 -B tb/verilator/mbx/mutants.py --jobs 2
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 scripts/lint_rtl.py --check --self-test
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_sv_idiom.py
python3 scripts/gen_toc.py --check
```

Expected result / pass criteria: every command exits 0. The ctrl gate passes all 16 arms (`acmp`
84, `acmpwalk` 127, `acmpnvm` 7, `acmpif2` 22, `maap` 37 and 12, `maap_if2` 13, `maap_debug` 1
tests). Each campaign slice prints `mutants: 26 of 26 caught` (the last `23 of 23`) with no
`[ESCAPED]` line. Coverage reports every file 100 % after exclusions (`ctrl_app.c` 42/42 lines
and 40/40 branches, `acmp.c` 734/734 and 342/342). `ctrl_image_selftest.py` prints
`ctrl_image self-test: 33 checks PASS`. `ctrl_image.py`, with `MILAN_RV32_CC` set to the pinned
SDK, prints its identity, the round-6 table above, and for each shape the audit line
`RV32I audit: e_flags 0, rv32i2p1, ... words all RV32I base instructions, nothing undefined`. The
mbx suite passes 382 and 427 checks through the two adapters, 384 and 429 at two interfaces and
369 on the model, and the co-simulation 32 checks; the RTL campaign prints
`mbx mutants: 147 of 147 caught`.

## Known limitations / out of scope

- **Time is not measured (A4).** The bounds are mailbox accesses. Every path costs at most 76.
  The full-backlog bounds fit T_svc = 10 ms only at 0.89 us per access or less behind a full
  acmp ring, and 0.44 us behind a full adp ring (H-DISC), which also exceeds the 20 ms ceiling at
  1 us. With MAAP composed as well, a pass is bounded at 1,580 accesses and those figures are
  0.57 us and 0.28 us. Measuring the access time is an acceptance item of the F2 to F5 bench
  pass. H-ACMP's wire round trip needs the datapath tap.
- **MAAP's allocation does not reach ACMP's talker inside the app.** The talker learns a
  stream's destination (`dest_mac_valid`) only from the integrator's `source` port (`acmp.h`);
  the app does not connect it to the stream-address port. That is integration work, stated in
  both READMEs.
- **The co-simulation composes ADP and ACMP**, not MAAP; the three-way composition is held on
  the host model, at one and two interfaces.
- **The table's area is over its target.** In distributed RAM, compared byte by byte, the term
  costs 357 LUT and 86 FF against 300 and 120 (round 2: 1,280 and 1,047). The rest is per-entry
  logic the contract needs: the compare and its flag, `BOUND_EN`, the owed copy and the
  reset-to-0 of `BOUND_EID`, and its read-back. Measured without the reset clearing `BOUND_EID`,
  +337 LUT; also write-only, +300. Those are contract changes; the ruling on #665 (6033962557)
  did not take them.
- **Copy latency.** A binding takes part once the fabric has copied it, at most 176 clocks
  (1.76 us at 100 MHz) for all sixteen entries of an interface, derived from the RTL; announcements
  are seconds apart.
- **The linked image is a measurement, not a product image.** `ctrl_image.py` links the
  composition with stub owners, runtime stand-ins and its own arithmetic helpers to size it. No
  shipped image links this firmware yet. The helpers stand in for LiteX's `libcompiler_rt`,
  whose bytes are not measured here. lwSRP's pool, the integrator's owners and the stack are not
  sized here. The mailbox stays behind the default-off `--ctrl-mailbox` switch: the default
  all-fabric build and the shipping image are unchanged.
- **No hosted workflow runs `ctrl_image.py` or its self-test.** Both take seconds with the
  pinned SDK. Adding them to `firmware-unit` is a workflow change outside rounds 5 and 6.
- The processor differences are processor issue #168; the submodule is not changed.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (lane F3's; #665 is a multi-lane issue)
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
