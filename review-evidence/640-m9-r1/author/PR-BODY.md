[A720]

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

GREEN, documentation only -- every docs gate exits 0 at head `dfc310fb3dec28f3d06333973e61cde44a4e786d` -- `640-mark2-charter` -> `dev` (base `e5b8405d`).

Requirement text (NFR-RES-01, NFR-LAT-03, NFR-REL-03 and the NFR-SCOUT-02/03/05 amendments) needs owner approval before merge.

## Linked Issue / roles

Relates to #640
Relates to #665
Relates to #823

This is the Mark II charter round; it does not complete #640.

Executor: `[A720]`
Internal cleared-context reviewer: `[R757]`
External reviewer: `[R758]`

## Description

The owner decisions of 2026-10-31 on #640, #665 and #823, written into the requirements, the split contract, the area plan and a new datapath design. No RTL, firmware, generator, gate or configuration change.

| Commit | File | What changed |
|---|---|---|
| `4083cea5` | `docs/reference/FR_NFR.md` | NFR-RES-01: Mark II below 20,000 LUTs at 32x32, fits Block RAM, timing at every corner; the 60 % (38,040) target kept as the Mark I bound. NEW NFR-LAT-03: talker latency below 65 µs, last sample at the TDM pin to the first bit on the wire, every talker stream. NEW NFR-REL-03: a save durable within 0.5 s worst case at 32x32, no erase on the save path. Each names its verification method. NFR-SCOUT-02/03/05, the plane table, the out-of-scope note and the traceability rows amended where the decisions contradict them (gPTP to firmware under F6, no permanent all-fabric option, Section 8 redundancy adopted for Mark II). |
| `cf342310` | `docs/ARCHITECTURE_HW_SW_SPLIT.md` | The split restated: ownership table as "shipping image until the switch-over" and "Mark II end state"; new "Mark II end state" and "Transition and deletion" sections; the processor stays in the default image only until the firmware passes the bench qualification, then it and its build switch are deleted, no dual maintenance; the fabric gPTP plane follows the same rule at F6. |
| `8ad28659` | `docs/design/MARK_II_STREAM_ENGINES.md` (new), `docs/README.md` | The 32x32 shared-engine datapath: one packetizer and one depacketizer with Block RAM contexts; capture buffer sized by the packet interval; packet-boundary stagger and its latency budget under the credit-based shaper; render buffer sized by the presentation time offset (one RAMB36); redundancy pairing by index parity and the first-copy-wins listener merge; per-port MAC, filter and timestamp units; register maps; the 32x32 Block RAM ledger; the append-only 0.5 s save path derived from the flash datasheet maxima. |
| `dfc310fb` | `docs/design/MARK_II_AREA_PLAN.md` | New target; measured basis (the 2026-10-31 routed 1x1 image: 52,008 LUTs, 87.5 tiles, 13 DSP, hierarchical rows and report digests); the owner's lever table, least risky first; the 32x32 additions; the three LiteX stages; the Block RAM ledger; decisions D10 to D17; the Mark II lane sequence. The Mark I sections stay as labelled history; L2, L6, L8 and L10 carry 2026-10-31 notes. |

Key results (each marked in the pages as measured or estimated):

- Talker latency at 32x32 (16 AAF streams and one CRF per port, idleSlope = Milan Table 4.4 sum, 27.08 %): worst 58.658 µs in the preferred phase order and 64.250 µs in the worst of all 90 orders, including one interfering maximum-size frame. Below 65 µs.
- Save at 32x32: 353.4 ms worst case at datasheet maxima, for change sets up to 32 pages behind one save in flight.
- Area: about 21.2k LUTs on central estimates at 32x32 (17.6k to 25.2k), above the ceiling centrally.
- Block RAM: about 141.5 tiles estimated against 121.5 usable; firmware memory binds first.

## Authoritative references

- #640 body ("Updated 2026-10-31") and comments of 2026-10-31; #665 body and comments of 2026-10-31; #823 body and comments of 2026-10-31.
- IEEE 802.1Q-2022 8.6.8.2, 34.3, 34.4, 34.6.1, 34.6.1.1, 34.6.1.2, L.3.1.1.
- IEEE 1722-2016 4.3.2, 4.4.4.3, 4.4.4.6 to 4.4.4.9, 7.5, 7.6.
- IEEE 1722.1-2021 7.2.6.
- IEEE 802.1AS-2020 8.4.3.
- IEEE 802.1BA-2011 6.3, 6.5.
- Milan v1.2 4.3.3.2 (Table 4.4), 4.3.4, 5.3.5.1, 5.3.7.1, 5.3.7.3, 5.3.7.6, 5.3.7.7, 5.3.8.2, 5.3.8.7, 5.3.8.10, 5.3.9.1, 5.3.13, 6.2, 8.2.2 to 8.2.5, 8.3.1 to 8.3.5, Annex C.
- N25Q128 datasheet Table 32 (tPP 5 ms, tSE 3 s, tSSE 2 s maxima), Table 17 (suspend parameters), section 9.1.20.
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 9.4; `docs/design/SPLIT_CONTROL_MEMORY.md` section 5; `docs/design/MAILBOX_SPLIT.md` measured area.

## How to get into the same state

```sh
git fetch origin
git checkout 640-mark2-charter
git log --oneline e5b8405d..HEAD     # four commits, one per file group
python3 -m venv "$HOME/mdvenv"
"$HOME/mdvenv/bin/python3" -m pip install --require-hashes -r tools/markdown/requirements.txt
python3 -m pip install --quiet pyyaml
```

## How to validate

```sh
V="$HOME/mdvenv/bin/python3"
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py --self-test
"$V" scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
"$V" scripts/check_em_dash.py --selftest
python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py && python3 scripts/check_gptp_docs.py --selftest
"$V" scripts/gen_toc.py --selftest
"$V" scripts/gen_toc.py --verify-anchors
"$V" scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 docs/DOC_MAP.gen.py --check
```

Expected result / pass criteria: every command exits 0. At this head: docs_check 0 findings over 211 pages; em dash 0 findings over 1,095 added lines; TOC anchors 563 reproduced; doc paths 1,075 resolved. The same docs_check and feature-status runs also exit 0 on an exported tree without `.git`.

`check_doc_style.py` gates a fixed page list that excludes the touched pages. Its own `analyze()` was applied to every prose block this change adds on the five touched pages: 0 findings (10 words per sentence, 20 per paragraph, 2 sentences).

The shaper schedule in the design page is plain arithmetic a reviewer can redo. A byte-resolution model of 8.6.8.2 corroborated it (18.336 µs against 18.333 µs; 30.632 µs with saturated best effort against the 30.669 µs bound); that model is lane evidence, not committed and not a gate.

## Known limitations / out of scope

- Documentation only: no RTL, firmware, generator, gate, configuration or saved-state format change. The format and flash layout belong to #823, the writer to #665 F1, gPTP to #665 F6.
- **Open owner question: talker latency below the 32x32 load.** With fewer reservations on a port, idleSlope shrinks with them (IEEE 802.1Q-2022 34.6.1.1, Milan v1.2 4.3.4). Two or three co-phased streams left running alone then wait 62.3 to 83.0 µs for credit, 74.6 to 95.4 µs with interference. Re-phasing a running stream breaks IEEE 1722-2016 7.6 and padding a reservation breaks Milan Table 4.4, so the 65 µs bound is shown at the 32x32 load only. NFR-LAT-03 keeps the owner's wording and names this question.
- The worst phase order leaves 0.75 µs of margin, with packet release at the TDM frame's end. Release after each stream's highest mapped slot widens it by up to 18.2 µs, depending on the stream's mapped slots.
- The talker path also feeds the AAF timestamp's fixed delay (the #773 rule, Milan v1.2 5.3.7.6, at most 125 µs). The implementation must re-derive that delay from the Mark II path.
- **Open owner question: save bursts.** The 0.5 s bound holds while the records changed during one save fit 32 pages and sustained saves stay below 10 % of the flash's worst-case write rate. Rewriting all 907 names at once drains in about 1.5 s at datasheet maxima.
- Table 17 of the flash datasheet gives only a typical erase-suspend latency (15 µs); the derivation allows 1 ms and the implementation must measure it.
- The 500 ms and 1,000 ms debounce windows of the materialization decisions exceed 0.5 s; #823 and F1 must restate them.
- Block RAM: the 32x32 estimate is about 20 tiles over the usable 121.5; the firmware memory is a linear extrapolation of two measured points; reductions (names or descriptor image served from flash, pool sizing) are unmeasured.
- Area: the central 32x32 estimate is about 21.2k, above the ceiling; reaching it needs the top of the ranges or new levers.
- The measured basis comes from a qualification-image build whose source commit is not on dev; the report digests are recorded in the plan.
- The gPTP daemon's source and licence are still unconfirmed (#665 F6).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (charter round only; #640's acceptance needs the implementation lanes)
- [ ] New or changed behavior has self-checking tests (no behavior change)
- [x] Required local verification bar passes (documentation gates above)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
