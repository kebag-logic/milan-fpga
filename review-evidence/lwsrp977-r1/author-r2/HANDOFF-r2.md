# HANDOFF r2: [A861] kebag-logic/lwSRP PR #22 (for kebag-logic/milan-fpga#977, part of #665), round 2

Status: **REVIEW READY** (07:20 CET 2026-11-27) at `opt-exec-3` `50a2106483141fcd7d1b20654bcf0803e7c3020a`, local
only. Every finding of R959-1 and R960-1 is closed; every lwSRP gate passes on clean clones. Nothing pushed or posted.
ETA: none owed by this lane; the next step is the manager's (push, PR body, merge method, re-review).

Inputs: internal review R959-1 (issuecomment-7210816023, NEGATIVE), external review R960-1 (issuecomment-7210817308,
NEGATIVE); CONTRIBUTING.md, doc/integrator.md, doc/tester.md.

## Result

- 10 commits on `73007b48` (`7b5e821`..`50a2106`), one-line subjects, no bodies or trailers; no rebase, no rewrite,
  no force. REVIEW-READY.md maps each finding to its commit and receipt; PR-BODY.md is the updated PR #22 body.
- With every option OFF: the only non-comment source change is `7ca4a6f` (the default restore spells its length
  `sizeof(previous_value)` with no local, as `main` does): 64 of 64 objects now byte-identical to `main`'s (61 of 64
  before), and the differential's default builds are trace-identical in both profiles.
- Tests added: an end-station unit suite (every build; option-aware), the recovery test at 1 and 2 ports, four
  end-station reversals (`--end-station ON`), two differential plants and a sparse-type test application. Each new
  plant fails named assertions (receipts/named-failures.txt) or a named trace seed (receipts/probes/).

## Decisions to check

- Issue IDs: the brief named #977 and #665; the internal reviewer also asked #872 for the bucket and wheel blocks.
  opt-exec-1 (key, buckets, wheel, merge) came from #872's work (opt-a808), so those four blocks cite "#872 and #977,
  part of #665"; the five end-station blocks cite "#977, part of #665".
- Default objects: made true rather than qualified (the reviewers allowed either). The PR body still states that
  with `-g` only the debug sections differ (verified, 24 of 24).
- The end-station unit build passes the five switches through `CMAKE_C_FLAGS`; no new CMake option was added.
- PR-BODY.md keeps the reviews' finding IDs in its "Changes since `73007b48`" table (not in commits or comments).

## Log
- 06:48 started at opt-exec-3 73007b48 (clean). Scratch: $VALIDATION_STORAGE/lwsrp22-a861-scratch. cgreen prefix read
  (not written) from $VALIDATION_STORAGE/977-a825/cgreen/prefix.
- 06:48 rm logged then run: `git rm` of tests/__pycache__/check_reversals.cpython-314.pyc (commit 7b5e821).
- 06:49 reproduced the -O0 object difference (61/64 at 73007b48: mrp_mad.c at -O0, -O0 Milan, -O0 -fPIC); fixed
  (7ca4a6f): 64/64.
- 06:50 rm (LOGGED LATE, after it ran): a stray `rm -rf /dev/null` in a command chain, a no-op (not root; /dev/null
  intact, nothing removed). Logged in disk-cleanup.log with that note. Every other rm was logged before it ran.
- 06:52-07:00 end-station suite, reversal runner, differential driver, contracts, option comments, changelog, guides
  (91f7c39..a8693e0); anchors re-pointed (50a2106). `git fetch` of origin opt-exec-1/opt-exec-2 (read only) to
  attribute the options to their issues.
- 06:53, 07:02, 07:06 planned removals logged before each differential/equivalence run (the tools' own rmtree of
  their scratch subtrees, literal paths).
- 07:04 two gate-harness faults (mine): the inventory regex missed `file`'s padded column, and the link checker needs
  an HTTPS origin in the clone. Fixed; reran clean (inventory-r2, docs-r2). The 06:49 first binary scan had the same
  regex fault; the r2 inventory is the valid one (74 files: 52 ASCII, 22 UTF-8).
- 07:04 I edited the gate script while six gates ran, which broke their final lines (rc 2) after their tools had
  passed. Reran all six from a frozen copy (gate-r2.sh): all rc 0. Superseded logs kept in receipts/superseded/.
- 07:19 rm logged then run: the ignored bytecode my probe's import left in the checkout
  (tests/__pycache__/check_differential.cpython-314.pyc) and its empty directory. Checkout clean.

## Not done

- No push, no post, no PR body edit, no hardware, no target (RV32) build: no target C library on this host.
- The bytecode blob remains in branch history (`cce36b5`): squash or rebuild at merge, the manager's choice.
