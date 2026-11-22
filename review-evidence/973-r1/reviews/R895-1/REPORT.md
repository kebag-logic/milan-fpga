[R895] NEGATIVE - exact head 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7

Internal cleared-context independent review, round R895-1, issue #973 / PR #978.
Head `9a71daa9aa2379e2a57eb93ccafe83101bcb37f7`, tree `0fe791d5c539f4100e312f17e469a2a9a50bc006`.
Reviewed range: `dd163e41..9a71daa9` (the flip PR #960's reviewed head to the published head), eight commits.

This is a source-review verdict at one exact head. It is not merge authorization, not a manager source bank, and not hardware evidence.

## Verdict in one paragraph

The core fix is correct for the defect #973 describes. SRP's poll takes a DOWN from the LINK register and an UP only while the last LINK the loop dispatched carried one (`link_carried`). My own runs reproduce the defect on the base firmware at four shapes and show the head passing. All twelve planted defects are killed at 1x1/1if, 8x8/1if and 1x1/2if: the author's seven, the moved `srp-poll-extra-read`, and four of my own. The image ROM growth (+16 / +24 / +8 / +16 B, RAMB36 unchanged) reproduces at base and head. The loop and the coverage ratchet are byte-identical to the base.

The verdict is NEGATIVE for two reasons:
- **F1 (BLOCKER):** the new plant table is not registered with the firmware boundary gate. The hosted `firmware-boundary` job fails deterministically at this exact head. The author's validation never ran the documented local gate that would have caught it.
- **F2 (MINOR):** the fix adds a liveness regression on SRP's re-attach path. An executable probe shows it, and it falsifies a statement in the adapter README. The shipping boot path cannot reach it.

## Reconstruction

Read in order:
- `AGENTS.md` and `CONTRIBUTING.md` (merge bar, lenses, comment rules).
- `docs/README.md`.
- Issue #973: its body, frozen acceptance, TAKEN and REVIEW READY. There were no maintainer scope comments beyond those.
- Related issues #970 and #972.
- The authorities: `docs/reference/MAILBOX_CONTRACT.md` (LINK register `0x014`, LINK event), `hdl/milan/mailbox/KL_mbx_evt.sv:28-45,108,155,342,387` (coalescing; a LINK record posts only when the level differs from `posted_up_r`), `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/loop/ctrl_loop.h`, and `docs/design/REBOOT_RESET.md` (REBOOT is an IPROG reload).
- The diff and per-commit history.
- The author's public packet at `62593bf0:review-evidence/973-r1/author-r1`.
- The hosted runs at the exact head.

Frozen acceptance (#973):
- (a) On the one-hart image, a link-up at any phase of a pass resets SRP's interface once, with the startup participants kept.
- (b) The host test of that ordering fails before the fix and passes after, at 1x1/1if and 8x8/1if, with a planted defect.
- (c) The CPU budget rows are unchanged within their bounds.
- (d) The images are within their ledgers.

The author reads (a) as two cases: a first UP resets nothing and keeps the startup participants (`on_event`, `hold`), and a later UP resets once. I accept that reading. It is what `on_event`'s first-UP rule (`srp_mbx.c:1227-1230`) already defines.

Independence note: I completed my pass over the diff before reading any PR comments. While listing the PR's comments to look for prior findings, I saw the heading and first lines of a concurrent external reviewer's comment. I stopped reading it there. My findings and ledger do not derive from it. The only earlier public rounds on this PR are the two review-start notices, so no prior finding needs resolving or retaining.

## Findings

### R895-1-F1 BLOCKER - lenses: Tests, Docs - `sw/firmware/ctrl/test/ctrl_configs.py:156` (`OUTSIDE`) with `sw/firmware/ctrl/test/srp_link_mutants.py:8` - the new plant table is not classified by the firmware boundary gate; hosted `firmware-boundary` fails at this head

- **Requirement/evidence:**
  - `ctrl_configs.held()` refuses any file that names the firmware's tree and compiles nothing, unless it is a known builder or is listed in `PART_OF`, `OUTSIDE` or `SUITES` (`ctrl_configs.py:441-466`). `srp_link_mutants.py` names `sw/firmware/ctrl` in its docstring (line 8) and is in none of those lists.
  - Its sibling tables are in `OUTSIDE` with a reason: `srp_talker_mutants.py`, `srp_listener_mutants.py` and `srp_reclaim_mutants.py` (`ctrl_configs.py:173-179`).
  - Hosted rtl-fast run 45061747278, job `firmware-boundary`, on head `9a71daa9`, failed at 19:58:17Z with: `REFUSED: sw/firmware/ctrl/test/srp_link_mutants.py names the firmware's tree, compiled nothing in the capture, and is neither a known builder (ctrl_configs.BUILDERS), one whose compiles are none of the firmware's (OUTSIDE), nor one that compiles only in a suite (SUITES)`, exit 2 (`receipts/hosted/firmware-boundary-failed-step.txt`).
  - The fail-fast then cancelled the rest of rtl-fast (`firmware-srp-mutants`, `firmware-control-mutants`, `publication-census`, `yosys-elaboration`). It also cancelled all nineteen rtl-full Verilator shards, which is why `verilator-suites` and `yosys-portability` fail (`receipts/hosted/runs-at-head.txt`).
  - My static census (`scripts/boundary_census.py`, `receipts/boundary-census-head.txt`) lists `srp_link_mutants.py` among the text-found builders that no list classifies. It is the only one of them that compiles nothing.
  - The documented local firmware gate set includes `ctrl_boundary.py --require-rv32 --selftest` (`docs/testing/CI_WORKFLOWS.md:3629`). It appears in neither the TAKEN validation plan nor the REVIEW READY evidence. The PR's Status still says "GREEN".
- **Impact:** the head cannot get a successful `rtl-fast` verdict, which is a completion bullet in AGENTS section 7. The fail-fast leaves this head without SRP-mutant and rtl-full hosted evidence. The published readiness claim is wrong about the head.
- **Required change:** `ctrl_boundary.py --require-rv32 --selftest` passes at the new head, with the new table classified as its siblings are. The local receipt for that gate is published. The PR's Status and evidence state the gate.
- **Verification:** `boundary_census.py` no longer lists `srp_link_mutants.py`. A local `ctrl_boundary.py --require-rv32 --selftest` exits 0. Hosted `firmware-boundary` succeeds at the new head, and the cancelled jobs then execute.

### R895-1-F2 MINOR - lenses: Conformance, RTL, Robustness, Tests, Docs - `sw/firmware/ctrl/srp/srp_mbx.c:1474` with `:1286`; `sw/firmware/ctrl/srp/README.md:111-113` - after a re-attach that reads a DOWN whose record the fabric then elides, SRP never follows the link that is up

- **Requirement/evidence:**
  - At head, `srp_mbx_attach` sets `link_carried` to the register level it reads (line 1474). The poll takes an UP only while `link_carried` is set (line 1286).
  - The fabric posts a LINK record only when the level differs from the last level it posted (`KL_mbx_evt.sv:155,387`; `mbx_model.c:169`). So a DOWN that is held by a full ring and then recovers before posting yields no record. The README states this case itself: "A held DOWN record can disappear when the level recovers" (line 113).
  - Sequence: SRP is destroyed and re-initialized after its loop has consumed the UP record. While the link is momentarily down with its DOWN record held, attach reads DOWN, so `link_carried` is false. The level recovers, and no record is owed. From then on, no LINK ever sets `link_carried`, so SRP holds the interface down on an up link indefinitely, until the next real link change.
  - At base, the poll took the register's UP and recovered. README line 112 states that contract: "Polling reconciles that level even without another LINK record". At head that statement is false in this case.
  - Executable evidence: `scripts/probe_reattach_elided.cpp` is a disposable suite on the repository's own fixture, modelled on `Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` (`srp_mbx.cpp:1062`) and `Srp.ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord` (`:1035`).
    - At head, `Srp.ProbeReattachWhileItsDownRecordIsElided` FAILS at 1x1/1if and 8x8/1if: "PROBE: SRP does not follow a link that is up" (`receipts/probe-reattach-head.log`).
    - On the base firmware, the same suite PASSES at both shapes (`receipts/probe-reattach-basefw.log`).
    - The control case, a re-attach with the link down followed by an owed UP, passes on both.
  - Not covered elsewhere: none of the seven plants or the tests exercises a re-attach that reads DOWN. The PR's limitations list the dropped-UP-on-re-entry case but not this one.
- **Reachability:** not on the shipping image's boot path. `ctrl_plat.c:405` attaches SRP once after a full fabric reset (REBOOT is an IPROG reload, `docs/design/REBOOT_RESET.md:27-34`). The fabric posts the first UP after reset, and that record is still in the ring when SRP attaches, so it sets `link_carried`. The exposure is the documented re-attach API (`README.md:110-111`; exercised by the tests) and any future runtime re-attach. That is why this is MINOR, not MAJOR.
- **Lenses:**
  - Conformance: in that path, an operational port carries no MRP declarations (IEEE 802.1Q-2018 10.7, the behaviour #973 cites).
  - RTL: the adapter's documented attach and poll contract no longer holds.
  - Robustness: re-attach during a link transition, an ordering and reset path.
  - Tests: no test or plant covers it.
  - Docs: README line 112 is false, and the PR omits the limitation.
- **Required change:** one of the following, without reintroducing #973's double reset (my plant `rv-poll-resets-on-register-up` and the author's `link-pass-attach-carries-an-up` must stay killed):
  - SRP follows an up link after a re-attach that read DOWN when no LINK record is owed; or
  - the limitation is stated exactly in the adapter README (line 112 corrected), pinned by a test, and filed as a follow-up Issue, as AGENTS section 4 requires for new work.
- **Verification:** the probe passes at the new head; or the README states the case and a committed test asserts the documented behaviour. In both cases the existing link-pass suite and the twelve plants stay green and killed.

### R895-1-F3 SUGGESTION - lens: Robustness - `sw/firmware/ctrl/srp/srp_mbx.c:1286` with `:1227-1229` - a DOWN inside a pass still resets twice

The poll resets on the register's DOWN, and the LINK DOWN record resets again. The second reset normally comes before any rebuild, which I confirmed by reading `reset_interface` (`reopen_polls = 1`). If the ring holds the DOWN record for more than one pass, the participants are rebuilt while the link is down and then destroyed again. Nothing is transmitted, because `i->link` is false. This is pre-existing and disclosed in the PR's limitations, and #973's acceptance is the link-up. Suggest a follow-up Issue if the wasted rebuild matters for the CPU budget.

### R895-1-F4 SUGGESTION - lenses: Robustness, Docs - `sw/firmware/ctrl/srp/srp_mbx.c:61-71` (`enter`) with `:1286` - an UP that the sink drops on re-entry is no longer recovered from the register

This path is counted and asserted in debug builds, so it is an invariant violation, not an expected path. The PR body discloses it. Suggest stating it in the adapter README beside the new rule, so the README is the complete statement of when SRP follows the register.

### R895-1-F5 RESIDUE - PR #978 body, "Linked Issue / roles" - the related-issue list omits issues the task names

The issue relates to #665, #970 and #972, and the PR's limitations name #872. The PR body's line reads `Relates to #665`. Exact fix: `Relates to #665, #970, #972, #872`.

## What was checked against the focus list

1. **Cause on the one-hart split image (IEEE 802.1Q-2018 10.7, 35.2):** confirmed.
   - The loop dispatches the ring's records at a pass's start (`ctrl_loop.c` `service_events`; `ctrl_loop.h` pass order), and SRP's poll read the register later (`dd163e41:srp_mbx.c` poll, `links[n] = mbx_link_up(n)`).
   - `srp_link_pass.cpp` on the base firmware (head tests, base `srp_mbx.c/.h`) fails only `SrpLinkPass.AfterTheEventsBeforeSrpsPoll`, at 1x1/1if, 8x8/1if, 8x8/2if and 1x1/2if. The other three phases pass. The diagnostics: "SRP's poll took a level no LINK had carried"; resets 2, not 0; "a first UP keeps the startup participants" (`receipts/basefw-arms.log`).
   - At head, all four tests pass at the same four shapes (`receipts/head-arms.log`).
2. **The fix:**
   - `link_carried` is set only by SRP's own LINK sink (`srp_mbx.c:1233`) and by attach (`:1474`).
   - Invariant: `i->link` implies `i->link_carried`. The poll writes `link = reg && carried`, and the sink writes both.
   - The poll still makes one register read per interface (plant `srp-poll-extra-read` killed).
   - A DOWN still fails closed (`Srp.LinkLevelLossAndFirstDownEventAreFailClosed`). An UP whose DOWN record a held ring cancelled is still recovered from the register (`Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive`, guarded by my plant `rv-poll-clears-carried`).
   - Other consumers of the raw LINK level: ADP reads it once at start (`tsn-c-stack/src/adp.c:238`) and then follows events idempotently (`adp.c:252`). MAAP reads it at start and compares on each event (`maap_mbx.c:214,273`). No non-SRP code reads SRP's `link`. None of them is left inconsistent.
   - #972 interplay: a boot path that publishes link DOWN at the arm makes attach carry DOWN and the first UP arrive as a record, which is the path this fix protects.
   - #970: ADP is untouched.
   - The exception is F2's re-attach path.
3. **Plants:** at 1x1/1if, 8x8/1if and 1x1/2if, each is caught by its named test's own words, in my runs of the repository's campaign driver (`receipts/plants-*.log`, rc 0). The set is:
   - the author's seven: fix reverted, attach carries an UP (a double reset at the first UP), carried stays up (a stale carried level gives a double reset at a later UP), first UP resets, carried never recorded, attach carries nothing, the two-hart form;
   - the moved `srp-poll-extra-read`;
   - my four (`scripts/reviewer_plants.py`): OR instead of AND, the poll clears carried, a double reset in the sink, the poll resets on a register UP.
4. **ROM and ledgers:** `plat_ledger.py`, run by me at head and with base `srp_mbx.c/.h` (`receipts/plat-ledger-{head,base-fw}.log`):

   | Point | ROM base | ROM head | Delta | SRAM | RAMB36 |
   |---|---:|---:|---:|---|---:|
   | 1x1/1if | 126,432 B | 126,448 B | +16 B | unchanged | 45 |
   | 1x1/2if | 128,032 B | 128,056 B | +24 B | unchanged | 46 |
   | 8x8/1if | 139,208 B | 139,216 B | +8 B | unchanged | 58 |
   | 8x8/2if | 140,784 B | 140,800 B | +16 B | unchanged | 63 |

   Every point passes. The 8x8/1if image is 48 B below 139,264 B, as the PR states. The first form (`8b76887e`, loop-held level) is gone: `git diff dd163e41 HEAD -- sw/firmware/ctrl/loop sw/firmware/gtest` is empty, so the loop and the coverage ratchet are back to the base.
5. **Gates:**
   - Firmware gate shard 0/4, run by me at head: PASS, 77 of 77 suite verdicts, 90 `[ok]`, 0 escaped, both `srp-srp_link_pass-if1-*` arms among them (`receipts/fw-gate-shard0.log`).
   - `fw_coverage.py --check`: PASS, 40 files; `srp_mbx.c` 100 % lines and branches (`receipts/fw-coverage-check.log`).
   - CPU graders `flip_grade --check` at both points, `load_grade --check` and `shape_costs --check`: PASS and byte-identical to the author's base receipts (`receipts/grader-*.txt`).
   - The author's measured CPU legs tally to 88 and 86 paired probes, 0 verdict changes, largest |head-base| 0.438 ms against a 20 ms budget (`receipts/author-cpu-probe-tally.txt`).
   - Docs gates at head (`receipts/docs-gates-head.txt`): `docs_check`, `check_em_dash --base dd163e41`, `check_doc_style`, `check_py_idiom`, `check_cpp_idiom`, `check_hygiene`, `check_todo_ownership`, `check_doc_paths`, `gen_toc --check` and `--verify-anchors`, `measure_test_evidence`, `measure_naming`: all rc 0.
   - The hosted docs and elaborate workflows: every executed job succeeded.
   - The boundary gate fails: F1.
   - Comment rule: no lane label, lane name, round, reviewer ID or comment ID appears in any added line of the delta.

## Lens results (each with its evidence at this head)

- `Conformance` - UNCLEAN (F2).
  - Examined: #973 acceptance (a) to (d) against `srp_link_pass.cpp` at base and head, four shapes.
  - Examined: `srp_mbx.c:1216-1235,1276-1295,1463-1476` against IEEE 802.1Q-2018 10.7 port-state handling as the issue cites it.
  - Examined: `KL_mbx_evt.sv` posting rule.
  - Acceptance (a) to (d) are met on the shipping path. F2 is the re-attach path.
- `RTL` - UNCLEAN (F2).
  - Examined: the adapter's state (`srp_mbx.h:66-68`), the invariant `link` implies `link_carried`, `turn_builds` (`srp_mbx.c:1243`) consuming the combined level, and the attach and poll contract in `README.md:110-118`.
  - Examined: struct growth and offsets (author image diff, SRAM unchanged).
  - No RTL or mailbox contract file is in the diff.
- `Robustness` - UNCLEAN (F2).
  - Examined: DOWN with a held record, an elided DOWN, a flap within a pass, re-entry drop, re-attach at UP and at DOWN (probe), ring coalescing that never drops a last state, and a DOWN double reset (F3).
- `Tests` - UNCLEAN (F1, F2).
  - Examined: `srp_link_pass.cpp:1-137` (it can fail; it fails on the base firmware), `srp_fixture.hpp:54-86` (`SetUp` is unchanged for existing suites), `srp_link_mutants.py`, `srp_arms.py:117-124`, `test_ctrl_firmware.py:212,234-240`.
  - Examined: the twelve plants at three shapes, shard 0, coverage, and the boundary gate (hosted).
- `Docs` - UNCLEAN (F1, F2).
  - Examined: `sw/firmware/ctrl/srp/README.md:110-118`, `CHANGELOG.md:11,62-67`, the source comments at `srp_mbx.c:1279-1283` and `srp_mbx.h:66-68`, the PR body, REVIEW READY, and the docs gates.
  - F5 is RESIDUE.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #973 acceptance; `srp_mbx.c` sink, poll and attach; `srp_link_pass.cpp` at base and head (4 shapes); `KL_mbx_evt.sv` posting rule; re-attach probe | R895-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| RTL | UNCLEAN (F2) | `srp_mbx.h:66-68`; `srp_mbx.c:1227-1233,1243-1248,1283-1295,1472-1474`; `README.md:110-118`; image diffs (ledger at base and head) | R895-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| Robustness | UNCLEAN (F2) | the held, elided, flap, re-entry and re-attach paths; `probe_reattach_elided.cpp` head vs base; ADP and MAAP level consumers | R895-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| Tests | UNCLEAN (F1, F2) | `srp_link_pass.cpp`; `srp_fixture.hpp`; `srp_link_mutants.py`; 12 plants x 3 shapes; firmware shard 0; `fw_coverage --check`; hosted `firmware-boundary`; `boundary_census.py` | R895-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| Docs | UNCLEAN (F1, F2) | `srp/README.md:110-118`; `CHANGELOG.md`; added source comments; PR body; REVIEW READY; 13 docs gates | R895-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |

## Real limits

- I did not run firmware gate shards 1/4 to 3/4. I ran only the #973 plants plus `srp-poll-extra-read` and my own four, through the same campaign driver, at the three SRP campaign shapes. The full shard results are the author's receipts.
- I did not re-run the twin and its plants, the split boot simulation, the CPU budget harness legs, or the builder legs. I tallied the author's receipts for the CPU legs only.
- I did not run `ctrl_boundary.py` locally. F1 rests on the exact-head hosted log plus a static census of the same classification rule.
- The base for the "fails before the fix" runs and the base ledger is head tests and tree with the base `srp_mbx.c` and `srp_mbx.h`. Those are the only firmware sources the delta changes.
- My `fw_gtest` build reported pkg-config gtest as "absent", but the suites linked and ran against the host's GoogleTest. The firmware gate pins its own toolchain identity on the hosted runners.
- No hardware, no physical calibration, no bench. Field skips are not hardware proof.
- An observation outside this delta: the firmware gate's shard self-test writes `dispatch-build/` relative to the working directory (`test_ctrl_firmware_shards.py:42`). My shard run left it in the clone, and I removed it.
- Clone state after the probes: worktree, index, blob bytes and modes equal HEAD, and the required gitlinks match (`receipts/clone-integrity.txt`). `external` was uninitialized from the start.

## Pending manager duties

- Hosted rtl-fast and rtl-full on a corrected head. At this head `firmware-boundary` fails, and the fail-fast cancelled the SRP and control mutant jobs and every rtl-full Verilator shard.
- The act replica.
- The current-dev merge candidate (builder and native banks; live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`).
- The bench re-run after merge.
- Carry F5 to the residue checklist.
- Re-review of F1 and F2 at the new head, with every lens re-covered at a head that includes the fix.

R895-1 FINISHED
