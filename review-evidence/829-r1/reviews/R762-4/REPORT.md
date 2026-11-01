[R762] POSITIVE - exact head b9628c8963d436af0dccebb205a5241ece5d9e93

R762-4, external independent review of #829 / PR #831. Tree `a829a5d0d7d90994d9e334e367e967ca1ad5424d`. Round-4 delta only: `git diff cfb79922..HEAD`, one commit, `sw/builder/test_builder.py` alone, no RTL. There is no open BLOCKER, MAJOR or MINOR at this head. R762-3-F1 is closed. One new wording residue and one suggestion are below.

## The three requested checks

### 1. The gate reads the build's whole list, and R762-3's plant now fails: yes

- `sw/builder/test_builder.py:18339-18349` gives the front end the record's defines, include directories and all 118 sources in order, with the text under test in the datapath's own place. The datapath is last in that list and the macro's source is earlier (positions 117 and 58, `receipts/gate1h-cost-split.log`, `soc-list-vs-record.log`).
- `scripts/plant_gate1h_r3.py`, sha256 equal to my R762-3 manifest, at 8 jobs with the pinned front end: `refuse 66, accept 15, limit 5, probe 4; not as wanted: 0`, rc 0, 64 s. The finding's four rows are each refused by name (`receipts/plants-r762-3-at-head.log`).
- With the shipped text, the gate's read equals the build's read byte for byte once the path-bearing `// Trace:` comment lines are removed, over all 1,621,234 remaining bytes and for the datapath's module alone. So the extra `-I hdl/milan` and the moved copy change no code the gate reads (`receipts/gate1h-equiv-and-mutants.log`).
- My own reader mutants, none of them from the author's five, all turn the gate red by name: no defines, no include directories, and the shipped file left in the list with the once-only assert removed and with it kept (`gate1h-equiv-and-mutants.log`, `gate1h-mutant3.log`). The author's five are published and I did not repeat them.
- The SoC's own list, `_MILAN_DATAPATH_SOURCES` at `sw/litex/milan_soc.py:553`, also has the datapath as its last row and the macro's source earlier (row 79 and row 14 of 80 rows). The order of other rows differs from the record, so the gate's reading holds on that route for this macro, not by identity of the lists (`receipts/soc-list-vs-record.log`).

### 2. The shipped wiring passes in the hosted job: yes, in the job that has finished

- `docs-gates-2`, run 41358009659, exact head: `sv2v v0.0.12`, `[gate 1h mutation] 43/43 cuts rejected, 9/9 equal spellings accepted`, `ALL GATES PASS EXCEPT 17 NOT RUN`, job success (`receipts/hosted-docs-gates-2-gate1h.log`). R762-3 explained the 17th row, gate 38, no Verilator on this runner.
- `elaborate-gates-1` runs the same leg. Its builder step ended `success` at this head in 793 s, but the job was still in its LiteX step at my last read, so I have the step's conclusion and not its log line.
- Locally by name: pinned `v0.0.12` rc 0 in 143.0 s at load 47, and `v0.0.13` rc 0 in 151.3 s at load 32, each `43/43` and `9/9` (`receipts/gate1h-by-name.log`, `gate1h-by-name-sv2v-0.0.13.log`).

### 3. The run time: acceptable, and reading the source list once is not worth doing

**Where the time goes** (`receipts/gate1h-cost-split.log`, load 47):

| Item | One call | Over the gate's 53 reads |
|---|---:|---:|
| `ask_authority`, which reads the source list | 0.10 s | 5.3 s, 3.7% of 143 s |
| Front end, datapath alone (the old read) | 0.72 s | 38 s |
| Front end, whole list (the new read) | 2.7 s | 143 s |

Reading the list once and sharing it saves about 5 s. The rise is the front end parsing 117 other sources on each read, about 2 s a time. Sharing that needs a macro prefix or similar model of the preprocessor, which is what `syn/ooc/dp_srcs.py:40-65` records as broken three times and removed. So I do not ask for it.

**The added cost.** Local: 143.0 to 178.5 s against 38.9 to 41.0 s, so 104 to 140 s. Hosted upper bound: the leg's first output block, which contains gate 1h's line, flushed 197 s after the leg's start at this head and 31 s at `cfb79922`, so at most 166 s (`receipts/hosted-docs-gates-2-gate1h.log`). The block's time also covers the gates before it, so this bounds the gate and does not measure it. Its 883 MB read runs one at a time inside the gate.

**Against the docs budget** (`docs/testing/CI_WORKFLOWS.md:3075-3077`, `:3111-3114`):

| Figure | Before | With the hosted bound added |
|---|---:|---:|
| `docs-gates-2` projected, own bound 1620 s | 1073 s, margin 547 s | 1239 s, margin 381 s |
| `docs-gates-0`, the slowest worker; runs no builder leg | 1395 s | 1395 s, 156 s above `docs-gates-2` |
| Workflow projection, `docs-gates-0` + 270 s | 1665 s, 27.8 min | **unchanged**, 135 s inside 30 min |

Gate 1h is not on the docs workflow's slowest worker, so it does not move that projection.

**Hosted spans, in seconds** (`receipts/hosted-docs-legs-by-head.txt`, `hosted-baseline-jobs.txt`, `hosted-step-spans.txt`, `hosted-final-snapshot.txt`):

| Item | dev `1f29f189` | `2d534bec` | `cfb79922` | this head |
|---|---:|---:|---:|---:|
| `docs-gates-2` job | 1043 | 676 | 682 | 1057 |
| its builder leg, with gate 1h | 614 | 404 | 406 | 695 |
| `docs-gates-1` builder leg, no gate 1h | not read | 999 | 987 | 587 |
| `docs-gates-0` job | 1387 | 1184 | 1384 | 1418 |

The leg's 289 s rise is more than the gate's bound, and the leg without gate 1h fell 400 s on the same run. Runner variation therefore exceeds the gate's cost, and one run does not isolate it. All three workers stayed inside 1620 s: `docs-gates-2` by 563 s and `docs-gates-0` by 202 s. `docs-gates-0` at 1418 s plus the same 270 s is 1688 s, 28.1 min.

**The other worker that runs this leg.** Adding the same bound to `elaborate-gates-1`'s table row gives 1353 + 166 = 1519 s, or 1789 s and 29.8 min for that workflow's projection: inside 30 min by 11 s, and now its slowest worker. That row no longer describes the hosted job, for a reason outside this delta; see R762-4-S1. At this head the builder step took 793 s, below 920 and 910 on the PR's prior heads and 913 on dev. With 873 s elapsed when the LiteX step began, and that step's longest time on this PR at 1540 s, the job projects to about 2423 s against its `timeout-minutes: 45`, 2700 s. That is a projection, not a finished run.

**The 16-job overrun.** The author's overrun was in the plant script, not the gate, which reads one at a time. 16 reads at 883 MB is about 14.1 GB, above the unit's 10 GiB throttle and 12 GiB cap, and the author's receipt shows the peak at that throttle (`author-r4/receipts/gates/load-and-memory.txt`). That is consistent with memory pressure, not shown to be the cause. It also shows my R762-3 verification command's `16` was too many for this limit; 8 jobs ran in 64 s. An overrun of the 300 s limit goes red, not green, and one read has about 110 times that margin.

## Findings

No BLOCKER, MAJOR or MINOR.

### R762-4-R1: RESIDUE

- **Lenses:** Docs
- **Path:** `sw/builder/test_builder.py:18313-18314`
- **Evidence:** the comment says "The gate's keeps fail if no earlier source defines it any more". With the macro undefined, the two cut controls fail first and the keeps are never reached (`author-r4/receipts/plants/gate1h-reader-mutants.log`, row "a macro no earlier source defines"). The gate does go red, so this is wording only.
- **Impact:** a reader looks at the wrong controls when that failure appears.
- **Exact fix:** `gate's keeps fail` becomes `gate's controls fail`.
- **Verification:** read the line.

### R762-4-S1: SUGGESTION

- **Lenses:** Docs
- **Path:** `docs/testing/CI_WORKFLOWS.md:3079`, `.github/workflows/elaborate.yml:247,484`
- **Evidence:** the table projects `elaborate-gates-1` at 1353 s against its own 1620 s bound. Hosted, that job took 2099 and 2096 s on dev and 2575 and 2509 s on this PR's two prior heads, because its LiteX step took 1087 s on dev and 1540 and 1479 s on those heads. This PR's `scripts/run_litex_sims.sh` comment names an added `padtrace-mii` target; I did not measure that target apart.
- **Impact:** the worker has been above its stated bound since before this PR and the table does not show it. Its real margin to the 2700 s job timeout was 125 to 191 s on the prior heads. Gate 1h is not the main cause and its share is small, but it spends that same margin.
- **Outcome suggested:** its own Issue, to re-project this worker or split the LiteX step. This does not gate this delta.
- **Verification:** the finished exact-head job's span against 2700 s, then a re-projected table row.

## Prior findings at this head

| Finding | State | Evidence |
|---|---|---|
| R762-3-F1, Tests and Docs | **Closed**, by its option 1 | `test_builder.py:18339-18349`, committed controls `:18436-18442`, `:18466-18467`; the plant above. The docstring's narrowed claim `:18321-18329` matches what was run |
| R762-3-R1, R761-3 RES1, Docs | **Retained, wording residue** | `README.md:223,252,281` unchanged. The fixes stated at R762-3 stand |
| R761-3 RES2, Docs | **Retained, wording residue** | `syn/ooc/dp_srcs.py:70` unchanged. The fix stated at R761-3 stands |
| R762-3-S1, Tests | **Retained, suggestion** | Its four `probe` rows are still accepted (`plants-r762-3-at-head.log:58-59,74-75`) |
| R762-3-S2, Docs | **Retained, suggestion** | `.github/ci-templates/docs.yml:164-166` unchanged |
| R761-3 S1, S2, Tests | **Retained, suggestions** | The delta adds neither check. The manager accepts the stated limit |
| R761-3 S3, Docs | **Macro case closed**; the `SYNTHESIS` `else` and `genvar` cases **retained** | Controls above. The manager accepts the stated limit |
| R761-2 S1, R762-2-S1, R762-2-S2, R761-2 S2, R761 S4, S5, R762-S1, R762-S3 | **Retained for their own Issues or the manager** | The delta does not touch them |

## Lens results

```text
[R762] PASS Conformance — git diff cfb79922..HEAD (no change at test_builder.py:18303-18311); receipts/gate1h-equiv-and-mutants.log — no protocol behaviour, wiring figure or acceptance criterion moves in the delta, and the shipped datapath module reads the same, so the prior verdict stands
[R762] PASS RTL — git diff --stat cfb79922 HEAD -- hdl (empty); receipts/gate1h-equiv-and-mutants.log — no RTL changed; the gate's read of the shipped module equals the build's apart from path comments
[R762] PASS Robustness — test_builder.py:18331-18357; receipts/gate1h-by-name-sv2v-0.0.13.log, gate1h-equiv-and-mutants.log, author-r4 gate1h-no-front-end.log and locale logs — missing front end, missing recipe, front-end refusal, overrun and module count other than one each fail closed; both front-end versions pass
[R762] PASS Tests — test_builder.py:18385-18495; receipts/plants-r762-3-at-head.log, gate1h-mutant3.log, gate1h-equiv-and-mutants.log, author-r4 gate1h-reader-mutants.log — counts re-derived (43 = 4 + 19 x 2 + 1; 9 = 4 x 2 + 1; 53 reads), new controls can fail, reader mutants go red
[R762] PASS Docs — test_builder.py:18313-18330; live PR #831 body, round 4 section, against author-r4/PR-BODY.md figures and receipts — the narrowed claim and stated limit match what was run; R762-4-R1 and retained residue are wording only
```

The comment rule holds: the delta's added lines name no bench lane, review round, reviewer ID or comment ID (`receipts/comment-rule-grep.txt`). Commit message: one line, no trailer; `git diff --check` rc 0.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta at `test_builder.py:18303-18311`; `gate1h-equiv-and-mutants.log`; issue #829 acceptance and scope comments | R762-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| RTL | CLEAN | empty `hdl` diff; `gate1h-equiv-and-mutants.log` | R762-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| Robustness | CLEAN | `test_builder.py:18331-18357`; `gate1h-by-name-sv2v-0.0.13.log`; author no-front-end and locale receipts | R762-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| Tests | CLEAN, suggestions optional | `test_builder.py:18385-18495`; `plants-r762-3-at-head.log`; `gate1h-mutant3.log`; `gate1h-equiv-and-mutants.log`; `hosted-docs-gates-2-gate1h.log` | R762-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |
| Docs | CLEAN, residue carried | `test_builder.py:18313-18330`; live PR body; `README.md:223,252,281`; `syn/ooc/dp_srcs.py:70`; `CI_WORKFLOWS.md:3075-3114` | R762-4 | `b9628c8963d436af0dccebb205a5241ece5d9e93` |

RTL and Conformance rest on the earlier rounds' verdicts for code this delta does not touch. I did not re-review that code in this round, as the token rule assigns.

## Real limits

- **Hosted, at my last read (23:05 UTC, `receipts/hosted-final-snapshot.txt`):** `docs-gates-0`, `-1`, `-2` and `elaborate-gates-0` finished with success, with no failed or cancelled job. `elaborate-gates-1` and most `rtl-full` shards were still running, and `docs-check` and `rtl-fast` were not finished. I make no claim for those.
- **The hosted gate time is a bound.** The logs carry block-flush times, not per-gate times.
- **The packet is not signed in a way I could check.** GitHub reports the evidence commit `e3b28a3a` and this head as unsigned, and the packet holds no signature file. What I verified is hashes: all 170 `author-r4` rows of `MANIFEST.json` match published bytes; 98 `INDEX.md` rows match directly, and the other 69 are path-redacted rows whose original hash equals the index (`receipts/packet-verify.txt`).
- **The reach is the front end's.** No plant went through Yosys or Vivado. The SoC comparison in check 1 reads the list in `milan_soc.py`; it does not run that build.
- **Reading scope:** as this round's focus assigns, I read the delta, the author-r4 packet, `AGENTS.md`, the `CI_WORKFLOWS.md` budget section, the issue body and its correction and owner-decision comments. I did not re-read `CONTRIBUTING.md`, `docs/README.md` or the linked requirements; the delta touches none of what they govern.
- **Not run:** full builder, parent, Yosys or Verilator banks, Docker or `act`, hardware. No manager source bank exists at this head and I infer none. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **My clone:** the probes wrote only `__pycache__` directories there, which I removed. It matches the head: tree, index, modes and the six gitlinks (`receipts/restore-verify.txt`). I wrote my verdict and ledger before opening R761-3 (`receipts/independent-pass-before-prior-findings.md`), and I did not read R761-4.

## Pending manager duties

- Read `elaborate-gates-1`'s finished exact-head span against 2700 s, and the remaining hosted contexts; hosted and local-replica acceptance stay with the manager.
- Carry R762-4-R1, R762-3-R1, R761-3 RES1 and RES2 to the residue checklist.
- Update the PR body's "hosted runs pending" line when those runs finish. The author's "hosted cost unmeasured" can now cite the figures in check 3.
- Build and validate the current-dev merge candidate, with builder and native banks, and post-merge containment. Source base and live `dev` were both `1f29f189` at my last read.
- Physical calibration and the tap-out check stay owed through #583.

R762-4 FINISHED
