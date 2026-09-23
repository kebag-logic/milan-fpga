[A222] REVIEW READY
Commit: `31e62ffead16e43d648993278b0ab9190d99b672` (tree `4d32ede1eba65adcee359d00751ddadf3314a36b`)

This is correction round 2 of PR #534, for R268-2 F1 and R269-2 F1, the same MINOR (Tests,
Docs). Three one-line commits sit on the reviewed head `535701a0`, with no trailers:
`b65030e0` (harness), `78cdff20` (docs) and `31e62ffe` (config comments). Nothing is pushed
from this lane.

**No RTL change.** `git diff 535701a0 HEAD -- hdl` is empty, and the datapath sha256 is
unchanged (`2b729369…`). CHANGELOG.md is unchanged.

**Changed.** The check was strengthened and the claim "and as nothing else" kept.

- `sim_nxn.cpp:567-571,590-591`: the arbiter observer in `step()` now counts every
  delivery its four records cannot hold: another type, a non-zero AVB_INTERFACE or
  CLOCK_DOMAIN index, or an index of 64 or more. Between them, the five records account
  for every {type, index} the arbiter can hand over.
- `sim_nxn.cpp:3473-3494`: the bind-edge arm clears all five, then requires STREAM_INPUT
  exactly `1 << N`, no STREAM_OUTPUT row, neither AVB_INTERFACE 0 nor CLOCK_DOMAIN 0, and
  no tuple of another type or index. That is three new checks.
- `sim_nxn.cpp:1333-1334`: `[NOTIFY-CRF]` now compares A's copy too, against the same
  solicited answer as B's. R269 filed this in F1, R268 as S2.
- `REGISTER_MAP.md:897-907,911-916` and `README.md:513-518,528-529,531-537`: criterion 3
  names what the window may not contain and says "each copy". The mutation lists gain the
  extra-tuple mutants below.
- One-liners from the suggestions:
  - the timed-leg header reads "RELEASED about 1000 ms later" (`sim_nxn.cpp:1069`; R268
    S4 / R269 S2);
  - three config comments point at the open audit B3 only (R268 S7 / R269 S3).

**Failing arms shown.** Pinned simulator 5.050. Each receipt names the datapath and harness
sha256. The new harness is `46cc9b15…` = HEAD; the previous one is `fe0e4c37…` = 535701a0.

| Mutant | Previous harness, nxn | New harness, nxn and nxn8 |
|---|---|---|
| the CRF pulse also raises STREAM_OUTPUT `N_STREAMS` (R268 `dirty_also_sout_n` = R269 `ve-also-sout`, byte-identical) | green 1705/0 | red: "...and as no STREAM_OUTPUT row" |
| ...also raises CLOCK_DOMAIN 0 (R268 `dirty_also_ckd` = R269 `ve-also-ckd`) | green | red: "...nor AVB_INTERFACE 0 or CLOCK_DOMAIN 0" |
| ...also raises AVB_INTERFACE 0 (new) | green | red: the same check |
| ...also raises AVB, handed out as {AVB_INTERFACE, 1}, which no named record holds (new) | green | red: "...nor any tuple of another type or index" |
| ...also raises every AAF input (R268 `dirty_also_aaf`) | red | red: "...as STREAM_INPUT N only" |

In every new-harness mutant run, the named check is the only `[FAIL]`. The dirty source
removed was rerun: it is red on nxn, and all 11 `[NOTIFY-CRF]` checks are red on notify.
A harness probe that flips one body bit of A's logged copy fails only the new A-copy
check on obj_notify (146 checks, 1 failure).

**Validation** at `31e62ffe`. Pinned simulator 5.050 with 8 jobs. Each leg was clean-built
from its own `make -n run` recipe line, at harness sha256 `46cc9b15…`:

| Leg | Result | At 535701a0 |
|---|---|---|
| nxn | 1708/0, with 75 `[CTRS-CRF]` | 1705, with 72 |
| nxndv | 1710/0 | 1707 |
| nxn8 | 3136/0 | 3133 |
| nxn4c | 1708/0 | 1705 |
| notify | 146/0, with 11 `[NOTIFY-CRF]` | 145, with 10 |
| main | 230/0 | 230 |

- `docs_check` exits 0 with 0 findings.
- `check_em_dash --base ede8d48e` finds 0 over 164 added lines.
- `check_cpp_idiom` exits 0, with every ratchet at 0 <= 0.
- `git diff --check` over `ede8d48e..HEAD` is clean, and the worktree is clean.
- A merge-tree against dev `26d855a9` is clean (tree `bc40b183`). It was not built.

**Acceptance criteria.** REGISTER_MAP closure criteria 1-4 are met. Criterion 3's evidence
now covers exclusivity across every tuple the arbiter can deliver, and both push copies.
The silicon Milan-compatible verdict follows the merge (#117). #529 stays open until then.

**Open risks and questions:**

- **Found, out of scope, for a new Issue.** `[NOTIFY-CRF]` (`sim_nxn.cpp:1322-1332`) and the
  base-era `[NOTIFY]` content bar (`:1190-1195`) each hold a pointer into the unsolicited
  log across `aecp_xact_from()`. That call's `await_aecp()` can append to the log, so the
  pointer could dangle if a frame arrived during it. It passes deterministically at this
  head. The new A-copy check fetches its pointer after the exchange.
- **Not taken, because none is a one-liner:** the silence constants from the recipe
  (R268 S1 / R269 S5), `public_flat_rw` on the tally wires (R268 S3, an RTL edit), arbiter
  no-starvation (R268 S5 / R269 S4), and a `crf_sink: false` leg (R268 S6 / R269 S1).
- **R269 S6** (the PR body sentence about closing at merge) is reworded in the packet's
  `PR-BODY.md`. The PR body is the coordinator's to edit.
- **Not run this round:** the milan_dp legs that do not compile `sim_nxn.cpp`, the other
  suites, xvlog, Yosys, the builder bank, act and hardware. `hdl/` is unchanged, and the
  config change is to comments only. Mutants ran on nxn and nxn8, not on nxndv or nxn4c.

The packet for the coordinator to archive holds:

- `HANDOFF.md`, `PR-BODY.md` and this text;
- the mutant diffs and the probe diff;
- every receipt and the leg runner;
- `MANIFEST.sha256`.

Lens labels and coverage are the reviewers' to judge. The `configs/` change is three
comment lines, and no generated file changes with it (`configs/generated/` carries no
copy of those lines).
