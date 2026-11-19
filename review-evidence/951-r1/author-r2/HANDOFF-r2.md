# [A801] #951 round 2 — R870-1's findings: comments and docs only — handoff

Status (17:00): **REVIEW READY (round 2).** Head `f09d82e0` (round 1's `0d1eb8e4` + two comments-and-docs commits, `e7b0272b` and `f09d82e0`),
committed, not pushed. R870-1's F1, F2, F3 and RS1, and R869-1's RES-1 and RES-2, resolved (section 2); no code change needed. All 20 images
byte-identical to round 1's; docs workflow steps 104 of 104 at both round 2 heads; Talker arms PASS. Posted: `[A801] REVIEW READY` (round 2)
on #951 (section 6). The complete CPU timing validation stays pending at the flip train's final head.

## 1. Input
- PR #952 (base `flip-train-1117`), opened by the manager at round 1's head `0d1eb8e4`.
- R870-1, external: NEGATIVE at `0d1eb8e4`, three MINOR and one RESIDUE, no functional defect (#952
  issuecomment-7012143102; the full report read in full).
- R869-1, internal: still running at the round's start; it posted POSITIVE at `0d1eb8e4` at 14:55 (#952
  issuecomment-7012716515), seen before posting, with two RESIDUE and two SUGGESTION. The residues are wording, in this
  round's docs-only scope, so they are folded in (`f09d82e0`) rather than left for a further round.
- Manager's round 2 scope: docs and comments only; keep the approved formula and value; show the images unchanged;
  re-run the docs steps; STOP if a code change turns out to be needed (none did).

## 2. RESOLUTIONS
| Finding | Lens | Resolution | Where (at `e7b0272b`) | Verification |
|---|---|---|---|---|
| R870-1-F1 MINOR: the maximum claimed for Milan-permitted timers is stronger than the nominal bound implemented | Conformance, Docs | The chosen maximum is stated as 802.1Q-2018 10.7.4.3's **nominal** random-draw maximum, a peer's too. Milan v1.2 Table 4.3's further tolerance (a leavealltimer up to 15.5 s) is stated as **not covered**, two periods at its edge reaching 31 s against the ruling's nominal 30 s. Formula and values unchanged (3,023 / 3,027 / 3,030 cs). | `srp_mbx.c:35-36,40-41` (comment only, same line count, so `:32-46` and `:526-527` still hold); `srp/README.md:225,234-242,532`; `MAILBOX_SPLIT.md:1290-1293`; `SPLIT_CONTROL_MEMORY.md:2855,3003,3171,3173`; `ctrl_service_budget/README.md:329`; the test comments `srp_talker.cpp:8,52` and `srp_gate.hpp:6,330-331` (comment only: the Milan citation now names Table 4.3 for the 10 s only) | Images byte-identical to round 1's (section 3); no non-comment line changed (`receipts/change/non-comment-lines.txt`) |
| R870-1-F2 MINOR: "the CPU rows carry" overstates a sample | Tests, Docs | The claim is replaced by the sample's scope (the `valid-destinations` arm, five arm A groups at 1x1/1if and four at 8x8/1if; most of arm A, `answering-every-port`, `answering-ports` and 8x8/2if omitted) and the complete timing validation is marked **PENDING at the flip train's final head**, where the train measures every row at every point again on that head's images. `ctrl_service_budget/README.md:261` was read: it states the formal pass's completeness rule (`record_classes.py` refuses a pass that did not run every arm A group) and claims nothing of this change, so it is unchanged. | `SPLIT_CONTROL_MEMORY.md:3184` (a new last bullet); PR body (Status, Description, Known limitations); this round's comment | Text review against the round 1 receipts (`cpu/`); the harness README line quoted in the receipts |
| R870-1-F3 MINOR: `.rodata` "moves 8" is wrong in 13 of 20 pairs | Docs | The code after the instruction moves 4 bytes; `.rodata` moves 0 or 8 bytes by its alignment, 0 in 13 of the 20 images (all four platform images among them) and 8 in 7; SRAM does not move. | `SPLIT_CONTROL_MEMORY.md:3176`; PR body (image diff) | `receipts/images/rodata-shifts.txt`, from the 20 round 1 pair receipts |
| R870-1-RS1 RESIDUE: reviewer placeholders | Docs | The PR body names `[R869]` (R869-1, internal) and `[R870]` (R870-1, external), as the review-start comments on #952 assign them. | PR body, Linked Issue / roles | #952's two `INDEPENDENT REVIEW STARTED` comments |
| R869-1 RES-1 RESIDUE: a renamed test still named by its old name | Docs | #901's historical bullet keeps the old name and gives the #951 name after it. | `SPLIT_CONTROL_MEMORY.md:2857` | `git grep WaitsTwoLeaveAllTimePeriods` finds only that annotated line |
| R869-1 RES-2 RESIDUE: a stale docstring beside its restated sibling | Docs | "two LeaveAllTime periods" becomes "two nominal longest LeaveAll periods, about 30 s (#951)"; nothing reads the docstring. | `tb/verilator/ctrl_service_budget/talker_notice.py:22-23` | `git grep "two LeaveAllTime periods" tb/verilator/ctrl_service_budget` finds nothing; the module parses |
| R869-1 SUG-1: cover Table 4.3's tolerance? | Conformance | The maintainer's decision; the ruling's nominal value is kept and F1 now says in-tree that the tolerance is not covered. | — | — |
| R869-1 SUG-2: the conditional bench measurement | Docs/process | Not done: no bench access. | — | — |

## 3. Image identity (round 2 against round 1)
- CPU budget harness, 12 images at `e7b0272b`: byte-identical to `4224df63`'s and `e5dee83b`'s (`hashes.txt` equal).
- Platform (4) and size fixture (4) at `e7b0272b`: byte-identical to `4224df63`'s and `e5dee83b`'s; `plat_ledger.py`
  PASS (0 findings), every fixture link rc 0.
- So all 20 images are byte-identical to round 1's, and the round 1 image diff, relinks and CPU legs carry by
  byte identity.

## 4. Gates
| Gate | Result |
|---|---|
| Docs workflow steps at `e7b0272b` | PASS, 104 of 104, tracked files unchanged after them |
| Docs workflow steps at `f09d82e0` | PASS, 104 of 104, tracked files unchanged after them |
| Docs builder legs 0 and 1 | carried from round 1's `0d1eb8e4` (PASS, one declared NOT RUN arm each): only comments and docs changed |
| Talker arms at `e7b0272b` (test comments only) | PASS: `srp_talker.cpp` 16 + 16 (1x1/1if, 8x8/2if), `SrpGate` 9 |
| Firmware gate, fw_coverage, twin | carried from round 1's code head `4224df63`: the images are byte-identical and the only source and test changes are comments (`receipts/change/non-comment-lines.txt`) |

## 5. Open
- R869-1 (internal) is POSITIVE at `0d1eb8e4`; its two residues are folded in.
- The complete CPU timing validation is pending at the flip train's final head (F2).
- The reference device's delay after a conflict: not measured (no bench access).

## 6. Posting
- `[A801] REVIEW READY (round 2)`: #951 issuecomment-7014462971 (the text is `REVIEW-READY-comment.md`).
- Nothing else posted; no existing comment edited. Commits `e7b0272b` and `f09d82e0` on `951-redeclare`, not pushed.
  `PR-BODY.md` is round 2's body for PR #952 (from the published body, `PR-BODY-published-r1.md`), for the manager.
