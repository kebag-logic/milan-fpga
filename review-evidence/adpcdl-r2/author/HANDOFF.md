# [A849] tsn-c-stack #37, PR #38, round 2

**Status: DONE, committed, not pushed, nothing posted.** Head `ec727b64663b4eef2fc8da1ea5e0eae6541597d1` (tree `00b9b9ee`), one commit on `e0b1449`. ETA: none left in this lane.

## Changes since e0b1449 (no production source)
- `tests/test_adp.cpp`: `AcceptsLongControlDataLength` sweeps 57 to 2047 in a fresh 82-octet allocation each time, and keeps 57, 84 and 2047 with the surplus present in an allocation of their own. New `ReadsNoOctetPastTheFrame`, with helper `read_up_to_a_protected_page`.
- `tests/mutations.json`: five plants (`adp-control-length-mask-0x03ff`, `-0x01ff`, `-0x00ff`, `-0x007f`, `adp-long-control-length-reads-surplus`).
- `examples/rv32/smoke.c`: a fifth control, length 256; its failure codes are renumbered (60 to 79) so that they stay distinct.
- `docs/REQUIREMENTS.md`, `CHANGELOG.md`, `docs/VERIFICATION.md` (485 core plants, the RV32 row); `docs/TRACEABILITY.md` and `docs/TESTS.md` by their generators.

## Decisions to check
- **The uncommitted test edit.** Its exact 82-octet allocation is kept. Its prose comment is not: the comment gate admits only licence, requirement and clause lines under `tests/`.
- **Why a protected page as well.** The campaign counts only named assertion failures, and a sanitizer abort leaves no report, so an abort is an escape there. The child process turns the read into a named assertion in every build. In the sanitizer gate the accept test's own allocation reports the read.
- **Round 1 lost coverage.** Its accept test sampled three lengths where main swept the field; seven reviewer mutants survived because of it. The sweep restores that.
- **The plant count** in `VERIFICATION.md` (485) has no generator; it is edited by hand and equals the campaign's 489 less the four configuration plants.
- **ADP-01's origin** stays "Import baseline" in the generated table; the issue link is in the section and the change log, as the finding asked.

## Parent patch (for the pin bump)
- Applies to dev-soft-core `5de21ff3`, where it was run, and to dev `e275d795` (apply check only).
- A first version took `ctrl_mutants.py` past its 1,000-line module limit. The final form shares one constant for the guard (997 lines); C++ idiom, Python idiom and hygiene checks pass.

## For the manager
1. The public copies of the round-1 packet still hold host paths; this packet does not change them.
2. The local round-1 packet is left as it was, host paths included.
3. Still true from round 1: frames above 128 octets are dropped by the mailbox before the core; the all-fabric validator, not used by the split build, reads the field and refuses a discover whose surplus is missing; `970-first-advertise` conflicts in the change log and the generated tables.
4. The PR body needs replacing with `PR-BODY.md` when the head is pushed.

The source checkout, the consumer worktree (restored clean at its own pin) and the build outputs are local artifacts; published receipts are in `receipts/`. No build directory was removed. Two build directories left by another session were not touched. CPU: unbooked, 8 jobs at most. No bench.
