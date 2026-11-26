[R937] NEGATIVE - exact head e5d8a71b6fa90352eca72314c7bd2275a1b20285

Round R937-2 is an internal, cleared-context delta re-review of kebag-logic/milan-fpga PR #1016 (Closes #1013).

- Exact head `e5d8a71b6fa90352eca72314c7bd2275a1b20285`, tree `490a2f2ac0734ccb7be0db84be3b3452e9bfccb5`.
- Source base `dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`.
- The delta is `a6864a49..e5d8a71b`: one commit with a one-line message and no trailer.

All five lenses were applied.

- Every prior finding from R937-1 and R938-1 is closed at its root, and my own controls confirm each closure.
- Two new MINOR findings are open, both statements of what was measured: one in the PR body, one in the change log.
- Conformance, RTL and Robustness are covered clean at this head. Tests and Docs are not.

## Reconstruction

- **Contract:**
  - AGENTS.md sections 3 to 8.
  - CONTRIBUTING.md, which is authoritative where the two differ.
  - docs/README.md.
- **Task:**
  - The #1013 body: objective, scope, acceptance 1 to 4.
  - The public pin ruling on #1013 moves the gPTP target to `3ce71b768a2f6f6a5274c127080146e755d02275`.
  - The stack target stays `a795471c0abc4e38f7e5146b4e539dd607b6f501`.
- **Requirements:** the #109 semantics in `docs/design/GPTP_PLANE.md:133-164` and in the phase-22 block comment (`tb/verilator/gptp_shadow/sim_main.cpp:2972-2980`):
  - 802.1AS-2011 11.2.2 b), Figure 11-8 and 11.2.13.2.1 f);
  - Milan v1.2 4.2.6.1.1 and 4.2.6.2.7.
  - The delta changes no product behaviour, so R937-1's clause interpretation carries.
- **Diff:** `git diff a6864a49..e5d8a71b`, 9 files, +65/-22. It changes:
  - phase 22's harness and two new controls;
  - the lifecycle counts;
  - one renamed `milan_dp` check;
  - prose.
- **Order of reading:** I read the following before any prior finding:
  - the diff;
  - the phase-22 harness (`sim_main.cpp:2972-3080`, with `gm_pair` at `:2451-2462`);
  - the bank's publication block (`hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:744-779`).
  - Only then did I read the R937-1 and R938-1 findings, to resolve them.
- **Author packet:** `4b3b21e2104d37db96040622edfe75a5acbf2a76:review-evidence/pins1125-r2`, 15 files.
  - Every git blob id equals the tree's.
  - All 14 MANIFEST.json entries match their `published_sha256` (`receipts/packet_verify.txt`).
  - The live PR body equals the packet's `author/PR-BODY.md`, but for one trailing blank line.
- **Hosted, at the exact head:** snapshot 2026-11-26T04:27Z (`receipts/hosted_summary.txt`).
  - Completed with success: `docs-check-no-git` and `full-ci-gate`.
  - Skipped: `Physical gPTP (nightly and manual)`.
  - 3 in progress and 41 queued, including the Verilator shards and Yosys.
  - Those are not executed evidence. The manager owns hosted and act acceptance.

## My own controls

The controls ran on disposable copies with the pinned Verilator. It identifies itself as `Verilator 5.050 2026-07-01 rev v5.050`.

- Each probe copies exactly what `make run` reads: `hdl/`, `gptp-processor/hdl`, `third_party/verilog-axis/rtl`, `tb/common` and `tb/verilator/gptp_shadow`.
- `tools/make_probes.py` builds the copies.
- Every probe prints each graded pair's `before`, `after` and delta. This is instrumentation only; no check is changed.
- `tools/run_probe.sh` ran the seven suites concurrently.
- Receipts: `receipts/probe_*.log` and `receipts/probe_summary.txt`.

| Probe | Plant | Tally | Named phase-22 result |
|---|---|---|---|
| p0 | none (head plus printf) | 490/490 PASS | graded deltas -401, -396, -394, -396, -396, -396 and -395 ns, against -400 ±64 expected and a 200 ns freshness bar |
| p1 | the bank holds `pub_offset_o` (`KL_gptp_shadow.sv:772`) | 21 FAIL | `the graded Follow_Up is used: its offset is fresh` fails at every trial from -3 to 800 ns, with delta 0 |
| p2 | the graded pair is not sent (`sim_main.cpp:3047` removed) | 14 FAIL | both graded checks fail at all 7 kept trials, with delta 0. This is the round-1 probe of both reviewers, now red by name |
| p3 | the 1213ac5b generator | 25 FAIL | `#109 -81 ns: the graded Follow_Up is used: its offset is fresh` fails with delta 0, as does every later kept trial. -3 and -80 stay green, as they must under the old -80 ns window |
| p4 | mine: the bank keeps a stale offset only while the raw delay is negative | 12 FAIL | freshness fails at -3, -80, -81, -263, -801 and -5,000,000 ns. 800 ns stays green (delta -395). The old check would have passed this defect |
| p5 | mine: the graded pair is built at -400 ns, not +400 | 7 FAIL | freshness passes (delta +396). `its offset uses the delay floored at -800 ns` fails at all 7 trials, so the second check grades direction |
| p6 | mine: the graded pair is built as if the used delay were 0 for negative d | 6 FAIL | `its offset uses the delay floored at -800 ns` fails at -80, -81, -263, -801 and -5,000,000 ns. **-3 ns passes**: a 3 ns error is inside the 64 ns band (see F1) |

What the probes show:

- The checks fail for each defect they claim to detect:
  - an unused pair;
  - an absent pair;
  - a stale bank;
  - a bank that is stale only on negative delays.
- The second check grades both sign and delays at least 80 ns apart.
- Reading `before` isolates the servo's residual between trials. In p0, `before` ranges from -19 to +1 ns, and every delta stays within 6 ns of -400.
- The author's campaign receipt (`author/receipts/gptp_shadow.log`) agrees independently:
  - `public_bank_keeps_a_stale_offset` and `graded_follow_up_not_sent` are each caught by `#109 -263 ns: the graded Follow_Up is used: its offset is fresh`;
  - its tally reads `controls: 16   failures: 0`.

## Findings

### R937-2-F1 MINOR - Tests, Docs - PR #1016 body, "The gPTP platform regression" table, `gptp_shadow` phase 22 row (packet `author/PR-BODY.md`)

"Which it does only when the plane uses that pair with the delay floored at -800 ns" claims more precision than the 64 ns check has.

- **Authority:** AGENTS.md section 6, under Tests and Docs:
  - a test must not be described as detecting more than it does;
  - the PR must give a cold reviewer enough evidence.
- **Evidence:**
  - The check is `near(after, before - 400, 64)` (`tb/verilator/gptp_shadow/sim_main.cpp:3051-3052`). It cannot separate used delays that are less than 64 ns apart.
  - Probe p6 measures this. With the graded pair built for a used delay of 0 instead of -3 ns, the -3 ns trial passes both graded checks, with delta -398 (`receipts/probe_p6_used_as_zero.log`).
  - By the same arithmetic, an unfloored -801 ns is 1 ns from the floored -800 ns, which is also inside the band.
- **What the documents say:**
  - README row 22 at the head is accurate: "as it does when the plane subtracts the delay floored at -800 ns". The PR body's "only when" is not.
  - `GPTP_PLANE.md:160-161` correctly leaves the to-the-nanosecond grade of the used delay to `gptp_plane` phase 6.
- **Classification:** this is a claim about what a test establishes. Under the residue rule it is MINOR, not RESIDUE.
- **Impact:** a reader is told phase 22 proves, at every trial, that the floored delay is the one used. That is not so at two trials:
  - at -3 ns it cannot tell that delay from a clamp to 0;
  - at -801 ns it cannot tell it from no floor. There, the -5,000,000 ns trial's `no PHC step` is what catches a missing floor.
- **Required outcome:** the PR body states the check's real resolution. Either of these will do:
  - the README's wording: "as it does when the plane uses that pair with the delay floored at -800 ns";
  - a statement that the check separates used delays at least 64 ns apart, and that `gptp_plane` grades the used delay to the nanosecond.
  - This edits the PR body only. No commit is needed.
- **Verification:** read the revised row against `sim_main.cpp:3049-3052` and `receipts/probe_p6_used_as_zero.log`.

### R937-2-F2 MINOR - Docs - `CHANGELOG.md:75`

"Nine planted defects each fail a named check" went stale when this delta added two phase-22 controls.

- **Authority:** AGENTS.md section 6, Docs: authoritative documents must reflect changed contracts and evidence statements.
- **Evidence:**
  - At `a6864a49` the nine were `link_delay.py`'s eight plus the public clamp's removal.
  - This delta adds `public_bank_keeps_a_stale_offset` and `graded_follow_up_not_sent` (`tb/verilator/gptp_shadow/mutants.py:224-242`).
  - The PR's own table, "Planted defects, each caught by name", now lists eleven (`receipts/claims.txt`). The change log line was not updated.
- **Why it is in scope:** the delta changed what this line depends on.
- **Classification:** correcting it changes a figure, so it is not RESIDUE.
- **Impact:** the release record understates the #109 control set and contradicts the PR's own table.
- **Required outcome:** `CHANGELOG.md` gives the count the PR table supports, or says what it counts. Either of these will do:
  - "Eleven planted defects each fail a named check";
  - "Eight engine defects and three phase-22 controls each fail a named check".
- **Verification:**
  - Count the #109 plants in `tb/verilator/gptp_plane/link_delay.py` and the #109 entries in `gptp_shadow/mutants.py`'s `MUTATIONS`, and compare with the line.
  - The docs gates pass: `check_doc_style.py`, `docs_check.py` and `check_em_dash.py --base <merge-base>`.

### R937-2-S1 SUGGESTION - Docs - `docs/reference/SUBMODULES.md:1107`

"Its campaign plants the clamp's removal, which fails by name" is still true, but it now omits two of the three phase-22 controls.

Optional rewording: "Its campaign plants the clamp's removal, a stale public offset and an unsent graded pair; each fails by name."

### R937-2-S2 SUGGESTION - Docs - `docs/design/GPTP_PLANE.md:164`

"`gptp_shadow` phase 22 and the `milan_dp` legs grade the public word" understates phase 22. Its graded pair now also grades the used delay through the transport, to 64 ns.

Optional rewording: "`gptp_shadow` phase 22 grades the public word and, to 64 ns, the used delay; the `milan_dp` legs grade the public word."

## Prior findings at this head

| Prior finding | Status at `e5d8a71b` | Evidence |
|---|---|---|
| R937-1-F1 MINOR Tests, Docs: two phase-22 checks cannot fail when the graded Follow_Up is unused | CLOSED at root | The graded pair is built 400 ns off and graded for freshness and value (`sim_main.cpp:2989-2991`, `:3042-3052`). The freshness check fails by name in p2, p3 and p4. README row 22 (`tb/verilator/gptp_shadow/README.md:38`) states what is graded |
| R938-1-F1 MINOR Tests, Docs: a stale offset passes | CLOSED at root | `the graded Follow_Up is used: its offset is fresh` fails at every negative trial in p1 (the bank holds) and p4 (it holds only on a negative delay) |
| R937-1-F2 MINOR Docs: "phase 6 grades every row" | CLOSED | `GPTP_PLANE.md:160-164` names what each suite grades. This matches `tb/verilator/gptp_plane/README.md:24` |
| R938-1-F2 MINOR Tests, Docs: an unexecuted datapath comparison was claimed | CLOSED | The PR body says "only `milan_dp`'s `gptp` leg, not `gptp-lat`". `author/receipts/old-generator-red.log:64-68` records `242 checks: 239 PASS, 3 FAIL`: `[#109] delay -81/-263/-5000000 ns: asCapable kept`. I spot-checked the hash-verified receipt and did not re-run it |
| R938-1-F3 MINOR Tests, Docs: route equality beyond the paired measurements | CLOSED | `SUBMODULES.md:1133-1139` marks AltSpreadLogic_high "no base pair" and claims equality for three pairs only. `CHANGELOG.md:82` says "Each selected image". The PR body no longer claims identical placements. The figures are those of the round-1 record |
| R937-1-R1 / R938-1-R1 RESIDUE: a blank line before phase 6 | CLOSED | `tb/verilator/gptp_plane/README.md:17-24` is one continuous table |
| R937-1-R2 RESIDUE: "then" without an antecedent | CLOSED | `GPTP_PLANE.md:150-152` |
| R937-1-R3 RESIDUE: two `[A850]` lines | CLOSED | The live PR body has one |
| R937-1-S1 SUGGESTION | TAKEN | The check at `tb/verilator/milan_dp/sim_gptp.cpp:1705` is now `harness precondition: the peer presents a negative delay`. No other file references the old name |

## Lens results

- **[R937] PASS Conformance** - `git diff a6864a49..e5d8a71b`, `receipts/clone_verify.txt`, `GPTP_PLANE.md:135-164`.
  - The delta changes no product source, no image input and no gitlink. The gitlinks are `gptp-processor` 3ce71b76 and `tsn-c-stack` a795471c at both heads.
  - 0 files changed under `hdl syn sw configs constraints avdecc` or any submodule.
  - The #109 table is unchanged and still matches the ruling: asCapable, signed use floored at -800 ns, and the public clamp only at `KL_gptp_shadow`.
  - Acceptance 2 says negative delays keep asCapable through the platform's transport and PHC, and the public value reads 0. Phase 22 grades that at this head: p0 is 490/490, and p3 is red from -81 ns.
- **[R937] PASS RTL** - `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:744-779`.
  - The delta changes no RTL.
  - The new control's target, `pub_offset_o <= pub_offset_raw_w;` (`:772`), is the only offset publication. It sits inside the commit-gated bank and occurs exactly once; `tools/make_probes.py` asserts that.
  - The prior RTL verdict (R937-1 at `a6864a49`) depends on nothing this delta touches.
- **[R937] PASS Robustness** - `tb/verilator/gptp_shadow/sim_main.cpp:3022-3056`, probes p0-p6.
  - Covered:
    - an absent pair;
    - an unused pair (the old generator);
    - a fully stale bank;
    - a bank stale only on negative delays;
    - a wrongly signed offset;
    - the servo's residual between trials (`before` from -19 to +1 ns, every delta within 6 ns of -400).
  - The 400 ns step takes no PHC step at any trial: `no PHC step` is green in p0.
  - The 801 ns bad exchange returns before the graded pair, as before.
- **Tests: UNCLEAN** under R937-2-F1.
  - The tests themselves are sound. Both new controls are caught by name: in the author's campaign (16/16) and in my p1 and p2.
  - The lifecycle literals match the campaign's `controls: 16`.
  - The open item is how the PR describes the check's resolution.
- **Docs: UNCLEAN** under R937-2-F1 and R937-2-F2.
- **Comment rule:** no RESIDUE.
  - The new source comments state behaviour and reason: `sim_main.cpp:2989-2990` and `:3042-3044`, `mutants.py:26-29`, `:225-226` and `:234-235`.
  - A scan of the delta's added lines finds no lane label, round, reviewer identity, issue-comment id, or tool or model name.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta diff; `GPTP_PLANE.md:135-164`; gitlinks and image-input diff (`receipts/clone_verify.txt`); p0, p3 | R937-2 | `e5d8a71b6fa90352eca72314c7bd2275a1b20285` |
| RTL | CLEAN | `KL_gptp_shadow.sv:744-779`, unchanged since `a6864a49`; no RTL in the delta | R937-2 | `e5d8a71b6fa90352eca72314c7bd2275a1b20285` |
| Robustness | CLEAN | `sim_main.cpp:2985-3056`; probes p0-p6 | R937-2 | `e5d8a71b6fa90352eca72314c7bd2275a1b20285` |
| Tests | UNCLEAN (F1) | `sim_main.cpp:3042-3052`, `mutants.py:224-242`, `test_mutant_lifecycle.py:165-195,441`, `milan_dp/sim_gptp.cpp:1705`; probes p0-p6; the author's receipts | R937-2 | `e5d8a71b6fa90352eca72314c7bd2275a1b20285` |
| Docs | UNCLEAN (F1, F2) | `CHANGELOG.md:67-86`, `GPTP_PLANE.md:146-164`, `SUBMODULES.md:1099-1146`, `gptp_shadow/README.md:38,98-110,154`, `gptp_plane/README.md:17-24`; the live PR body | R937-2 | `e5d8a71b6fa90352eca72314c7bd2275a1b20285` |

To close:

- F1 needs only a PR-body edit.
- F2 needs a one-line change log commit, which moves the head.
- That commit touches only Docs scope. If nothing else changes, Conformance, RTL and Robustness carry to it.

## Real limits

- I ran only `make run` on the probe copies. These I relied on the author's hash-verified receipts at this head for, read by section:
  - the 16-control `mutants.py` campaign;
  - the lifecycle test;
  - `gptp_plane`;
  - the `milan_dp` legs;
  - the docs gates.
- I did not re-run the old-generator `milan_dp gptp` comparison; I spot-checked its receipt.
- I did not re-examine the route, ledger, firmware or boundary results. The delta changes no image input (0 files), so they carry from the earlier rounds.
- No hardware was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The hosted contexts at this head were still queued or in progress when I took the snapshot. No hosted result is claimed.

## Pending manager duties

- At the merge turn, validate the current-dev merge candidate with the builder and native banks, and link the receipts. The source base is `c34e7d8b`; live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`.
- Accept the hosted and act results at the final head, including exact-head `verilator-suites` and `yosys-portability` evidence.
- Once F1 and F2 are answered, schedule a re-review at the new head (at least Tests and Docs) and the external review.

## Clone state

After the probes, the clone is unchanged (`receipts/clone_verify.txt`):

- HEAD `e5d8a71b`, tree `490a2f2a`;
- `git write-tree` equals the HEAD tree, and the porcelain status is empty;
- the gitlinks and the checked-out submodule HEADs are `3ce71b76` and `a795471c`;
- no probe wrote inside the clone.

R937-2 FINISHED
