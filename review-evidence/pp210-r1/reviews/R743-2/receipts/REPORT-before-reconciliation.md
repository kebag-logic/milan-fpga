[R743] NEGATIVE - exact head 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc

# R743-2: delta review of protocol-processor PR #211 (issue #210, part of milan-fpga #797), round 2 over `18a4dc1`

- Exact head `0ea635ea22eeb6d97335c4e814eede1ac0d67ebc`, tree `1833cde6be59abcfb24e1ba5b461c8fa8159fc2b`. Source base `a9e84b66`. The previously reviewed head is `18a4dc1`. The delta is six commits, 12 files, +165/-34 (`git diff --stat 18a4dc1..0ea635e`).
- Verdict basis: the round fixes every named finding at the page it cited, and the new derived checks work. I planted each drift the manager asked for (a fake µISA operation, a dropped target, an added target) and the gate caught every one with rc 1 (`make` rc 2). One MINOR finding remains, R743-2-F1. The cause of R744-1-F2 is a µISA count restated by hand that drifts from `ucpu_pkg.sv`. One other Markdown restatement of that count is still wrong: the retirement banner of the concept page says "a different 29-operation ISA in `hdl/aecp/ucpu_pkg.sv`". The enum declares 30. Every other item is resolved or is a suggestion.

## Findings

### R743-2-F1: MINOR. The concept page's retirement banner still says the tree has a "29-operation ISA"; `ucpu_pkg.sv` declares 30 (R744-1-F2's cause, not closed)
- **Lenses:** Docs, RTL.
- **Where:** `IEEE_1722_1_Hardware_Protocol_Processor.md:18`, in the quoted banner's "The tree does" column: "a different 29-operation ISA in [`hdl/aecp/ucpu_pkg.sv`](hdl/aecp/ucpu_pkg.sv); [06 §8](docs/architecture/06_aecp_engine.md) records which sketch operations were dropped and why".
- **Authority and evidence:** `hdl/aecp/ucpu_pkg.sv:49-88` `ucpu_op_e` declares 30 members, from `OP_NOP = 5'd0` to `OP_SHIFT_R = 5'd29`. `KL_aecp_ucpu.sv:681-684` executes `SHIFT_R`. The 06 §8 page this banner links to now says "µISA (30 operations)", and the gate holds it to that count (`receipts/plant-derived.txt` D0, D7). The banner is the page's pointer to its replacement (issue #210 scope, "banner it with a pointer to its replacement"). Its right-hand column states what the tree does today, so the body's superseded status does not excuse it. This is the same count R744-1-F2 found wrong in 06. The manager's rule for this round says such a count is derived or linked, not restated. The author searched "every current page's … 'N operations'" (author-r2 HANDOFF), but this banner sits on a superseded page and is written "29-operation". The new gate does not cover it either (`receipts/plant-derived.txt` L3: rc 0 with the text present). Neither this PR nor its "Not fixed here" list changes or flags it. `ucpu_pkg.sv:14` and `:48` say 29 too, but those are source comments, and the PR body flags them correctly.
- **Impact:** the start-here page's Retired link leads a reader to this page. Its banner, the one part the PR presents as true of the tree, contradicts `ucpu_pkg.sv` and the 06 page it points at. This is a count, not wording, so under the "unsure, MINOR" rule it is not RESIDUE. It also means R744-1-F2 is closed at 06 but not at its cause.
- **Required outcome:** remove the count and keep the link. For example: "a different ISA, the `ucpu_op_e` enum in [`hdl/aecp/ucpu_pkg.sv`](hdl/aecp/ucpu_pkg.sv); [06 §8](docs/architecture/06_aecp_engine.md) lists it and records which sketch operations were dropped and why". Writing "30-operation" would also be true, but it would be one more unguarded restatement. Optionally, add the banner to the inventory's derived checks.
- **Verification:** `git grep -nE '\b29[- ]operation' -- '*.md'` returns only `docs/10_RESOURCE_AND_EFFORT.md:536`, a historical statement in a superseded page's body. `make check` passes.

### Suggestions (do not affect the verdict)
- **R743-2-S1 (Robustness, gate):** `target_findings` reads only the first `^check:` line. Make merges every rule line for a target. In probe L1, a second `check: newgate` line passes the inventory gate (rc 0), while `make -p` shows `newgate` among `check`'s prerequisites. In probe L2, a backslash continuation fails closed. Two ways to close the gap: take the prerequisites from `make -pn check`'s database, or refuse a second `check:` line.
- **R743-2-S2 (gate):** `uisa_ops` takes a member's 06 spelling from a comment that opens with an upper-case word (`// BRANCH_IF_STATUS`). A future comment that opens with an ordinary capitalised token, such as `// NOTE …`, would rename that operation. The gate would fail closed, not pass wrongly. A stricter marker, such as `// 06: BRANCH_IF_STATUS`, would remove the ambiguity.
- **R743-2-S3 (PR text):** the PR body says "Planted mutants at head". The author's handoff says they ran on a clone of `06c934b`, which differs from the head by one README line. This review reproduced the same mutants at the exact head (`receipts/plant-derived.txt`), so no claim is wrong. Naming the commit the mutants ran on would make the provenance exact.
- Carried and not taken: R743-1-S1 to S4 (row link versus path, `*.MD`, `stale` issue number, the Milan §4.2 citation). The author recorded them as not taken. They remain suggestions.

## Prior findings at this head

| Finding | State | Evidence at `0ea635e` |
|---|---|---|
| R744-1-F1 (= R743-1-F4): 02 cites 802.1Q §34.6.1.1 | **RESOLVED** | `02_interfaces.md:283-289` now cites §34.3(d), §34.3.2, §34.3(c) and §34.6.1. I read each against 802.1Q-2014. §34.3(d) says operIdleSlope "is used by the credit-based shaper algorithm (8.6.8.2) as the idleSlope for the corresponding queue", and the page quotes this exactly. §34.3.2 says that if SRP is supported, operIdleSlope is "determined solely by the operation of SRP". §34.3(c) says adminIdleSlope "has no effect" if SRP is in operation. §34.6.1 sets a stream's idleSlope "to the bandwidth requirement of the stream". The standard has no §34.6.1.1 (its TOC lists 34.6.1 and 34.6.2). `git grep '34\.6\.1\.1' -- '*.md'` now returns only the superseded `docs/10_RESOURCE_AND_EFFORT.md:583`. |
| R744-1-F2 (= R743-1-F5): 06 µISA 29 operations, no `SHIFT_R` | **RESOLVED at 06; its cause is retained as R743-2-F1** | 06 `:1427` says 30. `:1434` lists `SHIFT_R` in Data. Its note ("shifts the 64-bit operand right, logically, by `imm[5:0]`") matches `KL_aecp_ucpu.sv:683` `opa_e_r >> uop_e_r.imm[5:0]`. The table now equals the enum, and the gate holds both. The concept page's banner still restates 29 (F1 above). |
| R743-1-F1: README counts two retired pages | **RESOLVED** | `README.md:28-30` now links to [Retired](docs/INVENTORY.md#retired) and gives no count. The anchor exists (`docs/INVENTORY.md:71` `## Retired`), and the link gate passes. |
| R743-1-F2: 02 summary, every CDC the integrator's | **RESOLVED** | `02_interfaces.md:8-11` now says "the integrator's but one: with P-EN-IDENTIFY-NOTIFICATION = 1, `identify_button_i` passes the processor's own two-flop synchronizer (§2 rule 3)". The RTL agrees: `KL_aecp_notify.sv:1022` `if (EN_IDENTIFY_NOTIF_P) begin : gen_ident`, `:1031-1032` `ASYNC_REG` `btn_q1_r`/`btn_q2_r`, `:1096-1097`. |
| R743-1-F3: `tb/nvm_port` `make` runs seven builds, not three | **RESOLVED** | `tb/nvm_port/README.md:6-9` now says the suite runs at each deadline bound, then the harness at each of its bounds, and that the Makefile's `BUILDS` counts them. This matches `Makefile:45-51` (`run`: three `suite` builds, then `fuzz_at` over `FUZZ_TMOS`) and `:41` `BUILDS = $(words 1 2 3 $(FUZZ_TMOS))`, which is 7. The summary also stays true when the bounds change. |
| R743-1-F6: diagram 22 cites §9.2.1.1 and 100 ms | **RESOLVED by disclosure** (the alternative R743-1 offered) | The SVG text is unchanged at `:155`. The PR body's "Not fixed here" now lists it with file:line and the suggested replacement text. Issue #210's scope allows "Fix each, or flag it with file:line". It is still for the manager to carry. |
| R743-1-RES1: three lane labels | **RESOLVED** | 00 `:577`, `:588` and the `tb/pp_top/README.md:2728` heading are now plain issue references. `git grep '#lane'` is empty. |
| R743-1-RES2: glossary carries a value | **RESOLVED** | `GLOSSARY.md:87` now says "far fewer clocks" and keeps the link to the HDL guide §7. |

## Derived-check probes (`receipts/plant-derived.txt`, script `scripts/plant_derived.sh`, disposable clone of the exact head restored after each)

| Plant | Gate result |
|---|---|
| D0 control, unmodified | rc 0, `inventory: 63 Markdown files, OK` |
| D1 fake operation `OP_FAKE = 5'd30` added to the enum | rc 1: `says 30 operations, the enum declares 31`; `table lacks FAKE` |
| D2 `stale` row dropped from 09 §7 | rc 1: ``table lacks `stale` `` |
| D3 `inventory` row dropped from 09 §7 | rc 1: ``table lacks `inventory` `` |
| D4 `newgate` added to the `check:` rule | rc 1: ``table lacks `newgate` `` |
| D5 06 put back to its `18a4dc1` text | rc 1: `says 29 operations, the enum declares 30`; `table lacks SHIFT_R` |
| D6 `SHIFT_R` removed from the Ops cell but still in Notes | rc 1: `table lacks SHIFT_R` (only the Ops column is read) |
| D7 heading says 31 | rc 1: `says 31 operations, the enum declares 30` |
| D8 `MOVE` listed twice | rc 1: `table names MOVE twice` |
| D9 `make inventory` with D1 | rc 2 |
| L1 second `check:` rule line (limit) | rc 0, though `make -p` merges `newgate` into `check` (S1) |
| L2 backslash-continued `check:` rule | rc 1, fails closed |
| L3 the concept banner's "29-operation" (present at head) | rc 0: not covered (F1) |
| End state | head `0ea635e`, only the untracked venv symlink |

The self-test runs 25 cases, 22 planted faults and 3 clean controls, all named (`receipts/gates-head/make_check.log`). The derived checks are not vacuous. Each of their failure modes (missing enum, unparsed member, missing heading, table or rule, missing defining file) is caught by a self-test case, and against the real tree by D1 to D9.

## Gates at the exact head (`receipts/gates-head/`, script `scripts/gates.sh`)

| Gate | rc |
|---|---|
| `make check` (wavedrom 2.0.3.post3 in a scratch venv, Mermaid CLI 11.16.0): lint, wavedrom-check, links, matrix, reqtags, modmatrix, params, aecpcmd, ids, figures, inventory (self-test 25 cases OK; 63 files OK), stale | 0 |
| `python3 scripts/gen_matrix.py --check` | 0 |
| `python3 scripts/check_upc_map.py` | 0 |
| `python3 scripts/check_m9_opcodes.py --selftest`, then plain | 0, 0 |
| `./scripts/lint_hdl.sh` (pinned Verilator, identity `Verilator 5.050 2026-07-01 rev v5.050`) | 0 |

`tb/nvm_port` figures gate: I extracted every README-derived input (135 claim regexes with their match counts and matched text, 137 figure spans, arm rows, the matrix, size claims against 393, claim-coverage problems). The output is byte-identical at `18a4dc1` and at the head, and it reports no problems (`receipts/nvm_port-readme-inputs-{18a4dc1,HEAD}.json`, script `scripts/nvm_readme_inputs.py`). The measuring half reads only RTL and suite sources, and the delta changes none of them.

## Lens results (delta)

| Lens | Result | Evidence |
|---|---|---|
| Conformance | CLEAN | The delta's only clause change is 02 §4.1. Each of its four citations, §34.3(c), §34.3(d), §34.3.2 and §34.6.1, matches the 802.1Q-2014 text, and the operIdleSlope quote is word-exact. No other clause text changed. R743-1-F6 is resolved by disclosure as the issue's "flag it with file:line" allows, so the round-1 Conformance findings F4 and F6 are closed. |
| RTL | UNCLEAN (F1) | 06 µISA set equals `ucpu_pkg.sv` (30, gated). `SHIFT_R` semantics match `KL_aecp_ucpu.sv:681-684`. The 02 CDC statement matches `KL_aecp_notify.sv:1022-1097`. No RTL, generator, test source or workflow byte changed. The Makefile change is comments only, and the only other non-Markdown change is the gate script, which no build reads. The concept banner's count contradicts the enum (F1). |
| Robustness | CLEAN | The new derived checks fail closed on every malformed input probed (D1 to D9, L2). The one pass-through is a second `check:` line, a limit outside today's tree (S1). The comment fallback is fail-closed (S2). The round-1 robustness verdict on the original gate stands, because the delta does not change those code paths beyond prefixing the derived findings. |
| Tests | CLEAN | R743-1-F3 is resolved against `tb/nvm_port/Makefile:41-51`. The figures gate's README inputs are byte-identical. No suite, tally or test source changed, so the round-1 suite runs (34 of 34 at `18a4dc1`) still describe these bytes. The adp_engine mutation-record change alters only reference text in a row no tooling reads. |
| Docs | UNCLEAN (F1) | All 11 changed Markdown and Makefile files were read. The README, 02, 06, nvm_port, glossary, inventory and 09 statements were checked against the tree. Label scan of the delta's added lines: no lane, round, reviewer, issue-comment, tool or model label is added. Lane-word count across Markdown is 18 at base, 4 at `18a4dc1` and 0 at the head. R-labels stay at 156. One of them (`review R406-1 F-1`) sits on the changed `tb/adp_engine/README.md:330` row but predates the PR, and the PR's "Not fixed here" discloses the 156 R-labels. The replacement "the change for issues #52, #59, #61, #62, #63 and #83" is consistent: AD8 and AD9 came in `ca49b56` via PR #150, which the tree already names this way at `09:242` and `tb/adp_engine/README.md:291`, `:332`. The delta's gate-script and Makefile comments carry no labels. F1 is open. |

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 802.1Q-2014 §34.3 (a) to (d), §34.3.1, §34.3.2, §34.6.1, TOC of §34.6; `02_interfaces.md:278-290`; PR body "Not fixed here" for diagram 22 | R743-2 (delta), R743-1 (rest) | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| RTL | UNCLEAN (F1) | `ucpu_pkg.sv:14,48-88`; `KL_aecp_ucpu.sv:681-684`; `KL_aecp_notify.sv:1022-1097`; Makefile delta; concept-page banner | R743-2 | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| Robustness | CLEAN | `scripts/check-doc-inventory.py` delta (`uisa_ops`, `uisa_findings`, `target_findings`, `derived_findings`, self-test); 12 plants plus control | R743-2 (delta), R743-1 (rest) | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| Tests | CLEAN | `tb/nvm_port/Makefile`, README summary, figures-gate README inputs at both heads; `tb/adp_engine/README.md:330` | R743-2 (delta), R743-1 (suite runs) | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| Docs | UNCLEAN (F1) | all 12 changed files; `docs/INVENTORY.md` Retired; concept-page banner; label scan of added lines; label counts at three revisions | R743-2 | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |

## Published evidence checked
- milan-fpga `6c494404…/review-evidence/pp210-r1`. I recomputed SHA-256 for `author/HANDOFF.md`, `author/PR-BODY.md`, `author-r2/HANDOFF.md`, `author-r2/PR-BODY.md` and `reviews/R743-1/REPORT.md`, and each equals its `MANIFEST.json` `published_sha256` (`receipts/evidence-hash-check.txt`). GitHub reports the evidence commit as `unsigned`. The packet's integrity therefore rests on the manifest hashes and the commit ID, not on a commit signature.
- The author's round-2 gate and mutant claims (`author-r2/HANDOFF.md` §Gates) agree with my exact-head runs. The consumer-gate claims (milan-fpga PR #805) were not re-run here.
- Hosted runs at the exact head (`receipts/hosted-check-runs-0ea635e.json`, read 11:47 UTC): `docs-gates` succeeded and `portability` succeeded in both runs (41049665225, 41049671908). `suites` was `in_progress` in both, so I make no claim for that job.

## Real limits
- `tb/pp_top`, `tb/srp_top`, the mutation campaigns and the full `make -C tb/nvm_port figures` were not run. Their inputs are unchanged by construction, and the README-input equivalence is shown above. The hosted `suites` job, which runs them, was still in progress.
- The standards were read only at the clauses listed. Other pages were not re-swept beyond the restated-count search that found F1.
- The search for restated tree-defined counts was a grep, not a proof. The patterns used are in this report.
- No physical calibration or hardware was involved. No manager source bank ran at this head, and none is claimed or inferred.

## Pending manager duties
- Hosted and act acceptance at the exact head, including the `suites` job (`make -C tb/nvm_port figures` and the campaigns).
- The current-dev merge candidate (source base `a9e84b66`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks at the merge turn.
- Carry diagram 22, the `ucpu_pkg.sv:14,48` comments, the source-comment clause numbers, the two `tb/pp_top` source-comment lane labels and the 156 R-labels (all disclosed in the PR's "Not fixed here") to their tracking work.
- A new head must close R743-2-F1 and be re-reviewed. Two independent positive reviews are still required.

## Receipts and scripts
- `scripts/gates.sh <checkout> <outdir>` runs the gates. Put a `python3` that imports the pinned wavedrom, and the pinned Verilator, first on `PATH`. `scripts/plant_derived.sh <head-clone> <out> <old-rev>` runs the derived-check plants and restores the clone. `scripts/nvm_readme_inputs.py <tb/nvm_port dir>` prints the figures gate's README inputs. Run it with `python3 -I` from outside the tree.
- `receipts/final-integrity.txt`: the review clone is at the exact head and tree with an empty status. The index equals the tree, blob IDs and modes included. The repository has no submodule gitlinks.
- Disposable clones, the worktree, the venv, the standard's text extraction and the downloaded evidence stayed under `scratch/` and are not published.

R743-2 FINISHED
