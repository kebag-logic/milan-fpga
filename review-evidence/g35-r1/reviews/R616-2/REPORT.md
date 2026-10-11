[R616] POSITIVE - exact head a70e38804cb16435c089d024c58e8c3fb4d39ff6

# R616-2 internal independent review: FPGA-gPTP PR #80 (issue #35)

- Exact head `a70e38804cb16435c089d024c58e8c3fb4d39ff6`, tree `e02031a9d589ad6dc0f9d005c762de610c737784`. Source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. Seven commits on the base (four from round 1, three from round 2), all fast-forward. No rebase.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open at this head.
  - New this round: one RESIDUE (wording only, R616-2-RES1) and one SUGGESTION (R616-2-S1).
  - The prior MAJOR R617-F1 and residue R616-1-RES1 are resolved.
  - R616-1-S1 is retained as a SUGGESTION. R616-1-S2 is retained in part and refined by R616-2-S1.
- All five lenses are CLEAN.

## Reconstruction (order followed)

1. **Contributor guidance.** This repository has no AGENTS.md or CONTRIBUTING.md. The root `README.md` and `docs/README.md` set the truth order: RTL and generated microcode, then executable tests, then current guides, then history.
2. **Issue #35.** The body has four acceptance items. The scope comments are:
   - 6104916029: the "safer default" ruling, the parser-only scope, parent tie-off identity, and the proof list.
   - 6105366046: the hierarchical +1 `$mux` (3567 -> 3568 cells) is accepted.
   - 6105869522: the bank ruling. It amends acceptance item 2: writes up to and including the flagged byte are accepted, and no write may follow it. Words are undefined and named by no event, and the next accepted event reads only its own frame. It also sets four required items for round 2.
3. **Interface authorities.**
   - Parser module header and port documentation.
   - `docs/INTEGRATION.md` receive interface.
   - The engine bank consumer (`hdl/top/KL_gptp_engine.sv:252-310`: bank ping-pong, Announce context).
   - The microcode generator's per-handler bank reads (`hdl/ucode/gen_gptp_ucode.py`).
   - The parent tie-off: `KL_gptp_shadow.sv:666` at parent dev `ac2c5e77`, read-only.
4. **Diff and history.** Full `git diff 5dce647..a70e388`: 11 files, +656/-18. Each commit read.
5. **Public evidence.** `kebag-logic/milan-fpga@2e32325/review-evidence/g35-r1`. Its gate, equivalence, mutation and parent receipts are bound to the **round-1 head `5b4ce397`**, not this head (`gates-head/identity.txt`). For round 2 the only author statement is the REVIEW READY comment 6106250782, which publishes no receipts. No manager evidence comment exists for this head.
6. **Prior findings.** I read the prior public findings (R616-1, R617-1) only after completing my own pass. They are dispositioned below.

## The change under review

`hdl/wire/KL_gptp_rx_parser.sv:652` adds `if (rx_err_i) bad_r <= 1'b1;` inside the `rx_valid_i` branch, after the sof arm.

- **First byte.** The latch is the last assignment, so it wins over the sof arm's `bad_r <= 1'b0`.
- **Gating after the flag.** Header writes are gated by registered `!bad_r` (`:461,466,471,478`), and body writes by `if (!bad_r)` (`:487`). So the flagged byte's own edge may still write (the "on" write the ruling allows), and every later edge cannot.
- **Eof byte.** `fin_ok_r` still takes `!rx_err_i` directly (`:632`). The deferred Announce `w12` write and the event are both gated by `fin_ok_r` (`:395-404`), so nothing lands after an eof-flagged refusal.
- **Drop count.** It counts once per frame through `fin_drop_w`. A flagged one-byte frame counts once through `runt_drop_w`.
- **Next frame.** Its sof clears `bad_r`, so a refusal cannot outlive its frame.
- **Round 2.** No RTL code changed. The round-2 RTL diff is comments only, as stated.

## Lenses

### Conformance: CLEAN

Each clause below is checked against the issue acceptance as amended by 6105869522.

- **Contract stated where an integrator reads it, and the code matches.**
  - Port comment `:113-116`, DROP-arm list `:32`, contract paragraph `:52-66`, eof-gate comment `:624-628`.
  - `docs/INTEGRATION.md:47,60-82`, with the link to the bank ruling.
  - The R616-1-RES1 sentence appears verbatim at `:60-63`.
- **One counted drop and no event at every byte.**
  - Author suite, four ruled types, every position: `receipts/head_parser.log`, 337/337.
  - Independent reviewer probe, ten shapes: Sync, Follow_Up, Pdelay_Req, Pdelay_Resp, Pdelay_Resp_Follow_Up, Signaling, a fixed Announce, an Announce with a 3-hop PathTrace, an Announce with a 9-hop (over-cap) PathTrace, and an Announce with physical padding. Every byte position: `receipts/probe_head.log`, 568/568.
  - Base RTL fails the same probe in 226 checks (`receipts/probe_base.log`).
- **No bank write after the flagged byte's own edge.**
  - The probe asserts zero writes on any later edge, including the drain.
  - It also asserts the stronger property that the writes up to and including that edge equal the clean frame's write prefix, address and data, at every position of all ten shapes.
- **No word of a refused frame reaches the next event.**
  - Probe: all 100 ordered pairs of the ten shapes, zero-gap, refused at eof (every word left) and at byte 30. The clean frame's event sees each word that frame writes holding its own value, with one drop and one event of the right code.
  - Microcode cross-check: every bank word a handler reads is a word its own type writes before the event.

    | Handler | Words read |
    |---|---|
    | Sync | w0, w2 |
    | Follow_Up | w0, w1, w2, w4, w5 |
    | Announce | w2, w8, w9, w10, w12 |
    | Pdelay_Req | w0, w2, w3 |
    | Pdelay_Resp | w0, w2, w4-w7 |
    | Pdelay_Resp_Follow_Up | w0, w2, w4-w7 |

  - The engine's path-trace tail is count-gated (`KL_gptp_engine.sv:204-209,285-290`). So the header claim "the next accepted frame writes every word its event names" holds.
- **Frames without an error are unchanged.**
  - Reviewer equivalence (`scripts/equiv.sh`, `receipts/equiv.log`): with `rx_err_i` tied low, 748 of 748 cells are proven.
  - With the port free, exactly one cell, `bad_r`, is unproven (non-vacuity; that script asserts and returns 1).
- **Parent.** The tie-off `.rx_err_i (1'b0)` is confirmed at `ac2c5e77:hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:666`. The +1 hierarchical `$mux` is ruled acceptable (6105366046) and is not a finding.

### RTL: CLEAN

- **Latch placement and priority.**
  - The latch wins over the sof clear on a first-byte flag (`:408-411` vs `:652`).
  - It is inside `rx_valid_i` (`:407`), so a flag in an idle gap is ignored.
  - The probe shows a flagged stray valid byte outside any frame causes no drop and leaves the next frame intact.
- **Interaction with other refusal arms.** A flag stacked on a bad EtherType or a foreign domain, at bytes 0, 13, 30 and eof, still gives exactly one drop and no event (probe §5).
- **Simultaneous drops.** A flagged frame's deferred drop coinciding with a zero-gap runt counts two drops; a flagged runt also gives no event (probe §7). The `fin_drop_w`/`runt_drop_w` single write site (`:389-391`) is unchanged.
- **Engine consumer.**
  - The bank flips only on an accepted event (`KL_gptp_engine.sv:307-308`), so a refused frame and its successor share one bank. The bench models this correctly.
  - The Announce context reserved at a `w8` write is released by the eof countdown when no accepted event follows (`:273-280`). An Announce refused mid-frame after byte 66 takes the same path as an eof-error refusal at base, so it adds no new lock-up state.
- **Lint.** `make lint` rc 0 with Verilator 5.050 (`receipts/head_lint.log`).
- **Engine suite.** 1613/1613 in all three seeded passes (`receipts/head_engine.log`).
- **Other gates.** tsngen 288 + 4/4 mutants (`receipts/head_tsngen.log`). Bench MII tag test PASS (`receipts/head_bench.log`).

### Robustness: CLEAN

- **Random multi-byte flag sets.** 200 seeded trials per shape for ten shapes, one to six flagged bytes each. Every trial gives exactly one drop, no event, and no write after the first flagged byte (probe §2).
- **Edge positions.**
  - Physical padding after the declared end, before eof (`ann_pad` bytes 78-82) is refused correctly at head.
  - Over-cap PathTrace (9 hops) and a deferred `w12` after eof are covered.
- **Zero-gap successors.** These cover both a refused frame followed by a clean frame, and a clean frame followed by a frame flagged on its first byte. In the second case the first frame still dispatches, and the successor writes nothing (probe §8).
- **Recovery after a refusal.** The next frame dispatches with no residual drop, both in the author's controls and in the probe.

### Tests: CLEAN (one SUGGESTION)

- **Author suite at head.** 337/337 (`receipts/head_parser.log`). The increment from base 268 (`receipts/base_parser.log`) is 30 + 15 + 24, as stated.
- **Head suite against base RTL.** 310 PASS, 27 FAIL. All 27 are the named rx_err checks (`receipts/baseRTL_headbench_parser.log`). This reproduces the PR's planted-control figures.
- **Mutation arm at head.** 9/9 (`receipts/head_parser_mutants.log`). Every mutant must fail each named check in a `FAIL ` line; `mutation_verdict` rejects crashes and masked exits.
- **Arm against base RTL.** 2 PASS / 7 FAIL, rc 1 (`receipts/baseRTL_parser_mutants.log`). The arm is not vacuous, and the stale-word mutant misses on base as the PR states.
- **Bank-write oracle.**
  - `feed_err` splits writes at the flagged byte's edge (`sim_main.cpp:267-291`). It asserts zero after at the first byte, byte 29 and the eof byte of four types plus an Announce.
  - The recorded before/on/after cells match the PR table exactly (INFO lines in `receipts/head_parser.log`).
- **Stale-word check.**
  - Eight pairs, same and different type, using salted fields so any stale word is distinguishable.
  - The planted skipped-`w2` defect fails all eight by name.
  - The "left/outside" INFO figures match the PR table.
- **Acceptance item 4.** `feed_gap` drives `rx_err_i = 0` explicitly (`sim_main.cpp:258`); this is unchanged from base.
- **Base per-position table.** Reproduced independently: Sync 1-6, Follow_Up 0-7, Pdelay_Req 0-4 and Pdelay_Resp 1-8 writes after the flag, 0 drops and 1 event at every non-eof position.
- **Coverage gap (R616-2-S1).** A reviewer mutant that ignores the flag only on bytes past the declared `messageLength` survives the whole committed suite, 337/337. The reviewer probe catches it (`receipts/mutant_pad*.{diff,log}`). This is beyond the frozen acceptance, so it is a SUGGESTION.

### Docs: CLEAN (one RESIDUE)

- **Changed guides and READMEs.**
  - `README.md` and `docs/MANAGER.md`: the #35 risk bullets are removed. That is appropriate now that the contract is implemented and ruled.
  - `docs/HDL_DEVELOPER.md:29`.
  - `docs/INTEGRATION.md:47,60-82`.
  - `docs/TEST_DEVELOPER.md:35,94-97`.
  - `tb/verilator/parser/README.md`.
- **Source evidence.** Anchors `#L393` (`if (fin_r) begin`) and `#L475` (`OFF_FLAGS0_C + 1` flags latch) resolve to the same constructs as base `#L374`/`#L456`. `make docs` rc 0 (`receipts/head_docs.log`).
- **Counts.** No current README carries a parser count (acceptance item 3 is satisfied as stated). `make contract` rc 0.
- **PR body.**
  - The line references (`:652`, `:632`, `:113-116`, `:32`, `:52-66`) are correct at this head.
  - Its tables match the receipts listed above.
  - Acceptance item 2 cites the bank ruling.
- **Wording inaccuracy (R616-2-RES1).** One sentence states the opposite of the ruled bank contract about what refused frames leave.

## Findings

### R616-2-RES1: RESIDUE (Docs)

- **Artifacts.** `docs/TEST_DEVELOPER.md:96` ("Proves refused frames leave no stale words.") and `tb/verilator/parser/README.md:16` ("It proves refused frames leave no stale words.").
- **Authority.** The bank ruling (issue #35 comment 6105869522) and the module header `:60-66` say refused frames *do* leave words, undefined and named by no event. The check (`check_a_refused_frame_leaves_no_stale_word`) proves that none of them reaches the next accepted event; its own INFO lines show, for example, "it left 8 of its 8 words".
- **Impact.** Wording only. Code, tests, figures and the contract are correct; only the summary sentence misdescribes what is proved.
- **Exact fix.**
  - `docs/TEST_DEVELOPER.md:96`: `- Proves no refused frame's word reaches the next accepted event.`
  - `tb/verilator/parser/README.md:16`: `It proves no refused frame's word reaches the next accepted event.`
- **Verification.** Text review against `receipts/head_parser.log` INFO lines. Carry to the residue checklist.

### R616-2-S1: SUGGESTION (Tests)

- **Artifact.** `tb/verilator/parser/sim_main.cpp:1337` (`check_rx_err_on_any_byte_drops_the_frame`) and the `rx_err_arms()` frames, plus `tb/verilator/parser/mutants.py`.
- **Evidence.**
  - The swept frames all end at their declared `messageLength`, so no flagged byte ever falls in physical Ethernet padding.
  - The parser treats padding specially (`:36-38`), and a real 58-byte Sync arrives padded to 60 bytes (the suite's own padded-Sync case, `sim_main.cpp:1028`).
  - Mutant `receipts/mutant_pad.diff` gives `if (rx_err_i && (rx_sof_i || cnt_r <= 11'(OFF_MSGLEN_END_C) || cnt_r <= msg_end_r)) bad_r <= 1'b1;`. It passes the committed suite 337/337 (`receipts/mutant_pad_author_suite.log`, rc 0) and fails the reviewer probe at `ann_pad` bytes 78-82 (`receipts/mutant_pad_probe.log`).
  - The head RTL itself is correct there (`receipts/probe_head.log`).
- **Impact.** No defect today. A future change that skips padding bytes would regress the "any byte of a frame" contract without a red gate.
- **Optional outcome.**
  - Add the existing 60-byte padded Sync to the every-byte sweep, including pad bytes 58 and 59.
  - Add a mutant that ignores the flag past the declared end, and require it to fail by name.
- **Verification.** The new mutant fails the named padded-Sync checks, and the head passes.
- **Scope.** The frozen acceptance and ruling name every byte of the four types, which the suite meets literally, so this is not required for the verdict. It refines R616-1-S2.

## Prior public findings: disposition at this head

- **R617-F1 (MAJOR, round-1 head): RESOLVED.** The manager's public ruling 6105869522 amends acceptance item 2 to allow writes up to and including the flagged byte. Its four required items are met at this head:
  1. Before/on/after oracle at the first, middle and eof byte of four types (plus an Announce), with zero after asserted. Verified, and extended to every position of ten shapes with prefix equality by the reviewer probe.
  2. Refused frame then clean frame of the same and a different type, with a planted skipped-write defect failing by name. Verified 8/8, and extended to 100 pairs by the probe.
  3. Header, port documentation and integration guide state the ruled contract, and the PR body cites the ruling. Verified.
  4. R616-1-RES1 applied. Verified.
- **R616-1-RES1 (RESIDUE): RESOLVED.** The exact sentence is at `KL_gptp_rx_parser.sv:60-63`, and the PR body uses "after the flagged byte's own edge" / "up to and including". R617-1 retained the same residue; it is resolved by the same text.
- **R616-1-S1 (SUGGESTION, Docs/Tests): RETAINED.** `docs/SOURCE_EVIDENCE.md:12` still links the file without an anchor. The author declined because a checker edit is out of scope. This is optional.
- **R616-1-S2 (SUGGESTION, Tests/Robustness): RETAINED IN PART.**
  - Taken: the Announce was added to the bank-write oracle.
  - Still probe-only: padding, Pdelay_Resp_Follow_Up, Signaling, PathTrace Announce, runts and adjacency. The padding part is made concrete by R616-2-S1.
  - This is optional.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue body and the three scope rulings; module header/port; INTEGRATION receive contract; microcode bank-read map per handler; engine bank/Announce-context consumer; reviewer every-byte and 100-pair stale-word probe; tied/free equivalence; parent tie-off `:666` | R616-2 | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| RTL | CLEAN | Parser latch/sof/eof/write-gating/drop-count paths `:385-658`; lint; engine 1613 x3; tsngen 288 + 4/4; bench MII tag; stacked-refusal, stray-byte, runt-adjacency probes | R616-2 | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| Robustness | CLEAN | 2000 random multi-flag trials over ten shapes; padding, over-cap PathTrace, deferred w12, zero-gap successors in both directions, recovery after refusal | R616-2 | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| Tests | CLEAN (S1 open, optional) | Parser suite 337 at head and 268 at base; head bench vs base RTL 310/27; arm 9/9 at head and 2/7 against base RTL; oracle and stale-word INFO tables vs PR; base per-position table; `feed_gap`; reviewer padding mutant | R616-2 | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| Docs | CLEAN (RES1 recorded) | README, `docs/{HDL_DEVELOPER,INTEGRATION,MANAGER,SOURCE_EVIDENCE,TEST_DEVELOPER}.md`, parser README, module header and port, source-evidence anchors, `make docs`/`make contract`, PR body line references and tables | R616-2 | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |

## Real limits

- **Not run by this reviewer:** the full `make tb`/`make` bank, the ucpu and gasket suites (they do not build the parser), engine mutants, and the parent, builder and Yosys banks.
- **Parent identity.** The netlist and ROM-digest figures (3567 -> 3568 hierarchical, 2432 flat identical, ROM bundle digest) were not reproduced here. They rest on the author's round-1 receipts at `5b4ce397`. Round 2 changed only RTL comments, which my own tied equivalence at this head is consistent with, but it is not a parent run.
- **No published source receipts at this head.** The author's gate statement for `a70e388` is the REVIEW READY comment only; the g35-r1 receipts are bound to `5b4ce397`. My own executions at this exact head are listed above.
- **No hosted evidence.** This head has no hosted check runs or statuses, and the tree has no workflow directory. Nothing hosted executed, and nothing was skipped either.
- **Hardware.** Physical calibration NOT RUN. No hardware or field evidence exists or is claimed.
- **Simulation scope.** The evidence is parser-level plus the existing engine suite. No engine bench drives `rx_err_i`, so the engine Announce-context behaviour after a refusal comes from code reading, not simulation.
- **Shared host.** Other sessions' jobs were running on the host. Wall-clock figures are not claimed.

## Pending manager duties

- Carry R616-2-RES1 to the residue checklist. Decide on R616-2-S1, R616-1-S1 and R616-1-S2 (all optional).
- At the merge turn, build and validate the current-dev merge candidate (source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`) with the builder and native banks, and link those receipts on the PR. This is distinct from the source-head execution above.
- Own hosted/local-workflow acceptance.
- Review the parent adoption separately, including the new-pin ROM-ledger row.
- Obtain the second independent positive review before merge.

## Reproduction

- `scripts/reproduce.sh <clone> <work> <receipts>` re-runs every execution above, given pinned Verilator 5.050 as `verilator` on PATH. `scripts/verilator_jcap.sh` caps the build's `-j 0` at 4 and changes nothing else.
- `scripts/probe.sh <tree> <build>` builds and runs `scripts/probe_rx_err.cpp`.
- `scripts/equiv.sh <base> <head> <work>` runs the tied/free equivalence.
- The clone was never modified (`receipts/clone_integrity.txt`):
  - HEAD, tree and index tree are `a70e388`/`e02031a`.
  - Porcelain status is empty, with 0 blob mismatches and 0 mode mismatches.
  - The repository has 0 gitlinks, so there are no submodule gitlinks to restore.
- Tool identity is in `receipts/tools_and_context.txt`.

R616-2 FINISHED
