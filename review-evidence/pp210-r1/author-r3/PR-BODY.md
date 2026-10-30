[A708c]

# Documentation sweep: inventory and its gate, glossary, start-here path, summaries, and the corrections they found

Refs #210 (part of milan-fpga #797). Base: main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`. Head: `6d1d038343e1f0a6b2027cce857a33528b8c2ac7`. Round 1 ended at `18a4dc1f`, round 2 at `0ea635ea`; round 3 adds four commits on top.

Markdown, plus three documentation-gate files (`Makefile`, `scripts/check-doc-inventory.py`, `scripts/check-links.py`). No RTL, generator, generated file, test source or workflow changes.

## What a reader gets

- **A start-here path** in `README.md`: this page, then the new glossary, then the guide for your job, then the architecture in its reading order.
- **`docs/GLOSSARY.md`**: the protocol and in-house terms (PAAD, ADP, ACMP, AECP, sink and source, side port, interface classes, D3, `P-` and `T-` IDs, golden, arm, KILLED). Each term points at its clause or home section and carries no values.
- **`docs/INVENTORY.md`**: one row per Markdown file, giving purpose, audience, the code or clause it describes, a status (current, generated, stale, superseded, obsolete) and the evidence for it.
- **Short summaries** ("In short.") under the title of every long page: architecture 02 to 07, 09 and 10, the three guides, and the `tb/pp_top`, `tb/nvm_port` and `tb/srp_top` READMEs.
- **Retired:** `docs/10_RESOURCE_AND_EFFORT.md` gets a superseded banner. It is the pre-build planning analysis, and its §10 advised against the SRP substitution that has since happened. The banner points at `syn/ooc/README.md` and the architecture. `docs/00_MILAN_COMPLIANCE_REVIEW.md` now says that its §1 to §4 review the superseded concept document and that §5 to §8 are live.
- **`tb/dyn_state/README.md`**: the one suite without a README now has one.

## Round 3: the restated µISA count, and a sweep for its class

| Where | Was | Now |
|---|---|---|
| the concept page's banner, µISA row | "a different 29-operation ISA" (the enum declares 30) | "a different ISA, the `ucpu_op_e` enum in `hdl/aecp/ucpu_pkg.sv`", linked to 06 §8, which lists it. No count |

`make inventory` now also fails on a µISA operation count stated anywhere but 06 §8's derived heading. It scans every current page and the opening banner of every retired page. A retired page's body is history and is not held.

One sweep of this PR's changed pages for any other restated count of a set the tree defines. Each count found now links to the file that defines the set, or is reworded so it states no count:

| Where | Count | Now points at |
|---|---|---|
| `README.md` start-here and guide table, inventory row for `docs/guides/README.md` | "the other two", "all three", "the three guides" | no count (`docs/guides/`) |
| `README.md` build commands | `make check` described by a partial list of its gates | 09 §7, which the inventory gate holds to the `check` rule |
| `tb/acmp_nvm`, `tb/adp_engine`, `tb/dyn_state`, `tb/nvm_port` READMEs; 09 §8.4 and §8.6; the inventory's `tb/nvm_port` row | "two builds", "two shapes", "three builds", "built three times" | each suite's Makefile `run` (and `TMO`, `TMO_ALT`, `TMO_MIN`) |
| 09 §8.6; `tb/nvm_port` README | "nine device models, four of which …"; "the twelve owed states" | the figures gate's `MODELS`; the port's state machine in `KL_pp_nvm_port.sv` |
| `tb/srp_top` README (one heading, its one link) | "four shapes", "five shapes" | `STORE_SHAPES` in its Makefile; the admission suite's Makefile `shapes` |
| `tb/timer_map` README | "ten shapes" (with eight of them named) | `LEGAL` in `shape_elab.sh`, and the wrap's `SI_TBL_C`, `SO_TBL_C` |

Every count replaced was true at round 2's head. The fix is to the class of statement, not to a wrong value. Kept on purpose: measured tallies (the gates and the inventory's evidence hold those), counts a standard defines, counts of structure the architecture itself defines and enumerates in the same sentence, and dated history.

## Round 2: the review findings at `18a4dc1f`, and stopping their class

| Where | Was | Now |
|---|---|---|
| 02 §4.1 | "§34.6.1.1 defines the per-stream idleSlope"; the operIdleSlope quote attributed to §34.6.1 | §34.3(d) for operIdleSlope as the shaper's idleSlope (quoted exactly), §34.3.2 and §34.3(c) for SRP as its sole source, §34.6.1 for the per-stream idleSlope. 802.1Q-2014 has no §34.6.1.1 |
| 06 §8 µISA | 29 operations, no `SHIFT_R` | 30 operations; `SHIFT_R` in Data, a logical right shift of the 64-bit operand by `imm[5:0]`, as `ucpu_pkg.sv` declares and `KL_aecp_ucpu.sv` executes |
| `README.md` start-here | "two pages are kept for provenance" (there are three) | links to the inventory's Retired heading and counts nothing |
| 02 summary | every clock-domain crossing is the integrator's | every crossing but one: with P-EN-IDENTIFY-NOTIFICATION = 1, `identify_button_i` passes the processor's own two-flop synchronizer (§2 rule 3, `KL_aecp_notify.sv`) |
| `tb/nvm_port` summary | `make` runs three builds (it runs seven) | names the suite's and the harness's bounds and points at the Makefile's `BUILDS` |
| 00 §7 (GAP-06, GAP-17), `tb/pp_top` heading, `tb/adp_engine` mutation record | four lane labels left | plain references to the issues |
| glossary, time compression | "a hundred clocks" | no value; the link to the HDL guide §7 carries it |

To stop a page restating a count or list the tree defines, `make inventory` now derives two of them: the 06 §8 µISA count and table from `ucpu_pkg.sv`'s operation enum, and the 09 §7 target table from the Makefile's `check` rule. The two other counts above are replaced by links to the file that defines them.

## What was wrong, and is fixed (round 1)

| Where | Was | Now |
|---|---|---|
| 01 F01.5 P-TIMER-SLOTS | baseline examples 66 and 89 | the formula's own example in 08 §5: 68 and 91, as `pp_pkg.sv` computes since the MAAP pair |
| 01 F01.5 P-DISPATCH-ROM-W | read as live | no RTL consumer: no dispatch ROM ships (06 §8.1) |
| 01 §5 shutdown | a `SHUTDOWN` request | the fall of ADP's effective enable, from the requested enable or the REBOOT sequence; there is no shutdown port |
| 03 §7.1, `tb/pp_top`, `tb/resp_buf` | "IEEE §9.2.1.1 gives an AECP command 100 ms" | `T-BUDGET-AECP-WC` (F08.1), inside IEEE 1722.1-2021 §9.3.2.6's `T-AECP-RESP`. The standard has no §9.2.1.1 and no 100 ms limit |
| 02 F02.10 | 802.1Q §35.2.2.7.4 and §34.6.1.1 | §35.2.2.7.2 (Table 35-3) and §34.6.1. Neither cited clause exists in 802.1Q-2014 |
| 10 §2 | 802.1Q §34.6.1.1 | §34.6.1 |
| 07 F07.1 | lists dispatch and response-size ROMs | lists only the µcode and listener transition ROMs, which ship |
| 00 §8 item 8 | IEEE counter masks from a plain-IEEE profile ROM | carried from the integrator's `ctr_*` face, as 01 §7 and 06 §6.6 say |
| integrator guide §4.2 | `wr_done_i`, `wr_ready_i` | `resp_mem_wr_done_i`, `resp_mem_wr_ready_i` |
| HDL engineer guide §9 | three divergence rows | shutdown row resolved and removed; decode and image rows match the tree |
| `tb/prng`, `tb/dispatch`, `tb/desc_store`, `tb/timer_map` | 57, 179, 584, 1,187 checks | 76, 211, 586, 1,360, re-measured |
| 16 links across 00, 01, 02, 05, 06, 08, the integrator guide and `tb/acmp_talker` | anchors that pass the link gate but not GitHub | GitHub's anchors |
| 00, 01, 06, 08, 09 and seven suite READMEs | lane labels ("lane C6", "lane P1", "the processor lane", "saved-state lane 3", an internal lane ID) | plain references to the issues and changes |

## Gates

- **`make inventory`**, new and part of `make check`. It fails when a Markdown file has no row, when a row has no file, on a duplicate row, a status outside the vocabulary or an empty evidence cell, and when a row's status disagrees with the page's own banner. It also fails when the 06 §8 µISA count or table differs from `ucpu_pkg.sv`'s operation enum, or the 09 §7 target table from the Makefile's `check` prerequisites. An enum member it cannot parse, a missing heading, table or rule, or a missing defining file is a failure too. It also fails on a µISA operation count stated on any current page, or in a retired page's banner, other than 06's derived heading. `--selftest` plants 25 faults in fixtures of its own, beside five clean controls, and must see each one named.
- **`scripts/check-links.py`** now computes anchors the way GitHub does: every space becomes one hyphen, and `_` is kept. The old rule collapsed whitespace, so a heading such as `4.2 maap — address allocation` passed as `#42-maap-address-allocation`, which GitHub does not resolve.

| Gate | Base | Head |
|---|---|---|
| `make check` | 0 | 0 |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 |
| `python3 scripts/check_upc_map.py` | 0 | 0 |
| `python3 scripts/check_m9_opcodes.py --selftest`, then without | 0, 0 | 0, 0 |
| `./scripts/lint_hdl.sh` | 0 | 0 |

Planted mutants, round 3, on a disposable clone of exactly `6d1d038`, restored after each:

| Mutant | Result |
|---|---|
| the concept banner put back to "29-operation ISA" | `RESTATED`, `make inventory` fails; the round-2 gate passes it |
| the banner given the true count, "30-operation ISA" | `RESTATED`, fails: a correct restatement is still a restatement |
| a current page saying "the 30 operations of the µISA" | `RESTATED`, fails |
| a second count beside 06's derived heading, on its line | `RESTATED`, fails |
| control: the retired page's historical body count changed | passes |

Planted mutants, rounds 1 and 2 (rounds 1 and 2 on clones of their own heads, round 2's at `06c934b`; reproduced by review at `0ea635e`):

| Mutant | Result |
|---|---|
| a deleted inventory row | `NO ROW`, rc 1 |
| a new page with no row | `NO ROW`, rc 1 |
| the superseded concept page marked current | `BANNERED`, rc 1 |
| a link in the old collapsed-anchor form | `missing anchor`, rc 1; the same link passes the base gate |
| 06 put back to its `18a4dc1f` text (29 operations, no `SHIFT_R`) | `make inventory` fails: count and `table lacks SHIFT_R` |
| an operation added to the enum | fails: count and `table lacks` the new name |
| an enum member written in hexadecimal | fails: `unparsed enum member` |
| the `inventory` row dropped from 09 §7, or a target added to `check` | fails: ``table lacks `<target>` `` |

`make -C tb/nvm_port figures` (the CI suites job) takes longer than could be run here. In that README, this PR changes only count words that are not figures. Every input the gate reads from the README (claim coverage, arm and matrix rows, each claim's matches, each figure) is byte-identical at round 2's head and at this head. The half of the gate that measures reads only unchanged RTL and suite sources. CI runs it on this PR.

Consumer check: milan-fpga at the head of PR #805, with the protocol-processor gitlink moved, in a scratch checkout, to this PR's base and then to its head. Its submodule-reading gates give the same verdicts at both:
- documentation, paths, hygiene, Python, shell, C++ and SystemVerilog idiom, TODO-ownership, naming, fail-fast, test-evidence and source-list gates: all pass, and the Python idiom gate's metrics are unchanged with the changed gate script;
- its pin page and boundary-diagram checks fail identically at base and head, because those records name the currently adopted pin.

## Not fixed here (findings)

- **`tb/pp_top/sim_main.cpp:20`** (new): the comment says "The suite builds six times (Makefile)"; the Makefile's `run` builds seven and requires seven tallies. This is a test-source comment.
- **Wrong clause numbers in source comments.** These are RTL and test comments, so this lane cannot change them. Behaviour is unaffected: the `tb/pp_top` bound is the right value.
  - `hdl/top/protocol_processor_top.sv:666` and `hdl/srp/KL_srp_admission.sv:10`: 802.1Q §34.6.1.1, should be §34.6.1.
  - `hdl/aecp/KL_aecp_resp_buf.sv:32` and `tb/pp_top/sim_main.cpp:3737`: IEEE 1722.1 §9.2.1.1, 100 ms. The clause does not exist; the limit is §9.3.2.6's 240 ms, and 100 ms is `T-BUDGET-AECP-WC`.
  - `tb/acmp_talker/sim_main.cpp:99`: 802.1Q §35.2.2.7.4, should be §35.2.2.7.2.
- **156 R-numbered review labels** remain in nine suite READMEs' mutation records (`tb/pp_top`, `tb/srp_top`, `tb/acmp_nvm`, `tb/nvm_port`, `tb/aecp_notify`, `tb/srp_decoder`, `tb/maap`, `tb/aecp_cmds`, `tb/adp_engine`). Each one keys a planted defect to the review that wrote it, and nothing in the tree turns a label into a link. Replacing them needs the owner's choice of reference, so #210's no-labels rule is not yet fully met. That is why this PR says "Refs" rather than "Closes".
- **Diagram 22** (`docs/diagrams/22-aecp-descriptor-fetch.svg:155`), a hand-authored SVG, still says "IEEE 1722.1-2021 §9.2.1.1 gives a controller 100 ms before it retries". This PR changes Markdown and documentation gates only. Suggested text: "the AECP design budget `T-BUDGET-AECP-WC`, inside IEEE 1722.1-2021 §9.3.2.6's `T-AECP-RESP`, against roughly one microsecond per memory access".
- **`hdl/aecp/ucpu_pkg.sv:14` and `:48`**: comments say "the 29 operations of 06 §8"; the enum below them declares 30.
- **`tb/pp_top/notify_mutants.py:3` and `tb/pp_top/notify_phases.hpp:2`**: "lane C6" in test-source comments.
- **`tb/dyn_state/shape_tally.txt`** is tracked but rewritten by every run of that suite.
- **`scripts/check-links.py`** does not model GitHub's `-1` suffix for duplicate headings. This can only refuse a valid link, never pass a broken one.
- **The inventory gate's target-table check** reads only the first `check:` rule line. A second such line would add a target it does not see. No such line exists today.
- **The F03.1 draw.io export** still draws the descriptor image on chip. The page says so under the figure.
- **Tallies not re-measured** for `tb/pp_top` and `tb/srp_top`, because of their run time.
