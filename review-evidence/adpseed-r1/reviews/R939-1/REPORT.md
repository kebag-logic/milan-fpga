[R939] NEGATIVE - exact head 5e6ab995b0c840bb318907642b14d45e8dd0efea

# Independent review R939-1: kebag-logic/tsn-c-stack PR #40 (Closes #39)

- Exact head `5e6ab995b0c840bb318907642b14d45e8dd0efea`, tree `b831ac0b6f409a41c0c39ff2e2f0b01551b36bfe`, one commit on `main` `a795471c0abc4e38f7e5146b4e539dd607b6f501`.
- Reviewer role: internal independent reviewer, cleared context, own detached clone.
- Verdict: **NEGATIVE**. There are two open MINOR findings (F1, F2), one SUGGESTION (S1) and two RESIDUE items (R1, R2).
- The core change works. Each transition out of DOWN takes exactly one sample and no other input takes one. The draws are uniform and host-distinct. The sequence has its full length. All 28 gates pass at this head, and 510 of 510 plants are caught.
- F1: the suite pins an end-around carry and cites IEEE 1722.1-2021 6.2.4.2.2 for it. That clause asks for the sum's least significant octets, and the literal sum is planted as a defect.
- F2: no test checks that the ENTITY_DISCOVER draw takes no sample. A plant that samples there escapes the whole suite.

## 1. What was reconstructed, in order

1. `CONTRIBUTING.md` (there is no `AGENTS.md` in this repository), `README.md`, `docs/CODING_STANDARD.md` (comments allow only SPDX lines, requirement IDs and short clause references), `docs/VERIFICATION.md`, `docs/COVERAGE.md`, `docs/DEVIATIONS.md` and `docs/PORTING.md`.
2. Issue #39 body: the frozen scope and acceptance. The issue has no comments.
   - Scope: one fresh sample through the seed port at each transition out of DOWN (startup and each qualified LINK_UP), mixed with the MAC address, the entity ID and the interface. No sample at a duplicate or disabled LINK_UP, or at any other draw.
   - Out of scope: the delay ranges, the advertise timer and any other ADP rule.
   - Acceptance: (1) tests count the samples per rise, duplicate, disabled, other interface and startup; (2) over boots alike but for the sample at a LINK_UP, the first delays are distinct and uniform; (3) one planted defect per rule, each caught, with the Linux and RV32 targets green.
3. The linked public scope decision: the ruling in kebag-logic/milan-fpga#970 (comment 7174054394, 2026-11-25), item 2. The draw change is accepted as its own change, and the draw mixes a fresh sample, the entity ID and the interface.
4. Requirement ADP-02 (`docs/requirements.json`, `docs/REQUIREMENTS.md:21`) and the port contract (`docs/PORTING.md:175-177`).
5. `git diff a795471c..5e6ab995` (12 files) and the history: one commit whose parent is `main`.
6. Public evidence: kebag-logic/milan-fpga@6682d3c0 `review-evidence/adpseed-r1/author`. All 8 files match their published SHA-256 values (`receipts/author-evidence-sha256-check.txt`).
7. PR comments: two review-start notices, no other evidence comments. The PR has no reviews and no review comments.

**Prior public review findings at this head:** none. There are no reviews, no review comments and no findings comments on PR #40 or issue #39, so nothing has to be resolved or retained.

## 2. Findings

### F1 - MINOR - Conformance, Tests, Docs - the end-around carry is pinned and attributed to IEEE 1722.1-2021 6.2.4.2.2

- **Where:**
  - `src/adp.c:105-106`: `sum = (uint32_t)e->mac + sample; sum += sum < sample;`
  - `tests/test_adp.cpp:607-612`: the A27 assertion "A27 the sum carries end around (6.2.4.2.2)"
  - `tests/test_adp.cpp:541-546`: A22's constant `0xDE81995C` mixes to zero only with the carry.
  - `tests/mutations.json:6893`: the plant `adp-seed-carry-dropped`
  - `docs/REQUIREMENTS.md:21` and `docs/requirements.json:22` (ADP-02 "the sum of the MAC address and the local clock"), and `CHANGELOG.md:5` ("with the sum of the MAC address and the local clock (IEEE 1722.1-2021 6.2.4.2.2)")
- **Authority:** IEEE 1722.1-2021 6.2.4.2.2, as quoted in the PR: the generator is "seeded using the least significant (most rapidly varying) octets of the sum of the requestor's IEEE 802 MAC address and the local real time clock".
  - The least significant 32 bits of that sum are `(mac mod 2^32 + clock mod 2^32) mod 2^32`. The carry out of bit 31 goes into the fifth octet. It is not folded back into bit 0.
  - An end-around carry gives a ones'-complement sum, which differs from the clause's value by one whenever the addition overflows. It is also not injective in the sample: samples `0` and `2^32 - 1` give the same seed.
- **Evidence:** the probe `probe-plain-modular-sum` drops the carry, giving the clause's literal least significant octets. It is caught by `AdpCore.A27EverySeedTermIsMixedIn` ("A27 the sum carries end around (6.2.4.2.2)") and by `AdpCore.A22GeneratorNeverStuckAtZero` (`receipts/probe-results.json`, `receipts/probe-campaign.log`).
- **Impact:**
  - No measurable effect on randomness or host-distinctness: the probes in section 3 pass either way.
  - The clause claim is wrong. The suite enforces a local choice in the clause's name, and the literal reading of the clause is graded as a planted defect. That misleads the traceability and any later correction.
- **Required outcome (either one):**
  - (a) Seed with the plain modular sum. Restate A27's sum assertion so it pins the modular wrap (for example `mac = 0xFFFFFFFF, sample = 5` against `mac = 0, sample = 4`). Re-derive A22's zero-mixing constant. Restate the carry plant as "carry added end around", caught.
  - (b) Keep the end-around carry as a documented local choice with its reason: no 6.2.4.2.2 attribution in the A27 message, and ADP-02, the change log and the deviation record saying "ones'-complement sum, a local choice beyond IEEE 1722.1-2021 6.2.4.2.2".
- **Verification:** under (a), `probe-plain-modular-sum` passes every test and an "end-around carry added" plant is caught by A27. Under (b), no test message cites 6.2.4.2.2 for the carry, and the requirement or deviation text records the choice. The 510-plant campaign stays 0 escaped.

### F2 - MINOR - Tests - no test asserts that the ENTITY_DISCOVER draw takes no sample

- **Where:**
  - `tests/test_adp.cpp:616-627` (A28 `core_fresh_sample`): it checks the TMR_ADVERTISE and GM_CHANGE draws only, and never delivers an ENTITY_DISCOVER.
  - `tests/mutations.json:6758` (`adp-every-draw-reseeded`): it plants inside `enter_delay`, so A28 catches it through the other draws.
  - `docs/PORTING.md:176` (contract "and at no other draw").
  - The PR body says A28 holds "none at any other draw" and that "every other draw (DISCOVER, TMR_ADVERTISE, GM_CHANGE) take[s] no sample".
- **Authority:**
  - Issue #39 scope: "none at a duplicate or disabled LINK_UP or any other draw".
  - Acceptance 3: "A planted defect per rule, each caught".
  - The published port contract, `docs/PORTING.md:176`.
- **Evidence:** the probe `probe-discover-draw-sampled` changes `adp_rx`'s draw to `leave_down`, which takes a sample at every answered ENTITY_DISCOVER. It builds, and every test binary passes ("ESCAPED (no test fails)", `receipts/probe-campaign.log`). The same probe at the GM_CHANGE draw and at the TMR_ADVERTISE draw is caught by A28. The behaviour at head is correct: the 2,000,000-step walk in section 3 sees no sample at any DISCOVER.
- **Impact:** ENTITY_DISCOVER is the one draw that remote hosts trigger. A regression that samples the clock there would pass the suite and the plant campaign, and would break the published port contract that integrators may rely on.
- **Required outcome:**
  - A28 (or a new assertion) delivers an ENTITY_DISCOVER in WAITING, with a matching and a zero target, and asserts that the seed count is unchanged while the draw is made.
  - Add a planted defect at the `adp_rx` draw site, like `probe-discover-draw-sampled`, killed by that assertion's message.
- **Verification:** the new plant is CAUGHT in `scripts/mutation.py`, the campaign reports 0 escaped, and the test inventory and traceability are regenerated.

### S1 - SUGGESTION - Tests - the interface term is pinned only by interfaces 0 and 1

- **Where:** `tests/test_adp.cpp:593-594`.
- **Evidence:** the probe `probe-interface-low-bit-only` keeps only `interface & 1` in the mix. No test fails.
- **Impact:** with one shared `adp_entity` (and so one MAC) across interfaces, interfaces 0 and 2 sampled together would draw alike, and no test would notice. Today's configurations use one or two interfaces, so this is a test-strength gap, not a defect.
- **Suggested:** compare several interfaces pairwise in A27, for example 0, 1, 2 and 255.

### R1 - RESIDUE - Docs (author evidence note) - wrong receipt path and an overclaim

- **Where:** milan-fpga@6682d3c0 `review-evidence/adpseed-r1/author/REVIEW-READY.md`.
- **Defect:** it says "receipts/stack holds validate.py, RV32, plants, coverage and the distribution test". The packet has `author/receipts/` with no `stack` directory and no separate distribution-test receipt: A25, A26 and A31 run inside the gcc-test gate.
- **Exact fix:** "receipts/ holds the validate.py, dev-linux merge, RV32, plant and coverage receipts; the distribution tests A25, A26 and A31 run inside the gcc-test gate of validate.py."

### R2 - RESIDUE - Docs - stale checklist wording for the ADP seed port

- **Where:** `docs/PORTING.md:144`. The ADP row of the callback checklist still says "entropy seed". Line 175 now defines the port as the least significant 32 bits of the local clock, sampled at each transition out of DOWN.
- **Exact fix:** in that row, replace "entropy seed" with "a local clock sample at each transition out of DOWN".
- Optionally, `docs/DEVIATIONS.md:13` (DEV-04) "Entropy comes from the integrator" could read "The integrator supplies a clock sample (ADP) or entropy (ACMP)".

## 3. Lens evidence

### Conformance (UNCLEAN: F1)

The standards documents were not available in the review environment. The clause checks below rely on the clause wording quoted publicly in issue #39 and the PR body.

- **Milan v1.2 5.6.3.5.2 (startup draw, 0 to 2 s) and 5.6.3.5.3 (LINK_UP from DOWN, 0 to 4 s):** both call sites use `leave_down` with the unchanged draw kinds (`src/adp.c:257`, `src/adp.c:275`).
  - `draw_ms`, `rng_next` (13, 17, 5), `ADP_DELAY_*` and `ADP_ADVERTISE_MS` are unchanged: no other ADP behaviour changes.
  - In a 2,000,000-step random walk on two interfaces (`scripts/seed_walk.c`, `receipts/seed_walk_head.log`), every draw stays in its kind's range. The startup kind appears only at an enable that leaves DOWN, and the timer gets the drawn value.
- **IEEE 1722.1-2021 6.2.4.2.2, uniform:** with 65,536 draws per case, all independent of the suite's parameters, every case passes at the 1 % level. Expected counts follow the unchanged `draw_ms` mapping.
  - One host over consecutive samples, link-up draw: chi-square 18.3 (16 bins) and 80.1 (64 bins). Startup draw: 17.9 and 79.2.
  - Neighbouring hosts sampled together: 8.4 and 58.2.
  - Hosts that differ only in the entity ID's high word: 8.1 to 8.5.
  - Boots alike but for the sample at a later LINK_UP: 14.8 and 47.1, with all 4,001 values reached. The first 4,096 give 2,555 distinct values, where about 2,565 are expected.
  - Main's core fails all of these: for example, one host's link-up draws take a single value over 65,536 samples, and 256 interfaces draw alike (`receipts/seed_walk_base.log`).
- **IEEE 1722.1-2021 6.2.4.2.2, host-distinct:** A26 and A27 pass, and the probes above agree. 256 interfaces of one host sampled together give 251 of 256 distinct link-up draws, the number expected by chance over 4,001 values.
- **IEEE 1722.1-2021 6.2.4.2.2, maximum length:** A29 computes the order of the step's matrix over GF(2): `M^(2^32-1) = I`, and it is not reached at `(2^32-1)/p` for p = 3, 5, 17, 257 and 65537. That is a correct proof that the length is exactly 2^32 - 1. The plants `adp-sequence-not-maximal`, `adp-sequence-a-third` and `adp-step-not-linear` are caught.
- **IEEE 1722.1-2021 6.2.4.2.2, MAC plus clock seeding:** the MAC address and the sample are summed, but with an end-around carry the clause does not state (F1).
- **The milan-fpga#970 ruling, item 2:** a fresh sample, the entity ID (both words) and the interface are mixed in at each transition out of DOWN.

### RTL (CLEAN)

- The delta has no HDL. This lens was applied to the freestanding RV32 target, which is the hardware-facing artifact.
- `scripts/baremetal.py`: rc 0 for Debug and Release (`receipts/rv32.log`).
  - Core imports stay within the allowed set (`__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`, plus `port_assert_failed` in Debug), and there are no unresolved final symbols.
  - The smoke test covers ADP discovery and backpressure.
- The Release disassembly of `adp.c.obj` shows that `mix()` compiles to shifts, adds and xors on rv32i: no multiply or library call. The one `__mulsi3` inside the inlined `leave_down` is the existing `draw_ms` product.
- The ELF hashes differ from the author's, as expected for a different build path. Symbol imports and smoke results agree.
- The hosted `bare-metal` jobs at this head ran to completion with success; they were not skipped (`receipts/hosted-check-runs.json`).

### Robustness (CLEAN)

- **Random walk** (`receipts/seed_walk_head.log`): 2,000,000 random inputs across enable, disable, link up and down, timer expiry, GM change, DISCOVER (own and zero target) and poll, with sends refused one time in eight.
  - The machine left DOWN 125,329 times and took exactly 125,329 samples. Every step had a sample exactly when it left DOWN.
  - The other interface was never disturbed, and no draw ran with the generator at zero.
- **Zero state:** after `adp_init` the generator is 0, but no draw path is reachable before `leave_down`. Every `enter_delay` caller outside `leave_down` requires WAITING, and the walk confirms it. A seed that mixes to zero becomes 1 (A22, plant `seed-left-at-zero` caught).
- **Re-entry:** the seed call is flagged `port_active` (plant `adp-seed-port-unflagged` caught under the release arm). Sanitizer builds pass (`receipts/clang-sanitizers-test.log`).

### Tests (UNCLEAN: F1, F2)

- **Clean run** of `validate.py --jobs 16 --graphs` at this head with the repository's pinned toolchain: rc 0 on all 28 gates (`receipts/validate.log`, `receipts/validate.rc`).
  - `mutation`: 510 CAUGHT, 0 escaped, 0 error (`receipts/mutation.log`). All 21 new plants are CAUGHT, including the four A30/A31 plants (`adp-later-rise-not-sampled`, `adp-duplicate-up-sampled`, `adp-disabled-up-sampled`, `adp-later-sample-ignored`), and so are the restated `seed-left-at-zero` and `link-up-draws-startup-kind`.
  - The set of plant names and their statuses is identical to the author's receipt.
- **A30** counts one sample per qualified rise over three rises, none for a duplicate, none for a disabled LINK_UP, one for the other interface's rise and one for the startup draw. This meets acceptance 1. My probes add that an enable with the link down, a disable, an unsampled other-interface rise, and sampling at the GM_CHANGE or TMR_ADVERTISE draw are all caught.
- **A31** covers 4,096 boots alike but for the sample at a later LINK_UP, in both startup modes: at least 2,400 distinct first delays and a uniform chi-square. This meets acceptance 2, together with A25 for the first LINK_UP after boot.
  - The probes `first-rise-sample-quantized` and `later-rise-sample-quantized` are caught, by A25/A27 and by A28/A31.
- **Against main's core:** under the head's tests it fails A22, A25, A26, A27, A28, A30, A31, `MockedPortOrder` and `AdpReentry.AdvertiseInlineExpiry`, and passes A29. That matches the PR's table.
- **Open:** sampling at the ENTITY_DISCOVER draw escapes the suite (F2). The end-around carry is pinned under a clause it does not come from (F1). The interface term is tested only at 0 against 1 (S1).

### Docs (UNCLEAN: F1)

- ADP-02 in `requirements.json` and `REQUIREMENTS.md` agree, and the traceability and test-inventory gates pass, so the generated `TRACEABILITY.md` and `TESTS.md` are current.
- `VERIFICATION.md` states 506 core plants plus 4 generated, which matches the 510 measured.
- The comment gate passes. The new source comments are clause references only (`src/adp.c:97-98`, `:257`, `:275`). The delta adds no bench lane label, lane name, review round, reviewer ID or comment ID in source, tests, docs or the change log, so there is no new comment-rule residue.
- The privacy gate passes, and the PR body and docs contain no private names.
- `PORTING.md:175-177` states the new seed contract accurately. Its checklist row is stale (R2), and the author's evidence note is wrong (R1).
- **Coverage:** lines and branches are 100 % after the existing exclusions; raw counts are `adp.c` 216/218 lines and 95/102 branches (`receipts/coverage.log`), identical to the author's. `tests/coverage.ratchet` is unchanged and the gate compares fractions, so it is not lowered.
- **Merges:** merging the head into `dev-linux` (9e1cd60f) and into `main` both give the head's own tree b831ac0b (`receipts/merge-trees.txt`). The source validation therefore applies unchanged to the dev-linux merge.

## 4. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `src/adp.c` delta; ADP-02; the issue #39 scope; the milan-fpga#970 ruling; Milan v1.2 5.6.3.5.2 and 5.6.3.5.3; IEEE 1722.1-2021 6.2.4.2.2 (quoted wording); `seed_walk` statistics; A29 proof; probes | R939-1 | 5e6ab995b0c840bb318907642b14d45e8dd0efea |
| RTL | CLEAN | RV32 Debug and Release builds, imports, smoke, `adp.c.obj` disassembly; hosted bare-metal check runs | R939-1 | 5e6ab995b0c840bb318907642b14d45e8dd0efea |
| Robustness | CLEAN | 2,000,000-step two-interface walk; zero-state reachability; re-entry flag plant; sanitizer suite | R939-1 | 5e6ab995b0c840bb318907642b14d45e8dd0efea |
| Tests | UNCLEAN (F1, F2) | A22, A25-A31, MockedPortOrder; 510-plant campaign; 14 reviewer probes including main's core under the head's tests; acceptance 1-3 | R939-1 | 5e6ab995b0c840bb318907642b14d45e8dd0efea |
| Docs | UNCLEAN (F1) | REQUIREMENTS, requirements.json, PORTING, VERIFICATION, CHANGELOG, DEVIATIONS, COVERAGE; generated TESTS and TRACEABILITY; comment and privacy gates; PR body; author evidence note | R939-1 | 5e6ab995b0c840bb318907642b14d45e8dd0efea |

## 5. Real limits

- The standards documents were not available in the review environment. The clause checks use the clause wording quoted in issue #39 and the PR body. That wording matches the clause structure cited by ADP-02.
- No manager source bank ran at this exact head, and I claim none. The source execution evidence here is the author's receipts plus my own focused reruns.
- Physical calibration NOT RUN. Nothing ran on hardware, and field skips are not hardware proof.
- My first validation attempt used the host's default toolchain, which the gates refuse by design. A second attempt overlapped another of my runs in one work directory. Both are discarded and not published. The published `receipts/validate.log` comes from a single uncontested run in a fresh directory.
- The hosted check runs (2 × quality, 2 × bare-metal, all completed with success) were only inspected. Hosted and act acceptance belong to the manager.
- Receipts replace host locations with `<clone>`, `<packet>`, `<tools>` and `<home>`.
- The clone was restored and verified after the probes: 100 tracked files, 0 blob or mode mismatches, the index equals the HEAD tree, 0 untracked or modified entries, and no submodule gitlinks in this repository (`receipts/clone-integrity.txt`). Probes ran only on a disposable export, whose `src/adp.c` was restored to the head blob's SHA-256.

## 6. Pending manager duties

- Build and validate the current-dev merge candidate (source base a795471c0abc4e38f7e5146b4e539dd607b6f501, live dev e275d7950ef3385753e6a15d2e191ba855b171ed) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Own hosted and act acceptance at the final head.
- Carry R1 and R2 to the residue checklist.
- Obtain the second independent review. Re-review after F1 and F2 are resolved at a new head.

## 7. Reproduction

- Gates: `. scripts/pinned-env.sh` (set `TSN_TOOLS` first), then `python3 scripts/validate.py --work <dir> --jobs 16 --graphs` and `python3 scripts/baremetal.py --work <dir> --jobs 4`.
- Walk and statistics: `cc -std=c11 -O1 -DNDEBUG -I<repo>/include scripts/seed_walk.c <repo>/src/adp.c -o seed_walk && ./seed_walk 2000000`.
- Probes: `python3 -I scripts/make_probes.py <export> probes.json <main-adp.c>`, then `python3 -I scripts/run_probes.py <export> probes.json <build> probe-results.json 12`.

R939-1 FINISHED
