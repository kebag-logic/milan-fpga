# srptx: the requested-transmit-opportunity [TIME] grade fails every scenario on dev-soft-core

## Objective and observed evidence

`make srptx` in `tb/verilator/milan_dp` (#867, the split build's SRP transmit path at the wire, graded by
`srptx_grade.py`) exits 2 on `dev-soft-core` at `aa30d77f`, with lwSRP at its pin `08ee86e8`. Every scenario fails:

| Scenario | Findings | MRPDUs | Kinds |
|---|---:|---:|---|
| `wire` | 1,108 | 1,459 | `[TIME]` MSRP 553, MVRP 555 |
| `hold` | 59 | 180 | `[TIME]` MSRP 29, MVRP 29; `[TX]` 1 |
| `licence` | 49 | 69 | `[TIME]` MSRP 24, MVRP 25 |
| off-grid controls (`licence` with the peer's LeaveAll at 16,240 and 16,280 ms) | 49 each | 69 each | as `licence` |

`make srptx-mutants` fails its own control for the same reason:
`FAIL control: the tracked sources must grade hold clean (rc 0)`.

The counts are the same at `854bd723`, the `dev-soft-core` before #961. There, 1,212 of the 1,216 finding lines
are identical. The other four (`licence`, ms 17000 and 22000) name the same frames with another delay.
With lwSRP moved to `d1bb4f4e` (lwSRP #20), the finding kinds are unchanged. Only the `[TIME]` count rises
(`wire` 1,185, `hold` 60, `licence` and each off-grid control 50) because declarations that fit a LeaveAll MRPDU no longer send two extra
Joins after it, so fewer MRPDUs leave (1,303 in `wire`) and more of them are periodic.

Every `[TIME]` finding is the requested-transmit-opportunity check of `srptx_grade.grade_time`, for example:

```text
[TIME] MSRP: a requested transmit opportunity at ms 2000, 810.001 ms after lwSRP last had nothing to send, past
JoinTime + T_svc (220 ms; IEEE 802.1Q-2018 10.7.4.1; Milan v1.2 4.2.7.1.1: a point-to-point requested transmit
opportunity occurs within JoinTime)
```

1,162 of the 1,215 such findings at `aa30d77f` are frames that leave on a whole second, the period of lwSRP's
periodic handler (100 centiseconds). The commonest delay is 810 ms (1,006 findings). So the check appears to grade
periodic transmit opportunities as requested ones. It dates the request from lwSRP's last poll that found nothing
to send. The SRP adapter polls lwSRP only when an MRPDU is owed, so that poll can be most of a second old. This is
the likely cause; the issue is to confirm or refute it.

The `[TX]` finding in `hold` is a separate check:
`the MAC refused every beat from ms 22000 to 25000, and the adapter never saw the SRP transmit ring full`.

No workflow runs `srptx`, `srptx-plants` or `srptx-mutants`, so CI is green while the leg is red.

## Authoritative references

- IEEE 802.1Q-2018 10.7.4 (the MRP timers; 10.7.4.1 the join timer and transmit opportunities), Table 10-7
  (timer values).
- Milan v1.2 4.2.7.1.1 (a point-to-point requested transmit opportunity occurs within JoinTime), Table 4.3.
- `docs/reference/FR_NFR.md` 3.4.1 (T_svc).
- `tb/verilator/milan_dp/README.md`, the srptx section (#867); `srptx_grade.py` `grade_time`; `srptx.hpp`.

## Context entry points

`tb/verilator/milan_dp/srptx_grade.py` (`grade_time`, `idle_us`), `tb/verilator/milan_dp/srptx.hpp` (what it records
as lwSRP's last idle poll), `sw/firmware/ctrl/srp/srp_mbx.c` (when the adapter polls lwSRP), `Makefile` targets
`srptx`, `srptx-plants`, `srptx-mutants`.

## Scope

In scope: find why periodic (or other non-requested) transmit opportunities are graded as requested ones, and fix
the grade or what it records so that it grades each transmit opportunity under the rule that applies to it. Find
why the `hold` scenario never sees the SRP transmit ring full, and fix the scenario or the check.

Out of scope: lwSRP, the adapter's transmit behaviour unless the investigation shows a real defect there (then a
separate issue), the twin's Applicant grade (`twin_mrp.py`).

## Acceptance criteria

1. `make srptx` exits 0 at the fixed head: 0 findings in `wire`, `hold` and `licence`, and the off-grid controls
   graded clean.
2. `make srptx-plants` and `make srptx-mutants` exit 0: each planted defect is still refused, including a requested
   transmit opportunity delayed past JoinTime + T_svc.
3. A new control shows that a periodic transmit opportunity is not graded as a requested one, and that a requested
   one past its bound still fails.
4. Decide whether `srptx` joins a CI workflow. If it does, register it in `scripts/suite_shards.py`.

## Validation

```sh
cd tb/verilator/milan_dp
make -k srptx; echo $?            # expect 0
make srptx-plants; echo $?        # expect 0
make srptx-mutants; echo $?       # expect 0
```

## Dependencies and lane conflicts

None blocking. The lwSRP pin bump to `d1bb4f4e` (lwSRP #20) changes the counts but not the kinds; either order works.

## Unresolved decisions

- Whether the requested-opportunity check should date the request from what the adapter records, or classify the
  opportunity by its trigger (Join timer, periodic, request).
- Whether `srptx` becomes a CI gate.
