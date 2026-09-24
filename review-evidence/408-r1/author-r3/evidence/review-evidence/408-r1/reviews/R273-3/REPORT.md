[R273] NEGATIVE - exact head ef9034578f97ebc2951801d867b7c57f8196423d

Round R273-3, external cleared-context review of PR #535 (#408, #409) at head
`ef9034578f97ebc2951801d867b7c57f8196423d`, tree
`1604179afc0b3af5e4590ecd5087e265c015f3dd`. Source base dev `759da623`. All
five lenses were applied. Two findings are open, both MINOR. Neither is a
store or enable reaching the CSR window, but each leaves its lenses unclean.
Receipts are under this packet. Paths in them read `<clone>`, `<sdk>`,
`<packet>` and `<pinned-tool-bin>`.

## Verdict in one paragraph

Correction round 1 fixes what it set out to fix, and I reproduced each fix:

- I ran gate 1b in both modes at this head:
  - with the pinned SDK: 255/255 mutations, 29/29 firmware and 4/4 Makefile
    edits accepted, 55/55 lexer spellings re-measured, 0 NOT RUN;
  - absent: 198/198, 29/29 and 4/4, and one registered NOT RUN.
- All 74 published round-one and round-two cases give the same verdicts as
  the author's receipts, in both modes.
- The disconnect matrix reproduces for the five configurations I re-ran.
- On the pinned GCC 14.3, all 55 corpus spellings are read by the gate
  exactly as recorded.

One spelling outside the corpus still disagrees: a UTF-8 byte-order mark
before `#` at offset 0. GCC skips it. Every gate 1b directive reader anchors
past it. A `##` macro defined behind a BOM therefore reaches `milan_init()`
past the paste ban that this round KEPT inside the six boot-path bodies. That
firmware forges the identity sample, and it is ACCEPTED at this head with the
pinned SDK and without it. dev refuses it on every machine (F1).

The same property is already open through a plain function-like macro (#544),
so no new effect is exposed. The rule-level reduction and the false "refuse
on every machine" claim are new.

Separately, the page says a `##` paste in any macro the six bodies name is
refused. A libc header's `__CONCAT` is such a macro, and a paste through it is
not refused (F2). That behaviour is pre-existing; the claim is new.

## Findings raised by this round

### R273-3-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifact.** In `sw/builder/test_builder.py`:
- `:2691`, `cpp_hash`, the one shared anchor;
- `:2542`, `c_lexed()`, which does not treat U+FEFF at offset 0 as GCC does;
- `:4559`, `macro_definitions()`;
- `:4633-4681`, `assert_boot_path_is_spelled()` (`bodies` at `:4655`);
- `:3772` and `:3824`, the directive-set closure and include pin;
- `:4706`, `lexer_corpus`, which has no BOM entry.

In `docs/integration/BAREMETAL_FIRMWARE.md`:
- `:293-307`: every reader lexes "as the pinned GCC 14.3 lexes";
- `:334-336`: KEPT "and they refuse on every machine";
- rows `:1265` and `:1266`.

**Authority and evidence.**
- #408/#409 acceptance 4 ("No reduction"), which the manager's assignment
  says governs.
- R272-1 F1's required outcome: "Every line the pinned GCC treats as a
  preprocessing directive must be a directive to every C directive reader in
  gate 1b."
- The round-two claim: "With the compiler, nothing dev refused is accepted
  here."

**Measured, lexer.** `receipts/lexer_probe.jsonl`
(`probes/lexer_probe.py`, `probes/lexer_extract.py`) loads gate 1b's own
reader functions unmodified and runs the pinned `riscv32-linux-gcc` 14.3.0
`-std=gnu99 -E`:
- 55/55 corpus entries agree three ways: recorded, gate and GCC.
- 18 of 20 extra spellings agree: NEL, mid-file U+FEFF, Ctrl-Z, CRLF splices,
  a comment between `#` and the name, and others.
- The two BOM spellings disagree. On `﻿#define FOO` then `#ifdef FOO`,
  GCC keeps `b` and the gate does not.

**Measured, whole gate.** `receipts/bom-table.md` and `bom-*.json`, graded
through `assert_boot_contract()` with `probes/probe.py` at dev and at this
head, in both modes:

| Case | dev, SDK | head, SDK | dev, absent | head, absent |
|---|---|---|---|---|
| B1: identity forged by `MILAN_CAT(i, d)`, whose `##` `#define` sits behind a BOM at offset 0 | REFUSED (`##` ban) | **ACCEPTED** | REFUSED | **ACCEPTED** |
| B1c: the same `#define` at offset 0, no BOM (control) | REFUSED | REFUSED (kept paste ban) | REFUSED | REFUSED |
| B2: verdict overwritten by the same BOM paste | REFUSED | REFUSED (resolver) | REFUSED | **ACCEPTED** |
| B4: a twelfth `#include <string.h>` behind a BOM | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| B7: `#line` behind a BOM | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| B6: BOM alone (benign control) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |

A BOM cannot hide a conditional, because a hidden `#if` leaves the gate an
unmatched `#endif` and the readers refuse. That is why no store or enable
reaching the window is exposed (B3 and B5 stay refused where dev refused
them, except B5 absent, which is the registered NOT RUN class). What a BOM
hides is a non-conditional directive:
- the `#define` the kept paste ban looks up (B1, B2);
- the `#include` and `#line` that the kept name pin and closure read (B4, B7).
  These are pre-existing at dev, but they share the cause and the fix.

**Impact.**
- B1 is refused at dev on every machine and accepted at this head on every
  machine, including the merge-grading configuration. That falsifies the kept
  ban's "refuse on every machine" and the round's "nothing dev refused is
  accepted".
- The identity property itself is already open through a plain macro (V2c,
  #544), so the practical exposure is small. That is why this is MINOR.

**Required outcome.**
- The shared lexer treats a UTF-8 BOM at offset 0 as the pinned GCC does, or
  gate 1b refuses U+FEFF anywhere in the firmware. The refusal costs no edit
  anybody writes.
- The corpus gains the BOM spelling, recorded from the compiler.
- A whole-gate control, B1 or equivalent, is refused on its own sentence in
  both modes and fails with the fix removed.
- The page states what the corpus bounds. The PR body's limitation "a
  spelling outside the corpus that GCC reads differently is outside the
  measurement" is not in the page or at the site.

**Verification.**
- `probes/lexer_probe.py <clone> <gcc>` shows 0 disagreements, including the
  BOM entries.
- `probes/run_probes.sh` over `cases/bom.json` shows B1 and B2 REFUSED at the
  fixed head in both modes, and B6 still ACCEPTED if the lexer route is
  taken.
- Gate 1b stays green in both modes.

### R273-3-F2 - MINOR - Conformance, Docs

**Artifact.** In `docs/integration/BAREMETAL_FIRMWARE.md`:
- `:1265`: "A splice or a `##` paste that rebuilds the local's name there is
  refused by the bans kept inside the six boot-path bodies";
- `:1266`: "a `##` paste in any macro they name at any depth ... refused on
  every machine";
- `:333-336`.

The code is `sw/builder/test_builder.py:4655`, where `bodies` holds only this
file's `#define`s.

**Authority and evidence.** #408 acceptance 5: the page matches what
survives. `receipts/extra-table.md` gives case X4: `__CONCAT(i, d) =
MILAN_ID_MAGIC;` before the identity guard in `milan_init()`, pasting through
the libc header's macro. It is ACCEPTED at dev and at this head, in both
modes.

**Impact.** The editing contract states a refusal that does not exist for
header-supplied paste macros. The behaviour is pre-existing and has the same
effect as the #544 bound, so no reduction is claimed. The new sentence is
what is inaccurate.

**Required outcome.** Either:
- the rows say the ban reads this file's own macro definitions, and a paste
  through a trusted header macro, such as `__CONCAT`, is outside it with the
  plain-macro bound (#544); or
- the ban covers header macros the six bodies name.

**Verification.** Read the page rows and the site comment against X4's
verdict.

## Prior public review findings on this PR, resolved or retained at this head

- **R272-1 F1 (BLOCKER): RESOLVED.** Every form-feed, vertical-tab, NUL and
  lone-CR case it and R273-1 listed is REFUSED with the SDK
  (`receipts/published-head-sdk.json`: R272 r1/r2/r3, R273 V1a-V1e, H9,
  H12-H14). The four listed pre-existing gaps are refused in both modes. The
  LEX disconnect lets 15 of 43 controls through (`disconnect-LEX-sdk.json`).
  The residual BOM spelling cannot hide a conditional, so it is filed above
  as F1 at MINOR.
- **R272-1 F2 (MAJOR): RESOLVED.** The splice and paste identity forgeries
  (R272 r3, V2a, V2b, the nested paste) are REFUSED in both modes. The BODY
  disconnect lets 13 of 43 through. The plain-macro bound is stated at
  `:1265` and recorded as #544. The residuals are F1 and F2 above.
- **R272-1 F3 (MINOR): RESOLVED.** The correlated debug edits (R272 r4, V3a,
  V3b) are ACCEPTED in both modes. The store in a related group is still
  refused (mutation table). The cost and its remedy are at `:1275` and in
  the print.
- **R272-1 F4 (MINOR): RESOLVED.** Open-quote cases (V4, R272 r2) are
  refused before any reader, in both modes. The bound is at `:304-307` and
  in row `:1268`.
- **R273-1 F1 (MINOR): RESOLVED.**
  - H6 is REFUSED in both modes, by one `#define` per name, with control
    `magic_read_redefined`; the ONCE disconnect lets 4 of 32 through.
  - The NOT RUN text, the verdict and the page (`:1439-1460`) name the reach
    ban's compiler half (`0 &&`) and the splice and `##` outside the six
    bodies.
- **R273-1 S2 (SUGGESTION): RESOLVED.** H7 is REFUSED in both modes.
- **R273-1 S3 (SUGGESTION): RETAINED as SUGGESTION.** H8 (verifier group
  with its `#else` deleted) is ACCEPTED in both modes at dev and at the head.
  It is pre-existing and mentioned in #544.

## Lens results with evidence

- `[R273] PASS RTL - git diff --stat 759da623..ef903457 (docs/integration/BAREMETAL_FIRMWARE.md, docs/testing/CI_WORKFLOWS.md, sw/builder/test_builder.py; no hdl/, no RTL source list, no gitlink) and receipts/gate1b-{sdk,absent}.log - checked that no RTL, CSR decode or datapath contract changed, the gate's SystemVerilog readers (blanked_sv, assert_sv_directive_set) are outside the diff, and 46/46 RTL mutation variants elaborate as the real milan_datapath under Verilator 5.050 (receipts/verilator-identity.txt) in both modes.`
- Conformance, UNCLEAN (F1, F2). Also checked, with no further finding:
  - #408 acceptance 1: the SDK log's first clause is TEXT RULES +
    INSTRUMENTS; the absent run has one registered NOT RUN naming the arm.
  - #408 acceptance 2: all three named accepted cases are GREEN in both modes
    (ACC1, ACC5, ACC6).
  - #408 acceptance 3: ACC11 (README, notes.txt) is GREEN; the link case H15
    is refused with the SDK.
  - #408 acceptance 4: counts are 255 and 198, both at least 163.
  - #409 acceptance 2 and 3: ACC7 to ACC10 are GREEN.
  - #409 acceptance 4: the blindness control is at `test_builder.py:11960-11980`
    and `:12204-12225`; I agree with both round-one reviews.
- Robustness, UNCLEAN (F1). Also checked, with no further finding:
  - 18 extra lexer spellings agree with GCC.
  - Nested, `#elif` and `#if 0` arms are refused per selection (E2, E3, E5).
  - The 16-selection bound (E6) holds.
  - `holds_error()` skips only selections that cannot build.
  - `condition_key()` relates groups only when nothing in the firmware can
    move the name.
  - Splice and paste inside the verifier (X1, X2) are refused by the resolver
    with the SDK; without it they are ACCEPTED, the registered NOT RUN class
    the page and print name.
- Tests, UNCLEAN (F1: no corpus entry or control for the BOM spelling). Also
  checked: I re-ran the disconnects NONE-sdk (0/43), BODY-sdk (13/43),
  LEX-sdk (15/43), ONCE-absent (4/32) and SEL-absent (8/32), and each matches
  the author's `disconnect/final/TABLE.md`. The corpus has a negative control
  (`:4931`). `test_firmware_compiler.py --selftest` exits 0.
- Docs, UNCLEAN (F1, F2). Also checked, with exit 0 each
  (`receipts/static-checks.log`): `docs_check.py`,
  `check_baremetal_only.py --check`, `check_em_dash.py --base 759da623` and
  `git diff --check`. The gate print's COSTS, NOT RUN and first clause match
  the page's ledger, apart from the two findings.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #408/#409 acceptance 1-5; `receipts/gate1b-*.log`, `published-head-*.json`, `bom-*.json`, `extra-*.json` | R273-3 | ef9034578f97ebc2951801d867b7c57f8196423d |
| RTL | CLEAN | `git diff --stat 759da623..ef903457`; `receipts/gate1b-{sdk,absent}.log` (46/46 RTL variants) | R273-3 | ef9034578f97ebc2951801d867b7c57f8196423d |
| Robustness | UNCLEAN (F1) | `receipts/lexer_probe.jsonl`, `bom-*.json`, `extra-*.json`, `published-head-*.json`; `test_builder.py:2542-2700, 2869-2960, 4559-4681` | R273-3 | ef9034578f97ebc2951801d867b7c57f8196423d |
| Tests | UNCLEAN (F1) | `receipts/disconnect-*.json`, `gate1b-*.log`; `test_builder.py:4706-4966` (corpus and its control) | R273-3 | ef9034578f97ebc2951801d867b7c57f8196423d |
| Docs | UNCLEAN (F1, F2) | `docs/integration/BAREMETAL_FIRMWARE.md:264-353, 1245-1300, 1305-1530`; `docs/testing/CI_WORKFLOWS.md:1126-1130`; `receipts/static-checks.log` | R273-3 | ef9034578f97ebc2951801d867b7c57f8196423d |

## Executable evidence (this packet, at this head unless the file says dev)

- `receipts/sdk-verify.log`: the pinned SDK verified. Archive sha256 is
  d42680e9..., and `riscv32-linux-gcc` is 14.3.0.
- `receipts/verilator-identity.txt`: Verilator 5.050, wrapper sha256.
- `receipts/gate1b-{sdk,absent}.log`: gate 1b through
  `test_firmware_compiler.py`, both exit 0.
- `receipts/lexer_probe.jsonl`: gate readers against GCC over the 55 corpus
  spellings and 20 extra spellings.
- `receipts/published-head-{sdk,absent}.{json,log}`: the 74 published cases
  (`cases/published.json`, rebuilt from the archived `correction-a219/cases`).
- `receipts/bom-{dev,head}-{sdk,absent}.{json,log}` and `bom-table.md`: the F1
  cases from `cases/bom.json` (`probes/make_bom_cases.py`).
- `receipts/extra-{dev,head}-{sdk,absent}.{json,log}` and `extra-table.md`:
  X1-X4 (`probes/make_extra_cases.py`).
- `receipts/disconnect-*.{json,log}`: the author's patches, re-run over
  `labels-round2.txt`.
- `receipts/static-checks.log` and `receipts/clone-state-after.txt`, the
  latter showing the index hash equal to the HEAD tree, a clean tree and the
  gitlinks at pin.
- `probes/probe.py` is the published in-memory grader with the lane path made
  an environment argument. It writes nothing into the checkout.

## Real limits

- Gate 1b was run in full in both modes. The whole builder, the parent,
  PP and gPTP banks, Yosys, act, hosted re-runs and hardware were not run by
  this round.
- I re-ran five of the author's eleven disconnect configurations, not all of
  them.
- The lexer was compared with GCC on 75 spellings, not exhaustively.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- Exact-head hosted check runs were read only. All completed successfully,
  and "Physical gPTP (nightly and manual)" was skipped. The manager owns the
  hosted and act acceptance.

## Pending manager duties

- Route F1 and F2 to a correction round.
- Decide whether R273-1 S3 stays under #544 or gets its own Issue.
- Build and validate the current-dev candidate merge (source base `759da623`,
  live dev `50e78097`) at the merge turn.

R273-3 FINISHED
