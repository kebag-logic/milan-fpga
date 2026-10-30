[A706]

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

GREEN: 96 of 96 local docs-workflow gate commands rc 0 at head `bd16b371`. Branch `797-d0-audit` -> `dev` (base `1e80128f`).

## Linked Issue / roles

Relates to #797

This is lane D0 of the sweep (the inventory and verification audit). It must not close #797: the area lanes follow it.

Executor: `[A706]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

| Piece | Change |
|---|---|
| `scripts/docs_inventory.py` (new) | Generator for the documentation inventory. It lists every tracked Markdown file and README with its area, line count, audience, purpose, what it describes and a status (current, stale, superseded, obsolete), each status with its evidence. `--check` is the freshness gate, `--selftest` runs 21 planted controls, and `--findings-dir` writes one findings file per area lane. |
| `scripts/docs_inventory.json` (new) | The verification baseline (`1e80128f`) and 23 verified contradictions. Each one quotes the statement exactly, names the contradicting source line or clause, and gives the correction. |
| `docs/DOCUMENTATION_AUDIT.md` | Regenerated from the generator: 210 documents, 89,111 lines; 182 current, 7 stale, 21 obsolete. Marked GENERATED. It replaces the hand-written 2026-08-31 page, whose three follow-up issues are closed. |
| docs workflow | A new step, "Documentation inventory freshness gate", after the Contents gate. The template, the generated workflow, the `ci_events.py` step pin, its self-test's step count and the CI image command table move together. |
| Three one-line fixes | `docs/guides/VERIFICATION_DEVELOPER.md:129` named a deleted LiteX test. `docs/README.md:72` called implemented media-clock following "proposed". `docs/reference/REGISTER_MAP.md:428` pointed at the closed #599 instead of its finding. |

Findings by area lane: overview and guides 6 (all in `README.md`); reference 17. The reference findings are 8 in `REGISTER_MAP.md`, including the ETH_GUARD row and the PHY_RESET, LINK_CTRL[1] and MAC_STATUS rows from the scope addition; 3 in `BAREMETAL_FIRMWARE.md`; 2 each in `FR_NFR.md` and `MILAN_COMPLIANCE_MATRIX.md` (CBS marked met or implemented, but not instantiated since 0x0056); and 1 each in `REGISTER_MAP_CLASSES.md` and `BOARD_PORTING_AX7101.md`.

Two statements in the issue's scope addition do not match the code at the base. ETH_GUARD does not gate the LiteX PHY clock/reset block's reset: the SoC exports the signal "for future SoC-side gating". And the firmware does publish MAC_STATUS from MDIO, while its saved-state writer runs. The findings record the code's behaviour; the gating itself needs a decision.

## Authoritative references

- #797 scope items 1, 2 and 6, its rules and acceptance; the scope addition (issuecomment-6489587365); the plan, section D0 (issuecomment-6518880512).
- [CONTRIBUTING.md section 6](../CONTRIBUTING.md#6-documentation-wording-and-privacy) and the em-dash rule.
- REQ-CSR-01 (the map matches the RTL decode), REQ-MAC-03, FR-QOS-01..03.
- IEEE 802.1Q-2022 35.2.2.7.2 and Table 35-3; IEEE 1722.1-2021 Table 7-156; Milan v1.2 5.3.8.10 and Table 5.6; IEEE 802.1AS-2011 10.3.10.2.1 d).

## How to get into the same state

```sh
git fetch origin
git switch 797-d0-audit
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 scripts/docs_inventory.py --check
python3 scripts/docs_inventory.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/check_baremetal_only.py --check
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
```

Expected result / pass criteria: every command exits 0. To see the gate fail, append a line to any tracked
Markdown file: `--check` then exits 1 and names the first differing line of the page.

## Known limitations / out of scope

- D0 verified the release-facing pages only. Every other page is marked "area lane" in the Verified column.
- `BUILDING.md`, `BAREMETAL_FIRMWARE.md` and `PP_DESCRIPTOR_OWNERSHIP.md` received the mechanical checks only (commands, clause numbers, register offsets, identifiers, open-issue claims). Release lanes hold the first two.
- No page is rewritten here. Findings on pages held by running lanes wait for those lanes.
- `ci/image/tool-inventory.json` and the dated execution-audit receipt are not regenerated. That generator needs the CI image's pinned shell parser, so it belongs to the next CI-image round.
- The page carries each document's line count, so a PR that edits a Markdown file reruns `python3 scripts/docs_inventory.py --write`, as it reruns `gen_toc.py --write` for headings.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (D0's part: the generated audit lists every document with a status)
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
