[R896] POSITIVE - exact head 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7

Independent external review, round R896-1, issue #973 / PR #978.
Tree: `0fe791d5c539f4100e312f17e469a2a9a50bc006`.
Reviewed range: `dd163e41..9a71daa9aa2379e2a57eb93ccafe83101bcb37f7`.

No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION was found. The scoped source change satisfies #973. This is a source-review verdict, not merge authorization or hardware qualification.

The independent assessment and ledger below were written before the public prior-finding reconciliation. No other reviewer's report was read.

## Contract and implementation

Read AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #973](https://github.com/kebag-logic/milan-fpga/issues/973) and its TAKEN/REVIEW READY comments, REQUIREMENTS.md sections 1, 7 and 8, the SRP adapter contract, mailbox register/event-coalescing contracts, and the split control-memory ledger. The issue ties port lifecycle behavior to IEEE 802.1Q-2018 10.7 and 35.2. This verdict applies that existing project contract; it does not claim a fresh audit of every state-machine clause or full standards compliance.

The loop dispatches queued LINK records at `ctrl_loop.c:137-157`; the later SRP poll independently reads the current LINK register. The base poll could see a new UP before its record was dispatched. It reset the interface and set `link_seen`, making the eventual first LINK UP take the repeated-UP reset path. The host reproduction exposes both resets and startup-participant loss.

`srp_mbx.c:1231-1233` records the LINK value accepted by SRP's own sink. The poll at `:1284-1286` allows UP only while the carried level is UP, retaining the raw register's immediate DOWN. Attach initializes both levels from the same sample at `:1472-1474`. The existing reentry guard encloses these updates; no second state owner is introduced.

The first UP deliberately resets zero times, preserving already-clean participants; a subsequent UP after DOWN resets once. That implements the issue's startup-preservation intent, explicitly described in REVIEW READY. A repeated UP after prior activity remains meaningful for coalesced transitions and still resets.

The carried level intentionally survives `reset_interface`: when a raw DOWN's held record disappears on recovery, the last carried UP permits recovery. The existing `CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` test checks this exception and old-input fencing. A dispatched DOWN does clear `link_carried`, preventing an early raw UP from starting an extra reset.

Other raw-level consumers were inspected: `adp/adp_mbx.c:44-47` supplies ADP's enable-time sample (`third_party/tsn-c-stack/src/adp.c:238`); subsequent transitions use LINK events. `maap/maap_mbx.c:273` samples at attach. Neither duplicates SRP's poll-time reset pattern. No mailbox ABI, timer, CDC, RTL, CPU bound, loop source or coverage ratchet changes in the reviewed range.

## Five-lens results

[R896] PASS Conformance - `sw/firmware/ctrl/srp/srp_mbx.c:1226`, `:1286`, `:1474`; #973 acceptance; `receipts/base-*.log`, `head-*.log` - confirmed the cause, startup preservation, single later-UP reset and retained fail-closed DOWN. Memory and CPU evidence below covers the other acceptance criteria without moving bounds.

[R896] PASS RTL - `sw/firmware/ctrl/srp/srp_mbx.h:68`; `srp_mbx.c:1160-1235`, `:1273-1319`; `loop/ctrl_loop.c:137-157`, `:289-331`; `docs/design/MAILBOX_SPLIT.md:182`; published platform-image comparisons - inspected serialization, interface indexing, attach/reset ownership, delayed rebuilding and dependent structure offsets. No RTL/crossing delta exists. Dependent objects reflect 8x8 structure-offset changes; published SRAM totals and tile allocations remain unchanged.

[R896] PASS Robustness - `sw/firmware/ctrl/test/srp_link_pass.cpp:77-135`; `srp_mbx.cpp:1004-1096`; `srp_app.cpp`; `receipts/head-8x8-2if.log` - exercised four UP phases, first/later UP, DOWN revocation, held-event recovery, reattach already UP, reentry refusal, malformed input, allocation/refusal paths and composition callbacks. Complete SRP mailbox/composition suites passed at both shipping shapes and 8x8/2if.

[R896] PASS Tests - `sw/firmware/ctrl/test/srp_link_pass.cpp:43-49`, `:87-135`; `srp_link_mutants.py:34-59`; `srp_mutants.py:19-34`, `:960-999`; `test_ctrl_firmware.py:212`, `:222-245`; `receipts/plants-*.log` - reset counting observes LICENCE writes independently of the participant-pointer check; outgoing declarations are also checked. Base fails in the intended diagnostic. All seven compiled plants fail the named assertion; compilation failures do not count as kills. Campaign wiring includes all three specified shapes.

[R896] PASS Docs - `sw/firmware/ctrl/srp/README.md:111-120`; `CHANGELOG.md:62-67`; public PR/issue evidence; `receipts/docs.log`, `em-dash.log`, `public-audit.log` - final behavior, attach exception and limits are documented. Added source comments describe behavior/reason and reference #973; no new bench label, lane name, review identity/round or issue-comment ID was found in them. Documentation gates pass.

## Reviewer execution

`run_focused.py` uses disposable sources/builds only beneath `scratch/`, four concurrent tasks and three compile jobs each (at most twelve compile workers). Foreground parent commands remained attached until completion. The clone's tracked sources were never edited.

| Check | Result | Receipt |
|---|---|---|
| Phase suite against base production SRP, 1x1/1if and 8x8/1if | Expected FAIL at AfterTheEventsBeforeSrpsPoll at each point; other three tests PASS | `receipts/base-*.log` |
| Exact-head phase suite | 4/4 at 1x1/1if, 8x8/1if and 8x8/2if | `receipts/head-*.log` |
| Exact-head complete SRP mailbox suite | 84/84, 84/84, 85/85 respectively | same |
| Exact-head composition suite | 8/8, 8/8, 10/10 respectively | same |
| Seven link plants | 7/7 killed at 1x1/1if, 8x8/1if and 1x1/2if; zero escapes | `receipts/plants-*.log` |
| Docs wording/privacy and added-line em-dash | PASS | `receipts/docs.log`, `em-dash.log` |
| Both flip checks, load and shape checks | PASS | `receipts/flip-*.log`, `load.log`, `shape.log` |
| Diff whitespace | PASS | `receipts/diff-check.log` |
| Raw tracked bytes/kinds/modes/index and required gitlinks | PASS | `receipts/integrity.log` |

Total unplanted exact-head host tests: 291. Baseline and planted failures are expected negative controls. Initial budget commands used the documentation interpreter, which lacks PyYAML; setup failures are retained in `receipts/setup-*.log`. Successful reruns used the existing configured Python environment, with no installation or source change.

Published logs retain captured output with only local checkout/packet paths replaced by `<checkout>`/`<packet>`. `finalize_packet.py` preserves original bytes under the unpublished `scratch/raw-receipts/` and creates `MANIFEST.sha256`. Only manifest-listed files and REPORT.md form the publication set.

Reproduce from the exact-head checkout, with the installed test-library include/library directories configured:

```sh
python3 /path/to/packet/run_focused.py
REVIEW_DOCS_PYTHON=/path/to/documentation/python3 python3 /path/to/packet/run_checks.py
python3 /path/to/packet/audit_integrity.py
```

## Published source evidence

Source: [public packet at 62593bf0](https://github.com/kebag-logic/milan-fpga/tree/62593bf0adb29cb13e2f1ebaa95c76c496f5cdf0/review-evidence/973-r1/author-r1/receipts). `receipts/public-audit.log` identifies 28 examined artifacts and verifies their published SHA-256 values. These are author source receipts. No manager source bank ran at this head; none is inferred.

Most gates ran at `862fd41cfc292d07480f0e6bb4b5dd5e0c42e2ea`. `git diff 862fd41c HEAD` confirms only a docstring rewrap follows: production bytes, test execution and mutation definitions are unchanged. Docs steps ran at the exact final head. Reviewer checks above ran at the exact final head.

The four firmware shard receipts report 77/77 suite verdicts, 826/826 control plants, 385 AECP and 564 SRP `[ok]` entries, zero escapes. These are selected gate output/summary receipts, not the full private campaign logs. Coverage self-test/check passes over 40 files. Twin, twin-plants, twin-maps and twin-maps-plants exit zero; the comparator reports zero findings, retaining documented placement differences. Split boot simulation passes both shapes with six native controls and six plants. Docs steps report 104/104 and no tracked changes. Builder legs pass with explicit NOT RUN rows; those rows are not hardware evidence.

| Platform point | Base ROM B | Final ROM B | Growth B | SRAM B, unchanged | RAMB36, unchanged |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 126432 | 126448 | 16 | 56736 | 45 |
| 1x1/2if | 128032 | 128056 | 24 | 59040 | 46 |
| 8x8/1if | 139208 | 139216 | 8 | 98160 | 58 |
| 8x8/2if | 140784 | 140800 | 16 | 115504 | 63 |

The superseded loop form grew 8x8/1if ROM by 104 B to 139312, requiring 58.5 RAMB36 and failing its 58-tile ledger. The final form fits. `ctrl_loop.c`, `ctrl_loop.h` and `coverage.ratchet` are independently verified byte-identical to `dd163e41`. Published image comparisons show only `srp_mbx.o` changes at 1x1; other changed 8x8 objects carry structure offsets/strides, which were inspected. Final 8x8/1if ROM has 48 B before the next half-tile.

Published CPU runs cover ten groups at both points before/after, with zero refusals, budget misses or passes beyond the share. Independently parsed 88 paired 1x1 and 86 paired 8x8/1if probes: all fit, zero verdict changes, largest absolute rounded differences 0.438 ms and 0.146 ms. Independently rerun graders retain 1x1 load 0.511, last queued notice 127.31 ms, ACMP 29.06 ms, txL 47.88 ms; 8x8/1if load is 0.744 against 0.75. The latter point's reported analytic rows are not held bounds; measured rows are supported by the published CPU-run evidence.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #973; srp_mbx.c LINK/poll/attach; baseline/head tests; memory/CPU receipts | R896-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| RTL | CLEAN | srp_mbx.h/c; ctrl_loop.c; mailbox contract; linked-image comparisons | R896-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| Robustness | CLEAN | srp_link_pass.cpp; srp_mbx.cpp; srp_app.cpp; three exact-head shape logs | R896-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| Tests | CLEAN | srp_arms.py; srp_link_mutants.py; srp_mutants.py; test_ctrl_firmware.py; 21 kills | R896-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |
| Docs | CLEAN | SRP README; CHANGELOG; PR/issue evidence; docs/em-dash; manifest audit | R896-1 | 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 |

## Prior public findings

After writing this verdict and ledger, read the PR conversation, formal reviews and inline review threads. The conversation contains the two manager review-start notices; formal reviews and inline threads are empty. There are no prior published findings on PR #978 to resolve or retain at this observation. Receipt: `receipts/pr-prior-findings.json`. Related-issue decisions were considered as authorities, not as findings on this PR.

## Limits and pending manager duties

- A DOWN inside a pass can reset at the raw read and again at its record. This pre-existing, disclosed behavior precedes rebuilding and is outside #973's UP acceptance. No general exactly-one-reset claim for DOWN is approved.
- Illegal callback reentry can discard LINK; the existing guard counts/refuses it. No new delivery guarantee for unsupported reentry is claimed.
- [#970's ruling](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7080789556) retains full ADP delay ranges. This head leaves ADP and the stack unchanged. [#972's manager decision](https://github.com/kebag-logic/milan-fpga/issues/972#issuecomment-7083292610) requires effective link qualification from reset, beyond the arm's DOWN publication. #973 does not discharge that separate work. Its carried-level logic accepts the resulting DOWN/UP sequence; actual composed boot behavior needs candidate validation.
- Source baseline is the reviewed flip head `dd163e41`. No current-dev merge candidate was built here. The manager must validate the candidate against current dev, identified in the handoff as `e275d7950ef3385753e6a15d2e191ba855b171ed`, and publish exact-candidate builder/native receipts. Narrow ROM headroom makes composed image checks material.
- Hosted observation at this SHA found docs/elaborate in progress and rtl-fast/rtl-full queued. These are not successful contexts or executed exhaustive evidence. Hosted/act acceptance remains the manager's. No act, Docker, full parent/processor/synthesis/builder bank or hardware run was performed here.
- Physical calibration is NOT RUN. The builder's platform-specific skipped control and missing physical-report row do not prove the excluded measurements. Host tests, twin receipts and CPU simulation do not establish physical link, timing or audio behavior. The manager owns the bench rerun after merge.
- Merge still requires the other independent positive review, no round in flight, exact-candidate gates, required hosted acceptance, explicit authorization, containment, and issue/project completion.

R896-1 FINISHED
