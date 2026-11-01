[R761] POSITIVE - exact head b9628c8963d436af0dccebb205a5241ece5d9e93

# R761-4: internal review of issue #829 / PR #831, round 4

Tree `a829a5d0d7d90994d9e334e367e967ca1ad5424d`. Delta `cfb79922..b9628c89`: one commit, `sw/builder/test_builder.py` alone, no RTL. Source base and live `dev`: `1f29f189279f9fc0132f4918e47342b87d22f33a`.

**No BLOCKER, MAJOR or MINOR is open at this head.** R762-3-F1 is closed at its cause. The shipped wiring passes in both hosted jobs that run the gate, at this exact head. The longer gate is acceptable against the docs legs' budget, and reading the source list once would not help: it saves about 4 s of about 130 s.

The one thing to know: the same gate also runs on `elaborate-gates-1`, which the assignment did not name, and that worker has much less room. See check 3 and S1.

## The three assigned checks

### 1. The gate feeds the front end the whole build context, and R762-3's plant now fails: yes

- **What the code does.** `sw/builder/test_builder.py:18331-18350` takes source list, defines and include directories from `dp_srcs.ask_authority("milan_datapath")`, puts the planted text in the datapath's own position, and asserts it appears once. `:18353-18357` reads exactly one `milan_datapath` module from the output.
- **The record it reads.** 118 sources, datapath at index 117 of 118, `ETHERNET_PACKET_PKG_SV`'s source at an earlier position, one define, seven include directories.
- **R762-3's plant.** The script is byte-identical to its published copy (sha256 `28f191b1...`). At 4 jobs on a disposable copy: rc 0, `refuse 66, accept 15, limit 5, probe 4; not as wanted: 0`. The finding's four rows are refused by name. Receipt: `receipts/probes/r762-3-plants-4jobs.log`, lines 18, 38, 48, 64.
- **16 jobs not run.** The finding's verification names 16 jobs. That would need 16 x 887 MB = 14.2 GB, above my 12 GB cap, and the job count does not change any row's answer.
- **The controls can fail.** The author's five reader mutants, re-run here: 5 of 5 red, `receipts/probes/reader-mutants.log`. My four further mutants: defines dropped, include directories dropped, the shipped text read in place of the plant, any module read as the datapath. 4 of 4 red, `receipts/probes/own-mutants.log`.
- **The extra include changes nothing today.** The gate's `-I hdl/milan` gives a whole-list read byte-identical to the build's flags alone, `receipts/probes/extra-include-compare.txt`.
- **Control count.** 43 cuts and 9 keeps match the code: 4 + 2 x 19 + 1 and 2 x 4 + 1. With the shipped text that is 53 reads, against 44 at the previous head.

### 2. The shipped wiring passes in the hosted job: yes

Executed at this exact head, read from the job logs, both with `sv2v v0.0.12` from the pinned archive:

| Job | Step | Gate line | Job result |
|---|---|---|---|
| `docs-gates-2` (125002140211) | Builder leg 1, `ALL GATES PASS EXCEPT 17 NOT RUN` | `43/43 cuts rejected, 9/9 equal spellings accepted` | success |
| `elaborate-gates-1` (125002140627) | Elaboration leg 1 | `43/43 cuts rejected, 9/9 equal spellings accepted` | success |

- `docs-gates-0`, `docs-gates-1`, `elaborate-gates-0`, `docs-check-no-git` and `wire-accountability` also succeeded.
- 17 not run is the same count as the previous head's hosted leg, so this delta moved no gate into it. The author's local replay reports 16.
- By name on a disposable copy here: same counts, rc 0, 141 s, `receipts/probes/gate1h-by-name.txt`.
- At my last readback the four workflow runs had not concluded: `docs-check`, the rtl-full shards and most of rtl-fast were still queued or running (`receipts/hosted/run-state-at-report.txt`). The manager owns that acceptance.

### 3. Run time against the 30-minute budget: acceptable on the docs legs, and do not share the source list

**What the delta costs on hosted runners.** The driver's output reaches the log in buffered bursts, so the gate has no timestamp of its own. In each pair below, the burst holding the gate opens and closes on the same lines, so the gain is the change in that stretch of gates (`receipts/hosted/gate1h-burst-bounds.txt`).

| Worker | Burst at `cfb79922` | Burst at this head | Added |
|---|---:|---:|---:|
| `docs-gates-2` | 31 s | 197 s | **+166 s** |
| `elaborate-gates-1` | 53 s | 183 s | **+130 s** |

This agrees with 28 s against 190 s for the same reads on 4 pinned CPUs here, `receipts/probes/cost-4cpu.txt`. The author's 144 to 178 s was therefore not a load artefact: the hosted cost is about the same.

**The docs legs.** Projections are `docs/testing/CI_WORKFLOWS.md:3075-3077`, with the worst added cost applied. Gate 1h runs only in builder leg 1, on the docs leg with the most room.

| Worker | Holds gate 1h | Projected | With the delta | Margin to own 1620 s | Measured, `cfb79922` then this head |
|---|---|---:|---:|---:|---:|
| `docs-gates-0` | no | 1395 | 1395 | 225 | 1384, 1418 |
| `docs-gates-1` | no | 1248 | 1248 | 372 | 1055, 664 |
| `docs-gates-2` | yes | 1073 | 1239 | 381 | 682, 1057 |

- The docs workflow's projection is unchanged at 1665 s, about 27.8 minutes, 135 s inside thirty (`:3111-3114`), because `docs-gates-0` stays the slowest worker.
- `docs-gates-2` would need a further 156 s of projected time before it set that figure. Its measured 1057 s is 743 s inside thirty minutes.
- Variation between runs is larger than the gate. Leg 1 rose by 289 s, of which the gate's stretch is 166 s. Leg 0, which this delta does not touch, fell by 400 s.

**Why reading the list once does not help.** One read, measured on the pinned front end, three runs each at load about 50 (`receipts/probes/one-read-cost.txt`):

| Part | Seconds per read | Over 53 reads |
|---|---:|---:|
| Asking the build's record (`run.sh --emit`) | 0.08 | **4 s** |
| The front end on the datapath alone | 0.60 | 32 s |
| The front end on the whole list | 2.38 | 126 s |
| The front end through the datapath only | 2.34 to 2.49 | same as whole list |

- **Caching the record** saves about 4 s.
- **Sharing the parse** is what would matter: the 1.78 s per read that the earlier sources cost, about 94 s in all. The front end keeps no macro state between runs, so sharing it means extracting that state here. That is the model of the preprocessor layer the gate's docstring says it does not contain, and this is the fix for the last finding.
- **Trimming the list** saves nothing, since the datapath is second to last.
- **Decision: keep the serial whole-list read as shipped.** If the time is ever wanted back, S1 is the route.

**`elaborate-gates-1`, which the assignment did not name.** The same leg runs there.

- **Projection for this delta:** 1353 + 130 to 166 = 1483 to 1519 s, which makes it the slowest elaboration worker in place of 1475. The workflow goes from 1745 s to 1753 to 1789 s: 47 to 11 s inside thirty minutes, against the documented 55 (`docs/testing/CI_WORKFLOWS.md:3117-3121`).
- **Projection for the whole gate,** which `dev` does not have: adding the previous head's 28 s gives 1781 to 1817 s, from 19 s inside to 17 s over.
- **Measured:** this worker has not matched its projection for reasons unrelated to this gate.

| Run | Head | Worker | Leg 1 | LiteX aggregate |
|---|---|---:|---:|---:|
| 41358009670 | this head | 1763 | 793 | 881 |
| 41349880701 | `cfb79922` | 2509 | 920 | 1479 |
| 41344712098 | `2d534bec` | 2575 | 910 | 1540 |
| 41276081605 | `dev` `1f29f189` | 2099 | 913 | 1087 |
| 41298447579 | another branch | 2159 | 918 | 1126 |
| 41324395007 | another branch | 1679 | 753 | 816 |
| 41355538924 | another branch | 1294 | 610 | 599 |

- `dev` itself ran this worker past 1800 s and its own 1620 s bound before this PR, so the delta did not create that. The LiteX aggregate, 599 to 1540 s, is what moves it.
- This head's 1763 s is inside thirty minutes and inside the job's 2700 s limit. But the slowest earlier run plus the gate's stretch is 2575 + 166 = 2741 s, 41 s past that limit. That would be a red, retriable timeout, not a false pass.
- I do not hold this against the delta. The projected bounds still hold for the delta, and the measured overrun predates it. The owner should see the figure, so it is S1 and a manager duty.

## Findings

**No BLOCKER, MAJOR or MINOR.**

### Residue (wording only; no effect on the verdict or any lens)

| ID | Lenses | Path | Defect | Exact fix |
|---|---|---|---|---|
| R761-4-RES1 | Docs | `sw/builder/test_builder.py:18313-18314` | "The gate's keeps fail if no earlier source defines it any more" names only the keeps. With the macro gone a cut row fails first, because cuts run before keeps: `receipts/probes/reader-mutants.log`, row 5 | Replace with: "The gate's cuts and keeps fail if no earlier source defines it any more." |

The delta adds no bench lane label, lane name, round, reviewer ID or comment ID to a source comment.

### Suggestions (no effect on coverage)

- **S1, Tests, `sw/builder/test_builder.py:18482-18493`: run the gate's reads across four workers if the owner wants the time back.** On 4 pinned CPUs under other host load, four workers took 99.0 s against 190.2 s serial, with every control answering correctly (`receipts/probes/cost-4cpu.txt`). Peak is about 3.5 GB. It saves about 90 s on `elaborate-gates-1`, the worker with little room. The docs legs do not need it.
- **S2, Docs, PR #831 body, "What it costs".** It predates the push, so it holds only local figures. Add: "Hosted at this head, the stretch holding the gate grew by 166 s on `docs-gates-2` and 130 s on `elaborate-gates-1`. The gate also runs on `elaborate-gates-1`, whose workflow projection moves from 55 s to 11 to 47 s inside thirty minutes."

## Prior public findings at this head

I read these after my own pass over the diff.

| Finding | Disposition | Evidence |
|---|---|---|
| R762-3-F1, MINOR, Tests and Docs: a dead arm under an earlier source's macro passed | **Closed at its cause**, by its option 1 | Check 1. The four rows are committed at `test_builder.py:18436-18442` and refused. The docstring at `:18319-18330` and the PR body's Round 4 state the new reach and the limit |
| R761-3 S3, macro case | **Closed** | Same change |
| R761-3 S3, the rest | **Retained as a suggestion** | Not touched |
| R762-3-R1, R761-3 RES1: the README does not say the builder gates need the front end | **Retained as residue** | `README.md:281` still reads `python3 + pyyaml`; not in the delta |
| R761-3 RES2: "Used by" omits gate 1h | **Retained as residue** | `syn/ooc/dp_srcs.py:70` unchanged |
| R762-3-S1, R761-3 S1 and S2 | **Retained as suggestions** | Deliberate escapes. The manager's ruling makes a new contrived escape residue, and I searched for none |
| R762-3-S2: the workflow comment gives an older reason for installing the front end | **Retained as a suggestion** | `.github/ci-templates/docs.yml:164-166` unchanged |
| R761-2 S1, R762-2-S1, R762-2-S2, R761-2 S2, R761 S4 and S5, R762-S1, R762-S3 | **Retained for their own Issues** | Unchanged by this delta |
| R761-1 F1 to F7, R762-1 F1 to F8 and R1 to R4, R761-2 F1, R762-F9, R762-F4 | **Stay closed** | The delta touches none of their artifacts apart from gate 1h, which is stronger |

**A behaviour change the PR already states:** a second plane in a module other than the datapath is no longer counted, and a plane only in a never-instantiated module is now refused as `0 planes`. Both are consistent with the gate's stated purpose, and the first is a committed control. I take no finding on it.

## Clean lenses

```text
[R761] PASS Conformance — hdl/milan/milan_datapath.sv:92-93,8885-8886 and #829 acceptance — the defaults and bindings the gate holds are unchanged; no RTL and no acceptance text moved
[R761] PASS RTL — git diff --name-only cfb79922..HEAD lists only sw/builder/test_builder.py — no RTL in the delta, so the prior verdict stands
[R761] PASS Robustness — test_builder.py:18331-18357 — missing front end, parse refusal, non-unique datapath in the list and a module count other than one each go red by name; a read past 300 s raises and goes red
[R761] PASS Tests — test_builder.py:18385-18495 with receipts/probes/{r762-3-plants-4jobs,reader-mutants,own-mutants}.log — 9 of 9 reader mutants red, plant script not as wanted 0
[R761] PASS Docs — test_builder.py:18313-18330 and PR #831 body, Round 4 — purpose and limit stated and consistent with the code; RES1 and S2 carried
```

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:92-93,8885-8886`; #829 acceptance; R762-3-F1's required outcome; hosted gate lines in `receipts/hosted/gate1h-burst-bounds.txt` | R761-4 for the delta; R761-3 and earlier for code it does not touch | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| RTL | CLEAN | Delta file list, no file under `hdl/`; prior RTL verdict unaffected | R761-4 for the delta; R761-2 and R761-3 for the RTL | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| Robustness | CLEAN | `test_builder.py:18331-18357`; author's no-front-end and locale receipts, hashes reconciled; `receipts/probes/one-read-cost.txt` | R761-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| Tests | CLEAN, S1 optional | `test_builder.py:18385-18495`; `receipts/probes/r762-3-plants-4jobs.log`, `reader-mutants.log`, `own-mutants.log`, `gate1h-by-name.txt`, `extra-include-compare.txt`; hosted jobs 125002140211 and 125002140627 | R761-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| Docs | CLEAN, RES1 carried, S2 optional | `test_builder.py:18313-18330`; PR #831 body, Round 4 and its published copy; `docs/testing/CI_WORKFLOWS.md:3073-3121`; `README.md:281`; `syn/ooc/dp_srcs.py:70` | R761-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |

## Evidence checks

- **Packet.** All 24 author-round-4 files I fetched equal their `published_sha256` in the evidence `MANIFEST.json` at `e3b28a3a`. Three differ from the author's `INDEX.md` only through path redaction: their `original_sha256` equals the INDEX hash.
- **No signature found.** The evidence commit and this head both report as unsigned, and the evidence tree holds no detached signature. What I verified is the manifest's hashes, not a signature.
- **Live PR body.** It equals the published `author-r4/PR-BODY.md` apart from one blank line.
- **Front end.** `sv2v v0.0.12`, from an archive whose sha256 starts `ff8c9eea5bc029b372fb`, the value in the workflow's cache key.
- **Clone restored.** No probe touched this clone's tracked bytes; every plant and mutant ran on a copy under the scratch directory. At the end: HEAD and tree as above, status clean, index and tree agree on blob hashes and modes, and the six submodule gitlinks match their checked-out commits (`external` is not initialised, as at the start).

## Real limits

- **Hosted cost is bounded, not timed.** The figures are burst-to-burst gains, on single runs of shared runners. The gain sits inside a stretch of other unchanged gates, so runner variation is in it.
- **Local timings ran under other host load**, 30 to 100. The three 4-CPU runs ran side by side on separate CPU sets.
- **Workflow projections add measured gains to a table measured at earlier heads.** They show the direction and size, not a forecast.
- **The 16-job timeout in the author's packet.** I did not reproduce it. 16 reads need more memory than the author's unit's 10.7 GB throttle, and its peak stood just above that throttle, so memory pressure is the likely cause. That is an inference, not a measurement. The gate itself reads serially.
- **The reach is the front end's.** Neither Yosys nor Vivado was run on a plant in this round, and no full bank was run.
- **Not re-run here:** the author's `docs.yml` replay. I read its table and verifier result, rc 0.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Conduct, for the record.** A filesystem-wide name search for the pinned front end walked the manager's private tree and printed one path under it. I read and ran nothing from there, and used the shared read-only copy under the tools directory. That search and one log fetch outran their foreground limits; I stopped the search and replaced the fetch, and no result here comes from either. One cleanup command ended only its own shell.

## Pending manager duties

- Hosted and local-replica acceptance at this head. The four runs had not concluded at my last readback.
- Validate the current-dev merge candidate (builder and native banks) and link its receipts. No manager source bank ran at this head and I claim none.
- The external review at this head. This report is the internal half only.
- Carry R761-4-RES1, R762-3-R1 and R761-3 RES1 and RES2 to the residue checklist.
- Show the owner the `elaborate-gates-1` figures in check 3, and take or decline S1 on that basis. The worker's overrun on `dev` predates this PR and is not this PR's to fix, but this PR adds to it.
- Physical calibration and the tap-out check stay owed through #583.

R761-4 FINISHED
