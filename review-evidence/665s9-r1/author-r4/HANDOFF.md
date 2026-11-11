# [A760g] #870 (S9 of #665), round 4: handoff

Lane: `665-s9-split-image`, round 4 adds three commits on round 3's head `a91fb27dd3` (base `dev-soft-core` `1d6bf555`).
PR target: `dev-soft-core` (PR #889). Nothing pushed. Earlier rounds' handoffs: `round1/`, `round2/`, `round3/`.
Ruling: #870 issuecomment-6796161767 (tests and docs only, no RTL, the route is not re-run, one delta reviewer).
TAKEN: #870 issuecomment-6796218806 (2026-11-11). REVIEW READY: #870 issuecomment-6799404933. Nothing edited.

## Status: REVIEW READY: ruling items 1 to 5 done, every gate the delta touches rc 0, one open question

Final head `a69fc0f597355a0a200ec5be6bb134b897e97ff5`, tree `bc5cc0e0f7d41e4a8a1aff1a704afc1cc58f5adc`.
`git diff --stat a91fb27d a69fc0f5`: `docs/design/MAILBOX_SPLIT.md`, `docs/design/MARK_II_AREA_PLAN.md`,
`sw/builder/test_builder.py`, `tb/verilator/mbx/{README.md,mutants.py,suite.hpp}`; no RTL, generator, contract, SoC,
builder recipe or routed file, so the route is not re-run (the ruling; the brief's "route the three directives" line is
superseded by the ruling's "The route is not re-run", which is this round's authority).

| # | Ruling item | Result |
|---|---|---|
| 1 | Identity gate controls (R827-1 F1, R828-1 F1) | Done (`8fea72f2`): the positive control and the manifest-ident plant in gate 23p. Verified: `if True:` and `have == bound` fail the positive control; the copy without `check_image_identity.py:175-176` fails the plant. At `a91fb27d` `if True:` and the removed rule both pass 23p |
| 2 | Check IDs (R827-1 F2, R828-1 F2) | Done (`626414f0`): the head-publication check is `U0`. `make` and `make mutants` (231 of 231) green. **Open question**: the stricter verification ("no two checks in suite.hpp and suite_face.hpp share an ID prefix") still finds F0-F2 and T0-T1, shared between the adp/token-bucket checks and the face block since `1d6bf555`; the ruling moved only the new check, so they are left for a decision (below) |
| 3 | Residue R1 wording | Done (`a69fc0f5`): `MARK_II_AREA_PLAN.md:971-972` and the PR text carry the ruling's sentence verbatim |
| 4 | S1 taken, S2 declined | S1 done (`a69fc0f5`, receipt `r4/bus-clock-paths.txt`). The round 3 reports do not list "15 worst": the route's timing report lists, per directive, the 10 worst setup paths within the bus clock and the 10 worst into it from `eth_clocks0_rx`; each slow signoff corner 5 of each. All are published, none from or to `KL_mbx/u_rx`, and `MARK_II_AREA_PLAN.md:1011-1012` now says exactly that instead of "the 15 worst". S2 declined, for #495 (the ruling) |
| 5 | Delta gates on a clean clone of the final head | Done, all rc 0 (table below); the route not re-run; the other gates' inputs unchanged (`r4/not_run.json`, `r4/delta-inputs.txt`) |

## Commits (added only, one-line subjects, no body, no trailers)

- `8fea72f2d5` Grade a split image whose manifest binds the bitstream its gateware holds as one the identity gate passes, and plant a manifest whose ident is not the image's, in builder gate 23p (#665)
- `626414f0bc` Name the mailbox suite's head-publication check U0, an ID no other check uses, in the suite, its mutant needle, the bench README and the mailbox design (#665)
- `a69fc0f597` State the identity gate's bound-bitstream control and manifest-ident plant, the routed nets of every directive of every round, and the bus clock's listed setup paths the receive block is absent from (#665)

## Changes (file:line at the final head, reason)

- `sw/builder/test_builder.py:23606-23614` gate 23p's header: the bound-bitstream control (R827-1 F1).
- `sw/builder/test_builder.py:23706-23710` plant "the manifest's ident changed": the manifest's `ident` set to the
  all-fabric ident (the split ident without its last word), the image untouched; must fail `FINDING manifest:`
  (R828-1 F1; the rule `check_image_identity.py:175-176` had no plant).
- `sw/builder/test_builder.py:23714-23723` `_identity_file_controls()`: a copy of the good split image with a fixture
  bitstream at `gateware/alinx_ax7101.bit` and the manifest's `bitstream` set to its `bitstream_binding`, the image a
  split `--build` writes (R827-1 F1: both good images carried `"bitstream": null`, so `_bitstream_rules` never
  compared).
- `sw/builder/test_builder.py:23757-23764` the gate runs each control through the CLI and requires exit 0 and no
  `FINDING`, else "the gate refused an image that agrees with its identity"; `:23774` the summary line counts it.
- `tb/verilator/mbx/suite.hpp:141,153,154` `H0` -> `U0` for the head-publication check (R827-1/R828-1 F2: `H0` is
  the RX_TAIL guard at `:958-963`, from the base); `mutants.py:603` its needle; `README.md:102,164,393` its row and
  the mutant table; `docs/design/MAILBOX_SPLIT.md:137` the design's citation.
- `docs/design/MAILBOX_SPLIT.md:1635-1648` gate 23p's paragraph: the control, thirteen plants, the new one.
- `docs/design/MARK_II_AREA_PLAN.md:971-972` the ruling's routed-nets sentence (R1).
- `docs/design/MARK_II_AREA_PLAN.md:1011-1012` the bus-clock path claim, to what the round 3 reports list (S1).

## New checks (planted mutant -> failing words)

Receipts `r4/gate23p-mutants-dev.txt` (the final head's tree) and `r4/gate23p-mutants-base.txt` (`a91fb27d`), driver
`r4/tools/gate_mutants.sh`, each arm planted in `sw/litex/check_image_identity.py` and restored:
- `if have != bound:` -> `if True:`: gate 23p fails, "a bound bitstream the image holds: the gate refused an image
  that agrees with its identity (exit 1): FINDING bitstream: ... binds {...}, the manifest records {...}". At
  `a91fb27d`: ALL GATES PASS (survived).
- `if have != bound:` -> `if have == bound:`: fails on the same control, and on "a bitstream other than the one the
  manifest binds: the gate did not find it by its bitstream rule (exit 0)". At `a91fb27d` only the second.
- lines 175-176 removed: fails "the manifest's ident changed: the gate did not find it by its manifest rule (exit 0)".
  At `a91fb27d`: ALL GATES PASS (survived).
- Check U0 (renamed, not new): `rx-head-published-one-cycle-early` and its `-axil` arm fail
  "U0 no receive ring word is written under the head the core sees got=169 exp=0" (`r4/gates/mbx-mutants.log`).

## Gate table (final head `a69fc0f5`, clean clones, never piped)

| Gate | Command (plain shell, in the clone) | Result | Receipt (`receipts/r4/`) |
|---|---|---|---|
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`, the same two rows as round 3's final run (gate 1b's MAKEFLAGS mutation, which has no effect on this make; gate 11's absent Arty mf48 build tree). Gate 23p: "the good split and all-fabric images and 1 bound-bitstream control pass the identity gate; 13 planted images each fail it by their kind" | `gates/test-builder.log` |
| Gate 23p mutants | `bash tools/gate_mutants.sh <clone> <log>` (three arms in `check_image_identity.py`, each restored) | final tree: 3 of 3 fail 23p (rc 1 each); `a91fb27d`: `if True:` and the removed ident rule pass (rc 0), `have == bound` fails | `gate23p-mutants-dev.txt`, `gate23p-mutants-base.txt` |
| Mailbox suite | `make VBUILD_JOBS=16` in `tb/verilator/mbx` | rc 0: WB 546, AXI-Lite 591, cosim 32, WB 2if 553, AXI-Lite 2if 598, model 490, 0 failures; quick arms 12 of 12 | `gates/mbx-make.log` |
| Mailbox mutants | `VBUILD_JOBS=4 python3 -B mutants.py --jobs 8` (the `make mutants` recipe) | rc 0, `mbx mutants: 231 of 231 caught`; U0's arm and its `-axil` arm fail U0 | `gates/mbx-mutants.log` |
| Check IDs | `python3 -I tools/check_ids.py <final> <a91fb27d> <1d6bf555>` | U0 used by one check; H0 by the RX_TAIL guard only; F0-F2, T0-T1 shared since `1d6bf555` (open question 1); S0 is one family checked in two places | `check-ids.txt` |
| docs.yml | `run_docs_yml.py <head> <job> <root>` for wire-accountability, docs-check-no-git, docs-gates-0, -1, -2; `verify_docs_yml.py <head> <root>` | rc 0: 64 steps ran, 31 not run with a reason, 0 bad. docs-gates-0 `gate_13` first failed for want of `wavedrom` in the runner's venv (the not-run `ci_step_10`'s pip half); `wavedrom==2.0.3.post3` was installed and `gate_13` re-run alone on a fresh clone, rc 0; the first attempt is kept | `docsyml/docsyml-verify.log`, `docsyml/*`, `docsyml/docs-gates-0__gate_13.first-attempt.log` |
| Whitespace | `git diff --check 1d6bf5556a a69fc0f5` | rc 0, no output | `gates/diff-check.log` |
| Tree after | `git status --porcelain` in the builder and mbx clones, and each docs job's | empty | `gates/*-tree-after.log`, `docsyml/*__tree-after.txt` |
| S1 paths | `python3 -I tools/buspaths.py <reports>` on round 3's reports (sha256 equal to round 3's) | 20 bus-clock setup paths per directive (route report), 10 per slow signoff corner; 0 lines naming `u_rx/` | `bus-clock-paths.txt` |

## Reused from round 3 (inputs unchanged)

The route (three directives, one checkpoint), the out-of-context term, the all-fabric endpoint compare, the split boots,
S2's harness, the sweep and the four pull_request workflows: their inputs (`hdl/`, `sw/mailbox/`, `sw/litex/`,
`sw/firmware/`, `sw/builder/endstation_builder.py`, configs, VERSION) are untouched by `a91fb27d..a69fc0f5`
(`r4/delta-inputs.txt`). The round 3 timing reports read for S1 match round 3's published sha256 (header of
`r4/bus-clock-paths.txt`).

## Open questions / decisions asked

1. Check IDs `F0`-`F2` and `T0`-`T1` are each used by two families: `suite.hpp`'s adp channel checks (F0-F2) and token
   bucket (T0, T1), and `suite_face.hpp`'s face block (F0-F10) and face timing (T0-T2), on `dev-soft-core` `1d6bf555`
   already (`r4/check-ids.txt`). The ruling's instruction moved the new check only; renaming the face block's IDs
   touches another lane's checks, the README's face rows and their needles, so it needs a decision and its own Issue.
2. S1's "15 worst" is not what the reports enumerate (item 4 above); the sentence was corrected rather than a
   15-path list invented.

## Environment notes

- The pinned RV32 SDK was installed fresh by `scripts/ci_rv32_sdk.py` under the scratch HOME and verified
  (`r4/sdk-verify.log`); the first full `test_builder.py --require-rv32` run, with the SDK on PATH from round 3's HOME,
  stopped at gate 1b's "the provisioned absolute SDK selector must be adopted" (the selector is `$HOME`-relative);
  that log is kept as `r4/gates/test-builder.sdk-selector-fail.log` and is not evidence either way.
- The full mutant campaign ran as `python3 -B mutants.py --jobs 8` (the recipe of `make mutants`, with the brief's
  `--jobs 8`).

REVIEW READY: #870 issuecomment-6799404933 (2026-11-11), head a69fc0f597355a0a200ec5be6bb134b897e97ff5.
