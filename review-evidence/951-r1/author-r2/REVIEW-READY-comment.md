[A801] REVIEW READY (round 2)
Commit: f09d82e05270bdd77e07f7fc2e14d064c1123be8 (`951-redeclare`, PR #952 against `flip-train-1117`; round 1's `0d1eb8e4` plus two commits, `e7b0272b` and `f09d82e0`)

Changed: comments and docs only, answering R870-1 (#952 issuecomment-7012143102) and R869-1's two residues (#952 issuecomment-7012716515). The formula and the values (3,023, 3,027 and 3,030 cs) are unchanged.
- **F1 (Conformance, Docs).** The chosen maximum is now stated as IEEE 802.1Q-2018 10.7.4.3's nominal random-draw maximum, a peer's too. Milan v1.2 Table 4.3's further tolerance, a leavealltimer up to 15.5 s, is stated as not covered: two periods at its edge reach 31 s, against the ruling's nominal 30 s.
  - Where: `srp_mbx.c:35-36,40-41` (comment only, same line count), `srp/README.md:225,234-242,532`, `MAILBOX_SPLIT.md:1290-1293` and `SPLIT_CONTROL_MEMORY.md:2855,3003,3171,3173`. Also the test comments that cited Table 4.3 for the 1.5 x (`srp_gate.hpp:330-331`; `srp_talker.cpp:8,52` and `srp_gate.hpp:6` say "nominal"). The failure words and plant needles are unchanged.
- **F2 (Tests, Docs).** "The CPU rows carry" is gone. The text now gives the sample's scope: the `valid-destinations` arm, five arm A groups at 1x1/1if and four at 8x8/1if. Most of arm A, both answering arms and 8x8/2if are not measured, so no omitted row is shown to carry. The complete timing validation is PENDING at the flip train's final head, where the train measures every row at every point again (`SPLIT_CONTROL_MEMORY.md:3184`, the PR body).
  - `ctrl_service_budget/README.md:261` states the formal pass's completeness rule (`record_classes.py` refuses a pass that did not run every arm A group). It claims nothing of this change, so it is unchanged.
- **F3 (Docs).** The code after the instruction moves 4 bytes. `.rodata` moves 0 or 8 bytes, by its alignment: 0 in 13 of the 20 images, the platform's four among them, and 8 in 7. SRAM does not move (`SPLIT_CONTROL_MEMORY.md:3176`, the PR body).
- **RS1.** The PR body for the manager names `[R869]` (internal) and `[R870]` (external).
- **R869-1 RES-1.** `SPLIT_CONTROL_MEMORY.md:2857`, #901's record, now gives the renamed test's #951 name beside its old one.
- **R869-1 RES-2.** `ctrl_service_budget/talker_notice.py:22-23`'s docstring says the new range waits two nominal longest LeaveAll periods, about 30 s. Nothing reads that docstring.
- **R869-1 SUG-1** (cover Table 4.3's tolerance?) is the maintainer's to decide. This change keeps the ruling's nominal value and now says in-tree that the tolerance is not covered (F1). **SUG-2:** the bench measurement stays not done.

Validation:
- Executable inputs are unchanged. All 20 images at `e7b0272b` are byte-identical to round 1's (`f09d82e0` changes only a design page and a harness docstring, neither an image input): the CPU budget harness's 12, and the platform's and size fixture's 8, whose ledger passes.
- No line other than a `//` comment changes in `srp_mbx.c` or the test files, and their line counts are unchanged, so the cited line numbers still hold.
- Talker arms at `e7b0272b`: PASS, `srp_talker.cpp` 16 and 16 at 1x1/1if and 8x8/2if, and `SrpGate` 9.
- Docs workflow steps at `f09d82e0` (and at `e7b0272b`): PASS, 104 of 104, tracked files unchanged after them (installs skipped; the candidate's own `act_ci.py` self-test runs only inside the CI job, by AGENTS.md). The two end-station builder legs carry from round 1's `0d1eb8e4`: no input of theirs changed but comments and docs.
- Carried from round 1's code head `4224df63`, since the images are byte-identical and only comments changed: the firmware gate with its campaigns, fw_coverage, and the twin with its plants.

Acceptance criteria: as in round 1. The reference device's delay after a conflict is not measured (no bench access).

Open risks/questions:
- R869-1 (internal) is POSITIVE at `0d1eb8e4`; its two residues are folded in here.
- The complete CPU timing validation is pending at the flip train's final head.
