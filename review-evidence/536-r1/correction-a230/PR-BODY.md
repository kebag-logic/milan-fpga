[A230]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Correction round 1](#correction-round-1)** -- R280-1 and R281-1 findings and how each is resolved.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (offline test model, scenarios and two documentation rows; no RTL, no
processor change). `536-aecp-model-mvu` -> `dev`, head
`fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad`, base
`26d855a9176d63625e6635a029a0c44e3d57ce9a`. behave: 14 features, 343
scenarios, 1736 steps, all passing (base: 316 / 1515).
`aecp_response_contract.feature`: 59 scenarios (base 32). 40 of 40
correction-round mutation arms fail exactly their expected scenarios.

## Linked Issue / roles

Closes #536
Relates to #510 (the owner decision that holds MVU `0x0001` to `0x0004` at
RECOMMENDED) and #537 (the lane recording that decision; see the limitations
for the shared file).

Executor: `[A223]` (first head `612db13c2`), `[A230]` (correction round 1)
Internal cleared-context reviewer: `[R280]`
External reviewer: `[R281]`

## Description

The offline AECP model in `tests/steps` had no Milan Vendor Unique dispatch,
so the contract scenario asserted `NOT_IMPLEMENTED` for `GET_MILAN_INFO` while
the pinned engine (`424c688`) serves it (`tb/pp_top` M1). The model now carries
the engine's MVU sub-decode and the `E_MVUINFO` program, and the scenarios
assert what the engine answers for every Table 5.18 command type and for each
term of the sub-decode.

| Piece | Change |
|---|---|
| `tests/steps/aecp_engine_model.py` | `_mvu_command_type()` mirrors `mvu_get_milan_info_w`: message_type 6, all 48 bits of `00-1B-C5-0A-C1-00`, at least the 8-octet Figure 5.3 payload, and the whole @28..@29 word (r bit included); the reserved field is not read. A whole command whose word is in the served MVU set runs `_mvu_program()`, which restates the 20-octet Figure 5.4 body (cdl 32, SUCCESS). Everything else keeps the NOT_IMPLEMENTED echo. `mvu_served` is a required keyword argument. `build_mvu_command()` takes a protocol_id, the @30 halfword and the octets from @32, and `MVU_COMMAND_FORMS` gives each Table 5.18 command in its own figure (5.3, 5.5, 5.3, 5.6, 5.7). |
| `tests/steps/aecp_engine_steps.py` | `SERVED_MVU` declares `0x0000 GET_MILAN_INFO` (Milan 5.4.4.1) beside `SERVED`, and a gate compares it, by value and name, to the engine's `MVU_GET_*_C` / `MVU_SET_*_C` constants. Steps: an MVU command in its named figure (refused if the row's figure is not the command's), a Figure 5.3 frame with each compared field variable (a longer cdl carries that many more octets), the served command's octets under another message_type, the Figure 5.4 layout and its three quadlets. The header lists the new sources and clauses. |
| `tests/features/aecp_response_contract.feature` | The MVU outline: `0x0000` served in Figure 5.3 (status 0, cdl 32, Figure 5.4 body); `0x0001` in Figure 5.5 (cdl 28), `0x0002` in Figure 5.3 (cdl 20), `0x0003` in Figure 5.6 (cdl 92) and `0x0004` in Figure 5.7 (cdl 20), each echoed NOT_IMPLEMENTED at its own length. The three quadlets a controller records (pp_top M2). The sub-decode outline: one row per protocol_id octet @22 to @27 (pp_top M8's values), @26 per nibble, the one-bit @27 row, r = 1, one octet short (all echoed); a junk reserved field and GET_MILAN_INFO at cdl 24 and cdl 112 (all served, cdl 32). The served command's octets as message_type 0, 2, 4, 8, 10, 12 and 14, each echoed under its own type. The RTL gate. |
| `tests/README.md`, `docs/MILAN_V12_ROADMAP.md` Section 6 | The T1 row (59 scenarios, the MVU answers) and the proof-ladder row (the inventory is gated against the `MVU_GET_*`/`MVU_SET_*` constants too). |

## Correction round 1

R280-1 (internal) and R281-1 (external) each returned NEGATIVE at
`612db13c2` on three MINOR findings, the same three defects. Commits
`8179587ee` (F2), `3753b5749` and `fb84de54e` (F1) and `bfe2e5c79` (F3)
answer them. The model's mirror of the engine is not changed: this round
edits the model's command builder and one comment only.

| Finding | Severity, lenses | Resolution | Failing arm |
|---|---|---|---|
| R280-F1 = R281-F1: the sub-decode outline pinned 3 of its guards | MINOR; Tests, Robustness | One row per protocol_id octet @22 to @27 plus @26 per nibble (OUI-36 `...0A-D`, protocol id `0x200`); GET_MILAN_INFO at cdl 24 and cdl 112, served; the served octets under message_type 0, 2, 4, 8, 10, 12, 14, echoed | R280 R1 to R5 and R281 `mt_guard_dropped`, `len_exact_20`, `pid_head_22_23_dropped`, `pid_24_25_dropped`, `pid_26_dropped`, `pid_only_27` are red. Each octet's comparison dropped fails exactly that octet's row, each @26 nibble cut fails exactly the other nibble's row, each extra message_type accepted fails exactly its row |
| R280-F2 = R281-F2: rows `0x0001` and `0x0003` sent a truncated Figure 5.3 frame | MINOR; Conformance, Tests, Robustness | Each RECOMMENDED row sends its own figure and asserts the echo at that length: cdl 28, 20, 92, 20 | R280 R10 and an echo capped at 8 payload octets both fail exactly rows `0x0001` and `0x0003`; a truncated form, a cdl cell set back to 20, or a wrong figure name fails exactly that row |
| R280-F3(a), retained by R281: IEEE 9.3.5.3.3 cited for the MVU echo | MINOR; Conformance, Docs | Milan Table 5.19 and IEEE 1722.1-2021 9.6 (Table 9-6, 9.6.5.3.1) cited for the status; the command-length echo stated as the engine's choice; 9.3.5.3.3 named as the AEM rule | text, checked against the Milan v1.2 and IEEE 1722.1-2021 texts |
| R280-F3(b) = R281-F3: a Section 4.2.4 quotation under a 5.4.4.1 heading | MINOR; Docs, Conformance | 5.4.4.1's own sentence quoted, and the SHALL quotation attributed to Section 4.2.4 | text |

The suggestions R280-S1 and R280-S2 (R281-1 kept both as suggestions) and
the out-of-scope observations R280-O1 to O3 (R281-S1 is O1) are not taken in
this round; none affects lens coverage.

## Authoritative references

- Milan v1.2 Section 4.2.4 (a PAAD sets protocol_version to 1), Section
  5.4.3.2 (the MVU AECPDU: protocol_id at @22..@27, 5.4.3.2.1 value
  `00-1B-C5-0A-C1-00` = the OUI-36 `00-1B-C5-0A-C` and the 12-bit protocol id
  `0x100`, 5.4.3.2.2 r = 0, command_type at @28..@29), Section 5.4.3.3 and
  Table 5.19 (status 1 NOT_IMPLEMENTED), Section 5.4.4.1 (GET_MILAN_INFO,
  SHALL: Figure 5.3 command, Figure 5.4 response, protocol_version 1),
  Table 5.18 (command types `0x0000` to `0x0004`), Table 5.20
  (features_flags), Sections 5.4.4.2 to 5.4.4.5 with Figures 5.5, 5.6 and 5.7
  (SET/GET_SYSTEM_UNIQUE_ID, SET/GET_MEDIA_CLOCK_REFERENCE_INFO, each a
  recommendation).
- IEEE 1722.1-2021 Section 9.6 (Vendor Unique format: Table 9-6 status 1
  NOT_IMPLEMENTED; 9.6.5.3.1 processCommand) and Table 9-1 (message types).
  Section 9.3.5.3.3 governs AEM commands and is not cited for MVU.
- The #510 decision:
  https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089
- `docs/reference/FR_NFR.md` FR-MVU-01 and FR-MVU-03 (REDUNDANCY reports 0);
  `docs/reference/MILAN_COMPLIANCE_MATRIX.md` Section 1.4.
- The engine at the pin: `protocol-processor/hdl/aecp/KL_aecp_engine.sv`
  (`mvu_get_milan_info_w`, the @26/@27 byte comparisons, the A_PLD-exit
  re-dispatch, the `MVU_*_C` constants),
  `protocol-processor/hdl/aecp/ucode/gen_ucode.py` (`E_MVUINFO`),
  `protocol-processor/hdl/packet_engine/KL_pp_rx_validator.sv` (message_type
  6/7 to the MVU bucket), `protocol-processor/tb/pp_top/sim_main.cpp` M1 to M8.

## How to get into the same state

```sh
git fetch origin
git switch --detach fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad
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
features / 343 scenarios / 1736 steps passed; the contract feature 59 / 435.
`check_py_idiom` stays at its ratchets (long function 9, long module 10, too
many parameters 7). `check_em_dash` reports 0 findings over 2 added lines in 2
pages.

Mutation arms: the correction round's `mutations.py` applies each arm to a
disposable copy of `tests/` (the checkout is never written) and requires the
failing set to equal the expected one. 40 of 40 are exact:

| Arm | Fails exactly |
|---|---|
| an MVU command walked, or its echo capped, at Figure 5.3's 8 octets | rows `0x0001`, `0x0003` |
| `0x0001` or `0x0003` sent without its Figure 5.5 / 5.6 octets; its cdl cell set back to 20 | that row |
| a row naming the wrong figure (`0x0001`, `0x0004`) | that row (the step refuses) |
| each row's status flipped | that row |
| `0x0001` to `0x0004` added to `SERVED_MVU`, one at a time | that row and the RTL gate |
| command_type not read | rows `0x0001` to `0x0004`, r = 1 |
| the MVU dispatch arm unreachable | row `0x0000`, the quadlets, the three served guard rows |
| the comparison of @22, @23, @24 or @25 dropped | that octet's row |
| @26 dropped / cut to its high nibble / cut to its low nibble | the three @26 rows / the `C2` row / the `D1` row |
| @27 dropped | the `C1-FF` and `C1-01` rows |
| only @27 compared | the seven @22 to @26 rows |
| message_type not compared; the step leaving the frame at type 6 | the seven message_type rows |
| message_type 0, 2, 4, 8, 10, 12 or 14 also decoded as MVU | that type's row |
| the length guard made exact | the cdl 24 and cdl 112 rows |
| the length capped at Figure 5.3 plus a quadlet | the cdl 112 row |
| the cdl 24 row's status flipped | that row |

The review rounds' own scripts, unmodified, at this head: R280-1's
`r280_mutations.py` turns R1 to R8, R10 and R11 red (R9, the MVU arm moved
ahead of the AEM arms, stays the equivalent mutant R280-1 classified it as);
R281-1's `mutate_model.py` kills all nine arms.

## Known limitations / out of scope

- No RTL was built or run in this lane. 23 of the 26 new or changed rows send
  a frame whose message_type, cdl and octets from @22 equal a frame the
  pinned RTL answered in the R280-1 or R281-1 receipts, and the head model
  answers each of those exact frames as the RTL did, byte for byte. The three
  others have no executed frame: the two @26 nibble rows (the engine compares
  @26 as a whole byte, `KL_aecp_engine.sv:3193`) and the cdl 24 row, which
  differs from R281-1's executed cdl 24 frame only at @33..@35, octets past
  Figure 5.3 that the sub-decode does not read.
- `SERVED_MVU` is gated against the RTL, not against the ledger's
  `served_mvu_operations`. Tying it into `scripts/check_feature_status.py`
  is possible and is not done here.
- The compliance matrix Section 1.4 and roadmap Section 3 MVU rows are being
  edited by #537 and are untouched. This PR edits one row of roadmap Section
  6, which #537 does not touch.
- The engine always replies to GET_MILAN_INFO (the 5.4.4.1 per-configuration
  recommendation is not implemented there), and so does the model.
- The "NOTE ON THE DECODE" paragraph at the top of the feature predates this
  PR and is stale since #83 (R280-O1, R281-S1); it is left for its own Issue.

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
