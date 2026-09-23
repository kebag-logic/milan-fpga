# [A209] handoff: #408 + #409 boot gate 1b retirement

State: REVIEW READY, not pushed, no PR opened (not in this lane's authority).

- Lane: `$LANES/408-409-boot-gate-retire`, branch `408-409-boot-gate-retire`
- Base: dev `759da623072358afdb0e9d570a7b4b6a788492c9`
- Head: `a13b6e2e461695cdb8d978444ae499a5a6745429`, one commit, one-line subject, no trailers
- Files: `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md`, `docs/testing/CI_WORKFLOWS.md`
- Public comments: `[A209] TAKEN` on #408 and #409 (posted by the first session, not repeated); `[A209] REVIEW READY` on both.
- `PR-BODY.md` beside this file is the body to open the PR with (starts `[A209]`, carries `Closes #408` and `Closes #409`).

## What the session did

The first session left an uncommitted edit of `test_builder.py`, plus base measurements and a probe driver. This session read it, kept it, and finished it:

- New controls: the define half of the preprocessor rule (kept for the verifier group, where dev did NOT refuse it; narrowed elsewhere); the 16-selection bound; the macro rule's narrowed half (store value built in a read macro, identity forged through a read macro); the verifier's QSPI-slot condition made false in the stub tree; a spliced `PP_CTRL` redefinition.
- Accepted cases added: an `#ifdef`/`#else` choosing a `#define`; a fifth inline-asm statement (a fence), so the asm set has an accepted case of its own.
- `assert_rejected` takes a tuple of reasons (all required), with a negative control. The arm-selection entries are pinned on `SELECTION_PIN` plus the property.
- Stale "nothing is retired" comments and prints corrected; the page rewritten; CI_WORKFLOWS line corrected.

## Evidence (receipts/, see receipts/README.md)

- Base: gate 1b at `759da623` with SDK 217/217, absent 182/182, 17/17 + 4/4.
- Head: gate 1b with SDK 228/228, absent 167/167, 27/27 + 4/4, exit 0 both.
- Whole builder at head: SDK exit 0 (`EXCEPT 1 NOT RUN`, gate 11); absent exit 0 (`EXCEPT 2 NOT RUN`).
- Accepted cases at base: all 11 texts RED on their retired rule's own sentence, both environments (40-accepted-at-base).
- Disconnect runs at `a13b6e2e` (41-disconnect/summary.txt): `-E` + census + resolver 12/12 pass the whole gate; `-H` 3/3; census + resolver 10/10; per-selection grading 15/15 fail their pin (4 pass the whole gate) and 6/6 without RV32 (1 passes). Unpatched control: 15/15 and 6/6 still refused.
- Static and docs gates: 38 commands, all exit 0 (20-static-gates.log).

## Open points for the reviewers

1. #409 acceptance 4: the two helper-body stores are pinned on the helper's return-provenance rule, which answers first on every machine. The resolver's refusal of them is asserted by the blindness control on every compiler run. Stated in the PR body and the page.
2. Without an RV32 compiler the retired rules' protection is `NOT RUN`, by design. The hosted builder jobs pass `--require-rv32`; the docs job's `--absent` control passes with the weaker verdict.
3. Pre-existing, measured, not changed: a plain second `#define` of a register name passes the text rules without a compiler (on dev too); the resolver refuses it. It could be a follow-up issue; the manager decides.
4. `-E` caveat (stub-tree macro definitions) and `-H` caveat (tree it is handed) are written at the sites and in the page.

## Not done (out of authority)

No push, no PR creation or edit, no merge, no act or Docker, no full banks, no hosted runs, no hardware.

## Tools (tools/)

- `probe.py`: runs gate 1b from an in-memory patched copy (`--patch`, `--labels`, `--collect`, `--grade-cases`, `--dump-cases`), SDK mapped or absent.
- `run_builder.py`: runs the whole builder main with the SDK mapped (`--require-rv32`) or every cross compiler hidden.
- `static_gates.sh`: the docs-workflow checks this diff touches, ratchets last.
