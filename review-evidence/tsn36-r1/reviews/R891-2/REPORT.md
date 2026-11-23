[R891] POSITIVE - exact head 55852269db3554900d2b71e6f9a7b153cff69e14

All five lenses are CLEAN for this delta re-review. R891-1-F1 (MINOR) and R891-1-F2 (RESIDUE) are resolved. No open BLOCKER, MAJOR, MINOR or RESIDUE remains. One publication suggestion is recorded below.

This verdict covers the test-only salvage in [tsn-c-stack PR #36](https://github.com/kebag-logic/tsn-c-stack/pull/36), not completion of the platform discovery fix. Head tree: `64ee38ee54fec8de8fb847df31e54d087a7b50ef`. Source base: `715589c1db7cf67e2f3259fd7083ebc7f0923376`. Prior reviewed head: `61a504eec3ec3de828ccd80076212533ef58644b`.

## Reconstruction and scope

The supplied operating instructions, CONTRIBUTING.md and coding rules were read first, followed by README.md and the verification, requirement, traceability and ADP port sections. This tree has no tracked AGENTS.md or docs/README. CONTRIBUTING requires a failing assertion, runnable plant, unchanged coverage ratchet, neutral public wording and two independent positive reviews.

Next came [issue #970](https://github.com/kebag-logic/milan-fpga/issues/970), its body and three public comments. The [frozen ruling](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7080789556) supersedes the earlier shortened-delay proposal. Startup retains 0–2,000 ms; other delay draws retain 0–4,000 ms. The stack salvage is the assertion and plant for GM_CHANGE in WAITING. The wider acceptance still requires discovery within the declared time at both platform sizes, both grandmaster orders, the FR_NFR derivation and bench reruns; the boot-path fix belongs to #972.

Authorities examined were ADP-02 and MFDISC-01, the pinned [FR-DISC source rows](https://github.com/kebag-logic/milan-fpga/blob/5603c353137e90c1fa95429f6d00ef7a2298d9ee/docs/reference/FR_NFR.md#L187), PORTING.md:166–206, and the unchanged ADP header/core. Milan v1.2 5.6.3.5.7 and Tables 5.49–5.51 govern the transition and delay; IEEE 1722.1-2021 6.2.4.2.2 supplies the distribution rule under the frozen ruling. This is a delta conformance check against those public authorities, not a fresh full-standards audit or statistical proof of uniformity.

The complete base-to-head diff and two-commit history were then inspected, followed by public executable evidence. The round delta changes six files: the assertion, mutation registry and four documents. Production source, headers, constants, examples, scripts, build definitions, configuration and CI are identical to the source base. The correction commit has a one-line subject and no body/trailers. Receipts: [base-head.diff](base-head.diff), [round-delta.diff](round-delta.diff).

The independent conclusion and five-lens ledger were written in [independent-verdict.md](independent-verdict.md) before opening prior public findings. The [prior R891 findings](https://github.com/kebag-logic/tsn-c-stack/pull/36#issuecomment-7083242024) were then reconciled at their causes. The other prior public review identifies no additional open finding; formal review and inline-comment collections were empty. Untouched code retains its previous lens coverage.

## Delta assessment

At tests/test_adp.cpp:138, A2 captures `const uint32_t draws = a.draws;` immediately before `adp_gm_change(&a)`. Lines 140–143 require:

- DELAY state and exactly one fresh draw: `a.draws == draws + 1u`;
- `ADP_DRAW_DELAY`;
- equality of the callback's armed delay and the recorded draw;
- the independent literal bound `4000u`.

The fixture reaches WAITING through accepted advertisements before this call. The existing following expiry, send and configuration assertions remain. The unsigned count matches the documented modulo-2^32 diagnostic contract. In unchanged src/adp.c:51–61, only the actual draw advances this count and records its kind/value; enter_delay at lines 81–85 arms that draw. Thus the new conjunct rejects reuse of the previous draw even when its kind and value satisfy all older checks.

The plant at tests/mutations.json:378 replaces precisely the WAITING call with re-arming `last_draw_ms` and entering DELAY, without a draw. Its original fragment matches exactly once. Its registered kill is A0toA2Schedule's owned A2 message. The earlier wrong-startup-kind plant remains registered at line 363. Both compile and fail the named assertion; a build error is never credited as a kill.

No RTL, mailbox, register interface, layout, timing constant or submodule input changes. This portable stack has 100 tracked blobs and zero gitlinks. The RTL lens is clean by this verified unchanged boundary; no new RTL simulation or hardware result is claimed.

TESTS.md and TRACEABILITY.md contain only the intended added plant and shifted line anchors. Their executable generators pass in check mode. VERIFICATION.md correctly states 475 core plants plus four generated configuration plants, 479 total. CHANGELOG.md:5 removes the prior reviewer reference and accurately describes both plants. No new source comment introduces a lane, round, reviewer or issue-comment identifier; the plant retains its existing clause comment. Existing unrelated comment residue remains outside this delta under #746.

## Executable evidence

All independent campaigns completed before this report. Commands ran as foreground-owned processes with bounded concurrent workers, no detached shell jobs, and no more than 16 requested compiler/build slots. Disposable copies and builds are confined to scratch/. No reviewed source file was edited.

| Check | Result | Receipt |
|---|---|---|
| Full `validate.py --jobs 2 --graphs` at head | 28/28 gates rc 0; GCC and sanitizer suites pass; coverage ratchet passes; static analysis, report controls and graphs pass | [gates.json](receipts/validate/gates.json), individual logs/rc files in receipts/validate/ |
| Full mutation campaign | 479 CAUGHT, 0 ESCAPED, 0 ERROR; both GM_CHANGE plants caught | [mutation.log](receipts/validate/mutation.log), [results.json](receipts/validate/mutations/results.json) |
| Registered no-draw and wrong-kind kills | Each XML records one executed test, one owned assertion failure, zero disabled tests/errors | receipts/validate/mutations/gm-change-rearms-without-a-draw/ and gm-change-draws-startup-kind/ |
| Independent clean/plant comparison | Clean head passes all 39 ADP instances in Debug and Release; no-draw passes prior head in both configurations; both plants fail A2 at current head in both | [probe/results.json](probe/results.json) and eight logs |
| Prior-head no-draw full suite | All 10 binaries pass: the plant escapes at 61a504ee | [old-ctest.log](receipts/old-ctest.log), [old-full.rc](old-full.rc) |
| `baremetal.py --jobs 2` | Debug and Release build, link, audit and execute smoke checks; no unresolved final symbols | [RV32 results](receipts/baremetal/results.json), build/smoke logs |
| Documentation and assertion ownership | 459 instances across 10 binaries; 185 declarations; 47 requirements; 479 plants; generators and needle controls pass | traceability.log, test-inventory.log and needles.log in receipts/validate/ |
| Exact tracked state | All 100 blob bytes, modes and index entries match head; clean status; no gitlinks | [integrity-after.json](integrity-after.json) |

The independent probes initially encountered a dependency-header warning because their include path was not marked as a system header. The final portable probe uses system-header treatment matching the repository build. An initial standalone needle check lacked the required compiler on PATH; the complete validation used the pinned dependency environment and passed. Neither setup failure is counted as a product failure or a successful plant kill.

The reviewer RV32 Release ELF hash is `a9cc5f9e2e3c0ad506ea1d232774b0d2813bd186081334bd9e86ce42c2849cd0`, identical to the published prior-head Release result. Debug hashes include build-path differences and are not asserted identical.

The supplied [public packet at f6dd644d](https://github.com/kebag-logic/milan-fpga/tree/f6dd644d37fe4035aa263fc05e8da3524f3c3fcc/review-evidence/tsn36-r1) contains author receipts for 61a504ee: 28 passing gates, 478 caught mutants, and RV32 Debug/Release. Four selected receipts match the published SHA-256 manifest exactly ([verification](public-evidence-verification.json)). Those receipts are not relabelled as execution at 55852269. The current PR body claims 28 gates and 479 kills at the new head; no linked raw author packet for that head was found. The independent executions above establish those results directly.

The supplied packet commit is reported as unsigned, and no detached signature was located. A hash match is not signature verification; no signed-packet verification is claimed. See [public-packet-commit.json](public-packet-commit.json).

At the last hosted observation, [push quality job 137527948897](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45125236796/job/137527948897) completed successfully, including the actual portable-core validation step and artifact upload. PR quality was still running and both bare-metal jobs were queued. These are executed versus pending states, not skipped jobs counted as passes. [Steps](hosted-quality-steps.json) and [final snapshot](hosted-final.json) preserve that distinction. Hosted/act acceptance belongs to the manager.

## Findings and reconciliation

**R891-1-F1 — MINOR — Tests, Conformance — RESOLVED.**  
Artifact: tests/test_adp.cpp:138–143; tests/mutations.json:378–389. Authority: frozen #970 salvage, MFDISC-01, Milan 5.6.3.5.7 and CONTRIBUTING's assertion/plant requirement. The original impact was an unobserved missing per-event draw. Required outcome was a count increment assertion, registered no-draw plant and updated generated records/count. All are present. Verification: independent old-head escape/current-head kill in Debug and Release, full prior suite escape, registered owned-message failure, and all 479 campaign kills. No residual unclean lens.

**R891-1-F2 — RESIDUE — Docs — RESOLVED AS WRITTEN.**  
Artifact: CHANGELOG.md:5. Authority: CONTRIBUTING's neutral public wording rule. The original wording-only defect was `, review finding R887-1-F1`. The exact required deletion is present; the issue link and unchanged-behaviour statement remain. Verification: the round diff and an empty reviewer-round-pattern search in CHANGELOG.md. No measurement, code or clause claim was changed by this cleanup.

**R891-2-S1 — SUGGESTION — Tests, Docs — publication follow-up.**  
Artifact: PR #36 validation table and supplied public evidence directory. Authority/evidence: the review's evidence-reuse requirement, packet manifest, unsigned commit metadata and PR body. Impact: the exact-head claims could not be audited from linked author receipts alone, requiring independent execution. Suggested outcome: link the exact-head author receipts and identify any intended signed packet; otherwise describe the available packet as hash-verified. Verification: links resolve to receipts bound to 55852269/tree 64ee38ee, with matching published hashes and an explicit signature status. This does not invalidate the independently reproduced results or leave a lens unclean.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #970 ruling; ADP-02/MFDISC-01; pinned FR-DISC rows; PORTING counters; A2 fresh-draw assertion; unchanged draw implementation and constants; plant reversal | R891-2 delta and F1 closure; untouched R891-1 coverage retained | 55852269db3554900d2b71e6f9a7b153cff69e14 |
| RTL | CLEAN | Complete diff/path inventory; unchanged production, headers, build inputs and interfaces; zero gitlinks; RV32 identity/results | R891-2 boundary verification; R891-1 untouched coverage retained | 55852269db3554900d2b71e6f9a7b153cff69e14 |
| Robustness | CLEAN | WAITING precondition; unsigned count and literal bound; unique plant match; Debug/Release probes; sanitizer and RV32 results | R891-2 delta; R891-1 untouched coverage retained | 55852269db3554900d2b71e6f9a7b153cff69e14 |
| Tests | CLEAN | 28 gates; 479 named kills; both GM_CHANGE XML reports; old full-suite escape; Debug/Release sensitivity; coverage and report controls | R891-2 delta and F1 closure | 55852269db3554900d2b71e6f9a7b153cff69e14 |
| Docs | CLEAN | Four changed documents; generator checks; count reconciliation; PR claims; source-comment scan; exact F2 deletion | R891-2 delta and F2 closure; R891-1 untouched coverage retained | 55852269db3554900d2b71e6f9a7b153cff69e14 |

## Limits and manager duties

These are source-head checks on the available host dependency environment. They are not a manager source bank, and no manager source bank is inferred. No parent, processor, gPTP, synthesis or builder bank ran. No hardware was accessed; physical calibration was NOT RUN. Field skips are not hardware proof.

The manager must obtain the required independent positive reviews, complete hosted/act acceptance, and validate the actual current-dev merge candidate with builder and native banks at the merge turn, publishing its receipts on the PR. Source base 715589c1 and live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` remain distinct. Any parent pin update needs its own validation. The wider #970 derivation, grandmaster-order/platform obligations and affected bench reruns remain with the parent work and #972.

No source fixes, commits, pushes, GitHub writes, merges, author contact, sub-agents or restricted private material were used. Final tracked bytes/modes/index equal the exact head; there are no required submodule gitlinks. The reviewer packet contains portable probe, reproduction, collection and integrity scripts. Text receipts preserve output with local path prefixes redacted; receipt-copy-record.json records original and published hashes. Publish only REPORT.md and MANIFEST.sha256-listed files; scratch/ is excluded.

R891-2 FINISHED
