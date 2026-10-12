[R630] POSITIVE - exact head f13c9c16c2b300d158f980dd7c7f071dcb84df5b

# R630-4 internal independent review: issue #24 / PR #25

- **Repository and PR:** kebag-logic/tsn-c-stack PR #25 (`acmp-da-fresh`). It closes issue #24 (milan-fpga lane F3b, core half).
- **Head:** exact head `f13c9c16c2b300d158f980dd7c7f071dcb84df5b`, tree `591d38854105564a5d632c18e846b0dd60c2f148`.
- **Base and scope:** source base `1ba2735`. This is a full review of `1ba2735..f13c9c1`, covering all five commits. The Round 4 delta is `1edff31..f13c9c1`.
- **Fabric reference:** milan-fpga dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, protocol-processor gitlink `2ad2f845dd583f8310075fa2380cb60a04fd091a`, `hdl/acmp/KL_acmp_talker.sv`.
- **Reconstruction order:**
  1. CONTRIBUTING. There is no AGENTS.md and no docs/README.
  2. README and docs.
  3. The issue body and every issue comment: assignment 6126061221, STOP 6126278688, ruling 6126295947, four REVIEW READY comments, and the Round 2, 3 and 4 instructions (6127660189, 6128504411, 6129059074).
  4. ACMP-11, PORTING "ACMP DA freshness", ENTITY_YAML and the VERIFICATION contract table.
  5. `git diff 1ba2735..f13c9c1` and the history.
  6. Executable evidence: the published author receipts at milan-fpga `a81c70d2` `review-evidence/tsn24-r1/author*` (no reviewer report was read there before the verdict), and the hosted check runs at the exact head.
- **Independence:**
  - My verdict and ledger draft were written before I read any prior review report. It is timestamped in `receipts/independent-verdict-draft.txt`.
  - I then read the earlier findings (R630-1/2/3, R631-1/2/3) and resolved each one below.
  - No R631-4 material was read.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. There is one new wording-only RESIDUE (R630-4-R1) and one new SUGGESTION (R630-4-S1). All five lenses are CLEAN.

**Predicate.** The predicate in `src/acmp.c:1250-1266` is: valid destination AND (an answered probe younger than `acmp_config.da_fresh_ms` OR a registered Listener), per source.

- It matches issue #24 acceptance 1 and the issue's wording of Milan v1.2 4.3.3.1.
- It matches the fabric processor's `fresh_f` / `lsn_reg_f` (`KL_acmp_talker.sv:391-398`).
- **Edge.** The window is half-open: open at 14999 ms, closed at 15000 ms. This was executed on both sides: the core through the hosted tests, and the fabric bench at both edges with the pinned 5.050 simulator.
- **Wrap.** The window survives counter wrap, including serviced aliasing past 2^32 ms.

**Round 4 (the request in 6129059074).** Everything it asked for is met and reproduces:

- **Contract table.** The table at `docs/VERIFICATION.md:215-276` has one row per behaviour sentence of `docs/PORTING.md:310-353` (29 rows) and of ACMP-11 at `docs/REQUIREMENTS.md:50` (2 rows). I checked it row by row against both sources.
  - Every sentence has a row.
  - The five no-test rows (P07, P08, P19, P25, P28) give sound reasons: caller obligations, an authority statement, and the clock precondition.
  - All 42 distinct plants are registered. Each row's registered killer appears in that row.
- **Per-row check.** Run independently for every row:
  - Each of the 42 plants fails exactly its named killer in the complete eight-binary suite, at 424 completed instances.
  - Each escapes when only that test is physically deleted: 423 instances, no failures, no skips.
- **R630-3's `full_suite_probe.py`.** Run unchanged (byte-identical to the author's copy). The three requested plants are CAUGHT by their single killers.
- **Production code.** No production code changed in Round 4: the delta touches only tests, the registry and docs.

**Both targets.** Linux GCC with coverage and Clang with ASan/UBSan pass. Bare-metal RV32 Debug and Release link, pass the import audit and run their smoke checks under the emulator.

- The Release loadable image grows from 35,792 to 36,864 bytes (+1,072). That is within the 2,048-byte Release ceiling set by ruling 6126295947.
- Debug grows from 45,744 to 47,512 bytes (+1,768). That figure is informational.

## Findings

### R630-4-R1 - RESIDUE - Docs - the contract-audit procedure points at an unlinked "review packet"

- **Where:** `docs/VERIFICATION.md:229-230`: "The review packet contains the portable full-suite runner, table-derived plant list, per-row grading receipts and raw XML."
- **Authority and evidence:**
  - No review packet exists in the repository.
  - The sentence gives no link or location.
  - The repository's gate table (`docs/VERIFICATION.md:17-43`) does not include the per-row check.
  - The procedure itself is fully specified in the preceding paragraph, and I re-implemented it from that text alone (`scripts/probe.py`).
- **Impact:** wording only. A reader cannot locate the named artifacts from the repository. No measurement, figure, test, code, generated artifact, conformance or clause claim changes, and no privacy rule is touched.
- **Exact fix:** replace the sentence with: "The runner, plant list and per-row receipts for this audit are published with the pull request's review evidence, outside this repository."
- **Verification:** the manager carries this to the residue checklist.

### R630-4-S1 - SUGGESTION - Tests, Robustness - no behavioural witness that a local Listener's own PROBE_TX_COMMAND leaves the local source closed

- **Where:** `src/acmp.c:119` filters counted frames by `frame[O_MSG] == ACMP_MSG_PROBE_TX_RESPONSE`.
- **Evidence:** the plant `r630-4-own-probe-command-counts` also counts the core's own outgoing PROBE_TX_COMMAND (sink probing). It is CAUGHT, but only by `AcmpCore.CommandPortBudgets` and `AcmpCore.TimerPortBudgets`, because of the extra clock read (`receipts/r630-4-results.json`).
- **Impact:** a variant that avoided the extra clock read would be judged only on predicate behaviour, and no predicate assertion covers this case. A duplex entity whose sink probes a remote talker with `talker_uid == k` would then open local source `k`. The head is correct, and the P15 sentence is covered.
- **Optional outcome:** a duplex-style test that binds a sink (it emits PROBE_TX_COMMAND with talker_uid 0) and asserts `acmp_declaring(&a, 0)` stays false.

## Prior findings at this head

| ID | Severity | Lenses | Status at f13c9c1 | Evidence |
|---|---|---|---|---|
| R630-1-F1 | MAJOR | Tests, Docs | **RESOLVED** | `examples/entity_roundtrip.c:220-246` checks only the generated 15000 ms value and one freshness-true path, which RV32 executes. R630-1's `physical_removal.py` and `escape_probe.py`, run unchanged: 29/29 removal escapes, and every registered dafresh/x plant escapes with only its killer excluded and fails alone on its needle. The PR body claim is corrected. |
| R630-1-F2 | MINOR | Tests, Robustness | **RESOLVED** | `AcmpFresh.ZeroWindow` (`tests/test_acmp.cpp:2446`) kills `x-zero-never-expires` and `dafresh-zero-blocks-listener`. `AcmpFresh.WindowRange` (`:2461`) and `src/acmp.c:1015` refuse values of 2^31 or more without changing the instance or calling a port. |
| R630-1-R1 | RESIDUE | Docs | **RESOLVED** | `docs/PORTING.md:336` carries the exact required sentence. |
| R631-D01 | RESIDUE | Docs | **RESOLVED** | `docs/ENTITY_YAML.md:141-148` lists all four configuration plants. |
| R630-2-F1 | MINOR | Tests, Robustness | **RESOLVED** | `AcmpFresh.StaleProbeAfterListenerWrap` and `StaleProbeAfterInvalidAddressWrap` (`tests/test_acmp.cpp:2301`, `:2318`) service queries through 2^32+100 ms with gaps of 1e9 ms or less. R630-2's `gap_mutants.py` (6/6 caught) and `physical_removal.py` (both `escapes: true`), run unchanged. |
| R630-3-F1 | MINOR | Tests, Robustness | **RESOLVED** | `AcmpFresh.ListenerInterfaceMismatch`, `FreshProbeAfterListenerWithdrawal` and `InitClearsListener` (`tests/test_acmp.cpp:2372`, `:2380`, `:2390`). R630-3's `full_suite_probe.py`, run unchanged, reports the three plants CAUGHT by those single killers. In the per-row check, each escapes with only its killer removed (424 to 423). |
| R630-1-S1 | SUGGESTION | Robustness | RETAINED | `src/acmp.c:122` indexes by the talker_uid read back from the frame. It is safe because only SUCCESS and DEST_MAC_FAIL responses for known, interface-matched sources are counted. `r630-4-any-status` and `r630-4-unknown-id-counts` are caught by `OtherRepliesDoNotRefresh`. |
| R630-1-S2 | SUGGESTION | RTL, Docs | PARTLY RESOLVED | VERIFICATION row P19 now states that fabric command acceptance can precede the core endpoint under backpressure. PORTING still does not name the difference. |
| R630-1-S3 | SUGGESTION | Docs | PARTLY RESOLVED | The field-table entry is present (`docs/PORTING.md:246`). There is no CHANGELOG note. PRs #19 and #20 also added none, so there is no rule to cite. |
| R630-1-S4 | SUGGESTION | Tests | RESOLVED | Separate `now` field (`examples/entity_roundtrip.c:21`). |
| R630-2-S4 | SUGGESTION | Tests | RETAINED (equivalent controls) | `x-no-clock-refresh`, `r630-3-drop-send-clock-reread` and my `r630-4-stale-cache` survive. They are equivalent because no clock read precedes an accepted PROBE_TX_RESPONSE in the same entry (`enter` clears the cache; the rx-talker and poll paths call no `now()` before `p_send`). `x-signed-age` is equivalent within the documented interval below 2^31. |

## Lens evidence

### Conformance - CLEAN

- **Predicate** (`src/acmp.c:1250-1266`):
  - Per source, it returns `dest_mac_valid AND (answered OR listener_registered)`, after observed expiry clears `answered`.
  - Destination validity is read live through the existing `env->source`.
  - The interval is `cfg.da_fresh_ms`. The core has no mirrored constant.
  - Zero disables the probe term, as ruled in 6127660189.
- **Answers** (`src/acmp.c:113-128`):
  - Only PROBE_TX_RESPONSEs that `ports->send` accepted with SUCCESS or TALKER_DEST_MAC_FAIL count.
  - Those frames are built only by `talker_command` (`src/acmp.c:959-1007`) after the unknown-ID and interface checks.
  - Queued and refused answers count only when `acmp_poll` sends them.
  - This is the documented reading of the issue's "answered" (`docs/PORTING.md:331-337`).
- **Fabric equivalence** (`KL_acmp_talker.sv:396-398`, `:686-689`, `:391-393`):
  - The window arithmetic is the same: `(now - ping_ts) < 15000`, modulo 2^32.
  - The answer set is the same: a valid uid on a matching interface pings before the DA check, so DEST_MAC_FAIL also pings.
  - The Listener term is the same: any state other than IGNORE, including Asking Failed.
  - The core is stricter in one respect: it clears `answered` on observed expiry, while the fabric keeps `pinged` and would alias after 2^32 ms. This does not break equivalence within the documented service contract.
  - Backpressure origin difference: see R630-1-S2 above.
- **Configuration:** the generator emits `.da_fresh_ms = 15000u` for all four example entities. `configs/talker.yaml:1-2` sets it explicitly. Omitting `acmp` selects 15000 (`scripts/entity_yaml.py:96-103, 233`).
- **No other ACMP path changed:**
  - The `p_send` move is byte-identical apart from the added block.
  - `finish()` (`src/acmp.c:495-515`) calls no `now()`, so the post-send clock sample cannot shift any later deadline.
  - The added clock read after an accepted send follows the existing rule at `docs/PORTING.md:101-102`.
  - `tests/test_acmp.cpp` has 294 additions and 0 deletions. The only edit to an existing registry entry is `acmp-init-too-many-sources`, re-anchored to the changed line.
  - ADP, MAAP and the port contract are unchanged beyond the one input, so no STOP condition applies.

### RTL - CLEAN

- **Artifact:** `KL_acmp_talker.sv` at gitlink `2ad2f845`, from milan-fpga `c6bd08c6`.
- **Simulator identity:** pinned simulator identity verified as `Verilator 5.050 2026-07-01 rev v5.050`.
- **Fabric bench** (`tb/acmp_talker`), run three ways by `scripts/fabric_edge.sh` (`receipts/fabric-edge.txt`, `receipts/fabric/`):
  - unchanged: 1342/1342 PASS;
  - expiry check moved to exactly 15000 ms: 1342/1342 PASS, so the gate is closed at the edge;
  - expiry check moved to 14999 ms: D2 fails ("freshness lapse: gate strobe missing"), so the gate is still open at 14999.
- **Core edges:**
  - `AcmpFresh.WithinWindowAndRefresh` and `ClockWrap` test open at 14999.
  - `AcmpFresh.WindowEdge` tests closed at 15000, including from `UINT32_MAX - 999`.
- No RTL is changed by this PR.

### Robustness - CLEAN

- **Bounds:** source index bounded through the response construction (see R630-1-S1).
- **Input refusals:**
  - `acmp_listener_registered` refuses an unknown source, a wrong interface (valid or out of range) and re-entry, and makes no port call.
  - `acmp_declaring` refuses re-entry and unknown sources.
  - Both count `reentries` and call the trap hook (`AcmpFresh.InputGuardsAndReentry`).
- **Init:** `acmp_init` refuses an interval of 2^31 or more before the `memset`, and clears all per-source state.
- **Expiry and wrap:** expiry is cleared under both Listener masking and invalid-address masking, which prevents wrap resurrection. My `r630-4-derived-fresh` plant, a fabric-style derived predicate with no clearing, is caught by three wrap tests.
- **Sanitizers:** the ASan/UBSan suite passes.
- **My plants:** 14 plants, all non-equivalent ones caught (`receipts/r630-4-results.json`):
  - any-status, unknown-ID and incompatible refresh;
  - refused-send counting;
  - wrong index field;
  - skipped source read;
  - sticky Listener;
  - loosened range;
  - edge ±1.

### Tests - CLEAN

- **Validation:** `scripts/validate.py --jobs 16 --graphs` passed 27 of 28 gates locally (`receipts/validation-gates.json`). These include:
  - entity golden and controls, boundary, needles, assertion templates, dependencies, comments, conditionals, port contracts, ACMP cache, registration, licence;
  - traceability, test inventory, coverage controls, privacy;
  - GCC and coverage, Clang sanitizers, mutation, mutation controls and graphs.
- **Static analysis:** the one local failure, `static-analysis`, is environmental. The host has clang-tidy 23 instead of the distro version the workflow installs. Base `1ba2735` fails identically on the same pre-existing `struct acmp_sink` padding diagnostic, and the head adds no diagnostic (`receipts/validation-logs/static-analysis*.log`). The hosted `quality` job at this exact head ran the same `validate.py` with the workflow's pinned packages and passed.
- **Coverage:** `src/acmp.c` 792/792 lines and 392/392 branches, matching `tests/coverage.ratchet`.
- **Mutation campaign:** 388/388 CAUGHT, 0 escaped, 0 errors.
- **Acceptance 4 terms.** Each plant is caught by exactly its test and escapes when that test is removed:
  - no probe: `NoProbe` / `dafresh-unanswered-clock`;
  - stale probe: `StaleProbe` / `dafresh-expiry-equality`;
  - exact window edge: `WindowEdge` / `dafresh-inclusive-edge`;
  - Listener without a probe: `ListenerWithoutProbe` / `dafresh-listener-needs-probe`;
  - invalid address: `InvalidAddress` / `dafresh-ignore-address`.
- **Generator plants** (`receipts/gen-results.json`):
  - Widening the range either way is caught only by `test_dafresh_configuration`, and escapes when that method is removed.
  - Emission and acceptance plants are also caught by the golden check.
- **RV32 sensitivity** (`receipts/rv32-plants.txt`): removing the probe term, or setting the generated talker window to 15001, makes `baremetal.py` fail under the emulator. The control passes.

### Docs - CLEAN

- **Acceptance 5:** the predicate and the clause citation are stated in `docs/PORTING.md:310-313` (ACMP documentation) and in ACMP-11 (`docs/REQUIREMENTS.md:38-50`).
- **Other records:**
  - The field table (`docs/PORTING.md:246`) and the ENTITY_YAML schema rows and plant table are present.
  - TESTS and TRACEABILITY are regenerated; their gates pass.
  - VERIFICATION's campaign count is 384 + 4 = 388, which matches the campaign.
- **PR body:** its figures reproduce: 42 plants, 424/423 instances, 388 plants, 792/392 coverage, +1,072 / +1,768 bytes, and query gaps of 1e9 ms or less.
- **Residue:** R630-4-R1 is wording only.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #24 acceptance and rulings 6126061221, 6126295947, 6127660189, 6128504411, 6129059074; `src/acmp.c`; `include/acmp.h`; ACMP-11; PORTING freshness contract; YAML generator and goldens; fabric `KL_acmp_talker.sv`; Release size | R630-4 (full review) | f13c9c16c2b300d158f980dd7c7f071dcb84df5b |
| RTL | CLEAN | Fabric `fresh_f`/`lsn_reg_f`/ping commit; `tb/acmp_talker` executed unchanged and at both edges with the pinned 5.050 simulator | R630-4 | f13c9c16c2b300d158f980dd7c7f071dcb84df5b |
| Robustness | CLEAN | Bounds, re-entry, range refusal, init clearing, masked expiry and wrap; sanitizers; 14 reviewer plants | R630-4 | f13c9c16c2b300d158f980dd7c7f071dcb84df5b |
| Tests | CLEAN | `validate.py` gates (27 + environmental static-analysis control); coverage; 388-plant campaign; 42-plant per-row catch and removal check; R630-1/2/3 scripts unchanged; generator plants; RV32 Debug/Release and RV32 plants; hosted runs | R630-4 | f13c9c16c2b300d158f980dd7c7f071dcb84df5b |
| Docs | CLEAN (RESIDUE R630-4-R1 carried) | CONTRIBUTING, README, PORTING, REQUIREMENTS, ENTITY_YAML, VERIFICATION contract table, TESTS, TRACEABILITY, PR body | R630-4 | f13c9c16c2b300d158f980dd7c7f071dcb84df5b |

## Real limits

- **Static analysis.** The local run used clang-tidy 23 (the pinned version was not available locally). The gate failed identically on base and head. Pass evidence at this head comes from the hosted `quality` job and the author's receipt, not from a local run.
- **Sanitizer compiler.** Local sanitizers used Clang 23.1.1. Comment and assertion lexing used the pinned Clang 18.1.3.
- **Hosted runs.** I inspected the hosted check runs (both `quality` and both `bare-metal` jobs executed and succeeded, on push and pull_request). I did not take hosted acceptance; the manager owns it.
- **Platform scope.** The hosted wrap and mutation assertions and the RV32 positive-path smoke do not establish platform integration, the milan-fpga `DA_GATE` wiring, or physical timing.
- **Not run.** Physical calibration was NOT RUN. No hardware, field or bench work was done. Field skips are not hardware proof.
- **Clause text.** The Milan v1.2 text was not available to me. Conformance is judged against the issue's frozen wording of 4.3.3.1 and the fabric implementation.
- **Clone integrity.** No source edits were made. All probes ran on copies (`git archive` of the exact head). The clone was verified afterwards (`receipts/clone-integrity.txt`):
  - HEAD, tree and index are `591d388`;
  - all 98 tracked blobs match by hash, with modes intact;
  - the porcelain status is empty, including ignored files, after removing a bytecode cache my run created;
  - the repository has no submodule gitlinks.

## Pending manager duties

- Obtain the second independent positive review.
- Build and validate the current-dev merge candidate at the merge turn: source base `1ba2735`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`, with the builder and native banks. Then link the receipts on the PR. No manager source bank ran at this head, and none is claimed.
- Own hosted and act acceptance.
- Carry R630-4-R1 to the residue checklist.
- Track the milan-fpga half: moving the pin, publishing the `DA_GATE` predicate, and setting `da_fresh_ms` in the firmware's hand-written configuration (zero disables the probe term).

R630-4 FINISHED
