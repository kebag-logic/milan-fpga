# [A222] #529 / PR #534, correction round 2: handoff

- Lane: `529-crf-input-counters`, `$LANES/529-crf-input-counters`.
- Round input head: `535701a06128d54c7f0f161e1c061fa02d4d1342`.
- New head: `31e62ffead16e43d648993278b0ab9190d99b672`, tree `4d32ede1eba65adcee359d00751ddadf3314a36b`.
- Base: `ede8d48ecd7c7f589a14b957951f040d92c99c70`. Nine one-line commits, linear on it.
- Gitlinks unchanged: protocol-processor `424c688f`, gptp-processor `c1b61743`,
  third_party/verilog-axis `48ff7a7e`.
- Not pushed. Pushing and editing the PR are the coordinator's.

The three new commits are one-line, with no trailers:

| SHA | Subject |
|---|---|
| `b65030e0` | Require the CRF bind edge to reach the arbiter as no tuple but STREAM_INPUT N and compare A's CRF push copy too in sim_nxn |
| `78cdff20` | State the CRF bind edge's arbiter exclusivity and both push copies as the strengthened sim_nxn checks prove them |
| `31e62ffe` | Point the CRF output config comments at the open audit B3 only now that B4 is closed |

**No RTL change.** `git diff 535701a0 HEAD -- hdl` is empty. The datapath sha256 is
`2b729369…`, the same as at the reviewed head. So there is no VERSION, descriptor, pin
or synthesis consequence, and CHANGELOG.md is unchanged. The changed files are
`sim_nxn.cpp`, `REGISTER_MAP.md`, the milan_dp `README.md`, and one comment line in
each of three `configs/*.yaml`.

## The finding

R268-2 F1 = R269-2 F1, MINOR, Tests and Docs, as filed by the reviewers.

The criterion-3 evidence said the bind edge reaches the Table 5.22 arbiter as
{STREAM_INPUT, `N_STREAMS`} "and as nothing else". The check cleared and compared only
the STREAM_INPUT bitmap. Two mutants that also raise a second descriptor passed every
check. R269 also found that "byte-identical ... to the solicited answer" was claimed for
both controllers, but only B's copy was compared. R268 filed that part as S2.

**The disposition: the check was strengthened and the claims kept.** Each claim now
names what its check covers.

### What changed in `sim_nxn.cpp`

1. **The arbiter observer is now total** (`:567-571`, `:590-591`). `step()` keeps four
   delivery records: STREAM_INPUT and STREAM_OUTPUT bitmaps (indices below 64),
   AVB_INTERFACE 0 and CLOCK_DOMAIN 0. A delivery none of them can hold used to be
   dropped silently: another descriptor type, a non-zero AVB_INTERFACE or CLOCK_DOMAIN
   index, or an index of 64 or more. It now counts in `pp_ctr_evt_other_n`. Between
   them, the five account for every {type, index} the arbiter can hand over.
2. **The bind-edge arm clears all five and grades all five** (`:3473-3494`). The
   existing check still requires the STREAM_INPUT bitmap to equal `1 << N` exactly.
   Three new checks require no STREAM_OUTPUT row, neither AVB_INTERFACE 0 nor
   CLOCK_DOMAIN 0, and no tuple of another type or index. The window is `crf_lever(true)`:
   three CSR writes and 64 cycles, all driven through `step()`.
3. **`[NOTIFY-CRF]` compares A's copy too** (`:1333-1334`). A's last unsolicited
   GET_COUNTERS(STREAM_INPUT, N) must be byte-identical, from the body on, to the same
   solicited answer B's copy is compared with. It is fetched after that exchange, so
   the pointer is fresh.
4. **One-liner, R268 S4 / R269 S2:** the timed-leg header (`:1069`) said "RELEASED
   after >= 1000 ms". It now says "about 1000 ms later". The check keeps its 990 ms floor,
   which its own comment (`:1350-1352`) explains.

`[CTRS-CRF]` goes from 72 to 75 checks on each broad leg. `[NOTIFY-CRF]` goes from 10
to 11.

### What changed in the docs

- **`REGISTER_MAP.md:897-907`, criterion 3.** The claim "and as nothing else" is kept.
  The text now says the harness records every tuple the arbiter hands over in that
  window, of any type and index, and names what may not appear: another STREAM_INPUT
  row, a STREAM_OUTPUT row (the CRF Media Clock Output's at the same index included),
  AVB_INTERFACE 0, CLOCK_DOMAIN 0, or any other type or index. The push reaches both
  controllers, and "each copy" is byte-identical.
- **`REGISTER_MAP.md:911-916`, criterion 4, and `README.md:531-537`.** The list of
  wiring mutations that turn at least one check red gains the ones below: the CRF
  pulse also raising the AAF inputs, STREAM_OUTPUT `N_STREAMS`, AVB_INTERFACE 0,
  CLOCK_DOMAIN 0, or a tuple at an undeclared index.
- **`README.md:513-518, 528-529`.** The same two statements as criterion 3. The paragraph
  from `:513` to its end is re-flowed at 79 columns. `git diff --word-diff` shows only the
  added words.
- **One-liner, R268 S7 / R269 S3:** `configs/endstation_arty_4x4.yaml:103`,
  `endstation_arty_8ch.yaml:139` and `endstation_ax7101_8x8.yaml:153` now point at "the
  current audit B3" only. B4 is recorded as closed by #529, and B3 is still open. These
  are comment lines. No file under `configs/generated/` carries them, which was checked
  with `grep -rl "current audit B3"`.

## Mutation evidence

Pinned simulator 5.050. Each build ran alone with the recipe's `-j 8`. Every receipt
names the datapath and harness sha256, the build and run exit codes, and the tally. They
are in `logs/mutants/`, with the diffs in `mutants/`.

| Mutant (edit to `milan_datapath.sv`) | Source | New harness `46cc9b15…` (= HEAD), nxn | New harness, nxn8 | Previous harness `fe0e4c37…` (= 535701a0), nxn |
|---|---|---|---|---|
| `dirty_also_sout_n`: the CRF pulse also raises STREAM_OUTPUT `N_STREAMS` | R268 `dirty_also_sout_n` = R269 `ve-also-sout` (byte-identical diffs) | **KILLED**: "...and as no STREAM_OUTPUT row" got `0x10` | **KILLED**: same check, got `0x100` | SURVIVED 1705/0 |
| `dirty_also_ckd`: also raises CLOCK_DOMAIN 0 | R268 `dirty_also_ckd` = R269 `ve-also-ckd` | **KILLED**: "...nor AVB_INTERFACE 0 or CLOCK_DOMAIN 0" got 1 | **KILLED**, same | SURVIVED 1705/0 |
| `dirty_also_avb`: also raises AVB_INTERFACE 0 | this round | **KILLED**: "...nor AVB_INTERFACE 0 or CLOCK_DOMAIN 0" got 1 | **KILLED**, same | SURVIVED 1705/0 |
| `dirty_also_other`: also raises the AVB pending bit, which the pick hands out as {AVB_INTERFACE, 1}, an undeclared index none of the four records holds | this round (two edits, so that only the catch-all can see it) | **KILLED**: "...nor any tuple of another type or index" got 1 | **KILLED**, same | SURVIVED 1705/0 |
| `dirty_also_aaf`: also raises every AAF input | R268 `dirty_also_aaf` (already red at 535701a0) | **KILLED**: "...as STREAM_INPUT N only" got `0x1f` | **KILLED**: got `0x1ff` | not rerun |

In each of the 10 new-harness runs, the named check is the only `[FAIL]`. The unmutated
head is the green control: nxn 1708/0 and nxn8 3136/0.

The dirty source removed (`mutants/dirty_removed.diff`, `pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w}`) was rerun at this head, because
the PR body's table counts its red checks. On nxn it is KILLED at "...as STREAM_INPUT N
only" (got 0). On obj_notify all 11 `[NOTIFY-CRF]` checks are red, the new A-copy
check among them.

**A-copy probe (a harness fault, not an RTL mutant).** `mutants/probe_acopy.harness.diff`
flips one body bit of A's logged copy just before the new comparison. On obj_notify the
result is 146 checks and 1 failure, `[NOTIFY-CRF] ...and so is A's copy`. B's comparison,
the counts, the withheld and released pushes and the quiet checks all stay green
(`logs/probes/probe_acopy_notify.txt`). So the check reads A's own frame. No RTL edit
reaches A's copy alone: the processor sends the one response to each registered
controller.

## Validation at the new head

The pinned simulator 5.050 (`logs/tool_identity.txt`) was first on PATH, with 8 jobs. Each
leg was clean-built with the object directory removed first, using its own line of
`make -n run VERILATOR_JOBS=8` (`make-n-run.txt`, run by `scripts/leg.py`). Every run used
harness sha256 `46cc9b158dfe26c7acedb5084a03932ebba17d5fed43ee70f04df755701a14b1`, which
is `git show HEAD:tb/verilator/milan_dp/sim_nxn.cpp`.

| Leg | Result | At 535701a0 |
|---|---|---|
| obj_nxn (4x4) | 1708/0, with 75 `[CTRS-CRF]` | 1705, with 72 |
| obj_nxndv (divergent 4x4) | 1710/0, with 75 | 1707 |
| obj_nxn8 (8x8) | 3136/0, with 75 | 3133 |
| obj_nxn4c (shipping Arty 4x4) | 1708/0, with 75 | 1705 |
| obj_notify (timed) | 146/0, with 11 `[NOTIFY-CRF]` | 145, with 10 |
| obj_dir (main, `sim_main.cpp`) | 230/0 | 230 |

Logs: `logs/run_<leg>.txt`.

Gates at `31e62ffe` (`logs/gates_static.txt`):

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | 0 findings, exit 0 |
| `scripts/check_em_dash.py --base ede8d48e` | 0 findings over 164 added lines in 9 pages, exit 0 |
| `scripts/check_cpp_idiom.py` | exit 0; every ratchet 0 <= 0 |
| `git diff --check ede8d48e..HEAD` and `535701a0..HEAD` | clean |
| worktree | clean |

A merge-tree against the live dev tip `26d855a9` is clean (exit 0, tree `bc40b183`). It
was not built.

## Other reviewer notes

Taken, because each is a one-liner:

- R268 S4 / R269 S2 (the header said ">= 1000 ms"): the comment is reworded (above).
- R268 S7 / R269 S3 (config comments pointed at B4): three comment lines (above).
- R268 S2 (A's copy counted, not compared): folded into F1, as R269 filed it.
- R269 S6 (the PR body says `Relates to #529` "closes the issue at merge"):
  `PR-BODY.md` rewords that sentence. The PR body itself is the coordinator's to edit.

Not taken, because none is a one-liner:

- R268 S1 / R269 S5: the silence constants passed from the recipe as `-D`.
- R268 S3: `public_flat_rw` on the ten tally wires. This is an RTL edit.
- R268 S5 / R269 S4: the arbiter's no-starvation property.
- R268 S6 / R269 S1: a `crf_sink: false` leg.

## Not run, and limits

- **The rest of milan_dp's `run` recipe** was not run: nolpf, prune, ax1x1, aclk, gptp,
  gptplat and the render mutants. None of them compiles `sim_nxn.cpp`, and `hdl/` is
  unchanged.
- **Other suites and gates** were not run: pp_shadow, milan_dp_render, crf_rx, behave,
  xvlog, Yosys, the builder bank, act/Docker and hardware. The config change is to
  comments only.
- **Mutants** ran on nxn and nxn8, the two shapes the reviewers used. They were not run
  on nxndv or nxn4c. Those legs run the same arm and are green at the head.

## Found, out of scope (for the coordinator)

`[NOTIFY-CRF]` (`sim_nxn.cpp:1322-1332`) holds `n1`, a pointer into `uns_log`, across
`aecp_xact_from()`. That exchange's `await_aecp()` can `push_back` into `uns_log`, which
would leave `n1` dangling if an unsolicited frame arrived while it waits and the vector
reallocated. The base-era `[NOTIFY]` content bar (`:1190-1195`, `nB2`) has the same
pattern. It passes deterministically at this head. This round's new A-copy check fetches
its pointer after the exchange, so it does not have the hazard. This round does not fix
it: the pattern predates the lane and no finding names it. It needs a new Issue.

## Packet

- `HANDOFF.md`, `PR-BODY.md`.
- `make-n-run.txt`: the suite recipe the legs were built from.
- `scripts/leg.py` and `scripts/run_mutants.sh`.
- `mutants/*.diff`: five datapath mutants and the A-copy harness probe.
- `logs/`: runs, mutant receipts (`logs/mutants/SUMMARY.tsv`), the probe, static gates,
  tool identity.
- `MANIFEST.sha256`.

Reproduce, from the lane at the head, with the pinned simulator first on PATH:

```sh
P=$MANAGEMENT/2026-09-23/529-a222
cp hdl/milan/milan_datapath.sv /tmp/m.sv && patch /tmp/m.sv < $P/mutants/dirty_also_ckd.diff
python3 $P/scripts/leg.py tb/verilator/milan_dp $P/make-n-run.txt nxn /tmp/ckd.txt --dp /tmp/m.sv --mdir /tmp/obj_ckd
```

A harness copy passed with `--harness` must sit two directories below a `tb/` that holds
`common/`, because of the harness's relative include.
