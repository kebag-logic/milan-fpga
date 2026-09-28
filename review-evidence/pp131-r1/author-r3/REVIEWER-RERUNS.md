# The reviewers' own scripts, rerun at `cbbb5ac`

Every script below is the reviewer's own, from the read-only packets
`pp131-r390-2-packet` and `pp131-r391-2-packet`, run on disposable `git archive` copies
of head `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` with the pinned Verilator 5.050. The
packets were not modified; where a script had to be adapted, the adapted copy is in
`receipts/` and the adaptation is stated. Receipts (SHA-256 in HANDOFF.md) are in
`receipts/`.

## R390-2

**Mutants** (`r390_2_mutants.py`, a copy with its `HEAD` constant set to this head; D3
section only, as the script runs it): `receipts/r390-2-mutants-head.txt`.

| Mutant | Round 2 | This head | Killing checks |
|---|---|---|---|
| `backoff_holds_dispatch` | KILLED | KILLED | `D3S10 backoff` |
| `disagree_one_direction` | KILLED | KILLED | `D3R4b` |
| `rollback_one_cycle` | KILLED | KILLED | `D3R4 strobe` |
| `backoff_derivation` | KILLED | KILLED | `D3S10 timing`, `D3S10 backoff` |
| `agg_removed` | KILLED | KILLED | 11 checks (D3R13 to D3R17) |
| `agg_one_late` | KILLED | KILLED | `D3R13 pass 0`, `D3R15 debt wait`, `D3R15 re-LOCATE` |
| `agg_restarts_on_go` | KILLED | KILLED | `D3R13 pass 0`, `D3R14` (both arms) |
| `agg_ignores_in_hand` (F3's S2) | SURVIVED | **KILLED** | `D3R17: the writer's grant`, `D3R17: once the device ends` |
| `agg_not_in_rollback` (F3) | SURVIVED | **KILLED** | `D3R15` (both arms, 4 checks) |
| `hold_unbounded` | KILLED | KILLED | D3O5, D3O6 (7) |
| `hold_until_any_terminal` | KILLED | KILLED | D3O5, D3O6 (4) |
| `hold_admits_two` | KILLED | KILLED | D3O5, D3O6 (5) |
| `hold_after_release` | SURVIVED the D3 section | SURVIVED the D3 section | as in round 2 the full `tb/pp_top` run kills it: `W21dd2`, `W21ee`, `U11g` (below) |
| `residency_counts_acmp` | KILLED | KILLED | D3O5, D3O6 (4) |
| `held_gate_ignores_da` | SURVIVED | SURVIVED | R390-2 judged it without effect (a frame already dropped lands in another counter) and raised no finding |

`hold_after_release` planted in an archive of this head and run over the full `tb/pp_top`
suite (default build): 7,855 checks, 3 failures, `W21dd2`, `W21ee` and `U11g`, the same
three R390-2 recorded in round 2 (`receipts/r390-hold_after_release-full-pp_top.log`).

**Probes** (`run_probes.sh`, unchanged: all five switches; `receipts/r390-probes-head.txt`):
- `--probe-hol`, `--probe-hol-restore`, `--probe-gaps`, `--probe-r2`: the same lines as
  their round-2 receipt (every GET_RX_STATE answered in CLOSED and during the slowed walk;
  A0-A4 at the aggregate; B1-B3 admission).
- `--probe-r2c` C1 (a grant forced at each of seven clocks around the bound): DEFAULTS at
  clock 1,000,001, drained, a later SET persisted, as in round 2 (their forced grant lands on
  the device, not on the writer's arbiter grant; D3R17 now lands it there).
- C2 (a pass-1 DEVICE error 300 or 3,000 clocks before the bound): k=300 ends **CLOSED at
  clock 1,000,001, cause 2**; k=3000 ends DEFAULTS, rolled back, at 997,547. Unchanged:
  the bound inside a roll-back ends it CLOSED (D3R15 grades both the debt wait and the
  re-LOCATE on the bound's own clock).

**Probe D1** (`probe_r2d.hpp` unchanged; `receipts/run_probe_r2d_head.sh` adds only the
probe and its switch, because the harness at this head already carries the per-byte knobs
under the reviewer's names `nv_hdr_every` / `nv_byte_every`; the header probe is told apart
by its offset 0 rather than by length 8, the same READs for this probe; receipt
`receipts/r390-probe-d1-head.txt`):
- erased: DEFAULTS at clock 1,000,544, as in round 2;
- **records saved: DEFAULTS at clock 1,000,005** (round 2: CLOSED at 1,000,001), the
  listener released at 1,000,003, binding cause 3, `rs_cause_o` 3, the longest D3 wait 0,
  image valid; afterwards own 0, ADP enabled, a READ_DESCRIPTOR answered.

## R391-2

**Mutants** (`r391_mutants2.py`, unchanged, `--tree` an archive of this head, D3 section):
15 of 15 KILLED (`receipts/r391-2-mutants-head.txt`), including its three round-2
survivors: `agg_fires_with_event_in_hand` (D3R17, 2 checks), `agg_not_stopped_at_terminal`
(D3R16, 3 checks) and `resident_never_returned` (D3O7).

**Probes** (`receipts/run_probes2-head.sh`, a copy of `run_probes2.sh` with two anchors
moved: P6/P7 hook the wrap after its new last port `dbg_d3_agg_fired_o`, and P8 no longer
patches the device model, whose per-byte knobs this head has; its header is used with
`nv_hdr_gap`/`nv_byte_gap` renamed to the harness's `nv_hdr_every`/`nv_byte_every`, same
semantics: the wait before each header and payload byte):
- P1-P5 (`receipts/r391-probes-P1-P6-head.txt`): the same results as round 2 (ACMP at 168
  cycles for every AECP backlog in CLOSED and during a walk, word 37 = n - 1; P3/P4 roll back
  to DEFAULTS; P5 ends at clock 1,000,544).
- P6 (AGG overridden to 2,800 in the probe copy, 5,802 runs): the script's oracle still
  encodes round 2's "CLOSED before the image is proven", so it flags 452 runs. They are
  exactly the 450 expiries in WAIT-GO and the 2 in IMAGE, each now **DONE (DEFAULTS),
  cause 3, rb 0, own 0**: the clarified behaviour. No other run deviates from its oracle;
  the RELOC expiries still end CLOSED.
- P7 (`receipts/r391-probe-P7-head.txt`): golden COMPLETE at clock 2,698 unchanged at clock
  20,000; the mutant still rolls it back (the in-tree D3R16 kills it).
- P8 (`receipts/r391-probe-P8-head.txt`): case A (both walks slowed per byte) now
  **restore_done at clock 1,000,005, DEFAULTS, cause 3, own 0** (round 2: CLOSED at
  1,000,001); case B unchanged (DEFAULTS at 1,000,544). The probe's `adp_enable 0` in both
  cases is its own `fresh()` resetting `entity_enable_i` after it set it (round 2 shows the
  same in case B); D3R14 grades the enable.
