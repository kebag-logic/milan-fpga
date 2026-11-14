[R837] NEGATIVE - exact head 5b264bf26416108add32d7fe5abca5252ffde2cb

# R837-4: internal independent delta review of PR #902 (issue #894), round 9

- Exact head: `5b264bf26416108add32d7fe5abca5252ffde2cb`, tree `2d2fa3312e4bf54ac42f71af967c83711a45bc36`.
- Delta reviewed: `dd01b0af..5b264bf2`, seven commits.
- Source base: `66f713267f201d1a00d7f711e04b3a996d804dee`.
- Authority: the round-9 ruling (#894 issuecomment-6870437042, items 1 to 5 and the STOP triggers), building on 6867990126.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

## Verdict

**NEGATIVE.** One MINOR finding is open: **R837-4-1** (Conformance, RTL, Tests, Docs).

The `_Static_assert` that ruling item 1 requires cannot fire, and it does not check the index range that `place()` actually forms. The table is safe at this head only because of how `MAP_SLOTS` is defined.

Everything else this round delivers holds at the exact head:

- **The direct index.** It is injective by construction. The work bound holds at all seven geometries.
- **The range refusal.** It takes the mapping's turn and returns BAD_ARGUMENTS before the port is read.
- **The definition test.** It is byte-identical.
- **The pace.** 8 ms is the smallest that holds: txL 48.09 of 49, R4L 188.39 of 238.
- **The restated inputs** (975 us, 1,650 us, AMAP_LIVE_WRITE 30 us).
- **Every image** is within its cap.

Every prior finding is resolved at its cause. Two RESIDUE items and six SUGGESTIONs are recorded for one-pass absorption.

## STOP triggers (rulings 6867990126 and 6870437042)

| Trigger | At this head | Evidence |
|---|---|---|
| No P up to 11 holds txL ≤ 49 with R4L ≤ 238 | Not hit. P = 8 holds (txL 48.09, R4L 188.39); P = 7 gives txL 49.69; `paced_rows.choice` = 8; statements none | `receipts/pace_choice_head.txt` |
| Last queued notice over 140 ms | Not hit: 126.46 of 130 | `receipts/flip_grade_check_1x1.txt` |
| Any image over its cap | Not hit. The 1x1/1if fixture has 16 B left in its block; the 8x8/1if platform is at 56.0 tiles | author `receipts/images/every-image-final.txt` |
| Map-command behaviour change | Not hit. The definition test is byte-identical and passes. The new refusal applies only to keys outside the domain, which no product state reaches: an output admits only its declared format (`hdl/milan/milan_datapath.sv:6483-6487`), and a cluster's channels are fixed | `receipts/definition_test_identity.txt`, `receipts/core_arm_1x1_asan.txt` |
| Collision case's pass over THE SHARE at 1x1/1if | Not hit. The heaviest work pass is 149,490 of 200,000 cycles; the refused edits' passes are at most 93,813 | author `receipts/model/measured-inputs-final-pass.txt` |

## What I checked, per ruling item

### 1. Direct index (`aecp_maps.c:139-210`, `aecp_shape.py:19-59`, `aecp_entity.py:44`)

**The index.** `place()` returns `first * MAP_CHANNELS + channel` only when `first < MAP_FIRSTS && channel < MAP_CHANNELS`, and `MAP_SLOTS` otherwise.
- This is injective over the rectangle, and every index is below `MAP_SLOTS`, because `MAP_SLOTS = MAP_MOST(MAP_FIRSTS * MAP_CHANNELS, 256u)`.
- A lookup is one `VISIT()` plus its key's chain.

**The key domain.** `key_domain` reads the same image the platform links (`plat/ctrl_plat.c:43-45` uses `aecp_entity_image` from the same generated header).
- An output key is a STREAM_OUTPUT index plus a channel of its current format or any advertised format, at descriptor offsets 74, 82 and 84.
- An input key is a cluster of a STREAM_PORT_INPUT plus that cluster's channel count, at offset 84.
- Each is taken as the maximum over every configuration.
- The constants at each checked-in configuration are in `receipts/key_domain_head.txt` (1x1/1if: 2/8/8/1, a 64-position domain).

**The range refusal** (`aecp_maps.c:379-384`).
- `legal()` runs first, then `place()`. A mapping outside the domain is flagged `ILLEGAL` at its turn, and the check loop refuses it before `idle()` reads the port (`:412`).
- In `look()`, a map row outside the domain visits no slot (`:220`).
- The order mutant, which forms the index before the geometry check, survives. It is an equivalent mutant: `place()` forms an index but accesses nothing, so the order is unobservable apart from one counted visit (`receipts/probe_plants.txt`).

**The `_Static_assert`** (`aecp_maps.c:158-160`): see R837-4-1.

**The header split.** `AECP_ENTITY_SHAPE_ONLY` and the second `#endif` compile correctly in every unit; the 65-suite sweep at head passed.

### 2. Controls

**Keys arm.** I ran `aecp_arms.py --keys` at the exact head (`receipts/keys_arm_head.txt`).
- All seven geometries exit 0: five checked-in, plus 16x4 and 16x32.
- Every 63-mapping ADD and REMOVE is within 2(n + R).
- At 16x4, the ADD is 63 visits of 126. At 16x32 (488 keys), the REMOVEs reach 1,165 of 2,078.
- The visit counts are identical to the author's receipt.

**Core arm at 1x1/1if under ASan.** 83 of 83 pass, the three new tests included (`receipts/core_arm_1x1_asan.txt`).

**Plants.** At the head I re-planted `map-index-channel-dropped` and `map-domain-a-channel-wide`; both are caught (`receipts/probe_plants.txt`).
- The author's 32-plant subset is at `992e52a0`. `aecp_maps.c` and the tests are byte-identical from that commit to the head: no later commit touches them.

**Counting controls and the definition test.** The 8/16/32/63 counting controls and the quadratic plants are kept. The definition test's comment and body hash `f2fed60f…` at both `dd01b0af` and the head.

### 3. The fallback

Not used. The index fits without narrowing the geometries the builder accepts, and no image grows.

### 4. Re-measurement

**Arithmetic.**
- 91,625 cycles is 916.25 us; plus 5 % is 962.1, so 965 us, and the stated 975 us stays.
- 156,716 cycles gives 1,650 us; 98,720 gives 1,040 us.
- AMAP_LIVE_WRITE 25.51 us gives 26.79, so 30 us.
- The 8x8/2if events 35.76, 32.79 and 22.65 us stay within 40, 40 and 25.

**Gates at the head (my runs).**
- `flip_grade.py --check --point 1x1/1if`: RESULT PASS, every row as stated.
- `load_grade.py --check`: 0.513 and 0.509 at 1x1/1if, 0.792 and 0.752 at 8x8/2if.
- `tier_grid.py --point 1x1/1if`: 18 of 420 designs hold, and it chooses the built one.

**The layout floor** (the ruling asked me to judge it; cf. #909). It is a sound design choice and it is stated. It does not hide a cost:
- The record at the shipped layout is measured, and restated by the rule.
- The 64-slot alternative's 98,720 cycles is published with its consequence: 1,040 us, a 9 ms pace, and a load of 0.705.
- The floor's cost at 8x8 is also stated: 156,716 cycles against 146,010 at the domain's 72 slots, so 1,650 us against a possible 1,535 (`SPLIT_CONTROL_MEMORY.md:2462`). 8x8/2if is reported only.

What the text does not say is that the margin against placement drift is small:
- The 1x1/1if load admits a stated record up to 1,015 us; at 1,020 us it is 0.7006 (author `receipts/item4/long-load-by-record.txt`). That is a measured record up to about 96,660 cycles.
- The 192 B frame move alone gave 98,720 cycles, 7.7 % more.
- The text does not cite #909, the open issue for exactly this sensitivity.
- See S2. The author's open risks disclose that each full pass re-measures the record.

**Rom reconciliation (R838-3-F3).** The author's `rom_layout.py` table checks out arithmetically (`.text` + pad + `.rodata` + 58 B of `.data`). It gives +184 B at the 1x1/1if fixture and +176 B at the other seven.

### 5. Docs

See the table of prior findings below, R837-4-R2, and S2 to S4.

### Full pass

The author's receipts at the exact head are consistent:
- Four sweep shards: 15 + 17 + 17 + 16 = 65 suites and 2,713,040 checks, 0 failures.
- Lane gates as listed in `lane-summary.txt`.
- The final pass's measured inputs at `5b264bf2`.

I did not re-run the sweep, the hosted-job replica, or the harness legs.

## Findings

### R837-4-1 MINOR - Conformance, RTL, Tests, Docs - the map table's `_Static_assert` cannot fire and does not bound the index `place()` forms

**Artifacts**
- `sw/firmware/ctrl/aecp/aecp_maps.c:157-161`.
- `docs/design/SPLIT_CONTROL_MEMORY.md:2461` ("A static assertion holds the table to the whole domain").
- `sw/firmware/ctrl/aecp/README.md:213-214` ("a static assertion holds the table to the whole domain, at least the 256 slots it held before").
- Receipt: `receipts/probe_static_assert.txt`; script: `scripts/probe_static_assert.py`.

**Authority and evidence.** Ruling 6870437042 item 1 requires "a `_Static_assert` that the table holds the whole key domain". The shipped assertion fails that in two ways:
- **It is vacuous.** It checks `KEY_STREAMS * KEY_STREAM_CHANNELS <= MAP_SLOTS && KEY_CLUSTERS * KEY_CLUSTER_CHANNELS <= MAP_SLOTS`. Since `MAP_SLOTS` is defined as at least `MAP_FIRSTS * MAP_CHANNELS`, and each product is at most that, it is true by definition and can never fail.
- **It checks the wrong range.** The two per-type products are not the range `place()` indexes. `place()` uses the shared stride `MAP_CHANNELS` over `MAP_FIRSTS` rows.
  - At 1x1/1if the products are 16 and 8.
  - Input keys index `cluster * 8 + 0`, up to 56.

**Probe.** I planted a table sized per type: `MAP_SLOTS` = the larger product, 16 slots at 1x1/1if.
- It compiles at all five checked-in configurations with the shipped assertion.
- It is caught only at run time, by the map tests at 1x1/1if: the out-of-bounds writes land in the adjacent arrays of `struct edit`.
- The same plant with an assertion on `MAP_FIRSTS * MAP_CHANNELS` is refused at compile time at `arty_8ch`, `arty_current` and `ax7101_1x1_tdm8`. At the other two configurations the per-type product equals the domain.

**Impact.**
- There is no defect at this head.
- The guard the ruling asked for protects nothing against a later change to the table's size. The floor's own rationale, a data-cache layout choice (#909), invites exactly such a change.
- An undersized table would be a silent out-of-bounds write within the edit's stack frame.
- The two documents describe the assertion as holding the table to the whole domain, which it does not do.

**Required outcome.**
- The assertion bounds the declared slot array by the index range `place()` forms. For example, after `struct edit`: `_Static_assert(sizeof ((struct edit *)0)->slot >= (size_t)MAP_FIRSTS * MAP_CHANNELS, ...)`, or the floor and the domain kept as separate macros with the array's size asserted against the domain.
- A compile-time control plants an undersized table at a configuration where it would overflow, and shows it refused.
- The two document sentences say what the assertion holds, and say separately that the 256-slot floor is a layout choice.
- No image or behaviour change is expected.

**Verification.**
- `scripts/probe_static_assert.py <clone> <scratch>`: the `per-type-slots` variant is refused at compile time at 1x1/1if or wherever it overflows.
- The head variant compiles at all five configurations.
- The keys arm and the map tests are unchanged.

### R837-4-R1 RESIDUE - Docs - a review named as provenance in a new source comment

- **Artifact:** `sw/firmware/ctrl/test/aecp_arms.py:17`: "16 talkers of 4 channels (the review's)". The owner's comment rule says source comments state behaviour and reason.
- **Exact fix:** replace "(the review's)" with ", a geometry whose keys shared a slot under the former hash". The line then reads: "16 talkers of 4 channels, a geometry whose keys shared a slot under the former hash, and the builder's most, …".
- This changes no code, test or figure.

### R837-4-R2 RESIDUE - Docs - "At this head" names a round-30 table

- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:2314` ("At this head (`load_grade.py --check` and `flip_grade.py --check`; …)") and `:2322` ("The load gate holds 1x1/1if in both columns: at the pin 0.501, …").
  - The table's 0.501 / 0.499 and 0.822 / 0.770 are round 30's figures at the merge of `dev-soft-core` `0fb66211` (`5bea2597`).
  - At this head the gates give 0.513 / 0.509 and 0.792 / 0.752 (`receipts/load_grade_check.txt`).
  - The same document's `:2481`, corrected this round, now says "at this head" with the new figures.
- **Exact fix:**
  - At `:2314`, replace "At this head (" with "At the merge of `dev-soft-core` `0fb66211`, round 30's legs (".
  - At `:2322`, replace "The load gate holds 1x1/1if in both columns:" with "There the load gate held 1x1/1if in both columns:".
  - Every figure stays as written.

### Suggestions (optional)

- **S1 - Tests - the stream/cluster half of the range check has no control.** The mutant `first-range-unchecked` (`place()` without `first < MAP_FIRSTS`) survives every map test (`receipts/probe_plants.txt`).
  - It is unreachable in product: the domain's row count is taken from the same image `legal()` reads.
  - The channel half has its control. One for the other half would make `MapKeysOutsideTheDomainAreRefusedAtTheirTurn` cover both edges, for example a STREAM_OUTPUT index or an input-port cluster past the build's count, with its descriptor in place.
- **S2 - Docs - tie the floor to #909 and state its margin.**
  - Cite #909 at `aecp_maps.c:149-153` and `SPLIT_CONTROL_MEMORY.md:2462`, so that a fix of the placement sensitivity revisits the floor.
  - State the margin: the 1x1/1if load admits a stated record up to 1,015 us, a measured record up to about 96,660 cycles, while the 192 B frame move alone measured 98,720.
- **S3 - Docs - name the product precondition for "no product state reaches it"** (`SPLIT_CONTROL_MEMORY.md:2461`).
  - A format is judged by the integrator's port (`aecp_commands.c:274-279`), not by the advertised list.
  - The domain holds because the datapath admits only an output's declared format (`milan_datapath.sv:6483-6487`, "until talker adaptation exists") and a cluster's channels are fixed.
  - A future talker adaptation must widen `key_domain`. Otherwise such mappings are refused with BAD_ARGUMENTS: safe, but a behaviour change.
- **S4 - Robustness, Docs - the edit's frame grows with the geometry.**
  - The slot table is max(domain, 256) B on the stack: 544 B at 16x32.
  - No gate bounds the target's call-chain stack; `fw_rv32.stack_frames` reports the largest static frame only.
  - The frame is unchanged at every checked-in configuration. Saying this beside "The table's size" would help an integrator choosing a wide geometry.
- **S5 - Evidence - the packet index** (carried from R837-3 S1 and R837-2 S2; also R838-3-S7).
  - `INDEX.md` lists `A10-RULING.md`, which is not published, and `scripts/index.py` differs from its listed bytes (1,211 against 1,224 B).
  - The other 73 rows verify (`receipts/packet_index_check.txt`).
  - Generate the index from the published bytes.
- **S6 - Evidence - where the item-2 receipts ran.** The R838-3 probe and the keys arm ran at `58e6b60f` and `992e52a0`. They apply to the head because `aecp_maps.c` and the tests are byte-identical there, and my keys arm at the head reproduces them. Naming that identity in the receipt header would save a cold reader the check.

## Prior findings at this head

| Finding | Status at `5b264bf2` | Evidence |
|---|---|---|
| R838-3-F1 MAJOR: legal key collisions defeat the map-work bound | **Resolved at cause.** The direct index is injective over the build's domain. The R838-3 geometry (16x4) and the builder's widest (16x32) are enumerated, with every edit within 2(n + R); the 16x4 ADD is 63 visits of 126 (714 before). Status and precedence are unchanged, and the definition test is byte-identical. The residual guard weakness is R837-4-1. | `receipts/keys_arm_head.txt`; `aecp_maps.c:201-210,379-384`; author `receipts/item2/r838-3-probe.txt` |
| R837-3-1 MINOR: the hash precondition the builder does not keep | **Resolved at cause.** The same index replaces the hash, so no precondition remains. | as above |
| R837-3-2 MINOR: R4L bound, pace rule and loads at pre-ruling values | **Resolved** at each listed line: `tb/verilator/ctrl_service_budget/README.md:183` (238 ms, ruling 6844175391), `:185` (the pace rule with R4L ≤ 238), `SPLIT_CONTROL_MEMORY.md:2355` (238 ms at the commit), `:2481` (0.792 / 0.752, 0.513 / 0.509). Another instance of the class, wording only, is R837-4-R2. | grep at head; `receipts/load_grade_check.txt` |
| R838-3-F2 MINOR: timing prose retains pre-egress bounds | **Resolved.** README:183 (238, both allowances, ruling link); the THE TIERS bullet now gives 49 ms with `T_egress` (`SPLIT_CONTROL_MEMORY.md:2475`). | diff `5cfa32c2` |
| R838-3-F3 MINOR: "+176 B every image" | **Resolved.** `.text` grew 180 B everywhere; the 8-byte alignment of `.rodata` gives +184 B at the 1x1/1if fixture and +176 B at the other seven. Arithmetic checked. | author `receipts/images/rom-layout-f3.txt`; REVIEW READY 6872978311 |
| R838-3-R1 RESIDUE: delta count | **Resolved.** The PR body and REVIEW READY say "the delta from `dd01b0af` to `5b264bf2`, seven commits" (`git rev-list --count` = 7). | PR body line 17 |
| R837-3-R1 RESIDUE: `long_notice.py` collision description | **Resolved** with the exact fix (`long_notice.py:19-22`). | diff `5cfa32c2` |
| R837-3 S1 (packet index) | Not addressed; carried as S5. | `receipts/packet_index_check.txt` |
| R837-3 S2-S4; R838-3-S1 to S7 | Optional. The delta does not touch their artifacts; carried unchanged, not re-judged. | - |

## Reviewer-owned completion ledger

| Lens | Result | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R837-4-1) | Ruling 6870437042 items 1-5 and STOP triggers against: `aecp_maps.c:139-210,355-420`; `aecp_shape.py:19-59`; `aecp_mbx.h:45-54`; `rows_tiers.py:99,132`; `flip_grade.py --check --point 1x1/1if`; `paced_rows.choice` (P = 1 to 13); `load_grade.py --check`; `tier_grid.py --point 1x1/1if`; image caps (author receipt); the SET_STREAM_FORMAT verdict, `milan_datapath.sv:6427-6488` | R837-4 | `5b264bf2` |
| RTL | UNCLEAN (R837-4-1) | `aecp_maps.c:139-230,355-430`: index injectivity, widths, the `MAP_SLOTS` floor, the `memset` scope, `uint8_t` slot entries against `AECP_MAP_PAGE < 256`, `ILLEGAL` precedence; `aecp_entity.py:44` header guard; `aecp_mbx.h:54`; static-assert probe at five configurations | R837-4 | `5b264bf2` |
| Robustness | CLEAN | Out-of-domain keys at their turn, before the port read (`aecp_maps.c:379-384,412`); out-of-domain map rows (`:220`); product reachability of out-of-domain keys (`aecp_commands.c:274-279`, `aecp_face.c:210-217`, `milan_datapath.sv:6479-6488`); `key_domain` across configurations; stack growth with geometry (S4); edits at 63 mappings, accepted and refused (`receipts/keys_arm_head.txt`); ASan core arm (`receipts/core_arm_1x1_asan.txt`) | R837-4 | `5b264bf2` |
| Tests | UNCLEAN (R837-4-1) | `test_aecp.cpp:178-206,2632-2742` (the three new tests and the reworked work test); `aecp_arms.py:10-41,161,190-194`; `aecp_map_mutants.py:14-129`; keys arm at seven geometries; two author plants re-planted and caught, two reviewer mutants (one equivalent, S1); definition-test hash at both heads; author 32-plant subset at `992e52a0` | R837-4 | `5b264bf2` |
| Docs | UNCLEAN (R837-4-1; RESIDUE R837-4-R1, R837-4-R2) | `SPLIT_CONTROL_MEMORY.md:2314-2322,2337-2380,2450-2490`; `FR_NFR.md:381-383`; `aecp/README.md:200-240`; `tb/verilator/ctrl_service_budget/README.md:180-186`; `long_notice.py:17-25`; `rows_tiers.py:94-132`; PR body; REVIEW READY 6872978311; author packet index | R837-4 | `5b264bf2` |

## Real limits

- I did not re-run the full sweep, the hosted-job replica, the lane gates, or any CPU budget harness leg (Verilator). The measured cycles (91,625, 156,716, 98,720; 25.51 us) are the author's receipts, which I checked for consistency and arithmetic, not by re-simulation.
- **The 8x8 core arm.** A core arm with the 8x8 header fails 14 tests (`receipts/core_arm_8x8_unsupported.txt`). This pairing is not run by the sweep: the core arm runs at 1x1 only, and the keys test runs at every configuration. The failures I sampled are fixture preconditions, for example `test_aecp.cpp:2552` (at least 4 clusters), against 8x8's `AECP_ENTITY_KEY_CLUSTERS 0`. A round-8 baseline of this pairing was not run: the extraction it needed was refused in this environment.
- **The author's packet commit** `fa3f0a8c` carries no signature header. I verified it through its `INDEX.md` hashes (S5).
- **Hosted evidence at the exact head**, as queried: 11 success, 1 skipped, 38 queued or in progress (`receipts/hosted_checks_head.txt`). This is not acceptance evidence. No manager source bank runs at this head, and I claim none.
- Physical calibration was not run; field skips are not hardware proof.

## Pending manager duties

- Route R837-4-1 to the author. It needs a source change (the assertion and its control, plus two document sentences), then re-review of Conformance, RTL, Tests and Docs at the new head.
- Carry R837-4-R1 and R837-4-R2 to the residue checklist.
- Hosted and act acceptance at the exact head.
- At the merge turn, the current-dev candidate (source base `66f71326`, live dev `b7d69295`) with the builder and native banks.
- The unchanged duties: 8x8/1if is lane 894b's; 8x8/2if stays reported (#910); #908 stays open; S12b's wire capture is owed.

## Packet

- `REPORT.md`.
- `scripts/`: `probe_static_assert.py`, `probe_plants.py`, `check_packet_index.py`.
- `receipts/`: listed in `MANIFEST.sha256`. Host paths in receipts are replaced by `<clone>` and `<packet>`.
- The clone was restored and verified after the probes (`receipts/clone_restore_check.txt`):
  - HEAD `5b264bf2`, tree `2d2fa331`.
  - Index and worktree match HEAD, with 0 untracked or ignored entries.
  - Every submodule gitlink matches HEAD, and every submodule is clean.

R837-4 FINISHED
