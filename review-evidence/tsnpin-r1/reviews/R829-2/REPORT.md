[R829] NEGATIVE - exact head bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb

# R829-2: internal cleared-context delta review of PR #892 (issue #665), tsn-c-stack pin 70936b77 -> 715589c

Delta reviewed: `50e2a722..bfe7a9d6` (six commits). The previous verdicts were R829-1 and R830-1, both NEGATIVE at `50e2a722`. Tree `32d7e5283d01e6ea541527d31974db62ee7c64b8`. Source base `1d6bf555`.

Authority:
- #665 issuecomment-6806698193 (round-2 ruling on R829-1 and R830-1);
- issuecomment-6807277620 (41.0 RAMB36 accepted at the size fixture's 1x1/2if point; `ACMP_MBX_PASS_MAX` 1,030 -> 2,754);
- issuecomment-6811790762 (the 8x8/2if load is recorded here, not graded; the 0.75 ceiling and the nested-receive rule belong to #890);
- tsn-c-stack `docs/PORTING.md` "ACMP owed bound" (ACMP-12) at `715589c`.

The verdict is NEGATIVE on two MINOR findings.
- **F1 (Tests, Robustness):** the redelivery's stop-on-decline clause has no test. Remove it and a kept command is silently lost, yet every ACMP arm stays green. A disposable test shows the loss.
- **F2 (Docs):** round 1's F2 still holds at one gate. Builder leg 0 is labelled and summarised as "the pinned RV32 SDK", but its gate 1b ran the non-pinned GCC 14.3.0 build.

Everything else in the delta holds against code and receipts. That includes the redelivery's RAMB36 effect, which I derived from my own pinned-SDK compile, the eleven SDK steps, S2 at both pins, the load figures, and the three items handed to S2b.

## Findings

### F1 MINOR [Tests, Robustness]: the redelivery's "until acmp_rx declines one" stop is untested; dropping it loses a kept command with every arm green

- **Where:** `sw/firmware/ctrl/acmp/acmp_mbx.c:166`:
  `for (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k) {`
  The condition `m->kept.len == 0u` stops the redelivery once a record is declined and kept. The stated contract is `acmp_mbx.h:38-41` ("each until acmp_rx declines one, which it keeps"), and the donor rule is tsn-c-stack `docs/PORTING.md:88` ("until `acmp_rx` declines one or none is left").
- **Authority:**
  - AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect, and boundary behaviour is covered. Robustness: backpressure, invalid ordering.
  - The round-2 ruling (issuecomment-6806698193) required R830-1 F1 to "meet the redelivery rule, with a test that fails without it".
  - IEEE 1722.1-2021 8.2.4 and 8.2.5: every command received is answered.
- **Evidence (reviewer probes, receipts listed in MANIFEST.sha256):**
  1. Plant `rv-continue-after-decline` drops `&& m->kept.len == 0u` from line 166.
     - It escapes the `acmp` arm with 0 checks failed (`receipts/redelivery_probe.log`).
     - It also escapes the `acmpif2`, `acmpwalk`, `acmpnvm`, `plat` and `model` arms, each with 0 checks failed (`receipts/redelivery_probe_arms.log`).
     - The six new author plants are caught in the same run (they match the head's campaign line `mutants: 585 of 585 caught`), and so are five more of my own: kept record not first, a single ring record, redelivery only when drained, a declined redelivered record not kept, and the header bound one short.
  2. I wrote a disposable test, `ZProbeThreeCommandsBehindTheFullOwedSetEachAnsweredOnce` (`scripts/redelivery_loss_probe.py`). It fills the owed set, offers GET_RX_STATE 0x7801, 0x7802 and 0x7803, then releases the egress.
     - At the head's code it passes (`receipts/loss_probe_arm_at_head_code.log`, 165 tests, 0 failures). So the code meets the rule.
     - With the plant it fails: `got { 30721, 30723 }`, `want { 30721, 30722, 30723 }` (`receipts/loss_probe_arm_with_defect.log:338-347`).
     - The failure mechanism: the first kept command is accepted on redelivery, 0x7802 is declined and kept, and the loop goes on, so 0x7803's decline overwrites `kept.frame`. 0x7802 is never answered.
  3. Why the shipped tests miss it: K1 (`test_acmp_mbx.cpp:1184`) has only two commands, so after the second is declined the ring is empty. K4 to K7 (`:1344-:1420`) never decline a redelivered record with another record waiting behind it. `coverage.ratchet` reports 42/42 branches, so the condition is executed but its outcome is never checked.
- **Impact:** a regression of this one condition brings back exactly what the pin move removes. A command taken and never answered, with no gate noticing, means the controller's 200 ms timeout fires (Milan v1.2 Table 5.26), and a BIND_RX also loses its binding. The code at this head is correct. The defect is that this clause of the redelivery rule is unpinned.
- **Required outcome:**
  - A test in which a redelivered record is declined while at least one more acmp record waits behind it. It must assert that each command is answered once, in arrival order.
  - A planted defect at line 166's `m->kept.len == 0u` stop, named by that test in the control campaign.
- **Verification:**
  - Apply the plant above (the `rv-continue-after-decline` entry of `scripts/redelivery_probe.py`). The new test must fail by name.
  - The control campaign count must rise by one caught plant (585 -> 586) on a clean clone of the new head.

### F2 MINOR [Docs]: builder leg 0 is stated as run on the pinned RV32 SDK, but its compiler is the other GCC 14.3.0 build (residual of R829-1 F2)

- **Where:**
  - The receipt `review-evidence/tsnpin-r1/author-r2/receipts/round2/builder-legs-bfe7a9d6/builder_leg0.log:1` reads "builder leg 0, LiteX interpreter, the pinned RV32 SDK". Its line 4 reads `[gate 1b] compiler argv[0]=<rv32-sdk>/host/bin/riscv32-linux-gcc version=riscv32-linux-gcc.br_real (Buildroot 2026.05) 14.3.0`. The same holds at `8ffcf2fc` (`builder-legs-8ffcf2fc/builder_leg0.log`, `builder_leg0_make44.log`).
  - The PR body states: "Every RV32 build in this PR's figures and gates used the pinned SDK" (line 59). It also says "On clean clones of the head, with the pinned RV32 SDK ... every gate exits 0" (line 136), with the `test_builder.py --require-rv32` row (line 145).
  - HANDOFF.md:55 heads the gate table "Gates (clean clones; the pinned RV32 SDK ...)".
- **Evidence:**
  - The pinned SDK identifies as `Buildroot 2021.11-18033-g83947c7bb6` 14.3.0. My offline install from the digest-matched archive `d42680e9...` reports that (`receipts/sdk_install.log`, `receipts/sdk_verify_only.log`), and so do the author's 29 round-2 receipts under `<pinned-rv32-sdk>`.
  - Builder gate 1b picks `Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"` (`sw/builder/test_builder.py:4773`). The legs therefore ran under a HOME whose SDK is the build round 1 found the verifier refuses ("missing regular SDK provenance receipt"; R829-1 F2).
  - The eleven gate jobs and every ledger, S2 and size figure do use the pinned SDK (see check 3). Only this leg does not.
- **Impact:** the statement a cold reviewer relies on to accept the builder leg as pinned-toolchain evidence is false for that leg's RV32 gate. The risk to the result is low: gate 1b is a source and compiled-output contract on the same GCC release, and leg 1 compiles no RV32 code. But this is the defect class round 1 raised, and the ruling's fix ("correct the replica's statement of which compiler built it") is not complete. It is a claim about verification evidence, not only wording, so it is MINOR.
- **Required outcome:** do one of the following, and say which in the PR:
  - rerun builder leg 0 with HOME at the pinned SDK's parent, so gate 1b prints the `Buildroot 2021.11-18033-g83947c7bb6` compiler, and record the receipt; or
  - state in the PR body, the HANDOFF and the receipt header that leg 0's gate 1b ran the non-pinned build, named, and narrow line 59's "every RV32 build" claim to match.
- **Verification:**
  - A leg-0 receipt at the new head whose gate 1b line names the pinned build, or PR text that names the build actually used.
  - `ci_rv32_sdk.py --verify-only --destination <the SDK gate 1b used>` rc 0 if the pinned one is claimed.

### RESIDUE (wording only; carried to the residue checklist)

- **RES1 (R829-1 RES2, retained):** PR body, commit-table row "Ledger the platform's struct at its new size and state each point's plan" (line 47). "`struct ctrl_plat` grows 144 to 152 B at every point" still reads as a size change from 144 B to 152 B. Exact fix: "`struct ctrl_plat` grows by 152 B with one interface and by 144 B with two, at both shapes (round 1); the redelivery adds 8 B at the two-interface points".
- **RES2 (R829-1 RES3, retained):** `docs/design/MAILBOX_SPLIT.md:582-583`. "A command that arrives with all eight owed is declined, not dropped" still leaves out the BIND_RX case (tsn-c-stack `PORTING.md:81-82`; `acmp_mbx.h:47-48` states it). Exact fix: "A command that arrives with all eight owed, or a BIND_RX that arrives with fewer than two owed slots free, is declined, not dropped: …".
- **RES3 (new):** `docs/design/SPLIT_CONTROL_MEMORY.md:309`. "the loop the redelivery serves" names the loop as the `sram` growth. The growth is the adapter's new pointer to it (`acmp_mbx.h:227`, `struct acmp_mbx.loop`; +0 B at one interface and +8 B at two, measured below). Exact fix: "…, the adapter's pointer to the loop it attached to (the redelivery takes records in that loop's buffer), and the core's walk marks and owed-bound state."

### SUGGESTIONS (optional)

- **S1 [Tests] (R829-1 S2, retained, not re-examined):** add the `__lshrdi3` refusal to the portable `rv32` arm too; only `platrv32` refuses it.
- **S2 [Tests]:** my plant `rv-bad-continues` (go on after a refused record instead of returning) escapes every arm. It is equivalent: `mbx_rx_take` resynchronises the ring to `RX_HEAD` on BAD (`mbx.c:386-389`), so the next take is EMPTY unless the fabric posted again in between. No test is owed. If one is wanted, post a record after the refused one in K6 and assert it waits for the next pass. The header comment at `acmp_mbx.c:151-152` already states the behaviour.

- **S3 [Tests] (R830-1 S1, retained):** the guard moved to `acmp_mbx.c:158` (`if (m->kept.len != 0u)` in `redeliver`), and it is still held by no test. The prior round's plant `empty-kept-offered` (`if (true)`) escapes the `acmp` and `acmpif2` arms at this head, 0 checks failed (`scripts/empty_kept_probe.py`, `receipts/empty_kept_probe.log`). Its only effect is a zero-length record offered on each accepting poll and counted in the core's `rx_malformed`. Suggestion as before: K1 or K7 asserts `rx_malformed` unchanged across the drain.

## Prior findings at this head (resolved at their cause)

R829-1 (my round 1):

| Item | State at `bfe7a9d6` | Line / evidence |
|---|---|---|
| F1 MINOR Tests: the "still owes" return unpinned at one frame | **CLOSED** | `test_acmp_mbx.cpp:1124` E3 isolates the ACMP poll (others false) and checks that the loop does not sleep. Plant `acmp-poll-owes-nothing-at-one` (`acmp_owed_mutants.py:64`, `return m->acmp.owed_count > 1u;`, my P6's boundary) is caught by name in my rerun (`receipts/redelivery_probe.log`, 2 checks failed) and in the head campaign (585/585). |
| F2 MINOR Docs: replica's SDK statement | **PARTLY CLOSED -> retained as F2 above** | The eleven "Install and verify the pinned RV32 SDK" steps ran: `gates-bfe7a9d6/verify.md` rows 32, 67, 78, 149, 158, 165, 172, 179, 189, 214 and 228. Each is rc 0 with "SDK cache hit: verified", archive `d42680e9…`, gcc 14.3.0, and the logs are stamped with the head. They match the workflows' 11 step definitions (docs 3, rtl-fast 6, elaborate 2, rtl 0). Ledger, S2 and size receipts name `<pinned-rv32-sdk>` and Buildroot 2021.11. Builder leg 0 does not (F2). |
| RES1 lane name in docstring | **CLOSED** | `acmp_owed_mutants.py:1` reads exactly the requested text. |
| RES2 PR-body 144 -> 152 wording | **retained** (RES1 above) | PR body line 47. |
| RES3 BIND_RX case in the kept-command sentence | **retained** (RES2 above) | `MAILBOX_SPLIT.md:582`. |
| S1 pin the BIND_RX-only-answered one-pass exception | **superseded** | The redelivery removes the exception (`acmp_mbx.h:42-44`: no timer probe ahead of a waiting command). K4 (`:1344`) and K5 (`:1364`) pin "ahead of the timer probe". |
| S2 `__lshrdi3` in the `rv32` arm | optional, retained (S1 above) | — |
| S3 S2 README "drops" wording | **CLOSED** | `tb/verilator/ctrl_service_budget/README.md:553-557,576` say "At tsn-c-stack `70936b77` …"; `scenario.py:827-828`. |
| S4 one record vs every waiting record | **superseded** | The adapter now keeps PORTING.md:88's rule as written (`acmp_mbx.c:157-175`). |

R830-1, as the round-2 ruling (issuecomment-6806698193) lists them. Checked against code here; the reviewer's own text is cross-checked in the addendum below.

| Item | State at `bfe7a9d6` | Line / evidence |
|---|---|---|
| F1 the later-command bound, and meeting the redelivery rule with a test that fails without it | **CLOSED for the bound and the rule; the stop clause is F1 above** | `acmp_mbx.h:28-51` states n + 1 + f + r for a kept or waiting command. The code keeps PORTING.md:88 (`acmp_mbx.c:157-190`). K4/K5 fail without the waiting-record redelivery (plants `acmp-redelivery-takes-no-waiting-record` and `-only-behind-a-kept-command`, both caught). No change inside tsn-c-stack was needed (submodule at `715589c1`, clean). |
| F2 S2 harness text says the core drops commands this pin keeps | **CLOSED** | `README.md:553-557`, `:576`; `scenario.py:827-828` (two lines, module held at 1,000 lines). |
| F3 lane name in the new docstring | **CLOSED** | `acmp_owed_mutants.py:1`. |

**Addendum: R830-1's report cross-checked after my verdict and ledger were written.** It changes neither.
- R830-1 F1 offered (a) a decision accepting one-record redelivery, or (b) the contract's rule. The head implements (b).
  - K4 (`test_acmp_mbx.cpp:1344`) is that reviewer's probe P1, case for case: GET_RX_STATE, two PROBE_TX_RESPONSEs that need no answer, GET_RX_STATE, and sink 0's TMR_NO_RESP due in the third pass. It asserts pass 10 (`ACMP_MBX_KEPT_PASSES + 1`), the contract figure.
  - Its plant `acmp-redelivery-takes-no-waiting-record` is caught: 4 checks failed, the K4 line among them (`receipts/redelivery_probe.log`).
  - The A1 take bound is qualified for the kept state (`acmp_mbx.h:117-127`).
  - The stated bound now covers no-answer frames and an only-answered BIND_RX (`acmp_mbx.h:42-49`).
  - So R830-1 F1 is CLOSED, apart from the stop clause, which is my F1.
- R830-1 F2's verification grep (`git grep -n "drops the commands\|busy drop\|may never be answered" -- tb/verilator/ctrl_service_budget`) gives one hit, `README.md:554`, which carries the pin label "at `70936b77`" (`receipts/r830_f2_grep.txt`). So F2 is CLOSED.
- R830-1 F3: `acmp_owed_mutants.py:1` has the exact fix. CLOSED.
- R830-1 S1: still open, optional. Retained as S3 above.

## Scope checks (the assignment's items)

1. **Round-1 findings:** see the table above. F1 is closed. F2 is partly closed and retained as F2.
2. **Redelivery and its RAMB36 effect, derived from the build.** I installed the pinned SDK offline from the digest-matched archive and verified it with `ci_rv32_sdk.py --verify-only`, rc 0. Then I compiled `acmp_mbx.c` at `50e2a722` and at the head with the image flags (`scripts/acmp_mbx_rv32_size.sh`, `receipts/acmp_mbx_rv32_size.log`):
   - `on_poll` 136 -> 260 B with `redeliver` inlined, and `acmp_mbx_attach` 240 -> 252 B. The adapter's text grows 1,692 -> 1,844 B. The author's linked image shows 128 -> 244 and +12 B (`fixture-1x1-if2-symbols-round1-head-vs-redelivery.diff`), so the same cause at the same size.
   - `sizeof(struct acmp_mbx)` is 5,272 -> 5,272 B at one interface (the pointer fills padding) and 5,280 -> 5,288 B at two. That is exactly the re-key of `ctrl_plat` 20,072 -> 20,080 (1x1/2if) and 21,384 -> 21,392 (8x8/2if) at `ctrl_memory.py:217` and `ctrl_memory_ledger.py:26`. The 1if keys stay unchanged.
   - `ACMP_MBX_PASS_MAX` compiles to 1,030 -> 2,754 (1if) and 1,061 -> 2,785 (2if).
   - The fixture receipts (`round2/fixture-{base,r1head,head}`) give 1x1/2if `rom` 106,408 -> 106,552 B (+144). Against three banks of 106,496 B that is 56 B over, so a fourth 2,048 B bank is needed: 40.5 -> 41.0 RAMB36, as accepted by issuecomment-6807277620. No other point's banks move.
   - Fixture `rom` margins at the head: 1,512, 1,992, 88 and 480 B. The 8x8/1if point is now the tightest, as `SPLIT_CONTROL_MEMORY.md:312` says.
   - Platform: 8x8/2if is refused by name at the old key (`platform-8x8-if2-refusal.log`), 59.0 at the new key, and 1x1/2if stays 42.0.
   - Limit: I could not link the LiteX images here, because there is no LiteX environment on this host and installing one would be a shared install. The bank arithmetic is from the receipts; the code and struct growth is my own build.
3. **The eleven pinned-SDK steps** run and pass at the head (table above). The gate summary at the head is 150 rc 0, 215 not run with a reason, 0 bad.
4. **S2 at both pins** (`round2/s2/{base,head,final}-{1x1,8x8}.table.md`, all rc 0):
   - At `70936b77` the four `backlog.owed_behind{0..3}` commands are NEVER ANSWERED: at least 362.726 ms at 1x1 and at least 370.366 ms at 8x8.
   - At `715589c` with the redelivery all four are answered at both points: 94.958 / 98.722 / … / worst 104.568 ms at 1x1, and 120.289 / 127.860 / 133.109 / 138.526 ms at 8x8. These are over S2's 20 ms ceiling and within Milan v1.2 Table 5.26's 200 ms.
   - The head tables are byte-identical to `8ffcf2fc`'s (the delta between them is a comment). The head S2 image's `rom` (104,984 B) equals the head fixture's 1x1/1if.
5. **Load figures:**
   - The PR body (lines 88-100) and HANDOFF.md:92-124 record 1x1/1if 0.483 (0.70, within), and 8x8/2if 0.767 under the committed rule and 0.730 with nested `acmp_rx` charged to its record.
   - They are labelled "recorded, not graded" and point to #890 (issuecomment-6811790762).
   - No file in `1d6bf555..bfe7a9d6` carries 0.767, 0.730, 0.483, a flip check, or `load_grade` / `flip_grade` / `poll_grade` (`git diff | grep`, `git ls-files`). Nothing is graded in this PR.
6. **Items handed to S2b's sync:** 8x8/2if 58.0 against 57.5, the `__lshrdi3` hot-list entry, and the 1x1 ACMP poll measured at 10,974 against 6,500. They are stated in the PR body (line 155) and HANDOFF.md:131-133.
   - None of them can land in this PR. `poll_grade.py`, `ctrl_split_hot.txt` and `ctrl_hot.py` are not tracked on this base.
   - The 58.0 belongs to S2b's own image (122,984 B of `rom`). This base's 8x8/2if fixture is 120,352 B and plans 57.5, within its ledger.
   - None of them has to be in this PR.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `acmp_mbx.c:157-190` against tsn-c-stack `docs/PORTING.md:74-121` (ACMP-12 redelivery rule: kept first, arrival order, until declined, before timer service) at `715589c1`. The head code passes my three-command arrival-order test (`receipts/loss_probe_arm_at_head_code.log`). `acmp_mbx.h:28-51` n + 1 + f + r against PORTING.md:107-112. S2 answer times against Milan v1.2 Table 5.26. The 41.0 RAMB36 and 2,754 bounds against issuecomment-6807277620. Load figures recorded and not graded, against issuecomment-6811790762. | R829-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| RTL | CLEAN | `git diff --name-only 50e2a722..HEAD -- hdl '*.sv' '*.v' '*.svh'` and the whole PR from `1d6bf555` are both empty, and there is no submodule change in the delta. Firmware contracts the delta depends on: `ctrl_loop.c:121-157` (polls run after receive service, so `l->frame` is free), `mbx.c:386-389` (BAD resynchronises), `mbx_hal.h:46-48` and `ctrl_loop.h:18-26` (level wake), `ctrl_app.c:51-52` (init then attach, so `m->loop` is set before any poll). Widths and bounds compiled on the pinned SDK (`receipts/acmp_mbx_rv32_size.log`). | R829-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| Robustness | UNCLEAN (F1 open) | `acmp_mbx.c:157-190` under 13 plants (11 caught; F1's escape is real, the other is equivalent, S2). Refused record (K6, `mbx.c:386-389`), full ring (K7), reset (K3, `memset` clears `loop` and `kept` together; attach re-sets it), sleep at one owed frame (E3). | R829-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| Tests | UNCLEAN (F1 open) | `test_acmp_mbx.cpp:1118-1155,1184-1420`, `acmp_owed_mutants.py:1-131`, `coverage.ratchet:5`. Head campaign `rtl-fast__firmware-control-mutants__ci_step_9.log` (585/585), my plant reruns across six arms, and the disposable loss test. | R829-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| Docs | UNCLEAN (F2 open; RES1 to RES3 are residue) | `MAILBOX_SPLIT.md:578-590,672-781` (held to the compiled headers by my rerun of the `service_bounds` arm: 47 checks, 0 failures, 38/38 controls, `receipts/ctrl_service_bounds.log`; hand checks 8,262 = 3 x 2,754, 24,786 = 9 x 2,754, 3,507 = 2,754 + 753), `SPLIT_CONTROL_MEMORY.md:94-97,293-312` against the fixture and platform receipts, the `ctrl/README.md` and `maap/README.md` figures, the S2 README, the PR body (174 lines, at the head), HANDOFF.md, and the builder-leg receipts. Comment rule: no new lane label, round, reviewer ID or comment ID in the delta's source comments. | R829-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |

## Evidence (this packet)

- Published author packet: archive `35242f33a935cf336ba0c49f3a27d9b634da66d0`, `review-evidence/tsnpin-r1` (branch `tsnpin-review-evidence` tip). All 2,235 entries of its `MANIFEST.json` re-hash to their `published_sha256`, with 0 unlisted files (`receipts/evidence_manifest_check.txt`). The archive commit is not signed: integrity rests on the manifest and the commit ID.
- `scripts/redelivery_probe.py` -> `receipts/redelivery_probe.{log,rc}`: the six new author plants and seven of mine, `acmp` arm, `--jobs 16`.
- `scripts/redelivery_probe_arms.py` -> `receipts/redelivery_probe_arms.{log,rc}`: the two escapes in five more arms.
- `scripts/redelivery_loss_probe.py` -> `receipts/redelivery_loss_probe.{log,rc}`, `receipts/loss_probe_arm_at_head_code.log`, `receipts/loss_probe_arm_with_defect.log`.
- `scripts/acmp_mbx_rv32_size.sh` (with `scripts/shim/string.h`, a declarations-only stand-in for picolibc's header) -> `receipts/acmp_mbx_rv32_size.log`.
- `receipts/sdk_install.log`, `receipts/sdk_verify_only.log`: the pinned SDK, offline, from the archive whose sha256 is `scripts/ci_rv32_sdk.py:25`'s.
- `scripts/service_bounds_arm.py` -> `receipts/ctrl_service_bounds.{log,rc}`.
- `scripts/empty_kept_probe.py` -> `receipts/empty_kept_probe.{log,rc}`; `receipts/r830_f2_grep.txt`.
- `receipts/restore_check.txt`: the clone after the probes. HEAD and the index tree are `32d7e528`, diff-index and diff-files are clean, no untracked or ignored files remain, every tracked blob re-hashes to its index entry with its mode, and every initialised submodule (protocol-processor, gptp-processor, lwSRP, tsn-c-stack at `715589c1`, verilog-axis) is checked out at its gitlink with no untracked or ignored file. Probe `__pycache__` directories, including one inside protocol-processor, were removed.

## Real limits

- No LiteX environment exists on this host, so I did not link the fixture, platform or S2 images. The bank and RAMB36 arithmetic comes from the author's receipts. The code and struct growth behind it is my own compile on the pinned SDK, of `acmp_mbx.c` alone, with a declarations-only `string.h`.
- I did not rerun the full control, AECP or SRP campaigns, the builder legs, the workflow replica, S2, or `load_grade.py` / `flip_grade.py`. I relied on the author's published receipts, spot-checked as above.
- The S2 receipts identify their tree by the author's snapshot label. I corroborated it by the image `rom` size equal to the head fixture's, not by a tree hash.
- Physical calibration NOT RUN. Field skips and hosted contexts are not hardware proof. I claim no manager source bank and no act result.

## Pending manager duties

- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`), builder and native banks, at the merge turn, and link its receipts on the PR.
- Own hosted and act acceptance at the exact head, including exact-head `verilator-suites` and `yosys-portability` for a ready PR.
- Carry RES1 to RES3 to the residue checklist.
- Rule on F1 and F2's fixes, then a delta round on the new head.
- #890 owns the 0.75 flip ceiling, the nested-receive accounting rule and their controls. S2b's sync owns the 58.0 ledger, the `__lshrdi3` hot-list entry and the 10,974-cycle restatement.

R829-2 FINISHED
