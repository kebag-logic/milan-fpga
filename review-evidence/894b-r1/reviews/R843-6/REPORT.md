[R843] NEGATIVE - exact head d0a2a1605d7acc691936a61f9afaa0e67f4b46f2

Internal cleared-context review R843-6, issue #894 / PR #914 (lane 894b), round 13. Head `d0a2a1605d7acc691936a61f9afaa0e67f4b46f2`, tree `200d73043aefc480fc11c6d00e2689c4757077ff`. This is a narrow delta review: `8883d499..d0a2a160` (`a840c14d`, `32a9242f`, `d0a2a160`), together with every named prior finding at its cause. No approval or merge authorization is given.

**NEGATIVE, on one MINOR (R843-6-F1; lenses Conformance and Docs).** `docs/reference/FR_NFR.md:420` still says, in the present tense, that 8x8/1if's hold-off is 2,026 cs for a 70 ms `CTRL_LOOP_TX_MS` and a 69.84 ms tx row. The head states 2,027 cs, 75 ms and 74.26 ms, and those 2,026 cs would not keep 35.2.2.8's two LeaveAllTime periods at the head's row. That sentence is the one place where R844-4-F1's required documentation refresh did not land.

Everything else in the delta holds:
- R843-5-F1 and R844-4-F1 are closed at their cause in code and gates.
- R844-4-F2 is closed.
- The three prior residues took their exact fixes.
- The fix for F1 changes one sentence of an authoritative document. No code, figure in the tree, image or gate changes.

## What was checked

1. **The gate (R843-5-F1, R844-4-F1).**
   - `flip_grade.tx_held` (`tb/verilator/ctrl_service_budget/flip_grade.py:74-92`, wired into `--check` at `:446-455`) runs `rows_tiers.tx_statements` (`rows_tiers.py:557-570`) at 8x8/1if, apart from that point's reported rows.
   - In disposable copies of the head (`scripts/tx_gate_probe.py`, `receipts/tx-gate-probe-d0a2a160.txt`):
     - 8x8/1if's figure planted at 74, 70 and 60 ms is refused by name by `flip_grade.py --check --point 8x8/1if` and by `--check`;
     - 76 ms passes;
     - emptying `tx_held`'s point filter makes the self-test report its three new controls ESCAPED, 612 of 615;
     - reverting the polls to the interface count raises the row to 77.87 ms, which the gate then refuses against 75.
   - At the two held shapes (`scripts/tx_other_shapes_probe.py`, `receipts/tx-other-shapes-probe-d0a2a160.txt`), 33 ms at 1x1/1if and 104 ms at 8x8/2if are each refused by name. That confirms `ctrl_loop.h:463-466`'s new claim.
2. **The hold-off derivation.**
   - `SRP_REDECLARE_CS = 2*1000 + SRP_JOIN_CS + ceil(TX/10)` (`srp_mbx.c:36`), with `CTRL_LOOP_JOIN_CS` 19 cs (`ctrl_loop.h:436`).
   - At 75 ms that is 2,027 cs. After a JoinTime (190 ms) and the 74.26 ms row, 20,270 ms leave **20,005.74 ms** against IEEE 802.1Q-2018 35.2.2.8's 20,000.
   - At 70 ms it was 2,026 cs, leaving 19,995.74 ms (`receipts/author-packet-verify.txt`).
   - `ctrl_loop.h:355` reads `75u`. `srp_talker.cpp:55` and `:342` derive the test's hold-off and latest Leave from the same constants.
3. **The image change.**
   - The author's identity receipt (`author-r13/receipts/images/img-identity-d0a2a160.txt`) shows the six 1x1/1if, 1x1/2if and 8x8/2if images byte-identical by ELF and loadable sha256.
   - Each 8x8/1if image differs in one `.text` line: `7ea00693 li a3,2026` becomes `7eb00693 li a3,2027`, with disassembly and contents line counts equal.
   - I decoded both words myself: `addi x13, x0, 2026` and `2027`. 2,027 is exactly the new `SRP_REDECLARE_CS`.
   - The author's control receipt (`img-identity-control-8883d499-against-itself.txt`) is present.
   - I did not rebuild the images (see limits).
4. **The graders, run by me at both heads** (`scripts/graders.sh`, `receipts/graders-d0a2a160/`, `receipts/graders-8883d499/`, `receipts/graders-8883d499-vs-d0a2a160.diff`). The rc values are identical:
   - flip `--check` 1, 1x1/1if 0, 8x8/2if 1 (by design), 8x8/1if 0;
   - load `--check` 0 and shape_costs 0;
   - flip `--selftest` 0 (615 of 615);
   - rows_tiers `--selftest` 0 (1033 of 1033);
   - load `--selftest` 0 (28 of 28).

   The output differs only in four places:
   - the shapes table's 8x8/1if TX column, 70 to 75;
   - the new `HELD 8x8/1if ... 75 ms against ... 74.26 ms` line;
   - the control count, 612 to 615;
   - the load header (R843-5-R1's exact text).

   So the shape-keyed polls and notices in `rows_grade.py:160-163` and `:309-316`, and the `NEAREST` datapath events in `rows_tiers.py:187`, change no figure at 1x1/1if or 8x8/2if. This matches the author's `graders-8883d499-against-d0a2a160.txt` byte for byte.
5. **The packet.**
   - The archive `48b6c3a2`'s `MANIFEST.json` gives published sha256 equal to the bytes for 228 of 228 author-r13 files.
   - INDEX.md equals the archive's original sha256 for 227 of 227.
   - The 11 INDEX mismatches against the published bytes are exactly the 11 `path_redacted` entries.
   - The INDEX names round 13 (`receipts/author-packet-verify.txt`).
6. **The 8x8/1if legs on the 75 ms image** (author receipts, `harness/legs-32a9242f/`):
   - `srp-talker-held`, `srp-talker`, `srp-talker-loss` and the eight transmit-aged groups each have a simulation log byte-identical to round 10's, rc 0 and no STATED line;
   - the control is caught in 8 of 8 groups;
   - the gate's only findings are the seven held-egress ledger rows, "no measured instance", which these groups do not stage.
7. **Docs.**
   - Section 13 (`SPLIT_CONTROL_MEMORY.md:2765`, `:2808`, `:2814-2840`): each figure now names its image (`a15345f7`, `46cf2a7d`, `af2c4d7a`, `32a9242f`) or its in-tree derivation.
   - The current 8x8/1if rows (R4 21.39, R5 136.64, R6 132.93, first 18.98, last 387.95, R4L 208.55, ACMP 52.76, ADP 52.64, MAAP 53.91, tx 74.26, txL 159.82; load 1.034 with every command the largest) equal `author-r13/receipts/model/rows-8x8-1if-d0a2a160.txt`.
   - `MAILBOX_SPLIT.md:390` gives 0.9 ms, matching `ctrl_loop.h:340`'s `900u`. #901 is the PR that carried #895's `73388996`, so the attribution is right.
   - `FR_NFR.md:393` carries R843-4-R1's exact fix. `srp/README.md:224-231`, `tb/.../README.md:205` and `load_grade.py:567` are consistent with the tree.
   - A sweep for 69.84, 2,026 and 70 ms finds every other occurrence explicitly historical, except `FR_NFR.md:420` (F1; `receipts/fr-nfr-420-stale.txt`).
8. **Hosted evidence at the exact head:** no check runs, no workflow runs, combined status pending with 0 statuses (`receipts/hosted-checks-d0a2a160.txt`). The manager owns hosted and act acceptance.

## Findings

### R843-6-F1: MINOR. Lenses: Conformance, Docs.

**`FR_NFR.md:420` states 8x8/1if's hold-off and THE TRANSMIT's figure at their round-8 values as current.**

- **Where:** `docs/reference/FR_NFR.md:420`, the SRP/MRP row: "... 2,030 cs at two interfaces (2,029 at 99 ms), 2,023 at 1x1/1if, and 2,026 at 8x8/1if, whose `CTRL_LOOP_TX_MS` is its own tx row's 69.84 ms rounded up, 70 ms, ... IEEE 802.1Q-2018 35.2.2.8 sets only the least, 2,000 cs, and the terms above it cover the Leave's latest departure".
- **Authority and evidence:**
  - The head states `CTRL_LOOP_TX_MS 75u` (`ctrl_loop.h:355`), so `SRP_REDECLARE_CS` is 2,027 cs (`srp_mbx.c:36`; the image's `li a3,2027`), held by `flip_grade.py --check` to the 74.26 ms row (`HELD` line).
  - `srp/README.md:227` and section 13 (`:2815`) already say 2,027 and 74.26/75.
  - R844-4-F1's required outcome included refreshing the docs "still saying 69.84/70/2026". The delta's only FR_NFR hunk is `:393` (`receipts/fr-nfr-420-stale.txt`).
- **Impact:**
  - The requirements reference names, as the conforming current configuration, a hold-off that at the head's row leaves 19,995.74 ms after the Leave's latest departure, under 35.2.2.8's 20,000.
  - Its "the terms above it cover the Leave's latest departure" is then false for the figures it gives.
  - This is the same class as R844-4-F2: a current-tense figure and conformance claim, not wording.
  - The code is correct. Only the authoritative statement is stale.
- **Required outcome:** `FR_NFR.md:420` gives 8x8/1if's hold-off as 2,027 cs and its figure as 75 ms for its 74.26 ms tx row, held by `flip_grade.py --check` (`tx_held`). Any older figure can be kept only if marked historical. Suggested text: replace "and 2,026 at 8x8/1if, whose `CTRL_LOOP_TX_MS` is its own tx row's 69.84 ms rounded up, 70 ms," with "and 2,027 at 8x8/1if, whose `CTRL_LOOP_TX_MS` is its own tx row's 74.26 ms rounded up, 75 ms, held to that row by `flip_grade.py --check` (`tx_held`; 2,026 at 70 ms before the row reached 74.26),".
- **Verification:** a docs diff at that line. Re-running this report's sweep (69.84, 2,026, "70 ms" beside 8x8/1if) leaves only historical-scoped occurrences, and `docs_check` passes.

### R843-6-S1: SUGGESTION. Lens: Tests.

**`--check`'s use of `tx_held` is held by no self-test.**

- **Where:** `flip_grade.py:454` (`... + tx_held(ROOT, points) + ...` in `main`), `:173`, `:81-92`.
- **Evidence:**
  - The new controls call `tx_held` directly. Removing it from `main`'s findings leaves `--selftest` at 615 of 615 and the harness mutants (`selftest_mutants.py:482-487`) untouched.
  - With that removal and a 70 ms plant, `flip_grade.py --check --point 8x8/1if` passes (`receipts/tx-gate-probe-d0a2a160.txt`, M9 and M11).
  - The head's wiring is correct: M1 to M3 are refused through the CLI.
  - The same idiom holds `row_findings` and `rule_findings` in `main` today, so this is not new to the delta.
- **Optional:** a control or harness mutant that runs `--check --point 8x8/1if` on a planted text, or that patches `tx_held` to return nothing and requires an escape.

### R843-6-R1: RESIDUE. Lens: Docs.

- **Where:** `flip_grade.py:64-65`: "the understated figures planted at a reported point ... two of the review's and one a millisecond under the head's figure".
- **Why:** under the comment rule, source comments state behaviour and reason, not review provenance.
- **Exact fix:** "#: The understated figures planted at a reported point, each refused by name (TX_HELD_CONTROLS): well under the row (60 ms), under it by more than a millisecond (69 ms), and a millisecond under the head's figure (74 ms)."

### R843-6-R2: RESIDUE. Lens: Docs.

- **Where:** `srp_mbx.c:34-35`: "which rows_tiers.py holds at every listed point: flip_grade.py, tx_held at 8x8/1if".
- **Exact fix:** "(hold, CTRL_LOOP_TX_MS, the built design's, held at or over its tx row at every shape by flip_grade.py --check: rows_tiers.tx_statements, and tx_held at 8x8/1if), so it adds both."

### R843-6-R3: RESIDUE. Lens: Docs.

- **Where:** `sw/firmware/ctrl/test/srp_talker.cpp:53`: "20,230 ms at one interface, 20,300 at two". 8x8/1if is also one interface, and its hold-off is 20,270 ms at this head (20,260 before it).
- **Exact fix:** "20,230 ms at 1x1/1if, 20,270 at 8x8/1if and 20,300 at two interfaces."

### R843-6-R4: RESIDUE. Lens: Docs.

- **Where:** `SPLIT_CONTROL_MEMORY.md:2816`: "At 70 ms the check refuses the head's costs, 74.26 ms."
- **Exact fix:** "A 70 ms figure is refused against the head's tx row, 74.26 ms."

### R843-6-R5: RESIDUE (PR text). Lens: Docs.

- **Where:** the PR #914 body, status paragraph: "Nothing has been pushed; the manager owns publication and the base synchronization for PR #914 (`894-8x8-1if` -> `894-tiers`)".
- **Why:** the head is published, and the PR's base is `dev-soft-core`.
- **Exact fix:** "The manager published this head and owns the base synchronization for PR #914 (`894-8x8-1if` -> `dev-soft-core`)." If `894-tiers` is the intended lane base, state that instead.

## Prior public findings at this head

| Finding | Status at d0a2a160 | Evidence |
|---|---|---|
| R843-5-F1, MINOR (Tests, Docs): 8x8/1if's `CTRL_LOOP_TX_MS` held by no gate | **RESOLVED**, option (a) | `tx_held` refuses 60, 69, 70 and 74 ms by name through the CLI; its controls escape when it is disabled (M10). `ctrl_loop.h:463-475` now names the real guard. |
| R844-4-F1, MAJOR (all five lenses): figure 70 under the 74.26 row, hold-off 19,995.74 | **RESOLVED** in code, images and gates. Its docs refresh is **incomplete at one line**, carried as R843-6-F1 | 75 ms and 2,027 cs leave 20,005.74 ms. The image differs in the one immediate. The understatement control at 8x8/1if is independent of the reported rows. `ctrl_loop.h:327-328` and `:467`, and section 13 `:2814`, are refreshed. `FR_NFR.md:420` is not. |
| R844-4-F2, MINOR (Conformance, Docs): older images' figures given as the head's | **RESOLVED** | Section 13 `:2765`, `:2808` and `:2829-2840` are scoped by image. The share-pass result is marked historical. The current rows equal the in-tree derivation. MAILBOX_SPLIT gives 0.9 ms. |
| R843-5-R1, RESIDUE: load header "owed to the pin move" | **RESOLVED** | `load_grade.py:567` carries the exact text. |
| R843-5-R2, RESIDUE: packet index round | **RESOLVED** | author-r13 INDEX reads "round 13". |
| R843-4-R1, RESIDUE: FR_NFR "as on each image before it" | **RESOLVED** | `FR_NFR.md:393` carries the exact fix. |
| R843-5-S1 and S2, SUGGESTION (Tests): walk-copy plants, environment seed | Retained, optional | `srp_listener_mutants.py` and `srp_listeners.cpp` are not touched by the delta. |
| R843-4-S1, SUGGESTION: packet F1 check by substring | Retained, optional | Packet tooling. |
| R843-2-S2 and R843-3-S2, SUGGESTION (RTL, Robustness): two-interface AECP debug arms | Retained, optional | Not touched by the delta. |

## Per-lens results

```text
[R843] UNCLEAN Conformance - docs/reference/FR_NFR.md:420 against ctrl_loop.h:355, srp_mbx.c:36 and IEEE 802.1Q-2018 35.2.2.8 - R843-6-F1: the requirements reference gives 2,026 cs / 70 ms / 69.84 ms as current; the code's 75 ms and 2,027 cs (20,005.74 ms after the latest Leave) and the gate are correct
[R843] PASS RTL - no HDL in the delta; ctrl_loop.h:338-375 THE SHAPES and srp_mbx.c:26-36 at d0a2a160; author-r13 img-identity-d0a2a160.txt (six images byte-identical, 8x8/1if one immediate 7ea00693->7eb00693, decoded) - the firmware change is one compile-time constant with its one derived immediate
[R843] PASS Robustness - flip_grade.py:74-92,446-455 and rows_tiers.py:557-570 at d0a2a160; receipts/tx-gate-probe-d0a2a160.txt (M1-M11) and tx-other-shapes-probe-d0a2a160.txt - boundary plants (74 refused, 76 passes, 75 holds at 74.26), wrong-derivation plants (polls at the interface count refused at 77.87) and the held shapes' plants refused by name
[R843] PASS Tests - flip --selftest 615/615, rows_tiers --selftest 1033/1033, load --selftest 28/28, shape_costs 25/25 run by me at d0a2a160 (receipts/graders-d0a2a160/); TX_HELD_CONTROLS escape when tx_held is disabled (M10); author receipts for the harness self-test (0 failures), the SRP campaign (436 ok, 0 escaped, talker-hold-off plants among them) and the 8x8/1if legs - S1 optional
[R843] UNCLEAN Docs - docs/reference/FR_NFR.md:420 - R843-6-F1; otherwise SPLIT_CONTROL_MEMORY.md:2765-2840, MAILBOX_SPLIT.md:390, FR_NFR.md:393, srp/README.md:224-231, ctrl_service_budget/README.md:205, load_grade.py:567 and the delta's source comments checked against the tree and receipts; residues R1 to R5 recorded with exact fixes
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN** (R843-6-F1) | `ctrl_loop.h:355,436`; `srp_mbx.c:26-36`; `FR_NFR.md:393,420`; the hold-off arithmetic against 802.1Q-2018 35.2.2.8; `flip_grade --check` at the three points | R843-6 | `d0a2a1605d7acc691936a61f9afaa0e67f4b46f2` |
| RTL | CLEAN | no HDL in the delta; THE SHAPES `ctrl_loop.h:338-375`; `srp_mbx.c:36`; the image identity receipts, with the instruction words decoded | R843-6 | `d0a2a1605d7acc691936a61f9afaa0e67f4b46f2` |
| Robustness | CLEAN | `flip_grade.py:64-92,173,446-455`; `rows_tiers.py:127,187,557-570`; `rows_grade.py:92-97,160-163,309-316`; probes M1-M11, P1 and P2 | R843-6 | `d0a2a1605d7acc691936a61f9afaa0e67f4b46f2` |
| Tests | CLEAN | the four grader self-tests run at both heads; the probe receipts; author-r13 harness, SRP campaign and legs receipts; `srp_talker.cpp:51-55,330-345` | R843-6 | `d0a2a1605d7acc691936a61f9afaa0e67f4b46f2` |
| Docs | **UNCLEAN** (R843-6-F1) | `SPLIT_CONTROL_MEMORY.md:2765-2840`; `MAILBOX_SPLIT.md:390`; `FR_NFR.md:393,420`; both READMEs; `load_grade.py:567`; the delta's comments; the PR body; the packet INDEX and MANIFEST | R843-6 | `d0a2a1605d7acc691936a61f9afaa0e67f4b46f2` |

Code the delta does not touch keeps its prior lens verdict. The delta touches the constant `FR_NFR.md:420` depends on, which is why that line is judged here.

## Real limits

- **Images not rebuilt.** Rebuilding needs the lane's harness-built flash maps and runtimes and the buildroot toolchain, which are not public inputs. The one-immediate claim rests on the author's identity receipt, its self-control and my decoding of the two words.
- **Not re-run by me:** the harness self-test, the SRP campaign, firmware-unit and coverage, the docs workflow and the 8x8/1if legs. I read their author receipts by section. The self-test receipt shows 0 FAIL lines, "self-test: 0 failures" and rc 0; its line prefixes do not spell the 931/259 totals directly. The SRP receipt shows 436 `[ok]` and 0 escaped.
- **`srp_talker.cpp` at 8x8/1if:** it is not compiled at that shape in any arm the author lists. The hold-off at 8x8/1if is covered by the formula, the image immediate and the gate, not by a unit run at that shape.
- **Known, not findings:**
  - campaigns not re-run at this head, listed in the PR body;
  - `twin` and `twin-plants`, owed to PR #935;
  - R4 and the other every-source rows at 8x8/1if, owed to #872 (tx 74.26 against the MRPDU's 49 ms is among them);
  - the timing floor, owed to #818;
  - physical calibration NOT RUN, and field skips are not hardware proof.
- **Outside this delta:** the hold-off covers the tx row, not txL (159.82 ms at 8x8/1if). That is the ruled design at every shape (`rows_tiers.tx_statements`' docstring), and this round did not re-review it.
- **No manager source bank at this head.** There is no hosted evidence at the exact head (0 check runs).

## Pending manager duties

- Route R843-6-F1 (a one-line authoritative-doc correction). Under the freeze rule, record it with the composition lane if #914 is not changed again.
- Carry R843-6-R1 to R5 to the residue checklist.
- Validate the current-dev merge candidate (source base `7398ec0a`, live dev `6b66f66d`) with the builder and native banks, and link the receipts. Hosted and act acceptance for this head, and the PR #935 dependency for `twin`, remain the manager's.

## Packet

Every listed receipt and script is in `MANIFEST.sha256` (paths relative to this packet).
- **Scripts:** `scripts/graders.sh`, `scripts/tx_gate_probe.py`, `scripts/tx_other_shapes_probe.py`, `scripts/verify_author_packet.py`.
- **Receipts:** `receipts/` holds the grader outputs at both heads and their diff, the probe receipts, the packet verification, the FR_NFR evidence, the hosted query and the clone's integrity.
- **The clone after the probes:** HEAD and index tree at `200d7304`, 0 changed paths, and the submodule gitlinks unchanged (`receipts/clone-integrity.txt`). Every probe ran in disposable copies under `scratch/`.

R843-6 FINISHED
