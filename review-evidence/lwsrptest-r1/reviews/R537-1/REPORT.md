[R537] POSITIVE - exact head e4f9995b791489c53b8ccb8a8dc09ec508e32e6b
<!-- SPDX-License-Identifier: Apache-2.0 -->

Independent external review, round R537-1, issue #2 / PR #3. Reviewed tree: `9457a9568dad668a04e2a4042f6d3f984aebe387`; base: `19f5796b63652eb1151906de73cb827d4980a53f`. All five lenses applied. No open BLOCKER, MAJOR or MINOR finding. One prose RESIDUE and three SUGGESTIONs remain; one suggestion was also identified in this independent pass. This verdict covers this standalone library and this exact source tree.

The frozen acceptance is met: the native build succeeds; CTest runs nine codec cases with 1,690 passing assertions; all three behave scenarios and ten steps execute successfully; the five individual planted reversals fail their named checks; and every `src/` byte is unchanged. The two added files carry the required Apache-2.0 SPDX first line.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue acceptance and assignment; all five changed paths; source identity, licenses and publication checks; public evidence tree identity | R537-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| RTL | CLEAN (not applicable) | Standalone C11 tree and complete change list; no RTL or programmable-logic implementation changed | R537-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| Robustness | CLEAN | CMake dependency handling and Zephyr early return; C/Python binding signatures; vtable forwarding and all 256 port IDs; 100 adapter lifecycle cycles; Release exports | R537-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| Tests | CLEAN | Base/head build, CTest, behave; codec registration and count; five independent reversal copies; binding probe | R537-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| Docs | CLEAN | README, architecture and public interface headers; issue/assignment/PR text; changed comments; public author evidence and its checksums | R537-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |

Requirements and reconstruction order

1. Checked the supplied instruction reference and applicable locations for `AGENTS.md` / `CONTRIBUTING.md`; neither is present in the tracked library tree or applicable ancestor locations. Read README and architecture before inspecting the change.
2. Reconstructed the [issue acceptance](https://github.com/kebag-logic/lwSRP/issues/2) and [manager assignment](https://github.com/kebag-logic/lwSRP/issues/2#issuecomment-6030566128): repair setup; run the real codec suite; demonstrate failures without the fixes; no protocol change; restrict changes to the harness; license new files.
3. Examined the linked test and interface authorities, including `src/include/shish_lan/switch.h:26`, `src/modules/sim_adapter.h`, the adapter implementation, codec header, feature scenarios and codec assertions. The four public switch helpers are inline vtable forwards; the new C exports preserve their signatures and operations.
4. Independently inspected `git diff 19f5796..e4f9995b791489c53b8ccb8a8dc09ec508e32e6b` and history. One commit changes five harness paths. Recorded the source pass in `independent-pass.txt` before reading executable author evidence or prior review findings.
5. Read only the public [author evidence archive](https://github.com/kebag-logic/milan-fpga/tree/d9259a0ea96050549a07044d5a4853a5d376e4da/review-evidence/lwsrptest-r1), its manifest and the manager's public review-start comments. All three published file hashes match the archive manifest. The author's `ad6199083a1eb242f37dacf88de94bd00c4b3658` and the reviewed published commit resolve to the same tree. No private author material or another reviewer's report informed this verdict or ledger.

Executable results

Fresh base and exact-head archives, dependencies, builds and reversal copies reside only in disposable scratch. cgreen 1.7.0 came from its public release archive, verified by SHA256; it was installed only into scratch. Python behave 1.3.3 was already available. Every subprocess was awaited in the foreground with a 540-second limit. Compilation used `make -j16`; builds did not overlap. Independent read-only evidence collection and the final binding/integrity probes ran concurrently. This follows the final foreground-only execution instruction; no background jobs or notifications were used.

| Check | Result | Receipt |
| --- | --- | --- |
| Dependency-complete base build | Configure/build exit 0 | `receipts/baseline-configure.log`, `baseline-build.log` |
| Base CTest | Exit 0 despite zero tests/assertions in its one registered target | `receipts/baseline-ctest.log` |
| Base behave | Exit 1: missing `shlan_connect`; 3 scenarios and 10 steps untested | `receipts/baseline-behave.log` |
| Exact-head build | Configure/build exit 0 | `receipts/head-configure.log`, `head-build.log` |
| Exact-head CTest | Exit 0; 1 target, 9 cases, 1,690 passes | `receipts/head-ctest.log` |
| Exact-head behave | Exit 0; 1 feature, 3 scenarios, 10 steps passed; none skipped | `receipts/head-behave.log` |
| Remove binding source from the library | behave exit 1: missing `shlan_test_connect` | `receipts/reversal-exports-behave.log` |
| Restore base Python hook | behave exit 1: missing `shlan_connect` | `receipts/reversal-ctypes-behave.log` |
| Restore placeholder unit source | CTest exit 8: `No assertions` rejected | `receipts/reversal-unit-wiring-ctest.log` |
| Substitute an empty runner suite | CTest exit 8: `No assertions` rejected | `receipts/reversal-empty-runner-ctest.log` |
| Change expected packed byte 215 to 214 | CTest exit 8: 1,689 passes and 1 failure | `receipts/reversal-assertion-ctest.log` |
| Binding forwarding | All four correct callbacks; pointer/return preservation; both port wrappers cover 0–255; 100 real-adapter cycles including 0/47/48/255 | `receipts/binding-forwarding.log` |
| No cgreen dependency | Head configuration exits 1, preventing silent omission; base configuration and library build exit 0 | `receipts/head-no-dependency-configure.log`, `base-no-dependency-build.log` |
| Zephyr source-list isolation | Minimal API stub builds the unchanged seven-source archive without cgreen; no `shlan_test_*` symbols | `receipts/zephyr-glue-build.log`, `zephyr-glue-symbols.log` |
| Standalone Release library | Four `shlan_test_*` exports remain; `BUILD_TESTING=OFF` is unused | `receipts/release-library-configure.log`, `release-library-symbols.log` |

Each command receipt has a matching `.rc` file. Published command output is unchanged except absolute-path normalization and a license/command header; original streams remain private to scratch. The portable `review.py` reproduces these checks from a supplied checkout; `binding_probe.py` is the separate binding test.

Finding R537-S1

- Severity: SUGGESTION.
- Attributable lenses: Robustness, Docs.
- Location: `CMakeLists.txt:29`, `CMakeLists.txt:38`, `CMakeLists.txt:44`.
- Authority/evidence: the README describes the host shared-library/test build and lists cgreen as a dependency; the embedded path returns at line 16 before all host test wiring. The Release probe confirms the host target includes all four test exports, requires cgreen at configuration, and does not implement `BUILD_TESTING`. The Zephyr source-list probe confirms those exports and dependencies are absent there.
- Impact: a consumer treating the standalone host target as a production library receives extra test entry points and must provide a test dependency to configure. There is no new runtime cgreen dependency on `libshlan` itself. This is an integration limitation, not a failed frozen acceptance item: the documented host build is the test/simulation route, and the existing embedded route remains isolated. An unconditional claim that bindings never enter any production build would be inaccurate.
- Suggested outcome: if a supported standalone production configuration is desired, introduce an explicit testing option, condition the test bindings and unit dependencies on it, and document the two configurations. No change is required for this issue's acceptance.
- Verification for that follow-up: a fresh library-only configuration succeeds without cgreen and exports no `shlan_test_*`; the testing configuration still passes nine cases/1,690 assertions, all three scenarios, and the five reversals.

Documentation assessment and real limits

The new comments and PR explanation correctly describe the missing-inline-symbol cause, forwarding bindings, unit runner, counts and failure propagation. The architecture directory listing has not been updated for the deleted placeholder and two added files; retain the precise prose-only correction below. Other existing architecture text describes parser/protocol scenario coverage that the unchanged tests do not provide. Those coverage inaccuracies predate this harness-only change; this review does not adopt their broader conformance claims. Current tests establish codec helper behavior and simulated port-operation return codes, not full MRP/MSRP/MVRP/MMRP compliance or hardware behavior. The existing scenario state assertions are return-code proxies. The adapter forwarding probe adds direct dispatch coverage, not real port-state or packet-network coverage.

The Zephyr probe checks the source selection and compiles it through minimal build API stubs; it is not a full embedded SDK build. The empty-suite guard was exercised with cgreen 1.7.0. No full parent banks, programmable-logic tools, hardware, physical calibration, containers or deployment actions were run. The cited archive contains author harness evidence, not independently inspected manager parent-bank receipts; any manager source-bank result remains separate evidence and does not establish a final current-development candidate.

Final source integrity

`receipts/integrity.txt` verifies all 34 tracked file blobs from actual disk bytes, executable modes, exact index entries, HEAD and tree; the built exact-head archive also matches those source bytes and modes. The worktree has no tracked, staged or untracked changes. No source checkout mutation was needed: all reversals used separate archived copies. This standalone tree has zero submodule gitlinks, so no parent submodule state is inferred. `src/` is byte-identical to the base; the two new files have the required first-line license identifier; added source text passes the scoped publication scan.

Public review reconciliation and manager duties

The own verdict and five-lens ledger were written before reading the [public internal review](https://github.com/kebag-logic/lwSRP/pull/3#issuecomment-6030780352), which arrived during this review. All four of its findings are explicitly retained at this exact head below; none is silently closed. New disposable probes independently confirmed its two scenario blind spots and missing-prototype warnings. These suggestions do not indicate an incorrect binding at the reviewed head: direct vtable checks pass there.

| Prior ID | Severity and all attributable lenses | Location / artifact | Authority and evidence | Impact | Required or suggested outcome | Verification / disposition |
| --- | --- | --- | --- | --- | --- | --- |
| R536-1-01 | RESIDUE; Docs | `doc/architecture.md:71` and `doc/architecture.md:74` | Current directory prose still lists the deleted placeholder and omits the new runner and binding file; checked against the full change list | Prose file listing only; no test, code, metric, clause or conformance claim is changed by the correction | Exact fix: replace `    │   └── placeholder.c` with `    │   └── main.c                 cgreen runner for mrp_pdu_suite`; after the `environment.py` entry insert `        ├── switch_bindings.c       ctypes test bindings for switch.h inline helpers` | RETAINED; manager carries to residue checklist. Read the later listing and confirm both additions and the removed placeholder |
| R536-1-02 | SUGGESTION; Tests, Robustness | `tests/features/steps/switch_steps.py:26`, `tests/features/steps/switch_steps.py:33`; binding functions | Own `receipts/prior-disable-dispatch-behave.log` and `prior-connect-noop-behave.log`: mapping disable to enable or making connect a no-op still passes all scenarios | Existing return-code proxies miss some binding mistakes; current binding correctness is separately verified | Optional follow-up: make connection/port state observable and assert the resulting state in scenarios | RETAINED; both mutations should make behave fail after that follow-up. No scenario strengthening is required by frozen acceptance |
| R536-1-03 | SUGGESTION; Robustness, Docs | `CMakeLists.txt:38` and `CMakeLists.txt:45` | Own Release, missing-dependency and embedded source-list receipts; same issue as R537-S1 | Standalone library configuration includes test exports/dependency; embedded path is isolated | Optional supported library-only test switch and documentation, as specified in R537-S1 | RETAINED and mapped to R537-S1; no duplicate action item. Test OFF excludes symbols/dependency; test ON retains passing suites |
| R536-1-04 | SUGGESTION; Tests | `tests/features/switch_bindings.c:6`, `tests/unit/main.c:5`, `tests/unit/mrp_pdu_test.c:139` | Own `receipts/prior-prototypes.log`: extra `-Wmissing-prototypes -Wstrict-prototypes` check exits 0 with five missing-prototype warnings | No warning under current repository flags; independently declared interfaces can drift without compile-time checking | Optional small test header for the suite factory and binding prototypes, used by their definitions/callers | RETAINED; the extra strict-prototype check should then emit no such warnings |

The public snapshot records zero check runs, zero workflow runs and zero commit-status contexts. The combined-status endpoint labels that empty set `pending`; it is neither an executed success nor a skipped job. There are no exact-head hosted contexts to treat as evidence. At collection the issue had three comments, the PR had the two start notices plus the internal review, and there were zero formal reviews or inline comments. No additional manager execution-evidence comment was present. `receipts/public-snapshot.json` records the URLs, counts and collection time. The repository coding-style guide was also cross-checked: the two new C files introduce neither control flow requiring braces nor enums.

The manager retains publication, hosted/local workflow acceptance, both independent-review requirements, the final current-development integration candidate and merge. Carry R536-1-01 to the residue checklist; optional suggestions remain follow-up decisions. Source base `19f5796` and live development `910f338dbd050f4efd2d96991ddcf928a583d55f` must remain distinct from this standalone reviewed head. Physical calibration is NOT RUN; skipped field checks are not hardware proof.

R537-1 FINISHED
