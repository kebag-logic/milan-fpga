# HANDOFF — #665 lane S5 (F2-F5 timing hooks on the target core), [A702]

STATUS: REVIEW READY at `eef3d97a` (2026-11-06), resumed 02:56 CET after the owner hold of 2026-11-05 19:17 ("after the bug fixes then continue")

## Resume (2026-11-06)

- Tree at resume: head `fa925043`, seven lane commits on `5b5f4336`; one uncommitted edit, `tb/verilator/ctrl_service_hooks/README.md` (the 100 MHz clock, the layout swing, H-DISC's undecided rule, the composed burst's scope, History of the 50 MHz figures, two limits). Kept and finished.
- `dev-soft-core` still `a68536fa`; S2b (#810) still open (now `d930ea98`, round 17), so no rebase (assignment item 3).
- Since the stop on #665: only ruling 6674728988 (S2b round 16 to 17: every MRP and notice bound must hold by construction; no bound amended). It changes nothing in this lane: the 18 ms and 20 ms bounds stand, and a fit under the layout swing is already a finding here (`NARROW`).
- Receipts found: the 16 plants at `fa925043` all complete, each `PLANT <name> caught` with rc 0 (chains A-D rc 0). The four hook runs at `fa925043` and the gate units (firmware self-test shards, S2's harness, builder) were killed by the hold mid-build: re-run in fresh build directories.
- 03:01 started 8x8 idle then answering on 0-15 (`cpu_ranges.py pick`, the only free range), 1x1 idle and answering on the lane's own 32-47.
- 03:05 removed the ignored `__pycache__` directories an earlier session left in the worktree (scratch out of the tree).
- 03:08 firmware self-test shards started on 32-47 (`fa925043` clone); all four rc 0 by 04:3x.
- 03:49 8x8 idle rc 0; 04:01 both 1x1 rc 0; 04:29 8x8 answering rc 0. No refusal, ORDER or NARROW in any.
- 04:02-04:30 S2's harness at both points, the builder, the boundary gate (both halves): all rc 0.
- 04:3x the docs check found a bare doc reference in the README's hooks table, present since `86392bd2`: linked.
- 04:4x commit `eef3d97a` (README: results, findings, history); the four runs regraded at it, rc 0, tables byte-identical.
- 04:4x docs gates (98) at `eef3d97a` rc 0; merge candidate `88a7e705` (head onto `a68536fa`, scratch clone): self-test rc 0, 1x1 idle run rc 0, same findings.
- 05:3x receipts collected (`receipts/INDEX.md`, generated); REVIEW READY.

## Resume (2026-11-05)

- Tree at resume: clean, head `3c514839`, six lane commits on `5b5f4336`; nothing lost.
- `dev-soft-core` is now `a68536fa` (PR #830, dev sync). No rebase (assignment item 3: only onto S2b if it merges first; S2b #810 is open at `a3f23bba`). `git merge-tree` of the head onto `a68536fa` is clean.
- Rulings since the stop that change this lane:
  - issuecomment-6514866239 (owner 2026-10-30 05:17): the split CPU clock is **100 MHz**, on `sys`. "S5 grades at the product clock: 100 MHz once S2b merges. Its 50 MHz figures become history." So the grade is now at 100 MHz; the 50 MHz runs recorded at `3c514839` are history.
  - issuecomment-6634982529 item 1: the composed burst with a grandmaster change at the load's first instant and every bucket full is in the SRP row's scope. At this base S2's backlog rows and this harness's composed rows already stage it (`scenario.gm_run` before `composed_load`, windows opened on full buckets).
  - issuecomment-6634982529 item 2: a fit by less than the 6,490-cycle layout swing fits by chance. Applied to the hook paths as a NARROW finding.
  - issuecomment-6630265194: the retried notice row is S2b's firmware (THE RETRY), not on this base; recorded as a limit.
- Found at resume: the 8x8 answering 100 MHz regrade at `3c514839` reports `ORDER H-DISC` on interface 1 in `acmp-disc`. Diagnosed as a false positive of the check: the sink's PROBE_TX follows a TMR_DELAY draw of 0 to 1000 ms (tsn-c-stack `ACMP_TMR_DELAY_MAX_MS`), here 672 ms, which ran past the script's next ADP record (557 ms later), where the check's window ended. Fix: an instance is decided only when a probe falls in the window or the window is longer than the delay's maximum plus two service bounds; otherwise it is counted as undecided.

- Repository: kebag-logic/milan-fpga (origin verified)
- Lane worktree: the lane's own worktree, branch `665-s5-hooks`
- Base: `origin/dev-soft-core` `5b5f433698d8832b63573b8d106f10e839a4210e` (verified: HEAD == merge-base == origin/dev-soft-core at start)
- PR target: `dev-soft-core` (manager pushes and opens it)
- Assignment: #665 issuecomment-6513150371 ([A10]); plan section S5 (A678 PLAN.md) as amended:
  T_svc = 20 ms graded per family as min(T_svc, 10 % of ceiling) (issuecomment-6495692075);
  product clock CPU 50 MHz / bus 100 MHz, plus a labelled 100 MHz CPU variant (issuecomment-6508196970).
- TAKEN posted: issuecomment-6513247351. REVIEW READY posted: issuecomment-6676840432 (2026-11-06, head `eef3d97a`; text in `REVIEW-READY-COMMENT.md`).

## Progress log

- 03:05 read the assignment, rulings and plan S5; read S2's harness (`tb/verilator/ctrl_service_budget`) and S3's (`tb/verilator/ctrl_split_boot`, `sw/firmware/ctrl/plat`).
- 03:12 TAKEN posted.
- 03:20 feasibility: S3's platform image on S2's SoC (CSR window in gateware) builds in 23 s (cached netlist) and S2's own groups (`control`, `adp-discover`, `aecp`) run and grade on it at 1x1, 50 MHz.
- 03:37 harness written: `hooks_soc.py`, `hooks_build.py`, `hooks.py`, `run.py`, `hooks_selftest.py`; self-test 18/18 checks, 20/20 mutants.
- 03:37 runs started: 1x1 50 MHz idle and answering; 03:43 8x8 50 MHz idle (development, working tree).
- 03:50-04:25 development plants: 15 of 16 caught on the first or second attempt; fixes from them:
  - H-MAAP check: a report writes AAF_CTRL twice (maap_csr.c: disable first, re-enable last), so the first version
    flagged the closing store of every unplanted report; a report is now told by its first three stores
    (AAF_CTRL, CRFT_CTRL, MAAP_CTRL); mutant "every AAF_CTRL store is a report (earlier rule)" pins it.
  - H-DISC check: the window ended at the next *tagged* ADP record, so the plant escaped (a PROBE_TX 80 ms after
    the next, untagged, AVAILABLE was counted); it now ends at the interface's next ADP record, tagged or not;
    mutant pins it.
  - H-NOTIFY plant: the notification loop rewrites the response buffer in place, so the first plant sent no
    solicited response at all (the probes went unmeasured); the plant now keeps the response aside.
  - S2's `acmp.tmr_no_adp.if1` probe is unmeasurable on the platform at 8x8 (the sink re-arms its aging timer
    after S2's mark; the 2 s expiry falls past its 1.9 s window): new group `hooks-disc-aging` measures the path
    with the window opened after the arm; the earlier probe's refusal is superseded only where that group measured
    the same path on the same interface (self-test check + mutant).
- 04:28 commit `86392bd2`; 04:31 recorded runs at it (clean clones): 8x8 idle 50, 1x1 idle 50, 8x8 answering 50.
- 04:46 commit `f5bf3677` (H-DISC window); 04:50 commit `b2d4ea80` (H-NOTIFY plant): build inputs and group
  scripts unchanged since `86392bd2` (only hooks.py grading and plant text, the self-test, README), so the
  recorded runs regrade at the head.
- 04:51 the 16 final plants at `b2d4ea80`, three chains in clean clones on the lane's CPUs.

## Progress log (resumed 2026-11-05)

- 17:38 resumed; read state, rulings 6514866239, 6630265194, 6634982529; diagnosed the H-DISC false positive (above).
- 17:58 commit `fa925043`: the product clock `sys` (100 MHz) by default, `milan` (50 MHz) as history; H-DISC's undecided rule; NARROW (layout swing); spin 120,000 turns; self-test 22/22 checks, 31/31 mutants. Scratch regrade of the recorded 100 MHz logs with the new rules: no ORDER, no NARROW; the 8x8 answering H-DISC case is 1 applied + 1 undecided; the recorded `disc-order` plant log is still caught.
- 18:05 started the two 8x8 runs at `fa925043` in clean clones (units on the lane's own range 96-111, which another lane's unit shares; `cpu_ranges.py pick` finds no free range).
- 18:13-18:30 the two 1x1 runs and three plant chains on 96-111: about 80 runnable processes on 16 CPUs, each simulation at about half a CPU (about 15 min per simulated second).
- 19:16 `cpu_ranges.py` found 0-15, 16-31 and 32-47 free. Stopped the two 8x8 runs and the plant chains (new jobs keep their cores for life, so they were restarted, not re-pinned) and restarted them: 8x8 idle on 0-15 and 8x8 answering on 16-31 (`--jobs 16`), four plant chains on 32-47. `maap-late` had finished at `fa925043` and is kept. The 1x1 runs continue on 96-111.

## Design (as built)

- New directory `tb/verilator/ctrl_service_hooks/`. S2's and S3's harness files are imported read only, never edited (S2b and S4 both edit S2's testbench, SoC and build).
- SoC: S2's split SoC + the Milan CSR window in gateware (S3's seeded words) + counter-change pads; face arm `idle` (S2's, formal) or `answering` (labelled: CTR and GSI answered at wait_cycles-1, the last cycle KL_mbx accepts; counter-change event driven).
- Testbench: S2's `sim_main.cpp`, copied into the build directory with anchored additions (the `ctrchg` step and its pads; a log line per CPU store into the Milan CSR window); each anchor must occur once.
- Image: `ctrl_plat_image.py`, two-stage map as S3; 8x8 two interfaces = ledgered `platform-8x8-two-interfaces`.
- Bound per hook: min(20, family ceiling) + W; margin to the family's normative timeout recorded.
- Ordering checks (apart from the budget), one per hook, each counting the instances it applied to.
- Plants: 16, each a scratch copy of the firmware tree (`hooks_build.planted`), never the checkout.

## Changes (file:line, reason)

All new files are under `tb/verilator/ctrl_service_hooks/` (this lane's directory); one shared file outside `tb/`.

| File:line | What | Why |
|---|---|---|
| `hooks_soc.py:76` `CsrFile` | the Milan CSR window answered in gateware (ID, VERSION, S3's seeded words, write-back, the TOD snapshot) | the platform image reads and writes the CSR window at boot (identity, policy, MAAP's report); S2's SoC has no window; in gateware so S2's testbench runs unchanged |
| `hooks_soc.py:108` `window_answer`, `:137` `FaceDrive`, `:159` `face_patch` | the answering-face arm: CTR and GSI answered at wait_cycles - 1 (the last cycle `KL_mbx.sv` win_* accepts), counter-change pads | H-COUNTERS' push reads the CTR window (`aecp_face.c` counters); without an answer it is never sent; labelled test arm, idle arm stays S2's |
| `hooks_soc.py:173` `Build`, `:189` `build` | the export: S2's split SoC from its parts, the CPU at the Milan clock or the labelled variant, the ledgered plan at 8x8 two interfaces | the S2 SoC with the platform's devices; the 100 MHz variant (#665 6508196970) |
| `hooks_build.py:44` `LEDGERED_POINTS` | `platform-8x8-two-interfaces` at 8x8/2if only | the largest shape plans 59.0 RAMB36 by ruling 6505997821 |
| `hooks_build.py:50` `TESTBENCH`, `:75` `CSR_STORES`, `:150` `testbench` | anchored additions to a copy of S2's `sim_main.cpp`: `ctrchg` step and pads; CSRW per CPU store into the CSR window; each anchor exactly once | S2's testbench, unedited in the tree (S2b and S4 edit it); H-COUNTERS start and H-MAAP's check need these |
| `hooks_build.py:100` `plant_text`, `:112` `planted` | a plant's edits applied to a scratch copy of the firmware tree, each anchor once | plants never edit the checkout (assignment: firmware is a STOP, never an edit) |
| `hooks_build.py:122`, `:210`, `:234` | the image (two-stage map as S3), the build, the reuse check (every input digest) | reproducible, attested builds and regrades |
| `hooks.py:41` `T_SVC_MS`, `:47` `NORMATIVE_MS`, `:63` `bound_ms` | T_svc 20 ms; bound min(T_svc, ceiling) + W; normative timeouts for the margin | the owner's decision and the per-family rule (6495692075) |
| `hooks.py:112` `HOOKS`, `:74` `Plant`, `:86` `SPIN` | the eight hooks: families, clauses, ordering obligation, check, late plant, ordering plant | assignment item 5; FR_NFR 3.4.2 "plant late-service and reordered-output defects" |
| `hooks.py:282`, `:314`, `:344`, `:364`, `:378`, `:397`, `:429` | new groups: counters (alone, under load), the loaded fan-out, ADP/ACMP ordering, H-DISC aging, the late groups | S2 has no counter push, no fan-out under load; the late groups wait long enough to see a late service end |
| `hooks.py:394` `SUPERSEDED` | S2's `acmp.tmr_no_adp` refusal superseded only where `hooks-disc-aging` measured the same path on the same interface | S2's window closes before the platform's 2 s aging expiry at 8x8 (see progress log) |
| `hooks.py:503`, `:511`, `:523` | split/parse/grade through S2's grader with this harness's lines taken off and the counter change as `pad:CTR` | S2's parser refuses unknown lines |
| `hooks.py:560`-`:833` | the eight ordering checks, each counting the instances it applied to; the held push | ordering apart from the budget (#664 ruling item 4) |
| `run.py:66` `hook_row`, `:80` `held_row`, `:98` `grade_all`, `:140` `summary`, `:167` `table`, `:214` `main` | per-path verdict, margin, alone/under load; findings by hook; plant mode | the runner |
| `hooks_selftest.py` | the portable self-test and its mutants (22 checks and 31 mutants at the head) | each rule must be able to fail |
| `README.md` | the harness's README | the test README |
| `sw/firmware/ctrl/test/ctrl_configs.py:218-223` | one `OUTSIDE` entry for `hooks_build.py` | the TSN stack boundary gate (rtl-fast) refuses an unclassified module naming the firmware tree; S2's and S3's harnesses have theirs |

Commits (one-line subjects, no body, no trailers):

- `86392bd2` the harness;
- `f5bf3677` the H-DISC window ends at the interface's next ADP record, tagged or not; mutant names;
- `b2d4ea80` the H-NOTIFY ordering plant keeps the solicited response aside;
- `4a0b3d16` the aging group answers each sink's PROBE_TX first;
- `e4d2a867` the aging group binds and answers one interface at a time (S2's `probe_answer` replies to the newest PROBE_TX on any interface).
- `3c514839` the composed windows open a full refill after the registrations (every bucket full at the 100 MHz CPU too).
- `fa925043` the product clock 100 MHz on `sys` (default), the Milan clock as history; H-DISC's undecided rule; NARROW (the layout swing); the spin doubled for the 100 MHz plants.

Changes of `fa925043` (resume round), file:line at that commit:

| File:line | What | Why |
|---|---|---|
| `hooks_build.py:48` `CPU_CLOCKS`, `:214` `build`, `:218` | the CPU clock is a name, `sys` (100 MHz, default) or `milan` (50 MHz); an unknown name is refused | owner 2026-10-30 (6514866239): the split CPU clock is 100 MHz on `sys`; S5 grades there; 50 MHz is history. A named parameter with the product default, as that ruling asks of S2b's build |
| `hooks_soc.py:32` (docstring), `:67` `CPU_CLOCK_KEYS`, `:189`, `:215`, `:244` | the export takes the CPU's frequency from the named clock; `soc.json` records `cpu_clock`, `milan_hz`, `product_cpu_hz` = `sys_clk_hz` | the build records the clock by name; the docstring says the CPU keeps this base's clock input and crossing (equal frequencies under `sys`), which the product wiring drops |
| `run.py:56` `clock_label` | `sys` labelled the product split CPU clock; `milan` labelled history, "not the product split CPU clock of 100 MHz" | every figure names its clock; no 50 MHz figure is presented as the product's |
| `run.py:215` `--cpu-clock`, `:252` | the option replaces `--cpu-hz`; plants build at `sys` | the plants run at the product clock |
| `hooks.py:45` `LAYOUT_SWING_CYCLES`, `run.py:99` `slack_cycles`, `:148` NARROW, `:310` | a path within its bound by fewer than 6,490 CPU cycles is a `NARROW` finding, recorded like `LATE` | ruling 6634982529 item 2: a fit by less than the layout swing fits by chance |
| `hooks.py:48` `TMR_DELAY_MAX_MS`, `:635` `disc_decided_ms`, `:641` `discovery_order`, `:561` `Checked.undecided` | a window with no PROBE_TX decides an H-DISC instance only when longer than 1040 ms; a shorter one is counted undecided | the false `ORDER H-DISC` at 8x8 answering 100 MHz (Resume above): the sink's TMR_DELAY draw (0 to 1000 ms, Milan v1.2 Table 5.29) ran past the next ADP record |
| `hooks.py:95` `SPIN` | 120,000 turns (was 60,000) | the late plants now run at 100 MHz; keeps each well past its bound |
| `run.py:110`, `:130`, `:170`, `:188` | undecided counts and the narrow count in the summary and the table; a slack column | the counts are public, never folded into "applied" |
| `hooks_selftest.py:37`, `:116`, `:175`, `:326`, mutants `:449`, `:451`, `:460`, `:500`, `:502` | product clocks in the synthetic logs; the clock labels and default; H-DISC's four cases; the layout swing; four new mutants and one renamed (27 to 31) | each new rule must be able to fail |
| `hooks.py:40`, `:64`, `hooks_build.py:43`, `run.py` | dated decisions in place of comment IDs in source comments | source comments carry issue and requirement IDs only |

Changes of `eef3d97a` (resume of 2026-11-06; the README only), file:line at that commit:

| File:line | What | Why |
|---|---|---|
| `README.md:16` | the clock: 100 MHz on `sys` is the product's, superseding the 50 MHz of the earlier correction; this base's `MilanSoC` drives the CPU from the Milan clock until S2b | owner 2026-10-30 (6514866239) |
| `README.md:82`, `:401` | the CPU keeps this base's crossing to the bus under `sys`; the product wiring has none, so the figures include its latency | the measured figure must say what it includes |
| `README.md:115` | the hooks table's reference to `ARCHITECTURE_HW_SW_SPLIT.md` section 1 made a link | `scripts/docs_check.py` refuses a bare doc reference; it was bare since `86392bd2`, so the docs gate failed at every earlier head of this lane |
| `README.md:132` | the composed rows open on full buckets with the grandmaster changes first: the burst ruling 6634982529 item 1 puts in the SRP row's scope | that ruling |
| `README.md:166` (Grading) | the layout swing: a fit by fewer than 6,490 CPU cycles is `NARROW` | ruling 6634982529 item 2 |
| `README.md:179`-`:186` | H-DISC's undecided instances and the 8x8 answering case (window 557.2 ms, probe at 672.3 ms); the `disc-order` plant's 1243 ms window | `fa925043`'s rule, with the measured case |
| `README.md:188`-`:192` | the superseded probe arose at the 50 MHz clock only; at 100 MHz `acmp-disc` measures it and nothing is superseded | measured: `superseded` is empty in all four runs |
| `README.md:235`-`:339` | Results: the four runs, the hook tables, the counts and ordering instances, the worst paths and margins, H-COUNTERS' paths, the 16 plants | the measurement at the head |
| `README.md:341`-`:357` | Findings by hook | S5's acceptance stated as measured |
| `README.md:359`-`:389` | History: the 50 MHz figures at `3c514839` | owner 2026-10-30: the 50 MHz figures become history |
| `README.md:402`, `:403` | limits: the retried notice's row is S2b's; the 50 MHz figures not re-measured | ruling 6630265194 |

## New checks (planted mutant, failing words)

### The 16 plants (real firmware defects, scratch copies; each must be caught by its own words)

All 16 at `fa925043`, 1x1, CPU 100 MHz on `sys`, each in a clean clone, rc 0 (receipts `plants/plant-<name>.log`). The head adds only `README.md` after `fa925043`, so the plants' inputs are those of the head.

| Plant | Defect planted | Group | Caught by (first finding, verbatim) |
|---|---|---|---|
| `adp-late` | `adp_mbx.c` receive handler spins 120,000 turns before `adp_rx` | `control` | `LATE H-ADP: control.discover.if0: 74.532 ms against its bound 20 ms` |
| `adp-order` | `adp_mbx.c` `port_gptp` returns the previous read's grandmaster | `hooks-order-adp` | `ORDER H-ADP: the ENTITY_AVAILABLE committed at bus cycle 184748560 on interface 0 carries grandmaster 0000000000000000, not the one in force` |
| `disc-late` | `acmp_mbx.c` `on_adp_frame` spins before `acmp_adp_rx` | `hooks-late-disc` | `LATE H-DISC: hooks-late-disc.entity_departing.if0: 129.678 ms against its bound 20 ms` |
| `disc-order` | `acmp_mbx.c` `on_adp_frame` holds an ENTITY_DEPARTING and applies it after the next AVAILABLE | `acmp-disc` | `ORDER H-DISC: after the ENTITY_DEPARTING at 73700102 and the ENTITY_AVAILABLE at 90700102 on interface 0, the sink never probed its talker: the departure was applied after the arrival` |
| `acmp-late` | `acmp_mbx.c` `on_frame` spins before `acmp_rx` | `hooks-late-acmp` | `LATE H-ACMP: hooks-late-acmp.get_rx_state.if0: 74.760 ms against its bound 20 ms` |
| `acmp-order` | `acmp_mbx.c` `on_frame` holds a command and takes it after the next | `hooks-order-acmp` | `ORDER H-ACMP: on interface 0 the command 0x7401 received at 69623957 after 0x7400 at 69623866 was answered first` |
| `aecp-late` | `aecp_mbx.c` `frame` spins before `aecp_rx` | `hooks-late-aecp` | `LATE H-AECP: hooks-late-aecp.read_descriptor.if0: 76.069 ms against its bound 20 ms` |
| `aecp-order` | `aecp_face.c` `changed` defers the publication; `aecp.c` no longer waits | `aecp` | `ORDER H-AECP: aecp.lock_entity.if0: its response at 79355294 precedes any face commit since its receive commit at 79223329` |
| `notify-late` | `aecp.c` `transmit` spins before a fan-out's first recipient | `hooks-late-notify` | `LATE H-NOTIFY: hooks-late-notify.set_name.if0: 79.352 ms against its bound 20 ms` |
| `notify-order` | `aecp.c` `transmit` sends the notifications before the owed response | `aecp-fanout` | `ORDER H-NOTIFY: aecp_fanout.set_name.if0: a notification at 75477884 precedes its response at 75694414` |
| `counters-late` | `ctrl_app_aecp.c` `face_event` spins on COUNTERS_CHANGED | `hooks-counters` | `LATE H-COUNTERS: counters.first.if0: 81.819 ms against its bound 20 ms` |
| `counters-order` | `aecp.c` `asynchronous` drops the 1 s spacing after a push's departure | `hooks-counters` | `ORDER H-COUNTERS: descriptor 0x0005 0 to 0a0b0c0d0e0f1000 on interface 0: pushes 115.251 ms apart at the wire, under 1000 ms` |
| `maap-late` | `maap_mbx.c` `receive` spins before `maap_rx` | `hooks-late-maap` | `LATE H-MAAP: hooks-late-maap.defend.if0: 74.690 ms against its bound 20 ms` |
| `maap-order` | `maap_mbx.c` `range` reports the allocation before publishing the DA gate | `maap` | `ORDER H-MAAP: the allocation report at 9496149 follows no DA_GATE publication since 4934743` |
| `srp-late` | `srp_mbx.c` `receive` spins before `apply_receive` | `hooks-late-srp` | `LATE H-SRP: hooks-late-srp.listener_ready.if0: 75.638 ms against its bound 18 ms` |
| `srp-order` | `srp_mbx.c` publishes the adopted Domain after the next MRPDU | `srp` | `ORDER H-SRP: the MRPDU committed at 276780935 on interface 0 after the Domain record at 276575280 precedes its SR_DOMAIN publication (276781521)` |

### The self-test (`run.py --self-test`): 22 checks, 31 mutants

Each mutant replaces one rule and must make the named check fail; the run prints `MUTANT <name>: caught by <check>` and ends `ctrl_service_hooks self-test: 22 of 22 checks pass; 31 of 31 mutants caught`, rc 0. The mutant table is the README's (Grading), one row per mutant; the four added in `fa925043`, and the one it renamed, are:

| Mutant | Failing check |
|---|---|
| label: the Milan clock the default (the earlier rule) | the clock labels |
| H-DISC: a window shorter than the sink's TMR_DELAY decides (the earlier rule) | H-DISC ordering |
| narrow: the layout swing is not applied | a fit under the layout swing is a finding |
| narrow: the slack counted at the 50 MHz CPU (the earlier clock) | a fit under the layout swing is a finding |
| label: the Milan clock labelled the product's (the earlier rule), renamed from "the variant labelled the product's" | the clock labels |

## Gate table

Head `eef3d97a`. `fa925043..eef3d97a` changes only `tb/verilator/ctrl_service_hooks/README.md`, which no gate below builds from; the gates marked `fa925043` therefore ran on the head's code, firmware and harness. Every gate ran in a clean clone, foreground of its own unit, never piped; every log ends with its rc and the tree's state after.

| Gate | Command (from the clone's root) | At | Result | Receipt |
|---|---|---|---|---|
| Hook harness self-test and its mutants | `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test` | `eef3d97a` | rc 0; 22 of 22 checks, 31 of 31 mutants | `gates/docs/hooks_selftest.log` |
| The 16 plants (late and ordering per hook) | `python3 -B tb/verilator/ctrl_service_hooks/run.py --plant <name> --build-dir <build>/plant-<name>` | `fa925043` | 16 of 16 `PLANT <name> caught`, each rc 0 | `plants/plant-*.log`, `plants/chain-*.log` |
| Hooks 1x1 idle, product clock | `python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --build-dir <build> --record-findings --jobs 8` | `fa925043`, regraded `eef3d97a` | rc 0 / rc 0; 145 paths, 0 refusals, 0 ORDER, 0 NARROW | `runs/1x1-idle/` |
| Hooks 1x1 answering | the same with `--arm answering` | `fa925043`, regraded `eef3d97a` | rc 0 / rc 0; 159 paths | `runs/1x1-ans/` |
| Hooks 8x8 idle | `--point 8x8 ... --jobs 16` | `fa925043`, regraded `eef3d97a` | rc 0 / rc 0; 207 paths | `runs/8x8-idle/` |
| Hooks 8x8 answering | `--point 8x8 --arm answering ... --jobs 16` | `fa925043`, regraded `eef3d97a` | rc 0 / rc 0; 221 paths | `runs/8x8-ans/` |
| Firmware self-test, 4 shards | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard <k>/4 --jobs 8` | `fa925043` | rc 0 each (515, 2577, 863, 1087 s) | `gates/selftest-shard<k>.log` |
| S2's harness, 1x1 | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <build> --record-budget-findings --jobs 6` | `fa925043` | rc 0; 18 groups, 0 refusals | `gates/s2_harness-1x1.log` |
| S2's harness, 8x8 | the same with `--point 8x8` | `fa925043` | rc 0; 17 groups, 0 refusals | `gates/s2_harness-8x8.log` |
| S2's harness self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | `eef3d97a` | rc 0 | `gates/docs/harness_selftest.log` |
| End-station builder | `python3 sw/builder/test_builder.py --require-rv32` | `fa925043` | rc 0 (2197 s) | `gates/builder_require_rv32.log` |
| TSN stack boundary (touched: `ctrl_configs.py`) | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | `fa925043` | rc 0, `ctrl_boundary: PASS` | `gates/ctrl_boundary.log` |
| TSN stack boundary, Verilator half | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator` | `fa925043` | rc 0, `ctrl_boundary: PASS` (1020 s) | `gates/ctrl_boundary-verilator.log` |
| Docs, scope, idiom, CI and behave gates (98, gates_s5.py), incl. `cd tests && behave` | see `gates/docs/*.log` first lines | `eef3d97a` | 0 of 98 nonzero, tree clean after each; behave 1977 steps passed | `gates/docs/summary.md` |
| Merge result smoke: head merged onto `dev-soft-core` `a68536fa` (scratch `88a7e705`) | hook self-test; `--point 1x1` idle full run | `88a7e705` | self-test rc 0 (22/22, 31/31); 1x1 idle rc 0, 145 paths, 0 refusals, 28 `LATE`, the same findings by path and verdict as the base run and every hook's worst equal to two decimals (84 paths shift, at most 0.95 ms, on timer phases) | `merge/` |

Not run: the full sweep and Vivado (no RTL change).

## Measurements

The four runs at the product clock (CPU 100 MHz on `sys`, bus 100 MHz), measured at `fa925043` in clean clones (`c-s<point>-<arm>`), each regraded at the head `eef3d97a` on its reused build (every input digest checked; each regraded `table.md` byte-identical to the run's). Receipts `runs/<point>-<arm>/` (run.log, regrade.log, table.md, results.json, build.json).

| Point | Arm | Groups | Paths | Refusals | Superseded | ORDER | NARROW | LATE | Run rc | Regrade rc at head |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 | idle | 27 | 145 | 0 | 0 | 0 | 0 | 28 | 0 | 0 |
| 1x1 | answering | 29 | 159 | 0 | 0 | 0 | 0 | 29 | 0 | 0 |
| 8x8 | idle | 27 | 207 | 0 | 0 | 0 | 0 | 38 | 0 | 0 |
| 8x8 | answering | 29 | 221 | 0 | 0 | 0 | 0 | 42 | 0 | 0 |

Each hook's worst, ms (bound), alone idle / alone answering / loaded idle / loaded answering; bold over:

| Hook | 1x1 | 8x8 |
|---|---|---|
| H-ADP (20) | 0.63 / 0.63 / **29.40** / **21.26** | 3.37 / 3.37 / **44.15** / **31.50** |
| H-DISC (20) | 8.40 / 0.81 / **24.78** / 14.03 | 15.93 / 1.34 / **37.32** / **21.79** |
| H-ACMP (20) | 8.16 / 0.87 / **never** / **never** | 15.99 / 1.64 / **never** / **never** |
| H-AECP (20) | 1.89 / 1.88 / **159.48** / **85.82** | 2.40 / 2.40 / **205.20** / **102.26** |
| H-NOTIFY (20) | 3.78 / 3.78 / **59.38** / **59.38** | 6.85 / 6.85 / **84.07** / **84.07** |
| H-COUNTERS (20) | - / **27.58** / - / **20.76** | - / **218.71** / - / **36.62** |
| H-MAAP (20) | 1.01 / 1.01 / **29.43** / **21.25** | 1.76 / 1.76 / **44.19** / **31.48** |
| H-SRP (18) | 1.81 / 1.81 / **never** / **68.05** | 4.04 / 4.04 / **never** / **102.31** |

- Alone: every hook within its bound at both points and arms but H-COUNTERS' ALL push (80 notices at 1x1, 608 at 8x8; about 32,000 to 36,000 CPU cycles a notice, the CTR window answered at the contract's slowest).
- Under the composed load: every hook over at both points and arms but H-DISC at 1x1 answering (14.03). Never served: the four ACMP commands behind the owed one (ACMP_OWED_MAX, S2's finding), both points and arms, at least 363 ms; SRP in `backlog-adp` and `backlog-adp-refill` on the idle arm, both points, at least 524.8 to 567.5 ms (S2's `rx_order_ready` starvation).
- Ordering: no finding in any run; every check applied wherever it can (H-COUNTERS not on the idle arm, by construction); H-DISC one undecided instance at 8x8 answering (interface 1: window to the next ADP record 557.2 ms, PROBE_TX at 672.3 ms, decided only above 1040 ms).
- NARROW: none. Superseded: none at 100 MHz (`acmp.tmr_no_adp.if1` is measured by `acmp-disc` itself; the 50 MHz case is history).
- History (50 MHz, `3c514839`, regrades rc 0): README History tables; receipts `history/<point>-<arm>-50/`. The two 8x8 run logs there (at `86392bd2`) end rc 1 on `hooks-disc-aging`'s refusals (and, idle, `acmp.tmr_no_adp.if1`'s); `4a0b3d16` and `e4d2a867` fixed that group, and each regrade log reruns it at `3c514839` before grading: rerun rc 0, regrade rc 0, 0 refusals.

## Shared files touched

- `sw/firmware/ctrl/test/ctrl_configs.py` (one `OUTSIDE` entry): the TSN stack boundary gate (rtl-fast) refuses any Python module that names the firmware's tree unless classified; `hooks_build.py` names it (the image builder and the plants' scratch copy). Same pattern as S2's and S3's entries. Outside `tb/`; disclosed.

## Open questions / STOP conditions

- No STOP condition was met: no firmware instrumentation was needed (H-COUNTERS is reached through the labelled answering arm, in test code). No firmware, RTL or shared harness file was edited.
- **Acceptance, stated as measured:** alone, every hook within its bound at both points and arms but H-COUNTERS' ALL push (27.58 ms at 1x1, 218.71 ms at 8x8). Under the composed load every hook misses but H-DISC at 1x1 answering. This is `dev-soft-core` without S2b's cuts (assignment item 3). Open for the maintainer: whether S5 re-measures on S2b's head once #810 merges (the harness reruns as is: four commands), and whether H-COUNTERS' ALL push, a volume of 80 to 608 notices from one event, is graded as one path (as FR_NFR 3.4.2's row reads: event to the last push) or per descriptor.
- **The merge target moves S2's split SoC** (`split_soc.py`: #799's `pub_src_sid_o`, #814's staged flash PHY). This harness builds its mailbox and flash through `split_soc.add_devices`, so the merge result takes both; the merge smoke above builds and runs. The figures here are at the base, without the staged flash PHY.
- The 100 MHz CPU runs behind this base's crossing; the product's no-crossing wiring arrives with S2b.
