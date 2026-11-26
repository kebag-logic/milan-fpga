# #970 round 7: #1015 model-count check covers all seven ADP paths (R935-3-F1) — handoff

**Status (11-26): REVIEW READY at `57f32b28de9602bd239d7686cf4360912638d1f0`** (branch `970-discovery`, worktree
`$VALIDATION_STORAGE/adp970-a847`). Committed on `701a980b`, not pushed. Nothing was posted or flashed, and the bench
was not touched.

**ETA:** nothing pending on this side.

## 1. What changed (one commit, `57f32b28`, 2 files)

**I took option (a) and extended the check, because both missing paths have a stated count.**

- `adp.shutdown` is held to `ADP_MBX_LAT_SHUTDOWN` (29).
- `adp.link_down` has no macro of its own, and the C test C5 caps it at `ADP_MBX_LAT_LINK` (≤ 12). The header states
  its exact count in that macro's comment, "(down, a stop: 9)". The check reads the 9 from that comment. If the
  comment stops stating it, the check raises KeyError and fails.
- No firmware file changed.

`tb/verilator/ctrl_service_budget/model_counts.py`:

- `PATHS` lists all seven ADP paths that publish a count: link_up, link_down, gm_change, discover, tmr_delay,
  tmr_advertise and shutdown.
- `groups_at()` now reads every build-free group set (`SETS`): acmp, adp, backlog, bound_talker, control, fixture,
  maap, shutdown, srp, kept_window, datapath_window and held. The build-dependent sets publish no count; in this
  harness only `scenario.py` writes `accesses=`.
- A probe in the ADP family that publishes a count on a path outside the seven is now a finding too. "Every" stays
  true if a new path appears.
- **Plants:** each of the seven paths is planted one short in turn. Each plant must be found at every instance of its
  path (findings == instances, with instances > 0).
  - This takes R935-3's S1: the old threshold, `>= interfaces`, is gone.
  - The docstring states the rule exactly, which also settles RES-A's "(one finding a point)".

`tb/verilator/ctrl_service_budget/README.md:1326` now names the seven paths and their sources, the any-other-path
finding and the plant rule. The 12 against the platform's 11 is kept.

## 2. Validation at `57f32b28`

**`model_counts.py`:** rc 0.

| Planted one short | 1 interface (found/instances) | 2 interfaces (found/instances) |
|---|---|---|
| link_up 11 | 6/6 | 11/11 |
| link_down 8 | 2/2 | 3/3 |
| gm_change 10 | 1/1 | 2/2 |
| discover 30 | 2/2 | 3/3 |
| tmr_delay 38 | 5/5 | 10/10 |
| tmr_advertise 10 | 1/1 | 2/2 |
| shutdown 28 | 2/2 | 3/3 |

The real scenario gives 0 stale counts at both points.

**Scratch probes** (`receipts/r7/probe_r7.log`, rc 0) cover R935-3's verification list:

| Probe | `701a980b`'s check | Head's check |
|---|---|---|
| LINK_DOWN 8 | MISSED | DETECTED |
| SHUTDOWN 28 | MISSED | DETECTED |
| LINK_UP 11 | DETECTED | DETECTED |
| header SHUTDOWN 30, LINK 11, DELAY 40, "a stop: 10" | — | DETECTED |
| header without LINK_DOWN's count | — | raises KeyError (fails closed) |
| ADP probe with a count on an unheld path | — | DETECTED |
| real scenario | — | 0 findings |

**Other checks:**
- Budget self-test (`run.py --self-test`, which runs the check first): `self-test: 0 failures`, rc 0.
- Python idiom gate: rc 0.
- Docs gates: 37 of 37 pass.
- I did not rerun the CPU legs. The commit changes only the check and a README line, and `accesses` feeds no verdict.

Logs: `receipts/r7/` (index in `receipts/INDEX.md`).

## 3. Not done

- **RES-B (PR body text), local only.** I updated `PR-BODY.md` locally so it names the seven paths: status item 6 and
  the validation row. I did not add R935-3's exact sentence to the "Harness waits" bullet. Nothing was posted.
- **For the manager:** R935-3's S2 (the Results table's `(11)` note for `e76a755a`) and S3 (PR body opening and roles).
- **Retained residues:** R935-2 RES2 and RES4.

Branch head: `57f32b28de9602bd239d7686cf4360912638d1f0`.
