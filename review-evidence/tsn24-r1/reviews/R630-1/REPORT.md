[R630] NEGATIVE - exact head 9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1

# R630-1 internal independent review: issue #24 / PR #25

- Repository: kebag-logic/tsn-c-stack, PR #25 (`acmp-da-fresh`), closes issue #24 (milan-fpga lane F3b, core half).
- Exact head `9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1`, tree `dcf00056e872f60856d46444b9871ca598fd4e50`; source base `1ba2735`.
- Fabric reference: milan-fpga dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, processor gitlink `2ad2f845dd583f8310075fa2380cb60a04fd091a`, `hdl/acmp/KL_acmp_talker.sv`.
- Reconstruction order: CONTRIBUTING, README and docs; issue body and comments (assignment 6126061221, STOP 6126278688, ruling 6126295947, REVIEW READY 6126652895); linked requirement and port authorities; `git diff 1ba2735..9ef7bd5` and history; then executable evidence.
- When this review was written, the PR had no earlier review findings: only the two review-start comments were present. Nothing needs resolving or retaining.

## Verdict

NEGATIVE. The predicate is correct. It matches the issue's wording of Milan v1.2 4.3.3.1 and the fabric processor's `fresh_f`/`lsn_reg_f`, including the half-open 15000 ms edge and clock wrap. Both targets build and pass, and all repository gates pass, with the one environment difference noted below. The Release image grows by 1,304 bytes, which is within the 2,048-byte ruling.

Frozen acceptance 4 is not met for 5 of the 15 registered plants. The PR's statement that every new test has an individual removal escape does not reproduce (F1). One documented zero-interval behaviour has no test, and a fail-open mutant of it survives (F2).

## Findings

### F1 - MAJOR - Tests, Docs - five plants do not escape without their named test

- **Where:** `tests/mutations.json` plants `dafresh-unanswered-clock` (killer `AcmpFresh.NoProbe`, `tests/test_acmp.cpp:2283`), `dafresh-inclusive-edge` (`AcmpFresh.WindowEdge`, `tests/test_acmp.cpp:2301`), `dafresh-listener-needs-probe` (`AcmpFresh.ListenerWithoutProbe`), `dafresh-ignore-address` (`AcmpFresh.InvalidAddress`) and `dafresh-absolute-clock` (`AcmpFresh.ClockWrap`).
  - The overlapping checks are in `examples/entity_roundtrip.c:226-253`, run by `EntityYaml.DaFreshRoundTrip`. They return codes 82 to 88: no probe, Listener, the 14999/15000 ms edge across wrap, and invalid address.
  - The claim is in the PR body ("all 15 added hosted tests have individual physical-removal escapes") and in the REVIEW READY comment.
- **Authority:** issue #24 acceptance 4 says: "Each mutant must escape without its test." Four of its five named terms are affected: no probe, window edge, Listener with no probe, and invalid address. CONTRIBUTING requires a runnable planted defect for each regression.
- **Evidence:**
  - `receipts/physical-removal.json`: each named test was deleted from the source, its plant applied, and the complete GoogleTest suite (all 8 binaries) run. All five still fail, every time through `EntityYaml.DaFreshRoundTrip` (for example, code 82 for the no-probe plant).
  - The control `dafresh-expiry-equality`, with `AcmpFresh.StaleProbe` removed, escapes as expected.
  - `receipts/escape-probe.json` shows the same result with filter exclusion. The other 10 plants escape. All 15 killers fail on their own plants with their needles.
  - The author's linked evidence commit could not be inspected (see Limits).
- **Impact:** the published necessity proof for four acceptance-named terms is false. Each named test is redundant for its own plant, so the evidence does not show what acceptance 4 requires. The code is not weakened: the plants are still caught.
- **Required outcome:** each `dafresh-*` plant escapes the complete hosted suite when only its registered killer is removed, and is caught when the killer is present. Any of these would get there:
  - choose plants that only the named core test detects;
  - narrow the round trip to checks the core tests do not duplicate, while keeping a real RV32-executed freshness path;
  - get an explicit manager ruling that defines "its test" as a registered set, and register that set.

  Then publish per-test removal receipts against all test binaries and correct the PR body.
- **Verification:** `scripts/physical_removal.py` and `scripts/escape_probe.py` from this packet show `escapes: true` for all 15 plants.

### F2 - MINOR - Tests, Robustness - documented zero interval is untested; fail-open mutant survives

- **Where:** `docs/PORTING.md:325` says "Zero disables the probe term, while Listener registration still applies." The code is `src/acmp.c:1259`, and `acmp_init` accepts any `da_fresh_ms`.
- **Evidence:** in `receipts/escape-probe.json`, the plant `x-zero-never-expires` makes a zero interval never expire. One answer would then declare indefinitely. It SURVIVES the complete suite.
- **Why it matters:**
  - Only `AcmpFresh` sets the field. Every other fixture runs with zero but never queries the gate.
  - Hand-written configurations that omit the new field get zero. The downstream firmware builds its image configuration from a static zero-initialised `struct acmp_config` (milan-fpga `c6bd08c6`, `sw/firmware/ctrl/test/ctrl_image.c:15`), so this is a realistic path once the pin moves.
- **Authority:** CONTRIBUTING says a protocol change updates its tests, and a regression needs a failing assertion and a runnable planted defect.
- **Impact:** a documented port-contract behaviour introduced by this PR is unprotected. Its fail-open inversion lets the talker keep declaring forever after one probe, which is what issue #24 exists to prevent.
- **Required outcome:** either of these:
  - add a test with a registered plant showing that `da_fresh_ms == 0` never opens the gate on a probe alone, while a Listener still does;
  - or refuse zero (and values of 2^31 or more) in `acmp_init`, with a test, and update PORTING to match.
- **Verification:** `x-zero-never-expires` is caught, and the new plant escapes without its test.

### R1 - RESIDUE - Docs - authority attribution wording

- **Where:** `docs/PORTING.md:333-334` reads: "This acceptance point is the local transport contract in issue #24."
- **Problem:** issue #24 says only "answered". Anchoring the window at the response `ports->send` accepts is this PR's reading of that word; the issue does not define it.
- **Scope:** wording only. No code, test, figure or clause claim changes.
- **Exact fix:** replace the sentence with: "This acceptance point is this repository's reading of 'answered' in [issue #24](https://github.com/kebag-logic/tsn-c-stack/issues/24)."

### Suggestions (non-blocking)

- **S1** - Robustness. `p_send` indexes `a->sources` with the talker_uid taken from frame bytes (`src/acmp.c:122`).
  - This is safe today: only SUCCESS and TALKER_DEST_MAC_FAIL PROBE_TX_RESPONSE frames are counted, and they are built only after `talker_command` checks `src < n_sources` and the interface (`src/acmp.c:970-989`). The probe `x-any-probe-status` confirms the status filter is what keeps the index in range.
  - Suggestion: add an explicit bound, or carry the source in `acmp_owed` the way `probe_of` is carried.
- **S2** - RTL. The fabric records the ping when a PROBE_TX is accepted, before and regardless of transmitting the response (`KL_acmp_talker.sv:686-689`). The core records it when the response send is accepted.
  - The two agree on edge, wrap and term set. Under backpressure the core's window starts later by the deferral, and busy-dropped or lost answers do not refresh it.
  - Both satisfy the issue's "answered". Stating the difference in PORTING would help the milan-fpga half argue `DA_GATE` equivalence.
- **S3** - Docs. `acmp_config.da_fresh_ms` is the first member, which changes every field offset.
  - Add it to the PORTING `acmp_config` field table (`docs/PORTING.md:242-245`).
  - Consider a CHANGELOG entry like PR #23's, telling integrators they must set it.
- **S4** - Tests. `entity_check_dafresh` uses `struct port.delay` as its clock, but the `timer` callback also writes `delay` (`examples/entity_roundtrip.c:45`). That is harmless for the sink-less talker entity, but fragile. A dedicated field would be safer.

## Lens evidence

### Conformance

Clause and issue predicate, `src/acmp.c:1249-1266`:

- The query returns `dest_mac_valid AND (answered-and-fresh OR listener_registered)` per source.
- Destination validity is read live through the existing `env->source`.
- Both SUCCESS and TALKER_DEST_MAC_FAIL answers record demand. The fabric matches this: it pings before its DA check (05 F05.11).
- Only the source's configured interface counts. Unknown IDs, incompatible interfaces, other talker commands and queued or refused sends do not refresh.
- The interval comes from `acmp_config.da_fresh_ms`. The core has no mirrored constant; the generator holds the single 15000.
- The Listener level means any registration state, including Asking Failed, the same as the fabric's `lsn_reg_f` (`!= SRP_DECL_IGNORE`).
- The port boundary gets one input, `acmp_listener_registered`. It makes no port calls: `InputGuardsAndReentry` asserts `fk.calls.empty()`.
- The query uses only the existing time and source ports.

The STOP conditions do not trigger: no ADP or MAAP change, and the port contract gains one input. The Release image delta is +1,304 bytes (35,792 to 37,096; `receipts/rv32-size.txt`), within the 2,048-byte ruling. Debug is +2,208 bytes, informational.

### RTL (fabric equivalence)

- `KL_acmp_talker.sv:396-397` uses `fresh = pinged && (now - ping_ts) < DAFRESH_MS_P`, mod 2^32. That is the same half-open window as the core.
- The fabric's own suite (1,342 checks) passes with the pinned 5.050 simulator. Its expiry check sits at ping+15001 ms.
- The edge probe (`scripts/fabric_edge_probe.sh`, `receipts/fabric-edge-probe.txt`):
  - with expiry at exactly ping+15000 ms, the suite still passes (the gate closes);
  - at ping+14999 ms, D2 fails (the gate stays open).
- So the fabric is open at 14,999 ms and closed at 15,000 ms, identical to the core's `WindowEdge` and `WithinWindowAndRefresh` tests and to `entity_check_dafresh` codes 87 and 88.
- Out of the issue's scope, and not compared: the fabric's MAAP-conflict LEAVEALL2 backoff, and its silent drop of wrong-interface probes. The core keeps its existing INCOMPATIBLE_REQUEST reply; neither refreshes the window.

### Robustness

- **Differential run** (`scripts/dafresh_differential.c`, built against the head `src/acmp.c` with ASan/UBSan): 400 seeds × 20,000 random steps, 32,000,000 queries. The core matches an independent model across three sources on two interfaces, unknown IDs, interface mismatch, send refusal and delay, the owed queue at its 8-entry limit, Listener toggles, DA toggles, steps hitting 14999/15000/15001 ms, and starts near wrap. Zero mismatches (`receipts/dafresh-differential.txt`).
- **Sensitivity:** the harness detects all 8 plant and probe mutants it was run against (`receipts/dafresh-differential-mutants.txt`).
- **Re-entry:** refused and counted for both new entries.
- **Expiry:** observing expiry clears `answered`, so a stale answer cannot reappear after a later wrap within the documented half-range service contract.
- **Survivors:** `x-no-clock-refresh` is equivalent at this head, because no clock read precedes a probe-answer send in the same entry. `x-signed-age` is equivalent within the documented interval below 2^31. F2 is open.

### Tests

- 14 `AcmpFresh` tests and `EntityYaml.DaFreshRoundTrip` were added. Existing tests are unchanged: the diff only adds to `tests/`.
- Every acceptance-4 term has a test and a plant, and all 15 killers fail with their needles.
- 10 additional mutants were run. 7 are caught; 2 survivors are equivalent at this head (`x-no-clock-refresh`, `x-signed-age`); 1 survivor is a real gap (`x-zero-never-expires`, F2).
- YAML range plant: caught by `entity_selftest.py`, and it escapes when `test_dafresh_configuration` is removed. Plants that drop the emission or default the value to zero are caught by the golden check.
- Coverage: `src/acmp.c` 792/792 lines, 390/390 branches, ratchet raised.
- Mutation campaign: 363 caught, 0 escaped.
- Open: F1 and F2.

### Docs

- `docs/PORTING.md` "ACMP DA freshness" (line 309 onward) states the predicate and cites Milan v1.2 4.3.3.1. That meets acceptance 5, which allows "the README or the ACMP documentation". README.md itself does not state the predicate.
- REQUIREMENTS, requirements.json, TRACEABILITY and TESTS gain ACMP-11 rows. The traceability and inventory gates confirm they are current.
- ENTITY_YAML documents the optional `acmp` mapping.
- VERIFICATION's count (359 core + 4 generated = 363) matches the campaign.
- Open: F1, the PR body's evidence claim. R1 is residue.

## Executed evidence (this reviewer, local, exact head)

- **`scripts/validate.py --jobs 16 --graphs`:** 27 of 28 entries returned rc 0 (`receipts/validation-gates.json`, `receipts/validation-summary.txt`). That includes:
  - entity golden and controls, boundary self-test, needles, assertion templates, dependency pin;
  - comments, the conditional matrix, port contracts, the ACMP cache check, registration controls, licence;
  - traceability, the test inventory, coverage controls, privacy and its self-test;
  - the GCC build and tests (8/8), coverage, Clang sanitizer build and tests (8/8);
  - the mutation campaign (363/363) and its controls, and graphs.
- **`static-analysis` returned rc 1 locally.** The cause is the host analyzer (version 23.1.1), which reports `optin.performance.Padding` on the unchanged `struct acmp_sink`. Base `1ba2735` fails identically (7 diagnostics; `receipts/static-analysis-head-vs-base.txt`). The exact-head hosted job, using the pinned distribution analyzer (18), reports `static-analysis: rc 0`. This is an environment difference, not a PR defect.
- **`scripts/baremetal.py`:** Debug and Release at head and at base, rc 0, smoke passing, no unresolved symbols (`receipts/rv32-*-results.json`).
- **Hosted exact-head runs:** 38266085764 (pull_request) and 38266077627 (push). Both the `quality` and `bare-metal` jobs executed and succeeded; every listed step succeeded. The quality job logs all 28 gates at rc 0 (`receipts/hosted-pr-run-38266085764-*.txt`). Hosted and act acceptance remain the manager's.
- **Clone integrity after the probes:** HEAD and tree are exact, index equals the tree, no worktree blob differs, and no untracked or ignored files remain. There are no gitlinks (`receipts/clone-integrity.txt`).

## Reviewer-owned ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` p_send hook and the two new entries, `include/acmp.h`, issue acceptance 1-2 and 5, the assignment and ruling, Milan 4.3.3.1 per the issue, the RV32 size delta | R630-1 | 9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1 |
| RTL | CLEAN | `KL_acmp_talker.sv` (`fresh_f`, `lsn_reg_f`, ping commit), the processor's 05 F05.11/F05.12 design, fabric suite plus the 14999/15000 edge probe with the pinned 5.050 simulator | R630-1 | 9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1 |
| Robustness | UNCLEAN (F2) | index bounds, re-entry, wrap, owed queue and backpressure, zero and out-of-range interval, 32M-query sanitized differential | R630-1 | 9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1 |
| Tests | UNCLEAN (F1, F2) | `tests/test_acmp.cpp` AcmpFresh, `tests/test_entity.cpp`, `tests/mutations.json`, physical and filter removal escapes, 10 extra mutants, YAML plants, coverage, mutation campaign | R630-1 | 9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1 |
| Docs | UNCLEAN (F1; R1 residue) | `docs/PORTING.md`, REQUIREMENTS, requirements.json, TRACEABILITY, TESTS, ENTITY_YAML, VERIFICATION, README, CHANGELOG, PR body, REVIEW READY | R630-1 | 9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1 |

## Real limits

- The author's linked evidence (`review-evidence/tsn24-r1` at `69e883d1722a610eced051be3d1320b7f7dab95e`) could not be read. The contents API returns 404, a fetch is refused as "not our ref", and no `tsn24` evidence branch exists. Source-head execution evidence here is therefore this reviewer's local runs plus the exact-head hosted jobs.
- The Milan v1.2 text was not available to this reviewer. The predicate is judged against the issue's frozen wording and the fabric implementation.
- The local sanitizer build used the host Clang (version 23), because the pinned Clang 18 copy here has no sanitizer runtime. Clang 18 was used for the lexing gates. The hosted job covers the distribution Clang.
- No manager source bank exists at this head, and none is claimed or inferred. The current-dev merge candidate (source base `1ba2735`, live dev `c6bd08c6`) is not validated here.
- Physical calibration was NOT RUN. Neither target establishes board or transport behaviour.

## Pending manager duties

- Rule on, or carry back to the author, F1 (acceptance 4 escapes) and F2 (zero-interval test or refusal). Carry R1 to the residue checklist.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts. Own hosted and act acceptance.
- Before merge, two independent positive reviews are needed at the final head.

## Packet

Scripts and receipts are listed in `MANIFEST.sha256`. In receipts, host paths are written as `<packet>`, `<clone>`, `<tools>`, `<home>` and `<data>`.

R630-1 FINISHED
