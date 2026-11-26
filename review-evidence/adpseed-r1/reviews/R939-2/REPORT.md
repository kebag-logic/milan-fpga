[R939] POSITIVE - exact head 9590206015ead2cfd2ef955c2f4ef8d8c4e4762c

# Independent review R939-2: kebag-logic/tsn-c-stack PR #40 (Closes #39), delta re-review

- Exact head `9590206015ead2cfd2ef955c2f4ef8d8c4e4762c`, tree `4064709bec5ebb15b18f16b13a5bae94688a4d56`.
- Delta under review: `5e6ab995..95902060`, one commit, on `main` `a795471c0abc4e38f7e5146b4e539dd607b6f501`.
- Reviewer role: internal independent reviewer, cleared context, own detached clone.
- Verdict: **POSITIVE**. No MINOR, MAJOR or BLOCKER is open.
  - R939-1 F1, F2, S1 and R2 are resolved at their cause.
  - R1 is retained as RESIDUE. It sits in a milan-fpga evidence note that this PR does not carry.
  - New items: two SUGGESTIONs (S2, S3) and two RESIDUE items (R3, R4).
- Token economy: code the delta does not touch keeps its R939-1 lens verdict. Only `leave_down`'s sum changed in source. All other changes are tests, plants and prose.

## 1. What was reconstructed, in order

1. `CONTRIBUTING.md` (the repository has no `AGENTS.md`). It requires a failing assertion and a runnable planted defect for each regression, one-line commit subjects and no lane labels in source.
   - The delta commit's subject is one line, with no body.
2. `docs/` contract files: `REQUIREMENTS.md` (ADP-02, PORT-01), `PORTING.md` (ADP callbacks), `DEVIATIONS.md` (DEV-04), `VERIFICATION.md`, and the generated `TESTS.md` and `TRACEABILITY.md`.
3. Issue #39's frozen scope and acceptance. The issue has no maintainer or manager comments.
   - Scope: one fresh sample at each transition out of DOWN, mixed with the MAC address, the entity ID and the interface. No sample at a duplicate or disabled LINK_UP, or at any other draw.
   - Acceptance: (1) sample counts; (2) distinct and uniform first delays; (3) one planted defect per rule, each caught; Linux and RV32 green.
   - Manager decision on R939-1 F1, as given in this review's brief: option (a), the plain modular sum of IEEE 1722.1-2021 6.2.4.2.2, with no end-around carry.
4. The diff `a795471..95902060`, then the one-commit delta `5e6ab995..95902060` and its history.
5. Public evidence, checked as follows:
   - The round-2 author packet, milan-fpga `adpseed-review-evidence` @ `d33da1ea`, `review-evidence/adpseed-r2/`. All seven `MANIFEST.json` sha256 values match the published bytes.
   - `author/PR-BODY.md` equals the live PR body, apart from a trailing newline.
   - The round-1 packet at `6682d3c0` was used only to check R1.
6. Prior public findings, read only after my own pass over the delta:
   - R939-1's findings are resolved in section 2.1.
   - R940-1's findings were read only after this verdict and ledger were written. They are resolved in section 8.

## 2. Findings

### 2.1 R939-1 findings at this head

| ID | R939-1 severity | Status at `95902060` | Evidence (own control) |
|---|---|---|---|
| F1 | MINOR | **RESOLVED** (option (a)) | See below. |
| F2 | MINOR | **RESOLVED** | See below. |
| S1 | SUGGESTION | **RESOLVED** as suggested. A residual gap is recorded as S2. | See below. |
| R1 | RESIDUE | **RETAINED** | milan-fpga@6682d3c0 `review-evidence/adpseed-r1/author/REVIEW-READY.md` still says "receipts/stack holds validate.py, RV32, plants, coverage and the distribution test". That packet is frozen evidence, and the round-2 note says the manager owns it. The exact fix in R939-1 stands. The manager carries it to the residue checklist. |
| R2 | RESIDUE | **RESOLVED** | `docs/PORTING.md:144` now reads "a local clock sample at each transition out of DOWN". `docs/DEVIATIONS.md:13` (DEV-04) reads "The integrator supplies a clock sample (ADP) or entropy (ACMP)". |

**F1, the plain sum, resolved at its root:**

- `src/adp.c:105`: `uint32_t sum = (uint32_t)e->mac + sample;`. The `sum += sum < sample;` line is gone.
  - This is the least significant 32 bits of the 48-bit MAC address plus the 32-bit sample. Bits above bit 31 of either operand cannot reach the low 32 bits of the sum. IEEE 1722.1-2021 6.2.4.2.2 asks for "the least significant (most rapidly varying) octets of the sum".
  - The rest of `leave_down` is unchanged: two `mix` rounds with the earlier state, both entity-ID words and the interface, then the zero guard.
- **A27 pins the modulo-2^32 wrap** (`tests/test_adp.cpp:612-619`):
  - MAC `0xFFFFFFFF` with sample 5 has the sum `0x1_00000004`, whose low 32 bits are 4. MAC 0 with sample 4 has the sum 4. The two must seed alike.
  - An end-around carry gives 5 against 4.
  - Own run: plant `adp-seed-end-around-carry-added` is CAUGHT by A27's message "A27 the seed is the sum's least significant 32 bits, modulo 2^32 (6.2.4.2.2)" (`receipts/mutation-key-plants.json`).
  - My extra probe `r939-sum-high-word-folded` exclusive-ors the 64-bit sum's high word into the low word. It is also CAUGHT by that message (`receipts/probe-mutation.log`).
- **A22's constant, re-derived independently** (`probes/a22_derive.c`, `receipts/a22_derive.txt`):
  - The A22 fixture is: generator 0, interface 0, entity ID `0x1122334455667788`, MAC `0x001B921122AA`.
  - An exhaustive scan of all 2^32 samples finds **exactly one** sample that mixes to zero under the plain sum: `0xDE81995D`. Under the old end-around sum it was `0xDE81995C`.
  - Uniqueness is expected. The map from sample to sum, the exclusive-ors and `mix` are all bijections.
  - `0x921122AA + 0xDE81995D` carries out of bit 31, so A22 also exercises the wrap.
  - Linked against the real `src/adp.c`, sample `0xDE81995D` leaves the generator at `0x00042021`, which is xorshift32(1). The old constant `0xDE81995C` leaves `0xA54FC701`.
  - So the test's expected value is exactly "the seed mixed to zero and was replaced by 1, then one step was drawn".
- **A22 also works as a known-answer vector.** My probe `r939-sum-adds-mac-high-bits` adds the MAC address's top 16 bits into the sum. A27 cannot see that change, because its wrap pair has MAC high bits 0. A22 CATCHES it, because the zero-mixing sample depends on the exact formula.
- **Stuck-at-zero argument, checked against the code:**
  - `a->rng` is written only by `adp_init`'s `memset` (0), by `rng_next` (xorshift32, a bijection that fixes 0, so a non-zero state stays non-zero), and by `leave_down`, which never writes 0 (`src/adp.c:108`).
  - Every draw goes through `enter_delay`. Apart from `leave_down`, its callers need WAITING:
    - `adp_gm_change` (`:291`);
    - `adp_timer_expired` with the TMR_ADVERTISE timer (`:309`);
    - `adp_rx` (`:338`).
  - WAITING is set only by `advertise`. That runs only in DELAY (`:307`, `:354`), and DELAY is set only by `enter_delay`.
  - So the first draw follows a `leave_down`, and no draw ever runs on state 0. `ADP_STATE_DOWN` is 0, so a zeroed struct holds the same property.
  - `seed-left-at-zero` is CAUGHT by A22 (own run).
- **Docs and the clause claim:**
  - `docs/PORTING.md:177` states the least significant 32 bits of the sum, modulo 2^32.
  - `CHANGELOG.md:5` adds "The sum is the plain one, modulo 2^32: its least significant 32 bits."
  - ADP-02 still says "the sum of the MAC address and the local clock", which now matches the code.
  - No source, test or document in the tree still says "end-around" or "carries end around".

**F2, the ENTITY_DISCOVER draw, resolved:**

- A32 (`tests/test_adp.cpp:719-734`, registered at `:892` with `REQ: ADP-02, PORT-01`) works as follows:
  1. It takes one first draw (one sample).
  2. For the target equal to this entity's ID, and then for target 0, it expires the delay into WAITING (`ASSERT_EQ`).
  3. It delivers an ENTITY_DISCOVER and requires DELAY, `draws + 1`, and the seed count still 1.
- Own run: `adp-discover-draw-sampled` turns `adp_rx`'s `enter_delay` into `leave_down`. It is CAUGHT by "A32 an ENTITY_DISCOVER in WAITING draws its delay and takes no sample".
- My extra probes `r939-discover-zero-target-sampled` and `r939-discover-own-target-sampled` sample only for target 0 or only for this entity's ID. Both are CAUGHT by A32. Both targets are needed.
- The per-site probes `r939-gm-change-draw-sampled` and `r939-advertise-draw-sampled` are CAUGHT by A28. Each of the four non-DOWN draw sites is now held by its own assertion.
- `TESTS.md:167` and `TRACEABILITY.md` list A32 with its plant. The traceability and test-inventory gates pass.

**S1, the interface term, resolved:**

- A27 now compares interfaces 0, 1, 2 and 255 pairwise (`tests/test_adp.cpp:593-600`).
- The new plant `adp-seed-interface-low-bit-only` is CAUGHT by "A27 interfaces 0, 1, 2 and 255 sampled together draw apart". `adp-seed-without-interface` is also CAUGHT (own run).

### 2.2 New items at this head

#### S2 - SUGGESTION - Tests - the interface check samples four of the 256 values

- **Where:** `tests/test_adp.cpp:594` (`for (const unsigned i : {0u, 1u, 2u, 255u})`).
- **Evidence:** my probe `r939-interface-seven-bits` mixes `a->interface & 0x7F`, so interfaces 0 and 128 seed alike. It ESCAPES: no test fails (`receipts/probe-mutation.log`). Values 0, 1, 2 and 255 stay distinct under that mask.
- **Impact:** test strength only. The head is correct: `interface` is a `uint8_t`, and `<< 24` keeps all eight bits. Today's configurations use one or two interfaces.
- **Suggested:** in A27, draw for every interface value 0 to 255, and require 256 distinct states. That costs 512 first draws over both kinds, and it kills any truncation of the interface term.

#### S3 - SUGGESTION - Tests - A22's constant has no derivation note

- **Where:** `tests/test_adp.cpp:544` (`b.sample = 0xDE81995Du;`).
- **Impact:** the constant depends on `mix`, on the sum rule and on the test entity. Any change to these silently turns A22 into a test that no longer reaches the zero guard. A22 would then fail on its expected value, and the reason would not be obvious. This review needed an exhaustive scan to confirm it.
- **Suggested:**
  - Add a behaviour comment: "the one sample that mixes to zero for the test entity, interface 0 and a zero state, with the sum modulo 2^32 (ADP-02)".
  - Optionally, assert in A22 that the sample really mixes to zero, by checking that a neighbouring sample leaves a state other than `0x42021`.

#### R3 - RESIDUE - author evidence note (milan-fpga `review-evidence/adpseed-r2/author/REVIEW-READY.md`) - wrong receipt path and a truncated section

- **Defect:** line 24 cites `receipts/r4/tsn-c-stack-*`. The packet holds `author/receipts/tsn-c-stack-*`, with no `r4` directory. Section 3 ("milan-fpga at `4f6ee193`") stops inside its first list, after the H7 bullet.
- **Exact fix:**
  - Line 24: replace `receipts/r4/tsn-c-stack-*` with `author/receipts/tsn-c-stack-*`.
  - Complete section 3, or end it after the gitlink and H7 bullets with "the rest of the parent commit is reviewed on the parent PR".

#### R4 - RESIDUE - PR body - the Documents section repeats itself

- **Where:** PR #40 body, `## Documents`.
- **Defect:** a first bullet about `PORTING.md` and DEV-04 is set apart by a blank line. A later bullet repeats "`PORTING.md` states the seed contract".
- **Exact fix:** delete the later bullet's words "`PORTING.md` states the seed contract;", and remove the blank line after the first bullet so that the section is one list.

### 2.3 Comment rule over the delta

- The delta adds no source comment that names a bench lane, a lane, a review round, a reviewer ID or an issue-comment ID.
- The only new comment is `// REQ: ADP-02, PORT-01`.
- Test messages use test IDs (A22, A27, A32). They are not lane labels.
- A scan of the added lines in `a795471..95902060` found no match.

## 3. Lens evidence

### Conformance - CLEAN

The standards documents were not available in the review environment. The clause checks below use the clause wording quoted publicly in issue #39 and the PR body.

- **IEEE 1722.1-2021 6.2.4.2.2, seeding:**
  - "seeded using the least significant (most rapidly varying) octets of the sum of the requestor's IEEE 802 MAC address and the local real time clock". The 32-bit seed term is `(uint32_t)mac + sample` modulo 2^32, as section 2.1 shows.
  - The port contract (`docs/PORTING.md:175`) asks for the clock's least significant 32 bits at its finest resolution.
  - The extra mix with the entity ID, the interface and the earlier state is the scope that issue #39 freezes.
- **IEEE 1722.1-2021 6.2.4.2.2, uniform distribution and a maximum-length sequence:**
  - `draw_ms` and xorshift32 (13, 17, 5) are untouched by the delta.
  - A25, A26, A29 and A31 pass in my gcc and sanitizer runs.
- **Milan v1.2 5.6.3.5.2 and 5.6.3.5.3:** the startup and LINK_UP call sites of `leave_down` are unchanged (`src/adp.c:256`, `:274`). A30 counts one sample per qualified rise and none for a duplicate or disabled LINK_UP (own run).
- **Milan v1.2 5.6.3.5.4, 5.6.3.5.5 and 5.6.3.5.7 (the DISCOVER, TMR_ADVERTISE and GM_CHANGE draws):** none takes a sample. Each is now held by its own assertion (A32, and A28 for the other two), as section 2.1 shows.
- **Draw ranges, timers and other ADP rules:** unchanged. These are out of the issue's scope, and the delta touches none of them.

### RTL - CLEAN (no HDL in scope; freestanding RV32 target examined)

- This repository has no HDL. The delta changes one C statement and the tests. The HDL simulator was not needed, so its identity was not checked.
- The hardware-facing target is the freestanding RV32 port. My own run, `scripts/baremetal.py --jobs 2`, gives rc 0 for Debug and Release, with no unresolved symbols at the final link (`receipts/rv32-results.json`).
  - The **Release** ELF (`3113c0cc…`) and the Release `adp.c` object (`14721411…`) are **byte-identical** to the author's `tsn-c-stack-rv32.log`. This independently ties the author's RV32 receipt to this source.
  - The Debug hashes differ. Debug objects embed the build directory: my Debug `adp.c.obj` contains six absolute work-directory strings, and Release contains none.
- The core's imports are unchanged against the author's receipt. `__mulsi3` and `__umodsi3` are pre-existing, and `mix` itself has no multiply.

### Robustness - CLEAN

- The zero guard and the stuck-at-zero argument hold (section 2.1).
- The plain sum is injective in the sample for a fixed MAC address. That fixes R939-1's note that samples `0` and `2^32 - 1` collided under the end-around carry.
- The re-entry flags around `seed()` are unchanged: `adp-seed-port-unflagged` is CAUGHT.
- The re-entry rig's constant in `tests/test_adp_reentry.cpp` is unchanged and still valid. It uses MAC 0, so the sum cannot wrap. The `adp_reentry` tests pass in my run.
- The clang address and undefined-behaviour sanitizer suite passes (`clang-sanitizers-test` rc 0).

### Tests - CLEAN (S2 and S3 are suggestions)

- Own full kit at the exact head: `scripts/validate.py --jobs 4 --graphs` gives rc 0, **28 of 28 steps** (`receipts/validate-gates.json`). The author's `tsn-c-stack-gates.json` lists the same 28 gates at rc 0.
- Plants: **512 CAUGHT, 0 ESCAPED, 0 ERROR** (`receipts/mutation-summary.txt`).
  - This is 23 more than `main`'s 489, with `link-up-draws-startup-kind` and `seed-left-at-zero` restated. This matches the PR body.
  - The kill record shows the named message for each key plant (`receipts/mutation-key-plants.json`).
  - `docs/VERIFICATION.md:24` gives "508 core plants and four generated configuration plants", which totals 512.
- Coverage: lines and branches 100.00 % after exclusions in all four files (`receipts/coverage.log`).
  - `src/adp.c` is 215/217 lines and 95/102 branches, identical to the author's receipt.
  - My `coverage.log` and `validate-gates.json` are byte-identical to the author's `tsn-c-stack-coverage.log` and `tsn-c-stack-gates.json` (sha256 `96dbac14…` and `84f0dd54…`).
- Reviewer probes (`receipts/probe-mutation.log`): 6 of 7 CAUGHT. The one escape is the out-of-scope truncation in S2.
- The A22 re-derivation is in section 2.1.

### Docs - CLEAN (R1, R3 and R4 are residue)

- `PORTING.md:144` and `:175-177`, `DEVIATIONS.md` DEV-04 and `CHANGELOG.md:5` state the plain sum and the clock-sample contract. No end-around wording remains.
- `VERIFICATION.md`'s plant count matches the campaign.
- `TESTS.md` and `TRACEABILITY.md` are regenerated. The traceability and test-inventory gates pass.
- Standards citations only. Privacy gates pass.

## 4. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/adp.c:99-110`, `:240-343`; ADP-02; IEEE 1722.1-2021 6.2.4.2.2 wording from the issue and PR; Milan v1.2 5.6.3.5.2-5.6.3.5.7 call sites; A22 re-derivation | R939-2 (delta); R939-1 for unchanged draw and range code | `9590206015ead2cfd2ef955c2f4ef8d8c4e4762c` |
| RTL | CLEAN | No HDL in the repository; own RV32 Debug and Release build and run; Release ELF and `adp.c` object byte-identical to the author's receipt | R939-2 | `9590206015ead2cfd2ef955c2f4ef8d8c4e4762c` |
| Robustness | CLEAN | Zero guard and reachability trace; re-entry flags; re-entry rig constant; sanitizer suite | R939-2 | `9590206015ead2cfd2ef955c2f4ef8d8c4e4762c` |
| Tests | CLEAN | A22, A27, A28, A30, A32; `tests/mutations.json` delta; own validate (28/28), 512/512 plants, coverage, 7 reviewer probes | R939-2 | `9590206015ead2cfd2ef955c2f4ef8d8c4e4762c` |
| Docs | CLEAN | `PORTING.md`, `DEVIATIONS.md`, `CHANGELOG.md`, `VERIFICATION.md`, `TESTS.md`, `TRACEABILITY.md`, PR body, author packets r1 and r2 | R939-2 | `9590206015ead2cfd2ef955c2f4ef8d8c4e4762c` |

## 5. Executed evidence (this review)

| Run | Result | Receipt |
|---|---|---|
| `validate.py --work <scratch> --jobs 4 --graphs`, with the pinned GoogleTest 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3 | rc 0, 28/28 | `receipts/validate-out.txt`, `receipts/validate-gates.json` |
| Its plant campaign | 512 CAUGHT / 0 ESCAPED / 0 ERROR | `receipts/mutation-summary.txt`, `receipts/mutation-key-plants.json` |
| Its coverage step | 100 % lines and branches after exclusions | `receipts/coverage.log` |
| `baremetal.py --jobs 2` | rc 0, Debug and Release; Release byte-identical to the author's | `receipts/rv32-results.json`, `receipts/rv32.out` |
| `probes/a22_derive.c`: exhaustive 2^32 scan, then the real core | one zero-mixing sample, `0xDE81995D` | `receipts/a22_derive.txt` |
| Seven reviewer plants (`probes/add_probe_plants.py`, on a disposable copy of the tree) | 6 CAUGHT, 1 ESCAPED (S2) | `receipts/probe-mutation.log` |
| `git merge-tree --write-tree` of the head into `dev-linux` (`9e1cd60f`) and into `main` | both give `4064709b`, the head's own tree | `receipts/merge-trees.txt` |
| Hosted check runs at the head (read only) | `bare-metal` success (2); `quality` one success and one in progress; combined status pending at read time | `receipts/hosted-check-runs.txt` |
| Restore check | HEAD, tree and index tree are `4064709b`; worktree and index clean; no gitlinks in this repository; only my own ignored `scripts/__pycache__` was present, and I removed it | `receipts/restore-check.txt` |

Toolchain identities are in `receipts/toolchain.txt`. The host's own GoogleTest 1.18.0 and its missing `clang-18` made the first validate attempt fail at setup. That attempt was discarded, and only the pinned-toolchain run counts.

## 6. Real limits

- The IEEE 1722.1-2021 and Milan v1.2 texts were not available. Clause checks rely on the wording quoted in the issue and the PR.
- No manager source bank runs at this head, and none is claimed. Source-head execution evidence is the author's receipts plus this review's own runs above.
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.
- My validate run used the host's Mermaid renderer (11.16.0), which may not be the CI version.
- Hosted checks were only read, and were not complete at read time. The manager owns hosted and act acceptance.
- The milan-fpga parent commit `4f6ee193` named in the author's note belongs to the parent PR and was not reviewed here.

## 7. Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base `a795471c0abc4e38f7e5146b4e539dd607b6f501`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`), with the builder and native banks, and link the receipts on the PR.
- Hosted and act acceptance at the exact head. `quality` was still in progress when read.
- Carry R1, R3 and R4 to the residue checklist.
- A second independent positive review is still required before merge.

## 8. R940-1 findings at this head

R940-1 (POSITIVE at `5e6ab995`) recorded one item, read only after sections 1 to 7 above were written.

| ID | R940-1 severity | Status at `95902060` | Evidence |
|---|---|---|---|
| R940-01 | RESIDUE (Docs) | **RETAINED** | It covers the same defect as R939-1 R1: `receipts/stack` in milan-fpga@6682d3c0 `review-evidence/adpseed-r1/author/REVIEW-READY.md:3`, where the files sit directly under `author/receipts/`. That frozen round-1 note is unchanged, and this PR does not carry it. The verdict and the lens states do not change. The manager carries one residue entry for R1 and R940-01 together. |

No other R940-1 finding exists, so nothing else needs to be resolved or retained.

R939-2 FINISHED
