STATUS (07:35 CET 2026-11-23): READY FOR INDEPENDENT RE-REVIEW at `87b2fc0f2867ef132b9388e22ec262fc626cbb57`.
All requested round-3 local gates pass at this head. Four round-3 commits are local on `pf-973-1`; the worktree is
clean. No push or PR edit was made. Hosted checks, including `firmware-boundary` for R895-1-F1, and independent
re-review are pending on this head.
ETA: local work complete; the manager may push and request re-review now.

# HANDOFF r3 — #973 ([A822]) — PR #978, round 3 (R896-2 NEGATIVE: F1 BLOCKER; R895-1-F1 hosted proof retained)

Round base: `5759780f2251ef25221c6a395250312dce656ca4` (pushed as `973-srp-link-carried`). Round 3 commits, local:
- `d9f8929d` the tests first: an UP elided behind a full ring and a DOWN, then a fresh UP, first and later. Both
  fail at `5759780f`;
- `0338f66a` the fix: a DOWN the poll reads clears the mark; three more plants;
- `9509dbd3` the corrected plant text (my first form did not compile; see section 1);
- `87b2fc0f` docs (SRP README, changelog).

## 1. R896-2-F1 BLOCKER (stale uncarried-UP mark) and what was done
Review: R896-2 NEGATIVE at `5759780f`. Its packet holds `REPORT.md`, `probe_stale_mark.cpp` and the run scripts.

**The defect.** The poll short-circuited `carried_up` on a register DOWN, so a DOWN left bit 1 (the mark) set. The
sequence:
1. An UP rises while the ring is full and is marked.
2. A DOWN comes before any take makes room, so the fabric drops the UP record (`posted_up_r` is still DOWN).
3. The ring drains while the link is down.
4. A fresh UP rises after a later pass's take. That take emptied the ring, but it ran before the fresh UP. The
   poll still took the fresh UP on the old mark, and its LINK then reset the interface a second time.

**Fix** (`sw/firmware/ctrl/srp/srp_mbx.c:1286-1294`, `carried_up`; `:1309`, the poll; `srp_mbx.h:65-67`).
- `carried_up` now takes the level the register read (`up`) and always runs. While bit 0 is clear, the new value is
  masked by `-(unsigned)up`, so a poll that reads a DOWN writes 0 and clears the mark. On an UP the value is the
  same as before. While bit 0 is set nothing changes, as before. It returns `c & up`, so a DOWN still fails closed.
- So the mark holds only while every poll since it was set has read the link up. A DOWN between them can elide the
  marked UP's record. The UP after that DOWN is owed a LINK of its own, posted after the takes the mark relied on.
  That UP is now taken from its own LINK: the first keeps the startup participants, and a later one resets once.
- What stays the same:
  - re-attach / elided-DOWN recovery: the mark is set and taken with no DOWN read in between;
  - the immediate fail-closed DOWN: `c & up` is 0 whenever `up` is 0;
  - ordinary carried-UP handling: bit 0 set skips the update;
  - the first-UP and later-UP reset rules: `on_event` is unchanged.
- Size: the variants I tried cost 0 to 16 B. The chosen form is **byte-identical** in `.text` at 1x1/1if and
  8x8/1if (8x8/1if: `poll` 812 B, `srp_mbx.c` 11,544 B, as at `5759780f`) and +4 B at 2if. GCC emits one `mul` for
  the mask; the core has the M extension. Evidence: `receipts/checks/size-variants.txt`.
- **A stated assumption, public in the code comment, the README and the PR.** A DOWN that no poll reads lies between
  two of SRP's polls. A level register cannot show it, and a register-only rule cannot close it. A DOWN followed by
  an UP within one poll gap is not a real link transition: a dropped autonegotiated link waits at least
  `break_link_timer`, 1,200 to 1,500 ms (IEEE 802.3-2022 28.3.2), before it renegotiates. The gap between two SRP
  polls is milliseconds.
- Comment argument and README corrected: `srp_mbx.c:1273-1284`; `README.md:120-123` (the reviewer's `README:117`
  line is kept, and the new lines state when the observation is valid); `CHANGELOG.md:69`.

**Tests, committed first (`d9f8929d`).** In `srp_link_pass.cpp`, `SrpLinkPassElided` (its own process; 1x1/1if and
8x8/1if through the existing `link_pass_arms`):
- `AnElidedUpAuthorizesNoFreshFirstUp` (`:218`; fixture `:171-215`): the reviewer's sequence, with set-up asserts that the UP record was
  elided and the ring drained. It checks that the fresh UP is not taken before its LINK, resets nothing and keeps the
  startup participants;
- `AnElidedUpAuthorizesNoFreshLaterUp` (`:230`): the same after a carried UP and its DOWN. The fresh UP must reset
  once (it reset twice);
- both FAIL at `5759780f` at both shapes. Both PASS with only `9a71daa9`'s `srp_mbx.c/.h` substituted: the
  re-attach test fails there, as known. Both PASS at the head. Receipts: `receipts/repro/`;
- the reviewer's unmodified `probe_stale_mark.cpp` and `run_focused.py` pass at the head at both shapes (10/10
  tests). Their `run_controls.py` passes too: its prior-production control and the re-attach probe. Receipts and
  input hashes, which match the published packet: `receipts/reviewer-probe/`.

**Plants** (`srp_link_mutants.py`; campaign at 1x1/1if, 8x8/1if, 1x1/2if, `receipts/plants/`):
- new: `link-pass-mark-survives-a-down` (the fix reverted, first UP), `link-pass-mark-survives-a-down-later` (the
  same, later UP: a double reset) and `link-pass-mark-masked-before-the-shift` (the mask on the wrong operand: a
  DOWN sets the mark). All three are killed at all three shapes;
- existing plants on the changed lines now plant at the new sites: `poll-or-instead-of-and` on the return
  (`(c | up) & 1u`), and `unowed-up-never-taken`, `-taken-unmarked`, `-ignores-the-take` on the masked line.
  `srp_mutants.py`'s `srp-poll-extra-read` follows the poll line;
- `rv-poll-resets-on-register-up`, `rv-sink-double-reset`, `link-pass-attach-carries-an-up` and every other link plant
  stay killed. `rv-poll-or-instead-of-and`'s site (the round-1 line) is gone, as in round 2. `rv-poll-clears-carried`
  still escapes, as disclosed in round 2;
- my first form of the two `mark-survives` plants did not compile (`-Werror=parentheses`), so it reported ESCAPED.
  That raw result is kept in `receipts/plants/r3-plants.txt`. `9509dbd3` parenthesizes them, and
  `r3-plants-mark.txt` shows them killed. A compile failure is not counted as a kill.

**R895-1-F1 (retained, hosted).** The source fix is unchanged since round 2 (`ctrl_configs.py:180`). The local
boundary gate is re-run at this head (section 2). The hosted `firmware-boundary` job at the pushed head is the
manager's step, and the PR body says so.

## 2. Gate table
All at `87b2fc0f2867ef132b9388e22ec262fc626cbb57`, each in its own clean clone and unit. No CPU range was free, so the
units ran on the shared session pool. Base CPU and image figures are retained from round 1 at `dd163e41`, and
round-2 figures from `5759780f`.

| Gate | Result | Receipt |
|---|---|---|
| Test-first regression, both shapes | the 2 new tests FAIL at `5759780f`, PASS with `9a71daa9`'s SRP, PASS at head (9/9 at each shape) | `receipts/repro/` |
| Reviewer's probe and controls, unmodified | `run_focused.py` 10/10 at both shapes; `run_controls.py` 4/4 | `receipts/reviewer-probe/` |
| Link plant campaign, 3 shapes | 14 link plants + `srp-poll-extra-read` + 2 reviewer plants killed at 1x1/1if, 8x8/1if, 1x1/2if; `rv-poll-clears-carried` escapes (disclosed in round 2); `rv-poll-or-instead-of-and` site gone | `receipts/plants/r3-plants*.txt` |
| Firmware shard 0: suites | PASS, 77 suite verdicts, 90 arms | `receipts/gates/firmware-shard-0.txt` |
| Firmware shard 1: control plants | PASS, 826 caught, 0 escaped | `receipts/gates/firmware-shard-1.txt` |
| Firmware shard 2: AECP plants | PASS, 385 `[ok]`, 0 escaped | `receipts/gates/firmware-shard-2.txt` |
| Firmware shard 3: SRP plants | PASS, 585 `[ok]` (576 + 3 new x 3 shapes), 0 escaped; all 14 link plants killed at 3 shapes | `receipts/gates/firmware-shard-3.txt`, `receipts/plants/srp-*` |
| Firmware boundary, RV32 and self-test | PASS; 4,455 compiled sources, 0 findings, 117 boundary, 185 pin and 4 figure controls, 0 misbehaved | `receipts/gates/r3-bnd.txt` |
| Firmware coverage self-test and check | PASS, 40 files | `receipts/gates/r3-cov.txt` |
| Twin, twin plants, map twin, map plants | PASS, all four rc 0 | `receipts/gates/r3-twin.txt` |
| CPU harness, ten groups each point | PASS: 1x1 88 probes, 8x8/1if 86; 0 refusals, 0 budget misses, 0 share misses; no verdict changed against base or round 2; largest base/head difference 0.204 ms (1x1), 0.146 ms (8x8/1if) against 20 ms | `receipts/cpu/` |
| CPU table graders (flip 1x1/1if, 8x8/1if; load; shape costs) | PASS, rc 0, byte-identical to round 2 and base: loads 0.511 / 0.744 against 0.70 / 0.75; 1x1 last notice 127.31 ms, ACMP 29.06 ms, txL 47.88 ms | `receipts/cpu/graders/` |
| Platform images, plat_ledger | PASS, 0 findings: ROM 126,488 / 128,112 / 139,256 / 140,856 B; 45 / 46 / 58 / 63 RAMB36. 1x1/1if and 8x8/1if identical to round 2 in every size field | `receipts/images/` |
| Split boot, both shapes, self-test | PASS; 6 native controls as required, 8 plants caught | `receipts/gates/r3-boot.txt` |
| Docs workflow steps | PASS, 104 / 104, tree unchanged after | `receipts/gates/docs-steps.txt` |
| Builder legs 0 / 1 | PASS, each with the same one declared NOT RUN arm as round 2 (gate 1b MAKEFLAGS plant; gate 11 physical calibration) | `receipts/gates/builder-leg-*.json` |

The builder legs first refused twice with "source dependency origin differs: third_party/tsn-c-stack". My clone
script had pointed the clone's dependency origins at local paths. The legs then passed after the dependency origin was set to its
canonical URL (no network). The refusals are kept in `receipts/gates/builder-refused/`.

### Changed checks and killing words

| Check / source | Planted defect | Required failing words |
|---|---|---|
| `srp_link_pass.cpp:218`, elided UP then a fresh first UP | `link-pass-mark-survives-a-down` (fix reverted) | `SRP's poll took a fresh UP on an elided UP's observation` |
| `srp_link_pass.cpp:230`, elided UP then a fresh later UP | `link-pass-mark-survives-a-down-later` | `a later UP resets the interface once` |
| `srp_link_pass.cpp:218` | `link-pass-mark-masked-before-the-shift` (a DOWN sets the mark) | `SRP's poll took a fresh UP on an elided UP's observation` |
| fail-closed DOWN (`srp_mbx.cpp`) | `link-pass-poll-or-instead-of-and`, replanted on `return c & up` | `adapter.ifs[0].active[0]` |

The other link plants keep their round-2 tests and words. Raw killing logs: `receipts/plants/`.

Not done here (manager or other parties):
- push;
- the hosted runs at this head, including the `firmware-boundary` job for R895-1-F1;
- the local `act` replica;
- independent re-review;
- merge-candidate validation;
- fit and timing gating;
- the bench re-runs.

No merge or LAB approval is claimed.

Publication receipt: `receipts/review-ready-post.json`.

REVIEW READY 87b2fc0f2867ef132b9388e22ec262fc626cbb57
