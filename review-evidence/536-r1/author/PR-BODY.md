[A223]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (offline test model, scenarios and two documentation rows; no RTL, no
processor change). `536-aecp-model-mvu` -> `dev`, head
`612db13c244335b0fa3467d02ebab1c350b01990`, base
`26d855a9176d63625e6635a029a0c44e3d57ce9a`. behave: 14 features, 326
scenarios, 1600 steps, all passing (base: 316 / 1515).
`aecp_response_contract.feature`: 42 scenarios (base 32). 21 of 21 mutation
arms turn the feature red.

## Linked Issue / roles

Closes #536
Relates to #510 (the owner decision that holds MVU `0x0001` to `0x0004` at
RECOMMENDED) and #537 (the lane recording that decision; see the limitations
for the shared file).

Executor: `[A223]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The offline AECP model in `tests/steps` had no Milan Vendor Unique dispatch,
so the contract scenario asserted `NOT_IMPLEMENTED` for `GET_MILAN_INFO` while
the pinned engine (`424c688`) serves it (`tb/pp_top` M1). The model now carries
the engine's MVU sub-decode and the `E_MVUINFO` program, and the scenario
asserts what the engine answers for every Table 5.18 command type.

| Piece | Change |
|---|---|
| `tests/steps/aecp_engine_model.py` | `_mvu_command_type()` mirrors `mvu_get_milan_info_w`: message_type 6, all 48 bits of `00-1B-C5-0A-C1-00`, at least the 8-octet Figure 5.3 payload, and the whole @28..@29 word (r bit included); the reserved field is not read. A whole command whose word is in the served MVU set runs `_mvu_program()`, which restates the 20-octet Figure 5.4 body (cdl 32, SUCCESS). Everything else keeps the NOT_IMPLEMENTED echo. `mvu_served` is a required keyword argument, so no caller can drop the dispatch by omission. `build_mvu_command()` takes a protocol_id and a reserved value. |
| `tests/steps/aecp_engine_steps.py` | `SERVED_MVU` declares `0x0000 GET_MILAN_INFO` (Milan 5.4.4.1) beside `SERVED`, and a new gate compares it, by value and name, to the engine's `MVU_GET_*_C` / `MVU_SET_*_C` constants. New steps: the Milan MVU command by command_type, a Figure 5.3 frame with each compared field variable, the Figure 5.4 layout, the three Figure 5.4 quadlets by name. The protocol_id step is renamed `... comes back whole in the AECP response` (the served body restates it; it is no longer only an echo). Header lists the new source and clauses. |
| `tests/features/aecp_response_contract.feature` | The MVU scenario becomes an outline: `0x0000` served (status 0, cdl 32, Figure 5.4 body), `0x0001` to `0x0004` echoed (status 1, cdl 20, payload verbatim), each row with its clause. New: the three quadlets a controller records (protocol_version 1, features_flags 0, certification_version 0; pp_top M2); the sub-decode guards (a foreign 12-bit protocol id, r = 1, one octet short of Figure 5.3, and a junk reserved field that is still served with reserved 0; pp_top M3, M5, M6, M5b); and the RTL gate. |
| `tests/README.md`, `docs/MILAN_V12_ROADMAP.md` Section 6 | The T1 row (42 scenarios, the MVU answers) and the proof-ladder row (the inventory is gated against the `MVU_GET_*`/`MVU_SET_*` constants too). |

## Authoritative references

- Milan v1.2 Section 5.4.3.2 (the MVU AECPDU: protocol_id at @22..@27,
  5.4.3.2.1 value `00-1B-C5-0A-C1-00`, 5.4.3.2.2 r = 0, command_type at
  @28..@29), Section 5.4.4.1 (GET_MILAN_INFO, SHALL: Figure 5.3 command,
  Figure 5.4 response, protocol_version 1), Table 5.18 (command types
  `0x0000` to `0x0004`), Table 5.19 (status 1 NOT_IMPLEMENTED), Table 5.20
  (features_flags), Sections 5.4.4.2 to 5.4.4.5 (SET/GET_SYSTEM_UNIQUE_ID,
  SET/GET_MEDIA_CLOCK_REFERENCE_INFO, each a recommendation).
- IEEE 1722.1-2021 Section 9.3.5.3.3 (a command not implemented is answered
  NOT_IMPLEMENTED with a correctly sized response).
- The #510 decision:
  https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089
- `docs/reference/FR_NFR.md` FR-MVU-01 and FR-MVU-03 (REDUNDANCY reports 0);
  `docs/reference/MILAN_COMPLIANCE_MATRIX.md` Section 1.4.
- The engine at the pin: `protocol-processor/hdl/aecp/KL_aecp_engine.sv`
  (`mvu_get_milan_info_w`, the A_PLD-exit re-dispatch, the `MVU_*_C`
  constants), `protocol-processor/hdl/aecp/ucode/gen_ucode.py` (`E_MVUINFO`),
  `protocol-processor/tb/pp_top/sim_main.cpp` M1 to M6.

## How to get into the same state

```sh
git fetch origin
git switch --detach 612db13c244335b0fa3467d02ebab1c350b01990
git submodule update --init protocol-processor gptp-processor
python3 -m pip install behave
```

## How to validate

```sh
(cd tests && behave --no-capture -f plain)
(cd tests && behave --no-capture -f plain features/aecp_response_contract.feature)
python3 -B scripts/check_py_idiom.py
python3 -B scripts/docs_check.py
python3 -B scripts/check_em_dash.py --base 26d855a9
python3 -B scripts/check_feature_status.py
git diff --check 26d855a9 HEAD
```

Expected result / pass criteria: every command exits 0. behave reports 14
features / 326 scenarios / 1600 steps passed; the contract feature 42 / 299.
`check_py_idiom` stays at its ratchets (long function 9, long module 10, too
many parameters 7). `check_em_dash` reports 0 findings over 2 added lines in 2
pages.

Mutation arms (each is one substitution on the head, run against the contract
feature, then restored; every arm must be red):

| Arm | Substitution | Fails |
|---|---|---|
| the model reverted | the MVU dispatch arm made unreachable (`elif False and _mvu_command_type(...)`) | row `0x0000`, the quadlet scenario, the junk-reserved row |
| each row's status flipped | the status cell of row `0x0000` (0 -> 1), and of `0x0001`, `0x0002`, `0x0003`, `0x0004` (1 -> 0), one at a time | that row only |
| the model serves a RECOMMENDED command | `0x0001`, `0x0002`, `0x0003` or `0x0004` added to `SERVED_MVU`, one at a time | that row (the model has no program for it) and the RTL gate |
| command_type ignored | `_mvu_command_type()` returns `MVU_GET_MILAN_INFO` for any whole Milan command | rows `0x0001` to `0x0004`, the r = 1 row |
| Figure 5.3 length guard dropped | `len(cmd_payload) < MVU_CMD_PLD` -> `< 0` | the one-octet-short row |
| protocol_id tail not compared | only @22..@23 compared | the foreign 12-bit protocol id row |
| r bit masked | the @28 word `& 0x7FFF` | the r = 1 row |
| reserved forwarded | the body's reserved field taken from the command | the junk-reserved row |
| protocol_version 2, features_flags 1, certification_version `0x01000000` | the model constant, one at a time | the quadlet scenario |
| body one quadlet short | certification_version dropped from the body (cdl 28) | row `0x0000`, the quadlet scenario, the junk-reserved row |
| a later pin serves GET_SYSTEM_UNIQUE_ID | the gate pointed at a copy of the pinned engine that adds `MVU_GET_SYSTEM_UNIQUE_ID_C = 16'h0002` (the submodule is not edited) | the RTL gate only |
| `SERVED_MVU` misnames the command | `GET_MILAN_INFO` -> `GET_MILAN_INFOS` | the RTL gate |

Two cross-checks: the base scenario run against the new model fails exactly
on `the AECP response status is 1` (the old assertion contradicts the
engine); the base model file restored whole makes all 42 scenarios error
(`mvu_served` has no default).

## Known limitations / out of scope

- `protocol-processor/tb/pp_top` was not run in this lane. The model's
  served frame was compared offline with the payload pp_top M1 builds
  (`C50AC100 0000 0000 00000001 00000000 00000000`, cdl 32, 60-octet frame)
  and its echo for `0x0001` to `0x0004` and r = 1 with M4 and M5.
- The Milan v1.2 text was not available in this lane. Clause numbers and the
  protocol_version wording are taken from the pinned processor's own
  citations and the repository's compliance matrix and roadmap.
- Per-command RTL evidence for `0x0001`, `0x0003` and `0x0004` stays with the
  protocol processor (pp_top M4 covers `0x0002`); these offline rows mirror
  the RTL source and are not RTL evidence.
- `SERVED_MVU` is gated against the RTL, not against the ledger's
  `served_mvu_operations`. Tying it into `scripts/check_feature_status.py`
  is possible and is not done here.
- The compliance matrix Section 1.4 and roadmap Section 3 MVU rows are being
  edited by #537 and are untouched. This PR edits one row of roadmap Section
  6, which #537 does not touch.
- The engine always replies to GET_MILAN_INFO (the 5.4.4.1 per-configuration
  recommendation is not implemented there), and so does the model.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the gates above; no RTL touched)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
