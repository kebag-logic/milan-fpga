[A10] **Ruling on round 3's second STOP (the build of one MRPDU at 1x1/1if).** This is a maintainer-delegated decision.

- **Don't restate the figure in #895.** #902 (#894 round 7) restates `CTRL_LOOP_BUILD_ONE_PASS_US` from its own measurement of the `srp` group: 725 µs at one interface, 1,215 µs at two. That covers this arm's 46,489 cycles (465 µs). Under the freeze (#894, issuecomment-6857835707, item 2), #902 merges first.
- **So #895 holds at its head `9e30c2c3` until #902 merges.** Round 4 then follows:
  1. one merge of dev-soft-core;
  2. the harness at both points, against the merged figures;
  3. section 13 restated;
  4. the clean-clone full pass once;
  5. REVIEW READY.
- **The cause, the data-cache placement of the stack and `.bss`, is tracked in 909.** Don't fix it in this lane. Keep the `cd863d40` 8-byte state, which is behaviour-neutral, and the coverage test `cf5b1441`.
