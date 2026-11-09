# [A754c] HANDOFF: processor issue #216, round 3 (docs only)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `216-mrp-applicant`.
- Base (source): main `044cb25f`. Round 2 head: `84f6d6ad77d51d678f8efdf26b45aae011a42001`.
- **Head: `03862f75c89e5c1d84baa4735eff1c1c6f796e25`** (one commit on top of `84f6d6a`, one-line subject, no body).
- Authority: the manager round 3 ruling on #216 (issuecomment-6751398007), on R802-2 (NEGATIVE, one MINOR, F1;
  residue R1, R2) and R801-2 (POSITIVE). S1 and S2 of both reviews: not this round (residue checklist at merge).
- Nothing pushed. TAKEN posted (issuecomment-6752816272). PR-BODY.md: round 2's, with the head moved, GAP-19 added
  under "Known", and a "Round 3 (docs only)" section.

## Changes (each with its clause)

| Ruling item | Where at head | Change | Clause |
|---|---|---|---|
| 1, F1 (option a) | `docs/architecture/10_srp_engine.md:525-530` | "Flush! is a Registrar event only (§10.7.5.2)" replaced by "Table 10-3 has no Flush! row, so LINK_DOWN leaves the Applicants as they are"; then: "§10.7.5.2 also signals leavealltimer! to the LeaveAll state machine at a Flush!; this engine's LINK_DOWN does not, on either participant, since issue #216 changes no MRP timers ([00 GAP-19])" | 802.1Q-2018 Table 10-3, 10.7.5.2 (second paragraph), 10.7.5.22 |
| 1, gap register row | `docs/00_MILAN_COMPLIANCE_REVIEW.md:384-392` (GAP-19 finding), `:609` (F00.2 row, owner "owed, not filed"), `:546` (REQ-SRP-001 Finding column) | GAP-19 [Minor]: LINK_DOWN (Flush!) does not signal leavealltimer! to the LeaveAll state machine of MSRP or MVRP; disposition kept, since #216 changes no MRP timers (Milan v1.2 Table 4.3) | 10.7.5.2, 10.7.5.22, 10.7.9 / Table 10-5 |
| 2, R1 | `docs/architecture/10_srp_engine.md:536-537` | "(below)" replaced by R802-2's exact text: "A link change does not reset `vid_sent_o`, the talker's streaming licence of [Join before the stream](#sec-10-join-before-stream) below." (wrapped at the paragraph's width) | none (wording) |
| 3, R2 | `docs/architecture/10_srp_engine.md:509-510` | line break after "never JoinIn without IN."; no other change | none (wording) |

Why GAP-19 is three edits in 00: `scripts/check-matrix.py` fails a GAP that is defined but has no disposition row
(F00.2), and one that no REQ row covers. The finding text is the register entry, the F00.2 row is its "one row"
with its owner, and REQ-SRP-001 (Milan Table 4.3, the MRP timers, leavealltimer among them) is the REQ row whose
timer the omission concerns. No open issue owns it (open issues: #210, #216, #217, #220; #220 is the stream
Applicants' Begin! at LINK_UP, not the LeaveAll machine), so its owner reads "owed, not filed", as ruled.

RTL fact behind the disclosure (read only, unchanged): `link_up_i` reaches only `KL_srp_domain`, `KL_srp_vlan` and
`KL_srp_listener_fsm` (`hdl/srp/KL_srp_top.sv:399,476,670`); no LeaveAll state machine takes it.

## New checks and planted mutants

None. The ruling makes this round docs only: no RTL, testbench or generated-file change. The new GAP-19 is
checked by the existing matrix gate (`matrix: 115 REQ rows, 19 GAP findings, OK`) and the link gate
(`links: 1334 checked, OK`, the new `#gap-19` and `#sec-10-vid-link` anchors among them).

## Gate table (clean clone of the head; receipts/gates/*.cmd, .log, .rc, .start, .end)

Python from the lane's docs virtualenv (3.12.3, `receipts/gates/python.log`); Mermaid CLI 11.16.0, the CI pin.

| Gate | Command | rc | Result |
|---|---|---|---|
| head | `git rev-parse HEAD` | 0 | `03862f75c89e5c1d84baa4735eff1c1c6f796e25`; clone status empty before the gates |
| hdl.yml docs-gates | `mmdc --version` | 0 | `11.16.0` |
| hdl.yml docs-gates | `make check` | 0 | `lint: 41 mermaid + 18 wavedrom blocks checked, OK`; `wavedrom: 18 blocks checked, OK`; `links: 1334 checked, OK`; `matrix: 115 REQ rows, 19 GAP findings, OK`; `req-tags: 115 REQ rows: 101 traced, 8 waived, 6 need no check; 266 tags in 20 files, OK`; `matrix: OK (94 rows, 0 untested)`; `parameters: top 29, guide 29, diagram 29, OK`; AECP commands, ids, figures OK |
| module matrix | `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` |
| whitespace | `git diff --check 84f6d6a HEAD`; `git diff --check 044cb25f HEAD` | 0, 0 | empty, empty |
| tree outside docs/ | `git diff --stat 84f6d6a..HEAD -- . ':(exclude)docs'` | 0 | empty (0 bytes): byte-identical to `84f6d6a` |
| delta | `git diff --stat 84f6d6a..HEAD` | 0 | `docs/00_MILAN_COMPLIANCE_REVIEW.md | 13 ++++++++++++-`, `docs/architecture/10_srp_engine.md | 17 +++++++++++------`, `2 files changed, 23 insertions(+), 7 deletions(-)` |

Not re-run, as ruled (the tree outside `docs/` is byte-identical to `84f6d6a`): the suite sweep, the campaigns,
portability, nvm_port figures, area, the scratch parent and the twin. Their round 2 results stand.

## Scratch-parent consumer gate

Not re-run this round. Round 2 (`84f6d6a` pinned on milan-fpga dev `ac0a01e3`): 40 gates rc 0; the twin reports
`fabric-mvrp-leave-all`, `fabric-domain-one-new` and `fabric-vid2-join-in` as "the defect has gone". The pin moves
only by `docs/`, which no parent gate builds from.

## Receipts

`receipts/INDEX.md` (generated from the files present). `receipts/STANDARDS.txt` records the clauses read
(802.1Q-2018 10.7.5.2, 10.7.5.22, 10.7.9 / Table 10-5). `receipts/gates/diff-84f6d6a-HEAD.patch` is the whole
round 3 delta.
