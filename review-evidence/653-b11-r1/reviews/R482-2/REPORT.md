[R482] POSITIVE - exact head 6b83de0009673ce2c438985a0f9720f079a3715d

# R482-2: internal independent re-review of PR #659 (Refs #653), lane B11 bench findings, round 2

- Head: `6b83de0009673ce2c438985a0f9720f079a3715d`, tree `2f5399e4b187d30847191e13743b36cad9aeb63b`. Two commits on dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`: `6f76d612` (round 1, reviewed NEGATIVE by R482-1 and R483-1) and `6b83de00` (round 2).
- Diff from base: `docs/findings/653_DISCONNECT_ORDER_BENCH.md` (new) and one row in `docs/findings/README.md`. The round-2 delta `6f76d612..6b83de00` changes only those two files, +51/-14 lines. It touches no HDL, test, script, gitlink or generated artifact (`receipts/clone_integrity.txt`).
- Reconstructed from:
  - AGENTS.md and CONTRIBUTING.md.
  - The #653 body and acceptance 1-4.
  - The lane comments on #653: the STOP, the ruling, the B11 assignment, TAKEN, both REVIEW READY comments and the round-2 assignment 5983716764.
  - The live PR body and the PR template.
  - The diff and history.
  - The public evidence: `review-evidence/653-b11-r1/author` and `author-r2/round2/` on branch `653-b11-review-evidence` at `9bb441d3`, which contains `980c5784`.
  - The upstream controller library source, fetched independently.
- Prior public findings, which I read only after my own pass over the delta: R482-1 F1, F2, S1 and S2. Each is resolved below. I did not read the other reviewer's round-1 or round-2 report before writing this verdict; only the assignment's one-line summary of it.

## Verdict

Both round-1 MINOR findings are fixed at this head. Neither fix changes any measurement, figure or capture.

- **The library's counter check.** I fetched the upstream library at tag `v4.3.1.1`, which resolves to tag object `080ab851` and commit `6d61a92e`.
  - `src/controller/avdeccControllerImpl.cpp:1611-1613` is exactly the condition the page states. The Milan flag is removed only when MEDIA_LOCKED is neither MEDIA_UNLOCKED nor MEDIA_UNLOCKED + 1.
  - The enclosing function, `updateStreamInputCounters` (`:1590`), has no connection-state term.
  - That function is the only path that stores a STREAM_INPUT counters update. Its four callers are `DelegateOverrides.cpp:787`, `Handlers.cpp:528`, `Handlers.cpp:2484` and `Overrides.cpp:3681`.
  - The copied header hashes to `3d09fa69...`, the same as the tag's copy.
  - The condition is also identical in every public release from v3.2.4 through v4.3.1.1, and at the upstream dev head `a3a62926` (`receipts/lib_scan.txt`).
  - So the page's conclusion holds: the owner's flag cannot come from this check, and the Hive layer is the open gap. That stays true even though the owner's library version is unknown.
- **The library's view of the counters.** I re-derived this from the raw probe logs. Every STREAM_INPUT counters update the library delivered in s0b and s1 was one of three kinds, 23 of each: 0/0 while Connected, 1/0 while Connected, or 1/1 while NotConnected. All three pass the check.
  - In R01 and R02 the first update after NotConnected arrives at +95.000 and +100.016 ms and carries 1/1. So no update reached the library inside either CRF window (`receipts/verify_r2.txt`).
- **The control interval.** I recomputed it from the provided decoder's C0 output. The UNBIND_RX command comes 1,629.836 µs after the probe's own GET_COUNTERS answer, and the response 1,637.340 µs after it. The command-to-response interval is 7.504 µs. The page now pairs 1,629.8 µs with the command and 1,637.3 µs with the response, and 1,629.8 equals the grade's `own_rsp_to_cmd_us`.
- **Nothing measured changed.**
  - All 75 table rows that contain a digit are unchanged between `6f76d612` and the head, except the acceptance-4 verdict cell.
  - Every hash token is unchanged.
  - The per-cycle rows and the capture-hash rows are byte-identical.
  - The only numeric token lost is `5.3.8.10.`, which is a change of punctuation.

The verdict is POSITIVE because no MINOR, MAJOR or BLOCKER finding is open. Two RESIDUE items remain. Both are wording precision in prose and the PR body, and both have exact fixes below.

## Prior findings at this head

| Finding | Status | Evidence at `6b83de00` |
|---|---|---|
| R482-1 F1 (MINOR; Conformance, Tests, Docs): the library's silence was presented as order evidence | **Resolved** | Every required outcome is now in the text:<br>• The condition is stated at `:226-238`.<br>• "Can flag neither order ... nor the CRF input's 1/0 window" is at `:240-246`.<br>• The acceptance-4 cell reads "No miscount flagged by the library; not a test of the order" (`:46`), and the headline is qualified at `:37-39`.<br>• The README row at `README.md:16` is qualified the same way.<br>• The CRF section says that no update arrived inside the window (`:279-287`).<br>• The conclusion that the flag must come from the Hive application is at `:248-249`, and Limits repeats it at `:318-324`.<br>The source cited at `v4.3.1.1` matches what I fetched. I also re-derived the update census and the CRF window myself. |
| R482-1 F2 (MINOR; Tests, Docs): 1,629.8 µs was attributed to the response | **Resolved** | `:260-261` reads "The UNBIND_RX command left 1,629.8 µs after the probe's own GET_COUNTERS answer, and its response 1,637.3 µs after it". Both figures match my recomputation from `summary/decode/b11-a535-s0b-C0.decode.txt`. |
| R482-1 S1 (SUGGESTION): name the identity tool's aggregate FAIL | Taken | `:64` reads "Equal to the build's AEM image, except the three live-state fields below; the scripted gate reports FAIL on exactly those three". `identity/identity-verdict.txt` has exactly three FAIL lines: `aecp-STREAM_INPUT 0` at offset 78, `aecp-CLOCK_DOMAIN 0` at offset 71, and `get-clock-source`. |
| R482-1 S2 (SUGGESTION): the control does not exercise the selection of the unlock's push | Taken | `:266-268` says the control exercises the comparison only. The PR body's limitations section has the matching line. |

## Findings

### RES1 - RESIDUE - Docs - `docs/findings/653_DISCONNECT_ORDER_BENCH.md:235-237` and the PR body's Round 2 table - "one other use of MEDIA_UNLOCKED" omits the JSON name table

- **Evidence:** At the tag, `StreamInputCounterValidFlag::MediaUnlocked` appears three times in `src/` and `include/`:
  - `src/controller/avdeccControllerImpl.cpp:1610`: the check.
  - `src/controller/avdeccControllerImplHandlers.cpp:35`: the mandatory-counter list.
  - `include/la/avdecc/internals/jsonTypes.hpp:833`: the JSON name table.

  Its enum definition is in `include/la/avdecc/internals/entityEnums.hpp:368` (`receipts/lib_scan.txt`, `receipts/verify_r2.txt` NOTE line). The JSON table is not a check, and the bench build left the JSON feature out. So no conclusion changes, but "one other use" is literally incomplete.
- **Impact:** wording only. It changes no measurement, figure, verdict, test or clause claim.
- **Exact fix:** at `:235`, write "The library's one other use of MEDIA_UNLOCKED in its controller logic," in place of "The library's one other use of MEDIA_UNLOCKED,". Make the same change in the PR body's Round 2 table cell ("the library's one other MEDIA_UNLOCKED use in its controller logic lists the mandatory counters").
- **Verification:** re-read the line at the next head. `lib_scan.sh` lists the references.

### RES2 - RESIDUE - Docs - `653_DISCONNECT_ORDER_BENCH.md:25`, `:37`, `:46`, `:319`, `docs/findings/README.md:16` and the PR body - "its one counter check" is unqualified

- **Evidence:** the library has other counter-value checks, at `avdeccControllerImpl.cpp`:
  - `:1543`: AVB_INTERFACE LINK_UP/LINK_DOWN.
  - `:1578`: CLOCK_DOMAIN LOCKED/UNLOCKED.
  - `:1714-1753`: STREAM_OUTPUT.

  `:226` correctly says "one check on a STREAM_INPUT's counter values". The other places shorten this to "its one counter check".
- **Impact:** wording only. The surrounding text names the MEDIA_LOCKED/MEDIA_UNLOCKED condition, and no conclusion changes.
- **Exact fix:** write "STREAM_INPUT counter check" for "counter check" in those places:
  - `:25`: "what its one STREAM_INPUT counter check can detect".
  - `:37`: "Its one STREAM_INPUT counter check accepts either order".
  - `:46`: "The library's one STREAM_INPUT counter check accepts ...".
  - `:319`: "its one STREAM_INPUT counter check cannot flag the order".
  - The README row: "its one STREAM_INPUT counter check accepts either order".
  - The PR body: the same edit in the Description's acceptance-4 cell and in Known limitations.
- **Verification:** re-read the lines at the next head, then run `gen_toc.py --check`, because `:25` is a contents line.

### S1 - SUGGESTION - Docs, Conformance - `653_DISCONNECT_ORDER_BENCH.md:320-324` (Limits) - say the check is the same in every public release

- **Evidence:** `receipts/lib_scan.txt` shows the same condition at v3.2.4, v3.4.1, v4.0.0, v4.1.0, v4.3.0, v4.3.1.1 and the upstream dev head `a3a62926`.
- **Benefit:** this narrows the stated gap "the owner's ... library versions are not known". It shows that the conclusion "cannot come from this library check" does not depend on which library version the owner ran.
- **Status:** optional. It does not affect coverage.

## Evidence per lens

**Conformance.**
- #653 acceptance 1-4 against the page's verdict table (`:41-46`). Rows 1-3 are unchanged from round 1. Row 4 now claims only "no miscount flagged", which is all a check with this condition can support.
- The library's citation string "Milan 1.3 - 5.3.8.10" and its message are quoted exactly as written at `:1613`.
- The conclusion at `:248-249` follows from the condition. It also holds in every public release (`receipts/lib_scan.txt`).
- The round-2 assignment's items 1-4 are each met:
  - Item 1: the receipt is cited, the condition stated, acceptance row 4 and the CRF section qualified, and the conclusion drawn.
  - Item 2: the control intervals are paired with their frames.
  - Item 3: the identity row is reworded and the PR body is in the template's sections.
  - Item 4: live dev is still the base, so no merge was needed.

**RTL.**
- `git diff --name-status 6c22d3ca..6b83de00` shows two Markdown files. There are no HDL changes and no gitlink changes. The four gitlinks are `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor 631eeb34` and `third_party/verilog-axis 48ff7a7e`.
- The delta makes no new RTL claim. The page's one RTL statement, at `:272-275` (PR #655 counts the CRF unlock at the bind fall, and this image predates it), is unchanged from round 1. Round 1 checked it against `KL_crf_rx.sv` at `bbf704ec`.

**Robustness.**
- **Version.** The library conclusion does not depend on the release: the condition is the same from v3.2.4 to the dev head.
- **Store paths.** It does not depend on how an update arrives: all four store paths go through `updateStreamInputCounters`.
- **The CRF window.** No update arrives inside either window: the first update after NotConnected is the 1/1 one, at +95.000 and +100.016 ms. The page's "95.0" and "100.0" ms are unchanged.
- **Diagnostics.** The library's Diagnostics struct at the tag has no counter-based field, only redundancy, control bounds and MSRP latency. So "no diagnostic" cannot hide a counter rule.

**Tests.**
- **Control evidence.** C0's line order is own answer, then command, then response, then the unlock push. The intervals are recomputed from the decoder's text and agree with the grade.
- **Honesty of claims.** The page no longer presents the library check as a test that could fail for the order. `:244-246` and the acceptance-4 cell say so explicitly. The control's scope is stated at `:266-268`.
- **Unchanged evidence.** No grader, decoder, probe or capture changed. Every hash on the page is unchanged.

**Docs.**
- Docs gates at the head, with the Markdown gates run in the pinned renderer environment:
  - `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base 6c22d3ca` (0 findings over 394 added lines), and `check_doc_paths.py`: all rc 0 (`receipts/docs_gates_md.txt`).
  - Under the system interpreter, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `check_feature_status.py --self-test` are rc 0, as are `git diff --check` from base and from round 1 (`receipts/docs_gates.txt`). The renderer gates are rc 2 there because the renderer is not installed, which is expected.
  - Under the venv, `check_baremetal_only.py --check` is rc 2 only because the venv lacks pyyaml. This is the same split the author's validation section documents.
- The TOC line `:25` and the README row are consistent with the body.
- The PR body has every template section: Status, Linked Issue / roles, Description, Authoritative references, How to get into the same state, How to validate, Known limitations / out of scope, and Definition of Done, plus a Round 2 section. It reads "Refs #653", as the B11 assignment requires, and is byte-equal, apart from the trailing newline, to the author's round-2 `PR-BODY.md` in the evidence branch.
- RES1 and RES2 are wording residue only.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:32-46`, `:226-249`, `:270-287`, `:316-324`; #653 acceptance 1-4; round-2 assignment 5983716764; library `v4.3.1.1` `avdeccControllerImpl.cpp:1590-1615`, `Handlers.cpp:35`; `receipts/lib_scan.txt`, `receipts/verify_r2.txt` | R482-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| RTL | CLEAN | `git diff --name-status 6c22d3ca..6b83de00` (two Markdown files, no gitlink change; `receipts/clone_integrity.txt`); page `:272-275`, unchanged from the round-1 coverage against `bbf704ec:hdl/ieee1722/crf/KL_crf_rx.sv` | R482-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| Robustness | CLEAN | Library store paths (4 callers), condition across v3.2.4 to dev `a3a62926`, Diagnostics struct (`receipts/lib_scan.txt`); CRF window updates in `runs/s1/s1-probe.jsonl` (`receipts/verify_r2.txt`) | R482-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| Tests | CLEAN | `summary/decode/b11-a535-s0b-C0.decode.txt`, `summary/o653-grade.json` `s0b/C0`, `runs/s0b` and `runs/s1` probe logs; page `:251-268`; per-cycle and hash rows round 1 against head (`receipts/verify_r2.txt`) | R482-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| Docs | CLEAN (RES1 and RES2 are residue only) | Whole page at head; `docs/findings/README.md:16`; live PR body against `.github/PULL_REQUEST_TEMPLATE.md`; `author-r2/round2/*` receipts; docs gates (`receipts/docs_gates_md.txt`, `receipts/docs_gates.txt`) | R482-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |

## Real limits of this review

- **The captures.** These pcaps are outside the published evidence. The order and interval figures are re-derived from the published decoder output, the grade JSON and the probe logs, not from the pcap bytes.
- **The library check, from source only.** It was read in the public source, at the tag and across releases, not in the bench's installed binary. The tag link rests on `runs/build/build-3.txt` (describe `v4.3.1.1`) and the copied header's hash.
- **Hive.** The Hive application and the owner's session were not examined. The page's conclusion names Hive as the open layer and does not claim anything about it.
- **Hardware.** No bench, hardware, act or Docker run was made, and no RTL simulation, because the delta is docs only. Physical calibration was NOT RUN, and skipped hosted contexts are not hardware proof.
- **Hosted checks.** These are the hosted check-runs at the exact head, recorded at 2026-10-04T20:04:57Z (`receipts/hosted_checks.txt`).
  - Executed and successful: `rtl-fast`, `full-ci-gate`, `elaborate`, `bdd-conformance`, `changes`, `docs-check-no-git` and `wire-accountability`.
  - `docs-check` was still in progress.
  - Skipped contexts, which are not evidence: `verilator-suites`, `verilator-lint`, the Verilator and Yosys shards, `yosys-portability`, `yosys-elaboration` and Physical gPTP.
- **The clone.** After the gates, the clone is at the exact head with a clean status. The index-as-tree equals `2f5399e4`, and the gitlinks are unchanged.

## Pending manager duties

- Hosted and act acceptance at `6b83de00`, including the outcome of the in-progress `docs-check`.
- The current-dev candidate validation at the merge turn: source base `6c22d3ca`, live dev `6c22d3ca` at review time.
- Carry RES1 and RES2 to the residue checklist. S1 is optional.
- Obtain the external reviewer's round-2 verdict. Merge needs two independent positive reviews and explicit maintainer authorization.
- Acceptance 4 at the Hive layer stays open on #653, which is why the PR body says "Refs #653".

R482-2 FINISHED
