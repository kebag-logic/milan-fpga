## Objective and observed evidence

At lwSRP `08ee86e8` an Applicant took two events at the device's own LeaveAll, so a stream withdrawal just after it was never sent as Lv (kebag-logic/lwSRP#20). At 8x8/1if, 351 of 387 such withdrawals were never sent; at 1x1/1if, 78 of 86. lwSRP PR #21 (merged as `d1bb4f4e`) fixes it. The platform still pins `08ee86e8`.

## Authoritative references

- IEEE 802.1Q-2022 10.7.5 (Applicant events at LeaveAll), Table 10-3, 10.7.5.9 (txLAF!).
- Milan v1.2 4.2.7 (SRP).

## Scope

In scope: move the lwSRP pin to `d1bb4f4e` at every pin site; a reproduction at the board level (a withdrawal after the own LeaveAll is sent as Lv within 240 ms, every input); the twin's Applicant grade for the own LeaveAll (txLA!, or txLAF! in a full MRPDU).

Out of scope: the srptx grade (#990).

## Acceptance criteria

1. The reproduction fails at `08ee86e8` and passes at `d1bb4f4e` at 1x1/1if and 8x8/1if.
2. The firmware gate, twin and plants, load and flip grades, harness and docs gates pass; tiles unchanged.

