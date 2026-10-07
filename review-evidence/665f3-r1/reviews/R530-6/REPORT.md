[R530] POSITIVE - exact head d8060d87f892239ac4e598d0a8556cbfcd4a52ec

R530-6: internal, cleared-context, independent review of issue #665 lane F3 / PR #688, round 7.

- Head `d8060d87f892239ac4e598d0a8556cbfcd4a52ec`, tree `7db44a4a68c725ee0f4a74cd453eb82134c8bfcd`.
- Delta reviewed: `13e71513..d8060d87`, three one-line commits, four files, tests and docs only (`receipts/delta_files.txt`).
- Baseline: R530-5 and R531-5 at `13e715136b0b7c8d9763e0b730d9709f2c9f5932`.
- Assignment: #665 comment 6041160063. REVIEW READY: comment 6042044802.

## Verdict

**POSITIVE.** All five lenses are CLEAN at this head.

- No BLOCKER, MAJOR or MINOR is open.
- R530-5-F1 (MINOR) is **RESOLVED**. R530-5-S1 and R530-5-S2 are addressed.
- One new RESIDUE (R530-6-R1): the PR body still describes round 6.
- One prior RESIDUE (R530-4-R1) is retained.
- Neither residue affects the verdict. Both go to the manager's residue checklist with their exact fixes.

## The five verification points

### 1. R530-5-F1 is closed

U6 is `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1008-1084`, and the new check is at `:1053-1076`. It runs in the `acmp` and `acmpif2` arms.

**What it checks.** For every captured frame on `MBX_CH_MAAP`, it reads the Ethernet source (bytes 6..11, `wire_be64(f->bytes + 6) >> 16`). It compares that source with `model.own_mac[f->interface]`, the OWN_MAC the open wrote for that interface. Each interface needs at least 3 such frames and none from another MAC (`:1074-1075`).

**Why that is the right property.** The model's own-unicast tuple compares a frame's destination with `own_mac[arrival interface]` (`host/mbx_model.c:289-299`). That is the contract's DEFEND-to-own-unicast `maap` row (`docs/reference/MAILBOX_CONTRACT.md:389`; REQUIREMENTS.md:73 and :91-93; IEEE 1722-2016 B.2.1). So the check pins exactly the condition under which a DEFEND answering this station's PROBE is admitted.

**Planted defects.** I planted each one alone in a copy of the tree and ran all 16 arms (`scripts/probe_mutant.py`, `receipts/probes/*.log|json`):

| Defect | Arms that fail | Failing lines (all of them) |
|---|---|---|
| `app-maap-mac-per-interface` (`mac[k] = cfg->entity->mac + k`) | `acmpif2` only | 1: `AcmpMailbox.U6...: U6 MAAP sends from its own unicast MAC, where a DEFEND is admitted, interface 1` |
| `app-own-mac-per-interface` (`own_mac[i] = cfg->entity->mac + i`) | `acmpif2` only | 1: the same U6 line, interface 1 |

The other 15 arms exit 0 with no `[FAIL]` for both defects, so the only cause is the named U6 interface-1 check.

**The one-interface arm.** These two defects cannot show at one interface (k = 0). So I added a reviewer probe, `rp-maap-mac-plus-one` (`mac[k] = cfg->entity->mac + 1u`):

- `acmp` fails U6 at interface 0;
- `acmpif2` fails U6 at interfaces 0 and 1;
- nothing else fails.

The check therefore bites in both arms.

**Control.** `rp-null` (an identity plant through the same machinery) passes all 16 arms.

### 2. R530-5-S1 is addressed

F6 is `test_acmp_mbx.cpp:923-977`, and the tie is at `:970-975`. It asserts:

`CTRL_APP_PASS_MAX == ACMP_MBX_PASS_MAX + MAAP_MBX_PASS_MAX - CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2)`

I recomputed both sides from the macro terms (`scripts/recompute_bounds.py`, `receipts/recompute_bounds.txt`):

| Interfaces | Left side | `ACMP_MBX_PASS_MAX` | `MAAP_MBX_PASS_MAX` | Shared event reads | Right side |
|---|---|---|---|---|---|
| one | 1,580 | 1,012 | 616 | 8 x 6 = 48 | 1,580 |
| two | 1,659 | 1,043 | 664 | 48 | 1,659 |

The identity is exact for these reasons:

- MAAP's share (`app/ctrl_app.h:62-66`) equals `MAAP_MBX_PASS_MAX` (`maap/maap_mbx.h:18-19`) less its per-event `6u`.
- That `6u` equals ACMP's `MBX_EV_WORDS + 2u` (`acmp/acmp_mbx.h:140`).
- Its record term `20u` equals `CTRL_APP_MAAP_RX_RECORD_MAX` (2 + 2 + 64/4).

**The author's two defects.** Each fails only F6's new line:

- `app-three-way-bound-drops-maap` fails in `acmp` and `acmpif2`;
- `app-three-way-bound-one-maap-poll` fails in `acmpif2` only, since it is identical at one interface.

**Reviewer probes.** Each fails only F6's tie, in both arms:

- `rp-maap-pass-event-7` (MAAP's own per-event `6u` changed to `7u` in `maap_mbx.h`);
- `rp-share-rx-record-plus-one` (`CTRL_APP_MAAP_RX_RECORD_MAX` raised by one).

So the tie also catches drift on MAAP's side, which no `maap` arm test pins.

### 3. R530-5-S2 is addressed

The new paragraph is at `docs/design/MAILBOX_SPLIT.md:709-713`. It uses the three-way pass of 1,580 and the "taken by pass" counts of the table at `:698-704`:

| Bound | Accesses | At 1 us | Status |
|---|---|---|---|
| Event | (2+1) x 1,580 = 4,740 | 4.74 ms | fits T_svc |
| Owed frame | (8+1) x 1,580 = 14,220 | 14.22 ms | over T_svc, under the ceiling |
| Full acmp ring | (10+1) x 1,580 = 17,380 | 17.38 ms | under the ceiling |
| Full adp ring | (21+1) x 1,580 = 34,760 | 34.76 ms | over the 20 ms ceiling |

- Every figure and classification recomputes. T_svc is 10 ms (`docs/reference/FR_NFR.md:323`, `:333`) and the ceiling is 20 ms (`MAILBOX_SPLIT.md:664-667`).
- "Which fits it without MAAP" also holds: the two-way owed bound is 9 x 1,012 = 9,108 accesses, or 9.108 ms.
- At two interfaces (1,659) the classification is the same: 4.98, 14.93, 18.25 and 36.50 ms. See SUGGESTION R530-6-S1.

### 4. No production change

**The linked ELFs are byte-identical to round 6.** I ran `ctrl_image.py --base 13e715136b0b...` with the pinned SDK (`scripts/image_compare.sh`, `receipts/image.log`, `receipts/elf_sha256.txt`):

| Shape | ELF sha256, head = base | Total bytes |
|---|---|---|
| `endstation_ax7101_1x1_tdm8` | `3d797e8f19a8b065...` | 46,608 |
| `endstation_ax7101_8x8` | `96eaa98578ea8eee...` | 56,980 |

- `cmp` reports both pairs byte-identical, and every section delta is +0.
- The RV32I audit passes: `rv32i2p1`, 8,361 and 8,362 words.

**The SDK.** It was installed from the archive with the pinned sha256 `d42680e9...b78f` by the repository installer into a disposable prefix (`receipts/sdk_install.log`).

**Files touched.** `git diff --name-only 13e71513 d8060d87` lists only the four test and doc files (`receipts/delta_files.txt`). No file under `hdl/`, `sw/mailbox/`, the ctrl firmware sources (`acmp`, `adp`, `app`, `loop`, `maap`, `mbx`, `plat`, `port`, `wire`, `host`) or `sw/firmware/ctrl_nvm/` changed.

### 5. Ratchet, suite and campaign at d8060d87

**The ctrl gate.** I ran `test_ctrl_firmware.py --require-rv32 --jobs 2` (`receipts/suite.log`, rc 0). All 16 arms pass:

- `acmp` 84 and `acmpif2` 22;
- `acmpwalk` 127 and `acmpnvm` 7;
- `maap` 37 + 12, `maap_if2` 13 and `maap_debug` 1;
- reentry 122 + 122;
- the `rv32` arm builds with the pinned SDK.

F6's worst pass is 231 of 1,580 at one interface and 233 of 1,659 at two.

**The mutation campaign.** I ran `--self-test --slice K/20` for K = 1..20, rc 0 for all 20 (`receipts/campaign/slice*.log`):

- 469 of 469 caught (19 x 24, then 13), with 0 `ESCAPED` and no test named by no defect;
- the four round-7 rows are caught on their named tests and words, with 1, 1, 2 and 1 failing checks.

**Coverage.** `fw_coverage.py --check` passes with rc 0: 20 files, all at 100.00 % lines and branches after exclusions (`receipts/cov_check.log`). `ctrl_app.c` is 42/43 lines and 40/44 branches raw, which is 100 % after its recorded exclusions. `--selftest` reads 28 of 28 planted cases as planted (`receipts/cov_selftest.log`).

**The mutant count.** The table counts 469 in total, 273 in `acmp_mutants.MUTANTS` and 78 in `acmp_review_mutants.MUTANTS`. This matches the README's "273" and the REVIEW READY's "469 of 469".

## Findings

### R530-6-R1 | RESIDUE | Docs | PR #688 body, section "Status" (body lines 16-24 at review time) | the PR body still reports round 6 as the current state

- **Evidence:**
  - The body opens "GREEN at `13e715136b0b7c8d9763e0b730d9709f2c9f5932` (round 6, #665 comment 6037650104)". It reports "the ctrl campaign, 465 of 465 (F3's 269 with round 6's 15, F2's 96, F0 and FC's 100)".
  - The PR head is now `d8060d87`, whose campaign is 469 of 469 with F3's 273.
  - The Tests row does not mention U6's per-interface MAAP source check or F6's tie.
  - Every statement is true as dated to round 6. No measurement, figure in the tree, test or code is wrong. The full round-7 evidence is public in REVIEW READY 6042044802.
- **Lenses:** Docs.
- **Impact:** a cold reader of the PR alone sees round 6 as the current state.
- **Exact fix:**
  - Status line: replace "GREEN at `13e715136b0b7c8d9763e0b730d9709f2c9f5932` (round 6, #665 comment 6037650104)" with "GREEN at `d8060d87f892239ac4e598d0a8556cbfcd4a52ec` (round 7, #665 comment 6041160063; round 6 was `13e71513`, comment 6037650104)".
  - Campaign line: replace "465 of 465 (F3's 269 with round 6's 15, F2's 96, F0 and FC's 100)" with "469 of 469 (F3's 273 with round 6's 15 and round 7's 4, F2's 96, F0 and FC's 100)".
  - Tests row: append "U6 also requires every MAAP frame on each interface to carry that interface's OWN_MAC as source; F6 also ties `CTRL_APP_PASS_MAX` to `ACMP_MBX_PASS_MAX` + `MAAP_MBX_PASS_MAX` - 48."
- **Verification:** read the PR body after the manager's update.

### R530-6-S1 | SUGGESTION | Docs | `docs/design/MAILBOX_SPLIT.md:705-713` | name the interface count of the 1 us figures

- The new paragraph's figures are the one-interface ones (1,580 a pass).
- The F6 sentence above it says "15 events, 12 acmp records and 7 maap records ... (233 at two interfaces)". At two interfaces the backlog the test builds holds 14 event records (`receipts/suite.log`, the `acmpif2` F6 line).
- Optional:
  - add "at one interface" to the paragraph, and the two-interface times (4.98, 14.93, 18.25 and 36.50 ms, the same classification);
  - say "14 at two interfaces" in the F6 sentence.
- Nothing stated is false. No lens effect.

### Observation (not a finding)

- `rp-maap-pass-event-7` changes `MAAP_MBX_PASS_MAX`'s own per-event term. It escapes every `maap`/`maap_if2` test and is caught only by this round's F6 tie.
- That is lane F2's bound, outside this lane's scope. Round 7's tie is now the check that pins it.

## Prior public review findings

I read these only after my own pass and probes. I did not read the concurrent R531-6 report.

| Finding | Disposition at d8060d87 | Evidence |
|---|---|---|
| R530-5-F1 MINOR, Tests | **RESOLVED** | Point 1: U6 `test_acmp_mbx.cpp:1053-1076` in both arms. Two planted defects are caught by `acmpif2` U6 interface 1 as the sole failure, and a reviewer probe is caught by `acmp` at interface 0. Campaign 469/469. |
| R530-5-S1 SUGGESTION, Tests | **ADDRESSED** | Point 2: F6 tie `:970-975`, two author defects and two reviewer probes. |
| R530-5-S2 SUGGESTION, Docs | **ADDRESSED** | Point 3: `MAILBOX_SPLIT.md:709-713`, all four figures recompute. |
| R530-4-R1 RESIDUE, Docs | **RETAINED** (verdict-neutral) | Published `review-evidence/665f3-r1/author-r6/HANDOFF.md:483` on the evidence branch head `109f3a6b` still reads "and its images would fail the audit (as round 4's do)". No round-7 handoff is published. **Exact fix** (unchanged): replace that clause with "and, since no library is linked, its images pass the audit with the same figures; only round 4's library-linked images fail it". |
| R530-4-S1, R530-4-S2 SUGGESTION, Robustness | Retained, optional | `ctrl_image.py` is unchanged. Under `python3 -I` it still fails (`ModuleNotFoundError: ctrl_arms`). |
| R530-3-F1 / R531-3-F1, R530-3-R1 | Still RESOLVED | The image table reproduces byte for byte (point 4). The PR title is unchanged. |
| R531-2-F1; R530-2-F1..F3, R1..R3; R531-1-F1..F5; R530-1-F1..F5, R1 | Still RESOLVED | No production file changed since `13e71513` (point 4). Their planted defects are inside the 469 caught. |
| R530-2-S1..S3 SUGGESTION | Unchanged | No lens effect. |

## Lens results

```text
[R530] PASS Conformance - test_acmp_mbx.cpp:1053-1076 vs REQUIREMENTS.md:73,91-93, MAILBOX_CONTRACT.md:389, host/mbx_model.c:289-299; ctrl_app.c:16-30,56-62 (unchanged, ELFs identical) - U6 asserts the B.2.1 DEFEND-admission condition per interface; assignment 6041160063 items 1-3 met; the T_svc paragraph is consistent with FR_NFR.md:323,333 and the 20 ms ceiling.
[R530] PASS RTL - receipts/delta_files.txt, elf_sha256.txt, image.log - no RTL, contract, register-map or firmware source in the delta; both shapes' linked ELFs are byte-identical to 13e71513 and the RV32I audit passes; the macro arithmetic (acmp_mbx.h:139-145, maap_mbx.h:15-19, ctrl_app.h:62-66) recomputes at one and two interfaces.
[R530] PASS Robustness - receipts/probes/*.json (8 plants x 16 arms), test_acmp_mbx.cpp:1053-1076 - each U6/F6 defect fails only its named check; a per-interface violation, a one-interface violation, and drift on MAAP's or the app's side of the bound are each caught; the null plant passes; the U6 loop reads only frames within the model's 64-frame capture (a lost frame would crash loudly, not pass silently).
[R530] PASS Tests - receipts/suite.log (16 arms), campaign/slice1..20.log (469/469), cov_check.log (20 files at 100 %), cov_selftest.log (28/28), probes/ - the new checks fail for the defects they claim, at the arms claimed, with named words; no test is unnamed by a defect; the ratchet holds.
[R530] PASS Docs - sw/firmware/ctrl/README.md:107-130,226-248, MAILBOX_SPLIT.md:705-713,955-958, acmp_review_mutants.py:1-11,403-419, receipts/docs_gates.log - counts (273/469), figures and clause citations verified; docs_check, em-dash (base 13e71513 and dev e21c1ca0), doc style, TOC, py/cpp idiom, hygiene and bare-metal-only gates rc 0; the PR-body staleness is RESIDUE R530-6-R1, which leaves the lens clean.
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | U6 vs REQUIREMENTS.md:73,91-93, MAILBOX_CONTRACT.md:389, the model filter `mbx_model.c:289-299`; the T_svc paragraph vs FR_NFR.md:323,333; assignment 6041160063 | R530-6 | `d8060d87f892239ac4e598d0a8556cbfcd4a52ec` |
| RTL | CLEAN | delta file list (no RTL, contract or firmware source); ELF byte-identity at both shapes; RV32I audit; pass-bound macro arithmetic at one and two interfaces | R530-6 | `d8060d87f892239ac4e598d0a8556cbfcd4a52ec` |
| Robustness | CLEAN | 8 single-defect plants across all 16 arms (4 author, 3 reviewer, 1 null); U6 capture handling | R530-6 | `d8060d87f892239ac4e598d0a8556cbfcd4a52ec` |
| Tests | CLEAN | full ctrl gate (16 arms), campaign 469/469 in 20 slices, coverage ratchet `--check` and `--selftest`, `test_acmp_mbx.cpp:923-977,1008-1084`, `acmp_review_mutants.py:403-419` | R530-6 | `d8060d87f892239ac4e598d0a8556cbfcd4a52ec` |
| Docs | CLEAN (R530-6-R1 and R530-4-R1 RESIDUE, verdict-neutral) | ctrl README, the MAILBOX_SPLIT.md three-way section and Open items, the mutant table docstring, the PR #688 body, the docs and idiom gates | R530-6 | `d8060d87f892239ac4e598d0a8556cbfcd4a52ec` |

## Real limits

**Not run by this reviewer:**

- the mbx RTL suites and co-simulation, the RTL campaign, lint, Yosys, Vivado and area;
- the store campaign and the standalone store gate.

The delta touches none of their inputs (`receipts/delta_files.txt`). The coverage run did execute the store arms ("saved-state store coverage run: PASS"). The full parent, processor, gPTP and builder banks are outside this assignment.

**Hosted evidence.** At 2026-10-07T16:45Z (`receipts/hosted_snapshot.txt`):

- Verilator shards 0, 1, 2 and 4 and `docs-check` were still in progress.
- "Physical gPTP (nightly and manual)" was skipped. A skip is not an executed job.
- The other listed contexts had succeeded.
- I ran no local CI replica or container.

**Linked public evidence.** The tree at `c961acab` holds the author's round-1 handoff at `351ae81f`. It predates this head and carries no bank result for `d8060d87`. I found no manager evidence comment for this head on #665 or PR #688 by 16:45Z. My verdict rests on my own runs above.

**Merge candidate.** The final current-dev candidate (source base `021b9c1f`, live dev `e21c1ca0`) is not validated here.

**Physical calibration** was NOT RUN. The access time (A4) is unmeasured, so every T_svc statement is in mailbox accesses at an assumed 1 us. No hardware was used.

**Toolchain.** Host compiler GCC 16.2.1 with GoogleTest 1.18.0. RV32 SDK: `riscv32-ilp32d--glibc--stable-2025.08-1`, GCC 14.3.0, archive sha256 as pinned.

**Clone integrity after the probes** (`receipts/integrity.txt`). Every probe planted into copies under `scratch/`; the clone was never edited. After the runs:

- HEAD and the index tree are both `7db44a4a`;
- the worktree equals the index, which equals HEAD;
- 1,186 tracked blobs and modes match;
- no assume-unchanged or skip-worktree flags are set, and there are no untracked files;
- the gitlinks are `protocol-processor` `ead80360`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e`; `external` `efeb541a` is uninitialised, as at the start.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Carry R530-6-R1 (PR body) and R530-4-R1 (round-6 handoff line 483) to the residue checklist with the exact fixes above.
- Confirm the exact-head hosted contexts finish green. Run the act-first local replica as the CI policy requires.
- Build and validate the current-dev merge candidate at the merge turn.
- Obtain the second independent positive review. Do not merge without explicit maintainer authorization.

R530-6 FINISHED
