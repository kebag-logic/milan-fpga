[R630] NEGATIVE - exact head 0868387deab21bd0db414424f306c7ea62498e29

# R630-2 internal independent review: issue #24 / PR #25

- Repository: kebag-logic/tsn-c-stack, PR #25 (`acmp-da-fresh`), closes issue #24 (milan-fpga lane F3b, core half).
- Exact head `0868387deab21bd0db414424f306c7ea62498e29`, tree `6964ccf56a4b217c3807e6d2ac59eda0e61ec43e`. Source base `1ba2735`. Round-2 delta `9ef7bd5..0868387`.
- Fabric reference: milan-fpga dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, processor gitlink `2ad2f845dd583f8310075fa2380cb60a04fd091a`, `hdl/acmp/KL_acmp_talker.sv`.
- Reconstruction order:
  1. CONTRIBUTING, README and docs.
  2. Issue #24: body, assignment 6126061221, STOP 6126278688, ruling 6126295947, REVIEW READY 6126652895, round-2 instruction 6127660189, REVIEW READY 6128015351.
  3. Requirement and port authorities (REQUIREMENTS ACMP-11, PORTING "ACMP DA freshness", ENTITY_YAML).
  4. `git diff 1ba2735..0868387` and the history.
  5. Executable evidence.
- Prior findings: R630-1 was read after my own pass over the diff. R631-1 was read only after the verdict and ledger below were written. Both are resolved or retained in "Prior findings".

## Verdict

NEGATIVE, on one new MINOR finding (F1).

Every round-2 request is met and reproduces at this head:

- **Per-test escapes.** Each of the 16 `dafresh-*` plants and `x-zero-never-expires` is caught by the complete hosted suite (all 8 binaries) with its named test present. In the campaign, exactly that one test fails. Each plant escapes when only that test is physically deleted. R630-1's two scripts were re-run unchanged, and a companion handles the entity test.
- **Zero interval.** Zero disables the probe term while a Listener still opens the gate. `x-zero-never-expires` is now caught.
- **Range refusal.** `acmp_init` refuses intervals of 2^31 ms or more, with a test.
- **Residue.** R630-1-R1 and R631-D01 are applied word for word.

**Predicate.** It matches the issue's wording of Milan v1.2 4.3.3.1 and the fabric's `fresh_f`/`lsn_reg_f`. The 15000 ms edge reproduces in both: open at 14999 ms, closed at 15000 ms, re-run on the fabric with the pinned 5.050 simulator.

**Targets and size.** Both targets pass. The Release RV32 image grows by 1,072 bytes, under the 2,048-byte ceiling.

**F1.** PORTING promises that an observed expiry clears a stale answer "even with a Listener or an invalid destination", so that an old probe cannot reappear after a later counter wrap. That is part of acceptance 2's wrap survival. No test protects those two paths. Two natural early-exit mutants survive the whole suite, and a harness shows each one re-opens the gate within the documented service contract.

## Findings

### F1 - MINOR - Tests, Robustness - wrap guarantee untested with a Listener or an invalid destination

- **Where:**
  - The claim is at `docs/PORTING.md:342-344`: "Observing expiry clears `answered`, even with a Listener or an invalid destination, so an old probe cannot reappear after a later counter wrap."
  - The code is `src/acmp.c:1258-1265`. The expiry check runs before `p_source` and does not depend on the Listener level, so the head is correct.
  - The only wrap-resurrection assertion is `AcmpFresh.StaleProbe` (`tests/test_acmp.cpp:2289-2298`). It covers neither a Listener nor an invalid destination.
- **Authority:**
  - Issue #24 acceptance 2: "It survives the time counter wrapping."
  - The port contract this PR adds (`docs/PORTING.md:342-350`), including the half-range service contract.
  - CONTRIBUTING: "A protocol change updates its requirement, tests and traceability."
  - Precedent: R630-1-F2, a documented ACMP-11 behaviour with no test and a surviving fail-open mutant, was ruled MINOR and fixed in this round.
- **Evidence:**
  - `receipts/gap-mutants.json` (`scripts/gap_mutants.py`) has two survivors (`suite_rc 0`, all 8 binaries):
    - `g-expiry-skipped-with-listener` skips the expiry check while `listener_registered` is set;
    - `g-expiry-skipped-invalid-da` checks expiry only after the destination reads valid.
  - Each is the shape a natural early return would take: "Listener present, skip freshness" or "invalid destination, return false first".
  - `receipts/wrap-alias-demo.txt` (`scripts/wrap_alias_demo.c`, ASan/UBSan) shows the effect. The service queries every 1e9 ms, inside the documented less-than-2^31 contract.
    - Head: the gate stays shut 2^32+100 ms after the answer, both after a Listener is withdrawn and after the destination becomes valid again.
    - Each mutant: the gate re-opens (`declaring=1`) on its path, with no probe answered in the last 15 s.
- **Impact:** a documented ACMP-11 guarantee and part of acceptance 2 have no failing assertion and no planted defect on two of their three paths.
  - A future early-exit refactor would pass every gate.
  - It would let a talker declare for up to 15 s without a fresh probe or a Listener whenever a Listener withdrawal, or a destination becoming valid again, lands in a wrap-alias window after at least 2^32 ms. That is fail-open, which is what issue #24 exists to prevent.
  - Today's code is correct. Field likelihood is low, but the property is promised and unprotected.
- **Required outcome:**
  - Add assertions that a probe answer, held across at least 2^32 ms of serviced queries, does not reappear after the counter aliases. Cover two cases:
    - a registered Listener, then withdrawn;
    - an invalid destination, then made valid again.
  - Register the two plants above (or equivalents) in `tests/mutations.json`, each with its own named killer.
  - Each plant must be caught by the complete suite and escape when only its killer is removed.
  - Update TESTS/TRACEABILITY.
- **Verification:**
  - `scripts/gap_mutants.py` reports both mutants CAUGHT.
  - `scripts/physical_removal.py` (unchanged) reports `escapes: true` for the two new plants.
  - The mutation campaign stays at 0 escapes.

No other MINOR, MAJOR or BLOCKER finding is open. There is no new RESIDUE.

### Suggestions (non-blocking)

- **S1** (retained from R630-1-S1) - Robustness. `src/acmp.c:122` indexes `a->sources` with the talker_uid read back from the frame.
  - It is safe because only SUCCESS and TALKER_DEST_MAC_FAIL PROBE_TX_RESPONSEs are counted, and they are built after `talker_command` checks `src < n_sources` and the interface. `x-any-probe-status` is still caught.
  - An explicit bound, or carrying the source in `acmp_owed`, would make that local.
- **S2** (retained from R630-1-S2) - RTL, Docs. The fabric stamps the ping when the PROBE_TX is accepted (`KL_acmp_talker.sv:686-689`). The core stamps it when the response is accepted by `ports->send`.
  - `docs/PORTING.md:330-336` now calls this the repository's reading of "answered".
  - It does not name the fabric difference: a later start under backpressure, and no refresh for busy-dropped commands. Naming it would help the milan-fpga half argue `DA_GATE` equivalence.
- **S3** (partly retained from R630-1-S3) - Docs. `acmp_config.da_fresh_ms` is now in the PORTING field table (`docs/PORTING.md:246`).
  - CHANGELOG still has no entry for the new first member of `acmp_config`, which moves every field offset, or for the two new entries.
  - PR #23 recorded its new required callback there.
- **S4** - Tests. `x-no-clock-refresh` still survives and is equivalent at this head. No clock read precedes an accepted PROBE_TX_RESPONSE send in the same entry, so `a->now_read = false;` at `src/acmp.c:123` is defensive only. No action is needed unless a future path reads the clock before that send.

## Lens evidence

### Conformance

**Predicate** (`src/acmp.c:1249-1266`):

- It returns `dest_mac_valid AND (answered-and-younger-than-da_fresh_ms OR listener_registered)` per source.
- Destination validity is read live through the existing `env->source`.
- The interval is `acmp_config.da_fresh_ms`. The core has no mirrored constant.
- The generator supplies 15000, refuses any other value (`scripts/entity_yaml.py:96-103, 233`), and emits it in all four example entities.

**Answers** (`src/acmp.c:113-128`). Only accepted PROBE_TX_RESPONSEs with SUCCESS or TALKER_DEST_MAC_FAIL count. Those are built only for a known source on its configured interface (`src/acmp.c:970-996`). Unknown-ID, incompatible-interface, other talker replies and queued or refused sends do not count. This matches the fabric, which pings regardless of DA validity.

**Listener input** (`src/acmp.c:1236-1247`):

- It is one input with no port calls.
- It is keyed per source and refused on a mismatched interface.
- The level means any registration, including Asking Failed, the same as the fabric's `lsn_reg_f` (`!= SRP_DECL_IGNORE`).

**Init** (`src/acmp.c:1014-1016`). It refuses an interval of 2^31 or more before touching the instance or calling a port. Zero keeps its documented meaning (`docs/PORTING.md:246, 325-327`).

**Other ACMP paths:**

- The diff only adds to `tests/`, and the existing tests are unchanged and green.
- No other response byte changes.
- The single added port call is one `now_ms` read on an accepted PROBE_TX answer. No documented budget covers it.
- `entity_check_acmp` sends no talker command, so the round trip's `source` change has no effect on it.

**STOP conditions:** none applies. ADP, MAAP and the port contract are unchanged apart from the one input.

**Release size:** 35,792 to 36,864 bytes (+1,072), within the ruling. Debug is +1,768, informational (`receipts/rv32-size.txt`). The figures match the author's exactly.

### RTL (fabric equivalence)

- The fabric's `fresh_f` is `pinged && (now - ping_ts) < DAFRESH_MS_P`, mod 2^32 (`KL_acmp_talker.sv:395-398`). It has the same half-open window and wrap arithmetic as the core.
- Its ping commit needs a valid enabled uid and a matching interface, and it ignores DA validity (`KL_acmp_talker.sv:656-690`). That is the same answer set as the core.
- The edge probe was re-run on the pinned 5.050 simulator (identity string checked); see `receipts/fabric-edge-probe.txt`.
  - The stock suite passes 1342/1342.
  - With expiry at exactly ping+15000 ms, it still passes: the gate closes.
  - At ping+14999 ms, the D2 close checks fail: the gate is still open.
- The core is identical: `WindowEdge` closes at 15000 ms, and `WithinWindowAndRefresh` is open at 14999 ms.
- Not compared, because they are outside the issue's scope: the fabric's LEAVEALL2 backoff on a MAAP conflict, its source-disable wipe, and its silent drop of wrong-interface probes. The core keeps INCOMPATIBLE_REQUEST, and neither refreshes the window.

### Robustness

- **Differential run.** R630-1's `dafresh_differential.c`, unchanged, was built against the head `src/acmp.c` with ASan/UBSan: 400 seeds × 20,000 steps, 32,000,000 queries, zero mismatches (`receipts/dafresh-differential.txt`).
- **Re-entry.** Refused and counted for both new entries.
- **Index safety.** See S1.
- **Interval range.** The 2^31 refusal makes the half-range clock contract sufficient for every accepted interval.
  - `g-refusal-after-memset` and `g-no-range-refusal` are caught.
  - `g-zero-refused` is caught by 95 tests: zero must stay valid.
- **Equivalent survivors.** `x-signed-age` is equivalent within the documented interval below 2^31.
- **Open:** F1.

### Tests

- **Campaign.** It is complete with 365/365 caught. Each `dafresh-*` plant and `x-zero-never-expires` fails exactly its one named test (`receipts/mutation-summary.txt`).
- **Escape probe** (`scripts/escape_probe.py`, unchanged; `receipts/escape-probe.json`):
  - 16/16 `dafresh-*` plants escape the complete suite with only their killer excluded.
  - 16/16 killers fail alone with their needles.
  - Extra mutants: `x-zero-never-expires` is CAUGHT (only `AcmpFresh.ZeroWindow`). 7 others are caught. `x-no-clock-refresh` and `x-signed-age` survive and are equivalent.
  - The YAML range plant is caught and escapes when its test is removed. The no-emission and default-zero plants are caught.
- **Physical removal** (`scripts/physical_removal.py`, unchanged; `receipts/physical-removal.json`). For all 16 plants whose killer is in `tests/test_acmp.cpp`, the test is physically deleted, the plant applied and the full suite passes. That set is the 15 `dafresh-*` plants other than the entity plant, plus `x-zero-never-expires`.
- **Entity plant** (`scripts/entity_removal.py`; `receipts/entity-removal.json`). The unchanged script cannot edit `tests/test_entity.cpp`, so this companion covers `dafresh-generated-window`:
  - unplanted control: passes, 418 test instances over 8 binaries;
  - planted: fails only `EntityYaml.DaFreshRoundTrip` with its needle;
  - planted with that test deleted: passes, 417 instances.
- **Round trip.** `entity_check_dafresh` (`examples/entity_roundtrip.c:225-246`) now checks only three things: the generated value in all four entities (code 80), init (81), and one freshness-true path (85).
- **RV32 execution** (`scripts/rv32_probe.py`; `receipts/rv32-probe.json`). Four plants each fail the RV32 gate through the QEMU exit code: generated window 15001, answer not recorded, gate always closed, window always stale. The unplanted control passes.
- **Coverage.** `src/acmp.c` is 792/792 lines and 392/392 branches, equal to the ratchet (`receipts/coverage-summary.txt`).
- **Open:** F1.

### Docs

- **Acceptance 5.** `docs/PORTING.md:310-353` states the predicate and cites Milan v1.2 4.3.3.1, which the acceptance allows as "the README or the ACMP documentation". README.md itself does not state it.
- **R630-1-R1 residue.** Applied verbatim at `docs/PORTING.md:336`.
- **Zero and range.** Documented at `docs/PORTING.md:246, 325-327`.
- **R631-D01.** `docs/ENTITY_YAML.md:139-148` lists four plants and their round-trip scope.
- **Requirements and indexes.** REQUIREMENTS, requirements.json, TRACEABILITY and TESTS carry ACMP-11 with correct line anchors. The traceability and inventory gates pass.
- **Plant counts.** VERIFICATION's "361 core plants and four generated configuration plants" matches the 365-plant campaign.
- **PR body.** Every figure in the round-2 section reproduces: 418 to 417, 365 plants, 792/792 and 392/392, +1,072/+1,768 bytes, and 28 gates (hosted).
- **Docs lens.** No Docs defect is open. F1 is a missing test for a true documented claim, not a wrong claim.

## Executed evidence (this reviewer, local, exact head)

- **`scripts/validate.py --jobs 16 --graphs`:** 27 of 28 entries returned rc 0 (`receipts/validation-gates.json`, `receipts/validation-summary.txt`). These include:
  - entity golden and controls, boundary self-test, needles, assertion templates, the dependency pin;
  - comments, the conditional matrix, port contracts, the ACMP cache check, registration controls, licence;
  - traceability, the test inventory, coverage controls, privacy and its self-test;
  - the GCC build and tests (8/8) with coverage, and the Clang sanitizer build and tests (8/8);
  - mutation (365/365) and its controls, and graphs.
- **`static-analysis` returned rc 1 locally.** The cause is the host analyzer (LLVM 23.1.1), which reports `optin.performance.Padding` on the unchanged `struct acmp_sink`. Base `1ba2735` gives the identical diagnostic set (`receipts/static-analysis-head-vs-base.txt`). The exact-head hosted job reports `static-analysis: rc 0`. This is an environment difference, not a PR defect.
- **`scripts/baremetal.py`:** Debug and Release at head and base, rc 0, smoke checks pass, no unresolved symbols (`receipts/rv32-head-results.json`, `receipts/rv32-base-results.json`).
- **Hosted exact-head runs:** 38275432785 (pull_request) and 38275425425 (push). Both `quality` and `bare-metal` jobs executed and succeeded, and every step succeeded (`receipts/hosted-runs-steps.txt`).
  - The PR run's quality log lists all 28 gates at rc 0 (`receipts/hosted-pr-run-38275432785-gates.txt`).
  - Its RV32 log shows Debug and Release rc 0 (`receipts/hosted-pr-run-38275432785-rv32.txt`).
  - Hosted and act acceptance remain the manager's.
- **Clone integrity after all probes:** every probe ran in disposable copies (`receipts/clone-integrity.txt`).
  - HEAD and tree are exact, and the index equals the tree.
  - No worktree blob or mode differs, and no untracked or ignored files remain.
  - There are no gitlinks at this head.

## Reviewer-owned ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` (p_send hook, `acmp_init` range, `acmp_listener_registered`, `acmp_declaring`), `include/acmp.h`, issue acceptance 1-2 and 5, assignment, ruling and round-2 instruction, ACMP-11, Milan 4.3.3.1 per the issue, generator, RV32 size delta | R630-2 | 0868387deab21bd0db414424f306c7ea62498e29 |
| RTL | CLEAN | `KL_acmp_talker.sv` (`fresh_f`, `lsn_reg_f`, ping commit) at processor `2ad2f845` from milan-fpga `c6bd08c6`; fabric suite plus the 14999/15000 edge probe on the pinned 5.050 simulator | R630-2 | 0868387deab21bd0db414424f306c7ea62498e29 |
| Robustness | UNCLEAN (F1) | index bounds, re-entry, wrap and wrap aliasing, owed queue and backpressure, zero and 2^31 interval, sanitized 32M-query differential, gap mutants, wrap-alias harness | R630-2 | 0868387deab21bd0db414424f306c7ea62498e29 |
| Tests | UNCLEAN (F1) | `tests/test_acmp.cpp` AcmpFresh, `tests/test_entity.cpp`, `examples/entity_roundtrip.c`, `tests/mutations.json`, campaign 365/365, unchanged escape and physical-removal scripts, entity removal, RV32 plants, gap mutants, coverage | R630-2 | 0868387deab21bd0db414424f306c7ea62498e29 |
| Docs | CLEAN | `docs/PORTING.md`, REQUIREMENTS, requirements.json, TRACEABILITY, TESTS, ENTITY_YAML, VERIFICATION, README, CHANGELOG, PR body, REVIEW READY | R630-2 | 0868387deab21bd0db414424f306c7ea62498e29 |

## Prior findings

Every earlier public finding on this PR, checked at this head:

| finding | origin | status at 0868387 | evidence |
|---|---|---|---|
| R630-1-F1 (MAJOR): five plants did not escape without their named test | R630-1 | RESOLVED | See below. |
| R630-1-F2 (MINOR): zero interval untested; `x-zero-never-expires` survived | R630-1 | RESOLVED | See below. |
| R630-1-R1 (RESIDUE): attribution of the answer acceptance point | R630-1 | RESOLVED | Exact text at `docs/PORTING.md:336`. |
| R630-1-S1: explicit source bound in `p_send` | R630-1 | RETAINED as S1 | `src/acmp.c:122` is unchanged. |
| R630-1-S2: state the fabric timestamp difference | R630-1 | RETAINED as S2 | PORTING calls it a local reading but does not name the fabric difference. |
| R630-1-S3: PORTING field table and CHANGELOG | R630-1 | PARTLY RESOLVED; CHANGELOG part RETAINED as S3 | The field is at `docs/PORTING.md:246`; CHANGELOG is unchanged. |
| R630-1-S4: round trip used `delay` as its clock | R630-1 | RESOLVED | It now has a dedicated `now` field and `fresh_clock` (`examples/entity_roundtrip.c:21, 220-223`). |
| R631-D01 (RESIDUE): the ENTITY_YAML plant table read as exhaustive with three rows | R631-1 | RESOLVED, per the manager's round-2 instruction | `docs/ENTITY_YAML.md:139-148` lists all four configuration plants: "four configuration defects", four rows, "All four plants still compile". |

**R630-1-F1 evidence:**

- `entity_check_dafresh` (`examples/entity_roundtrip.c:225-246`) is narrowed to the generated value plus one freshness-true path.
- The campaign fails exactly the named test for every plant.
- `receipts/escape-probe.json`: 16/16 plants escape without their killer.
- `receipts/physical-removal.json`: 16/16 escape with their killer physically deleted.
- `receipts/entity-removal.json`: 418 to 417 instances.
- The PR body now records the corrected claim.

**R630-1-F2 evidence:**

- `AcmpFresh.ZeroWindow` (`tests/test_acmp.cpp:2365-2377`) and the registered `x-zero-never-expires` are caught by that test alone and escape when it is removed.
- `AcmpFresh.WindowRange` (`tests/test_acmp.cpp:2380-2393`) and `dafresh-half-range` cover the 2^31 refusal.
- The refusal is at `src/acmp.c:1015`.

R631-1 made no other finding: it reported all five lenses CLEAN. Its statement that observed expiry clears the flag "even when a Listener or invalid destination would hide it" is true of the code. F1 concerns only the missing test protection for that property.

## Real limits

- The author's linked evidence (`review-evidence/tsn24-r1` at `dd34e9598bf038a56766dfcd9eef46bf62ac8b95`) could not be read. The contents API returns "No commit found for the ref", the commits API returns 422, and no tsn24 evidence branch exists on the remote.
  - Source-head execution evidence here is therefore this reviewer's local runs plus the exact-head hosted jobs.
  - This reviewer makes no claim about the author's receipts.
- The Milan v1.2 text was not available to this reviewer. The predicate is judged against the issue's frozen wording and the fabric implementation.
- The local toolchains differ from the hosted ones:
  - GCC is 16.2 and the sanitizer Clang is 23.1. The pinned Clang 18 copy has no sanitizer runtime and was used for the lexing gates.
  - The RV32 compiler is the distribution `riscv64-elf-gcc` 16.2. Its image sizes nonetheless match the author's to the byte.
  - The hosted job covers the distribution toolchains.
- No manager source bank exists at this head, and none is claimed or inferred. The current-dev merge candidate (source base `1ba2735`, live dev `c6bd08c6`) is not validated here.
- Physical calibration was NOT RUN. Neither target establishes board or transport behaviour, and the RV32 smoke runs on QEMU only.

## Pending manager duties

- Carry F1 back to the author. Carry S1-S4 at the manager's discretion.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts. Own hosted and act acceptance.
- Before merge, two independent positive reviews are needed at the final head.

## Packet

Scripts and receipts are listed in `MANIFEST.sha256`.

- Unchanged R630-1 copies, checked against the R630-1 manifest hashes: `physical_removal.py`, `escape_probe.py`, `fabric_edge_probe.sh`, `dafresh_differential.c`.
- New in this round: `entity_removal.py`, `gap_mutants.py`, `rv32_probe.py`, `wrap_alias_demo.c`.

In receipts, host paths are written as `<packet>`, `<clone>`, `<tools>`, `<home>` and `<data>`.

R630-2 FINISHED
