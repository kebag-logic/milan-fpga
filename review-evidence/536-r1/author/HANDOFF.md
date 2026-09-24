# [A223] handoff: #536, the offline AECP model's MVU dispatch

## State

- Lane: `$LANES/536-aecp-model-mvu`, branch `536-aecp-model-mvu`,
  base `dev` `26d855a9176d63625e6635a029a0c44e3d57ce9a`.
- Head: `612db13c244335b0fa3467d02ebab1c350b01990`. Working tree clean.
- **Not pushed. No PR opened.** Both were outside this assignment.
- Commits (one-line subjects, no trailers):
  - `92011f6aefd2067fed6a5bed4b124aa21dea27c7` The offline AECP model serves
    Milan GET_MILAN_INFO with its Figure 5.4 body and echoes MVU
    0x0001-0x0004 NOT_IMPLEMENTED, as the pinned engine does (#536)
  - `612db13c244335b0fa3467d02ebab1c350b01990` Record the MVU rows and their
    RTL gate in the T1 table and the roadmap proof ladder (#536)
- Public comments on #536: `[A223] TAKEN`
  (https://github.com/kebag-logic/milan-fpga/issues/536#issuecomment-5804893299)
  and `[A223] REVIEW READY`
  (https://github.com/kebag-logic/milan-fpga/issues/536#issuecomment-5804968393).

## What changed

| File | Change |
|---|---|
| `tests/steps/aecp_engine_model.py` | The MVU sub-decode (`_mvu_command_type`, mirrors `mvu_get_milan_info_w`) and the `E_MVUINFO` program (`_mvu_program`, the 20-octet Figure 5.4 body, cdl 32). `mvu_served` is a required keyword argument. `build_mvu_command` takes protocol_id and reserved. |
| `tests/steps/aecp_engine_steps.py` | `SERVED_MVU` (`0x0000 GET_MILAN_INFO`, Milan 5.4.4.1); the RTL gate against `MVU_GET_*_C`/`MVU_SET_*_C`; steps for the MVU commands, the Figure 5.4 layout and its three quadlets; the protocol_id step renamed to `... comes back whole in the AECP response`. |
| `tests/features/aecp_response_contract.feature` | The MVU outline (`0x0000` served; `0x0001` to `0x0004` NOT_IMPLEMENTED echo, one row each with its clause), the quadlet scenario, the four sub-decode guard rows, the RTL gate scenario. 32 -> 42 scenarios. |
| `tests/README.md` | The T1 row for the feature. |
| `docs/MILAN_V12_ROADMAP.md` | Section 6 "the inventory" row names the MVU constants gate. |

The engine behaviour was read at the processor pin `424c688`:
`KL_aecp_engine.sv` lines 149-171 (banner), 697-713 (constants), 1284-1296
(`mvu_get_milan_info_w`), 2820-2825 (the A_PLD-exit re-dispatch);
`gen_ucode.py` `E_MVUINFO` (the 20-octet body); `tb/pp_top/sim_main.cpp` M1
to M6 (the graded bytes). The processor was not modified.

## Evidence (all at `612db13c2`)

- `gates.log`: behave whole suite 14 / 326 / 1600 passed; the contract
  feature 42 / 299; `check_py_idiom` exit 0 at its ratchets; `docs_check` 0
  findings; `check_em_dash --base 26d855a9` 0 findings over 2 added lines;
  `git diff --check` clean; `check_feature_status` 0 findings.
- `mutations.log` + `mutations.py`: 21 arms, 0 survived, tree restored clean.
  Each row has its own failing arm (its status flipped; a RECOMMENDED command
  declared served), the model reverted fails `0x0000`, and every sub-decode
  guard and Figure 5.4 value has an arm. Two cross-checks: the base scenario
  fails on the new model at `the AECP response status is 1`; the base model
  file errors all 42 scenarios.
- Offline comparison: the model's GET_MILAN_INFO frame carries exactly the
  payload pp_top M1 builds (`C50AC100 0000 0000 00000001 00000000
  00000000`), cdl 32, 60 octets; `0x0001` to `0x0004` and r = 1 echo at cdl
  20 as M4/M5 expect.

## Things a reviewer should know

- **gptp-processor was initialized at its pin** (`c1b61743`) in this lane,
  read-only. `check_py_idiom` refuses without it, and two unrelated behave
  features error without it (24 errors at the base before init); CI
  initializes it too. Nothing in it was edited.
- **pp_top was not run here** (it builds inside the submodule tree, which
  this lane kept read-only). The RTL-side truth relied on is the pinned
  source and the pp_top check text.
- **The Milan v1.2 text was not available.** Clause numbers and the
  protocol_version wording come from the processor's citations and the
  repository's matrix and roadmap. A reviewer with the text should check
  5.4.3.2.2 (r = 0) and 5.4.4.1 (the reserved field and protocol_version 1).
- `SERVED_MVU` rows carry name and clause only: the model's program owns the
  response form, and the feature asserts status and cdl as literals.
- The guard outline reuses `the AECP response protocol_id is echoed whole`,
  which compares against the sent command. For the one served guard row the
  protocol_id is restated, not echoed; the bytes are identical.
- `@class` tags now sit on the Examples blocks (served rows positive, echo
  rows negative). Nothing in the repository reads them.
- A served MVU command type the model has no program for raises an assertion
  inside the model, so it shows as a behave error rather than a failure.

## Open questions / follow-ups (not filed)

- `SERVED_MVU` could be tied into `scripts/check_feature_status.py` against
  the ledger's `served_mvu_operations`, the way `SERVED` is. Not done here
  (scripts are out of this Issue's scope).
- #537 edits the compliance matrix Section 1.4 and roadmap Section 3 MVU
  rows. This lane touches roadmap Section 6 only; no textual overlap is
  expected at merge.

## Next steps for the lane owner

1. Push `536-aecp-model-mvu` and open a draft PR against `dev` with
   `PR-BODY.md`.
2. Run the local workflow replica from a clean trusted `dev` worktree
   (`python3 -I <trusted-dev>/scripts/act_ci.py --pr <N>`), the `rtl-fast`
   BDD job is the one this change affects.
3. Assign the internal cleared-context reviewer and the external reviewer.
