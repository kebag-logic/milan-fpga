[R630] NEGATIVE - exact head 1edff3180c2ff435b855cc770fb8be371f2096b3

# R630-3 internal independent review: issue #24 / PR #25

- **Repository:** kebag-logic/tsn-c-stack, PR #25 (`acmp-da-fresh`). It closes issue #24 (milan-fpga lane F3b, core half).
- **Head:** exact head `1edff3180c2ff435b855cc770fb8be371f2096b3`, tree `e08f8e9ba2a3732edbdd4c3656c46676355c41a6`, source base `1ba2735`.
- **Scope:** a full review of `1ba2735..1edff31`, including the Round 2 delta (`9ef7bd5..0868387`) and the Round 3 delta (`0868387..1edff31`).
- **Fabric reference:** milan-fpga dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, processor gitlink `2ad2f845dd583f8310075fa2380cb60a04fd091a`, `hdl/acmp/KL_acmp_talker.sv`.
- **Reconstruction order:**
  1. CONTRIBUTING; there is no AGENTS.md or docs/README.
  2. README and docs.
  3. The issue body and every issue comment: assignment 6126061221, STOP 6126278688, ruling 6126295947, the three REVIEW READY comments, and the Round 2 (6127660189) and Round 3 (6128504411) instructions.
  4. REQUIREMENTS ACMP-11, PORTING "ACMP DA freshness" and ENTITY_YAML.
  5. `git diff 1ba2735..1edff31` and the four-commit history.
  6. Executable evidence.
- **Independence:**
  - Prior R630 reports were read only after my own pass over the diff.
  - R631-1 and R631-2 were read only after the verdict and ledger draft (`receipts/independent-verdict-draft.md`) was saved.
  - No R631-3 material was read.

## Verdict

NEGATIVE, on one MINOR finding (F1). Everything the Round 3 instruction asked for is met and reproduces at this head:

- **The two new tests and their plants.** The exact R630-2 plants `g-expiry-skipped-with-listener` and `g-expiry-skipped-invalid-da` are each caught by the complete hosted suite (all 8 binaries) through exactly one named test. Each escapes when only that test is physically deleted: 420 completed instances become 419.
- **R630-2's scripts.** `gap_mutants.py` and `physical_removal.py`, unchanged, report both plants CAUGHT and `escapes: true`.
- **Production code.** No production code changed in Round 3.
- **Records.** TESTS and TRACEABILITY are current.
- **Campaign.** 367/367 plants caught, 0 escaped.
- **Round 1 and Round 2 claims.** These reproduce too: all 19 registered ACMP-11 plants pass both the single-killer catch and the physical-removal escape.
- **Predicate.** It matches the issue's wording of Milan v1.2 4.3.3.1 and the fabric's `fresh_f`/`lsn_reg_f`. The fabric edge was re-run on the pinned 5.050 simulator.
- **Targets.** Both targets pass.
- **Image size.** The Release image grows by +1,072 bytes, under the 2,048-byte ceiling. It is byte-identical to the author's round-3 image.

F1 comes from a fresh gap-mutant pass over the predicate's state transitions. Three behaviours that this PR documents have no failing assertion, and a natural mutant of each survives the complete suite:

- the Listener input's interface isolation;
- a fresh probe outliving a Listener withdrawal, which the fabric asserts in its own suite;
- initialization clearing a registered Listener.

## Findings

### F1 - MINOR - Tests, Robustness - three documented ACMP-11 behaviours have no failing assertion

**Where:**

- **(a) Listener interface isolation.**
  - Code: `src/acmp.c:1242`.
  - Contract: `docs/PORTING.md:317` ("returns false for an unknown source, a mismatched interface or re-entry") and ACMP-11 at `docs/REQUIREMENTS.md:50` ("preserve interface and source isolation").
  - The only guard assertion is `tests/test_acmp.cpp:2478-2479`. It passes `interface == cfg.n_interfaces`, which is out of range. So its message, "Listener interface must match the configured source interface", is never tested with a valid but wrong interface.
- **(b) The OR predicate when a Listener withdraws while a probe is fresh.**
  - Code: `src/acmp.c:1245` and `src/acmp.c:1265`.
  - Contract: issue #24 acceptance 1 ("true while the destination address is valid and one of these holds") and `docs/PORTING.md:312-313`.
  - Every withdrawal assertion (`tests/test_acmp.cpp:2313`, `2346`, `2367`, `2410`, `2501`) withdraws only once the probe is stale or absent.
- **(c) Initialization clears the Listener level.**
  - Contract: `docs/PORTING.md:328-329` ("Each source owns an `answered_at` timestamp, an `answered` flag and a `listener_registered` level; initialization clears all three").
  - The assertion that claims it, `tests/test_acmp.cpp:2504-2505` ("initialization clears previous demand and probe timestamps"), runs `acmp_init` after the Listener has already been withdrawn at line 2499. Only the probe half of "demand" is exercised.

**Authority:**

- Issue #24 acceptance 1 and 4.
- ACMP-11 (`docs/REQUIREMENTS.md:50`) and the port contract this PR adds (`docs/PORTING.md:310-353`).
- CONTRIBUTING: "A protocol change updates its requirement, tests and traceability. A regression needs a failing assertion and a runnable planted defect."
- The fabric this core must match asserts (b) itself:
  - `tb/acmp_talker/sim_main.cpp:643-644` reads `set_lsn(3, LSN_NONE); CHECK(gates.empty(), "D1 still fresh: no withdraw on listener loss")`.
  - Its `EVC_LSN` re-evaluates `fresh_f || lsn_reg_f` (`KL_acmp_talker.sv:830-841`; `receipts/fabric-reference.txt`).
- Precedent: R630-1-F2 and R630-2-F1 found the same class of defect in this PR: a documented ACMP-11 behaviour with no failing assertion, and a natural surviving mutant. Both were ruled MINOR and fixed.

**Evidence:** `receipts/full-suite-summary.txt` and `receipts/full_suite_probe.json`, produced by `full_suite_probe.py`. Each run applies the plant to a fresh copy of the exact head and runs all 8 binaries with fresh XML. Each of these three mutants completes 420/420 instances with no failure:

| mutant | change | effect |
|---|---|---|
| `r630-3-listener-range-only` | `interface != a->cfg.source_interface[source]` becomes `interface >= a->cfg.n_interfaces` | Fail-open: a Listener seen on another configured interface opens the gate. |
| `r630-3-withdrawal-clears-probe` | Withdrawing a Listener also clears `answered` | Fail-closed: the Talker declaration is withdrawn while a probe answered less than 15 s ago is still fresh, which contradicts acceptance 1 and the fabric's D1 check. |
| `r630-3-init-keeps-listener` | `acmp_init` keeps each source's `listener_registered` across its `memset` | Fail-open after re-initialization, against `docs/PORTING.md:329`. |

The code at this head is correct on all three paths; only their protection is missing.

**Feasibility.** A disposable demonstration in a scratch clone added three assertions; this is not a source fix (`receipts/fix-demo-probe.json`):

- each mutant is then caught by exactly its own new test, with its needle, at 423 completed instances;
- each escapes when only that test is deleted, at 422 instances.

**Impact:**

- An ACMP-11 isolation guarantee, one combination of the acceptance-1 predicate, and a documented reset rule would all pass every gate if a future refactor broke them.
- Two of the three directions are fail-open (a talker declares without demand on its own interface). The third withdraws a stream that a fresh probe still wants. Both outcomes are what issue #24 exists to prevent.
- Field likelihood is low today because the code is correct, but the properties are promised and unprotected.

**Required outcome:**

- Add assertions that:
  - (a) `acmp_listener_registered(&a, 1, 0, true)` (a valid interface that is not source 0's) returns false and leaves `acmp_declaring(&a, 0)` false;
  - (b) a fresh probe keeps the gate open after a Listener is registered and then withdrawn inside the window;
  - (c) a Listener registered before `acmp_init` no longer opens the gate after it.
- Register the three plants above, or equivalents, in `tests/mutations.json`, each with its own named killer.
- Each plant must be caught by the complete suite and escape when only its killer is removed.
- Update TESTS and TRACEABILITY. The campaign stays at 0 escapes.

**Verification:**

- `full_suite_probe.py --plants plants_gap.json` reports the three mutants CAUGHT.
- With the registered plants and killers, `full_suite_probe.py` (full and removed modes), or R630-2's unchanged `physical_removal.py`, reports `escapes: true` for each.
- `scripts/mutation.py` stays at 0 escaped.

No other MINOR, MAJOR or BLOCKER finding is open. There is no new RESIDUE.

### Suggestions (non-blocking)

- **S1** (retained from R630-1-S1) - Robustness. `src/acmp.c:122` indexes `a->sources` with the talker_uid read back from the frame.
  - It is safe today. Only SUCCESS and TALKER_DEST_MAC_FAIL PROBE_TX_RESPONSEs count, and `talker_command` builds them only after `src < n_sources` and the interface check (`src/acmp.c:970-996`).
  - `x-any-probe-status` is still caught.
  - An explicit bound would make the invariant local.
- **S2** (retained from R630-1-S2) - RTL, Docs. The fabric stamps the ping when the PROBE_TX is accepted (`KL_acmp_talker.sv:683-690`). The core stamps it when `ports->send` accepts the response.
  - `docs/PORTING.md:330-336` calls this the repository's reading of "answered".
  - Naming the fabric difference would help the milan-fpga `DA_GATE` equivalence argument: under backpressure the window starts later, and busy-dropped commands do not refresh it.
- **S3** (retained from R630-1-S3) - Docs. CHANGELOG has no entry for the new first member of `acmp_config`, which moves every field offset, or for the two new entries. PR #23 recorded its new callback there.
- **S4** (retained from R630-2-S4) - Tests. These survivors are equivalent at this head; no action is needed unless a clock read is added before a counted send:
  - `x-no-clock-refresh` and `r630-3-drop-send-clock-reread`: no clock read precedes an accepted PROBE_TX_RESPONSE send in the same entry;
  - `x-signed-age`: equivalent within the documented interval below 2^31.

## Lens evidence

### Conformance

**Predicate** (`src/acmp.c:1250-1266`):

- Per source, it returns `dest_mac_valid AND (answered-and-younger-than-da_fresh_ms OR listener_registered)`.
- Destination validity is read live through the existing `env->source`.
- The interval is `acmp_config.da_fresh_ms`; the core has no mirrored constant.
- `scripts/entity_yaml.py:96-103, 233` accepts the optional `acmp` mapping, refuses any value other than 15000 and emits it. All four generated entities carry `15000u`.

**Answers** (`src/acmp.c:113-128`):

- Only accepted SUCCESS or TALKER_DEST_MAC_FAIL PROBE_TX_RESPONSEs count. They exist only for a known source on its configured interface.
- Unknown-ID, incompatible-interface and other talker replies do not count, and neither do queued, refused or lost sends.
- This matches the fabric, which pings before its DA check.

**Listener input** (`src/acmp.c:1237-1247`):

- It is one input, per source and per configured interface, with no port calls.
- The level means any registration, including Asking Failed, the same as the fabric's `lsn_reg_f`.

**Init** (`src/acmp.c:1015`). It refuses an interval of 2^31 or more before touching the instance. Zero disables the probe term.

**Other ACMP paths:**

- The `p_send` move is byte-identical apart from the added block.
- Response bytes and listener transitions are unchanged.
- The test diff only adds; the pre-existing tests are unchanged and green.
- No ADP, MAAP or port-contract change beyond the one input, so the STOP conditions do not apply.

**Release size:** 35,792 to 36,864 bytes (+1,072), within the ruling. Debug is +1,768, informational (`receipts/rv32-size.txt`).

### RTL (fabric equivalence)

- `fresh_f` is `pinged && (now - ping_ts) < DAFRESH_MS_P`, mod 2^32. That is the same half-open window and wrap arithmetic as the core.
- The ping needs a valid uid and a matching interface, and ignores DA validity: the same answer set as the core.
- The listener term is `!= SRP_DECL_IGNORE`.
- `EVC_LSN` re-evaluates `fresh || listener`, so a fresh probe survives a Listener loss (D1). The core is correct here; F1(b) is about its missing test (`receipts/fabric-reference.txt`).
- R630-1's `fabric_edge_probe.sh` was re-run unchanged on the pinned 5.050 simulator; its identity was checked (`receipts/fabric-edge-probe.txt`):
  - stock suite: 1342/1342;
  - expiry at ping+15000: still 1342/1342, the gate closes;
  - expiry at ping+14999: the D2 close checks fail, the gate is still open.
- The core matches: `WindowEdge` closes at 15000 ms and `WithinWindowAndRefresh` is open at 14999 ms.
- Not compared, because they are outside this core-half issue: LEAVEALL2 backoff, the source-disable wipe, and the fabric's silent drop of wrong-interface probes versus the core's preserved INCOMPATIBLE_REQUEST. Neither refreshes the window.

### Robustness

- **Re-entry.** Refused and counted for both new entries (`AcmpFresh.InputGuardsAndReentry`).
- **Index safety.** See S1.
- **Expiry latch.** Observing expiry clears `answered` before the destination or Listener is consulted. It is now protected by `StaleProbeAfterListenerWrap` and `StaleProbeAfterInvalidAddressWrap`. Both service at gaps of at most 1e9 ms, inside the documented less-than-2^31 contract, out to 2^32+100 ms.
- **Interval range.** The 2^31 refusal makes the half-range service contract sufficient for every accepted interval:
  - `g-refusal-after-memset` and `g-no-range-refusal` are caught;
  - `g-zero-refused` is caught by 97 tests.
- **RV32 execution** (`receipts/rv32-plant-probe.txt`). Planting the generated window as 15001, or dropping `s->answered = true`, makes both RV32 images exit 80 and 85 under QEMU. So the bare-metal target executes the generated freshness-true path.
- **Open:** F1(a) and F1(c).

### Tests

The 19 registered ACMP-11 plants are the 16 `dafresh-*`, `x-zero-never-expires`, and the two `g-expiry-*`.

- **Complete-suite grading** (`receipts/full-suite-summary.txt`). For each plant, the complete 8-binary suite fails exactly its one named killer with its needle (420 completed instances). With only that test physically deleted, the suite passes with no skips (419). Result: 19/19.
- **R630-2 `physical_removal.py`, unchanged** (`receipts/physical-removal.json`). The 18 plants whose killer is in `tests/test_acmp.cpp` all report `escapes: true`, with no remaining failure.
- **R630-2 `gap_mutants.py`, unchanged** (`receipts/gap-mutants.json`). All 6 are CAUGHT. The two Round 3 plants are each caught only by their new test.
- **R630-1 `escape_probe.py`, unchanged** (`receipts/escape-probe.json`):
  - 16/16 `dafresh-*` plants escape the complete suite with only their killer excluded;
  - 16/16 killers fail alone with their needles;
  - 8 of the extra mutants are caught; `x-no-clock-refresh` and `x-signed-age` are equivalent survivors;
  - the YAML range plant is caught and escapes without its owner; the no-emit and default-zero plants are caught.
- **Script identities.** The unchanged scripts match the R630-1 and R630-2 manifests, and the author's copies (`receipts/prior-script-identities.txt`).
- **Mutation campaign:** 367 CAUGHT, 0 ESCAPED, 0 ERROR.
- **Coverage:** `src/acmp.c` 792/792 lines and 392/392 branches, equal to the ratchet.
- **Reviewer gap mutants:** 17 were run; 13 are caught. Of the 4 survivors, 1 is equivalent (S4) and 3 are F1.
- **Open:** F1.

### Docs

- **Acceptance 5.** `docs/PORTING.md:310-353` states the predicate and cites Milan v1.2 4.3.3.1. Acceptance 5 allows this as "the README or the ACMP documentation"; README.md itself does not state it.
- **Requirements and indexes.** REQUIREMENTS ACMP-11, requirements.json, TRACEABILITY and TESTS are current. All 18 `AcmpFresh` and `EntityYaml.DaFreshRoundTrip` line anchors resolve to their declarations.
- **VERIFICATION.** "363 core plants and four generated configuration plants" equals the 367-plant inventory.
- **ENTITY_YAML.** `docs/ENTITY_YAML.md:139` lists all four configuration plants.
- **PR body.** Every Round 3 figure reproduces:
  - 1e9 ms maximum gap and 2^32+100 ms;
  - 420 to 419 instances;
  - 367 plants with 0 escapes;
  - 792/792 lines and 392/392 branches;
  - 36,864 (+1,072) and 47,512 (+1,768) bytes;
  - 28 gates, as hosted.
- **Docs lens.** No Docs defect is open. F1 is missing protection for true documented claims, not a wrong claim.

## Executed evidence (this reviewer, local, exact head)

- **`scripts/validate.py --jobs 10 --graphs`:** 27 of 28 entries returned rc 0 (`receipts/validation-gates.json`, `receipts/validation-summary.txt`). These include:
  - entity golden and controls, boundary self-test, needles, assertion templates, the dependency pin;
  - comments, the conditional matrix, port contracts, the ACMP cache check, registration controls, licence;
  - traceability, the test inventory, coverage controls, privacy and its self-test;
  - GCC build and tests (8/8) with coverage, and the Clang sanitizer build and tests (8/8);
  - mutation (367/367) and its controls, and graphs.
- **`static-analysis` returned rc 1 locally.** The cause is the host analyzer (LLVM 23.1.1), which reports `optin.performance.Padding` on the unchanged `struct acmp_sink`. Base `1ba2735` gives the identical diagnostic set (`receipts/static-analysis-head-vs-base.txt`). The exact-head hosted job reports `static-analysis: rc 0`. This is an environment difference, not a PR defect.
- **`scripts/baremetal.py`:** Debug and Release at head and base, rc 0, smoke checks pass, no unresolved symbols (`receipts/rv32-head-results.json`, `receipts/rv32-base-results.json`). The loadable images match the author's round-3 `sizes.json` SHA-256 values (`receipts/rv32-size.txt`).
- **Hosted exact-head runs** (`receipts/hosted-runs.txt`, `receipts/hosted-pr-run-38280309558-gates.txt`):
  - 38280309558 (pull_request) and 38280304715 (push): `quality` and `bare-metal` executed and succeeded, with every listed step succeeding and none skipped;
  - the PR quality log lists all 28 gates at rc 0;
  - hosted and act acceptance remain the manager's.
- **Author evidence** (`receipts/evidence-location.txt`):
  - the assignment's link names tsn-c-stack, where commit `66585285` returns 404/422;
  - the identical commit resolves in kebag-logic/milan-fpga ("tsn24 author packet round 3 at 1edff318");
  - its `author-r3` STATUS (REVIEW READY, 28 gates rc 0, 367/0, 420/419, image sizes), the gate return codes and the image hashes were checked and agree with this reviewer's runs.
- **Memory:** the unit peak was 9,166,569,472 bytes, under the 12 GB cap (`receipts/memory.txt`).
- **Clone integrity after all probes** (`receipts/clone-integrity.txt`). Every probe ran in disposable copies. One ignored `scripts/__pycache__` left by running the validation kit was removed. Then:
  - HEAD and tree are exact, and the index equals the tree;
  - all 98 tracked blobs and modes match;
  - no untracked or ignored files remain;
  - there are no gitlinks (no `.gitmodules` at this head).

## Prior findings

Every earlier public finding on this PR, checked at this head:

| finding | origin | status at 1edff318 | evidence |
|---|---|---|---|
| R630-1-F1 (MAJOR): five plants did not escape without their named test | R630-1 | RESOLVED | All 19 registered plants, including those five, are caught only by their killer and escape on its physical removal (`receipts/full-suite-summary.txt`, `receipts/escape-probe.json`, `receipts/physical-removal.json`). |
| R630-1-F2 (MINOR): zero interval untested | R630-1 | RESOLVED | `AcmpFresh.ZeroWindow` (`tests/test_acmp.cpp:2399`) and `x-zero-never-expires` (caught only by it, escapes without it); `AcmpFresh.WindowRange` (`:2414`) and `dafresh-half-range` cover the 2^31 refusal at `src/acmp.c:1015`. |
| R630-1-R1 (RESIDUE): attribution of the answer acceptance point | R630-1 | RESOLVED | Exact text at `docs/PORTING.md:336`. |
| R630-1-S1: explicit source bound in `p_send` | R630-1 | RETAINED as S1 | `src/acmp.c:122` is unchanged. |
| R630-1-S2: state the fabric timestamp difference | R630-1 | RETAINED as S2 | Not named in PORTING. |
| R630-1-S3: PORTING field table and CHANGELOG | R630-1 | PARTLY RESOLVED; CHANGELOG part RETAINED as S3 | Field table at `docs/PORTING.md:246`. |
| R630-1-S4: round-trip clock shared `delay` | R630-1 | RESOLVED | Dedicated `now` and `fresh_clock` (`examples/entity_roundtrip.c:21, 220-223`). |
| R631-D01 (RESIDUE): ENTITY_YAML plant table read as exhaustive | R631-1 | RESOLVED | `docs/ENTITY_YAML.md:139-148` lists four plants. |
| R630-2-F1 (MINOR): wrap guarantee untested with a Listener or an invalid destination | R630-2 | RESOLVED | See below. |
| R630-2-S1 to S3 (carried from R630-1-S1 to S3) | R630-2 | RETAINED as S1 to S3 | As above. |
| R630-2-S4: `x-no-clock-refresh` equivalent | R630-2 | RETAINED as S4 | Still equivalent. |

**R630-2-F1 evidence:**

- `AcmpFresh.StaleProbeAfterListenerWrap` (`tests/test_acmp.cpp:2301`) and `AcmpFresh.StaleProbeAfterInvalidAddressWrap` (`:2318`) were added, with the exact plants registered (`tests/mutations.json`).
- The unchanged `gap_mutants.py` reports both CAUGHT; the unchanged `physical_removal.py` reports both `escapes: true`.
- TESTS and TRACEABILITY carry both tests.

R631-1 and R631-2 recorded no other finding; their suggestions restate R630-1-S1 to S3.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` (p_send hook, `acmp_init` range, `acmp_listener_registered`, `acmp_declaring`), `include/acmp.h`, issue acceptance 1-5, assignment, ruling, Round 2 and Round 3 instructions, ACMP-11, Milan 4.3.3.1 per the issue, YAML generator and the four generated configs, RV32 size delta | R630-3 | 1edff3180c2ff435b855cc770fb8be371f2096b3 |
| RTL | CLEAN | `KL_acmp_talker.sv` (`fresh_f`, `lsn_reg_f`, ping commit, `EVC_LSN`) at processor `2ad2f845` from milan-fpga `c6bd08c6`; fabric suite D1/D2 and the 14999/15000 edge probe on the pinned 5.050 simulator | R630-3 | 1edff3180c2ff435b855cc770fb8be371f2096b3 |
| Robustness | UNCLEAN (F1) | index bounds, re-entry, expiry latch and wrap aliasing, owed queue and backpressure, zero and 2^31 interval, per-source and per-interface isolation, reset, RV32 plant execution | R630-3 | 1edff3180c2ff435b855cc770fb8be371f2096b3 |
| Tests | UNCLEAN (F1) | `tests/test_acmp.cpp` AcmpFresh (18 tests), `tests/test_entity.cpp`, `examples/entity_roundtrip.c`, `tests/mutations.json` (19 ACMP-11 plants), complete-suite catch and physical-removal grading, unchanged R630-1 and R630-2 scripts, 17 reviewer gap mutants, campaign 367/367, coverage | R630-3 | 1edff3180c2ff435b855cc770fb8be371f2096b3 |
| Docs | CLEAN | `docs/PORTING.md`, REQUIREMENTS, requirements.json, TRACEABILITY, TESTS, ENTITY_YAML, VERIFICATION, README, CHANGELOG, PR body, the three REVIEW READY comments | R630-3 | 1edff3180c2ff435b855cc770fb8be371f2096b3 |

## Real limits

- **Clause text.** The Milan v1.2 text was not available to this reviewer. The predicate is judged against the issue's frozen wording and the fabric implementation.
- **Local toolchains differ from the hosted ones:**
  - GCC is 16.2 and the sanitizer Clang is 23.1. The pinned Clang 18 copy has no sanitizer runtime and was used for the lexing gates.
  - The RV32 compiler is the distribution `riscv64-elf-gcc` 16.2. Its loadable images are nonetheless byte-identical to the author's.
  - The static analyzer is 23.1 (see Executed evidence).
  - The hosted jobs cover the pinned distribution toolchains.
- **Author evidence.** It was read only for STATUS, sizes, gate return codes and the two script copies. This reviewer's conclusions rest on its own runs.
- **Manager source bank.** None exists at this head, and none is claimed or inferred. The current-dev merge candidate (source base `1ba2735`, live dev `c6bd08c6`) is not validated here.
- **Hardware.** Physical calibration was NOT RUN. Simulation and QEMU smoke establish neither board timing nor deployed transport behaviour. Field skips are not hardware proof.

## Pending manager duties

- Carry F1 back to the author. Carry S1-S4 at the manager's discretion.
- Correct the evidence locator. The assignment's `tsn-c-stack/tree/66585285...` link is a 404; the commit lives in kebag-logic/milan-fpga.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts. Own hosted and act acceptance.
- Before merge, two independent positive reviews are needed at the final head.

## Packet

Scripts, plant lists and receipts are listed in `MANIFEST.sha256`.

- **New scripts:**
  - `full_suite_probe.py`: complete-suite plant grading in full, physical-removal and control modes;
  - `rv32_plant_probe.sh`.
- **Plant lists:**
  - `plants_registered.json`: the 19 registered ACMP-11 plants;
  - `plants_gap.json`: the 17 reviewer gap mutants;
  - `plants_fix_demo.json`: the disposable demonstration.
- **Unchanged prior scripts** (`prior-scripts/`), whose identities are in `receipts/prior-script-identities.txt`:
  - R630-1's `escape_probe.py` and `fabric_edge_probe.sh`;
  - R630-2's `gap_mutants.py` and `physical_removal.py`.

In receipts, host paths are written as `<packet>`, `<clone>`, `<tools>`, `<home>` and `<data>`.

R630-3 FINISHED
