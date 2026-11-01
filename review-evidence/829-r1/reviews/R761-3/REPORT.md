[R761] POSITIVE - exact head cfb799229d3c5c695468cc1a7cad08403e57f265

Tree `ee5e690bf5af14052ef5d00bff34cecbdc8624ce`, issue #829, PR #831, round R761-3. Delta reviewed: `2d534bec..cfb79922`, 2 commits, 3 files, none under `hdl/`. Source base and live dev: `1f29f189279f9fc0132f4918e47342b87d22f33a`.

**No BLOCKER, MAJOR or MINOR is open at this head.** Both round 2 findings on gate 1h are closed at their cause. All 36 of my refusal plants are refused, on the pinned front end and on a newer one. The gate also passed in hosted `docs-gates-2` at this exact head. Two wording items and three suggestions go forward; none holds the verdict.

## The four assigned checks

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Does gate 1h read through the build's front end, and do the plants fail? | **Yes.** It runs `sv2v --pass-through` on the defines and include directories of `syn/yosys/run.sh --emit milan_datapath`, the same list `inc_flags_for` gives the portability gate (`run.sh:183-187`). 36 of 36 refusal plants refused and 6 of 6 equal spellings accepted, on v0.0.12 and v0.0.13. Missing sv2v is a refusal, rc 1. A front end that prints nothing is also a refusal, rc 1 | `plant_gate1h_r3.py`, `receipts/plants-sv2v-0.0.12.log`, `plants-sv2v-0.0.13.log`, `gate1h-no-front-end.log`, `gate1h-silent-front-end.log` |
| 2 | Is sv2v present where the gate runs in CI? | **Yes, in every job that runs it.** Gate 1h is in builder leg 1, which `docs-gates-2` and `elaborate-gates-1` run. Each fetches the source submodules and installs pinned v0.0.12 before that leg (`docs.yml:701,710,741`, `elaborate.yml:314,324,434`). **Executed, not only read:** hosted job 124977557590 at this head installed `sv2v v0.0.12`, then printed `37/37 cuts rejected, 6/6 equal spellings accepted`, and the job concluded success. The hosted `elaborate-gates-1` was still running when this was written | `receipts/hosted-docs-gates-2.txt` |
| 3 | Is the stated limit acceptable? | **Yes**, and it is narrower than it reads. See below | `receipts/plants-sv2v-0.0.12.log`, `limit_probe.log` |
| 4 | Is the residue applied, and is `milan_soc.py`'s parsed program unchanged? | **Yes to both.** The AST dump is identical to `2d534bec` while the bytes differ. The README's word sequence is also identical. Every round 2 residue item is applied or disposed of; see the prior-findings table | `soc_program_compare.py`, `receipts/soc_program_compare.log` |

### Why the stated limit is acceptable

- **A generate arm.** The gate counts planes in every arm, dead or live. A second plane in a dead arm is refused as two planes (measured), and by the same count so is any `if (x) A else B` pair. The only case left is the sole plane inside an arm that never elaborates. That is not a shape cut: no plane exists, so there is no gPTP at all. `sv2v --top=milan_datapath` converts that plant with rc 0 and no plane in its output (`receipts/limit_probe.log`), so plane presence is not something this gate or that conversion holds.
- **A `defparam`.** This is the one spelling that can override a correct binding, and the gate accepts it. Nobody writes it by accident, and a search of `hdl/`, `protocol-processor/hdl` and `gptp-processor/hdl` finds no use of it. It is the same gap R762-2-S2 named. One line would close it; see S1.
- **The round 2 requirement is met.** R761-2 F1 asked for a dead preprocessor arm to be refused or stated. It is refused. The generate and `defparam` cases are stated in the gate's docstring (`test_builder.py:18321-18322`) and in the PR body.

## Findings

No BLOCKER, MAJOR or MINOR.

### Residue (wording only; these do not affect the verdict or any lens)

| ID | Lens | Where | Defect | Exact fix |
|---|---|---|---|---|
| RES1 | Docs | `README.md:281` | The tool column reads `python3 + pyyaml`. Since this delta a plain run needs sv2v: without it the run stops at gate 1h with an assertion. `test_builder.py` itself called no sv2v at `2d534bec` | Change the cell to `python3 + pyyaml + sv2v` |
| RES2 | Docs | `syn/ooc/dp_srcs.py:70` | "Used by" names the two Tcl scripts, and gate 1h now imports this module too | Append: "Gate 1h in sw/builder/test_builder.py imports `ask_authority` and `FRONT_END`." |

### Suggestions (no effect on coverage)

These are real escapes, but each needs a deliberate edit that no accidental cut produces. I measured all of them except the macro case in S3, which comes from reading the gate's one-file command.

- **S1, Tests, `test_builder.py:18344`: refuse `defparam` by name.** The pass-through output keeps it as a code line, so one check would do: `re.search(r"^\s*defparam\b", code, re.MULTILINE)`. That closes half of the stated limit, with one added control.
- **S2, Tests, `test_builder.py:18349`: the plane count reads only a line that starts with the module name.** A second plane behind an attribute, `(* keep *) KL_gptp_shadow ...`, or under an escaped name is accepted, and the count stays at one. Count those forms too. The committed "second plane" control uses only the plain spelling.
- **S3, Docs, `test_builder.py:18321` and the PR body's limit paragraph: the limit reads as a closed list, and three more cases sit beside it.** The gate reads one configuration of one file, so:
  - `` `ifdef SYNTHESIS `` with the binding and an `` `else `` that ties it is accepted, and a reader without `SYNTHESIS` gets the tied value. The portability build reads the binding.
  - A `genvar` of the same name around the plane is accepted, because names are not resolved.
  - A macro defined in an earlier source of the read list is not visible to the gate.

  Suggested text: "It parses one file in one configuration and resolves no names, so a `defparam`, a generate arm that never elaborates, or a reader without these defines stays outside this gate."

## Prior findings at this head

I read these after my own plants had run and my verdict was formed. The author's closure text is in the REVIEW READY comment, so I had seen that summary first.

| Prior item | State | Evidence at this head |
|---|---|---|
| R761-2 F1, MINOR, Tests: gate reads comments and dead arms | **Closed at its cause** | The reader is now the front end. The R761-2 script, byte-identical to its published copy, reports `plants 17 accepted 0` (`receipts/r761-2-plant-script-at-head.log`). Committed controls cover line comment, block comment and dead `ifdef`, for both bindings and both defaults |
| R762-F9, MINOR, Tests: binding cut spelled as a comment | **Closed at its cause** | Same reader. `.X (8), // .X (param)` is a committed control. The published run of that reviewer's script reports 15 cuts, 0 not as wanted, and its hash matches the index. I did not re-run it |
| RES1, R762-2-R1: reset comment order | **Closed** | `milan_soc.py:2094-2096`: "That is what makes" follows the LiteEth reset, and the `eth_rst` sentence ends the comment |
| RES2: wiring comment | **Closed, figure re-derived** | `test_builder.py:18304-18307`. `KL_gptp_txret.sv:281` gives (90 + 2 + 2 - 1) x (40 - 8) = 2976 ns. The other two terms use the fabric tick and do not change |
| RES3: lifecycle bullet | **Closed** | The live PR body reads "See #833." It equals the published `author-r3/PR-BODY.md` except for one trailing line ending |
| RES4: README wrap | **Closed** | `gptp_txts/README.md:78`; word sequence identical |
| R762-2-R2: handoff citation | **Disposed of, not rewritten** | `author-r3/HANDOFF.md` corrects it to `:101`, and `KL_gptp_gmii_launch.sv:101` holds the clause. The round 2 packet stays as published |
| R761-1 F1 to F7, R762-1 F1 to F8 and R1 to R4 | **Stay closed** | Both round 2 reviews closed them. The delta touches none of their artifacts apart from gate 1h, which is stronger |
| R762-F4: no gate held the wiring | **Stronger** | Gate 1h now holds it through the front end |
| R761-2 S1, R762-2-S1: gate 1g has the same comment gap | **Retained as a suggestion** | Not taken, and the author says so. The delta does not touch gate 1g |
| R762-2-S2: no text gate sees every cut | **Retained**, see S1 and check 3 | An elaboration reading the plane's effective parameters remains the complete answer |
| R761-2 S2, attribution route | **Retained for the manager** | Unchanged |
| R761 S4, S5, R762-S1, R762-S3 | **Retained for their own Issues** | Unchanged by this delta |

## Other evidence

- **The gate's own reader can fail.** Five mutants of it each turn the gate red: reading raw text, dropping the defines, dropping the plane count, accepting any default, and accepting a binding that is one of several (`gate_mutants.py`, `receipts/gate_mutants.log`). A control cannot pass on a front-end parse error, because each one must name its specific finding.
- **Hosted shape.** In a fresh clone with only the three submodules the job fetches and pinned sv2v, the gate gives rc 0 in 34 s (`receipts/gate1h-pinned-clean-clone.log`). It also gives rc 0 in an empty environment with `LC_ALL=C`, though the datapath has 69 non-ASCII lines (`gate1h-bare-env-C-locale.log`).
- **Comment rule.** The added lines of the delta name no lane label, round, reviewer ID or issue-comment ID.
- **Commits.** Both are one line with no trailers (`receipts/delta-commits.txt`).
- **Author receipts.** I spot-checked 11 receipts against `author-r3/receipts/INDEX.md` and 3 files against `MANIFEST.json`, on fresh downloads. Ten receipts match the index and all 3 files match the manifest. The eleventh, `plants/gate1h-no-front-end.log`, differs from the index because the index holds its pre-redaction hash: the manifest marks it `path_redacted`, with that hash as `original_sha256` and my download's hash as `published_sha256` (`receipts/author-r3-spotcheck.log`).

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #829 acceptance and scope comments; `KL_gptp_txret.sv:281` against the gate comment's 2976 ns, `KL_gptp_shadow.sv:1036` against its 45 and 90; `receipts/delta-files.txt`, no RTL or parsed SoC change. Protocol reading stands from R761-2 at ancestor `2d534bec`, nothing in its scope having changed | R761-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| RTL | CLEAN | `receipts/delta-files.txt`, 0 files under `hdl/`; `receipts/soc_program_compare.log`; `hdl/milan/milan_datapath.sv:92-93,8880-8889` read against the gate. RTL coverage stands from R761-2 at ancestor `2d534bec` | R761-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| Robustness | CLEAN | Gate failure paths: `receipts/gate1h-no-front-end.log`, `gate1h-silent-front-end.log`, `gate1h-bare-env-C-locale.log`, and the parse-refusal rows of `plants-sv2v-0.0.12.log`. RTL robustness stands from R761-2 at ancestor `2d534bec` | R761-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| Tests | CLEAN, S1 to S3 optional | `sw/builder/test_builder.py:18314-18460`; `plant_gate1h_r3.py` with `receipts/plants-sv2v-0.0.12.log` and `plants-sv2v-0.0.13.log`; `receipts/gate_mutants.log`, `r761-2-plant-script-at-head.log`, `gate1h-pinned-clean-clone.log`, `hosted-docs-gates-2.txt` | R761-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| Docs | CLEAN, RES1 and RES2 carried as residue | `tb/verilator/gptp_txts/README.md:75-80`, `milan_soc.py:2091-2096`, `README.md:281`, `syn/ooc/dp_srcs.py:70`, the live PR body's round 3 section and limit paragraph, `author-r3/HANDOFF.md`, #829 REVIEW READY | R761-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |

## Real limits

- I ran gate 1h by name only. The figures for the full sweep, `behave`, lint, the other builder gates and the other suites are the author's at `2d534bec`, which this delta does not change in any lens-relevant way. The `gptp_txts` tally and the docs workflow table at this head are the author's receipts; I checked their hashes and did not re-run them.
- **The evidence commit `80e3b4ea` is unsigned**: its verification reason reads `unsigned`. So my receipt check shows that the published files agree with their own index and manifest, not who produced them. The hosted job above is the independent execution of gate 1h.
- The gate's define comes from the portability record. I did not run Vivado, so I did not check that the product flow defines `SYNTHESIS`.
- `ci/image/tool-inventory.json` pins a digest for `test_builder.py` that matches neither this head nor dev `1f29f189`. My search of `.github/workflows` found no reader of that file. This predates the delta and sits with retained R761 S4.
- At the time of writing, hosted `docs-gates-2`, `docs-check-no-git` and `wire-accountability` had concluded success at this head. `docs-gates-0`, `docs-gates-1`, both `elaborate-gates` jobs and the rest were still running. Nothing here stands in for them.
- Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.
- The review clone is untouched at the exact head: head, tree, index digest, tree digest, a clean status and gitlinks are recorded in `receipts/clone-restored.txt`. All plants and mutants ran in temporary files or a disposable clone.

## Pending manager duties

- Carry RES1 and RES2 to the residue checklist. Both are prose, and neither needs a re-review of a lens beyond reading the two lines.
- Decide whether to take S1 to S3 now or leave them as they stand.
- Hosted and local-replica acceptance at this head, including `elaborate-gates-1`, the other job that runs gate 1h.
- The current-dev merge candidate, with builder and native banks, at the merge turn. The second independent positive review remains required.
- The owner's tap-out check and physical calibration, through #583.

R761-3 FINISHED
