[A720b]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- How each round-1 finding was closed.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN, documentation only -- every step of the docs workflow exits 0 on a clean clone of head `f6b3e841646384177584ce75b657fb8dead7727c`, including the bare-metal scope gate and both builder legs -- `640-mark2-charter` -> `dev` (base `e5b8405d`, also the live dev tip).

Round 2 answers R757-1 and R758-1 (both NEGATIVE at `dfc310fb`). The requirement text (NFR-RES-01, NFR-LAT-03, NFR-REL-03, the NFR-SCOUT-02/03/05 amendments and the REQUIREMENTS.md scoping) needs owner approval before merge.

The talker latency target is met by the design only when each port carries one base format. With mixed channel counts at 16 reservations per port it is not met; that is an open owner question, not a claim.

## Linked Issue / roles

Relates to #640
Relates to #665
Relates to #823

This is the Mark II charter round; it does not complete #640.

Executor: `[A720b]` (round 1: `[A720]`)
Internal cleared-context reviewer: `[R757]`
External reviewer: `[R758]`

## Description

The owner decisions of 2026-10-31 on #640, #665 and #823, written into the requirements, the split contract, the area plan and a new datapath design. No RTL, firmware, generator, gate or configuration change.

| Commit | File | What changed |
|---|---|---|
| `4083cea5` | `docs/reference/FR_NFR.md` | Round 1: NFR-RES-01 Mark II ceiling; NEW NFR-LAT-03 (talker latency) and NFR-REL-03 (0.5 s save); NFR-SCOUT-02/03/05, the plane table, the out-of-scope note and the traceability rows amended. |
| `cf342310` | `docs/ARCHITECTURE_HW_SW_SPLIT.md` | Round 1: the split restated; no permanent all-fabric option; processor and, at F6, the fabric gPTP plane deleted at their switch-overs. |
| `8ad28659` | `docs/design/MARK_II_STREAM_ENGINES.md` (new), `docs/README.md` | Round 1: the 32x32 shared-engine datapath design. |
| `dfc310fb` | `docs/design/MARK_II_AREA_PLAN.md` | Round 1: target, measured basis, levers, LiteX stages, Block RAM ledger, decisions, lane sequence. |
| `7bcf9a9c` | area plan | The retired host-plane term replaced by "the host tools" (bare-metal scope gate). |
| `9aff05dc` | NFR-RES-01, area plan Target | The 60 % is recorded as the target the #234 ruling kept on 2026-10-03 for this redesign to meet, now replaced; the shipping image is held by the resource gate, with no other LUT bound. |
| `f38badda` | REQUIREMENTS.md, FR_NFR.md, overview architecture, area plan | Every placement, gPTP-owner and gPTP-deadline statement scoped "until the switch-over" or "until F6"; the lever 5 (MMCM servo in firmware) conflict with fabric-owned media published as an open owner decision. |
| `9140079a` | split, area plan, stream engines, FR_NFR.md | The gPTP software named `flexptpd`: source `kebag-logic/flexPTP` (MIT, a fork of `epagris/flexPTP`), branch `gptp` at `d116d3d`; its one global core state (one port per image) is the open redundancy item. |
| `f0cfa69c` | stream engines, NFR-LAT-03, area plan | Talker latency re-derived over every legal base-format mix: phase chosen at start by least wire time, never moved; shaper as an exact queue recursion; interference assumptions A1 and A2 stated; per-stream level shown never to bind; the pin-referenced latency instrument. |
| `3eb2f950` | stream engines, area plan | Wire load, engine load and render buffer at 48, 96 and 192 kHz; the 192 kHz reservation limit; the ledger books the 192 kHz buffer (four RAMB36). |
| `ec8ffd98` | stream engines | Each redundant copy carries its own port's time; listener merge rules that never drop the only copy of a packet, whatever its tu bit. |
| `790f7179` | stream engines | Register maps: every bit and offset defined or reserved, the not-mapped encoding, a per-slot render map (Milan v1.2 5.3.10.1), each Milan counter's reset event. |
| `119281c9` | stream engines, NFR-REL-03 | Compaction ordered so no saved change is lost without a power cut, with the power-cut cases; the save worst case gains the compaction page in flight and the second suspend (359.75 ms); `T-NVM-COMMIT-TIMEOUT` restatement assigned; every saved-state clause in the traceability row. |
| `f9786179` | area plan | Lever 6 netted of the kept timestamp return (+0.25k, 32x32 estimate ~21.45k); the lever 2 after lever 3 departure from D16 stated with its reason, for owner approval; Block RAM heading. |
| `3baf35c1` | REQUIREMENTS.md, split, overview, area plan | Changed sentences within ten words, changed paragraphs within twenty. |
| `f6b3e841` | stream engines | The 95.867 µs mixed-format figure bounded to 16-stream mixes. |

Key results (each marked in the pages as measured or estimated):

- **Talker latency at 16 reservations per port** (derived bound, pin to first bit, one interfering 1522-octet frame):

  | Rate | One base format per port | Mixed channel counts |
  |---|---|---|
  | 48 kHz | 63.431 µs worst: met | 92.530 µs reached, at most 95.867 µs: not met |
  | 96 kHz | 51.293 µs worst: met | 74.826 µs reached, at most 93.216 µs: not met |
  | 192 kHz | 32.071 µs worst (N up to 6): met | at least 72.915 µs before packetizer time: not met |

  Fewer reservations remain worse (three co-phased streams alone wait 83.012 µs for credit). Both cases are open owner question 1.
- **Save at 32x32:** 359.75 ms worst case at datasheet maxima, for change sets up to 32 pages.
- **Area:** about 21.45k LUTs on central estimates at 32x32 (17.8k to 25.45k), above the ceiling centrally.
- **Block RAM:** about 144.5 tiles estimated against 121.5 usable; firmware memory binds first.

## Round 2

Every finding and residue of R757-1 and R758-1 is closed below. The lane handoff carries each with file and line and its verification.

| Finding | Closure |
|---|---|
| R757-1-F1, R758-1-F1 (BLOCKER) | The term is gone; `check_baremetal_only.py --check` exits 0. Every docs-workflow step was run on the committed head (How to validate). |
| R757-1-F2, R758-1-F5 | NFR-RES-01 and the Target rows record only what was decided: the 60 % was kept on 2026-10-03 for this redesign to meet (#234 ruling, #640 original body) and is replaced by the 2026-10-31 ceiling; the resource gate holds the shipping image. No "Mark I bound". |
| R757-1-F3, R758-1-F4 | REQUIREMENTS.md section 1 and the section 4 preamble, FR_NFR.md 1.2, 2.0, NFR-LAT-02, NFR-SCUP-02, NFR-SCOUT-01, NFR-OBS-01, the 3.4.2 placement line, the plane table and the 4.3 diagram, and the overview are scoped to the switch-over or F6. The reviewers' greps return only scoped, transition, current-image or test-oracle lines. Lever 5 against fabric-owned media is an open owner decision (NFR-SCOUT-02, area plan). |
| R757-1-F4, R758-1-F2 | The stagger is by wire time, chosen at start, never moved (IEEE 1722-2016 7.6). An executable model covers every legal mix of N in 1, 2, 4, 6, 8 at 16 reservations per port at each rate, by exact search where it fits and by a sound superset with reachable witnesses otherwise. Results above; mixed formats are not presented as met. |
| R758-1-F3 | Seven-step compaction order (copy, replay the active tail above S0, repeat until nothing is dirty, then commit); boot applies records in sequence order; a power-cut table. NFR-REL-03 and the verification plan name the host flash-model test. |
| R757-1-F5, R758-1-F11 | `flexptpd`, from the public MIT fork, branch `gptp` at `d116d3d`; one port per image today, open for redundancy. |
| R757-1-F6 | Assumptions A1 (no own frame above 1522 octets) and A2 (no LPI) stated for the implementation to enforce and test; IEEE 802.1BA-2011 6.3 attribution corrected (2000-octet cap; 16.160 µs shown). |
| R757-1-F7, R758-1-F6 | 4.3.4 cites `[802.1Q]` 34.6.1, which is IEEE 802.1Q-2014; 802.1Q-2022 numbers it 34.6.1.1. N in 1, 2, 4, 6, 8. The listener map cites 5.3.10.1. The saved-state row lists 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.8.2, 5.3.8.3, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 and 5.5.2.4. |
| R757-1-F8 | The Mark II taps start at the pin instant of the packet's last sample (frame-end stamp less the synchronizer delay and the slots after the stream's last slot) and end at the first bit plus the PHY egress constant. NFR-LAT-03's test names them. |
| R757-1-F9, R758-1-F8 | Render buffer per rate (1, 2, 4 RAMB36 for 2.25 ms, above Milan v1.2 4.4.2.1's 2.126 ms); the ledger books four; the 192 kHz reservation limit (at most 13 eight-channel streams with a CRF) and the engine load per rate (33.47, 58.05, 92.67 %). |
| R757-1-F10 | T_worst adds one compaction page and a second suspend: 359.75 ms. `T-NVM-COMMIT-TIMEOUT` (8,000 ms) restatement assigned to #823 and #665 F1, listed open. |
| R757-1-F11, R758-1-F10 | Every bit and offset defined or reserved; PORT's index-parity reset stated as a rule; 15 marks a talker channel not mapped; VID is 12 bits; talker counters cleared when RUN rises (5.3.7.7), listener counters by CNT_CLR on binding (5.3.8.10). |
| R757-1-F12 | Lever 6 nets 4,944 of 5,194; +0.25k; central ~21.45k. |
| R757-1-F13, R758-1-F12 | Lever 2 is credited through LiteX stage 3, so it lands after lever 3; stated with its reason, as a proposal for owner approval. |
| R758-1-F7 | CDC basis matches its value (0.080 µs rounded up to 0.200 µs); the "any order" claim is replaced by what the rule can reach. |
| R758-1-F9 | Each copy uses its own port's time base; the merge renders a tu copy when it is the only one and lets a clean copy replace it. |
| R757 R1, R2, R3 | Applied as written (R2 split for the ten-word limit). |
| R758-1-R1 | The owner rule reads "20 to 30 words at most", an upper bound; the repository's stricter limits (10 words per sentence, 20 words and 2 sentences per paragraph) hold on every changed block of every touched page. |
| Suggestions | R757 S1 to S4 and R758 S1 to S6 taken (per-stream level, merge cases, one PHC per port, CRF phase by the rule and last in its phase, 4.4.2.1, 5.3.8.1, read-back retry and the 40 µs spacing, the 16:51 link). |

## Authoritative references

- #640 body ("Updated 2026-10-31") and comments of 2026-10-31; #665 body and comments of 2026-10-31; #823 body and comments of 2026-10-31; the #234 ruling of 2026-10-03; the #640 core survey of 2026-11-01 (the gPTP fork).
- IEEE 802.1Q-2022 8.6.8.2, 34.3.1, 34.6.1, 34.6.1.1, 34.6.1.2, L.3.1.1; IEEE 802.1Q-2014 34.6.1 (Milan's reference).
- IEEE 1722-2016 4.4.4.3, 4.4.4.6 to 4.4.4.9, 7.5, 7.6.
- IEEE 1722.1-2021 7.2.6.
- IEEE 802.1AS-2020 8.4.3.
- IEEE 802.1BA-2011 6.1, 6.3.
- Milan v1.2 4.3.3.2 (Table 4.4), 4.3.4, 4.4.2.1, 4.4.2.3, 5.3.5.1, 5.3.7.1, 5.3.7.3, 5.3.7.6, 5.3.7.7, 5.3.8.1, 5.3.8.2, 5.3.8.3, 5.3.8.7, 5.3.8.10, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13, 5.5.2.4, 6.2 (Table 6.1), 8.2.2 to 8.2.5, 8.3.1 to 8.3.5, Annex C.
- N25Q128 datasheet Table 32 (tPP 5 ms, tSE 3 s, tSSE 2 s maxima), Table 17 (suspend parameters), section 9.1.20.
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 9.4; `docs/design/SPLIT_CONTROL_MEMORY.md` section 5; `docs/design/MAILBOX_SPLIT.md` measured area.

## How to get into the same state

```sh
git fetch origin
git checkout 640-mark2-charter
git log --oneline e5b8405d..HEAD     # sixteen commits, one per file group or finding group
git submodule update --init --depth 1 third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
python3 -m venv "$HOME/gatevenv"
V="$HOME/gatevenv/bin/python3"
"$V" -m pip install --quiet pyyaml wavedrom==2.0.3.post3
"$V" -m pip install --quiet --require-hashes -r tools/markdown/requirements.txt
"$V" -m pip install --quiet --require-hashes -r tools/hdl_reference/requirements.txt
# the pinned RV32 SDK, into a prefix that does not exist yet
"$V" scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
```

The gates also need `rsvg-convert`, `sv2v` and `tclsh` on the path, as the workflow installs them.

## How to validate

Every step of `.github/workflows/docs.yml`, run as its jobs run them, with the venv first on `PATH`:

```sh
export PATH="$HOME/gatevenv/bin:$PATH"
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py && python3 scripts/check_gptp_docs.py --selftest
python3 docs/DOC_MAP.gen.py --check && python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check && python3 docs/diagrams/timesync_chain.gen.py --selftest
python3 scripts/check_solution_docs.py && python3 scripts/check_solution_docs.py --selftest
python3 docs/diagrams/submodule_boundaries.gen.py --check && python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py && python3 scripts/check_submodule_docs.py --selftest
python3 scripts/gen_wavedrom.py --selftest   # and the three --check runs of the workflow
python3 scripts/check_diagram_pngs.py && python3 scripts/check_diagram_pngs.py --selftest
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/check_gptp_docs.py --with-submodule && make -C gptp-processor docs
python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_doc_paths.py
python3 scripts/check_archive.py && python3 scripts/check_archive.py --selftest
python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check
# then the code-quality, source, NVM, shape, CI-control, builder-leg, events and act-runner steps
# of docs-gates-0/1/2, the wire-accountability self-test, and docs-check-no-git on an exported tree
```

Expected result / pass criteria: every step exits 0.

Recorded at `f6b3e841` (every step ran sequentially on a clean clone with the four submodules the jobs fetch):

| Job | Steps | rc |
|---|---|---:|
| wire-accountability | `check_wire_accountability.py --self-test` | 0 |
| docs-check-no-git | `docs_check.py`, `check_feature_status.py` without `.git` | 0 |
| docs-gates-0 | HDL reference; docs_check (0 findings, 211 pages); em dash (0 over 1,426 added lines in 7 pages); doc style and gPTP docs; diagram, solution and submodule no-drift; WaveDrom; PNGs; feature status; traceability; imported gPTP docs; measurement self-tests; **bare-metal scope (0 findings over 1,425 files)**; RV32 SDK; compiler-absent controls; NVM record space, capture census and writer; SoC and RTL source lists; naming, port-contract, fail-fast, TODO, test-evidence and hygiene ratchets; SV, C/C++, Python and shell idioms; cited paths (1,075); archive; contents (`--selftest`, `--verify-anchors`, `--check`); AEM store; sweep, deploy and entity shapes; CI scheduling controls | 0 each |
| docs-gates-1 | builder leg 0: ALL GATES PASS | 0 |
| docs-gates-2 | builder leg 1: ALL GATES PASS EXCEPT 16 NOT RUN; CI events; act runner contract | 0 each |

Builder leg 1's 16 NOT RUN gates skip by their own rules: 15 need migen and LiteX, which the docs workflow does not install, and one needs a local build report. The docs-check union step reads GitHub artifacts and runs only there, and act needs a pushed head, so neither ran locally.

`check_doc_style.py`'s own `analyze()` over every changed block of the 7 touched pages: 0 findings (10 words per sentence, 20 words and 2 sentences per paragraph).

The shaper model and its output are lane evidence, not a gate; an implementation lane must turn the model into a self-checking test. Its digest is in the handoff.

## Known limitations / out of scope

- Documentation only: no RTL, firmware, generator, gate, configuration or saved-state format change. The format and flash layout belong to #823, the writer to #665 F1, gPTP to #665 F6.
- **Open owner question 1: talker latency with mixed formats or fewer reservations.** The phase rule balances wire time only when a stream starts; when other streams stop, heavy frames can stay clustered while idleSlope falls with the reservations. Re-phasing a running stream breaks IEEE 1722-2016 7.6 and padding a reservation breaks Milan Table 4.4. The owner called 65 µs ideal; the choices include accepting the derived bounds, one base format per port, re-phasing with an audio gap, or another stagger or shape.
- The derived bounds rest on assumptions A1 (no own frame above 1522 octets on an AVB port) and A2 (no LPI); with 2000-octet frames the interference term is 16.160 µs instead of 12.336 µs.
- At 192 kHz the shared engines reach 92.67 % load and the latency there was bounded only before packetizer time for mixed formats (open question 7).
- **Open owner question: save bursts.** The 0.5 s bound holds while the records changed during one save fit 32 pages and sustained saves stay below 10 % of the flash's worst-case write rate.
- Table 17 of the flash datasheet gives only typical suspend timings; the derivation allows 1 ms per suspend and the implementation must measure it.
- The 500 ms debounce window uses the whole bound and the 1,000 ms window exceeds it; `T-NVM-COMMIT-TIMEOUT` must be restated. Both belong to #823 and #665 F1.
- Lever 5 (MMCM servo in firmware) conflicts with fabric-owned media (NFR-SCOUT-02/03), and lever 2 is proposed after lever 3: both are open owner decisions in the area plan.
- Block RAM: about 23 tiles over the usable 121.5 on estimates; reductions are unmeasured.
- Area: the central 32x32 estimate is about 21.45k, above the ceiling.
- The measured basis comes from a qualification-image build whose source commit is not on dev; the report digests are recorded in the plan.
- The adopted `flexptpd` fork serves one port per image; two ports are an open item for #665 F6.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (charter round only; #640's acceptance needs the implementation lanes)
- [ ] New or changed behavior has self-checking tests (no behavior change)
- [x] Required local verification bar passes (every docs-workflow step above)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
