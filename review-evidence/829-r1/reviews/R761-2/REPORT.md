[R761] NEGATIVE - exact head 2d534bec9348557a9407d3024c0b199c0ebc8bce

Tree `8ed7e82fcd001d9965a3e6bd9f33b741dae4dbf0`, issue #829, PR #831, round R761-2. Delta reviewed: `4cda0aa0..2d534bec`, 10 commits. Base and live dev: `1f29f189279f9fc0132f4918e47342b87d22f33a`.

**One MINOR holds this head; everything else from round 1 is closed.** All seven of my round-1 findings and all eight of the external round's are closed at their cause. The RTL delta is comment-only, by my own comparison. The style and idiom gates pass here and in hosted `docs-gates-0`. The one open finding is in the new gate 1h: it stays green when a binding or default is commented out, which is a cut of the wiring it exists to hold.

## Findings

### F1. MINOR. Lens: Tests
- **Where:** `sw/builder/test_builder.py:18311-18324` (`_datapath_shape_findings`), read by gate 1h at `:18345`.
- **Authority and evidence:** AGENTS section 6, `Tests`: each new test can fail for the defect it claims to detect. The gate's docstring says `milan_datapath` hands the plane the shape the SoC states. Its regexes read raw text, comments included. I planted 17 cuts: 12 were refused and 5 accepted.

| Plant | Gate 1h |
|---|---|
| Binding deleted, tied to a literal, crossed, scaled, or moved to another parameter | Refused, by name |
| Default moved, parameter made a localparam | Refused, by name |
| Second plane, instance renamed | Refused |
| `// .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),` | **Accepted** |
| `// .ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),` | **Accepted** |
| The tick binding inside `/* */` | **Accepted** |
| The tick binding inside a dead `ifdef` | **Accepted** |
| The real default commented out, with a live default of 40 below it | **Accepted** |

  The whole gate also returns rc 0, `7/7 cuts rejected`, on a real `milan_datapath.sv` with either binding commented out. Receipts: `receipts/gate1h/plants.log`, `real-comment-tick.log`, `real-comment-octet.log`. Deleting either binding fails it, rc 1, by name: `real-cut-tick.log`, `real-cut-octet.log`.
- **Impact:** a commented-out binding elaborates without error, because the plane falls back on its GMII default. On MII the plane then expects 45 clocks while the observer measures 90, the visible failure of this issue. Round 1 found no other reader of those bindings, so this gate is what holds them. The RTL is correct today; the defect is a false green in the gate.
- **Why it is not residue:** it changes what a test can detect.
- **Required outcome:** gate 1h reads the text with comments removed, and a commented binding and a commented default each join its planted cuts. A dead preprocessor arm is either refused or named as a limit in the gate's own comment.
- **Verification:** `scripts/plant_gate1h.py <tree>` reports the four comment plants as REFUSED, and the gate's mutation line counts the new cuts. The dead `ifdef` plant is REFUSED or stated as a limit.

### Residue (wording only; these do not affect the verdict or any lens)

| ID | Where | Defect | Exact fix |
|---|---|---|---|
| RES1 | `sw/litex/milan_soc.py:2092-2096` | "That is what makes..." now follows the sentence about MII, so "That" reads as if the MII exception were the reason | Move the sentence starting "That is what makes" directly after "the reset that clears the LiteEth transmit side.", and end the comment with the `eth_rst` sentence |
| RES2 | `sw/builder/test_builder.py:18301-18304` | "Cut a binding and ... every frame is lost unmeasured" is true of the octet binding only. Cutting the tick binding leaves the distance at 90 and makes the correction wrong by 93 x 32 ns = 2976 ns | "Cut the octet binding and the plane expects 45 clocks against the observer's 90, and every frame is lost unmeasured. Cut the tick binding and the correction is wrong by 2976 ns." |
| RES3 | PR #831 body, Known limitations, lifecycle bullet | "See [Round 2]" points at a section that says nothing about that test | Replace with "See #833." |
| RES4 | `tb/verilator/gptp_txts/README.md:76-79` | A hand wrap leaves "queued" alone at a short line end | Re-wrap the paragraph |

### Suggestions (no effect on coverage)
- **S1. Gate 1g shares F1's blind spot.** A commented-out MII entry in `milan_soc.py` returns no finding (`receipts/gate1h/gate1g-comment.log`). The delta only changed that gate's comment, so this is not a finding here. A shared comment-stripping helper would close both gates.
- **S2. Decide whether attribution of the routed effect is wanted.** One route of `dev` at the merge turn would separate this PR's effect from the record's older baseline. See check 8.

## Prior findings at this head

| Prior item | State | Evidence at this head |
|---|---|---|
| R761-F1, R762-F1: style gate | **Closed** | `check_doc_style.py` and `--selftest` rc 0 here; hosted `docs-gates-0` success, step "Concise audience documentation gate" success |
| R761-F2, R762-F2: idiom ratchet | **Closed** | `check_cpp_idiom.py` rc 0, `build without warnings: 0 <= 0`, self-test 75 of 75; hosted step "C and C++ idiom gate" success; no ratchet raised |
| R761-F3, R762-F7: GMII `ready` | **Closed** | Check 3 |
| R761-F4, R762-F8: fragment check | **Closed** | Check 4 |
| R761-F5, R762-F3: PHC window arm | **Closed** | Check 4 |
| R761-F6, R762-F6: figures | **Closed** | Check 8 |
| R761-F7, R762-F5: check's name | **Closed** | Check 4 |
| R762-F4: no gate on the shape wiring | **Closed for the cut it named; F1 is new** | Deleting either binding now fails a named check; F1 covers the comment form the new gate misses |
| R761 RES1, R762-R4 | **Closed** | `sim_main.cpp:14-15` reads "at 80 MHz and at 100 MHz" |
| R762-R1 | **Closed** | Export: `eth_rst` drives the PHY reset's preset through `milansoc_milanmac_phy_eth_reset` on GMII. `milan_soc.py:1646` builds the MII PHY with no `ext_reset` |
| R762-R2 | **Closed** | `GPTP_PLANE.md`, `KL_gptp_shadow.sv:91-93`, PR limitations |
| R762-R3 | **Closed** | PR bench table reads "range 631 to 675 ns" |
| R761 S1, R762 S2: inter-frame gap; R761 S2, R762 S4: lifecycle test | Filed as #832 and #833, both open, out of scope here | `author-r2/QUESTIONS.md` read |
| R761 S3 | **Closed** | Check 7 |
| R761 S6 | **Closed** | After my full run neither `obj_dir/Vgptp_txts_sim` nor `obj_mii/Vgptp_txts_sim` exists |
| R761 S4, S5; R762 S1, S3 | Optional, not taken, no finding | Noted in the handoff |

## The eight checks

1. **Round-1 findings:** see the table above.
2. **Style and idiom gates: pass.** Local receipts are in `receipts/gates/style-idiom.log`. Hosted `docs-gates-0`, `-1` and `-2` succeeded on run 41344711894 at this exact head. `docs_check.py`, `gen_toc.py --check`, `check_gptp_docs.py` and `git diff --check` against the base also rc 0 here. The rest of the hosted bank was still running when I stopped: 19 succeeded, 1 skipped, 30 in progress or queued (`receipts/gates/hosted-status.txt`).
3. **GMII `ready`: correct everywhere, and the "cannot move" sentence is gone.** The export shows `reg milansoc_milanmac_phy_sink_ready = 1'd0`, set to 1 each clock and cleared by `eth_tx_rst`. The observer's reset is `maceth_tx_rst`, whose preset is `eth_tx_rst | milansoc_milanmac_eth_rst`, so it asserts with that reset and releases two clocks later. So `ready` is already 1 when the observer leaves reset, as the text says. A sweep of the plane, the SoC, the builder, the suite and the changelog finds no remaining "constant" or "folds away" about it. The other "cannot move" lines in `test_builder.py` are about unrelated subjects. Receipts: `receipts/ready/`.
4. **The three checks now bite.**
   - **Fragment:** the check reads `45 * kEthCycPerOctet`. `mii_delta_forced_not_measured` is caught in my run, and the published receipts show the same defect green under the old check and red under the new one.
   - **PHC window:** `pad_at_first_symbol()` is the low nibble after the delimiter on MII and octet 8 on GMII, which matches the oracle's `ref_ns`. My guard series on the MII build:

     | Guard, cycles | First-symbol frame's own result | Reload check | Suite |
     |---|---|---|---|
     | 188 | **Fails**, with "the history guard counted it" | Fails | Fails |
     | 189 | Passes | **Fails** | Fails |
     | 202 | Passes | **Fails** | Fails |
     | 203, shipped | Passes | Passes | Passes |
     | 204 | Passes | **Fails** | Fails |

     The controls at 170 and 202 are in the 13 caught. The 188.5-cycle interval sits exactly where the result check turns, so the load really is at the window's early end.
   - **Bias:** the name states 1.754 ns on MII and one nanosecond on GMII, and the controls follow it.
   - **Other probes:** the suite passes 95 of 95 at MII system-clock arguments 18, 24 and 31, so the new arms are not sensitive to the clock. Cutting the record's refusal bit alone stays 95 of 95 on MII. That is not a test gap: `KL_gptp_txret.sv:605-613` also compares the measured distance, so the frame is refused either way.
5. **Gate 1h: partly.** It refuses every deletion, tie, crossing, default move and instance change I planted, and accepts the comment and dead-`ifdef` forms. That is F1.
6. **Comment-only RTL: confirmed.**
   - Only `KL_gptp_gmii_launch.sv` and `KL_gptp_shadow.sv` differ under `hdl/`. Their preprocessed forms hash identically to `4cda0aa0`'s, and `milan_soc.py`'s AST is identical.
   - I re-exported AX7101 at both heads from clean clones. With comments and the clone path normalized, both are 29720 lines with sha256 `a52117bb...`, IDENTICAL.
   - The same comparison against the base differs by exactly one line, `.gmii_tready_i (milansoc_milanmac_phy_sink_ready)`.
   - The converted plane is byte-identical when conversion starts from the comment-free preprocessed text, the only input on which I reproduce the author's IDENTICAL line; the author's receipt does not state its input (`receipts/commentonly/plane-sv2v-detail.log`).
   - From the raw sources, 7 of 4764 converted lines differ. All 7 are source line numbers inside message strings of `KL_gptp_gmii_launch.sv` and `KL_gptp_shadow.sv`, moved by the longer comments. With those locations removed the output is identical. This changes no logic, so it is not a finding, but "byte-identical" holds for the comment-free input only.
   - Receipts: `receipts/commentonly/rtl-compare.log`, `receipts/export/compare.log`.
7. **Citation: correct.** I read IEEE 802.1AS-2020. 11.3.9 is "Event message timestamp point": "the beginning of the first symbol following the start of frame delimiter". 11.3.2 is "Message types contained in each message class". 8.4.3 is the generation of event message timestamps, and its Note 1 covers the correction. No `11.3.2` remains in the plane, its documents, the suite or the SoC.
8. **Figures: trace.**
   - 13 controls at this head (6 + 7) and 10 at `4cda0aa0` (6 + 4), read from each commit's `mutants.py`. My run ends `controls: 13 failures: 0`.
   - The published comparison shows 126 lines equal and 0 different, and states that it compares `4cda0aa0` with the bench branch. The route logs behind it are not published; their hashes are.
   - The sweep total adds up: 361,121 + 1,525,511 + 284,228 + 21,575 = 2,192,435. All four shard records name this head with exit code 0.

### Is the record comparison enough?

**Yes for the acceptance as written; no as evidence that the default is unchanged, and the PR does not claim that.**

- **The elaborated default is not unchanged.** It has one new live connection, and because `ready` is a flop the observer's enable cannot fold away. In a generic mapping of the observer at its defaults, flops stay at 342 and LUTs go from 235 to 242 (`receipts/netlist/observer-map.log`). That is an indicative mapping, not the vendor's result.
- **The acceptance says GMII behaviour, not netlist.** Behaviour rests on other evidence, none of which the delta touches: the one-line export difference, round 1's formal equivalence of observer and ledger with `ready` high, the reset ordering in check 3, and a full GMII run with no octet held.
- **The route record shows only that the image still passes its gate.** It cannot attribute anything. FF +394 against the record cannot come from the observer, which adds none, so most of the movement likely belongs to the record's older baseline. WNS fell 0.204 ns to +0.236 ns, and slices are 15841 of 15850, on one placement.
- **What it leaves open.** No stated gate requires a `dev` route, so its absence is not a finding. The real risk is the thin slice margin at the next change, not this PR's behaviour. S2 is how to settle attribution.
- **One thing for the owner to see.** The 2026-11-01 14:10 decision says the AX7101's "shipping image must not change". I read that as scoped to the writable-correction build key, but this PR does change the image by that one connection. The PR says so plainly.

## Other checks
- **Comment rule:** no lane label, review round, reviewer ID or comment ID in the added lines. No U+2014 in them either.
- **Commits:** 10, each one line with no trailer.
- **Published packet:** all 959 `MANIFEST.json` entries match by sha256, with none missing (`receipts/gates/packet-manifest-verify.log`). The evidence commit `d8dfbe0c` is unsigned on the host, so this shows integrity against the manifest, not a signature.
- **Prose rewrite:** I read the `GPTP_PLANE.md` and `CHANGELOG.md` rewrite line by line against the old text. Every figure and fact is preserved. The one deliberate change is "no other link speed is qualified", replaced as R762-R2 asked.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 802.1AS-2020 11.3.9, 11.3.2, 8.4.3 against the PR and RTL banners; #829 acceptance; `receipts/suite/head-make.log`, pad oracle 95 of 95 on all three runs | R761-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| RTL | CLEAN | `KL_gptp_gmii_launch.sv`, `KL_gptp_shadow.sv` comment-only; AX7101 export reset chain; `receipts/commentonly/rtl-compare.log`, `receipts/export/compare.log`, `receipts/netlist/observer-map.log` | R761-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| Robustness | CLEAN | `receipts/guard/`, `receipts/probe/mii-q18.log`, `mii-q24.log`, `mii-q31.log`, `refusal-bit-cut-mii.log`; `KL_gptp_txret.sv:605-613` | R761-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| Tests | UNCLEAN (F1) | `sim_main.cpp`, `mutants.py`, `Makefile`, `test_builder.py`; `receipts/gate1h/`, `receipts/guard/`, `receipts/suite/head-make.log` | R761-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| Docs | CLEAN, with RES1 to RES4 carried as residue | `GPTP_PLANE.md`, `CHANGELOG.md`, suite `README.md`, PR body, #829 REVIEW READY, `author-r2/`; `receipts/gates/style-idiom.log`, `docs_check.log`, `gen_toc.log`, `check_gptp_docs.log`, `hosted-status.txt` | R761-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |

## Real limits
- I wrote `receipts/provisional-verdict.txt` before reading any prior report. The prior findings did not change its verdict. I had already seen the author's closure table, because it is in the PR body and handoff.
- The full sweep, `behave`, the builder legs, the docs workflow table and the AX7101 route are the author's receipts. I checked their tallies and heads, and did not re-run them.
- The AX7101 route ran at `4cda0aa0`. It stands for this head through check 6. The route logs behind the 126 lines are not published.
- The formal equivalence is round 1's, on RTL that this delta does not change. The observer mapping is generic and indicative only.
- My guard series and suite build changed `-j 0` to `-j 2` in disposable copies of the Makefile to respect the job limit. The run-mii build flags were otherwise unchanged.
- I did not read the bench branch, so "14 on the bench branch" is the author's figure, already traced in round 1.
- No hardware was used. Physical calibration was NOT RUN, and the tap-out check remains owed through #583. Field skips are not hardware proof.
- The review clone is restored: head, tree, index and gitlinks verified (`receipts/clone-restored.txt`).

## Pending manager duties
- Return F1 to the author, then re-review gate 1h at the new head. The fix is confined to `test_builder.py`, so only the Tests lens has to be covered again if nothing else moves. Carry RES1 to RES4 to the residue checklist.
- Hosted and act acceptance at the new head. At this head the docs jobs are green and the rest were still running.
- The current-dev merge candidate, with builder and native banks, at the merge turn.
- Decide S2, and make sure the owner sees the one-line AX7101 change against the 14:10 decision.
- The owner's tap-out check and physical calibration, through #583.

R761-2 FINISHED
