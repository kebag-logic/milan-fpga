[A720q]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- The answers to R765-1 and R766-1, one commit each.
- **[Round 3](#round-3)** -- The answer to R766-2-F1, one commit.
- **[Round 4](#round-4)** -- The answer to R765-3-F1, one commit.
- **[Round 5](#round-5)** -- The answer to R765-4-F1 / R766-4-F1 and three residues, one commit each.
- **[Sync with dev 0a75aa77](#sync-with-dev-0a75aa77)** -- One merge of dev; one conflict, both sides' rows kept.
- **[Sync with dev ac0a01e3](#sync-with-dev-ac0a01e3)** -- Round 7: one merge of dev; one conflict, both rows kept; no figure corrected.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN, documentation only -- every locally runnable step of the docs workflow exits 0 on a clean clone of head `e70ae2cb2dd0746060612493cb6724522b8701bc`, including both builder legs (65 run steps, all rc 0; 31 hosted-only steps not run, each with its stated reason), and `git diff --check` against the merge base `ac0a01e3` is clean -- `640-charter-followup` -> `dev`.

A small follow-up to the Mark II charter (PR #828, merged as `503bc97c`). Four Markdown pages change; no RTL, firmware, generator, gate or configuration file.

`docs/design/AREA_BUDGET.md` and `docs/design/MAILBOX_SPLIT.md` are gate-read pages (`scripts/ci_scope.py`), so CI does not classify this PR as docs-only. Their readers pass at the head: `pp_resource_gate.py check-baseline` ("baseline PASS: 3 endpoints") and the `ctrl_service_bounds` arm. Neither reads a changed line.

## Linked Issue / roles

Relates to #640
Relates to #495

Executor: `[A720j]`, then `[A720k]` for the second pass, then `[A720l]` for round 2, then `[A720m]` for round 3, then `[A720n]` for round 4, then `[A720o]` for round 5, then `[A720p]` for the sync with dev, then `[A720q]` for the second sync
Internal cleared-context reviewer: `[R765]`
External reviewer: `[R766]`

## Description

Five items, one commit each, all in `docs/design/MARK_II_AREA_PLAN.md` except the last. A second pass then adds two commits on the same page, from the manager's answer on #640 (issuecomment-6575277828).

| # | Item | What changed |
|---|---|---|
| 1 | Lever 4 accounting | `MilanSoC` under `--ctrl-mailbox` has always built one hart, so the owner's 34.2k start counted the split CPU (3,948 LUTs) on top of the SoC CPU the 52,008 basis already holds (3,249). Without the double count the start is 30,974 (derived). Lever 4 saves 0: it is an accounting correction. After lever 4 both chains reach 27,224 (derived). The owner's middle 3.55k overstated the 3,249 by about 0.3k, so the central totals from lever 4 on rise about 0.3k: the six levers reach about 21.0k and the 32x32 estimate about 21.75k (was 21.45k). Each derived figure is marked and names its netlist rows. |
| 2 | LiteX block census | A short table of every LiteX block the shipping 1x1 SoC builds, from the basis build's module tree and `milan_soc.py`, with the stage that removes it and its fate: removed with nothing in its place, replaced by a named first-party block, or replaced by a donor core under the owner's stage 2 decision. Placed rows are cited where the hierarchy has them; the LiteX top is one flat row. The owner's 2026-11-02 decisions are recorded as D18 to D20, linked to the comment on #640 that records them. |
| 3 | Console UART | A small first-party UART, transmit and receive only, no RTS/CTS. Receive is polled once per pass. At 115,200 baud a character takes 86.806 µs. The stage 1 probe's 16-byte FIFO lost characters on 17 of 300 22-character lines and none of 300 14-character lines. While every pass fits the 2.0 ms per-pass share, 24 characters can arrive between polls, so the buffer is 32 bytes (covers 2.778 ms); round 2 states that this share is unmerged S2b work. Console loss beyond that bound is accepted; console work never stretches a service bound. |
| 4 | LiteX stage 1 | The boot loader copies the firmware image from QSPI flash into Block RAM (owner, 2026-11-02); the image has its own flash slot (D21, below). Masters use the SoC bus, never the CPU's DMA port: the stage 1 probe measured that route hanging (3 reads issued, none answered). With the masters on the SoC bus the entity advertised and all 33 descriptors read back byte-identical. The cause is not established, and the page says it is a measurement, not a diagnosis. |
| 5 | #828 residue listed on #495 | `AREA_BUDGET.md`: "the accepted target"; the acceptance bar adds Block RAM and timing. `MAILBOX_SPLIT.md`: the placement pointer "defines the transition and end state"; the event record's grandmaster source and the fabric paragraph say "until #665 lane F6". `docs/findings/README.md`: the stale gap is the gap to NFR-RES-01's former 60 % target. Where the exact text broke the 10-word sentence or 20-word paragraph limit, the paragraph is split with the same content. |


Second pass:

| # | Item | What changed |
|---|---|---|
| 6 | D18 to D20 links | The three decision rows link to issuecomment-6575277828, which records the owner's 2026-11-02 decisions. |
| 7 | Firmware flash slot | The manager's decision of 2026-11-02 is recorded as D21: the firmware image gets its own flash slot, sized for the image, in a free erase-aligned range that is neither reserved (`journal`, `user`) nor used. The bitstream and AEM slots keep their offsets and budgets. The image does not go in the bitstream slot's tail, which would tie its offset to the bitstream's size. Open decision 4 and every statement that the layout stays as is are removed: the stage 1 table row and text, the D18 consequence, the stage 1 lane's dependency. The offset and budget are not chosen here: the stage 1 lane states them in `FLASHBOOT_LAYOUT` and the generated layout page. `QSPI_FLASHBOOT.md` still describes the shipping layout, unchanged until stage 1 lands. |

## Round 2

Both round 1 reviews were NEGATIVE with MINOR findings only: R765-1 (issuecomment-6577388726) and R766-1 (issuecomment-6577608536). Each finding is answered once, under every ID that raised it. Two pages change: `docs/design/MARK_II_AREA_PLAN.md` and one line of `docs/design/MAILBOX_SPLIT.md`.

| # | Findings | What changed |
|---|---|---|
| 8 | R765-1-F1, F2, F3; R766-1-F1 | The census is re-derived from `sw/litex/milan_soc.py` and the basis build's SoC hierarchy, CSR map and placed hierarchy, not from the first pass's table. New rows: the 200 MHz `idelay` clock and the `IDELAYCTRL`, which Ethernet keeps past stage 1 and whose clock drives the audio MMCM's `PSCLK` (the fate keeps today's clock for it; an `IDELAYCTRL` stays only if the stage 2 MAC uses an `IDELAYE2`, since all 32 in the basis are DDR3's); `MilanMAC`'s `link_status` CSR (REQ-MAC-03; a first-party register) and `loopback` CSR (removed: nothing writes it); the split build's `ctrl_memory` banks and decoder (first-party Block RAM at stage 3) and `ctrl_mbx`'s event manager, CSR bank and tick. The BIOS ROM and SRAM move to the switch-over, where the split build already drops them, and their fates no longer name a LiteX block. The Ethernet row's PHY reset pin keeps its power-on pulse and the reboot controller's hold. DDR3's row gains the CPU memory port's crossing and the `sys4x` clocks. Three cross-references follow: a note under the stage table, the basis row's disposition and the Block RAM ledger's line. Coverage was checked mechanically: every node of the SoC hierarchy, every CSR register and every placed child of the CPU wrapper maps to exactly one row with a stage and a fate, and the same check against the round 1 page fails on the nine objects the findings named. |
| 9 | R765-1-F5; R766-1-F2 | The page states that the 2.0 ms share and T_svc = 20 ms come from #665's S2b work (PR #810, not merged), and that dev's `FR_NFR.md` still proposes 10 ms. Under 10 ms, with no per-pass share, 116 characters complete within the gap and the buffer would be 128 bytes. The 32-byte result is marked conditional on the share and is re-derived if the share changes; at 32x32 #665 estimates passes over the share, where the loss rule applies. The census UART row and D20's consequence say the same. |
| 10 | R765-1-F4; R766-1-F3 | "311 of 311 reads were answered" is removed: no public source carries it. The page keeps the measured hang and adds what the cited probe comment shows for the SoC bus route: the entity advertised and all 33 descriptors read back byte-identical. |
| 11 | R766-1-R1 | `MAILBOX_SPLIT.md:151` now reads "Its sources also include fabric timer expiries, tagged by arm." The residue's exact text was 11 words; "with their arm" became "by arm" to meet the 10-word limit, as round 1 did for its residue. |
| 12 | R765-1-S1; R766-1-S1 | The split CPU's netlist identifier, which no public source records, is dropped; the cited #665 comment stays the source of 3,948 and 3,543. |

Suggestions not taken: R765-1-S2 (which CPU figure the start uses: the lever 4 figures recomputed clean in both reviews, and the CPU's clock moves with the S2b work); R765-1-S3 (the image behind the console-loss figure: the public probe comment does not name it, so naming it would add an unsourced fact); R766-1-S2 (recasting lever 4's "Why" cell and lane 7 needs the owner, whose text it is); R766-1-S3 (the probe's AX7101 area figure includes the failing DMA route and was not re-routed, so it does not measure stage 1 as planned).

## Round 3

R765-2 (issuecomment-6579373754) was POSITIVE. R766-2 (issuecomment-6579449561) was NEGATIVE on one MINOR, R766-2-F1: the plan still disagreed about which lane removes the BIOS memory, and about what takes its place. One page changes: `docs/design/MARK_II_AREA_PLAN.md`.

| # | Findings | What changed |
|---|---|---|
| 13 | R766-2-F1 | The BIOS ROM and SRAM rows say the switch-over removes the BIOS and its integrated ROM and SRAM, and that `ctrl_memory`'s `rom` and `sram` banks hold those regions (and `rom` the reset entry) until stage 3, then first-party Block RAM. From stage 1 the boot loader fills `rom` from the flash copy (D18). "Nothing in its place" and "the split build builds none" are gone. Lane 2's scope reads "Drop DDR3 (lane 1 already drops the BIOS memory); a boot loader filling `rom` from the firmware's QSPI flash copy (D18); ..." and no longer drops the BIOS ROM. The note under the stage table says the stage 1 row keeps the owner's words, that the switch-over removes the BIOS and its ROM and SRAM, that `ctrl_memory`'s banks hold them until stage 3, and that stage 1 drops DDR3 and fills `rom` from flash. |

Every other statement of who removes the BIOS memory already agreed and is unchanged: the basis row's disposition ("the switch-over and LiteX stages 1 to 3"), D19's scope line and decision row, the Block RAM ledger ("all 47 are gone once LiteX stage 3 ends"), the basis description of the LiteX top, M8a-1's row and text in the plan and in `AREA_BUDGET.md` ("the split builds neither BIOS memory"), and `MAILBOX_SPLIT.md`'s switch description ("builds no BIOS ROM or BIOS SRAM, and builds `rom` and `sram` block RAM from that image"). The stage table's stage 1 cells keep the owner's stage name; the note above reconciles them, as R766-2 read it.

Suggestions not taken this round: R766-2-S1 (T_svc = 20 ms as an approved owner decision, and a 256-byte row under it), R766-2-S2 (naming the probe board) and R766-2-S3 (`MilanMAC`'s first-party glue in the Ethernet fate). The round was limited to F1; each stays open for a later change.

## Round 4

R766-3 (issuecomment-6580971431) was POSITIVE. R765-3 (issuecomment-6580969269) was NEGATIVE on one MINOR, R765-3-F1: the stage table's stage 1 "Removes" cell still credited stage 1 with the BIOS ROM and SRAM and their measured 18 RAMB36, which the note, the census rows, lane 2's scope, the Block RAM ledger (M8a-1) and `AREA_BUDGET.md` book to the switch-over. One page changes: `docs/design/MARK_II_AREA_PLAN.md`, three lines.

| # | Findings | What changed |
|---|---|---|
| 14 | R765-3-F1 | Stage 1's "Removes" cell reads "LiteDRAM controller and PHY. The BIOS ROM and SRAM, 18 RAMB36 measured, already left at the switch-over (M8a-1)", linked to the firmware and block RAM ledger. Stage 1's "Change" cell keeps the owner's words, and the note now names it: "Stage 1's Change cell keeps the owner's words." |
| 14 | R765-3-F1, same cause | Stage 3's "Removes" cell credited stage 3 with "the generated FIFOs". The census says each leaves with the block that owns it, and none of the 29 RAMB36 belongs to a stage 3 row: 16 are DDR3's (stage 1), 5 the Ethernet MAC's (stage 2) and 8 the processor's memory-path crossings (switch-over), by the basis build's synthesis mapping. The cell read "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block", linked to the census; round 5 narrows it to the 29 RAMB36. |

Every other per-stage RAMB36 or LUT credit was re-read and books nothing twice: stage 1's "Lever 1, ~1.0k LUTs" is lever 1's DDR3 drop, with no BIOS figure; stage 2's and stage 3's LUT credits split the -1.75k "beyond levers 1 and 2"; the lane table's savings match the stage table; the Block RAM ledger books the BIOS's 18 at the switch-over (M8a-1) and credits no generated FIFO to any stage; and "all 47 are gone once LiteX stage 3 ends" states a bound, not a stage credit. The census coverage check maps the same objects to the same rows as round 3 (PASS).

Not taken this round, by the round's limit: R765-3-R1 ("hold them" takes the BIOS as its object) and R765-3-S1 (where stage 1's loader runs). R765-2-RESIDUE-1 and -2 stay as residue.

## Round 5

R765-4 (issuecomment-6584004136) and R766-4 (issuecomment-6582620684) were both NEGATIVE on the same MINOR, R765-4-F1 / R766-4-F1. Stage 3's "Removes" cell said every generated FIFO leaves before stage 3. The census places the UART's FIFOs and the CSR crossing `milan_axil_cdc`'s (two RAMB18) at stage 3. One page changes: `docs/design/MARK_II_AREA_PLAN.md`, five lines, one commit each.

| # | Findings | What changed |
|---|---|---|
| 15 | R765-4-F1 / R766-4-F1 | Stage 3's "Removes" cell takes R766-4-F1's exact fix: "Wishbone and CSR-bank glue; the FIFOs of stage 3 blocks. The 29 generated FIFO RAMB36 leave earlier, each with its block", linked to the census. Neither the stage table nor the census now says stage 3 removes no generated FIFO. |
| 16 | R766-3-RESIDUE-2 / R765-3-R1 | The note under the stage table reads "Until stage 3, `ctrl_memory`'s banks hold both regions." "Them" no longer takes the BIOS as its object. |
| 17 | R765-2-RESIDUE-1 | The console UART text reads "Taking 10 ms as the gap gives 128 bytes." |
| 18 | R765-2-RESIDUE-2 | The split build's census fate reads "From stage 1, `rom` is filled from the flash copy, not the configuration image." |
| 19 | R765-4-S1 | Stage 1's "Removes" cell names the link's target: "(M8a-1, Mark I ledger)", with "Mark I ledger" linked to the firmware and block RAM ledger. M8a-1's -18 RAMB36 row exists only in the Mark I history ledger, and the page also has a current Mark II Block RAM ledger. |

No figure moves. The census coverage check is unchanged (PASS), and every fragment link in the stage table and its note resolves.

Not taken, optional: R765-3-S1 (where stage 1's loader runs), R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3 and R765-2-S4.

## Sync with dev 0a75aa77

Both round 5 reviews were POSITIVE at `d85da329`: R765-5 (issuecomment-6586963259) and R766-5 (issuecomment-6587152040). Dev then moved, so this round merges it.

One merge commit, `git merge --no-ff origin/dev`, with no rebase, force or amend. Dev brought 9 merges, 231 commits, from `503bc97c` to `0a75aa77`:

| PR | Issue | Subject |
|---|---|---|
| #831 | #829 | Run the gPTP plane on the MII port at 100 Mb/s |
| #836 | #737 | Split the hosted LiteX simulations into three measured elaborate legs |
| #815 | #797 | Generate the documentation audit from every tracked document and verify the release-facing pages |
| #834 | #833 | Bound and explain the owned-process cleanup under load |
| #841 | #839 | Hold the CSR-addressed transmitters until the station MAC is written |
| #842 | #840 | Prototype identity, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page |
| #849 | #848 | Drop line counts from the generated audit page |
| #847 | #845 | Adopt protocol-processor main `92100657` |
| #846 | #843 | Adopt FPGA-gPTP main `1616fc8f` |

| File | Merge | Resolution |
|---|---|---|
| `docs/findings/README.md` | conflict on two adjacent rows | Dev's 234 row (#843's route record, #845's standalone records) and this branch's 649 row are both kept, each unchanged. |
| `docs/design/AREA_BUDGET.md` | clean | Dev's #845 and #843 records and this branch's target sentences are on separate lines; both kept. |
| `docs/design/MARK_II_AREA_PLAN.md` | clean | Dev's +0.242 ns record and its #845 and #843 lines merge beside this branch's text. No branch line cites a record dev moved. |

No generator output changes. The inventory, contents, diagram and matrix checks are fresh at the merge, so there is no regeneration commit.

Nothing else changes. The head differs from dev only in this branch's four pages: 231 lines added and 53 removed, as before.

Both round 5 reviews asked for the census coverage check on current dev. At the merge it passes against dev's `sw/litex/milan_soc.py`.

Its control against the round 1 page still fails, as it must.

## Sync with dev ac0a01e3

Both round 6 reviews were POSITIVE at `72816d26`: R765-6 (issuecomment-6719846258) and R766-6 (issuecomment-6719945800). Dev then moved, so this round merges it.

One merge commit, `git merge --no-ff origin/dev`, with no rebase, force or amend. Dev brought one merge, 11 commits, from `0a75aa77` to `ac0a01e3`:

| PR | Issue | Subject |
|---|---|---|
| #852 | #851 | Adopt the processor pin that sends one vector per value: processor `044cb25f`, the fifteenth area record, the area budget and the #234 page |

| File | Merge | Resolution |
|---|---|---|
| `docs/findings/README.md` | conflict on two adjacent rows | Dev's 234 row (now #851's record of 2026-11-08) and this branch's 649 row are both kept, each unchanged. |
| `docs/design/AREA_BUDGET.md` | clean | Dev's #851 record, record table and allocation figures sit on other lines than this branch's target sentences; both kept. |
| `docs/design/MARK_II_AREA_PLAN.md` | clean | Dev's +0.210 ns warning row and its #851 anchor line merge beside this branch's text. |

Corrected figures: none. Every figure the branch's lines cite comes from the 2026-10-31 basis build or NFR-RES-01. Dev changed neither.

No branch line cites a record figure that #851 moved. The superseded #843 figures still on the pages are dev's history lines.

No generator output changes. The inventory, contents, diagram and matrix checks are fresh at the merge, so there is no regeneration commit.

Nothing else changes. The head differs from dev only in this branch's four pages: 231 lines added and 53 removed, as before.

The census coverage check still passes at the merge, and its round 1 control still fails. Dev's `sw/litex/milan_soc.py` has not changed since `0a75aa77`.

Both round 6 residues, R765-6-R1 and R766-6-RESIDUE-1, ask for the reference bullet's base. It now names the merge base `ac0a01e3`.

## Authoritative references

- #640's body and its comments from 2026-10-31 on: the target (issuecomment-6545523624), the lever order (issuecomment-6545540394), the LiteX stages (issuecomment-6545999204), the core survey (issuecomment-6551164172), the stage 1 probes (issuecomment-6555550136, issuecomment-6556743957).
- The owner's decisions of 2026-11-02 07:21 (stage 1 copies the firmware from QSPI flash into Block RAM; every LiteX peripheral removed) and 07:22 (a first-party UART, transmit and receive only, no RTS/CTS). Recorded on #640 (issuecomment-6575277828).
- The manager's decision of 2026-11-02 on where the copied firmware sits in flash (#640 issuecomment-6575277828).
- #665: one hart under `--ctrl-mailbox` and the split CPU's netlist rows (issuecomment-6569635407); T_svc = 20 ms (issuecomment-6495692075); the 2.0 ms per-pass share (issuecomment-6514866239).
- #495: the #828 residue (issuecomment-6573412222).
- PR #835's round 1 reviews: R765-1 (issuecomment-6577388726) and R766-1 (issuecomment-6577608536).
- PR #835's round 2 reviews: R765-2 (issuecomment-6579373754) and R766-2 (issuecomment-6579449561).
- PR #835's round 3 reviews: R765-3 (issuecomment-6580969269) and R766-3 (issuecomment-6580971431).
- PR #835's round 4 reviews: R765-4 (issuecomment-6584004136) and R766-4 (issuecomment-6582620684).
- PR #835's round 5 reviews: R765-5 (issuecomment-6586963259) and R766-5 (issuecomment-6587152040), both POSITIVE.
- PR #835's round 6 reviews: R765-6 (issuecomment-6719846258) and R766-6 (issuecomment-6719945800), both POSITIVE.
- `sw/litex/ctrl_memory.py` (`ROM` and `RAM` regions) and `sw/litex/milan_soc.py` (`add_ctrl_memory`, the `--ctrl-mailbox` build switch).
- PR #810, the S2b lane, open and not merged.
- `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/MARK_II_STREAM_ENGINES.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/AREA_BUDGET.md`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/integration/QSPI_FLASHBOOT.md` at `ac0a01e3`, the merge base; since `503bc97c` only `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` changed, by dev's #845, #843 and #851 records; NFR-RES-01 and NFR-SCOUT-03 in `docs/reference/FR_NFR.md`.

## How to get into the same state

```sh
git fetch origin
git checkout 640-charter-followup
git rev-parse HEAD        # e70ae2cb2dd0746060612493cb6724522b8701bc
git merge-base HEAD origin/dev   # ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36
git submodule update --init gptp-processor protocol-processor third_party/tsn-c-stack third_party/verilog-axis
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base ac0a01e3
python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest
python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/docs_inventory.py --check
git diff --check ac0a01e3 HEAD
python3 syn/ooc/pp_resource_gate.py check-baseline
# every changed prose block of the four pages against the style limits:
python3 - <<'EOF'
import re, subprocess, sys
sys.path.insert(0, "scripts"); import check_doc_style as c
for page in ["docs/design/MARK_II_AREA_PLAN.md", "docs/design/AREA_BUDGET.md",
             "docs/design/MAILBOX_SPLIT.md", "docs/findings/README.md"]:
    diff = subprocess.run(["git", "diff", "-U0", "ac0a01e3", "--", page], capture_output=True, text=True).stdout
    added = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M):
        added.update(range(int(m.group(1)), int(m.group(1)) + int(m.group(2) or 1)))
    text = open(page).read(); lines = text.splitlines()
    for f in c.analyze(text):
        end = f.line
        while end < len(lines) and lines[end].strip() and not lines[end].lstrip().startswith(("#", "|", "-", "```")):
            end += 1
        if any(f.line <= n <= end for n in added):
            print(page, f.line, f.reason)
EOF
```

Expected result / pass criteria: every command exits 0, the style probe prints nothing, and `check-baseline` prints "baseline PASS: 3 endpoints". The full docs workflow, both builder legs included, is in the author's evidence; so are the census coverage check and its basis excerpts.

## Known limitations / out of scope

- **The firmware slot's offset and budget are not chosen.** D21 fixes where the image goes in principle; the stage 1 lane states the numbers in `FLASHBOOT_LAYOUT`. `QSPI_FLASHBOOT.md` is not edited: it describes the shipping layout.
- **The console buffer rests on the 2.0 ms per-pass share,** which the S2b lane (PR #810) carries and dev does not yet publish; the page now says so, and gives 128 bytes under dev's proposed 10 ms. At 32x32 the S2b estimates exceed the share; console loss is then accepted by rule.
- **The census is checked against the basis build's records,** which stay outside the repository. The author's evidence carries the SoC hierarchy, the CSR map, the placed hierarchy's top rows and the coverage check, with the digests of the full reports.
- **Two census fates keep today's behaviour rather than choose a new one:** the audio MMCM's `PSCLK` stays the 200 MHz clock, and the PHY reset pin keeps its power-on pulse and the reboot hold. Changing either is a later lane's measured decision.
- **The SPI flash donor is not chosen.** The fate is the owner's stage 2 decision; the core survey found no AXI core with both 7-series use and an active maintainer.
- **#640's body still shows the owner's 34.2k chain.** The plan corrects it; the issue body is not part of this PR.
- Not taken from the #495 list: the optional `SYSTEM_INTEGRATOR.md:95` and `BUILD_FLASH_BOOT.gen.py:44` items, PR #828's body, and the round-10 evidence prose.
- No figure is re-measured: every number is a recorded measurement or derived from one.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

